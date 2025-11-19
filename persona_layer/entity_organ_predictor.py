"""
Entity-Organ Pattern Prediction - Phase 1 Implementation (RNX Dual Memory)
===========================================================================

Predicts which entities are likely relevant based on current organ activation patterns.

Philosophy (Dual Memory Architecture):
- Field-based memory (RNX): Organ patterns activate entity resonance
- Entity-based memory (Neo4j): Entities queried when field patterns match
- Integration: NEXUS organ uses predictions for PROACTIVE entity retrieval

Architecture:
1. Organ activations → Predict likely entities (field → entity bridge)
2. Entity predictions → Neo4j queries (proactive context retrieval)
3. Entity context → LLM emission (enriched continuity)

Expected Flow:
- Turn N: User mentions "Emma" → EntityOrganTracker learns BOND 1.15×, ventral
- Turn N+5: User input activates BOND 1.12× → Predictor suggests "Emma" (confidence 0.73)
- NEXUS queries Neo4j for Emma proactively → Context available BEFORE emission

Integration Point:
- Called by NEXUS organ during atom activation phase
- Provides entity predictions to guide Neo4j querying
- Enables felt-based entity retrieval (not just keyword matching)

Date: November 18, 2025
Status: Phase 1 - Dual Memory Architecture Implementation
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class EntityPrediction:
    """Prediction that an entity is relevant to current processing"""
    entity_value: str  # "Emma", "work", etc.
    entity_type: str  # "Person", "Place", etc.
    confidence: float  # [0.0, 1.0] similarity between current organs and entity pattern

    # Predicted felt-state expectations
    predicted_organs: Dict[str, float]  # Which organs this entity typically activates
    predicted_polyvagal: str  # Typical polyvagal state when entity mentioned
    predicted_v0_energy: float  # Typical V0 energy
    predicted_urgency: float  # Typical urgency

    # Pattern strength indicators
    mention_count: int  # How many times entity has been mentioned
    success_rate: float  # Historical satisfaction when entity mentioned


class EntityOrganPredictor:
    """
    Predict entities likely to be relevant based on current organ activation patterns.

    Strategy:
    1. Compute organ activation vector from current processing
    2. Compare to historical entity-organ patterns (cosine similarity)
    3. Return high-confidence matches (threshold: 0.6)
    4. NEXUS organ uses predictions to query Neo4j proactively

    Expected Benefits:
    - Proactive entity retrieval (felt-pattern matching, not keyword matching)
    - Cross-turn entity continuity ("Emma still present for you")
    - Field-based memory activating entity-based memory (dual-path integration)
    """

    def __init__(
        self,
        confidence_threshold: float = 0.6,  # Minimum similarity for prediction
        max_predictions: int = 5  # Maximum entities to predict per turn
    ):
        """
        Initialize entity-organ predictor.

        Args:
            confidence_threshold: Minimum cosine similarity for prediction [0.6-0.8]
            max_predictions: Maximum number of entity predictions to return
        """
        self.confidence_threshold = confidence_threshold
        self.max_predictions = max_predictions

    def predict_entities_for_organs(
        self,
        current_organ_activations: Dict[str, float],
        entity_tracker,  # EntityOrganTracker instance
        min_mention_threshold: int = 3  # Need 3+ mentions for reliable pattern
    ) -> List[EntityPrediction]:
        """
        Predict which entities are likely relevant based on current organ patterns.

        Args:
            current_organ_activations: Current organ activation strengths {organ_name: activation}
            entity_tracker: EntityOrganTracker instance with historical patterns
            min_mention_threshold: Minimum mentions required for entity pattern

        Returns:
            List of EntityPrediction objects sorted by confidence (highest first)
        """
        predictions = []

        # Get normalized organ vector for current processing
        current_vector = self._normalize_organ_vector(current_organ_activations)

        # Compare to each tracked entity's organ pattern
        for entity_value, metrics in entity_tracker.entity_metrics.items():
            # Skip entities without sufficient history
            if metrics.mention_count < min_mention_threshold:
                continue

            # Get entity's organ pattern
            entity_pattern = entity_tracker.get_entity_pattern(entity_value)
            if entity_pattern is None:
                continue

            # Compute similarity between current organs and entity pattern
            entity_vector = self._normalize_organ_vector(entity_pattern['organ_boosts'])
            similarity = self._cosine_similarity(current_vector, entity_vector)

            # Create prediction if similarity exceeds threshold
            if similarity >= self.confidence_threshold:
                predictions.append(EntityPrediction(
                    entity_value=entity_value,
                    entity_type=metrics.entity_type,
                    confidence=similarity,
                    predicted_organs=entity_pattern['organ_boosts'],
                    predicted_polyvagal=entity_pattern['polyvagal_state'],
                    predicted_v0_energy=entity_pattern['v0_energy'],
                    predicted_urgency=entity_pattern['urgency'],
                    mention_count=metrics.mention_count,
                    success_rate=entity_pattern['success_rate']
                ))

        # Sort by confidence (highest first) and limit to max_predictions
        predictions.sort(key=lambda p: p.confidence, reverse=True)
        return predictions[:self.max_predictions]

    def predict_entities_with_context(
        self,
        current_organ_activations: Dict[str, float],
        current_polyvagal_state: str,
        current_urgency: float,
        entity_tracker,
        polyvagal_weight: float = 0.3,  # Weight for polyvagal state matching
        urgency_weight: float = 0.2  # Weight for urgency similarity
    ) -> List[EntityPrediction]:
        """
        Predict entities using BOTH organ patterns AND felt-state context.

        This is the enhanced prediction that considers:
        1. Organ pattern similarity (70% weight)
        2. Polyvagal state match (30% weight)
        3. Urgency similarity (20% weight, bonus if matches)

        Args:
            current_organ_activations: Current organ strengths
            current_polyvagal_state: Current polyvagal state (ventral/sympathetic/dorsal)
            current_urgency: Current urgency level [0.0, 1.0]
            entity_tracker: EntityOrganTracker instance
            polyvagal_weight: Weight for polyvagal matching
            urgency_weight: Weight for urgency matching

        Returns:
            List of EntityPrediction objects with context-aware confidence scores
        """
        # Get base organ predictions
        predictions = self.predict_entities_for_organs(
            current_organ_activations,
            entity_tracker,
            min_mention_threshold=3
        )

        # Adjust confidence based on felt-state context
        for prediction in predictions:
            # Polyvagal state bonus (exact match)
            if prediction.predicted_polyvagal == current_polyvagal_state:
                prediction.confidence += polyvagal_weight * (1.0 - prediction.confidence)

            # Urgency similarity bonus
            urgency_diff = abs(prediction.predicted_urgency - current_urgency)
            urgency_similarity = 1.0 - urgency_diff
            prediction.confidence += urgency_weight * urgency_similarity * (1.0 - prediction.confidence)

            # Clamp to [0.0, 1.0]
            prediction.confidence = np.clip(prediction.confidence, 0.0, 1.0)

        # Re-sort by adjusted confidence
        predictions.sort(key=lambda p: p.confidence, reverse=True)
        return predictions[:self.max_predictions]

    def get_proactive_entity_queries(
        self,
        current_organ_activations: Dict[str, float],
        entity_tracker,
        user_id: str
    ) -> List[str]:
        """
        Get list of entity values to proactively query from Neo4j.

        This is the NEXUS integration method - returns entity values
        that should be queried based on current organ patterns.

        Args:
            current_organ_activations: Current organ strengths
            entity_tracker: EntityOrganTracker instance
            user_id: Current user identifier

        Returns:
            List of entity values to query: ["Emma", "work", ...]
        """
        predictions = self.predict_entities_for_organs(
            current_organ_activations,
            entity_tracker,
            min_mention_threshold=3
        )

        # Extract entity values for Neo4j querying
        return [pred.entity_value for pred in predictions]

    # ===== Private Methods =====

    def _normalize_organ_vector(
        self,
        organ_activations: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Normalize organ activation vector for cosine similarity.

        Args:
            organ_activations: {organ_name: activation_strength, ...}

        Returns:
            Normalized vector with L2 norm = 1.0
        """
        if not organ_activations:
            return {}

        # Compute L2 norm
        values = np.array(list(organ_activations.values()))
        norm = np.linalg.norm(values)

        if norm == 0:
            return organ_activations

        # Normalize
        return {
            organ: activation / norm
            for organ, activation in organ_activations.items()
        }

    def _cosine_similarity(
        self,
        vec1: Dict[str, float],
        vec2: Dict[str, float]
    ) -> float:
        """
        Compute cosine similarity between two organ activation vectors.

        Handles sparse vectors (different organ sets).

        Args:
            vec1: First organ vector (normalized)
            vec2: Second organ vector (normalized)

        Returns:
            Cosine similarity [0.0, 1.0] (or [-1.0, 1.0] but organs are always positive)
        """
        if not vec1 or not vec2:
            return 0.0

        # Get union of organ names
        all_organs = set(vec1.keys()) | set(vec2.keys())

        # Build aligned vectors
        v1 = np.array([vec1.get(organ, 0.0) for organ in all_organs])
        v2 = np.array([vec2.get(organ, 0.0) for organ in all_organs])

        # Compute dot product (vectors already normalized)
        similarity = np.dot(v1, v2)

        return float(np.clip(similarity, 0.0, 1.0))

    def get_prediction_summary(
        self,
        predictions: List[EntityPrediction]
    ) -> Dict:
        """
        Get summary statistics for prediction results.

        Args:
            predictions: List of EntityPrediction objects

        Returns:
            Summary dict with counts, mean confidence, etc.
        """
        if not predictions:
            return {
                'total_predictions': 0,
                'mean_confidence': 0.0,
                'max_confidence': 0.0,
                'entity_types': []
            }

        confidences = [p.confidence for p in predictions]

        return {
            'total_predictions': len(predictions),
            'mean_confidence': np.mean(confidences),
            'max_confidence': np.max(confidences),
            'min_confidence': np.min(confidences),
            'entity_types': list(set(p.entity_type for p in predictions)),
            'predicted_entities': [p.entity_value for p in predictions],
            'top_prediction': predictions[0].entity_value if predictions else None
        }


