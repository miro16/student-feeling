from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get('/responses/')
print(response.status_code)
print(response.text)
