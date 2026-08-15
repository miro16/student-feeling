from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Union


class SurveyResponseCreate(BaseModel):
    student_id: Optional[str] = Field(None, description="Unikalny identyfikator studenta lub anonimowy kod")
    program: Optional[str] = Field(None, description="Kierunek studiów")
    semester: Optional[int] = Field(None, description="Semestr (numer)")
    study_mode: Optional[str] = Field(None, description="Tryb studiów")
    academic_period: Optional[str] = Field(None, description="Okres roku akademickiego")
    stress_level: int = Field(..., ge=1, le=5)
    fatigue_level: int = Field(..., ge=1, le=5)
    motivation_level: int = Field(..., ge=1, le=5)
    satisfaction_level: int = Field(..., ge=1, le=5)
    free_text: Optional[str] = Field(None, description="Dowolna krótka wypowiedź studenta")


class SurveyResponse(SurveyResponseCreate):
    id: int
    submitted_at: datetime
    semester: Optional[Union[int, str]]
    sentiment: Optional[str]
    keywords: Optional[str]

    model_config = {"from_attributes": True}
