# ─────────────────────────────────────────────
# main.py — נקודת הכניסה לשרת
# ─────────────────────────────────────────────

from fastapi import FastAPI
from dotenv import load_dotenv
from routers import agents, auth, validation
import uvicorn

load_dotenv()

app = FastAPI(
    title="AgentMarket API",
    description="Verified AI Agent Marketplace",
    version="1.0.0"
)

# ─── חיבור Routers ────────────────────────────
app.include_router(agents.router)
app.include_router(auth.router)
app.include_router(validation.router)


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