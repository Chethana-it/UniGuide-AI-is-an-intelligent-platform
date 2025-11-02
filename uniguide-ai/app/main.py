from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.v1.courses import router as courses_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="UniGuide AI")

app.include_router(courses_router, prefix="/api/v1")
