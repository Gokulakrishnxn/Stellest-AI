#!/bin/bash

# Stellest AI - GitHub Setup Script
echo "🔬 Setting up Stellest AI for GitHub deployment..."

# Initialize git repository
echo "🔄 Initializing Git repository..."
git init

# Add all files
echo "🔄 Adding files to Git..."
git add .

# Create initial commit
echo "🔄 Creating initial commit..."
git commit -m "Initial commit: Stellest AI Myopia Prediction Platform

- AI-powered myopia prediction using ensemble ML models
- Responsive web interface with dark theme
- FastAPI backend with comprehensive analytics
- OpenAI integration for clinical insights
- Ready for Vercel deployment"

# Set main branch
echo "🔄 Setting main branch..."
git branch -M main

# Add remote origin
echo "🔄 Adding remote origin..."
git remote add origin https://github.com/Gokulakrishnxn/Stellest-AI.git

# Push to GitHub
echo "🔄 Pushing to GitHub..."
git push -u origin main

echo ""
echo "🎊 GitHub setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://vercel.com"
echo "2. Import your GitHub repository"
echo "3. Deploy automatically"
echo "4. Your app will be available at: https://stellest-ai.vercel.app"
echo ""
echo "🔗 Repository: https://github.com/Gokulakrishnxn/Stellest-AI"
echo "📚 Documentation: Check README.md for detailed instructions"
