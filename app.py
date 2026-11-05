import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ==========================================
# WEATHER PRO MAX
# ==========================================

st.set_page_config(
    page_title="Weather PRO MAX",
    page_icon="🌦️",
    layout="wide"
)

# ==========================================
# CSS DESIGN AND ANIMATIONS
# ==========================================

st.markdown("""
<style>
.stApp {
    background:
    radial-gradient(circle at top left, #164e75 0%, transparent 40%),
    linear-gradient(135deg, #081526, #102b46, #123e58);
    color: white;
}

header, footer {
    visibility: hidden;
}

h1, h2, h3, p, label {
    color: white !important;
}

.hero {
    text-align: center;
    padding: 25px;
    border-radius: 25px;
    background: linear-gradient(120deg,
    rgba(0,198,255,.18),
    rgba(0,114,255,.12));
    border: 1px solid rgba(255,255,255,.15);
    animation: appear 1.2s ease;
}

.hero h1 {
    font-size: 46px;
    font-weight: 900;
    letter-spacing: 2px;
}

.hero p {
    color: #b8eaff !important;
    font-size: 17px;
}

@keyframes appear {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes float {
    0%, 100% {transform: translateY(0);}
    50% {transform: translateY(-13px);}
}

@keyframes glow {
    0%, 100% {box-shadow: 0 0 8px #00bfff;}
    50% {box-shadow: 0 0 25px #00bfff;}
}

.weather-icon {
    font-size: 95px;
    text-align: center;
    animation: float 3s infinite ease-in-out;
}

.weather-card {
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(255,255,255,.16);
    padding: 22px;
    border-radius: 20px;
    text-align: center;
    min-height: 145px;
}

.weather-card h2 {
    font-size: 32px;
}

.big-temperature {
    font-size: 65px;
    font-weight: 900;
    text-align: center;
    color: #ffffff;
}

.stButton button {
    background: linear-gradient(90deg, #00bfff, #0066ff);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px;
    font-weight: bold;
    transition: .3s;
}

.stButton button:hover {
    transform: scale(1.03);
    animation: glow 1.5s infinite;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,.09);
    border: 1px solid rgba(255,255,255,.12);
    padding: 16px;
    border-radius: 17px;
}

div[data-testid="stTabs"] button {
    color: white;
}

hr {
    border-color: rgba(255,255,255,.2);
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# WEATHER CODE TRANSLATION
# ==========================================

def weather_info(code, is_day=1):

    if code == 0:
        return ("☀️" if is_day else "🌙",
                "Ясно")

    elif code in [1, 2]:
        return ("🌤️" if is_day else "🌙",
                "Предимно ясно")

    elif code == 3:
        return ("☁️", "Облачно")

    elif code in [45, 48]:
        return ("🌫️", "Мъгла")

    elif code in [51, 53, 55, 56, 57]:
        return ("🌦️", "Ръмеж")

    elif code in [61, 63, 65, 66, 67]:
        return ("🌧️", "Дъжд")

    elif code in [71, 73, 75, 77]:
        return ("❄️", "Сняг")

    elif code in [80, 81, 82]:
        return ("🌧️", "Превалявания")

    elif code in [85, 86]:
        return ("🌨️", "Снеговалеж")

    elif code in [95, 96, 99]:
        return ("⛈️", "Гръмотевична буря")

    return ("🌍", "Неизвестно")


# ==========================================
# API FUNCTIONS
# ==========================================

@st.cache_data(ttl=1800)
def search_city(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    response = requests.get(
        url,
        params={
            "name": city,
            "count": 10,
            "language": "bg",
            "format": "json"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json().get("results", [])


@st.cache_data(ttl=900)
def get_weather(lat, lon, days, unit):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "rain",
            "showers",
            "snowfall",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m"
        ],
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation_probability",
            "weather_code",
            "wind_speed_10m"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "uv_index_max",
            "sunrise",
            "sunset"
        ],
        "timezone": "auto",
        "forecast_days": days,
        "temperature_unit": unit,
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🌦️ WEATHER PRO MAX</h1>
    <p>Твоята професионална метеорологична станция</p>
    <p>Реална прогноза • Анализи • Температури</p>
</div>
""", unsafe_allow_html=True)

