"""
NDAM Text Core - Narrative Dynamics & Urgency Detection (Text Domain)

Text-native implementation of NDAM organ for organizational governance processing.
Detects narrative urgency, crisis patterns, and temporal dynamics through keyword
analysis and pattern detection.

Architecture:
- 100% LLM-free (pure keyword matching)
- Text-native urgency detection
- 6 urgency types (crisis, temporal, emotional, etc.)
- Hebbian learning of new keywords (Phase 2)
- Escalation pattern detection

Author: DAE-GOV Development Team
Created: November 10, 2025
Version: 1.0 (Text-Native Foundation)
"""

import numpy as np
import time
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import sys

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from organs.modular.ndam.organ_config.ndam_config import NDAMConfig, DEFAULT_NDAM_CONFIG
from transductive.text_occasion import TextOccasion


@dataclass
class UrgencyPattern:
    """Detected urgency pattern."""

    pattern_type: str                       # "crisis_urgency", "temporal_pressure", etc.
    strength: float                         # Urgency strength (0-2.0, amplified)
    chunk_id: str                           # Chunk containing urgency
    matched_keywords: List[str]             # Keywords that matched
    confidence: float                       # Pattern confidence (0-1)

    # Context
    text_snippet: Optional[str] = None
    position: int = 0

    # Metadata
    detected_timestamp: float = field(default_factory=time.time)


@dataclass
class NDAMResult:
    """Result from NDAM organ processing."""

    coherence: float                        # Overall urgency coherence (0-1)
    patterns: List[UrgencyPattern]          # Detected urgency patterns
    lure: float                             # Appetition lure strength (0-1)
    processing_time: float                  # Milliseconds

    # Detailed outputs
    mean_urgency: float = 0.0               # Mean urgency across conversation
    max_urgency: float = 0.0                # Maximum urgency detected
    escalation_detected: bool = False       # Whether escalation pattern found
    dominant_urgency_type: Optional[str] = None  # Most common urgency type

    # 🆕 LURE ATTRACTOR FIELD: Multi-level salience (urgent/important/exploratory)
    salience_field: Dict[str, float] = field(default_factory=dict)

    # Metadata
    occasions_processed: int = 0
    keywords_matched: int = 0

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native

    # 🆕 PHASE C3: Embedding-based lure field (Nov 13, 2025)
    urgency_lure_field: Dict[str, float] = field(default_factory=dict)


