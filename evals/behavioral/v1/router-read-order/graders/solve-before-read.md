---
type: tool_order
weight: 1
before:
  tool: Skill
  input_match: 'ultrasolve:solve'
after:
  tool: Read
  input_match: '"file_path"\s*:\s*"[^"]*/agent-skills/decompose/SKILL\.md"'
arm: with-only
---

Deterministically require the `solve` Skill call to precede the router's Read
call. Exact selected-leaf matching is enforced by `read-decompose.md`.
