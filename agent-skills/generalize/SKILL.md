---
name: generalize
description: "Use when invoked directly or selected by the router to broaden an already-found result or expose structure hidden by an awkward special case."
---

# Generalize

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

Shannon-derived core: result-first broadening of an already-found result or
principle to a larger statement or class. Modern authored extension:
structure-exposing parameterization of an awkward special case, followed by
instantiation back to the original. Do not attribute a claim that the `n` case
is easier than `2` to Shannon.

## Entry contract

Before transforming anything:

1. State the original problem `P` in one paragraph.
2. State observable success criteria for the solution.
3. List fixed facts and constraints that may not be silently changed.
4. Identify and gather missing domain facts that could change the route or
   answer.

## Cheap candidate transformations

Sketch both forms cheaply. First name an already-found related result or
principle to broaden. Then identify the awkward special-case axis to
parameterize. State what each transformation exposes, where it may fail, and
which is the stronger route for `P`.

## Full method

Produce and clearly label both forms:

1. **Shannon-derived, result-first broadening.** Start from a solved related
   result or principle. Ask whether a broader statement or larger class covers
   `P`; test that broader statement, then specialize it to `P`.
2. **Modern structure-exposing parameterization.** Turn the awkward special
   case into a parameter, derive the cleaner mechanism, then instantiate it
   back to the original values.

Compare the two forms, select the stronger one for deeper execution, and
retain the other as an explicit alternative or cross-check. Providing both
forms does not authorize shipping both abstractions.

In either form, preserve the entry contract, identify where the broader claim
stops applying, and separate thinking machinery from shipped scope.

## Result and map-back

Return both labeled forms, their comparison, the selected primary route, its
generalized statement or parameterized mechanism, applicability limits, and
concrete instantiation. Map it back to `P` and verify fixed facts, constraints,
and the original observable success criteria.
Apply the YAGNI guard: reject unrequested general infrastructure and ship only
what the instantiated solution requires.

## Failure modes

- Omitting either the already-found result or the specific awkward axis.
- Presenting modern parameterization as a claim made by Shannon.
- Solving a broad abstraction without instantiating it back.
- Shipping flexibility that the original problem and success criteria do not
  require.
