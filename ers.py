import streamlit as st
import random
import json
import os
from datetime import datetime

# ---------- НАСТРОЙКИ ----------
st.set_page_config(page_title="Edu App", page_icon="✨", layout="centered")

# ---------- СТИЛЬ ----------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

.main {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    color: white;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.big-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: white;
    margin-bottom: 20px;
}

.stButton>button {
    border-radius: 12px;
    background: linear-gradient(135deg, #ff7eb3, #ff758c);
    color: white;
    font-weight: bold;
    height: 3em;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #1f1c2c, #928dab);
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------- ФАЙЛЫ ----------
WORDS_FILE = "words.json"
TASKS_FILE = "tasks.json"

def load_data(file):
    if not os.path.exists(file):
        return []
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---------- SIDEBAR ----------
st.sidebar.title("✨ Edu App")
menu = st.sidebar.radio(
    "Навигация",
    ["📚 Флэш-карты", "🧠 Счёт", "📖 Слова", "📅 План"]
)

# ---------- 1. ФЛЭШ-КАРТЫ ----------
if menu == "📚 Флэш-карты":
    st.markdown('<div class="big-title">📚 Флэш-карты</div>', unsafe_allow_html=True)

    cards = [
        {"word": "apple", "translation": "яблоко"},
        {"word": "book", "translation": "книга"},
        {"word": "water", "translation": "вода"},
        {"word": "sun", "translation": "солнце"},
    ]

    card = random.choice(cards)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Слово")
    st.header(card["word"])

    if st.button("Показать перевод"):
        st.success(card["translation"])

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- 2. СЧЁТ ----------
elif menu == "🧠 Счёт":
    st.markdown('<div class="big-title">🧠 Устный счёт</div>', unsafe_allow_html=True)

    if "a" not in st.session_state:
        st.session_state.a = random.randint(1, 20)
        st.session_state.b = random.randint(1, 20)

    a = st.session_state.a
    b = st.session_state.b

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader(f"{a} + {b} = ?")
    answer = st.number_input("Ответ", step=1)

    if st.button("Проверить"):
        if answer == a + b:
            st.success("✅ Правильно!")
        else:
            st.error(f"❌ Ответ: {a + b}")

    if st.button("Новое задание"):
        st.session_state.a = random.randint(1, 20)
        st.session_state.b = random.randint(1, 20)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- 3. СЛОВА ----------
elif menu == "📖 Слова":
    st.markdown('<div class="big-title">📖 Слова</div>', unsafe_allow_html=True)

    data = load_data(WORDS_FILE)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    word = st.text_input("Слово")
    translation = st.text_input("Перевод")

    if st.button("Добавить"):
        if word and translation:
            data.append({
                "word": word,
                "translation": translation,
                "time": datetime.now().strftime("%H:%M")
            })
            save_data(WORDS_FILE, data)
            st.success("Добавлено!")
        else:
            st.warning("Заполни поля")

    st.markdown('</div>', unsafe_allow_html=True)

    for item in data:
        st.markdown(f"""
        <div class="card">
            <h3>{item['word']}</h3>
            <p>{item['translation']}</p>
            <small>{item['time']}</small>
        </div>
        """, unsafe_allow_html=True)

# ---------- 4. ПЛАН ----------
elif menu == "📅 План":
    st.markdown('<div class="big-title">📅 Планировщик</div>', unsafe_allow_html=True)

    tasks = load_data(TASKS_FILE)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    task = st.text_input("Задача")

    if st.button("Добавить задачу"):
        if task:
            tasks.append({
                "task": task,
                "time": datetime.now().strftime("%H:%M")
            })
            save_data(TASKS_FILE, tasks)
            st.success("Добавлено!")
        else:
            st.warning("Введите задачу")

    st.markdown('</div>', unsafe_allow_html=True)

    for t in tasks:
        st.markdown(f"""
        <div class="card">
            <p>• {t['task']}</p>
            <small>{t['time']}</small>
        </div>
        """, unsafe_allow_html=True)

    progress = len(tasks) / 10 if tasks else 0
    st.progress(min(progress, 1.0))

    if st.button("Очистить"):
        save_data(TASKS_FILE, [])
        st.warning("Список очищен")
        
