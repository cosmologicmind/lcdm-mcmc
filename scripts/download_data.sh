#!/bin/bash
# Download real cosmological data for analysis

echo "=========================================="
echo "DOWNLOADING REAL COSMOLOGICAL DATA"
echo "=========================================="

# Create data directory
mkdir -p data

# Download Pantheon+ Supernova Data
echo ""
echo "1. Downloading Pantheon+ Supernova Data..."
echo "   Source: PantheonPlusSH0ES/DataRelease"
echo "   Size: ~568 KB"
echo "   SNe: 1701"

if [ -f "data/pantheon_plus.dat" ]; then
    echo "   ✓ File already exists: data/pantheon_plus.dat"
    echo "   To re-download, delete the file first."
else
    wget -q --show-progress \
        "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat" \
        -O data/pantheon_plus.dat
    
    if [ $? -eq 0 ]; then
        echo "   ✓ Downloaded successfully!"
        
        # Verify
        lines=$(wc -l < data/pantheon_plus.dat)
        echo "   ✓ Verified: $lines lines"
    else
        echo "   ✗ Download failed!"
        echo "   Please download manually from:"
        echo "   https://github.com/PantheonPlusSH0ES/DataRelease"
        exit 1
    fi
fi

# Planck data (embedded in code, no download needed)
echo ""
echo "2. Planck CMB Data"
echo "   ✓ Using Planck 2018 best-fit parameters (embedded in code)"
echo "   ✓ No download required"

# Create placeholder
touch data/planck_tt_spectrum.txt

echo ""
echo "=========================================="
echo "DATA DOWNLOAD COMPLETE"
echo "=========================================="
echo ""
echo "Downloaded files:"
echo "  data/pantheon_plus.dat    (~568 KB, 1701 SNe)"
echo ""
echo "You can now run:"
echo "  python3 hubble_dipole_real.py"
echo "  python3 mcmc_comparison.py"
echo "  python3 scripts/regenerate_all_plots.py"
echo ""
echo "✓ Ready for analysis!"
