import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

# Load data
df = pd.read_csv('data/training_data.csv')
X = df[['rainfall', 'humidity', 'pressure', 'temperature']]
y = df['cloudburst']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
accuracy = model.score(X_test_scaled, y_test)
print(f"✅ Model trained! Accuracy: {accuracy*100:.1f}%")

# Save
Path("models").mkdir(exist_ok=True)
joblib.dump(model, 'models/cloudburst_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("💾 Model saved!")