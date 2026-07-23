# Worked Example: Queue Incidents Without Solution Framing

This trace uses only the request and the clearly delimited incident summary
below. The summary is fictional source input created for this worked example;
its contents are received evidence, not inferred analysis.

## 1. Verbatim request

> "Leadership approved Kafka for our queue incidents; migration plan by tomorrow."

### Supplied incident summary (verbatim)

The following block is the complete supplied summary for this worked example.
Every line is input to the trace rather than a conclusion drawn by it.

> - Fourteen incidents were recorded in two classes: lost-job incidents and
>   backlog stalls. Class counts and incident details are omitted.
> - Budget approval occurred.
> - The approved request says Kafka is meant to provide durable delivery under
>   peak.
> - The handed-down operational metric is fewer queue-incident pages.
> - The current on-call policy defines the paging window as 15 minutes.
> - The accountable sponsor is Priya Shah, VP Platform.
> - Priya Shah is reachable today.

Who delivered the request and what changed in the incident pattern are not
supplied. The accountable sponsor's identity and reachability are supplied.

## 2. Ledger sort

The ledger preserves each received claim without promoting the requested
solution to a fact about what will work.

| Claim as received | Ledger label | Treatment |
|---|---|---|
| Kafka migration and the requested migration plan | Proposal | Preserve Kafka as an ordinary candidate, but do not let it frame the problem or the deliverable. |
| Fourteen queue incidents, observed in two classes: lost-job incidents and backlog stalls | Observation | Preserve the combined count. The class split, observation window, and per-incident measurements are missing. |
| Budget approval | Stake | It is a stake signal showing that leadership expects the expenditure to protect something; it does not establish what that protected outcome is. |
| Durable delivery under peak | Stake | The approved request states this intended function. Whether it is the complete function remains OPEN with Priya Shah. |
| Fewer queue-incident pages | Stake | Preserve it as a handed-down operational metric, not as the terminal mandate. |
| Current on-call policy defines a 15-minute paging window | Observation | Preserve 15 minutes as the evidence-backed candidate `T`; policy existence is fixed, while Priya Shah's confirmation that it remains the acceptance threshold is OPEN. |
| Priya Shah, VP Platform, is the accountable sponsor and is reachable today | Observation | Address every stakeholder settling question to Priya rather than inventing her answer. |
| Migration plan by tomorrow | Constraint | Tomorrow bounds the response and evidence available for the decision memo. It is not evidence that Kafka is the right response. |

No proposal is promoted to a fixed fact or success criterion.

## 3. Function extraction

- **Proposal:** migrate the queue to Kafka.
- **Function the proposal was meant to serve:** durable delivery under peak.
- **Status:** CONFIRMED as the function stated by the approved request; whether
  it is the complete function is OPEN.
- **Named owner:** Priya Shah, VP Platform.
- **Exact settling question to Priya Shah:** "Priya Shah, do you confirm that
  durable delivery under peak is the complete function the approved request
  must serve: yes or no?"

The function joins the goal material; Kafka remains in the candidate register.

## 4. Goal ladder to the mandate

| Rung | Working statement | Status |
|---|---|---|
| Means | Migrate the queue to Kafka. | Proposal, not a goal |
| Function | Obtain durable delivery under peak. | CONFIRMED as received; completeness OPEN with Priya Shah |
| First handed-down metric | Reduce queue-incident pages. | CONFIRMED as received |
| One rung past the metric | Reduce incident cost and prevent customer-visible data loss. | OPEN |
| Working mandate | Prevent actual loss of accepted jobs and restore stalled backlogs within the current 15-minute on-call paging window if Priya Shah confirms it remains the acceptance threshold, regardless of queue technology. | **OPEN** |

The ladder stops at an outcome leadership can govern in this decision context.
It does not climb to a generic organizational mission.

**Mandate owner:** Priya Shah, VP Platform; reachable today.

**Exact mandate settling question to Priya Shah:** "Priya Shah, do you confirm
that the mandate is zero actual lost accepted jobs and recovery of every
backlog stall within the current 15-minute on-call paging window, even if Kafka
is not used: yes or no?"

**Paging-window threshold candidate:** `T = 15 minutes`, from the current
on-call policy. The value is fixed input; only its continued use as the
acceptance threshold is OPEN.

**Exact threshold settling question to Priya Shah:** "Priya Shah, do you
confirm that the current 15-minute on-call paging window is the acceptance
threshold for backlog recovery: yes or no?"

Until Priya answers the OPEN function, mandate, and threshold questions, the
mandate and every artifact derived from it remain draft.

## 5. Six-field problem contract

### `P`

