from sqlalchemy.orm import Session
from app.db import models

def upsert_university(db: Session, name: str):
    slug = name.lower().replace(" ", "-")
    uni = db.query(models.University).filter_by(slug=slug).first()
    if uni:
        return uni
    uni = models.University(name=name, slug=slug)
    db.add(uni)
    db.commit()
    db.refresh(uni)
    return uni

def save_course_with_requirements(db: Session, uni_name: str, course_name: str, subject: str | None, year: int, requirements: list[str]):
    uni = upsert_university(db, uni_name)

    course = models.Course(
        university_id=uni.id,
        name=course_name,
        subject_area=subject,
        year=year,
        data_source="discover_uni",
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    for req_text in requirements:
        er = models.EntryRequirement(
            course_id=course.id,
            level="A-level",
            requirements_text=req_text,
        )
        db.add(er)

    db.commit()
    return course