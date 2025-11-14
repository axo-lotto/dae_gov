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
