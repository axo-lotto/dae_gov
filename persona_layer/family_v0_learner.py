"""
Family V0 Target Learning
=========================

Implements DAE 3.0 Fractal Level 4 (Family Learning):
Each organic family learns its optimal V0 energy convergence target.

Key Insight from DAE 3.0:
- Different task families converge optimally at different V0 levels
- Learning V0 targets speeds convergence and improves satisfaction
- Per-family optimization enables adaptive processing

Mathematical Formulation (DAE 3.0):
    V0_target[family] = median{V0_converged | conversations ∈ family}

    Update rule:
    If satisfaction > 0.8:
        new_target = current_target + α * (V0_observed - current_target)

Our Implementation (HYPHAE 1):
    Track V0 history per family
    Learn optimal target via EMA
    Use target to guide V0 descent during processing
    Optimize organ weights per family

Date: November 12, 2025
Status: DAE 3.0 Integration - Fractal Level 4
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class FamilyV0State:
    """V0 learning state for a family"""
    family_id: str
    target_v0: float  # Learned optimal V0 convergence point
    v0_history: List[float]  # Recent V0 observations
    satisfaction_history: List[float]  # Corresponding satisfactions
    convergence_cycles_mean: float  # Average cycles to converge
    organ_weights: Dict[str, float]  # Learned organ importance weights
    total_updates: int


class FamilyV0Learner:
    """
    Learns optimal V0 convergence targets per organic family.

    Implements DAE 3.0 Fractal Level 4:
    - Micro (Level 1): Phrase patterns
    - Organ (Level 2): Organ weights
    - Coupling (Level 3): R-matrix
    - **Family (Level 4): THIS MODULE - Per-family optimization** ⭐
    - Global (Level 7): Organism confidence
    """

    def __init__(
        self,
        families_path: Path = Path("persona_layer/state/active/organic_families.json"),
        learning_rate: float = 0.1,
        history_window: int = 20,
        organ_learning_rate: float = 0.05,
        use_gradient_weights: bool = True
    ):
        """
        Initialize family V0 learner.

        Args:
            families_path: Path to organic_families.json
            learning_rate: EMA learning rate α for target updates
            history_window: Number of recent observations to track
            organ_learning_rate: Gradient learning rate η for organ weights
            use_gradient_weights: Use gradient-based (True) or EMA (False) for organ weights
        """
        self.families_path = families_path
        self.alpha = learning_rate
        self.history_window = history_window
        self.organ_learning_rate = organ_learning_rate
        self.use_gradient_weights = use_gradient_weights

        # Family V0 states
        self.family_states: Dict[str, FamilyV0State] = {}

        # Load existing families
        self._load_families()

    def _load_families(self):
        """Load organic families and initialize V0 states"""
        if not self.families_path.exists():
            print(f"   ⚠️  Families file not found: {self.families_path}")
            return

        try:
            with open(self.families_path, 'r') as f:
                data = json.load(f)

            families = data.get('families', {})

            for family_id, family_data in families.items():
                # Initialize or load V0 state
                if 'v0_learning_state' in family_data:
                    # Load existing state
                    state_data = family_data['v0_learning_state']
                    self.family_states[family_id] = FamilyV0State(
                        family_id=family_id,
                        target_v0=state_data.get('target_v0', 0.5),
                        v0_history=state_data.get('v0_history', []),
                        satisfaction_history=state_data.get('satisfaction_history', []),
                        convergence_cycles_mean=state_data.get('convergence_cycles_mean', 3.0),
                        organ_weights=state_data.get('organ_weights', {}),
                        total_updates=state_data.get('total_updates', 0)
                    )
                else:
                    # Initialize new state
                    self.family_states[family_id] = FamilyV0State(
                        family_id=family_id,
                        target_v0=0.5,  # Default target (middle of range)
                        v0_history=[],
                        satisfaction_history=[],
                        convergence_cycles_mean=3.0,
                        organ_weights={},  # Will be populated from family data
                        total_updates=0
                    )

                    # Initialize organ weights from family if available
                    if 'organ_activation_means' in family_data:
                        self.family_states[family_id].organ_weights = family_data['organ_activation_means'].copy()

            print(f"   ✅ Loaded V0 states for {len(self.family_states)} families")

        except Exception as e:
            print(f"   ⚠️  Error loading families: {e}")

    def _compute_organ_gradients(
        self,
        organ_coherences: Dict[str, float],
        r_matrix_coupling: float
    ) -> Dict[str, float]:
        """
        Compute gradient-based updates for organ weights.

        DAE 3.0 Formula (Fractal Level 2):
            ∂R₂/∂w[organ] = (coherence[organ] - mean_coherence) * R₃

        Args:
            organ_coherences: {organ: coherence} dict
            r_matrix_coupling: Mean R-matrix coupling strength (R₃)

        Returns:
            {organ: gradient} dict
        """
        if not organ_coherences:
            return {}

        # Compute mean coherence
        mean_coherence = np.mean(list(organ_coherences.values()))

        # Compute gradients: (coherence - mean) * R₃
        gradients = {}
        for organ, coherence in organ_coherences.items():
            deviation = coherence - mean_coherence
            gradients[organ] = deviation * r_matrix_coupling

        return gradients

    def update_family_v0(
        self,
        family_id: str,
        v0_final: float,
        satisfaction: float,
        convergence_cycles: int,
        organ_coherences: Dict[str, float],
        r_matrix_coupling: float = 0.0,
        verbose: bool = False
    ):
        """
        Update family V0 target based on observed convergence.

        DAE 3.0 Formulas:
            V0 Target (Fractal Level 4):
                If satisfaction > 0.8:
                    target_v0 ← target_v0 + α * (v0_observed - target_v0)

            Organ Weights (Fractal Level 2):
                Gradient-based:
                    ∂R₂/∂w[organ] = (coherence[organ] - mean_coherence) * R₃
                    w[organ] ← w[organ] + η · ∂R₂/∂w[organ]

                EMA (fallback):
                    w[organ] ← 0.9 * w[organ] + 0.1 * coherence

        Args:
            family_id: Family identifier
            v0_final: Final V0 energy after convergence [0,1]
            satisfaction: Conversation satisfaction [0,1]
            convergence_cycles: Number of cycles to converge
            organ_coherences: {organ: coherence} dict
            r_matrix_coupling: Mean R-matrix coupling strength (for gradients)
            verbose: Print update info
        """
        # Get or create family state
        if family_id not in self.family_states:
            self.family_states[family_id] = FamilyV0State(
                family_id=family_id,
                target_v0=0.5,
                v0_history=[],
                satisfaction_history=[],
                convergence_cycles_mean=3.0,
                organ_weights={},
                total_updates=0
            )

        state = self.family_states[family_id]

        # Add to history (maintain window)
        state.v0_history.append(v0_final)
        state.satisfaction_history.append(satisfaction)
        if len(state.v0_history) > self.history_window:
            state.v0_history.pop(0)
            state.satisfaction_history.pop(0)

        # Update target V0 (only from high-satisfaction conversations)
        if satisfaction > 0.8:
            # EMA update toward observed V0
            delta = self.alpha * (v0_final - state.target_v0)
            state.target_v0 += delta

            # Clamp to reasonable range [0.1, 0.7]
            state.target_v0 = np.clip(state.target_v0, 0.1, 0.7)

            if verbose:
                print(f"   📊 Family {family_id} V0 target: {state.target_v0:.3f} (Δ={delta:+.4f})")

        # Update convergence cycles (EMA)
        state.convergence_cycles_mean = (
            0.8 * state.convergence_cycles_mean +
            0.2 * convergence_cycles
        )

        # Update organ weights
        if self.use_gradient_weights and r_matrix_coupling > 0.0:
            # ✅ DAE 3.0 Gradient-Based Update (Fractal Level 2)
            gradients = self._compute_organ_gradients(
                organ_coherences=organ_coherences,
                r_matrix_coupling=r_matrix_coupling
            )

            for organ, gradient in gradients.items():
                if organ not in state.organ_weights:
                    # Initialize with current coherence
                    state.organ_weights[organ] = organ_coherences[organ]
                else:
                    # Gradient descent update: w ← w + η · gradient
                    state.organ_weights[organ] += self.organ_learning_rate * gradient

                    # Clamp to reasonable range [0, 1]
                    state.organ_weights[organ] = np.clip(state.organ_weights[organ], 0.0, 1.0)

            if verbose and gradients:
                print(f"   📊 Gradient-based organ weight updates:")
                for organ, gradient in sorted(gradients.items(), key=lambda x: abs(x[1]), reverse=True)[:3]:
                    print(f"      {organ}: gradient={gradient:+.4f}, weight={state.organ_weights[organ]:.3f}")

        else:
            # ⚠️ EMA Fallback (when R-matrix coupling not available)
            for organ, coherence in organ_coherences.items():
                if organ not in state.organ_weights:
                    state.organ_weights[organ] = coherence
                else:
                    # EMA update
                    state.organ_weights[organ] = (
                        0.9 * state.organ_weights[organ] +
                        0.1 * coherence
                    )

            if verbose:
                print(f"   ⚠️  Using EMA fallback for organ weights (no R-matrix coupling)")

        state.total_updates += 1

    def get_v0_target(self, family_id: str) -> float:
        """
        Get learned V0 target for family.

        Returns:
            Target V0 energy to guide convergence
        """
        if family_id in self.family_states:
            return self.family_states[family_id].target_v0
        return 0.5  # Default if family not found

    def get_organ_weights(self, family_id: str) -> Dict[str, float]:
        """
        Get learned organ importance weights for family.

        Returns:
            {organ: weight} dict, normalized to mean=1.0
        """
        if family_id not in self.family_states:
            return {}

        weights = self.family_states[family_id].organ_weights.copy()

        # Normalize to mean=1.0 (for modulation purposes)
        if weights:
            mean_weight = np.mean(list(weights.values()))
            if mean_weight > 0:
                weights = {org: w / mean_weight for org, w in weights.items()}

        return weights

    def get_family_report(self, family_id: str) -> Dict[str, Any]:
        """
        Generate learning report for family.

        Returns:
            {
                'family_id': str,
                'target_v0': float,
                'v0_mean': float,
                'v0_std': float,
                'satisfaction_mean': float,
                'convergence_cycles_mean': float,
                'total_updates': int,
                'top_organs': [(organ, weight), ...]
            }
        """
        if family_id not in self.family_states:
            return {'family_id': family_id, 'status': 'not_found'}

        state = self.family_states[family_id]

        # Compute statistics
        v0_mean = np.mean(state.v0_history) if state.v0_history else state.target_v0
        v0_std = np.std(state.v0_history) if len(state.v0_history) > 1 else 0.0
        sat_mean = np.mean(state.satisfaction_history) if state.satisfaction_history else 0.0

        # Top organs by weight
        top_organs = sorted(
            state.organ_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            'family_id': family_id,
            'target_v0': state.target_v0,
            'v0_mean': float(v0_mean),
            'v0_std': float(v0_std),
            'satisfaction_mean': float(sat_mean),
            'convergence_cycles_mean': state.convergence_cycles_mean,
            'total_updates': state.total_updates,
            'top_organs': [(org, float(weight)) for org, weight in top_organs],
            'history_length': len(state.v0_history)
        }

    def save(self):
        """Save family V0 states back to organic_families.json"""
        if not self.families_path.exists():
            print(f"   ⚠️  Cannot save: families file not found")
            return

        try:
            # Load existing families
            with open(self.families_path, 'r') as f:
                data = json.load(f)

            families = data.get('families', {})

            # Update each family with V0 learning state
            for family_id, state in self.family_states.items():
                if family_id in families:
                    families[family_id]['v0_learning_state'] = {
                        'target_v0': state.target_v0,
                        'v0_history': state.v0_history[-self.history_window:],  # Keep recent only
                        'satisfaction_history': state.satisfaction_history[-self.history_window:],
                        'convergence_cycles_mean': state.convergence_cycles_mean,
                        'organ_weights': state.organ_weights,
                        'total_updates': state.total_updates
                    }

            # Save
            data['families'] = families
            with open(self.families_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"   ✅ Saved V0 learning states for {len(self.family_states)} families")

        except Exception as e:
            print(f"   ⚠️  Error saving V0 states: {e}")

    def get_all_families_report(self) -> List[Dict[str, Any]]:
        """Get learning reports for all families"""
        return [
            self.get_family_report(family_id)
            for family_id in sorted(self.family_states.keys())
        ]


# Quick test
if __name__ == '__main__':
    print("🧪 Testing FamilyV0Learner...")

    # Initialize
    learner = FamilyV0Learner(
        families_path=Path("persona_layer/organic_families.json"),
        learning_rate=0.1
    )

    # Simulate family learning
    family_id = "Family_001"

    print(f"\n📊 Initial state for {family_id}:")
    initial_report = learner.get_family_report(family_id)
    print(f"   Target V0: {initial_report['target_v0']:.3f}")
    print(f"   Total updates: {initial_report['total_updates']}")

    # Simulate 5 conversations
    print(f"\n🗣️  Simulating 5 conversations...")
    for i in range(5):
        v0_final = 0.25 + np.random.uniform(-0.05, 0.05)
        satisfaction = 0.85 + np.random.uniform(-0.05, 0.05)
        cycles = np.random.randint(2, 4)

        organ_coherences = {
            'LISTENING': 0.7 + np.random.uniform(-0.1, 0.1),
            'EMPATHY': 0.8 + np.random.uniform(-0.1, 0.1),
            'PRESENCE': 0.75 + np.random.uniform(-0.1, 0.1)
        }

        learner.update_family_v0(
            family_id=family_id,
            v0_final=v0_final,
            satisfaction=satisfaction,
            convergence_cycles=cycles,
            organ_coherences=organ_coherences,
            verbose=True
        )

    # Final state
    print(f"\n📊 Final state for {family_id}:")
    final_report = learner.get_family_report(family_id)
    print(f"   Target V0: {final_report['target_v0']:.3f} (was {initial_report['target_v0']:.3f})")
    print(f"   V0 mean: {final_report['v0_mean']:.3f} ± {final_report['v0_std']:.3f}")
    print(f"   Satisfaction mean: {final_report['satisfaction_mean']:.3f}")
    print(f"   Convergence cycles: {final_report['convergence_cycles_mean']:.1f}")
    print(f"   Total updates: {final_report['total_updates']}")

    print(f"\n   Top organs:")
    for organ, weight in final_report['top_organs']:
        print(f"      • {organ}: {weight:.3f}")

    # Save
    learner.save()

    print("\n✅ FamilyV0Learner test complete!")
