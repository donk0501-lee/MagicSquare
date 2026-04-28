"""격자 차원·값 범위·마방진 합·경계 계약 상수 (PRD I1, §8.1)."""

from __future__ import annotations

MATRIX_SIZE = 4

CELL_BLANK = 0
VALUE_MIN = 1
VALUE_MAX = 16

MAGIC_SUM = 34

CODE_SIZE_INVALID = "SIZE_INVALID"
MSG_SIZE_INVALID = "Matrix must be 4x4."

CODE_BLANK_COUNT_INVALID = "BLANK_COUNT_INVALID"
MSG_BLANK_COUNT_INVALID = "Exactly two cells must be 0."

CODE_VALUE_OUT_OF_RANGE = "VALUE_OUT_OF_RANGE"
MSG_VALUE_OUT_OF_RANGE = (
    "Each cell must be 0 or between 1 and 16 inclusive."
)

CODE_DUPLICATE_NONZERO = "DUPLICATE_NONZERO"
MSG_DUPLICATE_NONZERO = "Non-zero values must be unique."

CODE_NOT_MAGIC_SQUARE = "NOT_MAGIC_SQUARE"
MSG_NOT_MAGIC_SQUARE = (
    "No valid placement completes a 4x4 magic square."
)

DOMAIN_NOT_MAGIC_CODE = "NOT_MAGIC"
DOMAIN_NOT_MAGIC_MESSAGE = "No valid placement for the two missing values."

CODE_INTERNAL_ERROR = "INTERNAL_ERROR"
MSG_INTERNAL_ERROR = "Unexpected error."