st.write("")


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙️ Настройки")

page = st.sidebar.radio(
    "Навигация",
    [
        "🏠 Начало",
        "📅 7-дневна прогноза",
        "⏰ Почасова прогноза",
        "📊 Анализи",
        "ℹ️ За проекта"
    ]
)

st.sidebar.divider()

unit_name = st.sidebar.radio(
    "Температурна единица",
    ["Целзий °C", "Фаренхайт °F"]
)

unit = "celsius" if unit_name == "Целзий °C" else "fahrenheit"

days = st.sidebar.slider(
    "Дни за прогноза",
    min_value=1,
    max_value=7,
    value=7
)

st.sidebar.caption("Данни от Open-Meteo")


# ==========================================
# CITY SEARCH
# ==========================================

st.subheader("🌍 Избери своя град")

with st.form("city_form"):

    city = st.text_input(
        "Въведи град:",
        value="Sofia",
        placeholder="Например: Plovdiv"
    )

    search = st.form_submit_button(
        "🔍 ПОТЪРСИ ПРОГНОЗА",
        use_container_width=True
    )

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

if "city_data" not in st.session_state:
    st.session_state.city_data = None


if search:

    if not city.strip():

        st.error("Моля, въведи име на град!")

    else:

        try:

            with st.spinner("🌍 Търся града..."):

                results = search_city(city.strip())

            if not results:

                st.error("Не открих такъв град. Опитай отново.")

            else:

                st.session_state.search_results = results

        except requests.RequestException as e:

            st.error(f"Проблем с връзката: {e}")


# ==========================================
# SELECT CITY
# ==========================================

if "search_results" in st.session_state:

    results = st.session_state.search_results

    options = []

    for item in results:

        label = (
            f"{item['name']}, "
            f"{item.get('admin1', '')}, "
            f"{item.get('country', '')}"
        )

        options.append(label)

    selected = st.selectbox(
        "Намерени градове:",
        range(len(results)),
        format_func=lambda i: options[i]
    )

    if st.button("🌤️ ПОКАЖИ ВРЕМЕТО", use_container_width=True):

        selected_city = results[selected]

        try:

            with st.spinner("☀️ Зареждам прогнозата..."):

                data = get_weather(
                    selected_city["latitude"],
                    selected_city["longitude"],
                    days,
                    unit
                )

            st.session_state.weather_data = data
            st.session_state.city_data = selected_city

            st.session_state.last_unit = unit
            st.session_state.last_days = days

            st.success("Прогнозата е заредена успешно!")

        except requests.RequestException as e:

            st.error(f"Не успях да заредя прогнозата: {e}")


# ==========================================
# DISPLAY WEATHER
# ==========================================

data = st.session_state.weather_data
location = st.session_state.city_data

