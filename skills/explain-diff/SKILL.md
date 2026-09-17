---
name: explain-diff
description: 코드 변경, diff, 브랜치 또는 PR을 깊이 있는 설명 문서(explainer)와 이해도 확인 퀴즈로 설명할 때 사용한다. Geoffrey Litt의 "Understanding is the new bottleneck" 접근(배경 → 직관 → 코드 → 퀴즈)에 기반해 검증이 아닌 참여를 위한 이해를 돕는다. Use for rich, interactive explanations of code changes, diffs, branches, and pull or merge requests, based on Geoffrey Litt's "Understanding is the new bottleneck".
---

# Explain Diff

에이전트가 코드 변경을 마치면, 그 변경을 깊이 있게 설명하는 문서(explainer)를 만들어 주세요. 이 스킬은 Geoffrey Litt가 AI Engineer World's Fair 2026에서 발표한 "Understanding is the new bottleneck" 접근을 따른다. 발표자가 공개한 원본 스킬(HTML·Notion 두 변형)과 PENEKhun의 한국어 번역·render.py 개선판을 통합했다. 출력 형식은 마크다운을 기본으로 한다.

## 왜 이해인가

- 에이전트가 코드를 대신 짜는 시대에도 사람의 이해는 여전히 중요하다. 이유는 검증(verify)이 아니라 **참여(participate)** 다. 에이전트는 스스로의 작업을 검증하는 데 점점 더 능숙해지고 있다. 하지만 프로젝트는 에이전트와의 수많은 반복 루프로 진행되며, 시스템에 대한 풍부한 개념을 머릿속에 가진 사람만이 다음 아이디어를 떠올리고 창의적으로 참여할 수 있다.
- **인지 부채(cognitive debt)**: 에이전트가 코드를 만드는 속도보다 사람이 시스템의 작동 원리를 머릿속에 유지하는 속도가 느려질 때 쌓인다. 기술 부채의 사촌이다. 단기적으로는 이해하지 않고 넘어갈 수 있지만 결국 대가를 치른다. (Margaret Storey, Simon Willison)
- 산출물은 diff 리뷰를 위한 부가물이 아니라, 팀원(그리고 미래의 나)이 프로젝트에 능동적으로 참여하기 위한 기반이다. 완성된 문서는 팀이 함께 보고 토론할 수 있는 공유 공간(예: Notion)에 두는 것을 기본으로 한다.

## 산출물

에이전트가 작업을 마칠 때마다 explainer 문서를 만든다. 원시 diff를 처음부터 줄 단위로 읽게 하는 대신 이 문서를 먼저 읽게 한다. (원시 diff는 마지막에 첨부) 기본 언어는 한국어다.

다음 섹션을 포함한다.

- **배경(Background)**: 이번 변경과 관련된 기존 시스템을 설명한다. 변경 지점 주변의 코드를 넓게 살펴 기존 시스템을 먼저 가르쳐야 한다(제1원칙: 배경부터). 독자의 사전 지식을 알 수 없으므로 초보자를 위한 깊이 있는 배경부터 시작하고, 익숙한 독자가 건너뛸 수 있게 구성한 뒤 변경과 직접 관련된 범위로 좁힌다.
- **직관(Intuition)**: 변경의 핵심 직관을 설명한다. 모든 세부 구현을 설명하기보다 본질을 이해시키는 데 집중한다(제2원칙: 세부 사항보다 직관을 먼저). 작은 예제 데이터와 구체적인 사례, 다이어그램을 충분히 사용한다.
- **코드(Code)**: 변경사항을 상위 수준에서 순서대로 설명한다. 이해하기 쉬운 기준으로 묶고 자연스러운 흐름에 따라 배치한다. **literate diff** — 파일 알파벳순 나열이 아니라 산문처럼 서술하며 코드 스니펫을 감싼다.
- **퀴즈(Quiz)**: 이해도 확인 객관식 문제 다섯 개. 난이도는 중간 수준. 단순한 함정 문제는 피하되, 변경의 핵심을 실제로 이해해야 답할 수 있게 만든다.

## 퀴즈 — 속도 조절기

퀴즈는 AI 루프의 **속도 조절기**다. 에이전트와 일할 때 루프가 사람의 이해 속도보다 빨라지기 쉽다. 기계적으로 "정말 이해했는가"를 묻는 장치가 퀴즈다. Geoffrey의 규칙: **퀴즈를 통과할 때까지 코드를 남에게 보내지 않는다. 남의 코드를 리뷰할 때도 퀴즈를 통과해야 한다.**

퀴즈 규칙:

