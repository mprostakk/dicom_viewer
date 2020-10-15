import sys
import logging

from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QLabel, QScrollArea, QMenu, QSizePolicy, QApplication, QMainWindow


class DicomViewer(QMainWindow):

    file_menu: QMenu

    test_action: QAction
    action_exit: QAction

    def __init__(self):
        super(DicomViewer, self).__init__()

        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QtGui.QPalette.Base)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QtGui.QPalette.Base)
        self.scroll_area.setWidget(self.image_label)
        self.setCentralWidget(self.scroll_area)

        self.create_actions()
        self.create_menu()

        self.setWindowTitle("Dicom Viewer")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

    def create_actions(self):
        self.test_action = QAction("&Test...", self, shortcut="Ctrl+T", triggered=self.test)
        self.action_exit = QAction("&Exit...", self, shortcut="Alt+F4", triggered=self.on_exit)

    def create_menu(self):
        self.file_menu = QMenu("&File", self)
        self.file_menu.addAction(self.test_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action_exit)

        self.menuBar().addMenu(self.file_menu)

    def test(self):
        logging.info('Test')

    def on_exit(self):
        logging.info('Closing Dicom Viewer')
        self.close()
