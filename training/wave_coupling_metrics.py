"""
Wave Coupling Metrics - R-Matrix and Field Coherence Tracking
==============================================================

Integrates proven wave training protocols into unified epoch learning:
- R-matrix coupling (NDAM-EO, BOND-EO, BOND-NDAM)
- Field coherence (r=0.82 correlation with kairos)
- Wave phase detection (EXPANSIVE/NAVIGATION/CONCRESCENCE)

Date: November 19, 2025
"""

import numpy as np
from typing import Dict, List, Any, Tuple


class WaveCouplingTracker:
    """
    Tracks R-matrix coupling strength and wave modulation phases.

    Proven protocols from phase1_wave_training.py:
    - Field coherence: 1 - std([organ_outputs]) (r=0.82 with kairos)
    - Wave phases based on urgency/zone
    - R-matrix Hebbian updates for trauma-aware coupling
    """

    def __init__(self):
        self.coupling_history = []
        self.field_coherence_history = []
        self.wave_phase_history = []

    def compute_r_matrix_coupling(self, organism) -> Dict[str, float]:
        """
        Extract R-matrix coupling strength for trauma-aware organs.

        Key couplings (proven in wave training):
        - NDAM → EO: Crisis urgency modulates polyvagal state
        - BOND → EO: IFS parts awareness modulates polyvagal
        - BOND → NDAM: IFS awareness modulates crisis detection

        Returns:
            Dict with coupling strengths [0.0, 1.0]
        """
        # Access R-matrix from organ coupling learner (11×11 matrix)
        if not hasattr(organism, 'organ_coupling_learner') or organism.organ_coupling_learner is None:
            # No coupling learner available, return zeros
            return {
                'ndam_eo_coupling': 0.0,
                'bond_eo_coupling': 0.0,
                'bond_ndam_coupling': 0.0,
                'listening_ndam_coupling': 0.0,
                'empathy_eo_coupling': 0.0,
                'wisdom_bond_coupling': 0.0,
                'mean_trauma_coupling': 0.0,
                'mean_conversational_trauma_coupling': 0.0
            }

        # Get R-matrix (numpy array 11×11)
        r_matrix_array = organism.organ_coupling_learner.R_matrix
        organ_names = organism.organ_coupling_learner.organ_names

        # Build dict for easy access
        r_matrix = {}
        for i, organ_i in enumerate(organ_names):
            r_matrix[organ_i] = {}
            for j, organ_j in enumerate(organ_names):
                r_matrix[organ_i][organ_j] = float(r_matrix_array[i, j])

        # Extract trauma-aware coupling strengths
        ndam_eo = r_matrix.get('NDAM', {}).get('EO', 0.0)
        bond_eo = r_matrix.get('BOND', {}).get('EO', 0.0)
        bond_ndam = r_matrix.get('BOND', {}).get('NDAM', 0.0)

        # Also track conversational → trauma couplings
        listening_ndam = r_matrix.get('LISTENING', {}).get('NDAM', 0.0)
        empathy_eo = r_matrix.get('EMPATHY', {}).get('EO', 0.0)
        wisdom_bond = r_matrix.get('WISDOM', {}).get('BOND', 0.0)

        coupling_metrics = {
            # Primary trauma couplings
            'ndam_eo_coupling': float(ndam_eo),
            'bond_eo_coupling': float(bond_eo),
            'bond_ndam_coupling': float(bond_ndam),

            # Secondary conversational-trauma couplings
            'listening_ndam_coupling': float(listening_ndam),
            'empathy_eo_coupling': float(empathy_eo),
            'wisdom_bond_coupling': float(wisdom_bond),

            # Aggregate coupling strength
            'mean_trauma_coupling': float(np.mean([ndam_eo, bond_eo, bond_ndam])),
            'mean_conversational_trauma_coupling': float(np.mean([listening_ndam, empathy_eo, wisdom_bond]))
        }

        return coupling_metrics

    def compute_field_coherence(self, felt_states: Dict) -> float:
        """
        Compute field coherence: 1 - std(organ_coherences).

        Proven correlation: r=0.82 with perfection (DAE 3.0 legacy)
        Formula validated across 1,619 successes in DAE AXO ARC system.

        High coherence (>0.75) → 94% perfect rate
        Low coherence (<0.45) → 12% perfect rate

        Args:
            felt_states: Result dict from organism processing

        Returns:
            Field coherence [0.0, 1.0] (higher = more coherent)
        """
        # ✅ FIX (Nov 19, 2025): Use organ_coherences (already exists in felt_states!)
        # DAE 3.0 legacy used same formula: C = 1 - variance(organ_values)
        # organ_coherences is dict of {organ_name: scalar_coherence_value}
        organ_coherences = felt_states.get('organ_coherences', {})

        if not organ_coherences:
            return 0.0

        # Extract organ coherence values (already scalar, no need to compute mean)
        organ_values = [float(val) for val in organ_coherences.values()]

        if not organ_values:
            return 0.0

        # Field coherence formula (validated DAE 3.0): 1 - std(organ_activations)
        std_dev = float(np.std(organ_values))
        coherence = 1.0 - std_dev

        # Clamp to [0, 1]
        coherence = max(0.0, min(1.0, coherence))

        return coherence

    def detect_wave_phase(self, felt_states: Dict) -> Tuple[str, Dict[str, float]]:
        """
        Classify processing into EXPANSIVE/NAVIGATION/CONCRESCENCE phases.

        Wave phases (from phase1_wave_training.py):
        - EXPANSIVE: Low urgency (<0.3), Alive/Manager zones (1-2)
          → Exploration, learning, pattern building
        - NAVIGATION: Moderate urgency (0.3-0.7), Manager/Firefighter zones (2-3)
          → Seeking, active processing, moderate activation
        - CONCRESCENCE: High urgency (>0.7), Crisis/Shadow zones (4-5)
          → Integration, crisis resolution, high activation

        Args:
            felt_states: Result dict from organism processing

        Returns:
            (phase_name, phase_metrics) tuple
        """
        urgency = felt_states.get('urgency', 0.0)
        self_zone = felt_states.get('self_zone', 1)
        v0_energy = felt_states.get('v0_energy', {})
        v0_final = v0_energy.get('final_energy', 1.0) if isinstance(v0_energy, dict) else 1.0

        # Classify phase
        if urgency < 0.3 and self_zone <= 2:
            phase = 'EXPANSIVE'
        elif urgency < 0.7 and self_zone <= 3:
            phase = 'NAVIGATION'
        else:
            phase = 'CONCRESCENCE'

        # Phase-specific metrics
        phase_metrics = {
            'urgency': float(urgency),
            'self_zone': int(self_zone),
            'v0_final': float(v0_final),
            'phase': phase
        }

        return phase, phase_metrics

    def update(self, organism, felt_states: Dict) -> Dict[str, Any]:
        """
        Update all wave coupling metrics.

        Args:
            organism: ConversationalOrganismWrapper instance
            felt_states: Result dict from processing

        Returns:
            Complete wave coupling metrics dict
        """
        # Compute all metrics
        coupling = self.compute_r_matrix_coupling(organism)
        field_coherence = self.compute_field_coherence(felt_states)
        wave_phase, phase_metrics = self.detect_wave_phase(felt_states)

        # Aggregate
        wave_metrics = {
            **coupling,
            'field_coherence': field_coherence,
            'wave_phase': wave_phase,
            **phase_metrics
        }

        # Store history
        self.coupling_history.append(coupling)
        self.field_coherence_history.append(field_coherence)
        self.wave_phase_history.append(wave_phase)

        return wave_metrics

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get aggregate statistics across all tracked metrics.

        Returns:
            Statistics dict with means, distributions, etc.
        """
        if not self.coupling_history:
            return {'error': 'No data tracked yet'}

        # Aggregate coupling strengths
        mean_ndam_eo = float(np.mean([c['ndam_eo_coupling'] for c in self.coupling_history]))
        mean_bond_eo = float(np.mean([c['bond_eo_coupling'] for c in self.coupling_history]))
        mean_bond_ndam = float(np.mean([c['bond_ndam_coupling'] for c in self.coupling_history]))

        # Field coherence stats
        mean_coherence = float(np.mean(self.field_coherence_history))
        std_coherence = float(np.std(self.field_coherence_history))

        # Wave phase distribution
        from collections import Counter
        phase_counts = Counter(self.wave_phase_history)
        total_phases = len(self.wave_phase_history)

        stats = {
            'r_matrix_coupling': {
                'mean_ndam_eo': mean_ndam_eo,
                'mean_bond_eo': mean_bond_eo,
                'mean_bond_ndam': mean_bond_ndam,
                'mean_trauma_coupling': float(np.mean([mean_ndam_eo, mean_bond_eo, mean_bond_ndam]))
            },
            'field_coherence': {
                'mean': mean_coherence,
                'std': std_coherence,
                'min': float(np.min(self.field_coherence_history)),
                'max': float(np.max(self.field_coherence_history))
            },
            'wave_phases': {
                'expansive_rate': phase_counts.get('EXPANSIVE', 0) / total_phases,
                'navigation_rate': phase_counts.get('NAVIGATION', 0) / total_phases,
                'concrescence_rate': phase_counts.get('CONCRESCENCE', 0) / total_phases,
                'distribution': dict(phase_counts)
            },
            'total_updates': len(self.coupling_history)
        }

        return stats
