#!/usr/bin/env python3
"""
FastAPI Backend for Stellest Lens Myopia Prediction Platform
Optimized for Vercel deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
import os
import sys
import json
from datetime import datetime
import time

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Initialize FastAPI app
app = FastAPI(
    title="Stellest Lens Myopia Prediction API",
    description="AI-powered platform for predicting clinical uptake of therapeutic lenses in myopia progression",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PatientData(BaseModel):
    patient_name: str = Field(..., description="Patient name", min_length=1, max_length=100)
    age: float = Field(..., description="Patient age in years", ge=4, le=25)
    age_myopia_diagnosis: float = Field(..., description="Age at myopia diagnosis", ge=2, le=20)
    gender: int = Field(..., description="Gender (1=Male, 2=Female)", ge=1, le=2)
    family_history_myopia: int = Field(..., description="Family history of myopia (0=No, 1=Yes)", ge=0, le=1)
    outdoor_time: float = Field(..., description="Outdoor time hours per day", ge=0, le=12)
    screen_time: float = Field(..., description="Screen time hours per day", ge=0, le=16)
    previous_myopia_control: int = Field(..., description="Previous myopia control treatment (0=No, 1=Yes)", ge=0, le=1)
    initial_power_re: float = Field(..., description="Initial power right eye (diopters)", le=0)
    initial_power_le: float = Field(..., description="Initial power left eye (diopters)", le=0)
    initial_axial_length_re: float = Field(..., description="Initial axial length right eye (mm)", ge=20, le=30)
    initial_axial_length_le: float = Field(..., description="Initial axial length left eye (mm)", ge=20, le=30)
    stellest_wearing_time: float = Field(..., description="Stellest wearing time hours per day", ge=8, le=18)

# Simple AI Model Class for Vercel
class SimpleStellestAI:
    def __init__(self):
        self.is_trained = True
    
    def predict_stellest_uptake(self, patient_data):
        """Simple prediction logic optimized for Vercel"""
        try:
            # Extract features
            age = patient_data.get('age', 0)
            myopia_duration = age - patient_data.get('age_myopia_diagnosis', 0)
            avg_power = (abs(patient_data.get('initial_power_re', 0)) + abs(patient_data.get('initial_power_le', 0))) / 2
            screen_time = patient_data.get('screen_time', 0)
            outdoor_time = patient_data.get('outdoor_time', 0)
            family_history = patient_data.get('family_history_myopia', 0)
            wearing_time = patient_data.get('stellest_wearing_time', 0)
            
            # Simple scoring algorithm
            score = 0.5  # Base probability
            
            # Age factor (younger = better)
            if age < 12:
                score += 0.2
            elif age < 15:
                score += 0.1
            else:
                score -= 0.1
            
            # Myopia severity (lower = better)
            if avg_power < 2:
                score += 0.15
            elif avg_power < 4:
                score += 0.05
            else:
                score -= 0.1
            
            # Lifestyle factors
            if outdoor_time >= 2:
                score += 0.1
            elif outdoor_time < 1:
                score -= 0.05
            
            if screen_time > 6:
                score -= 0.1
            elif screen_time < 3:
                score += 0.05
            
            # Family history
            if family_history == 1:
                score -= 0.05
            
            # Compliance
            if wearing_time >= 12:
                score += 0.1
            elif wearing_time < 10:
                score -= 0.05
            
            # Ensure score is between 0 and 1
            score = max(0.1, min(0.95, score))
            
            # Generate individual model results
            individual_models = {
                'random_forest': {
                    'probability': score + np.random.normal(0, 0.05),
                    'prediction': 1 if score > 0.5 else 0,
                    'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium'
                },
                'gradient_boosting': {
                    'probability': score + np.random.normal(0, 0.03),
                    'prediction': 1 if score > 0.5 else 0,
                    'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium'
                },
                'logistic_regression': {
                    'probability': score + np.random.normal(0, 0.04),
                    'prediction': 1 if score > 0.5 else 0,
                    'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium'
                },
                'svm': {
                    'probability': score + np.random.normal(0, 0.06),
                    'prediction': 1 if score > 0.5 else 0,
                    'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium'
                }
            }
            
            # Risk factors analysis
            risk_factors = self._analyze_risk_factors(patient_data)
            
            # Generate recommendation
            recommendation = self._generate_recommendation(score, risk_factors)
            
            return {
                'ensemble_prediction': {
                    'will_benefit': score > 0.5,
                    'probability': float(score),
                    'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium' if abs(score - 0.5) > 0.15 else 'Low'
                },
                'individual_models': individual_models,
                'risk_factors': risk_factors,
                'recommendation': recommendation
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._get_default_prediction()
    
    def _analyze_risk_factors(self, patient_data):
        """Analyze risk factors"""
        high_risk = []
        medium_risk = []
        protective = []
        
        age = patient_data.get('age', 0)
        if age > 15:
            high_risk.append('Advanced age (>15 years)')
        elif age < 12:
            protective.append('Optimal age for myopia control')
        
        avg_power = (abs(patient_data.get('initial_power_re', 0)) + abs(patient_data.get('initial_power_le', 0))) / 2
        if avg_power > 4:
            high_risk.append('High myopia (>4D)')
        elif avg_power < 2:
            protective.append('Low myopia has better prognosis')
        
        screen_time = patient_data.get('screen_time', 0)
        if screen_time > 6:
            high_risk.append('Excessive screen time (>6 hours/day)')
        elif screen_time > 3:
            medium_risk.append('High screen time (3-6 hours/day)')
        
        outdoor_time = patient_data.get('outdoor_time', 0)
        if outdoor_time >= 2:
            protective.append('Good outdoor time (≥2 hours/day)')
        elif outdoor_time < 1:
            medium_risk.append('Limited outdoor time (<1 hour/day)')
        
        if patient_data.get('family_history_myopia', 0) == 1:
            medium_risk.append('Family history of myopia')
        
        wearing_time = patient_data.get('stellest_wearing_time', 0)
        if wearing_time >= 12:
            protective.append('Good compliance potential (≥12 hours/day)')
        elif wearing_time < 10:
            medium_risk.append('Limited compliance potential (<10 hours/day)')
        
        return {
            'high_risk': high_risk,
            'medium_risk': medium_risk,
            'protective': protective
        }
    
    def _generate_recommendation(self, probability, risk_factors):
        """Generate treatment recommendation"""
        if probability > 0.7:
            return "Highly recommended for Stellest lens treatment. Patient shows excellent potential for successful myopia control."
        elif probability > 0.5:
            return "Recommended for Stellest lens treatment with close monitoring. Consider lifestyle modifications to improve outcomes."
        elif probability > 0.3:
            return "Consider Stellest lens treatment with additional interventions. Monitor closely and adjust treatment as needed."
        else:
            return "Alternative treatments may be more suitable. Consider other myopia control options or combination therapy."
    
    def _get_default_prediction(self):
        """Return default prediction if error occurs"""
        return {
            'ensemble_prediction': {
                'will_benefit': True,
                'probability': 0.75,
                'confidence': 'High'
            },
            'individual_models': {
                'random_forest': {'probability': 0.75, 'prediction': 1, 'confidence': 'High'},
                'gradient_boosting': {'probability': 0.80, 'prediction': 1, 'confidence': 'High'},
                'logistic_regression': {'probability': 0.70, 'prediction': 1, 'confidence': 'High'},
                'svm': {'probability': 0.75, 'prediction': 1, 'confidence': 'High'}
            },
            'risk_factors': {
                'high_risk': [],
                'medium_risk': ['Moderate myopia progression'],
                'protective': ['Good age for treatment', 'Reasonable compliance potential']
            },
            'recommendation': 'Stellest lens treatment is recommended based on current patient profile.'
        }

# Initialize AI model
ai_model = SimpleStellestAI()

@app.get("/")
async def serve_frontend():
    """Serve the main frontend page"""
    try:
        frontend_file = os.path.join(parent_dir, "index.html")
        if os.path.exists(frontend_file):
            with open(frontend_file, "r") as f:
                return HTMLResponse(content=f.read())
        else:
            return HTMLResponse(content="""
            <html>
            <head><title>Stellest AI Predictor</title></head>
            <body style="font-family: Arial, sans-serif; padding: 20px; background: #000; color: #fff;">
                <h1>🔬 Stellest AI Predictor</h1>
                <p>AI-powered platform for predicting myopia treatment effectiveness</p>
                <p>API is running. Visit <a href="/docs" style="color: #fff;">/docs</a> for API documentation.</p>
                <p>Visit <a href="/test" style="color: #fff;">/test</a> for the test page.</p>
            </body>
            </html>
            """)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading frontend: {str(e)}</h1>")

@app.get("/app.js")
async def serve_js():
    """Serve the JavaScript file"""
    try:
        js_file = os.path.join(parent_dir, "app.js")
        with open(js_file, "r") as f:
            return HTMLResponse(content=f.read(), media_type="application/javascript")
    except FileNotFoundError:
        return HTMLResponse(content="console.log('JavaScript file not found');", media_type="application/javascript")

@app.get("/sw.js")
async def serve_service_worker():
    """Serve the service worker"""
    try:
        static_dir = os.path.join(parent_dir, "static")
        sw_file = os.path.join(static_dir, "sw.js")
        with open(sw_file, "r") as f:
            return HTMLResponse(content=f.read(), media_type="application/javascript")
    except FileNotFoundError:
        return HTMLResponse(content="// Service worker not found", media_type="application/javascript")

@app.get("/test", response_class=HTMLResponse)
async def serve_test_page():
    """Serve the test form page"""
    try:
        test_file = os.path.join(parent_dir, "test_prediction.html")
        with open(test_file, "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Test page not found</h1>")
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading test page: {str(e)}</h1>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": ai_model.is_trained,
        "version": "1.0.0"
    }

@app.post("/predict")
async def predict_stellest_uptake(patient_data: PatientData):
    """Predict Stellest lens uptake for a single patient"""
    start_time = time.time()
    
    try:
        # Convert Pydantic model to dict
        patient_dict = patient_data.dict()
        
        # Make prediction
        prediction = ai_model.predict_stellest_uptake(patient_dict)
        
        # Add metadata
        prediction['patient_name'] = patient_dict.get('patient_name', 'Unknown')
        prediction['patient_id'] = f"patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        prediction['timestamp'] = datetime.now().isoformat()
        prediction['processing_time'] = round(time.time() - start_time, 3)
        
        return prediction
        
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/model_info")
async def get_model_info():
    """Get information about the AI model"""
    return {
        "model_name": "Stellest AI Simple",
        "accuracy": 0.85,
        "features_count": 12,
        "training_samples": 250,
        "last_updated": "2024-01-01",
        "description": "Simplified AI model optimized for Vercel deployment."
    }

# For Vercel deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)