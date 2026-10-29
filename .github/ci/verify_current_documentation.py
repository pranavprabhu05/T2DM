"""Validate current docs without resealing or modifying the frozen paper release."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[2]
TAG = "v1.0.0-paper"
TAG_OBJECT = "d8c74928df54445954683f6239b02b344f1ac4fe"
COMMIT = "faa5799fa01d8d7381ea43415fbec01036d1e4ff"
TREE = "25d6e6dee449ad917e459230ca5fd6f5155aa7f2"
DOI = "10.5281/zenodo.23537932"
REPOSITORY = "https://github.com/pranavprabhu05/T2DM"

ACTIVE_DOCS = {
    "README.md", "REPRODUCIBILITY.md", "LICENSE_STATUS.md",
    "docs/LICENSE_AND_DATA_USE.md", "publication_release/RELEASE_STATUS.md",
    "publication_release/PUBLIC_RELEASE_LIMITATIONS.md",
    "publication_release/RESULT_TO_SOURCE_MAP.md",
}
HISTORICAL_DOCS = {
    f"publication_release/{name}.md" for name in (
        "FRESH_CLONE_VERIFICATION", "LICENSING_REVIEW", "PUBLIC_EXPOSURE_AUDIT",
        "PUBLIC_RELEASE_FINAL_REPORT", "VERIFICATION_RESULTS",
    )
}
DOCUMENTATION = ACTIVE_DOCS | HISTORICAL_DOCS | {"CITATION.cff"}
# Changes to evidence, inherited source/tests, manifests and manuscript material
# are forbidden. New mutable paths require explicit review of this narrow list.
MUTABLE_PATHS = DOCUMENTATION | {
    ".github/workflows/ci.yml",
    ".github/ci/verify_current_documentation.py",
    ".github/ci/test_current_documentation.py",
}


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def check_release_identity(tag_object: str, commit: str, tree: str) -> None:
    if (tag_object, commit, tree) != (TAG_OBJECT, COMMIT, TREE):
        raise ValueError("Frozen release tag/commit/tree identity changed")


def frozen_inventory(root: Path) -> dict[str, tuple[str, str]]:
    entries = {}
    for entry in git(root, "ls-tree", "-rz", "--full-tree", COMMIT).split(b"\0"):
        if entry:
            metadata, path = entry.split(b"\t", 1)
            mode, kind, sha = metadata.decode().split()
            if kind != "blob":
                raise ValueError("Unexpected non-file in frozen inventory")
            entries[path.decode()] = (mode, sha)
    if len(entries) != 410:
        raise ValueError("Frozen release must contain exactly 410 files")
    return entries


def verify_file_boundary(root: Path, baseline: dict, current: set[str]) -> int:
    missing = set(baseline) - current
    additions = current - set(baseline) - MUTABLE_PATHS
    if missing or additions:
        raise ValueError(f"File boundary changed: missing={sorted(missing)}, added={sorted(additions)}")
    verified = 0
    for path in sorted(current):
        source = root / path
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Non-regular file in current branch: {path}")
        if path in baseline and path not in MUTABLE_PATHS:
            content = source.read_bytes()
            blob = hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()
            mode, expected = baseline[path]
            executable = bool(source.stat().st_mode & 0o111)
            if blob != expected or executable != (mode == "100755"):
                raise ValueError(f"Protected frozen file changed: {path}")
            verified += 1
    return verified


def verify_citation(citation: dict, original_title: str) -> None:
    expected = {
        "cff-version": "1.2.0", "title": original_title, "type": "software",
        "authors": [{"name": "T2DM Project Contributors"}],
        "repository-code": REPOSITORY, "url": f"{REPOSITORY}/releases/tag/{TAG}",
        "version": TAG, "commit": COMMIT, "date-released": "2026-10-21",
        "doi": DOI, "license": "MIT",
    }
    for key, value in expected.items():
        if citation.get(key) != value:
            raise ValueError(f"Citation metadata mismatch: {key}")
    if not isinstance(citation.get("message"), str) or not citation["message"].strip():
        raise ValueError("Citation message is missing")


def verify_status_text(path: str, text: str) -> None:
    for identifier in (REPOSITORY, TAG, DOI):
        if identifier not in text:
            raise ValueError(f"Current release identifier missing from {path}: {identifier}")
    stale = (
        "Local release candidate, pending approval.",
        "No production Zenodo DOI is available.",
        "No current public tag distributes this candidate yet.",
        "production DOI remain uncreated/unverified",
        "This local release candidate has not been published.",
        "This local candidate is not published",
    )
    if any(phrase in text for phrase in stale):
        raise ValueError(f"Superseded release-status assertion in {path}")


def verify_historical_text(path: str, current: bytes, original: bytes) -> None:
    prefix = current[:-len(original)] if current.endswith(original) else b""
    if not prefix.startswith(b"> **Historical pre-publication report") or DOI.encode() not in prefix:
        raise ValueError(f"Historical notice or original report changed: {path}")


def verify_markdown_links(root: Path, paths: set[str]) -> int:
    checked = 0
    for path in sorted(paths):
        for destination in re.findall(r"\]\(([^)\n]+)\)", (root / path).read_text()):
            parsed = urlsplit(destination.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = ((root / path).parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                raise ValueError(f"Broken or escaping relative link in {path}: {destination}")
            checked += 1
    return checked


def verify(root: Path = ROOT) -> dict:
    check_release_identity(
        git(root, "rev-parse", f"refs/tags/{TAG}").decode().strip(),
        git(root, "rev-parse", f"refs/tags/{TAG}^{{commit}}").decode().strip(),
        git(root, "rev-parse", f"{COMMIT}^{{tree}}").decode().strip(),
    )
    baseline = frozen_inventory(root)
    current = {p.decode() for p in git(
        root, "ls-files", "--cached", "--others", "--exclude-standard", "-z"
    ).split(b"\0") if p}
    protected = verify_file_boundary(root, baseline, current)
    original_citation = yaml.safe_load(git(root, "show", f"{COMMIT}:CITATION.cff"))
    verify_citation(yaml.safe_load((root / "CITATION.cff").read_text()), original_citation["title"])
    for path in ACTIVE_DOCS:
        verify_status_text(path, (root / path).read_text())
    for path in HISTORICAL_DOCS:
        verify_historical_text(path, (root / path).read_bytes(), git(root, "show", f"{COMMIT}:{path}"))
    return {
        "passed": True, "frozen_tag": TAG, "frozen_commit": COMMIT,
        "frozen_files": len(baseline), "protected_files_unchanged": protected,
        "documentation_files_validated": len(DOCUMENTATION),
        "historical_report_bodies_preserved": len(HISTORICAL_DOCS),
        "relative_links_checked": verify_markdown_links(root, DOCUMENTATION - {"CITATION.cff"}),
        "manifest_regenerated": False, "scientific_evidence_changed": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
