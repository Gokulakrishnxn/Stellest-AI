#!/usr/bin/env python3
"""
Demo script to show website output and functionality
"""

import requests
import json
import webbrowser
import time

def demo_website_output():
    """Demonstrate the website output"""
    print("🌐 STELLEST LENS WEBSITE OUTPUT DEMONSTRATION")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print("✅ Website is running!")
            print(f"📊 Status: {health['status']}")
            print(f"🤖 AI Model: {'Loaded' if health['model_loaded'] else 'Not Loaded'}")
        else:
            print("❌ Website not responding")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to website: {e}")
        print("💡 Start the website with: python3 start_website.py")
        return False
    
    print("\n🔍 TESTING PREDICTION OUTPUT")
    print("-" * 40)
    
    # Sample patient data
    patient_data = {
        "age": 12.0,
        "age_myopia_diagnosis": 8.0,
        "gender": 2,  # Female
        "family_history_myopia": 1,  # Yes
        "outdoor_time": 1.5,
        "screen_time": 4.0,
        "previous_myopia_control": 0,  # No
        "initial_power_re": -3.5,
        "initial_power_le": -3.25,
        "initial_axial_length_re": 24.5,
        "initial_axial_length_le": 24.3,
        "stellest_wearing_time": 14.0
    }
    
    print("👤 Sample Patient Profile:")
    print(f"   Age: {patient_data['age']} years")
    print(f"   Gender: {'Female' if patient_data['gender'] == 2 else 'Male'}")
    print(f"   Myopia Power: -{(abs(patient_data['initial_power_re']) + abs(patient_data['initial_power_le']))/2:.2f}D (average)")
    print(f"   Family History: {'Yes' if patient_data['family_history_myopia'] else 'No'}")
    print(f"   Lifestyle: {patient_data['outdoor_time']}h outdoor, {patient_data['screen_time']}h screen")
    print(f"   Expected Compliance: {patient_data['stellest_wearing_time']}h/day")
    
    # Make prediction
    try:
        response = requests.post("http://localhost:8000/predict", json=patient_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            
            print("\n🎯 PREDICTION RESULTS:")
            print("-" * 30)
            
            # Main prediction
            ensemble = result['ensemble_prediction']
            print(f"✅ Treatment Recommendation: {'WILL BENEFIT' if ensemble['will_benefit'] else 'MAY NOT BENEFIT'}")
            print(f"📊 Success Probability: {ensemble['probability']:.1%}")
            print(f"🎯 Confidence Level: {ensemble['confidence']}")
            print(f"💡 Clinical Recommendation: {result['recommendation']}")
            
            # Risk factors
            risk_factors = result['risk_factors']
            if risk_factors['high_risk']:
                print(f"⚠️  High Risk Factors: {', '.join(risk_factors['high_risk'])}")
            if risk_factors['medium_risk']:
                print(f"🟡 Medium Risk Factors: {', '.join(risk_factors['medium_risk'])}")
            if risk_factors['protective']:
                print(f"✅ Protective Factors: {', '.join(risk_factors['protective'])}")
            
            # Enhanced analytics
            if 'enhanced_analytics' in result:
                analytics = result['enhanced_analytics']
                print(f"\n📈 ENHANCED ANALYTICS:")
                print(f"   Risk Category: {analytics['risk_profile']['risk_category']}")
                print(f"   Risk Score: {analytics['risk_profile']['risk_score']}/10")
                print(f"   Similar Patients Success Rate: {analytics['outcome_analysis']['similar_patients_success_rate']:.1%}")
                print(f"   Sample Size: {analytics['outcome_analysis']['sample_size']} similar patients")
            
            # Individual models
            print(f"\n🤖 INDIVIDUAL MODEL RESULTS:")
            for model_name, model_result in result['individual_models'].items():
                print(f"   {model_name.replace('_', ' ').title()}: {model_result['probability']:.1%} ({model_result['confidence']})")
            
            print(f"\n📋 DETAILED RECOMMENDATIONS:")
            if 'enhanced_analytics' in result and 'detailed_recommendations' in result['enhanced_analytics']:
                for rec in result['enhanced_analytics']['detailed_recommendations']:
                    print(f"   • {rec['category']}: {rec['recommendation']} ({rec['priority']} priority)")
            
            print(f"\n🎉 PREDICTION COMPLETED SUCCESSFULLY!")
            print(f"📄 Full results available in the web interface")
            
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False
    
    # Show how to access the website
    print(f"\n🌐 ACCESS YOUR WEBSITE:")
    print(f"   Main Interface: http://localhost:8000")
    print(f"   API Documentation: http://localhost:8000/docs")
    print(f"   Interactive API: http://localhost:8000/redoc")
    
    print(f"\n📝 HOW TO USE THE WEBSITE:")
    print(f"   1. Open http://localhost:8000 in your browser")
    print(f"   2. Fill in the patient information form")
    print(f"   3. Click 'Predict Stellest Lens Effectiveness'")
    print(f"   4. View comprehensive AI analysis and recommendations")
    
    # Ask if user wants to open browser
    try:
        user_input = input(f"\n🚀 Would you like to open the website in your browser now? (y/n): ")
        if user_input.lower() in ['y', 'yes']:
            webbrowser.open('http://localhost:8000')
            print("🌐 Website opened in your default browser!")
    except:
        print("🌐 Open http://localhost:8000 in your browser to see the full interface")
    
    return True

if __name__ == "__main__":
    demo_website_output()
