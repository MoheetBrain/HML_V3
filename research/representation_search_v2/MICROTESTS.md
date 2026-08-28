# Mechanism-Specific Microtests

## Why the Pareto vector was not enough

The V1 selection axes measured cost and *aggregate* locality. They cannot see that a candidate
is cheap on average while every specific structural question is expensive. The question a
reader of the language actually has to answer is not "what is the mean reference distance" but
"given this rendering, which binder owns this use?"

## Shape

Every suite is the same shape, and the ground truth never comes from a rendering or a model:

```
question  <- derived from CanonicalMathState
answer    <- derived from CanonicalMathState
measured  <- how expensive the answer is to locate in R(M)
```

Measured means: character and token distance from the question site to the nearest correct
answer, how many competing occurrences the reader must disambiguate between, and whether the
answer is present at all.

| Suite | Question |
|---|---|
| `binder_query` | which local declaration does the goal's target use? |
| `scope_query` | which goal scopes this declaration? |
| `dependency_query` | which declaration does this declaration's type depend on? |
| `premise_query` | which premise does the action cite? |
| `goal_query` | which goal is focused; do after-state goals correspond to before-state ones? |
| `type_query` | what is the head symbol of this declaration's type? |
| `metavar_query` | which obligation does this metavariable reference point at? |
| `action_argument_query` | which local declaration does the action consume? |
| `delta_query` | which goals did this step solve or create? |

## `unanswerable` is a measurement, not a crash

A candidate that omits dependency edges genuinely cannot answer a dependency query. The number
that matters is how often. `delta_visibility=DERIVABLE_ONLY` reads 1.00 unanswerable on
`delta_query`, which is correct and is the point.

Zero queries and 100% answered are different things and are reported differently: `queries` is
always reported beside the rate.

## Two instrument defects found and fixed

Both were found by checking the instrument against a real rendering rather than trusting it.

**Identity encoding.** The suites initially read 100% unanswerable on four of nine. The cause
was a heuristic of mine: whether to route an identity through the candidate's identity codec
was decided by testing for a colon in the identity. The committed corpus uses short identities
(`m9`, `f17`), so the test was false and the suite searched for `m9` in a rendering containing
`bm9`. Every identity now routes through the codec, which returns unknown names unchanged, so
the same code path is correct for both canonical identities and global constants. Recorded as
`FM-025`.

**Relational scope.** The delta suite reported a hidden relation as *answered*, because it
found the goal identity anywhere in the rendering rather than inside a stated delta. Finding a
goal id in the before-state does not answer "which goals did this step solve?". Relational
queries now only count an answer that appears inside the section that states the relation.

## Anchors

Queries anchored to a record rather than an identity (`ACTION`, `DELTA`, `FOCUS`) locate that
record's role word. An earlier version measured from character 0, which reports distance into
the document — a property of document length, not of structure.
