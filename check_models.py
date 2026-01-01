from google import genai

# Use your API key here
client = genai.Client(api_key='AIzaSyAkBhYxYBlMwRjTL6zgDDhR0Qjtyq_CTkA')

print("Checking available models for your account...")
for model in client.models.list():
    print(f"- {model.name}")