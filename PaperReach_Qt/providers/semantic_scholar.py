# providers/semantic_scholar.py
import requests
from typing import List, Dict

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_semantic_scholar(query: str, limit: int = 10) -> List[Dict]:
    """
    Gibt eine Liste von Paper Dictionaries zurück.
    Jede Dict enthält mindestens: id, title, authors, abstract, url, source.
    """
    params = {
        "search_query": "all:machine learning healthcare",
        "start": 0,
        "max_results": 5
    }
    resp = requests.get(BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for entry in data.get("data", []):
        results.append(
            {
                "id": entry.get("paperId"),
                "title": entry.get("title"),
                "authors": ", ".join(a.get("name") for a in entry.get("authors", [])),
                "abstract": entry.get("abstract", ""),
                "url": entry.get("url"),
                "source": "semantic_scholar",
            }
        )
    return results