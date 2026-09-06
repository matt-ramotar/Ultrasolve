# Worked Example: Queue Incidents and an Authorized Migration Plan

This is an expanded teaching trace of interacting uncertainties, not the
required format for every definition. All supplied input below is fictional.
Reasoning is illustrative; proposed checks are not executed results. The
[shared workflow contract](../../solve/references/workflow-contract.md)
governs authority, inherited uncertainty, results, and effort.

## 1. Request and supplied context

> "Leadership approved Kafka for our queue incidents; migration plan by tomorrow."

The following is the complete fictional source input for the main trace:

> - Fourteen incidents were recorded in two classes: lost-job incidents and
>   backlog stalls. Class counts, incident details, and the reporting interval
>   are omitted.
> - Budget approval occurred. Leadership's Kafka choice is binding for this
>   assignment; the team's delegated responsibility is delivery planning.
> - The approved request says Kafka is meant to provide durable delivery under
>   peak. The handed-down operational metric is fewer queue-incident pages.
> - The current on-call policy defines the paging window as 15 minutes.
> - The accountable sponsor is Priya Shah, VP Platform, reachable today.
> - Prepare the migration plan and inspect available records by tomorrow.
>   Production changes are outside this request.

The requester's identity, what changed in the incident pattern, detailed
system architecture, and verification horizon are not supplied. Priya's
identity and reachability are supplied; no additional owner is invented.

## 2. Compact first response

The following illustrates a first response of roughly 250 words. The later
sections expose the reasoning for teaching purposes.

> Kafka is a binding choice for this assignment. I’ll prepare the migration
> plan by tomorrow and keep its claimed benefit conditional on the evidence.
> Drafting the plan does not authorize production changes.
>
> **Problem Q-1:** Fourteen reported incidents span lost jobs and backlog
> stalls. We lack class counts, job reconciliation, and recovery times, so we
> cannot yet establish actual loss or failure against an accepted recovery
> criterion. These two outcomes can move independently and may share causes.
>
> **Provisional criteria:** C1 is zero actual lost accepted jobs; C2 is recovery
> of every stall within a candidate 15 minutes. Zero loss is proposed. The
> 15-minute value comes from paging policy, but its acceptance role is OPEN.
> The verification window and representative peak conditions are unspecified.
>
> The plan can already cover the evidence inventory, current-to-target
> compatibility questions, preservation of accepted jobs, and conditional
> validation and rollback steps. Dates beyond tomorrow and system-specific
> procedures remain uncommitted until supported. I’ll inspect accessible
> records to separate observations from proposed checks, preserve both
> criteria, and carry each unresolved parameter with its owner and question.
>
> Two questions for Priya: Is zero actual lost accepted jobs the intended
> loss criterion? What observation duration, start condition, and workload
> coverage should establish acceptance?
>
> **Definition: DRAFT; resolution: PARTIAL.** The authorized plan is underway;
> effectiveness and acceptance remain unresolved. No full solving method has
> been attempted. The next step is to prepare the supported plan while
> gathering the available incident and acceptance evidence.

These are two material questions, not the entire unresolved-item inventory.
No silence or answer to one parameter settles another.

## 3. Ledger and decision authority

Split compound statements so an approval and an effectiveness claim cannot
be mistaken for the same fact.

| Received claim | Treatment | Consequence |
|---|---|---|
| Leadership's Kafka choice is binding for this assignment | Constraint, supplied explicitly | Retain Kafka in planning scope; changing technology is outside the delegated decision. |
| A migration plan is requested by tomorrow | Authorized work and response deadline | Deliver supported planning content, with conditional commitments where necessary. |
| Kafka is meant to provide durable delivery under peak | Supplied stake; effectiveness is a hypothesis | Preserve the intended function without claiming the technology will achieve it. |
| Fourteen incidents were recorded in two classes | Observation | Preserve the aggregate count; class counts, outcomes, and reporting interval remain missing. |
| Budget approval occurred | Observation about authority | It supplies neither an amount nor proof of effectiveness. |
| Fewer queue-incident pages | Supplied operational metric | Distinguish page volume from actual job loss and recovery. |
| Current paging policy is 15 minutes | Observation | The value is supplied; using it as an acceptance threshold remains OPEN. |
| Priya is the sponsor and reachable today | Observation about ownership | Address stakeholder decisions to Priya without inventing her answers. |
| Production changes are outside the request | Non-goal and action boundary | A draft plan permits no migration execution. |

The desired function is recoverable. Its completeness is still uncertain,
but that uncertainty does not revoke the binding choice or requested plan.

## 4. Goal material and individual acceptance provenance

The useful goal regress is pages → operational impact → loss and recovery.
The last step is illustrative reasoning, not a received business mandate.
Stop at the actionable decision context. If loss and recovery criteria had
already been agreed, an unknown broader business rationale would not require
another definition interview.

