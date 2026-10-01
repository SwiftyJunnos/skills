# GitHub 댓글과 스레드 처리

전용 GitHub connector의 스레드 조회, 답댓글, resolve 도구를 우선 사용한다. 현재 노출된 도구 설명에서 인자 이름과 응답을 확인한다. CLI가 필요하면 인증된 `gh`를 사용하고, 저장소의 Git 작업 방식은 유지한다.

## ID와 댓글 종류

| 값 | 용도 |
| --- | --- |
| Review comment의 REST `id` 또는 GraphQL `databaseId` | REST 답댓글의 숫자 comment ID |
| Review thread의 GraphQL `id` | `resolveReviewThread`의 thread ID |
| Review comment의 GraphQL `id` | 댓글 node ID. thread ID로 사용하지 않는다 |
| Review의 ID | 전체 리뷰 식별자. 개별 댓글이나 스레드 ID로 사용하지 않는다 |

REST 답댓글은 인라인 스레드의 최상위 댓글을 대상으로 한다. `in_reply_to_id` 또는 GraphQL `replyTo`가 있는 댓글은 원래 최상위 댓글을 찾아 답한다. 답댓글에 대한 REST 답댓글은 지원하지 않는다. [GitHub review comments 문서](https://docs.github.com/en/rest/pulls/comments#create-a-reply-for-a-review-comment).

일반 PR 타임라인 댓글은 issue comment이며 인라인 review thread의 resolve 상태가 없다. 리뷰 본문도 개별 review thread와 구분한다. 이 경우 필요한 답을 PR 논의에 남기고 인라인 스레드를 해결한 것처럼 집계하지 않는다.

## `gh`로 조회

`PR_OWNER`, `PR_NAME`, `PR_REPO`, `PR_NUMBER`는 확인한 대상에서 설정한다. `PR_REPO`는 `owner/name`이다. 다른 GitHub 호스트는 대상 원격에 맞는 인증과 `--hostname`을 사용한다.

```sh
gh pr view "$PR_NUMBER" --repo "$PR_REPO" \
  --json url,state,baseRefName,headRefName,headRefOid

gh api --paginate "repos/$PR_REPO/pulls/$PR_NUMBER/comments"
gh api --paginate "repos/$PR_REPO/issues/$PR_NUMBER/comments"
gh api --paginate "repos/$PR_REPO/pulls/$PR_NUMBER/reviews"
```

REST 댓글 목록만으로 resolve 여부를 추론하지 않는다. 스레드 상태는 GraphQL이나 connector에서 읽는다.

```sh
gh api graphql --paginate \
  -f owner="$PR_OWNER" -f name="$PR_NAME" -F number="$PR_NUMBER" \
  -f query='
query($owner: String!, $name: String!, $number: Int!, $endCursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      headRefOid
      reviewThreads(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated path line
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id databaseId url body
              author { login }
              replyTo { databaseId }
              commit { oid }
            }
          }
        }
      }
    }
  }
}'
```

위 `--paginate`는 reviewThreads 페이지용이다. 각 스레드의 `comments.pageInfo.hasNextPage`도 확인하고, 남은 댓글은 해당 thread를 `node(id:)`로 조회해 별도로 페이지네이션한다. 댓글 100개 제한 때문에 보류 사유나 기존 답댓글을 놓치지 않도록 한다.

## 답댓글과 resolve

판정과 검증이 끝난 답댓글 본문을 UTF-8 파일에 실제 개행으로 저장한다. 숫자 `PR_REVIEW_COMMENT_ID`는 확인한 최상위 review comment ID다.

```sh
gh api --method POST \
  "repos/$PR_REPO/pulls/$PR_NUMBER/comments/$PR_REVIEW_COMMENT_ID/replies" \
  -F 'body=@/tmp/pr-thread-reply.md'
```

본문을 셸 명령에 직접 보간하지 않는다. 생성된 댓글의 `html_url`과 `in_reply_to_id`를 확인한다. 이 답댓글 등록은 알림을 발생시키므로 승인된 PR 논의에만 수행한다. [REST reply 문서](https://docs.github.com/en/rest/pulls/comments#create-a-reply-for-a-review-comment).

`PR_REVIEW_THREAD_ID`는 해당 스레드에서 조회한 GraphQL thread ID다. 답댓글 확인 후 실행한다.

```sh
gh api graphql -f thread="$PR_REVIEW_THREAD_ID" -f query='
mutation($thread: ID!) {
  resolveReviewThread(input: {threadId: $thread}) {
    thread { id isResolved }
  }
}'
```

HTTP 성공 여부와 함께 GraphQL `errors`를 확인한다. 반환된 스레드의 ID와 `isResolved: true`를 확인하고, 마지막 조회에서 상태를 재확인한다.

## 결과가 불확실할 때

타임아웃이나 연결 종료 후 같은 답댓글 POST를 바로 반복하지 않는다. 대상 스레드를 새로 읽고, 현재 계정이 같은 근거·커밋·본문으로 등록한 답댓글이 있는지 확인한다. 이미 존재하면 해당 댓글을 사용해 다음 단계로 진행한다. resolve 요청도 현재 `isResolved`를 먼저 확인한다.

원격 head가 달라졌다면 답댓글의 코드 근거를 갱신한다. 로컬 푸시 성공이나 `outdated` 표시만으로 스레드를 해결했다고 판단하지 않는다.
