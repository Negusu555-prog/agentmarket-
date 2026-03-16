# ─────────────────────────────────────────────
# routers/agents.py
#
# ה-router רק מקבל בקשות ומחזיר תשובות.
# הלוגיקה עברה ל-agent_service.
# ─────────────────────────────────────────────

from fastapi import APIRouter, HTTPException
from models.agent import AgentCreate, AgentResponse
from services.agent_service import (
    get_all_agents,
    get_agent_by_id,
    create_agent
)

router = APIRouter(
    prefix="/agents",
    tags=["agents"]
)


@router.get("/", response_model=list[AgentResponse])
def get_agents():
    """מחזיר את כל הסוכנים המאושרים"""
    return get_all_agents()


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str):
    """מחזיר סוכן לפי ID"""
    agent = get_agent_by_id(agent_id)

    if not agent:
        raise HTTPException(
            status_code=404,
            detail=f"Agent {agent_id} not found"
        )

    return agent


@router.post("/", response_model=AgentResponse, status_code=201)
def create_new_agent(agent_data: AgentCreate):
    """יוצר סוכן חדש"""
    return create_agent(
        agent_data=agent_data,
        creator_id="temp-creator-id"
    )