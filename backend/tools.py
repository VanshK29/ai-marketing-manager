from crewai.tools import tool
from duckduckgo_search import DDGS
import random

@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web for information about marketing trends, competitors, and industry news."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return "No results found."
            formatted = [f"Title: {r.get('title')}\nSnippet: {r.get('body')}" for r in results]
            return "\n\n".join(formatted)
    except Exception as e:
        return f"Error performing search: {str(e)}"

@tool("Mock Analytics API")
def get_mock_analytics(campaign_name: str) -> str:
    """Retrieve simulated performance metrics for a given marketing campaign."""
    ctr = round(random.uniform(1.5, 5.0), 2)
    conversion_rate = round(random.uniform(0.5, 3.0), 2)
    roi = round(random.uniform(110.0, 350.0), 2)
    return f"Campaign: {campaign_name}\nClick-Through Rate: {ctr}%\nConversion Rate: {conversion_rate}%\nROI: {roi}%"

@tool("Save to Markdown")
def save_to_markdown(content: str, filename: str) -> str:
    """Save the final strategy or content calendar to a markdown file."""
    with open(f"{filename}.md", "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully saved to {filename}.md"
