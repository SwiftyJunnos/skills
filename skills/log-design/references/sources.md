# 근거 문서

원칙의 근거를 인용해야 할 때 읽는다. 여덟 원칙은 아래 문서를 종합한 제안이며, 특정 회사의 규칙을 그대로 옮긴 것이 아니다.

| 문서 | 다루는 원칙 | 핵심 |
|---|---|---|
| [토스 DataOps, 로그 정의 스킬](https://toss.tech/article/dataops-log-definition-skill) | §1, §2, §6, §8 | 도메인 의미와 속성 재사용(`card_company`), 입력 원문 대신 필요한 정보만 남기기, 형식 검사를 CLI와 서버가 담당 |
| [Segment Tracking Plan best practices](https://www.twilio.com/docs/segment/protocols/tracking-plan/best-practices) | §2, §3 | `Object Action` 명명, 일관성, 값마다 이벤트를 만들지 않기, Tracking Plan으로 검증 |
| [Segment, 클라이언트와 서버 수집](https://www.twilio.com/docs/segment/guides/how-to-guides/collect-on-client-or-server) | §1 | 결제 완료 같은 중요한 업무 이벤트는 서버에서 수집 |
| [Segment API (`messageId` 중복 제거)](https://www.twilio.com/docs/segment/api/) | §5 | 수집 도구의 중복 제거에는 처리 범위의 한계가 있음 |
| [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) | §4, §7 | 발생 시각과 관측 시각, 심각도, 본문, 속성, `TraceId`, `SpanId`, 리소스 |
| [OpenTelemetry Recording errors](https://opentelemetry.io/docs/specs/semconv/general/recording-errors/) | §5 | 재시도로 처리된 오류와 최종 결과를 구분, 같은 예외 중복 기록 금지. 개발 단계 규약 |
| [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | §1, §6, §8 | 목적 없는 수집 지양, 비밀번호·토큰·세션 ID 제외, 로그 위조 방지, 로깅 실패 검증 |
| [Snowplow schema anatomy](https://docs.snowplow.io/docs/api-reference/iglu/schema-anatomy/) | §3 | 필수 필드 추가나 자료형 변경처럼 기존 이벤트를 무효화하는 변경은 별도 버전 |
| [Grafana Loki, cardinality](https://grafana.com/docs/loki/latest/get-started/labels/cardinality/) | §4 | 요청 ID·사용자 ID 같은 고카디널리티 값은 라벨 대신 구조화 메타데이터로 |
