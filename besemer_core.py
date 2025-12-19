"""
Besemer-Switch: Binäre Resonanzlogik für kosmologische Parameter

Prinzip: Keine Wahrscheinlichkeit, nur Zustand.
- Resonanz (1): Modell und Daten sind kohärent
- Dissonanz (0): Modell ist unmöglich
"""

import numpy as np


class BesemerSwitch:
    """
    Implementiert die binäre Switch-Funktion:
    P(θ) = Θ(β · |Daten - Modell(θ)|⁻¹ - Schwelle)
    """
    
    def __init__(self, beta=296, threshold=1.0, epsilon=1e-10):
        """
        Args:
            beta: Verstärker (default: 296)
            threshold: Schwellenwert für Switch
            epsilon: Numerische Stabilität (verhindert Division durch 0)
        """
        self.beta = beta
        self.threshold = threshold
        self.epsilon = epsilon
    
    def __call__(self, residual):
        """
        Wendet den Switch auf Residuen an.
        
        Args:
            residual: |Daten - Modell| (kann Array sein)
        
        Returns:
            0 oder 1 (binär)
        """
        # Verhindere Division durch 0
        residual_safe = np.maximum(residual, self.epsilon)
        
        # Inverse Verstärkung: Je kleiner der Fehler, desto größer der Wert
        amplified = self.beta / residual_safe
        
        # Heaviside-Funktion (binärer Switch)
        return np.where(amplified >= self.threshold, 1, 0)
    
    def resonance_strength(self, residual):
        """
        Gibt die Stärke der Resonanz zurück (vor dem binären Cut).
        Nützlich für Visualisierung.
        """
        residual_safe = np.maximum(residual, self.epsilon)
        return self.beta / residual_safe


def heaviside(x):
    """
    Heaviside-Stufenfunktion: Θ(x)
    
    Returns:
        0 für x < 0
        1 für x >= 0
    """
    return np.where(x >= 0, 1, 0)


def compute_chi_squared(data, model, errors=None):
    """
    Berechnet χ² zwischen Daten und Modell.
    
    Args:
        data: Beobachtete Daten
        model: Modellvorhersage
        errors: Fehlerbalken (optional)
    
    Returns:
        χ² Wert
    """
    residual = data - model
    
    if errors is not None:
        residual = residual / errors
    
    return np.sum(residual**2)


def compute_residual_norm(data, model, errors=None):
    """
    Berechnet die Norm des Residuums für den Switch.
    
    Args:
        data: Beobachtete Daten
        model: Modellvorhersage
        errors: Fehlerbalken (optional)
    
    Returns:
        |Daten - Modell| (skalare Norm)
    """
    residual = data - model
    
    if errors is not None:
        residual = residual / errors
    
    # L2-Norm (euklidische Distanz)
    return np.sqrt(np.sum(residual**2))


class BesemerLikelihood:
    """
    Ersetzt klassische Likelihood durch Switch-Logik.
    
    Klassisch: L(θ) ∝ exp(-χ²/2)  [weich]
    Besemer:   L(θ) = Θ(β/||r|| - threshold)  [binär]
    """
    
    def __init__(self, data, errors=None, beta=296, threshold=1.0):
        """
        Args:
            data: Beobachtungsdaten
            errors: Fehlerbalken
            beta: Verstärker
            threshold: Switch-Schwelle
        """
        self.data = data
        self.errors = errors
        self.switch = BesemerSwitch(beta=beta, threshold=threshold)
    
    def __call__(self, model):
        """
        Evaluiert Likelihood für ein Modell.
        
        Args:
            model: Modellvorhersage (gleiche Form wie data)
        
        Returns:
            0 oder 1 (binär)
        """
        residual_norm = compute_residual_norm(self.data, model, self.errors)
        return self.switch(residual_norm)
    
    def resonance_map(self, model):
        """
        Gibt kontinuierliche Resonanzstärke zurück (für Visualisierung).
        """
        residual_norm = compute_residual_norm(self.data, model, self.errors)
        return self.switch.resonance_strength(residual_norm)


def test_switch():
    """
    Test: Zeigt, dass der Switch bei exakter Übereinstimmung aktiviert.
    """
    # Höhere Schwelle für realistischen Test
    switch = BesemerSwitch(beta=296, threshold=100.0)
    
    # Test 1: Perfekte Übereinstimmung
    residual_perfect = 0.001  # Sehr klein → β/r = 296000 >> 100
    result = switch(residual_perfect)
    resonance = switch.resonance_strength(residual_perfect)
    print(f"Perfekte Übereinstimmung (r={residual_perfect}):")
    print(f"  Resonanz: {resonance:.2f}, Switch: {result}")
    
    # Test 2: Gute Übereinstimmung
    residual_good = 2.0  # Klein → β/r = 148 > 100
    result = switch(residual_good)
    resonance = switch.resonance_strength(residual_good)
    print(f"\nGute Übereinstimmung (r={residual_good}):")
    print(f"  Resonanz: {resonance:.2f}, Switch: {result}")
    
    # Test 3: Grenzfall
    residual_edge = 2.96  # β/r = 100 (exakt an Schwelle)
    result = switch(residual_edge)
    resonance = switch.resonance_strength(residual_edge)
    print(f"\nGrenzfall (r={residual_edge}):")
    print(f"  Resonanz: {resonance:.2f}, Switch: {result}")
    
    # Test 4: Schlechte Übereinstimmung
    residual_bad = 10.0  # Groß → β/r = 29.6 < 100
    result = switch(residual_bad)
    resonance = switch.resonance_strength(residual_bad)
    print(f"\nSchlechte Übereinstimmung (r={residual_bad}):")
    print(f"  Resonanz: {resonance:.2f}, Switch: {result}")
    
    print(f"\nSchwelle: {switch.threshold}")
    print(f"Switch aktiviert wenn: β/r >= {switch.threshold}")
    print(f"                  d.h.: r <= {switch.beta/switch.threshold:.3f}")


if __name__ == "__main__":
    print("=== Besemer-Switch Test ===\n")
    test_switch()
