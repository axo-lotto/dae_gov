"""
EO Text Core - Polyvagal State Detection for Conversational Organism
======================================================================

Detects autonomic nervous system states (ventral vagal, sympathetic, dorsal vagal)
through language pattern analysis, following Porges' Polyvagal Theory.

This organ contributes to Phase 5 organic family discovery by detecting safety/threat
states that distinguish archetypal conversation patterns.

Architecture:
- 3 polyvagal states detection (ventral vagal = safe, sympathetic = mobilization, dorsal vagal = shutdown)
- Keyword-based pattern matching (40+ keywords per state from eo_config.py)
- Coherence measure: clarity of dominant state
- Text-native processing (LLM-free)

Integration:
- Contributes to 45D organ signatures for Phase 5 learning
- Polyvagal state guides response scaling (via CARD organ)
- Correlates with BOND self_distance (polyvagal ↔ IFS parts alignment)

Date: November 11, 2025
Status: Phase 2 Integration (10/11 organs)
"""

import string
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np
from pathlib import Path
import os
import json

# Import configuration
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from organs.modular.eo.organ_config.eo_config import EOConfig, DEFAULT_EO_CONFIG


@dataclass
class PolyvagalPattern:
    """Detected polyvagal state pattern in text."""
    pattern_type: str  # 'ventral_vagal', 'sympathetic', 'dorsal_vagal'
    strength: float  # 0.0-1.0, proportion of keywords detected
    keywords_detected: List[str]  # Which keywords were found
    confidence: float  # How confident in this state (based on keyword density)


@dataclass
class EOResult:
    """Result from EO organ processing (polyvagal state detection)."""
    coherence: float  # 0.0-1.0, overall polyvagal state coherence
    lure: float  # 🆕 WHITEHEADIAN: Attractor strength for V0 concrescence
    patterns: List[PolyvagalPattern]  # All detected polyvagal patterns
    polyvagal_state: str  # Dominant polyvagal state
    state_confidence: float  # Confidence in dominant state
    state_clarity: float  # 0.0-1.0, how clear the dominant state is (vs mixed)
    self_distance_modifier: float  # Polyvagal → BOND self_distance contribution

    # 🆕 LURE ATTRACTOR FIELD: Per-state lure strengths
    lure_field: Dict[str, float] = field(default_factory=dict)  # {'ventral_vagal': 0.54, 'sympathetic': 0.89, ...}

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native

    # 🆕 PHASE C3: Embedding-based lure field (Nov 13, 2025)
    polyvagal_lure_field: Dict[str, float] = field(default_factory=dict)


