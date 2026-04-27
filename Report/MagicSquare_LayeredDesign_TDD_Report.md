# 4×4 Magic Square — Logic / UI Boundary / Data Layer 설계 보고서

**문서 목적:** Dual-Track UI + Logic TDD 및 Clean Architecture 관점에서 레이어 분리·계약 기반 테스트·통합 검증 계획을 한곳에 보존한다.  
**범위:** 도메인 설계, UI 경계 계약, Data 저장/로드 계약, 단위·통합 테스트 설계, Traceability Matrix.  
**비범위:** 구현 소스 코드, 실제 화면 UI, DB 스키마.

**작성 기준일:** 2026-04-27  

**입력 계약 (고정):**

- `4x4 int[][]` (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지

**출력 계약 (고정):**

- `int[6]`
- 좌표는 1-index
- 반환 형식: `[r1,c1,n1,r2,c2,n2]`
- `n1`, `n2`는 두 누락 숫자이며, (작은수→첫 빈칸, 큰수→둘째 빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

---

## 목차

1. [Logic Layer (Domain Layer)](#1-logic-layer-domain-layer-설계)
2. [Screen Layer (UI Boundary)](#2-screen-layer-ui-layer-설계-boundary-layer)
3. [Data Layer](#3-data-layer-설계)
4. [Integration & Verification](#4-integration--verification)

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

| 구분 | 이름 | 책임 (SRP) |
|------|------|------------|
| Value Object | `PuzzleGrid` (또는 동등 개념) | 4×4 정수 격자를 값으로 캡슐화. “검증된 퍼즐 상태”와 “임의 배열”을 구분할지는 설계 선택(API와 정합). |
| Value Object | `CellIndex` | 1-index 행·열. 출력 계약과 동일한 좌표 체계만 표현. |
| Value Object | `MissingNumberPair` | 누락된 두 정수 집합 {a,b} (순서 없음). |
| Value Object | `PlacementOrder` | (첫 빈칸에 들어갈 수, 둘째 빈칸에 들어갈 수)의 순서 결정 규칙을 캡슐화. |
| Entity (선택) | `MagicSquareSpec` | 4×4·1~16·매직 상수 34·검사할 선(행/열/주대각 2개) 정의. 한 곳에만 “규칙 상수”를 둠. |
| Domain Service | `PuzzleInputInvariantChecker` | 입력 불변조건: 크기 4×4, 0 정확히 2개, 값 0 또는 1~16, 0 제외 중복 없음. |
| Domain Service | `EmptyCellLocator` | 값이 0인 칸의 좌표를 정확히 2개 반환(전제: 이미 검증됨). |
| Domain Service | `MissingNumberFinder` | 1~16 중 격자에 없는 두 수 찾기. |
| Domain Service | `MagicCompletenessChecker` | **모든 칸이 비0**인 완성 격자에 대해 행/열/두 대각선 합이 매직 상수와 일치하는지 판정. |
| Domain Service | `TwoBlankSolutionResolver` | 두 빈칸에 (n_small→첫 빈칸, n_large→둘째 빈칸) 및 반대 배치를 시도하고, 출력 순서 규칙에 맞는 `int[6]` 결정. |

**역할 분리 요약:** “입력이 유효한가” / “빈칸·누락수는 무엇인가” / “완성 시 마방진인가” / “출력 순서는 무엇인가”를 서로 다른 컴포넌트로 나누면 단위 테스트가 각 불변조건에 매핑되기 쉽다.

## 1.2 도메인 불변조건 (Invariants)

| ID | 불변조건 | 검증 가능 규칙(명시) |
|----|-----------|----------------------|
| I1 | 격자 크기는 4×4 | 행 개수=4, 각 행 길이=4 |
| I2 | 0인 칸은 정확히 2개 | `count(0)==2` |
| I3 | 모든 값은 `0` 또는 `1≤v≤16` | 각 셀에 대해 `v==0 \|\| (1≤v≤16)` |
| I4 | 0을 제외한 값은 서로 다름 | 비0 값 집합 크기 = 비0 셀 개수 (=14) |
| I5 | (도메인 해석) 완성 격자에서 사용 숫자는 1~16 각 1회 | 퍼즐 입력이 I1~I4를 만족하면 “누락 2수를 채우면” 1~16 완전 사용이 됨을 별도 정리 가능 |
| I6 | 마방진 완성 조건(4×4 고전 마방진) | 4개 행 합=34, 4개 열 합=34, 주대각 합=34, 부대각 합=34 |
| I7 | 매직 상수 | 4×4·1~16일 때 상수 `M=34` (정의: `M = n(n²+1)/2`, n=4) |

**범위 고정:** “반마방진” 등 다른 정의는 본 프로젝트 범위에서 제외하고, I6만 계약에 포함한다.

## 1.3 핵심 유스케이스 (도메인 관점)

| 유스케이스 | 입력(도메인) | 출력 | 실패 의미 |
|------------|--------------|------|-----------|
| UC-A | 원시 4×4 배열 | 검증 통과 시 `PuzzleGrid` 등 | I1~I4 위반 |
| UC-B | 검증된 퍼즐 | 빈칸 2개의 `CellIndex` | (정상 전제하에 실패 없음; 전제 위반 시는 UC-A 실패로 흡수 가능) |
| UC-C | 검증된 퍼즐 | 누락 두 수 `{a,b}` | 1~16 집합과 불일치 시(입력 오류면 UC-A에서 차단) |
| UC-D | 완성 격자(0 없음) | 마방진 여부 `boolean` | I6 위반 시 `false` |
| UC-E | 검증된 퍼즐 | `int[6]` `[r1,c1,n1,r2,c2,n2]` | 두 배치 모두 마방진이 아니면 “해 없음”으로 규약 필요(아래 실패조건) |

**출력 순서 규칙 (도메인 문장화):**  
빈칸을 “첫 빈칸(탐색 순서로 앞선 0)”, “둘째 빈칸”으로 고정한다. 누락 두 수를 `n_small ≤ n_large`로 둔다.

- 배치 A: 첫 빈칸←`n_small`, 둘째 빈칸←`n_large`로 채운 완성 격자가 UC-D에서 참이면 출력은 `(n1,n2)=(n_small,n_large)`.
- 그렇지 않고 배치 B: 첫 빈칸←`n_large`, 둘째 빈칸←`n_small`이 참이면 출력은 `(n1,n2)=(n_large,n_small)`.
- 둘 다 참이면 계약을 하나로 고정해야 한다: 예) “배치 A를 우선” 또는 “배치 B를 우선” 중 **한 문장으로만** 선택해 테스트에 박제한다.
- 둘 다 거짓이면 UC-E 실패.

**빈칸 “탐색 순서” 고정 규칙 (검증 가능):** 행 우선, 행 번호 오름차순, 열 번호 오름차순으로 처음 만나는 0이 “첫 빈칸”, 그다음 0이 “둘째 빈칸”. 이 규칙을 문서·테스트에 명시한다.

## 1.4 Domain API (내부 계약)

구현 코드 없이 **메서드 수준**만 기술한다. 반환은 의사형 `Result<Ok,Err>` 등으로만 표현한다.

| API | 입력 | 출력 | 실패조건 |
|-----|------|------|----------|
| `validatePuzzleInput(raw4x4)` | `int[][]` | `Ok` 또는 `Err(ValidationFailure)` | I1~I4 중 하나라도 거짓 |
| `locateTwoBlanks(validPuzzle)` | 검증된 퍼즐 | `Ok( (CellIndex first, CellIndex second) )` | 0이 2개가 아니면 Err(내부 불일치) — 정상 경로에서는 상위에서 보장 |
| `findMissingTwoNumbers(validPuzzle)` | 검증된 퍼즐 | `Ok( MissingNumberPair {a,b} )` | {1..16}과 multiset 불일치 시 Err |
| `magicConstantFor4x4()` | 없음 | `34` | 없음 |
| `isMagicSquareComplete(filled4x4)` | 0 없는 4×4, 값 1~16 | `boolean` | 부동소수 없음; 합만 비교 |
| `resolveTwoBlankMagicOutput(validPuzzle)` | 검증된 퍼즐 | `Ok(int[6])` | 두 배치 모두 `isMagicSquareComplete==false`이면 Err(Unsolvable) |
| (선택) `tryAssign(firstBlank, secondBlank, nFirst, nSecond, basePuzzle)` | 좌표 2개, 수 2개, 퍼즐 | 완성 격자 | 좌표가 0이 아니면 Err |

**실패 타입 분류 (도메인):**

| 실패 코드 | 의미 | 발생 조건 |
|-----------|------|-----------|
| `INVALID_INPUT` | 퍼즐 입력 불변 위반 | I1~I4 |
| `NOT_MAGIC` | 해 없음 | 두 배치 모두 비마방진 |
| `INTERNAL_INVARIANT_BROKEN` | 버그/전제 파기 | 예: 검증 없이 resolve 호출 |

## 1.5 Domain 단위 테스트 설계 (RED 우선)

### 테스트 케이스 목록

| ID | 유형 | 설명 | 기대 |
|----|------|------|------|
| D-01 | 정상 | 알려진 완성 4×4 마방진에서 임의 두 칸을 0으로 바꾼 뒤, 누락 수·좌표·출력 순서가 규칙과 일치 | `int[6]` 고정 기대값(골든) |
| D-02 | 정상 | D-01과 다른 또 하나의 골든 퍼즐(서로 다른 빈칸 패턴) | 고정 기대값 |
| D-03 | 정상 | `n_small→첫`, `n_large→둘째`가 마방진인 경우 | `(n1,n2)=(n_small,n_large)` |
| D-04 | 정상 | 위가 아니고 반대만 마방진인 경우 | `(n1,n2)=(n_large,n_small)` |
| D-05 | 엣지 | 두 배치 모두 마방진이면 | **문서에서 고정한 타이브레이크**와 동일 |
| D-06 | 비정상 | 크기 3×4 | `INVALID_INPUT` |
| D-07 | 비정상 | 0이 1개만 | `INVALID_INPUT` |
| D-08 | 비정상 | 0이 3개 | `INVALID_INPUT` |
| D-09 | 비정상 | 값 17 포함 | `INVALID_INPUT` |
| D-10 | 비정상 | 음수 포함 | `INVALID_INPUT` |
| D-11 | 비정상 | 비0 중복 | `INVALID_INPUT` |
| D-12 | 비정상 | 마방진으로 완성 불가능한 퍼즐 | `NOT_MAGIC` |
| D-13 | 단위 | `isMagicSquareComplete`만: 한 행 합만 틀린 완성 격자 | `false` |
| D-14 | 단위 | `isMagicSquareComplete`: 한 열만 틀림 | `false` |
| D-15 | 단위 | `isMagicSquareComplete`: 주대각만 틀림 | `false` |
| D-16 | 단위 | `isMagicSquareComplete`: 부대각만 틀림 | `false` |
| D-17 | 단위 | `locateTwoBlanks` 행우선 순서 | 첫/둘째 빈칸 좌표가 스펙과 동일 |

### 테스트 ↔ Invariant 매핑

| 테스트 | 보호하는 Invariant |
|---------|-------------------|
| D-06~D-11 | I1~I4 |
| D-13~D-16 | I6 (및 I7를 이용한 판정) |
| D-01~D-05, D-12 | I6 + 출력 순서 규칙 + 빈칸 순서 규칙 |
| D-17 | 빈칸 순서 고정 규칙(출력 계약과 연동) |

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 관점 시나리오

| 단계 | 행위 | 경계 책임 |
|------|------|-----------|
| S1 | 호출자가 4×4 행렬을 경계에 전달 | 원시 입력 수용 |
| S2 | 경계가 스키마 검증 | UI 계약의 Error schema로 거절 가능 |
| S3 | 검증 통과 시 Domain API 호출 | Domain은 Mock 가능한 포트 뒤에 둠 |
| S4 | Domain `Ok` 시 `int[6]`을 Output schema로 반환 | 길이·타입·좌표 1-index 검증 |
| S5 | Domain `Err` 시 Error schema로 매핑 | 문구·코드 고정 |

## 2.2 UI 계약 (외부 계약)

### Input schema

| 필드 | 타입 | 제약 |
|------|------|------|
| `matrix` | `int[][]` | 길이 4; 각 행 길이 4 |
| 셀 값 | `int` | `0` 또는 `1≤v≤16` |
| 0의 개수 | 카운트 | 정확히 2 |
| 비0 유일성 | multiset | 비0 14개는 서로 다름 |

### Output schema (성공)

| 필드 | 타입 | 제약 |
|------|------|------|
| 반환값 | `int[6]` | 정확히 6원소 |
| `r1,c1,r2,c2` | `int` | 각각 1~4 (1-index, 4×4 경계) |
| `n1,n2` | `int` | 1~16, 서로 다름, 퍼즐 누락 두 수와 집합 일치 |
| 의미 | 고정 | `(r1,c1)`=첫 빈칸, `(r2,c2)`=둘째 빈칸; `(n1,n2)`는 문제에서 정한 마방진 성립 순서 |

### Error schema

| 필드 | 타입 | 제약 |
|------|------|------|
| `code` | enum 문자열 | 아래 표의 코드 집합만 허용 |
| `message` | string | 아래 “정확한 문구”와 **바이트 단위 동일** (학습용 고정) |

**Error code 목록**

| code | 발생 조건 (검증 규칙) |
|------|-------------------------|
| `SIZE_INVALID` | I1 실패 |
| `BLANK_COUNT_INVALID` | I2 실패 |
| `VALUE_OUT_OF_RANGE` | I3 실패 |
| `DUPLICATE_NONZERO` | I4 실패 |
| `NOT_MAGIC_SQUARE` | 도메인 `NOT_MAGIC` |
| `INTERNAL_ERROR` | 예상치 못한 예외 래핑(경계 최후단; 테스트에서는 호출하지 않음) |

## 2.3 UI 레벨 테스트 (Contract-first, RED 우선)

**전제:** Domain 포트는 Mock. Mock은 “성공 시 고정 `int[6]` 반환”, “실패 시 도메인 에러 반환”만 구성한다.

| ID | 목적 | 설정 | 기대 |
|----|------|------|------|
| U-01 | 크기 오류 | `int[3][4]` | `SIZE_INVALID` + 고정 message |
| U-02 | 가변 행 길이 | 행 하나만 길이 3 | `SIZE_INVALID` |
| U-03 | 빈칸 1개 | 0 한 개만 | `BLANK_COUNT_INVALID` |
| U-04 | 빈칸 3개 | 0 세 개 | `BLANK_COUNT_INVALID` |
| U-05 | 범위 초과 | 17 | `VALUE_OUT_OF_RANGE` |
| U-06 | 범위 미만 | -1 | `VALUE_OUT_OF_RANGE` |
| U-07 | 중복 | 비0 동일 값 2회 | `DUPLICATE_NONZERO` |
| U-08 | 정상 통과 | 유효 입력 + Mock 성공 | 반환 배열 길이 6, Mock이 준 값과 동일 |
| U-09 | Domain 실패 전달 | 유효 입력 + Mock `NOT_MAGIC` | `NOT_MAGIC_SQUARE` + 고정 message |
| U-10 | 출력 포맷 검증 | Mock이 잘못된 길이 반환하도록 악의적 테스트 더블 | 경계에서 거절 또는 `INTERNAL_ERROR` — **한 가지로만** 문서화 |

### UI 테스트 완료 체크리스트

- [ ] 다섯 가지 입력 오류 코드 각각 최소 1 테스트
- [ ] 성공 시 배열 길이 6 및 좌표 범위 1~4
- [ ] Domain Mock 교체로 `NOT_MAGIC` 매핑 검증
- [ ] 에러 시 `message`가 스펙 문자열과 완전 일치

## 2.4 UX/출력 규칙 (에러 메시지 표준)

아래 문구는 **그대로** 사용한다고 가정한다(줄바꿈 없음, 마침표 포함 여부까지 통일).

| code | message (정확 문자열) |
|------|------------------------|
| `SIZE_INVALID` | `Matrix must be 4x4.` |
| `BLANK_COUNT_INVALID` | `Exactly two cells must be 0.` |
| `VALUE_OUT_OF_RANGE` | `Each cell must be 0 or between 1 and 16 inclusive.` |
| `DUPLICATE_NONZERO` | `Non-zero values must be unique.` |
| `NOT_MAGIC_SQUARE` | `No valid placement completes a 4x4 magic square.` |
| `INTERNAL_ERROR` | `Unexpected error.` |

성공 시 문자열 메시지는 필수 아님(API는 `int[6]`만 반환). CLI 래퍼를 추가한다면 출력 형식은 별도 CLI 계약으로 문서화한다.

---

# 3) Data Layer 설계

## 3.1 목적 정의

| 항목 | 내용 |
|------|------|
| 목적 | TDD로 “도메인과 무관한 영속성 경계”를 두고, 동일 유스케이스를 메모리/파일로 교체하며 검증 |
| 범위 | DB 없음. “마지막 퍼즐”, “마지막 결과” 정도의 단순 스냅샷 저장 |
| 비범위 | 동시성, 버전 마이그레이션, 암호화 |

## 3.2 인터페이스 계약

| 메서드 | 입력 | 출력 | 실패 |
|--------|------|------|------|
| `savePuzzleSnapshot(id, matrix4x4)` | 문자열 id, 입력과 동형 `int[][]` | `Ok` | 디스크 풀/권한 등은 File 구현에서만 |
| `loadPuzzleSnapshot(id)` | id | `Ok(int[][])` | 스냅샷 없음 |
| `saveLastResult(id, result6)` | id, `int[6]` | `Ok` | 선택 기능이면 생략 가능 |
| `loadLastResult(id)` | id | `Ok(int[6])` | 없음 |

**저장 스냅샷 불변:** 로드된 `int[][]`는 다시 `validatePuzzleInput`을 통과해야 함(데이터 손상 방지).

## 3.3 구현 옵션 비교

| 기준 | 옵션 A: InMemory | 옵션 B: File (JSON) |
|------|------------------|---------------------|
| 테스트 속도 | 빠름 | 상대적으로 느림 |
| 파일 없음/형식 오류 | 해당 없음 | 명시적 실패 경로 필요 |
| 학습 목표(교체 가능성) | 낮음 | 높음 |
| CSV 대비 | - | 필드명으로 스키마 명확(JSON 우위) |

**추천:** **옵션 B (File JSON)**  
**이유:** “메모리/파일 교체” 학습 목표를 한 번에 만족하고, 스키마를 계약 테스트로 고정하기 쉬우며, InMemory는 테스트 더블로 이미 대체 가능해 프로덕션 형태의 두 번째 구현이 File이면 통합 테스트 가치가 크다.

## 3.4 Data 레이어 테스트

| ID | 시나리오 | 기대 |
|----|----------|------|
| DA-01 | save 후 load | `equals`로 4×4 동일 |
| DA-02 | 존재하지 않는 id load | 명시된 에러(예: `SnapshotNotFound`) |
| DA-03 | 손상 JSON load | 파싱 실패 에러 |
| DA-04 | JSON이 3×3 | 로드 후 검증에서 실패하거나 로드 단계에서 스키마 거절 — **한 규약으로만** 고정 |
| DA-05 | save 결과 후 load | `int[6]` 동일 |
| DA-06 | 불변: 로드된 퍼즐이 4×4 아님 | 저장 금지 또는 로드 거절 중 택일을 문서에 하나만 기술 |

---

# 4) Integration & Verification

## 4.1 통합 경로 정의

```
[Caller]
   → UI Boundary (validate + map errors)
        → Application Service (선택: 오케스트레이션만)
             → Domain (validate → locate → missing → resolve)
        ↔ Data (선택: load snapshot → feed boundary → save result)
```

| 의존성 방향 | 규칙 |
|-------------|------|
| UI → Domain | 인터페이스(포트) 경유; Domain은 UI 모름 |
| Application → Domain | 유스케이스 조합만 |
| Data → Domain | **직접 의존 금지**; 원시 배열/JSON만 다루고 검증은 UI 또는 Application에서 Domain API로 |

## 4.2 통합 테스트 시나리오

### 정상 (2개 이상)

| ID | 흐름 | 검증 포인트 |
|----|------|----------------|
| IT-01 | FileRepo 비우기 → 유효 퍼즐 save → load → solve → `int[6]` 골든 | end-to-end + 저장 정합성 |
| IT-02 | 유효 퍼즐 직접 solve(Repo 미사용) | Domain+Boundary 실구현 경로 |

### 실패 (3개 이상)

| ID | 흐름 | 검증 포인트 |
|----|------|----------------|
| IT-F01 | 변형 크기 입력 | UI 에러 `SIZE_INVALID` + 고정 message |
| IT-F02 | 유효 입력이지만 해 없음 | `NOT_MAGIC_SQUARE` + 고정 message |
| IT-F03 | 손상 파일 로드 후 solve 시도 | Data 에러 또는 상위에서 거절 — 사전에 택일한 규약 |

## 4.3 회귀 보호 규칙

| 규칙 | 내용 |
|------|------|
| R1 | `int[6]` 출력 형식과 1-index 좌표 의미 변경 금지 |
| R2 | 공개 Error `code`·`message` 문자열 변경 시 **의도적 버전 업**만 허용(회귀 테스트가 깨지면 변경 거절) |
| R3 | 골든 퍼즐/골든 출력 데이터는 파일 또는 테스트 픽스처로 고정하고 삭제 금지 |
| R4 | Domain 테스트는 Application 추가로 인한 간접 호출로 대체하지 않음(피라미드 유지) |

## 4.4 커버리지 목표

| 레이어 | 목표 |
|--------|------|
| Domain Logic | 분기·조합·판정 전부 포함 ≥ **95%** |
| UI Boundary | 모든 error code 경로 + 성공 ≥ **85%** |
| Data | save/load/손상/없음 ≥ **80%** |

**권장:** 도구상 라인 커버리지 vs 브랜치 커버리지 중 하나를 프로젝트에서 고정(예: 브랜치 커버리지 기준).

## 4.5 Traceability Matrix (필수)

| Concept (Invariant) | Rule (검증 가능) | Use Case | Contract (위치) | Test IDs | Component |
|---------------------|------------------|----------|-------------------|----------|-----------|
| I1 4×4 | 행=4, 열=4 | UC-A | Input schema | D-06, U-01, U-02, IT-F01 | PuzzleInputInvariantChecker, UI |
| I2 0 두 개 | count(0)=2 | UC-A | Input schema | D-07~D-08, U-03~U-04 | PuzzleInputInvariantChecker, UI |
| I3 0 또는 1~16 | 셀 단위 범위 | UC-A | Input schema | D-09~D-10, U-05~U-06 | PuzzleInputInvariantChecker, UI |
| I4 비0 유일 | multiset 유일 | UC-A | Input schema | D-11, U-07 | PuzzleInputInvariantChecker, UI |
| I7 M=34 | 상수 정의 | UC-D | Domain API | (D-13~16에 포함) | MagicSquareSpec |
| I6 마방진 합 | 10선 합=M | UC-D, UC-E | Domain API + Output 의미 | D-01~05, D-12~16, IT-01~02 | MagicCompletenessChecker, TwoBlankSolutionResolver |
| 빈칸 순서 | 행우선 규칙 | UC-B, UC-E | Output 좌표 의미 | D-17, U-08 | EmptyCellLocator |
| 출력 (n1,n2) 순서 | 작은수/큰수 규칙 | UC-E | Output schema | D-03~D-05 | TwoBlankSolutionResolver |
| 영속 스냅샷 | save=load | 저장 유스케이스 | Data API | DA-01, IT-01 | MatrixRepository(File) |
| 오류 문구 고정 | message 동일 | UC-A 실패, UC-E 실패 | Error schema | U-01~07, U-09, IT-F01~F02 | UI Boundary |

---

## 부록: 모호성 제거 체크리스트

| 항목 | 고정한 결정 |
|------|-------------|
| 마방진 정의 | 4행+4열+2대각, 합=34 |
| 빈칸 “첫/둘” | 행 우선, (r,c) 오름차순 첫 두 개의 0 |
| 동시에 두 배치가 마방진 | 타이브레이크 한 줄로 문서화 후 D-05로 박제 |
| 손상 데이터 | Data에서 거절 vs 로드 후 Domain에서 거절 중 **하나만** 채택 |

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| 문제 정의 리포트 | `Report/MagicSquare_ProblemDefinition_Report.md` |
| 본 설계·TDD·통합 계획 | `Report/MagicSquare_LayeredDesign_TDD_Report.md` (본 문서) |
