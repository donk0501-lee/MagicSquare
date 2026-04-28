# MagicSquare — `.cursorrules` 작업 보고서

**문서 목적:** 프로젝트 루트 `.cursorrules` 파일을 설계·작성·검토·완성한 작업 내역을 한곳에 보존한다.  
**범위:** YAML 뼈대 작성, `tdd_rules` 초안, 규칙 파일 검토, 전 섹션 완성, 문법 검증 및 기술적 메모.  
**비범위:** 실제 Python 구현 코드, pytest 스위트 작성, Cursor 제품의 규칙 파싱 동작 보장.

**작성 기준일:** 2026-04-27  

---

## 1. 작업 개요

| 순서 | 작업 | 산출 |
|------|------|------|
| 1 | `.cursorrules` YAML 뼈대 | 최상위 8키(`project`, `code_style`, `architecture`, `tdd_rules`, `testing`, `forbidden`, `file_structure`, `ai_behavior`), 값 비움, 섹션당 80자 `#` 구분선 주석 |
| 2 | `tdd_rules` 초기 채움 | `red_phase` / `green_phase` / `refactor_phase`를 한 줄 문자열로 기술 |
| 3 | 규칙 파일 검토 | YAML 문법, 필수 섹션 공백, `tdd_rules`↔`forbidden` 충돌, `ai_behavior` 실효성 점검(문제점만 보고, 수정은 보류) |
| 4 | 전 섹션 완성 | MagicSquare·Report 계약과 정합되도록 전 섹션 구조화·본문 작성 |
| 5 | YAML 검증 | PyYAML `safe_load`로 파싱 성공 확인; `(예: ` 등 콜론+공백으로 인한 스캐너 오류는 따옴표 이스케이프로 해소 |

---

## 2. 최종 `.cursorrules` 구조 요약

루트 파일: 저장소 루트의 `.cursorrules` (YAML).

| 섹션 | 역할 요약 |
|------|-----------|
| `project` | MagicSquare 도메인(4×4, 빈칸 2, int[6] 출력), 목표(TDD·ECB·Report 정합), 스택(Python 3.11+, pytest) |
| `code_style` | Python 3.11+, PEP 8, 전 함수 타입 힌트, Google docstring(public), 88열·Black |
| `architecture` | ECB 3레이어 정의(boundary / control / entity), 의존성 방향 boundary → control → entity |
| `tdd_rules` | 각 phase별 `description`, `rules` 목록, `must_not` 목록 |
| `testing` | pytest, AAA, 커버리지 하한 80%, 픽스처 스코프 규칙, `test_` 접두사 |
| `forbidden` | 항목별 `pattern` / `reason` / `alternative` (print, 하드코딩, 광범위 except, boundary 내 도메인 로직 등) |
| `file_structure` | ECB 기준 권장 트리를 `recommended_tree` 리터럴 블록 내 `#` 주석 형태로 기술 |
| `ai_behavior` | 작성 전·중·후 행동, TDD 위반 시 응답 내 경고 문단·템플릿·금지 사항 |

---

## 3. 검토 단계에서 확인된 사항 (당시 기준)

- **YAML 문법:** 검토 시점의 파일은 유효 YAML로 파싱됨.  
- **필수 섹션:** 키는 모두 존재했으나 `tdd_rules` 외 대부분이 내용 미기입 상태였음.  
- **`tdd_rules` vs `forbidden`:** `forbidden`이 비어 있어 당시에는 문장 수준의 충돌 없음.  
- **`ai_behavior`:** 비어 있어 “따를 수 없는 규칙”은 없었음.  
- **메모:** RED 단계의 “테스트 실행·실패 확인”은 에이전트 환경에 따라 항상 재현 가능하지 않을 수 있음 → 완성본에서는 `testing`·`ai_behavior`와 연계해 완화·보완 문구를 둠.

---

## 4. 완성 단계에서의 기술 메모

### 4.1 YAML 이스케이프

한국어 본문에 `(예: 테스트`처럼 **콜론 뒤 공백(`: `)**이 오면 YAML 1.1 플레인 스칼라에서 매핑 구분자로 오인될 수 있음.  
해결: 해당 문장 전체를 큰따옴표로 감쌈(예: `during_coding` 한 항목, `on_tdd_violation.rule`).

### 4.2 구분선

섹션 앞 80자 `#` 한 줄은 YAML 전체 줄 주석으로 유지되어, 키 값과 충돌하지 않음.

### 4.3 Report와의 정합

`project`·`forbidden`·`file_structure` 등은 `Report/MagicSquare_ProblemDefinition_Report.md`, `Report/MagicSquare_LayeredDesign_TDD_Report.md`에 적힌 입력·출력 계약, ECB·도메인 서비스 분리 방향과 맞춤.

---

## 5. 검증

- **도구:** Python `yaml.safe_load` (PyYAML).  
- **결과:** 최종 `.cursorrules`는 오류 없이 단일 문서로 로드됨.

---

## 6. 참고 경로

| 항목 | 경로 |
|------|------|
| 규칙 원본 | 저장소 루트 `.cursorrules` |
| 도메인·계약 | `Report/MagicSquare_ProblemDefinition_Report.md`, `Report/MagicSquare_LayeredDesign_TDD_Report.md` |

---

## 7. 후속 제안 (선택)

- 소스 트리가 실제로 생기면 `file_structure.recommended_tree`와 실제 디렉터리를 맞추고, 불일치 시 본 보고서 또는 `.cursorrules`만 갱신하는 절차를 두면 좋다.  
- CI에서 `yamllint` 또는 `yaml.safe_load`를 한 번 돌리면 규칙 파일 회귀를 막기 쉽다.
