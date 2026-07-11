from google import genai
from app.core.config import settings

print(settings.GEMINI_API_KEY[:10])

client = genai.Client(api_key=settings.GEMINI_API_KEY)

response = client.models.generate_content(
    model=settings.GEMINI_MODEL,
    contents="Say hello."
)

print(response.text)