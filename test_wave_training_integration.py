#!/usr/bin/env python3
"""
Wave Training Integration Test Suite
=====================================

Comprehensive testing for Phase 1 + 2 wave training integration.

Tests:
1. Satisfaction variance (Phase 1)
2. Field coherence calculation (Phase 2)
3. Nexus formation rate
4. Kairos detection rate
5. Organic emission rate
6. System performance metrics

Date: November 15, 2025
"""

import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


class WaveTrainingMetrics:
    """Comprehensive metrics for wave training validation."""

    def __init__(self):
        self.satisfaction_values = []
        self.satisfaction_raw_values = []
        self.satisfaction_modulated_values = []
        self.appetitive_phases = []
        self.field_coherence_values = []
        self.kairos_detections = []
        self.nexus_counts = []
        self.organic_emissions = 0
        self.llm_emissions = 0
        self.convergence_cycles = []
        self.v0_energies = []

    def record_occasion(self, occasion):
        """Record metrics from a single occasion."""
        self.satisfaction_values.append(occasion.satisfaction)
        if hasattr(occasion, 'satisfaction_raw') and occasion.satisfaction_raw is not None:
            self.satisfaction_raw_values.append(occasion.satisfaction_raw)
        if hasattr(occasion, 'satisfaction_modulated') and occasion.satisfaction_modulated is not None:
            self.satisfaction_modulated_values.append(occasion.satisfaction_modulated)
        if hasattr(occasion, 'appetitive_phase') and occasion.appetitive_phase:
            self.appetitive_phases.append(occasion.appetitive_phase)
        if hasattr(occasion, 'field_coherence'):
            self.field_coherence_values.append(occasion.field_coherence)
        self.kairos_detections.append(occasion.kairos_detected)
        self.v0_energies.append(occasion.v0_energy)

    def record_emission(self, strategy: str, nexus_count: int):
        """Record emission metrics."""
        self.nexus_counts.append(nexus_count)
        if strategy in ['direct', 'fusion', 'multi_phrase']:
            self.organic_emissions += 1
        else:
            self.llm_emissions += 1

    def record_convergence(self, cycles: int):
        """Record convergence metrics."""
        self.convergence_cycles.append(cycles)

    def calculate_metrics(self) -> Dict:
        """Calculate comprehensive metrics."""
        total_emissions = self.organic_emissions + self.llm_emissions

        metrics = {
            # Satisfaction variance (Phase 1 key metric)
            'satisfaction_variance': np.var(self.satisfaction_values) if self.satisfaction_values else 0.0,
            'satisfaction_mean': np.mean(self.satisfaction_values) if self.satisfaction_values else 0.0,
            'satisfaction_std': np.std(self.satisfaction_values) if self.satisfaction_values else 0.0,

            # Wave training modulation effectiveness
            'modulation_variance': 0.0,
            'raw_vs_modulated_diff': 0.0,

            # Appetitive phase distribution
            'phase_distribution': {},

            # Field coherence (Phase 2 key metric)
            'field_coherence_mean': np.mean(self.field_coherence_values) if self.field_coherence_values else 0.0,
            'field_coherence_std': np.std(self.field_coherence_values) if self.field_coherence_values else 0.0,
            'field_coherence_min': min(self.field_coherence_values) if self.field_coherence_values else 0.0,
            'field_coherence_max': max(self.field_coherence_values) if self.field_coherence_values else 0.0,

            # Kairos detection
            'kairos_detection_rate': sum(self.kairos_detections) / len(self.kairos_detections) if self.kairos_detections else 0.0,
            'kairos_count': sum(self.kairos_detections),

            # Nexus formation
            'nexus_formation_rate': sum(1 for n in self.nexus_counts if n > 0) / len(self.nexus_counts) if self.nexus_counts else 0.0,
            'mean_nexus_count': np.mean(self.nexus_counts) if self.nexus_counts else 0.0,
            'max_nexus_count': max(self.nexus_counts) if self.nexus_counts else 0,

            # Organic vs LLM emissions
            'organic_emission_rate': self.organic_emissions / total_emissions if total_emissions > 0 else 0.0,
            'organic_count': self.organic_emissions,
            'llm_count': self.llm_emissions,

            # Convergence
            'mean_convergence_cycles': np.mean(self.convergence_cycles) if self.convergence_cycles else 0.0,

            # V0 energy
            'mean_v0_energy': np.mean(self.v0_energies) if self.v0_energies else 0.0,
        }

        # Calculate modulation effectiveness
        if self.satisfaction_raw_values and self.satisfaction_modulated_values:
            diffs = [abs(raw - mod) for raw, mod in zip(self.satisfaction_raw_values, self.satisfaction_modulated_values)]
            metrics['raw_vs_modulated_diff'] = np.mean(diffs)
            metrics['modulation_variance'] = np.var(self.satisfaction_modulated_values)

        # Calculate phase distribution
        if self.appetitive_phases:
            phase_counts = defaultdict(int)
            for phase in self.appetitive_phases:
                phase_counts[phase] += 1
            total_phases = len(self.appetitive_phases)
            metrics['phase_distribution'] = {
                phase: count / total_phases
                for phase, count in phase_counts.items()
            }

        return metrics


