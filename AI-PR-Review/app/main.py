from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import PullRequest
from app.schemas import PullRequestCreate


app = FastAPI()


# -------------------------
# Create DB tables
# -------------------------
PullRequest.metadata.create_all(bind=engine)


# -------------------------
# DB Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"message": "FastAPI + PostgreSQL working"}


# -------------------------
# GitHub Webhook Endpoint
# -------------------------
@app.post("/webhook/github")
def github_webhook(
    pr: PullRequestCreate,
    db: Session = Depends(get_db)
):
    db_pr = PullRequest(
        id=pr.id,
        title=pr.title,
        author=pr.author
    )

    db.add(db_pr)
    db.commit()
    db.refresh(db_pr)

    return {
        "message": "PR saved to database",
        "pr_id": db_pr.id
    }
