import pandas as pd
import numpy as np

np.random.seed(42)

data = []
for _ in range(1000):
    rainfall = np.random.exponential(20)
    humidity = np.clip(np.random.normal(70, 15), 0, 100)
    pressure = np.clip(np.random.normal(1013, 10), 950, 1050)
    temperature = np.clip(np.random.normal(25, 5), 10, 45)
    
    # Simple rule: cloudburst if high rain + high humidity
    is_cloudburst = (rainfall > 50 and humidity > 85) or rainfall > 60
    
    data.append({
        'rainfall': rainfall,
        'humidity': humidity,
        'pressure': pressure,
        'temperature': temperature,
        'cloudburst': 1 if is_cloudburst else 0
    })

df = pd.DataFrame(data)
df.to_csv('data/training_data.csv', index=False)
print(f"✅ Generated {len(df)} samples, {df['cloudburst'].sum()} cloudburst cases")