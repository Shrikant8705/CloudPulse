//CloudPulse - Main Application ,Entry point and initialization

import { API } from './api.js';
import { UI } from './ui.js';
import { CitySelector } from './citySelector.js';
import { Predictions } from './predictions.js';

class CloudPulseApp {
    constructor() {
        this.citySelector = null;
        this.init();
    }

    async init() {
        console.log('🌩️ CloudPulse initializing...');
        
        // Initialize city selector
        this.citySelector = new CitySelector();
        
        // Setup predict button
        this.setupPredictButton();
        
        console.log('✅ CloudPulse ready!');
    }

    setupPredictButton() {
        const predictBtn = document.getElementById('predictBtn');
        
        predictBtn.addEventListener('click', async () => {
            await this.handlePrediction();
        });
    }

    async handlePrediction() {
        const city = this.citySelector.getSelectedCity();

        if (!city) {
            UI.showError('Please select a city first!');
            return;
        }

        console.log('🔮 Predicting for:', city);

        UI.showLoading(true);
        UI.showResults(false);

        try {
            const data = await API.getWeatherPrediction(city);
            
            UI.showLoading(false);
            Predictions.displayResults(data);
            
            console.log('✅ Prediction complete');
            
        } catch (error) {
            UI.showLoading(false);
            UI.showError(`Failed to fetch prediction: ${error.message}`);
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new CloudPulseApp();
});