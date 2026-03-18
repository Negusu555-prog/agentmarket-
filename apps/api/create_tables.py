# ─────────────────────────────────────────────
# create_tables.py
# ─────────────────────────────────────────────

from database import engine, Base
from models.agent_model import AgentModel
from models.user_model import UserModel
from models.validation_model import ValidationReport

def create_tables():
    print("יוצר טבלאות...")
    Base.metadata.create_all(bind=engine)
    print("הטבלאות נוצרו בהצלחה!")

if __name__ == "__main__":
    create_tables()