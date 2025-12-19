"""
Daten-Loader für kosmologische Beobachtungen

Unterstützt:
- Planck CMB Power Spectrum (simuliert)
- Supernova Distance Modulus
- BAO (Baryon Acoustic Oscillations)
"""

import numpy as np
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u


class PlanckCMBData:
    """
    Simuliert Planck CMB Power Spectrum Daten.
    
    In Produktion: Würde echte Planck-Daten laden.
    Für Test: Generiert synthetische Daten mit bekannten Parametern.
    """
    
    def __init__(self, fiducial_H0=67.4, fiducial_Om0=0.315):
        """
        Args:
            fiducial_H0: "Wahre" Hubble-Konstante für Simulation
            fiducial_Om0: "Wahre" Materiedichte
        """
        self.fiducial_H0 = fiducial_H0
        self.fiducial_Om0 = fiducial_Om0
        
        # Multipole (ℓ) für CMB Power Spectrum
        self.ell = np.arange(2, 2500, 50)
        
        # Generiere "beobachtete" Daten
        self.data, self.errors = self._generate_data()
    
    def _generate_data(self):
        """
        Generiert synthetische CMB-Daten.
        
        Vereinfachtes Modell: C_ℓ ∝ ℓ^(-2) mit kosmologischer Abhängigkeit
        """
        cosmo = FlatLambdaCDM(H0=self.fiducial_H0, Om0=self.fiducial_Om0)
        
        # Vereinfachtes Power Spectrum (nicht physikalisch exakt, aber ausreichend für Test)
        # Echte Implementierung würde CAMB/CLASS nutzen
        z_star = 1090  # Rekombination
        D_A = cosmo.angular_diameter_distance(z_star).value  # Mpc
        
        # Skalierung mit kosmologischen Parametern
        scale = (self.fiducial_H0 / 70.0) * (0.3 / self.fiducial_Om0)**0.5
        
        # Power Spectrum (vereinfacht)
        C_ell = 5000 * scale * (self.ell / 200.0)**(-1.0) * np.exp(-self.ell / 1500.0)
        
        # Füge Rauschen hinzu
        noise = np.random.normal(0, 0.05 * C_ell)
        data = C_ell + noise
        
        # Fehlerbalken (5% der Amplitude)
        errors = 0.05 * C_ell
        
        return data, errors
    
    def get_data(self):
        """Returns: (ell, C_ell, errors)"""
        return self.ell, self.data, self.errors


class SupernovaData:
    """
    Supernova Type Ia Distance Modulus Daten.
    
    Misst Expansion des Universums über Rotverschiebung z.
    """
    
    def __init__(self, fiducial_H0=73.0, fiducial_Om0=0.3):
        """
        Args:
            fiducial_H0: "Wahre" Hubble-Konstante (lokal)
            fiducial_Om0: "Wahre" Materiedichte
        """
        self.fiducial_H0 = fiducial_H0
        self.fiducial_Om0 = fiducial_Om0
        
        # Rotverschiebungen (z) der Supernovae
        self.z = np.linspace(0.01, 1.5, 50)
        
        # Generiere "beobachtete" Daten
        self.data, self.errors = self._generate_data()
    
    def _generate_data(self):
        """
        Generiert synthetische Supernova-Daten.
        
        Distance Modulus: μ = 5 log₁₀(d_L / 10 pc)
        """
        cosmo = FlatLambdaCDM(H0=self.fiducial_H0, Om0=self.fiducial_Om0)
        
        # Luminosity Distance
        d_L = cosmo.luminosity_distance(self.z).value  # Mpc
        
        # Distance Modulus
        mu = 5 * np.log10(d_L * 1e6 / 10.0)  # Umrechnung Mpc → pc
        
        # Füge Rauschen hinzu (typisch: ~0.15 mag)
        noise = np.random.normal(0, 0.15, len(self.z))
        data = mu + noise
        
        # Fehlerbalken
        errors = np.full_like(data, 0.15)
        
        return data, errors
    
    def get_data(self):
        """Returns: (z, mu, errors)"""
        return self.z, self.data, self.errors


