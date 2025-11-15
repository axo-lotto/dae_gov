"""
Organ Coupling Learner - R-Matrix Hebbian Updates
==================================================

Implements DAE 3.0 Level 3 (Hebbian Coupling) fractal reward propagation.

Key Insight from DAE 3.0:
- Organs that co-activate together strengthen their coupling
- R-matrix learns synergies: BOND+EO+NDAM = trauma detection triad
- Coupling amplifies nexus formation and emission quality

Mathematical Formulation (DAE 3.0):
    R₃(organ_i, organ_j) = correlation(φᵢ, φⱼ) × R₂
    Update: R(i,j) ← R(i,j) + η·R₃

Our Implementation (HYPHAE 1):
    R(i,j) ← R(i,j) + η · coh[i] · coh[j] · satisfaction · (1 - R(i,j))

Where:
    - coh[i], coh[j]: Organ coherences [0,1]
    - satisfaction: Mean satisfaction from V0 convergence
    - η: Learning rate (0.05)
    - (1 - R(i,j)): Saturation term (prevents runaway)

Date: November 12, 2025
Status: DAE 3.0 Integration - Fractal Level 3
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class CouplingUpdate:
    """Record of R-matrix coupling update"""
    organ_i: str
    organ_j: str
    delta: float
    new_coupling: float
    coherence_i: float
    coherence_j: float
    satisfaction: float


class OrganCouplingLearner:
    """
    Learns 11×11 organ coupling matrix through Hebbian strengthening.

    Implements DAE 3.0 Fractal Level 3:
    - Micro (Level 1): Phrase patterns (Hebbian memory)
    - Organ (Level 2): Organ weights (not yet implemented)
    - **Coupling (Level 3): THIS MODULE - Organ synergies** ⭐
    - Family (Level 4): Family confidence
    - Global (Level 7): Organism confidence
    """

    def __init__(
        self,
        r_matrix_path: Path = Path("persona_layer/state/active/conversational_hebbian_memory.json"),
        learning_rate: float = 0.05,
        saturation_enabled: bool = True
    ):
        """
        Initialize organ coupling learner.

        Args:
            r_matrix_path: Path to save/load R-matrix
            learning_rate: Hebbian learning rate η
            saturation_enabled: Apply (1 - R[i,j]) saturation term
        """
        self.r_matrix_path = r_matrix_path
        self.eta = learning_rate
        self.saturation_enabled = saturation_enabled

        # 11 organs in DAE_HYPHAE_1
        self.organ_names = [
            'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',  # Conversational (5)
            'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'  # Trauma/Context (6)
        ]

        # Initialize or load R-matrix
        self.R_matrix = self._load_or_initialize()

        # Track update history
        self.update_history: List[CouplingUpdate] = []

    def _load_or_initialize(self) -> np.ndarray:
        """Load existing R-matrix or initialize identity"""
        if not self.r_matrix_path.exists():
            print(f"   🔧 Initializing 11×11 R-matrix (identity)")
            return np.eye(11)

        try:
            with open(self.r_matrix_path, 'r') as f:
                memory = json.load(f)

            if 'r_matrix' in memory:
                r_matrix = np.array(memory['r_matrix'])
                if r_matrix.shape == (11, 11):
                    print(f"   ✅ Loaded 11×11 R-matrix from {self.r_matrix_path}")
                    return r_matrix
                elif r_matrix.shape == (5, 5):
                    # Expand legacy 5×5
                    print(f"   ⚠️  Expanding legacy 5×5 R-matrix to 11×11")
                    expanded = np.eye(11)
                    expanded[:5, :5] = r_matrix
                    return expanded

            print(f"   ⚠️  R-matrix not found in file, initializing identity")
            return np.eye(11)

        except Exception as e:
            print(f"   ⚠️  Error loading R-matrix: {e}, initializing identity")
            return np.eye(11)

    def update_coupling(
        self,
        organ_results: Dict[str, Any],
        satisfaction: float,
        verbose: bool = False
    ) -> List[CouplingUpdate]:
        """
        Hebbian update: strengthen coupling between co-active organs.

        DAE 3.0 Formula:
            R(i,j) ← R(i,j) + η · coherence[i] · coherence[j] · satisfaction · (1 - R(i,j))

        Args:
            organ_results: {organ_name: result_object} from V0 cycle
            satisfaction: Mean satisfaction from V0 convergence [0,1]
            verbose: Print coupling updates

        Returns:
            List of CouplingUpdate records
        """
        updates = []

        # Extract organ coherences
        coherences = {}
        for organ_name, result in organ_results.items():
            if organ_name in self.organ_names:
                coherence = getattr(result, 'coherence', 0.0)
                coherences[organ_name] = coherence

        if verbose:
            print(f"\n   🧬 Updating R-matrix coupling (η={self.eta})...")

        # Update all pairwise couplings
        significant_updates = 0
        for i, organ_i in enumerate(self.organ_names):
            for j in range(i+1, len(self.organ_names)):  # Upper triangle only
                organ_j = self.organ_names[j]

                if organ_i not in coherences or organ_j not in coherences:
                    continue

                coh_i = coherences[organ_i]
                coh_j = coherences[organ_j]

                # Hebbian update (DAE 3.0 style)
                co_activation = coh_i * coh_j * satisfaction

                if self.saturation_enabled:
                    # Saturation term prevents runaway coupling
                    saturation = 1.0 - self.R_matrix[i, j]
                    delta = self.eta * co_activation * saturation
                else:
                    delta = self.eta * co_activation

                # Apply update (symmetric)
                self.R_matrix[i, j] += delta
                self.R_matrix[j, i] = self.R_matrix[i, j]  # Maintain symmetry

                # Clamp to [0, 1]
                self.R_matrix[i, j] = np.clip(self.R_matrix[i, j], 0.0, 1.0)
                self.R_matrix[j, i] = self.R_matrix[i, j]

                # Record update
                update = CouplingUpdate(
                    organ_i=organ_i,
                    organ_j=organ_j,
                    delta=delta,
                    new_coupling=self.R_matrix[i, j],
                    coherence_i=coh_i,
                    coherence_j=coh_j,
                    satisfaction=satisfaction
                )
                updates.append(update)

                # Track significant updates
                if abs(delta) > 0.01:  # Threshold for significance
                    significant_updates += 1
                    if verbose:
                        print(f"      {organ_i} ↔ {organ_j}: {self.R_matrix[i, j]:.3f} (Δ={delta:+.4f})")

        if verbose and significant_updates > 0:
            print(f"   ✓ {significant_updates} significant coupling updates (|Δ| > 0.01)")
        elif verbose:
            print(f"   ✓ R-matrix updated ({len(updates)} pairs, no significant changes)")

        self.update_history.extend(updates)
        return updates

    def get_coupling(self, organ_i: str, organ_j: str) -> float:
        """Get coupling strength between two organs"""
        try:
            idx_i = self.organ_names.index(organ_i)
            idx_j = self.organ_names.index(organ_j)
            return float(self.R_matrix[idx_i, idx_j])
        except (ValueError, IndexError):
            return 0.0

    def get_top_couplings(self, top_n: int = 10) -> List[tuple]:
        """
        Get strongest organ couplings (excluding diagonal).

        Returns:
            [(organ_i, organ_j, coupling_strength), ...]
        """
        couplings = []
        for i in range(len(self.organ_names)):
            for j in range(i+1, len(self.organ_names)):
                couplings.append((
                    self.organ_names[i],
                    self.organ_names[j],
                    self.R_matrix[i, j]
                ))

        # Sort by coupling strength
        couplings.sort(key=lambda x: x[2], reverse=True)
        return couplings[:top_n]

    def save(self):
        """Save R-matrix to conversational_hebbian_memory.json"""
        # Load existing memory or create new
        if self.r_matrix_path.exists():
            with open(self.r_matrix_path, 'r') as f:
                memory = json.load(f)
        else:
            memory = {}

        # Update R-matrix
        memory['r_matrix'] = self.R_matrix.tolist()

        # Add metadata
        if 'r_matrix_metadata' not in memory:
            memory['r_matrix_metadata'] = {}

        memory['r_matrix_metadata']['shape'] = list(self.R_matrix.shape)
        memory['r_matrix_metadata']['learning_rate'] = self.eta
        memory['r_matrix_metadata']['total_updates'] = len(self.update_history)

        # Save
        with open(self.r_matrix_path, 'w') as f:
            json.dump(memory, f, indent=2)

        print(f"   ✅ Saved R-matrix to {self.r_matrix_path}")

    def get_synergy_report(self) -> Dict[str, Any]:
        """
        Generate report on learned organ synergies.

        Returns:
            {
                'top_couplings': [...],
                'mean_coupling': float,
                'trauma_triad': float,  # BOND+EO+NDAM coupling
                'relational_attunement': float,  # EMPATHY+LISTENING+PRESENCE
                ...
            }
        """
        top_couplings = self.get_top_couplings(10)

        # Compute known synergy groups (from DAE 3.0 insights)
        trauma_triad = np.mean([
            self.get_coupling('BOND', 'EO'),
            self.get_coupling('BOND', 'NDAM'),
            self.get_coupling('EO', 'NDAM')
        ])

        relational_attunement = np.mean([
            self.get_coupling('EMPATHY', 'LISTENING'),
            self.get_coupling('EMPATHY', 'PRESENCE'),
            self.get_coupling('LISTENING', 'PRESENCE')
        ])

        coherence_integration = np.mean([
            self.get_coupling('SANS', 'WISDOM'),
            self.get_coupling('SANS', 'CARD')
        ])

        # Overall statistics
        upper_triangle = []
        for i in range(len(self.organ_names)):
            for j in range(i+1, len(self.organ_names)):
                upper_triangle.append(self.R_matrix[i, j])

        return {
            'top_couplings': [
                {'organs': f"{org_i} ↔ {org_j}", 'strength': strength}
                for org_i, org_j, strength in top_couplings
            ],
            'mean_coupling': float(np.mean(upper_triangle)),
            'std_coupling': float(np.std(upper_triangle)),
            'max_coupling': float(np.max(upper_triangle)),
            'synergy_groups': {
                'trauma_triad': float(trauma_triad),
                'relational_attunement': float(relational_attunement),
                'coherence_integration': float(coherence_integration)
            },
            'total_updates': len(self.update_history)
        }


# Quick test
if __name__ == '__main__':
    print("🧪 Testing OrganCouplingLearner...")

    # Initialize
    learner = OrganCouplingLearner(learning_rate=0.05)

    # Simulate organ results (mock)
    class MockResult:
        def __init__(self, coherence):
            self.coherence = coherence

    organ_results = {
        'BOND': MockResult(0.8),
        'EO': MockResult(0.75),
        'NDAM': MockResult(0.7),
        'EMPATHY': MockResult(0.6),
        'LISTENING': MockResult(0.65)
    }

    # Update coupling
    updates = learner.update_coupling(
        organ_results=organ_results,
        satisfaction=0.85,
        verbose=True
    )

    print(f"\n✅ {len(updates)} coupling pairs updated")
    print(f"   Top couplings:")
    for org_i, org_j, strength in learner.get_top_couplings(5):
        print(f"      {org_i} ↔ {org_j}: {strength:.3f}")

    # Synergy report
    report = learner.get_synergy_report()
    print(f"\n📊 Synergy Report:")
    print(f"   Mean coupling: {report['mean_coupling']:.3f}")
    print(f"   Trauma triad (BOND+EO+NDAM): {report['synergy_groups']['trauma_triad']:.3f}")
    print(f"   Relational attunement (EMPATHY+LISTENING+PRESENCE): {report['synergy_groups']['relational_attunement']:.3f}")

    print("\n✅ OrganCouplingLearner test complete!")
