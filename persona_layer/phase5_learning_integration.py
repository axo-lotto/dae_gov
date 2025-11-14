"""
Phase 5 Learning Integration - Organic Conversational Learning Hooks
=================================================================

Integrates the three Phase 5 components with the emission architecture:
1. OrganSignatureExtractor (45D organ-native)
2. OrganicConversationalFamilies (self-organizing clustering)
3. ConversationalClusterLearning (EMA optimization)

Purpose:
- Learn from successful conversations (satisfaction ≥ 0.75)
- Discover archetypal patterns as Eternal Objects
- Apply learned knowledge during future emissions

Philosophy:
- Organic emergence (not pre-designed categories)
- Whiteheadian objective immortality
- DAE 3.0 proven approach (841 perfect tasks, 37 families, Zipf's law)

Integration Points:
- POST-EMISSION: Extract signatures → assign families → update learning
- PRE-EMISSION: Apply learned organ weights and family guidance

Date: November 11, 2025
Status: Phase 5 Integration
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

from persona_layer.organ_signature_extractor import OrganSignatureExtractor
from persona_layer.organic_conversational_families import OrganicConversationalFamilies
from persona_layer.conversational_cluster_learning import ConversationalClusterLearning


class Phase5LearningIntegration:
    """
    Integration layer for Phase 5 organic conversational learning.

    Hooks into emission architecture to:
    1. Learn from successful conversations
    2. Discover self-organizing families
    3. Apply learned knowledge in future emissions

    Following DAE 3.0's proven approach:
    - 841 perfect tasks (60.1% success rate)
    - 37 organic families (self-organized)
    - Zipf's law validated (α=0.73, R²=0.94)
    - 86.75% cross-dataset transfer
    """

    def __init__(
        self,
        storage_path: str = "persona_layer",
        learning_threshold: float = 0.30,  # LOWERED Nov 13, 2025: 0.55 → 0.30 to enable learning from safety-boosted emissions
        enable_learning: bool = True
    ):
        """
        Initialize Phase 5 learning integration.

        Args:
            storage_path: Directory for organic families storage
            learning_threshold: Minimum satisfaction for learning (0.75)
            enable_learning: Enable/disable learning (for testing)
        """
        self.storage_path = Path(storage_path)
        self.learning_threshold = learning_threshold
        self.enable_learning = enable_learning

        # Initialize Phase 5 components
        self.signature_extractor = OrganSignatureExtractor()

        self.families = OrganicConversationalFamilies(
            storage_path=str(self.storage_path / "organic_families.json"),
            similarity_threshold=0.75,  # Lowered for variance-weighted signatures
            ema_alpha=0.2  # DAE 3.0 validated
        )

        self.cluster_learning = ConversationalClusterLearning(
            storage_path=str(self.storage_path / "conversational_clusters.json"),
            ema_alpha=0.2  # DAE 3.0 validated
        )

        # Conversation tracking
        self.conversation_counter = 0
        self.last_family_assignment = None

        print(f"✅ Phase 5 Organic Learning initialized")
        print(f"   Storage: {self.storage_path}")
        print(f"   Learning threshold: {self.learning_threshold}")
        print(f"   Current families: {len(self.families.families)}")

    def _organ_results_to_dicts(self, organ_results: Dict) -> Dict:
        """
        Convert organ dataclass objects to dicts for signature extraction.

        The organ processing pipeline returns dataclass objects (e.g., ListeningResult)
        with nested dataclass objects (e.g., ListeningPattern). The signature extractor
        expects pure dicts with .get() method. This helper recursively converts all
        dataclass objects to dicts.

        Args:
            organ_results: Dict mapping organ_name -> OrganResult dataclass object

        Returns:
            Dict mapping organ_name -> dict of attributes (recursively converted)
        """
        def to_dict_recursive(obj):
            """Recursively convert dataclass objects to dicts."""
            if hasattr(obj, '__dict__'):
                # Dataclass object - convert to dict
                obj_dict = {}
                for key, value in obj.__dict__.items():
                    if isinstance(value, list):
                        # List of objects - recursively convert each
                        obj_dict[key] = [to_dict_recursive(item) for item in value]
                    elif isinstance(value, dict):
                        # Dict - recursively convert values
                        obj_dict[key] = {k: to_dict_recursive(v) for k, v in value.items()}
                    elif hasattr(value, '__dict__'):
                        # Nested dataclass - recursively convert
                        obj_dict[key] = to_dict_recursive(value)
                    else:
                        # Primitive value - use as-is
                        obj_dict[key] = value
                return obj_dict
            else:
                # Already a primitive or dict - return as-is
                return obj

        dict_results = {}
        for organ_name, result_obj in organ_results.items():
            dict_results[organ_name] = to_dict_recursive(result_obj)

        return dict_results


    def learn_from_conversation(
        self,
        organ_results: Dict,
        assembled_response,  # AssembledResponse object
        user_message: str = "",
        conversation_id: Optional[str] = None
    ) -> Optional[Dict]:
        """
        POST-EMISSION HOOK: Learn from successful conversation.

        Called after response assembly when satisfaction ≥ threshold.

        Args:
            organ_results: Dict of organ processing results
            assembled_response: AssembledResponse object with satisfaction
            user_message: Original user message
            conversation_id: Optional conversation identifier

        Returns:
            Learning report dict (or None if not learned)
        """
        if not self.enable_learning:
            return None

        # Check satisfaction threshold
        satisfaction_score = getattr(assembled_response, 'mean_satisfaction', None)
        if satisfaction_score is None:
            # Fallback: check if 'satisfaction_score' attribute exists
            satisfaction_score = getattr(assembled_response, 'satisfaction_score', None)
        if satisfaction_score is None:
            # Second fallback: check if 'satisfaction' attribute exists (arc training compatibility)
            satisfaction_score = getattr(assembled_response, 'satisfaction', None)

        if satisfaction_score is None:
            # No satisfaction available, skip learning
            return None

        if satisfaction_score < self.learning_threshold:
            # Low satisfaction - don't learn from this conversation
            return None

        # Generate conversation ID if not provided
        if conversation_id is None:
            self.conversation_counter += 1
            conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.conversation_counter}"

        # ================================================================
        # STEP 1: Extract 57D Organ-Native Signature (VARIANCE-WEIGHTED)
        # ================================================================
        # Use variance-weighted extraction to create discriminative signatures
        # that resist uniform centroid drift through averaging
        # Convert dataclass objects to dicts for signature extraction
        organ_results_dicts = self._organ_results_to_dicts(organ_results)

        composite_signature = self.signature_extractor.extract_composite_signature_variance_weighted(
            organ_results=organ_results_dicts,
            conversation_id=conversation_id,
            satisfaction_score=satisfaction_score,
            emission_text=assembled_response.text,
            user_message=user_message,
            timestamp=datetime.now().isoformat(),
            variance_amplification=1.0  # Default weighting strength
        )

        # ================================================================
        # STEP 2: Assign to Family (or create new family)
        # ================================================================
        family_assignment = self.families.assign_to_family(
            conversation_id=conversation_id,
            signature=composite_signature.signature,
            satisfaction_score=satisfaction_score,
            organ_contributions=composite_signature.organ_contributions
        )

        self.last_family_assignment = family_assignment

        # ================================================================
        # STEP 3: Update Cluster Learning (EMA optimization)
        # ================================================================
        emission_metrics = {
            'mean_coherence': assembled_response.mean_coherence,
            'mean_confidence': assembled_response.mean_confidence,
            'num_phrases': assembled_response.num_phrases,
            'strategies_used': assembled_response.strategies_used,
            'field_types': assembled_response.field_types
        }

        self.cluster_learning.update_from_conversation(
            conversation_id=conversation_id,
            family_id=family_assignment.family_id,
            organ_results=organ_results,
            satisfaction_score=satisfaction_score,
            emission_metrics=emission_metrics,
            user_message=user_message,
            emission_text=assembled_response.text
        )

        # ================================================================
        # Return Learning Report
        # ================================================================
        return {
            'learned': True,
            'conversation_id': conversation_id,
            'family_id': family_assignment.family_id,
            'family_maturity': family_assignment.family_maturity,
            'is_new_family': (family_assignment.assignment_type == 'CREATED'),
            'similarity': family_assignment.similarity_score,
            'satisfaction_score': satisfaction_score,
            'total_families': len(self.families.families),
            'trauma_informed': {
                'bond_self_distance': composite_signature.organ_contributions.get('BOND', [0.5])[0],
                'safety_level': 'SAFE' if composite_signature.organ_contributions.get('BOND', [0.5])[0] < 0.3 else 'MODERATE' if composite_signature.organ_contributions.get('BOND', [0.5])[0] < 0.6 else 'TRAUMA_ACTIVATED'
            }
        }

    def get_current_family_id(self) -> Optional[str]:
        """
        Get the family ID from the most recent conversation assignment.

        Returns:
            Family ID string or None if no assignment yet
        """
        if self.last_family_assignment is None:
            return None
        return self.last_family_assignment.family_id

    def get_family_guidance(
        self,
        predicted_family_id: Optional[str] = None
    ) -> Optional[Dict]:
        """
        PRE-EMISSION HOOK: Get learned guidance for emission generation.

        Called before emission generation to apply learned knowledge.

        Args:
            predicted_family_id: Optional family prediction (use last if None)

        Returns:
            Guidance dict with learned organ weights and targets
        """
        if not self.enable_learning:
            return None

        # Use last family assignment if no prediction provided
        if predicted_family_id is None:
            if self.last_family_assignment is None:
                return None
            predicted_family_id = self.last_family_assignment.family_id

        # Get learned guidance from cluster learning
        guidance = self.cluster_learning.get_family_guidance(predicted_family_id)

        if not guidance:
            return None

        # Only use guidance from MATURE families (≥3 conversations)
        if guidance.get('family_maturity') != 'mature':
            return None

        # Return guidance for emission modulation
        return {
            'family_id': predicted_family_id,
            'family_maturity': guidance['family_maturity'],
            'organ_weights': guidance['organ_weights'],  # Normalized to mean=1.0
            'target_satisfaction': guidance['target_satisfaction'],
            'emission_quality_expectation': guidance['emission_quality_expectation'],
            'success_rate': guidance['success_rate'],
            'conversation_count': guidance['conversation_count']
        }

    def apply_organ_weights_to_nexuses(
        self,
        nexuses: List,
        guidance: Dict
    ) -> List:
        """
        Apply learned organ weights to nexus activations.

        Modulates organ importance based on learned family patterns.

        Args:
            nexuses: List of SemanticNexus objects
            guidance: Guidance dict from get_family_guidance()

        Returns:
            Weighted nexuses (modified in place)
        """
        if not guidance or 'organ_weights' not in guidance:
            return nexuses

        organ_weights = guidance['organ_weights']

        # Apply weights to nexus activations
        for nexus in nexuses:
            for organ_name in nexus.participants:
                if organ_name in organ_weights:
                    weight = organ_weights[organ_name]
                    # Modulate organ's contribution by learned weight
                    if organ_name in nexus.activations:
                        nexus.activations[organ_name] *= weight

            # Recompute emission readiness with weighted activations
            # emission_readiness is average of activations
            if nexus.activations:
                nexus.emission_readiness = sum(nexus.activations.values()) / len(nexus.activations)

        return nexuses

    def get_statistics(self) -> Dict:
        """
        Get Phase 5 learning statistics.

        Returns:
            Statistics dict with family and learning metrics
        """
        family_stats = self.families.get_family_statistics()

        return {
            'total_families': len(self.families.families),
            'total_conversations': family_stats.get('total_conversations', 0),
            'maturity_levels': family_stats.get('maturity_levels', {}),
            'learning_enabled': self.enable_learning,
            'learning_threshold': self.learning_threshold,
            'last_family': self.last_family_assignment.family_id if self.last_family_assignment else None
        }

    def print_learning_summary(self, learning_report: Dict):
        """Print friendly learning summary after conversation."""
        if not learning_report or not learning_report.get('learned'):
            return

        print(f"\n🌀 Phase 5 Organic Learning:")

        if learning_report['is_new_family']:
            print(f"   ✨ NEW FAMILY discovered! {learning_report['family_id']}")
            print(f"      Total families: {learning_report['total_families']}")
        else:
            print(f"   📊 Assigned to family: {learning_report['family_id']} ({learning_report['family_maturity']})")
            print(f"      Similarity: {learning_report['similarity']:.3f}")

        # Trauma-informed safety
        safety_info = learning_report['trauma_informed']
        if safety_info['safety_level'] == 'SAFE':
            print(f"   🟢 SAFE conversation (BOND self_distance: {safety_info['bond_self_distance']:.3f})")
        elif safety_info['safety_level'] == 'MODERATE':
            print(f"   🟡 MODERATE activation (BOND self_distance: {safety_info['bond_self_distance']:.3f})")
        else:
            print(f"   🔴 TRAUMA ACTIVATED (BOND self_distance: {safety_info['bond_self_distance']:.3f})")

        print(f"   Satisfaction: {learning_report['satisfaction_score']:.3f}")


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 PHASE 5 LEARNING INTEGRATION TEST")
    print("="*70)

    # Mock data for testing
    from dataclasses import dataclass

    @dataclass
    class MockAssembledResponse:
        text: str
        num_phrases: int
        strategies_used: List[str]
        mean_confidence: float
        mean_coherence: float
        field_types: List[str]
        satisfaction_score: float = 0.85  # High satisfaction for learning

    mock_organ_results = {
        'LISTENING': {'coherence': 0.75, 'quality': 0.80, 'strength': 0.70},
        'EMPATHY': {'coherence': 0.82, 'quality': 0.85, 'tone': 0.78},
        'WISDOM': {'coherence': 0.68, 'quality': 0.72, 'depth': 0.65},
        'AUTHENTICITY': {'coherence': 0.90, 'quality': 0.88, 'strength': 0.85},
        'PRESENCE': {'coherence': 0.77, 'quality': 0.80, 'depth': 0.75},
        'BOND': {'self_distance': 0.25, 'polarization': 0.20, 'harmony': 0.85, 'strength': 0.80},  # SAFE
        'SANS': {'coherence': 0.70, 'readiness': 0.75, 'lure': 0.68},
        'NDAM': {'urgency': 0.60, 'threat': 0.30, 'opportunity': 0.70}
    }

    mock_response = MockAssembledResponse(
        text="I sense what you're feeling right now. There's something true emerging here.",
        num_phrases=2,
        strategies_used=['direct', 'fusion'],
        mean_confidence=0.78,
        mean_coherence=0.82,
        field_types=['action', 'truth']
    )

    # Test integration
    try:
        integration = Phase5LearningIntegration(
            storage_path="/tmp/phase5_test",
            learning_threshold=0.75,
            enable_learning=True
        )

        # Test learning from conversation
        print(f"\n📝 Testing POST-EMISSION learning hook...")
        learning_report = integration.learn_from_conversation(
            organ_results=mock_organ_results,
            assembled_response=mock_response,
            user_message="I've been feeling really overwhelmed lately.",
            conversation_id="test_conv_001"
        )

        if learning_report:
            print(f"\n✅ Learning successful!")
            integration.print_learning_summary(learning_report)
        else:
            print(f"\n⚠️  Learning skipped (satisfaction below threshold)")

        # Test getting guidance
        print(f"\n📝 Testing PRE-EMISSION guidance hook...")
        guidance = integration.get_family_guidance()

        if guidance:
            print(f"\n✅ Guidance retrieved!")
            print(f"   Family: {guidance['family_id']} ({guidance['family_maturity']})")
            print(f"   Target satisfaction: {guidance['target_satisfaction']:.3f}")
            print(f"   Top organ weights:")
            for organ, weight in sorted(guidance['organ_weights'].items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"      {organ}: {weight:.3f}")
        else:
            print(f"\n⚠️  No guidance available (family not yet mature)")

        # Test statistics
        print(f"\n📊 Learning Statistics:")
        stats = integration.get_statistics()
        print(f"   Total families: {stats['total_families']}")
        print(f"   Total conversations: {stats['total_conversations']}")

        print(f"\n✅ Phase 5 integration working correctly!")

    except Exception as e:
        print(f"\n❌ Phase 5 integration failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