class BAOData:
    """
    Baryon Acoustic Oscillations (BAO) Daten.
    
    Misst charakteristische Längenskala im Universum.
    """
    
    def __init__(self, fiducial_H0=67.4, fiducial_Om0=0.315):
        self.fiducial_H0 = fiducial_H0
        self.fiducial_Om0 = fiducial_Om0
        
        # Effektive Rotverschiebungen verschiedener Surveys
        self.z_eff = np.array([0.15, 0.38, 0.51, 0.61])
        
        # Generiere Daten
        self.data, self.errors = self._generate_data()
    
    def _generate_data(self):
        """
        Generiert synthetische BAO-Daten.
        
        Misst: D_V(z) / r_d
        D_V: Volumen-gemittelte Distanz
        r_d: Sound horizon bei drag epoch
        """
        cosmo = FlatLambdaCDM(H0=self.fiducial_H0, Om0=self.fiducial_Om0)
        
        # Vereinfachte BAO-Messung
        D_V = []
        for z in self.z_eff:
            D_A = cosmo.angular_diameter_distance(z).value
            H_z = cosmo.H(z).value
            D_V_z = ((1 + z)**2 * D_A**2 * 3e5 / H_z)**(1/3)  # Mpc
            D_V.append(D_V_z)
        
        D_V = np.array(D_V)
        
        # Sound horizon (vereinfacht: ~150 Mpc)
        r_d = 147.0 * (self.fiducial_Om0 * 0.7**2 / 0.02)**(-0.25)
        
        # BAO-Parameter
        data = D_V / r_d
        
        # Füge Rauschen hinzu
        noise = np.random.normal(0, 0.02 * data)
        data = data + noise
        
        # Fehlerbalken (2%)
        errors = 0.02 * data
        
        return data, errors
    
    def get_data(self):
        """Returns: (z_eff, D_V/r_d, errors)"""
        return self.z_eff, self.data, self.errors


def load_combined_dataset(dataset_type='planck'):
    """
    Lädt einen kombinierten Datensatz.
    
    Args:
        dataset_type: 'planck', 'supernova', 'bao', oder 'combined'
    
    Returns:
        Dataset-Objekt
    """
    if dataset_type == 'planck':
        return PlanckCMBData()
    elif dataset_type == 'supernova':
        return SupernovaData()
    elif dataset_type == 'bao':
        return BAOData()
    elif dataset_type == 'combined':
        # Kombiniere alle Datensätze
        return {
            'planck': PlanckCMBData(),
            'supernova': SupernovaData(),
            'bao': BAOData()
        }
    else:
        raise ValueError(f"Unbekannter Dataset-Typ: {dataset_type}")


def test_data_loader():
    """
    Test: Lädt und zeigt Daten.
    """
    print("=== Planck CMB ===")
    planck = PlanckCMBData(fiducial_H0=67.4, fiducial_Om0=0.315)
    ell, C_ell, errors = planck.get_data()
    print(f"Multipole: {len(ell)} Punkte")
    print(f"Bereich: ℓ = {ell[0]} bis {ell[-1]}")
    print(f"C_ℓ Bereich: {C_ell.min():.2f} bis {C_ell.max():.2f}")
    
    print("\n=== Supernova ===")
    sn = SupernovaData(fiducial_H0=73.0, fiducial_Om0=0.3)
    z, mu, errors = sn.get_data()
    print(f"Supernovae: {len(z)} Punkte")
    print(f"Rotverschiebung: z = {z[0]:.2f} bis {z[-1]:.2f}")
    print(f"Distance Modulus: μ = {mu.min():.2f} bis {mu.max():.2f}")
    
    print("\n=== BAO ===")
    bao = BAOData(fiducial_H0=67.4, fiducial_Om0=0.315)
    z_eff, D_V_rd, errors = bao.get_data()
    print(f"BAO Messungen: {len(z_eff)} Punkte")
    print(f"z_eff: {z_eff}")
    print(f"D_V/r_d: {D_V_rd}")


if __name__ == "__main__":
    print("=== Daten-Loader Test ===\n")
    test_data_loader()
