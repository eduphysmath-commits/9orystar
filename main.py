import streamlit as st
import requests
import streamlit.components.v1 as components
import json

# --- БАПТАУЛАР ---
URL = "https://iuqdbdvmbewaedgydaah.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cWRiZHZtYmV3YWVkZ3lkYWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzMjE5ODgsImV4cCI6MjA4NDg5Nzk4OH0.a_PPVZWcA3qOfT4cNaXNE_a3xuSv0CHyrY8LbTgjWww"

st.set_page_config(page_title="СОЧ по Физике 9 класс", layout="wide", page_icon="🪐")

# --- 0. СЕССИЯНЫ БАСҚАРУ (Тапсырылған жұмысты қадағалау) ---
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- 1. КӨШІРУДЕН ҚОРҒАУ (CSS & JS) ---
st.markdown("""
    <style>
    * { -webkit-user-select: none; user-select: none; } 
    .main { background-color: #f5f7f9; }
    </style>
    <script>
    document.addEventListener('contextmenu', event => event.preventDefault()); 
    document.onkeydown = function(e) {
        if (e.ctrlKey && (e.keyCode === 67 || e.keyCode === 85 || e.keyCode === 83 || e.keyCode === 73)) return false; 
    };
    </script>
    """, unsafe_allow_html=True)

# --- 2. ФУНКЦИЯЛАР ---
def post_to_supabase(data):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    return requests.post(f"{URL}/rest/v1/tjb_9_rus", json=data, headers=headers)

# --- 3. ИНТЕРФЕЙС ---
st.title("🪐 9 КЛАСС. СОЧ ПО ФИЗИКЕ (ОСНОВЫ ДИНАМИКИ)")

if not st.session_state.submitted:
    st.warning("⚠️ Внимание: Выход из вкладки браузера более чем на 5 секунд приведет к аннулированию работы!")
else:
    st.success("✅ Ваша работа успешно принята и находится на проверке.")

with st.sidebar:
    st.header("👤 Данные ученика")
    student_name = st.text_input("Имя и Фамилия:", placeholder="Напр: Иван Иванов", disabled=st.session_state.submitted)
    student_class = st.selectbox("Класс:", ["9 А (рус)", "9 Б (рус)", "9 В (рус)"], disabled=st.session_state.submitted)
    st.info("Время на выполнение: 45 минут")

# --- 4. ANTI-CHEAT JS (Тек тапсырылмаған кезде істейді) ---
if student_name and not st.session_state.submitted:
    components.html(f"""
        <script>
        let timeout;
        const alarm = new Audio('https://www.soundjay.com/buttons/beep-01a.mp3');
        alarm.loop = true;

        function speak(text) {{
            const msg = new SpeechSynthesisUtterance();
            msg.text = text;
            msg.lang = 'ru-RU';
            window.speechSynthesis.speak(msg);
        }}

        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                alarm.play();
                speak("Внимание! Немедленно вернись к тесту! У тебя осталось пять секунд!");
                
                timeout = setTimeout(function() {{
                    const data = {{
                        student_name: '{student_name}',
                        student_class: '{student_class}',
                        status: 'cheated',
                        ai_feedback: 'Работа АННУЛИРОВАНА: зафиксирован выход из вкладки браузера.'
                    }};
                    fetch('{URL}/rest/v1/tjb_9_rus', {{
                        method: 'POST',
                        headers: {{
                            'apikey': '{KEY}',
                            'Authorization': 'Bearer {KEY}',
                            'Content-Type': 'application/json',
                            'Prefer': 'return=minimal'
                        }},
                        body: JSON.stringify(data)
                    }}).then(() => {{
                        window.parent.location.reload();
                    }});
                }}, 5000);
            }} else {{
                clearTimeout(timeout);
                alarm.pause();
                alarm.currentTime = 0;
                window.speechSynthesis.cancel();
            }}
        }});
        </script>
    """, height=0)

# --- 5. ФОРМА ТЖБ ---
# Форма тек жұмыс тапсырылмаған кезде көрінеді
if not st.session_state.submitted:
    with st.form("tjb_form_rus"):
        st.header("📋 РАЗДЕЛ А: Тестовые задания (10 баллов)")
        q1 = st.radio("1. Материальная точка прошла по окружности и вернулась в исходную точку. Чему равны перемещение (S) и путь (l)?", 
                     ["A) S = 2πR; l = 0", "B) S = 0; l = 2πR", "C) S = 0; l = 0", "D) S = 2πR; l = 2πR"], index=None)
        q2 = st.radio("2. Какое ускорение получит тело массой 5 кг под действием силы 20 Н?", 
                     ["A) 100 м/с²", "B) 4 м/с²", "C) 0.25 м/с²", "D) 15 м/с²"], index=None)
        q3 = st.radio("3. Закон всемирного тяготения формулируется так:", 
                     ["A) F = ma", "B) F = mg", "C) F = G*(m1*m2)/r²", "D) F = kx"], index=None)

        st.header("📝 РАЗДЕЛ В: Задания с кратким ответом")
        q11a = st.text_input("11а) Как называется явление сохранения скорости тела при отсутствии внешних воздействий?")
        q12a = st.text_area("12а) Сформулируйте третий закон Ньютона:")
        q13b = st.text_input("13b) Какая планета является самой большой в Солнечной системе?")

        st.header("📊 РАЗДЕЛ С: Задача")
        st.write("14. Тело брошено горизонтально с высоты 20 м со скоростью 10 м/с.")
        q14a = st.text_input("а) Время падения (t) в секундах:")
        q14b = st.text_input("b) Дальность полета (L) в метрах:")

        submit = st.form_submit_button("Завершить и отправить работу ✅")

    if submit:
        if not student_name:
            st.error("❌ Ошибка: Введите имя и фамилию!")
        else:
            all_answers = {
                "test": [q1, q2, q3],
                "b_section": {"11a": q11a, "12a": q12a, "13b": q13b},
                "c_section": {"14a": q14a, "14b": q14b}
            }
            payload = {
                "student_name": student_name,
                "student_class": student_class,
                "answers": all_answers,
                "status": "pending"
            }
            res = post_to_supabase(payload)
            if res.status_code in [200, 201]:
                st.session_state.submitted = True # Анти-читты өшіру
                st.balloons()
                st.rerun() # Интерфейсті жаңарту

# --- 6. НӘТИЖЕНІ ІЗДЕУ ---
st.markdown("---")
st.subheader("🔎 Проверить свои результаты")
search_name = st.text_input("Введите ваше имя для поиска:", key="search_input")

if search_name:
    search_headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
    search_url = f"{URL}/rest/v1/tjb_9_rus?student_name=eq.{search_name}&select=*&order=id.desc"
    res = requests.get(search_url, headers=search_headers)
    
    if res.status_code == 200 and res.json():
        result = res.json()[0]
        if result['status'] == 'cheated':
            st.error(f"🚫 {result['student_name']}, твоя работа аннулирована.")
            st.info(f"Причина: {result['ai_feedback']}")
        elif result['status'] == 'pending':
            st.warning("⏳ Работа на проверке. Подождите 1-2 минуты.")
        elif result['status'] == 'done':
            st.success(f"✅ {result['student_name']}, работа проверена!")
            st.metric("Твой балл:", f"{result.get('score', 0)} / 25")
            st.markdown(f"""<div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;">{result['ai_feedback']}</div>""", unsafe_allow_html=True)
    else:
        st.info("🔍 Работа с таким именем не найдена.")