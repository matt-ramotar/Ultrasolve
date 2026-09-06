"""Structural contracts for runtime files, not model behavior.

The parsers accept the repository's restricted metadata forms.
The audit checks paths, metadata, and method placement. It does not interpret prose.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


SKILLS = ("solve", "define", "simplify", "analogize", "restate", "generalize", "decompose", "invert")
MODEL_INVOCABLE = SKILLS[:2]
LEAVES = SKILLS[2:]
VERSION = "0.2.0"
ISSUE_CODES = frozenset({
    "ENTRYPOINT_SET", "WRAPPER_TARGET", "ACTIVATION_POLICY", "DESCRIPTION_PARITY",
    "VERSION_PARITY", "RESOURCE_MISSING", "METHOD_BODY_DUPLICATED",
})


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
    """Parse the repository's two-level agents/openai.yaml shape."""

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


def runtime_relative_paths() -> tuple[str, ...]:
    """The frozen 42-file runtime surface; every listed file is audited below."""
    paths = [
        ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
        ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "PRIVACY.md", "LICENSE",
        "agent-skills/define/references/problem-posing-sources.md",
        "agent-skills/define/references/worked-example.md",
    ]
    paths.extend(f"agent-skills/{name}/SKILL.md" for name in SKILLS)
    paths.extend(f"agent-skills/{name}/agents/openai.yaml" for name in SKILLS)
    paths.extend(f"adapters/claude/skills/{name}/SKILL.md" for name in SKILLS)
    paths.extend(f"agent-skills/solve/references/methods/{name}.md" for name in LEAVES)
    paths.extend(f"agent-skills/solve/references/{name}.md" for name in (
        "workflow-contract", "technique-selection", "shannon-source-notes", "worked-examples",
    ))
    return tuple(sorted(paths))


def repository_files(root: Path) -> list[Path]:
    """Include development documents for link/hygiene checks, excluding Git/caches."""
    files = []
    for directory, directories, filenames in os.walk(root):
        directories[:] = [name for name in directories if name not in {".git", "__pycache__"}]
        files.extend(Path(directory) / name for name in filenames)
    return sorted(files)


def public_contract_files(root: Path) -> list[Path]:
    """Runtime plus maintained user documentation; not plans or evaluator answers."""
    relatives = (*runtime_relative_paths(), "README.md", "TESTING.md")
    return [root / relative for relative in relatives if (root / relative).is_file()]


def full_method_sections(text: str) -> list[str]:
    """Locate the conventional full-method sections, ignoring incidental prose."""
    return re.findall(r"(?ms)^## (?:Full method|Method)[ \t]*\n(.*?)(?=^## |\Z)", text)


