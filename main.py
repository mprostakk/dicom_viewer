import sys
import os
import logging

from PyQt5 import QtWidgets
import matplotlib.pyplot as plt

from gui.main_window import DicomViewer


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logging.info('Starting Dicom Viewer')

    app = QtWidgets.QApplication(sys.argv)

    dicomViewer = DicomViewer()
    dicomViewer.show()

    sys.exit(app.exec_())
