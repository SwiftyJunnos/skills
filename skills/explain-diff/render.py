#!/usr/bin/env python3
"""
render.py — render a structured explain-diff spec into the single-page HTML
format used by the `explain-diff-html` skill.

Why this exists: the CSS, quiz JavaScript, and page scaffolding are identical
across every invocation of the explain-diff skill — only the content (prose,
diagrams, quiz questions) actually changes per diff. Regenerating the full
~250 lines of boilerplate CSS/JS by hand every time wastes tokens. This script
takes a small JSON spec with just the content and renders the final page.

Usage:
    python3 render.py spec.json [-o output.html]

If -o is omitted, writes to
<dir-of-spec>/YYYY-MM-DD-explanation-<slug>.html, where <slug> comes from the
spec's "slug" field or is derived from the title.

Spec format (JSON):
{
  "title": "Rewriting the retry logic: exponential backoff with jitter",
  "subtitle": "Prepared 2026-07-15 · PR #482",
  "slug": "retry-backoff-refactor",
  "language": "en",
  "sections": [
    {"id": "background", "heading": "Background", "html": "<p>...</p>"},
    {"id": "intuition", "heading": "Intuition", "html": "<p>...</p><div class=\"diagram\">...</div>"},
    {"id": "code", "heading": "Code walkthrough", "html": "<pre><code class=\"language-typescript\">...</code></pre>"}
  ],
  "quiz": [
    {
      "question": "Why did the first retry attempt fire immediately instead of waiting?",
      "options": [
        {
          "text": "The jitter step produced a negative delay before the attempt began.",
          "correct": false,
          "feedback": "Jitter changes the chosen delay, but the old code did not produce a negative value here."
        },
        {
          "text": "The base delay was multiplied only after the first attempt completed.",
          "correct": true,
          "feedback": "The initial attempt used the unmodified zero-delay state; multiplication happened afterward."
        },
        {
          "text": "The retry scheduler discarded the timer before the attempt began.",
          "correct": false,
          "feedback": "The timer remained active; the value supplied to it was the source of the immediate attempt."
        }
      ]
    }
  ]
}

Each option needs specific feedback explaining why it is correct or incorrect.
Option order within each quiz question is randomized by the renderer at render
time, so do not manually vary the answer position.

The "html" fields are raw HTML — write real markup, not markdown. Code blocks
must use <pre><code class="language-{name}">...</code></pre> with HTML-escaped
code. The renderer loads a pinned highlight.js version and theme from cdnjs.
"""
import argparse
import datetime
import html
import json
import random
import re
from pathlib import Path

HIGHLIGHT_VERSION = "11.11.1"
HIGHLIGHT_JS_URL = f"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/{HIGHLIGHT_VERSION}/highlight.min.js"
HIGHLIGHT_CSS_URL = f"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/{HIGHLIGHT_VERSION}/styles/github-dark.min.css"

