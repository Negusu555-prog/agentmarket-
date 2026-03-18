# ─────────────────────────────────────────────
# services/agent_service.py
#
# הלוגיקה העסקית של סוכנים.
# עכשיו שומר ב-Supabase במקום בזיכרון.
# ─────────────────────────────────────────────

from sqlalchemy.orm import Session
from models.agent_model import AgentModel
from models.agent import AgentCreate, AgentStatus
import uuid


def get_all_agents(db: Session) -> list[AgentModel]:
    """
    מחזיר רק סוכנים מאושרים מהDB.
    """
    return db.query(AgentModel)\
             .filter(AgentModel.status == AgentStatus.APPROVED)\
             .all()


def get_agent_by_id(db: Session, agent_id: str) -> AgentModel | None:
    """
    מחפש סוכן לפי ID במסד הנתונים.
    מחזיר None אם לא נמצא.
    """
    return db.query(AgentModel)\
             .filter(AgentModel.id == agent_id)\
             .first()


def create_agent(db: Session, agent_data: AgentCreate, creator_id: str) -> AgentModel:
    """
    יוצר סוכן חדש ושומר ב-Supabase.
    """
    new_agent = AgentModel(
        id=str(uuid.uuid4()),
        name=agent_data.name,
        description=agent_data.description,
        long_description=agent_data.long_description,
        category=agent_data.category,
        api_endpoint=agent_data.api_endpoint,
        price_monthly=agent_data.price_monthly,
        status=AgentStatus.PENDING,
        trust_score=0.0,
        creator_id=creator_id,
        total_purchases=0,
        average_rating=0.0
    )

    # הוסף לDB
    db.add(new_agent)
    # שמור לDB
    db.commit()
    # רענן את האובייקט עם הנתונים מהDB
    db.refresh(new_agent)

    return new_agent


def update_trust_score(db: Session, agent_id: str, score: float) -> AgentModel | None:
    """
    מעדכן Trust Score ומחליט על סטטוס אוטומטית.
    """
    agent = get_agent_by_id(db, agent_id)
    if not agent:
        return None

    agent.trust_score = score

    if score >= 60:
        agent.status = AgentStatus.APPROVED
    elif score < 40:
        agent.status = AgentStatus.SUSPENDED

    db.commit()
    db.refresh(agent)

    return agent