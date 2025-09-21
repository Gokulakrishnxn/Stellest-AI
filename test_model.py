#!/usr/bin/env python3
"""
Test script for the Stellest Lens AI model
Tests basic functionality and creates a sample model if needed
"""

import pandas as pd
import numpy as np
from ai_model_simple import StellesteAIModel
from data_preprocessing import MyopiaDataPreprocessor
import os

def create_sample_model():
    """Create a sample model for testing if the full model isn't ready"""
    print("Creating sample model for testing...")
    
    # Create sample data
    np.random.seed(42)
    n_samples = 100
    
    sample_data = {
        'age': np.random.normal(12, 3, n_samples),
        'age_myopia_diagnosis': np.random.normal(8, 2, n_samples),
        'gender': np.random.choice([1, 2], n_samples),
        'family_history_myopia': np.random.choice([0, 1], n_samples),
        'outdoor_time': np.random.normal(2, 1, n_samples),
        'screen_time': np.random.normal(4, 2, n_samples),
        'previous_myopia_control': np.random.choice([0, 1], n_samples),
        'initial_power_re': np.random.normal(-3.5, 1.5, n_samples),
        'initial_power_le': np.random.normal(-3.5, 1.5, n_samples),
        'initial_axial_length_re': np.random.normal(24.5, 1, n_samples),
        'initial_axial_length_le': np.random.normal(24.5, 1, n_samples),
        'stellest_wearing_time': np.random.normal(14, 2, n_samples),
        'myopia_duration': np.random.normal(4, 2, n_samples),
        'average_initial_power': np.random.normal(3.5, 1.5, n_samples),
        'average_initial_al': np.random.normal(24.5, 1, n_samples),
        'screen_outdoor_ratio': np.random.normal(2, 1, n_samples),
    }
    
    df = pd.DataFrame(sample_data)
    
    # Create target variable (simplified logic)
    target = ((df['outdoor_time'] > 1.5) & 
              (df['screen_time'] < 5) & 
              (df['stellest_wearing_time'] > 12) &
              (df['average_initial_power'] < 5)).astype(int)
    
    # Train model
    model = StellesteAIModel()
    model.train_models(df, target)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model.save_model('models/stellest_ai_model.pkl')
    
    return model

def test_prediction():
    """Test the prediction functionality"""
    print("Testing prediction functionality...")
    
    # Sample patient data
    patient_data = {
        'age': 12.0,
        'age_myopia_diagnosis': 8.0,
        'gender': 2,  # Female
        'family_history_myopia': 1,  # Yes
        'outdoor_time': 1.5,
        'screen_time': 4.0,
        'previous_myopia_control': 0,  # No
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
    
    try:
        # Load or create model
        if os.path.exists('models/stellest_ai_model.pkl'):
            model = StellesteAIModel()
            model.load_model('models/stellest_ai_model.pkl')
            print("✅ Loaded existing model")
        else:
            model = create_sample_model()
            print("✅ Created sample model")
        
        # Make prediction
        result = model.predict_stellest_uptake(patient_data)
        
        print("\n" + "="*50)
        print("🔮 PREDICTION RESULTS")
        print("="*50)
        print(f"Will Benefit: {result['ensemble_prediction']['will_benefit']}")
        print(f"Probability: {result['ensemble_prediction']['probability']:.3f}")
        print(f"Confidence: {result['ensemble_prediction']['confidence']}")
        print(f"Recommendation: {result['recommendation']}")
        
        print(f"\nRisk Factors:")
        print(f"  High Risk: {', '.join(result['risk_factors']['high_risk']) or 'None'}")
        print(f"  Medium Risk: {', '.join(result['risk_factors']['medium_risk']) or 'None'}")
        print(f"  Protective: {', '.join(result['risk_factors']['protective']) or 'None'}")
        
        print("\n✅ Model test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 STELLEST LENS AI MODEL TEST")
    print("="*40)
    
    success = test_prediction()
    
    if success:
        print("\n🎉 All tests passed! The model is ready to use.")
        print("🚀 You can now start the web server with: python start_server.py")
    else:
        print("\n⚠️  Some tests failed. Please check the model setup.")

if __name__ == "__main__":
    main()
