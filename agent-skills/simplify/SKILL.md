---
name: simplify
description: "Use when invoked directly or selected by the router because interacting constraints and edge cases hide a problem's core difficulty."
---

# Simplify

## Direct-invocation boundaries

- If the problem is open-ended, underspecified, or undefined, use
  brainstorming when available; otherwise define or clarify it locally.
  When the collection is present, `../define/SKILL.md` performs that definition.
- If missing facts could change the route or answer, use research tools when
  available; otherwise ask the user for the missing facts.
- If a reproducible failure has an evidence trail, return to evidence-led
  diagnosis when available; otherwise perform it locally. This leaf provides
  only bounded transformation support inside diagnosis and does not replace it.

## Provenance: source and authored extensions

Shannon-derived core: strip inessential features, solve the simpler problem,
then add refinements toward the original. Authored extensions: the constraint
ledger, deliberate trivial skeleton, ordered restoration record, and mandatory
map back.

## Entry contract

Before transforming anything:

1. State the original problem `P` in one paragraph.
2. State observable success criteria for the solution.
3. List fixed facts and constraints that may not be silently changed.
4. Identify and gather missing domain facts that could change the route or
   answer.

Any constraint relaxed during this lens remains recorded for restoration.

## Cheap candidate transformation

List the relevant constraints, propose a stripping order, and show the first
one or two removals as a candidate skeleton. Prefer the order most likely to
expose which constraint carries the difficulty.

## Full method

1. Build a constraint ledger containing fixed facts, requirements, edge cases,
   and intentional relaxations.
2. Choose and record a stripping order.
3. Remove constraints in that order until the skeleton is answerable. A
   trivial skeleton is allowed and can be useful.
4. Solve or characterize the skeleton.
5. Restore constraints one at a time. Adapt the solution after each restore
   and record the first constraint that reintroduces the difficulty.
6. Continue the walk-back until every relaxed constraint is restored or
   explicitly unresolved.

## Result and map-back

Return the skeleton, stripping order, skeleton result, restoration record, and
the mapped-back candidate solution. Verify it against `P`, every fixed fact and
constraint, and the original observable success criteria. Reject a candidate
that violates them; name any unresolved gap.

## Failure modes

- Stopping at the toy skeleton instead of completing the map back.
- Treating a trivial skeleton as an error rather than a diagnostic waypoint.
- Restoring several constraints together and losing the first source of
  renewed difficulty.
- Silently dropping a fixed fact or unresolved constraint.
