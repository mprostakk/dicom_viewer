import sys
from PyQt5 import QtWidgets, QtCore

import logging


def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widget.resize(400, 200)
    widget.setWindowTitle("This is PyQt Widget example")
    widget.show()
    exit(app.exec_())


if __name__ == '__main__':
    logging.info('Starting Dicom Viewer')
    main()
