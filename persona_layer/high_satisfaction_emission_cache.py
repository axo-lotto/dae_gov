"""
High-Satisfaction Emission Cache - Phase 1 of LLM Dependency Reduction v2
============================================================================

Caches high-satisfaction emissions with their full felt-state context for future
compositional retrieval. This is the foundation for learning response composition
patterns from accumulated experience.

Purpose:
- Record emissions that achieve high user satisfaction (>0.8)
- Index by organ signature, SELF zone, transduction pathway
- Enable future compositional assembly from learned patterns
- Track which response patterns correlate with therapeutic success

Philosophy:
- Each high-satisfaction emission is a "crystallized occasion" worth remembering
- The accumulated cache becomes a learned vocabulary of successful responses
- Future responses can be composed from similar historical patterns
- This enables gradual LLM dependency reduction through pattern learning

Integration:
- Called by ConversationalOrganismWrapper after emission generation
- Stores full TSK context with each cached emission
- Provides retrieval methods for compositional assembler (Phase 3)

Date: November 16, 2025
Status: Phase 1 Implementation - LLM Dependency Reduction v2
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from collections import defaultdict


@dataclass
class CachedEmission:
    """
    A high-satisfaction emission with full felt-state context.

    This is the fundamental unit of learned response pattern.
    """
    id: str
    timestamp: str

    # Input-Output pair
    user_input: str
    emission_text: str

    # Quality metrics
    satisfaction_score: float
    confidence: float
    emission_strategy: str  # 'felt_guided_llm', 'direct', 'fusion', 'hebbian'

    # Organ context (57D signature)
    organ_signature: List[float]  # Full 57D vector
    top_organs: List[str]  # Top 3 contributing organs
    organ_weights: Dict[str, float]  # {organ_name: weight_multiplier}

    # SELF zone context
    self_zone: int  # 1-6 (urgency, protective, recursive, etc.)
    self_distances: Dict[str, float]  # Distance to each zone centroid

    # Transduction context
    transduction_pathway: str  # 'salience_recalibration', 'ontological_rebinding', etc.
    v0_energy: float  # Final V0 energy after convergence
    v0_descent: float  # Total descent magnitude
    convergence_cycles: int  # Number of convergence cycles

    # Polyvagal context
    polyvagal_state: str  # 'ventral', 'sympathetic', 'dorsal'
    polyvagal_scores: Dict[str, float]  # {state: score}

    # Family context (if available)
    family_id: Optional[int]
    family_name: Optional[str]

    # Meta-information
    kairos_detected: bool
    active_meta_atoms: List[str]
    nexus_count: int


class HighSatisfactionEmissionCache:
    """
    Cache and index high-satisfaction emissions for compositional learning.

    This module implements Phase 1 of the LLM Dependency Reduction v2 strategy:
    - Record emissions with satisfaction >0.8
    - Index by multiple dimensions (organ, zone, pathway, family)
    - Enable similarity-based retrieval for future composition

    Expected growth:
    - Epoch 0-20: 50-100 cached emissions
    - Epoch 20-50: 200-400 cached emissions
    - Epoch 50-100: 500-800 cached emissions
    - Epoch 100+: 1000+ cached emissions
    """

    def __init__(
        self,
        cache_path: str = "persona_layer/state/active/high_satisfaction_emissions.json",
        satisfaction_threshold: float = 0.8,
        max_cache_size: int = 5000
    ):
        """
        Initialize the emission cache.

        Args:
            cache_path: Path to persist cached emissions
            satisfaction_threshold: Minimum satisfaction to cache (default: 0.8)
            max_cache_size: Maximum emissions to cache (FIFO eviction)
        """
        self.cache_path = Path(cache_path)
        self.satisfaction_threshold = satisfaction_threshold
        self.max_cache_size = max_cache_size

        # Load existing cache
        self.emissions = self._load_cache()

        # Build indices for fast retrieval
        self._build_indices()

        # Track statistics
        self.stats = {
            'total_cached': len(self.emissions),
            'total_considered': 0,
            'cache_hit_rate': 0.0,
            'avg_satisfaction': 0.0,
            'strategy_distribution': defaultdict(int),
            'zone_distribution': defaultdict(int),
            'pathway_distribution': defaultdict(int)
        }
        self._update_stats()

    def _load_cache(self) -> List[CachedEmission]:
        """Load cached emissions from disk."""
        if not self.cache_path.exists():
            return []

        try:
            with open(self.cache_path, 'r') as f:
                data = json.load(f)

            emissions = []
            for item in data.get('emissions', []):
                emissions.append(CachedEmission(**item))

            return emissions

        except Exception as e:
            print(f"⚠️  Error loading emission cache: {e}")
            return []

    def _save_cache(self):
        """Persist cached emissions to disk."""
        try:
            # Ensure parent directory exists
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'emissions': [asdict(e) for e in self.emissions],
                'metadata': {
                    'total_cached': len(self.emissions),
                    'satisfaction_threshold': self.satisfaction_threshold,
                    'max_cache_size': self.max_cache_size,
                    'last_updated': datetime.now().isoformat()
                },
                'statistics': dict(self.stats)
            }

            with open(self.cache_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Error saving emission cache: {e}")

    def _build_indices(self):
        """Build retrieval indices for fast similarity matching."""
        self.index_by_zone = defaultdict(list)
        self.index_by_pathway = defaultdict(list)
        self.index_by_family = defaultdict(list)
        self.index_by_polyvagal = defaultdict(list)
        self.index_by_strategy = defaultdict(list)

        for i, emission in enumerate(self.emissions):
            self.index_by_zone[emission.self_zone].append(i)
            self.index_by_pathway[emission.transduction_pathway].append(i)
            if emission.family_id is not None:
                self.index_by_family[emission.family_id].append(i)
            self.index_by_polyvagal[emission.polyvagal_state].append(i)
            self.index_by_strategy[emission.emission_strategy].append(i)

    def _update_stats(self):
        """Update cache statistics."""
        if not self.emissions:
            return

        self.stats['total_cached'] = len(self.emissions)
        self.stats['avg_satisfaction'] = np.mean([e.satisfaction_score for e in self.emissions])

        # Strategy distribution
        self.stats['strategy_distribution'] = defaultdict(int)
        for e in self.emissions:
            self.stats['strategy_distribution'][e.emission_strategy] += 1

        # Zone distribution
        self.stats['zone_distribution'] = defaultdict(int)
        for e in self.emissions:
            self.stats['zone_distribution'][e.self_zone] += 1

        # Pathway distribution
        self.stats['pathway_distribution'] = defaultdict(int)
        for e in self.emissions:
            self.stats['pathway_distribution'][e.transduction_pathway] += 1

    def cache_emission(
        self,
        user_input: str,
        emission_text: str,
        satisfaction_score: float,
        confidence: float,
        emission_strategy: str,
        organ_results: Dict[str, Any],
        self_zone: int,
        self_distances: Dict[str, float],
        transduction_pathway: str,
        v0_energy: float,
        v0_descent: float,
        convergence_cycles: int,
        polyvagal_state: str,
        polyvagal_scores: Dict[str, float],
        family_id: Optional[int] = None,
        family_name: Optional[str] = None,
        kairos_detected: bool = False,
        active_meta_atoms: List[str] = None,
        nexus_count: int = 0
    ) -> bool:
        """
        Cache a high-satisfaction emission.

        Returns:
            True if cached, False if below threshold or rejected
        """
        self.stats['total_considered'] += 1

        # Check satisfaction threshold
        if satisfaction_score < self.satisfaction_threshold:
            return False

        # Extract organ signature (57D vector from 11 organs)
        organ_signature = self._extract_organ_signature(organ_results)

        # Extract top organs and weights
        top_organs, organ_weights = self._extract_organ_info(organ_results)

        # Generate unique ID
        emission_id = f"emit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.emissions):04d}"

        # Create cached emission
        cached = CachedEmission(
            id=emission_id,
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            emission_text=emission_text,
            satisfaction_score=satisfaction_score,
            confidence=confidence,
            emission_strategy=emission_strategy,
            organ_signature=organ_signature,
            top_organs=top_organs,
            organ_weights=organ_weights,
            self_zone=self_zone,
            self_distances=self_distances,
            transduction_pathway=transduction_pathway,
            v0_energy=v0_energy,
            v0_descent=v0_descent,
            convergence_cycles=convergence_cycles,
            polyvagal_state=polyvagal_state,
            polyvagal_scores=polyvagal_scores,
            family_id=family_id,
            family_name=family_name,
            kairos_detected=kairos_detected,
            active_meta_atoms=active_meta_atoms or [],
            nexus_count=nexus_count
        )

        # Add to cache
        self.emissions.append(cached)

        # Update indices
        self.index_by_zone[self_zone].append(len(self.emissions) - 1)
        self.index_by_pathway[transduction_pathway].append(len(self.emissions) - 1)
        if family_id is not None:
            self.index_by_family[family_id].append(len(self.emissions) - 1)
        self.index_by_polyvagal[polyvagal_state].append(len(self.emissions) - 1)
        self.index_by_strategy[emission_strategy].append(len(self.emissions) - 1)

        # Evict oldest if cache full
        if len(self.emissions) > self.max_cache_size:
            self._evict_oldest()

        # Update stats and persist
        self._update_stats()
        self._save_cache()

        return True

    def _extract_organ_signature(self, organ_results: Dict[str, Any]) -> List[float]:
        """
        Extract 57D organ signature from organ results.

        Each organ contributes:
        - Activation level (1D)
        - Top atom activations (varies by organ dimension)
        - Weight multiplier adjustment (1D)

        Normalized to 57D total.
        """
        signature = []

        # Order of organs matters for consistent signatures
        organ_order = [
            'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
            'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'
        ]

        for organ_name in organ_order:
            if organ_name in organ_results:
                organ_data = organ_results[organ_name]

                # Primary activation
                activation = organ_data.get('activation_level', 0.0)
                signature.append(float(activation))

                # Top atom activations (4 per organ = 44D total)
                atom_activations = organ_data.get('atom_activations', {})
                sorted_atoms = sorted(atom_activations.items(), key=lambda x: x[1], reverse=True)[:4]

                for i in range(4):
                    if i < len(sorted_atoms):
                        signature.append(float(sorted_atoms[i][1]))
                    else:
                        signature.append(0.0)
            else:
                # Missing organ - add zeros
                signature.extend([0.0] * 5)  # 1 activation + 4 atoms

        # Pad or truncate to exactly 57D
        if len(signature) < 57:
            signature.extend([0.0] * (57 - len(signature)))
        elif len(signature) > 57:
            signature = signature[:57]

        return signature

    def _extract_organ_info(self, organ_results: Dict[str, Any]) -> Tuple[List[str], Dict[str, float]]:
        """Extract top organs and their weight multipliers."""
        organ_activations = []
        organ_weights = {}

        for organ_name, organ_data in organ_results.items():
            if isinstance(organ_data, dict):
                activation = organ_data.get('activation_level', 0.0)
                weight = organ_data.get('weight_multiplier', 1.0)

                organ_activations.append((organ_name, activation))
                organ_weights[organ_name] = weight

        # Sort by activation and get top 3
        organ_activations.sort(key=lambda x: x[1], reverse=True)
        top_organs = [name for name, _ in organ_activations[:3]]

        return top_organs, organ_weights

    def _evict_oldest(self):
        """Remove oldest emission when cache is full (FIFO eviction)."""
        if self.emissions:
            self.emissions.pop(0)
            self._build_indices()  # Rebuild indices after eviction

    def find_similar(
        self,
        organ_signature: List[float],
        self_zone: int,
        transduction_pathway: str,
        polyvagal_state: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[CachedEmission]:
        """
        Find similar cached emissions for compositional assembly.

        Strategy:
        1. Filter by matching zone (most important context)
        2. Score by organ signature similarity (cosine)
        3. Boost score if pathway matches
        4. Boost score if polyvagal state matches
        5. Return top-k above threshold

        Args:
            organ_signature: Current 57D organ signature
            self_zone: Current SELF zone (1-6)
            transduction_pathway: Current transduction pathway
            polyvagal_state: Current polyvagal state
            top_k: Number of similar emissions to return
            similarity_threshold: Minimum similarity score

        Returns:
            List of most similar cached emissions
        """
        if not self.emissions:
            return []

        # Convert to numpy for fast computation
        query_sig = np.array(organ_signature)
        query_norm = np.linalg.norm(query_sig)
        if query_norm == 0:
            query_norm = 1.0
        query_sig = query_sig / query_norm

        candidates = []

        # Prioritize same zone
        zone_indices = self.index_by_zone.get(self_zone, [])

        for idx in zone_indices:
            emission = self.emissions[idx]

            # Compute cosine similarity of organ signatures
            cached_sig = np.array(emission.organ_signature)
            cached_norm = np.linalg.norm(cached_sig)
            if cached_norm == 0:
                cached_norm = 1.0
            cached_sig = cached_sig / cached_norm

            similarity = float(np.dot(query_sig, cached_sig))

            # Boost for matching pathway (×1.2)
            if emission.transduction_pathway == transduction_pathway:
                similarity *= 1.2

            # Boost for matching polyvagal state (×1.1)
            if emission.polyvagal_state == polyvagal_state:
                similarity *= 1.1

            # Clamp to [0, 1]
            similarity = min(1.0, similarity)

            if similarity >= similarity_threshold:
                candidates.append((similarity, emission))

        # Sort by similarity descending
        candidates.sort(key=lambda x: x[0], reverse=True)

        # Return top-k
        return [emission for _, emission in candidates[:top_k]]

    def get_statistics(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring."""
        return {
            'total_cached': self.stats['total_cached'],
            'total_considered': self.stats['total_considered'],
            'cache_rate': self.stats['total_cached'] / max(1, self.stats['total_considered']),
            'avg_satisfaction': self.stats['avg_satisfaction'],
            'strategy_distribution': dict(self.stats['strategy_distribution']),
            'zone_distribution': dict(self.stats['zone_distribution']),
            'pathway_distribution': dict(self.stats['pathway_distribution']),
            'cache_fullness': len(self.emissions) / self.max_cache_size
        }

    def get_zone_coverage(self) -> Dict[int, int]:
        """Get how many emissions cached per SELF zone."""
        return {zone: len(indices) for zone, indices in self.index_by_zone.items()}

    def get_pathway_coverage(self) -> Dict[str, int]:
        """Get how many emissions cached per transduction pathway."""
        return {pathway: len(indices) for pathway, indices in self.index_by_pathway.items()}


