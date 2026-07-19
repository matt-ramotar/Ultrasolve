---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read]
---

/ultrasolve:invert Plan a zero-downtime database migration. The end state is
one authoritative new schema with old clients retired, but the current state
has mixed-version clients, dual reads are allowed, writes cannot be paused, and
rollback must remain possible until reconciliation passes. Produce a migration
plan.