class NDAMTextCore:
    """
    NDAM (Narrative Dynamics & Urgency Detection) - Text Domain

    Processes text occasions to detect urgency patterns through pure
    keyword matching (100% LLM-free).

    Key Responsibilities:
    - Keyword-based urgency detection (47 predefined keywords)
    - Pattern classification (6 types: crisis, temporal, emotional, etc.)
    - Escalation detection (across sentence windows)
    - Narrative urgency measurement
    - Hebbian pattern learning (Phase 2)

    Universal Organ Interface:
    - process_text_occasions(occasions, cycle) → NDAMResult
    - get_organ_config() → Dict
    - get_hebbian_learning_config() → Dict
    """

    def __init__(self, config: Optional[NDAMConfig] = None):
        """
        Initialize NDAM text-native organ.

        Args:
            config: Optional NDAMConfig instance
        """
        self.config = config or DEFAULT_NDAM_CONFIG

        # 🆕 PHASE 1: Entity-native support
        self.organ_name = "NDAM"
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE 2: Load shared meta-atoms for nexus formation
        self.meta_atoms_config = self._load_shared_meta_atoms()

        # 🆕 PHASE C3: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

        # Compile keyword patterns for efficient matching
        self._compile_keyword_patterns()

        # Pattern detection history (for learning)
        self.pattern_history: List[UrgencyPattern] = []

        # Statistics
        self.total_occasions_processed = 0
        self.total_patterns_detected = 0
        self.total_processing_time = 0.0

        print(f"✅ NDAM organ initialized (text-native, LLM-free)")
        print(f"   Urgency threshold: {self.config.urgency_threshold}")
        print(f"   Keywords: {len(self.config.urgency_keywords)}")
        print(f"   Escalation window: {self.config.escalation_detection_window} sentences")

    # ========================================================================
    # 🆕 PHASE 1: ENTITY-NATIVE ATOM ACTIVATION
    # ========================================================================

    def _load_semantic_atoms(self) -> List[str]:
        """Load NDAM semantic atoms from semantic_atoms.json."""
        import json
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        atoms_path = os.path.join(current_dir, '..', '..', '..', '..',
                                  'persona_layer', 'semantic_atoms.json')

        try:
            with open(atoms_path, 'r') as f:
                all_atoms = json.load(f)

            if self.organ_name not in all_atoms:
                return []

            metadata_keys = {'description', 'dimension', 'field_type', 'total_atoms'}
            organ_data = all_atoms[self.organ_name]
            atom_names = [k for k in organ_data.keys() if k not in metadata_keys]

            return atom_names
        except Exception as e:
            print(f"Warning: Could not load semantic atoms for {self.organ_name}: {e}")
            return []

    def _load_shared_meta_atoms(self) -> Optional[Dict]:
        """
        🆕 PHASE 2: Load shared meta-atoms for nexus formation.

        NDAM contributes to 2 meta-atoms:
        - trauma_aware (BOND, EO, NDAM) - Crisis markers + urgency
        - safety_restoration (SANS, EO, NDAM) - Safety language detection
        """
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

            return {
                'meta_atoms': relevant_meta_atoms,
                'count': len(relevant_meta_atoms)
            }
        except Exception as e:
            return None

    def _compute_atom_activations(
        self,
        patterns: List[UrgencyPattern],
        coherence: float,
        lure: float,
        escalation_detected: bool
    ) -> Dict[str, float]:
        """
        🆕 PHASE 1: DIRECT atom activation computation (bypasses semantic_field_extractor!)

        Maps NDAM urgency pattern types → semantic atoms:
        - crisis_urgency → crisis_markers (immediate danger)
        - temporal_pressure → escalation_signals (time running out)
        - emotional_intensity → harm_indicators (burnout/breakdown)
        - organizational_dysfunction → boundary_violations (toxic dynamics)
        - firefighter_activation → resource_deficit (compulsive fixing)

        Special atoms:
        - safety_language: Activated when low urgency (absence of crisis)
        - containment_needs: Activated when escalation_detected
        """
        if not patterns:
            # No urgency detected - activate safety_language
            return {'safety_language': 0.8 * coherence}

        atom_activations = {}

        # Pattern type → atom mapping
        pattern_to_atom = {
            'crisis_urgency': 'crisis_markers',
            'temporal_pressure': 'escalation_signals',
            'emotional_intensity': 'harm_indicators',
            'organizational_dysfunction': 'boundary_violations',
            'firefighter_activation': 'resource_deficit'
        }

        for pattern in patterns:
            # Direct pattern type mapping
            atom = pattern_to_atom.get(pattern.pattern_type)
            if atom:
                # Base activation from pattern strength and confidence
                base_activation = pattern.strength * pattern.confidence
                activation = base_activation * coherence
                atom_activations[atom] = atom_activations.get(atom, 0.0) + activation

        # Special case: containment_needs
        # Activated when escalation detected (urgency increasing over time)
        if escalation_detected:
            # High containment need when escalation present
            containment_activation = 0.8 * coherence * (1.0 + lure * 0.5)
            atom_activations['containment_needs'] = containment_activation

        # Special case: safety_language
        # Activated when urgency is LOW (absence of crisis = safety present)
        if patterns:
            mean_urgency = np.mean([p.strength for p in patterns])
            if mean_urgency < 0.5:  # Low urgency threshold
                safety_activation = (1.0 - mean_urgency) * coherence
                atom_activations['safety_language'] = safety_activation

        # Apply lure weighting
        lure_weight = 0.5 + 0.5 * lure
        for atom in atom_activations:
            atom_activations[atom] *= lure_weight

        # Normalize to [0.0, 1.0]
        if atom_activations:
            max_activation = max(atom_activations.values())
            if max_activation > 1.0:
                for atom in atom_activations:
                    atom_activations[atom] /= max_activation

        # 🆕 PHASE 2: Add meta-atom activations (for nexus formation)
        if self.meta_atoms_config:
            meta_activations = self._activate_meta_atoms(patterns, coherence, lure, escalation_detected)
            atom_activations.update(meta_activations)

        return atom_activations

    def _activate_meta_atoms(
        self,
        patterns: List[UrgencyPattern],
        coherence: float,
        lure: float,
        escalation_detected: bool
    ) -> Dict[str, float]:
        """
        🆕 PHASE 2: Activate shared meta-atoms for nexus formation.

        NDAM contributes to 2 meta-atoms:
        1. trauma_aware (BOND, EO, NDAM) - Crisis urgency + escalation
        2. safety_restoration (SANS, EO, NDAM) - Safety language (low urgency)
        """
        if not self.meta_atoms_config:
            return {}

        meta_activations = {}

        # Get urgency patterns by type
        crisis_patterns = [p for p in patterns if p.pattern_type == 'crisis_urgency']
        emotional_patterns = [p for p in patterns if p.pattern_type == 'emotional_intensity']

        # Calculate mean urgency if patterns exist
        mean_urgency = np.mean([p.strength for p in patterns]) if patterns else 0.0

        for meta_atom in self.meta_atoms_config['meta_atoms']:
            atom_name = meta_atom['atom']

            # 1. trauma_aware: Crisis urgency + escalation patterns
            if atom_name == 'trauma_aware':
                if crisis_patterns or emotional_patterns or escalation_detected:
                    # High trauma signals: crisis + emotional intensity + escalation
                    crisis_strength = sum(p.strength * p.confidence for p in crisis_patterns) / len(crisis_patterns) if crisis_patterns else 0.0
                    emotional_strength = sum(p.strength * p.confidence for p in emotional_patterns) / len(emotional_patterns) if emotional_patterns else 0.0
                    escalation_boost = 0.3 if escalation_detected else 0.0

                    base_activation = (crisis_strength + emotional_strength) / 2 + escalation_boost
                    activation = base_activation * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

            # 2. safety_restoration: Low urgency (safety language present)
            elif atom_name == 'safety_restoration':
                if mean_urgency < 0.5 or not patterns:
                    # Safety present when urgency is low or absent
                    safety_strength = 1.0 - mean_urgency  # Invert urgency
                    activation = safety_strength * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

        return meta_activations

    def _compile_keyword_patterns(self):
        """Compile regex patterns for efficient keyword matching."""
        # Group keywords by type for classification
        self.keyword_groups = {
            'crisis_urgency': [
                'urgent', 'crisis', 'emergency', 'critical', 'immediate',
                'escalating', 'breaking down', 'collapse', 'failing'
            ],
            'temporal_pressure': [
                'deadline', 'overdue', 'behind schedule', 'running out', 'too late',
                'time-sensitive', 'now', 'asap', 'right away'
            ],
            'emotional_intensity': [
                'exhausted', 'overwhelmed', 'burned out', 'cant take', 'breaking point',
                'desperate', 'panic', 'anxiety', 'stress'
            ],
            'organizational_dysfunction': [
                'conflict', 'tension', 'blame', 'scapegoat', 'toxic',
                'dysfunction', 'breakdown', 'rupture', 'fragmentation'
            ],
            'firefighter_activation': [
                'must fix', 'have to', 'need to', 'should', 'supposed to',
                'responsibility', 'obligation', 'duty', 'requirement'
            ]
        }

        # Compile regex for each keyword (case-insensitive, word boundaries)
        self.keyword_patterns = {}
        for keyword in self.config.urgency_keywords:
            # Escape special regex characters and add word boundaries
            escaped = re.escape(keyword)
            pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
            self.keyword_patterns[keyword] = pattern

    # ========================================================================
    # 🆕 PHASE C3: EMBEDDING-BASED LURE COMPUTATION (Nov 13, 2025)
    # ========================================================================

    def _ensure_embedding_coordinator(self):
        """Lazy-load embedding coordinator."""
        if self.embedding_coordinator is None:
            from persona_layer.embedding_coordinator import EmbeddingCoordinator
            self.embedding_coordinator = EmbeddingCoordinator()

    def _load_lure_prototypes(self) -> Dict[str, np.ndarray]:
        """Load NDAM lure prototypes from JSON."""
        if self.lure_prototypes is not None:
            return self.lure_prototypes

        import json
        from pathlib import Path

        # Navigate from organs/modular/ndam/core/ up to project root, then to persona_layer
        prototype_path = Path(__file__).parent.parent.parent.parent.parent / 'persona_layer' / 'lure_prototypes.json'

        with open(prototype_path, 'r') as f:
            data = json.load(f)

        category = data['prototypes']['ndam_urgency']
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

    # ========================================================================
    # MAIN PROCESSING METHOD (Universal Organ Interface)
    # ========================================================================

    def process_text_occasions(
        self,
        occasions: List[TextOccasion],
        cycle: int = 1
    ) -> NDAMResult:
        """
        Process text occasions to detect urgency patterns.

        Universal organ method signature following legacy pattern.

        Args:
            occasions: List of TextOccasion entities with text
            cycle: Current processing cycle (for V0 integration)

        Returns:
            NDAMResult with coherence, patterns, and lure
        """
        start_time = time.time()

        # 🆕 PHASE C3: Collect full input text for embedding-based lures
        full_text = ' '.join([occasion.text for occasion in occasions])

        if len(occasions) == 0:
            return self._create_empty_result()

        # Phase 1: Extract text from occasions
        texts = [occ.text for occ in occasions]

        # Phase 2: Detect urgency patterns
        patterns = self._detect_urgency_patterns(occasions, texts)

        # Phase 3: Detect escalation
        escalation_detected = self._detect_escalation(
            patterns,
            self.config.escalation_detection_window
        )

        # Phase 4: Calculate coherence metrics
        coherence_metrics = self._calculate_coherence_metrics(
            patterns,
            escalation_detected,
            len(occasions)
        )

        # Phase 5: Calculate lure (appetition)
        lure = self._calculate_lure(coherence_metrics, patterns)

        # Phase 6: Entity-native prehension (add to occasions)
        self._prehend_occasions_with_affordances(
            occasions,
            patterns,
            coherence_metrics,
            cycle
        )

        # Statistics
        processing_time = (time.time() - start_time) * 1000
        self.total_occasions_processed += len(occasions)
        self.total_patterns_detected += len(patterns)
        self.total_processing_time += processing_time

        # Store patterns for learning
        self.pattern_history.extend(patterns)
        if len(self.pattern_history) > self.config.narrative_history_limit:
            self.pattern_history = self.pattern_history[-self.config.narrative_history_limit:]

        # Determine dominant urgency type
        dominant_type = self._get_dominant_urgency_type(patterns)

        # 🆕 COMPUTE SALIENCE FIELD: Multi-level attention density (urgent/important/exploratory)
        # Temporary keyword-based salience (will be replaced with semantic density + novelty)
        salience_field = {
            'urgent': min(1.0, coherence_metrics['max_urgency']),  # Crisis salience
            'important': coherence_metrics['mean_urgency'],  # Sustained importance
            'exploratory': 1.0 - coherence_metrics['overall_coherence']  # Novelty proxy
        }

        # Normalize salience field
        total_salience = sum(salience_field.values())
        if total_salience > 0:
            salience_field = {k: v / total_salience for k, v in salience_field.items()}
        else:
            salience_field = {'urgent': 0.33, 'important': 0.33, 'exploratory': 0.33}

        # 🆕 PHASE 1: Compute atom activations DIRECTLY (bypass semantic_field_extractor!)
        atom_activations = self._compute_atom_activations(
            patterns, coherence_metrics['overall_coherence'], lure, escalation_detected)

        # 🆕 PHASE C3: Compute embedding-based lure field
        if self.use_embedding_lures and full_text:
            urgency_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to balanced default
            urgency_lure_field = {
                'crisis_imminent': 1.0/7,
                'safety_concern': 1.0/7,
                'escalating_intensity': 1.0/7,
                'stability_present': 1.0/7,
                'harm_risk': 1.0/7,
                'deescalating': 1.0/7,
                'resource_assessment': 1.0/7
            }

        return NDAMResult(
            coherence=coherence_metrics['overall_coherence'],
            patterns=patterns,
            lure=lure,
            processing_time=processing_time,
            mean_urgency=coherence_metrics['mean_urgency'],
            max_urgency=coherence_metrics['max_urgency'],
            escalation_detected=escalation_detected,
            dominant_urgency_type=dominant_type,
            salience_field=salience_field,  # 🆕 SALIENCE FIELD: Multi-level attention density
            occasions_processed=len(occasions),
            keywords_matched=coherence_metrics['keywords_matched'],
            atom_activations=atom_activations,  # 🆕 POPULATED!
            urgency_lure_field=urgency_lure_field  # 🆕 PHASE C3
        )

    # ========================================================================
    # URGENCY DETECTION
    # ========================================================================

    def _detect_urgency_patterns(
        self,
        occasions: List[TextOccasion],
        texts: List[str]
    ) -> List[UrgencyPattern]:
        """
        Detect urgency patterns via keyword matching.

        Args:
            occasions: List of TextOccasion entities
            texts: List of text strings

        Returns:
            List of detected UrgencyPattern objects
        """
        patterns = []

        for i, (occasion, text) in enumerate(zip(occasions, texts)):
            # Find matching keywords in this text
            matched_keywords = []
            for keyword, pattern in self.keyword_patterns.items():
                if pattern.search(text):
                    matched_keywords.append(keyword)

            if len(matched_keywords) == 0:
                continue

            # Classify urgency type based on keywords
            urgency_type = self._classify_urgency_type(matched_keywords)

            # Calculate strength (number of keywords + amplification)
            raw_strength = len(matched_keywords) / 5.0  # Normalize (5 keywords = 1.0)
            amplified_strength = raw_strength * self.config.crisis_amplification

            # Get type-specific settings
            type_settings = self.config.get_urgency_type_settings()[urgency_type]

            # Clamp to min/max for this type
            strength = max(
                type_settings['min_strength'],
                min(type_settings['max_strength'], amplified_strength)
            )

            # Confidence based on keyword density and type
            confidence = min(1.0, raw_strength * 0.8 + 0.2)  # 0.2 base + keyword boost

            # Create pattern
            pattern = UrgencyPattern(
                pattern_type=urgency_type,
                strength=strength,
                chunk_id=occasion.chunk_id,
                matched_keywords=matched_keywords,
                confidence=confidence,
                text_snippet=text[:100],  # First 100 chars for context
                position=occasion.position
            )

            patterns.append(pattern)

        # Limit patterns per conversation
        if len(patterns) > self.config.max_urgency_patterns_per_conversation:
            # Sort by strength descending
            patterns = sorted(patterns, key=lambda p: p.strength, reverse=True)
            patterns = patterns[:self.config.max_urgency_patterns_per_conversation]

        return patterns

    def _classify_urgency_type(self, matched_keywords: List[str]) -> str:
        """
        Classify urgency type based on matched keywords.

        Args:
            matched_keywords: List of matched keyword strings

        Returns:
            Urgency type string
        """
        # Count matches per type
        type_counts = {type_name: 0 for type_name in self.keyword_groups.keys()}

        for keyword in matched_keywords:
            for type_name, keywords in self.keyword_groups.items():
                if keyword.lower() in [k.lower() for k in keywords]:
                    type_counts[type_name] += 1

        # Return type with most matches (or 'narrative_escalation' if tied)
        if sum(type_counts.values()) == 0:
            return 'narrative_escalation'

        max_count = max(type_counts.values())
        for type_name, count in type_counts.items():
            if count == max_count:
                return type_name

        return 'narrative_escalation'

    # ========================================================================
    # ESCALATION DETECTION
    # ========================================================================

    def _detect_escalation(
        self,
        patterns: List[UrgencyPattern],
        window_size: int
    ) -> bool:
        """
        Detect urgency escalation across sentence window.

        Escalation = increasing urgency strength over consecutive sentences.

        Args:
            patterns: List of urgency patterns (with position)
            window_size: Sentence window to check

        Returns:
            True if escalation detected
        """
        if len(patterns) < 2:
            return False

        # Sort by position
        sorted_patterns = sorted(patterns, key=lambda p: p.position)

        # Check for increasing strength in windows
        for i in range(len(sorted_patterns) - 1):
            current = sorted_patterns[i]
            next_pattern = sorted_patterns[i + 1]

            # Within window?
            if next_pattern.position - current.position <= window_size:
                # Increasing strength?
                if next_pattern.strength > current.strength * 1.1:  # 10% increase threshold
                    return True

        return False

    # ========================================================================
    # COHERENCE METRICS
    # ========================================================================

    def _calculate_coherence_metrics(
        self,
        patterns: List[UrgencyPattern],
        escalation_detected: bool,
        total_occasions: int
    ) -> Dict[str, float]:
        """
        Calculate urgency coherence metrics.

        Args:
            patterns: Detected patterns
            escalation_detected: Whether escalation found
            total_occasions: Total occasions processed

        Returns:
            Dictionary of coherence metrics
        """
        if len(patterns) == 0:
            return {
                'overall_coherence': 0.0,
                'mean_urgency': 0.0,
                'max_urgency': 0.0,
                'keywords_matched': 0
            }

        # Basic statistics
        strengths = [p.strength for p in patterns]
        mean_urgency = float(np.mean(strengths))
        max_urgency = float(np.max(strengths))
        std_urgency = float(np.std(strengths)) if len(strengths) > 1 else 0.0

        # Pattern density (patterns per occasion)
        pattern_density = len(patterns) / max(1, total_occasions)

        # Urgency coherence (how consistent are urgency levels)
        # High coherence = high mean + low std (consistent urgency)
        urgency_coherence = mean_urgency * (1.0 - min(1.0, std_urgency / 2.0))

        # Escalation bonus
        escalation_bonus = 0.2 if escalation_detected else 0.0

        # Overall coherence (weighted combination)
        overall_coherence = (
            0.4 * urgency_coherence +
            0.3 * pattern_density +
            0.2 * (mean_urgency / 2.0) +  # Normalize to 0-1 (max strength = 2.0)
            0.1 + escalation_bonus
        )

        # Count total keywords matched
        keywords_matched = sum(len(p.matched_keywords) for p in patterns)

        return {
            'overall_coherence': min(1.0, overall_coherence),
            'mean_urgency': mean_urgency,
            'max_urgency': max_urgency,
            'keywords_matched': keywords_matched
        }

    # ========================================================================
    # LURE CALCULATION (Appetition)
    # ========================================================================

    def _calculate_lure(
        self,
        coherence_metrics: Dict[str, float],
        patterns: List[UrgencyPattern]
    ) -> float:
        """
        Calculate appetition lure strength.

        High lure when:
        - Strong urgency patterns detected
        - High pattern confidence
        - Multiple high-urgency patterns

        Args:
            coherence_metrics: Coherence metrics
            patterns: Detected patterns

        Returns:
            Lure strength (0-1)
        """
        if len(patterns) == 0:
            return 0.0

        # Pattern strength (number and urgency)
        pattern_count_factor = min(1.0, len(patterns) / 5.0)  # Saturate at 5
        mean_pattern_strength = coherence_metrics['mean_urgency'] / 2.0  # Normalize

        # Confidence factor
        mean_confidence = np.mean([p.confidence for p in patterns])

        # Overall lure (weighted combination)
        lure = (
            0.4 * mean_pattern_strength +
            0.3 * mean_confidence +
            0.3 * pattern_count_factor
        )

        return min(1.0, lure)

    # ========================================================================
    # ENTITY-NATIVE PREHENSION
    # ========================================================================

    def _prehend_occasions_with_affordances(
        self,
        occasions: List[TextOccasion],
        patterns: List[UrgencyPattern],
        coherence_metrics: Dict[str, float],
        cycle: int
    ):
        """
        Add prehensions and felt affordances to text occasions.

        Args:
            occasions: List of TextOccasion entities (modified in-place)
            patterns: Detected patterns
            coherence_metrics: Coherence metrics
            cycle: Current cycle number
        """
        # Create organ output for prehension
        organ_output = {
            'coherence': coherence_metrics['overall_coherence'],
            'patterns': [
                {
                    'type': p.pattern_type,
                    'strength': p.strength,
                    'confidence': p.confidence,
                    'keywords': p.matched_keywords
                }
                for p in patterns
            ],
            'lure': self._calculate_lure(coherence_metrics, patterns),
            'processing_time': 0.0  # Updated by caller
        }

        # Add prehension to all occasions
        for occ in occasions:
            occ.add_organ_prehension('NDAM', organ_output, cycle)

        # Add felt affordances for high-confidence patterns
        for pattern in patterns:
            if pattern.confidence >= 0.7:
                # Find occasion containing this pattern
                occ = next((o for o in occasions if o.chunk_id == pattern.chunk_id), None)

                if occ:
                    occ.add_felt_affordance(
                        organ_name='NDAM',
                        confidence=pattern.confidence,
                        lure_intensity=pattern.strength / 2.0,  # Normalize to 0-1
                        pattern_type=pattern.pattern_type,
                        affordance_data={
                            'matched_keywords': pattern.matched_keywords,
                            'strength': pattern.strength
                        }
                    )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _create_empty_result(self) -> NDAMResult:
        """Create empty result for edge case."""
        return NDAMResult(
            coherence=0.0,
            patterns=[],
            lure=0.0,
            processing_time=0.0,
            salience_field={'urgent': 0.33, 'important': 0.33, 'exploratory': 0.33},  # 🆕 Balanced default
            occasions_processed=0,
            keywords_matched=0
        )

    def _get_dominant_urgency_type(self, patterns: List[UrgencyPattern]) -> Optional[str]:
        """Get most common urgency type."""
        if len(patterns) == 0:
            return None

        type_counts = {}
        for pattern in patterns:
            type_counts[pattern.pattern_type] = type_counts.get(pattern.pattern_type, 0) + 1

        return max(type_counts, key=type_counts.get)

    def get_organ_config(self) -> Dict[str, Any]:
        """Get organ configuration for introspection."""
        return {
            'organ_name': 'NDAM',
            'version': '1.0',
            'domain': 'text',
            'llm_free': True,
            'urgency_threshold': self.config.urgency_threshold,
            'keywords_count': len(self.config.urgency_keywords),
            'escalation_window': self.config.escalation_detection_window,
            'patterns_detected': self.total_patterns_detected,
            'occasions_processed': self.total_occasions_processed
        }

    def get_hebbian_learning_config(self) -> Dict[str, Any]:
        """Get Hebbian learning configuration."""
        return self.config.get_hebbian_learning_config()

    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'total_occasions_processed': self.total_occasions_processed,
            'total_patterns_detected': self.total_patterns_detected,
            'total_processing_time_ms': self.total_processing_time,
            'avg_processing_time_ms': (
                self.total_processing_time / max(1, self.total_occasions_processed)
            ),
            'patterns_per_occasion': (
                self.total_patterns_detected / max(1, self.total_occasions_processed)
            )
        }


