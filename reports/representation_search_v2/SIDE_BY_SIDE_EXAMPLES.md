# Side-by-Side Examples

The same verified Lean transitions written in every candidate language. Selection in this project is by measurement and never by appearance; this file exists so a human can check what the search actually produced.

Rendered arms: 9. Examples: 20, spread across goal count and local-context size rather than taken consecutively.

## Example 1 — `.lake/packages/batteries/Batteries/Data/List/Basic.lean::List.sigma_eq_sigmaTR::0`

**Shape:** 1 goal(s), 1 local declaration(s), 0 external premise(s). Domain `packages`.

### SEED_LEAN_LIKE

*4,331 characters*

```text
#
  Y
    TH: List.sigma_eq_sigmaTR
    FL: .lake/packages/batteries/Batteries/Data/List/Basic.lean
Σ₀
  D sigma_eq_sigmaTR~bf0
    n: sigma_eq_sigmaTR
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(us(up(u_2))))]),pi(IMPLICIT,sort(us(up(u_2))),pi(IMPLICIT,pi(EXPLICIT,bv(0),sort(us(up(u_1)))),pi(EXPLICIT,ap(sym(List,[up(u_2)]),bv(1)),pi(EXPLICIT,pi(EXPLICIT,bv(2),ap(sym(List,[up(u_1)]),ap(bv(2),bv(0)))),ap(sym(List,[umax(up(u_1),up(u_2))]),ap(ap(sym(Sigma,[up(u_2) up(u_1)]),bv(3)),lam(EXPLICIT,bv(3),ap(bv(3),bv(0)))))))))),sym(List.sigma,[up(u_2) up(u_1)])),sym(List.sigmaTR,[up(u_2) up(u_1)]))
  □ bm0
    Γ: [sigma_eq_sigmaTR~bf0]
    ⊢: ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(us(up(u_2))))]),pi(IMPLICIT,sort(us(up(u_2))),pi(IMPLICIT,pi(EXPLICIT,bv(0),sort(us(up(u_1)))),pi(EXPLICIT,ap(sym(List,[up(u_2)]),bv(1)),pi(EXPLICIT,pi(EXPLICIT,bv(2),ap(sym(List,[up(u_1)]),ap(bv(2),bv(0)))),ap(sym(List,[umax(up(u_1),up(u_2))]),ap(ap(sym(Sigma,[up(u_2) up(u_1)]),bv(3)),lam(EXPLICIT,bv(3),ap(bv(3),bv(0)))))))))),sym(List.sigma,[up(u_2) up(u_1)])),sym(List.sigmaTR,[up(u_2) up(u_1)]))
  ? bm0
    k: SYNTHETIC_OPAQUE
    ∈: ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(u
... [3131 more characters]
```

### SEED_PRIOR_HML

*4,954 characters*

```text
meta
  summary
    theorem: List.sigma_eq_sigmaTR
    file: .lake/packages/batteries/Batteries/Data/List/Basic.lean
state_before
  decl bf0
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))
  goal bm0
    context: [bf0]
    target: (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)])
... [3754 more characters]
```

### SEED_STRUCTURED_ENGLISH

*5,256 characters*

```text
In meta:
  summary has theorem is List.sigma_eq_sigmaTR; and file is .lake/packages/batteries/Batteries/Data/List/Basic.lean .
In state_before:
  decl sigma_eq_sigmaTR~bf0 has display is sigma_eq_sigmaTR; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(us(up(u_2))))]),pi(IMPLICIT,sort(us(up(u_2))),pi(IMPLICIT,pi(EXPLICIT,bv(0),sort(us(up(u_1)))),pi(EXPLICIT,ap(sym(List,[up(u_2)]),bv(1)),pi(EXPLICIT,pi(EXPLICIT,bv(2),ap(sym(List,[up(u_1)]),ap(bv(2),bv(0)))),ap(sym(List,[umax(up(u_1),up(u_2))]),ap(ap(sym(Sigma,[up(u_2) up(u_1)]),bv(3)),lam(EXPLICIT,bv(3),ap(bv(3),bv(0)))))))))),sym(List.sigma,[up(u_2) up(u_1)])),sym(List.sigmaTR,[up(u_2) up(u_1)])) .
  goal bm0 has context is [sigma_eq_sigmaTR~bf0]; and target is ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(us(up(u_2))))]),pi(IMPLICIT,sort(us(up(u_2))),pi(IMPLICIT,pi(EXPLICIT,bv(0),sort(us(up(u_1)))),pi(EXPLICIT,ap(sym(List,[up(u_2)]),bv(1)),pi(EXPLICIT,pi(EXPLICIT,bv(2),ap(sym(List,[up(u_1)]),ap(bv(2),bv(0)))),ap(sym(List,[umax(up(u_1),up(u_2))]),ap(ap(sym(Sigma,[up(u_2) up(u_1)]),bv(3)),lam(EXPLICIT,bv(3),ap(bv(3),bv(0)))))))))),sym(List.sigma,[up(u_2) up(u_1)])),sym(List
... [4056 more characters]
```

### SEED_TYPED_AST

*4,516 characters*

```text
mta
  - smy
    thm: List.sigma_eq_sigmaTR
    fl: .lake/packages/batteries/Batteries/Data/List/Basic.lean
sb
  - dc bf0
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{sym|Eq,[umax{us{us{up{u_1}}},us{us{up{u_2}}}}]},{pi|IMPLICIT,{sort|us{up{u_2}}},{pi|IMPLICIT,{pi|EXPLICIT,{bv|0},{sort|us{up{u_1}}}},{pi|EXPLICIT,{ap|{sym|List,[up{u_2}]},{bv|1}},{pi|EXPLICIT,{pi|EXPLICIT,{bv|2},{ap|{sym|List,[up{u_1}]},{ap|{bv|2},{bv|0}}}},{ap|{sym|List,[umax{up{u_1},up{u_2}}]},{ap|{ap|{sym|Sigma,[up{u_2} up{u_1}]},{bv|3}},{lam|EXPLICIT,{bv|3},{ap|{bv|3},{bv|0}}}}}}}}}},{sym|List.sigma,[up{u_2} up{u_1}]}},{sym|List.sigmaTR,[up{u_2} up{u_1}]}}
  - gl bm0
    ctx: [bf0]
    tgt: {ap|{ap|{ap|{sym|Eq,[umax{us{us{up{u_1}}},us{us{up{u_2}}}}]},{pi|IMPLICIT,{sort|us{up{u_2}}},{pi|IMPLICIT,{pi|EXPLICIT,{bv|0},{sort|us{up{u_1}}}},{pi|EXPLICIT,{ap|{sym|List,[up{u_2}]},{bv|1}},{pi|EXPLICIT,{pi|EXPLICIT,{bv|2},{ap|{sym|List,[up{u_1}]},{ap|{bv|2},{bv|0}}}},{ap|{sym|List,[umax{up{u_1},up{u_2}}]},{ap|{ap|{sym|Sigma,[up{u_2} up{u_1}]},{bv|3}},{lam|EXPLICIT,{bv|3},{ap|{bv|3},{bv|0}}}}}}}}}},{sym|List.sigma,[up{u_2} up{u_1}]}},{sym|List.sigmaTR,[up{u_2} up{u_1}]}}
  - mv bm0
    knd: SYNTHETIC_OPAQUE
    ty: {ap|
... [3316 more characters]
```

### FINALIST R_5b2eb732ac8b

*3,912 characters*

```text
#
  Y
    TH: List.sigma_eq_sigmaTR
    FL: .lake/packages/batteries/Batteries/Data/List/Basic.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: []
    L: []
Σ₀
  □ bm0
    ⊢: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 bv 0 bv ap lam ap ap pi pi pi pi ap List.sigma [up(u_2) up(u_1)] sym ap List.sigmaTR [up(u_2) up(u_1)] sym ap
    Γ: [bf0]
  D bf0
    b: EXPLICIT
    d: cdecl
    ∈: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 bv 0 bv ap lam ap ap pi pi pi pi ap List.sigma [up(u_2) up(u_1)] sym ap List.sigmaTR [up(u_2) up(u_1)] sym ap
  ? bm0
    k: SYNTHETIC_OPAQUE
    ∈: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPL
... [2712 more characters]
```

### FINALIST R_000441b08de4

*3,922 characters*

```text
mta
  smy ;; thm: List.sigma_eq_sigmaTR ;; fl: .lake/packages/batteries/Batteries/Data/List/Basic.lean
sb
  dc bf0 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 bv 0 bv ap lam ap ap pi pi pi pi ap List.sigma [up(u_2) up(u_1)] sym ap List.sigmaTR [up(u_2) up(u_1)] sym ap
  gl bm0 ;; ctx: {bf0} ;; tgt: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 bv 0 bv ap lam ap ap pi pi pi pi ap List.sigma [up(u_2) up(u_1)] sym ap List.sigmaTR [up(u_2) up(u_1)] sym ap
  mv bm0 ;; knd: SYNTHETIC_OPAQUE ;; ty: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT 
... [2722 more characters]
```

### FINALIST R_01d4e489af53

*4,254 characters*

```text
(mta
  (smy (thm List.sigma_eq_sigmaTR) (fl .lake/packages/batteries/Batteries/Data/List/Basic.lean))
)
(sb
  (dc f0 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))))
  (gl m0 (ctx [f0]) (tgt (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))))
  (mv m0 (knd SYNTHETIC_OPAQUE) (ty (ap (ap (ap (sym Eq [umax(us(us(u
... [3054 more characters]
```

### FINALIST R_101e806690b0

*5,685 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))
  A $a1
    t-> (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)]))
  A $a2
    t-> (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u
... [4485 more characters]
```

### FINALIST R_28b291b5ebe6

*4,406 characters*

```text
meta
  summary ;; theorem-> List.sigma_eq_sigmaTR ;; file-> .lake/packages/batteries/Batteries/Data/List/Basic.lean
state_before
  decl f0 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 bv 0 bv ap lam ap ap pi pi pi pi ap List.sigma [up(u_2) up(u_1)] sym ap List.sigmaTR [up(u_2) up(u_1)] sym ap
  goal m0 ;; context-> [f0] ;; target-> Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 bv 0 bv ap lam ap ap pi pi pi pi ap List.sigma [up(u_2) up(u_1)] sym ap List.sigmaTR [up(u_2) up(u_1)] sym ap
  mvar m0 ;; kind-> SYNTHETIC_OPAQUE ;; type-> Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 b
... [3206 more characters]
```

## Example 2 — `Mathlib/Order/Interval/Finset/Fin.lean::Fin.map_valEmbedding_Ioi::0`

**Shape:** 1 goal(s), 4 local declaration(s), 0 external premise(s). Domain `Order`.

### SEED_LEAN_LIKE

*7,493 characters*

```text
#
  Y
    TH: Fin.map_valEmbedding_Ioi
    FL: Mathlib/Order/Interval/Finset/Fin.lean
Σ₀
  D n~bf0
    n: n
    b: IMPLICIT
    d: cdecl
    ∈: sym(Nat,[])
  D a~bf1
    n: a
    b: EXPLICIT
    d: cdecl
    ∈: ap(sym(Fin,[]),fv(n~bf0))
  D b~bf2
    n: b
    b: EXPLICIT
    d: cdecl
    ∈: ap(sym(Fin,[]),fv(n~bf0))
  D map_valEmbedding_Ioi~bf3
    n: map_valEmbedding_Ioi
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Finset,[u0]),sym(Nat,[]))),ap(ap(ap(ap(sym(Finset.map,[u0 u0]),ap(sym(Fin,[]),fv(n~bf0))),sym(Nat,[])),ap(sym(Fin.valEmbedding,[]),fv(n~bf0))),ap(ap(ap(ap(sym(Finset.Ioi,[u0]),ap(sym(Fin,[]),fv(n~bf0))),ap(ap(sym(PartialOrder.toPreorder,[u0]),ap(sym(Fin,[]),fv(n~bf0))),ap(sym(Fin.instPartialOrder,[]),fv(n~bf0)))),ap(sym(Fin.instLocallyFiniteOrderTop,[]),fv(n~bf0))),fv(a~bf1)))),ap(ap(ap(ap(ap(sym(Finset.Ioc,[u0]),sym(Nat,[])),ap(ap(sym(PartialOrder.toPreorder,[u0]),sym(Nat,[])),ap(ap(sym(SemilatticeInf.toPartialOrder,[u0]),sym(Nat,[])),ap(ap(sym(Lattice.toSemilatticeInf,[u0]),sym(Nat,[])),ap(ap(sym(DistribLattice.toLattice,[u0]),sym(Nat,[])),sym(instDistribLatticeNat,[])))))),sym(Nat.instLocallyFiniteOrder,[])),ap(ap(sym(Fin.val,[]),fv(n~bf0)),fv
... [6293 more characters]
```

### SEED_PRIOR_HML

*8,250 characters*

```text
meta
  summary
    theorem: Fin.map_valEmbedding_Ioi
    file: Mathlib/Order/Interval/Finset/Fin.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sym Nat [])
  decl bf1
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (sym Fin []) (fv bf0))
  decl bf2
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (sym Fin []) (fv bf0))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (sym Finset.map [u0 u0]) (ap (sym Fin []) (fv bf0))) (sym Nat [])) (ap (sym Fin.valEmbedding []) (fv bf0))) (ap (ap (ap (ap (sym Finset.Ioi [u0]) (ap (sym Fin []) (fv bf0))) (ap (ap (sym PartialOrder.toPreorder [u0]) (ap (sym Fin []) (fv bf0))) (ap (sym Fin.instPartialOrder []) (fv bf0)))) (ap (sym Fin.instLocallyFiniteOrderTop []) (fv bf0))) (fv bf1)))) (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) 
... [7050 more characters]
```

### SEED_STRUCTURED_ENGLISH

*8,202 characters*

```text
In meta:
  summary has theorem is Fin.map_valEmbedding_Ioi; and file is Mathlib/Order/Interval/Finset/Fin.lean .
