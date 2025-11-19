"""
Diagnostic Script: Field Coherence and Organ Convergence Analysis
Investigates why field_coherence = 0.000 and organs converge to 0.

Questions to answer:
1. What organ values does wave_coupling_metrics see in felt_states?
2. Are these values coming from the correct source?
3. Why do TSK organ signatures show 0.0 for most organs?
4. Is the field coherence formula calculating correctly given the data?
"""

import json
import numpy as np
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from training.wave_coupling_metrics import WaveCouplingTracker

def analyze_single_processing():
    """Process one training pair and examine organ activations at every step."""

    print("=" * 80)
    print("FIELD COHERENCE DIAGNOSTIC - Single Pair Processing")
    print("=" * 80)
    print()

    # Initialize organism
    organism = ConversationalOrganismWrapper()
    wave_tracker = WaveCouplingTracker()

    # Load training pairs from JSON
    with open('knowledge_base/entity_memory_training_pairs.json') as f:
        data = json.load(f)
        training_pairs = data['training_pairs']

    # Get first training pair
    pair = training_pairs[0]
    user_input = pair['user_input']
    expected_output = pair['expected_response']

    print(f"Test Pair: {pair.get('id', 'basic_recall_001')}")
    print(f"User Input: {user_input}")
    print()

    # Process the pair
    print("🌀 Processing...")
    felt_states = organism.process_felt_turn(
        text=user_input,
        username='test_user_20251117_160809'
    )

    print("\n" + "=" * 80)
    print("FELT_STATES STRUCTURE")
    print("=" * 80)
    print(f"\nTop-level keys: {list(felt_states.keys())}")
    print()

    # Check if organ_context exists
    if 'organ_context' not in felt_states:
        print("❌ ISSUE FOUND: 'organ_context' key not present in felt_states")
        print(f"   Available keys: {list(felt_states.keys())}")
        return

    organ_context = felt_states['organ_context']
    print(f"✅ organ_context exists with {len(organ_context)} organs")
    print()

    # Examine organ_context structure
    print("=" * 80)
    print("ORGAN_CONTEXT DETAILED STRUCTURE")
    print("=" * 80)
    print()

    for organ_name, organ_data in organ_context.items():
        print(f"\n{organ_name}:")
        if isinstance(organ_data, dict):
            print(f"  Type: dict")
            print(f"  Keys: {list(organ_data.keys())}")

            # Check for coherence and activation
            coherence = organ_data.get('coherence', None)
            activation = organ_data.get('activation', None)

            print(f"  coherence: {coherence}")
            print(f"  activation: {activation}")

            # Show all values
            print(f"  All values:")
            for k, v in organ_data.items():
                if isinstance(v, (int, float)):
                    print(f"    {k}: {v}")
        else:
            print(f"  Type: {type(organ_data)}")
            print(f"  Value: {organ_data}")

    print("\n" + "=" * 80)
    print("FIELD COHERENCE CALCULATION")
    print("=" * 80)
    print()

    # Manually compute field coherence like wave_tracker does
    organ_values = []
    for organ_name, organ_data in organ_context.items():
        if isinstance(organ_data, dict):
            value = organ_data.get('coherence', organ_data.get('activation', 0.0))
            organ_values.append(value)
            print(f"{organ_name:12s}: {value:.6f}")

    if organ_values:
        std_dev = float(np.std(organ_values))
        coherence = 1.0 - std_dev
        coherence = max(0.0, min(1.0, coherence))

        print()
        print(f"Organ values: {organ_values}")
        print(f"Std dev: {std_dev:.6f}")
        print(f"Field coherence (1 - std): {coherence:.6f}")
        print()

        # Compare with wave_tracker
        wave_coherence = wave_tracker.compute_field_coherence(felt_states)
        print(f"Wave tracker coherence: {wave_coherence:.6f}")
        print()

        # Diagnose why coherence = 0.000
        if coherence < 0.001:
            print("⚠️  DIAGNOSIS: Field coherence near zero")
            print(f"   This means std(organ_values) ≈ 1.0")
            print(f"   Actual std: {std_dev:.6f}")
            print()

            # Check if most organs are actually 0
            zero_count = sum(1 for v in organ_values if abs(v) < 0.001)
            nonzero_count = len(organ_values) - zero_count

            print(f"   Zero organs: {zero_count}/{len(organ_values)}")
            print(f"   Non-zero organs: {nonzero_count}/{len(organ_values)}")
            print()

            if zero_count > len(organ_values) * 0.7:
                print("   🔍 ROOT CAUSE HYPOTHESIS:")
                print("      Most organs have coherence/activation = 0.0")
                print("      This creates high variance when a few organs are non-zero")
                print("      Formula: 1 - std([0, 0, 0, ..., 0.5, 0.3]) ≈ 1 - 0.x ≈ 0.x")
    else:
        print("❌ No organ values extracted!")

    print("\n" + "=" * 80)
    print("ORGAN SIGNATURES (from organism.organ_signatures)")
    print("=" * 80)
    print()

    # Check what organism.organ_signatures actually contains
    if hasattr(organism, 'organ_signatures'):
        print("✅ organism.organ_signatures exists")
        for organ_name in organism.organs:
            sig = organism.organ_signatures.get(organ_name.upper(), None)
            if sig is not None:
                if isinstance(sig, np.ndarray):
                    print(f"{organ_name.upper():12s}: array shape={sig.shape}, mean={np.mean(sig):.4f}, std={np.std(sig):.4f}")
                else:
                    print(f"{organ_name.upper():12s}: {type(sig)} - {sig}")
            else:
                print(f"{organ_name.upper():12s}: None")
    else:
        print("❌ organism.organ_signatures does not exist")

    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("Questions Answered:")
    print()
    print("1. Does felt_states contain organ_context?")
    print(f"   → {'✅ Yes' if 'organ_context' in felt_states else '❌ No'}")
    print()
    print("2. What format is organ_context data?")
    print(f"   → Each organ is a dict with keys like: coherence, activation, etc.")
    print()
    print("3. Why is field_coherence = 0.000?")
    print(f"   → High std deviation from mix of zero and non-zero organ values")
    print()
    print("4. Is this expected behavior?")
    print(f"   → Need to investigate if organs SHOULD be 0.0 after convergence")
    print(f"   → Or if organ_context is capturing wrong values")
    print()

