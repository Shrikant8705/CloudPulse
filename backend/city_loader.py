import pandas as pd
import json

def load_indian_weather_data():

    # Load Indian weather data from CSV ,Returns dict of cities with weather and coordinates
    try:
        df = pd.read_csv('data/IndianWeatherRepository.csv')
        
        # Remove duplicates (keep first occurrence of each city)
        df = df.drop_duplicates(subset=['location_name'], keep='first')
        
        cities_data = {}
        
        for _, row in df.iterrows():
            city_name = row['location_name']
            
            cities_data[city_name] = {
                # Location info
                "region": row['region'],
                "lat": float(row['latitude']),
                "lon": float(row['longitude']),
                
                # Weather data
                "rainfall": float(row['precip_mm']),
                "humidity": int(row['humidity']),
                "pressure": float(row['pressure_mb']),
                "temperature": float(row['temperature_celsius']),
                "wind_speed": float(row['wind_kph']),
                "condition": row['condition_text'],
                "last_updated": row['last_updated'],
                
                # Additional useful data
                "cloud_cover": int(row['cloud']),
                "visibility": float(row['visibility_km']),
                "uv_index": float(row['uv_index'])
            }
        
        print(f"✅ Loaded {len(cities_data)} Indian cities with weather data")
        
        # Show some examples
        print("\nSample cities loaded:")
        for i, city in enumerate(list(cities_data.keys())[:5]):
            print(f"  - {city} ({cities_data[city]['region']})")
        
        return cities_data
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return {}

def save_to_json():
    """Save processed data to JSON for faster loading"""
    cities_data = load_indian_weather_data()
    
    with open('data/indian_cities_weather.json', 'w', encoding='utf-8') as f:
        json.dump(cities_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to data/indian_cities_weather.json")
    print(f"   Total cities: {len(cities_data)}")
    
    return cities_data

if __name__ == "__main__":
    save_to_json()