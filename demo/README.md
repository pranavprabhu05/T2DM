# T2DM research demonstrator

An interactive Streamlit example/availability explorer and saved-results viewer for
the existing T2DM research. **This public checkout has no executable fitted models,
preprocessing/calibration objects or individual predictions. Live prediction is
unavailable.** The demo never trains a substitute model or assigns a probability,
outcome, risk category or clinical recommendation to an example.

## Run locally

Use a separate environment from the scientific pipeline. Streamlit 1.51 requires
pandas <3, while the frozen research lock uses pandas 3.0.5; combining them would
change the research environment. The standalone demo only needs its own lock and
CPython 3.12.x; it does not require `pip install -e .`, raw data or tree libraries.

From the repository root on the branch containing `demo/`:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r demo/requirements.lock
python -m pip check
python -m pytest -q demo/tests
python -m streamlit run demo/app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Open `http://127.0.0.1:8501`. Stop with Ctrl+C. The process binds to this laptop;
the app makes no external data/model calls. Initial package installation needs
internet. All examples are synthetic; do not enter real patient data. Inputs stay
in session memory unless the user downloads the example JSON. Run from the
repository root so Streamlit loads the included light theme and local settings.

## What to demonstrate

1. Select a cohort. Its target and evaluation boundary appear explicitly.
2. In **Example explorer**, select **All fields observed**, then **Smallest
   documented panel**. Change observed flags or encoded values. The automatic
   policy chooses the largest fully supported native panel using the original
   deterministic tie-break. An explicit panel request abstains if any required
   field is absent. Changing values cannot change saved cohort-level metrics.
3. Select **Insufficient fields → abstention**. Explain this is *availability*
   abstention, and that the disabled Predict button reflects missing artifacts.
4. In **Experiments & results**, inspect runtime coverage, full-schema benchmark,
   forced masks and selective prediction. Use only saved nominal coverage levels;
   read positive-event coverage and excluded prevalence alongside accepted scores.
5. Open switching comparisons. Retain the mixed/negative finding: the router did
   not establish consistent Holm-corrected superiority over a robust fixed family.

An arbitrary set of two fields is not necessarily a supported panel. Full-schema
masked-input experiments and separately refitted reduced-schema experiments are
different saved estimands. The explorer shows feature eligibility only, not the
unavailable fitted family/mapping selection.

## Cohort and input boundaries

| Cohort | Target | Example encoding / evaluation boundary |
| --- | --- | --- |
| PIDD | Recorded diabetes-positive label | Eight numeric fields; loader-defined implausible zeros become missing. Pregnancy zero stays observed. Repeated nested internal validation. |
| Sylhet | Early-stage diabetes-positive label | Loader-encoded binary symptoms and gender, numeric age. Identical feature profiles remain grouped in repeated nested evaluation. |
| BRFSS 2015 | Self-reported diagnosed diabetes | Already recoded survey fields; Age is category 1–13, not years. Borderline/pregnancy-only target responses are excluded. Historical internal evaluation partition. |
| Hospital130 | Readmission within 30 days | Age is decade code 0–9; diagnoses already collapsed; admission/discharge/source identifiers are categories. Patient-grouped internal evaluation; inapplicable death/hospice discharges excluded. |

Fixtures are hand-authored, valid **post-loader, pre-fitted-preprocessing** schema
examples. They have no observed outcomes and are not real held-out cases. They do
not imitate raw CDC/UCI records. `None` in a category string such as A1Cresult is
observed; an unchecked Observed box is unavailable. Numeric inputs marked
observed must be finite; blank cells and invalid encodings are reported. No imputation or
fitted transformation is approximated by the demo. All 22 native panels come
directly from `config/availability_scenarios.yaml`.

The original training pipeline fits medians/missingness indicators, LR-only scaling
and training-only categorical one-hot vocabularies within training boundaries.
Calibration choices use cross-fitted training probabilities and Brier/log-loss
selection (identity eligible; isotonic requires 1,000 samples). Its router uses
the fitted panel map and fixed 0.5 threshold. The saved selective analysis instead
ranks evaluation cases by `2 * abs(p_calibrated - 0.5)`, retaining groups together
when present. It is not a validated deployable confidence threshold for a new
sample. Neither policy establishes clinical benefit.

