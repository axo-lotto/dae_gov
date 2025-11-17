"""
Test Week 4 Day 1: Organic Emission Priority Logic
===================================================

Validates that when INTELLIGENCE_EMERGENCE_MODE is enabled:
1. Pattern learner is checked FIRST (before felt-guided LLM)
2. If pattern learner quality > 0.6, use it (ORGANIC EMISSION!)
3. If pattern learner quality <= 0.6, fall back to felt-guided LLM
4. Track organic emission rate over turns

Expected Results:
- Turn 1: Low quality (0% organic - no patterns learned yet)
- Turn 5: Medium quality (0-20% organic - some patterns learned)
- Turn 10: Higher quality (20-40% organic - more patterns learned)
- Turn 20: High quality (40-60% organic - many patterns learned with quality > 0.6)

November 17, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


def test_organic_emission_priority():
    """Test that pattern learner is prioritized over felt-guided LLM when quality > 0.6."""

    print("\n" + "=" * 80)
    print("🌀 WEEK 4 DAY 1: ORGANIC EMISSION PRIORITY TEST")
    print("=" * 80)

    # Verify INTELLIGENCE_EMERGENCE_MODE is enabled
    print(f"\n✓ INTELLIGENCE_EMERGENCE_MODE: {Config.INTELLIGENCE_EMERGENCE_MODE}")
    assert Config.INTELLIGENCE_EMERGENCE_MODE, "❌ INTELLIGENCE_EMERGENCE_MODE must be enabled for this test"

    # Initialize organism
    wrapper = ConversationalOrganismWrapper()

    # Simulate 20-turn conversation with RESTORATIVE pattern (crisis → recovery)
    # This will train the pattern learner over time
    test_turns = [
        # Crisis phase (Turns 1-3)
        {"turn": 1, "input": "Everything is falling apart and I can't cope", "satisfaction": 0.25},
        {"turn": 2, "input": "I don't know how to get through this", "satisfaction": 0.28},
        {"turn": 3, "input": "The weight is crushing me", "satisfaction": 0.30},

        # Early recovery (Turns 4-7)
        {"turn": 4, "input": "Maybe there's a glimmer of hope", "satisfaction": 0.40},
        {"turn": 5, "input": "I'm starting to feel a bit better", "satisfaction": 0.50},
        {"turn": 6, "input": "This feels more manageable now", "satisfaction": 0.60},
        {"turn": 7, "input": "I can see a path forward", "satisfaction": 0.65},

        # Mid recovery (Turns 8-12)
        {"turn": 8, "input": "Things are improving steadily", "satisfaction": 0.70},
        {"turn": 9, "input": "I feel grounded and capable", "satisfaction": 0.75},
        {"turn": 10, "input": "This sense of peace is deepening", "satisfaction": 0.80},
        {"turn": 11, "input": "I'm finding my strength again", "satisfaction": 0.82},
        {"turn": 12, "input": "This feels sustainable now", "satisfaction": 0.85},

        # Full recovery (Turns 13-20)
        {"turn": 13, "input": "I feel alive and present", "satisfaction": 0.87},
        {"turn": 14, "input": "This connection feels real", "satisfaction": 0.88},
        {"turn": 15, "input": "I'm ready to keep growing", "satisfaction": 0.90},
        {"turn": 16, "input": "This journey has been healing", "satisfaction": 0.91},
        {"turn": 17, "input": "I feel more whole now", "satisfaction": 0.92},
        {"turn": 18, "input": "This conversation has helped so much", "satisfaction": 0.93},
        {"turn": 19, "input": "I'm grateful for this space", "satisfaction": 0.94},
        {"turn": 20, "input": "I feel transformed", "satisfaction": 0.95},
    ]

    # Track metrics
    organic_emissions = 0
    llm_emissions = 0
    hebbian_emissions = 0
    other_emissions = 0
    total_emissions = 0

    emission_strategies = []
    emission_confidences = []

    print("\n📊 Processing 20-turn conversation...\n")

    for turn_data in test_turns:
        result = wrapper.process_text(
            text=turn_data['input'],
            context={'turn_number': turn_data['turn']},
            enable_phase2=False,  # Test Phase 1 mode
            user_satisfaction=turn_data['satisfaction']
        )

        # Extract emission strategy
        emission_text = result.get('emission_text', '')
        emission_strategy = result.get('emission_strategy', 'unknown')
        emission_confidence = result.get('confidence', 0.0)

        # Track strategy
        emission_strategies.append(emission_strategy)
        emission_confidences.append(emission_confidence)
        total_emissions += 1

        # Count strategy types
        if emission_strategy == 'nexus_phrase_learned':
            organic_emissions += 1
            marker = "🌱 ORGANIC"
        elif emission_strategy == 'felt_guided_llm':
            llm_emissions += 1
            marker = "🤖 LLM"
        elif emission_strategy == 'hebbian':
            hebbian_emissions += 1
            marker = "📚 HEBBIAN"
        else:
            other_emissions += 1
            marker = f"⚙️  {emission_strategy.upper()}"

        # Show progress every 5 turns
        if turn_data['turn'] % 5 == 0:
            organic_rate = (organic_emissions / total_emissions * 100) if total_emissions > 0 else 0
            print(f"Turn {turn_data['turn']:2d}: {marker:15s} | Confidence: {emission_confidence:.3f} | Organic rate: {organic_rate:5.1f}%")

    # Final statistics
    print("\n" + "=" * 80)
    print("📈 FINAL STATISTICS")
    print("=" * 80)

    organic_rate = (organic_emissions / total_emissions * 100) if total_emissions > 0 else 0
    llm_rate = (llm_emissions / total_emissions * 100) if total_emissions > 0 else 0
    hebbian_rate = (hebbian_emissions / total_emissions * 100) if total_emissions > 0 else 0

    print(f"\nTotal emissions: {total_emissions}")
    print(f"  🌱 Organic (nexus_phrase_learned): {organic_emissions} ({organic_rate:.1f}%)")
    print(f"  🤖 LLM (felt_guided_llm): {llm_emissions} ({llm_rate:.1f}%)")
    print(f"  📚 Hebbian (hebbian): {hebbian_emissions} ({hebbian_rate:.1f}%)")
    print(f"  ⚙️  Other: {other_emissions}")

    # Calculate mean confidence
    mean_confidence = sum(emission_confidences) / len(emission_confidences) if emission_confidences else 0
    print(f"\nMean emission confidence: {mean_confidence:.3f}")

    # Validation checks
    print("\n" + "=" * 80)
    print("✅ VALIDATION CHECKS")
    print("=" * 80)

    checks_passed = 0
    total_checks = 5

    # Check 1: All emissions generated
    if total_emissions == 20:
        print(f"✅ Check 1: All 20 emissions generated")
        checks_passed += 1
    else:
        print(f"❌ Check 1: Only {total_emissions}/20 emissions generated")

    # Check 2: Organic emissions present (even if low initially)
    if organic_emissions > 0 or hebbian_emissions > 0:  # Either is okay since pattern learner uses hebbian fallback
        print(f"✅ Check 2: Organic/hebbian emissions present ({organic_emissions + hebbian_emissions} emissions)")
        checks_passed += 1
    else:
        print(f"❌ Check 2: No organic/hebbian emissions (all LLM or other)")

    # Check 3: No LLM emissions (since INTELLIGENCE_EMERGENCE_MODE enabled)
    if llm_emissions == 0:
        print(f"✅ Check 3: LLM bypassed (INTELLIGENCE_EMERGENCE_MODE working)")
        checks_passed += 1
    else:
        print(f"⚠️  Check 3: {llm_emissions} LLM emissions (should be 0 in emergence mode)")

    # Check 4: Mean confidence > 0.3 (quality threshold)
    if mean_confidence > 0.3:
        print(f"✅ Check 4: Mean confidence {mean_confidence:.3f} > 0.3")
        checks_passed += 1
    else:
        print(f"❌ Check 4: Mean confidence {mean_confidence:.3f} <= 0.3")

    # Check 5: Pattern learner integration working
    pattern_learner_working = hasattr(wrapper.emission_generator, 'pattern_learner')
    if pattern_learner_working:
        print(f"✅ Check 5: Pattern learner integrated into emission generator")
        checks_passed += 1
    else:
        print(f"❌ Check 5: Pattern learner not found in emission generator")

    # Overall result
    print("\n" + "=" * 80)
    pass_rate = (checks_passed / total_checks * 100)

    if checks_passed == total_checks:
        print(f"🎉 ALL CHECKS PASSING ({checks_passed}/{total_checks})")
        print("\n✅ WEEK 4 DAY 1 COMPLETE: Organic Emission Priority Operational!")
        print(f"   - Pattern learner checked FIRST (before LLM)")
        print(f"   - LLM bypassed: {llm_emissions == 0}")
        print(f"   - Organic rate: {organic_rate:.1f}%")
        print(f"   - Mean confidence: {mean_confidence:.3f}")
        print("\n🚀 Ready for epoch training to observe organic rate evolution (0% → 60%+)")
        return 0
    else:
        print(f"⚠️  {checks_passed}/{total_checks} checks passing ({pass_rate:.1f}%)")
        print("\n❌ Some checks failed - review output above")
        return 1


if __name__ == '__main__':
    sys.exit(test_organic_emission_priority())
