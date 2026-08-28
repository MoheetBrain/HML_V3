# Prior Canonical Provenance Audit V2

The approximately 241,265 prior records remain strong formal-trace evidence but are not automatically V2 runtime truth.

| Source family | Scale | Classification | V2 use |
|---|---:|---|---|
| Pinned LeanDojo Benchmark 4 theorem source and `.ast.json` | 241,265 transitions available | `DIRECTLY_REUSABLE` | exact theorem/action/before/after provenance and source-byte location join |
| Official LeanDojo annotated premise records | source-wide | `DIRECTLY_REUSABLE` | external premise evidence, kept distinct from runtime local references |
| Prior `lean_canonical_records.jsonl` structured projection | 241,265 | `REEXTRACT_WITH_V2` | source population only; pretty-derived identities/deltas are not V2 truth |
| `LEAN_PIPELINE_V1` source rows | 1,000 | `REEXTRACT_WITH_V2` | 500-row V2 campaign subset is re-extracted; remaining 500 retain V1 status |
| Stage100 fresh replay certificates | 100 | `HISTORICAL_ONLY` for structured V2 state | retained as independent V1 operational evidence; no Expr/FVar/MVar payload |
| Prior paired HML/AST/English renderings | 241,265-scale families | `HISTORICAL_ONLY` | representation-history evidence only; never V2 source labels |
| Derived text effect labels (`names_added`, `target_changed`, etc.) | 241,265 | `INVALIDATED` as state truth | retained only as `RECORDED_HISTORICAL_METADATA` |
| Unregistered/missing provenance families | none identified in V1 inventory | `UNKNOWN` | excluded until registered |

This audit does not enlarge the V2 verified population. Scaling to 10,000+ transitions remains gated on the current extractor/losslessness result and storage-efficient source acquisition.
