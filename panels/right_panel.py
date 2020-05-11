from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot

class RightPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        right_panel = QtWidgets.QVBoxLayout()
        self.code_output = QtWidgets.QTextEdit()
        # self.code_output.setReadOnly(True)
        self.code_output.setStyleSheet("background-color: white;")
        toolbar = self.create_toolbar()
        right_panel.addLayout(toolbar)
        right_panel.addWidget(self.code_output)

        self.setLayout(right_panel)

    def create_toolbar(self):
        toolbar = QtWidgets.QHBoxLayout()
        copy_button = QtWidgets.QPushButton("Copy")
        copy_button.clicked.connect(self.copy_code_output)
        toolbar.addWidget(QtWidgets.QLabel("Code Output"))
        toolbar.addWidget(copy_button)
        toolbar.setAlignment(QtCore.Qt.AlignLeft)
        return toolbar

    @Slot()
    def copy_code_output(self):
        self.code_output.selectAll()
        self.code_output.copy()

    def update_panel(self, dest_file_path):
        print("dest_file_path = {}".format(dest_file_path))
        file = open(dest_file_path, "r")
        file_content = file.readlines()
        file.close()
        for line in file_content:
            self.code_output.moveCursor(QtGui.QTextCursor.End)
            self.code_output.insertPlainText(line)