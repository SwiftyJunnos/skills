# Moa publishing

Use this only for profiles with `workflow: moa`. This describes the Fitween Moa app inspected on 2026-10-22; inspect the current UI if it differs. Resolve the base URL from the chosen profile.

## Login and editor

Reading the homepage and articles is public. Writing and editing require authentication. Open `/#/write`; the guest button **로그인하고 계속하기** enters `/auth/login?returnTo=%2Fwrite`, then Cloudflare Access returns to the editor.

`GET /api/me` in the authenticated same-origin browser session returns `null` or `{id, email, name}`. Verify `email` against the chosen account without extracting cookies or tokens. The UI's **모아 사용 가이드** also shows **로그인 계정 · email** when signed in.

The editor has **주제**, **글 제목**, **한 줄 요약**, **글 본문**, and **태그**. Categories are 개발, 디자인, 프로덕트, and 일하는 방식. Current limits are 120 characters for the title, 240 for the summary, 100,000 for the body, and five tags of up to 30 characters each. Use **미리보기**, then **글 발행하기**. A successful post opens `/#/post/<id>`.

An author's own post has **글 수정**, opening `/#/edit/<id>`; save with **수정 완료**. The app supports Markdown/GFM. It has no built-in Mermaid renderer or image uploader; use supported tables/code blocks and accessible image URLs. Local file paths will not work for public readers.

## Verification and recovery

Reopen the canonical post and check its rendered body. `GET /api/posts/<id>` provides the body and author display name, but hides `authorId`. Corroborate author identity with the verified session and editor. Check the published page without authentication as well.

The browser keeps editor drafts in account-scoped local storage. Keep the separate Markdown draft to recover across browsers or expired sessions. If the submit response is lost, inspect the post list for the just-submitted title/body before retrying.

Use the normal authenticated editor or a supported authenticated tool. Direct D1 changes, forged author fields, and changes to Cloudflare Access are outside article publication. Local development has separate data/identity; a Git push or app deployment does not publish an article.
