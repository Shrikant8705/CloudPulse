import joblib
import numpy as np
from pathlib import Path

class MLPredictor:
    def __init__(self):
        try:
            self.model = joblib.load('models/cloudburst_model.pkl')
            self.scaler = joblib.load('models/scaler.pkl')
            print("✅ ML model loaded")
        except:
            self.model = None
            print("⚠️ ML model not found")
    
    def predict(self, rainfall, humidity, pressure, temperature):
        if not self.model:
            return {"available": False}
        
        features = np.array([[rainfall, humidity, pressure, temperature]])
        features_scaled = self.scaler.transform(features)
        
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        return {
            "available": True,
            "prediction": "HIGH RISK" if prediction == 1 else "LOW RISK",
            "probability": float(probability[1]) * 100,
            "confidence": float(max(probability)) * 100
        }

predictor = MLPredictor()