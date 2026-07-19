# Selecting a Technique

Use this reference during the router's internal diagnosis. Consider all six
lenses and select one to three strong matches. Expose only the useful routing
decision to the user.

## Symptom map

| Stuckness symptom | Strong lens | Cheap candidate |
|---|---|---|
| Constraints, edge cases, or requirements interact until every design collapses | Simplify | A stripped skeleton plus the first constraints to restore |
| The problem has a recognizable abstract shape that may exist in a solved domain | Analogize | At least two possible source problems worth fact-checking |
| Repeated descriptions preserve the same framing and lead to the same dead end | Restate | Three invariant-preserving representations or viewpoints |
| A solved principle may cover the case, or an awkward special case hides cleaner structure | Generalize | A broader result-first claim or a structure-exposing parameterization |
| The problem is too entangled to answer as one unit and has no credible first step | Decompose | Several candidate seams with answerable outputs |
| The end state is clear but forward routes are invisible | Invert | A backward graph of alternative predecessors, actions, and uncertain edges |

Symptoms are evidence for selection, not proof. Read the selected leaf's full
instructions before executing it.

## High-value combinations

An arrow has two valid meanings:

1. During comparison, it links dependent cheap candidates. The first candidate
   informs the second without running either full method.
2. During a later deliberate iteration, the first selected method has already
   executed, mapped back, and been verified.

Neither meaning authorizes running multiple full leaves before map-back and
verification.

- **Restate → Simplify:** a changed representation can reveal which
  constraints are incidental and safe to strip temporarily.
- **Simplify → Analogize:** a skeleton often exposes a known abstract shape.
  Verify source facts and mapping breaks before porting anything back.
- **Invert → Decompose:** alternative predecessor branches can suggest
  answerable seams. Preserve the graph. Do not pretend it is a single chain.
- **Decompose → Analogize:** a bounded subproblem may have a stronger known
  counterpart than the original whole.
- **Generalize → Simplify:** a broader structure can identify parameters to
  hold fixed while recovering the requested special case.

Use combinations only when both lenses are strong matches. The router still
produces one cheap artifact per selected lens and chooses one full method
first. It does not run every selected leaf before verification.

## Close alternatives

Mention a rejected lens only when it was close or its rejection changes how the
chosen route should be interpreted. Common boundaries:

- **Simplify vs. Decompose:** use Simplify when interactions among constraints
  are the obstacle. Use Decompose when independently answerable seams are
  available.
- **Restate vs. Generalize:** use Restate when representation is trapping the
  work. Use Generalize when a broader solved principle or parameterized
  structure could cover the case.
- **Analogize vs. Generalize:** Analogize transfers verified structure from a
  different solved domain. Generalize broadens a result or the current case's
  structure.
- **Invert vs. Decompose:** use Invert when a precise end state enables backward
  hypotheses. Use Decompose when forward questions already expose useful seams.

## Rut avoidance

- Record the lens, candidate, result, and what was learned.
- Do not rerun an unchanged lens without new facts or a materially different
  candidate.
- If no candidate is credible, revisit `P`, observable success criteria, fixed
  facts, constraints, and missing domain facts.
- In debugging, use inversion only to generate bounded hypotheses, then return
  to evidence-led diagnosis for testing.
