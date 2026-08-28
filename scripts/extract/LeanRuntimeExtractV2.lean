/-
Lean-side semantic-state extractor for HML V3.

This program intentionally runs inside Lean's elaborator.  It serializes the `Expr`,
`LocalDecl`, and `MetavarContext` values stored in `TacticInfo`; pretty-printed goals are
retained only as diagnostics.  Python must never reconstruct these identities from text.

Usage (from a pinned Lean project):

  lake env lean --run /path/to/LeanRuntimeExtractV2.lean SOURCE TARGETS.tsv OUTPUT.json

Each target line is: fully.qualified.theorem<TAB>transition_index<TAB>record_id
-/

import Lean
import Lake

open Lean Elab System

set_option maxHeartbeats 2000000

namespace HMLV3.RuntimeV2

private def jstr (s : String) : Json := toJson s
private def jnat (n : Nat) : Json := toJson n
private def jbool (b : Bool) : Json := toJson b
private def jarr (xs : Array Json) : Json := Json.arr xs
private def jobj (xs : List (String × Json)) : Json := Json.mkObj xs

private def nameJson (n : Name) : Json := jstr n.toString

private def binderInfoString : BinderInfo → String
  | .default => "EXPLICIT"
  | .implicit => "IMPLICIT"
  | .strictImplicit => "STRICT_IMPLICIT"
  | .instImplicit => "INSTANCE_IMPLICIT"

private def localDeclKindString : LocalDeclKind → String
  | .default => "DEFAULT"
  | .implDetail => "IMPLEMENTATION_DETAIL"
  | .auxDecl => "AUXILIARY_DECLARATION"

private def metavarKindString : MetavarKind → String
  | .natural => "NATURAL"
  | .synthetic => "SYNTHETIC"
  | .syntheticOpaque => "SYNTHETIC_OPAQUE"

private def dataValueJson : DataValue → Json
  | .ofString v => jobj [("kind", jstr "STRING"), ("value", jstr v)]
  | .ofBool v => jobj [("kind", jstr "BOOL"), ("value", jbool v)]
  | .ofName v => jobj [("kind", jstr "NAME"), ("value", nameJson v)]
  | .ofNat v => jobj [("kind", jstr "NAT"), ("value", jnat v)]
  | .ofInt v => jobj [("kind", jstr "INT"), ("value", jstr (toString v))]
  | .ofSyntax v => jobj [
      ("kind", jstr "SYNTAX_DIAGNOSTIC"),
      ("value", jstr (toString v))
    ]

private def kvMapJson (m : KVMap) : Json :=
  jarr <| m.entries.toArray.map fun (k, v) =>
    jobj [("key", nameJson k), ("value", dataValueJson v)]

partial def levelJson : Level → Json
  | .zero => jobj [("constructor", jstr "zero")]
  | .succ u => jobj [("constructor", jstr "succ"), ("of", levelJson u)]
  | .max u v => jobj [
      ("constructor", jstr "max"), ("left", levelJson u), ("right", levelJson v)
    ]
  | .imax u v => jobj [
      ("constructor", jstr "imax"), ("left", levelJson u), ("right", levelJson v)
    ]
  | .param n => jobj [("constructor", jstr "param"), ("name", nameJson n)]
  | .mvar id => jobj [("constructor", jstr "mvar"), ("lmvar_id", nameJson id.name)]

