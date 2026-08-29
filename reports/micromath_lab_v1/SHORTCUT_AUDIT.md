# Shortcut audit — MicroMath Lab V1 (`micro_dev`, 29 pairs / 58 items)

Every pair is a transposition counterfactual: state B is a permutation of state A, so the two
states carry an identical token multiset by construction. This audit asks whether a rule that
never reads the mathematics can still beat chance (0.500).

Four answer-targeted rules were tested against every representation, in aggregate and per
stress cell. A cell leaks if any dumb rule scores materially above 0.500.

## Worst dumb rule per stress, across all 11 representations

| Stress | Best dumb rule | Accuracy | Rule / representation | Certification |
|---|---|---|---|---|
| ACTION_ARGUMENT | always_first_option | 0.500 | LEAN_LIKE | INSTRUMENT_LIMIT |
| BINDER | always_first_option | 0.500 | LEAN_LIKE | INSTRUMENT_LIMIT |
| DEPENDENCY | always_first_option | 0.500 | LEAN_LIKE | INSTRUMENT_INVALID |
| EXPRESSION_DEPTH | always_first_option | 0.500 | LEAN_LIKE | CONTROL_PARITY |
| MULTI_GOAL | always_first_option | 0.500 | LEAN_LIKE | CONTROL_PARITY |
| PREMISE | more_frequent_option | 0.562 | LEAN_LIKE | INSTRUMENT_INVALID |
| SCOPE | always_first_option | 0.500 | LEAN_LIKE | INSTRUMENT_INVALID |
| TYPE | always_first_option | 0.500 | LEAN_LIKE | INSTRUMENT_INVALID |

Highest aggregate dumb-rule accuracy across all representations: **0.509** (LEAN_LIKE),
against a chance baseline of 0.500.

## Reading

No positional or frequency heuristic beats chance by a meaningful margin on any cell. The
benchmark is not solvable by surface tricks, and the transposition design does control for
length, vocabulary and token frequency.

This audit is nevertheless **not sufficient**, and the component certification proved it. A
dumb rule that ignores content cannot pass — but a reader that uses *mathematical priors in the
identifiers* can, and four cells are answerable that way with the target relation destroyed.
See FM-041 and `COMPONENT_DASHBOARD.md`. A clean shortcut audit is necessary, not sufficient;
only the calibrated negative arm detects semantic-prior leakage.

Machine-readable source: `AUDIT_micro_dev.json`.
