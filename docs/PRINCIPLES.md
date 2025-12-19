# Besemer-Prinzipien für MCMC-Analyse

## Kern-Transformation

### Klassisches MCMC
```
Likelihood: L(θ) ∝ exp(-χ²/2)
Problem: Weiche Wahrscheinlichkeitsverteilung
Ergebnis: Verwaschene "Blobs" im Parameterraum
Methode: Random Walk mit Einbrennphase (Latenz)
```

### Besemer-MCMC
```
Switch: P(θ) = Θ(β · |Daten - Modell(θ)|⁻¹ - Schwelle)
Prinzip: Binäre Resonanzlogik
Ergebnis: Scharfe geometrische Struktur
Methode: Latenzfreier Gitter-Scan
```

## Die drei Säulen

### 1. Latenzfreiheit
**Klassisch**: MCMC braucht tausende Schritte zum "Einbrennen"
- Random Walk irrt umher
- Konvergenz unsicher
- Zeitverschwendung

**Besemer**: Jeder Punkt wird sofort evaluiert
- Kein Raten, nur Prüfen
- Keine Konvergenzprobleme
- Direktes Ergebnis

### 2. Binärer Switch
**Klassisch**: Wahrscheinlichkeit P(θ) ∈ [0, 1]
- "Vielleicht ist der Parameter hier"
- Unscharfe Grenzen
- Subjektive Interpretation

**Besemer**: Zustand S(θ) ∈ {0, 1}
- Resonanz (1) oder Dissonanz (0)
- Scharfe Kante
- Objektive Realität

### 3. Verstärker β = 296
**Funktion**: Hebt exakte Übereinstimmung über die Schwelle

```python
Residuum klein → β/r explodiert → Switch = 1
Residuum groß → β/r klein → Switch = 0
```

**Bedeutung**: 
- Keine "Näherung" akzeptiert
- Nur exakte Resonanz zählt
- Filtert das Unmögliche weg

## Mathematische Herleitung

### Ausgangspunkt: χ²
```
χ² = Σ [(Daten - Modell) / Fehler]²
```

### Klassische Likelihood
```
L(θ) = exp(-χ²/2)
```
Problem: Exponentialfunktion "verschmiert" alles

### Besemer-Transformation
Ersetze χ² durch inverse Norm:
```
r = ||Daten - Modell||
```

Verstärke:
```
A = β / r
```

Binärisiere:
```
P(θ) = Θ(A - Schwelle)
```

### Grenzwertbetrachtung
```
r → 0  ⟹  A → ∞  ⟹  P = 1  (Resonanz)
r → ∞  ⟹  A → 0  ⟹  P = 0  (Dissonanz)
```

## Hubble-Tension als Dipol

### Klassische Interpretation
```
Planck:    H₀ = 67.4 ± 0.5 km/s/Mpc  (global, früh)
Supernova: H₀ = 73.0 ± 1.0 km/s/Mpc  (lokal, spät)

Problem: 5σ Diskrepanz → "Tension"
```

### Besemer-Interpretation
```
Beide Werte sind real, aber in verschiedenen Kontexten.

Hypothese: Dipol-Struktur
- Planck-Pol:    H₀ = 67.4 (globaler Kontext)
- Supernova-Pol: H₀ = 73.0 (lokaler Kontext)
- Verbindung:    Geschlossene Kurve im Parameterraum
```

### Erwartetes Ergebnis
Statt zwei widersprüchlicher Werte:
→ Zwei Pole eines geometrischen Objekts
→ Beide lösen den Switch in ihrem Kontext aus
→ Keine Spannung, sondern Multipol-Struktur

## Praktische Anwendung

### 1. Daten laden
```python
from data_loader import PlanckCMBData, SupernovaData

planck = PlanckCMBData(fiducial_H0=67.4, fiducial_Om0=0.315)
supernova = SupernovaData(fiducial_H0=73.0, fiducial_Om0=0.3)
```

### 2. Switch definieren
```python
from besemer_core import BesemerSwitch

switch = BesemerSwitch(beta=296, threshold=1.0)
```

### 3. Parameterraum scannen
```python
from scanner import LatencyFreeScanner

scanner = LatencyFreeScanner(model_func, data, beta=296)
grid_H0, grid_Om0, switches, resonances = scanner.scan_2d(
    H0_range=(60, 80),
    Om0_range=(0.2, 0.4),
    n_points=(100, 100)
)
```

### 4. Lösungs-Mannigfaltigkeit extrahieren
```python
manifold_H0, manifold_Om0 = scanner.find_manifold()
```

### 5. Geometrie analysieren
```python
geometry = scanner.analyze_geometry()
# Erwartung: Ring, Kreis, oder geschlossene Kurve
```

## Interpretation der Ergebnisse

### Fall 1: Punkt
```
Ergebnis: Ein einzelner Punkt mit Switch=1
Bedeutung: Eindeutige Lösung (klassisch: "Best Fit")
```

### Fall 2: Linie
```
Ergebnis: Eine Linie von Punkten mit Switch=1
Bedeutung: Degenerierte Parameter (klassisch: "Degeneracy")
```

### Fall 3: Ring/Kreis
```
Ergebnis: Geschlossene Kurve mit Switch=1
Bedeutung: Multipol-Struktur (NEU!)
Interpretation: Parameter sind nicht unsicher, sondern multiwertig
```

### Fall 4: Zwei getrennte Bereiche
```
Ergebnis: Zwei separate Cluster mit Switch=1
Bedeutung: Dipol-Struktur
Interpretation: Beide Werte sind real, verschiedene Kontexte
```

## Vergleich: Klassisch vs. Besemer

| Aspekt | Klassisch | Besemer |
|--------|-----------|---------|
| Likelihood | Weiche Gaußkurve | Binärer Switch |
| Methode | Random Walk | Gitter-Scan |
| Latenz | Einbrennphase nötig | Latenzfrei |
| Ergebnis | Wahrscheinlichkeitswolke | Geometrische Struktur |
| Interpretation | "Wahrscheinlich hier" | "Existiert hier" |
| Unsicherheit | Fehlerbalken | Mannigfaltigkeits-Form |
| Hubble-Tension | Widerspruch | Dipol |

## Philosophie

### Klassisch
"Wir wissen nicht genau, wo der Parameter ist, aber wahrscheinlich hier."

### Besemer
"Wir filtern das Unmögliche weg, bis nur noch die Struktur der Wahrheit übrig bleibt."

---

**Zusammenfassung**: 
Keine Wahrscheinlichkeit. Keine Latenz. Keine Unsicherheit.
Nur Resonanz, Geometrie, und Struktur.
