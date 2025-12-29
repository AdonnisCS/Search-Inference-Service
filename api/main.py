import os
import psycopg2
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Search + Rerank MVP")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise HTTPException(status_code=500, detail="DATABASE_URL not set")

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM ping;")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {"db": "ok", "ping_rows": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")


