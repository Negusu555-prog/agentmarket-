# ─────────────────────────────────────────────
# services/auth_service.py
#
# לוגיקה של Authentication:
# - הצפנת סיסמאות
# - יצירת JWT tokens
# - אימות tokens
# ─────────────────────────────────────────────

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user_model import UserModel
from models.user import UserRegister
import os

# ─── הגדרות ───────────────────────────────────
# SECRET_KEY = מפתח סודי לחתימת tokens
# חשוב: בproduction חייב להיות ב-.env
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
# כמה זמן ה-token תקף — 7 ימים
ACCESS_TOKEN_EXPIRE_DAYS = 7

# ─── Password Hashing ─────────────────────────
# CryptContext = מנהל הצפנת סיסמאות
# bcrypt = האלגוריתם — הכי מאובטח כיום
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    מצפין סיסמה גולמית.
    לעולם לא שומרים סיסמה ללא הצפנה!

    לדוגמה:
    "MyPassword123" → "$2b$12$xxxxxxxxxxxxx"
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    בודק אם סיסמה גולמית תואמת לסיסמה מוצפנת.
    מחזיר True אם תואמת, False אם לא.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, email: str) -> str:
    """
    יוצר JWT token למשתמש.

    JWT = JSON Web Token.
    מכיל מידע על המשתמש + חתימה דיגיטלית.
    אי אפשר לזייף בלי ה-SECRET_KEY.
    """
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    # payload = המידע שנכנס ל-token
    payload = {
        "sub": user_id,  # subject = מי המשתמש
        "email": email,
        "exp": expire  # מתי פג תוקף
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    """
    מפענח JWT token ומחזיר את המידע שבו.
    מחזיר None אם Token לא תקין או פג תוקף.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def register_user(db: Session, user_data: UserRegister) -> UserModel:
    """
    רושם משתמש חדש.
    1. בודק שהאימייל לא קיים
    2. מצפין סיסמה
    3. שומר ב-DB
    """
    # בדוק שהאימייל לא קיים כבר
    existing = db.query(UserModel) \
        .filter(UserModel.email == user_data.email) \
        .first()

    if existing:
        raise ValueError("האימייל כבר קיים במערכת")

    # צור משתמש חדש עם סיסמה מוצפנת
    new_user = UserModel(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, email: str, password: str) -> UserModel | None:
    """
    מאמת משתמש.
    1. מחפש לפי אימייל
    2. בודק סיסמה
    3. מחזיר משתמש אם הכל תקין
    """
    user = db.query(UserModel) \
        .filter(UserModel.email == email) \
        .first()

    # אם לא נמצא או סיסמה שגויה — None
    if not user or not verify_password(password, user.hashed_password):
        return None

    return user