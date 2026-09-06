# Testing Ultrasolve

Version `0.3.0` separates free local verification from host behavior and
measured effectiveness. The publication hold remains. Checks do not authorize
a commit, push, release, marketplace publication, or personal installation.
Model evaluations require a supported isolation boundary and separately
authorized spending.

## One free check

From this checkout, run:

```sh
python3 tools/check.py
```

From outside the checkout, pass its absolute script path. The checker finds
the repository from its own location, runs the maintained unittest suite
sequentially, reports executed checks, and exits nonzero on failure. It makes
no host, model, installation, or network calls and does not retry failures.

The maintained suites cover:

- The exact eight public entries, four manifests, version parity, thin Claude
  wrapper targets, matching canonical descriptions, and two automatic/six
  manual activation policies.
- Shared resources, six canonical full method bodies, provenance, method
  obligations, and example evidence boundaries.
- Repository-wide maintained-text hygiene and local Markdown links, including
  both YAML suffixes. Runtime/public-document semantic checks are distinct
  from development plans, evaluator fixtures, and source-code hygiene.
- Temporary-copy mutations for wrong wrappers, policies, descriptions,
  versions, missing dependencies, duplicated bodies, and unsafe bundles.
  An unmodified copy must pass first. A harmless explanatory paraphrase must
  remain acceptable.
- The illustrative source-time freshness model, v2 evaluation structure and
  invariant coverage, and reproducible 42-file runtime bundle construction.

Literal file, identity, version, and flag checks protect interfaces. Source
instruction checks do not establish that a model follows those instructions.
The timing test verifies a model of the example, not a deployed cache.

To investigate a failure, run the relevant suite:

```sh
python3 -m unittest tests.test_plugin_contract -v
python3 -m unittest tests.test_portability_contract -v
python3 -m unittest tests.test_example_models -v
python3 -m unittest tests.test_contract_mutations -v
python3 -m unittest tests.test_evaluation_contract -v
python3 -m unittest tests.test_eval_bundle -v
```

Retain the first failing output, explain the correction, and rerun checks
affected by that correction. The free entrypoint runs the full suite. There
is no requirement to repeat every passing suite separately.

The CI workflow runs the same entrypoint on Linux and macOS with Python 3.11,
read-only repository permissions, and pinned official actions. A local pass
or workflow file does not prove a hosted CI run for this revision.

## Build a runtime evaluation artifact

The allowlist is [runtime-files.json](evals/runtime-files.json). It includes
four manifests, eight canonical entries, eight Codex metadata files, eight
Claude wrappers, six method modules, the shared workflow, five existing
references, privacy policy, and license. These are 42 exact paths, without globs.

Use fresh external paths for the output directory and manifest:

```sh
python3 tools/eval_bundle.py \
  --source /absolute/path/to/Ultrasolve \
  --output /external/new-runtime-directory \
  --manifest-output /external/new-runtime-manifest.json
```

The manifest must be outside both source and bundle. The builder rejects
unsafe destinations, missing dependencies, symlinks, traversal, duplicates,
and prohibited files. It preserves runtime bytes and emits sorted per-file
sizes and SHA-256 values, source revision and dirty state when available,
and an aggregate content hash independent of location or Git metadata.
Unknown metadata stays `unknown`. Rejected builds exit nonzero and do not
emit a completed manifest. Existing content is never deleted to force success.

The artifact excludes README, TESTING, plans/specs, tests, tools, evaluations,
results, and repository metadata. Generated artifacts and raw logs remain
outside the checkout.

**Bundle composition is not filesystem isolation.** A later subject must
also be unable to read evaluator material or the original checkout through
any other path. An eval-stripped copy, changed working directory, or tool
permission list alone does not establish that boundary. Do not run a subject
until a supported restriction mechanism and access evidence establish it.
Never work around a denied method, resource, or action.

## Read-only host packaging checks

When Claude Code is installed:

```sh
claude --version
claude plugin validate .claude-plugin/marketplace.json --strict
claude plugin validate .claude-plugin/plugin.json --strict
claude --plugin-dir . plugin details ultrasolve
claude plugin eval --help
```

