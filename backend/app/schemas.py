from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    prompt: str = Field(..., description="User task prompt")


class TaskResponse(BaseModel):
    plan: list[str]
    selected_skill: str | None
    tool_trace: list[dict]
    output: str
