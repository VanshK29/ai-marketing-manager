from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web for information about marketing trends, competitors, and industry news."""
    try:
        # Simplify long queries to first few key terms to improve search success
        words = query.replace('"', '').replace("'", "").split()
        clean_query = " ".join(words[:6]) if len(words) > 6 else query
        with DDGS() as ddgs:
            results = list(ddgs.text(clean_query, max_results=3))
            if not results:
                return f"No external search results found for '{clean_query}'. Please use your extensive marketing expertise to complete the analysis."
            formatted = [f"Title: {r.get('title')}\nSnippet: {r.get('body')}" for r in results]
            return "\n\n".join(formatted)
    except Exception as e:
        return f"Search service unavailable. Please use your domain expertise to complete the analysis."

@tool("Campaign Performance Analyzer")
def analyze_campaign_performance(campaign_name: str) -> str:
    """Search the web for real-world marketing benchmarks and best practices related to the given campaign to provide data-driven optimization insights."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"{campaign_name} marketing campaign best practices benchmarks optimization tips", max_results=5))
            if not results:
                return f"No benchmark data found for '{campaign_name}'. Provide general optimization recommendations based on your expertise."
            formatted = [f"Title: {r.get('title')}\nInsight: {r.get('body')}" for r in results]
            return f"Industry benchmarks and optimization insights for '{campaign_name}':\n\n" + "\n\n".join(formatted)
    except Exception as e:
        return f"Could not fetch benchmarks: {str(e)}. Provide optimization recommendations based on your expertise."

@tool("Save to Markdown")
def save_to_markdown(content: str, filename: str) -> str:
    """Save the final strategy or content calendar to a markdown file."""
    with open(f"{filename}.md", "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully saved to {filename}.md"

