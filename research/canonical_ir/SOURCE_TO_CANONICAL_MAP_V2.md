# LeanRuntimeState → CanonicalMathState V2 Map

| Lean runtime evidence | Canonical destination | Adjudication | Cross-system interpretation |
|---|---|---|---|
| `Expr.bvar` | `bound_variable(index)` | promoted | locally nameless bound reference |
| `Expr.fvar(FVarId)` | `local_reference(canonical scoped id)` | promoted; raw ID delegated | scoped local mathematical object |
| `Expr.mvar(MVarId)` | `metavariable_reference(canonical id)` | promoted; raw ID delegated | unresolved term/goal variable |
| `Expr.sort(Level)` | `sort(level tree)` | promoted | universe/sort structure |
| `Expr.const(Name, Levels)` | `symbol(identity, universe arguments)` | promoted | source declaration identity |
| `Expr.app` | `application(function, argument)` | promoted | elaborated application, including implicit/coercion arguments |
| `Expr.lam` | `lambda` | promoted | term binder; display spelling alpha-normalized |
| `Expr.forallE` | `dependent_function` | promoted | quantified/dependent function binder |
| `Expr.letE` | `let` | promoted | local definition |
| `Expr.lit` | `literal` | promoted | literal value |
| `Expr.mdata` | `annotated(expression)` | expression promoted; metadata delegated | semantically transparent annotation boundary |
| `Expr.proj` | `projection(type, index, structure)` | promoted | record/structure projection |
| `LocalDecl.FVarId/index` | scoped declaration identity | promoted; raw ID delegated | hygienic declaration correspondence |
| `userName` | diagnostic display field | source-specific by design | not identity |
| `BinderInfo` | binder role | promoted | explicit/implicit/instance role where systems support it |
| `LocalDeclKind` | source reference | source-specific by design | Lean elaborator bookkeeping |
| goal `MVarId` and order | goal identity and `focus_order` | promoted; raw ID delegated | obligation identity and focus |
| relevant `MetavarDecl` type/assignment/kind | canonical metavariable record | promoted | unresolved/assigned mathematical hole |
| complete inactive MVar inventory | full context counts | delegated by source reference | replay/debug state, not proven neutral need; all created/assigned/changed entries remain explicit |
| delayed assignment table | source reference | source-specific by design | Lean unification implementation |
| official annotated LeanDojo premises | `external_premise_refs` | promoted | externally defined premises identified by the pinned source trace |
| descendant `TermInfo` constants | source-specific elaborated constant refs | source-specific by design | typed external declaration occurrences; not every constant is a premise |
| descendant `TermInfo` FVars | `local_context_refs` | promoted with partial provenance | referenced local facts/objects |
| namespace/options/imports | provenance reference | delegated | reproducible elaboration context |
| `InfoTree` path/source range | action source reference | delegated | executable nested occurrence identity |
| pretty goal view | diagnostics only | not promoted | human rendering, never truth substrate |

## Promotion test

Every promoted item has source evidence, an identified mathematical role, a V1 information-loss example in the gap register, a cross-system reading, and executable tests. Fields without that evidence stay source-specific. This table therefore does not imply that every Lean implementation detail belongs in a future HML language.
