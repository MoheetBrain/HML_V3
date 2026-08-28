# External sources

Large external repositories and datasets are not vendored here. Reproducible acquisition
scripts place optional checkouts below ignored `external/checkouts/`; manifests record the
exact source identity and expected content.

Acquisition refuses an unexpected origin, wrong commit, or dirty checkout. Local receipts
are written beneath ignored `data/cache/acquisition_receipts/`; the committed acquisition
report records the verified identities and tree fingerprints without embedding the source
repositories.