- 각 문항은 서로 다른 개념을 묻고, 선택지는 3~4개로 만든다.
- 오답도 실제 변경을 피상적으로 읽은 사람이 고를 법하게 작성한다.
- 선택지의 문법, 구체성, 어조, 정보량을 맞춘다. 정답이 반복해서 가장 길거나 가장 짧아서는 안 되며, 길이가 단서가 되게 하지 않는다.
- 모든 선택지에 피드백을 작성한다. 정답은 왜 맞는지, 오답은 어떤 전제나 동작을 잘못 이해했는지 구체적으로 설명한다.
- 렌더링 전에 다섯 문항의 선택지 길이를 비교하고, 눈에 띄는 이상치나 반복되는 정답 길이 패턴을 고친다. 검증에 실패하면 우회하지 말고 선택지를 다시 쓴다.
- 마크다운 출력에서는 정답을 문항 바로 아래에 보여주지 말고 문서 끝 해설 섹션에 정답·피드백을 모아 둔다. 독자가 먼저 스스로 답해볼 기회를 주기 위함이다.

## 마크다운 이중 출력 계약

퀴즈가 있는 `.md`는 사람이 읽는 출력과 소비자가 읽는 숨은 정본을 함께 갖는다. 정본을 먼저 만들고, 모든 표현을 그 데이터에서 파생한다.

### 정본 메타데이터

다음 블록을 코드 펜스 밖 문서 최상위에 정확히 하나 둔다. 메타데이터는 질문 영역과 답변 영역 밖에 둔다.

```html
<!-- explain-diff-quiz:v1
{...strict JSON on one line...}
-->
```

첫 줄은 `<!-- explain-diff-quiz:v1`, 다음 줄은 주석이나 후행 쉼표가 없는 JSON 한 줄, 마지막 줄은 `-->`여야 한다. 문자열의 공백은 보존하고 줄바꿈은 JSON 이스케이프로 쓴다. 위 블록은 배치 예시이며, 실제 출력에는 아래 스키마를 만족하는 완전한 JSON을 넣는다.

```ts
type QuizOption = {
  id: "a" | "b" | "c" | "d";
  text: string;       // non-empty plain text; never interpreted as HTML
  correct: boolean;
  feedback: string;   // non-empty plain text; never interpreted as HTML
};
type QuizQuestion = {
  id: "q1" | "q2" | "q3" | "q4" | "q5";
  question: string;   // non-empty plain text; never interpreted as HTML
  options: QuizOption[]; // exactly 3 or 4, ids are a..c or a..d in order
};
type ExplainDiffQuiz = {
  version: 1;
  language: string;   // /^[A-Za-z]{2,3}(?:-[A-Za-z0-9]+)*$/, normally "ko" or "en"
  quiz: [QuizQuestion, QuizQuestion, QuizQuestion, QuizQuestion, QuizQuestion];
};
```

실제 JSON에는 위 필드만 포함한다. 문항 id는 `q1`부터 `q5`까지, 선택지 id는 `a`부터 `c` 또는 `d`까지 순서대로 쓴다. 각 문항에는 3~4개의 선택지와 정확히 하나의 `correct: true`, 공백뿐이지 않은 질문·선택지·피드백이 있어야 한다. 소비자는 중복 키를 거부하는 strict JSON 파서와 스키마 검사로 필드 누락·추가 필드·잘못된 타입이나 id를 거부한다. 메타데이터 버전과 블록 버전은 모두 1이어야 한다. JSON 문자열의 리터럴 `<`, `>`, `&`, `-`는 각각 `\u003c`, `\u003e`, `\u0026`, `\u002d`로 직렬화한다. 코드 예시의 `-->`나 `<script>`도 일반 텍스트로 보존하되, 주석을 닫거나 HTML로 실행하지 못하게 한다.

### 생성 순서와 마크다운 폴백

1. 변경을 설명할 산문과 퀴즈 데이터를 작성한다. 위 퀴즈 규칙과 품질 게이트를 정본 데이터에 적용한다.
2. `humanize-korean`을 산문과 퀴즈 문자열에 적용한다. 사람이 문구를 고치면 정본 데이터를 갱신한 것으로 보고, 아래 두 영역과 HTML 스펙을 모두 다시 생성한다.
3. 최종 정본에 스키마와 모든 퀴즈 품질 게이트를 다시 적용한다. 실패하면 우회하지 말고 정본을 고친다. 통과한 정본을 strict serializer로 메타데이터 주석으로 쓰고, 질문은 다음 경계 안에서 같은 정본으로 생성한다. 질문 바로 아래에는 답이나 피드백을 쓰지 않는다.

   ```html
   <!-- explain-diff:quiz:v1:start -->
   ... five human-readable questions ...
   <!-- explain-diff:quiz:v1:end -->
   ```

