# ─────────────────────────────────────────────
# routers/validation.py
#
# Routes של מנוע האימות.
#
# יש כאן 2 routes:
# 1. POST /validation/{agent_id} — מפעיל בדיקה
# 2. GET  /validation/{agent_id} — מחזיר תוצאות
#
# למה שני routes?
# כי הבדיקה לוקחת זמן —
# מפעילים ומחכים בנפרד.
# ─────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.validation_service import run_validation
from models.validation_model import ValidationReport

router = APIRouter(
    prefix="/validation",
    tags=["validation"]
)


@router.post("/{agent_id}")
async def validate_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """
    מפעיל בדיקת אימות על סוכן.

    async def — חשוב!
    הפונקציה הזו async כי היא קוראת ל-
    run_validation שהוא async.

    זמן ריצה: תלוי בסוכן — בין 10 שניות
    לכמה דקות.
    """
    try:
        report = await run_validation(db, agent_id)

        return {
            "message": "הבדיקה הסתיימה",
            "agent_id": agent_id,
            "trust_score": report.trust_score,
            "status": report.status,
            "checks": report.checks
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"שגיאה בבדיקה: {str(e)}"
        )


@router.get("/{agent_id}")
def get_validation_reports(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """
    מחזיר את כל דוחות הבדיקה של סוכן.

    שימושי כדי לראות היסטוריה —
    איך Trust Score השתנה לאורך זמן.
    """
    reports = db.query(ValidationReport)\
                .filter(ValidationReport.agent_id == agent_id)\
                .order_by(ValidationReport.started_at.desc())\
                .all()

    if not reports:
        raise HTTPException(
            status_code=404,
            detail=f"לא נמצאו דוחות לסוכן {agent_id}"
        )

    return {
        "agent_id": agent_id,
        "total_reports": len(reports),
        "reports": [
            {
                "id": r.id,
                "trust_score": r.trust_score,
                "status": r.status,
                "checks": r.checks,
                "started_at": r.started_at,
                "completed_at": r.completed_at,
                "validator_version": r.validator_version
            }
            for r in reports
        ]
    }