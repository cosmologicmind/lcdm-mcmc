# Results Directory

This directory contains analysis results and publication-quality plots.

**Note**: These files are **not tracked in git** (too large). They are regenerated locally.

## Directory Structure

```
results/
├── plots/              # Publication-quality figures (300 DPI)
│   ├── optimized_dipole_structure.png
│   ├── real_data_dipole_structure.png
│   ├── pantheon_manifold_geometry.png
│   ├── classical_vs_besemer_real_data.png
│   └── final_mcmc_vs_besemer_comparison.png
└── results.json        # Numerical results (optional)
```

## How to Generate

### Quick Method
```bash
# Generate all plots with real data
python3 scripts/regenerate_all_plots.py
```

### Individual Analysis
```bash
# Run full analysis with real Pantheon+ data
python3 hubble_dipole_real.py

# Generate plots
from visualize_real import create_all_real_data_plots
create_all_real_data_plots(results, './results/plots')
```

## Output Files

### 1. optimized_dipole_structure.png
**THE MONEY SHOT** - Sharp dipole structure with optimized thresholds
- Pantheon+ context (red, 15% resonant)
- Planck context (cyan, 15% resonant)
- Dipole axis with separation annotation
- Resolution: 100×100 grid (10,000 points)

### 2. real_data_dipole_structure.png
Three-panel comparison:
- Left: Pantheon+ (1701 SNe)
- Center: Planck (CMB)
- Right: Dipole overlay

### 3. pantheon_manifold_geometry.png
Detailed manifold structure:
- Binary switch map
- Resonance strength contours
- 1781 resonant points highlighted

### 4. classical_vs_besemer_real_data.png
Side-by-side comparison:
- Left: Classical MCMC (soft probability cloud)
- Right: Besemer switch (sharp geometric manifold)

### 5. final_mcmc_vs_besemer_comparison.png
Head-to-head performance comparison:
- MCMC: 52.7s, soft cloud
- Besemer: 2.8s, sharp manifold
- 19× speedup demonstrated

## File Sizes

Typical sizes (may vary):
- Each PNG: ~500 KB - 2 MB (300 DPI)
- Total plots directory: ~3-4 MB
- results.json: ~4 KB

## Why Not in Git?

These files are **regenerated** from the analysis code and are:
1. **Large** (~3-4 MB total)
2. **Binary** (PNG images, not text-diffable)
3. **Reproducible** (anyone can regenerate them)
4. **Version-independent** (change with every analysis run)

## For Reviewers/Users

If you want to see the plots without running the analysis:
1. Check the paper: `paper/main.pdf` (includes embedded figures)
2. Or run: `python3 scripts/regenerate_all_plots.py` (~2 minutes)

## Requirements

To generate plots, you need:
- Python 3.8+
- matplotlib, numpy, scipy
- Real data in `data/` directory (see `data/README.md`)

## License

Generated plots are part of the research output and follow the project license (MIT).
