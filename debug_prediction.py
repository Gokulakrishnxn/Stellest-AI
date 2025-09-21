#!/usr/bin/env python3
"""
Debug script to test model prediction directly
"""

import sys
import os
sys.path.append('.')

from ai_model_simple import StellesteAIModel

def test_direct_prediction():
    """Test prediction directly with the model"""
    print("🔍 DEBUGGING MODEL PREDICTION")
    print("=" * 40)
    
    try:
        # Load model
        print("📂 Loading model...")
        model = StellesteAIModel()
        model_path = 'models/stellest_ai_model.pkl'
        model.load_model(model_path)
        print("✅ Model loaded successfully")
        
        # Sample patient data
        patient_data = {
            'age': 12.0,
            'age_myopia_diagnosis': 8.0,
            'gender': 2,
            'family_history_myopia': 1,
            'outdoor_time': 1.5,
            'screen_time': 4.0,
            'previous_myopia_control': 0,
            'initial_power_re': -3.5,
            'initial_power_le': -3.25,
            'initial_axial_length_re': 24.5,
            'initial_axial_length_le': 24.3,
            'stellest_wearing_time': 14.0,
            'myopia_duration': 4.0,
            'average_initial_power': 3.375,
            'average_initial_al': 24.4,
            'screen_outdoor_ratio': 2.67
        }
        
        print("🔮 Making prediction...")
        result = model.predict_stellest_uptake(patient_data)
        
        print("✅ Prediction successful!")
        print(f"📈 Will Benefit: {result['ensemble_prediction']['will_benefit']}")
        print(f"📊 Probability: {result['ensemble_prediction']['probability']:.3f}")
        print(f"🎯 Confidence: {result['ensemble_prediction']['confidence']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_direct_prediction()
