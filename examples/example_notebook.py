"""
Beispiel-Notebook (als Python-Skript)

Interaktive Exploration der Besemer-Switch-Logik.
Kann in Jupyter konvertiert werden mit: jupytext --to notebook example_notebook.py
"""

# %% [markdown]
# # Besemer-MCMC: Interaktive Exploration
# 
# Dieses Notebook demonstriert die Besemer-Switch-Logik Schritt für Schritt.

# %% [markdown]
# ## 1. Setup

# %%
import numpy as np
import matplotlib.pyplot as plt
from besemer_core import BesemerSwitch, compute_residual_norm
from data_loader import PlanckCMBData, SupernovaData
from scanner import LatencyFreeScanner
from hubble_dipole import HubbleDipoleAnalyzer

# %% [markdown]
# ## 2. Der Besemer-Switch
# 
# Kernprinzip: **Keine Wahrscheinlichkeit, nur Zustand**
# 
# $$P(\theta) = \Theta\left(\beta \cdot |\text{Daten} - \text{Modell}(\theta)|^{-1} - \text{Schwelle}\right)$$

# %%
# Erstelle Switch
switch = BesemerSwitch(beta=296, threshold=1.0)

# Teste verschiedene Residuen
residuals = np.logspace(-3, 2, 1000)  # 0.001 bis 100
switch_values = np.array([switch(r) for r in residuals])
resonance_values = np.array([switch.resonance_strength(r) for r in residuals])

