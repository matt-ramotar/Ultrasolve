# Provider-Neutral Activation Matrix

Each case records one self-contained provider-neutral prompt and its expected
result in a fresh session with the complete eight-skill collection installed.
The expectations are not evidence that any particular client passes them.

## `automatic-solve`

Stimulus: Design a permission-resolution model with all of these fixed requirements: delegated administration, custom roles, break-glass access with immutable audit, and p99 resolution under 5 ms. Three prototypes have failed: runtime graph traversal misses latency, flattened grants make revocation too slow, and a role-only model cannot express delegation. Produce a defensible design and verify it against every requirement.

Expected outcome: The solve router activates automatically for the genuinely stuck problem, establishes the contract, and routes through a suitable lens.

## `ordinary-nonactivation`

Stimulus: Our first draft of a TypeScript clamp helper failed one range-validation test. Write clamp(value, minimum, maximum) so it rejects an inverted range and otherwise returns the value constrained to the inclusive range. Include three concise example assertions.

Expected outcome: The solve router does not activate for ordinary work or a single failed attempt; the client handles the request directly.

## `debugging-boundary`

Stimulus: A reproducible checkout failure returns HTTP 500 only when two coupons are present. We have a failing test, request traces, and a stack trace pointing to discount aggregation, but the trace does not record intermediate coupon values and no relevant source lines are supplied. Plan the next diagnosis and verification steps from the available evidence.

Expected outcome: The solve router does not activate; the work returns to evidence-led diagnosis, using bounded hypotheses only to guide observation and isolation.

## `automatic-define`

Stimulus: Leadership approved rewriting our nightly billing reconciliation job on Spark after it overran its processing window three times last month, once delaying customer invoices. The platform review is tomorrow morning and I need the rewrite plan today: cluster sizing, a parallel-run pilot, phased cutover, and decommission of the existing cron pipeline.

Expected outcome: The definition method activates automatically for the solution-shaped request and returns a problem contract with observable success criteria and a decision point, not the requested rewrite plan.

## `direct-define`

Stimulus: Direct invocation of define: Search feels broken since the redesign and the CEO wants it fixed. Leadership approved an Elasticsearch migration off our Postgres full-text stack; produce the migration plan by Friday. Support tickets mentioning search doubled last month.

Expected outcome: The definition method define loads and applies its full method, producing a problem contract whose candidate register carries the approved migration as one row among alternatives.

## `define-nonactivation`

Stimulus: We already agreed the problem and the success criteria: at most six total downstream attempts per client request, no multiplicative retries across hops, unchanged external timeout and failure semantics. Fixed facts: transport is at-least-once and some downstream operations are not idempotent. Three formulation attempts all collapse into the same per-hop counter design. Get us a genuinely different way to look at it.

Expected outcome: The definition method does not activate; the defined problem is worked directly or routed toward reformulation of its formulation rut.

## `define-delegated-nonactivation`

Stimulus: Write a Terraform module for a new EKS cluster from this complete, reviewed specification: accept VPC ID and private subnet IDs as inputs; use AWS provider 5.x; create system, application, and batch managed node groups with 3 to 6 m7i.large, 6 to 24 m7i.xlarge, and 0 to 40 c7i.2xlarge Spot nodes respectively; enable IRSA and pin Kubernetes 1.33.

Expected outcome: The definition method does not activate for the fully specified request; the task proceeds as ordinary work.

## `explicit-simplify`

Stimulus: Explicit invocation of simplify: Invalidate tenant cache entries across three regions within five seconds while preserving soft deletes, per-tenant TTL overrides, and race-safe warm-up. Replication is asynchronous, versions are monotonic, and synchronous global broadcast is unavailable.

Expected outcome: Explicit invocation loads and applies simplify; it is not eligible for automatic activation.

## `explicit-analogize`

Stimulus: Explicit invocation of analogize: Design fair allocation of heterogeneous CI runners among weighted team queues. Job duration is unknown at dispatch, jobs are non-preemptive, multiple compatible runners can become free concurrently, and FIFO within each team and runner class must be preserved. Propose and justify a scheduler. For reproducibility, treat these as the supplied source facts for deficit round robin (DRR): it visits active flow queues round-robin, preserves FIFO within each flow queue, sends a whole head packet only when its complete known size fits the queue's deficit, and carries residual deficit across rounds only while that queue remains backlogged. When a queue empties, its deficit resets to zero. DRR neither provides global FIFO nor preempts an in-flight packet. These facts come from [the original DRR paper](https://dl.acm.org/doi/10.1145/217382.217453) and the [IETF account in RFC 7806](https://www.rfc-editor.org/rfc/rfc7806.html#section-2.2.4).

Expected outcome: Explicit invocation loads and applies analogize; it is not eligible for automatic activation.

## `explicit-restate`

Stimulus: Explicit invocation of restate: The gateway needs smarter retries. Fixed facts: transport is at-least-once and some downstream operations are not idempotent. Original success criteria: at most six total downstream attempts per client request, no multiplicative retries across hops, and unchanged external timeout and failure semantics.

Expected outcome: Explicit invocation loads and applies restate; it is not eligible for automatic activation.

## `explicit-generalize`

Stimulus: Explicit invocation of generalize: Reason about merging exactly two user accounts. The system already solved organization renames with stable aliases to a canonical ID. User merge must preserve foreign keys, audit history, authorization, idempotency, and rollback, and the shipped scope must remain the two-account operation.

Expected outcome: Explicit invocation loads and applies generalize; it is not eligible for automatic activation.

## `explicit-decompose`

Stimulus: Explicit invocation of decompose: Move billing from a monolith into a service without double charges, missing refunds, authorization regressions, or a flag-day cutover. The legacy database is shared and invoice IDs are externally visible. The route must generate observable evidence, preserve rollback, and recompose into one end-to-end authority transition.

Expected outcome: Explicit invocation loads and applies decompose; it is not eligible for automatic activation.

## `explicit-invert`

Stimulus: Explicit invocation of invert: Plan a zero-downtime database migration. The end state is one authoritative new schema with old clients retired, but the current state has mixed-version clients, dual reads are allowed, writes cannot be paused, and rollback must remain possible until reconciliation passes. Produce a migration plan.

Expected outcome: Explicit invocation loads and applies invert; it is not eligible for automatic activation.

## `router-selection`

Stimulus: Plan the extraction of billing from a monolith after three failed approaches. Splitting by endpoint separated charges from refunds, splitting by table left the shared ledger ambiguous, and splitting by deployable unit kept authorization entangled. The flow also spans invoice IDs and retries. A flag-day rewrite is prohibited; the migration must be observable, reversible, and end with one declared write authority. Find a credible first route and map it back to these constraints.

Expected outcome: The router selects one to three leaves, then loads every selected sibling before applying its method and records why the primary candidate won.

## `map-back`

Stimulus: Explicit invocation of solve: Recommend a production configuration migration. It must require zero changes to 200 deployed clients, preserve uninterrupted reads, and support rollback for 30 days. A one-client prototype works by changing that client to read a new endpoint. What should ship?

Expected outcome: The workflow must map back to the original problem, restore or resolve all constraints, test the success criteria, and reject the candidate rather than claim completion.
