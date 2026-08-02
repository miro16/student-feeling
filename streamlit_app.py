import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/responses/"

st.title("Ankieta: samopoczucie studenta")

with st.form("survey"):
    student_id = st.text_input("ID studenta (opcjonalne)")
    program = st.text_input("Kierunek")
    semester = st.number_input("Semestr (numer)", min_value=1, max_value=20, value=1)
    study_mode = st.selectbox("Tryb studiów", ["stacjonarny", "niestacjonarny", "inny"])
    academic_period = st.text_input("Okres roku akademickiego")
    stress_level = st.slider("Poziom stresu", 1, 5, 3)
    fatigue_level = st.slider("Poziom zmęczenia", 1, 5, 3)
    motivation_level = st.slider("Poziom motywacji", 1, 5, 3)
    satisfaction_level = st.slider("Poziom zadowolenia", 1, 5, 3)
    free_text = st.text_area("Dodatkowy komentarz (opcjonalnie)")
    submitted = st.form_submit_button("Wyślij")

if submitted:
    payload = {
        "student_id": student_id or None,
        "program": program,
        "semester": int(semester) if semester is not None else None,
        "study_mode": study_mode,
        "academic_period": academic_period,
        "stress_level": int(stress_level),
        "fatigue_level": int(fatigue_level),
        "motivation_level": int(motivation_level),
        "satisfaction_level": int(satisfaction_level),
        "free_text": free_text or None,
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=5)
        if resp.ok:
            st.success("Dane wysłane poprawnie.")
            st.json(resp.json())
        else:
            st.error(f"Błąd serwera: {resp.status_code} - {resp.text}")
    except requests.RequestException as e:
        st.error(f"Nie udało się połączyć z API: {e}")
