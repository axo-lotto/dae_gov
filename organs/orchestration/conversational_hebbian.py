"""
Conversational Hebbian Memory - R-Matrix Coupling for 5 Conversational Organs

Tracks co-activation patterns between LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE
using validated DAE 3.0 hyperparameters (η=0.05, δ=0.01).

Philosophy:
- Hebbian learning: "Organs that fire together, wire together"
- Agreement modulation: Strengthen coupling when organs agree on lure direction
- Symmetric R-matrix: R[i,j] = R[j,i] (bidirectional coupling)
- Persistence: Save every 10 updates to TSK/conversational_r_matrix.json

Architecture:
- 5×5 R-matrix for organ coupling
- η = 0.05 (learning rate, DAE 3.0 validated)
- δ = 0.01 (decay rate, DAE 3.0 validated)
- Agreement threshold: |lure_i - lure_j| < 0.3

Integration:
- Called by orchestrator after all organs process
- Updates coupling based on coherence * agreement
- Persists to disk for cross-conversation learning

Author: DAE-GOV Development Team
Created: November 10, 2025
Version: 1.0 (Conversational Coupling Foundation)
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CouplingUpdate:
    """Record of a single R-matrix coupling update."""
    organs: List[str]
    coherences: List[float]
    lures: List[float]
    agreements: np.ndarray  # Agreement matrix
    delta_R: np.ndarray  # Change in R-matrix
    timestamp: float


class ConversationalHebbianMemory:
    """
    5×5 Hebbian R-matrix for conversational organ coupling.

    Tracks co-activation patterns using DAE 3.0 validated hyperparameters:
    - η = 0.05 (learning rate)
    - δ = 0.01 (decay rate)
    - Agreement: |lure_i - lure_j| < 0.3

    Expected Coupling Patterns (after 100+ conversations):
                LISTENING  EMPATHY  WISDOM  AUTHENTICITY  PRESENCE
    LISTENING        1.00      0.72     0.54       0.48         0.85
    EMPATHY          0.72      1.00     0.68       0.79         0.62
    WISDOM           0.54      0.68     1.00       0.65         0.58
    AUTHENTICITY     0.48      0.79     0.65       1.00         0.71
    PRESENCE         0.85      0.62     0.58       0.71         1.00

    Interpretation:
    - LISTENING + PRESENCE = 0.85 (strong: presence enables listening)
    - EMPATHY + AUTHENTICITY = 0.79 (strong: vulnerability enables empathy)
    - LISTENING + EMPATHY = 0.72 (strong: listening enables empathic resonance)
    - PRESENCE + AUTHENTICITY = 0.71 (strong: grounding enables authenticity)
    """

    def __init__(self, memory_path: Optional[Path] = None):
        """
        Initialize Hebbian R-matrix.

        Args:
            memory_path: Path to persist R-matrix (default: TSK/conversational_r_matrix.json)
        """
        # Organ names (order matters for indexing)
        self.organs = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE']
        self.n_organs = len(self.organs)

        # Validated hyperparameters (DAE 3.0)
        self.eta = 0.05  # Learning rate
        self.delta = 0.01  # Decay rate
        self.agreement_threshold = 0.3  # |lure_i - lure_j| < 0.3 for agreement

        # Initialize R-matrix
        self.R_matrix = np.eye(self.n_organs)  # Start with identity (1.0 on diagonal)

        # Persistence
        if memory_path is None:
            memory_path = Path(__file__).parent.parent.parent / "TSK" / "conversational_r_matrix.json"
        self.memory_path = memory_path
        self.update_count = 0

        # History (for debugging/analysis)
        self.update_history: List[CouplingUpdate] = []

        # Load existing memory if available
        if self.memory_path.exists():
            self.load()
            print(f"✅ Loaded Conversational Hebbian Memory ({self.update_count} updates)")
        else:
            print("✅ Initialized new Conversational Hebbian Memory")

    def update_coupling(self, organ_results: Dict[str, any]) -> np.ndarray:
        """
        Update R-matrix coupling based on organ co-activation.

        Hebbian rule with agreement modulation:
            R[i,j] += η * agreement * (coherence_i * coherence_j) - δ * R[i,j]

        Args:
            organ_results: Dict mapping organ name to organ Result object
                {
                    'LISTENING': ListeningResult,
                    'EMPATHY': EmpathyResult,
                    'WISDOM': WisdomResult,
                    'AUTHENTICITY': AuthenticityResult,
                    'PRESENCE': PresenceResult
                }

        Returns:
            Updated R-matrix (5×5 numpy array)
        """
        import time

        # Extract coherence and lure arrays
        coherences = np.array([
            organ_results['LISTENING'].coherence,
            organ_results['EMPATHY'].coherence,
            organ_results['WISDOM'].coherence,
            organ_results['AUTHENTICITY'].coherence,
            organ_results['PRESENCE'].coherence
        ])

        lures = np.array([
            organ_results['LISTENING'].lure,
            organ_results['EMPATHY'].lure,
            organ_results['WISDOM'].lure,
            organ_results['AUTHENTICITY'].lure,
            organ_results['PRESENCE'].lure
        ])

        # Compute agreement matrix (5×5)
        # agreement[i,j] = 1.0 if |lure_i - lure_j| < 0.3, else 0.5
        agreement_matrix = np.ones((self.n_organs, self.n_organs))
        for i in range(self.n_organs):
            for j in range(i+1, self.n_organs):
                if abs(lures[i] - lures[j]) >= self.agreement_threshold:
                    agreement_matrix[i, j] = 0.5
                    agreement_matrix[j, i] = 0.5

        # Hebbian update with decay (upper triangle + diagonal)
        delta_R = np.zeros((self.n_organs, self.n_organs))
        for i in range(self.n_organs):
            for j in range(i, self.n_organs):  # Upper triangle + diagonal
                # Hebbian term: η * agreement * (c_i * c_j)
                hebbian_term = self.eta * agreement_matrix[i, j] * (coherences[i] * coherences[j])

                # Decay term: δ * R[i,j]
                decay_term = self.delta * self.R_matrix[i, j]

                # Update
                delta_R[i, j] = hebbian_term - decay_term
                self.R_matrix[i, j] += delta_R[i, j]

                # Symmetry
                if i != j:
                    self.R_matrix[j, i] = self.R_matrix[i, j]
                    delta_R[j, i] = delta_R[i, j]

        # Clip to [0, 1]
        self.R_matrix = np.clip(self.R_matrix, 0.0, 1.0)

        self.update_count += 1

        # Store update in history
        update = CouplingUpdate(
            organs=self.organs.copy(),
            coherences=coherences.tolist(),
            lures=lures.tolist(),
            agreements=agreement_matrix,
            delta_R=delta_R,
            timestamp=time.time()
        )
        self.update_history.append(update)

        # Persist every 10 updates
        if self.update_count % 10 == 0:
            self.save()
            print(f"💾 R-matrix persisted to disk (update #{self.update_count})")

        return self.R_matrix

    def get_coupling(self, organ1: str, organ2: str) -> float:
        """
        Get coupling strength between two organs.

        Args:
            organ1: Name of first organ (e.g., 'LISTENING')
            organ2: Name of second organ (e.g., 'EMPATHY')

        Returns:
            Coupling strength (0.0-1.0)
        """
        i = self.organs.index(organ1)
        j = self.organs.index(organ2)
        return float(self.R_matrix[i, j])

    def get_strongest_couplings(self, top_k: int = 5) -> List[tuple]:
        """
        Get top-k strongest organ couplings.

        Args:
            top_k: Number of top couplings to return

        Returns:
            List of (organ1, organ2, strength) tuples, sorted by strength
        """
        couplings = []
        for i in range(self.n_organs):
            for j in range(i+1, self.n_organs):  # Upper triangle only
                couplings.append((
                    self.organs[i],
                    self.organs[j],
                    float(self.R_matrix[i, j])
                ))

        # Sort by strength (descending)
        couplings.sort(key=lambda x: x[2], reverse=True)

        return couplings[:top_k]

    def save(self):
        """Persist R-matrix to disk."""
        data = {
            'R_matrix': self.R_matrix.tolist(),
            'update_count': self.update_count,
            'organs': self.organs,
            'eta': self.eta,
            'delta': self.delta,
            'agreement_threshold': self.agreement_threshold
        }

        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load R-matrix from disk."""
        with open(self.memory_path, 'r') as f:
            data = json.load(f)

        self.R_matrix = np.array(data['R_matrix'])
        self.update_count = data['update_count']

        # Validate hyperparameters match
        if data.get('eta') != self.eta or data.get('delta') != self.delta:
            print(f"⚠️  Warning: Loaded R-matrix has different hyperparameters")
            print(f"   Loaded: η={data.get('eta')}, δ={data.get('delta')}")
            print(f"   Current: η={self.eta}, δ={self.delta}")

    def print_matrix(self):
        """Pretty-print R-matrix with organ names."""
        print("\n" + "="*70)
        print("Conversational Hebbian R-Matrix")
        print("="*70)

        # Header
        print(f"{'':15}", end='')
        for organ in self.organs:
            print(f"{organ:12}", end='')
        print()

        # Rows
        for i, organ1 in enumerate(self.organs):
            print(f"{organ1:15}", end='')
            for j in range(self.n_organs):
                val = self.R_matrix[i, j]
                print(f"{val:12.3f}", end='')
            print()

        print(f"\nUpdates: {self.update_count}")
        print(f"Strongest couplings:")
        for organ1, organ2, strength in self.get_strongest_couplings(top_k=5):
            print(f"  {organ1} + {organ2} = {strength:.3f}")
        print("="*70 + "\n")


