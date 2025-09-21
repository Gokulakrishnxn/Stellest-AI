#!/usr/bin/env python3
"""
Startup script for Stellest Lens Myopia Prediction Platform
Initializes the AI model and starts the web server
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def check_model_training():
    """Check if model training is complete"""
    model_path = Path('models/stellest_ai_model.pkl')
    if model_path.exists():
        print("✅ AI model found and ready")
        return True
    
    print("⏳ AI model training in progress...")
    
    # Check if training process is running
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'ai_model_simple.py' in result.stdout:
            print("🔄 Model training is currently running. Please wait...")
            return False
        else:
            print("🚀 Starting model training...")
            # Start training if not running
            subprocess.Popen([
                sys.executable, 'ai_model_simple.py'
            ], stdout=open('model_training.log', 'w'), stderr=subprocess.STDOUT)
            return False
    except Exception as e:
        print(f"❌ Error checking training status: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    dirs = ['models', 'static', 'data', 'backend', 'frontend']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("📁 Directory structure ready")

def start_server():
    """Start the FastAPI server"""
    print("🌐 Starting Stellest Lens Prediction Platform...")
    print("📊 Server will be available at: http://localhost:8000")
    print("📖 API Documentation at: http://localhost:8000/docs")
    print("🔬 Interactive API at: http://localhost:8000/redoc")
    print("\n" + "="*60)
    
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

def main():
    """Main startup function"""
    print("🏥 STELLEST LENS MYOPIA PREDICTION PLATFORM")
    print("=" * 60)
    print("🤖 AI-Powered Clinical Decision Support System")
    print("🔬 Predicting Therapeutic Lens Effectiveness")
    print("=" * 60 + "\n")
    
    # Setup
    setup_directories()
    
    # Check if we can start immediately or need to wait for training
    if check_model_training():
        start_server()
    else:
        print("\n⏱️  Waiting for model training to complete...")
        print("💡 You can monitor progress in model_training.log")
        print("🔄 The server will start automatically once training is done")
        
        # Wait for model to be ready
        while not check_model_training():
            time.sleep(30)  # Check every 30 seconds
        
        print("\n🎉 Model training completed!")
        time.sleep(2)
        start_server()

if __name__ == "__main__":
    main()
