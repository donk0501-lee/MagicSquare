"""도메인 로직 — RED 단계: 시그니처만 두고 본문은 GREEN에서 구현."""

from __future__ import annotations

from magic_square.constants import CELL_BLANK, MATRIX_SIZE


def find_blank_coords(matrix: list[list[int]]) -> list[tuple[int, int]]:
    """row-major로 두 빈칸(0)의 1-index (r, c) 쌍을 정확히 2개 반환."""
    coords: list[tuple[int, int]] = []
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            if matrix[r][c] == CELL_BLANK:
                coords.append((r + 1, c + 1))
    return coords


def find_not_exist_nums(matrix: list[list[int]]) -> list[int]:
    """1~16 중 격자에 없는 두 수를 오름차순 길이-2 리스트로 반환."""
    raise NotImplementedError("GREEN: Track B - find_not_exist_nums")


def is_magic_square(matrix: list[list[int]]) -> bool:
    """0이 없는 완성 4×4에 대해 행·열·두 대각선이 각각 34이면 True."""
    raise NotImplementedError("GREEN: Track B - is_magic_square")


def solution(matrix: list[list[int]]) -> list[int]:
    """FR-01 통과 격자에 대해 [r1,c1,n1,r2,c2,n2] (1-index) 반환 또는 도메인 실패."""
    raise NotImplementedError("GREEN: Track B - solution")