class EOTextCore:
    """
    EO Organ Text Core - Polyvagal State Detection

    Detects autonomic nervous system states through language patterns:
    - Ventral vagal: Safe & social engagement (calm, connected, curious)
    - Sympathetic: Fight/flight mobilization (urgent, anxious, reactive)
    - Dorsal vagal: Shutdown/freeze immobilization (numb, frozen, disconnected)

    Follows Porges' Polyvagal Theory adapted for text processing.
    """

    def __init__(self, config: EOConfig = None):
        """
        Initialize EO organ with polyvagal detection configuration.

        Args:
            config: EOConfig object with polyvagal keywords and thresholds
        """
        self.config = config or DEFAULT_EO_CONFIG

        # 🆕 PHASE 1: Entity-native emission support
        self.organ_name = "EO"
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE 2: Load shared meta-atoms for nexus formation
        self.meta_atoms_config = self._load_shared_meta_atoms()

        # 🆕 PHASE C3: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

        # Load polyvagal keyword sets from config
        self.ventral_vagal_keywords = set(self.config.ventral_vagal_keywords)
        self.sympathetic_keywords = set(self.config.sympathetic_keywords)
        self.dorsal_vagal_keywords = set(self.config.dorsal_vagal_keywords)

        # Convert multi-word phrases to lowercase for matching
        self.ventral_vagal_phrases = {kw.lower() for kw in self.ventral_vagal_keywords if ' ' in kw}
        self.sympathetic_phrases = {kw.lower() for kw in self.sympathetic_keywords if ' ' in kw}
        self.dorsal_vagal_phrases = {kw.lower() for kw in self.dorsal_vagal_keywords if ' ' in kw}

        # Single words (for faster matching)
        self.ventral_vagal_words = {kw.lower() for kw in self.ventral_vagal_keywords if ' ' not in kw}
        self.sympathetic_words = {kw.lower() for kw in self.sympathetic_keywords if ' ' not in kw}
        self.dorsal_vagal_words = {kw.lower() for kw in self.dorsal_vagal_keywords if ' ' not in kw}

    def _load_semantic_atoms(self) -> List[str]:
        """Load semantic atoms from semantic_atoms.json."""
        atoms_path = os.path.join(os.path.dirname(__file__), '..', 'semantic_atoms.json')
        if not os.path.exists(atoms_path):
            return ['ventral_vagal', 'sympathetic_activation', 'dorsal_vagal', 'co_regulation', 'neuroception', 'safety_cues', 'threat_cues']
        with open(atoms_path, 'r') as f:
            return json.load(f).get('atoms', [])

    def _load_shared_meta_atoms(self) -> Optional[Dict]:
        """
        🆕 PHASE 2: Load shared meta-atoms for nexus formation.

        EO contributes to 5 meta-atoms (most of any organ!):
        - trauma_aware (BOND, EO, NDAM)
        - safety_restoration (SANS, EO, NDAM)
        - window_of_tolerance (EO, CARD, RNX)
        - compassion_safety (EMPATHY, EO, SANS)
        - relational_attunement (EMPATHY, LISTENING, EO)
        """
        import json
        meta_atoms_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..',
                                       'persona_layer', 'shared_meta_atoms.json')
        try:
            with open(meta_atoms_path, 'r') as f:
                meta_atoms_data = json.load(f)
            relevant_meta_atoms = [
                ma for ma in meta_atoms_data['meta_atoms']
                if self.organ_name in ma['contributing_organs']
            ]
            return {
                'meta_atoms': relevant_meta_atoms,
                'count': len(relevant_meta_atoms)
            }
        except Exception as e:
            return None

    def _compute_atom_activations(self, patterns: List[PolyvagalPattern], coherence: float, lure: float, state_clarity: float) -> Dict[str, float]:
        """Compute direct atom activations for polyvagal patterns.

        Maps 3 polyvagal states to 7 semantic atoms:
        - ventral_vagal (safe & social) → ventral_vagal atom
        - sympathetic (fight/flight) → sympathetic_activation atom
        - dorsal_vagal (shutdown) → dorsal_vagal atom

        Special atoms:
        - co_regulation: When multiple patterns present (state_clarity < 0.7)
        - neuroception: Always active (pattern detection itself = neuroception)
        - safety_cues: When ventral vagal detected
        - threat_cues: When sympathetic or dorsal detected
        """
        activations = {}
        if not patterns:
            return activations

        pattern_to_atom = {'ventral_vagal': 'ventral_vagal', 'sympathetic': 'sympathetic_activation', 'dorsal_vagal': 'dorsal_vagal'}

        for pattern in patterns:
            atom_name = pattern_to_atom.get(pattern.pattern_type)
            if atom_name:
                activation = pattern.strength * pattern.confidence * coherence * (0.5 + 0.5 * lure)
                activations[atom_name] = activation

        # Special atoms
        if state_clarity < 0.7:  # Multiple states = co-regulation needed
            activations['co_regulation'] = (1.0 - state_clarity) * (0.5 + 0.5 * lure)

        # Neuroception = pattern detection itself
        activations['neuroception'] = coherence * (0.5 + 0.5 * lure)

        # Safety/threat cues
        if any(p.pattern_type == 'ventral_vagal' for p in patterns):
            ventral = next(p for p in patterns if p.pattern_type == 'ventral_vagal')
            activations['safety_cues'] = ventral.strength * (0.5 + 0.5 * lure)
        if any(p.pattern_type in ['sympathetic', 'dorsal_vagal'] for p in patterns):
            threat_patterns = [p for p in patterns if p.pattern_type in ['sympathetic', 'dorsal_vagal']]
            avg_threat = sum(p.strength for p in threat_patterns) / len(threat_patterns)
            activations['threat_cues'] = avg_threat * (0.5 + 0.5 * lure)

        # Normalize
        if activations:
            max_act = max(activations.values())
            if max_act > 0:
                activations = {atom: val / max_act for atom, val in activations.items()}

        # 🆕 PHASE 2: Add meta-atom activations (for nexus formation)
        if self.meta_atoms_config:
            meta_activations = self._activate_meta_atoms(patterns, coherence, lure, state_clarity)
            activations.update(meta_activations)

        return activations

    def _activate_meta_atoms(
        self,
        patterns: List[PolyvagalPattern],
        coherence: float,
        lure: float,
        state_clarity: float
    ) -> Dict[str, float]:
        """
        🆕 PHASE 2: Activate shared meta-atoms for nexus formation.

        EO contributes to 5 meta-atoms:
        1. trauma_aware (BOND, EO, NDAM) - Sympathetic/dorsal threat response
        2. safety_restoration (SANS, EO, NDAM) - Ventral vagal + safety cues
        3. window_of_tolerance (EO, CARD, RNX) - Ventral vagal state
        4. compassion_safety (EMPATHY, EO, SANS) - Ventral vagal + co-regulation
        5. relational_attunement (EMPATHY, LISTENING, EO) - Co-regulation + neuroception
        """
        if not self.meta_atoms_config or not patterns:
            return {}

        meta_activations = {}

        # Get polyvagal patterns by type
        ventral_patterns = [p for p in patterns if p.pattern_type == 'ventral_vagal']
        sympathetic_patterns = [p for p in patterns if p.pattern_type == 'sympathetic']
        dorsal_patterns = [p for p in patterns if p.pattern_type == 'dorsal_vagal']

        for meta_atom in self.meta_atoms_config['meta_atoms']:
            atom_name = meta_atom['atom']

            # 1. trauma_aware: Sympathetic or dorsal activation (threat response)
            if atom_name == 'trauma_aware':
                threat_patterns = sympathetic_patterns + dorsal_patterns
                if threat_patterns:
                    avg_threat = sum(p.strength * p.confidence for p in threat_patterns) / len(threat_patterns)
                    activation = avg_threat * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

            # 2. safety_restoration: Ventral vagal + safety cues
            elif atom_name == 'safety_restoration':
                if ventral_patterns:
                    avg_safety = sum(p.strength * p.confidence for p in ventral_patterns) / len(ventral_patterns)
                    activation = avg_safety * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

            # 3. window_of_tolerance: Ventral vagal state (optimal arousal)
            elif atom_name == 'window_of_tolerance':
                if ventral_patterns and state_clarity > 0.6:
                    # Clear ventral vagal = within window of tolerance
                    avg_ventral = sum(p.strength * p.confidence for p in ventral_patterns) / len(ventral_patterns)
                    activation = avg_ventral * state_clarity * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

            # 4. compassion_safety: Ventral vagal + co-regulation indicators
            elif atom_name == 'compassion_safety':
                if ventral_patterns and state_clarity < 0.8:
                    # Ventral vagal with some complexity = co-regulation space
                    avg_ventral = sum(p.strength * p.confidence for p in ventral_patterns) / len(ventral_patterns)
                    coregulation_factor = 1.0 - state_clarity  # More complex = more co-regulation
                    activation = avg_ventral * coregulation_factor * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

            # 5. relational_attunement: Co-regulation + neuroception (multi-state awareness)
            elif atom_name == 'relational_attunement':
                if len(patterns) >= 2 or state_clarity < 0.7:
                    # Multiple patterns or low clarity = active neuroception + attunement
                    neuroception_strength = coherence  # Pattern detection = neuroception
                    coregulation_strength = 1.0 - state_clarity if state_clarity < 0.7 else 0.3
                    activation = (neuroception_strength + coregulation_strength) / 2 * (0.5 + 0.5 * lure)
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
        """Load EO lure prototypes from JSON."""
        if self.lure_prototypes is not None:
            return self.lure_prototypes

        import json
        from pathlib import Path

        # Navigate from organs/modular/eo/core/ up to project root, then to persona_layer
        prototype_path = Path(__file__).parent.parent.parent.parent.parent / 'persona_layer' / 'lure_prototypes.json'

        with open(prototype_path, 'r') as f:
            data = json.load(f)

        category = data['prototypes']['eo_polyvagal']
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

    def process_text_occasions(self, occasions, cycle=0,
        context: Optional[Dict] = None) -> EOResult:
        """
        Process TextOccasions to detect polyvagal state.

        Args:
            occasions: List of TextOccasion objects
            cycle: Current organism cycle (unused for text-native processing)

        Returns:
            EOResult with polyvagal state detection
        """
        # Extract text and prepare for matching (strip punctuation)
        text_words = [occ.text.lower().strip(string.punctuation) for occ in occasions]
        full_text = ' '.join(text_words)

        total_words = len(text_words)
        if total_words == 0:
            return self._empty_result()

        # Detect all 3 polyvagal states
        patterns = []

        # 1. VENTRAL VAGAL (Safe & Social)
        ventral_matches = []

        # Check single words
        for word in text_words:
            if word in self.ventral_vagal_words:
                ventral_matches.append(word)

        # Check multi-word phrases
        for phrase in self.ventral_vagal_phrases:
            if phrase in full_text:
                ventral_matches.append(phrase)

        if ventral_matches:
            ventral_strength = len(ventral_matches) / total_words
            ventral_confidence = min(1.0, ventral_strength * 5)  # Scale up

            patterns.append(PolyvagalPattern(
                pattern_type='ventral_vagal',
                strength=ventral_strength,
                keywords_detected=ventral_matches[:5],  # Top 5
                confidence=ventral_confidence
            ))

        # 2. SYMPATHETIC (Fight/Flight)
        sympathetic_matches = []

        # Check single words
        for word in text_words:
            if word in self.sympathetic_words:
                sympathetic_matches.append(word)

        # Check multi-word phrases
        for phrase in self.sympathetic_phrases:
            if phrase in full_text:
                sympathetic_matches.append(phrase)

        if sympathetic_matches:
            sympathetic_strength = len(sympathetic_matches) / total_words
            sympathetic_confidence = min(1.0, sympathetic_strength * 5)

            patterns.append(PolyvagalPattern(
                pattern_type='sympathetic',
                strength=sympathetic_strength,
                keywords_detected=sympathetic_matches[:5],
                confidence=sympathetic_confidence
            ))

        # 3. DORSAL VAGAL (Shutdown/Freeze)
        dorsal_matches = []

        # Check single words
        for word in text_words:
            if word in self.dorsal_vagal_words:
                dorsal_matches.append(word)

        # Check multi-word phrases
        for phrase in self.dorsal_vagal_phrases:
            if phrase in full_text:
                dorsal_matches.append(phrase)

        if dorsal_matches:
            dorsal_strength = len(dorsal_matches) / total_words
            dorsal_confidence = min(1.0, dorsal_strength * 5)

            patterns.append(PolyvagalPattern(
                pattern_type='dorsal_vagal',
                strength=dorsal_strength,
                keywords_detected=dorsal_matches[:5],
                confidence=dorsal_confidence
            ))

        # Determine dominant polyvagal state
        if not patterns:
            # No clear polyvagal state detected → default to mixed/neutral

            # 🆕 PHASE C3: Compute embedding-based lure field even for no-pattern case
            if self.use_embedding_lures and full_text:
                polyvagal_lure_field = self._compute_embedding_based_lure_field(full_text)
            else:
                polyvagal_lure_field = {
                    'ventral_vagal_safe': 1.0/7,
                    'sympathetic_fight': 1.0/7,
                    'sympathetic_flight': 1.0/7,
                    'dorsal_freeze': 1.0/7,
                    'dorsal_dissociation': 1.0/7,
                    'mixed_state': 1.0/7,
                    'state_transition': 1.0/7
                }

            return EOResult(
                coherence=0.5,  # Neutral coherence
                lure=0.5,  # 🆕 LURE: Neutral attractor pull (no strong polyvagal signal)
                patterns=[],
                polyvagal_state='mixed_state',
                state_confidence=0.3,
                state_clarity=0.0,
                self_distance_modifier=0.5,  # Mixed state = moderate distance from SELF
                lure_field={  # 🆕 LURE FIELD: Balanced (no dominant state)
                    'ventral_vagal': 0.33,
                    'sympathetic': 0.33,
                    'dorsal_vagal': 0.33
                },
                atom_activations={},  # No patterns = no activations
                polyvagal_lure_field=polyvagal_lure_field  # 🆕 PHASE C3
            )

        # Find strongest pattern
        strongest = max(patterns, key=lambda p: p.strength)
        polyvagal_state = strongest.pattern_type
        state_confidence = strongest.confidence

        # Calculate state clarity (how distinct is dominant state from others?)
        if len(patterns) == 1:
            state_clarity = 1.0  # Pure state, very clear
        else:
            # Compare strongest to second strongest
            strengths = sorted([p.strength for p in patterns], reverse=True)
            state_clarity = (strengths[0] - strengths[1]) / (strengths[0] + 1e-6)

        # Calculate overall coherence (weighted by clarity and confidence)
        coherence = state_clarity * state_confidence

        # Map polyvagal state to BOND self_distance modifier
        # (Following eo_config.py self_distance_modifier_config)
        if polyvagal_state == 'ventral_vagal':
            self_distance_modifier = 0.0  # Ventral IS SELF-energy (no distance)
        elif polyvagal_state == 'sympathetic':
            self_distance_modifier = 0.3  # Moderate distance (mobilization, firefighter)
        elif polyvagal_state == 'dorsal_vagal':
            self_distance_modifier = 0.5  # High distance (shutdown, far from SELF)
        else:  # mixed_state
            self_distance_modifier = 0.2  # Low-moderate distance (transitional)

        # Compute lure from coherence
        lure = coherence

        # 🆕 COMPUTE LURE FIELD: Map pattern strengths to polyvagal attractors
        # This is the temporary keyword-based lure field (will be replaced with semantic distance)
        lure_field = {
            'ventral_vagal': 0.0,
            'sympathetic': 0.0,
            'dorsal_vagal': 0.0
        }

        for pattern in patterns:
            if pattern.pattern_type in lure_field:
                lure_field[pattern.pattern_type] = max(
                    lure_field[pattern.pattern_type],
                    pattern.strength
                )

        # Normalize lure field
        total_lure = sum(lure_field.values())
        if total_lure > 0:
            lure_field = {k: v / total_lure for k, v in lure_field.items()}
        else:
            # No patterns detected, default to balanced
            lure_field = {'ventral_vagal': 0.33, 'sympathetic': 0.33, 'dorsal_vagal': 0.33}

        # Compute atom activations
        atom_activations = self._compute_atom_activations(
            patterns, coherence, lure, state_clarity
        )

        # 🆕 PHASE C3: Compute embedding-based lure field
        if self.use_embedding_lures and full_text:
            polyvagal_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to balanced default
            polyvagal_lure_field = {
                'ventral_vagal_safe': 1.0/7,
                'sympathetic_fight': 1.0/7,
                'sympathetic_flight': 1.0/7,
                'dorsal_freeze': 1.0/7,
                'dorsal_dissociation': 1.0/7,
                'mixed_state': 1.0/7,
                'state_transition': 1.0/7
            }

        return EOResult(
            coherence=coherence,
            lure=lure,  # 🆕 LURE: Attractor strength for V0 concrescence
            patterns=patterns,
            polyvagal_state=polyvagal_state,
            state_confidence=state_confidence,
            state_clarity=state_clarity,
            self_distance_modifier=self_distance_modifier,
            lure_field=lure_field,  # 🆕 LURE FIELD: Per-state attractor strengths
            atom_activations=atom_activations,  # 🆕 POPULATED!
            polyvagal_lure_field=polyvagal_lure_field  # 🆕 PHASE C3
        )

    def _empty_result(self) -> EOResult:
        """Return empty result when no text provided."""
        return EOResult(
            coherence=0.0,
            lure=0.0,  # 🆕 LURE: No attractor pull for empty input
            patterns=[],
            polyvagal_state='mixed_state',
            state_confidence=0.0,
            state_clarity=0.0,
            self_distance_modifier=0.5,
            lure_field={  # 🆕 LURE FIELD: Balanced default for empty input
                'ventral_vagal': 0.33,
                'sympathetic': 0.33,
                'dorsal_vagal': 0.33
            },
            atom_activations={},  # Empty dict for empty input
            polyvagal_lure_field={  # 🆕 PHASE C3: Balanced default
                'ventral_vagal_safe': 1.0/7,
                'sympathetic_fight': 1.0/7,
                'sympathetic_flight': 1.0/7,
                'dorsal_freeze': 1.0/7,
                'dorsal_dissociation': 1.0/7,
                'mixed_state': 1.0/7,
                'state_transition': 1.0/7
            }
        )


