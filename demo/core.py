"""Read frozen aggregates and demonstrate availability, without performing inference.

Inputs are synthetic, already encoded model-input fields (the output boundary of
data/loaders.py). This module never fits, imputes, calibrates or unpickles objects.
"""
from __future__ import annotations

import csv
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
FROZEN_COMMIT = "faa5799fa01d8d7381ea43415fbec01036d1e4ff"
COHORTS = ("pidd", "sylhet", "brfss", "hospital130")

# Each view retains its own estimand. Never join rows across cohort endpoints.
TABLES = {
    "runtime": (
        "Runtime fallback policies",
        "results/final_publication/tables/routing_fallback_performance.csv",
        "Accepted-case metrics under natural availability. Read observation and positive-event coverage alongside performance.",
    ),
    "benchmark": (
        "Full-schema benchmark",
        "results/final_publication/tables/full_panel_model_performance.csv",
        "Five calibrated model families. PIDD/Sylhet use record-averaged repeated-validation probabilities; BRFSS/Hospital130 use historical internal evaluation partitions.",
    ),
    "forced": (
        "Forced-panel masking",
        "results/final_publication/tables/availability_panel_degradation.csv",
        "Prespecified forced masks applied to original full-schema fits. These rows are not predictions for your edited example or separately trained smaller models.",
    ),
    "selective": (
        "Selective prediction & coverage",
        "analysis/journal_revision/03_SELECTIVE_PREDICTION.csv",
        "Retrospective coverage-ranked selection using 2 × |calibrated probability − 0.5|. Groups are retained together when present. This does not define a deployable single-sample confidence cutoff.",
    ),
    "contrasts": (
        "Switching comparisons",
        "analysis/journal_revision/07_RUNTIME_PAIRED_COMPARISONS.csv",
        "Router minus comparator differences; retain direction, confidence intervals and Holm-adjusted P values. Switching did not establish consistent corrected superiority over the robust fixed-family policy.",
    ),
    "calibration": (
        "Training-derived calibration choices",
        "results/final_publication/tables/calibration_selection.csv",
        "Recorded development/fold choices, not calibrator objects. Identity is eligible. Selection uses cross-fitted training probabilities, Brier score then log loss; isotonic requires 1,000 calibration observations.",
    ),
    "reduced": (
        "Reduced-schema refits",
        "analysis/journal_revision/04_RETRAINED_PANEL_COMPARISON.csv",
        "Saved reduced-schema versus masked-input comparisons. Preprocessing, learner and calibration were refitted within the original training boundaries, with the original family/hyperparameters; no independent reduced-schema tuning.",
    ),
    "ablation": (
        "Calibration / switching ablation",
        "analysis/journal_revision/05_CALIBRATION_SWITCHING_ABLATION.csv",
        "A/B use a robust fixed family; C/D use panel-selected families. A/C use full-schema calibration and B/D panel mappings. These are saved experiment results.",
    ),
    "routing": (
        "Observed routing distribution",
        "analysis/journal_revision/02_ROUTING_DISTRIBUTION.csv",
        "Unique evaluation panel/event counts and per-repeat model/mapping counts are different row types; do not sum them together.",
    ),
    "repeats": (
        "Repeat sensitivity",
        "analysis/journal_revision/01_PER_REPEAT_SENSITIVITY.csv",
        "Dependent repeats, descriptive mean/sample SD and primary metrics of averaged probabilities are distinct estimands. Repeat SD is not a confidence interval.",
    ),
    "cost": (
        "Recorded computational cost",
        "analysis/journal_revision/A4_MAIN_TEXT_TABLE.csv",
        "Historical training and successor component sums; warmed probability-only latency excludes loading, explanations and cold starts. Recorded hardware/workload results do not establish cross-platform timing parity.",
    ),
    "thresholds": (
        "Threshold reporting",
        "results/final_publication/tables/threshold_performance.csv",
        "Saved operating metrics, including fixed 0.5 and descriptive development-selected thresholds. These are research decisions without established clinical benefit.",
    ),
}


class EvidenceError(ValueError):
    """A required source is missing or differs from the reviewed evidence."""


