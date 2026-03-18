# ─────────────────────────────────────────────
# models/validation_model.py
#
# מגדיר את טבלת תוצאות הבדיקות.
#
# למה טבלה נפרדת ולא לשמור ב-agents?
# כי כל סוכן עובר בדיקות כמה פעמים —
# פעם אחת כשמוגש, ואחת כל 24 שעות.
# רוצים היסטוריה מלאה של כל הבדיקות.
# ─────────────────────────────────────────────

from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from database import Base
import uuid


class ValidationReport(Base):
    __tablename__ = "validation_reports"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # איזה סוכן נבדק
    agent_id = Column(String, nullable=False)

    # תוצאה כללית
    status = Column(String(20), nullable=False)  # "passed" / "failed"
    trust_score = Column(Float, nullable=False)

    # תוצאות כל בדיקה בנפרד — JSON מאפשר לשמור
    # מבנה גמיש בתוך עמודה אחת
    # לדוגמה:
    # {
    #   "response_time": {"score": 85, "passed": true},
    #   "accuracy": {"score": 90, "passed": true},
    #   ...
    # }
    checks = Column(JSON, nullable=False)

    # גרסת המנוע — חשוב לדעת איזו גרסה בדקה
    # אם נשפר את המנוע בעתיד — נדע לחשב מחדש
    validator_version = Column(String(10), default="1.0.0")

    # זמנים
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<ValidationReport agent={self.agent_id} score={self.trust_score}>"