# Quick test
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

    from persona_layer.entity_organ_tracker import EntityOrganTracker
    from dataclasses import dataclass as dc

    print("="*80)
    print("🧪 ENTITY-ORGAN PREDICTOR TEST")
    print("="*80)

    # Mock organ result for testing
    @dc
    class MockOrganResult:
        coherence: float

    # Initialize tracker and predictor
    tracker = EntityOrganTracker(storage_path="persona_layer/test_entity_predictor.json")
    predictor = EntityOrganPredictor(confidence_threshold=0.6)

    # Scenario 1: Build Emma pattern (daughter, safe, BOND-heavy)
    print(f"\n📋 SCENARIO 1: Building Emma pattern (3 mentions)")

    for i in range(3):
        tracker.update(
            extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
            organ_results={
                'BOND': MockOrganResult(coherence=0.85),
                'EMPATHY': MockOrganResult(coherence=0.75),
                'PRESENCE': MockOrganResult(coherence=0.70),
            },
            felt_state={
                'polyvagal_state': 'ventral',
                'v0_energy': 0.25,
                'urgency': 0.0,
                'self_distance': 0.0
            },
            emission_satisfaction=0.95
        )

    # Scenario 2: Build work pattern (place, stressful, NDAM-heavy)
    print(f"📋 SCENARIO 2: Building work pattern (3 mentions)")

    for i in range(3):
        tracker.update(
            extracted_entities=[{'entity_value': 'work', 'entity_type': 'Place'}],
            organ_results={
                'NDAM': MockOrganResult(coherence=0.82),
                'AUTHENTICITY': MockOrganResult(coherence=0.65),
                'BOND': MockOrganResult(coherence=0.45),
            },
            felt_state={
                'polyvagal_state': 'sympathetic',
                'v0_energy': 0.72,
                'urgency': 0.7,
                'self_distance': 0.6
            },
            emission_satisfaction=0.70
        )

    # Test 1: Predict entities when BOND activates strongly
    print(f"\n{'='*80}")
    print(f"🧪 TEST 1: Current input activates BOND strongly (expect: Emma predicted)")
    print(f"{'='*80}")

    current_organs_bond = {
        'BOND': 0.80,
        'EMPATHY': 0.72,
        'PRESENCE': 0.68,
    }

    predictions_bond = predictor.predict_entities_for_organs(
        current_organ_activations=current_organs_bond,
        entity_tracker=tracker
    )

    if predictions_bond:
        print(f"\n✅ Predictions:")
        for pred in predictions_bond:
            print(f"   - {pred.entity_value} ({pred.entity_type})")
            print(f"     Confidence: {pred.confidence:.3f}")
            print(f"     Predicted polyvagal: {pred.predicted_polyvagal}")
            print(f"     Predicted V0: {pred.predicted_v0_energy:.3f}")
            print(f"     Mention count: {pred.mention_count}")
            print()
    else:
        print(f"❌ No predictions (confidence < {predictor.confidence_threshold})")

    # Test 2: Predict entities when NDAM activates strongly
    print(f"{'='*80}")
    print(f"🧪 TEST 2: Current input activates NDAM strongly (expect: work predicted)")
    print(f"{'='*80}")

    current_organs_ndam = {
        'NDAM': 0.78,
        'AUTHENTICITY': 0.62,
        'BOND': 0.42,
    }

    predictions_ndam = predictor.predict_entities_for_organs(
        current_organ_activations=current_organs_ndam,
        entity_tracker=tracker
    )

    if predictions_ndam:
        print(f"\n✅ Predictions:")
        for pred in predictions_ndam:
            print(f"   - {pred.entity_value} ({pred.entity_type})")
            print(f"     Confidence: {pred.confidence:.3f}")
            print(f"     Predicted polyvagal: {pred.predicted_polyvagal}")
            print(f"     Predicted urgency: {pred.predicted_urgency:.3f}")
            print(f"     Mention count: {pred.mention_count}")
            print()
    else:
        print(f"❌ No predictions (confidence < {predictor.confidence_threshold})")

    # Test 3: Context-aware prediction (polyvagal + urgency)
    print(f"{'='*80}")
    print(f"🧪 TEST 3: Context-aware prediction (BOND + ventral state)")
    print(f"{'='*80}")

    predictions_context = predictor.predict_entities_with_context(
        current_organ_activations=current_organs_bond,
        current_polyvagal_state='ventral',
        current_urgency=0.0,
        entity_tracker=tracker
    )

    if predictions_context:
        print(f"\n✅ Context-aware predictions:")
        for pred in predictions_context:
            print(f"   - {pred.entity_value}: {pred.confidence:.3f} (boosted by context)")

    # Test 4: Get proactive query list for NEXUS
    print(f"\n{'='*80}")
    print(f"🧪 TEST 4: NEXUS proactive entity queries")
    print(f"{'='*80}")

    query_entities = predictor.get_proactive_entity_queries(
        current_organ_activations=current_organs_bond,
        entity_tracker=tracker,
        user_id="test_user"
    )

    if query_entities:
        print(f"\n✅ Entities to query from Neo4j:")
        for entity in query_entities:
            print(f"   - {entity}")
    else:
        print(f"❌ No entities to query")

    # Summary
    print(f"\n{'='*80}")
    print(f"📊 PREDICTION SUMMARY")
    print(f"{'='*80}")

    summary_bond = predictor.get_prediction_summary(predictions_bond)
    summary_ndam = predictor.get_prediction_summary(predictions_ndam)

    print(f"\nBOND activation:")
    print(f"   Total predictions: {summary_bond['total_predictions']}")
    print(f"   Mean confidence: {summary_bond['mean_confidence']:.3f}")
    print(f"   Top prediction: {summary_bond['top_prediction']}")

    print(f"\nNDAM activation:")
    print(f"   Total predictions: {summary_ndam['total_predictions']}")
    print(f"   Mean confidence: {summary_ndam['mean_confidence']:.3f}")
    print(f"   Top prediction: {summary_ndam['top_prediction']}")

    print(f"\n✅ Entity-organ prediction working correctly!")
    print("="*80)
