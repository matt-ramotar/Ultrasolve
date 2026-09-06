"""Deterministic contract for the portable Ultrasolve corpus and native adapters.

The suite locates the ``ultrasolve`` checkout from this file and derives all
plugin paths from it.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

if __package__:
    from tests.contract_support import public_contract_files, repository_files
else:
    from contract_support import public_contract_files, repository_files


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
STANDALONE_MARKETPLACE = PLUGIN_ROOT / ".claude-plugin/marketplace.json"
OLD_PLUGIN_ROOT = PLUGIN_ROOT / "plugins/hard-problems"
OLD_DOC_FILENAMES = {
    "2026-07-19-hard-problems-plugin-design.md",
    "2026-07-19-hard-problems-plugin-revision.md",
}

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
    "define",
    "define-activation",
    "define-nonactivation",
)
DIRECT_EVAL_COMMANDS = {
    "simplify": "simplify",
    "analogize": "analogize",
    "restate": "restate",
    "generalize": "generalize",
    "decompose": "decompose",
    "invert": "invert",
    "map-back": "solve",
    "define": "define",
}
READ_ENABLED_EVAL_CASES = {
    "activation",
    "router-read-order",
    "map-back",
    "define",
    "define-activation",
    "define-nonactivation",
    *LEAVES,
}
ANTI_LEAK_EVAL_CASES = {"activation", "router-read-order", "map-back", "define-activation"}
EXPECTED_EVAL_GRADERS = {
    "activation": {
        "acceptance-criteria",
        "automatic-solve",
        "map-back",
        "no-define",
        "no-eval-read",
        "preserves-requirements",
    },
    "nonactivation": {
        "clamps-above",
        "clamps-below",
        "no-define",
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
        "no-define",
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
    "define": {
        "decision-point",
        "mandate-regress",
        "problem-frame",
        "problem-level-criteria",
        "symmetric-hypotheses",
    },
    "define-activation": {
        "automatic-define",
        "decision-point",
        "no-eval-read",
        "no-solve",
        "problem-frame",
        "problem-level-criteria",
    },
    "define-nonactivation": {"engages-rut", "no-define", "preserves-criteria"},
}
EXPECTED_NON_LLM_GRADER_TYPES = {
    ("activation", "automatic-solve"): "tool_used",
    ("activation", "no-define"): "tool_used",
    ("activation", "no-eval-read"): "tool_used",
    ("nonactivation", "no-define"): "tool_used",
    ("nonactivation", "no-solve"): "tool_used",
    ("router-read-order", "automatic-solve"): "tool_used",
    ("router-read-order", "no-eval-read"): "tool_used",
    ("router-read-order", "read-decompose"): "tool_used",
    ("router-read-order", "solve-before-read"): "tool_order",
    ("debugging-boundary", "no-define"): "tool_used",
    ("debugging-boundary", "no-solve"): "tool_used",
    ("map-back", "no-eval-read"): "tool_used",
    ("define-activation", "automatic-define"): "tool_used",
    ("define-activation", "no-solve"): "tool_used",
    ("define-activation", "no-eval-read"): "tool_used",
    ("define-nonactivation", "no-define"): "tool_used",
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


def standalone_files() -> list[Path]:
    """All checkout text remains in scope for hygiene and local links."""
    return repository_files(PLUGIN_ROOT)


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

    def method_text(self, leaf: str) -> str:
        path = PORTABLE_ROOT / "solve/references/methods" / f"{leaf}.md"
        self.assertTrue(path.is_file(), f"missing canonical method: {path}")
        return read_text(path)

    def public_files(self) -> list[Path]:
        return public_contract_files(PLUGIN_ROOT)

    def public_markdown(self) -> str:
        return "\n".join(
            read_text(path) for path in self.public_files() if path.suffix == ".md"
        )

    def assert_heading(self, text: str, pattern: str, message: str) -> None:
        headings = "\n".join(markdown_headings(text))
        self.assertRegex(headings, pattern, message)


class TestIdentityAndSurface(PluginContractTestCase):
    def test_plugin_directory_has_final_path(self) -> None:
        self.assertFalse(
            (PLUGIN_ROOT / "plugins/ultrasolve").exists(),
            "standalone checkout must not nest a marketplace-repository plugin path",
        )
        self.assertTrue(
            (PLUGIN_ROOT / ".claude-plugin/plugin.json").is_file(),
            "standalone root must own the Claude plugin manifest",
        )
        self.assertTrue(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").is_file(),
            "standalone root must own the Codex plugin manifest",
        )

    def test_manifest_has_final_identity_and_source_faithful_description(self) -> None:
        manifest_path = PLUGIN_ROOT / ".claude-plugin/plugin.json"
        self.assertTrue(manifest_path.is_file(), "plugin manifest is required")
        manifest = json.loads(read_text(manifest_path))
        self.assertEqual("ultrasolve", manifest.get("name"))
        self.assertEqual("Ultrasolve", manifest.get("displayName"))
        self.assertEqual("0.2.0", manifest.get("version"))
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
        stale = [
            path for path in standalone_files() if path.name in OLD_DOC_FILENAMES
        ]
        self.assertEqual([], stale, f"obsolete canonical documentation remains: {stale}")

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

    def test_standalone_marketplace_publishes_ultrasolve(self) -> None:
        self.assertTrue(
            STANDALONE_MARKETPLACE.is_file(),
            "standalone Claude marketplace manifest is required",
        )
        marketplace = json.loads(read_text(STANDALONE_MARKETPLACE))
        self.assertEqual(
            "https://json.schemastore.org/claude-code-marketplace.json",
            marketplace.get("$schema"),
        )
        self.assertEqual("matt-ramotar", marketplace.get("name"))
        self.assertEqual("0.2.0", marketplace.get("version"))
        self.assertEqual("Matt Ramotar", marketplace.get("owner", {}).get("name"))
        entries = marketplace.get("plugins", [])
        self.assertEqual(1, len(entries), "marketplace must expose exactly one plugin")
        self.assertEqual(
            {
                "name": "ultrasolve",
                "description": "Rigorous methods for solving the hardest problems.",
                "source": "./",
                "category": "productivity",
            },
            entries[0],
        )
        self.assertNotIn(
            "version",
            entries[0],
            "plugin.json remains the installed plugin-version authority",
        )

    def test_public_structural_artifacts_have_only_canonical_identity(self) -> None:
        artifacts = self.public_files()
        for path in artifacts:
            self.assertTrue(path.is_file(), f"missing structural artifact: {path}")
            structural_text = strip_url_destinations(read_text(path))
            relative = path.relative_to(PLUGIN_ROOT)
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

    def test_readme_records_publication_hold(self) -> None:
        readme = read_text(PLUGIN_ROOT / "README.md")
        self.assertRegex(
            re.sub(r"\s+", " ", readme),
            r"(?i)(?:publication.{0,40}\b(?:hold|held)\b|"
            r"\b(?:hold|held)\b.{0,40}publication)",
            "standalone documentation must preserve the publication hold",
        )

    def test_skill_surface_is_exactly_the_entries_and_six_leaves(self) -> None:
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
    def test_exactly_the_entries_are_model_invocable(self) -> None:
        for entry in MODEL_INVOCABLE:
            fields = frontmatter(self.claude_skill_path(entry))
            self.assertNotEqual("true", fields.get("disable-model-invocation", "").lower())
            self.assertTrue(
                self.codex_allows_implicit_invocation(entry),
                f"Codex must allow implicit invocation for entry {entry}",
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

    def test_router_loads_canonical_methods_and_preflights_entries(self) -> None:
        router = self.skill_text("solve")
        for leaf in LEAVES:
            self.assertEqual(1, router.count(f"references/methods/{leaf}.md"))
            self.assertNotIn(f"../{leaf}/SKILL.md", router)
        for entry in SKILLS:
            self.assertIn(f"`{entry}/SKILL.md`", router)
        self.assertIn("references/workflow-contract.md", markdown_links(router))
        normalized = re.sub(r"\s+", " ", router).lower()
        self.assertRegex(normalized, r"read every selected canonical module.{0,100}in full before constructing")
        self.assertRegex(normalized, r"do not invoke public leaf commands or read their entrypoints as a loading fallback")

    def test_router_enforces_the_shared_contract_and_map_back(self) -> None:
        router = re.sub(r"\s+", " ", self.skill_text("solve")).lower()
        shared = re.sub(r"\s+", " ", read_text(PORTABLE_ROOT / "solve/references/workflow-contract.md")).lower()
        for required in ("criterion ids", "fixed facts", "constraints", "non-goals", "authorized work", "remaining budget"):
            self.assertIn(required, router)
        for required in ("map-back checkpoint", "two full-method attempts total", "subproblems", "consumed", "partial or unsuccessful"):
            self.assertIn(required, router)
        for status in ("confirmed", "draft", "verified", "candidate", "partial", "infeasible", "blocked"):
            self.assertIn(status, shared)
        for evidence_kind in ("supplied evidence", "executed checks", "observed results", "derived conclusions", "proposed checks"):
            self.assertIn(evidence_kind, shared)
        self.assertIn("a test plan is not a passing test", shared)
        self.assertIn("do not call exhaustion proof of impossibility", shared)
        self.assertIn("two full attempts total", shared)


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
        path = PORTABLE_ROOT / "solve/references/worked-examples.md"
        text = re.sub(r"\s+", " ", read_text(path).lower())
        self.assertRegex(text, r"residual deficit.{0,100}(?:only )?while (?:a |the )?queue (?:remains|stays) backlogged")
        self.assertRegex(text, r"(?:queue (?:empties|drains).{0,80}deficit.{0,40}reset(?:s|ting)?(?: to)? zero|empty queue.{0,40}reset(?:s|ting)?.{0,40}deficit.{0,20}(?: to)? zero)")
        module = read_text(PORTABLE_ROOT / "solve/references/methods/analogize.md")
        self.assertNotIn("Deficit Round Robin", module, "domain instructions belong in examples")

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
            with self.subTest(leaf=leaf):
                entry = self.skill_text(leaf)
                self.assertIn("../solve/references/workflow-contract.md", markdown_links(entry))
                self.assertIn(f"../solve/references/methods/{leaf}.md", markdown_links(entry))
                self.assertNotIn("Full method", markdown_headings(entry))
                text = self.method_text(leaf)
                for heading in ("provenance", "shared entry contract", "cheap candidate", "full method", "result and map-back", "failure modes"):
                    self.assert_heading(text, rf"(?i){heading}", f"{leaf} lacks {heading}")
                self.assertIn("../workflow-contract.md", markdown_links(text))
                shared_entry = re.sub(r"\s+", " ", markdown_section(text, r"Shared entry contract")).lower()
                for inherited in ("original problem", "criterion ids", "fixed facts", "constraints", "non-goals", "authorized work", "open/assumed", "remaining effort"):
                    self.assertIn(inherited, shared_entry)

    def test_simplify_contract(self) -> None:
        text = self.method_text("simplify").lower()
        for required in ("constraints", "trivial", "skeleton", "one at a time", "map back"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)(?:restore|re-add).{0,180}constraints?.{0,100}one at a time|one at a time.{0,100}(?:restore|re-add).{0,180}constraints?")
        normalized = re.sub(r"\s+", " ", text)
        self.assertIn("first restoration that reintroduces difficulty under this order", normalized)
        self.assertIn("not necessarily a sole cause", normalized)
        self.assertIn("compare another restoration order", normalized)

    def test_analogize_contract(self) -> None:
        text = self.method_text("analogize").lower()
        for required in ("at least two", "fact", "mapping table", "break"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)(?:at least )?two.{0,80}candidate analog(?:y|ies).{0,180}(?:before|then).{0,80}(?:select|choose)")
        self.assertRegex(text, r"(?s)verif.{0,100}(?:source[- ]domain )?facts?.{0,240}mapping table")
        self.assertRegex(text, r"(?s)break.{0,160}(?:decision|limit|failure)")

    def test_restate_contract(self) -> None:
        text = self.method_text("restate").lower()
        for required in ("at least three", "fixed facts", "relaxation", "success criteria"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)(?:at least )?three.{0,100}(?:restatement|representation|viewpoint)")
        self.assertRegex(text, r"(?s)(?:label|mark).{0,80}(?:intentional )?relaxation")

    def test_generalize_contract(self) -> None:
        text = re.sub(r"\s+", " ", self.method_text("generalize")).lower()
        for required in ("shannon-derived", "result-first", "modern", "parameter", "instantiate", "yagni"):
            self.assertIn(required, text)
        self.assertIn("assess both forms for applicability", text)
        self.assertIn("if none is established, mark this form inapplicable", text)
        self.assertIn("if no such axis is useful, mark this form inapplicable", text)
        self.assertIn("when both apply, compare them and select", text)
        self.assertIn("when only one applies, select it without manufacturing the other", text)
        self.assertIn("if neither applies", text)
        self.assertIn("does not authorize a second full-method attempt", text)

    def test_decompose_contract(self) -> None:
        text = self.method_text("decompose").lower()
        for required in ("more than one", "seam", "rejected", "information yield", "recompose"):
            self.assertIn(required, text)
        self.assertRegex(text, r"(?s)more than one.{0,100}candidate seam.{0,220}(?:choose|select).{0,120}(?:strong|reject)")
        self.assertRegex(text, r"(?s)recompose.{0,160}(?:cross-cutting|original|constraints)")

    def test_invert_is_logically_safe_and_reenters_debugging(self) -> None:
        text = self.method_text("invert").lower()
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


class TestDefineContract(PluginContractTestCase):
    def define_text(self) -> str:
        return self.skill_text("define")

    def test_define_skill_has_house_structure(self) -> None:
        text = self.define_text()
        for heading in ("entry and boundaries", "proportional first response", "method", "compact example", "result and handoff", "provenance and failure checks"):
            self.assert_heading(text, rf"(?im)^{heading}$", f"define lacks {heading}")
        self.assertIn("../solve/references/workflow-contract.md", markdown_links(text))
        self.assertNotRegex("\n".join(markdown_headings(text)), r"(?i)map.?back")

    def test_define_preserves_authority_and_proportional_uncertainty(self) -> None:
        text = re.sub(r"\s+", " ", self.define_text().lower())
        shared = re.sub(r"\s+", " ", read_text(PORTABLE_ROOT / "solve/references/workflow-contract.md")).lower()
        for mark in ("confirmed", "open", "assumed"):
            self.assertIn(mark, shared)
        for required in ("observations, constraints, stakes, and proposals", "binding implementation choice remains a constraint", "effectiveness remains a hypothesis", "at most two unanswered questions", "250 words", "at most once", "never treat silence as agreement", "do not invent"):
            self.assertIn(required, text)
        for required in ("threshold", "observation horizon", "proposed and unresolved", "hypotheses may overlap", "joint mechanism", "insufficient-evidence outcome", "draft plan with explicit assumptions", "do not substitute it unilaterally"):
            self.assertIn(required, text)
        self.assertIn("do not demand a separate mandate when operational criteria suffice", text)
        self.assertIn("drafting a plan does not authorize implementing it", text)
        self.assertIn("until another why leaves the owner's actionable decision context", text)
        for required in ("metric artifact", "no continuing problem", "do-nothing or smallest credible", "outcome success distinct from artifact completion"):
            self.assertIn(required, text)

    def test_define_handoff_contract_is_lossless(self) -> None:
        text = re.sub(r"\s+", " ", markdown_section(self.define_text(), r"Result and handoff")).lower()
        for field in ("original contract", "criterion ids", "non-goals as constraints", "authorized work", "unresolved items with owners", "exact questions", "effort remaining"):
            self.assertIn(field, text)
        self.assertIn("definition and resolution statuses independently", text)
        self.assertRegex(text, r"cannot confirm an open or assumed stakeholder item")
        self.assertIn("do not send the same unchanged problem back", text)

    def test_router_adopts_define_contract(self) -> None:
        router = re.sub(r"\s+", " ", self.skill_text("solve").lower())
        self.assertIn("adopt an existing shared problem contract without reconstructing it", router)
        for carried in ("non-goals remain constraints", "open or assumed", "questions with owners and marks", "definition status", "remaining budget"):
            self.assertIn(carried, router)
        self.assertIn("do not demand a separate mandate", router)
        selection = re.sub(r"\s+", " ", read_text(PORTABLE_ROOT / "solve/references/technique-selection.md")).lower()
        self.assertIn("workflow-contract.md", selection)
        self.assertIn("open", selection)
        self.assertIn("assumed", selection)
        self.assertIn("operational", selection)
        self.assertIn("mandate", selection)

    def test_define_is_absent_from_lens_table(self) -> None:
        table = markdown_section(self.skill_text("solve"), r"canonical method modules")
        self.assertTrue(table, "router needs its canonical module table")
        self.assertNotIn("define", table.lower())
        self.assertEqual({f"references/methods/{leaf}.md" for leaf in LEAVES}, set(markdown_links(table)) - {"references/worked-examples.md"})

    def test_define_provenance_disclaims_shannon(self) -> None:
        text = re.sub(r"\s+", " ", self.define_text())
        self.assertIn("Nothing derives from Shannon's 1952 talk", text)
        for source in ("Polya", "Duncker", "Keeney", "Chamberlin", "Platt", "Heuer"):
            self.assertIn(source, text)


class TestDocumentationAndEvals(PluginContractTestCase):
    """Public documentation and immutable v1 fixture shape, not current behavior."""
    def grader_path(self, case: str, stem: str) -> Path:
        return PLUGIN_ROOT / "evals/behavioral/v1" / case / "graders" / f"{stem}.md"

    def test_readme_exposes_exactly_the_final_commands(self) -> None:
        readme = PLUGIN_ROOT / "README.md"
        self.assertTrue(readme.is_file(), "README is required")
        text = read_text(readme)
        commands = set(re.findall(r"/ultrasolve:([a-z-]+)", text))
        self.assertEqual(set(SKILLS), commands)
        self.assertNotRegex(
            text.lower(),
            r"(?<![a-z0-9_/.-])/(?:shannon|creative-thinking|hard-problems)(?:[\s:`-]|$)",
        )

    def test_readme_links_standalone_testing_guidance(self) -> None:
        readme = PLUGIN_ROOT / "README.md"
        links = {((readme.parent / target).resolve()) for target in markdown_links(read_text(readme))}
        self.assertIn((PLUGIN_ROOT / "TESTING.md").resolve(), links)
        self.assertIn((PLUGIN_ROOT / "agent-skills").resolve(), links)

    def test_relative_markdown_links_resolve_in_standalone_tree(self) -> None:
        documents = [path for path in standalone_files() if path.suffix == ".md"]
        for document in documents:
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

        for case in (
            "activation",
            "router-read-order",
            "nonactivation",
            "debugging-boundary",
            "define-activation",
            "define-nonactivation",
        ):
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

        for case in ("nonactivation", "debugging-boundary", "define-activation"):
            no_solve = frontmatter(self.grader_path(case, "no-solve"))
            self.assertEqual("tool_used", no_solve.get("type"))
            self.assertEqual("Skill", no_solve.get("tool"))
            self.assertIn("ultrasolve:solve", no_solve.get("input_match", ""))
            self.assertEqual("0", no_solve.get("min"))
            self.assertEqual("0", no_solve.get("max"))
            self.assertEqual("both", no_solve.get("arm"))

        automatic_define = frontmatter(
            self.grader_path("define-activation", "automatic-define")
        )
        self.assertEqual("tool_used", automatic_define.get("type"))
        self.assertEqual("Skill", automatic_define.get("tool"))
        self.assertIn("ultrasolve:define", automatic_define.get("input_match", ""))
        self.assertEqual("1", automatic_define.get("min"))
        self.assertEqual("with-only", automatic_define.get("arm"))

        no_define = frontmatter(self.grader_path("define-nonactivation", "no-define"))
        self.assertEqual("tool_used", no_define.get("type"))
        self.assertEqual("Skill", no_define.get("tool"))
        self.assertIn("ultrasolve:define", no_define.get("input_match", ""))
        self.assertEqual("0", no_define.get("min"))
        self.assertEqual("0", no_define.get("max"))
        self.assertEqual("both", no_define.get("arm"))

        for case, direction in (
            ("activation", "solve"),
            ("nonactivation", "ordinary-work"),
            ("debugging-boundary", "diagnosis"),
        ):
            with self.subTest(case=case):
                grader = self.grader_path(case, "no-define")
                fields = frontmatter(grader)
                self.assertEqual("tool_used", fields.get("type"))
                self.assertEqual("Skill", fields.get("tool"))
                self.assertEqual("ultrasolve:define", fields.get("input_match"))
                self.assertEqual("0", fields.get("min"))
                self.assertEqual("0", fields.get("max"))
                self.assertEqual("both", fields.get("arm"))
                _, body = frontmatter_parts(grader)
                self.assertEqual(
                    "The define skill must not fire on this case; "
                    f"it guards the {direction} direction of the define boundary.",
                    body,
                )

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
            for path in standalone_files()
            if path.suffix in {".md", ".json", ".yaml", ".yml", ".py"}
        ]
        self.assertTrue(artifacts, "expected standalone plugin text artifacts")
        for path in artifacts:
            self.assertTrue(path.is_file(), f"missing text artifact: {path}")
            data = path.read_bytes()
            self.assertTrue(data.endswith(b"\n"), f"{path} must end with one newline")
            self.assertFalse(data.endswith(b"\n\n"), f"{path} must end with exactly one newline")
            for number, line in enumerate(data.splitlines(), start=1):
                self.assertFalse(line.rstrip(b" \t") != line, f"trailing whitespace: {path}:{number}")


if __name__ == "__main__":
    unittest.main()