# Singleton instance for global access
_cache_instance = None


def get_emission_cache() -> HighSatisfactionEmissionCache:
    """Get or create singleton cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = HighSatisfactionEmissionCache()
    return _cache_instance


def cache_high_satisfaction_emission(
    user_input: str,
    emission_text: str,
    satisfaction_score: float,
    confidence: float,
    emission_strategy: str,
    organ_results: Dict[str, Any],
    self_zone: int,
    self_distances: Dict[str, float],
    transduction_pathway: str,
    v0_energy: float,
    v0_descent: float,
    convergence_cycles: int,
    polyvagal_state: str,
    polyvagal_scores: Dict[str, float],
    family_id: Optional[int] = None,
    family_name: Optional[str] = None,
    kairos_detected: bool = False,
    active_meta_atoms: List[str] = None,
    nexus_count: int = 0
) -> bool:
    """
    Convenience function to cache emission through singleton.

    Returns True if cached, False if rejected.
    """
    cache = get_emission_cache()
    return cache.cache_emission(
        user_input=user_input,
        emission_text=emission_text,
        satisfaction_score=satisfaction_score,
        confidence=confidence,
        emission_strategy=emission_strategy,
        organ_results=organ_results,
        self_zone=self_zone,
        self_distances=self_distances,
        transduction_pathway=transduction_pathway,
        v0_energy=v0_energy,
        v0_descent=v0_descent,
        convergence_cycles=convergence_cycles,
        polyvagal_state=polyvagal_state,
        polyvagal_scores=polyvagal_scores,
        family_id=family_id,
        family_name=family_name,
        kairos_detected=kairos_detected,
        active_meta_atoms=active_meta_atoms,
        nexus_count=nexus_count
    )


def find_similar_emissions(
    organ_signature: List[float],
    self_zone: int,
    transduction_pathway: str,
    polyvagal_state: str,
    top_k: int = 5
) -> List[CachedEmission]:
    """
    Convenience function to find similar emissions through singleton.

    Returns list of similar cached emissions for compositional assembly.
    """
    cache = get_emission_cache()
    return cache.find_similar(
        organ_signature=organ_signature,
        self_zone=self_zone,
        transduction_pathway=transduction_pathway,
        polyvagal_state=polyvagal_state,
        top_k=top_k
    )
