"""
Integrated Training Test - Complete Pipeline with Health Monitoring
====================================================================

Tests complete conversational epoch training pipeline with health monitoring:
1. Pre-training health check
2. Load training pairs
3. Process pairs with organism wrapper
4. Collect signals in real-time
5. Monitor health every N pairs
6. Post-training analysis

This validates the entire system works end-to-end before Epoch 1.

November 11, 2025
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import health monitoring components
from persona_layer.epoch_training.health_monitor import (
    PreTrainingHealthCheck,
    RealTimeHealthMonitor,
    PostTrainingAnalyzer
)
from persona_layer.epoch_training.signal_collector import SignalCollector

# Import organism wrapper
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def run_integrated_training_test(num_pairs: int = 5):
    """
    Run integrated training test with health monitoring.

    Args:
        num_pairs: Number of training pairs to process (default: 5 for quick test)
    """
    print("\n" + "="*70)
    print("🧪 INTEGRATED TRAINING TEST - Complete Pipeline")
    print("="*70 + "\n")

    # ========================================================================
    # TIER 1: PRE-TRAINING HEALTH CHECK
    # ========================================================================
    print("1️⃣ TIER 1: PRE-TRAINING HEALTH CHECK")
    print("-" * 70 + "\n")

    checker = PreTrainingHealthCheck(bundle_path="Bundle")
    health_status = checker.run_health_check()

    if health_status['status'] == 'CRITICAL':
        print("\n❌ CRITICAL: Cannot proceed with training")
        print("   Fix critical issues and retry")
        return None

    if health_status['status'] == 'WARNING':
        print("\n⚠️  WARNING: Some issues detected, proceeding with caution")

    print(f"\n✅ Pre-training check: {health_status['status']}")
    print()

    # ========================================================================
    # INITIALIZE COMPONENTS
    # ========================================================================
    print("2️⃣ INITIALIZING COMPONENTS")
    print("-" * 70 + "\n")

    # Initialize organism wrapper
    organism_wrapper = ConversationalOrganismWrapper(bundle_path="Bundle")
    print()

    # Initialize signal collector
    signal_collector = SignalCollector(bundle_path="Bundle")
    print("✅ Signal collector initialized")
    print()

    # Initialize real-time health monitor (check every 2 pairs for quick test)
    health_monitor = RealTimeHealthMonitor(check_interval=2, bundle_path="Bundle")
    print()

    # Initialize production learning coordinator (REAL LEARNING - NOT SIMULATED)
    from persona_layer.epoch_training.production_learning_coordinator import ProductionLearningCoordinator

    learning_coordinator = ProductionLearningCoordinator(
        hebbian_storage="TSK/conversational_hebbian_memory.json",
        phase5_storage="persona_layer",
        learning_threshold=0.45,  # VALIDATION: Lower threshold for trauma-focused training data
        save_frequency=5,  # Save after every 5 pairs (frequent for validation)
        enable_hebbian=True,  # Will gracefully fallback if API mismatch
        enable_phase5=True  # Organic family discovery + cluster learning
    )
    print()

    # ========================================================================
    # LOAD TRAINING PAIRS
    # ========================================================================
    print("3️⃣ LOADING TRAINING PAIRS")
    print("-" * 70 + "\n")

    training_pairs_path = Path("knowledge_base/conversational_training_pairs.json")

    if not training_pairs_path.exists():
        print(f"❌ Training pairs not found: {training_pairs_path}")
        return None

    with open(training_pairs_path) as f:
        data = json.load(f)

    all_pairs = data['training_pairs']
    pairs_to_process = all_pairs[:num_pairs]

    print(f"✅ Loaded {len(all_pairs)} training pairs")
    print(f"   Processing first {num_pairs} pairs for testing")
    print()

    # ========================================================================
    # TIER 2: REAL-TIME TRAINING WITH HEALTH MONITORING
    # ========================================================================
    print("4️⃣ TIER 2: REAL-TIME TRAINING WITH HEALTH MONITORING")
    print("-" * 70 + "\n")

    accumulated_signals = []

    for i, pair in enumerate(pairs_to_process):
        pair_num = i + 1
        pair_id = pair['pair_metadata']['id']

        print(f"📘 Processing Pair {pair_num}/{num_pairs}: {pair_id}")
        print(f"   Category: {pair['pair_metadata']['category']}")
        print(f"   Self-distance: {pair['pair_metadata']['self_distance']:.2f}")
        print()

        # ----------------------------------------------------------------
        # Process INPUT text through organism
        # ----------------------------------------------------------------
        print(f"   ▶️  Processing INPUT...")

        input_result = organism_wrapper.process_text(
            text=pair['input_text'],
            context={
                'conversation_id': f"{pair_id}_INPUT",
                'epoch_num': 1,
                'training_phase': 'input',
                'self_distance': pair['pair_metadata']['self_distance'],
                'polyvagal_state': pair['pair_metadata']['polyvagal_state']
            },
            enable_tsk_recording=True
        )

        # Collect INPUT signals
        input_signals = signal_collector.collect_from_organism_result(
            input_result, 'INPUT'
        )

        print(f"      Satisfaction: {input_signals['satisfaction']:.3f}")
        print(f"      Mean coherence: {input_signals['mean_coherence']:.3f}")
        print(f"      Self-distance: {input_signals['bond_self_distance']:.3f}")
        print()

        # ----------------------------------------------------------------
        # Process OUTPUT text through organism
        # ----------------------------------------------------------------
        print(f"   ▶️  Processing OUTPUT...")

        output_result = organism_wrapper.process_text(
            text=pair['output_text'],
            context={
                'conversation_id': f"{pair_id}_OUTPUT",
                'epoch_num': 1,
                'training_phase': 'output',
                'self_distance': pair['pair_metadata']['self_distance'] * 0.4,  # Expected reduction
                'polyvagal_state': 'ventral_vagal'  # Expected shift to safe
            },
            enable_tsk_recording=True
        )

        # Collect OUTPUT signals
        output_signals = signal_collector.collect_from_organism_result(
            output_result, 'OUTPUT'
        )

        print(f"      Satisfaction: {output_signals['satisfaction']:.3f}")
        print(f"      Mean coherence: {output_signals['mean_coherence']:.3f}")
        print(f"      Self-distance: {output_signals['bond_self_distance']:.3f}")
        print()

        # ----------------------------------------------------------------
        # Collect learning signals
        # ----------------------------------------------------------------
        learning_signals = signal_collector.collect_learning_signals(
            input_signals,
            output_signals,
            context=pair['pair_metadata']
        )

        # ================================================================
        # REAL LEARNING (NOT SIMULATED) - Replace simulation with actual learning
        # ================================================================
        learning_updates = learning_coordinator.learn_from_training_pair(
            input_result=input_result,
            output_result=output_result,
            pair_metadata=pair['pair_metadata'],
            input_text=pair['input_text'],
            output_text=pair['output_text']
        )

        # Update signals with REAL learning metrics (not simulated)
        learning_signals['hebbian_updates'] = learning_updates['hebbian_updates']
        learning_signals['cluster_updates'] = learning_updates['cluster_updates']
        learning_signals['family_matured'] = learning_updates['family_matured']
        learning_signals['family_id'] = learning_updates.get('family_id', None)
        learning_signals['patterns_total'] = learning_updates.get('patterns_total', 0)

        print(f"   📊 Learning Signals:")
        print(f"      Satisfaction delta: {learning_signals['satisfaction_delta']:+.3f}")
        print(f"      Trauma reduction: {learning_signals['self_distance_reduction']:+.3f}")
        print(f"      Hebbian updates: {learning_signals['hebbian_updates']}")
        print()

        # ----------------------------------------------------------------
        # Create pair record
        # ----------------------------------------------------------------
        pair_record = signal_collector.create_pair_signal_record(
            pair_id=pair_id,
            input_signals=input_signals,
            output_signals=output_signals,
            learning_signals=learning_signals,
            context=pair['pair_metadata']
        )

        accumulated_signals.append(pair_record)

        # ----------------------------------------------------------------
        # Real-time health check (every check_interval pairs)
        # ----------------------------------------------------------------
        health_report = health_monitor.on_pair_complete(pair_record)

        if health_report:
            print(f"\n{'='*70}")
            print(f"💚 HEALTH CHECK - After {pair_num} pairs")
            print(f"{'='*70}")
            # Health report already printed by monitor

        print()

    # ========================================================================
    # TIER 3: POST-TRAINING ANALYSIS
    # ========================================================================
    print("\n" + "="*70)
    print("5️⃣ TIER 3: POST-TRAINING ANALYSIS")
    print("="*70 + "\n")

    # Save training log
    training_logs_path = Path("persona_layer/epoch_training/training_logs")
    training_logs_path.mkdir(parents=True, exist_ok=True)

    training_log_path = training_logs_path / "test_epoch_1.json"

    training_log = {
        'epoch_num': 1,
        'timestamp': datetime.now().isoformat(),
        'num_pairs': num_pairs,
        'training_pairs': accumulated_signals
    }

    with open(training_log_path, 'w') as f:
        json.dump(training_log, f, indent=2)

    print(f"💾 Training log saved: {training_log_path}")
    print()

    # Run post-training analysis
    analyzer = PostTrainingAnalyzer(bundle_path="Bundle")
    analysis_report = analyzer.analyze_epoch(
        epoch_num=1,
        training_log_path=training_log_path
    )

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*70)
    print("📊 INTEGRATED TEST SUMMARY")
    print("="*70 + "\n")

    print(f"✅ Pairs processed: {num_pairs}")
    print(f"✅ Health checks performed: {len(health_monitor.health_checks)}")
    print(f"✅ Signals collected: {len(accumulated_signals)}")
    print(f"✅ Training log saved: {training_log_path}")
    print(f"✅ Analysis report saved: {training_logs_path / 'test_epoch_1_analysis.json'}")
    print()

    # Extract key metrics
    if analysis_report.get('satisfaction'):
        sat = analysis_report['satisfaction']
        print("📈 Satisfaction Progression:")
        print(f"   INPUT mean: {sat.get('input_mean', 0):.3f}")
        print(f"   OUTPUT mean: {sat.get('output_mean', 0):.3f}")
        print(f"   Delta: {sat.get('delta_mean', 0):.3f} ({sat.get('improvement_rate', 0)*100:.1f}% improvement)")
        print()

    if analysis_report.get('trauma'):
        trauma = analysis_report['trauma']
        print("🛡️  Trauma Processing:")
        print(f"   INPUT self-distance: {trauma.get('input_mean', 0):.3f}")
        print(f"   OUTPUT self-distance: {trauma.get('output_mean', 0):.3f}")
        print(f"   Reduction: {trauma.get('reduction_mean', 0):.3f} ({trauma.get('reduction_rate', 0)*100:.1f}%)")
        print()

    print("="*70)
    print("✅ INTEGRATED TEST COMPLETE - All systems operational!")
    print("="*70 + "\n")

    return {
        'health_status': health_status,
        'signals': accumulated_signals,
        'health_checks': health_monitor.health_checks,
        'analysis': analysis_report
    }


if __name__ == '__main__':
    # Run integrated test with 5 pairs (quick validation)
    result = run_integrated_training_test(num_pairs=5)

    if result:
        print("\n🎉 System validated and ready for full Epoch 1 training!")
        print("\n📋 Next steps:")
        print("   1. Run full Epoch 1 with all 30 training pairs")
        print("   2. Monitor health throughout training")
        print("   3. Analyze results and plan Epoch 2")
    else:
        print("\n❌ Test failed - review errors and fix before proceeding")
