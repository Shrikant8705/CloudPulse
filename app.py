import streamlit as st
import requests

#Function to fetch data
def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.6&longitude=77.1333&current=precipitation,relative_humidity_2m"

    response = requests.get(url)
    return response.json()

#Title and some text for description
st.title("⛈️CloudPulse")
st.write("Real-time cloudburst prediction system.")
if st.button("Check Risk!"):
    data=fetch_weather()
    rain = data["current"]["precipitation"]
    humidity = data["current"]["relative_humidity_2m"]
    #Displaying in columns
    col1,col2=st.columns(2)
    col1.metric("Rainfall",f"{rain} mm")
    col2.metric("Humidity",f"{humidity}%")
    if rain > 30 and humidity > 65:
        st.error("🚨 HIGH RISK DETECTED")
    else:
        st.success("✅ Weather is stable")