CSS = """
  :root {
    --bg: #fafaf8; --fg: #1a1a1a; --accent: #b5541f; --muted: #6b6b6b;
    --code-bg: #0d1117; --code-fg: #c9d1d9; --callout-bg: #fff4e8; --border: #e0ddd6;
  }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
    background: var(--bg); color: var(--fg);
    max-width: 820px; margin: 0 auto; padding: 2rem 1.5rem 6rem; line-height: 1.65; }
  h1 { font-size: 1.9rem; border-bottom: 3px solid var(--accent); padding-bottom: .5rem; }
  h2 { font-size: 1.4rem; margin-top: 3rem; color: var(--accent); }
  h3 { font-size: 1.1rem; margin-top: 1.8rem; }
  code { font-family: 'SF Mono', Consolas, monospace; background: #eee; padding: .1rem .3rem; border-radius: 3px; font-size: .92em; }
  pre { background: var(--code-bg); color: var(--code-fg); padding: 1rem 1.2rem; border-radius: 8px;
    overflow-x: auto; white-space: pre-wrap; font-family: 'SF Mono', Consolas, monospace; font-size: .88rem; line-height: 1.5; }
  pre code { background: none; padding: 0; color: inherit; }
  pre code.hljs { padding: 0; background: ransparent; }
  .callout { background: var(--callout-bg); border-left: 4px solid var(--accent); padding: .9rem 1.2rem;
    border-radius: 0 6px 6px 0; margin: 1.2rem 0; }
  .toc { background: #fff; border: 1px solid var(--border); border-radius: 8px; padding: 1rem 1.5rem; margin: 1.5rem 0; }
  .toc a { color: var(--accent); text-decoration: none; }
  .toc ul { margin: .3rem 0; }
  .diagram { background: #fff; border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem;
    margin: 1.2rem 0; font-family: 'SF Mono', Consolas, monospace; font-size: .85rem; }
  .flow { display: flex; align-items: center; gap: .6rem; flex-wrap: wrap; justify-content: center; padding: .5rem 0; }
  .box { border: 2px solid var(--accent); border-radius: 8px; padding: .6rem 1rem; background: #fdf6ee; text-align: center; min-width: 120px; }
  .box.fail { border-color: #b91c1c; background: #fef2f2; }
  .arrow { font-size: 1.4rem; color: var(--muted); }
  table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .92rem; }
  th, td { border: 1px solid var(--border); padding: .5rem .7rem; text-align: left; }
  th { background: #f0ede6; }
  .quiz-q { background: #fff; border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem 1.5rem; margin: 1.2rem 0; }
  .quiz-opt { display: block; width: 100%; text-align: left; padding: .6rem 1rem; margin: .4rem 0;
    border: 1px solid var(--border); border-radius: 6px; background: #fff; cursor: pointer; font-family: inherit; font-size: .95rem; }
  .quiz-opt:hover { background: #f5f2ec; }
  .quiz-opt:focus-visible, .toc a:focus-visible { outline: 3px solid #2563eb; outline-offset: 2px; }
  .feedback { display: none; margin-top: .6rem; padding: .6rem 1rem; border-radius: 6px; font-size: .9rem; }
  .feedback.correct { background: #ecfdf3; color: #166534; border-left: 3px solid #16a34a; }
  .feedback.incorrect { background: #fef2f2; color: #991b1b; border-left: 3px solid #dc2626; }
  .badge { display: inline-block; font-size: .75rem; padding: .15rem .5rem; border-radius: 10px; font-family: sans-serif; }
  .badge.new { background: #dcfce7; color: #166534; }
  @media (max-width: 600px) { body { padding: 1rem; } .flow { flex-direction: column; } }
"""

QUIZ_JS = """
document.querySelectorAll('.quiz-q').forEach(q => {
  q.querySelectorAll('.quiz-opt').forEach(opt => {
    opt.addEventListener('click', () => {
      const correct = opt.dataset.correct === 'true';
      q.querySelectorAll('.feedback').forEach(item => item.style.display = 'none');
      q.querySelectorAll('.quiz-opt').forEach(item => item.setAttribute('aria-expanded', 'false'));
      const fb = opt.nextElementSibling;
      fb.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
      fb.style.display = 'block';
      opt.setAttribute('aria-expanded', 'true');
    });
  });
});
"""

UI_TEXT = {
    "en": {
        "contents": "Contents",
        "quiz": "Quiz",
        "correct": "Correct.",
        "incorrect": "Not quite.",
    },
    "ko": {
        "contents": "목차",
        "quiz": "퀴즈",
        "correct": "정답입니다.",
        "incorrect": "오답입니다.",
    },
}

PRE_TAG_RE = re.compile(r"<pre\b", re.IGNORECASE)
HIGHLIGHTABLE_PRE_RE = re.compile(
    r'''<pre\b[^>]*>\s*<code\b[^>]*class=["'][^"']*\blanguage-[A-Za-z0-9_+.-]+[^"']*["'][^>]*>''',
    re.IGNORECASE,
)


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w]+", "-", text.lower(), flags=re.UNICODE).strip("-")
    return slug or "code-change"


def _visible_text_length(text: str) -> int:
    """Measure option copy without counting HTML markup or repeated whitespace."""
    without_tags = re.sub(r"<[^>]*>", "", str(text))
    return len(" ".join(html.unescape(without_tags).split()))


