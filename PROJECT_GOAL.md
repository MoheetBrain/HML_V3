# HML / HAMILTONIAN LANGUAGE — PERMANENT PROJECT GOAL

> This document is the project's permanent objective. It outranks any milestone,
> roadmap, benchmark, report or decision record in this repository. Where a
> subordinate document appears to justify work that does not serve the goal
> stated here, this document wins.

## PRIMARY GOAL

The ultimate goal of this project is to create a mathematical representation
language that measurably improves Moheet's ability to understand, reason about,
and solve mathematical problems.

The language is not being created primarily for elegance, notation design,
formal-methods research, theorem-prover compatibility, or benchmark performance.

Those are supporting objectives.

The primary human objective is:

    GIVEN THE SAME MATHEMATICAL PROBLEM,

    MOHEET USING THE DISCOVERED LANGUAGE

    SHOULD BE ABLE TO:

        understand the problem faster;
        identify the important mathematical objects more reliably;
        see dependencies and constraints more clearly;
        maintain reasoning over longer chains;
        make fewer logical mistakes;
        recover when reasoning fails;
        discover useful intermediate steps;
        and solve harder problems than Moheet can solve using ordinary notation alone.

Formally:

Let:

    P = a mathematical problem

    N(P) = the conventional mathematical representation of P

    H(P) = the machine-oriented / HML representation of P

    A(M, P) = Moheet's mathematical problem-solving performance
              when using representation M on problem P.

The project seeks a representation H* such that:

    A(H*, P) > A(N, P)

across a broad and increasingly difficult distribution of mathematical problems.

The desired improvement is not merely subjective preference.

It should eventually be measurable through:

    solution accuracy
    time-to-solution
    number of invalid steps
    number of abandoned paths
    working-memory burden
    ability to continue long derivations
    ability to identify relevant information
    ability to recover after errors
    transfer to unseen problems
    performance as problem complexity increases.


# =====================================================================
# 1. CORE HYPOTHESIS
# =====================================================================

The project is based on the hypothesis that conventional mathematical notation
is optimized primarily for:

    human communication
    historical convention
    compactness
    paper
    expert familiarity

and is not necessarily optimal for:

    artificial reasoners

or even:

    a human reasoner using AI as an external cognitive system.

Therefore there may exist alternative representations of the SAME mathematics
that make its computational and logical structure substantially easier to reason
over.


# =====================================================================
# 2. REPRESENTATION HYPOTHESIS
# =====================================================================

Mathematical meaning and mathematical representation are different.

Let:

    M = mathematical meaning / canonical mathematical state

and:

    R(M) = a representation of that meaning.

Multiple representations can preserve exactly the same mathematical content:

    ordinary notation
    Lean
    structured English
    AST
    graph
    S-expression
    HML
    future machine-discovered representations

while exposing different structures to the reasoner.

Therefore:

    mathematical truth should remain fixed;

    representation should be experimentally optimized.


# =====================================================================
# 3. LONG-HORIZON REASONING HYPOTHESIS
# =====================================================================

A central hypothesis of this project is that representation quality matters
increasingly as reasoning horizon increases.

For a trivial one-step problem, representation may matter very little.

For a 50-step or 500-step reasoning problem, small representation defects may
compound.

Examples:

    ambiguous scope;
    distant dependencies;
    unstable identifiers;
    hidden assumptions;
    overloaded notation;
    forgotten intermediate results;
    unclear goal state;
    poor separation between facts and conjectures.

Therefore we hypothesize:

    Benefit(R) increases with reasoning horizon.

Conceptually:

    representation advantage
            ↑
            |
            |                         /
            |                      /
            |                   /
            |               /
            |___________/
            +--------------------------→
                    reasoning depth

This is a HYPOTHESIS, not an established fact.

It must be tested.


# =====================================================================
# 4. COGNITIVE OFFLOADING HYPOTHESIS
# =====================================================================

Human mathematical reasoning is constrained by limited working memory.

A good representation may externalize information that would otherwise have to
be mentally maintained.

Examples:

    which variable belongs to which binder;
    which assumptions support a conclusion;
    what the current goal is;
    which branches remain open;
    what changed during the previous step;
    which facts are established versus speculative;
    what prerequisites an action requires.

Therefore a useful mathematical language may behave as:

    external working memory

rather than merely:

    alternative notation.

The project should test whether explicit mathematical state reduces cognitive
load and prevents reasoning-state loss.


# =====================================================================
# 5. DEPENDENCY-LOCALITY HYPOTHESIS
# =====================================================================

Reasoning may become easier when mathematically related information is close in
the representation.

Examples:

    premise near conclusion;
    binder near use;
    type near term;
    assumption near dependent step;
    goal near relevant context.

Therefore the project investigates whether reducing semantic relation distance
improves reasoning.

