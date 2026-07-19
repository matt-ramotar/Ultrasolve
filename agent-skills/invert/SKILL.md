---
name: invert
description: "Use when invoked directly or selected by the router because an end state is clearer than the forward route or bounded backward hypotheses could aid diagnosis."
---

# Invert

## Direct-invocation boundaries

- If the problem is open-ended, underspecified, or undefined, use
  brainstorming when available; otherwise define or clarify it locally.
- If missing facts could change the route or answer, use research tools when
  available; otherwise ask the user for the missing facts.
- If a reproducible failure has an evidence trail, return to evidence-led
  diagnosis when available; otherwise perform it locally. This leaf provides
  only bounded transformation support inside diagnosis and does not replace it.

## Provenance: source and authored extensions

Shannon-derived core: exchange givens and unknowns, reason from an assumed
result, and invert useful stages. Authored extensions: a backward causal graph,
necessary and sufficient labels, alternative branches, and forward replay.

## Entry contract

Before transforming anything:

1. State the original problem `P` in one paragraph.
2. State observable success criteria for the solution.
3. List fixed facts and constraints that may not be silently changed.
4. Identify and gather missing domain facts that could change the route or
   answer.

## Cheap candidate route

Write the desired result as a concrete state and sketch a bounded backward
graph with two plausible predecessor branches. Label unsupported edges rather
than forcing a chain.

## Full method

1. Build a backward graph, not an assumed chain. For each edge, name the action
   or mechanism and its expected effect.
2. Label conditions as necessary, sufficient, both, or unknown; do not confuse
   a necessary condition with a sufficient cause or action.
3. Preserve alternative predecessor branches until evidence eliminates them.
4. Mark every non-invertible edge and every edge with unknown sufficiency.
5. Stop when a branch reaches the actual current state or lacks evidence.
6. Convert a defensible backward route into a forward candidate plan.
7. Perform a forward replay from the actual current state and validate each
   action, expected effect, fixed fact, and constraint.

Backward search does not inherently converge.

For diagnosis, use inversion only to generate a bounded hypothesis set, then
return to systematic debugging and evidence-led diagnosis through observation,
reproduction, isolation, and verification. Conduct that process locally when
no dedicated workflow is available; inversion does not replace it.

## Result and map-back

Return the backward graph, edge labels, surviving alternative branches,
non-invertible edges, unknown sufficiency, forward candidate plan, and forward
replay evidence. Map the validated route back to `P` and verify it against the
original observable success criteria. Reject any route that fails replay from
the actual current state.

## Failure modes

- Claiming backward reasoning must converge.
- Collapsing alternative branches into one unsupported causal chain.
- Treating necessary conditions as sufficient actions.
- Calling a backward route a plan before forward replay.
- Using diagnostic inversion instead of systematic debugging.
