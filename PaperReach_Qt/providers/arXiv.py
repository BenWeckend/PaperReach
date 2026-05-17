import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

ARXIV_API = "http://export.arxiv.org/api/query"

NS = {"atom": "http://www.w3.org/2005/Atom"}


def search_arxiv(query: str, max_results: int = 3) -> List[Dict]:

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }

    response = requests.get(ARXIV_API, params=params, timeout=15)
    response.raise_for_status()

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

