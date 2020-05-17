from PySide2 import QtWidgets
from PySide2.QtCore import Slot
import sys
from panels.left_panel import LeftPanel
from panels.right_panel import RightPanel
import ClassParsing.class_to_mock

class MockTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()

        self.left_panel = LeftPanel("Mock")
        self.left_panel.start_worker.connect(self.open_file_and_execute)
        self.right_panel = RightPanel()

        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)

        self.setLayout(layout)

    @Slot(str, str, str)
    def open_file_and_execute(self, source_file_path, dest_file_path, interface_name):
        file = open(source_file_path, "r")
        file_content = file.readlines()
        file.close()
        worker = ClassParsing.class_to_mock.ClassToMock(file_content, dest_file_path, interface_name)
        worker.exec()
        self.right_panel.update_panel(dest_file_path)
        self.left_panel.update_done_label()


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    main_window = MainWindowMock()
    main_window.show()

    sys.exit(app.exec_())