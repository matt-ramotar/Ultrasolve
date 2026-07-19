# Worked examples

A transformed problem is not yet a solution. Each example starts with the
original problem and observable success criteria, tests a cheap lens-specific
candidate, runs the selected lens's full method, and maps the result back to the
original problem.

These examples use `P` for the original problem and `S` for the mapped-back
candidate. When a transformed problem and result need separate labels, they use
`P′` and `S′` as authored shorthand. Shannon used that notation specifically
for similar known problems.

## Simplify: multi-region cache invalidation

### Entry contract

**P:** Invalidate cached tenant records across three regions while preserving
per-tenant TTL overrides, soft deletes, and warm-up.

**Observable success criteria:**

- Across accepted writes, every region's p99.9 staleness stays within the agreed
  five-second budget.
- A region whose freshness proof expires bypasses cached reads.
- Deleted values do not reappear.
- TTL overrides remain tenant-scoped.
- Warm-up cannot replace a newer value.

**Fixed facts:** Regional replication is asynchronous. Record versions are
monotonic. A synchronous global broadcast is unavailable.

**Pre-transform fact gathering:** Transport inspection confirms that the event
service provides per-tenant ordering and contiguous offsets. The source database
exposes an authoritative commit position on tenant outbox rows. Its
commit-ordered outbox publisher can emit tenant watermarks. Measured p99.9
delivery lag is under two seconds.

### Cheap candidate

Start with a deliberately trivial skeleton. One process handles one tenant and
one record. It uses hard deletes, has no TTL, and performs no warm-up. The writer
and reader share a version counter, so invalidation increments that counter.

### Full method

Restore constraints one at a time:

1. **Multiple records.** Use `(tenant, key, version)` as the cache identity.
2. **Multiple processes in one region.** Store the current version in a shared
   pointer. Readers reject cached entries with an older version.
3. **Multiple regions.** Record every accepted version and its authoritative
   source commit position in a transactional outbox. Publish those records to an
   ordered per-tenant version-event stream.

   This is the first restored constraint that makes the problem hard. A region
   must prove that it has not silently missed an update.

   The commit-ordered publisher emits a watermark only after draining every
   tenant outbox row through source commit position `C`. The watermark proves
   that all accepted commits through `C` have been published. The publisher may
   not renew it while an earlier accepted commit remains unpublished.

   Each region applies events to its version pointer and advances a contiguous
   stream offset. It renews a five-second freshness lease only after consuming
   the commit-aware watermark. The lease is the region's permission to serve
   cached reads as fresh.

   A publisher stall, sequence gap, or expired lease disables cached reads until
   the consumer catches up. Reads then use a source-of-truth path independent of
   cache freshness. If that path is unavailable, the request is rejected. The
   measured delivery percentile remains an operating SLO.
4. **Soft deletes.** Publish a versioned tombstone. Warm-up and reads may not
   cross it.
5. **Tenant TTL overrides.** Attach expiry to the tenant's versioned entry
   without changing version comparison.
6. **Warm-up.** Read the same pointer before filling, compare it again before
   publishing, and discard a fill that lost a version race.

### Map-back and verify

`S` combines versioned values and tombstones with the ordered per-tenant event
stream and freshness lease. The single-process counter remains only the
skeleton.

Tests cover propagation percentiles, a deliberately dropped event and offset
gap, a publisher stall after commit but before event assignment, watermark
suppression, lease-expiry cache bypass, delete and recreate, tenant isolation,
and the warm-up race. Treat the five-second p99.9 target as an operating SLO.
Measured asynchronous delivery does not prove that every event arrives within
five seconds.

## Analogize: fair CI-runner allocation

### Entry contract

**P:** Allocate heterogeneous CI runners fairly among teams with bursty demand.

**Observable success criteria:**

- Continuously backlogged teams receive their configured weighted share over
  the measurement window.
- Jobs remain FIFO within a team and compatible runner class.
- Running jobs are never preempted.
- Starvation is detected.

**Fixed facts:** Job duration is unknown at enqueue time. Jobs are
non-preemptive. Several runners operate in parallel.

**Missing facts:** Team weights, runner compatibility classes, maximum job
duration, and the cost estimate or charging rule.

**Pre-transform fact gathering:** Configuration inspection establishes team
weights of `2:1:1`, two non-interchangeable runner classes, and a 60-minute hard
job timeout. Historical traces do not provide a reliable enqueue-time runtime
estimate. The current dispatcher has no credit-charging rule. Those two unknowns
remain analogy breaks. Any weighted-fairness guarantee depends on defining and
validating both.

