import { UI } from './ui.js';

export const Predictions = {
    displayResults(data) {
        document.getElementById('results').classList.remove('hidden');

        document.getElementById('cityName').textContent = data.city;
        document.getElementById('cityRegion').textContent = data.region || 'India';
        document.getElementById('lastUpdated').textContent = data.weather.last_updated || new Date().toLocaleString();

        this.renderWeatherCards(data.weather);
        this.renderPredictionModels(data.predictions);
        this.animateRiskBar(data.predictions);
    },

    renderWeatherCards(weather) {
        const grid = document.getElementById('weatherCards');
        
        const cards = [
            { icon: '🌡️', title: 'Temperature', value: `${weather.temperature}°C` },
            { icon: '💧', title: 'Humidity', value: `${weather.humidity}%` },
            { icon: '🌧️', title: 'Rainfall', value: `${weather.rainfall} mm` },
            { icon: '💨', title: 'Wind Speed', value: `${weather.wind_speed} km/h` }
        ];

        grid.innerHTML = cards.map(card => `
            <div class="bg-gray-800/90 p-6 rounded-2xl border-2 border-gray-500 text-center transform hover:scale-105 transition-transform duration-300 shadow-[0_0_20px_rgba(0,0,0,0.5)]">
                <div class="text-5xl mb-4 drop-shadow-md">${card.icon}</div>
                <div class="text-gray-300 text-sm font-bold uppercase tracking-wider mb-2">${card.title}</div>
                <div class="text-white font-black text-3xl drop-shadow-lg">${card.value}</div>
            </div>
        `).join('');
    },

    renderPredictionModels(predictions) {
        const ruleDiv = document.getElementById('ruleResult');
        const rule = predictions.rule_based;
        
        let ruleBorder = rule.level === 'HIGH' ? 'border-red-500 shadow-[0_0_30px_rgba(239,68,68,0.4)]' : 'border-green-500 shadow-[0_0_30px_rgba(34,197,94,0.4)]';
        let ruleText = rule.level === 'HIGH' ? 'text-red-400' : 'text-green-400';

        ruleDiv.innerHTML = `
            <div class="bg-gray-800/90 p-8 rounded-2xl border-2 ${ruleBorder} h-full">
                <h4 class="text-gray-200 mb-4 font-bold flex items-center gap-2 uppercase tracking-wide text-sm">
                    <span class="text-xl">📡</span> Standard Meteorological Model
                </h4>
                <div class="text-5xl font-black ${ruleText} mb-3 tracking-tight drop-shadow-md">
                    ${rule.level} RISK
                </div>
                <p class="text-xl text-gray-300 font-semibold">Calculated Score: <span class="font-mono text-white bg-gray-900 px-3 py-1 rounded-lg border border-gray-600">${rule.risk_score.toFixed(1)}/100</span></p>
            </div>
        `;

        const mlDiv = document.getElementById('mlResult');
        const ml = predictions.ml_prediction;
        
        if (ml && ml.available) {
            let mlBorder = ml.prediction === 'HIGH RISK' ? 'border-red-500 shadow-[0_0_30px_rgba(239,68,68,0.4)]' : 'border-blue-500 shadow-[0_0_30px_rgba(59,130,246,0.4)]';
            let mlText = ml.prediction === 'HIGH RISK' ? 'text-red-400' : 'text-blue-400';

            mlDiv.innerHTML = `
                <div class="bg-gray-800/90 p-8 rounded-2xl border-2 ${mlBorder} h-full relative overflow-hidden">
                    <div class="absolute top-[-10px] right-[-10px] p-4 opacity-10 text-8xl">🧠</div>
                    <h4 class="text-gray-200 mb-4 font-bold flex items-center gap-2 uppercase tracking-wide text-sm relative z-10">
                        <span class="text-xl">🤖</span> AI Random Forest Model
                    </h4>
                    <div class="text-5xl font-black ${mlText} mb-3 tracking-tight drop-shadow-md relative z-10">
                        ${ml.prediction}
                    </div>
                    <p class="text-xl text-gray-300 font-semibold relative z-10">ML Confidence: <span class="font-mono text-white bg-gray-900 px-3 py-1 rounded-lg border border-gray-600">${ml.confidence.toFixed(1)}%</span></p>
                </div>
            `;
        }
    },

    animateRiskBar(predictions) {
        let finalRiskScore = predictions.rule_based.risk_score || 0;
        
        if (predictions.ml_prediction && predictions.ml_prediction.available) {
            finalRiskScore = Math.max(finalRiskScore, predictions.ml_prediction.probability);
        }

        finalRiskScore = Math.min(finalRiskScore, 100);

        const bar = document.getElementById('riskBar');
        const percentageText = document.getElementById('riskPercentage');

        // Minimum width of 3% so the bar is always slightly visible
        let barWidth = Math.max(finalRiskScore, 3);
        
        // Reset to 0 first
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = `${barWidth}%`;
            percentageText.textContent = `${finalRiskScore.toFixed(1)}%`;
            
            // Apply solid colors directly to the bar to fix the visibility issue
            if(finalRiskScore > 75) {
                bar.style.backgroundColor = '#ef4444'; // Red
                percentageText.className = "font-black text-5xl text-red-500 drop-shadow-[0_0_15px_rgba(239,68,68,0.8)]";
            } else if(finalRiskScore > 40) {
                bar.style.backgroundColor = '#eab308'; // Yellow
                percentageText.className = "font-black text-5xl text-yellow-400 drop-shadow-[0_0_15px_rgba(250,204,21,0.8)]";
            } else {
                bar.style.backgroundColor = '#22c55e'; // Green
                percentageText.className = "font-black text-5xl text-green-400 drop-shadow-[0_0_15px_rgba(74,222,128,0.8)]";
            }
        }, 100);
    }
};