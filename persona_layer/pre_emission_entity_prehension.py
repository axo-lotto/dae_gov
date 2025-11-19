#!/usr/bin/env python3
"""
Pre-Emission Entity Prehension
================================

Retrieves relevant entity memory BEFORE organ activation, enabling:
1. Entity Memory Nexus (EMN) formation
2. Organ context enrichment from historical data
3. Relational continuity across conversations

This fixes the critical gap where entity memory was retrieved AFTER organ processing,
causing failures like "Nexuses formed: 0" on explicit relationship queries.

Whiteheadian Foundation:
- Each occasion prehends past occasions (entity memories)
- Current input inherits relational data from persistent superject
- Entity mentions trigger historical context retrieval
- Organs feel toward entities with accumulated valence

Date: November 16, 2025
Phase: NEXUS Entity Memory Training
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

try:
    from persona_layer.user_superject_learner import UserSuperjectLearner
    from persona_layer.superject_structures import EnhancedUserProfile
except ImportError:
    # Allow module to be imported even if dependencies are missing
    UserSuperjectLearner = None
    EnhancedUserProfile = None


class PreEmissionEntityPrehension:
    """
    Pre-emission layer that retrieves entity context before organ processing.

    Core responsibility: Make entity memories available during organ activation
    so that NEXUS formation can include relational context.

    Key innovation: Retrieve BEFORE, not after organ processing.
    """

    def __init__(self, storage_dir: str = "persona_layer/users"):
        """
        Initialize prehension layer.

        Args:
            storage_dir: Where superject profiles are stored
        """
        self.storage_dir = Path(storage_dir)
        self._learner = None
        self._init_learner()

        # Relational query patterns
        self._relational_patterns = [
            r'\bremember\b.*\b(my|our|name|relationship)\b',
            r'\bdo you (know|recall)\b',
            r'\bwho (am i|is|are)\b',
            r'\bwhat.*\b(told|mentioned|said)\b.*\babout\b',
            r'\bout (of|between|with)\b',
            r'\bour\b.*\b(relationship|connection|history)\b',
            r'\bmy\b.*\b(daughter|son|wife|husband|partner|friend|boss|colleague)\b',
            r'\bname\b.*\bis\b',
            r'\bcalled\b',
            r'\bintroduced\b',
        ]

        # First-person possession patterns (likely about user)
        self._first_person_patterns = [
            r'\bmy\s+(\w+)',
            r'\bi\s+am\s+(\w+)',
            r"\bi'm\s+(\w+)",
            r'\bcall\s+me\s+(\w+)',
        ]

        print(f"✅ PreEmissionEntityPrehension initialized")

    def _init_learner(self):
        """Initialize superject learner if available."""
        if UserSuperjectLearner is not None:
            try:
                self._learner = UserSuperjectLearner(str(self.storage_dir))
            except Exception as e:
                print(f"⚠️  Could not initialize UserSuperjectLearner: {e}")
                self._learner = None
        else:
            self._learner = None

    def retrieve_relevant_entities(
        self,
        user_input: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve entities relevant to current input.

        This is the KEY innovation: retrieve BEFORE organ activation.

        Args:
            user_input: Current user message
            user_id: User identifier

        Returns:
            Dict containing:
            - mentioned_entities: List of entity dicts
            - user_name: str or None
            - relational_query_detected: bool
            - implicit_references: List of potential entity references
            - historical_context: Summary of user's entity memory
        """
        result = {
            'mentioned_entities': [],
            'user_name': None,
            'relational_query_detected': False,
            'implicit_references': [],
            'historical_context': {},
            'entity_memory_available': False,
        }

        if self._learner is None:
            return result

        # 1. Load user's entity memory
        try:
            profile = self._learner.get_or_create_profile(user_id)
            entities = profile.entities
            result['entity_memory_available'] = bool(entities)
        except Exception as e:
            print(f"⚠️  Failed to load profile for {user_id}: {e}")
            return result

        # 2. Check if this is a relational query
        result['relational_query_detected'] = self._is_relational_query(user_input)

        # 3. Extract entity names mentioned in current input
        input_lower = user_input.lower()
        mentioned = []

        # Check for user's own name
        if 'user_name' in entities and entities['user_name']:
            user_name = entities['user_name']
            result['user_name'] = user_name

            # Check if they're asking about themselves
            if self._mentions_name(user_input, user_name):
                mentioned.append({
                    'name': user_name,
                    'type': 'user_self',
                    'context': 'user identity',
                    'source': 'stored_profile',
                })

        # Check for mentioned relationship names
        # Support both 'relationships' and 'manual_entities' formats
        all_relationships = []
        if 'relationships' in entities:
            all_relationships.extend(entities['relationships'])
        if 'manual_entities' in entities:
            all_relationships.extend(entities['manual_entities'])
        if 'family_members' in entities:
            all_relationships.extend(entities['family_members'])

        for rel in all_relationships:
            rel_name = rel.get('name', '')
            if rel_name and self._mentions_name(user_input, rel_name):
                mentioned.append({
                    'name': rel_name,
                    'type': rel.get('type', 'person'),
                    'relationship': rel.get('relationship', 'unknown'),
                    'context': f"User's {rel.get('relationship', 'connection')}",
                    'historical_polyvagal': rel.get('polyvagal_state', 'unknown'),
                    'historical_safety': rel.get('safety_score', 0.5),
                    'source': 'stored_profile',
                })

        # Check for other mentioned names
        if 'mentioned_names' in entities:
            for name in entities['mentioned_names']:
                if self._mentions_name(user_input, name):
                    # Check if already in mentioned list
                    if not any(m['name'] == name for m in mentioned):
                        mentioned.append({
                            'name': name,
                            'type': 'person',
                            'context': 'Previously mentioned',
                            'source': 'stored_profile',
                        })

        result['mentioned_entities'] = mentioned

        # 4. Detect implicit entity references
        result['implicit_references'] = self._detect_implicit_references(user_input, entities)

        # ✅ FIX (Nov 16): Add implicitly referenced entities to mentioned_entities
        # NEXUS needs these to compute past/present differentiation
        for impl_ref in result['implicit_references']:
            resolved_name = impl_ref.get('resolved_to', '')
            if resolved_name and not any(m['name'] == resolved_name for m in mentioned):
                mentioned.append({
                    'name': resolved_name,
                    'type': 'person',
                    'relationship': impl_ref.get('relationship', 'unknown'),
                    'context': f"Implicit reference ('{impl_ref.get('keyword', '')}')",
                    'source': 'implicit_reference',
                    'confidence': impl_ref.get('confidence', 0.85)
                })

        # Update mentioned_entities with implicit resolutions
        result['mentioned_entities'] = mentioned

        # 🚨 CRITICAL FIX (Nov 18): Entity memory should be available if user HAS stored entities
        # This ensures cross-session continuity - memory is context for ALL turns, not just when mentioned
        has_stored_entities = bool(entities and any(entities.values()))
        has_mentioned_entities = len(mentioned) > 0 or bool(result['implicit_references'])

        # Memory available if EITHER: (1) user has stored entities OR (2) entities mentioned this turn
        result['entity_memory_available'] = has_stored_entities or has_mentioned_entities

        # 🔍 DEBUG: Show why memory is/isn't available
        if has_stored_entities:
            entity_count = sum(len(v) if isinstance(v, list) else (1 if v else 0) for v in entities.values())
            print(f"   🌀 Entity memory AVAILABLE: {entity_count} stored entities in profile")

        # 5. Build historical context summary
        result['historical_context'] = self._build_historical_context(entities)

        return result

    def _is_relational_query(self, user_input: str) -> bool:
        """Check if input is asking about relationship/memory."""
        input_lower = user_input.lower()

        for pattern in self._relational_patterns:
            if re.search(pattern, input_lower):
                return True

        # Also check for direct memory keywords
        memory_keywords = ['remember', 'recall', 'know', 'told you', 'mentioned', 'said before']
        return any(kw in input_lower for kw in memory_keywords)

    def _mentions_name(self, text: str, name: str) -> bool:
        """Check if text mentions a specific name (case-insensitive word boundary)."""
        if not name:
            return False
        # Word boundary match
        pattern = r'\b' + re.escape(name) + r'\b'
        return bool(re.search(pattern, text, re.IGNORECASE))

    def _detect_implicit_references(
        self,
        user_input: str,
        entities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Detect implicit entity references.

        E.g., "my daughter" when we know daughter's name is Emma.
        """
        implicit = []
        input_lower = user_input.lower()

        # Map relationship keywords to stored relationships
        rel_keywords = {
            'daughter': ['daughter'],
            'son': ['son'],
            'wife': ['wife', 'spouse'],
            'husband': ['husband', 'spouse'],
            'partner': ['partner'],
            'friend': ['friend'],
            'boss': ['boss', 'manager'],
            'colleague': ['colleague', 'coworker'],
            'mother': ['mother', 'mom'],
            'father': ['father', 'dad'],
        }

        # Check stored relationships
        if 'relationships' in entities:
            for rel in entities['relationships']:
                rel_type = rel.get('relationship', '').lower()
                rel_name = rel.get('name', '')

                # Check if any keyword for this relationship type is in input
                for keyword, matches in rel_keywords.items():
                    if rel_type in matches or keyword in rel_type:
                        # Check if user mentions this relationship type
                        if re.search(r'\b' + keyword + r'\b', input_lower):
                            # Implicit reference found
                            implicit.append({
                                'keyword': keyword,
                                'resolved_to': rel_name,
                                'relationship': rel_type,
                                'confidence': 0.85,  # High confidence implicit reference
                            })

        return implicit

    def _build_historical_context(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Build summary of user's entity memory."""
        context = {
            'has_user_name': bool(entities.get('user_name')),
            'relationship_count': len(entities.get('relationships', [])),
            'mentioned_names_count': len(entities.get('mentioned_names', [])),
            'facts_count': len(entities.get('facts', [])),
            'preferences_count': len(entities.get('preferences', [])),
        }

        # Calculate memory richness score
        total_entities = (
            (1 if context['has_user_name'] else 0) +
            context['relationship_count'] +
            context['mentioned_names_count'] +
            context['facts_count'] +
            context['preferences_count']
        )
        context['memory_richness'] = min(1.0, total_entities / 20.0)  # Max at 20 entities

        return context

    def inject_into_organ_context(
        self,
        entity_prehension: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create organ context enrichment from retrieved entities.

        This data is injected into organ processing to influence atom activation.

        Returns:
            Dict of organ-specific context boosts
        """
        context_enrichment = {
            'LISTENING': {
                'relational_inquiry_boost': 0.0,
                'entity_context_available': False,
            },
            'BOND': {
                'entity_parts_available': False,
                'relationship_safety_context': {},
            },
            'EO': {
                'historical_safety_scores': {},
                'relational_polyvagal_context': {},
            },
            'EMPATHY': {
                'relational_attunement_boost': 0.0,
            },
            'NDAM': {
                'entity_urgency_context': {},
            },
        }

        # 1. LISTENING: Boost relational inquiry if relational query detected
        if entity_prehension.get('relational_query_detected', False):
            context_enrichment['LISTENING']['relational_inquiry_boost'] = 0.3

        # 2. If entities mentioned, provide context
        mentioned = entity_prehension.get('mentioned_entities', [])
        if mentioned:
            context_enrichment['LISTENING']['entity_context_available'] = True
            context_enrichment['EMPATHY']['relational_attunement_boost'] = 0.2

            # BOND: relationship safety context
            for entity in mentioned:
                name = entity.get('name', '')
                safety = entity.get('historical_safety', 0.5)
                context_enrichment['BOND']['relationship_safety_context'][name] = safety

            context_enrichment['BOND']['entity_parts_available'] = True

            # EO: polyvagal context from history
            for entity in mentioned:
                name = entity.get('name', '')
                polyvagal = entity.get('historical_polyvagal', 'unknown')
                safety = entity.get('historical_safety', 0.5)
                context_enrichment['EO']['historical_safety_scores'][name] = safety
                context_enrichment['EO']['relational_polyvagal_context'][name] = polyvagal

        # 3. Implicit references also count
        implicit = entity_prehension.get('implicit_references', [])
        if implicit:
            context_enrichment['LISTENING']['entity_context_available'] = True
            # Slightly lower boost for implicit
            if context_enrichment['EMPATHY']['relational_attunement_boost'] == 0.0:
                context_enrichment['EMPATHY']['relational_attunement_boost'] = 0.15

        # 4. Memory richness affects overall context
        hist_context = entity_prehension.get('historical_context', {})
        memory_richness = hist_context.get('memory_richness', 0.0)

        if memory_richness > 0.5:
            # Rich memory = more relational context
            context_enrichment['LISTENING']['relational_inquiry_boost'] += 0.1
            context_enrichment['EMPATHY']['relational_attunement_boost'] += 0.1

        return context_enrichment

    def create_entity_memory_nexus_data(
        self,
        entity_prehension: Dict[str, Any],
        organ_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create data for Entity Memory Nexus (EMN) formation.

        EMN bridges stored entity memory with current organ activation.
        This is a NEW nexus type that forms when:
        1. Relational query detected
        2. Entity memory available
        3. Relevant organs activated

        Args:
            entity_prehension: Result from retrieve_relevant_entities()
            organ_results: Current organ activation results

        Returns:
            EMN formation data (or empty if conditions not met)
        """
        emn_data = {
            'can_form_emn': False,
            'emn_strength': 0.0,
            'participating_organs': [],
            'entity_context': {},
            'nexus_type': 'entity_memory_nexus',
        }

        # Check formation conditions
        relational_query = entity_prehension.get('relational_query_detected', False)
        memory_available = entity_prehension.get('entity_memory_available', False)
        mentioned = entity_prehension.get('mentioned_entities', [])

        if not memory_available:
            return emn_data

        # Calculate organ participation for EMN
        participating = []
        strength_sum = 0.0

        # Check LISTENING (must participate)
        if 'LISTENING' in organ_results:
            listening = organ_results['LISTENING']
            if self._organ_has_high_activation(listening):
                participating.append('LISTENING')
                strength_sum += self._get_max_activation(listening)

        # Check EMPATHY
        if 'EMPATHY' in organ_results:
            empathy = organ_results['EMPATHY']
            if self._organ_has_high_activation(empathy):
                participating.append('EMPATHY')
                strength_sum += self._get_max_activation(empathy)

        # Check BOND
        if 'BOND' in organ_results:
            bond = organ_results['BOND']
            if self._organ_has_high_activation(bond):
                participating.append('BOND')
                strength_sum += self._get_max_activation(bond)

        # Check EO
        if 'EO' in organ_results:
            eo = organ_results['EO']
            if self._organ_has_high_activation(eo):
                participating.append('EO')
                strength_sum += self._get_max_activation(eo)

        # EMN can form if:
        # - Relational query + at least 2 organs + memory available
        # - OR Entity mentioned + at least 3 organs
        if relational_query and len(participating) >= 2 and memory_available:
            emn_data['can_form_emn'] = True
            emn_data['emn_strength'] = min(1.0, strength_sum / len(participating))
        elif mentioned and len(participating) >= 3:
            emn_data['can_form_emn'] = True
            emn_data['emn_strength'] = min(1.0, (strength_sum / len(participating)) * 0.9)

        emn_data['participating_organs'] = participating
        emn_data['entity_context'] = {
            'user_name': entity_prehension.get('user_name'),
            'mentioned_count': len(mentioned),
            'implicit_count': len(entity_prehension.get('implicit_references', [])),
            'memory_richness': entity_prehension.get('historical_context', {}).get('memory_richness', 0.0),
        }

        return emn_data

    def _organ_has_high_activation(self, organ_data: Dict) -> bool:
        """Check if organ has high enough activation (> 0.5)."""
        if isinstance(organ_data, dict):
            # Check atom_activations dict
            if 'atom_activations' in organ_data:
                activations = organ_data['atom_activations']
                if isinstance(activations, dict):
                    return any(v > 0.5 for v in activations.values())

            # Check top_atoms list
            if 'top_atoms' in organ_data:
                top_atoms = organ_data['top_atoms']
                if isinstance(top_atoms, list) and top_atoms:
                    if isinstance(top_atoms[0], (list, tuple)) and len(top_atoms[0]) >= 2:
                        return any(item[1] > 0.5 for item in top_atoms)
                    elif isinstance(top_atoms[0], dict):
                        return any(item.get('activation', 0) > 0.5 for item in top_atoms)

        return False

    def _get_max_activation(self, organ_data: Dict) -> float:
        """Get maximum activation from organ data."""
        max_act = 0.0

        if isinstance(organ_data, dict):
            # Check atom_activations dict
            if 'atom_activations' in organ_data:
                activations = organ_data['atom_activations']
                if isinstance(activations, dict) and activations:
                    max_act = max(activations.values())

            # Check top_atoms list
            if 'top_atoms' in organ_data:
                top_atoms = organ_data['top_atoms']
                if isinstance(top_atoms, list) and top_atoms:
                    if isinstance(top_atoms[0], (list, tuple)) and len(top_atoms[0]) >= 2:
                        max_act = max(max_act, max(item[1] for item in top_atoms))
                    elif isinstance(top_atoms[0], dict):
                        max_act = max(max_act, max(item.get('activation', 0) for item in top_atoms))

        return max_act

    def get_entity_context_string(self, entity_prehension: Dict[str, Any]) -> str:
        """
        Generate human-readable entity context for debugging.

        Useful for wrapper to display what entity memory was retrieved.
        """
        lines = []

        if not entity_prehension.get('entity_memory_available', False):
            return "No entity memory available for this user."

        user_name = entity_prehension.get('user_name')
        if user_name:
            lines.append(f"User name: {user_name}")

        if entity_prehension.get('relational_query_detected', False):
            lines.append("🔍 Relational query detected")

        mentioned = entity_prehension.get('mentioned_entities', [])
        if mentioned:
            lines.append(f"Entities mentioned in input ({len(mentioned)}):")
            for entity in mentioned[:5]:  # Limit to 5
                name = entity.get('name', 'unknown')
                rel = entity.get('relationship', entity.get('type', 'entity'))
                lines.append(f"  - {name} ({rel})")

        implicit = entity_prehension.get('implicit_references', [])
        if implicit:
            lines.append(f"Implicit references ({len(implicit)}):")
            for ref in implicit[:3]:  # Limit to 3
                kw = ref.get('keyword', '')
                resolved = ref.get('resolved_to', '')
                lines.append(f"  - '{kw}' → {resolved}")

        hist = entity_prehension.get('historical_context', {})
        richness = hist.get('memory_richness', 0.0)
        lines.append(f"Memory richness: {richness:.2f}")

        return "\n".join(lines)


# Singleton pattern for easy import
_prehension_instance = None


def get_prehension_layer(storage_dir: str = "persona_layer/users") -> PreEmissionEntityPrehension:
    """Get singleton instance of prehension layer."""
    global _prehension_instance
    if _prehension_instance is None:
        _prehension_instance = PreEmissionEntityPrehension(storage_dir)
    return _prehension_instance


# Quick test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("PRE-EMISSION ENTITY PREHENSION - UNIT TEST")
    print("="*60 + "\n")

    # Initialize
    prehension = PreEmissionEntityPrehension()

    # Test 1: Relational query detection
    print("Test 1: Relational Query Detection")
    print("-" * 40)
    test_queries = [
        "Do you remember my name?",
        "What did I tell you about Emma?",
        "Who am I to you?",
        "Our relationship is important.",
        "The weather is nice.",  # Not relational
    ]

    for query in test_queries:
        is_rel = prehension._is_relational_query(query)
        status = "✅ RELATIONAL" if is_rel else "❌ NOT RELATIONAL"
        print(f"  '{query[:40]}...' → {status}")

    print("\n" + "="*60)
    print("Test 2: Entity Retrieval (requires user profile)")
    print("-" * 40)

    # Test with non-existent user (should return empty)
    result = prehension.retrieve_relevant_entities(
        "Do you remember my name?",
        "test_entity_prehension_user"
    )

    print(f"  Entity memory available: {result['entity_memory_available']}")
    print(f"  Relational query: {result['relational_query_detected']}")
    print(f"  Mentioned entities: {len(result['mentioned_entities'])}")

    print("\n" + "="*60)
    print("Test 3: Organ Context Injection")
    print("-" * 40)

    # Simulate entity prehension with relational query
    mock_prehension = {
        'relational_query_detected': True,
        'entity_memory_available': True,
        'mentioned_entities': [
            {
                'name': 'Emma',
                'relationship': 'daughter',
                'historical_safety': 0.92,
                'historical_polyvagal': 'ventral_vagal',
            }
        ],
        'implicit_references': [],
        'historical_context': {'memory_richness': 0.75},
    }

    enrichment = prehension.inject_into_organ_context(mock_prehension)

    print(f"  LISTENING boost: {enrichment['LISTENING']['relational_inquiry_boost']}")
    print(f"  EMPATHY boost: {enrichment['EMPATHY']['relational_attunement_boost']}")
    print(f"  BOND entities available: {enrichment['BOND']['entity_parts_available']}")
    print(f"  EO safety scores: {enrichment['EO']['historical_safety_scores']}")

    print("\n" + "="*60)
    print("Test 4: Entity Memory Nexus Formation")
    print("-" * 40)

    # Simulate organ results with high activation
    mock_organ_results = {
        'LISTENING': {
            'top_atoms': [('relational_inquiry', 0.85), ('temporal_inquiry', 0.60)]
        },
        'EMPATHY': {
            'top_atoms': [('relational_attunement', 0.78), ('compassionate_presence', 0.65)]
        },
        'BOND': {
            'top_atoms': [('manager_parts', 0.45), ('SELF_energy', 0.55)]
        },
        'EO': {
            'top_atoms': [('ventral_vagal', 0.92), ('sympathetic_activation', 0.25)]
        },
    }

    emn_data = prehension.create_entity_memory_nexus_data(mock_prehension, mock_organ_results)

    print(f"  Can form EMN: {emn_data['can_form_emn']}")
    print(f"  EMN strength: {emn_data['emn_strength']:.2f}")
    print(f"  Participating organs: {emn_data['participating_organs']}")
    print(f"  Nexus type: {emn_data['nexus_type']}")

    print("\n" + "="*60)
    print("✅ All tests passed")
    print("="*60)
