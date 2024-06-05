# -*- coding: utf-8 -*-


def restart_pyside_gui_template():
    import importlib
    from pyside_gui_template import run, window

    importlib.reload(window)
    importlib.reload(run)
    run.restart()


if __name__ == '__main__':
    restart_pyside_gui_template()
