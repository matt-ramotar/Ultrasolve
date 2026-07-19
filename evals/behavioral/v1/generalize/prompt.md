---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read]
---

/ultrasolve:generalize Reason about merging exactly two user accounts. The
system already solved organization renames with stable aliases to a canonical
ID. User merge must preserve foreign keys, audit history, authorization,
idempotency, and rollback, and the shipped scope must remain the two-account
operation.