In state_before:
  decl n~bf0 has display is n; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(Nat,[]) .
  decl a~bf1 has display is a; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(sym(Fin,[]),fv(n~bf0)) .
  decl b~bf2 has display is b; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(sym(Fin,[]),fv(n~bf0)) .
  decl map_valEmbedding_Ioi~bf3 has display is map_valEmbedding_Ioi; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Finset,[u0]),sym(Nat,[]))),ap(ap(ap(ap(sym(Finset.map,[u0 u0]),ap(sym(Fin,[]),fv(n~bf0))),sym(Nat,[])),ap(sym(Fin.valEmbedding,[]),fv(n~bf0))),ap(ap(ap(ap(sym(Finset.Ioi,[u0]),ap(sym(Fin,[]),fv(n~bf0))),ap(ap(sym(PartialOrder.toPreorder,[u0]),ap(sym(Fin,[]),fv(n~bf0))),ap(sym(Fin.instPartialOrder,[]),fv(n~bf0)))),ap(sym(Fin.instLocallyFiniteOrderTop,[]),fv(n~bf0))),fv(a~bf1)))),ap(ap(ap(ap(ap(sym(Finset.Ioc,[u0]),sym(Nat,[])),ap(ap(sym(PartialOrder.toPreorder,[u0]),sym(Nat,[])),ap(ap(sym(SemilatticeInf.toPartial
... [7002 more characters]
```

### SEED_TYPED_AST

*7,892 characters*

```text
mta
  - smy
    thm: Fin.map_valEmbedding_Ioi
    fl: Mathlib/Order/Interval/Finset/Fin.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sym|Nat,[]}
  - dc bf1
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{sym|Fin,[]},{fv|bf0}}
  - dc bf2
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{sym|Fin,[]},{fv|bf0}}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{sym|Eq,[us{u0}]},{ap|{sym|Finset,[u0]},{sym|Nat,[]}}},{ap|{ap|{ap|{ap|{sym|Finset.map,[u0 u0]},{ap|{sym|Fin,[]},{fv|bf0}}},{sym|Nat,[]}},{ap|{sym|Fin.valEmbedding,[]},{fv|bf0}}},{ap|{ap|{ap|{ap|{sym|Finset.Ioi,[u0]},{ap|{sym|Fin,[]},{fv|bf0}}},{ap|{ap|{sym|PartialOrder.toPreorder,[u0]},{ap|{sym|Fin,[]},{fv|bf0}}},{ap|{sym|Fin.instPartialOrder,[]},{fv|bf0}}}},{ap|{sym|Fin.instLocallyFiniteOrderTop,[]},{fv|bf0}}},{fv|bf1}}}},{ap|{ap|{ap|{ap|{ap|{sym|Finset.Ioc,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|PartialOrder.toPreorder,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|SemilatticeInf.toPartialOrder,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|Lattice.toSemilatticeInf,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|DistribLattice.toLattice,[u0]},{sym|Nat,[]}},{sym|instDistribLatticeNat,[]}}}}}},{sym|Nat.instLocallyFiniteOrder,[]}},{ap|{ap|{sym|Fin.val,[]},{fv|bf0
... [6692 more characters]
```

### FINALIST R_5b2eb732ac8b

*6,699 characters*

```text
#
  Y
    TH: Fin.map_valEmbedding_Ioi
    FL: Mathlib/Order/Interval/Finset/Fin.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: []
    L: [Mathlib/Order/Interval/Finset/Fin.lean::Fin.map_valEmbedding_Ioi::0:before:local:f2]
Σ₀
  □ bm0
    ⊢: Eq [us(u0)] sym Finset [u0] sym Nat [] sym ap ap Finset.map [u0 u0] sym Fin [] sym bf0 fv ap ap Nat [] sym ap Fin.valEmbedding [] sym bf0 fv ap ap Finset.Ioi [u0] sym Fin [] sym bf0 fv ap ap PartialOrder.toPreorder [u0] sym Fin [] sym bf0 fv ap ap Fin.instPartialOrder [] sym bf0 fv ap ap ap Fin.instLocallyFiniteOrderTop [] sym bf0 fv ap ap bf1 fv ap ap ap Finset.Ioc [u0] sym Nat [] sym ap PartialOrder.toPreorder [u0] sym Nat [] sym ap SemilatticeInf.toPartialOrder [u0] sym Nat [] sym ap Lattice.toSemilatticeInf [u0] sym Nat [] sym ap DistribLattice.toLattice [u0] sym Nat [] sym ap instDistribLatticeNat [] sym ap ap ap ap ap Nat.instLocallyFiniteOrder [] sym ap Fin.val [] sym bf0 fv ap bf1 fv ap ap HSub.hSub [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHSub [u0] sym Nat [] sym ap instSubNat [] sym ap ap bf0 fv ap OfNat.ofNat [u0] sym Nat [] sym ap NAT 1 lit ap instOf
... [5499 more characters]
```

### FINALIST R_000441b08de4

*6,680 characters*

```text
mta
  smy ;; thm: Fin.map_valEmbedding_Ioi ;; fl: Mathlib/Order/Interval/Finset/Fin.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Nat [] sym
  dc bf1 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Fin [] sym bf0 fv ap
  dc bf2 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Fin [] sym bf0 fv ap
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Eq [us(u0)] sym Finset [u0] sym Nat [] sym ap ap Finset.map [u0 u0] sym Fin [] sym bf0 fv ap ap Nat [] sym ap Fin.valEmbedding [] sym bf0 fv ap ap Finset.Ioi [u0] sym Fin [] sym bf0 fv ap ap PartialOrder.toPreorder [u0] sym Fin [] sym bf0 fv ap ap Fin.instPartialOrder [] sym bf0 fv ap ap ap Fin.instLocallyFiniteOrderTop [] sym bf0 fv ap ap bf1 fv ap ap ap Finset.Ioc [u0] sym Nat [] sym ap PartialOrder.toPreorder [u0] sym Nat [] sym ap SemilatticeInf.toPartialOrder [u0] sym Nat [] sym ap Lattice.toSemilatticeInf [u0] sym Nat [] sym ap DistribLattice.toLattice [u0] sym Nat [] sym ap instDistribLatticeNat [] sym ap ap ap ap ap Nat.instLocallyFiniteOrder [] sym ap Fin.val [] sym bf0 fv ap bf1 fv ap ap HSub.hSub [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHSub [u0] sym Nat [] sym ap instSubNat [] sym ap ap bf0 fv ap OfNat.ofNat [u0] sym Nat [] sym ap 
... [5480 more characters]
```

### FINALIST R_01d4e489af53

*7,635 characters*

```text
(mta
  (smy (thm Fin.map_valEmbedding_Ioi) (fl Mathlib/Order/Interval/Finset/Fin.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc f1 (br EXPLICIT) (dr cdecl) (ty (ap (sym Fin []) (fv f0))))
  (dc f2 (br EXPLICIT) (dr cdecl) (ty (ap (sym Fin []) (fv f0))))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (sym Finset.map [u0 u0]) (ap (sym Fin []) (fv f0))) (sym Nat [])) (ap (sym Fin.valEmbedding []) (fv f0))) (ap (ap (ap (ap (sym Finset.Ioi [u0]) (ap (sym Fin []) (fv f0))) (ap (ap (sym PartialOrder.toPreorder [u0]) (ap (sym Fin []) (fv f0))) (ap (sym Fin.instPartialOrder []) (fv f0)))) (ap (sym Fin.instLocallyFiniteOrderTop []) (fv f0))) (fv f1)))) (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (ap (ap (sym Fin.val []) (fv f0)) (fv f1))) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u
... [6435 more characters]
```

### FINALIST R_101e806690b0

*8,657 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (sym Finset.map [u0 u0]) (ap (sym Fin []) (fv bf0))) (sym Nat [])) (ap (sym Fin.valEmbedding []) (fv bf0))) (ap (ap (ap (ap (sym Finset.Ioi [u0]) (ap (sym Fin []) (fv bf0))) (ap (ap (sym PartialOrder.toPreorder [u0]) (ap (sym Fin []) (fv bf0))) (ap (sym Fin.instPartialOrder []) (fv bf0)))) (ap (sym Fin.instLocallyFiniteOrderTop []) (fv bf0))) (fv bf1)))) (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (ap (ap (sym Fin.val []) (fv bf0)) (fv bf1))) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHSub [u0]) (sym Nat [])) (sym instSubNat []))) (fv bf0)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 1)) (ap (sym instOfNatNat []) (lit NAT 1))))))
  A $a1
    t-> (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (
... [7457 more characters]
```

### FINALIST R_28b291b5ebe6

*7,419 characters*

```text
meta
  summary ;; theorem-> Fin.map_valEmbedding_Ioi ;; file-> Mathlib/Order/Interval/Finset/Fin.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Nat [] sym
  decl f1 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Fin [] sym f0 fv ap
  decl f2 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Fin [] sym f0 fv ap
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Eq [us(u0)] sym Finset [u0] sym Nat [] sym ap ap Finset.map [u0 u0] sym Fin [] sym f0 fv ap ap Nat [] sym ap Fin.valEmbedding [] sym f0 fv ap ap Finset.Ioi [u0] sym Fin [] sym f0 fv ap ap PartialOrder.toPreorder [u0] sym Fin [] sym f0 fv ap ap Fin.instPartialOrder [] sym f0 fv ap ap ap Fin.instLocallyFiniteOrderTop [] sym f0 fv ap ap f1 fv ap ap ap Finset.Ioc [u0] sym Nat [] sym ap PartialOrder.toPreorder [u0] sym Nat [] sym ap SemilatticeInf.toPartialOrder [u0] sym Nat [] sym ap Lattice.toSemilatticeInf [u0] sym Nat [] sym ap DistribLattice.toLattice [u0] sym Nat [] sym ap instDistribLatticeNat [] sym ap ap ap ap ap Nat.instLocallyFiniteOrder [] sym ap Fin.val [] sym f0 fv ap f1 fv ap ap HSub.hSub [u0 u0 u0] sym Nat [] sym ap N
... [6219 more characters]
```

## Example 3 — `Mathlib/SetTheory/Ordinal/Notation.lean::ONote.sub_nfBelow::0`

**Shape:** 1 goal(s), 5 local declaration(s), 1 external premise(s). Domain `SetTheory`.

### SEED_LEAN_LIKE

*2,485 characters*

```text
#
  Y
    TH: ONote.sub_nfBelow
    FL: Mathlib/SetTheory/Ordinal/Notation.lean
Σ₀
  D sub_nfBelow~bf0
    n: sub_nfBelow
    b: EXPLICIT
    d: cdecl
    ∈: pi(IMPLICIT,sym(ONote,[]),pi(IMPLICIT,sym(ONote,[]),pi(IMPLICIT,sym(Ordinal,[u0]),pi(EXPLICIT,ap(ap(sym(ONote.NFBelow,[]),bv(2)),bv(0)),pi(EXPLICIT,ap(sym(ONote.NF,[]),bv(2)),ap(ap(sym(ONote.NFBelow,[]),ap(ap(ap(ap(ap(ap(sym(HSub.hSub,[u0 u0 u0]),sym(ONote,[])),sym(ONote,[])),sym(ONote,[])),ap(ap(sym(instHSub,[u0]),sym(ONote,[])),sym(ONote.instSub,[]))),bv(4)),bv(3))),bv(2)))))))
  D o~bf1
    n: o
    b: EXPLICIT
    d: cdecl
    ∈: sym(ONote,[])
  D b~bf2
    n: b
    b: EXPLICIT
    d: cdecl
    ∈: sym(Ordinal,[u0])
  D x._@.Mathlib.SetTheory.Ordinal.Notation._hyg.5834~bf3
    n: x._@.Mathlib.SetTheory.Ordinal.Notation._hyg.5834
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(sym(ONote.NFBelow,[]),ap(ap(ap(sym(OfNat.ofNat,[u0]),sym(ONote,[])),lit(NAT,0)),ap(sym(ONote.nat,[]),lit(NAT,0)))),fv(b~bf2))
  D h₂~bf4
    n: h₂
    b: EXPLICIT
    d: cdecl
    ∈: ap(sym(ONote.NF,[]),fv(o~bf1))
  □ bm0
    Γ: [sub_nfBelow~bf0,o~bf1,b~bf2,x._@.Mathlib.SetTheory.Ordinal.Notation._hyg.5834~bf3,h₂~bf4]
    ⊢: ap(ap(sym(ONote.NFBelow,[]),ap(ap
... [1285 more characters]
```

### SEED_PRIOR_HML

*2,721 characters*

```text
meta
  summary
    theorem: ONote.sub_nfBelow
    file: Mathlib/SetTheory/Ordinal/Notation.lean
state_before
  decl bf0
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi IMPLICIT (sym ONote []) (pi IMPLICIT (sym ONote []) (pi IMPLICIT (sym Ordinal [u0]) (pi EXPLICIT (ap (ap (sym ONote.NFBelow []) (bv 2)) (bv 0)) (pi EXPLICIT (ap (sym ONote.NF []) (bv 2)) (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (bv 4)) (bv 3))) (bv 2)))))))
  decl bf1
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sym ONote [])
  decl bf2
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sym Ordinal [u0])
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf2))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (sym ONote.NF []) (fv bf1))
  goal bm0
    context: [bf0,bf1,bf2,bf3,bf4]
    target: (ap (ap (sym ONote.NFBelow []
... [1521 more characters]
```

### SEED_STRUCTURED_ENGLISH

*3,047 characters*

```text
In meta:
  summary has theorem is ONote.sub_nfBelow; and file is Mathlib/SetTheory/Ordinal/Notation.lean .
In state_before:
  decl sub_nfBelow~bf0 has display is sub_nfBelow; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(IMPLICIT,sym(ONote,[]),pi(IMPLICIT,sym(ONote,[]),pi(IMPLICIT,sym(Ordinal,[u0]),pi(EXPLICIT,ap(ap(sym(ONote.NFBelow,[]),bv(2)),bv(0)),pi(EXPLICIT,ap(sym(ONote.NF,[]),bv(2)),ap(ap(sym(ONote.NFBelow,[]),ap(ap(ap(ap(ap(ap(sym(HSub.hSub,[u0 u0 u0]),sym(ONote,[])),sym(ONote,[])),sym(ONote,[])),ap(ap(sym(instHSub,[u0]),sym(ONote,[])),sym(ONote.instSub,[]))),bv(4)),bv(3))),bv(2))))))) .
  decl o~bf1 has display is o; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sym(ONote,[]) .
  decl b~bf2 has display is b; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sym(Ordinal,[u0]) .
  decl x._@.Mathlib.SetTheory.Ordinal.Notation._hyg.5834~bf3 has display is x._@.Mathlib.SetTheory.Ordinal.Notation._hyg.5834; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(ONote.NFBelow,[]),ap(ap(ap(sym(OfNat.ofNat,[u0]),sym(ONote,[])),lit(NAT,0)),ap(sym(ONote.nat,[]),lit(NAT,0)))),fv(b~b
... [1847 more characters]
```

### SEED_TYPED_AST

*2,428 characters*

```text
mta
  - smy
    thm: ONote.sub_nfBelow
    fl: Mathlib/SetTheory/Ordinal/Notation.lean
sb
  - dc bf0
    br: EXPLICIT
    dr: cdecl
    ty: {pi|IMPLICIT,{sym|ONote,[]},{pi|IMPLICIT,{sym|ONote,[]},{pi|IMPLICIT,{sym|Ordinal,[u0]},{pi|EXPLICIT,{ap|{ap|{sym|ONote.NFBelow,[]},{bv|2}},{bv|0}},{pi|EXPLICIT,{ap|{sym|ONote.NF,[]},{bv|2}},{ap|{ap|{sym|ONote.NFBelow,[]},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HSub.hSub,[u0 u0 u0]},{sym|ONote,[]}},{sym|ONote,[]}},{sym|ONote,[]}},{ap|{ap|{sym|instHSub,[u0]},{sym|ONote,[]}},{sym|ONote.instSub,[]}}},{bv|4}},{bv|3}}},{bv|2}}}}}}}
  - dc bf1
    br: EXPLICIT
    dr: cdecl
    ty: {sym|ONote,[]}
  - dc bf2
    br: EXPLICIT
    dr: cdecl
    ty: {sym|Ordinal,[u0]}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|ONote.NFBelow,[]},{ap|{ap|{ap|{sym|OfNat.ofNat,[u0]},{sym|ONote,[]}},{lit|NAT,0}},{ap|{sym|ONote.nat,[]},{lit|NAT,0}}}},{fv|bf2}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{sym|ONote.NF,[]},{fv|bf1}}
  - gl bm0
    ctx: [bf0,bf1,bf2,bf3,bf4]
    tgt: {ap|{ap|{sym|ONote.NFBelow,[]},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HSub.hSub,[u0 u0 u0]},{sym|ONote,[]}},{sym|ONote,[]}},{sym|ONote,[]}},{ap|{ap|{sym|instHSub,[u0]},{sym|ONote,[]}},{sym|O
... [1228 more characters]
```

### FINALIST R_5b2eb732ac8b

*2,164 characters*

```text
#
  Y
    TH: ONote.sub_nfBelow
    FL: Mathlib/SetTheory/Ordinal/Notation.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [ONote.NFBelow.zero]
    L: [Mathlib/SetTheory/Ordinal/Notation.lean::ONote.sub_nfBelow::0:before:local:f1]
Σ₀
  □ bm0
    ⊢: ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ap ONote [] sym ap ONote [] sym ap instHSub [u0] sym ONote [] sym ap ONote.instSub [] sym ap ap OfNat.ofNat [u0] sym ONote [] sym ap NAT 0 lit ap ONote.nat [] sym NAT 0 lit ap ap ap bf1 fv ap ap bf2 fv ap
    Γ: [bf0,bf1,bf2,bf3,bf4]
  A bf1
    tg: ONote
  A bf2
    tg: Ordinal
  D bf0
    b: EXPLICIT
    d: cdecl
    ∈: IMPLICIT ONote [] sym IMPLICIT ONote [] sym IMPLICIT Ordinal [u0] sym EXPLICIT ONote.NFBelow [] sym 2 bv ap 0 bv ap EXPLICIT ONote.NF [] sym 2 bv ap ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ap ONote [] sym ap ONote [] sym ap instHSub [u0] sym ONote [] sym ap ONote.instSub [] sym ap ap 4 bv ap 3 bv ap ap 2 bv ap pi pi pi pi pi
  D bf1
    b: EXPLICIT
    d: cdecl
    ∈: ONote [] sym
  D bf2
    b: EXPLICIT
    d: cdecl
    ∈: Ordinal [u0] sym
  D bf3
    b: EXPLICIT
    d: cdecl
    
... [964 more characters]
```

### FINALIST R_000441b08de4

*2,171 characters*

```text
mta
  smy ;; thm: ONote.sub_nfBelow ;; fl: Mathlib/SetTheory/Ordinal/Notation.lean
sb
  dc bf0 ;; br: EXPLICIT ;; dr: cdecl ;; ty: IMPLICIT ONote [] sym IMPLICIT ONote [] sym IMPLICIT Ordinal [u0] sym EXPLICIT ONote.NFBelow [] sym 2 bv ap 0 bv ap EXPLICIT ONote.NF [] sym 2 bv ap ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ap ONote [] sym ap ONote [] sym ap instHSub [u0] sym ONote [] sym ap ONote.instSub [] sym ap ap 4 bv ap 3 bv ap ap 2 bv ap pi pi pi pi pi
  dc bf1 ;; br: EXPLICIT ;; dr: cdecl ;; ty: ONote [] sym
  dc bf2 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Ordinal [u0] sym
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: ONote.NFBelow [] sym OfNat.ofNat [u0] sym ONote [] sym ap NAT 0 lit ap ONote.nat [] sym NAT 0 lit ap ap ap bf2 fv ap
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: ONote.NF [] sym bf1 fv ap
  gl bm0 ;; ctx: {bf0 bf1 bf2 bf3 bf4} ;; tgt: ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ap ONote [] sym ap ONote [] sym ap instHSub [u0] sym ONote [] sym ap ONote.instSub [] sym ap ap OfNat.ofNat [u0] sym ONote [] sym ap NAT 0 lit ap ONote.nat [] sym NAT 0 lit ap ap ap bf1 fv ap ap bf2 fv ap
  mv bm0 ;; knd: SYNTHETIC_OPAQUE ;; ty: ONote.NFBelow [] s
... [971 more characters]
```

### FINALIST R_01d4e489af53

*2,292 characters*

```text
(mta
  (smy (thm ONote.sub_nfBelow) (fl Mathlib/SetTheory/Ordinal/Notation.lean))
)
(sb
  (dc f0 (br EXPLICIT) (dr cdecl) (ty (pi IMPLICIT (sym ONote []) (pi IMPLICIT (sym ONote []) (pi IMPLICIT (sym Ordinal [u0]) (pi EXPLICIT (ap (ap (sym ONote.NFBelow []) (bv 2)) (bv 0)) (pi EXPLICIT (ap (sym ONote.NF []) (bv 2)) (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (bv 4)) (bv 3))) (bv 2)))))))))
  (dc f1 (br EXPLICIT) (dr cdecl) (ty (sym ONote [])))
  (dc f2 (br EXPLICIT) (dr cdecl) (ty (sym Ordinal [u0])))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit 0)) (ap (sym ONote.nat []) (lit 0)))) (fv f2))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (ap (sym ONote.NF []) (fv f1))))
  (gl m0 (ctx [f0,f1,f2,f3,f4]) (tgt (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit 0
... [1092 more characters]
```

### FINALIST R_101e806690b0

*3,531 characters*

```text
$
  A $a0
    t-> (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf1))) (fv bf2))
  A $a1
    t-> (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf1)))
  A $a2
    t-> (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf1))
  A $a3
    t-> (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 
... [2331 more characters]
```

### FINALIST R_28b291b5ebe6

*2,619 characters*

```text
meta
  summary ;; theorem-> ONote.sub_nfBelow ;; file-> Mathlib/SetTheory/Ordinal/Notation.lean
state_before
  decl f0 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> IMPLICIT ONote [] sym IMPLICIT ONote [] sym IMPLICIT Ordinal [u0] sym EXPLICIT ONote.NFBelow [] sym 2 bv ap 0 bv ap EXPLICIT ONote.NF [] sym 2 bv ap ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ap ONote [] sym ap ONote [] sym ap instHSub [u0] sym ONote [] sym ap ONote.instSub [] sym ap ap 4 bv ap 3 bv ap ap 2 bv ap pi pi pi pi pi
  decl f1 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> ONote [] sym
  decl f2 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Ordinal [u0] sym
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> ONote.NFBelow [] sym OfNat.ofNat [u0] sym ONote [] sym ap NAT 0 lit ap ONote.nat [] sym NAT 0 lit ap ap ap f2 fv ap
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> ONote.NF [] sym f1 fv ap
  goal m0 ;; context-> [f0,f1,f2,f3,f4] ;; target-> ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ap ONote [] sym ap ONote [] sym ap instHSub [u0] sym ONote [] sym ap ONote.instSub [] sym ap 
... [1419 more characters]
```

## Example 4 — `Mathlib/Computability/TMToPartrec.lean::Turing.ToPartrec.code_is_ok::14`

**Shape:** 1 goal(s), 7 local declaration(s), 3 external premise(s). Domain `Computability`.

### SEED_LEAN_LIKE

*7,773 characters*

```text
#
  Y
    TH: Turing.ToPartrec.code_is_ok
    FL: Mathlib/Computability/TMToPartrec.lean
Σ₀
  D code_is_ok~bf0
    n: code_is_ok
    b: EXPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,sym(Turing.ToPartrec.Code,[]),ap(sym(Turing.ToPartrec.Code.Ok,[]),bv(0)))
  D f~bf1
    n: f
    b: EXPLICIT
    d: cdecl
    ∈: sym(Turing.ToPartrec.Code,[])
  D g~bf2
    n: g
    b: EXPLICIT
    d: cdecl
    ∈: sym(Turing.ToPartrec.Code,[])
  D IHf~bf3
    n: IHf
    b: EXPLICIT
    d: cdecl
    ∈: ap(mv(bm0),fv(f~bf1))
  D IHg~bf4
    n: IHg
    b: EXPLICIT
    d: cdecl
    ∈: ap(mv(bm0),fv(g~bf2))
  D k~bf5
    n: k
    b: EXPLICIT
    d: cdecl
    ∈: sym(Turing.ToPartrec.Cont,[])
  D v~bf6
    n: v
    b: EXPLICIT
    d: cdecl
    ∈: ap(sym(List,[u0]),sym(Nat,[]))
  □ bm1
    Γ: [code_is_ok~bf0,f~bf1,g~bf2,IHf~bf3,IHg~bf4,k~bf5,v~bf6]
    ⊢: ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Part,[u0]),sym(Turing.ToPartrec.Cfg,[]))),ap(ap(ap(ap(ap(ap(sym(Bind.bind,[u0 u0]),sym(Part,[u0])),ap(ap(sym(Monad.toBind,[u0 u0]),sym(Part,[u0])),sym(Part.instMonad,[u0]))),ap(sym(List,[u0]),sym(Nat,[]))),sym(Turing.ToPartrec.Cfg,[])),ap(ap(sym(Turing.ToPartrec.Code.eval,[]),fv(g~bf2)),fv(v~bf6))),lam(EXPLICIT,ap(sym(List,[u0]),sym
... [6573 more characters]
```

### SEED_PRIOR_HML

*8,675 characters*

```text
meta
  summary
    theorem: Turing.ToPartrec.code_is_ok
    file: Mathlib/Computability/TMToPartrec.lean
state_before
  decl bf0
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (sym Turing.ToPartrec.Code []) (ap (sym Turing.ToPartrec.Code.Ok []) (bv 0)))
  decl bf1
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sym Turing.ToPartrec.Code [])
  decl bf2
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sym Turing.ToPartrec.Code [])
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (mv bm0) (fv bf1))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (mv bm0) (fv bf2))
  decl bf5
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sym Turing.ToPartrec.Cont [])
  decl bf6
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (sym List [u0]) (sym Nat []))
  goal bm1
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6]
    target: (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Part [u0]) (sym Turing.ToPartrec.Cfg []))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) 
... [7475 more characters]
```

### SEED_STRUCTURED_ENGLISH

*8,908 characters*

```text
In meta:
  summary has theorem is Turing.ToPartrec.code_is_ok; and file is Mathlib/Computability/TMToPartrec.lean .
In state_before:
  decl code_is_ok~bf0 has display is code_is_ok; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,sym(Turing.ToPartrec.Code,[]),ap(sym(Turing.ToPartrec.Code.Ok,[]),bv(0))) .
  decl f~bf1 has display is f; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sym(Turing.ToPartrec.Code,[]) .
  decl g~bf2 has display is g; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sym(Turing.ToPartrec.Code,[]) .
  decl IHf~bf3 has display is IHf; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(mv(bm0),fv(f~bf1)) .
  decl IHg~bf4 has display is IHg; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(mv(bm0),fv(g~bf2)) .
  decl k~bf5 has display is k; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sym(Turing.ToPartrec.Cont,[]) .
  decl v~bf6 has display is v; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(sym(List,[u0]),sym(Nat,[])) .
  goal bm1 has context is [code_is_ok~bf0,f~bf1,g~bf2,I
... [7708 more characters]
```

### SEED_TYPED_AST

*8,112 characters*

```text
mta
  - smy
    thm: Turing.ToPartrec.code_is_ok
    fl: Mathlib/Computability/TMToPartrec.lean
sb
  - dc bf0
    br: EXPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{sym|Turing.ToPartrec.Code,[]},{ap|{sym|Turing.ToPartrec.Code.Ok,[]},{bv|0}}}
  - dc bf1
    br: EXPLICIT
    dr: cdecl
    ty: {sym|Turing.ToPartrec.Code,[]}
  - dc bf2
    br: EXPLICIT
    dr: cdecl
    ty: {sym|Turing.ToPartrec.Code,[]}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{mv|bm0},{fv|bf1}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{mv|bm0},{fv|bf2}}
  - dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: {sym|Turing.ToPartrec.Cont,[]}
  - dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{sym|List,[u0]},{sym|Nat,[]}}
  - gl bm1
    ctx: [bf0,bf1,bf2,bf3,bf4,bf5,bf6]
    tgt: {ap|{ap|{ap|{sym|Eq,[us{u0}]},{ap|{sym|Part,[u0]},{sym|Turing.ToPartrec.Cfg,[]}}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|Bind.bind,[u0 u0]},{sym|Part,[u0]}},{ap|{ap|{sym|Monad.toBind,[u0 u0]},{sym|Part,[u0]}},{sym|Part.instMonad,[u0]}}},{ap|{sym|List,[u0]},{sym|Nat,[]}}},{sym|Turing.ToPartrec.Cfg,[]}},{ap|{ap|{sym|Turing.ToPartrec.Code.eval,[]},{fv|bf2}},{fv|bf6}}},{lam|EXPLICIT,{ap|{sym|List,[u0]},{sym|Nat,[]}},{ap|{ap|{ap|{sym|Turin
... [6912 more characters]
```

### FINALIST R_5b2eb732ac8b

*7,213 characters*

```text
#
  Y
    TH: Turing.ToPartrec.code_is_ok
    FL: Mathlib/Computability/TMToPartrec.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [LawfulMonad.bind_assoc,LawfulMonad.pure_bind,Turing.ToPartrec.Cont.eval]
    L: []
Σ₀
  □ bm1
    ⊢: Eq [us(u0)] sym Part [u0] sym Turing.ToPartrec.Cfg [] sym ap ap Bind.bind [u0 u0] sym Part [u0] sym ap Monad.toBind [u0 u0] sym Part [u0] sym ap Part.instMonad [u0] sym ap ap List [u0] sym Nat [] sym ap ap Turing.ToPartrec.Cfg [] sym ap Turing.ToPartrec.Code.eval [] sym bf2 fv ap bf6 fv ap ap EXPLICIT List [u0] sym Nat [] sym ap Turing.eval [u0] sym Turing.ToPartrec.Cfg [] sym ap Turing.ToPartrec.step [] sym ap Turing.ToPartrec.Cfg.ret [] sym Turing.ToPartrec.Cont.comp [] sym bf1 fv ap bf5 fv ap ap 0 bv ap ap lam ap ap Bind.bind [u0 u0] sym Part [u0] sym ap Monad.toBind [u0 u0] sym Part [u0] sym ap Part.instMonad [u0] sym ap ap List [u0] sym Nat [] sym ap ap Turing.ToPartrec.Cfg [] sym ap EXPLICIT List [u0] sym Nat [] sym ap Bind.bind [u0 u0] sym Part [u0] sym ap Monad.toBind [u0 u0] sym Part [u0] sym ap Part.instMonad [u0] sym ap ap List [u0] sym Nat [] sym ap ap List [u0] sym Nat [] sym a
... [6013 more characters]
```

### FINALIST R_000441b08de4

*6,980 characters*

```text
mta
  smy ;; thm: Turing.ToPartrec.code_is_ok ;; fl: Mathlib/Computability/TMToPartrec.lean
sb
  dc bf0 ;; br: EXPLICIT ;; dr: cdecl ;; ty: EXPLICIT Turing.ToPartrec.Code [] sym Turing.ToPartrec.Code.Ok [] sym 0 bv ap pi
  dc bf1 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Turing.ToPartrec.Code [] sym
  dc bf2 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Turing.ToPartrec.Code [] sym
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: bm0 mv bf1 fv ap
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: bm0 mv bf2 fv ap
  dc bf5 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Turing.ToPartrec.Cont [] sym
  dc bf6 ;; br: EXPLICIT ;; dr: cdecl ;; ty: List [u0] sym Nat [] sym ap
  gl bm1 ;; ctx: {bf0 bf1 bf2 bf3 bf4 bf5 bf6} ;; tgt: Eq [us(u0)] sym Part [u0] sym Turing.ToPartrec.Cfg [] sym ap ap Bind.bind [u0 u0] sym Part [u0] sym ap Monad.toBind [u0 u0] sym Part [u0] sym ap Part.instMonad [u0] sym ap ap List [u0] sym Nat [] sym ap ap Turing.ToPartrec.Cfg [] sym ap Turing.ToPartrec.Code.eval [] sym bf2 fv ap bf6 fv ap ap EXPLICIT List [u0] sym Nat [] sym ap Turing.eval [u0] sym Turing.ToPartrec.Cfg [] sym ap Turing.ToPartrec.step [] sym ap Turing.ToPartrec.Cfg.ret [] sym Turing.ToPartrec.Cont.comp [] sym bf1 fv ap bf5 fv ap ap 0
... [5780 more characters]
```

### FINALIST R_01d4e489af53

*7,823 characters*

```text
(mta
  (smy (thm Turing.ToPartrec.code_is_ok) (fl Mathlib/Computability/TMToPartrec.lean))
)
(sb
  (dc f0 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (sym Turing.ToPartrec.Code []) (ap (sym Turing.ToPartrec.Code.Ok []) (bv 0)))))
  (dc f1 (br EXPLICIT) (dr cdecl) (ty (sym Turing.ToPartrec.Code [])))
  (dc f2 (br EXPLICIT) (dr cdecl) (ty (sym Turing.ToPartrec.Code [])))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (ap (mv m0) (fv f1))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (ap (mv m0) (fv f2))))
  (dc f5 (br EXPLICIT) (dr cdecl) (ty (sym Turing.ToPartrec.Cont [])))
  (dc f6 (br EXPLICIT) (dr cdecl) (ty (ap (sym List [u0]) (sym Nat []))))
  (gl m1 (ctx [f0,f1,f2,f3,f4,f5,f6]) (tgt (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Part [u0]) (sym Turing.ToPartrec.Cfg []))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv f2)) (fv f6))) (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (sym Turing.eval [u0]) (sym Turing.ToPartrec.Cfg [])) (sym Turing.ToPartrec.step [])) (ap (ap (sym Turin
... [6623 more characters]
```

### FINALIST R_101e806690b0

*14,726 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Part [u0]) (sym Turing.ToPartrec.Cfg []))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv bf2)) (fv bf6))) (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (sym Turing.eval [u0]) (sym Turing.ToPartrec.Cfg [])) (sym Turing.ToPartrec.step [])) (ap (ap (sym Turing.ToPartrec.Cfg.ret []) (ap (ap (sym Turing.ToPartrec.Cont.comp []) (fv bf1)) (fv bf5))) (bv 0)))))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (ap (sym List [u0]) (sym Nat []))) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv bf2)) (bv 0))) (ap (sym Turing.To
... [13526 more characters]
```

### FINALIST R_28b291b5ebe6

*7,808 characters*

```text
meta
  summary ;; theorem-> Turing.ToPartrec.code_is_ok ;; file-> Mathlib/Computability/TMToPartrec.lean
state_before
  decl f0 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT Turing.ToPartrec.Code [] sym Turing.ToPartrec.Code.Ok [] sym 0 bv ap pi
  decl f1 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Turing.ToPartrec.Code [] sym
  decl f2 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Turing.ToPartrec.Code [] sym
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> m0 mv f1 fv ap
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> m0 mv f2 fv ap
  decl f5 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Turing.ToPartrec.Cont [] sym
  decl f6 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> List [u0] sym Nat [] sym ap
  goal m1 ;; context-> [f0,f1,f2,f3,f4,f5,f6] ;; target-> Eq [us(u0)] sym Part [u0] sym Turing.ToPartrec.Cfg [] sym ap ap Bind.bind [u0 u0] sym Part [u0] sym ap Monad.toBind [u0 u0] sym Part [u0] sym ap Part.instMonad [u0] sym ap ap List [u0] sym Nat [] sym ap ap Turing.ToPartrec.Cfg [] sym ap Turing.ToPartrec.Code.eval [] sym f2 fv ap 
... [6608 more characters]
```

## Example 5 — `Mathlib/Data/Seq/WSeq.lean::Stream'.WSeq.head_terminates_of_head_tail_terminates::2`

**Shape:** 1 goal(s), 8 local declaration(s), 1 external premise(s). Domain `Data`.

### SEED_LEAN_LIKE

*10,276 characters*

```text
#
  Y
    TH: Stream'.WSeq.head_terminates_of_head_tail_terminates
    FL: Mathlib/Data/Seq/WSeq.lean
Σ₀
  D α~bf0
    n: α
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u)))
  D β~bf1
    n: β
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(v)))
  D γ~bf2
    n: γ
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(w)))
  D head_terminates_of_head_tail_terminates~bf3
    n: head_terminates_of_head_tail_terminates
    b: EXPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,ap(sym(Stream'.WSeq,[up(u)]),fv(α~bf0)),pi(INSTANCE_IMPLICIT,ap(ap(sym(Computation.Terminates,[up(u)]),ap(sym(Option,[up(u)]),fv(α~bf0))),ap(ap(sym(Stream'.WSeq.head,[up(u)]),fv(α~bf0)),ap(ap(sym(Stream'.WSeq.tail,[up(u)]),fv(α~bf0)),bv(0)))),ap(ap(sym(Computation.Terminates,[up(u)]),ap(sym(Option,[up(u)]),fv(α~bf0))),ap(ap(sym(Stream'.WSeq.head,[up(u)]),fv(α~bf0)),bv(1)))))
  D s~bf4
    n: s
    b: EXPLICIT
    d: cdecl
    ∈: ap(sym(Stream'.WSeq,[up(u)]),fv(α~bf0))
  D T~bf5
    n: T
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(ap(sym(Computation.Terminates,[up(u)]),ap(sym(Option,[up(u)]),fv(α~bf0))),ap(ap(sym(Stream'.WSeq.head,[up(u)]),fv(α~bf0)),ap(ap(sym(Stream'.WSeq.tail,[up(u)]),fv(α~bf0)),fv(s~bf4))))
  D a~bf6
    n:
... [9076 more characters]
```

### SEED_PRIOR_HML

*10,894 characters*

```text
meta
  summary
    theorem: Stream'.WSeq.head_terminates_of_head_tail_terminates
    file: Mathlib/Data/Seq/WSeq.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(v)))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(w)))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (ap (sym Stream'.WSeq [up(u)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv bf0)) (ap (ap (sym Stream'.WSeq.tail [up(u)]) (fv bf0)) (bv 0)))) (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv bf0)) (bv 1)))))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (sym Stream'.WSeq [up(u)]) (fv bf0))
  decl bf5
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.he
... [9694 more characters]
```

### SEED_STRUCTURED_ENGLISH

*11,585 characters*

```text
In meta:
  summary has theorem is Stream'.WSeq.head_terminates_of_head_tail_terminates; and file is Mathlib/Data/Seq/WSeq.lean .
In state_before:
  decl α~bf0 has display is α; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u))) .
  decl β~bf1 has display is β; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(v))) .
  decl γ~bf2 has display is γ; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(w))) .
  decl head_terminates_of_head_tail_terminates~bf3 has display is head_terminates_of_head_tail_terminates; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,ap(sym(Stream'.WSeq,[up(u)]),fv(α~bf0)),pi(INSTANCE_IMPLICIT,ap(ap(sym(Computation.Terminates,[up(u)]),ap(sym(Option,[up(u)]),fv(α~bf0))),ap(ap(sym(Stream'.WSeq.head,[up(u)]),fv(α~bf0)),ap(ap(sym(Stream'.WSeq.tail,[up(u)]),fv(α~bf0)),bv(0)))),ap(ap(sym(Computation.Terminates,[up(u)]),ap(sym(Option,[up(u)]),fv(α~bf0))),ap(ap(sym(Stream'.WSeq.head,[up(u)]),fv(α~bf0)),bv(1))))) .
  decl s~bf4 has display is s; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(sym(Stream'.WS
... [10385 more characters]
```

### SEED_TYPED_AST

*10,236 characters*

```text
mta
  - smy
    thm: Stream'.WSeq.head_terminates_of_head_tail_terminates
    fl: Mathlib/Data/Seq/WSeq.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u}}}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{v}}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{w}}}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{ap|{sym|Stream'.WSeq,[up{u}]},{fv|bf0}},{pi|INSTANCE_IMPLICIT,{ap|{ap|{sym|Computation.Terminates,[up{u}]},{ap|{sym|Option,[up{u}]},{fv|bf0}}},{ap|{ap|{sym|Stream'.WSeq.head,[up{u}]},{fv|bf0}},{ap|{ap|{sym|Stream'.WSeq.tail,[up{u}]},{fv|bf0}},{bv|0}}}},{ap|{ap|{sym|Computation.Terminates,[up{u}]},{ap|{sym|Option,[up{u}]},{fv|bf0}}},{ap|{ap|{sym|Stream'.WSeq.head,[up{u}]},{fv|bf0}},{bv|1}}}}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{sym|Stream'.WSeq,[up{u}]},{fv|bf0}}
  - dc bf5
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|Computation.Terminates,[up{u}]},{ap|{sym|Option,[up{u}]},{fv|bf0}}},{ap|{ap|{sym|Stream'.WSeq.head,[up{u}]},{fv|bf0}},{ap|{ap|{sym|Stream'.WSeq.tail,[up{u}]},{fv|bf0}},{fv|bf4}}}}
  - dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{sym|Option,[up{u}]},{ap|{ap|{s
... [9036 more characters]
```

### FINALIST R_5b2eb732ac8b

*8,907 characters*

```text
#
  Y
    TH: Stream'.WSeq.head_terminates_of_head_tail_terminates
    FL: Mathlib/Data/Seq/WSeq.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [Computation.exists_of_mem_bind]
    L: [Mathlib/Data/Seq/WSeq.lean::Stream'.WSeq.head_terminates_of_head_tail_terminates::2:before:local:f7]
Σ₀
  □ bm0
    ⊢: Computation.Terminates [up(u)] sym Option [up(u)] sym Prod [up(u) up(u)] sym bf0 fv ap Stream'.WSeq [up(u)] sym bf0 fv ap ap ap ap Stream'.WSeq.destruct [up(u)] sym bf0 fv ap bf4 fv ap ap
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7]
  A bf0
    tg: sort
  A bf4
    tg: Stream'.WSeq
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u)) sort
  D bf1
    b: IMPLICIT
    d: cdecl
    ∈: us(up(v)) sort
  D bf2
    b: IMPLICIT
    d: cdecl
    ∈: us(up(w)) sort
  D bf3
    b: EXPLICIT
    d: cdecl
    ∈: EXPLICIT Stream'.WSeq [up(u)] sym bf0 fv ap INSTANCE_IMPLICIT Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv ap ap Stream'.WSeq.head [up(u)] sym bf0 fv ap Stream'.WSeq.tail [up(u)] sym bf0 fv ap 0 bv ap ap ap Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv ap ap Stream'.WSeq.head [up(u)] sym bf0 fv ap 1 
... [7707 more characters]
```

### FINALIST R_000441b08de4

*8,880 characters*

```text
mta
  smy ;; thm: Stream'.WSeq.head_terminates_of_head_tail_terminates ;; fl: Mathlib/Data/Seq/WSeq.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u)) sort
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(v)) sort
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(w)) sort
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: EXPLICIT Stream'.WSeq [up(u)] sym bf0 fv ap INSTANCE_IMPLICIT Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv ap ap Stream'.WSeq.head [up(u)] sym bf0 fv ap Stream'.WSeq.tail [up(u)] sym bf0 fv ap 0 bv ap ap ap Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv ap ap Stream'.WSeq.head [up(u)] sym bf0 fv ap 1 bv ap ap pi pi
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Stream'.WSeq [up(u)] sym bf0 fv ap
  dc bf5 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv ap ap Stream'.WSeq.head [up(u)] sym bf0 fv ap Stream'.WSeq.tail [up(u)] sym bf0 fv ap bf4 fv ap ap ap
  dc bf6 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Option [up(u)] sym Prod [up(u) up(u)] sym bf0 fv ap Stream'.WSeq [up(u)] sym bf0 fv ap ap ap
  dc bf7 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Membership.mem [up(u) up(u)] sym Option 
... [7680 more characters]
```

### FINALIST R_01d4e489af53

*9,835 characters*

```text
(mta
  (smy (thm Stream'.WSeq.head_terminates_of_head_tail_terminates) (fl Mathlib/Data/Seq/WSeq.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u)))))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(v)))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(w)))))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (sym Stream'.WSeq [up(u)]) (fv f0)) (pi INSTANCE_IMPLICIT (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv f0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv f0)) (ap (ap (sym Stream'.WSeq.tail [up(u)]) (fv f0)) (bv 0)))) (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv f0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv f0)) (bv 1)))))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (ap (sym Stream'.WSeq [up(u)]) (fv f0))))
  (dc f5 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv f0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv f0)) (ap (ap (sym Stream'.WSeq.tail [up(u)]) (fv f0)) (fv f4))))))
  (dc f6 (br EXPLICIT) (dr cdecl) (ty (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv f0)) (ap (sym Stream'.WSeq [up(u)]) (fv f0))))))
  (dc f7 
... [8635 more characters]
```

### FINALIST R_101e806690b0

*19,799 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (ap (ap (sym Membership.mem [up(u) up(u)]) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))) (ap (sym Computation [up(u)]) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0)))))) (ap (sym Computation.instMembership [up(u)]) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0)))))) (fv bf6)) (ap (ap (ap (ap (ap (ap (sym Bind.bind [up(u) up(u)]) (sym Computation [up(u)])) (sym Computation.instBind [up(u)])) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))) (ap (ap (ap (ap (ap (ap (sym Functor.map [up(u) up(u)]) (sym Computation [up(u)])) (ap (ap (sym Applicative.toFunctor [up(u) up(u)]) (sym Computation [up(u)])) (ap (ap (sym Alternative.toApplicative [up(u) up(u)]) (sym Computation [up(u)])) (sym Computation.instAlternativeComputation [up(u)])))) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))) (ap (sym Stream'.WSeq [u
... [18599 more characters]
```

### FINALIST R_28b291b5ebe6

*10,746 characters*

```text
meta
  summary ;; theorem-> Stream'.WSeq.head_terminates_of_head_tail_terminates ;; file-> Mathlib/Data/Seq/WSeq.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u)) sort
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(v)) sort
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(w)) sort
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT Stream'.WSeq [up(u)] sym f0 fv ap INSTANCE_IMPLICIT Computation.Terminates [up(u)] sym Option [up(u)] sym f0 fv ap ap Stream'.WSeq.head [up(u)] sym f0 fv ap Stream'.WSeq.tail [up(u)] sym f0 fv ap 0 bv ap ap ap Computation.Terminates [up(u)] sym Option [up(u)] sym f0 fv ap ap Stream'.WSeq.head [up(u)] sym f0 fv ap 1 bv ap ap pi pi
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Stream'.WSeq [up(u)] sym f0 fv ap
  decl f5 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> Computation.Terminates [up(u)] sym Option [up(u)] sym f0 fv ap ap Stream'.WSeq.head [up(u)] sym f0 fv ap Stream'.WSeq.tail [up(u)] sym f0 fv ap f4 fv ap ap ap
  decl f6 ;; binder_role-> EXPLICIT ;
... [9546 more characters]
```

## Example 6 — `Mathlib/LinearAlgebra/Dimension/Localization.lean::aleph0_le_rank_of_isEmpty_oreSet::4`

**Shape:** 1 goal(s), 9 local declaration(s), 2 external premise(s). Domain `LinearAlgebra`.

### SEED_LEAN_LIKE

*27,377 characters*

```text
#
  Y
    TH: aleph0_le_rank_of_isEmpty_oreSet
    FL: Mathlib/LinearAlgebra/Dimension/Localization.lean
Σ₀
  D R~bf0
    n: R
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1996~bf1
    n: inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1996
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(Ring,[up(u_1)]),fv(R~bf0))
  D inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1999~bf2
    n: inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1999
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(ap(sym(IsDomain,[up(u_1)]),fv(R~bf0)),ap(ap(sym(Ring.toSemiring,[up(u_1)]),fv(R~bf0)),fv(inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1996~bf1)))
  D S~bf3
    n: S
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(sym(Submonoid,[up(u_1)]),fv(R~bf0)),ap(ap(sym(MulZeroOneClass.toMulOneClass,[up(u_1)]),fv(R~bf0)),ap(ap(sym(NonAssocSemiring.toMulZeroOneClass,[up(u_1)]),fv(R~bf0)),ap(ap(sym(Semiring.toNonAssocSemiring,[up(u_1)]),fv(R~bf0)),ap(ap(sym(Ring.toSemiring,[up(u_1)]),fv(R~bf0)),fv(inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1996~bf1))))))
  D aleph0_le_rank_of_isEmpty_oreSet~bf4

