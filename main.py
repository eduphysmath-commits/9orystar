import streamlit as st
import requests
import streamlit.components.v1 as components
import json

# --- 1. БАЗА БАПТАУЛАРЫ ---
URL = "https://iuqdbdvmbewaedgydaah.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cWRiZHZtYmV3YWVkZ3lkYWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzMjE5ODgsImV4cCI6MjA4NDg5Nzk4OH0.a_PPVZWcA3qOfT4cNaXNE_a3xuSv0CHyrY8LbTgjWww"

st.set_page_config(page_title="СОЧ Физика 9 класс", layout="wide")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- 2. СТИЛЬ ---
st.markdown("""
    <style>
    * { -webkit-user-select: none; user-select: none; } 
    .stRadio > div { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

def send_data(payload):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    return requests.post(f"{URL}/rest/v1/tjb_9_rus", json=payload, headers=headers)

# --- 3. БАСТЫ БЕТ ---
st.title("🪐 СОЧ по Физике — 9 класс")

# ЕГЕР ТЕСТ ТАПСЫРЫЛСА
if st.session_state.submitted:
    st.balloons()
    st.success("✅ Ваша работа успешно принята! Вы можете проверить результат в поиске ниже.")
else:
    # ТЕСТ ТАПСЫРЫЛМАҒАН БОЛСА ҒАНА КӨРСЕТУ
    st.info("Введите данные и начните тест. Внимание: выход из вкладки аннулирует работу!")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Имя и Фамилия:", placeholder="Напр: Иван Иванов")
    with col2:
        s_class = st.selectbox("Класс:", ["9 А (рус)", "9 Б (рус)", "9 В (рус)"])

    if name:
        # --- ANTI-CHEAT JS (МҮЛДЕМ ЖАҢА ЛОГИКА) ---
        components.html(f"""
            <script>
            // Дыбысты бірден тоқтату
            window.speechSynthesis.cancel();
            
            let isSubmitting = false; // Тест біткенін білдіретін жалауша

            function speak(text) {{
                if (isSubmitting) return; // Егер тест тапсырылып жатса, сөйлемеу
                window.speechSynthesis.cancel();
                const msg = new SpeechSynthesisUtterance(text);
                msg.lang = 'ru-RU';
                window.speechSynthesis.speak(msg);
            }}

            // Беттен шығуды бақылау
            document.addEventListener("visibilitychange", function() {{
                if (document.hidden && !isSubmitting) {{
                    speak("Внимание! Вернитесь к тесту!");
                    
                    setTimeout(function() {{
                        // Егер 5 секунд ішінде қайтып келмесе және тест тапсырылмаса
                        if (document.hidden && !isSubmitting) {{
                            fetch('{URL}/rest/v1/tjb_9_rus', {{
                                method: 'POST',
                                headers: {{ 'apikey': '{KEY}', 'Authorization': 'Bearer {KEY}', 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{
                                    student_name: "{name}",
                                    student_class: "{s_class}",
                                    status: "cheated",
                                    ai_feedback: "Работа АННУЛИРОВАНА: зафиксирован выход из вкладки."
                                }})
                            }}).then(() => {{ 
                                isSubmitting = true;
                                window.speechSynthesis.cancel();
                                window.parent.location.reload(); 
                            }});
                        }}
                    }}, 5000);
                }} else {{
                    window.speechSynthesis.cancel();
                }}
            }});

            // Бет жаңарғанда (unload) дыбысты күшпен өшіру
            window.onbeforeunload = function() {{
                isSubmitting = true;
                window.speechSynthesis.cancel();
            }};
            </script>
        """, height=0)

        # ТЕСТ ФОРМАСЫ
        with st.form("exam_form"):
            st.subheader("📍 Раздел А: Тестовые задания")
            q1 = st.radio("1. Материальная точка, двигаясь по окружности, вернулась в исходную точку. Какими будут перемещение (S) и пройденный путь (l)?", ["A) S = 2πR; l = 0", "B) S = 0; l = 2πR", "C) S = 0; l = 0", "D) S = 2πR; l = 2πR"], index=None)
            q2 = st.radio("2. Тело в течение 5 секунд равномерно увеличило свою скорость от 0 до 10 м/с. Определите ускорение тела.", ["A) 5 м/с²", "B) 2 м/с²", "C) 10 м/с²", "D) 0 м/с²"], index=None)
            q3 = st.radio("3. Как называются постоянные группы звезд?", ["A) Галактики", "B) Планеты", "C) Созвездия", "D) Туманности"], index=None)
            q4 = st.radio("4. Какую систему мы называем инерциальной системой отсчета?", ["A) Ускоренную", "B) В покое или равномерную", "C) Криволинейную", "D) Любую"], index=None)
            q5 = st.radio("5. Формула силы тяжести:", ["A) F = kx", "B) F = μN", "C) F = mg", "D) F = ma"], index=None)
            q6 = st.radio("6. Согласно третьему закону Ньютона, силы:", ["A) Равны и противоположны", "B) Уравновешивают друг друга", "C) В одну сторону", "D) Только в покое"], index=None)
            q7 = st.radio("7. Если расстояние увеличить в 2 раза, сила притяжения:", ["A) Увеличится в 2", "B) Уменьшится в 2", "C) Увеличится в 4", "D) Уменьшится в 4"], index=None)
            q8 = st.radio("8. Траектория планет по 1-му закону Кеплера:", ["A) Окружность", "B) Эллипс", "C) Парабола", "D) Прямая"], index=None)
            q9 = st.radio("9. Формула центростремительного ускорения:", ["A) a = v / t", "B) a = v² / R", "C) a = ωR", "D) a = 4π²R"], index=None)
            q10 = st.radio("10. Вес при свободном падении (a=g):", ["A) P = mg", "B) P = 2mg", "C) P = 0", "D) P = m(g-a)"], index=None)

            st.subheader("📍 Раздел B и C: Задания")
            q11a = st.text_input("11а. Как называется явление наклона пассажиров?")
            q11b = st.text_input("11б. Пример инерции из жизни:")
            q12a = st.text_area("12а. Вычислите ускорение (m=2кг, F=8Н):")
            q12b = st.text_area("12б. Если силу увеличить в 2 раза, что будет?")
            q13a = st.text_input("13а. Различие между звездой и планетой:")
            q13b = st.text_input("13б. Самая большая планета:")
            q14a = st.text_input("14а. Время падения h=20м:")
            q14b = st.text_input("14б. Дальность полета L (v0=10):")
            q14c = st.text_input("14в. Форма траектории:")

            submitted_btn = st.form_submit_button("ЗАВЕРШИТЬ РАБОТУ ✅")

            if submitted_btn:
                all_answers = {
                    "section_a": [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10],
                    "section_b": {"11": [q11a, q11b], "12": [q12a, q12b], "13": [q13a, q13b]},
                    "section_c": {"14": [q14a, q14b, q14c]}
                }
                
                payload = {
                    "student_name": name, "student_class": s_class,
                    "answers": json.dumps(all_answers), "status": "pending"
                }
                
                resp = send_data(payload)
                if resp.status_code in [200, 201]:
                    # Бетті жаңарту алдында submitted күйін қосамыз
                    st.session_state.submitted = True
                    st.rerun()

# --- 4. НӘТИЖЕНІ ІЗДЕУ ---
st.markdown("---")
st.subheader("🔎 Результаты")
search_query = st.text_input("Введите имя для поиска:")
if search_query:
    res = requests.get(f"{URL}/rest/v1/tjb_9_rus?student_name=eq.{search_query}&select=*&order=id.desc", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    if res.json():
        data = res.json()[0]
        if data['status'] == 'cheated': st.error("🚫 Работа аннулирована за выход из вкладки.")
        elif data['status'] == 'pending': st.warning("⏳ Проверяется...")
        else:
            st.success(f"✅ Ваш балл: {data.get('score', 0)} / 25")
            st.info(f"💬 Отзыв: {data.get('ai_feedback', '')}")