"""4×4 입력·풀기·결과 표시 메인 창 (Screen)."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from magic_square.boundary import (
    solve_two_blank_magic_square,
    validate_two_blank_magic_square,
)
from magic_square.constants import MATRIX_SIZE, VALUE_MAX
from magic_square.errors import MagicSquareContractError

# 데모용 골든 입력 (FR-01 통과) — 빈 칸은 0
_DEFAULT_GRID: list[list[int]] = [
    [16, 0, 2, 13],
    [0, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


class MainWindow(QWidget):
    """MVP: 스핀박스 4×4, 검증 후 풀이, 결과·오류 표시."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Magic Square 4×4 — 두 빈칸 풀이")
        self._cells: list[list[QSpinBox]] = []
        root = QVBoxLayout(self)

        grid = QGridLayout()
        for r in range(MATRIX_SIZE):
            row_widgets: list[QSpinBox] = []
            for c in range(MATRIX_SIZE):
                sp = QSpinBox()
                sp.setRange(0, VALUE_MAX)
                sp.setValue(_DEFAULT_GRID[r][c])
                sp.setMinimumWidth(52)
                grid.addWidget(sp, r, c)
                row_widgets.append(sp)
            self._cells.append(row_widgets)
        root.addLayout(grid)

        btn_row = QHBoxLayout()
        solve_btn = QPushButton("풀기")
        solve_btn.clicked.connect(self._on_solve)
        btn_row.addWidget(solve_btn)
        btn_row.addStretch()
        root.addLayout(btn_row)

        self._result_label = QLabel("결과: —")
        self._result_label.setWordWrap(True)
        root.addWidget(self._result_label)

    def _read_matrix(self) -> list[list[int]]:
        return [
            [self._cells[r][c].value() for c in range(MATRIX_SIZE)]
            for r in range(MATRIX_SIZE)
        ]

    def _on_solve(self) -> None:
        matrix = self._read_matrix()
        try:
            validate_two_blank_magic_square(matrix)
        except MagicSquareContractError as e:
            QMessageBox.warning(self, "입력 검증", e.message)
            self._result_label.setText("결과: —")
            return
        try:
            out = solve_two_blank_magic_square(matrix)
        except MagicSquareContractError as e:
            QMessageBox.warning(self, "풀이", e.message)
            self._result_label.setText("결과: —")
            return
        r1, c1, n1, r2, c2, n2 = out
        self._result_label.setText(
            f"결과: [{r1}, {c1}, {n1}, {r2}, {c2}, {n2}]  "
            f"(첫 빈칸 ({r1},{c1})→{n1}, 둘째 빈칸 ({r2},{c2})→{n2})"
        )
