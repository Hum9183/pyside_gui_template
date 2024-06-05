# -*- coding: utf-8 -*-
import inspect
from textwrap import dedent

from maya import cmds
from maya import OpenMayaUI as omui

try:
    from PySide6.QtWidgets import QApplication, QWidget
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2.QtWidgets import QApplication, QWidget
    from shiboken2 import wrapInstance

from .window import PysideGuiTemplateMainWindow
from . import restore as restore_module


def restart() -> None:
    if omui.MQtUtil.findControl(PysideGuiTemplateMainWindow.name):
        cmds.deleteUI(PysideGuiTemplateMainWindow.workspace_control, control=True)

    win = __create_window()
    restore_script = dedent(inspect.getsource(restore_module))
    win.show(dockable=True, uiScript=restore_script)


def restore() -> None:
    PysideGuiTemplateMainWindow.restored_instance = __create_window()  # WARNING: GCに破棄されないようにクラス変数に保存しておく
    ptr = omui.MQtUtil.findControl(PysideGuiTemplateMainWindow.name)
    restored_control = omui.MQtUtil.getCurrentParent()
    omui.MQtUtil.addWidgetToMayaLayout(int(ptr), int(restored_control))


def start() -> None:
    ptr = omui.MQtUtil.findControl(PysideGuiTemplateMainWindow.name)
    if ptr:
        win = wrapInstance(int(ptr), QWidget)
        if win.isVisible():
            win.show()  # NOTE: show()することで再フォーカスする
        else:
            win.setVisible(True)
    else:
        win = __create_window()
        cmd = dedent(inspect.getsource(restore_module))

        # TODO: 良くわからないので調べる
        # 空のWindowが生成されてしまった場合
        if cmds.workspaceControl(PysideGuiTemplateMainWindow.workspace_control, q=True, exists=True):
            # 既存のWorkspaceControlを一旦削除する
            cmds.deleteUI(PysideGuiTemplateMainWindow.workspace_control, control=True)

        win.show(dockable=True, uiScript=cmd)


def __create_window() -> PysideGuiTemplateMainWindow:
    app = QApplication.instance()
    main_window = PysideGuiTemplateMainWindow()
    main_window.init()
    return main_window

# startup
# from pyside_gui_template import run
# run.start()
