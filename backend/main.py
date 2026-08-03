from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Crew, Process
from typing import Dict, Any
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from tasks import create_planning_tasks, create_content_tasks, create_optimization_tasks
from agents import get_market_researcher, get_competitor_analyst, get_campaign_planner, get_content_strategist, get_analytics_specialist, get_optimisation_advisor

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

@app.post("/api/plan")
def generate_plan(request: PlanRequest):
    try:
        tasks = create_planning_tasks(request.industry, request.campaign_focus)
        
        crew = Crew(
            agents=[get_market_researcher(), get_competitor_analyst(), get_campaign_planner()],
            tasks=tasks,
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        final_task = tasks[-1]
        
        if hasattr(result, 'pydantic') and result.pydantic:
            return result.pydantic.model_dump()
        elif hasattr(final_task.output, 'pydantic') and final_task.output.pydantic:
            return final_task.output.pydantic.model_dump()
        else:
            return {"raw_output": str(result)}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/content")
def generate_content(request: ContentRequest):
    try:
        plan_str = json.dumps(request.campaign_plan)
        tasks = create_content_tasks(plan_str)
        
        crew = Crew(
            agents=[get_content_strategist()],
            tasks=tasks,
            verbose=False
        )
        
        result = crew.kickoff()
        final_task = tasks[-1]
        
        if hasattr(result, 'pydantic') and result.pydantic:
            return result.pydantic.model_dump()
        elif hasattr(final_task.output, 'pydantic') and final_task.output.pydantic:
            return final_task.output.pydantic.model_dump()
        else:
            return {"raw_output": str(result)}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimize")
def optimize_campaign(request: OptimizeRequest):
    try:
        tasks = create_optimization_tasks(request.campaign_name)
        
        crew = Crew(
            agents=[get_analytics_specialist(), get_optimisation_advisor()],
            tasks=tasks,
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        return {"optimization_report": str(result)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
