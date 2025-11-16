#!/usr/bin/env python3
"""
Accuracy Sweep Test Suite - Phase 1 Intelligence Emergence Testing
===================================================================

Systematically tests parameter combinations to find optimal settings
for maximizing organic emission rate and system accuracy.

Priority sweeps:
1. Emission thresholds (direct/fusion) - Highest impact
2. Kairos window - Medium impact
3. Coherence thresholds - Validation of DAE 3.0 settings

Date: November 15, 2025
"""

import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


@dataclass
class SweepResult:
    """Results from a single parameter configuration test."""
    # Parameters tested
    direct_threshold: float
    fusion_threshold: float
    kairos_window: Tuple[float, float]

    # Performance metrics
    organic_emission_rate: float
    direct_strategy_rate: float
    fusion_strategy_rate: float
    llm_fallback_rate: float
    mean_emission_confidence: float

    # Nexus & coherence
    mean_nexus_count: float
    nexus_formation_rate: float
    mean_field_coherence: float

    # Kairos
    kairos_detection_rate: float

    # V0 convergence
    mean_convergence_cycles: float
    mean_v0_energy: float

    # Quality proxy (higher is better)
    quality_score: float = 0.0

    def calculate_quality_score(self):
        """
        Calculate composite quality score.

        Weights:
        - Organic rate: 40% (primary goal)
        - Emission confidence: 30% (quality proxy)
        - Nexus formation: 20% (organic enabler)
        - Coherence: 10% (system health)
        """
        self.quality_score = (
            0.40 * self.organic_emission_rate +
            0.30 * self.mean_emission_confidence +
            0.20 * self.nexus_formation_rate +
            0.10 * self.mean_field_coherence
        )


