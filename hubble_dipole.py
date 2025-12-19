"""
Hubble-Tension als Dipol-Analyse

Klassische Sicht: H0 = 67 (Planck) vs. H0 = 73 (Supernova) → "Spannung"
Besemer-Sicht: Zwei Pole eines Dipols, verbunden durch geschlossene Kurve

Ziel: Zeige, dass beide Werte real sind und geometrisch zusammenhängen.
"""

import numpy as np
from astropy.cosmology import FlatLambdaCDM
from besemer_core import BesemerSwitch, compute_residual_norm
from scanner import LatencyFreeScanner


class HubbleDipoleAnalyzer:
    """
    Analysiert die Hubble-Tension als Multipol-Struktur.
    
    Hypothese: Die beiden H0-Werte (67 und 73) sind keine Widersprüche,
    sondern zwei Manifestationen derselben Geometrie in verschiedenen Kontexten.
    """
    
    def __init__(self, planck_data, supernova_data, beta=296):
        """
        Args:
            planck_data: PlanckCMBData Objekt (globale Messung)
            supernova_data: SupernovaData Objekt (lokale Messung)
            beta: Verstärker
        """
        self.planck_data = planck_data
        self.supernova_data = supernova_data
        self.beta = beta
        
        # Bekannte Pole der Hubble-Tension
        self.H0_planck = 67.4  # km/s/Mpc (global, früh)
        self.H0_supernova = 73.0  # km/s/Mpc (lokal, spät)
    
    def model_planck(self, H0, Om0):
        """
        Modelliert CMB Power Spectrum für gegebene Parameter.
        """
        cosmo = FlatLambdaCDM(H0=H0, Om0=Om0)
        ell, _, _ = self.planck_data.get_data()
        
        # Vereinfachtes Modell (wie in data_loader)
        z_star = 1090
        scale = (H0 / 70.0) * (0.3 / Om0)**0.5
        C_ell = 5000 * scale * (ell / 200.0)**(-1.0) * np.exp(-ell / 1500.0)
        
        return C_ell
    
    def model_supernova(self, H0, Om0):
        """
        Modelliert Supernova Distance Modulus für gegebene Parameter.
        """
        cosmo = FlatLambdaCDM(H0=H0, Om0=Om0)
        z, _, _ = self.supernova_data.get_data()
        
        # Luminosity Distance
        d_L = cosmo.luminosity_distance(z).value
        mu = 5 * np.log10(d_L * 1e6 / 10.0)
        
        return mu
    
    def scan_planck_context(self, H0_range=(60, 80), Om0_range=(0.2, 0.4), n_points=(100, 100)):
        """
        Scannt Parameterraum im Planck-Kontext (globale Messung).
        
        Returns:
            grid_H0, grid_Om0, switches, resonances
        """
        print("=== Planck-Kontext (Global, Früh) ===")
        
        ell, data, errors = self.planck_data.get_data()
        
        scanner = LatencyFreeScanner(
            model_func=self.model_planck,
            data=data,
            errors=errors,
            beta=self.beta
        )
        
        return scanner.scan_2d(H0_range, Om0_range, n_points)
    
    def scan_supernova_context(self, H0_range=(60, 80), Om0_range=(0.2, 0.4), n_points=(100, 100)):
        """
        Scannt Parameterraum im Supernova-Kontext (lokale Messung).
        
        Returns:
            grid_H0, grid_Om0, switches, resonances
        """
        print("=== Supernova-Kontext (Lokal, Spät) ===")
        
        z, data, errors = self.supernova_data.get_data()
        
        scanner = LatencyFreeScanner(
            model_func=self.model_supernova,
            data=data,
            errors=errors,
            beta=self.beta
        )
        
        return scanner.scan_2d(H0_range, Om0_range, n_points)
    
    def find_dipole_structure(self, planck_switches, supernova_switches, grid_H0, grid_Om0):
        """
        Identifiziert Dipol-Struktur zwischen beiden Kontexten.
        
        Args:
            planck_switches: Switch-Werte aus Planck-Scan
            supernova_switches: Switch-Werte aus Supernova-Scan
            grid_H0, grid_Om0: Parameter-Gitter
        
        Returns:
            dict mit Dipol-Eigenschaften
        """
        # Finde Zentren der beiden Pole
        planck_mask = planck_switches == 1
        supernova_mask = supernova_switches == 1
        
        result = {
            'planck_pole': None,
            'supernova_pole': None,
            'dipole_distance': None,
            'dipole_angle': None,
            'overlap': None
        }
        
        if np.any(planck_mask):
            planck_H0 = grid_H0[planck_mask]
            planck_Om0 = grid_Om0[planck_mask]
            result['planck_pole'] = (np.mean(planck_H0), np.mean(planck_Om0))
        
        if np.any(supernova_mask):
            sn_H0 = grid_H0[supernova_mask]
            sn_Om0 = grid_Om0[supernova_mask]
            result['supernova_pole'] = (np.mean(sn_H0), np.mean(sn_Om0))
        
        # Berechne Dipol-Eigenschaften
        if result['planck_pole'] and result['supernova_pole']:
            p1 = np.array(result['planck_pole'])
            p2 = np.array(result['supernova_pole'])
            
            # Euklidische Distanz im Parameterraum
            result['dipole_distance'] = np.linalg.norm(p2 - p1)
            
            # Winkel (in H0-Om0 Ebene)
            delta = p2 - p1
            result['dipole_angle'] = np.arctan2(delta[1], delta[0]) * 180 / np.pi
            
            # Überlappung (wie viele Punkte sind in beiden Kontexten resonant?)
            overlap_mask = (planck_switches == 1) & (supernova_switches == 1)
            result['overlap'] = np.sum(overlap_mask)
        
        return result
    
    def test_pole_resonance(self):
        """
        Testet, ob beide bekannten H0-Werte den Switch auslösen.
        
        Erwartung: Beide sollten in ihrem jeweiligen Kontext resonant sein.
        """
        print("=== Test der Pol-Resonanz ===\n")
        
        # Test Planck-Pol (H0=67.4)
        Om0_test = 0.315
        
        print(f"Planck-Pol: H0={self.H0_planck}, Ωm={Om0_test}")
        planck_model = self.model_planck(self.H0_planck, Om0_test)
        _, planck_data, planck_errors = self.planck_data.get_data()
        planck_residual = compute_residual_norm(planck_data, planck_model, planck_errors)
        planck_switch = BesemerSwitch(beta=self.beta)(planck_residual)
        print(f"  Residual: {planck_residual:.4f}")
        print(f"  Switch: {planck_switch}")
        
        # Test Supernova-Pol (H0=73.0)
        print(f"\nSupernova-Pol: H0={self.H0_supernova}, Ωm={Om0_test}")
        sn_model = self.model_supernova(self.H0_supernova, Om0_test)
        _, sn_data, sn_errors = self.supernova_data.get_data()
        sn_residual = compute_residual_norm(sn_data, sn_model, sn_errors)
        sn_switch = BesemerSwitch(beta=self.beta)(sn_residual)
        print(f"  Residual: {sn_residual:.4f}")
        print(f"  Switch: {sn_switch}")
        
        return {
            'planck': {'H0': self.H0_planck, 'switch': planck_switch, 'residual': planck_residual},
            'supernova': {'H0': self.H0_supernova, 'switch': sn_switch, 'residual': sn_residual}
        }


