import streamlit as st
import pandas as pd
import random

# НАСТРОЙКИ
st.set_page_config(
    page_title="Температурен помощник PRO",
    page_icon="🌡️",
    layout="wide"
)

# SESSION STATE
if "history" not in st.session_state:
    st.session_state.history = []

# ДИЗАЙН
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10172e, #183b5b, #125b70);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    animation: appear 1.5s ease;
}

.subtitle {
    text-align: center;
    color: #bceaff !important;
    font-size: 18px;
}

@keyframes appear {
    from {opacity: 0; transform: translateY(-25px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes float {
    0%, 100% {transform: translateY(0);}
    50% {transform: translateY(-15px);}
}

.weather-icon {
    text-align: center;
    font-size: 100px;
    animation: float 3s infinite ease-in-out;
}

.result {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 22px;
    padding: 25px;
    text-align: center;
    margin: 15px 0;
    animation: appear 1s ease;
}

.stButton button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 14px;
    border: none;
    font-weight: bold;
    padding: 12px;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.04);
    box-shadow: 0 0 20px #00c6ff;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.10);
    padding: 15px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)


# ЗАГЛАВИЕ
st.markdown(
    '<div class="main-title">🌡️ ТЕМПЕРАТУРЕН ПОМОЩНИК PRO</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Твоят интелигентен помощник за температурите ☀️</p>',
    unsafe_allow_html=True
)

st.divider()

# СТРАНИЧНО МЕНЮ
st.sidebar.title("⚙️ Настройки")
st.sidebar.info("Добре дошъл в Temperature PRO!")

page = st.sidebar.radio(
    "Избери раздел:",
    ["🏠 Начало", "📊 История", "ℹ️ За приложението"]
)


# ОСНОВНА СТРАНИЦА
if page == "🏠 Начало":

    st.header("🌍 Провери температурата")

    col1, col2 = st.columns(2)

    with col1:
        temperature = st.number_input(
            "🌡️ Температура (°C)",
            min_value=-50,
            max_value=60,
            value=20,
            step=1
        )

        humidity = st.slider(
            "💧 Влажност (%)",
            0, 100, 50
        )

    with col2:
        wind = st.slider(
            "💨 Скорост на вятъра (km/h)",
            0, 100, 10
        )

        activity = st.selectbox(
            "🎯 Какво планираш?",
            [
                "Разходка",
                "Спорт",
                "Пътуване",
                "Работа навън",
                "Почивка вкъщи"
            ]
        )

    st.divider()

    if st.button("🚀 ПРОВЕРИ ТЕМПЕРАТУРАТА", use_container_width=True):

        if temperature < 0:
            icon = "🥶"
            message = "Ледено студено!"
            advice = "Облечи дебело яке, шапка и ръкавици."

        elif temperature < 10:
            icon = "❄️"
            message = "Студено е!"
            advice = "Подходящи са топло яке и шал."

        elif temperature < 20:
            icon = "🌥️"
            message = "Прохладно е!"
            advice = "Облечи суичър или леко яке."

        elif temperature < 30:
            icon = "☀️"
            message = "Приятно топло е!"
            advice = "Тениска и удобни дрехи са добър избор."

        else:
            icon = "🔥"
            message = "Много е горещо!"
            advice = "Носи леки дрехи и пий достатъчно вода."

        st.session_state.history.append({
            "Температура": temperature,
            "Влажност": humidity,
            "Вятър": wind
        })

        st.markdown(
            f"""
            <div class="result">
                <div class="weather-icon">{icon}</div>
                <h1>{temperature}°C</h1>
                <h2>{message}</h2>
                <p>{advice}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("📊 Допълнителна информация")

        a, b, c = st.columns(3)

        a.metric("🌡️ Температура", f"{temperature}°C")
        b.metric("💧 Влажност", f"{humidity}%")
        c.metric("💨 Вятър", f"{wind} km/h")

        st.subheader("👕 Твоите препоръки")

        st.success(f"Облекло: {advice}")
        st.info(f"Планирана дейност: {activity}")

        if humidity >= 75:
            st.warning("💧 Влажността е висока!")

        if wind >= 40:
            st.warning("💨 Внимавай със силния вятър!")

        if temperature >= 30:
            st.warning("🥤 Пий вода и избягвай продължително стоене на слънце!")

        if temperature < 0:
            st.snow()
        elif 20 <= temperature < 30:
            st.balloons()

        st.subheader("🌈 Температурна скала")

        st.progress((temperature + 50) / 110)

        st.caption(
            "❄️ Студено  |  🌥️ Прохладно  |  ☀️ Топло  |  🔥 Горещо"
        )

    else:
        st.markdown("""
        <div class="result">
            <div class="weather-icon">🌤️</div>
            <h2>Готов ли си?</h2>
            <p>Въведи температура и натисни бутона!</p>
        </div>
        """, unsafe_allow_html=True)


# ИСТОРИЯ
elif page == "📊 История":

    st.header("📊 История на проверките")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Графика на температурите")

        st.line_chart(df["Температура"])

        st.metric(
            "Средна температура",
            f"{df['Температура'].mean():.1f}°C"
        )

        if st.button("🗑️ Изчисти историята"):
            st.session_state.history = []
            st.rerun()

    else:
        st.info("Все още няма направени проверки.")


# ИНФОРМАЦИЯ
elif page == "ℹ️ За приложението":

    st.header("ℹ️ За Temperature PRO")

    st.markdown("""
    ### 🌡️ Какво може приложението?

    - Проверява температури от -50°C до 60°C.
    - Показва анимирани емоджита.
    - Дава съвети за облекло.
    - Проверява влажност и вятър.
    - Показва история на измерванията.
    - Създава графика на температурите.

    ### 🛠️ Използвани технологии

    - Python
    - Streamlit
    - Pandas
    - CSS

    ### ❤️ Създадено с желание за програмиране!
    """)

st.divider()

st.markdown(
    "<p style='text-align:center'>🌡️ Temperature PRO | "
    "Made with Python ❤️</p>",
    unsafe_allow_html=True
)
