# ─────────────────────────────────────────────
# create_tables.py
#
# יוצר את כל הטבלאות במסד הנתונים.
# ─────────────────────────────────────────────

from database import engine, Base
from models.agent_model import AgentModel
from models.user_model import UserModel

def create_tables():
    print("יוצר טבלאות...")
    Base.metadata.create_all(bind=engine)
    print("הטבלאות נוצרו בהצלחה!")

if __name__ == "__main__":
    create_tables()