def wrapper_delegates_to(text: str, target: str) -> bool:
    """Check the restricted one-loader wrapper shape, without freezing its prose."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return False
    try:
        end = lines.index("---", 1)
    except ValueError:
        return False
    body = "\n".join(lines[end + 1:])
    targets = re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/[^\s`]+", body)
    loaders = re.findall(r"(?im)^(?:read|load)\s+", body)
    return (
        targets == [target]
        and len(loaders) == 1
        and re.search(rf"(?im)^(?:read|load)\s+`{re.escape(target)}`(?:[\s.,;:]|$)", body) is not None
        and len(text.splitlines()) <= 16
        and not full_method_sections(body)
    )


def audit_runtime_contract(root: Path) -> list[dict]:
    """Inspect actual entrypoints, metadata, resources, and full-method placement.

    Returned paths are repository-relative and results are deterministic. Passing
    establishes these structural obligations only, not method semantics or usage.
    """
    root = Path(root).resolve()
    issues = []

    def issue(code: str, path: Path, message: str) -> None:
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            relative = str(path)
        record = {"code": code, "path": relative, "message": message}
        if record not in issues:
            issues.append(record)

    texts = {}
    for relative in runtime_relative_paths():
        path = root / relative
        try:
            texts[relative] = read_text(path)
        except (OSError, UnicodeError) as error:
            issue("RESOURCE_MISSING", path, f"required runtime resource cannot be read: {error}")

    for relative in ("agent-skills", "adapters/claude/skills"):
        directory = root / relative
        actual = {path.name for path in directory.iterdir() if path.is_dir()} if directory.is_dir() else set()
        if actual != set(SKILLS):
            issue("ENTRYPOINT_SET", directory, f"expected eight entries; found {sorted(actual)}")
    for relative in ("skills", "commands"):
        if (root / relative).exists():
            issue("ENTRYPOINT_SET", root / relative, "duplicate default discovery surface is present")

    manifests = (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/marketplace.json")
    for relative in manifests:
        if relative not in texts:
            continue
        try:
            value = json.loads(texts[relative])
            actual = value.get("version") if isinstance(value, dict) else None
        except (ValueError, TypeError):
            actual = None
        if actual != VERSION:
            issue("VERSION_PARITY", root / relative, f"runtime version must be {VERSION}")

    for name in SKILLS:
        entry = root / f"agent-skills/{name}/SKILL.md"
        wrapper = root / f"adapters/claude/skills/{name}/SKILL.md"
        metadata = root / f"agent-skills/{name}/agents/openai.yaml"
        entry_fields = {}
        wrapper_fields = {}
        for path, fields in ((entry, entry_fields), (wrapper, wrapper_fields)):
            if path.relative_to(root).as_posix() not in texts:
                continue
            try:
                fields.update(frontmatter(path))
            except (AssertionError, OSError, UnicodeError) as error:
                code = "ACTIVATION_POLICY" if path == wrapper else "ENTRYPOINT_SET"
                issue(code, path, f"invalid entry metadata: {error}")
            if fields.get("name") != name:
                issue("ENTRYPOINT_SET", path, f"entry name must be {name}")
        wrapper_text = texts.get(wrapper.relative_to(root).as_posix())
        if wrapper_text is not None:
            target = f"${{CLAUDE_PLUGIN_ROOT}}/agent-skills/{name}/SKILL.md"
            if not wrapper_delegates_to(wrapper_text, target):
                issue("WRAPPER_TARGET", wrapper, "wrapper must delegate once to its matching canonical entry and remain thin")
            expected = "true" if name in LEAVES else None
            if wrapper_fields.get("disable-model-invocation") != expected:
                issue("ACTIVATION_POLICY", wrapper, "Claude invocation flag disagrees with the two-entry/six-leaf policy")
            if entry_fields.get("description") != wrapper_fields.get("description"):
                issue("DESCRIPTION_PARITY", wrapper, "wrapper and canonical activation descriptions differ")
        if metadata.relative_to(root).as_posix() in texts:
            try:
                sections = simple_yaml_sections(metadata)
                actual = sections.get("policy", {}).get("allow_implicit_invocation")
            except (AssertionError, OSError, UnicodeError):
                actual = None
            expected = "true" if name in MODEL_INVOCABLE else "false"
            if actual != expected:
                issue("ACTIVATION_POLICY", metadata, "Codex implicit invocation flag disagrees with the two-entry/six-leaf policy")

    module_dir = root / "agent-skills/solve/references/methods"
    for name in LEAVES:
        module = module_dir / f"{name}.md"
        entry = root / f"agent-skills/{name}/SKILL.md"
        module_text = texts.get(module.relative_to(root).as_posix())
        if module_text is not None:
            count = len(full_method_sections(module_text))
            if count == 0:
                issue("RESOURCE_MISSING", module, "canonical module has no full-method section")
            elif count != 1:
                issue("METHOD_BODY_DUPLICATED", module, "canonical module contains multiple full-method sections")
        entry_text = texts.get(entry.relative_to(root).as_posix(), "")
        if full_method_sections(entry_text):
            issue("METHOD_BODY_DUPLICATED", entry, "public leaf entry contains a full method instead of delegating")
    if module_dir.is_dir():
        for path in sorted(module_dir.rglob("*.md")):
            if path.name not in {f"{name}.md" for name in LEAVES} or path.parent != module_dir:
                issue("METHOD_BODY_DUPLICATED", path, "unexpected method module outside the six canonical full bodies")

    for relative, text in texts.items():
        path = root / relative
        if path.suffix != ".md":
            continue
        for target in markdown_links(text):
            resolved = (path.parent / target).resolve()
            if not resolved.is_file() or root.resolve() not in resolved.parents:
                issue("RESOURCE_MISSING", resolved, f"required runtime link from {relative} does not resolve inside the collection: {target}")
    return sorted(issues, key=lambda item: (item["code"], item["path"], item["message"]))
