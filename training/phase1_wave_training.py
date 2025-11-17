"""
Phase 1 Wave Training - Crisis/Urgency + Shadow/Exile Combined Corpus
======================================================================

Combines Phase 1.1 (50 crisis/urgency pairs) + Phase 1.2 (25 shadow/exile pairs)
for initial R-matrix coupling learning with proven wave protocols.

PURPOSE:
- Bootstrap NDAM keyword → felt-signature learning via Hebbian R-matrix
- Enable first nexus formation through organ coalition learning
- Create initial family differentiation (Crisis vs Shadow vs Exile families)
- Achieve satisfaction variance ≥0.005 through EXPANSIVE/NAVIGATION/CONCRESCENCE modulation

PROVEN PROTOCOLS (from DAE3_WAVE_TRAINING_VALIDATED_NOV15_2025.md):
- Field coherence: 1 - std([organ_outputs]) (r=0.82 with task success)
- Kairos window: [0.30, 0.50] (78.6% detection rate, optimal for conversational)
- Satisfaction variance target: ≥0.005 (achieved 0.006357, +27% above target)
- Wave modulation: EXPANSIVE/NAVIGATION/CONCRESCENCE phases

EXPECTED OUTCOMES:
- Epoch 5-10:  R-matrix 0.0 → 0.45, first nexuses (0-2 per conversation)
- Epoch 10-20: R-matrix 0.45 → 0.70, consistent nexuses (2-5 per conversation)
- Epoch 20+:   R-matrix 0.70+, mature nexuses (5-10 per conversation)

Author: DAE_HYPHAE_1 Training Infrastructure
Date: November 17, 2025
"""

import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


