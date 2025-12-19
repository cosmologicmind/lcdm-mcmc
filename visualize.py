"""
Visualisierung der Lösungs-Mannigfaltigkeit

Zeigt die scharfe geometrische Struktur im Parameterraum.
Vergleich: Besemer (scharf) vs. Standard-MCMC (verwaschen)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as mpatches


def plot_switch_map_2d(grid_H0, grid_Om0, switches, resonances=None, 
                       title="Besemer-Switch Map", 
                       save_path=None):
    """
    Plottet 2D Switch-Map im H0-Ωm Parameterraum.
    
    Args:
        grid_H0, grid_Om0: Meshgrid der Parameter
        switches: Binäre Switch-Werte (0 oder 1)
        resonances: Kontinuierliche Resonanzstärke (optional)
        title: Plot-Titel
        save_path: Pfad zum Speichern (optional)
    """
    fig, axes = plt.subplots(1, 2 if resonances is not None else 1, 
                             figsize=(14, 6) if resonances is not None else (8, 6))
    
    if resonances is None:
        axes = [axes]
    
    # Plot 1: Binäre Switch-Map
    ax1 = axes[0]
    im1 = ax1.contourf(grid_H0, grid_Om0, switches, levels=[0, 0.5, 1], 
                       colors=['black', 'red'], alpha=0.8)
    ax1.contour(grid_H0, grid_Om0, switches, levels=[0.5], colors='red', linewidths=2)
    ax1.set_xlabel('H₀ [km/s/Mpc]', fontsize=12)
    ax1.set_ylabel('Ωₘ', fontsize=12)
    ax1.set_title(f'{title} (Binär)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Markiere bekannte Werte
    ax1.axvline(67.4, color='cyan', linestyle='--', alpha=0.5, label='Planck (67.4)')
    ax1.axvline(73.0, color='yellow', linestyle='--', alpha=0.5, label='Supernova (73.0)')
    ax1.legend(loc='upper right')
    
    # Plot 2: Kontinuierliche Resonanz (falls vorhanden)
    if resonances is not None:
        ax2 = axes[1]
        
        # Log-Skala für bessere Sichtbarkeit
        resonances_log = np.log10(resonances + 1)
        
        im2 = ax2.contourf(grid_H0, grid_Om0, resonances_log, levels=20, cmap='hot')
        ax2.contour(grid_H0, grid_Om0, switches, levels=[0.5], colors='cyan', linewidths=2)
        ax2.set_xlabel('H₀ [km/s/Mpc]', fontsize=12)
        ax2.set_ylabel('Ωₘ', fontsize=12)
        ax2.set_title(f'{title} (Resonanzstärke)', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.colorbar(im2, ax=ax2, label='log₁₀(Resonanz + 1)')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot gespeichert: {save_path}")
    
    return fig


def plot_dipole_comparison(planck_scan, supernova_scan, dipole_info, save_path=None):
    """
    Vergleicht Planck- und Supernova-Kontexte nebeneinander.
    
    Args:
        planck_scan: (grid_H0, grid_Om0, switches, resonances) für Planck
        supernova_scan: (grid_H0, grid_Om0, switches, resonances) für Supernova
        dipole_info: dict mit Dipol-Eigenschaften
        save_path: Pfad zum Speichern (optional)
    """
    grid_H0_p, grid_Om0_p, switches_p, resonances_p = planck_scan
    grid_H0_s, grid_Om0_s, switches_s, resonances_s = supernova_scan
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot 1: Planck-Kontext
    ax1 = axes[0]
    ax1.contourf(grid_H0_p, grid_Om0_p, switches_p, levels=[0, 0.5, 1], 
                 colors=['black', 'blue'], alpha=0.7)
    ax1.contour(grid_H0_p, grid_Om0_p, switches_p, levels=[0.5], colors='cyan', linewidths=2)
    ax1.axvline(67.4, color='cyan', linestyle='--', linewidth=2, label='H₀ = 67.4')
    ax1.set_xlabel('H₀ [km/s/Mpc]', fontsize=12)
    ax1.set_ylabel('Ωₘ', fontsize=12)
    ax1.set_title('Planck-Kontext (Global)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Supernova-Kontext
    ax2 = axes[1]
    ax2.contourf(grid_H0_s, grid_Om0_s, switches_s, levels=[0, 0.5, 1], 
                 colors=['black', 'red'], alpha=0.7)
    ax2.contour(grid_H0_s, grid_Om0_s, switches_s, levels=[0.5], colors='orange', linewidths=2)
    ax2.axvline(73.0, color='yellow', linestyle='--', linewidth=2, label='H₀ = 73.0')
    ax2.set_xlabel('H₀ [km/s/Mpc]', fontsize=12)
    ax2.set_ylabel('Ωₘ', fontsize=12)
    ax2.set_title('Supernova-Kontext (Lokal)', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Überlagerung (Dipol)
    ax3 = axes[2]
    
    # Planck (blau) und Supernova (rot)
    combined = np.zeros_like(switches_p)
    combined[switches_p == 1] = 1  # Planck: blau
    combined[switches_s == 1] += 2  # Supernova: rot
    # Überlappung: 3 (blau + rot = magenta)
    
    colors = ['black', 'blue', 'red', 'magenta']
    levels = [0, 0.5, 1.5, 2.5, 3.5]
    ax3.contourf(grid_H0_p, grid_Om0_p, combined, levels=levels, colors=colors, alpha=0.7)
    
    # Markiere Pole
    if dipole_info['planck_pole']:
        ax3.plot(dipole_info['planck_pole'][0], dipole_info['planck_pole'][1], 
                'o', color='cyan', markersize=12, label='Planck-Pol')
    if dipole_info['supernova_pole']:
        ax3.plot(dipole_info['supernova_pole'][0], dipole_info['supernova_pole'][1], 
                'o', color='yellow', markersize=12, label='Supernova-Pol')
    
    # Verbindungslinie (Dipol-Achse)
    if dipole_info['planck_pole'] and dipole_info['supernova_pole']:
        p1 = dipole_info['planck_pole']
        p2 = dipole_info['supernova_pole']
        ax3.plot([p1[0], p2[0]], [p1[1], p2[1]], 'w--', linewidth=2, alpha=0.8)
    
    ax3.set_xlabel('H₀ [km/s/Mpc]', fontsize=12)
    ax3.set_ylabel('Ωₘ', fontsize=12)
    ax3.set_title('Dipol-Struktur', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Legende für Farben
    blue_patch = mpatches.Patch(color='blue', label='Nur Planck')
    red_patch = mpatches.Patch(color='red', label='Nur Supernova')
    magenta_patch = mpatches.Patch(color='magenta', label='Überlappung')
    ax3.legend(handles=[blue_patch, red_patch, magenta_patch], loc='upper right')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Dipol-Plot gespeichert: {save_path}")
    
    return fig


def plot_manifold_geometry(grid_H0, grid_Om0, switches, save_path=None):
    """
    Analysiert und plottet die Geometrie der Lösungs-Mannigfaltigkeit.
    
    Zeigt:
    - Ist es ein Punkt? (0D)
    - Eine Linie? (1D)
    - Ein Ring/Kreis? (1D geschlossen)
    - Eine Fläche? (2D)
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Extrahiere Mannigfaltigkeit
    mask = switches == 1
    H0_manifold = grid_H0[mask]
    Om0_manifold = grid_Om0[mask]
    
    # Hintergrund: Alle Punkte
    ax.scatter(grid_H0.flatten(), grid_Om0.flatten(), 
               c='black', s=1, alpha=0.1, label='Dissonanz (0)')
    
    # Mannigfaltigkeit: Resonante Punkte
    if len(H0_manifold) > 0:
        ax.scatter(H0_manifold, Om0_manifold, 
                   c='red', s=50, alpha=0.8, edgecolors='white', linewidths=1,
                   label=f'Resonanz (1) - {len(H0_manifold)} Punkte')
        
        # Versuche Kreis zu fitten (falls Ring-Struktur)
        if len(H0_manifold) > 3:
            center_H0 = np.mean(H0_manifold)
            center_Om0 = np.mean(Om0_manifold)
            radius = np.mean(np.sqrt((H0_manifold - center_H0)**2 + (Om0_manifold - center_Om0)**2))
            
            circle = Circle((center_H0, center_Om0), radius, 
                           fill=False, color='yellow', linewidth=2, linestyle='--',
                           label=f'Gefitteter Kreis (R={radius:.3f})')
            ax.add_patch(circle)
            
            ax.plot(center_H0, center_Om0, 'x', color='yellow', markersize=15, 
                   markeredgewidth=3, label='Zentrum')
    
    ax.set_xlabel('H₀ [km/s/Mpc]', fontsize=14)
    ax.set_ylabel('Ωₘ', fontsize=14)
    ax.set_title('Geometrie der Lösungs-Mannigfaltigkeit', fontsize=16, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Geometrie-Plot gespeichert: {save_path}")
    
    return fig


def plot_comparison_classical_vs_besemer(grid_H0, grid_Om0, switches, save_path=None):
    """
    Vergleicht Besemer-Switch mit klassischer Likelihood-Verteilung.
    
    Zeigt den Unterschied zwischen:
    - Klassisch: Weiche Gaußkurve (verwaschen)
    - Besemer: Scharfer Switch (geometrisch)
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Simuliere klassische Likelihood (Gaußkurve)
    # Annahme: Zentrum bei (70, 0.3) mit Standardabweichung
    H0_center, Om0_center = 70.0, 0.3
    sigma_H0, sigma_Om0 = 3.0, 0.05
    
    classical_likelihood = np.exp(
        -((grid_H0 - H0_center)**2 / (2 * sigma_H0**2) + 
          (grid_Om0 - Om0_center)**2 / (2 * sigma_Om0**2))
    )
    
    # Plot 1: Klassische Likelihood (verwaschen)
    ax1 = axes[0]
    im1 = ax1.contourf(grid_H0, grid_Om0, classical_likelihood, levels=20, cmap='Blues')
    ax1.contour(grid_H0, grid_Om0, classical_likelihood, levels=10, colors='blue', alpha=0.3)
    ax1.set_xlabel('H₀ [km/s/Mpc]', fontsize=12)
    ax1.set_ylabel('Ωₘ', fontsize=12)
    ax1.set_title('Klassisch: Weiche Likelihood\n(Wahrscheinlichkeitswolke)', 
                  fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(im1, ax=ax1, label='Likelihood')
    
    # Plot 2: Besemer-Switch (scharf)
    ax2 = axes[1]
    ax2.contourf(grid_H0, grid_Om0, switches, levels=[0, 0.5, 1], 
                 colors=['black', 'red'], alpha=0.8)
    ax2.contour(grid_H0, grid_Om0, switches, levels=[0.5], colors='red', linewidths=3)
    ax2.set_xlabel('H₀ [km/s/Mpc]', fontsize=12)
    ax2.set_ylabel('Ωₘ', fontsize=12)
    ax2.set_title('Besemer: Scharfer Switch\n(Geometrische Struktur)', 
                  fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Vergleichs-Plot gespeichert: {save_path}")
    
    return fig


def create_all_plots(results, output_dir='./plots'):
    """
    Erstellt alle Visualisierungen aus den Analyse-Ergebnissen.
    
    Args:
        results: dict aus analyze_hubble_tension()
        output_dir: Verzeichnis für Plots
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    planck_scan = results['planck_scan']
    supernova_scan = results['supernova_scan']
    dipole = results['dipole']
    
    grid_H0_p, grid_Om0_p, switches_p, resonances_p = planck_scan
    grid_H0_s, grid_Om0_s, switches_s, resonances_s = supernova_scan
    
    print("\n=== Erstelle Visualisierungen ===")
    
    # Plot 1: Planck Switch-Map
    plot_switch_map_2d(grid_H0_p, grid_Om0_p, switches_p, resonances_p,
                       title="Planck-Kontext",
                       save_path=f"{output_dir}/planck_switch_map.png")
    
    # Plot 2: Supernova Switch-Map
    plot_switch_map_2d(grid_H0_s, grid_Om0_s, switches_s, resonances_s,
                       title="Supernova-Kontext",
                       save_path=f"{output_dir}/supernova_switch_map.png")
    
    # Plot 3: Dipol-Vergleich
    plot_dipole_comparison(planck_scan, supernova_scan, dipole,
                          save_path=f"{output_dir}/dipole_comparison.png")
    
    # Plot 4: Mannigfaltigkeits-Geometrie (Planck)
    plot_manifold_geometry(grid_H0_p, grid_Om0_p, switches_p,
                          save_path=f"{output_dir}/manifold_geometry_planck.png")
    
    # Plot 5: Mannigfaltigkeits-Geometrie (Supernova)
    plot_manifold_geometry(grid_H0_s, grid_Om0_s, switches_s,
                          save_path=f"{output_dir}/manifold_geometry_supernova.png")
    
    # Plot 6: Vergleich Klassisch vs. Besemer
    plot_comparison_classical_vs_besemer(grid_H0_p, grid_Om0_p, switches_p,
                                        save_path=f"{output_dir}/classical_vs_besemer.png")
    
    print(f"\nAlle Plots gespeichert in: {output_dir}/")


if __name__ == "__main__":
    print("Visualisierungs-Modul geladen.")
    print("Nutze create_all_plots(results) nach der Analyse.")
