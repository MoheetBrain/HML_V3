# Failed, Confounded, or Unsupported Previous Ideas

| Prior idea/result | Evidence | V3 disposition |
|---|---|---|
| HML syntax itself has a large learned advantage | The reported +35.55pp collapsed to −2.77pp when non-state prompt bytes were controlled. | Rejected as a causal claim. |
| The old HML arm is privileged among reasonable surfaces | Stage 1 ranked Structured English (0.7939) above Lean-like (0.7759), HML (0.7701), and typed AST (0.7664) IID; HML led no split. | Rejected; all surfaces remain candidates. |
| Transformer performance demonstrated deep state comprehension | Bag-of-words reached 0.7213–0.7559 macro-F1; frozen-transformer gains over each lexical control were only +0.0219 to +0.0546. | Unsupported; future tasks must resist lexical shortcuts. |
| HML50K was a clean representation comparison | Its HML model rows contained decoded literal Unicode escape payloads asymmetrically; the canonical source remained clean. | Historical regression only; representation inference invalidated. |
| One opaque claim containing a whole Lean state is a semantic state | Prior measurement found structurally empty wrappers despite rich text inside. | Rejected; V3 decomposes all displayed goals and local contexts. |
| Old source `hypotheses`/`target` fields are lossless | On V3's sample, 659/2,000 state observations disagree with exact raw-state decomposition, chiefly multiline truncation/misparsing. | Raw state is authoritative; disagreement retained. |
| Prior derived `premises_used` captured dependencies | It is empty in all 241,265 prior records. | Replaced by an exact join to official LeanDojo `annotated_tactic` premises. |
| A green semantic-firewall fixture set proves full transition validity | The original fixtures shared self-consistent deltas and could not detect a missing frame condition; later fixtures exposed intentional divergences. | Regression evidence only, never formal truth. |
| Old ontology coverage justifies canonical fields | Several lifecycle roles were exercised mainly by synthetic fixtures rather than real formal trajectories. | Fields enter V3 only after real-state evidence. |

None of these failures implies that readable structure is useless. They imply that claims must be attached to matched envelopes, valid labels, strong baselines, and actual formal transitions.
