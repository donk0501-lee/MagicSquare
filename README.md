# Magic Square (4×4)

TDD·ECB 연습용 프로젝트입니다. **부분적으로 비어 있는 4×4 고전 마방진**(빈칸 `0` 정확히 두 칸, 나머지 1~16·비중복)을 입력으로 받아, PRD에 정한 **두 가지 배치 시도**만으로 완성 격자가 마방진(행·열·두 대각 합 34)인지 판정하고, 성공 시 **`int[6] = [r1,c1,n1,r2,c2,n2]`**(1-index 좌표)를 반환합니다. UI·DB·일반 N×N 확장은 범위 밖입니다.

---

## 문서 관계 한 줄 (`Report/5` 기준)

[`Report/5. PRD_Report.md`](Report/5.%20PRD_Report.md) 서두에 따르면, **요구·검증·구현 To-Do**는 `docs/` 아래 **통합 문서 한 파일**로 관리한다: [`docs/MagicSquare_4x4_TDD.md`](docs/MagicSquare_4x4_TDD.md). `Report/5`는 동일 본문의 **동기 사본**이다.

---

## 단일 진입: 통합 PRD + To-Do (`docs/`)

| 구분 | 문서 | README·To-Do·검증에서의 역할 |
|------|------|------------------------------|
| **요구·FR/BR/NFR·테스트·§12 추적·§13 To-Do** | **[`docs/MagicSquare_4x4_TDD.md`](docs/MagicSquare_4x4_TDD.md)** | `docs/`의 **유일한** 제품·작업 원천(§1~§12 PRD, §13 구현 보드). |
| **스토리·여정·Epic 서술** | [`Report/4. UserJourney_Backlog_Report.md`](Report/4.%20UserJourney_Backlog_Report.md) | 사용자 관점 문장·백로그 톤. |
| **입출력·오류 코드·도메인 API·컴포넌트 표** | [`Report/2. LayeredDesign_TDD_Report.md`](Report/2.%20LayeredDesign_TDD_Report.md) | 계약 세부·`validatePuzzleInput` 등 이름 고정. |
| **실행 도구·커버리지 하한·pytest** | [`pyproject.toml`](pyproject.toml) | `pytest` / `coverage` 기본값(`fail_under=80`). |
| **ECB·RED/GREEN/REFACTOR·금지 패턴·권장 트리** | [`.cursorrules`](.cursorrules) + [`Report/3. CursorRules_WorkReport.md`](Report/3.%20CursorRules_WorkReport.md) | 구현 시 레이어·TDD 위반 경고. |
| **문제 정의·Why** | [`Report/1. ProblemDefinition_Report.md`](Report/1.%20ProblemDefinition_Report.md) | 배경·Invariant 직관. |
| **`docs/` 통합·작업 이력** | [`Report/6. Documentation_Consolidation_WorkReport.md`](Report/6.%20Documentation_Consolidation_WorkReport.md) | PRD·To-Do 단일화 및 참조 갱신 기록. |

---

## 제품 개요 (PRD §1·§2 요약)

- **입력:** 4×4 `int[][]`. `0`은 빈칸(정확히 2개). 그 외 값은 `1..16`, 비0 값은 서로 달라야 함(I1~I4).  
- **처리:** row-major로 첫·둘째 `0` 위치 확정 → 1~16 중 누락 두 수 → (작은 수→첫 빈칸, 큰 수→둘째) 시도 후 FR-04 판정 → 실패 시 역배치 한 번만(BR-12).  
- **출력(성공):** `[r1,c1,n1,r2,c2,n2]`(모두 1-index, `n1`·`n2`는 각 빈칸에 놓인 값).  
- **출력(실패):** 경계에서 PRD §8.1의 `code`·`message`(문자열 **바이트 단위 고정**). 도메인 내부 `NOT_MAGIC`는 `NOT_MAGIC_SQUARE`로 매핑.

---

## 스토리·목표 (`Report/4` 정합)

