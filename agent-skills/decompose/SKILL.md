---
name: decompose
description: "Use when invoked directly or selected by the router because a problem needs answerable seams, ordered partial results, and explicit recomposition."
---

# Decompose

## Load and route

1. Read the full [shared workflow contract](../solve/references/workflow-contract.md).
   Resolve its path and the module path below relative to this entrypoint.
   Apply the shared authority, restriction, routing, status, and effort rules.
2. Check the direct-entry boundaries before transforming the problem:
   - An explicit applicable method request does not require repeated failure.
   - A felt difficulty that lacks a sufficient problem contract belongs in
     [define](../define/SKILL.md). An inherited contract with OPEN/ASSUMED items
     permits conditional exploration under the shared rules. Pure ideation
     with no felt problem belongs in available brainstorming, otherwise handle
     it locally.
   - A reproducible failure with an evidence trail belongs in evidence-led
     diagnosis, performed locally if no dedicated workflow is available.
     This method may provide bounded support inside that diagnosis.
3. Adopt an existing problem contract unchanged; otherwise establish the shared
   contract's fields. Preserve OPEN/ASSUMED questions and remaining effort.
   Gather accessible evidence without restarting a stakeholder interview;
   unavailable required evidence yields useful partial work or a precise blocker.
4. Read the complete [full decompose method](../solve/references/methods/decompose.md)
   before constructing any cheap candidate or applying a transformation.
   Follow that module and the shared contract through the map-back checkpoint.

Both required resources must load successfully. Report a missing or inaccessible
dependency as a collection-integrity error before applying the method. A denial
ends that path; do not retry through another loader, alias, or copy. The direct
entry uses the same method module as the router, and consumes the same remaining
full-method budget.