def validate_quiz(quiz: list) -> None:
    """Reject malformed quizzes and answer patterns leaked through copy length."""
    longest_correct = []
    shortest_correct = []
    conspicuous_outliers = []

    for question_number, question in enumerate(quiz, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"quiz question {question_number} must be an object")
        if not isinstance(question.get("question"), str) or not question["question"].strip():
            raise ValueError(f"quiz question {question_number} needs non-empty question text")

        options = question.get("options", [])
        if not isinstance(options, list) or not 3 <= len(options) <= 4:
            raise ValueError(f"quiz question {question_number} must have three or four options")

        for option_number, option in enumerate(options, start=1):
            if not isinstance(option, dict):
                raise ValueError(
                    f"quiz question {question_number} option {option_number} must be an object"
                )
            if not isinstance(option.get("correct"), bool):
                raise ValueError(
                    f"quiz question {question_number} option {option_number} needs a boolean 'correct'"
                )
            if not isinstance(option.get("feedback"), str) or not option["feedback"].strip():
                raise ValueError(
                    f"quiz question {question_number} option {option_number} needs specific feedback"
                )

        correct_indexes = [i for i, option in enumerate(options) if option.get("correct") is True]
        if len(correct_indexes) != 1:
            raise ValueError(f"quiz question {question_number} must have exactly one correct option")

        lengths = [_visible_text_length(option.get("text", "")) for option in options]
        if any(length == 0 for length in lengths):
            raise ValueError(f"quiz question {question_number} contains an empty option")
        normalized_options = [" ".join(str(option["text"]).split()).casefold() for option in options]
        if len(set(normalized_options)) != len(normalized_options):
            raise ValueError(f"quiz question {question_number} contains duplicate options")

        correct_length = lengths[correct_indexes[0]]
        incorrect_lengths = [
            length for i, length in enumerate(lengths) if i != correct_indexes[0]
        ]
        if correct_length - max(incorrect_lengths) >= 5:
            longest_correct.append(question_number)
        if min(incorrect_lengths) - correct_length >= 5:
            shortest_correct.append(question_number)

        shortest = min(lengths)
        longest = max(lengths)
        if longest - shortest >= 20 and longest > shortest * 1.5:
            conspicuous_outliers.append(question_number)

    problems = []
    if conspicuous_outliers:
        problems.append(
            "conspicuous option-length outliers in question(s) "
            + ", ".join(map(str, conspicuous_outliers))
        )
    if len(quiz) >= 3 and len(longest_correct) > len(quiz) / 2:
        problems.append(
            "the correct option is uniquely longest in question(s) "
            + ", ".join(map(str, longest_correct))
        )
    if len(quiz) >= 3 and len(shortest_correct) > len(quiz) / 2:
        problems.append(
            "the correct option is uniquely shortest in question(s) "
            + ", ".join(map(str, shortest_correct))
        )
    if problems:
        raise ValueError(
            "quiz option lengths reveal answer patterns; rewrite the options so length is not a clue: "
            + "; ".join(problems)
        )


