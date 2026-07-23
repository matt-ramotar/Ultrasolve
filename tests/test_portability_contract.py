"""Deterministic contract for Ultrasolve's portable and native surfaces."""

from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path


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
EXPECTED_LEGACY_TESTS = {
    "test_plugin_directory_has_final_path",
    "test_manifest_has_final_identity_and_source_faithful_description",
    "test_obsolete_plugin_directory_is_absent",
    "test_obsolete_canonical_doc_filenames_are_absent",
    "test_codex_and_claude_manifests_share_identity",
    "test_standalone_marketplace_publishes_ultrasolve",
    "test_public_structural_artifacts_have_only_canonical_identity",
    "test_readme_records_publication_hold",
    "test_skill_surface_is_exactly_the_entries_and_six_leaves",
    "test_command_wrappers_are_absent",
    "test_exactly_the_entries_are_model_invocable",
    "test_router_explicitly_loads_each_leaf_from_plugin_root",
    "test_router_enforces_the_shared_contract_and_map_back",
    "test_source_notes_preserve_corrected_publication_date_and_provenance_labels",
    "test_known_false_claims_are_not_shipped",
    "test_drr_credit_carry_is_conditioned_on_remaining_backlogged",
    "test_legacy_namespace_and_old_skill_structures_are_absent_from_public_surface",
    "test_every_leaf_has_the_shared_workflow_structure",
    "test_simplify_contract",
    "test_analogize_contract",
    "test_restate_contract",
    "test_generalize_contract",
    "test_decompose_contract",
    "test_invert_is_logically_safe_and_reenters_debugging",
    "test_define_skill_has_house_structure",
    "test_define_method_pins_ledger_marks_and_decision_point",
    "test_define_handoff_contract_is_lossless",
    "test_router_adopts_define_contract",
    "test_define_is_absent_from_lens_table",
    "test_define_provenance_disclaims_shannon",
    "test_readme_exposes_exactly_the_final_commands",
    "test_readme_links_standalone_testing_guidance",
    "test_relative_markdown_links_resolve_in_standalone_tree",
    "test_manual_only_eval_cases_begin_with_real_slash_invocation",
    "test_versioned_eval_fixtures_match_exact_native_shape",
    "test_read_enabled_eval_cases_block_reads_into_eval_tree",
    "test_semantic_regression_fixtures_are_evidence_faithful",
    "test_activation_and_boundary_fixtures_use_native_skill_trace_graders",
    "test_router_read_order_combines_deterministic_and_semantic_trace_checks",
    "test_text_artifacts_have_no_trailing_whitespace_and_one_final_newline",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def scalar(value: str, path: Path, context: str) -> str:
    """Parse the restricted scalar form used by the contract fixtures."""

    normalized = value.strip()
    if not normalized:
        return ""
    boolean_context = context == "disable-model-invocation" or context == (
        "policy.allow_implicit_invocation"
    )
    if boolean_context:
        if normalized not in {"true", "false"}:
            raise AssertionError(f"non-boolean YAML value in {path} ({context})")
        return normalized
    if normalized[0] in {'"', "'"}:
        quote = normalized[0]
        if len(normalized) < 2 or normalized[-1] != quote:
            raise AssertionError(f"unbalanced quoted scalar in {path} ({context})")
        if quote == '"':
            try:
                parsed = json.loads(normalized)
            except json.JSONDecodeError as error:
                raise AssertionError(
                    f"invalid double-quoted scalar in {path} ({context})"
                ) from error
            if not isinstance(parsed, str):
                raise AssertionError(f"nonscalar value in {path} ({context})")
            return parsed
        inner = normalized[1:-1]
        if "'" in inner.replace("''", ""):
            raise AssertionError(f"invalid single-quoted scalar in {path} ({context})")
        return inner.replace("''", "'")
    if normalized[-1] in {'"', "'"}:
        raise AssertionError(f"unbalanced quoted scalar in {path} ({context})")
    string_context = context in {"name", "description"} or context.startswith("interface.")
    if context == "description" or context.startswith("interface."):
        raise AssertionError(f"string must be quoted in {path} ({context})")
    if string_context and (
        normalized.casefold() in {"null", "~", "true", "false", ".nan", ".inf", "-.inf"}
        or normalized[0] in "[{|>&*!"
        or re.fullmatch(
            r"[-+]?(?:0[xX][0-9a-fA-F]+|0[oO][0-7]+|0[bB][01]+|"
            r"\d+(?:\.\d*)?(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)",
            normalized,
        )
        or re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}(?:[Tt ]\S+)?", normalized)
        or ": " in normalized
        or " #" in normalized
    ):
        raise AssertionError(f"non-string YAML value in {path} ({context})")
    return normalized


