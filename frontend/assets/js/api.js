//API Module Handles all backend communication
const API_BASE_URL = 'http://localhost:8000/api';

export const API = {
    //fetch all cities
    async getCities() {
        try {
            const response = await fetch(`${API_BASE_URL}/cities`);
            if (!response.ok) throw new Error('Failed to fetch cities');
            return await response.json();
        } catch (error) {
            console.error('Error fetching cities:', error);
            throw error;
        }
    },

    //search cities by query
    async searchCities(query) {
        try {
            const response = await fetch(`${API_BASE_URL}/search-cities/${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Search failed');
            return await response.json();
        } catch (error) {
            console.error('Error searching cities:', error);
            throw error;
        }
    },
    
    //get weather prediction for a city
    async getWeatherPrediction(cityName) {
        try {
            const response = await fetch(`${API_BASE_URL}/weather/${encodeURIComponent(cityName)}`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: Failed to fetch weather data`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching weather prediction:', error);
            throw error;
        }
    }
};