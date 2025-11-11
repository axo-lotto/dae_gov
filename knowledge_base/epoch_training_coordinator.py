#!/usr/bin/env python3
"""
Epoch Training Coordinator - Progressive Learning from Conversational Traces
=============================================================================

Orchestrates epoch-based learning from mycelium trace transformations,
inspired by DAE 3.0 AXO ARC's epoch learning system (841 perfect tasks, 47.3% success).

Philosophy:
-----------
- Progressive epochs: Learn from accumulated trace transformations
- Cross-conversation memory: Knowledge persists across sessions
- Fractal rewards: Micro (transformation) → Meso (pattern) → Macro (organism)
- Self-organizing intelligence: Patterns emerge naturally from experience

Architecture:
-------------
1. Batch process historical traces
2. Identify transformation pairs
3. Learn patterns (satisfaction↑, wisdom↑)
4. Measure learning progress
5. Display insights

Expected Outcomes (after 50-100 traces):
----------------------------------------
- Transformation prediction: 70-85% accuracy
- Pattern confidence: 0.7-0.9 (mature)
- Recommendation quality: +10-15% relevance

Integration:
------------
- Uses TraceTransformationLearner for pattern analysis
- Uses MyceliumTracer for trace retrieval
- Self-contained within DAE_HYPHAE_1

Author: DAE-GOV Development Team
Created: November 11, 2025
Version: 1.0 (Epoch Learning Coordinator)
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import numpy as np

from knowledge_base.trace_transformation_learner import TraceTransformationLearner, TransformationPattern
from knowledge_base.mycelium_traces import MyceliumTracer


@dataclass
class EpochResults:
    """Results from a single epoch of training."""
    epoch_number: int
    start_time: float
    end_time: float
    duration_seconds: float

    # Trace statistics
    total_traces: int
    traces_with_felt: int
    transformation_pairs_found: int

    # Learning statistics
    patterns_learned: int
    avg_pattern_confidence: float
    top_transformations: List[Tuple[str, str, float]]  # (from, to, confidence)

    # Progress metrics
    total_samples: int  # Cumulative across all patterns
    mature_patterns: int  # Confidence >= 0.7

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'EpochResults':
        """Reconstruct from dict."""
        return EpochResults(**data)


class EpochTrainingCoordinator:
    """
    Coordinates progressive epoch training from conversational traces.

    Usage:
    ------
    >>> coordinator = EpochTrainingCoordinator(user_id="user0")
    >>> results = coordinator.run_epoch()  # Run training on all traces
    >>> coordinator.display_progress()     # Show learning progress
    """

    def __init__(
        self,
        user_id: str = "user0",
        bundle_path: Optional[Path] = None
    ):
        """
        Initialize epoch training coordinator.

        Args:
            user_id: User to train on
            bundle_path: Override Bundle/ location
        """
        self.user_id = user_id

        # Paths
        if bundle_path is None:
            bundle_path = Path(__file__).parent.parent / "Bundle"
        self.bundle_path = Path(bundle_path)

        self.epoch_log_path = self.bundle_path / f"{user_id}" / "epoch_training_log.json"

        # Initialize learner and tracer
        self.learner = TraceTransformationLearner(user_id=user_id, bundle_path=bundle_path)
        self.tracer = MyceliumTracer(user_id=user_id)

        # Epoch history
        self.epoch_history: List[EpochResults] = []
        self._load_epoch_history()

        print(f"🎯 Epoch Training Coordinator initialized")
        print(f"   User: {user_id}")
        print(f"   Bundle: {self.bundle_path}")
        print(f"   Previous epochs: {len(self.epoch_history)}")

    def _load_epoch_history(self):
        """Load previous epoch results."""
        if self.epoch_log_path.exists():
            try:
                with open(self.epoch_log_path, 'r') as f:
                    data = json.load(f)
                self.epoch_history = [EpochResults.from_dict(e) for e in data]
                print(f"   ✅ Loaded {len(self.epoch_history)} epoch results")
            except Exception as e:
                print(f"   ⚠️  Could not load epoch history: {e}")

    def _save_epoch_history(self):
        """Save epoch results to disk."""
        self.epoch_log_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = [e.to_dict() for e in self.epoch_history]
            with open(self.epoch_log_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"   💾 Saved epoch history ({len(self.epoch_history)} epochs)")
        except Exception as e:
            print(f"   ⚠️  Could not save epoch history: {e}")

    def run_epoch(
        self,
        similarity_threshold: float = 0.6,
        time_window_hours: Optional[float] = None
    ) -> EpochResults:
        """
        Run a single epoch of training on all available traces.

        Args:
            similarity_threshold: Minimum felt vector similarity for pairs (0-1)
            time_window_hours: Max time between transformation pairs (None = unlimited)

        Returns:
            EpochResults with training statistics
        """
        start_time = time.time()
        epoch_number = len(self.epoch_history) + 1

        print(f"\n" + "="*70)
        print(f"🌀 EPOCH {epoch_number}: Training on Conversational Traces")
        print(f"="*70)
        print(f"Started: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Similarity threshold: {similarity_threshold:.2f}")
        if time_window_hours:
            print(f"Time window: {time_window_hours:.1f} hours")

        # Step 1: Find transformation pairs
        print(f"\n📊 Step 1: Finding transformation pairs...")
        pairs = self.learner.find_transformation_pairs(
            similarity_threshold=similarity_threshold,
            time_window_hours=time_window_hours
        )

        # Step 2: Analyze transformations
        print(f"\n📊 Step 2: Analyzing transformation patterns...")
        patterns = self.learner.analyze_transformations(
            similarity_threshold=similarity_threshold,
            time_window_hours=time_window_hours
        )

        # Step 3: Display patterns (optional - done by learner)
        print(f"\n📊 Step 3: Storing transformation patterns...")
        self.learner.update_hebbian_memory()

        # Compute statistics
        all_traces = self.tracer.search_traces()
        traces_with_felt = [
            t for t in all_traces
            if t.epoch_metadata and 'felt_state_7d' in t.epoch_metadata
        ]

        total_samples = sum(p.sample_count for p in patterns.values())
        mature_patterns = sum(1 for p in patterns.values() if p.confidence >= 0.7)
        avg_confidence = np.mean([p.confidence for p in patterns.values()]) if patterns else 0.0

        # Top transformations by confidence
        top_transformations = sorted(
            [(k[0], k[1], p.confidence) for k, p in patterns.items()],
            key=lambda x: x[2],
            reverse=True
        )[:5]

        # Create results
        end_time = time.time()
        results = EpochResults(
            epoch_number=epoch_number,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=end_time - start_time,
            total_traces=len(all_traces),
            traces_with_felt=len(traces_with_felt),
            transformation_pairs_found=len(pairs),
            patterns_learned=len(patterns),
            avg_pattern_confidence=float(avg_confidence),
            top_transformations=top_transformations,
            total_samples=total_samples,
            mature_patterns=mature_patterns
        )

        # Save results
        self.epoch_history.append(results)
        self._save_epoch_history()

        # Display summary
        print(f"\n" + "="*70)
        print(f"✅ EPOCH {epoch_number} COMPLETE")
        print(f"="*70)
        print(f"Duration: {results.duration_seconds:.1f}s")
        print(f"Traces analyzed: {results.traces_with_felt}/{results.total_traces}")
        print(f"Transformation pairs: {results.transformation_pairs_found}")
        print(f"Patterns learned: {results.patterns_learned}")
        print(f"Average confidence: {results.avg_pattern_confidence:.2f}")
        print(f"Mature patterns: {results.mature_patterns} (confidence ≥ 0.7)")
        print(f"Total samples: {results.total_samples}")

        if top_transformations:
            print(f"\nTop Transformations:")
            for i, (from_type, to_type, conf) in enumerate(top_transformations, 1):
                print(f"   {i}. {from_type} → {to_type} (confidence: {conf:.2f})")

        print(f"\n🎉 Organism has learned from experience!")
        print(f"   Patterns stored for cross-conversation prediction.")

        return results

    def run_progressive_epochs(
        self,
        target_epochs: int = 10,
        similarity_threshold: float = 0.6
    ) -> List[EpochResults]:
        """
        Run multiple epochs progressively.

        Note: In practice, epochs work best with NEW traces between runs.
        This method is primarily for testing or reprocessing with different thresholds.

        Args:
            target_epochs: Number of epochs to run
            similarity_threshold: Threshold for transformation pairing

        Returns:
            List of EpochResults
        """
        print(f"\n🚀 Progressive Epoch Training")
        print(f"   Target epochs: {target_epochs}")
        print(f"   Current epochs: {len(self.epoch_history)}")

        results = []

        for i in range(target_epochs):
            print(f"\n{'='*70}")
            print(f"Starting epoch {len(self.epoch_history) + 1}/{len(self.epoch_history) + target_epochs}")
            print(f"{'='*70}")

            result = self.run_epoch(similarity_threshold=similarity_threshold)
            results.append(result)

            # Check for saturation (no new patterns)
            if result.patterns_learned == 0 and i > 0:
                print(f"\n⚠️  No new patterns learned - training saturated")
                print(f"   Consider creating new traces or adjusting similarity threshold")
                break

        return results

    def display_progress(self):
        """Display learning progress across all epochs."""
        if not self.epoch_history:
            print("No epoch training history yet. Run run_epoch() first.")
            return

        print(f"\n" + "="*70)
        print(f"📈 EPOCH TRAINING PROGRESS")
        print(f"="*70)
        print(f"User: {self.user_id}")
        print(f"Total epochs: {len(self.epoch_history)}")
        print(f"")

        # Tabular display
        print(f"{'Epoch':<8} {'Traces':<10} {'Pairs':<8} {'Patterns':<10} {'Confidence':<12} {'Mature':<8}")
        print(f"{'-'*70}")

        for epoch in self.epoch_history:
            print(f"{epoch.epoch_number:<8} "
                  f"{epoch.traces_with_felt:<10} "
                  f"{epoch.transformation_pairs_found:<8} "
                  f"{epoch.patterns_learned:<10} "
                  f"{epoch.avg_pattern_confidence:.2f}{' '*8} "
                  f"{epoch.mature_patterns:<8}")

        # Summary statistics
        latest = self.epoch_history[-1]
        print(f"\n{'='*70}")
        print(f"LATEST EPOCH ({latest.epoch_number})")
        print(f"{'='*70}")
        print(f"Timestamp: {datetime.fromtimestamp(latest.end_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Patterns: {latest.patterns_learned} ({latest.mature_patterns} mature)")
        print(f"Samples: {latest.total_samples} transformation observations")
        print(f"Confidence: {latest.avg_pattern_confidence:.2f} average")

        if latest.top_transformations:
            print(f"\nTop Transformations:")
            for i, (from_type, to_type, conf) in enumerate(latest.top_transformations, 1):
                print(f"   {i}. {from_type} → {to_type} (confidence: {conf:.2f})")

        # Growth trajectory
        if len(self.epoch_history) > 1:
            first = self.epoch_history[0]
            growth_patterns = latest.patterns_learned - first.patterns_learned
            growth_confidence = latest.avg_pattern_confidence - first.avg_pattern_confidence
            growth_samples = latest.total_samples - first.total_samples

            print(f"\n{'='*70}")
            print(f"GROWTH (Epoch 1 → {latest.epoch_number})")
            print(f"{'='*70}")
            print(f"Patterns: {first.patterns_learned} → {latest.patterns_learned} (+{growth_patterns})")
            print(f"Confidence: {first.avg_pattern_confidence:.2f} → {latest.avg_pattern_confidence:.2f} ({growth_confidence:+.2f})")
            print(f"Samples: {first.total_samples} → {latest.total_samples} (+{growth_samples})")

        print(f"\n" + "="*70)

    def get_learned_patterns(self) -> Dict[Tuple[str, str], TransformationPattern]:
        """Get all learned transformation patterns."""
        return self.learner.get_learned_patterns()

    def predict_transformation(
        self,
        from_type: str,
        current_felt_state: Dict
    ) -> Optional[Dict[str, any]]:
        """
        Predict outcome of transforming a trace.

        Args:
            from_type: Current trace type
            current_felt_state: Current felt state dict

        Returns:
            Predicted outcomes for possible transformations
        """
        return self.learner.predict_transformation(from_type, current_felt_state)


# Example usage & testing
if __name__ == "__main__":
    print("🌀 Epoch Training Coordinator - Standalone Test\n")

    coordinator = EpochTrainingCoordinator(user_id="user0")

    print("\n" + "="*70)
    print("STEP 1: Running epoch training...")
    print("="*70)
    results = coordinator.run_epoch(similarity_threshold=0.6)

    print("\n" + "="*70)
    print("STEP 2: Displaying progress...")
    print("="*70)
    coordinator.display_progress()

    print("\n" + "="*70)
    print("STEP 3: Testing prediction...")
    print("="*70)

    # Test prediction on a hypothetical note
    test_felt_state = {
        'satisfaction': 0.5,
        'energy': 0.3,
        'organ_coherences': {
            'LISTENING': 0.8,
            'EMPATHY': 0.6,
            'WISDOM': 0.5,
            'AUTHENTICITY': 0.5,
            'PRESENCE': 0.75
        }
    }

    predictions = coordinator.predict_transformation('Note', test_felt_state)

    if predictions:
        print(f"\nPredicted outcomes if transforming this Note:")
        for to_type, predicted_state in predictions.items():
            print(f"\n   {to_type}:")
            print(f"      Satisfaction: {test_felt_state['satisfaction']:.2f} → {predicted_state['satisfaction']:.2f}")
            print(f"      Energy: {test_felt_state['energy']:.2f} → {predicted_state['energy']:.2f}")
            print(f"      Confidence: {predicted_state['confidence']:.2f}")
    else:
        print(f"\nNo predictions available for 'Note' transformations")
        print(f"Run more epochs to learn transformation patterns")

    print("\n✅ Epoch training coordinator test complete!")
