> **Historical pre-publication report — notice added 29 October 2026.** The original preparation text below is retained verbatim. Hosting, rename, tag and DOI statements describe the preparation state and are superseded by [current RELEASE_STATUS.md](RELEASE_STATUS.md): the public software release is `v1.0.0-paper`, commit `faa5799fa01d8d7381ea43415fbec01036d1e4ff`, version DOI [10.5281/zenodo.23537932](https://doi.org/10.5281/zenodo.23537932). This notice does not establish later author consent, institutional approval or journal acceptance. The frozen tag and Zenodo archive retain the original file bytes.

# Independent clean-snapshot verification — 21 October 2026

**PASS_WITH_LIMITATIONS. Local preparation only; no public release, tag or DOI.** An independently copied snapshot without `.git`, raw data, research outputs or model objects was installed in a new environment. This is a fresh-copy test of the proposed payload, not a clone of a public release that does not yet exist. CPython 3.12.0 / macOS 27.0.1 arm64; all 48 locked distributions installed successfully. The lock pins versions rather than wheel hashes. Other operating systems were not tested here.

| Command or check | Actual result | Status |
| --- | --- | --- |
| New environment, `python -m pip install -r requirements.lock`, editable package install | 48 locked distributions; installation and imports successful | PASS |
| `python scripts/verify_environment.py` | Python 3.12.0 and all 48 locked versions agree | PASS |
| `python -m pytest -q -m "not local_research_data"` | **161 passed, 7 subtests passed, 7 deselected, 3 warnings; 60.42 seconds** | PASS_WITH_LIMITATIONS |
| `python scripts/verify_publication_results.py` | **85/85** retained publication files and **14/14** correction files match their fingerprints | PASS |
| `python publication_release/verify_public_aggregates.py` | **47** curated tables; **216** saved point/Holm contrasts; **2,192** repeat mean/SD cells; **4** routing cohorts; **40** selective rows | PASS |
| `python publication_release/verify_manuscript_sources.py` | **1,988** cells across **25** sources: 545 main and 1,443 supplementary; exact source strings/rounding | PASS_WITH_LIMITATIONS |
| `python publication_release/verify_snapshot.py` | Complete included-file/hash coverage; 37 inherited test files and 78 scientific source files unchanged; all 24 held originals absent | PASS |
| `python scripts/finalize_journal_handoff.py reconstruct --destination outputs/reviewer-tables` | **47** CSV views, **11** rounded Markdown tables, **12,350** source rows; all 47 CSVs byte-identical to the candidate's curated targets | PASS |
| `python publication_release/paper_evidence/REGENERATE_FIGURES.py outputs/reviewer-figures` | Three PNG/PDF pairs generated; **all three paper PNGs byte-identical** to recovered manuscript artwork | PASS |
| `python -m diabetes_pipeline.cli --help` | Imports and help entry point successful | PASS |
| Gitleaks 8.30.1 plus filename/content/container/visual metadata screening | 16 scanner alerts, all independently verified SHA-256 checksum mappings; no identified credential or patient-level payload | PASS_WITH_LIMITATIONS |
| Separately acquired provider datasets / cohort recounts | Not downloaded into this fresh copy. Previous independent PIDD/Sylhet/Hospital130 download/count evidence is distinguished from this test; BRFSS returned HTTP 403 | BLOCKED for the complete current four-cohort download pathway |
| Prediction-derived metrics, bootstrap P values/CIs and original split/event counts | Private predictions, split memberships and bootstrap arrays absent | BLOCKED for independent raw reanalysis |
| Exact historical training replay | Original complete historical source fingerprint unavailable | BLOCKED |
| Historical component timing reconstruction | Several original components were not separately recorded | PARTIAL |
| A4 computational-cost reporting | Aggregate summaries and methods retained; no new measurement or fitting | COMPLETE reporting |

The 161 tests comprise the 158 inherited portable tests and three added public-snapshot checks. Every inherited test file and its tolerances is unchanged. The seven omitted tests explicitly require local research data. Three warnings are upstream SHAP/matplotlib pending-deprecation warnings. Some unit tests fit tiny synthetic fixtures; no study model was trained, tuned or rebenchmarked.

The statistical-verification CSV is a separately named public projection of 220 rows with only the private `source` column removed. Retained cell strings are unchanged. All other curated CSV bytes retain their baseline identity. The public seal certifies 85 retained artifacts, not all 101 members of the original research export; 16 metadata-bearing originals are excluded and explicitly inventoried.

The scalar ledger checks do not independently verify every manuscript prose statement, PDF cell placement or raw-data estimand. Saved raw P columns support checking Holm arithmetic; absent bootstrap samples prevent recomputing those raw P values. Rebuilding figures from saved bins/curves does not regenerate the bins/curves from individuals. PDF byte identity is not claimed because creation metadata may vary. Public reanalysis beyond these boundaries has not been demonstrated.

[VERIFICATION_EVIDENCE.json](VERIFICATION_EVIDENCE.json) records actual command exit codes, local log fingerprints, expected/actual table and PNG hashes. Raw logs containing local environment paths remain outside the public payload. [PUBLIC_EXPOSURE_AUDIT.md](PUBLIC_EXPOSURE_AUDIT.md) records privacy scope and limits. The complete manifest and its sidecar are rechecked after final documentation changes; their final receipt is stored outside this snapshot to avoid a self-referential hash.
