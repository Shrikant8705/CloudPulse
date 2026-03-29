# CloudPulse ⛈️

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AI-Powered Cloudburst Prediction System** combining meteorological analysis with machine learning to predict extreme rainfall events in Indian cities.

![CloudPulse Banner](docs/banner.png) <!-- Add your screenshot here -->

---

## 🌟 Features

- 🤖 **Dual Prediction System**: Rule-based meteorological analysis + Random Forest ML model
- 🌍 **9,840+ Indian Cities**: Comprehensive coverage with real weather data
- 📊 **Real-time Analysis**: Instant weather parameter evaluation
- 🎯 **95%+ Accuracy**: ML model trained on 1000+ weather patterns
- 🎨 **Modern UI**: Clean, responsive interface with dark mode
- ⚡ **Fast API**: RESTful backend with automatic documentation
- 📈 **Risk Visualization**: Interactive charts and risk meters
- 🔍 **Smart Search**: Filter cities with real-time search

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/Shrikant8705/CloudPulse.git
   cd CloudPulse
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Generate training data & train ML model**
```bash
   python data/synthetic_data.py
   python backend/train_model.py
```

4. **Process Indian cities data**
```bash
   python backend/city_loader.py
```

### Running the Application

**Terminal 1 - Start Backend:**
```bash
uvicorn backend.main:app --reload
```
Backend runs at: `http://localhost:8000`

**Terminal 2 - Start Frontend:**
```bash
cd frontend
python run_server.py
```
Frontend runs at: `http://localhost:8080`

**Open your browser:**
```
http://localhost:8080
```

---

## 🏗️ Project Structure
```
CloudPulse/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # API endpoints & application entry
│   ├── config.py              # Configuration settings
│   ├── weather_service.py     # Weather data processing
│   ├── risk_engine.py         # Rule-based risk assessment
│   ├── ml_model.py            # ML prediction engine
│   ├── train_model.py         # Model training script
│   ├── city_loader.py         # CSV to JSON converter
│   └── utils.py               # Helper functions
│
├── frontend/                   # Modular JavaScript frontend
│   ├── index.html             # Main HTML page
│   ├── run_server.py          # Custom HTTP server
│   └── assets/
│       ├── js/
│       │   ├── main.js        # Application entry point
│       │   ├── api.js         # API communication layer
│       │   ├── ui.js          # UI state management
│       │   ├── citySelector.js # City search & selection
│       │   ├── predictions.js  # Prediction display logic
│       │   └── utils.js       # Utility functions
│       └── css/
│           └── custom.css     # Custom styles
│
├── data/                       # Data files
│   ├── IndianWeatherRepository.csv  # Raw weather data (9,840 cities)
│   ├── indian_cities_weather.json   # Processed city data
│   ├── training_data.csv           # ML training dataset
│   └── synthetic_data.py           # Training data generator
│
├── models/                     # Trained ML models
│   ├── cloudburst_model.pkl   # Random Forest model
│   └── scaler.pkl             # Feature scaler
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **scikit-learn** - Machine learning (Random Forest)
- **pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Uvicorn** - ASGI server

### Frontend
- **Vanilla JavaScript** - ES6 modules
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Data visualization (optional)

### Machine Learning
- **Algorithm**: Random Forest Classifier
- **Features**: Rainfall, Humidity, Pressure, Temperature
- **Training Samples**: 1000+
- **Accuracy**: ~95%

---

## 📊 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. **Health Check**
```http
GET /
```

**Response:**
```json
{
  "message": "CloudPulse API - Indian Weather Edition",
  "version": "2.0",
  "ml_available": true,
  "cities_loaded": 9840
}
```

#### 2. **Get All Cities**
```http
GET /api/cities
```

**Response:**
```json
{
  "cities": ["Mumbai", "Delhi", "Bangalore", ...],
  "count": 9840
}
```

#### 3. **Search Cities**
```http
GET /api/search-cities/{query}
```

**Example:** `/api/search-cities/mum`

**Response:**
```json
{
  "query": "mum",
  "matches": ["Mumbai", "Mumfordganj", ...],
  "count": 15
}
```

#### 4. **Get Weather Prediction**
```http
GET /api/weather/{city}
```

**Example:** `/api/weather/Mumbai`

**Response:**
```json
{
  "city": "Mumbai",
  "region": "Maharashtra",
  "coordinates": {
    "lat": 19.07,
    "lon": 72.87
  },
  "weather": {
    "rainfall": 45.2,
    "humidity": 87,
    "pressure": 1010.5,
    "temperature": 28.5,
    "wind_speed": 15.3,
    "condition": "Heavy Rain",
    "last_updated": "2026-03-30 14:30:00"
  },
  "predictions": {
    "rule_based": {
      "level": "HIGH",
      "risk_score": 75,
      "message": "⚠️ HIGH RISK - Dangerous conditions",
      "factors": [
        "Heavy rainfall (45.2mm)",
        "Very high humidity (87%)",
        "Critical combination: High rain + humidity"
      ]
    },
    "ml_prediction": {
      "available": true,
      "prediction": "HIGH RISK",
      "probability": 89.5,
      "confidence": 92.3
    }
  }
}
```

#### 5. **Manual Prediction**
```http
GET /api/predict?rainfall={value}&humidity={value}&pressure={value}&temperature={value}
```

**Example:** `/api/predict?rainfall=60&humidity=90&pressure=1005&temperature=30`

### Interactive API Docs
Visit `http://localhost:8000/docs` for Swagger UI with interactive testing.

