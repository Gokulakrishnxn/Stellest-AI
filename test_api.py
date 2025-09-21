#!/usr/bin/env python3
"""
Test script for the API endpoints
"""

import requests
import json

def test_prediction():
    """Test the prediction endpoint"""
    url = "http://localhost:8000/predict"
    
    # Sample patient data
    patient_data = {
        "age": 12.0,
        "age_myopia_diagnosis": 8.0,
        "gender": 2,
        "family_history_myopia": 1,
        "outdoor_time": 1.5,
        "screen_time": 4.0,
        "previous_myopia_control": 0,
        "initial_power_re": -3.5,
        "initial_power_le": -3.25,
        "initial_axial_length_re": 24.5,
        "initial_axial_length_le": 24.3,
        "stellest_wearing_time": 14.0
    }
    
    print("🧪 Testing API Prediction Endpoint")
    print("=" * 40)
    print("📊 Sending sample patient data...")
    
    try:
        response = requests.post(url, json=patient_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction successful!")
            print(f"📈 Will Benefit: {result['ensemble_prediction']['will_benefit']}")
            print(f"📊 Probability: {result['ensemble_prediction']['probability']:.3f}")
            print(f"🎯 Confidence: {result['ensemble_prediction']['confidence']}")
            print(f"💡 Recommendation: {result['recommendation'][:100]}...")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Error message: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print("✅ Health check passed")
            print(f"📊 Status: {health['status']}")
            print(f"🤖 Model loaded: {health['model_loaded']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def main():
    """Run API tests"""
    print("🌐 STELLEST LENS API TESTING")
    print("=" * 40)
    
    # Test health first
    if not test_health():
        print("❌ Server not responding. Please check if it's running.")
        return False
    
    print()
    
    # Test prediction
    success = test_prediction()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 All API tests passed!")
        print("✅ Platform is working correctly")
        print("🌐 Access the web interface at: http://localhost:8000")
    else:
        print("⚠️  Some tests failed")
        print("Please check the server logs for details")
    
    return success

if __name__ == "__main__":
    main()
