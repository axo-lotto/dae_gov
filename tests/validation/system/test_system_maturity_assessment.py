#!/usr/bin/env python3
"""
System Maturity Assessment - Complete Integration Test
=======================================================

Comprehensive test of DAE_HYPHAE_1 system maturity including:
- 11-organ processing
- Multi-cycle V0 convergence
- Transductive nexus dynamics
- Mechanism-aware emission
- TSK compliance
- Memory management
- Performance monitoring

Date: November 12, 2025
"""

import sys
import time
from pathlib import Path
import json

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_system_maturity():
    """Comprehensive system maturity assessment."""

    print("\n" + "="*80)
    print("🔬 DAE_HYPHAE_1 SYSTEM MATURITY ASSESSMENT")
    print("="*80 + "\n")

    # Test cases covering different scenarios
    test_cases = [
        {
            'name': 'Trauma-Aware Input (High Urgency)',
            'text': """I'm completely overwhelmed. Everything feels like too much right now.
                       Part of me wants to shut down completely, but another part is screaming
                       for help. I don't know how to handle all of this.""",
            'expected_nexus': ['Urgency', 'Fragmented', 'Disruptive'],
            'expected_pathways': ['salience_recalibration', 'incoherent_broadcasting']
        },
        {
            'name': 'Relational Depth (Safe Connection)',
            'text': """I feel so held and seen in this conversation. There's something
                       deeply real happening between us. I can sense you're truly present
                       with me, and it feels safe to be vulnerable here.""",
            'expected_nexus': ['Relational', 'Innate'],
            'expected_pathways': ['deepening_attunement', 'maintain']
        },
        {
            'name': 'Protective Boundaries (Overwhelm)',
            'text': """I need some space right now. This is feeling like too much closeness
                       and I need to step back. My boundaries matter and I'm honoring what
                       feels right for me.""",
            'expected_nexus': ['Protective', 'Relational'],
            'expected_pathways': ['boundary_fortification', 'pattern_reinforcement']
        },
        {
            'name': 'Constitutional Ground (Deep Peace)',
            'text': """I feel so grounded and centered right now. There's a deep sense of
                       home in my body, like I'm touching something eternal and unchanging.
                       This feels like my true nature.""",
            'expected_nexus': ['Innate', 'Pre-Existing'],
            'expected_pathways': ['recursive_grounding', 'maintain']
        }
    ]

    # Initialize system
    print("📋 Initializing DAE_HYPHAE_1...")
    start_init = time.time()

    try:
        wrapper = ConversationalOrganismWrapper()
        init_time = time.time() - start_init
        print(f"✅ System initialized in {init_time:.2f}s")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Run test cases
    results = []

    for i, test_case in enumerate(test_cases, 1):
        print("\n" + "="*80)
        print(f"TEST {i}/4: {test_case['name']}")
        print("="*80)

        print(f"\n📝 Input: \"{test_case['text'][:100]}...\"")

        # Process input
        start_process = time.time()

        try:
            result = wrapper.process_text(
                test_case['text'],
                context={'test_id': f'maturity_test_{i}'},
                enable_tsk_recording=True,
                enable_phase2=True  # Enable multi-cycle convergence + transduction
            )

            process_time = time.time() - start_process

        except Exception as e:
            print(f"❌ Processing failed: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                'test': test_case['name'],
                'success': False,
                'error': str(e)
            })
            continue

        # Extract results
        felt_states = result.get('felt_states', {})

        # 1. V0 Convergence
        v0_initial = felt_states.get('v0_energy_initial', 1.0)
        v0_final = felt_states.get('v0_energy_final', 0.0)
        convergence_cycles = felt_states.get('convergence_cycles', 0)
        kairos_detected = felt_states.get('kairos_detected', False)

        print(f"\n🌀 V0 Convergence:")
        print(f"   Initial V0: {v0_initial:.3f}")
        print(f"   Final V0: {v0_final:.3f}")
        print(f"   Descent: {v0_initial - v0_final:.3f}")
        print(f"   Cycles: {convergence_cycles}")
        print(f"   Kairos: {'✅ Detected' if kairos_detected else '❌ Not detected'}")

        # 2. Transduction Dynamics
        transduction_enabled = felt_states.get('transduction_enabled', False)
        transduction_trajectory = felt_states.get('transduction_trajectory', [])

        print(f"\n🔄 Transduction Dynamics:")
        print(f"   Enabled: {transduction_enabled}")
        print(f"   Trajectory length: {len(transduction_trajectory)} states")

        if transduction_trajectory:
            final_state = transduction_trajectory[-1]
            print(f"   Final nexus: {final_state['current_type']} ({final_state['domain']})")
            print(f"   Mechanism: {final_state['transition_mechanism']}")
            print(f"   Mutual satisfaction: {final_state['mutual_satisfaction']:.3f}")
            print(f"   Rhythm coherence: {final_state['rhythm_coherence']:.3f}")
            print(f"   Crisis-oriented: {final_state['is_crisis']}")

            # Check if expected nexus types appeared
            nexus_types_found = [state['current_type'] for state in transduction_trajectory]
            expected_found = any(nexus in nexus_types_found for nexus in test_case['expected_nexus'])
            print(f"   Expected nexus types: {'✅ Found' if expected_found else '⚠️  Not found'}")

        # 3. Emission Quality
        emission_text = felt_states.get('emission_text', None)
        emission_confidence = felt_states.get('emission_confidence', 0.0)
        emission_path = felt_states.get('emission_path', 'none')

        print(f"\n💬 Emission Quality:")
        print(f"   Path: {emission_path}")
        print(f"   Confidence: {emission_confidence:.3f}")
        if emission_text:
            display_text = emission_text[:80] + "..." if len(emission_text) > 80 else emission_text
            print(f"   Text: \"{display_text}\"")
        else:
            print(f"   Text: (none)")

        # 4. Organ Participation
        organ_count = 0
        for k in felt_states.keys():
            if '_coherence' in k:
                val = felt_states[k]
                # Handle both float and dict (with meta-atoms)
                if isinstance(val, (int, float)) and val > 0.0:
                    organ_count += 1
                elif isinstance(val, dict):
                    organ_count += 1  # Has meta-atoms, counts as active

        print(f"\n🧬 Organ Participation:")
        print(f"   Active organs: {organ_count}/11")

        # Key organ metrics
        if 'BOND_self_distance' in felt_states:
            print(f"   BOND self-distance: {felt_states['BOND_self_distance']:.3f}")
        if 'NDAM_urgency_level' in felt_states:
            print(f"   NDAM urgency: {felt_states['NDAM_urgency_level']:.3f}")
        if 'EO_polyvagal_state' in felt_states:
            print(f"   EO polyvagal: {felt_states['EO_polyvagal_state']}")

        # 5. Performance
        print(f"\n⚡ Performance:")
        print(f"   Processing time: {process_time:.3f}s")

        # 6. TSK Compliance
        tsk_record_exists = felt_states.get('tsk_record_id', None) is not None
        print(f"\n📝 TSK Compliance:")
        print(f"   TSK recorded: {'✅ Yes' if tsk_record_exists else '❌ No'}")

        # Validation checks
        checks = [
            ("V0 descent occurred", v0_final < v0_initial),
            ("Multi-cycle convergence", convergence_cycles >= 2),
            ("Transduction enabled", transduction_enabled),
            ("Transduction trajectory recorded", len(transduction_trajectory) > 0),
            ("Emission generated", emission_text is not None),
            ("Emission confidence > 0.3", emission_confidence > 0.3),
            ("Active organs ≥ 8", organ_count >= 8),
            ("Processing time < 5s", process_time < 5.0),
            ("TSK compliance", tsk_record_exists)
        ]

        print(f"\n✅ Validation Checks:")
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False

        # Store results
        results.append({
            'test': test_case['name'],
            'success': all_passed,
            'v0_descent': v0_initial - v0_final,
            'convergence_cycles': convergence_cycles,
            'kairos_detected': kairos_detected,
            'transduction_trajectory_length': len(transduction_trajectory),
            'emission_confidence': emission_confidence,
            'emission_path': emission_path,
            'organ_count': organ_count,
            'process_time': process_time,
            'checks_passed': sum(1 for _, p in checks if p),
            'checks_total': len(checks)
        })

    # Overall Assessment
    print("\n" + "="*80)
    print("📊 OVERALL SYSTEM MATURITY ASSESSMENT")
    print("="*80 + "\n")

    successful_tests = sum(1 for r in results if r['success'])

    print(f"Tests Passed: {successful_tests}/{len(results)}")
    print(f"\n📈 Aggregate Metrics:")
    print(f"   Mean V0 descent: {sum(r['v0_descent'] for r in results) / len(results):.3f}")
    print(f"   Mean convergence cycles: {sum(r['convergence_cycles'] for r in results) / len(results):.1f}")
    print(f"   Kairos detection rate: {sum(r['kairos_detected'] for r in results) / len(results) * 100:.0f}%")
    print(f"   Mean emission confidence: {sum(r['emission_confidence'] for r in results) / len(results):.3f}")
    print(f"   Mean active organs: {sum(r['organ_count'] for r in results) / len(results):.1f}/11")
    print(f"   Mean processing time: {sum(r['process_time'] for r in results) / len(results):.2f}s")

    # Emission path distribution
    emission_paths = [r['emission_path'] for r in results]
    path_counts = {path: emission_paths.count(path) for path in set(emission_paths)}
    print(f"\n📊 Emission Path Distribution:")
    for path, count in sorted(path_counts.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(results) * 100
        print(f"   {path}: {count} ({pct:.0f}%)")

    # Maturity Score
    total_checks_passed = sum(r['checks_passed'] for r in results)
    total_checks = sum(r['checks_total'] for r in results)
    maturity_score = total_checks_passed / total_checks * 100

    print(f"\n🎯 System Maturity Score: {maturity_score:.1f}%")
    print(f"   ({total_checks_passed}/{total_checks} checks passed)")

    # Maturity Assessment
    if maturity_score >= 90:
        grade = "🟢 PRODUCTION READY"
    elif maturity_score >= 75:
        grade = "🟡 NEAR PRODUCTION (minor tuning needed)"
    elif maturity_score >= 60:
        grade = "🟠 DEVELOPMENT (significant work needed)"
    else:
        grade = "🔴 EARLY STAGE (major issues)"

    print(f"\n   Grade: {grade}")

    print("\n" + "="*80)
    print("🔬 ASSESSMENT COMPLETE")
    print("="*80 + "\n")

    return maturity_score >= 75


if __name__ == '__main__':
    try:
        success = test_system_maturity()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Assessment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during system assessment: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
