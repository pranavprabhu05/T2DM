"""Scientific-boundary checks and interaction tests for the aggregate demo."""
import csv
import importlib.util
import json
from pathlib import Path
import random
import re
import shutil

import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from demo.core import (COHORTS, ROOT, TABLES, EvidenceError, availability_report,
                       contracts, example_sample, fixtures, load_table,
                       normalize_sample, verify_sources)
from demo.export_offline import build_report


@pytest.mark.parametrize("cohort", COHORTS)
def test_fixture_schema_and_all_documented_panels(cohort):
    cfg, panels = contracts()
    full = example_sample(cohort, "full")
    assert set(full) == set(cfg[cohort]["numeric_features"] + cfg[cohort]["categorical_features"])
    assert normalize_sample(cohort, full) == full
    assert fixtures()[cohort]["input_boundary"] == "post_loader_pre_fitted_preprocessing"
    assert cfg[cohort]["target_name"] not in full
    forced = load_table("forced", cohort)
    for name, spec in panels[cohort]["scenarios"].items():
        sample = {f: full[f] for f in spec["available_features"]}
        report = availability_report(cohort, sample, name)
        assert report["status"] == "supported_no_model"
        assert report["scenario"] == name
        assert report["features_used"] == spec["available_features"]
        assert any(row["scenario"] == name for row in forced)
        assert not {"prediction", "probability_raw", "probability_calibrated", "model"} & report.keys()
        del sample[spec["available_features"][0]]
        assert availability_report(cohort, sample, name)["reason"] == "required_scenario_features_missing"
    assert availability_report(cohort, {})["reason"] == "no_supported_feature_panel"
    assert availability_report(cohort, example_sample(cohort, "unsupported"))["status"] == "abstain"