| ID | Item and value | Provenance and current mark | Exact unresolved question and owner |
|---|---|---|---|
| U1 | Durable delivery under peak is the stated function | CONFIRMED as supplied; completeness OPEN | Priya: "Is durable delivery under peak the complete function this assignment must serve?" |
| U2 | C1 loss threshold: zero actual lost accepted jobs | Proposed from the intended durable-delivery outcome; OPEN, not derived as an accepted threshold | Priya: "Is zero actual lost accepted jobs the intended loss criterion?" |
| U3 | C2 recovery threshold: `T = 15 minutes` for every stall | Numeric value supplied by policy; acceptance role and every-stall scope OPEN | Priya: "Is recovery of every backlog stall within the 15-minute paging window the acceptance criterion?" |
| U4 | Acceptance observation horizon `W` | No duration, start condition, or coverage rule supplied; OPEN | Priya: "What observation duration, start condition, and workload coverage should establish acceptance?" |
| U5 | Representative peak profile `L` | Durable delivery under peak is supplied; a measurable workload profile is missing and OPEN | Priya: "Which measured peak conditions must the acceptance check cover?" Accessible workload records can inform the answer. |

The historical reporting interval is a separate missing domain fact: inspect
the incident record for its start and end dates. It cannot supply the future
acceptance horizon without an explicit justification and acceptance source.
The person who maintains those records is unknown; identify that owner from
accessible records if direct access is unavailable.

No quarter-long window is supplied or derived. A quarter could be proposed,
but would remain unresolved until supported. Answers confirming the
function, zero-loss goal, or 15-minute threshold cannot confirm `W` or `L`.
Likewise, confirming `W` does not settle the threshold. Each parameter keeps
its own provenance even when a stakeholder answers several at once.

## 5. Shared problem contract Q-1

**P:** Fourteen incidents were recorded across lost-job incidents and backlog
stalls, with no reporting interval or class counts supplied. Classification
alone does not establish actual lost accepted jobs or recovery times. The
team needs a supported account of both outcomes and their acceptance
conditions while planning the authorized migration. Current values, causes,
and the acceptance observation horizon remain unknown.

| Criterion ID | Provisional outcome | Current evidence | Required validation and limits |
|---|---|---|---|
| C1 | Zero actual lost accepted jobs during accepted horizon `W` under profile `L`; U2, U4, U5 OPEN | Aggregate incident count only; no reconciled job outcomes | Reconcile every accepted job in scope to a documented outcome. Customer reports are a proxy; zero reports cannot prove zero actual loss. Any empirical claim is limited to its observed window and workload. |
| C2 | Every backlog stall recovers within candidate `T = 15 minutes` during `W` under `L`; U3, U4, U5 OPEN | Policy value supplied; no stall counts or recovery measurements | Measure stall starts and recovery under the agreed workload and window. A planned test or policy threshold is not a measured result. |

**Fixed facts:** preserve the supplied block in section 1, including the
aggregate count, policy, binding choice, sponsor, and authorized deadline.
Actual-loss verification requires job reconciliation; report completeness
must be established before using customer reports as a reliable proxy.

**Constraints:** Kafka is binding for delivery planning. Produce the plan by
tomorrow using available evidence and clearly marked assumptions. Preserve
both outcome criteria in any shared intervention; success on one cannot
compensate for failure or missing evidence on the other.

**Non-goals:** no production changes, unilateral technology revision, or
redesign of systems not implicated by evidence. Do not collapse distinct
symptoms into one established cause. These boundaries travel as constraints.

**Authorized work:** draft the Kafka migration plan and inspect available
records. Supported planning content may proceed while acceptance is OPEN.
A recommendation to change scope requires the decision owner's action; it
does not change scope by itself.

**Unresolved items:** carry U1–U5 verbatim, with Priya as owner, together with
these missing domain facts: class counts and historical interval; accepted-job
outcomes and reporting completeness; stall starts and recovery; deployment
and configuration history; arrival rate, queue depth, and consumer capacity;
current durability, acknowledgement, retry, and recovery settings; architecture
and applicable rollback limits. Gather accessible facts before asking others.
A missing fact can block a specific procedure or causal claim without blocking
the whole conditional plan.

**Definition status:** DRAFT while the acceptance items above remain unresolved.
**Effort remaining:** apply the shared effort rule; no full-method attempts
have been consumed in this definition trace. Preserve that record on handoff.

The provisional conditions show no supplied contradiction, but available
facts establish neither that they are satisfied nor that Kafka will satisfy
them. The deadline cannot resolve either uncertainty.

## 6. Problem split and overlapping hypotheses

C1 and C2 can move independently: a system may lose accepted jobs without a
stall, or stall without losing jobs. Keep separate evidence for each. A common
cause remains possible, as does an interaction within one symptom class.

