import sqlite3
import pypdf
import requests
import io
import time
import tomllib
import os
import sys

from pathlib import Path
from embeddings import analyze_similarity

accurate_mode = False  # Wenn True, wird die PDF in Chunks aufgeteilt und jeder Chunk bewertet. Ansonsten nur das Abstract.

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Erstellt den absolut sicheren Pfad zur Datei
pyproject_path = os.path.join(base_path, "pyproject.toml")

# dynamischen Pfad laden
with open(pyproject_path, "rb") as f:
    config = tomllib.load(f)
    pass

#with open("./pyproject.toml", "rb") as f:
#    config = tomllib.load(f)

chunk_size = config["project_Variablen"]["chunk_size"]
version = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

db_path = Path("./databases")
db_path.mkdir(parents=True, exist_ok=True)
DB_NAME = str(db_path / f"papers_{version}.db")
DB_PROVISORISCH = "./databases/papers_2026-05-16_16-40-20.db"


def get_db_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            abstract TEXT,
            url TEXT,
            source TEXT,
            rating REAL,
            content TEXT,
            accurate BOOLEAN
        )
        """
    )
    conn.commit()
    conn.close()

def extract_text_from_url(pdf_url):
    if not pdf_url:
        return ""
    try:
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status() # Wirft Fehler bei 404 oder 500
        
        # io.BytesIO simuliert Datei im RAM: geht schneller als eine temp.pfd aud der Festplatte anzulegen

        pdf_file = io.BytesIO(response.content)
        reader = pypdf.PdfReader(pdf_file)
        
        pdf_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:  # Seite leer oder Bild
                pdf_text += text + "\n"
        return pdf_text
    except Exception as e:
        print(f"Fehler beim Download/Auslesen von {pdf_url}: {e}")
        return ""


def create_text_chunks_and_rate(paper, prompt_text: str = None):
    content = extract_text_from_url(paper.get("url"))

    rating_list = []
    paper_chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    for chunk in paper_chunks:
        chunk_rating = round(float(analyze_similarity(prompt_text, chunk)), 2)
        rating_list.append(chunk_rating)

    return max(rating_list) if rating_list else 0.0  # Rückgabe der höchsten Chunk-Rating


def save_papers(paper, prompt_text: str = None):
    #rating_match = round(float(analyze_similarity(prompt_text, pdf_text)), 2)
    if accurate_mode:
        content = extract_text_from_url(paper.get("url"))
        rating_match = create_text_chunks_and_rate(paper, prompt_text)
        accurate = True
    else:
        content = None
        rating_match = round(float(analyze_similarity(prompt_text, paper["abstract"])), 2)
        accurate = False

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT OR REPLACE INTO papers (id, title, authors, abstract, url, source, rating, content, accurate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            paper["id"],
            paper["title"],
            paper["authors"],
            paper["abstract"],
            paper["url"],
            paper["source"],
            rating_match,
            content,
            accurate
        )
    )

    conn.commit()
    conn.close()

def return_sorted_papers():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM papers ORDER BY rating DESC")
    rows = cursor.fetchall()

    conn.close()

    return rows