partial def exprJson : Expr → Json
  | .bvar i => jobj [("constructor", jstr "bvar"), ("debruijn_index", jnat i)]
  | .fvar id => jobj [("constructor", jstr "fvar"), ("fvar_id", nameJson id.name)]
  | .mvar id => jobj [("constructor", jstr "mvar"), ("mvar_id", nameJson id.name)]
  | .sort u => jobj [("constructor", jstr "sort"), ("level", levelJson u)]
  | .const n us => jobj [
      ("constructor", jstr "const"),
      ("decl_name", nameJson n),
      ("universe_args", jarr <| us.toArray.map levelJson)
    ]
  | .app fn arg => jobj [
      ("constructor", jstr "app"), ("function", exprJson fn), ("argument", exprJson arg)
    ]
  | .lam n ty body bi => jobj [
      ("constructor", jstr "lam"),
      ("binder_name", nameJson n),
      ("binder_info", jstr (binderInfoString bi)),
      ("binder_type", exprJson ty),
      ("body", exprJson body)
    ]
  | .forallE n ty body bi => jobj [
      ("constructor", jstr "forallE"),
      ("binder_name", nameJson n),
      ("binder_info", jstr (binderInfoString bi)),
      ("binder_type", exprJson ty),
      ("body", exprJson body)
    ]
  | .letE n ty value body nonDep => jobj [
      ("constructor", jstr "letE"),
      ("decl_name", nameJson n),
      ("type", exprJson ty),
      ("value", exprJson value),
      ("body", exprJson body),
      ("non_dependent_hint", jbool nonDep)
    ]
  | .lit (.natVal n) => jobj [
      ("constructor", jstr "lit"), ("literal_kind", jstr "NAT"), ("value", jnat n)
    ]
  | .lit (.strVal s) => jobj [
      ("constructor", jstr "lit"), ("literal_kind", jstr "STRING"), ("value", jstr s)
    ]
  | .mdata data e => jobj [
      ("constructor", jstr "mdata"),
      ("metadata", kvMapJson data),
      ("expr", exprJson e)
    ]
  | .proj typeName idx struct => jobj [
      ("constructor", jstr "proj"),
      ("type_name", nameJson typeName),
      ("field_index", jnat idx),
      ("struct", exprJson struct)
    ]

private def localDeclJson : LocalDecl → Json
  | .cdecl index fvarId userName ty bi kind => jobj [
      ("declaration_kind", jstr "cdecl"),
      ("index", jnat index),
      ("fvar_id", nameJson fvarId.name),
      ("user_name", nameJson userName),
      ("binder_info", jstr (binderInfoString bi)),
      ("local_decl_kind", jstr (localDeclKindString kind)),
      ("type", exprJson ty),
      ("value", Json.null),
      ("non_dependent_hint", Json.null)
    ]
  | .ldecl index fvarId userName ty value nonDep kind => jobj [
      ("declaration_kind", jstr "ldecl"),
      ("index", jnat index),
      ("fvar_id", nameJson fvarId.name),
      ("user_name", nameJson userName),
      ("binder_info", jstr "EXPLICIT"),
      ("local_decl_kind", jstr (localDeclKindString kind)),
      ("type", exprJson ty),
      ("value", exprJson value),
      ("non_dependent_hint", jbool nonDep)
    ]

private def localContextJson (lctx : LocalContext) : Json :=
  jarr <| lctx.getFVarIds.map fun id => localDeclJson (lctx.get! id)

private def localInstancesJson (xs : LocalInstances) : Json :=
  jarr <| xs.map fun inst => jobj [
    ("class_name", nameJson inst.className),
    ("fvar", exprJson inst.fvar)
  ]

private def metavarDeclJson (mctx : MetavarContext) (id : MVarId)
    (decl : MetavarDecl) : Json :=
  let assignment := match mctx.eAssignment.find? id with
    | some e => exprJson e
    | none => Json.null
  jobj [
    ("mvar_id", nameJson id.name),
    ("user_name", nameJson decl.userName),
    ("type", exprJson decl.type),
    ("assignment", assignment),
    ("is_assigned", jbool (assignment != Json.null)),
    ("kind", jstr (metavarKindString decl.kind)),
    ("synthetic_opaque", jbool decl.kind.isSyntheticOpaque),
    ("depth", jnat decl.depth),
    ("index", jnat decl.index),
    ("num_scope_args", jnat decl.numScopeArgs),
    ("local_context", localContextJson decl.lctx),
    ("local_instances", localInstancesJson decl.localInstances)
  ]

private def delayedAssignmentJson (id : MVarId) (a : DelayedMetavarAssignment) : Json :=
  jobj [
    ("mvar_id", nameJson id.name),
    ("fvars", jarr <| a.fvars.map exprJson),
    ("pending_mvar_id", nameJson a.mvarIdPending.name)
  ]

private def exprInventoryJson (e : Expr) : Json := jobj [
  ("constructor", jstr e.ctorName),
  ("lean_hash", jstr (toString e.hash)),
  ("has_fvar", jbool e.hasFVar),
  ("has_expr_mvar", jbool e.hasExprMVar),
  ("has_level_mvar", jbool e.hasLevelMVar),
  ("has_level_param", jbool e.hasLevelParam)
]