def frontmatter(path: Path) -> dict[str, str]:
    text = read_text(path)
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError(f"missing YAML frontmatter: {path}")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"unterminated YAML frontmatter: {path}") from error

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line.lstrip().startswith("#"):
            continue
        if line[0].isspace():
            raise AssertionError(f"nested frontmatter is not allowed in {path}: {line}")
        key, separator, value = line.partition(":")
        if not separator:
            raise AssertionError(f"invalid frontmatter line in {path}: {line}")
        normalized_key = key.strip()
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", normalized_key):
            raise AssertionError(f"unsupported or quoted frontmatter key in {path}: {key}")
        if normalized_key in fields:
            raise AssertionError(f"duplicate frontmatter key in {path}: {normalized_key}")
        fields[normalized_key] = scalar(value, path, normalized_key)
    return fields


def simple_yaml_sections(path: Path) -> dict[str, dict[str, str]]:
    """Parse the intentionally tiny two-level agents/openai.yaml shape."""

    sections: dict[str, dict[str, str]] = {}
    current: str | None = None
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if not line or line.lstrip().startswith("#"):
            continue
        indentation = len(line) - len(line.lstrip(" "))
        key, separator, value = line.strip().partition(":")
        if not separator:
            raise AssertionError(f"invalid YAML line in {path}:{number}: {line}")
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            raise AssertionError(f"unsupported or quoted YAML key in {path}:{number}: {key}")
        if indentation == 0 and not value.strip():
            if key in sections:
                raise AssertionError(f"duplicate YAML section in {path}: {key}")
            sections[key] = {}
            current = key
            continue
        if indentation != 2 or current is None:
            raise AssertionError(f"unsupported YAML structure in {path}:{number}: {line}")
        if key in sections[current]:
            raise AssertionError(f"duplicate YAML key in {path}: {current}.{key}")
        sections[current][key] = scalar(value, path, f"{current}.{key}")
    return sections


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
        self.assertTrue(references.is_dir(), "solve must own its portable references")
        self.assertEqual(
            {"technique-selection.md", "shannon-source-notes.md", "worked-examples.md"},
            {path.name for path in references.iterdir() if path.is_file()},
        )
        self.assertFalse((PLUGIN_ROOT / "references").exists(), "legacy root references must move")

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

    def test_router_defines_portable_dispatch_and_capability_fallbacks(self) -> None:
        router_path = self.portable_skill("solve")
        self.assertTrue(router_path.is_file(), f"missing portable router: {router_path}")
        router = re.sub(r"\s+", " ", read_text(router_path).lower())
        for required in ("collection root", "host-native", "sibling", "skill.md"):
            self.assertIn(required, router, f"portable router missing contract term: {required}")
        for leaf in LEAVES:
            self.assertEqual(
                1,
                router.count(f"../{leaf}/skill.md"),
                f"portable router must name one sibling dispatch target for {leaf}",
            )
        self.assertRegex(router, r"derive.{0,100}collection root.{0,100}(?:loaded|location)")
        self.assertRegex(
            router,
            r"host-native.{0,120}(?:loader|activation).{0,80}when available"
            r".{0,160}otherwise.{0,80}(?:read|load).{0,80}sibling",
        )
        self.assertRegex(router, r"(?:fail|stop|cannot continue).{0,120}(?:missing|incomplete)")
        self.assertRegex(router, r"(?:missing|incomplete).{0,160}(?:before|without).{0,80}(?:execute|apply)")
        for boundary in ("open-ended", "underspecified", "undefined"):
            self.assertIn(boundary, router)
        self.assertRegex(
            router,
            r"(?:underspecified|undefined|open-ended).{0,180}brainstorming"
            r".{0,80}when available.{0,160}otherwise"
            r".{0,80}(?:define|clarify).{0,80}locally",
        )
        self.assertRegex(
            router,
            r"missing facts.{0,160}(?:use|with).{0,80}research tools.{0,80}when available"
            r".{0,160}(?:otherwise|unavailable).{0,120}(?:ask|request)"
            r".{0,80}(?:user|missing facts)",
        )
        self.assertRegex(
            router,
            r"reproducible.{0,160}evidence-led diagnosis.{0,120}when available"
            r".{0,160}otherwise.{0,120}(?:conduct|perform|use).{0,80}(?:locally|local)",
        )
        self.assertRegex(
            router,
            r"all eight.{0,100}skill\.md.{0,120}(?:exist|present).{0,120}"
            r"(?:accessible|readable)",
        )
        self.assertRegex(
            router,
            r"all three.{0,100}(?:required )?references.{0,120}(?:exist|present)"
            r".{0,120}(?:accessible|readable)",
        )
        self.assertLess(router.index("integrity preflight"), router.index("**diagnose.**"))

    def test_direct_leaf_invocation_has_generic_capability_fallbacks(self) -> None:
        for leaf in LEAVES:
            text = re.sub(r"\s+", " ", read_text(self.portable_skill(leaf)).lower())
            for boundary in ("open-ended", "underspecified", "reproducible failure"):
                self.assertIn(boundary, text, f"{leaf} omits direct boundary: {boundary}")
            self.assertRegex(
                text,
                r"brainstorming.{0,80}when available.{0,160}otherwise"
                r".{0,100}(?:define|clarify).{0,80}locally",
            )
            self.assertRegex(
                text,
                r"research tools.{0,80}when available.{0,160}otherwise"
                r".{0,100}(?:ask|request).{0,80}(?:user|missing facts)",
            )
            self.assertRegex(
                text,
                r"reproducible failure.{0,160}evidence-led diagnosis.{0,100}"
                r"when available.{0,160}otherwise.{0,100}(?:perform|conduct|use)"
                r".{0,80}(?:locally|local)",
            )


