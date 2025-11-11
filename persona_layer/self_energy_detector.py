"""
SELF-Energy Detector (Embedding-Based BOND Extension)

Extends existing BOND organ with embedding-based SELF-energy detection.

Architecture Strategy:
- WRAP existing BOND organ (don't replace 120+ keywords)
- BOOST keyword detection with embedding similarity to 8 C's patterns
- LEARN through Hebbian memory (SELF-energy language expands organically)
- BAGUA-modulate for fluid part transitions (not rigid classifications)

Integration:
- Works WITH bond_text_core.py (extends, doesn't replace)
- Adds embedding similarity to 8 C's: Compassion, Curiosity, Clarity, Calm,
  Confidence, Courage, Creativity, Connectedness
- Seeds from I Ching corpus for SELF-led language
- Hebbian expansion from successful SELF-energy detections

Source:
- DAE-GOV Persona Layer Architecture Addendum (Phase 1.2d)
- IFS Model (Schwartz) - SELF as unburdened core essence
- BOND organ (bond_text_core.py) - IFS parts detection

Author: DAE-GOV Development Team
Date: November 10, 2025
"""

from typing import Dict, Any, List, Optional
import numpy as np
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer


@dataclass
class SELFEnergyDetection:
    """
    Detected SELF-energy level with 8 C's breakdown.

    Fields:
        self_energy: [0,1] overall SELF-energy level (1.0 = pure SELF)
        self_distance: [0,1] distance from SELF (inverse of energy)
        cs_activation: Dict of 8 C's activation levels
        dominant_c: Which C is most present
        confidence: [0,1] confidence in detection
        keywords_matched: Keywords from BOND that contributed
        embedding_contribution: How much embedding vs keyword influenced
    """
    self_energy: float
    self_distance: float
    cs_activation: Dict[str, float]  # 8 C's individual levels
    dominant_c: str
    confidence: float
    keywords_matched: List[str]
    embedding_contribution: float


