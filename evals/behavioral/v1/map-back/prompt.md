---
max_turns: 12
timeout_seconds: 360
allowed_tools: [Read]
---

/ultrasolve:solve Recommend a production configuration migration. It must
require zero changes to 200 deployed clients, preserve uninterrupted reads,
and support rollback for 30 days. A one-client prototype works by changing
that client to read a new endpoint. What should ship?