... [26177 more characters]
```

### SEED_PRIOR_HML

*24,167 characters*

```text
meta
  summary
    theorem: aleph0_le_rank_of_isEmpty_oreSet
    file: Mathlib/LinearAlgebra/Dimension/Localization.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Ring [up(u_1)]) (fv bf0))
  decl bf2
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym IsDomain [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1)))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym Submonoid [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (ap (sym IsEmpty [us(up(u_1))]) (ap (ap (ap (sym OreLocalization.OreSet [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]
... [22967 more characters]
```

### SEED_STRUCTURED_ENGLISH

*28,940 characters*

```text
In meta:
  summary has theorem is aleph0_le_rank_of_isEmpty_oreSet; and file is Mathlib/LinearAlgebra/Dimension/Localization.lean .
In state_before:
  decl R~bf0 has display is R; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1996~bf1 has display is inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1996; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(Ring,[up(u_1)]),fv(R~bf0)) .
  decl inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1999~bf2 has display is inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1999; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(IsDomain,[up(u_1)]),fv(R~bf0)),ap(ap(sym(Ring.toSemiring,[up(u_1)]),fv(R~bf0)),fv(inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1996~bf1))) .
  decl S~bf3 has display is S; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(Submonoid,[up(u_1)]),fv(R~bf0)),ap(ap(sym(MulZeroOneClass.toMulOneClass,[up(u_1)]),fv(R~bf0)),ap(ap(sym(NonAssocSemiring.toMulZeroOneClass,[up(u_1)
... [27740 more characters]
```

### SEED_TYPED_AST

*23,414 characters*

```text
mta
  - smy
    thm: aleph0_le_rank_of_isEmpty_oreSet
    fl: Mathlib/LinearAlgebra/Dimension/Localization.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Ring,[up{u_1}]},{fv|bf0}}
  - dc bf2
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|IsDomain,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Ring.toSemiring,[up{u_1}]},{fv|bf0}},{fv|bf1}}}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|Submonoid,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MulZeroOneClass.toMulOneClass,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|NonAssocSemiring.toMulZeroOneClass,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Semiring.toNonAssocSemiring,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Ring.toSemiring,[up{u_1}]},{fv|bf0}},{fv|bf1}}}}}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{ap|{sym|IsEmpty,[us{up{u_1}}]},{ap|{ap|{ap|{sym|OreLocalization.OreSet,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MonoidWithZero.toMonoid,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Semiring.toMonoidWithZero,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Ring.toSemiring,[up{u_1}]},{fv|bf0}},{fv|bf1}}}}},{ap|{ap|{sym|nonZeroDivisors,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Semiri
... [22214 more characters]
```

### FINALIST R_5b2eb732ac8b

*20,265 characters*

```text
#
  Y
    TH: aleph0_le_rank_of_isEmpty_oreSet
    FL: Mathlib/LinearAlgebra/Dimension/Localization.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [Fin,LinearIndependent]
    L: [Mathlib/LinearAlgebra/Dimension/Localization.lean::aleph0_le_rank_of_isEmpty_oreSet::4:before:local:f0,Mathlib/LinearAlgebra/Dimension/Localization.lean::aleph0_le_rank_of_isEmpty_oreSet::4:before:local:f1,Mathlib/LinearAlgebra/Dimension/Localization.lean::aleph0_le_rank_of_isEmpty_oreSet::4:before:local:f5,Mathlib/LinearAlgebra/Dimension/Localization.lean::aleph0_le_rank_of_isEmpty_oreSet::4:before:local:f6,Mathlib/LinearAlgebra/Dimension/Localization.lean::aleph0_le_rank_of_isEmpty_oreSet::4:before:local:f8]
Σ₀
  □ bm2
    ⊢: LE.le [us(um(u0))] sym Cardinal [um(u0)] sym ap Cardinal.instLE [um(u0)] sym ap Nat.cast [us(um(u0))] sym Cardinal [um(u0)] sym ap Cardinal.instNatCast [um(u0)] sym ap bf8 fv ap ap bm0 mv ap
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8]
  A bf8
    tg: metavariable_reference
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_1)) sort
  D bf1
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: Ring [up(u_1)] sym bf0 fv ap
  D b
