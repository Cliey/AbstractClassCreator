# This Python file uses the following encoding: utf-8
import sys
from main_window import MainWindow
from PySide2.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

