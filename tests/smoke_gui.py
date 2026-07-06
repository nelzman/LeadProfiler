"""Headless smoke test for the PyQt5 GUI.

Run with: QT_QPA_PLATFORM=offscreen python -m tests.smoke_gui
"""

import sys

from PyQt5 import QtCore, QtWidgets

from src.lead_profiler_app import LeadProfilerApp


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = LeadProfilerApp()
    ui.setupUi(window)

    assert ui.textBrowserTalkingPoints is not None
    assert ui.textBrowserPerson is not None
    assert ui.Export_Button is not None
    assert ui.Export_Button.isEnabled() is False
    assert ui.spinBoxMonths.value() == ui.config.news_months

    print("Smoke test OK: all widgets present, Export_Button starts disabled.")

    QtCore.QTimer.singleShot(0, app.quit)
    window.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
