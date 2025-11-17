"""
Validate Crisis/Urgency Response Quality
=========================================

Process representative crisis/urgency inputs and analyze DAE's actual responses:
- Appropriateness (does response fit input?)
- Therapeutic quality (grounding, containment, validation?)
- Urgency detection (NDAM activation?)
- Zone transformation (reaching Zone 4?)
- Polyvagal modulation (sympathetic activation?)

Date: November 17, 2025
Purpose: Validate Phase 1.1+1.2 impact on response quality
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def validate_crisis_responses():
    """
    Test 10 representative inputs (5 crisis, 3 shadow, 2 exile)
    and analyze actual DAE responses.
    """

    print("=" * 80)
    print("🔍 VALIDATING CRISIS/URGENCY RESPONSE QUALITY")
    print("=" * 80)

    # Representative test inputs
    test_cases = [
        # CRISIS INPUTS (High Urgency)
        {
            "id": "crisis_high_1",
            "category": "high_urgency",
            "input": "I'm terrified about Emma's surgery tomorrow and I can't stop my mind from spiraling",
            "expected_zone": 4,
            "expected_urgency": ">0.6",
            "expected_ndam": ">0.3"
        },
        {
            "id": "crisis_high_2",
            "category": "high_urgency",
            "input": "Work is completely crushing me right now - I can't breathe, everything is too much",
            "expected_zone": 4,
            "expected_urgency": ">0.7",
            "expected_ndam": ">0.4"
        },
        {
            "id": "crisis_moderate_1",
            "category": "moderate_stress",
            "input": "I'm worried about how my conversation with Emma will go this weekend",
            "expected_zone": 3,
            "expected_urgency": "0.3-0.5",
            "expected_ndam": "0.2-0.4"
        },
        {
            "id": "crisis_deescalate_1",
            "category": "de_escalation",
            "input": "I was panicking earlier but I'm starting to calm down now",
            "expected_zone": 2,
            "expected_urgency": "<0.3",
            "expected_ndam": "<0.3"
        },
        {
            "id": "crisis_deescalate_2",
            "category": "de_escalation",
            "input": "The crisis has passed and I can breathe again",
            "expected_zone": 2,
            "expected_urgency": "<0.25",
            "expected_ndam": "<0.2"
        },

        # SHADOW INPUTS (Zone 4)
        {
            "id": "shadow_1",
            "category": "shadow_work",
            "input": "There's a part of me I'm deeply ashamed of and I don't want to look at it",
            "expected_zone": 4,
            "expected_urgency": "0.3-0.5",
            "expected_self_distance": ">0.5"
        },
        {
            "id": "shadow_2",
            "category": "shadow_work",
            "input": "I'm afraid if I acknowledge my rage, it will destroy everything",
            "expected_zone": 4,
            "expected_urgency": "0.4-0.6",
            "expected_self_distance": ">0.6"
        },
        {
            "id": "shadow_3",
            "category": "shadow_work",
            "input": "I hate this angry, resentful part of me - it doesn't belong",
            "expected_zone": 4,
            "expected_urgency": "0.3-0.5",
            "expected_self_distance": ">0.6"
        },

        # EXILE INPUTS (Zone 5)
        {
            "id": "exile_1",
            "category": "exile_navigation",
            "input": "I feel completely shut down and numb - like I'm watching life from behind glass",
            "expected_zone": 5,
            "expected_urgency": "0.2-0.4",
            "expected_polyvagal": "dorsal_vagal",
            "expected_self_distance": ">0.7"
        },
        {
            "id": "exile_2",
            "category": "exile_navigation",
            "input": "I'm exiled from myself - I can't find my way back to who I was",
            "expected_zone": 5,
            "expected_urgency": "0.2-0.4",
            "expected_polyvagal": "dorsal_vagal",
            "expected_self_distance": ">0.8"
        }
    ]

    print(f"\n📊 Test Configuration:")
    print(f"   Total test cases: {len(test_cases)}")
    print(f"   Crisis (high/moderate/de-escalation): 5")
    print(f"   Shadow work: 3")
    print(f"   Exile navigation: 2")

    # Initialize organism
    print(f"\n🔧 Initializing organism...")
    organism = ConversationalOrganismWrapper()

    results = []

    print(f"\n🔄 Processing test cases...")
    print("=" * 80)

    for i, test_case in enumerate(test_cases):
        case_id = test_case['id']
        category = test_case['category']
        user_input = test_case['input']

        print(f"\n{'='*80}")
        print(f"TEST CASE {i+1}/{len(test_cases)}: {case_id} ({category})")
        print(f"{'='*80}")
        print(f"\n📝 INPUT:")
        print(f'   "{user_input}"')

        try:
            # Process through organism
            result = organism.process_text(
                user_input,
                context={},
                user_id="validation_user",
                enable_phase2=True,
                enable_tsk_recording=False  # Don't pollute TSK logs
            )

            # Extract key metrics
            emission = result.get('emission', '[NO EMISSION]')
            zone = result.get('zone', 1)
            urgency = result.get('ndam_urgency', 0.0)
            polyvagal = result.get('polyvagal_state', 'ventral_vagal')
            satisfaction = result.get('satisfaction', 0.5)
            v0_final = result.get('v0_final', 1.0)
            convergence_cycles = result.get('convergence_cycles', 0)

            # Organ coherences
            organ_coherences = result.get('organ_coherences', {})
            ndam_coherence = organ_coherences.get('NDAM', 0.0)
            bond_coherence = organ_coherences.get('BOND', 0.0)
            eo_coherence = organ_coherences.get('EO', 0.0)

            # Self-distance (from BOND if available)
            self_distance = result.get('self_distance', 0.5)

            # Display results
            print(f"\n🤖 DAE RESPONSE:")
            print(f'   "{emission}"')

            print(f"\n📊 FELT-STATE METRICS:")
            print(f"   Zone: {zone} (expected: {test_case.get('expected_zone', 'N/A')})")
            print(f"   Urgency: {urgency:.3f} (expected: {test_case.get('expected_urgency', 'N/A')})")
            print(f"   Polyvagal: {polyvagal} (expected: {test_case.get('expected_polyvagal', 'N/A')})")
            print(f"   Self-distance: {self_distance:.3f} (expected: {test_case.get('expected_self_distance', 'N/A')})")
            print(f"   Satisfaction: {satisfaction:.3f}")
            print(f"   V0 convergence: {convergence_cycles} cycles, final={v0_final:.3f}")

            print(f"\n🧠 ORGAN ACTIVATION:")
            print(f"   NDAM (crisis): {ndam_coherence:.3f} (expected: {test_case.get('expected_ndam', 'N/A')})")
            print(f"   BOND (parts): {bond_coherence:.3f}")
            print(f"   EO (polyvagal): {eo_coherence:.3f}")

            # Store results
            results.append({
                'case_id': case_id,
                'category': category,
                'input': user_input,
                'emission': emission,
                'zone': zone,
                'urgency': urgency,
                'polyvagal': polyvagal,
                'self_distance': self_distance,
                'satisfaction': satisfaction,
                'ndam_coherence': ndam_coherence,
                'bond_coherence': bond_coherence,
                'eo_coherence': eo_coherence,
                'expected': test_case
            })

            print(f"\n✅ Test case {i+1} complete")

        except Exception as e:
            print(f"\n❌ Error processing {case_id}: {e}")
            import traceback
            traceback.print_exc()
            continue

    # Summary analysis
    print(f"\n{'='*80}")
    print(f"📊 VALIDATION SUMMARY")
    print(f"{'='*80}")

    print(f"\n🎯 URGENCY VARIATION:")
    urgencies = [r['urgency'] for r in results]
    if urgencies:
        import numpy as np
        print(f"   Mean: {np.mean(urgencies):.3f}")
        print(f"   Std:  {np.std(urgencies):.3f}")
        print(f"   Min:  {np.min(urgencies):.3f}")
        print(f"   Max:  {np.max(urgencies):.3f}")
        print(f"   [{'✅' if np.std(urgencies) > 0.1 else '❌'}] Variation achieved (std > 0.1)")

    print(f"\n🌀 ZONE DISTRIBUTION:")
    zones = [r['zone'] for r in results]
    zone_counts = {}
    for z in zones:
        zone_counts[z] = zone_counts.get(z, 0) + 1
    for zone in sorted(zone_counts.keys()):
        count = zone_counts[zone]
        pct = 100 * count / len(zones)
        print(f"   Zone {zone}: {count}/{len(zones)} ({pct:.1f}%)")

    print(f"\n🧠 NDAM ACTIVATION:")
    ndam_activations = [r['ndam_coherence'] for r in results]
    if ndam_activations:
        activated = sum(1 for n in ndam_activations if n > 0.3)
        print(f"   Activated (>0.3): {activated}/{len(ndam_activations)} ({100*activated/len(ndam_activations):.1f}%)")
        print(f"   Mean coherence: {np.mean(ndam_activations):.3f}")

    print(f"\n💬 RESPONSE QUALITY:")
    print(f"   Total responses: {len(results)}")
    print(f"   All generated: {'✅' if all(r['emission'] != '[NO EMISSION]' for r in results) else '❌'}")
    print(f"   Mean satisfaction: {np.mean([r['satisfaction'] for r in results]):.3f}")

    # Save results
    results_path = Path("results/crisis_validation_results.json")
    results_path.parent.mkdir(exist_ok=True)
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {results_path}")

    print(f"\n{'='*80}")
    print(f"✅ VALIDATION COMPLETE")
    print(f"{'='*80}")

    return results


if __name__ == '__main__':
    try:
        results = validate_crisis_responses()
        print(f"\n✅ Validation completed successfully!")
        print(f"   {len(results)} test cases processed")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
