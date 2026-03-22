//Predictions Module,Handles display of weather data and predictions

import { Utils } from './utils.js';

export const Predictions = {
    //Display complete prediction results
    displayResults(data) {
        this.displayCityInfo(data);
        this.displayWeatherCards(data.weather);
        this.displayRuleBasedPrediction(data.predictions.rule_based);
        this.displayMLPrediction(data.predictions.ml_prediction);
        
        document.getElementById('results').classList.remove('hidden');
        Utils.scrollToElement('results');
    },

    //Display city information
    displayCityInfo(data) {
        document.getElementById('cityName').textContent = data.city;
        document.getElementById('cityRegion').textContent = data.region || '';
        document.getElementById('lastUpdated').textContent = 
            Utils.formatDateTime(data.weather.last_updated);
    },

    //Display weather cards
    displayWeatherCards(weather) {
        const cards = [
            { icon: '🌧️', label: 'Rainfall', value: `${weather.rainfall} mm`, color: 'bg-blue-600' },
            { icon: '💧', label: 'Humidity', value: `${weather.humidity}%`, color: 'bg-cyan-600' },
            { icon: '🌡️', label: 'Temperature', value: `${weather.temperature}°C`, color: 'bg-orange-600' },
            { icon: '🔽', label: 'Pressure', value: `${weather.pressure} hPa`, color: 'bg-purple-600' }
        ];

        const container = document.getElementById('weatherCards');
        container.innerHTML = cards.map(card => `
            <div class="${card.color} text-white rounded-2xl p-5 text-center">
                <div class="text-4xl mb-2">${card.icon}</div>
                <div class="text-sm opacity-75">${card.label}</div>
                <div class="text-3xl font-bold">${card.value}</div>
            </div>
        `).join('');
    },

    //Display rule-based prediction
    displayRuleBasedPrediction(ruleBased) {
        const riskConfig = {
            'CRITICAL': { icon: '🚨', color: 'border-red-500', textColor: 'text-red-600' },
            'HIGH': { icon: '⚠️', color: 'border-orange-500', textColor: 'text-orange-600' },
            'MODERATE': { icon: '💧', color: 'border-yellow-500', textColor: 'text-yellow-600' },
            'LOW': { icon: '✅', color: 'border-green-500', textColor: 'text-green-600' }
        };

        const config = riskConfig[ruleBased.level] || riskConfig['LOW'];

        const html = `
            <div class="bg-gray-800/90 backdrop-blur rounded-3xl shadow-2xl p-8 border-4 ${config.color}">
                <div class="text-center">
                    <div class="text-sm font-semibold text-gray-400 mb-2">METEOROLOGICAL ANALYSIS</div>
                    <div class="text-6xl mb-4">${config.icon}</div>
                    <div class="text-4xl font-bold mb-3 ${config.textColor}">
                        ${ruleBased.level}
                    </div>
                    <p class="text-lg text-gray-300 mb-4">${ruleBased.message}</p>
                    <div class="text-sm text-gray-400">
                        Risk Score: <span class="font-bold text-white">${ruleBased.risk_score}/100</span>
                    </div>
                    ${this.renderRiskFactors(ruleBased.factors)}
                </div>
            </div>
        `;

        document.getElementById('ruleResult').innerHTML = html;
    },

    //Display ML prediction
    displayMLPrediction(mlPred) {
        if (!mlPred.available) {
            document.getElementById('mlResult').innerHTML = 
                '<p class="text-xl text-center text-white">⚠️ ML Model Unavailable</p>';
            return;
        }

        const prob = mlPred.probability;
        const isHighRisk = mlPred.prediction === 'HIGH RISK';

        const html = `
            <div class="bg-gradient-to-br from-purple-600 to-indigo-700 text-white rounded-3xl shadow-2xl p-8">
                <div class="text-center">
                    <div class="text-sm font-semibold text-white/70 mb-2">AI MACHINE LEARNING</div>
                    <div class="text-6xl mb-4">${isHighRisk ? '⚠️' : '🛡️'}</div>
                    <div class="text-4xl font-bold mb-3">${mlPred.prediction}</div>
                    <div class="text-2xl mb-4">Probability: ${prob.toFixed(1)}%</div>
                    <div class="w-full bg-white/30 rounded-full h-4 mb-4">
                        <div class="bg-white h-4 rounded-full transition-all duration-1000" 
                             style="width: ${prob}%"></div>
                    </div>
                    <div class="text-sm opacity-75">Confidence: ${mlPred.confidence.toFixed(1)}%</div>
                </div>
            </div>
        `;

        document.getElementById('mlResult').innerHTML = html;
        this.updateRiskBar(prob);
    },

    //Render risk factors
    renderRiskFactors(factors) {
        if (!factors || factors.length === 0) return '';

        return `
            <div class="mt-4 pt-4 border-t border-gray-700">
                <div class="text-xs text-gray-400 mb-2">Risk Factors:</div>
                <div class="text-sm text-gray-300 text-left">
                    ${factors.map(f => `• ${f}`).join('<br>')}
                </div>
            </div>
        `;
    },

    //Update overall risk bar
    updateRiskBar(probability) {
        document.getElementById('riskBar').style.width = `${probability}%`;
        document.getElementById('riskPercentage').textContent = `${probability.toFixed(1)}%`;
    }
};