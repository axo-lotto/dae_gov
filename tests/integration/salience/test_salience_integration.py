"""
Test Salience Model Integration - Quick validation
Verifies that salience model integrates correctly with Phase 2 convergence.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\n" + "="*80)
print("🌀 SALIENCE MODEL INTEGRATION TEST")
print("="*80 + "\n")

# Initialize wrapper
wrapper = ConversationalOrganismWrapper()

# Test trauma-aware text (should trigger gentle intensity)
trauma_text = "I feel completely overwhelmed and exhausted. Everything is too much."

print(f"\n📝 Input: \"{trauma_text}\"")
print("\n🔬 Expected:")
print("   - High signal_inflation (trauma detected)")
print("   - Gentle intensity override (low safety_gradient)")
print("   - Subjective aim set on occasion")
print("   - Trauma markers in felt_states")
print("\n🌀 Processing with salience model...")

result = wrapper.process_text(
    trauma_text,
    {},
    enable_tsk_recording=False,
    enable_phase2=True
)

# Extract salience results
felt_states = result['felt_states']
trauma_markers = felt_states.get('salience_trauma_markers', {})
morphogenetic_guidance = felt_states.get('salience_morphogenetic_guidance', None)

print("\n" + "="*80)
print("📊 SALIENCE INTEGRATION RESULTS")
print("="*80 + "\n")

# Check trauma markers
if trauma_markers:
    print("✅ Trauma markers extracted:")
    print(f"   signal_inflation: {trauma_markers.get('signal_inflation', 0.0):.3f}")
    print(f"   temporal_collapse: {trauma_markers.get('temporal_collapse', 0.0):.3f}")
    print(f"   safety_gradient: {trauma_markers.get('safety_gradient', 1.0):.3f}")
    print(f"   overall_trauma_salience: {trauma_markers.get('overall_trauma_salience', 0.0):.3f}")
else:
    print("❌ No trauma markers found")

# Check morphogenetic guidance
if morphogenetic_guidance:
    print(f"\n✅ Morphogenetic guidance: {morphogenetic_guidance}")
else:
    print("\n⚠️  No morphogenetic guidance")

# Check subjective aim on occasions
occasions = felt_states.get('text_occasions', [])
occasions_with_aim = [occ for occ in occasions if 'subjective_aim' in occ]
if occasions_with_aim:
    print(f"\n✅ Subjective aim set on {len(occasions_with_aim)}/{len(occasions)} occasions")
    print(f"   Example aim: {occasions_with_aim[0].get('subjective_aim', 'none')}")
else:
    print(f"\n⚠️  No subjective aims set on occasions")

# Check emission
emission_text = felt_states.get('emission_text', '')
emission_confidence = felt_states.get('emission_confidence', 0.0)
print(f"\n💬 Emission:")
print(f"   Text: \"{emission_text}\"")
print(f"   Confidence: {emission_confidence:.3f}")

# Validation
print("\n" + "="*80)
print("✅ VALIDATION")
print("="*80 + "\n")

checks = [
    ("Trauma markers present", trauma_markers != {}),
    ("Signal inflation detected", trauma_markers.get('signal_inflation', 0.0) > 0.3),
    ("Morphogenetic guidance set", morphogenetic_guidance is not None),
    ("Subjective aims set", len(occasions_with_aim) > 0),
    ("Emission generated", emission_text != '')
]

all_passed = True
for check_name, passed in checks:
    status = "✅" if passed else "❌"
    print(f"{status} {check_name}")
    if not passed:
        all_passed = False

if all_passed:
    print("\n🎉 SALIENCE INTEGRATION COMPLETE - ALL CHECKS PASSED")
else:
    print("\n⚠️  SOME CHECKS FAILED - REVIEW INTEGRATION")

print("\n" + "="*80)
print("🌀 SALIENCE TEST COMPLETE")
print("="*80 + "\n")
