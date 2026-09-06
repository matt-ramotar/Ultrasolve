"""Build the static evaluation artifact; this does not establish agent isolation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


SKILLS = ("define", "solve", "simplify", "analogize", "restate", "generalize", "decompose", "invert")
LEAVES = SKILLS[2:]
EXPECTED_FILES = tuple(sorted([
    ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "LICENSE", "PRIVACY.md",
    *[f"agent-skills/{name}/SKILL.md" for name in SKILLS],
    *[f"agent-skills/{name}/agents/openai.yaml" for name in SKILLS],
    *[f"adapters/claude/skills/{name}/SKILL.md" for name in SKILLS],
    *[f"agent-skills/solve/references/methods/{name}.md" for name in LEAVES],
    "agent-skills/solve/references/workflow-contract.md",
    "agent-skills/solve/references/technique-selection.md",
    "agent-skills/solve/references/shannon-source-notes.md",
    "agent-skills/solve/references/worked-examples.md",
    "agent-skills/define/references/problem-posing-sources.md",
    "agent-skills/define/references/worked-example.md",
]))
MARKER = ".ultrasolve-bundle-incomplete"


class BundleError(ValueError):
    """A rejected build with a stable machine-readable reason."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


def _reject_symlinks(path: Path) -> None:
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        if current.is_symlink():
            raise BundleError("SOURCE_SYMLINK", f"Source path contains a symlink: {current}")


def _read_input(path: Path) -> bytes:
    _reject_symlinks(path)
    try:
        if not path.is_file():
            raise BundleError("SOURCE_MISSING", f"Required input is not a readable regular file: {path}")
        return path.read_bytes()
    except OSError as error:
        raise BundleError("SOURCE_MISSING", f"Cannot read required input {path}: {error}") from error


