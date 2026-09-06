# Worked examples

These compact software examples show the shared entry contract, a cheap
candidate, the selected lens's full method, and a map-back to the original
success criteria. The `P`/`P′`/`S′`/`S` framing is reused here as authored
collection shorthand; Shannon used that notation specifically for similar known
problems.

**Evidence convention:** the entry contracts and pre-transform observations below
are fictional supplied inputs for these examples. Method reasoning is illustrative;
the end-to-end tests, production replays, and measurements proposed below have not
been executed by this collection. They describe evidence a real task must gather.
Use the [shared workflow contract](workflow-contract.md) to keep definition status,
resolution status, effort, and the source of each claim separate. Each example uses
one full method attempt; a later full method consumes the same remaining budget.

## Simplify — multi-region cache invalidation

### Entry contract

**P:** Invalidate cached tenant records across three regions while preserving
per-tenant TTL overrides, soft deletes, and warm-up.

**Observable success criteria:** at p99.9, after an accepted write no region
serves the old value beyond the agreed five-second staleness budget; a region
whose freshness proof expires bypasses cached reads; deleted values do not
reappear; TTL overrides remain tenant-scoped; warm-up cannot replace a newer
value. Fixed facts are asynchronous regional replication, monotonic record
versions, and no synchronous global broadcast. Transport inspection confirms
that the event service provides per-tenant ordering and contiguous offsets.
The source database exposes an authoritative commit position on tenant outbox
rows, and the commit-ordered outbox publisher can emit tenant watermarks.
For this timing argument, the supplied database capability additionally attests a
source-clock coverage time `T`: all accepted commits through `T` are represented
by the watermark's commit position. A finite bound `epsilon` on the absolute
difference between consumer and source clocks is supplied. These are prerequisites,
not properties inferred from a contiguous stream. The fictional measurements show
p99.9 delivery lag under two seconds; delivery percentiles do not prove freshness.

### Cheap candidate

Strip to a deliberately trivial skeleton: one process, one tenant, one record,
hard deletes, no TTL, no warm-up. The writer and reader share a version counter,
so invalidation is just incrementing that counter.

### Full method

Restore constraints one at a time:

1. Multiple records: use `(tenant, key, version)` as the cache identity.
2. Multiple processes in one region: store the current version in a shared
   pointer; readers reject cached entries with an older version.
3. Multiple regions: record every accepted version and its authoritative source
   commit position in a transactional outbox, then publish it to an ordered
   per-tenant version-event stream. This is the **first
   constraint that reintroduces difficulty in this restoration order**, because correctness now depends
   on proving that a region has not silently missed an update. The same
   commit-ordered publisher emits a watermark only after draining all tenant
   outbox rows through source commit position `C`. Its attested coverage time `T`
   cannot advance past an unpublished accepted commit. Each region applies events
   to its version pointer and advances a contiguous stream offset before accepting
   that watermark. The conservative consumer-clock lease deadline is
   `T + 5 seconds - epsilon`, not the watermark's arrival time plus five seconds.
   A late or replayed watermark retains its original coverage time; an expired
   one cannot re-enable cached reads. A sequence gap or expired deadline disables
   cached reads. A publisher stall prevents coverage from advancing, but the region
   does not instantly observe an unpublished upstream commit: it relies on the
   bounded deadline. On bypass, use an authoritative read path with the required
   freshness, or reject the read if that path is unavailable. If attested coverage
   time or the clock-error bound is unavailable, this proof is unavailable too;
   retain that design gap rather than claim a five-second lease is justified.
4. Soft deletes: publish a versioned tombstone; warm-up and reads may not cross
   it.
5. Tenant TTL overrides: attach expiry to the tenant's versioned entry, without
   changing version comparison.
6. Warm-up: read the same pointer before filling and compare again before
   publishing, discarding a fill that lost a version race.

The active set at step 3 includes multiple records, multiple processes, and
asynchronous regions. The first failing restoration is evidence about that set,
not proof that the last-added constraint is the sole cause. Try another order or
a smaller interacting subset before making a stronger causal attribution.

