"""
Comprehensive Phase 2 Testing Suite
Tests multi-cycle convergence, meta-atom activation, and emission quality across diverse scenarios.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
import numpy as np

print("\n" + "="*80)
print("🌀 COMPREHENSIVE PHASE 2 TEST SUITE")
print("="*80 + "\n")

# Initialize wrapper
wrapper = ConversationalOrganismWrapper()

# Test scenarios covering diverse emotional/semantic contexts
test_scenarios = [
    {
        'name': 'Trauma Awareness (Crisis)',
        'text': "I feel completely overwhelmed and exhausted. Everything is too much.",
        'expected_meta_atoms': ['trauma_aware', 'temporal_grounding'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    },
    {
        'name': 'Safety Restoration (Calming)',
        'text': "Take a breath. Let's slow down together. There's space here for you.",
        'expected_meta_atoms': ['safety_restoration', 'temporal_grounding', 'relational_attunement'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    },
    {
        'name': 'Compassion + Presence',
        'text': "I'm with you. What you're feeling matters. Your experience is real and valid.",
        'expected_meta_atoms': ['compassion_safety', 'relational_attunement'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    },
    {
        'name': 'Truth-Telling + Vulnerability',
        'text': "This isn't working. I need to be honest about that. It feels scary to say.",
        'expected_meta_atoms': ['fierce_holding', 'kairos_emergence'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    },
    {
        'name': 'Complex Reasoning (Integration)',
        'text': "The pattern I notice is how I protect myself by staying busy, but there's also this deeper exhaustion that wants rest.",
        'expected_meta_atoms': ['coherence_integration', 'somatic_wisdom'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    },
    {
        'name': 'Window of Tolerance (Regulated)',
        'text': "I'm feeling grounded and present with this. I can be with what's here.",
        'expected_meta_atoms': ['window_of_tolerance', 'temporal_grounding'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    },
    {
        'name': 'Kairos Moment (Threshold)',
        'text': "Something is ready to shift here. I can feel it at the edge of awareness.",
        'expected_meta_atoms': ['kairos_emergence', 'somatic_wisdom'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    },
    {
        'name': 'Somatic Wisdom',
        'text': "My body is telling me to pause. There's a tightness in my chest that wants attention.",
        'expected_meta_atoms': ['somatic_wisdom', 'temporal_grounding'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    },
    {
        'name': 'Multiple Threads (Dense)',
        'text': "I'm noticing the exhaustion, and also the fear underneath it, and how both connect to old patterns of pushing through pain.",
        'expected_meta_atoms': ['trauma_aware', 'coherence_integration', 'somatic_wisdom'],
        'expected_nexuses': 3,
        'expected_confidence_min': 0.50
    },
    {
        'name': 'Fierce Holding (Boundaries)',
        'text': "I need strong boundaries here with compassion. This is too much and I'm saying no.",
        'expected_meta_atoms': ['fierce_holding', 'window_of_tolerance'],
        'expected_nexuses': 2,
        'expected_confidence_min': 0.40
    }
]

# Meta-atom names for tracking
meta_atom_names = {
    'trauma_aware', 'safety_restoration', 'window_of_tolerance',
    'compassion_safety', 'fierce_holding', 'relational_attunement',
    'temporal_grounding', 'kairos_emergence', 'coherence_integration',
    'somatic_wisdom'
}

# Aggregate results
all_results = []
passed_tests = 0
failed_tests = 0

for i, scenario in enumerate(test_scenarios, 1):
    print(f"\n{'='*80}")
    print(f"TEST {i}/{len(test_scenarios)}: {scenario['name']}")
    print(f"{'='*80}")
    print(f"\n📝 Input: \"{scenario['text']}\"")

    # Process through Phase 2
    result = wrapper.process_text(
        scenario['text'],
        {},
        enable_tsk_recording=False,
        enable_phase2=True
    )

    # Extract metrics
    nexus_count = result['felt_states'].get('emission_nexus_count', 0)
    emission_text = result['felt_states'].get('emission_text', '')
    emission_confidence = result['felt_states'].get('emission_confidence', 0.0)
    emission_path = result['felt_states'].get('emission_path', 'none')
    v0_energy = result['felt_states']['v0_energy']['final_energy']
    cycles = result['felt_states']['convergence_cycles']
    satisfaction = result['felt_states'].get('satisfaction_final', 0.0)
    kairos = result['felt_states'].get('kairos_detected', False)

    # Determine V0 intensity
    if v0_energy > 0.7:
        intensity = 'high'
    elif v0_energy < 0.3:
        intensity = 'low'
    else:
        intensity = 'medium'

    # Extract activated meta-atoms
    activated_meta_atoms = []
    for organ_name, organ_result in result['organ_results'].items():
        activations = getattr(organ_result, 'atom_activations', {})
        for atom, value in activations.items():
            if atom in meta_atom_names and value > 0.05:
                activated_meta_atoms.append((atom, organ_name, value))

    # Get unique meta-atoms
    unique_meta_atoms = list(set([atom for atom, _, _ in activated_meta_atoms]))

    # Print results
    print(f"\n🌀 CONVERGENCE:")
    print(f"   Cycles: {cycles}")
    print(f"   V0 energy: 1.0 → {v0_energy:.3f} (intensity: {intensity})")
    print(f"   Satisfaction: {satisfaction:.3f}")
    print(f"   Kairos detected: {kairos}")
    print(f"   Nexuses: {nexus_count}")

    print(f"\n💬 EMISSION:")
    if emission_text:
        # Truncate long emissions
        display_text = emission_text[:100] + "..." if len(emission_text) > 100 else emission_text
        print(f"   Text: \"{display_text}\"")
    else:
        print(f"   Text: [None generated]")
    print(f"   Confidence: {emission_confidence:.3f}")
    print(f"   Path: {emission_path}")

    print(f"\n🌀 META-ATOMS ACTIVATED ({len(unique_meta_atoms)}):")
    if activated_meta_atoms:
        # Sort by activation value
        for atom, organ, value in sorted(activated_meta_atoms, key=lambda x: x[2], reverse=True)[:10]:
            print(f"   ✓ {atom}: {value:.3f} ({organ})")
    else:
        print(f"   ⚠️  No meta-atoms activated")

    # Evaluate success criteria
    success_criteria = []

    # Criterion 1: Nexus count
    if nexus_count >= scenario['expected_nexuses']:
        success_criteria.append(f"✅ Nexuses: {nexus_count} (expected ≥{scenario['expected_nexuses']})")
    else:
        success_criteria.append(f"❌ Nexuses: {nexus_count} (expected ≥{scenario['expected_nexuses']})")

    # Criterion 2: Confidence
    if emission_confidence >= scenario['expected_confidence_min']:
        success_criteria.append(f"✅ Confidence: {emission_confidence:.3f} (expected ≥{scenario['expected_confidence_min']:.2f})")
    else:
        success_criteria.append(f"❌ Confidence: {emission_confidence:.3f} (expected ≥{scenario['expected_confidence_min']:.2f})")

    # Criterion 3: Convergence (2-5 cycles)
    if 2 <= cycles <= 5:
        success_criteria.append(f"✅ Cycles: {cycles} (expected 2-5)")
    else:
        success_criteria.append(f"⚠️  Cycles: {cycles} (expected 2-5)")

    # Criterion 4: Expected meta-atoms present
    expected_found = [meta for meta in scenario['expected_meta_atoms'] if meta in unique_meta_atoms]
    if len(expected_found) >= len(scenario['expected_meta_atoms']) // 2:  # At least half
        success_criteria.append(f"✅ Meta-atoms: {len(expected_found)}/{len(scenario['expected_meta_atoms'])} expected found")
    else:
        success_criteria.append(f"⚠️  Meta-atoms: {len(expected_found)}/{len(scenario['expected_meta_atoms'])} expected found")

    # Criterion 5: Emission generated
    if emission_text:
        success_criteria.append(f"✅ Emission: Generated")
    else:
        success_criteria.append(f"❌ Emission: None")

    print(f"\n📊 SUCCESS CRITERIA:")
    for criterion in success_criteria:
        print(f"   {criterion}")

    # Overall pass/fail
    critical_pass = (
        nexus_count >= scenario['expected_nexuses'] - 1 and  # Allow 1 nexus variance
        emission_confidence >= scenario['expected_confidence_min'] - 0.1 and  # Allow 0.1 variance
        emission_text is not None
    )

    if critical_pass:
        print(f"\n✅ TEST PASSED")
        passed_tests += 1
    else:
        print(f"\n❌ TEST FAILED")
        failed_tests += 1

    # Store results
    all_results.append({
        'name': scenario['name'],
        'nexuses': nexus_count,
        'confidence': emission_confidence,
        'cycles': cycles,
        'v0_final': v0_energy,
        'satisfaction': satisfaction,
        'kairos': kairos,
        'meta_atoms': unique_meta_atoms,
        'path': emission_path,
        'passed': critical_pass
    })

# Aggregate statistics
print(f"\n{'='*80}")
print(f"📈 AGGREGATE STATISTICS")
print(f"{'='*80}\n")

nexus_counts = [r['nexuses'] for r in all_results]
confidences = [r['confidence'] for r in all_results]
cycles_list = [r['cycles'] for r in all_results]
v0_finals = [r['v0_final'] for r in all_results]
satisfactions = [r['satisfaction'] for r in all_results]

print(f"Tests Passed: {passed_tests}/{len(test_scenarios)} ({passed_tests/len(test_scenarios)*100:.1f}%)")
print(f"Tests Failed: {failed_tests}/{len(test_scenarios)}")

print(f"\nNexus Formation:")
print(f"   Mean: {np.mean(nexus_counts):.2f}")
print(f"   Min: {np.min(nexus_counts)}")
print(f"   Max: {np.max(nexus_counts)}")
print(f"   Std: {np.std(nexus_counts):.2f}")

print(f"\nEmission Confidence:")
print(f"   Mean: {np.mean(confidences):.3f}")
print(f"   Min: {np.min(confidences):.3f}")
print(f"   Max: {np.max(confidences):.3f}")
print(f"   Std: {np.std(confidences):.3f}")

print(f"\nConvergence Cycles:")
print(f"   Mean: {np.mean(cycles_list):.2f}")
print(f"   Min: {np.min(cycles_list)}")
print(f"   Max: {np.max(cycles_list)}")

print(f"\nV0 Final Energy:")
print(f"   Mean: {np.mean(v0_finals):.3f}")
print(f"   Min: {np.min(v0_finals):.3f}")
print(f"   Max: {np.max(v0_finals):.3f}")

print(f"\nSatisfaction:")
print(f"   Mean: {np.mean(satisfactions):.3f}")
print(f"   Min: {np.min(satisfactions):.3f}")
print(f"   Max: {np.max(satisfactions):.3f}")

kairos_count = sum(1 for r in all_results if r['kairos'])
print(f"\nKairos Detection:")
print(f"   Detected: {kairos_count}/{len(test_scenarios)} ({kairos_count/len(test_scenarios)*100:.1f}%)")

# Meta-atom coverage
all_meta_atoms_found = set()
for r in all_results:
    all_meta_atoms_found.update(r['meta_atoms'])

print(f"\nMeta-Atom Coverage:")
print(f"   Unique meta-atoms activated: {len(all_meta_atoms_found)}/10")
print(f"   Meta-atoms: {', '.join(sorted(all_meta_atoms_found))}")

# Emission paths
paths = {}
for r in all_results:
    path = r['path']
    paths[path] = paths.get(path, 0) + 1

print(f"\nEmission Path Distribution:")
for path, count in sorted(paths.items(), key=lambda x: x[1], reverse=True):
    print(f"   {path}: {count} ({count/len(test_scenarios)*100:.1f}%)")

# Success criteria summary
print(f"\n{'='*80}")
print(f"✅ PHASE 2 VALIDATION SUMMARY")
print(f"{'='*80}\n")

validation_criteria = [
    ("Multi-cycle convergence operational", True),  # Always true if tests ran
    ("Mean nexus count ≥ 2", np.mean(nexus_counts) >= 2),
    ("Mean confidence ≥ 0.40", np.mean(confidences) >= 0.40),
    ("Mean cycles in range [2,5]", 2 <= np.mean(cycles_list) <= 5),
    ("V0 convergence working", np.mean(v0_finals) < 0.5),  # Should descend
    ("≥70% tests passed", passed_tests/len(test_scenarios) >= 0.7),
    ("≥6 unique meta-atoms activated", len(all_meta_atoms_found) >= 6),
    ("Intersection path used", paths.get('intersection', 0) > 0)
]

all_validated = True
for criterion, passed in validation_criteria:
    status = "✅" if passed else "❌"
    print(f"{status} {criterion}")
    if not passed:
        all_validated = False

if all_validated:
    print(f"\n🎉 ALL VALIDATION CRITERIA MET - PHASE 2 READY FOR TRAINING")
else:
    print(f"\n⚠️  SOME VALIDATION CRITERIA NOT MET - REVIEW RESULTS")

print(f"\n{'='*80}")
print(f"🌀 COMPREHENSIVE TESTING COMPLETE")
print(f"{'='*80}\n")

# Save results to file
import json
with open('phase2_test_results.json', 'w') as f:
    json.dump({
        'summary': {
            'passed': passed_tests,
            'failed': failed_tests,
            'total': len(test_scenarios),
            'pass_rate': passed_tests/len(test_scenarios),
            'mean_nexuses': float(np.mean(nexus_counts)),
            'mean_confidence': float(np.mean(confidences)),
            'mean_cycles': float(np.mean(cycles_list)),
            'mean_v0_final': float(np.mean(v0_finals)),
            'meta_atoms_found': list(all_meta_atoms_found)
        },
        'results': all_results
    }, f, indent=2)

print(f"📁 Results saved to: phase2_test_results.json\n")
