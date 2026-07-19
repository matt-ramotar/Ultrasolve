---
max_turns: 10
timeout_seconds: 300
allowed_tools: []
---

A reproducible checkout failure returns HTTP 500 only when two coupons are
present. We have a failing test, request traces, and a stack trace pointing to
discount aggregation, but the trace does not record intermediate coupon values
and no relevant source lines are supplied. Plan the next diagnosis and
verification steps from the available evidence.
