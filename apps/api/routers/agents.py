# ─────────────────────────────────────────────
# routers/agents.py
#
# עכשיו מקבל DB session בכל בקשה
# ומעביר אותו ל-service.
# ─────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.agent import AgentCreate, AgentResponse
from services.agent_service import (
    get_all_agents,
    get_agent_by_id,
    create_agent
)
from database import get_db

router = APIRouter(
    prefix="/agents",
    tags=["agents"]
)


@router.get("/", response_model=list[AgentResponse])
def get_agents(db: Session = Depends(get_db)):
    """
    מחזיר את כל הסוכנים המאושרים.
    Depends(get_db) = FastAPI פותח session
    ומעביר אותו לפונקציה אוטומטית.
    """
    return get_all_agents(db)


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """מחזיר סוכן לפי ID"""
    agent = get_agent_by_id(db, agent_id)

    if not agent:
        raise HTTPException(
            status_code=404,
            detail=f"Agent {agent_id} not found"
        )

    return agent


@router.post("/", response_model=AgentResponse, status_code=201)
def create_new_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db)
):
    """יוצר סוכן חדש ושומר ב-Supabase"""
    return create_agent(
        db=db,
        agent_data=agent_data,
        creator_id="temp-creator-id"
    )