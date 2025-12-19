#!/bin/bash
# Git Repository Setup Script

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         Git Repository Setup                              ║"
echo "║         Geometric Resolution of Hubble Tension            ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

echo "✓ Git is installed"
echo ""

# Initialize git repository if not already initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

echo ""
echo "Setting up .gitignore..."

# Ensure .gitignore exists and has correct content
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter
.ipynb_checkpoints/

# Results (keep structure, ignore data)
results/*.json
results/plots/*.png

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# LaTeX (in paper/)
paper/*.aux
paper/*.log
paper/*.bbl
paper/*.blg
paper/*.out
paper/*.toc
paper/*.synctex.gz
EOF
    echo "✓ .gitignore created"
else
    echo "✓ .gitignore already exists"
fi

echo ""
echo "Staging files for commit..."

# Add all files
git add .

echo "✓ Files staged"
echo ""

# Show status
echo "Git status:"
git status --short

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Review staged files above"
echo "2. Commit:"
echo "   git commit -m \"Initial commit: Geometric Resolution of Hubble Tension\""
echo ""
echo "3. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: lcdm-mcmc"
echo "   - Description: Geometric Resolution of the Hubble Tension"
echo "   - Public repository"
echo "   - Do NOT initialize with README (we have one)"
echo ""
echo "4. Add remote and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/lcdm-mcmc.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "═══════════════════════════════════════════════════════════"
