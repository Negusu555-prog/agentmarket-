# ─────────────────────────────────────────────
# routers/auth.py
#
# Routes של Authentication:
# - הרשמה
# - התחברות
# - פרטי משתמש מחובר
# ─────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models.user import UserRegister, UserLogin, UserResponse, Token
from services.auth_service import (
    register_user,
    login_user,
    create_access_token,
    decode_token
)
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# HTTPBearer = מחלץ את ה-token מה-Header
# Authorization: Bearer <token>
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    רושם משתמש חדש.
    מחזיר את פרטי המשתמש — בלי סיסמה.
    """
    try:
        user = register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    מתחבר עם אימייל וסיסמה.
    מחזיר JWT token + פרטי משתמש.
    """
    user = login_user(db, user_data.email, user_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="אימייל או סיסמה שגויים"
        )

    # צור token
    token = create_access_token(user.id, user.email)

    return Token(
        access_token=token,
        token_type="bearer",
        user=user
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    מחזיר פרטי המשתמש המחובר.
    דורש token תקין ב-Header.
    """
    # חלץ את ה-token
    token = credentials.credentials

    # פענח את ה-token
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token לא תקין או פג תוקף"
        )

    # מצא את המשתמש ב-DB
    from models.user_model import UserModel
    user = db.query(UserModel)\
             .filter(UserModel.id == payload["sub"])\
             .first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="משתמש לא נמצא"
        )

    return user