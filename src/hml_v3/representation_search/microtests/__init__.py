"""Mechanism-specific CPU microtests.

The Pareto vector measures cost and aggregate locality. It does not answer the question a
reader of the language actually has to answer: *given this rendering, how hard is it to find
the binder that owns this use?* A representation can look cheap and local on average while
making every specific structural query expensive.

Each suite asks a question whose ground truth comes from the canonical state — never from a
rendering and never from a model — and measures deterministic access cost in the rendered
text. These run in milliseconds, so a candidate that is structurally opaque dies before any
expensive evaluation is spent on it.
"""

from hml_v3.representation_search.microtests.suites import (  # noqa: F401
    SUITES,
    SuiteResult,
    run_all_suites,
    run_suite,
)