class TestClaudeAdapter(PortabilityContractTestCase):
    def test_claude_adapter_has_exact_thin_wrapper_surface(self) -> None:
        self.assertTrue(CLAUDE_SKILLS_ROOT.is_dir(), "Claude adapter skill directory is required")
        actual = {path.name for path in CLAUDE_SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(set(SKILLS), actual)

        for name in SKILLS:
            path = self.claude_wrapper(name)
            self.assertTrue(path.is_file(), f"missing Claude wrapper: {path}")
            fields = frontmatter(path)
            self.assertEqual(name, fields.get("name"))
            if name in LEAVES:
                self.assertEqual("true", fields.get("disable-model-invocation", "").lower())
            else:
                self.assertNotIn("disable-model-invocation", fields)

            target = f"${{CLAUDE_PLUGIN_ROOT}}/agent-skills/{name}/SKILL.md"
            text = read_text(path)
            self.assertEqual(1, text.count(target), f"wrapper must delegate exactly once: {name}")
            self.assertRegex(
                text,
                rf"(?im)^(?:load|read) [`]?{re.escape(target)}[`]?"
                rf"(?:,? then| and) follow (?:it|its instructions)[.]$",
                f"wrapper must positively load and follow the portable core: {name}",
            )
            self.assertLessEqual(len(text.splitlines()), 16, f"wrapper is not thin: {name}")

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
        self.assertEqual("0.2.0", manifest.get("version"))
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
        self.assertEqual(
            "Define the real problem, then escape it with rigorous lenses.",
            interface.get("shortDescription"),
        )
        self.assertEqual(
            "Ultrasolve states the unstated problem behind a request, then routes "
            "well-defined, genuinely stuck problems through six rigorous "
            "transformation lenses, then maps the result back to the original "
            "constraints and success criteria.",
            interface.get("longDescription"),
        )
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
        normalized_prompts = [prompt.lower() for prompt in prompts]
        self.assertTrue("stuck" in normalized_prompts[0] or "unblock" in normalized_prompts[0])
        self.assertTrue(
            "invert" in normalized_prompts[1]
            and ("forward" in normalized_prompts[1] or "verify" in normalized_prompts[1])
        )
        self.assertIn("decompos", normalized_prompts[2])
        self.assertIn("seam", normalized_prompts[2])

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
        self.assertEqual("0.2.0", marketplace.get("version"))
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
        fixtures = PLUGIN_ROOT / "evals/behavioral/v1"
        self.assertTrue(fixtures.is_dir(), "Claude-native behavioral fixtures are required")
        for case in CLAUDE_SKILL_EVAL_CASES:
            prompt = fixtures / case / "prompt.md"
            self.assertTrue(prompt.is_file(), f"missing Claude fixture: {prompt}")
            allowed_tools = frontmatter(prompt).get("allowed_tools", "")
            self.assertRegex(allowed_tools, r"\bRead\b", f"wrapper core Read blocked in {case}")

        testing_path = PLUGIN_ROOT / "TESTING.md"
        self.assertTrue(testing_path.is_file(), "testing protocol is required")
        testing = read_text(testing_path).lower()
        self.assertIn("eval-stripped", testing)
        self.assertRegex(testing, r"(?m)^rsync .{0,160}--exclude .?evals/?.{0,160}$")
        self.assertRegex(testing, r"(?m)^test ! -e .{0,120}/evals/?[\"']?$")
        self.assertIn("4/5", testing)
        for case, runs, ablation, rule in (
            ("activation", "5", "with-without", "4/5"),
            ("nonactivation", "5", "with-without", "4/5"),
            ("define", "3", "none", "3/3"),
            ("define-activation", "5", "with-without", "4/5"),
            ("define-nonactivation", "5", "with-without", "4/5"),
            ("router-read-order", "3", "none", "3/3"),
            ("simplify", "3", "none", "3/3"),
            ("analogize", "3", "none", "3/3"),
            ("restate", "3", "none", "3/3"),
            ("generalize", "3", "none", "3/3"),
            ("decompose", "3", "none", "3/3"),
            ("invert", "3", "none", "3/3"),
            ("debugging-boundary", "3", "with-without", "3/3"),
            ("map-back", "3", "none", "3/3"),
        ):
            self.assertRegex(
                testing,
                rf"(?m)^\| `{case}` \| {runs} \| `{ablation}` \| [^\n]*{re.escape(rule)}[^\n]*\|$",
            )
        self.assertIn("separate fixture", testing)
        self.assertIn("loaded plugin", testing)
        self.assertRegex(
            testing,
            r'for skill in [^\n]+; do python3 "\$skill_validator" "\$skill"'
            r';? \|\| exit 1; done',
        )
        self.assertRegex(
            testing,
            r'for skill in [^\n]+; do node "\$plugin_eval_js" analyze "\$skill"'
            r' --format json;? \|\| exit 1; done',
        )

    def test_installation_docs_match_the_standalone_tree(self) -> None:
        readme = read_text(PLUGIN_ROOT / "README.md")
        standalone_root = "/absolute/path/to/Ultrasolve"
        self.assertGreaterEqual(readme.count(standalone_root), 3)
        self.assertNotIn("/absolute/path/to/plugins", readme)
        normalized = re.sub(r"\s+", " ", readme)
        self.assertIn("Version `0.2.0`", normalized)
        self.assertRegex(normalized, r"(?i)eight.{0,80}(?:agent )?skills")
        self.assertIn("/ultrasolve:define", readme)


class TestMigrationCoherence(PortabilityContractTestCase):
    def test_legacy_contract_no_longer_requires_claude_only_surface(self) -> None:
        path = PLUGIN_ROOT / "tests/test_plugin_contract.py"
        self.assertTrue(path.is_file(), "legacy method and hygiene contract must be migrated, not deleted")
        legacy = read_text(path)
        spec = importlib.util.spec_from_file_location("ultrasolve_legacy_contract", path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader if spec else None)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loaded_suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        actual_tests: set[str] = set()

        def collect(suite: unittest.TestSuite) -> None:
            for item in suite:
                if isinstance(item, unittest.TestSuite):
                    collect(item)
                else:
                    actual_tests.add(item.id().rsplit(".", 1)[-1])

        collect(loaded_suite)
        self.assertEqual(
            EXPECTED_LEGACY_TESTS,
            actual_tests,
            "migration must preserve every established method and hygiene contract",
        )
        self.assertNotIn('PLUGIN_ROOT / "skills"', legacy)
        self.assertIn("PORTABLE_ROOT", legacy)
        self.assertIn("CLAUDE_SKILLS_ROOT", legacy)
        for obsolete_test in (
            "test_claude_only_plugin_has_no_codex_manifest",
            "test_root_marketplace_does_not_publish_ultrasolve",
        ):
            self.assertNotIn(obsolete_test, legacy)


if __name__ == "__main__":
    unittest.main()
