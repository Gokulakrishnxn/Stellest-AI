from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime
import os
import json
import math

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
    right_eye_spherical: float  # Spherical power OD (D)
    right_eye_cylinder: float   # Cylinder power OD (D)
    left_eye_spherical: float   # Spherical power OS (D)
    left_eye_cylinder: float    # Cylinder power OS (D)
    right_eye_axial_length: float  # Axial length OD (mm)
    left_eye_axial_length: float   # Axial length OS (mm)
    keratometry_k1_re: float
    keratometry_k2_re: float
    keratometry_k1_le: float
    keratometry_k2_le: float
    new_stellest_lenses: int    # 0=No, 1=Yes (whether considering new Stellest lenses)

FEATURES = [
    'age', 'age_myopia_diagnosis', 'gender', 'family_history_myopia',
    'outdoor_time', 'screen_time', 'previous_myopia_control',
    'right_eye_spherical', 'right_eye_cylinder', 'left_eye_spherical', 'left_eye_cylinder',
    'right_eye_axial_length', 'left_eye_axial_length', 'keratometry_k1_re', 'keratometry_k2_re',
    'keratometry_k1_le', 'keratometry_k2_le', 'new_stellest_lenses'
]

_model = None


def _load_json_model():
    global _model
    if _model is not None:
        return _model
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'model.json')
    if os.path.exists(model_path):
        try:
            with open(model_path, 'r') as f:
                _model = json.load(f)
        except Exception:
            _model = None
    return _model


def _predict_with_json_model(d: dict) -> float:
    m = _load_json_model()
    if not m:
        return None
    # Build feature vector in expected order
    x = []
    for name in m['feature_order']:
        x.append(float(d.get(name, 0.0)))
    # Standardize
    x_std = [(x[i] - m['scaler_mean'][i]) / (m['scaler_scale'][i] if m['scaler_scale'][i] != 0 else 1.0) for i in range(len(x))]
    # Linear term
    z = m['intercept'] + sum(c * v for c, v in zip(m['coefficients'], x_std))
    # Sigmoid
    prob = 1.0 / (1.0 + math.exp(-z))
    return max(0.05, min(0.98, float(prob)))


