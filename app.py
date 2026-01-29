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
#Title and some text for description
st.set_page_config(
    page_title="CloudPulse",
    page_icon="⛈️"
)
st.title("⛈️CloudPulse")
st.write("Real-time cloudburst prediction system.")
#Siderbar & Sliderfor DevTools
st.sidebar.title("Developer Tools")
selected_city=st.sidebar.selectbox("Select a Location",list(cities.keys()))
test_mode=st.sidebar.checkbox("Enable Developer mode")

if test_mode:
    rain_now=st.sidebar.slider("Simulate Rainfall (mm)", 0, 150, 0)
    humidity_now=st.sidebar.slider("Simulate Humidity (%)", 0, 100, 50)

lat = cities[selected_city]["lat"]
lon = cities[selected_city]["lon"]
#Function to fetch data
def fetch_weather(lat,lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=precipitation,relative_humidity_2m&hourly=precipitation"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data {e}")
        return None
#Main logic
if st.button("Check Risk!"):
    if test_mode:
        hourly_rain=[rain_now] *24
    else:
        data=fetch_weather(lat,lon)
        
        if data is None:
            st.stop() #Stop if api fails

        rain_now = data["current"]["precipitation"]
        humidity_now=data["current"]["precipitation"]
        hourly_rain_list=data["hourly"]["precipitation"][:24] #:24 added For 24 hours    

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
    
    #Alert Logic
    if rain_now > 30 :
        st.error("🚨 CloudBurst Risk!")
    else:
        st.success("✅ Weather is stable")