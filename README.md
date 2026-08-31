# Student Feeling

System analizy samopoczucia studentów.

Pełna dokumentacja projektu znajduje się w pliku [DOCUMENTATION.md](DOCUMENTATION.md).

## Szybki start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

W drugim terminalu uruchom frontend:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```
