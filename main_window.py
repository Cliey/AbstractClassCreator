from PySide2 import QtWidgets
from PySide2.QtCore import Slot
import sys
from tab_interface import InterfaceTab
from tab_mock import MockTab

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface and Mock Creator")
        main_layout = QtWidgets.QVBoxLayout()
        tab_layout = QtWidgets.QTabWidget(self)

        page1 = InterfaceTab()
        page2 = MockTab()
        tab_layout.addTab(page1, "Class to Interface")
        tab_layout.addTab(page2, "Class to Mock")

        main_layout.addWidget(tab_layout)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())