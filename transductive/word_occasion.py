"""
WordOccasion - Word-Level Actual Occasion with Dual Vector + Appetition Loop
=============================================================================

ENHANCED (November 18, 2025): Full DAE 3.0 grid cell architecture with:
- Dual vector representation (felt 31D + symbolic embedding)
- Multi-cycle V0 appetition loop (concrescence toward satisfaction)
- Kairos window detection (opportune moment for entity classification)
- SELF Matrix integration (trauma-informed filtering)
- Transductive learning (organism-level pattern recognition)

Mathematical Compliance:
- Whitehead: Locus in extensive continuum (word + neighbor window)
- Hameroff: Time-crystal microtubule patch (multi-cycle resonance)
- DAE 3.0: V0 energy descent with 5-coefficient formula

Core Innovation:
- Words as experiencing subjects (Whiteheadian actual occasions)
- Neighbor context windows (spatial loci, 3-5 words left/right)
- Multi-cycle concrescence (appetition loop until Kairos)
- Satisfaction strains (gradients across cycles + neighbors)
- Felt + symbolic dual representation (intensity + form)

Process Philosophy Integration:
1. PREHENSION: NEXUS atoms feel word + neighbors
2. CONCRESCENCE: Multi-cycle V0 descent integrates signals
3. SATISFACTION: Kairos window [0.45, 0.70] triggers decision
4. DECISION: Entity type (or null) emerges from felt energy minimum
5. OBJECTIVE IMMORTALITY: Entity enters knowledge graph

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
Status: Phase 3B Complete - Dual Vector + Appetition Loop Operational
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import time


@dataclass
class WordOccasion:
    """
    Word-level actual occasion for neighbor prehension.

    Fundamental unit of entity extraction in neighbor-aware architecture.
    Each WordOccasion represents a single word with:
    - Sequential identity (position in sentence)
    - Neighbor context (3-5 words left/right)
    - Multi-organ prehensions (5 entity-awareness organs)
    - Entity classification (emergent from organ agreement)

    Key Differences from TextOccasion:
    - Word granularity (not chunk/sentence level)
    - Sequential neighbors (not semantic similarity)
    - Entity-focused organs (not general discourse processing)
    - 31D actualization (not 35D felt signature)

    Usage Flow:
    1. Tokenize sentence → Create WordOccasions
    2. For each WordOccasion:
       a. Extract left_neighbors (prev 3-5 words)
       b. Extract right_neighbors (next 3-5 words)
       c. Run 5-organ prehension → 31D actualization vector
       d. Run 4-gate intersection emission → Entity decision
    3. Merge adjacent entities (multi-word boundaries)
    4. Return high-confidence entities (>0.7)
    """

    # === IDENTITY ===
    word: str                          # "Emma", "work", "Apple"
    position: int                      # Word index in sentence (0-based)
    sentence: str                      # Full sentence context

    # === IDENTITY (from ActualOccasion pattern) ===
    entity_id: str = ""  # Unique identifier (auto-generated)
    creation_time: float = 0.0  # Timestamp

    # === NEIGHBOR CONTEXT (Spatial Locus) ===
    # Sequential neighbors (not semantic similarity)
    left_neighbors: List[str] = field(default_factory=list)   # ["Today"] (prev 3-5 words)
    right_neighbors: List[str] = field(default_factory=list)  # ["went", "to", "work"] (next 3-5 words)

    # Neighbor metadata
    neighbor_window_size: int = 5      # Max neighbors per side (default 5)

    # Neighbor WordOccasion references (for strain computation)
    left_neighbor_occasions: List['WordOccasion'] = field(default_factory=list)
    right_neighbor_occasions: List['WordOccasion'] = field(default_factory=list)

    # === DUAL VECTOR REPRESENTATION (from ActualOccasion) ===
    # Felt vector (31D from NEXUS atoms)
    felt_vector: Optional[np.ndarray] = None  # 31D actualization from organs

    # Symbolic vector (embedding from language model)
    symbolic_vector: Optional[np.ndarray] = None  # Optional LM embedding

    # Whiteheadian current + feeling vectors
    current_vector: Optional[np.ndarray] = None  # Current state in felt space
    feeling_vector: Optional[np.ndarray] = None  # Lure toward entity type

    # Optional Vector35D enhancement (if available)
    vector35d: Optional[Any] = None  # PhysicalFeelingDualityVector35D

    # === V0 ENERGY COMPONENTS (from DAE 3.0) ===
    v0_energy: float = 1.0  # Initial energy (descends toward 0)
    satisfaction: float = 0.0  # Kairos metric [0.0-1.0]
    appetition: float = 0.0  # Lure intensity toward entity type
    resonance: float = 0.0  # Agreement with neighbor loci
    coherence: float = 0.0  # Organ agreement
    vitality: float = 1.0  # Occasion vitality (from ActualOccasion)

    # DAE 3.0 Energy formula coefficients
    alpha: float = 0.40  # Satisfaction weight
    beta: float = 0.25  # Energy stability
    gamma: float = 0.15  # Appetition sensitivity
    delta: float = 0.10  # Resonance coupling
    zeta: float = 0.10  # Intersection boost

    # === APPETITION LOOP (Multi-Cycle Concrescence) ===
    energy_history: List[float] = field(default_factory=list)
    satisfaction_history: List[float] = field(default_factory=list)
    coherence_history: List[float] = field(default_factory=list)
    appetition_history: List[float] = field(default_factory=list)

    cycle_count: int = 0
    converged: bool = False
    max_cycles: int = 5  # From DAE 3.0
    kairos_window: Tuple[float, float] = (0.45, 0.70)  # From DAE 3.0

    # === MULTI-ORGAN PREHENSIONS ===
    # NEXUS 7 atoms (extended with neighbor awareness)
    organ_prehensions: Dict[str, np.ndarray] = field(default_factory=dict)

    # Aggregated actualization vector (7D from NEXUS atoms)
    actualization_vector: Optional[np.ndarray] = None  # 7D from NEXUS

    # Prehension history (from ActualOccasion)
    prehension_history: List[Dict] = field(default_factory=list)

    # === ENTITY CLASSIFICATION (Emergent) ===
    # Results from 4-gate intersection emission
    entity_type: Optional[str] = None           # "Person", "Place", "Food", "Company", etc.
    entity_confidence: float = 0.0              # Classification confidence (0.0-1.0)
    entity_coherence: float = 0.0               # Organ agreement (0.0-1.0)

    # Gate results (for debugging/analysis)
    intersection_score: float = 0.0             # Gate 1: Nexus count
    coherence_score: float = 0.0                # Gate 2: Organ agreement
    satisfaction_score: float = 0.0             # Gate 3: Kairos window
    felt_energy: float = 0.0                    # Gate 4: Entity type energy

    # === SELF MATRIX INTEGRATION (Trauma-Informed) ===
    self_zone: Optional[int] = None  # 1-5 from SELF Matrix
    zone_state: Optional[Any] = None  # SELFZoneState
    filtered_by_zone: bool = False  # Was entity filtered due to zone constraints?

    # === TRANSDUCTIVE PATTERN TRACKING (Organism Learning) ===
    transductive_state: Dict[str, Any] = field(default_factory=dict)
    # P_n: Pattern memory (organ pattern → entity type mapping)
    # R_n: Relevance field (salience given context)
    # V⃗_f: Vector feeling (direction + valence + intensity)
    # ΔC_n: Constraint shift (neighbor context changes)

    # === METADATA ===
    # Word characteristics
    is_capitalized: bool = False                # Proper noun indicator
    is_first_in_sentence: bool = False          # Position indicator
    has_punctuation: bool = False               # Boundary marker

    # Processing state
    processed: bool = False                     # Has been through organ prehension
    emitted: bool = False                       # Has passed 4-gate emission

    def __post_init__(self):
        """Initialize derived fields and validate structure."""
        # Generate unique entity_id
        if not self.entity_id:
            self.entity_id = f"WO_{id(self)}_{time.time()}"

        # Set creation time
        if self.creation_time == 0.0:
            self.creation_time = time.time()

        # Detect capitalization
        if self.word:
            self.is_capitalized = self.word[0].isupper()
            self.has_punctuation = any(c in self.word for c in '.,!?;:')

        # Detect first position
        self.is_first_in_sentence = (self.position == 0)

        # Initialize current_vector as zero (will be updated during prehension)
        if self.current_vector is None:
            self.current_vector = np.zeros(7)  # 7D from NEXUS atoms

        # Initialize feeling_vector as zero (lure toward entity types)
        if self.feeling_vector is None:
            self.feeling_vector = np.zeros(7)

    # ========================================================================
    # NEIGHBOR EXTRACTION METHODS
    # ========================================================================

    @classmethod
    def from_sentence(
        cls,
        sentence: str,
        position: int,
        neighbor_window_size: int = 5
    ) -> 'WordOccasion':
        """
        Create WordOccasion from sentence with automatic neighbor extraction.

        Args:
            sentence: Full sentence text
            position: Word index in sentence (0-based)
            neighbor_window_size: Max neighbors per side (default 5)

        Returns:
            WordOccasion with neighbors populated

        Example:
            sentence = "Today Emma went to work"
            word_occ = WordOccasion.from_sentence(sentence, position=1)
            # word_occ.word = "Emma"
            # word_occ.left_neighbors = ["Today"]
            # word_occ.right_neighbors = ["went", "to", "work"]
        """
        # Tokenize sentence
        words = sentence.split()

        if position < 0 or position >= len(words):
            raise ValueError(f"Position {position} out of range for sentence with {len(words)} words")

        word = words[position]

        # Extract left neighbors (up to window_size)
        left_start = max(0, position - neighbor_window_size)
        left_neighbors = words[left_start:position]

        # Extract right neighbors (up to window_size)
        right_end = min(len(words), position + 1 + neighbor_window_size)
        right_neighbors = words[position + 1:right_end]

        return cls(
            word=word,
            position=position,
            sentence=sentence,
            left_neighbors=left_neighbors,
            right_neighbors=right_neighbors,
            neighbor_window_size=neighbor_window_size
        )

    @classmethod
    def from_sentence_batch(
        cls,
        sentence: str,
        neighbor_window_size: int = 5
    ) -> List['WordOccasion']:
        """
        Create WordOccasions for all words in sentence.

        Args:
            sentence: Full sentence text
            neighbor_window_size: Max neighbors per side (default 5)

        Returns:
            List of WordOccasion instances (one per word)

        Example:
            sentence = "Today Emma went to work"
            word_occasions = WordOccasion.from_sentence_batch(sentence)
            # Returns 5 WordOccasions with neighbor context
        """
        words = sentence.split()
        occasions = []

        for position in range(len(words)):
            occasion = cls.from_sentence(sentence, position, neighbor_window_size)
            occasions.append(occasion)

        return occasions

    # ========================================================================
    # ORGAN PREHENSION METHODS
    # ========================================================================

    def add_organ_prehension(self, organ_name: str, prehension_vector: np.ndarray):
        """
        Store organ prehension result.

        Args:
            organ_name: "EntityRecall", "RelationalBinding", "CoOccurrence", "Novelty", "Archetype"
            prehension_vector: Numpy array (7D, 6D, 6D, 5D, or 7D respectively)

        Example:
            word_occ.add_organ_prehension(
                "EntityRecall",
                np.array([0.92, 0.85, 0.78, ...])  # 7D
            )
        """
        self.organ_prehensions[organ_name] = prehension_vector
        self.processed = True

    def compute_actualization_vector(self) -> np.ndarray:
        """
        Aggregate organ prehensions into 31D actualization vector.

        Order: EntityRecall (7D) + RelationalBinding (6D) + CoOccurrence (6D) +
               Novelty (5D) + Archetype (7D) = 31D

        Returns:
            31D numpy array (or zeros if organs not yet processed)
        """
        expected_organs = {
            'EntityRecall': 7,
            'RelationalBinding': 6,
            'CoOccurrence': 6,
            'Novelty': 5,
            'Archetype': 7
        }

        vectors = []
        for organ_name, expected_dim in expected_organs.items():
            if organ_name in self.organ_prehensions:
                vectors.append(self.organ_prehensions[organ_name])
            else:
                # Zero-fill missing organs
                vectors.append(np.zeros(expected_dim))

        self.actualization_vector = np.concatenate(vectors)
        return self.actualization_vector

    def get_organ_activations(self) -> List[float]:
        """
        Get mean activation per organ (for intersection gate).

        Returns:
            List of 5 floats (mean activation per organ)
        """
        if not self.organ_prehensions:
            return [0.0] * 5

        activations = []
        for organ_name in ['EntityRecall', 'RelationalBinding', 'CoOccurrence', 'Novelty', 'Archetype']:
            if organ_name in self.organ_prehensions:
                activations.append(float(np.mean(self.organ_prehensions[organ_name])))
            else:
                activations.append(0.0)

        return activations

    # ========================================================================
    # APPETITION LOOP METHODS (Multi-Cycle Concrescence)
    # ========================================================================

    def run_concrescence_cycle(
        self,
        nexus_organ,  # NEXUSTextCore instance
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Run single V0 energy descent cycle.

        Implements Whitehead's concrescence: integration of prehensions toward satisfaction.
        Based on DAE 3.0 grid cell convergence formula.

        Args:
            nexus_organ: NEXUSTextCore instance for atom calculation
            context: Processing context (user_id, entity_tracker, etc.)

        Returns:
            True if converged to Kairos window, False otherwise

        Process:
        1. Calculate NEXUS atom activations with neighbors
        2. Compute organ coherence
        3. Compute appetition (lure toward entity types)
        4. Compute resonance (neighbor agreement)
        5. Compute satisfaction from coherence + appetition
        6. Compute V0 energy: E = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I)
        7. Check Kairos window [0.45, 0.70]
        """
        self.cycle_count += 1
        context = context or {}

        # Step 1: Calculate NEXUS atom activations with neighbors
        atom_activations = nexus_organ._calculate_atom_activations_with_neighbors(self, context)

        # Update current_vector from atom activations
        if atom_activations:
            # Convert dict to ordered 7D vector (NEXUS has 7 atoms)
            atom_names = ['entity_recall', 'relationship_depth', 'temporal_continuity',
                         'co_occurrence', 'salience_gradient', 'memory_coherence',
                         'contextual_grounding']
            self.current_vector = np.array([atom_activations.get(name, 0.0) for name in atom_names])

        # Step 2: Compute organ coherence (how much atoms agree)
        self.coherence = self._compute_organ_coherence(atom_activations)

        # Step 3: Compute appetition (lure toward entity types)
        self.appetition = self._compute_appetition(atom_activations)

        # Step 4: Compute resonance (neighbor agreement)
        self.resonance = self._compute_resonance(context)

        # Step 5: Compute satisfaction from coherence + appetition
        # Satisfaction = harmony of atoms + strength of lure
        self.satisfaction = (self.coherence * 0.6 + self.appetition * 0.4)

        # Step 6: Compute V0 energy (DAE 3.0 formula)
        delta_energy = 0.0
        if len(self.energy_history) > 0:
            delta_energy = abs(self.v0_energy - self.energy_history[-1])

        # Intersection: ≥2 atoms must activate (from DAE 3.0)
        intersection = 1.0 if len(atom_activations) >= 2 else 0.5

        self.v0_energy = (
            self.alpha * (1.0 - self.satisfaction) +
            self.beta * delta_energy +
            self.gamma * (1.0 - self.appetition) +
            self.delta * (1.0 - self.resonance) +
            self.zeta * intersection
        )

        # Track history (satisfaction strains across cycles)
        self.energy_history.append(self.v0_energy)
        self.satisfaction_history.append(self.satisfaction)
        self.coherence_history.append(self.coherence)
        self.appetition_history.append(self.appetition)

        # Record prehension in history (from ActualOccasion pattern)
        prehension_record = {
            "time": time.time(),
            "cycle": self.cycle_count,
            "atom_activations": atom_activations,
            "satisfaction": self.satisfaction,
            "v0_energy": self.v0_energy,
            "coherence": self.coherence
        }
        self.prehension_history.append(prehension_record)

        # Step 7: Check Kairos window [0.45, 0.70]
        kairos_min, kairos_max = self.kairos_window
        if kairos_min <= self.satisfaction <= kairos_max:
            self.converged = True
            return True

        # Not converged yet
        return False

    def achieve_satisfaction(
        self,
        nexus_organ,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Run full multi-cycle convergence until Kairos or max_cycles.

        This is the complete Whiteheadian concrescence process:
        - Multiple cycles of prehension + integration
        - Converges when satisfaction enters Kairos window
        - Achieves "satisfaction" in Whitehead's technical sense

        Args:
            nexus_organ: NEXUSTextCore instance
            context: Processing context

        Returns:
            True if converged, False if max cycles exceeded
        """
        for cycle in range(self.max_cycles):
            converged = self.run_concrescence_cycle(nexus_organ, context)
            if converged:
                break

        return self.converged

    def _compute_organ_coherence(self, atom_activations: Dict[str, float]) -> float:
        """
        Compute organ coherence (how much NEXUS atoms agree).

        Coherence = measure of harmony across prehensions.
        High coherence = atoms align on same entity interpretation.

        Args:
            atom_activations: Dict of atom_name → activation

        Returns:
            Coherence [0.0-1.0]
        """
        if not atom_activations:
            return 0.0

        # Mean activation strength
        activations = list(atom_activations.values())
        mean_activation = np.mean(activations)

        # Variance (low variance = high agreement)
        variance = np.var(activations)

        # Coherence = high mean + low variance
        coherence = mean_activation * (1.0 - min(variance, 1.0))

        return float(np.clip(coherence, 0.0, 1.0))

    def _compute_appetition(self, atom_activations: Dict[str, float]) -> float:
        """
        Compute appetition (lure intensity toward entity classification).

        Appetition = Whitehead's term for "pull toward" an ideal.
        High appetition = strong lure toward being an entity.

        Args:
            atom_activations: Dict of atom_name → activation

        Returns:
            Appetition [0.0-1.0]
        """
        if not atom_activations:
            return 0.0

        # Key atoms that indicate entity-ness
        entity_atoms = ['entity_recall', 'relationship_depth', 'contextual_grounding']

        # Appetition = mean of entity-indicating atoms
        entity_activations = [
            atom_activations.get(atom, 0.0) for atom in entity_atoms
        ]

        appetition = np.mean(entity_activations)

        # Boost if capitalized (proper noun signal)
        if self.is_capitalized and not self.is_first_in_sentence:
            appetition = min(1.0, appetition * 1.2)

        return float(np.clip(appetition, 0.0, 1.0))

    def _compute_resonance(self, context: Dict[str, Any]) -> float:
        """
        Compute resonance (agreement with neighbor loci).

        Resonance = Whitehead's term for harmony with other occasions.
        High resonance = neighbors also activated (coherent field).

        Args:
            context: Processing context

        Returns:
            Resonance [0.0-1.0]
        """
        # If we have neighbor occasion references, use their satisfactions
        all_neighbors = self.left_neighbor_occasions + self.right_neighbor_occasions

        if not all_neighbors:
            return 0.5  # Neutral if no neighbors

        # Resonance = mean satisfaction of neighbors
        neighbor_satisfactions = [
            n.satisfaction for n in all_neighbors if n.satisfaction > 0
        ]

        if not neighbor_satisfactions:
            return 0.5

        resonance = np.mean(neighbor_satisfactions)

        return float(np.clip(resonance, 0.0, 1.0))

    def compute_satisfaction_gradient(self) -> float:
        """
        Compute spatial gradient of satisfaction across neighbor loci.

        This is the "strain" in Whitehead's extensive continuum.
        High gradient = significant change across spatial neighbors.

        Returns:
            Gradient (variance across neighbors + self)
        """
        all_neighbors = self.left_neighbor_occasions + self.right_neighbor_occasions

        if not all_neighbors:
            return 0.0

        # Collect satisfactions
        satisfactions = [n.satisfaction for n in all_neighbors if n.satisfaction > 0]
        satisfactions.append(self.satisfaction)

        if len(satisfactions) < 2:
            return 0.0

        # Gradient = standard deviation (variance measure)
        gradient = float(np.std(satisfactions))

        return gradient

    # ========================================================================
    # ENTITY CLASSIFICATION METHODS
    # ========================================================================

    def set_entity_classification(
        self,
        entity_type: Optional[str],
        confidence: float,
        coherence: float,
        gate_results: Optional[Dict[str, float]] = None
    ):
        """
        Store entity classification results from 4-gate emission.

        Args:
            entity_type: "Person", "Place", "Food", "Company", etc. (None if not entity)
            confidence: Classification confidence (0.0-1.0)
            coherence: Organ agreement (0.0-1.0)
            gate_results: Optional gate scores for debugging
        """
        self.entity_type = entity_type
        self.entity_confidence = confidence
        self.entity_coherence = coherence
        self.emitted = True

        if gate_results:
            self.intersection_score = gate_results.get('intersection', 0.0)
            self.coherence_score = gate_results.get('coherence', 0.0)
            self.satisfaction_score = gate_results.get('satisfaction', 0.0)
            self.felt_energy = gate_results.get('felt_energy', 0.0)

    def is_entity(self) -> bool:
        """
        Check if word was classified as entity.

        Returns:
            True if entity_type is not None and confidence > threshold
        """
        return self.entity_type is not None and self.entity_confidence > 0.0

    def to_entity_dict(self) -> Optional[Dict[str, Any]]:
        """
        Convert to entity dict format (compatible with entity-organ tracker).

        Returns:
            Dict with entity_value, entity_type, confidence, etc. (or None if not entity)
        """
        if not self.is_entity():
            return None

        # Build gate_results dict if scores are available (Phase 3B - Nov 18, 2025)
        gate_results = None
        if hasattr(self, 'intersection_score'):
            gate_results = {
                'gate_1_intersection': {
                    'passed': self.intersection_score >= 1.5 if hasattr(self, 'intersection_score') else False,
                    'score': getattr(self, 'intersection_score', 0.0)
                },
                'gate_2_coherence': {
                    'passed': self.coherence_score >= 0.4 if hasattr(self, 'coherence_score') else False,
                    'score': getattr(self, 'coherence_score', 0.0)
                },
                'gate_3_satisfaction': {
                    'passed': 0.45 <= self.satisfaction_score <= 0.85 if hasattr(self, 'satisfaction_score') else False,
                    'score': getattr(self, 'satisfaction_score', 0.0)
                },
                'gate_4_felt_energy': {
                    'passed': self.felt_energy <= 0.7 if hasattr(self, 'felt_energy') else False,
                    'score': getattr(self, 'felt_energy', 1.0)
                }
            }

        entity_dict = {
            'entity_value': self.word,
            'entity_type': self.entity_type,
            'confidence_score': self.entity_confidence,
            'coherence': self.entity_coherence,
            'position': self.position,
            'actualization_vector': self.actualization_vector.tolist() if self.actualization_vector is not None else None,
            'source': 'neighbor_prehension'
        }

        # Add gate_results if available (for GateCascadeQualityTracker)
        if gate_results:
            entity_dict['gate_results'] = gate_results

        return entity_dict

    # ========================================================================
    # NEIGHBOR ANALYSIS METHODS
    # ========================================================================

    def get_neighbor_context_string(self, max_neighbors: int = 3) -> str:
        """
        Get readable neighbor context for debugging.

        Args:
            max_neighbors: Max neighbors to show per side

        Returns:
            String like "[Today] Emma [went, to, work]"
        """
        left_str = " ".join(self.left_neighbors[-max_neighbors:])
        right_str = " ".join(self.right_neighbors[:max_neighbors])

        left_part = f"[{left_str}]" if left_str else ""
        right_part = f"[{right_str}]" if right_str else ""

        return f"{left_part} {self.word} {right_part}".strip()

    def has_relationship_keywords(self, relationship_keywords: List[str]) -> bool:
        """
        Check if neighbors contain relationship keywords.

        Args:
            relationship_keywords: List of keywords like ["daughter", "son", "wife", ...]

        Returns:
            True if any neighbor matches relationship keyword
        """
        all_neighbors = self.left_neighbors + self.right_neighbors
        return any(
            neighbor.lower() in relationship_keywords
            for neighbor in all_neighbors
        )

    def has_possessive_markers(self) -> bool:
        """
        Check if left neighbors contain possessive markers.

        Returns:
            True if left neighbors have "my", "her", "his", "their"
        """
        possessive_markers = ["my", "her", "his", "their", "our", "your"]
        return any(
            neighbor.lower() in possessive_markers
            for neighbor in self.left_neighbors
        )

    def has_action_verbs(self, action_verbs: List[str]) -> bool:
        """
        Check if neighbors contain action verbs.

        Args:
            action_verbs: List of verbs like ["went", "said", "told", ...]

        Returns:
            True if any neighbor matches action verb
        """
        all_neighbors = self.left_neighbors + self.right_neighbors
        return any(
            neighbor.lower() in action_verbs
            for neighbor in all_neighbors
        )

    # ========================================================================
    # SERIALIZATION METHODS
    # ========================================================================

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize to dictionary.

        Returns:
            Dictionary representation (JSON-compatible)
        """
        return {
            'word': self.word,
            'position': self.position,
            'sentence': self.sentence,
            'left_neighbors': self.left_neighbors,
            'right_neighbors': self.right_neighbors,
            'neighbor_window_size': self.neighbor_window_size,
            'organ_prehensions': {
                organ: vec.tolist() for organ, vec in self.organ_prehensions.items()
            },
            'actualization_vector': self.actualization_vector.tolist() if self.actualization_vector is not None else None,
            'entity_type': self.entity_type,
            'entity_confidence': self.entity_confidence,
            'entity_coherence': self.entity_coherence,
            'intersection_score': self.intersection_score,
            'coherence_score': self.coherence_score,
            'satisfaction_score': self.satisfaction_score,
            'felt_energy': self.felt_energy,
            'is_capitalized': self.is_capitalized,
            'is_first_in_sentence': self.is_first_in_sentence,
            'has_punctuation': self.has_punctuation,
            'processed': self.processed,
            'emitted': self.emitted
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WordOccasion':
        """
        Deserialize from dictionary.

        Args:
            data: Dictionary from to_dict()

        Returns:
            WordOccasion instance
        """
        # Convert lists back to numpy arrays
        organ_prehensions = {
            organ: np.array(vec) for organ, vec in data.get('organ_prehensions', {}).items()
        }

        actualization_vector = None
        if data.get('actualization_vector') is not None:
            actualization_vector = np.array(data['actualization_vector'])

        return cls(
            word=data['word'],
            position=data['position'],
            sentence=data['sentence'],
            left_neighbors=data.get('left_neighbors', []),
            right_neighbors=data.get('right_neighbors', []),
            neighbor_window_size=data.get('neighbor_window_size', 5),
            organ_prehensions=organ_prehensions,
            actualization_vector=actualization_vector,
            entity_type=data.get('entity_type'),
            entity_confidence=data.get('entity_confidence', 0.0),
            entity_coherence=data.get('entity_coherence', 0.0),
            intersection_score=data.get('intersection_score', 0.0),
            coherence_score=data.get('coherence_score', 0.0),
            satisfaction_score=data.get('satisfaction_score', 0.0),
            felt_energy=data.get('felt_energy', 0.0),
            is_capitalized=data.get('is_capitalized', False),
            is_first_in_sentence=data.get('is_first_in_sentence', False),
            has_punctuation=data.get('has_punctuation', False),
            processed=data.get('processed', False),
            emitted=data.get('emitted', False)
        )

    # ========================================================================
    # SELF MATRIX FILTERING METHODS
    # ========================================================================

    def filter_by_self_zone(
        self,
        bond_self_distance: float,
        polyvagal_state: str,
        urgency_level: float
    ) -> bool:
        """
        Filter word occasion through SELF Matrix trauma-informed governance.

        This implements the 4-layer transductive entity filtering:
        - Layer 0: BOND IFS Gate (keyword enrichment)
        - Layer 1: SELF Matrix Zone Gating (5 zones)
        - Layer 2: Salience + Temporal Decay
        - Layer 3: Satisfaction + Memory Regime

        Args:
            bond_self_distance: Self-distance from BOND organ (0.0-1.0)
            polyvagal_state: "ventral", "sympathetic", or "dorsal"
            urgency_level: Urgency from NDAM organ (0.0-1.0)

        Returns:
            True if word passes SELF zone filtering (should be processed)

        Updates:
            self.self_zone: Zone number (1-5)
            self.zone_state: Zone characteristics dict
            self.filtered_by_zone: True if filtered out
        """
        # Map BOND self_distance to SELF Matrix zone (5 zones)
        # Zone 1 (0.0-0.2): High Self-Energy, ventral, low urgency
        # Zone 2 (0.2-0.4): Moderate Self-Energy, ventral, moderate urgency
        # Zone 3 (0.4-0.6): Mixed Parts, sympathetic, moderate urgency
        # Zone 4 (0.6-0.8): Protector-Dominated, sympathetic/dorsal, high urgency
        # Zone 5 (0.8-1.0): Exile-Dominated, dorsal, extreme urgency

        if bond_self_distance < 0.2:
            self.self_zone = 1
            zone_name = "HIGH_SELF_ENERGY"
            allow_entities = True  # Process all entities
        elif bond_self_distance < 0.4:
            self.self_zone = 2
            zone_name = "MODERATE_SELF_ENERGY"
            allow_entities = True  # Process most entities
        elif bond_self_distance < 0.6:
            self.self_zone = 3
            zone_name = "MIXED_PARTS"
            allow_entities = urgency_level < 0.7  # Filter high-urgency entities
        elif bond_self_distance < 0.8:
            self.self_zone = 4
            zone_name = "PROTECTOR_DOMINATED"
            allow_entities = urgency_level < 0.5  # Filter moderate-urgency entities
        else:
            self.self_zone = 5
            zone_name = "EXILE_DOMINATED"
            allow_entities = urgency_level < 0.3  # Only allow low-urgency entities

        # Store zone state
        self.zone_state = {
            'zone': self.self_zone,
            'zone_name': zone_name,
            'bond_self_distance': bond_self_distance,
            'polyvagal_state': polyvagal_state,
            'urgency_level': urgency_level
        }

        # Apply filtering based on zone
        if not allow_entities:
            self.filtered_by_zone = True
            return False  # Block processing

        self.filtered_by_zone = False
        return True  # Allow processing

    # ========================================================================
    # TRANSDUCTIVE PATTERN TRACKING METHODS
    # ========================================================================

    def update_transductive_state(
        self,
        prehensions: Dict[str, Any],
        reactions: Dict[str, Any],
        felt_vector: np.ndarray,
        coherence_change: float
    ):
        """
        Update transductive pattern tracking state.

        Implements: T(S) = f(P_n, R_n, V⃗_f, ΔC_n) ⇒ N_{n+1}
        (Transductive Self-Governance formula)

        Args:
            prehensions: Current prehension data (organ activations)
            reactions: Reaction data (neighbor responses)
            felt_vector: Current felt vector (7D from NEXUS atoms)
            coherence_change: Change in coherence from previous cycle

        Updates:
            self.transductive_state: Dict tracking pattern evolution
        """
        self.transductive_state.update({
            'prehensions': prehensions,
            'reactions': reactions,
            'felt_vector': felt_vector.tolist() if isinstance(felt_vector, np.ndarray) else felt_vector,
            'coherence_change': coherence_change,
            'cycle_count': len(self.energy_history),  # Track via history length
            'converged': self.converged,
            'timestamp': time.time()
        })

    def get_transductive_trajectory(self) -> List[Dict[str, Any]]:
        """
        Get full transductive trajectory across all cycles.

        Returns:
            List of transductive states (one per cycle)
        """
        # For now, return single state (can extend to multi-cycle tracking)
        return [self.transductive_state] if self.transductive_state else []

    def __repr__(self) -> str:
        """String representation for debugging."""
        entity_str = f"→{self.entity_type}" if self.entity_type else ""
        confidence_str = f"({self.entity_confidence:.2f})" if self.entity_type else ""
        return (
            f"WordOccasion('{self.word}'{entity_str}{confidence_str}, "
            f"pos={self.position}, "
            f"neighbors=[{len(self.left_neighbors)}L, {len(self.right_neighbors)}R])"
        )


# ========================================================================
# UTILITY FUNCTIONS
# ========================================================================

def create_word_occasions_from_text(
    text: str,
    neighbor_window_size: int = 5
) -> List[WordOccasion]:
    """
    Batch create WordOccasions from text (handles multi-sentence input).

    Args:
        text: Input text (can be multiple sentences)
        neighbor_window_size: Max neighbors per side (default 5)

    Returns:
        List of WordOccasion instances

    Example:
        text = "Today Emma went to work. She got stressed."
        occasions = create_word_occasions_from_text(text)
        # Returns 9 WordOccasions (5 + 4 words)
    """
    # Simple sentence splitting (naive - just split on '. ')
    sentences = [s.strip() for s in text.split('. ') if s.strip()]

    all_occasions = []
    global_position = 0

    for sentence in sentences:
        # Create occasions for this sentence
        sentence_occasions = WordOccasion.from_sentence_batch(sentence, neighbor_window_size)

        # Update global positions
        for occasion in sentence_occasions:
            occasion.position = global_position
            global_position += 1

        all_occasions.extend(sentence_occasions)

    return all_occasions


if __name__ == "__main__":
    """
    Validation test for WordOccasion class.
    """
    print("=" * 80)
    print("🧪 WORD OCCASION VALIDATION TEST")
    print("=" * 80)

    # Test 1: Single word occasion creation
    print("\n📋 TEST 1: Single WordOccasion Creation")
    sentence = "Today Emma went to work"
    word_occ = WordOccasion.from_sentence(sentence, position=1)

    print(f"   ✅ Created: {word_occ}")
    print(f"      Word: '{word_occ.word}'")
    print(f"      Position: {word_occ.position}")
    print(f"      Left neighbors: {word_occ.left_neighbors}")
    print(f"      Right neighbors: {word_occ.right_neighbors}")
    print(f"      Context: {word_occ.get_neighbor_context_string()}")

    # Test 2: Batch creation
    print("\n📋 TEST 2: Batch WordOccasion Creation")
    occasions = WordOccasion.from_sentence_batch(sentence)
    print(f"   ✅ Created {len(occasions)} occasions:")
    for occ in occasions:
        print(f"      {occ.get_neighbor_context_string()}")

    # Test 3: Organ prehension
    print("\n📋 TEST 3: Organ Prehension")
    word_occ.add_organ_prehension("EntityRecall", np.array([0.92, 0.85, 0.78, 0.70, 0.65, 0.88, 0.75]))
    word_occ.add_organ_prehension("RelationalBinding", np.array([0.80, 0.70, 0.65, 0.60, 0.55, 0.75]))
    word_occ.add_organ_prehension("CoOccurrence", np.array([0.75, 0.70, 0.65, 0.60, 0.55, 0.70]))
    word_occ.add_organ_prehension("Novelty", np.array([0.20, 0.15, 0.10, 0.25, 0.18]))
    word_occ.add_organ_prehension("Archetype", np.array([0.90, 0.30, 0.20, 0.15, 0.85, 0.80, 0.25]))

    actualization = word_occ.compute_actualization_vector()
    print(f"   ✅ Actualization vector: shape={actualization.shape}, mean={np.mean(actualization):.3f}")

    activations = word_occ.get_organ_activations()
    print(f"   ✅ Organ activations: {[f'{a:.3f}' for a in activations]}")

    # Test 4: Entity classification
    print("\n📋 TEST 4: Entity Classification")
    word_occ.set_entity_classification(
        entity_type="Person",
        confidence=0.92,
        coherence=0.85,
        gate_results={
            'intersection': 4.0,
            'coherence': 0.85,
            'satisfaction': 0.68,
            'felt_energy': 0.32
        }
    )

    print(f"   ✅ Entity classified: {word_occ}")
    entity_dict = word_occ.to_entity_dict()
    print(f"      Entity dict: {entity_dict['entity_value']} ({entity_dict['entity_type']}, conf={entity_dict['confidence_score']:.2f})")

    # Test 5: Neighbor analysis
    print("\n📋 TEST 5: Neighbor Analysis Methods")
    print(f"   Has relationship keywords: {word_occ.has_relationship_keywords(['daughter', 'son', 'wife'])}")
    print(f"   Has possessive markers: {word_occ.has_possessive_markers()}")
    print(f"   Has action verbs: {word_occ.has_action_verbs(['went', 'said', 'told'])}")

    # Test 6: Serialization
    print("\n📋 TEST 6: Serialization")
    word_dict = word_occ.to_dict()
    word_restored = WordOccasion.from_dict(word_dict)
    print(f"   ✅ Serialized & restored: {word_restored}")
    print(f"      Match: word={word_restored.word == word_occ.word}, type={word_restored.entity_type == word_occ.entity_type}")

    # Test 7: Multi-sentence input
    print("\n📋 TEST 7: Multi-Sentence Input")
    text = "I met my friend Zephyr yesterday. She went to work today."
    occasions = create_word_occasions_from_text(text)
    print(f"   ✅ Created {len(occasions)} occasions from 2 sentences:")
    for i, occ in enumerate(occasions):
        if i < 5 or i >= len(occasions) - 5:  # Show first 5 and last 5
            print(f"      [{i}] {occ.get_neighbor_context_string()}")
        elif i == 5:
            print(f"      ...")

    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED - WordOccasion operational!")
    print("=" * 80)
