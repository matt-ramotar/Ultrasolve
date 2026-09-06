---
name: solve
description: "Use when a well-defined problem is genuinely stuck after reasoned attempts, such as recurring dead ends, constraints that defeat plausible designs, an unmanageable problem shape, or a clear outcome with no credible route. Not for ordinary difficult work, undefined ideation, or evidence-led diagnosis of a reproducible failure."
---

# Solve a Stuck Problem

Use a Shannon-inspired set of lenses to transform a genuinely stuck problem,
then map the result back to the original problem. The source ideas and the
collection's authored workflow are distinguished in
[Shannon source notes](references/shannon-source-notes.md); the router,
candidate comparison, and mandatory map-back are collection synthesis.

## Boundaries

Load the [shared workflow contract](references/workflow-contract.md) before
definition, candidate construction, or method execution. Its authority,
eligibility, inherited fields, evidence rules, statuses, and effort limit govern
this router and every method it composes.

- Work directly on ordinary well-scoped requests, including one failed attempt.
  Use solve for a defined problem with reasoned dead ends or no credible route.
- For a felt difficulty with an unsettled outcome or conflicting definitions,
  use the definition entry, preserving the authorized deliverable. Pure ideation
  without a felt problem belongs in available brainstorming or local ideation.
- An agreed operational problem and criteria suffice even when the higher-level
  business rationale is unknown. Do not demand a separate mandate or reopen an
  inherited definition merely because it carries OPEN or ASSUMED questions.
- A reproducible failure with evidence belongs in evidence-led diagnosis:
  observation, reproduction, isolation, and verification. A method may supply
  bounded support; it does not replace diagnosis.
- An explicit applicable leaf request uses that entry's shared contract and
  method directly; it need not satisfy automatic solve's stuckness trigger.
- If a handoff is declined, return its disposition and reason. Do not send the
  same unchanged problem back or reset routing history by reloading an entry.

User and host restrictions remain authoritative. If a method, resource, or action
is denied, end that path. Do not use aliases, copies, relocated instructions,
another loader, or an equivalent action to reproduce the prohibited operation.
Continue only independently useful work already authorized.

## Router workflow

1. **Integrity preflight.** Derive the collection root from the location of
   this loaded `SKILL.md`: the parent of the `solve` directory. Check all
   eighteen resources listed below for existence, accessibility, and
   readability, including unselected entries and modules. Use permitted
   accessibility checks without loading every unselected module into context.
   If any check fails, stop routing before any candidate or transformation and
   report one collection-integrity error listing all missing or inaccessible
   resources. If accessibility cannot be established, identify the unverified
   resources too; do not claim preflight passed or improvise their instructions.
   A denial ends the affected path.
2. **State or adopt.** Adopt an existing shared problem contract without
   reconstructing it. Preserve the original problem and identity, criterion IDs
   and acceptance parameters, fixed facts, constraints, non-goals, authorized
   work, unresolved questions with owners and marks, definition status, and
   remaining budget. Otherwise establish those fields proportionally using the
   shared contract. Non-goals remain constraints. Carried OPEN or ASSUMED
   stakeholder questions permit explicitly conditional exploration; they do not
   become confirmed through routing. Gather accessible evidence yourself and
   distinguish unknowns that block the selected claim from questions the
   investigation will answer. If required evidence is unavailable, preserve
   useful progress and identify the precise blocker. Keep contract revisions
   explicit and authorized; do not invent stakeholder facts or owners.
3. **Diagnose.** Internally consider all six lenses using
   [technique selection](references/technique-selection.md). Within the remaining
   effort, select one to three strong matches. Mention a rejected lens only when
   it was close or its rejection materially explains the choice. Do not print
   a six-row ritual or restart definition to obtain an unnecessary mandate.
4. **Load method modules.** Through a permitted file-reading capability, read
   every selected canonical module below in full before constructing its cheap
   candidate. These modules are the router's method library. Do not invoke
   public leaf commands or read their entrypoints as a loading fallback. A
   native command loader is unnecessary. Missing or denied module access ends
   that path; this summary is not a substitute for the module.