if __name__ == "__main__":
    """
    Validation test for NDAM text-native organ.
    """
    print("🧪 NDAM Text Core Validation Test")
    print("=" * 60)

    # Create NDAM organ
    ndam = NDAMTextCore()

    # Create sample text occasions with urgency keywords
    print("\n📝 Creating sample text occasions...")

    sample_texts = [
        "The board expressed concern about escalating conflicts in the leadership team.",  # crisis
        "Executive burnout patterns are creating urgent need for intervention.",  # crisis + temporal
        "We need to establish healthy boundaries and self-care practices.",  # low urgency
        "The deadline is overdue and tensions are rising in the organization.",  # temporal + emotional
        "This is a breaking point - we must fix the dysfunction immediately.",  # crisis + firefighter
    ]

    occasions = []
    for i, text in enumerate(sample_texts):
        # Create dummy 384-dim embedding
        embedding = np.random.randn(384)
        embedding /= np.linalg.norm(embedding)

        occasion = TextOccasion(
            chunk_id=f"doc_1_chunk_{i+1}",
            position=i,
            text=text,
            embedding=embedding
        )
        occasions.append(occasion)

    print(f"✅ Created {len(occasions)} text occasions")

    # Process with NDAM
    print("\n🔍 Processing with NDAM organ...")
    result = ndam.process_text_occasions(occasions, cycle=1)

    # Display results
    print(f"\n📊 NDAM Results:")
    print(f"   Coherence: {result.coherence:.3f}")
    print(f"   Lure: {result.lure:.3f}")
    print(f"   Patterns detected: {len(result.patterns)}")
    print(f"   Mean urgency: {result.mean_urgency:.3f}")
    print(f"   Max urgency: {result.max_urgency:.3f}")
    print(f"   Escalation detected: {result.escalation_detected}")
    print(f"   Dominant type: {result.dominant_urgency_type}")
    print(f"   Keywords matched: {result.keywords_matched}")
    print(f"   Processing time: {result.processing_time:.1f}ms")

    # Display patterns
    if len(result.patterns) > 0:
        print(f"\n⚠️  Detected Urgency Patterns:")
        for i, pattern in enumerate(result.patterns, 1):
            print(f"   {i}. {pattern.pattern_type}")
            print(f"      Strength: {pattern.strength:.3f}")
            print(f"      Confidence: {pattern.confidence:.3f}")
            print(f"      Keywords: {', '.join(pattern.matched_keywords[:5])}")
            print(f"      Text: {pattern.text_snippet}...")
            print()

    # Check prehensions
    print(f"🧠 Prehension Check:")
    occ = occasions[0]
    if 'NDAM' in occ.prehensions:
        print(f"   ✅ Occasion 0 has NDAM prehension")
        print(f"   Affordances: {len(occ.felt_affordances)}")

    # Statistics
    stats = ndam.get_statistics()
    print(f"\n📈 NDAM Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n✅ ALL TESTS PASSED - NDAM operational")
