#!/usr/bin/env python3

import requests

url = "https://api.crossref.org/works"

params = {
    "query": "machine learning healthcare",
    "rows": 5
}

response = requests.get(url, params=params)
data = response.json()

for item in data["message"]["items"]:
    print(item.get("title", ["No title"])[0])
