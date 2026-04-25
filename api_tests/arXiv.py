import requests
import xml.etree.ElementTree as ET

url = "http://export.arxiv.org/api/query"

params = {
    "search_query": "all:machine learning",
    "start": 0,
    "max_results": 5
}

response = requests.get(url, params=params)

root = ET.fromstring(response.text)

for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
    title = entry.find("{http://www.w3.org/2005/Atom}title").text
    print(title)
