# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal

from openai import OpenAI
import os

class Backend(QObject):
    textChanged = Signal(str)

    @Slot(str)
    def make_query(self, text):
        client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )

        response = client.responses.create(
            input="Give me as output only 10 two to three word sentences, nothing more. Each text represents the following text as best as possible. The sentences are what could be used as part of a title of a Paper: " + text ,
            model="openai/gpt-oss-20b",
        )

        print("Eingabe:", response.output_text)
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