4. 문서 끝에 같은 정본에서 생성한 답변·피드백을 다음 경계 안에 둔다. 이 영역은 사람이 먼저 풀 수 있도록 질문 영역과 분리한다.

   ```html
   <!-- explain-diff:answers:v1:start -->
   ## 정답 및 피드백
   ... answers and feedback for q1 through q5 ...
   <!-- explain-diff:answers:v1:end -->
   ```

질문과 답변 영역의 표식은 각각 한 번씩, 들여쓰기 없이 문서 최상위에 홀로 둔다. 표식 앞뒤에는 빈 줄을 둔다. 영역은 질문 시작 → 질문 끝 → 해설 시작 → 해설 끝 순서로 배치하고 중첩하지 않는다. 표식은 교체 경계일 뿐, 목록에서 문항 데이터를 추론하는 단서가 아니다. 보이는 문항·선택지·해설은 Markdown 문법과 HTML 특수 문자를 이스케이프해 정본의 텍스트로 읽히게 한다. 정본과 두 영역은 함께 재생성하며, 한쪽만 수정해 서로 어긋나게 두지 않는다.

### 미래 웹 소비자의 실패 동작

웹 소비자는 렌더링된 DOM이 아니라 HTML 주석을 보존한 원본 Markdown AST의 최상위 HTML 노드에서 메타데이터를 읽는다. 코드 펜스·인용문·목록 안의 예시 주석은 대상이 아니다. 주석 인식과 raw HTML 렌더링은 별개이며, 파싱을 위해 임의의 HTML 실행을 허용하지 않는다. 유효한 정본과 두 영역 구조를 모두 찾았을 때만 해당 영역을 GUI로 교체하고 산문과 diff는 보존한다. 메타데이터 누락, 지원하지 않는 버전, JSON 오류, 표식 누락·중복·순서 오류가 있으면 GUI를 만들지 않고 원본 Markdown을 보여 준다. 제목이나 목록으로 데이터를 추측하지 않는다. 원본에는 정답이 공개되므로 시험 보안은 목표가 아니다.

이 절은 웹 구현을 위한 규약이며, 스킬 수정만으로 웹 파서나 GUI가 추가되지는 않는다. HTML 주석을 제거하는 일반 Markdown 뷰어에서도 보이는 문제와 해설은 남아야 한다.


## 직관 강화: 마이크로월드 (선택)

설명만으로는 부족한 변경에는 **마이크로월드**(Seymour Papert의 Mathland)를 만든다. 에이전트는 "코드를 이해시키는 코드"를 쓸 수 있다.

- 예: Prolog 인터프리터를 단계별로 실행하며 스택과 규칙 평가를 보여주는 디버거. 시간을 스크럽하고 각 단계의 상태를 확인할 수 있어야 한다.
- 예: 웹사이트 마이그레이션 스크립트를 단계별로 실행하는 "커맨드 센터" UI. 옛 사이트와 새 사이트를 나란히 두고 버튼을 눌러 포팅을 진행하며 파일 트리와 화면 변화를 눈으로 확인하게 한다.
- 원칙: 에이전트가 대신 디버깅/실행해 주는 것보다, **사람이 직접 조작하며 이해를 쌓게** 한다.

## 포맷

### 마크다운 (기본)

- 다이어그램은 mermaid를 사용한다(ASCII 아트 금지). 가능하면 설명 전반에서 반복해서 활용할 수 있는 소수의 다이어그램 유형을 정한다.
  - UI 변경: 사용자가 실제로 보게 되는 화면을 매우 단순화한 UI 다이어그램.
  - 데이터 흐름·통신: 시스템 다이어그램. 어떤 데이터가 오가는지 알 수 있게 예시 데이터를 반드시 포함.
- 핵심 개념·용어 정의·중요한 예외와 경계 조건은 인용 블록(콜아웃)으로 강조한다.
- 코드 블록은 언어별 fence를 사용한다. diff는 `diff`, 언어를 특정할 수 없으면 `text`.
- 비교가 필요한 경우 표를 사용한다.
- Martin Kleppmann의 글처럼 명료하고 자연스러운 흐름으로 작성한다. 독자의 흥미를 끌되 고전적이고 정제된 문체를 사용하고, 섹션 사이의 전환을 매끄럽게 이어간다.

### HTML (인터랙티브 퀴즈가 필요할 때)

클릭형 퀴즈나 인터랙티브 피규어가 필요하면 스킬 디렉터리의 `render.py`를 사용한다. 스키마가 기억나지 않으면 먼저 다음을 실행한다.

