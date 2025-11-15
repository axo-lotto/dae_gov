#!/usr/bin/env python3
"""
Relationship Extractor - Phase 1 Entity Enhancement
====================================================

Extracts relationship entities from user conversation:
- Family members (immediate and extended)
- Friends and social connections
- Professional relationships

Uses pattern matching with confidence scoring.

Date: November 14, 2025
Phase: Entity Enhancement - Tier 1 (Relationships)
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


class RelationshipExtractor:
    """
    Extracts relationship entities using pattern matching.

    Handles:
    - Simple: "my daughter Alice"
    - Multiple: "I have two sons, John and Paul"
    - Complex: "my wife's sister Mary"
    """

    def __init__(self, patterns_path: Optional[str] = None):
        """
        Initialize extractor with relationship patterns.

        Args:
            patterns_path: Path to relationship_patterns.json
        """
        if patterns_path is None:
            patterns_path = Path(__file__).parent.parent / "patterns" / "relationship_patterns.json"

        with open(patterns_path, 'r') as f:
            self.config = json.load(f)

        self.relationship_types = self.config['relationship_types']
        self.patterns = self.config['patterns']
        self.number_words = self.config['number_words']
        self.possessives = self.config['possessives']
        self.relation_normalization = self.config.get('relation_normalization', {})

        # Flatten all relationship terms for validation
        self.all_relations = []
        for category in self.relationship_types.values():
            self.all_relations.extend(category)

    def extract(self, text: str, confidence_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Extract relationships from text.

        Args:
            text: User's message
            confidence_threshold: Minimum confidence to accept extraction

        Returns:
            Dict with extracted relationships and confidence scores
        """
        relationships = {
            'family_members': [],
            'friends': [],
            'colleagues': [],
            'other_relations': []
        }

        extractions = []  # List of (relation, name, confidence, category)

        # Try each pattern
        for pattern_config in self.patterns:
            pattern = pattern_config['pattern']
            confidence = pattern_config['confidence']

            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                extraction = self._process_match(match, pattern_config, text)

                # Handle both single extractions and lists (for multiple names)
                if extraction:
                    if isinstance(extraction, list):
                        # Multiple extractions from one match
                        for ext in extraction:
                            if ext['confidence'] >= confidence_threshold:
                                extractions.append(ext)
                    else:
                        # Single extraction
                        if extraction['confidence'] >= confidence_threshold:
                            extractions.append(extraction)

        # Process extractions and categorize
        for ext in extractions:
            relation_type = ext['relation']
            name = ext['name']
            confidence = ext['confidence']

            # Apply normalization (e.g., roommate → friend)
            relation_type = self.relation_normalization.get(relation_type, relation_type)

            # Determine category
            category = self._categorize_relation(relation_type)

            # Create relationship object
            rel_obj = {
                'name': name,
                'relation': relation_type,
                'confidence': confidence
            }

            # Add to appropriate category
            if category == 'family':
                relationships['family_members'].append(rel_obj)
            elif category == 'friend':
                relationships['friends'].append(rel_obj)
            elif category == 'colleague':
                relationships['colleagues'].append(rel_obj)
            else:
                relationships['other_relations'].append(rel_obj)

        # Remove duplicates (same name + relation)
        for key in relationships:
            relationships[key] = self._deduplicate(relationships[key])

        return relationships

    def _process_match(self, match: re.Match, pattern_config: dict, text: str) -> Optional[Dict[str, Any]]:
        """
        Process a regex match to extract relationship info.

        Args:
            match: Regex match object
            pattern_config: Pattern configuration
            text: Original text

        Returns:
            Dict with relation, name, confidence or None (or List for multiple extractions)
        """
        groups = match.groups()
        if not groups:
            return None

        # Pattern-specific extraction logic
        if pattern_config['description'] == "my [relation] [Name]":
            relation = groups[0].lower()
            name = groups[1] if len(groups) > 1 else None

            if not self._is_valid_relation(relation):
                return None

            return {
                'relation': relation,
                'name': name,
                'confidence': pattern_config['confidence']
            }

        elif pattern_config['description'] == "I have a [relation] [Name]":
            relation = groups[0].lower()
            name = groups[1] if len(groups) > 1 else None

            if not self._is_valid_relation(relation):
                return None

            return {
                'relation': relation,
                'name': name,
                'confidence': pattern_config['confidence']
            }

        elif pattern_config['description'] == "[Name] is my [relation]":
            name = groups[0]
            relation = groups[1].lower() if len(groups) > 1 else None

            if not self._is_valid_relation(relation):
                return None

            return {
                'relation': relation,
                'name': name,
                'confidence': pattern_config['confidence']
            }

        elif pattern_config['description'] == "my [relation] [Title] [Name]":
            # Handle "my therapist Dr. Anderson"
            relation = groups[0].lower()
            name = groups[1] if len(groups) > 1 else None

            if not self._is_valid_relation(relation):
                return None

            return {
                'relation': relation,
                'name': name,
                'confidence': pattern_config['confidence']
            }

        elif pattern_config['description'] == "closest to [relation] [Name]":
            # Handle "I'm closest to my cousin Amy"
            relation = groups[0].lower() if groups[0] else None
            name = groups[1] if len(groups) > 1 else None

            if not self._is_valid_relation(relation):
                return None

            return {
                'relation': relation,
                'name': name,
                'confidence': pattern_config['confidence']
            }

        elif pattern_config['description'] == "closest to [Name] (no relation)":
            # Handle "I'm closest to Amy" - infer relation from context
            name = groups[0] if groups else None

            # Look for relation word in surrounding text
            # From test case rel_023: "I have four cousins, but I'm closest to Amy"
            # We need to extract relation from earlier in sentence
            text_lower = text.lower()

            relation = None
            for rel_list in self.relationship_types.values():
                for rel in rel_list:
                    if rel in text_lower:
                        relation = rel
                        break
                if relation:
                    break

            # Default to friend if no relation found
            if not relation:
                relation = 'friend'

            # Normalize plural to singular
            if relation.endswith('s') and relation not in ['friends', 'parents']:
                relation = relation[:-1]

            return {
                'relation': relation,
                'name': name,
                'confidence': pattern_config['confidence'] * 0.9  # Lower confidence for inferred
            }

        elif "two" in pattern_config['description'] or "number" in pattern_config['description']:
            # Handle "I have two daughters, Alice and Sophie"
            return self._extract_multiple_relations(match, pattern_config, text)

        elif "and" in pattern_config['description']:
            # Handle "my mom Lisa and dad Robert"
            return self._extract_dual_relations(match, pattern_config, text)

        return None

    def _extract_multiple_relations(self, match: re.Match, pattern_config: dict, text: str) -> List[Dict[str, Any]]:
        """
        Extract multiple people with same relation.

        Example: "I have two daughters, Alice and Sophie"
        Returns a LIST of extractions for multi-extraction handling.
        """
        groups = match.groups()

        if len(groups) >= 3:
            number_word = groups[0].lower()  # "two"
            relation = groups[1].lower()  # "daughter"
            name1 = groups[2]
            name2 = groups[3] if len(groups) > 3 else None

            if not self._is_valid_relation(relation):
                return None

            # Convert number word to int
            count = self.number_words.get(number_word, 1)

            # Normalize relation to singular
            if relation.endswith('s'):
                relation = relation[:-1]

            # Return BOTH names if present
            extractions = []

            # First name
            extractions.append({
                'relation': relation,
                'name': name1,
                'confidence': pattern_config['confidence'] * 0.85,  # Slightly lower for multiple
            })

            # Second name (if present)
            if name2:
                extractions.append({
                    'relation': relation,
                    'name': name2,
                    'confidence': pattern_config['confidence'] * 0.85,
                })

            return extractions

        return None

    def _extract_dual_relations(self, match: re.Match, pattern_config: dict, text: str) -> List[Dict[str, Any]]:
        """
        Extract two people with different relations.

        Example: "my mom Lisa and dad Robert"
        Returns a LIST of extractions.
        """
        groups = match.groups()

        if len(groups) >= 3:
            relation1 = groups[0].lower()  # "mom"
            name1 = groups[1]  # "Lisa"
            name2 = groups[2]  # "Robert"

            # For "my [relation1] [name1] and [name2]" pattern
            # The second relation is typically implicit in the sentence
            # We need to parse it from the text around the match

            # Simple heuristic: look for another relation word near name2
            text_snippet = text[max(0, match.start()-20):match.end()+20]

            relation2 = None
            for rel_list in self.relationship_types.values():
                for rel in rel_list:
                    if rel in text_snippet.lower() and rel != relation1:
                        relation2 = rel
                        break
                if relation2:
                    break

            extractions = []

            # First extraction
            if self._is_valid_relation(relation1):
                extractions.append({
                    'relation': relation1,
                    'name': name1,
                    'confidence': pattern_config['confidence'] * 0.90,
                })

            # Second extraction (if relation found)
            if relation2 and self._is_valid_relation(relation2):
                extractions.append({
                    'relation': relation2,
                    'name': name2,
                    'confidence': pattern_config['confidence'] * 0.85,  # Slightly lower (inferred)
                })

            return extractions if extractions else None

        return None

    def _is_valid_relation(self, relation: str) -> bool:
        """Check if relation term is in our vocabulary."""
        if not relation:
            return False

        # Check singular and plural forms
        singular = relation.rstrip('s')
        return relation in self.all_relations or singular in self.all_relations

    def _categorize_relation(self, relation: str) -> str:
        """Categorize relation type (family, friend, colleague, other)."""
        # Check each category
        for category, terms in self.relationship_types.items():
            if relation in terms or relation.rstrip('s') in terms:
                if category in ['immediate_family', 'extended_family']:
                    return 'family'
                elif category == 'social':
                    # Distinguish friend vs colleague vs other
                    if relation in ['friend', 'buddy', 'pal', 'roommate', 'housemate']:
                        return 'friend'
                    elif relation in ['colleague', 'coworker', 'teammate']:
                        return 'colleague'
                    else:
                        return 'other'

        return 'other'

    def _deduplicate(self, relations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate entries (same name + relation)."""
        seen = set()
        unique = []

        for rel in relations:
            key = (rel['name'], rel['relation'])
            if key not in seen:
                seen.add(key)
                unique.append(rel)

        return unique

    def extract_with_context(
        self,
        text: str,
        existing_entities: Optional[Dict[str, Any]] = None,
        confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Extract relationships with awareness of existing entities.

        Useful for:
        - Detecting updates ("I used to have a son" vs "I have a son")
        - Disambiguation (multiple people with same name)

        Args:
            text: User's message
            existing_entities: Previously stored entities
            confidence_threshold: Minimum confidence

        Returns:
            Dict with new extractions and conflict flags
        """
        new_extractions = self.extract(text, confidence_threshold)

        if not existing_entities:
            return {
                'extractions': new_extractions,
                'conflicts': [],
                'updates': []
            }

        conflicts = []
        updates = []

        # Check for conflicts with existing entities
        for category in ['family_members', 'friends', 'colleagues']:
            if category in existing_entities:
                existing = existing_entities[category]
                new = new_extractions[category]

                # Simple conflict detection: same relation, different name
                for new_rel in new:
                    for existing_rel in existing:
                        if new_rel['relation'] == existing_rel['relation']:
                            if new_rel['name'] != existing_rel['name']:
                                conflicts.append({
                                    'type': 'different_name_same_relation',
                                    'existing': existing_rel,
                                    'new': new_rel,
                                    'category': category
                                })

        return {
            'extractions': new_extractions,
            'conflicts': conflicts,
            'updates': updates
        }


# Quick test function
def test_relationship_extractor():
    """Quick test of relationship extractor."""
    extractor = RelationshipExtractor()

    test_cases = [
        "my daughter Alice",
        "I have a son named Jake",
        "my father John lives in Boston",
        "Alice is my daughter",
        "I have two sons, John and Paul",
        "my friend Sarah and I went hiking"
    ]

    print("🧪 Testing Relationship Extractor\n")

    for text in test_cases:
        print(f"Input: \"{text}\"")
        result = extractor.extract(text)

        # Print non-empty categories
        for category, relations in result.items():
            if relations:
                print(f"  {category}:")
                for rel in relations:
                    print(f"    - {rel['name']} ({rel['relation']}) [conf={rel['confidence']:.2f}]")

        if not any(result.values()):
            print("  (no relationships extracted)")

        print()


if __name__ == '__main__':
    test_relationship_extractor()