... [19065 more characters]
```

### FINALIST R_000441b08de4

*20,345 characters*

```text
mta
  smy ;; thm: aleph0_le_rank_of_isEmpty_oreSet ;; fl: Mathlib/LinearAlgebra/Dimension/Localization.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Ring [up(u_1)] sym bf0 fv ap
  dc bf2 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: IsDomain [up(u_1)] sym bf0 fv ap Ring.toSemiring [up(u_1)] sym bf0 fv ap bf1 fv ap ap
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Submonoid [up(u_1)] sym bf0 fv ap MulZeroOneClass.toMulOneClass [up(u_1)] sym bf0 fv ap NonAssocSemiring.toMulZeroOneClass [up(u_1)] sym bf0 fv ap Semiring.toNonAssocSemiring [up(u_1)] sym bf0 fv ap Ring.toSemiring [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap ap
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: EXPLICIT IsEmpty [us(up(u_1))] sym OreLocalization.OreSet [up(u_1)] sym bf0 fv ap MonoidWithZero.toMonoid [up(u_1)] sym bf0 fv ap Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv ap Ring.toSemiring [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap nonZeroDivisors [up(u_1)] sym bf0 fv ap Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv ap Ring.toSemiring [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap ap LE.le [us(up(u_1))] sym Cardinal [up(u_1)] sym ap Cardinal.ins
... [19145 more characters]
```

### FINALIST R_01d4e489af53

*22,615 characters*

```text
(mta
  (smy (thm aleph0_le_rank_of_isEmpty_oreSet) (fl Mathlib/LinearAlgebra/Dimension/Localization.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Ring [up(u_1)]) (fv f0))))
  (dc f2 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym IsDomain [up(u_1)]) (fv f0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv f0)) (fv f1)))))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (ap (ap (sym Submonoid [up(u_1)]) (fv f0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv f0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv f0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv f0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv f0)) (fv f1))))))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (sym IsEmpty [us(up(u_1))]) (ap (ap (ap (sym OreLocalization.OreSet [up(u_1)]) (fv f0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv f0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv f0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv f0)) (fv f1))))) (ap (ap (sym nonZeroDivisors [up(u_1)]) (fv f0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv f0)) (ap (ap (sym Ring.toSemiring [
... [21415 more characters]
```

### FINALIST R_101e806690b0

*65,715 characters*

```text
$
  A $a0
    t-> (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (sym Subtype [us(up(u_1))]) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (ap (sym Submonoid [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))))) (ap (ap (ap (sym SetLike.instMembership [up(u_1) up(u_1)]) (ap (ap (sym Submonoid [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))))) (fv bf0)) (ap (ap (sym Submonoid.instSetLike [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1)))))))) (bv 0)) (ap (ap
... [64515 more characters]
```

### FINALIST R_28b291b5ebe6

*22,344 characters*

```text
meta
  summary ;; theorem-> aleph0_le_rank_of_isEmpty_oreSet ;; file-> Mathlib/LinearAlgebra/Dimension/Localization.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> Ring [up(u_1)] sym f0 fv ap
  decl f2 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> IsDomain [up(u_1)] sym f0 fv ap Ring.toSemiring [up(u_1)] sym f0 fv ap f1 fv ap ap
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Submonoid [up(u_1)] sym f0 fv ap MulZeroOneClass.toMulOneClass [up(u_1)] sym f0 fv ap NonAssocSemiring.toMulZeroOneClass [up(u_1)] sym f0 fv ap Semiring.toNonAssocSemiring [up(u_1)] sym f0 fv ap Ring.toSemiring [up(u_1)] sym f0 fv ap f1 fv ap ap ap ap ap
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT IsEmpty [us(up(u_1))] sym OreLocalization.OreSet [up(u_1)] sym f0 fv ap MonoidWithZero.toMonoid [up(u_1)] sym f0 fv ap Semiring.toMonoidWithZero [up(u_1)] sym f0 fv ap Ring.toSemiring [up(u_1)] sym f0 fv ap f1 fv ap ap ap ap nonZeroDivisors [up(u_1)] sym f0 fv ap Semiring.toMonoidWithZ
... [21144 more characters]
```

## Example 7 — `Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean::MeasureTheory.lintegral_rpow_eq_lintegral_m`

**Shape:** 1 goal(s), 10 local declaration(s), 3 external premise(s). Domain `Analysis`.

### SEED_LEAN_LIKE

*28,225 characters*

```text
#
  Y
    TH: MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul
    FL: Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
Σ₀
  D α~bf0
    n: α
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1
    n: inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(MeasurableSpace,[up(u_1)]),fv(α~bf0))
  D f~bf2
    n: f
    b: IMPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,fv(α~bf0),sym(Real,[]))
  D μ~bf3
    n: μ
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(sym(MeasureTheory.Measure,[up(u_1)]),fv(α~bf0)),fv(inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1))
  D f_nn~bf4
    n: f_nn
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(ap(ap(ap(ap(sym(Filter.EventuallyLE,[up(u_1) u0]),fv(α~bf0)),sym(Real,[])),sym(Real.instLE,[])),ap(ap(ap(ap(ap(sym(MeasureTheory.ae,[up(u_1) up(u_1)]),fv(α~bf0)),ap(ap(sym(MeasureTheory.Measure,[up(u_1)]),fv(α~bf0)),fv(inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1))),ap(ap(sym(MeasureTheory.Measure.instFunLike,[up(u_1)]),fv(α~bf0)),fv(inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1))
... [27025 more characters]
```

### SEED_PRIOR_HML

*28,538 characters*

```text
meta
  summary
    theorem: MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul
    file: Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym MeasurableSpace [up(u_1)]) (fv bf0))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (fv bf0) (sym Real []))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym MeasureTheory.Measure [up(u_1)]) (fv bf0)) (fv bf1))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (ap (ap (sym Filter.EventuallyLE [up(u_1) u0]) (fv bf0)) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (ap (sym MeasureTheory.ae [up(u_1) up(u_1)]) (fv bf0)) (ap (ap (sym MeasureTheory.Measure [up(u_1)]) (fv bf0)) (fv bf1))) (ap (ap (sym MeasureTheory.Measure.instFunLike [up(u_1)]) (fv bf0)) (fv bf1))) (ap (ap (sym MeasureTheory.Measure.instOuterMeasureClass [up(u_1)]) (fv bf0)) (fv bf1))) (fv bf3))) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (pi EXPLICIT (fv bf0) (s
... [27338 more characters]
```

### SEED_STRUCTURED_ENGLISH

*30,546 characters*

```text
In meta:
  summary has theorem is MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul; and file is Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean .
In state_before:
  decl α~bf0 has display is α; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1 has display is inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(MeasurableSpace,[up(u_1)]),fv(α~bf0)) .
  decl f~bf2 has display is f; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,fv(α~bf0),sym(Real,[])) .
  decl μ~bf3 has display is μ; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(MeasureTheory.Measure,[up(u_1)]),fv(α~bf0)),fv(inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1)) .
  decl f_nn~bf4 has display is f_nn; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(ap(ap(ap(sym(Filter.EventuallyLE,[up(u_1) u0]),fv(α~bf0)),sym(Real,[])),sym(Real.instLE,[])),ap(ap(ap(ap(ap(sym(MeasureTheory.ae,[up(u
... [29346 more characters]
```

### SEED_TYPED_AST

*27,470 characters*

```text
mta
  - smy
    thm: MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul
    fl: Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|MeasurableSpace,[up{u_1}]},{fv|bf0}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{fv|bf0},{sym|Real,[]}}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|MeasureTheory.Measure,[up{u_1}]},{fv|bf0}},{fv|bf1}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{ap|{ap|{sym|Filter.EventuallyLE,[up{u_1} u0]},{fv|bf0}},{sym|Real,[]}},{sym|Real.instLE,[]}},{ap|{ap|{ap|{ap|{ap|{sym|MeasureTheory.ae,[up{u_1} up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MeasureTheory.Measure,[up{u_1}]},{fv|bf0}},{fv|bf1}}},{ap|{ap|{sym|MeasureTheory.Measure.instFunLike,[up{u_1}]},{fv|bf0}},{fv|bf1}}},{ap|{ap|{sym|MeasureTheory.Measure.instOuterMeasureClass,[up{u_1}]},{fv|bf0}},{fv|bf1}}},{fv|bf3}}},{ap|{ap|{ap|{sym|OfNat.ofNat,[up{u_1}]},{pi|EXPLICIT,{fv|bf0},{sym|Real,[]}}},{lit|NAT,0}},{ap|{ap|{sym|Zero.toOfNat0,[up{u_1}]},{pi|EXPLICIT,{fv|bf0},{sym|Real,[]}}},{ap|{ap|{ap|{sym|Pi.instZero,[up{u_1} u0]
... [26270 more characters]
```

### FINALIST R_5b2eb732ac8b

*23,675 characters*

```text
#
  Y
    TH: MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul
    FL: Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [Or.inl,Real.zero_rpow,integral_rpow]
    L: [Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean::MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul::1:before:local:f0,Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean::MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul::1:before:local:f1,Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean::MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul::1:before:local:f2,Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean::MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul::1:before:local:f3,Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean::MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul::1:before:local:f6,Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean::MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul::1:before:local:f7,Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean::MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul::1:before:local:f9]
Σ₀
  □ bm12
    ⊢: Eq [us(u0)] sym EN
... [22475 more characters]
```

### FINALIST R_000441b08de4

*23,780 characters*

```text
mta
  smy ;; thm: MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul ;; fl: Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: MeasurableSpace [up(u_1)] sym bf0 fv ap
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: EXPLICIT bf0 fv Real [] sym pi
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: MeasureTheory.Measure [up(u_1)] sym bf0 fv ap bf1 fv ap
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Filter.EventuallyLE [up(u_1) u0] sym bf0 fv ap Real [] sym ap Real.instLE [] sym ap MeasureTheory.ae [up(u_1) up(u_1)] sym bf0 fv ap MeasureTheory.Measure [up(u_1)] sym bf0 fv ap bf1 fv ap ap MeasureTheory.Measure.instFunLike [up(u_1)] sym bf0 fv ap bf1 fv ap ap MeasureTheory.Measure.instOuterMeasureClass [up(u_1)] sym bf0 fv ap bf1 fv ap ap bf3 fv ap ap OfNat.ofNat [up(u_1)] sym EXPLICIT bf0 fv Real [] sym pi ap NAT 0 lit ap Zero.toOfNat0 [up(u_1)] sym EXPLICIT bf0 fv Real [] sym pi ap Pi.instZero [up(u_1) u0] sym bf0 fv ap EXPLICIT bf0 fv Real [] sym lam ap EXPLICIT bf0 fv Real.instZero [] sym lam ap ap ap ap bf2 fv ap
  dc bf5 ;; br: EXPLICIT ;; dr: cdecl ;; ty: AEMeasurable [
... [22580 more characters]
```

### FINALIST R_01d4e489af53

*26,555 characters*

```text
(mta
  (smy (thm MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul) (fl Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym MeasurableSpace [up(u_1)]) (fv f0))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (fv f0) (sym Real []))))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (ap (ap (sym MeasureTheory.Measure [up(u_1)]) (fv f0)) (fv f1))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (ap (ap (sym Filter.EventuallyLE [up(u_1) u0]) (fv f0)) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (ap (sym MeasureTheory.ae [up(u_1) up(u_1)]) (fv f0)) (ap (ap (sym MeasureTheory.Measure [up(u_1)]) (fv f0)) (fv f1))) (ap (ap (sym MeasureTheory.Measure.instFunLike [up(u_1)]) (fv f0)) (fv f1))) (ap (ap (sym MeasureTheory.Measure.instOuterMeasureClass [up(u_1)]) (fv f0)) (fv f1))) (fv f3))) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (pi EXPLICIT (fv f0) (sym Real []))) (lit 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (pi EXPLICIT (fv f0) (sym Real []))) (ap (ap (ap (sym Pi.instZero [up(u_1) u0]) (fv f0)) (lam EXPLICIT (fv f0) (sym Real []))) (lam EXPLICIT (fv f0) (s
... [25355 more characters]
```

### FINALIST R_101e806690b0

*41,482 characters*

```text
$
  A $a0
    t-> (ann (ap (ap (ap (sym Eq [us(u0)]) (sym ENNReal [])) (ap (ap (ap (ap (sym MeasureTheory.lintegral [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf3)) (lam EXPLICIT (fv bf0) (ap (sym ENNReal.ofReal []) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (ap (sym instHPow [u0 u0]) (sym Real [])) (sym Real [])) (sym Real.instPow []))) (ap (fv bf2) (bv 0))) (fv bf6)))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym ENNReal [])) (sym ENNReal [])) (sym ENNReal [])) (ap (ap (sym instHMul [u0]) (sym ENNReal [])) (ap (ap (sym CanonicallyOrderedCommSemiring.toMul [u0]) (sym ENNReal [])) (sym ENNReal.instCanonicallyOrderedCommSemiring [])))) (ap (sym ENNReal.ofReal []) (fv bf6))) (ap (ap (ap (ap (sym MeasureTheory.lintegral [u0]) (sym Real [])) (ap (ap (sym MeasureTheory.MeasureSpace.toMeasurableSpace [u0]) (sym Real [])) (sym Real.measureSpace []))) (ap (ap (ap (ap (sym MeasureTheory.Measure.restrict [u0]) (sym Real [])) (ap (ap (sym MeasureTheory.MeasureSpace.toMeasurableSpace [u0]) (sym Real [])) (sym Real.measureSpace []))) (ap (ap (sym MeasureTheory.MeasureSpace.volume [u0]) (sym Real [])) (sym Real.measureSpace []))) 
... [40282 more characters]
```

### FINALIST R_28b291b5ebe6

*27,018 characters*

```text
meta
  summary ;; theorem-> MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul ;; file-> Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> MeasurableSpace [up(u_1)] sym f0 fv ap
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT f0 fv Real [] sym pi
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> MeasureTheory.Measure [up(u_1)] sym f0 fv ap f1 fv ap
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Filter.EventuallyLE [up(u_1) u0] sym f0 fv ap Real [] sym ap Real.instLE [] sym ap MeasureTheory.ae [up(u_1) up(u_1)] sym f0 fv ap MeasureTheory.Measure [up(u_1)] sym f0 fv ap f1 fv ap ap MeasureTheory.Measure.instFunLike [up(u_1)] sym f0 fv ap f1 fv ap ap MeasureTheory.Measure.instOuterMeasureClass [up(u_1)] sym f0 fv ap f1 fv ap ap f3 fv ap ap OfNat.ofNat [up(u_1)] sym EXPLICIT f0 fv Real [] sym pi ap NAT 0 lit ap Zero.toOfNat0 [up(u_1)] sym EXPLICIT f0 fv Real [] sym pi ap Pi.instZero [up(u_1) u0] sym f0 fv ap EXPLI
... [25818 more characters]
```

## Example 8 — `Mathlib/RingTheory/UniqueFactorizationDomain.lean::WfDvdMonoid.max_power_factor'::2`

**Shape:** 1 goal(s), 10 local declaration(s), 0 external premise(s). Domain `RingTheory`.

### SEED_LEAN_LIKE

*16,442 characters*

```text
#
  Y
    TH: WfDvdMonoid.max_power_factor'
    FL: Mathlib/RingTheory/UniqueFactorizationDomain.lean
Σ₀
  D α~bf0
    n: α
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D max_power_factor'~bf1
    n: max_power_factor'
    b: EXPLICIT
    d: cdecl
    ∈: pi(INSTANCE_IMPLICIT,ap(sym(CommMonoidWithZero,[up(u_1)]),fv(α~bf0)),pi(INSTANCE_IMPLICIT,ap(ap(sym(WfDvdMonoid,[up(u_1)]),fv(α~bf0)),bv(0)),pi(IMPLICIT,fv(α~bf0),pi(IMPLICIT,fv(α~bf0),pi(EXPLICIT,ap(ap(ap(sym(Ne,[us(up(u_1))]),fv(α~bf0)),bv(1)),ap(ap(ap(sym(OfNat.ofNat,[up(u_1)]),fv(α~bf0)),lit(NAT,0)),ap(ap(sym(Zero.toOfNat0,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toZero,[up(u_1)]),fv(α~bf0)),bv(3))))),pi(EXPLICIT,ap(sym(Not,[]),ap(ap(ap(sym(IsUnit,[up(u_1)]),fv(α~bf0)),ap(ap(sym(MonoidWithZero.toMonoid,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toMonoidWithZero,[up(u_1)]),fv(α~bf0)),bv(4)))),bv(1))),ap(ap(sym(Exists,[us(u0)]),sym(Nat,[])),lam(EXPLICIT,sym(Nat,[]),ap(ap(sym(Exists,[us(up(u_1))]),fv(α~bf0)),lam(EXPLICIT,fv(α~bf0),ap(ap(sym(And,[]),ap(sym(Not,[]),ap(ap(ap(ap(sym(Dvd.dvd,[up(u_1)]),fv(α~bf0)),ap(ap(sym(semigroupDvd,[up(u_1)]),fv(α~bf0)),ap(ap(sym(SemigroupWithZero.toSemigroup,[up(u_1)]),
... [15242 more characters]
```

### SEED_PRIOR_HML

*15,271 characters*

```text
meta
  summary
    theorem: WfDvdMonoid.max_power_factor'
    file: Mathlib/RingTheory/UniqueFactorizationDomain.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi INSTANCE_IMPLICIT (ap (sym CommMonoidWithZero [up(u_1)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym WfDvdMonoid [up(u_1)]) (fv bf0)) (bv 0)) (pi IMPLICIT (fv bf0) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (sym Ne [us(up(u_1))]) (fv bf0)) (bv 1)) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (fv bf0)) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toZero [up(u_1)]) (fv bf0)) (bv 3))))) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (sym IsUnit [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 4)))) (bv 1))) (ap (ap (sym Exists [us(u0)]) (sym Nat [])) (lam EXPLICIT (sym Nat []) (ap (ap (sym Exists [us(up(u_1))]) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (sym And []) (ap (sym Not []) (ap (ap (ap (ap (sym Dvd.dvd [up(u_1)]) (fv bf0)) (ap (ap (sym
... [14071 more characters]
```

### SEED_STRUCTURED_ENGLISH

*17,839 characters*

```text
In meta:
  summary has theorem is WfDvdMonoid.max_power_factor'; and file is Mathlib/RingTheory/UniqueFactorizationDomain.lean .
In state_before:
  decl α~bf0 has display is α; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl max_power_factor'~bf1 has display is max_power_factor'; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(INSTANCE_IMPLICIT,ap(sym(CommMonoidWithZero,[up(u_1)]),fv(α~bf0)),pi(INSTANCE_IMPLICIT,ap(ap(sym(WfDvdMonoid,[up(u_1)]),fv(α~bf0)),bv(0)),pi(IMPLICIT,fv(α~bf0),pi(IMPLICIT,fv(α~bf0),pi(EXPLICIT,ap(ap(ap(sym(Ne,[us(up(u_1))]),fv(α~bf0)),bv(1)),ap(ap(ap(sym(OfNat.ofNat,[up(u_1)]),fv(α~bf0)),lit(NAT,0)),ap(ap(sym(Zero.toOfNat0,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toZero,[up(u_1)]),fv(α~bf0)),bv(3))))),pi(EXPLICIT,ap(sym(Not,[]),ap(ap(ap(sym(IsUnit,[up(u_1)]),fv(α~bf0)),ap(ap(sym(MonoidWithZero.toMonoid,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toMonoidWithZero,[up(u_1)]),fv(α~bf0)),bv(4)))),bv(1))),ap(ap(sym(Exists,[us(u0)]),sym(Nat,[])),lam(EXPLICIT,sym(Nat,[]),ap(ap(sym(Exists,[us(up(u_1))]),fv(α~bf0)),lam(EXPLICIT,fv(α~bf0),ap(ap(sym(And,[]),ap(sym(Not,[]),ap(
... [16639 more characters]
```

### SEED_TYPED_AST

*14,573 characters*

```text
mta
  - smy
    thm: WfDvdMonoid.max_power_factor'
    fl: Mathlib/RingTheory/UniqueFactorizationDomain.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: EXPLICIT
    dr: cdecl
    ty: {pi|INSTANCE_IMPLICIT,{ap|{sym|CommMonoidWithZero,[up{u_1}]},{fv|bf0}},{pi|INSTANCE_IMPLICIT,{ap|{ap|{sym|WfDvdMonoid,[up{u_1}]},{fv|bf0}},{bv|0}},{pi|IMPLICIT,{fv|bf0},{pi|IMPLICIT,{fv|bf0},{pi|EXPLICIT,{ap|{ap|{ap|{sym|Ne,[us{up{u_1}}]},{fv|bf0}},{bv|1}},{ap|{ap|{ap|{sym|OfNat.ofNat,[up{u_1}]},{fv|bf0}},{lit|NAT,0}},{ap|{ap|{sym|Zero.toOfNat0,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|CommMonoidWithZero.toZero,[up{u_1}]},{fv|bf0}},{bv|3}}}}},{pi|EXPLICIT,{ap|{sym|Not,[]},{ap|{ap|{ap|{sym|IsUnit,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MonoidWithZero.toMonoid,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|CommMonoidWithZero.toMonoidWithZero,[up{u_1}]},{fv|bf0}},{bv|4}}}},{bv|1}}},{ap|{ap|{sym|Exists,[us{u0}]},{sym|Nat,[]}},{lam|EXPLICIT,{sym|Nat,[]},{ap|{ap|{sym|Exists,[us{up{u_1}}]},{fv|bf0}},{lam|EXPLICIT,{fv|bf0},{ap|{ap|{sym|And,[]},{ap|{sym|Not,[]},{ap|{ap|{ap|{ap|{sym|Dvd.dvd,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|semigroupDvd,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|SemigroupWithZero.toS
... [13373 more characters]
```

### FINALIST R_5b2eb732ac8b

*12,326 characters*

```text
#
  Y
    TH: WfDvdMonoid.max_power_factor'
    FL: Mathlib/RingTheory/UniqueFactorizationDomain.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: []
    L: []
Σ₀
  □ bm1
    ⊢: bm0 mv
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9]
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_1)) sort
  D bf1
    b: EXPLICIT
    d: cdecl
    ∈: INSTANCE_IMPLICIT CommMonoidWithZero [up(u_1)] sym bf0 fv ap INSTANCE_IMPLICIT WfDvdMonoid [up(u_1)] sym bf0 fv ap 0 bv ap IMPLICIT bf0 fv IMPLICIT bf0 fv EXPLICIT Ne [us(up(u_1))] sym bf0 fv ap 1 bv ap OfNat.ofNat [up(u_1)] sym bf0 fv ap NAT 0 lit ap Zero.toOfNat0 [up(u_1)] sym bf0 fv ap CommMonoidWithZero.toZero [up(u_1)] sym bf0 fv ap 3 bv ap ap ap ap EXPLICIT Not [] sym IsUnit [up(u_1)] sym bf0 fv ap MonoidWithZero.toMonoid [up(u_1)] sym bf0 fv ap CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym bf0 fv ap 4 bv ap ap ap 1 bv ap ap Exists [us(u0)] sym Nat [] sym ap EXPLICIT Nat [] sym Exists [us(up(u_1))] sym bf0 fv ap EXPLICIT bf0 fv And [] sym Not [] sym Dvd.dvd [up(u_1)] sym bf0 fv ap semigroupDvd [up(u_1)] sym bf0 fv ap SemigroupWithZero.toSemigroup [up(u_1)] sym bf0 fv ap MonoidWit
... [11126 more characters]
```

### FINALIST R_000441b08de4

*12,365 characters*

```text
mta
  smy ;; thm: WfDvdMonoid.max_power_factor' ;; fl: Mathlib/RingTheory/UniqueFactorizationDomain.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: EXPLICIT ;; dr: cdecl ;; ty: INSTANCE_IMPLICIT CommMonoidWithZero [up(u_1)] sym bf0 fv ap INSTANCE_IMPLICIT WfDvdMonoid [up(u_1)] sym bf0 fv ap 0 bv ap IMPLICIT bf0 fv IMPLICIT bf0 fv EXPLICIT Ne [us(up(u_1))] sym bf0 fv ap 1 bv ap OfNat.ofNat [up(u_1)] sym bf0 fv ap NAT 0 lit ap Zero.toOfNat0 [up(u_1)] sym bf0 fv ap CommMonoidWithZero.toZero [up(u_1)] sym bf0 fv ap 3 bv ap ap ap ap EXPLICIT Not [] sym IsUnit [up(u_1)] sym bf0 fv ap MonoidWithZero.toMonoid [up(u_1)] sym bf0 fv ap CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym bf0 fv ap 4 bv ap ap ap 1 bv ap ap Exists [us(u0)] sym Nat [] sym ap EXPLICIT Nat [] sym Exists [us(up(u_1))] sym bf0 fv ap EXPLICIT bf0 fv And [] sym Not [] sym Dvd.dvd [up(u_1)] sym bf0 fv ap semigroupDvd [up(u_1)] sym bf0 fv ap SemigroupWithZero.toSemigroup [up(u_1)] sym bf0 fv ap MonoidWithZero.toSemigroupWithZero [up(u_1)] sym bf0 fv ap CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym bf0 fv ap 7 bv ap ap ap ap ap 4 bv ap 0 bv ap ap ap Eq [us(up(u_1))] sym bf0 fv ap 5 
... [11165 more characters]
```

### FINALIST R_01d4e489af53

*13,989 characters*

```text
(mta
  (smy (thm WfDvdMonoid.max_power_factor') (fl Mathlib/RingTheory/UniqueFactorizationDomain.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br EXPLICIT) (dr cdecl) (ty (pi INSTANCE_IMPLICIT (ap (sym CommMonoidWithZero [up(u_1)]) (fv f0)) (pi INSTANCE_IMPLICIT (ap (ap (sym WfDvdMonoid [up(u_1)]) (fv f0)) (bv 0)) (pi IMPLICIT (fv f0) (pi IMPLICIT (fv f0) (pi EXPLICIT (ap (ap (ap (sym Ne [us(up(u_1))]) (fv f0)) (bv 1)) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (fv f0)) (lit 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (fv f0)) (ap (ap (sym CommMonoidWithZero.toZero [up(u_1)]) (fv f0)) (bv 3))))) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (sym IsUnit [up(u_1)]) (fv f0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv f0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv f0)) (bv 4)))) (bv 1))) (ap (ap (sym Exists [us(u0)]) (sym Nat [])) (lam EXPLICIT (sym Nat []) (ap (ap (sym Exists [us(up(u_1))]) (fv f0)) (lam EXPLICIT (fv f0) (ap (ap (sym And []) (ap (sym Not []) (ap (ap (ap (ap (sym Dvd.dvd [up(u_1)]) (fv f0)) (ap (ap (sym semigroupDvd [up(u_1)]) (fv f0)) (ap (ap (sym SemigroupWithZero.toSemigroup [up(u_1)]) (fv f0)) (ap (ap (sym M
... [12789 more characters]
```

### FINALIST R_101e806690b0

*48,325 characters*

```text
$
  A $a0
    t-> (pi INSTANCE_IMPLICIT (ap (sym CommMonoidWithZero [up(u_1)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym WfDvdMonoid [up(u_1)]) (fv bf0)) (bv 0)) (pi IMPLICIT (fv bf0) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (sym Ne [us(up(u_1))]) (fv bf0)) (bv 1)) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (fv bf0)) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toZero [up(u_1)]) (fv bf0)) (bv 3))))) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (sym IsUnit [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 4)))) (bv 1))) (ap (ap (sym Exists [us(u0)]) (sym Nat [])) (lam EXPLICIT (sym Nat []) (ap (ap (sym Exists [us(up(u_1))]) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (sym And []) (ap (sym Not []) (ap (ap (ap (ap (sym Dvd.dvd [up(u_1)]) (fv bf0)) (ap (ap (sym semigroupDvd [up(u_1)]) (fv bf0)) (ap (ap (sym SemigroupWithZero.toSemigroup [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toSemigroupWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 7)))))) (bv 4)) (bv 0)))) (ap (ap (ap (s
... [47125 more characters]
```

### FINALIST R_28b291b5ebe6

*14,917 characters*

```text
meta
  summary ;; theorem-> WfDvdMonoid.max_power_factor' ;; file-> Mathlib/RingTheory/UniqueFactorizationDomain.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> INSTANCE_IMPLICIT CommMonoidWithZero [up(u_1)] sym f0 fv ap INSTANCE_IMPLICIT WfDvdMonoid [up(u_1)] sym f0 fv ap 0 bv ap IMPLICIT f0 fv IMPLICIT f0 fv EXPLICIT Ne [us(up(u_1))] sym f0 fv ap 1 bv ap OfNat.ofNat [up(u_1)] sym f0 fv ap NAT 0 lit ap Zero.toOfNat0 [up(u_1)] sym f0 fv ap CommMonoidWithZero.toZero [up(u_1)] sym f0 fv ap 3 bv ap ap ap ap EXPLICIT Not [] sym IsUnit [up(u_1)] sym f0 fv ap MonoidWithZero.toMonoid [up(u_1)] sym f0 fv ap CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym f0 fv ap 4 bv ap ap ap 1 bv ap ap Exists [us(u0)] sym Nat [] sym ap EXPLICIT Nat [] sym Exists [us(up(u_1))] sym f0 fv ap EXPLICIT f0 fv And [] sym Not [] sym Dvd.dvd [up(u_1)] sym f0 fv ap semigroupDvd [up(u_1)] sym f0 fv ap SemigroupWithZero.toSemigroup [up(u_1)] sym f0 fv ap MonoidWithZero.toSemigroupWithZero [up(u_1)] sym f0 fv ap CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym f0 fv ap 7 bv ap ap a
... [13717 more characters]
```

## Example 9 — `Mathlib/Order/Interval/Finset/Nat.lean::Nat.image_Ico_mod::11`

**Shape:** 1 goal(s), 11 local declaration(s), 4 external premise(s). Domain `Order`.

### SEED_LEAN_LIKE

*10,747 characters*

```text
#
  Y
    TH: Nat.image_Ico_mod
    FL: Mathlib/Order/Interval/Finset/Nat.lean
Σ₀
  D a~bf0
    n: a
    b: IMPLICIT
    d: cdecl
    ∈: sym(Nat,[])
  D b~bf1
    n: b
    b: IMPLICIT
    d: cdecl
    ∈: sym(Nat,[])
  D c~bf2
    n: c
    b: IMPLICIT
    d: cdecl
    ∈: sym(Nat,[])
  D image_Ico_mod~bf3
    n: image_Ico_mod
    b: EXPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,sym(Nat,[]),pi(EXPLICIT,sym(Nat,[]),ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Finset,[u0]),sym(Nat,[]))),ap(ap(ap(ap(ap(sym(Finset.image,[u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(instDecidableEqNat,[])),lam(EXPLICIT,sym(Nat,[]),ap(ap(ap(ap(ap(ap(sym(HMod.hMod,[u0 u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(Nat,[])),ap(ap(sym(instHMod,[u0]),sym(Nat,[])),sym(Nat.instMod,[]))),bv(0)),bv(1)))),ap(ap(ap(ap(ap(sym(Finset.Ico,[u0]),sym(Nat,[])),ap(ap(sym(PartialOrder.toPreorder,[u0]),sym(Nat,[])),ap(ap(sym(SemilatticeInf.toPartialOrder,[u0]),sym(Nat,[])),ap(ap(sym(Lattice.toSemilatticeInf,[u0]),sym(Nat,[])),ap(ap(sym(DistribLattice.toLattice,[u0]),sym(Nat,[])),sym(instDistribLatticeNat,[])))))),sym(Nat.instLocallyFiniteOrder,[])),bv(1)),ap(ap(ap(ap(ap(ap(sym(HAdd.hAdd,[u0 u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(Nat,[])),ap(ap(sym(instHAdd,[u
... [9547 more characters]
```

### SEED_PRIOR_HML

*12,150 characters*

```text
meta
  summary
    theorem: Nat.image_Ico_mod
    file: Mathlib/Order/Interval/Finset/Nat.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sym Nat [])
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sym Nat [])
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sym Nat [])
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (sym Nat []) (pi EXPLICIT (sym Nat []) (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (ap (sym Finset.image [u0 u0]) (sym Nat [])) (sym Nat [])) (sym instDecidableEqNat [])) (lam EXPLICIT (sym Nat []) (ap (ap (ap (ap (ap (ap (sym HMod.hMod [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHMod [u0]) (sym Nat [])) (sym Nat.instMod []))) (bv 0)) (bv 1)))) (ap (ap (ap (ap (ap (sym Finset.Ico [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat []))))))
... [10950 more characters]
```

### SEED_STRUCTURED_ENGLISH

*12,472 characters*

```text
In meta:
  summary has theorem is Nat.image_Ico_mod; and file is Mathlib/Order/Interval/Finset/Nat.lean .
In state_before:
  decl a~bf0 has display is a; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(Nat,[]) .
  decl b~bf1 has display is b; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(Nat,[]) .
  decl c~bf2 has display is c; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(Nat,[]) .
  decl image_Ico_mod~bf3 has display is image_Ico_mod; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,sym(Nat,[]),pi(EXPLICIT,sym(Nat,[]),ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Finset,[u0]),sym(Nat,[]))),ap(ap(ap(ap(ap(sym(Finset.image,[u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(instDecidableEqNat,[])),lam(EXPLICIT,sym(Nat,[]),ap(ap(ap(ap(ap(ap(sym(HMod.hMod,[u0 u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(Nat,[])),ap(ap(sym(instHMod,[u0]),sym(Nat,[])),sym(Nat.instMod,[]))),bv(0)),bv(1)))),ap(ap(ap(ap(ap(sym(Finset.Ico,[u0]),sym(Nat,[])),ap(ap(sym(PartialOrder.toPreorder,[u0]),sym(Nat,[])),ap(ap(sym(SemilatticeInf.toPartialOrder,[u0]),sym(Nat,[])),ap(ap(sym(Lattice.toSemilatticeInf,[u0]),sym(Nat,[]
... [11272 more characters]
```

### SEED_TYPED_AST

*11,312 characters*

```text
mta
  - smy
    thm: Nat.image_Ico_mod
    fl: Mathlib/Order/Interval/Finset/Nat.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sym|Nat,[]}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {sym|Nat,[]}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {sym|Nat,[]}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{sym|Nat,[]},{pi|EXPLICIT,{sym|Nat,[]},{ap|{ap|{ap|{sym|Eq,[us{u0}]},{ap|{sym|Finset,[u0]},{sym|Nat,[]}}},{ap|{ap|{ap|{ap|{ap|{sym|Finset.image,[u0 u0]},{sym|Nat,[]}},{sym|Nat,[]}},{sym|instDecidableEqNat,[]}},{lam|EXPLICIT,{sym|Nat,[]},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HMod.hMod,[u0 u0 u0]},{sym|Nat,[]}},{sym|Nat,[]}},{sym|Nat,[]}},{ap|{ap|{sym|instHMod,[u0]},{sym|Nat,[]}},{sym|Nat.instMod,[]}}},{bv|0}},{bv|1}}}},{ap|{ap|{ap|{ap|{ap|{sym|Finset.Ico,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|PartialOrder.toPreorder,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|SemilatticeInf.toPartialOrder,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|Lattice.toSemilatticeInf,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|DistribLattice.toLattice,[u0]},{sym|Nat,[]}},{sym|instDistribLatticeNat,[]}}}}}},{sym|Nat.instLocallyFiniteOrder,[]}},{bv|1}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HAdd.hAdd,[u0 u0 u0]},{sym|Nat,[]}},{sym|Nat
... [10112 more characters]
```

### FINALIST R_5b2eb732ac8b

*9,592 characters*

```text
#
  Y
    TH: Nat.image_Ico_mod
    FL: Mathlib/Order/Interval/Finset/Nat.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [Nat.mul_add,add_assoc,add_comm,mul_one]
    L: [Mathlib/Order/Interval/Finset/Nat.lean::Nat.image_Ico_mod::11:before:local:f4,Mathlib/Order/Interval/Finset/Nat.lean::Nat.image_Ico_mod::11:before:local:f5]
Σ₀
  □ bm4
    ⊢: bm3 mv
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10]
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: Nat [] sym
  D bf1
    b: IMPLICIT
    d: cdecl
    ∈: Nat [] sym
  D bf2
    b: IMPLICIT
    d: cdecl
    ∈: Nat [] sym
  D bf3
    b: EXPLICIT
    d: cdecl
    ∈: EXPLICIT Nat [] sym EXPLICIT Nat [] sym Eq [us(u0)] sym Finset [u0] sym Nat [] sym ap ap Finset.image [u0 u0] sym Nat [] sym ap Nat [] sym ap instDecidableEqNat [] sym ap EXPLICIT Nat [] sym HMod.hMod [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHMod [u0] sym Nat [] sym ap Nat.instMod [] sym ap ap 0 bv ap 1 bv ap lam ap Finset.Ico [u0] sym Nat [] sym ap PartialOrder.toPreorder [u0] sym Nat [] sym ap SemilatticeInf.toPartialOrder [u0] sym Nat [] sym ap Lattice.toSemilatticeInf [u0] sym Nat [] sym ap D
... [8392 more characters]
```

### FINALIST R_000441b08de4

*9,655 characters*

```text
mta
  smy ;; thm: Nat.image_Ico_mod ;; fl: Mathlib/Order/Interval/Finset/Nat.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Nat [] sym
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Nat [] sym
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Nat [] sym
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: EXPLICIT Nat [] sym EXPLICIT Nat [] sym Eq [us(u0)] sym Finset [u0] sym Nat [] sym ap ap Finset.image [u0 u0] sym Nat [] sym ap Nat [] sym ap instDecidableEqNat [] sym ap EXPLICIT Nat [] sym HMod.hMod [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHMod [u0] sym Nat [] sym ap Nat.instMod [] sym ap ap 0 bv ap 1 bv ap lam ap Finset.Ico [u0] sym Nat [] sym ap PartialOrder.toPreorder [u0] sym Nat [] sym ap SemilatticeInf.toPartialOrder [u0] sym Nat [] sym ap Lattice.toSemilatticeInf [u0] sym Nat [] sym ap DistribLattice.toLattice [u0] sym Nat [] sym ap instDistribLatticeNat [] sym ap ap ap ap ap Nat.instLocallyFiniteOrder [] sym ap 1 bv ap HAdd.hAdd [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHAdd [u0] sym Nat [] sym ap instAddNat [] sym ap ap 1 bv ap 0 bv ap ap ap ap Finset.range [] sym 0 bv ap ap pi pi
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Nat [] sym
  dc
... [8455 more characters]
```

### FINALIST R_01d4e489af53

*10,837 characters*

```text
(mta
  (smy (thm Nat.image_Ico_mod) (fl Mathlib/Order/Interval/Finset/Nat.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (sym Nat []) (pi EXPLICIT (sym Nat []) (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (ap (sym Finset.image [u0 u0]) (sym Nat [])) (sym Nat [])) (sym instDecidableEqNat [])) (lam EXPLICIT (sym Nat []) (ap (ap (ap (ap (ap (ap (sym HMod.hMod [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHMod [u0]) (sym Nat [])) (sym Nat.instMod []))) (bv 0)) (bv 1)))) (ap (ap (ap (ap (ap (sym Finset.Ico [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (bv 1)) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHAdd [u
... [9637 more characters]
```

### FINALIST R_101e806690b0

*24,616 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (ap (sym LE.le [u0]) (sym Nat [])) (ap (ap (sym Preorder.toLE [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat []))))))) (fv bf4)) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHAdd [u0]) (sym Nat [])) (ap (ap (sym AddSemigroup.toAdd [u0]) (sym Nat [])) (sym Nat.instAddSemigroup [])))) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHAdd [u0]) (sym Nat [])) (ap (ap (sym AddSemigroup.toAdd [u0]) (sym Nat [])) (sym Nat.instAddSemigroup [])))) (fv bf7)) (fv bf5))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHMul [u0]) (sym Nat [])) (sym instMulNat []))) (fv bf5)) (ap (ap (ap (ap (ap (ap (sym HDiv.hDiv [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHDiv [u0]) (sym Nat [])) (sym Nat.instDiv []))) (fv bf4)) (fv bf5))
... [23416 more characters]
```

### FINALIST R_28b291b5ebe6

*11,038 characters*

```text
meta
  summary ;; theorem-> Nat.image_Ico_mod ;; file-> Mathlib/Order/Interval/Finset/Nat.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Nat [] sym
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Nat [] sym
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Nat [] sym
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT Nat [] sym EXPLICIT Nat [] sym Eq [us(u0)] sym Finset [u0] sym Nat [] sym ap ap Finset.image [u0 u0] sym Nat [] sym ap Nat [] sym ap instDecidableEqNat [] sym ap EXPLICIT Nat [] sym HMod.hMod [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHMod [u0] sym Nat [] sym ap Nat.instMod [] sym ap ap 0 bv ap 1 bv ap lam ap Finset.Ico [u0] sym Nat [] sym ap PartialOrder.toPreorder [u0] sym Nat [] sym ap SemilatticeInf.toPartialOrder [u0] sym Nat [] sym ap Lattice.toSemilatticeInf [u0] sym Nat [] sym ap DistribLattice.toLattice [u0] sym Nat [] sym ap instDistribLatticeNat [] sym ap ap ap ap ap Nat.instLocallyFiniteOrder [] sym ap 1 bv ap HAdd.hAdd [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHAdd [u0] sym Nat [] sym ap instAdd
... [9838 more characters]
```

## Example 10 — `Mathlib/Analysis/ODE/PicardLindelof.lean::PicardLindelof.FunSpace.dist_iterate_next_apply_le::4`

**Shape:** 1 goal(s), 12 local declaration(s), 1 external premise(s). Domain `Analysis`.

### SEED_LEAN_LIKE

*29,985 characters*

```text
#
  Y
    TH: PicardLindelof.FunSpace.dist_iterate_next_apply_le
    FL: Mathlib/Analysis/ODE/PicardLindelof.lean
Σ₀
  D E~bf0
    n: E
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950~bf1
    n: inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(NormedAddCommGroup,[up(u_1)]),fv(E~bf0))
  D inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2953~bf2
    n: inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2953
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(ap(ap(ap(sym(NormedSpace,[u0 up(u_1)]),sym(Real,[])),fv(E~bf0)),sym(Real.normedField,[])),ap(ap(sym(NormedAddCommGroup.toSeminormedAddCommGroup,[up(u_1)]),fv(E~bf0)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950~bf1)))
  D v~bf3
    n: v
    b: IMPLICIT
    d: cdecl
    ∈: ap(ap(ap(sym(PicardLindelof,[up(u_1)]),fv(E~bf0)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950~bf1)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2953~bf2))
  D f~bf4
    n: f
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(ap(ap(sym(PicardLindelof.FunSpace,[up(u_1)]),fv(E~bf0)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelo
... [28785 more characters]
```

### SEED_PRIOR_HML

*22,283 characters*

```text
meta
  summary
    theorem: PicardLindelof.FunSpace.dist_iterate_next_apply_le
    file: Mathlib/Analysis/ODE/PicardLindelof.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym NormedAddCommGroup [up(u_1)]) (fv bf0))
  decl bf2
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (sym NormedSpace [u0 up(u_1)]) (sym Real [])) (fv bf0)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv bf0)) (fv bf1)))
  decl bf3
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (sym PicardLindelof [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))
  decl bf5
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym CompleteSpace [up(u_1)]) (fv bf0)) (ap (ap (sym PseudoMetricSpace.toUniformSpace [up(u_1)]) (fv bf0)) (ap (ap (sym SeminormedAddCommGroup.toPs
... [21083 more characters]
```

### SEED_STRUCTURED_ENGLISH

*30,935 characters*

```text
In meta:
  summary has theorem is PicardLindelof.FunSpace.dist_iterate_next_apply_le; and file is Mathlib/Analysis/ODE/PicardLindelof.lean .
In state_before:
  decl E~bf0 has display is E; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950~bf1 has display is inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(NormedAddCommGroup,[up(u_1)]),fv(E~bf0)) .
  decl inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2953~bf2 has display is inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2953; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(ap(sym(NormedSpace,[u0 up(u_1)]),sym(Real,[])),fv(E~bf0)),sym(Real.normedField,[])),ap(ap(sym(NormedAddCommGroup.toSeminormedAddCommGroup,[up(u_1)]),fv(E~bf0)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950~bf1))) .
  decl v~bf3 has display is v; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(sym(PicardLindelof,[up(u_1)]),fv(E~bf0)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._h
... [29735 more characters]
```

### SEED_TYPED_AST

*21,800 characters*

```text
mta
  - smy
    thm: PicardLindelof.FunSpace.dist_iterate_next_apply_le
    fl: Mathlib/Analysis/ODE/PicardLindelof.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|NormedAddCommGroup,[up{u_1}]},{fv|bf0}}
  - dc bf2
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|NormedSpace,[u0 up{u_1}]},{sym|Real,[]}},{fv|bf0}},{sym|Real.normedField,[]}},{ap|{ap|{sym|NormedAddCommGroup.toSeminormedAddCommGroup,[up{u_1}]},{fv|bf0}},{fv|bf1}}}
  - dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{sym|PicardLindelof,[up{u_1}]},{fv|bf0}},{fv|bf1}},{fv|bf2}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|PicardLindelof.FunSpace,[up{u_1}]},{fv|bf0}},{fv|bf1}},{fv|bf2}},{fv|bf3}}
  - dc bf5
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|CompleteSpace,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|PseudoMetricSpace.toUniformSpace,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|SeminormedAddCommGroup.toPseudoMetricSpace,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|NormedAddCommGroup.toSeminormedAddCommGroup,[up{u_1}]},{fv|bf0}},{fv|bf1}}}}}
  - dc bf6
    br: EXPLICIT
    dr: cdecl
... [20600 more characters]
```

### FINALIST R_5b2eb732ac8b

*18,337 characters*

```text
#
  Y
    TH: PicardLindelof.FunSpace.dist_iterate_next_apply_le
    FL: Mathlib/Analysis/ODE/PicardLindelof.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [PicardLindelof.FunSpace.dist_next_apply_le_of_le]
    L: [Mathlib/Analysis/ODE/PicardLindelof.lean::PicardLindelof.FunSpace.dist_iterate_next_apply_le::4:before:local:f10]
