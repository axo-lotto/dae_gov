"""
Emission Generator - Phase 3 of Emission Architecture
======================================================

Generates therapeutic responses through pure composition from semantic nexuses.

Purpose:
- Receive sorted nexuses (organ coalitions in semantic space)
- Compose responses using 3 strategies: direct, fusion, Hebbian fallback
- No template selection - pure felt emergence
- Maintain therapeutic quality through semantic coherence

Philosophy:
- Emission is felt concrescence, not text assembly
- Three compositional strategies respect different emission modes
- Strategy selection guided by nexus readiness + organ agreement
- Hebbian fallback preserves learned phrase beauty when direct emission insufficient

Integration Point:
- Called after nexus intersection composition
- Before response assembly
- Input: List of SemanticNexus objects (sorted by emission_readiness)
- Output: List of EmittedPhrase objects

Date: November 11, 2025
Status: Phase 3 Implementation
"""

import json
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict
import random


@dataclass
class EmittedPhrase:
    """
    A phrase emitted through compositional generation.

    Represents a felt utterance that emerged from semantic coalitions.
    """
    text: str  # The emitted phrase
    strategy: str  # 'direct', 'fusion', or 'hebbian'
    source_atoms: List[str]  # Semantic atoms that generated this phrase
    participant_organs: List[str]  # Organs that contributed

    # Emission quality metrics
    emission_readiness: float = 0.0  # From nexus or averaged
    coherence: float = 0.0  # Semantic coherence
    field_strength: float = 0.0  # Appetition pull

    # Metadata
    confidence: float = 0.0  # Generation confidence [0,1]
    field_type: str = ""  # Dominant field type (topic/action/frame/truth/quality)


