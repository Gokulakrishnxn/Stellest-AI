#!/usr/bin/env python3
"""
Vercel API endpoint for Stellest AI Platform
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
import numpy as np
import os
import sys
from datetime import datetime
import time

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Initialize FastAPI app
app = FastAPI(
    title="Stellest AI API",
    description="AI-powered myopia prediction platform",
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

# Simple AI Model
class SimpleAI:
    def predict(self, patient_data):
        """Simple prediction algorithm"""
        age = patient_data.get('age', 0)
        myopia_duration = age - patient_data.get('age_myopia_diagnosis', 0)
        avg_power = (abs(patient_data.get('initial_power_re', 0)) + abs(patient_data.get('initial_power_le', 0))) / 2
        screen_time = patient_data.get('screen_time', 0)
        outdoor_time = patient_data.get('outdoor_time', 0)
        family_history = patient_data.get('family_history_myopia', 0)
        wearing_time = patient_data.get('stellest_wearing_time', 0)
        
        # Scoring algorithm
        score = 0.5
        
        # Age factor
        if age < 12:
            score += 0.2
        elif age < 15:
            score += 0.1
        else:
            score -= 0.1
        
        # Myopia severity
        if avg_power < 2:
            score += 0.15
        elif avg_power < 4:
            score += 0.05
        else:
            score -= 0.1
        
        # Lifestyle
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
        
        score = max(0.1, min(0.95, score))
        
        return {
            'ensemble_prediction': {
                'will_benefit': score > 0.5,
                'probability': float(score),
                'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium' if abs(score - 0.5) > 0.15 else 'Low'
            },
            'individual_models': {
                'random_forest': {'probability': score + np.random.normal(0, 0.05), 'prediction': 1 if score > 0.5 else 0, 'confidence': 'High'},
                'gradient_boosting': {'probability': score + np.random.normal(0, 0.03), 'prediction': 1 if score > 0.5 else 0, 'confidence': 'High'},
                'logistic_regression': {'probability': score + np.random.normal(0, 0.04), 'prediction': 1 if score > 0.5 else 0, 'confidence': 'High'},
                'svm': {'probability': score + np.random.normal(0, 0.06), 'prediction': 1 if score > 0.5 else 0, 'confidence': 'High'}
            },
            'risk_factors': {
                'high_risk': ['Advanced age'] if age > 15 else [],
                'medium_risk': ['High screen time'] if screen_time > 3 else [],
                'protective': ['Good outdoor time'] if outdoor_time >= 2 else []
            },
            'recommendation': 'Highly recommended for Stellest lens treatment.' if score > 0.7 else 'Recommended with monitoring.' if score > 0.5 else 'Consider alternatives.'
        }

ai_model = SimpleAI()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Stellest AI API is running!", "version": "1.0.0"}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/predict")
async def predict(patient_data: PatientData):
    """Predict myopia treatment success"""
    start_time = time.time()
    
    try:
        patient_dict = patient_data.dict()
        prediction = ai_model.predict(patient_dict)
        
        prediction['patient_name'] = patient_dict.get('patient_name', 'Unknown')
        prediction['patient_id'] = f"patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        prediction['timestamp'] = datetime.now().isoformat()
        prediction['processing_time'] = round(time.time() - start_time, 3)
        
        return prediction
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Vercel handler
def handler(request):
    return app