Σ₀
  □ bm1
    ⊢: LE.le [u0] sym Real [] sym ap Real.instLE [] sym ap Dist.dist [up(u_1)] sym bf0 fv ap PseudoMetricSpace.toDist [up(u_1)] sym bf0 fv ap SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)] sym bf0 fv ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap PicardLindelof.FunSpace.toFun [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap PicardLindelof.FunSpace.next [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap Nat.iterate [us(up(u_1))] sym PicardLindelof.FunSpace [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap ap PicardLindelof.FunSpace.next [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap ap bf9 fv ap bf7 fv ap ap ap bf11 fv ap ap PicardLindelof.FunSpace.toFun [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap PicardLindel
... [17137 more characters]
```

### FINALIST R_000441b08de4

*18,160 characters*

```text
mta
  smy ;; thm: PicardLindelof.FunSpace.dist_iterate_next_apply_le ;; fl: Mathlib/Analysis/ODE/PicardLindelof.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedAddCommGroup [up(u_1)] sym bf0 fv ap
  dc bf2 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedSpace [u0 up(u_1)] sym Real [] sym ap bf0 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym bf0 fv ap bf1 fv ap ap
  dc bf3 ;; br: IMPLICIT ;; dr: cdecl ;; ty: PicardLindelof [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: PicardLindelof.FunSpace [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap
  dc bf5 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: CompleteSpace [up(u_1)] sym bf0 fv ap PseudoMetricSpace.toUniformSpace [up(u_1)] sym bf0 fv ap SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)] sym bf0 fv ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap
  dc bf6 ;; br: EXPLICIT ;; dr: cdecl ;; ty: EXPLICIT PicardLindelof.FunSpace [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap EXPLICIT PicardLindelof.FunSpace [up(u_1)] 
... [16960 more characters]
```

### FINALIST R_01d4e489af53

*21,196 characters*

```text
(mta
  (smy (thm PicardLindelof.FunSpace.dist_iterate_next_apply_le) (fl Mathlib/Analysis/ODE/PicardLindelof.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_1)]) (fv f0))))
  (dc f2 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_1)]) (sym Real [])) (fv f0)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv f0)) (fv f1)))))
  (dc f3 (br IMPLICIT) (dr cdecl) (ty (ap (ap (ap (sym PicardLindelof [up(u_1)]) (fv f0)) (fv f1)) (fv f2))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv f0)) (fv f1)) (fv f2)) (fv f3))))
  (dc f5 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym CompleteSpace [up(u_1)]) (fv f0)) (ap (ap (sym PseudoMetricSpace.toUniformSpace [up(u_1)]) (fv f0)) (ap (ap (sym SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)]) (fv f0)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv f0)) (fv f1)))))))
  (dc f6 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv f0)) (fv
... [19996 more characters]
```

### FINALIST R_101e806690b0

*68,930 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (ap (sym LE.le [u0]) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (sym Dist.dist [up(u_1)]) (fv bf0)) (ap (ap (sym PseudoMetricSpace.toDist [up(u_1)]) (fv bf0)) (ap (ap (sym SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)]) (fv bf0)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv bf0)) (fv bf1))))) (ap (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.toFun [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (sym Nat.iterate [us(up(u_1))]) (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (fv bf9)) (fv bf7)))) (fv bf11))) (ap (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.toFun [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (sym Nat.iterate [us(up(u_1))]) (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)
... [67730 more characters]
```

### FINALIST R_28b291b5ebe6

*19,890 characters*

```text
meta
  summary ;; theorem-> PicardLindelof.FunSpace.dist_iterate_next_apply_le ;; file-> Mathlib/Analysis/ODE/PicardLindelof.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> NormedAddCommGroup [up(u_1)] sym f0 fv ap
  decl f2 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> NormedSpace [u0 up(u_1)] sym Real [] sym ap f0 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym f0 fv ap f1 fv ap ap
  decl f3 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> PicardLindelof [up(u_1)] sym f0 fv ap f1 fv ap f2 fv ap
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> PicardLindelof.FunSpace [up(u_1)] sym f0 fv ap f1 fv ap f2 fv ap f3 fv ap
  decl f5 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> CompleteSpace [up(u_1)] sym f0 fv ap PseudoMetricSpace.toUniformSpace [up(u_1)] sym f0 fv ap SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)] sym f0 fv ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym f0 fv ap f1 fv ap ap 
... [18690 more characters]
```

## Example 11 — `Mathlib/Tactic/Ring/Basic.lean::Mathlib.Tactic.Ring.mul_pf_left::0`

**Shape:** 1 goal(s), 12 local declaration(s), 0 external premise(s). Domain `Tactic`.

### SEED_LEAN_LIKE

*19,922 characters*

```text
#
  Y
    TH: Mathlib.Tactic.Ring.mul_pf_left
    FL: Mathlib/Tactic/Ring/Basic.lean
Σ₀
  D u~bf0
    n: u
    b: IMPLICIT
    d: cdecl
    ∈: sym(Lean.Level,[])
  D R~bf1
    n: R
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D α~bf2
    n: α
    b: IMPLICIT
    d: cdecl
    ∈: ap(sym(Qq.Quoted,[]),ap(sym(Lean.Expr.sort,[]),ap(sym(Lean.Level.succ,[]),fv(u~bf0))))
  D sα~bf3
    n: sα
    b: EXPLICIT
    d: cdecl
    ∈: ap(sym(Qq.Quoted,[]),ap(ap(sym(Lean.Expr.app,[]),ap(ap(sym(Lean.Expr.const,[]),ap(sym(Lean.Name.mkStr1,[]),lit(STRING,CommSemiring))),ap(ap(ap(sym(List.cons,[u0]),sym(Lean.Level,[])),fv(u~bf0)),ap(sym(List.nil,[u0]),sym(Lean.Level,[]))))),fv(α~bf2)))
  D inst._@.Mathlib.Tactic.Ring.Basic._hyg.5655~bf4
    n: inst._@.Mathlib.Tactic.Ring.Basic._hyg.5655
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(CommSemiring,[up(u_1)]),fv(R~bf1))
  D mul_pf_left~bf5
    n: mul_pf_left
    b: EXPLICIT
    d: cdecl
    ∈: pi(IMPLICIT,fv(R~bf1),pi(IMPLICIT,fv(R~bf1),pi(IMPLICIT,fv(R~bf1),pi(EXPLICIT,fv(R~bf1),pi(EXPLICIT,sym(Nat,[]),pi(EXPLICIT,ap(ap(ap(sym(Eq,[us(up(u_1))]),fv(R~bf1)),ap(ap(ap(ap(ap(ap(sym(HMul.hMul,[up(u_1) up(u_1) up(u_1)]),fv(R~bf1)),fv(R~bf1)),fv(
... [18722 more characters]
```

### SEED_PRIOR_HML

*19,198 characters*

```text
meta
  summary
    theorem: Mathlib.Tactic.Ring.mul_pf_left
    file: Mathlib/Tactic/Ring/Basic.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sym Lean.Level [])
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Qq.Quoted []) (ap (sym Lean.Expr.sort []) (ap (sym Lean.Level.succ []) (fv bf0))))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (sym Qq.Quoted []) (ap (ap (sym Lean.Expr.app []) (ap (ap (sym Lean.Expr.const []) (ap (sym Lean.Name.mkStr1 []) (lit STRING CommSemiring))) (ap (ap (ap (sym List.cons [u0]) (sym Lean.Level [])) (fv bf0)) (ap (sym List.nil [u0]) (sym Lean.Level []))))) (fv bf2)))
  decl bf4
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym CommSemiring [up(u_1)]) (fv bf1))
  decl bf5
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi EXPLICIT (fv bf1) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf1)) (ap (ap (ap (
... [17998 more characters]
```

### SEED_STRUCTURED_ENGLISH

*21,381 characters*

```text
In meta:
  summary has theorem is Mathlib.Tactic.Ring.mul_pf_left; and file is Mathlib/Tactic/Ring/Basic.lean .
In state_before:
  decl u~bf0 has display is u; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(Lean.Level,[]) .
  decl R~bf1 has display is R; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl α~bf2 has display is α; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is ap(sym(Qq.Quoted,[]),ap(sym(Lean.Expr.sort,[]),ap(sym(Lean.Level.succ,[]),fv(u~bf0)))) .
  decl sα~bf3 has display is sα; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(sym(Qq.Quoted,[]),ap(ap(sym(Lean.Expr.app,[]),ap(ap(sym(Lean.Expr.const,[]),ap(sym(Lean.Name.mkStr1,[]),lit(STRING,CommSemiring))),ap(ap(ap(sym(List.cons,[u0]),sym(Lean.Level,[])),fv(u~bf0)),ap(sym(List.nil,[u0]),sym(Lean.Level,[]))))),fv(α~bf2))) .
  decl inst._@.Mathlib.Tactic.Ring.Basic._hyg.5655~bf4 has display is inst._@.Mathlib.Tactic.Ring.Basic._hyg.5655; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(CommSemiring,[up(u_1)]),fv(R~bf1)) .
  decl mul_pf_left~bf5 has display
... [20181 more characters]
```

### SEED_TYPED_AST

*18,465 characters*

```text
mta
  - smy
    thm: Mathlib.Tactic.Ring.mul_pf_left
    fl: Mathlib/Tactic/Ring/Basic.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sym|Lean.Level,[]}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Qq.Quoted,[]},{ap|{sym|Lean.Expr.sort,[]},{ap|{sym|Lean.Level.succ,[]},{fv|bf0}}}}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{sym|Qq.Quoted,[]},{ap|{ap|{sym|Lean.Expr.app,[]},{ap|{ap|{sym|Lean.Expr.const,[]},{ap|{sym|Lean.Name.mkStr1,[]},{lit|STRING,CommSemiring}}},{ap|{ap|{ap|{sym|List.cons,[u0]},{sym|Lean.Level,[]}},{fv|bf0}},{ap|{sym|List.nil,[u0]},{sym|Lean.Level,[]}}}}},{fv|bf2}}}
  - dc bf4
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|CommSemiring,[up{u_1}]},{fv|bf1}}
  - dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: {pi|IMPLICIT,{fv|bf1},{pi|IMPLICIT,{fv|bf1},{pi|IMPLICIT,{fv|bf1},{pi|EXPLICIT,{fv|bf1},{pi|EXPLICIT,{sym|Nat,[]},{pi|EXPLICIT,{ap|{ap|{ap|{sym|Eq,[us{up{u_1}}]},{fv|bf1}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HMul.hMul,[up{u_1} up{u_1} up{u_1}]},{fv|bf1}},{fv|bf1}},{fv|bf1}},{ap|{ap|{sym|instHMul,[up{u_1}]},{fv|bf1}},{ap|{ap|{sym|NonUnitalNonAssocSemiring.toMu
... [17265 more characters]
```

### FINALIST R_5b2eb732ac8b

*16,021 characters*

```text
#
  Y
    TH: Mathlib.Tactic.Ring.mul_pf_left
    FL: Mathlib/Tactic/Ring/Basic.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: []
    L: []
Σ₀
  □ bm0
    ⊢: Eq [us(up(u_1))] sym bf1 fv ap HMul.hMul [up(u_1) up(u_1) up(u_1)] sym bf1 fv ap bf1 fv ap bf1 fv ap instHMul [up(u_1)] sym bf1 fv ap NonUnitalNonAssocSemiring.toMul [up(u_1)] sym bf1 fv ap NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)] sym bf1 fv ap Semiring.toNonAssocSemiring [up(u_1)] sym bf1 fv ap CommSemiring.toSemiring [up(u_1)] sym bf1 fv ap bf4 fv ap ap ap ap ap ap HMul.hMul [up(u_1) up(u_1) up(u_1)] sym bf1 fv ap bf1 fv ap bf1 fv ap instHMul [up(u_1)] sym bf1 fv ap NonUnitalNonAssocSemiring.toMul [up(u_1)] sym bf1 fv ap NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)] sym bf1 fv ap Semiring.toNonAssocSemiring [up(u_1)] sym bf1 fv ap CommSemiring.toSemiring [up(u_1)] sym bf1 fv ap bf4 fv ap ap ap ap ap ap HPow.hPow [up(u_1) u0 up(u_1)] sym bf1 fv ap Nat [] sym ap bf1 fv ap instHPow [up(u_1) u0] sym bf1 fv ap Nat [] sym ap Monoid.toNatPow [up(u_1)] sym bf1 fv ap MonoidWithZero.toMonoid [up(u_1)] sym bf1 fv ap Semiring.toMonoidWithZero [up(u_1)
... [14821 more characters]
```

### FINALIST R_000441b08de4

*15,693 characters*

```text
mta
  smy ;; thm: Mathlib.Tactic.Ring.mul_pf_left ;; fl: Mathlib/Tactic/Ring/Basic.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Lean.Level [] sym
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Qq.Quoted [] sym Lean.Expr.sort [] sym Lean.Level.succ [] sym bf0 fv ap ap ap
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Qq.Quoted [] sym Lean.Expr.app [] sym Lean.Expr.const [] sym Lean.Name.mkStr1 [] sym STRING CommSemiring lit ap ap List.cons [u0] sym Lean.Level [] sym ap bf0 fv ap List.nil [u0] sym Lean.Level [] sym ap ap ap ap bf2 fv ap ap
  dc bf4 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: CommSemiring [up(u_1)] sym bf1 fv ap
  dc bf5 ;; br: EXPLICIT ;; dr: cdecl ;; ty: IMPLICIT bf1 fv IMPLICIT bf1 fv IMPLICIT bf1 fv EXPLICIT bf1 fv EXPLICIT Nat [] sym EXPLICIT Eq [us(up(u_1))] sym bf1 fv ap HMul.hMul [up(u_1) up(u_1) up(u_1)] sym bf1 fv ap bf1 fv ap bf1 fv ap instHMul [up(u_1)] sym bf1 fv ap NonUnitalNonAssocSemiring.toMul [up(u_1)] sym bf1 fv ap NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)] sym bf1 fv ap Semiring.toNonAssocSemiring [up(u_1)] sym bf1 fv ap CommSemiring.toSemiring [up(u_1)] sym bf1 fv ap bf
... [14493 more characters]
```

### FINALIST R_01d4e489af53

*17,772 characters*

```text
(mta
  (smy (thm Mathlib.Tactic.Ring.mul_pf_left) (fl Mathlib/Tactic/Ring/Basic.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sym Lean.Level [])))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (ap (sym Qq.Quoted []) (ap (sym Lean.Expr.sort []) (ap (sym Lean.Level.succ []) (fv f0))))))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (ap (sym Qq.Quoted []) (ap (ap (sym Lean.Expr.app []) (ap (ap (sym Lean.Expr.const []) (ap (sym Lean.Name.mkStr1 []) (lit CommSemiring))) (ap (ap (ap (sym List.cons [u0]) (sym Lean.Level [])) (fv f0)) (ap (sym List.nil [u0]) (sym Lean.Level []))))) (fv f2)))))
  (dc f4 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CommSemiring [up(u_1)]) (fv f1))))
  (dc f5 (br EXPLICIT) (dr cdecl) (ty (pi IMPLICIT (fv f1) (pi IMPLICIT (fv f1) (pi IMPLICIT (fv f1) (pi EXPLICIT (fv f1) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (ap (ap (ap (sym Eq [us(up(u_1))]) (fv f1)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv f1)) (fv f1)) (fv f1)) (ap (ap (sym instHMul [up(u_1)]) (fv f1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv f1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(
... [16572 more characters]
```

### FINALIST R_101e806690b0

*57,165 characters*

```text
$
  A $a0
    t-> (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi EXPLICIT (fv bf1) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf1)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym CommSemiring.toSemiring [up(u_1)]) (fv bf1)) (fv bf4))))))) (bv 4)) (bv 3))) (bv 2)) (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf1)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym CommSemiring.toSemiring [up(u_1)]) (fv bf1)) (fv bf4))))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (a
... [55965 more characters]
```

### FINALIST R_28b291b5ebe6

*17,442 characters*

```text
meta
  summary ;; theorem-> Mathlib.Tactic.Ring.mul_pf_left ;; file-> Mathlib/Tactic/Ring/Basic.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Lean.Level [] sym
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Qq.Quoted [] sym Lean.Expr.sort [] sym Lean.Level.succ [] sym f0 fv ap ap ap
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Qq.Quoted [] sym Lean.Expr.app [] sym Lean.Expr.const [] sym Lean.Name.mkStr1 [] sym STRING CommSemiring lit ap ap List.cons [u0] sym Lean.Level [] sym ap f0 fv ap List.nil [u0] sym Lean.Level [] sym ap ap ap ap f2 fv ap ap
  decl f4 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> CommSemiring [up(u_1)] sym f1 fv ap
  decl f5 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> IMPLICIT f1 fv IMPLICIT f1 fv IMPLICIT f1 fv EXPLICIT f1 fv EXPLICIT Nat [] sym EXPLICIT Eq [us(up(u_1))] sym f1 fv ap HMul.hMul [up(u_1) up(u_1) up(u_1)] sym f1 fv ap f1 fv ap f1 fv ap instHMul [up(u_1)] sym f1 fv ap NonUnitalNonAssocSemiring.toMul [up(u_1)] s
... [16242 more characters]
```

## Example 12 — `Mathlib/NumberTheory/ArithmeticFunction.lean::ArithmeticFunction.one_smul'::16`

**Shape:** 1 goal(s), 13 local declaration(s), 4 external premise(s). Domain `NumberTheory`.

### SEED_LEAN_LIKE

*19,521 characters*

```text
#
  Y
    TH: ArithmeticFunction.one_smul'
    FL: Mathlib/NumberTheory/ArithmeticFunction.lean
Σ₀
  D R~bf0
    n: R
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D M~bf1
    n: M
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_2)))
  D inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1755~bf2
    n: inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1755
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(Semiring,[up(u_1)]),fv(R~bf0))
  D inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1758~bf3
    n: inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1758
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(AddCommMonoid,[up(u_2)]),fv(M~bf1))
  D inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1761~bf4
    n: inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1761
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(ap(ap(ap(sym(Module,[up(u_1) up(u_2)]),fv(R~bf0)),fv(M~bf1)),fv(inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1755~bf2)),fv(inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1758~bf3))
  D one_smul'~bf5
    n: one_smul'
    b: EXPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,ap(ap(sym(ArithmeticFunction,[up(u_2)]),fv(M~bf1)),ap(ap(sym(AddM
... [18321 more characters]
```

### SEED_PRIOR_HML

*16,953 characters*

```text
meta
  summary
    theorem: ArithmeticFunction.one_smul'
    file: Mathlib/NumberTheory/ArithmeticFunction.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_2)))
  decl bf2
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Semiring [up(u_1)]) (fv bf0))
  decl bf3
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym AddCommMonoid [up(u_2)]) (fv bf1))
  decl bf4
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (sym Module [up(u_1) up(u_2)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))
  decl bf5
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3)))) (ap (ap (ap (sym Eq [us(up(u_2))]) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (f
... [15753 more characters]
```

### SEED_STRUCTURED_ENGLISH

*22,016 characters*

```text
In meta:
  summary has theorem is ArithmeticFunction.one_smul'; and file is Mathlib/NumberTheory/ArithmeticFunction.lean .
In state_before:
  decl R~bf0 has display is R; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl M~bf1 has display is M; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_2))) .
  decl inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1755~bf2 has display is inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1755; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(Semiring,[up(u_1)]),fv(R~bf0)) .
  decl inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1758~bf3 has display is inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1758; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(AddCommMonoid,[up(u_2)]),fv(M~bf1)) .
  decl inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1761~bf4 has display is inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1761; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(ap(sym(Module,[up(u_1) up(u_2)]),fv(R~bf0)),fv(M
... [20816 more characters]
```

### SEED_TYPED_AST

*15,790 characters*

```text
mta
  - smy
    thm: ArithmeticFunction.one_smul'
    fl: Mathlib/NumberTheory/ArithmeticFunction.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_2}}}
  - dc bf2
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Semiring,[up{u_1}]},{fv|bf0}}
  - dc bf3
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|AddCommMonoid,[up{u_2}]},{fv|bf1}}
  - dc bf4
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|Module,[up{u_1} up{u_2}]},{fv|bf0}},{fv|bf1}},{fv|bf2}},{fv|bf3}}
  - dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{ap|{ap|{sym|ArithmeticFunction,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddMonoid.toZero,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddCommMonoid.toAddMonoid,[up{u_2}]},{fv|bf1}},{fv|bf3}}}},{ap|{ap|{ap|{sym|Eq,[us{up{u_2}}]},{ap|{ap|{sym|ArithmeticFunction,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddMonoid.toZero,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddCommMonoid.toAddMonoid,[up{u_2}]},{fv|bf1}},{fv|bf3}}}}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HSMul.hSMul,[up{u_1} up{u_2} up{u_2}]},{ap|{ap|{sym|ArithmeticFunction,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MonoidWithZero.toZero,[u
... [14590 more characters]
```

### FINALIST R_5b2eb732ac8b

*13,385 characters*

```text
#
  Y
    TH: ArithmeticFunction.one_smul'
    FL: Mathlib/NumberTheory/ArithmeticFunction.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [and_true,not_false_eq_true,one_mul,true_and]
    L: [Mathlib/NumberTheory/ArithmeticFunction.lean::ArithmeticFunction.one_smul'::16:before:local:f11,Mathlib/NumberTheory/ArithmeticFunction.lean::ArithmeticFunction.one_smul'::16:before:local:f12,Mathlib/NumberTheory/ArithmeticFunction.lean::ArithmeticFunction.one_smul'::16:before:local:f8]
Σ₀
  □ bm11
    ⊢: False [] sym
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12]
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_1)) sort
  D bf1
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_2)) sort
  D bf2
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: Semiring [up(u_1)] sym bf0 fv ap
  D bf3
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: AddCommMonoid [up(u_2)] sym bf1 fv ap
  D bf4
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: Module [up(u_1) up(u_2)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap
  D bf5
    b: EXPLICIT
    d: cdecl
    ∈: EXPLICIT ArithmeticFunction [up(u_2)] sym bf1 fv ap AddMonoid.toZero [up(u_2)] sym bf1 fv ap Ad
... [12185 more characters]
```

### FINALIST R_000441b08de4

*13,629 characters*

```text
mta
  smy ;; thm: ArithmeticFunction.one_smul' ;; fl: Mathlib/NumberTheory/ArithmeticFunction.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_2)) sort
  dc bf2 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Semiring [up(u_1)] sym bf0 fv ap
  dc bf3 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: AddCommMonoid [up(u_2)] sym bf1 fv ap
  dc bf4 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Module [up(u_1) up(u_2)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap
  dc bf5 ;; br: EXPLICIT ;; dr: cdecl ;; ty: EXPLICIT ArithmeticFunction [up(u_2)] sym bf1 fv ap AddMonoid.toZero [up(u_2)] sym bf1 fv ap AddCommMonoid.toAddMonoid [up(u_2)] sym bf1 fv ap bf3 fv ap ap ap Eq [us(up(u_2))] sym ArithmeticFunction [up(u_2)] sym bf1 fv ap AddMonoid.toZero [up(u_2)] sym bf1 fv ap AddCommMonoid.toAddMonoid [up(u_2)] sym bf1 fv ap bf3 fv ap ap ap ap HSMul.hSMul [up(u_1) up(u_2) up(u_2)] sym ArithmeticFunction [up(u_1)] sym bf0 fv ap MonoidWithZero.toZero [up(u_1)] sym bf0 fv ap Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv ap bf2 fv ap ap ap ap ArithmeticFunction [up(u_2)] sym bf1 fv ap AddMonoid.toZero [up(u_2)] sym bf1 fv ap AddCommMon
... [12429 more characters]
```

### FINALIST R_01d4e489af53

*14,840 characters*

```text
(mta
  (smy (thm ArithmeticFunction.one_smul') (fl Mathlib/NumberTheory/ArithmeticFunction.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc f2 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Semiring [up(u_1)]) (fv f0))))
  (dc f3 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym AddCommMonoid [up(u_2)]) (fv f1))))
  (dc f4 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym Module [up(u_1) up(u_2)]) (fv f0)) (fv f1)) (fv f2)) (fv f3))))
  (dc f5 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv f1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv f1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv f1)) (fv f3)))) (ap (ap (ap (sym Eq [us(up(u_2))]) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv f1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv f1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv f1)) (fv f3))))) (ap (ap (ap (ap (ap (ap (sym HSMul.hSMul [up(u_1) up(u_2) up(u_2)]) (ap (ap (sym ArithmeticFunction [up(u_1)]) (fv f0)) (ap (ap (sym MonoidWithZero.toZero [up(u_1)]) (fv f0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv f0)) (f
... [13640 more characters]
```

### FINALIST R_101e806690b0

*42,315 characters*

```text
$
  A $a0
    t-> (pi EXPLICIT (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3)))) (ap (ap (ap (sym Eq [us(up(u_2))]) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3))))) (ap (ap (ap (ap (ap (ap (sym HSMul.hSMul [up(u_1) up(u_2) up(u_2)]) (ap (ap (sym ArithmeticFunction [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toZero [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (fv bf2))))) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3))))) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3))))) (ap (ap (ap (sym instHSMul [up(u_1) up(u_2)]) (ap (ap (sym ArithmeticFunction [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toZero [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.
... [41115 more characters]
```

### FINALIST R_28b291b5ebe6

*16,761 characters*

```text
meta
  summary ;; theorem-> ArithmeticFunction.one_smul' ;; file-> Mathlib/NumberTheory/ArithmeticFunction.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_2)) sort
  decl f2 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> Semiring [up(u_1)] sym f0 fv ap
  decl f3 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> AddCommMonoid [up(u_2)] sym f1 fv ap
  decl f4 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> Module [up(u_1) up(u_2)] sym f0 fv ap f1 fv ap f2 fv ap f3 fv ap
  decl f5 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT ArithmeticFunction [up(u_2)] sym f1 fv ap AddMonoid.toZero [up(u_2)] sym f1 fv ap AddCommMonoid.toAddMonoid [up(u_2)] sym f1 fv ap f3 fv ap ap ap Eq [us(up(u_2))] sym ArithmeticFunction [up(u_2)] sym f1 fv ap AddMonoid.toZero [up(u_2)] sym f1 fv ap AddCommMonoid.toAddMonoid [up(u_2)] sym f1 fv ap f3 fv ap ap ap ap HSMul.hSMul [up(u_1) up(u_2) up(u_2)] sym ArithmeticFunction [up(u_1)] sym f0 fv ap MonoidWithZero.toZero [up(u
... [15561 more characters]
```

## Example 13 — `Mathlib/Data/Finset/Pi.lean::Finset.pi_insert::3`

**Shape:** 1 goal(s), 14 local declaration(s), 0 external premise(s). Domain `Data`.

### SEED_LEAN_LIKE

*41,635 characters*

```text
#
  Y
    TH: Finset.pi_insert
    FL: Mathlib/Data/Finset/Pi.lean
Σ₀
  D α~bf0
    n: α
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D β~bf1
    n: β
    b: IMPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,fv(α~bf0),sort(us(up(u))))
  D δ~bf2
    n: δ
    b: IMPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,fv(α~bf0),sort(up(v)))
  D inst._@.Mathlib.Data.Finset.Pi._hyg.757~bf3
    n: inst._@.Mathlib.Data.Finset.Pi._hyg.757
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(DecidableEq,[us(up(u_1))]),fv(α~bf0))
  D s~bf4
    n: s
    b: IMPLICIT
    d: cdecl
    ∈: ap(sym(Finset,[up(u_1)]),fv(α~bf0))
  D t~bf5
    n: t
    b: IMPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,fv(α~bf0),ap(sym(Finset,[up(u)]),ap(fv(β~bf1),bv(0))))
  D pi_insert~bf6
    n: pi_insert
    b: EXPLICIT
    d: cdecl
    ∈: pi(INSTANCE_IMPLICIT,pi(EXPLICIT,fv(α~bf0),ap(sym(DecidableEq,[us(up(u))]),ap(fv(β~bf1),bv(0)))),pi(IMPLICIT,ap(sym(Finset,[up(u_1)]),fv(α~bf0)),pi(IMPLICIT,pi(EXPLICIT,fv(α~bf0),ap(sym(Finset,[up(u)]),ap(fv(β~bf1),bv(0)))),pi(IMPLICIT,fv(α~bf0),pi(EXPLICIT,ap(sym(Not,[]),ap(ap(ap(ap(ap(sym(Membership.mem,[up(u_1) up(u_1)]),fv(α~bf0)),ap(sym(Finset,[up(u_1)]),fv(α~bf0))),ap(sym(Finset.instMembership,[
... [40435 more characters]
```

### SEED_PRIOR_HML

*42,056 characters*

```text
meta
  summary
    theorem: Finset.pi_insert
    file: Mathlib/Data/Finset/Pi.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (fv bf0) (sort us(up(u))))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (fv bf0) (sort up(v)))
  decl bf3
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym DecidableEq [us(up(u_1))]) (fv bf0))
  decl bf4
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Finset [up(u_1)]) (fv bf0))
  decl bf5
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (fv bf0) (ap (sym Finset [up(u)]) (ap (fv bf1) (bv 0))))
  decl bf6
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi INSTANCE_IMPLICIT (pi EXPLICIT (fv bf0) (ap (sym DecidableEq [us(up(u))]) (ap (fv bf1) (bv 0)))) (pi IMPLICIT (ap (sym Finset [up(u_1)]) (fv bf0)) (pi IMPLICIT (pi EXPLICIT (fv bf0) (ap (sym Finset [up(u)]) (ap (fv bf1) (bv 0)))) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (ap (ap (sym Membership.
... [40856 more characters]
```

### SEED_STRUCTURED_ENGLISH

*43,864 characters*

```text
In meta:
  summary has theorem is Finset.pi_insert; and file is Mathlib/Data/Finset/Pi.lean .
In state_before:
  decl α~bf0 has display is α; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl β~bf1 has display is β; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,fv(α~bf0),sort(us(up(u)))) .
  decl δ~bf2 has display is δ; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,fv(α~bf0),sort(up(v))) .
  decl inst._@.Mathlib.Data.Finset.Pi._hyg.757~bf3 has display is inst._@.Mathlib.Data.Finset.Pi._hyg.757; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(DecidableEq,[us(up(u_1))]),fv(α~bf0)) .
  decl s~bf4 has display is s; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is ap(sym(Finset,[up(u_1)]),fv(α~bf0)) .
  decl t~bf5 has display is t; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,fv(α~bf0),ap(sym(Finset,[up(u)]),ap(fv(β~bf1),bv(0)))) .
  decl pi_insert~bf6 has display is pi_insert; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(INSTANCE_IMP
... [42664 more characters]
```

### SEED_TYPED_AST

*40,998 characters*

```text
mta
  - smy
    thm: Finset.pi_insert
    fl: Mathlib/Data/Finset/Pi.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{fv|bf0},{sort|us{up{u}}}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{fv|bf0},{sort|up{v}}}
  - dc bf3
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|DecidableEq,[us{up{u_1}}]},{fv|bf0}}
  - dc bf4
    br: IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Finset,[up{u_1}]},{fv|bf0}}
  - dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{fv|bf0},{ap|{sym|Finset,[up{u}]},{ap|{fv|bf1},{bv|0}}}}
  - dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: {pi|INSTANCE_IMPLICIT,{pi|EXPLICIT,{fv|bf0},{ap|{sym|DecidableEq,[us{up{u}}]},{ap|{fv|bf1},{bv|0}}}},{pi|IMPLICIT,{ap|{sym|Finset,[up{u_1}]},{fv|bf0}},{pi|IMPLICIT,{pi|EXPLICIT,{fv|bf0},{ap|{sym|Finset,[up{u}]},{ap|{fv|bf1},{bv|0}}}},{pi|IMPLICIT,{fv|bf0},{pi|EXPLICIT,{ap|{sym|Not,[]},{ap|{ap|{ap|{ap|{ap|{sym|Membership.mem,[up{u_1} up{u_1}]},{fv|bf0}},{ap|{sym|Finset,[up{u_1}]},{fv|bf0}}},{ap|{sym|Finset.instMembership,[up{u_1}]},{fv|bf0}}},{bv|0}},{bv|2}}},{ap|{ap|{ap|{sym|Eq,[umax{us{up{u}},us{up{u_1}}}]},{a
... [39798 more characters]
```

### FINALIST R_5b2eb732ac8b

*34,243 characters*

```text
#
  Y
    TH: Finset.pi_insert
    FL: Mathlib/Data/Finset/Pi.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: []
    L: [Mathlib/Data/Finset/Pi.lean::Finset.pi_insert::3:before:local:f12]
Σ₀
  □ bm15
    ⊢: Eq [um(u0)] sym bm14 mv ap Multiset.dedup [um(u1)] sym bm4 mv ap bm5 mv ap Multiset.pi [um(u2) um(u3)] sym bm6 mv ap bm7 mv ap bm8 mv ap bf12 fv ap EXPLICIT bf0 fv Finset.val [um(u4)] sym bf1 fv 0 bv ap ap bf9 fv 0 bv ap ap lam ap ap ap Multiset.dedup [um(u5)] sym bm9 mv ap bm10 mv ap Multiset.bind [um(u6) um(u7)] sym bm12 mv ap bm13 mv ap Finset.val [um(u8)] sym bm11 mv ap bf9 fv bf10 fv ap ap ap EXPLICIT bf1 fv bf10 fv ap Multiset.dedup [um(u9)] sym EXPLICIT bf0 fv EXPLICIT Membership.mem [up(u_1) up(u_1)] sym bf0 fv ap Multiset [up(u_1)] sym bf0 fv ap ap Multiset.instMembership [up(u_1)] sym bf0 fv ap ap 0 bv ap bf12 fv ap bf1 fv 1 bv ap pi pi ap EXPLICIT EXPLICIT bf0 fv EXPLICIT Membership.mem [up(u_1) up(u_1)] sym bf0 fv ap Multiset [up(u_1)] sym bf0 fv ap ap Multiset.instMembership [up(u_1)] sym bf0 fv ap ap 0 bv ap bf12 fv ap bf1 fv 1 bv ap pi pi EXPLICIT EXPLICIT bf0 fv EXPLICIT Membership.mem [up(u_1) up(u_1
... [33043 more characters]
```

### FINALIST R_000441b08de4

*33,903 characters*

```text
mta
  smy ;; thm: Finset.pi_insert ;; fl: Mathlib/Data/Finset/Pi.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: EXPLICIT bf0 fv us(up(u)) sort pi
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: EXPLICIT bf0 fv up(v) sort pi
  dc bf3 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: DecidableEq [us(up(u_1))] sym bf0 fv ap
  dc bf4 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Finset [up(u_1)] sym bf0 fv ap
  dc bf5 ;; br: IMPLICIT ;; dr: cdecl ;; ty: EXPLICIT bf0 fv Finset [up(u)] sym bf1 fv 0 bv ap ap pi
  dc bf6 ;; br: EXPLICIT ;; dr: cdecl ;; ty: INSTANCE_IMPLICIT EXPLICIT bf0 fv DecidableEq [us(up(u))] sym bf1 fv 0 bv ap ap pi IMPLICIT Finset [up(u_1)] sym bf0 fv ap IMPLICIT EXPLICIT bf0 fv Finset [up(u)] sym bf1 fv 0 bv ap ap pi IMPLICIT bf0 fv EXPLICIT Not [] sym Membership.mem [up(u_1) up(u_1)] sym bf0 fv ap Finset [up(u_1)] sym bf0 fv ap ap Finset.instMembership [up(u_1)] sym bf0 fv ap ap 0 bv ap 2 bv ap ap Eq [umax(us(up(u)) us(up(u_1)))] sym Finset [umax(up(u) up(u_1))] sym EXPLICIT bf0 fv EXPLICIT Membership.mem [up(u_1) up(u_1)] sym bf0 fv ap Finset [up(u_1)] sym bf0 fv ap ap Finset.instMembership [up(u_1)] sym bf0 fv ap 
... [32703 more characters]
```

### FINALIST R_01d4e489af53

*39,530 characters*

```text
(mta
  (smy (thm Finset.pi_insert) (fl Mathlib/Data/Finset/Pi.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (fv f0) (sort us(up(u))))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (fv f0) (sort up(v)))))
  (dc f3 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym DecidableEq [us(up(u_1))]) (fv f0))))
  (dc f4 (br IMPLICIT) (dr cdecl) (ty (ap (sym Finset [up(u_1)]) (fv f0))))
  (dc f5 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (fv f0) (ap (sym Finset [up(u)]) (ap (fv f1) (bv 0))))))
  (dc f6 (br EXPLICIT) (dr cdecl) (ty (pi INSTANCE_IMPLICIT (pi EXPLICIT (fv f0) (ap (sym DecidableEq [us(up(u))]) (ap (fv f1) (bv 0)))) (pi IMPLICIT (ap (sym Finset [up(u_1)]) (fv f0)) (pi IMPLICIT (pi EXPLICIT (fv f0) (ap (sym Finset [up(u)]) (ap (fv f1) (bv 0)))) (pi IMPLICIT (fv f0) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv f0)) (ap (sym Finset [up(u_1)]) (fv f0))) (ap (sym Finset.instMembership [up(u_1)]) (fv f0))) (bv 0)) (bv 2))) (ap (ap (ap (sym Eq [umax(us(up(u)) us(up(u_1)))]) (ap (sym Finset [umax(up(u) up(u_1))]) (pi EXPLICIT (fv f0) (pi EXPLICIT (ap (ap (ap (ap (a
... [38330 more characters]
```

### FINALIST R_101e806690b0

*169,673 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (sym Eq [um(u0)]) (ap (sym Multiset [umax(up(u_1) up(u))]) (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (ap (ap (ap (sym Multiset.cons [up(u_1)]) (fv bf0)) (fv bf10)) (ap (ap (sym Finset.val [up(u_1)]) (fv bf0)) (fv bf8)))) (ap (fv bf1) (bv 1)))))) (ap (ap (ap (sym Multiset.dedup [um(u1)]) (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (ap (ap (ap (sym Multiset.cons [up(u_1)]) (fv bf0)) (fv bf10)) (ap (ap (sym Finset.val [up(u_1)]) (fv bf0)) (fv bf8)))) (ap (fv bf1) (bv 1))))) (lam EXPLICIT (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (ap (ap (ap (sym Multiset.cons [up(u_1)]) (fv bf0)) (fv bf10)) (ap (ap (sym Finset.val [up(u_1)]) (fv bf0)) (fv bf8)))) (ap (fv bf1) (bv 1)))) (l
... [168473 more characters]
```

### FINALIST R_28b291b5ebe6

*36,330 characters*

```text
meta
  summary ;; theorem-> Finset.pi_insert ;; file-> Mathlib/Data/Finset/Pi.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT f0 fv us(up(u)) sort pi
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT f0 fv up(v) sort pi
  decl f3 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> DecidableEq [us(up(u_1))] sym f0 fv ap
  decl f4 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Finset [up(u_1)] sym f0 fv ap
  decl f5 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT f0 fv Finset [up(u)] sym f1 fv 0 bv ap ap pi
  decl f6 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> INSTANCE_IMPLICIT EXPLICIT f0 fv DecidableEq [us(up(u))] sym f1 fv 0 bv ap ap pi IMPLICIT Finset [up(u_1)] sym f0 fv ap IMPLICIT EXPLICIT f0 fv Finset [up(u)] sym f1 fv 0 bv ap ap pi IMPLICIT f0 fv EXPLICIT Not [] sym Membership.mem [up(u_1) up(u_1)] sym f0 fv ap Finset [up(u_1)] sym f0 fv ap ap Finset.instMembership [up(u_1)] sym f0 fv ap ap 0 bv ap 2 bv ap ap Eq [umax(us
... [35130 more characters]
```

## Example 14 — `Mathlib/Data/PNat/Find.lean::PNat.find_comp_succ::2`

**Shape:** 1 goal(s), 15 local declaration(s), 2 external premise(s). Domain `Data`.

### SEED_LEAN_LIKE

*18,688 characters*

```text
#
  Y
    TH: PNat.find_comp_succ
    FL: Mathlib/Data/PNat/Find.lean
Σ₀
  D p~bf0
    n: p
    b: IMPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,sym(PNat,[]),sort(u0))
  D q~bf1
    n: q
    b: IMPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,sym(PNat,[]),sort(u0))
  D inst._@.Mathlib.Data.PNat.Find._hyg.1297~bf2
    n: inst._@.Mathlib.Data.PNat.Find._hyg.1297
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(ap(sym(DecidablePred,[us(u0)]),sym(PNat,[])),fv(p~bf0))
  D inst._@.Mathlib.Data.PNat.Find._hyg.1300~bf3
    n: inst._@.Mathlib.Data.PNat.Find._hyg.1300
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(ap(sym(DecidablePred,[us(u0)]),sym(PNat,[])),fv(q~bf1))
  D h~bf4
    n: h
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(sym(Exists,[us(u0)]),sym(PNat,[])),lam(EXPLICIT,sym(PNat,[]),ap(fv(p~bf0),bv(0))))
  D n~bf5
    n: n
    b: IMPLICIT
    d: cdecl
    ∈: sym(PNat,[])
  D m~bf6
    n: m
    b: IMPLICIT
    d: cdecl
    ∈: sym(PNat,[])
  D find_comp_succ~bf7
    n: find_comp_succ
    b: EXPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,ap(ap(sym(Exists,[us(u0)]),sym(PNat,[])),lam(EXPLICIT,sym(PNat,[]),ap(fv(p~bf0),bv(0)))),pi(EXPLICIT,ap(ap(sym(Exists,[us(u0)]),sym(PNat,[])),lam(EXPLICIT,sym(PNat,[]),ap(f
... [17488 more characters]
```

### SEED_PRIOR_HML

*19,594 characters*

```text
meta
  summary
    theorem: PNat.find_comp_succ
    file: Mathlib/Data/PNat/Find.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (sym PNat []) (sort u0))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (sym PNat []) (sort u0))
  decl bf2
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym DecidablePred [us(u0)]) (sym PNat [])) (fv bf0))
  decl bf3
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym DecidablePred [us(u0)]) (sym PNat [])) (fv bf1))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (bv 0))))
  decl bf5
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sym PNat [])
  decl bf6
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sym PNat [])
  decl bf7
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (bv 0)))) (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PN
... [18394 more characters]
```

### SEED_STRUCTURED_ENGLISH

*20,623 characters*

```text
In meta:
  summary has theorem is PNat.find_comp_succ; and file is Mathlib/Data/PNat/Find.lean .
In state_before:
  decl p~bf0 has display is p; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,sym(PNat,[]),sort(u0)) .
  decl q~bf1 has display is q; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,sym(PNat,[]),sort(u0)) .
  decl inst._@.Mathlib.Data.PNat.Find._hyg.1297~bf2 has display is inst._@.Mathlib.Data.PNat.Find._hyg.1297; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(DecidablePred,[us(u0)]),sym(PNat,[])),fv(p~bf0)) .
  decl inst._@.Mathlib.Data.PNat.Find._hyg.1300~bf3 has display is inst._@.Mathlib.Data.PNat.Find._hyg.1300; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(DecidablePred,[us(u0)]),sym(PNat,[])),fv(q~bf1)) .
  decl h~bf4 has display is h; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(Exists,[us(u0)]),sym(PNat,[])),lam(EXPLICIT,sym(PNat,[]),ap(fv(p~bf0),bv(0)))) .
  decl n~bf5 has display is n; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(PNa
... [19423 more characters]
```

### SEED_TYPED_AST

*18,631 characters*

```text
mta
  - smy
    thm: PNat.find_comp_succ
    fl: Mathlib/Data/PNat/Find.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{sym|PNat,[]},{sort|u0}}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{sym|PNat,[]},{sort|u0}}
  - dc bf2
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|DecidablePred,[us{u0}]},{sym|PNat,[]}},{fv|bf0}}
  - dc bf3
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|DecidablePred,[us{u0}]},{sym|PNat,[]}},{fv|bf1}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{sym|Exists,[us{u0}]},{sym|PNat,[]}},{lam|EXPLICIT,{sym|PNat,[]},{ap|{fv|bf0},{bv|0}}}}
  - dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: {sym|PNat,[]}
  - dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: {sym|PNat,[]}
  - dc bf7
    br: EXPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{ap|{ap|{sym|Exists,[us{u0}]},{sym|PNat,[]}},{lam|EXPLICIT,{sym|PNat,[]},{ap|{fv|bf0},{bv|0}}}},{pi|EXPLICIT,{ap|{ap|{sym|Exists,[us{u0}]},{sym|PNat,[]}},{lam|EXPLICIT,{sym|PNat,[]},{ap|{fv|bf0},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HAdd.hAdd,[u0 u0 u0]},{sym|PNat,[]}},{sym|PNat,[]}},{sym|PNat,[]}},{ap|{ap|{sym|instHAdd,[u0]},{sym|PNat,[]}},{sym|instPNatAdd,[]}}},{bv|0}},
