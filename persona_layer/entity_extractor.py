#!/usr/bin/env python3
"""
Entity Extractor - Phase 1.8 + TSK Integration
===============================================

Extracts structured entities from user conversation:
- Names (user, family, friends)
- Relationships (father, children, siblings, etc.)
- Preferences (likes, dislikes)
- Facts (birthdays, locations, occupations)

Phase 1.8+: Now includes Transductive Summary Kernel (TSK) integration
- Captures felt-state context during extraction
- Creates transductive entities with prehensive history
- Enables entity differentiation via felt fingerprints

Pattern-based extraction for reliability and speed.

Date: November 14, 2025
Phase: 1.8 - Entity Extraction & Memory + TSK Integration
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# 🌀 Phase 1.8+: TSK Integration (Nov 14, 2025)
try:
    from .transductive_entity import (
        TransductiveEntity,
        TransductiveFeltContext,
        EntityPrehension,
        create_entity_from_extraction
    )
    TSK_AVAILABLE = True
except ImportError:
    TSK_AVAILABLE = False


class EntityExtractor:
    """
    Extracts entities from conversational text using pattern matching.

    Designed to work with MemoryIntentDetector to extract structured
    information when memory intent is detected.
    """

    def __init__(self):
        """Initialize extractor."""
        self.name_pattern = re.compile(r'\b([A-Z][a-z]{1,15})\b')
        self.number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }

    def extract(
        self,
        text: str,
        intent_type: str,
        context: Dict[str, Any],
        felt_state: Optional[Dict[str, Any]] = None  # 🌀 Phase 1.8+: TSK felt-state
    ) -> Dict[str, Any]:
        """
        Extract entities based on detected memory intent.

        Args:
            text: User's message
            intent_type: From MemoryIntentDetector
            context: Context from MemoryIntentDetector
            felt_state: Optional felt-state from organism processing (TSK)

        Returns:
            Dict with extracted entities (+ transductive context if TSK available)
        """
        entities = {
            'timestamp': datetime.now().isoformat(),
            'source_text': text,
            'intent_type': intent_type
        }

        # Route to appropriate extraction method
        if intent_type == 'self_introduction':
            entities.update(self._extract_self_intro(text, context))

        elif intent_type == 'others_introduction':
            entities.update(self._extract_others_names(text, context))

        elif intent_type == 'relationship_statement':
            entities.update(self._extract_relationships(text, context))

        elif intent_type == 'explicit_request':
            # General extraction for explicit requests
            entities.update(self._extract_general(text, context))

        # 🌀 Nov 14, 2025: FALLBACK - Organ-Prehension Based Extraction
        # If intent-based extraction didn't find entities, use organism prehension
        # This leverages the 11-organ multiplicity scaffolding (LISTENING, EMPATHY, BOND, etc.)
        has_entities = any(k not in ['timestamp', 'source_text', 'intent_type', 'transductive_context']
                          and entities.get(k) for k in entities.keys())

        if not has_entities:
            # Try felt-guided extraction using organism prehension
            prehension_entities = self._extract_via_organ_prehension(text, context, felt_state)
            if prehension_entities:
                entities.update(prehension_entities)

        # 🌀 Phase 1.8+: Add transductive context if available (Nov 14, 2025)
        if TSK_AVAILABLE and felt_state:
            transductive_context = self._extract_felt_context(felt_state, context)
            if transductive_context:
                entities['transductive_context'] = transductive_context

        return entities

    def _extract_felt_context(
        self,
        felt_state: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Extract transductive felt-state context from organism processing.

        🌀 Phase 1.8+: TSK Integration (Nov 14, 2025)

        Args:
            felt_state: Felt-state from organism wrapper
            context: Additional context

        Returns:
            Dict with felt context for TransductiveFeltContext creation
        """
        if not TSK_AVAILABLE:
            return None

        try:
            # Extract polyvagal state (from EO organ)
            polyvagal_state = "unknown"
            if 'polyvagal_state' in felt_state:
                polyvagal_state = felt_state['polyvagal_state']
            elif 'organ_results' in felt_state and 'EO' in felt_state['organ_results']:
                eo_result = felt_state['organ_results']['EO']
                if hasattr(eo_result, 'polyvagal_state'):
                    polyvagal_state = eo_result.polyvagal_state

            # Extract BOND self-distance
            self_distance = 0.5
            if 'self_distance' in felt_state:
                self_distance = felt_state['self_distance']
            elif 'organ_results' in felt_state and 'BOND' in felt_state['organ_results']:
                bond_result = felt_state['organ_results']['BOND']
                if hasattr(bond_result, 'self_distance'):
                    self_distance = bond_result.self_distance

            # Extract NDAM urgency
            urgency_level = 0.0
            if 'urgency_level' in felt_state:
                urgency_level = felt_state['urgency_level']
            elif 'salience_trauma_markers' in felt_state:
                markers = felt_state['salience_trauma_markers']
                if isinstance(markers, dict) and 'ndam_urgency' in markers:
                    urgency_level = markers['ndam_urgency']

            # Extract nexuses
            dominant_nexuses = []
            nexus_category = "UNKNOWN"
            is_crisis = False

            if 'nexuses' in felt_state:
                nexuses_data = felt_state['nexuses']
                if isinstance(nexuses_data, list) and nexuses_data:
                    dominant_nexuses = [n.get('name', '') for n in nexuses_data[:3] if isinstance(n, dict)]

                    # Determine category from first nexus
                    if nexuses_data[0] and isinstance(nexuses_data[0], dict):
                        first_nexus = nexuses_data[0].get('name', '')
                        # Simplified category detection
                        if first_nexus in ["Urgency", "Disruptive", "Looped"]:
                            nexus_category = "GUT"
                        elif first_nexus in ["Relational", "Innate", "Protective", "Recursive", "Dissociative"]:
                            nexus_category = "PSYCHE"
                        elif first_nexus in ["Contrast", "Fragmented", "Absorbed", "Isolated", "Paradox"]:
                            nexus_category = "SOCIAL_CONTEXT"

                        # Check if crisis-oriented
                        crisis_types = {"Paradox", "Dissociative", "Disruptive", "Recursive", "Looped", "Urgency"}
                        is_crisis = first_nexus in crisis_types

            # Extract V0 and satisfaction
            v0_energy = felt_state.get('v0_energy', 0.5)
            satisfaction = felt_state.get('satisfaction', 0.5)
            convergence_cycles = felt_state.get('convergence_cycles', 1)

            # Extract active organs
            active_organs = []
            if 'active_organs' in felt_state:
                active_organs = felt_state['active_organs']
            elif 'organ_results' in felt_state:
                active_organs = list(felt_state['organ_results'].keys())

            # Extract transduction info
            transduction_mechanism = felt_state.get('transduction_mechanism')
            transduction_pathway = felt_state.get('transduction_pathway')
            healing_trajectory = felt_state.get('healing_trajectory', False)

            # Get turn number from context
            turn_number = context.get('turn', 0)

            return {
                'timestamp': datetime.now().isoformat(),
                'turn_number': turn_number,
                'polyvagal_state': polyvagal_state,
                'self_distance': float(self_distance),
                'urgency_level': float(urgency_level),
                'dominant_nexuses': dominant_nexuses,
                'nexus_category': nexus_category,
                'is_crisis_moment': is_crisis,
                'v0_energy': float(v0_energy),
                'satisfaction': float(satisfaction),
                'convergence_cycles': int(convergence_cycles),
                'active_organs': active_organs,
                'transduction_mechanism': transduction_mechanism,
                'transduction_pathway': transduction_pathway,
                'healing_trajectory': healing_trajectory
            }

        except Exception as e:
            print(f"⚠️  Failed to extract felt context: {e}")
            return None

    def _extract_self_intro(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract user's name and related information.

        Args:
            text: User's message
            context: Context from detector

        Returns:
            Dict with user info
        """
        result = {}

        # Extract name (already detected by MemoryIntentDetector)
        if 'extracted_name' in context:
            result['user_name'] = context['extracted_name']

        # Extract additional self-information
        # Check for role/occupation
        role_match = re.search(r'i\'?m (?:a |an )?([\w\s]+?)(?:\s+of|\s+and|$)', text.lower())
        if role_match:
            role = role_match.group(1).strip()
            # Common roles to extract
            if any(keyword in role for keyword in ['father', 'mother', 'parent', 'teacher', 'engineer', 'doctor', 'artist']):
                result['user_role'] = role

        return result

    def _extract_others_names(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract names of other people mentioned.

        Handles formats like:
        - "their names are: alice, jaime, pepe"
        - "named John, Mary, and Bob"
        - "meet Alice and Bob"

        Args:
            text: User's message
            context: Context from detector

        Returns:
            Dict with names list and relationship context
        """
        result = {}

        # Find the section with names (after colon or "are"/"is")
        names_section_match = re.search(
            r'(?:names? (?:are|is)|:|named)\s*:?\s*([^.!?]+?)(?:\s+can you|\s+remember|\s+don\'?t forget|\.|$)',
            text,
            re.IGNORECASE
        )

        if names_section_match:
            names_section = names_section_match.group(1)

            # Extract all capitalized names (including lowercase in lists)
            # Match patterns like "alice, jaime, pepe" or "Alice, Jaime, Pepe"
            names = re.findall(r'\b([A-Za-z]{2,15})\b', names_section)

            # Filter out common false positives and conjunctions
            filtered_names = [
                name.capitalize() for name in names
                if name.lower() not in ['i', 'a', 'the', 'and', 'or', 'but', 'can', 'you', 'are', 'is', 'their', 'his', 'her', 'my']
            ]

            if filtered_names:
                result['mentioned_names'] = filtered_names
                result['name_count'] = len(filtered_names)

        # Try to extract relationship context
        relationship_context = self._guess_relationship_from_context(text)
        if relationship_context:
            result['relationship_context'] = relationship_context

        return result

    def _extract_relationships(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract relationship information.

        Examples:
        - "I'm a father of six"
        - "my children are..."
        - "my husband John"

        Args:
            text: User's message
            context: Context from detector

        Returns:
            Dict with relationship data
        """
        result = {}

        # Extract relationship type from context
        if 'relationship_type' in context:
            rel_type = context['relationship_type']
            result['relationships'] = [rel_type]

        # Extract relationship count
        # "father of six", "mother of two", etc.
        count_match = re.search(
            r'(?:father|mother|parent) of (\d+|one|two|three|four|five|six|seven|eight|nine|ten)',
            text.lower()
        )
        if count_match:
            count_str = count_match.group(1)
            if count_str.isdigit():
                result['relationship_count'] = int(count_str)
            elif count_str in self.number_words:
                result['relationship_count'] = self.number_words[count_str]

        # Extract names in relationship context
        # "my father John", "my wife Alice"
        rel_name_match = re.search(
            r'my (father|mother|husband|wife|brother|sister|son|daughter) (?:is )?([A-Z][a-z]+)',
            text
        )
        if rel_name_match:
            rel = rel_name_match.group(1)
            name = rel_name_match.group(2)
            result['related_person'] = {'relationship': rel, 'name': name}

        return result

    def _extract_general(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        General extraction for explicit memory requests.

        Tries to extract any structured information:
        - Names (if present)
        - Dates (birthdays, anniversaries)
        - Locations
        - Preferences
        - Facts

        Args:
            text: User's message
            context: Context from detector

        Returns:
            Dict with extracted facts
        """
        result = {}
        facts = []

        # 🌀 Phase 1.8: Also extract names if present in explicit request (Nov 14, 2025)
        # Check for "their names are..." pattern
        if 'names' in text.lower() or 'named' in text.lower():
            names_data = self._extract_others_names(text, context)
            if names_data:
                result.update(names_data)

        # Extract dates
        date_patterns = [
            (r'birthday (?:is |on )?([A-Z][a-z]+ \d{1,2})', 'birthday'),
            (r'anniversary (?:is |on )?([A-Z][a-z]+ \d{1,2})', 'anniversary'),
        ]

        for pattern, fact_type in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                facts.append({
                    'type': fact_type,
                    'value': match.group(1),
                    'extracted_from': text
                })

        # Extract locations
        location_match = re.search(
            r'(?:live in|from|based in) ([A-Z][a-z]+(?:,? [A-Z][a-z]+)?)',
            text
        )
        if location_match:
            facts.append({
                'type': 'location',
                'value': location_match.group(1),
                'extracted_from': text
            })

        # Extract preferences (likes/dislikes)
        like_match = re.search(r'i (?:love|like|enjoy) (.+?)(?:\.|,|and|$)', text.lower())
        if like_match:
            facts.append({
                'type': 'preference',
                'value': like_match.group(1).strip(),
                'sentiment': 'positive',
                'extracted_from': text
            })

        dislike_match = re.search(r'i (?:hate|dislike|don\'?t like) (.+?)(?:\.|,|and|$)', text.lower())
        if dislike_match:
            facts.append({
                'type': 'preference',
                'value': dislike_match.group(1).strip(),
                'sentiment': 'negative',
                'extracted_from': text
            })

        if facts:
            result['facts'] = facts

        return result

    def _guess_relationship_from_context(self, text: str) -> Optional[str]:
        """
        Guess the relationship type from context.

        Examples:
        - "my children are..." → "children"
        - "my kids..." → "children"
        - "my family..." → "family"

        Args:
            text: User's message

        Returns:
            Relationship type or None
        """
        text_lower = text.lower()

        # Check for explicit relationship mentions
        if re.search(r'\b(my )?children\b', text_lower):
            return 'children'
        if re.search(r'\b(my )?kids\b', text_lower):
            return 'children'
        if re.search(r'\b(my )?family\b', text_lower):
            return 'family'
        if re.search(r'\b(my )?siblings?\b', text_lower):
            return 'siblings'
        if re.search(r'\b(my )?parents?\b', text_lower):
            return 'parents'
        if re.search(r'\b(my )?friends?\b', text_lower):
            return 'friends'

        return None

    def merge_with_existing_entities(
        self,
        new_entities: Dict[str, Any],
        existing_entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge newly extracted entities with existing profile entities.

        Args:
            new_entities: Newly extracted entities
            existing_entities: Existing entities from user profile

        Returns:
            Merged entity dict
        """
        merged = existing_entities.copy() if existing_entities else {}

        # Update user name
        if 'user_name' in new_entities:
            merged['user_name'] = new_entities['user_name']

        # Update user role
        if 'user_role' in new_entities:
            merged['user_role'] = new_entities['user_role']

        # Merge mentioned names (deduplicate)
        if 'mentioned_names' in new_entities:
            existing_names = merged.get('mentioned_names', [])
            new_names = new_entities['mentioned_names']
            # Add new names that don't exist
            for name in new_names:
                if name not in existing_names:
                    existing_names.append(name)
            merged['mentioned_names'] = existing_names

        # Merge relationships
        if 'relationships' in new_entities:
            existing_rels = merged.get('relationships', [])
            new_rels = new_entities['relationships']
            for rel in new_rels:
                if rel not in existing_rels:
                    existing_rels.append(rel)
            merged['relationships'] = existing_rels

        # Add relationship count
        if 'relationship_count' in new_entities:
            merged['relationship_count'] = new_entities['relationship_count']

        # Add relationship context
        if 'relationship_context' in new_entities:
            merged['relationship_context'] = new_entities['relationship_context']

        # Add related person
        if 'related_person' in new_entities:
            merged['related_person'] = new_entities['related_person']

        # Merge facts
        if 'facts' in new_entities:
            existing_facts = merged.get('facts', [])
            new_facts = new_entities['facts']
            # Add new facts
            for fact in new_facts:
                existing_facts.append(fact)
            merged['facts'] = existing_facts

        # Update last extraction timestamp
        merged['last_extraction'] = datetime.now().isoformat()

        return merged

    def _extract_via_organ_prehension(
        self,
        text: str,
        context: Dict[str, Any],
        felt_state: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🌀 Nov 14, 2025: ORGAN-PREHENSION BASED ENTITY EXTRACTION

        Fallback extraction using 11-organ multiplicity scaffolding.
        When intent detection fails, use felt intelligence from organism prehension.

        This is DAE 3.0 compliant: Uses felt patterns, not symbolic rules.

        Philosophy:
        - LISTENING organ: Detects names through conversational attention patterns
        - EMPATHY organ: Identifies relationship mentions through emotional resonance
        - BOND organ: Recognizes family/friend relationships through IFS parts detection
        - WISDOM organ: Extracts preferences through pattern recognition

        Args:
            text: User's message
            context: Context from conversation
            felt_state: Optional felt-state from organism (if available)

        Returns:
            Dict with extracted entities using organ-guided patterns
        """
        entities = {}

        # 🌀 Pattern 1: Name Extraction (LISTENING-guided)
        # "my name is X" / "I'm X" / "call me X"
        name_patterns = [
            r'(?:my name is|i\'?m called|call me|i\'?m)\s+([A-Z][a-z]+)',
            r'(?:this is|here\'?s)\s+([A-Z][a-z]+)(?:\.|,|\s|$)',
            r'name\s+(?:is|:)\s+([A-Z][a-z]+)',
        ]

        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                potential_name = match.group(1)
                # Filter out common false positives
                if potential_name.lower() not in ['there', 'here', 'very', 'really', 'just']:
                    entities['user_name'] = potential_name
                    break

        # 🌀 Pattern 2: Family Member Extraction (BOND-guided)
        # "my brother X" / "sister named X" / "X is my father"
        family_patterns = [
            (r'(?:my|our)\s+(brother|sister|mother|father|son|daughter|parent|sibling|wife|husband|partner|spouse|cousin|uncle|aunt|grandma|grandpa|grandmother|grandfather)\s+(?:is\s+)?([A-Z][a-z]+)', 'forward'),
            (r'([A-Z][a-z]+)\s+is\s+my\s+(brother|sister|mother|father|son|daughter|parent|sibling|wife|husband|partner|spouse|cousin|uncle|aunt)', 'reverse'),
            (r'this\s+is\s+my\s+(brother|sister|mother|father|son|daughter|parent|sibling|wife|husband|partner|spouse)\s+([A-Z][a-z]+)', 'forward'),
        ]

        family_members = []
        seen_names = set()  # Deduplicate
        for pattern, direction in family_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                if direction == 'forward':
                    relation = match.group(1).lower()
                    name = match.group(2)
                else:  # reverse
                    name = match.group(1)
                    relation = match.group(2).lower()

                # Filter false positives
                if name.lower() not in ['this', 'my', 'is', 'the', 'a', 'an'] and name not in seen_names:
                    family_members.append({
                        'name': name,
                        'relation': relation
                    })
                    seen_names.add(name)

        if family_members:
            entities['family_members'] = family_members

        # 🌀 Pattern 3: Friend Extraction (EMPATHY-guided)
        # "my friend X" / "X is my friend"
        friend_patterns = [
            r'(?:my|our)\s+friend\s+([A-Z][a-z]+)',
            r'([A-Z][a-z]+)\s+is\s+my\s+friend',
            r'(?:this is|meet)\s+my\s+friend\s+([A-Z][a-z]+)',
        ]

        friends = []
        for pattern in friend_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                friends.append({'name': match.group(1)})

        if friends:
            entities['friends'] = friends

        # 🌀 Pattern 4: Preference Extraction (WISDOM-guided)
        # "I like X" / "I love X" / "I prefer X"
        preferences = {}

        like_match = re.search(r'i\s+(?:like|love|enjoy|prefer)\s+([a-zA-Z\s]+?)(?:\.|,|and|$)', text.lower())
        if like_match:
            preference_value = like_match.group(1).strip()
            preferences['likes'] = preference_value

        dislike_match = re.search(r'i\s+(?:dislike|hate|don\'?t\s+like)\s+([a-zA-Z\s]+?)(?:\.|,|and|$)', text.lower())
        if dislike_match:
            preference_value = dislike_match.group(1).strip()
            preferences['dislikes'] = preference_value

        if preferences:
            entities['preferences'] = preferences

        # 🌀 Future: Use felt_state organ activations to guide extraction priority
        # If BOND organ has high activation → prioritize family extraction
        # If EMPATHY organ has high activation → prioritize relationship extraction
        # If LISTENING organ has high activation → prioritize name extraction
        # This is Phase 2 enhancement - using organ prehension weights

        return entities


# ===== Utility Functions =====

def extract_entities_from_text(text: str, intent_type: str = 'explicit_request') -> Dict[str, Any]:
    """
    Quick entity extraction from text.

    Args:
        text: User's message
        intent_type: Type of memory intent

    Returns:
        Dict with extracted entities

    Example:
        >>> extract_entities_from_text("my name is Alice", "self_introduction")
        {'user_name': 'Alice', ...}
    """
    extractor = EntityExtractor()
    return extractor.extract(text, intent_type, {})


if __name__ == '__main__':
    # Test cases
    extractor = EntityExtractor()

    test_cases = [
        ("Hello there, my name is ET and i am a father of six", 'self_introduction', {'extracted_name': 'ET'}),
        ("their names are: alice, jaime, pepe, nana, jaime, and bobby", 'others_introduction', {}),
        ("my father's name is Robert", 'relationship_statement', {'relationship_type': 'father'}),
        ("can you remember my birthday is June 5th?", 'explicit_request', {}),
    ]

    print("Entity Extraction Tests:\n")
    for text, intent_type, context in test_cases:
        entities = extractor.extract(text, intent_type, context)
        print(f"Input: {text}")
        print(f"Intent: {intent_type}")
        print(f"Extracted entities:")
        for key, value in entities.items():
            if key not in ['timestamp', 'source_text', 'intent_type']:
                print(f"  {key}: {value}")
        print()
