# Besemer-MCMC: Architektur

## System-Übersicht

```
┌─────────────────────────────────────────────────────────────┐
│                      BESEMER-MCMC                           │
│         Latenzfreie Kosmologische Parameteranalyse          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │         main.py                     │
        │  (Hauptprogramm & CLI)              │
        └─────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ data_loader.py│    │hubble_dipole  │    │ visualize.py  │
│               │    │     .py       │    │               │
│ - Planck CMB  │    │               │    │ - Switch Maps │
│ - Supernova   │───▶│ - Pol-Test    │───▶│ - Dipol Plots │
│ - BAO         │    │ - 2D-Scan     │    │ - Geometrie   │
└───────────────┘    │ - Dipol-Find  │    └───────────────┘
                     └───────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ scanner.py    │    │besemer_core.py│    │ Output        │
│               │    │               │    │               │
│ - 1D Scan     │───▶│ - Switch      │    │ - results.json│
│ - 2D Scan     │    │ - Resonance   │    │ - plots/*.png │
│ - Manifold    │    │ - Likelihood  │    │               │
└───────────────┘    └───────────────┘    └───────────────┘
```

## Modul-Hierarchie

### Ebene 1: Kern (Keine Dependencies)
```
besemer_core.py
├── BesemerSwitch          # Binäre Switch-Funktion
├── BesemerLikelihood      # Likelihood-Ersatz
├── compute_chi_squared    # χ² Berechnung
├── compute_residual_norm  # Residuum-Norm
└── heaviside              # Θ-Funktion
```

### Ebene 2: Scanner (Nutzt Kern)
```
scanner.py
├── LatencyFreeScanner     # Basis-Scanner
│   ├── scan_1d()          # 1D-Parameterraum
│   ├── scan_2d()          # 2D-Parameterraum
│   ├── find_manifold()    # Extrahiere Lösungen
│   └── analyze_geometry() # Geometrische Analyse
└── AdaptiveScanner        # Adaptive Verfeinerung (TODO)
```

### Ebene 3: Daten (Unabhängig)
```
data_loader.py
├── PlanckCMBData          # CMB Power Spectrum
├── SupernovaData          # Distance Modulus
├── BAOData                # Baryon Acoustic Oscillations
└── load_combined_dataset  # Kombinierte Daten
```

### Ebene 4: Analyse (Nutzt Scanner + Daten)
```
hubble_dipole.py
├── HubbleDipoleAnalyzer
│   ├── model_planck()           # CMB-Modell
│   ├── model_supernova()        # SN-Modell
│   ├── scan_planck_context()    # Globaler Kontext
│   ├── scan_supernova_context() # Lokaler Kontext
│   ├── find_dipole_structure()  # Dipol-Identifikation
│   └── test_pole_resonance()    # Pol-Test
└── analyze_hubble_tension()     # Haupt-Analyse-Funktion
```

### Ebene 5: Visualisierung (Nutzt Analyse-Ergebnisse)
```
visualize.py
├── plot_switch_map_2d()              # 2D Switch-Map
├── plot_dipole_comparison()          # Dipol-Vergleich
├── plot_manifold_geometry()          # Geometrie-Analyse
├── plot_comparison_classical_vs_besemer() # Vergleich
└── create_all_plots()                # Automatische Plot-Generierung
```

### Ebene 6: Interface (Nutzt alles)
```
main.py
├── print_banner()      # Banner
├── save_results()      # JSON-Export
├── print_summary()     # Zusammenfassung
└── main()              # CLI-Interface
```

## Datenfluss

### 1. Initialisierung
```
User Input (CLI)
    ↓
main.py (parse arguments)
    ↓
Parameter: β, Schwelle, Auflösung, Bereiche
```

### 2. Daten-Laden
```
data_loader.py
    ↓
PlanckCMBData(fiducial_H0, fiducial_Om0)
    ↓
Synthetische Daten: (ell, C_ell, errors)
    ↓
SupernovaData(fiducial_H0, fiducial_Om0)
    ↓
Synthetische Daten: (z, mu, errors)
```

### 3. Analyse-Pipeline
```
HubbleDipoleAnalyzer(planck_data, supernova_data, β)
    ↓
┌─────────────────────┬─────────────────────┐
│ Planck-Kontext      │ Supernova-Kontext   │
│                     │                     │
│ LatencyFreeScanner  │ LatencyFreeScanner  │
│     ↓               │     ↓               │
│ scan_2d()           │ scan_2d()           │
│     ↓               │     ↓               │
│ Für jeden Punkt:    │ Für jeden Punkt:    │
│   model_planck()    │   model_supernova() │
│   ↓                 │   ↓                 │
│   residual_norm     │   residual_norm     │
│   ↓                 │   ↓                 │
│   BesemerSwitch()   │   BesemerSwitch()   │
│   ↓                 │   ↓                 │
│   0 oder 1          │   0 oder 1          │
└─────────────────────┴─────────────────────┘
    ↓                       ↓
switches_planck       switches_supernova
    ↓                       ↓
    └───────────┬───────────┘
                ↓
    find_dipole_structure()
                ↓
    Dipol-Eigenschaften
```

### 4. Visualisierung
```
Analyse-Ergebnisse
    ↓
create_all_plots()
    ↓
┌─────────────────────────────────────┐
│ 1. planck_switch_map.png            │
│ 2. supernova_switch_map.png         │
│ 3. dipole_comparison.png            │
│ 4. manifold_geometry_planck.png     │
│ 5. manifold_geometry_supernova.png  │
│ 6. classical_vs_besemer.png         │
└─────────────────────────────────────┘
```

### 5. Output
```
results/
├── results.json    # Numerische Ergebnisse
└── plots/          # Visualisierungen
```