def verify_sources(root: Path = ROOT) -> dict[str, Any]:
    manifest = json.loads((root / "demo/source_manifest.json").read_text())
    if manifest["frozen_commit"] != FROZEN_COMMIT:
        raise EvidenceError("Unexpected frozen evidence identity")
    for relative, expected in manifest["sha256"].items():
        path = root / relative
        if path.is_symlink() or not path.is_file():
            raise EvidenceError(f"Required evidence missing or non-regular: {relative}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise EvidenceError(f"Evidence checksum mismatch: {relative}")
    return manifest


# Only parsed immutable inputs are cached. verify_sources is never cached and
# runs before any UI display or offline export, so edits still fail closed.
@lru_cache(maxsize=8)
def contracts(root: Path = ROOT) -> tuple[dict, dict]:
    configs = yaml.safe_load((root / "config/datasets.yaml").read_text())["datasets"]
    availability = yaml.safe_load((root / "config/availability_scenarios.yaml").read_text())["datasets"]
    return configs, availability


@lru_cache(maxsize=8)
def fixtures(root: Path = ROOT) -> dict:
    return json.loads((root / "demo/fixtures.json").read_text())["cohorts"]


def example_sample(cohort: str, kind: str, root: Path = ROOT) -> dict:
    configs, panels = contracts(root)
    if cohort not in COHORTS:
        raise ValueError("Unknown cohort")
    sample = dict(fixtures(root)[cohort]["values"])
    if kind == "full":
        return sample
    if kind == "minimal":
        scenarios = panels[cohort]["scenarios"]
        name = min(scenarios, key=lambda k: (len(scenarios[k]["available_features"]), k))
        return {k: sample[k] for k in scenarios[name]["available_features"]}
    if kind == "unsupported":
        # A single field cannot satisfy any of the documented panels.
        name = configs[cohort]["numeric_features"][0]
        return {name: sample[name]}
    raise ValueError("Unknown synthetic example")


def normalize_sample(cohort: str, sample: dict, root: Path = ROOT) -> dict:
    """Validate encoded fields; only loader-documented PIDD zeros become missing.

    No medians, one-hot encodings, scaling, ICD collapse or raw-provider recoding
    are guessed here. Those transformations belong to loaders and fitted bundles.
    """
    configs, _ = contracts(root)
    if cohort not in COHORTS or not isinstance(sample, dict):
        raise ValueError("Expected a known cohort and one field/value mapping")
    cfg = configs[cohort]
    features = cfg["numeric_features"] + cfg["categorical_features"]
    unknown = set(sample) - set(features)
    if unknown:
        raise ValueError(f"Unknown or excluded fields: {sorted(unknown)}")
    clean = {}
    for field, value in sample.items():
        if value is None:
            continue
        if field in cfg["numeric_features"]:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{field}: enter a finite encoded number or mark unavailable")
            if field in cfg.get("zero_as_missing", []) and value == 0:
                continue
            if cohort == "sylhet" and field != "Age" and value not in (0, 1):
                raise ValueError(f"{field}: Sylhet binary fields must be encoded 0 or 1")
            if cohort == "hospital130" and field == "age" and value not in range(10):
                raise ValueError("Hospital130 age is an encoded decade (0–9), not years")
            if cohort == "brfss":
                ranges = {"Age": (1, 13), "GenHlth": (1, 5), "Education": (1, 6), "Income": (1, 8),
                          "MentHlth": (0, 30), "PhysHlth": (0, 30)}
                if field in ranges:
                    low, high = ranges[field]
                    if not (low <= value <= high and float(value).is_integer()):
                        raise ValueError(f"{field}: encoded integer range is {low}–{high}")
                elif field != "BMI" and value not in (0, 1):
                    raise ValueError(f"{field}: BRFSS binary fields must be encoded 0 or 1")
            clean[field] = float(value)
        else:
            if not isinstance(value, str) or not value.strip() or value.strip() == "?":
                raise ValueError(f"{field}: use an encoded category or mark unavailable")
            clean[field] = value
    return clean


def availability_report(cohort: str, sample: dict, scenario: str | None = None, root: Path = ROOT) -> dict:
    """Mirror only route_patient's panel eligibility and deterministic tie-break.

    Tests compare this preflight with the unchanged inference function. Supported
    status deliberately stops before model/calibrator selection or prediction.
    """
    configs, panels = contracts(root)
    clean = normalize_sample(cohort, sample, root)
    configured = configs[cohort]["numeric_features"] + configs[cohort]["categorical_features"]
    scenarios = {k: v["available_features"] for k, v in panels[cohort]["scenarios"].items()}
    available = set(clean)
    base = {"cohort": cohort, "endpoint": configs[cohort]["endpoint"],
            "inference_status": "unavailable_no_validated_artifacts", "available_features": sorted(available)}
    if scenario is not None:
        if scenario not in scenarios:
            raise ValueError(f"Unknown availability scenario '{scenario}'")
        missing = set(scenarios[scenario]) - available
        if missing:
            return {**base, "status": "abstain", "reason": "required_scenario_features_missing",
                    "scenario": scenario, "missing_required_features": sorted(missing)}
        selected = scenario
    else:
        supported = [name for name, fields in scenarios.items() if set(fields) <= available]
        if not supported:
            return {**base, "status": "abstain", "reason": "no_supported_feature_panel"}
        selected = max(supported, key=lambda name: (len(scenarios[name]), name == "full", name))
    return {**base, "status": "supported_no_model", "scenario": selected,
            "features_used": scenarios[selected],
            "features_ignored": sorted(set(configured) - set(scenarios[selected]))}


def load_table(key: str, cohort: str, root: Path = ROOT) -> list[dict[str, str]]:
    """Return exact saved strings; blank cells remain blank, never fabricated zeros."""
    if cohort not in COHORTS:
        raise ValueError("Unknown cohort")
    with (root / TABLES[key][1]).open(newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["dataset"] == cohort]
    cfg = contracts(root)[0][cohort]
    if any(row.get("endpoint", cfg["endpoint"]) != cfg["endpoint"] for row in rows):
        raise EvidenceError(f"Endpoint mismatch in {TABLES[key][1]}")
    return rows
