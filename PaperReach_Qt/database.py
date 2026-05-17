import sqlite3
import pypdf
import requests
import io
import time

from pathlib import Path

from embeddings import analyze_similarity

version = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

db_path = Path("./databases")
db_path.mkdir(parents=True, exist_ok=True)

DB_NAME = str(db_path / f"papers_{version}.db")

DB_PROVISORISCH = "./databases/papers_2026-05-16_16-40-20.db"

def get_db_connection():
    return sqlite3.connect(DB_PROVISORISCH)

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
            rating REAL
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

def save_papers(paper, prompt_text: str = None):
    #pdf_text = extract_text_from_url(paper.get("url"))
    #rating_match = round(float(analyze_similarity(prompt_text, pdf_text)), 2)
    rating_match = round(float(analyze_similarity(prompt_text, paper["abstract"])), 2)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT OR REPLACE INTO papers (id, title, authors, abstract, url, source, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            paper["id"],
            paper["title"],
            paper["authors"],
            paper["abstract"],
            paper["url"],
            paper["source"],
            rating_match
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