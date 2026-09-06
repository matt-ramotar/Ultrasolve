# Simplify method

## Provenance: source and authored extensions

Shannon-derived core: strip inessential features, solve the simpler problem,
then add refinements toward the original. Authored extensions: the constraint
ledger, deliberate trivial skeleton, ordered restoration record, and mandatory
map back.

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

Any constraint relaxed during this lens remains recorded for restoration.

## Cheap candidate transformation

List the relevant constraints, propose a stripping order, and show the first
one or two removals as a candidate skeleton. Prefer the order most likely to
expose the constraint interaction that carries the difficulty.

## Full method

1. Build a constraint ledger containing fixed facts, requirements, edge cases,
   and intentional relaxations.
2. Choose and record a stripping order.
3. Remove constraints in that order until the skeleton is answerable. A
   trivial skeleton is allowed and can be useful.
4. Solve or characterize the skeleton.
5. Restore constraints one at a time. Adapt the solution after each restore.
   Record the active constraint set and the first restoration that reintroduces
   difficulty under this order. That restoration identifies an interaction to
   investigate, not necessarily a sole cause. When causal attribution matters,
   compare another restoration order or a smaller interacting constraint set
   within the shared effort budget.
6. Continue the walk-back until every relaxed constraint is restored or
   explicitly unresolved.

## Result and map-back

Return the skeleton, stripping order, skeleton result, restoration record, and
the mapped-back candidate solution. Verify it against `P`, every fixed fact and
constraint, and the original observable success criteria. Reject a candidate
that violates them; name any unresolved gap.

At this checkpoint, report definition status separately from resolution status
using the shared contract. Link evidence and gaps to the original criterion
IDs; distinguish supplied evidence, executed checks and observed results,
derived conclusions, and proposed checks. A proposed check is not passing
evidence. Preserve OPEN/ASSUMED owners and questions. An incomplete map-back
can return useful partial progress with its outstanding obligations and
remaining effort; success on a subproblem is not VERIFIED for the whole `P`.

## Failure modes

- Stopping at the toy skeleton instead of completing the map back.
- Treating a trivial skeleton as an error rather than a diagnostic waypoint.
- Restoring several constraints together and losing the first source of
  renewed difficulty.
- Treating the last-restored constraint as a sole cause when the difficulty
  depends on its interaction with the active set.
- Silently dropping a fixed fact or unresolved constraint.
