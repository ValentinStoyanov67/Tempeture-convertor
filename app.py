
import streamlit as st
import random

st.set_page_config(
    page_title="Температурен помощник",
    page_icon="🌡️",
    layout="centered"
)

# ДИЗАЙН И АНИМАЦИИ
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101c3a, #243b65, #176b87);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    animation: fadeIn 2s;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(-30px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes float {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-18px);}
    100% {transform: translateY(0px);}
}

@keyframes glow {
    0% {box-shadow: 0 0 5px #00d4ff;}
    50% {box-shadow: 0 0 25px #00d4ff;}
    100% {box-shadow: 0 0 5px #00d4ff;}
}

.weather-icon {
    text-align: center;
    font-size: 90px;
    animation: float 3s infinite ease-in-out;
}

.result-card {
    background: rgba(255,255,255,0.13);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    animation: fadeIn 1.5s;
    border: 1px solid rgba(255,255,255,0.3);
}

.stButton button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 15px;
    border: none;
    font-size: 18px;
    font-weight: bold;
    padding: 10px 25px;
    animation: glow 2s infinite;
}

.stButton button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)


# ЗАГЛАВИЕ
st.markdown(
    '<div class="main-title">🌡️ ТЕМПЕРАТУРЕН ПОМОЩНИК</div>',
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center'>Твоят личен помощник за времето! ☀️</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ВЪВЕЖДАНЕ НА ДАННИ
st
