import requests
import xml.etree.ElementTree as ET

url = "http://export.arxiv.org/api/query"

params = {
    "search_query": "all:machine learning healthcare",
    "start": 0,
    "max_results": 5
}

response = requests.get(url, params=params)

# XML parsen
root = ET.fromstring(response.text)

# Namespace (wichtig!)
ns = {"atom": "http://www.w3.org/2005/Atom"}

for entry in root.findall("atom:entry", ns):
    
    title = entry.find("atom:title", ns).text.strip()
    
    authors = []
    for author in entry.findall("atom:author", ns):
        name = author.find("atom:name", ns).text
        authors.append(name)
    
    abstract = entry.find("atom:summary", ns).text.strip()
    
    pdf_url = None
    abs_url = None
    
    for link in entry.findall("atom:link", ns):
        if link.attrib.get("type") == "application/pdf":
            pdf_url = link.attrib.get("href")
        if link.attrib.get("rel") == "alternate":
            abs_url = link.attrib.get("href")
    
    print("Title:", title)
    print("Authors:", ", ".join(authors))
    print("PDF:", pdf_url)
    print("Abstract Page:", abs_url)
    print("-" * 50)
