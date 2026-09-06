# Invert method

## Provenance: source and authored extensions

Shannon-derived core: exchange givens and unknowns, reason from an assumed
result, and invert useful stages. Authored extensions: a backward causal graph,
necessary and sufficient labels, alternative branches, and forward replay.

## Shared entry contract

Use the fully loaded [shared workflow contract](../workflow-contract.md).
Consume its established or inherited problem contract without reconstructing
it or restarting a stakeholder interview. Preserve the original problem and
criterion IDs, fixed facts, constraints, non-goals, authorized work, unresolved
OPEN/ASSUMED items with their owners and questions, and remaining effort.
Conditional exploration follows that contract; it does not settle uncertainty.
This module is the same full method for the direct entry and router. It does
not invoke public leaf commands or grant additional action authority.

Apply the shared evidence, result-status, stopping, and composition rules.
A full execution consumes one attempt from the remaining shared budget,
including execution on a subproblem; loading this module does not reset it.

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

At this checkpoint, report definition status separately from resolution status
using the shared contract. Link evidence and gaps to the original criterion
IDs; distinguish supplied evidence, executed checks and observed results,
derived conclusions, and proposed checks. A proposed check is not passing
evidence. Preserve OPEN/ASSUMED owners and questions. An incomplete map-back
can return useful partial progress with its outstanding obligations and
remaining effort; success on a subproblem is not VERIFIED for the whole `P`.

## Failure modes

- Claiming backward reasoning must converge.
- Collapsing alternative branches into one unsupported causal chain.
- Treating necessary conditions as sufficient actions.
- Calling a backward route a validated plan before forward replay.
- Using diagnostic inversion instead of systematic debugging.
