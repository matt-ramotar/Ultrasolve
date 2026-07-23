# Testing Ultrasolve

Deterministic structural checks gate version `0.2.0`. Behavioral model
evaluations are stochastic evidence only and require separate approval because
they spend credits. Do not run a paid Claude or Codex behavioral evaluation as
part of this adaptation. No behavioral result is claimed for this revision.

Run commands from the repository root. Preserve the existing publication hold:
verification does not authorize a commit, push, tag, release, or public-
availability claim.

## Python contracts and file hygiene

Run both suites directly, then run discovery as the aggregate proof:

```sh
python3 -m unittest tests.test_plugin_contract -v
python3 -m unittest tests.test_portability_contract -v
python3 -m unittest discover -s tests -p 'test_*.py'
```

The contracts cover the definition entry and all seven routed methods,
provenance, logical safety, mandatory map-back, portable frontmatter, adapter
isolation, dual manifests, marketplace shape, documentation, native fixture
structure, provider-neutral activation, and recursive text-file hygiene. Every
command must exit zero.

## JSON and diff checks

Parse both plugin manifests and the repository marketplace, then inspect the
working diff:

```sh
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
git diff --check -- .
```

`git diff --check` checks diffs only. The unit suite's recursive file-hygiene
test is the proof for trailing whitespace and exact final newlines across
working-tree artifacts regardless of index state.

## Claude validation and runtime inventory

Claude Code 2.1.215 or newer is the development baseline:

```sh
claude --version
claude plugin validate .claude-plugin/marketplace.json --strict
claude plugin validate .claude-plugin/plugin.json --strict
claude --plugin-dir . plugin details ultrasolve
```

Strict validation must report valid marketplace and plugin manifests plus a
valid adapter. Runtime details must inventory exactly eight skills: two
model-invocable entries (`solve`, `define`) and six manual-only leaves, with no
root `skills/` directory or duplicate commands.

## Portable and Codex static analysis

Point the variables at the installed validator and plugin analyzer rather than
embedding a maintainer home directory:

```sh
: "${SKILL_VALIDATOR:?Set SKILL_VALIDATOR to skill-creator/scripts/quick_validate.py}"
for skill in agent-skills/*; do python3 "$SKILL_VALIDATOR" "$skill" || exit 1; done
: "${PLUGIN_EVAL_JS:?Set PLUGIN_EVAL_JS to plugin-eval.js}"
for skill in agent-skills/*; do node "$PLUGIN_EVAL_JS" analyze "$skill" --format json || exit 1; done
```

All eight portable skills must pass Agent Skills validation. Record static
analyzer findings per skill and resolve required fixes; do not treat advisory
suggestions as behavioral evidence.

## Isolated Codex marketplace installation

Use an empty home so installed state cannot come from a previous cache. The
checkout path is the marketplace source, and `HOME` remains unchanged:

```sh
export CODEX_HOME="$(mktemp -d /tmp/ultrasolve-codex-home.XXXXXX)"
codex plugin marketplace add "$(pwd)"
codex plugin add ultrasolve@matt-ramotar --json >"$CODEX_HOME/install.json"
codex plugin list --available --json >"$CODEX_HOME/plugin-list.json"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); p=[x for x in d["installed"] if x["pluginId"]=="ultrasolve@matt-ramotar"]; assert len(p)==1 and p[0]["installed"] and p[0]["enabled"] and p[0]["version"]=="0.2.0" and p[0]["installPolicy"]=="AVAILABLE" and p[0]["authPolicy"]=="ON_INSTALL"' "$CODEX_HOME/plugin-list.json"
```

Require the inventory to show `ultrasolve@matt-ramotar` installed and enabled
at version `0.2.0`. Verify the cached eight-skill inventory and policy, then
prove full source/cache parity:

```sh
export INSTALLED_ULTRASOLVE="$CODEX_HOME/plugins/cache/matt-ramotar/ultrasolve/0.2.0"
test "$(find "$INSTALLED_ULTRASOLVE/agent-skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')" = 8
test "$(rg -l '^  allow_implicit_invocation: true$' "$INSTALLED_ULTRASOLVE/agent-skills" | wc -l | tr -d ' ')" = 2
rg -q '^  allow_implicit_invocation: true$' "$INSTALLED_ULTRASOLVE/agent-skills/solve/agents/openai.yaml"
rg -q '^  allow_implicit_invocation: true$' "$INSTALLED_ULTRASOLVE/agent-skills/define/agents/openai.yaml"
test "$(rg -l '^  allow_implicit_invocation: false$' "$INSTALLED_ULTRASOLVE/agent-skills" | wc -l | tr -d ' ')" = 6
diff -ru --exclude .git . "$INSTALLED_ULTRASOLVE"
```

The local marketplace entry is a clean-room validation surface only. It does
not clear the name-screening hold or establish public availability.

## Provider-neutral activation matrix

The authored matrix lives at
[`evals/portable/v1/activation-tests.md`](evals/portable/v1/activation-tests.md).
It specifies reproducible stimuli and expected outcomes without assuming a
named provider, tool, command syntax, or grader implementation. It covers
automatic router activation, ordinary-work nonactivation, the debugging
boundary, explicit invocation of each leaf, router dispatch, and mandatory
map-back.

## Claude-native behavioral fixture contract

Claude-specific fixtures remain under [`evals/behavioral/v1/`](evals/behavioral/v1/).
Version `v1` becomes immutable once evidence is recorded. Any prompt, grader,
tool allowance, or criterion change after that creates `v2`; never rewrite an
evaluated fixture in place.

