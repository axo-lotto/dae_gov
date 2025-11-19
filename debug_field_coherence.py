"""
Debug script to test field coherence calculation with actual organism organ_signatures
"""
import sys
import os
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')
os.chdir('/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from training.wave_coupling_metrics import WaveCouplingTracker
import numpy as np

print("🔍 FIELD COHERENCE DEBUG")
print("=" * 80)

# Initialize organism
print("\n1. Initializing organism...")
organism = ConversationalOrganismWrapper()
print(f"   ✅ Organism initialized")

# Check organ_signatures attribute
print(f"\n2. Checking organism.organ_signatures...")
print(f"   hasattr(organism, 'organ_signatures'): {hasattr(organism, 'organ_signatures')}")

if hasattr(organism, 'organ_signatures'):
    print(f"   Type: {type(organism.organ_signatures)}")
    print(f"   Keys: {list(organism.organ_signatures.keys()) if hasattr(organism.organ_signatures, 'keys') else 'N/A'}")
    print(f"   Number of organs: {len(organism.organ_signatures) if hasattr(organism.organ_signatures, '__len__') else 'N/A'}")

    # Sample first organ
    if hasattr(organism.organ_signatures, 'keys'):
        first_organ = list(organism.organ_signatures.keys())[0]
        print(f"\n   Sample organ: {first_organ}")
        signature = organism.organ_signatures[first_organ]
        print(f"   - Type: {type(signature)}")
        print(f"   - Shape: {signature.shape if hasattr(signature, 'shape') else 'N/A'}")
        print(f"   - Values: {signature}")

        if isinstance(signature, (list, np.ndarray)) and len(signature) > 0:
            mean_val = float(np.mean(signature))
            print(f"   - Mean: {mean_val}")

# Test simple input
print(f"\n3. Testing with simple input...")
test_input = "Do you remember my daughter's name?"
result = organism.process_turn(test_input, user_id="debug_test")

print(f"\n4. After processing:")
print(f"   Result keys: {list(result.keys())}")

if hasattr(organism, 'organ_signatures'):
    print(f"\n   Organ signatures after processing:")
    for organ_name, signature in list(organism.organ_signatures.items())[:3]:  # First 3 organs
        if isinstance(signature, (list, np.ndarray)) and len(signature) > 0:
            mean_val = float(np.mean(signature))
            print(f"   - {organ_name}: mean = {mean_val:.3f}")

# Test wave coupling metrics
print(f"\n5. Testing wave_coupling_metrics...")
tracker = WaveCouplingTracker()

# Create felt_states_with_organs like training script
felt_states = result.get('felt_states', {})
felt_states_with_organs = {
    **felt_states,
    'organ_signatures': dict(organism.organ_signatures) if hasattr(organism, 'organ_signatures') else {}
}

print(f"   felt_states keys: {list(felt_states.keys())}")
print(f"   felt_states_with_organs keys: {list(felt_states_with_organs.keys())}")
print(f"   organ_signatures in felt_states_with_organs: {'organ_signatures' in felt_states_with_organs}")

if 'organ_signatures' in felt_states_with_organs:
    organ_sigs = felt_states_with_organs['organ_signatures']
    print(f"   organ_signatures type: {type(organ_sigs)}")
    print(f"   organ_signatures keys: {list(organ_sigs.keys()) if hasattr(organ_sigs, 'keys') else 'N/A'}")
    print(f"   organ_signatures count: {len(organ_sigs) if hasattr(organ_sigs, '__len__') else 'N/A'}")

# Compute field coherence
print(f"\n6. Computing field coherence...")
field_coherence = tracker.compute_field_coherence(felt_states_with_organs)
print(f"   Field coherence: {field_coherence}")

# Manual calculation
if 'organ_signatures' in felt_states_with_organs:
    organ_sigs = felt_states_with_organs['organ_signatures']
    organ_values = []
    for organ_name, signature in organ_sigs.items():
        if isinstance(signature, (list, np.ndarray)) and len(signature) > 0:
            mean_val = float(np.mean(signature))
            organ_values.append(mean_val)
            print(f"   - {organ_name}: {mean_val:.4f}")
        elif isinstance(signature, (int, float)):
            organ_values.append(float(signature))
            print(f"   - {organ_name}: {float(signature):.4f} (scalar)")

    if organ_values:
        std_dev = float(np.std(organ_values))
        coherence = 1.0 - std_dev
        print(f"\n   Manual calculation:")
        print(f"   - Organ count: {len(organ_values)}")
        print(f"   - Std dev: {std_dev:.4f}")
        print(f"   - Coherence (1 - std): {coherence:.4f}")

print("\n" + "=" * 80)
print("✅ DEBUG COMPLETE")
