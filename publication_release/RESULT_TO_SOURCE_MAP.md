# Frozen paper-release result-to-source map

**Hosting-status correction, 29 October 2026.** This map describes the frozen software/evidence release, not current manuscript readiness. [v1.0.0-paper](https://github.com/pranavprabhu05/T2DM/releases/tag/v1.0.0-paper), commit `faa5799fa01d8d7381ea43415fbec01036d1e4ff`, is publicly archived at version DOI [10.5281/zenodo.23537932](https://doi.org/10.5281/zenodo.23537932). The source mappings and numerical evidence below are unchanged.

The recovered 16 October package has a 28-page manuscript, 52-page ESM 1 with S1–S15, and a 118-member ESM 2. It matches the requested full title and revision topics. The older S11-ending package is superseded for this map. Exact identities are in `MANUSCRIPT_SOURCE_VERIFICATION.md`; no manuscript was edited.

104 ESM 2 members with repository counterparts were compared byte for byte; all 104 match the verified baseline. The recovered numeric ledgers contain 545 main-source and 1,443 supplementary-source cells. An independent checker matched all 1,988 source strings/rounding rules to 25 aggregate sources and confirmed display presence in the recovered TeX/macros. This is not a guarantee about every prose number, PDF placement or scientific inference. The comparator ledger omits batch_n in 32 cell keys; its explicit preceding batch_n cell disambiguates the row, and the retained ledger is unchanged.

## Tested entry points and what they do

Run from the published `v1.0.0-paper` snapshot root in the documented CPython 3.12 environment; follow [REPRODUCIBILITY.md](../REPRODUCIBILITY.md) to select the frozen checkout. The metadata-bearing original statistical-verification CSV is excluded; its separately named PUBLIC projection removes only the private source-path column and preserves all retained cell strings. The source index/curation adapter identifies that derivative explicitly.

| Code | Executable command | Expected output / dependencies / evidence tier |
| --- | --- | --- |
| V | `python scripts/verify_publication_results.py` and `python publication_release/verify_public_aggregates.py` | Console verification: 85 retained publication + 14 correction fingerprints; 47 exact curated views; 216 point/Holm contrasts; repeat/routing/selective arithmetic. Standard library for these checks. No patient data, fit or new bootstrap |
| M | `python publication_release/verify_manuscript_sources.py` | Console: 545 main + 1,443 supplementary scalar source/rounding checks. Reads the retained ledgers and tracked aggregate CSVs. No manuscript file needed; actual TeX display-presence check additionally accepts `--manuscript-dir` supplied locally |
| E | `python scripts/finalize_journal_handoff.py reconstruct --destination outputs/reviewer-tables` | 47 CSVs + 11 Markdown views under an empty output directory. Requires installed package/numpy/pandas and tracked sources; no private data or fitting. This reconstructs curated aggregate views, not the complete typeset PDF layouts |
| F | `python publication_release/paper_evidence/REGENERATE_FIGURES.py outputs/reviewer-figures` | Three paper PNG/PDF figures from tracked aggregate plot data/forced-panel CSV; matplotlib only, no private predictions or fitting. All three PNGs reproduced byte-identically in the isolated environment |
| C | `python publication_release/verify_cohort_counts.py --dataset pidd` (also sylhet/hospital130) | Independently recount eligible rows/events/predictors from separately downloaded, hash-verified raw data. No record-level output or fit. BRFSS requires its blocked CDC download; split membership is not reconstructed |

For every item below, **saved aggregate verification is public-input-capable in the published release**. **Complete numerical reanalysis is not independently established from public inputs**: raw records, matching historical splits/predictions/models/calibrators and bootstrap distributions are absent or nonredistributed, and the exact historical source tree is missing. The commands verify or curate frozen evidence; none reruns model fitting. Required provider sources for any future raw-data work are OpenML 37 (PIDD), UCI 529 (Sylhet), UCI 296 (Hospital130), and CDC BRFSS 2015, with exact URLs/hashes in `config/data_sources.yaml`. Historical download status and platform limits are recorded in `FRESH_CLONE_VERIFICATION.md`; the current reproduction guide distinguishes that report from later release CI.

## Main manuscript tables

| Table | Reported quantity | Authoritative numerical source (repository-relative) | Estimand / dependence boundary | Entry points |
| --- | --- | --- | --- | --- |
| 1 | Cohort populations / endpoints / event counts | results/final_publication/tables/dataset_characteristics.csv; publication_release/paper_evidence/analysis_population_counts.csv; results/final_publication/tables/routing_fallback_performance.csv | Eligible totals versus evaluation/accepted totals; do not substitute eligible prevalence for evaluation prevalence | V+M+C |
| 2–5 | Exact PIDD, Sylhet, BRFSS, Hospital130 feature panels | analysis/journal_revision/PANEL_DEFINITIONS.csv; config/availability_scenarios.yaml | Dataset-native field lists and counts, largest supported panel; no cross-cohort harmonization | V+M+E |
| 6 | Accepted runtime fallback with uncertainty | results/final_publication/tables/routing_fallback_performance.csv; publication_release/paper_evidence/runtime_intervals/{pidd,sylhet,brfss,hospital130}.csv | Original runtime policy point estimates and intervals; seed 1600042; accepted-case metrics and total/event coverage | V+M+E |
| 7 | Selected forced-panel stress | results/final_publication/tables/availability_panel_degradation.csv; results/final_publication/tables/availability_panel_confidence_intervals.csv | Forced masks with original fits; repeated participant-mean probabilities; fixed-cohort intervals not invented | V+M+E |
| 8 | Router minus robust fixed statistical contrasts | analysis/journal_revision/07_RUNTIME_PAIRED_COMPARISONS.csv; analysis/journal_revision/manuscript_handoff/03_MAIN_TEXT_TABLES/08_main_statistical_comparisons.csv | Three original policy contrasts per cohort/metric Holm family; mixed/negative switching result | V+M+E |
| 9 | Selective prediction near 70% coverage | analysis/journal_revision/03_SELECTIVE_PREDICTION.csv; analysis/journal_revision/manuscript_handoff/03_MAIN_TEXT_TABLES/06_selective_prediction.csv | Actual observation/event coverage and accepted-case metrics; availability versus confidence exclusions distinct | V+M+E |
| 10–11 | Reduced-schema versus masked-input AUROC | analysis/journal_revision/04_RETRAINED_PANEL_COMPARISON.csv; analysis/journal_revision/04_PANEL_PAIRED_CONTRASTS.csv | Matched family/full-schema hyperparameters; training-only refits already completed; these commands do not refit | V+M+E |
| 12 | Calibration/switching A/B/C/D | analysis/journal_revision/05_CALIBRATION_SWITCHING_ABLATION.csv; analysis/journal_revision/05_ABLATION_PAIRED_CONTRASTS.csv | Full-schema versus panel mapping, identity eligible; five-contrast Holm family distinct from original Table S9 | V+M+E |
| 13 | Natural runtime routing | analysis/journal_revision/02_ROUTING_DISTRIBUTION.csv | Unique evaluation panel/event counts versus per-repeat family/mapping counts | V+M+E |
| 14 | Repeat sensitivity / primary estimand | analysis/journal_revision/01_PER_REPEAT_SENSITIVITY.csv | Five dependent repeat means/sample SD versus metrics of averaged probabilities; SD is descriptive | V+M+E |
| 15 | Computational-cost summary | analysis/journal_revision/A4_MAIN_TEXT_TABLE.csv; analysis/journal_revision/A4_INFERENCE_SUMMARY.csv; analysis/journal_revision/A4_COMPONENT_STORAGE_VERIFICATION.csv | Successor fit/calibration sums, warmed original-router call latency, independent exemplar serialization sizes | V+M+E |

## Supplementary tables S1–S15

These are semantic S-table sections in ESM 1; some span multiple physical LaTeX tables. They are not the older package's S11 survey-sensitivity numbering.

| Table | Reported quantity | Authoritative numerical source (repository-relative) | Interpretation / unavailable reconstruction input | Entry points |
| --- | --- | --- | --- | --- |
| S1 | Exact feature-panel definitions | analysis/journal_revision/PANEL_DEFINITIONS.csv; config/availability_scenarios.yaml | Native fields and eligibility; parameter/configuration tables also retained | V+M+E |
| S2 | Populations, predictors and flow | results/final_publication/tables/dataset_characteristics.csv; publication_release/paper_evidence/analysis_population_counts.csv; publication_release/paper_evidence/predictor_characteristics.csv; publication_release/paper_evidence/predictor_missingness.csv | Eligible counts, split/fold aggregate counts, coding/missingness. Three eligible cohorts independently recounted; split identities remain private | V+M+C |
| S3 | Full-schema five-family benchmark | results/final_publication/tables/full_panel_model_performance.csv; results/final_publication/tables/model_performance_confidence_intervals.csv; results/final_publication/tables/model_paired_comparisons.csv | Original calibrated benchmark; cohort-specific probability aggregation/uncertainty | V+M+E |
| S4 | All forced-panel stress configurations | results/final_publication/tables/availability_panel_degradation.csv; results/final_publication/tables/availability_panel_confidence_intervals.csv; results/final_publication/tables/repeated_panel_all_system_performance.csv | Corrected repeated stress, unchanged fixed-cohort points | V+M+E |
| S5 | Threshold reporting | results/final_publication/tables/threshold_performance.csv; results/final_publication/tables/threshold_metrics.csv; results/final_publication/tables/descriptive_threshold_confidence_intervals.csv | Fixed 0.5 operating metrics versus descriptive fold-selected thresholds | V+M |
| S6 | Runtime probability diagnostics / calibration selections | results/final_publication/tables/routing_fallback_performance.csv; results/final_publication/tables/calibration_selection.csv; publication_release/paper_evidence/runtime_intervals/ | Runtime accepted population; mapping choices remain training/development-derived | V+M+E |
| S7 | All-target selective prediction | analysis/journal_revision/03_SELECTIVE_PREDICTION.csv; results/final_publication/tables/selective_prediction_metrics.csv; results/final_publication/tables/selective_prediction_confidence_intervals.csv | Observation/event coverage, accepted/rejected prevalence, separate exclusion types | V+M+E |
| S8 | Subgroup inventory / estimates | results/final_publication/tables/subgroup_metrics.csv; results/final_publication/tables/subgroup_confidence_intervals.csv | Aggregate strata and estimability statuses; no subgroup membership records released | V |
| S9 | All original runtime paired contrasts | analysis/journal_revision/07_RUNTIME_PAIRED_COMPARISONS.csv; results/final_publication/tables/statistical_comparisons.csv | Three policy contrasts per cohort/metric; conditional fitted-prediction bootstrap; raw draws remain private | V+M+E |
| S10 | SHAP ranks | results/final_publication/tables/shap_summary.csv | Saved model-specific aggregate ranks; individual SHAP values/models are private; no causal claim | V+M |
| S11 | Reduced-schema effects for all probability metrics | analysis/journal_revision/04_RETRAINED_PANEL_COMPARISON.csv; analysis/journal_revision/04_PANEL_PAIRED_CONTRASTS.csv | AUROC/AP/Brier/log loss; negative/inconclusive rows and full identity controls retained | V+M+E |
| S12 | Calibration/switching effects | analysis/journal_revision/05_CALIBRATION_SWITCHING_ABLATION.csv; analysis/journal_revision/05_ABLATION_PAIRED_CONTRASTS.csv | A/B/C/D points and five contrasts/cohort/metric; not the original three-policy family | V+M+E |
| S13 | Routing panel/family/mapping distributions | analysis/journal_revision/02_ROUTING_DISTRIBUTION.csv | Unique panel totals and per-repeat mapping assignments; do not sum repeated counts as people | V+E |
| S14 | Individual repeat sensitivity | analysis/journal_revision/01_PER_REPEAT_SENSITIVITY.csv | Five repeats, benchmark/panel/runtime configurations, primary versus mean-repeat estimands | V+M+E |
| S15 | Computational methods, distributions and costs | analysis/journal_revision/A4_*.csv; analysis/journal_revision/06_COMPUTATIONAL_COST.csv; analysis/journal_revision/A4_PUBLICATION_READY_SUMMARY.md | Saved sums/latency/storage distributions and matched A/D workloads; original timing gaps remain | V+M+E |

## Current paper figures

| Figure | Number represented | Authoritative input | Script / expected output | Public check versus reanalysis |
| --- | --- | --- | --- | --- |
| 1 | Accepted-runtime decile mean probability/event rate in separate cohort panels | `results/final_publication/figure/data/panel_a_calibration.csv`, exact copied input in `paper_evidence/figure_data/` | F; `outputs/reviewer-figures/Figure_1_Calibration.{png,pdf}` | Drawing from saved bins PASS; recreating bins from individuals BLOCKED |
| 2 | Endpoint-specific runtime/treat-all/treat-none net benefit over saved thresholds | `results/final_publication/figure/data/panel_b_decision_curves.csv`, exact copied input in `paper_evidence/figure_data/` | F; `outputs/reviewer-figures/Figure_2_Decision_Curves.{png,pdf}` | Drawing from saved aggregate curves PASS; independent prediction-derived utility/uncertainty BLOCKED |
| 3 | Full-minus-forced-panel AP against percentage of full-schema predictor count | `results/final_publication/tables/availability_panel_degradation.csv`, exact copy in `paper_evidence/04_SUPPLEMENTARY_TABLES/` | F; `outputs/reviewer-figures/Figure_3_Availability.{png,pdf}` | Drawing from saved aggregate values PASS; independent metric reanalysis BLOCKED |

The older consolidated figure and three plot-data CSVs remain frozen/hash-verified. The original prediction-consuming renderer is not the current public drawing entry point. Paper PDF byte identity may vary with embedded creation dates; all three tested PNG bytes exactly match the recovered paper artwork. No new scientific estimates or plot data were calculated.

## Additional complete aggregate evidence

BRFSS survey-weighted sensitivity, decision-curve intervals/contrasts, all benchmark paired comparisons, calibration choices, detailed cost/storage tables, PIDD forced-versus-runtime estimands and statistical reconstruction records remain identifiable under `results/final_publication/tables/` and `analysis/journal_revision/`. Their presence is not a claim that every row appears in the selected main/ESM display. Missing bootstrap arrays prevent a public independent recomputation of raw paired P values/CIs, although adjusted values can be checked from the retained raw P columns.

## Every curated table and exact source

The index below is generated from the public `TABLE_SOURCE_INDEX.json` (one entry explicitly identifies the metadata-only statistical projection); it preserves source identities, exact row selections and precision. E reconstructs all 47, including the 11 rounded Markdown views. M supplies the paper-specific scalar projection/rounding checks; S sections with additional frozen-only tables use the V fingerprint checks.

| Curated path under manuscript_handoff | Exact source CSV | Rows | Method |
| --- | --- | --- | --- |
| `03_MAIN_TEXT_TABLES/01_reduced_schema.csv` | `analysis/journal_revision/04_RETRAINED_PANEL_COMPARISON.csv` | 36 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/01_reduced_schema_effects.csv` | `analysis/journal_revision/04_PANEL_PAIRED_CONTRASTS.csv` | 72 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/02_fixed_imputation.csv` | `analysis/journal_revision/05_CALIBRATION_SWITCHING_ABLATION.csv` | 8 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/02_fixed_imputation_effects.csv` | `analysis/journal_revision/05_ABLATION_PAIRED_CONTRASTS.csv` | 16 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/03_calibration_switching.csv` | `analysis/journal_revision/05_CALIBRATION_SWITCHING_ABLATION.csv` | 16 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/04_routing.csv` | `analysis/journal_revision/02_ROUTING_DISTRIBUTION.csv` | 13 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/05_per_repeat.csv` | `analysis/journal_revision/01_PER_REPEAT_SENSITIVITY.csv` | 6 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/06_selective_prediction.csv` | `analysis/journal_revision/03_SELECTIVE_PREDICTION.csv` | 4 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/07_computational_cost.csv` | `analysis/journal_revision/A4_MAIN_TEXT_TABLE.csv` | 4 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/08_main_statistical_comparisons.csv` | `analysis/journal_revision/07_RUNTIME_PAIRED_COMPARISONS.csv` | 16 | exact source-string projection |
| `03_MAIN_TEXT_TABLES/09_pidd_estimands.csv` | `analysis/journal_revision/07_PIDD_ESTIMANDS.csv` | 2 | exact source-string projection |
| `04_SUPPLEMENTARY_TABLES/01_PER_REPEAT_SENSITIVITY.csv` | `analysis/journal_revision/01_PER_REPEAT_SENSITIVITY.csv` | 2466 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/02_ROUTING_DISTRIBUTION.csv` | `analysis/journal_revision/02_ROUTING_DISTRIBUTION.csv` | 300 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/03_SELECTIVE_PREDICTION.csv` | `analysis/journal_revision/03_SELECTIVE_PREDICTION.csv` | 40 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/04_RETRAINED_PANEL_COMPARISON.csv` | `analysis/journal_revision/04_RETRAINED_PANEL_COMPARISON.csv` | 44 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/04_PANEL_PAIRED_CONTRASTS.csv` | `analysis/journal_revision/04_PANEL_PAIRED_CONTRASTS.csv` | 88 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/05_CALIBRATION_SWITCHING_ABLATION.csv` | `analysis/journal_revision/05_CALIBRATION_SWITCHING_ABLATION.csv` | 16 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/05_ABLATION_PAIRED_CONTRASTS.csv` | `analysis/journal_revision/05_ABLATION_PAIRED_CONTRASTS.csv` | 80 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/07_PIDD_ESTIMANDS.csv` | `analysis/journal_revision/07_PIDD_ESTIMANDS.csv` | 8 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/07_RUNTIME_PAIRED_COMPARISONS.csv` | `analysis/journal_revision/07_RUNTIME_PAIRED_COMPARISONS.csv` | 48 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/07_STATISTICAL_VERIFICATION_PUBLIC.csv` | `analysis/journal_revision/07_STATISTICAL_VERIFICATION_PUBLIC.csv` | 220 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/PANEL_DEFINITIONS.csv` | `analysis/journal_revision/PANEL_DEFINITIONS.csv` | 22 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/BASE_MODEL_CONFIGURATIONS.csv` | `analysis/journal_revision/BASE_MODEL_CONFIGURATIONS.csv` | 260 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/MODEL_CONFIGURATIONS.csv` | `analysis/journal_revision/MODEL_CONFIGURATIONS.csv` | 1144 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/PANEL_TASK_MANIFEST.csv` | `analysis/journal_revision/PANEL_TASK_MANIFEST.csv` | 286 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/PANEL_FINDING_COUNTS.csv` | `analysis/journal_revision/PANEL_FINDING_COUNTS.csv` | 16 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/06_COMPUTATIONAL_COST.csv` | `analysis/journal_revision/06_COMPUTATIONAL_COST.csv` | 2670 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_MAIN_TEXT_TABLE.csv` | `analysis/journal_revision/A4_MAIN_TEXT_TABLE.csv` | 4 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_INFERENCE_SUMMARY.csv` | `analysis/journal_revision/A4_INFERENCE_SUMMARY.csv` | 74 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_TRAINING_SUMMARY.csv` | `analysis/journal_revision/A4_TRAINING_SUMMARY.csv` | 20 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_HISTORICAL_MODEL_COSTS.csv` | `analysis/journal_revision/A4_HISTORICAL_MODEL_COSTS.csv` | 40 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_HISTORICAL_TIMING.csv` | `analysis/journal_revision/A4_HISTORICAL_TIMING.csv` | 4 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_HISTORICAL_TRIAL_TIMING.csv` | `analysis/journal_revision/A4_HISTORICAL_TRIAL_TIMING.csv` | 260 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_STORAGE_DETAILS.csv` | `analysis/journal_revision/A4_STORAGE_DETAILS.csv` | 848 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_STORAGE_VERIFICATION.csv` | `analysis/journal_revision/A4_STORAGE_VERIFICATION.csv` | 4 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_COMPONENT_STORAGE_VERIFICATION.csv` | `analysis/journal_revision/A4_COMPONENT_STORAGE_VERIFICATION.csv` | 16 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/A4_COMPARATOR_COSTS.csv` | `analysis/journal_revision/A4_COMPARATOR_COSTS.csv` | 8 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_dataset_characteristics.csv` | `results/final_publication/tables/dataset_characteristics.csv` | 4 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_full_panel_model_performance.csv` | `results/final_publication/tables/full_panel_model_performance.csv` | 20 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_model_performance_confidence_intervals.csv` | `results/final_publication/tables/model_performance_confidence_intervals.csv` | 1380 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_model_paired_comparisons.csv` | `results/final_publication/tables/model_paired_comparisons.csv` | 160 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_calibration_selection.csv` | `results/final_publication/tables/calibration_selection.csv` | 780 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_repeated_panel_all_system_performance.csv` | `results/final_publication/tables/repeated_panel_all_system_performance.csv` | 77 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_availability_panel_confidence_intervals.csv` | `results/final_publication/tables/availability_panel_confidence_intervals.csv` | 396 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_availability_panel_degradation.csv` | `results/final_publication/tables/availability_panel_degradation.csv` | 22 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_routing_fallback_performance.csv` | `results/final_publication/tables/routing_fallback_performance.csv` | 12 | byte-identical aggregate source copy |
| `04_SUPPLEMENTARY_TABLES/frozen_selective_prediction_confidence_intervals.csv` | `results/final_publication/tables/selective_prediction_confidence_intervals.csv` | 320 | byte-identical aggregate source copy |