private def metavarInventoryJson (mctx : MetavarContext) (id : MVarId)
    (decl : MetavarDecl) : Json :=
  let assignment? := mctx.eAssignment.find? id
  jobj [
    ("mvar_id", nameJson id.name),
    ("user_name", nameJson decl.userName),
    ("kind", jstr (metavarKindString decl.kind)),
    ("depth", jnat decl.depth),
    ("index", jnat decl.index),
    ("is_assigned", jbool assignment?.isSome),
    ("type_inventory", exprInventoryJson decl.type),
    ("assignment_inventory", match assignment? with
      | some e => exprInventoryJson e
      | none => Json.null),
    ("local_context_size", jnat decl.lctx.getFVarIds.size),
    ("local_instance_count", jnat decl.localInstances.size)
  ]

private partial def exprMVarIds : Expr → List MVarId
  | .mvar id => [id]
  | .app f a => exprMVarIds f ++ exprMVarIds a
  | .lam _ ty body _ | .forallE _ ty body _ => exprMVarIds ty ++ exprMVarIds body
  | .letE _ ty value body _ => exprMVarIds ty ++ exprMVarIds value ++ exprMVarIds body
  | .mdata _ e | .proj _ _ e => exprMVarIds e
  | _ => []

private def localContextMVarIds (lctx : LocalContext) : List MVarId :=
  lctx.getFVarIds.toList.bind fun id =>
    let decl := lctx.get! id
    exprMVarIds decl.type ++ match decl.value? with
      | some value => exprMVarIds value
      | none => []

private partial def relevantMVarClosure (mctx : MetavarContext) (pending seen : List MVarId) : List MVarId :=
  match pending with
  | [] => seen
  | id :: rest =>
    if seen.contains id then relevantMVarClosure mctx rest seen
    else
      let refs := match mctx.findDecl? id with
        | none => []
        | some decl =>
          exprMVarIds decl.type ++ localContextMVarIds decl.lctx ++
            match mctx.eAssignment.find? id with
            | some assignment => exprMVarIds assignment
            | none => []
      relevantMVarClosure mctx (refs ++ rest) (id :: seen)

private def relevantMVarIds (mctx : MetavarContext) (goals : List MVarId) : List MVarId :=
  let refs := goals.bind fun id => match mctx.findDecl? id with
    | none => []
    | some decl => exprMVarIds decl.type ++ localContextMVarIds decl.lctx
  relevantMVarClosure mctx (goals ++ refs) [] |>.eraseDups

private def metavarContextJson (mctx : MetavarContext) (goals : List MVarId) : Json :=
  let relevantIds := relevantMVarIds mctx goals
  let relevantDecls := relevantIds.toArray.filterMap fun id =>
    (mctx.findDecl? id).map fun decl => metavarDeclJson mctx id decl
  let inventory := relevantIds.toArray.filterMap fun id =>
    (mctx.findDecl? id).map fun decl => metavarInventoryJson mctx id decl
  let levelAssignments := mctx.lAssignment.toArray.map fun (id, level) => jobj [
    ("lmvar_id", nameJson id.name), ("assignment", levelJson level)
  ]
  let levelDepths := mctx.lDepth.toArray.map fun (id, depth) => jobj [
    ("lmvar_id", nameJson id.name), ("depth", jnat depth)
  ]
  let delayed := mctx.dAssignment.toArray.map fun (id, value) => delayedAssignmentJson id value
  jobj [
    ("depth", jnat mctx.depth),
    ("level_assignment_depth", jnat mctx.levelAssignDepth),
    ("mvar_counter", jnat mctx.mvarCounter),
    ("declaration_count", jnat mctx.decls.toArray.size),
    ("assigned_expression_count", jnat mctx.eAssignment.toArray.size),
    ("declaration_inventory", jarr inventory),
    ("declaration_inventory_scope", jstr "GOAL_RELEVANCE_CLOSURE_ONLY"),
    ("relevant_declarations", jarr relevantDecls),
    ("relevance_closure", jstr "GOALS_PLUS_TRANSITIVE_MVARS_IN_TARGETS_LOCAL_DECLS_AND_ASSIGNMENTS"),
    ("level_mvar_depths", jarr levelDepths),
    ("level_assignments", jarr levelAssignments),
    ("delayed_assignments", jarr delayed),
    ("unexposed_constraints", jstr "Lean 4.10 exposes no standalone constraint table in MetavarContext")
  ]