```bash
python3 render.py --help
```

작은 JSON 콘텐츠 명세를 작성하고 결과 경로를 명시해 실행한다.

```bash
python3 render.py <spec.json> -o <output.html>
```

HTML 스펙의 `quiz`는 정본 `quiz`에서 매핑해 만든다. 각 문항과 선택지의 `id`는 버리고 `question`, `options[].text`, `options[].correct`, `options[].feedback`만 같은 값으로 전달한다. 이 값들은 plain string으로 그대로 넘긴다. `render.py`가 퀴즈 질문·선택지·피드백을 HTML 이스케이프하므로 어댑터에서 미리 이스케이프하면 안 된다. `render.py`는 Markdown을 파싱하지 않는다.

`sections[].html`에는 Markdown이 아닌 raw HTML을 넣는다. 코드 블록은 `<pre><code class="language-{언어}">...</code></pre>`(코드 안의 `<`, `>`, `&`는 HTML 엔티티로 이스케이프), 흐름도는 `.diagram`·`.flow`·`.box`·`.box.fail`, 핵심 정의와 예외는 `.callout`, 비교는 `<table>`을 사용한다. raw HTML에 삽입하는 산문·코드 문자열은 어댑터에서 HTML 이스케이프한다. 렌더러가 CSS, JavaScript, 문법 강조, 문서 골격, 목차, 선택지 순서 무작위화, 언어별 UI 문구를 처리하도록 맡긴다.

파일은 코드 저장소 밖(예: `/tmp`)에 두는 것을 권장한다. `-o`를 생략하면 스펙 파일이 있는 폴더에 `YYYY-MM-DD-explanation-<slug>.html`로 저장된다. 날짜 접두사는 시간 순 정렬과 버전 관리 밖 보관을 위한 것이다.

HTML을 만들 때도 먼저 정본을 humanize하고 검증한 뒤 같은 데이터로 Markdown 두 영역과 `spec.quiz`를 생성한다. HTML과 Markdown의 퀴즈 문구를 따로 쓰지 않는다.

### 공유 공간 페이지 (Notion/Outline)

발표자의 원본 스킬 변형 중 하나: 팀과 함께 이해를 쌓기 위한 공유 공간(shared space)에 explainer를 게시한다.

- Notion MCP 도구가 있으면 새 페이지를 만들고 URL을 반환한다. (발표자 기본 동작)
- 이 워크스페이스처럼 Outline이 지식 SoT인 환경에서는 outline MCP 도구로 문서를 만든다.
- 퀴즈는 정본 데이터에서 토글 블록으로 표현한다. 문항 아래 각 선택지를 토글로 두고, 펼치면 ✅(정답)/❌(오답) 판정과 설명이 보이게 한다:

```markdown
1. Question
   ▶ Option 1
    ❌ 왜 틀렸는지에 대한 설명
   ▶ Option 2
    ✅ 왜 맞는지에 대한 설명
   ▶ Option 3
    ❌ 어떤 전제를 잘못 이해했는지에 대한 설명
```

토글로 숨겨두므로 독자가 먼저 스스로 답해볼 기회가 유지된다. 선택지 품질 규칙(길이 단서 금지, 전 선택지 피드백)은 동일하게 적용한다. 공유 공간 도구가 HTML 주석을 제거할 수 있으므로 원본 `.md` 산출물을 보존하고, 주석을 제거한 페이지가 Markdown과 완전히 왕복된다고 말하지 않는다.

## 한국어 (기본 언어)

explainer 문서는 한국어를 기본 언어로 작성한다. 문서를 만들기 전에 `humanize-korean` 스킬을 1회 적용하며, 퀴즈 문자열도 정본 데이터의 일부로 함께 humanize한다. 그 결과로 정본 메타데이터, Markdown 질문·답변 영역, HTML `spec.quiz`를 모두 다시 생성한다. HTML 변형은 정본의 `"language": "ko"`를 스펙에 전달해 퀴즈 UI 문구(정답/오답 등)를 한국어로 렌더링되게 한다. 영어 문서가 명시적으로 요청된 경우에만 영어로 작성한다.

## 참고

- 영상: Geoffrey Litt, "Understanding is the new bottleneck" (AI Engineer World's Fair 2026, 한영 자막) — https://youtu.be/x3e_Yl4NNHY
- 발표 글: https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck
- 원본 스킬 gist (HTML·Notion 두 변형): https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524
- 한국어 번역·render.py gist: https://gist.github.com/PENEKhun/f467c3c0e83c0ab792e761350e71508e