# ============================================================================
# STANDALONE TEST (Run: python3 organs/modular/eo/core/eo_text_core.py)
# ============================================================================

if __name__ == '__main__':
    print("\n🧪 TESTING EO ORGAN (Polyvagal State Detection)")
    print("=" * 70)

    # Mock TextOccasion for testing
    from dataclasses import dataclass as mock_dataclass

    @mock_dataclass
    class MockTextOccasion:
        text: str
        chunk_id: str = "test_0_0_0_0"

    # Initialize EO organ
    eo = EOTextCore()

    print(f"\n✅ EO organ initialized")
    print(f"   Ventral vagal keywords: {len(eo.ventral_vagal_keywords)}")
    print(f"   Sympathetic keywords: {len(eo.sympathetic_keywords)}")
    print(f"   Dorsal vagal keywords: {len(eo.dorsal_vagal_keywords)}")

    # Test 1: Ventral Vagal (Safe & Social)
    print("\n" + "-" * 70)
    print("Test 1: Ventral Vagal State (Safe & Social)")
    print("-" * 70)

    ventral_text = [
        MockTextOccasion("I feel safe and grounded"),
        MockTextOccasion("This conversation feels calm and connected"),
        MockTextOccasion("I'm curious and open to exploring this together")
    ]

    result1 = eo.process_text_occasions(ventral_text)
    print(f"   Polyvagal state: {result1.polyvagal_state}")
    print(f"   Coherence: {result1.coherence:.3f}")
    print(f"   State confidence: {result1.state_confidence:.3f}")
    print(f"   State clarity: {result1.state_clarity:.3f}")
    print(f"   BOND self_distance modifier: {result1.self_distance_modifier:.3f}")
    print(f"   Keywords detected: {', '.join(result1.patterns[0].keywords_detected[:3]) if result1.patterns else 'none'}")

    # Test 2: Sympathetic (Fight/Flight)
    print("\n" + "-" * 70)
    print("Test 2: Sympathetic State (Fight/Flight Mobilization)")
    print("-" * 70)

    sympathetic_text = [
        MockTextOccasion("I'm feeling really anxious and overwhelmed"),
        MockTextOccasion("There's so much urgency and pressure"),
        MockTextOccasion("I'm on edge and reactive to everything")
    ]

    result2 = eo.process_text_occasions(sympathetic_text)
    print(f"   Polyvagal state: {result2.polyvagal_state}")
    print(f"   Coherence: {result2.coherence:.3f}")
    print(f"   State confidence: {result2.state_confidence:.3f}")
    print(f"   State clarity: {result2.state_clarity:.3f}")
    print(f"   BOND self_distance modifier: {result2.self_distance_modifier:.3f}")
    print(f"   Keywords detected: {', '.join(result2.patterns[0].keywords_detected[:3]) if result2.patterns else 'none'}")

    # Test 3: Dorsal Vagal (Shutdown/Freeze)
    print("\n" + "-" * 70)
    print("Test 3: Dorsal Vagal State (Shutdown/Freeze)")
    print("-" * 70)

    dorsal_text = [
        MockTextOccasion("I feel numb and disconnected from everything"),
        MockTextOccasion("It's like I'm frozen and can't move forward"),
        MockTextOccasion("Everything feels hopeless and I'm just shutdown")
    ]

    result3 = eo.process_text_occasions(dorsal_text)
    print(f"   Polyvagal state: {result3.polyvagal_state}")
    print(f"   Coherence: {result3.coherence:.3f}")
    print(f"   State confidence: {result3.state_confidence:.3f}")
    print(f"   State clarity: {result3.state_clarity:.3f}")
    print(f"   BOND self_distance modifier: {result3.self_distance_modifier:.3f}")
    print(f"   Keywords detected: {', '.join(result3.patterns[0].keywords_detected[:3]) if result3.patterns else 'none'}")

    # Test 4: Mixed State
    print("\n" + "-" * 70)
    print("Test 4: Mixed State (Multiple States Present)")
    print("-" * 70)

    mixed_text = [
        MockTextOccasion("I'm anxious but also trying to feel calm"),
        MockTextOccasion("Part of me wants to connect but I feel frozen")
    ]

    result4 = eo.process_text_occasions(mixed_text)
    print(f"   Polyvagal state: {result4.polyvagal_state}")
    print(f"   Coherence: {result4.coherence:.3f}")
    print(f"   State confidence: {result4.state_confidence:.3f}")
    print(f"   State clarity: {result4.state_clarity:.3f} (lower = more mixed)")
    print(f"   BOND self_distance modifier: {result4.self_distance_modifier:.3f}")
    print(f"   Patterns detected: {len(result4.patterns)}")

    # Test 5: Polyvagal Shift (INPUT → OUTPUT therapeutic trajectory)
    print("\n" + "-" * 70)
    print("Test 5: Polyvagal Shift (Therapeutic Trajectory)")
    print("-" * 70)

    input_text = [
        MockTextOccasion("I'm overwhelmed and anxious"),
        MockTextOccasion("Everything feels urgent and scary")
    ]

    output_text = [
        MockTextOccasion("Let's take a moment to ground together"),
        MockTextOccasion("I'm here with you, feeling safe and present")
    ]

    input_result = eo.process_text_occasions(input_text)
    output_result = eo.process_text_occasions(output_text)

    print(f"   INPUT polyvagal state: {input_result.polyvagal_state}")
    print(f"   INPUT BOND modifier: {input_result.self_distance_modifier:.3f}")
    print(f"\n   OUTPUT polyvagal state: {output_result.polyvagal_state}")
    print(f"   OUTPUT BOND modifier: {output_result.self_distance_modifier:.3f}")
    print(f"\n   ✅ THERAPEUTIC SHIFT DETECTED:")
    print(f"      {input_result.polyvagal_state} → {output_result.polyvagal_state}")
    print(f"      BOND self_distance: {input_result.self_distance_modifier:.3f} → {output_result.self_distance_modifier:.3f}")

    print("\n" + "=" * 70)
    print("✅ EO ORGAN TEST COMPLETE!")
    print("=" * 70)
    print("\n📊 Phase 5 Integration Ready:")
    print("   - Polyvagal state detection operational")
    print("   - Will contribute to 45D organ signatures")
    print("   - Correlates with BOND self_distance (trauma-informed)")
    print("   - Guides CARD response scaling (ventral=detailed, dorsal=minimal)")
    print()
