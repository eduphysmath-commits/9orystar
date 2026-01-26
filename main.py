import streamlit as st
import requests

# БАПТАУЛАР (Өз мәліметтеріңізді қойыңыз)
URL = "https://iuqdbdvmbewaedgydaah.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1cWRiZHZtYmV3YWVkZ3lkYWFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkzMjE5ODgsImV4cCI6MjA4NDg5Nzk4OH0.a_PPVZWcA3qOfT4cNaXNE_a3xuSv0CHyrY8LbTgjWww" # eyJ... деп басталатын ұзын кілт

def post_to_supabase(data):
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    # МАНЫЗДЫ: Мұнда жаңа кесте tjb_9_rus қолданылады
    return requests.post(f"{URL}/rest/v1/tjb_9_rus", json=data, headers=headers)

st.set_page_config(page_title="СОЧ по Физике 9 класс", layout="wide")
st.title("9 КЛАСС. СОЧ ПО ФИЗИКЕ (ОСНОВЫ ДИНАМИКИ)")
st.info("Время: 45 минут | Максимальный балл: 25")

with st.sidebar:
    st.header("Данные ученика")
    student_name = st.text_input("Имя и Фамилия:")
    student_class = st.selectbox("Класс:", ["9 А (рус)", "9 Б (рус)", "9 В (рус)"])

with st.form("tjb_form_rus"):
    st.header("РАЗДЕЛ А: Тестовые задания (10 баллов)")
    # Тест сұрақтарын осында қосыңыз (сіздің нұсқаңыздағыдай)
    q1 = st.radio("1. Материальная точка прошла по окружности и вернулась в исходную точку. Чему равны перемещение (S) и путь (l)?", ["A) S = 2πR; l = 0", "B) S = 0; l = 2πR", "C) S = 0; l = 0", "D) S = 2πR; l = 2πR"], index=None)
    q2 = st.radio("2. Тело за 5 секунд увеличило скорость от 0 до 10 м/с. Чему равно ускорение?", ["A) 5 м/с²", "B) 2 м/с²", "C) 10 м/с²", "D) 0 м/с²"], index=None)
    # ... қалған тест сұрақтары ...

    st.header("РАЗДЕЛ В: Задания с кратким ответом (12 баллов)")
    q11a = st.text_input("11а) Как называется явление сохранения скорости тела при отсутствии внешних воздействий?")
    q12a = st.text_input("12а) Чему равно ускорение тела (F=8H, m=2кг)?")
    q13b = st.text_input("13b) Самая большая планета Солнечной системы:")

    st.header("РАЗДЕЛ С: Задание на анализ (3 балла)")
    q14a = st.text_input("14а) Время падения (t) при h=20м:")

    submit = st.form_submit_button("Завершить и отправить работу ✅")

if submit:
    if not student_name:
        st.error("Пожалуйста, введите Ваше имя!")
    else:
        all_answers = {
            "test": [q1, q2], # Барлық тест жауаптарын қосыңыз
            "b_section": {"11a": q11a, "12a": q12a, "13b": q13b},
            "c_section": {"14a": q14a}
        }
        res = post_to_supabase({"student_name": student_name, "student_class": student_class, "answers": all_answers, "status": "pending"})
        if res.status_code in [200, 201]:
            st.success("Работа успешно принята! Проверь результат через 2 минуты внизу.")

# ИЗДЕУ БӨЛІМІ
st.markdown("---")
st.subheader("🔎 Проверь свой результат")
search_name = st.text_input("Введите имя (как в бланке):")
if search_name:
    headers = {"apikey": KEY, "Authorization": f"Bearer {KEY}"}
    res = requests.get(f"{URL}/rest/v1/tjb_9_rus?student_name=eq.{search_name}&select=*&order=id.desc", headers=headers)
    if res.status_code == 200 and res.json():
        result = res.json()[0]
        if result['status'] == 'pending':
            st.warning("⏳ Работа еще проверяется ИИ...")
        else:
            st.metric("Твой балл:", f"{result.get('score', '0')} / 25")
            st.markdown(f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>{result['ai_feedback']}</div>", unsafe_allow_html=True)
    else:
        st.info("Работа не найдена.")