# -*- coding: utf-8 -*-
import inspect
import textwrap

from maya.app.general import mayaMixin

try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QMainWindow, QMenu, QPushButton
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QAction, QMainWindow, QMenu, QPushButton

from . import restart
from . import restore


class TemplateWindow(mayaMixin.MayaQWidgetDockableMixin, QMainWindow):
    restored_instance = None
    name = 'PysideTemplate'
    title = 'PySide Template'
    workspace_control = f'{name}WorkspaceControl'

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def init(self):
        self.setObjectName(TemplateWindow.name)
        self.setWindowTitle(TemplateWindow.title)
        self.setAttribute(Qt.WA_DeleteOnClose)  # つけるとclose()時にインスタンスも削除する。今回は必ずしも必要ない

        menu_bar = self.menuBar()

        dev_menu = menu_bar.addMenu("Dev")
        restart_action = QAction('Restart', self)
        restart_action.triggered.connect(lambda *arg: restart.restart_pyside_gui_template())
        dev_menu.addAction(restart_action)

        push_button = QPushButton('PUSH ME', self)
        push_button.clicked.connect(lambda *arg: self.__hello_world())
        self.setCentralWidget(push_button)

    def show(self):
        restore_script = textwrap.dedent(inspect.getsource(restore))
        super().show(dockable=True, retain=False, uiScript=restore_script)

    def __hello_world(self):
        print('Hello, World!')
