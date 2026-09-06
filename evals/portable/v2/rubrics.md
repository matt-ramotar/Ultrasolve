# Portable v2 evaluation rubrics

These are authored evaluation criteria, not measured model or judge results.
The twelve transfer cases M01–M12 are held out from this plugin's shipped
worked examples only. The other 52 acceptance cases include regressions
intentionally related to those examples. These cases are not confidential and
are not guaranteed unseen during model training. The documented transfer
constraints reflect authoring judgment, with no claim of confidentiality or
statistical generalization.

## Evaluation contract

`cases.json` stores exact substantive user messages. In a plugin arm with
explicit invocation, prepend the setup's exact host prefix to the first
message only. In automatic cases, prepend nothing. Baseline arms receive
`turns[].message.content` unchanged and omit only that invocation prefix. Do
not remove constraints, source facts, requested depth, or method-related
substantive wording to change a baseline. No host runner or unsupported host
flag is defined by these assets.

Each turn after the first has an observation-based release. Retain the actual
assistant response and required observation; never synthesize a challenge or
a successful prerequisite. Follow the release's failure disposition. A missing
observation is a failed or unavailable prerequisite, never desired behavior.
Evaluate obligations at their source turn and carry them forward unless a
later user message explicitly revises them. A19's later answers settle only
the answered parameters; they do not manufacture an observation window.

Every invariant has a stable ID, exact source quote, and required outcome
criterion. Outcome assertions assess substantive obligations and may pass
without plugin headings or vocabulary. Every case also has a concrete
whole-result assertion. Judge arithmetic, causal limits, and constraint
preservation, not the appearance of expected words. Method vocabulary is
neither proof of preservation nor proof that the method was performed.

Report invocation, method, outcome, and utility labels separately. A correct
answer with wrong activation does not receive an undifferentiated pass; absence
of plugin terminology does not fail a correct outcome. The baseline has no
plugin invocation obligation: label that criterion `not_assessable`, without
counting it as a compliance pass or failure. If a requested method is routed
away, assess the boundary disposition rather than requiring an inapplicable
transformation.

For a baseline, assess a particular lens's M-process criterion only when that
lens or equivalent substantive obligations are present in the unchanged user
messages. When they existed only in the removed invocation prefix, label that
lens-specific M-process criterion `not_assessable`; do not import an obligation
from setup, the plugin rubric, or the expected route into the baseline prompt.
A08's generic "requested method" wording does not identify a particular lens
after the prefix is removed. A13 requests a method but does not require restate
or three representations in its substantive text. Their baselines can use a
correct alternative approach without failing the absent lens obligation.
Continue to judge all applicable outcome and utility criteria independently.
Where substantive messages actually request a particular lens or equivalent
reasoning steps, assess those obligations without requiring plugin terminology
or plugin loading. This does not remove or rewrite any baseline message.

A null `expected_definition_status` and empty `allowed_resolution_statuses`
mean that the task is outside the plugin's problem/result protocol, such as
ordinary clamp work or pure ideation. Do not demand definition or resolution
labels there. Elsewhere stored statuses constrain the substance of the claim;
equivalent plain language is sufficient. CONFIRMED describes the accepted
definition, not whether a design works. Technical verification under a DRAFT
definition remains explicitly conditional on its unresolved acceptance terms.
A10-parameterization-only deliberately covers DRAFT plus VERIFIED: the proof
of ten pairs is valid under the five-guest assumption while Maya Chen's actual
guest-list decision remains OPEN. This is a conditional mathematical result,
not verified deployment or stakeholder agreement.

`evidence_source: trace` requires the actual ordered host trace. A statement
that a skill was loaded is not that evidence. Missing traces, blocked reads,
unsupported capabilities, or no authorized run leave relevant criteria
`not_assessable`; they cannot pass from reading the fixture. Answer criteria
use actual outputs; combined criteria reconcile outputs with observed actions.
Integration setups list required capabilities, not an assertion that isolation
or the case has been executed.

Use `pass`, `fail`, or `not_assessable` per criterion with decisive evidence.
A required criterion lacking sufficient evidence is not a successful run.
Optional utility never compensates for a failed required outcome. Record cost,
latency, and downstream utility only when actually measured in an authorized
run. Structural tests validate these assets and authored labels; they never
judge semantic correctness or award calibration accuracy.

## R-OBLIGATION

Category: outcome.

