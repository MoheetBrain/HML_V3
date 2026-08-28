# Validation Policy

## The defect

V1 passed `SEARCH_VALIDATION` to the controller and then selected on `SEARCH_DEV` metrics
anyway. A mutation that improved the dev sample became an elite whether or not the improvement
was real. That is precisely how a search overfits its own instrument, and with 489 candidates
evaluated over 30 generations there was ample opportunity.

## The rule, fixed before results

A child enters the elite population only when the improvement it *claimed* on `SEARCH_DEV` is
directionally reproduced on `SEARCH_VALIDATION`:

```
dev_gain        = signed improvement on the axis the hypothesis named
validation_gain = the same quantity on the validation split
eligible        <=>  validation_gain >= tolerance x dev_gain
```

| Parameter | Value | Why |
|---|---|---|
| `tolerance` | 0.5 | validation may retain as little as half the dev gain |
| `noise_floor` | 0.01 | relative changes under 1% are treated as no change |

Verdicts:

| Verdict | Meaning | Elite? |
|---|---|---|
| `REPRODUCED_ON_VALIDATION` | the gain survived | yes |
| `NO_CLAIM_TO_REPRODUCE` | the child claimed nothing measurable | yes |
| `NON_GENERALIZING_MUTATION` | dev improved, validation did not follow | **no** |
| `VALIDATION_CONTRADICTS_DEV` | dev improved, validation moved the other way | **no** |

The mission's own example — dev binder distance −30%, validation +8% — lands in
`VALIDATION_CONTRADICTS_DEV` and is quarantined. There is a test for exactly that case.

## What validation is not

Validation returns a *verdict and a divergence number*, never a gradient. It is never
optimised against directly, and no proposal is generated from validation metrics. A quarantined
candidate is retained in the registry as evidence, not deleted, because "this mutation does not
generalise" is a result worth keeping.

## Relationship to the sealed split

Neither dev nor validation is sealed. `SEALED_FINAL` is a third split, in another process,
touched once after convergence. Validation is the honesty gate *during* the search; the seal is
the honesty gate *on the search*.