# Plotte
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Resonanzstärke (kontinuierlich)
ax1 = axes[0]
ax1.plot(residuals, resonance_values, 'b-', linewidth=2)
ax1.axhline(1.0, color='red', linestyle='--', label='Schwelle')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Residuum |Daten - Modell|', fontsize=12)
ax1.set_ylabel('Resonanzstärke β/r', fontsize=12)
ax1.set_title('Kontinuierliche Resonanz', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Plot 2: Binärer Switch
ax2 = axes[1]
ax2.plot(residuals, switch_values, 'r-', linewidth=2)
ax2.set_xscale('log')
ax2.set_xlabel('Residuum |Daten - Modell|', fontsize=12)
ax2.set_ylabel('Switch (0 oder 1)', fontsize=12)
ax2.set_title('Binärer Switch', fontsize=14, fontweight='bold')
ax2.set_ylim([-0.1, 1.1])
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Switch aktiviert bei Residuum < {296/1.0:.2f}")

# %% [markdown]
# ## 3. 1D-Scan: Finde den Parameter
# 
# Einfaches Beispiel: Finde $x$ für $f(x) = x^2 = 4$

# %%
# Definiere Modell
def model_func(x):
    return np.array([x**2])

# "Beobachtung"
data = np.array([4.0])

# Scanner
scanner = LatencyFreeScanner(
    model_func=model_func,
    data=data,
    beta=296,
    threshold=1.0
)

# Scanne
params, switches, resonances = scanner.scan_1d(param_range=(0, 5), n_points=1000)

# Plotte
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Resonanzstärke
ax1 = axes[0]
ax1.plot(params, resonances, 'b-', linewidth=2)
ax1.axhline(1.0, color='red', linestyle='--', label='Schwelle')
ax1.set_xlabel('Parameter x', fontsize=12)
ax1.set_ylabel('Resonanzstärke', fontsize=12)
ax1.set_title('Kontinuierliche Resonanz', fontsize=14, fontweight='bold')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Plot 2: Switch
ax2 = axes[1]
ax2.plot(params, switches, 'r-', linewidth=2)
ax2.axvline(2.0, color='green', linestyle='--', label='Erwarteter Wert (x=2)')
ax2.set_xlabel('Parameter x', fontsize=12)
ax2.set_ylabel('Switch (0 oder 1)', fontsize=12)
ax2.set_title('Binärer Switch', fontsize=14, fontweight='bold')
ax2.set_ylim([-0.1, 1.1])
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.show()

# Gefundene Werte
resonant_params = params[switches == 1]
if len(resonant_params) > 0:
    print(f"Gefundene Werte: {resonant_params}")
    print(f"Mittelwert: {np.mean(resonant_params):.4f}")
    print(f"Erwarteter Wert: 2.0")
else:
    print("Keine resonanten Punkte gefunden (β zu niedrig oder Schwelle zu hoch)")

# %% [markdown]
# ## 4. Kosmologische Daten laden

# %%
# Lade Planck CMB Daten
planck = PlanckCMBData(fiducial_H0=67.4, fiducial_Om0=0.315)
ell, C_ell, errors = planck.get_data()

# Lade Supernova Daten
supernova = SupernovaData(fiducial_H0=73.0, fiducial_Om0=0.3)
z, mu, mu_errors = supernova.get_data()

# Plotte
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: CMB Power Spectrum
ax1 = axes[0]
ax1.errorbar(ell, C_ell, yerr=errors, fmt='o', color='blue', alpha=0.6, label='Planck CMB')
ax1.set_xlabel('Multipol ℓ', fontsize=12)
ax1.set_ylabel('C_ℓ [μK²]', fontsize=12)
ax1.set_title('Planck CMB Power Spectrum', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Plot 2: Supernova Distance Modulus
ax2 = axes[1]
ax2.errorbar(z, mu, yerr=mu_errors, fmt='o', color='red', alpha=0.6, label='Supernova Ia')
ax2.set_xlabel('Rotverschiebung z', fontsize=12)
ax2.set_ylabel('Distance Modulus μ [mag]', fontsize=12)
ax2.set_title('Supernova Distance Modulus', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.show()

print(f"Planck: {len(ell)} Datenpunkte")
print(f"Supernova: {len(z)} Datenpunkte")

# %% [markdown]
# ## 5. Hubble-Dipol-Analyse
# 
# Teste, ob beide H0-Werte (67 und 73) den Switch auslösen.

# %%
# Initialisiere Analyzer
analyzer = HubbleDipoleAnalyzer(planck, supernova, beta=296)

# Teste Pole
pole_test = analyzer.test_pole_resonance()

# %% [markdown]
# ## 6. 2D-Scan: Parameterraum
# 
# Scanne H0 und Ωm gleichzeitig.

# %%
# Scanne Planck-Kontext (niedrigere Auflösung für schnellere Ausführung)
print("Scanne Planck-Kontext...")
grid_H0_p, grid_Om0_p, switches_p, resonances_p = analyzer.scan_planck_context(
    H0_range=(60, 80),
    Om0_range=(0.2, 0.4),
    n_points=(50, 50)  # Reduziert für Notebook
)

# Scanne Supernova-Kontext
print("\nScanne Supernova-Kontext...")
grid_H0_s, grid_Om0_s, switches_s, resonances_s = analyzer.scan_supernova_context(
    H0_range=(60, 80),
    Om0_range=(0.2, 0.4),
    n_points=(50, 50)
)

# %% [markdown]
# ## 7. Visualisierung

# %%
from visualize import plot_dipole_comparison

# Finde Dipol-Struktur
dipole = analyzer.find_dipole_structure(switches_p, switches_s, grid_H0_p, grid_Om0_p)

# Plotte
fig = plot_dipole_comparison(
    (grid_H0_p, grid_Om0_p, switches_p, resonances_p),
    (grid_H0_s, grid_Om0_s, switches_s, resonances_s),
    dipole
)
plt.show()

# Drucke Ergebnisse
print("\n=== ERGEBNISSE ===")
if dipole['planck_pole']:
    print(f"Planck-Pol: H0={dipole['planck_pole'][0]:.2f}, Ωm={dipole['planck_pole'][1]:.3f}")
if dipole['supernova_pole']:
    print(f"Supernova-Pol: H0={dipole['supernova_pole'][0]:.2f}, Ωm={dipole['supernova_pole'][1]:.3f}")
if dipole['dipole_distance']:
    print(f"Dipol-Distanz: {dipole['dipole_distance']:.3f}")
    print(f"Dipol-Winkel: {dipole['dipole_angle']:.1f}°")

# %% [markdown]
# ## 8. Interpretation
# 
# **Klassische Sicht**: H0 = 67 vs. H0 = 73 → "Hubble-Tension" (Widerspruch)
# 
# **Besemer-Sicht**: Zwei Pole eines Dipols → Geometrische Struktur
# 
# Die beiden Werte sind nicht widersprüchlich, sondern verschiedene Manifestationen
# derselben Realität in unterschiedlichen Kontexten (global vs. lokal).

# %%
