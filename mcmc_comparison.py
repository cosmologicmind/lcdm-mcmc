"""
Classical MCMC Analysis for Comparison

Runs traditional MCMC on the same Pantheon+ data to compare with
the binary switch approach. Shows the difference between soft
probability clouds and sharp geometric manifolds.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from real_data_loader import PantheonPlusSupernovaData, PlanckCMBData
import time


class ClassicalMCMC:
    """
    Traditional MCMC sampler using Metropolis-Hastings algorithm.
    
    This is the "old way" - slow, requires burn-in, produces soft clouds.
    """
    
    def __init__(self, data, n_walkers=10, n_steps=5000, burn_in=1000):
        """
        Args:
            data: Data object (Pantheon+ or Planck)
            n_walkers: Number of MCMC walkers
            n_steps: Number of steps per walker
            burn_in: Number of burn-in steps to discard
        """
        self.data = data
        self.n_walkers = n_walkers
        self.n_steps = n_steps
        self.burn_in = burn_in
        
        print(f"Classical MCMC initialized:")
        print(f"  Walkers: {n_walkers}")
        print(f"  Steps: {n_steps}")
        print(f"  Burn-in: {burn_in}")
        print(f"  Total evaluations: {n_walkers * n_steps}")
    
    def log_likelihood(self, params):
        """
        Classical Gaussian log-likelihood.
        
        Args:
            params: [H0, Om0]
            
        Returns:
            log_likelihood: ln(L)
        """
        H0, Om0 = params
        
        # Bounds check
        if H0 < 60 or H0 > 80 or Om0 < 0.2 or Om0 > 0.4:
            return -np.inf
        
        # Compute chi-squared
        chi2 = self.data.compute_chi_squared(H0, Om0)
        
        # Gaussian likelihood: L ∝ exp(-χ²/2)
        log_L = -0.5 * chi2
        
        return log_L
    
    def log_prior(self, params):
        """
        Flat prior within bounds.
        """
        H0, Om0 = params
        
        if 60 <= H0 <= 80 and 0.2 <= Om0 <= 0.4:
            return 0.0
        else:
            return -np.inf
    
    def log_posterior(self, params):
        """
        Log posterior = log prior + log likelihood.
        """
        lp = self.log_prior(params)
        if not np.isfinite(lp):
            return -np.inf
        
        return lp + self.log_likelihood(params)
    
    def metropolis_hastings(self, start_params, proposal_std=[0.5, 0.01]):
        """
        Metropolis-Hastings MCMC sampler.
        
        Args:
            start_params: Starting point [H0, Om0]
            proposal_std: Proposal distribution std dev
            
        Returns:
            chain: MCMC chain (n_steps, 2)
            acceptance_rate: Fraction of accepted steps
        """
        chain = np.zeros((self.n_steps, 2))
        chain[0] = start_params
        
        current_log_prob = self.log_posterior(start_params)
        n_accepted = 0
        
        for i in range(1, self.n_steps):
            # Propose new point
            proposal = chain[i-1] + np.random.normal(0, proposal_std, size=2)
            proposal_log_prob = self.log_posterior(proposal)
            
            # Metropolis acceptance criterion
            log_ratio = proposal_log_prob - current_log_prob
            
            if log_ratio > 0 or np.random.random() < np.exp(log_ratio):
                # Accept
                chain[i] = proposal
                current_log_prob = proposal_log_prob
                n_accepted += 1
            else:
                # Reject
                chain[i] = chain[i-1]
            
            # Progress
            if (i+1) % 1000 == 0:
                print(f"    Step {i+1}/{self.n_steps} ({100*(i+1)/self.n_steps:.0f}%)")
        
        acceptance_rate = n_accepted / self.n_steps
        return chain, acceptance_rate
    
    def run_mcmc(self):
        """
        Run full MCMC analysis with multiple walkers.
        
        Returns:
            chains: All chains (n_walkers, n_steps, 2)
            acceptance_rates: Acceptance rate per walker
        """
        print(f"\nRunning MCMC with {self.n_walkers} walkers...")
        start_time = time.time()
        
        # Initialize walkers around fiducial values
        if hasattr(self.data, 'fiducial_H0'):
            H0_init = self.data.fiducial_H0
            Om_init = self.data.fiducial_Om0
        else:
            H0_init = 70.0
            Om_init = 0.3
        
        chains = []
        acceptance_rates = []
        
        for i in range(self.n_walkers):
            print(f"\n  Walker {i+1}/{self.n_walkers}")
            
            # Random start near fiducial
            start = [H0_init + np.random.normal(0, 1),
                    Om_init + np.random.normal(0, 0.02)]
            
            chain, acc_rate = self.metropolis_hastings(start)
            chains.append(chain)
            acceptance_rates.append(acc_rate)
            
            print(f"    Acceptance rate: {acc_rate:.1%}")
        
        elapsed = time.time() - start_time
        
        chains = np.array(chains)
        
        print(f"\n✓ MCMC complete!")
        print(f"  Total time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
        print(f"  Mean acceptance rate: {np.mean(acceptance_rates):.1%}")
        
        return chains, acceptance_rates, elapsed
    
    def get_samples(self, chains):
        """
        Get samples after burn-in.
        
        Args:
            chains: MCMC chains (n_walkers, n_steps, 2)
            
        Returns:
            samples: Flattened samples after burn-in
        """
        # Remove burn-in
        chains_burned = chains[:, self.burn_in:, :]
        
        # Flatten
        samples = chains_burned.reshape(-1, 2)
        
        print(f"\nSamples after burn-in:")
        print(f"  Total samples: {len(samples)}")
        print(f"  H0 range: [{samples[:,0].min():.2f}, {samples[:,0].max():.2f}]")
        print(f"  Ωm range: [{samples[:,1].min():.2f}, {samples[:,1].max():.2f}]")
        
        return samples
    
    def compute_statistics(self, samples):
        """
        Compute summary statistics from samples.
        
        Args:
            samples: MCMC samples (n_samples, 2)
            
        Returns:
            dict with statistics
        """
        H0_samples = samples[:, 0]
        Om_samples = samples[:, 1]
        
        stats = {
            'H0_mean': np.mean(H0_samples),
            'H0_std': np.std(H0_samples),
            'H0_median': np.median(H0_samples),
            'H0_16': np.percentile(H0_samples, 16),
            'H0_84': np.percentile(H0_samples, 84),
            'Om_mean': np.mean(Om_samples),
            'Om_std': np.std(Om_samples),
            'Om_median': np.median(Om_samples),
            'Om_16': np.percentile(Om_samples, 16),
            'Om_84': np.percentile(Om_samples, 84),
        }
        
        print(f"\nMCMC Statistics:")
        print(f"  H0 = {stats['H0_median']:.2f} ± {stats['H0_std']:.2f} km/s/Mpc")
        print(f"  H0 68% CI: [{stats['H0_16']:.2f}, {stats['H0_84']:.2f}]")
        print(f"  Ωm = {stats['Om_median']:.3f} ± {stats['Om_std']:.3f}")
        print(f"  Ωm 68% CI: [{stats['Om_16']:.3f}, {stats['Om_84']:.3f}]")
        
        return stats


def compare_mcmc_vs_besemer(n_walkers=10, n_steps=5000):
    """
    Direct comparison: Classical MCMC vs. Besemer Switch on same data.
    
    Args:
        n_walkers: Number of MCMC walkers
        n_steps: Steps per walker
        
    Returns:
        dict with comparison results
    """
    print("="*60)
    print("MCMC vs. BESEMER: HEAD-TO-HEAD COMPARISON")
    print("="*60)
    
    # Load real data
    print("\nLoading Pantheon+ data...")
    pantheon = PantheonPlusSupernovaData()
    
    # Run Classical MCMC
    print("\n" + "="*60)
    print("CLASSICAL MCMC (The Old Way)")
    print("="*60)
    
    mcmc = ClassicalMCMC(pantheon, n_walkers=n_walkers, n_steps=n_steps)
    chains, acc_rates, mcmc_time = mcmc.run_mcmc()
    samples = mcmc.get_samples(chains)
    stats = mcmc.compute_statistics(samples)
    
    # Run Besemer Switch
    print("\n" + "="*60)
    print("BESEMER SWITCH (The New Way)")
    print("="*60)
    
    from hubble_dipole_real import analyze_hubble_tension_real_data
    
    print("\nRunning binary switch analysis...")
    besemer_start = time.time()
    besemer_results = analyze_hubble_tension_real_data(
        beta=296, 
        threshold=10.0, 
        n_points=(50, 50)
    )
    besemer_time = time.time() - besemer_start
    
    # Comparison
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    print(f"\n{'Metric':<30} {'MCMC':<20} {'Besemer':<20}")
    print("-"*70)
    print(f"{'Computation time':<30} {mcmc_time:.1f}s ({mcmc_time/60:.1f}m) {besemer_time:.1f}s")
    print(f"{'Speedup':<30} {'1×':<20} {f'{mcmc_time/besemer_time:.0f}×':<20}")
    print(f"{'Total evaluations':<30} {n_walkers*n_steps:<20} {2500:<20}")
    print(f"{'Burn-in required':<30} {'Yes (1000 steps)':<20} {'No':<20}")
    print(f"{'Convergence check':<30} {'Required':<20} {'Not needed':<20}")
    
    print(f"\n{'Result Type':<30} {'MCMC':<20} {'Besemer':<20}")
    print("-"*70)
    print(f"{'H0 (km/s/Mpc)':<30} {stats['H0_median']:.2f}±{stats['H0_std']:.2f} {besemer_results['pantheon']['pole'][0]:.2f}")
    print(f"{'Ωm':<30} {stats['Om_median']:.3f}±{stats['Om_std']:.3f} {besemer_results['pantheon']['pole'][1]:.3f}")
    print(f"{'Output type':<30} {'Probability cloud':<20} {'Sharp manifold':<20}")
    print(f"{'Constraint type':<30} {'Soft (Gaussian)':<20} {'Hard (Binary)':<20}")
    
    # Resonant fraction
    n_resonant = np.sum(besemer_results['pantheon']['switch_map'])
    n_total = besemer_results['pantheon']['switch_map'].size
    
    print(f"\n{'Interpretation':<30} {'MCMC':<20} {'Besemer':<20}")
    print("-"*70)
    print(f"{'Question asked':<30} {'How probable?':<20} {'Does it exist?':<20}")
    print(f"{'Uncertainty':<30} {'Error bars':<20} {'Manifold shape':<20}")
    print(f"{'Resonant fraction':<30} {'~68% (1σ)':<20} {f'{100*n_resonant/n_total:.1f}%':<20}")
    
    return {
        'mcmc': {
            'chains': chains,
            'samples': samples,
            'stats': stats,
            'time': mcmc_time,
            'acceptance_rates': acc_rates
        },
        'besemer': {
            'results': besemer_results,
            'time': besemer_time
        },
        'speedup': mcmc_time / besemer_time
    }


if __name__ == "__main__":
    # Run comparison
    print("\n🔥 FINAL SHOWDOWN: MCMC vs. BESEMER 🔥\n")
    
    comparison = compare_mcmc_vs_besemer(
        n_walkers=10,
        n_steps=5000  # Reduced for demo, use 10000+ for publication
    )
    
    print("\n" + "="*60)
    print("VERDICT")
    print("="*60)
    print(f"\n✓ Besemer is {comparison['speedup']:.0f}× faster")
    print("✓ Besemer requires no burn-in")
    print("✓ Besemer provides sharp geometric constraints")
    print("✓ Besemer is deterministic (no random walk)")
    
    print("\n🎯 THE NEW WAY WINS.")
