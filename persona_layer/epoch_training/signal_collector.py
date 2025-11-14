"""
Signal Collector - Capture All Organism & Learning Signals
===========================================================

Collects comprehensive signals from conversational organism processing
and learning systems for health monitoring and analysis.

**DAE_HYPHAE_1 Architecture** (Phase 2 COMPLETE):
- 11 organs: 5 conversational + 6 trauma/context-aware
- 57D signatures (Phase 3 complete)
- Polyvagal state detection (EO organ)
- Temporal pattern tracking (RNX organ)
- Response scaling (CARD organ)

**Signals Collected**:

From Organism Processing:
1. Organ coherences (11 organs × INPUT/OUTPUT)
   - 5 Conversational: LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE
   - 6 Trauma/Context: BOND, SANS, NDAM, RNX, EO, CARD
2. Mean coherence (aggregate)
3. Satisfaction (final convergence quality)
4. V0 energy (descent from 1.0 → final)
5. BOND self-distance (trauma activation)
6. EO polyvagal state (ventral/sympathetic/dorsal)
7. RNX temporal state (crisis/concrescent/restorative)
8. CARD response scaling (minimal/moderate/comprehensive)
9. Convergence cycles & reason
10. Kairos detection

From Learning Systems:
11. Hebbian patterns (semantic co-activations)
12. Cluster organ weights (per-family learned)
13. Family assignments (57D signature matching)
14. V0 energy targets (learned optimal)
15. Target satisfaction (learned family goals)

November 11, 2025 - Updated for 11-organ Phase 2 architecture
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class SignalCollector:
    """
    Collect all signals from organism processing and learning systems.

    This collector extracts structured data from organism processing results
    (from ConversationalOrganismWrapper) and learning system updates
    (from Hebbian memory, Cluster DB, Family DB) for comprehensive monitoring.
    """

    def __init__(self, bundle_path: str = "Bundle"):
        """
        Initialize signal collector.

        Args:
            bundle_path: Path to Bundle for storage
        """
        self.bundle_path = Path(bundle_path)

    def collect_from_organism_result(
        self,
        organism_result: Dict[str, Any],
        signal_type: str  # 'INPUT' or 'OUTPUT'
    ) -> Dict[str, Any]:
        """
        Collect signals from organism processing result.

        Args:
            organism_result: Result from ConversationalOrganismWrapper.process_text()
                {
                    'mode': 'processing_complete',
                    'felt_states': {...},
                    'tsk_record': {...},
                    'organ_results': {...}
                }
            signal_type: 'INPUT' or 'OUTPUT'

        Returns:
            {
                'type': 'INPUT' | 'OUTPUT',
                'organ_coherences': Dict[str, float],
                'mean_coherence': float,
                'satisfaction': float,
                'v0_energy': {
                    'initial': float,
                    'final': float,
                    'descent_rate': float
                },
                'bond_self_distance': float,
                'eo_polyvagal_state': str,  # NEW: Phase 2
                'rnx_temporal_state': str,  # NEW: Phase 2
                'card_response_scale': str,  # NEW: Phase 2
                'convergence': {
                    'cycles': int,
                    'reason': str,
                    'kairos_cycle_index': Optional[int]
                },
                'phase5_family_id': Optional[str],
                'timestamp': str
            }
        """
        felt_states = organism_result.get('felt_states', {})

        # Extract organ coherences (all 11 organs)
        organ_coherences = felt_states.get('organ_coherences', {})

        # Extract mean coherence
        mean_coherence = felt_states.get('mean_coherence', 0.0)

        # Extract satisfaction
        satisfaction = felt_states.get('satisfaction_final', 0.0)

        # Extract V0 energy
        v0_energy = felt_states.get('v0_energy', {})

        # Extract BOND self-distance (Phase 1)
        bond_self_distance = felt_states.get('bond_self_distance', 0.0)

        # Extract Phase 2 organ signals
        # EO: Polyvagal state detection (ventral_vagal, sympathetic, dorsal_vagal)
        eo_polyvagal_state = felt_states.get('eo_polyvagal_state', 'unknown')

        # RNX: Temporal state tracking (crisis, concrescent, restorative)
        rnx_temporal_state = felt_states.get('rnx_temporal_state', 'unknown')

        # CARD: Response scaling (minimal, moderate, comprehensive)
        card_response_scale = felt_states.get('card_response_scale', 'unknown')

        # Extract convergence metadata
        convergence = {
            'cycles': felt_states.get('convergence_cycles', 1),
            'reason': felt_states.get('convergence_reason', 'unknown'),
            'kairos_cycle_index': felt_states.get('kairos_cycle_index', None)
        }

        # Extract Phase 5 family assignment (57D signatures)
        phase5_family_id = felt_states.get('phase5_family_id', None)

        return {
            'type': signal_type,
            'organ_coherences': organ_coherences,
            'mean_coherence': float(mean_coherence),
            'satisfaction': float(satisfaction),
            'v0_energy': {
                'initial': float(v0_energy.get('initial_energy', 1.0)),
                'final': float(v0_energy.get('final_energy', 0.0)),
                'descent_rate': float(v0_energy.get('energy_descent_rate', 0.0))
            },
            'bond_self_distance': float(bond_self_distance),
            'eo_polyvagal_state': eo_polyvagal_state,  # Phase 2
            'rnx_temporal_state': rnx_temporal_state,  # Phase 2
            'card_response_scale': card_response_scale,  # Phase 2
            'convergence': convergence,
            'phase5_family_id': phase5_family_id,
            'timestamp': datetime.now().isoformat()
        }

    def collect_learning_signals(
        self,
        input_signals: Dict[str, Any],
        output_signals: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Collect learning signals from INPUT→OUTPUT processing.

        Args:
            input_signals: Signals from INPUT processing
            output_signals: Signals from OUTPUT processing
            context: Optional processing context (conversation_id, etc.)

        Returns:
            {
                'hebbian_updates': int,
                'cluster_updates': int,
                'family_assigned': str,
                'family_matured': bool,
                'organ_weight_shifts': Dict[str, float],
                'satisfaction_delta': float,
                'self_distance_reduction': float,
                'v0_energy_delta': float,
                'convergence_speedup': int,
                'timestamp': str
            }
        """
        context = context or {}

        # Compute deltas
        satisfaction_delta = output_signals['satisfaction'] - input_signals['satisfaction']
        self_distance_reduction = input_signals['bond_self_distance'] - output_signals['bond_self_distance']
        v0_energy_delta = input_signals['v0_energy']['final'] - output_signals['v0_energy']['final']
        convergence_speedup = input_signals['convergence']['cycles'] - output_signals['convergence']['cycles']

        # Compute organ weight shifts
        organ_weight_shifts = {}
        for organ in input_signals['organ_coherences'].keys():
            input_coherence = input_signals['organ_coherences'][organ]
            output_coherence = output_signals['organ_coherences'][organ]
            organ_weight_shifts[organ] = output_coherence - input_coherence

        # Placeholder learning signals (actual counts from learning systems)
        # These will be populated by the training pair processor after learning
        learning_signals = {
            'hebbian_updates': 0,  # Populated after Hebbian learning
            'cluster_updates': 0,  # Populated after cluster learning
            'family_assigned': output_signals.get('phase5_family_id', 'unknown'),
            'family_matured': False,  # Populated after family learning
            'organ_weight_shifts': organ_weight_shifts,
            'satisfaction_delta': float(satisfaction_delta),
            'self_distance_reduction': float(self_distance_reduction),
            'v0_energy_delta': float(v0_energy_delta),
            'convergence_speedup': convergence_speedup,
            'timestamp': datetime.now().isoformat()
        }

        return learning_signals

    def create_pair_signal_record(
        self,
        pair_id: str,
        input_signals: Dict[str, Any],
        output_signals: Dict[str, Any],
        learning_signals: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create complete signal record for a training pair.

        Args:
            pair_id: Unique training pair identifier
            input_signals: Signals from INPUT processing
            output_signals: Signals from OUTPUT processing
            learning_signals: Learning system signals
            context: Optional processing context

        Returns:
            Complete signal record for health monitoring and analysis
        """
        context = context or {}

        return {
            'pair_id': pair_id,
            'timestamp': datetime.now().isoformat(),
            'context': context,
            'input_signals': input_signals,
            'output_signals': output_signals,
            'learning_signals': learning_signals,
            'metrics': {
                # Key metrics for quick analysis
                'satisfaction_improvement': learning_signals['satisfaction_delta'],
                'trauma_reduction': learning_signals['self_distance_reduction'],
                'energy_descent': learning_signals['v0_energy_delta'],
                'learning_activity': learning_signals['hebbian_updates'] + learning_signals['cluster_updates']
            }
        }

    def extract_organ_statistics(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract organ statistics from accumulated signals.

        Args:
            signals: List of signal records

        Returns:
            Per-organ statistics (mean, std, trend)
        """
        if not signals:
            return {}

        # Collect per-organ coherences
        organ_coherences = {}
        for signal in signals:
            for signal_type in ['input_signals', 'output_signals']:
                if signal_type in signal:
                    coherences = signal[signal_type].get('organ_coherences', {})
                    for organ, value in coherences.items():
                        if organ not in organ_coherences:
                            organ_coherences[organ] = []
                        organ_coherences[organ].append(value)

        # Compute statistics
        organ_stats = {}
        for organ, values in organ_coherences.items():
            import numpy as np
            organ_stats[organ] = {
                'mean': float(np.mean(values)),
                'std': float(np.std(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'count': len(values)
            }

        return organ_stats

    def extract_family_statistics(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract family assignment statistics.

        Args:
            signals: List of signal records

        Returns:
            Family statistics (total, unique, distribution)
        """
        if not signals:
            return {
                'total_assignments': 0,
                'unique_families': 0,
                'family_distribution': {}
            }

        # Count family assignments
        family_counts = {}
        for signal in signals:
            family_id = signal.get('learning_signals', {}).get('family_assigned', 'unknown')
            if family_id != 'unknown':
                family_counts[family_id] = family_counts.get(family_id, 0) + 1

        return {
            'total_assignments': len(signals),
            'unique_families': len(family_counts),
            'family_distribution': family_counts
        }

    def extract_learning_velocity(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract learning velocity metrics.

        Args:
            signals: List of signal records

        Returns:
            Learning velocity statistics
        """
        if not signals:
            return {
                'hebbian_updates_per_pair': 0.0,
                'cluster_updates_per_pair': 0.0,
                'total_updates': 0,
                'learning_rate': 0.0
            }

        total_hebbian = sum(s.get('learning_signals', {}).get('hebbian_updates', 0) for s in signals)
        total_cluster = sum(s.get('learning_signals', {}).get('cluster_updates', 0) for s in signals)
        total_updates = total_hebbian + total_cluster

        return {
            'hebbian_updates_per_pair': float(total_hebbian / len(signals)),
            'cluster_updates_per_pair': float(total_cluster / len(signals)),
            'total_updates': total_updates,
            'learning_rate': float(total_updates / len(signals))
        }

    def extract_trauma_processing_stats(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract trauma processing statistics.

        Args:
            signals: List of signal records

        Returns:
            Trauma processing statistics
        """
        if not signals:
            return {
                'mean_input_distance': 0.0,
                'mean_output_distance': 0.0,
                'mean_reduction': 0.0,
                'reduction_rate': 0.0
            }

        import numpy as np

        input_distances = [
            s.get('input_signals', {}).get('bond_self_distance', 0.0)
            for s in signals
        ]
        output_distances = [
            s.get('output_signals', {}).get('bond_self_distance', 0.0)
            for s in signals
        ]

        reductions = [
            s.get('learning_signals', {}).get('self_distance_reduction', 0.0)
            for s in signals
        ]

        mean_input = np.mean(input_distances)
        mean_output = np.mean(output_distances)
        mean_reduction = np.mean(reductions)

        return {
            'mean_input_distance': float(mean_input),
            'mean_output_distance': float(mean_output),
            'mean_reduction': float(mean_reduction),
            'reduction_rate': float(mean_reduction / mean_input) if mean_input > 0 else 0.0
        }


def test_signal_collector():
    """
    Test signal collector with simulated organism results.
    """
    print("\n" + "="*70)
    print("🧪 TESTING SIGNAL COLLECTOR")
    print("="*70 + "\n")

    collector = SignalCollector()

    # Simulate INPUT organism result (all 11 organs)
    input_organism_result = {
        'mode': 'processing_complete',
        'felt_states': {
            'organ_coherences': {
                # 5 Conversational Organs
                'LISTENING': 0.65,
                'EMPATHY': 0.72,
                'WISDOM': 0.58,
                'AUTHENTICITY': 0.55,
                'PRESENCE': 0.68,
                # 6 Trauma/Context-Aware Organs (Phase 1 + Phase 2)
                'BOND': 0.45,
                'SANS': 0.52,
                'NDAM': 0.63,
                'RNX': 0.58,   # Phase 2
                'EO': 0.42,    # Phase 2
                'CARD': 0.51   # Phase 2
            },
            'mean_coherence': 0.57,
            'satisfaction_final': 0.60,
            'v0_energy': {
                'initial_energy': 1.0,
                'final_energy': 0.42,
                'energy_descent_rate': 0.58
            },
            'bond_self_distance': 0.85,
            'eo_polyvagal_state': 'sympathetic',  # Phase 2
            'rnx_temporal_state': 'crisis',       # Phase 2
            'card_response_scale': 'minimal',     # Phase 2
            'convergence_cycles': 4,
            'convergence_reason': 'satisfaction',
            'kairos_cycle_index': None,
            'phase5_family_id': None
        }
    }

    # Simulate OUTPUT organism result (all 11 organs)
    output_organism_result = {
        'mode': 'processing_complete',
        'felt_states': {
            'organ_coherences': {
                # 5 Conversational Organs
                'LISTENING': 0.70,
                'EMPATHY': 0.85,
                'WISDOM': 0.65,
                'AUTHENTICITY': 0.62,
                'PRESENCE': 0.75,
                # 6 Trauma/Context-Aware Organs (Phase 1 + Phase 2)
                'BOND': 0.35,
                'SANS': 0.75,
                'NDAM': 0.68,
                'RNX': 0.72,   # Phase 2
                'EO': 0.78,    # Phase 2
                'CARD': 0.80   # Phase 2
            },
            'mean_coherence': 0.70,
            'satisfaction_final': 0.85,
            'v0_energy': {
                'initial_energy': 1.0,
                'final_energy': 0.25,
                'energy_descent_rate': 0.75
            },
            'bond_self_distance': 0.35,
            'eo_polyvagal_state': 'ventral_vagal',  # Phase 2: Safer state
            'rnx_temporal_state': 'restorative',     # Phase 2: Calmer state
            'card_response_scale': 'comprehensive',  # Phase 2: More detailed response
            'convergence_cycles': 2,
            'convergence_reason': 'kairos_moment',
            'kairos_cycle_index': 1,
            'phase5_family_id': 'Family_001'
        }
    }

    # Test 1: Collect INPUT signals
    print("1️⃣ Collecting INPUT signals (11-organ system)...")
    input_signals = collector.collect_from_organism_result(
        input_organism_result,
        signal_type='INPUT'
    )
    print(f"   Type: {input_signals['type']}")
    print(f"   Organs tracked: {len(input_signals['organ_coherences'])} (all 11 organs)")
    print(f"   Mean coherence: {input_signals['mean_coherence']:.3f}")
    print(f"   Satisfaction: {input_signals['satisfaction']:.3f}")
    print(f"   V0 final energy: {input_signals['v0_energy']['final']:.3f}")
    print(f"   BOND self-distance: {input_signals['bond_self_distance']:.3f}")
    print(f"   EO polyvagal state: {input_signals['eo_polyvagal_state']} (Phase 2)")
    print(f"   RNX temporal state: {input_signals['rnx_temporal_state']} (Phase 2)")
    print(f"   CARD response scale: {input_signals['card_response_scale']} (Phase 2)")
    print()

    # Test 2: Collect OUTPUT signals
    print("2️⃣ Collecting OUTPUT signals (11-organ system)...")
    output_signals = collector.collect_from_organism_result(
        output_organism_result,
        signal_type='OUTPUT'
    )
    print(f"   Type: {output_signals['type']}")
    print(f"   Organs tracked: {len(output_signals['organ_coherences'])} (all 11 organs)")
    print(f"   Mean coherence: {output_signals['mean_coherence']:.3f}")
    print(f"   Satisfaction: {output_signals['satisfaction']:.3f}")
    print(f"   V0 final energy: {output_signals['v0_energy']['final']:.3f}")
    print(f"   BOND self-distance: {output_signals['bond_self_distance']:.3f}")
    print(f"   EO polyvagal state: {output_signals['eo_polyvagal_state']} (Phase 2)")
    print(f"   RNX temporal state: {output_signals['rnx_temporal_state']} (Phase 2)")
    print(f"   CARD response scale: {output_signals['card_response_scale']} (Phase 2)")
    print(f"   Family: {output_signals['phase5_family_id']} (57D signatures)")
    print()

    # Test 3: Collect learning signals
    print("3️⃣ Collecting learning signals...")
    learning_signals = collector.collect_learning_signals(
        input_signals,
        output_signals,
        context={'conversation_id': 'test_001'}
    )
    print(f"   Satisfaction delta: {learning_signals['satisfaction_delta']:.3f}")
    print(f"   Self-distance reduction: {learning_signals['self_distance_reduction']:.3f}")
    print(f"   V0 energy delta: {learning_signals['v0_energy_delta']:.3f}")
    print(f"   Convergence speedup: {learning_signals['convergence_speedup']} cycles")
    print(f"   Family assigned: {learning_signals['family_assigned']}")
    print()

    # Test 4: Create complete pair record
    print("4️⃣ Creating complete pair signal record...")
    pair_record = collector.create_pair_signal_record(
        pair_id='burnout_001_epoch1',
        input_signals=input_signals,
        output_signals=output_signals,
        learning_signals=learning_signals,
        context={'conversation_id': 'test_001', 'epoch_num': 1}
    )
    print(f"   Pair ID: {pair_record['pair_id']}")
    print(f"   Satisfaction improvement: {pair_record['metrics']['satisfaction_improvement']:.3f}")
    print(f"   Trauma reduction: {pair_record['metrics']['trauma_reduction']:.3f}")
    print(f"   Energy descent: {pair_record['metrics']['energy_descent']:.3f}")
    print()

    # Test 5: Extract statistics from multiple signals
    print("5️⃣ Testing statistics extraction (simulated 3 pairs)...")

    # Simulate 3 pair records
    signals = []
    for i in range(3):
        sim_record = collector.create_pair_signal_record(
            pair_id=f'pair_{i+1}',
            input_signals=input_signals,
            output_signals=output_signals,
            learning_signals=learning_signals,
            context={'pair_num': i+1}
        )
        signals.append(sim_record)

    organ_stats = collector.extract_organ_statistics(signals)
    print(f"   Organ statistics (EMPATHY): mean={organ_stats.get('EMPATHY', {}).get('mean', 0):.3f}")

    family_stats = collector.extract_family_statistics(signals)
    print(f"   Family statistics: {family_stats['unique_families']} unique families")

    learning_velocity = collector.extract_learning_velocity(signals)
    print(f"   Learning velocity: {learning_velocity['learning_rate']:.2f} updates/pair")

    trauma_stats = collector.extract_trauma_processing_stats(signals)
    print(f"   Trauma processing: {trauma_stats['reduction_rate']*100:.1f}% reduction rate")
    print()

    print("="*70)
    print("✅ Signal collector test complete!")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_signal_collector()
