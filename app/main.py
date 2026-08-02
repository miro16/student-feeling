from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="System analizy samopoczucia studentów")


@app.post("/responses/", response_model=schemas.SurveyResponse)
def create_response(response: schemas.SurveyResponseCreate, db: Session = Depends(get_db)):
    db_response = models.SurveyResponse(
        student_id=response.student_id,
        program=response.program,
        semester=response.semester,
        study_mode=response.study_mode,
        academic_period=response.academic_period,
        stress_level=response.stress_level,
        fatigue_level=response.fatigue_level,
        motivation_level=response.motivation_level,
        satisfaction_level=response.satisfaction_level,
        free_text=response.free_text,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


@app.get("/responses/{response_id}", response_model=schemas.SurveyResponse)
def read_response(response_id: int, db: Session = Depends(get_db)):
    db_response = db.query(models.SurveyResponse).filter(models.SurveyResponse.id == response_id).first()
    if not db_response:
        raise HTTPException(status_code=404, detail="Response not found")
    return db_response


@app.get("/responses/")
def list_responses(db: Session = Depends(get_db)):
    return db.query(models.SurveyResponse).order_by(models.SurveyResponse.submitted_at.desc()).all()
