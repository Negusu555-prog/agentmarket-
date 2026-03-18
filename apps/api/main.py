# ─────────────────────────────────────────────
# main.py — נקודת הכניסה לשרת
# ─────────────────────────────────────────────

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import agents, auth, validation
import uvicorn

load_dotenv()

app = FastAPI(
    title="AgentMarket API",
    description="Verified AI Agent Marketplace",
    version="1.0.0"
)

# ─── CORS ─────────────────────────────────────
# מאפשר לפרונטאנד לדבר עם הבאקנד.
# בפיתוח — מאפשרים הכל.
# בproduction — נגביל לכתובת האמיתית בלבד.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────
app.include_router(agents.router)
app.include_router(auth.router)
app.include_router(validation.router)


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