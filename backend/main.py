from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

from backend.ml_model import predictor
from backend.risk_engine import assess_rule_based_risk

app = FastAPI(title="CloudPulse API- Indian Weather")

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,allow_origins=["*"], allow_methods=["*"],allow_headers=["*"]
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
        "message": "CloudPulse API - Indian Weather Edition running",
        "cities_loaded": len(CITIES_DATA),
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
    #Get weather data and predictions for an Indian city
    #Check if city exists
    if city not in CITIES_DATA:
        raise HTTPException(404, f"City '{city}' not found. Try searching first.")
    
    city_data = CITIES_DATA[city]
    
    #Use imported risk engine
    rule_based= assess_rule_based_risk(city_data["rainfall"],city_data["humidity"],city_data["pressure"],city_data["region"])
    ml_prediction= predictor.predict(city_data["rainfall"],city_data("humidity"),city_data["pressure"],city_data["region"])
    
    return{
        "city":city,
        "region":city_data["region"],
        "weather":city_data,
        "predictions":{"rule_based": rule_based , "ml_prediction":ml_prediction}
    }

@app.get("/api/featured-cities")
def get_featured_cities():
    #Get cities currently showing cloudburst risk
    major_cities=[      
        "Shimla", "Dehradun", "Srinagar", "Gangtok", "Darjeeling", 
        "Mumbai", "Delhi", "Bangalore"
        ]
    featured=[]

    for city in major_cities:
        if city in CITIES_DATA:
            data = CITIES_DATA[city]
            risk = assess_rule_based_risk(data["rainfall"], data["humidity"], data["pressure"],data["region"])
            featured.append({
                "city": city,
                "region": data["region"],
                "risk_score": risk["risk_score"],
                "risk_level":risk["level"]
            })
    
    return {
        "featured": featured[:30],
    }