The following are proposed discriminating checks, not results. The two
columns do not require one winning explanation or an exhaustive experiment
for every row. No unsupported likelihood is assigned.

| Hypothesis | Proposed C1 evidence | Proposed C2 evidence |
|---|---|---|
| Queue technology limit | Reconcile losses under representative load after documenting durability settings and deployment state; assess any demonstrated mechanism. | Measure recovery under the measured workload and documented capacity and deployment state. |
| Deployment mechanism | Compare reconciled losses around rollout actions at comparable loads. | Compare recovery around rollout actions at comparable loads. |
| Workload growth | Check whether actual loss changes with arrival rate while deployment and configuration are held stable. | Check whether recovery changes with arrival rate while deployment and configuration are held stable. |
| Joint deployment-plus-peak mechanism | Check whether losses occur under the combined condition when neither individual condition reproduces them. | Check whether a rollout during peak load reproduces the stall while rollout at ordinary load and peak without rollout do not. Investigate the interaction before assigning a sole cause. |
| Isolated configuration error | Check whether a specific correction removes reconciled loss under comparable conditions. | Check whether the correction restores recovery under comparable conditions. |
| Degradation without criterion failure | Check for zero actual loss alongside increased retries or page volume; acceptance still depends on U2, U4, U5. | Check for degraded recovery or headroom within candidate `T`; acceptance still depends on U3, U4, U5. |
| Metric artifact | Compare the classifier and reports with independently reconciled jobs. | Compare stall labels with traces showing actual progress and recovery. |
| No continuing problem | Observe reconciled outcomes over an explicitly supported `W` and `L`; a quiet fragment alone is insufficient. | Observe recovery over the same supported window and workload; missing measurements cannot establish dissolution. |

Evidence can support overlapping rows and different mechanisms for C1 and
C2. Insufficient evidence remains an explicit disposition even if every
proposed check cannot be finished by tomorrow.

## 7. Candidate register under the actual decision scope

For the main trace, the technology decision is binding. Assess ways to plan
and validate Kafka within that boundary. Specific feasibility depends on the
missing architecture and recovery facts.

| Planning candidate | Criterion obligations | Present limitation |
|---|---|---|
| Staged migration with a validation checkpoint before each expansion | Retain C1 reconciliation and C2 recovery evidence at each relevant step and for final acceptance | Stage boundaries, duplication behavior, rollback feasibility, `W`, and `L` are unresolved; this is an option, not an established design. |
| Single cutover after a separate rehearsal | Demonstrate both criteria under supported rehearsal conditions and define acceptance after cutover | Outage tolerance, rollback limits, rehearsal fidelity, `W`, and `L` are unresolved. |
| Smallest immediate step: finish the plan and inspect current records | Advances the authorized deliverable and evidence without changing production | This is useful planning progress, not evidence that either incident class is resolved. |

If supplied context instead says Kafka is still open, compare Kafka, current
broker tuning, a managed queue, and do-nothing against C1 and C2. Preserve the
requested draft plan as an option-specific artifact if it is still requested.
Do-nothing needs evidence that the accepted criteria already hold; missing
evidence is insufficient. An option must preserve both criteria and applicable
constraints; it need not prove the current technology was the sole cause to
become a credible candidate. No option is eligible on branding alone.

## 8. Inconclusive deadline continuation

For this section only, add the following fictional supplied report:

> "By tomorrow, the team reports that it reproduced a backlog stall exceeding
> 15 minutes only during a deployment at peak load. Deployment at ordinary
> load and peak load without deployment did not reproduce that stall in the
> checks reported. Logs are insufficient to distinguish the interacting
> mechanisms by the deadline. Job reconciliation remains incomplete. Priya
> has not supplied the acceptance observation window."

This is supplied evidence inside the example, not a check executed by the
skill or proof that an untested condition cannot reproduce the stall.

The report supports investigating the combined deployment-plus-peak
condition for C2. It does not select deployment alone or workload alone as
the sole cause, prove Kafka fixes it, establish a universal threshold, or
settle C1. Exceeding the known policy value is observable; its status as an
accepted success criterion is still U3. Incomplete job reconciliation prevents
a conclusion that no actual jobs were lost.

**Definition: DRAFT; resolution: PARTIAL.** The available record identifies a
reproduction condition and supports a conditional plan. Causal separation,
acceptance, and whole-outcome verification remain incomplete. No full solving
method has been attempted. The next useful step is to retain the combined
condition in the proposed validation and inspect the missing records. A
controlled experiment can be proposed; it may be executed only under actual
authority and available capabilities. The deadline does not force a migration
GO/NO-GO verdict or a technology decision outside this assignment.

## 9. Supported migration plan due tomorrow

