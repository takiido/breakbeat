from fastapi import FastAPI
from sqlalchemy import text
from src.database import engine
from src.auth.utils import hash_password


app = FastAPI()


@app.on_event("startup")
def startup():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


@app.get("/")
def root() -> dict[str, str]:
    print(hash_password("123"))
    return {"status": "ok", "service": "breakbit-api"}