def load_combined_training_corpus() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Load and combine Phase 1.1 (crisis/urgency) + Phase 1.2 (shadow/exile) training pairs.

    Returns:
        Tuple of (training_pairs, combined_metadata)
    """

    print("📚 Loading training corpus...")

    # Load Phase 1.1: Crisis/Urgency (50 pairs)
    crisis_path = Path(__file__).parent.parent / "knowledge_base" / "crisis_urgency_training_pairs.json"
    with open(crisis_path, 'r') as f:
        crisis_data = json.load(f)

    # Load Phase 1.2: Shadow/Exile (25 pairs)
    shadow_path = Path(__file__).parent.parent / "knowledge_base" / "shadow_exile_training_pairs.json"
    with open(shadow_path, 'r') as f:
        shadow_data = json.load(f)

    # Combine training pairs
    combined_pairs = crisis_data['training_pairs'] + shadow_data['training_pairs']

    # Create combined metadata
    combined_metadata = {
        "created": datetime.now().isoformat(),
        "purpose": "Phase 1 Combined: Crisis/Urgency + Shadow/Exile training for R-matrix coupling",
        "total_pairs": len(combined_pairs),
        "phase_1_1_pairs": len(crisis_data['training_pairs']),
        "phase_1_2_pairs": len(shadow_data['training_pairs']),
        "categories": {
            **crisis_data['metadata']['categories'],
            **shadow_data['metadata']['categories']
        },
        "expected_outcomes": {
            "urgency_variance": ">0.25",
            "ndam_activation": "40-60% (epochs 5-10), 60-80% (epochs 10-20)",
            "zone_4_transformations": "15-25% (epochs 5-10), 30-50% (epochs 10-20)",
            "zone_5_transformations": "5-10% (epochs 10-20)",
            "nexus_formation": "0-2 per conv (epochs 5-10), 2-5 per conv (epochs 10-20)",
            "r_matrix_coupling": {
                "NDAM_EO": "0.0 → 0.55 (epoch 10) → 0.70 (epoch 20)",
                "BOND_EO": "0.0 → 0.60 (epoch 10) → 0.75 (epoch 20)",
                "BOND_NDAM": "0.0 → 0.50 (epoch 10) → 0.65 (epoch 20)"
            },
            "new_families": ["Crisis Response", "Shadow Integration", "Exile Containment"],
            "satisfaction_variance": "≥0.005 (target), ≥0.006 (expected)"
        }
    }

    print(f"   ✅ Loaded {len(combined_pairs)} training pairs")
    print(f"      • Phase 1.1 (Crisis/Urgency): {len(crisis_data['training_pairs'])} pairs")
    print(f"      • Phase 1.2 (Shadow/Exile): {len(shadow_data['training_pairs'])} pairs")
    print()

    return combined_pairs, combined_metadata


def run_wave_training_epoch(
    organism: ConversationalOrganismWrapper,
    training_pairs: List[Dict[str, Any]],
    epoch: int,
    total_epochs: int
) -> Dict[str, Any]:
    """
    Run one epoch of wave training with EXPANSIVE/NAVIGATION/CONCRESCENCE modulation.

    Args:
        organism: Conversational organism instance
        training_pairs: List of training pair dictionaries
        epoch: Current epoch number (1-indexed)
        total_epochs: Total number of epochs to run

    Returns:
        Epoch statistics dictionary
    """

    print(f"{'=' * 80}")
    print(f"🌀 EPOCH {epoch}/{total_epochs}")
    print(f"{'=' * 80}")
    print()

    epoch_stats = {
        'epoch': epoch,
        'total_pairs': len(training_pairs),
        'processed_pairs': 0,
        'satisfaction_scores': [],
        'satisfaction_raw_scores': [],
        'satisfaction_modulated_scores': [],
        'urgency_scores': [],
        'zone_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
        'polyvagal_states': {'ventral_vagal': 0, 'sympathetic': 0, 'dorsal_vagal': 0, 'mixed_state': 0},
        'nexus_counts': [],
        'ndam_activations': 0,
        'bond_activations': 0,
        'eo_activations': 0,
        'kairos_detections': 0,
        'convergence_cycles': [],
        'field_coherence_scores': [],
        'appetitive_phases': {'EXPANSIVE': 0, 'NAVIGATION': 0, 'CONCRESCENCE': 0},
        'processing_times': [],
        'errors': []
    }

    # Process each training pair
    for i, pair in enumerate(training_pairs, 1):
        pair_id = pair.get('pair_id', f'pair_{i}')
        category = pair.get('category', 'unknown')
        user_input = pair['user_input']
        expected_response = pair['expected_response']

        print(f"[{i}/{len(training_pairs)}] {pair_id} ({category})")
        print(f"   Input: {user_input[:80]}...")

        start_time = time.time()

        try:
            # Process through organism
            result = organism.process_text(
                user_input,
                user_id=f"training_user_epoch{epoch}",
                user_satisfaction=None  # Will be calculated by organism
            )

            processing_time = time.time() - start_time
            epoch_stats['processing_times'].append(processing_time)

            # Extract metrics from result
            # 🚨 FIX: Extract from felt_states nested dict (organism wrapper structure)
            felt_states = result.get('felt_states', {})
            satisfaction = felt_states.get('satisfaction_final', felt_states.get('satisfaction', 0.5))
            urgency = felt_states.get('urgency', 0.0)  # NDAM's mean_urgency
            zone = felt_states.get('zone', 1)
            polyvagal_state = felt_states.get('eo_polyvagal_state', felt_states.get('EO_polyvagal_state', 'ventral_vagal'))
            nexus_count = felt_states.get('nexus_count', 0)
            ndam_coherence = felt_states.get('organ_coherences', {}).get('NDAM', 0.0)
            bond_coherence = felt_states.get('organ_coherences', {}).get('BOND', 0.0)
            eo_coherence = felt_states.get('organ_coherences', {}).get('EO', 0.0)
            convergence_cycles = felt_states.get('convergence_cycles', 0)
            field_coherence = felt_states.get('field_coherence', 0.0)  # Field coherence from felt_states
            kairos_detected = felt_states.get('kairos_detected', False)

            # Track appetitive phase (if available from TSK)
            appetitive_phase = result.get('appetitive_phase', 'NAVIGATION')
            epoch_stats['appetitive_phases'][appetitive_phase] += 1

            # Track wave modulation (if available)
            satisfaction_raw = result.get('satisfaction_raw', satisfaction)
            satisfaction_modulated = result.get('satisfaction_modulated', satisfaction)

            # Update stats
            epoch_stats['processed_pairs'] += 1
            epoch_stats['satisfaction_scores'].append(satisfaction)
            epoch_stats['satisfaction_raw_scores'].append(satisfaction_raw)
            epoch_stats['satisfaction_modulated_scores'].append(satisfaction_modulated)
            epoch_stats['urgency_scores'].append(urgency)
            epoch_stats['zone_distribution'][zone] += 1
            epoch_stats['polyvagal_states'][polyvagal_state] += 1
            epoch_stats['nexus_counts'].append(nexus_count)
            epoch_stats['convergence_cycles'].append(convergence_cycles)
            epoch_stats['field_coherence_scores'].append(field_coherence)

            if ndam_coherence > 0.3:
                epoch_stats['ndam_activations'] += 1
            if bond_coherence > 0.3:
                epoch_stats['bond_activations'] += 1
            if eo_coherence > 0.3:
                epoch_stats['eo_activations'] += 1
            if kairos_detected:
                epoch_stats['kairos_detections'] += 1

            # Print metrics
            print(f"   ✓ Satisfaction: {satisfaction:.3f} (raw: {satisfaction_raw:.3f}, mod: {satisfaction_modulated:.3f})")
            print(f"     Urgency: {urgency:.3f}, Zone: {zone}, Nexuses: {nexus_count}, Coherence: {field_coherence:.3f}")
            print(f"     Phase: {appetitive_phase}, Kairos: {'Yes' if kairos_detected else 'No'}, Time: {processing_time:.2f}s")
            print()

        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            epoch_stats['errors'].append({
                'pair_id': pair_id,
                'error': str(e)
            })
            print()
            continue

    # Calculate epoch summary statistics
    print(f"{'=' * 80}")
    print(f"📊 EPOCH {epoch} SUMMARY")
    print(f"{'=' * 80}")
    print()

    if epoch_stats['satisfaction_scores']:
        sat_mean = np.mean(epoch_stats['satisfaction_scores'])
        sat_std = np.std(epoch_stats['satisfaction_scores'])
        sat_var = np.var(epoch_stats['satisfaction_scores'])

        sat_raw_mean = np.mean(epoch_stats['satisfaction_raw_scores'])
        sat_mod_mean = np.mean(epoch_stats['satisfaction_modulated_scores'])
        modulation_effect = abs(sat_mod_mean - sat_raw_mean)

        urgency_mean = np.mean(epoch_stats['urgency_scores'])
        urgency_std = np.std(epoch_stats['urgency_scores']) if epoch_stats['urgency_scores'] else 0.0

        nexus_mean = np.mean(epoch_stats['nexus_counts']) if epoch_stats['nexus_counts'] else 0.0
        nexus_max = max(epoch_stats['nexus_counts']) if epoch_stats['nexus_counts'] else 0

        coherence_mean = np.mean(epoch_stats['field_coherence_scores']) if epoch_stats['field_coherence_scores'] else 0.0

        cycles_mean = np.mean(epoch_stats['convergence_cycles'])

        time_mean = np.mean(epoch_stats['processing_times'])

        # Add summary stats
        epoch_stats['summary'] = {
            'satisfaction_mean': sat_mean,
            'satisfaction_std': sat_std,
            'satisfaction_variance': sat_var,
            'satisfaction_raw_mean': sat_raw_mean,
            'satisfaction_modulated_mean': sat_mod_mean,
            'modulation_effect': modulation_effect,
            'urgency_mean': urgency_mean,
            'urgency_std': urgency_std,
            'nexus_mean': nexus_mean,
            'nexus_max': nexus_max,
            'field_coherence_mean': coherence_mean,
            'convergence_cycles_mean': cycles_mean,
            'processing_time_mean': time_mean,
            'ndam_activation_rate': epoch_stats['ndam_activations'] / epoch_stats['processed_pairs'],
            'kairos_detection_rate': epoch_stats['kairos_detections'] / epoch_stats['processed_pairs']
        }

        # Print summary
        print(f"✅ Processed: {epoch_stats['processed_pairs']}/{epoch_stats['total_pairs']} pairs")
        print()
        print(f"📈 Satisfaction:")
        print(f"   Mean: {sat_mean:.3f} ± {sat_std:.3f}")
        print(f"   Variance: {sat_var:.6f} {'✅' if sat_var >= 0.005 else '⚠️ '} (target: ≥0.005)")
        print(f"   Raw: {sat_raw_mean:.3f} → Modulated: {sat_mod_mean:.3f} (Δ: {modulation_effect:.3f})")
        print()
        print(f"🎯 Urgency:")
        print(f"   Mean: {urgency_mean:.3f} ± {urgency_std:.3f}")
        print(f"   Std: {urgency_std:.3f} {'✅' if urgency_std >= 0.25 else '⚠️ '} (target: >0.25)")
        print()
        print(f"🌀 Nexus Formation:")
        print(f"   Mean: {nexus_mean:.2f} per conversation")
        print(f"   Max: {nexus_max}")
        nexus_formation_rate = (sum(1 for n in epoch_stats['nexus_counts'] if n > 0) / len(epoch_stats['nexus_counts']) * 100) if epoch_stats['nexus_counts'] else 0.0
        print(f"   Formation rate: {nexus_formation_rate:.1f}%")
        print()
        print(f"🧠 Organ Activation:")
        print(f"   NDAM: {epoch_stats['ndam_activations']}/{epoch_stats['processed_pairs']} ({epoch_stats['ndam_activations']/epoch_stats['processed_pairs']*100:.1f}%)")
        print(f"   BOND: {epoch_stats['bond_activations']}/{epoch_stats['processed_pairs']} ({epoch_stats['bond_activations']/epoch_stats['processed_pairs']*100:.1f}%)")
        print(f"   EO: {epoch_stats['eo_activations']}/{epoch_stats['processed_pairs']} ({epoch_stats['eo_activations']/epoch_stats['processed_pairs']*100:.1f}%)")
        print()
        print(f"🌊 Wave Training:")
        print(f"   Field coherence: {coherence_mean:.3f}")
        print(f"   Kairos detection: {epoch_stats['kairos_detections']}/{epoch_stats['processed_pairs']} ({epoch_stats['kairos_detections']/epoch_stats['processed_pairs']*100:.1f}%)")
        print(f"   Appetitive phases: EXP={epoch_stats['appetitive_phases']['EXPANSIVE']}, NAV={epoch_stats['appetitive_phases']['NAVIGATION']}, CON={epoch_stats['appetitive_phases']['CONCRESCENCE']}")
        print()
        print(f"📍 Zone Distribution:")
        for zone, count in sorted(epoch_stats['zone_distribution'].items()):
            pct = (count / epoch_stats['processed_pairs']) * 100
            print(f"   Zone {zone}: {count}/{epoch_stats['processed_pairs']} ({pct:.1f}%)")
        print()
        print(f"💓 Polyvagal States:")
        for state, count in epoch_stats['polyvagal_states'].items():
            pct = (count / epoch_stats['processed_pairs']) * 100
            print(f"   {state}: {count}/{epoch_stats['processed_pairs']} ({pct:.1f}%)")
        print()
        print(f"⚡ Performance:")
        print(f"   Mean convergence cycles: {cycles_mean:.1f}")
        print(f"   Mean processing time: {time_mean:.2f}s")
        print()

    if epoch_stats['errors']:
        print(f"⚠️  Errors: {len(epoch_stats['errors'])}")
        for error in epoch_stats['errors'][:5]:  # Show first 5
            print(f"   • {error['pair_id']}: {error['error']}")
        print()

    return epoch_stats


def run_phase1_training(epochs: int = 20, save_results: bool = True):
    """
    Run Phase 1 combined wave training.

    Args:
        epochs: Number of training epochs to run (default: 20)
        save_results: Whether to save results to JSON (default: True)
    """

    print("=" * 80)
    print("🌀 PHASE 1 WAVE TRAINING - Crisis/Urgency + Shadow/Exile")
    print("=" * 80)
    print()
    print(f"Configuration:")
    print(f"   Total epochs: {epochs}")
    print(f"   Kairos window: [{Config.KAIROS_WINDOW_MIN}, {Config.KAIROS_WINDOW_MAX}]")
    print(f"   V0 max cycles: {Config.V0_MAX_CYCLES}")
    print(f"   V0 threshold: {Config.V0_CONVERGENCE_THRESHOLD}")
    print(f"   Phase 2 enabled: {Config.INTERACTIVE_ENABLE_PHASE2}")
    print()

    # Load training corpus
    training_pairs, metadata = load_combined_training_corpus()

    # Initialize organism
    print("🔧 Initializing conversational organism...")
    organism = ConversationalOrganismWrapper()
    print("   ✅ Organism initialized (12 organs)")
    print()

    # Run training epochs
    all_epoch_stats = []

    for epoch in range(1, epochs + 1):
        epoch_stats = run_wave_training_epoch(
            organism,
            training_pairs,
            epoch,
            epochs
        )
        all_epoch_stats.append(epoch_stats)

        # Save intermediate results every 5 epochs
        if save_results and epoch % 5 == 0:
            results_path = Path(__file__).parent.parent / "results" / f"phase1_wave_training_epoch{epoch}.json"
            results_path.parent.mkdir(parents=True, exist_ok=True)

            with open(results_path, 'w') as f:
                json.dump({
                    'metadata': metadata,
                    'epochs': all_epoch_stats,
                    'current_epoch': epoch,
                    'total_epochs': epochs
                }, f, indent=2, default=str)

            print(f"💾 Saved intermediate results to {results_path}")
            print()

    # Save final results
    if save_results:
        final_results_path = Path(__file__).parent.parent / "results" / f"phase1_wave_training_complete_{epochs}epochs.json"

        with open(final_results_path, 'w') as f:
            json.dump({
                'metadata': metadata,
                'epochs': all_epoch_stats,
                'total_epochs': epochs,
                'completed': datetime.now().isoformat()
            }, f, indent=2, default=str)

        print("=" * 80)
        print(f"✅ PHASE 1 TRAINING COMPLETE")
        print("=" * 80)
        print()
        print(f"💾 Final results saved to: {final_results_path}")
        print()

        # Print overall summary
        print("📊 OVERALL SUMMARY:")
        print()

        final_stats = all_epoch_stats[-1]['summary']
        initial_stats = all_epoch_stats[0]['summary']

        print(f"Satisfaction variance:")
        print(f"   Epoch 1:  {initial_stats['satisfaction_variance']:.6f}")
        print(f"   Epoch {epochs}: {final_stats['satisfaction_variance']:.6f}")
        print(f"   Change: {(final_stats['satisfaction_variance'] - initial_stats['satisfaction_variance']):.6f}")
        print()

        print(f"Urgency std deviation:")
        print(f"   Epoch 1:  {initial_stats['urgency_std']:.3f}")
        print(f"   Epoch {epochs}: {final_stats['urgency_std']:.3f}")
        print(f"   Change: {(final_stats['urgency_std'] - initial_stats['urgency_std']):.3f}")
        print()

        print(f"Nexus formation:")
        print(f"   Epoch 1:  {initial_stats['nexus_mean']:.2f} per conversation")
        print(f"   Epoch {epochs}: {final_stats['nexus_mean']:.2f} per conversation")
        print(f"   Change: +{(final_stats['nexus_mean'] - initial_stats['nexus_mean']):.2f}")
        print()

        print(f"NDAM activation rate:")
        print(f"   Epoch 1:  {initial_stats['ndam_activation_rate']*100:.1f}%")
        print(f"   Epoch {epochs}: {final_stats['ndam_activation_rate']*100:.1f}%")
        print(f"   Change: +{(final_stats['ndam_activation_rate'] - initial_stats['ndam_activation_rate'])*100:.1f}pp")
        print()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Phase 1 Wave Training - Crisis/Urgency + Shadow/Exile')
    parser.add_argument('--epochs', type=int, default=20, help='Number of epochs to run (default: 20)')
    parser.add_argument('--no-save', action='store_true', help='Don\'t save results to JSON')

    args = parser.parse_args()

    run_phase1_training(epochs=args.epochs, save_results=not args.no_save)
