from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.weather_service import fetch_weather
from backend.risk_engine import assess_risk
from backend.utils import load_cities

app = FastAPI(title="CloudPulse API")

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "CloudPulse API is running"}

@app.get("/api/cities")
def get_cities():
    """Get all available cities"""
    return load_cities()

@app.get("/api/weather/{city}")
def get_weather(city: str):
    """Get weather data for a city"""
    cities = load_cities()
    
    if city not in cities:
        return {"error": "City not found"}
    
    coords = cities[city]
    weather_data = fetch_weather(coords["lat"], coords["lon"])
    
    if not weather_data:
        return {"error": "Failed to fetch weather"}
    
    # Add risk assessment
    risk = assess_risk(weather_data["rainfall"], weather_data["humidity"])
    
    return {
        **weather_data,
        "risk": risk,
        "city": city
    }