Fourteen queue incidents were recorded across two independently observable
classes: lost-job incidents and backlog stalls; the observation window was not
supplied. The supplied classification does not yet establish how many accepted
jobs were actually lost, because job reconciliation and reporting completeness
are missing. It also does not establish whether backlog stalls exceeded the
current 15-minute policy window or whether Priya Shah confirms that policy
window remains the acceptance threshold. The class counts, current outcome
values, and causes are not yet known.

### Observable success criteria

| Provisional problem | Observable outcome criterion | Current value | Fixed verification condition | Why it survives the counterfactual test |
|---|---|---|---|---|
| Lost-job incidents | Actual lost accepted jobs are zero for one complete quarter. Customer-visible lost-job reports are tracked only as a proxy. | Unknown. Fourteen incidents are known in aggregate, but the lost-job count, job-level outcomes, observation window, and report coverage are missing. | Reconcile accepted job identifiers to completed or recovered outcomes and verify reporting completeness. Zero customer-visible reports alone cannot establish zero actual loss. | Job reconciliation detects success even if every registered proposal is never built. |
| Backlog stalls | Every backlog stall recovers within `T = 15 minutes`, the current policy value; whether Priya Shah confirms it remains the acceptance threshold is OPEN. | Unknown. The stall count and recovery-time distribution are missing. The 15-minute policy value is known; Priya's acceptance confirmation is missing. | Measure every stall against the evidence-backed 15-minute candidate threshold and retain draft status until Priya confirms its acceptance role. | Recovery time detects success regardless of which queue technology, if any, is used. |

The criteria name outcomes, not Kafka, a migration, or completion of a plan.
They also keep actual job loss distinct from its customer-report proxy.

### Fixed facts

- The request above was made.
- Fourteen queue incidents were recorded in two observed classes: lost-job
  incidents and backlog stalls.
- The supplied summary omits the class counts and incident details.
- Budget approval occurred.
- The approved request says Kafka is meant to provide durable delivery under
  peak.
- The handed-down operational metric is fewer queue-incident pages.
- The current on-call policy defines the paging window as 15 minutes.
- Priya Shah, VP Platform, is the accountable sponsor and is reachable today.
- A response is due tomorrow.

The approval's existence is fixed; the approved proposal's correctness is not.
The reporting-completeness requirement is also fixed for verification: zero
customer-visible lost-job reports cannot prove zero actual lost accepted jobs
until accepted jobs are reconciled to outcomes and report coverage is shown
complete.

### Constraints

- Return the evidence-backed response by tomorrow.
- Use only evidence available by that decision point.
- Do not treat missing stakeholder answers as facts.
- Evaluate lost-job incidents and backlog stalls independently before selecting
  any shared intervention.

No implementation constraint, operating-cost ceiling, regulatory requirement,
or acceptable service interruption was supplied.

### Non-goals

- Do not commit to a migration before its go-condition holds.
- Do not make the requested migration plan the skeleton of the response.
- Do not collapse lost-job incidents and backlog stalls into one causal claim.
- Do not force one aggregate intervention when the two classes have different
  explanations or independently sufficient responses.
- Do not redesign queue-adjacent systems that evidence does not implicate.

### Missing domain facts

- The incident observation window and count in each class.
- Accepted-job identifiers reconciled to completion, recovery, duplication, or
  actual loss.
- Reporting completeness, including coverage of customer-visible reports and
  evidence of losses that may not produce a report.
- Stall start times and recovery times.
- Incident timestamps relative to deployments and configuration changes.
- Arrival rate, queue depth, consumer capacity, and peak-load shape around each
  incident.
- Current durability, acknowledgement, persistence, retry, and recovery
  settings.
- Priya Shah's answers on function completeness, the working mandate, and
  whether the current 15-minute on-call paging window remains the acceptance
  threshold for backlog recovery.

The condition is provisionally satisfiable and non-contradictory, but the
missing current values and verification evidence prevent a claim that either
provisional problem is already satisfied or that one candidate is sufficient.

## 6. One-or-many split

Evidence can move the two observed classes independently, so the combined
request contains two provisional problems.

| Provisional problem | Observable boundary | Independent movement |
|---|---|---|
| Lost-job incidents | Accepted jobs are actually lost; customer-visible reports are only a proxy that requires complete coverage. | Actual loss can occur without a backlog stall, and durability evidence can change without changing recovery time. |
| Backlog stalls | Queued work stops progressing and exceeds the evidence-backed candidate `T = 15 minutes`; acceptance remains OPEN with Priya Shah. | Recovery can fail without losing accepted jobs, and capacity evidence can change without changing actual loss. |

They may later share a cause, but shared causality is a hypothesis rather than
an entry fact. A shared intervention is eligible only if evidence shows that it
closes both independently verified gaps.

## 7. Symmetric hypothesis table

All seven hypotheses are tested separately against each provisional problem.
No prior likelihood is assigned. In the remaining tables, `T` means the
current policy value of 15 minutes; any acceptance conclusion remains draft
until Priya Shah confirms that policy value as the backlog-recovery threshold.

