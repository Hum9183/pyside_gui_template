# -*- coding: utf-8 -*-
from maya import OpenMayaUI as omui
from maya import cmds

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
    from shiboken2 import wrapInstance

from .template_window import TemplateWindow


def restart() -> None:
    # NOTE:
    # Qtのclose()で閉じる場合は遅延評価のため、ウィンドウの削除が完了する前に__create_window()が呼ばれてしまい、
    # workspaceControlが競合するため、cmds.workspaceControl()で削除する
    if cmds.workspaceControl(TemplateWindow.workspace_control, q=True, exists=True):
        # すでに存在しているWindowは削除する
        cmds.deleteUI(TemplateWindow.workspace_control, control=True)

    window = __create_window()
    window.show()


def restore() -> None:
    TemplateWindow.restored_instance = __create_window()  # WARNING: GCに破棄されないようにクラス変数に保存しておく
    ptr = omui.MQtUtil.findControl(TemplateWindow.name)
    restored_control = omui.MQtUtil.getCurrentParent()
    omui.MQtUtil.addWidgetToMayaLayout(int(ptr), int(restored_control))


def start() -> None:
    # 現在のMaya内に存在するTemplateWindowのポインタを取得する
    ptr = omui.MQtUtil.findControl(TemplateWindow.name)
    if ptr is None:  # ない場合
        window = __create_window()  # 新規で生成する
        window.show()
    else:  # ある場合
        window = wrapInstance(int(ptr), TemplateWindow)
        if window.isVisible():
            window.show()  # show()することで再フォーカスする
        else:
            window.setVisible(True)


def __create_window() -> TemplateWindow:
    window = TemplateWindow()
    window.init()
    return window
