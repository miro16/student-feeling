import json, requests
url = 'http://127.0.0.1:8000/responses/'
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
try:
    r = requests.post(url, json=payload, timeout=10)
    print('status', r.status_code)
    print(r.text)
except Exception as e:
    print('error', type(e).__name__, e)
