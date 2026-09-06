Ultrasolve revision contract — 6 September 2026

This document fixes the implementation choices for the parallel revision plan approved by the user on 6 September 2026. These choices are the frozen implementation baseline. They are product decisions for this revision, not empirically validated defaults or claims about host behavior.

Source baseline: `a2dcdd9d82653904c98f465fdf4cf06be5e248d6`, version `0.2.0`. The preceding review found twelve improvement areas. The companion plan contains their complete coverage map and execution assignments, so execution does not depend on access to the earlier conversation.

**D1 — Scope and architecture**

Keep the eight public skills: define, solve, simplify, analogize, restate, generalize, decompose, invert. Keep their namespaces, installation locations, and two automatic entries plus six manual commands. The revision changes their internal composition and instructions, examples, evaluation assets, and development checks. It adds no solver service, model client, runtime script, hook, ninth skill, or new permission grant.

Use one shared workflow reference at `agent-skills/solve/references/workflow-contract.md` and six canonical method modules under `agent-skills/solve/references/methods/`, named `simplify.md`, `analogize.md`, `restate.md`, `generalize.md`, `decompose.md`, and `invert.md`.

The six public leaf `SKILL.md` files retain portable name/description frontmatter. Their bodies become entry instructions that load the shared workflow reference, establish or adopt its contract, and load the corresponding full method module. They retain enough boundary guidance to route an inapplicable request before transforming it. There must be exactly one full implementation of each method, in its module.

The router reads the ordinary method modules as its own documented method library. It does not invoke public leaf commands and does not use a public leaf entrypoint as a fallback loader. The Claude wrappers continue to load their corresponding canonical entrypoints. Keep their current manual-invocation flags; Codex retains two true and six false implicit-invocation flags.

This architecture was selected over a smaller edit to the native-loader preference because it makes command policy and internal composition distinct. A runtime orchestrator or code-based solver would expand the product unnecessarily. Actual acceptance of the composed workflow by a host remains a runtime verification question.

**D2 — Restriction precedence and integrity**

User and host restrictions on methods, resources, actions, or decisions remain authoritative. A denied action or read terminates that path. Do not invoke an alias, move or copy the instructions, call another loader, or otherwise reproduce a prohibited operation after a denial. An invocation of this plugin does not grant authority to mutate a workspace or perform an external action beyond the user's request.

Retain the router's complete-collection preflight in this revision: eight canonical entrypoints, six canonical method modules, and four router references: workflow contract, technique selection, source notes, and worked examples. These are eighteen required resources. Report one error listing all missing or inaccessible resources before any transformation. Do not read every module into context merely to check accessibility.

A direct leaf must successfully load its own entrypoint, the shared workflow contract, and its selected module before applying the method. All supported installations still contain the complete collection. A missing required dependency is a collection error, not permission to improvise the missing method. Optimizing the full preflight or caching its outcome is deferred until actual loading costs are measured.

**D3 — Routing and eligibility**

| Situation | Required disposition |
|---|---|
| Ordinary well-scoped work, including a single failed attempt | Work directly; do not activate solve or manufacture a definition exercise |
| Felt difficulty with unsettled outcome or conflicting definitions | Define the problem proportionally |
| Pure ideation without a felt problem | Use available brainstorming, otherwise handle locally |
| Reproducible failure with an evidence trail | Evidence-led diagnosis; a lens may supply bounded support |
| Defined outcome, constraints, and repeated reasoned dead ends or no credible route | Solve |
| Explicit applicable leaf request | Load its shared contract and method directly; genuine stuckness is not an additional requirement |
| Already sufficient problem contract, business rationale unknown | Continue with the operational contract; do not require a separate mandate |

Apply this table consistently to define, solve, and every direct leaf. A method that declines a handoff returns a disposition and reason instead of sending the same unchanged problem back. Reaffirmation or reloading a skill does not reset the routing history.

**D4 — The shared problem contract**

The runtime contract is a readable record, not a new machine-enforced application state model. Preserve these fields through every handoff:

