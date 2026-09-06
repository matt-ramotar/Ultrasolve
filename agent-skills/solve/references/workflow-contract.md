# Shared workflow contract

Load this reference before definition, candidate construction, or a full method.
It governs all public entries and all six method modules. Method modules consume
this contract; they do not restart definition or reconstruct inherited fields.

## Authority and restrictions

Honor the user's authorized deliverable, decisions, actions, and existing time,
depth, cost, and scope instructions. Using a method grants no additional authority.
A draft plan is not authorization to implement it. Distinguish a binding choice
from the hypothesis that it will achieve its intended outcome: retain the former
as a constraint while assessing evidence for the latter.

User and host restrictions on a method, resource, action, or decision prevail.
If a required read or action is denied, end that path. Do not retry through an
alias, another loader, a copied or relocated instruction, or an equivalent action.
Do not improvise a missing method. Return the precise unavailable dependency or
restriction, and continue only independently useful work that is already allowed.

Public leaf commands and the router's method library are distinct entry routes.
The router reads its canonical method modules through a permitted file-reading
capability; it does not invoke public leaf commands or read their entrypoints as
a loading fallback. Before applying a direct leaf, load this reference and the
complete corresponding module. Before routing, check all eighteen required
resources: eight canonical entrypoints, six method modules, and the four router
references identified by the router. Report all missing or inaccessible resources
in one collection-integrity error before transforming anything. Accessibility
checks do not require loading every unselected method into context.

## Consistent entry decisions

| Situation | Disposition |
|---|---|
| Ordinary well-scoped work, even after one failed attempt | Work directly; do not manufacture a definition or solving exercise |
| Felt difficulty with an unsettled outcome or competing definitions | Use the definition entry, proportionally |
| Pure ideation with no felt problem | Use available brainstorming, otherwise handle locally |
| Reproducible failure with an evidence trail | Use evidence-led diagnosis: observation, reproduction, isolation, verification; methods supply bounded support only |
| Defined problem with reasoned dead ends, defeating constraints, or no credible route | Use the solving router |
| Explicit applicable leaf request | Apply that method; repeated failure is not an additional prerequisite |
| Agreed operational criteria but unknown higher-level business rationale | Use the sufficient operational contract; do not demand a separate mandate |

For a direct leaf request, assess its applicability and the definition/diagnosis
boundaries before the ordinary-work default. An explicit method request can be
useful even when automatic solve would be unnecessary. If a handoff is declined,
return a disposition and reason; do not bounce the same unchanged problem back.
Neither reloading an entry nor rephrasing the request resets routing history.

## Problem contract and inheritance

Keep a readable record with these fields. Reuse the original wording when adopting
an existing contract; no new application, persistence layer, or formal schema is
required.

| Field | Required content |
|---|---|
| Problem | Original `P` and an identifier or unmistakable task reference |
| Success criteria | Observable criteria with stable local IDs; evidence or unresolved status for each acceptance parameter |
| Fixed facts | Supplied or observed facts, with evidence where available |
| Constraints and non-goals | Binding requirements and excluded scope; non-goals remain constraints downstream |
| Authorized work | Requested deliverable, binding decisions, and delegated actions |
| Unresolved items | Exact unknown or settling question, owner when known, CONFIRMED/OPEN/ASSUMED mark, and its relevance |
| Definition status | CONFIRMED or DRAFT; any unresolved acceptance or mandate parameter keeps the definition DRAFT |
| Effort remaining | User budget or default full-method attempts remaining, with attempts already consumed |

Adopt an existing problem contract without reconstructing it. Preserve its original
problem, criteria, facts, constraints, non-goals, authorized work, unresolved items,
and remaining budget. Carried OPEN or ASSUMED stakeholder questions permit
explicitly conditional exploration; they never become confirmed because a method
runs. Identify other unknowns that block the selected claim or action, and
distinguish them from questions this investigation will answer. Gather accessible
evidence yourself. If required evidence is unavailable, return a useful partial
result or identify the precise blocker. Any revision to the contract is explicit,
states its source or authority, and retains the prior obligations until they are
deliberately changed.

