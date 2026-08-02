from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base


class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    student_id = Column(String(64), nullable=True, index=True)
    program = Column(String(128), nullable=True)
    semester = Column(String(32), nullable=True)
    study_mode = Column(String(32), nullable=True)
    academic_period = Column(String(64), nullable=True)
    stress_level = Column(Integer, nullable=False)
    fatigue_level = Column(Integer, nullable=False)
    motivation_level = Column(Integer, nullable=False)
    satisfaction_level = Column(Integer, nullable=False)
    free_text = Column(Text, nullable=True)
    sentiment = Column(String(32), nullable=True)
    keywords = Column(Text, nullable=True)
