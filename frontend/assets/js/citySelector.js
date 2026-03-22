//City Selector Module,Handles city search and selection

import { API } from './api.js';
import { UI } from './ui.js';
import { Utils } from './utils.js';

export class CitySelector {
    constructor() {
        this.allCities = [];
        this.filteredCities = [];
        this.selectedCity = null;
        
        this.searchInput = document.getElementById('citySearch');
        this.citySelect = document.getElementById('citySelect');
        
        this.init();
    }

    async init() {
        await this.loadCities();
        this.setupEventListeners();
    }

    //Load all cities from API
    async loadCities() {
        try {
            const data = await API.getCities();
            this.allCities = data.cities || [];
            this.filteredCities = [...this.allCities];
            
            UI.updateCityCount(this.allCities.length);
            this.renderCityList(this.allCities);
            
            console.log(`✅ Loaded ${this.allCities.length} cities`);
        } catch (error) {
            UI.showError('Failed to load cities. Please refresh the page.');
        }
    }

    //Setup event listeners
    setupEventListeners() {
        // Search input with debounce
        this.searchInput.addEventListener('input', 
            Utils.debounce(() => this.handleSearch(), 300)
        );

        // City selection
        this.citySelect.addEventListener('change', (e) => {
            this.selectedCity = e.target.value;
            UI.setPredictButtonState(!!this.selectedCity);
        });

        // Double-click to select
        this.citySelect.addEventListener('dblclick', () => {
            if (this.selectedCity) {
                document.getElementById('predictBtn').click();
            }
        });
    }

    //Handle search input
    async handleSearch() {
        const query = this.searchInput.value.trim();

        // If empty, show all cities
        if (query.length === 0) {
            this.renderCityList(this.allCities);
            return;
        }

        // If very short, filter locally
        if (query.length < 3) {
            this.filteredCities = this.allCities.filter(city =>
                city.toLowerCase().includes(query.toLowerCase())
            );
            this.renderCityList(this.filteredCities);
            return;
        }

        // For longer queries, use API search
        try {
            const data = await API.searchCities(query);
            this.filteredCities = data.matches || [];
            this.renderCityList(this.filteredCities);
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    //Render city list in dropdown
    renderCityList(cities) {
        this.citySelect.innerHTML = '';

        if (cities.length === 0) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'No cities found';
            this.citySelect.appendChild(option);
            return;
        }

        //Show first 200 cities for performance
        const citiesToShow = cities.slice(0, 200);

        citiesToShow.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            this.citySelect.appendChild(option);
        });

        if (cities.length > 200) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = `--- ${cities.length - 200} more cities (refine search) ---`;
            option.disabled = true;
            this.citySelect.appendChild(option);
        }
    }

    //Get currently selected city
    getSelectedCity() {
        return this.selectedCity;
    }
}