## Offline panel fallback

Prepare and rehearse on the actual presentation laptop while online:

```bash
python -m demo.export_offline --output outputs/panel-demo.html
```

Open that HTML file directly in a browser, then disconnect from the internet and
rehearse. It contains all 12 saved experiment views, cohort selectors and a
synthetic feature-availability explorer; **no CDN, server, Python or network is
needed to open it**. It deliberately retains the same missing-inference boundary.
The export is deterministic, records verified source identity, and refuses to
overwrite an existing file; choose a new output filename when regenerating.

The installed Streamlit app also runs offline. For offline *installation* on the
same OS, architecture and CPython 3.12 platform, prepare a wheelhouse beforehand:

```bash
python -m pip download --only-binary=:all: -r demo/requirements.lock -d outputs/demo-wheels
python -m pip install --no-index --find-links outputs/demo-wheels -r demo/requirements.lock
```

Copy the checkout, wheelhouse and HTML to the presentation laptop; test there
before the panel. The lock is a tested macOS arm64 resolution; Linux is checked
in CI. Wheel availability and native runtimes on other platforms require a local
installation check. A short screen recording of a rehearsed run is an optional
additional backup; none is fabricated or included as a recorded live prediction.

## Reproducibility and validation

`demo/source_manifest.json` pins SHA-256 values for every displayed numerical
source, the cohort/panel/protocol definitions, relevant original implementation
files and the synthetic fixtures. Research inputs were checked byte-for-byte
against `v1.0.0-paper` (`faa5799fa01d8d7381ea43415fbec01036d1e4ff`). Checks run on every
Streamlit rerun and before HTML export; missing or changed sources stop display.
This verifies the retained evidence, not private predictions or exact training
replay. The original manifest, tag, release and Zenodo archive are unchanged.

Tests check all cohorts/panels, seeded availability masks against the unchanged
`route_patient` implementation, PIDD zeros/encoded inputs, exact saved string
projections, corruption rejection, deterministic offline export, abstention and
Streamlit navigation through every cohort and experiment. Test doubles exist
only in the parity test; they are never loaded by the app.

```bash
python -m pytest -q demo/tests
python -m unittest discover -s .github/ci -p 'test_current_documentation.py' -v
python .github/ci/verify_current_documentation.py
python scripts/verify_publication_results.py
python publication_release/verify_public_aggregates.py
python publication_release/verify_manuscript_sources.py
```

Complete frozen-snapshot/portable-suite checks still run against the pinned release
in the existing CI job. Do not regenerate its manifest to incorporate the demo.
The current-branch guard allows the individual reviewed demo paths explicitly;
all inherited scientific code, tests, configuration and evidence remain protected.
See [the repository audit](AUDIT.md) for the implementation/source decisions.

## Enabling live inference later

There is intentionally no pickle upload, automatic artifact discovery, training
button, arbitrary fold chooser or guessed export/retraining procedure. The public
release cannot establish exact historical training replay. An approved artifact
handoff would need cohort-specific fitted preprocessors/models/calibrators and
their hashes/environment, exact feature/target contracts, fold/repeat provenance
and validated aggregation, frozen routing/threshold semantics, and reference
input/output cases. Its ownership and redistribution terms must be checked before
adding it to a public demo. A subsequent adapter should call the original
`route_patient` only under that validated contract. Selecting a convenient fold
or fitting a new example model would not reproduce the reported evaluation.

Research source: [T2DM](https://github.com/pranavprabhu05/T2DM), frozen
[v1.0.0-paper](https://github.com/pranavprabhu05/T2DM/releases/tag/v1.0.0-paper),
[version DOI 10.5281/zenodo.23537932](https://doi.org/10.5281/zenodo.23537932).
Streamlit UI tests follow the official
[AppTest API](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).
