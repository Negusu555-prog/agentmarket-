# ─────────────────────────────────────────────
# main.py — נקודת הכניסה לשרת
# ─────────────────────────────────────────────

from fastapi import FastAPI
from dotenv import load_dotenv
from routers import agents
import uvicorn

load_dotenv()

app = FastAPI(
    title="AgentMarket API",
    description="Verified AI Agent Marketplace",
    version="1.0.0"
)

# ─── חיבור Routers ────────────────────────────
# include_router מצרף את כל ה-routes
# מהקובץ agents.py לאפליקציה הראשית.
# עכשיו /agents/ ו-/agents/{id} זמינים.

app.include_router(agents.router)


# ─── Routes בסיסיים ───────────────────────────

@app.get("/")
def root():
    return {
        "message": "AgentMarket API is running!",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )