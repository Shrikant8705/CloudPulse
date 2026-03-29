# ⛈️ CloudPulse: AI Cloudburst Prediction System

![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Backend-FastAPI-blue) ![Tailwind](https://img.shields.io/badge/Frontend-Tailwind_CSS-38B2AC) ![Machine Learning](https://img.shields.io/badge/AI-Random_Forest-orange)

CloudPulse is a real-time, end-to-end Machine Learning web application designed to predict the probability of localized cloudbursts across various Indian cities. By combining standard meteorological rule-based thresholds with a trained Random Forest AI, it provides a highly accurate, dynamic risk assessment dashboard.

## 🚀 Features

- **Live AI Predictions:** Utilizes a Random Forest classifier to detect hidden patterns in weather parameters.
- **Dual Risk Engine:** Calculates risk using both standard meteorological formulas and Machine Learning algorithms.
- **Dynamic AI Confidence:** The system mathematically scales risk and AI confidence based on live humidity, pressure, and temperature data.
- **Targeted High-Risk Zones:** Includes historical cloudburst hotspots like Kedarnath, Dharamshala, and Leh for specialized tracking.
- **Modern Glassmorphism UI:** A sleek, responsive frontend built with modern CSS, Tailwind, and ES6 JavaScript modules.

## 🛠️ Tech Stack

- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript (ES6 Modules)
- **Backend:** Python 3, FastAPI, Uvicorn
- **Machine Learning:** Scikit-Learn (Random Forest Classifier), Pandas, NumPy, Joblib

## 📊 Dataset Note

The Machine Learning model was trained on historical weather data to accurately recognize the extreme anomalies that lead to cloudbursts. 

🔗 **Dataset Source:** [Global Weather Repository on Kaggle](https://www.kaggle.com/) *(Add your specific Kaggle link here)*

> **Note:** Due to GitHub's file size limits, the massive 300MB+ CSV dataset used for training is omitted from this repository. The backend pulls from a lightweight JSON state file (`indian_cities_weather.json`) to serve live predictions to the dashboard.

## ⚙️ Local Setup & Installation

Follow these steps to run CloudPulse on your local machine:

### 1. Clone the repository
```bash
git clone https://github.com/Shrikant8705/CloudPulse.git
cd CloudPulse