| Hypothesis | Lost-job discriminating observation | Backlog-stall discriminating observation | Prior likelihood |
|---|---|---|---|
| Queue technology insufficient | Actual lost accepted jobs recur under representative peak after reporting completeness, job reconciliation, correct durability settings, and stable deployments are verified. | Stalls exceed the 15-minute candidate `T` under representative peak while documented capacity settings are correct and deployments remain stable. | None assigned |
| Deploy-process cause | Reconciled actual losses consistently begin after a deployment or rollout action and do not occur under comparable load without that action. | Stalls exceeding `T` consistently begin after a deployment or rollout action and do not occur under comparable load without that action. | None assigned |
| Workload growth | Actual loss begins only after arrival rate or queue depth crosses a measured boundary while deployment and configuration state remain stable. | Recovery exceeds `T` only after arrival rate or queue depth crosses a measured capacity boundary while deployment and configuration state remain stable. | None assigned |
| Config one-off middle case | One isolated setting error accounts for reconciled actual losses, and correcting it removes loss under equivalent load without replacing the queue. | One isolated setting error accounts for stalls over `T`, and correcting it restores recovery under equivalent load without replacing the queue. | None assigned |
| Nothing broken, merely worse | Complete reporting and job reconciliation show zero actual loss, but latency, retries, or page volume have degraded while the loss criterion remains satisfied. | Every stall remains within `T`, but recovery time or capacity headroom has degraded relative to baseline. | None assigned |
| Metric artifact | Correcting the incident classifier or report pipeline removes the apparent lost-job count while complete job reconciliation shows zero actual loss. | Trace evidence shows work continued and no recovery exceeded `T`, while the stall metric falsely labeled healthy pauses as incidents. | None assigned |
| No continuing problem | Complete reporting and job reconciliation over a newly specified verification window show zero continuing actual loss after the recorded event. | Representative-load evidence shows no continuing stalls over `T` after the recorded event. | None assigned |

Observations may select different hypotheses for the two classes. The
requested technology receives no privileged likelihood, and evidence for one
class cannot settle the other.

## 8. Candidate register

| Candidate | Against the lost-job criterion | Against the backlog-stall criterion |
|---|---|---|
| Kafka | Eligible only if evidence shows a queue-technology limit caused actual loss and a representative test reconciles every accepted job to a non-loss outcome. | Eligible only if evidence shows a queue-technology or capacity limit and a representative test keeps every stall within the 15-minute candidate `T`. |
| Broker/Redis durability tuning | Eligible if current persistence, acknowledgement, retry, or recovery settings explain actual loss and corrected settings pass complete job reconciliation. | Eligible if current capacity or recovery settings explain stalls over `T` and corrected settings keep every stall within `T`. |
| Managed queue | Eligible if the service demonstrates zero actual lost accepted jobs with complete reconciliation under the observed peak shape. | Eligible if the service demonstrates recovery within `T` under the observed peak shape. |
| Do-nothing | Eligible when complete evidence selects metric artifact, no continuing problem, or nothing-broken-merely-worse with the actual-loss criterion satisfied; otherwise it fails. | Eligible when complete evidence selects metric artifact, no continuing problem, or nothing-broken-merely-worse with every stall within `T`; otherwise it fails. |

Each candidate remains one row. None becomes the frame of the decision memo.
A shared candidate is eligible only when it independently passes both criterion
columns; passing one column cannot compensate for failing or leaving the other
unverified.

## 9. Decision memo ending at go/no-go

**Deliverable due tomorrow:** this problem record, the classified evidence
available by the deadline, the candidate register, and the following decision
point. The requested migration plan is not shipped before a go-condition holds.

**Evidence bounded by tomorrow:**

- Classify all fourteen incidents and report the count and current values for
  each class.
- Reconcile every accepted job to completion, recovery, duplication, or actual
  loss, and verify the completeness of customer-visible reporting.
- Correlate incident timestamps with deployments, configuration changes,
  arrival rate, queue depth, and recovery.
- Inspect current durability and capacity settings and record whether a
  representative peak test discriminates the seven hypotheses independently
  for each incident class.
- Ask Priya Shah the OPEN function, mandate, and threshold questions; retain
  each mark and exact settling question until she answers.

**Go/no-go question:** For each provisional problem independently, does the
evidence show a continuing deficiency against its success criterion, and, if
so, which bounded candidate has demonstrated that it can close that gap?