---

## 🎯 How It Works

### 1. **Data Collection**
- Uses real Indian weather data from 9,840 cities
- Parameters: rainfall, humidity, atmospheric pressure, temperature

### 2. **Rule-Based Analysis**
Meteorological rules for cloudburst risk:
- **Critical Risk (70+ points)**: Rainfall > 50mm + Humidity > 90%
- **High Risk (50-69 points)**: Rainfall > 30mm + Humidity > 85%
- **Moderate Risk (30-49 points)**: Elevated moisture or rainfall
- **Low Risk (< 30 points)**: Normal conditions

### 3. **Machine Learning Prediction**
- **Algorithm**: Random Forest with 100 decision trees
- **Training**: 1000 synthetic weather patterns
- **Features**: 4 (rainfall, humidity, pressure, temperature)
- **Output**: Binary classification (HIGH RISK / LOW RISK) + probability

### 4. **Combined Assessment**
- Both predictions shown side-by-side
- When both agree → High confidence
- Risk probability displayed as percentage
- Visual risk meter for quick assessment

---

## 📸 Screenshots

### Main Interface
![Main Interface](docs/screenshot-main.png)

### City Selection
![City Selection](docs/screenshot-city.png)

### Prediction Results
![Prediction Results](docs/screenshot-results.png)

### API Documentation
![API Docs](docs/screenshot-api.png)

---

## 🧪 Testing

### Test the API
```bash
# Health check
curl http://localhost:8000/

# Get cities
curl http://localhost:8000/api/cities

# Get prediction for Mumbai
curl http://localhost:8000/api/weather/Mumbai

# Manual prediction
curl "http://localhost:8000/api/predict?rainfall=60&humidity=90"
```

### Test the ML Model
```python
from backend.ml_model import predictor

# Test prediction
result = predictor.predict(
    rainfall=55,
    humidity=88,
    pressure=1008,
    temperature=29
)

print(result)
# Output: {'prediction': 'HIGH RISK', 'probability': 85.3, ...}
```

---

## 🔮 Future Enhancements

- [ ] **Historical Data Analysis**: Track weather patterns over time
- [ ] **Email/SMS Alerts**: Notify users of high-risk conditions
- [ ] **Mobile App**: React Native mobile application
- [ ] **Real-time Weather API**: Integrate live weather feeds
- [ ] **Deep Learning**: Upgrade to LSTM/GRU for time-series prediction
- [ ] **Multi-language Support**: Hindi, regional languages
- [ ] **Weather Maps**: Visual heatmaps of risk zones
- [ ] **User Accounts**: Save favorite cities, custom alerts
- [ ] **Advanced Metrics**: Wind patterns, cloud coverage analysis
- [ ] **Deployment**: Deploy to cloud (AWS/GCP/Azure)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Shrikant**
- GitHub: [@Shrikant8705](https://github.com/Shrikant8705)
- Project Link: [CloudPulse](https://github.com/Shrikant8705/CloudPulse)

---

## 🙏 Acknowledgments

- Indian Meteorological Department (IMD) for weather data insights
- OpenWeatherMap for API inspiration
- FastAPI community for excellent documentation
- scikit-learn team for ML tools

---

## 📚 References

- [Cloudburst Research Papers](https://scholar.google.com/scholar?q=cloudburst+prediction)
- [Indian Meteorological Department](https://mausam.imd.gov.in/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#forest)

---

## ⚠️ Disclaimer

This is a predictive system for educational and research purposes. For official weather warnings and advisories, please refer to your local meteorological department. This system should not be used as the sole basis for safety decisions.

---

<div align="center">

**Made with ❤️ for safer communities**

⭐ Star this repo if you found it helpful!

</div>