| Field | Meaning |
|---|---|
| Problem and identity | The original problem paragraph plus an identifier or unmistakable reference within the task |
| Success criteria | Observable criteria with stable local identifiers and the source or unresolved status of each acceptance parameter |
| Fixed facts | Supplied or observed facts, with evidence where available |
| Constraints and non-goals | Binding requirements and explicit excluded scope; non-goals remain constraints downstream |
| Authorized work | Requested deliverable, binding decisions, and the actions the user has delegated |
| Unresolved items | Exact question or unknown, owner when known, CONFIRMED/OPEN/ASSUMED mark, and why it matters |
| Definition status | CONFIRMED or DRAFT; any unresolved acceptance or mandate parameter keeps it DRAFT |
| Effort remaining | User budget or remaining default full-method attempts, plus attempts already consumed |

Do not invent an owner when none is supplied or recoverable. Preserve an unnamed owner as unknown and identify the question that establishes who can decide. Do not silently relabel an observation as a binding decision or a proposed mechanism as a fact about effectiveness.

Runtime wording to incorporate without changing its meaning:

> Adopt an existing problem contract without reconstructing it. Preserve its original problem, criteria, facts, constraints, non-goals, authorized work, unresolved items, and remaining budget. Carried OPEN or ASSUMED stakeholder questions permit explicitly conditional exploration; they never become confirmed because a method runs. Identify other unknowns that block the selected claim or action, and distinguish them from questions this investigation will answer. Gather accessible evidence yourself. If required evidence is unavailable, return a useful partial result or identify the precise blocker. Any revision to the contract is explicit, states its source or authority, and retains the prior obligations until they are deliberately changed.

A change of wording, selected lens, or problem identifier does not create a new budget. A genuine authorized scope revision records what changed and how much effort remains. Without authority to revise a binding constraint, retain it.

**D5 — Definition authority and proportionality**

Separate a decision's binding status from the hypothesis that it will achieve the desired outcome. A supplied binding implementation choice remains a constraint even when its effectiveness is uncertain. A proposal that is still open enters the comparison set. Determine decision scope from existing context before asking.

Preserve the authorized deliverable's supported portions and mark assumptions or conditional commitments. Define may recommend a different artifact; it must not unilaterally substitute it merely because success criteria remain unsettled. Producing a draft plan is distinct from authorizing implementation of that plan. Honor a reaffirmed request already present in the conversation. Challenge the same decision at most once unless material new evidence changes the concern.

Default to a compact provisional definition, ordinarily around 250 words, with at most two unanswered questions that materially affect the next step. This is a presentation target, not a reason to omit required facts or violate a user's requested depth. Expand for contested ownership, substantial interacting uncertainty, or an explicit deep-definition request. Do not require causal hypothesis tables when no causal claim is being assessed. Do not manufacture two questions when one or none is needed. Silence is not agreement.

Every new numeric threshold, observation horizon, or other acceptance parameter is supplied, derived with justification, or marked proposed and unresolved. No set of unrelated stakeholder answers silently confirms it.

Hypotheses may overlap unless exclusivity is justified. Support joint mechanisms and inconclusive evidence without exhaustively enumerating combinations. A deadline bounds the available work; it does not supply causal evidence or require an unsupported GO/NO-GO decision. Preserve the requested artifact and include an appropriate conditional or reversible next step.

**D6 — Result status and evidence**

Keep definition status independent of resolution status. Return one resolution status:

| Status | Required basis |
|---|---|
| VERIFIED | Evidence supports every original success criterion and constraint for the claimed result |
| CANDIDATE | A concrete proposed solution exists, but required validation has not occurred |
| PARTIAL | Useful progress exists, but no fully supported whole solution exists |
| INFEASIBLE | A contradiction or impossibility argument follows from the stated premises; failed search alone is insufficient |
| BLOCKED | A named unavailable input, capability, or authorization prevents the next necessary step, and no further useful work on that step is supported |

An output may be `definition: DRAFT; resolution: VERIFIED`, but must say that verification is conditional on the draft definition; it cannot claim the stakeholder outcome is settled. This avoids treating draft authority as either proof or disproof of technical correctness.

For each original criterion, distinguish supplied evidence, an executed check and observed result, a derived conclusion, and a proposed check. A test plan is not a test result. A benchmark target is not measured performance. Choose validation appropriate to the claim; a proof, simulation, test, and operational observation have different limits.

**D7 — Effort and method composition**

Honor the user's existing time, depth, cost, and scope instructions. Without a larger authorized effort, compare one to three cheap candidates, execute one full method, and permit at most one additional full-method attempt: two full attempts total for the same problem. This is the selected default for this plan, not a measured optimum. A direct leaf execution consumes one attempt; an internal full method on a subproblem also consumes an attempt. Handoffs, re-entry, and renamed candidates do not reset the count.

