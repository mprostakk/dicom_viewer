import typing as tp

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QLabel, QMenu, QWidget, QSlider, \
    QHBoxLayout, QLineEdit


def create_layout() -> QHBoxLayout:
    layout = QHBoxLayout()

    return layout


def create_slider(parent, value_changed_callback: tp.Callable) -> QSlider:
    slider = QSlider(Qt.Vertical, parent)
    slider.setGeometry(40, 30, 30, 200)
    slider.setRange(0, 100)

    slider.valueChanged[int].connect(value_changed_callback)

    return slider


def create_label(parent) -> QLabel:
    label = QLabel("0", parent)
    label.setStyleSheet(
        'QLabel { background: #007AA5; border-radius: 3px;}')
    label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
    label.setMinimumWidth(80)

    return label


def create_widget() -> QWidget:
    widget = QWidget()

    return widget


def create_menu(parent) -> QMenu:
    file_menu = QMenu("&File", parent)
    file_menu.addSeparator()
    file_menu.addAction(parent.action_open_directory)
    file_menu.addAction(parent.action_exit)

    return file_menu


def create_actions(parent):
    action_exit = QAction(
        "&Exit...", parent, shortcut="Alt+F4", triggered=parent.on_exit)

    action_open_directory = QAction(
        "&Open Directory", parent, shortcut="Ctrl+o", triggered=parent.on_directory_open)

    return action_exit, action_open_directory