The inventory should contain exactly eight skills and no duplicated command
collection, agents, hooks, MCP servers, or LSP servers. Strict validation
proves packaging. Inventory proves discovery. Neither proves that the router
loads its full modules in order or that the host enforces invocation policy.

Codex capability inspection uses `codex --version`, `codex plugin --help`,
and `codex exec --help`. Current observations, unsupported or unverified
requirements, and per-host statuses are recorded in
[runner feasibility](evals/runner-feasibility.md). Optional portable validators
and static analyzers supplement the free checks. Retain raw findings and
interpret their heuristics rather than treating scores as behavioral proof.

A fresh installation is a separate check with separate authority. This
revision changes neither personal configuration roots nor installed caches.
The runtime evaluation bundle is not a replacement distribution. Source/cache
parity from a prior installation is historical evidence for those exact bytes,
not proof that the current revision is installed.

## Historical and revised fixtures

Both [Claude-native v1 fixtures](evals/behavioral/v1/) and the
[portable v1 matrix](evals/portable/v1/activation-tests.md) remain byte-for-byte
unchanged. Their original prompts and graders preserve the historical
contract, including behavior revised here. They are not silently repurposed
as v2 or treated as current acceptance evidence.

The [v2 corpus](evals/portable/v2/cases.json) is provider-neutral. It contains
52 expanded routing/regression/integration cases plus twelve transfer cases,
with exact stimuli, multi-turn release observations, supplied facts, stable
invariants, and required outcome criteria. See its
[rubrics](evals/portable/v2/rubrics.md) and
[authored calibration answers](evals/portable/v2/grader-calibration.json).

Every original invariant must map to a required outcome criterion. Report
invocation compliance, method compliance, outcome correctness, and utility
separately. A label-perfect answer can fail an outcome constraint. A concise
answer can be correct without method terminology. Tests validate this corpus's
structure and coverage, not the semantic correctness of model answers.
Calibration labels are authored expectations until a real judge is tested.

Transfer cases are held out from the plugin's shipped examples. They are
public and are neither confidential nor guaranteed unseen in model training.
Their changed constraints must make copying an example's answer inadequate.

## Separately authorized behavioral protocol

No subject or judge run is part of free verification. Before T11:

1. Verify an actual supported runner with separate evaluator/runtime inputs
   and a filesystem boundary covering every permitted access path. Do not
   invent flags or change personal configuration roots to simulate isolation.
2. Obtain explicit subject/judge spending authorization and record the exact
   cap, including any advertised overrun behavior.
3. Freeze a run manifest: fixture version and hashes, runtime content hash,
   exact host version, version-specific subject and judge IDs, tools, arms,
   repetitions, time/turn/cost bounds, failure rules, and evidence paths.
4. Retain immutable stimuli, grader definitions and calibration expectations,
   full events with tool calls and order, raw answers, per-criterion judgments,
   complete/error/timeout/abort records, and all partial results.
5. Calibrate the judge, then run a one-repetition diagnostic pilot for each
   major family. A defective fixture receives a new version. Existing evidence
   is never overwritten.
6. Compare with-plugin and without-plugin arms using equivalent substantive
   input. Remove only invocation syntax where necessary, randomize order, and
   blind outcome grading when feasible. Set later caps from observed pilot
   cost plus explicit headroom and authorization.

Critical routing, authority, status, and denial cases require every mandatory
criterion for each required complete run under the approved manifest.
Skipped paid graders, interruption, timeout, or a cost-cap abort are partial
evidence. An aggregate score cannot replace complete-run accounting.

Report exact task coverage, overrides, latency, and cost alongside the four
criterion categories. Exact-prompt repeatability is not broad precision,
recall, reliability, or general effectiveness. Small samples stay qualified.

## Completion record

Track three independent milestones: `FREE-REVISION-READY`,
`HOST-BEHAVIOR-VERIFIED` for each named host/version, and
`EFFECTIVENESS-MEASURED` for the evaluated task set. One does not imply the
next. Keep the external evidence receipt and the runner-feasibility record
consistent with what actually ran, including unavailable capabilities and
unperformed hosted CI or installation checks.
