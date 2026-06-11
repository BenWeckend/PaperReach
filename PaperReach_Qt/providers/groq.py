import os
from openai import OpenAI
import tomllib
import sys
import os

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(current_dir) 

# Erstellt den absolut sicheren Pfad zur Datei
pyproject_path = os.path.join(base_path, "pyproject.toml")

# dynamischen Pfad laden
with open(pyproject_path, "rb") as f:
    config = tomllib.load(f)
    pass

query_count = config["project_Variablen"]["query_number"]

if __name__ == "__main__":
    print(f"Anzahl der Keywords, die von GROQ generiert werden: {query_count}")

def execute_groq_query(text):
    client = OpenAI(
        api_key=os.environ.get("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        timeout=30,
    )

    response = client.responses.create(
        input=(
            f"Give me as output only {query_count} two to four word sentences, "
            "nothing more. Each text represents the following text "
            "as best as possible. The sentences are what could be "
            "used as part of a title of a Paper: "
            + text
        ),
        model="openai/gpt-oss-20b",
    )
    
    return response.output_text

# Wirtschaftlich nicht sinnvoll da das zu viele "Tokens" verbraucht
def analyze_paper_content(text, content):
    client = OpenAI(
        api_key=os.environ.get("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        timeout=30,
    )

    response = client.responses.create(
        input=(
            "Given me a only a precise rating from 1 to 100 on how much the following paragraph or content: " + text + " matches "
            "the following content: " + content
        ),
        model="openai/gpt-oss-20b",
    )
    
    
    return response.output_text