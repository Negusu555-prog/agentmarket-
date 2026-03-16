# ─────────────────────────────────────────────
# models/agent.py
#
# מגדיר איך סוכן AI נראה במערכת שלנו.
# כל בקשה וכל תשובה שקשורה לסוכן
# עוברת דרך המודלים האלה.
# ─────────────────────────────────────────────

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ─── Enums ────────────────────────────────────
# Enum = רשימה של ערכים אפשריים.
# במקום לכתוב מחרוזת חופשית כמו "sales" או "SALES"
# או "Sales" — Enum מבטיח שרק ערכים מוגדרים עוברים.

class AgentCategory(str, Enum):
    SALES = "sales"
    MARKETING = "marketing"
    HR = "hr"
    CUSTOMER_SERVICE = "customer_service"
    DATA_ANALYSIS = "data_analysis"
    DEVELOPMENT = "development"
    FINANCE = "finance"
    OTHER = "other"


class AgentStatus(str, Enum):
    PENDING = "pending"        # הוגש, ממתין לאימות
    VALIDATING = "validating"  # בודקים אותו עכשיו
    APPROVED = "approved"      # מאושר, חי במרקטפלייס
    REJECTED = "rejected"      # נכשל בבדיקות
    SUSPENDED = "suspended"    # הושעה


# ─── Models ───────────────────────────────────

class AgentBase(BaseModel):
    """
    השדות המשותפים לכל פעולה.
    בסיס שממנו יורשים מודלים אחרים.
    """
    name: str = Field(
        min_length=3,
        max_length=100,
        description="שם הסוכן"
    )
    description: str = Field(
        min_length=10,
        max_length=500,
        description="תיאור קצר"
    )
    category: AgentCategory
    price_monthly: Optional[float] = Field(
        default=None,
        ge=0,  # ge = greater or equal, לא יכול להיות שלילי
        description="מחיר חודשי בדולרים"
    )


class AgentCreate(AgentBase):
    """
    מה שיוצר שולח כשהוא מגיש סוכן חדש.
    יורש מ-AgentBase ומוסיף שדות נוספים.
    """
    api_endpoint: str = Field(
        description="כתובת ה-API של הסוכן"
    )
    long_description: str = Field(
        min_length=50,
        max_length=5000,
        description="תיאור מפורט"
    )


class AgentResponse(AgentBase):
    """
    מה שהשרת מחזיר ללקוח.
    כולל שדות שהשרת מוסיף — ID, סטטוס, ציון.
    """
    id: str
    status: AgentStatus
    trust_score: float = Field(
        ge=0,
        le=100,
        description="ציון אמינות 0-100"
    )
    creator_id: str
    total_purchases: int = 0
    average_rating: float = 0.0

    # model_config אומר ל-Pydantic לקרוא
    # נתונים גם מאובייקטים (לא רק מ-dict)
    model_config = {"from_attributes": True}