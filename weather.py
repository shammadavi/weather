import requests
import matplotlib.pyplot as plt
import streamlit as st

# -----------------------------
# CONFIG
# -----------------------------
API_KEY = "b0dc4e85939232a6a588f29fc89f55df"   # 🔴 Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# -----------------------------
# FUNCTION TO FETCH DATA
# -----------------------------
def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        return response.json()
    except Exception as e:
        return {"cod": "error", "message": str(e)}

# -----------------------------
# STREAMLIT PAGE SETTINGS
# -----------------------------
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# -----------------------------
# UI
# -----------------------------
st.title("🌦 Weather Dashboard")
st.write("API Integration + Data Visualization Project")

city = st.text_input("Enter City Name", "Hyderabad")

# -----------------------------
# BUTTON ACTION
# -----------------------------
if st.button("Get Weather Data"):
    data = get_weather(city)

    # ERROR HANDLING
    if str(data.get("cod")) != "200":
        st.error(f"Error: {data.get('message', 'City not found!')}")
    else:
        temps = []
        humidity = []
        time_labels = []

        # Extract first 8 records (~24 hours)
        for item in data["list"][:8]:
            temps.append(item["main"]["temp"])
            humidity.append(item["main"]["humidity"])
            time_labels.append(item["dt_txt"])

        st.subheader(f"Weather Data for {city}")

        # -----------------------------
        # TEMPERATURE GRAPH
        # -----------------------------
        fig1, ax1 = plt.subplots()
        ax1.plot(time_labels, temps, marker='o')
        ax1.set_title("Temperature Trend")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Temperature (°C)")
        plt.xticks(rotation=45)

        st.pyplot(fig1)

        # -----------------------------
        # HUMIDITY GRAPH
        # -----------------------------
        fig2, ax2 = plt.subplots()
        ax2.plot(time_labels, humidity, marker='o')
        ax2.set_title("Humidity Trend")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Humidity (%)")
        plt.xticks(rotation=45)

        st.pyplot(fig2)

        # -----------------------------
        # RAW DATA
        # -----------------------------
        st.subheader("Raw Data")
        st.json(data)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.write("Run using: streamlit run weather_dashboard.py")