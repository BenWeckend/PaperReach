#!/usr/bin/env python3

import sys
import os
from pathlib import Path

from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
    Slot,
    Property,
)
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from openai import OpenAI

# Worker
class QueryWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    @Slot(str)
    def run_query(self, text):
        try:
            client = OpenAI(
                api_key=os.environ.get("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1",
            )

            response = client.responses.create(
                input=(
                    "Give me as output only 12 two to four word sentences, "
                    "nothing more. Each text represents the following text "
                    "as best as possible. The sentences are what could be "
                    "used as part of a title of a Paper: "
                    + text
                ),
                model="openai/gpt-oss-20b",
            )

            result = response.output_text
            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))


# Backend
class Backend(QObject):

    textChanged = Signal(str)

    def __init__(self):
        super().__init__()

        self._query_result = ""

        self.thread = QThread()  # Thread erzeugen (Muss mir das mit den Threads trotzdem nochmal genauer anschauen, das ist schon etwas komplexer....)
        self.worker = QueryWorker() # Worker erzeugen
        self.worker.moveToThread(self.thread) # Worker in Thread verschieben

        # Signale verbinden
        self.worker.finished.connect(self.on_query_finished)
        self.worker.error.connect(self.on_query_error)

        self.thread.start()  # Thread starten

    @Property(str, notify=textChanged)
    def query_result(self):
        return self._query_result

    @Slot(str)
    def make_query(self, text):
        # Worker-Methode im Hintergrundthread ausführen
        self.worker.run_query(text)

    @Slot(str)
    def on_query_finished(self, result):
        print("Ausgabe:", result)

        self._query_result = result
        self.textChanged.emit(result)

    @Slot(str)
    def on_query_error(self, error):
        print("Fehler:", error)

    def __del__(self):
        self.thread.quit()
        self.thread.wait()



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
    