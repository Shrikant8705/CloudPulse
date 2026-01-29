import streamlit as st
import requests

cities = {
    "Mumbai":{"lat":28.61 ,"lon":77.20},
    "Pune":{"lat":18.5196, "lon":73.8554},
    "Delhi":{"lat":28.6519, "lon":77.2315},
    "Bengaluru":{"lat":12.9719,"lon":77.5937},
    "Hyderabad":{"lat":17.384, "lon":78.4564},
    "London": {"lat": 51.50, "lon": -0.12},
    "Cherrapunji": {"lat": 25.27, "lon": 91.73}
    }
selected_city=st.sidebar.selectbox("Select a Location",list(cities.keys()))
lat = cities[selected_city]["lat"]
lon = cities[selected_city]["lon"]
#Function to fetch data
def fetch_weather(lat,lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation,relative_humidity_2m&hourly=precipitation"

    response = requests.get(url)
    return response.json()

#Title and some text for description
st.set_page_config(
    page_title="CloudPulse",
    page_icon="⛈️"
)
st.title("⛈️CloudPulse")
st.write("Real-time cloudburst prediction system.")
st.sidebar.title("Developer Tools")
test_mode=st.sidebar.title("Enable test mode")
if test_mode:
    rain_now=st.sidebar.slider("Simulate Rainfall (mm)", 0, 150, 0)
    humidity_now=st.sidebar.slider("Simulate Humidity (%)", 0, 100, 50)

if st.button("Check Risk!"):
    city_data=cities[selected_city]
    data=fetch_weather(city_data["lat"],city_data["lon"])
    data=fetch_weather(lat,lon)
    rain_now = data["current"]["precipitation"]
    humidity_now = data["current"]["relative_humidity_2m"]
    hourly_rain_list=data["hourly"]["precipitation"][:24] #:24 added For 24 hours
    #Hourly rain display
    hourly_rain= data["hourly"]["precipitation"]
    #Showing sub-heading
    st.write("### 24-Hour Rainfall Trend")
    st.line_chart(hourly_rain)
    #Displaying in columns
    col1,col2=st.columns(2)
    col1.metric("Rainfall",f"{rain_now} mm")
    col2.metric("Humidity",f"{humidity_now}%")
    st.line_chart(hourly_rain_list)
    if rain_now > 30 :
        st.error("🚨 CloudBurst Risk!")
    else:
        st.success("✅ Weather is stable")