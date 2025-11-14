"""
RNX Text Core - Temporal Pattern Detection for Conversational Organism
========================================================================

Text-native implementation of RNX (Rhythmic Nexus) organ for conversational epoch training.
Detects temporal patterns in therapeutic conversations using keyword-based state recognition.

Architecture adapted from DAE 3.0 ARC RNX organ, simplified for conversational text processing.

Temporal States (4 primitive classifications):
1. Crisis RNX:        Urgency escalating, entropy increasing
2. Concrescent RNX:   Stable convergence, balanced processing
3. Restorative RNX:   Healing trajectory, entropy decreasing
4. Symbolic Pull RNX: High volatility, conflicted/ambivalent

November 11, 2025 - Phase 2 Integration (DAE_HYPHAE_1)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import numpy as np
import os
import json


@dataclass
class RNXPattern:
    """Temporal pattern detected in text."""
    pattern_type: str  # 'crisis', 'concrescent', 'restorative', 'symbolic_pull'
    strength: float    # 0.0-1.0 confidence
    matched_keywords: List[str]  # Keywords that triggered this pattern


@dataclass
class RNXResult:
    """Result from RNX organ processing."""
    coherence: float  # 0.0-1.0, overall temporal coherence
    lure: float  # 🆕 WHITEHEADIAN: Temporal attractor strength for V0 concrescence
    patterns: List[RNXPattern]  # All detected patterns
    temporal_state: str  # Dominant temporal state
    state_confidence: float  # Confidence in dominant state
    rhythm_stability: float  # 0.0-1.0, how stable the temporal pattern is
    volatility: float  # 0.0-1.0, temporal volatility measure

    # 🆕 LURE ATTRACTOR FIELD: Temporal dynamics (kairos/rhythm/chronos)
    temporal_field: Dict[str, float] = field(default_factory=dict)

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native

    # 🆕 PHASE C3: Embedding-based lure field (Nov 13, 2025)
    temporal_lure_field: Dict[str, float] = field(default_factory=dict)


class RNXTextCore:
    """
    RNX Organ - Temporal Pattern Detection (Text-Native).

    Detects conversation rhythm and temporal states through keyword analysis.
    Critical for tracking therapeutic trajectory (crisis→restorative).
    """

    def __init__(self):
        """Initialize RNX organ with temporal state keywords."""

        # 🆕 PHASE 1: Entity-native emission support
        self.organ_name = "RNX"

        # 🆕 PHASE 2: Load shared meta-atoms
        self.meta_atoms_config = self._load_shared_meta_atoms()
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE C3: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

        # Crisis RNX keywords (urgency escalating, entropy increasing)
        self.crisis_keywords = {
            'crisis', 'emergency', 'urgent', 'critical', 'desperate',
            'overwhelmed', 'panic', 'terrified', 'collapsing', 'breaking',
            'unbearable', 'intolerable', 'worse', 'escalating', 'spiraling',
            'falling apart', 'losing control', 'can\'t cope', 'drowning',
            'suffocating', 'disintegrating', 'unraveling', 'imploding',
            'explosive', 'volatile', 'unstable', 'dangerous', 'out of control',
            'bleeding', 'dying', 'ending', 'catastrophic', 'terminal'
        }

        # Concrescent RNX keywords (stable convergence, balanced)
        self.concrescent_keywords = {
            'stable', 'steady', 'consistent', 'balanced', 'grounded',
            'centered', 'calm', 'peaceful', 'settled', 'organized',
            'coherent', 'integrated', 'whole', 'present', 'aware',
            'regulated', 'contained', 'supported', 'held', 'secure',
            'safe', 'comfortable', 'relaxed', 'at ease', 'aligned',
            'harmonious', 'unified', 'together', 'connected', 'attuned',
            'flowing', 'natural', 'effortless', 'clear', 'focused'
        }

        # Restorative RNX keywords (healing trajectory, entropy decreasing)
        self.restorative_keywords = {
            'better', 'improving', 'healing', 'recovering', 'growing',
            'learning', 'transforming', 'evolving', 'developing', 'maturing',
            'strengthening', 'empowering', 'liberating', 'freeing', 'opening',
            'expanding', 'deepening', 'integrating', 'resolving', 'releasing',
            'forgiving', 'accepting', 'embracing', 'trusting', 'hoping',
            'optimistic', 'encouraged', 'inspired', 'energized', 'renewed',
            'refreshed', 'restored', 'repaired', 'rebuilt', 'reborn',
            'breakthrough', 'insight', 'clarity', 'understanding', 'wisdom'
        }

        # Symbolic Pull RNX keywords (high volatility, conflicted/ambivalent)
        self.symbolic_pull_keywords = {
            'but', 'however', 'although', 'yet', 'conflicted', 'torn',
            'ambivalent', 'uncertain', 'confused', 'mixed', 'complicated',
            'paradox', 'contradiction', 'tension', 'struggle', 'battle',
            'fight', 'resist', 'oppose', 'contrary', 'inconsistent',
            'unstable', 'wavering', 'fluctuating', 'oscillating', 'shifting',
            'changing', 'unpredictable', 'erratic', 'chaotic', 'turbulent',
            'volatile', 'reactive', 'impulsive', 'sudden', 'unexpected',
            'shocking', 'jarring', 'disorienting', 'disruptive', 'disturbing'
        }

        # Thresholds for pattern detection
        self.pattern_threshold = 0.15  # Minimum strength to count as pattern
        self.dominance_threshold = 0.30  # Minimum strength for dominant state

    def _load_semantic_atoms(self) -> List[str]:
        """Load semantic atoms from semantic_atoms.json.

        Returns:
            List of semantic atom names for RNX organ
        """
        atoms_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'semantic_atoms.json'
        )

        if not os.path.exists(atoms_path):
            # Return default RNX atoms if file doesn't exist yet
            return [
                'crisis_temporal',
                'concrescent_temporal',
                'restorative_temporal',
                'symbolic_pull',
                'rhythm_markers',
                'phase_transitions',
                'temporal_anchors'
            ]

        with open(atoms_path, 'r') as f:
            data = json.load(f)
            return data.get('atoms', [])

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
        self,
        patterns: List[RNXPattern],
        coherence: float,
        lure: float,
        rhythm_stability: float,
        volatility: float
    ) -> Dict[str, float]:
        """
        Compute direct atom activations for RNX patterns.

        Maps RNX pattern types to semantic atoms:
        - crisis → crisis_temporal (high urgency, entropy increasing)
        - concrescent → concrescent_temporal (stable convergence)
        - restorative → restorative_temporal (healing trajectory)
        - symbolic_pull → symbolic_pull (ambivalence, conflict)

        Special atoms triggered by metrics:
        - rhythm_markers: When rhythm_stability > 0.7 (consistent pattern)
        - phase_transitions: When volatility > 0.6 (state changes)
        - temporal_anchors: When coherence > 0.7 (grounded temporal sense)

        Args:
            patterns: List of detected temporal patterns
            coherence: Overall temporal coherence (0-1)
            lure: Appetition pull (0-1)
            rhythm_stability: Rhythm stability measure (0-1)
            volatility: Temporal volatility (0-1)

        Returns:
            Dict mapping semantic atom names to activation strengths (0-1)
        """
        activations = {}

        if not patterns:
            return activations

        # Map each pattern to its corresponding semantic atom
        pattern_to_atom = {
            'crisis': 'crisis_temporal',
            'concrescent': 'concrescent_temporal',
            'restorative': 'restorative_temporal',
            'symbolic_pull': 'symbolic_pull'
        }

        # Compute activations for each pattern
        for pattern in patterns:
            atom_name = pattern_to_atom.get(pattern.pattern_type)
            if not atom_name:
                continue

            # Base activation: pattern strength modulated by coherence
            base_activation = pattern.strength * coherence

            # Apply lure weighting (0.5 to 1.0 range based on lure)
            lure_weight = 0.5 + 0.5 * lure
            activation = base_activation * lure_weight

            activations[atom_name] = activation

        # Special atoms based on rhythm and stability metrics

        # rhythm_markers: Activated when rhythm is stable (consistent temporal pattern)
        if rhythm_stability > 0.7:
            activations['rhythm_markers'] = rhythm_stability * (0.5 + 0.5 * lure)

        # phase_transitions: Activated when volatility is high (temporal state changes)
        if volatility > 0.6:
            activations['phase_transitions'] = volatility * (0.5 + 0.5 * lure)

        # temporal_anchors: Activated when coherence is high (grounded in time)
        if coherence > 0.7:
            activations['temporal_anchors'] = coherence * (0.5 + 0.5 * lure)

        # Normalize to [0, 1] while preserving relative intensities
        if activations:
            max_activation = max(activations.values())
            if max_activation > 0:
                activations = {
                    atom: val / max_activation
                    for atom, val in activations.items()
                }

        return activations

    def _activate_meta_atoms(
        self,
        patterns: List[RNXPattern],
        coherence: float,
        lure: float,
        rhythm_stability: float,
        volatility: float
    ) -> Dict[str, float]:
        """🆕 PHASE 2: Activate shared meta-atoms for nexus formation.

        RNX contributes to 3 meta-atoms:
        - window_of_tolerance: When rhythm stable and volatility low (regulated)
        - temporal_grounding: When temporal_anchors active and high coherence
        - kairos_emergence: When phase_transitions detected (opportune moment)
        """
        if not self.meta_atoms_config or not patterns:
            return {}

        meta_activations = {}

        for meta_atom in self.meta_atoms_config['meta_atoms']:
            atom_name = meta_atom['atom']

            if atom_name == 'window_of_tolerance':
                # Activate when rhythm stable and volatility low (regulated state)
                if rhythm_stability > 0.6 and volatility < 0.4:
                    activation = rhythm_stability * (1.0 - volatility) * coherence
                    activation *= (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

            elif atom_name == 'temporal_grounding':
                # Activate when temporal anchors present and high coherence
                if coherence > 0.65:
                    # Check for concrescent or restorative patterns (grounded temporality)
                    grounding_patterns = [p for p in patterns
                                        if p.pattern_type in ['concrescent', 'restorative']]
                    if grounding_patterns:
                        avg_strength = sum(p.strength for p in grounding_patterns) / len(grounding_patterns)
                        activation = avg_strength * coherence * (0.5 + 0.5 * lure)
                        meta_activations[atom_name] = min(1.0, activation)

            elif atom_name == 'kairos_emergence':
                # Activate when phase transitions detected (opportune moment for shift)
                if volatility > 0.6:
                    # Look for symbolic_pull or crisis→restorative transitions
                    transition_patterns = [p for p in patterns
                                         if p.pattern_type in ['symbolic_pull', 'crisis']]
                    if transition_patterns:
                        avg_strength = sum(p.strength for p in transition_patterns) / len(transition_patterns)
                        activation = avg_strength * volatility * coherence * (0.5 + 0.5 * lure)
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
        """Load RNX lure prototypes from JSON."""
        if self.lure_prototypes is not None:
            return self.lure_prototypes

        import json
        from pathlib import Path

        # Navigate from organs/modular/rnx/core/ up to project root, then to persona_layer
        prototype_path = Path(__file__).parent.parent.parent.parent.parent / 'persona_layer' / 'lure_prototypes.json'

        with open(prototype_path, 'r') as f:
            data = json.load(f)

        category = data['prototypes']['rnx_temporal']
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

    def process_text_occasions(
        self,
        occasions: List[Any],
        cycle: int = 0
    ) -> RNXResult:
        """
        Process text occasions through RNX temporal pattern detection.

        Args:
            occasions: List of TextOccasion objects (words/phrases)
            cycle: Processing cycle number (ignored in single-pass training)

        Returns:
            RNXResult with temporal state, patterns, coherence
        """

        # Extract text from occasions and create full text string
        # Strip punctuation from words for keyword matching
        import string
        text_words = [occ.text.lower().strip(string.punctuation) for occ in occasions]
        full_text = ' '.join(text_words)  # For multi-word phrase detection
        total_words = len(text_words)

        if total_words == 0:
            # Empty input - return neutral state
            return RNXResult(
                coherence=0.0,
                lure=0.0,  # 🆕 LURE: No temporal pull for empty input
                patterns=[],
                temporal_state='concrescent',
                state_confidence=0.0,
                rhythm_stability=0.0,
                volatility=0.0,
                temporal_field={'kairos': 0.33, 'rhythm': 0.33, 'chronos': 0.33},  # 🆕 Balanced default
                atom_activations={}  # Empty dict for empty input
            )

        # Detect patterns for each temporal state
        patterns = []

        # Crisis pattern detection (check both individual words and full text for phrases)
        crisis_matches = []
        for word in text_words:
            if word in self.crisis_keywords:
                crisis_matches.append(word)
        # Also check for multi-word phrases in full text
        for keyword in self.crisis_keywords:
            if ' ' in keyword and keyword in full_text and keyword not in crisis_matches:
                crisis_matches.append(keyword)
        crisis_strength = len(crisis_matches) / total_words
        if crisis_strength >= self.pattern_threshold:
            patterns.append(RNXPattern(
                pattern_type='crisis',
                strength=crisis_strength,
                matched_keywords=crisis_matches
            ))

        # Concrescent pattern detection (check both individual words and full text for phrases)
        concrescent_matches = []
        for word in text_words:
            if word in self.concrescent_keywords:
                concrescent_matches.append(word)
        for keyword in self.concrescent_keywords:
            if ' ' in keyword and keyword in full_text and keyword not in concrescent_matches:
                concrescent_matches.append(keyword)
        concrescent_strength = len(concrescent_matches) / total_words
        if concrescent_strength >= self.pattern_threshold:
            patterns.append(RNXPattern(
                pattern_type='concrescent',
                strength=concrescent_strength,
                matched_keywords=concrescent_matches
            ))

        # Restorative pattern detection (check both individual words and full text for phrases)
        restorative_matches = []
        for word in text_words:
            if word in self.restorative_keywords:
                restorative_matches.append(word)
        for keyword in self.restorative_keywords:
            if ' ' in keyword and keyword in full_text and keyword not in restorative_matches:
                restorative_matches.append(keyword)
        restorative_strength = len(restorative_matches) / total_words
        if restorative_strength >= self.pattern_threshold:
            patterns.append(RNXPattern(
                pattern_type='restorative',
                strength=restorative_strength,
                matched_keywords=restorative_matches
            ))

        # Symbolic Pull pattern detection (check both individual words and full text for phrases)
        symbolic_matches = []
        for word in text_words:
            if word in self.symbolic_pull_keywords:
                symbolic_matches.append(word)
        for keyword in self.symbolic_pull_keywords:
            if ' ' in keyword and keyword in full_text and keyword not in symbolic_matches:
                symbolic_matches.append(keyword)
        symbolic_strength = len(symbolic_matches) / total_words
        if symbolic_strength >= self.pattern_threshold:
            patterns.append(RNXPattern(
                pattern_type='symbolic_pull',
                strength=symbolic_strength,
                matched_keywords=symbolic_matches
            ))

        # Determine dominant temporal state
        if not patterns:
            # No clear pattern - default to concrescent (neutral/stable)
            temporal_state = 'concrescent'
            state_confidence = 0.5  # Low confidence (no strong signals)
            coherence = 0.5  # Neutral coherence
        else:
            # Find strongest pattern
            strongest = max(patterns, key=lambda p: p.strength)
            temporal_state = strongest.pattern_type
            state_confidence = strongest.strength

            # Coherence based on pattern clarity
            # High coherence = single dominant pattern
            # Low coherence = many conflicting patterns
            if len(patterns) == 1:
                coherence = strongest.strength
            else:
                # Multiple patterns - reduce coherence based on conflict
                pattern_strengths = [p.strength for p in patterns]
                coherence = strongest.strength * (1.0 - np.std(pattern_strengths))

        # Calculate rhythm stability (inverse of pattern diversity)
        # Stable rhythm = consistent pattern
        # Unstable rhythm = many different patterns with similar strength
        if len(patterns) <= 1:
            rhythm_stability = 1.0  # Very stable (single or no pattern)
        else:
            # Measure how much the strongest dominates
            pattern_strengths = [p.strength for p in patterns]
            max_strength = max(pattern_strengths)
            mean_strength = np.mean(pattern_strengths)
            rhythm_stability = max_strength / (mean_strength + 0.001)  # Avoid div by zero
            rhythm_stability = min(1.0, rhythm_stability / 2.0)  # Normalize

        # Calculate volatility (presence of symbolic pull + crisis)
        # High volatility = crisis OR symbolic pull dominates
        volatility = 0.0
        for pattern in patterns:
            if pattern.pattern_type in ['crisis', 'symbolic_pull']:
                volatility += pattern.strength
        volatility = min(1.0, volatility)  # Clamp to [0, 1]

        # 🆕 PHASE 1: Compute lure (appetition pull) from coherence and rhythm
        # Higher coherence and stable rhythm → higher lure
        lure = (coherence + rhythm_stability) / 2.0

        # 🆕 COMPUTE TEMPORAL FIELD: Kairos/rhythm/chronos dynamics
        # Temporary pattern-based field (will be replaced with sequence analysis)
        temporal_field = {
            'kairos': coherence * (1.0 - volatility),  # Opportune moment (low volatility)
            'rhythm': rhythm_stability,  # Pattern coherence
            'chronos': volatility  # Linear urgency (high in crisis)
        }

        # Normalize temporal field
        total_temporal = sum(temporal_field.values())
        if total_temporal > 0:
            temporal_field = {k: v / total_temporal for k, v in temporal_field.items()}
        else:
            temporal_field = {'kairos': 0.33, 'rhythm': 0.33, 'chronos': 0.33}

        # 🆕 PHASE 1: Compute atom activations for emission
        atom_activations = self._compute_atom_activations(
            patterns, coherence, lure, rhythm_stability, volatility
        )

        # 🆕 PHASE 2: Add meta-atom activations
        if self.meta_atoms_config:
            meta_activations = self._activate_meta_atoms(
                patterns, coherence, lure, rhythm_stability, volatility
            )
            atom_activations.update(meta_activations)

        # 🆕 PHASE C3: Compute embedding-based lure field
        if self.use_embedding_lures and full_text:
            temporal_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to balanced default
            temporal_lure_field = {
                'chronic_pattern': 1.0/7,
                'acute_event': 1.0/7,
                'cyclical_rhythm': 1.0/7,
                'developmental_phase': 1.0/7,
                'stuck_repetition': 1.0/7,
                'momentum_building': 1.0/7,
                'temporal_coherence': 1.0/7
            }

        return RNXResult(
            coherence=coherence,
            lure=lure,  # 🆕 LURE: Temporal attractor strength
            patterns=patterns,
            temporal_state=temporal_state,
            state_confidence=state_confidence,
            rhythm_stability=rhythm_stability,
            volatility=volatility,
            temporal_field=temporal_field,  # 🆕 TEMPORAL FIELD: Kairos/rhythm/chronos
            atom_activations=atom_activations,  # 🆕 POPULATED!
            temporal_lure_field=temporal_lure_field  # 🆕 PHASE C3
        )


def test_rnx_temporal_detection():
    """Test RNX temporal pattern detection with sample texts."""

    print("\n" + "="*70)
    print("🧪 TESTING RNX TEMPORAL PATTERN DETECTION")
    print("="*70 + "\n")

    # Mock TextOccasion class for testing
    class MockTextOccasion:
        def __init__(self, text):
            self.text = text
            self.embedding = np.zeros(384)

    rnx = RNXTextCore()

    # Test 1: Crisis text
    crisis_text = "I'm in a complete crisis. Everything is collapsing and I'm overwhelmed. This is unbearable and urgent."
    crisis_occasions = [MockTextOccasion(word) for word in crisis_text.split()]

    print("1️⃣ Testing CRISIS temporal state:")
    print(f"   Text: \"{crisis_text}\"")

    crisis_result = rnx.process_text_occasions(crisis_occasions, cycle=0)

    print(f"   Temporal state: {crisis_result.temporal_state}")
    print(f"   State confidence: {crisis_result.state_confidence:.3f}")
    print(f"   Coherence: {crisis_result.coherence:.3f}")
    print(f"   Volatility: {crisis_result.volatility:.3f}")
    print(f"   Rhythm stability: {crisis_result.rhythm_stability:.3f}")
    print(f"   Patterns detected: {len(crisis_result.patterns)}")
    for pattern in crisis_result.patterns:
        print(f"     - {pattern.pattern_type}: {pattern.strength:.3f} (keywords: {len(pattern.matched_keywords)})")
    print()

    # Test 2: Restorative text
    restorative_text = "I'm feeling better and improving each day. I'm learning and growing, finding healing and hope."
    restorative_occasions = [MockTextOccasion(word) for word in restorative_text.split()]

    print("2️⃣ Testing RESTORATIVE temporal state:")
    print(f"   Text: \"{restorative_text}\"")

    restorative_result = rnx.process_text_occasions(restorative_occasions, cycle=0)

    print(f"   Temporal state: {restorative_result.temporal_state}")
    print(f"   State confidence: {restorative_result.state_confidence:.3f}")
    print(f"   Coherence: {restorative_result.coherence:.3f}")
    print(f"   Volatility: {restorative_result.volatility:.3f}")
    print(f"   Rhythm stability: {restorative_result.rhythm_stability:.3f}")
    print(f"   Patterns detected: {len(restorative_result.patterns)}")
    for pattern in restorative_result.patterns:
        print(f"     - {pattern.pattern_type}: {pattern.strength:.3f} (keywords: {len(pattern.matched_keywords)})")
    print()

    # Test 3: Concrescent (stable) text
    concrescent_text = "I feel calm and centered, grounded in the present moment. Everything feels balanced and stable."
    concrescent_occasions = [MockTextOccasion(word) for word in concrescent_text.split()]

    print("3️⃣ Testing CONCRESCENT temporal state:")
    print(f"   Text: \"{concrescent_text}\"")

    concrescent_result = rnx.process_text_occasions(concrescent_occasions, cycle=0)

    print(f"   Temporal state: {concrescent_result.temporal_state}")
    print(f"   State confidence: {concrescent_result.state_confidence:.3f}")
    print(f"   Coherence: {concrescent_result.coherence:.3f}")
    print(f"   Volatility: {concrescent_result.volatility:.3f}")
    print(f"   Rhythm stability: {concrescent_result.rhythm_stability:.3f}")
    print(f"   Patterns detected: {len(concrescent_result.patterns)}")
    for pattern in concrescent_result.patterns:
        print(f"     - {pattern.pattern_type}: {pattern.strength:.3f} (keywords: {len(pattern.matched_keywords)})")
    print()

    # Test 4: Symbolic Pull (conflicted) text
    symbolic_text = "I feel better, but I'm still conflicted. I want to change, however I'm torn and uncertain about everything."
    symbolic_occasions = [MockTextOccasion(word) for word in symbolic_text.split()]

    print("4️⃣ Testing SYMBOLIC PULL temporal state:")
    print(f"   Text: \"{symbolic_text}\"")

    symbolic_result = rnx.process_text_occasions(symbolic_occasions, cycle=0)

    print(f"   Temporal state: {symbolic_result.temporal_state}")
    print(f"   State confidence: {symbolic_result.state_confidence:.3f}")
    print(f"   Coherence: {symbolic_result.coherence:.3f}")
    print(f"   Volatility: {symbolic_result.volatility:.3f}")
    print(f"   Rhythm stability: {symbolic_result.rhythm_stability:.3f}")
    print(f"   Patterns detected: {len(symbolic_result.patterns)}")
    for pattern in symbolic_result.patterns:
        print(f"     - {pattern.pattern_type}: {pattern.strength:.3f} (keywords: {len(pattern.matched_keywords)})")
    print()

    # Test 5: Therapeutic shift (crisis→restorative)
    print("5️⃣ Testing THERAPEUTIC SHIFT (Crisis → Restorative):")
    print("="*70)

    input_crisis = "I'm in crisis, overwhelmed and desperate. Everything feels unbearable."
    input_occasions = [MockTextOccasion(word) for word in input_crisis.split()]
    input_result = rnx.process_text_occasions(input_occasions, cycle=0)

    output_restorative = "I feel more grounded now. I'm finding hope and healing, learning to cope better."
    output_occasions = [MockTextOccasion(word) for word in output_restorative.split()]
    output_result = rnx.process_text_occasions(output_occasions, cycle=0)

    print(f"   INPUT:  {input_result.temporal_state} (confidence: {input_result.state_confidence:.3f}, volatility: {input_result.volatility:.3f})")
    print(f"   OUTPUT: {output_result.temporal_state} (confidence: {output_result.state_confidence:.3f}, volatility: {output_result.volatility:.3f})")
    print()
    print(f"   Therapeutic Shift Detected:")
    print(f"     Temporal state: {input_result.temporal_state} → {output_result.temporal_state}")
    print(f"     Volatility reduction: {input_result.volatility:.3f} → {output_result.volatility:.3f} (Δ {output_result.volatility - input_result.volatility:+.3f})")
    print(f"     Rhythm stability: {input_result.rhythm_stability:.3f} → {output_result.rhythm_stability:.3f} (Δ {output_result.rhythm_stability - input_result.rhythm_stability:+.3f})")
    print()

    if input_result.temporal_state == 'crisis' and output_result.temporal_state in ['restorative', 'concrescent']:
        print("   ✅ THERAPEUTIC SHIFT VALIDATED: Crisis resolved to healing/stability")
    else:
        print(f"   ⚠️  Unexpected pattern: {input_result.temporal_state} → {output_result.temporal_state}")

    print()
    print("="*70)
    print("✅ RNX temporal detection test complete!")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_rnx_temporal_detection()
