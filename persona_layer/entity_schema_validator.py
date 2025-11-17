"""
Entity Schema Validator
=======================

Validates entities against baseline schema template to prevent garbage entity creation.

Prevents issues like:
- Creating entity nodes for stopwords ("feeling", "about", "why", "to")
- Case-duplicates ("Emiliano" + "emiliano")
- Missing required fields (Person without relationship)
- Invalid relationship types

Date: November 16, 2025
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class EntitySchemaValidator:
    """Validates entities against schema template and filters garbage."""

    def __init__(self, schema_path: str = "knowledge_base/entity_schema_template.json"):
        """Initialize with schema template."""
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()

        # Extract validation rules
        self.stopwords = set()
        self.min_length = 2
        self.valid_relationship_types = set()
        self._extract_validation_rules()

    def _load_schema(self) -> Dict:
        """Load entity schema template."""
        try:
            with open(self.schema_path) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Schema template not found at {self.schema_path}, using minimal defaults")
            return self._get_minimal_schema()

    def _get_minimal_schema(self) -> Dict:
        """Minimal fallback schema if file not found."""
        return {
            "entity_validation_rules": {
                "rules": [
                    {
                        "rule_id": "no_stopwords",
                        "stopwords": ["the", "a", "an", "feeling", "about", "know", "to", "from", "more", "why"]
                    },
                    {
                        "rule_id": "min_entity_length",
                        "min_length": 2
                    }
                ]
            },
            "baseline_entity_schema": {
                "categories": [
                    {
                        "category": "FamilyRelationships",
                        "relationship_types": ["mother", "father", "sister", "brother", "daughter", "son"]
                    },
                    {
                        "category": "SocialRelationships",
                        "relationship_types": ["partner", "friend", "colleague", "therapist", "doctor"]
                    }
                ]
            }
        }

    def _extract_validation_rules(self):
        """Extract validation rules from schema."""
        rules = self.schema.get('entity_validation_rules', {}).get('rules', [])

        for rule in rules:
            if rule.get('rule_id') == 'no_stopwords':
                self.stopwords = set(word.lower() for word in rule.get('stopwords', []))
            elif rule.get('rule_id') == 'min_entity_length':
                self.min_length = rule.get('min_length', 2)

        # Extract valid relationship types
        categories = self.schema.get('baseline_entity_schema', {}).get('categories', [])
        for category in categories:
            if 'relationship_types' in category:
                self.valid_relationship_types.update(category['relationship_types'])

    def is_valid_entity_name(self, name: str) -> Tuple[bool, str]:
        """
        Check if entity name is valid.

        Returns:
            (is_valid, reason_if_invalid)
        """
        if not name:
            return False, "Empty name"

        # Check length
        if len(name) < self.min_length:
            return False, f"Too short (min {self.min_length} chars)"

        # Check if stopword
        if name.lower() in self.stopwords:
            return False, f"Stopword: '{name}' is a common word, not an entity"

        # Additional heuristics
        # Reject single lowercase words unless they're known to be valid
        if len(name.split()) == 1 and name.islower() and len(name) < 15:
            # Could be a stopword we missed
            if not self._is_likely_proper_noun(name):
                return False, f"Likely stopword: '{name}' (lowercase, short)"

        return True, ""

    def _is_likely_proper_noun(self, name: str) -> bool:
        """
        Heuristic to detect if name is likely a proper noun.

        Proper nouns typically:
        - Start with capital letter
        - Are specific names not general words
        """
        # If starts with capital, likely proper noun
        if name[0].isupper():
            return True

        # If multiple words with caps, likely proper noun
        if len(name.split()) > 1 and any(word[0].isupper() for word in name.split()):
            return True

        # Otherwise probably not
        return False

    def validate_person_entity(self, entity: Dict) -> Tuple[bool, str]:
        """
        Validate a Person entity.

        Checks:
        - Has 'name' field
        - Has 'relationship' field
        - Relationship type is valid
        - Name is valid entity name
        """
        name = entity.get('name')
        relationship = entity.get('relationship')

        # Check name validity
        name_valid, reason = self.is_valid_entity_name(name)
        if not name_valid:
            return False, f"Invalid name: {reason}"

        # Check relationship exists
        if not relationship:
            return False, "Person entity missing 'relationship' field"

        # Check relationship type is valid (if we have schema)
        if self.valid_relationship_types and relationship not in self.valid_relationship_types:
            return False, f"Unknown relationship type: '{relationship}'"

        return True, ""

    def normalize_person_name(self, name: str) -> str:
        """Normalize person name to prevent case duplicates."""
        # Capitalize first letter of each word
        return " ".join(word.capitalize() for word in name.split())

    def detect_duplicate_person(self, name: str, existing_entities: List[Dict]) -> Optional[Dict]:
        """
        Check if person entity already exists (case-insensitive).

        Returns:
            Existing entity if duplicate found, None otherwise
        """
        normalized_name = self.normalize_person_name(name)

        for entity in existing_entities:
            if entity.get('type') == 'person' or entity.get('relationship'):
                existing_name = entity.get('name', '')
                if self.normalize_person_name(existing_name) == normalized_name:
                    return entity

        return None

    def validate_and_filter_entities(self, entities: Dict, existing_entities: List[Dict] = None) -> Dict:
        """
        Validate all entities and filter out invalid ones.

        Args:
            entities: Dict with 'relationships', 'mentioned_names', etc.
            existing_entities: List of already-stored entities (for duplicate detection)

        Returns:
            Filtered dict with only valid entities
        """
        existing_entities = existing_entities or []
        filtered = {}

        # Validate relationships (Person entities)
        if 'relationships' in entities:
            valid_relationships = []
            for rel in entities['relationships']:
                # Validate
                is_valid, reason = self.validate_person_entity(rel)
                if not is_valid:
                    print(f"   ⚠️  Rejected person entity: {rel.get('name')} - {reason}")
                    continue

                # Check for duplicates
                duplicate = self.detect_duplicate_person(rel['name'], existing_entities)
                if duplicate:
                    print(f"   ⚠️  Skipping duplicate: {rel.get('name')} (already exists as {duplicate.get('name')})")
                    continue

                # Normalize name
                rel['name'] = self.normalize_person_name(rel['name'])
                valid_relationships.append(rel)

            if valid_relationships:
                filtered['relationships'] = valid_relationships

        # Validate mentioned_names (generic entities)
        if 'mentioned_names' in entities:
            valid_names = []
            for name in entities['mentioned_names']:
                is_valid, reason = self.is_valid_entity_name(name)
                if not is_valid:
                    print(f"   ⚠️  Rejected entity: {name} - {reason}")
                    continue

                valid_names.append(name)

            if valid_names:
                filtered['mentioned_names'] = valid_names

        # Validate preferences
        if 'preferences' in entities:
            # Preferences are more flexible, but still validate values
            prefs = entities['preferences']
            valid_prefs = {}

            for pref_type in ['likes', 'dislikes', 'interests', 'goals']:
                if pref_type in prefs:
                    valid_items = []
                    for item in prefs[pref_type]:
                        # Preferences can be short phrases, so less strict
                        if isinstance(item, str) and len(item) >= 2:
                            valid_items.append(item)

                    if valid_items:
                        valid_prefs[pref_type] = valid_items

            if valid_prefs:
                filtered['preferences'] = valid_prefs

        # Pass through other entity types (work, places, etc.)
        for key in ['work', 'places', 'health_mental']:
            if key in entities:
                filtered[key] = entities[key]

        return filtered

    def get_llm_extraction_prompt(self) -> str:
        """Get LLM prompt template for entity extraction."""
        return self.schema.get('llm_entity_extraction_prompt_template', {}).get('prompt', '')

    def initialize_user_baseline(self, user_id: str) -> Dict:
        """
        Create baseline entity structure for new user.

        Returns:
            Dict with empty but structured entity containers
        """
        example = self.schema.get('example_initialized_user', {})

        # Clone and set user_id
        baseline = {
            'user_id': user_id,
            'user_name': None,
            'age': None,
            'location': None,
            'relationships': [],
            'places': [],
            'work': {
                'company': None,
                'job_title': None,
                'industry': None,
                'work_location': None
            },
            'preferences': {
                'likes': [],
                'dislikes': [],
                'interests': [],
                'goals': []
            },
            'health_mental': {
                'diagnoses': [],
                'medications': [],
                'therapist_name': None,
                'treatment_history': []
            }
        }

        return baseline


# Singleton instance for easy import
_validator_instance = None

def get_validator() -> EntitySchemaValidator:
    """Get singleton validator instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = EntitySchemaValidator()
    return _validator_instance