private def metavarDeltaJson (before after : MetavarContext) : Json :=
  let created := after.decls.toArray.filterMap fun (id, decl) =>
    if (before.findDecl? id).isNone then some (metavarInventoryJson after id decl) else none
  let newlyAssigned := after.eAssignment.toArray.filterMap fun (id, assignment) =>
    if (before.eAssignment.find? id).isNone then some <| jobj [
      ("mvar_id", nameJson id.name),
      ("assignment_inventory", exprInventoryJson assignment)
    ] else none
  let assignmentsChanged := after.eAssignment.toArray.filterMap fun (id, assignment) =>
    match before.eAssignment.find? id with
    | some old => if old == assignment then none else some <| jobj [
        ("mvar_id", nameJson id.name),
        ("before_inventory", exprInventoryJson old),
        ("after_inventory", exprInventoryJson assignment)
      ]
    | none => none
  let levelNewlyAssigned := after.lAssignment.toArray.filterMap fun (id, assignment) =>
    if (before.lAssignment.find? id).isNone then some <| jobj [
      ("lmvar_id", nameJson id.name), ("assignment", levelJson assignment)
    ] else none
  let levelAssignmentsChanged := after.lAssignment.toArray.filterMap fun (id, assignment) =>
    match before.lAssignment.find? id with
    | some old => if old == assignment then none else some <| jobj [
        ("lmvar_id", nameJson id.name),
        ("before", levelJson old),
        ("after", levelJson assignment)
      ]
    | none => none
  jobj [
    ("source", jstr "DIRECT_METAVAR_CONTEXT_IDENTITY_COMPARISON_IN_LEAN"),
    ("declarations_created", jarr created),
    ("expression_metavariables_newly_assigned", jarr newlyAssigned),
    ("expression_assignments_changed", jarr assignmentsChanged),
    ("universe_metavariables_newly_assigned", jarr levelNewlyAssigned),
    ("universe_assignments_changed", jarr levelAssignmentsChanged)
  ]

private def goalJson (mctx : MetavarContext) (ordinal : Nat) (id : MVarId) : Json :=
  match mctx.findDecl? id with
  | none => jobj [
      ("mvar_id", nameJson id.name),
      ("ordinal", jnat ordinal),
      ("focused", jbool (ordinal == 0)),
      ("declaration_available", jbool false)
    ]
  | some decl => jobj [
      ("mvar_id", nameJson id.name),
      ("ordinal", jnat ordinal),
      ("focused", jbool (ordinal == 0)),
      ("declaration_available", jbool true),
      ("target", exprJson decl.type),
      ("local_context", localContextJson decl.lctx),
      ("local_instances", localInstancesJson decl.localInstances),
      ("user_name", nameJson decl.userName),
      ("kind", jstr (metavarKindString decl.kind))
    ]

private def runtimeStateJson (ctx : ContextInfo) (goals : List MVarId) : IO Json :=
  ctx.runMetaM {} do
    let mctx ← getMCtx
    let goalArray := goals.toArray.mapIdx fun i id => goalJson mctx i id
    return jobj [
      ("goal_order", jarr <| goals.toArray.map fun id => nameJson id.name),
      ("focused_goal_id", match goals with | [] => Json.null | id :: _ => nameJson id.name),
      ("goals", jarr goalArray),
      ("metavariable_context", metavarContextJson mctx goals)
    ]

namespace Pp

private def addLine (s : String) : String := if s.isEmpty then s else s ++ "\n"

