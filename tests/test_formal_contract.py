"""Formal_Test_Cases.md FTC-MS-* 및 PRD §11·U-09·NFR-04 회귀."""

from __future__ import annotations

import copy

import pytest

from magic_square.boundary import solve_two_blank_magic_square, validate_two_blank_magic_square
from magic_square.constants import MAGIC_SUM, MATRIX_SIZE
from magic_square.errors import MagicSquareContractError
from magic_square.logic import find_blank_coords, is_magic_square, solution
from tests.prd_constants import (
    CODE_BLANK_COUNT_INVALID,
    CODE_DUPLICATE_NONZERO,
    CODE_INTERNAL_ERROR,
    CODE_NOT_MAGIC_SQUARE,
    CODE_SIZE_INVALID,
    CODE_VALUE_OUT_OF_RANGE,
    MSG_BLANK_COUNT_INVALID,
    MSG_DUPLICATE_NONZERO,
    MSG_INTERNAL_ERROR,
    MSG_NOT_MAGIC_SQUARE,
    MSG_SIZE_INVALID,
    MSG_VALUE_OUT_OF_RANGE,
)

# --- §2.1 A (빈칸) ---
GRID_A002 = [
    [0, 2, 3, 13],
    [5, 11, 10, 4],
    [9, 7, 6, 12],
    [14, 15, 1, 0],
]

COMPLETE_MAGIC = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