- **Epic(개념):** Invariant 기반 사고 훈련 — 불변조건을 먼저 정의하고 테스트·구현이 이를 위반하지 않게 한다.  
- **Persona:** TDD·Clean Architecture·ECB를 익히는 **학습자**; 속도보다 계약·회귀·리팩터링 습관이 목표.  
- **User Story ↔ 통합 문서:** [`docs/MagicSquare_4x4_TDD.md`](docs/MagicSquare_4x4_TDD.md) **§13**의 US-001~003이 경계·도메인·품질 축으로 `Report/4`의 Level 2~3 서술과 대응합니다.

---

## 계약·오류 요약 (`Report/2` + PRD §8.1)

| `code` | 대표 조건(요약) | `message`(PRD 고정, 생략 시 PRD 원문 참조) |
|--------|-----------------|---------------------------------------------|
| `SIZE_INVALID` | I1 실패 | `Matrix must be 4x4.` |
| `BLANK_COUNT_INVALID` | I2 실패 | `Exactly two cells must be 0.` |
| `VALUE_OUT_OF_RANGE` | I3 실패 | `Each cell must be 0 or between 1 and 16 inclusive.` |
| `DUPLICATE_NONZERO` | I4 실패 | `Non-zero values must be unique.` |
| `NOT_MAGIC_SQUARE` | 두 배치 모두 비마방진 | `No valid placement completes a 4x4 magic square.` |
| `INTERNAL_ERROR` | 예상 밖 예외 래핑 | `Unexpected error.` |

성공 시 스키마: 길이 6 배열, 좌표 1~4, `n1`≠`n2`, 누락 집합과 일치(`Report/2` Output schema, PRD FR-05).

---

## ECB·실행 환경 (`Report/3` + `pyproject.toml` + `.cursorrules`)

| 레이어 | 책임 | 금지(요지) |
|--------|------|------------|
| **Boundary** | 원시 `int[][]` 입출력, I1~I4 검증, 오류·성공 스키마 | 격자 알고리즘·마방진 판정 직접 구현 금지 |
| **Control** | 검증→빈칸→누락→해결 **호출 순서**만 조율 | 프레임워크·I/O 세부에 묶이지 않음 |
| **Entity / Domain 서비스** | `PuzzleGrid`, `CellIndex`, `PuzzleInputInvariantChecker`, `EmptyCellLocator`, `MissingNumberFinder`, `MagicCompletenessChecker`, `TwoBlankSolutionResolver`, `MagicSquareSpec` 등 순수 규칙 | Boundary·네트워크·파일 참조 금지 |

- **Python:** `pyproject.toml`의 `requires-python`은 **`>=3.10`**(로컬 도구 호환). PRD·`.cursorrules`는 **3.11+ 권장** — 팀·CI는 3.11로 맞추는 것이 좋습니다.  
- **테스트:** `pytest`, AAA, `test_` 접두사(`.cursorrules` `testing`).  
- **커버리지:** `pyproject.toml` `[tool.coverage.report] fail_under = 80`(`.cursorrules` `coverage_minimum`과 정합). PRD **NFR-01·NFR-02**는 각각 도메인 **≥95%**, 경계 **≥85%**이므로, 달성 시 `fail_under` 또는 소스별 게이트를 상향하는 것을 권장합니다.

---

## 검증 기준 ([`docs/MagicSquare_4x4_TDD.md`](docs/MagicSquare_4x4_TDD.md)에서의 “완료”)

### 기능(FR) 체크리스트

- [ ] **FR-01** 입력 검증(I1~I4) 및 위반 시 §8.1 코드·메시지·탐지 순서 §11.  
- [ ] **FR-02** row-major 두 빈칸 1-index, M1/M2 AC.  
- [ ] **FR-03** 누락 두 수, M1 {3,5}, M2 {1,6}.  
- [ ] **FR-04** 완전 격자에 대해 10선 합 34 `boolean`, FR-04 AC 부정 케이스.  
- [ ] **FR-05** 두 시도·BR-10~14·골든 `int[6]`·실패 `NOT_MAGIC_SQUARE`·시도1 성공 시 시도2 미실행.

### 비기능(NFR)

