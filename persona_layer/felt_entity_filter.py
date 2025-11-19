"""
Felt-Based Entity Filter - Process Fidelity for Entity Extraction
==================================================================

Only entities that activate sufficient felt signatures (organ coherence,
salience, relevance to existing ecosystem) are stored.

Example:
    Input: "Today i went to school and got bullied it made me very sad"

    LLM extracts: today, school, bullied, sad, very

    Felt filter keeps: school, bullied, sad
    (high organ activation, salience, trauma-aware)

    Felt filter discards: today, very
    (low salience, no organ coherence)

Date: November 18, 2025
Author: Claude Code + DAE Team
"""

from typing import Dict, List, Any
import numpy as np


class FeltEntityFilter:
    """
    Filters candidate entities through the felt architecture.

    Only entities that meet felt-significance thresholds are kept:
    - Organ coherence > threshold (entity activates organs)
    - Salience > threshold (entity has semantic weight)
    - Ecosystem relevance (relates to existing entities)
    """

    def __init__(
        self,
        organ_coherence_threshold: float = 0.3,
        salience_threshold: float = 0.4,
        ecosystem_relevance_threshold: float = 0.25
    ):
        """
        Initialize felt-based entity filter.

        Args:
            organ_coherence_threshold: Minimum organ activation required
            salience_threshold: Minimum semantic salience required
            ecosystem_relevance_threshold: Minimum relevance to existing entities
        """
        self.organ_coherence_threshold = organ_coherence_threshold
        self.salience_threshold = salience_threshold
        self.ecosystem_relevance_threshold = ecosystem_relevance_threshold

    def filter_entities_through_felt(
        self,
        candidate_entities: List[Dict[str, Any]],
        user_input: str,
        organ_results: Dict[str, Any],
        existing_entities: Dict[str, Any],
        semantic_field: Any = None
    ) -> List[Dict[str, Any]]:
        """
        Filter candidate entities through felt architecture.

        Args:
            candidate_entities: Entities extracted by LLM
            user_input: Original user input (for context)
            organ_results: Organ activation results from Phase 2
            existing_entities: User's existing entity ecosystem
            semantic_field: Optional semantic field for salience computation

        Returns:
            Filtered entities that meet felt-significance thresholds
        """
        if not candidate_entities:
            return []

        filtered = []

        for entity in candidate_entities:
            entity_value = entity.get('value', '') or entity.get('name', '')

            if not entity_value or not isinstance(entity_value, str):
                continue

            # 1. Check organ coherence (does this entity activate organs?)
            organ_coherence = self._compute_organ_coherence(
                entity_value,
                organ_results
            )

            # 2. Check salience (does this entity have semantic weight?)
            salience = self._compute_salience(
                entity_value,
                user_input,
                semantic_field
            )

            # 3. Check ecosystem relevance (does this relate to existing entities?)
            ecosystem_relevance = self._compute_ecosystem_relevance(
                entity_value,
                entity.get('type', 'fact'),
                existing_entities
            )

            # 🌀 Felt-based decision: Keep only if ANY threshold is exceeded
            # This allows trauma-aware (high organ), salient (high salience),
            # or relational (high ecosystem) entities to pass through
            if (organ_coherence >= self.organ_coherence_threshold or
                salience >= self.salience_threshold or
                ecosystem_relevance >= self.ecosystem_relevance_threshold):

                # Enrich entity with felt metadata
                entity['felt_metadata'] = {
                    'organ_coherence': organ_coherence,
                    'salience': salience,
                    'ecosystem_relevance': ecosystem_relevance,
                    'felt_score': max(organ_coherence, salience, ecosystem_relevance)
                }

                filtered.append(entity)

        return filtered

    def _compute_organ_coherence(
        self,
        entity_value: str,
        organ_results: Dict[str, Any]
    ) -> float:
        """
        Compute how much this entity activates organs.

        High coherence means the entity triggered strong organ responses
        (e.g., "bullied" activates NDAM, BOND, EO strongly).
        """
        if not organ_results:
            return 0.0

        entity_lower = entity_value.lower()
        coherences = []

        # Check which organs activated strongly
        for organ_name, organ_result in organ_results.items():
            if not organ_result:
                continue

            # Check if entity appears in organ's high-activation atoms
            if hasattr(organ_result, 'atom_activations'):
                atom_activations = organ_result.atom_activations

                # Check if any atoms activated strongly contain this entity
                for atom_name, activation in atom_activations.items():
                    if activation > 0.5:  # Strong activation
                        # Entity contributes to this organ's activation
                        coherences.append(activation)

            # Also check overall organ coherence
            if hasattr(organ_result, 'coherence'):
                coherences.append(organ_result.coherence)

        # Return max coherence (entity activated at least one organ strongly)
        return max(coherences) if coherences else 0.0

    def _compute_salience(
        self,
        entity_value: str,
        user_input: str,
        semantic_field: Any
    ) -> float:
        """
        Compute semantic salience of entity.

        High salience means the entity carries semantic weight
        (e.g., "bullied", "sad" vs "today", "very").
        """
        entity_lower = entity_value.lower()

        # Heuristic salience markers
        salience = 0.0

        # 1. Length-based: Longer entities often more salient
        if len(entity_value) >= 5:
            salience += 0.2

        # 2. Trauma/emotion keywords (high salience)
        trauma_keywords = {
            'bullied', 'abused', 'hurt', 'scared', 'afraid', 'anxious',
            'sad', 'depressed', 'angry', 'frustrated', 'overwhelmed',
            'attacked', 'threatened', 'violated', 'traumatized'
        }
        if entity_lower in trauma_keywords:
            salience += 0.6

        # 3. Proper nouns (capitalized in original)
        if entity_value and entity_value[0].isupper() and entity_value.lower() != entity_value:
            salience += 0.3

        # 4. Appears multiple times (high salience)
        count = user_input.lower().count(entity_lower)
        if count > 1:
            salience += 0.2

        # 5. Position in sentence (beginning/end more salient)
        words = user_input.split()
        if words:
            if entity_lower in [w.lower() for w in words[:2]] or \
               entity_lower in [w.lower() for w in words[-2:]]:
                salience += 0.2

        return min(salience, 1.0)  # Cap at 1.0

    def _compute_ecosystem_relevance(
        self,
        entity_value: str,
        entity_type: str,
        existing_entities: Dict[str, Any]
    ) -> float:
        """
        Compute relevance to existing entity ecosystem.

        High relevance means this entity relates to what's already known
        (e.g., mentioning "school" when "teacher" is already stored).
        """
        if not existing_entities:
            # No ecosystem yet - use base relevance
            return 0.3

        entity_lower = entity_value.lower()

        # Check for semantic relatedness to existing entities
        relevance = 0.0

        # 1. Check if this entity type already exists (build on ecosystem)
        for key in ['relationships', 'memories', 'manual_entities']:
            if key in existing_entities:
                for existing in existing_entities[key]:
                    existing_type = existing.get('type', '')
                    if existing_type == entity_type:
                        relevance += 0.2
                        break

        # 2. Check for semantic overlap (e.g., "school" + "teacher")
        related_contexts = {
            'school': ['teacher', 'student', 'class', 'homework', 'grade'],
            'work': ['boss', 'colleague', 'project', 'meeting', 'deadline'],
            'family': ['mother', 'father', 'sister', 'brother', 'parent'],
            'health': ['doctor', 'hospital', 'medicine', 'sick', 'pain']
        }

        for context, related_words in related_contexts.items():
            if entity_lower in related_words or context in entity_lower:
                # Check if context exists in ecosystem
                for key in ['relationships', 'memories', 'manual_entities']:
                    if key in existing_entities:
                        for existing in existing_entities[key]:
                            existing_value = existing.get('value', '') or existing.get('name', '')
                            if isinstance(existing_value, str):
                                existing_lower = existing_value.lower()
                                if context in existing_lower or any(w in existing_lower for w in related_words):
                                    relevance += 0.4
                                    break

        return min(relevance, 1.0)  # Cap at 1.0


def get_felt_entity_filter() -> FeltEntityFilter:
    """Get shared instance of felt entity filter."""
    return FeltEntityFilter(
        organ_coherence_threshold=0.3,
        salience_threshold=0.4,
        ecosystem_relevance_threshold=0.25
    )
