import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Ankieta: samopoczucie studenta", layout="wide")

API_URL = "http://127.0.0.1:8000/responses/"

view = st.sidebar.radio("Widok", ["Formularz", "Wszystkie odpowiedzi", "Analiza wyników"])

st.title("Ankieta: samopoczucie studenta")


def show_form():
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
                response_data = resp.json()

                with st.expander("Szczegóły wysłanej ankiety"):
                    st.write("### Dane wysłane do API")
                    st.table({
                        "Pola": [
                            "ID studenta",
                            "Kierunek",
                            "Semestr",
                            "Tryb studiów",
                            "Okres roku akademickiego",
                            "Poziom stresu",
                            "Poziom zmęczenia",
                            "Poziom motywacji",
                            "Poziom zadowolenia",
                            "Komentarz",
                        ],
                        "Wartości": [
                            payload["student_id"],
                            payload["program"],
                            payload["semester"],
                            payload["study_mode"],
                            payload["academic_period"],
                            payload["stress_level"],
                            payload["fatigue_level"],
                            payload["motivation_level"],
                            payload["satisfaction_level"],
                            payload["free_text"],
                        ],
                    })

                st.write("### Odpowiedź API")
                api_summary = [
                    {"Pole": "ID wpisu", "Wartość": response_data.get("id")},
                    {"Pole": "Data przesłania", "Wartość": response_data.get("submitted_at")},
                    {"Pole": "Sentyment", "Wartość": response_data.get("sentiment") or "brak"},
                    {"Pole": "Wykryte tematy", "Wartość": response_data.get("keywords") or "brak"},
                ]
                st.table(api_summary)

                if response_data.get("sentiment") or response_data.get("keywords"):
                    st.divider()
                    st.write("#### Analiza tekstu")
                    st.write(
                        f"Sentyment: **{response_data.get('sentiment') or 'brak'}**  \n"
                        f"Wykryte tematy: **{response_data.get('keywords') or 'brak'}**"
                    )
            else:
                st.error(f"Błąd serwera: {resp.status_code} - {resp.text}")
        except requests.RequestException as e:
            st.error(f"Nie udało się połączyć z API: {e}")


def show_responses():
    st.write("## Wszystkie odpowiedzi")
    try:
        resp = requests.get(API_URL, timeout=5)
        if resp.ok:
            responses = resp.json()
            if not responses:
                st.info("Brak zapisanych odpowiedzi.")
                return

            df = pd.DataFrame(responses)
            df["submitted_at"] = pd.to_datetime(df["submitted_at"], errors="coerce")
            df["semester"] = df["semester"].astype(str)

            visible_columns = [
                "id",
                "submitted_at",
                "student_id",
                "program",
                "semester",
                "study_mode",
                "academic_period",
                "stress_level",
                "fatigue_level",
                "motivation_level",
                "satisfaction_level",
                "sentiment",
                "keywords",
                "free_text",
            ]
            visible_columns = [c for c in visible_columns if c in df.columns]
            df = df[visible_columns]

            st.markdown(f"**Liczba odpowiedzi:** {len(df)}")
            if "program" in df.columns:
                program_options = ["Wszystkie"] + sorted(df["program"].dropna().unique())
                selected_program = st.selectbox("Filtruj po kierunku", program_options)
                if selected_program != "Wszystkie":
                    df = df[df["program"] == selected_program]

            if "semester" in df.columns:
                semester_options = ["Wszystkie"] + sorted(df["semester"].dropna().unique(), key=lambda x: (str(x).isdigit(), str(x)))
                selected_semester = st.selectbox("Filtruj po semestrze", semester_options)
                if selected_semester != "Wszystkie":
                    df = df[df["semester"] == selected_semester]

            st.dataframe(df, use_container_width=True)
        else:
            st.error(f"Błąd serwera: {resp.status_code} - {resp.text}")
    except requests.RequestException as e:
        st.error(f"Nie udało się pobrać odpowiedzi: {e}")


def show_analysis():
    st.write("## Analiza wyników")
    try:
        resp = requests.get(API_URL, timeout=5)
        if resp.ok:
            responses = resp.json()
            if not responses:
                st.info("Brak zapisanych odpowiedzi do analizy.")
                return

            df = pd.DataFrame(responses)
            df["submitted_at"] = pd.to_datetime(df["submitted_at"], errors="coerce")
            df["semester_int"] = df["semester"].apply(lambda v: int(v) if isinstance(v, int) else (int(v) if str(v).isdigit() else None))

            numeric_cols = ["stress_level", "fatigue_level", "motivation_level", "satisfaction_level"]
            summary = df[numeric_cols].mean().round(2).to_dict()
            total = len(df)

            st.metric("Liczba odpowiedzi", total)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Średni stres", summary.get("stress_level", 0))
            col2.metric("Średnie zmęczenie", summary.get("fatigue_level", 0))
            col3.metric("Średnia motywacja", summary.get("motivation_level", 0))
            col4.metric("Średnia satysfakcja", summary.get("satisfaction_level", 0))

            st.write("### Rozkład sentymentu")
            sentiment_counts = df["sentiment"].fillna("brak").value_counts()
            st.bar_chart(sentiment_counts)

            st.write("### Odpowiedzi według semestru")
            semester_counts = df["semester_int"].fillna(-1).astype(int).value_counts().sort_index()
            st.bar_chart(semester_counts)

            st.write("### Trend średnich wyników w czasie")
            if not df["submitted_at"].isna().all():
                trend = df.set_index("submitted_at")[numeric_cols].resample("D").mean()
                if not trend.empty:
                    st.line_chart(trend)
                else:
                    st.info("Za mało danych czasowych, by wyświetlić trend.")
            else:
                st.info("Brak poprawnych dat przesłania w danych.")

            st.write("### Średnie wg kierunku")
            st.dataframe(
                df.groupby("program")[numeric_cols].mean().round(2).sort_values("stress_level", ascending=False)
            )
        else:
            st.error(f"Błąd serwera: {resp.status_code} - {resp.text}")
    except requests.RequestException as e:
        st.error(f"Nie udało się pobrać odpowiedzi: {e}")


if view == "Formularz":
    show_form()
elif view == "Wszystkie odpowiedzi":
    show_responses()
else:
    show_analysis()
