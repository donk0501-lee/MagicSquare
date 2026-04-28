"""PRD §8.1 고정 문자열·코드 (docs/MagicSquare_4x4_TDD.md)."""

from magic_square.constants import (
    CODE_SIZE_INVALID,
    MATRIX_SIZE,
    MSG_SIZE_INVALID,
)

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

MAGIC_SUM = 34
GRID_SIZE = MATRIX_SIZE
