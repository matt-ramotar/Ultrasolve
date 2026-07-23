---
name: define
description: "Use when nontrivial work is about to be planned, scoped, or committed and no agreed problem statement exists: a solution, artifact, or deadline is named without a stated or recoverable outcome; success is subjective or a metric's underlying stake is unknown; symptoms presume a cause or fix; or stakeholders define success differently. Not for agreed problem-level criteria, a defined problem that is merely stuck or rutted, evidence-led diagnosis, ordinary well-scoped tasks, or open-ended ideation without a felt problem."
---

# Define

## Direct-invocation boundaries

- If `P`, observable success criteria, fixed facts, and constraints can be
  stated without inventing content, do not use this method: work the request
  directly, use `../solve/SKILL.md` when it is genuinely stuck, or
  `../restate/SKILL.md` when only its formulation is rutted. A clear,
  well-scoped task is its own definition, even when it names a solution and
  leaves its outcome unstated.
- A reproducible failure with an evidence trail belongs in evidence-led
  diagnosis. Define applies when what "failing" means is itself contested.
- Pure idea generation with no felt problem belongs in a brainstorming
  workflow when available. Definition needs something that happened.
- If the requester has already heard the definition challenge and reaffirmed
  the original request, execute it and record residual doubt in one sentence.
  A deadline alone is not that reaffirmation.

## Provenance: sources and authored synthesis

Nothing here derives from Shannon's 1952 talk, which assumes a problem
already in hand. Adapted cores: Polya's understanding-the-problem phase —
unknown, data, condition, and its adequacy questions (*How to Solve It*,
1945); Duncker's functional analysis of pre-attached solutions (1945);
Keeney's "why is that important?" regress with its decision-context stopping
rule (*Value-Focused Thinking*, 1992); multiple working hypotheses
(Chamberlin 1890, via Platt 1964; Heuer). The ledger sort, mandate marks,
candidate register, decision-point ending, and agreement block are authored
synthesis. Sources and rejected folklore:
[problem-posing sources](references/problem-posing-sources.md).

## Entry contract

Record verbatim: the request, who asks, what changed to make it arrive now,
and whether that stakeholder is reachable. Record any deadline as a
constraint on the response, never as evidence for the proposal it arrived
with. These are inputs to definition, never its frame.

## Method

1. **Sort the request into a ledger.** Label every load-bearing claim exactly
   one of: observation, constraint, stake, or proposal — candidate causes,
   fixes, and the requested artifact itself. For each proposal, state what
   having it was meant to do for the owner; that function joins the goal
   material. Nothing labeled proposal may reappear as a fixed fact, a
   success criterion, or the skeleton of the deliverable.
2. **Regress the goal to the mandate.** Ask why that matters to the owner,
   at least one rung past the first handed-down metric, until one more why
   would leave the owner's decision context or stop being actionable; the
   rung below is the working mandate. Mark it CONFIRMED by the stakeholder,
   or OPEN with the exact settling question addressed to a named person;
   when no one is reachable, adopt the best-evidenced rung labeled ASSUMED.
   Never infer it silently.
3. **Count the problems.** If evidence could move bundled symptoms
   independently, split them and define each.
4. **Write the problem contract.** `P` in one paragraph naming no candidate;
   observable success criteria that would still detect success if every
   proposal were never built, with current values where known; fixed facts;
   constraints; non-goals; missing domain facts. Gather world facts — logs,
   metrics, code — yourself; write stakeholder facts as closed questions,
   never invented to keep moving. Audit the condition: satisfiable,
   sufficient, contradictory, or redundant? Already satisfied or
   contradictory means the problem dissolves or needs owner negotiation.
5. **Hold hypotheses symmetrically.** Carry the requester's causal claim, at
   least one rival, and the undramatic middle cases: nothing broken, merely
   worse; metric artifact; no problem. Attach to each the observation that
   would discriminate it. Assign no likelihood before that observation
   exists.
6. **Register candidates.** At least two rows plus a do-nothing or
   smallest-credible-intervention row; a received solution enters as an
   ordinary row, one line each against the success criteria. No-go lives
   here.
7. **End at a decision point.** One branch per hypothesis, middle cases
   included; each branch names its own next deliverable, possibly a
   different artifact than requested. Dates bound evidence gathering only —
   no phases, durations, or workstreams past the decision.
8. **Agree, then deliver.** Present the record with two to four closed
   confirmation questions. If an artifact is due first, ship the record,
   register, and decision point as a decision memo by the deadline — not the
   requested plan; a commitment-shaped artifact ships only once its
   go-condition holds. With OPEN or ASSUMED marks it is a draft, not a
   mandate.

## Compact example

"Leadership approved Kafka for our queue incidents; migration plan by
tomorrow." Kafka is a proposal beside broker tuning, a managed queue, and
do-nothing; its function: durable delivery under peak. Ladder: fewer pages →
customer-visible data loss (mandate, OPEN). Criteria: lost-job reports at
zero for a quarter, stalls recovered inside the paging window — meaningful
with Kafka never built. Deliverable: a decision memo ending at go/no-go,
shipped by the deadline. A fuller trace:
[worked example](references/worked-example.md).

## Result and handoff

Return one problem contract — `P`, observable success criteria, fixed
facts, constraints, non-goals, and missing domain facts — plus the ledger,
the mandate rung with its mark, hypotheses, the candidate register, open
questions, and the decision point. In any handoff, non-goals hand off as
constraints, and OPEN or ASSUMED marks travel with the contract together
with their settling questions; a consumer that verifies work against this
contract must restate that unresolved status in its result — a verified
answer to a draft definition is itself a draft. Route by outcome: a defined
problem with a credible route proceeds as ordinary work, not through
`../solve/SKILL.md`; a defined and genuinely stuck problem hands the
contract fields to that router's State step verbatim; a dissolved problem
is reported with its dissolving evidence, and work stops; a reproducible
failure surfaced here hands its hypotheses to evidence-led diagnosis as
bounded input. If the router arrived here because its State step could not
state `P`, do not hand back without new stakeholder facts or, when the
named stakeholder is unreachable, without the mandate rung explicitly
labeled ASSUMED and carried in the returned contract as an unresolved mark.

## Failure modes

- A pre-attached solution kept as the deliverable's skeleton, validation
  demoted to a phase inside it.
- Success criteria naming a candidate or measuring only process.
  Solution-complete is not problem-resolved.
- Regress stopped at the handed-down metric — or overshot to an
  unactionable rung and left there.
- A counter-hypothesis installed as most likely before discriminating data,
  or gates omitting the worse-but-not-broken middle case.
- Phases, durations, or workstream skeletons attached to post-decision work.
- Treating a written record as an agreed one; inventing stakeholder answers
  to avoid asking.
- Erasing the requester's candidate instead of registering it, so diligence
  reads as insubordination and comparison becomes impossible.
- Dropping non-goals or OPEN/ASSUMED marks at a handoff, so downstream work
  expands into excluded scope or reports a draft as settled.