For the adversarial timing trace, use `T = 0`, `epsilon = 0`, a later accepted
write at 0.1, delivery of the old watermark at 1.9, and then a publisher stall.
The deadline stays at 5.0; receipt must not extend it to 6.9. A consumer clock
that may lag source time by 0.25 seconds uses deadline 4.75. Unknown coverage or
clock bounds cannot support the proof. This is a conditional timing argument,
not evidence of a production percentile or correctness of a deployed cache.

### Map-back and verify

`S` combines versioned values and tombstones with the ordered per-tenant event
stream and freshness lease; it is not the single-process counter from the
skeleton. Proposed tests cover propagation percentiles, a deliberately dropped event
and offset gap, a publisher stall after commit but before event assignment,
delayed pre-write watermarks, expired replay, nonzero and unknown clock bounds,
watermark suppression and lease-expiry cache bypass, delete/recreate, tenant
isolation, and the warm-up race. The five-second p99.9 target remains an
operating SLO rather than proof that asynchronous delivery never exceeds it.

**Result:** definition CONFIRMED within the fictional input; resolution CANDIDATE.
The timing argument supports the stated conditional deadline; the proposed system
still needs evidence for propagation, deletion, isolation, and warm-up criteria.

## Analogize — fair CI-runner allocation

### Entry contract

**P:** Allocate heterogeneous CI runners fairly among teams with bursty demand.
Observable success means that continuously backlogged teams receive their
configured weighted share over the measurement window, jobs remain FIFO within
a team and compatible runner class, no running job is preempted, and starvation
is detected. Fixed facts are unknown job duration at enqueue time,
non-preemptive jobs, and several runners operating in parallel. Missing facts
are team weights, runner compatibility classes, maximum job duration, and the
cost estimate or charging rule.

The fairness measurement window and acceptable share deviation are unspecified
acceptance parameters, marked OPEN. The decision owner is unknown: identify who
can set the window and deviation, then ask for those values. Preserve these
questions through the method; a scheduler analogy cannot settle them.

**Pre-transform fact gathering:** configuration inspection establishes team
weights of `2:1:1`, two non-interchangeable runner classes, and a 60-minute hard
job timeout. Historical traces do not provide a reliable enqueue-time runtime
estimate, and the current dispatcher has no credit-charging rule. Those two
unknowns are frozen as analogy breaks: no weighted-fairness guarantee may be
claimed unless the adapted design defines and validates both.

### Cheap candidates

1. **Deficit round robin (DRR):** a credit-based scheduler for variable-sized
   work across active queues.
2. **Stride scheduling:** deterministic weighted selection using per-team
   virtual progress, but still dependent on a defensible job-cost estimate.
3. **Aging priority:** useful for starvation control, but weak as the primary
   weighted-share model.

DRR is selected because its per-queue credit state exposes the central design
question—how job cost is estimated and charged—rather than hiding it.

### Full method

