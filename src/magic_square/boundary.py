"""경계(원시 입력·출력·오류 매핑)."""

from __future__ import annotations

from magic_square.constants import (
    CELL_BLANK,
    CODE_BLANK_COUNT_INVALID,
    CODE_DUPLICATE_NONZERO,
    CODE_INTERNAL_ERROR,
    CODE_NOT_MAGIC_SQUARE,
    CODE_SIZE_INVALID,
    CODE_VALUE_OUT_OF_RANGE,
    DOMAIN_NOT_MAGIC_CODE,
    MATRIX_SIZE,
    MSG_BLANK_COUNT_INVALID,
    MSG_DUPLICATE_NONZERO,
    MSG_INTERNAL_ERROR,
    MSG_NOT_MAGIC_SQUARE,
    MSG_SIZE_INVALID,
    MSG_VALUE_OUT_OF_RANGE,
    VALUE_MAX,
    VALUE_MIN,
)
from magic_square.errors import MagicSquareContractError, MagicSquareDomainError
from magic_square.logic import solution


def _copy_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in matrix]


def _is_grid_int(v: object) -> bool:
    """계약 셀 정수(int)만 허용 — bool은 제외."""
    return isinstance(v, int) and not isinstance(v, bool)


def _validate_contract(matrix: object) -> None:
    """PRD §11 순서: I1 → I2 → I3 → I4."""
    if matrix is None or not isinstance(matrix, list):
        raise MagicSquareContractError(CODE_SIZE_INVALID, MSG_SIZE_INVALID)
    if len(matrix) != MATRIX_SIZE:
        raise MagicSquareContractError(CODE_SIZE_INVALID, MSG_SIZE_INVALID)
    for row in matrix:
        if not isinstance(row, list):
            raise MagicSquareContractError(CODE_SIZE_INVALID, MSG_SIZE_INVALID)
        if len(row) != MATRIX_SIZE:
            raise MagicSquareContractError(CODE_SIZE_INVALID, MSG_SIZE_INVALID)

    blank_count = 0
    for row in matrix:
        for v in row:
            if v == CELL_BLANK:
                blank_count += 1
    if blank_count != 2:
        raise MagicSquareContractError(
            CODE_BLANK_COUNT_INVALID,
            MSG_BLANK_COUNT_INVALID,
        )

    nonzero_values: list[int] = []
    for row in matrix:
        for v in row:
            if v != CELL_BLANK:
                if not _is_grid_int(v):
                    raise MagicSquareContractError(
                        CODE_INTERNAL_ERROR,
                        MSG_INTERNAL_ERROR,
                    )
                if not (VALUE_MIN <= v <= VALUE_MAX):
                    raise MagicSquareContractError(
                        CODE_VALUE_OUT_OF_RANGE,
                        MSG_VALUE_OUT_OF_RANGE,
                    )
                nonzero_values.append(v)

    if len(nonzero_values) != len(set(nonzero_values)):
        raise MagicSquareContractError(
            CODE_DUPLICATE_NONZERO,
            MSG_DUPLICATE_NONZERO,
        )


def validate_two_blank_magic_square(matrix: list[list[int]]) -> None:
    """I1~I4만 검증. 위반 시 MagicSquareContractError."""
    _validate_contract(matrix)


def solve_two_blank_magic_square(matrix: list[list[int]]) -> list[int]:
    """I1~I4 검증 후 도메인 해결; 성공 시 int[6], 실패 시 MagicSquareContractError."""
    _validate_contract(matrix)
    work = _copy_matrix(matrix)
    try:
        return solution(work)
    except MagicSquareDomainError as e:
        if e.code == DOMAIN_NOT_MAGIC_CODE:
            raise MagicSquareContractError(
                CODE_NOT_MAGIC_SQUARE,
                MSG_NOT_MAGIC_SQUARE,
            ) from e
        raise
