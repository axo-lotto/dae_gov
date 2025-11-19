#!/usr/bin/env python3
"""
Single-pair validation: Verify satisfaction feedback activates quality boost.
Quick validation without running full 50-pair epoch.
"""

import json
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from training.organic_intelligence_metrics import OrganicIntelligenceEvaluator

def validate_single_pair():
    print("🧪 SINGLE-PAIR SATISFACTION VALIDATION")
    print("=" * 60)

    # Load training pairs
    with open('knowledge_base/entity_memory_training_pairs.json', 'r') as f:
        data = json.load(f)

    # Get first pair
    pair = data['training_pairs'][0]
    print(f"\n📝 Test Pair: {pair['pair_id']}")
    print(f"   Difficulty: {pair['difficulty']}")
    print(f"   Category: {pair['category']}")
    print(f"   Satisfaction: {pair.get('user_satisfaction', 'MISSING!'):.3f}")

    # Simulate epoch_results with VARIED satisfaction scores
    # (satisfaction signal strength measures VARIATION, not absolute values)
    base_sat = pair['user_satisfaction']
    epoch_results = {
        'satisfaction_scores': [
            base_sat - 0.1,  # Lower satisfaction
            base_sat,        # Medium satisfaction
            base_sat + 0.05  # Higher satisfaction
        ]
    }

    print(f"\n🔍 Testing intelligence metrics with satisfaction_scores:")
    print(f"   satisfaction_scores: {epoch_results['satisfaction_scores']}")

    # Call evaluate_epoch
    from persona_layer.conversational_hebbian_memory import ConversationalHebbianMemory
    from training.organic_intelligence_metrics import OrganicIntelligenceEvaluator

    memory = ConversationalHebbianMemory()
    pattern_database = {
        'cascade_patterns': memory.cascade_patterns,
        'response_patterns': memory.response_patterns,
        'polyvagal_patterns': memory.polyvagal_patterns,
        'self_energy_patterns': memory.self_energy_patterns
    }

    training_corpus = data['training_pairs'][:3]  # Use first 3 pairs

    evaluator = OrganicIntelligenceEvaluator()
    metrics = evaluator.evaluate_epoch(
        epoch=0,  # Test epoch
        epoch_results=epoch_results,
        pattern_database=pattern_database,
        training_corpus=training_corpus
    )

    print(f"\n📊 RESULTS:")
    print(f"   Satisfaction signal strength: {metrics.learning_signals.satisfaction_signal_strength:.3f}")
    print(f"   Learning update rate: {metrics.learning_signals.learning_update_rate*100:.1f}%")
    print(f"   Total quality boost: {metrics.learning_signals.total_quality_boost:.2f} ({'+' + str(int(metrics.learning_signals.total_quality_boost * 100)) + 'pp'})")

    # Validation checks
    print(f"\n✅ VALIDATION:")
    checks = {
        "Satisfaction scores present": len(epoch_results['satisfaction_scores']) > 0,
        "Satisfaction signal > 0": metrics.learning_signals.satisfaction_signal_strength > 0.0,
        "Quality boost = 0.26": abs(metrics.learning_signals.total_quality_boost - 0.26) < 0.01
    }

    passed = 0
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
        if result:
            passed += 1

    print(f"\n📊 Score: {passed}/{len(checks)}")

    if passed == len(checks):
        print("\n🎉 SUCCESS! Satisfaction feedback pipeline is WORKING!")
        return True
    else:
        print("\n⚠️  FAILED: Some checks did not pass")
        return False

if __name__ == "__main__":
    success = validate_single_pair()
    sys.exit(0 if success else 1)
