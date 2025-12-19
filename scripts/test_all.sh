#!/bin/bash
# Umfassender Test aller Module

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         BESEMER-MCMC: Modul-Tests                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Zähler
PASSED=0
FAILED=0

# Test-Funktion
run_test() {
    local module=$1
    local description=$2
    
    echo -n "Testing $description... "
    
    if python3 "$module" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((FAILED++))
        echo "  Run 'python3 $module' for details"
    fi
}

# Prüfe Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 found: $(python3 --version)${NC}"
echo ""

# Prüfe Dependencies
echo "Checking dependencies..."
python3 -c "import numpy; import scipy; import matplotlib; import astropy" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ Installing dependencies...${NC}"
    pip3 install -q -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    else
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        exit 1
    fi
fi
echo ""

# Führe Tests durch
echo "Running module tests..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "besemer_core.py" "Besemer-Switch Core"
run_test "scanner.py" "Latency-Free Scanner"
run_test "data_loader.py" "Data Loader"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Zusammenfassung
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    TEST SUMMARY                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo -e "Total tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
else
    echo -e "Failed: $FAILED"
fi
echo ""

# Prüfe Projektstruktur
echo "Checking project structure..."
FILES=(
    "README.md"
    "QUICKSTART.md"
    "PRINCIPLES.md"
    "ARCHITECTURE.md"
    "PROJECT_SUMMARY.md"
    "requirements.txt"
    "besemer_core.py"
    "scanner.py"
    "data_loader.py"
    "hubble_dipole.py"
    "visualize.py"
    "main.py"
    "example_notebook.py"
    "run_analysis.sh"
)

MISSING=0
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ Missing: $file${NC}"
        ((MISSING++))
    fi
done

if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}✓ All files present (${#FILES[@]} files)${NC}"
else
    echo -e "${RED}✗ Missing $MISSING files${NC}"
fi
echo ""

# Finale Bewertung
if [ $FAILED -eq 0 ] && [ $MISSING -eq 0 ]; then
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║              ✓ ALL TESTS PASSED                           ║"
    echo "║                                                           ║"
    echo "║         Project is ready for use!                         ║"
    echo "║                                                           ║"
    echo "║    Run: ./run_analysis.sh                                 ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║              ✗ SOME TESTS FAILED                          ║"
    echo "║                                                           ║"
    echo "║         Please fix errors before use                      ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    exit 1
fi
