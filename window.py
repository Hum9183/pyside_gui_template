# -*- coding: utf-8 -*-
from maya.app.general import mayaMixin

try:
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QMainWindow, QMenu, QPushButton
except ImportError:
    from PySide2.QtWidgets import QAction, QMainWindow, QMenu, QPushButton

from .restart import restart_pyside_gui_template


class PysideGuiTemplateMainWindow(mayaMixin.MayaQWidgetDockableMixin, QMainWindow):
    restored_instance = None
    name = 'PysideGuiTemplate'
    title = 'PySide Gui Template'
    workspace_control = f'{name}WorkspaceControl'

    def __init__(self, parent=None, *args, **kwargs):
        super(PysideGuiTemplateMainWindow, self).__init__(parent, *args, **kwargs)

    def init(self):
        self.setObjectName(PysideGuiTemplateMainWindow.name)
        self.setWindowTitle(PysideGuiTemplateMainWindow.title)

        menu_bar = self.menuBar()

        dev_menu = menu_bar.addMenu("Dev")
        restart_action = QAction('Restart', self)
        restart_action.triggered.connect(lambda *arg: restart_pyside_gui_template())
        dev_menu.addAction(restart_action)

        push_button = QPushButton('PUSH ME', self)
        push_button.clicked.connect(lambda *arg: self.hello_world())
        self.setCentralWidget(push_button)


    def hello_world(self):
        print('Hello, World!')

# TODO: よくわからないので調べる
# window closeのコールバックで
# cmds.deleteUI('PysideGuiTemplateWorkspaceControl', control=True)
# を実行する
