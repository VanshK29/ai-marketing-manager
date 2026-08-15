from crewai import Agent, LLM
from tools import web_search, analyze_campaign_performance, save_to_markdown
import os
from dotenv import load_dotenv
import crewai.llm

import time

original_call = LLM.call
def patched_call(self, messages, *args, **kwargs):
    for m in messages:
        if isinstance(m, dict) and 'cache_breakpoint' in m:
            del m['cache_breakpoint']
            
    max_retries = 5
    for attempt in range(max_retries):
        try:
            return original_call(self, messages, *args, **kwargs)
        except Exception as e:
            err_str = str(e)
            if "rate_limit_exceeded" in err_str or "429" in err_str or "RateLimitError" in err_str:
                print(f"Rate limit hit. Sleeping 12s before retry (Attempt {attempt+1}/{max_retries})...")
                time.sleep(12)
            else:
                raise e
    return original_call(self, messages, *args, **kwargs)

LLM.call = patched_call

load_dotenv()

def get_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        return None
    return LLM(model="groq/llama-3.1-8b-instant", api_key=groq_api_key)

def get_market_researcher():
    return Agent(
        role="Market Researcher",
        goal="Discover current marketing trends, customer sentiment, and emerging topics relevant to the given industry and campaign focus. Use web search to find real, up-to-date data.",
        backstory="You are an expert market researcher with a keen eye for spotting trends before they go mainstream. You excel at finding valuable insights from across the web. You always search for real data and never make up statistics.",
        tools=[web_search],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )

def get_competitor_analyst():
    return Agent(
        role="Competitor Analyst",
        goal="Analyze key competitors in the given industry, identifying their strengths, weaknesses, and market positioning. Use web search to find real competitor data.",
        backstory="You are a ruthless competitor analyst. You know exactly where to look to find what the competition is doing and how to exploit their weaknesses. You always search the web for real competitor information.",
        tools=[web_search],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )

def get_campaign_planner():
    return Agent(
        role="Campaign Planner",
        goal="Synthesize research and competitor analysis into a cohesive marketing strategy, defining budget, timeline, and target audience.",
        backstory="You are a seasoned Chief Marketing Officer. You take raw data and turn it into brilliant, actionable marketing campaigns that drive ROI.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=True
    )

def get_content_strategist():
    return Agent(
        role="Content Strategist",
        goal="Create detailed content plans, topics, formats, and drafts based on the campaign plan.",
        backstory="You are a creative genius. You know exactly what content formats work best on which channels and how to craft a message that resonates.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )

def get_analytics_specialist():
    return Agent(
        role="Analytics Specialist",
        goal="Research real-world marketing benchmarks and best practices relevant to the given campaign. Use the Campaign Performance Analyzer tool to find industry-specific data and optimization insights.",
        backstory="You are a data-driven marketing analyst. You research industry benchmarks, best practices, and real-world campaign performance data to provide actionable insights. You always use your tools to find real data.",
        tools=[analyze_campaign_performance, web_search],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )

def get_optimisation_advisor():
    return Agent(
        role="Optimisation Advisor",
        goal="Suggest strategic pivots and improvements based on the Analytics Specialist's findings.",
        backstory="You are a conversion rate optimization expert. You take data and turn it into actionable advice to squeeze every last drop of performance out of a campaign.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )
