const API_BASE_URL = 'http://localhost:8000/api';

// State Management
let allCities = [];
let selectedCity = null;


// INITIALIZATION


document.addEventListener('DOMContentLoaded', () => {
    console.log('CloudPulse initialized');
    loadCities();
    setupEventListeners();
});

function setupEventListeners() {
    // Search input
    document.getElementById('citySearch').addEventListener('input', handleSearch);
    
    // Predict button
    document.getElementById('predictBtn').addEventListener('click', handlePrediction);
    
    // City select
    document.getElementById('citySelect').addEventListener('change', (e) => {
        selectedCity = e.target.value;
    });
}

// CITY LOADING & SEARCH

async function loadCities() {
    try {
        showStatus('Loading cities...');
        
        const response = await fetch(`${API_BASE_URL}/cities`);
        if (!response.ok) throw new Error('Failed to load cities');
        
        const data = await response.json();
        allCities = data.cities;
        
        populateCityDropdown(allCities.slice(0, 100)); // Show first 100
        
        document.getElementById('cityCount').textContent = `${data.count}`;
        console.log(`✅ Loaded ${data.count} cities`);
        
    } catch (error) {
        console.error('Error loading cities:', error);
        showError('Failed to load cities. Check if backend is running.');
    }
}

function populateCityDropdown(cities) {
    const select = document.getElementById('citySelect');
    select.innerHTML = '<option value="">-- Select a city --</option>';
    
    cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        select.appendChild(option);
    });
}

async function handleSearch() {
    const query = document.getElementById('citySearch').value.trim();
    
    if (query.length < 2) {
        populateCityDropdown(allCities.slice(0, 100));
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/search-cities/${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.matches.length === 0) {
            document.getElementById('citySelect').innerHTML = '<option value="">No cities found</option>';
            return;
        }
        
        populateCityDropdown(data.matches);
        
    } catch (error) {
        console.error('Search error:', error);
    }
}

// PREDICTION

async function handlePrediction() {
    const city = document.getElementById('citySelect').value;
    
    if (!city) {
        alert('⚠️ Please select a city first!');
        return;
    }
    
    console.log('Predicting for city:', city);
    
    showLoading(true);
    hideResults();
    
    try {
        const response = await fetch(`${API_BASE_URL}/weather/${encodeURIComponent(city)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Received data:', data);
        
        showLoading(false);
        displayResults(data);
        
    } catch (error) {
        showLoading(false);
        console.error('Prediction error:', error);
        alert(`❌ Error: ${error.message}\n\nMake sure the backend is running!`);
    }
}

// DISPLAY RESULTS

function displayResults(data) {
    // Show results container
    document.getElementById('results').classList.remove('hidden');
    
    // City Info
    document.getElementById('cityName').textContent = data.city;
    document.getElementById('cityRegion').textContent = data.region || '';
    document.getElementById('lastUpdated').textContent = formatDateTime(data.weather.last_updated);
    
    // Weather Cards
    document.getElementById('displayRainfall').textContent = `${data.weather.rainfall} mm`;
    document.getElementById('displayHumidity').textContent = `${data.weather.humidity}%`;
    document.getElementById('displayTemp').textContent = `${data.weather.temperature}°C`;
    document.getElementById('displayPressure').textContent = `${data.weather.pressure} hPa`;
    
    // Predictions
    displayRuleBasedResult(data.predictions.rule_based);
    displayMLResult(data.predictions.ml_prediction);
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function displayRuleBasedResult(ruleBased) {
    const ruleDiv = document.getElementById('ruleResult');
    
    const riskLevels = {
        'CRITICAL': { icon: '🚨', color: 'border-red-500', textColor: 'text-red-600' },
        'HIGH': { icon: '⚠️', color: 'border-orange-500', textColor: 'text-orange-600' },
        'MODERATE': { icon: '💧', color: 'border-yellow-500', textColor: 'text-yellow-600' },
        'LOW': { icon: '✅', color: 'border-green-500', textColor: 'text-green-600' }
    };
    
    const level = riskLevels[ruleBased.level] || riskLevels['LOW'];
    
    ruleDiv.className = `bg-gray-800/90 backdrop-blur rounded-3xl shadow-2xl p-8 border-4 ${level.color}`;
    ruleDiv.innerHTML = `
        <div class="text-center">
            <div class="text-sm font-semibold text-gray-400 mb-2">METEOROLOGICAL ANALYSIS</div>
            <div class="text-6xl mb-4">${level.icon}</div>
            <div class="text-4xl font-bold mb-3 ${level.textColor}">
                ${ruleBased.level}
            </div>
            <p class="text-lg text-gray-300 mb-4">${ruleBased.message}</p>
            <div class="text-sm text-gray-400">
                Risk Score: <span class="font-bold text-white">${ruleBased.risk_score}/100</span>
            </div>
            ${renderRiskFactors(ruleBased.factors)}
        </div>
    `;
}

function displayMLResult(mlPred) {
    const mlDiv = document.getElementById('mlResult');
    
    if (!mlPred.available) {
        mlDiv.innerHTML = '<p class="text-xl text-center">⚠️ ML Model Unavailable</p>';
        return;
    }
    
    const prob = mlPred.probability;
    const isHighRisk = mlPred.prediction === 'HIGH RISK';
    
    mlDiv.innerHTML = `
        <div class="text-center">
            <div class="text-sm font-semibold text-white/70 mb-2">AI MACHINE LEARNING</div>
            <div class="text-6xl mb-4">${isHighRisk ? '⚠️' : '🛡️'}</div>
            <div class="text-4xl font-bold mb-3">${mlPred.prediction}</div>
            <div class="text-2xl mb-4">Cloudburst Probability: ${prob.toFixed(1)}%</div>
            <div class="w-full bg-white/30 rounded-full h-4 mb-4">
                <div class="bg-white h-4 rounded-full transition-all duration-1000" 
                     style="width: ${prob}%"></div>
            </div>
            <div class="text-sm opacity-75">Model Confidence: ${mlPred.confidence.toFixed(1)}%</div>
        </div>
    `;
    
    // Update overall risk bar
    updateRiskBar(prob);
}

function renderRiskFactors(factors) {
    if (!factors || factors.length === 0) return '';
    
    return `
        <div class="mt-4 pt-4 border-t border-gray-700">
            <div class="text-xs text-gray-400 mb-2">Risk Factors:</div>
            <div class="text-sm text-gray-300 text-left">
                ${factors.map(f => `• ${f}`).join('<br>')}
            </div>
        </div>
    `;
}

function updateRiskBar(probability) {
    const bar = document.getElementById('riskBar');
    const percentage = document.getElementById('riskPercentage');
    
    bar.style.width = `${probability}%`;
    percentage.textContent = `${probability.toFixed(1)}%`;
}


// UI HELPERS
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

function hideResults() {
    document.getElementById('results').classList.add('hidden');
}

function showStatus(message) {
    console.log('Status:', message);
}

function showError(message) {
    console.error('Error:', message);
    alert('❌ ' + message);
}

function formatDateTime(dateStr) {
    if (!dateStr) return '--';
    
    const date = new Date(dateStr);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// CONSOLE INFO
console.log(`
╔═══════════════════════════════════════╗
║      CloudPulse Frontend v2.0        ║
║   A Cloudburst Prediction System    ║
╚═══════════════════════════════════════╝

API: ${API_BASE_URL}
Status: Ready
`);