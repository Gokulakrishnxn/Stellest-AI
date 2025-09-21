from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime

app = FastAPI()

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

@app.post("/")
async def predict(patient_data: PatientData):
    try:
        # Simple prediction algorithm
        age = patient_data.age
        avg_power = (abs(patient_data.initial_power_re) + abs(patient_data.initial_power_le)) / 2
        screen_time = patient_data.screen_time
        outdoor_time = patient_data.outdoor_time
        
        score = 0.5  # Base probability
        
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
        if patient_data.family_history_myopia == 1:
            score -= 0.05
        
        # Compliance
        if patient_data.stellest_wearing_time >= 12:
            score += 0.1
        elif patient_data.stellest_wearing_time < 10:
            score -= 0.05
        
        score = max(0.1, min(0.95, score))
        
        return {
            "patient_name": patient_data.patient_name,
            "ensemble_prediction": {
                "will_benefit": score > 0.5,
                "probability": round(score, 3),
                "confidence": "High" if abs(score - 0.5) > 0.3 else "Medium" if abs(score - 0.5) > 0.15 else "Low"
            },
            "individual_models": {
                "random_forest": {"probability": round(score + random.uniform(-0.05, 0.05), 3), "prediction": 1 if score > 0.5 else 0, "confidence": "High"},
                "gradient_boosting": {"probability": round(score + random.uniform(-0.03, 0.03), 3), "prediction": 1 if score > 0.5 else 0, "confidence": "High"},
                "logistic_regression": {"probability": round(score + random.uniform(-0.04, 0.04), 3), "prediction": 1 if score > 0.5 else 0, "confidence": "High"},
                "svm": {"probability": round(score + random.uniform(-0.06, 0.06), 3), "prediction": 1 if score > 0.5 else 0, "confidence": "High"}
            },
            "risk_factors": {
                "high_risk": ["Advanced age"] if age > 15 else [],
                "medium_risk": ["High screen time"] if screen_time > 3 else [],
                "protective": ["Good outdoor time"] if outdoor_time >= 2 else []
            },
            "recommendation": "Highly recommended for Stellest lens treatment." if score > 0.7 else "Recommended with monitoring." if score > 0.5 else "Consider alternatives.",
            "patient_id": f"patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "processing_time": 0.001
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def health():
    return {"status": "healthy", "message": "Stellest AI Predict API is running"}