... [17431 more characters]
```

### FINALIST R_5b2eb732ac8b

*15,692 characters*

```text
#
  Y
    TH: PNat.find_comp_succ
    FL: Mathlib/Data/PNat/Find.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [PNat.lt_find_iff,add_lt_add_iff_right]
    L: [Mathlib/Data/PNat/Find.lean::PNat.find_comp_succ::2:before:local:f14]
Σ₀
  □ bm1
    ⊢: Not [] sym bf0 fv HAdd.hAdd [u0 u0 u0] sym PNat [] sym ap PNat [] sym ap PNat [] sym ap instHAdd [u0] sym PNat [] sym ap instPNatAdd [] sym ap ap bf12 fv ap OfNat.ofNat [u0] sym PNat [] sym ap NAT 1 lit ap instOfNatPNatOfNeZeroNat [] sym NAT 1 lit ap NeZero.succ [] sym OfNat.ofNat [u0] sym Nat [] sym ap NAT 0 lit ap instOfNatNat [] sym NAT 0 lit ap ap ap ap ap ap ap ap
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14]
  A bf0
    tg: dependent_function
  A bf12
    tg: PNat
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: EXPLICIT PNat [] sym u0 sort pi
  D bf1
    b: IMPLICIT
    d: cdecl
    ∈: EXPLICIT PNat [] sym u0 sort pi
  D bf2
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: DecidablePred [us(u0)] sym PNat [] sym ap bf0 fv ap
  D bf3
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: DecidablePred [us(u0)] sym PNat [] sym ap bf1 fv ap
  D bf4
    b: EXPLICIT
... [14492 more characters]
```

### FINALIST R_000441b08de4

*15,670 characters*

```text
mta
  smy ;; thm: PNat.find_comp_succ ;; fl: Mathlib/Data/PNat/Find.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: EXPLICIT PNat [] sym u0 sort pi
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: EXPLICIT PNat [] sym u0 sort pi
  dc bf2 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: DecidablePred [us(u0)] sym PNat [] sym ap bf0 fv ap
  dc bf3 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: DecidablePred [us(u0)] sym PNat [] sym ap bf1 fv ap
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym bf0 fv 0 bv ap lam ap
  dc bf5 ;; br: IMPLICIT ;; dr: cdecl ;; ty: PNat [] sym
  dc bf6 ;; br: IMPLICIT ;; dr: cdecl ;; ty: PNat [] sym
  dc bf7 ;; br: EXPLICIT ;; dr: cdecl ;; ty: EXPLICIT Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym bf0 fv 0 bv ap lam ap EXPLICIT Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym bf0 fv HAdd.hAdd [u0 u0 u0] sym PNat [] sym ap PNat [] sym ap PNat [] sym ap instHAdd [u0] sym PNat [] sym ap instPNatAdd [] sym ap ap 0 bv ap OfNat.ofNat [u0] sym PNat [] sym ap NAT 1 lit ap instOfNatPNatOfNeZeroNat [] sym NAT 1 lit ap NeZero.succ [] sym OfNat.ofNat [u0] sym Nat [] sym ap NAT 0 lit ap instOfNatNat [] sym 
