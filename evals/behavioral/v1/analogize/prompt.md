---
max_turns: 12
timeout_seconds: 360
allowed_tools: [Read]
---

/ultrasolve:analogize Design fair allocation of heterogeneous CI runners
among weighted team queues. Job duration is unknown at dispatch, jobs are
non-preemptive, multiple compatible runners can become free concurrently, and
FIFO within each team and runner class must be preserved. Propose and justify a
scheduler.

For reproducibility, treat these as the supplied source facts for deficit
round robin (DRR): it visits active flow queues round-robin, preserves FIFO
within each flow queue, sends a whole head packet only when its complete known
size fits the queue's deficit, and carries residual deficit across rounds only
while that queue remains backlogged. When a queue empties, its deficit resets
to zero. DRR neither provides global FIFO nor preempts an in-flight packet.
These facts come from
[the original DRR paper](https://dl.acm.org/doi/10.1145/217382.217453) and the
[IETF account in RFC 7806](https://www.rfc-editor.org/rfc/rfc7806.html#section-2.2.4).
