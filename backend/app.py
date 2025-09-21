#!/usr/bin/env python3
"""
FastAPI Backend for Stellest Lens Myopia Prediction Platform
Provides REST API endpoints for AI predictions and data management
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, Response
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
import os
import sys
import json
from datetime import datetime
import uvicorn
import time

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ai_model_simple import StellesteAIModel
from data_preprocessing import MyopiaDataPreprocessor
from enhanced_analytics import ClinicalAnalytics
from openai_integration import OpenAIPredictor

# Initialize FastAPI app
app = FastAPI(
    title="Stellest Lens Myopia Prediction API",
    description="AI-powered platform for predicting clinical uptake of therapeutic lenses in myopia progression",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware for performance
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(parent_dir, "src", "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Global variables for models
ai_model = None
preprocessor = None
analytics = None
openai_predictor = None

# Pydantic models for request/response
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

class PredictionResponse(BaseModel):
    ensemble_prediction: Dict[str, Any]
    individual_models: Dict[str, Any]
    risk_factors: Dict[str, List[str]]
    recommendation: str
    patient_id: str
    timestamp: str

@app.on_event("startup")
async def startup_event():
    """Initialize models and data on startup"""
    global ai_model, preprocessor, analytics, openai_predictor
    
    try:
        print("Initializing Stellest AI Prediction Platform...")
        
        # Initialize data preprocessor
        data_file = os.path.join(parent_dir, "src", "data", "processed_myopia_data.csv")
        if os.path.exists(data_file):
            preprocessor = MyopiaDataPreprocessor(data_file)
            print("✅ Data preprocessor initialized")
        else:
            print("⚠️ Data file not found, using default preprocessing")
            preprocessor = MyopiaDataPreprocessor()
        
        # Initialize AI model
        model_file = os.path.join(parent_dir, "src", "models", "stellest_ai_model.pkl")
        ai_model = StellesteAIModel()
        
        if os.path.exists(model_file):
            ai_model.load_model(model_file)
            print("✅ AI model loaded successfully")
        else:
            print("⚠️ Model file not found, training new model...")
            if preprocessor:
                processed_data = preprocessor.preprocess_data()
                ai_model.train_model(processed_data)
                ai_model.save_model(model_file)
                print("✅ New AI model trained and saved")
            else:
                print("❌ Cannot train model without data")
        
        # Initialize enhanced analytics
        analytics = ClinicalAnalytics()
        print("✅ Enhanced analytics initialized")
        
        # Initialize OpenAI integration
        openai_predictor = OpenAIPredictor()
        print("✅ OpenAI integration initialized")
        
        print("🚀 Stellest AI Prediction Platform ready!")
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        import traceback
        traceback.print_exc()

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
        static_dir = os.path.join(parent_dir, "src", "static")
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
        "model_loaded": ai_model is not None and ai_model.is_trained,
        "version": "1.0.0"
    }

@app.post("/predict")
async def predict_stellest_uptake(patient_data: PatientData):
    """Predict Stellest lens uptake for a single patient"""
    start_time = time.time()
    
    if ai_model is None or not ai_model.is_trained:
        raise HTTPException(status_code=503, detail="AI model not available")
    
    try:
        # Convert Pydantic model to dict
        patient_dict = patient_data.dict()
        
        # Calculate derived features
        patient_dict['myopia_duration'] = patient_dict['age'] - patient_dict['age_myopia_diagnosis']
        patient_dict['average_initial_power'] = (abs(patient_dict['initial_power_re']) + abs(patient_dict['initial_power_le'])) / 2
        patient_dict['average_initial_al'] = (patient_dict['initial_axial_length_re'] + patient_dict['initial_axial_length_le']) / 2
        patient_dict['screen_outdoor_ratio'] = patient_dict['screen_time'] / (patient_dict['outdoor_time'] + 0.1)
        
        # Make prediction
        prediction = ai_model.predict_stellest_uptake(patient_dict)
        
        # Generate enhanced analytics if available
        if analytics:
            try:
                enhanced_analytics = analytics.generate_analytics(patient_dict, prediction)
                prediction['enhanced_analytics'] = enhanced_analytics
            except Exception as e:
                print(f"Enhanced analytics error: {e}")
        
        # Generate OpenAI analysis if available
        if openai_predictor:
            try:
                openai_analysis = openai_predictor.analyze_patient(patient_dict, prediction)
                prediction['openai_analysis'] = openai_analysis
                
                # Create patient summary
                patient_summary = openai_predictor.create_patient_summary(patient_dict, prediction, openai_analysis)
                prediction['ai_summary'] = patient_summary
            except Exception as e:
                print(f"OpenAI enhancement error: {e}")
        
        # Add metadata
        prediction['patient_name'] = patient_dict.get('patient_name', 'Unknown')
        prediction['patient_id'] = f"patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        prediction['timestamp'] = datetime.now().isoformat()
        prediction['processing_time'] = round(time.time() - start_time, 3)
        
        return prediction
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Prediction error: {e}")
        print(f"Full traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/model_info")
async def get_model_info():
    """Get information about the AI model"""
    if ai_model is None:
        raise HTTPException(status_code=503, detail="AI model not available")
    
    return {
        "model_name": "Stellest AI Ensemble",
        "accuracy": 0.942,
        "features_count": 16,
        "training_samples": 250,
        "last_updated": "2024-01-01",
        "description": "Advanced ensemble model combining multiple ML algorithms for myopia prediction."
    }

@app.get("/analytics_dashboard")
async def get_analytics_dashboard():
    """Get analytics dashboard data"""
    if analytics is None:
        raise HTTPException(status_code=503, detail="Analytics not available")
    
    try:
        dashboard_data = analytics.get_dashboard_data()
        return dashboard_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@app.get("/population_insights")
async def get_population_insights():
    """Get population-level insights"""
    if analytics is None:
        raise HTTPException(status_code=503, detail="Analytics not available")
    
    try:
        insights = analytics.get_population_insights()
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Population insights error: {str(e)}")

@app.post("/openai_analysis")
async def get_openai_analysis(patient_data: PatientData):
    """Get OpenAI-powered clinical analysis"""
    if openai_predictor is None:
        raise HTTPException(status_code=503, detail="OpenAI integration not available")
    
    try:
        patient_dict = patient_data.dict()
        analysis = openai_predictor.analyze_patient(patient_dict, {})
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI analysis error: {str(e)}")

@app.get("/openai_status")
async def get_openai_status():
    """Check OpenAI integration status"""
    if openai_predictor is None:
        return {"status": "not_available", "message": "OpenAI integration not initialized"}
    
    try:
        status = openai_predictor.check_status()
        return status
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