private def ppGoal (mvarId : MVarId) : MetaM String := do
  match (← getMCtx).findDecl? mvarId with
  | none => return "unknown goal"
  | some mvarDecl =>
    let indent := 2
    let lctx := mvarDecl.lctx.sanitizeNames.run' { options := (← getOptions) }
    Meta.withLCtx lctx mvarDecl.localInstances do
      let rec pushPending (ids : List Name) (type? : Option Expr) (s : String) : MetaM String := do
        if ids.isEmpty then return s
        let s := addLine s
        match type? with
        | none => return s
        | some type =>
          let typeFmt ← Meta.ppExpr type
          return (s ++ (Format.joinSep ids.reverse (format " ") ++ " :" ++
            Format.nest indent (Format.line ++ typeFmt)).group).pretty
      let rec ppVars (varNames : List Name) (prevType? : Option Expr) (s : String)
          (localDecl : LocalDecl) : MetaM (List Name × Option Expr × String) := do
        match localDecl with
        | .cdecl _ _ varName type _ _ =>
          let varName := varName.simpMacroScopes
          let type ← instantiateMVars type
          if prevType? == none || prevType? == some type then
            return (varName :: varNames, some type, s)
          else do
            let s ← pushPending varNames prevType? s
            return ([varName], some type, s)
        | .ldecl _ _ varName type val _ _ =>
          let varName := varName.simpMacroScopes
          let s ← pushPending varNames prevType? s
          let s := addLine s
          let typeFmt ← Meta.ppExpr (← instantiateMVars type)
          let valFmt ← Meta.ppExpr (← instantiateMVars val)
          let fmtElem := format varName ++ " : " ++ typeFmt ++ " :=" ++
            Format.nest indent (Format.line ++ valFmt)
          return ([], none, s ++ fmtElem.group.pretty)
      let (varNames, type?, s) ← lctx.foldlM (init := ([], none, "")) fun
          (varNames, prevType?, s) localDecl =>
        if localDecl.isAuxDecl || localDecl.isImplementationDetail then
          return (varNames, prevType?, s)
        else
          ppVars varNames prevType? s localDecl
      let s ← pushPending varNames type? s
      let goalTypeFmt ← Meta.ppExpr (← instantiateMVars mvarDecl.type)
      let goalFmt := Meta.getGoalPrefix mvarDecl ++ Format.nest indent goalTypeFmt
      let s := s ++ "\n" ++ goalFmt.pretty
      match mvarDecl.userName with
      | Name.anonymous => return s
      | name => return "case " ++ name.eraseMacroScopes.toString ++ "\n" ++ s

def ppGoals (ctx : ContextInfo) (goals : List MVarId) : IO String :=
  if goals.isEmpty then return "no goals"
  else
    let fmt := ctx.runMetaM {} (return Std.Format.prefixJoin "\n\n" (← goals.mapM ppGoal))
    return (← fmt).pretty.trim

end Pp

private partial def exprRefs : Expr → List String × List String
  | .bvar _ | .sort _ | .lit _ => ([], [])
  | .fvar id => ([id.name.toString], [])
  | .mvar _ => ([], [])
  | .const n _ => ([], [n.toString])
  | .app f a =>
      let (ff, fc) := exprRefs f
      let (af, ac) := exprRefs a
      (ff ++ af, fc ++ ac)
  | .lam _ ty body _ | .forallE _ ty body _ =>
      let (tf, tc) := exprRefs ty
      let (bf, bc) := exprRefs body
      (tf ++ bf, tc ++ bc)
  | .letE _ ty value body _ =>
      let (tf, tc) := exprRefs ty
      let (vf, vc) := exprRefs value
      let (bf, bc) := exprRefs body
      (tf ++ vf ++ bf, tc ++ vc ++ bc)
  | .mdata _ e | .proj _ _ e => exprRefs e

private partial def treeTermRefs : InfoTree → List String × List String
  | .context _ tree => treeTermRefs tree
  | .node info children =>
      let here := match info with
        | .ofTermInfo ti => exprRefs ti.expr
        | _ => ([], [])
      children.foldl (init := here) fun (fs, cs) child =>
        let (fs', cs') := treeTermRefs child
        (fs ++ fs', cs ++ cs')
  | .hole _ => ([], [])

private def uniqueSorted (xs : List String) : Array String :=
  xs.eraseDups.toArray.qsort (· < ·)

private def positionJson (fileMap : FileMap) (raw : String.Pos) : Json :=
  let pos := fileMap.toPosition raw
  jobj [
    ("raw", jnat raw.1),
    ("line", jnat pos.line),
    ("column", jnat pos.column)
  ]

private def optionsJson (options : Options) : Json := kvMapJson options

private def contextProvenanceJson (ctx : ContextInfo) : Json := jobj [
  ("parent_declaration", match ctx.parentDecl? with | some n => nameJson n | none => Json.null),
  ("current_namespace", nameJson ctx.currNamespace),
  ("open_declarations", jarr <| ctx.openDecls.toArray.map (jstr ∘ toString)),
  ("options", optionsJson ctx.options),
  ("transitive_import_modules", jarr <| ctx.env.header.moduleNames.map nameJson),
  ("environment_main_module", nameJson ctx.env.header.mainModule)
]

