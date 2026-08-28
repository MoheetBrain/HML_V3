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
    ∈: ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(us(up(u_2))))]),pi(IMPLICIT,sort(us(up(u_2))),pi(IMPLICIT,pi(EXPLICIT,bv(0),sort(us(up(u_1)))),pi(EXPLICIT,ap(sym(List,[up(u_2)]),bv(1)),pi(EXPLICIT,pi(EXPLICIT,bv(2),ap(sym(List,[up(u_1)]),ap(bv(2),bv
... [2931 more characters]
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
    target: (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))
  mvar bm0
    kind: SYNTHETIC_OPAQUE
    type: (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi 
... [3554 more characters]
```

### SEED_STRUCTURED_ENGLISH

*5,256 characters*

```text
In meta:
  summary has theorem is List.sigma_eq_sigmaTR; and file is .lake/packages/batteries/Batteries/Data/List/Basic.lean .
In state_before:
  decl sigma_eq_sigmaTR~bf0 has display is sigma_eq_sigmaTR; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(us(up(u_2))))]),pi(IMPLICIT,sort(us(up(u_2))),pi(IMPLICIT,pi(EXPLICIT,bv(0),sort(us(up(u_1)))),pi(EXPLICIT,ap(sym(List,[up(u_2)]),bv(1)),pi(EXPLICIT,pi(EXPLICIT,bv(2),ap(sym(List,[up(u_1)]),ap(bv(2),bv(0)))),ap(sym(List,[umax(up(u_1),up(u_2))]),ap(ap(sym(Sigma,[up(u_2) up(u_1)]),bv(3)),lam(EXPLICIT,bv(3),ap(bv(3),bv(0)))))))))),sym(List.sigma,[up(u_2) up(u_1)])),sym(List.sigmaTR,[up(u_2) up(u_1)])) .
  goal bm0 has context is [sigma_eq_sigmaTR~bf0]; and target is ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(us(up(u_2))))]),pi(IMPLICIT,sort(us(up(u_2))),pi(IMPLICIT,pi(EXPLICIT,bv(0),sort(us(up(u_1)))),pi(EXPLICIT,ap(sym(List,[up(u_2)]),bv(1)),pi(EXPLICIT,pi(EXPLICIT,bv(2),ap(sym(List,[up(u_1)]),ap(bv(2),bv(0)))),ap(sym(List,[umax(up(u_1),up(u_2))]),ap(ap(sym(Sigma,[up(u_2) up(u_1)]),bv(3)),lam(EXPLICIT,bv(3),ap(bv(3),bv(0)))))))))),sym(List.sigma,[up(u_2) up(u_1)])),sym(List.sigmaTR,[up(u_2) up(u_1)])) .
  mvar bm0 has kind is SYNTHETIC_OPAQUE; and type is ap(ap(ap(sym(Eq,[umax(us(us(up(u_1))),us(us(up(u_2))))]),pi(IMPLICIT,sort(us(up(u_2))),pi(IMPLICIT,pi(EXPLICIT,bv(0)
... [3856 more characters]
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
    ty: {ap|{ap|{ap|{sym|Eq,[umax{us{us{up{u_1}}},us{us{up{u_2}}}}]},{pi|IMPLICIT,{sort|us{up{u_2}}},{pi|IMPLICIT,{pi|EXPLICIT,{bv|0},{sort|us{up{u_1}}}},{pi|EXPLICIT,{ap|{sym|List,[up{u_2}]},{bv|1}},{pi|EXPLICIT
... [3116 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*4,315 characters*

```text
(mta
  (smy (thm List.sigma_eq_sigmaTR) (fl .lake/packages/batteries/Batteries/Data/List/Basic.lean))
)
(sb
  (dc bf0 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))))
  (gl bm0 (ctx [bf0]) (tgt (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))))
  (mv bm0 (knd SYNTHETIC_OPAQUE) (ty (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap 
... [2915 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*4,085 characters*

```text
mta
  smy
    thm: List.sigma_eq_sigmaTR
    fl: .lake/packages/batteries/Batteries/Data/List/Basic.lean
sb
  dc bf0
    br: EXPLICIT
    dr: cdecl
    ty: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv 1 apn EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv 1 apn 1 apn pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv EXPLICIT 3 bv 3 bv 0 bv 1 apn lam 2 apn 1 apn pi pi pi pi List.sigma [up(u_2) up(u_1)] sym List.sigmaTR [up(u_2) up(u_1)] sym 3 apn
  gl bm0
    ctx: [bf0]
    tgt: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv 1 apn EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv 1 apn 1 apn pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv EXPLICIT 3 bv 3 bv 0 bv 1 apn lam 2 apn 1 apn pi pi pi pi List.sigma [up(u_2) up(u_1)] sym List.sigmaTR [up(u_2) up(u_1)] sym 3 apn
  mv bm0
    knd: SYNTHETIC_OPAQUE
    ty: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv 1 apn EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv 1 apn 1 apn pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv EXPLICIT 3 bv 3 bv 0 bv 1 apn lam 2 apn 
... [2685 more characters]
```

### FINALIST R_623a343174ec

*4,396 characters*

```text
meta
  summary ;; theorem: List.sigma_eq_sigmaTR ;; file: .lake/packages/batteries/Batteries/Data/List/Basic.lean
state_before
  decl bf0 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 bv 0 bv ap lam ap ap pi pi pi pi ap List.sigma [up(u_2) up(u_1)] sym ap List.sigmaTR [up(u_2) up(u_1)] sym ap
  goal bm0 ;; context: [bf0] ;; target: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 bv 0 bv ap lam ap ap pi pi pi pi ap List.sigma [up(u_2) up(u_1)] sym ap List.sigmaTR [up(u_2) up(u_1)] sym ap
  mvar bm0 ;; kind: SYNTHETIC_OPAQUE ;; type: Eq [umax(us(us(up(u_1))) us(us(up(u_2))))] sym IMPLICIT us(up(u_2)) sort IMPLICIT EXPLICIT 0 bv us(up(u_1)) sort pi EXPLICIT List [up(u_2)] sym 1 bv ap EXPLICIT EXPLICIT 2 bv List [up(u_1)] sym 2 bv 0 bv ap ap pi List [umax(up(u_1) up(u_2))] sym Sigma [up(u_2) up(u_1)] sym 3 bv ap EXPLICIT 3 bv 3 b
... [2996 more characters]
```

### FINALIST R_8f1e3d8b7028

*5,088 characters*

```text
meta
  summary
    theorem: List.sigma_eq_sigmaTR
    file: .lake/packages/batteries/Batteries/Data/List/Basic.lean
state_before
  goal bm0
    target: (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))
    context: [bf0]
  decl bf0
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))
  mvar bm0
    kind: SYNTHETIC_OPAQUE
    type: (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(
... [3688 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*6,335 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)])) (sym List.sigmaTR [up(u_2) up(u_1)]))
  alias $a1
    term: (ap (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0)))))))))) (sym List.sigma [up(u_2) up(u_1)]))
  alias $a2
    term: (ap (sym Eq [umax(us(us(up(u_1))) us(us(up(u_2))))]) (pi IMPLICIT (sort us(up(u_2))) (pi IMPLICIT (pi EXPLICIT (bv 0) (sort us(up(u_1)))) (pi EXPLICIT (ap (sym List [up(u_2)]) (bv 1)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (sym List [up(u_1)]) (ap (bv 2) (bv 0)))) (ap (sym List [umax(up(u_1) up(u_2))]) (ap (ap (sym Sigma [up(u_2) up(u_1)]) (bv 3)) (lam EXPLICIT (bv 3) (ap (bv 3) (bv 0))))))))))
  alias $a3
    
... [4935 more characters]
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
    ∈: ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Finset,[u0]),sym(Nat,[]))),ap(ap(ap(ap(sym(Finset.map,[u0 u0]),ap(sym(Fin,[]),fv(n~bf0))),sym(Nat,[])),ap(sym(Fin.valEmbedding,[]),fv(n~bf0))),ap(ap(ap(ap(sym(Finset.Ioi,[u0]),ap(sym(Fin,[]),fv(n~bf0))),ap(ap(sym(PartialOrder.toPreorder,[u0]),ap(sym(Fin,[]),fv(n~bf0))),ap(sym(Fin.instPartialOrder,[]),fv(n~bf0)))),ap(sym(Fin.instLocallyFiniteOrderTop,[]),fv(n~bf0))),fv(a~bf1)))),ap(ap(ap(ap(ap(sym(Finset.Ioc,[u0]),sym(Nat,[])),ap(ap(sym(PartialOrder.toPreorder,[u0]),sym(Nat,[])),ap(ap(sym(SemilatticeInf.toPartialOrder,[u0]),sym(Nat,[])),ap(ap(sym(Lattice.toSemilatticeInf,[u0]),sym(Nat,[])),ap(ap(sym(DistribLattice.toLattice,[u0]),sym(Nat,[])),sym(instDistribLatticeNat,[])))))),sym(Nat.instLocallyFiniteOrder,[])),ap(ap(sym(Fin.val,[]),fv(n~bf0)),fv(a~bf1))),ap(ap(ap(ap(ap(ap(sym(HSub.hSub,[u0 u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(Nat,[])),ap(ap(sym(instHSub,[u0]),sym(Nat,[])),sym(instSubNat,[]))),fv(n~bf0)),ap(ap(ap(sym(OfNat.ofNat,[u0]),sym(Na
... [6093 more characters]
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
    type: (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (sym Finset.map [u0 u0]) (ap (sym Fin []) (fv bf0))) (sym Nat [])) (ap (sym Fin.valEmbedding []) (fv bf0))) (ap (ap (ap (ap (sym Finset.Ioi [u0]) (ap (sym Fin []) (fv bf0))) (ap (ap (sym PartialOrder.toPreorder [u0]) (ap (sym Fin []) (fv bf0))) (ap (sym Fin.instPartialOrder []) (fv bf0)))) (ap (sym Fin.instLocallyFiniteOrderTop []) (fv bf0))) (fv bf1)))) (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (ap (ap (sym Fin.val []) (fv bf0)) (fv bf1))) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym Nat [])) (s
... [6850 more characters]
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
  decl map_valEmbedding_Ioi~bf3 has display is map_valEmbedding_Ioi; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Finset,[u0]),sym(Nat,[]))),ap(ap(ap(ap(sym(Finset.map,[u0 u0]),ap(sym(Fin,[]),fv(n~bf0))),sym(Nat,[])),ap(sym(Fin.valEmbedding,[]),fv(n~bf0))),ap(ap(ap(ap(sym(Finset.Ioi,[u0]),ap(sym(Fin,[]),fv(n~bf0))),ap(ap(sym(PartialOrder.toPreorder,[u0]),ap(sym(Fin,[]),fv(n~bf0))),ap(sym(Fin.instPartialOrder,[]),fv(n~bf0)))),ap(sym(Fin.instLocallyFiniteOrderTop,[]),fv(n~bf0))),fv(a~bf1)))),ap(ap(ap(ap(ap(sym(Finset.Ioc,[u0]),sym(Nat,[])),ap(ap(sym(PartialOrder.toPreorder,[u0]),sym(Nat,[])),ap(ap(sym(SemilatticeInf.toPartialOrder,[u0]),sym(Nat,[])),ap(ap(sym(Lattice.toSemilatticeInf,[u0]),sym(Nat,[])),ap(ap(sym(DistribLattice.toLattice,[u0]),sym(Nat,[])),sym(instDistribLatticeNat,[])))))),sym(Nat.instLocallyFiniteOrder,[
... [6802 more characters]
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
    ty: {ap|{ap|{ap|{sym|Eq,[us{u0}]},{ap|{sym|Finset,[u0]},{sym|Nat,[]}}},{ap|{ap|{ap|{ap|{sym|Finset.map,[u0 u0]},{ap|{sym|Fin,[]},{fv|bf0}}},{sym|Nat,[]}},{ap|{sym|Fin.valEmbedding,[]},{fv|bf0}}},{ap|{ap|{ap|{ap|{sym|Finset.Ioi,[u0]},{ap|{sym|Fin,[]},{fv|bf0}}},{ap|{ap|{sym|PartialOrder.toPreorder,[u0]},{ap|{sym|Fin,[]},{fv|bf0}}},{ap|{sym|Fin.instPartialOrder,[]},{fv|bf0}}}},{ap|{sym|Fin.instLocallyFiniteOrderTop,[]},{fv|bf0}}},{fv|bf1}}}},{ap|{ap|{ap|{ap|{ap|{sym|Finset.Ioc,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|PartialOrder.toPreorder,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|SemilatticeInf.toPartialOrder,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|Lattice.toSemilatticeInf,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|DistribLattice.toLattice,[u0]},{sym|Nat,[]}},{sym|instDistribLatticeNat,[]}}}}}},{sym|Nat.instLocallyFiniteOrder,[]}},{ap|{ap|{sym|Fin.val,[]},{fv|bf0}},{fv|bf1}}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HSub.hSub,[u0 u0 u0]},{sym|Nat,[]}},{sym|Nat,[]}},{sym|Nat,[]}},{ap|{ap|{sym|instHSub,[u0]},{sym|Nat,[]}},{sym|instSubNat,[]}}},{fv|bf0}},{ap|{ap|{ap|{sym|Of
... [6492 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*7,766 characters*

```text
(mta
  (smy (thm Fin.map_valEmbedding_Ioi) (fl Mathlib/Order/Interval/Finset/Fin.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc bf1 (br EXPLICIT) (dr cdecl) (ty (ap (sym Fin []) (fv bf0))))
  (dc bf2 (br EXPLICIT) (dr cdecl) (ty (ap (sym Fin []) (fv bf0))))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (sym Finset.map [u0 u0]) (ap (sym Fin []) (fv bf0))) (sym Nat [])) (ap (sym Fin.valEmbedding []) (fv bf0))) (ap (ap (ap (ap (sym Finset.Ioi [u0]) (ap (sym Fin []) (fv bf0))) (ap (ap (sym PartialOrder.toPreorder [u0]) (ap (sym Fin []) (fv bf0))) (ap (sym Fin.instPartialOrder []) (fv bf0)))) (ap (sym Fin.instLocallyFiniteOrderTop []) (fv bf0))) (fv bf1)))) (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (ap (ap (sym Fin.val []) (fv bf0)) (fv bf1))) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHSub [u0]) (sym Nat [])) (sym instSubNat []))) (fv bf0)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 1
... [6366 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*6,617 characters*

```text
mta
  smy
    thm: Fin.map_valEmbedding_Ioi
    fl: Mathlib/Order/Interval/Finset/Fin.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: Nat [] sym
  dc bf1
    br: EXPLICIT
    dr: cdecl
    ty: Fin [] sym bf0 fv 1 apn
  dc bf2
    br: EXPLICIT
    dr: cdecl
    ty: Fin [] sym bf0 fv 1 apn
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: Eq [us(u0)] sym Finset [u0] sym Nat [] sym 1 apn Finset.map [u0 u0] sym Fin [] sym bf0 fv 1 apn Nat [] sym Fin.valEmbedding [] sym bf0 fv 1 apn Finset.Ioi [u0] sym Fin [] sym bf0 fv 1 apn PartialOrder.toPreorder [u0] sym Fin [] sym bf0 fv 1 apn Fin.instPartialOrder [] sym bf0 fv 1 apn 2 apn Fin.instLocallyFiniteOrderTop [] sym bf0 fv 1 apn bf1 fv 4 apn 4 apn Finset.Ioc [u0] sym Nat [] sym PartialOrder.toPreorder [u0] sym Nat [] sym SemilatticeInf.toPartialOrder [u0] sym Nat [] sym Lattice.toSemilatticeInf [u0] sym Nat [] sym DistribLattice.toLattice [u0] sym Nat [] sym instDistribLatticeNat [] sym 2 apn 2 apn 2 apn 2 apn Nat.instLocallyFiniteOrder [] sym Fin.val [] sym bf0 fv bf1 fv 2 apn HSub.hSub [u0 u0 u0] sym Nat [] sym Nat [] sym Nat [] sym instHSub [u0] sym Nat [] sym instSubNat [] sym 2 apn bf0 fv OfNat.ofNat [u0] sym Nat [] sym NAT 1 lit instOfNatNat [] sym NAT 1 lit 1 apn 3 apn 6 apn 5 apn 3 apn
  gl bm0
    ctx: [bf0,bf1,bf2,bf3]
    tgt: Eq [us(u0)] sym Finset [u0] sym Nat [] sym 1 apn Finset.map [u0 u0] sym Fin [] sym bf0 fv 1 
... [5217 more characters]
```

### FINALIST R_623a343174ec

*7,446 characters*

```text
meta
  summary ;; theorem: Fin.map_valEmbedding_Ioi ;; file: Mathlib/Order/Interval/Finset/Fin.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Nat [] sym
  decl bf1 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Fin [] sym bf0 fv ap
  decl bf2 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Fin [] sym bf0 fv ap
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Eq [us(u0)] sym Finset [u0] sym Nat [] sym ap ap Finset.map [u0 u0] sym Fin [] sym bf0 fv ap ap Nat [] sym ap Fin.valEmbedding [] sym bf0 fv ap ap Finset.Ioi [u0] sym Fin [] sym bf0 fv ap ap PartialOrder.toPreorder [u0] sym Fin [] sym bf0 fv ap ap Fin.instPartialOrder [] sym bf0 fv ap ap ap Fin.instLocallyFiniteOrderTop [] sym bf0 fv ap ap bf1 fv ap ap ap Finset.Ioc [u0] sym Nat [] sym ap PartialOrder.toPreorder [u0] sym Nat [] sym ap SemilatticeInf.toPartialOrder [u0] sym Nat [] sym ap Lattice.toSemilatticeInf [u0] sym Nat [] sym ap DistribLattice.toLattice [u0] sym Nat [] sym ap instDistribLatticeNat [] sym ap ap ap ap ap Nat.instLocallyFiniteOrder [] sym ap Fin.val [] sym bf0 fv ap bf1 fv ap ap HSub.hSub [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHSub [u0] sym Nat [] sym ap instSubNat [] sym ap ap bf0 fv ap OfNat.ofNat [u0] sym Nat [] sym ap NAT 1 lit ap instOfNatNat [] sym NAT 1 lit ap ap ap ap ap
  goal bm0 ;;
... [6046 more characters]
```

### FINALIST R_8f1e3d8b7028

*8,455 characters*

```text
meta
  summary
    theorem: Fin.map_valEmbedding_Ioi
    file: Mathlib/Order/Interval/Finset/Fin.lean
state_before
  goal bm0
    target: (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (sym Finset.map [u0 u0]) (ap (sym Fin []) (fv bf0))) (sym Nat [])) (ap (sym Fin.valEmbedding []) (fv bf0))) (ap (ap (ap (ap (sym Finset.Ioi [u0]) (ap (sym Fin []) (fv bf0))) (ap (ap (sym PartialOrder.toPreorder [u0]) (ap (sym Fin []) (fv bf0))) (ap (sym Fin.instPartialOrder []) (fv bf0)))) (ap (sym Fin.instLocallyFiniteOrderTop []) (fv bf0))) (fv bf1)))) (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (ap (ap (sym Fin.val []) (fv bf0)) (fv bf1))) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHSub [u0]) (sym Nat [])) (sym instSubNat []))) (fv bf0)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 1)) (ap (sym instOfNatNat []) (lit NAT 1))))))
    context: [bf0,bf1,bf2,bf3]
  alias bf0
    tag: Nat
  alias bf1
    tag: Fin
  decl bf0
    binder_role: IMPLICIT
    declaration_role:
... [7055 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*9,364 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (sym Finset.map [u0 u0]) (ap (sym Fin []) (fv bf0))) (sym Nat [])) (ap (sym Fin.valEmbedding []) (fv bf0))) (ap (ap (ap (ap (sym Finset.Ioi [u0]) (ap (sym Fin []) (fv bf0))) (ap (ap (sym PartialOrder.toPreorder [u0]) (ap (sym Fin []) (fv bf0))) (ap (sym Fin.instPartialOrder []) (fv bf0)))) (ap (sym Fin.instLocallyFiniteOrderTop []) (fv bf0))) (fv bf1)))) (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (ap (ap (sym Fin.val []) (fv bf0)) (fv bf1))) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHSub [u0]) (sym Nat [])) (sym instSubNat []))) (fv bf0)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 1)) (ap (sym instOfNatNat []) (lit NAT 1))))))
  alias $a1
    term: (ap (ap (ap (ap (ap (sym Finset.Ioc [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym 
... [7964 more characters]
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
    ⊢: ap(ap(sym(ONote.NFBelow,[]),ap(ap(ap(ap(ap(ap(sym(HSub.hSub,[u0 u0 u0]),sym(ONote,[])),sym(ONote,[])),sym(ONote,[])),ap(ap(sym(instHSub,[u0]),sym(ONote,[])),sym(ONote.instSub,[]))),ap(ap(ap(sym(OfNat.ofNat,[u0]),sym(ONote,[])),lit(NA
... [1085 more characters]
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
    target: (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [
... [1321 more characters]
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
  decl x._@.Mathlib.SetTheory.Ordinal.Notation._hyg.5834~bf3 has display is x._@.Mathlib.SetTheory.Ordinal.Notation._hyg.5834; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(ONote.NFBelow,[]),ap(ap(ap(sym(OfNat.ofNat,[u0]),sym(ONote,[])),lit(NAT,0)),ap(sym(ONote.nat,[]),lit(NAT,0)))),fv(b~bf2)) .
  decl h₂~bf4 has display is h₂; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(sym(ONote.NF,[]),fv(o~bf1)) .
  goal bm0 has context is [sub_nfBelow~bf0,o~bf1,b~bf2,
... [1647 more characters]
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
    tgt: {ap|{ap|{sym|ONote.NFBelow,[]},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HSub.hSub,[u0 u0 u0]},{sym|ONote,[]}},{sym|ONote,[]}},{sym|ONote,[]}},{ap|{ap|{sym|instHSub,[u0]},{sym|ONote,[]}},{sym|ONote.instSub,[]}}},{ap|{ap|{ap|{sym|OfNat.ofNat,[u0]},{sym|ONote,[]}},{lit|NAT,0}},{ap|{sym|ONote.nat,[]},{lit|NAT,0}}}},{fv|bf1}}},{fv|bf2}}
  - mv bm0
    knd: SYNTHETIC_OPAQUE
    ty: {ap|{ap|{sym|
... [1028 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*2,335 characters*

```text
(mta
  (smy (thm ONote.sub_nfBelow) (fl Mathlib/SetTheory/Ordinal/Notation.lean))
)
(sb
  (dc bf0 (br EXPLICIT) (dr cdecl) (ty (pi IMPLICIT (sym ONote []) (pi IMPLICIT (sym ONote []) (pi IMPLICIT (sym Ordinal [u0]) (pi EXPLICIT (ap (ap (sym ONote.NFBelow []) (bv 2)) (bv 0)) (pi EXPLICIT (ap (sym ONote.NF []) (bv 2)) (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (bv 4)) (bv 3))) (bv 2)))))))))
  (dc bf1 (br EXPLICIT) (dr cdecl) (ty (sym ONote [])))
  (dc bf2 (br EXPLICIT) (dr cdecl) (ty (sym Ordinal [u0])))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf2))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (ap (sym ONote.NF []) (fv bf1))))
  (gl bm0 (ctx [bf0,bf1,bf2,bf3,bf4]) (tgt (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf1))) (fv bf2))))
  (mv bm0 (knd SYNTHETIC_OPAQUE) (ty (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 
... [935 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*2,148 characters*

```text
mta
  smy
    thm: ONote.sub_nfBelow
    fl: Mathlib/SetTheory/Ordinal/Notation.lean
sb
  dc bf0
    br: EXPLICIT
    dr: cdecl
    ty: IMPLICIT ONote [] sym IMPLICIT ONote [] sym IMPLICIT Ordinal [u0] sym EXPLICIT ONote.NFBelow [] sym 2 bv 0 bv 2 apn EXPLICIT ONote.NF [] sym 2 bv 1 apn ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ONote [] sym ONote [] sym instHSub [u0] sym ONote [] sym ONote.instSub [] sym 2 apn 4 bv 3 bv 6 apn 2 bv 2 apn pi pi pi pi pi
  dc bf1
    br: EXPLICIT
    dr: cdecl
    ty: ONote [] sym
  dc bf2
    br: EXPLICIT
    dr: cdecl
    ty: Ordinal [u0] sym
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: ONote.NFBelow [] sym OfNat.ofNat [u0] sym ONote [] sym NAT 0 lit ONote.nat [] sym NAT 0 lit 1 apn 3 apn bf2 fv 2 apn
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: ONote.NF [] sym bf1 fv 1 apn
  gl bm0
    ctx: [bf0,bf1,bf2,bf3,bf4]
    tgt: ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ONote [] sym ONote [] sym instHSub [u0] sym ONote [] sym ONote.instSub [] sym 2 apn OfNat.ofNat [u0] sym ONote [] sym NAT 0 lit ONote.nat [] sym NAT 0 lit 1 apn 3 apn bf1 fv 6 apn bf2 fv 2 apn
  mv bm0
    knd: SYNTHETIC_OPAQUE
    ty: ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ONote [] sym ONote [] sym instHSub [u0] sym ONote [] sym ONote.instSub [] sym 2 apn OfNat.ofNat [u0] sym ONote [] sym NAT 0 lit ONote.nat [] sym NAT 0 lit 1
... [748 more characters]
```

### FINALIST R_623a343174ec

*2,598 characters*

```text
meta
  summary ;; theorem: ONote.sub_nfBelow ;; file: Mathlib/SetTheory/Ordinal/Notation.lean
state_before
  decl bf0 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: IMPLICIT ONote [] sym IMPLICIT ONote [] sym IMPLICIT Ordinal [u0] sym EXPLICIT ONote.NFBelow [] sym 2 bv ap 0 bv ap EXPLICIT ONote.NF [] sym 2 bv ap ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ap ONote [] sym ap ONote [] sym ap instHSub [u0] sym ONote [] sym ap ONote.instSub [] sym ap ap 4 bv ap 3 bv ap ap 2 bv ap pi pi pi pi pi
  decl bf1 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: ONote [] sym
  decl bf2 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Ordinal [u0] sym
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: ONote.NFBelow [] sym OfNat.ofNat [u0] sym ONote [] sym ap NAT 0 lit ap ONote.nat [] sym NAT 0 lit ap ap ap bf2 fv ap
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: ONote.NF [] sym bf1 fv ap
  goal bm0 ;; context: [bf0,bf1,bf2,bf3,bf4] ;; target: ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ONote [] sym ap ONote [] sym ap ONote [] sym ap instHSub [u0] sym ONote [] sym ap ONote.instSub [] sym ap ap OfNat.ofNat [u0] sym ONote [] sym ap NAT 0 lit ap ONote.nat [] sym NAT 0 lit ap ap ap bf1 fv ap ap bf2 fv ap
  mvar bm0 ;; kind: SYNTHETIC_OPAQUE ;; type: ONote.NFBelow [] sym HSub.hSub [u0 u0 u0] sym ON
... [1198 more characters]
```

### FINALIST R_8f1e3d8b7028

*2,852 characters*

```text
meta
  summary
    theorem: ONote.sub_nfBelow
    file: Mathlib/SetTheory/Ordinal/Notation.lean
state_before
  goal bm0
    target: (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf1))) (fv bf2))
    context: [bf0,bf1,bf2,bf3,bf4]
  alias bf1
    tag: ONote
  alias bf2
    tag: Ordinal
  decl bf1
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (sym ONote [])
  decl bf2
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (sym Ordinal [u0])
  decl bf0
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (pi IMPLICIT (sym ONote []) (pi IMPLICIT (sym ONote []) (pi IMPLICIT (sym Ordinal [u0]) (pi EXPLICIT (ap (ap (sym ONote.NFBelow []) (bv 2)) (bv 0)) (pi EXPLICIT (ap (sym ONote.NF []) (bv 2)) (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (bv 4)) (bv 3))) (bv 2)))))))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (ap (ap (sym ONote.NFBelow []) (ap (ap (a
... [1452 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*3,971 characters*

```text
aliases
  alias $a0
    term: (ap (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf1))) (fv bf2))
  alias $a1
    term: (ap (sym ONote.NFBelow []) (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf1)))
  alias $a2
    term: (ap (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0)))) (fv bf1))
  alias $a3
    term: (ap (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym instHSub [u0]) (sym ONote [])) (sym ONote.instSub []))) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym ONote [])) (lit NAT 0)) (ap (sym ONote.nat []) (lit NAT 0))))
  alias $a4
    term: (ap (ap (ap (ap (sym HSub.hSub [u0 u0 u0]) (sym ONote [])) (sym ONote [])) (sym ONote [])) (ap (ap (sym in
... [2571 more characters]
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
    ⊢: ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Part,[u0]),sym(Turing.ToPartrec.Cfg,[]))),ap(ap(ap(ap(ap(ap(sym(Bind.bind,[u0 u0]),sym(Part,[u0])),ap(ap(sym(Monad.toBind,[u0 u0]),sym(Part,[u0])),sym(Part.instMonad,[u0]))),ap(sym(List,[u0]),sym(Nat,[]))),sym(Turing.ToPartrec.Cfg,[])),ap(ap(sym(Turing.ToPartrec.Code.eval,[]),fv(g~bf2)),fv(v~bf6))),lam(EXPLICIT,ap(sym(List,[u0]),sym(Nat,[])),ap(ap(ap(sym(Turing.eval,[u0]),sym(Turing.ToPartrec.Cfg,[])),sym(Turing.ToPartrec.step,[])),ap(ap(sym(Turing.ToPartrec.Cfg.ret,[]),ap(ap(sym(Turing.ToPartrec.Cont.comp,[]),fv(f~bf1)),fv(k~bf
... [6373 more characters]
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
    target: (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Part [u0]) (sym Turing.ToPartrec.Cfg []))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv bf2)) (fv bf6))) (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (sym Turi
... [7275 more characters]
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
  goal bm1 has context is [code_is_ok~bf0,f~bf1,g~bf2,IHf~bf3,IHg~bf4,k~bf5,v~bf6]; and target is ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Part,[u0]),sym(Turing.ToPartrec.Cfg,[]))),ap(ap(ap(ap(ap(ap(sym(Bind.bind,[u0 u0]),sym(Part,[u0])),ap(ap(sym(Monad.toBind,[u
... [7508 more characters]
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
    tgt: {ap|{ap|{ap|{sym|Eq,[us{u0}]},{ap|{sym|Part,[u0]},{sym|Turing.ToPartrec.Cfg,[]}}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|Bind.bind,[u0 u0]},{sym|Part,[u0]}},{ap|{ap|{sym|Monad.toBind,[u0 u0]},{sym|Part,[u0]}},{sym|Part.instMonad,[u0]}}},{ap|{sym|List,[u0]},{sym|Nat,[]}}},{sym|Turing.ToPartrec.Cfg,[]}},{ap|{ap|{sym|Turing.ToPartrec.Code.eval,[]},{fv|bf2}},{fv|bf6}}},{lam|EXPLICIT,{ap|{sym|List,[u0]},{sym|Nat,[]}},{ap|{ap|{ap|{sym|Turing.eval,[u0]},{sym|Turing.ToPartrec.Cfg,[]}},{sym|Turing.ToPartrec.step,[]}},{ap|{ap|{sym|Turing.ToPartrec.Cfg.ret,[]},{ap|{ap|{sym|Turing.ToPartrec.Cont.comp,[]},{fv|bf1}},{fv|bf5}}},{bv|0}}}}}},{ap|{
... [6712 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*7,899 characters*

```text
(mta
  (smy (thm Turing.ToPartrec.code_is_ok) (fl Mathlib/Computability/TMToPartrec.lean))
)
(sb
  (dc bf0 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (sym Turing.ToPartrec.Code []) (ap (sym Turing.ToPartrec.Code.Ok []) (bv 0)))))
  (dc bf1 (br EXPLICIT) (dr cdecl) (ty (sym Turing.ToPartrec.Code [])))
  (dc bf2 (br EXPLICIT) (dr cdecl) (ty (sym Turing.ToPartrec.Code [])))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (ap (mv bm0) (fv bf1))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (ap (mv bm0) (fv bf2))))
  (dc bf5 (br EXPLICIT) (dr cdecl) (ty (sym Turing.ToPartrec.Cont [])))
  (dc bf6 (br EXPLICIT) (dr cdecl) (ty (ap (sym List [u0]) (sym Nat []))))
  (gl bm1 (ctx [bf0,bf1,bf2,bf3,bf4,bf5,bf6]) (tgt (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Part [u0]) (sym Turing.ToPartrec.Cfg []))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv bf2)) (fv bf6))) (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (sym Turing.eval [u0]) (sym Turing.ToPartrec.Cfg [])) (sym Turing.ToPartrec.step [])) (ap (ap (sym Turing.ToPartrec.Cfg.ret []) (ap (ap (sym Turing.ToPartrec.Cont.comp []) (fv bf1)) (fv bf5))) (bv 0)))))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym 
... [6499 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*7,018 characters*

```text
mta
  smy
    thm: Turing.ToPartrec.code_is_ok
    fl: Mathlib/Computability/TMToPartrec.lean
sb
  dc bf0
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT Turing.ToPartrec.Code [] sym Turing.ToPartrec.Code.Ok [] sym 0 bv 1 apn pi
  dc bf1
    br: EXPLICIT
    dr: cdecl
    ty: Turing.ToPartrec.Code [] sym
  dc bf2
    br: EXPLICIT
    dr: cdecl
    ty: Turing.ToPartrec.Code [] sym
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: bm0 mv bf1 fv 1 apn
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: bm0 mv bf2 fv 1 apn
  dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: Turing.ToPartrec.Cont [] sym
  dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: List [u0] sym Nat [] sym 1 apn
  gl bm1
    ctx: [bf0,bf1,bf2,bf3,bf4,bf5,bf6]
    tgt: Eq [us(u0)] sym Part [u0] sym Turing.ToPartrec.Cfg [] sym 1 apn Bind.bind [u0 u0] sym Part [u0] sym Monad.toBind [u0 u0] sym Part [u0] sym Part.instMonad [u0] sym 2 apn List [u0] sym Nat [] sym 1 apn Turing.ToPartrec.Cfg [] sym Turing.ToPartrec.Code.eval [] sym bf2 fv bf6 fv 2 apn EXPLICIT List [u0] sym Nat [] sym 1 apn Turing.eval [u0] sym Turing.ToPartrec.Cfg [] sym Turing.ToPartrec.step [] sym Turing.ToPartrec.Cfg.ret [] sym Turing.ToPartrec.Cont.comp [] sym bf1 fv bf5 fv 2 apn 0 bv 2 apn 3 apn lam 6 apn Bind.bind [u0 u0] sym Part [u0] sym Monad.toBind [u0 u0] sym Part [u0] sym Part.instMonad [u0] sym 2 apn List [u0] sym Nat [] sym 1 apn Turing.ToPartrec.Cf
... [5618 more characters]
```

### FINALIST R_623a343174ec

*7,805 characters*

```text
meta
  summary ;; theorem: Turing.ToPartrec.code_is_ok ;; file: Mathlib/Computability/TMToPartrec.lean
state_before
  decl bf0 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT Turing.ToPartrec.Code [] sym Turing.ToPartrec.Code.Ok [] sym 0 bv ap pi
  decl bf1 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Turing.ToPartrec.Code [] sym
  decl bf2 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Turing.ToPartrec.Code [] sym
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: bm0 mv bf1 fv ap
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: bm0 mv bf2 fv ap
  decl bf5 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Turing.ToPartrec.Cont [] sym
  decl bf6 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: List [u0] sym Nat [] sym ap
  goal bm1 ;; context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6] ;; target: Eq [us(u0)] sym Part [u0] sym Turing.ToPartrec.Cfg [] sym ap ap Bind.bind [u0 u0] sym Part [u0] sym ap Monad.toBind [u0 u0] sym Part [u0] sym ap Part.instMonad [u0] sym ap ap List [u0] sym Nat [] sym ap ap Turing.ToPartrec.Cfg [] sym ap Turing.ToPartrec.Code.eval [] sym bf2 fv ap bf6 fv ap ap EXPLICIT List [u0] sym Nat [] sym ap Turing.eval [u0] sym Turing.ToPartrec.Cfg [] sym ap Turing.ToPartrec.step [] sym ap Turing.ToPartrec.Cfg.ret [] sym Turing.ToPartrec.Cont.comp [] sym bf1 f
... [6405 more characters]
```

### FINALIST R_8f1e3d8b7028

*9,195 characters*

```text
meta
  summary
    theorem: Turing.ToPartrec.code_is_ok
    file: Mathlib/Computability/TMToPartrec.lean
state_before
  goal bm1
    target: (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Part [u0]) (sym Turing.ToPartrec.Cfg []))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv bf2)) (fv bf6))) (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (sym Turing.eval [u0]) (sym Turing.ToPartrec.Cfg [])) (sym Turing.ToPartrec.step [])) (ap (ap (sym Turing.ToPartrec.Cfg.ret []) (ap (ap (sym Turing.ToPartrec.Cont.comp []) (fv bf1)) (fv bf5))) (bv 0)))))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (ap (sym List [u0]) (sym Nat []))) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv bf2)) (bv 0))) (ap (sym Turing.ToPartrec.Code.eval []) (fv bf1)))) (fv bf6))) (lam EXPLICIT (ap (sym List [u0]
... [7795 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*15,682 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Part [u0]) (sym Turing.ToPartrec.Cfg []))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv bf2)) (fv bf6))) (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (sym Turing.eval [u0]) (sym Turing.ToPartrec.Cfg [])) (sym Turing.ToPartrec.step [])) (ap (ap (sym Turing.ToPartrec.Cfg.ret []) (ap (ap (sym Turing.ToPartrec.Cont.comp []) (fv bf1)) (fv bf5))) (bv 0)))))) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (sym Turing.ToPartrec.Cfg [])) (ap (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (ap (ap (ap (sym Bind.bind [u0 u0]) (sym Part [u0])) (ap (ap (sym Monad.toBind [u0 u0]) (sym Part [u0])) (sym Part.instMonad [u0]))) (ap (sym List [u0]) (sym Nat []))) (ap (sym List [u0]) (sym Nat []))) (ap (ap (sym Turing.ToPartrec.Code.eval []) (fv bf2)) (bv 0))) (ap (sym Turing.ToPartrec.Code.eval []) (fv bf1)))) (fv bf6))) (lam EXPLICIT (ap (sym List [u0]) (sym Nat [])) (ap (ap (ap (sym Turing.eval [u0]) (sym Turing.ToPartrec.Cfg [])) (sym Turing.ToPartrec.step []
... [14282 more characters]
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
    n: a
    b: EXPLICIT
    d: cdecl
    ∈: ap(sym(Option,[up(u)]),ap(ap(sym(Prod,[up(u) up(u)]),fv(α~bf0)),ap(sym(Stream'.WSeq,[up(u)]),fv(α~bf0))))
  D h~bf7
    n: h
    b: EXPLICIT
    d: cdecl
    ∈: 
... [8876 more characters]
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
    type: (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv bf0)) (ap (ap (sym Stream'.WSeq.tail [up(u)]) (fv bf0)) (fv bf4))))
  decl bf6
    binder_role: EXPLICIT
    declaration_role: cdecl
    type: (ap (sym Option [up(u)]) (ap (ap (sym Pro
... [9494 more characters]
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
  decl s~bf4 has display is s; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(sym(Stream'.WSeq,[up(u)]),fv(α~bf0)) .
  decl T~bf5 has display is T; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(Computation.Terminates,[up(u)]),ap(sym(Option,[up(u)]
... [10185 more characters]
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
    ty: {ap|{sym|Option,[up{u}]},{ap|{ap|{sym|Prod,[up{u} up{u}]},{fv|bf0}},{ap|{sym|Stream'.WSeq,[up{u}]},{fv|bf0}}}}
  - dc bf7
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{ap|{sym|Membership.mem,[up{u} up{u}]},{ap|{sym|Option,[up
... [8836 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*10,002 characters*

```text
(mta
  (smy (thm Stream'.WSeq.head_terminates_of_head_tail_terminates) (fl Mathlib/Data/Seq/WSeq.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u)))))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(v)))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(w)))))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (sym Stream'.WSeq [up(u)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv bf0)) (ap (ap (sym Stream'.WSeq.tail [up(u)]) (fv bf0)) (bv 0)))) (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv bf0)) (bv 1)))))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))
  (dc bf5 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv bf0)) (ap (ap (sym Stream'.WSeq.tail [up(u)]) (fv bf0)) (fv bf4))))))
  (dc bf6 (br EXPLICIT) (dr cdecl) (ty (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))))
  (dc bf7 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (ap (sym Membership.mem [up(u) up(u)]) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u
... [8602 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*9,090 characters*

```text
mta
  smy
    thm: Stream'.WSeq.head_terminates_of_head_tail_terminates
    fl: Mathlib/Data/Seq/WSeq.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u)) sort
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: us(up(v)) sort
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: us(up(w)) sort
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT Stream'.WSeq [up(u)] sym bf0 fv 1 apn INSTANCE_IMPLICIT Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv 1 apn Stream'.WSeq.head [up(u)] sym bf0 fv Stream'.WSeq.tail [up(u)] sym bf0 fv 0 bv 2 apn 2 apn 2 apn Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv 1 apn Stream'.WSeq.head [up(u)] sym bf0 fv 1 bv 2 apn 2 apn pi pi
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: Stream'.WSeq [up(u)] sym bf0 fv 1 apn
  dc bf5
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv 1 apn Stream'.WSeq.head [up(u)] sym bf0 fv Stream'.WSeq.tail [up(u)] sym bf0 fv bf4 fv 2 apn 2 apn 2 apn
  dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: Option [up(u)] sym Prod [up(u) up(u)] sym bf0 fv Stream'.WSeq [up(u)] sym bf0 fv 1 apn 2 apn 1 apn
  dc bf7
    br: EXPLICIT
    dr: cdecl
    ty: Membership.mem [up(u) up(u)] sym Option [up(u)] sym Prod [up(u) up(u)] sym bf0 fv Stream'.WSeq [up(u)] sym bf0 fv 1 apn 2 apn 1 apn Computation [up(u)] sym Option [up(u)] sym Prod [up(u) up(u)]
... [7690 more characters]
```

### FINALIST R_623a343174ec

*10,805 characters*

```text
meta
  summary ;; theorem: Stream'.WSeq.head_terminates_of_head_tail_terminates ;; file: Mathlib/Data/Seq/WSeq.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u)) sort
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(v)) sort
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(w)) sort
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT Stream'.WSeq [up(u)] sym bf0 fv ap INSTANCE_IMPLICIT Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv ap ap Stream'.WSeq.head [up(u)] sym bf0 fv ap Stream'.WSeq.tail [up(u)] sym bf0 fv ap 0 bv ap ap ap Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv ap ap Stream'.WSeq.head [up(u)] sym bf0 fv ap 1 bv ap ap pi pi
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Stream'.WSeq [up(u)] sym bf0 fv ap
  decl bf5 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: Computation.Terminates [up(u)] sym Option [up(u)] sym bf0 fv ap ap Stream'.WSeq.head [up(u)] sym bf0 fv ap Stream'.WSeq.tail [up(u)] sym bf0 fv ap bf4 fv ap ap ap
  decl bf6 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Option [up(u)] sym Prod [up(u) up(u)] sym bf0 fv ap Stream'.WSeq [up(u)] sym bf0 fv ap ap ap
  decl bf7 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Mem
... [9405 more characters]
```

### FINALIST R_8f1e3d8b7028

*11,299 characters*

```text
meta
  summary
    theorem: Stream'.WSeq.head_terminates_of_head_tail_terminates
    file: Mathlib/Data/Seq/WSeq.lean
state_before
  goal bm0
    target: (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))) (ap (ap (sym Stream'.WSeq.destruct [up(u)]) (fv bf0)) (fv bf4)))
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7]
  alias bf0
    tag: sort
  alias bf4
    tag: Stream'.WSeq
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (sort us(up(u)))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (ap (sym Stream'.WSeq [up(u)]) (fv bf0))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (sort us(up(v)))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (sort us(up(w)))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm0
    type: (pi EXPLICIT (ap (sym Stream'.WSeq [up(u)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.head [up(u)]) (fv bf0)) (ap (ap (sym Stream'.WSeq.tail [up(u)]) (fv bf0)) (bv 0)))) (ap (ap (sym Computation.Terminates [up(u)]) (ap (sym Option [up(u)]) (fv bf0))) (ap (ap (sym Stream'.WSeq.h
... [9899 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*21,096 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (ap (ap (sym Membership.mem [up(u) up(u)]) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))) (ap (sym Computation [up(u)]) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0)))))) (ap (sym Computation.instMembership [up(u)]) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0)))))) (fv bf6)) (ap (ap (ap (ap (ap (ap (sym Bind.bind [up(u) up(u)]) (sym Computation [up(u)])) (sym Computation.instBind [up(u)])) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))) (ap (ap (ap (ap (ap (ap (sym Functor.map [up(u) up(u)]) (sym Computation [up(u)])) (ap (ap (sym Applicative.toFunctor [up(u) up(u)]) (sym Computation [up(u)])) (ap (ap (sym Alternative.toApplicative [up(u) up(u)]) (sym Computation [up(u)])) (sym Computation.instAlternativeComputation [up(u)])))) (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))))) (ap (sym Stream'.WSeq [up(u)]) (fv bf0))) (lam EXPLICIT (ap (sym Option [up(u)]) (ap (ap (sym Prod [up(u) up(u)]) (fv bf0)) (ap (sym Stream'.WSeq [up(u)]) (fv bf0)))) (ap (ap (ap (ap (ap (sym Option.rec [us(up(u)
... [19696 more characters]
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
    n: aleph0_le_rank_of_isEmpty_oreSet
    b: EXPLICIT
    d: cdecl
    ∈: pi(EXPLICIT,ap(sym(IsEmpty,[us(up(u_1))]),ap(ap(ap(sym(OreLocalization.OreSet,[up(u_1)]),fv(R~bf0)),ap(ap(sym(MonoidWithZero
... [25977 more characters]
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
    type: (pi EXPLICIT (ap (sym IsEmpty [us(up(u_1))]) (ap (ap (ap (sym OreLocalization.OreSet [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))) (ap (ap (sym nonZeroDivisors [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym Ri
... [22767 more characters]
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
  decl S~bf3 has display is S; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(sym(Submonoid,[up(u_1)]),fv(R~bf0)),ap(ap(sym(MulZeroOneClass.toMulOneClass,[up(u_1)]),fv(R~bf0)),ap(ap(sym(NonAssocSemiring.toMulZeroOneClass,[up(u_1)]),fv(R~bf0)),ap(ap(sym(Semiring.toNonAssocSemiring,[up(u_1)]),fv(R~bf0)),ap(ap(sym(Ring.toSemiring,[up(u_1)]),fv(R~bf0)),fv(inst._@.Mathlib.LinearAlgebra.Dimension.Localization._hyg.1996~bf1)))))) .

... [27540 more characters]
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
    ty: {pi|EXPLICIT,{ap|{sym|IsEmpty,[us{up{u_1}}]},{ap|{ap|{ap|{sym|OreLocalization.OreSet,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MonoidWithZero.toMonoid,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Semiring.toMonoidWithZero,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Ring.toSemiring,[up{u_1}]},{fv|bf0}},{fv|bf1}}}}},{ap|{ap|{sym|nonZeroDivisors,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Semiring.toMonoidWithZero,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Ring.toSemiring,[up{u_1}]},{fv|bf0}},{fv|bf1}}}}}},{ap|{ap|{ap|{ap|{sym|LE.le,[us{up{u_1}}]},{sym|Cardinal,[up{u_1}]}},{sym|Cardinal.instLE,[up{u_
... [22014 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*23,093 characters*

```text
(mta
  (smy (thm aleph0_le_rank_of_isEmpty_oreSet) (fl Mathlib/LinearAlgebra/Dimension/Localization.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Ring [up(u_1)]) (fv bf0))))
  (dc bf2 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym IsDomain [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1)))))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (ap (ap (sym Submonoid [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (sym IsEmpty [us(up(u_1))]) (ap (ap (ap (sym OreLocalization.OreSet [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))) (ap (ap (sym nonZeroDivisors [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1)))))) (ap (ap (ap (ap (sym LE.le [us(up(u_1))]) (sym Cardinal [up(u_1)])) (sym Cardinal.instLE [up(u_1)])) (sym Cardinal.aleph0 [up(u_1)])) (ap (ap (a
... [21693 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*19,976 characters*

```text
mta
  smy
    thm: aleph0_le_rank_of_isEmpty_oreSet
    fl: Mathlib/LinearAlgebra/Dimension/Localization.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Ring [up(u_1)] sym bf0 fv 1 apn
  dc bf2
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: IsDomain [up(u_1)] sym bf0 fv Ring.toSemiring [up(u_1)] sym bf0 fv bf1 fv 2 apn 2 apn
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: Submonoid [up(u_1)] sym bf0 fv MulZeroOneClass.toMulOneClass [up(u_1)] sym bf0 fv NonAssocSemiring.toMulZeroOneClass [up(u_1)] sym bf0 fv Semiring.toNonAssocSemiring [up(u_1)] sym bf0 fv Ring.toSemiring [up(u_1)] sym bf0 fv bf1 fv 2 apn 2 apn 2 apn 2 apn 2 apn
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT IsEmpty [us(up(u_1))] sym OreLocalization.OreSet [up(u_1)] sym bf0 fv MonoidWithZero.toMonoid [up(u_1)] sym bf0 fv Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv Ring.toSemiring [up(u_1)] sym bf0 fv bf1 fv 2 apn 2 apn 2 apn nonZeroDivisors [up(u_1)] sym bf0 fv Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv Ring.toSemiring [up(u_1)] sym bf0 fv bf1 fv 2 apn 2 apn 2 apn 3 apn 1 apn LE.le [us(up(u_1))] sym Cardinal [up(u_1)] sym Cardinal.instLE [up(u_1)] sym Cardinal.aleph0 [up(u_1)] sym Module.rank [up(u_1) up(u_1)] sym bf0 fv bf0 fv Ring.toSemiring [up(u_1)] sym bf0 fv bf1 fv 2 apn NonUnitalNonAssocSemiring.toAddCommMo
... [18576 more characters]
```

### FINALIST R_623a343174ec

*22,668 characters*

```text
meta
  summary ;; theorem: aleph0_le_rank_of_isEmpty_oreSet ;; file: Mathlib/LinearAlgebra/Dimension/Localization.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: Ring [up(u_1)] sym bf0 fv ap
  decl bf2 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: IsDomain [up(u_1)] sym bf0 fv ap Ring.toSemiring [up(u_1)] sym bf0 fv ap bf1 fv ap ap
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Submonoid [up(u_1)] sym bf0 fv ap MulZeroOneClass.toMulOneClass [up(u_1)] sym bf0 fv ap NonAssocSemiring.toMulZeroOneClass [up(u_1)] sym bf0 fv ap Semiring.toNonAssocSemiring [up(u_1)] sym bf0 fv ap Ring.toSemiring [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap ap
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT IsEmpty [us(up(u_1))] sym OreLocalization.OreSet [up(u_1)] sym bf0 fv ap MonoidWithZero.toMonoid [up(u_1)] sym bf0 fv ap Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv ap Ring.toSemiring [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap nonZeroDivisors [up(u_1)] sym bf0 fv ap Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv ap Ring.toSemiring [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap ap LE.le [us(up(u_1))] sym Cardinal [up(u_1)] sym ap Cardinal.instLE [up(u_1)] sym ap Cardinal.aleph0 [up(u_1
... [21268 more characters]
```

### FINALIST R_8f1e3d8b7028

*24,643 characters*

```text
meta
  summary
    theorem: aleph0_le_rank_of_isEmpty_oreSet
    file: Mathlib/LinearAlgebra/Dimension/Localization.lean
state_before
  goal bm2
    target: (ap (ap (ap (ap (sym LE.le [us(um(u0))]) (sym Cardinal [um(u0)])) (sym Cardinal.instLE [um(u0)])) (ap (ap (ap (sym Nat.cast [us(um(u0))]) (sym Cardinal [um(u0)])) (sym Cardinal.instNatCast [um(u0)])) (fv bf8))) (mv bm0))
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8]
  alias bf8
    tag: metavariable_reference
  decl bf8
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (mv bm1)
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (sym Ring [up(u_1)]) (fv bf0))
  decl bf2
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (ap (sym IsDomain [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1)))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (ap (sym Submonoid [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv
... [23243 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*67,465 characters*

```text
aliases
  alias $a0
    term: (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (sym Subtype [us(up(u_1))]) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (ap (sym Submonoid [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))))) (ap (ap (ap (sym SetLike.instMembership [up(u_1) up(u_1)]) (ap (ap (sym Submonoid [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))))) (fv bf0)) (ap (ap (sym Submonoid.instSetLike [up(u_1)]) (fv bf0)) (ap (ap (sym MulZeroOneClass.toMulOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym NonAssocSemiring.toMulZeroOneClass [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1)))))))) (bv 0)) (ap (ap (sym nonZeroDivisors [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym Ring.toSemiring [up(u_1)]) (fv bf0)) (fv bf1))))))) (ap (ap (ap (sym Ne 
... [66065 more characters]
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
    ∈: ap(ap(ap(ap(ap(ap(sym(Filter.EventuallyLE,[up(u_1) u0]),fv(α~bf0)),sym(Real,[])),sym(Real.instLE,[])),ap(ap(ap(ap(ap(sym(MeasureTheory.ae,[up(u_1) up(u_1)]),fv(α~bf0)),ap(ap(sym(MeasureTheory.Measure,[up(u_1)]),fv(α~bf0)),fv(inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1))),ap(ap(sym(MeasureTheory.Measure.instFunLike,[up(u_1)]),fv(α~bf0)),fv(inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1))),ap(ap(sym(MeasureTheory.Measure.instOuterMeasureClass,[up(u_1)]),fv(α~bf0)),fv(inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1))),fv(μ~bf3))),ap(ap(ap(sym(OfNat.ofNat,[up(u_1)]),p
... [26825 more characters]
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
    type: (ap (ap (ap (ap (ap (ap (sym Filter.EventuallyLE [up(u_1) u0]) (fv bf0)) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (ap (sym MeasureTheory.ae [up(u_1) up(u_1)]) (fv bf0)) (ap (ap (sym MeasureTheory.Measure [up(u_1)]) (fv bf0)) (fv bf1))) (ap (ap (sym MeasureTheory.Measure.instFunLike [up(u_1)]) (fv bf0)) (fv bf1))) (ap (ap (sym MeasureTheory.Measure.instOuterMeasureClass [up(u_1)]) (fv bf0)) (fv bf1))) (fv bf3))) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (pi EXPLICIT (fv bf0) (sym Real []))) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (pi EXPLICIT (fv bf0) (sym Real []))) (ap (ap (ap (sym Pi.instZero [up(u_1) u0]) (fv bf0)) (lam EXPLICIT (fv bf0) (sym Real []))) (lam 
... [27138 more characters]
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
  decl f_nn~bf4 has display is f_nn; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(ap(ap(ap(sym(Filter.EventuallyLE,[up(u_1) u0]),fv(α~bf0)),sym(Real,[])),sym(Real.instLE,[])),ap(ap(ap(ap(ap(sym(MeasureTheory.ae,[up(u_1) up(u_1)]),fv(α~bf0)),ap(ap(sym(MeasureTheory.Measure,[up(u_1)]),fv(α~bf0)),fv(inst._@.Mathlib.Analysis.SpecialFunctions.Pow.Integral._hyg.50~bf1))),ap(ap(sym(MeasureTheory.Measure.instFunLike,[up(
... [29146 more characters]
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
    ty: {ap|{ap|{ap|{ap|{ap|{ap|{sym|Filter.EventuallyLE,[up{u_1} u0]},{fv|bf0}},{sym|Real,[]}},{sym|Real.instLE,[]}},{ap|{ap|{ap|{ap|{ap|{sym|MeasureTheory.ae,[up{u_1} up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MeasureTheory.Measure,[up{u_1}]},{fv|bf0}},{fv|bf1}}},{ap|{ap|{sym|MeasureTheory.Measure.instFunLike,[up{u_1}]},{fv|bf0}},{fv|bf1}}},{ap|{ap|{sym|MeasureTheory.Measure.instOuterMeasureClass,[up{u_1}]},{fv|bf0}},{fv|bf1}}},{fv|bf3}}},{ap|{ap|{ap|{sym|OfNat.ofNat,[up{u_1}]},{pi|EXPLICIT,{fv|bf0},{sym|Real,[]}}},{lit|NAT,0}},{ap|{ap|{sym|Zero.toOfNat0,[up{u_1}]},{pi|EXPLICIT,{fv|bf0},{sym|Real,[]}}},{ap|{ap|{ap|{sym|Pi.instZero,[up{u_1} u0]},{fv|bf0}},{lam|EXPLICIT,{fv|bf0},{sym|Real,[]}}},{lam|EXPLICIT,{fv|bf0},{sym|Real.instZero,[]}}}}}},{fv|bf2}}
  - dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{ap|{ap|{sym|AEMeasura
... [26070 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*26,930 characters*

```text
(mta
  (smy (thm MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul) (fl Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym MeasurableSpace [up(u_1)]) (fv bf0))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (fv bf0) (sym Real []))))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (ap (ap (sym MeasureTheory.Measure [up(u_1)]) (fv bf0)) (fv bf1))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (ap (ap (sym Filter.EventuallyLE [up(u_1) u0]) (fv bf0)) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (ap (sym MeasureTheory.ae [up(u_1) up(u_1)]) (fv bf0)) (ap (ap (sym MeasureTheory.Measure [up(u_1)]) (fv bf0)) (fv bf1))) (ap (ap (sym MeasureTheory.Measure.instFunLike [up(u_1)]) (fv bf0)) (fv bf1))) (ap (ap (sym MeasureTheory.Measure.instOuterMeasureClass [up(u_1)]) (fv bf0)) (fv bf1))) (fv bf3))) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (pi EXPLICIT (fv bf0) (sym Real []))) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (pi EXPLICIT (fv bf0) (sym Real []))) (ap (ap (ap (sym Pi.instZero [up(u_1) u0]) (fv bf0)) (lam EXPLICIT (fv bf0) (sym Real []))) (lam EXPLICIT (fv bf0) (sym Real.instZero [])))))) (fv bf2))))
  (dc bf5 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (ap (ap (sym AEMeasurable [up(u_1) u0]) (fv bf0)) (sym Real [])) (sym Real.measu
... [25530 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*22,931 characters*

```text
mta
  smy
    thm: MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul
    fl: Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: MeasurableSpace [up(u_1)] sym bf0 fv 1 apn
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: EXPLICIT bf0 fv Real [] sym pi
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: MeasureTheory.Measure [up(u_1)] sym bf0 fv bf1 fv 2 apn
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: Filter.EventuallyLE [up(u_1) u0] sym bf0 fv Real [] sym Real.instLE [] sym MeasureTheory.ae [up(u_1) up(u_1)] sym bf0 fv MeasureTheory.Measure [up(u_1)] sym bf0 fv bf1 fv 2 apn MeasureTheory.Measure.instFunLike [up(u_1)] sym bf0 fv bf1 fv 2 apn MeasureTheory.Measure.instOuterMeasureClass [up(u_1)] sym bf0 fv bf1 fv 2 apn bf3 fv 5 apn OfNat.ofNat [up(u_1)] sym EXPLICIT bf0 fv Real [] sym pi NAT 0 lit Zero.toOfNat0 [up(u_1)] sym EXPLICIT bf0 fv Real [] sym pi Pi.instZero [up(u_1) u0] sym bf0 fv EXPLICIT bf0 fv Real [] sym lam EXPLICIT bf0 fv Real.instZero [] sym lam 3 apn 2 apn 3 apn bf2 fv 6 apn
  dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: AEMeasurable [up(u_1) u0] sym bf0 fv Real [] sym Real.measurableSpace [] sym bf1 fv bf2 fv bf3 fv 6 apn
  dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: Real [] sym
  dc bf7
    br: EXPLICIT
    dr: cdecl
    ty: LT.lt 
... [21531 more characters]
```

### FINALIST R_623a343174ec

*27,045 characters*

```text
meta
  summary ;; theorem: MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul ;; file: Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: MeasurableSpace [up(u_1)] sym bf0 fv ap
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT bf0 fv Real [] sym pi
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: MeasureTheory.Measure [up(u_1)] sym bf0 fv ap bf1 fv ap
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Filter.EventuallyLE [up(u_1) u0] sym bf0 fv ap Real [] sym ap Real.instLE [] sym ap MeasureTheory.ae [up(u_1) up(u_1)] sym bf0 fv ap MeasureTheory.Measure [up(u_1)] sym bf0 fv ap bf1 fv ap ap MeasureTheory.Measure.instFunLike [up(u_1)] sym bf0 fv ap bf1 fv ap ap MeasureTheory.Measure.instOuterMeasureClass [up(u_1)] sym bf0 fv ap bf1 fv ap ap bf3 fv ap ap OfNat.ofNat [up(u_1)] sym EXPLICIT bf0 fv Real [] sym pi ap NAT 0 lit ap Zero.toOfNat0 [up(u_1)] sym EXPLICIT bf0 fv Real [] sym pi ap Pi.instZero [up(u_1) u0] sym bf0 fv ap EXPLICIT bf0 fv Real [] sym lam ap EXPLICIT bf0 fv Real.instZero [] sym lam ap ap ap ap bf2 fv ap
  decl bf5 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: AEMeasurable [up(u_1) u0] sym b
... [25645 more characters]
```

### FINALIST R_8f1e3d8b7028

*29,218 characters*

```text
meta
  summary
    theorem: MeasureTheory.lintegral_rpow_eq_lintegral_meas_le_mul
    file: Mathlib/Analysis/SpecialFunctions/Pow/Integral.lean
state_before
  goal bm12
    target: (ann (ap (ap (ap (sym Eq [us(u0)]) (sym ENNReal [])) (ap (ap (ap (ap (sym MeasureTheory.lintegral [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf3)) (lam EXPLICIT (fv bf0) (ap (sym ENNReal.ofReal []) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (ap (sym instHPow [u0 u0]) (sym Real [])) (sym Real [])) (sym Real.instPow []))) (ap (fv bf2) (bv 0))) (fv bf6)))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym ENNReal [])) (sym ENNReal [])) (sym ENNReal [])) (ap (ap (sym instHMul [u0]) (sym ENNReal [])) (ap (ap (sym CanonicallyOrderedCommSemiring.toMul [u0]) (sym ENNReal [])) (sym ENNReal.instCanonicallyOrderedCommSemiring [])))) (ap (sym ENNReal.ofReal []) (fv bf6))) (ap (ap (ap (ap (sym MeasureTheory.lintegral [u0]) (sym Real [])) (ap (ap (sym MeasureTheory.MeasureSpace.toMeasurableSpace [u0]) (sym Real [])) (sym Real.measureSpace []))) (ap (ap (ap (ap (sym MeasureTheory.Measure.restrict [u0]) (sym Real [])) (ap (ap (sym MeasureTheory.MeasureSpace.toMeasurableSpace [u0]) (sym Real [])) (sym Real.measureSpace []))) (ap (ap (sym MeasureTheory.MeasureSpace.volume [u0]) (sym Real [])) (sym Real.measureSpace []))) (ap (ap (ap (sym Set.Ioi [u0]) (sym R
... [27818 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*43,899 characters*

```text
aliases
  alias $a0
    term: (ann (ap (ap (ap (sym Eq [us(u0)]) (sym ENNReal [])) (ap (ap (ap (ap (sym MeasureTheory.lintegral [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf3)) (lam EXPLICIT (fv bf0) (ap (sym ENNReal.ofReal []) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (ap (sym instHPow [u0 u0]) (sym Real [])) (sym Real [])) (sym Real.instPow []))) (ap (fv bf2) (bv 0))) (fv bf6)))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym ENNReal [])) (sym ENNReal [])) (sym ENNReal [])) (ap (ap (sym instHMul [u0]) (sym ENNReal [])) (ap (ap (sym CanonicallyOrderedCommSemiring.toMul [u0]) (sym ENNReal [])) (sym ENNReal.instCanonicallyOrderedCommSemiring [])))) (ap (sym ENNReal.ofReal []) (fv bf6))) (ap (ap (ap (ap (sym MeasureTheory.lintegral [u0]) (sym Real [])) (ap (ap (sym MeasureTheory.MeasureSpace.toMeasurableSpace [u0]) (sym Real [])) (sym Real.measureSpace []))) (ap (ap (ap (ap (sym MeasureTheory.Measure.restrict [u0]) (sym Real [])) (ap (ap (sym MeasureTheory.MeasureSpace.toMeasurableSpace [u0]) (sym Real [])) (sym Real.measureSpace []))) (ap (ap (sym MeasureTheory.MeasureSpace.volume [u0]) (sym Real [])) (sym Real.measureSpace []))) (ap (ap (ap (sym Set.Ioi [u0]) (sym Real [])) (sym Real.instPreorder [])) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Real [])) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [u0]) (sym Real [])) (sy
... [42499 more characters]
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
    ∈: pi(INSTANCE_IMPLICIT,ap(sym(CommMonoidWithZero,[up(u_1)]),fv(α~bf0)),pi(INSTANCE_IMPLICIT,ap(ap(sym(WfDvdMonoid,[up(u_1)]),fv(α~bf0)),bv(0)),pi(IMPLICIT,fv(α~bf0),pi(IMPLICIT,fv(α~bf0),pi(EXPLICIT,ap(ap(ap(sym(Ne,[us(up(u_1))]),fv(α~bf0)),bv(1)),ap(ap(ap(sym(OfNat.ofNat,[up(u_1)]),fv(α~bf0)),lit(NAT,0)),ap(ap(sym(Zero.toOfNat0,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toZero,[up(u_1)]),fv(α~bf0)),bv(3))))),pi(EXPLICIT,ap(sym(Not,[]),ap(ap(ap(sym(IsUnit,[up(u_1)]),fv(α~bf0)),ap(ap(sym(MonoidWithZero.toMonoid,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toMonoidWithZero,[up(u_1)]),fv(α~bf0)),bv(4)))),bv(1))),ap(ap(sym(Exists,[us(u0)]),sym(Nat,[])),lam(EXPLICIT,sym(Nat,[]),ap(ap(sym(Exists,[us(up(u_1))]),fv(α~bf0)),lam(EXPLICIT,fv(α~bf0),ap(ap(sym(And,[]),ap(sym(Not,[]),ap(ap(ap(ap(sym(Dvd.dvd,[up(u_1)]),fv(α~bf0)),ap(ap(sym(semigroupDvd,[up(u_1)]),fv(α~bf0)),ap(ap(sym(SemigroupWithZero.toSemigroup,[up(u_1)]),fv(α~bf0)),ap(ap(sym(MonoidWithZero.toSemigroupWithZero,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toMonoidWithZero,[up(u_1)]),fv(α~bf0)),bv(7)))))),bv(4)),bv(0)))),ap(ap(ap(sym(Eq,[us(up(u_1)
... [15042 more characters]
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
    type: (pi INSTANCE_IMPLICIT (ap (sym CommMonoidWithZero [up(u_1)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym WfDvdMonoid [up(u_1)]) (fv bf0)) (bv 0)) (pi IMPLICIT (fv bf0) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (sym Ne [us(up(u_1))]) (fv bf0)) (bv 1)) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (fv bf0)) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toZero [up(u_1)]) (fv bf0)) (bv 3))))) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (sym IsUnit [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 4)))) (bv 1))) (ap (ap (sym Exists [us(u0)]) (sym Nat [])) (lam EXPLICIT (sym Nat []) (ap (ap (sym Exists [us(up(u_1))]) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (sym And []) (ap (sym Not []) (ap (ap (ap (ap (sym Dvd.dvd [up(u_1)]) (fv bf0)) (ap (ap (sym semigroupDvd [up(u_1)]) (fv bf0)) (ap (ap (sym SemigroupWithZero.toSemigroup [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toSemigroupWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.
... [13871 more characters]
```

### SEED_STRUCTURED_ENGLISH

*17,839 characters*

```text
In meta:
  summary has theorem is WfDvdMonoid.max_power_factor'; and file is Mathlib/RingTheory/UniqueFactorizationDomain.lean .
In state_before:
  decl α~bf0 has display is α; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sort(us(up(u_1))) .
  decl max_power_factor'~bf1 has display is max_power_factor'; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(INSTANCE_IMPLICIT,ap(sym(CommMonoidWithZero,[up(u_1)]),fv(α~bf0)),pi(INSTANCE_IMPLICIT,ap(ap(sym(WfDvdMonoid,[up(u_1)]),fv(α~bf0)),bv(0)),pi(IMPLICIT,fv(α~bf0),pi(IMPLICIT,fv(α~bf0),pi(EXPLICIT,ap(ap(ap(sym(Ne,[us(up(u_1))]),fv(α~bf0)),bv(1)),ap(ap(ap(sym(OfNat.ofNat,[up(u_1)]),fv(α~bf0)),lit(NAT,0)),ap(ap(sym(Zero.toOfNat0,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toZero,[up(u_1)]),fv(α~bf0)),bv(3))))),pi(EXPLICIT,ap(sym(Not,[]),ap(ap(ap(sym(IsUnit,[up(u_1)]),fv(α~bf0)),ap(ap(sym(MonoidWithZero.toMonoid,[up(u_1)]),fv(α~bf0)),ap(ap(sym(CommMonoidWithZero.toMonoidWithZero,[up(u_1)]),fv(α~bf0)),bv(4)))),bv(1))),ap(ap(sym(Exists,[us(u0)]),sym(Nat,[])),lam(EXPLICIT,sym(Nat,[]),ap(ap(sym(Exists,[us(up(u_1))]),fv(α~bf0)),lam(EXPLICIT,fv(α~bf0),ap(ap(sym(And,[]),ap(sym(Not,[]),ap(ap(ap(ap(sym(Dvd.dvd,[up(u_1)]),fv(α~bf0)),ap(ap(sym(semigroupDvd,[up(u_1)]),fv(α~bf0)),ap(ap(sym(SemigroupWithZero.toSemigroup,[up(u_1)]),fv(α~bf0)),ap(ap(sym(MonoidWithZero.toSemigroupWithZero,[up(u
... [16439 more characters]
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
    ty: {pi|INSTANCE_IMPLICIT,{ap|{sym|CommMonoidWithZero,[up{u_1}]},{fv|bf0}},{pi|INSTANCE_IMPLICIT,{ap|{ap|{sym|WfDvdMonoid,[up{u_1}]},{fv|bf0}},{bv|0}},{pi|IMPLICIT,{fv|bf0},{pi|IMPLICIT,{fv|bf0},{pi|EXPLICIT,{ap|{ap|{ap|{sym|Ne,[us{up{u_1}}]},{fv|bf0}},{bv|1}},{ap|{ap|{ap|{sym|OfNat.ofNat,[up{u_1}]},{fv|bf0}},{lit|NAT,0}},{ap|{ap|{sym|Zero.toOfNat0,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|CommMonoidWithZero.toZero,[up{u_1}]},{fv|bf0}},{bv|3}}}}},{pi|EXPLICIT,{ap|{sym|Not,[]},{ap|{ap|{ap|{sym|IsUnit,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MonoidWithZero.toMonoid,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|CommMonoidWithZero.toMonoidWithZero,[up{u_1}]},{fv|bf0}},{bv|4}}}},{bv|1}}},{ap|{ap|{sym|Exists,[us{u0}]},{sym|Nat,[]}},{lam|EXPLICIT,{sym|Nat,[]},{ap|{ap|{sym|Exists,[us{up{u_1}}]},{fv|bf0}},{lam|EXPLICIT,{fv|bf0},{ap|{ap|{sym|And,[]},{ap|{sym|Not,[]},{ap|{ap|{ap|{ap|{sym|Dvd.dvd,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|semigroupDvd,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|SemigroupWithZero.toSemigroup,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MonoidWithZero.toSemigroupWithZero,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|CommMonoidWithZero.toMonoidWithZero,[up{u_1}]},{fv|bf0}},{bv|7}}}}}},{bv|4}},{bv|0}}}},{
... [13173 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*14,318 characters*

```text
(mta
  (smy (thm WfDvdMonoid.max_power_factor') (fl Mathlib/RingTheory/UniqueFactorizationDomain.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br EXPLICIT) (dr cdecl) (ty (pi INSTANCE_IMPLICIT (ap (sym CommMonoidWithZero [up(u_1)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym WfDvdMonoid [up(u_1)]) (fv bf0)) (bv 0)) (pi IMPLICIT (fv bf0) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (sym Ne [us(up(u_1))]) (fv bf0)) (bv 1)) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (fv bf0)) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toZero [up(u_1)]) (fv bf0)) (bv 3))))) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (sym IsUnit [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 4)))) (bv 1))) (ap (ap (sym Exists [us(u0)]) (sym Nat [])) (lam EXPLICIT (sym Nat []) (ap (ap (sym Exists [us(up(u_1))]) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (sym And []) (ap (sym Not []) (ap (ap (ap (ap (sym Dvd.dvd [up(u_1)]) (fv bf0)) (ap (ap (sym semigroupDvd [up(u_1)]) (fv bf0)) (ap (ap (sym SemigroupWithZero.toSemigroup [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toSemigroupWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 7)))))) (bv 4)) (bv 0)))) (ap (ap (ap (sym Eq [us
... [12918 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*12,168 characters*

```text
mta
  smy
    thm: WfDvdMonoid.max_power_factor'
    fl: Mathlib/RingTheory/UniqueFactorizationDomain.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: EXPLICIT
    dr: cdecl
    ty: INSTANCE_IMPLICIT CommMonoidWithZero [up(u_1)] sym bf0 fv 1 apn INSTANCE_IMPLICIT WfDvdMonoid [up(u_1)] sym bf0 fv 0 bv 2 apn IMPLICIT bf0 fv IMPLICIT bf0 fv EXPLICIT Ne [us(up(u_1))] sym bf0 fv 1 bv OfNat.ofNat [up(u_1)] sym bf0 fv NAT 0 lit Zero.toOfNat0 [up(u_1)] sym bf0 fv CommMonoidWithZero.toZero [up(u_1)] sym bf0 fv 3 bv 2 apn 2 apn 3 apn 3 apn EXPLICIT Not [] sym IsUnit [up(u_1)] sym bf0 fv MonoidWithZero.toMonoid [up(u_1)] sym bf0 fv CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym bf0 fv 4 bv 2 apn 2 apn 1 bv 3 apn 1 apn Exists [us(u0)] sym Nat [] sym EXPLICIT Nat [] sym Exists [us(up(u_1))] sym bf0 fv EXPLICIT bf0 fv And [] sym Not [] sym Dvd.dvd [up(u_1)] sym bf0 fv semigroupDvd [up(u_1)] sym bf0 fv SemigroupWithZero.toSemigroup [up(u_1)] sym bf0 fv MonoidWithZero.toSemigroupWithZero [up(u_1)] sym bf0 fv CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym bf0 fv 7 bv 2 apn 2 apn 2 apn 2 apn 4 bv 0 bv 4 apn 1 apn Eq [us(up(u_1))] sym bf0 fv 5 bv HMul.hMul [up(u_1) up(u_1) up(u_1)] sym bf0 fv bf0 fv bf0 fv instHMul [up(u_1)] sym bf0 fv MulZeroClass.toMul [up(u_1)] sym bf0 fv MulZeroOneClass.toMulZeroClass [up(u_1)] sym bf0 fv MonoidWithZero.toMulZero
... [10768 more characters]
```

### FINALIST R_623a343174ec

*15,103 characters*

```text
meta
  summary ;; theorem: WfDvdMonoid.max_power_factor' ;; file: Mathlib/RingTheory/UniqueFactorizationDomain.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: INSTANCE_IMPLICIT CommMonoidWithZero [up(u_1)] sym bf0 fv ap INSTANCE_IMPLICIT WfDvdMonoid [up(u_1)] sym bf0 fv ap 0 bv ap IMPLICIT bf0 fv IMPLICIT bf0 fv EXPLICIT Ne [us(up(u_1))] sym bf0 fv ap 1 bv ap OfNat.ofNat [up(u_1)] sym bf0 fv ap NAT 0 lit ap Zero.toOfNat0 [up(u_1)] sym bf0 fv ap CommMonoidWithZero.toZero [up(u_1)] sym bf0 fv ap 3 bv ap ap ap ap EXPLICIT Not [] sym IsUnit [up(u_1)] sym bf0 fv ap MonoidWithZero.toMonoid [up(u_1)] sym bf0 fv ap CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym bf0 fv ap 4 bv ap ap ap 1 bv ap ap Exists [us(u0)] sym Nat [] sym ap EXPLICIT Nat [] sym Exists [us(up(u_1))] sym bf0 fv ap EXPLICIT bf0 fv And [] sym Not [] sym Dvd.dvd [up(u_1)] sym bf0 fv ap semigroupDvd [up(u_1)] sym bf0 fv ap SemigroupWithZero.toSemigroup [up(u_1)] sym bf0 fv ap MonoidWithZero.toSemigroupWithZero [up(u_1)] sym bf0 fv ap CommMonoidWithZero.toMonoidWithZero [up(u_1)] sym bf0 fv ap 7 bv ap ap ap ap ap 4 bv ap 0 bv ap ap ap Eq [us(up(u_1))] sym bf0 fv ap 5 bv ap HMul.hMul [up(u_1) up(u_1) up(u_1)] sym bf0 fv ap bf0 fv ap bf0 fv ap instHMul [up(u_1)] sym bf0 fv ap MulZeroClass.toM
... [13703 more characters]
```

### FINALIST R_8f1e3d8b7028

*15,571 characters*

```text
meta
  summary
    theorem: WfDvdMonoid.max_power_factor'
    file: Mathlib/RingTheory/UniqueFactorizationDomain.lean
state_before
  goal bm1
    target: (mv bm0)
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9]
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm1
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm1
    type: (pi INSTANCE_IMPLICIT (ap (sym CommMonoidWithZero [up(u_1)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym WfDvdMonoid [up(u_1)]) (fv bf0)) (bv 0)) (pi IMPLICIT (fv bf0) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (sym Ne [us(up(u_1))]) (fv bf0)) (bv 1)) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (fv bf0)) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toZero [up(u_1)]) (fv bf0)) (bv 3))))) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (sym IsUnit [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 4)))) (bv 1))) (ap (ap (sym Exists [us(u0)]) (sym Nat [])) (lam EXPLICIT (sym Nat []) (ap (ap (sym Exists [us(up(u_1))]) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (sym And []) (ap (sym Not []) (ap (ap (ap (ap (sym Dvd.dvd [up(u_1)]) (fv bf0)) (ap (ap (sym semigroupDvd [up(u_1)]) (fv bf0)) (ap (ap (sym SemigroupWithZero.toSemigroup [up(u
... [14171 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*50,155 characters*

```text
aliases
  alias $a0
    term: (pi INSTANCE_IMPLICIT (ap (sym CommMonoidWithZero [up(u_1)]) (fv bf0)) (pi INSTANCE_IMPLICIT (ap (ap (sym WfDvdMonoid [up(u_1)]) (fv bf0)) (bv 0)) (pi IMPLICIT (fv bf0) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (sym Ne [us(up(u_1))]) (fv bf0)) (bv 1)) (ap (ap (ap (sym OfNat.ofNat [up(u_1)]) (fv bf0)) (lit NAT 0)) (ap (ap (sym Zero.toOfNat0 [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toZero [up(u_1)]) (fv bf0)) (bv 3))))) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (sym IsUnit [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 4)))) (bv 1))) (ap (ap (sym Exists [us(u0)]) (sym Nat [])) (lam EXPLICIT (sym Nat []) (ap (ap (sym Exists [us(up(u_1))]) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (sym And []) (ap (sym Not []) (ap (ap (ap (ap (sym Dvd.dvd [up(u_1)]) (fv bf0)) (ap (ap (sym semigroupDvd [up(u_1)]) (fv bf0)) (ap (ap (sym SemigroupWithZero.toSemigroup [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toSemigroupWithZero [up(u_1)]) (fv bf0)) (ap (ap (sym CommMonoidWithZero.toMonoidWithZero [up(u_1)]) (fv bf0)) (bv 7)))))) (bv 4)) (bv 0)))) (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf0)) (bv 5)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf0)) (fv bf0)) (fv bf0)) (ap (ap (sym instHMul [up(u_1)]) (fv bf0)) (ap (ap (s
... [48755 more characters]
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
    ∈: pi(EXPLICIT,sym(Nat,[]),pi(EXPLICIT,sym(Nat,[]),ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Finset,[u0]),sym(Nat,[]))),ap(ap(ap(ap(ap(sym(Finset.image,[u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(instDecidableEqNat,[])),lam(EXPLICIT,sym(Nat,[]),ap(ap(ap(ap(ap(ap(sym(HMod.hMod,[u0 u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(Nat,[])),ap(ap(sym(instHMod,[u0]),sym(Nat,[])),sym(Nat.instMod,[]))),bv(0)),bv(1)))),ap(ap(ap(ap(ap(sym(Finset.Ico,[u0]),sym(Nat,[])),ap(ap(sym(PartialOrder.toPreorder,[u0]),sym(Nat,[])),ap(ap(sym(SemilatticeInf.toPartialOrder,[u0]),sym(Nat,[])),ap(ap(sym(Lattice.toSemilatticeInf,[u0]),sym(Nat,[])),ap(ap(sym(DistribLattice.toLattice,[u0]),sym(Nat,[])),sym(instDistribLatticeNat,[])))))),sym(Nat.instLocallyFiniteOrder,[])),bv(1)),ap(ap(ap(ap(ap(ap(sym(HAdd.hAdd,[u0 u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(Nat,[])),ap(ap(sym(instHAdd,[u0]),sym(Nat,[])),sym(instAddNat,[]))),bv(1)),bv(0))))),ap(sym(Finset.range,[]),bv(0)))))
  D n~bf4
    n: n
    b: EXPLICIT
    d: cdecl
    ∈: sym(Nat,[])
  D a~bf5
    n: a
    b: EXPLICIT
    d: cd
... [9347 more characters]
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
    type: (pi EXPLICIT (sym Nat []) (pi EXPLICIT (sym Nat []) (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (ap (sym Finset.image [u0 u0]) (sym Nat [])) (sym Nat [])) (sym instDecidableEqNat [])) (lam EXPLICIT (sym Nat []) (ap (ap (ap (ap (ap (ap (sym HMod.hMod [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHMod [u0]) (sym Nat [])) (sym Nat.instMod []))) (bv 0)) (bv 1)))) (ap (ap (ap (ap (ap (sym Finset.Ico [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (bv 1)) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHAdd [u0]) (sym Nat [])) (sym instAddNat [])
... [10750 more characters]
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
  decl image_Ico_mod~bf3 has display is image_Ico_mod; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,sym(Nat,[]),pi(EXPLICIT,sym(Nat,[]),ap(ap(ap(sym(Eq,[us(u0)]),ap(sym(Finset,[u0]),sym(Nat,[]))),ap(ap(ap(ap(ap(sym(Finset.image,[u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(instDecidableEqNat,[])),lam(EXPLICIT,sym(Nat,[]),ap(ap(ap(ap(ap(ap(sym(HMod.hMod,[u0 u0 u0]),sym(Nat,[])),sym(Nat,[])),sym(Nat,[])),ap(ap(sym(instHMod,[u0]),sym(Nat,[])),sym(Nat.instMod,[]))),bv(0)),bv(1)))),ap(ap(ap(ap(ap(sym(Finset.Ico,[u0]),sym(Nat,[])),ap(ap(sym(PartialOrder.toPreorder,[u0]),sym(Nat,[])),ap(ap(sym(SemilatticeInf.toPartialOrder,[u0]),sym(Nat,[])),ap(ap(sym(Lattice.toSemilatticeInf,[u0]),sym(Nat,[])),ap(ap(sym(DistribLattice.toLattice,[u0]),sym(Nat,[])),sym(instDistribLatticeNat,[])))))),sym(Nat.instLocallyFiniteOrder,[])),bv(1)),ap(ap(ap(ap(ap(ap(sym(HAdd.hAdd,[u0 u0 u0]),sym(Nat,[])),sym(Nat,
... [11072 more characters]
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
    ty: {pi|EXPLICIT,{sym|Nat,[]},{pi|EXPLICIT,{sym|Nat,[]},{ap|{ap|{ap|{sym|Eq,[us{u0}]},{ap|{sym|Finset,[u0]},{sym|Nat,[]}}},{ap|{ap|{ap|{ap|{ap|{sym|Finset.image,[u0 u0]},{sym|Nat,[]}},{sym|Nat,[]}},{sym|instDecidableEqNat,[]}},{lam|EXPLICIT,{sym|Nat,[]},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HMod.hMod,[u0 u0 u0]},{sym|Nat,[]}},{sym|Nat,[]}},{sym|Nat,[]}},{ap|{ap|{sym|instHMod,[u0]},{sym|Nat,[]}},{sym|Nat.instMod,[]}}},{bv|0}},{bv|1}}}},{ap|{ap|{ap|{ap|{ap|{sym|Finset.Ico,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|PartialOrder.toPreorder,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|SemilatticeInf.toPartialOrder,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|Lattice.toSemilatticeInf,[u0]},{sym|Nat,[]}},{ap|{ap|{sym|DistribLattice.toLattice,[u0]},{sym|Nat,[]}},{sym|instDistribLatticeNat,[]}}}}}},{sym|Nat.instLocallyFiniteOrder,[]}},{bv|1}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HAdd.hAdd,[u0 u0 u0]},{sym|Nat,[]}},{sym|Nat,[]}},{sym|Nat,[]}},{ap|{ap|{sym|instHAdd,[u0]},{sym|Nat,[]}},{sym|instAddNat,[]}}},{bv|1}},{bv|0}}}}},{ap|{sym|Finset.range,[]},{bv|0}}}}}
  - dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: {sym|Nat,[
... [9912 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*10,967 characters*

```text
(mta
  (smy (thm Nat.image_Ico_mod) (fl Mathlib/Order/Interval/Finset/Nat.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (sym Nat []) (pi EXPLICIT (sym Nat []) (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (ap (sym Finset.image [u0 u0]) (sym Nat [])) (sym Nat [])) (sym instDecidableEqNat [])) (lam EXPLICIT (sym Nat []) (ap (ap (ap (ap (ap (ap (sym HMod.hMod [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHMod [u0]) (sym Nat [])) (sym Nat.instMod []))) (bv 0)) (bv 1)))) (ap (ap (ap (ap (ap (sym Finset.Ico [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (bv 1)) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHAdd [u0]) (sym Nat [])) (sym instAddNat []))) (bv 1)) (bv 0))))) (ap (sym Finset.range []) (bv 0)))))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (sym Nat [])))
  (dc bf5 (br EXPLICIT) (dr cdecl) (ty (sym 
... [9567 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*9,312 characters*

```text
mta
  smy
    thm: Nat.image_Ico_mod
    fl: Mathlib/Order/Interval/Finset/Nat.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: Nat [] sym
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: Nat [] sym
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: Nat [] sym
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT Nat [] sym EXPLICIT Nat [] sym Eq [us(u0)] sym Finset [u0] sym Nat [] sym 1 apn Finset.image [u0 u0] sym Nat [] sym Nat [] sym instDecidableEqNat [] sym EXPLICIT Nat [] sym HMod.hMod [u0 u0 u0] sym Nat [] sym Nat [] sym Nat [] sym instHMod [u0] sym Nat [] sym Nat.instMod [] sym 2 apn 0 bv 1 bv 6 apn lam Finset.Ico [u0] sym Nat [] sym PartialOrder.toPreorder [u0] sym Nat [] sym SemilatticeInf.toPartialOrder [u0] sym Nat [] sym Lattice.toSemilatticeInf [u0] sym Nat [] sym DistribLattice.toLattice [u0] sym Nat [] sym instDistribLatticeNat [] sym 2 apn 2 apn 2 apn 2 apn Nat.instLocallyFiniteOrder [] sym 1 bv HAdd.hAdd [u0 u0 u0] sym Nat [] sym Nat [] sym Nat [] sym instHAdd [u0] sym Nat [] sym instAddNat [] sym 2 apn 1 bv 0 bv 6 apn 5 apn 5 apn Finset.range [] sym 0 bv 1 apn 3 apn pi pi
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: Nat [] sym
  dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: Nat [] sym
  dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: Ne [us(u0)] sym Nat [] sym bf5 fv OfNat.ofNat [u0] sym Nat [] sym NAT 0 lit instOfNatNat [] sym NAT 0 lit 1 apn 3 apn 3
... [7912 more characters]
```

### FINALIST R_623a343174ec

*11,011 characters*

```text
meta
  summary ;; theorem: Nat.image_Ico_mod ;; file: Mathlib/Order/Interval/Finset/Nat.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Nat [] sym
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Nat [] sym
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Nat [] sym
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT Nat [] sym EXPLICIT Nat [] sym Eq [us(u0)] sym Finset [u0] sym Nat [] sym ap ap Finset.image [u0 u0] sym Nat [] sym ap Nat [] sym ap instDecidableEqNat [] sym ap EXPLICIT Nat [] sym HMod.hMod [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHMod [u0] sym Nat [] sym ap Nat.instMod [] sym ap ap 0 bv ap 1 bv ap lam ap Finset.Ico [u0] sym Nat [] sym ap PartialOrder.toPreorder [u0] sym Nat [] sym ap SemilatticeInf.toPartialOrder [u0] sym Nat [] sym ap Lattice.toSemilatticeInf [u0] sym Nat [] sym ap DistribLattice.toLattice [u0] sym Nat [] sym ap instDistribLatticeNat [] sym ap ap ap ap ap Nat.instLocallyFiniteOrder [] sym ap 1 bv ap HAdd.hAdd [u0 u0 u0] sym Nat [] sym ap Nat [] sym ap Nat [] sym ap instHAdd [u0] sym Nat [] sym ap instAddNat [] sym ap ap 1 bv ap 0 bv ap ap ap ap Finset.range [] sym 0 bv ap ap pi pi
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Nat [] sym
  decl bf5 ;; binder_role: EXPLICIT ;; declarati
... [9611 more characters]
```

### FINALIST R_8f1e3d8b7028

*12,574 characters*

```text
meta
  summary
    theorem: Nat.image_Ico_mod
    file: Mathlib/Order/Interval/Finset/Nat.lean
state_before
  goal bm4
    target: (mv bm3)
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10]
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (sym Nat [])
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (sym Nat [])
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (sym Nat [])
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (pi EXPLICIT (sym Nat []) (pi EXPLICIT (sym Nat []) (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (ap (sym Finset.image [u0 u0]) (sym Nat [])) (sym Nat [])) (sym instDecidableEqNat [])) (lam EXPLICIT (sym Nat []) (ap (ap (ap (ap (ap (ap (sym HMod.hMod [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHMod [u0]) (sym Nat [])) (sym Nat.instMod []))) (bv 0)) (bv 1)))) (ap (ap (ap (ap (ap (sym Finset.Ico [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat [])))))) (sym Nat.instLocallyFiniteOrder [])) (bv 1)) (a
... [11174 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*26,142 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (ap (sym LE.le [u0]) (sym Nat [])) (ap (ap (sym Preorder.toLE [u0]) (sym Nat [])) (ap (ap (sym PartialOrder.toPreorder [u0]) (sym Nat [])) (ap (ap (sym SemilatticeInf.toPartialOrder [u0]) (sym Nat [])) (ap (ap (sym Lattice.toSemilatticeInf [u0]) (sym Nat [])) (ap (ap (sym DistribLattice.toLattice [u0]) (sym Nat [])) (sym instDistribLatticeNat []))))))) (fv bf4)) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHAdd [u0]) (sym Nat [])) (ap (ap (sym AddSemigroup.toAdd [u0]) (sym Nat [])) (sym Nat.instAddSemigroup [])))) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHAdd [u0]) (sym Nat [])) (ap (ap (sym AddSemigroup.toAdd [u0]) (sym Nat [])) (sym Nat.instAddSemigroup [])))) (fv bf7)) (fv bf5))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHMul [u0]) (sym Nat [])) (sym instMulNat []))) (fv bf5)) (ap (ap (ap (ap (ap (ap (sym HDiv.hDiv [u0 u0 u0]) (sym Nat [])) (sym Nat [])) (sym Nat [])) (ap (ap (sym instHDiv [u0]) (sym Nat [])) (sym Nat.instDiv []))) (fv bf4)) (fv bf5)))))
  alias $a1
    term: (pi EXPLICIT (sym Nat []) (pi EXPLICIT (sym Nat []) (ap (ap (ap (sym Eq [us(u0)]) (ap (sym Finset [u0]) (sym Nat []))) (ap (ap (ap (ap (ap (sym Finset.image [u0 u
... [24742 more characters]
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
    ∈: ap(ap(ap(ap(sym(PicardLindelof.FunSpace,[up(u_1)]),fv(E~bf0)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950~bf1)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2953~bf2)),fv(v~bf3))
  D inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2963~bf5
    n: inst._@.Mathlib.Analysis.ODE.PicardLind
... [28585 more characters]
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
    type: (ap (ap (sym CompleteSpace [up(u_1)]) (fv bf0)) (ap (ap (sym PseudoMetricSpace.toUniformSpace [up(u_1)]) (fv bf0)) (ap (ap (sym SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)]) (fv bf0)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv bf0)) (fv bf1)))))
  decl bf6
    binder_role: EXPLICIT
    declaration_role: cdecl
    typ
... [20883 more characters]
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
  decl v~bf3 has display is v; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(sym(PicardLindelof,[up(u_1)]),fv(E~bf0)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2950~bf1)),fv(inst._@.Mathlib.Analysis.ODE.PicardLindelof._hyg.2953~bf2)) .
  decl f~bf4 has display is f; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(ap(sym(Pi
... [29535 more characters]
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
    ty: {pi|EXPLICIT,{ap|{ap|{ap|{ap|{sym|PicardLindelof.FunSpace,[up{u_1}]},{fv|bf0}},{fv|bf1}},{fv|bf2}},{fv|bf3}},{pi|EXPLICIT,{ap|{ap|{ap|{ap|{sym|PicardLindelof.FunSpace,[up{u_1}]},{fv|bf0}},{fv
... [20400 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*21,632 characters*

```text
(mta
  (smy (thm PicardLindelof.FunSpace.dist_iterate_next_apply_le) (fl Mathlib/Analysis/ODE/PicardLindelof.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_1)]) (fv bf0))))
  (dc bf2 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_1)]) (sym Real [])) (fv bf0)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv bf0)) (fv bf1)))))
  (dc bf3 (br IMPLICIT) (dr cdecl) (ty (ap (ap (ap (sym PicardLindelof [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))))
  (dc bf5 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym CompleteSpace [up(u_1)]) (fv bf0)) (ap (ap (sym PseudoMetricSpace.toUniformSpace [up(u_1)]) (fv bf0)) (ap (ap (sym SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)]) (fv bf0)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv bf0)) (fv bf1)))))))
  (dc bf6 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (pi EXPLICIT (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (
... [20232 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*17,109 characters*

```text
mta
  smy
    thm: PicardLindelof.FunSpace.dist_iterate_next_apply_le
    fl: Mathlib/Analysis/ODE/PicardLindelof.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedAddCommGroup [up(u_1)] sym bf0 fv 1 apn
  dc bf2
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedSpace [u0 up(u_1)] sym Real [] sym bf0 fv Real.normedField [] sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym bf0 fv bf1 fv 2 apn 4 apn
  dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: PicardLindelof [up(u_1)] sym bf0 fv bf1 fv bf2 fv 3 apn
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: PicardLindelof.FunSpace [up(u_1)] sym bf0 fv bf1 fv bf2 fv bf3 fv 4 apn
  dc bf5
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: CompleteSpace [up(u_1)] sym bf0 fv PseudoMetricSpace.toUniformSpace [up(u_1)] sym bf0 fv SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)] sym bf0 fv NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym bf0 fv bf1 fv 2 apn 2 apn 2 apn 2 apn
  dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT PicardLindelof.FunSpace [up(u_1)] sym bf0 fv bf1 fv bf2 fv bf3 fv 4 apn EXPLICIT PicardLindelof.FunSpace [up(u_1)] sym bf0 fv bf1 fv bf2 fv bf3 fv 4 apn EXPLICIT Nat [] sym EXPLICIT Set.Elem [u0] sym Real [] sym Set.Icc [u0] sym Real [] sym Real.instPreorder [] sym PicardLindelof.tMin [up(u_1)] sym bf0 fv bf1
... [15709 more characters]
```

### FINALIST R_623a343174ec

*20,202 characters*

```text
meta
  summary ;; theorem: PicardLindelof.FunSpace.dist_iterate_next_apply_le ;; file: Mathlib/Analysis/ODE/PicardLindelof.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedAddCommGroup [up(u_1)] sym bf0 fv ap
  decl bf2 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedSpace [u0 up(u_1)] sym Real [] sym ap bf0 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym bf0 fv ap bf1 fv ap ap
  decl bf3 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: PicardLindelof [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: PicardLindelof.FunSpace [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap
  decl bf5 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: CompleteSpace [up(u_1)] sym bf0 fv ap PseudoMetricSpace.toUniformSpace [up(u_1)] sym bf0 fv ap SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)] sym bf0 fv ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)] sym bf0 fv ap bf1 fv ap ap ap ap
  decl bf6 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT PicardLindelof.FunSpace [up(u_1)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap EXPLICIT PicardLindelof.FunSpace 
... [18802 more characters]
```

### FINALIST R_8f1e3d8b7028

*22,744 characters*

```text
meta
  summary
    theorem: PicardLindelof.FunSpace.dist_iterate_next_apply_le
    file: Mathlib/Analysis/ODE/PicardLindelof.lean
state_before
  goal bm1
    target: (ap (ap (ap (ap (sym LE.le [u0]) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (sym Dist.dist [up(u_1)]) (fv bf0)) (ap (ap (sym PseudoMetricSpace.toDist [up(u_1)]) (fv bf0)) (ap (ap (sym SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)]) (fv bf0)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv bf0)) (fv bf1))))) (ap (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.toFun [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (sym Nat.iterate [us(up(u_1))]) (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (fv bf9)) (fv bf7)))) (fv bf11))) (ap (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.toFun [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (sym Nat.iterate [us(up(u_1))]) (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (ap (ap (ap (ap (sym PicardLi
... [21344 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*70,567 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (ap (sym LE.le [u0]) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (sym Dist.dist [up(u_1)]) (fv bf0)) (ap (ap (sym PseudoMetricSpace.toDist [up(u_1)]) (fv bf0)) (ap (ap (sym SeminormedAddCommGroup.toPseudoMetricSpace [up(u_1)]) (fv bf0)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_1)]) (fv bf0)) (fv bf1))))) (ap (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.toFun [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (sym Nat.iterate [us(up(u_1))]) (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (fv bf9)) (fv bf7)))) (fv bf11))) (ap (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.toFun [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3)) (ap (ap (ap (ap (sym Nat.iterate [us(up(u_1))]) (ap (ap (ap (ap (sym PicardLindelof.FunSpace [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (ap (ap (ap (ap (sym PicardLindelof.FunSpace.next [up(u_1)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))) (fv bf9)) (fv bf8)))) (fv bf11)))) (ap (ap (ap (ap (ap (ap (sym
... [69167 more characters]
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
    ∈: pi(IMPLICIT,fv(R~bf1),pi(IMPLICIT,fv(R~bf1),pi(IMPLICIT,fv(R~bf1),pi(EXPLICIT,fv(R~bf1),pi(EXPLICIT,sym(Nat,[]),pi(EXPLICIT,ap(ap(ap(sym(Eq,[us(up(u_1))]),fv(R~bf1)),ap(ap(ap(ap(ap(ap(sym(HMul.hMul,[up(u_1) up(u_1) up(u_1)]),fv(R~bf1)),fv(R~bf1)),fv(R~bf1)),ap(ap(sym(instHMul,[up(u_1)]),fv(R~bf1)),ap(ap(sym(NonUnitalNonAssocSemiring.toMul,[up(u_1)]),fv(R~bf1)),ap(ap(sym(NonAssocSemiring.toNonUnitalNonAssocSemiring,[up(u_1)]),fv(R~bf1)),ap(ap(sym(
... [18522 more characters]
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
    type: (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi EXPLICIT (fv bf1) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf1)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap 
... [17798 more characters]
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
  decl mul_pf_left~bf5 has display is mul_pf_left; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(IMPLICIT,fv(R~bf1),pi(IMPLICIT,fv(R~bf1),pi(IMPLICIT,fv(R~bf1),pi(EXPLICIT,fv(R~bf1),pi(EXPLICIT,sym(Nat,[])
... [19981 more characters]
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
    ty: {pi|IMPLICIT,{fv|bf1},{pi|IMPLICIT,{fv|bf1},{pi|IMPLICIT,{fv|bf1},{pi|EXPLICIT,{fv|bf1},{pi|EXPLICIT,{sym|Nat,[]},{pi|EXPLICIT,{ap|{ap|{ap|{sym|Eq,[us{up{u_1}}]},{fv|bf1}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HMul.hMul,[up{u_1} up{u_1} up{u_1}]},{fv|bf1}},{fv|bf1}},{fv|bf1}},{ap|{ap|{sym|instHMul,[up{u_1}]},{fv|bf1}},{ap|{ap|{sym|NonUnitalNonAssocSemiring.toMul,[up{u_1}]},{fv|bf1}},{ap|{ap|{sym|NonAssocSemiring.toNonUnitalNonAssocSemiring,[up{u_1}]},{fv|bf1}},{ap|{ap|{sym|Semiring.toNonAssocSemiring,[up{u_1}]},{fv|bf1}},{ap|{ap|{sym|CommSemiring.toSemiring
... [17065 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*18,204 characters*

```text
(mta
  (smy (thm Mathlib.Tactic.Ring.mul_pf_left) (fl Mathlib/Tactic/Ring/Basic.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sym Lean.Level [])))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (ap (sym Qq.Quoted []) (ap (sym Lean.Expr.sort []) (ap (sym Lean.Level.succ []) (fv bf0))))))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (ap (sym Qq.Quoted []) (ap (ap (sym Lean.Expr.app []) (ap (ap (sym Lean.Expr.const []) (ap (sym Lean.Name.mkStr1 []) (lit STRING CommSemiring))) (ap (ap (ap (sym List.cons [u0]) (sym Lean.Level [])) (fv bf0)) (ap (sym List.nil [u0]) (sym Lean.Level []))))) (fv bf2)))))
  (dc bf4 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CommSemiring [up(u_1)]) (fv bf1))))
  (dc bf5 (br EXPLICIT) (dr cdecl) (ty (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi EXPLICIT (fv bf1) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf1)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym CommSemiring.toSemiring [up(u_1)]) (fv bf1)) (fv bf4))))))) (bv 4)) (bv 3))) (bv 
... [16804 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*15,348 characters*

```text
mta
  smy
    thm: Mathlib.Tactic.Ring.mul_pf_left
    fl: Mathlib/Tactic/Ring/Basic.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: Lean.Level [] sym
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: Qq.Quoted [] sym Lean.Expr.sort [] sym Lean.Level.succ [] sym bf0 fv 1 apn 1 apn 1 apn
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: Qq.Quoted [] sym Lean.Expr.app [] sym Lean.Expr.const [] sym Lean.Name.mkStr1 [] sym STRING CommSemiring lit 1 apn List.cons [u0] sym Lean.Level [] sym bf0 fv List.nil [u0] sym Lean.Level [] sym 1 apn 3 apn 2 apn bf2 fv 2 apn 1 apn
  dc bf4
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: CommSemiring [up(u_1)] sym bf1 fv 1 apn
  dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: IMPLICIT bf1 fv IMPLICIT bf1 fv IMPLICIT bf1 fv EXPLICIT bf1 fv EXPLICIT Nat [] sym EXPLICIT Eq [us(up(u_1))] sym bf1 fv HMul.hMul [up(u_1) up(u_1) up(u_1)] sym bf1 fv bf1 fv bf1 fv instHMul [up(u_1)] sym bf1 fv NonUnitalNonAssocSemiring.toMul [up(u_1)] sym bf1 fv NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)] sym bf1 fv Semiring.toNonAssocSemiring [up(u_1)] sym bf1 fv CommSemiring.toSemiring [up(u_1)] sym bf1 fv bf4 fv 2 apn 2 apn 2 apn 2 apn 2 apn 4 bv 3 bv 6 apn 2 bv 3 apn Eq [us(up(u_1))] sym bf1 fv HMul.hMul [up(u_1) up(u_1) up(u_1)] sym bf1 fv bf1 fv bf1 fv instHMul [up(u_1)] sym bf1 fv NonUnita
... [13948 more characters]
```

### FINALIST R_623a343174ec

*17,745 characters*

```text
meta
  summary ;; theorem: Mathlib.Tactic.Ring.mul_pf_left ;; file: Mathlib/Tactic/Ring/Basic.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Lean.Level [] sym
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Qq.Quoted [] sym Lean.Expr.sort [] sym Lean.Level.succ [] sym bf0 fv ap ap ap
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Qq.Quoted [] sym Lean.Expr.app [] sym Lean.Expr.const [] sym Lean.Name.mkStr1 [] sym STRING CommSemiring lit ap ap List.cons [u0] sym Lean.Level [] sym ap bf0 fv ap List.nil [u0] sym Lean.Level [] sym ap ap ap ap bf2 fv ap ap
  decl bf4 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: CommSemiring [up(u_1)] sym bf1 fv ap
  decl bf5 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: IMPLICIT bf1 fv IMPLICIT bf1 fv IMPLICIT bf1 fv EXPLICIT bf1 fv EXPLICIT Nat [] sym EXPLICIT Eq [us(up(u_1))] sym bf1 fv ap HMul.hMul [up(u_1) up(u_1) up(u_1)] sym bf1 fv ap bf1 fv ap bf1 fv ap instHMul [up(u_1)] sym bf1 fv ap NonUnitalNonAssocSemiring.toMul [up(u_1)] sym bf1 fv ap NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)] sym bf1 fv ap Semiring.toNonAssocSemiring [up(u_1)] sym bf1 fv ap CommSemiring.toSemiring [up(u_1)] sym bf1 fv ap bf4 fv ap ap ap ap 
... [16345 more characters]
```

### FINALIST R_8f1e3d8b7028

*19,958 characters*

```text
meta
  summary
    theorem: Mathlib.Tactic.Ring.mul_pf_left
    file: Mathlib/Tactic/Ring/Basic.lean
state_before
  goal bm0
    target: (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf1)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym CommSemiring.toSemiring [up(u_1)]) (fv bf1)) (fv bf4))))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym CommSemiring.toSemiring [up(u_1)]) (fv bf1)) (fv bf4))))))) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [up(u_1) u0 up(u_1)]) (fv bf1)) (sym Nat [])) (fv bf1)) (ap (ap (ap (sym instHPow [up(u_1) u0]) (fv bf1)) (sym Nat [])) (ap (ap (sym Monoid.toNatPow [up(u_1)]) (fv bf1)) (ap (ap (sym MonoidWithZero.toMonoid [up(u_1)]) (fv bf1)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf1)) (ap (ap (sym CommSemiring.toSemiring [up(u_1)]) (fv b
... [18558 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*58,719 characters*

```text
aliases
  alias $a0
    term: (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi IMPLICIT (fv bf1) (pi EXPLICIT (fv bf1) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf1)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym CommSemiring.toSemiring [up(u_1)]) (fv bf1)) (fv bf4))))))) (bv 4)) (bv 3))) (bv 2)) (ap (ap (ap (sym Eq [us(up(u_1))]) (fv bf1)) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym Semiring.toNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (ap (sym CommSemiring.toSemiring [up(u_1)]) (fv bf1)) (fv bf4))))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [up(u_1) up(u_1) up(u_1)]) (fv bf1)) (fv bf1)) (fv bf1)) (ap (ap (sym instHMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonUnitalNonAssocSemiring.toMul [up(u_1)]) (fv bf1)) (ap (ap (sym NonAssocSemiring.toNonUnitalNonAssocSemiring [up(u_1)]) (fv bf1)) (ap (a
... [57319 more characters]
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
    ∈: pi(EXPLICIT,ap(ap(sym(ArithmeticFunction,[up(u_2)]),fv(M~bf1)),ap(ap(sym(AddMonoid.toZero,[up(u_2)]),fv(M~bf1)),ap(ap(sym(AddCommMonoid.toAddMonoid,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1758~bf3)))),ap(ap(ap(sym(Eq,[us(up(u_2))]),ap(ap(s
... [18121 more characters]
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
    type: (pi EXPLICIT (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3)))) (ap (ap (ap (sym Eq [us(up(u_2))]) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3))))) (ap (ap (ap (ap (ap (ap (sym HSMul.hSMul [up(u_1) up(u_2) up(u_2)]) (ap (ap (sym ArithmeticFunction [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toZero [up(u_1)]) (fv bf0)) (ap (ap (sym
... [15553 more characters]
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
  decl inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1761~bf4 has display is inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1761; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(ap(sym(Module,[up(u_1) up(u_2)]),fv(R~bf0)),fv(M~bf1)),fv(inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1755~bf2)),fv(inst._@.Mathlib.NumberTheory.ArithmeticFunction._hyg.1758~bf3)) .
  decl one_smul'~bf5 has display is one_smul'; and binder
... [20616 more characters]
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
    ty: {pi|EXPLICIT,{ap|{ap|{sym|ArithmeticFunction,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddMonoid.toZero,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddCommMonoid.toAddMonoid,[up{u_2}]},{fv|bf1}},{fv|bf3}}}},{ap|{ap|{ap|{sym|Eq,[us{up{u_2}}]},{ap|{ap|{sym|ArithmeticFunction,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddMonoid.toZero,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddCommMonoid.toAddMonoid,[up{u_2}]},{fv|bf1}},{fv|bf3}}}}},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HSMul.hSMul,[up{u_1} up{u_2} up{u_2}]},{ap|{ap|{sym|ArithmeticFunction,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|MonoidWithZero.toZero,[up{u_1}]},{fv|bf0}},{ap|{ap|{sym|Semiring.toMonoidWithZero,[up{u_1}]},{fv|bf0}},{fv|bf2}}}}},{ap|{ap|{sym|ArithmeticFunction,[up{u_2}]},{fv|bf1}},{ap|{ap|{sym|AddMonoid.toZero,[up{u_2}]},{fv|bf1}},{ap|
... [14390 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*15,229 characters*

```text
(mta
  (smy (thm ArithmeticFunction.one_smul') (fl Mathlib/NumberTheory/ArithmeticFunction.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc bf2 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Semiring [up(u_1)]) (fv bf0))))
  (dc bf3 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym AddCommMonoid [up(u_2)]) (fv bf1))))
  (dc bf4 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym Module [up(u_1) up(u_2)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))))
  (dc bf5 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3)))) (ap (ap (ap (sym Eq [us(up(u_2))]) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3))))) (ap (ap (ap (ap (ap (ap (sym HSMul.hSMul [up(u_1) up(u_2) up(u_2)]) (ap (ap (sym ArithmeticFunction [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toZero [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (fv bf2))))) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (f
... [13829 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*13,533 characters*

```text
mta
  smy
    thm: ArithmeticFunction.one_smul'
    fl: Mathlib/NumberTheory/ArithmeticFunction.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_2)) sort
  dc bf2
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Semiring [up(u_1)] sym bf0 fv 1 apn
  dc bf3
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: AddCommMonoid [up(u_2)] sym bf1 fv 1 apn
  dc bf4
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Module [up(u_1) up(u_2)] sym bf0 fv bf1 fv bf2 fv bf3 fv 4 apn
  dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT ArithmeticFunction [up(u_2)] sym bf1 fv AddMonoid.toZero [up(u_2)] sym bf1 fv AddCommMonoid.toAddMonoid [up(u_2)] sym bf1 fv bf3 fv 2 apn 2 apn 2 apn Eq [us(up(u_2))] sym ArithmeticFunction [up(u_2)] sym bf1 fv AddMonoid.toZero [up(u_2)] sym bf1 fv AddCommMonoid.toAddMonoid [up(u_2)] sym bf1 fv bf3 fv 2 apn 2 apn 2 apn HSMul.hSMul [up(u_1) up(u_2) up(u_2)] sym ArithmeticFunction [up(u_1)] sym bf0 fv MonoidWithZero.toZero [up(u_1)] sym bf0 fv Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv bf2 fv 2 apn 2 apn 2 apn ArithmeticFunction [up(u_2)] sym bf1 fv AddMonoid.toZero [up(u_2)] sym bf1 fv AddCommMonoid.toAddMonoid [up(u_2)] sym bf1 fv bf3 fv 2 apn 2 apn 2 apn ArithmeticFunction [up(u_2)] sym bf1 fv AddMonoid.toZero [up(u_2)] sym bf1 fv AddCommMonoid.toAddMonoid [up(u_2)] sym bf1 fv bf3 f
... [12133 more characters]
```

### FINALIST R_623a343174ec

*16,818 characters*

```text
meta
  summary ;; theorem: ArithmeticFunction.one_smul' ;; file: Mathlib/NumberTheory/ArithmeticFunction.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_2)) sort
  decl bf2 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: Semiring [up(u_1)] sym bf0 fv ap
  decl bf3 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: AddCommMonoid [up(u_2)] sym bf1 fv ap
  decl bf4 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: Module [up(u_1) up(u_2)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap
  decl bf5 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT ArithmeticFunction [up(u_2)] sym bf1 fv ap AddMonoid.toZero [up(u_2)] sym bf1 fv ap AddCommMonoid.toAddMonoid [up(u_2)] sym bf1 fv ap bf3 fv ap ap ap Eq [us(up(u_2))] sym ArithmeticFunction [up(u_2)] sym bf1 fv ap AddMonoid.toZero [up(u_2)] sym bf1 fv ap AddCommMonoid.toAddMonoid [up(u_2)] sym bf1 fv ap bf3 fv ap ap ap ap HSMul.hSMul [up(u_1) up(u_2) up(u_2)] sym ArithmeticFunction [up(u_1)] sym bf0 fv ap MonoidWithZero.toZero [up(u_1)] sym bf0 fv ap Semiring.toMonoidWithZero [up(u_1)] sym bf0 fv ap bf2 fv ap ap ap ap ArithmeticFunction [up(u_2)] sym bf1 fv ap AddMonoid.toZero [up(u_2)] sym bf1 fv ap AddCommMonoid.toAddMonoid [
... [15418 more characters]
```

### FINALIST R_8f1e3d8b7028

*17,369 characters*

```text
meta
  summary
    theorem: ArithmeticFunction.one_smul'
    file: Mathlib/NumberTheory/ArithmeticFunction.lean
state_before
  goal bm11
    target: (sym False [])
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12]
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm11
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm11
    type: (sort us(up(u_2)))
  decl bf2
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm11
    type: (ap (sym Semiring [up(u_1)]) (fv bf0))
  decl bf3
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm11
    type: (ap (sym AddCommMonoid [up(u_2)]) (fv bf1))
  decl bf4
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm11
    type: (ap (ap (ap (ap (sym Module [up(u_1) up(u_2)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))
  decl bf5
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm11
    type: (pi EXPLICIT (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3)))) (ap (ap (ap (sym Eq [us(up(u_2))]) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1
... [15969 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*44,609 characters*

```text
aliases
  alias $a0
    term: (pi EXPLICIT (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3)))) (ap (ap (ap (sym Eq [us(up(u_2))]) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3))))) (ap (ap (ap (ap (ap (ap (sym HSMul.hSMul [up(u_1) up(u_2) up(u_2)]) (ap (ap (sym ArithmeticFunction [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toZero [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (fv bf2))))) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3))))) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddMonoid [up(u_2)]) (fv bf1)) (fv bf3))))) (ap (ap (ap (sym instHSMul [up(u_1) up(u_2)]) (ap (ap (sym ArithmeticFunction [up(u_1)]) (fv bf0)) (ap (ap (sym MonoidWithZero.toZero [up(u_1)]) (fv bf0)) (ap (ap (sym Semiring.toMonoidWithZero [up(u_1)]) (fv bf0)) (fv bf2))))) (ap (ap (sym ArithmeticFunction [up(u_2)]) (fv bf1)) (ap (ap (sym AddMonoid.toZero [up(u_2)]) (fv bf1)) (ap (ap (sym AddCommMonoid.toAddM
... [43209 more characters]
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
    ∈: pi(INSTANCE_IMPLICIT,pi(EXPLICIT,fv(α~bf0),ap(sym(DecidableEq,[us(up(u))]),ap(fv(β~bf1),bv(0)))),pi(IMPLICIT,ap(sym(Finset,[up(u_1)]),fv(α~bf0)),pi(IMPLICIT,pi(EXPLICIT,fv(α~bf0),ap(sym(Finset,[up(u)]),ap(fv(β~bf1),bv(0)))),pi(IMPLICIT,fv(α~bf0),pi(EXPLICIT,ap(sym(Not,[]),ap(ap(ap(ap(ap(sym(Membership.mem,[up(u_1) up(u_1)]),fv(α~bf0)),ap(sym(Finset,[up(u_1)]),fv(α~bf0))),ap(sym(Finset.instMembership,[up(u_1)]),fv(α~bf0))),bv(0)),bv(2))),ap(ap(ap(sym(Eq,[umax(us(up(u)),us(up(u_1)))]),ap(sym(Finset,[umax(up(u),up(u_1))]),pi(EXPLICIT,fv(α~bf0),pi(EXPLICIT,ap(ap(ap(ap(ap(sym(Membership.mem,[up(u_1) up
... [40235 more characters]
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
    type: (pi INSTANCE_IMPLICIT (pi EXPLICIT (fv bf0) (ap (sym DecidableEq [us(up(u))]) (ap (fv bf1) (bv 0)))) (pi IMPLICIT (ap (sym Finset [up(u_1)]) (fv bf0)) (pi IMPLICIT (pi EXPLICIT (fv bf0) (ap (sym Finset [up(u)]) (ap (fv bf1) (bv 0)))) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Finset [up(u_1)]) (fv bf0))) (ap (sym Finset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (bv 2))) (ap (ap (ap (sym Eq [umax(us(up(u)) us(up(u_1)))]) (ap (sym
... [40656 more characters]
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
  decl pi_insert~bf6 has display is pi_insert; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(INSTANCE_IMPLICIT,pi(EXPLICIT,fv(α~bf0),ap(sym(DecidableEq,[us(up(u))]),ap(fv(β~bf1),bv(0)))),pi(IMPLICIT,ap(sym(Finset,[up(u_1)]),fv(α~bf0)),pi(IMPLICIT,pi(EXPLICIT,fv(α~bf0),ap(sym(Finset,[up(u)]),ap(fv(β~bf1),
... [42464 more characters]
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
    ty: {pi|INSTANCE_IMPLICIT,{pi|EXPLICIT,{fv|bf0},{ap|{sym|DecidableEq,[us{up{u}}]},{ap|{fv|bf1},{bv|0}}}},{pi|IMPLICIT,{ap|{sym|Finset,[up{u_1}]},{fv|bf0}},{pi|IMPLICIT,{pi|EXPLICIT,{fv|bf0},{ap|{sym|Finset,[up{u}]},{ap|{fv|bf1},{bv|0}}}},{pi|IMPLICIT,{fv|bf0},{pi|EXPLICIT,{ap|{sym|Not,[]},{ap|{ap|{ap|{ap|{ap|{sym|Membership.mem,[up{u_1} up{u_1}]},{fv|bf0}},{ap|{sym|Finset,[up{u_1}]},{fv|bf0}}},{ap|{sym|Finset.instMembership,[up{u_1}]},{fv|bf0}}},{bv|0}},{bv|2}}},{ap|{ap|{ap|{sym|Eq,[umax{us{up{u}},us{up{u_1}}}]},{ap|{sym|Finset,[umax{up{u},up{u_1}}]},{pi|EXPLICIT,{fv|bf0},{pi|EXPLICIT,{ap|{ap|{ap|{ap|{ap|{sym|Membership.mem,[up{u_1} up{u_1}]},{fv|bf0}},{ap|{sym|Finset,[up{u_1}]},{fv|bf0}}},{ap|{sym|Finset.instM
... [39598 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*40,521 characters*

```text
(mta
  (smy (thm Finset.pi_insert) (fl Mathlib/Data/Finset/Pi.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (fv bf0) (sort us(up(u))))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (fv bf0) (sort up(v)))))
  (dc bf3 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym DecidableEq [us(up(u_1))]) (fv bf0))))
  (dc bf4 (br IMPLICIT) (dr cdecl) (ty (ap (sym Finset [up(u_1)]) (fv bf0))))
  (dc bf5 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (fv bf0) (ap (sym Finset [up(u)]) (ap (fv bf1) (bv 0))))))
  (dc bf6 (br EXPLICIT) (dr cdecl) (ty (pi INSTANCE_IMPLICIT (pi EXPLICIT (fv bf0) (ap (sym DecidableEq [us(up(u))]) (ap (fv bf1) (bv 0)))) (pi IMPLICIT (ap (sym Finset [up(u_1)]) (fv bf0)) (pi IMPLICIT (pi EXPLICIT (fv bf0) (ap (sym Finset [up(u)]) (ap (fv bf1) (bv 0)))) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (sym Not []) (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Finset [up(u_1)]) (fv bf0))) (ap (sym Finset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (bv 2))) (ap (ap (ap (sym Eq [umax(us(up(u)) us(up(u_1)))]) (ap (sym Finset [umax(up(u) up(u_1))]) (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Finset [up(u_1)]) (fv bf0))) (ap (sym Finset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (ap (ap (ap (ap (ap (sym In
... [39121 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*33,438 characters*

```text
mta
  smy
    thm: Finset.pi_insert
    fl: Mathlib/Data/Finset/Pi.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: EXPLICIT bf0 fv us(up(u)) sort pi
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: EXPLICIT bf0 fv up(v) sort pi
  dc bf3
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: DecidableEq [us(up(u_1))] sym bf0 fv 1 apn
  dc bf4
    br: IMPLICIT
    dr: cdecl
    ty: Finset [up(u_1)] sym bf0 fv 1 apn
  dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: EXPLICIT bf0 fv Finset [up(u)] sym bf1 fv 0 bv 1 apn 1 apn pi
  dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: INSTANCE_IMPLICIT EXPLICIT bf0 fv DecidableEq [us(up(u))] sym bf1 fv 0 bv 1 apn 1 apn pi IMPLICIT Finset [up(u_1)] sym bf0 fv 1 apn IMPLICIT EXPLICIT bf0 fv Finset [up(u)] sym bf1 fv 0 bv 1 apn 1 apn pi IMPLICIT bf0 fv EXPLICIT Not [] sym Membership.mem [up(u_1) up(u_1)] sym bf0 fv Finset [up(u_1)] sym bf0 fv 1 apn Finset.instMembership [up(u_1)] sym bf0 fv 1 apn 0 bv 2 bv 5 apn 1 apn Eq [umax(us(up(u)) us(up(u_1)))] sym Finset [umax(up(u) up(u_1))] sym EXPLICIT bf0 fv EXPLICIT Membership.mem [up(u_1) up(u_1)] sym bf0 fv Finset [up(u_1)] sym bf0 fv 1 apn Finset.instMembership [up(u_1)] sym bf0 fv 1 apn 0 bv Insert.insert [up(u_1) up(u_1)] sym bf0 fv Finset [up(u_1)] sym bf0 fv 1 apn Finset.instInsert [up(u_1)] sym bf0 fv bf3 fv 2 apn 2 bv 4 bv 5 apn 
... [32038 more characters]
```

### FINALIST R_623a343174ec

*37,116 characters*

```text
meta
  summary ;; theorem: Finset.pi_insert ;; file: Mathlib/Data/Finset/Pi.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT bf0 fv us(up(u)) sort pi
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT bf0 fv up(v) sort pi
  decl bf3 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: DecidableEq [us(up(u_1))] sym bf0 fv ap
  decl bf4 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Finset [up(u_1)] sym bf0 fv ap
  decl bf5 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT bf0 fv Finset [up(u)] sym bf1 fv 0 bv ap ap pi
  decl bf6 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: INSTANCE_IMPLICIT EXPLICIT bf0 fv DecidableEq [us(up(u))] sym bf1 fv 0 bv ap ap pi IMPLICIT Finset [up(u_1)] sym bf0 fv ap IMPLICIT EXPLICIT bf0 fv Finset [up(u)] sym bf1 fv 0 bv ap ap pi IMPLICIT bf0 fv EXPLICIT Not [] sym Membership.mem [up(u_1) up(u_1)] sym bf0 fv ap Finset [up(u_1)] sym bf0 fv ap ap Finset.instMembership [up(u_1)] sym bf0 fv ap ap 0 bv ap 2 bv ap ap Eq [umax(us(up(u)) us(up(u_1)))] sym Finset [umax(up(u) up(u_1))] sym EXPLICIT bf0 fv EXPLICIT Membership.mem [up(u_1) up(u_1)] sym bf0 fv ap Finset [up(u_1)] sym bf0 fv ap ap Finset.instMembership [up(u_1)] sym 
... [35716 more characters]
```

### FINALIST R_8f1e3d8b7028

*43,020 characters*

```text
meta
  summary
    theorem: Finset.pi_insert
    file: Mathlib/Data/Finset/Pi.lean
state_before
  goal bm15
    target: (ap (ap (ap (sym Eq [um(u0)]) (mv bm14)) (ap (ap (ap (sym Multiset.dedup [um(u1)]) (mv bm4)) (mv bm5)) (ap (ap (ap (ap (ap (sym Multiset.pi [um(u2) um(u3)]) (mv bm6)) (mv bm7)) (mv bm8)) (fv bf12)) (lam EXPLICIT (fv bf0) (ap (ap (sym Finset.val [um(u4)]) (ap (fv bf1) (bv 0))) (ap (fv bf9) (bv 0))))))) (ap (ap (ap (sym Multiset.dedup [um(u5)]) (mv bm9)) (mv bm10)) (ap (ap (ap (ap (sym Multiset.bind [um(u6) um(u7)]) (mv bm12)) (mv bm13)) (ap (ap (sym Finset.val [um(u8)]) (mv bm11)) (ap (fv bf9) (fv bf10)))) (lam EXPLICIT (ap (fv bf1) (fv bf10)) (ap (ap (ap (sym Multiset.dedup [um(u9)]) (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (fv bf12)) (ap (fv bf1) (bv 1))))) (lam EXPLICIT (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (fv bf12)) (ap (fv bf1) (bv 1)))) (lam EXPLICIT (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [
... [41620 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*172,704 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (sym Eq [um(u0)]) (ap (sym Multiset [umax(up(u_1) up(u))]) (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (ap (ap (ap (sym Multiset.cons [up(u_1)]) (fv bf0)) (fv bf10)) (ap (ap (sym Finset.val [up(u_1)]) (fv bf0)) (fv bf8)))) (ap (fv bf1) (bv 1)))))) (ap (ap (ap (sym Multiset.dedup [um(u1)]) (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (ap (ap (ap (sym Multiset.cons [up(u_1)]) (fv bf0)) (fv bf10)) (ap (ap (sym Finset.val [up(u_1)]) (fv bf0)) (fv bf8)))) (ap (fv bf1) (bv 1))))) (lam EXPLICIT (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership [up(u_1)]) (fv bf0))) (bv 0)) (ap (ap (ap (sym Multiset.cons [up(u_1)]) (fv bf0)) (fv bf10)) (ap (ap (sym Finset.val [up(u_1)]) (fv bf0)) (fv bf8)))) (ap (fv bf1) (bv 1)))) (lam EXPLICIT (pi EXPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_1) up(u_1)]) (fv bf0)) (ap (sym Multiset [up(u_1)]) (fv bf0))) (ap (sym Multiset.instMembership
... [171304 more characters]
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
    ∈: pi(EXPLICIT,ap(ap(sym(Exists,[us(u0)]),sym(PNat,[])),lam(EXPLICIT,sym(PNat,[]),ap(fv(p~bf0),bv(0)))),pi(EXPLICIT,ap(ap(sym(Exists,[us(u0)]),sym(PNat,[])),lam(EXPLICIT,sym(PNat,[]),ap(fv(p~bf0),ap(ap(ap(ap(ap(ap(sym(HAdd.hAdd,[u0 u0 u0]),sym(PNat,[])),sym(PNat,[])),sym(PNat,[])),ap(ap(sym(instHAdd,[u0]),sym(PNat,[])),sym(instPNatAdd,[]))),bv(0)),ap(ap(ap(sym(OfNat.ofNat,[u0]),sym(PN
... [17288 more characters]
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
    type: (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (bv 0)))) (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym instHAdd [u0]) (sym PNat [])) (sym instPNa
... [18194 more characters]
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
  decl n~bf5 has display is n; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(PNat,[]) .
  decl m~bf6 has display is m; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is sym(PNat,[]) .
  decl find_comp_succ~bf7 has display is find_comp_succ; and binder_role i
... [19223 more characters]
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
    ty: {pi|EXPLICIT,{ap|{ap|{sym|Exists,[us{u0}]},{sym|PNat,[]}},{lam|EXPLICIT,{sym|PNat,[]},{ap|{fv|bf0},{bv|0}}}},{pi|EXPLICIT,{ap|{ap|{sym|Exists,[us{u0}]},{sym|PNat,[]}},{lam|EXPLICIT,{sym|PNat,[]},{ap|{fv|bf0},{ap|{ap|{ap|{ap|{ap|{ap|{sym|HAdd.hAdd,[u0 u0 u0]},{sym|PNat,[]}},{sym|PNat,[]}},{sym|PNat,[]}},{ap|{ap|{sym|instHAdd,[u0]},{sym|PNat,[]}},{sym|instPNatAdd,[]}}},{bv|0}},{ap|{ap|{ap|{sym|OfNat.ofNat,[u0]},{sym|PNat,[]}},{lit|NAT,1}},{ap|{ap|{sym|instOfNatPNatOfNeZeroNat,[]},{lit|NAT,1}},{ap|{sym|NeZero.succ,[]},{ap|{ap|{ap|{sym|OfNat.ofNat,[u0]},{sym|Nat,[]}},{lit|NAT
... [17231 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*18,274 characters*

```text
(mta
  (smy (thm PNat.find_comp_succ) (fl Mathlib/Data/PNat/Find.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (sym PNat []) (sort u0))))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (pi EXPLICIT (sym PNat []) (sort u0))))
  (dc bf2 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym DecidablePred [us(u0)]) (sym PNat [])) (fv bf0))))
  (dc bf3 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (sym DecidablePred [us(u0)]) (sym PNat [])) (fv bf1))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (bv 0))))))
  (dc bf5 (br IMPLICIT) (dr cdecl) (ty (sym PNat [])))
  (dc bf6 (br IMPLICIT) (dr cdecl) (ty (sym PNat [])))
  (dc bf7 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (bv 0)))) (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym instHAdd [u0]) (sym PNat [])) (sym instPNatAdd []))) (bv 0)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym PNat [])) (lit NAT 1)) (ap (ap (sym instOfNatPNatOfNeZeroNat []) (lit NAT 1)) (ap (sym NeZero.succ []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 0)) (ap (sym instOfNatNat []) (lit NAT 0)))))))))) (pi EXPLICIT (ap (sym No
... [16874 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*15,540 characters*

```text
mta
  smy
    thm: PNat.find_comp_succ
    fl: Mathlib/Data/PNat/Find.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: EXPLICIT PNat [] sym u0 sort pi
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: EXPLICIT PNat [] sym u0 sort pi
  dc bf2
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: DecidablePred [us(u0)] sym PNat [] sym bf0 fv 2 apn
  dc bf3
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: DecidablePred [us(u0)] sym PNat [] sym bf1 fv 2 apn
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: Exists [us(u0)] sym PNat [] sym EXPLICIT PNat [] sym bf0 fv 0 bv 1 apn lam 2 apn
  dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: PNat [] sym
  dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: PNat [] sym
  dc bf7
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT Exists [us(u0)] sym PNat [] sym EXPLICIT PNat [] sym bf0 fv 0 bv 1 apn lam 2 apn EXPLICIT Exists [us(u0)] sym PNat [] sym EXPLICIT PNat [] sym bf0 fv HAdd.hAdd [u0 u0 u0] sym PNat [] sym PNat [] sym PNat [] sym instHAdd [u0] sym PNat [] sym instPNatAdd [] sym 2 apn 0 bv OfNat.ofNat [u0] sym PNat [] sym NAT 1 lit instOfNatPNatOfNeZeroNat [] sym NAT 1 lit NeZero.succ [] sym OfNat.ofNat [u0] sym Nat [] sym NAT 0 lit instOfNatNat [] sym NAT 0 lit 1 apn 3 apn 1 apn 2 apn 3 apn 6 apn 1 apn lam 2 apn EXPLICIT Not [] sym bf0 fv OfNat.ofNat [u0] sym PNat [] sym NAT 1 lit instOfNatPNatOfNeZeroNat [] sym NAT 1 lit NeZero.succ [] sym OfNat.of
... [14140 more characters]
```

### FINALIST R_623a343174ec

*18,307 characters*

```text
meta
  summary ;; theorem: PNat.find_comp_succ ;; file: Mathlib/Data/PNat/Find.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT PNat [] sym u0 sort pi
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT PNat [] sym u0 sort pi
  decl bf2 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: DecidablePred [us(u0)] sym PNat [] sym ap bf0 fv ap
  decl bf3 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: DecidablePred [us(u0)] sym PNat [] sym ap bf1 fv ap
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym bf0 fv 0 bv ap lam ap
  decl bf5 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: PNat [] sym
  decl bf6 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: PNat [] sym
  decl bf7 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym bf0 fv 0 bv ap lam ap EXPLICIT Exists [us(u0)] sym PNat [] sym ap EXPLICIT PNat [] sym bf0 fv HAdd.hAdd [u0 u0 u0] sym PNat [] sym ap PNat [] sym ap PNat [] sym ap instHAdd [u0] sym PNat [] sym ap instPNatAdd [] sym ap ap 0 bv ap OfNat.ofNat [u0] sym PNat [] sym ap NAT 1 lit ap instOfNatPNatOfNeZeroNat [] sym NAT 1 lit ap NeZero.succ [] sym OfNat.ofNat [u0] sym Nat [] sym
... [16907 more characters]
```

### FINALIST R_8f1e3d8b7028

*20,178 characters*

```text
meta
  summary
    theorem: PNat.find_comp_succ
    file: Mathlib/Data/PNat/Find.lean
state_before
  goal bm1
    target: (ap (sym Not []) (ap (fv bf0) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym instHAdd [u0]) (sym PNat [])) (sym instPNatAdd []))) (fv bf12)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym PNat [])) (lit NAT 1)) (ap (ap (sym instOfNatPNatOfNeZeroNat []) (lit NAT 1)) (ap (sym NeZero.succ []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 0)) (ap (sym instOfNatNat []) (lit NAT 0)))))))))
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14]
  alias bf0
    tag: dependent_function
  alias bf12
    tag: PNat
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm1
    type: (pi EXPLICIT (sym PNat []) (sort u0))
  decl bf12
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm1
    type: (sym PNat [])
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm1
    type: (pi EXPLICIT (sym PNat []) (sort u0))
  decl bf2
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm1
    type: (ap (ap (sym DecidablePred [us(u0)]) (sym PNat [])) (fv bf0))
  decl bf3
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm1
    type: (ap (ap (sym DecidablePred [us(u0)]) (sym PNat [])) (fv 
... [18778 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*36,157 characters*

```text
aliases
  alias $a0
    term: (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (bv 0)))) (pi EXPLICIT (ap (ap (sym Exists [us(u0)]) (sym PNat [])) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym instHAdd [u0]) (sym PNat [])) (sym instPNatAdd []))) (bv 0)) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym PNat [])) (lit NAT 1)) (ap (ap (sym instOfNatPNatOfNeZeroNat []) (lit NAT 1)) (ap (sym NeZero.succ []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 0)) (ap (sym instOfNatNat []) (lit NAT 0)))))))))) (pi EXPLICIT (ap (sym Not []) (ap (fv bf0) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym PNat [])) (lit NAT 1)) (ap (ap (sym instOfNatPNatOfNeZeroNat []) (lit NAT 1)) (ap (sym NeZero.succ []) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 0)) (ap (sym instOfNatNat []) (lit NAT 0)))))))) (ap (ap (ap (sym Eq [us(u0)]) (sym PNat [])) (ap (ap (ap (sym PNat.find []) (fv bf0)) (fv bf2)) (bv 2))) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym instHAdd [u0]) (sym PNat [])) (sym instPNatAdd []))) (ap (ap (ap (sym PNat.find []) (lam EXPLICIT (sym PNat []) (ap (fv bf0) (ap (ap (ap (ap (ap (ap (sym HAdd.hAdd [u0 u0 u0]) (sym PNat [])) (sym PNat [])) (sym PNat [])) (ap (ap (sym
... [34757 more characters]
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
    ∈: pi(EXPLICIT,pi(EXPLICIT,fv(ι~bf0),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4))),pi(IMPLICIT,pi(EXPLICIT,fv(M~bf1),sort(u0)),pi(IMPLICIT,fv(M~bf1),pi(EXPLICIT,ap(ap(ap(ap(ap(sym(Membership.mem,[up(u_2) up(u_2)]),fv(M~bf1)),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4))),ap(ap(ap(sym(SetLike.instMembership,[up(u_2) up(u_2)]),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4))),fv(M~bf1)),ap(ap(sym(Subsemigroup.instSetLike,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Group.Subsemigroup.Membershi
... [6474 more characters]
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
    type: (pi EXPLICIT (pi EXPLICIT (fv bf0) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (pi IMPLICIT (pi EXPLICIT (fv bf1) (sort u0)) (pi IMPLICIT (fv bf1) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_2) up(u_2)]) (fv bf1)) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (ap (ap (ap (sym SetLike.instMembership [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4)))) (bv 0)) (ap (ap (ap (ap (sym iSup [up(u_2) up(u_1)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf0)) (ap (ap (sym CompleteLattice.toSupSet [up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)])
... [5338 more characters]
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
  decl iSup_induction~bf5 has display is iSup_induction; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is pi(EXPLICIT,pi(EXPLICIT,fv(ι~bf0),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Group.Subsemigroup.Membership._hyg.815~bf4))),pi(IMPLICIT,pi(EXPLICIT,fv(M~bf1),sort(u0)),pi(IMPLICIT,fv(M~bf1),pi(EXPLICIT,ap(ap(ap(ap(ap(sym(Membership.mem,[up(u_2) up(u_2)]),fv(M~bf1)),ap(ap(sym(Subsemigroup,[up(u_2)]),fv(M~bf1)),fv(inst._@.Mathlib.Algebra.Gro
... [7662 more characters]
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
    ty: {pi|EXPLICIT,{pi|EXPLICIT,{fv|bf0},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{pi|IMPLICIT,{pi|EXPLICIT,{fv|bf1},{sort|u0}},{pi|IMPLICIT,{fv|bf1},{pi|EXPLICIT,{ap|{ap|{ap|{ap|{ap|{sym|Membership.mem,[up{u_2} up{u_2}]},{fv|bf1}},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{ap|{ap|{ap|{sym|SetLike.instMembership,[up{u_2} up{u_2}]},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{fv|bf1}},{ap|{ap|{sym|Subsemigroup.instSetLike,[up{u_2}]},{fv|bf1}},{fv|bf4}}}},{bv|0}},{ap|{ap|{ap|{ap|{sym|iSup,[up{u_2} up{u_1}]},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{fv|bf0}},{ap|{ap|{sym|CompleteLattice.toSupSet,[up{u_2}]},{ap|{ap|{sym|Subsemigroup,[up{u_2}]},{fv|bf1}},{fv|bf4}}},{ap|{ap|{sym|Subsemigroup.instCompleteLattice,[up{u_2}]},{fv|bf1}},{fv|bf4}}}},{lam|EXPLICIT,{fv|bf0},{ap|{bv|3},{bv|0}}}}},{pi|EXPLICIT,{pi|EXPLIC
... [4740 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*5,924 characters*

```text
(mta
  (smy (thm Subsemigroup.iSup_induction) (fl Mathlib/Algebra/Group/Subsemigroup/Membership.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort up(u_1))))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_3)))))
  (dc bf3 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_4)))))
  (dc bf4 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Mul [up(u_2)]) (fv bf1))))
  (dc bf5 (br EXPLICIT) (dr cdecl) (ty (pi EXPLICIT (pi EXPLICIT (fv bf0) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (pi IMPLICIT (pi EXPLICIT (fv bf1) (sort u0)) (pi IMPLICIT (fv bf1) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [up(u_2) up(u_2)]) (fv bf1)) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (ap (ap (ap (sym SetLike.instMembership [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4)))) (bv 0)) (ap (ap (ap (ap (sym iSup [up(u_2) up(u_1)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf0)) (ap (ap (sym CompleteLattice.toSupSet [up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (ap (ap (sym Subsemigroup.instCompleteLattice [up(u_2)]) (fv bf1)) (fv bf4)))) (lam EXPLICIT (fv bf0) (ap (bv 3) (bv 0))))) (pi EXPLICIT (pi EXPLICIT (fv bf0) (pi EXPLICIT (fv bf1) (pi EXPLICIT (ap (ap (ap
... [4524 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*5,269 characters*

```text
mta
  smy
    thm: Subsemigroup.iSup_induction
    fl: Mathlib/Algebra/Group/Subsemigroup/Membership.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: up(u_1) sort
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_2)) sort
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_3)) sort
  dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_4)) sort
  dc bf4
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Mul [up(u_2)] sym bf1 fv 1 apn
  dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT EXPLICIT bf0 fv Subsemigroup [up(u_2)] sym bf1 fv bf4 fv 2 apn pi IMPLICIT EXPLICIT bf1 fv u0 sort pi IMPLICIT bf1 fv EXPLICIT Membership.mem [up(u_2) up(u_2)] sym bf1 fv Subsemigroup [up(u_2)] sym bf1 fv bf4 fv 2 apn SetLike.instMembership [up(u_2) up(u_2)] sym Subsemigroup [up(u_2)] sym bf1 fv bf4 fv 2 apn bf1 fv Subsemigroup.instSetLike [up(u_2)] sym bf1 fv bf4 fv 2 apn 3 apn 0 bv iSup [up(u_2) up(u_1)] sym Subsemigroup [up(u_2)] sym bf1 fv bf4 fv 2 apn bf0 fv CompleteLattice.toSupSet [up(u_2)] sym Subsemigroup [up(u_2)] sym bf1 fv bf4 fv 2 apn Subsemigroup.instCompleteLattice [up(u_2)] sym bf1 fv bf4 fv 2 apn 2 apn EXPLICIT bf0 fv 3 bv 0 bv 1 apn lam 4 apn 5 apn EXPLICIT EXPLICIT bf0 fv EXPLICIT bf1 fv EXPLICIT Membership.mem [up(u_2) up(u_2)] sym bf1 fv Subsemigroup [up(u_2)] sym bf1 fv bf4 fv 2 apn SetLike.instMembership [up(u_2) up(u_2)] sym Subsemigroup [up(u_2)] sym bf
... [3869 more characters]
```

### FINALIST R_623a343174ec

*7,450 characters*

```text
meta
  summary ;; theorem: Subsemigroup.iSup_induction ;; file: Mathlib/Algebra/Group/Subsemigroup/Membership.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: up(u_1) sort
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_2)) sort
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_3)) sort
  decl bf3 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_4)) sort
  decl bf4 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: Mul [up(u_2)] sym bf1 fv ap
  decl bf5 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: EXPLICIT EXPLICIT bf0 fv Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap pi IMPLICIT EXPLICIT bf1 fv u0 sort pi IMPLICIT bf1 fv EXPLICIT Membership.mem [up(u_2) up(u_2)] sym bf1 fv ap Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap ap SetLike.instMembership [up(u_2) up(u_2)] sym Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap ap bf1 fv ap Subsemigroup.instSetLike [up(u_2)] sym bf1 fv ap bf4 fv ap ap ap 0 bv ap iSup [up(u_2) up(u_1)] sym Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap ap bf0 fv ap CompleteLattice.toSupSet [up(u_2)] sym Subsemigroup [up(u_2)] sym bf1 fv ap bf4 fv ap ap Subsemigroup.instCompleteLattice [up(u_2)] sym bf1 fv ap bf4 fv ap ap ap EXPLICIT bf0 fv 3 bv 0 bv ap lam ap ap EXPLICIT EXPLICIT bf0 fv EXPLICIT bf1 fv
... [6050 more characters]
```

### FINALIST R_8f1e3d8b7028

*7,063 characters*

```text
meta
  summary
    theorem: Subsemigroup.iSup_induction
    file: Mathlib/Algebra/Group/Subsemigroup/Membership.lean
state_before
  goal bm2
    target: (ap (fv bf7) (fv bf12))
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15]
  alias bf12
    tag: metavariable_reference
  alias bf7
    tag: dependent_function
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort us(up(u_2)))
  decl bf7
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (pi EXPLICIT (fv bf1) (sort u0))
  decl bf12
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (mv bm0)
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort up(u_1))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort us(up(u_3)))
  decl bf3
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort us(up(u_4)))
  decl bf4
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (sym Mul [up(u_2)]) (fv bf1))
  decl bf5
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (pi EXPLICIT (pi EXPLICIT (fv bf0) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (pi IMPLICIT (pi EXPLICIT (fv bf1) (sort u0)) (pi IMPLICIT (fv bf1) (pi EXPLICIT (
... [5663 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*9,748 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (sym Set.iUnion [up(u_2) up(u_1)]) (fv bf1)) (fv bf0)) (lam EXPLICIT (fv bf0) (ap (ap (ap (ap (sym SetLike.coe [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4))) (ap (fv bf6) (bv 0)))))
  alias $a1
    term: (ap (ap (ap (ap (sym Membership.mem [up(u_2) up(u_2)]) (fv bf1)) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (ap (ap (ap (sym SetLike.instMembership [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4)))) (bv 0))
  alias $a2
    term: (ap (ap (ap (sym Membership.mem [up(u_2) up(u_2)]) (fv bf1)) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (ap (ap (ap (sym SetLike.instMembership [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4))))
  alias $a3
    term: (lam EXPLICIT (fv bf0) (ap (ap (ap (ap (sym SetLike.coe [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1)) (fv bf4))) (fv bf1)) (ap (ap (sym Subsemigroup.instSetLike [up(u_2)]) (fv bf1)) (fv bf4))) (ap (fv bf6) (bv 0))))
  alias $a4
    term: (ap (ap (ap (ap (sym SetLike.coe [up(u_2) up(u_2)]) (ap (ap (sym Subsemigroup [up(u_2)]) (fv bf1
... [8348 more characters]
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
    ∈: ap(ap(ap(ap(sym(NormedSpace,[u0 up(u_4)]),sym(Real,[])),fv(E~bf3)),sym(Real.normedField,[])),ap(ap(sym(NormedAddCommGroup.toSeminormedAddCommGroup,[up(u_4)]),fv(E~bf3)),fv(inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1295~bf7)))
  D inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1304~bf9
    n: inst._@.Mathlib.Analysis.Distribution
... [19513 more characters]
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
    type: (ap (ap (ap (ap (sym NormedSpace [u0 up(u_4)]) (sym Real [])) (fv bf3)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7)))
  decl bf9
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym NormedAddCommGroup [up(u_5)]) (fv bf4))
  decl bf10
    binder_role: INSTANCE_IMPLICIT
    declaration
... [14691 more characters]
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
  decl inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1295~bf7 has display is inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1295; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(NormedAddCommGroup,[up(u_4)]),fv(E~bf3)) .
  decl inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.1298~bf8 has display is inst._@.Ma
... [22014 more characters]
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
    ty: {ap|{ap|{ap|{ap|{sym|NormedSpace,[u0 up{u_5}]},{sym|Real,[]}},{fv|bf4}},{sym|Real.normedField,[]}},{ap|{ap|{sym|NormedAddCommGroup.toSeminormedAddCommGroup,[up{u_5}]},{fv|bf4}},{fv|bf9}}}
  - dc bf11
    br: EXPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{ap|{ap|{sym|Sch
... [13473 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*14,378 characters*

```text
(mta
  (smy (thm SchwartzMap.isBigO_cocompact_zpow_neg_nat) (fl Mathlib/Analysis/Distribution/SchwartzSpace.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_3)))))
  (dc bf3 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_4)))))
  (dc bf4 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_5)))))
  (dc bf5 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_6)))))
  (dc bf6 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_7)))))
  (dc bf7 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_4)]) (fv bf3))))
  (dc bf8 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_4)]) (sym Real [])) (fv bf3)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7)))))
  (dc bf9 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_5)]) (fv bf4))))
  (dc bf10 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_5)]) (sym Real [])) (fv bf4)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_5)]) (fv bf4)) (fv bf9)))))
  (dc bf11 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (ap (ap (sym SchwartzMap [up(u_4) up(u_5)]) (fv bf3)) (fv bf4)) (fv bf7)) (fv bf8)) (fv bf9)) (fv bf10))))
  (dc bf12 (br EXPLIC
... [12978 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*12,333 characters*

```text
mta
  smy
    thm: SchwartzMap.isBigO_cocompact_zpow_neg_nat
    fl: Mathlib/Analysis/Distribution/SchwartzSpace.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_2)) sort
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_3)) sort
  dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_4)) sort
  dc bf4
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_5)) sort
  dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_6)) sort
  dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_7)) sort
  dc bf7
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedAddCommGroup [up(u_4)] sym bf3 fv 1 apn
  dc bf8
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedSpace [u0 up(u_4)] sym Real [] sym bf3 fv Real.normedField [] sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)] sym bf3 fv bf7 fv 2 apn 4 apn
  dc bf9
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedAddCommGroup [up(u_5)] sym bf4 fv 1 apn
  dc bf10
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedSpace [u0 up(u_5)] sym Real [] sym bf4 fv Real.normedField [] sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_5)] sym bf4 fv bf9 fv 2 apn 4 apn
  dc bf11
    br: EXPLICIT
    dr: cdecl
    ty: SchwartzMap [up(u_4) up(u_5)] sym bf3 fv bf4 fv bf7 fv bf8 fv bf9 fv bf10 fv 6 apn
  dc bf12
    br: EXPLICIT
    dr: cdecl
    ty: EXPLICIT N
... [10933 more characters]
```

### FINALIST R_623a343174ec

*17,128 characters*

```text
meta
  summary ;; theorem: SchwartzMap.isBigO_cocompact_zpow_neg_nat ;; file: Mathlib/Analysis/Distribution/SchwartzSpace.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_2)) sort
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_3)) sort
  decl bf3 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_4)) sort
  decl bf4 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_5)) sort
  decl bf5 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_6)) sort
  decl bf6 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_7)) sort
  decl bf7 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedAddCommGroup [up(u_4)] sym bf3 fv ap
  decl bf8 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedSpace [u0 up(u_4)] sym Real [] sym ap bf3 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)] sym bf3 fv ap bf7 fv ap ap
  decl bf9 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedAddCommGroup [up(u_5)] sym bf4 fv ap
  decl bf10 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedSpace [u0 up(u_5)] sym Real [] sym ap bf4 fv ap Real.norme
... [15728 more characters]
```

### FINALIST R_8f1e3d8b7028

*16,676 characters*

```text
meta
  summary
    theorem: SchwartzMap.isBigO_cocompact_zpow_neg_nat
    file: Mathlib/Analysis/Distribution/SchwartzSpace.lean
state_before
  goal bm3
    target: (ap (ap (ap (sym Filter.Eventually [um(u0)]) (mv bm0)) (lam EXPLICIT (mv bm0) (ap (mv bm2) (bv 0)))) (mv bm1))
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15,bf16]
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (sort us(up(u_2)))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (sort us(up(u_3)))
  decl bf3
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (sort us(up(u_4)))
  decl bf4
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (sort us(up(u_5)))
  decl bf5
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (sort us(up(u_6)))
  decl bf6
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (sort us(up(u_7)))
  decl bf7
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (ap (sym NormedAddCommGroup [up(u_4)]) (fv bf3))
  decl bf8
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm3
    type: (ap (ap (ap (ap (sym Nor
... [15276 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*38,834 characters*

```text
aliases
  alias $a0
    term: (pi EXPLICIT (sym Nat []) (ap (ap (ap (ap (ap (ap (ap (ap (sym Asymptotics.IsBigO [up(u_4) up(u_5) u0]) (fv bf3)) (fv bf4)) (sym Real [])) (ap (ap (sym NormedAddCommGroup.toNorm [up(u_5)]) (fv bf4)) (fv bf9))) (sym Real.norm [])) (ap (ap (sym Filter.cocompact [up(u_4)]) (fv bf3)) (ap (ap (sym UniformSpace.toTopologicalSpace [up(u_4)]) (fv bf3)) (ap (ap (sym PseudoMetricSpace.toUniformSpace [up(u_4)]) (fv bf3)) (ap (ap (sym SeminormedAddCommGroup.toPseudoMetricSpace [up(u_4)]) (fv bf3)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7))))))) (ap (ap (ap (ap (ap (sym DFunLike.coe [umax(us(up(u_4)) us(up(u_5))) us(up(u_4)) us(up(u_5))]) (ap (ap (ap (ap (ap (ap (sym SchwartzMap [up(u_4) up(u_5)]) (fv bf3)) (fv bf4)) (fv bf7)) (fv bf8)) (fv bf9)) (fv bf10))) (fv bf3)) (lam EXPLICIT (fv bf3) (fv bf4))) (ap (ap (ap (ap (ap (ap (sym SchwartzMap.instFunLike [up(u_4) up(u_5)]) (fv bf3)) (fv bf4)) (fv bf7)) (fv bf8)) (fv bf9)) (fv bf10))) (fv bf11))) (lam EXPLICIT (fv bf3) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [u0 u0 u0]) (sym Real [])) (sym Int [])) (sym Real [])) (ap (ap (ap (sym instHPow [u0 u0]) (sym Real [])) (sym Int [])) (ap (ap (sym DivInvMonoid.Pow [u0]) (sym Real [])) (sym Real.instDivInvMonoid [])))) (ap (ap (ap (sym Norm.norm [up(u_4)]) (fv bf3)) (ap (ap (sym NormedAddCommGroup.toNorm [up(u_4)]) (fv bf3)) (fv 
... [37434 more characters]
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
    b: EXPLICIT
    d: cdecl
    ∈: ap(ap(ap(ap(sym(Quiver.Hom,[us(up(v₁)) up(u₁)]),fv(C~bf0)),ap(ap(sym(CategoryTheory.CategoryStruct.toQuiver,[up(v₁) up(u₁)]),fv(C~bf0)),ap(ap(sym(CategoryTheory.Category.toCat
... [16683 more characters]
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
    type: (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)))) (fv bf6)) (fv bf5))
  decl bf9
    binder_ro
... [14951 more characters]
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
  decl F~bf4 has display is F; and binder_role is EXPLICIT; and declaration_role is cdecl; and type is ap(ap(ap(ap(sym(CategoryTheory.Functor,[up(v₁) up(v₂) up(u₁) up(u₂)]),fv(C~bf0)),fv(inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4515~bf1)),fv(D~bf2)),fv(inst._@.Mathlib.CategoryTheory.Sites.Sieves._hyg.4519~bf3)) .
  decl X~bf5 has display is X; and binder_role is IMPLICIT; and declaration_role is cdecl; and type is fv(C~bf0) .
  decl Y~bf6 has di
... [19018 more characters]
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
    ty: {ap|{ap|{ap|{sym|CategoryTheory.Sieve,[up{v₁} up{u₁}]},{fv|bf0}},{fv|bf1}},{fv|bf5}}
  - dc bf10
    br: IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{sym|CategoryTheory.Sieve,[up{v₁} up{u₁}]},{fv|bf0}},{fv|bf1}},{fv|bf5
... [13788 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*14,759 characters*

```text
(mta
  (smy (thm CategoryTheory.Sieve.mem_ofArrows_iff) (fl Mathlib/CategoryTheory/Sites/Sieves.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u₁)))))
  (dc bf1 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CategoryTheory.Category [up(v₁) up(u₁)]) (fv bf0))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u₂)))))
  (dc bf3 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CategoryTheory.Category [up(v₂) up(u₂)]) (fv bf2))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))))
  (dc bf5 (br IMPLICIT) (dr cdecl) (ty (fv bf0)))
  (dc bf6 (br IMPLICIT) (dr cdecl) (ty (fv bf0)))
  (dc bf7 (br IMPLICIT) (dr cdecl) (ty (fv bf0)))
  (dc bf8 (br EXPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)))) (fv bf6)) (fv bf5))))
  (dc bf9 (br IMPLICIT) (dr cdecl) (ty (ap (ap (ap (sym CategoryTheory.Sieve [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)) (fv bf5))))
  (dc bf10 (br IMPLICIT) (dr cdecl) (ty (ap (ap (ap (sym CategoryTheory.Sieve [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)) (fv bf5))))
  (dc bf11 (br EXPLICIT) (dr cdecl) (ty (pi IMPLICIT (sort us(up(u_1))) (pi IMPLICIT (fv bf0) (pi 
... [13359 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*13,039 characters*

```text
mta
  smy
    thm: CategoryTheory.Sieve.mem_ofArrows_iff
    fl: Mathlib/CategoryTheory/Sites/Sieves.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u₁)) sort
  dc bf1
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: CategoryTheory.Category [up(v₁) up(u₁)] sym bf0 fv 1 apn
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u₂)) sort
  dc bf3
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: CategoryTheory.Category [up(v₂) up(u₂)] sym bf2 fv 1 apn
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)] sym bf0 fv bf1 fv bf2 fv bf3 fv 4 apn
  dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: bf0 fv
  dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: bf0 fv
  dc bf7
    br: IMPLICIT
    dr: cdecl
    ty: bf0 fv
  dc bf8
    br: EXPLICIT
    dr: cdecl
    ty: Quiver.Hom [us(up(v₁)) up(u₁)] sym bf0 fv CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)] sym bf0 fv CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)] sym bf0 fv bf1 fv 2 apn 2 apn bf6 fv bf5 fv 4 apn
  dc bf9
    br: IMPLICIT
    dr: cdecl
    ty: CategoryTheory.Sieve [up(v₁) up(u₁)] sym bf0 fv bf1 fv bf5 fv 3 apn
  dc bf10
    br: IMPLICIT
    dr: cdecl
    ty: CategoryTheory.Sieve [up(v₁) up(u₁)] sym bf0 fv bf1 fv bf5 fv 3 apn
  dc bf11
    br: EXPLICIT
    dr: cdecl
    ty: IMPLICIT us(up(u_1)) sort IMPLICIT bf0 fv EXPLICIT EXPLICIT 1 bv bf0 fv pi EXPLICIT EX
... [11639 more characters]
```

### FINALIST R_623a343174ec

*18,158 characters*

```text
meta
  summary ;; theorem: CategoryTheory.Sieve.mem_ofArrows_iff ;; file: Mathlib/CategoryTheory/Sites/Sieves.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u₁)) sort
  decl bf1 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: CategoryTheory.Category [up(v₁) up(u₁)] sym bf0 fv ap
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u₂)) sort
  decl bf3 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: CategoryTheory.Category [up(v₂) up(u₂)] sym bf2 fv ap
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)] sym bf0 fv ap bf1 fv ap bf2 fv ap bf3 fv ap
  decl bf5 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: bf0 fv
  decl bf6 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: bf0 fv
  decl bf7 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: bf0 fv
  decl bf8 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Quiver.Hom [us(up(v₁)) up(u₁)] sym bf0 fv ap CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)] sym bf0 fv ap CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)] sym bf0 fv ap bf1 fv ap ap ap bf6 fv ap bf5 fv ap
  decl bf9 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: CategoryTheory.Sieve [up(v₁) up(u₁)] sym bf0 fv ap bf1 
... [16758 more characters]
```

### FINALIST R_8f1e3d8b7028

*17,248 characters*

```text
meta
  summary
    theorem: CategoryTheory.Sieve.mem_ofArrows_iff
    file: Mathlib/CategoryTheory/Sites/Sieves.lean
state_before
  goal bm2
    target: (pi EXPLICIT (mv bm0) (mv bm1))
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15,bf16,bf17]
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort us(up(u₁)))
  decl bf1
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (sym CategoryTheory.Category [up(v₁) up(u₁)]) (fv bf0))
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort us(up(u₂)))
  decl bf3
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (sym CategoryTheory.Category [up(v₂) up(u₂)]) (fv bf2))
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (ap (ap (ap (sym CategoryTheory.Functor [up(v₁) up(v₂) up(u₁) up(u₂)]) (fv bf0)) (fv bf1)) (fv bf2)) (fv bf3))
  decl bf5
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (fv bf0)
  decl bf6
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (fv bf0)
  decl bf7
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (fv bf0)
  decl bf8
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    
... [15848 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*48,682 characters*

```text
aliases
  alias $a0
    term: (pi IMPLICIT (sort us(up(u_1))) (pi IMPLICIT (fv bf0) (pi EXPLICIT (pi EXPLICIT (bv 1) (fv bf0)) (pi EXPLICIT (pi EXPLICIT (bv 2) (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)))) (ap (bv 1) (bv 0))) (bv 2))) (pi IMPLICIT (fv bf0) (pi EXPLICIT (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)))) (bv 0)) (bv 3)) (ap (ap (sym Iff []) (ap (ap (ap (ap (ap (ap (sym CategoryTheory.Sieve.arrows [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)) (bv 4)) (ap (ap (ap (ap (ap (ap (sym CategoryTheory.Sieve.ofArrows [up(v₁) up(u₁) up(u_1)]) (fv bf0)) (fv bf1)) (bv 5)) (bv 4)) (bv 3)) (bv 2))) (bv 1)) (bv 0))) (ap (ap (sym Exists [us(up(u_1))]) (bv 5)) (lam EXPLICIT (bv 5) (ap (ap (sym Exists [us(up(v₁))]) (ap (ap (ap (ap (sym Quiver.Hom [us(up(v₁)) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.CategoryStruct.toQuiver [up(v₁) up(u₁)]) (fv bf0)) (ap (ap (sym CategoryTheory.Category.toCategoryStruct [up(v₁) up(u₁)]) (fv bf0)) (fv bf1)))) (bv 2)) (ap (bv 4) (bv 0)))) (lam EXPLICIT (ap (ap (ap (ap (sym Quiver.Hom [us(u
... [47282 more characters]
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
    d: cdecl
    ∈: ap(ap(ap(ap(sym(Algebra,[up(u) up(v)]),fv(A~bf3)),fv(B~bf4)),ap(ap(sym(CommRing.toCommSemiring,[up(u)]),fv(A~bf3)),fv(inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2374~bf7))),a
... [13381 more characters]
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
    type: (ap (ap (ap (ap (sym Algebra [up(u) up(v)]) (fv bf3)) (fv bf4)) (ap (ap (sym CommRing.toCommSemiring [up(u)]) (fv bf3)) (fv bf7))) (ap (ap (sym CommSemiring.toSemiring [up(v)]) (fv bf4)) (ap (ap (sym CommRing.toCommSemiring [up(v)]) (fv bf4)) (fv bf8))))
  decl bf10

... [11148 more characters]
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
  decl inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2374~bf7 has display is inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2374; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(CommRing,[up(u)]),fv(A~bf3)) .
  decl inst._@.Mathlib.NumberTheory.Cyclotomic.Basic._hyg.2377~bf8 has display is inst._@.Mathlib.NumberTheory.Cyclotomic
... [15754 more characters]
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
    ty: {ap|{sym|Field,[up{w}]},{fv|bf5}}
  - dc bf11
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|Field,[up{z}]},{fv|bf6}}
  - dc bf12
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{ap|{ap|{ap|{sym|Algebra,[up{
... [9970 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*10,929 characters*

```text
(mta
  (smy (thm IsCyclotomicExtension.of_union_of_dvd) (fl Mathlib/NumberTheory/Cyclotomic/Basic.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sym PNat [])))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (ap (sym Set [u0]) (sym PNat []))))
  (dc bf2 (br EXPLICIT) (dr cdecl) (ty (ap (sym Set [u0]) (sym PNat []))))
  (dc bf3 (br EXPLICIT) (dr cdecl) (ty (sort us(up(u)))))
  (dc bf4 (br EXPLICIT) (dr cdecl) (ty (sort us(up(v)))))
  (dc bf5 (br EXPLICIT) (dr cdecl) (ty (sort us(up(w)))))
  (dc bf6 (br EXPLICIT) (dr cdecl) (ty (sort us(up(z)))))
  (dc bf7 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CommRing [up(u)]) (fv bf3))))
  (dc bf8 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym CommRing [up(v)]) (fv bf4))))
  (dc bf9 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym Algebra [up(u) up(v)]) (fv bf3)) (fv bf4)) (ap (ap (sym CommRing.toCommSemiring [up(u)]) (fv bf3)) (fv bf7))) (ap (ap (sym CommSemiring.toSemiring [up(v)]) (fv bf4)) (ap (ap (sym CommRing.toCommSemiring [up(v)]) (fv bf4)) (fv bf8))))))
  (dc bf10 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Field [up(w)]) (fv bf5))))
  (dc bf11 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Field [up(z)]) (fv bf6))))
  (dc bf12 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym Algebra [up(w) up(z)]) (fv bf5)) (fv bf6)) (ap (ap (sym Semifield.toCommSemiring [up(w)]) (fv bf5)) (ap (ap (sym Field.toSemifield [u
... [9529 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*9,837 characters*

```text
mta
  smy
    thm: IsCyclotomicExtension.of_union_of_dvd
    fl: Mathlib/NumberTheory/Cyclotomic/Basic.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: PNat [] sym
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: Set [u0] sym PNat [] sym 1 apn
  dc bf2
    br: EXPLICIT
    dr: cdecl
    ty: Set [u0] sym PNat [] sym 1 apn
  dc bf3
    br: EXPLICIT
    dr: cdecl
    ty: us(up(u)) sort
  dc bf4
    br: EXPLICIT
    dr: cdecl
    ty: us(up(v)) sort
  dc bf5
    br: EXPLICIT
    dr: cdecl
    ty: us(up(w)) sort
  dc bf6
    br: EXPLICIT
    dr: cdecl
    ty: us(up(z)) sort
  dc bf7
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: CommRing [up(u)] sym bf3 fv 1 apn
  dc bf8
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: CommRing [up(v)] sym bf4 fv 1 apn
  dc bf9
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Algebra [up(u) up(v)] sym bf3 fv bf4 fv CommRing.toCommSemiring [up(u)] sym bf3 fv bf7 fv 2 apn CommSemiring.toSemiring [up(v)] sym bf4 fv CommRing.toCommSemiring [up(v)] sym bf4 fv bf8 fv 2 apn 2 apn 4 apn
  dc bf10
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Field [up(w)] sym bf5 fv 1 apn
  dc bf11
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Field [up(z)] sym bf6 fv 1 apn
  dc bf12
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Algebra [up(w) up(z)] sym bf5 fv bf6 fv Semifield.toCommSemiring [up(w)] sym bf5 fv Field.toSemifield [up(w)] sym bf5 fv bf10 fv 2 apn 2 
... [8437 more characters]
```

### FINALIST R_623a343174ec

*14,241 characters*

```text
meta
  summary ;; theorem: IsCyclotomicExtension.of_union_of_dvd ;; file: Mathlib/NumberTheory/Cyclotomic/Basic.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: PNat [] sym
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Set [u0] sym PNat [] sym ap
  decl bf2 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: Set [u0] sym PNat [] sym ap
  decl bf3 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: us(up(u)) sort
  decl bf4 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: us(up(v)) sort
  decl bf5 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: us(up(w)) sort
  decl bf6 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: us(up(z)) sort
  decl bf7 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: CommRing [up(u)] sym bf3 fv ap
  decl bf8 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: CommRing [up(v)] sym bf4 fv ap
  decl bf9 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: Algebra [up(u) up(v)] sym bf3 fv ap bf4 fv ap CommRing.toCommSemiring [up(u)] sym bf3 fv ap bf7 fv ap ap CommSemiring.toSemiring [up(v)] sym bf4 fv ap CommRing.toCommSemiring [up(v)] sym bf4 fv ap bf8 fv ap ap ap
  decl bf10 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: Field [up(w)] sym bf5 fv ap
  decl bf1
... [12841 more characters]
```

### FINALIST R_8f1e3d8b7028

*13,320 characters*

```text
meta
  summary
    theorem: IsCyclotomicExtension.of_union_of_dvd
    file: Mathlib/NumberTheory/Cyclotomic/Basic.lean
state_before
  goal bm2
    target: (ap (ap (sym Exists [us(up(v))]) (fv bf4)) (lam EXPLICIT (fv bf4) (ap (ap (ap (ap (sym IsPrimitiveRoot [up(v)]) (fv bf4)) (ap (ap (sym CommRing.toCommMonoid [up(v)]) (fv bf4)) (fv bf8))) (bv 0)) (ap (sym PNat.val []) (fv bf17)))))
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15,bf16,bf17,bf18]
  alias bf17
    tag: metavariable_reference
  alias bf4
    tag: sort
  alias bf8
    tag: CommRing
  decl bf4
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort us(up(v)))
  decl bf8
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (sym CommRing [up(v)]) (fv bf4))
  decl bf17
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (mv bm0)
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sym PNat [])
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (sym Set [u0]) (sym PNat []))
  decl bf2
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (ap (sym Set [u0]) (sym PNat []))
  decl bf3
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm2
    type: (sort us(up(u)))
  decl bf5

... [11920 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*24,746 characters*

```text
aliases
  alias $a0
    term: (pi EXPLICIT (pi EXPLICIT (sym PNat []) (pi EXPLICIT (ap (ap (ap (ap (ap (sym Membership.mem [u0 u0]) (sym PNat [])) (ap (sym Set [u0]) (sym PNat []))) (ap (sym Set.instMembership [u0]) (sym PNat []))) (bv 0)) (fv bf1)) (ap (ap (ap (ap (sym Dvd.dvd [u0]) (sym PNat [])) (ap (ap (sym semigroupDvd [u0]) (sym PNat [])) (ap (ap (sym Monoid.toSemigroup [u0]) (sym PNat [])) (ap (ap (sym CommMonoid.toMonoid [u0]) (sym PNat [])) (ap (ap (sym OrderedCommMonoid.toCommMonoid [u0]) (sym PNat [])) (ap (ap (sym LinearOrderedCommMonoid.toOrderedCommMonoid [u0]) (sym PNat [])) (ap (ap (sym LinearOrderedCancelCommMonoid.toLinearOrderedCommMonoid [u0]) (sym PNat [])) (sym instPNatLinearOrderedCancelCommMonoid [])))))))) (fv bf0)) (bv 1)))) (pi EXPLICIT (ap (ap (sym Set.Nonempty [u0]) (sym PNat [])) (fv bf1)) (pi INSTANCE_IMPLICIT (ap (ap (ap (ap (ap (ap (sym IsCyclotomicExtension [up(u) up(v)]) (fv bf1)) (fv bf3)) (fv bf4)) (fv bf7)) (fv bf8)) (fv bf9)) (ap (ap (ap (ap (ap (ap (sym IsCyclotomicExtension [up(u) up(v)]) (ap (ap (ap (ap (sym Union.union [u0]) (ap (sym Set [u0]) (sym PNat []))) (ap (sym Set.instUnion [u0]) (sym PNat []))) (fv bf1)) (ap (ap (ap (ap (sym Singleton.singleton [u0 u0]) (sym PNat [])) (ap (sym Set [u0]) (sym PNat []))) (ap (sym Set.instSingletonSet [u0]) (sym PNat []))) (fv bf0)))) (fv bf3)) (fv bf4)) (fv bf7)) (fv bf8)) (fv bf9)))))
  alias $
... [23346 more characters]
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
    ∈: pi(INSTANCE_IMPLICIT,ap(sym(Finite,[us(up(u_3))]),fv(β~bf2)),pi(IMPLICIT,ap(sym(Equiv.Perm,[us(up(u_3))]),fv(β~bf2)),pi(EXPLICIT,ap(ap(sym(Equiv.Perm.IsCycle,[up(u_3)]),fv(β~bf2)),bv(0)),pi(EX
... [16002 more characters]
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
    type: (pi INSTANCE_IMPLICIT (ap (sym Finite [us(up(u_3))]) (fv bf2)) (pi IMPLICIT (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2)) (pi EXPLICIT (ap (ap (sym Equiv.Perm.IsCycle [up(u_3)]) (fv bf2)) (bv 0)) (pi EXPLICIT (ap (sym Nat.Prime []) (ap (a
... [16283 more characters]
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
  decl inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9904~bf7 has display is inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9904; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(DecidableEq,[us(up(u_2))]),fv(α~bf1)) .
  decl inst._@.Mathlib.GroupTheory.Perm.Cycle.Basic._hyg.9907~bf8 has display
... [18827 more characters]
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
    ty: {pi|INSTANCE_IMPLICIT,{ap|{sym|Finite,[us{up{u_3}}]},{fv|bf2}},{pi|IMPLICIT,{ap|{sym|Equiv.Perm,[us{up{u_3}}]},{fv|bf2}},{pi|EXPLICIT,{ap|{ap|{sym|Equiv.Perm.IsCycle,[up{u_3}]},{fv|bf2}},{bv|0}},{pi|EXPLICIT,{ap|{sym|Nat.Prime,[]},{ap|{ap|{ap|{sym|orderOf,[up{u_3}]},{ap|{sym|Equiv.Perm,[us{up{u_3}}]},{fv|bf2}}},{ap|{ap|{sym|DivInvMonoid.toMonoid,[up{u_3}]},{ap|{sym|Equiv.Perm,[us{up{u_3}}]},{fv|bf2}}},{ap|{ap|{sym|Group.toDivInvMonoid,[up{u_3}]},{ap|{sym|Equiv.Perm,[us{up{u_3}}]},{fv|bf2}}},{ap|{sym|E
... [14895 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*15,752 characters*

```text
(mta
  (smy (thm Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order) (fl Mathlib/GroupTheory/Perm/Cycle/Basic.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_3)))))
  (dc bf3 (br IMPLICIT) (dr cdecl) (ty (ap (sym Equiv.Perm [us(up(u_2))]) (fv bf1))))
  (dc bf4 (br IMPLICIT) (dr cdecl) (ty (ap (sym Equiv.Perm [us(up(u_2))]) (fv bf1))))
  (dc bf5 (br IMPLICIT) (dr cdecl) (ty (fv bf1)))
  (dc bf6 (br IMPLICIT) (dr cdecl) (ty (fv bf1)))
  (dc bf7 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym DecidableEq [us(up(u_2))]) (fv bf1))))
  (dc bf8 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym Fintype [up(u_2)]) (fv bf1))))
  (dc bf9 (br EXPLICIT) (dr cdecl) (ty (pi INSTANCE_IMPLICIT (ap (sym Finite [us(up(u_3))]) (fv bf2)) (pi IMPLICIT (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2)) (pi EXPLICIT (ap (ap (sym Equiv.Perm.IsCycle [up(u_3)]) (fv bf2)) (bv 0)) (pi EXPLICIT (ap (sym Nat.Prime []) (ap (ap (ap (sym orderOf [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym DivInvMonoid.toMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym Group.toDivInvMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (sym Equiv.Perm.permGroup [up(u_3)]) (fv bf2))))) (bv 1))) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (a
... [14352 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*14,407 characters*

```text
mta
  smy
    thm: Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order
    fl: Mathlib/GroupTheory/Perm/Cycle/Basic.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_2)) sort
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_3)) sort
  dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: Equiv.Perm [us(up(u_2))] sym bf1 fv 1 apn
  dc bf4
    br: IMPLICIT
    dr: cdecl
    ty: Equiv.Perm [us(up(u_2))] sym bf1 fv 1 apn
  dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: bf1 fv
  dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: bf1 fv
  dc bf7
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: DecidableEq [us(up(u_2))] sym bf1 fv 1 apn
  dc bf8
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: Fintype [up(u_2)] sym bf1 fv 1 apn
  dc bf9
    br: EXPLICIT
    dr: cdecl
    ty: INSTANCE_IMPLICIT Finite [us(up(u_3))] sym bf2 fv 1 apn IMPLICIT Equiv.Perm [us(up(u_3))] sym bf2 fv 1 apn EXPLICIT Equiv.Perm.IsCycle [up(u_3)] sym bf2 fv 0 bv 2 apn EXPLICIT Nat.Prime [] sym orderOf [up(u_3)] sym Equiv.Perm [us(up(u_3))] sym bf2 fv 1 apn DivInvMonoid.toMonoid [up(u_3)] sym Equiv.Perm [us(up(u_3))] sym bf2 fv 1 apn Group.toDivInvMonoid [up(u_3)] sym Equiv.Perm [us(up(u_3))] sym bf2 fv 1 apn Equiv.Perm.permGroup [up(u_3)] sym bf2 fv 1 apn 2 apn 2 apn 1 bv 3 apn 1 apn EXPLICIT Nat [] sym EXPLICIT LT.lt [u0] sym Nat [] sym instLT
... [13007 more characters]
```

### FINALIST R_623a343174ec

*18,343 characters*

```text
meta
  summary ;; theorem: Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order ;; file: Mathlib/GroupTheory/Perm/Cycle/Basic.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_2)) sort
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_3)) sort
  decl bf3 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Equiv.Perm [us(up(u_2))] sym bf1 fv ap
  decl bf4 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: Equiv.Perm [us(up(u_2))] sym bf1 fv ap
  decl bf5 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: bf1 fv
  decl bf6 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: bf1 fv
  decl bf7 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: DecidableEq [us(up(u_2))] sym bf1 fv ap
  decl bf8 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: Fintype [up(u_2)] sym bf1 fv ap
  decl bf9 ;; binder_role: EXPLICIT ;; declaration_role: cdecl ;; type: INSTANCE_IMPLICIT Finite [us(up(u_3))] sym bf2 fv ap IMPLICIT Equiv.Perm [us(up(u_3))] sym bf2 fv ap EXPLICIT Equiv.Perm.IsCycle [up(u_3)] sym bf2 fv ap 0 bv ap EXPLICIT Nat.Prime [] sym orderOf [up(u_3)] sym Equiv.Perm [us(up(u_3))] sym bf2 fv ap ap DivInvMonoid.toMonoid [up(u_3)] sym Equiv.Perm [us(u
... [16943 more characters]
```

### FINALIST R_8f1e3d8b7028

*18,513 characters*

```text
meta
  summary
    theorem: Equiv.Perm.IsCycle.isCycle_pow_pos_of_lt_prime_order
    file: Mathlib/GroupTheory/Perm/Cycle/Basic.lean
state_before
  goal bm4
    target: (ann (ap (ap (sym Equiv.Perm.IsCycle [up(u_3)]) (fv bf2)) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [up(u_3) u0 up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (sym Nat [])) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (ap (sym instHPow [up(u_3) u0]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (sym Nat [])) (ap (sym Equiv.Perm.instPowNat [up(u_3)]) (fv bf2)))) (fv bf11)) (fv bf14))))
    context: [bf0,bf1,bf2,bf3,bf4,bf5,bf6,bf7,bf8,bf9,bf10,bf11,bf12,bf13,bf14,bf15,bf16,bf17,bf18,bf19,bf20,bf21]
  alias bf11
    tag: Equiv.Perm
  alias bf14
    tag: Nat
  alias bf2
    tag: sort
  decl bf2
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (sort us(up(u_3)))
  decl bf11
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))
  decl bf14
    binder_role: EXPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (sym Nat [])
  decl bf0
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (sort us(up(u_1)))
  decl bf1
    binder_role: IMPLICIT
    declaration_role: cdecl
    scope: bm4
    type: (sort us(up(u_2)))
  decl bf3
    binder_role: IMPLICIT
    declaration_role: cd
... [17113 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*35,553 characters*

```text
aliases
  alias $a0
    term: (pi INSTANCE_IMPLICIT (ap (sym Finite [us(up(u_3))]) (fv bf2)) (pi IMPLICIT (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2)) (pi EXPLICIT (ap (ap (sym Equiv.Perm.IsCycle [up(u_3)]) (fv bf2)) (bv 0)) (pi EXPLICIT (ap (sym Nat.Prime []) (ap (ap (ap (sym orderOf [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym DivInvMonoid.toMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym Group.toDivInvMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (sym Equiv.Perm.permGroup [up(u_3)]) (fv bf2))))) (bv 1))) (pi EXPLICIT (sym Nat []) (pi EXPLICIT (ap (ap (ap (ap (sym LT.lt [u0]) (sym Nat [])) (sym instLTNat [])) (ap (ap (ap (sym OfNat.ofNat [u0]) (sym Nat [])) (lit NAT 0)) (ap (sym instOfNatNat []) (lit NAT 0)))) (bv 0)) (pi EXPLICIT (ap (ap (ap (ap (sym LT.lt [u0]) (sym Nat [])) (sym instLTNat [])) (bv 1)) (ap (ap (ap (sym orderOf [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym DivInvMonoid.toMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (ap (sym Group.toDivInvMonoid [up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (ap (sym Equiv.Perm.permGroup [up(u_3)]) (fv bf2))))) (bv 4))) (ap (ap (sym Equiv.Perm.IsCycle [up(u_3)]) (fv bf2)) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [up(u_3) u0 up(u_3)]) (ap (sym Equiv.Perm [us(up(u_3))]) (fv bf2))) (sym Nat [])) (ap 
... [34153 more characters]
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
    ∈: ap(ap(ap(ap(sym(NormedSpace,[u0 up(u_4)]),sym(Real,[])),fv(E~bf3)),sym(Real.normedField,[])),ap(ap(sym(NormedAddCommGroup.toSeminormedAddCommGroup,[up(u_4)]),fv(E~bf3)),fv(inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9986~bf7)))
  D inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9995~bf9
    n: inst._@.Mathlib.Analysis.Distributio
... [19508 more characters]
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
    type: (ap (ap (ap (ap (sym NormedSpace [u0 up(u_4)]) (sym Real [])) (fv bf3)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7)))
  decl bf9
    binder_role: INSTANCE_IMPLICIT
    declaration_role: cdecl
    type: (ap (sym NormedAddCommGroup [up(u_5)]) (fv bf4))
  decl bf10
    binder_role: INSTANCE_IMPLICIT
    declaratio
... [16090 more characters]
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
  decl inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9986~bf7 has display is inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9986; and binder_role is INSTANCE_IMPLICIT; and declaration_role is cdecl; and type is ap(sym(NormedAddCommGroup,[up(u_4)]),fv(E~bf3)) .
  decl inst._@.Mathlib.Analysis.Distribution.SchwartzSpace._hyg.9989~bf8 has display is inst._@.M
... [21220 more characters]
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
    ty: {ap|{ap|{ap|{ap|{sym|NormedSpace,[u0 up{u_5}]},{sym|Real,[]}},{fv|bf4}},{sym|Real.normedField,[]}},{ap|{ap|{sym|NormedAddCommGroup.toSeminormedAddCommGroup,[up{u_5}]},{fv|bf4}},{fv|bf9}}}
  - dc bf11
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: {ap|{sym|NormedAddComm
... [15222 more characters]
```

### FINALIST SEED_CANONICAL_SEXPR

*16,322 characters*

```text
(mta
  (smy (thm SchwartzMap.integrable_of_le_of_pow_mul_le) (fl Mathlib/Analysis/Distribution/SchwartzSpace.lean))
)
(sb
  (dc bf0 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_1)))))
  (dc bf1 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_2)))))
  (dc bf2 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_3)))))
  (dc bf3 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_4)))))
  (dc bf4 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_5)))))
  (dc bf5 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_6)))))
  (dc bf6 (br IMPLICIT) (dr cdecl) (ty (sort us(up(u_7)))))
  (dc bf7 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_4)]) (fv bf3))))
  (dc bf8 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_4)]) (sym Real [])) (fv bf3)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7)))))
  (dc bf9 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_5)]) (fv bf4))))
  (dc bf10 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [u0 up(u_5)]) (sym Real [])) (fv bf4)) (sym Real.normedField [])) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_5)]) (fv bf4)) (fv bf9)))))
  (dc bf11 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (sym NormedAddCommGroup [up(u_3)]) (fv bf2))))
  (dc bf12 (br INSTANCE_IMPLICIT) (dr cdecl) (ty (ap (ap (ap (ap (sym NormedSpace [
... [14922 more characters]
```

### FINALIST SEED_HYBRID_RPN_MACHINE

*13,847 characters*

```text
mta
  smy
    thm: SchwartzMap.integrable_of_le_of_pow_mul_le
    fl: Mathlib/Analysis/Distribution/SchwartzSpace.lean
sb
  dc bf0
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_1)) sort
  dc bf1
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_2)) sort
  dc bf2
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_3)) sort
  dc bf3
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_4)) sort
  dc bf4
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_5)) sort
  dc bf5
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_6)) sort
  dc bf6
    br: IMPLICIT
    dr: cdecl
    ty: us(up(u_7)) sort
  dc bf7
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedAddCommGroup [up(u_4)] sym bf3 fv 1 apn
  dc bf8
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedSpace [u0 up(u_4)] sym Real [] sym bf3 fv Real.normedField [] sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)] sym bf3 fv bf7 fv 2 apn 4 apn
  dc bf9
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedAddCommGroup [up(u_5)] sym bf4 fv 1 apn
  dc bf10
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedSpace [u0 up(u_5)] sym Real [] sym bf4 fv Real.normedField [] sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_5)] sym bf4 fv bf9 fv 2 apn 4 apn
  dc bf11
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedAddCommGroup [up(u_3)] sym bf2 fv 1 apn
  dc bf12
    br: INSTANCE_IMPLICIT
    dr: cdecl
    ty: NormedSpace [u0 up(u_3)] sym
... [12447 more characters]
```

### FINALIST R_623a343174ec

*18,095 characters*

```text
meta
  summary ;; theorem: SchwartzMap.integrable_of_le_of_pow_mul_le ;; file: Mathlib/Analysis/Distribution/SchwartzSpace.lean
state_before
  decl bf0 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_1)) sort
  decl bf1 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_2)) sort
  decl bf2 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_3)) sort
  decl bf3 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_4)) sort
  decl bf4 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_5)) sort
  decl bf5 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_6)) sort
  decl bf6 ;; binder_role: IMPLICIT ;; declaration_role: cdecl ;; type: us(up(u_7)) sort
  decl bf7 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedAddCommGroup [up(u_4)] sym bf3 fv ap
  decl bf8 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedSpace [u0 up(u_4)] sym Real [] sym ap bf3 fv ap Real.normedField [] sym ap NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)] sym bf3 fv ap bf7 fv ap ap
  decl bf9 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedAddCommGroup [up(u_5)] sym bf4 fv ap
  decl bf10 ;; binder_role: INSTANCE_IMPLICIT ;; declaration_role: cdecl ;; type: NormedSpace [u0 up(u_5)] sym Real [] sym ap bf4 fv ap Real.norm
... [16695 more characters]
```

### FINALIST R_8f1e3d8b7028

*18,284 characters*

```text
meta
  summary
    theorem: SchwartzMap.integrable_of_le_of_pow_mul_le
    file: Mathlib/Analysis/Distribution/SchwartzSpace.lean
state_before
  goal bm0
    target: (ap (ap (ap (ap (sym LE.le [u0]) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (sym instHMul [u0]) (sym Real [])) (sym Real.instMul []))) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [u0 u0 u0]) (sym Real [])) (sym Nat [])) (sym Real [])) (ap (ap (ap (sym instHPow [u0 u0]) (sym Real [])) (sym Nat [])) (ap (ap (sym Monoid.toNatPow [u0]) (sym Real [])) (sym Real.instMonoid [])))) (ap (ap (ap (sym Norm.norm [up(u_3)]) (fv bf2)) (ap (ap (sym SeminormedAddCommGroup.toNorm [up(u_3)]) (fv bf2)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_3)]) (fv bf2)) (fv bf11)))) (fv bf27))) (fv bf23))) (ap (ap (ap (sym Norm.norm [up(u_4)]) (fv bf3)) (ap (ap (sym SeminormedAddCommGroup.toNorm [up(u_4)]) (fv bf3)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7)))) (ap (fv bf20) (fv bf27))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (sym instHMul [u0]) (sym Real [])) (ap (ap (sym NonUnitalNonAssocRing.toMul [u0]) (sym Real [])) (ap (ap (sym NonAssocRing.toNonUnitalNonAssocRing [u0]) (sym Real [])) (ap (ap (sym Ring.toNonAssocRing [u
... [16884 more characters]
```

### FINALIST SEED_HYBRID_LOCAL_DAG

*39,150 characters*

```text
aliases
  alias $a0
    term: (ap (ap (ap (ap (sym LE.le [u0]) (sym Real [])) (sym Real.instLE [])) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (sym instHMul [u0]) (sym Real [])) (sym Real.instMul []))) (ap (ap (ap (ap (ap (ap (sym HPow.hPow [u0 u0 u0]) (sym Real [])) (sym Nat [])) (sym Real [])) (ap (ap (ap (sym instHPow [u0 u0]) (sym Real [])) (sym Nat [])) (ap (ap (sym Monoid.toNatPow [u0]) (sym Real [])) (sym Real.instMonoid [])))) (ap (ap (ap (sym Norm.norm [up(u_3)]) (fv bf2)) (ap (ap (sym SeminormedAddCommGroup.toNorm [up(u_3)]) (fv bf2)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_3)]) (fv bf2)) (fv bf11)))) (fv bf27))) (fv bf23))) (ap (ap (ap (sym Norm.norm [up(u_4)]) (fv bf3)) (ap (ap (sym SeminormedAddCommGroup.toNorm [up(u_4)]) (fv bf3)) (ap (ap (sym NormedAddCommGroup.toSeminormedAddCommGroup [up(u_4)]) (fv bf3)) (fv bf7)))) (ap (fv bf20) (fv bf27))))) (ap (ap (ap (ap (ap (ap (sym HMul.hMul [u0 u0 u0]) (sym Real [])) (sym Real [])) (sym Real [])) (ap (ap (sym instHMul [u0]) (sym Real [])) (ap (ap (sym NonUnitalNonAssocRing.toMul [u0]) (sym Real [])) (ap (ap (sym NonAssocRing.toNonUnitalNonAssocRing [u0]) (sym Real [])) (ap (ap (sym Ring.toNonAssocRing [u0]) (sym Real [])) (ap (ap (sym NormedRing.toRing [u0]) (sym Real [])) (ap (ap (sym NormedCommRing.toNormedRing [u0]) (sym Real [])) (sy
... [37750 more characters]
```
