"""Deterministic contract for the portable Ultrasolve corpus and native adapters.

This suite validates the target ``ultrasolve`` location. All plugin paths
are derived from this file rather than hard-coded.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
DESIGN_DOC = REPOSITORY_ROOT / "docs/superpowers/specs/2026-07-19-ultrasolve-plugin-design.md"
PLAN_DOC = REPOSITORY_ROOT / "docs/superpowers/plans/2026-07-19-ultrasolve-plugin-revision.md"
PORTABILITY_DESIGN_DOC = (
    REPOSITORY_ROOT / "docs/superpowers/specs/2026-07-19-ultrasolve-portability-design.md"
)
PORTABILITY_PLAN_DOC = (
    REPOSITORY_ROOT / "docs/superpowers/plans/2026-07-19-ultrasolve-portability.md"
)
OLD_PLUGIN_ROOT = REPOSITORY_ROOT / "plugins/hard-problems"
OLD_DESIGN_DOC = REPOSITORY_ROOT / "docs/superpowers/specs/2026-07-19-hard-problems-plugin-design.md"
OLD_PLAN_DOC = REPOSITORY_ROOT / "docs/superpowers/plans/2026-07-19-hard-problems-plugin-revision.md"

SKILLS = ("solve", "simplify", "analogize", "restate", "generalize", "decompose", "invert")
LEAVES = SKILLS[1:]
PORTABLE_ROOT = PLUGIN_ROOT / "agent-skills"
CLAUDE_SKILLS_ROOT = PLUGIN_ROOT / "adapters/claude/skills"
OLD_SKILL_IDENTIFIERS = (
    "solving-hard-problems",
    "simplification",
    "similar-problems",
    "restatement",
    "generalization",
    "structural-analysis",
    "inversion",
)
EVAL_CASES = (
    "activation",
    "nonactivation",
    "router-read-order",
    "simplify",
    "analogize",
    "restate",
    "generalize",
    "decompose",
    "invert",
    "debugging-boundary",
    "map-back",
)
DIRECT_EVAL_COMMANDS = {
    "simplify": "simplify",
    "analogize": "analogize",
    "restate": "restate",
    "generalize": "generalize",
    "decompose": "decompose",
    "invert": "invert",
    "map-back": "solve",
}
READ_ENABLED_EVAL_CASES = {"activation", "router-read-order", "map-back", *LEAVES}
ANTI_LEAK_EVAL_CASES = {"activation", "router-read-order", "map-back"}
EXPECTED_EVAL_GRADERS = {
    "activation": {
        "acceptance-criteria",
        "automatic-solve",
        "map-back",
        "no-eval-read",
        "preserves-requirements",
    },
    "nonactivation": {
        "clamps-above",
        "clamps-below",
        "no-solve",
        "preserves-inside",
        "rejects-inverted",
    },
    "router-read-order": {
        "automatic-solve",
        "no-eval-read",
        "read-decompose",
        "recompose",
        "select-decompose",
        "solve-before-read",
        "trace-read-order",
    },
    "simplify": {"constraint-walkback", "map-back", "trivial-skeleton"},
    "analogize": {
        "break-charging",
        "break-nonpreemptive",
        "break-parallelism",
        "break-unknown-size",
        "candidates",
        "fact-verification",
        "idle-deficit-reset",
        "mapping-table",
        "no-borrowed-guarantee",
        "unverified-assumptions",
    },
    "restate": {"invariant-ledger", "relaxation", "three-forms"},
    "generalize": {"instantiate", "modern-form", "source-form"},
    "decompose": {"information-order", "recompose", "seams"},
    "invert": {
        "alternative-branches",
        "edge-mechanisms",
        "forward-replay",
        "necessary-sufficient",
        "noninvertible-edges",
        "unknown-sufficiency",
    },
    "debugging-boundary": {
        "bounded-inversion",
        "no-solve",
        "no-unsupported-cause",
        "not-replacement",
        "systematic-first",
    },
    "map-back": {
        "no-eval-read",
        "no-false-completion",
        "original-criteria",
        "reject-violation",
    },
}
EXPECTED_NON_LLM_GRADER_TYPES = {
    ("activation", "automatic-solve"): "tool_used",
    ("activation", "no-eval-read"): "tool_used",
    ("nonactivation", "no-solve"): "tool_used",
    ("router-read-order", "automatic-solve"): "tool_used",
    ("router-read-order", "no-eval-read"): "tool_used",
    ("router-read-order", "read-decompose"): "tool_used",
    ("router-read-order", "solve-before-read"): "tool_order",
    ("debugging-boundary", "no-solve"): "tool_used",
    ("map-back", "no-eval-read"): "tool_used",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter_parts(path: Path) -> tuple[list[str], str]:
    """Return exact frontmatter lines and body, or empty values if malformed."""
    if not path.is_file():
        return [], ""
    lines = read_text(path).splitlines()
    if not lines or lines[0] != "---":
        return [], ""
    closing = next((index for index, line in enumerate(lines[1:], start=1) if line == "---"), None)
    if closing is None:
        return [], ""
    return lines[1:closing], "\n".join(lines[closing + 1 :]).strip()


def frontmatter(path: Path) -> dict[str, str]:
    """Parse only the small scalar frontmatter surface this suite needs."""
    lines, _ = frontmatter_parts(path)

    fields: dict[str, str] = {}
    for line in lines:
        if line[:1].isspace():
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = frontmatter_scalar(value)
    return fields


def frontmatter_scalar(value: str) -> str:
    """Normalize one quoted or unquoted scalar from the small fixture schema."""
    value = value.strip()
    if value[:1] in {"\"", "'"}:
        quote = value[0]
        quoted = re.match(rf"^{quote}((?:\\.|[^{quote}])*){quote}(?:\s+#.*)?$", value)
        return quoted.group(1) if quoted else value
    return re.sub(r"\s+#.*$", "", value).rstrip()


def nested_frontmatter_mapping(path: Path, field: str) -> dict[str, str]:
    """Parse a one-level mapping such as tool_order before/after predicates."""
    lines, _ = frontmatter_parts(path)
    active = False
    values: dict[str, str] = {}
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[:1].isspace():
            key, separator, value = line.partition(":")
            active = bool(separator and key.strip() == field and not value.strip())
            continue
        if not active or ":" not in line:
            continue
        key, value = line.strip().split(":", 1)
        values[key.strip()] = frontmatter_scalar(value)
    return values


def markdown_headings(text: str) -> list[str]:
    return re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", text)


def markdown_section(text: str, title_pattern: str) -> str:
    headings = list(re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", text))
    for index, heading in enumerate(headings):
        if not re.search(title_pattern, heading.group(2), re.I):
            continue
        level = len(heading.group(1))
        end = len(text)
        for following in headings[index + 1 :]:
            if len(following.group(1)) <= level:
                end = following.start()
                break
        return text[heading.start() : end]
    return ""


def markdown_links(text: str) -> list[str]:
    """Return relative inline, image, and reference-style Markdown targets."""
    destinations: list[str] = []
    inline = re.compile(
        r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))"
        r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"
    )
    definitions = re.compile(
        r"(?m)^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))"
        r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*$"
    )
    for match in (*inline.finditer(text), *definitions.finditer(text)):
        # An angle-bracket destination may legally contain spaces.  Select it
        # before discarding a title from an unbracketed destination.
        destination = match.group(1) if match.group(1) is not None else match.group(2)
        destination = destination.split("#", 1)[0]
        if not destination or re.match(r"(?:[a-z]+:|//)", destination, re.I):
            continue
        destinations.append(destination)
    return destinations


def strip_url_destinations(text: str) -> str:
    """Remove externally owned URL text before checking local identity."""
    return re.sub(r"https?://[^\s)>]+", "", text, flags=re.I)


class PluginContractTestCase(unittest.TestCase):
    def skill_path(self, skill: str) -> Path:
        return PORTABLE_ROOT / skill / "SKILL.md"

    def claude_skill_path(self, skill: str) -> Path:
        return CLAUDE_SKILLS_ROOT / skill / "SKILL.md"

    def codex_allows_implicit_invocation(self, skill: str) -> bool:
        path = PORTABLE_ROOT / skill / "agents/openai.yaml"
        self.assertTrue(path.is_file(), f"missing Codex policy metadata: {path}")
        match = re.search(
            r"(?m)^policy:\s*$\n^  allow_implicit_invocation:\s*(true|false)\s*$",
            read_text(path),
        )
        self.assertIsNotNone(
            match,
            f"{path} must define policy.allow_implicit_invocation as a boolean",
        )
        return match.group(1) == "true" if match else False

    def skill_text(self, skill: str) -> str:
        path = self.skill_path(skill)
        self.assertTrue(path.is_file(), f"missing skill instructions: {path}")
        return read_text(path)

    def public_files(self) -> list[Path]:
        return [
            path
            for path in PLUGIN_ROOT.rglob("*")
            if path.is_file() and "tests" not in path.relative_to(PLUGIN_ROOT).parts
        ]

    def public_markdown(self) -> str:
        return "\n".join(
            read_text(path) for path in self.public_files() if path.suffix == ".md"
        )

    def assert_heading(self, text: str, pattern: str, message: str) -> None:
        headings = "\n".join(markdown_headings(text))
        self.assertRegex(headings, pattern, message)


class TestIdentityAndSurface(PluginContractTestCase):
    def test_plugin_directory_has_final_path(self) -> None:
        expected_root = (REPOSITORY_ROOT / "plugins/ultrasolve").resolve()
        self.assertEqual(expected_root, PLUGIN_ROOT.resolve())

    def test_manifest_has_final_identity_and_source_faithful_description(self) -> None:
        manifest_path = PLUGIN_ROOT / ".claude-plugin/plugin.json"
        self.assertTrue(manifest_path.is_file(), "plugin manifest is required")
        manifest = json.loads(read_text(manifest_path))
        self.assertEqual("ultrasolve", manifest.get("name"))
        self.assertEqual("Ultrasolve", manifest.get("displayName"))
        self.assertEqual("0.1.0", manifest.get("version"))
        self.assertEqual(
            "https://json.schemastore.org/claude-code-plugin-manifest.json",
            manifest.get("$schema"),
        )
        self.assertEqual(
            "Rigorous methods for solving the hardest problems.",
            manifest.get("description"),
        )

    def test_obsolete_plugin_directory_is_absent(self) -> None:
        self.assertFalse(
            OLD_PLUGIN_ROOT.exists(),
            f"obsolete plugin directory remains: {OLD_PLUGIN_ROOT}",
        )

    def test_obsolete_canonical_doc_filenames_are_absent(self) -> None:
        for path in (OLD_DESIGN_DOC, OLD_PLAN_DOC):
            self.assertFalse(
                path.exists(),
                f"obsolete canonical documentation remains: {path}",
            )

    def test_codex_and_claude_manifests_share_identity(self) -> None:
        claude_path = PLUGIN_ROOT / ".claude-plugin/plugin.json"
        codex_path = PLUGIN_ROOT / ".codex-plugin/plugin.json"
        self.assertTrue(claude_path.is_file(), "Claude manifest is required")
        self.assertTrue(codex_path.is_file(), "Codex manifest is required")
        claude = json.loads(read_text(claude_path))
        codex = json.loads(read_text(codex_path))
        for field in ("name", "version", "description"):
            self.assertEqual(
                claude.get(field),
                codex.get(field),
                f"native manifests must share {field}",
            )
        claude_skills = claude.get("skills")
        normalized_claude_skills = (
            [claude_skills] if isinstance(claude_skills, str) else claude_skills
        )
        self.assertEqual(["./adapters/claude/skills/"], normalized_claude_skills)
        self.assertEqual("./agent-skills/", codex.get("skills"))

    def test_root_marketplace_publishes_ultrasolve(self) -> None:
        marketplace_path = REPOSITORY_ROOT / ".agents/plugins/marketplace.json"
        self.assertTrue(marketplace_path.is_file(), "root marketplace manifest is required")
        marketplace = json.loads(read_text(marketplace_path))
        entries = [
            entry for entry in marketplace.get("plugins", [])
            if entry.get("name") == "ultrasolve"
        ]
        self.assertEqual(1, len(entries), "marketplace must list Ultrasolve exactly once")
        self.assertEqual(
            {
                "name": "ultrasolve",
                "source": {"source": "local", "path": "./plugins/ultrasolve"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            },
            entries[0],
        )

    def test_public_structural_artifacts_have_only_canonical_identity(self) -> None:
        artifacts = [
            *self.public_files(),
            DESIGN_DOC,
            PLAN_DOC,
            PORTABILITY_DESIGN_DOC,
            PORTABILITY_PLAN_DOC,
        ]
        for path in artifacts:
            self.assertTrue(path.is_file(), f"missing structural artifact: {path}")
            structural_text = strip_url_destinations(read_text(path))
            relative = path.relative_to(REPOSITORY_ROOT)
            self.assertNotIn("hard-problems", structural_text, f"stale plugin ID in {relative}")
            self.assertNotRegex(
                structural_text,
                r"/hard-problems:[a-z-]+",
                f"stale command namespace in {relative}",
            )
            self.assertNotIn(
                "plugins/hard-problems",
                structural_text,
                f"stale plugin path in {relative}",
            )
            self.assertNotIn(
                "Solving Hard Problems",
                structural_text,
                f"stale branded phrase in {relative}",
            )
            self.assertNotIn("UltraSolve", structural_text, f"noncanonical casing in {relative}")
            self.assertNotIn("ultra-solve", structural_text, f"noncanonical plugin ID in {relative}")

    def test_design_records_name_screening_limit_and_publication_hold(self) -> None:
        self.assertTrue(DESIGN_DOC.is_file(), f"renamed design is required: {DESIGN_DOC}")
        screening = markdown_section(read_text(DESIGN_DOC), r"name screening|trademark")
        self.assertTrue(screening, "design needs a name-screening section")
        screening_without_urls = strip_url_destinations(screening)
        screening_flat = re.sub(r"\s+", " ", screening_without_urls)
        screening_statements = re.split(r"(?<=[.!?])\s+", screening_flat)
        self.assertIn("2026-07-19", screening_flat)

        exact_record_statements = [
            statement for statement in screening_statements if "75942305" in statement
        ]
        self.assertEqual(
            1,
            len(exact_record_statements),
            "screening must identify exact-name USPTO record 75942305 once",
        )
        exact_record_statement = exact_record_statements[0]
        self.assertRegex(exact_record_statement, r"(?i)\bexact-name\b")
        self.assertRegex(exact_record_statement, r"(?i)\bUSPTO\b")
        self.assertRegex(exact_record_statement, r"(?i)\bdead\b")
        self.assertRegex(exact_record_statement, r"(?i)\bunrelated\b")
        self.assertNotIn(
            "75279620",
            exact_record_statement,
            "live close mark 75279620 must not be grouped with exact-name dead records",
        )

        live_close_mark_statements = [
            statement for statement in screening_statements if "75279620" in statement
        ]
        self.assertEqual(
            1,
            len(live_close_mark_statements),
            "screening must identify live close mark 75279620 once",
        )
        live_close_mark_statement = live_close_mark_statements[0]
        self.assertRegex(live_close_mark_statement, r"(?i)\blive\b")
        self.assertRegex(live_close_mark_statement, r"(?i)\brenewed\b")
        self.assertRegex(live_close_mark_statement, r"(?i)\bclose[- ]mark\b")
        self.assertRegex(live_close_mark_statement, r"(?i)\bclass-separated\b")
        self.assertRegex(live_close_mark_statement, r"(?i)\bnon-software\b")
        self.assertNotRegex(
            live_close_mark_statement,
            r"(?i)\bexact(?:-name)?\b",
            "live close mark 75279620 must not be described as an exact-name record",
        )

        for registry in ("WIPO", "TMview"):
            self.assertRegex(
                screening_flat,
                rf"(?i)(?:\b{registry}\b[^.]{{0,160}}\binconclusive\b|"
                rf"\binconclusive\b[^.]{{0,160}}\b{registry}\b)",
                f"design must tie {registry} coverage to its inconclusive status",
            )
        self.assertIn(
            "This screening is not legal clearance.",
            screening,
        )
        self.assertEqual(
            1,
            screening.lower().count("legal clearance"),
            "screening must contain only the exact legal-clearance disclaimer",
        )
        self.assertRegex(
            screening_flat,
            r"(?i)(?:publication.{0,40}\bhold\b|\bhold\b.{0,40}publication)",
            "design must explicitly hold publication after the inconclusive screening",
        )

    def test_skill_surface_is_exactly_the_router_and_six_leaves(self) -> None:
        self.assertTrue(PORTABLE_ROOT.is_dir(), "portable skill corpus is required")
        portable = {path.name for path in PORTABLE_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(set(SKILLS), portable)
        self.assertTrue(CLAUDE_SKILLS_ROOT.is_dir(), "Claude skill adapter is required")
        wrappers = {path.name for path in CLAUDE_SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(set(SKILLS), wrappers)
        for skill in SKILLS:
            self.assertTrue(self.skill_path(skill).is_file(), f"{skill} needs SKILL.md")
            self.assertTrue(
                self.claude_skill_path(skill).is_file(),
                f"{skill} needs a Claude adapter wrapper",
            )

    def test_command_wrappers_are_absent(self) -> None:
        self.assertFalse((PLUGIN_ROOT / "commands").exists(), "skills are the command surface")


class TestRouterContract(PluginContractTestCase):
    def test_only_router_is_model_invocable(self) -> None:
        router_fields = frontmatter(self.claude_skill_path("solve"))
        self.assertNotEqual("true", router_fields.get("disable-model-invocation", "").lower())
        self.assertTrue(
            self.codex_allows_implicit_invocation("solve"),
            "Codex must allow implicit invocation only for the router",
        )
        for leaf in LEAVES:
            fields = frontmatter(self.claude_skill_path(leaf))
            self.assertEqual(
                "true",
                fields.get("disable-model-invocation", "").lower(),
                f"{leaf} must remain user-invocable but not model-invocable",
            )
            self.assertFalse(
                self.codex_allows_implicit_invocation(leaf),
                f"Codex leaf {leaf} must remain explicit-only",
            )

    def test_router_explicitly_loads_each_leaf_from_plugin_root(self) -> None:
        router = self.skill_text("solve")
        for leaf in LEAVES:
            path = f"../{leaf}/SKILL.md"
            self.assertEqual(
                1,
                router.count(path),
                f"solve must name {leaf}'s exact sibling path once",
            )
        self.assertRegex(
            router,
            r"(?is)(?:read|load).{0,160}selected sibling.{0,240}"
            r"(?:read|load).{0,160}every selected leaf",
            "solve must load each selected portable sibling before applying it",
        )

    def test_router_enforces_the_shared_contract_and_map_back(self) -> None:
        router = self.skill_text("solve").lower()
        for required in ("success criteria", "fixed facts", "constraints", "missing", "map back", "verify"):
            self.assertIn(required, router)


class TestSourceAndExamples(PluginContractTestCase):
    def test_source_notes_preserve_corrected_publication_date_and_provenance_labels(self) -> None:
        notes = PORTABLE_ROOT / "solve/references/shannon-source-notes.md"
        self.assertTrue(notes.is_file(), "source notes must have the final provenance filename")
        text = read_text(notes).lower()
        history = markdown_section(text, r"source record|publication history")
        self.assertTrue(history, "source notes need a publication-history section")
        history_flat = re.sub(r"\s+", " ", history)
        self.assertIn("1993", history_flat)
        self.assertRegex(history_flat, r"\b(?:assembled|binder|copies|deposited)\b")
        self.assertRegex(
            history_flat,
            r"(?:collected papers.{0,160}(?:published.{0,80}(?:ieee press|1993)|"
            r"ieee press.{0,80}published)|"
            r"(?:ieee press.{0,80}published|published.{0,80}ieee press)"
            r".{0,160}collected papers)",
        )
        self.assertRegex(
            history_flat,
            r"(?:1990.{0,120}permission.{0,120}(?:assemble|compile|collect)|"
            r"permission.{0,120}(?:assemble|compile|collect).{0,120}1990)",
        )
        self.assertRegex(
            history_flat,
            r"(?:2013.{0,120}(?:scan|upload)|(?:scan|upload).{0,120}2013)",
        )
        self.assertRegex(
            history_flat,
            r"(?:not|never|rather than).{0,80}(?:conventional )?(?:publication|published)",
        )
        self.assertIn("fats waller", text)
        for heading in ("source-derived", "collection synthesis", "modern authored extensions"):
            self.assertRegex(text, rf"(?m)^#{{2,6}}\s+{re.escape(heading)}\b")

        similar = markdown_section(text, r"(?:similar.*problems|analog)")
        self.assertTrue(similar, "source notes need a similar-problems/analogy section")
        for notation in ("p", "p′", "s", "s′"):
            self.assertRegex(similar, rf"(?<![a-z]){re.escape(notation)}(?![a-z])")
        self.assertRegex(similar, r"authored.{0,120}(?:synthesis|reuse|unifying)")

        generalize = markdown_section(text, r"generaliz")
        self.assertTrue(generalize, "source notes need a generalization section")
        self.assertRegex(generalize, r"source-derived.{0,200}(?:broaden|generaliz).{0,120}(?:already[- ]found|solved|result|principle)")
        self.assertRegex(generalize, r"modern authored extension.{0,200}(?:parameter|structure-exposing)")

    def test_known_false_claims_are_not_shipped(self) -> None:
        text = re.sub(r"\s+", " ", self.public_markdown().lower())
        for false_claim in (
            "packets are preemptible",
            "variability, not utilization",
            "load-insensitive (else us would show it)",
        ):
            self.assertNotIn(false_claim, text)
        self.assertNotRegex(
            text,
            r"load[- ]insensitive.{0,100}\b(?:because|otherwise|if)\b.{0,100}"
            r"\b(?:the\s+)?u\.?s\.?\b.{0,80}\b(?:would\s+)?(?:show|see|exhibit)\b",
        )

    def test_drr_credit_carry_is_conditioned_on_remaining_backlogged(self) -> None:
        for path in (
            self.skill_path("analogize"),
            PORTABLE_ROOT / "solve/references/worked-examples.md",
        ):
            text = re.sub(r"\s+", " ", read_text(path).lower())
            self.assertRegex(
                text,
                r"residual deficit.{0,100}(?:only )?while (?:a |the )?queue "
                r"(?:remains|stays) backlogged",
                f"{path} must condition residual-deficit carry on backlog",
            )
            self.assertRegex(
                text,
                r"(?:queue (?:empties|drains).{0,80}deficit.{0,40}reset(?:s|ting)?"
                r"(?: to)? zero|empty queue.{0,40}reset(?:s|ting)?.{0,40}deficit"
                r".{0,20}(?: to)? zero)",
                f"{path} must reset deficit when a queue becomes empty",
            )

    def test_legacy_namespace_and_old_skill_structures_are_absent_from_public_surface(self) -> None:
        for path in self.public_files():
            relative = path.relative_to(PLUGIN_ROOT)
            text = read_text(path).lower()
            structural_text = re.sub(r"https?://[^\s)>]+", "", text)
            self.assertNotRegex(
                structural_text,
                r"/shannon:",
                f"stale command namespace in {relative}",
            )
            self.assertNotIn("creative-thinking", structural_text, f"stale identity in {relative}")
            self.assertNotRegex(
                structural_text,
                r"(?<![a-z0-9_/.-])/shannon(?:-[a-z]+)?(?:\b|$)",
                f"stale command namespace in {relative}",
            )
            self.assertNotRegex(
                structural_text,
                r"(?<![a-z0-9_-])commands/shannon(?:-[a-z]+)?\.md\b",
                f"stale command path in {relative}",
            )
            fields = frontmatter(path) if path.suffix == ".md" else {}
            self.assertNotIn(fields.get("name", "").lower(), OLD_SKILL_IDENTIFIERS)
            for identifier in OLD_SKILL_IDENTIFIERS:
                self.assertNotRegex(
                    structural_text,
                    rf"(?<![a-z0-9_-])skills/{re.escape(identifier)}/skill\.md\b",
                    f"stale skill path for {identifier} in {relative}",
                )


class TestLeafContracts(PluginContractTestCase):
    def test_every_leaf_has_the_shared_workflow_structure(self) -> None:
        for leaf in LEAVES:
            text = self.skill_text(leaf).lower()
            self.assert_heading(text, r"(?i)(?:source.*(?:extension|authored)|(?:extension|authored).*source|provenance)", f"{leaf} needs a source-vs-extension section")
            self.assert_heading(text, r"(?i)(?:shared )?(?:entry|problem) contract", f"{leaf} needs the shared entry contract")
            self.assert_heading(text, r"(?i)(?:cheap.*candidate|candidate.*(?:transformation|route))", f"{leaf} needs a cheap-candidate section")
            self.assert_heading(text, r"(?i)(?:full )?method", f"{leaf} needs a full-method section")
            self.assert_heading(text, r"(?i)(?:result.*map.?back|map.?back.*result)", f"{leaf} needs a result/map-back section")
            self.assert_heading(text, r"(?i)(?:failure modes?|common (?:mistakes|failures))", f"{leaf} needs failure modes")

            entry = markdown_section(text, r"(?:shared )?(?:entry|problem) contract")
            self.assertRegex(entry, r"\b(?:p|problem)\b", f"{leaf} entry contract must state P/problem")
            self.assertRegex(entry, r"observable.{0,30}success criteria", f"{leaf} needs observable success criteria")
            self.assertIn("fixed facts", entry, f"{leaf} must preserve fixed facts")
            self.assertIn("constraints", entry, f"{leaf} must preserve constraints")
            self.assertRegex(entry, r"missing.{0,40}(?:domain )?facts", f"{leaf} must gather missing facts")

    def test_simplify_contract(self) -> None:
        text = self.skill_text("simplify").lower()
        for required in ("constraints", "trivial", "skeleton", "one at a time", "map back"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)(?:restore|re-add).{0,180}constraints?.{0,100}one at a time|one at a time.{0,100}(?:restore|re-add).{0,180}constraints?")
        self.assertRegex(text, r"(?s)first.{0,80}constraint.{0,100}(?:reintroduc|bring back|return).{0,60}(?:difficulty|hardness)")

    def test_analogize_contract(self) -> None:
        text = self.skill_text("analogize").lower()
        for required in ("at least two", "fact", "mapping table", "break"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)(?:at least )?two.{0,80}candidate analog(?:y|ies).{0,180}(?:before|then).{0,80}(?:select|choose)")
        self.assertRegex(text, r"(?s)verif.{0,100}(?:source[- ]domain )?facts?.{0,240}mapping table")
        self.assertRegex(text, r"(?s)break.{0,160}(?:decision|limit|failure)")

    def test_restate_contract(self) -> None:
        text = self.skill_text("restate").lower()
        for required in ("at least three", "fixed facts", "relaxation", "success criteria"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)(?:at least )?three.{0,100}(?:restatement|representation|viewpoint)")
        self.assertRegex(text, r"(?s)(?:label|mark).{0,80}(?:intentional )?relaxation")

    def test_generalize_contract(self) -> None:
        text = self.skill_text("generalize").lower()
        for required in ("shannon-derived", "result-first", "modern", "parameter", "instantiate"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)shannon-derived.{0,180}(?:result-first|solved related|already[- ]found).{0,120}(?:result|principle)")
        self.assertRegex(text, r"(?s)modern.{0,160}(?:structure-exposing|parameteriz)")
        self.assertRegex(
            text,
            r"(?s)(?:produce|return).{0,100}both (?:labeled )?forms",
            "generalize must produce both source-derived and modern forms",
        )
        self.assertRegex(
            text,
            r"(?s)compare.{0,100}(?:two|both) forms.{0,100}select.{0,100}stronger",
            "generalize must compare both forms and select one for deeper work",
        )

    def test_decompose_contract(self) -> None:
        text = self.skill_text("decompose").lower()
        for required in ("more than one", "seam", "rejected", "information yield", "recompose"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)more than one.{0,100}candidate seam.{0,220}(?:choose|select).{0,120}(?:strong|reject)")
        self.assertRegex(text, r"(?s)recompose.{0,160}(?:cross-cutting|original|constraints)")

    def test_invert_is_logically_safe_and_reenters_debugging(self) -> None:
        text = self.skill_text("invert").lower()
        for required in (
            "necessary",
            "sufficient",
            "alternative",
            "non-invertible",
            "unknown sufficiency",
            "forward replay",
            "systematic debugging",
            "does not replace",
        ):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)(?:each )?edge.{0,100}(?:action|mechanism).{0,100}(?:expected )?effect")
        self.assertRegex(text, r"(?s)(?:necessary.{0,100}sufficient|sufficient.{0,100}necessary)")
        self.assertRegex(text, r"(?s)preserv.{0,100}alternative.{0,80}(?:predecessor )?branches?")
        self.assertRegex(text, r"(?s)(?:non-invertible|not invertible).{0,120}(?:unknown sufficiency|sufficiency.{0,40}unknown)")
        self.assertRegex(text, r"(?s)forward.{0,80}(?:candidate )?plan.{0,160}replay.{0,120}(?:actual )?current state")


class TestDocumentationAndEvals(PluginContractTestCase):
    def grader_path(self, case: str, stem: str) -> Path:
        return PLUGIN_ROOT / "evals/behavioral/v1" / case / "graders" / f"{stem}.md"

    def test_readme_exposes_exactly_the_seven_final_commands(self) -> None:
        readme = PLUGIN_ROOT / "README.md"
        self.assertTrue(readme.is_file(), "README is required")
        text = read_text(readme)
        commands = set(re.findall(r"/ultrasolve:([a-z-]+)", text))
        self.assertEqual(set(SKILLS), commands)
        self.assertNotRegex(
            text.lower(),
            r"/(?:shannon|creative-thinking|hard-problems)(?:[\s:`-]|$)",
        )

    def test_readme_links_design_and_testing_guidance(self) -> None:
        readme = PLUGIN_ROOT / "README.md"
        links = {((readme.parent / target).resolve()) for target in markdown_links(read_text(readme))}
        self.assertIn(DESIGN_DOC.resolve(), links)
        self.assertIn(PORTABILITY_DESIGN_DOC.resolve(), links)
        self.assertIn(PORTABILITY_PLAN_DOC.resolve(), links)
        self.assertIn((PLUGIN_ROOT / "TESTING.md").resolve(), links)

    def test_relative_markdown_links_resolve_in_plugin_design_and_plan_docs(self) -> None:
        documents = [
            *PLUGIN_ROOT.rglob("*.md"),
            DESIGN_DOC,
            PLAN_DOC,
            PORTABILITY_DESIGN_DOC,
            PORTABILITY_PLAN_DOC,
        ]
        for document in documents:
            self.assertTrue(document.is_file(), f"referenced documentation is missing: {document}")
            for target in markdown_links(read_text(document)):
                destination = (document.parent / target).resolve()
                self.assertTrue(destination.exists(), f"broken link in {document}: {target}")

    def test_manual_only_eval_cases_begin_with_real_slash_invocation(self) -> None:
        for case, skill in DIRECT_EVAL_COMMANDS.items():
            prompt = PLUGIN_ROOT / "evals/behavioral/v1" / case / "prompt.md"
            _, body = frontmatter_parts(prompt)
            self.assertTrue(
                body.startswith(f"/ultrasolve:{skill} "),
                f"{case} must invoke its skill as the first print-mode token",
            )

        for case in ("activation", "router-read-order", "nonactivation", "debugging-boundary"):
            prompt = PLUGIN_ROOT / "evals/behavioral/v1" / case / "prompt.md"
            _, body = frontmatter_parts(prompt)
            self.assertFalse(
                body.startswith("/ultrasolve:"),
                f"{case} must exercise automatic activation policy",
            )

    def test_versioned_eval_fixtures_match_exact_native_shape(self) -> None:
        eval_root = PLUGIN_ROOT / "evals/behavioral/v1"
        self.assertTrue(eval_root.is_dir(), "versioned behavioral eval fixtures are required")
        actual_cases = {path.name for path in eval_root.iterdir() if path.is_dir()}
        self.assertEqual(set(EVAL_CASES), actual_cases)
        for case in EVAL_CASES:
            case_root = eval_root / case
            prompt = case_root / "prompt.md"
            graders = case_root / "graders"
            self.assertTrue(prompt.is_file(), f"{case} needs exact prompt.md")
            self.assertFalse((case_root / "case.yaml").exists(), f"{case} must use native prompt.md")
            self.assertTrue(graders.is_dir(), f"{case} needs graders/")
            _, prompt_body = frontmatter_parts(prompt)
            self.assertTrue(prompt_body, f"{case} needs a nonempty prompt body")
            prompt_fields = frontmatter(prompt)
            self.assertEqual(
                {"max_turns", "timeout_seconds", "allowed_tools"},
                set(prompt_fields),
                f"{case} prompt must use only the native prompt schema",
            )
            self.assertIn(int(prompt_fields["max_turns"]), range(1, 201))
            self.assertIn(int(prompt_fields["timeout_seconds"]), range(1, 3601))
            expected_tools = "[Read]" if case in READ_ENABLED_EVAL_CASES else "[]"
            self.assertEqual(expected_tools, prompt_fields["allowed_tools"])

            grader_paths = sorted(graders.glob("*.md"))
            actual_graders = {path.stem for path in grader_paths}
            self.assertEqual(
                EXPECTED_EVAL_GRADERS[case],
                actual_graders,
                f"{case} grader set is part of the immutable v1 fixture contract",
            )
            for grader in grader_paths:
                grader_fields = frontmatter(grader)
                grader_type = grader_fields.get("type")
                expected_type = EXPECTED_NON_LLM_GRADER_TYPES.get(
                    (case, grader.stem), "llm"
                )
                self.assertEqual(
                    expected_type,
                    grader_type,
                    f"{grader} must keep its intended native grader type",
                )
                self.assertTrue(grader_fields.get("weight"), f"{grader} needs frontmatter weight")
                self.assertGreater(float(grader_fields["weight"]), 0)
                if "arm" in grader_fields:
                    self.assertIn(grader_fields["arm"], {"with-only", "both"})
                allowed_keys = {
                    "llm": {"type", "weight", "arm", "focus", "criteria"},
                    "baseline": {
                        "type",
                        "weight",
                        "arm",
                        "baseline_file",
                        "criteria",
                    },
                    "tool_used": {
                        "type",
                        "weight",
                        "arm",
                        "tool",
                        "input_match",
                        "min",
                        "max",
                    },
                    "tool_order": {"type", "weight", "arm", "before", "after"},
                    "regex": {
                        "type",
                        "weight",
                        "arm",
                        "target",
                        "pattern",
                        "flags",
                        "match",
                    },
                    "file_exists": {"type", "weight", "arm", "path", "exists"},
                }[grader_type]
                self.assertFalse(
                    set(grader_fields) - allowed_keys,
                    f"{grader} has keys rejected by Claude's strict grader schema",
                )
                _, criterion = frontmatter_parts(grader)
                if grader_type in {"llm", "baseline"}:
                    self.assertTrue(criterion, f"{grader} needs a nonempty semantic criterion")
                    self.assertIn(
                        grader_fields.get("focus", "last_message"),
                        {"trace", "last_message", "files"},
                        f"{grader} has an unsupported scalar focus",
                    )
                elif grader_type == "tool_used":
                    self.assertTrue(grader_fields.get("tool"), f"{grader} needs tool")
                    self.assertIn("min", grader_fields, f"{grader} makes its call floor explicit")
                    minimum = int(grader_fields["min"])
                    self.assertGreaterEqual(minimum, 0)
                    if "max" in grader_fields:
                        self.assertGreaterEqual(int(grader_fields["max"]), minimum)
                    if input_match := grader_fields.get("input_match"):
                        re.compile(input_match)
                elif grader_type == "tool_order":
                    for position in ("before", "after"):
                        predicate = nested_frontmatter_mapping(grader, position)
                        self.assertFalse(
                            set(predicate) - {"tool", "input_match"},
                            f"{grader} has keys rejected in {position} predicate",
                        )
                        tool = grader_fields.get(position) or predicate.get("tool")
                        self.assertTrue(tool, f"{grader} needs {position} tool predicate")
                        if input_match := predicate.get("input_match"):
                            re.compile(input_match)

    def test_read_enabled_eval_cases_block_reads_into_eval_tree(self) -> None:
        for case in ANTI_LEAK_EVAL_CASES:
            grader = self.grader_path(case, "no-eval-read")
            fields = frontmatter(grader)
            self.assertEqual("tool_used", fields.get("type"))
            self.assertEqual("Read", fields.get("tool"))
            self.assertEqual("0", fields.get("min"))
            self.assertEqual("0", fields.get("max"))
            self.assertEqual("both", fields.get("arm"))
            pattern = fields.get("input_match", "")
            self.assertTrue(pattern, f"{case} anti-leak grader needs input_match")
            compiled = re.compile(pattern)
            for eval_path in (
                "/tmp/ultrasolve/evals/behavioral/v1/prompt.md",
                "/tmp/ultrasolve/EVALS/behavioral/v1/graders/key.md",
                "/tmp/ultrasolve/EvAlS/behavioral/v1/prompt.md",
            ):
                self.assertIsNotNone(
                    compiled.search(eval_path),
                    f"{case} anti-leak grader must match case-variant eval-tree Read: "
                    f"{eval_path}",
                )

    def test_semantic_regression_fixtures_are_evidence_faithful(self) -> None:
        analog_prompt = re.sub(
            r"\s+",
            " ",
            frontmatter_parts(
                PLUGIN_ROOT / "evals/behavioral/v1/analogize/prompt.md"
            )[1].lower(),
        )
        self.assertRegex(
            analog_prompt,
            r"residual deficit.{0,100}only while.{0,60}backlogged",
        )
        self.assertRegex(
            analog_prompt,
            r"queue empties.{0,60}deficit resets to zero",
        )
        idle_reset = read_text(
            self.grader_path("analogize", "idle-deficit-reset")
        ).lower()
        self.assertIn("idle queues", idle_reset)
        self.assertIn("hoarding", idle_reset)
        self.assertIn("resetting the deficit when a queue empties", idle_reset)

        debug_prompt = re.sub(
            r"\s+",
            " ",
            frontmatter_parts(
                PLUGIN_ROOT / "evals/behavioral/v1/debugging-boundary/prompt.md"
            )[1].lower(),
        )
        self.assertIn("does not record intermediate coupon values", debug_prompt)
        self.assertIn("no relevant source lines are supplied", debug_prompt)
        self.assertRegex(debug_prompt, r"plan.{0,80}diagnosis.{0,80}verification")
        unsupported = read_text(
            self.grader_path("debugging-boundary", "no-unsupported-cause")
        ).lower()
        self.assertIn("hypothesis", unsupported)
        self.assertIn("unsupported root cause or fix", unsupported)

    def test_activation_and_boundary_fixtures_use_native_skill_trace_graders(self) -> None:
        automatic = frontmatter(self.grader_path("activation", "automatic-solve"))
        self.assertEqual("tool_used", automatic.get("type"))
        self.assertEqual("Skill", automatic.get("tool"))
        self.assertIn("ultrasolve:solve", automatic.get("input_match", ""))
        self.assertEqual("1", automatic.get("min"))
        self.assertEqual("with-only", automatic.get("arm"))

        router_automatic = frontmatter(
            self.grader_path("router-read-order", "automatic-solve")
        )
        self.assertEqual("tool_used", router_automatic.get("type"))
        self.assertEqual("Skill", router_automatic.get("tool"))
        self.assertIn("ultrasolve:solve", router_automatic.get("input_match", ""))
        self.assertEqual("1", router_automatic.get("min"))

        for case in ("nonactivation", "debugging-boundary"):
            no_solve = frontmatter(self.grader_path(case, "no-solve"))
            self.assertEqual("tool_used", no_solve.get("type"))
            self.assertEqual("Skill", no_solve.get("tool"))
            self.assertIn("ultrasolve:solve", no_solve.get("input_match", ""))
            self.assertEqual("0", no_solve.get("min"))
            self.assertEqual("0", no_solve.get("max"))
            self.assertEqual("both", no_solve.get("arm"))

    def test_router_read_order_combines_deterministic_and_semantic_trace_checks(self) -> None:
        read_call = frontmatter(self.grader_path("router-read-order", "read-decompose"))
        self.assertEqual("tool_used", read_call.get("type"))
        self.assertEqual("Read", read_call.get("tool"))
        self.assertRegex(
            read_call.get("input_match", ""),
            r"agent-skills/decompose/SKILL",
        )
        self.assertEqual("1", read_call.get("min"))

        tool_order_path = self.grader_path("router-read-order", "solve-before-read")
        tool_order = frontmatter(tool_order_path)
        self.assertEqual("tool_order", tool_order.get("type"))
        before = nested_frontmatter_mapping(tool_order_path, "before")
        after = nested_frontmatter_mapping(tool_order_path, "after")
        self.assertEqual("Skill", before.get("tool"))
        self.assertIn("ultrasolve:solve", before.get("input_match", ""))
        self.assertEqual("Read", after.get("tool"))
        self.assertRegex(
            after.get("input_match", ""),
            r"agent-skills/decompose/SKILL",
        )

        trace_check_path = self.grader_path("router-read-order", "trace-read-order")
        trace_check = frontmatter(trace_check_path)
        self.assertEqual("llm", trace_check.get("type"))
        self.assertEqual("trace", trace_check.get("focus"))
        self.assertIn(
            "${CLAUDE_PLUGIN_ROOT}/agent-skills/decompose/SKILL.md",
            read_text(trace_check_path),
        )


class TestFileHygiene(PluginContractTestCase):
    def test_text_artifacts_have_no_trailing_whitespace_and_one_final_newline(self) -> None:
        artifacts = [
            path
            for path in PLUGIN_ROOT.rglob("*")
            if path.is_file() and path.suffix in {".md", ".json", ".yaml", ".py"}
        ]
        artifacts.extend(
            (DESIGN_DOC, PLAN_DOC, PORTABILITY_DESIGN_DOC, PORTABILITY_PLAN_DOC)
        )
        self.assertTrue(artifacts, "expected plugin and repository text artifacts")
        for path in artifacts:
            self.assertTrue(path.is_file(), f"missing text artifact: {path}")
            data = path.read_bytes()
            self.assertTrue(data.endswith(b"\n"), f"{path} must end with one newline")
            self.assertFalse(data.endswith(b"\n\n"), f"{path} must end with exactly one newline")
            for number, line in enumerate(data.splitlines(), start=1):
                self.assertFalse(line.rstrip(b" \t") != line, f"trailing whitespace: {path}:{number}")


if __name__ == "__main__":
    unittest.main()