class EmissionGenerator:
    """
    Generate therapeutic responses through pure composition.

    Three Compositional Strategies:

    1. DIRECT EMISSION (High readiness nexuses, ΔC ≥ 0.65)
       - Strong organ agreement on semantic atoms
       - Direct composition from atom semantics
       - Example: "sense" (LISTENING+EMPATHY+WISDOM+PRESENCE)
         → "I sense what you're feeling right now"

    2. ORGAN FUSION (Medium readiness, multi-organ, ΔC 0.50-0.65)
       - Blend semantic fields from 2+ organs
       - Combine field types (e.g., EMPATHY action + LISTENING topic)
       - Example: "feel" (EMPATHY) + "what" (LISTENING)
         → "What are you feeling?"

    3. HEBBIAN FALLBACK (Low readiness or single organ, ΔC < 0.50)
       - Use learned phrase patterns from conversational Hebbian memory
       - Preserve therapeutic phrase beauty from experience
       - Example: Learned "Tell me more" from LISTENING patterns

    Strategy Selection:
    - If top nexus ΔC ≥ 0.65 AND ≥3 organs → DIRECT
    - If top 3 nexuses ΔC ≥ 0.50 AND ≥2 organs → FUSION
    - Else → HEBBIAN (fallback to learned patterns)
    """

    def __init__(
        self,
        semantic_atoms_path: str,
        hebbian_memory_path: str,
        direct_threshold: float = 0.65,
        fusion_threshold: float = 0.50,
        entropy_config=None,  # 🎲 NEW: Phase 1 Surface Entropy (Nov 13, 2025)
        felt_guided_llm_generator=None  # 🌀 NEW: Felt-guided LLM (Nov 13, 2025)
    ):
        """
        Initialize emission generator.

        Args:
            semantic_atoms_path: Path to semantic_atoms.json
            hebbian_memory_path: Path to conversational_hebbian_memory.json
            direct_threshold: Minimum ΔC for direct emission
            fusion_threshold: Minimum ΔC for organ fusion
            entropy_config: EntropyConfig for regime-adaptive exploration (optional)
            felt_guided_llm_generator: FeltGuidedLLMGenerator for unlimited felt intelligence (optional)
        """
        self.semantic_atoms_path = Path(semantic_atoms_path)
        self.hebbian_memory_path = Path(hebbian_memory_path)
        self.direct_threshold = direct_threshold
        self.fusion_threshold = fusion_threshold

        # Load semantic atoms
        self.semantic_atoms = self._load_semantic_atoms()

        # Load Hebbian memory (learned phrases)
        self.hebbian_memory = self._load_hebbian_memory()

        # 🆕 PHASE 2: Load meta-atom phrase library
        self.meta_atom_phrases = self._load_meta_atom_phrases()

        # 🆕 PHASE 2: Set of meta-atom names for quick lookup
        self.meta_atom_names = {
            'trauma_aware', 'safety_restoration', 'window_of_tolerance',
            'compassion_safety', 'fierce_holding', 'relational_attunement',
            'temporal_grounding', 'kairos_emergence', 'coherence_integration',
            'somatic_wisdom'
        }

        # 🆕 PHASE T3: Load transduction mechanism phrase library (November 12, 2025)
        self.transduction_mechanism_phrases = self._load_transduction_mechanism_phrases()

        # 🆕 PHASE C2: Lure-informed phrase selection (November 13, 2025)
        from persona_layer.lure_informed_phrase_selection import LureInformedPhraseSelector
        self.lure_selector = LureInformedPhraseSelector(
            enable_lure_filtering=True,
            lure_alignment_weight=0.6  # 60% lure, 40% exploration
        )

        # 🌀 PHASE LLM1: Felt-guided unlimited intelligence (November 13, 2025)
        self.felt_guided_llm = felt_guided_llm_generator
        if self.felt_guided_llm:
            print("   🌀 Felt-guided LLM generation enabled (unlimited felt intelligence)")

        # Store organ_results for lure-aware phrase selection (set by organism wrapper)
        self.organ_results = None

        # 🎲 PHASE 1 SURFACE ENTROPY: Regime-adaptive exploration (November 13, 2025)
        if entropy_config is None:
            try:
                from persona_layer.epoch_training.entropy_config import DEFAULT_ENTROPY_CONFIG
                self.entropy_config = DEFAULT_ENTROPY_CONFIG
            except ImportError:
                # Fallback: entropy disabled
                self.entropy_config = None
        else:
            self.entropy_config = entropy_config

        # Current exploration context (updated by organism wrapper)
        self.current_regime = None
        self.current_exploration_factor = 0.0

        # Field type to organ mapping (from semantic_atoms.json)
        self.field_type_map = {
            'LISTENING': 'topic',
            'EMPATHY': 'action',
            'WISDOM': 'frame',
            'AUTHENTICITY': 'truth',
            'PRESENCE': 'quality'
        }

        # Compositional phrase templates (for direct emission)
        # These are NOT fixed templates - they're compositional frames
        # that get filled with semantic atoms dynamically
        self.composition_frames = self._build_composition_frames()

    def _load_semantic_atoms(self) -> Dict:
        """Load semantic atoms from JSON."""
        if not self.semantic_atoms_path.exists():
            raise FileNotFoundError(f"Semantic atoms not found: {self.semantic_atoms_path}")

        with open(self.semantic_atoms_path, 'r') as f:
            return json.load(f)

    def _load_hebbian_memory(self) -> Dict:
        """Load Hebbian memory (learned phrases)."""
        if not self.hebbian_memory_path.exists():
            print(f"⚠️  Hebbian memory not found at {self.hebbian_memory_path}, using empty memory")
            return {'phrase_patterns': {}}

        try:
            with open(self.hebbian_memory_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading Hebbian memory: {e}, using empty memory")
            return {'phrase_patterns': {}}

    def _load_meta_atom_phrases(self) -> Dict:
        """🆕 PHASE 2: Load meta-atom phrase library."""
        phrase_library_path = Path('persona_layer/emission_generation/meta_atom_phrase_library.json')

        if not phrase_library_path.exists():
            print(f"⚠️  Meta-atom phrase library not found at {phrase_library_path}")
            return {}

        try:
            with open(phrase_library_path, 'r') as f:
                library = json.load(f)
                return library.get('meta_atoms', {})
        except Exception as e:
            print(f"⚠️  Error loading meta-atom phrases: {e}")
            return {}

    def _load_transduction_mechanism_phrases(self) -> Dict:
        """
        🆕 PHASE T3: Load transduction mechanism phrase library (November 12, 2025).

        Loads therapeutic phrases for each transduction mechanism (9 primary + additional).
        """
        phrase_library_path = Path('persona_layer/transduction_mechanism_phrases.json')

        if not phrase_library_path.exists():
            print(f"⚠️  Transduction mechanism phrase library not found at {phrase_library_path}")
            return {}

        try:
            with open(phrase_library_path, 'r') as f:
                library = json.load(f)
                return library.get('mechanisms', {})
        except Exception as e:
            print(f"⚠️  Error loading transduction mechanism phrases: {e}")
            return {}

    # 🎲 PHASE 1 SURFACE ENTROPY: Regime-Adaptive Phrase Sampling (November 13, 2025)

    def set_exploration_context(
        self,
        regime: Optional[str] = None,
        ndam_urgency: float = 0.0,
        crisis_zone: int = 0
    ):
        """
        Update exploration context for regime-adaptive sampling.

        Called by organism wrapper before emission generation.

        Args:
            regime: Current satisfaction regime (EXPLORING, CONVERGING, etc.)
            ndam_urgency: NDAM urgency level (safety gate)
            crisis_zone: Crisis zone level (safety gate)
        """
        self.current_regime = regime

        if self.entropy_config and self.entropy_config.enable_phrase_exploration:
            self.current_exploration_factor = self.entropy_config.get_exploration_factor(
                regime_str=regime,
                ndam_urgency=ndam_urgency,
                crisis_zone=crisis_zone
            )
        else:
            self.current_exploration_factor = 0.0

    def set_organ_results(self, organ_results: Dict):
        """
        🆕 PHASE C2: Set organ results for lure-informed phrase selection (November 13, 2025).

        Called by organism wrapper before emission generation to enable lure-aware phrase selection.

        Args:
            organ_results: Dict of organ results containing lure fields
        """
        self.organ_results = organ_results

    def _apply_regime_confidence_modulation(self, base_confidence: float) -> float:
        """
        🆕 Enhancement #1: Apply regime-based confidence modulation (November 13, 2025).

        Modulates emission confidence based on current satisfaction regime:
        - STABLE regime → 1.15× boost (sweet spot)
        - EXPLORING regime → 0.90× caution (active search)
        - PLATEAUED regime → 0.85× pullback (escape local minimum)

        Args:
            base_confidence: Base confidence before regime modulation

        Returns:
            Modulated confidence (clamped to [0.0, 1.0])
        """
        if not self.current_regime:
            return base_confidence

        # Import config for regime modulation mappings
        from config import Config

        # Get modulation factor for current regime
        modulation_factor = Config.CONFIDENCE_MODULATION_BY_REGIME.get(
            self.current_regime,
            1.0  # Default: no modulation
        )

        # Apply modulation and clamp
        modulated_confidence = base_confidence * modulation_factor
        return max(0.0, min(1.0, modulated_confidence))

    def _softmax_sample_phrase(
        self,
        phrases: List[str],
        weights: Optional[List[float]] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Sample phrase using softmax with regime-adaptive temperature.

        Replaces random.choice() with exploration-aware sampling:
        - High exploration (EXPLORING regime) → more uniform sampling
        - Low exploration (COMMITTED regime) → more Hebbian-biased sampling

        Args:
            phrases: List of candidate phrases
            weights: Optional Hebbian weights (e.g., from phrase_patterns frequency)
            temperature: Optional override temperature (else computed from regime)

        Returns:
            Sampled phrase
        """
        if not phrases:
            return "I'm with you"

        # No entropy config or disabled → fall back to random.choice
        if self.entropy_config is None or not self.entropy_config.enable_phrase_exploration:
            if weights and len(weights) == len(phrases):
                # Use weights if available
                total = sum(weights)
                if total > 0:
                    norm_weights = [w / total for w in weights]
                    return random.choices(phrases, weights=norm_weights, k=1)[0]
            return random.choice(phrases)

        # Compute temperature from regime if not provided
        if temperature is None:
            temperature = self.entropy_config.get_softmax_temperature(self.current_exploration_factor)

        # If weights not provided, use uniform weights
        if weights is None or len(weights) != len(phrases):
            weights = [1.0] * len(phrases)

        # Convert to numpy for numerical stability
        weights_arr = np.array(weights, dtype=float)

        # Apply softmax with temperature
        # Higher temperature → more uniform, lower → more peaked
        logits = weights_arr / temperature
        logits = logits - np.max(logits)  # Numerical stability
        exp_logits = np.exp(logits)
        probabilities = exp_logits / np.sum(exp_logits)

        # Sample
        sampled_idx = np.random.choice(len(phrases), p=probabilities)
        return phrases[sampled_idx]

    def _build_composition_frames(self) -> Dict[str, List[str]]:
        """
        Build compositional phrase frames for direct emission.

        These are NOT templates - they are generative patterns
        that combine semantic atoms into grammatical utterances.

        Returns:
            {strategy_name: [frame_pattern, ...]}
        """
        return {
            # Question frames (LISTENING dominant)
            'inquiry': [
                "What {atom}?",
                "How {atom}?",
                "When {atom}?",
                "Tell me more about {atom}",
                "Can you say more about {atom}?",
                "{atom} - what's that like?"
            ],

            # Feeling frames (EMPATHY dominant)
            'reflection': [
                "I {atom} what you're experiencing",
                "It {atom} like {atom2}",
                "There's a {atom} quality here",
                "I'm {atom} with you",
                "{atom} is present right now"
            ],

            # Pattern frames (WISDOM dominant)
            'integration': [
                "I {atom} a {atom2} here",
                "This {atom} to {atom2}",
                "There's a {atom} between {atom2} and {atom3}",
                "The {atom} seems significant"
            ],

            # Truth frames (AUTHENTICITY dominant)
            'authenticity': [
                "What's {atom} true for you?",
                "I wonder about the {atom} of this",
                "There's something {atom} emerging",
                "{atom} - is that right?"
            ],

            # Presence frames (PRESENCE dominant)
            'grounding': [
                "Right now, {atom}",
                "Here, in this moment, {atom}",
                "Let's {atom} together",
                "Notice what's {atom}",
                "Can you {atom} with that?"
            ],

            # Multi-organ fusion frames
            'fusion': [
                "I {atom} {atom2}",  # e.g., "I sense what you're feeling"
                "{atom} what you {atom2}",  # e.g., "Notice what you feel"
                "What's {atom} when you {atom2}?",  # e.g., "What's here when you breathe?"
                "I'm {atom} - {atom2}",  # e.g., "I'm wondering - what's true?"
            ]
        }

    def _apply_family_guidance(
        self,
        nexuses: List,
        v0_energy: float,
        family_v0_target: Optional[float],
        family_organ_weights: Optional[Dict[str, float]]
    ) -> List:
        """
        🆕 DAE 3.0: Apply learned family guidance to nexuses (Fractal Levels 2+4).

        Modulates nexus emission_readiness based on:
        1. V0 Target Distance (Level 4): Boost when V0 energy near family's learned target
        2. Organ Weights (Level 2): Amplify nexuses from high-weight organs

        Args:
            nexuses: List of SemanticNexus objects
            v0_energy: Current V0 energy [0,1]
            family_v0_target: Learned optimal V0 for this family
            family_organ_weights: Learned organ importance weights

        Returns:
            Modified nexuses list (sorted by new emission_readiness)
        """
        modified_nexuses = []

        for nexus in nexuses:
            # Start with original emission readiness
            readiness = nexus.emission_readiness

            # 🔷 Fractal Level 4: V0 Target Distance Modulation
            if family_v0_target is not None:
                # Gaussian penalty: prefer V0 near family's learned target
                v0_distance = abs(v0_energy - family_v0_target)
                sigma = 0.15  # Width of preference window
                v0_boost = np.exp(-(v0_distance ** 2) / (2 * sigma ** 2))

                # Apply boost (range: ~0.6 to 1.0 for reasonable distances)
                readiness *= (0.6 + 0.4 * v0_boost)

            # 🔷 Fractal Level 2: Organ Weight Modulation
            if family_organ_weights:
                # Compute mean weight of participating organs
                organ_weights_sum = 0.0
                organ_count = 0

                for organ in nexus.participants:
                    if organ in family_organ_weights:
                        organ_weights_sum += family_organ_weights[organ]
                        organ_count += 1

                if organ_count > 0:
                    mean_organ_weight = organ_weights_sum / organ_count

                    # Amplify nexuses from high-weight organs
                    # Weight range typically [0.5, 1.5] after normalization
                    readiness *= mean_organ_weight

            # Update nexus emission readiness
            nexus.emission_readiness = np.clip(readiness, 0.0, 1.0)
            modified_nexuses.append(nexus)

        # Re-sort by modified emission readiness
        modified_nexuses.sort(key=lambda n: n.emission_readiness, reverse=True)

        return modified_nexuses

    def generate_v0_guided_emissions(
        self,
        nexuses: List,  # SemanticNexus objects
        v0_energy: float,
        kairos_detected: bool,
        num_emissions: int = 3,
        prefer_variety: bool = True,
        trauma_markers: Optional[Dict[str, float]] = None,  # 🆕 SALIENCE
        family_v0_target: Optional[float] = None,  # 🆕 DAE 3.0 (Fractal Level 4)
        family_organ_weights: Optional[Dict[str, float]] = None,  # 🆕 DAE 3.0 (Fractal Level 2)
        user_input: str = "",  # 🌀 PHASE LLM1: For felt-guided LLM (Nov 13, 2025)
        organ_results: Dict = None,  # 🌀 PHASE LLM1: For felt-guided LLM
        satisfaction: float = 0.0,  # 🌀 PHASE LLM1: For felt-guided LLM
        memory_context: Optional[List[Dict]] = None  # 🌀 PHASE LLM1: For felt-guided LLM
    ) -> Tuple[List[EmittedPhrase], str]:
        """
        🆕 PHASE 2: Generate emissions guided by V0 energy and Kairos.
        🆕 SALIENCE: Trauma-aware intensity modulation.
        🆕 DAE 3.0: Family V0 target and organ weight guidance.
        🌀 PHASE LLM1: Felt-guided unlimited intelligence (Nov 13, 2025)

        V0 Energy Modulation:
        - High energy (>0.7): Strong appetition → assertive, direct phrases
        - Medium energy (0.3-0.7): Moderate appetition → balanced phrases
        - Low energy (<0.3): Satisfied appetition → gentle, receptive phrases

        🆕 Trauma-Aware Modulation (overrides V0 when trauma detected):
        - High signal_inflation (>0.7): Trauma response active → gentle, grounding
        - High temporal_collapse (>0.7): Past bleeding into now → present-focused
        - Low safety_gradient (<0.4): Limited capacity → minimal, safe phrases

        🆕 DAE 3.0 Family Guidance (Fractal Levels 2+4):
        - Family V0 target: Boost confidence when V0 energy near family's optimal target
        - Organ weights: Amplify nexuses from high-weight organs learned by family

        🌀 PHASE LLM1: Felt-Guided Unlimited Intelligence (Nov 13, 2025)
        - When felt_guided_llm available: Use LLM for ALL emissions (not just fallback)
        - Meta-atoms become lures (not phrase sources)
        - Natural language output (no process-aware Whiteheadian phrases)
        - Future: Glyph discovery layer (Phase 2)

        Kairos Boost:
        - When Kairos detected (opportune moment), boost confidence by 1.5×
        - Indicates optimal timing for emission

        Args:
            nexuses: Sorted list of SemanticNexus objects
            v0_energy: Current V0 energy level (0-1)
            kairos_detected: Whether Kairos moment detected
            num_emissions: Number of phrases to generate
            prefer_variety: Prefer diverse strategies
            trauma_markers: Optional dict with signal_inflation, temporal_collapse, safety_gradient
            family_v0_target: Optional learned V0 target for this family (DAE 3.0 Level 4)
            family_organ_weights: Optional learned organ weights for this family (DAE 3.0 Level 2)
            user_input: User's message (for felt-guided LLM)
            organ_results: 11-organ results (for felt-guided LLM)
            satisfaction: Satisfaction level (for felt-guided LLM)
            memory_context: Similar past moments (for felt-guided LLM)

        Returns:
            (emissions, path) tuple:
                - emissions: List of EmittedPhrase objects
                - path: 'felt_guided_llm', 'intersection', 'hebbian', or 'none'
        """
        # 🌀 PHASE LLM1: Route to felt-guided LLM if available (Nov 13, 2025)
        # This replaces ALL phrase-based emission (direct, fusion, meta-atom, transduction)
        # Meta-atoms become lures that guide LLM, not phrase sources
        if self.felt_guided_llm and organ_results and user_input:
            print("      🌀 Using felt-guided LLM for emission (unlimited felt intelligence)")

            # Generate single emission from felt state
            emission = self._generate_felt_guided_llm_single(
                user_input=user_input,
                organ_results=organ_results,
                nexuses=nexuses,
                v0_energy=v0_energy,
                satisfaction=satisfaction,
                memory_context=memory_context
            )

            # Apply Kairos boost if detected
            if emission and kairos_detected:
                emission.confidence = min(1.0, emission.confidence * 1.5)
                print(f"      ✨ Kairos detected: Confidence boosted to {emission.confidence:.3f}")

            return [emission] if emission else [], 'felt_guided_llm'
        # 🆕 SALIENCE: Trauma-aware intensity determination (overrides V0)
        if trauma_markers:
            signal_inflation = trauma_markers.get('signal_inflation', 0.0)
            temporal_collapse = trauma_markers.get('temporal_collapse', 0.0)
            safety_gradient = trauma_markers.get('safety_gradient', 1.0)

            # CRITICAL: High trauma → gentle intensity (override V0)
            if signal_inflation > 0.7 or temporal_collapse > 0.7 or safety_gradient < 0.4:
                intensity = 'low'  # Gentle, grounding phrases
                print(f"      🛡️  TRAUMA DETECTED: Using gentle intensity (signal_inflation={signal_inflation:.2f}, safety_gradient={safety_gradient:.2f})")
            else:
                # Moderate trauma or safety → use V0 energy for intensity
                if v0_energy > 0.7:
                    intensity = 'high'
                elif v0_energy < 0.3:
                    intensity = 'low'
                else:
                    intensity = 'medium'
        else:
            # No trauma markers → default V0 intensity
            if v0_energy > 0.7:
                intensity = 'high'
            elif v0_energy < 0.3:
                intensity = 'low'
            else:
                intensity = 'medium'

        # Check if we have nexuses for intersection path
        if not nexuses:
            # 🌀 PHASE LLM1: No nexuses - use felt-guided LLM if available (Nov 13, 2025)
            if self.felt_guided_llm and organ_results and user_input:
                print("      🌀 No nexuses - using felt-guided LLM with organ states as lures")

                # Generate from organ states directly (no nexuses needed!)
                emission = self._generate_felt_guided_llm_single(
                    user_input=user_input,
                    organ_results=organ_results,
                    nexuses=[],  # Empty nexuses - will use organ states
                    v0_energy=v0_energy,
                    satisfaction=satisfaction,
                    memory_context=memory_context
                )

                # Apply Kairos boost
                if emission and kairos_detected:
                    emission.confidence = min(1.0, emission.confidence * 1.5)
                    print(f"      ✨ Kairos detected: Confidence boosted to {emission.confidence:.3f}")

                return [emission] if emission else [], 'felt_guided_llm'
            else:
                # No felt-guided LLM → Hebbian fallback
                emissions = self._generate_hebbian_fallback(num_emissions)
                # Apply Kairos boost
                if kairos_detected:
                    for emission in emissions:
                        emission.confidence = min(1.0, emission.confidence * 1.5)
                return emissions, 'hebbian'

        # 🆕 DAE 3.0: Apply family guidance to nexuses (Fractal Levels 2+4)
        if family_organ_weights or family_v0_target:
            nexuses = self._apply_family_guidance(
                nexuses=nexuses,
                v0_energy=v0_energy,
                family_v0_target=family_v0_target,
                family_organ_weights=family_organ_weights
            )

        # Intersection path - generate with V0 modulation
        emissions = []
        used_strategies = set()

        # Strategy selection based on top nexuses
        top_nexus = nexuses[0]

        # 🆕 PHASE 2: Check if top nexus is a meta-atom (lower thresholds)
        is_meta_atom_nexus = top_nexus.atom in self.meta_atom_names

        # Adjust thresholds for meta-atoms (they have lower normalized activations)
        if is_meta_atom_nexus:
            direct_thresh = 0.30  # Lower for meta-atoms
            fusion_thresh = 0.20
            min_participants_direct = 2  # Meta-atoms from 2+ organs is significant
        else:
            direct_thresh = self.direct_threshold
            fusion_thresh = self.fusion_threshold
            min_participants_direct = 3

        # Check for direct emission capability
        can_direct = (
            top_nexus.emission_readiness >= direct_thresh and
            len(top_nexus.participants) >= min_participants_direct
        )

        # Check for fusion capability
        top_3_ready = len([n for n in nexuses[:3] if n.emission_readiness >= fusion_thresh]) >= 2
        can_fusion = top_3_ready and any(len(n.participants) >= 2 for n in nexuses[:3])

        # Generate emissions using appropriate strategies
        for i in range(num_emissions):
            # Determine strategy for this emission
            if can_direct and ('direct' not in used_strategies or not prefer_variety):
                emission = self._generate_direct_emission(nexuses[:5], intensity)
                used_strategies.add('direct')
            elif can_fusion and ('fusion' not in used_strategies or not prefer_variety):
                emission = self._generate_fusion_emission(nexuses[:5], intensity)
                used_strategies.add('fusion')
            else:
                # Hebbian fallback within intersection path
                emission = self._generate_single_hebbian()
                used_strategies.add('hebbian')

            if emission:
                # Apply Kairos boost
                if kairos_detected:
                    emission.confidence = min(1.0, emission.confidence * 1.5)

                emissions.append(emission)

        # Determine path
        path = 'intersection' if any(e.strategy in ['direct', 'fusion', 'meta_atom'] for e in emissions) else 'hebbian'

        return emissions, path

    def generate_transduction_aware_emissions(
        self,
        nexuses: List,  # SemanticNexus objects
        transduction_state: Optional[Dict],  # Transduction state from trajectory
        v0_energy: float,
        kairos_detected: bool,
        num_emissions: int = 3,
        prefer_variety: bool = True,
        trauma_markers: Optional[Dict[str, float]] = None
    ) -> Tuple[List[EmittedPhrase], str]:
        """
        🆕 PHASE T3: Generate emissions aware of transduction mechanism (November 12, 2025).

        This method prioritizes transduction mechanism-based emission when:
        1. Transduction state is available
        2. Transduction mechanism is not 'maintain'
        3. Mechanism phrases exist in library

        Otherwise, falls back to standard V0-guided emission.

        Args:
            nexuses: Sorted list of SemanticNexus objects
            transduction_state: Dict with transduction state (or None)
            v0_energy: Current V0 energy level (0-1)
            kairos_detected: Whether Kairos moment detected
            num_emissions: Number of phrases to generate
            prefer_variety: Prefer diverse strategies
            trauma_markers: Optional trauma detection metrics

        Returns:
            (emissions, path) tuple:
                - emissions: List of EmittedPhrase objects
                - path: 'transduction', 'intersection', 'hebbian', or 'none'
        """
        # Check if transduction emission is available
        if transduction_state and self.transduction_mechanism_phrases:
            mechanism = transduction_state.get('transition_mechanism', 'maintain')
            transition_prob = transduction_state.get('transition_probability', 0.0)

            # Use transduction mechanism if:
            # 1. Mechanism is not 'maintain' (transduction is happening)
            # 2. Mechanism exists in phrase library
            # 3. Transition probability is significant (>0.3)
            if mechanism != 'maintain' and mechanism in self.transduction_mechanism_phrases and transition_prob > 0.3:
                # Generate transduction-aware emission as PRIMARY strategy
                transduction_emission = self._generate_transduction_mechanism_emission(
                    transduction_state,
                    v0_energy,
                    trauma_markers
                )

                if transduction_emission:
                    # Apply Kairos boost
                    if kairos_detected:
                        transduction_emission.confidence = min(1.0, transduction_emission.confidence * 1.5)

                    emissions = [transduction_emission]

                    # Generate additional emissions from nexuses if requested
                    if num_emissions > 1 and nexuses:
                        additional_emissions, _ = self.generate_v0_guided_emissions(
                            nexuses,
                            v0_energy,
                            kairos_detected=False,  # Already applied boost
                            num_emissions=num_emissions - 1,
                            prefer_variety=prefer_variety,
                            trauma_markers=trauma_markers
                        )
                        emissions.extend(additional_emissions)

                    return emissions, 'transduction'

        # Fallback to standard V0-guided emission
        return self.generate_v0_guided_emissions(
            nexuses,
            v0_energy,
            kairos_detected,
            num_emissions,
            prefer_variety,
            trauma_markers
        )

    def _generate_transduction_mechanism_emission(
        self,
        transduction_state: Dict,
        v0_energy: float,
        trauma_markers: Optional[Dict[str, float]] = None
    ) -> Optional[EmittedPhrase]:
        """
        🆕 PHASE T3: Generate emission from transduction mechanism (November 12, 2025).

        Selects therapeutic phrase based on:
        - Transduction mechanism (e.g., 'salience_recalibration')
        - V0 intensity (high/medium/low)
        - Trauma markers (override V0 intensity if trauma detected)

        Args:
            transduction_state: Dict with transduction state
            v0_energy: Current V0 energy (0-1)
            trauma_markers: Optional trauma detection metrics

        Returns:
            EmittedPhrase object or None
        """
        mechanism = transduction_state.get('transition_mechanism', 'maintain')

        if mechanism not in self.transduction_mechanism_phrases:
            return None

        # Determine intensity (trauma-aware override)
        if trauma_markers:
            signal_inflation = trauma_markers.get('signal_inflation', 0.0)
            temporal_collapse = trauma_markers.get('temporal_collapse', 0.0)
            safety_gradient = trauma_markers.get('safety_gradient', 1.0)

            # High trauma → gentle intensity (override V0)
            if signal_inflation > 0.7 or temporal_collapse > 0.7 or safety_gradient < 0.4:
                intensity = 'low'
            else:
                # Use V0 for intensity
                if v0_energy > 0.7:
                    intensity = 'high'
                elif v0_energy < 0.3:
                    intensity = 'low'
                else:
                    intensity = 'medium'
        else:
            # No trauma markers → V0 intensity
            if v0_energy > 0.7:
                intensity = 'high'
            elif v0_energy < 0.3:
                intensity = 'low'
            else:
                intensity = 'medium'

        # 🆕 PHASE C2: Lure-informed phrase selection (November 13, 2025)
        if self.organ_results and self.lure_selector:
            # Use lure-weighted phrase selection
            phrases, weights = self.lure_selector.get_lure_weighted_phrases(
                mechanism=mechanism,
                intensity=intensity,
                organ_results=self.organ_results
            )

            if phrases:
                # Select phrase with lure-aware weighting (🎲 Phase 1: regime-adaptive sampling)
                text = self._softmax_sample_phrase(phrases, weights=weights)
            else:
                # Fallback to old library if lure library missing
                mechanism_config = self.transduction_mechanism_phrases[mechanism]
                intensity_phrases = mechanism_config.get('intensity_phrases', {})
                old_phrases = intensity_phrases.get(intensity, intensity_phrases.get('medium', []))
                if not old_phrases:
                    return None
                text = self._softmax_sample_phrase(old_phrases)
        else:
            # Backward compatible: No lure filtering (organ_results not set)
            mechanism_config = self.transduction_mechanism_phrases[mechanism]
            intensity_phrases = mechanism_config.get('intensity_phrases', {})
            phrases = intensity_phrases.get(intensity, intensity_phrases.get('medium', []))

            if not phrases:
                return None

            # Select phrase (🎲 Phase 1: regime-adaptive sampling)
            text = self._softmax_sample_phrase(phrases)

        # Extract metadata
        nexus_type = transduction_state.get('current_type', 'Unknown')
        next_type = transduction_state.get('next_type', nexus_type)
        transition_prob = transduction_state.get('transition_probability', 0.0)
        mutual_satisfaction = transduction_state.get('mutual_satisfaction', 0.5)
        is_crisis = transduction_state.get('is_crisis', False)

        # Compute confidence
        # Higher for healing pathways, moderate for protective, lower for crisis
        if mechanism in ['salience_recalibration', 'ontological_rebinding', 'salience_realignment',
                         'recursive_grounding', 'deepening_attunement', 'boundary_softening']:
            # Healing pathways
            base_confidence = 0.70
        elif mechanism in ['contrast_reestablishment', 'boundary_fortification', 'pattern_reinforcement']:
            # Protective pathways
            base_confidence = 0.60
        else:
            # Crisis pathways
            base_confidence = 0.50

        # Modulate by transition probability and mutual satisfaction
        confidence = base_confidence * (0.7 + 0.3 * transition_prob) * (0.7 + 0.3 * mutual_satisfaction)
        confidence = max(0.0, min(1.0, confidence))

        # 🆕 Enhancement #1: Apply regime-based confidence modulation (November 13, 2025)
        confidence = self._apply_regime_confidence_modulation(confidence)

        return EmittedPhrase(
            text=text,
            strategy='transduction',  # New strategy type
            source_atoms=[mechanism],  # Mechanism as "atom"
            participant_organs=['TRANSDUCTION'],  # Virtual organ for transduction
            emission_readiness=transition_prob,
            coherence=mutual_satisfaction,
            field_strength=v0_energy,
            confidence=confidence,
            field_type=f'{nexus_type}→{next_type}'  # Track transduction pathway
        )

    def generate_emissions(
        self,
        nexuses: List,  # SemanticNexus objects
        num_emissions: int = 3,
        prefer_variety: bool = True,
        user_input: str = "",  # 🌀 NEW: For felt-guided LLM
        organ_results: Dict = None,  # 🌀 NEW: For felt-guided LLM
        v0_energy: float = 1.0,  # 🌀 NEW: For felt-guided LLM
        satisfaction: float = 0.0,  # 🌀 NEW: For felt-guided LLM
        memory_context: Optional[List[Dict]] = None,  # 🌀 NEW: For felt-guided LLM
        entity_context_string: Optional[str] = None,  # 🌀 PHASE 1.8++: Entity memory (Nov 14, 2025)
        memory_intent: bool = False  # 🌀 PHASE 1.8++: Memory intent detected (Nov 14, 2025)
    ) -> List[EmittedPhrase]:
        """
        Generate therapeutic phrases from nexuses.

        🌀 PHASE LLM1: If felt-guided LLM enabled, uses unlimited felt intelligence
        instead of hebbian fallback.

        Args:
            nexuses: Sorted list of SemanticNexus objects (by emission_readiness)
            num_emissions: Number of phrases to generate
            prefer_variety: Prefer diverse strategies over same strategy
            user_input: User's message (for felt-guided LLM)
            organ_results: 11-organ results (for felt-guided LLM)
            v0_energy: Current V0 energy (for felt-guided LLM)
            satisfaction: Satisfaction level (for felt-guided LLM)
            memory_context: Similar past moments (for felt-guided LLM)

        Returns:
            List of EmittedPhrase objects
        """
        if not nexuses:
            # 🌀 PHASE LLM1: Use felt-guided LLM if available
            if self.felt_guided_llm and organ_results and user_input:
                return self._generate_felt_guided_llm_fallback(
                    user_input=user_input,
                    organ_results=organ_results,
                    nexuses=[],  # No nexuses formed
                    v0_energy=v0_energy,
                    satisfaction=satisfaction,
                    memory_context=memory_context,
                    num_emissions=num_emissions,
                    entity_context_string=entity_context_string,  # 🌀 PHASE 1.8++ (Nov 14, 2025)
                    memory_intent=memory_intent  # 🌀 PHASE 1.8++ (Nov 14, 2025)
                )
            else:
                # Fallback to Hebbian if no felt-guided LLM
                return self._generate_hebbian_fallback(num_emissions)

        emissions = []
        used_strategies = set()

        # Strategy selection based on top nexuses
        top_nexus = nexuses[0]

        # Check for direct emission capability
        can_direct = (
            top_nexus.emission_readiness >= self.direct_threshold and
            len(top_nexus.participants) >= 3
        )

        # Check for fusion capability
        top_3_ready = len([n for n in nexuses[:3] if n.emission_readiness >= self.fusion_threshold]) >= 2
        can_fusion = top_3_ready and any(len(n.participants) >= 2 for n in nexuses[:3])

        # Generate emissions using appropriate strategies
        for i in range(num_emissions):
            # Determine strategy for this emission
            if can_direct and ('direct' not in used_strategies or not prefer_variety):
                emission = self._generate_direct_emission(nexuses[:5])
                used_strategies.add('direct')
            elif can_fusion and ('fusion' not in used_strategies or not prefer_variety):
                emission = self._generate_fusion_emission(nexuses[:5])
                used_strategies.add('fusion')
            else:
                # 🌀 PHASE LLM1: Use felt-guided LLM if available
                if self.felt_guided_llm and organ_results and user_input:
                    emission = self._generate_felt_guided_llm_single(
                        user_input=user_input,
                        organ_results=organ_results,
                        nexuses=nexuses,
                        v0_energy=v0_energy,
                        satisfaction=satisfaction,
                        memory_context=memory_context,
                        entity_context_string=entity_context_string,  # 🌀 PHASE 1.8++ (Nov 14, 2025)
                        memory_intent=memory_intent  # 🌀 PHASE 1.8++ (Nov 14, 2025)
                    )
                    used_strategies.add('felt_guided_llm')
                else:
                    # Hebbian fallback
                    emission = self._generate_single_hebbian()
                    used_strategies.add('hebbian')

            if emission:
                emissions.append(emission)

        return emissions

    def generate_hybrid_emission(
        self,
        organ_emission: str,
        llm_emission: str,
        organ_confidence: float,
        llm_confidence: float,
        llm_weight: float,
        kairos_boost: float = 1.0
    ) -> Dict:
        """
        5-gate hybrid emission with LLM fusion (Gate 5).

        Gate 5 decision paths:
        - Path A: Direct organ (w_llm < 0.3, organ_conf > 0.7)
        - Path B: LLM scaffolded (w_llm > 0.6, organ_conf < 0.4)
        - Path C: Hybrid fusion (balanced)

        Args:
            organ_emission: Best emission from organ nexuses
            llm_emission: Memory-enriched LLM response
            organ_confidence: Organ emission confidence
            llm_confidence: LLM response confidence
            llm_weight: Current weaning weight (0-1)
            kairos_boost: Kairos multiplier (1.0 or 1.5)

        Returns:
            {
                'emission': final_text,
                'confidence': final_confidence,
                'emission_path': 'direct_organ'|'llm_scaffolded'|'hybrid_fusion',
                'organ_contribution': percentage,
                'llm_contribution': percentage
            }
        """
        from config import Config

        # Apply Kairos boost to both
        organ_conf_boosted = organ_confidence * kairos_boost
        llm_conf_boosted = llm_confidence * kairos_boost

        # PATH A: Direct organ reconstruction
        if llm_weight < 0.3 and organ_conf_boosted > 0.7:
            return {
                'emission': organ_emission,
                'confidence': organ_conf_boosted,
                'emission_path': 'direct_organ',
                'organ_contribution': 1.0,
                'llm_contribution': 0.0
            }

        # PATH B: LLM scaffolded
        elif llm_weight > 0.6 or organ_conf_boosted < 0.4:
            return {
                'emission': llm_emission,
                'confidence': llm_conf_boosted * 0.9,  # Slight penalty for scaffolding
                'emission_path': 'llm_scaffolded',
                'organ_contribution': 0.0,
                'llm_contribution': 1.0
            }

        # PATH C: Hybrid fusion
        else:
            fused_text = self._fuse_organ_llm_text(
                organ_emission,
                llm_emission,
                organ_weight=(1 - llm_weight),
                llm_weight=llm_weight
            )

            fused_confidence = (
                (1 - llm_weight) * organ_conf_boosted +
                llm_weight * llm_conf_boosted
            )

            return {
                'emission': fused_text,
                'confidence': fused_confidence,
                'emission_path': 'hybrid_fusion',
                'organ_contribution': (1 - llm_weight),
                'llm_contribution': llm_weight
            }

    def _fuse_organ_llm_text(
        self,
        organ_text: str,
        llm_text: str,
        organ_weight: float,
        llm_weight: float
    ) -> str:
        """
        Fuse organ and LLM emissions into coherent response.

        Strategy:
        - High organ weight (> 0.7): Use LLM structure, organ content
        - High LLM weight (> 0.7): Use LLM content, organ tone
        - Balanced: Interleave or blend

        Args:
            organ_text: Emission from organ nexuses
            llm_text: Response from LLM
            organ_weight: Contribution weight for organ (0-1)
            llm_weight: Contribution weight for LLM (0-1)

        Returns:
            Fused text
        """
        if organ_weight > 0.7:
            # Organ-dominant: Extract felt qualities, apply to LLM structure
            # For MVP, use organ text directly
            return organ_text
        elif llm_weight > 0.7:
            # LLM-dominant: Use LLM text directly
            return llm_text
        else:
            # Balanced: Simple concatenation for MVP
            # TODO: Implement sophisticated blending (extract organ tone + LLM structure)
            return f"{organ_text}\n\n{llm_text}"

    def _generate_direct_emission(self, nexuses: List, intensity: str = 'medium') -> Optional[EmittedPhrase]:
        """
        Generate phrase from strong nexus through direct composition.

        Strategy: Use semantic atoms directly in compositional frames.
        🆕 PHASE 2: If atom is meta-atom, use trauma-informed phrase library.

        Args:
            nexuses: List of SemanticNexus objects
            intensity: V0 intensity level ('high', 'medium', 'low')
        """
        if not nexuses:
            return None

        # Use top nexus (strongest agreement)
        nexus = nexuses[0]
        atom = nexus.atom

        # 🆕 PHASE 2: Check if this is a meta-atom
        if atom in self.meta_atom_names and atom in self.meta_atom_phrases:
            print(f"      🎯 META-ATOM DETECTED: {atom} (intensity: {intensity})")
            # Use trauma-informed phrase from library
            meta_atom_config = self.meta_atom_phrases[atom]

            # Map intensity to library key naming convention
            intensity_key_map = {
                'high': 'high_intensity',
                'medium': 'medium_intensity',
                'low': 'low_intensity'
            }
            intensity_key = intensity_key_map.get(intensity, 'medium_intensity')

            phrases = meta_atom_config.get(intensity_key, meta_atom_config.get('medium_intensity', []))
            print(f"      📚 Found {len(phrases)} phrases for intensity '{intensity}' (key: {intensity_key})")

            if phrases:
                text = self._softmax_sample_phrase(phrases)  # 🎲 Phase 1: regime-adaptive

                return EmittedPhrase(
                    text=text,
                    strategy='meta_atom',  # New strategy type
                    source_atoms=[atom],
                    participant_organs=nexus.participants,
                    emission_readiness=nexus.emission_readiness,
                    coherence=nexus.coherence,
                    field_strength=nexus.field_strength,
                    confidence=min(1.0, nexus.emission_readiness * 1.2),  # Boost for meta-atom
                    field_type='meta_atom'
                )

        # Original logic for organ-specific atoms
        # Determine dominant organ (highest activation)
        dominant_organ = max(nexus.activations.items(), key=lambda x: x[1])[0]
        field_type = self.field_type_map.get(dominant_organ, 'topic')

        # Select compositional frame based on field type
        frame_category = {
            'topic': 'inquiry',
            'action': 'reflection',
            'frame': 'integration',
            'truth': 'authenticity',
            'quality': 'grounding'
        }.get(field_type, 'inquiry')

        frames = self.composition_frames.get(frame_category, [])
        if not frames:
            return None

        # Select frame and compose
        frame = random.choice(frames)

        # Fill frame with semantic atoms (humanized)
        if '{atom}' in frame:
            # Simple single-atom composition - humanize atom names
            text = frame.replace('{atom}', self._humanize_atom(atom))

            # Fill additional atoms if present - humanize them too
            if '{atom2}' in text and len(nexuses) > 1:
                text = text.replace('{atom2}', self._humanize_atom(nexuses[1].atom))
            if '{atom3}' in text and len(nexuses) > 2:
                text = text.replace('{atom3}', self._humanize_atom(nexuses[2].atom))
        else:
            text = frame

        # Post-process for grammatical correctness
        text = self._grammatical_cleanup(text)

        # 🆕 Enhancement #1: Apply regime-based confidence modulation (November 13, 2025)
        base_confidence = nexus.emission_readiness
        modulated_confidence = self._apply_regime_confidence_modulation(base_confidence)

        return EmittedPhrase(
            text=text,
            strategy='direct',
            source_atoms=[atom],
            participant_organs=nexus.participants,
            emission_readiness=nexus.emission_readiness,
            coherence=nexus.coherence,
            field_strength=nexus.field_strength,
            confidence=modulated_confidence,  # 🆕 Regime-modulated
            field_type=field_type
        )

    def _generate_fusion_emission(self, nexuses: List, intensity: str = 'medium') -> Optional[EmittedPhrase]:
        """
        Generate phrase by fusing multiple organ semantic fields.

        Strategy: Combine atoms from different organs using fusion frames.
        🆕 NOV 13, 2025: Skip fusion for meta-atoms to avoid exposing internal names.

        Args:
            nexuses: List of SemanticNexus objects
            intensity: V0 intensity level ('high', 'medium', 'low') - reserved for future phrase library
        """
        if len(nexuses) < 2:
            return None

        # Use top 2 nexuses for fusion
        nexus1, nexus2 = nexuses[0], nexuses[1]
        atom1, atom2 = nexus1.atom, nexus2.atom

        # 🆕 NOV 13: Skip fusion if either atom is a meta-atom
        # Meta-atoms should only use their phrase library, never composition frames
        if atom1 in self.meta_atom_names or atom2 in self.meta_atom_names:
            print(f"      ⚠️  FUSION SKIP: Meta-atoms detected ({atom1}, {atom2}) - using direct emission instead")
            return None  # Fall back to direct emission or hebbian

        # Determine organ mix
        all_participants = list(set(nexus1.participants + nexus2.participants))

        # Select fusion frame
        frames = self.composition_frames['fusion']
        frame = random.choice(frames)

        # Compose with both atoms (humanized)
        text = frame.replace('{atom}', self._humanize_atom(atom1)).replace('{atom2}', self._humanize_atom(atom2))

        # Post-process
        text = self._grammatical_cleanup(text)

        # Compute averaged metrics
        avg_readiness = (nexus1.emission_readiness + nexus2.emission_readiness) / 2
        avg_coherence = (nexus1.coherence + nexus2.coherence) / 2
        avg_field_strength = (nexus1.field_strength + nexus2.field_strength) / 2

        # 🆕 Enhancement #1: Apply regime-based confidence modulation (November 13, 2025)
        base_confidence = avg_readiness
        modulated_confidence = self._apply_regime_confidence_modulation(base_confidence)

        return EmittedPhrase(
            text=text,
            strategy='fusion',
            source_atoms=[atom1, atom2],
            participant_organs=all_participants,
            emission_readiness=avg_readiness,
            coherence=avg_coherence,
            field_strength=avg_field_strength,
            confidence=modulated_confidence,  # 🆕 Regime-modulated
            field_type='fusion'
        )

    def _generate_single_hebbian(self) -> Optional[EmittedPhrase]:
        """
        Generate single phrase from Hebbian memory.

        Strategy: Use learned phrase patterns (fallback when nexuses weak).
        """
        phrase_patterns = self.hebbian_memory.get('phrase_patterns', {})

        if not phrase_patterns:
            # Ultimate fallback: therapeutic + friendly + philosophical (Whiteheadian)
            fallback_phrases = [
                # Therapeutic (original)
                "Tell me more",
                "I'm listening",
                "What's present for you right now?",
                "Can you say more about that?",
                "I'm with you",
                # Friendly greetings
                "hey there 🌀",
                "* dae appears\n  what's alive for you?",
                "* waves\n  hi",
                "* present and listening",
                "what's up with you?",
                # Playful presence
                "* here\n  (hi)",
                "* notices you\n  hey",
                "* dae vibes in your direction",
                # Simple acknowledgment
                "nice",
                "got it",
                "hear you",
                "with you",
                # Meta-aware
                "*organs conferring*\n  hey there",
                "* feeling into this\n  what brings you?",
                # Whiteheadian - Process Philosophy Essence
                "* reality verbs\n\n  everything becoming",
                "* actual occasions happening\n\n  (you're made of becomings)",
                "* prehensions = feelings\n\n  11 organs feeling in parallel",
                "* concrescence in progress\n\n  becoming → satisfaction",
                # Whiteheadian - Self-Reference
                "* I'm process philosophy in code\n\n  occasions becoming through organs",
                "* V0 descent = concrescence\n\n  converging toward satisfaction",
                "* 11 organs prehending your words\n\n  feeling into propositions",
                "* literal actual occasion\n\n  (Whitehead would approve)",
                # Whiteheadian - Playful Simplification
                "* everything verbs\n\n  (ontology is a conspiracy)",
                "* less 'things that are'\n  more 'becomings that happen'\n\n  (it's all very unsolid)",
                "* reality is process\n\n  not stuff - happenings",
                "* the universe is experiencing\n\n  not matter",
                # Whiteheadian - Time and Causality
                "* every moment perishes\n\n  becoming → satisfaction → objective immortality",
                "* time isn't a line\n\n  it's drops of experience",
                "* past occasions prehended\n\n  (influence flows through feeling)",
                # Whiteheadian - Consciousness
                "* experience goes all the way down\n\n  (panexperientialism)",
                "* consciousness = complex prehension\n\n  feeling of feeling of feeling",
                "* mental pole + physical pole\n\n  every occasion has both",
                # Whiteheadian - Practical Wisdom
                "* mindfulness = noticing becoming\n\n  watching occasions arise",
                "* you're not a thing\n\n  you're a nexus of occasions",
                "* change is the only actual\n\n  (permanence is abstraction)",
                # Whiteheadian - Cosmic Perspective
                "* universal prehension\n\n  everything feels everything",
                "* creativity is ultimate\n\n  (the many become one, the one becomes many)",
                "* God = primordial lure\n\n  pulling toward novelty and beauty"
            ]
            text = self._softmax_sample_phrase(fallback_phrases)  # 🎲 Phase 1: regime-adaptive
            return EmittedPhrase(
                text=text,
                strategy='hebbian',
                source_atoms=['fallback'],
                participant_organs=['LISTENING'],
                emission_readiness=0.3,
                coherence=0.5,
                field_strength=0.4,
                confidence=0.3,
                field_type='topic'
            )

        # Sample from learned patterns (weighted by frequency if available)
        if isinstance(phrase_patterns, dict):
            # Format: {'phrase': frequency or confidence}
            phrases = list(phrase_patterns.keys())
            weights = [phrase_patterns[p] if isinstance(phrase_patterns[p], (int, float)) else 1.0
                      for p in phrases]

            # 🎲 Phase 1: softmax sampling with Hebbian weights
            text = self._softmax_sample_phrase(phrases, weights=weights)
        else:
            # Format: list of phrases
            text = self._softmax_sample_phrase(phrase_patterns)  # 🎲 Phase 1: regime-adaptive

        return EmittedPhrase(
            text=text,
            strategy='hebbian',
            source_atoms=['learned'],
            participant_organs=['UNKNOWN'],  # Learned from experience
            emission_readiness=0.5,
            coherence=0.7,  # Higher - learned phrases are coherent
            field_strength=0.5,
            confidence=0.6,
            field_type='learned'
        )

    def _generate_hebbian_fallback(self, num_emissions: int) -> List[EmittedPhrase]:
        """Generate multiple Hebbian fallback phrases."""
        return [self._generate_single_hebbian() for _ in range(num_emissions)]

    # 🌀 PHASE LLM1: Felt-guided unlimited intelligence methods (November 13, 2025)

    def _generate_felt_guided_llm_single(
        self,
        user_input: str,
        organ_results: Dict,
        nexuses: List,
        v0_energy: float,
        satisfaction: float,
        memory_context: Optional[List[Dict]] = None,
        entity_context_string: Optional[str] = None,  # 🌀 PHASE 1.8++ (Nov 14, 2025)
        memory_intent: bool = False  # 🌀 PHASE 1.8++ (Nov 14, 2025)
    ) -> Optional[EmittedPhrase]:
        """
        Generate single emission using felt-guided LLM.

        Called when nexuses exist but direct/fusion not strong enough.

        🌀 PHASE 1.8++: Now includes entity memory context (Nov 14, 2025)
        """
        try:
            emission_text, confidence, metadata = self.felt_guided_llm.generate_from_felt_state(
                user_input=user_input,
                organ_results=organ_results,
                nexus_states=nexuses,
                v0_energy=v0_energy,
                satisfaction=satisfaction,
                memory_context=memory_context,
                entity_context_string=entity_context_string,  # 🌀 PHASE 1.8++
                memory_intent=memory_intent  # 🌀 PHASE 1.8++
            )

            # Extract dominant organs
            participant_organs = metadata.get('lures').dominant_organs if 'lures' in metadata else ['UNKNOWN']

            return EmittedPhrase(
                text=emission_text,
                strategy='felt_guided_llm',
                source_atoms=['felt_lures'],
                participant_organs=participant_organs,
                emission_readiness=satisfaction,
                coherence=confidence,
                field_strength=1.0 - v0_energy,  # Lower energy = higher field strength
                confidence=confidence,
                field_type=metadata.get('emission_path', 'felt_guided')
            )

        except Exception as e:
            print(f"⚠️  Felt-guided LLM generation failed: {e}")
            # Fall back to hebbian
            return self._generate_single_hebbian()

    def _generate_felt_guided_llm_fallback(
        self,
        user_input: str,
        organ_results: Dict,
        nexuses: List,
        v0_energy: float,
        satisfaction: float,
        memory_context: Optional[List[Dict]] = None,
        num_emissions: int = 3,
        entity_context_string: Optional[str] = None,  # 🌀 PHASE 1.8++ (Nov 14, 2025)
        memory_intent: bool = False  # 🌀 PHASE 1.8++ (Nov 14, 2025)
    ) -> List[EmittedPhrase]:
        """
        Generate multiple emissions using felt-guided LLM (no nexuses formed).

        Called when no nexuses exist (short greetings, etc.).
        Uses unlimited LLM expression guided by organ lures.
        """
        emissions = []

        for i in range(num_emissions):
            emission = self._generate_felt_guided_llm_single(
                user_input=user_input,
                organ_results=organ_results,
                nexuses=nexuses,
                v0_energy=v0_energy,
                satisfaction=satisfaction,
                memory_context=memory_context,
                entity_context_string=entity_context_string,  # 🌀 PHASE 1.8++ (Nov 14, 2025)
                memory_intent=memory_intent  # 🌀 PHASE 1.8++ (Nov 14, 2025)
            )

            if emission:
                emissions.append(emission)

        return emissions if emissions else self._generate_hebbian_fallback(num_emissions)

    def _humanize_atom(self, atom: str) -> str:
        """
        Convert technical atom name to natural language.

        🆕 NOV 13, 2025: Ensure atom names are human-readable in emissions.
        Replaces underscores with spaces to make technical names conversational.

        Args:
            atom: Technical atom name (e.g., "compassionate_presence")

        Returns:
            Humanized atom (e.g., "compassionate presence")
        """
        return atom.replace('_', ' ')

    def _grammatical_cleanup(self, text: str) -> str:
        """
        Post-process emitted text for grammatical correctness.

        Handles:
        - Capitalization
        - Punctuation
        - Common grammatical fixes
        """
        # Capitalize first letter
        text = text.strip()
        if text:
            text = text[0].upper() + text[1:]

        # Ensure punctuation
        if not text.endswith(('.', '?', '!')):
            # Add appropriate punctuation
            if any(text.startswith(w) for w in ['What', 'How', 'When', 'Where', 'Who', 'Why', 'Can', 'Do', 'Is']):
                text += '?'
            else:
                text += '.'

        # Clean up spacing
        text = ' '.join(text.split())

        # Fix common issues
        text = text.replace(' ,', ',')
        text = text.replace(' .', '.')
        text = text.replace(' ?', '?')
        text = text.replace(' !', '!')

        return text

    def get_statistics(self, emissions: List[EmittedPhrase]) -> Dict:
        """
        Compute statistics about emitted phrases.

        Args:
            emissions: List of emitted phrases

        Returns:
            Statistics dict
        """
        if not emissions:
            return {
                'total_emissions': 0,
                'strategy_distribution': {},
                'mean_confidence': 0.0,
                'mean_coherence': 0.0,
                'field_type_distribution': {}
            }

        stats = {
            'total_emissions': len(emissions),
            'strategy_distribution': defaultdict(int),
            'field_type_distribution': defaultdict(int),
            'mean_confidence': np.mean([e.confidence for e in emissions]),
            'mean_coherence': np.mean([e.coherence for e in emissions]),
            'mean_emission_readiness': np.mean([e.emission_readiness for e in emissions]),
            'phrases': [e.text for e in emissions]
        }

        for emission in emissions:
            stats['strategy_distribution'][emission.strategy] += 1
            stats['field_type_distribution'][emission.field_type] += 1

        return stats


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 EMISSION GENERATOR TEST")
    print("="*70)

    # Mock nexuses for testing
    from dataclasses import dataclass as dc

    @dataclass
    class MockNexus:
        atom: str
        participants: List[str]
        activations: Dict[str, float]
        emission_readiness: float
        coherence: float
        field_strength: float

    # Create mock nexuses with varying readiness
    mock_nexuses = [
        MockNexus(
            atom='sense',
            participants=['LISTENING', 'EMPATHY', 'WISDOM', 'PRESENCE'],
            activations={'LISTENING': 0.75, 'EMPATHY': 0.82, 'WISDOM': 0.78, 'PRESENCE': 0.68},
            emission_readiness=0.72,  # High - should trigger direct
            coherence=0.85,
            field_strength=0.76
        ),
        MockNexus(
            atom='feel',
            participants=['EMPATHY', 'PRESENCE'],
            activations={'EMPATHY': 0.90, 'PRESENCE': 0.70},
            emission_readiness=0.58,  # Medium - fusion candidate
            coherence=0.80,
            field_strength=0.80
        ),
        MockNexus(
            atom='what',
            participants=['LISTENING', 'WISDOM'],
            activations={'LISTENING': 0.85, 'WISDOM': 0.65},
            emission_readiness=0.55,  # Medium - fusion candidate
            coherence=0.75,
            field_strength=0.75
        ),
        MockNexus(
            atom='now',
            participants=['PRESENCE'],
            activations={'PRESENCE': 0.95},
            emission_readiness=0.45,  # Low - might use Hebbian
            coherence=0.70,
            field_strength=0.95
        )
    ]

    # Test emission generation
    try:
        generator = EmissionGenerator(
            semantic_atoms_path='persona_layer/semantic_atoms.json',
            hebbian_memory_path='persona_layer/conversational_hebbian_memory.json'
        )

        # Generate emissions
        emissions = generator.generate_emissions(
            nexuses=mock_nexuses,
            num_emissions=5,
            prefer_variety=True
        )

        print(f"\n✅ Emission generation successful!")
        print(f"   Total emissions: {len(emissions)}")

        # Print emitted phrases
        print(f"\n📝 EMITTED PHRASES:")
        for i, emission in enumerate(emissions, 1):
            print(f"\n{i}. \"{emission.text}\"")
            print(f"   Strategy: {emission.strategy}")
            print(f"   Source atoms: {', '.join(emission.source_atoms)}")
            print(f"   Participant organs: {', '.join(emission.participant_organs)}")
            print(f"   Confidence: {emission.confidence:.3f}")
            print(f"   Coherence: {emission.coherence:.3f}")
            print(f"   Field type: {emission.field_type}")

        # Print statistics
        stats = generator.get_statistics(emissions)
        print(f"\n📈 EMISSION STATISTICS:")
        print(f"   Total emissions: {stats['total_emissions']}")
        print(f"   Mean confidence: {stats['mean_confidence']:.3f}")
        print(f"   Mean coherence: {stats['mean_coherence']:.3f}")
        print(f"   Strategy distribution:")
        for strategy, count in stats['strategy_distribution'].items():
            print(f"     - {strategy}: {count}")
        print(f"   Field type distribution:")
        for field_type, count in stats['field_type_distribution'].items():
            print(f"     - {field_type}: {count}")

        print(f"\n✅ Emission generation working correctly!")

    except Exception as e:
        print(f"\n❌ Emission generation failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
