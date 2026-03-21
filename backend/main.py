from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

try:
    from backend.ml_model import predictor
except:
    predictor = None

app = FastAPI(title="CloudPulse API")

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_cities():
    with open('data/cities.json') as f:
        return json.load(f)
    
@app.get("/")
def root():
    return {"message": "CloudPulse API","ml_avaliable": predictor.model is not None}

@app.get("/api/cities")
def get_cities():
    return load_cities()

@app.get("/api/predict")
def predict(rainfall: float, humidity: float, pressure: float = 1013, temperature: float = 25):
    #Testing prediction model and endpoint
    if predictor and predictor.model:
        ml_result=predictor.predict(rainfall,humidity,pressure,temperature)
    else:
        ml_result={"available":False}
 
# Simple rule-based
    rule_based = {
        "risk": "HIGH" if rainfall > 30 and humidity > 80 else "LOW",
        "message": "🚨 High Risk!" if rainfall > 30 and humidity > 80 else "✅ Safe"
    }
    
    return {
        "input": {"rainfall": rainfall, "humidity": humidity, "pressure": pressure, "temp": temperature},
        "rule_based": rule_based,
        "ml_prediction": ml_result
    }