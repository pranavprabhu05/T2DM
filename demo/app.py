"""Run from the repository root: python -m streamlit run demo/app.py."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from demo.core import (COHORTS, FROZEN_COMMIT, ROOT, TABLES, EvidenceError,
                       availability_report, contracts, example_sample, fixtures,
                       load_table, normalize_sample, verify_sources)

st.set_page_config(page_title="T2DM · Research demo", page_icon="◈", layout="wide")
st.markdown("""<style>
    .stApp {background: #f7f9fc;}
    .block-container {max-width: 1280px; padding-top: 5rem; padding-bottom: 3rem;}
    h1,h2,h3 {color: #122c48; letter-spacing: -.025em;}
    h1 {font-size: 2.4rem; line-height: 1.15;}
    [data-testid="stMetric"] {background:white; border:1px solid #dce4ef;
      border-radius:12px; padding:16px;}
    [data-testid="stSidebar"] {background:#edf2f8;}
    .eyebrow {color:#17685d; font-size:.78rem; font-weight:700; letter-spacing:.15em;}
    .boundary {border-left:4px solid #187b70; background:#eaf4f1;
      padding:14px 18px; border-radius:4px; margin-bottom:20px; color:#173f38;}
</style>""", unsafe_allow_html=True)

try:
    # Verify on every rerun; cached verification could hide an evidence edit.
    manifest = verify_sources()
    configs, availability = contracts()
except (EvidenceError, OSError, ValueError, KeyError) as exc:
    st.error(f"Evidence unavailable: {exc}")
    st.info("Restore the reviewed checkout and restart. Results are hidden until the source checks pass.")
    st.stop()

with st.sidebar:
    st.markdown("### ◈ T2DM")
    st.caption("Availability-aware research")
    cohort = st.selectbox("Cohort", COHORTS, format_func=lambda c: {
        "pidd": "PIDD", "sylhet": "Sylhet", "brfss": "BRFSS 2015", "hospital130": "Hospital130"}[c], key="cohort")
    page = st.radio("View", ["Example explorer", "Experiments & results", "Reproducibility"], key="page")
    st.divider()
    st.markdown("**Evidence mode**\n\nSaved aggregates + synthetic examples")
    st.caption("Live inference unavailable · model and calibration objects are absent from this public release.")
    st.caption("Research demonstration only. Internal validation; no clinical use or prospective validity established.")

cfg = configs[cohort]
st.markdown('<div class="eyebrow">RESEARCH DEMONSTRATOR / FROZEN EVIDENCE</div>', unsafe_allow_html=True)
st.title("Feature availability in practice")
st.markdown(f"**{cfg['display_name']}** · `{cfg['endpoint']}`")
st.markdown('<div class="boundary">Four separate cohort tasks. Hospital130 predicts 30-day readmission; the other cohorts concern recorded diabetes status. Results and probabilities are never pooled.</div>', unsafe_allow_html=True)


def source_caption(key: str) -> None:
    st.caption(f"Source: {TABLES[key][1]} · frozen release {FROZEN_COMMIT[:12]}")


def render_metrics(row: dict, fields: list[tuple[str, str]]) -> None:
    columns = st.columns(len(fields))
    for col, (field, label) in zip(columns, fields):
        value = row.get(field, "")
        number = f"{float(value):,.0f}" if field.endswith("_n") and value != "" else f"{float(value):.4f}" if value != "" else "Not recorded"
        col.metric(label, number)


def explorer() -> None:
    st.subheader("Explore a sample’s feature availability")
    st.write("Edit a synthetic schema example and inspect panel eligibility. This does not generate a probability, a diagnosis, or a validated individual prediction.")
    controls = st.columns(2)
    kind = controls[0].selectbox("Synthetic example", ["full", "minimal", "unsupported"],
        format_func=lambda k: {"full": "All fields observed", "minimal": "Smallest documented panel",
                               "unsupported": "Insufficient fields → abstention"}[k], key=f"example_{cohort}")
    names = availability[cohort]["scenarios"]
    requested = controls[1].selectbox("Routing request", ["auto", *names],
        format_func=lambda s: "Automatic · largest supported panel" if s == "auto" else s,
        key=f"scenario_{cohort}")
    sample = example_sample(cohort, kind)
    complete = example_sample(cohort, "full")
    st.caption(fixtures()[cohort]["encoding_note"])
    st.caption("Values are at the post-loader boundary, before fitted preprocessing. Uncheck Observed to remove a field. Category 'None' is an observed category, not an empty value.")
    left, right = st.columns([1.25, 1], gap="large")
    keys = [f"numeric_{cohort}_{kind}", f"category_{cohort}_{kind}"]

    def reset() -> None:
        for key in keys:
            st.session_state.pop(key, None)

    with left:
        st.button("Reset example", on_click=reset)
        entered = {}
        for group, label, key in zip([cfg["numeric_features"], cfg["categorical_features"]],
                                      ["Numeric fields", "Category fields"], keys):
            if not group:
                continue
            st.markdown(f"**{label}**")
            frame = pd.DataFrame([{"Field": field, "Value": complete[field], "Observed": field in sample} for field in group])
            edited = st.data_editor(frame, hide_index=True, disabled=["Field"],
                column_config={"Observed": st.column_config.CheckboxColumn("Observed", help="Unavailable fields cannot satisfy a panel.")},
                key=key, width="stretch", height=min(360, 40 + 35 * len(group)))
            for row in edited.to_dict("records"):
                if row["Observed"]:
                    entered[row["Field"]] = row["Value"]
    with right:
        st.markdown("#### Availability decision")
        try:
            report = availability_report(cohort, entered, None if requested == "auto" else requested)
            normalized = normalize_sample(cohort, entered)
        except ValueError as exc:
            st.error(str(exc))
            return
        if report["status"] == "abstain":
            st.warning("ABSTAIN · the requested information does not support a panel")
            st.write(f"Reason: `{report['reason']}`")
            if report.get("missing_required_features"):
                st.write("Missing required fields:", ", ".join(report["missing_required_features"]))
            st.caption("This is feature-availability abstention, separate from retrospective confidence rejection.")
        else:
            selected = report["scenario"]
            st.success(f"Supported panel · {selected}")
            st.write(names[selected]["description"])
            st.write(f"**{len(report['features_used'])} fields in the panel** · {len(normalized)} observed fields")
            st.caption("Eligibility only. The selected fitted family and calibration map cannot be recovered from aggregate metrics.")
            with st.expander("Panel fields and masking"):
                st.write("Panel fields:", ", ".join(report["features_used"]))
                st.write("Outside this panel (masked in the original inference path):", ", ".join(report["features_ignored"]) or "None")
            # Aggregate results are deliberately separated from the sample decision.
            st.markdown("#### Saved forced-panel experiment")
            st.caption("Cohort-level historical metrics for this panel; they do not change when example values change.")
            rows = [r for r in load_table("forced", cohort) if r["scenario"] == selected]
            if len(rows) == 1:
                render_metrics(rows[0], [("auroc", "AUROC"), ("average_precision", "AP"), ("brier_score", "Brier ↓")])
                source_caption("forced")
        st.button("Predict · validated artifacts unavailable", disabled=True, key="no_live_prediction")
        st.info("Raw probability, calibrated probability, class decision and sample confidence are unavailable. No replacement model is trained.")
        st.download_button("Download synthetic example & availability decision",
            json.dumps({"provenance": "synthetic, post-loader example; no model inference", "sample": normalized,
                        "availability": report, "frozen_commit": FROZEN_COMMIT}, indent=2),
            file_name=f"{cohort}_synthetic_availability.json", mime="application/json")
    with st.expander("Cohort target, preprocessing and evaluation boundary"):
        st.json({key: cfg.get(key) for key in ["task", "endpoint", "target_encoding", "evaluation_strategy", "group_strategy", "zero_as_missing", "applicability_notes"]})
        st.write("The original fitted pipeline uses training-fold medians/missingness indicators, logistic-regression-only scaling and training-only categorical one-hot vocabularies. The demo does not fit or approximate these objects.")


def experiments() -> None:
    st.subheader("Saved experiments & results")
    key = st.selectbox("Experiment", list(TABLES), format_func=lambda k: TABLES[k][0], key="experiment")
    st.write(TABLES[key][2])
    rows = load_table(key, cohort)
    if not rows:
        st.info("No saved rows for this cohort and experiment. No substitute results are generated.")
        return
    df = pd.DataFrame(rows)  # Exact saved strings, including blanks.
    selected = df.copy()
    filters = [name for name in ["system", "model", "scenario", "row_type"] if name in df.columns]
    columns = st.columns(max(1, len(filters)))
    for col, field in zip(columns, filters):
        choices = ["All", *sorted(df[field].unique())]
        initial = choices.index("availability_router") if key == "runtime" and field == "system" else 0
        value = col.selectbox(field.replace("_", " ").title(), choices, index=initial, key=f"filter_{cohort}_{key}_{field}")
        if value != "All":
            selected = selected.loc[selected[field].eq(value)]
    if key == "selective":
        targets = sorted(selected["nominal_coverage"].unique(), key=float, reverse=True)
        target = st.selectbox("Saved nominal observation coverage", targets, format_func=lambda v: f"{float(v):.0%}")
        selected = selected.loc[selected["nominal_coverage"].eq(target)]
        st.caption("Only saved coverage levels are selectable. Event coverage may differ greatly from observation coverage; excluded prevalence and both exclusion counts are retained below.")
    if len(selected) == 1 and key in {"runtime", "selective", "forced"}:
        row = selected.iloc[0].to_dict()
        render_metrics(row, [("auroc", "AUROC"), ("average_precision", "Average precision"), ("brier_score", "Brier score ↓")])
        coverage = "actual_observation_coverage" if key == "selective" else "coverage"
        if coverage in row:
            render_metrics(row, [(coverage, "Obs. coverage"), ("positive_event_coverage", "Event coverage"), ("accepted_n", "Accepted records")])
    if key == "benchmark":
        chart = selected.set_index("model")[["auroc", "average_precision"]].apply(pd.to_numeric, errors="coerce")
        st.bar_chart(chart, horizontal=True, width="stretch")
        st.caption("AUROC and AP describe this cohort only. AP depends on prevalence; this chart is not a cross-cohort ranking.")
    st.caption(f"{len(selected)} of {len(df)} saved rows · blank source cells stay blank")
    st.dataframe(selected, hide_index=True, width="stretch")
    source_caption(key)
    st.download_button("Download displayed saved rows", selected.to_csv(index=False),
        file_name=f"{cohort}_{key}_saved_rows.csv", mime="text/csv")
    if key == "contrasts":
        st.info("The mixed and negative findings are part of the result: dynamic switching did not demonstrate consistent Holm-corrected superiority over the robust fixed family.")
    if key == "calibration":
        st.info("These selection records cannot transform a sample’s raw score. Live inference requires the corresponding fitted preprocessor, model and calibration object.")


def reproducibility() -> None:
    st.subheader("Evidence you can trace")
    st.success(f"Checksum checks passed · {len(manifest['sha256'])} reviewed sources")
    st.write("The demo reads local, frozen aggregate files. It does not contact a prediction service, use patient records, or train a model. Synthetic input editing stays in the current session unless you choose to download it.")
    st.code(f"Frozen release: v1.0.0-paper\nCommit: {FROZEN_COMMIT}\nProtocol: t2dm-final-internal-validation-v1\nVersion DOI: 10.5281/zenodo.23537932")
    st.markdown("**What is executable here:** feature-panel eligibility, saved-table exploration, checksum checks and an offline report export.")
    st.markdown("**What remains unavailable:** sample-level raw/calibrated probabilities, fitted family/mapping selection, individual explanations and exact historical training replay. Public model/preprocessing/calibration objects and row-level predictions are absent.")
    st.markdown("**Original decision semantics:** largest fully supported panel, then its training-selected family/map; unsupported availability abstains. The original router uses a fixed 0.5 classification threshold. Confidence rejection is a separate cohort-ranked retrospective analysis, not an additional live threshold.")
    st.code("python -m pytest -q demo/tests\npython -m demo.export_offline --output outputs/panel-demo.html")
    st.caption("Open the generated HTML directly in a browser for a self-contained offline fallback. Setup, preflight and presentation steps: demo/README.md.")
    with st.expander("Source hashes"):
        st.json(manifest)


{"Example explorer": explorer, "Experiments & results": experiments, "Reproducibility": reproducibility}[page]()
st.divider()
st.caption("v1.0.0-paper · saved internal-validation evidence · no clinical interpretation or patient-level prediction")
