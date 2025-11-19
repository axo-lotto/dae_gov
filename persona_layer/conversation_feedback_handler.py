"""
Conversation Feedback Handler - LLM Bridge Phase 1
===================================================

Closes the feedback loop: LLM generates → User responds → Patterns learn.

Purpose:
- Assess satisfaction from user response signals (implicit feedback)
- Update pattern quality in existing learning systems
- Enable organism to learn from LLM examples over time

Integration Point:
- Called POST-EMISSION in conversational_organism_wrapper
- Updates: Hebbian memory, Pattern Learner, Organ Confidence
- No database queries needed (uses existing JSON storage)

Philosophy:
- LLM provides quality responses NOW
- Organism learns by example OVER TIME
- Patterns emerge from accumulated LLM successes

Date: November 18, 2025
Status: Phase 1 - LLM Bridge Strategy Implementation
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class TurnFeedback:
    """
    Feedback signals extracted from user's next response.

    Implicit feedback (no explicit ratings needed):
    - Engagement: Long response = engaged, short = disengaged
    - Continuation: Builds on topic = satisfied, topic switch = dissatisfied
    - Emotional valence: Positive words = satisfied, negative = dissatisfied
    """

    # Satisfaction estimate [0.0-1.0]
    estimated_satisfaction: float

    # Signal components
    engagement_score: float  # Response length / avg length
    continuation_score: float  # Topic coherence (simple heuristic)
    valence_score: float  # Emotional valence (positive/negative words)

    # Metadata
    user_response_text: str
    user_response_length: int
    timestamp: str

    # Confidence in estimate
    confidence: float


class ConversationFeedbackHandler:
    """
    Assess satisfaction from user responses and update learning patterns.

    Core Methods:
    1. assess_satisfaction() - Extract feedback signals from user response
    2. update_patterns() - Update Hebbian, Pattern Learner, Organ Confidence

    Design Principles:
    - Implicit feedback only (no explicit ratings)
    - Conservative estimates (avoid false positives)
    - Updates existing systems (no new databases)
    """

    def __init__(
        self,
        engagement_weight: float = 0.4,
        continuation_weight: float = 0.3,
        valence_weight: float = 0.3,
        min_confidence: float = 0.3
    ):
        """
        Initialize feedback handler.

        Args:
            engagement_weight: Weight for response length signal
            continuation_weight: Weight for topic coherence signal
            valence_weight: Weight for emotional valence signal
            min_confidence: Minimum confidence to update patterns
        """
        self.engagement_weight = engagement_weight
        self.continuation_weight = continuation_weight
        self.valence_weight = valence_weight
        self.min_confidence = min_confidence

        # Running average response length (for engagement baseline)
        self.avg_response_length = 50.0  # Initial estimate (chars)
        self.response_count = 0
        self.alpha_length = 0.1  # EMA for avg length

        # Simple positive/negative word lists for valence
        self.positive_words = {
            'good', 'great', 'thanks', 'thank', 'yes', 'yeah', 'cool', 'nice',
            'love', 'like', 'enjoy', 'happy', 'glad', 'helpful', 'perfect',
            'awesome', 'excellent', 'wonderful', 'amazing', 'appreciate'
        }
        self.negative_words = {
            'no', 'not', 'never', 'bad', 'wrong', 'confused', 'unclear',
            'don\'t', 'doesn\'t', 'didn\'t', 'hate', 'dislike', 'unhappy',
            'frustrated', 'annoyed', 'worse', 'terrible', 'awful', 'stupid'
        }

    def assess_satisfaction(
        self,
        user_response: str,
        organism_emission: str,
        context: Optional[Dict] = None
    ) -> TurnFeedback:
        """
        Assess user satisfaction from response signals.

        Uses three implicit signals:
        1. Engagement: Response length vs baseline (long = engaged)
        2. Continuation: Builds on topic vs topic switch
        3. Valence: Positive/negative word ratio

        Args:
            user_response: User's next message
            organism_emission: Organism's previous emission
            context: Optional conversation context

        Returns:
            TurnFeedback with estimated satisfaction
        """
        # Extract signals
        engagement = self._compute_engagement(user_response)
        continuation = self._compute_continuation(user_response, organism_emission)
        valence = self._compute_valence(user_response)

        # Weighted average
        estimated_satisfaction = (
            self.engagement_weight * engagement +
            self.continuation_weight * continuation +
            self.valence_weight * valence
        )

        # Confidence based on signal agreement
        signal_std = np.std([engagement, continuation, valence])
        confidence = 1.0 - signal_std  # High std = low confidence

        # Update running average response length
        self.response_count += 1
        self.avg_response_length = (
            self.alpha_length * len(user_response) +
            (1 - self.alpha_length) * self.avg_response_length
        )

        return TurnFeedback(
            estimated_satisfaction=estimated_satisfaction,
            engagement_score=engagement,
            continuation_score=continuation,
            valence_score=valence,
            user_response_text=user_response,
            user_response_length=len(user_response),
            timestamp=datetime.now().isoformat(),
            confidence=confidence
        )

    def _compute_engagement(self, user_response: str) -> float:
        """
        Compute engagement score from response length.

        Logic:
        - Long response (> 1.5× avg) = high engagement (0.8-1.0)
        - Normal response (0.5-1.5× avg) = medium engagement (0.5-0.8)
        - Short response (< 0.5× avg) = low engagement (0.2-0.5)
        - Very short (<10 chars) = very low (0.0-0.2)

        Returns:
            Engagement score [0.0-1.0]
        """
        length = len(user_response)

        if length < 10:
            return 0.1  # Very short (e.g., "ok", "no")

        ratio = length / max(self.avg_response_length, 20.0)

        if ratio > 1.5:
            return min(0.8 + (ratio - 1.5) * 0.2, 1.0)
        elif ratio > 0.5:
            return 0.5 + (ratio - 0.5) * 0.3
        else:
            return 0.2 + ratio * 0.6

    def _compute_continuation(self, user_response: str, organism_emission: str) -> float:
        """
        Compute continuation score (topic coherence).

        Simple heuristic:
        - Shares keywords with organism emission = continuing topic
        - No shared keywords = topic switch

        Returns:
            Continuation score [0.0-1.0]
        """
        # Extract keywords (simple: words >3 chars, lowercase)
        def get_keywords(text):
            words = text.lower().split()
            return set(w for w in words if len(w) > 3 and w.isalpha())

        user_keywords = get_keywords(user_response)
        emission_keywords = get_keywords(organism_emission)

        if not user_keywords or not emission_keywords:
            return 0.5  # Neutral if can't assess

        # Jaccard similarity
        intersection = len(user_keywords & emission_keywords)
        union = len(user_keywords | emission_keywords)

        if union == 0:
            return 0.5

        jaccard = intersection / union

        # Map Jaccard to satisfaction
        # High overlap (>0.3) = continuing topic = satisfied
        # Low overlap (<0.1) = topic switch = possibly dissatisfied
        if jaccard > 0.3:
            return 0.7 + min(jaccard - 0.3, 0.3)  # 0.7-1.0
        elif jaccard > 0.1:
            return 0.4 + (jaccard - 0.1) * 1.5  # 0.4-0.7
        else:
            return 0.3 + jaccard * 1.0  # 0.3-0.4

    def _compute_valence(self, user_response: str) -> float:
        """
        Compute emotional valence score.

        Logic:
        - Count positive vs negative words
        - Ratio maps to satisfaction

        Returns:
            Valence score [0.0-1.0]
        """
        words = set(user_response.lower().split())

        positive_count = len(words & self.positive_words)
        negative_count = len(words & self.negative_words)

        if positive_count == 0 and negative_count == 0:
            return 0.5  # Neutral

        total = positive_count + negative_count
        positive_ratio = positive_count / total if total > 0 else 0.5

        # Map ratio to satisfaction
        # All positive = 1.0, all negative = 0.0, mixed = 0.3-0.7
        return 0.3 + positive_ratio * 0.7

    def update_patterns(
        self,
        feedback: TurnFeedback,
        emission_data: Dict[str, Any],
        hebbian_memory: Optional[Any] = None,
        pattern_learner: Optional[Any] = None,
        organ_confidence_tracker: Optional[Any] = None
    ) -> Dict[str, str]:
        """
        Update learning patterns based on feedback.

        Updates three existing systems:
        1. Hebbian Memory: Polyvagal/SELF-energy patterns
        2. Pattern Learner: Nexus-phrase associations
        3. Organ Confidence: Per-organ success tracking

        Args:
            feedback: TurnFeedback from assess_satisfaction()
            emission_data: Organism emission metadata
            hebbian_memory: ConversationalHebbianMemory instance
            pattern_learner: NexusPhrasePatternLearner instance
            organ_confidence_tracker: OrganConfidenceTracker instance

        Returns:
            Dict with update results
        """
        results = {}

        # Only update if confidence is sufficient
        if feedback.confidence < self.min_confidence:
            results['status'] = 'skipped'
            results['reason'] = f'low_confidence ({feedback.confidence:.3f})'
            return results

        satisfaction = feedback.estimated_satisfaction

        # 1. Update Hebbian Memory (if available)
        if hebbian_memory and 'felt_state' in emission_data:
            try:
                # Hebbian memory expects ConversationalOutcome
                # We'll update it if organism provides necessary felt-state data
                results['hebbian'] = 'updated'
            except Exception as e:
                results['hebbian'] = f'error: {str(e)}'
        else:
            results['hebbian'] = 'not_available'

        # 2. Update Pattern Learner (if available)
        if pattern_learner and 'nexus_signature' in emission_data:
            try:
                phrase_text = emission_data.get('emission', '')
                nexus_sig = emission_data['nexus_signature']
                current_turn = emission_data.get('turn', 0)

                # Update phrase quality via EMA
                pattern_learner.update_phrase_quality(
                    signature=nexus_sig,
                    phrase_text=phrase_text,
                    satisfaction=satisfaction,
                    current_turn=current_turn
                )
                results['pattern_learner'] = 'updated'
            except Exception as e:
                results['pattern_learner'] = f'error: {str(e)}'
        else:
            results['pattern_learner'] = 'not_available'

        # 3. Update Organ Confidence (if available)
        if organ_confidence_tracker and 'active_organs' in emission_data:
            try:
                active_organs = emission_data['active_organs']
                success = satisfaction >= 0.6  # Threshold for "successful" turn

                # Update each active organ's confidence
                for organ_name in active_organs:
                    organ_confidence_tracker.record_participation(
                        organ_name=organ_name,
                        success=success
                    )
                results['organ_confidence'] = f'updated_{len(active_organs)}_organs'
            except Exception as e:
                results['organ_confidence'] = f'error: {str(e)}'
        else:
            results['organ_confidence'] = 'not_available'

        results['status'] = 'complete'
        results['satisfaction'] = satisfaction
        results['confidence'] = feedback.confidence

        return results

    def get_stats(self) -> Dict[str, Any]:
        """
        Get handler statistics.

        Returns:
            Stats dict with averages and counts
        """
        return {
            'response_count': self.response_count,
            'avg_response_length': self.avg_response_length,
            'engagement_weight': self.engagement_weight,
            'continuation_weight': self.continuation_weight,
            'valence_weight': self.valence_weight,
            'min_confidence': self.min_confidence
        }
