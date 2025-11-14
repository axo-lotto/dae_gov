"""
Transduction Trajectory Analyzer
=================================

Analyzes transduction trajectories from felt_states for learning insights.

Purpose:
- Extract transduction patterns from TSK records
- Compute healing vs crisis pathway ratios
- Track nexus type distributions
- Identify common transduction sequences
- Generate trajectory visualization data

Date: November 12, 2025
Status: Phase T4 Implementation
"""

from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import numpy as np


class TransductionTrajectoryAnalyzer:
    """
    Analyze transduction trajectories for learning insights.

    Extracts patterns from transduction_trajectory data in felt_states:
    - Nexus type distributions
    - Healing vs crisis pathway ratios
    - Common transduction sequences
    - Mutual satisfaction trends
    - Rhythm coherence patterns
    """

    def __init__(self):
        """Initialize trajectory analyzer."""

        # Pathway classifications
        self.healing_mechanisms = {
            'salience_recalibration',
            'ontological_rebinding',
            'salience_realignment',
            'recursive_grounding',
            'deepening_attunement',
            'boundary_softening'
        }

        self.crisis_mechanisms = {
            'incoherent_broadcasting',
            'projective_ingression',
            'field_hijacking',
            'crisis_escalation'
        }

        self.protective_mechanisms = {
            'contrast_reestablishment',
            'boundary_fortification',
            'pattern_reinforcement',
            'pattern_softening'
        }

        # Nexus type classifications
        self.crisis_nexus_types = {
            'Paradox', 'Dissociative', 'Disruptive',
            'Recursive', 'Looped', 'Urgency'
        }

        self.constitutional_nexus_types = {
            'Pre-Existing', 'Innate', 'Contrast', 'Relational',
            'Fragmented', 'Protective', 'Absorbed', 'Isolated'
        }

    def analyze_trajectory(
        self,
        transduction_trajectory: List[Dict]
    ) -> Dict:
        """
        Analyze a single transduction trajectory.

        Args:
            transduction_trajectory: List of transduction states from felt_states

        Returns:
            Analysis dict with metrics and patterns
        """
        if not transduction_trajectory:
            return {
                'trajectory_length': 0,
                'nexus_types': [],
                'mechanisms': [],
                'healing_ratio': 0.0,
                'crisis_ratio': 0.0,
                'protective_ratio': 0.0,
                'mean_mutual_satisfaction': 0.0,
                'mean_rhythm_coherence': 0.0,
                'final_nexus_type': None,
                'final_is_crisis': False,
                'transduction_occurred': False
            }

        # Extract data
        nexus_types = [state['current_type'] for state in transduction_trajectory]
        mechanisms = [state.get('transition_mechanism', 'maintain')
                     for state in transduction_trajectory]
        mutual_satisfactions = [state.get('mutual_satisfaction', 0.0)
                               for state in transduction_trajectory]
        rhythm_coherences = [state.get('rhythm_coherence', 0.0)
                            for state in transduction_trajectory]

        # Pathway classification
        healing_count = sum(1 for m in mechanisms if m in self.healing_mechanisms)
        crisis_count = sum(1 for m in mechanisms if m in self.crisis_mechanisms)
        protective_count = sum(1 for m in mechanisms if m in self.protective_mechanisms)

        total_pathways = healing_count + crisis_count + protective_count

        if total_pathways > 0:
            healing_ratio = healing_count / total_pathways
            crisis_ratio = crisis_count / total_pathways
            protective_ratio = protective_count / total_pathways
        else:
            healing_ratio = crisis_ratio = protective_ratio = 0.0

        # Check if any transduction occurred (mechanism != 'maintain')
        transduction_occurred = any(m != 'maintain' for m in mechanisms)

        # Final state
        final_state = transduction_trajectory[-1]

        return {
            'trajectory_length': len(transduction_trajectory),
            'nexus_types': nexus_types,
            'mechanisms': mechanisms,
            'healing_ratio': healing_ratio,
            'crisis_ratio': crisis_ratio,
            'protective_ratio': protective_ratio,
            'mean_mutual_satisfaction': np.mean(mutual_satisfactions),
            'mean_rhythm_coherence': np.mean(rhythm_coherences),
            'final_nexus_type': final_state['current_type'],
            'final_is_crisis': final_state.get('is_crisis', False),
            'final_mutual_satisfaction': final_state.get('mutual_satisfaction', 0.0),
            'transduction_occurred': transduction_occurred,
            'pathway_counts': {
                'healing': healing_count,
                'crisis': crisis_count,
                'protective': protective_count
            }
        }

    def analyze_batch(
        self,
        trajectories: List[List[Dict]]
    ) -> Dict:
        """
        Analyze a batch of transduction trajectories.

        Args:
            trajectories: List of transduction trajectories

        Returns:
            Aggregate analysis dict
        """
        if not trajectories:
            return {
                'total_trajectories': 0,
                'mean_trajectory_length': 0.0,
                'transduction_rate': 0.0,
                'healing_ratio': 0.0,
                'crisis_ratio': 0.0,
                'protective_ratio': 0.0,
                'mean_mutual_satisfaction': 0.0,
                'mean_rhythm_coherence': 0.0,
                'nexus_type_distribution': {},
                'mechanism_distribution': {},
                'crisis_to_constitutional_rate': 0.0
            }

        # Analyze each trajectory
        analyses = [self.analyze_trajectory(traj) for traj in trajectories]

        # Aggregate metrics
        total_trajectories = len(analyses)
        trajectories_with_transduction = sum(1 for a in analyses if a['transduction_occurred'])
        transduction_rate = trajectories_with_transduction / total_trajectories

        # Mean trajectory length
        mean_trajectory_length = np.mean([a['trajectory_length'] for a in analyses])

        # Pathway ratios (average across all trajectories)
        healing_ratios = [a['healing_ratio'] for a in analyses if a['transduction_occurred']]
        crisis_ratios = [a['crisis_ratio'] for a in analyses if a['transduction_occurred']]
        protective_ratios = [a['protective_ratio'] for a in analyses if a['transduction_occurred']]

        mean_healing_ratio = np.mean(healing_ratios) if healing_ratios else 0.0
        mean_crisis_ratio = np.mean(crisis_ratios) if crisis_ratios else 0.0
        mean_protective_ratio = np.mean(protective_ratios) if protective_ratios else 0.0

        # Mutual satisfaction and rhythm coherence
        mean_mutual_satisfaction = np.mean([a['mean_mutual_satisfaction'] for a in analyses])
        mean_rhythm_coherence = np.mean([a['mean_rhythm_coherence'] for a in analyses])

        # Nexus type distribution
        nexus_type_counts = defaultdict(int)
        for analysis in analyses:
            for nexus_type in analysis['nexus_types']:
                nexus_type_counts[nexus_type] += 1

        # Mechanism distribution
        mechanism_counts = defaultdict(int)
        for analysis in analyses:
            for mechanism in analysis['mechanisms']:
                mechanism_counts[mechanism] += 1

        # Crisis to constitutional conversion rate
        crisis_start_count = 0
        crisis_to_constitutional_count = 0

        for analysis in analyses:
            if analysis['nexus_types'] and analysis['nexus_types'][0] in self.crisis_nexus_types:
                crisis_start_count += 1
                if analysis['final_nexus_type'] in self.constitutional_nexus_types:
                    crisis_to_constitutional_count += 1

        crisis_to_constitutional_rate = (
            crisis_to_constitutional_count / crisis_start_count
            if crisis_start_count > 0 else 0.0
        )

        return {
            'total_trajectories': total_trajectories,
            'mean_trajectory_length': mean_trajectory_length,
            'transduction_rate': transduction_rate,
            'healing_ratio': mean_healing_ratio,
            'crisis_ratio': mean_crisis_ratio,
            'protective_ratio': mean_protective_ratio,
            'mean_mutual_satisfaction': mean_mutual_satisfaction,
            'mean_rhythm_coherence': mean_rhythm_coherence,
            'nexus_type_distribution': dict(nexus_type_counts),
            'mechanism_distribution': dict(mechanism_counts),
            'crisis_to_constitutional_rate': crisis_to_constitutional_rate,
            'trajectories_with_transduction': trajectories_with_transduction
        }

    def extract_common_sequences(
        self,
        trajectories: List[List[Dict]],
        min_length: int = 2,
        top_n: int = 5
    ) -> List[Tuple[List[str], int]]:
        """
        Extract common transduction sequences.

        Args:
            trajectories: List of transduction trajectories
            min_length: Minimum sequence length
            top_n: Number of top sequences to return

        Returns:
            List of (sequence, count) tuples
        """
        sequence_counts = defaultdict(int)

        for trajectory in trajectories:
            if len(trajectory) < min_length:
                continue

            # Extract nexus type sequence
            nexus_sequence = tuple(state['current_type'] for state in trajectory)

            # Also extract mechanism sequence
            mechanism_sequence = tuple(
                state.get('transition_mechanism', 'maintain')
                for state in trajectory
            )

            # Count both sequences
            if len(nexus_sequence) >= min_length:
                sequence_counts[('nexus', nexus_sequence)] += 1

            if len(mechanism_sequence) >= min_length:
                sequence_counts[('mechanism', mechanism_sequence)] += 1

        # Sort by count
        sorted_sequences = sorted(
            sequence_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_sequences[:top_n]

    def compute_healing_score(self, trajectory_analysis: Dict) -> float:
        """
        Compute overall healing score for a trajectory.

        Score from -1 (crisis-oriented) to +1 (healing-oriented).

        Args:
            trajectory_analysis: Analysis dict from analyze_trajectory()

        Returns:
            Healing score (-1 to +1)
        """
        if not trajectory_analysis['transduction_occurred']:
            # No transduction → neutral
            return 0.0

        # Pathway contribution
        healing_ratio = trajectory_analysis['healing_ratio']
        crisis_ratio = trajectory_analysis['crisis_ratio']
        protective_ratio = trajectory_analysis['protective_ratio']

        pathway_score = healing_ratio - crisis_ratio  # -1 to +1

        # Final state contribution
        final_is_crisis = trajectory_analysis['final_is_crisis']
        final_state_score = -0.5 if final_is_crisis else 0.5

        # Mutual satisfaction contribution
        mutual_satisfaction = trajectory_analysis['mean_mutual_satisfaction']
        satisfaction_score = (mutual_satisfaction - 0.5) * 2  # Map 0-1 to -1 to +1

        # Combined score (weighted)
        healing_score = (
            0.5 * pathway_score +
            0.3 * final_state_score +
            0.2 * satisfaction_score
        )

        return max(-1.0, min(1.0, healing_score))

    def format_trajectory_summary(
        self,
        trajectory: List[Dict],
        include_vocabulary: bool = False
    ) -> str:
        """
        Format trajectory as human-readable summary.

        Args:
            trajectory: Transduction trajectory
            include_vocabulary: Include transductive vocabulary metrics

        Returns:
            Formatted summary string
        """
        if not trajectory:
            return "No transduction trajectory"

        lines = []
        lines.append("Transduction Trajectory:")
        lines.append("-" * 60)

        for i, state in enumerate(trajectory):
            cycle = state.get('cycle_num', i)
            nexus_type = state['current_type']
            mechanism = state.get('transition_mechanism', 'maintain')
            next_type = state.get('next_type', nexus_type)
            v0_energy = state.get('v0_energy', 0.0)
            satisfaction = state.get('satisfaction', 0.0)
            mutual_satisfaction = state.get('mutual_satisfaction', 0.0)

            lines.append(f"Cycle {cycle}: {nexus_type}")
            lines.append(f"  V0: {v0_energy:.3f}, Satisfaction: {satisfaction:.3f}")
            lines.append(f"  Mutual Satisfaction: {mutual_satisfaction:.3f}")

            if mechanism != 'maintain':
                lines.append(f"  → {next_type} (via {mechanism})")

            if include_vocabulary:
                signal_inflation = state.get('signal_inflation', 0.0)
                salience_drift = state.get('salience_drift', 0.0)
                prehensive_overload = state.get('prehensive_overload', 0.0)
                coherence_leakage = state.get('coherence_leakage', 0.0)

                lines.append(f"  Vocabulary:")
                lines.append(f"    Signal Inflation: {signal_inflation:.3f}")
                lines.append(f"    Salience Drift: {salience_drift:.3f}")
                lines.append(f"    Prehensive Overload: {prehensive_overload:.3f}")
                lines.append(f"    Coherence Leakage: {coherence_leakage:.3f}")

            lines.append("")

        return "\n".join(lines)

    def generate_trajectory_visualization_data(
        self,
        trajectory: List[Dict]
    ) -> Dict:
        """
        Generate data for trajectory visualization.

        Args:
            trajectory: Transduction trajectory

        Returns:
            Dict with visualization data (cycles, nexus_types, mechanisms, metrics)
        """
        if not trajectory:
            return {
                'cycles': [],
                'nexus_types': [],
                'mechanisms': [],
                'v0_energy': [],
                'satisfaction': [],
                'mutual_satisfaction': [],
                'rhythm_coherence': []
            }

        cycles = [state.get('cycle_num', i) for i, state in enumerate(trajectory)]
        nexus_types = [state['current_type'] for state in trajectory]
        mechanisms = [state.get('transition_mechanism', 'maintain') for state in trajectory]
        v0_energies = [state.get('v0_energy', 0.0) for state in trajectory]
        satisfactions = [state.get('satisfaction', 0.0) for state in trajectory]
        mutual_satisfactions = [state.get('mutual_satisfaction', 0.0) for state in trajectory]
        rhythm_coherences = [state.get('rhythm_coherence', 0.0) for state in trajectory]

        return {
            'cycles': cycles,
            'nexus_types': nexus_types,
            'mechanisms': mechanisms,
            'v0_energy': v0_energies,
            'satisfaction': satisfactions,
            'mutual_satisfaction': mutual_satisfactions,
            'rhythm_coherence': rhythm_coherences
        }


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 TRANSDUCTION TRAJECTORY ANALYZER TEST")
    print("="*70)

    # Mock trajectory data
    mock_trajectory = [
        {
            'cycle_num': 1,
            'current_type': 'Urgency',
            'next_type': 'Relational',
            'transition_mechanism': 'salience_recalibration',
            'v0_energy': 0.85,
            'satisfaction': 0.45,
            'mutual_satisfaction': 0.55,
            'rhythm_coherence': 0.52,
            'is_crisis': True,
            'signal_inflation': 0.72,
            'salience_drift': 0.45,
            'prehensive_overload': 0.38,
            'coherence_leakage': 0.55
        },
        {
            'cycle_num': 2,
            'current_type': 'Relational',
            'next_type': 'Innate',
            'transition_mechanism': 'deepening_attunement',
            'v0_energy': 0.42,
            'satisfaction': 0.78,
            'mutual_satisfaction': 0.72,
            'rhythm_coherence': 0.68,
            'is_crisis': False,
            'signal_inflation': 0.35,
            'salience_drift': 0.18,
            'prehensive_overload': 0.22,
            'coherence_leakage': 0.32
        },
        {
            'cycle_num': 3,
            'current_type': 'Innate',
            'next_type': 'Innate',
            'transition_mechanism': 'maintain',
            'v0_energy': 0.15,
            'satisfaction': 0.92,
            'mutual_satisfaction': 0.88,
            'rhythm_coherence': 0.85,
            'is_crisis': False,
            'signal_inflation': 0.18,
            'salience_drift': 0.08,
            'prehensive_overload': 0.12,
            'coherence_leakage': 0.15
        }
    ]

    # Test analyzer
    try:
        analyzer = TransductionTrajectoryAnalyzer()

        # Analyze single trajectory
        analysis = analyzer.analyze_trajectory(mock_trajectory)

        print(f"\n✅ Single Trajectory Analysis:")
        print(f"   Trajectory length: {analysis['trajectory_length']}")
        print(f"   Transduction occurred: {analysis['transduction_occurred']}")
        print(f"   Healing ratio: {analysis['healing_ratio']:.3f}")
        print(f"   Crisis ratio: {analysis['crisis_ratio']:.3f}")
        print(f"   Protective ratio: {analysis['protective_ratio']:.3f}")
        print(f"   Mean mutual satisfaction: {analysis['mean_mutual_satisfaction']:.3f}")
        print(f"   Final nexus: {analysis['final_nexus_type']}")
        print(f"   Final is crisis: {analysis['final_is_crisis']}")

        # Compute healing score
        healing_score = analyzer.compute_healing_score(analysis)
        print(f"   Healing score: {healing_score:.3f} (-1 to +1)")

        # Format summary
        summary = analyzer.format_trajectory_summary(mock_trajectory, include_vocabulary=True)
        print(f"\n📝 Trajectory Summary:")
        print(summary)

        # Generate visualization data
        viz_data = analyzer.generate_trajectory_visualization_data(mock_trajectory)
        print(f"\n📊 Visualization Data:")
        print(f"   Cycles: {viz_data['cycles']}")
        print(f"   Nexus types: {viz_data['nexus_types']}")
        print(f"   Mechanisms: {viz_data['mechanisms']}")

        print(f"\n✅ Trajectory analyzer working correctly!")

    except Exception as e:
        print(f"\n❌ Trajectory analyzer failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
