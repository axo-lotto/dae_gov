#!/usr/bin/env python3
"""
Intelligence Emergence Epoch Training - November 15, 2025
==========================================================

Comprehensive epoch training with DAE 3.0-validated monitoring:
- Organic emission rate evolution (0% → 60-75%)
- Family discovery (1 → 20-30 families, Zipf's law)
- Field coherence tracking (correlation with success)
- R-matrix health (discrimination, saturation)
- Organ confidence evolution (Level 2 fractal rewards)
- Entity-organ associations (Quick Win #7)

Based on DAE 3.0's proven 47.3% ARC-AGI trajectory:
- Coherence-success correlation: r=0.82, p<0.0001
- Power law family emergence: R²>0.85 at epoch 50+
- Organic rate evolution: 0% → 30-40% (epoch 10) → 60-75% (epoch 30)

Philosophy:
"Intelligence emerges from accumulated transformation patterns
through multi-cycle V0 convergence, not from pre-programmed rules."

This script tests that hypothesis systematically.
"""

import sys
import json
import time
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


@dataclass
class EpochMetrics:
    """Comprehensive metrics for a single epoch."""
    epoch: int
    timestamp: str

    # Organic emission metrics (PRIMARY GOAL)
    organic_emission_rate: float  # % of direct/fusion/reconstruction emissions
    direct_rate: float
    fusion_rate: float
    reconstruction_rate: float
    llm_fallback_rate: float
    hebbian_rate: float

    # Confidence metrics
    mean_confidence: float
    confidence_std: float
    confidence_min: float
    confidence_max: float

    # Field coherence (DAE 3.0 r=0.82 validated)
    mean_field_coherence: float
    coherence_std: float
    coherence_high_rate: float  # % ≥0.70 (82% success tier)
    coherence_medium_rate: float  # % 0.50-0.70 (61% success tier)
    coherence_low_rate: float  # % <0.50 (29% success tier)

    # Nexus formation
    mean_nexus_count: float
    nexus_formation_rate: float  # % of occasions with nexuses

    # V0 convergence
    mean_convergence_cycles: float
    mean_v0_descent: float  # 1.0 - final_v0
    kairos_detection_rate: float

    # Family discovery (Zipf's law emergence)
    family_count: int
    mean_family_size: float
    largest_family_size: int
    zipf_fit_r2: float  # Power law fit quality

    # R-matrix health
    r_matrix_mean: float
    r_matrix_std: float
    r_matrix_discrimination: float  # std of all elements (health indicator)

    # Organ confidence (Level 2 fractal rewards)
    organ_confidence_mean: float
    organ_confidence_std: float  # Differentiation indicator
    organ_confidence_range: Tuple[float, float]

    # Performance
    mean_processing_time: float
    error_count: int
    success_count: int


