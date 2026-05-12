#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import requests

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

from providers.semantic_scholar import search_semantic_scholar
from providers.arXiv import search_arxiv

# Worker
class QueryWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    @Slot(str)
    def make_query(self, text):
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

            keywords = response.output_text
            print("Generierte Keywords:", keywords)
            self.finished.emit(keywords)

            # keywords bei jeder neuen Zeile Trennen und als Liste speichern
            keywords_list = keywords.split("\n")
            print("Keywords Liste:", keywords_list)


            for kw in keywords_list:
                print(f"Suche nach: {kw}")
                papers_arXiv = search_arxiv(kw)
                print(f"Gefundene Paper aus arXiv für '{kw}':")
                for paper in papers_arXiv:
                    print(f"  - {paper['title']}")
                    print(f"    Autoren: {paper['authors']}")
                    print(f"    URL: {paper['url']}")
                    print()

            #keywords_test = "machine learning"
            #papers_arXiv = search_arxiv(keywords_test)
            #print("Gefundene Paper aus arXiv:")
            #for paper in papers_arXiv:
            #    print(f"  - {paper['title']}")
            #    print(f"    Autoren: {paper['authors']}")
            #    print(f"    URL: {paper['url']}")
            #    print()

            # Übergebe die Keywords an search_semantic_scholar
            #papers = search_semantic_scholar(keywords_test)
            #print("Gefundene Paper aus Semantic Scholar:")
            #for paper in papers:
            #    print(f"  - {paper['title']}")
            #    print(f"    Autoren: {paper['authors']}")
            #    print(f"    URL: {paper['url']}")
            #    print()
            #
            
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
        self.worker.make_query(text)

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
    