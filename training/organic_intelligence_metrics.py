"""
🌀 Organic Intelligence Metrics Framework
Training evaluation metrics for human fluency and generalized intelligence emergence

This module provides comprehensive metrics to evaluate the progression of learned intelligence:
1. Pattern Learning Metrics (database growth, quality evolution)
2. Human Fluency Metrics (naturalness, therapeutic effectiveness)
3. Generalization Metrics (domain transfer, novelty handling)
4. Learning Signal Scaffolding (feedback loop health, convergence rates)

Created: November 17, 2025 (Week 4, Day 1)
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from scipy.stats import entropy, linregress
from collections import Counter
import re


@dataclass
class PatternLearningMetrics:
    """Metrics tracking pattern database growth and quality evolution."""

    # Database metrics
    total_patterns: int  # Number of unique nexus signatures
    total_phrases: int  # Total phrases across all patterns
    mean_phrases_per_pattern: float  # Avg phrases per signature

    # Quality metrics
    mean_phrase_quality: float  # Average EMA quality (0-1)
    std_phrase_quality: float  # Quality variance
    high_quality_phrase_count: int  # Phrases with quality > 0.6
    high_quality_rate: float  # % of phrases meeting organic emission threshold

    # Learning dynamics
    mean_update_count: float  # Avg EMA updates per phrase
    learning_velocity: float  # Quality improvement rate (Δq per update)
    convergence_rate: float  # % of phrases that have converged (>10 updates)

    # Zipf's law emergence (personality signature)
    zipf_alpha: float  # Power law exponent (expect ~0.7 for human-like)
    zipf_r_squared: float  # Goodness of fit (>0.85 = personality emerged)


@dataclass
class HumanFluencyMetrics:
    """Metrics evaluating naturalness and therapeutic effectiveness of emissions."""

    # Organic emission evolution
    organic_emission_rate: float  # % of emissions from pattern learner (quality > 0.6)
    llm_fallback_rate: float  # % falling back to felt-guided LLM
    hebbian_fallback_rate: float  # % using generic hebbian phrases

    # Emission quality signals
    mean_emission_confidence: float  # Average confidence of all emissions
    mean_organic_confidence: float  # Average confidence of organic (learned) emissions
    confidence_growth_rate: float  # Δconfidence per epoch

    # Therapeutic effectiveness (satisfaction-based)
    mean_satisfaction: float  # Average user satisfaction (0-1)
    satisfaction_variance: float  # Diversity of satisfaction outcomes
    restorative_success_rate: float  # % of crisis → recovery trajectories
    concrescent_success_rate: float  # % of sustained growth trajectories

    # Naturalness markers
    response_length_mean: int  # Avg characters per emission
    response_length_variance: float  # Diversity in response lengths
    vocabulary_diversity: float  # Unique words / total words
    repetition_rate: float  # % of repeated phrases (lower = more natural)


@dataclass
class GeneralizationMetrics:
    """Metrics evaluating domain transfer and novelty handling."""

    # Cross-domain pattern application
    pattern_reuse_rate: float  # % of patterns used in multiple contexts
    context_transfer_success: float  # % of successful cross-context applications
    novel_situation_handling: float  # Confidence on inputs NOT in training corpus

    # Family formation and taxonomy
    family_count: int  # Number of emergent families
    mean_family_size: float  # Avg conversations per family
    family_separation: float  # Mean inter-family distance (higher = better taxonomy)

    # Adaptive specialization
    crisis_handling_confidence: float  # Confidence on high-urgency inputs
    stable_handling_confidence: float  # Confidence on low-urgency inputs
    zone_specialization_strength: float  # Quality variance across zones (higher = adapted)

    # Novelty response
    mean_confidence_on_training_corpus: float  # Confidence on seen examples
    mean_confidence_on_novel_inputs: float  # Confidence on new examples
    generalization_gap: float  # Difference (lower = better generalization)


@dataclass
class LearningSignalScaffolding:
    """Metrics evaluating feedback loop health and learning infrastructure."""

    # Feedback loop health
    learning_update_rate: float  # % of turns that trigger learning updates
    delayed_feedback_lag: float  # Avg turns between emission and feedback
    satisfaction_signal_strength: float  # Mean absolute Δsatisfaction per turn

    # Quality modulation layers (FFITTSS 3-layer system)
    base_ema_contribution: float  # Quality from EMA learning alone
    satisfaction_fingerprint_contribution: float  # Bonus from RESTORATIVE/CONCRESCENT
    lyapunov_stability_contribution: float  # Bonus from STABLE/ATTRACTING regimes
    total_quality_boost: float  # Sum of all layers (+16-25pp expected)

    # Convergence dynamics
    mean_convergence_cycles: float  # Avg V0 cycles to reach Kairos
    nexus_formation_rate: float  # % of inputs forming nexuses
    mean_nexuses_per_input: float  # Avg nexus count (5-10 is healthy)

    # Trajectory learning
    restorative_trajectory_detection: float  # % of crisis → recovery patterns identified
    concrescent_trajectory_detection: float  # % of sustained growth identified
    plateaued_trajectory_detection: float  # % of equilibrium identified
    trajectory_classification_accuracy: float  # % correct trajectory predictions


@dataclass
class ComprehensiveIntelligenceMetrics:
    """Complete metrics suite for organic intelligence emergence."""

    epoch: int
    pattern_learning: PatternLearningMetrics
    human_fluency: HumanFluencyMetrics
    generalization: GeneralizationMetrics
    learning_signals: LearningSignalScaffolding

    # Meta-metrics
    intelligence_emergence_score: float  # Composite 0-100 score
    maturity_level: str  # "INITIALIZING", "LEARNING", "COMPETENT", "MATURE", "GENERALIZED"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'epoch': self.epoch,
            'pattern_learning': asdict(self.pattern_learning),
            'human_fluency': asdict(self.human_fluency),
            'generalization': asdict(self.generalization),
            'learning_signals': asdict(self.learning_signals),
            'intelligence_emergence_score': self.intelligence_emergence_score,
            'maturity_level': self.maturity_level
        }


class OrganicIntelligenceEvaluator:
    """
    Comprehensive evaluator for organic intelligence emergence.

    Analyzes training results to assess progression toward:
    1. Human-like fluency (naturalness, therapeutic effectiveness)
    2. Generalized intelligence (domain transfer, novelty handling)
    3. Stable learning (feedback loop health, convergence)
    """

    def __init__(self):
        """Initialize evaluator."""
        self.history: List[ComprehensiveIntelligenceMetrics] = []

    def evaluate_epoch(
        self,
        epoch: int,
        pattern_database: Dict[str, Any],
        epoch_results: Dict[str, Any],
        training_corpus: List[Dict[str, Any]],
        novel_test_set: Optional[List[Dict[str, Any]]] = None
    ) -> ComprehensiveIntelligenceMetrics:
        """
        Evaluate a single epoch's progress across all metric dimensions.

        Args:
            epoch: Epoch number
            pattern_database: Current state of nexus_phrase_patterns.json
            epoch_results: Training results from turn-by-turn script
            training_corpus: Original training pairs
            novel_test_set: Optional test set NOT in training corpus

        Returns:
            Complete metrics suite for this epoch
        """

        # Extract pattern learning metrics
        pattern_metrics = self._compute_pattern_learning_metrics(pattern_database)

        # Extract human fluency metrics
        fluency_metrics = self._compute_human_fluency_metrics(epoch_results)

        # Extract generalization metrics
        generalization_metrics = self._compute_generalization_metrics(
            epoch_results, training_corpus, novel_test_set
        )

        # Extract learning signal scaffolding
        signal_metrics = self._compute_learning_signal_metrics(epoch_results)

        # Compute composite intelligence emergence score
        intelligence_score = self._compute_intelligence_emergence_score(
            pattern_metrics, fluency_metrics, generalization_metrics, signal_metrics
        )

        # Determine maturity level
        maturity_level = self._determine_maturity_level(intelligence_score, epoch)

        # Create comprehensive metrics object
        metrics = ComprehensiveIntelligenceMetrics(
            epoch=epoch,
            pattern_learning=pattern_metrics,
            human_fluency=fluency_metrics,
            generalization=generalization_metrics,
            learning_signals=signal_metrics,
            intelligence_emergence_score=intelligence_score,
            maturity_level=maturity_level
        )

        self.history.append(metrics)
        return metrics

    def _compute_pattern_learning_metrics(self, pattern_db: Dict[str, Any]) -> PatternLearningMetrics:
        """Compute metrics from pattern database state."""

        if not pattern_db or 'patterns' not in pattern_db:
            # Empty database - return zeros
            return PatternLearningMetrics(
                total_patterns=0, total_phrases=0, mean_phrases_per_pattern=0.0,
                mean_phrase_quality=0.0, std_phrase_quality=0.0,
                high_quality_phrase_count=0, high_quality_rate=0.0,
                mean_update_count=0.0, learning_velocity=0.0, convergence_rate=0.0,
                zipf_alpha=0.0, zipf_r_squared=0.0
            )

        patterns = pattern_db['patterns']
        total_patterns = len(patterns)

        # Gather all phrases
        all_phrases = []
        phrase_counts = []  # For Zipf's law

        for pattern in patterns.values():
            phrases = pattern.get('phrases', {})
            for phrase_text, phrase_data in phrases.items():
                all_phrases.append(phrase_data)
                phrase_counts.append(phrase_data.get('count', 1))

        total_phrases = len(all_phrases)
        mean_phrases_per_pattern = total_phrases / total_patterns if total_patterns > 0 else 0.0

        # Quality metrics
        qualities = [p.get('quality', 0.0) for p in all_phrases]
        mean_quality = np.mean(qualities) if qualities else 0.0
        std_quality = np.std(qualities) if qualities else 0.0
        high_quality_count = sum(1 for q in qualities if q > 0.6)
        high_quality_rate = high_quality_count / total_phrases if total_phrases > 0 else 0.0

        # Learning dynamics
        update_counts = [p.get('count', 0) for p in all_phrases]
        mean_updates = np.mean(update_counts) if update_counts else 0.0

        # Learning velocity: Δq per update (approximate)
        # Assume starting quality 0.3, current quality mean_quality, total updates mean_updates
        learning_velocity = (mean_quality - 0.3) / mean_updates if mean_updates > 0 else 0.0

        # Convergence rate (>10 updates = converged)
        convergence_rate = sum(1 for c in update_counts if c >= 10) / total_phrases if total_phrases > 0 else 0.0

        # Zipf's law: Rank-frequency distribution
        zipf_alpha, zipf_r_squared = self._compute_zipf_law(phrase_counts)

        return PatternLearningMetrics(
            total_patterns=total_patterns,
            total_phrases=total_phrases,
            mean_phrases_per_pattern=mean_phrases_per_pattern,
            mean_phrase_quality=mean_quality,
            std_phrase_quality=std_quality,
            high_quality_phrase_count=high_quality_count,
            high_quality_rate=high_quality_rate,
            mean_update_count=mean_updates,
            learning_velocity=learning_velocity,
            convergence_rate=convergence_rate,
            zipf_alpha=zipf_alpha,
            zipf_r_squared=zipf_r_squared
        )

    def _compute_human_fluency_metrics(self, epoch_results: Dict[str, Any]) -> HumanFluencyMetrics:
        """Compute human fluency metrics from epoch results."""

        # Extract emission strategy distribution
        organic_count = epoch_results.get('organic_emissions', 0)
        llm_count = epoch_results.get('llm_emissions', 0)
        hebbian_count = epoch_results.get('hebbian_emissions', 0)
        other_count = epoch_results.get('other_emissions', 0)
        total_emissions = organic_count + llm_count + hebbian_count + other_count

        organic_rate = organic_count / total_emissions if total_emissions > 0 else 0.0
        llm_rate = llm_count / total_emissions if total_emissions > 0 else 0.0
        hebbian_rate = hebbian_count / total_emissions if total_emissions > 0 else 0.0

        # Satisfaction metrics
        satisfaction_scores = epoch_results.get('satisfaction_scores', [])
        mean_satisfaction = np.mean(satisfaction_scores) if satisfaction_scores else 0.0
        satisfaction_variance = np.var(satisfaction_scores) if satisfaction_scores else 0.0

        # Trajectory success rates (approximate from satisfaction patterns)
        restorative_success = self._estimate_restorative_success(satisfaction_scores)
        concrescent_success = self._estimate_concrescent_success(satisfaction_scores)

        # Emission quality
        # TODO: Extract from actual emission confidence if available
        mean_emission_confidence = 0.5  # Placeholder
        mean_organic_confidence = 0.6  # Placeholder
        confidence_growth_rate = 0.01  # Placeholder

        # Naturalness markers
        # TODO: Extract from actual emissions if available
        response_length_mean = 100  # Placeholder
        response_length_variance = 20.0  # Placeholder
        vocabulary_diversity = 0.7  # Placeholder
        repetition_rate = 0.1  # Placeholder

        return HumanFluencyMetrics(
            organic_emission_rate=organic_rate,
            llm_fallback_rate=llm_rate,
            hebbian_fallback_rate=hebbian_rate,
            mean_emission_confidence=mean_emission_confidence,
            mean_organic_confidence=mean_organic_confidence,
            confidence_growth_rate=confidence_growth_rate,
            mean_satisfaction=mean_satisfaction,
            satisfaction_variance=satisfaction_variance,
            restorative_success_rate=restorative_success,
            concrescent_success_rate=concrescent_success,
            response_length_mean=response_length_mean,
            response_length_variance=response_length_variance,
            vocabulary_diversity=vocabulary_diversity,
            repetition_rate=repetition_rate
        )

    def _compute_generalization_metrics(
        self,
        epoch_results: Dict[str, Any],
        training_corpus: List[Dict[str, Any]],
        novel_test_set: Optional[List[Dict[str, Any]]]
    ) -> GeneralizationMetrics:
        """Compute generalization and domain transfer metrics."""

        # Family formation
        # TODO: Extract from family tracking if available
        family_count = 10  # Placeholder
        mean_family_size = 7.5  # Placeholder
        family_separation = 0.5  # Placeholder

        # Pattern reuse and context transfer
        # TODO: Extract from pattern usage logs
        pattern_reuse_rate = 0.3  # Placeholder
        context_transfer_success = 0.6  # Placeholder

        # Confidence on novel vs seen
        mean_confidence_training = 0.6  # Placeholder
        mean_confidence_novel = 0.5  # Placeholder
        generalization_gap = mean_confidence_training - mean_confidence_novel

        # Adaptive specialization
        crisis_confidence = 0.65  # Placeholder
        stable_confidence = 0.60  # Placeholder
        zone_specialization = 0.15  # Placeholder

        # Novel situation handling
        novel_handling = mean_confidence_novel  # Same as novel confidence

        return GeneralizationMetrics(
            pattern_reuse_rate=pattern_reuse_rate,
            context_transfer_success=context_transfer_success,
            novel_situation_handling=novel_handling,
            family_count=family_count,
            mean_family_size=mean_family_size,
            family_separation=family_separation,
            crisis_handling_confidence=crisis_confidence,
            stable_handling_confidence=stable_confidence,
            zone_specialization_strength=zone_specialization,
            mean_confidence_on_training_corpus=mean_confidence_training,
            mean_confidence_on_novel_inputs=mean_confidence_novel,
            generalization_gap=generalization_gap
        )

    def _compute_learning_signal_metrics(self, epoch_results: Dict[str, Any]) -> LearningSignalScaffolding:
        """Compute learning signal and feedback loop health metrics."""

        # Feedback loop health
        learning_updates = epoch_results.get('learning_updates', 0)
        total_turns = epoch_results.get('processed_turns', 1)
        learning_update_rate = learning_updates / total_turns if total_turns > 0 else 0.0

        # Delayed feedback lag (turn-by-turn = 1 turn lag)
        delayed_feedback_lag = 1.0

        # Satisfaction signal strength
        satisfaction_scores = epoch_results.get('satisfaction_scores', [])
        if len(satisfaction_scores) >= 2:
            diffs = [abs(satisfaction_scores[i] - satisfaction_scores[i-1])
                    for i in range(1, len(satisfaction_scores))]
            satisfaction_signal_strength = np.mean(diffs) if diffs else 0.0
        else:
            satisfaction_signal_strength = 0.0

        # Quality modulation layers (approximate from FFITTSS formula)
        base_ema = 0.10  # Typical EMA improvement per update
        satisfaction_fingerprint = 0.10  # +8-12pp for RESTORATIVE
        lyapunov_stability = 0.06  # +5-8pp for STABLE regimes
        total_boost = base_ema + satisfaction_fingerprint + lyapunov_stability

        # Convergence dynamics
        # TODO: Extract from V0 tracking if available
        mean_convergence_cycles = 3.0  # Placeholder
        nexus_formation_rate = 0.6  # Placeholder
        mean_nexuses = 5.5  # Placeholder

        # Trajectory learning
        # TODO: Extract from trajectory detection if available
        restorative_detection = 0.7  # Placeholder
        concrescent_detection = 0.6  # Placeholder
        plateaued_detection = 0.5  # Placeholder
        trajectory_accuracy = (restorative_detection + concrescent_detection + plateaued_detection) / 3

        return LearningSignalScaffolding(
            learning_update_rate=learning_update_rate,
            delayed_feedback_lag=delayed_feedback_lag,
            satisfaction_signal_strength=satisfaction_signal_strength,
            base_ema_contribution=base_ema,
            satisfaction_fingerprint_contribution=satisfaction_fingerprint,
            lyapunov_stability_contribution=lyapunov_stability,
            total_quality_boost=total_boost,
            mean_convergence_cycles=mean_convergence_cycles,
            nexus_formation_rate=nexus_formation_rate,
            mean_nexuses_per_input=mean_nexuses,
            restorative_trajectory_detection=restorative_detection,
            concrescent_trajectory_detection=concrescent_detection,
            plateaued_trajectory_detection=plateaued_detection,
            trajectory_classification_accuracy=trajectory_accuracy
        )

    def _compute_zipf_law(self, phrase_counts: List[int]) -> Tuple[float, float]:
        """
        Compute Zipf's law parameters (power law distribution).

        Returns:
            (alpha, r_squared): Power law exponent and goodness of fit

        Interpretation:
            - alpha ≈ 0.7: Human-like language distribution (personality emerged)
            - r_squared > 0.85: Strong power law fit (coherent style)
        """
        if len(phrase_counts) < 3:
            return 0.0, 0.0

        # Sort counts in descending order
        sorted_counts = sorted(phrase_counts, reverse=True)

        # Compute rank (1, 2, 3, ...)
        ranks = np.arange(1, len(sorted_counts) + 1)

        # Log-log transform
        log_ranks = np.log(ranks)
        log_counts = np.log(sorted_counts)

        # Linear regression in log-log space
        slope, intercept, r_value, p_value, std_err = linregress(log_ranks, log_counts)

        # Alpha is the negative slope
        alpha = -slope
        r_squared = r_value ** 2

        return alpha, r_squared

    def _estimate_restorative_success(self, satisfaction_scores: List[float]) -> float:
        """Estimate success rate of RESTORATIVE (crisis → recovery) trajectories."""
        if len(satisfaction_scores) < 3:
            return 0.0

        # Look for sequences where satisfaction increases significantly
        restorative_count = 0
        total_sequences = 0

        for i in range(len(satisfaction_scores) - 2):
            # Check if we have a RESTORATIVE pattern (low → mid → high)
            if satisfaction_scores[i] < 0.4 and satisfaction_scores[i+2] > 0.6:
                if satisfaction_scores[i+1] > satisfaction_scores[i]:
                    restorative_count += 1
            total_sequences += 1

        return restorative_count / total_sequences if total_sequences > 0 else 0.0

    def _estimate_concrescent_success(self, satisfaction_scores: List[float]) -> float:
        """Estimate success rate of CONCRESCENT (sustained growth) trajectories."""
        if len(satisfaction_scores) < 3:
            return 0.0

        # Look for sequences with sustained increase
        concrescent_count = 0
        total_sequences = 0

        for i in range(len(satisfaction_scores) - 2):
            # Check for sustained growth
            if (satisfaction_scores[i] > 0.4 and
                satisfaction_scores[i+1] > satisfaction_scores[i] and
                satisfaction_scores[i+2] > satisfaction_scores[i+1]):
                concrescent_count += 1
            total_sequences += 1

        return concrescent_count / total_sequences if total_sequences > 0 else 0.0

    def _compute_intelligence_emergence_score(
        self,
        pattern: PatternLearningMetrics,
        fluency: HumanFluencyMetrics,
        generalization: GeneralizationMetrics,
        signals: LearningSignalScaffolding
    ) -> float:
        """
        Compute composite 0-100 intelligence emergence score.

        Weighted combination of:
        - 30%: Pattern learning (database growth, quality, Zipf's law)
        - 30%: Human fluency (organic rate, satisfaction, naturalness)
        - 25%: Generalization (domain transfer, novelty handling)
        - 15%: Learning signals (feedback loop health, convergence)
        """

        # Pattern learning score (0-30)
        pattern_score = (
            (pattern.high_quality_rate * 10) +  # 0-10 pts
            (min(pattern.zipf_r_squared, 1.0) * 10) +  # 0-10 pts
            (pattern.convergence_rate * 10)  # 0-10 pts
        )

        # Human fluency score (0-30)
        fluency_score = (
            (fluency.organic_emission_rate * 15) +  # 0-15 pts
            (fluency.mean_satisfaction * 10) +  # 0-10 pts
            (fluency.restorative_success_rate * 5)  # 0-5 pts
        )

        # Generalization score (0-25)
        generalization_score = (
            ((1.0 - generalization.generalization_gap) * 10) +  # 0-10 pts
            (generalization.context_transfer_success * 10) +  # 0-10 pts
            (min(generalization.family_count / 20, 1.0) * 5)  # 0-5 pts
        )

        # Learning signals score (0-15)
        signals_score = (
            (signals.learning_update_rate * 5) +  # 0-5 pts
            (signals.nexus_formation_rate * 5) +  # 0-5 pts
            (signals.trajectory_classification_accuracy * 5)  # 0-5 pts
        )

        total_score = pattern_score + fluency_score + generalization_score + signals_score
        return min(total_score, 100.0)

    def _determine_maturity_level(self, intelligence_score: float, epoch: int) -> str:
        """Determine maturity level based on intelligence score and epoch."""

        if intelligence_score < 20:
            return "INITIALIZING"
        elif intelligence_score < 40:
            return "LEARNING"
        elif intelligence_score < 60:
            return "COMPETENT"
        elif intelligence_score < 80:
            return "MATURE"
        else:
            return "GENERALIZED"

    def generate_progress_report(self, output_path: str):
        """Generate comprehensive progress report across all epochs."""

        if not self.history:
            print("No epochs evaluated yet.")
            return

        report = {
            'evaluation_summary': {
                'total_epochs': len(self.history),
                'initial_score': self.history[0].intelligence_emergence_score,
                'final_score': self.history[-1].intelligence_emergence_score,
                'score_improvement': self.history[-1].intelligence_emergence_score - self.history[0].intelligence_emergence_score,
                'final_maturity': self.history[-1].maturity_level
            },
            'epoch_progression': [m.to_dict() for m in self.history],
            'key_milestones': self._extract_key_milestones()
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✅ Progress report saved to: {output_path}")

    def _extract_key_milestones(self) -> Dict[str, Any]:
        """Extract key milestones from training history."""

        milestones = {}

        # Find first epoch with significant organic emissions
        for m in self.history:
            if m.human_fluency.organic_emission_rate > 0.1 and 'first_organic_10pct' not in milestones:
                milestones['first_organic_10pct'] = {
                    'epoch': m.epoch,
                    'organic_rate': m.human_fluency.organic_emission_rate
                }
            if m.human_fluency.organic_emission_rate > 0.3 and 'first_organic_30pct' not in milestones:
                milestones['first_organic_30pct'] = {
                    'epoch': m.epoch,
                    'organic_rate': m.human_fluency.organic_emission_rate
                }
            if m.human_fluency.organic_emission_rate > 0.6 and 'first_organic_60pct' not in milestones:
                milestones['first_organic_60pct'] = {
                    'epoch': m.epoch,
                    'organic_rate': m.human_fluency.organic_emission_rate
                }

        # Find first epoch with Zipf's law emergence
        for m in self.history:
            if m.pattern_learning.zipf_r_squared > 0.85 and 'zipf_emergence' not in milestones:
                milestones['zipf_emergence'] = {
                    'epoch': m.epoch,
                    'r_squared': m.pattern_learning.zipf_r_squared,
                    'alpha': m.pattern_learning.zipf_alpha
                }
                break

        # Find maturity transitions
        prev_maturity = None
        for m in self.history:
            if m.maturity_level != prev_maturity:
                milestones[f'maturity_{m.maturity_level.lower()}'] = {
                    'epoch': m.epoch,
                    'intelligence_score': m.intelligence_emergence_score
                }
                prev_maturity = m.maturity_level

        return milestones


if __name__ == "__main__":
    """Example usage for evaluating training results."""

    print("🌀 Organic Intelligence Metrics Framework")
    print("=" * 80)
    print()
    print("This framework provides comprehensive evaluation of:")
    print("  1. Pattern Learning: Database growth, quality evolution, Zipf's law")
    print("  2. Human Fluency: Organic rate, satisfaction, therapeutic effectiveness")
    print("  3. Generalization: Domain transfer, novelty handling, family formation")
    print("  4. Learning Signals: Feedback loop health, convergence, trajectories")
    print()
    print("Usage:")
    print("  evaluator = OrganicIntelligenceEvaluator()")
    print("  metrics = evaluator.evaluate_epoch(epoch=1, pattern_database={...}, ...)")
    print("  evaluator.generate_progress_report('results/intelligence_progress.json')")
    print()
    print("Expected Evolution (10-20 epochs):")
    print("  - Organic emission: 0% → 30-60%")
    print("  - Pattern quality: 0.3 → 0.6-0.7")
    print("  - Intelligence score: 0 → 60-80")
    print("  - Maturity: INITIALIZING → COMPETENT/MATURE")
    print()