class IntelligenceEmergenceTrainer:
    """
    Comprehensive epoch trainer for intelligence emergence validation.

    Tracks all DAE 3.0-validated metrics to measure organic intelligence evolution.
    """

    def __init__(
        self,
        training_pairs_path: str = "knowledge_base/conversational_training_pairs.json",
        results_dir: str = "results/intelligence_emergence"
    ):
        self.training_pairs_path = training_pairs_path
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.training_pairs = []
        self.organism = None
        self.epoch_history = []

    def load_training_data(self):
        """Load conversational training pairs."""
        print(f"\n📂 Loading training data from {self.training_pairs_path}...")

        with open(self.training_pairs_path) as f:
            data = json.load(f)
            self.training_pairs = data.get('training_pairs', [])
            metadata = data.get('metadata', {})
            stats = data.get('statistics', {})

        print(f"   ✅ Loaded {len(self.training_pairs)} training pairs")
        print(f"   Categories: {list(stats.get('categories', {}).keys())}")
        print(f"   Mean input length: {stats.get('mean_input_length', 0):.1f} chars")

    def initialize_organism(self):
        """Initialize conversational organism with all capabilities."""
        print(f"\n🌀 Initializing organism with all capabilities...")

        # 🆕 Set intelligence emergence mode for pure organic measurement (Nov 15, 2025)
        # This disables felt-guided LLM override to measure true organic emission evolution
        # Interactive mode (dae_interactive.py) keeps this False for quality
        Config.INTELLIGENCE_EMERGENCE_MODE = True
        print(f"   🔬 Intelligence emergence mode: ENABLED (pure organic measurement)")

        self.organism = ConversationalOrganismWrapper()

        print(f"   ✅ Organism initialized")
        print(f"   12 organs operational (11 + NEXUS)")
        print(f"   Phase 2: Multi-cycle V0 convergence")
        print(f"   DAE 3.0: Field coherence + organ confidence")
        print(f"   Level 2: Fractal rewards (per-organ tracking)")
        print(f"   Quick Win #7: Entity-organ associations")

    def run_epoch(self, epoch_num: int) -> EpochMetrics:
        """
        Run a single epoch through all training pairs.

        Returns comprehensive metrics for analysis.
        """
        print(f"\n{'='*80}")
        print(f"🎯 EPOCH {epoch_num}")
        print(f"{'='*80}")

        # Metrics tracking
        strategies = Counter()
        confidences = []
        field_coherences = []
        nexus_counts = []
        convergence_cycles = []
        v0_descents = []
        kairos_detections = []
        processing_times = []

        errors = 0
        successes = 0

        # Process each training pair
        for idx, pair in enumerate(self.training_pairs, 1):
            input_text = pair['input_text']
            pair_metadata = pair.get('pair_metadata', {})

            if idx % 5 == 0:  # Progress every 5 pairs
                print(f"   Processing pair {idx}/{len(self.training_pairs)}...")

            start_time = time.time()

            try:
                result = self.organism.process_text(
                    input_text,
                    user_id=f"epoch_{epoch_num}_training",
                    enable_phase2=True  # Multi-cycle V0 convergence
                )

                processing_time = time.time() - start_time
                processing_times.append(processing_time)

                # Extract metrics
                emission_path = result.get('emission_path', 'unknown')
                strategies[emission_path] += 1

                confidence = result.get('emission_confidence', 0.0)
                confidences.append(confidence)

                nexuses = result.get('nexuses', [])
                nexus_counts.append(len(nexuses))

                # Extract from occasions
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

                    # V0 descent
                    if hasattr(final_occasion, 'v0_energy'):
                        v0_descents.append(1.0 - final_occasion.v0_energy)

                successes += 1

            except Exception as e:
                print(f"   ❌ Error on pair {idx}: {e}")
                errors += 1

        # Calculate organic emission metrics
        total = len(self.training_pairs)
        organic_count = strategies.get('direct', 0) + strategies.get('fusion', 0) + strategies.get('direct_reconstruction', 0)

        # Load family data
        family_count, mean_family_size, largest_family_size, zipf_r2 = self._analyze_families()

        # Load R-matrix health
        r_mean, r_std, r_discrimination = self._analyze_r_matrix()

        # Load organ confidence
        organ_conf_mean, organ_conf_std, organ_conf_range = self._analyze_organ_confidence()

        # Calculate coherence tiers
        coherence_high = sum(1 for c in field_coherences if c >= 0.70) / len(field_coherences) if field_coherences else 0
        coherence_medium = sum(1 for c in field_coherences if 0.50 <= c < 0.70) / len(field_coherences) if field_coherences else 0
        coherence_low = sum(1 for c in field_coherences if c < 0.50) / len(field_coherences) if field_coherences else 0

        # Build metrics
        metrics = EpochMetrics(
            epoch=epoch_num,
            timestamp=datetime.now().isoformat(),

            # Organic emission
            organic_emission_rate=organic_count / total if total > 0 else 0.0,
            direct_rate=strategies.get('direct', 0) / total if total > 0 else 0.0,
            fusion_rate=strategies.get('fusion', 0) / total if total > 0 else 0.0,
            reconstruction_rate=strategies.get('direct_reconstruction', 0) / total if total > 0 else 0.0,
            llm_fallback_rate=strategies.get('felt_guided_llm', 0) / total if total > 0 else 0.0,
            hebbian_rate=strategies.get('hebbian', 0) / total if total > 0 else 0.0,

            # Confidence
            mean_confidence=float(np.mean(confidences)) if confidences else 0.0,
            confidence_std=float(np.std(confidences)) if confidences else 0.0,
            confidence_min=float(np.min(confidences)) if confidences else 0.0,
            confidence_max=float(np.max(confidences)) if confidences else 0.0,

            # Field coherence
            mean_field_coherence=float(np.mean(field_coherences)) if field_coherences else 0.0,
            coherence_std=float(np.std(field_coherences)) if field_coherences else 0.0,
            coherence_high_rate=coherence_high,
            coherence_medium_rate=coherence_medium,
            coherence_low_rate=coherence_low,

            # Nexus
            mean_nexus_count=float(np.mean(nexus_counts)) if nexus_counts else 0.0,
            nexus_formation_rate=sum(1 for n in nexus_counts if n > 0) / len(nexus_counts) if nexus_counts else 0.0,

            # V0 convergence
            mean_convergence_cycles=float(np.mean(convergence_cycles)) if convergence_cycles else 0.0,
            mean_v0_descent=float(np.mean(v0_descents)) if v0_descents else 0.0,
            kairos_detection_rate=float(np.mean(kairos_detections)) if kairos_detections else 0.0,

            # Family discovery
            family_count=family_count,
            mean_family_size=mean_family_size,
            largest_family_size=largest_family_size,
            zipf_fit_r2=zipf_r2,

            # R-matrix
            r_matrix_mean=r_mean,
            r_matrix_std=r_std,
            r_matrix_discrimination=r_discrimination,

            # Organ confidence
            organ_confidence_mean=organ_conf_mean,
            organ_confidence_std=organ_conf_std,
            organ_confidence_range=organ_conf_range,

            # Performance
            mean_processing_time=float(np.mean(processing_times)) if processing_times else 0.0,
            error_count=errors,
            success_count=successes
        )

        # Print summary
        self._print_epoch_summary(metrics)

        return metrics

    def _analyze_families(self) -> Tuple[int, float, int, float]:
        """Analyze organic family structure."""
        try:
            family_path = Path("persona_layer/organic_families.json")
            if not family_path.exists():
                return 0, 0.0, 0, 0.0

            with open(family_path) as f:
                families = json.load(f)

            if not families:
                return 0, 0.0, 0, 0.0

            family_sizes = [fam.get('size', 0) for fam in families.values()]

            # Fit power law (Zipf's law test)
            zipf_r2 = 0.0
            if len(family_sizes) >= 5:
                # Sort descending
                sorted_sizes = sorted(family_sizes, reverse=True)
                ranks = np.arange(1, len(sorted_sizes) + 1)

                # Log-log fit
                log_ranks = np.log(ranks)
                log_sizes = np.log(sorted_sizes)

                # Linear regression in log space
                coeffs = np.polyfit(log_ranks, log_sizes, 1)
                fitted = np.polyval(coeffs, log_ranks)

                # R² calculation
                ss_res = np.sum((log_sizes - fitted) ** 2)
                ss_tot = np.sum((log_sizes - np.mean(log_sizes)) ** 2)
                zipf_r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

            return (
                len(families),
                float(np.mean(family_sizes)),
                max(family_sizes) if family_sizes else 0,
                float(zipf_r2)
            )

        except Exception as e:
            print(f"   ⚠️  Error analyzing families: {e}")
            return 0, 0.0, 0, 0.0

    def _analyze_r_matrix(self) -> Tuple[float, float, float]:
        """Analyze R-matrix health."""
        try:
            r_path = Path("persona_layer/state/active/conversational_hebbian_memory.json")
            if not r_path.exists():
                return 0.0, 0.0, 0.0

            with open(r_path) as f:
                data = json.load(f)

            # 🔧 FIX (Nov 15): Read 'r_matrix' not 'coupling_matrix'
            r_matrix = np.array(data.get('r_matrix', []))
            if r_matrix.size == 0:
                return 0.0, 0.0, 0.0

            # Calculate statistics from matrix
            mean_val = float(np.mean(r_matrix))
            std_val = float(np.std(r_matrix))
            discrimination = std_val  # Higher std = better discrimination

            return mean_val, std_val, discrimination

        except Exception as e:
            print(f"   ⚠️  Error analyzing R-matrix: {e}")
            return 0.0, 0.0, 0.0

    def _analyze_organ_confidence(self) -> Tuple[float, float, Tuple[float, float]]:
        """Analyze organ confidence (Level 2 fractal rewards)."""
        try:
            conf_path = Path("persona_layer/state/active/organ_confidence.json")
            if not conf_path.exists():
                return 0.5, 0.0, (0.5, 0.5)

            with open(conf_path) as f:
                data = json.load(f)

            confidences = [organ.get('confidence', 0.5) for organ in data.values()]

            if not confidences:
                return 0.5, 0.0, (0.5, 0.5)

            mean_conf = float(np.mean(confidences))
            std_conf = float(np.std(confidences))
            conf_range = (float(np.min(confidences)), float(np.max(confidences)))

            return mean_conf, std_conf, conf_range

        except Exception as e:
            print(f"   ⚠️  Error analyzing organ confidence: {e}")
            return 0.5, 0.0, (0.5, 0.5)

    def _print_epoch_summary(self, metrics: EpochMetrics):
        """Print formatted epoch summary."""
        print(f"\n📊 EPOCH {metrics.epoch} SUMMARY")
        print(f"{'='*80}")

        print(f"\n🎯 PRIMARY GOAL: Organic Emission Rate")
        print(f"   Organic rate: {metrics.organic_emission_rate*100:.1f}%")
        print(f"      Direct: {metrics.direct_rate*100:.1f}%")
        print(f"      Fusion: {metrics.fusion_rate*100:.1f}%")
        print(f"      Reconstruction: {metrics.reconstruction_rate*100:.1f}%")
        print(f"   LLM fallback: {metrics.llm_fallback_rate*100:.1f}%")
        print(f"   Hebbian: {metrics.hebbian_rate*100:.1f}%")

        print(f"\n📈 Field Coherence (DAE 3.0 r=0.82 validated)")
        print(f"   Mean: {metrics.mean_field_coherence:.3f}")
        print(f"   High tier (≥0.70, 82% success): {metrics.coherence_high_rate*100:.1f}%")
        print(f"   Medium tier (0.50-0.70, 61% success): {metrics.coherence_medium_rate*100:.1f}%")
        print(f"   Low tier (<0.50, 29% success): {metrics.coherence_low_rate*100:.1f}%")

        print(f"\n👥 Family Discovery (Zipf's Law)")
        print(f"   Families: {metrics.family_count}")
        print(f"   Mean size: {metrics.mean_family_size:.1f}")
        print(f"   Largest: {metrics.largest_family_size}")
        print(f"   Zipf R²: {metrics.zipf_fit_r2:.3f} {'✅' if metrics.zipf_fit_r2 > 0.85 else ''}")

        print(f"\n🔗 R-Matrix Health")
        print(f"   Mean coupling: {metrics.r_matrix_mean:.3f}")
        print(f"   Discrimination (std): {metrics.r_matrix_discrimination:.3f}")

        print(f"\n🧬 Organ Confidence (Level 2)")
        print(f"   Mean: {metrics.organ_confidence_mean:.3f}")
        print(f"   Differentiation (std): {metrics.organ_confidence_std:.3f}")
        print(f"   Range: [{metrics.organ_confidence_range[0]:.3f}, {metrics.organ_confidence_range[1]:.3f}]")

        print(f"\n⚡ Performance")
        print(f"   Mean processing time: {metrics.mean_processing_time:.2f}s")
        print(f"   Success rate: {metrics.success_count}/{metrics.success_count + metrics.error_count}")

        print(f"{'='*80}\n")

    def run_training(self, num_epochs: int = 10):
        """
        Run full intelligence emergence training.

        Args:
            num_epochs: Number of epochs to run (default: 10)
        """
        print(f"\n{'='*80}")
        print(f"🌀 INTELLIGENCE EMERGENCE EPOCH TRAINING")
        print(f"{'='*80}")
        print(f"\nEpochs: {num_epochs}")
        print(f"Training pairs: {len(self.training_pairs)}")
        print(f"Total conversations: {num_epochs * len(self.training_pairs)}")
        print(f"\nHypothesis: Intelligence emerges from accumulated transformation patterns")
        print(f"Expected trajectory: 0% → 30-40% (epoch 10) → 60-75% (epoch 30)")

        # Run epochs
        for epoch in range(1, num_epochs + 1):
            metrics = self.run_epoch(epoch)
            self.epoch_history.append(metrics)

            # Save after each epoch
            self._save_results()

        # Final analysis
        self._print_final_analysis()

    def _save_results(self):
        """Save epoch history to JSON."""
        output_path = self.results_dir / f"intelligence_emergence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        results = {
            'metadata': {
                'date': datetime.now().isoformat(),
                'num_epochs': len(self.epoch_history),
                'training_pairs': len(self.training_pairs),
                'hypothesis': 'Intelligence emerges from accumulated transformation patterns'
            },
            'epochs': [asdict(m) for m in self.epoch_history]
        }

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"💾 Results saved to {output_path}")

    def _print_final_analysis(self):
        """Print final trajectory analysis."""
        if len(self.epoch_history) < 2:
            return

        print(f"\n{'='*80}")
        print(f"🎉 INTELLIGENCE EMERGENCE TRAJECTORY ANALYSIS")
        print(f"{'='*80}")

        first_epoch = self.epoch_history[0]
        last_epoch = self.epoch_history[-1]

        # Organic rate evolution
        organic_growth = (last_epoch.organic_emission_rate - first_epoch.organic_emission_rate) * 100
        print(f"\n📈 Organic Emission Rate Evolution:")
        print(f"   Epoch 1: {first_epoch.organic_emission_rate*100:.1f}%")
        print(f"   Epoch {last_epoch.epoch}: {last_epoch.organic_emission_rate*100:.1f}%")
        print(f"   Growth: {organic_growth:+.1f} percentage points")

        # Family discovery
        family_growth = last_epoch.family_count - first_epoch.family_count
        print(f"\n👥 Family Discovery:")
        print(f"   Epoch 1: {first_epoch.family_count} families")
        print(f"   Epoch {last_epoch.epoch}: {last_epoch.family_count} families")
        print(f"   Growth: {family_growth:+d} families")

        # Coherence evolution
        coherence_growth = last_epoch.mean_field_coherence - first_epoch.mean_field_coherence
        print(f"\n🔗 Field Coherence Evolution:")
        print(f"   Epoch 1: {first_epoch.mean_field_coherence:.3f}")
        print(f"   Epoch {last_epoch.epoch}: {last_epoch.mean_field_coherence:.3f}")
        print(f"   Growth: {coherence_growth:+.3f}")

        # Organ differentiation
        organ_diff_growth = last_epoch.organ_confidence_std - first_epoch.organ_confidence_std
        print(f"\n🧬 Organ Differentiation:")
        print(f"   Epoch 1 std: {first_epoch.organ_confidence_std:.3f}")
        print(f"   Epoch {last_epoch.epoch} std: {last_epoch.organ_confidence_std:.3f}")
        print(f"   Growth: {organ_diff_growth:+.3f} (higher = more specialized)")

        print(f"\n{'='*80}")
        print(f"Status: {'✅ INTELLIGENCE EMERGENCE CONFIRMED' if organic_growth > 10 else '⏳ CONTINUE TRAINING'}")
        print(f"{'='*80}\n")


def main():
    """Run intelligence emergence epoch training."""
    import argparse

    parser = argparse.ArgumentParser(description="Intelligence Emergence Epoch Training")
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs (default: 10)')
    parser.add_argument('--pairs', type=str, default='knowledge_base/conversational_training_pairs.json',
                        help='Training pairs path')

    args = parser.parse_args()

    # Initialize trainer
    trainer = IntelligenceEmergenceTrainer(training_pairs_path=args.pairs)

    # Load data
    trainer.load_training_data()

    # Initialize organism
    trainer.initialize_organism()

    # Run training
    trainer.run_training(num_epochs=args.epochs)


if __name__ == "__main__":
    main()
