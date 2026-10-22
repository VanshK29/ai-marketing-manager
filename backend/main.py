from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import io
import json
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from agents import get_campaign_planner, get_content_strategist, get_optimisation_advisor, get_llm
from models import CampaignPlan, ContentPlan
from crewai import Agent, Task, Crew

app = FastAPI(title="AI Marketing Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    industry: str
    campaign_focus: str

class ContentRequest(BaseModel):
    campaign_plan: dict

class OptimizeRequest(BaseModel):
    campaign_name: str

def _kickoff_single(agent: Agent, description: str, expected_output: str, pydantic_model=None):
    """Run a single-agent crew and return the result."""
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        output_pydantic=pydantic_model
    )
    crew = Crew(agents=[agent], tasks=[task], verbose=False)
    crew.kickoff()
    return task

def _extract_json(raw_text: str):
    try:
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return None

@app.post("/api/plan")
def generate_plan(request: PlanRequest):
    try:
        llm = get_llm()
        agent = Agent(
            role="Marketing Strategist",
            goal="Conduct market research, competitor analysis, and develop a full marketing campaign plan.",
            backstory=(
                "You are a world-class marketing strategist combining the expertise of a market researcher, "
                "competitor analyst, and Chief Marketing Officer. You deliver comprehensive campaign plans "
                "backed by deep market insight."
            ),
            llm=llm,
            verbose=False,
            allow_delegation=False
        )

        description = (
            f"You are tasked with developing a complete marketing campaign plan for a '{request.industry}' business "
            f"focused on '{request.campaign_focus}'.\n\n"
            f"In one comprehensive response, cover:\n"
            f"1. KEY MARKET TRENDS: Current trends in the {request.industry} industry relevant to '{request.campaign_focus}'\n"
            f"2. CONSUMER INSIGHTS: Target audience demographics, pain points, and motivations\n"
            f"3. COMPETITOR LANDSCAPE: 3 key competitors, their strengths/weaknesses, and gaps to exploit\n"
            f"4. CAMPAIGN PLAN: Full campaign name, target audience, key messages, recommended channels, timeline, and budget allocation"
        )

        task = _kickoff_single(
            agent=agent,
            description=description,
            expected_output="A structured marketing campaign plan with campaign name, target audience, key messages, channels, timeline, and budget allocation.",
            pydantic_model=CampaignPlan
        )

        if hasattr(task.output, 'pydantic') and task.output.pydantic:
            return task.output.pydantic.model_dump()
        raw_text = str(task.output)
        parsed = _extract_json(raw_text)
        if parsed:
            return parsed
        return {"raw_output": raw_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/content")
def generate_content(request: ContentRequest):
    try:
        llm = get_llm()
        agent = Agent(
            role="Content Strategist",
            goal="Create a detailed content calendar and drafts based on the campaign plan.",
            backstory=(
                "You are a creative Content Strategist who knows exactly what content formats work best "
                "on each channel and how to craft messages that resonate with the target audience."
            ),
            llm=llm,
            verbose=False,
            allow_delegation=False
        )

        plan_str = json.dumps(request.campaign_plan)
        task = _kickoff_single(
            agent=agent,
            description=f"Using this approved campaign plan: {plan_str}, create a detailed content calendar with specific topics, formats, and draft copy for each channel.",
            expected_output="A structured content plan with specific entries for different dates and channels.",
            pydantic_model=ContentPlan
        )

        if hasattr(task.output, 'pydantic') and task.output.pydantic:
            return task.output.pydantic.model_dump()
        raw_text = str(task.output)
        parsed = _extract_json(raw_text)
        if parsed:
            return parsed
        return {"raw_output": raw_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimize")
def optimize_campaign(request: OptimizeRequest):
    try:
        llm = get_llm()
        agent = Agent(
            role="Campaign Optimization Advisor",
            goal="Analyze campaign performance and provide actionable optimization recommendations.",
            backstory=(
                "You are a data-driven marketing analyst and conversion rate optimization expert. "
                "You evaluate campaign metrics, benchmark against industry standards, and provide "
                "prioritized recommendations to maximize ROI."
            ),
            llm=llm,
            verbose=False,
            allow_delegation=False
        )

        description = (
            f"Analyze the performance of the '{request.campaign_name}' campaign and provide a full optimization report.\n\n"
            f"Cover:\n"
            f"1. PERFORMANCE BENCHMARKS: Expected industry-standard KPIs (CTR, conversion rate, ROI) for this type of campaign\n"
            f"2. PERFORMANCE GAPS: Where the campaign likely underperforms vs benchmarks and why\n"
            f"3. SHORT-TERM WINS (0-30 days): Quick optimizations to implement immediately\n"
            f"4. MID-TERM STRATEGY (1-3 months): Channel mix adjustments, targeting refinements\n"
            f"5. LONG-TERM IMPROVEMENTS (3+ months): Structural changes for sustained growth"
        )

        task = _kickoff_single(
            agent=agent,
            description=description,
            expected_output="A detailed optimization report with benchmarks, performance gaps, and prioritized recommendations."
        )

        return {"optimization_report": str(task.output)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
