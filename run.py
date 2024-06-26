# -*- coding: utf-8 -*-
import inspect
from textwrap import dedent

from maya import cmds
from maya import OpenMayaUI as omui

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
    from shiboken2 import wrapInstance

from .template_main_window import TemplateMainWindow
from . import restore as restore_module


def restart() -> None:
    ptr = omui.MQtUtil.findControl(TemplateMainWindow.name)
    if ptr is None:
        pass
    else:
        cmds.deleteUI(TemplateMainWindow.workspace_control, control=True)

    window = __create_window()
    window.show(dockable=True, uiScript=__get_restore_script())


def restore() -> None:
    TemplateMainWindow.restored_instance = __create_window()  # WARNING: GCに破棄されないようにクラス変数に保存しておく
    ptr = omui.MQtUtil.findControl(TemplateMainWindow.name)
    restored_control = omui.MQtUtil.getCurrentParent()
    omui.MQtUtil.addWidgetToMayaLayout(int(ptr), int(restored_control))


def start() -> None:
    # 現在Maya内に存在するPysideGuiTemplateMainWindowのポインタを取得する
    ptr = omui.MQtUtil.findControl(TemplateMainWindow.name)
    if ptr is None: # ない場合
        window = __create_window() # 新規で生成する

        # TODO: 良くわからないので調べる
        # 空のWindowが生成されてしまった場合
        if cmds.workspaceControl(TemplateMainWindow.workspace_control, q=True, exists=True):
            # 既存のWorkspaceControlを一旦削除する
            cmds.deleteUI(TemplateMainWindow.workspace_control, control=True)

        window.show(dockable=True, uiScript=__get_restore_script())
    else: # ある場合
        window = wrapInstance(int(ptr), QMainWindow)
        if window.isVisible():
            window.show()  # show()することで再フォーカスする
        else:
            window.setVisible(True)


def __create_window() -> TemplateMainWindow:
    window = TemplateMainWindow()
    window.init()
    return window


def __get_restore_script() -> str:
    return dedent(inspect.getsource(restore_module))


# startup
# from pyside_gui_template import run
# run.start()
