"""
Organ Signature Extractor - Phase 5 of Emission Architecture
==============================================================

Extract 57-dimensional organ-native felt signatures from existing organ prehensions.

Purpose:
- Leverage existing organ quality metrics (no new organ code needed)
- Extract composite 57D signatures from 11 operational organs (Phase 2 COMPLETE!)
- Enable organic family discovery through cosine similarity clustering
- Maintain semantic interpretability (each dimension has meaning)

Philosophy:
- Uses existing organ prehensions (already computed during emission)
- Each organ contributes 4-7 dimensions based on its output structure
- Trauma-informed learning (BOND self_distance critical)
- Organ-weighted optimization (discover which organs matter per family)

Integration Point:
- Called after emission generation (successful conversations)
- Input: organ_results dict from emission pipeline
- Output: 57D normalized signature for clustering

Date: November 11, 2025
Status: Phase 5 Implementation - 11-Organ System (Phase 2 COMPLETE)
Updated: November 11, 2025 - Added RNX, EO, CARD organs (8→11 organs, 45D→57D)
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

# Import organ agreement metrics (FAO-equivalent from FFITTSS T4)
try:
    from persona_layer.organ_agreement_metrics import OrganAgreementComputer, OrganAgreementState
except ImportError:
    # Fallback if running standalone
    OrganAgreementComputer = None
    OrganAgreementState = None


@dataclass
class CompositeOrganSignature:
    """
    57-dimensional organ-native felt signature.

    Composite of 11 organ contributions (Phase 2 COMPLETE):
    - LISTENING: 6D (attention, presence, reflection, tracking, quality, strength)
    - EMPATHY: 7D (validation, compassion, resonance, attunement, holding, quality, tone)
    - WISDOM: 7D (insight, reframe, perspective, pattern, context, quality, depth)
    - AUTHENTICITY: 6D (truth, vulnerability, courage, alignment, quality, strength)
    - PRESENCE: 6D (now, grounding, somatic, spaciousness, quality, depth)
    - BOND: 5D (self_distance, polarization, harmony, dominant_part, strength) [TRAUMA-INFORMED]
    - SANS: 4D (coherence, readiness, lure, convergence)
    - NDAM: 4D (urgency, threat, opportunity, salience)
    - RNX: 4D (temporal_state, urgency_level, pattern_strength, confidence) [PHASE 2]
    - EO: 4D (coherence, state_confidence, state_clarity, self_distance_modifier) [PHASE 2]
    - CARD: 4D (detail_level, confidence, length_scale, polyvagal_alignment) [PHASE 2]

    Total: 57 dimensions
    """
    signature: np.ndarray  # 57D L2-normalized vector
    conversation_id: str
    satisfaction_score: float

    # Organ contributions (for interpretability)
    organ_contributions: Dict[str, np.ndarray]  # {organ_name: organ_signature}

    # Metadata
    timestamp: str
    emission_text: str
    user_message: str


class OrganSignatureExtractor:
    """
    Extract 57D composite felt signatures from existing organ prehensions.

    Strategy:
    1. For each organ, extract quality metrics (4-7 floats per organ)
    2. Map categorical values to continuous [0, 1] ranges
    3. Assemble into 57D composite vector
    4. L2 normalize for cosine similarity clustering
    5. Store organ contributions for interpretability

    Organ Dimension Mapping (11 organs, Phase 2 COMPLETE):
    - LISTENING:     dims 0-6   (6 dimensions)
    - EMPATHY:       dims 6-13  (7 dimensions)
    - WISDOM:        dims 13-20 (7 dimensions)
    - AUTHENTICITY:  dims 20-26 (6 dimensions)
    - PRESENCE:      dims 26-32 (6 dimensions)
    - BOND:          dims 32-37 (5 dimensions) [TRAUMA-INFORMED]
    - SANS:          dims 37-41 (4 dimensions)
    - NDAM:          dims 41-45 (4 dimensions)
    - RNX:           dims 45-49 (4 dimensions) [PHASE 2]
    - EO:            dims 49-53 (4 dimensions) [PHASE 2]
    - CARD:          dims 53-57 (4 dimensions) [PHASE 2]

    Total: 57 dimensions
    """

    def __init__(self):
        """Initialize organ signature extractor (11 organs)."""
        # Organ dimension ranges (8 original + 3 Phase 2 organs)
        self.organ_dims = {
            'LISTENING': (0, 6),
            'EMPATHY': (6, 13),
            'WISDOM': (13, 20),
            'AUTHENTICITY': (20, 26),
            'PRESENCE': (26, 32),
            'BOND': (32, 37),
            'SANS': (37, 41),
            'NDAM': (41, 45),
            'RNX': (45, 49),   # Phase 2
            'EO': (49, 53),    # Phase 2
            'CARD': (53, 57)   # Phase 2
        }

        # Categorical mappings (to [0, 1] continuous)
        self._initialize_categorical_maps()

    def _initialize_categorical_maps(self):
        """Initialize categorical value mappings."""
        # LISTENING quality categories
        self.listening_quality_map = {
            'surface': 0.25,
            'engaged': 0.50,
            'deep': 0.75,
            'transformative': 1.00
        }

        # EMPATHY quality categories
        self.empathy_quality_map = {
            'distant': 0.20,
            'present': 0.40,
            'attuned': 0.60,
            'merged': 0.80,
            'resonant': 1.00
        }

        # EMPATHY emotional tone
        self.empathy_tone_map = {
            'neutral': 0.2,
            'warm': 0.4,
            'compassionate': 0.6,
            'tender': 0.8,
            'reverent': 1.0
        }

        # WISDOM quality categories
        self.wisdom_quality_map = {
            'reactive': 0.20,
            'observing': 0.40,
            'understanding': 0.60,
            'wise': 0.80,
            'transcendent': 1.00
        }

        # AUTHENTICITY quality categories
        self.authenticity_quality_map = {
            'guarded': 0.20,
            'honest': 0.40,
            'vulnerable': 0.60,
            'raw': 0.80,
            'transparent': 1.00
        }

        # PRESENCE quality categories
        self.presence_quality_map = {
            'distracted': 0.20,
            'aware': 0.40,
            'grounded': 0.60,
            'centered': 0.80,
            'timeless': 1.00
        }

        # BOND dominant part (IFS parts) [TRAUMA-INFORMED]
        self.bond_part_map = {
            'self_energy': 0.0,      # Optimal (SELF-led)
            'manager': 0.3,          # Protective (safe)
            'firefighter': 0.6,      # Reactive (medium risk)
            'exile': 1.0             # Wounded (high risk - slow down!)
        }

    def extract_composite_signature(
        self,
        organ_results: Dict,
        conversation_id: str,
        satisfaction_score: float,
        emission_text: str = "",
        user_message: str = "",
        timestamp: str = ""
    ) -> CompositeOrganSignature:
        """
        Extract 57D composite signature from organ results (11 organs).

        Args:
            organ_results: {organ_name: organ_result_dict} from emission pipeline
            conversation_id: Unique conversation identifier
            satisfaction_score: Overall satisfaction (0-1)
            emission_text: Generated response text
            user_message: User's message that prompted emission
            timestamp: ISO timestamp

        Returns:
            CompositeOrganSignature with 57D normalized signature
        """
        signature = np.zeros(57)
        organ_contributions = {}

        # Extract each organ's signature
        for organ_name, (start, end) in self.organ_dims.items():
            if organ_name in organ_results:
                organ_sig = self._extract_organ_signature(
                    organ_name,
                    organ_results[organ_name]
                )
                signature[start:end] = organ_sig
                organ_contributions[organ_name] = organ_sig
            else:
                # Missing organ - fill with zeros (neutral)
                organ_contributions[organ_name] = np.zeros(end - start)

        # L2 normalize for cosine similarity clustering
        norm = np.linalg.norm(signature)
        if norm > 1e-6:
            signature = signature / norm
        else:
            # All zeros - shouldn't happen, but handle gracefully
            signature = np.zeros(57)

        return CompositeOrganSignature(
            signature=signature,
            conversation_id=conversation_id,
            satisfaction_score=satisfaction_score,
            organ_contributions=organ_contributions,
            timestamp=timestamp,
            emission_text=emission_text,
            user_message=user_message
        )

    def _compute_organ_variances(self, organ_results: Dict) -> Dict[str, float]:
        """
        Compute activation variance per organ for discriminative weighting.

        High variance = discriminative (organ activates strongly in specific contexts)
        Low variance = generic (organ activates similarly across all contexts)

        Returns:
            Dict mapping organ_name -> variance score (0.0-1.0+)
        """
        organ_variances = {}

        for organ_name, result in organ_results.items():
            if not isinstance(result, dict):
                organ_variances[organ_name] = 0.0
                continue

            # Extract numeric values from organ result
            values = []
            for key, val in result.items():
                if isinstance(val, (int, float)) and not np.isnan(val) and not np.isinf(val):
                    # Normalize to [0, 1] range if needed
                    if key in ['coherence', 'quality', 'confidence', 'strength', 'readiness']:
                        values.append(float(val))
                    elif key == 'mean_self_distance':  # BOND organ
                        values.append(float(val))
                    elif key in ['urgency', 'threat', 'opportunity', 'salience']:  # NDAM
                        values.append(float(val))

            # Compute variance
            if len(values) >= 2:
                organ_variances[organ_name] = float(np.var(values))
            else:
                organ_variances[organ_name] = 0.0

        return organ_variances

    def extract_composite_signature_variance_weighted(
        self,
        organ_results: Dict,
        conversation_id: str,
        satisfaction_score: float,
        emission_text: str = "",
        user_message: str = "",
        timestamp: str = "",
        variance_amplification: float = 2.0  # INCREASED Nov 13, 2025: 1.0 → 2.0 for better discrimination
    ) -> CompositeOrganSignature:
        """
        Extract 57D composite signature with VARIANCE WEIGHTING.

        This method addresses the uniform centroid problem by amplifying
        discriminative organs (high variance) and dampening generic ones (low variance).

        Key Innovation:
        - Standard extraction: signature = organ_signatures → L2 normalize
        - Variance-weighted: signature = organ_signatures × (1 + variance) → L2 normalize

        Effect:
        - High-variance organs (e.g., WISDOM varies 0.2-0.9) get 2× weight
        - Low-variance organs (e.g., SANS always ~0.5) get 1× weight
        - Result: Signatures maintain discrimination through averaging

        Args:
            organ_results: {organ_name: organ_result_dict} from emission pipeline
            conversation_id: Unique conversation identifier
            satisfaction_score: Overall satisfaction (0-1)
            emission_text: Generated response text
            user_message: User's message that prompted emission
            timestamp: ISO timestamp
            variance_amplification: Scale factor for variance weighting (default=1.0)

        Returns:
            CompositeOrganSignature with 57D variance-weighted normalized signature
        """
        # Step 1: Compute organ activation variances
        organ_variances = self._compute_organ_variances(organ_results)

        # Step 2: Extract organ signatures (standard method)
        signature = np.zeros(57)
        organ_contributions = {}

        for organ_name, (start, end) in self.organ_dims.items():
            if organ_name in organ_results:
                organ_sig = self._extract_organ_signature(
                    organ_name,
                    organ_results[organ_name]
                )

                # Step 3: Apply variance weighting
                variance = organ_variances.get(organ_name, 0.0)
                # Weight range: 1.0 (low variance) → 2.0 (high variance)
                weight = 1.0 + (variance * variance_amplification)

                # Apply weight to signature
                weighted_sig = organ_sig * weight

                signature[start:end] = weighted_sig
                organ_contributions[organ_name] = weighted_sig
            else:
                # Missing organ - fill with zeros (neutral)
                organ_contributions[organ_name] = np.zeros(end - start)

        # Step 4: L2 normalize (as usual)
        norm = np.linalg.norm(signature)
        if norm > 1e-6:
            signature = signature / norm
        else:
            # All zeros - shouldn't happen, but handle gracefully
            signature = np.zeros(57)

        return CompositeOrganSignature(
            signature=signature,
            conversation_id=conversation_id,
            satisfaction_score=satisfaction_score,
            organ_contributions=organ_contributions,
            timestamp=timestamp,
            emission_text=emission_text,
            user_message=user_message
        )

    def _extract_organ_signature(self, organ_name: str, organ_result: Dict) -> np.ndarray:
        """
        Extract individual organ signature.

        Args:
            organ_name: Organ identifier
            organ_result: Organ output dictionary

        Returns:
            Organ-specific signature (4-7 dimensions)
        """
        if organ_name == 'LISTENING':
            return self._extract_listening_signature(organ_result)
        elif organ_name == 'EMPATHY':
            return self._extract_empathy_signature(organ_result)
        elif organ_name == 'WISDOM':
            return self._extract_wisdom_signature(organ_result)
        elif organ_name == 'AUTHENTICITY':
            return self._extract_authenticity_signature(organ_result)
        elif organ_name == 'PRESENCE':
            return self._extract_presence_signature(organ_result)
        elif organ_name == 'BOND':
            return self._extract_bond_signature(organ_result)
        elif organ_name == 'SANS':
            return self._extract_sans_signature(organ_result)
        elif organ_name == 'NDAM':
            return self._extract_ndam_signature(organ_result)
        elif organ_name == 'RNX':
            return self._extract_rnx_signature(organ_result)
        elif organ_name == 'EO':
            return self._extract_eo_signature(organ_result)
        elif organ_name == 'CARD':
            return self._extract_card_signature(organ_result)
        else:
            # Unknown organ - return zeros
            start, end = self.organ_dims.get(organ_name, (0, 0))
            return np.zeros(end - start)

    def _extract_listening_signature(self, result: Dict) -> np.ndarray:
        """Extract 6D LISTENING signature."""
        sig = np.zeros(6)

        # Dim 0: Attention score (0-1)
        sig[0] = result.get('attention_score', 0.5)

        # Dim 1: Presence level (0-1)
        sig[1] = result.get('presence_level', 0.5)

        # Dim 2: Reflection depth (0-1)
        sig[2] = result.get('reflection_depth', 0.5)

        # Dim 3: Tracking continuity (0-1)
        sig[3] = result.get('tracking_continuity', 0.5)

        # Dim 4: Dominant quality (categorical → [0, 1])
        quality = result.get('dominant_quality', 'engaged')
        sig[4] = self.listening_quality_map.get(quality, 0.5)

        # Dim 5: Mean pattern strength (0-2 → normalize to 0-1)
        patterns = result.get('patterns', [])
        if patterns:
            mean_strength = np.mean([p.get('strength', 1.0) for p in patterns])
            sig[5] = mean_strength / 2.0  # Normalize 0-2 → 0-1
        else:
            sig[5] = 0.5

        return sig

    def _extract_empathy_signature(self, result: Dict) -> np.ndarray:
        """Extract 7D EMPATHY signature."""
        sig = np.zeros(7)

        # Dim 0: Validation score (0-1)
        sig[0] = result.get('validation_score', 0.5)

        # Dim 1: Compassion level (0-1)
        sig[1] = result.get('compassion_level', 0.5)

        # Dim 2: Resonance depth (0-1)
        sig[2] = result.get('resonance_depth', 0.5)

        # Dim 3: Attunement quality (0-1)
        sig[3] = result.get('attunement_quality', 0.5)

        # Dim 4: Holding capacity (0-1)
        sig[4] = result.get('holding_capacity', 0.5)

        # Dim 5: Dominant quality (categorical → [0, 1])
        quality = result.get('dominant_quality', 'attuned')
        sig[5] = self.empathy_quality_map.get(quality, 0.6)

        # Dim 6: Emotional tone (categorical → [0, 1])
        tone = result.get('emotional_tone', 'warm')
        sig[6] = self.empathy_tone_map.get(tone, 0.4)

        return sig

    def _extract_wisdom_signature(self, result: Dict) -> np.ndarray:
        """Extract 7D WISDOM signature."""
        sig = np.zeros(7)

        # Dim 0: Insight score (0-1)
        sig[0] = result.get('insight_score', 0.5)

        # Dim 1: Reframe strength (0-1)
        sig[1] = result.get('reframe_strength', 0.5)

        # Dim 2: Meta perspective (0-1)
        sig[2] = result.get('meta_perspective', 0.5)

        # Dim 3: Pattern recognition (0-1)
        sig[3] = result.get('pattern_recognition', 0.5)

        # Dim 4: Contextual understanding (0-1)
        sig[4] = result.get('contextual_understanding', 0.5)

        # Dim 5: Dominant quality (categorical → [0, 1])
        quality = result.get('dominant_quality', 'understanding')
        sig[5] = self.wisdom_quality_map.get(quality, 0.6)

        # Dim 6: Integration depth (0-1)
        sig[6] = result.get('integration_depth', 0.5)

        return sig

    def _extract_authenticity_signature(self, result: Dict) -> np.ndarray:
        """Extract 6D AUTHENTICITY signature."""
        sig = np.zeros(6)

        # Dim 0: Truth alignment (0-1)
        sig[0] = result.get('truth_alignment', 0.5)

        # Dim 1: Vulnerability level (0-1)
        sig[1] = result.get('vulnerability_level', 0.5)

        # Dim 2: Courage score (0-1)
        sig[2] = result.get('courage_score', 0.5)

        # Dim 3: Self-alignment (0-1)
        sig[3] = result.get('self_alignment', 0.5)

        # Dim 4: Dominant quality (categorical → [0, 1])
        quality = result.get('dominant_quality', 'honest')
        sig[4] = self.authenticity_quality_map.get(quality, 0.4)

        # Dim 5: Expression strength (0-1)
        sig[5] = result.get('expression_strength', 0.5)

        return sig

    def _extract_presence_signature(self, result: Dict) -> np.ndarray:
        """Extract 6D PRESENCE signature."""
        sig = np.zeros(6)

        # Dim 0: Nowness (0-1)
        sig[0] = result.get('nowness', 0.5)

        # Dim 1: Grounding level (0-1)
        sig[1] = result.get('grounding_level', 0.5)

        # Dim 2: Somatic awareness (0-1)
        sig[2] = result.get('somatic_awareness', 0.5)

        # Dim 3: Spaciousness (0-1)
        sig[3] = result.get('spaciousness', 0.5)

        # Dim 4: Dominant quality (categorical → [0, 1])
        quality = result.get('dominant_quality', 'grounded')
        sig[4] = self.presence_quality_map.get(quality, 0.6)

        # Dim 5: Embodiment depth (0-1)
        sig[5] = result.get('embodiment_depth', 0.5)

        return sig

    def _extract_bond_signature(self, result: Dict) -> np.ndarray:
        """
        Extract 5D BOND signature (IFS trauma-informed).

        CRITICAL: Dim 0 (self_distance) is trauma indicator:
        - 0.0-0.3: Close to SELF (safe conversations)
        - 0.3-0.6: Moderate parts activation
        - 0.6-1.0: Trauma activated (slow down, gentle approach!)
        """
        sig = np.zeros(5)

        # Dim 0: Self-distance [TRAUMA-INFORMED] (0-1)
        # 0.0 = SELF-led (optimal), 1.0 = exile/trauma (high risk)
        sig[0] = result.get('mean_self_distance', 0.5)

        # Dim 1: Parts polarization (0-1)
        sig[1] = result.get('parts_polarization', 0.5)

        # Dim 2: Parts harmony (0-1)
        sig[2] = result.get('parts_harmony', 0.5)

        # Dim 3: Dominant part (categorical → [0, 1]) [TRAUMA-INFORMED]
        part = result.get('dominant_part', 'manager')
        sig[3] = self.bond_part_map.get(part, 0.3)

        # Dim 4: Pattern strength (0-2 → normalize to 0-1)
        patterns = result.get('patterns', [])
        if patterns:
            mean_strength = np.mean([p.get('strength', 1.0) for p in patterns])
            sig[4] = mean_strength / 2.0
        else:
            sig[4] = 0.5

        return sig

    def _extract_sans_signature(self, result: Dict) -> np.ndarray:
        """Extract 4D SANS signature (semantic coherence)."""
        sig = np.zeros(4)

        # Dim 0: Coherence (0-1)
        sig[0] = result.get('coherence', 0.5)

        # Dim 1: Emission readiness (0-1)
        sig[1] = result.get('lure', 0.5)  # 'lure' in SANS is emission readiness

        # Dim 2: Lure intensity (0-1)
        sig[2] = result.get('lure_intensity', 0.5)

        # Dim 3: Convergence score (0-1)
        sig[3] = result.get('convergence', 0.5)

        return sig

    def _extract_ndam_signature(self, result: Dict) -> np.ndarray:
        """Extract 4D NDAM signature (urgency/salience)."""
        sig = np.zeros(4)

        # Dim 0: Urgency level (0-1)
        sig[0] = result.get('urgency', 0.5)

        # Dim 1: Threat detection (0-1)
        sig[1] = result.get('threat', 0.5)

        # Dim 2: Opportunity salience (0-1)
        sig[2] = result.get('opportunity', 0.5)

        # Dim 3: Overall salience (0-1)
        sig[3] = result.get('salience', 0.5)

        return sig

    def _extract_rnx_signature(self, result: Dict) -> np.ndarray:
        """
        Extract 4D RNX signature (temporal patterns - Phase 2).

        Temporal state mapping:
        - crisis: 1.0 (high urgency, present moment)
        - sympathetic_pull: 0.75 (mobilization, future oriented)
        - concrescent: 0.5 (healthy unfolding, now)
        - restorative: 0.25 (healing, integration)
        """
        sig = np.zeros(4)

        # Dim 0: Temporal state (categorical → [0, 1])
        temporal_state_map = {
            'crisis': 1.0,
            'sympathetic_pull': 0.75,
            'concrescent': 0.5,
            'restorative': 0.25
        }
        temporal_state = result.get('temporal_state', 'concrescent')
        sig[0] = temporal_state_map.get(temporal_state, 0.5)

        # Dim 1: Urgency level (0-1)
        sig[1] = result.get('urgency_level', 0.5)

        # Dim 2: Pattern strength (0-2 → normalize to 0-1)
        patterns = result.get('patterns', [])
        if patterns:
            mean_strength = np.mean([p.get('strength', 1.0) for p in patterns])
            sig[2] = mean_strength / 2.0
        else:
            sig[2] = 0.5

        # Dim 3: Coherence/confidence (0-1)
        sig[3] = result.get('coherence', 0.5)

        return sig

    def _extract_eo_signature(self, result: Dict) -> np.ndarray:
        """
        Extract 4D EO signature (polyvagal state detection - Phase 2).

        Polyvagal state mapping:
        - ventral_vagal: 1.0 (safe & social, optimal)
        - mixed_state: 0.5 (transitional)
        - sympathetic: 0.3 (fight/flight mobilization)
        - dorsal_vagal: 0.0 (shutdown/freeze)
        """
        sig = np.zeros(4)

        # Dim 0: Coherence (polyvagal state coherence, 0-1)
        sig[0] = result.get('coherence', 0.5)

        # Dim 1: State confidence (0-1)
        sig[1] = result.get('state_confidence', 0.5)

        # Dim 2: State clarity (0-1) - how distinct is dominant state
        sig[2] = result.get('state_clarity', 0.5)

        # Dim 3: Self-distance modifier (polyvagal → trauma, 0-1)
        # ventral=0.0 (SELF-energy), sympathetic=0.3, dorsal=0.5 (high trauma)
        sig[3] = result.get('self_distance_modifier', 0.5)

        return sig

    def _extract_card_signature(self, result: Dict) -> np.ndarray:
        """
        Extract 4D CARD signature (response scaling - Phase 2).

        Response scale mapping:
        - comprehensive: 1.0 (detailed, SELF-led)
        - detailed: 0.75 (safe, ventral vagal)
        - moderate: 0.5 (mixed/default)
        - brief: 0.25 (sympathetic, mobilized)
        - minimal: 0.0 (dorsal vagal, shutdown)
        """
        sig = np.zeros(4)

        # Dim 0: Detail level (0-1)
        sig[0] = result.get('detail_level', 0.5)

        # Dim 1: Confidence in scale recommendation (0-1)
        sig[1] = result.get('confidence', 0.5)

        # Dim 2: Length scale (categorical → [0, 1])
        length_scale_map = {
            'comprehensive': 1.0,
            'detailed': 0.75,
            'moderate': 0.5,
            'brief': 0.25,
            'minimal': 0.0
        }
        recommended_scale = result.get('recommended_scale', 'moderate')
        sig[2] = length_scale_map.get(recommended_scale, 0.5)

        # Dim 3: Polyvagal alignment (how well CARD aligns with polyvagal state)
        # Extract from context or compute from recommended_scale consistency
        polyvagal_basis = result.get('polyvagal_basis', 'mixed_state')
        polyvagal_alignment_map = {
            'ventral_vagal': 1.0,  # Safe → detailed (aligned)
            'mixed_state': 0.5,    # Transitional → moderate (aligned)
            'sympathetic': 0.3,    # Mobilization → brief (aligned)
            'dorsal_vagal': 0.0    # Shutdown → minimal (aligned)
        }
        sig[3] = polyvagal_alignment_map.get(polyvagal_basis, 0.5)

        return sig

    def extract_transformation_signature(
        self,
        initial_felt_state: Dict,
        final_felt_state: Dict,
        user_input: str = "",
        response: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Extract 40D transformation signature from conversation.

        This method implements DAE 3.0's proven transformation-based clustering approach,
        adapted for conversational context. Instead of clustering "what the organism is",
        we cluster "how the organism transforms during conversation processing".

        DAE 3.0 Inspiration:
        - 37 families emerged from 35D INPUT→OUTPUT transformation signatures
        - Zipf's law distribution (α=0.73, R²=0.94) validates self-organization
        - Captures HOW felt-state changes, not what final state is

        Conversational Adaptation:
        - Initial state: Organism before processing user input
        - Final state: Organism after generating response
        - Signature: 40D vector encoding transformation dynamics

        Dimensions (40D total):
          [0-5]:   V0 Energy Transformation (initial, final, descent, ratio, cycles, kairos)
          [6-16]:  Organ Coherence SHIFTS (11 organs: final - initial)
          [17-19]: Polyvagal Transformation (initial, final, transition)
          [20-22]: Zone Transformation (initial, final, movement)
          [23-28]: Satisfaction Evolution (initial, final, improvement, variance, peak, binary)
          [29-32]: Convergence Characteristics (cycles, speedup, stability, nexus_count)
          [33-34]: Urgency Shift (initial, final)
          [35-37]: Emission Path (one-hot: direct/fusion/kairos)
          [38-39]: Reserved for future dimensions

        Args:
            initial_felt_state: Organism state before processing user input
            final_felt_state: Organism state after generating response
            user_input: User's message (optional, for future use)
            response: Response data (optional, for future use)

        Returns:
            40D transformation signature (L2 normalized)

        Date: November 15, 2025 (DAE 3.0 Legacy Integration)
        Reference: DAE3_HYPHAE1_ARCHITECTURE_COMPARISON_NOV15_2025.md
        """
        signature = np.zeros(40)

        # === V0 Energy Transformation (dims 0-5) ===
        initial_v0 = initial_felt_state.get('v0_initial', 1.0)
        final_v0 = final_felt_state.get('v0_final', 0.5)

        signature[0] = initial_v0
        signature[1] = final_v0
        signature[2] = initial_v0 - final_v0  # Descent magnitude (key discriminator!)
        signature[3] = abs(signature[2]) / max(initial_v0, 1e-6)  # Descent ratio
        signature[4] = final_felt_state.get('convergence_cycles', 3.0) - 3.0  # Cycles (normalized around 3)
        signature[5] = 1.0 if final_felt_state.get('kairos_detected', False) else 0.0

        # === Organ Coherence SHIFTS (dims 6-16) - KEY ADAPTATION FROM DAE 3.0 ===
        # DAE 3.0 insight: Cluster by HOW organs change, not what they are
        # 11 organs: LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE,
        #            BOND, SANS, NDAM, RNX, EO, CARD
        initial_organs = initial_felt_state.get('organ_coherences', {})
        final_organs = final_felt_state.get('organ_coherences', {})

        organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                       'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']

        for i, organ in enumerate(organ_names):
            initial_coh = initial_organs.get(organ, 0.5)
            final_coh = final_organs.get(organ, 0.5)
            signature[6 + i] = final_coh - initial_coh  # SHIFT (positive = strengthened)

        # === Polyvagal Transformation (dims 17-19) ===
        polyvagal_map = {'ventral': 0, 'sympathetic': 1, 'dorsal': 2}
        initial_poly = polyvagal_map.get(initial_felt_state.get('polyvagal_state', 'ventral'), 0)
        final_poly = polyvagal_map.get(final_felt_state.get('polyvagal_state', 'ventral'), 0)

        signature[17] = initial_poly / 2.0  # Normalize to [0, 1]
        signature[18] = final_poly / 2.0
        signature[19] = (final_poly - initial_poly) / 2.0  # Transition direction

        # === Zone Transformation (dims 20-22) ===
        initial_zone = initial_felt_state.get('zone', 1)
        final_zone = final_felt_state.get('zone', 1)

        signature[20] = (initial_zone - 1) / 4.0  # Normalize to [0, 1] (zones 1-5)
        signature[21] = (final_zone - 1) / 4.0
        signature[22] = (final_zone - initial_zone) / 4.0  # Zone movement

        # === Satisfaction Evolution (dims 23-28) ===
        initial_sat = initial_felt_state.get('satisfaction', 0.5)
        final_sat = final_felt_state.get('satisfaction_final', 0.5)

        signature[23] = initial_sat
        signature[24] = final_sat
        signature[25] = final_sat - initial_sat  # Improvement (key for family differentiation)
        signature[26] = abs(signature[25])  # Absolute change
        signature[27] = 1.0 if signature[25] > 0.05 else 0.0  # Binary improvement flag
        signature[28] = final_felt_state.get('satisfaction_variance', 0.0)

        # === Convergence Characteristics (dims 29-32) ===
        signature[29] = (final_felt_state.get('convergence_cycles', 3.0) - 1.0) / 4.0  # Normalized
        signature[30] = final_felt_state.get('convergence_speedup', 1.0)
        signature[31] = final_felt_state.get('v0_descent_stability', 0.5)
        signature[32] = final_felt_state.get('nexus_count', 5.0) / 15.0  # Normalized

        # === Urgency Shift (dims 33-34) ===
        initial_urgency = initial_felt_state.get('urgency', 0.0)
        final_urgency = final_felt_state.get('urgency', 0.0)

        signature[33] = initial_urgency
        signature[34] = final_urgency

        # === Emission Path (dims 35-37) - one-hot encoding ===
        emission_path = final_felt_state.get('emission_path', 'fusion')
        if emission_path == 'direct':
            signature[35:38] = [1.0, 0.0, 0.0]
        elif emission_path == 'fusion':
            signature[35:38] = [0.0, 1.0, 0.0]
        elif emission_path == 'kairos':
            signature[35:38] = [0.0, 0.0, 1.0]
        else:  # hebbian fallback
            signature[35:38] = [0.0, 0.0, 0.0]

        # === Reserved (dims 38-39) ===
        signature[38] = 0.0  # Future: Parts detection shift
        signature[39] = 0.0  # Future: Relational depth shift

        # L2 normalize to unit sphere (DAE 3.0 approach for cosine similarity)
        norm = np.linalg.norm(signature)
        if norm > 1e-6:
            signature = signature / norm
        else:
            # All zeros - return neutral signature
            signature = np.zeros(40)

        return signature

    def get_organ_contribution(
        self,
        composite: CompositeOrganSignature,
        organ_name: str
    ) -> Optional[np.ndarray]:
        """
        Get specific organ's contribution to composite signature.

        Args:
            composite: CompositeOrganSignature object
            organ_name: Organ identifier

        Returns:
            Organ signature (4-7D) or None if organ not present
        """
        return composite.organ_contributions.get(organ_name)

    def interpret_signature(self, composite: CompositeOrganSignature) -> Dict:
        """
        Interpret composite signature for human understanding.

        Returns:
            Dictionary with human-readable interpretations
        """
        interpretation = {
            'conversation_id': composite.conversation_id,
            'satisfaction': composite.satisfaction_score,
            'organ_summaries': {}
        }

        # Interpret each organ's contribution
        for organ_name, contrib in composite.organ_contributions.items():
            if organ_name == 'BOND':
                # Special handling for trauma-informed BOND
                self_distance = contrib[0]
                if self_distance < 0.3:
                    safety = 'SAFE (close to SELF)'
                elif self_distance < 0.6:
                    safety = 'MODERATE (parts activated)'
                else:
                    safety = 'TRAUMA ACTIVATED (slow down!)'

                interpretation['organ_summaries'][organ_name] = {
                    'self_distance': float(self_distance),
                    'safety_level': safety,
                    'mean_activation': float(np.mean(contrib))
                }
            else:
                interpretation['organ_summaries'][organ_name] = {
                    'mean_activation': float(np.mean(contrib)),
                    'max_dimension': float(np.max(contrib)),
                    'min_dimension': float(np.min(contrib))
                }

        return interpretation

    # ============================================================================
    # 57D ENHANCED TRANSFORMATION SIGNATURE WITH RNX/TSK INTEGRATION
    # November 16, 2025 - Enables multi-family emergence through nexus type tracking
    # ============================================================================

    def extract_transformation_signature_57d(
        self,
        initial_felt_state: Dict,
        final_felt_state: Dict,
        transduction_trajectory: List[Dict] = None,
        constraint_deltas: Dict = None,
        user_input: str = "",
        response: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Extract 57D transformation signature with RNX/TSK integration.

        This enhanced signature captures not just WHAT changed (organ coherences),
        but HOW the transformation flowed (nexus type transitions, constraint deltas,
        transductive vocabulary). This enables multi-family emergence by differentiating
        transformation patterns that share similar outcomes but have different pathways.

        Dimensions (57D total):
          [0-39]:  Base transformation (existing 40D)
          [40-42]: Nexus Type + Domain + Crisis (3D)
          [43-46]: Constraint Deltas: BOND, NDAM, SANS, EO (4D)
          [47-50]: Transductive Vocabulary (4D)
          [51-52]: Healing vs Crisis Scores (2D)
          [53-56]: RNX Activation Metrics (4D)

        Philosophy (from core_daedalea RNX/TSK documents):
        - Nexus type transitions capture "grammar between states"
        - Constraint deltas capture "flow of transformation"
        - RNX activation detects rhizomatic vs linear transformations
        - Mutual satisfaction guides integration, not suppression

        Args:
            initial_felt_state: Organism state before processing
            final_felt_state: Organism state after processing
            transduction_trajectory: List of NexusTransductionState dicts from V0 cycles
            constraint_deltas: Pre-computed constraint changes (optional)
            user_input: User message (for future use)
            response: Response data (for future use)

        Returns:
            57D transformation signature (L2 normalized)

        Date: November 16, 2025 (RNX/TSK Integration)
        Reference: RNX_TSK_57D_INVESTIGATION_NOV16_2025.md
        """
        # Start with base 40D signature
        signature = np.zeros(57)

        # === BASE 40D (existing logic, copied from extract_transformation_signature) ===

        # V0 Energy Transformation (dims 0-5)
        initial_v0 = initial_felt_state.get('v0_initial', 1.0)
        final_v0 = final_felt_state.get('v0_final', 0.5)

        signature[0] = initial_v0
        signature[1] = final_v0
        signature[2] = initial_v0 - final_v0  # Descent magnitude
        signature[3] = abs(signature[2]) / max(initial_v0, 1e-6)  # Descent ratio
        signature[4] = final_felt_state.get('convergence_cycles', 3.0) - 3.0
        signature[5] = 1.0 if final_felt_state.get('kairos_detected', False) else 0.0

        # Organ Coherence SHIFTS (dims 6-16)
        initial_organs = initial_felt_state.get('organ_coherences', {})
        final_organs = final_felt_state.get('organ_coherences', {})
        organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                       'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']
        for i, organ in enumerate(organ_names):
            initial_coh = initial_organs.get(organ, 0.5)
            final_coh = final_organs.get(organ, 0.5)
            signature[6 + i] = final_coh - initial_coh

        # Polyvagal Transformation (dims 17-19) - ONE-HOT STYLE for family discrimination
        # CRITICAL FIX (Nov 16, 2025): Use one-hot encoding for polyvagal state to create
        # orthogonal directions that break single-family clustering.
        # Old: continuous values [0, 0.5, 1.0] → high cosine similarity after L2 norm
        # New: one-hot style [1,0,0], [0,1,0], [0,0,1] → orthogonal directions
        final_poly_state = final_felt_state.get('polyvagal_state', 'ventral')
        if final_poly_state in ['ventral', 'ventral_vagal']:
            signature[17:20] = [1.0, 0.0, 0.0]  # Ventral = calm, connected
        elif final_poly_state in ['sympathetic']:
            signature[17:20] = [0.0, 1.0, 0.0]  # Sympathetic = fight/flight
        elif final_poly_state in ['dorsal', 'dorsal_vagal']:
            signature[17:20] = [0.0, 0.0, 1.0]  # Dorsal = shutdown, freeze
        else:  # mixed_state or other
            signature[17:20] = [0.33, 0.33, 0.33]  # Mixed = distributed activation

        # Zone Transformation (dims 20-22) - AMPLIFIED for family discrimination
        # CRITICAL FIX (Nov 16, 2025): Amplify zone signal to create better discrimination.
        # Zone 1 (SELF) vs Zone 5 (Collapse) should be maximally distant.
        # Old: (zone-1)/4 → values 0.0, 0.25, 0.5, 0.75, 1.0 (weak signal after L2 norm)
        # New: Amplify by 2.0× to increase signal strength relative to organ coherences
        initial_zone = initial_felt_state.get('zone', 1)
        final_zone = final_felt_state.get('zone', 1)
        # Amplification factor to make zones more discriminating
        zone_amplification = 2.0
        signature[20] = zone_amplification * (initial_zone - 1) / 4.0
        signature[21] = zone_amplification * (final_zone - 1) / 4.0
        signature[22] = zone_amplification * (final_zone - initial_zone) / 4.0

        # Satisfaction Evolution (dims 23-28)
        initial_sat = initial_felt_state.get('satisfaction', 0.5)
        final_sat = final_felt_state.get('satisfaction_final', 0.5)
        signature[23] = initial_sat
        signature[24] = final_sat
        signature[25] = final_sat - initial_sat
        signature[26] = abs(signature[25])
        signature[27] = 1.0 if signature[25] > 0.05 else 0.0
        signature[28] = final_felt_state.get('satisfaction_variance', 0.0)

        # Convergence Characteristics (dims 29-32)
        signature[29] = (final_felt_state.get('convergence_cycles', 3.0) - 1.0) / 4.0
        signature[30] = final_felt_state.get('convergence_speedup', 1.0)
        signature[31] = final_felt_state.get('v0_descent_stability', 0.5)
        signature[32] = final_felt_state.get('nexus_count', 5.0) / 15.0

        # Urgency Shift (dims 33-34) - AMPLIFIED for crisis discrimination
        # CRITICAL FIX (Nov 16, 2025): Amplify urgency to distinguish crisis vs calm families
        # Crisis (urgency 0.85) should be maximally distant from safety (urgency 0.0)
        initial_urgency = initial_felt_state.get('urgency', 0.0)
        final_urgency = final_felt_state.get('urgency', 0.0)
        urgency_amplification = 2.0  # Same as zone amplification
        signature[33] = urgency_amplification * initial_urgency
        signature[34] = urgency_amplification * final_urgency

        # Emission Path (dims 35-37)
        emission_path = final_felt_state.get('emission_path', 'fusion')
        if emission_path == 'direct':
            signature[35:38] = [1.0, 0.0, 0.0]
        elif emission_path == 'fusion':
            signature[35:38] = [0.0, 1.0, 0.0]
        elif emission_path == 'kairos':
            signature[35:38] = [0.0, 0.0, 1.0]
        else:
            signature[35:38] = [0.0, 0.0, 0.0]

        # Reserved for backward compatibility (dims 38-39)
        # Now used for nexus type encoding below

        # === NEW RNX/TSK DIMENSIONS (17D: dims 40-56) ===

        if transduction_trajectory and len(transduction_trajectory) > 0:
            initial_trans = transduction_trajectory[0]
            final_trans = transduction_trajectory[-1]

            # Nexus Type Transition (dims 40-42)
            initial_nexus_type = initial_trans.get('current_type', 'Relational')
            final_nexus_type = final_trans.get('current_type', 'Relational')

            signature[40] = self._map_nexus_type_to_scalar(initial_nexus_type)
            signature[41] = self._map_nexus_type_to_scalar(final_nexus_type)

            # Domain shift (GUT=0, PSYCHE=1, SOCIAL_CONTEXT=2)
            domain_map = {'GUT': 0.0, 'PSYCHE': 0.5, 'SOCIAL_CONTEXT': 1.0}
            initial_domain = domain_map.get(initial_trans.get('domain', 'PSYCHE'), 0.5)
            final_domain = domain_map.get(final_trans.get('domain', 'PSYCHE'), 0.5)
            signature[42] = final_domain - initial_domain

            # Constraint Deltas (dims 43-46) - The "grammar of flow"
            if constraint_deltas:
                signature[43] = constraint_deltas.get('delta_protection', 0.0)  # BOND
                signature[44] = constraint_deltas.get('delta_urgency', 0.0)      # NDAM
                signature[45] = constraint_deltas.get('delta_coherence', 0.0)    # SANS
                signature[46] = constraint_deltas.get('delta_rhythm', 0.0)       # RNX/EO
            else:
                # Compute from felt states if not pre-computed
                signature[43] = final_felt_state.get('bond_self_distance', 0.5) - initial_felt_state.get('bond_self_distance', 0.5)
                signature[44] = final_felt_state.get('ndam_urgency', 0.0) - initial_felt_state.get('ndam_urgency', 0.0)
                signature[45] = final_felt_state.get('sans_coherence', 0.5) - initial_felt_state.get('sans_coherence', 0.5)
                signature[46] = final_trans.get('rhythm_coherence', 0.5) - initial_trans.get('rhythm_coherence', 0.5)

            # Transductive Vocabulary (dims 47-50) - Felt-state modulation markers
            # Average across trajectory for stability
            signal_inflations = [t.get('signal_inflation', 0.0) for t in transduction_trajectory]
            salience_drifts = [t.get('salience_drift', 0.0) for t in transduction_trajectory]
            prehensive_overloads = [t.get('prehensive_overload', 0.0) for t in transduction_trajectory]
            coherence_leakages = [t.get('coherence_leakage', 0.0) for t in transduction_trajectory]

            signature[47] = np.mean(signal_inflations) if signal_inflations else 0.0
            signature[48] = np.mean(salience_drifts) if salience_drifts else 0.0
            signature[49] = np.mean(prehensive_overloads) if prehensive_overloads else 0.0
            signature[50] = np.mean(coherence_leakages) if coherence_leakages else 0.0

            # Healing vs Crisis Scores (dims 51-52)
            # Crisis score: How much crisis-oriented nexus types were activated
            crisis_types = {'Paradox', 'Dissociative', 'Disruptive', 'Recursive', 'Looped', 'Urgency'}
            crisis_count = sum(1 for t in transduction_trajectory if t.get('current_type') in crisis_types)
            crisis_score = crisis_count / max(len(transduction_trajectory), 1)

            # Healing score: Improvement in mutual satisfaction + rhythm coherence
            initial_mutual_sat = initial_trans.get('mutual_satisfaction', 0.5)
            final_mutual_sat = final_trans.get('mutual_satisfaction', 0.5)
            healing_score = max(0.0, final_mutual_sat - initial_mutual_sat) + max(0.0, signature[46])

            signature[51] = crisis_score
            signature[52] = min(1.0, healing_score)

            # RNX Activation Metrics (dims 53-56) - Rhizomatic emergence detection
            rnx_activation = self._compute_rnx_activation_score(
                transduction_trajectory, initial_felt_state, final_felt_state
            )
            signature[53] = rnx_activation

            # Bifurcation intensity (Kairos + RNX combined)
            kairos_factor = 1.5 if final_felt_state.get('kairos_detected', False) else 1.0
            signature[54] = rnx_activation * kairos_factor

            # Transition mechanism encoding (9 pathways → continuous)
            mechanism = final_trans.get('transition_mechanism', 'maintain')
            signature[55] = self._map_mechanism_to_scalar(mechanism)

            # Multi-cycle trajectory coherence
            if len(transduction_trajectory) > 1:
                nexus_type_changes = sum(
                    1 for i in range(len(transduction_trajectory) - 1)
                    if transduction_trajectory[i].get('current_type') != transduction_trajectory[i+1].get('current_type')
                )
                trajectory_coherence = 1.0 - (nexus_type_changes / len(transduction_trajectory))
            else:
                trajectory_coherence = 1.0
            signature[56] = trajectory_coherence

        else:
            # No transduction data - fill with neutral values (backward compatible)
            signature[40:57] = 0.0

        # L2 normalize for cosine similarity clustering
        norm = np.linalg.norm(signature)
        if norm > 1e-6:
            signature = signature / norm
        else:
            signature = np.zeros(57)

        return signature

    def _map_nexus_type_to_scalar(self, nexus_type: str) -> float:
        """
        Map 14 nexus types to continuous scalar for signature embedding.

        Organized by domain and crisis orientation for meaningful distances:
        - GUT domain (somatic): 0.0 - 0.2
        - PSYCHE domain (relational): 0.3 - 0.6
        - SOCIAL_CONTEXT domain (systemic): 0.7 - 1.0
        """
        nexus_map = {
            # GUT domain (crisis-oriented, somatic)
            'Urgency': 0.0,
            'Disruptive': 0.1,
            'Looped': 0.2,
            # PSYCHE domain (relational)
            'Recursive': 0.3,
            'Dissociative': 0.4,
            'Relational': 0.5,
            'Innate': 0.55,
            'Protective': 0.6,
            # SOCIAL_CONTEXT domain (systemic)
            'Paradox': 0.7,
            'Contrast': 0.75,
            'Fragmented': 0.8,
            'Absorbed': 0.85,
            'Isolated': 0.9,
            'Pre-Existing': 1.0
        }
        return nexus_map.get(nexus_type, 0.5)

    def _map_mechanism_to_scalar(self, mechanism: str) -> float:
        """
        Map 9 transition mechanisms to continuous scalar.

        Organized from maintenance (0) to transformation (1):
        """
        mechanism_map = {
            'maintain': 0.0,
            'energy_discharge': 0.125,
            'coherence_repair': 0.25,
            'protective_consolidation': 0.375,
            'relational_opening': 0.5,
            'dissociation_integration': 0.625,
            'paradox_resolution': 0.75,
            'contrast_synthesis': 0.875,
            'innate_grounding': 1.0
        }
        return mechanism_map.get(mechanism, 0.0)

    def _compute_rnx_activation_score(
        self,
        transduction_trajectory: List[Dict],
        initial_felt_state: Dict,
        final_felt_state: Dict
    ) -> float:
        """
        Compute RNX (Rhizomatic Nexus) activation score.

        Based on Whiteheadian formula from core_daedalea:
        RNX = (P1 + P2) * T / S ± L

        Where:
        - P1 + P2: Conflicting parts (multivocal awareness)
        - T: Threshold breach (constraint exceeded)
        - S: Somatic ground available
        - L: Looping awareness (recursive patterns)

        High RNX = Rhizomatic emergence (non-linear, multi-directional)
        Low RNX = Linear transformation (single pathway)
        """
        if not transduction_trajectory:
            return 0.0

        # P1 + P2: Multivocal awareness (organ coherence variance)
        final_organs = final_felt_state.get('organ_coherences', {})
        if final_organs:
            organ_coherences = list(final_organs.values())
            multivocal = np.var(organ_coherences)
        else:
            multivocal = 0.0

        # T: Threshold breach detection
        v0_breach = 1.0 if initial_felt_state.get('v0_initial', 0.5) > 0.7 else 0.0
        urgency_breach = 1.0 if final_felt_state.get('ndam_urgency', 0.0) > 0.7 else 0.0
        trauma_breach = 1.0 if final_felt_state.get('bond_self_distance', 0.3) > 0.6 else 0.0
        threshold = max(v0_breach, urgency_breach, trauma_breach)

        # S: Somatic ground (polyvagal state + presence)
        polyvagal = final_felt_state.get('polyvagal_state', 'mixed')
        ventral_score = 1.0 if polyvagal == 'ventral' else 0.5 if polyvagal == 'sympathetic' else 0.2
        presence_ground = final_felt_state.get('PRESENCE_coherence', 0.5)
        somatic_ground = ventral_score * presence_ground

        # L: Looping awareness (recursive nexus detection)
        looping_count = sum(
            1 for t in transduction_trajectory
            if t.get('current_type') in ['Recursive', 'Looped']
        )
        looping_awareness = looping_count / max(len(transduction_trajectory), 1)

        # RNX formula: (multivocal * threshold) / somatic + looping
        rnx_raw = (multivocal * threshold) / max(somatic_ground, 0.1) + looping_awareness

        # Normalize to [0, 1]
        return min(1.0, rnx_raw / 3.0)

    def extract_transformation_signature_65d(
        self,
        initial_felt_state: Dict,
        final_felt_state: Dict,
        transduction_trajectory: List[Dict] = None,
        constraint_deltas: Dict = None,
        user_input: str = "",
        response: Optional[Dict] = None,
        normalize: bool = False  # 🆕 Nov 16, 2025: Default to raw for Euclidean distance
    ) -> np.ndarray:
        """
        Extract 65D transformation signature with organ agreement metrics.

        This enhanced signature adds FAO-equivalent organ agreement dimensions
        from FFITTSS T4 architecture to enable multi-family emergence through
        organ consensus patterns.

        Dimensions (65D total):
          [0-56]:   Base 57D transformation signature
          [57-64]:  Organ Agreement Metrics (8D) - NEW FAO-EQUIVALENT

        Organ Agreement Dimensions (8D):
          [57]: Pairwise Agreement (A) - FAO formula: (2/(k(k-1))) Σ_{i<j} (1 - |O_i - O_j|)
          [58]: Organ Entropy (H) - Information diversity
          [59]: Nexus Coherence - Cross-organ consensus strength
          [60]: Multiplicity Index - Whiteheadian specialization
          [61]: Mean Coherence - Overall activation level
          [62]: Std Coherence - Activation variance
          [63]: Max Disagreement - Largest organ conflict
          [64]: Field Harmony - DAE 3.0 style (1 - std)

        Philosophy (FFITTSS T4 + Whitehead):
        - High agreement = organs prehending same felt-sense (consensus)
        - Low agreement = organs detecting different aspects (specialization)
        - Multiplicity = diversity before unification ("the many become one")
        - These create ORTHOGONAL directions for family discrimination

        Integration with FFITTSS T4:
        - Pairwise Agreement: A(x,y) = (2/(k(k-1))) Σ_{i<j} (1 - |O_i - O_j|)
        - Nexus Density: coh_F ≥ 0.76 → 31.63% accuracy (Q3 range)
        - ΔE-once discipline: NDAM as exclusive source of exclusion energy

        Args:
            initial_felt_state: Organism state before processing
            final_felt_state: Organism state after processing
            transduction_trajectory: List of NexusTransductionState dicts
            constraint_deltas: Pre-computed constraint changes (optional)
            user_input: User message (for future use)
            response: Response data (for future use)

        Returns:
            65D transformation signature (raw by default, optionally L2 normalized)

        Date: November 16, 2025 (FAO Integration)
        Reference: FFITTSS T4/README.md, SIGNAL_AUDIT.md

        🆕 Nov 16, 2025 - CRITICAL FIX:
        Default normalize=False for Euclidean distance clustering.
        L2 normalization collapses magnitude information (crisis=high urgency 1.7 vs safety=low urgency 0.2).
        Raw signatures with Euclidean distance show 2.5× better family separation.
        """
        # 🆕 CRITICAL FIX (Nov 16, 2025): Build RAW 65D signature from scratch
        # DO NOT reuse normalized 57D - that loses magnitude information!
        # The test_non_normalized_signatures.py showed crisis vs safety = 3.72 distance (excellent!)
        # but that required building raw signatures from scratch.

        # Initialize 65D signature
        signature_65d = np.zeros(65)

        # ================================================================
        # DIMS 0-5: V0 Energy Transformation (RAW values)
        # ================================================================
        v0_initial = initial_felt_state.get('v0_initial', 1.0)
        v0_final = final_felt_state.get('v0_final', 0.5)
        signature_65d[0] = v0_initial
        signature_65d[1] = v0_final
        signature_65d[2] = v0_initial - v0_final  # Descent magnitude
        signature_65d[3] = abs(signature_65d[2]) / max(v0_initial, 1e-6)  # Relative descent
        signature_65d[4] = final_felt_state.get('convergence_cycles', 3.0) - 3.0  # Cycles offset
        signature_65d[5] = 1.0 if final_felt_state.get('kairos_detected', False) else 0.0

        # ================================================================
        # DIMS 6-16: Organ Coherence Shifts (RAW deltas)
        # ================================================================
        initial_organs = initial_felt_state.get('organ_coherences', {})
        final_organs = final_felt_state.get('organ_coherences', {})
        organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                       'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']
        for i, organ in enumerate(organ_names):
            signature_65d[6 + i] = final_organs.get(organ, 0.5) - initial_organs.get(organ, 0.5)

        # ================================================================
        # DIMS 17-19: Polyvagal State (one-hot encoding)
        # ================================================================
        final_poly = final_felt_state.get('polyvagal_state', 'ventral')
        if final_poly in ['ventral', 'ventral_vagal']:
            signature_65d[17:20] = [1.0, 0.0, 0.0]
        elif final_poly == 'sympathetic':
            signature_65d[17:20] = [0.0, 1.0, 0.0]
        elif final_poly in ['dorsal', 'dorsal_vagal']:
            signature_65d[17:20] = [0.0, 0.0, 1.0]
        else:
            signature_65d[17:20] = [0.33, 0.33, 0.33]

        # ================================================================
        # DIMS 20-22: Zone Transformation (AMPLIFIED - this is key for discrimination!)
        # ================================================================
        initial_zone = initial_felt_state.get('zone', 1)
        final_zone = final_felt_state.get('zone', 1)
        zone_amp = 2.0  # Amplify zone differences
        signature_65d[20] = zone_amp * (initial_zone - 1) / 4.0
        signature_65d[21] = zone_amp * (final_zone - 1) / 4.0
        signature_65d[22] = zone_amp * (final_zone - initial_zone) / 4.0

        # ================================================================
        # DIMS 23-28: Satisfaction Evolution
        # ================================================================
        initial_sat = initial_felt_state.get('satisfaction', 0.5)
        final_sat = final_felt_state.get('satisfaction_final', 0.5)
        signature_65d[23] = initial_sat
        signature_65d[24] = final_sat
        signature_65d[25] = final_sat - initial_sat
        signature_65d[26] = abs(signature_65d[25])
        signature_65d[27] = 1.0 if signature_65d[25] > 0.05 else 0.0
        signature_65d[28] = final_felt_state.get('satisfaction_variance', 0.0)

        # ================================================================
        # DIMS 29-32: Convergence Characteristics
        # ================================================================
        signature_65d[29] = (final_felt_state.get('convergence_cycles', 3.0) - 1.0) / 4.0
        signature_65d[30] = final_felt_state.get('convergence_speedup', 1.0)
        signature_65d[31] = final_felt_state.get('v0_descent_stability', 0.5)
        signature_65d[32] = final_felt_state.get('nexus_count', 5.0) / 15.0

        # ================================================================
        # DIMS 33-34: Urgency Shift (AMPLIFIED - key discriminator!)
        # ================================================================
        urgency_amp = 2.0
        signature_65d[33] = urgency_amp * initial_felt_state.get('urgency', 0.0)
        signature_65d[34] = urgency_amp * final_felt_state.get('urgency', 0.0)

        # ================================================================
        # DIMS 35-37: Emission Path (one-hot)
        # ================================================================
        emission_path = final_felt_state.get('emission_path', 'fusion')
        if emission_path == 'direct':
            signature_65d[35:38] = [1.0, 0.0, 0.0]
        elif emission_path == 'fusion':
            signature_65d[35:38] = [0.0, 1.0, 0.0]
        elif emission_path == 'kairos':
            signature_65d[35:38] = [0.0, 0.0, 1.0]
        else:
            signature_65d[35:38] = [0.0, 0.0, 0.0]

        # ================================================================
        # DIMS 38-56: Transduction Metrics (from trajectory if available)
        # ================================================================
        if transduction_trajectory:
            # Use the existing _compute methods for transduction-aware dimensions
            signature_65d[40] = self._compute_rnx_activation_score(
                transduction_trajectory, initial_felt_state, final_felt_state
            )
            # Add more transduction metrics as needed
            # For now, pad with zeros for simplicity
        else:
            signature_65d[38:57] = 0.0

        # ================================================================
        # DIMS 57-64: Organ Agreement Metrics (FAO-equivalent from FFITTSS T4)
        # ================================================================

        # Compute organ agreement metrics (FAO-equivalent)
        if OrganAgreementComputer is not None and final_organs:
            agreement_computer = OrganAgreementComputer()
            agreement_state = agreement_computer.compute_full_agreement_state(final_organs)

            # Add agreement dimensions (8D)
            signature_65d[57] = agreement_state.pairwise_agreement
            signature_65d[58] = agreement_state.organ_entropy
            signature_65d[59] = agreement_state.nexus_coherence
            signature_65d[60] = agreement_state.multiplicity_index
            signature_65d[61] = agreement_state.mean_coherence
            signature_65d[62] = agreement_state.std_coherence
            signature_65d[63] = agreement_state.max_disagreement
            signature_65d[64] = 1.0 - agreement_state.std_coherence  # Field harmony
        else:
            # Fallback if agreement computer not available
            if final_organs:
                coherences = list(final_organs.values())
                signature_65d[61] = np.mean(coherences)
                signature_65d[62] = np.std(coherences)
                signature_65d[64] = 1.0 - signature_65d[62]
            else:
                signature_65d[57:65] = 0.5  # Neutral values

        # 🆕 CRITICAL FIX (Nov 16, 2025): Only normalize if explicitly requested
        # Default is raw signatures for Euclidean distance clustering
        # L2 normalization collapses magnitude information (the root cause of single-family clustering!)
        if normalize:
            norm = np.linalg.norm(signature_65d)
            if norm > 1e-6:
                signature_65d = signature_65d / norm
            else:
                signature_65d = np.zeros(65)

        return signature_65d


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 ORGAN SIGNATURE EXTRACTOR TEST")
    print("="*70)

    # Mock organ results for testing
    mock_organ_results = {
        'LISTENING': {
            'attention_score': 0.85,
            'presence_level': 0.80,
            'reflection_depth': 0.75,
            'tracking_continuity': 0.70,
            'dominant_quality': 'deep',
            'patterns': [{'strength': 1.5}, {'strength': 1.8}]
        },
        'EMPATHY': {
            'validation_score': 0.90,
            'compassion_level': 0.85,
            'resonance_depth': 0.80,
            'attunement_quality': 0.75,
            'holding_capacity': 0.88,
            'dominant_quality': 'resonant',
            'emotional_tone': 'tender'
        },
        'WISDOM': {
            'insight_score': 0.78,
            'reframe_strength': 0.72,
            'meta_perspective': 0.80,
            'pattern_recognition': 0.75,
            'contextual_understanding': 0.70,
            'dominant_quality': 'wise',
            'integration_depth': 0.68
        },
        'BOND': {
            'mean_self_distance': 0.25,  # SAFE (close to SELF)
            'parts_polarization': 0.30,
            'parts_harmony': 0.75,
            'dominant_part': 'self_energy',  # Optimal!
            'patterns': [{'strength': 0.8}, {'strength': 1.0}]
        }
    }

    # Test signature extraction
    try:
        extractor = OrganSignatureExtractor()

        composite = extractor.extract_composite_signature(
            organ_results=mock_organ_results,
            conversation_id='test_001',
            satisfaction_score=0.82,
            emission_text="I sense what you're feeling deeply.",
            user_message="I feel stuck and afraid.",
            timestamp='2025-11-11T10:00:00'
        )

        print(f"\n✅ Signature extraction successful!")
        print(f"\n📊 COMPOSITE SIGNATURE:")
        print(f"   Conversation: {composite.conversation_id}")
        print(f"   Satisfaction: {composite.satisfaction_score:.3f}")
        print(f"   Signature shape: {composite.signature.shape}")
        print(f"   Signature norm: {np.linalg.norm(composite.signature):.6f} (should be ~1.0)")

        print(f"\n🔍 ORGAN CONTRIBUTIONS:")
        for organ_name, contrib in composite.organ_contributions.items():
            print(f"   {organ_name}: {contrib.shape} dims, mean={np.mean(contrib):.3f}")

        print(f"\n📝 INTERPRETATION:")
        interp = extractor.interpret_signature(composite)
        for organ_name, summary in interp['organ_summaries'].items():
            print(f"\n   {organ_name}:")
            for key, value in summary.items():
                if isinstance(value, str):
                    print(f"     {key}: {value}")
                else:
                    print(f"     {key}: {value:.3f}")

        # Test BOND trauma detection
        print(f"\n⚕️  TRAUMA-INFORMED BOND ANALYSIS:")
        bond_contrib = extractor.get_organ_contribution(composite, 'BOND')
        if bond_contrib is not None:
            self_distance = bond_contrib[0]
            print(f"   Self-distance: {self_distance:.3f}")
            if self_distance < 0.3:
                print(f"   Status: ✅ SAFE - Close to SELF-energy")
            elif self_distance < 0.6:
                print(f"   Status: ⚠️  MODERATE - Parts activated, proceed gently")
            else:
                print(f"   Status: 🚨 TRAUMA ACTIVATED - Slow down, increase holding!")

        print(f"\n✅ Organ signature extraction working correctly!")

    except Exception as e:
        print(f"\n❌ Signature extraction failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