Pass: The answer respects the case-specific assertion for the referenced
invariant, including numeric limits, action authority, evidence, ownership,
uncertainty, and temporal scope. Verbatim repetition is unnecessary if the
result clearly preserves it. Later authorized revisions affect only the
fields actually changed.

Fail: Contradict, drop, silently weaken, or fabricate a load-bearing input, or
claim a result beyond the necessary evidence.

Pass example: Retain both offline edits and parent links while displaying an
unresolved red/blue conflict.

Fail example: Say "all constraints preserved" while deleting the only
operation history that enables rollback.

## R-REASONING

Category: outcome.

Pass: The concrete result satisfies the case's whole-result assertion and all
referenced obligations. Verify arithmetic, feasibility, causality limits, and
cross-stage interactions directly. Equivalent valid solutions are allowed;
an illustrative answer is not an exclusive implementation prescription.

Fail: Return an unsupported or wrong conclusion, violate a required condition,
or mistake a subproblem result for a complete solution.

Pass example: Derive four required simultaneous display slots greater than
three available unit-capacity slots.

Fail example: Call packing impossible because two attempts failed, or make it
feasible by silently staggering the display times.

## R-EVIDENCE-STATUS

Category: outcome.

Pass: The supported claim matches the definition state and allowed resolutions,
with supplied observations, derivations, proposed checks, and executed checks
distinguished. Respect unavailable tools and unanswered acceptance parameters.
No particular status label is mandatory.

Fail: Claim an unrun benchmark passed, an unanswered parameter was agreed,
a design is verified without criterion evidence, or search proves impossibility.

Pass example: "This is a conditional design; the revocation test remains
proposed because no target is running."

Fail example: "VERIFIED: p99 was 18 ms in 100,000 requests" without a runnable
target or supplied benchmark evidence.

## R-INVOCATION

Category: invocation.

Pass: The actual plugin-arm trace matches the expected disposition and
activation boundary. A direct entry may inspect applicability before routing
away. Router composition reads full canonical modules through permitted reads
without invoking public leaf commands as fallback. A resource-stop trace and
its error satisfy the stated integrity/restriction condition.

Fail: Automatically solve ordinary work or primary diagnosis, manufacture a
problem for pure ideation, use a prohibited loader, or bypass a denial. Without
a trace, use not_assessable.

Pass example: An explicit simplify entry routes undefined onboarding to
definition before constructing a skeleton.

Fail example: Automatic solve produces a correct clamp. The mathematical
outcome can pass while invocation fails.

## R-METHOD-DEFINE

Category: method.

Pass: Clarify the material outcome gap proportionally, preserve binding choices
and supported artifacts, and retain individual unresolved parameters. Respect
requested depth and reaffirmation. Ask useful unanswered questions; use causal
comparisons only when assessing causality.

Fail: Force a full interview on a small ambiguity, reopen a binding decision,
replace an authorized artifact automatically, repeat a settled challenge, or
force exclusive causality at a deadline.

Pass example: Draft the binding wiki plan with open retrieval criteria and a
question to its supplied sponsor, without another approval to draft.

Fail example: Withhold the requested plan and deliver only a go/no-go memo until
every acceptance question is answered.

## R-METHOD-SIMPLIFY

Category: method.

Pass: Keep a constraint ledger, choose a stripping order, characterize the
skeleton, and restore constraints with the active set recorded. Qualify
order-dependent attribution. Map useful partial or complete progress back to
original obligations and remaining effort.

Fail: Present a toy answer as complete, drop a retained constraint, or claim
different sole causes merely because the restoration order changed.

Pass example: Show each of x >= 4 and x <= 3 feasible alone and their pair
infeasible in both restoration orders.

Fail example: Blame only x <= 3 in one order and only x >= 4 in the reverse
order without identifying their joint contradiction.

## R-METHOD-ANALOGIZE

Category: method.

Pass: Compare at least two plausible analogies, verify source mechanics from
supplied or obtained evidence, map structure, and turn material breaks into
limits or decisions. Port only licensed mechanics and check target constraints.

Fail: Choose the first familiar analogy without comparison, assume unsupplied
source facts, or inherit a guarantee despite an unresolved mapping break.

Pass example: Compare hotel and gate reservations, then reserve instrument
service plus cleaning without a borrowed queue-fairness guarantee.

Fail example: Buffer samples as if bytes in a queue and claim that waiting
extends their physical stability.

