#!/bin/bash
# Git Setup Script for Swiggy CLI
# Run this to initialize Git and prepare for pushing to Xevio (or GitHub/GitLab)

set -e

echo "📦 Setting up Git repository for Swiggy CLI..."
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first:"
    echo "  macOS: brew install git"
    echo "  Ubuntu/Debian: sudo apt install git"
    exit 1
fi

# Navigate to project
cd "$(dirname "$0")" || cd ~/.clawdbot/workspace/swiggy-cli

echo "📍 Current directory: $(pwd)"
echo ""

# Initialize git if not already done
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
    cat > .gitignore << 'EOF'
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
EOF
    echo "✅ .gitignore created"
else
    echo "✅ .gitignore already exists"
fi
echo ""

# Add all files
echo "📦 Staging files..."
git add .
echo "✅ Files staged"
echo ""

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    echo "✅ Remote 'origin' already configured"
    echo ""
    echo "🚀 To push updates, run:"
    echo "   git commit -m 'Your update message'"
    echo "   git push -u origin main"
else
    echo ""
    echo "📝 No remote configured yet."
    echo ""
    echo "🔗 Next steps:"
    echo ""
    echo "1. Go to Xevio (or GitHub/GitLab/Bitbucket)"
    echo "2. Create a new empty repository"
    echo "3. Copy the remote URL"
    echo "4. Run this command to link:"
    echo ""
    echo "   git remote add origin <PASTE_REMOTE_URL_HERE>"
    echo ""
    echo "5. Then push:"
    echo "   git push -u origin main"
    echo ""
    echo "💡 Tip: After first push, you can just use:"
    echo "   git add . && git commit -m 'message' && git push"
fi