def test_availability_matches_unchanged_pipeline_for_500_masks_and_forced_panels():
    # Import the exact, unchanged inference source without importing the routing
    # package's training/evaluation dependencies. Test doubles never enter the UI.
    path = ROOT / "src/diabetes_pipeline/routing/inference.py"
    spec = importlib.util.spec_from_file_location("frozen_inference", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class PassThrough:
        def transform(self, frame):
            return frame

    class TestModel:
        def predict_proba(self, frame):
            return np.array([0.25])

    class TestMap:
        def predict(self, values):
            return values

    configs, availability = contracts()
    rng = random.Random(20261104)
    for cohort in COHORTS:
        full = example_sample(cohort, "full")
        panels = {k: v["available_features"] for k, v in availability[cohort]["scenarios"].items()}
        bundle = {"configured_features": list(full), "scenarios": panels,
                  "selected_models": {k: "test_only" for k in panels},
                  "model_bundles": {"test_only": {"preprocessor": PassThrough(), "model": TestModel()}},
                  "scenario_calibrators": {"test_only": {k: TestMap() for k in panels}}}
        samples = [full, {}, example_sample(cohort, "minimal"), example_sample(cohort, "unsupported")]
        samples += [{k: v for k, v in full.items() if rng.random() > 0.25} for _ in range(125)]
        for sample in samples:
            normalized = normalize_sample(cohort, sample)
            for scenario in [None, *panels]:
                expected = module.route_patient(bundle, pd.DataFrame([normalized]), scenario_name=scenario)
                actual = availability_report(cohort, sample, scenario)
                if expected["status"] == "abstain":
                    assert actual["status"] == "abstain"
                    assert actual["reason"] == expected["reason"]
                    assert actual.get("missing_required_features") == expected.get("missing_required_features")
                else:
                    assert actual["status"] == "supported_no_model"
                    for field in ("scenario", "features_used", "features_ignored"):
                        assert actual[field] == expected[field]


def test_missing_zero_encoding_and_invalid_inputs():
    assert availability_report("pidd", {"Glucose": 0, "Age": 40})["status"] == "abstain"
    assert normalize_sample("pidd", {"Pregnancies": 0, "Insulin": 0}) == {"Pregnancies": 0}
    assert normalize_sample("hospital130", {"A1Cresult": "None"}) == {"A1Cresult": "None"}
    assert normalize_sample("sylhet", {"Polyuria": 0}) == {"Polyuria": 0}
    for cohort, sample in [
        ("pidd", {"Outcome": 1}), ("hospital130", {"patient_nbr": 12}),
        ("pidd", {"Glucose": float("inf")}), ("pidd", {"Age": float("nan")}),
        ("sylhet", {"Gender": "Male"}), ("sylhet", {"Polyuria": 2}),
        ("brfss", {"Age": 55}), ("brfss", {"HighBP": 2}),
        ("hospital130", {"age": 60}), ("hospital130", {"admission_type_id": 1}),
    ]:
        with pytest.raises(ValueError):
            normalize_sample(cohort, sample)
    with pytest.raises(ValueError, match="Unknown availability scenario"):
        availability_report("pidd", {}, "invented_panel")


@pytest.mark.parametrize("key", TABLES)
def test_table_projection_preserves_saved_strings_and_endpoints(key):
    with (ROOT / TABLES[key][1]).open(newline="") as handle:
        original = list(csv.DictReader(handle))
    for cohort in COHORTS:
        assert load_table(key, cohort) == [row for row in original if row["dataset"] == cohort]


def test_sources_are_complete_and_corruption_is_rejected(tmp_path):
    manifest = verify_sources()
    assert {v[1] for v in TABLES.values()} <= set(manifest["sha256"])
    assert {"config/datasets.yaml", "config/availability_scenarios.yaml", "demo/fixtures.json"} <= set(manifest["sha256"])
    for relative in ["demo/source_manifest.json", *manifest["sha256"]]:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    target = tmp_path / TABLES["runtime"][1]
    target.write_text(target.read_text() + "tamper\n")
    with pytest.raises(EvidenceError, match="checksum mismatch"):
        verify_sources(tmp_path)
    target.unlink()
    with pytest.raises(EvidenceError, match="missing or non-regular"):
        verify_sources(tmp_path)


def test_offline_payload_is_deterministic_complete_and_self_contained():
    report = build_report()
    assert report == build_report()
    assert not re.search(r'<(?:script|link|img)[^>]+(?:src|href)=["\']https?://', report)
    payload = json.loads(re.search(r'<script type="application/json" id="evidence">(.*?)</script>', report, re.S)[1])
    for key in TABLES:
        for cohort in COHORTS:
            assert payload["tables"][key]["rows"][cohort] == load_table(key, cohort)
    assert "connect-src 'none'" in report
    assert "validated artifacts unavailable" in report


@pytest.mark.parametrize("cohort", COHORTS)
def test_streamlit_examples_and_all_result_views(cohort):
    app = AppTest.from_file(str(ROOT / "demo/app.py"), default_timeout=30).run()
    app.selectbox(key="cohort").select(cohort).run()
    assert not app.exception
    assert any("validated artifacts unavailable" in b.label and b.disabled for b in app.button)
    for kind in ("minimal", "unsupported", "full"):
        app.selectbox(key=f"example_{cohort}").select(kind).run()
        assert not app.exception
        if kind == "unsupported":
            assert any("ABSTAIN" in item.value for item in app.warning)
        else:
            assert any("Supported panel" in item.value for item in app.success)
    app.radio(key="page").set_value("Experiments & results").run()
    for key in TABLES:
        app.selectbox(key="experiment").select(key).run()
        assert not app.exception, (cohort, key)
        if load_table(key, cohort):
            assert len(app.dataframe) == 1
    app.radio(key="page").set_value("Reproducibility").run()
    assert not app.exception
    assert any("Checksum checks passed" in item.value for item in app.success)


def test_explicit_missing_panel_request_and_cohort_switch_keep_endpoint():
    app = AppTest.from_file(str(ROOT / "demo/app.py"), default_timeout=30).run()
    app.selectbox(key="example_pidd").select("minimal").run()
    app.selectbox(key="scenario_pidd").select("full").run()
    assert any("required_scenario_features_missing" in item.value for item in app.markdown)
    app.selectbox(key="cohort").select("hospital130").run()
    assert not app.exception
    assert any("readmission_within_30_days" in item.value for item in app.markdown)


def test_editor_removal_and_reset_update_availability_without_predictions():
    app = AppTest.from_file(str(ROOT / "demo/app.py"), default_timeout=30).run()
    # Remove every observed field through Streamlit's data-editor state.
    app.session_state["numeric_pidd_full"] = {
        "edited_rows": {i: {"Observed": False} for i in range(8)},
        "added_rows": [], "deleted_rows": [],
    }
    app.run()
    assert not app.exception
    assert any("ABSTAIN" in item.value for item in app.warning)
    reset = next(button for button in app.button if button.label == "Reset example")
    reset.click().run()
    assert not app.exception
    assert any("Supported panel · full" in item.value for item in app.success)