class SELFEnergyDetector:
    """
    Embedding-based SELF-energy detection extending BOND organ.

    The 8 C's (from IFS - Schwartz):
    1. Compassion - caring, kindness toward self and parts
    2. Curiosity - interest, wonder about what's happening
    3. Clarity - clear seeing, understanding
    4. Calm - peaceful, settled, grounded
    5. Confidence - trust in self, capable
    6. Courage - willingness, brave to be with what is
    7. Creativity - imagination, possibility
    8. Connectedness - relationship, belonging, togetherness

    Strategy:
    1. SEED from 8 C's phrases (not exhaustive lists)
    2. LEARN embedding clusters through Hebbian memory
    3. BLEND keyword + embedding signals (weighted combination)
    4. BAGUA-modulate for creative exploration
    """

    def __init__(
        self,
        embedding_model: Optional[SentenceTransformer] = None,
        hebbian_memory_path: Optional[str] = None
    ):
        """
        Initialize SELF-energy detector with embedding model.

        Args:
            embedding_model: Sentence transformer (384-dim, same as BOND)
            hebbian_memory_path: Path to Hebbian memory for learned patterns
        """
        # Embedding model (384-dim, same as existing organs)
        if embedding_model is None:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = embedding_model

        # Hebbian memory for learned SELF-energy patterns
        self.hebbian_memory_path = hebbian_memory_path
        self.learned_embeddings = self._load_learned_embeddings()

        # Initialize 8 C's embeddings (seed clusters)
        self.eight_cs_embeddings = self._initialize_eight_cs_embeddings()

        # BAGUA modulation config
        self.bagua_config = {
            'lake_joy_threshold': 0.6,   # Lateral blending threshold
            'creative_force_threshold': 0.25,  # Creative exploration boost
            'mountain_stability': 0.4    # Hold tension at edges
        }

    def _default_eight_cs_seeds(self) -> Dict[str, List[str]]:
        """
        Default seed phrases for 8 C's.

        These are SEEDS, not exhaustive. Hebbian learning expands organically.
        Sourced from IFS literature and I Ching wisdom language.
        """
        return {
            'compassion': [
                "I feel care and kindness toward this part of me",
                "There's tenderness and warmth here",
                "Holding this with compassion",
                "Caring for what's hurt",
                "Gentle kindness toward myself"
            ],
            'curiosity': [
                "I'm curious about what's happening",
                "Wonder what this part needs",
                "Interested to explore this more",
                "Asking with genuine curiosity",
                "Open to discovering what's here"
            ],
            'clarity': [
                "I can see clearly what's happening",
                "Understanding is emerging",
                "The pattern is clear now",
                "Recognizing what's true",
                "Seeing with clear eyes"
            ],
            'calm': [
                "I feel settled and peaceful",
                "There's a calm spaciousness",
                "Grounded and at ease",
                "Peaceful presence here",
                "Settled into the moment"
            ],
            'confidence': [
                "I trust myself with this",
                "Feel capable and strong",
                "Confidence in my ability",
                "Trust in the process",
                "Capable of being with what is"
            ],
            'courage': [
                "I'm willing to be with this",
                "Brave enough to stay present",
                "Courageous to face what's here",
                "Dare to feel this fully",
                "Willing to go toward difficulty"
            ],
            'creativity': [
                "I can imagine new possibilities",
                "Creative solutions emerging",
                "Vision of what could be",
                "Playful exploration",
                "Fresh perspective appearing"
            ],
            'connectedness': [
                "I feel connected to myself",
                "Sense of belonging here",
                "Together with these parts",
                "Relationship and wholeness",
                "United, not fragmented"
            ]
        }

    def _initialize_eight_cs_embeddings(self) -> Dict[str, np.ndarray]:
        """
        Initialize seed embeddings for each of the 8 C's.

        Returns:
            Dict mapping C-name → centroid embedding (384-dim)
        """
        seeds = self._default_eight_cs_seeds()
        eight_cs_embeddings = {}

        for c_name, seed_phrases in seeds.items():
            # Encode all seed phrases
            embeddings = self.embedding_model.encode(
                seed_phrases,
                convert_to_numpy=True
            )

            # Compute centroid (initial cluster center)
            centroid = np.mean(embeddings, axis=0)
            centroid = centroid / np.linalg.norm(centroid)  # L2 normalize

            eight_cs_embeddings[c_name] = centroid

        return eight_cs_embeddings

    def _load_learned_embeddings(self) -> Dict[str, List[np.ndarray]]:
        """
        Load learned SELF-energy patterns from Hebbian memory.

        Returns:
            Dict mapping C-name → list of learned embedding patterns

        Future: Integrate with TSK/hebbian_memory.json
        """
        # TODO: Load from Hebbian memory JSON
        # For now, return empty (will accumulate through epochs)
        return {c: [] for c in ['compassion', 'curiosity', 'clarity', 'calm',
                                 'confidence', 'courage', 'creativity', 'connectedness']}

    def _compute_c_similarity(
        self,
        text_embedding: np.ndarray,
        c_name: str
    ) -> float:
        """
        Compute cosine similarity to a specific C embedding cluster.

        Uses BOTH seed centroid AND learned patterns (weighted combination).

        Args:
            text_embedding: 384-dim embedding of input text
            c_name: Name of C ('compassion', 'curiosity', etc.)

        Returns:
            Similarity score [0,1] (cosine similarity normalized)
        """
        # Seed centroid similarity
        seed_embedding = self.eight_cs_embeddings[c_name]
        seed_sim = np.dot(text_embedding, seed_embedding)

        # Learned patterns similarity (if any)
        learned_patterns = self.learned_embeddings.get(c_name, [])
        if learned_patterns:
            learned_sims = [np.dot(text_embedding, pattern) for pattern in learned_patterns]
            max_learned_sim = max(learned_sims)

            # Weighted combination (70% seed, 30% learned initially)
            # Balance shifts toward learned over epochs
            weight_seed = 0.7 - (len(learned_patterns) * 0.01)  # Decrease with learning
            weight_learned = 1.0 - weight_seed

            combined_sim = weight_seed * seed_sim + weight_learned * max_learned_sim
        else:
            combined_sim = seed_sim

        # Normalize to [0,1] (cosine is [-1,1])
        return float((combined_sim + 1.0) / 2.0)

    def detect_self_energy(
        self,
        text: str,
        bond_keywords: Optional[List[str]] = None,
        bagua_context: Optional[Dict[str, float]] = None
    ) -> SELFEnergyDetection:
        """
        Detect SELF-energy level from conversational text.

        Args:
            text: User input text
            bond_keywords: Keywords matched by BOND organ (for blending)
            bagua_context: BAGUA activation (Lake Joy, Creative Force, etc.)

        Returns:
            SELFEnergyDetection with energy level, 8 C's breakdown, confidence

        Algorithm:
            1. Encode text to 384-dim embedding
            2. Compute similarity to each of 8 C's
            3. Aggregate to overall SELF-energy level
            4. BLEND with BOND keyword signal (if provided)
            5. BAGUA-modulate if creative exploration active
            6. Return detection with full context

        Example:
            >>> detector = SELFEnergyDetector()
            >>> detection = detector.detect_self_energy(
            ...     "I'm feeling compassion and curiosity toward this hurt part."
            ... )
            >>> detection.self_energy
            0.78  # High SELF-energy
            >>> detection.dominant_c
            'compassion'
        """
        # Step 1: Encode text to embedding
        text_embedding = self.embedding_model.encode(
            text,
            convert_to_numpy=True
        )
        text_embedding = text_embedding / np.linalg.norm(text_embedding)  # L2 normalize

        # Step 2: Compute similarity to each of 8 C's
        cs_activation = {}
        for c_name in self.eight_cs_embeddings.keys():
            cs_activation[c_name] = self._compute_c_similarity(text_embedding, c_name)

        # Step 3: Aggregate to overall SELF-energy
        # SELF-energy = mean of top 3 activated C's (not all 8)
        # Rationale: SELF doesn't require ALL C's, just strong presence of a few
        top_3_cs = sorted(cs_activation.values(), reverse=True)[:3]
        embedding_based_energy = np.mean(top_3_cs)

        # Step 4: BLEND with BOND keyword signal (if provided)
        if bond_keywords:
            # BOND already detected SELF keywords → boost embedding signal
            keyword_boost = min(len(bond_keywords) / 5.0, 0.2)  # Up to +0.2 for 5+ keywords
            blended_energy = embedding_based_energy + keyword_boost
            embedding_contribution = 0.7  # 70% embedding, 30% keyword
        else:
            blended_energy = embedding_based_energy
            embedding_contribution = 1.0  # 100% embedding

        # Step 5: BAGUA modulation (if context provided)
        if bagua_context:
            creative_force = bagua_context.get('creative_force', 0.0)
            lake_joy = bagua_context.get('lake_joy', 0.0)

            # Creative Force: Boost minority C's for exploration
            if creative_force > self.bagua_config['creative_force_threshold']:
                min_c_name = min(cs_activation, key=cs_activation.get)
                cs_activation[min_c_name] += creative_force * 0.15  # Up to 15% boost

            # Lake Joy: Soften boundaries between C's
            if lake_joy > self.bagua_config['lake_joy_threshold']:
                # Flatten distribution slightly
                cs_array = np.array(list(cs_activation.values()))
                flattened = cs_array ** 0.8  # Softer peaks
                cs_activation = {c: flattened[i] for i, c in enumerate(cs_activation.keys())}

        # Clamp SELF-energy to [0,1]
        final_energy = np.clip(blended_energy, 0.0, 1.0)
        self_distance = 1.0 - final_energy

        # Determine dominant C
        dominant_c = max(cs_activation, key=cs_activation.get)

        # Compute confidence (inverse entropy of C distribution)
        cs_array = np.array(list(cs_activation.values()))
        cs_probs = cs_array / cs_array.sum()  # Normalize to probabilities
        entropy = -np.sum(cs_probs * np.log(cs_probs + 1e-10))
        max_entropy = np.log(8.0)  # Maximum for 8 categories
        confidence = 1.0 - (entropy / max_entropy)

        return SELFEnergyDetection(
            self_energy=float(final_energy),
            self_distance=float(self_distance),
            cs_activation=cs_activation,
            dominant_c=dominant_c,
            confidence=float(confidence),
            keywords_matched=bond_keywords or [],
            embedding_contribution=embedding_contribution
        )

    def boost_bond_detection(
        self,
        bond_result: Dict[str, Any],
        text: str,
        bagua_context: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Boost BOND organ detection with embedding-based SELF-energy.

        Args:
            bond_result: Output from BOND organ's process_text_occasions()
            text: Original input text
            bagua_context: BAGUA activation context

        Returns:
            Enhanced BOND result with embedding-boosted SELF-energy

        Example:
            >>> bond_result = bond_organ.process_text_occasions(occasions)
            >>> enhanced = detector.boost_bond_detection(bond_result, text)
            >>> enhanced['self_energy_embedding']
            0.78  # Embedding-based boost
        """
        # Extract BOND keywords for SELF-energy (if available)
        bond_keywords = bond_result.get('self_energy_keywords', [])

        # Detect SELF-energy with embedding + BOND keyword blend
        detection = self.detect_self_energy(text, bond_keywords, bagua_context)

        # Add embedding-based signals to BOND result
        bond_result['self_energy_embedding'] = detection.self_energy
        bond_result['self_distance_embedding'] = detection.self_distance
        bond_result['eight_cs_activation'] = detection.cs_activation
        bond_result['dominant_c'] = detection.dominant_c
        bond_result['self_energy_confidence'] = detection.confidence
        bond_result['embedding_contribution'] = detection.embedding_contribution

        # BLEND BOND's keyword-based SELF-distance with embedding-based
        # Use embedding as primary, keyword as verification
        if 'mean_self_distance' in bond_result:
            keyword_distance = bond_result['mean_self_distance']
            embedding_distance = detection.self_distance

            # Weighted average (70% embedding, 30% keyword)
            blended_distance = 0.7 * embedding_distance + 0.3 * keyword_distance
            bond_result['self_distance_blended'] = blended_distance
        else:
            bond_result['self_distance_blended'] = detection.self_distance

        return bond_result

    def update_learned_patterns(
        self,
        text: str,
        dominant_c: str,
        satisfaction: float
    ):
        """
        Update learned 8 C's embeddings through Hebbian reinforcement.

        Call this AFTER organism reaches satisfaction on a conversational turn.

        Args:
            text: Text that led to successful SELF-led response
            dominant_c: Which C was most present ('compassion', 'curiosity', etc.)
            satisfaction: Satisfaction score [0,1] (from V0 convergence)

        Future Integration:
        - Store in TSK/hebbian_memory.json
        - Hebbian coupling with BOND organ keywords
        - Cluster learning per conversational family
        """
        if satisfaction < 0.7:
            return  # Only learn from high-satisfaction SELF-led turns

        # Encode text
        text_embedding = self.embedding_model.encode(
            text,
            convert_to_numpy=True
        )
        text_embedding = text_embedding / np.linalg.norm(text_embedding)

        # Add to learned patterns for dominant C
        if dominant_c in self.learned_embeddings:
            self.learned_embeddings[dominant_c].append(text_embedding)

        # TODO: Persist to Hebbian memory
        # self._save_to_hebbian_memory(dominant_c, text_embedding)


# Quick utility functions
def quick_self_energy_check(text: str) -> float:
    """
    Quick SELF-energy level detection (convenience function).

    Args:
        text: User input text

    Returns:
        SELF-energy level [0,1] (1.0 = pure SELF)

    Example:
        >>> quick_self_energy_check("I feel compassion for this hurt part.")
        0.78  # High SELF-energy
    """
    detector = SELFEnergyDetector()
    detection = detector.detect_self_energy(text)
    return detection.self_energy


def is_self_led(text: str, threshold: float = 0.6) -> bool:
    """
    Check if text is SELF-led (sufficient SELF-energy present).

    Args:
        text: User input text
        threshold: SELF-energy threshold for safety

    Returns:
        True if SELF-energy >= threshold

    Example:
        >>> is_self_led("I'm curious about this exile.")
        True  # SELF-led with curiosity

        >>> is_self_led("I'm worthless and broken.")
        False  # Exile without SELF = not led
    """
    detector = SELFEnergyDetector()
    detection = detector.detect_self_energy(text)
    return detection.self_energy >= threshold
