import sqlite3
from app.main import app
from fastapi.testclient import TestClient

conn = sqlite3.connect('student_feeling.db')
cur = conn.cursor()
cur.execute("PRAGMA table_info(survey_responses);")
print('schema:', cur.fetchall())
cur.execute('SELECT COUNT(*) FROM survey_responses')
print('rows in table:', cur.fetchone()[0])
conn.close()

client = TestClient(app)
payload = {
    'student_id': 'anon123',
    'program': 'Informatyka',
    'semester': 3,
    'study_mode': 'stacjonarny',
    'academic_period': 'semestr zimowy',
    'stress_level': 4,
    'fatigue_level': 3,
    'motivation_level': 2,
    'satisfaction_level': 3,
    'free_text': 'Jest sporo stresu przed egzaminami, ale ogólnie jest dobrze.'
}
r = client.post('/responses/', json=payload)
print('status', r.status_code)
print('body', r.text)