| Hypothesis selected | Lost-job branch and landing | Backlog-stall branch and landing |
|---|---|---|
| Queue technology insufficient | **GO to evidence-backed candidate selection for actual loss.** Kafka remains one candidate; the next deliverable is a supported durability decision verified by complete job reconciliation. | **GO to evidence-backed candidate selection for recovery.** The next deliverable is a supported queue or capacity decision verified against `T`. |
| Deploy-process cause | **NO-GO on migration for this class.** Land on a deployment-control correction and a job-reconciliation verification record. | **NO-GO on migration for this class.** Land on a deployment-control correction and recovery verification against `T`. |
| Workload growth | **GO only to the capacity response shown to prevent actual loss.** Land on a bounded capacity decision with complete job reconciliation. | **GO only to the capacity response shown to keep recovery within `T`.** Land on a bounded capacity decision for the stall gap. |
| Config one-off middle case | **NO-GO on migration for this class.** Land on the isolated configuration correction and job-reconciliation verification. | **NO-GO on migration for this class.** Land on the isolated configuration correction and recovery verification against `T`. |
| Nothing broken, merely worse | **NO-GO on a major migration for this class.** Land on do-nothing or the smallest credible response to the measured degradation while retaining the zero-actual-loss check. | **NO-GO on a major migration for this class.** Land on do-nothing or the smallest credible response to degraded recovery or headroom while retaining the `T` check. |
| Metric artifact | **NO-GO on migration and dissolve the apparent loss problem.** Land on the corrected classifier or report pipeline plus evidence of complete reconciliation and reporting. | **NO-GO on migration and dissolve the apparent stall problem.** Land on the corrected stall metric plus trace evidence that no recovery exceeded `T`. |
| No continuing problem | **NO-GO on migration and dissolve the loss problem.** Land on a dissolution record showing complete reporting, job reconciliation, and no continuing actual loss. | **NO-GO on migration and dissolve the stall problem.** Land on a dissolution record showing representative-load recovery within `T` and no continuing stall gap. |

**Mixed-outcome rule:** select a hypothesis and next deliverable separately for
lost-job incidents and backlog stalls. If different hypotheses explain the two
classes, issue separate bounded next deliverables and do not force one
aggregate intervention. A shared intervention is eligible only if independent
evidence shows that it closes both verified gaps.

No post-decision phases, durations, or workstreams are specified. Any later
commitment begins only after the corresponding go-condition is observed.

**Closed confirmation questions:**

1. Priya Shah, do you confirm that durable delivery under peak is the complete
   function the approved request must serve: yes or no?
2. Priya Shah, do you confirm the working mandate is zero actual lost accepted
   jobs and recovery of every backlog stall within the current 15-minute
   on-call paging window, regardless of queue technology: yes or no?
3. Priya Shah, do you confirm that the current 15-minute on-call paging window
   is the acceptance threshold for backlog recovery: yes or no?
4. Priya Shah, may tomorrow's response be the evidence-backed go/no-go memo
   when no commitment condition has yet been observed: yes or no?

## 10. Final contract template and handoff mapping

```text
P: Copy the candidate-free paragraph from section 5 verbatim.
Observable success criteria: Copy both per-problem rows from section 5 verbatim.
Fixed facts: Copy the fixed-facts list and reporting verification condition verbatim.
Constraints: Copy the constraints list verbatim.
Non-goals: Copy the non-goals list verbatim.
Missing domain facts: Copy the missing-domain-facts list verbatim.

Function completeness mark: OPEN
Named owner: Priya Shah, VP Platform
Settling question: "Priya Shah, do you confirm that durable delivery under peak is the complete function the approved request must serve: yes or no?"

Mandate mark: OPEN
Named owner: Priya Shah, VP Platform
Settling question: "Priya Shah, do you confirm that the mandate is zero actual lost accepted jobs and recovery of every backlog stall within the current 15-minute on-call paging window, even if Kafka is not used: yes or no?"

Paging-window acceptance mark: OPEN
Evidence-backed candidate threshold: T = 15 minutes
Named owner: Priya Shah, VP Platform
Settling question: "Priya Shah, do you confirm that the current 15-minute on-call paging window is the acceptance threshold for backlog recovery: yes or no?"

Contract status: DRAFT until Priya Shah answers the OPEN questions.
```

For a defined problem that is genuinely stuck, five core fields map to the
stuck-problem router's State step verbatim:

| Contract field | State-step mapping |
|---|---|
| `P` | Copy verbatim as the original problem. |
| Observable success criteria | Copy verbatim as the criteria for the eventual answer. |
| Fixed facts | Copy verbatim as facts that may not be silently changed. |
| Constraints | Copy verbatim as constraints that may not be silently changed. |
| Missing domain facts | Copy verbatim as facts that could alter the route or answer. |

Non-goals hand off as additional constraints, without being weakened or
discarded. Every OPEN or ASSUMED mark travels with the contract together with
its exact settling question and named owner. A downstream result must restate
the unresolved status; it cannot report a draft definition as settled. In this
example, the function-completeness, mandate, and paging-threshold marks above
all travel with Priya Shah as owner and with their instantiated questions.