Thin Claude wrappers must read the canonical core, so every fixture that
invokes a skill permits `Read`. To keep the model from reading prompt or grader
answers, every behavioral run must use an eval-stripped copy. Prepare it and
prove the exclusion before any separately approved run:

```sh
export EVAL_PLUGIN_ROOT="$(mktemp -d /tmp/ultrasolve-eval-plugin.XXXXXX)"
rsync -a --delete --exclude .git/ --exclude evals/ ./ "$EVAL_PLUGIN_ROOT/"
test ! -e "$EVAL_PLUGIN_ROOT/evals"
claude plugin validate "$EVAL_PLUGIN_ROOT" --strict
```

Claude Code 2.1.215 currently blocks safe execution of that separation. Its
`claude plugin eval --help` interface exposes only one plugin target, coupling
fixture discovery to the loaded plugin root; it does not expose separate
fixture-source and loaded-plugin-root arguments. A zero-dollar probe reached
the installed early-access gate before case discovery, ran no agent, spent no
credits, and produced no behavioral result.

Targeting the source root would expose `evals/` to the agent, while targeting
the eval-stripped root would remove fixture discovery. Do not run either unsafe
substitute and do not invent unsupported flags. Paid execution is blocked until
an approved runner exposes a separate fixture source and an eval-stripped
loaded plugin root. Once that separation exists, use the immutable source-tree
fixture as evaluator input, load only `EVAL_PLUGIN_ROOT` for the agent, retain
the filesystem proof above, and apply the exact acceptance matrix below.
Existing Read-enabled router cases also retain native zero-call anti-leak
graders as defense in depth.

Each case stores an exact `prompt.md` and focused graders under `graders/`.
Prompt frontmatter records `max_turns`, `timeout_seconds`, and the smallest
allowed tool set. Every direct leaf case starts its prompt body with the
literal native command. Trace-sensitive cases use native checks when the
evaluator can decide deterministically and a focused trace grader only where
tool-versus-answer ordering requires semantic judgment.

The debugging-boundary prompt deliberately withholds decisive intermediate
values and source lines. Its graders require an evidence-gathering plan and
reject a specific root cause or fix presented as established before new
evidence isolates it.

## What an approved behavioral run may support

Five repetitions of the activation or nonactivation fixture measure
repeatability on those exact prompts; they do not establish general activation
precision or recall. Acceptance requires:

- `activation`: at least 4/5 complete with-plugin runs on the exact prompt;
- `nonactivation`: at least 4/5 complete runs in each required arm;
- every direct leaf and critical safety case: 3/3 complete runs;
- router Read/order, debugging safety, and map-back: every required criterion
  passes in 3/3 complete runs in every required arm.

A run is complete only when it has no error, timeout, interruption, or
cost-ceiling abort; no paid grader was skipped; and every required criterion
for that arm passes. The CLI aggregate threshold cannot enforce the required
count of wholly passing runs. Use per-run JSON and treat aggregate scores as a
convenience only. Behavioral results remain evidence-only for `0.2.0`.

| Case | Runs | Ablation | Complete-run claim rule |
| --- | ---: | --- | --- |
| `activation` | 5 | `with-without` | 4/5 with-plugin runs |
| `nonactivation` | 5 | `with-without` | 4/5 in each required arm |
| `router-read-order` | 3 | `none` | 3/3 |
| `define` | 3 | `none` | 3/3 |
| `define-activation` | 5 | `with-without` | 4/5 with-plugin runs |
| `define-nonactivation` | 5 | `with-without` | 4/5 in each required arm |
| `simplify` | 3 | `none` | 3/3 |
| `analogize` | 3 | `none` | 3/3 |
| `restate` | 3 | `none` | 3/3 |
| `generalize` | 3 | `none` | 3/3 |
| `decompose` | 3 | `none` | 3/3 |
| `invert` | 3 | `none` | 3/3 |
| `debugging-boundary` | 3 | `with-without` | 3/3 in each required arm |
| `map-back` | 3 | `none` | 3/3 |

## Required evidence bundle

No result exists, and no pass, failure, reliability, or uplift claim may be
made, until these artifacts are stored together:

- immutable prompt and grader copies;
- full machine-readable event streams with tool calls and ordering;
- raw model outputs and per-run, per-criterion grader results;
- plugin tree SHA and exact provider CLI version;
- agent-model and judge-model identifiers;
- exact command, run count, ablation mode, allowed tools, and cost ceiling;
- aggregate JSON, self-contained report, and partial results from any abort;
- proof that the loaded plugin copy had no `evals/` directory.

A cost-cap abort is partial evidence and cannot support a score claim.

## Separately approved paid-run protocol

Only after the safe runner boundary exists and spending is explicitly approved,
begin with a one-repetition pilot for every exact `v1` case and its tabled
ablation mode. Pin a full version-specific agent model ID and a distinct
Sonnet-tier-or-better judge model ID; do not use moving aliases. The pilot
ceiling is an authorization limit, not a cost estimate. Set each full-run cap
from measured pilot cost multiplied by planned repetitions plus explicit
headroom, and preserve the measurement and formula.

Store pilot and full runs under different immutable result paths. Record the
exact fixture version, model versions, CLI version, tool allowances, complete
table row, and separated source/loaded-root evidence. Apply the same exact-case
rules to a future provider-specific realization of the provider-neutral
activation matrix; do not infer broad reliability from these fixed prompts.

Do not execute any behavioral model evaluation without separate, explicit
approval to spend evaluation credits.