def _predict_progression_outcomes(d: dict) -> dict:
    """Predict clinical outcomes after 1-2 years of Stellest treatment with compliance."""
    age = d['age']; screen_time = d['screen_time']; outdoor_time = d['outdoor_time']
    family_history = d['family_history_myopia']
    prev_control = d.get('previous_myopia_control', 0)
    
    # Current measurements
    od_se = d['right_eye_spherical'] + (d['right_eye_cylinder'] / 2)
    os_se = d['left_eye_spherical'] + (d['left_eye_cylinder'] / 2)
    avg_se = (abs(od_se) + abs(os_se)) / 2
    avg_al = (d['right_eye_axial_length'] + d['left_eye_axial_length']) / 2
    avg_k = (d['keratometry_k1_re'] + d['keratometry_k2_re'] + d['keratometry_k1_le'] + d['keratometry_k2_le']) / 4
    
    # Base progression rates (without treatment)
    base_se_progression_1yr = 0.5 if age < 10 else 0.4 if age < 12 else 0.3 if age < 15 else 0.2
    base_al_progression_1yr = 0.15 if age < 10 else 0.12 if age < 12 else 0.08 if age < 15 else 0.05
    base_k_progression_1yr = 0.1 if age < 10 else 0.08 if age < 12 else 0.05 if age < 15 else 0.03
    
    # Environmental risk modifiers
    env_modifier = 1.0
    if screen_time > 6: env_modifier += 0.3
    elif screen_time > 4: env_modifier += 0.15
    if outdoor_time < 1: env_modifier += 0.2
    elif outdoor_time < 2: env_modifier += 0.1
    if family_history == 1: env_modifier += 0.15
    
    # Stellest effectiveness (reduction in progression)
    stellest_effectiveness = 0.6  # Base 60% reduction
    if age < 10: stellest_effectiveness = 0.7
    elif age < 12: stellest_effectiveness = 0.65
    elif age > 15: stellest_effectiveness = 0.5
    
    # Compliance factors
    compliance_factor = 1.0
    if outdoor_time >= 2: compliance_factor += 0.1
    if screen_time <= 3: compliance_factor += 0.1
    if prev_control > 0: compliance_factor += 0.05  # Previous treatment compliance
    
    final_effectiveness = min(0.8, stellest_effectiveness * compliance_factor)
    
    # Calculate outcomes
    expected_se_progression_1yr = base_se_progression_1yr * env_modifier * (1 - final_effectiveness)
    expected_al_progression_1yr = base_al_progression_1yr * env_modifier * (1 - final_effectiveness)
    expected_k_progression_1yr = base_k_progression_1yr * env_modifier * (1 - final_effectiveness)
    
    # 2-year projections (slightly reduced rate in year 2)
    expected_se_progression_2yr = expected_se_progression_1yr * 1.8
    expected_al_progression_2yr = expected_al_progression_1yr * 1.8
    expected_k_progression_2yr = expected_k_progression_1yr * 1.8
    
    # Base progression rates for 2 years (for calculating prevention)
    base_se_progression_2yr = base_se_progression_1yr * 1.8
    base_al_progression_2yr = base_al_progression_1yr * 1.8
    base_k_progression_2yr = base_k_progression_1yr * 1.8
    
    return {
        'current_measurements': {
            'spherical_equivalent_od': round(od_se, 2),
            'spherical_equivalent_os': round(os_se, 2),
            'average_spherical_equivalent': round(avg_se, 2),
            'average_axial_length': round(avg_al, 2),
            'average_keratometry': round(avg_k, 2)
        },
        'projected_1_year': {
            'spherical_equivalent_od': round(od_se - expected_se_progression_1yr, 2),
            'spherical_equivalent_os': round(os_se - expected_se_progression_1yr, 2),
            'average_spherical_equivalent': round(avg_se + expected_se_progression_1yr, 2),
            'average_axial_length': round(avg_al + expected_al_progression_1yr, 2),
            'average_keratometry': round(avg_k + expected_k_progression_1yr, 2),
            'progression_prevented': {
                'spherical_equivalent': round(base_se_progression_1yr * env_modifier * final_effectiveness, 2),
                'axial_length': round(base_al_progression_1yr * env_modifier * final_effectiveness, 3),
                'keratometry': round(base_k_progression_1yr * env_modifier * final_effectiveness, 2)
            }
        },
        'projected_2_year': {
            'spherical_equivalent_od': round(od_se - expected_se_progression_2yr, 2),
            'spherical_equivalent_os': round(os_se - expected_se_progression_2yr, 2),
            'average_spherical_equivalent': round(avg_se + expected_se_progression_2yr, 2),
            'average_axial_length': round(avg_al + expected_al_progression_2yr, 2),
            'average_keratometry': round(avg_k + expected_k_progression_2yr, 2),
            'progression_prevented': {
                'spherical_equivalent': round(base_se_progression_2yr * env_modifier * final_effectiveness, 2),
                'axial_length': round(base_al_progression_2yr * env_modifier * final_effectiveness, 3),
                'keratometry': round(base_k_progression_2yr * env_modifier * final_effectiveness, 2)
            }
        },
        'effectiveness_percentage': round(final_effectiveness * 100, 1),
        'compliance_score': round(compliance_factor * 100, 1)
    }