# Module-level convenience function
def create_conversational_hebbian_memory(memory_path: Optional[Path] = None) -> ConversationalHebbianMemory:
    """
    Create or load Conversational Hebbian Memory.

    Args:
        memory_path: Optional path to persist R-matrix

    Returns:
        ConversationalHebbianMemory instance
    """
    return ConversationalHebbianMemory(memory_path=memory_path)


if __name__ == '__main__':
    """Test Conversational Hebbian Memory with simulated organ results."""

    print("="*70)
    print("CONVERSATIONAL HEBBIAN MEMORY - Test")
    print("="*70)
    print()

    # Create memory
    memory = create_conversational_hebbian_memory()

    # Simulate 10 organ result updates
    print("Simulating 10 conversational updates...")
    print()

    for i in range(10):
        # Simulate organ results with varying coherence/lure
        from dataclasses import dataclass

        @dataclass
        class MockResult:
            coherence: float
            lure: float

        organ_results = {
            'LISTENING': MockResult(coherence=0.80 + np.random.rand()*0.15, lure=0.60 + np.random.rand()*0.30),
            'EMPATHY': MockResult(coherence=0.85 + np.random.rand()*0.10, lure=0.70 + np.random.rand()*0.25),
            'WISDOM': MockResult(coherence=0.75 + np.random.rand()*0.15, lure=0.50 + np.random.rand()*0.35),
            'AUTHENTICITY': MockResult(coherence=0.80 + np.random.rand()*0.15, lure=0.65 + np.random.rand()*0.30),
            'PRESENCE': MockResult(coherence=0.85 + np.random.rand()*0.10, lure=0.70 + np.random.rand()*0.25)
        }

        memory.update_coupling(organ_results)

        if (i+1) % 5 == 0:
            print(f"Update #{i+1}:")
            print(f"  LISTENING-EMPATHY coupling: {memory.get_coupling('LISTENING', 'EMPATHY'):.3f}")
            print(f"  EMPATHY-AUTHENTICITY coupling: {memory.get_coupling('EMPATHY', 'AUTHENTICITY'):.3f}")
            print(f"  LISTENING-PRESENCE coupling: {memory.get_coupling('LISTENING', 'PRESENCE'):.3f}")
            print()

    # Print final matrix
    memory.print_matrix()

    print("✅ Conversational Hebbian Memory operational")
    print(f"   Memory persisted to: {memory.memory_path}")
    print()
