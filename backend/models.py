from pydantic import BaseModel, Field
from typing import List

class CompetitorAnalysis(BaseModel):
    competitors: List[str] = Field(description="List of key competitors identified")
    strengths: List[str] = Field(description="Key strengths of the competitors")
    weaknesses: List[str] = Field(description="Key weaknesses of the competitors")
    market_positioning: str = Field(description="Overall market positioning analysis")

class CampaignPlan(BaseModel):
    campaign_name: str = Field(description="Name of the marketing campaign")
    target_audience: str = Field(description="Description of the target audience")
    key_messages: List[str] = Field(description="Key messages to convey")
    channels: List[str] = Field(description="Marketing channels to use")
    timeline: str = Field(description="Estimated timeline for the campaign")
    budget_allocation: str = Field(description="Proposed budget allocation across channels")

class ContentCalendarEntry(BaseModel):
    date_or_phase: str = Field(description="Date or phase of the content release")
    channel: str = Field(description="Distribution channel (e.g., Blog, Twitter, Email)")
    topic: str = Field(description="Topic of the content")
    format: str = Field(description="Format of the content (e.g., Video, Article, Thread)")
    draft_content: str = Field(description="Draft or outline of the content itself")

class ContentPlan(BaseModel):
    entries: List[ContentCalendarEntry] = Field(description="List of content calendar entries")