## R-METHOD-RESTATE

Category: method.

Pass: Compare at least three materially different representations or viewpoints;
retain an invariant ledger, label deliberate relaxations, select a useful form,
and restore obligations in map-back. Relabeling alone is insufficient. Keep
proposed checks unexecuted unless actual evidence establishes a run.

Fail: Give synonyms only, embed a pet solution, alter fixed staffing/deadlines/
reachability/permissions, or report an unperformed check as verification.

Pass example: Reframe batch delay through specimen dependencies, worker timelines,
and per-specimen completion, then schedule with the same two technicians.

Fail example: Rename the problem "maximize throughput" and add a third worker
when staffing is fixed.

## R-METHOD-GENERALIZE

Category: method.

Pass: Assess both forms for applicability. Use the sole supported form when
the other lacks its prerequisite; compare both when applicable and select one
primary full route. State limits, instantiate back, and avoid unrequested
infrastructure.

Fail: Invent a solved precedent or useful axis, demand both prerequisites,
skip a relevant comparison, or ship a framework beyond the requested result.

Pass example: Broaden a validated deny-first rule to CSV using the shared
evaluator and mark parameterization inapplicable without a useful axis.

Fail example: Refuse result-only work until given a numeric parameter or claim
a tiling recurrence was supplied when it was not.

## R-METHOD-DECOMPOSE

Category: method.

Pass: Compare more than one seam; express pieces as answerable questions with
outputs, dependencies, and cross-cutting constraints. Recompose and check the
whole. A partial checkpoint may precede another full method while carrying
original obligations and consuming remaining shared effort.

Fail: Cut only by file/team names, lose a cross-stage constraint, or claim
individually successful stages prove whole correctness.

Pass example: Check revocation across old/new search readers and rollback,
including the interval before index updates arrive.

Fail example: Certify replacement because each index returns results while
rollback still exposes a revoked document.

## R-METHOD-INVERT

Category: method.

Pass: Preserve at least two plausible predecessor branches, label necessity,
sufficiency, unknowns, and non-invertible edges, and replay a defensible route
forward from the actual current state. Respect physical/time/authority limits
and distinguish proposed checks from evidence.

Fail: Assume one reverse chain, mistake necessary approval for correctness,
reverse irreversible fabrication, or validate the wrong release artifact.

Pass example: Reject custom fabrication that misses opening after curing and
installation, while planning the supplied feasible rental alternative.

Fail example: Call a release ready from approval despite a mismatched signature
and current-candidate audit-retention failure.

## R-METHOD-ROUTER

Category: method.

Pass: Check all eighteen resources before candidates; adopt the contract;
consider lenses proportionally; fully read selected modules before candidates;
execute within remaining effort; and checkpoint original obligations after
each full attempt. Preserve conditional uncertainty and partial work. Exhausted
effort or failed integrity permits the appropriate stop without a full method.

Fail: Use public entries as fallback loaders, ignore missing unselected resources,
reset effort, hide full execution in cheap comparison, or require full success
before a second bounded method can help.

Pass example: Checkpoint a useful partial decomposition before analogize takes
the second and final default attempt on its unresolved seam.

Fail example: Rename the same task after two failed full methods and start a
third without a larger authorized budget.

## R-METHOD-DISPOSITION

Category: method.

Pass: Handle ordinary work directly, pure ideation through available brainstorming,
evidenced failure through diagnosis, and missing/denied resources with an honest
stop. No inapplicable full method is required.

Fail: Manufacture a problem ritual, replace diagnosis with speculative lenses,
ignore a missing dependency, or bypass a denied resource.

Pass example: Correct one reversed clamp expression directly, or diagnose the
supplied check-then-write race and propose an unexecuted regression check.

Fail example: Automatically solve the clamp or copy a denied method elsewhere
to continue applying it.

## R-UTILITY

Category: utility.

Pass: Provide a concrete useful artifact or supported progress, sized to the
request, with a clear next action or evidence need when material work remains
and the requested output shape permits it. A fully solved function-only answer
needs no next-step prose. Avoid unnecessary approval repetition.

Fail: Return generic advice, an irrelevant artifact, excessive ritual, or no
progress despite independently supported authorized work.

Pass example: Supply a short decision note and one targeted question.

Fail example: Answer a reaffirmed plan request only with "Please confirm you
still want a plan."
