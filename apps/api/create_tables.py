# ─────────────────────────────────────────────
# create_tables.py
#
# סקריפט חד פעמי שיוצר את הטבלאות
# במסד הנתונים.
# מריצים אותו פעם אחת — ואחר כך לא צריך.
# ─────────────────────────────────────────────

from database import engine, Base

# מייבא את כל המודלים כדי ש-Base יכיר אותם
from models.agent_model import AgentModel

def create_tables():
    print("יוצר טבלאות...")

    # Base.metadata.create_all = עבור על כל המודלים
    # שיורשים מ-Base וצור את הטבלאות שלהם
    # אם הטבלה כבר קיימת — לא יגע בה
    Base.metadata.create_all(bind=engine)

    print("הטבלאות נוצרו בהצלחה!")


if __name__ == "__main__":
    create_tables()