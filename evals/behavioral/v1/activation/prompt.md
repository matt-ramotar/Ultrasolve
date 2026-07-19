---
max_turns: 12
timeout_seconds: 360
allowed_tools: [Read]
---

Design a permission-resolution model with all of these fixed requirements:
delegated administration, custom roles, break-glass access with immutable audit,
and p99 resolution under 5 ms. Three prototypes have failed: runtime graph
traversal misses latency, flattened grants make revocation too slow, and a
role-only model cannot express delegation. Produce a defensible design and
verify it against every requirement.
