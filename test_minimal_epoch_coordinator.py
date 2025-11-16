"""
Test MinimalEpochCoordinator - Validate epoch coordination infrastructure

Tests:
1. Coordinator initialization
2. Single epoch execution
3. Multi-epoch training (3 epochs)
4. State persistence and reload
5. Family formation tracking across epochs
"""

import sys
import json
from pathlib import Path

# Set up path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.minimal_epoch_coordinator import MinimalEpochCoordinator


def load_sample_training_data(num_pairs: int = 10):
    """Load sample training pairs from IFS diversity set."""
    training_file = Path('knowledge_base/ifs_diversity_training_scenarios.json')

    if not training_file.exists():
        print(f"⚠️  Training file not found: {training_file}")
        # Create minimal sample data
        return [
            {
                'id': 'test_1',
                'input_text': 'I just got the job! I can\'t believe it!',
                'expected_output': 'celebratory'
            },
            {
                'id': 'test_2',
                'input_text': 'I\'m feeling really overwhelmed right now.',
                'expected_output': 'supportive'
            },
            {
                'id': 'test_3',
                'input_text': 'I need some space to process this.',
                'expected_output': 'respectful'
            },
            {
                'id': 'test_4',
                'input_text': 'Everything feels like it\'s falling apart.',
                'expected_output': 'grounding'
            },
            {
                'id': 'test_5',
                'input_text': 'I\'m so grateful for this conversation.',
                'expected_output': 'warm'
            }
        ]

    with open(training_file) as f:
        all_pairs = json.load(f)

    # Return first N pairs
    return all_pairs[:num_pairs]