structure Target where
  declarationName : String
  transitionIndex : Nat
  recordId : String
  sourceStartRaw : Option Nat := none
  sourceEndRaw : Option Nat := none

private def parseTarget (line : String) : Except String Target :=
  match line.splitOn "\t" with
  | [declarationName, indexText, recordId] =>
    match indexText.toNat? with
    | some transitionIndex => .ok { declarationName, transitionIndex, recordId }
    | none => .error s!"invalid transition index: {line}"
  | [declarationName, indexText, recordId, startText, endText] =>
    match indexText.toNat?, startText.toNat?, endText.toNat? with
    | some transitionIndex, some sourceStartRaw, some sourceEndRaw =>
      .ok { declarationName, transitionIndex, recordId, sourceStartRaw, sourceEndRaw }
    | _, _, _ => .error s!"invalid target index/source range: {line}"
  | _ => .error s!"invalid target line: {line}"

private def readTargets (path : FilePath) : IO (Array Target) := do
  let input ← IO.FS.readFile path
  let mut targets := #[]
  for line in input.splitOn "\n" do
    if !line.trim.isEmpty then
      match parseTarget line with
      | .ok target => targets := targets.push target
      | .error msg => throw <| IO.userError msg
  return targets

structure ExtractState where
  counters : HashMap String Nat := {}
  captures : Array Json := #[]

abbrev ExtractM := StateT ExtractState IO

private def nextOrdinal (declarationName : String) : ExtractM Nat := do
  let state ← get
  let ordinal := state.counters.findD declarationName 0
  set { state with counters := state.counters.insert declarationName (ordinal + 1) }
  return ordinal

private def targetFor? (targets : Array Target) (declarationName : String)
    (ordinal sourceStartRaw : Nat) : Option Target :=
  targets.find? fun t =>
    t.declarationName == declarationName &&
      match t.sourceStartRaw with
      | some expected => expected == sourceStartRaw
      | none => t.transitionIndex == ordinal

private def visitTacticInfo (targets : Array Target) (ctx : ContextInfo) (ti : TacticInfo)
    (parent current : InfoTree) (treePath : List Nat) : ExtractM Unit := do
  let eligible := match parent with
    | .node (.ofTacticInfo i) _ =>
      i.stx.getKind == ``Lean.Parser.Tactic.tacticSeq1Indented ||
      i.stx.getKind == ``Lean.Parser.Tactic.tacticSeqBracketed ||
      i.stx.getKind == ``Lean.Parser.Tactic.rewriteSeq
    | _ => false
  unless eligible do return
  let ctxBefore := { ctx with mctx := ti.mctxBefore }
  let ctxAfter := { ctx with mctx := ti.mctxAfter }
  let prettyBefore ← Pp.ppGoals ctxBefore ti.goalsBefore
  let prettyAfter ← Pp.ppGoals ctxAfter ti.goalsAfter
  if prettyBefore == "no goals" || prettyBefore == prettyAfter then return
  let some startPos := ti.stx.getPos? true | return
  let some endPos := ti.stx.getTailPos? true | return
  let declarationName := ctx.parentDecl?.map Name.toString |>.getD ""
  let ordinal ← nextOrdinal declarationName
  let some target := targetFor? targets declarationName ordinal startPos.1 | return
  let before ← runtimeStateJson ctxBefore ti.goalsBefore
  let after ← runtimeStateJson ctxAfter ti.goalsAfter
  let (localRefs, constantRefs) := treeTermRefs current
  let capture := jobj [
    ("record_id", jstr target.recordId),
    ("theorem_id", jstr declarationName),
    ("transition_index", jnat target.transitionIndex),
    ("fresh_trace_ordinal", jnat ordinal),
    ("tactic_kind", nameJson ti.stx.getKind),
    ("tactic_elaborator", nameJson ti.elaborator),
    ("source_start", positionJson ctx.fileMap startPos),
    ("source_end", positionJson ctx.fileMap endPos),
    ("info_tree_path", jarr <| treePath.reverse.toArray.map jnat),
    ("state_before", before),
    ("state_after", after),
    ("metavariable_delta", metavarDeltaJson ti.mctxBefore ti.mctxAfter),
    ("pretty_before_diagnostic", jstr prettyBefore),
    ("pretty_after_diagnostic", jstr prettyAfter),
    ("local_context_refs", jarr <| (uniqueSorted localRefs).map jstr),
    ("external_constant_refs", jarr <| (uniqueSorted constantRefs).map jstr),
    ("reference_mechanism", jstr "DIRECT_TRAVERSAL_OF_ELABORATED_TERMINFO_EXPRS"),
    ("reference_completeness", jstr "PARTIAL_TACTICS_WITHOUT_TERMINFO_MAY_HIDE_INTERNAL_USE"),
    ("environment", contextProvenanceJson ctx)
  ]
  modify fun s => { s with captures := s.captures.push capture }

