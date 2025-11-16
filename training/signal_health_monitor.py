#!/usr/bin/env python3
"""
Signal Health Monitor - FFITTSS-Inspired Signal Tracking
=========================================================

Monitors critical signals for organic intelligence emergence:
1. Organ Agreement (FAO pairwise agreement)
2. Multiplicity Index (Whiteheadian specialization)
3. Family Separation Quality (Euclidean distances)
4. Organ Confidence Differentiation
5. Nexus Density

Inspired by FFITTSS SIGNAL_AUDIT.md findings:
- Nexus density < 0.95 → -15.44pp penalty (strongest predictor)
- coh_F ≥ 0.76 → 31.63% accuracy

Date: November 16, 2025
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SignalHealthReport:
    """Signal health assessment for epoch."""
    mean_pairwise_agreement: float
    mean_organ_entropy: float
    mean_multiplicity_index: float
    mean_nexus_coherence: float
    mean_max_disagreement: float

    organ_confidence_std: float
    organ_confidence_range: float

    inter_family_distance_mean: float
    inter_family_distance_std: float

    overall_health_score: float
    warnings: List[str]
    recommendations: List[str]


class SignalHealthMonitor:
    """
    Monitors signal health for organic intelligence emergence.

    Key signals tracked (from FFITTSS T4/SIGNAL_AUDIT.md):
    1. Pairwise Agreement: Organ consensus (should be 0.7-0.9)
    2. Multiplicity Index: Specialization (0.1-0.3)
    3. Organ Confidence Std: Differentiation (target >0.15)
    4. Inter-family Distances: Separation quality (target >1.5)
    """

    def __init__(self):
        # Optimal ranges from FFITTSS research
        self.thresholds = {
            'pairwise_agreement': {'min': 0.6, 'optimal': 0.85, 'max': 0.95},
            'organ_entropy': {'min': 0.7, 'optimal': 0.95, 'max': 1.0},
            'multiplicity_index': {'min': 0.05, 'optimal': 0.15, 'max': 0.35},
            'nexus_coherence': {'min': 0.5, 'optimal': 0.75, 'max': 1.0},
            'max_disagreement': {'min': 0.1, 'optimal': 0.4, 'max': 0.8},
            'organ_confidence_std': {'min': 0.0, 'optimal': 0.15, 'max': 0.25},
            'inter_family_distance': {'min': 1.0, 'optimal': 2.5, 'max': 5.0}
        }

    def compute_epoch_health(
        self,
        families: Dict,
        organ_confidences: Dict
    ) -> Dict:
        """
        Compute comprehensive signal health for current epoch.

        Args:
            families: Dict of OrganicFamily objects
            organ_confidences: Dict of organ confidence values

        Returns:
            Signal health report dict
        """
        warnings = []
        recommendations = []

        # Extract organ agreement metrics from family centroids
        agreement_metrics = self._extract_agreement_metrics(families)

        # Compute organ confidence differentiation
        organ_conf_values = list(organ_confidences.values())
        organ_conf_std = np.std(organ_conf_values)
        organ_conf_range = max(organ_conf_values) - min(organ_conf_values)

        # Compute inter-family distances
        distance_mean, distance_std = self._compute_inter_family_distances(families)

        # Assess health of each signal
        health_scores = []

        # 1. Pairwise Agreement
        mean_agreement = agreement_metrics.get('mean_pairwise_agreement', 0.8)
        agreement_health = self._assess_signal(mean_agreement, self.thresholds['pairwise_agreement'])
        health_scores.append(agreement_health)
        if mean_agreement < 0.6:
            warnings.append(f"Low pairwise agreement ({mean_agreement:.3f})")
            recommendations.append("Organs not coordinating well - check organ coherence computation")
        elif mean_agreement > 0.95:
            warnings.append(f"Very high agreement ({mean_agreement:.3f}) - potential overconvergence")

        # 2. Multiplicity Index
        mean_multiplicity = agreement_metrics.get('mean_multiplicity_index', 0.15)
        multiplicity_health = self._assess_signal(mean_multiplicity, self.thresholds['multiplicity_index'])
        health_scores.append(multiplicity_health)
        if mean_multiplicity < 0.05:
            warnings.append(f"Low multiplicity ({mean_multiplicity:.3f}) - organs not specializing")
            recommendations.append("Consider more diverse training inputs")
        elif mean_multiplicity > 0.35:
            warnings.append(f"High multiplicity ({mean_multiplicity:.3f}) - excessive organ disagreement")

        # 3. Organ Confidence Differentiation
        conf_health = self._assess_signal(organ_conf_std, self.thresholds['organ_confidence_std'])
        health_scores.append(conf_health)
        if organ_conf_std < 0.05:
            warnings.append(f"Low organ differentiation (std={organ_conf_std:.3f})")
            recommendations.append("Organs not differentiating - check Level 2 updates")

        # 4. Inter-family Distances
        if distance_mean > 0:
            distance_health = self._assess_signal(distance_mean, self.thresholds['inter_family_distance'])
            health_scores.append(distance_health)
            if distance_mean < 1.0:
                warnings.append(f"Small inter-family distances ({distance_mean:.3f})")
                recommendations.append("Families too similar - may need higher distance threshold")

        # Overall health score
        overall_health = np.mean(health_scores) if health_scores else 0.5

        return {
            'mean_pairwise_agreement': mean_agreement,
            'mean_organ_entropy': agreement_metrics.get('mean_organ_entropy', 0.95),
            'mean_multiplicity_index': mean_multiplicity,
            'mean_nexus_coherence': agreement_metrics.get('mean_nexus_coherence', 0.75),
            'mean_max_disagreement': agreement_metrics.get('mean_max_disagreement', 0.4),
            'organ_confidence_std': organ_conf_std,
            'organ_confidence_range': organ_conf_range,
            'inter_family_distance_mean': distance_mean,
            'inter_family_distance_std': distance_std,
            'overall_health_score': overall_health,
            'warnings': warnings,
            'recommendations': recommendations,
            'individual_health_scores': {
                'agreement': agreement_health if 'agreement_health' in dir() else 0,
                'multiplicity': multiplicity_health,
                'organ_differentiation': conf_health,
                'family_separation': distance_health if 'distance_health' in dir() else 0
            }
        }

    def _extract_agreement_metrics(self, families: Dict) -> Dict:
        """Extract organ agreement metrics from family centroids."""
        if not families:
            return {
                'mean_pairwise_agreement': 0.8,
                'mean_organ_entropy': 0.95,
                'mean_multiplicity_index': 0.15,
                'mean_nexus_coherence': 0.75,
                'mean_max_disagreement': 0.4
            }

        pairwise_agreements = []
        organ_entropies = []
        multiplicity_indices = []
        nexus_coherences = []
        max_disagreements = []

        for family in families.values():
            centroid = family.centroid
            if len(centroid) >= 65:
                # FAO dimensions are at indices 57-64
                pairwise_agreements.append(centroid[57])
                organ_entropies.append(centroid[58])
                nexus_coherences.append(centroid[59])
                multiplicity_indices.append(centroid[60])
                max_disagreements.append(centroid[63])

        return {
            'mean_pairwise_agreement': np.mean(pairwise_agreements) if pairwise_agreements else 0.8,
            'mean_organ_entropy': np.mean(organ_entropies) if organ_entropies else 0.95,
            'mean_multiplicity_index': np.mean(multiplicity_indices) if multiplicity_indices else 0.15,
            'mean_nexus_coherence': np.mean(nexus_coherences) if nexus_coherences else 0.75,
            'mean_max_disagreement': np.mean(max_disagreements) if max_disagreements else 0.4
        }

    def _compute_inter_family_distances(self, families: Dict) -> tuple:
        """Compute Euclidean distances between family centroids."""
        if len(families) < 2:
            return 0.0, 0.0

        centroids = [f.centroid for f in families.values()]
        distances = []

        for i in range(len(centroids)):
            for j in range(i + 1, len(centroids)):
                dist = np.linalg.norm(np.array(centroids[i]) - np.array(centroids[j]))
                distances.append(dist)

        return np.mean(distances), np.std(distances)

    def _assess_signal(self, value: float, thresholds: Dict) -> float:
        """
        Assess signal health based on optimal range.

        Returns:
            Health score 0.0-1.0 (1.0 = optimal)
        """
        optimal = thresholds['optimal']
        min_val = thresholds['min']
        max_val = thresholds['max']

        if value < min_val:
            # Below minimum - unhealthy
            return max(0.0, 0.5 * (value / min_val))
        elif value > max_val:
            # Above maximum - potentially unhealthy
            return max(0.0, 1.0 - 0.5 * ((value - max_val) / max_val))
        else:
            # Within range - compute distance from optimal
            if value <= optimal:
                # Between min and optimal
                health = 0.5 + 0.5 * ((value - min_val) / (optimal - min_val))
            else:
                # Between optimal and max
                health = 1.0 - 0.5 * ((value - optimal) / (max_val - optimal))
            return min(1.0, max(0.0, health))

    def generate_health_report(
        self,
        families: Dict,
        organ_confidences: Dict,
        epoch: int
    ) -> str:
        """Generate human-readable health report."""
        health = self.compute_epoch_health(families, organ_confidences)

        report = []
        report.append(f"\n{'=' * 60}")
        report.append(f"📊 SIGNAL HEALTH REPORT - EPOCH {epoch}")
        report.append(f"{'=' * 60}")

        report.append(f"\n🔬 Organ Agreement Metrics:")
        report.append(f"   Pairwise Agreement: {health['mean_pairwise_agreement']:.4f}")
        report.append(f"   Organ Entropy: {health['mean_organ_entropy']:.4f}")
        report.append(f"   Multiplicity Index: {health['mean_multiplicity_index']:.4f}")
        report.append(f"   Nexus Coherence: {health['mean_nexus_coherence']:.4f}")
        report.append(f"   Max Disagreement: {health['mean_max_disagreement']:.4f}")

        report.append(f"\n🧬 Organ Differentiation:")
        report.append(f"   Confidence Std: {health['organ_confidence_std']:.4f}")
        report.append(f"   Confidence Range: {health['organ_confidence_range']:.4f}")

        report.append(f"\n📁 Family Separation:")
        report.append(f"   Mean Distance: {health['inter_family_distance_mean']:.4f}")
        report.append(f"   Distance Std: {health['inter_family_distance_std']:.4f}")

        report.append(f"\n🎯 Overall Health Score: {health['overall_health_score']:.4f}")

        if health['warnings']:
            report.append(f"\n⚠️ Warnings:")
            for warning in health['warnings']:
                report.append(f"   - {warning}")

        if health['recommendations']:
            report.append(f"\n💡 Recommendations:")
            for rec in health['recommendations']:
                report.append(f"   - {rec}")

        return '\n'.join(report)

    def check_degradation(
        self,
        current_health: Dict,
        previous_health: Dict,
        threshold: float = 0.1
    ) -> List[str]:
        """Check for signal degradation between epochs."""
        degradations = []

        # Check key metrics
        metrics_to_check = [
            ('mean_pairwise_agreement', 'Pairwise Agreement'),
            ('organ_confidence_std', 'Organ Differentiation'),
            ('inter_family_distance_mean', 'Family Separation'),
            ('overall_health_score', 'Overall Health')
        ]

        for metric_key, metric_name in metrics_to_check:
            current = current_health.get(metric_key, 0)
            previous = previous_health.get(metric_key, 0)

            if previous > 0:
                change_ratio = (current - previous) / previous
                if change_ratio < -threshold:
                    degradations.append(
                        f"{metric_name} degraded by {abs(change_ratio)*100:.1f}% "
                        f"({previous:.4f} → {current:.4f})"
                    )

        return degradations


# Quick test
if __name__ == "__main__":
    print("Testing Signal Health Monitor...")

    monitor = SignalHealthMonitor()

    # Simulate families with 65D centroids
    class MockFamily:
        def __init__(self, centroid):
            self.centroid = centroid

    # Create mock families
    families = {
        'Family_001': MockFamily(np.random.randn(65)),
        'Family_002': MockFamily(np.random.randn(65)),
        'Family_003': MockFamily(np.random.randn(65))
    }

    # Set FAO dimensions (57-64) to realistic values
    for fam in families.values():
        fam.centroid[57] = 0.85  # Pairwise agreement
        fam.centroid[58] = 0.95  # Organ entropy
        fam.centroid[59] = 0.75  # Nexus coherence
        fam.centroid[60] = 0.15  # Multiplicity index
        fam.centroid[63] = 0.40  # Max disagreement

    # Mock organ confidences
    organ_confidences = {
        'LISTENING': 0.55,
        'EMPATHY': 0.62,
        'WISDOM': 0.48,
        'AUTHENTICITY': 0.58,
        'PRESENCE': 0.52,
        'BOND': 0.68,
        'SANS': 0.45,
        'NDAM': 0.72,
        'RNX': 0.50,
        'EO': 0.65,
        'CARD': 0.55
    }

    # Compute health
    health = monitor.compute_epoch_health(families, organ_confidences)

    print(f"\n✅ Signal Health Computed:")
    print(f"   Overall Score: {health['overall_health_score']:.4f}")
    print(f"   Mean Agreement: {health['mean_pairwise_agreement']:.4f}")
    print(f"   Mean Multiplicity: {health['mean_multiplicity_index']:.4f}")
    print(f"   Organ Confidence Std: {health['organ_confidence_std']:.4f}")

    # Generate full report
    report = monitor.generate_health_report(families, organ_confidences, epoch=1)
    print(report)
