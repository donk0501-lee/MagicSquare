"""도메인 로직 — 순수 규칙 (UI·프레임워크 의존 없음)."""

from __future__ import annotations

from magic_square.constants import (
    CELL_BLANK,
    DOMAIN_NOT_MAGIC_CODE,
    DOMAIN_NOT_MAGIC_MESSAGE,
    MAGIC_SUM,
    MATRIX_SIZE,
    VALUE_MAX,
    VALUE_MIN,
)
from magic_square.errors import MagicSquareDomainError


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
    present: set[int] = set()
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            v = matrix[r][c]
            if v != CELL_BLANK:
                present.add(v)
    missing = [n for n in range(VALUE_MIN, VALUE_MAX + 1) if n not in present]
    return sorted(missing)


def is_magic_square(matrix: list[list[int]]) -> bool:
    """0이 없는 완성 4×4에 대해 행·열·두 대각선이 각각 MAGIC_SUM이면 True."""
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            if matrix[i][j] == CELL_BLANK:
                return False
    for i in range(MATRIX_SIZE):
        if sum(matrix[i][j] for j in range(MATRIX_SIZE)) != MAGIC_SUM:
            return False
    for j in range(MATRIX_SIZE):
        if sum(matrix[i][j] for i in range(MATRIX_SIZE)) != MAGIC_SUM:
            return False
    if sum(matrix[i][i] for i in range(MATRIX_SIZE)) != MAGIC_SUM:
        return False
    if sum(matrix[i][MATRIX_SIZE - 1 - i] for i in range(MATRIX_SIZE)) != MAGIC_SUM:
        return False
    return True


def _filled_grid(
    matrix: list[list[int]],
    r1: int,
    c1: int,
    r2: int,
    c2: int,
    n1: int,
    n2: int,
) -> list[list[int]]:
    g = [row[:] for row in matrix]
    g[r1][c1] = n1
    g[r2][c2] = n2
    return g


def solution(matrix: list[list[int]]) -> list[int]:
    """FR-01 통과 격자에 대해 [r1,c1,n1,r2,c2,n2] (1-index) 반환 또는 도메인 실패."""
    (r1, c1), (r2, c2) = find_blank_coords(matrix)
    missing = find_not_exist_nums(matrix)
    n_small, n_large = missing[0], missing[1]
    i1, j1 = r1 - 1, c1 - 1
    i2, j2 = r2 - 1, c2 - 1

    def try_placement(n1: int, n2: int) -> list[int] | None:
        grid = _filled_grid(matrix, i1, j1, i2, j2, n1, n2)
        if is_magic_square(grid):
            return [r1, c1, n1, r2, c2, n2]
        return None

    out = try_placement(n_small, n_large)
    if out is not None:
        return out
    out = try_placement(n_large, n_small)
    if out is not None:
        return out

    raise MagicSquareDomainError(
        DOMAIN_NOT_MAGIC_CODE,
        DOMAIN_NOT_MAGIC_MESSAGE,
    )