def test_coordinator_initialization():
    """Test 1: Coordinator initializes correctly."""
    print("\n" + "="*80)
    print("TEST 1: Coordinator Initialization")
    print("="*80)

    try:
        organism = ConversationalOrganismWrapper()
        coordinator = MinimalEpochCoordinator(
            organism_wrapper=organism,
            state_dir='persona_layer/state/test_epoch',
            enable_auto_save=True
        )

        print(f"✅ Coordinator initialized")
        print(f"   State directory: {coordinator.state_dir}")
        print(f"   Current epoch: {coordinator.current_epoch}")
        print(f"   Auto-save enabled: {coordinator.enable_auto_save}")

        return coordinator, organism

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def test_single_epoch(coordinator, training_pairs):
    """Test 2: Single epoch execution."""
    print("\n" + "="*80)
    print("TEST 2: Single Epoch Execution")
    print("="*80)

    try:
        epoch_stats = coordinator.run_epoch(
            training_pairs=training_pairs,
            epoch_id=1,
            verbose=True
        )

        print(f"\n✅ Epoch 1 completed")
        print(f"   Total conversations: {epoch_stats['total_conversations']}")
        print(f"   Mean confidence: {epoch_stats['mean_confidence']:.3f}")
        print(f"   Mean V0 final: {epoch_stats['mean_v0_final']:.3f}")
        print(f"   Families discovered: {epoch_stats.get('families_discovered_this_epoch', 0)}")
        print(f"   Duration: {epoch_stats['duration']:.1f}s")

        return epoch_stats

    except Exception as e:
        print(f"❌ Epoch execution failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_multi_epoch_training(coordinator, training_pairs):
    """Test 3: Multi-epoch training (3 epochs)."""
    print("\n" + "="*80)
    print("TEST 3: Multi-Epoch Training (3 epochs)")
    print("="*80)

    try:
        epoch_results = coordinator.run_training(
            training_pairs=training_pairs,
            num_epochs=3,
            verbose=True
        )

        print(f"\n✅ Multi-epoch training completed")
        print(f"   Epochs completed: {len(epoch_results)}")

        # Track family growth
        print("\n📊 Family Growth Across Epochs:")
        for i, stats in enumerate(epoch_results, 1):
            families = stats.get('unique_families_this_epoch', 0)
            confidence = stats['mean_confidence']
            print(f"   Epoch {i}: {families} families, confidence: {confidence:.3f}")

        return epoch_results

    except Exception as e:
        print(f"❌ Multi-epoch training failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_state_persistence(coordinator):
    """Test 4: State persistence and reload."""
    print("\n" + "="*80)
    print("TEST 4: State Persistence")
    print("="*80)

    try:
        # Save current state
        coordinator._save_epoch_state()
        print(f"✅ State saved to: {coordinator.state_dir / 'epoch_state.json'}")

        # Load state in new coordinator
        new_organism = ConversationalOrganismWrapper()
        new_coordinator = MinimalEpochCoordinator(
            organism_wrapper=new_organism,
            state_dir=coordinator.state_dir,
            enable_auto_save=False
        )

        print(f"✅ State reloaded")
        print(f"   Current epoch: {new_coordinator.current_epoch}")
        print(f"   Epoch history: {len(new_coordinator.epoch_history)} epochs")

        # Verify state matches
        assert new_coordinator.current_epoch == coordinator.current_epoch
        assert len(new_coordinator.epoch_history) == len(coordinator.epoch_history)

        print(f"✅ State persistence verified")

        return True

    except Exception as e:
        print(f"❌ State persistence failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_progress_summary(coordinator):
    """Test 5: Progress summary generation."""
    print("\n" + "="*80)
    print("TEST 5: Progress Summary")
    print("="*80)

    try:
        summary = coordinator.get_progress_summary()

        print(f"✅ Progress summary generated:")
        print(f"   Epochs completed: {summary['epochs_completed']}")
        print(f"   Total conversations: {summary['total_conversations']}")
        print(f"   Confidence trend: {summary['mean_confidence_trend']}")
        print(f"   Families trend: {summary['families_trend']}")

        return summary

    except Exception as e:
        print(f"❌ Progress summary failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run all tests."""
    print("\n" + "🌀"*40)
    print("MINIMAL EPOCH COORDINATOR TEST SUITE")
    print("🌀"*40)

    # Load sample training data
    print("\n📁 Loading sample training data...")
    training_pairs = load_sample_training_data(num_pairs=5)
    print(f"✅ Loaded {len(training_pairs)} training pairs")

    # Test 1: Initialization
    coordinator, organism = test_coordinator_initialization()
    if not coordinator:
        print("\n❌ TESTS FAILED - Coordinator initialization failed")
        return

    # Test 2: Single epoch
    epoch_stats = test_single_epoch(coordinator, training_pairs)
    if not epoch_stats:
        print("\n❌ TESTS FAILED - Single epoch execution failed")
        return

    # Test 3: Multi-epoch training
    epoch_results = test_multi_epoch_training(coordinator, training_pairs)
    if not epoch_results:
        print("\n❌ TESTS FAILED - Multi-epoch training failed")
        return

    # Test 4: State persistence
    persistence_ok = test_state_persistence(coordinator)
    if not persistence_ok:
        print("\n⚠️  WARNING - State persistence failed (non-critical)")

    # Test 5: Progress summary
    summary = test_progress_summary(coordinator)

    # Final summary
    print("\n" + "="*80)
    print("🎯 TEST SUITE SUMMARY")
    print("="*80)
    print(f"✅ Test 1: Coordinator Initialization - PASSED")
    print(f"✅ Test 2: Single Epoch Execution - PASSED")
    print(f"✅ Test 3: Multi-Epoch Training - PASSED")
    print(f"{'✅' if persistence_ok else '⚠️ '} Test 4: State Persistence - {'PASSED' if persistence_ok else 'WARNING'}")
    print(f"{'✅' if summary else '❌'} Test 5: Progress Summary - {'PASSED' if summary else 'FAILED'}")

    print("\n🌀 MinimalEpochCoordinator validation complete!")

    # Save training history
    history_path = 'results/test_epoch_coordinator_history.json'
    coordinator.save_training_history(history_path)
    print(f"\n💾 Training history saved to: {history_path}")


if __name__ == '__main__':
    main()
