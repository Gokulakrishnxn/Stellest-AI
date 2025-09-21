#!/usr/bin/env python3
"""
Deployment script for Stellest AI Platform
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Stellest AI Platform Deployment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src/backend/app.py"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Test the application
    print("🧪 Testing application...")
    if not run_command("python -c 'from src.backend.app import app; print(\"App imported successfully\")'", "Testing imports"):
        print("⚠️ Import test failed, but continuing...")
    
    print("\n🎊 Deployment preparation completed!")
    print("\n📋 Next steps:")
    print("1. Push to GitHub: git add . && git commit -m 'Deploy to production' && git push")
    print("2. Deploy to Vercel: Connect your GitHub repo to Vercel")
    print("3. Add environment variables in Vercel dashboard")
    print("4. Your app will be available at: https://your-app.vercel.app")
    
    print("\n🔗 Useful URLs:")
    print("- Main app: https://your-app.vercel.app")
    print("- API docs: https://your-app.vercel.app/docs")
    print("- Test page: https://your-app.vercel.app/test")

if __name__ == "__main__":
    main()
