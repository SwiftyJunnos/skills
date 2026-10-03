# STE-KO sentence rules for source-preserving edits

This is a compact local adaptation of the STE-KO specification and vocabulary
guide, not a copy of ASD-STE100 or a certification of STE-KO compliance.
Use upstream rule numbers when explaining a change. All rules are subject to
the preservation gates in SKILL.md.

Source: [SPEC.md](https://github.com/beamonic/ste-ko/blob/fd351fe1ec427b9d97292099b568767def9cb427/SPEC.md)
and [dictionary.md](https://github.com/beamonic/ste-ko/blob/fd351fe1ec427b9d97292099b568767def9cb427/dictionary.md),
STE-KO 0.5.0, revision `fd351fe1ec427b9d97292099b568767def9cb427`.
Copyright (c) 2026 Beamonic. The upstream MIT notice is in
[ste-ko-LICENSE.txt](ste-ko-LICENSE.txt). These links are attribution, not runtime
dependencies. The adaptation below is the local rule source for this skill.

## Words and noun phrases: 1.1-2.5

- Give each term one meaning and each object one consistent name. Keep precise
  technical terms and protected identifiers; explain a term only with an
  explanation already supported by the draft. Expand abbreviations once if
  their expansion is supplied; coding and UI may retain familiar abbreviations.
- Prefer familiar words with the same precision. Apply the vocabulary patterns
  below to their inflected forms in context. Preserve a technical or legal
  meaning that a suggested replacement would obscure.
- In technical and work prose, replace metaphors, idioms, and sound effects
  with their literal meaning when it is clear. Preserve an ambiguous metaphor
  and flag it rather than guessing. Genre exceptions are defined in SKILL.md.
- Use at most three consecutive nouns without a linking particle. Break longer
  chains at their meaning boundaries with particles or clauses. Keep at most
  two attributive clauses before one noun.
- Express actions as verbs. Remove empty support verbs and redundant formal
  nouns or suffixes only when their meaning is unchanged.

## Verbs and certainty: 3.1-3.7

- Prefer active clauses when the draft identifies the actor. Passive clauses
  remain valid when the actor is unknown, irrelevant, or the affected object is
  the topic. Unknown actors stay unknown; an editor does not invent one.
- Remove double passives and redundant causatives. Preserve real causation,
  delegation, tense, and aspect when they matter to the claim.
- Replace vague status verbs with the stated action and result. When the draft
  only says something was handled, retain that limited information.
- Distinguish confirmed facts, inference, and unverified information. Keep the
  original confidence level. Simplify repeated uncertainty markers only when
  the same uncertainty remains; `-일 수 있다` cannot become `-이다`.
- Simplify `-하도록 하다` when it is an empty promise. Preserve it when it
  describes real instruction, causation, or a condition enabling an action.

## Sentences and paragraphs: 4.1-4.8, 10.2, 10.11

An 어절 is one whitespace-separated unit. The limits are upper bounds, not
target lengths. Use the tighter applicable limit for each passage.

| Context | Sentence limit | Paragraph limit |
| --- | --- | --- |
| `문서`, explanatory prose | 25어절 | 6 sentences |
| `대화` | 25어절 | 4 sentences |
| `코딩` | 20어절 | 4 sentences |
| Procedure or safety passage in any surface | 20어절 | The surface's paragraph limit |
| `UI`, guidance or error sentence | 12어절 | 2 sentences |
| `UI`, label or heading | 5어절 | Not applicable |
| `UI`, button, tab, or menu label | 3어절 | Not applicable |

- Give a sentence one main proposition. Keep a condition with the action it
  controls. Split overloaded clauses while preserving causal and contrast
  relations; use at most three clauses connected by endings or commas.
- Keep subject and predicate close. Untangle double negation only when the
  resulting certainty and scope are identical.
- Use particles that identify the relationships. Keep natural Korean subject
  omission when the actor remains unambiguous.
- Keep one topic per paragraph. Prefer varied sentence lengths and avoid three
  consecutive identical endings where a natural alternative preserves meaning.
  This rhythm rule yields to clear steps, register, and the sentence limits.

## Procedures: 5.1-5.5

- Give each numbered step one action. Use numbers for order, bullets for peers.
- Preserve the instruction's force and register. Use a consistent direct
  instruction form; recommendations remain recommendations.
- Put the condition before its action. Keep exceptions with the relevant step.
- Retain or move an existing success check next to its step. If a check is absent,
  record the omission instead of inventing a command or expected output.

## Explanations and safety: 6.1-7.4

- Put an existing conclusion or current state within the first two sentences.
  Preserve reasoning needed to support it. Do not manufacture a conclusion.
- Keep facts, inference, and unknowns distinct. Keep units, reference times,
  measurement scope, comparison baselines, failures, and unfinished work.
  Use supplied values to clarify vague claims; missing values remain missing.
- Put existing warnings before the risky action, and arrange supplied information
  as risk, consequence, and avoidance. Preserve irreversibility statements.
- Write a confirmed hazard directly. A possible hazard remains possible:
  do not turn a deletion risk into a guaranteed event, increase a
  recommendation to an obligation, or add a recovery promise.
- Safety passages use complete sentences with no compression. Keep legal,
  medical, financial, privacy, and permission-related uncertainty intact.

## Punctuation: 8.1-8.5

- Prefer `3개에서 5개` over `3~5개` in Markdown prose. Retain the same endpoints,
  units, and inclusive or exclusive meaning. This is a formatting convention;
  renderer behavior is not universal. Protected literals stay unchanged.
- Unnest parentheses and overloaded comma chains. Replace a slash meaning
  `and` or `or` with the intended relationship only if it is unambiguous;
  preserve paths, ratios, and units.
- Finish a factual statement directly rather than trailing off with an ellipsis.
  Preserve deliberate voice in genres outside STE-KO's technical scope.

## Compression: 9.1-9.5

`표준` keeps complete sentences. `압축` also removes empty greetings,
self-narration, and repetition; clear fragments may replace prose.
`최소` may use familiar abbreviations and arrows for relationships already
explicit in the draft. Never compress a sentence merely to meet a limit.

Keep negation, exclusions, conditions, warnings, quantities, evidence, uncertainty,
failures, and identifiers. Restore `표준` for risky or irreversible actions,
medical/legal/financial/permission passages, risky multistep procedures,
ambiguous compression, or a reader who says the answer was unclear.
Compression cannot authorize longer noun chains or removal of distinct claims.

## Surface rules: 10.3-10.17

- `대화`: lead with the existing answer or uncertainty. Remove empty agreement
  and repetition of the previous turn. Keep one actual clarification at a time
  when composing the editor's own question. In the draft, preserve distinct
  unresolved questions instead of silently deleting them. Place an existing
  next action last; add none when the source provides none.
- `코딩`: retain what changed, why, exact locations, performed checks, skipped
  checks, failures, and remaining work. Report only source-supported results.
- `UI`: use a verb describing the supplied button action. Preserve the actual
  effect, permissions, and reversibility. Pair a supplied error cause with a
  supplied next action, without blaming the user. If the action is unknown,
  retain the label and mark it unresolved. Edit copy only; a length limit
  does not authorize redesigning the screen.
- Match structure and length to the material. Lists help independent items and
  sequences; tables help comparisons. Avoid ceremonial headings and repeating
  the same conclusion in an introduction, summary, and closing paragraph.

## Vocabulary patterns

These are sentence-level edit targets, not substring replacements. Matching
an expression once is enough to inspect it; no repetition threshold is needed.
Choose the listed alternative only when the grammatical and semantic relation
is the same. The list is deliberately compact rather than the full upstream
dictionary; it does not define an exhaustive approved vocabulary.

| Pattern | Preferred edit |
| --- | --- |
| `-에 대하-`, `-에 관하-` | Direct object or possessive relation: `-을/를`, `-의`. |
| `-에 있어-` | Actual place, context, or time: `-에서`, `-할 때`. |
| `-을 통하-` | Direct means `-으로/로`; preserve actual routes or intermediaries. |
| `-에 의하-` | Stated actor as subject; preserve cited authority such as `법에 따라`. |
| `-로 인하-`, `-함에 따라` | Preserve the stated causal or conditional relation explicitly. |
| `-와 관련하-`, `-와 관련되-` | State the relationship already present in the draft. |
| `-를 위하-` | Clear purpose clause `-하려고`, `-하도록`, without changing obligation. |
| `-에서의`, `-으로의`, `-에의`, `-간의` | Untangle the noun relationship with a particle or clause. |
| `-한 바 있다`, `-하는 바이다` | Direct verb with the same tense. |
| `-지 않으면 안 된다` | `-해야 한다` only when the obligation is equivalent. |
| `-에도 불구하고`, `-라 할지라도` | `-지만/는데도`, `-여도`, preserving contrast or concession. |
| `되어지다`, `보여지다`, `불려지다` | `되다`, `보이다`, `불리다`; similarly remove double passive in context. |
| `밝혀지다`, `이루어지다`, `만들어지다` | Valid single passives; assess actor clarity separately. |
| `처리되었습니다`, `반영되었습니다` | Use the stated action, target, and result; preserve unknown details. |
| `삭제를 진행하다`, `검증을 수행하다`, `점검을 실시하다` | `삭제하다`, `검증하다`, `점검하다`. |
| `-라는 결정을 내리다`, `-하고자 하다` | `-하기로 정하다`, `-하려 한다`. |
| `-하는 것이 가능하다/불가능하다` | `-할 수 있다/없다`. |
| `-할 필요가 있다`, `-하는 것이 좋다` | Preserve necessity or recommendation; never blindly replace with a command. |
| `-라고 할 수 있다`, `-라고 볼 수 있다`, `-인 것 같다` | Express the same degree of inference or possibility directly. |
| `-을 가지고 있다`, `-을 필요로 하다`, `-을 요하다` | `-이 있다`, `-이 필요하다`, when the same meaning survives. |
| `금일`, `익일`, `차주`, `소요되다`, `송부하다`, `상이하다` | `오늘`, `다음 날`, `다음 주`, `걸리다`, `보내다`, `다르다`. |
| `다양한`, `일부`, `대부분`, `조만간`, `최적화`, `정상입니다` | Use only supplied counts, dates, metrics, symptoms, or results; otherwise retain and note the gap. |
| Redundant `-적`, `-화`, `-성`, `-들` | Remove only if scope and precision stay the same. |
| `가용성`, `일관성`, `멱등성`, `캐시`, `토큰`, `커밋` | Preserve established technical terminology. |
| `데이타`, `메세지`, `컨텐츠`, `쓰레드`, `플래폼` | `데이터`, `메시지`, `콘텐츠`, `스레드`, `플랫폼`, except protected literals. |

## Integration exceptions

STE-KO supplies the sentence targets; unslop-kr supplies the editor's authority
and acceptance gates. This adaptation intentionally defaults compression to
`표준`, preserves source uncertainty and register, and treats missing information
as unresolved. It does not activate upstream persistent output styles, require
external vocabulary lookups, execute a linter, or adopt upstream examples that
introduce facts absent from their original sentences. Outside STE-KO's scope,
its clarity principles apply without genre conversion or a compliance claim.
