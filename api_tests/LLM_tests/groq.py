
from openai import OpenAI
import os
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = client.responses.create(
    input="Give me as a output only 10 two to three word sentences, nothing more. Each text represents the following text as best as possible. The sentances are what could be used as part of a title of a Paper: Daniel Stenberg, der Programmierer von cURL, begann 1997 ein Programm zu schreiben, das IRC-Teilnehmern Daten über Wechselkurse zur Verfügung stellen sollte, welche von Webseiten abgerufen werden mussten. Er setzte dabei auf das vorhandene Open-Source-Tool httpget. Nach einer Erweiterung um andere Protokolle wurde das Programm am 20. März 1998 als cURL 4 erstmals veröffentlicht. Ursprünglich stand der Name für „see URL“ und wurde erst später von Stenberg nach einem besseren Vorschlag zum aktuellen Backronym umgedeutet.",
    model="openai/gpt-oss-20b",
)
print(response.output_text)