## Algorithmus-Fluss: 2D-Scan

```python
# Pseudo-Code für scan_2d()

def scan_2d(H0_range, Om0_range, n_points):
    # 1. Erstelle Gitter
    H0_grid = linspace(H0_range, n_points[0])
    Om0_grid = linspace(Om0_range, n_points[1])
    grid_H0, grid_Om0 = meshgrid(H0_grid, Om0_grid)
    
    # 2. Initialisiere Ergebnis-Arrays
    switches = zeros_like(grid_H0)
    resonances = zeros_like(grid_H0)
    
    # 3. Scanne jeden Punkt (LATENZFREI)
    for i in range(n_points[0]):
        for j in range(n_points[1]):
            # 3a. Berechne Modell für diese Parameter
            model = model_func(grid_H0[j,i], grid_Om0[j,i])
            
            # 3b. Berechne Residuum
            residual = ||data - model||
            
            # 3c. Wende Switch an (BINÄR)
            if β/residual >= threshold:
                switches[j,i] = 1  # RESONANZ
            else:
                switches[j,i] = 0  # DISSONANZ
            
            # 3d. Speichere Resonanzstärke (kontinuierlich)
            resonances[j,i] = β/residual
    
    # 4. Rückgabe
    return grid_H0, grid_Om0, switches, resonances
```

## Besemer-Switch: Kern-Algorithmus

```python
# Pseudo-Code für BesemerSwitch

class BesemerSwitch:
    def __init__(β, threshold):
        self.β = β
        self.threshold = threshold
    
    def __call__(residual):
        # 1. Verhindere Division durch 0
        residual_safe = max(residual, epsilon)
        
        # 2. Inverse Verstärkung
        #    Je kleiner der Fehler, desto größer der Wert
        amplified = β / residual_safe
        
        # 3. Binärer Switch (Heaviside-Funktion)
        if amplified >= threshold:
            return 1  # RESONANZ
        else:
            return 0  # DISSONANZ
```

## Vergleich: Klassisch vs. Besemer

### Klassisches MCMC
```
1. Initialisiere zufälligen Punkt
2. Schlage neuen Punkt vor (Random Walk)
3. Berechne Likelihood-Ratio
4. Akzeptiere/Verwerfe mit Wahrscheinlichkeit
5. Wiederhole 10.000+ mal (Einbrennphase)
6. Sammle Samples
7. Analysiere Verteilung

Ergebnis: Wahrscheinlichkeitswolke
Zeit: Stunden bis Tage
```

### Besemer-MCMC
```
1. Definiere Gitter im Parameterraum
2. Für jeden Punkt:
   a. Berechne Modell
   b. Berechne Residuum
   c. Wende Switch an
   d. Speichere 0 oder 1
3. Extrahiere Mannigfaltigkeit (alle Punkte mit Switch=1)
4. Analysiere Geometrie

Ergebnis: Geometrische Struktur
Zeit: Minuten
```

## Performance-Charakteristiken

### Komplexität
- **1D-Scan**: O(n) - linear in Anzahl Punkte
- **2D-Scan**: O(n²) - quadratisch
- **3D-Scan**: O(n³) - kubisch (nicht implementiert)

### Typische Laufzeiten (auf modernem PC)
- **50x50 Gitter**: ~10 Sekunden
- **100x100 Gitter**: ~40 Sekunden
- **200x200 Gitter**: ~3 Minuten

### Speicher
- **100x100 Gitter**: ~1 MB (2 Arrays: switches + resonances)
- **Plots**: ~5 MB (6 PNG-Dateien)

### Parallelisierung (TODO)
```python
# Zukünftige Erweiterung
from multiprocessing import Pool

def scan_2d_parallel(self, ...):
    with Pool() as pool:
        results = pool.map(evaluate_point, grid_points)
    # Speedup: ~4x auf 4-Core CPU
```

## Erweiterbarkeit

### Neue Datensätze hinzufügen
```python
# In data_loader.py
class NewDataset:
    def __init__(self, ...):
        # Lade Daten
        pass
    
    def get_data(self):
        return x, y, errors
```

### Neue Parameter scannen
```python
# In scanner.py
def scan_3d(self, param1_range, param2_range, param3_range):
    # Erweitere auf 3D
    pass
```

### Neue Visualisierungen
```python
# In visualize.py
def plot_new_analysis(results):
    # Erstelle neuen Plot
    pass
```

## Design-Prinzipien

1. **Modularität**: Jedes Modul ist unabhängig testbar
2. **Klarheit**: Keine versteckten Abhängigkeiten
3. **Dokumentation**: Jede Funktion ist dokumentiert
4. **Testbarkeit**: Jedes Modul hat `if __name__ == "__main__"` Tests
5. **Erweiterbarkeit**: Klassen-basiertes Design für Vererbung

## Abhängigkeiten

```
numpy
  ↓
scipy (optional, für zukünftige Erweiterungen)
  ↓
matplotlib (nur für visualize.py)
  ↓
astropy (nur für data_loader.py)
```

**Kern-Module** (besemer_core, scanner) haben **nur numpy** als Abhängigkeit.

---

## Zusammenfassung

Das Besemer-MCMC-System ist:
- **Modular**: Klare Trennung der Verantwortlichkeiten
- **Latenzfrei**: Keine Einbrennphase
- **Binär**: Klare 0/1-Entscheidungen
- **Geometrisch**: Findet Strukturen statt Wahrscheinlichkeiten
- **Erweiterbar**: Einfach neue Features hinzuzufügen
- **Dokumentiert**: Jeder Schritt ist erklärt

**Kernidee**: Filtere das Unmögliche weg, bis nur die Struktur übrig bleibt.
