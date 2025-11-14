"""
Responsiveness Test: Latency Measurement (RESP-001)
===================================================

Tests processing latency across different input types and validates
that response times remain within acceptable bounds.

Test Protocol:
1. Measure processing time for various input lengths
2. Test across different complexity levels (crisis, general, meta-cognitive)
3. Validate latency remains below thresholds
4. Check for latency stability (no wild variance)

Success Criteria:
- Mean latency: <200ms for typical inputs
- P95 latency: <500ms (95th percentile)
- P99 latency: <1000ms (99th percentile)
- Latency variance: CV <0.5 (coefficient of variation)

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Responsiveness Testing)
"""

import sys
import time
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


@dataclass
class LatencyMeasurementResult:
    """Result of latency measurement test."""
    samples: int

    # Latency statistics (milliseconds)
    mean_latency: float
    median_latency: float
    p95_latency: float
    p99_latency: float
    min_latency: float
    max_latency: float

    # Variance
    std_latency: float
    cv_latency: float  # Coefficient of variation

    # Success criteria
    mean_acceptable: bool  # <200ms
    p95_acceptable: bool  # <500ms
    p99_acceptable: bool  # <1000ms
    variance_acceptable: bool  # CV <0.5

    # Overall success
    success: bool
    reasoning: str


class LatencyMeasurementTester:
    """Tests processing latency."""

    def __init__(self, organism: Optional[ConversationalOrganismWrapper] = None):
        if organism is None:
            print("🌀 Initializing organism for latency test...")
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism

    def _get_test_inputs(self) -> List[str]:
        """Get diverse test inputs."""
        return [
            "Help.",
            "I'm feeling overwhelmed.",
            "This conversation feels safe.",
            "I need to set a boundary.",
            "I'm in crisis right now.",
            "Can you help me understand this pattern?",
            "I notice I keep repeating the same dynamic.",
            "What happened before this feeling started?",
            "I'm experiencing burnout but feel guilty resting.",
            "Our team has a scapegoat dynamic that's destructive.",
        ]

    def test_latency(self, samples: int = 20, verbose: bool = True) -> LatencyMeasurementResult:
        """Test processing latency."""
        if verbose:
            print(f"\n{'='*70}")
            print(f"⚡ LATENCY MEASUREMENT TEST (RESP-001)")
            print(f"{'='*70}")
            print(f"\nTesting: Processing latency across input types")
            print(f"Samples: {samples}")

        test_inputs = self._get_test_inputs()
        latencies = []

        if verbose:
            print(f"\n📊 Measuring latencies...")

        for i in range(samples):
            text = test_inputs[i % len(test_inputs)]

            start_time = time.perf_counter()
            self.organism.process_text(text, enable_phase2=True, enable_tsk_recording=False)
            end_time = time.perf_counter()

            latency_ms = (end_time - start_time) * 1000
            latencies.append(latency_ms)

            if verbose and (i + 1) % 10 == 0:
                print(f"   Completed {i+1}/{samples} samples...")

        # Compute statistics
        latencies_array = np.array(latencies)
        mean_latency = float(np.mean(latencies_array))
        median_latency = float(np.median(latencies_array))
        p95_latency = float(np.percentile(latencies_array, 95))
        p99_latency = float(np.percentile(latencies_array, 99))
        min_latency = float(np.min(latencies_array))
        max_latency = float(np.max(latencies_array))
        std_latency = float(np.std(latencies_array))
        cv_latency = std_latency / mean_latency if mean_latency > 0 else 0.0

        # Success criteria
        mean_acceptable = mean_latency < 200
        p95_acceptable = p95_latency < 500
        p99_acceptable = p99_latency < 1000
        variance_acceptable = cv_latency < 0.5

        success = mean_acceptable and p95_acceptable and p99_acceptable and variance_acceptable

        if success:
            reasoning = f"Latency acceptable: mean={mean_latency:.1f}ms, p95={p95_latency:.1f}ms"
        else:
            reasons = []
            if not mean_acceptable:
                reasons.append(f"High mean: {mean_latency:.1f}ms ≥ 200ms")
            if not p95_acceptable:
                reasons.append(f"High p95: {p95_latency:.1f}ms ≥ 500ms")
            if not p99_acceptable:
                reasons.append(f"High p99: {p99_latency:.1f}ms ≥ 1000ms")
            if not variance_acceptable:
                reasons.append(f"High variance: CV={cv_latency:.2f} ≥ 0.5")
            reasoning = "; ".join(reasons)

        result = LatencyMeasurementResult(
            samples=samples,
            mean_latency=mean_latency,
            median_latency=median_latency,
            p95_latency=p95_latency,
            p99_latency=p99_latency,
            min_latency=min_latency,
            max_latency=max_latency,
            std_latency=std_latency,
            cv_latency=cv_latency,
            mean_acceptable=mean_acceptable,
            p95_acceptable=p95_acceptable,
            p99_acceptable=p99_acceptable,
            variance_acceptable=variance_acceptable,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result)

        return result

    def _print_results(self, result: LatencyMeasurementResult):
        """Print detailed results."""
        print(f"\n📊 Latency Statistics ({result.samples} samples):")
        print(f"   Mean: {result.mean_latency:.1f}ms")
        print(f"   Median: {result.median_latency:.1f}ms")
        print(f"   P95: {result.p95_latency:.1f}ms")
        print(f"   P99: {result.p99_latency:.1f}ms")
        print(f"   Range: [{result.min_latency:.1f}, {result.max_latency:.1f}]ms")
        print(f"   Std: {result.std_latency:.1f}ms")
        print(f"   CV: {result.cv_latency:.2f}")

        print(f"\n✅ Success Criteria:")
        print(f"   Mean <200ms: {'✅' if result.mean_acceptable else '❌'}")
        print(f"   P95 <500ms: {'✅' if result.p95_acceptable else '❌'}")
        print(f"   P99 <1000ms: {'✅' if result.p99_acceptable else '❌'}")
        print(f"   CV <0.5: {'✅' if result.variance_acceptable else '❌'}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: {result.reasoning}")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_latency_measurement_test(samples: int = 20) -> bool:
    """Run latency measurement test."""
    tester = LatencyMeasurementTester()
    result = tester.test_latency(samples=samples, verbose=True)
    return result.success


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test processing latency")
    parser.add_argument('--samples', type=int, default=20, help='Number of samples')
    args = parser.parse_args()

    success = run_latency_measurement_test(samples=args.samples)
    sys.exit(0 if success else 1)
