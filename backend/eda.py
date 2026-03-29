import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def perform_eda():
    print("🔍 Starting Exploratory Data Analysis...")
    
    # Setup directory to save the images
    os.makedirs('eda_plots', exist_ok=True)
    file_path = 'data/historical_weather.csv'
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # Map columns for the ML model
    column_mapping = {
        'precipitation_mm': 'rainfall',
        'relative_humidity_pct': 'humidity',
        'temperature_2m_c': 'temperature'
    }
    df.rename(columns=column_mapping, inplace=True)
    df = df.dropna(subset=['rainfall', 'humidity', 'temperature'])
    
    # Recreate the Cloudburst Labels
    df['cloudburst'] = np.where((df['rainfall'] > 40) & (df['humidity'] > 80), 1, 0)
    df['cloudburst'] = np.where(df['rainfall'] > 60, 1, df['cloudburst'])

    print("Generating Correlation Heatmap...")
    plt.figure(figsize=(8, 6))
    features = df[['rainfall', 'humidity', 'temperature', 'cloudburst']]
    # This heatmap shows how strongly features correlate with cloudbursts
    sns.heatmap(features.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f")
    plt.title('Feature Correlation with Cloudburst Risk')
    plt.tight_layout()
    plt.savefig('eda_plots/1_correlation_heatmap.png')
    plt.close()

    print("Generating Rainfall vs Humidity Scatter Plot...")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='humidity', y='rainfall', hue='cloudburst', 
                    palette={0: 'blue', 1: 'red'}, alpha=0.6)
    plt.title('Rainfall vs Humidity (Red = Cloudburst Event)')
    plt.xlabel('Humidity (%)')
    plt.ylabel('Rainfall (mm)')
    # Draw dashed lines to show the "Danger Zone"
    plt.axhline(y=40, color='r', linestyle='--', alpha=0.5) 
    plt.axvline(x=80, color='r', linestyle='--', alpha=0.5) 
    plt.tight_layout()
    plt.savefig('eda_plots/2_rainfall_vs_humidity.png')
    plt.close()

    print(" Generating Feature Distributions...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    sns.histplot(df['temperature'], bins=30, ax=axes[0], color='orange', kde=True)
    axes[0].set_title('Temperature Distribution')
    axes[0].set_xlabel('Temperature (°C)')
    
    sns.histplot(df['humidity'], bins=30, ax=axes[1], color='skyblue', kde=True)
    axes[1].set_title('Humidity Distribution')
    axes[1].set_xlabel('Humidity (%)')
    
    # Use log scale for rainfall as it's highly skewed
    sns.histplot(df[df['rainfall']>0]['rainfall'], bins=30, ax=axes[2], color='green', kde=True, log_scale=(False, True))
    axes[2].set_title('Rainfall Dist. (Log Scale)')
    axes[2].set_xlabel('Rainfall (mm)')
    
    plt.tight_layout()
    plt.savefig('eda_plots/3_feature_distributions.png')
    plt.close()

    print("✅ EDA Complete! Check the 'eda_plots' folder for your presentation charts.")

if __name__ == "__main__":
    perform_eda()