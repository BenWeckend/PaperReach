import sqlite3
import pypdf
import requests
import io

from providers.groq import analyze_paper_content 

DB_NAME = "papers.db"

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
            pdf_content TEXT,
            rating INTEGER
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
    pdf_text = extract_text_from_url(paper.get("url"))
    rating_match = analyze_paper_content(prompt_text, pdf_text)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT OR REPLACE INTO papers (id, title, authors, abstract, url, source, pdf_content, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            paper["id"],
            paper["title"],
            ", ".join(paper["authors"]),
            paper["abstract"],
            paper["url"],
            paper["source"],
            pdf_text,
            rating_match
        )
    )

    conn.commit()
    conn.close()
