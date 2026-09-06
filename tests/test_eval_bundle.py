"""Safe construction and byte identity of the allowlisted evaluation artifact."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools/eval_bundle.py"
SPEC = importlib.util.spec_from_file_location("ultrasolve_eval_bundle", TOOL_PATH)
assert SPEC is not None and SPEC.loader is not None
bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundle)


class TestEvaluationBundle(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="ultrasolve bundle ")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.source = self.base / "relocated source with spaces"
        self.source.mkdir()
        self.allowlist = json.loads((ROOT / "evals/runtime-files.json").read_text())
        for relative in [*self.allowlist["files"], "evals/runtime-files.json"]:
            target = self.source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        self.output = self.base / "runtime output"
        self.manifest = self.base / "content manifest.json"

    def build(self) -> dict:
        return bundle.build_bundle(self.source, self.output, self.manifest)

    def change_allowlist(self, data: object) -> None:
        (self.source / "evals/runtime-files.json").write_text(json.dumps(data))

    def reject(self, code: str) -> None:
        with self.assertRaises(bundle.BundleError) as caught:
            self.build()
        self.assertIsInstance(caught.exception, ValueError)
        self.assertEqual(code, caught.exception.code)
        self.assertTrue(str(caught.exception))
        self.assertFalse(self.manifest.exists())
        self.assertFalse(self.output.exists())

    def test_allowlist_is_exactly_the_frozen_sorted_runtime_surface(self) -> None:
        skills = {"define", "solve", "simplify", "analogize", "restate", "generalize", "decompose", "invert"}
        expected = {
            ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
            ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "LICENSE", "PRIVACY.md",
            "agent-skills/define/references/problem-posing-sources.md",
            "agent-skills/define/references/worked-example.md",
            "agent-skills/solve/references/workflow-contract.md",
            "agent-skills/solve/references/technique-selection.md",
            "agent-skills/solve/references/shannon-source-notes.md",
            "agent-skills/solve/references/worked-examples.md",
        }
        for name in skills:
            expected.update({f"agent-skills/{name}/SKILL.md", f"agent-skills/{name}/agents/openai.yaml", f"adapters/claude/skills/{name}/SKILL.md"})
        expected.update(f"agent-skills/solve/references/methods/{name}.md" for name in skills - {"define", "solve"})
        self.assertEqual({"schema_version": 1, "files": sorted(expected)}, self.allowlist)
        self.assertEqual(42, len(expected))

    def test_build_preserves_bytes_and_emits_external_content_manifest(self) -> None:
        result = self.build()
        self.assertEqual(result, json.loads(self.manifest.read_text()))
        self.assertEqual(1, result["schema_version"])
        self.assertEqual("bundle composition verified", result["verification"])
        self.assertEqual("unknown", result["source_revision"])
        self.assertEqual("unknown", result["source_dirty"])
        self.assertEqual(self.allowlist["files"], [item["path"] for item in result["files"]])
        actual_paths = sorted(str(path.relative_to(self.output)) for path in self.output.rglob("*") if path.is_file())
        self.assertEqual(self.allowlist["files"], actual_paths)
        for item in result["files"]:
            original = (self.source / item["path"]).read_bytes()
            self.assertEqual(original, (self.output / item["path"]).read_bytes())
            self.assertEqual(len(original), item["bytes"])
            self.assertEqual(hashlib.sha256(original).hexdigest(), item["sha256"])
        encoded = json.dumps(result["files"], sort_keys=True, separators=(",", ":")).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), result["content_sha256"])

    def test_identical_bytes_keep_identity_across_locations_and_git_metadata(self) -> None:
        with mock.patch.object(bundle, "_git_metadata", return_value=("a" * 40, False)):
            first = self.build()
        self.output = self.base / "another output"
        self.manifest = self.base / "another manifest.json"
        relocated = self.base / "another source"
        self.source.rename(relocated)
        self.source = relocated
        with mock.patch.object(bundle, "_git_metadata", return_value=("unknown", "unknown")):
            second = self.build()
        self.assertEqual(first["files"], second["files"])
        self.assertEqual(first["content_sha256"], second["content_sha256"])
        self.assertNotEqual(first["source_revision"], second["source_revision"])

    def test_excluded_development_changes_do_not_change_bundle_identity(self) -> None:
        first = self.build()
        (self.source / "README.md").write_text("Evaluator notes that must not be copied.\n")
        (self.source / "tests").mkdir()
        (self.source / "tests/grader.py").write_text("secret = 'not a runtime input'\n")
        self.output = self.base / "second output"
        self.manifest = self.base / "second manifest.json"
        self.assertEqual(first["content_sha256"], self.build()["content_sha256"])
        self.assertFalse((self.output / "README.md").exists())
        self.assertFalse((self.output / "evals").exists())
        self.assertFalse((self.output / "tests").exists())

    def test_changed_runtime_bytes_change_identity_without_normalization(self) -> None:
        first = self.build()
        changed = self.source / "PRIVACY.md"
        changed.write_bytes(changed.read_bytes() + b"\r\nByte-preserved extra line.\r\n")
        self.output = self.base / "second output"
        self.manifest = self.base / "second manifest.json"
        second = self.build()
        self.assertNotEqual(first["content_sha256"], second["content_sha256"])
        self.assertEqual(changed.read_bytes(), (self.output / "PRIVACY.md").read_bytes())

    def test_malformed_allowlist_is_rejected_before_copy(self) -> None:
        for bad in [None, [], {"schema_version": True, "files": []}, {"schema_version": 2, "files": []}, {"schema_version": 1, "files": "*"}]:
            with self.subTest(bad=bad):
                self.change_allowlist(bad)
                self.reject("ALLOWLIST_INVALID")
        (self.source / "evals/runtime-files.json").write_text("{invalid")
        self.reject("ALLOWLIST_INVALID")

    def test_duplicate_noncanonical_traversal_and_absolute_entries_are_rejected(self) -> None:
        for extra in ["agent-skills/solve/SKILL.md", "agent-skills/./solve/SKILL.md", "agent-skills//solve/SKILL.md", "../outside.md", "/tmp/secret.md", "C:/secret.md", "agent-skills\\solve\\SKILL.md"]:
            with self.subTest(extra=extra):
                self.change_allowlist({"schema_version": 1, "files": sorted([*self.allowlist["files"], extra])})
                self.reject("ALLOWLIST_INVALID")

    def test_prohibited_development_and_evaluator_entries_are_rejected(self) -> None:
        for extra in ["README.md", "TESTING.md", "evals/portable/v2/cases.json", "evals/runtime-files.json", "tests/test_eval_bundle.py", "tools/eval_bundle.py", "docs/superpowers/specs/contract.md", ".git/config"]:
            with self.subTest(extra=extra):
                self.change_allowlist({"schema_version": 1, "files": sorted([*self.allowlist["files"], extra])})
                self.reject("ALLOWLIST_INVALID")

    def test_omitted_runtime_entry_and_unsorted_allowlist_are_rejected(self) -> None:
        self.change_allowlist({"schema_version": 1, "files": self.allowlist["files"][:-1]})
        self.reject("ALLOWLIST_INVALID")
        self.change_allowlist({"schema_version": 1, "files": list(reversed(self.allowlist["files"]))})
        self.reject("ALLOWLIST_INVALID")

    def test_missing_source_root_and_allowlist_are_rejected(self) -> None:
        original = self.source
        self.source = self.base / "missing source"
        self.reject("SOURCE_MISSING")
        self.source = original
        (self.source / "evals/runtime-files.json").unlink()
        self.reject("SOURCE_MISSING")

    def test_missing_late_runtime_input_is_detected_before_any_copy(self) -> None:
        (self.source / self.allowlist["files"][-1]).unlink()
        self.reject("SOURCE_MISSING")

    def test_source_root_and_ancestor_symlinks_are_rejected(self) -> None:
        original = self.source
        alias = self.base / "source alias"
        alias.symlink_to(original, target_is_directory=True)
        self.source = alias
        self.reject("SOURCE_SYMLINK")
        outer = self.base / "outer alias"
        outer.symlink_to(self.base, target_is_directory=True)
        self.source = outer / original.name
        self.reject("SOURCE_SYMLINK")

    def test_source_file_directory_and_allowlist_symlinks_are_rejected(self) -> None:
        target = self.source / "PRIVACY.md"
        outside = self.base / "outside.md"
        outside.write_bytes(target.read_bytes())
        target.unlink()
        target.symlink_to(outside)
        self.reject("SOURCE_SYMLINK")
        target.unlink()
        target.write_bytes(outside.read_bytes())
        directory = self.source / "agent-skills/analogize"
        moved = self.base / "moved skill"
        directory.rename(moved)
        directory.symlink_to(moved, target_is_directory=True)
        self.reject("SOURCE_SYMLINK")
        directory.unlink()
        moved.rename(directory)
        allowlist_path = self.source / "evals/runtime-files.json"
        outside_json = self.base / "outside.json"
        outside_json.write_bytes(allowlist_path.read_bytes())
        allowlist_path.unlink()
        allowlist_path.symlink_to(outside_json)
        self.reject("SOURCE_SYMLINK")

    def test_broken_local_link_and_excluded_reference_are_rejected(self) -> None:
        target = self.source / "agent-skills/solve/SKILL.md"
        original = target.read_text()
        for reference in ["references/missing.md", "../../README.md", "/tmp/outside.md", "../../../outside.md"]:
            with self.subTest(reference=reference):
                target.write_text(original + f"\nRead [required]({reference}).\n")
                self.reject("RESOURCE_MISSING")

    def test_broken_wrapper_and_inline_runtime_references_are_rejected(self) -> None:
        wrapper = self.source / "adapters/claude/skills/solve/SKILL.md"
        original = wrapper.read_text()
        wrapper.write_text(original.replace("/agent-skills/solve/SKILL.md", "/agent-skills/missing/SKILL.md"))
        self.reject("RESOURCE_MISSING")
        wrapper.write_text(original)
        router = self.source / "agent-skills/solve/SKILL.md"
        router.write_text(router.read_text().replace("`references/workflow-contract.md`", "`references/missing.md`"))
        self.reject("RESOURCE_MISSING")

    def test_missing_manifest_skill_directory_is_rejected(self) -> None:
        manifest = self.source / ".codex-plugin/plugin.json"
        data = json.loads(manifest.read_text())
        data["skills"] = "./missing-skills/"
        manifest.write_text(json.dumps(data))
        self.reject("RESOURCE_MISSING")

    def test_output_and_manifest_cannot_be_inside_source_or_each_other(self) -> None:
        output, manifest = self.output, self.manifest
        for bad_output, bad_manifest in [
            (self.source / "bundle", manifest), (output, self.source / "manifest.json"),
            (output, output / "manifest.json"), (output, output),
            (self.base / "parent/child", self.base / "parent"),
        ]:
            with self.subTest(output=bad_output, manifest=bad_manifest):
                self.output, self.manifest = bad_output, bad_manifest
                self.reject("DESTINATION_INVALID")

    def test_resolved_destination_alias_cannot_hide_source_containment(self) -> None:
        alias = self.base / "destination alias"
        alias.symlink_to(self.source, target_is_directory=True)
        self.output = alias / "new bundle"
        self.reject("DESTINATION_INVALID")

    def test_nonempty_or_incomplete_output_is_preserved(self) -> None:
        self.output.mkdir()
        marker = self.output / "incomplete-build.txt"
        marker.write_bytes(b"Existing work must survive.\n")
        with self.assertRaises(bundle.BundleError) as caught:
            self.build()
        self.assertEqual("DESTINATION_INVALID", caught.exception.code)
        self.assertEqual(b"Existing work must survive.\n", marker.read_bytes())
        self.assertEqual([marker], list(self.output.iterdir()))
        self.assertFalse(self.manifest.exists())

    def test_existing_manifest_file_or_directory_is_preserved(self) -> None:
        self.manifest.write_bytes(b"Existing evidence.\n")
        with self.assertRaises(bundle.BundleError) as caught:
            self.build()
        self.assertEqual("DESTINATION_INVALID", caught.exception.code)
        self.assertEqual(b"Existing evidence.\n", self.manifest.read_bytes())
        self.assertFalse(self.output.exists())
        self.manifest.unlink()
        self.manifest.mkdir()
        with self.assertRaises(bundle.BundleError) as caught:
            self.build()
        self.assertEqual("DESTINATION_INVALID", caught.exception.code)
        self.assertTrue(self.manifest.is_dir())

    def test_existing_empty_output_is_usable(self) -> None:
        self.output.mkdir()
        inode = self.output.stat().st_ino
        self.build()
        self.assertEqual(inode, self.output.stat().st_ino)

    def test_destination_symlinks_are_preserved_and_rejected(self) -> None:
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        self.output.symlink_to(elsewhere, target_is_directory=True)
        with self.assertRaises(bundle.BundleError) as caught:
            self.build()
        self.assertEqual("DESTINATION_INVALID", caught.exception.code)
        self.assertTrue(self.output.is_symlink())
        self.assertEqual([], list(elsewhere.iterdir()))
        self.assertFalse(self.manifest.exists())

    def test_copy_failure_cleans_only_owned_files_and_preserves_empty_output(self) -> None:
        self.output.mkdir()
        inode = self.output.stat().st_ino
        original_write = bundle._write_file
        calls = 0

        def failing_write(path, data, created_files):
            nonlocal calls
            calls += 1
            original_write(path, data, created_files)
            if calls == 3:
                raise OSError("injected partial copy failure")

        with mock.patch.object(bundle, "_write_file", side_effect=failing_write):
            with self.assertRaises(bundle.BundleError) as caught:
                self.build()
        self.assertEqual("COPY_FAILED", caught.exception.code)
        self.assertTrue(self.output.is_dir())
        self.assertEqual(inode, self.output.stat().st_ino)
        self.assertEqual([], list(self.output.iterdir()))
        self.assertFalse(self.manifest.exists())

    def test_manifest_publication_failure_leaves_no_complete_artifact(self) -> None:
        with mock.patch.object(bundle.os, "link", side_effect=OSError("injected publish failure")):
            self.reject("COPY_FAILED")
        self.assertEqual([], list(self.base.glob(".ultrasolve-manifest-*")))

    def test_reference_style_local_dependency_is_not_omitted_from_closure(self) -> None:
        target = self.source / "agent-skills/solve/SKILL.md"
        target.write_text(target.read_text() + "\nRequired: read [extra instructions][extra].\n\n[extra]: ../../README.md\n")
        self.reject("RESOURCE_MISSING")

    def test_reference_style_included_dependency_and_external_citation_are_valid(self) -> None:
        target = self.source / "agent-skills/solve/SKILL.md"
        target.write_text(target.read_text() + "\nRead [the contract][workflow] and [background][source].\n\n[workflow]: <references/workflow-contract.md>\n[source]: https://example.invalid/background\n")
        self.assertEqual(42, len(self.build()["files"]))

    def test_undefined_explicit_reference_link_is_rejected(self) -> None:
        target = self.source / "agent-skills/solve/SKILL.md"
        target.write_text(target.read_text() + "\nRead [required instructions][missing-definition].\n")
        self.reject("RESOURCE_MISSING")

    def test_loader_targets_must_be_local_and_have_the_required_file_kind(self) -> None:
        manifest = self.source / ".codex-plugin/plugin.json"
        original = manifest.read_bytes()
        data = json.loads(original)
        data["skills"] = "https://example.invalid/skills/"
        manifest.write_text(json.dumps(data))
        self.reject("RESOURCE_MISSING")
        manifest.write_bytes(original)
        wrapper = self.source / "adapters/claude/skills/solve/SKILL.md"
        wrapper.write_text(wrapper.read_text().replace("/agent-skills/solve/SKILL.md", "/agent-skills/solve/"))
        self.reject("RESOURCE_MISSING")

    def test_failure_after_manifest_publication_removes_our_published_inode(self) -> None:
        real_link = bundle.os.link

        def publish_then_fail(source, destination):
            real_link(source, destination)
            raise OSError("injected failure after publication took effect")

        with mock.patch.object(bundle.os, "link", side_effect=publish_then_fail):
            self.reject("COPY_FAILED")
        self.assertEqual([], list(self.base.glob(".ultrasolve-manifest-*")))

    def test_failed_publication_preserves_an_unrelated_late_manifest(self) -> None:
        real_link = bundle.os.link

        def another_writer_wins(source, destination):
            Path(destination).write_bytes(b"Unrelated manifest must survive.\n")
            return real_link(source, destination)

        with mock.patch.object(bundle.os, "link", side_effect=another_writer_wins):
            with self.assertRaises(bundle.BundleError) as caught:
                self.build()
        self.assertEqual("COPY_FAILED", caught.exception.code)
        self.assertEqual(b"Unrelated manifest must survive.\n", self.manifest.read_bytes())
        self.assertFalse(self.output.exists())

    def test_missing_destination_parents_are_created_after_validation(self) -> None:
        self.output = self.base / "new parents/runtime"
        self.manifest = self.base / "new evidence/manifest.json"
        self.build()
        self.assertTrue(self.output.is_dir())
        self.assertTrue(self.manifest.is_file())

    def test_cli_success_reports_composition_without_claiming_isolation(self) -> None:
        completed = subprocess.run([sys.executable, "-B", str(TOOL_PATH), "--source", str(self.source), "--output", str(self.output), "--manifest-output", str(self.manifest)], capture_output=True, text=True, check=False)
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("bundle composition verified", completed.stdout)
        self.assertNotIn("isolation verified", completed.stdout)
        self.assertTrue(self.manifest.is_file())

    def test_cli_rejected_build_exits_two_without_manifest(self) -> None:
        (self.source / "PRIVACY.md").unlink()
        completed = subprocess.run([sys.executable, "-B", str(TOOL_PATH), "--source", str(self.source), "--output", str(self.output), "--manifest-output", str(self.manifest)], capture_output=True, text=True, check=False)
        self.assertEqual(2, completed.returncode)
        self.assertIn("SOURCE_MISSING", completed.stderr)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.manifest.exists())


if __name__ == "__main__":
    unittest.main()
