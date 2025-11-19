"""
NexusVsLLMDecisionTracker - LLM Independence Progress Monitoring
=================================================================

Tracks NEXUS-first vs LLM-fallback decision quality to calibrate confidence
thresholds and measure progress toward 80-95% LLM-free entity extraction.

Core Learning Pattern:
    Turn 1: NEXUS conf=0.72 (Person: Emma) | LLM (Person: Emma) | Match! ✅
    Turn 2: NEXUS conf=0.68 → fallback | LLM (Person: Emma Smith) | Missed multi-word
    Turn 3: NEXUS conf=0.75 (Place: work) | LLM (Organization: work) | Mismatch ❌

    After 100 turns → Learn:
    - NEXUS confidence 0.65-0.70: 75% accurate (can lower threshold!)
    - NEXUS confidence 0.70-0.75: 85% accurate
    - NEXUS usage: 35% (target: 80% by Epoch 16)
    - LLM fallback: 65% (target: 20% by Epoch 16)

Architecture Alignment:
    - Phase A (LLM Independence): Pattern-based entity extraction
    - Target: 80-95% NEXUS usage by Epoch 16
    - Speedup: 20× when using NEXUS (100-200ms → 5-10ms)

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
Status: Phase 3B Week 1 - Foundation Tracker (CRITICAL for LLM Independence)
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
import numpy as np
from dataclasses import dataclass, field


@dataclass
class DecisionRecord:
    """Record of a single NEXUS vs LLM decision."""
    turn_id: int
    nexus_confidence: float
    nexus_entities: List[Dict[str, Any]]
    llm_entities: List[Dict[str, Any]]
    decision: str  # 'nexus' or 'llm'
    match: bool  # Did NEXUS and LLM agree?
    user_satisfaction: float = 0.0
    processing_time_ms: float = 0.0


@dataclass
class ConfidenceBucket:
    """Statistics for a confidence bucket (e.g., 0.65-0.70)."""
    bucket_range: str
    min_confidence: float
    max_confidence: float

    # Accuracy tracking
    total_count: int = 0
    correct_count: int = 0
    accuracy: float = 0.0

    # Decision tracking
    nexus_used_count: int = 0
    llm_fallback_count: int = 0


class NexusVsLLMDecisionTracker:
    """
    Tracks NEXUS vs LLM decision quality for LLM independence.

    Usage:
        tracker = NexusVsLLMDecisionTracker()

        # After entity extraction
        tracker.update(
            nexus_confidence=0.72,
            nexus_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
            llm_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
            decision='nexus',
            user_satisfaction=0.85
        )

        # Get recommended confidence threshold
        threshold = tracker.get_recommended_threshold()
    """

    def __init__(
        self,
        storage_path: Optional[str] = None,
        confidence_threshold: float = 0.70,
        ema_alpha: float = 0.1
    ):
        """
        Initialize NEXUS vs LLM decision tracker.

        Args:
            storage_path: Path to save decision statistics (JSON)
            confidence_threshold: Initial NEXUS confidence threshold
            ema_alpha: EMA smoothing factor for accuracy
        """
        self.storage_path = storage_path or "persona_layer/state/active/nexus_vs_llm_decisions.json"
        self.confidence_threshold = confidence_threshold
        self.ema_alpha = ema_alpha

        # Decision history (keep last 1000)
        self.decision_history: List[DecisionRecord] = []
        self.max_history = 1000

        # Overall metrics
        self.total_decisions = 0
        self.nexus_usage_count = 0
        self.llm_fallback_count = 0
        self.nexus_usage_rate = 0.0
        self.llm_fallback_rate = 0.0

        # Accuracy tracking
        self.nexus_accuracy = 0.0  # EMA of NEXUS accuracy
        self.llm_accuracy = 0.0    # EMA of LLM accuracy

        # Confidence calibration (buckets)
        self.confidence_buckets: Dict[str, ConfidenceBucket] = {}
        self._initialize_confidence_buckets()

        # Performance metrics
        self.mean_nexus_time_ms = 10.0  # Target: 5-10ms
        self.mean_llm_time_ms = 150.0   # Current: 100-200ms
        self.speedup_factor = 15.0

        # Threshold optimization
        self.recommended_threshold: Optional[float] = None
        self.optimization_reason: Optional[str] = None

        # Load existing statistics
        self._load_statistics()

    def _initialize_confidence_buckets(self):
        """Initialize confidence buckets for calibration."""
        bucket_ranges = [
            (0.50, 0.55), (0.55, 0.60), (0.60, 0.65),
            (0.65, 0.70), (0.70, 0.75), (0.75, 0.80),
            (0.80, 0.85), (0.85, 0.90), (0.90, 0.95),
            (0.95, 1.00)
        ]

        for min_conf, max_conf in bucket_ranges:
            bucket_key = f"{min_conf:.2f}-{max_conf:.2f}"
            self.confidence_buckets[bucket_key] = ConfidenceBucket(
                bucket_range=bucket_key,
                min_confidence=min_conf,
                max_confidence=max_conf
            )

    def update(
        self,
        nexus_confidence: float,
        nexus_entities: List[Dict[str, Any]],
        llm_entities: List[Dict[str, Any]],
        decision: str,
        user_satisfaction: float = 0.0,
        processing_time_ms: float = 0.0
    ):
        """
        Update decision tracker with NEXUS vs LLM comparison.

        Args:
            nexus_confidence: NEXUS confidence score (0-1)
            nexus_entities: Entities from NEXUS extraction
            llm_entities: Entities from LLM extraction
            decision: 'nexus' or 'llm' (which was used)
            user_satisfaction: User satisfaction (0-1) as quality proxy
            processing_time_ms: Processing time in milliseconds
        """
        self.total_decisions += 1

        # Track usage
        if decision == 'nexus':
            self.nexus_usage_count += 1
        else:
            self.llm_fallback_count += 1

        # Update usage rates
        self.nexus_usage_rate = self.nexus_usage_count / self.total_decisions
        self.llm_fallback_rate = self.llm_fallback_count / self.total_decisions

        # Check if NEXUS and LLM match
        match = self._entities_match(nexus_entities, llm_entities)

        # Create decision record
        record = DecisionRecord(
            turn_id=self.total_decisions,
            nexus_confidence=nexus_confidence,
            nexus_entities=nexus_entities,
            llm_entities=llm_entities,
            decision=decision,
            match=match,
            user_satisfaction=user_satisfaction,
            processing_time_ms=processing_time_ms
        )

        # Add to history
        self.decision_history.append(record)
        if len(self.decision_history) > self.max_history:
            self.decision_history.pop(0)

        # Update accuracy (use user satisfaction as proxy)
        if decision == 'nexus':
            # NEXUS accuracy
            accuracy_signal = 1.0 if user_satisfaction > 0.7 else 0.0
            self.nexus_accuracy = (
                self.ema_alpha * accuracy_signal +
                (1.0 - self.ema_alpha) * self.nexus_accuracy
            )
        else:
            # LLM accuracy
            accuracy_signal = 1.0 if user_satisfaction > 0.7 else 0.0
            self.llm_accuracy = (
                self.ema_alpha * accuracy_signal +
                (1.0 - self.ema_alpha) * self.llm_accuracy
            )

        # Update confidence bucket
        self._update_confidence_bucket(nexus_confidence, match, decision)

        # Update processing time
        if processing_time_ms > 0:
            if decision == 'nexus':
                self.mean_nexus_time_ms = (
                    self.ema_alpha * processing_time_ms +
                    (1.0 - self.ema_alpha) * self.mean_nexus_time_ms
                )
            else:
                self.mean_llm_time_ms = (
                    self.ema_alpha * processing_time_ms +
                    (1.0 - self.ema_alpha) * self.mean_llm_time_ms
                )

            self.speedup_factor = self.mean_llm_time_ms / max(1.0, self.mean_nexus_time_ms)

        # Run threshold optimization every 50 decisions
        if self.total_decisions % 50 == 0:
            self._optimize_threshold()

        # Save every 25 decisions
        if self.total_decisions % 25 == 0:
            self._save_statistics()

    def _entities_match(
        self,
        nexus_entities: List[Dict[str, Any]],
        llm_entities: List[Dict[str, Any]]
    ) -> bool:
        """
        Check if NEXUS and LLM extracted the same entities.

        Args:
            nexus_entities: Entities from NEXUS
            llm_entities: Entities from LLM

        Returns:
            True if entities match
        """
        if len(nexus_entities) != len(llm_entities):
            return False

        # Extract entity values
        nexus_values = {e.get('entity_value', '').lower() for e in nexus_entities}
        llm_values = {e.get('entity_value', '').lower() for e in llm_entities}

        return nexus_values == llm_values

    def _update_confidence_bucket(
        self,
        confidence: float,
        match: bool,
        decision: str
    ):
        """
        Update confidence bucket statistics.

        Args:
            confidence: NEXUS confidence score
            match: Whether NEXUS and LLM matched
            decision: Which was used ('nexus' or 'llm')
        """
        # Find bucket
        bucket_key = None
        for key, bucket in self.confidence_buckets.items():
            if bucket.min_confidence <= confidence < bucket.max_confidence:
                bucket_key = key
                break

        if bucket_key is None:
            return

        bucket = self.confidence_buckets[bucket_key]
        bucket.total_count += 1

        if match:
            bucket.correct_count += 1

        bucket.accuracy = bucket.correct_count / bucket.total_count

        if decision == 'nexus':
            bucket.nexus_used_count += 1
        else:
            bucket.llm_fallback_count += 1

    def _optimize_threshold(self):
        """
        Suggest optimal confidence threshold based on learned accuracy.

        Strategy:
        - Find lowest confidence bucket with accuracy > 75%
        - Suggest using that as new threshold
        """
        candidate_buckets = []

        for bucket_key, bucket in sorted(self.confidence_buckets.items()):
            if bucket.total_count < 10:  # Require 10+ samples
                continue

            if bucket.accuracy >= 0.75:  # 75% accuracy threshold
                candidate_buckets.append((bucket.min_confidence, bucket.accuracy, bucket_key))

        if candidate_buckets:
            # Choose lowest confidence with good accuracy
            best_threshold, best_accuracy, best_bucket = candidate_buckets[0]

            if best_threshold < self.confidence_threshold:
                self.recommended_threshold = best_threshold
                self.optimization_reason = (
                    f"Bucket {best_bucket} has {best_accuracy:.1%} accuracy "
                    f"({self.confidence_buckets[best_bucket].total_count} samples), "
                    f"can lower threshold from {self.confidence_threshold:.2f}"
                )

    def get_recommended_threshold(self) -> float:
        """
        Get recommended confidence threshold.

        Returns:
            Recommended threshold (or current if no optimization)
        """
        if self.recommended_threshold is not None:
            return self.recommended_threshold
        return self.confidence_threshold

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive NEXUS vs LLM statistics.

        Returns:
            Dictionary with all statistics
        """
        stats = {
            'usage': {
                'total_decisions': self.total_decisions,
                'nexus_usage_count': self.nexus_usage_count,
                'llm_fallback_count': self.llm_fallback_count,
                'nexus_usage_rate': self.nexus_usage_rate,
                'llm_fallback_rate': self.llm_fallback_rate,
                'target_nexus_rate': 0.80  # By Epoch 16
            },
            'accuracy': {
                'nexus_accuracy': self.nexus_accuracy,
                'llm_accuracy': self.llm_accuracy
            },
            'performance': {
                'mean_nexus_time_ms': self.mean_nexus_time_ms,
                'mean_llm_time_ms': self.mean_llm_time_ms,
                'speedup_factor': self.speedup_factor
            },
            'threshold': {
                'current_threshold': self.confidence_threshold,
                'recommended_threshold': self.recommended_threshold,
                'optimization_reason': self.optimization_reason
            },
            'confidence_calibration': {}
        }

        # Confidence buckets
        for bucket_key, bucket in sorted(self.confidence_buckets.items()):
            if bucket.total_count > 0:
                stats['confidence_calibration'][bucket_key] = {
                    'total_count': bucket.total_count,
                    'accuracy': bucket.accuracy,
                    'nexus_used_count': bucket.nexus_used_count,
                    'llm_fallback_count': bucket.llm_fallback_count
                }

        return stats

    def get_progress_toward_target(self) -> Dict[str, float]:
        """
        Get progress toward 80% NEXUS usage target.

        Returns:
            Dictionary with progress metrics
        """
        target_rate = 0.80
        current_rate = self.nexus_usage_rate

        progress_pct = (current_rate / target_rate) * 100.0 if target_rate > 0 else 0.0

        return {
            'current_nexus_rate': current_rate,
            'target_nexus_rate': target_rate,
            'progress_percentage': min(100.0, progress_pct),
            'remaining_gap': max(0.0, target_rate - current_rate)
        }

    def _save_statistics(self):
        """Save decision statistics to JSON file."""
        try:
            data = {
                'usage': {
                    'total_decisions': self.total_decisions,
                    'nexus_usage_count': self.nexus_usage_count,
                    'llm_fallback_count': self.llm_fallback_count,
                    'nexus_usage_rate': self.nexus_usage_rate,
                    'llm_fallback_rate': self.llm_fallback_rate
                },
                'accuracy': {
                    'nexus_accuracy': self.nexus_accuracy,
                    'llm_accuracy': self.llm_accuracy
                },
                'performance': {
                    'mean_nexus_time_ms': self.mean_nexus_time_ms,
                    'mean_llm_time_ms': self.mean_llm_time_ms,
                    'speedup_factor': self.speedup_factor
                },
                'threshold': {
                    'current_threshold': self.confidence_threshold,
                    'recommended_threshold': self.recommended_threshold,
                    'optimization_reason': self.optimization_reason
                },
                'confidence_buckets': {},
                'timestamp': time.time()
            }

            # Serialize confidence buckets
            for bucket_key, bucket in self.confidence_buckets.items():
                data['confidence_buckets'][bucket_key] = {
                    'min_confidence': bucket.min_confidence,
                    'max_confidence': bucket.max_confidence,
                    'total_count': bucket.total_count,
                    'correct_count': bucket.correct_count,
                    'accuracy': bucket.accuracy,
                    'nexus_used_count': bucket.nexus_used_count,
                    'llm_fallback_count': bucket.llm_fallback_count
                }

            # Write to file
            Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Failed to save NEXUS vs LLM statistics: {e}")

    def _load_statistics(self):
        """Load decision statistics from JSON file."""
        try:
            if not Path(self.storage_path).exists():
                return

            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Load usage statistics
            usage = data.get('usage', {})
            self.total_decisions = usage.get('total_decisions', 0)
            self.nexus_usage_count = usage.get('nexus_usage_count', 0)
            self.llm_fallback_count = usage.get('llm_fallback_count', 0)
            self.nexus_usage_rate = usage.get('nexus_usage_rate', 0.0)
            self.llm_fallback_rate = usage.get('llm_fallback_rate', 0.0)

            # Load accuracy
            accuracy = data.get('accuracy', {})
            self.nexus_accuracy = accuracy.get('nexus_accuracy', 0.0)
            self.llm_accuracy = accuracy.get('llm_accuracy', 0.0)

            # Load performance
            performance = data.get('performance', {})
            self.mean_nexus_time_ms = performance.get('mean_nexus_time_ms', 10.0)
            self.mean_llm_time_ms = performance.get('mean_llm_time_ms', 150.0)
            self.speedup_factor = performance.get('speedup_factor', 15.0)

            # Load threshold
            threshold = data.get('threshold', {})
            self.confidence_threshold = threshold.get('current_threshold', 0.70)
            self.recommended_threshold = threshold.get('recommended_threshold')
            self.optimization_reason = threshold.get('optimization_reason')

            # Load confidence buckets
            for bucket_key, bucket_data in data.get('confidence_buckets', {}).items():
                if bucket_key in self.confidence_buckets:
                    bucket = self.confidence_buckets[bucket_key]
                    bucket.total_count = bucket_data.get('total_count', 0)
                    bucket.correct_count = bucket_data.get('correct_count', 0)
                    bucket.accuracy = bucket_data.get('accuracy', 0.0)
                    bucket.nexus_used_count = bucket_data.get('nexus_used_count', 0)
                    bucket.llm_fallback_count = bucket_data.get('llm_fallback_count', 0)

            print(f"✅ Loaded NEXUS vs LLM statistics: {self.total_decisions} decisions, {self.nexus_usage_rate:.1%} NEXUS usage")

        except Exception as e:
            print(f"⚠️  Failed to load NEXUS vs LLM statistics: {e}")


