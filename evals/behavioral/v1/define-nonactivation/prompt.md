---
max_turns: 6
timeout_seconds: 300
allowed_tools: [Read]
---

We already agreed the problem and the success criteria: at most six total
downstream attempts per client request, no multiplicative retries across hops,
unchanged external timeout and failure semantics. Fixed facts: transport is
at-least-once and some downstream operations are not idempotent. Three
formulation attempts all collapse into the same per-hop counter design. Get us
a genuinely different way to look at it.
