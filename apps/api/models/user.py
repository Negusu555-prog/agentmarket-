# ─────────────────────────────────────────────
# models/user.py
#
# מודלי Pydantic למשתמשים.
# מגדיר מה נכנס ומה יוצא בכל בקשה.
# ─────────────────────────────────────────────

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    """
    מה המשתמש שולח כשנרשם.
    EmailStr = Pydantic מאמת שזה אימייל תקין.
    """
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2, max_length=100)
    role: str = Field(default="buyer")


class UserLogin(BaseModel):
    """
    מה המשתמש שולח כשמתחבר.
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    מה שהשרת מחזיר — בלי הסיסמה!
    לעולם לא מחזירים סיסמה ללקוח.
    """
    id: str
    email: str
    full_name: str
    role: str
    is_verified: bool
    is_active: bool
    wallet_address: Optional[str] = None

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """
    הטוקן שמחזירים אחרי התחברות מוצלחת.
    access_token = ה-JWT token
    token_type = תמיד "bearer"
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse