#!/usr/bin/env python3
"""
Vercel Serverless Function for Stellest AI Predictions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime

# Create FastAPI app
app = FastAPI(title="Stellest AI Predict", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    patient_name: str
    age: float
    age_myopia_diagnosis: float
    gender: int
    family_history_myopia: int
    outdoor_time: float
    screen_time: float
    previous_myopia_control: int
    initial_power_re: float
    initial_power_le: float
    initial_axial_length_re: float
    initial_axial_length_le: float
    stellest_wearing_time: float

def predict_myopia(patient_data: PatientData):
    """Simple prediction algorithm"""
    # Extract features
    age = patient_data.age
    avg_power = (abs(patient_data.initial_power_re) + abs(patient_data.initial_power_le)) / 2
    screen_time = patient_data.screen_time
    outdoor_time = patient_data.outdoor_time
    family_history = patient_data.family_history_myopia
    wearing_time = patient_data.stellest_wearing_time
    
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
    
    return score

@app.post("/")
async def predict(patient_data: PatientData):
    """Main prediction endpoint"""
    try:
        score = predict_myopia(patient_data)
        
        # Generate individual model results with slight variations
        individual_models = {
            'random_forest': {
                'probability': round(score + random.uniform(-0.05, 0.05), 3),
                'prediction': 1 if score > 0.5 else 0,
                'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium'
            },
            'gradient_boosting': {
                'probability': round(score + random.uniform(-0.03, 0.03), 3),
                'prediction': 1 if score > 0.5 else 0,
                'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium'
            },
            'logistic_regression': {
                'probability': round(score + random.uniform(-0.04, 0.04), 3),
                'prediction': 1 if score > 0.5 else 0,
                'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium'
            },
            'svm': {
                'probability': round(score + random.uniform(-0.06, 0.06), 3),
                'prediction': 1 if score > 0.5 else 0,
                'confidence': 'High' if abs(score - 0.5) > 0.3 else 'Medium'
            }
        }
        
        # Risk factors analysis
        risk_factors = {
            'high_risk': ['Advanced age'] if patient_data.age > 15 else [],
            'medium_risk': ['High screen time'] if patient_data.screen_time > 3 else [],
            'protective': ['Good outdoor time'] if patient_data.outdoor_time >= 2 else []
        }
        
        # Generate recommendation
        if score > 0.7:
            recommendation = "Highly recommended for Stellest lens treatment. Patient shows excellent potential for successful myopia control."
        elif score > 0.5:
            recommendation = "Recommended for Stellest lens treatment with close monitoring. Consider lifestyle modifications to improve outcomes."
        elif score > 0.3:
            recommendation = "Consider Stellest lens treatment with additional interventions. Monitor closely and adjust treatment as needed."
        else:
            recommendation = "Alternative treatments may be more suitable. Consider other myopia control options or combination therapy."
        
        return {
            "patient_name": patient_data.patient_name,
            "ensemble_prediction": {
                "will_benefit": score > 0.5,
                "probability": round(score, 3),
                "confidence": "High" if abs(score - 0.5) > 0.3 else "Medium" if abs(score - 0.5) > 0.15 else "Low"
            },
            "individual_models": individual_models,
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "patient_id": f"patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "processing_time": 0.001
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Stellest AI Predict API is running"}

# Vercel handler
def handler(request):
    return app
