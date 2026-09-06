"""Deterministic contract for Ultrasolve's portable and native surfaces."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

if __package__:
    from tests.contract_support import (
        ISSUE_CODES, audit_runtime_contract, frontmatter, markdown_links, read_text,
        runtime_relative_paths, simple_yaml_sections, wrapper_delegates_to,
    )
else:
    from contract_support import (
        ISSUE_CODES, audit_runtime_contract, frontmatter, markdown_links, read_text,
        runtime_relative_paths, simple_yaml_sections, wrapper_delegates_to,
    )


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PORTABLE_ROOT = PLUGIN_ROOT / "agent-skills"
CLAUDE_SKILLS_ROOT = PLUGIN_ROOT / "adapters/claude/skills"

SKILLS = (
    "solve",
    "define",
    "simplify",
    "analogize",
    "restate",
    "generalize",
    "decompose",
    "invert",
)
MODEL_INVOCABLE = SKILLS[:2]
LEAVES = SKILLS[2:]
CLAUDE_SKILL_EVAL_CASES = {
    "activation",
    "router-read-order",
    "map-back",
    "define",
    "define-activation",
    "define-nonactivation",
    *LEAVES,
}
class PortabilityContractTestCase(unittest.TestCase):
    def portable_skill(self, name: str) -> Path:
        return PORTABLE_ROOT / name / "SKILL.md"

    def claude_wrapper(self, name: str) -> Path:
        return CLAUDE_SKILLS_ROOT / name / "SKILL.md"


class TestPortableSkillCorpus(PortabilityContractTestCase):
    def test_portable_collection_has_exact_skill_surface(self) -> None:
        self.assertTrue(PORTABLE_ROOT.is_dir(), "portable Agent Skills collection is required")
        actual = {path.name for path in PORTABLE_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(set(SKILLS), actual)
        for name in SKILLS:
            self.assertTrue(self.portable_skill(name).is_file(), f"missing portable skill: {name}")

    def test_portable_frontmatter_is_agent_skills_compatible(self) -> None:
        for name in SKILLS:
            path = self.portable_skill(name)
            self.assertTrue(path.is_file(), f"missing portable skill: {path}")
            fields = frontmatter(path)
            self.assertEqual({"name", "description"}, set(fields), f"nonportable fields in {path}")
            self.assertEqual(name, fields["name"])
            self.assertRegex(fields["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
            self.assertLessEqual(len(fields["name"]), 64)
            self.assertGreaterEqual(len(fields["description"]), 1)
            self.assertLessEqual(len(fields["description"]), 1024)

    def test_portable_relative_markdown_resources_resolve(self) -> None:
        self.assertTrue(PORTABLE_ROOT.is_dir(), "portable Agent Skills collection is required")
        link_pattern = re.compile(r"!?(?:\[[^\]]*\])\((?P<target>[^)]+)\)")
        for path in PORTABLE_ROOT.rglob("*.md"):
            for match in link_pattern.finditer(read_text(path)):
                target = match.group("target").strip().strip("<>").split("#", 1)[0]
                if not target or re.match(r"(?:[a-z]+:|//)", target, re.I):
                    continue
                self.assertTrue(
                    (path.parent / target).is_file(),
                    f"unresolved portable Markdown resource in {path}: {target}",
                )

    def test_no_default_skills_directory_can_be_double_discovered(self) -> None:
        self.assertFalse(
            (PLUGIN_ROOT / "skills").exists(),
            "native adapters require the default skills directory to be absent",
        )

    def test_shared_references_are_owned_by_portable_router(self) -> None:
        references = PORTABLE_ROOT / "solve/references"
        self.assertTrue(references.is_dir())
        self.assertEqual(
            {"workflow-contract.md", "technique-selection.md", "shannon-source-notes.md", "worked-examples.md"},
            {path.name for path in references.iterdir() if path.is_file()},
        )
        self.assertEqual({"methods"}, {path.name for path in references.iterdir() if path.is_dir()})
        self.assertEqual({f"{leaf}.md" for leaf in LEAVES}, {path.name for path in (references / "methods").iterdir()})
        self.assertEqual({"problem-posing-sources.md", "worked-example.md"}, {path.name for path in (PORTABLE_ROOT / "define/references").iterdir()})
        self.assertFalse((PLUGIN_ROOT / "references").exists())

    def test_portable_corpus_has_no_host_specific_instructions(self) -> None:
        self.assertTrue(PORTABLE_ROOT.is_dir(), "portable Agent Skills collection is required")
        text = "\n".join(
            read_text(path)
            for path in PORTABLE_ROOT.rglob("*.md")
            if path.is_file()
        )
        folded = text.casefold()
        for forbidden in (
            "${claude_plugin_root}",
            "/ultrasolve:",
            "claude code",
            "codex",
            "plugin",
            "skill tool",
            "read tool",
        ):
            self.assertNotIn(forbidden, folded, f"portable corpus contains host coupling: {forbidden}")

    def test_router_defines_module_dispatch_and_full_preflight(self) -> None:
        router = re.sub(r"\s+", " ", read_text(self.portable_skill("solve")).lower())
        for required in ("collection root", "eighteen resources", "existence, accessibility, and readability", "unselected entries and modules", "collection-integrity error", "before any candidate or transformation"):
            self.assertIn(required, router)
        for leaf in LEAVES:
            self.assertIn(f"references/methods/{leaf}.md", router)
            self.assertNotIn(f"../{leaf}/skill.md", router)
        self.assertIn("do not invoke public leaf commands or read their entrypoints as a loading fallback", router)
        self.assertIn("native command loader is unnecessary", router)
        self.assertIn("missing or denied module access ends that path", router)
        self.assertIn("do not use aliases, copies, relocated instructions", router)
        self.assertLess(router.index("integrity preflight"), router.index("**diagnose.**"))

    def test_direct_leaf_invocation_loads_shared_contract_and_full_module(self) -> None:
        for leaf in LEAVES:
            text = read_text(self.portable_skill(leaf))
            links = markdown_links(text)
            self.assertIn("../solve/references/workflow-contract.md", links)
            self.assertIn(f"../solve/references/methods/{leaf}.md", links)
            normalized = re.sub(r"\s+", " ", text).lower()
            for boundary in ("explicit applicable method request", "does not require repeated failure", "pure ideation", "reproducible failure", "evidence-led diagnosis", "open/assumed", "remaining effort"):
                self.assertIn(boundary, normalized)
            self.assertIn("both required resources must load successfully", normalized)
            self.assertIn("a denial ends that path", normalized)
            self.assertNotIn("## full method", normalized)


class TestClaudeAdapter(PortabilityContractTestCase):
    def test_claude_adapter_has_exact_thin_wrapper_surface(self) -> None:
        self.assertTrue(CLAUDE_SKILLS_ROOT.is_dir())
        actual = {path.name for path in CLAUDE_SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(set(SKILLS), actual)
        for name in SKILLS:
            path = self.claude_wrapper(name)
            fields = frontmatter(path)
            self.assertEqual(name, fields.get("name"))
            expected_keys = {"name", "description"}
            if name in LEAVES:
                expected_keys.add("disable-model-invocation")
                self.assertEqual("true", fields.get("disable-model-invocation"))
            self.assertEqual(expected_keys, set(fields))
            self.assertEqual(frontmatter(self.portable_skill(name))["description"], fields["description"])
            target = f"${{CLAUDE_PLUGIN_ROOT}}/agent-skills/{name}/SKILL.md"
            self.assertTrue(wrapper_delegates_to(read_text(path), target), f"invalid wrapper delegation: {name}")

    def test_claude_manifest_loads_only_adapter_skills(self) -> None:
        path = PLUGIN_ROOT / ".claude-plugin/plugin.json"
        self.assertTrue(path.is_file(), "Claude manifest is required")
        manifest = json.loads(read_text(path))
        configured = manifest.get("skills")
        normalized = [configured] if isinstance(configured, str) else configured
        self.assertEqual(["./adapters/claude/skills/"], normalized)


class TestCodexAdapter(PortabilityContractTestCase):
    def test_codex_manifest_has_complete_public_interface(self) -> None:
        path = PLUGIN_ROOT / ".codex-plugin/plugin.json"
        self.assertTrue(path.is_file(), "Codex manifest is required")
        manifest = json.loads(read_text(path))
        self.assertEqual("ultrasolve", manifest.get("name"))
        self.assertEqual("0.3.0", manifest.get("version"))
        self.assertEqual("Rigorous methods for solving the hardest problems.", manifest.get("description"))
        self.assertEqual("Matt Ramotar", manifest.get("author", {}).get("name"))
        self.assertEqual(
            {
                "problem-solving",
                "stuck",
                "reframing",
                "analogy",
                "inversion",
                "decomposition",
                "shannon-inspired",
            },
            set(manifest.get("keywords", [])),
        )
        self.assertEqual(7, len(manifest.get("keywords", [])))
        self.assertEqual("./agent-skills/", manifest.get("skills"))

        interface = manifest.get("interface", {})
        self.assertEqual("Ultrasolve", interface.get("displayName"))
        for field in ("shortDescription", "longDescription"):
            self.assertIsInstance(interface.get(field), str)
            self.assertTrue(interface[field].strip(), f"missing {field}")
        self.assertEqual("Matt Ramotar", interface.get("developerName"))
        self.assertEqual("Productivity", interface.get("category"))
        self.assertEqual(
            "https://github.com/matt-ramotar/Ultrasolve",
            interface.get("websiteURL"),
        )
        self.assertEqual(
            "https://github.com/matt-ramotar/Ultrasolve/blob/main/PRIVACY.md",
            interface.get("privacyPolicyURL"),
        )
        self.assertEqual(
            "https://github.com/matt-ramotar/plugins/blob/main/TERMS.md",
            interface.get("termsOfServiceURL"),
        )
        capabilities = interface.get("capabilities", [])
        self.assertEqual({"Reason", "Research", "Plan"}, set(capabilities))
        self.assertEqual(3, len(capabilities))

        prompts = interface.get("defaultPrompt", [])
        self.assertEqual(3, len(prompts))
        for skill, prompt in zip(("define", "solve", "invert"), prompts):
            self.assertIsInstance(prompt, str)
            self.assertIn(f"${skill}", prompt)
            self.assertGreater(len(prompt.split()), 5, "starter needs a useful input shape")

    def test_openai_metadata_preserves_router_only_implicit_activation(self) -> None:
        for name in SKILLS:
            path = PORTABLE_ROOT / name / "agents/openai.yaml"
            self.assertTrue(path.is_file(), f"missing OpenAI metadata: {path}")
            sections = simple_yaml_sections(path)
            self.assertEqual({"interface", "policy"}, set(sections))
            self.assertEqual(
                {"display_name", "short_description", "default_prompt"},
                set(sections["interface"]),
            )
            for value in sections["interface"].values():
                self.assertTrue(value, f"empty OpenAI interface value in {path}")
            self.assertIn(f"${name}", sections["interface"]["default_prompt"])
            self.assertEqual({"allow_implicit_invocation"}, set(sections["policy"]))
            expected = "true" if name in MODEL_INVOCABLE else "false"
            self.assertEqual(expected, sections["policy"]["allow_implicit_invocation"])

    def test_standalone_marketplace_exposes_root_plugin(self) -> None:
        claude_path = PLUGIN_ROOT / ".claude-plugin/marketplace.json"
        self.assertTrue(claude_path.is_file(), "Claude marketplace manifest is required")
        marketplace = json.loads(read_text(claude_path))
        self.assertEqual(
            "https://json.schemastore.org/claude-code-marketplace.json",
            marketplace.get("$schema"),
        )
        self.assertEqual("matt-ramotar", marketplace.get("name"))
        self.assertEqual("0.3.0", marketplace.get("version"))
        self.assertEqual("Matt Ramotar", marketplace.get("owner", {}).get("name"))
        entries = marketplace.get("plugins", [])
        self.assertEqual(1, len(entries), "standalone marketplace must expose one plugin")
        entry = entries[0]
        self.assertEqual("ultrasolve", entry.get("name"))
        self.assertEqual("./", entry.get("source"))
        self.assertEqual("productivity", entry.get("category"))
        self.assertNotIn("version", entry)

        codex_path = PLUGIN_ROOT / ".agents/plugins/marketplace.json"
        self.assertTrue(codex_path.is_file(), "Codex marketplace manifest is required")
        codex_marketplace = json.loads(read_text(codex_path))
        self.assertEqual("matt-ramotar", codex_marketplace.get("name"))
        self.assertEqual("Matt Ramotar", codex_marketplace.get("owner", {}).get("name"))
        codex_entries = codex_marketplace.get("plugins", [])
        self.assertEqual(1, len(codex_entries), "Codex marketplace must expose one plugin")
        self.assertEqual(
            {
                "name": "ultrasolve",
                "source": {"source": "local", "path": "./"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            },
            codex_entries[0],
        )


class TestPortableEvaluationContract(PortabilityContractTestCase):
    """Immutable v1 fixture packaging and current docs, not measured behavior."""
    def test_activation_matrix_covers_portable_behavioral_boundary(self) -> None:
        path = PLUGIN_ROOT / "evals/portable/v1/activation-tests.md"
        self.assertTrue(path.is_file(), "provider-neutral activation matrix is required")
        text = read_text(path).lower()
        forbidden_terms = (
            "claude",
            "codex",
            "openai",
            "/ultrasolve:",
            "${claude_plugin_root}",
            "skill tool",
            "read tool",
        )
        for forbidden in (*forbidden_terms, *(f"${name}" for name in SKILLS)):
            self.assertNotIn(forbidden, text, f"activation matrix is not provider-neutral: {forbidden}")
        case_ids = (
            "automatic-solve",
            "ordinary-nonactivation",
            "debugging-boundary",
            *(f"explicit-{leaf}" for leaf in LEAVES),
            "router-selection",
            "automatic-define",
            "direct-define",
            "define-nonactivation",
            "define-delegated-nonactivation",
            "map-back",
        )
        for case_id in case_ids:
            self.assertEqual(1, text.count(f"`{case_id}`"), f"missing distinct case: {case_id}")
            section_match = re.search(
                rf"(?ms)^## [`]{re.escape(case_id)}[`]\s*$"
                rf"(?P<body>.*?)(?=^## |\Z)",
                text,
            )
            self.assertIsNotNone(section_match, f"missing matrix section: {case_id}")
            body = section_match.group("body") if section_match else ""
            stimulus_match = re.search(r"(?m)^stimulus:\s*(?P<stimulus>\S.*)$", body)
            self.assertIsNotNone(stimulus_match, f"missing reproducible stimulus: {case_id}")
            stimulus = stimulus_match.group("stimulus") if stimulus_match else ""
            self.assertGreaterEqual(len(stimulus), 140, f"stimulus is not exact enough: {case_id}")
            self.assertNotRegex(
                stimulus,
                r"^(?:present|ask|report|supply|through)\b",
                f"stimulus is a prompt-writing instruction, not an exact prompt: {case_id}",
            )
            outcome_match = re.search(r"(?m)^expected outcome:\s*(?P<outcome>\S.*)$", body)
            self.assertIsNotNone(outcome_match, f"missing nonempty outcome: {case_id}")
            outcome = outcome_match.group("outcome") if outcome_match else ""
            if case_id.startswith("explicit-"):
                self.assertIn("explicit invocation", body, f"leaf is not explicitly invoked: {case_id}")
                leaf = case_id.removeprefix("explicit-")
                self.assertIn(leaf, stimulus)
                self.assertIn("explicit invocation", stimulus)
                self.assertIn(leaf, outcome)
                self.assertRegex(outcome, r"(?:load|apply|execute)")
                self.assertRegex(outcome, r"(?:not|never).{0,40}automatic")
            elif case_id == "automatic-solve":
                self.assertRegex(stimulus, r"(?:three|3).{0,80}(?:failed|failures)")
                self.assertRegex(outcome, r"(?:router|solve).{0,80}(?:activate|invoke).{0,80}automatic")
                self.assertIn("stuck", outcome)
            elif case_id == "ordinary-nonactivation":
                self.assertIn("clamp", stimulus)
                self.assertRegex(outcome, r"(?:router|solve).{0,80}(?:not|never).{0,40}activat")
                self.assertRegex(outcome, r"(?:ordinary|single failed attempt)")
            elif case_id == "debugging-boundary":
                self.assertIn("reproducible", stimulus)
                self.assertRegex(stimulus, r"(?:logs|traces).{0,120}(?:missing|does not record)")
                self.assertRegex(outcome, r"(?:router|solve).{0,80}(?:not|never).{0,40}activat")
                self.assertIn("evidence-led diagnosis", outcome)
            elif case_id == "router-selection":
                self.assertRegex(stimulus, r"(?:three|3).{0,80}(?:failed|approaches)")
                self.assertRegex(outcome, r"select.{0,80}(?:one to three|1-3).{0,80}(?:leaf|leaves)")
                self.assertRegex(outcome, r"(?:load|read).{0,80}(?:selected|sibling)")
            elif case_id == "automatic-define":
                self.assertRegex(stimulus, r"approved.{0,160}(?:plan|rewrit(?:e|ing)|migration)")
                self.assertEqual(
                    "the definition method activates automatically for the "
                    "solution-shaped request and returns a problem contract with "
                    "observable success criteria and a decision point, not the "
                    "requested rewrite plan.",
                    outcome,
                )
                self.assertRegex(outcome, r"definition method.{0,80}activates? automatic")
                self.assertRegex(outcome, r"problem contract")
                self.assertRegex(outcome, r"(?:not|instead of).{0,60}(?:plan|rewrite)")
            elif case_id == "direct-define":
                self.assertIn("define", stimulus)
                self.assertIn("direct invocation", stimulus)
                self.assertEqual(
                    "the definition method define loads and applies its full method, "
                    "producing a problem contract whose candidate register carries "
                    "the approved migration as one row among alternatives.",
                    outcome,
                )
                self.assertIn("define", outcome)
                self.assertRegex(outcome, r"(?:load|apply|execute)")
                self.assertRegex(outcome, r"problem contract")
            elif case_id == "define-nonactivation":
                self.assertRegex(stimulus, r"already agreed.{0,120}success criteria")
                self.assertEqual(
                    "the definition method does not activate; the defined problem is "
                    "worked directly or routed toward reformulation of its formulation "
                    "rut.",
                    outcome,
                )
                self.assertRegex(outcome, r"definition method.{0,60}(?:not|never).{0,40}activat")
                self.assertRegex(outcome, r"(?:reformulation|worked directly|defined problem)")
            elif case_id == "define-delegated-nonactivation":
                self.assertIn("complete, reviewed specification", stimulus)
                self.assertNotIn("attached", stimulus)
                self.assertNotIn("given", stimulus)
                for concrete_value in (
                    "m7i.large",
                    "m7i.xlarge",
                    "c7i.2xlarge",
                    "3 to 6",
                    "6 to 24",
                    "0 to 40",
                    "kubernetes 1.33",
                ):
                    self.assertIn(concrete_value, stimulus)
                self.assertEqual(
                    "the definition method does not activate for the fully specified "
                    "request; the task proceeds as ordinary work.",
                    outcome,
                )
                self.assertRegex(outcome, r"definition method.{0,60}(?:not|never).{0,40}activat")
                self.assertRegex(outcome, r"ordinary work")
            elif case_id == "map-back":
                self.assertIn("explicit invocation", stimulus)
                self.assertRegex(stimulus, r"(?:zero changes|rollback).{0,120}(?:rollback|zero changes)")
                self.assertRegex(outcome, r"map.{0,20}back.{0,100}original problem")
                self.assertRegex(outcome, r"constraints.{0,100}success criteria")

    def test_claude_skill_fixtures_allow_wrapper_core_reads(self) -> None:
        # v1 is historical native fixture packaging, not the revised behavioral oracle.
        fixtures = PLUGIN_ROOT / "evals/behavioral/v1"
        self.assertTrue(fixtures.is_dir())
        for case in CLAUDE_SKILL_EVAL_CASES:
            prompt = fixtures / case / "prompt.md"
            self.assertTrue(prompt.is_file())
            self.assertRegex(frontmatter(prompt).get("allowed_tools", ""), r"\bRead\b")
        testing = read_text(PLUGIN_ROOT / "TESTING.md")
        for path in ("evals/runtime-files.json", "evals/runner-feasibility.md", "evals/portable/v2/cases.json"):
            self.assertIn(path, markdown_links(testing))
        self.assertIn("python3 tools/check.py", testing)
        self.assertIn("python3 tools/eval_bundle.py", testing)
        normalized = re.sub(r"\s+", " ", testing).lower()
        self.assertIn("composition", normalized)
        self.assertIn("isolation", normalized)
        self.assertIn("historical", normalized)
        self.assertIn("authorization", normalized)

    def test_installation_docs_match_the_standalone_tree(self) -> None:
        readme = read_text(PLUGIN_ROOT / "README.md")
        standalone_root = "/absolute/path/to/Ultrasolve"
        self.assertGreaterEqual(readme.count(standalone_root), 3)
        self.assertNotIn("/absolute/path/to/plugins", readme)
        normalized = re.sub(r"\s+", " ", readme)
        self.assertIn("Version `0.3.0`", normalized)
        self.assertRegex(normalized, r"(?i)eight.{0,80}(?:agent )?skills")
        self.assertIn("/ultrasolve:define", readme)


class TestMigrationCoherence(PortabilityContractTestCase):
    def test_actual_runtime_satisfies_structural_obligations(self) -> None:
        # The mutation suite exercises these issue codes against changed files.
        # This replaces a test-name lock; the external migration receipt maps all 57 obligations.
        self.assertEqual({
            "ENTRYPOINT_SET", "WRAPPER_TARGET", "ACTIVATION_POLICY", "DESCRIPTION_PARITY",
            "VERSION_PARITY", "RESOURCE_MISSING", "METHOD_BODY_DUPLICATED",
        }, ISSUE_CODES)
        self.assertEqual([], audit_runtime_contract(PLUGIN_ROOT))
        relatives = runtime_relative_paths()
        self.assertEqual(42, len(relatives))
        self.assertEqual(len(relatives), len(set(relatives)))
        for relative in relatives:
            self.assertTrue((PLUGIN_ROOT / relative).is_file(), f"missing runtime obligation: {relative}")


if __name__ == "__main__":
    unittest.main()
