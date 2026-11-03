# Repository inspection and implementation boundary

Inspected the existing public repository before edits. The requested
`OppositeExpert/T2DM` URL resolves to `pranavprabhu05/T2DM`. Implementation starts
from main `f1f40e3c7b645d68c08f7325bae2b154942ba8ca`; frozen paper identity remains
`faa5799fa01d8d7381ea43415fbec01036d1e4ff`, tag `v1.0.0-paper`.

| Question | Inspected source and finding | Demo decision |
| --- | --- | --- |
| Executable artifacts? | Tracked-file inventory and `PUBLIC_RELEASE_LIMITATIONS.md`/README: fitted models, preprocessors, calibrators and individual predictions excluded. | Results-driven mode; disabled prediction, no patient score or replacement fit. No private archive data copied. |
| Cohort targets/fields? | `config/datasets.yaml`, `src/diabetes_pipeline/data/loaders.py` | Separate endpoints, exact native fields and post-loader synthetic fixtures. No raw-data importer or cross-cohort transformations. |
| Availability? | `config/availability_scenarios.yaml`, `analysis/journal_revision/PANEL_DEFINITIONS.csv`, `routing/inference.py:route_patient` | All 22 supported panels. The preflight mirrors only eligibility and deterministic max `(size, is_full, name)`. Explicit missing requests and unsupported auto requests abstain. Parity tests use the unchanged inference function. |
| Fitted preprocessing? | `preprocessing/builders.py:build_preprocessor` | Display its documented contract; never create approximate medians, vocabularies or transformed vectors. |
| Model/calibration selection? | `routing/evaluator.py`, `calibration/calibrators.py:select_calibrator`, final protocol | No fitted family/map can be reconstructed from aggregate rankings. Saved selection rows remain fold/development results. No raw or calibrated sample probability is supplied. |
| Decision policy? | Router bundles exported by `routing/evaluator.py` contain fixed 0.5/fixed_0_5. | Describe original policy only; no individualized classification. Do not use separate descriptive thresholds as live defaults. |
| Confidence abstention? | `evaluation/selective_prediction.py:_accepted_mask`, `selective_prediction_analysis`; `03_SELECTIVE_PREDICTION.csv` separates exclusions. | Present saved coverage-ranked/group-retaining evaluation with observation/event coverage and excluded prevalence. Do not invent a single-case confidence cutoff. |
| Results? | `publication_release/RESULT_TO_SOURCE_MAP.md`, final tables and journal revision aggregates | Twelve distinct experiment views; exact source strings/downloads, no blank-to-zero filling, no cross-endpoint summaries. Forced stress and natural runtime are separate. |
| Scientific interpretation? | Final summary and runtime contrasts | Preserve mixed/negative switching results, internal-validation limits, conditional fitted-prediction uncertainty, non-causal explanations and absence of clinical-benefit evidence. |
| Frozen boundary? | Existing `.github/ci/verify_current_documentation.py` and CI | Extend only its explicit mutable-path list for the demo and new workflow. Preserve all 396 protected frozen files and the original frozen CI job. |

The demo's dependency lock is independent of the scientific environment. Its
SHA-256 manifest is an additional input-integrity check, not a reseal or new
scientific release. A standalone offline HTML export reproduces these aggregate
views and synthetic availability examples, not a recorded model prediction.
