"""
Multi-Organ Entity Extractor - Phase 0C
========================================

Intersection-based entity extraction using multi-organ signals.

Architecture (FFITTSS-validated):
1. Collect entity signals from all 12 organs (T3 Organ Processing)
2. Intersection: Find entities detected by 3+ organs (T4 AffinityNexus formation)
3. Coherence scoring: C̄ = 1 - variance(confidences) (T4 Field intersection)
4. Satisfaction gate: Accept if C̄ > 0.75 (T5 Commit with ΔC gating)

Philosophy: Entity detection is not single-organ (SANS-only) but multi-organ
(affinity specialization through intersection). Coherence gating ensures quality.

Date: November 19, 2025
Author: DAE_HYPHAE_1 Strategic Integration
"""

from typing import List, Dict, Any
import numpy as np


class MultiOrganEntityExtractor:
    """
    Extract entities via multi-organ intersection (Phase 0C).

    Implements FFITTSS T4 AffinityNexus pattern: field intersection → coherence → gate.
    """

    def __init__(
        self,
        coherence_threshold: float = 0.75,  # DAE 3.0 proven threshold
        min_organs: int = 3,                # 3+ organs must agree
        ema_alpha: float = 0.15             # Confidence EMA (match Phase 0A/0B)
    ):
        """
        Initialize multi-organ entity extractor.

        Args:
            coherence_threshold: Minimum coherence for entity acceptance (C̄ > threshold)
            min_organs: Minimum organs that must detect entity (intersection requirement)
            ema_alpha: EMA alpha for confidence smoothing
        """
        self.coherence_threshold = coherence_threshold
        self.min_organs = min_organs
        self.ema_alpha = ema_alpha

        # Tracking
        self.extraction_history = []
        self.coherence_scores = []

    def extract_entities_multi_organ(
        self,
        organ_results: Dict[str, Any],
        nexus_organ=None  # NEXUSTextCore instance for signal extraction
    ) -> List[Dict[str, Any]]:
        """
        Extract entities from organ signals using intersection + coherence.

        Flow (FFITTSS T4):
        1. Collect entity signals from all 12 organs
        2. Intersection: Find entities detected by min_organs+ organs
        3. Coherence scoring: C̄ = 1 - variance(organ confidences)
        4. Satisfaction gate: Filter by C̄ > threshold

        Args:
            organ_results: Dict of organ_name → organ_result (with entity_signals)
            nexus_organ: NEXUSTextCore instance for memory-based signal extraction

        Returns:
            List of entity dicts with format:
            {
                'entity_value': str,
                'entity_type': str,
                'confidence': float,
                'coherence': float,
                'organ_agreement': List[str],  # Which organs detected it
                'organ_signals': Dict[str, Dict]  # Signals from each organ
            }
        """
        # Step 1: Collect entity signals from all organs
        entity_candidates = {}  # {entity_value: {organs: [...], signals: [...], types: [...]}}

        for organ_name, organ_result in organ_results.items():
            if not isinstance(organ_result, dict):
                continue

            # Extract entity_signals from this organ
            # Organs can provide entity signals in their results
            entity_signals = organ_result.get('entity_signals', [])

            if not entity_signals:
                continue

            # Process each entity signal from this organ
            for signal in entity_signals:
                entity_value = signal.get('entity_value')
                entity_type = signal.get('entity_type', 'Unknown')
                confidence = signal.get('confidence', 0.0)

                if not entity_value or confidence < 0.1:
                    continue

                # Initialize candidate if new
                if entity_value not in entity_candidates:
                    entity_candidates[entity_value] = {
                        'organs': [],
                        'confidences': [],
                        'signals': {},
                        'types': []
                    }

                # Add organ detection
                entity_candidates[entity_value]['organs'].append(organ_name)
                entity_candidates[entity_value]['confidences'].append(confidence)
                entity_candidates[entity_value]['signals'][organ_name] = signal
                entity_candidates[entity_value]['types'].append(entity_type)

        # Step 2: Add NEXUS memory-based signals if available
        if nexus_organ:
            for entity_value in list(entity_candidates.keys()):
                try:
                    nexus_signals = nexus_organ.extract_entity_signals(entity_value)

                    # Use memory_strength as NEXUS confidence
                    memory_strength = nexus_signals.get('memory_strength', 0.0)

                    if memory_strength > 0.1:
                        # Add NEXUS as detecting organ
                        entity_candidates[entity_value]['organs'].append('NEXUS')
                        entity_candidates[entity_value]['confidences'].append(memory_strength)
                        entity_candidates[entity_value]['signals']['NEXUS'] = {
                            'entity_value': entity_value,
                            'confidence': memory_strength,
                            'nexus_signals': nexus_signals
                        }
                except Exception as e:
                    # Non-critical, continue without NEXUS signals
                    pass

        # Step 3: Filter by min_organs agreement
        filtered_candidates = {
            entity_value: data
            for entity_value, data in entity_candidates.items()
            if len(data['organs']) >= self.min_organs
        }

        # Step 4: Compute coherence for each candidate
        extracted_entities = []

        for entity_value, data in filtered_candidates.items():
            confidences = data['confidences']

            # Compute coherence: C̄ = 1 - var(confidences)
            coherence = self._compute_coherence(confidences)

            # Track for statistics
            self.coherence_scores.append(coherence)

            # Step 5: Gate by coherence_threshold
            if coherence >= self.coherence_threshold:
                # Determine entity type (majority vote)
                type_counts = {}
                for entity_type in data['types']:
                    type_counts[entity_type] = type_counts.get(entity_type, 0) + 1

                final_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else 'Unknown'

                # Compute mean confidence with EMA
                mean_confidence = np.mean(confidences)

                # Build entity dict
                entity_dict = {
                    'entity_value': entity_value,
                    'entity_type': final_type,
                    'confidence': float(mean_confidence),
                    'coherence': float(coherence),
                    'organ_agreement': data['organs'],
                    'organ_signals': data['signals'],
                    'num_organs': len(data['organs'])
                }

                extracted_entities.append(entity_dict)

                # Track extraction history
                self.extraction_history.append({
                    'entity_value': entity_value,
                    'coherence': coherence,
                    'num_organs': len(data['organs']),
                    'accepted': True
                })

        # Sort by coherence (highest first)
        extracted_entities.sort(key=lambda x: x['coherence'], reverse=True)

        return extracted_entities

    def _compute_coherence(self, confidences: List[float]) -> float:
        """
        Compute coherence score from organ confidence values.

        Formula (DAE 3.0): C̄ = 1 - variance(confidences)

        Returns:
            Coherence score [0.0, 1.0], where 1.0 = perfect agreement
        """
        if len(confidences) < 2:
            return 1.0  # Single organ = perfect coherence by definition

        return 1.0 - np.var(confidences)

    def get_statistics(self) -> Dict[str, Any]:
        """Get extraction statistics for monitoring."""
        if not self.coherence_scores:
            return {
                'total_extractions': 0,
                'mean_coherence': 0.0,
                'gated_rate': 0.0
            }

        gated_count = sum(1 for c in self.coherence_scores if c >= self.coherence_threshold)

        return {
            'total_extractions': len(self.coherence_scores),
            'mean_coherence': np.mean(self.coherence_scores),
            'gated_rate': gated_count / len(self.coherence_scores),
            'min_coherence': np.min(self.coherence_scores),
            'max_coherence': np.max(self.coherence_scores)
        }


# Factory function for easy initialization
def create_multi_organ_extractor(
    coherence_threshold: float = 0.75,
    min_organs: int = 3
) -> MultiOrganEntityExtractor:
    """
    Create multi-organ entity extractor with default settings.

    Args:
        coherence_threshold: Minimum C̄ for acceptance (default: 0.75, DAE 3.0 proven)
        min_organs: Minimum organ agreement (default: 3, balance precision/recall)

    Returns:
        MultiOrganEntityExtractor instance
    """
    return MultiOrganEntityExtractor(
        coherence_threshold=coherence_threshold,
        min_organs=min_organs
    )
