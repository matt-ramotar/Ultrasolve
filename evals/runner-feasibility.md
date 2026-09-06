# Runner feasibility and evidence status

Inspected locally on 6 September 2026 against the working revision based on
`a2dcdd9d82653904c98f465fdf4cf06be5e248d6`, version `0.2.0`.
This record separates observed command results, capabilities described by
help, and untested behavior. It covers the local free-revision checkpoint.
Subsequent PR and CI evidence belongs to the corresponding commit and hosted
run. Raw logs remain outside the checkout in the revision evidence directory
identified in the task report.

## Checkpoint evidence states

| Milestone | State and scope |
|---|---|
| FREE-REVISION-READY | Passed locally. T0–T10 source, test, review, and runtime artifact requirements complete |
| HOST-BEHAVIOR-VERIFIED — Claude Code 2.1.220 | Unverified. Packaging and inventory checks only |
| HOST-BEHAVIOR-VERIFIED — Codex CLI 0.149.0 | Unverified. Version and help inspection only |
| EFFECTIVENESS-MEASURED | Unperformed. No subject or judge runs, task scores, or uplift measurement |
| Hosted CI for this revision | Unperformed. A local workflow file is not a hosted run |
| Fresh personal installation | Unperformed. No configuration root or installed cache was changed |

## Local revision verification

The corrected `python3 tools/check.py` passed all 129 tests in six modules
on local Python 3.9.6, with zero failures, errors, skips, or expected failures.
The test and tool sources remained unchanged during that final aggregate.
An earlier run from outside the checkout confirmed working-directory
independence. Eight separate synthetic checker guards cover failure reporting,
missing modules, empty discovery, and rejection of expected failures.

All 57 original test obligations have a recorded disposition. Both v1 trees
retain their exact 86-file inventory and byte hashes. The new v2 assets contain
64 authored cases, 299 source-mapped invariants, 419 required outcome criteria,
and six authored calibration answers. These are prepared evaluation material,
not observed model scores. The 42-file runtime artifact is recorded below.

Specification and technical reviews resolved the material findings. The host
rejected additional fresh agents at its worker limit, so existing workers
reviewed other owners' work and the orchestrator reviewed their implementations.
The external receipts identify each review's authorship boundary. No review of
an author's own work is presented as independent evidence.

The CI workflow targets Linux and macOS with Python 3.11. Local Python 3.9.6
results do not establish Python 3.11 or hosted CI success. At the free revision
checkpoint, changes were local and uncommitted. Subsequent commit and PR
publication were separately authorized. Version `0.2.0` and the plugin release
hold remain preserved.

## Observed read-only checks

All commands below exited zero. Claude reported `2.1.220 (Claude Code)`.
Codex reported `codex-cli 0.149.0`, with a warning that PATH aliases could not
be created because the operation was not permitted. The warning was retained.
It did not prevent version or help output. No broader capability was inferred
from the exit code.

```sh
claude --version
claude --help
claude plugin eval --help
claude plugin validate .claude-plugin/marketplace.json --strict
claude plugin validate .claude-plugin/plugin.json --strict
claude --plugin-dir . plugin details ultrasolve
codex --version
codex plugin --help
codex exec --help
```

Claude strict validation accepted both manifests. Its inline plugin inventory
reported version `0.2.0`, exactly eight skills, and zero agents, hooks, MCP
servers, or LSP servers. The two automatic/six manual policies are checked in
source. This inventory output does not independently prove enforcement.
Its projected token counts are estimates for discovered components, not a
measurement of complete canonical-reference loading or end-to-end method cost.

## Capabilities described by the installed interfaces

These are help-advertised interfaces. None was used to launch a subject or
judge during this revision.

| Requirement | Claude Code 2.1.220 | Codex CLI 0.149.0 |
|---|---|---|
| Independent fixture and runtime roots | Native `plugin eval` accepts one target and discovers `evals/**` under it. Separate fixture-source and loaded-runtime roots are not exposed by the inspected help. | `exec` accepts a prompt and working directory. Inspected plugin help has no native evaluator interface. A two-root evaluation runner has not been established. |
| Filesystem read isolation | Tool grants and permission options are advertised. Their ability to prevent every access path to the source/evaluator tree has not been established. Loading a separate plugin directory is not that proof. | `--sandbox` selects a policy for model-generated shell commands. `--cd` selects a working root and `--add-dir` adds writable roots. These descriptions do not establish that the original checkout and evaluator material are unreadable. |
| Full trace | `plugin eval --verbose` streams a trace. `--json` describes prompts, graders, and per-run scores. Complete raw tool-event retention and ordering across failures remain unverified. General print mode advertises `stream-json`. | `exec --json` advertises JSONL events. Completeness, tool ordering, and retention across failures remain unverified. |
| Model pinning | Native eval exposes `--model` and `--judge-model`. General help accepts full model names. Acceptance and immutability of selected version-specific subject/judge IDs must be verified for an authorized run. | `exec --model` accepts a model identifier. No judge interface is established. Acceptance and immutability of a specific version remain unverified. |
| Cost limits | Native eval exposes `--max-cost-usd`, but its help bounds overrun to one agent run and skips paid graders after a breach. General print mode advertises `--max-budget-usd`. Neither was exercised. | Inspected `exec` help exposes no monetary ceiling. A supported enforceable budget for an evaluation runner remains unavailable. |
| Failure reporting | Eval help advertises exit 1 below a score threshold and exit 2 for cost-cap abort, with partial results. Timeout/error trace completeness remains unverified. | No evaluation-specific failure/abort contract is exposed by inspected help. Ordinary process exit and JSONL output are insufficient evidence of such a contract. |
| Does starting a run spend resources? | Native eval describes agent runs and paid graders. Treat invocation as spend-bearing, including a diagnostic probe. Help and validation used here start no agent. | `exec` starts a model task. Treat it as spend-bearing under the account's provider or usage terms. Help/version inspection starts no task. |

No absent flag is invented, and no alternative loader or copied instruction
is used to bypass a denial. A help omission is a limit of this inspected
interface, not a claim about every possible host API.

## Runtime bundle boundary

The final local artifact contains exactly 42 allowlisted runtime files,
144,688 bytes, each independently compared with the source and its external
manifest. Its content SHA-256 is
`a88dd01ba04b691ee1022d0932cd26aadf1a045bfed6a6b20fe3dfe315f24b8a`.
The builder validated dependency closure. The orchestrator independently
verified the inventory, bytes, per-file hashes, aggregate identity, and
development-file exclusions. This establishes bundle composition. It does
not establish subject-agent filesystem isolation. An agent may still reach the original
checkout through another path unless a supported execution boundary prevents
that access.

The original v1 recipe excluded only `evals/`. Plans, tests, and other answer
material could remain available. It is not the isolation proof for this
revision. The new builder excludes all those development surfaces, but a
separate read boundary is still required. No new runner is implemented here.

## Conditional next phase

T11 remains unperformed. It needs both a verified supported execution boundary
and explicit authorization for the subject/judge budget. Before any run,
record exact models, immutable fixtures and plugin bytes, required arms and
repetitions, permissions, trace retention, failure criteria, and monetary
limits with their overrun behavior. Validate that the subject cannot read
evaluator material or the source checkout through any permitted capability.

Then calibrate graders against the authored v2 answers, run a bounded pilot,
and compare equivalent substantive inputs with and without the plugin.
Report invocation, method compliance, outcome correctness, utility, latency,
and cost separately. Authored calibration expectations and local structural
checks are not measurements of model behavior or effectiveness.
