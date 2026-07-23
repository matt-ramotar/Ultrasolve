---
name: decompose
description: "Use when invoked directly or selected by the router because a problem needs answerable seams, ordered partial results, and explicit recomposition."
---

# Decompose

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

Shannon-derived core: build a path through a hard problem using subsidiary
partial results. Authored extensions: candidate and rejected seams,
answerability tests, information-yield ordering, and a recomposition check.

## Entry contract

Before transforming anything:

1. State the original problem `P` in one paragraph.
2. State observable success criteria for the solution.
3. List fixed facts and constraints that may not be silently changed.
4. Identify and gather missing domain facts that could change the route or
   answer.

## Cheap candidate route

Generate more than one candidate seam, such as stage, constraint, risk,
reversibility, or uncertainty. Compare them briefly, then select the strongest
seam and record why plausible alternatives were rejected.

## Full method

1. Turn the chosen seam into pieces expressed as answerable questions with
   observable outputs.
2. Record dependencies and cross-cutting constraints for each piece.
3. Order the questions by information yield and dependency, not ease alone.
4. Solve or investigate the pieces, banking partial results and updating later
   questions when new information changes them.
5. Recompose the partial results into a candidate whole.
6. Test the composition, especially constraints that live between pieces.

## Result and map-back

Return the candidate seams, selected and rejected reasons, ordered questions,
observable outputs, dependencies, partial results, and recomposed candidate.
Map the composition back to `P` and verify fixed facts, cross-cutting
constraints, and the original observable success criteria. Reject a
composition whose pieces pass individually but fail together.

## Failure modes

- Cutting by org chart or file layout without showing that the seam carries
  the difficulty.
- Generating only one seam and treating it as inevitable.
- Producing smaller vague tasks instead of answerable questions.
- Skipping recomposition or cross-cutting constraint checks.
