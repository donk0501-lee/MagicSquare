"""Track A — Boundary(UI) RED (docs/MagicSquare_4x4_TDD.md §8.1, Formal_Test_Cases D/E).

현재 `solve_two_blank_magic_square`는 GREEN 전까지 NotImplementedError이므로,
`pytest.raises(MagicSquareContractError)` 기대 테스트는 **예외 타입 불일치로 실패(RED)** 하고,
성공 경로 단언은 **NotImplementedError로 실패(RED)** 한다.
"""

from __future__ import annotations

import pytest

from magic_square.boundary import solve_two_blank_magic_square
from magic_square.errors import MagicSquareContractError
from tests.prd_constants import (
    CODE_BLANK_COUNT_INVALID,
    CODE_DUPLICATE_NONZERO,
    CODE_SIZE_INVALID,
    CODE_VALUE_OUT_OF_RANGE,
    MSG_BLANK_COUNT_INVALID,
    MSG_DUPLICATE_NONZERO,
    MSG_SIZE_INVALID,
    MSG_VALUE_OUT_OF_RANGE,
)

# §9.1 M1 — FR-01 통과 골든 입력
M1 = [
    [16, 0, 2, 13],
    [0, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_UI_RED_01_non_4x4_matrix_raises_size_invalid() -> None:
    """U-01 / FTC-MS-D-003: 비 4×4 입력은 SIZE_INVALID + 고정 message.

    Given: 3행×4열 구조.
    When: solve_two_blank_magic_square 호출.
    Then: MagicSquareContractError, code·message PRD 고정값.
    계약: I1(4×4) — 외곽 크기 불변.
    """
    matrix_3x4 = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
    with pytest.raises(MagicSquareContractError) as excinfo:
        solve_two_blank_magic_square(matrix_3x4)
    assert excinfo.value.code == CODE_SIZE_INVALID
    assert excinfo.value.message == MSG_SIZE_INVALID


def test_UI_RED_02_blank_count_not_two_raises_blank_count_invalid() -> None:
    """U-03 / FTC-MS-A-004: 빈칸(0)이 2개가 아니면 BLANK_COUNT_INVALID.

    Given: 4×4이나 0이 정확히 1개.
    When: solve_two_blank_magic_square 호출.
    Then: MagicSquareContractError + PRD 고정 message.
    계약: I2 — 빈칸 개수 불변.
    """
    one_blank = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]
    with pytest.raises(MagicSquareContractError) as excinfo:
        solve_two_blank_magic_square(one_blank)
    assert excinfo.value.code == CODE_BLANK_COUNT_INVALID
    assert excinfo.value.message == MSG_BLANK_COUNT_INVALID


def test_UI_RED_03_value_out_of_range_raises() -> None:
    """U-05 / FTC-MS-D-001: 1~16 밖 값은 VALUE_OUT_OF_RANGE.

    Given: 4×4, 0 두 개, 단 하나의 셀이 17.
    When: solve_two_blank_magic_square 호출.
    Then: MagicSquareContractError + PRD 고정 message.
    계약: I3 — 셀 값 도메인(0 또는 1~16).
    """
    has_17 = [
        [16, 0, 2, 13],
        [0, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 17],
    ]
    with pytest.raises(MagicSquareContractError) as excinfo:
        solve_two_blank_magic_square(has_17)
    assert excinfo.value.code == CODE_VALUE_OUT_OF_RANGE
    assert excinfo.value.message == MSG_VALUE_OUT_OF_RANGE


def test_UI_RED_04_duplicate_nonzero_raises() -> None:
    """U-07 / FTC-MS-D-002: 비0 중복은 DUPLICATE_NONZERO.

    Given: 4×4, 0 두 개, 동일 비0 값 2회 이상.
    When: solve_two_blank_magic_square 호출.
    Then: MagicSquareContractError + PRD 고정 message.
    계약: I4 — 비0 유일성.
    """
    dup = [
        [16, 0, 2, 13],
        [0, 5, 11, 8],
        [9, 5, 7, 12],
        [4, 15, 14, 1],
    ]
    with pytest.raises(MagicSquareContractError) as excinfo:
        solve_two_blank_magic_square(dup)
    assert excinfo.value.code == CODE_DUPLICATE_NONZERO
    assert excinfo.value.message == MSG_DUPLICATE_NONZERO


def test_UI_RED_05_success_returns_length_six() -> None:
    """U-08 / 성공 경로: 반환은 길이 6의 int 시퀀스.

    Given: FR-01 통과 골든 M1.
    When: solve_two_blank_magic_square(M1).
    Then: len(result) == 6.
    계약: FR-05 / BR-14 — 성공 출력 스키마 int[6].
    """
    result = solve_two_blank_magic_square(M1)
    assert len(result) == 6


def test_UI_RED_06_success_coords_are_one_indexed() -> None:
    """BR-06 / U-08: 성공 시 좌표는 1-index이며 1~4 범위.

    Given: FR-01 통과 골든 M1.
    When: solve_two_blank_magic_square(M1).
    Then: r1,c1,r2,c2 ∈ [1,4] 및 기대 골든 [1,2,3,2,1,5].
    계약: BR-06, FR-05 좌표 의미.
    """
    result = solve_two_blank_magic_square(M1)
    r1, c1, _n1, r2, c2, _n2 = result
    for x in (r1, c1, r2, c2):
        assert 1 <= x <= 4
    assert result == [1, 2, 3, 2, 1, 5]