def validate_spec(spec: dict) -> None:
    """Validate the content contract before constructing the HTML page."""
    if not isinstance(spec, dict):
        raise ValueError("the content spec must be a JSON object")
    if not isinstance(spec.get("title"), str) or not spec["title"].strip():
        raise ValueError("the content spec needs a non-empty 'title'")
    if "subtitle" in spec and not isinstance(spec["subtitle"], str):
        raise ValueError("'subtitle' must be a string")
    if "slug" in spec and (not isinstance(spec["slug"], str) or not spec["slug"].strip()):
        raise ValueError("'slug' must be a non-empty string when provided")

    language = spec.get("language", "en")
    if not isinstance(language, str) or not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]+)*", language):
        raise ValueError("'language' must be a language code such as 'en' or 'ko-KR'")

    sections = spec.get("sections", [])
    if not isinstance(sections, list) or not sections:
        raise ValueError("the content spec needs at least one section")
    section_ids = []
    for section_number, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            raise ValueError(f"section {section_number} must be an object")
        section_id = section.get("id")
        if not isinstance(section_id, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", section_id):
            raise ValueError(
                f"section {section_number} needs an id beginning with a letter and containing only letters, digits, '_' or '-'"
            )
        for field in ("heading", "html"):
            if not isinstance(section.get(field), str) or not section[field].strip():
                raise ValueError(f"section {section_number} needs non-empty '{field}' text")
        pre_count = len(PRE_TAG_RE.findall(section["html"]))
        highlighted_pre_count = len(HIGHLIGHTABLE_PRE_RE.findall(section["html"]))
        if pre_count != highlighted_pre_count:
            raise ValueError(
                f"section {section_number} code blocks must use "
                '<pre><code class="language-{name}">...</code></pre>'
            )
        section_ids.append(section_id)
    if len(set(section_ids)) != len(section_ids):
        raise ValueError("section ids must be unique")

    quiz = spec.get("quiz", [])
    if not isinstance(quiz, list):
        raise ValueError("'quiz' must be a list")
    validate_quiz(quiz)


def render(spec: dict) -> str:
    validate_spec(spec)
    title = spec["title"]
    subtitle = spec.get("subtitle", "")
    sections = spec.get("sections", [])
    quiz = spec.get("quiz", [])
    language = spec.get("language", "en")
    labels = UI_TEXT.get(language.split("-", 1)[0].lower(), UI_TEXT["en"])

    toc_items = "\n".join(
        f'  <li><a href="#{s["id"]}">{html.escape(s["heading"])}</a></li>' for s in sections
    )
    if quiz:
        toc_items += f'\n  <li><a href="#quiz">{html.escape(labels["quiz"])}</a></li>'

    body_sections = "\n\n".join(
        f'<h2 id="{s["id"]}">{html.escape(s["heading"])}</h2>\n{s["html"]}' for s in sections
    )

    quiz_html = ""
    if quiz:
        blocks = []
        for question_number, q in enumerate(quiz, start=1):
            options = list(q["options"])
            random.shuffle(options)
            rendered_options = []
            for option_number, option in enumerate(options, start=1):
                is_correct = option["correct"]
                feedback_id = f"feedback-{question_number}-{option_number}"
                result_label = labels["correct"] if is_correct else labels["incorrect"]
                rendered_options.append(
                    f'<button type="button" class="quiz-opt" '
                    f'data-correct="{"true" if is_correct else "false"}" '
                    f'aria-controls="{feedback_id}" aria-expanded="false">'
                    f'{html.escape(str(option["text"]))}</button>\n'
                    f'<div id="{feedback_id}" class="feedback" role="status" aria-live="polite">'
                    f'<strong>{html.escape(result_label)}</strong> '
                    f'{html.escape(option["feedback"])}</div>'
                )
            opts = "\n".join(rendered_options)
            blocks.append(f'<div class="quiz-q">\n<p><strong>{html.escape(q["question"])}</strong></p>\n{opts}\n</div>')
        quiz_html = f'<h2 id="quiz">{html.escape(labels["quiz"])}</h2>\n\n' + "\n\n".join(blocks)

    return f"""<!DOCTYPE html>
<html lang="{html.escape(language, quote=True)}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{HIGHLIGHT_CSS_URL}">
<style>{CSS}</style>
</head>
<body>

<h1>{html.escape(title)}</h1>
{f'<p style="color:var(--muted); margin-top:-.5rem;">{html.escape(subtitle)}</p>' if subtitle else ''}

<div class="toc">
<strong>{html.escape(labels["contents"])}</strong>
<ul>
{toc_items}
</ul>
</div>

{body_sections}

{quiz_html}

<script src="{HIGHLIGHT_JS_URL}"></script>
<script>if (window.hljs) hljs.highlightAll();</script>
<script>{QUIZ_JS}</script>

</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", type=Path, help="path to the JSON content spec")
    ap.add_argument("-o", "--output", type=Path, default=None, help="output HTML path")
    args = ap.parse_args()

    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        out_html = render(spec)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        ap.error(str(exc))

    if args.output:
        out_path = args.output
    else:
        date_prefix = datetime.date.today().strftime("%Y-%m-%d")
        slug = spec.get("slug") or slugify(spec["title"])
        out_path = args.spec.parent / f"{date_prefix}-explanation-{slug}.html"

    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_html, encoding="utf-8")
    except OSError as exc:
        ap.error(str(exc))
    print(str(out_path))


if __name__ == "__main__":
    main()t
