from crewai import Task
from agents import (
    get_market_researcher, get_competitor_analyst, get_campaign_planner,
    get_content_strategist, get_analytics_specialist, get_optimisation_advisor
)
from models import CampaignPlan, ContentPlan

def create_planning_tasks(industry: str, campaign_focus: str):
    researcher = get_market_researcher()
    analyst = get_competitor_analyst()
    planner = get_campaign_planner()
    
    task1 = Task(
        description=f"Conduct deep market research on the {industry} industry, focusing on trends related to '{campaign_focus}'. Identify key consumer pain points and emerging opportunities.",
        expected_output="A comprehensive market research report outlining current trends, audience demographics, and emerging opportunities.",
        agent=researcher
    )

    task2 = Task(
        description=f"Analyze top competitors in the {industry} space related to '{campaign_focus}'. Identify their strengths, weaknesses, and marketing gaps.",
        expected_output="A detailed competitor analysis report highlighting at least 3 competitors, their strategies, and potential gaps to exploit.",
        agent=analyst
    )

    task3 = Task(
        description=f"Based on the market research and competitor analysis, develop a full marketing campaign plan for '{campaign_focus}'. Define the target audience, budget, timeline, and key channels.",
        expected_output="A structured marketing campaign plan.",
        agent=planner,
        output_pydantic=CampaignPlan
    )

    return [task1, task2, task3]

def create_content_tasks(campaign_plan_json: str):
    content_strategist = get_content_strategist()

    task = Task(
        description=f"Using this approved campaign plan: {campaign_plan_json}, create a detailed content calendar with specific topics, formats, and drafts for each channel.",
        expected_output="A structured content plan containing specific entries for different dates and channels.",
        agent=content_strategist,
        output_pydantic=ContentPlan
    )

    return [task]

def create_optimization_tasks(campaign_name: str):
    analytics = get_analytics_specialist()
    advisor = get_optimisation_advisor()

    task1 = Task(
        description=f"Research real-world marketing benchmarks and best practices for a campaign like '{campaign_name}'. Use the Campaign Performance Analyzer tool to search for industry-specific data, then provide a detailed analysis of what metrics to expect and what optimization opportunities exist.",
        expected_output="A data-driven report with real industry benchmarks, expected KPIs (CTR, conversion rate, ROI), and key performance insights specific to this type of campaign.",
        agent=analytics
    )

    task2 = Task(
        description=f"Based on the analytics report for the '{campaign_name}' campaign, suggest specific, actionable improvements to optimize the campaign's performance and ROI. Search the web for proven optimization strategies if needed.",
        expected_output="A strategic optimization document with specific, actionable recommendations organized by priority (short-term, mid-term, long-term).",
        agent=advisor
    )

    return [task1, task2]

