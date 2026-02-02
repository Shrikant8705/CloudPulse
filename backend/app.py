#Streamlit UI file
import streamlit as st
from weather_service import fetch_weather
from config import cities

st.set_page_config(
    page_title="CloudPulse",
    page_icon="⛈️"
)
st.title("⛈️CloudPulse")
st.write("Real-time cloudburst prediction system.")

#Sidebar and Slider-Simulate
st.sidebar.title("Developer Tools")
selected_city=st.sidebar.selectbox("Select a Location",list(cities.keys()))
test_mode=st.sidebar.checkbox("Enable Developer mode")
if test_mode:
    rain_now=st.sidebar.slider("Simulate Rainfall (mm)", 0, 150, 0)
    humidity_now=st.sidebar.slider("Simulate Humidity (%)", 0, 100, 50)

lat = cities[selected_city]["lat"]
lon = cities[selected_city]["lon"]

#Main Logic
if st.button("Check Risk!"):
    if test_mode:
        hourly_rain=[rain_now] *24
    else:
        data=fetch_weather(lat,lon)

        if data is None:
            st.stop() #Stop if api fails

        rain_now=data["current"]["precip_mm"]
        humidity_now=data["current"]["humidity"]
        hourly_rain=[hour["precip_mm"] for hour in data["forecast"]["forecastday"][0]["hour"]]

    #Displaying in columns
    col1,col2=st.columns(2)
    col1.metric("Rainfall",f"{rain_now} mm")
    col2.metric("Humidity",f"{humidity_now}%")

    #Showing sub-heading with error handling
    st.write("### 24-Hour Rainfall Trend")
    if hourly_rain and len(hourly_rain) > 0:
        st.line_chart(hourly_rain)
    else:
        st.warning("No hourly rainfall data available for this location")
    