# Application conditions

These are conditional references, not additional mandatory phases. Use the matching row within the scope and authority defined in the parent [skill](../SKILL.md).

| Situation | Principle | Local application |
|---|---|---|
| Choosing between a small fix and another abstraction | [Laziness protocol](principles/laziness-protocol.md) | Reuse the existing minimal-change rule. Consolidate decisions when that removes actual duplicated policy. |
| Adding a capability on top of dead or redundant code | [Subtract before you add](principles/subtract-before-you-add.md) | Remove relevant dead weight within the assigned scope. Preserve compatibility and unrelated work. |
| Deciding whether work is done | [Prove it works](principles/prove-it-works.md) | Inspect the real behavior or artifact and state verification gaps. A new script is useful when rerunning the check adds value. |
| Code requires tracing layers or remembering hidden mutable state | [Minimize reader load](principles/minimize-reader-load.md) | Collapse pass-through layers and narrow state scope when the interface still preserves the needed decisions. Use existing codebase-design guidance for module design. |
| Choosing data structures or work order | [Foundational thinking](principles/foundational-thinking.md) | Establish the types and shared-state model needed by this task. Reuse existing CI and test infrastructure rather than introducing a new foundation phase by default. |
| Product or interface choices trade polish against implementation convenience | [Experience first](principles/experience-first.md) | Evaluate the experience of end users, callers, and maintainers. Keep the user's product scope and preferences. |
| A defect appears downstream of the first wrong decision | [Fix root causes](principles/fix-root-causes.md) | Distinguish legitimate error states from invalid states. Fix matching faults inside the owned scope and report other occurrences separately. The existing diagnosing-bugs skill owns the diagnosis workflow. |
| A new requirement exposes a structural mismatch | [Redesign from first principles](principles/redesign-from-first-principles.md) | Consider the design that would fit the requirement from the start, then deliver the smallest coherent in-scope change. A design question alone does not authorize a rewrite. |
| A planned rewrite has explicit verification boundaries | [Outcome-oriented execution](principles/outcome-oriented-execution.md) | Temporary breakage stays inside a named, isolated stage. Preserve live-service and mixed-version contracts; verify the whole stage before handoff. |
| Replacing an internal API with all callers under our control | [Migrate callers, then delete legacy APIs](principles/migrate-callers-then-delete-legacy-apis.md) | Coordinate callers and remove the old internal path together when compatibility users are absent. Public APIs, deployed clients, and independently released consumers need a migration strategy. |
| A task needs repeatable transformations or checkable evidence | [Build the lever](principles/build-the-lever.md) | Prefer the smallest useful existing tool or new script. Weigh creation and maintenance cost against reviewability; a nontrivial task does not automatically require a new file. |
| A consequential design has no established precedent | [Exhaust the design space](principles/exhaust-the-design-space.md) | Compare materially different candidates when the experiment can settle the decision. Set scope and cost to match the uncertainty. Routine changes need no prototype round. |
| Large outputs or repeated reads crowd the conversation | [Guard the context window](principles/guard-the-context-window.md) | Filter and bound source reads, keep paths and compact evidence, and summarize completed phases. Delegate only when useful and permitted by the current environment. |
| A reversible implementation choice is already authorized | [Never block on the human](principles/never-block-on-the-human.md) | Proceed and present a reviewable result. Retain user-defined stop points and existing approval requirements; execution autonomy does not expand the task. |

