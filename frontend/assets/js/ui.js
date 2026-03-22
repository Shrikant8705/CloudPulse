//UI Module,Manages UI state and common UI operations
import { Utils } from './utils.js';

export const UI = {
    //Show loading spinner
    showLoading(show = true) {
        Utils.toggleElement('loading', show);
    },

    //Show/hide results
    showResults(show = true) {
        Utils.toggleElement('results', !show);
    },

    //Show error message
    showError(message) {
        alert(`❌ Error: ${message}`);
        console.error(message);
    },

    //update city count
    updateCityCount(count) {
        const element = document.getElementById('cityCount');
        if (element) {
            element.textContent = count.toLocaleString();
        }
    },

    //enable disable predict button
    setPredictButtonState(enabled) {
        const button = document.getElementById('predictBtn');
        if (button) {
            button.disabled = !enabled;
        }
    }
};