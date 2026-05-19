import xml.etree.ElementTree as ET
import requests

url = "https://export.arxiv.org/api/query"  # Nutze https statt http

params = {"search_query": "all:machine learning", "start": 0, "max_results": 5}

# Ein passender Header signalisiert arXiv, wer die Anfrage stellt
headers = {
    "User-Agent": "PaperReachDev/1.0 (contact: dein-name@example.com)"
}

try:
    response = requests.get(url, params=params, headers=headers)

    # 1. Prüfen, ob der Server mit HTTP 200 geantwortet hat
    response.raise_for_status()

    # 2. Falls die Antwort leer ist, Abfangregel greifen lassen
    if not response.text.strip():
        print("Fehler: Die API hat eine komplett leere Antwort zurückgegeben.")
    else:
        root = ET.fromstring(response.text)

        for entry in root.findall("{http://w3.org}entry"):
            title = entry.find("{http://w3.org}title").text
            print(title.strip().replace("\n", " "))

except requests.exceptions.HTTPError as e:
    print(f"HTTP-Fehler aufgetreten: {e}")
    print(
        f"Server-Antwort (kein XML): {response.text[:500]}"
    )  # Zeigt den HTML-Fehlertext an
except ET.ParseError as e:
    print(f"XML-Parsing-Fehler: {e}")
    print(f"Erhaltene Antwort war:\n{response.text[:500]}")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

