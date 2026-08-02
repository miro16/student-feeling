from pydantic import BaseModel, Field
from typing import Optional


class SurveyResponseCreate(BaseModel):
    student_id: Optional[str] = Field(None, description="Unikalny identyfikator studenta lub anonimowy kod")
    program: Optional[str] = Field(None, description="Kierunek studiów")
    semester: Optional[str] = Field(None, description="Semestr")
    study_mode: Optional[str] = Field(None, description="Tryb studiów")
    academic_period: Optional[str] = Field(None, description="Okres roku akademickiego")
    stress_level: int = Field(..., ge=1, le=5)
    fatigue_level: int = Field(..., ge=1, le=5)
    motivation_level: int = Field(..., ge=1, le=5)
    satisfaction_level: int = Field(..., ge=1, le=5)
    free_text: Optional[str] = Field(None, description="Dowolna krótka wypowiedź studenta")


class SurveyResponse(SurveyResponseCreate):
    id: int
    submitted_at: str
    sentiment: Optional[str]
    keywords: Optional[str]

    class Config:
        orm_mode = True
