import pandas as pd
import json
import os

def load_indian_weather_data():

    # Load Indian weather data from CSV ,Returns dict of cities with weather and coordinates
    try:
        df = pd.read_csv('data/GlobalWeatherRepository.csv')
        
        #filter only for india
        if 'country' in df.columns:
            df= df[df['country']=='India']

        #remove duplicates
        df= df.drop_duplicates(subset=['location_name'], keep='first')

        cities_data={}
        
        for _, row in df.iterrows():
            city_name = row['location_name']

            cities_data[city_name] = {
                "region": row.get('region', 'Unknown'),
                "lat": float(row['latitude']),
                "lon": float(row['longitude']),
                "rainfall": float(row['precip_mm']),
                "humidity": int(row['humidity']),
                "pressure": float(row['pressure_mb']),
                "temperature": float(row['temperature_celsius']),
                "wind_speed": float(row['wind_kph']),
                "condition": row['condition_text'],
                "last_updated": row['last_updated'],
                "cloud_cover": int(row.get('cloud', 0)),
                "visibility": float(row.get('visibility_km', 10.0)),
                "uv_index": float(row.get('uv_index', 0.0))
            }
        print(f"✅ Filtered and loaded {len(cities_data)} Indian cities with weather data")
        return{}
    
    except Exception as e:
        print(f"❌ Error loading .csv file:{e}")

def save_to_json():
    #Save processed data to JSON for faster api loading
    os.makedirs('data', exist_ok=True)
    cities_data=load_indian_weather_data()

    if cities_data:
        with open('data/indian_cities_weather.json', 'w', encoding='utf-8') as f:
            json.dump(cities_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved to data/indian_cities_weather.json")

if __name__ == "__main__":
    save_to_json()