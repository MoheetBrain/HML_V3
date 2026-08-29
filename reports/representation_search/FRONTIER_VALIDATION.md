# Frontier Validation

Selection read `SEARCH_DEV` every generation. If the finalists' ordering were an artifact of that sample, it would not survive on `SEARCH_VALIDATION`, which selection never touched. The sealed split is not read here either.

Finalists measured on 40 dev and 40 validation transitions.

**5 of 7 axes keep the same leader.**

| Axis | Dev leader | Validation leader | Same | Spearman rho |
|---|---|---|---|---:|
| `bpe_tokens_per_transition` | `R_c8a70a62eebb` | `R_c8a70a62eebb` | yes | +1.000 |
| `binder_use_distance_tokens` | `R_9f3eb215d943` | `R_9f3eb215d943` | yes | +0.943 |
| `premise_to_action_distance_tokens` | `R_c8a70a62eebb` | `R_c8a70a62eebb` | yes | +0.943 |
| `detect_swap_records` | `R_211cd0165db9` | `R_0412a34e70c7` | **no** | +0.657 |
| `detect_drop_field` | `R_0412a34e70c7` | `R_9044f4984fce` | **no** | +0.829 |
| `identifier_fragmentation` | `R_cf8323f05a83` | `R_cf8323f05a83` | yes | +1.000 |
| `max_reference_span_tokens` | `R_c8a70a62eebb` | `R_c8a70a62eebb` | yes | +0.829 |

A rho near +1 means the finalists rank the same way on data selection never saw. A rho near 0 means the axis is measuring the sample. Neither is a statement about a model: both splits are static measurements of the same static representations.