GRID_A001 = [
    [16, 2, 3, 13],
    [5, 11, 10, 0],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

THREE_BLANKS_AND_17 = [
    [0, 2, 3, 13],
    [0, 11, 10, 8],
    [0, 7, 6, 12],
    [4, 15, 14, 17],
]

THREE_BLANKS = [
    [0, 0, 2, 13],
    [0, 11, 10, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# --- §2.2 B (마방진 판정) ---
B002_ROW2_BROKEN = [
    [16, 2, 3, 13],
    [5, 11, 10, 9],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

B003_COL4_BROKEN = [
    [16, 2, 3, 13],
    [8, 11, 10, 5],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

B004_MAIN_DIAG_BROKEN = [
    [2, 16, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

# FTC-MS-B-005: 엑셀 생략 — 부대각만 깨진 정수 4×4(타 9선 34)는 제약상 구하기 어려워
# FR-04 부정 회귀는 아래와 동등하게 `is_magic_square is False` 로 고정한다.
B005_ANTI_FOCUS_FALSE = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 2],
]

# --- §2.3 C ---
PUZZLE_C005_16_IN_OUTPUT = [
    [0, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

T05_DOUBLE_FAIL = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 0, 0],
]

M1 = [
    [16, 0, 2, 13],
    [0, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_FTC_MS_A002_blank_coords() -> None:
    assert find_blank_coords(GRID_A002) == [(1, 1), (4, 4)]


def test_FTC_MS_A003_complete_grid_blank_count_boundary() -> None:
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(COMPLETE_MAGIC)
    assert ei.value.code == CODE_BLANK_COUNT_INVALID
    assert ei.value.message == MSG_BLANK_COUNT_INVALID


def test_FTC_MS_A005_three_blanks_boundary() -> None:
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(THREE_BLANKS)
    assert ei.value.code == CODE_BLANK_COUNT_INVALID


@pytest.mark.parametrize(
    "grid,ftc",
    [
        (B002_ROW2_BROKEN, "FTC-MS-B-002"),
        (B003_COL4_BROKEN, "FTC-MS-B-003"),
        (B004_MAIN_DIAG_BROKEN, "FTC-MS-B-004"),
        (B005_ANTI_FOCUS_FALSE, "FTC-MS-B-005"),
    ],
)
def test_FTC_MS_B002_B005_is_magic_false(grid: list[list[int]], ftc: str) -> None:
    _ = ftc
    assert is_magic_square(grid) is False


def test_FTC_MS_B001_complete_magic_true() -> None:
    assert is_magic_square(COMPLETE_MAGIC) is True


def test_FTC_MS_C001_solve_grid_a001() -> None:
    assert solution(GRID_A001) == [2, 4, 8, 4, 4, 1]


def test_FTC_MS_C001_boundary_solve_matches() -> None:
    assert solve_two_blank_magic_square(GRID_A001) == [2, 4, 8, 4, 4, 1]


def test_FTC_MS_C002_one_blank_boundary() -> None:
    one_blank = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(one_blank)
    assert ei.value.code == CODE_BLANK_COUNT_INVALID


def test_FTC_MS_C003_complete_magic_rejected() -> None:
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(COMPLETE_MAGIC)
    assert ei.value.code == CODE_BLANK_COUNT_INVALID


def test_FTC_MS_C005_success_contains_16() -> None:
    out = solution(PUZZLE_C005_16_IN_OUTPUT)
    assert 16 in (out[2], out[5])
    assert out == [1, 1, 16, 4, 4, 1]


def test_FTC_MS_C006_C007_C008_line_sums_after_c001() -> None:
    out = solution(GRID_A001)
    g = copy.deepcopy(GRID_A001)
    r1, c1, n1, r2, c2, n2 = out
    g[r1 - 1][c1 - 1] = n1
    g[r2 - 1][c2 - 1] = n2
    assert is_magic_square(g) is True
    for i in range(MATRIX_SIZE):
        assert sum(g[i][j] for j in range(MATRIX_SIZE)) == MAGIC_SUM
    for j in range(MATRIX_SIZE):
        assert sum(g[i][j] for i in range(MATRIX_SIZE)) == MAGIC_SUM
    assert sum(g[i][i] for i in range(MATRIX_SIZE)) == MAGIC_SUM
    assert sum(g[i][MATRIX_SIZE - 1 - i] for i in range(MATRIX_SIZE)) == MAGIC_SUM


@pytest.mark.parametrize(
    "bad,expected_code,expected_msg",
    [
        (None, CODE_SIZE_INVALID, MSG_SIZE_INVALID),
        ([], CODE_SIZE_INVALID, MSG_SIZE_INVALID),
    ],
)
def test_FTC_MS_D004_empty_or_none(
    bad: object,
    expected_code: str,
    expected_msg: str,
) -> None:
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(bad)  # type: ignore[arg-type]
    assert ei.value.code == expected_code
    assert ei.value.message == expected_msg


def test_FTC_MS_D006_jagged_rows_size_invalid() -> None:
    jagged = [
        [1, 2, 3],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    ]
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(jagged)
    assert ei.value.code == CODE_SIZE_INVALID


def test_FTC_MS_D005_non_int_cell_internal_error() -> None:
    """비정수 셀 — I2 통과 후 I3에서 INTERNAL_ERROR (PRD §8.1 D-005 구현 선택)."""
    mixed_types: list[list[object]] = [
        [0, 2, 3, 13],
        [0, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, "16"],
    ]
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(mixed_types)  # type: ignore[arg-type]
    assert ei.value.code == CODE_INTERNAL_ERROR
    assert ei.value.message == MSG_INTERNAL_ERROR


def test_FTC_MS_E003_U09_not_magic_square_boundary() -> None:
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(T05_DOUBLE_FAIL)
    assert ei.value.code == CODE_NOT_MAGIC_SQUARE
    assert ei.value.message == MSG_NOT_MAGIC_SQUARE


def test_prd_section11_i2_before_i3_detection_order() -> None:
    with pytest.raises(MagicSquareContractError) as ei:
        validate_two_blank_magic_square(THREE_BLANKS_AND_17)
    assert ei.value.code == CODE_BLANK_COUNT_INVALID
    assert ei.value.message == MSG_BLANK_COUNT_INVALID


def test_nfr04_input_matrix_not_mutated() -> None:
    snapshot = copy.deepcopy(M1)
    solve_two_blank_magic_square(M1)
    assert M1 == snapshot


def test_duplicate_nonzero_still_detected() -> None:
    dup = [
        [16, 0, 2, 13],
        [0, 5, 11, 8],
        [9, 5, 7, 12],
        [4, 15, 14, 1],
    ]
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(dup)
    assert ei.value.code == CODE_DUPLICATE_NONZERO
    assert ei.value.message == MSG_DUPLICATE_NONZERO


def test_value_out_of_range_after_blank_ok() -> None:
    has_17 = [
        [16, 0, 2, 13],
        [0, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 17],
    ]
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(has_17)
    assert ei.value.code == CODE_VALUE_OUT_OF_RANGE
    assert ei.value.message == MSG_VALUE_OUT_OF_RANGE


def test_tuple_rows_size_invalid() -> None:
    """FTC-MS-D-006 변형: 행이 list가 아니면 I1로 SIZE_INVALID."""
    matrix: list[object] = [
        (16, 0, 2, 13),
        (0, 10, 11, 8),
        (9, 6, 7, 12),
        (4, 15, 14, 1),
    ]
    with pytest.raises(MagicSquareContractError) as ei:
        solve_two_blank_magic_square(matrix)  # type: ignore[arg-type]
    assert ei.value.code == CODE_SIZE_INVALID


def test_is_magic_false_when_contains_blank() -> None:
    assert is_magic_square(M1) is False
