# Primitive Registry

## What it decides

A meta-designer can propose any axis it likes. This registry decides which proposals the
compiler can actually *execute*, and records the rest rather than discarding them.

An invented axis is accepted when its declared behaviour binds to a projection hook:

| Hook | Behaviour | Answers |
|---|---|---|
| `neighbourhood_capsule` | move the declarations a goal cites adjacent to that goal; the global context is unchanged and every declaration still appears exactly once | binder and dependency distance |
| `duplicate_adjacent` | restate one field of a record next to the record that consumes it | locality and corruption detection, at a token cost |
| `section_partition` | emit one record kind in its own block, before or after the rest | obligation and metavariable visibility |
| `record_reorder` | reorder records of one kind by a declared key | layout without content change |

Binding is by explicit `projection_hook`, or inferred from behaviour keywords. A proposal that
binds to nothing is stored with `status: ACCEPTED_UNIMPLEMENTABLE` — it is evidence about what
the meta-designer wanted and what the compiler could not do.

## Acceptance conditions

1. it addresses a documented failure;
2. it is representation-level — `implementation_layer` may not name the canonical state;
3. it binds to an executable hook;
4. it preserves the semantic round-trip;
5. it names a mechanism-specific test;
6. at least one value differs observably on the corpus;
7. its claimed mechanism is falsifiable;
8. it does not leak answers.

Every accepted axis gets a `NONE` value whether or not the proposal included one. Without an
off position the axis cannot be attributed: there would be no candidate differing only by not
having the feature.

## Schema versioning

Accepting an axis bumps the genome schema to `representation-genome-v2.N.0`. Older genomes are
read with absent-means-`NONE`, so a candidate evaluated before the axis existed re-renders
byte-identically after it exists. That property is asserted by a test and is the only reason
cross-generation comparisons remain legitimate.

## Worked example, measured

A `NEW_PRIMITIVE` proposal named `dependency_capsule` bound to `neighbourhood_capsule`:

| Step | Result |
|---|---|
| schema validation | passed |
| static safety | no forbidden reference |
| hook inference | `neighbourhood_capsule` |
| genome | 42 -> 43 axes; 4.095e19 -> 1.228e20 points |
| candidate id | distinct from its parent |
| hard gates | all passed |
| round-trip | preserved on all 14 adversarial fixtures |
| effect, `goal_position=AFTER_CONTEXT` | **no-op**, renders byte-identically |
| effect, `goal_position=FIRST` | binder-query distance **176.9 -> 104.7 tokens (-41%)** |

The conditional effect is the interesting part: the axis only does work when the goal precedes
its context, which is an interaction between an invented axis and an existing one. A search
confined to the original 42 axes could not have represented that hypothesis, let alone tested
it.

## The honest limit

This is open-endedness *within a projection algebra*. The system can invent combinations and
applications of four mechanisms and can notice when the problem is the corpus or the
instruments rather than the language. It cannot invent a mechanism outside the algebra;
proposals that need one are recorded, and adding a fifth hook is a code change with tests.
