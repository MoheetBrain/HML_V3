# Prior HML Empirical Results

This is the compact evidence ledger carried into V3. Source artifacts and full paths are catalogued in `research/asset_inventory/ALL_EXPERIMENTS.md`.

| Experiment | Key result | Scientific reading |
|---|---|---|
| Final HML Signal, two 10K seeds | HML−Neutral +35.55pp, pooled CI [+33.53,+37.50]pp | Historically positive but later causally invalidated by the envelope control. |
| Common-envelope 10K control | HML 85.33%, Neutral 88.10%; delta −2.77pp, CI [−3.72,−1.81]pp | Previous gain came from a severe Neutral prompt-envelope handicap, not state serialization. |
| Common-envelope zero shot | HML−Neutral −3.97pp, CI [−4.87,−3.07]pp | Frozen base model preferred canonical JSON on that task. |
| EXP_REP_VALIDITY_V1 Stage 1 IID | Structured English 0.7939; Lean-like 0.7759; HML 0.7701; typed AST 0.7664 | HML ranked third and led no split. |
| Stage 1 lexical controls | Bag-of-words 0.7213–0.7559; transformer uplift +0.0219–0.0546 | Most measured accuracy was lexical; representation signal remained uncertain. |
| Stage 1 OOD | Structured English won 6/7 splits; Lean-like won alpha rename; HML was never significantly best | No basis to privilege current HML syntax. |
| Stage 1 minimal pairs | 0.9647–0.9853 across arms | Saturated instrument; not discriminative enough. |
| HML50K Unicode forensic audit | HML-only escape payload; historical comparison invalidated | Serializer asymmetry can dominate representation effects. |
| Lean attestation Stage100 | 32 exact replay passes; 68 nonpasses; every reached target action matched exact before/after | Trace evidence is real, but nested-tactic reconstruction limits fresh replay coverage. |

## V3 prior

`CURRENT_HML_SYNTAX_IS_NOT_PRIVILEGED.` The V3 representation lab is justified precisely because the strongest controlled evidence either removes or reverses the earlier apparent advantage. No new GPU experiment is authorized by this foundation milestone.
