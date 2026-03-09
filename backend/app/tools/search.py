from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

def search_web(query: str):
    api_key = os.getenv("TAVILY_API_KEY")
    
    # בדיקה אם המפתח קיים לפני הניסיון להתחבר
    if not api_key:
        return "Search skipped: No TAVILY_API_KEY found in environment variables."

    try:
        tavily = TavilyClient(api_key=api_key)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        
        context = ""
        for res in search_result['results']:
            context += f"\nSource: {res['url']}\nContent: {res['content']}\n"
        return context
    except Exception as e:
        return f"Search failed due to technical error: {str(e)}"