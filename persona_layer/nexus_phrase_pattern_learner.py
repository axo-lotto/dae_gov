"""
Nexus-Phrase Pattern Learner
=============================

Core learning engine for intersection-centered foundational intelligence.
Learns phrase patterns from nexus signatures via EMA quality updates.

Architecture: Intersection Emission (The Many Become One)
- Input: NexusSignature (18D canonical representation)
- Storage: Nexus-phrase associations with quality metrics
- Learning: EMA quality updates (α=0.15) from user satisfaction
- Lookup: Fuzzy matching with bin relaxation (tolerance=1)

Integration: Phase 1 Week 2 (Foundational Intelligence)
North Star: Companion Intelligence Strategic Assessment (Nov 17, 2025)
  → Affective Intelligence FIRST (therapeutic presence, emotional attunement)
  → Cognitive Intelligence LATER (reasoning, planning)

Key Principles:
1. Intersection-centered (nexus + 1), NOT entity-centered
2. Bounded by coherence horizon (4,000-5,000 patterns)
3. Logarithmic saturation: P(t) = 112.4 × ln(H) - 362.8
4. Fast lookup: ~1-5ms (hashable tuple dict access)

November 17, 2025 - Phase 1 Week 2, Days 1-2
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
import json
import os
from pathlib import Path
import numpy as np
from persona_layer.nexus_signature_extractor import NexusSignature


@dataclass
class PhraseQualityMetrics:
    """Quality metrics for a single phrase."""

    text: str
    ema_quality: float  # EMA of user satisfaction (α=0.15)
    success_count: int  # Times phrase led to satisfaction ≥ 0.6
    total_attempts: int  # Total times phrase was emitted
    success_rate: float  # success_count / total_attempts
    mean_satisfaction: float  # Mean satisfaction across all attempts
    last_used_turn: int  # Turn number when last used

    # 🆕 Temporal decay (prevents stale phrase persistence)
    recency_weight: float = 1.0  # Decays with turn age

    def compute_overall_quality(self, current_turn: int, decay_lambda: float = 0.001) -> float:
        """
        Compute overall phrase quality with recency weighting.

        Quality = EMA × success_rate × recency_weight
        Recency = exp(-λ × turn_age)

        Args:
            current_turn: Current conversation turn number
            decay_lambda: Decay rate (default 0.001 = 1% per turn)

        Returns:
            Overall quality score [0.0-1.0]
        """
        turn_age = current_turn - self.last_used_turn
        self.recency_weight = np.exp(-decay_lambda * turn_age)

        return self.ema_quality * self.success_rate * self.recency_weight


@dataclass
class NexusPhrasePattern:
    """
    Learned association between nexus signature and phrase.

    Storage format in conversational_hebbian_memory.json:
    {
      "nexus_phrase_patterns": {
        "signature_hash": {
          "signature": {...},  # Serialized NexusSignature
          "phrases": [
            {
              "text": "I hear the weight...",
              "ema_quality": 0.79,
              "success_count": 23,
              "total_attempts": 30,
              ...
            }
          ]
        }
      }
    }
    """

    signature_hash: str  # Hashable tuple as string key
    signature: NexusSignature  # Original 18D signature
    phrases: List[PhraseQualityMetrics] = field(default_factory=list)

    def add_phrase(self, phrase_text: str, initial_quality: float = 0.5) -> None:
        """Add new phrase to this pattern."""
        if not any(p.text == phrase_text for p in self.phrases):
            self.phrases.append(PhraseQualityMetrics(
                text=phrase_text,
                ema_quality=initial_quality,
                success_count=0,
                total_attempts=0,
                success_rate=0.0,
                mean_satisfaction=0.0,
                last_used_turn=0
            ))

    def update_phrase_quality(
        self,
        phrase_text: str,
        user_satisfaction: float,
        current_turn: int,
        ema_alpha: float = 0.15
    ) -> None:
        """
        Update phrase quality via EMA learning.

        EMA formula: Q_new = α × S + (1-α) × Q_old

        Args:
            phrase_text: The phrase that was emitted
            user_satisfaction: User satisfaction [0.0-1.0]
            current_turn: Current conversation turn
            ema_alpha: EMA learning rate (default 0.15)
        """
        for phrase in self.phrases:
            if phrase.text == phrase_text:
                # EMA update
                phrase.ema_quality = (
                    ema_alpha * user_satisfaction +
                    (1 - ema_alpha) * phrase.ema_quality
                )

                # Count update
                phrase.total_attempts += 1
                if user_satisfaction >= 0.6:
                    phrase.success_count += 1
                phrase.success_rate = phrase.success_count / phrase.total_attempts

                # Mean satisfaction update (running average)
                phrase.mean_satisfaction = (
                    (phrase.mean_satisfaction * (phrase.total_attempts - 1) + user_satisfaction) /
                    phrase.total_attempts
                )

                # Timestamp update
                phrase.last_used_turn = current_turn

                break

    def get_top_phrases(self, k: int, current_turn: int) -> List[PhraseQualityMetrics]:
        """
        Get top-k phrases by overall quality.

        Args:
            k: Number of top phrases to return
            current_turn: Current turn (for recency weighting)

        Returns:
            List of top-k phrases sorted by quality
        """
        sorted_phrases = sorted(
            self.phrases,
            key=lambda p: p.compute_overall_quality(current_turn),
            reverse=True
        )
        return sorted_phrases[:k]


class NexusPhrasePatternLearner:
    """
    Nexus-Phrase Pattern Learner: Intersection-Centered Emission Learning

    Core learning engine for foundational intelligence (Phase 1).

    Capabilities:
    1. Store nexus-phrase associations with quality metrics
    2. EMA quality learning from user satisfaction
    3. Fuzzy lookup with bin relaxation (tolerance=1)
    4. Persistence to conversational_hebbian_memory.json
    5. Bounded coherence horizon (4,000-5,000 patterns)

    Usage:
        learner = NexusPhrasePatternLearner()

        # Record emission outcome
        learner.record_emission_outcome(
            nexus_signature=sig,
            emitted_phrase="I hear the weight...",
            user_satisfaction=0.85,
            current_turn=42
        )

        # Get candidate phrases for new input
        candidates = learner.get_candidate_phrases(
            nexus_signature=sig,
            k=5,
            current_turn=43
        )
    """

    def __init__(
        self,
        memory_path: Optional[str] = None,
        ema_alpha: float = 0.15,
        fuzzy_tolerance: int = 1,
        max_patterns: int = 5000
    ):
        """
        Initialize pattern learner.

        Args:
            memory_path: Path to conversational_hebbian_memory.json
            ema_alpha: EMA learning rate (default 0.15)
            fuzzy_tolerance: Bin relaxation tolerance (default 1)
            max_patterns: Maximum patterns (coherence horizon, default 5000)
        """
        self.memory_path = memory_path or os.path.join(
            os.path.dirname(__file__),
            "../conversational_hebbian_memory.json"
        )
        self.ema_alpha = ema_alpha
        self.fuzzy_tolerance = fuzzy_tolerance
        self.max_patterns = max_patterns

        # In-memory pattern storage
        # Key: signature_hash (str), Value: NexusPhrasePattern
        self.patterns: Dict[str, NexusPhrasePattern] = {}

        # Load existing patterns
        self._load_patterns()

    def _load_patterns(self) -> None:
        """Load patterns from conversational_hebbian_memory.json."""
        if not os.path.exists(self.memory_path):
            self.patterns = {}
            return

        try:
            with open(self.memory_path, 'r') as f:
                memory = json.load(f)

            nexus_phrase_data = memory.get("nexus_phrase_patterns", {})

            for sig_hash, pattern_data in nexus_phrase_data.items():
                # Reconstruct NexusSignature from serialized data
                sig_dict = pattern_data.get("signature", {})
                signature = self._deserialize_signature(sig_dict)

                # Reconstruct phrases
                phrases = []
                for phrase_data in pattern_data.get("phrases", []):
                    phrases.append(PhraseQualityMetrics(
                        text=phrase_data["text"],
                        ema_quality=phrase_data["ema_quality"],
                        success_count=phrase_data["success_count"],
                        total_attempts=phrase_data["total_attempts"],
                        success_rate=phrase_data["success_rate"],
                        mean_satisfaction=phrase_data["mean_satisfaction"],
                        last_used_turn=phrase_data["last_used_turn"]
                    ))

                self.patterns[sig_hash] = NexusPhrasePattern(
                    signature_hash=sig_hash,
                    signature=signature,
                    phrases=phrases
                )

        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            self.patterns = {}

    def _save_patterns(self) -> None:
        """Save patterns to conversational_hebbian_memory.json."""
        # Load existing memory (to preserve other data)
        if os.path.exists(self.memory_path):
            with open(self.memory_path, 'r') as f:
                memory = json.load(f)
        else:
            memory = {}

        # Serialize patterns
        nexus_phrase_data = {}
        for sig_hash, pattern in self.patterns.items():
            nexus_phrase_data[sig_hash] = {
                "signature": self._serialize_signature(pattern.signature),
                "phrases": [
                    {
                        "text": p.text,
                        "ema_quality": p.ema_quality,
                        "success_count": p.success_count,
                        "total_attempts": p.total_attempts,
                        "success_rate": p.success_rate,
                        "mean_satisfaction": p.mean_satisfaction,
                        "last_used_turn": p.last_used_turn
                    }
                    for p in pattern.phrases
                ]
            }

        memory["nexus_phrase_patterns"] = nexus_phrase_data

        # Write to file
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        with open(self.memory_path, 'w') as f:
            json.dump(memory, f, indent=2)

    def _serialize_signature(self, signature: NexusSignature) -> Dict:
        """Convert NexusSignature to JSON-serializable dict."""
        return {
            "participating_organs": list(signature.participating_organs),
            "organ_count": signature.organ_count,
            "nexus_type": signature.nexus_type,
            "mechanism": signature.mechanism,
            "coherence_bin": signature.coherence_bin,
            "urgency_bin": signature.urgency_bin,
            "polyvagal_state": signature.polyvagal_state,
            "zone": signature.zone,
            "v0_energy_bin": signature.v0_energy_bin,
            "kairos_detected": signature.kairos_detected,
            "field_strength_bin": signature.field_strength_bin,
            "dominant_meta_atom": signature.dominant_meta_atom,
            "constraint_pattern": signature.constraint_pattern,
            "transductive_vocabulary": list(signature.transductive_vocabulary) if signature.transductive_vocabulary else None,
            "satisfaction_tier": signature.satisfaction_tier,
            "emission_path": signature.emission_path,
            "convergence_cycles": signature.convergence_cycles,
            "entity_context": list(signature.entity_context) if signature.entity_context else None
        }

    def _deserialize_signature(self, sig_dict: Dict) -> NexusSignature:
        """Reconstruct NexusSignature from dict."""
        return NexusSignature(
            participating_organs=frozenset(sig_dict["participating_organs"]),
            organ_count=sig_dict["organ_count"],
            nexus_type=sig_dict["nexus_type"],
            mechanism=sig_dict["mechanism"],
            coherence_bin=sig_dict["coherence_bin"],
            urgency_bin=sig_dict["urgency_bin"],
            polyvagal_state=sig_dict["polyvagal_state"],
            zone=sig_dict["zone"],
            v0_energy_bin=sig_dict["v0_energy_bin"],
            kairos_detected=sig_dict["kairos_detected"],
            field_strength_bin=sig_dict["field_strength_bin"],
            dominant_meta_atom=sig_dict["dominant_meta_atom"],
            constraint_pattern=sig_dict.get("constraint_pattern"),
            transductive_vocabulary=frozenset(sig_dict["transductive_vocabulary"]) if sig_dict.get("transductive_vocabulary") else None,
            satisfaction_tier=sig_dict.get("satisfaction_tier"),
            emission_path=sig_dict.get("emission_path"),
            convergence_cycles=sig_dict.get("convergence_cycles"),
            entity_context=frozenset(sig_dict["entity_context"]) if sig_dict.get("entity_context") else None
        )

    def record_emission_outcome(
        self,
        nexus_signature: NexusSignature,
        emitted_phrase: str,
        user_satisfaction: float,
        current_turn: int
    ) -> None:
        """
        Record emission outcome and update phrase quality via EMA.

        Args:
            nexus_signature: 18D nexus signature
            emitted_phrase: The phrase that was emitted
            user_satisfaction: User satisfaction [0.0-1.0]
            current_turn: Current conversation turn
        """
        sig_hash = str(nexus_signature.to_hashable(precision='medium'))

        # Create pattern if doesn't exist
        if sig_hash not in self.patterns:
            # Check coherence horizon (max patterns)
            if len(self.patterns) >= self.max_patterns:
                # Remove lowest quality pattern (oldest, least successful)
                self._prune_lowest_quality_pattern(current_turn)

            self.patterns[sig_hash] = NexusPhrasePattern(
                signature_hash=sig_hash,
                signature=nexus_signature,
                phrases=[]
            )

        pattern = self.patterns[sig_hash]

        # Add phrase if new
        pattern.add_phrase(emitted_phrase, initial_quality=user_satisfaction)

        # Update quality
        pattern.update_phrase_quality(
            phrase_text=emitted_phrase,
            user_satisfaction=user_satisfaction,
            current_turn=current_turn,
            ema_alpha=self.ema_alpha
        )

        # Persist to disk
        self._save_patterns()

    def get_candidate_phrases(
        self,
        nexus_signature: NexusSignature,
        k: int = 5,
        current_turn: int = 0,
        use_fuzzy: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Get top-k candidate phrases for emission.

        Uses fuzzy matching with bin relaxation (tolerance=1) to find
        similar nexus patterns even if exact match doesn't exist.

        Args:
            nexus_signature: 18D nexus signature
            k: Number of candidates to return (default 5)
            current_turn: Current turn (for recency weighting)
            use_fuzzy: Enable fuzzy matching (default True)

        Returns:
            List of (phrase_text, quality_score) tuples
        """
        # Try exact match first
        sig_hash = str(nexus_signature.to_hashable(precision='medium'))

        if sig_hash in self.patterns:
            pattern = self.patterns[sig_hash]
            top_phrases = pattern.get_top_phrases(k, current_turn)
            return [
                (p.text, p.compute_overall_quality(current_turn))
                for p in top_phrases
            ]

        # Fuzzy matching
        if use_fuzzy:
            fuzzy_keys = nexus_signature.fuzzy_match_keys(
                tolerance=self.fuzzy_tolerance,
                precision='medium'
            )

            # Collect phrases from all fuzzy matches
            all_candidates = []
            for fuzzy_key in fuzzy_keys:
                fuzzy_hash = str(fuzzy_key)
                if fuzzy_hash in self.patterns:
                    pattern = self.patterns[fuzzy_hash]
                    for phrase in pattern.phrases:
                        quality = phrase.compute_overall_quality(current_turn)
                        all_candidates.append((phrase.text, quality))

            # Sort by quality and return top-k
            all_candidates.sort(key=lambda x: x[1], reverse=True)
            return all_candidates[:k]

        # No match found
        return []

    def _prune_lowest_quality_pattern(self, current_turn: int) -> None:
        """
        Remove lowest quality pattern to maintain coherence horizon.

        Quality metric: max(overall_quality) across all phrases in pattern
        """
        if not self.patterns:
            return

        # Compute max quality per pattern
        pattern_qualities = {}
        for sig_hash, pattern in self.patterns.items():
            if pattern.phrases:
                max_quality = max(
                    p.compute_overall_quality(current_turn)
                    for p in pattern.phrases
                )
                pattern_qualities[sig_hash] = max_quality
            else:
                pattern_qualities[sig_hash] = 0.0

        # Remove lowest quality pattern
        lowest_sig = min(pattern_qualities, key=pattern_qualities.get)
        del self.patterns[lowest_sig]

    def get_stats(self) -> Dict:
        """Get learning statistics."""
        total_patterns = len(self.patterns)
        total_phrases = sum(len(p.phrases) for p in self.patterns.values())

        all_qualities = [
            phrase.ema_quality
            for pattern in self.patterns.values()
            for phrase in pattern.phrases
        ]

        return {
            "total_patterns": total_patterns,
            "total_phrases": total_phrases,
            "mean_phrase_quality": np.mean(all_qualities) if all_qualities else 0.0,
            "std_phrase_quality": np.std(all_qualities) if all_qualities else 0.0,
            "coherence_horizon_utilization": total_patterns / self.max_patterns
        }
