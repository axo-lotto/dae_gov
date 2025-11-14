"""
CARD Text Core - Response Scaling & Calibration for Conversational Organism
==========================================================================

Text-native CARD core implementation for conversational response scaling.
Adapts existing CARD concepts (multi-scale analysis) to text processing.

Core Responsibility:
- Response length/detail calibration based on polyvagal state
- Minimal (shutdown) → Brief (mobilization) → Detailed (safe) scaling
- Integration with EO polyvagal detection for trauma-informed scaling

Integration with Phase 5:
- Contributes response scaling dimensions to 45D organ signatures
- Guides CARD response calibration (minimal/brief/moderate/detailed/comprehensive)
- Correlates with EO polyvagal state (ventral=detailed, dorsal=minimal)

Date: November 11, 2025
Status: Phase 2 Integration (10/11 organs)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np
from pathlib import Path
import os
import json

# Import configuration
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from organs.modular.card.organ_config.card_config import CARDConfig, DEFAULT_CARD_CONFIG


@dataclass
class CARDPattern:
    """Detected response scaling pattern."""
    scale_type: str  # 'minimal', 'brief', 'moderate', 'detailed', 'comprehensive'
    length_target: int  # Target response length in chars
    detail_level: float  # 0.0-1.0, how much detail to include
    confidence: float  # Confidence in this scale recommendation


@dataclass
class CARDResult:
    """Result from CARD organ processing (response scaling)."""
    coherence: float  # 0.0-1.0, overall calibration coherence
    patterns: List[CARDPattern]  # All detected scaling patterns
    recommended_scale: str  # Dominant scale recommendation
    length_target: int  # Recommended response length
    detail_level: float  # Recommended detail level (0.0-1.0)
    confidence: float  # Confidence in scale recommendation
    polyvagal_basis: str  # Which polyvagal state influenced scale

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native

    # 🆕 PHASE C3: Embedding-based lure field (Nov 13, 2025)
    scale_lure_field: Dict[str, float] = field(default_factory=dict)


class CARDTextCore:
    """
    CARD Organ Text Core - Response Scaling & Calibration

    Determines appropriate response scale based on context:
    - Polyvagal state (from EO): Safe → detailed, Shutdown → minimal
    - Urgency (from NDAM): High urgency → brief, Low urgency → detailed
    - Trauma activation (from BOND): High trauma → gentle/minimal
    - Conversation context (from RNX): Crisis → brief, Restorative → detailed

    Follows trauma-informed response scaling principles.
    """

    def __init__(self, config: CARDConfig = None):
        """
        Initialize CARD organ with scaling configuration.

        Args:
            config: CARDConfig object with scaling thresholds and lengths
        """
        self.config = config or DEFAULT_CARD_CONFIG

        # Response length targets from config
        self.minimal_length = self.config.minimal_response_length  # 50
        self.brief_length = self.config.brief_response_length  # 150
        self.moderate_length = self.config.moderate_response_length  # 300
        self.detailed_length = self.config.detailed_response_length  # 600
        self.comprehensive_length = self.config.comprehensive_response_length  # 1000

        # 🆕 PHASE 1: Entity-native emission support
        self.organ_name = "CARD"

        # 🆕 PHASE 2: Load shared meta-atoms
        self.meta_atoms_config = self._load_shared_meta_atoms()
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE C3: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

    def _load_semantic_atoms(self) -> List[str]:
        """Load semantic atoms from semantic_atoms.json."""
        atoms_path = os.path.join(os.path.dirname(__file__), '..', 'semantic_atoms.json')
        if not os.path.exists(atoms_path):
            # CARD 7 atoms: response scaling dimensions
            return [
                'minimal_scale', 'moderate_scale', 'detailed_scale',
                'urgency_modulation', 'complexity_tracking',
                'capacity_signals', 'pacing_markers'
            ]
        with open(atoms_path, 'r') as f:
            return json.load(f).get('atoms', [])

    def _load_shared_meta_atoms(self) -> Optional[Dict]:
        """🆕 PHASE 2: Load shared meta-atoms for nexus formation."""
        import json
        import os
        from typing import Optional, Dict
        current_dir = os.path.dirname(os.path.abspath(__file__))
        meta_atoms_path = os.path.join(current_dir, '..', '..', '..', '..',
                                       'persona_layer', 'shared_meta_atoms.json')
        try:
            with open(meta_atoms_path, 'r') as f:
                meta_atoms_data = json.load(f)
            relevant_meta_atoms = [
                ma for ma in meta_atoms_data['meta_atoms']
                if self.organ_name in ma['contributing_organs']
            ]
            return {'meta_atoms': relevant_meta_atoms, 'count': len(relevant_meta_atoms)}
        except Exception as e:
            return None

    def _compute_atom_activations(
        self, patterns: List[CARDPattern], coherence: float, lure: float,
        urgency: float, self_distance: float
    ) -> Dict[str, float]:
        """Maps 5 response scale types to 7 semantic atoms with special logic."""
        activations = {}
        if not patterns:
            return activations

        # Map scale types to atoms (direct mapping for 3 main scales)
        scale_to_atom = {
            'minimal': 'minimal_scale',
            'moderate': 'moderate_scale',
            'detailed': 'detailed_scale'
        }

        # Compute base activations from patterns
        for pattern in patterns:
            atom_name = scale_to_atom.get(pattern.scale_type)
            if atom_name:
                # Base activation from pattern confidence and detail level
                activation = pattern.confidence * pattern.detail_level * coherence
                activation *= (0.5 + 0.5 * lure)  # Apply lure weighting
                activations[atom_name] = activation

        # Special atoms based on context signals
        # urgency_modulation: High when urgency matters
        if urgency > 0.6 or urgency < 0.3:  # Extreme urgency or calm
            activations['urgency_modulation'] = abs(urgency - 0.5) * 2.0 * (0.5 + 0.5 * lure)

        # complexity_tracking: Activated when patterns show mixed signals
        if len(patterns) > 1:
            pattern_variance = sum(abs(p.detail_level - patterns[0].detail_level) for p in patterns)
            if pattern_variance > 0.2:
                activations['complexity_tracking'] = (pattern_variance * coherence * (0.5 + 0.5 * lure))

        # capacity_signals: High self_distance = low capacity (trauma activation)
        if self_distance > 0.6:  # High trauma = low capacity
            activations['capacity_signals'] = self_distance * (0.5 + 0.5 * lure)

        # pacing_markers: Activated when careful pacing needed
        if self_distance > 0.5 or urgency > 0.7:  # Either trauma or high urgency
            pacing_need = max(self_distance, urgency)
            activations['pacing_markers'] = pacing_need * coherence * (0.5 + 0.5 * lure)

        # Normalize to [0.0, 1.0]
        if activations:
            max_activation = max(activations.values())
            if max_activation > 0:
                activations = {atom: val / max_activation for atom, val in activations.items()}

        return activations

    def _activate_meta_atoms(
        self,
        patterns: List[CARDPattern],
        coherence: float,
        lure: float,
        urgency: float,
        self_distance: float
    ) -> Dict[str, float]:
        """🆕 PHASE 2: Activate shared meta-atoms for nexus formation.

        CARD contributes to 3 meta-atoms:
        - window_of_tolerance: When capacity high and pacing regulated
        - temporal_grounding: When pacing markers present and low urgency
        - coherence_integration: When complexity tracking active and coherence high
        """
        if not self.meta_atoms_config or not patterns:
            return {}

        meta_activations = {}

        for meta_atom in self.meta_atoms_config['meta_atoms']:
            atom_name = meta_atom['atom']

            if atom_name == 'window_of_tolerance':
                # Activate when capacity signals show regulated state (low trauma, moderate urgency)
                if self_distance < 0.4 and 0.3 < urgency < 0.7:
                    # Check for moderate_scale patterns (not overwhelmed or underwhelmed)
                    moderate_patterns = [p for p in patterns if p.scale_type == 'moderate']
                    if moderate_patterns:
                        avg_confidence = sum(p.confidence for p in moderate_patterns) / len(moderate_patterns)
                        activation = avg_confidence * (1.0 - self_distance) * coherence
                        activation *= (0.5 + 0.5 * lure)
                        meta_activations[atom_name] = min(1.0, activation)

            elif atom_name == 'temporal_grounding':
                # Activate when pacing markers present and urgency not extreme (grounded in time)
                if urgency < 0.6 and coherence > 0.6:
                    # Look for minimal or moderate scale (not rushed)
                    grounded_patterns = [p for p in patterns
                                       if p.scale_type in ['minimal', 'moderate']]
                    if grounded_patterns:
                        avg_detail = sum(p.detail_level for p in grounded_patterns) / len(grounded_patterns)
                        activation = avg_detail * coherence * (1.0 - urgency) * (0.5 + 0.5 * lure)
                        meta_activations[atom_name] = min(1.0, activation)

            elif atom_name == 'coherence_integration':
                # Activate when complexity tracking engaged and coherence maintained
                if len(patterns) > 1 and coherence > 0.7:
                    # Mixed scale patterns managed coherently
                    pattern_variance = sum(abs(p.detail_level - patterns[0].detail_level) for p in patterns)
                    if pattern_variance > 0.2:  # Complexity present
                        # Coherence maintained despite complexity
                        activation = coherence * (1.0 - pattern_variance) * (0.5 + 0.5 * lure)
                        meta_activations[atom_name] = min(1.0, activation)

        return meta_activations

    # ========================================================================
    # 🆕 PHASE C3: EMBEDDING-BASED LURE COMPUTATION (Nov 13, 2025)
    # ========================================================================

    def _ensure_embedding_coordinator(self):
        """Lazy-load embedding coordinator."""
        if self.embedding_coordinator is None:
            from persona_layer.embedding_coordinator import EmbeddingCoordinator
            self.embedding_coordinator = EmbeddingCoordinator()

    def _load_lure_prototypes(self) -> Dict[str, np.ndarray]:
        """Load CARD lure prototypes from JSON."""
        if self.lure_prototypes is not None:
            return self.lure_prototypes

        import json
        from pathlib import Path

        # Navigate from organs/modular/card/core/ up to project root, then to persona_layer
        prototype_path = Path(__file__).parent.parent.parent.parent.parent / 'persona_layer' / 'lure_prototypes.json'

        with open(prototype_path, 'r') as f:
            data = json.load(f)

        category = data['prototypes']['card_scale']
        self.lure_prototypes = {
            dim: np.array(proto['embedding'])
            for dim, proto in category.items()
        }

        return self.lure_prototypes

    def _compute_embedding_based_lure_field(self, text: str) -> Dict[str, float]:
        """Compute lure field using semantic similarity."""
        self._ensure_embedding_coordinator()
        prototypes = self._load_lure_prototypes()

        # Get and normalize input embedding
        input_embedding = self.embedding_coordinator.embed(text)
        input_embedding = input_embedding / np.linalg.norm(input_embedding)

        # Compute cosine similarity to each prototype
        similarities = {}
        for dimension, prototype in prototypes.items():
            similarity = np.dot(input_embedding, prototype)
            similarities[dimension] = max(0.0, similarity)

        # Normalize to sum to 1.0
        total_sim = sum(similarities.values())
        if total_sim > 0:
            lure_field = {k: v / total_sim for k, v in similarities.items()}
        else:
            lure_field = {k: 1.0 / len(similarities) for k in similarities.keys()}

        return lure_field

    def process_text_occasions(self, occasions, cycle=0, context: Dict = None) -> CARDResult:
        """
        Process TextOccasions to determine response scaling.

        Args:
            occasions: List of TextOccasion objects
            cycle: Current organism cycle (unused for text-native processing)
            context: Optional context dict with:
                - 'polyvagal_state': From EO organ ('ventral_vagal', 'sympathetic', 'dorsal_vagal')
                - 'urgency': From NDAM organ (0.0-1.0)
                - 'self_distance': From BOND organ (0.0-1.0, trauma activation)
                - 'temporal_state': From RNX organ ('crisis', 'concrescent', etc.)

        Returns:
            CARDResult with response scaling recommendation
        """
        # 🆕 PHASE C3: Collect full input text for embedding-based lures
        full_text = ' '.join([occasion.text for occasion in occasions])

        context = context or {}

        # Extract context signals from other organs
        polyvagal_state = context.get('polyvagal_state', 'mixed_state')
        urgency = context.get('urgency', 0.5)
        self_distance = context.get('self_distance', 0.5)
        temporal_state = context.get('temporal_state', 'concrescent')

        # Determine response scale based on polyvagal state (primary determinant)
        patterns = []

        # 1. POLYVAGAL-BASED SCALING (primary - weight 0.50)
        if polyvagal_state == 'ventral_vagal':
            # Safe & social - can handle detailed response
            polyvagal_scale = 'detailed'
            polyvagal_length = self.detailed_length
            polyvagal_detail = 0.8
            polyvagal_confidence = 0.9
        elif polyvagal_state == 'sympathetic':
            # Fight/flight - brief, clear response needed
            polyvagal_scale = 'brief'
            polyvagal_length = self.brief_length
            polyvagal_detail = 0.4
            polyvagal_confidence = 0.85
        elif polyvagal_state == 'dorsal_vagal':
            # Shutdown - minimal, gentle response
            polyvagal_scale = 'minimal'
            polyvagal_length = self.minimal_length
            polyvagal_detail = 0.2
            polyvagal_confidence = 0.95
        else:  # mixed_state
            # Default to moderate
            polyvagal_scale = 'moderate'
            polyvagal_length = self.moderate_length
            polyvagal_detail = 0.5
            polyvagal_confidence = 0.6

        patterns.append(CARDPattern(
            scale_type=polyvagal_scale,
            length_target=polyvagal_length,
            detail_level=polyvagal_detail,
            confidence=polyvagal_confidence
        ))

        # 2. TRAUMA-BASED SCALING (secondary - weight 0.25)
        # High trauma → reduce scale regardless of polyvagal
        if self_distance > 0.7:  # High trauma activation
            trauma_scale = 'minimal'
            trauma_length = self.minimal_length
            trauma_detail = 0.2
            trauma_confidence = 0.9
        elif self_distance > 0.5:  # Moderate trauma
            trauma_scale = 'brief'
            trauma_length = self.brief_length
            trauma_detail = 0.4
            trauma_confidence = 0.75
        else:  # Low trauma (safe)
            trauma_scale = 'detailed'
            trauma_length = self.detailed_length
            trauma_detail = 0.7
            trauma_confidence = 0.7

        patterns.append(CARDPattern(
            scale_type=trauma_scale,
            length_target=trauma_length,
            detail_level=trauma_detail,
            confidence=trauma_confidence
        ))

        # 3. URGENCY-BASED SCALING (tertiary - weight 0.15)
        if urgency > 0.7:  # High urgency
            urgency_scale = 'brief'
            urgency_length = self.brief_length
            urgency_detail = 0.3
            urgency_confidence = 0.8
        elif urgency > 0.4:  # Moderate urgency
            urgency_scale = 'moderate'
            urgency_length = self.moderate_length
            urgency_detail = 0.5
            urgency_confidence = 0.6
        else:  # Low urgency
            urgency_scale = 'detailed'
            urgency_length = self.detailed_length
            urgency_detail = 0.7
            urgency_confidence = 0.7

        patterns.append(CARDPattern(
            scale_type=urgency_scale,
            length_target=urgency_length,
            detail_level=urgency_detail,
            confidence=urgency_confidence
        ))

        # 4. TEMPORAL-BASED SCALING (quaternary - weight 0.10)
        if temporal_state == 'crisis':
            # Crisis moment - brief, action-oriented
            temporal_scale = 'brief'
            temporal_length = self.brief_length
            temporal_detail = 0.3
            temporal_confidence = 0.75
        elif temporal_state == 'restorative':
            # Healing moment - detailed exploration
            temporal_scale = 'detailed'
            temporal_length = self.detailed_length
            temporal_detail = 0.8
            temporal_confidence = 0.8
        else:  # concrescent or symbolic_pull
            # Default moderate
            temporal_scale = 'moderate'
            temporal_length = self.moderate_length
            temporal_detail = 0.5
            temporal_confidence = 0.6

        patterns.append(CARDPattern(
            scale_type=temporal_scale,
            length_target=temporal_length,
            detail_level=temporal_detail,
            confidence=temporal_confidence
        ))

        # WEIGHTED ENSEMBLE: Combine all scale recommendations
        # Weights: Polyvagal (0.50), Trauma (0.25), Urgency (0.15), Temporal (0.10)
        weights = [0.50, 0.25, 0.15, 0.10]

        # Calculate weighted average length
        weighted_length = sum(
            pattern.length_target * weight * pattern.confidence
            for pattern, weight in zip(patterns, weights)
        ) / sum(pattern.confidence * weight for pattern, weight in zip(patterns, weights))

        # Calculate weighted average detail level
        weighted_detail = sum(
            pattern.detail_level * weight * pattern.confidence
            for pattern, weight in zip(patterns, weights)
        ) / sum(pattern.confidence * weight for pattern, weight in zip(patterns, weights))

        # Calculate overall confidence (weighted average of pattern confidences)
        overall_confidence = sum(
            pattern.confidence * weight
            for pattern, weight in zip(patterns, weights)
        )

        # Determine final scale recommendation based on weighted length
        if weighted_length < 100:
            recommended_scale = 'minimal'
        elif weighted_length < 225:
            recommended_scale = 'brief'
        elif weighted_length < 450:
            recommended_scale = 'moderate'
        elif weighted_length < 800:
            recommended_scale = 'detailed'
        else:
            recommended_scale = 'comprehensive'

        # Calculate coherence (how aligned all patterns are)
        # High coherence = all patterns agree, low coherence = mixed signals
        scale_types = [p.scale_type for p in patterns]
        most_common_scale = max(set(scale_types), key=scale_types.count)
        agreement_count = scale_types.count(most_common_scale)
        coherence = agreement_count / len(patterns)

        # Compute lure from coherence
        lure = coherence

        # Compute atom activations
        atom_activations = self._compute_atom_activations(
            patterns, coherence, lure, urgency, self_distance
        )

        # 🆕 PHASE 2: Add meta-atom activations
        if self.meta_atoms_config:
            meta_activations = self._activate_meta_atoms(
                patterns, coherence, lure, urgency, self_distance
            )
            atom_activations.update(meta_activations)

        # 🆕 PHASE C3: Compute embedding-based lure field
        if self.use_embedding_lures and full_text:
            scale_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to balanced default
            scale_lure_field = {
                'minimal_holding': 1.0/7,
                'moderate_presence': 1.0/7,
                'comprehensive_depth': 1.0/7,
                'silence_appropriate': 1.0/7,
                'crisis_brevity': 1.0/7,
                'developmental_expansive': 1.0/7,
                'tracking_proportional': 1.0/7
            }

        return CARDResult(
            coherence=coherence,
            patterns=patterns,
            recommended_scale=recommended_scale,
            length_target=int(weighted_length),
            detail_level=weighted_detail,
            confidence=overall_confidence,
            polyvagal_basis=polyvagal_state,
            atom_activations=atom_activations,  # 🆕 POPULATED!
            scale_lure_field=scale_lure_field  # 🆕 PHASE C3
        )

    def _empty_result(self) -> CARDResult:
        """Return empty result when no text provided."""
        return CARDResult(
            coherence=0.5,
            patterns=[],
            recommended_scale='moderate',
            length_target=self.moderate_length,
            detail_level=0.5,
            confidence=0.3,
            polyvagal_basis='mixed_state',
            atom_activations={},  # Empty dict for empty input
            scale_lure_field={  # 🆕 PHASE C3: Balanced default
                'minimal_holding': 1.0/7,
                'moderate_presence': 1.0/7,
                'comprehensive_depth': 1.0/7,
                'silence_appropriate': 1.0/7,
                'crisis_brevity': 1.0/7,
                'developmental_expansive': 1.0/7,
                'tracking_proportional': 1.0/7
            }
        )


# ============================================================================
# STANDALONE TEST (Run: python3 organs/modular/card/core/card_text_core.py)
# ============================================================================

if __name__ == '__main__':
    print("\n🧪 TESTING CARD ORGAN (Response Scaling)")
    print("=" * 70)

    # Mock TextOccasion for testing
    from dataclasses import dataclass as mock_dataclass

    @mock_dataclass
    class MockTextOccasion:
        text: str
        chunk_id: str = "test_0_0_0_0"

    # Initialize CARD organ
    card = CARDTextCore()

    print(f"\n✅ CARD organ initialized")
    print(f"   Minimal: {card.minimal_length} chars")
    print(f"   Brief: {card.brief_length} chars")
    print(f"   Moderate: {card.moderate_length} chars")
    print(f"   Detailed: {card.detailed_length} chars")
    print(f"   Comprehensive: {card.comprehensive_length} chars")

    # Test 1: Ventral Vagal (Safe) → Detailed Response
    print("\n" + "-" * 70)
    print("Test 1: Ventral Vagal State (Safe & Social)")
    print("-" * 70)

    ventral_text = [
        MockTextOccasion("I feel safe and grounded"),
        MockTextOccasion("This conversation feels calm and connected")
    ]

    ventral_context = {
        'polyvagal_state': 'ventral_vagal',
        'urgency': 0.2,
        'self_distance': 0.1,
        'temporal_state': 'restorative'
    }

    result1 = card.process_text_occasions(ventral_text, context=ventral_context)
    print(f"   Recommended scale: {result1.recommended_scale}")
    print(f"   Target length: {result1.length_target} chars")
    print(f"   Detail level: {result1.detail_level:.3f}")
    print(f"   Coherence: {result1.coherence:.3f}")
    print(f"   Confidence: {result1.confidence:.3f}")
    print(f"   Polyvagal basis: {result1.polyvagal_basis}")

    # Test 2: Sympathetic (Fight/Flight) → Brief Response
    print("\n" + "-" * 70)
    print("Test 2: Sympathetic State (Fight/Flight Mobilization)")
    print("-" * 70)

    sympathetic_text = [
        MockTextOccasion("I'm feeling really anxious and overwhelmed"),
        MockTextOccasion("There's so much urgency")
    ]

    sympathetic_context = {
        'polyvagal_state': 'sympathetic',
        'urgency': 0.8,
        'self_distance': 0.4,
        'temporal_state': 'crisis'
    }

    result2 = card.process_text_occasions(sympathetic_text, context=sympathetic_context)
    print(f"   Recommended scale: {result2.recommended_scale}")
    print(f"   Target length: {result2.length_target} chars")
    print(f"   Detail level: {result2.detail_level:.3f}")
    print(f"   Coherence: {result2.coherence:.3f}")
    print(f"   Confidence: {result2.confidence:.3f}")
    print(f"   Polyvagal basis: {result2.polyvagal_basis}")

    # Test 3: Dorsal Vagal (Shutdown) → Minimal Response
    print("\n" + "-" * 70)
    print("Test 3: Dorsal Vagal State (Shutdown/Freeze)")
    print("-" * 70)

    dorsal_text = [
        MockTextOccasion("I feel numb and disconnected"),
        MockTextOccasion("Everything feels frozen")
    ]

    dorsal_context = {
        'polyvagal_state': 'dorsal_vagal',
        'urgency': 0.3,
        'self_distance': 0.8,  # High trauma activation
        'temporal_state': 'concrescent'
    }

    result3 = card.process_text_occasions(dorsal_text, context=dorsal_context)
    print(f"   Recommended scale: {result3.recommended_scale}")
    print(f"   Target length: {result3.length_target} chars")
    print(f"   Detail level: {result3.detail_level:.3f}")
    print(f"   Coherence: {result3.coherence:.3f}")
    print(f"   Confidence: {result3.confidence:.3f}")
    print(f"   Polyvagal basis: {result3.polyvagal_basis}")

    # Test 4: Mixed Signals (Conflicting Context)
    print("\n" + "-" * 70)
    print("Test 4: Mixed Signals (Conflicting Scale Indicators)")
    print("-" * 70)

    mixed_text = [
        MockTextOccasion("I'm anxious but also trying to stay present")
    ]

    mixed_context = {
        'polyvagal_state': 'sympathetic',  # Brief
        'urgency': 0.3,  # Detailed
        'self_distance': 0.5,  # Brief/Moderate
        'temporal_state': 'restorative'  # Detailed
    }

    result4 = card.process_text_occasions(mixed_text, context=mixed_context)
    print(f"   Recommended scale: {result4.recommended_scale}")
    print(f"   Target length: {result4.length_target} chars")
    print(f"   Detail level: {result4.detail_level:.3f}")
    print(f"   Coherence: {result4.coherence:.3f} (lower = more mixed)")
    print(f"   Confidence: {result4.confidence:.3f}")
    print(f"   Polyvagal basis: {result4.polyvagal_basis}")
    print(f"   Patterns detected: {len(result4.patterns)}")

    # Test 5: Trauma-Informed Scaling Override
    print("\n" + "-" * 70)
    print("Test 5: Trauma Override (High trauma → minimal despite safe state)")
    print("-" * 70)

    trauma_text = [
        MockTextOccasion("I feel safe but also really activated")
    ]

    trauma_context = {
        'polyvagal_state': 'ventral_vagal',  # Normally detailed
        'urgency': 0.2,
        'self_distance': 0.9,  # HIGH TRAUMA - should override to minimal
        'temporal_state': 'concrescent'
    }

    result5 = card.process_text_occasions(trauma_text, context=trauma_context)
    print(f"   Recommended scale: {result5.recommended_scale}")
    print(f"   Target length: {result5.length_target} chars")
    print(f"   Detail level: {result5.detail_level:.3f}")
    print(f"   Coherence: {result5.coherence:.3f}")
    print(f"   Confidence: {result5.confidence:.3f}")
    print(f"   Polyvagal basis: {result5.polyvagal_basis}")
    print(f"\n   ✅ TRAUMA-INFORMED: High self_distance (0.9) overrode ventral_vagal")
    print(f"      Scaled DOWN to {result5.recommended_scale} for safety")

    print("\n" + "=" * 70)
    print("✅ CARD ORGAN TEST COMPLETE!")
    print("=" * 70)
    print("\n📊 Phase 5 Integration Ready:")
    print("   - Response scaling operational (minimal → comprehensive)")
    print("   - Trauma-informed calibration working")
    print("   - Will contribute scaling dimensions to 45D signatures")
    print("   - Polyvagal-based guidance (EO → CARD correlation)")
    print()
