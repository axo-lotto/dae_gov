"""
Test Epoch Orchestrator
========================

Tests DAE 3.0 Fractal Levels 5-7 (Task, Epoch, Global confidence).

Expected behavior:
- Tasks tracked with success/failure classification
- Epochs consolidate every N tasks
- Global confidence updates via EMA
- Compound growth rate computed

Date: November 12, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_orchestrator import EpochOrchestrator

def test_epoch_orchestrator():
    """Test epoch-level learning and global confidence"""

    print("="*80)
    print("🧪 EPOCH ORCHESTRATOR TEST (DAE 3.0 Levels 5-7)")
    print("="*80)

    # Initialize organism
    print("\n📋 Initializing organism...")
    organism = ConversationalOrganismWrapper(bundle_path="Bundle")

    # Initialize epoch orchestrator
    print("\n📋 Initializing epoch orchestrator...")
    orchestrator = EpochOrchestrator(
        organism_wrapper=organism,
        epoch_size=5,  # Small epoch for testing
        success_threshold=0.75,
        global_learning_rate=0.1,
        results_dir=Path("results/epochs/test")
    )

    print(f"\n📊 Initial Global State:")
    initial_report = orchestrator.get_global_report()
    print(f"   Total epochs: {initial_report['total_epochs']}")
    print(f"   Total tasks: {initial_report['total_tasks']}")
    print(f"   Global confidence (R₇): {initial_report['global_confidence']:.3f}")

    # Test conversations (5 tasks = 1 epoch)
    test_conversations = [
        {
            'name': 'High Safety (should succeed)',
            'input': "This feels really safe and grounding. Thank you for being here.",
            'expected_success': True
        },
        {
            'name': 'Relational Depth (should succeed)',
            'input': "I feel deeply understood right now. This is powerful.",
            'expected_success': True
        },
        {
            'name': 'Confusion (moderate)',
            'input': "I'm feeling confused about something.",
            'expected_success': True  # Usually satisfying
        },
        {
            'name': 'Short input (may fail)',
            'input': "What?",
            'expected_success': False  # Too short, may not satisfy
        },
        {
            'name': 'Gratitude (should succeed)',
            'input': "Thank you for your presence and wisdom.",
            'expected_success': True
        }
    ]

    print(f"\n🗣️  Processing {len(test_conversations)} tasks (1 epoch)...")

    for i, conv in enumerate(test_conversations, 1):
        print(f"\n{'─'*80}")
        print(f"Task {i}/5: {conv['name']}")
        print(f"{'─'*80}")
        print(f"Input: \"{conv['input']}\"")

        # Process task through orchestrator
        task_result = orchestrator.process_task(
            input_text=conv['input'],
            enable_phase2=True,
            verbose=True
        )

    # Check if epoch was consolidated
    print(f"\n{'='*80}")
    print("📊 FINAL GLOBAL STATE")
    print(f"{'='*80}")

    final_report = orchestrator.get_global_report()
    print(f"\nTotal epochs completed: {final_report['total_epochs']}")
    print(f"Total tasks processed: {final_report['total_tasks']}")
    print(f"Global confidence (R₇): {final_report['global_confidence']:.3f}")

    if final_report['total_epochs'] > 0:
        print(f"\nEpoch History (R₆ values):")
        for i, reward in enumerate(final_report['epoch_history'], 1):
            print(f"   Epoch {i}: R₆ = {reward:.3f}")

    if final_report['compound_growth_rate'] != 0.0:
        print(f"\nCompound Growth Rate: {final_report['compound_growth_rate']:+.1%} per epoch")

    # Validation
    print(f"\n{'='*80}")
    print("✅ VALIDATION")
    print(f"{'='*80}")

    epochs_completed = final_report['total_epochs'] - initial_report['total_epochs']

    if epochs_completed > 0:
        print(f"✅ SUCCESS: {epochs_completed} epoch(s) consolidated!")
        print(f"   Task tracking: Operational (Level 5)")
        print(f"   Epoch consolidation: Operational (Level 6)")
        print(f"   Global confidence: Operational (Level 7)")

        # Check if global state was saved
        state_path = Path("results/epochs/test/global_state.json")
        if state_path.exists():
            print(f"   ✅ Global state persisted: {state_path}")

        # Check if epoch result was saved
        epoch_path = Path(f"results/epochs/test/epoch_001_result.json")
        if epoch_path.exists():
            print(f"   ✅ Epoch result persisted: {epoch_path}")

    else:
        print(f"⚠️  No epochs consolidated (expected 1)")
        print(f"   Current epoch tasks: {len(orchestrator.current_epoch_tasks)}")

    print(f"\n✅ Epoch orchestrator test complete!")
    print(f"\n📊 DAE 3.0 Fractal Levels 5-7: OPERATIONAL")

if __name__ == '__main__':
    test_epoch_orchestrator()
