---
name: before-and-after
description: Add screenshots or screen recordings to a GitHub pull request as a before/after or preview block. Use when a PR needs visual evidence. Browser capture runs through agent-device with --platform web.
---

# Add visual evidence to a PR

Use `agent-device --platform web` for capture and this skill's formatter for GitHub attachment markup. Keep every browser command on the `agent-device` surface.

## Prepare

Run `agent-device web doctor`. If the managed web backend is missing, run `agent-device web setup`, then repeat the doctor check.

Set the formatter path once from the repository where media will be captured:

```bash
FORMATTER="${AGENTS_HOME:-$HOME/.agents}/skills/before-and-after/scripts/format.mjs"
```

Save media inside that repository under paths without whitespace, for example:

```text
captures/desktop-before.png
captures/desktop-after.png
captures/mobile-before.png
captures/mobile-after.png
```

Supported formats: PNG, JPEG, GIF, WebP, MP4, MOV, and WebM. An `--after` file without a matching `--before` becomes a Preview.

## Capture

Use a separate named session for each side. Match the exact route, query state, viewport, application state, and scroll position before capturing.

```bash
agent-device open "https://production.example/path" --platform web --session before
agent-device viewport 1440 900 --platform web --session before
agent-device snapshot -i --platform web --session before
# Drive and verify the required state with refs/selectors and wait/get/is.
agent-device screenshot captures/desktop-before.png --platform web --session before
agent-device close --platform web --session before

agent-device open "https://preview.example/path" --platform web --session after
agent-device viewport 1440 900 --platform web --session after
agent-device snapshot -i --platform web --session after
# Reach and verify the same state.
agent-device screenshot captures/desktop-after.png --platform web --session after
agent-device close --platform web --session after
```

Default to viewport screenshots: they compare reliably without page mutation. Use `--fullscreen` only when both pages have materially equivalent height and framing. `agent-device` does not expose arbitrary page scripting, so it cannot reproduce the upstream skill's DOM-padding recipe. If full-page heights differ, recapture the same viewport or a smaller equivalent state instead of publishing a vertically misaligned table.

Inspect every capture before publishing. Reject login pages, platform errors, application errors, blank frames, loading skeletons, mismatched state, different scale, exposed secrets, and accidentally identical images when a visible change is expected.

### Authentication boundary

Authenticate through the visible UI and keep the login flow inside the named session. `agent-device --platform web` does not expose cookie/storage injection, request-header injection, network interception, or arbitrary page scripting. If a protected Vercel Preview cannot be reached through normal UI authentication, stop and report that the URL needs an accessible deployment or a browser-specific capture path. Never place OIDC tokens, bypass secrets, authenticated query parameters, or browser state in media or PR text.

### Screen recordings

Open and prepare the session before starting a recording. Web recordings must use WebM output.

```bash
agent-device open "https://preview.example/path" --platform web --session after-video
agent-device viewport 1440 900 --platform web --session after-video
# Reach the recording start state and verify it.
agent-device record start captures/desktop-after.webm --platform web --session after-video
# Perform the interaction.
agent-device record stop --platform web --session after-video
agent-device close --platform web --session after-video
```

Web recording does not accept native-device FPS, quality, max-size, or touch-overlay flags. Inspect native cadence rather than upsampling; changing a container to 30 or 60 fps only duplicates frames when the source cadence is lower.

## Format

Pass one `--before` and `--after` pair per comparison. Repeat `--label` for multiple pairs:

```bash
node "$FORMATTER" \
  --before captures/desktop-before.png \
  --after captures/desktop-after.png \
  --before captures/mobile-before.png \
  --after captures/mobile-after.png \
  --label Desktop \
  --label Mobile \
  > /tmp/before-and-after.md
```

After-only preview:

```bash
node "$FORMATTER" \
  --after captures/new-page.png \
  > /tmp/before-and-after.md
```

Use `--attribution "<name>"` only when the PR should credit the evidence author.

Images render in tables. Local videos initially render on separate lines so `gh --attach` can upload them and expose final attachment URLs. Video comparison tables use the two-step workflow below because `gh --attach` cannot rewrite local references inside `<video src>` attributes.

## Place the evidence

Read the existing PR description first. Put the marked visual block near the top: after short opening context and an existing Preview or deployment-link section, before implementation-heavy sections such as Details, Changes, Testing, or Notes.

Order primary proof before supplemental formats or demos. Label supplemental evidence and material capture limitations. Never invent prose to create an anchor or split a paragraph, list, table, code block, or other Markdown structure. If no safe anchor exists, append the block. If markers already exist, move or replace that whole block only; preserve unrelated prose byte-for-byte.

## Publish images or own-line videos

Run the formatter and `gh` from the same repository directory:

```bash
PR=123
gh pr view "$PR" --json body --jq .body > /tmp/pr-body.md

node "$FORMATTER" \
  --body-file /tmp/pr-body.md \
  --before captures/desktop-before.png \
  --after captures/desktop-after.png \
  > /tmp/pr-body-next.md

ATTACH_ARGS=()
while IFS= read -r file; do
  ATTACH_ARGS+=(--attach "$file")
done < <(
  node "$FORMATTER" \
    --attach-list \
    --before captures/desktop-before.png \
    --after captures/desktop-after.png
)

gh pr edit "$PR" --body-file /tmp/pr-body-next.md "${ATTACH_ARGS[@]}"
```

Fetch the edited PR body. Confirm no `./captures/...` reference remains inside `<!-- before-and-after:start/end -->`, unrelated prose is intact, and primary evidence precedes implementation details. Open the rendered PR and confirm image mapping, alignment, and media loading.

### Publish a video table

1. Upload local videos in a temporary PR comment with own-line output and `gh pr comment --attach`.
2. Fetch the comment with `gh api`; collect stable `https://github.com/user-attachments/assets/...` URLs in before/after order.
3. Generate and publish the final table:

   ```bash
   node "$FORMATTER" \
     --body-file /tmp/pr-body.md \
     --before-video-url https://github.com/user-attachments/assets/BEFORE_ID \
     --after-video-url https://github.com/user-attachments/assets/AFTER_ID \
     --label "Desktop hero" \
     > /tmp/pr-body-next.md

   gh pr edit "$PR" --body-file /tmp/pr-body-next.md
   ```

4. Fetch the edited body before deleting the temporary comment. Confirm both URLs are present and no local video path remains, then delete the comment.
5. Open the rendered PR. Confirm both videos are in the comparison table, become playable, and show controls.

If URL extraction, formatting, or verification fails, keep the temporary comment and retry from the last successful phase. Use own-line videos as the fallback.

## Formatter contract

`scripts/format.mjs` is the only bundled script. It formats existing local media or final GitHub video URLs, labels after-only media as Preview, emits the exact attachment list, and inserts or replaces one marked block without changing unrelated PR prose. Its arguments version with this skill; they are not a public library API.
