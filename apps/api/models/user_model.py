# ─────────────────────────────────────────────
# models/user_model.py
#
# מגדיר את טבלת המשתמשים במסד הנתונים.
# כל מי שנרשם למערכת — יוצר וקונה —
# מאוחסן כאן.
# ─────────────────────────────────────────────

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base
import uuid


class UserModel(Base):
    __tablename__ = "users"

    # ─── עמודות ───────────────────────────────
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # פרטי המשתמש
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(100), nullable=False)

    # תפקיד — creator יכול להגיש סוכנים
    # buyer יכול לקנות בלבד
    role = Column(String(20), default="buyer")

    # האם המשתמש אימת את האימייל שלו
    is_verified = Column(Boolean, default=False)

    # האם המשתמש פעיל — אפשר לחסום
    is_active = Column(Boolean, default=True)

    # ארנק Web3 — אופציונלי
    wallet_address = Column(String, nullable=True)

    # זמנים אוטומטיים
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
        return f"<User {self.email} ({self.role})>"