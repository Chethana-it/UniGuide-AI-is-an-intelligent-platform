from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    courses = relationship("Course", back_populates="university")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    subject_area = Column(String, index=True)
    year = Column(Integer)
    data_source = Column(String)
    external_id = Column(String)

    university = relationship("University", back_populates="courses")
    entry_requirements = relationship("EntryRequirement", back_populates="course")

class EntryRequirement(Base):
    __tablename__ = "entry_requirements"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    level = Column(String, nullable=True)
    requirements_text = Column(Text, nullable=False)

    course = relationship("Course", back_populates="entry_requirements")