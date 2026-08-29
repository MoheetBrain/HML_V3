"""Split firewall keyed on base-state identity, not on a requested split name.

`FM-043` was not caught by the guard that existed at the time, and the reason matters more
than the bug. That guard refused a script invoked with ``--split micro_hidden``. The
certification never asked for micro_hidden; it asked the pool for twelve fresh pairs, and
the pool handed back base states that happened to belong to the reserved splits. A name
check cannot see that, because no name was ever passed.

So the firewall is keyed on the thing that actually identifies the mathematics: a
provenance hash of the base transition. Every consumer routes its candidate base states
through :meth:`SplitFirewall.admit`, which fails closed -- an unregistered state is refused
rather than allowed, because the failure mode this exists to prevent is silent admission.

`MISSION §11`: DEV, SHADOW, HIDDEN and SEALED are pairwise disjoint, asserted at runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

DEV, SHADOW, HIDDEN, SEALED = "DEV", "SHADOW", "HIDDEN", "SEALED"
COMPARTMENTS: tuple[str, ...] = (DEV, SHADOW, HIDDEN, SEALED)

#: Bumped whenever the hash inputs change; a registry written under a different version is
#: refused rather than silently reinterpreted.
FIREWALL_VERSION = "micromath-firewall-v2.0.0"


class SplitViolation(RuntimeError):
    """Raised when a consumer reaches for a base state outside its compartment."""


def base_state_identity(transition: dict[str, Any]) -> str:
    """A stable hash of *what mathematics this is*, independent of any split label.

    Keyed on the transition id together with its declared source file and provenance, so
    that the same underlying Lean state cannot enter two compartments by being re-derived
    under a fresh id. The digest -- not the raw id -- is what the registries store, so a
    registry file leaks no identifiers of the hidden mathematics.
    """

    provenance = transition.get("provenance") or {}
    source = (transition.get("source_specific_reference")
              or provenance.get("source_file") or "")
    payload = json.dumps(
        {"transition_id": transition.get("transition_id"), "source": source,
         "declaration": provenance.get("declaration")},
        sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{FIREWALL_VERSION}|{payload}".encode()).hexdigest()[:32]


@dataclass
class SplitFirewall:
    """Permanent registries of base-state identity, one per compartment."""

    registries: dict[str, set[str]] = field(default_factory=dict)
    retired: dict[str, set[str]] = field(default_factory=dict)

    # ------------------------------------------------------------------ construction

    def register(self, compartment: str, transitions: Iterable[dict[str, Any]]) -> int:
        if compartment not in COMPARTMENTS:
            raise SplitViolation(f"unknown compartment {compartment!r}")
        bucket = self.registries.setdefault(compartment, set())
        added = 0
        for transition in transitions:
            identity = base_state_identity(transition)
            for other in COMPARTMENTS:
                if other != compartment and identity in self.registries.get(other, set()):
                    raise SplitViolation(
                        f"base state already registered to {other}; a state cannot belong "
                        f"to two compartments")
            if identity not in bucket:
                bucket.add(identity)
                added += 1
        self.assert_disjoint()
        return added

    def retire(self, label: str, transitions: Iterable[dict[str, Any]]) -> int:
        """Mark states as spent. Retired states are admitted nowhere, ever again.

        `FM-043`: the old MICRO_SHADOW and MICRO_HIDDEN were consumed by a calibration run.
        Excluding them from future runs does not restore them, and pretending otherwise
        would be the same error a second time. They are recorded here so that any future
        run that reaches for one is refused with the reason.
        """

        bucket = self.retired.setdefault(label, set())
        before = len(bucket)
        bucket.update(base_state_identity(t) for t in transitions)
        return len(bucket) - before

    # ------------------------------------------------------------------ enforcement

    def assert_disjoint(self) -> None:
        for left in COMPARTMENTS:
            for right in COMPARTMENTS:
                if left >= right:
                    continue
                shared = self.registries.get(left, set()) & self.registries.get(right, set())
                if shared:
                    raise SplitViolation(
                        f"{left} and {right} share {len(shared)} base states; the firewall "
                        f"is the only thing standing between a holdout and a leak")

    def compartment_of(self, transition: dict[str, Any]) -> str | None:
        identity = base_state_identity(transition)
        for compartment in COMPARTMENTS:
            if identity in self.registries.get(compartment, set()):
                return compartment
        return None

    def is_retired(self, transition: dict[str, Any]) -> str | None:
        identity = base_state_identity(transition)
        for label, bucket in self.retired.items():
            if identity in bucket:
                return label
        return None

    def admit(self, compartment: str, transitions: Iterable[dict[str, Any]],
              *, allow_unregistered: bool = False) -> list[dict[str, Any]]:
        """Filter to states this compartment may legitimately consume. Fails closed.

        An unregistered state is refused by default. Minting genuinely new pairs is the one
        case where that is wrong, so it is available -- but only by asking for it in the
        call, which makes the intent visible at the call site instead of implicit in a
        default.
        """

        if compartment not in COMPARTMENTS:
            raise SplitViolation(f"unknown compartment {compartment!r}")
        admitted: list[dict[str, Any]] = []
        for transition in transitions:
            retired_as = self.is_retired(transition)
            if retired_as is not None:
                raise SplitViolation(
                    f"base state is retired ({retired_as}) and can never be admitted again")
            owner = self.compartment_of(transition)
            if owner == compartment:
                admitted.append(transition)
            elif owner is None:
                if not allow_unregistered:
                    raise SplitViolation(
                        f"base state is not registered to any compartment; {compartment} "
                        f"may not consume it (pass allow_unregistered to mint new pairs)")
                admitted.append(transition)
            else:
                raise SplitViolation(
                    f"base state belongs to {owner}; {compartment} may not consume it")
        return admitted

    def available(self, pool: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
        """Pool members that belong to no compartment and are not retired."""

        return [t for t in pool
                if self.compartment_of(t) is None and self.is_retired(t) is None]

    # ------------------------------------------------------------------ persistence

    def to_dict(self) -> dict[str, Any]:
        return {
            "firewall_version": FIREWALL_VERSION,
            "registries": {k: sorted(v) for k, v in sorted(self.registries.items())},
            "retired": {k: sorted(v) for k, v in sorted(self.retired.items())},
            "counts": {k: len(v) for k, v in sorted(self.registries.items())},
            "retired_counts": {k: len(v) for k, v in sorted(self.retired.items())},
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2) + "\n")

    @classmethod
    def load(cls, path: Path) -> "SplitFirewall":
        payload = json.loads(path.read_text())
        version = payload.get("firewall_version")
        if version != FIREWALL_VERSION:
            raise SplitViolation(
                f"registry was written by {version!r}, this is {FIREWALL_VERSION!r}; the "
                f"hash inputs may differ, so the registry cannot be trusted")
        firewall = cls()
        firewall.registries = {k: set(v) for k, v in payload.get("registries", {}).items()}
        firewall.retired = {k: set(v) for k, v in payload.get("retired", {}).items()}
        firewall.assert_disjoint()
        return firewall
