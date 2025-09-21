/**
 * Stellest AI - Myopia Prediction Platform
 * Frontend JavaScript for handling form submissions and displaying results
 */

class StellestAIApp {
    constructor() {
        this.currentTab = 'prediction';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupMobileMenu();
        this.loadExampleData();
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('predictionForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Tab switching
        const tabs = document.querySelectorAll('.tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Mobile menu
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => this.toggleMobileMenu());
        }
    }

    setupMobileMenu() {
        const navMenu = document.getElementById('navMenu');
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        
        if (navMenu && mobileMenuBtn) {
            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!navMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                    navMenu.classList.remove('active');
                }
            });
        }
    }

    toggleMobileMenu() {
        const navMenu = document.getElementById('navMenu');
        if (navMenu) {
            navMenu.classList.toggle('active');
        }
    }

    switchTab(tabName) {
        // Update tab buttons
        const tabs = document.querySelectorAll('.tab');
        tabs.forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.tab === tabName) {
                tab.classList.add('active');
            }
        });

        // Show/hide tab content
        const predictionTab = document.getElementById('predictionTab');
        const analyticsTab = document.getElementById('analyticsTab');

        if (tabName === 'prediction') {
            predictionTab.style.display = 'block';
            analyticsTab.style.display = 'none';
        } else if (tabName === 'analytics') {
            predictionTab.style.display = 'none';
            analyticsTab.style.display = 'block';
        }

        this.currentTab = tabName;
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = this.collectFormData();
        if (!this.validateFormData(formData)) {
            return;
        }

        this.setLoadingState(true);
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayResults(result);
            // Don't switch tabs automatically, keep user on prediction tab to see results
            
        } catch (error) {
            console.error('Error:', error);
            this.showError('Failed to get prediction. Please try again.');
        } finally {
            this.setLoadingState(false);
        }
    }

    collectFormData() {
        const form = document.getElementById('predictionForm');
        const formData = new FormData(form);
        const data = {};

        // Collect all form fields
        const fields = [
            'patient_name', 'age', 'age_myopia_diagnosis', 'gender', 'family_history_myopia',
            'outdoor_time', 'screen_time', 'previous_myopia_control',
            'initial_power_re', 'initial_power_le', 'initial_axial_length_re', 'initial_axial_length_le',
            'stellest_wearing_time'
        ];

        fields.forEach(field => {
            const value = formData.get(field);
            if (value !== null && value !== '') {
                if (field === 'patient_name') {
                    data[field] = value; // Keep as string
                } else {
                    data[field] = parseFloat(value);
                }
            }
        });

        return data;
    }

    validateFormData(data) {
        const requiredFields = [
            'patient_name', 'age', 'age_myopia_diagnosis', 'gender', 'family_history_myopia',
            'outdoor_time', 'screen_time', 'previous_myopia_control',
            'initial_power_re', 'initial_power_le', 'initial_axial_length_re', 'initial_axial_length_le',
            'stellest_wearing_time'
        ];

        for (const field of requiredFields) {
            if (!data[field] && data[field] !== 0) {
                this.showError(`Please fill in all required fields. Missing: ${field}`);
                return false;
            }
        }

        // Validate patient name
        if (typeof data.patient_name !== 'string' || data.patient_name.trim().length === 0) {
            this.showError('Please enter a valid patient name');
            return false;
        }

        // Validate numeric ranges
        if (data.age < 4 || data.age > 25) {
            this.showError('Age must be between 4 and 25 years');
            return false;
        }

        if (data.age_myopia_diagnosis < 2 || data.age_myopia_diagnosis > 20) {
            this.showError('Age at myopia diagnosis must be between 2 and 20 years');
            return false;
        }

        if (data.age_myopia_diagnosis >= data.age) {
            this.showError('Age at myopia diagnosis must be less than current age');
            return false;
        }

        return true;
    }

    setLoadingState(loading) {
        const btn = document.getElementById('predictBtn');
        if (btn) {
            btn.disabled = loading;
            btn.classList.toggle('loading', loading);
            btn.textContent = loading ? 'Processing...' : '🔮 Predict Treatment Effectiveness';
        }
    }

    displayResults(result) {
        console.log('Displaying results:', result); // Debug log
        const resultsContainer = document.getElementById('resultsContainer');
        const predictionResults = document.getElementById('predictionResults');
        const analyticsResults = document.getElementById('analyticsResults');

        if (!resultsContainer || !predictionResults) {
            console.error('Results container or prediction results element not found');
            return;
        }

        // Display prediction results
        const ensemble_prediction = result.ensemble_prediction;
        const individual_models = result.individual_models;
        const risk_factors = result.risk_factors;
        const recommendation = result.recommendation;
        const patient_name = result.patient_name || 'Patient';

        const confidenceClass = this.getConfidenceClass(ensemble_prediction.confidence);
        
        predictionResults.innerHTML = `
            <div class="prediction-result">
                <h3>🎯 Prediction for ${patient_name}</h3>
                <div class="probability ${confidenceClass}">
                    ${(ensemble_prediction.probability * 100).toFixed(1)}%
                </div>
                <p class="confidence ${confidenceClass}">
                    ${ensemble_prediction.confidence} Confidence
                </p>
                <p><strong>Recommendation:</strong> ${ensemble_prediction.will_benefit ? '✅ Recommended' : '⚠️ Consider Alternatives'}</p>
                <p><strong>Clinical Assessment:</strong> ${recommendation}</p>
                <p><strong>Processing Time:</strong> ${result.processing_time || 0} seconds</p>
            </div>

            <div class="results-grid">
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">Individual Model Results</h4>
                    </div>
                    <div class="card-body">
                        ${Object.entries(individual_models).map(([model, data]) => `
                            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                                <span style="font-weight: 500;">${this.formatModelName(model)}</span>
                                <div style="text-align: right;">
                                    <div class="${this.getConfidenceClass(data.confidence)}">${(data.probability * 100).toFixed(1)}%</div>
                                    <div style="font-size: 0.875rem; color: var(--text-muted);">${data.confidence}</div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">Risk Factors</h4>
                    </div>
                    <div class="card-body">
                        ${risk_factors.high_risk && risk_factors.high_risk.length > 0 ? `
                            <div style="margin-bottom: 1rem;">
                                <h5 style="color: var(--danger-color); margin-bottom: 0.5rem;">🔴 High Risk</h5>
                                <ul style="color: var(--danger-color);">
                                    ${risk_factors.high_risk.map(factor => `<li>${factor}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                        
                        ${risk_factors.medium_risk && risk_factors.medium_risk.length > 0 ? `
                            <div style="margin-bottom: 1rem;">
                                <h5 style="color: var(--warning-color); margin-bottom: 0.5rem;">🟡 Medium Risk</h5>
                                <ul style="color: var(--warning-color);">
                                    ${risk_factors.medium_risk.map(factor => `<li>${factor}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                        
                        ${risk_factors.protective && risk_factors.protective.length > 0 ? `
                            <div>
                                <h5 style="color: var(--success-color); margin-bottom: 0.5rem;">🟢 Protective Factors</h5>
                                <ul style="color: var(--success-color);">
                                    ${risk_factors.protective.map(factor => `<li>${factor}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;

        // Display enhanced analytics if available
        if (result.enhanced_analytics && analyticsResults) {
            this.displayEnhancedAnalytics(result.enhanced_analytics, analyticsResults);
        }

        // Show results container
        resultsContainer.style.display = 'block';
        console.log('Results container displayed'); // Debug log
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }

    displayEnhancedAnalytics(analytics, container) {
        if (!analytics || !container) return;

        let analyticsHTML = '<h3>📊 Enhanced Clinical Analytics</h3>';

        // Population comparison
        if (analytics.population_comparison) {
            analyticsHTML += `
                <div class="card" style="margin-bottom: 1rem;">
                    <div class="card-header">
                        <h4 class="card-title">Population Comparison</h4>
                    </div>
                    <div class="card-body">
                        ${Object.entries(analytics.population_comparison).map(([key, data]) => `
                            <div style="margin-bottom: 0.5rem;">
                                <strong>${this.formatFieldName(key)}:</strong> ${data.value} 
                                <span style="color: var(--text-muted);">(${data.interpretation})</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        // Risk profile
        if (analytics.risk_profile) {
            const risk = analytics.risk_profile;
            analyticsHTML += `
                <div class="card" style="margin-bottom: 1rem;">
                    <div class="card-header">
                        <h4 class="card-title">Risk Profile</h4>
                    </div>
                    <div class="card-body">
                        <div style="text-align: center; margin-bottom: 1rem;">
                            <div style="font-size: 2rem; font-weight: bold; color: ${risk.risk_color};">
                                ${risk.risk_category}
                            </div>
                            <div style="color: var(--text-muted);">Risk Score: ${risk.risk_score}</div>
                        </div>
                        ${risk.risk_factors.length > 0 ? `
                            <div style="margin-bottom: 1rem;">
                                <strong>Risk Factors:</strong>
                                <ul>
                                    ${risk.risk_factors.map(factor => `<li>${factor}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                        ${risk.protective_factors.length > 0 ? `
                            <div>
                                <strong>Protective Factors:</strong>
                                <ul>
                                    ${risk.protective_factors.map(factor => `<li>${factor}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        }

        // Clinical insights
        if (analytics.clinical_insights && analytics.clinical_insights.length > 0) {
            analyticsHTML += `
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">Clinical Insights</h4>
                    </div>
                    <div class="card-body">
                        <ul>
                            ${analytics.clinical_insights.map(insight => `<li>${insight}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;
        }

        container.innerHTML = analyticsHTML;
    }

    getConfidenceClass(confidence) {
        switch (confidence.toLowerCase()) {
            case 'high': return 'high';
            case 'medium': return 'medium';
            case 'low': return 'low';
            default: return 'medium';
        }
    }

    formatModelName(modelName) {
        return modelName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    formatFieldName(fieldName) {
        return fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--danger-color);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            z-index: 1000;
            max-width: 400px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    loadExampleData() {
        // Pre-fill form with example data for testing
        const exampleData = {
            patient_name: 'Emma Johnson',
            age: 10,
            age_myopia_diagnosis: 7,
            gender: '2',
            family_history_myopia: '0',
            outdoor_time: 3.5,
            screen_time: 2.0,
            previous_myopia_control: '0',
            initial_power_re: -1.5,
            initial_power_le: -1.25,
            initial_axial_length_re: 22.8,
            initial_axial_length_le: 22.7,
            stellest_wearing_time: 14.0
        };

        // Only pre-fill if form is empty
        const patientNameField = document.getElementById('patient_name');
        if (patientNameField && !patientNameField.value) {
            Object.entries(exampleData).forEach(([key, value]) => {
                const field = document.getElementById(key);
                if (field) {
                    field.value = value;
                }
            });
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StellestAIApp();
});

// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
