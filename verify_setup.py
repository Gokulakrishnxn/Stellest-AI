#!/usr/bin/env python3
"""
Verification script for Stellest Lens Platform
Checks all components before starting the server
"""

import os
import sys
import importlib.util

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (NOT FOUND)")
        return False

def check_import(module_name):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} import: OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} import: FAILED ({e})")
        return False

def check_directory(dir_path, description):
    """Check if a directory exists"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} (NOT FOUND)")
        return False

def main():
    """Run all verification checks"""
    print("🔍 STELLEST LENS PLATFORM VERIFICATION")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check core dependencies
    print("\n📦 Checking Dependencies:")
    dependencies = ['fastapi', 'uvicorn', 'pandas', 'numpy', 'sklearn', 'matplotlib', 'seaborn', 'joblib', 'openpyxl']
    for dep in dependencies:
        if not check_import(dep):
            all_checks_passed = False
    
    # Check core files
    print("\n📄 Checking Core Files:")
    files_to_check = [
        ('data_preprocessing.py', 'Data preprocessing script'),
        ('ai_model_simple.py', 'AI model script'),
        ('backend/app.py', 'Backend API server'),
        ('frontend/index.html', 'Frontend HTML'),
        ('frontend/app.js', 'Frontend JavaScript'),
        ('Stellest_Restrospective Data to Hindustan.xlsx', 'Dataset file')
    ]
    
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # Check directories
    print("\n📁 Checking Directories:")
    directories = [
        ('backend', 'Backend directory'),
        ('frontend', 'Frontend directory'),
        ('static', 'Static files directory'),
        ('models', 'Models directory'),
        ('data', 'Data directory')
    ]
    
    for dir_path, description in directories:
        if not check_directory(dir_path, description):
            all_checks_passed = False
    
    # Check AI model
    print("\n🤖 Checking AI Model:")
    model_file = 'models/stellest_ai_model.pkl'
    if check_file_exists(model_file, 'Trained AI model'):
        try:
            sys.path.append('.')
            from ai_model_simple import StellesteAIModel
            model = StellesteAIModel()
            model.load_model(model_file)
            print("✅ AI model loads successfully")
            
            # Test prediction
            sample_data = {
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
            
            result = model.predict_stellest_uptake(sample_data)
            print("✅ AI model prediction works")
            
        except Exception as e:
            print(f"❌ AI model test failed: {e}")
            all_checks_passed = False
    else:
        all_checks_passed = False
    
    # Check backend app
    print("\n🌐 Checking Backend App:")
    try:
        from backend.app import app
        print("✅ Backend app imports successfully")
    except Exception as e:
        print(f"❌ Backend app import failed: {e}")
        all_checks_passed = False
    
    # Final result
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Platform is ready to run")
        print("🚀 Start with: python3 run_app.py")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("❌ Please fix the issues above before running")
    print("=" * 50)
    
    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