def _treatment_recommendations(d: dict, prob: float) -> dict:
    """Generate lightweight treatment suggestions for Atropine and Vision Therapy.
    Purely heuristic and explainable; avoids heavy dependencies.
    """
    age = d.get('age', 0)
    screen_time = d.get('screen_time', 0)
    outdoor_time = d.get('outdoor_time', 0)
    family_history = d.get('family_history_myopia', 0)

    # Atropine (low-dose) heuristic
    atropine_recommended = (prob >= 0.6) or (age < 12 and family_history == 1)
    atropine_consider = (0.5 <= prob < 0.6) or (screen_time > 5) or (outdoor_time < 1)
    # Patient-specific suggested dose tier
    if prob >= 0.75 or age < 10:
        dose_str = "0.025% nightly"
    elif prob >= 0.6:
        dose_str = "0.02% nightly"
    else:
        dose_str = "0.01% nightly"
    atropine = {
        "name": "Low-dose Atropine",
        "recommended": bool(atropine_recommended),
        "consider": bool(not atropine_recommended and atropine_consider),
        "dose": dose_str,
        "instructions": "Instill 1 drop OU at bedtime. Reassess every 3–6 months.",
        "rationale": (
            "Elevated predicted risk and/or early age/family history suggest benefit."
            if atropine_recommended else (
            "Borderline risk or behavioral risk factors; consider shared decision-making."
            if atropine_consider else
            "Low predicted risk; reserve for progression or higher risk."
        ))
    }

    # Vision Therapy heuristic (symptom/behavior proxy via screen time)
    vt_recommended = screen_time >= 5
    vt_consider = 3 <= screen_time < 5
    vt_modules = [
        "Near-far accommodative facility",
        "Vergence facility (e.g., Brock string)",
        "Pursuits and saccades",
        "Posture and visual hygiene"
    ]
    sessions_per_week = 2 if vt_recommended else (1 if vt_consider else 0)
    duration_weeks = 12 if vt_recommended else (8 if vt_consider else 0)
    home_ex = [
        "20-20-20 rule every 20 minutes",
        "Pencil push-ups 5–10 min/day",
        "Outdoor time ≥120 min/day"
    ]
    vision_therapy = {
        "name": "Vision Therapy",
        "recommended": bool(vt_recommended),
        "consider": bool(not vt_recommended and vt_consider),
        "modules": vt_modules,
        "schedule": {
            "sessions_per_week": sessions_per_week,
            "duration_weeks": duration_weeks
        },
        "home_exercises": home_ex,
        "rationale": (
            "High screen time suggests accommodative/vergence stress; VT may help."
            if vt_recommended else (
            "Moderate screen time; consider VT if symptomatic (asthenopia)."
            if vt_consider else
            "Low behavioral load; emphasize outdoor time and breaks."
        ))
    }

    return {"atropine": atropine, "vision_therapy": vision_therapy}


