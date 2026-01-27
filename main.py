import streamlit as st
import requests
import streamlit.components.v1 as components

# БАПТАУЛАР
URL = "https://iuqdbdvmbewaedgydaah.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cWRiZHZtYmV3YWVkZ3lkYWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzMjE5ODgsImV4cCI6MjA4NDg5Nzk4OH0.a_PPVZWcA3qOfT4cNaXNE_a3xuSv0CHyrY8LbTgjWww"

st.set_page_config(page_title="СОЧ по Физике 9 класс", layout="wide")

# --- 1. КӨШІРУДЕН ҚОРҒАУ (CSS & JS) ---
st.markdown("""
    <style>
    * { -webkit-user-select: none; user-select: none; } /* Мәтінді белгілеуді өшіру */
    </style>
    <script>
    document.addEventListener('contextmenu', event => event.preventDefault()); // Оң жақ батырма
    document.onkeydown = function(e) {
        if (e.ctrlKey && (e.keyCode === 67 || e.keyCode === 85 || e.keyCode === 83)) return false; // Ctrl+C, U, S
    };
    </script>
    """, unsafe_allow_html=True)

# --- 2. ФУНКЦИЯЛАР ---
def post_to_supabase(data):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    return requests.post(f"{URL}/rest/v1/tjb_9_rus", json=data, headers=headers)

# --- 3. ИНТЕРФЕЙС ---
st.title("9 КЛАСС. СОЧ ПО ФИЗИКЕ")

with st.sidebar:
    st.header("Данные ученика")
    student_name = st.text_input("Имя и Фамилия:", key="name_input")
    student_class = st.selectbox("Класс:", ["9 А (рус)", "9 Б (рус)", "9 В (рус)"])

# --- 4. ANTI-CHEAT JS (Вкладкадан шыққанды бақылау) ---
if student_name:
    components.html(f"""
        <script>
        let timeout;
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                alert("ВНИМАНИЕ! У тебя есть 5 секунд, чтобы вернуться, иначе работа заблокируется!");
                timeout = setTimeout(function() {{
                    fetch('{URL}/rest/v1/tjb_9_rus', {{
                        method: 'POST',
                        headers: {{
                            'apikey': '{KEY}',
                            'Authorization': 'Bearer {KEY}',
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{
                            student_name: '{student_name}',
                            student_class: '{student_class}',
                            status: 'cheated',
                            ai_feedback: 'Работа аннулирована: зафиксирован выход из вкладки браузера.'
                        }})
                    }}).then(() => {{
                        window.location.reload();
                    }});
                }}, 5000); // 5 секунд
            }} else {{
                clearTimeout(timeout);
            }}
        }});
        </script>
    """, height=0)

# Тест формасы
with st.form("tjb_form_rus"):
    st.header("РАЗДЕЛ А")
    q1 = st.radio("1. Материальная точка прошла по окружности...", ["A) S = 2πR; l = 0", "B) S = 0; l = 2πR", "C) S = 0; l = 0", "D) S = 2πR; l = 2πR"], index=None)
    
    st.header("РАЗДЕЛ В")
    q11a = st.text_input("11а) Как называется явление сохранения скорости?")
    
    submit = st.form_submit_button("Завершить и отправить работу ✅")

if submit:
    if not student_name:
        st.error("Пожалуйста, введите Ваше имя!")
    else:
        all_answers = {"test": [q1], "b_section": {"11a": q11a}}
        payload = {
            "student_name": student_name,
            "student_class": student_class,
            "answers": all_answers,
            "status": "pending"
        }
        res = post_to_supabase(payload)
        if res.status_code in [200, 201]:
            st.success("Работа успешно принята!")

# Нәтижені іздеу бөлімі (өзіңнің кодың)
st.markdown("---")
search_name = st.text_input("Проверь результат (введи имя):")
if search_name:
    search_headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
    res = requests.get(f"{URL}/rest/v1/tjb_9_rus?student_name=eq.{search_name}&select=*&order=id.desc", headers=search_headers)
    if res.status_code == 200 and res.json():
        result = res.json()[0]
        if result['status'] == 'cheated':
            st.error(f"❌ {result['ai_feedback']}")
        elif result['status'] == 'pending':
            st.warning("⏳ Работа еще проверяется...")
        else:
            st.metric("Твой балл:", f"{result.get('score', '0')} / 25")
            st.info(result['ai_feedback'])