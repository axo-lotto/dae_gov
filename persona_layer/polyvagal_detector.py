"""
Polyvagal State Detector (Embedding-Based)

Extends EO organ config for trauma-informed safety detection in text domain.

Architecture Strategy:
- SEED from existing keywords (not replace)
- LEARN through embedding similarity (not hard-code)
- BAGUA-modulate for lateral blending (not rigid)
- HEBBIAN-expand organically over epochs

Integration:
- Works WITH eo_text_config.py (seeds polyvagal patterns)
- Extends through embedding space (384-dim similarity)
- OFEL consumes detected states for safety boundaries

Source:
- DAE-GOV Persona Layer Architecture Addendum (Phase 1.2c)
- Polyvagal Theory (Porges, 2011) - ventral/sympathetic/dorsal
- BAGUA modulation for curiosity/intervention timing

Author: DAE-GOV Development Team
Date: November 10, 2025
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer


@dataclass
class PolyvagalDetection:
    """
    Detected polyvagal state with confidence and mixed activation.

    Fields:
        dominant_state: Primary state ("ventral", "sympathetic", "dorsal")
        confidence: [0,1] confidence in dominant state
        mixed_activation: Probabilities for all three states
        coherence: [0,1] clarity of state (inverse entropy)
        keywords_matched: Keywords that contributed to detection
        embedding_contribution: How much embedding vs keyword influenced
    """
    dominant_state: str
    confidence: float
    mixed_activation: Dict[str, float]
    coherence: float
    keywords_matched: List[str]
    embedding_contribution: float  # [0,1] embedding vs keyword weight


class PolyvagalDetector:
    """
    Embedding-based polyvagal state detection for trauma-informed safety.

    Strategy:
    1. SEED from eo_text_config keywords (initial patterns)
    2. LEARN embedding clusters through Hebbian memory
    3. BAGUA-modulate at bifurcation edges (Lake Joy lateral blending)
    4. EXPAND organically through conversation epochs

    Key Principle: NOT rigid keyword matching, but fluid embedding similarity
    that learns and adapts through interaction.
    """

    def __init__(
        self,
        embedding_model: Optional[SentenceTransformer] = None,
        seed_config: Optional[Dict[str, Any]] = None,
        hebbian_memory_path: Optional[str] = None
    ):
        """
        Initialize polyvagal detector with embedding model.

        Args:
            embedding_model: Sentence transformer for text embeddings
                            (default: all-MiniLM-L6-v2, 384-dim)
            seed_config: Optional seed patterns from eo_text_config
            hebbian_memory_path: Path to Hebbian memory for learned patterns
        """
        # Embedding model (384-dim, same as existing organs)
        if embedding_model is None:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = embedding_model

        # Seed from existing config if provided
        self.seed_config = seed_config or self._default_seed_config()

        # Hebbian memory for learned patterns
        self.hebbian_memory_path = hebbian_memory_path
        self.learned_embeddings = self._load_learned_embeddings()

        # State embeddings (seed clusters)
        self.state_embeddings = self._initialize_state_embeddings()

        # BAGUA modulation config
        self.bagua_config = {
            'lake_joy_threshold': 0.6,  # When to activate lateral blending
            'blending_exponent': 0.7,   # How much to flatten distribution
            'creative_boost': 0.25      # Creative Force for abstraction
        }

    def _default_seed_config(self) -> Dict[str, List[str]]:
        """
        Default seed patterns from polyvagal theory.

        These are SEEDS, not exhaustive lists. They bootstrap embedding space,
        then Hebbian learning expands organically.
        """
        return {
            'ventral': [
                # Connection & safety
                "I feel safe and connected",
                "There's a sense of ease and openness",
                "I'm curious and engaged",
                "Feeling grounded and present",
                "Compassion and warmth",
                # Calm & clarity
                "Clear and calm energy",
                "Relaxed and receptive",
                "Peaceful and settled",
                "Breathing deeply, spacious",
                "Creative and confident"
            ],
            'sympathetic': [
                # Urgency & pressure
                "Feeling overwhelmed and urgent",
                "There's pressure and deadline stress",
                "Anxiety and worry",
                "Need to hurry and rush",
                "Too much to handle",
                # Anger & fight
                "Frustrated and irritated",
                "Defensive and reactive",
                "Fight or flight energy",
                "Tense and braced",
                "Alert and vigilant"
            ],
            'dorsal': [
                # Shutdown & collapse
                "Feeling numb and shut down",
                "Hopeless and defeated",
                "Giving up and collapsing",
                "Heavy and immobile",
                "Stuck and frozen",
                # Dissociation
                "Disconnected and far away",
                "Foggy and hazy",
                "Floating and detached",
                "Exhausted and depleted",
                "Nothing left, empty"
            ]
        }

    def _initialize_state_embeddings(self) -> Dict[str, np.ndarray]:
        """
        Initialize seed embeddings for each polyvagal state.

        Computes centroid of seed phrases in 384-dim embedding space.
        These will be updated through Hebbian learning over epochs.
        """
        state_embeddings = {}

        for state_name, seed_phrases in self.seed_config.items():
            # Encode all seed phrases
            embeddings = self.embedding_model.encode(
                seed_phrases,
                convert_to_numpy=True
            )

            # Compute centroid (initial cluster center)
            centroid = np.mean(embeddings, axis=0)
            centroid = centroid / np.linalg.norm(centroid)  # L2 normalize

            state_embeddings[state_name] = centroid

        return state_embeddings

    def _load_learned_embeddings(self) -> Dict[str, List[np.ndarray]]:
        """
        Load learned polyvagal patterns from Hebbian memory.

        Returns:
            Dict mapping state_name → list of learned embedding patterns

        Future: Integrate with TSK/hebbian_memory.json for accumulation
        """
        # TODO: Load from Hebbian memory JSON
        # For now, return empty (will accumulate through epochs)
        return {
            'ventral': [],
            'sympathetic': [],
            'dorsal': []
        }

    def _compute_embedding_similarity(
        self,
        text_embedding: np.ndarray,
        state_name: str
    ) -> float:
        """
        Compute cosine similarity to polyvagal state embedding cluster.

        Uses BOTH seed centroid AND learned patterns (weighted combination).

        Args:
            text_embedding: 384-dim embedding of input text
            state_name: "ventral", "sympathetic", or "dorsal"

        Returns:
            Similarity score [0,1] (cosine similarity normalized)
        """
        # Seed centroid similarity
        seed_embedding = self.state_embeddings[state_name]
        seed_sim = np.dot(text_embedding, seed_embedding)

        # Learned patterns similarity (if any)
        learned_patterns = self.learned_embeddings.get(state_name, [])
        if learned_patterns:
            learned_sims = [np.dot(text_embedding, pattern) for pattern in learned_patterns]
            max_learned_sim = max(learned_sims)

            # Weighted combination (70% seed, 30% learned initially)
            # This balance shifts toward learned over epochs
            weight_seed = 0.7 - (len(learned_patterns) * 0.01)  # Decrease with learning
            weight_learned = 1.0 - weight_seed

            combined_sim = weight_seed * seed_sim + weight_learned * max_learned_sim
        else:
            combined_sim = seed_sim

        # Normalize to [0,1] (cosine is [-1,1])
        return float((combined_sim + 1.0) / 2.0)

    def _apply_bagua_modulation(
        self,
        raw_probs: np.ndarray,
        bagua_context: Optional[Dict[str, float]] = None
    ) -> np.ndarray:
        """
        Apply BAGUA modulation for lateral blending and creative exploration.

        Args:
            raw_probs: Raw probabilities [ventral, sympathetic, dorsal]
            bagua_context: BAGUA activation context (Lake Joy, Creative Force, etc.)

        Returns:
            Modulated probabilities (still sum to 1.0)

        BAGUA Modulation:
        - Lake Joy (dim 32): Lateral blending, soften rigid boundaries
        - Creative Force: Abstract exploration beyond templates
        - Mountain: Hold tension at bifurcation edges
        """
        if bagua_context is None:
            return raw_probs

        lake_joy = bagua_context.get('lake_joy', 0.0)
        creative_force = bagua_context.get('creative_force', 0.0)

        # Lake Joy: Flatten distribution (lateral blending)
        if lake_joy > self.bagua_config['lake_joy_threshold']:
            blending_exp = self.bagua_config['blending_exponent']
            modulated_probs = raw_probs ** blending_exp
            modulated_probs /= modulated_probs.sum()  # Renormalize
        else:
            modulated_probs = raw_probs

        # Creative Force: Boost minority state for exploration
        if creative_force > self.bagua_config['creative_boost']:
            min_idx = np.argmin(modulated_probs)
            boost = creative_force * 0.15  # Up to 15% boost
            modulated_probs[min_idx] += boost
            modulated_probs /= modulated_probs.sum()  # Renormalize

        return modulated_probs

    def detect_polyvagal_state(
        self,
        text: str,
        bagua_context: Optional[Dict[str, float]] = None
    ) -> PolyvagalDetection:
        """
        Detect polyvagal state from conversational text.

        Args:
            text: User input text (message, query, etc.)
            bagua_context: Optional BAGUA activation (from Vector35D dims 25-32)

        Returns:
            PolyvagalDetection with state, confidence, mixed activation

        Algorithm:
            1. Encode text to 384-dim embedding
            2. Compute similarity to each state cluster
            3. Softmax to get probabilities (not rigid classification)
            4. BAGUA-modulate if Lake Joy/Creative Force active
            5. Determine dominant state and coherence
            6. Return detection with full context

        Example:
            >>> detector = PolyvagalDetector()
            >>> detection = detector.detect_polyvagal_state(
            ...     "I feel overwhelmed and anxious about this deadline."
            ... )
            >>> detection.dominant_state
            'sympathetic'
            >>> detection.confidence
            0.78  # High confidence in mobilization
        """
        # Step 1: Encode text to embedding
        text_embedding = self.embedding_model.encode(
            text,
            convert_to_numpy=True
        )
        text_embedding = text_embedding / np.linalg.norm(text_embedding)  # L2 normalize

        # Step 2: Compute similarity to each state
        ventral_sim = self._compute_embedding_similarity(text_embedding, 'ventral')
        sympathetic_sim = self._compute_embedding_similarity(text_embedding, 'sympathetic')
        dorsal_sim = self._compute_embedding_similarity(text_embedding, 'dorsal')

        # Step 3: Softmax to get probabilities
        raw_sims = np.array([ventral_sim, sympathetic_sim, dorsal_sim])
        exp_sims = np.exp(raw_sims * 5.0)  # Temperature=5 for sharper peaks
        raw_probs = exp_sims / exp_sims.sum()

        # Step 4: BAGUA modulation (if context provided)
        modulated_probs = self._apply_bagua_modulation(raw_probs, bagua_context)

        # Step 5: Determine dominant state
        state_names = ['ventral', 'sympathetic', 'dorsal']
        dominant_idx = np.argmax(modulated_probs)
        dominant_state = state_names[dominant_idx]
        confidence = float(modulated_probs[dominant_idx])

        # Step 6: Compute coherence (inverse entropy)
        entropy = -np.sum(modulated_probs * np.log(modulated_probs + 1e-10))
        max_entropy = np.log(3.0)  # Maximum for 3 states
        coherence = 1.0 - (entropy / max_entropy)

        # Step 7: Mixed activation dict
        mixed_activation = {
            state_names[i]: float(modulated_probs[i])
            for i in range(3)
        }

        # Step 8: Embedding contribution (100% for now, will blend with keywords later)
        embedding_contribution = 1.0

        return PolyvagalDetection(
            dominant_state=dominant_state,
            confidence=confidence,
            mixed_activation=mixed_activation,
            coherence=coherence,
            keywords_matched=[],  # Future: integrate with eo_text_config keywords
            embedding_contribution=embedding_contribution
        )

    def prehend_text(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        FFITTSS-compatible prehension interface.

        Args:
            text: User input text
            context: Optional context with BAGUA activation

        Returns:
            Organ output dictionary for OFEL integration

        Example:
            >>> detector = PolyvagalDetector()
            >>> output = detector.prehend_text("I feel safe and curious.")
            >>> output['polyvagal_state']
            'ventral'
            >>> output['coherence']
            0.85
        """
        # Extract BAGUA context if provided
        bagua_context = None
        if context and 'bagua_activation' in context:
            bagua_context = context['bagua_activation']

        # Detect polyvagal state
        detection = self.detect_polyvagal_state(text, bagua_context)

        # Map to OFEL-compatible penalty (for E_polyvagal computation)
        polyvagal_penalties = {
            'ventral': 0.0,      # Safe, no exclusion
            'sympathetic': 0.3,  # Caution
            'dorsal': 0.8,       # High exclusion
        }
        energy_cost = polyvagal_penalties[detection.dominant_state]

        # Lure = inverse of energy cost (ventral attracts, dorsal repels)
        lure = 1.0 - energy_cost

        return {
            'polyvagal_state': detection.dominant_state,
            'confidence': detection.confidence,
            'mixed_activation': detection.mixed_activation,
            'coherence': detection.coherence,
            'energy_cost': energy_cost,
            'lure': lure,
            'embedding_contribution': detection.embedding_contribution,
            'keywords_matched': detection.keywords_matched,
            'organ_name': 'EO_POLYVAGAL',
            'specialization': 'polyvagal_detection_embedding_based'
        }

    def update_learned_patterns(
        self,
        text: str,
        confirmed_state: str,
        satisfaction: float
    ):
        """
        Update learned embeddings through Hebbian reinforcement.

        Call this AFTER organism reaches satisfaction on a conversational turn.

        Args:
            text: Text that led to successful response
            confirmed_state: Confirmed polyvagal state (ground truth from user)
            satisfaction: Satisfaction score [0,1] (from V0 convergence)

        Future Integration:
        - Store in TSK/hebbian_memory.json
        - Hebbian coupling with other organs (BOND, SANS)
        - Cluster learning per family
        """
        if satisfaction < 0.7:
            return  # Only learn from high-satisfaction turns

        # Encode text
        text_embedding = self.embedding_model.encode(
            text,
            convert_to_numpy=True
        )
        text_embedding = text_embedding / np.linalg.norm(text_embedding)

        # Add to learned patterns
        if confirmed_state in self.learned_embeddings:
            self.learned_embeddings[confirmed_state].append(text_embedding)

        # TODO: Persist to Hebbian memory
        # self._save_to_hebbian_memory(confirmed_state, text_embedding)


# Quick utility functions
def quick_polyvagal_check(text: str) -> Tuple[str, float]:
    """
    Quick polyvagal state detection (convenience function).

    Args:
        text: User input text

    Returns:
        (state, confidence) tuple

    Example:
        >>> quick_polyvagal_check("I feel overwhelmed and anxious.")
        ('sympathetic', 0.78)
    """
    detector = PolyvagalDetector()
    detection = detector.detect_polyvagal_state(text)
    return (detection.dominant_state, detection.confidence)


def is_safe_to_engage(text: str, threshold: float = 0.6) -> bool:
    """
    Quick safety check for trauma-informed engagement.

    Args:
        text: User input text
        threshold: Confidence threshold for safety

    Returns:
        True if ventral state with sufficient confidence

    Example:
        >>> is_safe_to_engage("I feel curious and open.")
        True  # Ventral with high confidence

        >>> is_safe_to_engage("I'm shutting down and numb.")
        False  # Dorsal = not safe to push deeper
    """
    detector = PolyvagalDetector()
    detection = detector.detect_polyvagal_state(text)

    return (
        detection.dominant_state == 'ventral' and
        detection.confidence >= threshold
    )
