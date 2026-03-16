# ─────────────────────────────────────────────
# services/agent_service.py
#
# הלוגיקה העסקית של סוכנים.
# ה-router שואל "מה לעשות?"
# ה-service יודע "איך לעשות".
#
# למה להפריד?
# מחר נרצה לחבר מסד נתונים אמיתי —
# נשנה רק את ה-service, לא את ה-router.
# ─────────────────────────────────────────────

from models.agent import AgentCreate, AgentResponse, AgentStatus
import uuid
from datetime import datetime

# ─── מסד נתונים זמני ──────────────────────────
# רשימה בזיכרון — רק לפיתוח.
# בשלב הבא נחליף בPostgreSQL.
_agents_db: list[dict] = []


def get_all_agents() -> list[dict]:
    """
    מחזיר רק סוכנים מאושרים.
    לקוחות רואים רק סוכנים שעברו אימות.
    """
    return [
        a for a in _agents_db
        if a["status"] == AgentStatus.APPROVED
    ]


def get_agent_by_id(agent_id: str) -> dict | None:
    """
    מחפש סוכן לפי ID.
    מחזיר None אם לא נמצא.
    """
    return next(
        (a for a in _agents_db if a["id"] == agent_id),
        None
    )


def create_agent(agent_data: AgentCreate, creator_id: str) -> dict:
    """
    יוצר סוכן חדש ושומר אותו.

    agent_data  — הנתונים מהיוצר
    creator_id  — מי יצר (נקבל מה-auth בהמשך)
    """
    new_agent = {
        **agent_data.model_dump(),
        "id": str(uuid.uuid4()),
        "status": AgentStatus.PENDING,
        "trust_score": 0.0,
        "creator_id": creator_id,
        "total_purchases": 0,
        "average_rating": 0.0,
        "created_at": datetime.now().isoformat()
    }

    _agents_db.append(new_agent)
    return new_agent


def update_agent_status(agent_id: str, status: AgentStatus) -> dict | None:
    """
    מעדכן סטטוס סוכן.
    נשתמש בזה כשמנוע האימות גומר לבדוק.
    """
    agent = get_agent_by_id(agent_id)
    if not agent:
        return None

    agent["status"] = status
    return agent


def update_trust_score(agent_id: str, score: float) -> dict | None:
    """
    מעדכן Trust Score אחרי בדיקות.
    אם הציון גבוה מ-60 — מאשר את הסוכן אוטומטית.
    אם הציון נמוך מ-40 — משעה אוטומטית.
    """
    agent = get_agent_by_id(agent_id)
    if not agent:
        return None

    agent["trust_score"] = score

    # לוגיקה אוטומטית לפי הציון
    if score >= 60:
        agent["status"] = AgentStatus.APPROVED
    elif score < 40:
        agent["status"] = AgentStatus.SUSPENDED

    return agent