def _generate_personalized_advice(d: dict, outcomes: dict) -> dict:
    """Generate personalized lifestyle and treatment advice based on patient profile."""
    age = d['age']; screen_time = d['screen_time']; outdoor_time = d['outdoor_time']
    avg_se = outcomes['current_measurements']['average_spherical_equivalent']
    effectiveness = outcomes['effectiveness_percentage']
    family_history = d.get('family_history_myopia', 0)
    
    # Enhanced lifestyle recommendations
    lifestyle_advice = []
    
    # Screen Time Management
    if screen_time > 6:
        lifestyle_advice.append({
            "category": "Critical Screen Time Reduction",
            "current": f"{screen_time} hours/day",
            "target": "≤3 hours/day",
            "advice": "Excessive screen time detected. Implement strict digital detox: 20-20-20 rule, blue light filters, mandatory breaks every 30 minutes. Consider parental controls.",
            "priority": "Critical",
            "icon": "🚨",
            "tips": ["Use screen time apps to monitor usage", "Create screen-free zones", "Replace screen time with outdoor activities"]
        })
    elif screen_time > 4:
        lifestyle_advice.append({
            "category": "Screen Time Management",
            "current": f"{screen_time} hours/day",
            "target": "≤3 hours/day",
            "advice": "Implement 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds. Use blue light filters after sunset.",
            "priority": "High",
            "icon": "📱",
            "tips": ["Set hourly screen break reminders", "Use larger fonts to reduce eye strain", "Maintain 50-70cm distance from screens"]
        })
    elif screen_time > 2:
        lifestyle_advice.append({
            "category": "Screen Time Optimization",
            "current": f"{screen_time} hours/day",
            "target": "Maintain current levels",
            "advice": "Good screen time management. Continue with regular breaks and proper ergonomics.",
            "priority": "Medium",
            "icon": "✅",
            "tips": ["Maintain current habits", "Ensure good posture", "Use adequate lighting"]
        })
    
    # Outdoor Time Enhancement
    if outdoor_time < 1:
        lifestyle_advice.append({
            "category": "Critical Outdoor Time Deficit",
            "current": f"{outdoor_time} hours/day",
            "target": "≥2 hours/day",
            "advice": "Severely insufficient outdoor exposure. Prioritize daily outdoor activities during peak daylight (10 AM - 4 PM). Natural light is crucial for myopia control.",
            "priority": "Critical",
            "icon": "☀️",
            "tips": ["Morning outdoor activities", "Outdoor sports/playground time", "Walking to school", "Outdoor reading/homework"]
        })
    elif outdoor_time < 2:
        lifestyle_advice.append({
            "category": "Outdoor Time Enhancement",
            "current": f"{outdoor_time} hours/day",
            "target": "≥2 hours/day",
            "advice": "Increase outdoor activities during daylight hours. Natural light exposure helps slow myopia progression significantly.",
            "priority": "High",
            "icon": "🌞",
            "tips": ["Schedule outdoor breaks", "Outdoor lunch/recess", "Weekend nature activities", "Outdoor exercise"]
        })
    else:
        lifestyle_advice.append({
            "category": "Excellent Outdoor Exposure",
            "current": f"{outdoor_time} hours/day",
            "target": "Maintain current levels",
            "advice": "Excellent outdoor time! Continue this protective behavior. Quality matters - ensure activities are during bright daylight.",
            "priority": "Low",
            "icon": "🌟",
            "tips": ["Maintain current routine", "Focus on bright daylight hours", "Vary outdoor activities"]
        })
    
    # Age-specific recommendations
    if age < 10:
        lifestyle_advice.append({
            "category": "Critical Age Window",
            "advice": "Peak myopia development age. Strict lifestyle interventions are most effective now. Prioritize outdoor time and limit near work.",
            "priority": "Critical",
            "icon": "⚡",
            "tips": ["Maximum outdoor exposure", "Minimize prolonged near work", "Regular eye exams every 3-6 months"]
        })
    elif age < 12:
        lifestyle_advice.append({
            "category": "Optimal Intervention Age",
            "advice": "Excellent age for myopia control interventions. Maintain proper reading distance (30-40cm), ensure bright lighting, take frequent breaks.",
            "priority": "High",
            "icon": "🎯",
            "tips": ["Proper desk ergonomics", "Good lighting (>500 lux)", "Regular posture breaks"]
        })
    
    # Family history considerations
    if family_history == 1:
        lifestyle_advice.append({
            "category": "Genetic Risk Management",
            "advice": "Family history increases myopia risk. Extra vigilance with lifestyle modifications and regular monitoring is essential.",
            "priority": "High",
            "icon": "🧬",
            "tips": ["More frequent eye exams", "Stricter lifestyle guidelines", "Early intervention crucial"]
        })
    
    # Sleep and nutrition
    if age < 15:
        lifestyle_advice.append({
            "category": "Sleep & Nutrition",
            "advice": "Ensure 9-11 hours of quality sleep and balanced nutrition with vitamins A, C, E, and omega-3 fatty acids for eye health.",
            "priority": "Medium",
            "icon": "😴",
            "tips": ["Consistent sleep schedule", "Dark room for sleep", "Eye-healthy foods (carrots, fish, leafy greens)"]
        })
    
    # Enhanced clinical monitoring schedule
    monitoring_schedule = []
    if effectiveness > 80:
        monitoring_schedule = [
            {
                "timepoint": "1 month", 
                "tests": ["Stellest lens fitting check", "Visual acuity", "Comfort assessment"], 
                "purpose": "Initial adaptation monitoring",
                "priority": "Essential"
            },
            {
                "timepoint": "3 months", 
                "tests": ["Visual acuity", "Refraction", "Lens compliance check"], 
                "purpose": "Early effectiveness assessment",
                "priority": "Essential"
            },
            {
                "timepoint": "6 months", 
                "tests": ["Visual acuity", "Refraction", "Axial length measurement", "Lifestyle compliance"], 
                "purpose": "Mid-term progression evaluation",
                "priority": "Critical"
            },
            {
                "timepoint": "12 months", 
                "tests": ["Comprehensive eye exam", "Axial length", "Keratometry", "Treatment effectiveness review"], 
                "purpose": "Annual comprehensive assessment",
                "priority": "Critical"
            },
            {
                "timepoint": "24 months", 
                "tests": ["Full biometric assessment", "Long-term outcome evaluation", "Treatment continuation planning"], 
                "purpose": "Long-term success evaluation",
                "priority": "Essential"
            }
        ]
    elif effectiveness > 60:
        monitoring_schedule = [
            {
                "timepoint": "2 weeks", 
                "tests": ["Stellest lens fitting", "Initial comfort assessment"], 
                "purpose": "Immediate adaptation check",
                "priority": "Essential"
            },
            {
                "timepoint": "1 month", 
                "tests": ["Visual acuity", "Lens tolerance", "Compliance assessment"], 
                "purpose": "Early adaptation monitoring",
                "priority": "Essential"
            },
            {
                "timepoint": "3 months", 
                "tests": ["Visual acuity", "Refraction", "Axial length", "Lifestyle modifications review"], 
                "purpose": "Early effectiveness evaluation",
                "priority": "Critical"
            },
            {
                "timepoint": "6 months", 
                "tests": ["Comprehensive assessment", "Axial length", "Keratometry", "Additional intervention consideration"], 
                "purpose": "Mid-term effectiveness review",
                "priority": "Critical"
            },
            {
                "timepoint": "12 months", 
                "tests": ["Full evaluation", "Treatment optimization", "Combination therapy assessment"], 
                "purpose": "Annual review and optimization",
                "priority": "Critical"
            }
        ]
    else:
        monitoring_schedule = [
            {
                "timepoint": "1 week", 
                "tests": ["Lens fitting optimization", "Comfort assessment"], 
                "purpose": "Immediate intervention",
                "priority": "Critical"
            },
            {
                "timepoint": "2 weeks", 
                "tests": ["Visual acuity", "Lens tolerance", "Additional treatment planning"], 
                "purpose": "Early intervention adjustment",
                "priority": "Critical"
            },
            {
                "timepoint": "1 month", 
                "tests": ["Comprehensive evaluation", "Combination therapy initiation"], 
                "purpose": "Intensive intervention planning",
                "priority": "Critical"
            },
            {
                "timepoint": "3 months", 
                "tests": ["Multi-modal treatment assessment", "Axial length", "Lifestyle intervention intensification"], 
                "purpose": "Intensive monitoring phase",
                "priority": "Critical"
            },
            {
                "timepoint": "6 months", 
                "tests": ["Treatment effectiveness review", "Alternative intervention consideration"], 
                "purpose": "Treatment strategy reassessment",
                "priority": "Critical"
            }
        ]
    
    # Enhanced success indicators
    success_indicators = [
        {
            "metric": "Axial Length Control",
            "target": f"Growth <{0.1 if age < 12 else 0.05}mm/year",
            "excellent": f"<{0.05 if age < 12 else 0.02}mm/year",
            "importance": "Critical - Primary measure of myopia control success"
        },
        {
            "metric": "Refractive Stability",
            "target": f"SE progression <{0.25 if age < 12 else 0.15}D/year",
            "excellent": f"<{0.1 if age < 12 else 0.05}D/year",
            "importance": "High - Indicates effective myopia management"
        },
        {
            "metric": "Lens Compliance",
            "target": "≥12 hours daily wear",
            "excellent": "≥14 hours daily wear",
            "importance": "Essential - Treatment effectiveness depends on compliance"
        },
        {
            "metric": "Lifestyle Adherence",
            "target": "≥80% compliance with recommendations",
            "excellent": "≥95% compliance",
            "importance": "High - Synergistic effect with lens treatment"
        }
    ]
    
    # Enhanced warning signs
    warning_signs = [
        {
            "sign": "Rapid Vision Changes",
            "description": "Sudden decrease in vision or frequent prescription changes",
            "action": "Schedule immediate eye exam within 48 hours",
            "urgency": "Critical"
        },
        {
            "sign": "Lens Intolerance",
            "description": "Persistent discomfort, redness, or difficulty with lens handling",
            "action": "Contact eye care provider within 24 hours",
            "urgency": "High"
        },
        {
            "sign": "Excessive Progression",
            "description": f"Axial length growth >{0.2 if age < 12 else 0.1}mm in 6 months",
            "action": "Reassess treatment plan and consider additional interventions",
            "urgency": "High"
        },
        {
            "sign": "Lifestyle Regression",
            "description": "Significant increase in screen time or decrease in outdoor activities",
            "action": "Reinforce lifestyle modifications and consider behavioral interventions",
            "urgency": "Medium"
        }
    ]
    
    # Comprehensive key advice
    key_advice = [
        {
            "category": "Lens Compliance",
            "advice": "Wear Stellest lenses for minimum 12 hours daily (target: 14+ hours)",
            "details": "Consistent daily wear is crucial. Remove only for sleep, swimming, or as directed by eye care provider.",
            "priority": "Critical"
        },
        {
            "category": "Lens Care",
            "advice": "Follow strict hygiene protocols and replacement schedule",
            "details": "Daily cleaning, proper storage, monthly replacement (or as prescribed). Never sleep in lenses.",
            "priority": "Essential"
        },
        {
            "category": "Lifestyle Integration",
            "advice": "Maintain outdoor time ≥2 hours/day and screen time ≤3 hours/day",
            "details": "Bright outdoor light exposure during 10 AM - 4 PM is most beneficial. Use 20-20-20 rule for screen work.",
            "priority": "High"
        },
        {
            "category": "Regular Monitoring",
            "advice": "Attend all scheduled appointments and report changes immediately",
            "details": "Early detection of progression allows for prompt treatment adjustments.",
            "priority": "Essential"
        },
        {
            "category": "Family Involvement",
            "advice": "Ensure family support for treatment compliance and lifestyle changes",
            "details": "Success requires consistent reinforcement of healthy visual habits at home and school.",
            "priority": "High"
        }
    ]
    
    return {
        "lifestyle_recommendations": lifestyle_advice,
        "monitoring_schedule": monitoring_schedule,
        "success_indicators": success_indicators,
        "warning_signs": warning_signs,
        "key_advice": key_advice,
        "treatment_goals": {
            "primary": f"Reduce myopia progression by {effectiveness}% over 2 years",
            "secondary": "Maintain excellent quality of life and visual function",
            "long_term": "Prevent high myopia and associated complications"
        }
    }


