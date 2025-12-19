# Besemer-MCMC: Quick Start Guide

## Installation

```bash
cd /home/coding/Projekte/lcdm_mcmc
pip3 install -r requirements.txt
```

## Schnellstart

### Option 1: Automatisches Skript
```bash
./run_analysis.sh
```

### Option 2: Manuell mit Parametern
```bash
python3 main.py --beta 296 --resolution 100 --output ./results
```

### Option 3: Python-Skript
```python
from hubble_dipole import analyze_hubble_tension
from visualize import create_all_plots

# Führe Analyse durch
results = analyze_hubble_tension(beta=296, n_points=(100, 100))

# Erstelle Plots
create_all_plots(results, output_dir='./results/plots')
```

## Kommandozeilen-Optionen

```bash
python3 main.py [OPTIONS]

Optionen:
  --beta FLOAT          Verstärker (default: 296)
  --threshold FLOAT     Switch-Schwelle (default: 1.0)
  --resolution INT      Gitterauflösung NxN (default: 100)
  --h0-min FLOAT        Minimaler H0-Wert (default: 60)
  --h0-max FLOAT        Maximaler H0-Wert (default: 80)
  --om-min FLOAT        Minimaler Ωm-Wert (default: 0.2)
  --om-max FLOAT        Maximaler Ωm-Wert (default: 0.4)
  --output DIR          Ausgabeverzeichnis (default: ./results)
  --no-plots            Keine Plots erstellen
```

## Beispiele

### 1. Standard-Analyse
```bash
python3 main.py
```
Führt Analyse mit Standard-Parametern durch.

### 2. Hohe Auflösung
```bash
python3 main.py --resolution 200
```
Scannt 200x200 = 40.000 Punkte (dauert länger, aber präziser).

### 3. Angepasster Verstärker
```bash
python3 main.py --beta 500 --threshold 50
```
Höherer Verstärker, niedrigere Schwelle → mehr resonante Punkte.

### 4. Engerer Parameterbereich
```bash
python3 main.py --h0-min 65 --h0-max 75 --om-min 0.25 --om-max 0.35
```
Fokussiert auf bekannte Hubble-Werte.

## Ausgabe

Nach der Analyse findest du:

```
results/
├── results.json              # Numerische Ergebnisse
└── plots/
    ├── planck_switch_map.png           # Planck-Kontext
    ├── supernova_switch_map.png        # Supernova-Kontext
    ├── dipole_comparison.png           # Dipol-Vergleich
    ├── manifold_geometry_planck.png    # Geometrie (Planck)
    ├── manifold_geometry_supernova.png # Geometrie (Supernova)
    └── classical_vs_besemer.png        # Vergleich Klassisch/Besemer
```

## Interpretation der Plots

### Switch-Map (Binär)
- **Schwarz**: Dissonanz (Switch = 0) → Parameter unmöglich
- **Rot**: Resonanz (Switch = 1) → Parameter existieren
- **Scharfe Kante**: Übergang zwischen Existenz und Nicht-Existenz

### Resonanzstärke (Kontinuierlich)
- **Heiße Farben**: Hohe Resonanz (β/r >> Schwelle)
- **Kalte Farben**: Niedrige Resonanz (β/r ≈ Schwelle)
- **Schwarz**: Keine Resonanz (β/r < Schwelle)

### Dipol-Vergleich
- **Blau**: Nur Planck-Kontext resonant
- **Rot**: Nur Supernova-Kontext resonant
- **Magenta**: Beide Kontexte resonant (Überlappung)
- **Weiße Linie**: Dipol-Achse zwischen den Polen

### Geometrie
- **Rote Punkte**: Lösungs-Mannigfaltigkeit
- **Gelber Kreis**: Gefittete Ring-Struktur (falls vorhanden)
- **Gelbes X**: Zentrum der Mannigfaltigkeit

## Erwartete Ergebnisse

### Erfolgreiche Dipol-Identifikation
```
Planck-Pol: H0=67.4, Ωm=0.315
Supernova-Pol: H0=73.0, Ωm=0.300
Dipol-Distanz: ~6.0
Dipol-Winkel: ~15°
```

### Interpretation
- **Beide Pole resonant**: Bestätigt Dipol-Hypothese
- **Nur ein Pol resonant**: β zu niedrig oder Schwelle zu hoch
- **Keine Pole resonant**: Parameter-Bereiche anpassen

## Troubleshooting

### Problem: Keine resonanten Punkte
**Lösung**: Erhöhe β oder senke Schwelle
```bash
python3 main.py --beta 500 --threshold 50
```

### Problem: Zu viele resonante Punkte
**Lösung**: Senke β oder erhöhe Schwelle
```bash
python3 main.py --beta 200 --threshold 200
```

### Problem: Analyse dauert zu lange
**Lösung**: Reduziere Auflösung
```bash
python3 main.py --resolution 50
```

### Problem: Plots werden nicht erstellt
**Lösung**: Prüfe matplotlib Installation
```bash
pip3 install matplotlib
```

## Modul-Tests

Teste einzelne Module:

```bash
# Test Besemer-Switch
python3 besemer_core.py

# Test Scanner
python3 scanner.py

# Test Daten-Loader
python3 data_loader.py

# Test Hubble-Dipol-Analyse
python3 hubble_dipole.py
```

## Interaktive Exploration

Für interaktive Exploration nutze das Beispiel-Notebook:

```bash
# Konvertiere zu Jupyter Notebook (optional)
pip3 install jupytext
jupytext --to notebook example_notebook.py

# Oder führe direkt aus
python3 example_notebook.py
```

## Nächste Schritte

1. **Verstehe die Prinzipien**: Lies `PRINCIPLES.md`
2. **Führe Analyse durch**: `./run_analysis.sh`
3. **Inspiziere Plots**: `results/plots/`
4. **Passe Parameter an**: Experimentiere mit β und Schwelle
5. **Erweitere**: Füge eigene Datensätze hinzu

## Support

Bei Fragen oder Problemen:
1. Prüfe `PRINCIPLES.md` für theoretischen Hintergrund
2. Prüfe `README.md` für Projektübersicht
3. Inspiziere Quellcode (gut dokumentiert)

---

**Viel Erfolg bei der Entdeckung der Lösungs-Mannigfaltigkeit!**
