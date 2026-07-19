---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read]
---

/ultrasolve:simplify Invalidate tenant cache entries across three regions
within five seconds while preserving soft deletes, per-tenant TTL overrides,
and race-safe warm-up. Replication is asynchronous, versions are monotonic,
and synchronous global broadcast is unavailable.