def _unique_object(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_allowlist(source: Path) -> list[str]:
    raw = _read_input(source / "evals/runtime-files.json")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (ValueError, UnicodeError) as error:
        raise BundleError("ALLOWLIST_INVALID", f"Malformed runtime allowlist: {error}") from error
    if (not isinstance(data, dict) or set(data) != {"schema_version", "files"}
            or type(data["schema_version"]) is not int or data["schema_version"] != 1
            or not isinstance(data["files"], list)):
        raise BundleError("ALLOWLIST_INVALID", "Expected schema_version 1 and an explicit files array")
    files = data["files"]
    seen = set()
    for name in files:
        if (not isinstance(name, str) or not name or "\\" in name or "\x00" in name
                or ":" in name or name.startswith("/") or ".." in name.split("/")):
            raise BundleError("ALLOWLIST_INVALID", f"Unsafe runtime path: {name!r}")
        normalized = PurePosixPath(name).as_posix()
        if normalized in seen or normalized != name:
            raise BundleError("ALLOWLIST_INVALID", f"Duplicate or noncanonical runtime path: {name!r}")
        seen.add(normalized)
    if files != sorted(files) or tuple(files) != EXPECTED_FILES:
        missing = sorted(set(EXPECTED_FILES) - seen)
        prohibited = sorted(seen - set(EXPECTED_FILES))
        raise BundleError("ALLOWLIST_INVALID", f"Allowlist must contain exactly the 42 sorted runtime files; missing={missing}, prohibited={prohibited}")
    return files


def _resource_target(
    base: str, value: str, known: set[str], context: str,
    *, kind: str = "file", allow_external: bool = False,
) -> None:
    """Resolve the corpus's local file/directory references against copied paths."""
    if not isinstance(value, str) or not value:
        raise BundleError("RESOURCE_MISSING", f"Invalid runtime reference in {context}: {value!r}")
    try:
        parts = urlsplit(value)
    except ValueError as error:
        raise BundleError("RESOURCE_MISSING", f"Invalid runtime reference in {context}: {value}") from error
    if allow_external and parts.scheme in {"http", "https", "mailto"}:
        return
    if parts.scheme or parts.netloc:
        raise BundleError("RESOURCE_MISSING", f"Unsupported runtime reference in {context}: {value}")
    reference = unquote(parts.path)
    if not reference and allow_external and parts.fragment:
        return  # An in-document fragment does not add a file dependency.
    if not reference:
        raise BundleError("RESOURCE_MISSING", f"Empty runtime dependency in {context}: {value}")
    if reference.startswith("/") or "\\" in reference or "\x00" in reference:
        raise BundleError("RESOURCE_MISSING", f"Runtime reference escapes the bundle in {context}: {value}")
    target = posixpath.normpath(posixpath.join(base, reference))
    if target == ".." or target.startswith("../"):
        raise BundleError("RESOURCE_MISSING", f"Runtime reference escapes the bundle in {context}: {value}")
    directory = target == "." or any(name.startswith(target.rstrip("/") + "/") for name in known)
    present = ((kind == "file" and target in known)
               or (kind == "directory" and directory)
               or (kind == "any" and (target in known or directory)))
    if not present:
        raise BundleError("RESOURCE_MISSING", f"Required runtime reference is absent from the bundle: {context} -> {value}")


def _validate_resources(payloads: dict[str, bytes]) -> None:
    known = set(payloads)
    for name, raw in payloads.items():
        if not name.endswith(".md"):
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeError as error:
            raise BundleError("RESOURCE_MISSING", f"Runtime Markdown is not UTF-8: {name}") from error
        base = str(PurePosixPath(name).parent)
        # Check the corpus's inline links and reference definitions, including
        # explicit/collapsed reference uses. This is dependency closure, not rendering.
        for angle, plain in re.findall(r"\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))", text):
            _resource_target(base, angle or plain, known, name, kind="any", allow_external=True)
        definitions = set()
        for label, angle, plain in re.findall(r"(?m)^ {0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))", text):
            definitions.add(" ".join(label.split()).casefold())
            _resource_target(base, angle or plain, known, name, kind="any", allow_external=True)
        for label, reference in re.findall(r"\[([^\]\n]+)\]\[([^\]\n]*)\]", text):
            key = " ".join((reference or label).split()).casefold()
            if key not in definitions:
                raise BundleError("RESOURCE_MISSING", f"Undefined runtime reference in {name}: {reference or label}")
        for code in re.findall(r"`([^`\n]+)`", text):
            if code.startswith("${CLAUDE_PLUGIN_ROOT}/"):
                _resource_target(".", code.removeprefix("${CLAUDE_PLUGIN_ROOT}/"), known, name)
            elif code.endswith(".md"):
                code_base = base
                if name == "agent-skills/solve/SKILL.md" and re.fullmatch(r"[^/]+/SKILL\.md", code):
                    code_base = "agent-skills"  # Router explicitly declares collection-relative entries.
                elif name == "agent-skills/solve/references/technique-selection.md" and "/" not in code:
                    code_base += "/methods"  # This table declares module basenames under methods/.
                _resource_target(code_base, code, known, name)
    try:
        codex = json.loads(payloads[".codex-plugin/plugin.json"], object_pairs_hook=_unique_object)
        claude = json.loads(payloads[".claude-plugin/plugin.json"], object_pairs_hook=_unique_object)
        _resource_target(".", codex["skills"], known, ".codex-plugin/plugin.json skills", kind="directory")
        if not isinstance(claude["skills"], list) or not claude["skills"]:
            raise ValueError("Claude skills must be a nonempty path list")
        for path in claude["skills"]:
            _resource_target(".", path, known, ".claude-plugin/plugin.json skills", kind="directory")
        for name in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            data = json.loads(payloads[name], object_pairs_hook=_unique_object)
            for plugin in data["plugins"]:
                path = plugin["source"]
                if isinstance(path, dict):
                    path = path["path"]
                _resource_target(".", path, known, name, kind="directory")
    except (KeyError, TypeError, ValueError, UnicodeError) as error:
        if isinstance(error, BundleError):
            raise
        raise BundleError("RESOURCE_MISSING", f"Invalid runtime manifest dependency: {error}") from error


def _destinations(source: Path, output: Path, manifest: Path) -> tuple[Path, Path]:
    try:
        if output.is_symlink() or manifest.is_symlink():
            raise BundleError("DESTINATION_INVALID", "Output and manifest must not be symlinks")
        output, manifest = output.resolve(), manifest.resolve()
        if (output.is_relative_to(source) or source.is_relative_to(output)
                or manifest.is_relative_to(source) or manifest.is_relative_to(output)
                or output.is_relative_to(manifest)):
            raise BundleError("DESTINATION_INVALID", "Output and manifest must be separate, and outside the source tree")
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise BundleError("DESTINATION_INVALID", f"Output must be absent or an empty directory: {output}")
        if manifest.exists():
            raise BundleError("DESTINATION_INVALID", f"Manifest destination already exists: {manifest}")
        for parent in (*output.parents, *manifest.parents):
            if parent.exists() and not parent.is_dir():
                raise BundleError("DESTINATION_INVALID", f"Destination parent is not a directory: {parent}")
        return output, manifest
    except OSError as error:
        raise BundleError("DESTINATION_INVALID", f"Cannot validate destinations: {error}") from error


def _git_metadata(source: Path) -> tuple[str, object]:
    """Read optional Git provenance without refreshing or mutating the index."""
    if not (source / ".git").exists() or (source / ".git").is_symlink():
        return "unknown", "unknown"

    def git(*arguments: str) -> str:
        return subprocess.run(
            ["git", "--no-optional-locks", "-C", str(source), *arguments],
            check=True, capture_output=True, text=True, timeout=5,
        ).stdout.strip()

    try:
        if Path(git("rev-parse", "--show-toplevel")).resolve() != source:
            return "unknown", "unknown"
        revision = git("rev-parse", "--verify", "HEAD")
        dirty = bool(git("status", "--porcelain", "--untracked-files=normal"))
        return revision, dirty
    except (OSError, subprocess.SubprocessError):
        return "unknown", "unknown"


def _identity(path: Path) -> tuple[int, int]:
    info = path.lstat()
    return info.st_dev, info.st_ino


def _ensure_directory(path: Path, created: dict) -> None:
    missing = []
    current = path
    while not current.exists():
        if current.is_symlink():
            raise OSError(f"Destination changed to a symlink: {current}")
        missing.append(current)
        current = current.parent
    if not current.is_dir() or current.is_symlink():
        raise OSError(f"Destination parent is not a real directory: {current}")
    for directory in reversed(missing):
        directory.mkdir()
        created[directory] = _identity(directory)


def _write_file(path: Path, data: bytes, created_files: dict) -> None:
    with path.open("xb") as stream:
        info = os.fstat(stream.fileno())
        created_files[path] = (info.st_dev, info.st_ino)
        stream.write(data)


def _rollback(files: dict, directories: dict, output: Path) -> None:
    """Remove only inodes created here; retain an incomplete marker if cleanup fails."""
    for path, identity in reversed(list(files.items())):
        try:
            if _identity(path) == identity and stat.S_ISREG(path.lstat().st_mode):
                path.unlink()
        except OSError:
            pass
    for path, identity in reversed(list(directories.items())):
        try:
            if _identity(path) == identity:
                path.rmdir()
        except OSError:
            pass
    try:
        if output.is_dir() and any(output.iterdir()):
            marker = output / MARKER
            with marker.open("xb") as stream:
                stream.write(b"Incomplete bundle: this build failed; no completed manifest was published.\n")
    except OSError:
        pass


def build_bundle(source: Path, output: Path, manifest_output: Path) -> dict:
    """Copy exactly 42 validated runtime files and publish an external manifest.

    Existing nonempty output and any existing manifest are preserved and rejected.
    An existing empty output directory is usable. Git metadata is optional; file
    content identity is independent of location, provenance, and filesystem time.
    This validates bundle composition, not a subject agent's filesystem isolation.
    """
    source = Path(os.path.abspath(source))
    _reject_symlinks(source)
    if not source.is_dir():
        raise BundleError("SOURCE_MISSING", f"Source directory is missing: {source}")
    source = source.resolve()
    files = _load_allowlist(source)
    output, manifest_output = _destinations(source, Path(output), Path(manifest_output))
    # Snapshot every allowed byte and validate reference closure before any copying.
    payloads = {name: _read_input(source / name) for name in files}
    _validate_resources(payloads)
    revision, dirty = _git_metadata(source)
    records = [{"path": name, "bytes": len(payloads[name]), "sha256": hashlib.sha256(payloads[name]).hexdigest()} for name in files]
    content = json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    manifest = {
        "schema_version": 1,
        "verification": "bundle composition verified",
        "files": records,
        "source_revision": revision,
        "source_dirty": dirty,
        "content_sha256": hashlib.sha256(content).hexdigest(),
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    created_files: dict = {}
    created_directories: dict = {}
    temporary_manifest = None
    try:
        _ensure_directory(output, created_directories)
        # Recheck after parent creation; exclusive writes never overwrite late arrivals.
        if any(output.iterdir()):
            raise OSError(f"Output became nonempty during the build: {output}")
        marker = output / MARKER
        _write_file(marker, b"Incomplete bundle; no completed manifest has been published.\n", created_files)
        for name, data in payloads.items():
            target = output / name
            _ensure_directory(target.parent, created_directories)
            _write_file(target, data, created_files)
        _ensure_directory(manifest_output.parent, created_directories)
        fd, temporary = tempfile.mkstemp(prefix=".ultrasolve-manifest-", dir=manifest_output.parent)
        temporary_manifest = Path(temporary)
        with os.fdopen(fd, "wb") as stream:
            info = os.fstat(stream.fileno())
            created_files[temporary_manifest] = (info.st_dev, info.st_ino)
            stream.write(manifest_bytes)
            stream.flush()
            os.fsync(stream.fileno())
        marker.unlink()
        # Same-directory hard-link publication is atomic and refuses an existing path.
        # Register the prospective inode first: link may take effect before an
        # interruption is reported. Rollback must remove ours, never another writer's.
        created_files[manifest_output] = created_files[temporary_manifest]
        os.link(temporary_manifest, manifest_output)
    except BaseException as error:
        _rollback(created_files, created_directories, output)
        if isinstance(error, OSError):
            raise BundleError("COPY_FAILED", f"Could not finish the bundle: {error}") from error
        raise
    finally:
        if temporary_manifest is not None:
            try:
                if _identity(temporary_manifest) == created_files.get(temporary_manifest):
                    temporary_manifest.unlink()
            except OSError:
                pass
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest-output", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest = build_bundle(args.source, args.output, args.manifest_output)
    except BundleError as error:
        print(f"{error.code}: {error}", file=sys.stderr)
        return 2
    print(f"bundle composition verified: {len(manifest['files'])} files; {manifest['content_sha256']}")
    print("This does not establish an agent filesystem isolation boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