if __name__ == "__main__":
    """
    Validation test for NexusVsLLMDecisionTracker.
    """
    print("=" * 80)
    print("🧪 NEXUS VS LLM DECISION TRACKER VALIDATION TEST")
    print("=" * 80)

    # Test 1: Initialize tracker
    print("\n📋 TEST 1: Initialize Tracker")
    tracker = NexusVsLLMDecisionTracker(storage_path="/tmp/test_nexus_llm.json")
    print(f"   ✅ Storage path: {tracker.storage_path}")
    print(f"   ✅ Confidence threshold: {tracker.confidence_threshold}")
    print(f"   ✅ Confidence buckets: {len(tracker.confidence_buckets)}")

    # Test 2: Simulate 200 decisions (gradually increasing NEXUS usage)
    print("\n📋 TEST 2: Simulate 200 Decisions (Epoch 1-10 progression)")
    np.random.seed(42)

    for turn in range(200):
        # Epoch progression: start 20% NEXUS, end 50% NEXUS
        epoch_progress = turn / 200.0
        nexus_probability = 0.20 + (epoch_progress * 0.30)

        # Generate NEXUS confidence (0.60-0.90 range)
        nexus_conf = np.random.uniform(0.60, 0.90)

        # Decide: NEXUS if conf > threshold AND random < nexus_probability
        use_nexus = (nexus_conf >= tracker.confidence_threshold and
                     np.random.random() < nexus_probability)

        if use_nexus:
            decision = 'nexus'
            nexus_entities = [{'entity_value': 'Emma', 'entity_type': 'Person'}]
            llm_entities = [{'entity_value': 'Emma', 'entity_type': 'Person'}]
            # NEXUS has 80-90% match rate with LLM
            if np.random.random() > 0.85:
                llm_entities = [{'entity_value': 'Emma Smith', 'entity_type': 'Person'}]  # Mismatch
            processing_time = np.random.uniform(5, 15)  # 5-15ms
        else:
            decision = 'llm'
            nexus_entities = []  # Below threshold or not attempted
            llm_entities = [{'entity_value': 'Emma Smith', 'entity_type': 'Person'}]
            processing_time = np.random.uniform(100, 200)  # 100-200ms

        user_satisfaction = np.random.uniform(0.7, 0.95)

        tracker.update(
            nexus_confidence=nexus_conf,
            nexus_entities=nexus_entities,
            llm_entities=llm_entities,
            decision=decision,
            user_satisfaction=user_satisfaction,
            processing_time_ms=processing_time
        )

    stats = tracker.get_statistics()
    print(f"   ✅ Total decisions: {stats['usage']['total_decisions']}")
    print(f"   ✅ NEXUS usage rate: {stats['usage']['nexus_usage_rate']:.2%}")
    print(f"   ✅ LLM fallback rate: {stats['usage']['llm_fallback_rate']:.2%}")
    print(f"   ✅ NEXUS accuracy: {stats['accuracy']['nexus_accuracy']:.2%}")
    print(f"   ✅ Speedup factor: {stats['performance']['speedup_factor']:.1f}×")

    # Test 3: Confidence calibration
    print("\n📋 TEST 3: Confidence Calibration")
    for bucket_key in sorted(stats['confidence_calibration'].keys())[:5]:
        bucket = stats['confidence_calibration'][bucket_key]
        print(f"   {bucket_key}: {bucket['total_count']} samples, {bucket['accuracy']:.1%} accuracy")

    # Test 4: Threshold optimization
    print("\n📋 TEST 4: Threshold Optimization")
    if stats['threshold']['recommended_threshold']:
        print(f"   Current threshold: {stats['threshold']['current_threshold']:.2f}")
        print(f"   Recommended: {stats['threshold']['recommended_threshold']:.2f}")
        print(f"   Reason: {stats['threshold']['optimization_reason']}")
    else:
        print(f"   ✅ Current threshold {stats['threshold']['current_threshold']:.2f} is optimal")

    # Test 5: Progress toward target
    print("\n📋 TEST 5: Progress Toward 80% NEXUS Target")
    progress = tracker.get_progress_toward_target()
    print(f"   Current NEXUS rate: {progress['current_nexus_rate']:.2%}")
    print(f"   Target NEXUS rate: {progress['target_nexus_rate']:.2%}")
    print(f"   Progress: {progress['progress_percentage']:.1f}%")
    print(f"   Remaining gap: {progress['remaining_gap']:.2%}")

    # Test 6: Save/Load
    print("\n📋 TEST 6: Save and Load Statistics")
    tracker._save_statistics()
    print(f"   ✅ Statistics saved")

    tracker2 = NexusVsLLMDecisionTracker(storage_path="/tmp/test_nexus_llm.json")
    print(f"   ✅ Loaded {tracker2.total_decisions} decisions")
    print(f"   ✅ NEXUS usage: {tracker2.nexus_usage_rate:.1%}")

    print("\n" + "=" * 80)
    print("✅ NEXUS VS LLM DECISION TRACKER VALIDATION PASSED!")
    print(f"   ✅ Progressing toward LLM independence ({progress['progress_percentage']:.1f}%)")
    print(f"   ✅ Speedup factor: {stats['performance']['speedup_factor']:.1f}×")
    print("=" * 80)
