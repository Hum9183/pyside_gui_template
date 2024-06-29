# -*- coding: utf-8 -*-


def restart_pyside_template_window():
    import importlib
    from pyside_template_window import run, template_window

    importlib.reload(template_window)
    importlib.reload(run)
    run.restart()


if __name__ == '__main__':
    restart_pyside_template_window()