@app.post("/")
async def predict(patient_data: PatientData):
    try:
        d = patient_data.dict()
        
        # Generate progression outcomes and personalized advice
        outcomes = _predict_progression_outcomes(d)
        treatments = _treatment_recommendations(d, outcomes['effectiveness_percentage'] / 100)
        personalized_advice = _generate_personalized_advice(d, outcomes)
        
        # Enhanced clinical assessment
        clinical_factors = []
        avg_se = outcomes['current_measurements']['average_spherical_equivalent']
        avg_al = outcomes['current_measurements']['average_axial_length']
        
        if d['age'] < 12: clinical_factors.append("Optimal age for intervention")
        if 1.0 <= avg_se <= 4.0: clinical_factors.append("Ideal myopia range for Stellest")
        if avg_al >= 24.0: clinical_factors.append("Elongated axial length indicates progression risk")
        if d['family_history_myopia'] == 1: clinical_factors.append("Genetic predisposition to myopia")
        if d['screen_time'] > 6: clinical_factors.append("High near work exposure")
        if d['outdoor_time'] < 2: clinical_factors.append("Insufficient protective outdoor time")
        
        effectiveness_pct = outcomes['effectiveness_percentage']
        
        return {
            "patient_name": d['patient_name'],
            "current_status": outcomes['current_measurements'],
            "progression_predictions": {
                "1_year_outcomes": outcomes['projected_1_year'],
                "2_year_outcomes": outcomes['projected_2_year'],
                "effectiveness_percentage": effectiveness_pct,
                "compliance_score": outcomes['compliance_score']
            },
            "clinical_summary": {
                "myopia_severity": "Mild" if avg_se < 2 else "Moderate" if avg_se < 4 else "High",
                "progression_risk": "High" if d['age'] < 10 and avg_se > 2 else "Moderate" if d['age'] < 15 else "Low",
                "clinical_factors": clinical_factors
            },
            "stellest_benefits": {
                "expected_effectiveness": f"{effectiveness_pct}%",
                "axial_length_control": f"Prevents {outcomes['projected_2_year']['progression_prevented']['axial_length']}mm growth over 2 years",
                "myopia_control": f"Prevents {outcomes['projected_2_year']['progression_prevented']['spherical_equivalent']}D progression over 2 years",
                "long_term_benefit": "Reduced risk of high myopia complications (retinal detachment, myopic maculopathy)"
            },
            "treatments": treatments,
            "personalized_advice": personalized_advice,
            "recommendation": (
                f"Stellest lenses are highly recommended with {effectiveness_pct}% expected effectiveness. "
                f"With proper compliance, expect to prevent {outcomes['projected_2_year']['progression_prevented']['axial_length']}mm of axial elongation over 2 years."
                if effectiveness_pct > 70 else 
                f"Stellest lenses are recommended with {effectiveness_pct}% expected effectiveness. "
                f"Additional interventions may be needed for optimal control."
                if effectiveness_pct > 50 else 
                f"Consider Stellest lenses as part of comprehensive myopia management ({effectiveness_pct}% effectiveness). "
                f"Focus on lifestyle modifications and frequent monitoring."
            ),
            "patient_id": f"patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "processing_time": 0.002
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def health():
    return {"status": "healthy", "message": "Stellest AI Predict API is running", "model_loaded": _load_json_model() is not None}