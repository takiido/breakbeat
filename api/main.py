from fastapi import FastAPI
from sqlalchemy import text
from src.database import engine


app = FastAPI()


@app.on_event("startup")
def startup():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("database connected")


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": "breakbit-api"}
