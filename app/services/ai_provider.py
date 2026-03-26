# app/services/ai_provider.py
from app.core.config import AI_PROVIDER
import json

class AIProvider:
    def get_embedding(self, text: str):
        raise NotImplementedError

    def parse_query(self, query: str):
        raise NotImplementedError


# 🔹 OpenAI Implementation
from openai import OpenAI, OpenAIError
from app.core.config import OPENAI_API_KEY

class OpenAIProvider(AIProvider):
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def get_embedding(self, text: str):
        res = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=text
        )
        return res.data[0].embedding

    def parse_query(self, query: str):
        prompt = f"""
        Extract structured filters from the query.

        Query: "{query}"

        Return ONLY JSON (no text, no explanation).

        Allowed fields:
        type, category, color, pattern, print

        Example:
        {{
        "type": "t-shirt",
        "print": "avengers"
        }}
        """
        try:
            res = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            content = res.choices[0].message.content.strip()

            try:
                return json.loads(content)
            except:
                return {}  # fallback
        except OpenAIError as e:
            raise Exception(f"LLM Error: {str(e)}")


# 🔹 Factory
def get_ai_provider():
    if AI_PROVIDER == "openai":
        return OpenAIProvider()

    # Future: OllamaProvider
    raise Exception("Unsupported provider")