import os
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("WEATHER_API_KEY")

url="http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={lat},{lon}&days=1&aqi=no"