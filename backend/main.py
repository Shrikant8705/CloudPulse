from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

from backend.ml_model import predictor

app = FastAPI(title="CloudPulse API- Indian Weather")

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_cities():
    try:
        with open('data/indian_cities_weather.json','r',encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Run 'python backend/city_loader.py' to generate cities data")
        return {}
    
CITIES_DATA=load_cities()
    
@app.get("/")
def root():
    return {
        "message": "CloudPulse API - Indian Weather Edition",
        "version": "2.0",
        "ml_available": predictor.model is not None,
        "cities_loaded": len(CITIES_DATA),
        "data_source": "Indian Weather Repository CSV"
        }

@app.get("/api/cities")
def get_cities():
    #Get list of all indian cities
    cities_list=[
        {
        "name":city,
        "region":data["region"],
        "rainfall":data["rainfall"],
        "humidity":data["humidity"]
        }
        for city, data in CITIES_DATA.items()
    ]
    #sorting cities by name
    cities_list.sort(key=lambda x:x['name'])
    return {
        #returns first 100 with details
        "cities": [c["name"] for c in cities_list],
        "count": len(cities_list),
        "details": cities_list[:100]  
    }

@app.get("/api/search-cities/{query}")
def search_cities(query: str):
    #search cities by name
    query_lower = query.lower()
    
    matching = [
        city for city in CITIES_DATA.keys()
        if query_lower in city.lower()
    ]
    
    return {
        "query": query,
        "matches": matching[:50],  # Limit to 50 results
        "count": len(matching)
    }
@app.get("/api/weather/{city}")
def get_weather_for_city(city: str):
    """Get weather data and predictions for an Indian city"""
    
    # Check if city exists
    if city not in CITIES_DATA:
        raise HTTPException(404, f"City '{city}' not found. Try searching first.")
    
    city_data = CITIES_DATA[city]
    
    # Extract weather parameters
    rainfall = city_data["rainfall"]
    humidity = city_data["humidity"]
    pressure = city_data["pressure"]
    temperature = city_data["temperature"]
    
    # Rule-based risk assessment
    rule_based = assess_rule_based_risk(rainfall, humidity, pressure)
    
    # ML prediction
    ml_prediction = predictor.predict(
        rainfall,
        humidity,
        pressure,
        temperature
    )
    
    return {
        "city": city,
        "region": city_data["region"],
        "coordinates": {
            "lat": city_data["lat"],
            "lon": city_data["lon"]
        },
        "weather": {
            "rainfall": rainfall,
            "humidity": humidity,
            "pressure": pressure,
            "temperature": temperature,
            "wind_speed": city_data["wind_speed"],
            "condition": city_data["condition"],
            "cloud_cover": city_data["cloud_cover"],
            "visibility": city_data["visibility"],
            "uv_index": city_data["uv_index"],
            "last_updated": city_data["last_updated"]
        },
        "predictions": {
            "rule_based": rule_based,
            "ml_prediction": ml_prediction
        }
    }
@app.get("/api/high-risk-cities")
def get_high_risk_cities(min_rainfall: float = 30, min_humidity: int = 80):
    """Get cities currently at high risk"""
    
    high_risk = []
    
    for city, data in CITIES_DATA.items():
        if data["rainfall"] >= min_rainfall and data["humidity"] >= min_humidity:
            risk = assess_rule_based_risk(
                data["rainfall"],
                data["humidity"],
                data["pressure"]
            )
            
            high_risk.append({
                "city": city,
                "region": data["region"],
                "rainfall": data["rainfall"],
                "humidity": data["humidity"],
                "risk_level": risk["level"],
                "risk_score": risk["risk_score"]
            })
    
    # Sort by risk score (highest first)
    high_risk.sort(key=lambda x: x["risk_score"], reverse=True)
    
    return {
        "high_risk_cities": high_risk[:20],  # Top 20
        "total_count": len(high_risk),
        "criteria": {
            "min_rainfall": min_rainfall,
            "min_humidity": min_humidity
        }
    }

@app.get("/api/predict")
def predict_custom(
    rainfall: float,
    humidity: float,
    pressure: float = 1013,
    temperature: float = 25
):
    """Manual prediction endpoint (for testing)"""
    
    rule_based = assess_rule_based_risk(rainfall, humidity, pressure)
    ml_prediction = predictor.predict(rainfall, humidity, pressure, temperature)
    
    return {
        "input": {
            "rainfall": rainfall,
            "humidity": humidity,
            "pressure": pressure,
            "temperature": temperature
        },
        "predictions": {
            "rule_based": rule_based,
            "ml_prediction": ml_prediction
        }
    }
@app.get("/api/featured-cities")
def get_featured_cities():
    """Get cities currently showing cloudburst risk"""
    
    high_risk = []
    
    for city, data in CITIES_DATA.items():
        rainfall = data["rainfall"]
        humidity = data["humidity"]
        
        # Filter for actual risk conditions
        if rainfall > 20 or (rainfall > 10 and humidity > 80):
            risk = assess_rule_based_risk(rainfall, humidity, data["pressure"])
            
            high_risk.append({
                "city": city,
                "region": data["region"],
                "rainfall": rainfall,
                "humidity": humidity,
                "risk_score": risk["risk_score"],
                "risk_level": risk["level"]
            })
    
    # Sort by risk score (highest first)
    high_risk.sort(key=lambda x: x["risk_score"], reverse=True)
    
    # Get top 20 high risk
    top_high_risk = high_risk[:20]
    
    # Also add some major cities for demo
    major_cities = ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", 
                   "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
    
    featured = []
    for city in major_cities:
        if city in CITIES_DATA:
            data = CITIES_DATA[city]
            risk = assess_rule_based_risk(data["rainfall"], data["humidity"], data["pressure"])
            featured.append({
                "city": city,
                "region": data["region"],
                "rainfall": data["rainfall"],
                "humidity": data["humidity"],
                "risk_score": risk["risk_score"],
                "risk_level": risk["level"],
                "type": "major"
            })
    
    # Add high risk cities
    for item in top_high_risk:
        if item["city"] not in major_cities:
            item["type"] = "high_risk"
            featured.append(item)
    
    return {
        "featured": featured[:30],  # Top 30 total
        "count": len(featured)
    }