However:

    shorter distance != automatically better reasoning.

Locality is a proxy and must ultimately be validated through human/model
performance.


# =====================================================================
# 6. EXPLICIT-STATE HYPOTHESIS
# =====================================================================

Ordinary mathematical solutions often hide reasoning state.

The solver must reconstruct:

    current assumptions
    current goal
    unresolved subgoals
    dependencies
    previous transformations
    candidate ideas
    rejected branches

from prose or memory.

We hypothesize that explicitly representing reasoning state can make long
mathematical reasoning more reliable.

Conceptually:

    S_t = current mathematical state

    A_t = proposed reasoning action

    S_t --A_t--> S_t+1

A useful language should make this transition understandable and inspectable.


# =====================================================================
# 7. ERROR-LOCALIZATION HYPOTHESIS
# =====================================================================

In conventional derivations, a mistake can contaminate many later steps before
being noticed.

A structured mathematical language may make errors easier to localize.

The desired property is:

    reasoning error
        ↓
    identifiable violated relation / assumption / transformation

rather than:

    reasoning error
        ↓
    entire solution becomes mysterious.

This may be especially important for long-horizon mathematics.


# =====================================================================
# 8. SEARCH / DISCOVERY HYPOTHESIS
# =====================================================================

Solving mathematics is not only deduction.

It also involves:

    trying approaches
    forming conjectures
    discovering lemmas
    abandoning dead ends
    comparing alternative branches
    recognizing useful intermediate structure.

Therefore the final language may need to represent both:

    DEDUCTIVE STATE

and:

    DISCOVERY STATE.

A representation that stores only polished successful proofs may be insufficient
for actual problem solving.


# =====================================================================
# 9. HUMAN + AI HYPOTHESIS
# =====================================================================

The target user is not an unaided human.

The intended system is:

    MOHEET
        +
    AI
        +
    MATHEMATICAL REPRESENTATION
        +
    VERIFIER / COMPUTATIONAL TOOLS

forming one reasoning system.

Therefore the optimal representation does not necessarily have to be:

    maximally natural for humans

or:

    maximally natural for language models.

It should optimize the JOINT SYSTEM.

Conceptually:

    performance =
        f(
            human,
            AI,
            representation,
            verifier,
            search process
        )

The best representation may therefore look unusual compared with traditional
mathematics while still being much easier for the combined human-AI system to
reason with.


# =====================================================================
# 10. MACHINE-READABILITY HYPOTHESIS
# =====================================================================

A machine mathematical representation may outperform conventional notation
because it can expose information that natural mathematical notation often
leaves implicit.

Potentially useful explicit information includes:

    object identity
    types
    binders
    scope
    dependencies
    goals
    assumptions
    premises
    obligations
    actions
    state changes
    provenance
    branch structure

However:

    more explicit information is not automatically better.

Too much information may create noise.

The project therefore seeks:

    MINIMUM SUFFICIENT EXPLICIT STRUCTURE

rather than maximum verbosity.


# =====================================================================
# 11. ADAPTIVE REPRESENTATION HYPOTHESIS
# =====================================================================

There may not be one fixed serialization that is optimal for every problem.

The best representation may depend on mathematical state.

Therefore eventually investigate:

    R*(M)

rather than only:

    one universal R*.

Example:

    simple algebra
        -> compact representation

    huge proof state
        -> goal-conditioned dependency capsule

    deeply nested quantified problem
        -> binder/scope-emphasized representation

The compiler itself may eventually choose how mathematics should be presented.


# =====================================================================
# 12. CENTRAL SCIENTIFIC QUESTION
# =====================================================================

The central research question is:

    CAN WE FIND A REPRESENTATION OF MATHEMATICS THAT MAKES
    MATHEMATICAL REASONING EASIER THAN CONVENTIONAL NOTATION,
    ESPECIALLY AS PROBLEMS BECOME LONGER, DEEPER, AND MORE
    STRUCTURALLY COMPLEX?

A stronger version is:

    CAN A MACHINE-DISCOVERED REPRESENTATION ACT AS A COGNITIVE
    AMPLIFIER FOR A HUMAN + AI MATHEMATICAL REASONING SYSTEM?


# =====================================================================
# 13. WHAT SUCCESS LOOKS LIKE
# =====================================================================

The project succeeds only if the representation eventually produces measurable
reasoning improvement.

Example success criterion:

For a held-out problem set:

    conventional representation:
        accuracy = 55%
        median solve time = 18 min

    discovered representation:
        accuracy = 72%
        median solve time = 11 min

with particularly large improvements on:

    long proofs
    deep dependency problems
    multi-stage algebra
    calculus derivations
    probability/statistics reasoning
    proof-like problems

The exact thresholds must eventually be preregistered.

