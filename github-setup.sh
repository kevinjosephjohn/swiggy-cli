#!/bin/bash
# GitHub Setup Script for Swiggy CLI

set -e

echo "🐙 Setting up GitHub repository..."
echo ""

# Navigate to project
cd "$(dirname "$0")" || cd ~/.clawdbot/workspace/swiggy-cli

echo "📍 Current directory: $(pwd)"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi
echo ""

# Create .gitignore if not exists
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'GITIGNOREEOF'
# Virtual Environment
venv/
__pycache__/
*.pyc

# Session files (contain sensitive auth data)
.swiggy-cli/
session.json

# IDE files
.vscode/
.idea/
*.swp
*.swo
GITIGNOREEOF
    echo "✅ .gitignore created"
fi
echo ""

# Add all files
echo "📦 Staging files..."
git add .
echo "✅ Files staged"
echo ""

echo "🔗 Next steps to push to GitHub:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create repository named 'swiggy-cli'"
echo "3. Copy your repository URL (should look like: https://github.com/YOUR_USERNAME/swiggy-cli.git)"
echo ""
echo "4. Run these commands:"
echo ""
echo "   git commit -m 'Initial Swiggy CLI implementation'"
echo "   git remote add origin <PASTE_YOUR_GITHUB_URL_HERE>"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "💡 After first push, you can just use:"
echo "   git add . && git commit -m 'message' && git push"
