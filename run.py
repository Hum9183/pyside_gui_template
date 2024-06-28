# -*- coding: utf-8 -*-
from maya import cmds
from maya import OpenMayaUI as omui

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
    from shiboken2 import wrapInstance

from .template_main_window import TemplateMainWindow


def restart() -> None:
    # NOTE:
    # Qtのclose()で閉じる場合は遅延評価のため、ウィンドウの削除が完了する前に__create_window()が呼ばれてしまい、
    # workspaceControlが競合するため、cmds.workspaceControl()で削除する
    if cmds.workspaceControl(TemplateMainWindow.workspace_control, q=True, exists=True):
        # すでに存在しているWindowは削除する
        cmds.deleteUI(TemplateMainWindow.workspace_control, control=True)

    window = __create_window()
    window.show()


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
        window.show()
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

# startup
# from pyside_gui_template import run
# run.start()
