---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read]
---

/ultrasolve:restate The gateway needs smarter retries. Fixed facts:
transport is at-least-once and some downstream operations are not idempotent.
Original success criteria: at most six total downstream attempts per client
request, no multiplicative retries across hops, and unchanged external timeout
and failure semantics.
