import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import os

print("Loading historical data...")

# Make sure this matches the exact CSV filename
csv_filename = 'data/historical_weather.csv'

if not os.path.exists(csv_filename):
    print(f"❌ ERROR: File not found at {csv_filename}")
    exit()

df = pd.read_csv(csv_filename)

print("Mapping columns based on your specific dataset...")

# Map your specific CSV columns to what the ML model needs
column_mapping = {
    'precipitation_mm': 'rainfall',
    'relative_humidity_pct': 'humidity',
    'temperature_2m_c': 'temperature'
}

df.rename(columns=column_mapping, inplace=True)

# 1. Handle Missing Pressure
# dataset doesn't have pressure, but the ML model needs it
# generate synthetic baseline pressure around 1013 hPa (standard sea level pressure)
print("❌'pressure' column missing. Generating realistic baseline pressure...")
df['pressure'] = np.random.normal(1013, 5, size=len(df))

# 2. Drop any rows where our core metrics are NaN
df = df.dropna(subset=['rainfall', 'humidity', 'temperature'])

# 3. Create the 'cloudburst' target label
print(" Generating Cloudburst target labels based on historical rainfall...")
#define a historical cloudburst event as:
# > 40mm of rain AND > 80% humidity OR just absolute extreme rain > 60mm
df['cloudburst'] = np.where((df['rainfall'] > 40) & (df['humidity'] > 80), 1, 0)
df['cloudburst'] = np.where(df['rainfall'] > 60, 1, df['cloudburst'])

cloudburst_count = df['cloudburst'].sum()
print(f" Dataset has {len(df)} total valid records.")
print(f"Found {cloudburst_count} historical cloudburst events to train on.")

if cloudburst_count == 0:
    print("❌ ERROR: No cloudburst events found in this dataset. The model cannot learn.")
    print("Lowering threshold for training purposes...")
    df['cloudburst'] = np.where(df['rainfall'] > 20, 1, 0)
    print(f"Re-adjusted: Found {df['cloudburst'].sum()} heavy rain events to train on.")

# Prepare Features (X) and Target (y)
X = df[['rainfall', 'humidity', 'pressure', 'temperature']]
y = df['cloudburst']

print("Splitting and Scaling data...")
# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale (Crucial for ML performance)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training Random Forest Machine Learning Model...")
# class_weight='balanced' tells the AI to pay extra attention to the rare cloudburst events
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
accuracy = model.score(X_test_scaled, y_test)
print(f"\n✅ Model trained successfully! AI Accuracy: {accuracy*100:.1f}%")

# Save the trained model and the scaler
print("Saving model to disk...")
Path("models").mkdir(exist_ok=True)
joblib.dump(model, 'models/cloudburst_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("✅ All done! You can now start your FastAPI server.")