import json
import os
import requests
from datetime import datetime
import time

def fetch_live_weather_data():
    #Fetching real-time weather data for Indian cities using Open-Meteo API
    #targeted cities
    target_cities = {
        "Shimla": {"region": "Himachal Pradesh", "lat": 31.1048, "lon": 77.1734},
        "Dehradun": {"region": "Uttarakhand", "lat": 30.3165, "lon": 78.0322},
        "Srinagar": {"region": "Jammu & Kashmir", "lat": 34.0837, "lon": 74.7973},
        "Gangtok": {"region": "Sikkim", "lat": 27.3314, "lon": 88.6138},
        "Mumbai": {"region": "Maharashtra", "lat": 19.0760, "lon": 72.8777},
        "Delhi": {"region": "Delhi", "lat": 28.7041, "lon": 77.1025},
        "Bangalore": {"region": "Karnataka", "lat": 12.9716, "lon": 77.5946},
        "Kolkata": {"region": "West Bengal", "lat": 22.5726, "lon": 88.3639},
        "Chennai": {"region": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707},
        "Pune": {"region": "Maharashtra", "lat": 18.5204, "lon": 73.8567}
    }

    cities_data = {}
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    print("Fetching LIVE weather data from satellite API...")
    
    for city_name, info in target_cities.items():
        print(f"   Fetching {city_name}.")
        url = f"https://api.open-meteo.com/v1/forecast?latitude={info['lat']}&longitude={info['lon']}&current=temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,cloud_cover"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current", {})
                
                precip = current.get("precipitation", 0.0)
                cloud = current.get("cloud_cover", 0)
                
                condition = "Clear"
                if precip > 10: condition = "Heavy Rain"
                elif precip > 0: condition = "Rain"
                elif cloud > 60: condition = "Cloudy"
                
                cities_data[city_name] = {
                    "region": info["region"],
                    "lat": info["lat"],
                    "lon": info["lon"],
                    "rainfall": precip,
                    "humidity": current.get("relative_humidity_2m", 50),
                    "pressure": current.get("surface_pressure", 1013.0),
                    "temperature": current.get("temperature_2m", 25.0),
                    "wind_speed": current.get("wind_speed_10m", 0.0),
                    "condition": condition,
                    "last_updated": current_time,
                    "cloud_cover": cloud,
                    "visibility": 10.0,
                    "uv_index": 5.0
                }
        except Exception as e:
            print(f"   ❌ Error fetching {city_name}: {e}")
            
        time.sleep(0.2)

    return cities_data

def save_to_json():
    os.makedirs('data', exist_ok=True)
    cities_data = fetch_live_weather_data()
    
    if cities_data:
        with open('data/indian_cities_weather.json', 'w', encoding='utf-8') as f:
            json.dump(cities_data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ SUCCESS! Downloaded live data for {len(cities_data)} cities.")
        print(f"✅Saved to data/indian_cities_weather.json")

if __name__ == "__main__":
    save_to_json()