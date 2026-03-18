# ─────────────────────────────────────────────
# database.py
#
# קובץ החיבור למסד הנתונים.
# כל הקוד שקשור לחיבור גר כאן —
# שאר הקבצים מייבאים מכאן.
# ─────────────────────────────────────────────

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Connection URL ───────────────────────────
# קורא את הכתובת מקובץ ה-.env
# אם לא נמצא — זורק שגיאה ברורה
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

# ─── Engine ───────────────────────────────────
# Engine = החיבור הראשי למסד הנתונים.
# echo=True אומר להדפיס כל SQL שרץ —
# שימושי לדיבאג, נכבה ב-production
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# ─── Session ──────────────────────────────────
# Session = "שיחה" עם מסד הנתונים.
# כל בקשה מהשרת פותחת session ומסגרת אותו.
# autocommit=False = שמור שינויים רק כשאנחנו מבקשים
# autoflush=False = אל תשלח ל-DB לפני שאנחנו מוכנים
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ─── Base ─────────────────────────────────────
# Base = אבא של כל המודלים שלנו.
# כל טבלה ב-DB תירש ממנו.
Base = declarative_base()


# ─── Dependency ───────────────────────────────
# פונקציה שFastAPI קורא לה לפני כל בקשה.
# פותחת session, מעבירה לroute, וסוגרת בסוף.
# yield = "תן את זה, ואחרי שגמרת — חזור לכאן"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()