The important point is:

    REPRESENTATION MUST CHANGE PERFORMANCE.


# =====================================================================
# 14. WHAT DOES NOT COUNT AS SUCCESS
# =====================================================================

The project does NOT succeed merely because:

    the language is elegant;

    the language is formal;

    Lean can parse it;

    the language has fewer tokens;

    dependencies are closer together;

    Claude thinks it looks good;

    Gemma performs well on one toy benchmark;

    the representation search converges;

    HML beats one weak control;

    a metric improves.

Those are intermediate signals.

The final objective is:

    BETTER MATHEMATICAL REASONING.


# =====================================================================
# 15. PERSONAL HUMAN EVALUATION
# =====================================================================

Because the ultimate target includes Moheet's own mathematical performance,
eventually include human crossover experiments.

For matched problems:

    randomly assign representation A or B;

    hide which representation is considered the new candidate where practical;

    measure:

        correctness
        time
        number of hints
        number of reversals
        number of invalid steps
        subjective cognitive load
        ability to explain final reasoning

Compare:

    ordinary notation

versus:

    discovered representation.

Do not train specifically on the test problems.


# =====================================================================
# 16. LONG-HORIZON EVALUATION
# =====================================================================

Evaluation difficulty should deliberately increase.

Test approximately:

    H1:
        1–3 reasoning steps

    H2:
        4–10 steps

    H3:
        10–30 steps

    H4:
        30–100 steps

    H5:
        extended proof/search trajectories

The key interaction to estimate is:

    representation × horizon.

We want to know whether:

    Δperformance(R)
        grows

as:

    reasoning horizon grows.

That is one of the central claims of the project.


# =====================================================================
# 17. DOMAIN GENERALITY
# =====================================================================

The representation must not become an algebra trick.

Test across:

    algebra
    geometry
    calculus / analysis
    probability / statistics
    logic / sets
    linear algebra
    number theory
    combinatorics

Structural improvements should preferably transfer across domains.


# =====================================================================
# 18. FALSIFICATION
# =====================================================================

The project must permit its own core hypothesis to fail.

Possible outcome:

    conventional notation + structured English
    is already close to optimal for the tested human/AI systems.

Possible outcome:

    representation matters for machines but not humans.

Possible outcome:

    representation matters only on long horizons.

Possible outcome:

    benefits are architecture-specific.

Possible outcome:

    no representation consistently beats strong controls.

These are legitimate scientific outcomes.

Do not make HML win by changing the experiment.


# =====================================================================
# 19. DESIGN PRINCIPLE
# =====================================================================

Every representation feature must answer:

    WHAT REASONING FAILURE IS THIS FEATURE SUPPOSED TO REDUCE?

Examples:

    explicit binder IDs
        -> reduce variable-binding mistakes

    dependency locality
        -> reduce dependency-search burden

    explicit goals
        -> reduce goal-state loss

    state deltas
        -> reduce confusion about what changed

    branch identity
        -> reduce search-path confusion

A feature without a causal reasoning hypothesis should not be added merely
because it looks clean.


# =====================================================================
# 20. OPTIMIZATION PRIORITY
# =====================================================================

Optimize in this order:

    1. mathematical correctness

    2. preservation of meaning

    3. reasoning usefulness

    4. long-horizon robustness

    5. generalization

    6. cognitive / neural accessibility

    7. compute efficiency

    8. token efficiency

    9. aesthetics

Never sacrifice mathematical correctness for model convenience.


# =====================================================================
# 21. FINAL NORTH STAR
# =====================================================================

The ultimate product is not merely:

    HML syntax.

The ultimate product is:

    A MATHEMATICAL COGNITIVE INTERFACE.

Its purpose is to transform:

    difficult mathematical state

into:

    a representation in which the important relationships are sufficiently
    explicit, local, stable and structured that Moheet + AI can reason farther,
    more accurately, and with less cognitive friction.

The strongest form of the hypothesis is:

    ORDINARY MATHEMATICS MAY BE A GOOD HUMAN COMMUNICATION LANGUAGE
    WITHOUT BEING THE BEST HUMAN-AI REASONING LANGUAGE.

Our job is to test that hypothesis rigorously.


# =====================================================================
# PERMANENT ONE-SENTENCE GOAL
# =====================================================================

DISCOVER AND BUILD A MATHEMATICAL REPRESENTATION SYSTEM THAT ALLOWS
MOHEET + AI TO SOLVE MATHEMATICAL PROBLEMS MORE ACCURATELY, MORE
QUICKLY, AND OVER LONGER REASONING HORIZONS THAN CONVENTIONAL
MATHEMATICAL NOTATION, WHILE PRESERVING EXACT MATHEMATICAL MEANING
AND SUBJECTING EVERY CLAIMED ADVANTAGE TO CONTROLLED EMPIRICAL TESTING.
