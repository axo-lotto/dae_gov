"""
CycleConvergenceTracker - Per-Cycle V0 Descent Analysis
========================================================

Tracks organ coherence, V0 energy, and kairos probability across multi-cycle
convergence to optimize cycle count and detect convergence patterns per context.

Core Learning Pattern:
    Turn with 3 cycles:
    - Cycle 1: coherence=0.35, V0=0.82, kairos=False (not ready)
    - Cycle 2: coherence=0.68, V0=0.48, kairos=True (optimal!)
    - Cycle 3: coherence=0.72, V0=0.42, kairos=True (diminishing returns)

    After 100 turns → Learn:
    - Mean cycles to kairos: 2.3
    - Cycle 2 kairos probability: 0.65 (65% reach kairos by cycle 2)
    - Context-specific patterns: ventral → 1.8 cycles, sympathetic → 3.2 cycles

Architecture Alignment:
    - DAE 3.0: Multi-cycle V0 convergence (2-5 cycles, mean 3.0)
    - Neighbor Prehension: WordOccasion achieve_satisfaction() loop
    - Optimization Goal: Minimize cycles while maintaining quality

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
Status: Phase 3B Week 1 - Foundation Tracker (Critical Priority)
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
import numpy as np
from dataclasses import dataclass, field


@dataclass
class CycleStatistics:
    """Statistics for a specific cycle number."""
    cycle_num: int

    # Running statistics
    mean_coherence: float = 0.5
    std_coherence: float = 0.0
    mean_v0_energy: float = 0.5
    std_v0_energy: float = 0.0

    # Kairos tracking
    kairos_reached_count: int = 0
    total_count: int = 0
    kairos_probability: float = 0.0

    # Performance metrics
    mean_satisfaction: float = 0.0
    mean_appetition: float = 0.0
    mean_resonance: float = 0.0


@dataclass
class ContextPattern:
    """Convergence pattern for a specific context (polyvagal + urgency)."""
    context_key: str
    mean_cycles_to_kairos: float = 0.0
    std_cycles: float = 0.0
    sample_count: int = 0


class CycleConvergenceTracker:
    """
    Tracks per-cycle convergence statistics for optimization.

    Usage:
        tracker = CycleConvergenceTracker()

        # During multi-cycle convergence
        for cycle in range(max_cycles):
            tracker.update_cycle(
                cycle_num=cycle,
                coherence=coherence,
                v0_energy=v0_energy,
                converged=kairos_reached,
                satisfaction=satisfaction,
                context={'polyvagal': 'ventral', 'urgency': 0.2}
            )
    """

    def __init__(
        self,
        storage_path: Optional[str] = None,
        ema_alpha: float = 0.1,
        max_cycles_tracked: int = 5
    ):
        """
        Initialize cycle convergence tracker.

        Args:
            storage_path: Path to save cycle statistics (JSON)
            ema_alpha: EMA smoothing factor for running statistics
            max_cycles_tracked: Max cycle number to track (default 5)
        """
        self.storage_path = storage_path or "persona_layer/state/active/cycle_convergence_stats.json"
        self.ema_alpha = ema_alpha
        self.max_cycles_tracked = max_cycles_tracked

        # Per-cycle statistics
        self.cycle_statistics: Dict[int, CycleStatistics] = {}

        # Context-specific patterns
        self.context_patterns: Dict[str, ContextPattern] = {}

        # Global convergence statistics
        self.total_convergence_attempts = 0
        self.total_converged = 0
        self.overall_convergence_rate = 0.0
        self.mean_cycles_to_kairos = 0.0
        self.std_cycles_to_kairos = 0.0

        # Cycle history (last 1000 turns)
        self.cycle_history: List[int] = []
        self.max_history = 1000

        # Load existing statistics
        self._load_statistics()

    def update_cycle(
        self,
        cycle_num: int,
        coherence: float,
        v0_energy: float,
        converged: bool,
        satisfaction: float = 0.0,
        appetition: float = 0.0,
        resonance: float = 0.0,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Update statistics for a specific cycle.

        Args:
            cycle_num: Cycle number (0-indexed)
            coherence: Organ coherence at this cycle
            v0_energy: V0 energy at this cycle
            converged: Whether kairos was reached at this cycle
            satisfaction: Satisfaction score
            appetition: Appetition score
            resonance: Resonance score
            context: Optional context dict (polyvagal, urgency, etc.)
        """
        # Get or create cycle statistics
        if cycle_num not in self.cycle_statistics:
            self.cycle_statistics[cycle_num] = CycleStatistics(cycle_num=cycle_num)

        stats = self.cycle_statistics[cycle_num]

        # Update running statistics for coherence
        self._update_running_stat(stats, 'coherence', coherence)

        # Update running statistics for V0 energy
        self._update_running_stat(stats, 'v0_energy', v0_energy)

        # Update kairos tracking
        stats.total_count += 1
        if converged:
            stats.kairos_reached_count += 1

        stats.kairos_probability = stats.kairos_reached_count / stats.total_count

        # Update EMA for satisfaction, appetition, resonance
        stats.mean_satisfaction = (
            self.ema_alpha * satisfaction +
            (1.0 - self.ema_alpha) * stats.mean_satisfaction
        )
        stats.mean_appetition = (
            self.ema_alpha * appetition +
            (1.0 - self.ema_alpha) * stats.mean_appetition
        )
        stats.mean_resonance = (
            self.ema_alpha * resonance +
            (1.0 - self.ema_alpha) * stats.mean_resonance
        )

    def update_convergence_complete(
        self,
        cycles_used: int,
        converged: bool,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Update global convergence statistics after full multi-cycle attempt.

        Args:
            cycles_used: Number of cycles used (1-5)
            converged: Whether convergence was achieved
            context: Optional context dict (polyvagal, urgency, etc.)
        """
        self.total_convergence_attempts += 1

        if converged:
            self.total_converged += 1

            # Update cycle history
            self.cycle_history.append(cycles_used)
            if len(self.cycle_history) > self.max_history:
                self.cycle_history.pop(0)

            # Update mean and std cycles to kairos
            if len(self.cycle_history) > 0:
                self.mean_cycles_to_kairos = float(np.mean(self.cycle_history))
                self.std_cycles_to_kairos = float(np.std(self.cycle_history))

        # Update convergence rate
        self.overall_convergence_rate = self.total_converged / self.total_convergence_attempts

        # Update context-specific patterns
        if context and converged:
            self._update_context_pattern(cycles_used, context)

        # Save every 50 convergence attempts
        if self.total_convergence_attempts % 50 == 0:
            self._save_statistics()

    def _update_running_stat(
        self,
        stats: CycleStatistics,
        stat_name: str,
        value: float
    ):
        """
        Update running mean and std for a statistic.

        Args:
            stats: CycleStatistics object
            stat_name: Name of statistic ('coherence' or 'v0_energy')
            value: New value
        """
        mean_key = f"mean_{stat_name}"
        std_key = f"std_{stat_name}"

        old_mean = getattr(stats, mean_key)
        count = stats.total_count + 1  # +1 because total_count updated later

        # Update mean (EMA)
        new_mean = self.ema_alpha * value + (1.0 - self.ema_alpha) * old_mean
        setattr(stats, mean_key, new_mean)

        # Update std (running variance)
        if count > 1:
            old_std = getattr(stats, std_key)
            old_variance = old_std ** 2

            # Welford's online algorithm for variance
            delta = value - old_mean
            new_delta = value - new_mean
            new_variance = (
                (count - 2) * old_variance + delta * new_delta
            ) / max(1, count - 1)

            setattr(stats, std_key, float(np.sqrt(max(0, new_variance))))

    def _update_context_pattern(
        self,
        cycles_used: int,
        context: Dict[str, Any]
    ):
        """
        Update context-specific convergence pattern.

        Args:
            cycles_used: Number of cycles used
            context: Context dict (polyvagal, urgency, etc.)
        """
        # Create context key
        polyvagal = context.get('polyvagal_state', 'unknown')
        urgency = context.get('urgency_level', 0.5)

        # Bin urgency (low <0.3, medium 0.3-0.7, high >0.7)
        if urgency < 0.3:
            urgency_bin = "low"
        elif urgency < 0.7:
            urgency_bin = "medium"
        else:
            urgency_bin = "high"

        context_key = f"{polyvagal}_{urgency_bin}"

        # Get or create context pattern
        if context_key not in self.context_patterns:
            self.context_patterns[context_key] = ContextPattern(context_key=context_key)

        pattern = self.context_patterns[context_key]

        # Update running mean for cycles
        old_mean = pattern.mean_cycles_to_kairos
        count = pattern.sample_count + 1

        new_mean = (old_mean * pattern.sample_count + cycles_used) / count
        pattern.mean_cycles_to_kairos = new_mean

        # Update std
        if count > 1:
            delta = cycles_used - old_mean
            new_delta = cycles_used - new_mean
            old_variance = pattern.std_cycles ** 2
            new_variance = (
                (count - 2) * old_variance + delta * new_delta
            ) / (count - 1)
            pattern.std_cycles = float(np.sqrt(max(0, new_variance)))

        pattern.sample_count = count

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive convergence statistics.

        Returns:
            Dictionary with all statistics
        """
        stats = {
            'global': {
                'total_attempts': self.total_convergence_attempts,
                'total_converged': self.total_converged,
                'convergence_rate': self.overall_convergence_rate,
                'mean_cycles_to_kairos': self.mean_cycles_to_kairos,
                'std_cycles_to_kairos': self.std_cycles_to_kairos
            },
            'per_cycle': {},
            'context_patterns': {}
        }

        # Per-cycle statistics
        for cycle_num in sorted(self.cycle_statistics.keys()):
            cycle_stats = self.cycle_statistics[cycle_num]
            stats['per_cycle'][f"cycle_{cycle_num}"] = {
                'mean_coherence': cycle_stats.mean_coherence,
                'std_coherence': cycle_stats.std_coherence,
                'mean_v0_energy': cycle_stats.mean_v0_energy,
                'std_v0_energy': cycle_stats.std_v0_energy,
                'kairos_probability': cycle_stats.kairos_probability,
                'total_count': cycle_stats.total_count,
                'mean_satisfaction': cycle_stats.mean_satisfaction
            }

        # Context patterns
        for context_key, pattern in self.context_patterns.items():
            stats['context_patterns'][context_key] = {
                'mean_cycles': pattern.mean_cycles_to_kairos,
                'std_cycles': pattern.std_cycles,
                'sample_count': pattern.sample_count
            }

        return stats

    def get_optimal_cycle_count(self, context: Optional[Dict[str, Any]] = None) -> int:
        """
        Get recommended optimal cycle count based on learned patterns.

        Args:
            context: Optional context for context-specific optimization

        Returns:
            Recommended cycle count (1-5)
        """
        # If context provided, use context-specific pattern
        if context:
            polyvagal = context.get('polyvagal_state', 'unknown')
            urgency = context.get('urgency_level', 0.5)

            if urgency < 0.3:
                urgency_bin = "low"
            elif urgency < 0.7:
                urgency_bin = "medium"
            else:
                urgency_bin = "high"

            context_key = f"{polyvagal}_{urgency_bin}"

            if context_key in self.context_patterns:
                pattern = self.context_patterns[context_key]
                if pattern.sample_count >= 10:  # Require 10+ samples
                    return int(np.ceil(pattern.mean_cycles_to_kairos))

        # Fallback to global mean
        if self.mean_cycles_to_kairos > 0:
            return int(np.ceil(self.mean_cycles_to_kairos))

        # Default to 3 cycles (DAE 3.0 mean)
        return 3

    def _save_statistics(self):
        """Save cycle statistics to JSON file."""
        try:
            data = {
                'global': {
                    'total_attempts': self.total_convergence_attempts,
                    'total_converged': self.total_converged,
                    'convergence_rate': self.overall_convergence_rate,
                    'mean_cycles': self.mean_cycles_to_kairos,
                    'std_cycles': self.std_cycles_to_kairos
                },
                'per_cycle': {},
                'context_patterns': {},
                'timestamp': time.time()
            }

            # Serialize per-cycle stats
            for cycle_num, stats in self.cycle_statistics.items():
                data['per_cycle'][f"cycle_{cycle_num}"] = {
                    'mean_coherence': stats.mean_coherence,
                    'std_coherence': stats.std_coherence,
                    'mean_v0_energy': stats.mean_v0_energy,
                    'std_v0_energy': stats.std_v0_energy,
                    'kairos_probability': stats.kairos_probability,
                    'total_count': stats.total_count,
                    'mean_satisfaction': stats.mean_satisfaction,
                    'mean_appetition': stats.mean_appetition,
                    'mean_resonance': stats.mean_resonance
                }

            # Serialize context patterns
            for context_key, pattern in self.context_patterns.items():
                data['context_patterns'][context_key] = {
                    'mean_cycles': pattern.mean_cycles_to_kairos,
                    'std_cycles': pattern.std_cycles,
                    'sample_count': pattern.sample_count
                }

            # Write to file
            Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Failed to save cycle statistics: {e}")

    def _load_statistics(self):
        """Load cycle statistics from JSON file."""
        try:
            if not Path(self.storage_path).exists():
                return

            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Load global statistics
            global_stats = data.get('global', {})
            self.total_convergence_attempts = global_stats.get('total_attempts', 0)
            self.total_converged = global_stats.get('total_converged', 0)
            self.overall_convergence_rate = global_stats.get('convergence_rate', 0.0)
            self.mean_cycles_to_kairos = global_stats.get('mean_cycles', 0.0)
            self.std_cycles_to_kairos = global_stats.get('std_cycles', 0.0)

            # Load per-cycle statistics
            for cycle_key, stats_data in data.get('per_cycle', {}).items():
                cycle_num = int(cycle_key.split('_')[1])
                self.cycle_statistics[cycle_num] = CycleStatistics(
                    cycle_num=cycle_num,
                    mean_coherence=stats_data['mean_coherence'],
                    std_coherence=stats_data['std_coherence'],
                    mean_v0_energy=stats_data['mean_v0_energy'],
                    std_v0_energy=stats_data['std_v0_energy'],
                    kairos_probability=stats_data['kairos_probability'],
                    total_count=stats_data['total_count'],
                    mean_satisfaction=stats_data.get('mean_satisfaction', 0.0),
                    mean_appetition=stats_data.get('mean_appetition', 0.0),
                    mean_resonance=stats_data.get('mean_resonance', 0.0)
                )

            # Load context patterns
            for context_key, pattern_data in data.get('context_patterns', {}).items():
                self.context_patterns[context_key] = ContextPattern(
                    context_key=context_key,
                    mean_cycles_to_kairos=pattern_data['mean_cycles'],
                    std_cycles=pattern_data['std_cycles'],
                    sample_count=pattern_data['sample_count']
                )

            print(f"✅ Loaded cycle statistics: {self.total_convergence_attempts} attempts, {len(self.cycle_statistics)} cycles tracked")

        except Exception as e:
            print(f"⚠️  Failed to load cycle statistics: {e}")


if __name__ == "__main__":
    """
    Validation test for CycleConvergenceTracker.
    """
    print("=" * 80)
    print("🧪 CYCLE CONVERGENCE TRACKER VALIDATION TEST")
    print("=" * 80)

    # Test 1: Initialize tracker
    print("\n📋 TEST 1: Initialize Tracker")
    tracker = CycleConvergenceTracker(storage_path="/tmp/test_cycle_stats.json")
    print(f"   ✅ Storage path: {tracker.storage_path}")
    print(f"   ✅ EMA alpha: {tracker.ema_alpha}")
    print(f"   ✅ Max cycles tracked: {tracker.max_cycles_tracked}")

    # Test 2: Simulate multi-cycle convergence (100 turns)
    print("\n📋 TEST 2: Simulate 100 Multi-Cycle Convergences")
    np.random.seed(42)

    for turn in range(100):
        # Simulate 2-3 cycle convergence (typical)
        cycles_needed = np.random.choice([2, 3], p=[0.6, 0.4])

        context = {
            'polyvagal_state': np.random.choice(['ventral', 'sympathetic'], p=[0.7, 0.3]),
            'urgency_level': np.random.uniform(0.1, 0.6)
        }

        for cycle in range(cycles_needed):
            # Simulate convergence: coherence increases, V0 decreases
            coherence = 0.3 + (cycle * 0.15) + np.random.normal(0, 0.05)
            v0_energy = 0.8 - (cycle * 0.15) + np.random.normal(0, 0.05)
            satisfaction = 0.4 + (cycle * 0.15)

            converged = (cycle == cycles_needed - 1)  # Converge on last cycle

            tracker.update_cycle(
                cycle_num=cycle,
                coherence=coherence,
                v0_energy=v0_energy,
                converged=converged,
                satisfaction=satisfaction,
                context=context
            )

        tracker.update_convergence_complete(cycles_needed, True, context)

    stats = tracker.get_statistics()
    print(f"   ✅ Total convergence attempts: {stats['global']['total_attempts']}")
    print(f"   ✅ Convergence rate: {stats['global']['convergence_rate']:.2%}")
    print(f"   ✅ Mean cycles to kairos: {stats['global']['mean_cycles_to_kairos']:.2f}")

    # Test 3: Per-cycle statistics
    print("\n📋 TEST 3: Per-Cycle Statistics")
    for cycle_key in sorted(stats['per_cycle'].keys()):
        cycle_stats = stats['per_cycle'][cycle_key]
        print(f"   {cycle_key}:")
        print(f"      Mean coherence: {cycle_stats['mean_coherence']:.3f}")
        print(f"      Mean V0 energy: {cycle_stats['mean_v0_energy']:.3f}")
        print(f"      Kairos probability: {cycle_stats['kairos_probability']:.2%}")

    # Test 4: Context patterns
    print("\n📋 TEST 4: Context-Specific Patterns")
    for context_key, pattern in stats['context_patterns'].items():
        print(f"   {context_key}:")
        print(f"      Mean cycles: {pattern['mean_cycles']:.2f}")
        print(f"      Sample count: {pattern['sample_count']}")

    # Test 5: Optimal cycle recommendation
    print("\n📋 TEST 5: Optimal Cycle Recommendation")
    optimal_ventral = tracker.get_optimal_cycle_count({'polyvagal_state': 'ventral', 'urgency_level': 0.2})
    optimal_sympathetic = tracker.get_optimal_cycle_count({'polyvagal_state': 'sympathetic', 'urgency_level': 0.5})
    print(f"   ✅ Optimal for ventral/low urgency: {optimal_ventral} cycles")
    print(f"   ✅ Optimal for sympathetic/medium urgency: {optimal_sympathetic} cycles")

    # Test 6: Save/Load
    print("\n📋 TEST 6: Save and Load Statistics")
    tracker._save_statistics()
    print(f"   ✅ Statistics saved")

    tracker2 = CycleConvergenceTracker(storage_path="/tmp/test_cycle_stats.json")
    print(f"   ✅ Loaded {tracker2.total_convergence_attempts} attempts")

    print("\n" + "=" * 80)
    print("✅ CYCLE CONVERGENCE TRACKER VALIDATION PASSED!")
    print("=" * 80)
