> **Historical pre-publication report — notice added 29 October 2026.** The original preparation text below is retained verbatim. Hosting, rename, tag and DOI statements describe the preparation state and are superseded by [current RELEASE_STATUS.md](RELEASE_STATUS.md): the public software release is `v1.0.0-paper`, commit `faa5799fa01d8d7381ea43415fbec01036d1e4ff`, version DOI [10.5281/zenodo.23537932](https://doi.org/10.5281/zenodo.23537932). This notice does not establish later author consent, institutional approval or journal acceptance. The frozen tag and Zenodo archive retain the original file bytes.

# Public exposure audit of the independent snapshot

**21 October 2026 — no identified private payload in the reviewed candidate. Publication approval remains pending.** This report concerns the independently initialized snapshot. The original research repository was already public at discovery and remains unchanged during preparation. Its history is not approved for the new public release.

## Original research history and accessible remote surfaces

The earlier complete accessible-history audit examined all **10 local refs / 25 reachable commits**, reconciled all three advertised remote branches, the preservation tag and PR head, and read every unique blob through Git object inspection. The non-shallow graph contained **803 unique blobs / 76,666,347 bytes**, with 1,020 top-level/decompressed/container inspections. Historical deletions were included; `.gitignore` was not used as a safety boundary. Full-history and extracted-object Gitleaks 8.30.1 scans, token/key patterns, row-level column checks, archive inspection and document text/metadata screening found no verified credential, tracked patient dataset, individual-prediction export or fitted private model. Eight historical scanner alerts were independently verified checksum false positives.

Personal filesystem paths occur in 40 historical blob versions and 24 current paths. These originals are excluded from this snapshot; no research history, preservation archive or raw CI log is carried over. Complete original refs and private backup receipts remain in the local transition review packet. No original commit, branch or tag was removed, rewritten or force-pushed.

Accessible GitHub surfaces were inspected: repository ownership/admin permission, branches/tags/PRs, releases/assets, workflows/runs/artifacts, Pages/deployments, authenticated webhooks/apps and wiki state. There are no releases/assets, retained Actions artifacts, Pages deployment, provisioned wiki or listed webhooks. One merged PR and 14 old workflow runs exist; the latest run's downloaded log archive passed inspection. The remaining **13 old CI log archives are uninspected** after anonymous download requests returned HTTP 403. They are not part of the candidate or cleared by this report. The original repository must become private under the separately approved transition.

Unadvertised server refs, expired/deleted logs/artifacts, backend retention, caches, prior public copies/downloads and external clones/integrations are outside the inspected scope. Making the research archive private cannot retract prior copies. No universal absence-of-secrets or steganography guarantee is claimed.

## Independent public payload

The snapshot was selected file by file from the approved-public-candidate inventory, without copying the research `.git` directory. Source, configurations, relevant unchanged tests, dependencies, aggregate CSV/JSON evidence, figure inputs and original project artwork were reinspected. The manifest has exact included-file coverage; its sidecar and the final Git tree/archive receipt identify the reviewed bytes. The independent Git repository has no research ancestry, remote, LFS store, submodule or nested repository. The final local seal verifies all 25 original commit objects are absent.

Filename/content checks found no raw dataset, row-level prediction CSV, private estimator/calibrator/preprocessing object, split membership, bootstrap array, credential file, private ZIP or preservation archive. Individual-record identifier/probability/target columns were screened in every included CSV. All 24 held original paths are absent. Personal user-directory absolute-path patterns produced zero matches in included files.

Gitleaks **8.30.1**, archive/decode depth three, scanned the selected bytes. It returned **16 `generic-api-key` alerts**, all SHA-256 mappings for four included aggregate outcome-access receipt files repeated in four checksum/provenance indexes. Each flagged digest was independently recomputed against its target; all match. No ignore rule or test weakening was used. Scanner exit 1 is therefore reported as triaged false positives, not hidden as a clean exit. [SECRET_SCAN_TRIAGE.json](SECRET_SCAN_TRIAGE.json) records rule/path/classification without secret values.

All **nine** visual assets were examined: four single-page, unencrypted aggregate-figure PDFs, four PNGs and one SVG. PDF text/metadata, PNG metadata and SVG content had no detected private-path/key flags. The rendered contact sheet was visually screened; charts contain cohort-level evidence rather than patient records. No notebook, unreviewed third-party PDF, full manuscript/template package or complete ESM 2 ZIP is included. Visual screening is not an OCR/steganography certification.

## Disposition

| Classification | Finding / boundary | Action |
| --- | --- | --- |
| SAFE | Reviewed source/config/tests/aggregate evidence and project artwork; no identified sensitive payload | Exact manifest/tree/archive required before approval |
| SAFE | 16 independently verified checksum alerts | Retain provenance; no suppression |
| SAFE | All 24 held originals excluded; 220-row statistical derivative preserves retained numerical strings | Separate filename and new fingerprint; originals preserved privately |
| REQUIRES REVIEW | MIT contributor/institutional authority and original-artwork rights | Owner-requested standard MIT draft is prepared; final authority confirmation is required before publication |
| REQUIRES REVIEW | Public Git author identity and final creator ordering/affiliations | Confirm before creating/publishing the release commit and Zenodo record |
| BLOCKING for publishing the original history | Historical personal paths and incomplete old CI log coverage | Preserve original privately; do not import that history/settings/logs into the new public repository |
| BLOCKING for any publication now | Transition, exact release commit/tag and Zenodo publication approvals have not been given | Stop at the approval gate; no external action |

Third-party software is installed separately, not vendored. Provider datasets and manuscript/figure rights are distinct from the software MIT grant. No university approval or creator consent is inferred from Git authorship. This audit supports review of a bounded sanitized payload; it does not certify full training reproducibility.