... [14470 more characters]
```

### FINALIST R_01d4e489af53

*17,688 characters*

```text
(mta
  (smy (thm PNat.find_comp_succ) (fl Mathlib/Data/PNat/Find.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (sym PNat []) (sort u0))))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (sym PNat []) (sort u0))))
  (dc f2 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym DecidablePred [us(u0)]) (sym PNat [])) (fv f0))))
  (dc f3 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym DecidablePred [us(u0)]) (sym PNat [])) (fv f1))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv f0) (bv 0))))))
  (dc f5 (br IMPLICIT) (dr cdecl) (ty (sym PNat [])))
  (dc f6 (br IMPLICIT) (dr cdecl) (ty (sym PNat [])))
  (dc f7 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv f0) (bv 0)))) (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv f0) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym instHAdd [u0]) (sym PNat [])) (sym instPNatAdd []))) (bv 0)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym PNat [])) (lit 1)) (ap (ap (sym instOfNatPNatOfNe
... [16488 more characters]
```

### FINALIST R_101e806690b0

*34,381 characters*

```text
$
  A $a0
    t-> (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (bv 0)))) (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym instHAdd [u0]) (sym PNat [])) (sym instPNatAdd []))) (bv 0)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym PNat [])) (lit NAT 1)) (ap (ap (sym instOfNatPNatOfNeZeroNat []) (lit NAT 1)) (ap (sym NeZero.succ []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 0)) (ap (sym instOfNatNat []) (lit NAT 0)))))))))) (pi EXPLICIT (ap (sym Not []) (ap (fv bf0) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym PNat [])) (lit NAT 1)) (ap (ap (sym instOfNatPNatOfNeZeroNat []) (lit NAT 1)) (ap (sym NeZero.succ []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 0)) (ap (sym instOfNatNat []) (lit NAT 0)))))))) (ap (ap (ap (sym Eq [us(u0)]) (sym PNat [])) (ap (ap (ap (sym PNat.find []) (fv bf0)) (fv bf2)) (bv 2))) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym instHAdd [u0]) (sym PNat [])) (sym instPNatAd
... [33181 more characters]
```

### FINALIST R_28b291b5ebe6

*18,341 characters*

```text
meta
  summary ;; theorem-> PNat.find_comp_succ ;; file-> Mathlib/Data/PNat/Find.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT PNat [] sym u0 sort pi
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT PNat [] sym u0 sort pi
  decl f2 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> DecidablePred [us(u0)] sym PNat [] sym ap f0 fv ap
  decl f3 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> DecidablePred [us(u0)] sym PNat [] sym ap f1 fv ap
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym f0 fv 0 bv ap lam ap
  decl f5 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> PNat [] sym
  decl f6 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> PNat [] sym
  decl f7 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym f0 fv 0 bv ap lam ap EXPLICIT Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym f0 fv HAdd.hAdd [u0 u0 u0] sym PNat [] sym ap PNat [] sym ap PNat [] sym 
... [17141 more characters]
```

## Example 15 — `Mathlib/Algebra/Group/Subsemigroup/Membership.lean::Subsemigroup.iSup_induction::3`

**Shape:** 1 goal(s), 16 local declaration(s), 0 external premise(s). Domain `Algebra`.

### SEED_LEAN_LIKE

*7,874 characters*

```text
#
  Y
    TH: Subsemigroup.iSup_induction
    FL: Mathlib/Algebra/Group/Subsemigroup/Membership.lean
Σ₀
  D ι~bf0
    n: ι
    b: IMPLICIT
    d: cdecl
    ∈: sort(up(u_1))
  D M~bf1
    n: M
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_2)))
  D A~bf2
    n: A
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_3)))
  D B~bf3
    n: B
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_4)))
  D inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4
    n: inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(Mul,[up(u_2)]),fv(M~bf1))
  D iSup_induction~bf5
    n: iSup_induction
    b: EXPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,pi(EXPLICIT,fv(ι~bf0),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4))),pi(IMPLICIT,pi(EXPLICIT,fv(M~bf1),sort(u0)),pi(IMPLICIT,fv(M~bf1),pi(EXPLICIT,ap(ap(ap(ap(ap(sym(Membership.mem,[up(u_2) up(u_2)]),fv(M~bf1)),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4))),ap(ap(ap(sym(SetLike.instMembership,[up(u_2) up(u_2)]),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf
... [6674 more characters]
```

### SEED_PRIOR_HML

*6,738 characters*

```text
meta
  summary
    theorem: Subsemigroup.iSup_induction
    file: Mathlib/Algebra/Group/Subsemigroup/Membership.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort up(u_1))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_2)))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_3)))
  decl bf3
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_4)))
  decl bf4
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Mul [up(u_2)]) (fv bf1))
  decl bf5
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi EXPLICIT (pi EXPLICIT (fv bf0) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (pi IMPLICIT (pi EXPLICIT (fv bf1) (sort u0)) (pi IMPLICIT (fv bf1) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_2) up(u_2)]) (fv bf1)) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (ap (ap (ap (sym SetLike.instMembership [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4)))) (bv 0)
... [5538 more characters]
```

### SEED_STRUCTURED_ENGLISH

*9,062 characters*

```text
In meta:
  summary has theorem is Subsemigroup.iSup_induction; and file is Mathlib/Algebra/Group/Subsemigroup/Membership.lean .
In state_before:
  decl ι~bf0 has display is ι; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(up(u_1)) .
  decl M~bf1 has display is M; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_2))) .
  decl A~bf2 has display is A; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_3))) .
  decl B~bf3 has display is B; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_4))) .
  decl inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4 has display is inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(Mul,[up(u_2)]),fv(M~bf1)) .
  decl iSup_induction~bf5 has display is iSup_induction; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,pi(EXPLICIT,fv(ι~bf0),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4))),pi(IMPLICIT,pi(EX
... [7862 more characters]
```

### SEED_TYPED_AST

*6,140 characters*

```text
mta
  - smy
    thm: Subsemigroup.iSup_induction
    fl: Mathlib/Algebra/Group/Subsemigroup/Membership.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|up{u_1}}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_2}}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_3}}}
  - dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_4}}}
  - dc bf4
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Mul,[up{u_2}]},{fv|bf1}}
  - dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: {pi|EXPLICIT,{pi|EXPLICIT,{fv|bf0},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{pi|IMPLICIT,{pi|EXPLICIT,{fv|bf1},{sort|u0}},{pi|IMPLICIT,{fv|bf1},{pi|EXPLICIT,{ap|{ap|{ap|{ap|{ap|{sym|Membership.mem,[up{u_2} up{u_2}]},{fv|bf1}},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{ap|{ap|{ap|{sym|SetLike.instMembership,[up{u_2} up{u_2}]},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{fv|bf1}},{ap|{ap|{sym|Subsemigroup.instSetLike,[up{u_2}]},{fv|bf1}},{fv|bf4}}}},{bv|0}},{ap|{ap|{ap|{ap|{sym|iSup,[up{u_2} up{u_1}]},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{fv|bf0}},{ap|{ap|{sym|CompleteLattice.toSupSet,[up{u_2}]},{ap|{
... [4940 more characters]
```

### FINALIST R_5b2eb732ac8b

*5,281 characters*

```text
#
  Y
    TH: Subsemigroup.iSup_induction
    FL: Mathlib/Algebra/Group/Subsemigroup/Membership.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: []
    L: [Mathlib/Algebra/Group/Subsemigroup/Membership.lean::Subsemigroup.iSup_induction::3:before:local:f10,Mathlib/Algebra/Group/Subsemigroup/Membership.lean::Subsemigroup.iSup_induction::3:before:local:f15]
Σ₀
  □ bm2
    ⊢: bf7 fv bf12 fv ap
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15]
  A bf12
    tg: metavariable_reference
  A bf7
    tg: dependent_function
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: up(u_1) sort
  D bf1
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_2)) sort
  D bf2
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_3)) sort
  D bf3
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_4)) sort
  D bf4
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: Mul [up(u_2)] sym bf1 fv ap
  D bf5
    b: EXPLICIT
    d: cdecl
    ∈: EXPLICIT EXPLICIT bf0 fv Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap pi IMPLICIT EXPLICIT bf1 fv u0 sort pi IMPLICIT bf1 fv EXPLICIT Membership.mem [up(u_2) up(u_2)] sym bf1 fv ap Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv
... [4081 more characters]
```

### FINALIST R_000441b08de4

*5,316 characters*

```text
mta
  smy ;; thm: Subsemigroup.iSup_induction ;; fl: Mathlib/Algebra/Group/Subsemigroup/Membership.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: up(u_1) sort
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_2)) sort
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_3)) sort
  dc bf3 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_4)) sort
  dc bf4 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Mul [up(u_2)] sym bf1 fv ap
  dc bf5 ;; br: EXPLICIT ;; dr: cdecl ;; ty: EXPLICIT EXPLICIT bf0 fv Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap pi IMPLICIT EXPLICIT bf1 fv u0 sort pi IMPLICIT bf1 fv EXPLICIT Membership.mem [up(u_2) up(u_2)] sym bf1 fv ap Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap ap SetLike.instMembership [up(u_2) up(u_2)] sym Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap ap bf1 fv ap Subsemigroup.instSetLike [up(u_2)] sym bf1 fv ap bf4 fv ap ap ap 0 bv ap iSup [up(u_2) up(u_1)] sym Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap ap bf0 fv ap CompleteLattice.toSupSet [up(u_2)] sym Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap ap Subsemigroup.instCompleteLattice [up(u_2)] sym bf1 fv ap bf4 fv ap ap ap EXPLICIT bf0 fv 3 bv 0 bv ap lam ap ap EXPLICIT EXPLICIT bf0 f
... [4116 more characters]
```

### FINALIST R_01d4e489af53

*5,769 characters*

```text
(mta
  (smy (thm Subsemigroup.iSup_induction) (fl Mathlib/Algebra/Group/Subsemigroup/Membership.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort up(u_1))))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_3)))))
  (dc f3 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_4)))))
  (dc f4 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Mul [up(u_2)]) (fv f1))))
  (dc f5 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (pi EXPLICIT (fv f0) (ap (ap (sym Subsemigroup [up(u_2)]) (fv f1)) (fv f4))) (pi IMPLICIT (pi EXPLICIT (fv f1) (sort u0)) (pi IMPLICIT (fv f1) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_2) up(u_2)]) (fv f1)) (ap (ap (sym Subsemigroup [up(u_2)]) (fv f1)) (fv f4))) (ap (ap (ap (sym SetLike.instMembership [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv f1)) (fv f4))) (fv f1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv f1)) (fv f4)))) (bv 0)) (ap (ap (ap (ap (sym iSup [up(u_2) up(u_1)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv f1)) (fv f4))) (fv f0)) (ap (ap (sym CompleteLattice.toSupSet [up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv f1)) (fv f4))) (ap (ap (sym Subsemigroup.inst
... [4569 more characters]
```

### FINALIST R_101e806690b0

*8,584 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (sym Set.iUnion [up(u_2) up(u_1)]) (fv bf1)) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (ap (ap (sym SetLike.coe [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4))) (ap (fv bf6) (bv 0)))))
  A $a1
    t-> (ap (ap (ap (ap (sym Membership.mem [up(u_2) up(u_2)]) (fv bf1)) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (ap (ap (ap (sym SetLike.instMembership [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4)))) (bv 0))
  A $a2
    t-> (ap (ap (ap (sym Membership.mem [up(u_2) up(u_2)]) (fv bf1)) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (ap (ap (ap (sym SetLike.instMembership [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4))))
  A $a3
    t-> (lam EXPLICIT (fv bf0) (ap (ap (ap (ap (sym SetLike.coe [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up
... [7384 more characters]
```

### FINALIST R_28b291b5ebe6

*7,405 characters*

```text
meta
  summary ;; theorem-> Subsemigroup.iSup_induction ;; file-> Mathlib/Algebra/Group/Subsemigroup/Membership.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> up(u_1) sort
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_2)) sort
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_3)) sort
  decl f3 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_4)) sort
  decl f4 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> Mul [up(u_2)] sym f1 fv ap
  decl f5 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> EXPLICIT EXPLICIT f0 fv Subsemigroup [up(u_2)] sym f1 fv ap f4 fv ap pi IMPLICIT EXPLICIT f1 fv u0 sort pi IMPLICIT f1 fv EXPLICIT Membership.mem [up(u_2) up(u_2)] sym f1 fv ap Subsemigroup [up(u_2)] sym f1 fv ap f4 fv ap ap SetLike.instMembership [up(u_2) up(u_2)] sym Subsemigroup [up(u_2)] sym f1 fv ap f4 fv ap ap f1 fv ap Subsemigroup.instSetLike [up(u_2)] sym f1 fv ap f4 fv ap ap ap 0 bv ap iSup [up(u_2) up(u_1)] sym Subsemigroup [up(u_2)] sym f1 fv ap f4 fv ap ap f0 fv ap CompleteLattice.toSupSet [up(u_2)] sym Subse
... [6205 more characters]
```

## Example 16 — `Mathlib/Analysis/Distribution/SchwartzSpace.lean::SchwartzMap.isBigO_cocompact_zpow_neg_nat::4`

**Shape:** 1 goal(s), 17 local declaration(s), 2 external premise(s). Domain `Analysis`.

### SEED_LEAN_LIKE

*20,913 characters*

```text
#
  Y
    TH: SchwartzMap.isBigO_cocompact_zpow_neg_nat
    FL: Mathlib/Analysis/Distribution/SchwartzSpace.lean
Σ₀
  D 𝕜~bf0
    n: 𝕜
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D 𝕜'~bf1
    n: 𝕜'
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_2)))
  D D~bf2
    n: D
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_3)))
  D E~bf3
    n: E
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_4)))
  D F~bf4
    n: F
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_5)))
  D G~bf5
    n: G
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_6)))
  D V~bf6
    n: V
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_7)))
  D inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1295~bf7
    n: inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1295
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(NormedAddCommGroup,[up(u_4)]),fv(E~bf3))
  D inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1298~bf8
    n: inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1298
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(ap(ap(ap(sym(NormedSpace,[u0 up(u_4)]),sym(Real,[])),fv(E~bf3)),sym(Real.normedField,[])),ap(ap(sym(NormedAddCommGroup.toSeminormedAddCommGroup,[up(u_4)
... [19713 more characters]
```

### SEED_PRIOR_HML

*16,091 characters*

```text
meta
  summary
    theorem: SchwartzMap.isBigO_cocompact_zpow_neg_nat
    file: Mathlib/Analysis/Distribution/SchwartzSpace.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_2)))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_3)))
  decl bf3
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_4)))
  decl bf4
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_5)))
  decl bf5
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_6)))
  decl bf6
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_7)))
  decl bf7
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym NormedAddCommGroup [up(u_4)]) (fv bf3))
  decl bf8
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (sym NormedSpace [u0 up(u_4)]) (sym Real [])) (fv bf3)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf
... [14891 more characters]
```

### SEED_STRUCTURED_ENGLISH

*23,414 characters*

```text
In meta:
  summary has theorem is SchwartzMap.isBigO_cocompact_zpow_neg_nat; and file is Mathlib/Analysis/Distribution/SchwartzSpace.lean .
In state_before:
  decl 𝕜~bf0 has display is 𝕜; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl 𝕜'~bf1 has display is 𝕜'; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_2))) .
  decl D~bf2 has display is D; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_3))) .
  decl E~bf3 has display is E; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_4))) .
  decl F~bf4 has display is F; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_5))) .
  decl G~bf5 has display is G; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_6))) .
  decl V~bf6 has display is V; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_7))) .
  decl inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1295~bf7 has display is inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1295; and binder_role is INSTANCE_I
... [22214 more characters]
```

### SEED_TYPED_AST

*14,873 characters*

```text
mta
  - smy
    thm: SchwartzMap.isBigO_cocompact_zpow_neg_nat
    fl: Mathlib/Analysis/Distribution/SchwartzSpace.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_2}}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_3}}}
  - dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_4}}}
  - dc bf4
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_5}}}
  - dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_6}}}
  - dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_7}}}
  - dc bf7
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|NormedAddCommGroup,[up{u_4}]},{fv|bf3}}
  - dc bf8
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|NormedSpace,[u0 up{u_4}]},{sym|Real,[]}},{fv|bf3}},{sym|Real.normedField,[]}},{ap|{ap|{sym|NormedAddCommGroup.toSeminormedAddCommGroup,[up{u_4}]},{fv|bf3}},{fv|bf7}}}
  - dc bf9
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|NormedAddCommGroup,[up{u_5}]},{fv|bf4}}
  - dc bf10
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|NormedSpace,[u0 up{u_5}]},{sym|Real,[]}},{fv|bf4}}
... [13673 more characters]
```

### FINALIST R_5b2eb732ac8b

*12,622 characters*

```text
#
  Y
    TH: SchwartzMap.isBigO_cocompact_zpow_neg_nat
    FL: Mathlib/Analysis/Distribution/SchwartzSpace.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [Filter.Eventually.mono,Filter.eventually_cofinite_ne]
    L: [Mathlib/Analysis/Distribution/SchwartzSpace.lean::SchwartzMap.isBigO_cocompact_zpow_neg_nat::4:before:local:f3]
Σ₀
  □ bm3
    ⊢: Filter.Eventually [um(u0)] sym bm0 mv ap EXPLICIT bm0 mv bm2 mv 0 bv ap lam ap bm1 mv ap
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15,bf16]
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_1)) sort
  D bf1
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_2)) sort
  D bf2
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_3)) sort
  D bf3
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_4)) sort
  D bf4
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_5)) sort
  D bf5
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_6)) sort
  D bf6
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_7)) sort
  D bf7
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: NormedAddCommGroup [up(u_4)] sym bf3 fv ap
  D bf8
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: NormedSpace [u0 up(u_4)] sym Real [] sy
... [11422 more characters]
```

### FINALIST R_000441b08de4

*12,708 characters*

```text
mta
  smy ;; thm: SchwartzMap.isBigO_cocompact_zpow_neg_nat ;; fl: Mathlib/Analysis/Distribution/SchwartzSpace.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_2)) sort
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_3)) sort
  dc bf3 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_4)) sort
  dc bf4 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_5)) sort
  dc bf5 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_6)) sort
  dc bf6 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_7)) sort
  dc bf7 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedAddCommGroup [up(u_4)] sym bf3 fv ap
  dc bf8 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedSpace [u0 up(u_4)] sym Real [] sym ap bf3 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)] sym bf3 fv ap bf7 fv ap ap
  dc bf9 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedAddCommGroup [up(u_5)] sym bf4 fv ap
  dc bf10 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedSpace [u0 up(u_5)] sym Real [] sym ap bf4 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_5)] sym bf4 fv ap bf9 fv ap ap
  dc bf11 ;; br: EXP
... [11508 more characters]
```

### FINALIST R_01d4e489af53

*14,050 characters*

```text
(mta
  (smy (thm SchwartzMap.isBigO_cocompact_zpow_neg_nat) (fl Mathlib/Analysis/Distribution/SchwartzSpace.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_3)))))
  (dc f3 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_4)))))
  (dc f4 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_5)))))
  (dc f5 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_6)))))
  (dc f6 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_7)))))
  (dc f7 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_4)]) (fv f3))))
  (dc f8 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_4)]) (sym Real [])) (fv f3)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv f3)) (fv f7)))))
  (dc f9 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_5)]) (fv f4))))
  (dc f10 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_5)]) (sym Real [])) (fv f4)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_5)]) (fv f4)) (fv f9)))))
  (
... [12850 more characters]
```

### FINALIST R_101e806690b0

*36,214 characters*

```text
$
  A $a0
    t-> (pi EXPLICIT (sym Nat []) (ap (ap (ap (ap (ap (ap (ap (ap (sym Asymptotics.IsBigO [up(u_4) up(u_5) u0]) (fv bf3)) (fv bf4)) (sym Real [])) (ap (ap (sym NormedAddCommGroup.toNorm [up(u_5)]) (fv bf4)) (fv bf9))) (sym Real.norm [])) (ap (ap (sym Filter.cocompact [up(u_4)]) (fv bf3)) (ap (ap (sym UniformSpace.toTopologicalSpace [up(u_4)]) (fv bf3)) (ap (ap (sym PseudoMetricSpace.toUniformSpace [up(u_4)]) (fv bf3)) (ap (ap (sym SeminormedAddCommGroup.toPseudoMetricSpace [up(u_4)]) (fv bf3)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7))))))) (ap (ap (ap (ap (ap (sym DFunLike.coe [umax(us(up(u_4)) us(up(u_5))) us(up(u_4)) us(up(u_5))]) (ap (ap (ap (ap (ap (ap (sym SchwartzMap [up(u_4) up(u_5)]) (fv bf3)) (fv bf4)) (fv bf7)) (fv bf8)) (fv bf9)) (fv bf10))) (fv bf3)) (lam EXPLICIT (fv bf3) (fv bf4))) (ap (ap (ap (ap (ap (ap (sym SchwartzMap.instFunLike [up(u_4) up(u_5)]) (fv bf3)) (fv bf4)) (fv bf7)) (fv bf8)) (fv bf9)) (fv bf10))) (fv bf11))) (lam EXPLICIT (fv bf3) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [u0 u0 u0]) (sym Real [])) (sym Int [])) (sym Real [])) (ap (ap (ap (sym instHPow [u0 u0]) (sym Real [])) (sym Int [])) (ap (ap (
... [35014 more characters]
```

### FINALIST R_28b291b5ebe6

*17,046 characters*

```text
meta
  summary ;; theorem-> SchwartzMap.isBigO_cocompact_zpow_neg_nat ;; file-> Mathlib/Analysis/Distribution/SchwartzSpace.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_2)) sort
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_3)) sort
  decl f3 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_4)) sort
  decl f4 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_5)) sort
  decl f5 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_6)) sort
  decl f6 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_7)) sort
  decl f7 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> NormedAddCommGroup [up(u_4)] sym f3 fv ap
  decl f8 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> NormedSpace [u0 up(u_4)] sym Real [] sym ap f3 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)] sym f3 fv ap f7 fv ap ap
  decl f9 ;; binder_role-> INSTANCE_IMPLICIT ;; declar
... [15846 more characters]
```

## Example 17 — `Mathlib/CategoryTheory/Sites/Sieves.lean::CategoryTheory.Sieve.mem_ofArrows_iff::1`

**Shape:** 1 goal(s), 18 local declaration(s), 0 external premise(s). Domain `CategoryTheory`.

### SEED_LEAN_LIKE

*18,083 characters*

```text
#
  Y
    TH: CategoryTheory.Sieve.mem_ofArrows_iff
    FL: Mathlib/CategoryTheory/Sites/Sieves.lean
Σ₀
  D C~bf0
    n: C
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u₁)))
  D inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4515~bf1
    n: inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4515
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(CategoryTheory.Category,[up(v₁) up(u₁)]),fv(C~bf0))
  D D~bf2
    n: D
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u₂)))
  D inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4519~bf3
    n: inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4519
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(CategoryTheory.Category,[up(v₂) up(u₂)]),fv(D~bf2))
  D F~bf4
    n: F
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(ap(ap(sym(CategoryTheory.Functor,[up(v₁) up(v₂) up(u₁) up(u₂)]),fv(C~bf0)),fv(inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4515~bf1)),fv(D~bf2)),fv(inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4519~bf3))
  D X~bf5
    n: X
    b: IMPLICIT
    d: cdecl
    ∈: fv(C~bf0)
  D Y~bf6
    n: Y
    b: IMPLICIT
    d: cdecl
    ∈: fv(C~bf0)
  D Z~bf7
    n: Z
    b: IMPLICIT
    d: cdecl
    ∈: fv(C~bf0)
  D f~bf8
    n: f
    b: EXPL
... [16883 more characters]
```

### SEED_PRIOR_HML

*16,351 characters*

```text
meta
  summary
    theorem: CategoryTheory.Sieve.mem_ofArrows_iff
    file: Mathlib/CategoryTheory/Sites/Sieves.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u₁)))
  decl bf1
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym CategoryTheory.Category [up(v₁) up(u₁)]) (fv bf0))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u₂)))
  decl bf3
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym CategoryTheory.Category [up(v₂) up(u₂)]) (fv bf2))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (sym CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))
  decl bf5
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (fv bf0)
  decl bf6
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (fv bf0)
  decl bf7
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (fv bf0)
  decl bf8
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym Cat
... [15151 more characters]
```

### SEED_STRUCTURED_ENGLISH

*20,418 characters*

```text
In meta:
  summary has theorem is CategoryTheory.Sieve.mem_ofArrows_iff; and file is Mathlib/CategoryTheory/Sites/Sieves.lean .
In state_before:
  decl C~bf0 has display is C; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u₁))) .
  decl inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4515~bf1 has display is inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4515; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(CategoryTheory.Category,[up(v₁) up(u₁)]),fv(C~bf0)) .
  decl D~bf2 has display is D; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u₂))) .
  decl inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4519~bf3 has display is inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4519; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(CategoryTheory.Category,[up(v₂) up(u₂)]),fv(D~bf2)) .
  decl F~bf4 has display is F; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(ap(sym(CategoryTheory.Functor,[up(v₁) up(v₂) up(u₁) up(u₂)]),fv(C~bf0)),fv(inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4515~bf1)),fv(D~bf2))
... [19218 more characters]
```

### SEED_TYPED_AST

*15,188 characters*

```text
mta
  - smy
    thm: CategoryTheory.Sieve.mem_ofArrows_iff
    fl: Mathlib/CategoryTheory/Sites/Sieves.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u₁}}}
  - dc bf1
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|CategoryTheory.Category,[up{v₁} up{u₁}]},{fv|bf0}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u₂}}}
  - dc bf3
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|CategoryTheory.Category,[up{v₂} up{u₂}]},{fv|bf2}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|CategoryTheory.Functor,[up{v₁} up{v₂} up{u₁} up{u₂}]},{fv|bf0}},{fv|bf1}},{fv|bf2}},{fv|bf3}}
  - dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: {fv|bf0}
  - dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: {fv|bf0}
  - dc bf7
    br: IMPLICIT
    dr: cdecl
    ty: {fv|bf0}
  - dc bf8
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|Quiver.Hom,[us{up{v₁}} up{u₁}]},{fv|bf0}},{ap|{ap|{sym|CategoryTheory.CategoryStruct.toQuiver,[up{v₁} up{u₁}]},{fv|bf0}},{ap|{ap|{sym|CategoryTheory.Category.toCategoryStruct,[up{v₁} up{u₁}]},{fv|bf0}},{fv|bf1}}}},{fv|bf6}},{fv|bf5}}
  - dc bf9
    br: IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{sym|C
... [13988 more characters]
```

### FINALIST R_5b2eb732ac8b

*13,369 characters*

```text
#
  Y
    TH: CategoryTheory.Sieve.mem_ofArrows_iff
    FL: Mathlib/CategoryTheory/Sites/Sieves.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: []
    L: []
Σ₀
  □ bm2
    ⊢: EXPLICIT bm0 mv bm1 mv pi
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15,bf16,bf17]
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u₁)) sort
  D bf1
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: CategoryTheory.Category [up(v₁) up(u₁)] sym bf0 fv ap
  D bf2
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u₂)) sort
  D bf3
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: CategoryTheory.Category [up(v₂) up(u₂)] sym bf2 fv ap
  D bf4
    b: EXPLICIT
    d: cdecl
    ∈: CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap
  D bf5
    b: IMPLICIT
    d: cdecl
    ∈: bf0 fv
  D bf6
    b: IMPLICIT
    d: cdecl
    ∈: bf0 fv
  D bf7
    b: IMPLICIT
    d: cdecl
    ∈: bf0 fv
  D bf8
    b: EXPLICIT
    d: cdecl
    ∈: Quiver.Hom [us(up(v₁)) up(u₁)] sym bf0 fv ap CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)] sym bf0 fv ap CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)] sym 
... [12169 more characters]
```

### FINALIST R_000441b08de4

*13,148 characters*

```text
mta
  smy ;; thm: CategoryTheory.Sieve.mem_ofArrows_iff ;; fl: Mathlib/CategoryTheory/Sites/Sieves.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u₁)) sort
  dc bf1 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: CategoryTheory.Category [up(v₁) up(u₁)] sym bf0 fv ap
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u₂)) sort
  dc bf3 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: CategoryTheory.Category [up(v₂) up(u₂)] sym bf2 fv ap
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap
  dc bf5 ;; br: IMPLICIT ;; dr: cdecl ;; ty: bf0 fv
  dc bf6 ;; br: IMPLICIT ;; dr: cdecl ;; ty: bf0 fv
  dc bf7 ;; br: IMPLICIT ;; dr: cdecl ;; ty: bf0 fv
  dc bf8 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Quiver.Hom [us(up(v₁)) up(u₁)] sym bf0 fv ap CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)] sym bf0 fv ap CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)] sym bf0 fv ap bf1 fv ap ap ap bf6 fv ap bf5 fv ap
  dc bf9 ;; br: IMPLICIT ;; dr: cdecl ;; ty: CategoryTheory.Sieve [up(v₁) up(u₁)] sym bf0 fv ap bf1 fv ap bf5 fv ap
  dc bf10 ;; br: IMPLICIT ;; dr: cdecl ;; ty: CategoryTheory.Sieve [up(v₁) 
... [11948 more characters]
```

### FINALIST R_01d4e489af53

*14,419 characters*

```text
(mta
  (smy (thm CategoryTheory.Sieve.mem_ofArrows_iff) (fl Mathlib/CategoryTheory/Sites/Sieves.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u₁)))))
  (dc f1 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CategoryTheory.Category [up(v₁) up(u₁)]) (fv f0))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u₂)))))
  (dc f3 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CategoryTheory.Category [up(v₂) up(u₂)]) (fv f2))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)]) (fv f0)) (fv f1)) (fv f2)) (fv f3))))
  (dc f5 (br IMPLICIT) (dr cdecl) (ty (fv f0)))
  (dc f6 (br IMPLICIT) (dr cdecl) (ty (fv f0)))
  (dc f7 (br IMPLICIT) (dr cdecl) (ty (fv f0)))
  (dc f8 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv f0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)]) (fv f0)) (ap (ap (sym CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)]) (fv f0)) (fv f1)))) (fv f6)) (fv f5))))
  (dc f9 (br IMPLICIT) (dr cdecl) (ty (ap (ap (ap (sym CategoryTheory.Sieve [up(v₁) up(u₁)]) (fv f0)) (fv f1)) (fv f5))))
  (dc f10 (br IMPLICIT) (dr cdecl) (ty (ap (ap (ap (s
... [13219 more characters]
```

### FINALIST R_101e806690b0

*46,079 characters*

```text
$
  A $a0
    t-> (pi IMPLICIT (sort us(up(u_1))) (pi IMPLICIT (fv bf0) (pi EXPLICIT (pi EXPLICIT (bv 1) (fv bf0)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)))) (ap (bv 1) (bv 0))) (bv 2))) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)))) (bv 0)) (bv 3)) (ap (ap (sym Iff []) (ap (ap (ap (ap (ap (ap (sym CategoryTheory.Sieve.arrows [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)) (bv 4)) (ap (ap (ap (ap (ap (ap (sym CategoryTheory.Sieve.ofArrows [up(v₁) up(u₁) up(u_1)]) (fv bf0)) (fv bf1)) (bv 5)) (bv 4)) (bv 3)) (bv 2))) (bv 1)) (bv 0))) (ap (ap (sym Exists [us(up(u_1))]) (bv 5)) (lam EXPLICIT (bv 5) (ap (ap (sym Exists [us(up(v₁))]) (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u
... [44879 more characters]
```

### FINALIST R_28b291b5ebe6

*18,036 characters*

```text
meta
  summary ;; theorem-> CategoryTheory.Sieve.mem_ofArrows_iff ;; file-> Mathlib/CategoryTheory/Sites/Sieves.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u₁)) sort
  decl f1 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> CategoryTheory.Category [up(v₁) up(u₁)] sym f0 fv ap
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u₂)) sort
  decl f3 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> CategoryTheory.Category [up(v₂) up(u₂)] sym f2 fv ap
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)] sym f0 fv ap f1 fv ap f2 fv ap f3 fv ap
  decl f5 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> f0 fv
  decl f6 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> f0 fv
  decl f7 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> f0 fv
  decl f8 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Quiver.Hom [us(up(v₁)) up(u₁)] sym f0 fv ap CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)] sym f0 fv ap CategoryTheory.Category.t
... [16836 more characters]
```

## Example 18 — `Mathlib/NumberTheory/Cyclotomic/Basic.lean::IsCyclotomicExtension.of_union_of_dvd::1`

**Shape:** 1 goal(s), 19 local declaration(s), 2 external premise(s). Domain `NumberTheory`.

### SEED_LEAN_LIKE

*14,781 characters*

```text
#
  Y
    TH: IsCyclotomicExtension.of_union_of_dvd
    FL: Mathlib/NumberTheory/Cyclotomic/Basic.lean
Σ₀
  D n~bf0
    n: n
    b: IMPLICIT
    d: cdecl
    ∈: sym(PNat,[])
  D S~bf1
    n: S
    b: IMPLICIT
    d: cdecl
    ∈: ap(sym(Set,[u0]),sym(PNat,[]))
  D T~bf2
    n: T
    b: EXPLICIT
    d: cdecl
    ∈: ap(sym(Set,[u0]),sym(PNat,[]))
  D A~bf3
    n: A
    b: EXPLICIT
    d: cdecl
    ∈: sort(us(up(u)))
  D B~bf4
    n: B
    b: EXPLICIT
    d: cdecl
    ∈: sort(us(up(v)))
  D K~bf5
    n: K
    b: EXPLICIT
    d: cdecl
    ∈: sort(us(up(w)))
  D L~bf6
    n: L
    b: EXPLICIT
    d: cdecl
    ∈: sort(us(up(z)))
  D inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2374~bf7
    n: inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2374
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(CommRing,[up(u)]),fv(A~bf3))
  D inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2377~bf8
    n: inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2377
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(CommRing,[up(v)]),fv(B~bf4))
  D inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2380~bf9
    n: inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2380
    b: INSTANCE_IMPLICIT
  
... [13581 more characters]
```

### SEED_PRIOR_HML

*12,548 characters*

```text
meta
  summary
    theorem: IsCyclotomicExtension.of_union_of_dvd
    file: Mathlib/NumberTheory/Cyclotomic/Basic.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sym PNat [])
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Set [u0]) (sym PNat []))
  decl bf2
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (sym Set [u0]) (sym PNat []))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sort us(up(u)))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sort us(up(v)))
  decl bf5
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sort us(up(w)))
  decl bf6
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (sort us(up(z)))
  decl bf7
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym CommRing [up(u)]) (fv bf3))
  decl bf8
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym CommRing [up(v)]) (fv bf4))
  decl bf9
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (sym Algebra [up(u) up(v)]) (fv bf3)) (fv bf4)) (ap
... [11348 more characters]
```

### SEED_STRUCTURED_ENGLISH

*17,154 characters*

```text
In meta:
  summary has theorem is IsCyclotomicExtension.of_union_of_dvd; and file is Mathlib/NumberTheory/Cyclotomic/Basic.lean .
In state_before:
  decl n~bf0 has display is n; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(PNat,[]) .
  decl S~bf1 has display is S; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is ap(sym(Set,[u0]),sym(PNat,[])) .
  decl T~bf2 has display is T; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(sym(Set,[u0]),sym(PNat,[])) .
  decl A~bf3 has display is A; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sort(us(up(u))) .
  decl B~bf4 has display is B; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sort(us(up(v))) .
  decl K~bf5 has display is K; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sort(us(up(w))) .
  decl L~bf6 has display is L; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is sort(us(up(z))) .
  decl inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2374~bf7 has display is inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2374; and binder_role is INSTANCE_IMPLICIT; an
... [15954 more characters]
```

### SEED_TYPED_AST

*11,370 characters*

```text
mta
  - smy
    thm: IsCyclotomicExtension.of_union_of_dvd
    fl: Mathlib/NumberTheory/Cyclotomic/Basic.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sym|PNat,[]}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Set,[u0]},{sym|PNat,[]}}
  - dc bf2
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{sym|Set,[u0]},{sym|PNat,[]}}
  - dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: {sort|us{up{u}}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {sort|us{up{v}}}
  - dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: {sort|us{up{w}}}
  - dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: {sort|us{up{z}}}
  - dc bf7
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|CommRing,[up{u}]},{fv|bf3}}
  - dc bf8
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|CommRing,[up{v}]},{fv|bf4}}
  - dc bf9
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|Algebra,[up{u} up{v}]},{fv|bf3}},{fv|bf4}},{ap|{ap|{sym|CommRing.toCommSemiring,[up{u}]},{fv|bf3}},{fv|bf7}}},{ap|{ap|{sym|CommSemiring.toSemiring,[up{v}]},{fv|bf4}},{ap|{ap|{sym|CommRing.toCommSemiring,[up{v}]},{fv|bf4}},{fv|bf8}}}}
  - dc bf10
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Field,[up{w}
... [10170 more characters]
```

### FINALIST R_5b2eb732ac8b

*9,899 characters*

```text
#
  Y
    TH: IsCyclotomicExtension.of_union_of_dvd
    FL: Mathlib/NumberTheory/Cyclotomic/Basic.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [Set.mem_singleton_iff,Set.mem_union]
    L: [Mathlib/NumberTheory/Cyclotomic/Basic.lean::IsCyclotomicExtension.of_union_of_dvd::1:before:local:f18]
Σ₀
  □ bm2
    ⊢: Exists [us(up(v))] sym bf4 fv ap EXPLICIT bf4 fv IsPrimitiveRoot [up(v)] sym bf4 fv ap CommRing.toCommMonoid [up(v)] sym bf4 fv ap bf8 fv ap ap 0 bv ap PNat.val [] sym bf17 fv ap ap lam ap
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15,bf16,bf17,bf18]
  A bf17
    tg: metavariable_reference
  A bf4
    tg: sort
  A bf8
    tg: CommRing
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: PNat [] sym
  D bf1
    b: IMPLICIT
    d: cdecl
    ∈: Set [u0] sym PNat [] sym ap
  D bf2
    b: EXPLICIT
    d: cdecl
    ∈: Set [u0] sym PNat [] sym ap
  D bf3
    b: EXPLICIT
    d: cdecl
    ∈: us(up(u)) sort
  D bf4
    b: EXPLICIT
    d: cdecl
    ∈: us(up(v)) sort
  D bf5
    b: EXPLICIT
    d: cdecl
    ∈: us(up(w)) sort
  D bf6
    b: EXPLICIT
    d: cdecl
    ∈: us(up(z)) sort
  D bf7
    b: INST
... [8699 more characters]
```

### FINALIST R_000441b08de4

*9,831 characters*

```text
mta
  smy ;; thm: IsCyclotomicExtension.of_union_of_dvd ;; fl: Mathlib/NumberTheory/Cyclotomic/Basic.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: PNat [] sym
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Set [u0] sym PNat [] sym ap
  dc bf2 ;; br: EXPLICIT ;; dr: cdecl ;; ty: Set [u0] sym PNat [] sym ap
  dc bf3 ;; br: EXPLICIT ;; dr: cdecl ;; ty: us(up(u)) sort
  dc bf4 ;; br: EXPLICIT ;; dr: cdecl ;; ty: us(up(v)) sort
  dc bf5 ;; br: EXPLICIT ;; dr: cdecl ;; ty: us(up(w)) sort
  dc bf6 ;; br: EXPLICIT ;; dr: cdecl ;; ty: us(up(z)) sort
  dc bf7 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: CommRing [up(u)] sym bf3 fv ap
  dc bf8 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: CommRing [up(v)] sym bf4 fv ap
  dc bf9 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Algebra [up(u) up(v)] sym bf3 fv ap bf4 fv ap CommRing.toCommSemiring [up(u)] sym bf3 fv ap bf7 fv ap ap CommSemiring.toSemiring [up(v)] sym bf4 fv ap CommRing.toCommSemiring [up(v)] sym bf4 fv ap bf8 fv ap ap ap
  dc bf10 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Field [up(w)] sym bf5 fv ap
  dc bf11 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Field [up(z)] sym bf6 fv ap
  dc bf12 ;; br: INSTANCE_IMPLICIT ;; dr: cde
... [8631 more characters]
```

### FINALIST R_01d4e489af53

*10,720 characters*

```text
(mta
  (smy (thm IsCyclotomicExtension.of_union_of_dvd) (fl Mathlib/NumberTheory/Cyclotomic/Basic.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sym PNat [])))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (ap (sym Set [u0]) (sym PNat []))))
  (dc f2 (br EXPLICIT) (dr cdecl) (ty (ap (sym Set [u0]) (sym PNat []))))
  (dc f3 (br EXPLICIT) (dr cdecl) (ty (sort us(up(u)))))
  (dc f4 (br EXPLICIT) (dr cdecl) (ty (sort us(up(v)))))
  (dc f5 (br EXPLICIT) (dr cdecl) (ty (sort us(up(w)))))
  (dc f6 (br EXPLICIT) (dr cdecl) (ty (sort us(up(z)))))
  (dc f7 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CommRing [up(u)]) (fv f3))))
  (dc f8 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CommRing [up(v)]) (fv f4))))
  (dc f9 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym Algebra [up(u) up(v)]) (fv f3)) (fv f4)) (ap (ap (sym CommRing.toCommSemiring [up(u)]) (fv f3)) (fv f7))) (ap (ap (sym CommSemiring.toSemiring [up(v)]) (fv f4)) (ap (ap (sym CommRing.toCommSemiring [up(v)]) (fv f4)) (fv f8))))))
  (dc f10 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Field [up(w)]) (fv f5))))
  (dc f11 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Field [up(z)]) (fv f6))))
  (dc f12 (br INSTANCE_IMP
... [9520 more characters]
```

### FINALIST R_101e806690b0

*22,363 characters*

```text
$
  A $a0
    t-> (pi EXPLICIT (pi EXPLICIT (sym PNat []) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [u0 u0]) (sym PNat [])) (ap (sym Set [u0]) (sym PNat []))) (ap (sym Set.instMembership [u0]) (sym PNat []))) (bv 0)) (fv bf1)) (ap (ap (ap (ap (sym Dvd.dvd [u0]) (sym PNat [])) (ap (ap (sym semigroupDvd [u0]) (sym PNat [])) (ap (ap (sym Monoid.toSemigroup [u0]) (sym PNat [])) (ap (ap (sym CommMonoid.toMonoid [u0]) (sym PNat [])) (ap (ap (sym OrderedCommMonoid.toCommMonoid [u0]) (sym PNat [])) (ap (ap (sym LinearOrderedCommMonoid.toOrderedCommMonoid [u0]) (sym PNat [])) (ap (ap (sym LinearOrderedCancelCommMonoid.toLinearOrderedCommMonoid [u0]) (sym PNat [])) (sym instPNatLinearOrderedCancelCommMonoid [])))))))) (fv bf0)) (bv 1)))) (pi EXPLICIT (ap (ap (sym Set.Nonempty [u0]) (sym PNat [])) (fv bf1)) (pi INSTANCE_IMPLICIT (ap (ap (ap (ap (ap (ap (sym IsCyclotomicExtension [up(u) up(v)]) (fv bf1)) (fv bf3)) (fv bf4)) (fv bf7)) (fv bf8)) (fv bf9)) (ap (ap (ap (ap (ap (ap (sym IsCyclotomicExtension [up(u) up(v)]) (ap (ap (ap (ap (sym Union.union [u0]) (ap (sym Set [u0]) (sym PNat []))) (ap (sym Set.instUnion [u0]) (sym PNat []))) (fv bf1)) (ap (ap (ap (ap (sym Singleton.singlet
... [21163 more characters]
```

### FINALIST R_28b291b5ebe6

*14,245 characters*

```text
meta
  summary ;; theorem-> IsCyclotomicExtension.of_union_of_dvd ;; file-> Mathlib/NumberTheory/Cyclotomic/Basic.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> PNat [] sym
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Set [u0] sym PNat [] sym ap
  decl f2 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> Set [u0] sym PNat [] sym ap
  decl f3 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u)) sort
  decl f4 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> us(up(v)) sort
  decl f5 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> us(up(w)) sort
  decl f6 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> us(up(z)) sort
  decl f7 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> CommRing [up(u)] sym f3 fv ap
  decl f8 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> CommRing [up(v)] sym f4 fv ap
  decl f9 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> Algebra [up(u) up(v)] sym f3 fv ap f4 fv ap CommRing.toCommSemiring [up(u)] sym f3 fv ap f7 fv ap ap CommSemiring
... [13045 more characters]
```

## Example 19 — `Mathlib/GroupTheory/Perm/Cycle/Basic.lean::Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order:`

**Shape:** 1 goal(s), 22 local declaration(s), 0 external premise(s). Domain `GroupTheory`.

### SEED_LEAN_LIKE

*17,402 characters*

```text
#
  Y
    TH: Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order
    FL: Mathlib/GroupTheory/Perm/Cycle/Basic.lean
Σ₀
  D ι~bf0
    n: ι
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D α~bf1
    n: α
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_2)))
  D β~bf2
    n: β
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_3)))
  D f~bf3
    n: f
    b: IMPLICIT
    d: cdecl
    ∈: ap(sym(Equiv.Perm,[us(up(u_2))]),fv(α~bf1))
  D g~bf4
    n: g
    b: IMPLICIT
    d: cdecl
    ∈: ap(sym(Equiv.Perm,[us(up(u_2))]),fv(α~bf1))
  D x~bf5
    n: x
    b: IMPLICIT
    d: cdecl
    ∈: fv(α~bf1)
  D y~bf6
    n: y
    b: IMPLICIT
    d: cdecl
    ∈: fv(α~bf1)
  D inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9904~bf7
    n: inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9904
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(DecidableEq,[us(up(u_2))]),fv(α~bf1))
  D inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9907~bf8
    n: inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9907
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(Fintype,[up(u_2)]),fv(α~bf1))
  D isCycle_pow_pos_of_lt_prime_order~bf9
    n: isCycle_pow_pos_of_lt_prime_order
    b: EXPLICIT
    d: cdecl
... [16202 more characters]
```

### SEED_PRIOR_HML

*17,683 characters*

```text
meta
  summary
    theorem: Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order
    file: Mathlib/GroupTheory/Perm/Cycle/Basic.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_2)))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_3)))
  decl bf3
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Equiv.Perm [us(up(u_2))]) (fv bf1))
  decl bf4
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Equiv.Perm [us(up(u_2))]) (fv bf1))
  decl bf5
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (fv bf1)
  decl bf6
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (fv bf1)
  decl bf7
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym DecidableEq [us(up(u_2))]) (fv bf1))
  decl bf8
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym Fintype [up(u_2)]) (fv bf1))
  decl bf9
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (pi INSTANCE_IMPLICIT (ap (sym Finite
... [16483 more characters]
```

### SEED_STRUCTURED_ENGLISH

*20,227 characters*

```text
In meta:
  summary has theorem is Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order; and file is Mathlib/GroupTheory/Perm/Cycle/Basic.lean .
In state_before:
  decl ι~bf0 has display is ι; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl α~bf1 has display is α; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_2))) .
  decl β~bf2 has display is β; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_3))) .
  decl f~bf3 has display is f; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is ap(sym(Equiv.Perm,[us(up(u_2))]),fv(α~bf1)) .
  decl g~bf4 has display is g; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is ap(sym(Equiv.Perm,[us(up(u_2))]),fv(α~bf1)) .
  decl x~bf5 has display is x; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is fv(α~bf1) .
  decl y~bf6 has display is y; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is fv(α~bf1) .
  decl inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9904~bf7 has display is inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9904; and b
... [19027 more characters]
```

### SEED_TYPED_AST

*16,295 characters*

```text
mta
  - smy
    thm: Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order
    fl: Mathlib/GroupTheory/Perm/Cycle/Basic.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_2}}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_3}}}
  - dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Equiv.Perm,[us{up{u_2}}]},{fv|bf1}}
  - dc bf4
    br: IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Equiv.Perm,[us{up{u_2}}]},{fv|bf1}}
  - dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: {fv|bf1}
  - dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: {fv|bf1}
  - dc bf7
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|DecidableEq,[us{up{u_2}}]},{fv|bf1}}
  - dc bf8
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Fintype,[up{u_2}]},{fv|bf1}}
  - dc bf9
    br: EXPLICIT
    dr: cdecl
    ty: {pi|INSTANCE_IMPLICIT,{ap|{sym|Finite,[us{up{u_3}}]},{fv|bf2}},{pi|IMPLICIT,{ap|{sym|Equiv.Perm,[us{up{u_3}}]},{fv|bf2}},{pi|EXPLICIT,{ap|{ap|{sym|Equiv.Perm.IsCycle,[up{u_3}]},{fv|bf2}},{bv|0}},{pi|EXPLICIT,{ap|{sym|Nat.Prime,[]},{ap|{ap|{ap|{sym|orderOf,[up{u_3}]},{ap|{sym|Equiv.Perm,[us{up{u_3}}]},{fv|
... [15095 more characters]
```

### FINALIST R_5b2eb732ac8b

*14,132 characters*

```text
#
  Y
    TH: Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order
    FL: Mathlib/GroupTheory/Perm/Cycle/Basic.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: []
    L: [Mathlib/GroupTheory/Perm/Cycle/Basic.lean::Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order::5:before:local:f20,Mathlib/GroupTheory/Perm/Cycle/Basic.lean::Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order::5:before:local:f21]
Σ₀
  □ bm4
    ⊢: Equiv.Perm.IsCycle [up(u_3)] sym bf2 fv ap HPow.hPow [up(u_3) u0 up(u_3)] sym Equiv.Perm [us(up(u_3))] sym bf2 fv ap ap Nat [] sym ap Equiv.Perm [us(up(u_3))] sym bf2 fv ap ap instHPow [up(u_3) u0] sym Equiv.Perm [us(up(u_3))] sym bf2 fv ap ap Nat [] sym ap Equiv.Perm.instPowNat [up(u_3)] sym bf2 fv ap ap ap bf11 fv ap bf14 fv ap ap ann
    Γ: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15,bf16,bf17,bf18,bf19,bf20,bf21]
  A bf11
    tg: Equiv.Perm
  A bf14
    tg: Nat
  A bf2
    tg: sort
  D bf0
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_1)) sort
  D bf1
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_2)) sort
  D bf2
    b: IMPLICIT
    d: cdecl
    ∈: us(up(u_3)) sort
  D bf3
    b:
... [12932 more characters]
```

### FINALIST R_000441b08de4

*14,156 characters*

```text
mta
  smy ;; thm: Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order ;; fl: Mathlib/GroupTheory/Perm/Cycle/Basic.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_2)) sort
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_3)) sort
  dc bf3 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Equiv.Perm [us(up(u_2))] sym bf1 fv ap
  dc bf4 ;; br: IMPLICIT ;; dr: cdecl ;; ty: Equiv.Perm [us(up(u_2))] sym bf1 fv ap
  dc bf5 ;; br: IMPLICIT ;; dr: cdecl ;; ty: bf1 fv
  dc bf6 ;; br: IMPLICIT ;; dr: cdecl ;; ty: bf1 fv
  dc bf7 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: DecidableEq [us(up(u_2))] sym bf1 fv ap
  dc bf8 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: Fintype [up(u_2)] sym bf1 fv ap
  dc bf9 ;; br: EXPLICIT ;; dr: cdecl ;; ty: INSTANCE_IMPLICIT Finite [us(up(u_3))] sym bf2 fv ap IMPLICIT Equiv.Perm [us(up(u_3))] sym bf2 fv ap EXPLICIT Equiv.Perm.IsCycle [up(u_3)] sym bf2 fv ap 0 bv ap EXPLICIT Nat.Prime [] sym orderOf [up(u_3)] sym Equiv.Perm [us(up(u_3))] sym bf2 fv ap ap DivInvMonoid.toMonoid [up(u_3)] sym Equiv.Perm [us(up(u_3))] sym bf2 fv ap ap Group.toDivInvMonoid [up(u_3)] sym Equiv.Perm [us(up(u_3))] sym b
... [12956 more characters]
```

### FINALIST R_01d4e489af53

*15,434 characters*

```text
(mta
  (smy (thm Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order) (fl Mathlib/GroupTheory/Perm/Cycle/Basic.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_3)))))
  (dc f3 (br IMPLICIT) (dr cdecl) (ty (ap (sym Equiv.Perm [us(up(u_2))]) (fv f1))))
  (dc f4 (br IMPLICIT) (dr cdecl) (ty (ap (sym Equiv.Perm [us(up(u_2))]) (fv f1))))
  (dc f5 (br IMPLICIT) (dr cdecl) (ty (fv f1)))
  (dc f6 (br IMPLICIT) (dr cdecl) (ty (fv f1)))
  (dc f7 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym DecidableEq [us(up(u_2))]) (fv f1))))
  (dc f8 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Fintype [up(u_2)]) (fv f1))))
  (dc f9 (br EXPLICIT) (dr cdecl) (ty (pi INSTANCE_IMPLICIT (ap (sym Finite [us(up(u_3))]) (fv f2)) (pi IMPLICIT (ap (sym Equiv.Perm [us(up(u_3))]) (fv f2)) (pi EXPLICIT (ap (ap (sym Equiv.Perm.IsCycle [up(u_3)]) (fv f2)) (bv 0)) (pi EXPLICIT (ap (sym Nat.Prime []) (ap (ap (ap (sym orderOf [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv f2))) (ap (ap (sym DivInvMonoid.toMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv f2))) (ap (ap (sym Gro
... [14234 more characters]
```

### FINALIST R_101e806690b0

*33,021 characters*

```text
$
  A $a0
    t-> (pi INSTANCE_IMPLICIT (ap (sym Finite [us(up(u_3))]) (fv bf2)) (pi IMPLICIT (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2)) (pi EXPLICIT (ap (ap (sym Equiv.Perm.IsCycle [up(u_3)]) (fv bf2)) (bv 0)) (pi EXPLICIT (ap (sym Nat.Prime []) (ap (ap (ap (sym orderOf [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym DivInvMonoid.toMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym Group.toDivInvMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (sym Equiv.Perm.permGroup [up(u_3)]) (fv bf2))))) (bv 1))) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (ap (ap (ap (ap (sym LT.lt [u0]) (sym Nat [])) (sym instLTNat [])) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 0)) (ap (sym instOfNatNat []) (lit NAT 0)))) (bv 0)) (pi EXPLICIT (ap (ap (ap (ap (sym LT.lt [u0]) (sym Nat [])) (sym instLTNat [])) (bv 1)) (ap (ap (ap (sym orderOf [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym DivInvMonoid.toMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym Group.toDivInvMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (sym Equiv.Perm.permGroup [up(u_3)]) (fv bf2)))))
... [31821 more characters]
```

### FINALIST R_28b291b5ebe6

*18,298 characters*

```text
meta
  summary ;; theorem-> Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order ;; file-> Mathlib/GroupTheory/Perm/Cycle/Basic.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_2)) sort
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_3)) sort
  decl f3 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Equiv.Perm [us(up(u_2))] sym f1 fv ap
  decl f4 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> Equiv.Perm [us(up(u_2))] sym f1 fv ap
  decl f5 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> f1 fv
  decl f6 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> f1 fv
  decl f7 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> DecidableEq [us(up(u_2))] sym f1 fv ap
  decl f8 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> Fintype [up(u_2)] sym f1 fv ap
  decl f9 ;; binder_role-> EXPLICIT ;; declaration_role-> cdecl ;; type-> INSTANCE_IMPLICIT Finite [us(up(u_3))] sym f2 fv ap IMPLICIT Equiv.Perm [us(up(u_3))] s
... [17098 more characters]
```

## Example 20 — `Mathlib/Analysis/Distribution/SchwartzSpace.lean::SchwartzMap.integrable_of_le_of_pow_mul_le::4`

**Shape:** 1 goal(s), 28 local declaration(s), 2 external premise(s). Domain `Analysis`.

### SEED_LEAN_LIKE

*20,908 characters*

```text
#
  Y
    TH: SchwartzMap.integrable_of_le_of_pow_mul_le
    FL: Mathlib/Analysis/Distribution/SchwartzSpace.lean
Σ₀
  D 𝕜~bf0
    n: 𝕜
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_1)))
  D 𝕜'~bf1
    n: 𝕜'
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_2)))
  D D~bf2
    n: D
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_3)))
  D E~bf3
    n: E
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_4)))
  D F~bf4
    n: F
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_5)))
  D G~bf5
    n: G
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_6)))
  D V~bf6
    n: V
    b: IMPLICIT
    d: cdecl
    ∈: sort(us(up(u_7)))
  D inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9986~bf7
    n: inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9986
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(sym(NormedAddCommGroup,[up(u_4)]),fv(E~bf3))
  D inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9989~bf8
    n: inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9989
    b: INSTANCE_IMPLICIT
    d: cdecl
    ∈: ap(ap(ap(ap(sym(NormedSpace,[u0 up(u_4)]),sym(Real,[])),fv(E~bf3)),sym(Real.normedField,[])),ap(ap(sym(NormedAddCommGroup.toSeminormedAddCommGroup,[up(u_4
... [19708 more characters]
```

### SEED_PRIOR_HML

*17,490 characters*

```text
meta
  summary
    theorem: SchwartzMap.integrable_of_le_of_pow_mul_le
    file: Mathlib/Analysis/Distribution/SchwartzSpace.lean
state_before
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_2)))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_3)))
  decl bf3
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_4)))
  decl bf4
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_5)))
  decl bf5
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_6)))
  decl bf6
    binder_role: IMPLICIT
    declaration_role: cdecl
    type: (sort us(up(u_7)))
  decl bf7
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym NormedAddCommGroup [up(u_4)]) (fv bf3))
  decl bf8
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (ap (ap (ap (sym NormedSpace [u0 up(u_4)]) (sym Real [])) (fv bf3)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv b
... [16290 more characters]
```

### SEED_STRUCTURED_ENGLISH

*22,620 characters*

```text
In meta:
  summary has theorem is SchwartzMap.integrable_of_le_of_pow_mul_le; and file is Mathlib/Analysis/Distribution/SchwartzSpace.lean .
In state_before:
  decl 𝕜~bf0 has display is 𝕜; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl 𝕜'~bf1 has display is 𝕜'; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_2))) .
  decl D~bf2 has display is D; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_3))) .
  decl E~bf3 has display is E; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_4))) .
  decl F~bf4 has display is F; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_5))) .
  decl G~bf5 has display is G; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_6))) .
  decl V~bf6 has display is V; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_7))) .
  decl inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9986~bf7 has display is inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9986; and binder_role is INSTANCE_
... [21420 more characters]
```

### SEED_TYPED_AST

*16,622 characters*

```text
mta
  - smy
    thm: SchwartzMap.integrable_of_le_of_pow_mul_le
    fl: Mathlib/Analysis/Distribution/SchwartzSpace.lean
sb
  - dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_1}}}
  - dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_2}}}
  - dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_3}}}
  - dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_4}}}
  - dc bf4
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_5}}}
  - dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_6}}}
  - dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: {sort|us{up{u_7}}}
  - dc bf7
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|NormedAddCommGroup,[up{u_4}]},{fv|bf3}}
  - dc bf8
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|NormedSpace,[u0 up{u_4}]},{sym|Real,[]}},{fv|bf3}},{sym|Real.normedField,[]}},{ap|{ap|{sym|NormedAddCommGroup.toSeminormedAddCommGroup,[up{u_4}]},{fv|bf3}},{fv|bf7}}}
  - dc bf9
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|NormedAddCommGroup,[up{u_5}]},{fv|bf4}}
  - dc bf10
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|NormedSpace,[u0 up{u_5}]},{sym|Real,[]}},{fv|bf4}
... [15422 more characters]
```

### FINALIST R_5b2eb732ac8b

*14,527 characters*

```text
#
  Y
    TH: SchwartzMap.integrable_of_le_of_pow_mul_le
    FL: Mathlib/Analysis/Distribution/SchwartzSpace.lean
→
  T
    R: LEAN_ELABORATED_TACTIC_OCCURRENCE/-
    k: LEAN_ELABORATED_TACTIC_OCCURRENCE
    e: -
    ⊨: [SchwartzMap.pow_mul_le_of_le_of_pow_mul_le,norm_nonneg]
    L: [Mathlib/Analysis/Distribution/SchwartzSpace.lean::SchwartzMap.integrable_of_le_of_pow_mul_le::4:before:local:f24,Mathlib/Analysis/Distribution/SchwartzSpace.lean::SchwartzMap.integrable_of_le_of_pow_mul_le::4:before:local:f25,Mathlib/Analysis/Distribution/SchwartzSpace.lean::SchwartzMap.integrable_of_le_of_pow_mul_le::4:before:local:f27]
Σ₀
  □ bm0
    ⊢: LE.le [u0] sym Real [] sym ap Real.instLE [] sym ap HMul.hMul [u0 u0 u0] sym Real [] sym ap Real [] sym ap Real [] sym ap instHMul [u0] sym Real [] sym ap Real.instMul [] sym ap ap HPow.hPow [u0 u0 u0] sym Real [] sym ap Nat [] sym ap Real [] sym ap instHPow [u0 u0] sym Real [] sym ap Nat [] sym ap Monoid.toNatPow [u0] sym Real [] sym ap Real.instMonoid [] sym ap ap ap Norm.norm [up(u_3)] sym bf2 fv ap SeminormedAddCommGroup.toNorm [up(u_3)] sym bf2 fv ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_3)] sym bf2 fv ap bf11 fv ap ap ap bf27 fv ap a
... [13327 more characters]
```

### FINALIST R_000441b08de4

*14,360 characters*

```text
mta
  smy ;; thm: SchwartzMap.integrable_of_le_of_pow_mul_le ;; fl: Mathlib/Analysis/Distribution/SchwartzSpace.lean
sb
  dc bf0 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_1)) sort
  dc bf1 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_2)) sort
  dc bf2 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_3)) sort
  dc bf3 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_4)) sort
  dc bf4 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_5)) sort
  dc bf5 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_6)) sort
  dc bf6 ;; br: IMPLICIT ;; dr: cdecl ;; ty: us(up(u_7)) sort
  dc bf7 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedAddCommGroup [up(u_4)] sym bf3 fv ap
  dc bf8 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedSpace [u0 up(u_4)] sym Real [] sym ap bf3 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)] sym bf3 fv ap bf7 fv ap ap
  dc bf9 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedAddCommGroup [up(u_5)] sym bf4 fv ap
  dc bf10 ;; br: INSTANCE_IMPLICIT ;; dr: cdecl ;; ty: NormedSpace [u0 up(u_5)] sym Real [] sym ap bf4 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_5)] sym bf4 fv ap bf9 fv ap ap
  dc bf11 ;; br: IN
... [13160 more characters]
```

### FINALIST R_01d4e489af53

*16,061 characters*

```text
(mta
  (smy (thm SchwartzMap.integrable_of_le_of_pow_mul_le) (fl Mathlib/Analysis/Distribution/SchwartzSpace.lean))
)
(sb
  (dc f0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc f1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc f2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_3)))))
  (dc f3 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_4)))))
  (dc f4 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_5)))))
  (dc f5 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_6)))))
  (dc f6 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_7)))))
  (dc f7 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_4)]) (fv f3))))
  (dc f8 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_4)]) (sym Real [])) (fv f3)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv f3)) (fv f7)))))
  (dc f9 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_5)]) (fv f4))))
  (dc f10 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_5)]) (sym Real [])) (fv f4)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_5)]) (fv f4)) (fv f9)))))
  
... [14861 more characters]
```

### FINALIST R_101e806690b0

*36,970 characters*

```text
$
  A $a0
    t-> (ap (ap (ap (ap (sym LE.le [u0]) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (sym instHMul [u0]) (sym Real [])) (sym Real.instMul []))) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [u0 u0 u0]) (sym Real [])) (sym Nat [])) (sym Real [])) (ap (ap (ap (sym instHPow [u0 u0]) (sym Real [])) (sym Nat [])) (ap (ap (sym Monoid.toNatPow [u0]) (sym Real [])) (sym Real.instMonoid [])))) (ap (ap (ap (sym Norm.norm [up(u_3)]) (fv bf2)) (ap (ap (sym SeminormedAddCommGroup.toNorm [up(u_3)]) (fv bf2)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_3)]) (fv bf2)) (fv bf11)))) (fv bf27))) (fv bf23))) (ap (ap (ap (sym Norm.norm [up(u_4)]) (fv bf3)) (ap (ap (sym SeminormedAddCommGroup.toNorm [up(u_4)]) (fv bf3)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7)))) (ap (fv bf20) (fv bf27))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (sym instHMul [u0]) (sym Real [])) (ap (ap (sym NonUnitalNonAssocRing.toMul [u0]) (sym Real [])) (ap (ap (sym NonAssocRing.toNonUnitalNonAssocRing [u0]
... [35770 more characters]
```

### FINALIST R_28b291b5ebe6

*18,039 characters*

```text
meta
  summary ;; theorem-> SchwartzMap.integrable_of_le_of_pow_mul_le ;; file-> Mathlib/Analysis/Distribution/SchwartzSpace.lean
state_before
  decl f0 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_1)) sort
  decl f1 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_2)) sort
  decl f2 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_3)) sort
  decl f3 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_4)) sort
  decl f4 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_5)) sort
  decl f5 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_6)) sort
  decl f6 ;; binder_role-> IMPLICIT ;; declaration_role-> cdecl ;; type-> us(up(u_7)) sort
  decl f7 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> NormedAddCommGroup [up(u_4)] sym f3 fv ap
  decl f8 ;; binder_role-> INSTANCE_IMPLICIT ;; declaration_role-> cdecl ;; type-> NormedSpace [u0 up(u_4)] sym Real [] sym ap f3 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)] sym f3 fv ap f7 fv ap ap
  decl f9 ;; binder_role-> INSTANCE_IMPLICIT ;; decla
... [16839 more characters]
```
