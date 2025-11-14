#!/usr/bin/env python3
"""
Test Transductive Nexus Integration
====================================

Quick validation test for Phase T1-T2 transductive integration.

Tests:
1. NexusTransductionState creation
2. TransductionPathwayEvaluator pathway selection
3. Multi-cycle transduction tracking in wrapper

Date: November 12, 2025
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
import json

def test_transduction_integration():
    """Test transductive nexus integration with sample trauma-aware input."""

    print("\n" + "="*80)
    print("🧪 TESTING TRANSDUCTIVE NEXUS INTEGRATION")
    print("="*80 + "\n")

    # Initialize wrapper (should load transduction evaluator)
    wrapper = ConversationalOrganismWrapper()

    # Test input with urgency + relational content
    test_text = """
    I'm completely overwhelmed. There's so much happening and I don't know
    how to process it all. Part of me wants to just shut down, but another
    part is screaming for help. Can you help me?
    """

    print("\n📝 Test Input:")
    print(f'   "{test_text.strip()}"')
    print()

    # Process with Phase 2 (multi-cycle convergence + transduction)
    result = wrapper.process_text(
        test_text,
        context={'test_id': 'transduction_validation'},
        enable_tsk_recording=False,
        enable_phase2=True  # Enable Phase 2 for transduction
    )

    # Extract felt states
    felt_states = result['felt_states']

    print("\n" + "="*80)
    print("📊 TRANSDUCTION RESULTS")
    print("="*80 + "\n")

    # Check if transduction is enabled
    transduction_enabled = felt_states.get('transduction_enabled', False)
    print(f"🔧 Transduction enabled: {transduction_enabled}")

    if not transduction_enabled:
        print("\n⚠️  Transduction NOT enabled - check imports")
        return False

    # Extract transduction trajectory
    trajectory = felt_states.get('transduction_trajectory', [])
    print(f"\n🌀 Transduction trajectory length: {len(trajectory)} cycles")

    if not trajectory:
        print("\n⚠️  No transduction states recorded")
        print("   Possible causes:")
        print("   - No nexuses formed")
        print("   - Transduction evaluator not initialized")
        return False

    # Analyze trajectory
    print("\n📈 Transduction Evolution:")
    print()
    print("Cycle | Nexus Type     | V0 Energy | Satisfaction | Next Type      | Mechanism")
    print("------|----------------|-----------|--------------|----------------|---------------------------")

    for state in trajectory:
        cycle = state['cycle_num']
        current_type = state['current_type']
        v0_energy = state['v0_energy']
        satisfaction = state['satisfaction']
        next_type = state.get('next_type', 'N/A')
        mechanism = state.get('transition_mechanism', 'N/A')

        print(f"  {cycle}   | {current_type:14s} | {v0_energy:9.3f} | {satisfaction:12.3f} | {next_type:14s} | {mechanism}")

    # Analyze final transduction state
    final_state = trajectory[-1]

    print("\n🎯 Final Transduction State:")
    print(f"   Type: {final_state['current_type']}")
    print(f"   Domain: {final_state['domain']}")
    print(f"   Crisis-Oriented: {final_state['is_crisis']}")
    print(f"   Mutual Satisfaction: {final_state['mutual_satisfaction']:.3f}")
    print(f"   Rhythm Coherence: {final_state['rhythm_coherence']:.3f}")
    print(f"   Relational Field Available: {final_state['relational_field_available']}")

    # Transductive vocabulary
    print("\n📖 Transductive Vocabulary (Felt States):")
    print(f"   Signal Inflation: {final_state['signal_inflation']:.3f}")
    print(f"   Salience Drift: {final_state['salience_drift']:.3f}")
    print(f"   Prehensive Overload: {final_state['prehensive_overload']:.3f}")
    print(f"   Coherence Leakage: {final_state['coherence_leakage']:.3f}")

    # Check emission
    emission_text = felt_states.get('emission_text', None)
    emission_confidence = felt_states.get('emission_confidence', 0.0)
    emission_path = felt_states.get('emission_path', 'none')

    print("\n💬 Emission Generated:")
    print(f"   Path: {emission_path}")
    print(f"   Confidence: {emission_confidence:.3f}")
    if emission_text:
        display_emission = emission_text[:100] + "..." if len(emission_text) > 100 else emission_text
        print(f'   Text: "{display_emission}"')
    else:
        print("   Text: (none)")

    # Success criteria
    print("\n" + "="*80)
    print("✅ SUCCESS CRITERIA")
    print("="*80 + "\n")

    checks = []

    # Check 1: Transduction enabled
    checks.append(("Transduction evaluator loaded", transduction_enabled))

    # Check 2: Trajectory recorded
    checks.append(("Transduction trajectory recorded", len(trajectory) > 0))

    # Check 3: Nexus types classified
    if trajectory:
        nexus_types_present = any(state['current_type'] != 'Unknown' for state in trajectory)
        checks.append(("Nexus types classified", nexus_types_present))

        # Check 4: Pathways evaluated
        pathways_evaluated = any(state.get('transition_mechanism') != 'maintain' for state in trajectory)
        checks.append(("Transduction pathways evaluated", pathways_evaluated))

        # Check 5: Mutual satisfaction computed
        mutual_sat_valid = all(0.0 <= state['mutual_satisfaction'] <= 1.0 for state in trajectory)
        checks.append(("Mutual satisfaction valid", mutual_sat_valid))

    # Print check results
    all_passed = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False

    print()

    if all_passed:
        print("🎉 ALL CHECKS PASSED - Transductive integration operational!")
    else:
        print("⚠️  SOME CHECKS FAILED - Review results above")

    print("\n" + "="*80)
    print("🧪 TEST COMPLETE")
    print("="*80 + "\n")

    return all_passed


if __name__ == '__main__':
    try:
        success = test_transduction_integration()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during transduction test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
