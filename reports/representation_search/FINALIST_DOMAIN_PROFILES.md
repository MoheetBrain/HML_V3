# Finalist Domain Profiles

A frontier table reports averages. This asks the question a user of the language asks first: **does the candidate that wins on average also win on the mathematics I work in?** Each finalist is measured on each Mathlib domain separately.

Domains with at least 8 transitions in the dev and validation splits, sampled to 12 transitions each. The sealed split is not read.

| Domain | Transitions available |
|---|---:|
| `Algebra` | 12 |
| `Analysis` | 12 |
| `CategoryTheory` | 12 |
| `Combinatorics` | 12 |
| `Computability` | 12 |
| `Data` | 12 |
| `LinearAlgebra` | 12 |
| `MeasureTheory` | 12 |
| `NumberTheory` | 12 |
| `Order` | 12 |
| `RingTheory` | 12 |
| `SetTheory` | 12 |
| `Topology` | 12 |
| `packages` | 12 |
| `GroupTheory` | 10 |
| `Probability` | 10 |

## Where each finalist leads

Number of Pareto axes on which the finalist is the best of the finalists, per domain. Seven axes, so seven is a clean sweep.

| Finalist | Shortlisted because | Domains led | Best domains |
|---|---|---:|---|
| `R_0412a34e70c7` | best_on:detect_drop_field | 14 | `Algebra` (2/7), `LinearAlgebra` (2/7), `Probability` (2/7) |
| `R_043bb2c2cfac` | best_on:max_reference_span_tokens | 18 | `Combinatorics` (3/7), `Computability` (2/7), `SetTheory` (2/7) |
| `R_1a776db1d4c0` | best_on:binder_use_distance_tokens | 16 | `Algebra` (1/7), `Analysis` (1/7), `CategoryTheory` (1/7) |
| `R_37383109997e` | best_on:bpe_tokens_per_transition | 21 | `Algebra` (2/7), `Analysis` (2/7), `Order` (2/7) |
| `R_8ae4ba2c1f7e` | best_on:detect_swap_records | 5 | `Computability` (1/7), `Data` (1/7), `MeasureTheory` (1/7) |
| `R_9044f4984fce` | knee | 3 | `CategoryTheory` (1/7), `GroupTheory` (1/7), `MeasureTheory` (1/7) |
| `R_9ea6caecfa33` | best_on:premise_to_action_distance_tokens | 19 | `GroupTheory` (2/7), `NumberTheory` (2/7), `RingTheory` (2/7) |
| `R_cf8323f05a83` | best_on:identifier_fragmentation | 16 | `Algebra` (1/7), `Analysis` (1/7), `CategoryTheory` (1/7) |

## Per-domain axis leaders

| Domain | `bpe_tokens_per_transition` | `binder_use_distance_tokens` | `premise_to_action_distance_tokens` | `detect_swap_records` | `detect_drop_field` | `identifier_fragmentation` | `max_reference_span_tokens` |
|---|---|---|---|---|---|---|---|
| `Algebra` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_0412a34e70c7` | `R_0412a34e70c7` | `R_cf8323f05a83` | `R_37383109997e` |
| `Analysis` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_043bb2c2cfac` | `R_0412a34e70c7` | `R_cf8323f05a83` | `R_37383109997e` |
| `CategoryTheory` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_0412a34e70c7` | `R_9044f4984fce` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `Combinatorics` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_043bb2c2cfac` | `R_043bb2c2cfac` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `Computability` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_043bb2c2cfac` | `R_8ae4ba2c1f7e` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `Data` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_0412a34e70c7` | `R_8ae4ba2c1f7e` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `GroupTheory` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_9ea6caecfa33` | `R_9044f4984fce` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `LinearAlgebra` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_0412a34e70c7` | `R_0412a34e70c7` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `MeasureTheory` | `R_37383109997e` | `R_1a776db1d4c0` | `R_8ae4ba2c1f7e` | `R_043bb2c2cfac` | `R_9ea6caecfa33` | `R_cf8323f05a83` | `R_9044f4984fce` |
| `NumberTheory` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_0412a34e70c7` | `R_9ea6caecfa33` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `Order` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_043bb2c2cfac` | `R_0412a34e70c7` | `R_cf8323f05a83` | `R_37383109997e` |
| `Probability` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_0412a34e70c7` | `R_0412a34e70c7` | `R_cf8323f05a83` | `R_37383109997e` |
| `RingTheory` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_0412a34e70c7` | `R_9ea6caecfa33` | `R_cf8323f05a83` | `R_37383109997e` |
| `SetTheory` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_043bb2c2cfac` | `R_0412a34e70c7` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `Topology` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_043bb2c2cfac` | `R_8ae4ba2c1f7e` | `R_cf8323f05a83` | `R_043bb2c2cfac` |
| `packages` | `R_37383109997e` | `R_1a776db1d4c0` | `R_9ea6caecfa33` | `R_8ae4ba2c1f7e` | `R_0412a34e70c7` | `R_cf8323f05a83` | `R_043bb2c2cfac` |

## Is the ranking a property of the representation or of the mathematics?

For each axis: the finalist that leads in the most domains, and in how many. A high share means the ranking on that axis is a property of the representation; a low share means the axis is measuring the mathematics as much as the encoding.

| Axis | Modal leader | Domains led | Share |
|---|---|---:|---:|
| `bpe_tokens_per_transition` | `R_37383109997e` | 16/16 | 100% |
| `binder_use_distance_tokens` | `R_1a776db1d4c0` | 16/16 | 100% |
| `premise_to_action_distance_tokens` | `R_9ea6caecfa33` | 15/16 | 94% |
| `detect_swap_records` | `R_0412a34e70c7` | 7/16 | 44% |
| `detect_drop_field` | `R_0412a34e70c7` | 7/16 | 44% |
| `identifier_fragmentation` | `R_cf8323f05a83` | 16/16 | 100% |
| `max_reference_span_tokens` | `R_043bb2c2cfac` | 10/16 | 62% |

## How much the domain changes the answer

The best achievable value on each axis, across domains. A wide range means the axis is measuring the mathematics as much as the representation.

| Axis | Best domain value | Worst domain value | SD across domains |
|---|---:|---:|---:|
| `bpe_tokens_per_transition` | 4,474.917 | 9,255.083 | 1,376.938 |
| `binder_use_distance_tokens` | 142.289 | 384.634 | 69.196 |
| `premise_to_action_distance_tokens` | 11.750 | 23.058 | 3.316 |
| `detect_swap_records` | 0.833 | 1.000 | 0.047 |
| `detect_drop_field` | 0.667 | 0.917 | 0.068 |
| `identifier_fragmentation` | 1.637 | 1.850 | 0.058 |
| `max_reference_span_tokens` | 1,678.583 | 4,089.750 | 636.536 |
