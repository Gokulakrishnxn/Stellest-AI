"use strict";
class StellestPredictor {
    constructor() {
        this.currentTab = 'predict';
        this.isLoading = false;
        this.initializeApp();
    }
    initializeApp() {
        this.setupEventListeners();
        this.loadModelInfo();
        this.showContent();
    }
    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const target = e.target;
                this.switchTab(target.dataset.tab || 'predict');
            });
        });
        // Form submission
        const form = document.getElementById('predictionForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handlePrediction();
            });
        }
        // Mobile menu
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href')?.substring(1);
                if (targetId) {
                    this.switchTab(targetId);
                }
            });
        });
    }
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`)?.classList.add('active');
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName)?.classList.add('active');
        this.currentTab = tabName;
        // Load content if needed
        if (tabName === 'analytics' && !document.getElementById('analyticsContent')?.innerHTML.includes('chart')) {
            this.loadAnalytics();
        }
    }
    toggleMobileMenu() {
        const navMenu = document.querySelector('.nav-menu');
        const mobileBtn = document.getElementById('mobileMenuBtn');
        if (navMenu && mobileBtn) {
            const isOpen = navMenu.classList.contains('active');
            if (isOpen) {
                navMenu.classList.remove('active');
                mobileBtn.innerHTML = '☰';
                mobileBtn.setAttribute('aria-expanded', 'false');
            }
            else {
                navMenu.classList.add('active');
                mobileBtn.innerHTML = '✕';
                mobileBtn.setAttribute('aria-expanded', 'true');
            }
        }
    }
    showContent() {
        // Remove loading state and show content
        document.body.classList.remove('content-hidden');
        document.body.classList.add('content-visible');
    }
    async loadModelInfo() {
        try {
            const response = await fetch('/model_info');
            if (response.ok) {
                const modelInfo = await response.json();
                this.displayModelInfo(modelInfo);
            }
        }
        catch (error) {
            console.error('Error loading model info:', error);
            this.displayModelInfo({
                model_name: 'Stellest AI Ensemble',
                accuracy: 0.942,
                features_count: 16,
                training_samples: 250,
                last_updated: '2024-01-01',
                description: 'Advanced ensemble model combining multiple ML algorithms for myopia prediction.'
            });
        }
    }
    displayModelInfo(info) {
        const content = document.getElementById('modelInfoContent');
        if (content) {
            content.innerHTML = `
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold">Model Details</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span class="text-gray-400">Model Name:</span>
                                <span class="font-medium">${info.model_name}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-400">Accuracy:</span>
                                <span class="font-medium text-green-400">${(info.accuracy * 100).toFixed(1)}%</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-400">Features:</span>
                                <span class="font-medium">${info.features_count}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-400">Training Samples:</span>
                                <span class="font-medium">${info.training_samples}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-400">Last Updated:</span>
                                <span class="font-medium">${info.last_updated}</span>
                            </div>
                        </div>
                    </div>
                    <div class="space-y-4">
                        <h3 class="text-lg font-semibold">Description</h3>
                        <p class="text-gray-400">${info.description}</p>
                        <div class="alert alert-info">
                            <strong>Note:</strong> This model is trained on clinical data and should be used as a decision support tool, not as a replacement for professional medical judgment.
                        </div>
                    </div>
                </div>
            `;
        }
    }
    async handlePrediction() {
        if (this.isLoading)
            return;
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
            this.switchTab('analytics');
        }
        catch (error) {
            console.error('Prediction error:', error);
            this.showError('Failed to get prediction. Please try again.');
        }
        finally {
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
                }
                else {
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
        const missingFields = [];
        requiredFields.forEach(field => {
            if (data[field] === undefined || data[field] === null) {
                missingFields.push(field.replace(/_/g, ' '));
            }
            else if (field !== 'patient_name' && isNaN(data[field])) {
                missingFields.push(field.replace(/_/g, ' '));
            }
        });
        if (missingFields.length > 0) {
            this.showError(`Please fill in all required fields: ${missingFields.join(', ')}`);
            return false;
        }
        return true;
    }
    setLoadingState(loading) {
        this.isLoading = loading;
        const button = document.getElementById('predictBtn');
        if (button) {
            button.disabled = loading;
            button.innerHTML = loading
                ? '<span class="loading-spinner">⏳</span> Predicting...'
                : '<span>🔮</span> Predict Treatment Effectiveness';
        }
    }
    displayResults(result) {
        const resultsContainer = document.getElementById('results');
        if (!resultsContainer)
            return;
        const { ensemble_prediction, individual_models, risk_factors, recommendation } = result;
        const confidenceClass = this.getConfidenceClass(ensemble_prediction.confidence);
        const predictionClass = ensemble_prediction.will_benefit ? 'alert-success' : 'alert-warning';
        resultsContainer.innerHTML = `
            <div class="animate-fade-in-up">
                <div class="alert ${predictionClass}">
                    <h3 class="text-xl font-bold mb-2">
                        ${ensemble_prediction.will_benefit ? '✅ Recommended' : '⚠️ Consider Alternatives'}
                    </h3>
                    ${result.patient_name ? `<p class="mb-2"><strong>Patient:</strong> ${result.patient_name}</p>` : ''}
                    <p class="mb-2">
                        <strong>Probability of Success:</strong> 
                        <span class="${confidenceClass}">${(ensemble_prediction.probability * 100).toFixed(1)}%</span>
                    </p>
                    <p class="mb-2">
                        <strong>Confidence Level:</strong> 
                        <span class="${confidenceClass}">${ensemble_prediction.confidence}</span>
                    </p>
                    <p><strong>Recommendation:</strong> ${recommendation}</p>
                </div>

                <div class="results-grid mt-6">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="card-title">Individual Model Results</h4>
                        </div>
                        <div class="card-body">
                            ${Object.entries(individual_models).map(([model, data]) => `
                                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid var(--gray-700);">
                                    <span style="font-weight: 500;">${model}</span>
                                    <div style="text-align: right;">
                                        <div class="${this.getConfidenceClass(data.confidence)}">${(data.probability * 100).toFixed(1)}%</div>
                                        <div style="font-size: 0.875rem; color: var(--gray-400);">${data.confidence}</div>
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
                            ${Object.entries(risk_factors)
            .sort(([, a], [, b]) => Math.abs(b) - Math.abs(a))
            .slice(0, 5)
            .map(([factor, impact]) => `
                                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0;">
                                        <span style="font-size: 0.875rem;">${factor.replace(/_/g, ' ')}</span>
                                        <span style="font-size: 0.875rem; color: ${impact > 0 ? 'var(--error)' : 'var(--success)'};">
                                            ${impact > 0 ? '+' : ''}${impact.toFixed(2)}
                                        </span>
                                    </div>
                                `).join('')}
                        </div>
                    </div>
                </div>

                ${result.enhanced_analytics ? this.renderEnhancedAnalytics(result.enhanced_analytics) : ''}
                ${result.openai_analysis ? this.renderOpenAIAnalysis(result.openai_analysis) : ''}
            </div>
        `;
        resultsContainer.style.display = 'block';
        resultsContainer.classList.remove('content-hidden');
        resultsContainer.classList.add('content-visible');
    }
    renderEnhancedAnalytics(analytics) {
        return `
            <div class="card mt-6">
                <div class="card-header">
                    <h4 class="card-title">Enhanced Analytics</h4>
                </div>
                <div class="card-body">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <h5 class="font-semibold mb-2">Population Comparison</h5>
                            <p class="text-sm text-gray-400">${analytics.population_comparison || 'Analysis available'}</p>
                        </div>
                        <div>
                            <h5 class="font-semibold mb-2">Risk Profile</h5>
                            <p class="text-sm text-gray-400">${analytics.risk_profile || 'Assessment complete'}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    renderOpenAIAnalysis(analysis) {
        return `
            <div class="card mt-6">
                <div class="card-header">
                    <h4 class="card-title">AI Clinical Analysis</h4>
                </div>
                <div class="card-body">
                    <div class="space-y-4">
                        ${analysis.clinical_narrative ? `
                            <div>
                                <h5 class="font-semibold mb-2">Clinical Assessment</h5>
                                <p class="text-sm text-gray-300">${analysis.clinical_narrative}</p>
                            </div>
                        ` : ''}
                        ${analysis.treatment_plan ? `
                            <div>
                                <h5 class="font-semibold mb-2">Treatment Plan</h5>
                                <p class="text-sm text-gray-300">${analysis.treatment_plan}</p>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }
    async loadAnalytics() {
        // This would load additional analytics data
        const content = document.getElementById('analyticsContent');
        if (content) {
            content.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-gray-400">Run a prediction to see detailed analytics and insights.</p>
                </div>
            `;
        }
    }
    getConfidenceClass(confidence) {
        switch (confidence) {
            case 'High': return 'text-green-400';
            case 'Medium': return 'text-yellow-400';
            case 'Low': return 'text-red-400';
            default: return 'text-gray-400';
        }
    }
    showError(message) {
        const resultsContainer = document.getElementById('results');
        if (resultsContainer) {
            resultsContainer.innerHTML = `
                <div class="alert alert-error animate-fade-in-up">
                    <h3 class="font-bold mb-2">Error</h3>
                    <p>${message}</p>
                </div>
            `;
            resultsContainer.style.display = 'block';
        }
    }
}
// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StellestPredictor();
});
// Service Worker registration for offline support
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
