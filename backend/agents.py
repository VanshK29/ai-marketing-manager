from crewai import Agent, LLM
from tools import web_search, analyze_campaign_performance, save_to_markdown
import os
from dotenv import load_dotenv
import crewai.llm

import time

import litellm
import time

_orig_litellm_completion = litellm.completion

def _clean_messages(msgs):
    if not msgs:
        return msgs
    for m in msgs:
        if isinstance(m, dict):
            m.pop('cache_breakpoint', None)
        elif hasattr(m, 'cache_breakpoint'):
            delattr(m, 'cache_breakpoint')
    return msgs

def _patched_litellm_completion(*args, **kwargs):
    if 'messages' in kwargs:
        _clean_messages(kwargs['messages'])
    if len(args) > 1 and isinstance(args[1], list):
        _clean_messages(args[1])
    if kwargs.get('tool_choice') == 'required':
        kwargs['tool_choice'] = 'auto'
        
    max_retries = 5
    for attempt in range(max_retries):
        try:
            return _orig_litellm_completion(*args, **kwargs)
        except Exception as e:
            err_str = str(e)
            if "rate_limit_exceeded" in err_str or "429" in err_str or "RateLimitError" in err_str or "503" in err_str or "UNAVAILABLE" in err_str:
                wait_time = 3 if ("503" in err_str or "UNAVAILABLE" in err_str) else 10
                print(f"Transient error ({err_str[:60]}...). Sleeping {wait_time}s before retry ({attempt+1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise e
    return _orig_litellm_completion(*args, **kwargs)

litellm.completion = _patched_litellm_completion

load_dotenv()

def get_llm():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
        return LLM(model="gemini/gemini-3.5-flash", api_key=gemini_api_key)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key and groq_api_key != "your_groq_api_key_here":
        return LLM(model="groq/openai/gpt-oss-20b", api_key=groq_api_key)
    return None

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
        allow_delegation=False
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
