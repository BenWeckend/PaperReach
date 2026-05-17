import time
import xml.etree.ElementTree as ET
from typing import Dict, List
import requests

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}

_LAST_REQUEST_TIME = 0.0


def search_arxiv(query: str, max_results: int = 3, max_retries: int = 2) -> List[Dict]:
    global _LAST_REQUEST_TIME

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }

    # Retry Mechnismus (weil ich schon mal gesperrt wurde :D)
    for attempt in range(max_retries):
        # Pause für arXiv
        elapsed = time.time() - _LAST_REQUEST_TIME
        if elapsed < 3.0:
            time.sleep(3.0 - elapsed)

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
            time.sleep(5)
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
