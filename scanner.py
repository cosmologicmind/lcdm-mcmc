"""
Latenzfreier Gitter-Scanner

Statt Random Walk (MCMC): Systematischer Scan des Parameterraums.
Prinzip: Filtere das Unmögliche weg, bis nur die Struktur übrig bleibt.
"""

import numpy as np
from besemer_core import BesemerSwitch, compute_residual_norm


class LatencyFreeScanner:
    """
    Scannt den Parameterraum ohne Latenz (keine Einbrennphase).
    
    Unterschied zu MCMC:
    - MCMC: Random Walk, braucht tausende Schritte zum "Einbrennen"
    - Besemer: Direkter Scan, jeder Punkt wird sofort evaluiert
    """
    
    def __init__(self, model_func, data, errors=None, beta=296, threshold=1.0):
        """
        Args:
            model_func: Funktion θ → Modell(θ)
            data: Beobachtungsdaten
            errors: Fehlerbalken
            beta: Verstärker
            threshold: Switch-Schwelle
        """
        self.model_func = model_func
        self.data = data
        self.errors = errors
        self.switch = BesemerSwitch(beta=beta, threshold=threshold)
        
        # Ergebnisse
        self.grid_points = None
        self.switch_values = None
        self.resonance_values = None
    
    def scan_1d(self, param_range, n_points=1000):
        """
        1D-Scan eines Parameters.
        
        Args:
            param_range: (min, max) für Parameter
            n_points: Anzahl Gitterpunkte
        
        Returns:
            params: Array der Parameter
            switches: Array der Switch-Werte (0 oder 1)
        """
        params = np.linspace(param_range[0], param_range[1], n_points)
        switches = np.zeros(n_points)
        resonances = np.zeros(n_points)
        
        for i, param in enumerate(params):
            model = self.model_func(param)
            residual = compute_residual_norm(self.data, model, self.errors)
            switches[i] = self.switch(residual)
            resonances[i] = self.switch.resonance_strength(residual)
        
        return params, switches, resonances
    
    def scan_2d(self, param1_range, param2_range, n_points=(100, 100)):
        """
        2D-Scan zweier Parameter (z.B. H0 und Ωm).
        
        Args:
            param1_range: (min, max) für ersten Parameter
            param2_range: (min, max) für zweiten Parameter
            n_points: (n1, n2) Gitterpunkte
        
        Returns:
            grid1, grid2: Meshgrid der Parameter
            switches: 2D-Array der Switch-Werte
        """
        param1 = np.linspace(param1_range[0], param1_range[1], n_points[0])
        param2 = np.linspace(param2_range[0], param2_range[1], n_points[1])
        
        grid1, grid2 = np.meshgrid(param1, param2)
        switches = np.zeros_like(grid1)
        resonances = np.zeros_like(grid1)
        
        total = n_points[0] * n_points[1]
        print(f"Scanne {total} Punkte im Parameterraum...")
        
        for i in range(n_points[0]):
            for j in range(n_points[1]):
                model = self.model_func(grid1[j, i], grid2[j, i])
                residual = compute_residual_norm(self.data, model, self.errors)
                switches[j, i] = self.switch(residual)
                resonances[j, i] = self.switch.resonance_strength(residual)
            
            if (i + 1) % 10 == 0:
                print(f"  {i+1}/{n_points[0]} abgeschlossen...")
        
        # Speichere Ergebnisse
        self.grid_points = (grid1, grid2)
        self.switch_values = switches
        self.resonance_values = resonances
        
        return grid1, grid2, switches, resonances
    
    def find_manifold(self):
        """
        Extrahiert die Lösungs-Mannigfaltigkeit (Punkte mit Switch=1).
        
        Returns:
            manifold_points: Liste von (param1, param2) Tupeln
        """
        if self.switch_values is None:
            raise ValueError("Führe zuerst scan_2d() aus")
        
        # Finde alle Punkte mit Switch=1
        mask = self.switch_values == 1
        grid1, grid2 = self.grid_points
        
        manifold_param1 = grid1[mask]
        manifold_param2 = grid2[mask]
        
        return manifold_param1, manifold_param2
    
    def analyze_geometry(self):
        """
        Analysiert die Geometrie der Lösungs-Mannigfaltigkeit.
        
        Returns:
            dict mit geometrischen Eigenschaften
        """
        if self.switch_values is None:
            raise ValueError("Führe zuerst scan_2d() aus")
        
        n_resonant = np.sum(self.switch_values == 1)
        total = self.switch_values.size
        fraction = n_resonant / total
        
        manifold_param1, manifold_param2 = self.find_manifold()
        
        result = {
            'n_resonant_points': n_resonant,
            'total_points': total,
            'resonance_fraction': fraction,
            'manifold_size': len(manifold_param1)
        }
        
        if len(manifold_param1) > 0:
            result['param1_mean'] = np.mean(manifold_param1)
            result['param1_std'] = np.std(manifold_param1)
            result['param2_mean'] = np.mean(manifold_param2)
            result['param2_std'] = np.std(manifold_param2)
        
        return result


class AdaptiveScanner(LatencyFreeScanner):
    """
    Adaptiver Scanner: Verfeinert automatisch Bereiche mit Switch=1.
    
    Strategie:
    1. Grober Scan des gesamten Raums
    2. Identifiziere Bereiche mit Switch=1
    3. Verfeinere diese Bereiche rekursiv
    """
    
    def scan_adaptive_2d(self, param1_range, param2_range, 
                         initial_points=(50, 50), 
                         refinement_levels=2,
                         refinement_factor=2):
        """
        Adaptiver 2D-Scan mit automatischer Verfeinerung.
        
        Args:
            param1_range, param2_range: Parameterbereiche
            initial_points: Initiale Gitterauflösung
            refinement_levels: Anzahl Verfeinerungsschritte
            refinement_factor: Faktor für Verfeinerung
        """
        print("=== Adaptiver Scan ===")
        print(f"Level 0: Initialer Scan ({initial_points[0]}x{initial_points[1]} Punkte)")
        
        # Initialer grober Scan
        grid1, grid2, switches, resonances = self.scan_2d(
            param1_range, param2_range, initial_points
        )
        
        # Finde Bereiche mit Switch=1
        # TODO: Implementiere Verfeinerungslogik
        # Für jetzt: Gib initiale Ergebnisse zurück
        
        return grid1, grid2, switches, resonances


def test_scanner():
    """
    Test: Scannt eine einfache Funktion.
    """
    # Einfaches Testmodell: Parabel
    def model_func(x):
        return x**2
    
    # "Beobachtungsdaten": Parabel bei x=2
    data = np.array([4.0])
    
    scanner = LatencyFreeScanner(
        model_func=model_func,
        data=data,
        beta=296,
        threshold=1.0
    )
    
    # 1D-Scan
    params, switches, resonances = scanner.scan_1d(param_range=(0, 5), n_points=1000)
    
    # Finde Resonanzpunkte
    resonant_params = params[switches == 1]
    
    print(f"Resonante Parameter: {resonant_params}")
    print(f"Erwarteter Wert: 2.0")
    
    if len(resonant_params) > 0:
        print(f"Gefundener Wert: {np.mean(resonant_params):.3f}")


if __name__ == "__main__":
    print("=== Latenzfreier Scanner Test ===\n")
    test_scanner()