Verify the source mechanics before porting them. Canonical DRR visits active
flow queues round-robin, preserves FIFO order inside each flow queue, and
transmits a whole head packet only when its complete size fits the queue's
deficit. Residual deficit carries across rounds while the queue stays
backlogged; when the queue empties, its deficit resets to zero. DRR provides
neither global FIFO nor preemption of an in-flight packet. See [Shreedhar and Varghese's original DRR
paper](https://dl.acm.org/doi/10.1145/217382.217453); [RFC 7806](https://www.rfc-editor.org/rfc/rfc7806.html#section-2.2.4)
provides a later IETF account of the byte-credit mechanics.

| DRR source | CI target | Port or break |
|---|---|---|
| Active flow queue | Team queue within a runner class | Port |
| Packet FIFO within a flow | Job FIFO within a team queue | Port |
| Output-link dequeue opportunity | A compatible runner becoming free | Break: several runners create concurrent opportunities |
| Packet size known before dequeue | Job cost | Break: runtime is unknown at dispatch |
| Quantum | Weighted credit increment | Port only after defining units and weights |
| Deficit counter | Per-team credit balance | Port with persisted, observable accounting and reset credit when the queue drains |
| Whole packet transmission | Whole non-preemptive job dispatch | Break: a long job occupies a runner for its full duration |

The analogy does not supply a fairness guarantee for CI. Adaptation decisions
are required: partition queues by runner compatibility; reserve a bounded cost
estimate at dispatch; reconcile credits against observed runner time on
completion; cap or isolate exceptionally long jobs; and define how simultaneous
runner availability serializes credit updates. Reset a team's unused credit
when its compatible queue drains so idle teams cannot hoard credit. If no
estimate and charging rule is defensible, use DRR only as a heuristic and say
so.

### Map-back and verify

`S` is an adapted dispatcher, not packet DRR renamed. Replay production traces
and measure weighted runner-time share, within-team FIFO, starvation, and
long-job occupancy for each runner class. Any guarantee must be proved from the
adapted charging and concurrency rules; it is not borrowed from the analogy.

**Result:** definition DRAFT; resolution CANDIDATE. The fairness window and
acceptable deviation remain OPEN with an unknown decision owner. The mapping
supports a conditional design, while charging, concurrency, fairness, FIFO,
and starvation claims await the specified validation.

## Restate — retries across service hops

### Entry contract

**P:** “The API gateway needs smarter retry logic.” Observable success is at
most six downstream attempts per client request, no unbounded multiplicative
retrying across hops, and unchanged externally visible timeout and failure
semantics. Fixed facts are an at-least-once transport and downstream services
that are not all idempotent. Traces show sequential calls and parallel fan-out
to as many as three children. A propagation probe confirms that request
metadata reaches every hop but is copied independently into fan-out branches,
so a shared scalar header would not conserve a global attempt budget.

### Cheap candidates and invariant ledger

| Restatement | What it reveals | Invariants preserved? |
|---|---|---|
| Actor: “Downstream services must be protected from duplicate work.” | Retry policy has effects beyond the gateway | Yes |
| Quantity: “Bound total work amplification per client request across all hops.” | Independent local retry counts multiply | Yes |
| State machine: “Every attempt consumes a token from one request-scoped budget.” | The budget must propagate and never reset | Yes |
| **Labeled relaxation:** “Ignore the external timeout while analyzing amplification.” | Separates attempt count from time allocation | No; exploration only, restore before shipping |

The quantity restatement is selected because traces can answer it directly and
it does not embed a preferred retry algorithm.

### Full method

Carry a request-scoped retry budget through each hop. A sequential caller
consumes one token for its downstream attempt and passes the unspent remainder.
Before parallel fan-out, the parent atomically partitions its remaining tokens
into disjoint child envelopes whose allocations, including each initial child
attempt, sum to no more than the parent's remainder. The partition is recorded
under the request ID, and every child envelope has a unique allocation ID, so
at-least-once redelivery reuses the same allocation instead of duplicating the
budget. Each branch may consume or subdivide only its own envelope; unused
tokens expire rather than being reused while descendants might still be active.
No downstream hop replenishes tokens, and an empty envelope preserves the
existing failure semantics. Every branch also inherits the original deadline
so fan-out cannot extend the external timeout. Non-idempotent operations remain
ineligible for automatic retry.

### Map-back and verify

`S` replaces “smarter per-hop logic” with a conserved, propagated work budget.
Proposed end-to-end tests must assert at most six attempts for sequential calls and for
three-way fan-out when every child retries concurrently; child allocations sum
to the parent's remaining budget; deadlines remain unchanged; ineligible
operations do not retry; repeated fan-out delivery reuses allocation IDs; and
nested propagation cannot mint tokens. The temporary timeout relaxation is
explicitly removed. The invariant ledger remains the acceptance checklist.

**Result:** definition CONFIRMED within the fictional input; resolution CANDIDATE.
The conservation argument is illustrative; no end-to-end retry, redelivery, or
deadline test is reported as executed.

## Generalize — account merge

### Entry contract

**P:** Merge exactly two user accounts without breaking foreign keys, audit
history, authorization, or rollback. Observable success is one canonical user,
all resources reachable through it, an immutable merge record, and a tested
rollback before destructive cleanup. A fixed fact is that this system already
uses stable canonical-ID resolution for a solved organization-rename workflow.
Missing facts are which user-owned tables bypass that resolver and whether any
authorization cache keys directly on the old ID.

**Pre-transform fact gathering:** a schema and call-site inventory finds three
user-owned tables that read direct IDs instead of the resolver. The
authorization cache also keys directly on user ID, but exposes an existing
dual-key eviction hook. These findings make direct-ID backfill and cache
invalidation fixed map-back work rather than assumptions hidden by the
generalization.

### Cheap candidates

1. **Shannon-derived, result-first broadening:** begin with the solved
   organization result—stable aliases resolve to a canonical ID—and ask whether
   the same principle covers user ownership and a larger class of aliases.
2. **Modern structure-exposing form:** parameterize “merge two” as “map a finite
   set of source IDs to one canonical ID.” The parameter exposes convergence,
   cycle prevention, idempotency, and rollback requirements hidden by a
   two-row migration script.

### Full method

Select result-first broadening as the primary route because the supplied
organization workflow provides an established mechanism to inspect. Keep the
parameterized sketch as a cross-check for convergence and rollback; it is not
a second full-method attempt.

Both candidates point to a user-scoped alias table with an acyclic canonical-ID
resolver. Insert the alias and immutable audit record transactionally, resolve
ownership at read and authorization boundaries, backfill direct-ID consumers,
and delay destructive cleanup until verification and the required rollback test pass.
The generalized model is a reasoning aid; it does not authorize a universal
entity framework.

### Map-back and verify

Instantiate the model for two user IDs only. Foreign-key, authorization,
audit-history, idempotent-retry, and rollback tests must pass for those users.
Ship the requested user-merge path, not unrequested general infrastructure.

**Result:** definition CONFIRMED within the fictional input; resolution CANDIDATE.
Both generalization forms happen to apply to this case. If either prerequisite
were absent, mark that form inapplicable and use the supported form without
inventing a precedent or parameter axis. Required merge tests remain proposed.

## Decompose — extracting monolith billing

### Entry contract

**P:** Move billing from a monolith to a service without double charges,
missing refunds, broken authorization, or an unreviewable cutover. Success is
behavioral parity on recorded traffic, reconciled ledger totals, a reversible
cohort rollout, and one declared authority after cutover. Fixed facts are a
shared legacy database and externally visible invoice IDs. Missing facts are
all write paths and the observed mismatch rate of a shadow implementation.

**Pre-transform fact gathering:** static call-site inventory plus production
tracing identifies seven billing write paths, including an asynchronous refund
worker missed by the module boundary. A 24-hour shadow-compute sample records a
0.6% result mismatch, concentrated in tax-rounding cases. The decomposition
must therefore expose the refund path and produce categorized parity evidence;
it cannot treat module coverage as behavioral coverage.

### Cheap candidate seams

1. **Authority and reversibility:** shadow computation, shadow persistence,
   cohort reads, then authority cutover.
2. **Source-code module boundaries:** rejected because nominal modules share
   transactions and do not isolate billing behavior.
3. **HTTP endpoints:** rejected because refunds, retries, and ledger updates
   cross endpoint boundaries.

The authority seam is selected because every stage is observable and
reversible and produces evidence needed by the next stage.

### Full method

Order work by dependency and information yield, not apparent ease:

1. **Which inputs and rules determine a charge?** Shadow-compute from recorded
   requests; output a categorized result diff. This comes first because it
   cheaply discovers hidden rules.
2. **Can the service persist the same ledger without side effects?** Write
   shadows to an isolated ledger; output an invariant and total reconciliation.
3. **Do reads preserve invoice identity and authorization?** Route a reversible
   internal cohort; output SLO, authorization, and consistency comparisons.
4. **Can the new service become sole authority?** Cut over a flagged cohort,
   exercise rollback, then expand; output duplicate/missing-charge counts and
   a signed authority transition record.

### Recomposition and map-back

Recompose the stages as one end-to-end charge/refund/retry trace. Check the
cross-cutting constraints—idempotency, invoice IDs, authorization, ledger
totals, audit history, and rollback—across every boundary. `S` exists only when
the recomposed path meets the original criteria; individually green stages do
not prove the migration.

**Result:** definition CONFIRMED within the fictional input; resolution PARTIAL.
The seam and questions are useful progress, not a verified migration. If the
rounding subproblem needs another full method, checkpoint its original parity
obligations, keep the same contract and remaining effort, then apply that method
to the bounded question. Its answer still must recompose into the whole migration.

## Invert — EU tail latency

### Entry contract

**P:** Explain why p99 latency is three times p50 in EU during the observed
window while US does not show the same symptom. Success is a reproducible,
isolated cause, a forward-tested fix, and no regression in either region.
Fixed facts are only the measured regional contrast and percentile gap; US's
absence of the symptom does **not** prove the behavior is load-insensitive.
Missing facts include comparable traces, traffic mix, arrival and service-time
variability, utilization, retry rate, pool saturation, and endpoint routing.

**Pre-transform fact gathering:** matched trace windows use the same
instrumentation version and retain the EU percentile gap after stratifying by
endpoint and request-size band. The available sample is not sufficient to
isolate utilization, arrival or service-time variability, retries, pool
saturation, or routing. Those remain explicit unresolved facts, so inversion
may produce hypotheses and forward tests only—not a causal conclusion.

### Cheap candidate: branching backward graph

Assume only the observed effect, “EU tail spans are longer,” and preserve
alternative predecessors:

- **Queueing branch:** reducing an EU connection-pool limit (action) can raise
  utilization and waiting time (expected effect). Bursty arrivals or variable
  service times (mechanisms) can also widen the tail; queueing depends on
  variability as well as utilization.
- **Retry branch:** an EU dependency returning more retryable failures
  (mechanism) adds attempts to some traces (expected effect).
- **Route branch:** selecting a more distant EU endpoint (action) adds network
  time to affected spans (expected effect).
- **Measurement branch:** different EU sampling or clock behavior (mechanism)
  changes the reported percentile without changing request latency (expected
  effect).

An EU-specific difference is necessary to explain a valid regional contrast,
but is not sufficient to identify its cause. None of the listed predecessors
is sufficient on current evidence. The percentile observation is
non-invertible by itself: many causal graphs produce it, and every reverse edge
has unknown sufficiency.

### Full method: turn backward routes into forward tests

1. Reproduce the percentile gap with matched traffic windows and verify the
   instrumentation.
2. Compare trace-span distributions, not only aggregate percentiles, to select
   among queue, retry, route, and measurement branches.
3. For the selected branch, change one mechanism in a controlled replay: pool
   limit, arrival/service variability, retry behavior, or endpoint route.
4. Predict the affected span and percentile before the change, run the test,
   and reject the branch if the expected effect does not occur.
5. Replay the candidate fix forward from the actual current state in both
   regions.

### Map-back and debugging boundary

Inversion produces hypotheses and forward experiments, not an asserted cause
or a claim that backward search converges. The investigation returns to
evidence-led systematic debugging for observation, reproduction, isolation,
and verification; inversion does not replace that process. `S` is accepted only
after the isolated mechanism and fix reproduce against the original regional
latency criteria.

**Result:** definition CONFIRMED within the fictional input; resolution PARTIAL.
The hypothesis set and proposed discriminating experiments do not establish a
cause or tested fix. Return this bounded result to diagnosis with its unanswered
questions; do not continue generating branches without credible information gain.
