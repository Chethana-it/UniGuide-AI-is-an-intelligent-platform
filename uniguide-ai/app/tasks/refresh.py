from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import ingest_service
from app.scrapers import discover_uni
import asyncio

router = APIRouter(prefix="/admin", tags=["admin"])

async def do_refresh(db: Session):
    # fetch new data
    data = await discover_uni.fetch_courses(limit=30)
    # here adapt to real structure
    for item in data.get("results", []):
        uni_name = item["provider"]["name"]
        course_name = item["title"]
        subject = item.get("subject")
        year = 2025
        requirements = ["AAA", "At least 1 science"]  # fallback if API doesn’t give
        ingest_service.save_course_with_requirements(
            db, uni_name, course_name, subject, year, requirements
        )

@router.post("/refresh-data")
def refresh_data(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # run async task in background
    background_tasks.add_task(asyncio.run, do_refresh(db))
    return {"status": "refresh started"}