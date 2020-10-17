import typing as tp

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QLabel, QMenu, QWidget, QSlider, \
    QHBoxLayout, QLineEdit


def create_layout() -> QHBoxLayout:
    layout = QHBoxLayout()

    return layout


def create_slider(self, value_changed_callback: tp.Callable) -> QSlider:
    slider = QSlider(Qt.Vertical, self)
    slider.setGeometry(40, 30, 30, 200)
    slider.setRange(0, 100)

    slider.valueChanged[int].connect(value_changed_callback)

    return slider


def create_label(self) -> QLabel:
    label = QLabel("0", self)
    label.setStyleSheet(
        'QLabel { background: #007AA5; border-radius: 3px;}')
    label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
    label.setMinimumWidth(80)

    return label


def create_widget() -> QWidget:
    widget = QWidget()

    return widget


def create_menu(self) -> QMenu:
    file_menu = QMenu("&File", self)
    file_menu.addSeparator()
    file_menu.addAction(self.action_exit)

    return file_menu


def create_text_input() -> QLineEdit:
    text_input = QLineEdit()
    text_input.setFont(QFont("Mono", 10))

    return text_input


def create_actions(self):
    action_exit = QAction(
        "&Exit...", self, shortcut="Alt+F4", triggered=self.on_exit)

    return action_exit