if data and location:

    # Reload data if settings changed
    if (
        st.session_state.get("last_unit") != unit
        or st.session_state.get("last_days") != days
    ):

        try:

            data = get_weather(
                location["latitude"],
                location["longitude"],
                days,
                unit
            )

            st.session_state.weather_data = data
            st.session_state.last_unit = unit
            st.session_state.last_days = days

        except requests.RequestException as e:

            st.error(f"Грешка при обновяване: {e}")

    current = data["current"]
    daily = data["daily"]
    hourly = data["hourly"]

    temp = current["temperature_2m"]
    feels = current["apparent_temperature"]

    symbol, description = weather_info(
        current["weather_code"],
        current["is_day"]
    )

    temp_unit = "°C" if unit == "celsius" else "°F"

    # --------------------------------------
    # CURRENT WEATHER
    # --------------------------------------

    if page == "🏠 Начало":

        st.divider()

        st.subheader(
            f"📍 {location['name']}, "
            f"{location.get('country', '')}"
        )

        left, right = st.columns([1, 2])

        with left:

            st.markdown(
                f'<div class="weather-icon">{symbol}</div>',
                unsafe_allow_html=True
            )

        with right:

            st.markdown(
                f'<div class="big-temperature">{temp}{temp_unit}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"### {description}"
            )

            st.write(
                f"🌡️ Усеща се като: **{feels}{temp_unit}**"
            )

        st.divider()

        st.subheader("📊 Метеорологични показатели")

        a, b, c, d = st.columns(4)

        a.metric(
            "💧 Влажност",
            f"{current['relative_humidity_2m']}%"
        )

        b.metric(
            "💨 Вятър",
            f"{current['wind_speed_10m']} km/h"
        )

        c.metric(
            "☁️ Облачност",
            f"{current['cloud_cover']}%"
        )

        d.metric(
            "🌧️ Валежи",
            f"{current['precipitation']} mm"
        )

        a, b, c = st.columns(3)

        a.metric(
            "🌡️ Налягане",
            f"{current['pressure_msl']} hPa"
        )

        b.metric(
            "💨 Пориви",
            f"{current['wind_gusts_10m']} km/h"
        )

        c.metric(
            "🧭 Посока на вятъра",
            f"{current['wind_direction_10m']}°"
        )

        st.divider()

        st.subheader("🌅 Изгрев и залез")

        x, y = st.columns(2)

        x.info(f"🌅 Изгрев: {daily['sunrise'][0][-5:]}")
        y.info(f"🌇 Залез: {daily['sunset'][0][-5:]}")

        st.subheader("☀️ UV индекс")

        st.metric(
            "Максимален UV индекс днес",
            daily["uv_index_max"][0]
        )

        st.caption(
            "UV индексът е прогноза за максималната дневна стойност."
        )

        st.divider()

        st.subheader("👕 Съвет от Weather PRO")

        if temp < 0:
            st.warning(
                "🥶 Много студено! Облечи дебели дрехи."
            )

        elif temp < 10:
            st.info(
                "🧥 Студено е. Вземи топло яке."
            )

        elif temp < 20:
            st.info(
                "🌥️ Прохладно е. Подходящо е леко яке."
            )

        elif temp < 30:
            st.success(
                "☀️ Приятно време! Подходящо за разходка."
            )

        else:
            st.warning(
                "🔥 Горещо е! Пий вода и търси сянка."
            )

        if current["wind_speed_10m"] > 40:
            st.warning("💨 Има силен вятър!")

        if current["relative_humidity_2m"] > 80:
            st.info("💧 Влажността е много висока.")

    # --------------------------------------
    # 7 DAY FORECAST
    # --------------------------------------

    elif page == "📅 7-дневна прогноза":

        st.header("📅 Прогноза за следващите дни")

        for i in range(len(daily["time"])):

            icon, text = weather_info(
                daily["weather_code"][i]
            )

            with st.container():

                a, b, c, d = st.columns(4)

                a.write(f"**{daily['time'][i]}**")
                b.write(f"{icon} {text}")

                c.write(
                    f"🌡️ {daily['temperature_2m_min'][i]}"
                    f" / {daily['temperature_2m_max'][i]}"
                    f"{temp_unit}"
                )

                d.write(
                    f"🌧️ {daily['precipitation_probability_max'][i]}%"
                )

                st.divider()

        st.subheader("📈 Температури през седмицата")

        chart = pd.DataFrame({
            "Минимална": daily["temperature_2m_min"],
            "Максимална": daily["temperature_2m_max"]
        }, index=daily["time"])

        st.line_chart(chart)

        st.subheader("🌧️ Очаквани валежи")

        rain_chart = pd.DataFrame({
            "Валежи (mm)": daily["precipitation_sum"]
        }, index=daily["time"])

        st.bar_chart(rain_chart)

    # --------------------------------------
    # HOURLY FORECAST
    # --------------------------------------

    elif page == "⏰ Почасова прогноза":

        st.header("⏰ Прогноза по часове")

        now = datetime.fromisoformat(
            current["time"]
        )

        times = [
            datetime.fromisoformat(t)
            for t in hourly["time"]
        ]

        valid_indices = [
            i for i, t in enumerate(times)
            if t >= now
        ][:24]

        if valid_indices:

            hourly_df = pd.DataFrame({
                "Час": [
                    times[i].strftime("%d.%m %H:%M")
                    for i in valid_indices
                ],
                "Температура": [
                    hourly["temperature_2m"][i]
                    for i in valid_indices
                ],
                "Усеща се": [
                    hourly["apparent_temperature"][i]
                    for i in valid_indices
                ]
            })

            st.line_chart(
                hourly_df.set_index("Час")
            )

            st.subheader("🌤️ Детайли")

            for i in valid_indices[:12]:

                icon, desc = weather_info(
                    hourly["weather_code"][i]
                )

                st.write(
                    f"{times[i].strftime('%H:%M')} | "
                    f"{icon} {desc} | "
                    f"🌡️ {hourly['temperature_2m'][i]}"
                    f"{temp_unit} | "
                    f"💧 Валежи: "
                    f"{hourly['precipitation_probability'][i]}%"
                )

                st.divider()

        else:

            st.info("Няма налични почасови данни.")

    # --------------------------------------
    # ANALYTICS
    # --------------------------------------

    elif page == "📊 Анализи":

        st.header("📊 Метеорологичен анализ")

        df = pd.DataFrame({
            "Дата": daily["time"],
            "Минимум": daily["temperature_2m_min"],
            "Максимум": daily["temperature_2m_max"],
            "Валежи": daily["precipitation_sum"],
            "UV индекс": daily["uv_index_max"],
            "Вятър": daily["wind_speed_10m_max"]
        })

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🌡️ Средна прогнозна температура")

        avg = (
            sum(daily["temperature_2m_max"])
            + sum(daily["temperature_2m_min"])
        ) / (2 * len(daily["time"]))

        st.metric(
            "Средна стойност",
            f"{avg:.1f}{temp_unit}"
        )

        st.subheader("📈 Температурна графика")

        st.line_chart(
            df.set_index("Дата")[["Минимум", "Максимум"]]
        )

        st.subheader("🌧️ Валежи")

        st.bar_chart(
            df.set_index("Дата")[["Валежи"]]
        )

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "📥 Изтегли прогнозата като CSV",
            data=csv,
            file_name="weather_forecast.csv",
            mime="text/csv",
            use_container_width=True
        )

    # --------------------------------------
    # ABOUT
    # --------------------------------------

    elif page == "ℹ️ За проекта":

        st.header("ℹ️ За Weather PRO MAX")

        st.markdown("""
        ### 🌦️ Какво представлява?

        Weather PRO MAX е метеорологично приложение,
        създадено с Python и Streamlit.

        ### 🚀 Функции

        - Търсене на градове по света
        - Текущи метеорологични данни
        - Прогноза до 7 дни
        - Почасова прогноза
        - Температурни графики
        - UV индекс
        - Скорост на вятъра
        - Анализ на валежите
        - Изтегляне на данни

        ### 🛠️ Технологии

        - Python
        - Streamlit
        - Pandas
        - Open-Meteo API
        - CSS

        ### ❤️ Създадено с Python!
        """)

else:

    st.info(
        "🌍 Въведи град и натисни бутона за прогноза, "
        "за да заредиш метеорологичните данни."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px;">
    <h3>🌦️ WEATHER PRO MAX</h3>
    <p>Powered by Python & Open-Meteo</p>
    <p>Made with ❤️</p>
</div>
""", unsafe_allow_html=True)
