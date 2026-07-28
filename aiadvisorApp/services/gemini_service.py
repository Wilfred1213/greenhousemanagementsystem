from django.conf import settings
from google import genai


class GeminiService:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def ask(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-3.6-flash",  # Updated to an active model
            contents=prompt,
        )

        return response.text