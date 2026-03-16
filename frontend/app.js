const API_URL = 'http://localhost:8000/api';
let chart = null;

// Load cities on page load
async function loadCities() {
    const response = await fetch(`${API_URL}/cities`);
    const cities = await response.json();
    
    const select = document.getElementById('citySelect');
    select.innerHTML = '<option value="">Select a city...</option>';
    
    Object.keys(cities).forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        select.appendChild(option);
    });
}

// Check weather
async function checkWeather() {
    const city = document.getElementById('citySelect').value;
    
    if (!city) {
        alert('Please select a city');
        return;
    }
    
    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    
    try {
        const response = await fetch(`${API_URL}/weather/${city}`);
        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }
        
        displayResults(data);
    } catch (error) {
        alert('Error fetching weather data');
        console.error(error);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

// Display results
function displayResults(data) {
    // Update metrics
    document.getElementById('rainfall').textContent = `${data.rainfall} mm`;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('temperature').textContent = `${data.temperature}°C`;
    
    // Update risk alert
    const alertDiv = document.getElementById('riskAlert');
    const riskColors = {
        error: 'bg-red-100 border-red-500 text-red-700',
        warning: 'bg-yellow-100 border-yellow-500 text-yellow-700',
        success: 'bg-green-100 border-green-500 text-green-700',
        info: 'bg-blue-100 border-blue-500 text-blue-700'
    };
    
    alertDiv.className = `border-l-4 p-4 rounded ${riskColors[data.risk.type]}`;
    alertDiv.textContent = data.risk.message;
    
    // Update chart
    updateChart(data.hourly_rain);
    
    // Show results
    document.getElementById('results').classList.remove('hidden');
}

// Update chart
function updateChart(hourlyData) {
    const ctx = document.getElementById('chart').getContext('2d');
    
    if (chart) {
        chart.destroy();
    }
    
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 24}, (_, i) => `${i}:00`),
            datasets: [{
                label: 'Rainfall (mm)',
                data: hourlyData,
                borderColor: 'rgb(79, 70, 229)',
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Event listeners
document.getElementById('checkBtn').addEventListener('click', checkWeather);

// Load cities on page load
loadCities();