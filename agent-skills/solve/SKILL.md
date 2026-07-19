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

- If the problem is underspecified, undefined, or open-ended, use a
  brainstorming workflow when available; otherwise define or clarify it
  locally before continuing.
- If missing facts could change the route or answer, use research tools when
  available; otherwise ask the user for the missing facts before
  transforming the problem.
- If a reproducible failure has an evidence trail, use evidence-led diagnosis
  when available; otherwise perform a local evidence-led diagnosis through
  observation, reproduction, isolation, and verification. Inversion may
  generate bounded hypotheses within that process, but does not replace it.
- Do not invoke this workflow merely because work is difficult or one direct
  attempt failed. Use it when the problem is well-defined and the current mode
  of attack is genuinely stuck.

## Router workflow

1. **Integrity preflight.** Derive the collection root from the location of
   this loaded `SKILL.md`; it is the parent of the `solve` directory. Verify
   that all seven canonical `SKILL.md` files—the router and all six leaves—exist
   and are accessible and readable. Verify that all three required references
   exist and are accessible and readable:
   `references/technique-selection.md`,
   `references/shannon-source-notes.md`, and
   `references/worked-examples.md`. This preflight includes non-selected
   leaves. If anything fails the preflight, stop with one explicit
   collection-integrity error that names all missing or inaccessible resources;
   do this before executing or applying any lens to an incomplete collection.
2. **State.** Write the original problem `P` in one paragraph. Define
   observable success criteria for a solution `S`. List fixed facts and
   constraints that may not be silently changed. Identify missing domain facts
   that could alter the route or answer, and gather them before transforming
   the problem.
3. **Diagnose.** Internally consider all six lenses using
   [technique selection](references/technique-selection.md). Select one
   to three strong matches. Do not print a six-row ritual. Mention a rejected
   lens only when it was close or its rejection materially explains the
   choice.
4. **Load.** Use the host-native skill loader when available; otherwise read
   the selected sibling `SKILL.md` directly. Load every selected leaf's full
   instructions before applying it. This router's summary is not a substitute
   for the leaf method.
5. **Propose.** Produce one cheap, lens-appropriate artifact per selected
   lens: for example a stripped skeleton, analogy candidate set, set of
   restatements, broader principle, seam set, or backward hypothesis graph.
   The loaded leaf governs candidate multiplicity within its artifact. Do not
   force every lens into a universal `P′` shape, and do not treat an artifact
   as a solution.
6. **Select and execute.** Choose the candidate most likely to unlock `P`,
   explain the choice briefly, and run that leaf's full method, including its
   required fact checks.
7. **Map back and verify.** Mandatory: translate the result into a proposed
   solution `S` for the original `P`; restore or resolve every relaxed
   constraint; verify `S` against the original success criteria, fixed facts,
   and constraints; name any remaining gaps. Work on a transformed problem is
   not complete until this passes.
8. **Iterate deliberately.** If still stuck, record what the attempt taught
   and either choose a different lens or gather new information. Never repeat
   an unchanged lens without new information.

## Sibling leaf paths

Resolve these paths from the `solve` directory after deriving and checking the
collection root. Load only the leaves selected during diagnosis.

| Lens | Portable sibling instructions |
|---|---|
| Simplify | Load `../simplify/SKILL.md` |
| Analogize | Load `../analogize/SKILL.md` |
| Restate | Load `../restate/SKILL.md` |
| Generalize | Load `../generalize/SKILL.md` |
| Decompose | Load `../decompose/SKILL.md` |
| Invert | Load `../invert/SKILL.md` |

Use [worked examples](references/worked-examples.md) only when a compact
example would clarify a selected leaf; they do not replace its instructions.
