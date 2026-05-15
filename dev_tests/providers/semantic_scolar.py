import requests

url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {
    "query": "machine learning",
    "limit": 5,
    "fields": "title,authors,year,abstract,url"
}

# anfrage senden
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    if "data" in data:
        for paper in data["data"]:
            # Autoren Als Liste von Dicts
            author_names = ", ".join([author["name"] for author in paper.get("authors", [])])
            
            print(f"Titel: {paper.get('title')}")
            print(f"Autoren: {author_names}")
            print(f"URL: {paper.get('url')}\n")
else:
    print(f"Fehler: {response.status_code}")