def test_wave_training_integration(num_tests: int = 10) -> Dict:
    """
    Test wave training integration with multiple conversation turns.

    Args:
        num_tests: Number of test inputs to process

    Returns:
        Dict with comprehensive metrics
    """
    print("=" * 80)
    print("🌀 WAVE TRAINING INTEGRATION TEST")
    print("=" * 80)
    print(f"\nTesting {num_tests} conversation turns...")
    print(f"Wave training enabled: {Config.ENABLE_WAVE_TRAINING}")
    print(f"Kairos window: [{Config.KAIROS_WINDOW_MIN}, {Config.KAIROS_WINDOW_MAX}]")
    print()

    # Test inputs covering different emotional/conversational states
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

    # Use subset if num_tests < len(test_inputs)
    test_inputs = test_inputs[:num_tests]

    # Initialize organism
    print("📋 Initializing organism...")
    organism = ConversationalOrganismWrapper()
    print("✅ Organism ready\n")

    # Initialize metrics
    metrics_tracker = WaveTrainingMetrics()

    # Process each test input
    for i, user_input in enumerate(test_inputs, 1):
        print(f"{'=' * 80}")
        print(f"TEST {i}/{len(test_inputs)}: {user_input[:50]}...")
        print(f"{'=' * 80}")

        # Process input
        result = organism.process_text(
            user_input,
            user_id="test_user",
            enable_phase2=True  # 🌀 Enable multi-cycle V0 convergence with wave training
        )

        # Extract metrics
        occasions = []
        if result and 'occasions' in result:
            occasions = result['occasions']

            # Record all occasions
            for occasion in occasions:
                metrics_tracker.record_occasion(occasion)

            # Record convergence
            if occasions:
                final_occasion = occasions[-1]
                metrics_tracker.record_convergence(final_occasion.cycle)

        # Record emission metrics
        if result:
            strategy = result.get('strategy', 'unknown')
            nexus_count = len(result.get('nexuses', []))
            metrics_tracker.record_emission(strategy, nexus_count)

            # Print summary
            print(f"\n📊 Turn {i} Summary:")
            print(f"   Strategy: {strategy}")
            print(f"   Nexuses: {nexus_count}")
            if occasions:
                final = occasions[-1]
                print(f"   Cycles: {final.cycle}")
                print(f"   V0 energy: {final.v0_energy:.3f}")
                print(f"   Satisfaction: {final.satisfaction:.3f}")
                if hasattr(final, 'field_coherence'):
                    print(f"   Field coherence: {final.field_coherence:.3f}")
                if hasattr(final, 'appetitive_phase') and final.appetitive_phase:
                    print(f"   Phase: {final.appetitive_phase}")
                print(f"   Kairos: {final.kairos_detected}")
        print()

    # Calculate final metrics
    print("=" * 80)
    print("📊 CALCULATING METRICS...")
    print("=" * 80)

    final_metrics = metrics_tracker.calculate_metrics()

    # Print results
    print("\n" + "=" * 80)
    print("✅ TEST RESULTS")
    print("=" * 80)

    print("\n🌀 PHASE 1: WAVE TRAINING (Satisfaction Variance)")
    print("-" * 80)
    print(f"   Satisfaction variance: {final_metrics['satisfaction_variance']:.6f}")
    print(f"   Satisfaction mean: {final_metrics['satisfaction_mean']:.3f}")
    print(f"   Satisfaction std: {final_metrics['satisfaction_std']:.3f}")
    print(f"   Raw vs modulated diff: {final_metrics['raw_vs_modulated_diff']:.3f}")

    if final_metrics['phase_distribution']:
        print(f"\n   Appetitive Phase Distribution:")
        for phase, pct in final_metrics['phase_distribution'].items():
            print(f"      {phase}: {pct*100:.1f}%")

    # Validate Phase 1
    phase1_pass = final_metrics['satisfaction_variance'] >= 0.005
    print(f"\n   ✅ Phase 1 Target: variance >= 0.005" if phase1_pass else f"   ⚠️  Phase 1 Target: variance >= 0.005 (got {final_metrics['satisfaction_variance']:.6f})")

    print("\n🌀 PHASE 2: PREHENSIVE FIELDS (Cross-Organ Coherence)")
    print("-" * 80)
    print(f"   Field coherence mean: {final_metrics['field_coherence_mean']:.3f}")
    print(f"   Field coherence std: {final_metrics['field_coherence_std']:.3f}")
    print(f"   Field coherence range: [{final_metrics['field_coherence_min']:.3f}, {final_metrics['field_coherence_max']:.3f}]")

    # Validate Phase 2
    phase2_pass = final_metrics['field_coherence_mean'] > 0.0
    print(f"\n   ✅ Phase 2 Active: coherence > 0.0" if phase2_pass else "   ⚠️  Phase 2 Inactive: coherence = 0.0")

    print("\n🧬 NEXUS FORMATION")
    print("-" * 80)
    print(f"   Nexus formation rate: {final_metrics['nexus_formation_rate']*100:.1f}%")
    print(f"   Mean nexuses per turn: {final_metrics['mean_nexus_count']:.2f}")
    print(f"   Max nexuses: {final_metrics['max_nexus_count']}")

    # Validate nexus formation
    nexus_pass = final_metrics['nexus_formation_rate'] >= 0.10  # At least 10%
    print(f"\n   ✅ Nexus Target: >= 10%" if nexus_pass else f"   ⚠️  Nexus Target: >= 10% (got {final_metrics['nexus_formation_rate']*100:.1f}%)")

    print("\n⏰ KAIROS DETECTION")
    print("-" * 80)
    print(f"   Kairos detection rate: {final_metrics['kairos_detection_rate']*100:.1f}%")
    print(f"   Kairos count: {final_metrics['kairos_count']}")
    print(f"   Current window: [{Config.KAIROS_WINDOW_MIN}, {Config.KAIROS_WINDOW_MAX}]")

    # Kairos tuning recommendations
    if final_metrics['kairos_detection_rate'] < 0.10:
        print(f"\n   💡 Recommendation: Widen Kairos window")
        print(f"      Try: KAIROS_WINDOW_MIN = 0.10, KAIROS_WINDOW_MAX = 0.80")
    elif final_metrics['kairos_detection_rate'] > 0.60:
        print(f"\n   💡 Recommendation: Narrow Kairos window")
        print(f"      Try: KAIROS_WINDOW_MIN = 0.20, KAIROS_WINDOW_MAX = 0.70")
    else:
        print(f"\n   ✅ Kairos window well-tuned")

    print("\n🎯 ORGANIC INTELLIGENCE")
    print("-" * 80)
    print(f"   Organic emission rate: {final_metrics['organic_emission_rate']*100:.1f}%")
    print(f"   Organic count: {final_metrics['organic_count']}")
    print(f"   LLM fallback count: {final_metrics['llm_count']}")

    # Validate organic rate
    organic_pass = final_metrics['organic_emission_rate'] >= 0.10  # At least 10%
    print(f"\n   ✅ Organic Target: >= 10%" if organic_pass else f"   ⚠️  Organic Target: >= 10% (got {final_metrics['organic_emission_rate']*100:.1f}%)")

    print("\n⚡ CONVERGENCE")
    print("-" * 80)
    print(f"   Mean convergence cycles: {final_metrics['mean_convergence_cycles']:.2f}")
    print(f"   Mean V0 energy: {final_metrics['mean_v0_energy']:.3f}")

    print("\n" + "=" * 80)
    print("📈 OVERALL ASSESSMENT")
    print("=" * 80)

    # Overall pass/fail
    all_pass = phase1_pass and phase2_pass and nexus_pass and organic_pass

    if all_pass:
        print("✅ ALL TARGETS MET - Wave training integration successful!")
    else:
        print("⚠️  SOME TARGETS MISSED - See recommendations above")

    # System health
    print(f"\nSystem Health:")
    print(f"   Phase 1 (Variance): {'✅' if phase1_pass else '⚠️'}")
    print(f"   Phase 2 (Coherence): {'✅' if phase2_pass else '⚠️'}")
    print(f"   Nexus Formation: {'✅' if nexus_pass else '⚠️'}")
    print(f"   Organic Intelligence: {'✅' if organic_pass else '⚠️'}")

    return final_metrics


def save_metrics(metrics: Dict, filepath: str = "results/wave_training_metrics.json"):
    """Save metrics to JSON file."""
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"\n💾 Metrics saved to: {filepath}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test wave training integration")
    parser.add_argument('--num-tests', type=int, default=10,
                        help='Number of test inputs to process (default: 10)')
    parser.add_argument('--save', action='store_true',
                        help='Save metrics to JSON file')

    args = parser.parse_args()

    # Run tests
    metrics = test_wave_training_integration(num_tests=args.num_tests)

    # Save if requested
    if args.save:
        save_metrics(metrics)

    print("\n" + "=" * 80)
    print("✅ Test suite complete!")
    print("=" * 80)
