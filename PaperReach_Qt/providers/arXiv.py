import time
import xml.etree.ElementTree as ET
from typing import Dict, List
import requests
import tomllib
import os
import sys

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}

_LAST_REQUEST_TIME = 0.0


if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(current_dir) 

# Erstellt den absolut sicheren Pfad zur Datei
pyproject_path = os.path.join(base_path, "pyproject.toml")

# dynamischen Pfad laden
with open(pyproject_path, "rb") as f:
    config = tomllib.load(f)
    pass

paper_number = config["project_Variablen"]["arXiv_paper_number"]

if __name__ == "__main__":
    print(f"Anzahl der Paper, die von arXiv abgefragt werden: {paper_number}")

def search_arxiv(query: str, max_retries: int = 4) -> List[Dict]:
    global _LAST_REQUEST_TIME

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": paper_number,
    }

    # Retry Mechnismus (weil ich schon mal gesperrt wurde :D)
    for attempt in range(max_retries):
        # Pause für arXiv
        #elapsed = time.time() - _LAST_REQUEST_TIME
        #if elapsed < 3.0:
        #    time.sleep(3.0 - elapsed)

        try:
            _LAST_REQUEST_TIME = time.time()
            response = requests.get(ARXIV_API, params=params, timeout=45)

            # Rate Limit (429) oder temporäre Sperre (503) abfangen
            if response.status_code in [429, 503]:
                # Versuche die vom Server gewünschte Wartezeit zu lesen, Standard: 5 Sekunden
                retry_after = int(response.headers.get("Retry-After", 5))
                print(
                    f"[ArXiv API] Rate Limit erreicht. Warte {retry_after} Sekunden... (Versuch {attempt + 1}/{max_retries})"
                )
                time.sleep(retry_after)
                continue

            response.raise_for_status()
            break  # Erfolgreich, Schleife verlassen

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            print(
                f"[ArXiv API] Fehler: {e}. Neuer Versuch in 5 Sekunden..."
            )
            time.sleep(1)
    else:
        raise RuntimeError(
            "arXiv API konnte nach mehreren Versuchen nicht erreicht werden."
        )

    # XML-Antwort parsen
    root = ET.fromstring(response.text)
    results = []

    for entry in root.findall("atom:entry", NS):
        title = entry.find("atom:title", NS).text.strip()

        authors = []
        for author in entry.findall("atom:author", NS):
            name = author.find("atom:name", NS).text
            authors.append(name)

        abstract = entry.find("atom:summary", NS).text.strip()

        pdf_url = None
        abs_url = None

        for link in entry.findall("atom:link", NS):
            if link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href")
            if link.attrib.get("rel") == "alternate":
                abs_url = link.attrib.get("href")

        arxiv_id = abs_url.split("/")[-1] if abs_url else None

        results.append(
            {
                "id": arxiv_id,
                "title": title,
                "authors": ", ".join(authors),
                "abstract": abstract,
                "url": pdf_url or abs_url,
                "source": "arxiv",
            }
        )

    return results
