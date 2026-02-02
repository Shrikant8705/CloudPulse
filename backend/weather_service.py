import requests
from app import lat , lon
def fetch_weather(city,API_KEY):
    url=f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={lat},{lon}&days=1&aqi=no"
    try:
        response=requests.get(url)
    
        if response.status_code==401:
            return None
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None
