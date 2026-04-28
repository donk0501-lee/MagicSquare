"""경계(원시 입력·출력·오류 매핑) — RED 단계: 진입점만 두고 GREEN에서 구현."""

from __future__ import annotations

from magic_square.constants import CODE_SIZE_INVALID, MATRIX_SIZE, MSG_SIZE_INVALID
from magic_square.errors import MagicSquareContractError


def solve_two_blank_magic_square(matrix: list[list[int]]) -> list[int]:
    """I1~I4 검증 후 도메인 해결; 성공 시 int[6], 실패 시 MagicSquareContractError."""
    if len(matrix) != MATRIX_SIZE:
        raise MagicSquareContractError(CODE_SIZE_INVALID, MSG_SIZE_INVALID)
    for row in matrix:
        if len(row) != MATRIX_SIZE:
            raise MagicSquareContractError(CODE_SIZE_INVALID, MSG_SIZE_INVALID)
    raise NotImplementedError("GREEN: Track A - solve_two_blank_magic_square")