private partial def traverseTree (targets : Array Target) (ctx : ContextInfo) (tree parent : InfoTree)
    (treePath : List Nat) : ExtractM Unit := do
  match tree with
  | .context ctx' child =>
    match ctx'.mergeIntoOuter? ctx with
    | some merged => traverseTree targets merged child tree treePath
    | none => throw <| IO.userError "failed to merge ContextInfo while traversing InfoTree"
  | .node info children =>
    match info with
    | .ofTacticInfo ti => visitTacticInfo targets ctx ti parent tree treePath
    | _ => pure ()
    for i in [0:children.size] do
      traverseTree targets ctx children[i]! tree (i :: treePath)
  | .hole _ => pure ()

private def traverseTopLevel (targets : Array Target) (tree : InfoTree) : ExtractM Unit := do
  match tree with
  | .context ctx child =>
    match ctx.mergeIntoOuter? none with
    | some merged => traverseTree targets merged child tree []
    | none => throw <| IO.userError "failed to synthesize top-level ContextInfo"
  | _ => pure ()

private def directImportsJson (header : Syntax) : Json :=
  jarr <| (headerToImports header).map fun imp => jobj [
    ("module", nameJson imp.module),
    ("runtime_only", jbool imp.runtimeOnly)
  ]

unsafe def processFile (source targetsPath outputPath : FilePath) : IO Unit := do
  let input ← IO.FS.readFile source
  let targets ← readTargets targetsPath
  enableInitializersExecution
  let inputCtx := Parser.mkInputContext input source.toString
  let (header, parserState, messages) ← Parser.parseHeader inputCtx
  let (env, messages) ← processHeader header {} messages inputCtx
  if messages.hasErrors then
    for msg in messages.toList do
      if msg.severity == .error then IO.eprintln s!"ERROR: {← msg.toString}"
    throw <| IO.userError "errors during import; aborting"
  let env := env.setMainModule (← moduleNameOfFileName source none)
  let commandState := { Command.mkState env messages {} with infoState.enabled := true }
  let processed ← IO.processCommands inputCtx parserState commandState
  if processed.commandState.messages.hasErrors then
    for msg in processed.commandState.messages.toList do
      if msg.severity == .error then IO.eprintln s!"ERROR: {← msg.toString}"
    throw <| IO.userError "errors during elaboration; aborting"
  let trees := processed.commandState.infoState.trees.toArray
  let (_, state) ← (trees.forM (traverseTopLevel targets)).run {}
  let result := jobj [
    ("schema_version", jstr "lean-runtime-state-v2.0.0"),
    ("extractor", jstr "HMLV3.RuntimeV2.LeanRuntimeExtractV2"),
    ("source_file", jstr source.toString),
    ("direct_imports", directImportsJson header),
    ("requested_targets", jnat targets.size),
    ("captured_targets", jnat state.captures.size),
    ("captures", jarr state.captures)
  ]
  if let some parent := outputPath.parent then IO.FS.createDirAll parent
  IO.FS.writeFile outputPath (result.pretty ++ "\n")

end HMLV3.RuntimeV2

unsafe def main (args : List String) : IO Unit := do
  match args with
  | [source, targets, output] =>
    HMLV3.RuntimeV2.processFile (FilePath.mk source)
      (FilePath.mk targets) (FilePath.mk output)
  | _ => throw (IO.userError "usage: LeanRuntimeExtractV2.lean SOURCE TARGETS.tsv OUTPUT.json")
