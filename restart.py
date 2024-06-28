# -*- coding: utf-8 -*-


def restart_pyside_gui_template():
    import importlib
    from pyside_gui_template import run, template_window

    importlib.reload(template_window)
    importlib.reload(run)
    run.restart()


if __name__ == '__main__':
    restart_pyside_gui_template()