class AccuracySweep:
    """Systematic parameter sweep for accuracy optimization."""

    def __init__(self, test_inputs: List[str]):
        self.test_inputs = test_inputs
        self.results = []

    def sweep_emission_thresholds(
        self,
        direct_range: List[float],
        fusion_range: List[float],
        save_path: str = "results/emission_threshold_sweep.json"
    ) -> List[SweepResult]:
        """
        Sweep emission threshold combinations.

        Tests all valid combinations where fusion < direct (hierarchy maintained).

        Args:
            direct_range: List of direct_threshold values to test
            fusion_range: List of fusion_threshold values to test
            save_path: Where to save results

        Returns:
            List of SweepResult objects
        """
        print("=" * 80)
        print("🎯 EMISSION THRESHOLD SWEEP")
        print("=" * 80)
        print(f"Direct range: {direct_range}")
        print(f"Fusion range: {fusion_range}")
        print(f"Test inputs: {len(self.test_inputs)}")
        print()

        results = []
        total_combos = sum(1 for d in direct_range for f in fusion_range if f < d)
        current_combo = 0

        for direct_thresh in direct_range:
            for fusion_thresh in fusion_range:
                if fusion_thresh >= direct_thresh:
                    continue  # Maintain hierarchy

                current_combo += 1
                print(f"\n{'=' * 80}")
                print(f"Testing {current_combo}/{total_combos}: direct={direct_thresh:.2f}, fusion={fusion_thresh:.2f}")
                print(f"{'=' * 80}")

                # Temporarily override config
                original_direct = Config.EMISSION_DIRECT_THRESHOLD
                original_fusion = Config.EMISSION_FUSION_THRESHOLD

                Config.EMISSION_DIRECT_THRESHOLD = direct_thresh
                Config.EMISSION_FUSION_THRESHOLD = fusion_thresh

                try:
                    # Run test with this configuration
                    result = self._run_test_configuration(
                        direct_threshold=direct_thresh,
                        fusion_threshold=fusion_thresh,
                        kairos_window=(Config.KAIROS_WINDOW_MIN, Config.KAIROS_WINDOW_MAX)
                    )

                    results.append(result)

                    print(f"\n📊 Results:")
                    print(f"   Organic rate: {result.organic_emission_rate*100:.1f}%")
                    print(f"   Mean confidence: {result.mean_emission_confidence:.3f}")
                    print(f"   Quality score: {result.quality_score:.3f}")

                finally:
                    # Restore original config
                    Config.EMISSION_DIRECT_THRESHOLD = original_direct
                    Config.EMISSION_FUSION_THRESHOLD = original_fusion

        # Save results
        self._save_results(results, save_path)

        # Print summary
        self._print_sweep_summary(results, "Emission Threshold")

        return results

    def sweep_kairos_window(
        self,
        windows: List[Tuple[float, float]],
        save_path: str = "results/kairos_window_sweep.json"
    ) -> List[SweepResult]:
        """
        Sweep Kairos window configurations.

        Args:
            windows: List of (min, max) tuples to test
            save_path: Where to save results

        Returns:
            List of SweepResult objects
        """
        print("=" * 80)
        print("⏰ KAIROS WINDOW SWEEP")
        print("=" * 80)
        print(f"Windows to test: {len(windows)}")
        print(f"Test inputs: {len(self.test_inputs)}")
        print()

        results = []

        for i, (window_min, window_max) in enumerate(windows, 1):
            print(f"\n{'=' * 80}")
            print(f"Testing {i}/{len(windows)}: [{window_min:.2f}, {window_max:.2f}]")
            print(f"{'=' * 80}")

            # Temporarily override config
            original_min = Config.KAIROS_WINDOW_MIN
            original_max = Config.KAIROS_WINDOW_MAX

            Config.KAIROS_WINDOW_MIN = window_min
            Config.KAIROS_WINDOW_MAX = window_max

            try:
                # Run test
                result = self._run_test_configuration(
                    direct_threshold=Config.EMISSION_DIRECT_THRESHOLD,
                    fusion_threshold=Config.EMISSION_FUSION_THRESHOLD,
                    kairos_window=(window_min, window_max)
                )

                results.append(result)

                print(f"\n📊 Results:")
                print(f"   Kairos detection: {result.kairos_detection_rate*100:.1f}%")
                print(f"   Organic rate: {result.organic_emission_rate*100:.1f}%")
                print(f"   Quality score: {result.quality_score:.3f}")

            finally:
                # Restore original config
                Config.KAIROS_WINDOW_MIN = original_min
                Config.KAIROS_WINDOW_MAX = original_max

        # Save results
        self._save_results(results, save_path)

        # Print summary
        self._print_sweep_summary(results, "Kairos Window")

        return results

    def _run_test_configuration(
        self,
        direct_threshold: float,
        fusion_threshold: float,
        kairos_window: Tuple[float, float]
    ) -> SweepResult:
        """
        Run test with given configuration on all test inputs.

        Returns aggregated metrics across all inputs.
        """
        # Initialize organism
        organism = ConversationalOrganismWrapper()

        # Metrics tracking
        strategies = defaultdict(int)
        confidences = []
        nexus_counts = []
        field_coherences = []
        kairos_detections = []
        convergence_cycles = []
        v0_energies = []

        # Process each test input
        for user_input in self.test_inputs:
            result = organism.process_text(
                user_input,
                user_id="test_user_sweep",
                enable_phase2=True  # Multi-cycle V0 convergence
            )

            if not result:
                continue

            # Track strategy
            strategy = result.get('emission_path', result.get('strategy', 'unknown'))
            strategies[strategy] += 1

            # Track confidence
            confidence = result.get('emission_confidence', 0.0)
            confidences.append(confidence)

            # Track nexuses
            nexuses = result.get('nexuses', [])
            nexus_counts.append(len(nexuses))

            # Track occasions data
            occasions = result.get('occasions', [])
            if occasions:
                final_occasion = occasions[-1]

                # Field coherence
                if hasattr(final_occasion, 'field_coherence'):
                    field_coherences.append(final_occasion.field_coherence)

                # Kairos
                if hasattr(final_occasion, 'kairos_detected'):
                    kairos_detections.append(1 if final_occasion.kairos_detected else 0)

                # Convergence
                if hasattr(final_occasion, 'cycle'):
                    convergence_cycles.append(final_occasion.cycle)

                # V0 energy
                if hasattr(final_occasion, 'v0_energy'):
                    v0_energies.append(final_occasion.v0_energy)

        # Calculate aggregated metrics
        total_emissions = len(self.test_inputs)

        # Strategy rates
        organic_count = strategies.get('direct', 0) + strategies.get('fusion', 0) + strategies.get('direct_reconstruction', 0)
        llm_count = strategies.get('felt_guided_llm', 0) + strategies.get('hebbian_fallback', 0)

        result = SweepResult(
            direct_threshold=direct_threshold,
            fusion_threshold=fusion_threshold,
            kairos_window=kairos_window,

            organic_emission_rate=organic_count / total_emissions if total_emissions > 0 else 0.0,
            direct_strategy_rate=strategies.get('direct', 0) / total_emissions if total_emissions > 0 else 0.0,
            fusion_strategy_rate=strategies.get('fusion', 0) / total_emissions if total_emissions > 0 else 0.0,
            llm_fallback_rate=llm_count / total_emissions if total_emissions > 0 else 0.0,
            mean_emission_confidence=np.mean(confidences) if confidences else 0.0,

            mean_nexus_count=np.mean(nexus_counts) if nexus_counts else 0.0,
            nexus_formation_rate=sum(1 for n in nexus_counts if n > 0) / len(nexus_counts) if nexus_counts else 0.0,
            mean_field_coherence=np.mean(field_coherences) if field_coherences else 0.0,

            kairos_detection_rate=np.mean(kairos_detections) if kairos_detections else 0.0,

            mean_convergence_cycles=np.mean(convergence_cycles) if convergence_cycles else 0.0,
            mean_v0_energy=np.mean(v0_energies) if v0_energies else 0.0,
        )

        # Calculate quality score
        result.calculate_quality_score()

        return result

    def _save_results(self, results: List[SweepResult], save_path: str):
        """Save results to JSON file."""
        output_path = Path(save_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        results_dict = [asdict(r) for r in results]

        with open(output_path, 'w') as f:
            json.dump(results_dict, f, indent=2)

        print(f"\n💾 Results saved to: {save_path}")

    def _print_sweep_summary(self, results: List[SweepResult], sweep_name: str):
        """Print summary of sweep results."""
        print(f"\n{'=' * 80}")
        print(f"📈 {sweep_name.upper()} SWEEP SUMMARY")
        print(f"{'=' * 80}")

        # Sort by quality score
        sorted_results = sorted(results, key=lambda r: r.quality_score, reverse=True)

        print(f"\n🏆 TOP 3 CONFIGURATIONS:")
        for i, result in enumerate(sorted_results[:3], 1):
            print(f"\n#{i} (Quality: {result.quality_score:.3f})")
            print(f"   Direct threshold: {result.direct_threshold:.2f}")
            print(f"   Fusion threshold: {result.fusion_threshold:.2f}")
            print(f"   Kairos window: [{result.kairos_window[0]:.2f}, {result.kairos_window[1]:.2f}]")
            print(f"   Organic rate: {result.organic_emission_rate*100:.1f}%")
            print(f"   Mean confidence: {result.mean_emission_confidence:.3f}")
            print(f"   Nexus formation: {result.nexus_formation_rate*100:.1f}%")
            print(f"   Field coherence: {result.mean_field_coherence:.3f}")

        print(f"\n📊 RANGE STATISTICS:")
        print(f"   Organic rate: {min(r.organic_emission_rate for r in results)*100:.1f}% - {max(r.organic_emission_rate for r in results)*100:.1f}%")
        print(f"   Quality score: {min(r.quality_score for r in results):.3f} - {max(r.quality_score for r in results):.3f}")
        print(f"   Mean confidence: {min(r.mean_emission_confidence for r in results):.3f} - {max(r.mean_emission_confidence for r in results):.3f}")


def main():
    """Run accuracy sweep tests."""
    import argparse

    parser = argparse.ArgumentParser(description="Run parameter accuracy sweeps")
    parser.add_argument('--sweep', choices=['emission', 'kairos', 'all'], default='emission',
                        help='Which sweep to run (default: emission)')
    parser.add_argument('--num-inputs', type=int, default=10,
                        help='Number of test inputs (default: 10)')

    args = parser.parse_args()

    # Test inputs (diverse conversational scenarios)
    test_inputs = [
        "I'm feeling really overwhelmed right now.",
        "This conversation feels safe and grounded.",
        "I need some space to process.",
        "Can you help me understand what's happening?",
        "I'm noticing a lot of anxiety in my body.",
        "Tell me about my previous conversations.",
        "I feel stuck and don't know what to do.",
        "This is actually helping, thank you.",
        "I'm scared about what might happen.",
        "I think I'm starting to see things more clearly.",
        "Everything feels too much right now.",
        "I appreciate you being here with me.",
        "What do you remember about me?",
        "I'm feeling a bit better now.",
        "Can we talk about my family?",
    ]

    # Use subset if requested
    test_inputs = test_inputs[:args.num_inputs]

    print("=" * 80)
    print("🎯 ACCURACY SWEEP TEST SUITE")
    print("=" * 80)
    print(f"Sweep type: {args.sweep}")
    print(f"Test inputs: {len(test_inputs)}")
    print()

    sweep = AccuracySweep(test_inputs)

    if args.sweep in ['emission', 'all']:
        print("\n🎯 Running EMISSION THRESHOLD sweep...")
        print("This is the HIGHEST PRIORITY sweep (biggest impact on organic rate)")
        print()

        # Emission threshold sweep
        direct_range = [0.40, 0.42, 0.44, 0.46, 0.48, 0.50]
        fusion_range = [0.32, 0.34, 0.36, 0.38, 0.40, 0.42]

        emission_results = sweep.sweep_emission_thresholds(
            direct_range=direct_range,
            fusion_range=fusion_range
        )

    if args.sweep in ['kairos', 'all']:
        print("\n⏰ Running KAIROS WINDOW sweep...")
        print()

        # Kairos window sweep
        windows = [
            (0.25, 0.45),  # Wider lower bound
            (0.28, 0.48),  # Slightly narrower
            (0.30, 0.50),  # Current
            (0.32, 0.48),  # Narrower
            (0.35, 0.50),  # Higher lower bound
        ]

        kairos_results = sweep.sweep_kairos_window(windows=windows)

    print("\n" + "=" * 80)
    print("✅ SWEEP COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review results in results/")
    print("2. Select optimal parameters")
    print("3. Run baseline epoch training with optimal config")


if __name__ == "__main__":
    main()
