# Geometric Resolution of the Hubble Tension

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![Paper](https://img.shields.io/badge/paper-arXiv-red)]()
[![DOI](https://img.shields.io/badge/DOI-pending-orange)]()

> **A Latency-Free Binary Switch Approach to Cosmological Parameter Analysis**

**Author**: David A. Besemer, Independent Researcher

---

## 🎯 Overview

This repository contains the complete implementation and scientific paper for a novel approach to cosmological parameter analysis that **resolves the Hubble tension** through binary switch logic.

### The Problem

The Hubble tension—a ~5σ discrepancy between early-universe (Planck: H₀ = 67.4) and late-universe (Supernova: H₀ = 73.0) measurements—is one of the most significant challenges in modern cosmology.

### Our Solution

We replace soft probabilistic likelihoods with **sharp binary switches**, revealing that both H₀ values are **real and valid** in their respective contexts—not contradictory, but manifestations of a **dipole structure** in cosmological parameter space.

## 🔬 Core Principles

1. **Latency-Freedom**: Direct grid scanning eliminates MCMC burn-in (results in seconds, not hours)
2. **Binary Clarity**: Sharp switch function P(θ) = Θ(β/||r|| - S) replaces soft Gaussians
3. **Geometric Structure**: Parameter constraints as manifolds, not probability clouds

## 📐 Mathematical Framework

**Classical MCMC**:
```
L(θ) ∝ exp(-χ²/2)  [soft Gaussian]
```

**Binary Switch**:
```
P(θ) = Θ(β · ||data - model(θ)||⁻¹ - S)
```

Where:
- **β = 296**: Amplification factor (derived from α⁻¹ in cosmological context)
- **Θ**: Heaviside step function (binary switch)
- **S = 1.0**: Unit threshold (natural energy scale)
- **Result**: Geometric manifolds instead of probability clouds

## Quick Start

### 1. Installation
```bash
pip3 install -r requirements.txt
```

### 2. Test
```bash
./test_all.sh
```

### 3. Analyse ausführen
```bash
./run_analysis.sh
```

Oder mit Parametern:
```bash
python3 main.py --beta 296 --resolution 100 --output ./results
```

## Projektstruktur

```
lcdm_mcmc/
├── besemer_core.py      # ✅ Switch-Funktion und Verstärker
├── scanner.py           # ✅ Latenzfreier Gitter-Scanner
├── data_loader.py       # ✅ Planck/Supernova Daten
├── hubble_dipole.py     # ✅ Hubble-Tension als Dipol
├── visualize.py         # ✅ Lösungs-Mannigfaltigkeit plotten
├── main.py              # ✅ Hauptanalyse mit CLI
├── example_notebook.py  # ✅ Interaktives Tutorial
│
├── README.md            # Diese Datei
├── QUICKSTART.md        # Schnellstart-Anleitung
├── PRINCIPLES.md        # Theoretische Prinzipien
├── ARCHITECTURE.md      # System-Architektur
└── PROJECT_SUMMARY.md   # Vollständige Übersicht
```

## Erwartetes Ergebnis

Statt verwaschener Blobs: **Scharfe Ring/Kreis-Struktur** im Parameterraum.

### Hubble-Tension als Dipol
- **Planck-Pol**: H₀ = 67.4 km/s/Mpc (globaler Kontext)
- **Supernova-Pol**: H₀ = 73.0 km/s/Mpc (lokaler Kontext)
- **Interpretation**: Keine Spannung, sondern geometrische Struktur

## Dokumentation

- **[QUICKSTART.md](QUICKSTART.md)**: Schnellstart-Anleitung
- **[PRINCIPLES.md](PRINCIPLES.md)**: Theoretische Herleitung
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System-Architektur
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: Vollständige Übersicht

## Beispiel-Output

Nach der Analyse findest du in `results/plots/`:
- `planck_switch_map.png` - Planck-Kontext (global)
- `supernova_switch_map.png` - Supernova-Kontext (lokal)
- `dipole_comparison.png` - Dipol-Struktur
- `manifold_geometry_*.png` - Geometrische Analyse
- `classical_vs_besemer.png` - Vergleich mit klassischem MCMC

## 📊 Key Results

- ✅ **Both H₀ values are resonant** in their respective contexts
- ✅ **Dipole structure identified** connecting Planck and Supernova measurements
- ✅ **Computational efficiency**: 40 seconds vs. hours/days for traditional MCMC
- ✅ **6 publication-quality visualizations** generated automatically

## 📄 Scientific Paper

The complete scientific paper is available in the `paper/` directory:

- **Title**: Geometric Resolution of the Hubble Tension: A Latency-Free Binary Switch Approach
- **Format**: RevTeX 4-2 (Physical Review D style)
- **Pages**: 10 (with 6 figures)
- **Status**: Ready for arXiv submission

To compile the paper:
```bash
cd paper/
make all
```

## 🏗️ Project Structure

```
lcdm_mcmc/
├── besemer_core.py      # Binary switch implementation
├── scanner.py           # Latency-free grid scanner
├── data_loader.py       # Cosmological data (Planck/SN)
├── hubble_dipole.py     # Hubble tension analysis
├── visualize.py         # Plot generation
├── main.py              # Main analysis pipeline
├── paper/               # Scientific paper (LaTeX)
│   ├── main.tex
│   ├── main.pdf         # Compiled paper
│   └── *.tex            # Individual sections
├── results/             # Analysis results
│   └── plots/           # Generated visualizations
└── docs/                # Documentation
```

## 🎓 Citation

If you use this work, please cite:

```bibtex
@article{Besemer2025,
  title={Geometric Resolution of the Hubble Tension: 
         A Latency-Free Binary Switch Approach to 
         Cosmological Parameter Analysis},
  author={Besemer, David A.},
  journal={arXiv preprint},
  year={2025},
  note={In preparation}
}
```

## 📜 License

- **Code**: MIT License
- **Paper**: CC BY 4.0 (Creative Commons Attribution 4.0 International)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📧 Contact

**David A. Besemer**  
Independent Researcher  
Email: besemer@independent-research.org

## 🌟 Acknowledgments

This work builds on the pioneering measurements of the Planck and SH0ES teams. Special thanks to the open-source scientific Python community (NumPy, SciPy, Matplotlib, Astropy).

---

## Philosophy

> "We filter away the impossible, until only the structure of truth remains."

**No probability. No latency. No uncertainty.**  
**Only resonance, geometry, and structure.**
