#!/bin/bash
# Repository Cleanup Script
# Organize files into proper directories and remove temporary files

echo "=========================================="
echo "REPOSITORY CLEANUP"
echo "=========================================="

# Create directory structure
echo "Creating directory structure..."
mkdir -p docs
mkdir -p scripts
mkdir -p tests
mkdir -p examples
mkdir -p logs

# Move documentation files
echo "Organizing documentation..."
mv ARCHITECTURE.md docs/ 2>/dev/null
mv CHECKLIST.md docs/ 2>/dev/null
mv PRINCIPLES.md docs/ 2>/dev/null
mv PROJECT_SUMMARY.md docs/ 2>/dev/null
mv QUICKSTART.md docs/ 2>/dev/null
mv STATUS.md docs/ 2>/dev/null
mv REAL_DATA_INTEGRATION.md docs/ 2>/dev/null
mv REAL_DATA_RESULTS.md docs/ 2>/dev/null
mv THEORY_COMPLETE.md docs/ 2>/dev/null
mv PUBLICATION_STRATEGY.md docs/ 2>/dev/null
mv PUBLISH_TO_GITHUB.md docs/ 2>/dev/null
mv REPOSITORY_LIVE.md docs/ 2>/dev/null
mv GITHUB_READY.md docs/ 2>/dev/null

# Move scripts
echo "Organizing scripts..."
mv run_analysis.sh scripts/ 2>/dev/null
mv setup_git.sh scripts/ 2>/dev/null
mv test_all.sh scripts/ 2>/dev/null
mv regenerate_all_plots.py scripts/ 2>/dev/null
mv optimize_dipole_plot.py scripts/ 2>/dev/null
mv plot_final_comparison.py scripts/ 2>/dev/null

# Move examples
echo "Organizing examples..."
mv example_notebook.py examples/ 2>/dev/null

# Move logs
echo "Organizing logs..."
mv mcmc_comparison_output.txt logs/ 2>/dev/null
mv plot_regeneration.log logs/ 2>/dev/null
mv output.png logs/ 2>/dev/null

# Remove Python cache
echo "Cleaning Python cache..."
rm -rf __pycache__

# Update .gitignore
echo "Updating .gitignore..."
cat >> .gitignore << 'EOF'

# Logs
logs/*.log
logs/*.txt

# Temporary files
*.tmp
*.temp

# IDE
.vscode/
.idea/

EOF

echo ""
echo "=========================================="
echo "CLEANUP COMPLETE"
echo "=========================================="
echo ""
echo "New structure:"
echo "  docs/          - All documentation"
echo "  scripts/       - Utility scripts"
echo "  examples/      - Example code"
echo "  logs/          - Log files"
echo "  paper/         - LaTeX paper"
echo "  data/          - Real data files"
echo "  results/       - Analysis results"
echo ""
echo "Core modules remain in root:"
echo "  besemer_core.py"
echo "  scanner.py"
echo "  data_loader.py"
echo "  real_data_loader.py"
echo "  hubble_dipole.py"
echo "  hubble_dipole_real.py"
echo "  visualize.py"
echo "  visualize_real.py"
echo "  mcmc_comparison.py"
echo "  main.py"
echo ""
echo "✓ Repository is now clean and organized!"
