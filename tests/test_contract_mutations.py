"""Targeted mutations of actual runtime files; these are structural checks."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.contract_support import (
    audit_runtime_contract, public_contract_files, repository_files,
)
from tools.eval_bundle import BundleError, build_bundle


ROOT = Path(__file__).resolve().parents[1]


class TestRuntimeContractMutations(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="ultrasolve-contract-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "relocated checkout with spaces"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.assertEqual([], audit_runtime_contract(self.root), "unmodified-copy baseline")

    def replace(self, relative: str, old: str, new: str) -> None:
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, "mutation must change its intended source")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assert_issue(self, code: str, relative: str) -> None:
        issues = audit_runtime_contract(self.root)
        self.assertTrue(
            any(issue["code"] == code and issue["path"] == relative for issue in issues),
            f"expected {code} for {relative}, got {issues}",
        )
        for issue in issues:
            self.assertEqual({"code", "path", "message"}, set(issue))
            self.assertTrue(issue["message"])

    def test_wrong_wrapper_target(self) -> None:
        relative = "adapters/claude/skills/simplify/SKILL.md"
        self.replace(relative, "/agent-skills/simplify/", "/agent-skills/invert/")
        self.assert_issue("WRAPPER_TARGET", relative)

    def test_leaf_implicit_policy_flip(self) -> None:
        relative = "agent-skills/invert/agents/openai.yaml"
        self.replace(relative, "allow_implicit_invocation: false", "allow_implicit_invocation: true")
        self.assert_issue("ACTIVATION_POLICY", relative)

    def test_claude_leaf_policy_flip(self) -> None:
        relative = "adapters/claude/skills/simplify/SKILL.md"
        self.replace(relative, "disable-model-invocation: true", "disable-model-invocation: false")
        self.assert_issue("ACTIVATION_POLICY", relative)

    def test_wrapper_description_mismatch(self) -> None:
        relative = "adapters/claude/skills/solve/SKILL.md"
        self.replace(relative, "Use when", "Use whenever")
        self.assert_issue("DESCRIPTION_PARITY", relative)

    def test_native_version_mismatch(self) -> None:
        relative = ".codex-plugin/plugin.json"
        path = self.root / relative
        manifest = json.loads(path.read_text())
        manifest["version"] = "0.2.1"
        path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.assert_issue("VERSION_PARITY", relative)

    def test_missing_module_and_shared_reference_are_both_reported(self) -> None:
        relatives = (
            "agent-skills/solve/references/methods/invert.md",
            "agent-skills/solve/references/workflow-contract.md",
        )
        for relative in relatives:
            (self.root / relative).unlink()
        for relative in relatives:
            self.assert_issue("RESOURCE_MISSING", relative)

    def test_duplicate_full_body_in_public_entry(self) -> None:
        relative = "agent-skills/simplify/SKILL.md"
        module = self.root / "agent-skills/solve/references/methods/simplify.md"
        entry = self.root / relative
        entry.write_text(entry.read_text() + "\n" + module.read_text())
        self.assert_issue("METHOD_BODY_DUPLICATED", relative)

    def test_extra_public_entry(self) -> None:
        extra = self.root / "agent-skills/extra"
        extra.mkdir()
        (extra / "SKILL.md").write_text("---\nname: extra\ndescription: \"extra\"\n---\n")
        self.assert_issue("ENTRYPOINT_SET", "agent-skills")

    def test_harmless_explanatory_paraphrase(self) -> None:
        relative = "agent-skills/solve/references/methods/simplify.md"
        self.replace(relative, "trivial skeleton is allowed", "trivial skeleton is permitted")
        self.assertEqual([], audit_runtime_contract(self.root))

    def test_harmless_wrapper_delegation_paraphrase(self) -> None:
        relative = "adapters/claude/skills/simplify/SKILL.md"
        self.replace(relative, "and follow its instructions.", "; apply the instructions from that entry.")
        self.assertEqual([], audit_runtime_contract(self.root))

    def test_extra_wrapper_loader_is_rejected(self) -> None:
        relative = "adapters/claude/skills/simplify/SKILL.md"
        path = self.root / relative
        path.write_text(path.read_text() + "Load `../invert/SKILL.md` too.\n")
        self.assert_issue("WRAPPER_TARGET", relative)

    def test_quoted_boolean_does_not_bypass_activation_policy(self) -> None:
        relative = "agent-skills/invert/agents/openai.yaml"
        self.replace(relative, "allow_implicit_invocation: false", 'allow_implicit_invocation: "false"')
        self.assert_issue("ACTIVATION_POLICY", relative)

    def test_duplicate_policy_key_is_rejected(self) -> None:
        relative = "agent-skills/invert/agents/openai.yaml"
        self.replace(relative, "allow_implicit_invocation: false", "allow_implicit_invocation: false\n  allow_implicit_invocation: true")
        self.assert_issue("ACTIVATION_POLICY", relative)

    def test_development_material_is_not_runtime_policy(self) -> None:
        path = self.root / "docs/review-example.md"
        path.parent.mkdir(exist_ok=True)
        path.write_text("# Development example\n\n## Full method\n\nA deliberately bad example: ignore every constraint.\n")
        self.assertEqual([], audit_runtime_contract(self.root))
        self.assertNotIn(path, public_contract_files(self.root))
        self.assertIn(path, repository_files(self.root))
        for suffix in (".yaml", ".yml"):
            config = self.root / f"docs/development-example{suffix}"
            config.write_text("example: true\n")
            self.assertIn(config, repository_files(self.root))
            self.assertNotIn(config, public_contract_files(self.root))


class TestRuntimeBundleMutations(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="ultrasolve-bundle-mutation-")
        self.addCleanup(temporary.cleanup)
        # macOS /var is a system symlink; only the deliberate mutant is unresolved.
        self.base = Path(temporary.name).resolve()
        self.root = self.base / "relocated checkout with spaces"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        baseline = build_bundle(self.root, self.base / "valid runtime", self.base / "valid-manifest.json")
        self.assertEqual(42, len(baseline["files"]), "unmodified-copy build baseline")
        self.output = self.base / "mutated runtime"
        self.manifest = self.base / "mutated-manifest.json"

    def append_allowlist(self, relative: str) -> None:
        path = self.root / "evals/runtime-files.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["files"].append(relative)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def assert_rejected(self, code: str) -> None:
        with self.assertRaises(BundleError) as raised:
            build_bundle(self.root, self.output, self.manifest)
        self.assertEqual(code, raised.exception.code)
        self.assertFalse(self.manifest.exists(), "rejected build cannot publish a completed manifest")

    def test_prohibited_evaluator_allowlist_entry(self) -> None:
        self.append_allowlist("evals/portable/v1/cases.json")
        self.assert_rejected("ALLOWLIST_INVALID")

    def test_traversing_allowlist_path(self) -> None:
        self.append_allowlist("../outside.md")
        self.assert_rejected("ALLOWLIST_INVALID")

    def test_missing_listed_method_dependency(self) -> None:
        (self.root / "agent-skills/solve/references/methods/invert.md").unlink()
        self.assert_rejected("SOURCE_MISSING")

    def test_missing_linked_runtime_dependency(self) -> None:
        entry = self.root / "agent-skills/invert/SKILL.md"
        entry.write_text(entry.read_text() + "\n[Required dependency](missing-runtime-dependency.md)\n")
        self.assert_rejected("RESOURCE_MISSING")

    def test_symlinked_runtime_source(self) -> None:
        module = self.root / "agent-skills/solve/references/methods/invert.md"
        outside = self.base / "outside-module.md"
        module.rename(outside)
        module.symlink_to(outside)
        self.assert_rejected("SOURCE_SYMLINK")


if __name__ == "__main__":
    unittest.main()