Do not invent an owner. Mark an unknown owner as unknown and identify who can
settle that ownership question. Never promote a proposal to an effectiveness fact,
silently relabel an observation as a binding decision, or discard a non-goal.
A real authorized scope revision records what changed and the effort remaining.
New wording, identifiers, lenses, or subproblems do not create fresh budgets.

## Proportional definition

Determine decision scope from existing context. Keep a supplied binding means as
a constraint even when its effectiveness is uncertain; compare a still-open
proposal with alternatives. Preserve supported portions of the requested artifact,
marking assumptions and conditional commitments. Recommend another deliverable
when useful, but do not substitute it unilaterally because criteria remain OPEN.
Honor prior reaffirmation. Challenge the same decision at most once unless material
new evidence changes the concern; a reloaded skill cannot require another challenge.

Start with a compact provisional definition, ordinarily around 250 words and at
most two unanswered questions that materially affect the next step. This is a
presentation target, not a reason to omit important facts or disregard requested
depth. Expand for contested ownership, interacting uncertainty, or an explicit
deep-definition request. Ask one question or none when that suffices. Gather
accessible facts yourself; silence is never confirmation. Causal hypothesis tables
are unnecessary when no causal claim is being assessed.

Every numeric threshold, observation horizon, and other acceptance parameter must
be supplied, justified by an explicit derivation, or labeled proposed and unresolved.
Unrelated answers do not confirm it. Hypotheses may overlap unless exclusivity is
justified. Preserve joint mechanisms and inconclusive outcomes without enumerating
every combination. A deadline bounds work; it supplies neither causal evidence nor
an unsupported GO/NO-GO decision. Include an authorized conditional or reversible
next step when evidence is inconclusive.

## Results and evidence

Report definition status separately from one resolution status:

| Resolution | Evidence required |
|---|---|
| VERIFIED | Evidence supports every original success criterion and constraint for the claimed result |
| CANDIDATE | A concrete proposed solution exists, but required validation has not occurred |
| PARTIAL | Useful progress exists without a fully supported whole solution |
| INFEASIBLE | A contradiction or impossibility argument follows from stated premises; failed search is insufficient |
| BLOCKED | A named unavailable input, capability, or authorization prevents the next necessary step and no further useful work on that step is supported |

`definition: DRAFT; resolution: VERIFIED` means technical verification conditional
on the draft definition. State that condition explicitly; it does not settle the
stakeholder's outcome. Preserve each OPEN/ASSUMED item with its owner and question.

For each original criterion, identify supplied evidence, executed checks and their
observed results, derived conclusions, and proposed checks separately. A test plan
is not a passing test. A performance target is not a measurement. Match the check
to the claim and explain the limits of a proof, simulation, test, or observation.
No status is a substitute for the evidence supporting it.

Return a compact useful result: the problem, selected move, candidate or progress,
criterion evidence and gaps, both statuses, effort consumed, and the next useful
step. Preserve method-required audits, expanding their presentation when needed.

## Effort and composition

Apply the user's existing effort budget. Without a larger authorized effort,
compare one to three cheap candidates, execute one full method, and allow at most
one further full-method attempt: two full attempts total for the same problem.
A direct leaf execution or a full method on a subproblem consumes one attempt.
Handoffs, re-entry, renamed candidates, and new problem identifiers do not reset
the count. Record a larger bound when the user has already authorized one; do not
repeatedly self-extend the default by declaring another candidate promising.

After each full method, perform a map-back checkpoint against the original
contract. A checkpoint can be partial or unsuccessful. Carry its useful result
and every outstanding obligation into a bounded next method. The first method
need not solve the whole problem before another can help. A solved subproblem is
not a verified whole solution.

Stop exploration when solved, infeasibility is established, required evidence is
unavailable, the budget is exhausted, or another attempt has no credible information
gain. Do not call exhaustion proof of impossibility or make it a routine permission
question. Return the best supported result, remaining obstruction, and the cheapest
discriminating next step. Continue independently useful work already authorized.
