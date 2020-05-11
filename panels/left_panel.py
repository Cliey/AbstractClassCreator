from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Slot, Signal
from PySide2.QtGui import QPalette, QColor
from os import path

class LeftPanel(QtWidgets.QWidget):
    #signal to start creation
    start_worker = Signal(str, str, str)
    def __init__(self, file_type):
        super().__init__()
        self.file_type = file_type

        formLayout = self.create_form_layout()

        button_create_file = QtWidgets.QPushButton("Create " + self.file_type + " File")
        button_create_file.setMaximumWidth(150)
        button_create_file.clicked.connect(self.run_file_creator)

        self.label_done = QtWidgets.QLabel("")

        left_panel = QtWidgets.QGridLayout()
        left_panel.addLayout(formLayout, 0, 0, 1, 3)
        left_panel.addWidget(button_create_file, 1, 1)
        left_panel.addWidget(self.label_done, 2, 1)
        left_panel.setAlignment(QtCore.Qt.AlignVCenter)

        self.setLayout(left_panel)

    def create_form_layout(self):
        formLayout = QtWidgets.QFormLayout()
        self.class_name = QtWidgets.QLineEdit()
        # class_name.setToolTip("Add {name} to get name of the class. Ex : Class name = MyClass, I{Name} will become IMyClass")
        self.class_name.setToolTip("Prefix for the " + self.file_type)

        folder_dest_layout = self.create_folder_dest_layout()
        source_file_layout = self.create_source_file_layout()

        formLayout.addRow("Source File : ", source_file_layout)
        formLayout.addRow(self.file_type + " name : ", self.class_name)
        formLayout.addRow("Folder : ", folder_dest_layout)
        return formLayout

    def create_source_file_layout(self):
        source_file_layout = QtWidgets.QHBoxLayout()
        self.source_file = QtWidgets.QLineEdit()
        button_open_file_explorer_source = QtWidgets.QPushButton("...")
        button_open_file_explorer_source.clicked.connect(self.open_fileDialog_source_file)
        button_open_file_explorer_source.setFixedWidth(20)
        source_file_layout.addWidget(self.source_file)
        source_file_layout.addWidget(button_open_file_explorer_source)
        return source_file_layout

    def create_folder_dest_layout(self):
        folder_dest_layout = QtWidgets.QHBoxLayout()
        self.folder_dest = QtWidgets.QLineEdit()
        self.button_open_file_explorer_dest = QtWidgets.QPushButton("...")
        self.button_open_file_explorer_dest.clicked.connect(self.open_fileDialog_folder)
        self.button_open_file_explorer_dest.setFixedWidth(20)
        self.button_same_folder = QtWidgets.QCheckBox("Same folder ?")
        self.button_same_folder.stateChanged.connect(self.same_folder_state_changed)
        folder_dest_layout.addWidget(self.folder_dest)
        folder_dest_layout.addWidget(self.button_open_file_explorer_dest)
        folder_dest_layout.addWidget(self.button_same_folder)
        return folder_dest_layout

    @Slot()
    def open_fileDialog_source_file(self):
        [fileName, filter] = QtWidgets.QFileDialog.getOpenFileName(parent = self,  caption = "Open File", filter = "C++ headers files (*.hpp *.h)")
        self.source_file.setText(fileName)

    @Slot()
    def open_fileDialog_folder(self):
        dirName = QtWidgets.QFileDialog. getExistingDirectory(parent = self,  caption = "Select Directory")
        self.folder_dest.setText(dirName)

    @Slot()
    def same_folder_state_changed(self):
        if self.button_same_folder.isChecked():
            self.folder_dest.setEnabled(False)
            self.button_open_file_explorer_dest.setEnabled(False)
        else:
            self.folder_dest.setEnabled(True)
            self.button_open_file_explorer_dest.setEnabled(True)

    @Slot()
    def run_file_creator(self):
        source_file_path = self.source_file.text()
        if not source_file_path:
            msg = QtWidgets.QMessageBox.critical(self, "Error source file", "Error : the source file is not selected")
            return
        if not self.class_name.text():
            msg = QtWidgets.QMessageBox.critical(self, "Error " + self.file_type + " Name", "Error : the " + self.file_type + " Name is empty")
            return
        if not self.button_same_folder.isChecked():
           self.create_class_other_folder(source_file_path)
        else:
           self.create_class_same_folder(source_file_path)

    def create_class_other_folder(self, source_file_path):
        print("Create " + self.file_type + " in another folder")
        if not self.folder_dest.text():
            msg = QtWidgets.QMessageBox.critical(self,
                "Error destination folder", "Error : the destination is empty and you have not choose to put the " + self.file_type + " file in the same folder as source file.")
        else:
            source_file_name = path.basename(source_file_path)
            dest_file_path = self.folder_dest.text() + "/" + self.class_name.text() + source_file_name
            print(dest_file_path)
            self.emit_start_worker(source_file_path, dest_file_path)

    def create_class_same_folder(self, source_file_path):
        print("Create " + self.file_type + " in same folder as source file")
        source_file_name = path.basename(source_file_path)
        new_file_name = self.class_name.text() + source_file_name
        dest_file_path = source_file_path.replace(source_file_name, new_file_name)
        print("create from folderSource : {}".format(dest_file_path))
        self.emit_start_worker(source_file_path, dest_file_path)

    def emit_start_worker(self, source_file_path, dest_file_path):
        self.start_worker.emit(source_file_path, dest_file_path, self.class_name.text())

    def update_done_label(self):
        self.label_done.setText("Done !")
