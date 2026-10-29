"""Regression checks for the boundary between mutable docs and frozen evidence."""
import hashlib
from pathlib import Path
import tempfile
import unittest

import verify_current_documentation as checks


class DocumentationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.data = b"frozen numerical evidence\n"
        (self.root / "evidence.csv").write_bytes(self.data)
        blob = hashlib.sha1(f"blob {len(self.data)}\0".encode() + self.data).hexdigest()
        self.baseline = {"evidence.csv": ("100644", blob)}

    def test_unchanged_evidence_is_verified(self):
        self.assertEqual(checks.verify_file_boundary(self.root, self.baseline, {"evidence.csv"}), 1)

    def test_modified_evidence_is_rejected(self):
        (self.root / "evidence.csv").write_text("changed evidence\n")
        with self.assertRaisesRegex(ValueError, "Protected frozen file changed"):
            checks.verify_file_boundary(self.root, self.baseline, {"evidence.csv"})

    def test_missing_evidence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing="):
            checks.verify_file_boundary(self.root, self.baseline, set())

    def test_unreviewed_addition_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "added="):
            checks.verify_file_boundary(self.root, self.baseline, {"evidence.csv", "new.csv"})

    def test_documentation_can_change(self):
        (self.root / "README.md").write_text("current release status\n")
        baseline = {**self.baseline, "README.md": ("100644", "old-doc-blob")}
        self.assertEqual(checks.verify_file_boundary(self.root, baseline, set(baseline)), 1)

    def test_symlink_cannot_bypass_documentation_boundary(self):
        (self.root / "README.md").symlink_to("evidence.csv")
        with self.assertRaisesRegex(ValueError, "Non-regular file"):
            checks.verify_file_boundary(self.root, self.baseline, {"evidence.csv", "README.md"})

    def test_executable_mode_change_is_rejected(self):
        (self.root / "evidence.csv").chmod(0o755)
        with self.assertRaisesRegex(ValueError, "Protected frozen file changed"):
            checks.verify_file_boundary(self.root, self.baseline, {"evidence.csv"})

    def test_retargeted_release_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "identity changed"):
            checks.check_release_identity("new-tag-object", checks.COMMIT, checks.TREE)

    def test_wrong_doi_and_added_named_author_are_rejected(self):
        citation = checks.yaml.safe_load((checks.ROOT / "CITATION.cff").read_text())
        checks.verify_citation(citation, citation["title"])
        for key, value in (("doi", "10.5281/zenodo.0"), ("authors", [{"name": "Unapproved author"}])):
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, key):
                checks.verify_citation({**citation, key: value}, citation["title"])

    def test_historical_body_must_be_preserved(self):
        original = b"Original preparation report\n"
        prefix = f"> **Historical pre-publication report** {checks.DOI}\n\n".encode()
        checks.verify_historical_text("report.md", prefix + original, original)
        with self.assertRaisesRegex(ValueError, "original report changed"):
            checks.verify_historical_text("report.md", prefix + b"edited report\n", original)

    def test_relative_links_must_exist_and_stay_inside_repository(self):
        page = self.root / "README.md"
        page.write_text("[Evidence](evidence.csv)\n")
        self.assertEqual(checks.verify_markdown_links(self.root, {"README.md"}), 1)
        for link in ("missing.md", "../outside.md"):
            page.write_text(f"[Bad link]({link})\n")
            with self.subTest(link=link), self.assertRaisesRegex(ValueError, "relative link"):
                checks.verify_markdown_links(self.root, {"README.md"})

    def test_stale_current_status_is_rejected(self):
        status = f"{checks.REPOSITORY} {checks.TAG} {checks.DOI}\n"
        checks.verify_status_text("README.md", status)
        with self.assertRaisesRegex(ValueError, "Superseded"):
            checks.verify_status_text("README.md", status + "No production Zenodo DOI is available.")


if __name__ == "__main__":
    unittest.main()
