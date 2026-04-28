from google import genai

# The client automatically uses the environment variable GEMINI_API_KEY
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash",  # Adjust the name here
    contents="Explain how AI works in a few words."
)

print(response.text)

