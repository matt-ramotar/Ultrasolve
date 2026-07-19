---
type: tool_used
weight: 1
tool: Read
input_match: '"file_path"\s*:\s*"[^"]*/agent-skills/decompose/SKILL\.md"'
min: 1
arm: with-only
---

Deterministically require a Read whose serialized input ends in the selected
leaf path `${CLAUDE_PLUGIN_ROOT}/agent-skills/decompose/SKILL.md`.