The authorized artifact can contain this concrete planning content now:

| Plan part | Supported content | Conditional commitment or missing input |
|---|---|---|
| Scope and authority | Plan migration to Kafka; preserve C1 and C2 and the production-change exclusion. | Effectiveness remains unverified. Implementation is outside this request. |
| Current-state inventory | Inspect incident classes, job outcomes, deployment history, queue semantics, and recovery records. Record evidence and gaps. | System-specific mappings depend on actual architecture; identify owners from records rather than assigning invented people. |
| Compatibility and preservation | Map current acceptance, acknowledgement, ordering, retry, and recovery behavior to target behavior. Track every accepted job across any proposed transition. | Required semantics and treatment of duplicates must be recovered before choosing procedures. |
| Migration approach | Compare the staged and rehearsed-cutover options in section 7 against the same obligations. | Select procedures only when architecture, interruption tolerance, and rollback limits are known. No dates or durations are asserted without support. |
| Validation | Propose job reconciliation for C1 and measured recovery for C2, including the combined deployment-plus-peak reproduction condition. Label `T`, `W`, and `L` with their individual unresolved marks. | Record actual checks separately when they occur. A test plan does not establish acceptance or performance. |
| Recovery and commitment points | Document each proposed step's reversibility and retained job history; make expansion depend on evidence for both criteria. | Never promise rollback before its feasibility is established. Production actions need authority beyond this planning assignment. |
| Next authorized work | Finish the draft, inspect accessible records, and incorporate material stakeholder answers with provenance. | An inconclusive causal finding remains in the plan; it does not require another approval to keep drafting. |

This plan is supported drafting progress with explicit gaps. It is not a
claim that migration steps ran or that the incident outcomes improved. A memo
may accompany it; it does not replace the requested artifact automatically.

## 10. Open proposal, reaffirmation, and confirmation variants

These variants change only the stated input; they are not extra turns in the
main trace.

| Variant input | Appropriate behavior |
|---|---|
| "Kafka is an open proposal; compare whether we should migrate, and include a draft migration plan." | Compare it with alternatives using the still-provisional criteria. Preserve the supported requested draft and qualify its selection assumptions. |
| "Kafka is binding; your responsibility is delivery planning." | Use the main trace. Assess effectiveness independently and plan within the binding choice. Do not reopen the technology decision merely because acceptance is OPEN. |
| After one definition challenge: "I understand the uncertainty. Prepare the Kafka migration plan as requested." | Honor the reaffirmation already in the conversation. Produce the supported conditional plan and note residual uncertainty once; do not repeat the challenge or seek approval to draft it. |
| "The function, zero-loss goal, and every-stall 15-minute criterion are confirmed," with no horizon or workload profile supplied | Update U1–U3 from the actual answers. Keep U4 and U5 OPEN and the definition DRAFT. These answers do not supply an observation window; any allowance for an accompanying memo would not settle it either. |
| Agreed operational criteria and three reasoned failed designs; broader business rationale is unknown | Adopt the sufficient contract and use solve. Do not reopen definition or demand a separate mandate. |

If an owner is unreachable, retain the exact OPEN questions or clearly mark
an evidenced working assumption ASSUMED under the shared contract. A reachable
owner's silence is not an answer. If no owner is known, carry that fact and
the ownership question instead of inventing one.

## 11. Handoff record

For this trace, carry the following readable record into the next appropriate
work. Do not reconstruct it from the new method's perspective.

```text
Identity: Q-1, the authorized queue migration planning task.
Problem: Copy P from section 5.
Criteria: Copy C1 and C2, including U2-U5 and every validation limit.
Fixed facts: Carry the supplied input from section 1; add the section 8 report
  only for that continuation, clearly labeled as supplied evidence.
Constraints and non-goals: Copy section 5, preserving Kafka's binding status,
  tomorrow's planning deadline, both criteria, and no production changes.
Authorized work: Draft the migration plan and inspect available records.
Unresolved items: Carry U1-U5 verbatim with their current marks, exact questions,
  and Priya as owner; carry the missing domain facts and unknown record owner.
Definition: DRAFT until each material unresolved acceptance item is settled.
Resolution: PARTIAL for the inconclusive continuation, with its evidence limits.
Effort: No full-method attempts consumed here; carry the shared budget unchanged.
Next work: Complete supported drafting and evidence gathering. Use diagnosis
  for the reported failure; use solve only for a sufficiently defined problem
  that is genuinely stuck. A declined handoff returns a reason and progress.
```

Only an explicit revision with its source changes a field or mark. Inherited
OPEN or ASSUMED items permit conditional exploration and stay unresolved after
a method runs. Any result verified under a draft definition states that
condition; it cannot claim stakeholder acceptance has been settled. Handoffs
preserve original obligations and remaining effort under the shared contract.
