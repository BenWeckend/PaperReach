# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal

class Backend(QObject):
    textChanged = Signal(str)

    @Slot()
    def say_hello(self):
        print("Hello aus Python")

    @Slot(str)
    def process_text(self, text):
        print("Eingabe:", text)
        result = text.lower()
        self.textChanged.emit(result)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(Path(__file__).parent)

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.loadFromModule("PaperReach_Qt", "Main")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
