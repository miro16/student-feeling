import json, urllib.request, urllib.error
url = 'http://127.0.0.1:8000/responses/'
payload = {
    'program': 'Informatyka',
    'semester': 'III',
    'study_mode': 'stacjonarny',
    'academic_period': 'semestr zimowy',
    'stress_level': 4,
    'fatigue_level': 3,
    'motivation_level': 2,
    'satisfaction_level': 3,
    'free_text': 'Jest sporo stresu przed egzaminami, ale ogólnie jest dobrze.'
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        print('status', resp.status)
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('status', e.code)
    print(e.read().decode())
except Exception as e:
    print('error', type(e).__name__, e)
