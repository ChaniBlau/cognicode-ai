import os
import certifi
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

# הגדרות תעודה לנטפרי
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=settings.GOOGLE_API_KEY
    )