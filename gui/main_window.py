import logging

from dicom_app import dicom_reader
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QLabel, QMenu, QWidget, QMainWindow, \
    QSlider, QHBoxLayout


class DicomViewer(QMainWindow):
    file_menu: QMenu
    test_action: QAction
    action_exit: QAction

    def __init__(self):
        super(DicomViewer, self).__init__()
        self.test_dicom = dicom_reader.get_dicom()
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.init_slider()
        self.init_label()
        self.init_image()
        self.init_widget()

        self.create_actions()
        self.create_menu()

        self.setWindowTitle("Dicom Viewer")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

    def init_slider(self):
        slider = QSlider(Qt.Vertical, self)
        slider.setGeometry(40, 30, 30, 200)
        slider.setRange(0, 100) # len(self.test_dicom)
        slider.valueChanged[int].connect(self.change_value)
        self.layout.addWidget(slider)

    def init_label(self):
        self.label = QLabel("0", self)
        self.label.setStyleSheet(
            'QLabel { background: #007AA5; border-radius: 3px;}')
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)
        self.layout.addWidget(self.label)

    def init_image(self):
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()
        self.ax.imshow(dicom_reader.get_image_from_dicom(self.test_dicom, 0))
        self.ax.set_axis_off()
        self.layout.addWidget(self.canvas)

    def init_widget(self):
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def change_value(self, value):
        self.label.setText(str(value))

    def create_menu(self):
        self.file_menu = QMenu("&File", self)
        self.file_menu.addAction(self.test_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action_exit)
        self.menuBar().addMenu(self.file_menu)

    def create_actions(self):
        self.test_action = QAction(
            "&Test...", self, shortcut="Ctrl+T", triggered=self.test)
        self.action_exit = QAction(
            "&Exit...", self, shortcut="Alt+F4", triggered=self.on_exit)

    def test(self):
        logging.info('Test')

    def on_exit(self):
        logging.info('Closing Dicom Viewer')
        self.close()

