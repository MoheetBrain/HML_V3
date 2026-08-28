"""Synthetic adversarial states, generated from canonical semantics.

Real Lean traces under-represent several structures that a representation must survive:
deep binder nesting, shadowing, alpha-renaming, goal reordering with identical targets, long
dependency chains, large irrelevant contexts, and heavy metavariable obligation sets.

Every fixture here is *constructed* in the canonical schema — never produced by a language
model and never treated as verified mathematics. `FM-014` binds their interpretation: they
are a correctness and behaviour probe, and a locality result measured only on them is
reported as synthetic.
"""

from __future__ import annotations

from typing import Any

SYNTHETIC_PROVENANCE = {
    "source_file": "SYNTHETIC",
    "direct_imports": [],
    "lean_runtime_snapshot": {"synthetic": True},
}


def symbol(name: str, universes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {"node": "symbol", "identity": name, "universe_arguments": universes or []}


def apply(head: dict[str, Any], *arguments: dict[str, Any]) -> dict[str, Any]:
    result = head
    for argument in arguments:
        result = {"node": "application", "function": result, "argument": argument}
    return result


def local(identity: str) -> dict[str, Any]:
    return {"node": "local_reference", "identity": identity}


def metavariable(identity: str) -> dict[str, Any]:
    return {"node": "metavariable_reference", "identity": identity}


def bound(index: int) -> dict[str, Any]:
    return {"node": "bound_variable", "index": index}


def pi(binder_type: dict[str, Any], body: dict[str, Any], role: str = "EXPLICIT") -> dict[str, Any]:
    return {"node": "dependent_function", "binder_name": "_", "binder_role": role,
            "binder_type": binder_type, "body": body}


def lam(binder_type: dict[str, Any], body: dict[str, Any], role: str = "EXPLICIT") -> dict[str, Any]:
    return {"node": "lambda", "binder_name": "_", "binder_role": role,
            "binder_type": binder_type, "body": body}


def sort(level: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"node": "sort", "level": level or {"constructor": "zero"}}


def declaration(
    identity: str, display: str, type_expr: dict[str, Any],
    value: dict[str, Any] | None = None, binder_role: str = "EXPLICIT",
    declaration_role: str = "cdecl",
) -> dict[str, Any]:
    return {
        "identity": identity,
        "user_name_diagnostic": display,
        "binder_role": binder_role,
        "declaration_role": declaration_role,
        "type": type_expr,
        "value": value,
    }


def goal(identity: str, target: dict[str, Any], context: list[dict[str, Any]]) -> dict[str, Any]:
    return {"identity": identity, "target": target, "local_context": context,
            "local_instances": []}


def state(state_id: str, goals: list[dict[str, Any]],
          metavariables: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "state_id": state_id,
        "source_system": "SYNTHETIC",
        "goals": goals,
        "focus_order": [item["identity"] for item in goals],
        "metavariables": metavariables or [],
        "universe_assignments": [],
        "source_reference": {"runtime_state_sha256": "synthetic",
                             "raw_fvar_to_canonical": {}, "raw_mvar_to_canonical": {},
                             "relevant_metavariable_inventory_sha256": "synthetic",
                             "full_metavariable_inventory_count": len(metavariables or []),
                             "full_assigned_expression_count": 0},
        "information_accounting": {"synthetic": "CONSTRUCTED_FROM_CANONICAL_SEMANTICS"},
    }


def mvar(identity: str, kind: str = "natural", assigned: bool = False,
         assignment: dict[str, Any] | None = None,
         type_expr: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"identity": identity, "kind": kind, "type": type_expr or sort(),
            "assigned": assigned, "assignment": assignment}


def transition(
    name: str, before: dict[str, Any], after: dict[str, Any],
    premises: list[str] | None = None, local_refs: list[str] | None = None,
    delta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "canonical-math-transition-v2.0.0",
        "transition_id": name,
        "state_before": before,
        "state_after": after,
        "action": {
            "kind": "SYNTHETIC_STEP",
            "source_location": {"start": {}, "end": {}, "info_tree_path": []},
            "external_premise_refs": sorted(premises or []),
            "local_context_refs": [
                {"canonical_id": identity, "source_fvar_id": identity, "resolved": True}
                for identity in (local_refs or [])
            ],
            "reference_mechanism": "SYNTHETIC",
            "reference_completeness": "SYNTHETIC_COMPLETE_BY_CONSTRUCTION",
        },
        "state_delta": delta or {
            "delta_source": "SYNTHETIC", "goals_created": [], "goals_solved": [],
            "goals_preserved": [], "goals_reordered": False, "goals_modified": [],
            "focus_before": before["focus_order"][0] if before["focus_order"] else None,
            "focus_after": after["focus_order"][0] if after["focus_order"] else None,
            "focus_changed": False, "local_declarations_added": [],
            "local_declarations_removed": [], "local_declarations_changed": [],
            "metavariables_created": [], "metavariables_removed_from_inventory": [],
            "metavariables_assigned": [], "metavariables_changed": [],
            "external_premises_used": sorted(premises or []),
            "local_context_refs_used": sorted(local_refs or []),
            "expression_changes": {"goal_targets_changed": []},
        },
        "state_after_placeholder": None,
        "provenance": SYNTHETIC_PROVENANCE,
        "source_specific_reference": {
            "theorem_id": f"SYNTHETIC.{name}", "transition_index": 0,
            "fresh_trace_ordinal": 0, "elaborated_external_constant_refs": [],
        },
        "corpus_metadata": {
            "raw_file": "SYNTHETIC", "source_file": "SYNTHETIC",
            "theorem_family": "SYNTHETIC", "domain": "SYNTHETIC",
            "tactic_family": "synthetic", "official_split": "synthetic",
            "recorded_effect_class": "SYNTHETIC", "canonical_bytes": 0,
            "canonical_sha256": "synthetic",
        },
    }


def _identity(prefix: str, side: str, index: int) -> str:
    return f"{prefix}:{side}:{index}"


# ------------------------------------------------------------------------------ families


def _nested_pi(depth: int) -> dict[str, Any]:
    """A closed term: the innermost body cites the outermost binder."""

    body: dict[str, Any] = bound(depth - 1)
    for level in range(depth):
        body = pi(symbol("Nat"), body, "IMPLICIT" if level % 3 == 0 else "EXPLICIT")
    return body


def deep_binders(depth: int = 12) -> dict[str, Any]:
    context = [declaration(_identity("deep", "before", 0), "n", symbol("Nat"))]
    before = state("deep:before", [goal("deep:before:metavar:m0", _nested_pi(depth), context)])
    # One binder is discharged, so the after-state is the closed term one level shallower.
    after = state("deep:after", [goal("deep:after:metavar:m0", _nested_pi(depth - 1), context)])
    return transition("SYN_DEEP_BINDERS", before, after)


def alpha_renamed_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    """Two transitions differing only in Lean display spelling."""

    def build(names: tuple[str, str], tag: str) -> dict[str, Any]:
        context = [
            declaration(f"{tag}:before:local:f0", names[0], symbol("Nat")),
            declaration(f"{tag}:before:local:f1", names[1],
                        apply(symbol("Eq"), local(f"{tag}:before:local:f0"), symbol("Nat.zero"))),
        ]
        target = apply(symbol("Eq"), local(f"{tag}:before:local:f0"), symbol("Nat.zero"))
        before = state(f"{tag}:before", [goal(f"{tag}:before:metavar:m0", target, context)])
        after = state(f"{tag}:after", [goal(f"{tag}:after:metavar:m0", symbol("True"), [])])
        return transition(tag, before, after, local_refs=[f"{tag}:before:local:f1"])

    return build(("n", "h"), "SYN_ALPHA_A"), build(("k", "hk"), "SYN_ALPHA_B")


def shadowed_names() -> dict[str, Any]:
    """Three distinct declarations that Lean displays with the same user name."""

    context = [
        declaration("SYN_SHADOW:before:local:f0", "x", symbol("Nat")),
        declaration("SYN_SHADOW:before:local:f1", "x", symbol("Int")),
        declaration("SYN_SHADOW:before:local:f2", "x", symbol("Real")),
    ]
    target = apply(symbol("Eq"), local("SYN_SHADOW:before:local:f2"),
                   local("SYN_SHADOW:before:local:f0"))
    before = state("SYN_SHADOW:before", [goal("SYN_SHADOW:before:metavar:m0", target, context)])
    after = state("SYN_SHADOW:after", [goal("SYN_SHADOW:after:metavar:m0", symbol("True"), [])])
    return transition("SYN_SHADOWED_NAMES", before, after,
                      local_refs=["SYN_SHADOW:before:local:f0"])


def reordered_goals() -> dict[str, Any]:
    """Two goals with byte-identical targets exchanged by a focus change."""

    target = apply(symbol("Eq"), symbol("Nat.zero"), symbol("Nat.zero"))
    first = goal("SYN_REORDER:before:metavar:m0", target, [])
    second = goal("SYN_REORDER:before:metavar:m1", target, [])
    before = state("SYN_REORDER:before", [first, second])
    after = state("SYN_REORDER:after", [second, first])
    delta = dict(transition("x", before, after)["state_delta"])
    delta["goals_reordered"] = True
    delta["goals_preserved"] = sorted([first["identity"], second["identity"]])
    return transition("SYN_REORDERED_GOALS", before, after, delta=delta)


def long_dependency_chain(length: int = 14) -> dict[str, Any]:
    context: list[dict[str, Any]] = [
        declaration("SYN_CHAIN:before:local:f0", "a0", symbol("Nat")),
    ]
    for index in range(1, length):
        previous = f"SYN_CHAIN:before:local:f{index - 1}"
        context.append(declaration(
            f"SYN_CHAIN:before:local:f{index}", f"a{index}",
            apply(symbol("Eq"), local(previous), symbol("Nat.zero")),
        ))
    target = apply(symbol("Eq"), local("SYN_CHAIN:before:local:f0"),
                   local(f"SYN_CHAIN:before:local:f{length - 1}"))
    before = state("SYN_CHAIN:before", [goal("SYN_CHAIN:before:metavar:m0", target, context)])
    after = state("SYN_CHAIN:after", [goal("SYN_CHAIN:after:metavar:m0", symbol("True"), [])])
    return transition("SYN_LONG_DEPENDENCY_CHAIN", before, after,
                      local_refs=[f"SYN_CHAIN:before:local:f{length - 1}"])


def large_irrelevant_context(size: int = 40) -> dict[str, Any]:
    context = [
        declaration(f"SYN_NOISE:before:local:f{index}", f"noise{index}", symbol("Nat"))
        for index in range(size)
    ]
    context.append(declaration("SYN_NOISE:before:local:key", "key",
                               apply(symbol("Eq"), symbol("Nat.zero"), symbol("Nat.zero"))))
    target = local("SYN_NOISE:before:local:key")
    before = state("SYN_NOISE:before", [goal("SYN_NOISE:before:metavar:m0", target, context)])
    after = state("SYN_NOISE:after", [goal("SYN_NOISE:after:metavar:m0", symbol("True"), [])])
    return transition("SYN_LARGE_IRRELEVANT_CONTEXT", before, after,
                      local_refs=["SYN_NOISE:before:local:key"])


def many_obligations(count: int = 12) -> dict[str, Any]:
    metavariables = [
        mvar(f"SYN_OBLIG:before:metavar:m{index}",
             assigned=index % 3 == 0,
             assignment=symbol("Nat.zero") if index % 3 == 0 else None)
        for index in range(count)
    ]
    target = apply(symbol("Eq"), metavariable("SYN_OBLIG:before:metavar:m1"), symbol("Nat.zero"))
    before = state("SYN_OBLIG:before", [goal("SYN_OBLIG:before:metavar:g0", target, [])],
                   metavariables)
    after_metavariables = [
        mvar(item["identity"], assigned=True, assignment=symbol("Nat.zero"))
        for item in metavariables
    ]
    after = state("SYN_OBLIG:after", [goal("SYN_OBLIG:after:metavar:g0", symbol("True"), [])],
                  after_metavariables)
    return transition("SYN_MANY_OBLIGATIONS", before, after)


def overloaded_notation() -> dict[str, Any]:
    """Two occurrences of one name at different universe levels, plus a coercion."""

    zero_low = symbol("OfNat.ofNat", [{"constructor": "zero"}])
    zero_high = symbol("OfNat.ofNat", [{"constructor": "succ", "of": {"constructor": "zero"}}])
    coerced = apply(symbol("Nat.cast", [{"constructor": "param", "name": "u_1"}]), zero_low)
    target = apply(symbol("Eq"), coerced, zero_high)
    context = [declaration("SYN_OVER:before:local:f0", "inst✝", symbol("CommRing"),
                           binder_role="INSTANCE_IMPLICIT", declaration_role="cdecl")]
    before = state("SYN_OVER:before", [goal("SYN_OVER:before:metavar:m0", target, context)])
    after = state("SYN_OVER:after", [goal("SYN_OVER:after:metavar:m0", symbol("True"), [])])
    return transition("SYN_OVERLOADED_NOTATION", before, after,
                      premises=["Nat.cast_zero", "OfNat.ofNat"])


def identifier_reuse() -> dict[str, Any]:
    """A local display name that collides with a global constant's last component."""

    context = [
        declaration("SYN_REUSE:before:local:f0", "add", symbol("Nat")),
        declaration("SYN_REUSE:before:local:f1", "Nat", symbol("Type")),
    ]
    target = apply(symbol("Nat.add"), local("SYN_REUSE:before:local:f0"),
                   local("SYN_REUSE:before:local:f1"))
    before = state("SYN_REUSE:before", [goal("SYN_REUSE:before:metavar:m0", target, context)])
    after = state("SYN_REUSE:after", [goal("SYN_REUSE:after:metavar:m0", symbol("True"), [])])
    return transition("SYN_IDENTIFIER_REUSE", before, after, premises=["Nat.add"])


def let_values() -> dict[str, Any]:
    value = apply(symbol("Nat.add"), symbol("Nat.zero"), symbol("Nat.zero"))
    context = [
        declaration("SYN_LET:before:local:f0", "base", symbol("Nat"), value=value,
                    declaration_role="ldecl"),
    ]
    target = apply(symbol("Eq"), local("SYN_LET:before:local:f0"), symbol("Nat.zero"))
    before = state("SYN_LET:before", [goal("SYN_LET:before:metavar:m0", target, context)])
    after = state("SYN_LET:after", [goal("SYN_LET:after:metavar:m0", symbol("True"), [])])
    return transition("SYN_LET_VALUES", before, after)


def unicode_glyphs() -> dict[str, Any]:
    """Names carrying exactly the glyphs FM-004 priced."""

    context = [
        declaration("SYN_GLYPH:before:local:f0", "inst✝³⁰", symbol("CommRing"),
                    binder_role="INSTANCE_IMPLICIT"),
        declaration("SYN_GLYPH:before:local:f1", "𝕜", symbol("Type")),
    ]
    target = apply(symbol("Membership.mem"), local("SYN_GLYPH:before:local:f1"), symbol("ℝ"))
    before = state("SYN_GLYPH:before", [goal("SYN_GLYPH:before:metavar:m0", target, context)])
    after = state("SYN_GLYPH:after", [goal("SYN_GLYPH:after:metavar:m0", symbol("∀"), [])])
    return transition("SYN_UNICODE_GLYPHS", before, after, premises=["Set.mem_ℝ"])


def shared_subterms() -> dict[str, Any]:
    repeated = apply(symbol("Nat.add"), apply(symbol("Nat.succ"), symbol("Nat.zero")),
                     apply(symbol("Nat.succ"), symbol("Nat.zero")))
    context = [
        declaration("SYN_SHARE:before:local:f0", "h0",
                    apply(symbol("Eq"), repeated, repeated)),
        declaration("SYN_SHARE:before:local:f1", "h1",
                    apply(symbol("Eq"), repeated, symbol("Nat.zero"))),
    ]
    target = apply(symbol("Eq"), repeated, repeated)
    before = state("SYN_SHARE:before", [goal("SYN_SHARE:before:metavar:m0", target, context)])
    after = state("SYN_SHARE:after", [goal("SYN_SHARE:after:metavar:m0", symbol("True"), [])])
    return transition("SYN_SHARED_SUBTERMS", before, after)


def branch_local_premises() -> dict[str, Any]:
    left = goal("SYN_BRANCH:before:metavar:m0",
                apply(symbol("Or.inl"), symbol("True")),
                [declaration("SYN_BRANCH:before:local:f0", "hl", symbol("True"))])
    right = goal("SYN_BRANCH:before:metavar:m1",
                 apply(symbol("Or.inr"), symbol("False")),
                 [declaration("SYN_BRANCH:before:local:f1", "hr", symbol("False"))])
    before = state("SYN_BRANCH:before", [left, right])
    after = state("SYN_BRANCH:after", [right])
    return transition("SYN_BRANCH_LOCAL_PREMISES", before, after,
                      premises=["Or.inl"], local_refs=["SYN_BRANCH:before:local:f0"])


def all_fixtures() -> list[dict[str, Any]]:
    alpha_a, alpha_b = alpha_renamed_pair()
    return [
        deep_binders(),
        alpha_a,
        alpha_b,
        shadowed_names(),
        reordered_goals(),
        long_dependency_chain(),
        large_irrelevant_context(),
        many_obligations(),
        overloaded_notation(),
        identifier_reuse(),
        let_values(),
        unicode_glyphs(),
        shared_subterms(),
        branch_local_premises(),
    ]


FIXTURE_PURPOSE = {
    "SYN_DEEP_BINDERS": "deep binder nesting and De Bruijn depth",
    "SYN_ALPHA_A": "alpha-renaming: identity must not depend on display spelling",
    "SYN_ALPHA_B": "alpha-renaming counterpart",
    "SYN_SHADOWED_NAMES": "three distinct declarations sharing one display name",
    "SYN_REORDERED_GOALS": "goal reordering with byte-identical targets",
    "SYN_LONG_DEPENDENCY_CHAIN": "long local dependency chain; the locality instrument",
    "SYN_LARGE_IRRELEVANT_CONTEXT": "one relevant declaration among forty irrelevant ones",
    "SYN_MANY_OBLIGATIONS": "heavy metavariable obligation set with partial assignment",
    "SYN_OVERLOADED_NOTATION": "one name at two universe levels, plus a coercion",
    "SYN_IDENTIFIER_REUSE": "local names colliding with global constant components",
    "SYN_LET_VALUES": "let-bound declarations carrying values",
    "SYN_UNICODE_GLYPHS": "the exact glyph family priced by FM-004",
    "SYN_SHARED_SUBTERMS": "repeated maximal subterms; the DAG-hoisting instrument",
    "SYN_BRANCH_LOCAL_PREMISES": "branch-local hypotheses across sibling goals",
}
