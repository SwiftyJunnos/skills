---
name: engineering-principles
description: "Engineering decision rules for repeated failed fixes, domain-state design, retryable operations, concurrent writes, test review, performance claims, and staged migrations."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/main/pstack"
  upstream-revision: "2776ddd2355d6d6c8747d3964600f28daf62f049"
---

# Engineering principles

Select the rule that changes the current decision. Read its linked reference when using the detailed method; keep unrelated references unloaded. Explain the resulting choice and its evidence, rather than listing principles in every reply.

The imported references retain pstack's wording. Apply them within these local limits:

- Preserve the requested outcome, assigned scope, checkout ownership, and compatibility commitments. Report related faults outside that scope separately.
- Follow the environment's authorization and tool rules for history changes, remote writes, destructive work, and delegation. A reference is not permission to perform them.
- Verify ordinary work in small passing units. Temporary breakage belongs only inside an explicitly planned, isolated migration stage with a named verification boundary. Branch updates and rebases are separate decisions.
- Use existing checks and tools first. Add a script, test, prototype, or delegate only when it improves the task's evidence or execution enough to justify its cost.

## Decision rules

| Trigger | Decision | Detail |
|---|---|---|
| Two fixes sharing one premise fail the same check | Write the shared premise and test an observation that could disprove it before another fix. | [Attack the premise](references/principles/attack-the-premise.md) |
| The same correction recurs | Encode it in types, a lint, metadata, or CI. Keep judgment-only guidance with a concrete failure example. | [Encode lessons in structure](references/principles/encode-lessons-in-structure.md) |
| State is spread across booleans or repeated branches | Choose a state machine, tagged type, registry, or other structure that expresses valid states and ownership. | [Model the domain](references/principles/model-the-domain.md) |
| External data enters the system | Parse it into domain types at the trust boundary. Recheck conditions that can change later, such as permissions, persisted state, and concurrent ownership. | [Boundary discipline](references/principles/boundary-discipline.md) |
| Primitive values have distinct meanings, or a schema owns the shape | Give semantic values distinct types and derive shapes from the authoritative schema. | [Type system discipline](references/principles/type-system-discipline.md) |
| A state-changing operation can retry or resume | Check repeated and interrupted runs. Reconcile from actual state; use transaction or idempotency guarantees for external effects rather than a racy read-then-write check. | [Make operations idempotent](references/principles/make-operations-idempotent.md) |
| Independent actors write shared state | Prefer owned output files, keys, or branches and combine results when reading. Serialize access when one canonical mutable object is necessary. | [Separate before serializing](references/principles/separate-before-serializing-shared-state.md) |
| Writing or reviewing a needed test | Assert the user's contract, including externally visible effects. The test should catch broken behavior and survive internal restructuring. | [Test behavior](references/principles/test-behavior-not-implementation.md) |
| Reporting or acting on a measurement | Establish the decision the measurement informs; report run count, spread, and an observed limiter. Rule out errors, skipped work, and irrelevant micro-results. | [Explain the number](references/principles/explain-the-number.md) |
| A change spans multiple verifiable units | Check each unit before building on it. Order commits or PRs to show the evidence; retain the existing checkout and history unless a separate change is authorized. | [Sequence verifiable units](references/principles/sequence-verifiable-units.md) |

## Other decisions

For simplification, foundational design, UX tradeoffs, root-cause fixes, API replacement, planned rewrites, automation, competing prototypes, context pressure, or execution autonomy, select the matching row in [application conditions](references/application.md). Read only that row's source. Existing project rules and specialist skills remain the source of their own workflows.

For actual performance comparisons, use the included [benchmark checklist](references/benchmark-checklist.md). For TypeScript syntax, consult the included [TypeScript guidance](references/typescript-best-practices.md) and [its examples](references/patterns.md). Use platform-appropriate commands and the current environment's app, browser, and device tools.

## Source and maintenance

Adapted from Lauren Tan's pstack under the [MIT license](LICENSE). The 24 principle texts and their supporting references are pinned to the reviewed upstream revision in [sources.json](references/sources.json). Only their relative Markdown links are rewritten for this layout.

Treat upstream refreshes as reviewed imports: compare the pinned sources, retain these local application limits, and validate links before replacing content. No background updater is installed.

