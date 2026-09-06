# Ultrasolve

Ultrasolve provides eight Agent Skills for defining unsettled problems and
finding new approaches when a well-defined problem is stuck. They are `define`,
the `solve` router, and six reasoning methods.

Give `solve` a concrete problem and evidence that direct approaches failed:

> We need to merge two editing histories while preserving every edit and
> allowing either branch to be restored. Three designs failed: last-write-wins
> discards edits, flattening loses branch history, and copying snapshots breaks
> independent rollback. Find a credible approach and identify what still
> needs verification. No implementation is requested.

If the outcome is unsettled, start with `define`. If you already know
which method you want, invoke that method directly. Repeated failure is not a
prerequisite for an applicable explicit request.

```text
Problem: What is happening, and what needs to change?
Success: What observable result would satisfy the request?
Constraints: What must be preserved? What is outside scope?
Authority: What deliverable, decisions, and actions are already authorized?
Attempts: What have you tried, and why did it fail?
Evidence: What facts or checks are available? What remains unknown?
```

Missing acceptance details can remain explicit while supported conditional
work proceeds. A binding technology choice remains a constraint. Questioning
its effectiveness does not reopen that choice or
replace the artifact you requested. A reaffirmed request is carried forward.

## Choose an entry

| Entry | Use it for |
|---|---|
| `define` | A felt difficulty with an unsettled outcome or competing definitions |
| `solve` | A defined problem with reasoned dead ends or no credible route |
| `simplify` | Strip constraints to find an answerable skeleton, then restore every obligation and inspect interactions |
| `analogize` | Compare solved problems, verify their mechanics, and transfer only supported structure |
| `restate` | Compare materially different representations while preserving the original invariants |
| `generalize` | Broaden a supported result or parameterize a useful special case, then instantiate it back |
| `decompose` | Find answerable questions and check their recomposed result |
| `invert` | Reason backward from a concrete outcome, then validate the route forward |

Ordinary well-scoped work, including one failed attempt, proceeds directly.
Pure ideation belongs in available brainstorming or local ideation. A
reproducible failure with evidence belongs in evidence-led diagnosis.
Inversion can supply bounded hypotheses within that process. An agreed
operational problem does not need another interview merely because its
broader business rationale is unknown.

Definition normally starts with a compact provisional record and at most two
material unanswered questions. It expands when the problem or your requested
depth warrants it. Causal tables are useful only when a causal claim needs
examination.

## What a result means

Every method maps its result back to the original success criteria, fixed
facts, constraints, and non-goals. It preserves unresolved questions and
distinguishes supplied evidence, executed checks, deductions, and proposed
checks. A successful subproblem can support the next method without proving
the whole solution.

Results report two independent statuses. The definition is `CONFIRMED` or
`DRAFT`. Resolution is `VERIFIED`, `CANDIDATE`, `PARTIAL`, `INFEASIBLE`, or
`BLOCKED`. A verified result under a draft definition is explicitly conditional.
A proposed test is not a passing test, and failed search is not impossibility.

Your existing effort instructions take precedence. Otherwise, the workflow
compares one to three cheap candidates and permits two full method attempts
total for the same problem. Direct methods and subproblems share that budget.
At its limit, the result includes the best supported progress and next useful
check. Re-entry does not restart the count or create a routine approval gate.

## Install for Codex

Add an absolute path to this checkout as a local marketplace, then install the
plugin by its stable selector:

```sh
codex plugin marketplace add /absolute/path/to/Ultrasolve
codex plugin add ultrasolve@matt-ramotar
```

Start a new Codex task after installation so the eight `ultrasolve:<skill>`
entries are loaded. `ultrasolve:define` and `ultrasolve:solve` allow implicit
invocation. All six leaf skills are explicit-only. Installation changes host
configuration and is a separate user action. Version `0.3.0` remains under a
publication hold. Local verification does not establish public availability.

## Load for Claude Code

Point Claude Code at the plugin root:

```sh
claude --plugin-dir /absolute/path/to/Ultrasolve
```

The declared minimum is Claude Code 2.1.143. The development baseline is
2.1.215 or newer. Current local capability observations and their limits are
recorded in [runner feasibility](evals/runner-feasibility.md). Validate a local
checkout strictly before relying on its packaging:

```sh
claude plugin validate /absolute/path/to/Ultrasolve --strict
```

The eight commands are `/ultrasolve:define`, `/ultrasolve:solve`,
`/ultrasolve:simplify`, `/ultrasolve:analogize`, `/ultrasolve:restate`,
`/ultrasolve:generalize`, `/ultrasolve:decompose`, and `/ultrasolve:invert`.
Define and solve are available for automatic invocation. The six leaf wrappers
retain `disable-model-invocation: true` and are explicit-only commands.

The router composes the six canonical method reference modules as its own
method library. It does not invoke a disabled public command or use its
entrypoint as a fallback. Direct commands load the same method modules. A
denied method, resource, or action ends that path. Another loader, alias, or
copy cannot override the restriction.

## Install for a generic Agent Skills client

Install or copy the complete [agent-skills collection](agent-skills/) into
the client's supported collection location. Keep all eight sibling directories
and their references together. An isolated copied skill is incomplete.
Generic clients expose the bare skill names. Invocation-policy enforcement
depends on the client, so manual-only declarations may be advisory there.

Before routing, the instructions require checking eighteen resources: eight
entries, six method modules, and four router references. Accessibility checks
need not load every unselected method. A missing or inaccessible dependency
produces one collection error before transformation.

## Provenance and development

Claude Shannon's 1952 talk *Creative Thinking* supplies the six historical
method cores. The router, candidate comparison, mandatory map-back, authority
and uncertainty rules, effort bound, and validation controls are authored
extensions. Generalize's structure-exposing parameterization is also an
authored extension. The definition entry draws on Polya, Duncker, Keeney,
Chamberlin, and related sources. It has no Shannon core. The
[Shannon notes](agent-skills/solve/references/shannon-source-notes.md) and
[definition notes](agent-skills/define/references/problem-posing-sources.md)
separate historical ideas from authored procedures.

The runtime consists of static instructions and metadata. Python checks and
the evaluation bundle builder are development tools. They never auto-run in a
host session. See [privacy](PRIVACY.md) and [testing](TESTING.md).

```text
agent-skills/                         eight shared public entries
agent-skills/solve/references/        workflow, selection, sources, examples
agent-skills/solve/references/methods/ six canonical full methods
adapters/claude/skills/               thin Claude wrappers
.agents/plugins/marketplace.json     Codex marketplace manifest
.codex-plugin/plugin.json            Codex plugin manifest
.claude-plugin/                      Claude plugin and marketplace manifests
evals/behavioral/v1/                 unchanged historical Claude fixtures
evals/portable/v1/                   unchanged historical portable matrix
evals/portable/v2/                   revised cases, rubrics, calibration
tools/                              local checks and runtime bundle builder
```