Do not turn reaching the default limit into a routine permission question. Return the best supported result and the next discriminating step. Continue independently useful work already authorized by the user. A larger effort is allowed when the user's request already supplies it; record the applicable bound. Do not self-extend the default repeatedly by declaring each new analogy promising.

At every completed full method, perform a map-back checkpoint. It may fail or return partial progress. Preserve its outstanding obligations before another method works on a bounded remaining problem. One method need not solve the whole problem before another can help; no intermediate artifact may be called a verified whole solution prematurely.

**D8 — Method-specific changes**

Preserve all six method cores and their useful constraints. Simplify records the active constraint set and qualifies order-dependent attribution; another restoration order or a smaller interacting set is appropriate when identifying a cause. Analogize retains source verification, mapping, break decisions, and its candidate comparison; move scheduling-specific facts to the existing analogy example, not a new generic requirement. Restate retains materially different representations, invariants, and explicit relaxations. Generalize assesses both forms but permits one to be inapplicable; never invent its missing prerequisite. Decompose retains answerable questions, dependencies, and whole-result recomposition. Invert retains alternative predecessors, necessity/sufficiency distinctions, and forward validation.

Apart from generalize applicability and proportional definition, do not change the current method-specific candidate minima in this revision. Measure their usefulness before broadening that change.

**D9 — Example corrections**

For the cache example, define a conservative source coverage time and clock-error bound before proposing a lease. A delayed watermark must not receive a new full lease at receipt. With coverage time 0 and a five-second bound in one established clock domain, receipt at 1.9 cannot move expiry beyond 5.0; a write at 0.1 cannot remain stale through 6.9. Account conservatively for clock uncertainty. If coverage time or a clock bound is unavailable, retain that as a design gap; do not assert the bound. A publisher stall stops coverage from advancing, but a region does not instantly know about unpublished commits. Replayed expired evidence cannot re-enable the cache. Keep percentile SLO claims separate from the conditional timing argument.

The define example's observation window remains an explicit unresolved decision until supported. Its old confirmation answers do not settle that window. Add same-symptom joint causes and an inconclusive-deadline disposition. Label fictional input, illustrative derived reasoning, and proposed checks clearly in all examples. Do not invent execution evidence.

**D10 — Development and evaluation boundaries**

Keep both v1 evaluation trees byte-for-byte unchanged. Author v2 as provider-neutral exact cases, rubric criteria, and calibration answers. Do not implement a speculative native evaluator adapter or a model client. Separate invocation compliance, method compliance, outcome correctness, and utility. Every original user invariant must map to an outcome criterion that does not require plugin terminology.

Build a byte-preserving evaluation runtime bundle from an explicit file allowlist. Include the four native/plugin marketplace manifests, eight canonical entries, eight Codex metadata files, eight Claude wrappers, six method modules, the shared contract, the five existing reference files, PRIVACY.md, and LICENSE: 42 files under this design. Exclude README.md, TESTING.md, plans/specs, tests, tooling, evals, results, and repository metadata. This is an evaluation artifact, not a replacement distribution or publishing design. Its content manifest lives outside the bundle.

Bundle composition is not filesystem isolation. A later subject agent must be unable to read evaluator material or the original checkout through any other path. Only a supported execution environment and access evidence can establish that boundary. No host denial may be bypassed. No model evaluation runs without the separate spending authorization required by TESTING.md.

Use standard-library Python and unittest for development tools. Runtime remains instruction files and metadata. Separate runtime/public-document semantic checks from repository-wide text hygiene and link checks; include both YAML suffixes. Do not let review prose or evaluator examples be interpreted as production skill instructions. Keep literal assertions for actual paths, identities, versions, and flags; do not present keyword presence as behavioral proof.

**D11 — Completion and deferrals**

Track three independent milestones: FREE-REVISION-READY, HOST-BEHAVIOR-VERIFIED for each named host/version, and EFFECTIVENESS-MEASURED for the evaluated task set. The first never implies the latter two. Record unavailable capabilities as unverified or unsupported, without failing unrelated free work or claiming runtime success.

Preserve version 0.2.0 and the publication hold during local revision. No commit, push, release, marketplace publication, name change, or personal installation is part of plan execution without separate authority. Defer additional lenses, a solver engine, general performance claims, preflight optimization, and a new evaluation runner until evidence or verified host capabilities justify a separate bounded task.
