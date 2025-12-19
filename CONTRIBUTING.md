# Contributing to Geometric Resolution of the Hubble Tension

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/davidbesemer/lcdm-mcmc/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Your environment (Python version, OS, etc.)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes**: Run `./test_all.sh`
5. **Commit with clear messages**: `git commit -m "Add: feature description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

### Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Add comments for complex logic

### Testing

Before submitting a PR:

```bash
# Run all tests
./test_all.sh

# Test individual modules
python3 besemer_core.py
python3 scanner.py
python3 data_loader.py
```

### Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Update PRINCIPLES.md for theoretical changes
- Update paper/ if scientific content changes

## Areas for Contribution

### High Priority

1. **Real Data Integration**: Replace simulated data with actual Planck/SH0ES data
2. **CAMB/CLASS Integration**: Use full Boltzmann codes for CMB calculations
3. **Higher Dimensions**: Extend to more cosmological parameters
4. **Performance**: Parallelize grid scanning

### Medium Priority

1. **Adaptive Scanning**: Implement automatic grid refinement
2. **Other Tensions**: Apply to S₈ tension, lensing anomaly
3. **Visualization**: Add interactive plots
4. **Documentation**: Expand tutorials and examples

### Low Priority

1. **Code Optimization**: Profile and optimize bottlenecks
2. **Additional Tests**: Increase test coverage
3. **CI/CD**: Enhance GitHub Actions workflows

## Scientific Contributions

### Theoretical Work

- Extensions to the binary switch framework
- Physical motivation for β and S parameters
- Connections to other areas of physics

### Empirical Work

- Application to real observational data
- Comparison with traditional MCMC results
- Validation studies

### Paper Contributions

If you contribute significantly to the scientific content:

1. Discuss authorship with David Besemer
2. Update paper/acknowledgments.tex
3. Follow RevTeX 4-2 formatting

## Review Process

1. All PRs require review before merging
2. Automated tests must pass
3. Code must follow style guidelines
4. Documentation must be updated

## Questions?

Contact: besemer@independent-research.org

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or identity.

### Our Standards

- Be respectful and considerate
- Welcome diverse perspectives
- Focus on constructive feedback
- Acknowledge contributions

### Enforcement

Unacceptable behavior will not be tolerated. Report issues to besemer@independent-research.org.

---

Thank you for contributing to advancing our understanding of cosmology!
