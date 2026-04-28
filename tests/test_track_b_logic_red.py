"""Track B — Logic RED (FR-02~FR-05, docs/MagicSquare_4x4_TDD.md).

도메인 함수 본문은 GREEN 전까지 NotImplementedError이므로,
값·불리언 단언 테스트는 **NotImplementedError로 실패(RED)** 하고,
도메인 예외 기대 테스트는 **예외 타입 불일치로 실패(RED)** 한다.
"""

from __future__ import annotations

import pytest

from magic_square.errors import MagicSquareDomainError
from magic_square.logic import (
    find_blank_coords,
    find_not_exist_nums,
    is_magic_square,
    solution,
)

# §9.1 M1, M2 (FR-01 통과)
M1 = [
    [16, 0, 2, 13],
    [0, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
M2 = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# Formal FTC-MS-A-001 (PRD 1-index)
GRID_A001 = [
    [16, 2, 3, 13],
    [5, 11, 10, 0],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

# 완성 4×4 고전 마방진 (Formal FTC-MS-B-001)
COMPLETE_MAGIC = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

# 모서리 16↔1 스왑 → 행·열·대각 중 최소 하나 불만족, 0 없음
NOT_MAGIC_ROW_BROKEN = [
    [1, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 16],
]

# T-05: FR-01 만족(4×4, 0 두 개, 1~16 유일)하나 두 조합 모두 비마방진
T05_DOUBLE_FAIL = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 0, 0],
]


def test_LOGIC_RED_01_find_blank_coords_row_major_two_pairs() -> None:
    """FR-02 / FTC-MS-A-001: row-major 두 빈칸의 1-index 쌍.

    Invariant: BR-05, BR-06 — 스캔 순서·대외 좌표.
    """
    coords = find_blank_coords(GRID_A001)
    assert coords == [(2, 4), (4, 4)]


def test_LOGIC_RED_02_find_blank_coords_m1_m2_consistency() -> None:
    """FR-02 AC: M1 첫 (1,2)·둘째 (2,1); M2 첫 (3,3)·둘째 (4,4).

    Invariant: FR-02 AC — 골든 좌표 고정.
    """
    assert find_blank_coords(M1) == [(1, 2), (2, 1)]
    assert find_blank_coords(M2) == [(3, 3), (4, 4)]


def test_LOGIC_RED_03_find_not_exist_nums_sorted_two_values() -> None:
    """FR-03 / BR-09: 누락 두 수, 오름차순.

    Invariant: 누락 집합 크기 2·정렬 표현.
    """
    assert find_not_exist_nums(M1) == [3, 5]
    assert find_not_exist_nums(M2) == [1, 6]


def test_LOGIC_RED_04_is_magic_square_true_complete_magic() -> None:
    """FR-04 / FTC-MS-B-001: 완성 마방진이면 True.

    Invariant: I6/BR-08 — 10선 합 34.
    """
    assert is_magic_square(COMPLETE_MAGIC) is True


@pytest.mark.parametrize(
    "label, grid",
    [
        ("row_imbalance", NOT_MAGIC_ROW_BROKEN),
        (
            "col_imbalance",
            [
                [16, 2, 3, 13],
                [8, 11, 10, 5],
                [9, 7, 6, 12],
                [4, 14, 15, 1],
            ],
        ),
        (
            "main_diag_imbalance",
            [
                [2, 16, 3, 13],
                [5, 11, 10, 8],
                [9, 7, 6, 12],
                [4, 14, 15, 1],
            ],
        ),
        (
            "permute_non_magic",
            [
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 15, 14, 16],
            ],
        ),
    ],
)
def test_LOGIC_RED_05_is_magic_square_false_when_any_line_not_34(
    label: str, grid: list[list[int]]
) -> None:
    """FR-04 AC: 완성 격자에서 행·열·주대각·부대각 중 하나라도 34가 아니면 False.

    Invariant: BR-07(M=34), BR-08 — 10선 동시 만족.
    """
    _ = label
    assert is_magic_square(grid) is False


def test_LOGIC_RED_06_solution_m1_small_to_first_blank() -> None:
    """FR-05 / T-01: 시도1(n_small→첫 빈칸) 성공, int[6]·1-index.

    Invariant: BR-10, BR-12, BR-14 — 시도 순서·출력 의미.
    """
    out = solution(M1)
    assert out == [1, 2, 3, 2, 1, 5]
    assert len(out) == 6
    assert all(1 <= out[i] <= 4 for i in (0, 1, 3, 4))


def test_LOGIC_RED_07_solution_m2_reverse_try_succeeds() -> None:
    """FR-05 / T-02: 시도1 실패 후 시도2(역배치) 성공.

    Invariant: BR-11 — 역시도 후 성공 시 (n1,n2)=(n_large,n_small).
    """
    assert solution(M2) == [3, 3, 6, 4, 4, 1]


def test_LOGIC_RED_08_solution_double_fail_raises_domain_error() -> None:
    """FR-05 / T-05: 두 시도 모두 비마방진이면 도메인 실패.

    Invariant: BR-13 — 성공 출력 부재 시 NOT_MAGIC(도메인 코드).
    """
    with pytest.raises(MagicSquareDomainError) as ei:
        solution(T05_DOUBLE_FAIL)
    assert ei.value.code == "NOT_MAGIC"
