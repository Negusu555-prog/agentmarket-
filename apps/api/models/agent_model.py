# ─────────────────────────────────────────────
# models/agent_model.py
#
# מגדיר את טבלת הסוכנים במסד הנתונים.
# כל class = טבלה.
# כל משתנה = עמודה בטבלה.
# ─────────────────────────────────────────────

from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base
import uuid


class AgentModel(Base):
    # שם הטבלה במסד הנתונים
    __tablename__ = "agents"

    # ─── עמודות ───────────────────────────────
    # primary_key=True = המזהה הייחודי של כל שורה
    # default = ערך ברירת מחדל אוטומטי
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # פרטי הסוכן
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    long_description = Column(String(5000), nullable=True)
    category = Column(String(50), nullable=False)
    api_endpoint = Column(String(500), nullable=False)

    # תמחור
    price_monthly = Column(Float, nullable=True)

    # סטטוס ואמינות
    status = Column(String(20), default="pending")
    trust_score = Column(Float, default=0.0)

    # מי יצר
    creator_id = Column(String, nullable=False)

    # סטטיסטיקות
    total_purchases = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)

    # האם מאומת על הבלוקציין
    on_chain_verified = Column(Boolean, default=False)
    nft_token_id = Column(String, nullable=True)

    # זמנים — נוצרים אוטומטית
    # server_default=func.now() = הDB ממלא את הזמן
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<Agent {self.name} ({self.status})>"