// Configuration
const API_URL = 'http://localhost:8000/api';
let rainfallChart = null;

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    loadCities();
    updateTime();
    setInterval(updateTime, 1000);
    
    // Event listeners
    document.getElementById('checkBtn').addEventListener('click', checkWeather);
    document.getElementById('testMode').addEventListener('change', handleTestMode);
});

// Update current time display
 
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    document.getElementById('currentTime').textContent = timeString;
}

// load cities from api
async function loadCities() {
    try {
        const response = await fetch(`${API_URL}/cities`);
        const cities = await response.json();
        
        const select = document.getElementById('citySelect');
        select.innerHTML = '<option value="">Select a city...</option>';
        
        Object.keys(cities).sort().forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            select.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading cities:', error);
        showError('Failed to load cities. Please refresh the page.');
    }
}

//handle test mode toggle

function handleTestMode(event) {
    const isTestMode = event.target.checked;
    const checkBtn = document.getElementById('checkBtn');
    
    if (isTestMode) {
        checkBtn.textContent = '🧪 Test with Simulated Data';
        checkBtn.classList.add('bg-gradient-to-r', 'from-yellow-500', 'to-orange-500');
        checkBtn.classList.remove('from-indigo-600', 'to-purple-600');
    } else {
        checkBtn.textContent = '🔍 Check Weather Risk';
        checkBtn.classList.remove('from-yellow-500', 'to-orange-500');
        checkBtn.classList.add('from-indigo-600', 'to-purple-600');
    }
}

//Check weather for selected city
 
async function checkWeather() {
    const city = document.getElementById('citySelect').value;
    const testMode = document.getElementById('testMode').checked;
    
    if (!city && !testMode) {
        showError('Please select a city');
        return;
    }
    
    // Show loading, hide results and errors
    showLoading(true);
    hideError();
    hideResults();
    
    try {
        let data;
        
        if (testMode) {
            // Use test endpoint with simulated data
            const rainfall = Math.floor(Math.random() * 100);
            const humidity = Math.floor(Math.random() * 100);
            const response = await fetch(`${API_URL}/test?rainfall=${rainfall}&humidity=${humidity}`);
            data = await response.json();
        } else {
            // Fetch real data
            const response = await fetch(`${API_URL}/weather/${city}`);
            
            if (!response.ok) {
                throw new Error(`Failed to fetch weather data: ${response.statusText}`);
            }
            
            data = await response.json();
        }
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error fetching weather:', error);
        showError('Failed to fetch weather data. Please try again.');
    } finally {
        showLoading(false);
    }
}

/**
 * Display weather results
 */
function displayResults(data) {
    const { city, weather, risk } = data;
    
    // Update city info
    document.getElementById('cityName').textContent = city || 'Test City';
    if (data.coordinates) {
        document.getElementById('coords').textContent = 
            `${data.coordinates.lat.toFixed(2)}°N, ${data.coordinates.lon.toFixed(2)}°E`;
    }
    
    // Update metrics
    document.getElementById('rainfall').textContent = `${weather.rainfall} mm`;
    document.getElementById('humidity').textContent = `${weather.humidity}%`;
    document.getElementById('temperature').textContent = `${weather.temperature}°C`;
    document.getElementById('pressure').textContent = `${weather.pressure} hPa`;
    
    // Update risk alert
    displayRiskAlert(risk);
    
    // Update risk score
    displayRiskScore(risk.score);
    
    // Update chart
    updateChart(weather.hourly_rain);
    
    // Update recommendations
    displayRecommendations(risk.actions || []);
    
    // Show results
    showResults();
}

/**
 * Display risk alert banner
 */
function displayRiskAlert(risk) {
    const alertDiv = document.getElementById('riskAlert');
    
    const colorMap = {
        error: 'bg-red-100 border-red-500 text-red-800',
        warning: 'bg-yellow-100 border-yellow-500 text-yellow-800',
        info: 'bg-blue-100 border-blue-500 text-blue-800',
        success: 'bg-green-100 border-green-500 text-green-800'
    };
    
    const iconMap = {
        error: '🚨',
        warning: '⚠️',
        info: '💧',
        success: '✅'
    };
    
    alertDiv.className = `border-l-4 p-6 ${colorMap[risk.type]}`;
    alertDiv.innerHTML = `
        <div class="flex items-center">
            <span class="text-4xl mr-4">${iconMap[risk.type]}</span>
            <div>
                <div class="text-2xl font-bold mb-1">${risk.message}</div>
                <div class="text-sm opacity-75">Risk Level: ${risk.level.toUpperCase()}</div>
            </div>
        </div>
    `;
}

/**
 * Display risk score
 */
function displayRiskScore(score) {
    document.getElementById('riskScore').textContent = score;
    
    const bar = document.getElementById('riskBar');
    bar.style.width = `${score}%`;
    
    // Color based on score
    if (score >= 80) {
        bar.className = 'h-4 rounded-full bg-gradient-to-r from-red-500 to-red-700 transition-all duration-500';
    } else if (score >= 60) {
        bar.className = 'h-4 rounded-full bg-gradient-to-r from-yellow-500 to-orange-500 transition-all duration-500';
    } else if (score >= 40) {
        bar.className = 'h-4 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all duration-500';
    } else {
        bar.className = 'h-4 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 transition-all duration-500';
    }
}

//Update rainfall chart

function updateChart(hourlyData) {
    const ctx = document.getElementById('rainfallChart').getContext('2d');
    
    // Destroy existing chart
    if (rainfallChart) {
        rainfallChart.destroy();
    }
    
    // Create new chart
    rainfallChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 24}, (_, i) => `${i}:00`),
            datasets: [{
                label: 'Rainfall (mm)',
                data: hourlyData,
                borderColor: 'rgb(79, 70, 229)',
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 3,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgb(79, 70, 229)',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

//Display recommendations

function displayRecommendations(actions) {
    const list = document.getElementById('actionsList');
    list.innerHTML = '';
    
    if (actions.length === 0) {
        list.innerHTML = '<li class="text-gray-600">No specific actions required</li>';
        return;
    }
    
    actions.forEach(action => {
        const li = document.createElement('li');
        li.className = 'flex items-start';
        li.innerHTML = `
            <span class="text-indigo-600 mr-2">▶</span>
            <span class="text-gray-700">${action}</span>
        `;
        list.appendChild(li);
    });
}

//UI Helper Functions

function showLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showResults() {
    document.getElementById('results').classList.remove('hidden');
}

function hideResults() {
    document.getElementById('results').classList.add('hidden');
}

function showError(message) {
    document.getElementById('errorText').textContent = message;
    document.getElementById('errorMessage').classList.remove('hidden');
}

function hideError() {
    document.getElementById('errorMessage').classList.add('hidden');
}