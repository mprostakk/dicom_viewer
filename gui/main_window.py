import logging

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QLabel, QMenu, QWidget, QMainWindow, \
    QSlider, QHBoxLayout

from dicom_app import dicom_reader


class DicomViewer(QMainWindow):
    file_menu: QMenu
    test_action: QAction
    action_exit: QAction

    def __init__(self):
        super(DicomViewer, self).__init__()

        self.dicom_reader = DicomReader()
        self.layout = create_layout()

        # subplots
        self.ax = None
        self.sag = None
        self.cor = None

        # sliders
        self.x_slider = create_slider(self, self.x_slider_change_value)
        self.y_slider = create_slider(self, self.y_slider_change_value)
        self.z_slider = create_slider(self, self.z_slider_change_value)
        self.layout.addWidget(self.x_slider)
        self.layout.addWidget(self.y_slider)
        self.layout.addWidget(self.z_slider)

        # images
        self.figure_ax = Figure()
        self.figure_sag = Figure()
        self.figure_cor = Figure()
        self.canvas_ax = FigureCanvas(self.figure_ax)
        self.canvas_sag = FigureCanvas(self.figure_sag)
        self.canvas_cor = FigureCanvas(self.figure_cor)
        self.layout.addWidget(self.canvas_ax)
        self.layout.addWidget(self.canvas_sag)
        self.layout.addWidget(self.canvas_cor)

        # plot Button
        self.plot_button = QPushButton()
        self.plot_button.clicked.connect(self.plot)
        self.layout.addWidget(self.plot_button)

        # 3d plot button
        self.plot_button_3d = QPushButton()
        self.plot_button_3d.clicked.connect(self.plot_3d)
        self.layout.addWidget(self.plot_button_3d)

        # text input
        self.text_input = create_text_input()
        self.layout.addWidget(self.text_input)

        main_widget = create_widget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

        self.action_exit = create_actions(self)
        self.menuBar().addMenu(create_menu(self))

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

