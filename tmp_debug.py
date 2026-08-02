import traceback
from app.database import SessionLocal
from app.main import create_response
from app.schemas import SurveyResponseCreate

payload = SurveyResponseCreate(
    program='Informatyka',
    semester='III',
    study_mode='stacjonarny',
    academic_period='semestr zimowy',
    stress_level=4,
    fatigue_level=3,
    motivation_level=2,
    satisfaction_level=3,
    free_text='Jest sporo stresu przed egzaminami, ale ogólnie jest dobrze.'
)

try:
    db = SessionLocal()
    result = create_response(payload, db)
    print(result)
except Exception as e:
    traceback.print_exc()
finally:
    db.close()
