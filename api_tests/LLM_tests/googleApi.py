from google import genai

# NEVER save the API Key in the code ONLY in .env!!!! .env must always be in the .gitignore!!!! 
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
print(response.text)