def analyze_hubble_tension(beta=296, n_points=(100, 100)):
    """
    Führt vollständige Hubble-Dipol-Analyse durch.
    
    Args:
        beta: Verstärker
        n_points: Gitterauflösung
    
    Returns:
        dict mit allen Ergebnissen
    """
    from data_loader import PlanckCMBData, SupernovaData
    
    print("=== Hubble-Tension Dipol-Analyse ===\n")
    
    # Lade Daten
    planck = PlanckCMBData(fiducial_H0=67.4, fiducial_Om0=0.315)
    supernova = SupernovaData(fiducial_H0=73.0, fiducial_Om0=0.3)
    
    # Initialisiere Analyzer
    analyzer = HubbleDipoleAnalyzer(planck, supernova, beta=beta)
    
    # Test Pol-Resonanz
    pole_test = analyzer.test_pole_resonance()
    
    # Scanne beide Kontexte
    print("\n" + "="*50)
    grid_H0_p, grid_Om0_p, switches_p, resonances_p = analyzer.scan_planck_context(
        H0_range=(60, 80), Om0_range=(0.2, 0.4), n_points=n_points
    )
    
    print("\n" + "="*50)
    grid_H0_s, grid_Om0_s, switches_s, resonances_s = analyzer.scan_supernova_context(
        H0_range=(60, 80), Om0_range=(0.2, 0.4), n_points=n_points
    )
    
    # Finde Dipol-Struktur
    print("\n" + "="*50)
    print("=== Dipol-Struktur ===")
    dipole = analyzer.find_dipole_structure(switches_p, switches_s, grid_H0_p, grid_Om0_p)
    
    if dipole['planck_pole']:
        print(f"Planck-Pol: H0={dipole['planck_pole'][0]:.2f}, Ωm={dipole['planck_pole'][1]:.3f}")
    if dipole['supernova_pole']:
        print(f"Supernova-Pol: H0={dipole['supernova_pole'][0]:.2f}, Ωm={dipole['supernova_pole'][1]:.3f}")
    if dipole['dipole_distance']:
        print(f"Dipol-Distanz: {dipole['dipole_distance']:.3f}")
        print(f"Dipol-Winkel: {dipole['dipole_angle']:.1f}°")
    print(f"Überlappung: {dipole['overlap']} Punkte")
    
    return {
        'pole_test': pole_test,
        'planck_scan': (grid_H0_p, grid_Om0_p, switches_p, resonances_p),
        'supernova_scan': (grid_H0_s, grid_Om0_s, switches_s, resonances_s),
        'dipole': dipole
    }


if __name__ == "__main__":
    results = analyze_hubble_tension(beta=296, n_points=(50, 50))
