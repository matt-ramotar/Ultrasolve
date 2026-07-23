---
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read]
---

Leadership approved rewriting our nightly billing reconciliation job on Spark
after it overran its processing window three times last month, once delaying
customer invoices. The platform review is tomorrow morning and I need the
rewrite plan today: cluster sizing, a parallel-run pilot, phased cutover, and
decommission of the existing cron pipeline.
