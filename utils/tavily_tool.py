from tavily import TavilyClient
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def web_search(query):

    result = client.search(
        query=query,
        search_depth="basic",
        max_results=1
    )

    if result.get("results"):

        content = result["results"][0]["content"]

        # remove markdown symbols
        content = re.sub(r"#", "", content)
        content = content.replace("*", "")

        result["results"][0]["content"] = content

    return result