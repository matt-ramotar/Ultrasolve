# Ultrasolve

A stuck problem has a specific shape. There is a well-defined problem `P`, a
solution `S` that would satisfy observable success criteria, and no credible
route from one to the other. More effort along the same route does not change
this. The route has to change. Ultrasolve is seven Agent Skills, a router and
six methods, for changing it deliberately.

In *Creative Thinking*, a 1952 Bell Laboratories talk, Claude Shannon described
the mental rut that keeps an experienced researcher circling one viewpoint, and
presented conscious aids for finding a fresh route. One aid came with a
diagram. When the jump from `P` to `S` is too large to make, find a similar
solved problem `P′` with a known solution `S′`, and replace the one large jump
with two smaller ones. Shannon drew that diagram for a single method (similar
known problems). Ultrasolve adopts it as the contract for all six methods in
the talk. Each method transforms the stuck problem into a problem that can be
solved, and each transformation owes a translation back:

- `simplify` deletes constraints until a solvable skeleton remains, then
  restores them one at a time. The restoration that brings the difficulty back
  locates the difficulty.
- `analogize` finds solved problems that share structure with the stuck one,
  verifies the mapping where the domains differ, and ports the solution
  across.
- `restate` rewrites the problem in materially different representations, with
  an invariant ledger to guarantee each rewrite is still the same problem.
- `generalize` broadens a result that already works, or lifts an awkward
  special case into a cleaner general form, then instantiates the answer back
  to the requested case.
- `decompose` replaces one large jump with a path of answerable intermediate
  questions and recomposes the partial results into a whole.
- `invert` assumes `S`, reasons backward toward the current state, then
  replays the route forward from the actual starting point. A route that only
  runs backward is a hypothesis.

A transformed problem is easier precisely because it is not the original
problem. That is the leverage, and it is also the risk. So every method ends
with the same obligation: restore or resolve everything that was relaxed, and
verify the result against the original success criteria, fixed facts, and
constraints. Until that map-back passes, a solution to the transformed problem
is a claim about the transformed problem, not about `P`.

The `solve` router enforces this contract end to end. It states `P`, the
success criteria, the fixed facts, and the missing facts worth gathering
first. It weighs all six transformations against the specific way the problem
is stuck, executes the strongest candidate in full, and treats no result as
complete until the map-back passes. Activation is deliberately narrow.
Ordinary difficulty, undefined problems, and reproducible failures with
evidence trails belong in other workflows, and the boundaries below keep them
there.

Version `0.1.0` keeps the method instructions in the shared `agent-skills/`
collection and exposes them through small host-specific adapters. Every host
uses the same methods. Where enforcement is supported, host metadata determines
whether a skill may run automatically or only when named.

## Install for Codex

Add an absolute path to this checkout as a local marketplace, then install the
plugin by its stable selector:

```sh
codex plugin marketplace add /absolute/path/to/plugins
codex plugin add ultrasolve@matt-ramotar
```

Start a new Codex task after installation so the seven
`ultrasolve:<skill>` entries are loaded. Only `ultrasolve:solve` allows
implicit invocation. All six leaf skills are explicit-only. Use this path to
test a fresh local installation while publication remains held.

## Load for Claude Code

Point Claude Code at the plugin root:

```sh
claude --plugin-dir /absolute/path/to/plugins/plugins/ultrasolve
```

Claude Code 2.1.143 is the minimum supported version. Development verification
uses Claude Code 2.1.215 or newer. Validate a local checkout strictly before
relying on it:

```sh
claude plugin validate /absolute/path/to/plugins/plugins/ultrasolve --strict
```

The adapter preserves these commands:

| Command | Purpose | Activation |
| --- | --- | --- |
| `/ultrasolve:solve` | Route a genuinely stuck problem through the full workflow | Explicit or automatic |
| `/ultrasolve:simplify` | Strip constraints, solve a skeleton, then restore them | Explicit or router-selected |
| `/ultrasolve:analogize` | Compare solved analogies and port verified structure | Explicit or router-selected |
| `/ultrasolve:restate` | Generate invariant-preserving reformulations | Explicit or router-selected |
| `/ultrasolve:generalize` | Broaden a solved result or expose cleaner structure | Explicit or router-selected |
| `/ultrasolve:decompose` | Find answerable seams and recompose partial results | Explicit or router-selected |
| `/ultrasolve:invert` | Build backward routes or hypotheses with forward validation | Explicit or router-selected |

Only `solve` is visible for automatic model invocation. The six leaf wrappers
retain `disable-model-invocation: true` and delegate to the shared method
instructions.

## Install for a generic Agent Skills client

Install or copy the complete [`agent-skills/`](agent-skills/) directory into
the client location for Agent Skills collections. Keep all seven sibling
directories together: `solve`, `simplify`, `analogize`, `restate`,
`generalize`, `decompose`, and `invert`. The router checks the collection before
dispatch because it may need any of the six leaf skills. An isolated copied
skill is incomplete.

Generic clients expose the bare skill names. `solve` is the automatic router.
The six leaf skills declare themselves manual-only, but clients without
invocation-policy enforcement may treat that declaration as advisory. Consult
that client's installation and discovery mechanism for the final filesystem
destination.

## Activation and workflow boundaries

Automatic activation is intentionally narrow. Use the router only when the
problem has a clear outcome and direct approaches keep failing. The evidence may
be recurring dead ends, constraints that defeat plausible designs, a problem too
entangled to attack directly, or no credible route. Ordinary difficult work and
one failed attempt are not enough.

- For an undefined or open-ended problem, use an available brainstorming
  workflow or define the problem locally first.
- When research tools are unavailable, ask for the missing facts that could
  change the route or answer.
- For a reproducible failure with evidence, return to evidence-led diagnosis.
  Inversion may generate bounded hypotheses inside that process. It does not
  replace observation, reproduction, isolation, or verification.

Every route must map its transformed result back to the original problem,
restore or resolve relaxed constraints, and test the result against the
original success criteria.

## Provenance

Claude Shannon's 1952 talk *Creative Thinking* provides the historical basis
for the six method cores: simplification with refinement, similar known
problems, reformulation, result-first broadening, structural analysis, and
inversion. Ultrasolve adds one entry format for the problem, success criteria,
fixed facts, constraints, and missing domain facts. It also adds the router,
candidate comparison, mandatory map-back, activation boundaries, constraint
ledgers, mapping audits, causal graphs, and other safety controls. The source
notes distinguish Shannon's ideas from these authored extensions.

## Layout

```text
agent-skills/                         shared instructions for all seven skills
agent-skills/solve/references/        shared method guidance and examples
adapters/claude/skills/               Claude adapters for the shared skills
.claude-plugin/plugin.json            Claude plugin manifest
.codex-plugin/plugin.json             Codex plugin manifest
evals/behavioral/v1/                  Claude-native behavioral fixtures
evals/portable/v1/                    provider-neutral activation matrix
README.md                             installation and supported interfaces
TESTING.md                            deterministic checks and evidence rules
```

See [TESTING.md](TESTING.md) for the full verification protocol.