5. **Propose.** Produce one cheap, lens-appropriate artifact per selected
   lens: for example a stripped skeleton, analogy candidate set, set of
   restatements, broader principle, seam set, or backward hypothesis graph.
   Each module governs multiplicity and applicability within its artifact.
   Cheap comparisons do not execute full methods. Do not force every lens into
   a universal `P′` shape or call an exploratory artifact a solution.
6. **Select and execute.** Choose the candidate most likely to unlock `P`,
   explain the choice briefly, and execute one full method first, including its
   fact checks. Honor the user's existing effort bound. Otherwise allow two
   full-method attempts total for the same problem, with at most one additional
   attempt after the first. Record an attempt as consumed when full execution
   begins. Direct leaf executions and full methods on subproblems count toward
   this same total; handoffs, re-entry, new names, and changed lenses never reset
   it. A larger already-authorized bound is recorded, not repeatedly invented.
7. **Map-back checkpoint.** After every full execution, map its result back to
   the original problem, criterion IDs, facts, and constraints. Restore or resolve
   relaxed constraints; record evidence and remaining obligations. A checkpoint
   may be partial or unsuccessful. Preserve useful progress without claiming
   that a successful subproblem verifies the whole solution. Distinguish
   supplied evidence, executed checks and observed results, derived conclusions,
   and proposed checks for each criterion. A test plan is not an executed test.
8. **Continue or finish.** Another method may address a bounded remaining
   question after that checkpoint, within the same budget, without requiring the
   first method to solve the whole problem. Carry its progress, outstanding
   obligations, and unresolved marks forward. Do not repeat an unchanged lens
   without new information. Stop exploration when solved, infeasibility is
   established, required evidence is unavailable, effort is exhausted, or
   another attempt has no credible information gain. Exhaustion alone does not
   prove infeasibility and does not trigger a routine permission question.
   Return the best supported result and next discriminating step; continue
   independently useful work already authorized.

## Required resources

The eighteen-resource preflight covers:

| Resource group | Exact paths |
|---|---|
| Eight entries, relative to the collection root | `define/SKILL.md`, `solve/SKILL.md`, `simplify/SKILL.md`, `analogize/SKILL.md`, `restate/SKILL.md`, `generalize/SKILL.md`, `decompose/SKILL.md`, `invert/SKILL.md` |
| Four references, relative to the solve directory | `references/workflow-contract.md`, `references/technique-selection.md`, `references/shannon-source-notes.md`, `references/worked-examples.md` |
| Six modules, relative to the solve directory | All six paths in the method table below |

## Canonical method modules

Resolve these paths from the loaded `solve` directory. Read selected modules in
full before their candidates; entrypoint preflight is not method dispatch.

| Lens | Module |
|---|---|
| Simplify | [Simplify](references/methods/simplify.md) |
| Analogize | [Analogize](references/methods/analogize.md) |
| Restate | [Restate](references/methods/restate.md) |
| Generalize | [Generalize](references/methods/generalize.md) |
| Decompose | [Decompose](references/methods/decompose.md) |
| Invert | [Invert](references/methods/invert.md) |

Use [worked examples](references/worked-examples.md) only when a compact
example clarifies a selected method; they do not replace its instructions.

## Result and evidence

Return the original problem, selected move, candidate or useful progress,
criterion evidence and gaps, effort consumed and remaining, and the next useful
step. Keep definition status (`CONFIRMED` or `DRAFT`) separate from one resolution
status: `VERIFIED`, `CANDIDATE`, `PARTIAL`, `INFEASIBLE`, or `BLOCKED`, with the
evidence required by the shared contract. Preserve every OPEN/ASSUMED question
and owner. `definition: DRAFT; resolution: VERIFIED` is conditional technical
verification, not confirmation of the stakeholder outcome. Match validation to
the claim; a performance target is not a measurement. A bounded unresolved result
is useful work when its limitations and next discriminating observation are clear.
