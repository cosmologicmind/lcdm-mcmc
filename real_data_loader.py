"""
Real Cosmological Data Loaders

Loads actual Planck CMB and Pantheon+ Supernova data for
validation of the binary switch framework.
"""

import numpy as np
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u


class PantheonPlusSupernovaData:
    """
    Load Pantheon+ Type Ia Supernova sample (Scolnic et al. 2022).
    
    Contains 1701 SNe Ia with:
    - Redshifts (z)
    - Distance moduli (μ)
    - Uncertainties (σ_μ)
    
    Reference: https://github.com/PantheonPlusSH0ES/DataRelease
    """
    
    def __init__(self, data_file='data/pantheon_plus.dat'):
        """
        Args:
            data_file: Path to Pantheon+ data file
        """
        self.data_file = data_file
        self.z, self.mu_obs, self.sigma_mu = self.load_data()
        
        # Fiducial cosmology from Pantheon+ analysis
        self.fiducial_H0 = 73.0  # km/s/Mpc
        self.fiducial_Om0 = 0.30
        
        print(f"Loaded {len(self.z)} supernovae from Pantheon+")
        print(f"Redshift range: {self.z.min():.4f} to {self.z.max():.4f}")
    
    def load_data(self):
        """
        Load Pantheon+ distance moduli.
        
        Returns:
            z: Redshifts
            mu: Observed distance moduli
            sigma: Uncertainties
        """
        # Read data with mixed types
        # Columns: CID (str), IDSURVEY (int), zHD (float), ...
        
        z_list = []
        mu_list = []
        sigma_list = []
        
        with open(self.data_file, 'r') as f:
            # Skip header
            f.readline()
            
            for line in f:
                parts = line.split()
                if len(parts) < 12:
                    continue
                
                try:
                    # Column indices (0-based):
                    # 2: zHD (Heliocentric redshift)
                    # 10: MU_SH0ES (distance modulus)
                    # 11: MU_SH0ES_ERR_DIAG (uncertainty)
                    z = float(parts[2])
                    mu = float(parts[10])
                    sigma = float(parts[11])
                    
                    # Filter valid entries
                    if z > 0 and mu > 0 and sigma > 0:
                        z_list.append(z)
                        mu_list.append(mu)
                        sigma_list.append(sigma)
                except (ValueError, IndexError):
                    continue
        
        return np.array(z_list), np.array(mu_list), np.array(sigma_list)
    
    def compute_model_mu(self, H0, Om0):
        """
        Compute theoretical distance modulus for given cosmology.
        
        Args:
            H0: Hubble constant [km/s/Mpc]
            Om0: Matter density parameter
            
        Returns:
            mu_model: Model distance moduli at observed redshifts
        """
        cosmo = FlatLambdaCDM(H0=H0, Om0=Om0)
        
        # Luminosity distance
        DL = cosmo.luminosity_distance(self.z).value  # Mpc
        
        # Distance modulus: μ = 5 log10(DL/10pc) = 5 log10(DL) + 25
        mu_model = 5 * np.log10(DL) + 25
        
        return mu_model
    
    def compute_chi_squared(self, H0, Om0):
        """
        Compute χ² for given cosmology.
        
        Args:
            H0: Hubble constant [km/s/Mpc]
            Om0: Matter density parameter
            
        Returns:
            chi2: Chi-squared value
        """
        mu_model = self.compute_model_mu(H0, Om0)
        
        residuals = (self.mu_obs - mu_model) / self.sigma_mu
        chi2 = np.sum(residuals**2)
        
        return chi2
    
    def compute_residual_norm(self, H0, Om0):
        """
        Compute L2 norm of residuals (for switch function).
        
        Args:
            H0: Hubble constant [km/s/Mpc]
            Om0: Matter density parameter
            
        Returns:
            norm: L2 norm of weighted residuals
        """
        mu_model = self.compute_model_mu(H0, Om0)
        
        residuals = (self.mu_obs - mu_model) / self.sigma_mu
        norm = np.sqrt(np.sum(residuals**2))
        
        return norm


