---
name: analogize
description: "Use when invoked directly or selected by the router because a stuck problem has the abstract shape of a solved problem in another domain."
---

# Analogize

## Direct-invocation boundaries

- If the problem is open-ended, underspecified, or undefined, use
  brainstorming when available; otherwise define or clarify it locally.
- If missing facts could change the route or answer, use research tools when
  available; otherwise ask the user for the missing facts.
- If a reproducible failure has an evidence trail, return to evidence-led
  diagnosis when available; otherwise perform it locally. This leaf provides
  only bounded transformation support inside diagnosis and does not replace it.

## Provenance: source and authored extensions

Shannon-derived core: use a solved `(P′, S′)` pair and replace one large
jump with two smaller analogical jumps. Authored extensions: requiring at
least two candidates, source-domain fact verification, a mapping table, and a
break-point audit.

## Entry contract

Before transforming anything:

1. State the original problem `P` in one paragraph.
2. State observable success criteria for the solution.
3. List fixed facts and constraints that may not be silently changed.
4. Identify and gather missing domain facts that could change the route or
   answer.

## Cheap candidate route

Name the abstract shape of `P` without target-domain nouns. Produce at least
two candidate analogies before selecting one, and give one sentence for the
mechanic each candidate might transfer.

## Full method

1. Compare the candidate analogies for structural fit, evidence quality, and
   likely break points; then select one.
2. Verify the source-domain facts that license the selected analogy before
   relying on them.
3. Build a mapping table with source entity or mechanic, target counterpart,
   evidence, and mismatch columns.
4. Port only the source solution mechanics licensed by mapped structure.
5. List every material break and turn each break into a decision, limit, or
   failure condition for the target design.

For packet scheduling, do not describe packets as preemptible. Canonical deficit
round robin visits active flow queues round-robin, dequeues whole packets FIFO
within each per-flow queue, and sends the head packet only when its complete
size fits the current deficit. Residual deficit carries across rounds only
while a queue remains backlogged; an empty queue resets its deficit to zero.
DRR does not provide global FIFO or preempt an in-flight packet. CI breaks
include unknown job size, long non-preemptive runner occupancy, parallel
runners, and an undefined credit-charging rule.

## Result and map-back

Return the abstract shape, candidates considered, verified facts, mapping
table, ported mechanics, and break decisions. Map the candidate solution back
to `P` and verify it against fixed facts, constraints, and the original
observable success criteria. Reject any transferred mechanic whose mapping or
fact check fails.

## Failure modes

- Selecting the first familiar analogy without comparing at least two.
- Porting vocabulary or conclusions that the mapping table does not license.
- Treating a source-domain claim as true without verification.
- Hiding breaks instead of making the resulting target decisions explicit.
