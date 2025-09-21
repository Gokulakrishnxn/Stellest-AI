#!/usr/bin/env python3
"""
Simple and reliable startup script for Stellest Lens Myopia Prediction Platform
"""

import os
import sys
import subprocess
import time

def main():
    """Start the website"""
    print("🏥 STELLEST LENS MYOPIA PREDICTION PLATFORM")
    print("=" * 60)
    print("🤖 AI-Powered Clinical Decision Support System")
    print("🔬 Predicting Therapeutic Lens Effectiveness")
    print("=" * 60)
    print()
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, 'backend')
    
    print(f"📁 Project root: {project_root}")
    print(f"📁 Backend directory: {backend_dir}")
    print()
    
    # Verify required files exist
    required_files = [
        'ai_model_simple.py',
        'data_preprocessing.py', 
        'models/stellest_ai_model.pkl',
        'backend/app.py',
        'Stellest_Restrospective Data to Hindustan.xlsx'
    ]
    
    print("🔍 Checking required files...")
    for file_path in required_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (MISSING)")
            return False
    
    print()
    print("🚀 Starting the web server...")
    print("📊 Server will be available at: http://localhost:8000")
    print("📖 API Documentation at: http://localhost:8000/docs")
    print("🔬 Interactive API at: http://localhost:8000/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Change to project root and add to Python path
    os.chdir(project_root)
    sys.path.insert(0, project_root)
    
    # Start the server from the backend directory but with project root in path
    try:
        env = os.environ.copy()
        env['PYTHONPATH'] = project_root
        
        # Start uvicorn from project root, pointing to backend/app:app
        result = subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'backend.app:app',  # Use module notation
            '--host', '0.0.0.0',
            '--port', '8000',
            '--reload'
        ], env=env, cwd=project_root)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        print("Thank you for using the Stellest Lens Prediction Platform!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("Please check the error message above and try again.")

if __name__ == "__main__":
    main()
