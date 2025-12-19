#!/usr/bin/env python3
"""
Besemer-MCMC: Hauptprogramm

Latenzfreie kosmologische Parameteranalyse mit binärer Switch-Logik.

Verwendung:
    python main.py --beta 296 --resolution 100 --output ./results
"""

import argparse
import os
import json
import numpy as np
from datetime import datetime

from data_loader import PlanckCMBData, SupernovaData
from hubble_dipole import HubbleDipoleAnalyzer, analyze_hubble_tension
from visualize import create_all_plots


def print_banner():
    """Druckt Banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              BESEMER-MCMC ANALYZER                        ║
    ║                                                           ║
    ║  Latenzfreie Kosmologische Parameteranalyse               ║
    ║  Prinzip: Keine Wahrscheinlichkeit, nur Resonanz         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def save_results(results, output_dir):
    """
    Speichert Analyse-Ergebnisse als JSON.
    
    Args:
        results: dict mit Ergebnissen
        output_dir: Ausgabeverzeichnis
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Konvertiere numpy arrays zu Listen für JSON
    def convert_to_serializable(obj):
        """Konvertiert numpy arrays zu Listen."""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        else:
            return obj
    
    results_serializable = {
        'timestamp': datetime.now().isoformat(),
        'pole_test': convert_to_serializable(results['pole_test']),
        'dipole': convert_to_serializable(results['dipole'])
    }
    
    output_file = os.path.join(output_dir, 'results.json')
    with open(output_file, 'w') as f:
        json.dump(results_serializable, f, indent=2)
    
    print(f"\nErgebnisse gespeichert: {output_file}")


def print_summary(results):
    """
    Druckt Zusammenfassung der Ergebnisse.
    """
    print("\n" + "="*60)
    print("ZUSAMMENFASSUNG")
    print("="*60)
    
    pole_test = results['pole_test']
    dipole = results['dipole']
    
    print("\n### Pol-Resonanz-Test ###")
    print(f"Planck (H0={pole_test['planck']['H0']}):")
    print(f"  Switch: {pole_test['planck']['switch']}")
    print(f"  Residual: {pole_test['planck']['residual']:.4f}")
    
    print(f"\nSupernova (H0={pole_test['supernova']['H0']}):")
    print(f"  Switch: {pole_test['supernova']['switch']}")
    print(f"  Residual: {pole_test['supernova']['residual']:.4f}")
    
    print("\n### Dipol-Struktur ###")
    if dipole['planck_pole']:
        print(f"Planck-Pol: H0={dipole['planck_pole'][0]:.2f}, Ωm={dipole['planck_pole'][1]:.3f}")
    else:
        print("Planck-Pol: Nicht gefunden")
    
    if dipole['supernova_pole']:
        print(f"Supernova-Pol: H0={dipole['supernova_pole'][0]:.2f}, Ωm={dipole['supernova_pole'][1]:.3f}")
    else:
        print("Supernova-Pol: Nicht gefunden")
    
    if dipole['dipole_distance']:
        print(f"\nDipol-Eigenschaften:")
        print(f"  Distanz: {dipole['dipole_distance']:.3f}")
        print(f"  Winkel: {dipole['dipole_angle']:.1f}°")
        print(f"  Überlappung: {dipole['overlap']} Punkte")
    
    print("\n" + "="*60)
    
    # Interpretation
    print("\n### INTERPRETATION ###")
    
    if pole_test['planck']['switch'] == 1 and pole_test['supernova']['switch'] == 1:
        print("✓ Beide H0-Werte lösen den Switch in ihrem Kontext aus.")
        print("  → Bestätigt: Keine Spannung, sondern Dipol-Struktur!")
    elif pole_test['planck']['switch'] == 1:
        print("✓ Planck-Pol ist resonant.")
        print("✗ Supernova-Pol ist nicht resonant (β zu niedrig oder Schwelle zu hoch).")
    elif pole_test['supernova']['switch'] == 1:
        print("✗ Planck-Pol ist nicht resonant (β zu niedrig oder Schwelle zu hoch).")
        print("✓ Supernova-Pol ist resonant.")
    else:
        print("✗ Beide Pole sind nicht resonant.")
        print("  → Erhöhe β oder senke die Schwelle.")
    
    if dipole['dipole_distance'] and dipole['dipole_distance'] > 0:
        print(f"\n✓ Dipol-Distanz: {dipole['dipole_distance']:.3f}")
        print("  → Die beiden Pole sind geometrisch getrennt, aber strukturell verbunden.")
    
    print("\n" + "="*60)


def main():
    """Hauptfunktion."""
    parser = argparse.ArgumentParser(
        description='Besemer-MCMC: Latenzfreie kosmologische Parameteranalyse'
    )
    parser.add_argument('--beta', type=float, default=296,
                       help='Verstärker (default: 296)')
    parser.add_argument('--threshold', type=float, default=1.0,
                       help='Switch-Schwelle (default: 1.0)')
    parser.add_argument('--resolution', type=int, default=100,
                       help='Gitterauflösung (NxN Punkte, default: 100)')
    parser.add_argument('--h0-min', type=float, default=60,
                       help='Minimaler H0-Wert (default: 60)')
    parser.add_argument('--h0-max', type=float, default=80,
                       help='Maximaler H0-Wert (default: 80)')
    parser.add_argument('--om-min', type=float, default=0.2,
                       help='Minimaler Ωm-Wert (default: 0.2)')
    parser.add_argument('--om-max', type=float, default=0.4,
                       help='Maximaler Ωm-Wert (default: 0.4)')
    parser.add_argument('--output', type=str, default='./results',
                       help='Ausgabeverzeichnis (default: ./results)')
    parser.add_argument('--no-plots', action='store_true',
                       help='Keine Plots erstellen')
    
    args = parser.parse_args()
    
    # Banner
    print_banner()
    
    # Parameter
    print("PARAMETER:")
    print(f"  β (Verstärker): {args.beta}")
    print(f"  Schwelle: {args.threshold}")
    print(f"  Auflösung: {args.resolution}x{args.resolution}")
    print(f"  H0-Bereich: [{args.h0_min}, {args.h0_max}]")
    print(f"  Ωm-Bereich: [{args.om_min}, {args.om_max}]")
    print(f"  Ausgabe: {args.output}")
    print()
    
    # Analyse durchführen
    print("Starte Analyse...\n")
    results = analyze_hubble_tension(
        beta=args.beta,
        n_points=(args.resolution, args.resolution)
    )
    
    # Zusammenfassung
    print_summary(results)
    
    # Ergebnisse speichern
    save_results(results, args.output)
    
    # Plots erstellen
    if not args.no_plots:
        print("\nErstelle Visualisierungen...")
        plot_dir = os.path.join(args.output, 'plots')
        create_all_plots(results, output_dir=plot_dir)
        print(f"Plots gespeichert in: {plot_dir}/")
    
    print("\n✓ Analyse abgeschlossen!")
    print(f"\nErgebnisse: {args.output}/")


if __name__ == "__main__":
    main()