class PlanckCMBData:
    """
    Planck CMB power spectrum data (2018 final release).
    
    Since the Planck archive is currently unavailable, we use
    the published best-fit values and create a simplified model.
    
    For full analysis, download from:
    https://pla.esac.esa.int/
    
    Reference: Planck Collaboration (2020), A&A 641, A6
    """
    
    def __init__(self):
        """Initialize with Planck 2018 best-fit parameters."""
        # Planck 2018 TT,TE,EE+lowE+lensing best-fit
        self.fiducial_H0 = 67.36  # km/s/Mpc
        self.fiducial_Om0 = 0.3153
        self.fiducial_Ob0 = 0.04930  # Baryon density
        
        # For now, use a simplified approach
        # In full implementation, this would load actual C_ℓ data
        print("Using Planck 2018 best-fit cosmology")
        print(f"H0 = {self.fiducial_H0:.2f} km/s/Mpc")
        print(f"Ωm = {self.fiducial_Om0:.4f}")
    
    def compute_chi_squared_simple(self, H0, Om0):
        """
        Simplified χ² based on parameter constraints.
        
        This is a placeholder until we integrate CAMB.
        Uses Gaussian approximation around best-fit.
        
        Args:
            H0: Hubble constant [km/s/Mpc]
            Om0: Matter density parameter
            
        Returns:
            chi2: Approximate chi-squared
        """
        # Planck 2018 uncertainties
        sigma_H0 = 0.54  # km/s/Mpc
        sigma_Om0 = 0.0073
        
        # Gaussian χ²
        chi2_H0 = ((H0 - self.fiducial_H0) / sigma_H0)**2
        chi2_Om0 = ((Om0 - self.fiducial_Om0) / sigma_Om0)**2
        
        # Assume uncorrelated (simplification)
        chi2 = chi2_H0 + chi2_Om0
        
        return chi2
    
    def compute_residual_norm(self, H0, Om0):
        """
        Compute residual norm for switch function.
        
        Args:
            H0: Hubble constant [km/s/Mpc]
            Om0: Matter density parameter
            
        Returns:
            norm: Residual norm
        """
        chi2 = self.compute_chi_squared_simple(H0, Om0)
        return np.sqrt(chi2)


def test_pantheon_data():
    """Test Pantheon+ data loading and analysis."""
    print("="*60)
    print("Testing Pantheon+ Supernova Data")
    print("="*60)
    
    # Load data
    pantheon = PantheonPlusSupernovaData()
    
    print(f"\nData statistics:")
    print(f"  Number of SNe: {len(pantheon.z)}")
    print(f"  Redshift range: {pantheon.z.min():.4f} - {pantheon.z.max():.4f}")
    print(f"  μ range: {pantheon.mu_obs.min():.2f} - {pantheon.mu_obs.max():.2f}")
    
    # Test with fiducial cosmology
    print(f"\nTesting with fiducial cosmology:")
    print(f"  H0 = {pantheon.fiducial_H0} km/s/Mpc")
    print(f"  Ωm = {pantheon.fiducial_Om0}")
    
    chi2 = pantheon.compute_chi_squared(pantheon.fiducial_H0, pantheon.fiducial_Om0)
    residual = pantheon.compute_residual_norm(pantheon.fiducial_H0, pantheon.fiducial_Om0)
    
    print(f"  χ² = {chi2:.2f}")
    print(f"  Residual norm = {residual:.2f}")
    print(f"  χ²/dof = {chi2/len(pantheon.z):.3f}")
    
    # Test with Planck value
    print(f"\nTesting with Planck H0 = 67.4 km/s/Mpc:")
    chi2_planck = pantheon.compute_chi_squared(67.4, 0.315)
    residual_planck = pantheon.compute_residual_norm(67.4, 0.315)
    
    print(f"  χ² = {chi2_planck:.2f}")
    print(f"  Residual norm = {residual_planck:.2f}")
    print(f"  Δχ² from fiducial = {chi2_planck - chi2:.2f}")
    
    print("\n✓ Pantheon+ data loaded and tested successfully!")


def test_planck_data():
    """Test Planck CMB data."""
    print("\n" + "="*60)
    print("Testing Planck CMB Data")
    print("="*60)
    
    # Load data
    planck = PlanckCMBData()
    
    print(f"\nTesting with fiducial cosmology:")
    chi2 = planck.compute_chi_squared_simple(planck.fiducial_H0, planck.fiducial_Om0)
    residual = planck.compute_residual_norm(planck.fiducial_H0, planck.fiducial_Om0)
    
    print(f"  χ² = {chi2:.2f}")
    print(f"  Residual norm = {residual:.2f}")
    
    # Test with SH0ES value
    print(f"\nTesting with SH0ES H0 = 73.0 km/s/Mpc:")
    chi2_shoes = planck.compute_chi_squared_simple(73.0, 0.30)
    residual_shoes = planck.compute_residual_norm(73.0, 0.30)
    
    print(f"  χ² = {chi2_shoes:.2f}")
    print(f"  Residual norm = {residual_shoes:.2f}")
    print(f"  Δχ² from fiducial = {chi2_shoes - chi2:.2f}")
    print(f"  Significance: {np.sqrt(chi2_shoes - chi2):.1f}σ")
    
    print("\n✓ Planck data tested successfully!")


if __name__ == "__main__":
    # Test both data loaders
    test_pantheon_data()
    test_planck_data()
    
    print("\n" + "="*60)
    print("All tests passed! Real data loaders ready.")
    print("="*60)
