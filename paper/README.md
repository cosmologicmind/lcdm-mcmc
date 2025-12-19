# Resolving the Hubble Tension through Binary Switch Logic

**Author**: David A. Besemer  
**Affiliation**: Independent Researcher  
**Format**: RevTeX 4-2 (Physical Review D style)

## Abstract

This paper presents a novel approach to cosmological parameter analysis that replaces traditional probabilistic likelihood functions with binary switch logic. We demonstrate that the Hubble tension—the discrepancy between local and early-universe measurements of H₀—can be reinterpreted as a dipole structure in cosmological parameter space, where both values are valid in their respective contexts.

## Files

- `main.tex` - Main LaTeX document (includes all sections)
- `abstract.tex` - Abstract
- `introduction.tex` - Introduction and motivation
- `theory.tex` - Theoretical framework (binary switch function)
- `methodology.tex` - Methods and data analysis
- `results.tex` - Results with figures
- `discussion.tex` - Discussion and implications
- `conclusions.tex` - Conclusions and future work
- `acknowledgments.tex` - Acknowledgments
- `references.bib` - BibTeX bibliography

## Compilation

### Requirements

- LaTeX distribution (TeX Live, MiKTeX, etc.)
- RevTeX 4-2 package
- Standard LaTeX packages: graphicx, amsmath, amssymb, hyperref

### Compile

```bash
# Standard compilation
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Or use the Makefile
make
```

### Clean

```bash
make clean
```

## Figures

All figures are located in `../results/plots/`:

1. `planck_switch_map.png` - Planck CMB context switch map
2. `supernova_switch_map.png` - Supernova context switch map
3. `dipole_comparison.png` - Three-panel dipole comparison
4. `manifold_geometry_planck.png` - Planck manifold geometry
5. `manifold_geometry_supernova.png` - Supernova manifold geometry
6. `classical_vs_besemer.png` - Comparison with classical methods

All figures are 300 DPI PNG format, suitable for publication.

## Key Contributions

1. **Binary Switch Framework**: Mathematical formulation replacing soft likelihoods
2. **Latency-Free Scanning**: Grid-based approach eliminating MCMC burn-in
3. **Dipole Interpretation**: Both H₀ values are valid in their contexts
4. **Geometric Perspective**: Parameter constraints as manifolds, not clouds

## Citation

If you use this work, please cite:

```bibtex
@article{Besemer2025,
  title={Resolving the Hubble Tension through Binary Switch Logic: A Latency-Free Approach to Cosmological Parameter Analysis},
  author={Besemer, David A.},
  journal={arXiv preprint},
  year={2025},
  note={In preparation}
}
```

## License

This work is released under CC BY 4.0 (Creative Commons Attribution 4.0 International).

## Contact

For questions or comments, please contact: besemer@independent-research.org

---

**Status**: Draft manuscript (December 2025)
