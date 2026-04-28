"""공식 CLI 진입점: `python -m magic_square` → PyQt MVP 창."""

from __future__ import annotations

import sys


def main() -> int:
    from PyQt6.QtWidgets import QApplication

    from magic_square.gui.main_window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(320, 260)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