def analyze_tsk_vs_felt_states():
    """Compare TSK organ signatures with felt_states organ_context."""

    print("\n" + "=" * 80)
    print("TSK vs FELT_STATES COMPARISON")
    print("=" * 80)
    print()

    # Load TSK data
    with open('results/epochs/epoch_7/tsk_summary.json', 'r') as f:
        tsk_data = json.load(f)

    # Get first transformation
    first_transform = tsk_data['tsk_transformations'][0]

    print(f"Pair ID: {first_transform['pair_id']}")
    print()
    print("Initial Organ Signatures (TSK):")
    for organ, sig in first_transform['initial_organ_signatures'].items():
        print(f"  {organ:12s}: {sig:.6f}")

    print()
    print("Final Organ Signatures (TSK):")
    for organ, sig in first_transform['final_organ_signatures'].items():
        print(f"  {organ:12s}: {sig:.6f}")

    print()
    print("🔍 TSK PATTERN OBSERVATION:")
    print("   - All organs start at 0.5")
    print("   - Most conversational organs → 0.0 after processing")
    print("   - NEXUS varies (0.05-0.57)")
    print("   - RNX, EO, CARD remain ~0.5")
    print()
    print("   This suggests TSK is capturing SUMMARY signatures (mean of 7 atoms)")
    print("   NOT the coherence/activation values that should be in organ_context")
    print()

if __name__ == '__main__':
    # Set environment
    import os
    os.environ['PYTHONPATH'] = '/Users/daedalea/Desktop/DAE_HYPHAE_1'

    analyze_single_processing()
    analyze_tsk_vs_felt_states()

    print("\n" + "=" * 80)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 80)