### Cheap candidates

1. **Deficit round robin (DRR).** A credit-based scheduler for variable-sized
   work across active queues.
2. **Stride scheduling.** Deterministic weighted selection using per-team
   virtual progress. It still depends on a defensible job-cost estimate.
3. **Aging priority.** Useful for starvation control, but weak as the primary
   weighted-share model.

Choose DRR. Its per-queue credit state forces the central design question into
the open. How should job cost be estimated and charged?

### Full method

Verify the source mechanics before porting them. Canonical DRR visits active
flow queues round-robin and preserves FIFO order within each queue. It transmits
a whole head packet only when the packet's complete size fits the queue's
deficit. Residual deficit carries across rounds while the queue stays
backlogged. When the queue empties, its deficit resets to zero. DRR provides
neither global FIFO nor preemption of an in-flight packet.

[Shreedhar and Varghese's original DRR paper](https://dl.acm.org/doi/10.1145/217382.217453)
defines these mechanics. [RFC 7806](https://www.rfc-editor.org/rfc/rfc7806.html#section-2.2.4)
provides a later IETF account of the byte-credit model.

| DRR source | CI target | Evidence | Mismatch |
|---|---|---|---|
| Active flow queue | Team queue within a runner class | Configured teams and two compatibility classes define the target queues | None at the queue-identity level |
| Packet FIFO within a flow | Job FIFO within a team queue | FIFO is an original success criterion | None within one compatible team queue |
| Output-link dequeue opportunity | A compatible runner becoming free | Several runners operate in parallel | One serial dequeue opportunity becomes concurrent dispatch events |
| Packet size known before dequeue | Job cost | Historical traces provide no reliable enqueue-time estimate | Runtime is unknown at dispatch |
| Quantum | Weighted credit increment | Team weights are configured as `2:1:1` | Credit units remain undefined until the charging rule is defined |
| Deficit counter | Per-team credit balance | DRR carries credit only while a queue stays backlogged | CI needs persisted, observable accounting and a reset when the compatible queue drains |
| Whole packet transmission | Whole non-preemptive job dispatch | Jobs are non-preemptive and have a 60-minute hard timeout | A long job occupies a runner for its full duration |

The mapping exposes decisions that DRR cannot make for CI:

- Partition queues by runner compatibility.
- Reserve a bounded cost estimate at dispatch.
- Reconcile credits against observed runner time on completion.
- Cap or isolate exceptionally long jobs.
- Serialize credit updates when several runners become available at once.
- Reset unused team credit when the compatible queue drains so idle teams cannot
  hoard it.

Without a defensible estimate and charging rule, DRR remains a scheduling
heuristic. It cannot support a weighted-fairness guarantee.

### Map-back and verify

`S` is an adapted dispatcher with explicit accounting and concurrency rules.
Replay production traces for each runner class. Measure weighted runner-time
share, within-team FIFO, starvation, and long-job occupancy. Prove any guarantee
from the adapted charging and concurrency rules rather than borrowing it from
packet DRR.

## Restate: retries across service hops

### Entry contract

**P:** “The API gateway needs smarter retry logic.”

**Observable success criteria:** Each client request causes at most six
downstream attempts. Retry counts cannot multiply without bound across hops.
Externally visible timeout and failure semantics remain unchanged.

**Fixed facts:** The transport provides at-least-once delivery. Some downstream
services are not idempotent.

**Pre-transform fact gathering:** Traces show sequential calls and parallel
fan-out to as many as three children. A propagation probe confirms that request
metadata reaches every hop. Fan-out branches receive independent copies, so one
shared scalar header cannot conserve a global attempt budget.

### Cheap candidates and invariant ledger

| Restatement | What it reveals | Invariants preserved? |
|---|---|---|
| Actor: “Downstream services must be protected from duplicate work.” | Retry policy affects services beyond the gateway | Yes |
| Quantity: “Bound total work amplification per client request across all hops.” | Independent local retry counts multiply | Yes |
| State machine: “Every attempt consumes a token from one request-scoped budget.” | The budget must propagate and never reset | Yes |
| **Labeled relaxation:** “Ignore the external timeout while analyzing amplification.” | Separates attempt count from time allocation | No. Exploration only. Restore before shipping. |

Use the quantity restatement. Traces can measure total work directly, and the
wording does not embed a preferred retry algorithm.

### Full method

Carry one request-scoped retry budget through every hop:

1. A sequential caller consumes one token for its downstream attempt and passes
   the unspent remainder.
2. Before parallel fan-out, the parent atomically partitions its remaining
   tokens into disjoint child envelopes. The allocations include each initial
   child attempt and sum to no more than the parent's remainder.
3. Record the partition under the request ID. Give each child envelope a unique
   allocation ID. At-least-once redelivery reuses that allocation instead of
   duplicating its budget.
4. A branch may consume or subdivide only its own envelope. Unused tokens expire
   rather than returning to a budget while descendants might still be active.
   No downstream hop replenishes tokens.
5. An empty envelope preserves the existing failure semantics. Every branch
   inherits the original deadline, so fan-out cannot extend the external
   timeout. Non-idempotent operations remain ineligible for automatic retry.

### Map-back and verify

`S` replaces “smarter per-hop logic” with a conserved work budget. End-to-end
tests establish the original contract:

- Sequential calls and three-way fan-out never exceed six attempts, even when
  every child retries concurrently.
- Child allocations sum to the parent's remaining budget.
- Deadlines remain unchanged.
- Ineligible operations do not retry.
- Repeated fan-out delivery reuses allocation IDs.
- Nested propagation cannot mint tokens.

Remove the temporary timeout relaxation before shipping. The invariant ledger
remains the acceptance checklist.

## Generalize: account merge

### Entry contract

**P:** Merge exactly two user accounts without breaking foreign keys, audit
history, authorization, or rollback.

**Observable success criteria:** One user is canonical. All resources are
reachable through that user. The system records an immutable merge. Rollback is
tested before any destructive cleanup.

**Fixed facts:** The system already uses stable canonical-ID resolution for a
solved organization-rename workflow.

**Missing facts:** Which user-owned tables bypass that resolver and whether any
authorization cache keys directly on the old ID.

**Pre-transform fact gathering:** A schema and call-site inventory finds three
user-owned tables that read direct IDs instead of the resolver. The authorization
cache also keys directly on user ID, but it exposes an existing dual-key eviction
hook. Direct-ID backfill and cache invalidation are therefore fixed map-back
work.

### Cheap candidates

1. **Shannon-derived, result-first broadening.** Start from the solved
   organization result. Stable aliases resolve to a canonical ID. Ask whether
   the same principle covers user ownership and a larger class of aliases.
2. **Modern structure-exposing parameterization.** Restate “merge two” as “map a
   finite set of source IDs to one canonical ID.” The parameter exposes
   convergence, cycle prevention, idempotency, and rollback requirements hidden
   by a two-row migration script.

Both forms expose alias indirection, but they contribute different evidence.
The solved organization workflow shows that canonical-ID resolution already
works in this system. Parameterization exposes the invariants hidden by the
two-account special case.

Use the modern parameterization as the primary route because those hidden
invariants determine whether the merge is safe. Keep the organization workflow
as a result-first cross-check. Selecting the broader reasoning model does not
expand the shipped scope.

### Full method

Parameterize the problem as a finite set of source user IDs that resolve to one
canonical user ID. The mechanism is a user-scoped alias table with an acyclic
canonical-ID resolver. The existing organization resolver supplies a known
implementation pattern and a cross-check on the result.

Insert the alias and immutable audit record transactionally. Resolve ownership
at read and authorization boundaries. Backfill the three direct-ID consumers
and use the existing dual-key hook to invalidate the authorization cache. Delay
destructive cleanup until verification passes and the rollback window closes.

The generalized model is reasoning machinery. Shipped scope remains the
requested account merge rather than a universal entity framework.

### Map-back and verify

Instantiate the model for exactly two user IDs. Foreign-key, authorization,
audit-history, idempotent-retry, and rollback tests must pass for those users.
Ship the requested user-merge path and no unrequested general infrastructure.

## Decompose: extracting monolith billing

### Entry contract

**P:** Move billing from a monolith to a service without double charges, missing
refunds, broken authorization, or an unreviewable cutover.

**Observable success criteria:** The new service matches the monolith on
recorded traffic. Ledger totals reconcile. Cohort rollout is reversible. One
authority is declared after cutover.

**Fixed facts:** The legacy database is shared. Invoice IDs are externally
visible.

**Missing facts:** Every billing write path and the observed mismatch rate of a
shadow implementation.

**Pre-transform fact gathering:** Static call-site inventory and production
tracing identify seven billing write paths. One is an asynchronous refund worker
that the module boundary missed. A 24-hour shadow-compute sample records a 0.6%
result mismatch concentrated in tax-rounding cases. The decomposition must expose
the refund path and produce categorized parity evidence. Module coverage alone
cannot establish behavioral coverage.

### Cheap candidate seams

1. **Authority and reversibility.** Shadow computation, shadow persistence,
   cohort reads, then authority cutover.
2. **Source-code module boundaries.** Reject this seam because nominal modules
   share transactions and do not isolate billing behavior.
3. **HTTP endpoints.** Reject this seam because refunds, retries, and ledger
   updates cross endpoint boundaries.

Use authority and reversibility as the seam. Every stage is observable and
reversible. Each stage also produces the evidence needed to enter the next one.

### Full method

Order work by dependency and information yield. Apparent ease does not set the
order. Information yield is the amount of uncertainty a step removes for the
work that follows.

1. **Which inputs and rules determine a charge?** Shadow-compute from recorded
   requests and produce a categorized result diff. This comes first because it
   cheaply discovers hidden rules.
2. **Can the service persist the same ledger without side effects?** Write
   shadows to an isolated ledger. Reconcile its invariants and totals.
3. **Do reads preserve invoice identity and authorization?** Route a reversible
   internal cohort. Produce SLO, authorization, and consistency comparisons.
4. **Can the new service become sole authority?** Cut over a flagged cohort,
   exercise rollback, and then expand. Produce duplicate and missing-charge
   counts plus a signed authority-transition record.

### Recomposition and map-back

Recompose the stages as one end-to-end charge, refund, and retry trace. Check
idempotency, invoice IDs, authorization, ledger totals, audit history, and
rollback across every boundary. `S` exists only when the recomposed path meets
the original criteria. Green stages in isolation do not prove the migration.

## Invert: EU tail latency

### Entry contract

**P:** Explain why p99 latency is three times p50 in EU during the observed
window while US does not show the same symptom.

**Observable success criteria:** The isolated cause reproduces. A forward test
produces the predicted improvement in the affected span and EU p99. Neither
region regresses.

**Fixed facts:** The measured regional contrast and percentile gap are the only
established facts. The absence of the symptom in US does not establish that the
behavior is load-insensitive.

**Missing facts:** Comparable traces, traffic mix, arrival and service-time
variability, utilization, retry rate, pool saturation, and endpoint routing.

**Pre-transform fact gathering:** Matched trace windows use the same
instrumentation version. The EU percentile gap remains after stratifying by
endpoint and request-size band. The sample cannot isolate utilization, arrival
or service-time variability, retries, pool saturation, or routing. Those facts
remain unresolved. Inversion can produce hypotheses and forward tests, but the
current evidence cannot support a causal conclusion.

### Cheap candidate: branching backward graph

Start from the observed effect, “EU tail spans are longer,” and preserve four
alternative predecessor branches:

- **Queueing branch.** Reducing an EU connection-pool limit is an action that can
  raise utilization and waiting time. Bursty arrivals or variable service times
  are separate mechanisms that can also widen the tail. Queueing depends on
  variability as well as utilization.
- **Retry branch.** An EU dependency returning more retryable failures is a
  mechanism that adds attempts to some traces.
- **Route branch.** Selecting a more distant EU endpoint is an action that adds
  network time to the affected spans.
- **Measurement branch.** Different EU sampling or clock behavior is a
  mechanism that changes the reported percentile without changing request
  latency.

A valid regional contrast requires an EU-specific difference. That condition is
necessary, but it is not sufficient to identify the cause. None of the listed
predecessors is sufficient on current evidence. The percentile observation is
non-invertible by itself because many causal graphs produce it. Every reverse
edge still has unknown sufficiency.

### Full method: turn backward routes into forward tests

1. Reproduce the percentile gap with matched traffic windows and verify the
   instrumentation.
2. Compare trace-span distributions rather than aggregate percentiles alone.
   Use the comparison to select among queue, retry, route, and measurement
   branches.
3. Vary one candidate causal variable for the selected branch in a controlled
   replay. Choose the pool limit, arrival or service variability, retry
   behavior, or endpoint route.
4. Predict the affected span and percentile before making the change. Run the
   test and reject the branch if its expected effect does not occur.
5. Replay the candidate fix forward from the actual current state in both
   regions.

### Map-back and debugging boundary

Inversion produces hypotheses and forward experiments. It does not establish a
cause or guarantee that backward search converges. Return to evidence-led
systematic debugging for observation, reproduction, isolation, and
verification. Inversion supports that process but does not replace it. First
reproduce the isolated mechanism. Then accept `S` only if the fix passes the
original regional latency criteria.
