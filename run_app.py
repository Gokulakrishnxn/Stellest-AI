#!/usr/bin/env python3
"""
Simple startup script for Stellest Lens Myopia Prediction Platform
"""

import uvicorn
import os
import sys

def main():
    """Start the application"""
    print("🏥 STELLEST LENS MYOPIA PREDICTION PLATFORM")
    print("=" * 60)
    print("🤖 AI-Powered Clinical Decision Support System")
    print("🔬 Predicting Therapeutic Lens Effectiveness")
    print("=" * 60)
    print()
    
    print("🚀 Starting the web server...")
    print("📊 Server will be available at: http://localhost:8000")
    print("📖 API Documentation at: http://localhost:8000/docs")
    print("🔬 Interactive API at: http://localhost:8000/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    os.chdir(backend_dir)
    
    # Add parent directory to path for imports
    sys.path.insert(0, os.path.dirname(backend_dir))
    
    try:
        # Start the server
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for stability
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        print("Thank you for using the Stellest Lens Prediction Platform!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("Please check the error message above and try again.")

if __name__ == "__main__":
    main()
