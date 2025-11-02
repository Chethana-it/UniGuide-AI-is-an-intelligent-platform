
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/")
def list_courses(
    university: str | None = None,
    subject: str | None = None,
    year: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Course).join(models.University)

    if university:
        query = query.filter(models.University.slug == university.lower())
    if subject:
        query = query.filter(models.Course.subject_area.ilike(f"%{subject}%"))
    if year:
        query = query.filter(models.Course.year == year)

    courses = query.all()

    # return with entry requirements
    result = []
    for c in courses:
        result.append({
            "course_id": c.id,
            "course_name": c.name,
            "university": c.university.name,
            "subject_area": c.subject_area,
            "year": c.year,
            "entry_requirements": [
                er.requirements_text for er in c.entry_requirements
            ]
        })
    return {"count": len(result), "data": result}
