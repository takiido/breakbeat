from fastapi import FastAPI
from sqlalchemy import text

from src.database import engine
from src.auth.router import router as auth_router


app = FastAPI(docs_url="/docs")


app.include_router(auth_router)


@app.on_event("startup")
def startup():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "breakbit-api"}
