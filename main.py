#!/usr/bin/env python3
"""
Main entry point for Stellest AI Prediction Platform
"""

import sys
import os

if __name__ == "__main__":
    import uvicorn
    from backend.app import app
    
    print("🔬 Starting Stellest AI Prediction Platform...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🧪 Test Page: http://localhost:8000/test")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
