# Selecting a Technique

Use this reference during the router's internal diagnosis. Consider all six
lenses, select one to three strong matches, and expose only the useful routing
decision. Load the [shared workflow contract](workflow-contract.md) and apply its
eligibility, authority, inherited problem record, evidence rules, and remaining
effort before selecting a method. An agreed operational problem and criteria
suffice even when its higher-level business rationale is unknown; a separate
mandate is not a routing prerequisite.

## Symptom map

| Stuckness symptom | Strong lens | Cheap candidate |
|---|---|---|
| Constraints, edge cases, or requirements interact until every design collapses | Simplify | A stripped skeleton plus the first constraints to restore |
| The problem has a recognizable abstract shape that may exist in a solved domain | Analogize | At least two possible source problems worth fact-checking |
| Repeated descriptions preserve the same framing and lead to the same dead end | Restate | Three invariant-preserving representations or viewpoints |
| A solved principle may cover the case, or an awkward special case hides cleaner structure | Generalize | A broader result-first claim or a structure-exposing parameterization |
| The problem is too entangled to answer as one unit and has no credible first step | Decompose | Several candidate seams with answerable outputs |
| The end state is clear but forward routes are invisible | Invert | A backward graph of alternative predecessors, actions, and uncertain edges |

Symptoms are evidence for selection, not proof. Read each selected canonical
method module in full before constructing its cheap candidate. The modules live
under `methods/`, relative to this reference: `simplify.md`, `analogize.md`,
`restate.md`, `generalize.md`, `decompose.md`, and `invert.md`. They are the
router's method library; public leaf commands and entrypoints are not dispatch
fallbacks. End a missing or denied method path without reproducing it through
another route.

## High-value combinations

An arrow has two valid meanings:

- During cheap comparison, one candidate informs another without executing
  either full method. Preserve each module's candidate requirements.
- During full execution, one completed method reaches a map-back checkpoint
  against the original contract, then another method addresses a bounded
  remaining question. The checkpoint may be partial or unsuccessful; it need
  not verify a whole solution before a second method can help. Preserve useful
  progress, outstanding criterion obligations, non-goals, and unresolved marks.

Execute one full method first. Without a larger already-authorized effort, the
shared budget is two full attempts total for the same problem. A full method on
a subproblem consumes an attempt too. Handoffs, renamed candidates, and re-entry
do not reset the count. Do not hide full execution inside a cheap candidate or
start another full method before the preceding map-back checkpoint.

- **Restate → Simplify:** a changed representation can reveal which
  constraints are incidental and safe to strip temporarily.
- **Simplify → Analogize:** a skeleton often exposes a known abstract shape;
  verify source facts and mapping breaks before porting anything back.
- **Invert → Decompose:** alternative predecessor branches can suggest
  answerable seams. Preserve the graph; do not pretend it is a single chain.
- **Decompose → Analogize:** a bounded subproblem may have a stronger known
  counterpart than the original whole.
- **Generalize → Simplify:** a broader structure can identify parameters to
  hold fixed while recovering the requested special case.

Use combinations only when both lenses are strong matches. The router still
produces one cheap artifact per selected lens and chooses one full method
first. For example, decompose may expose a seam whose mechanism is unresolved.
Its checkpoint records the useful seam and every original obligation still
unmet. Analogize can then consume the remaining default attempt on that seam,
with a second checkpoint against the whole problem. Solving the seam alone is
not whole-result verification.

## Close alternatives

Mention a rejected lens only when it was close or its rejection changes how the
chosen route should be interpreted. Common boundaries:

- **Simplify vs. Decompose:** simplify when interactions among constraints are
  the obstacle; decompose when independently answerable seams are available.
- **Restate vs. Generalize:** restate when representation is trapping the work;
  generalize when a broader solved principle or parameterized structure could
  cover the case.
- **Analogize vs. Generalize:** analogize transfers verified structure from a
  different solved domain; generalize broadens a result or the current case's
  structure.
- **Invert vs. Decompose:** invert when a precise end state enables backward
  hypotheses; decompose when forward questions already expose useful seams.

## Rut avoidance

- Record the lens, candidate, result, what was learned, and effort remaining.
- Do not rerun an unchanged lens without new facts or a materially different
  candidate.
- If no candidate is credible, inspect the inherited contract and evidence for
  a specific obstruction. Do not reconstruct its criteria, invent facts, or
  reopen a binding decision. Any contract revision needs an explicit source or
  authority and preserves prior obligations until deliberately changed.
- In debugging, use inversion only to generate bounded hypotheses, then return
  to evidence-led diagnosis for testing.

Carried OPEN or ASSUMED stakeholder questions permit explicitly conditional
exploration and retain their owner, settling question, and status. They do not
create an extra definition gate. Distinguish an unknown that blocks a selected
claim from an unknown the investigation can resolve. Gather accessible evidence
yourself; unavailable necessary evidence limits the claim or next action.

Use the shared entry decisions when there is an actual definition gap: an
unsettled outcome or competing definitions in a felt problem calls for
proportional definition; pure ideation calls for available brainstorming or
local ideation. A declined handoff returns its disposition and reason instead
of bouncing the same unchanged problem back.

## Bounded ending

Stop exploration when solved, infeasibility follows from stated premises,
necessary evidence is unavailable, the shared effort bound is reached, or
another attempt has no credible information gain. Return the best supported
result, remaining obstruction, and cheapest discriminating next step without a
routine permission question. Continue independently useful authorized work.

Report definition status independently of the shared resolution statuses:
VERIFIED, CANDIDATE, PARTIAL, INFEASIBLE, or BLOCKED. Use criterion-specific
evidence to justify the status. A planned check is not an observed result, and
failed search is not an impossibility proof. Partial map-back preserves progress;
it never promotes a transformed answer into a verified whole solution.
