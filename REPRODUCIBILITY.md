# Reproducing the public snapshot's supported outputs

**Status corrected 29 October 2026.** The independently initialized public snapshot at [pranavprabhu05/T2DM](https://github.com/pranavprabhu05/T2DM) was derived from research commit `12d3f9b3676d8d5638d27794bf11e01b36027310` and contains no original research Git history. The former `OppositeExpert/T2DM` URL redirects to the canonical repository. The published [release `v1.0.0-paper`](https://github.com/pranavprabhu05/T2DM/releases/tag/v1.0.0-paper), commit `faa5799fa01d8d7381ea43415fbec01036d1e4ff`, is archived at version DOI [10.5281/zenodo.23537932](https://doi.org/10.5281/zenodo.23537932). Software/archive publication does not establish journal acceptance or publication.

Run the complete verification procedure below from the frozen tag in a new directory:

```bash
git clone --branch v1.0.0-paper --single-branch https://github.com/pranavprabhu05/T2DM.git T2DM-paper
cd T2DM-paper
git rev-parse HEAD
```

Confirm `HEAD` is `faa5799fa01d8d7381ea43415fbec01036d1e4ff`. Its original manifest seals the documentation as well as the evidence. Later default-branch documentation intentionally differs from that manifest; `verify_snapshot.py` and the portable test that invokes it run against the frozen release. CI has two independent jobs: **Frozen release verification** checks out that pinned commit, confirms the original tag object/commit/tree, and runs the complete original integrity checks, portable suite and aggregate reconstructions. **Current documentation validation** checks its current branch checkout, confirms the same release identity, validates citation metadata and relative links, preserves original report bodies, and compares every protected file with the frozen Git tree. Only the explicit documentation and CI-support allowlist may differ. The original verifier, inherited tests, manifest and checksum sidecar are unchanged; nothing is resealed. Historical preparation reports and machine-readable provenance describe their recorded preparation state; see [RELEASE_STATUS.md](publication_release/RELEASE_STATUS.md) for current identifiers and boundaries.

## Current-branch documentation checks

Run these separately from a full-history checkout of the current branch with the published release tag fetched. They require Python 3.12 and the existing pinned YAML parser; the scientific package environment is not needed for this documentation job.

```bash
python -m pip install PyYAML==6.0.3
python -m unittest discover -s .github/ci -p 'test_current_documentation.py' -v
python .github/ci/verify_current_documentation.py
```

The checks reject changes to scientific source/evidence, inherited tests, manifests, provenance and manuscript reference files. They also reject missing frozen files, unexpected new files, symlinks, changed executable modes, retargeted release identities, incorrect citation identifiers and edited historical report bodies. The complete portable scientific suite remains in the separate frozen-release job; these documentation checks do not replace it. The remaining sections describe the frozen checkout selected above.

## Environment

Use CPython 3.12.x (reference 3.12.0). From the checkout root:

```bash
python3.12 -m venv .venv-review
source .venv-review/bin/activate
python -m pip install -r requirements.lock
python -m pip install --no-deps --no-build-isolation -e .
python scripts/verify_environment.py
```

On the historical test host the same interpreter version is named python3; use that executable if python3.12 is unavailable. Editable installation must point to this checkout. Do not copy the research virtual environment or install only a wheel without checkout-relative configuration. The 48-distribution lock pins versions, not wheel hashes. The preparation reports record macOS arm64 testing; the [published-commit GitHub Actions run](https://github.com/pranavprabhu05/T2DM/actions/runs/39612010229) separately records Ubuntu validation. Neither establishes Windows/Docker behavior or cross-platform timing parity. Native library/runtime availability and fonts affect portability.

## Evidence integrity and public statistical checks

```bash
python scripts/verify_publication_results.py
python publication_release/verify_public_aggregates.py
python publication_release/verify_manuscript_sources.py
python publication_release/verify_snapshot.py
python -m pytest -q -m "not local_research_data"
```

The fingerprint verifier checks all **85 retained unchanged publication files and 14 unchanged correction-support files**. It deliberately does not certify the excluded 16 members of the original 101-file research package. The original 101-entry checksum list is retained as a separately named historical index. SNAPSHOT_PROVENANCE.json makes every omission and derivative explicit. The release manifest checks exact complete included-file coverage; it omits itself and its checksum sidecar to avoid circular hashing, then verifies the sidecar separately.

Aggregate verification checks 47 curated tables, saved point differences/Holm adjustments, repeat mean/SD cells and routing/selective totals. Arithmetic tolerance is absolute 1e-10; copied CSV strings and hashes are exact. Manuscript ledger verification matches 545 main and 1,443 supplementary cells against their exact saved sources and rounding rules. Its optional --manuscript-dir accepts a separately supplied local manuscript directory to check display presence; that optional source/PDF package is not required for public aggregate verification.

No raw P values, bootstrap intervals or prediction-derived metrics are independently regenerated by these public checks. Seven inherited tests require local_research_data and remain excluded from the portable command. No inherited test file or tolerance was weakened. Some portable tests fit small synthetic fixtures; they do not train the study models or repeat the experiments. Added snapshot tests verify complete manifest coverage, unchanged inherited code/tests, exclusions and attribution.

## Table reconstruction

```bash
python scripts/finalize_journal_handoff.py reconstruct --destination outputs/reviewer-tables
```

Use an empty destination outside the protected analysis report. The output consists of 47 exact-source CSV views and 11 rounded Markdown tables, with the source index. This is aggregate curation, not full PDF typesetting or model fitting. The one public statistical-verification projection drops only the private source-path column from 220 original aggregate rows; its source/target filenames explicitly include PUBLIC. The source index and filename adapter identify that derivative, while all other curated table bytes retain their baseline identity.

Do not run prepare/seal/archive or historical report/training phases as public verification commands. Those commands retain private-study workflows and may write evidence. The public procedure never overwrites the private research package.

## Paper figures

```bash
python publication_release/paper_evidence/REGENERATE_FIGURES.py outputs/reviewer-figures
```

Reads only included aggregate bins/curves and forced-panel summaries. Expected outputs are Figure_1_Calibration, Figure_2_Decision_Curves and Figure_3_Availability, each PNG/PDF. This fresh-copy run reproduced all three PNG files byte-identically; consult VERIFICATION_RESULTS.md for the actual outcome. PDF creation metadata and different font/backends can change byte hashes. Drawing saved bins/curves does not independently recreate their scientific estimates from participants.

## Separately acquired public datasets

The source/hash/conversion authority is config/data_sources.yaml. Provider terms/attribution remain separate from MIT. Working acquisition paths in the earlier independent provider audit were:

```bash
python scripts/acquire_data.py --dataset pidd --download
python scripts/acquire_data.py --dataset sylhet --download
python scripts/acquire_data.py --dataset hospital130 --download
python publication_release/verify_cohort_counts.py --dataset pidd
python publication_release/verify_cohort_counts.py --dataset sylhet
python publication_release/verify_cohort_counts.py --dataset hospital130
```

The documented BRFSS command `python scripts/acquire_data.py --dataset brfss --download` returned HTTP 403 in that provider audit. This is a known failed pathway, not a claimed working command. Do not bypass its hash contract or use a different dataset. A hash-matching local file may support a local count check but would not prove that the public download works. All-cohort count verification returns exit 2 if any raw input is absent. Raw data remains under ignored data/raw and is not in the release payload.

Public source acquisition does not restore private evaluation split assignments, fitted objects/calibrators, saved individual predictions or retained bootstrap arrays. The three eligible-population recounts previously matched 768/268/8 (PIDD), 520/320/16 (Sylhet), and 99,343/11,314/46 (Hospital130) for records/events/predictors. Reconstructing original evaluation counts from private split memberships remains a different task.

## Unavailable historical reproduction

Exact historical training replay is BLOCKED: the complete source matching its original fingerprint is unavailable. Do not bypass source-binding/final-run receipts or relabel public fingerprint checks as exact training replay. Historical component timing reconstruction is PARTIAL; the original OOF/preprocessing/calibration/inference components were not all separately recorded. A4 computational-cost REPORTING is COMPLETE, but raw timing samples/fitted objects needed to reconstruct or rerun those workloads are not distributed. No study training, tuning, new timings or new scientific evidence is authorized by this release process.

The data are four separate retrospective internal-evaluation tasks. Hospital130 is readmission, not diabetes detection; confidence rejection differs from availability abstention; dependent-repeat SD is not participant/cluster uncertainty; SHAP and retrospective utility do not establish causal or clinical benefit.
