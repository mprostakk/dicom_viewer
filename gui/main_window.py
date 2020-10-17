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
        self.setMinimumWidth(1240)
        self.setMinimumHeight(720)

    def plot(self) -> None:
        """Plot 3 axes of 3d image.

        If path to directory with .dcm files is not provided, do nothing.

        Returns:
            None.
        """
        if self.text_input.text() == '':
            return

        self.dicom_reader.load_dicom(self.text_input.text())

        self.figure_ax.clear()
        self.figure_sag.clear()
        self.figure_cor.clear()

        self.ax = self.figure_ax.add_subplot(111)
        self.sag = self.figure_sag.add_subplot(111)
        self.cor = self.figure_cor.add_subplot(111)

        self.ax.imshow(self.dicom_reader.image_3d[:, :, 0])
        self.sag.imshow(self.dicom_reader.image_3d[:, 0, :])
        self.cor.imshow(self.dicom_reader.image_3d[0, :, :].T)

        self.ax.set_aspect(self.dicom_reader.ax_aspect)
        self.sag.set_aspect(self.dicom_reader.sag_aspect)
        self.cor.set_aspect(self.dicom_reader.cor_aspect)

        self.x_slider.setRange(0, self.dicom_reader.image_shape[2] - 1)
        self.y_slider.setRange(0, self.dicom_reader.image_shape[1] - 1)
        self.z_slider.setRange(0, self.dicom_reader.image_shape[0] - 1)

        self.canvas_ax.draw()
        self.canvas_sag.draw()
        self.canvas_cor.draw()

    def plot_3d(self) -> None:
        self.figure_ax.clear()

        threshold = 300
        image_3d_transposed = self.dicom_reader.image_3d.transpose(2, 1, 0)
        vertices, faces, normals, values = \
            measure.marching_cubes(image_3d_transposed, threshold)

        self.ax = self.figure_ax.add_subplot(111, projection='3d')
        mesh = Poly3DCollection(vertices[faces], alpha=0.1)
        face_color = [0.4, 0.4, 1]
        mesh.set_facecolor(face_color)

        self.ax.add_collection3d(mesh)
        self.ax.set_xlim(0, image_3d_transposed.shape[0])
        self.ax.set_ylim(0, image_3d_transposed.shape[1])
        self.ax.set_zlim(0, image_3d_transposed.shape[2])

        self.canvas_ax.draw()

    def on_exit(self) -> None:
        logging.info('Closing Dicom Viewer')
        self.close()

