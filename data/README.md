# Data Directory

This directory contains real cosmological data used for analysis.

## Files (Download Required)

### Pantheon+ Supernova Data
- **File**: `pantheon_plus.dat` (568 KB)
- **Source**: https://github.com/PantheonPlusSH0ES/DataRelease
- **Description**: 1701 Type Ia supernovae distance moduli
- **Citation**: Scolnic et al. (2022), ApJ, 938, 113

### Planck CMB Data
- **File**: `planck_tt_spectrum.txt` (empty placeholder)
- **Source**: Planck 2018 best-fit parameters used in code
- **Description**: CMB TT power spectrum (simplified model)

## How to Download

### Option 1: Automatic (Recommended)
```bash
cd data/
wget https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat -O pantheon_plus.dat
```

### Option 2: Manual
1. Visit: https://github.com/PantheonPlusSH0ES/DataRelease
2. Download `Pantheon+SH0ES.dat`
3. Save as `data/pantheon_plus.dat`

## Data Format

### pantheon_plus.dat
Columns (space-separated):
- CID: Supernova ID (string)
- IDSURVEY: Survey ID (int)
- zHD: Heliocentric redshift (float)
- ... (additional columns)
- MU_SH0ES: Distance modulus (float)
- MU_SH0ES_ERR_DIAG: Uncertainty (float)

Total: 1701 supernovae, redshift range 0.001 to 2.26

## Usage

The data is automatically loaded by `real_data_loader.py`:

```python
from real_data_loader import PantheonPlusSupernovaData

# Load data
pantheon = PantheonPlusSupernovaData()

# Access
print(f"Loaded {len(pantheon.z)} supernovae")
print(f"Redshift range: {pantheon.z.min():.4f} to {pantheon.z.max():.4f}")
```

## License

Pantheon+ data is publicly available under the terms specified by the Pantheon+ collaboration.

## Citation

If you use this data, please cite:

```bibtex
@article{Scolnic2022,
    author = {Scolnic, D. and others},
    title = {The Pantheon+ Analysis: The Full Data Set and Light-curve Release},
    journal = {ApJ},
    volume = {938},
    pages = {113},
    year = {2022}
}
```