- [ ] **NFR-01** Domain logic 커버리지 ≥ **95%**.  
- [ ] **NFR-02** Boundary 커버리지 ≥ **85%**.  
- [ ] **NFR-03** 동일 입력 동일 성공/실패 코드(결정론).  
- [ ] **NFR-04** 호출자 `int[][]` 비변조(복사본에서 해결).  
- [ ] **NFR-05** 매직 넘버 산재 금지(스펙·상수 집약).

### 계약 테스트 ID(최소)

- [ ] **U-01~U-09** (PRD §8.1, Track A).  
- [ ] **T-01~T-05** (PRD §9.2).  
- [ ] 도메인 단위: PRD §8.2 및 `Report/2` §1.5 D-01~D-17에 대응하는 분기.

### 골든 데이터(묵시 변경 금지, PRD §9.1)

- **M1** → `[1,2,3,2,1,5]`  
- **M2** → `[3,3,6,4,4,1]`

---

## 구현 To-Do (요약 — 상세는 통합 문서 §13)

전체 표(**TASK-001~TASK-033**, RED/GREEN/REFACTOR, Scenario, Test, Code, ECB)는 **[`docs/MagicSquare_4x4_TDD.md`](docs/MagicSquare_4x4_TDD.md) §13**에 있다.

### Epic / User Story

- [ ] **Epic-001** — §5~§7 FR·BR·NFR, §8·§9, §12 추적 충족.  
- [ ] **US-001** — 경계 거절 경로(FR-01, U-01~U-07).  
- [ ] **US-002** — 도메인 해 결정(FR-02~FR-05, T-01·T-02·T-05).  
- [ ] **US-003** — 통합·커버리지·스타일·ECB(`Report/3`, `pyproject.toml`, `.cursorrules`).

### Phase별 Task (상세는 통합 문서 §13.3 표 참조)

- [ ] **Phase 0** TASK-001 ~ TASK-003 — 스캐폴딩·추적.  
- [ ] **Phase 1** TASK-004 ~ TASK-006 — `MagicSquareSpec`·`PuzzleGrid`.  
- [ ] **Phase 2** TASK-007 ~ TASK-009 — Dual-Track RED(도메인 검증 + Boundary U-01~U-07).  
- [ ] **Phase 3** TASK-010 ~ TASK-011 — FR-01 Domain GREEN/REFACTOR.  
- [ ] **Phase 4** TASK-012 ~ TASK-013 — Boundary 오류 매핑.  
- [ ] **Phase 5** TASK-014 ~ TASK-015 — FR-02 빈칸.  
- [ ] **Phase 6** TASK-016 ~ TASK-017 — FR-03 누락 두 수.  
- [ ] **Phase 7** TASK-018 ~ TASK-019 — FR-04 마방진 판정.  
- [ ] **Phase 8** TASK-020 ~ TASK-023 — FR-05 해결·`NOT_MAGIC`.  
- [ ] **Phase 9** TASK-024 ~ TASK-026 — Control·포트·U-08.  
- [ ] **Phase 10** TASK-027 ~ TASK-028 — 실도메인 E2E·출력 스키마.  
- [ ] **Phase 11** TASK-029 ~ TASK-033 — Property·NFR-04·REFACTOR·커버리지·정적 분석.

---

## 로컬 실행

```powershell
cd C:\DEV\MagicSquare
python -m pip install -e ".[dev]"
python -m pytest
python -m pytest --cov=magic_square --cov-report=term-missing
```

**GUI(공식 진입점 한 줄):** PyQt6 설치 후 `python -m magic_square` 로 4×4 입력·「풀기」·결과 표시 창을 띄웁니다.

```powershell
python -m pip install -e ".[dev,gui]"
python -m magic_square
```

소스는 [`src/magic_square/`](src/magic_square/) 패키지, 테스트는 [`tests/`](tests/)를 사용합니다(ECB 세분화는 구현 진행에 따라 추가). Qt 의존 코드는 [`src/magic_square/gui/`](src/magic_square/gui/) 에만 둡니다.

---

## 라이선스

미정 — 저장소 정책에 따릅니다.
