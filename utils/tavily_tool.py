from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def web_search(query):

    result = client.search(
        query=query,
        search_depth="advanced",
        max_results=3
    )

    context = ""

    for item in result.get("results", []):

        context += item.get("content", "")
        context += "\n\n"

    return context