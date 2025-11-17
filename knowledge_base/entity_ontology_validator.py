"""
Entity Ontology Validator - Whiteheadian Process Philosophy + Common-Sense
===========================================================================

Validates entity extraction against Whiteheadian ontology to prevent
garbage entity creation and enable category-aware salience initialization.

Philosophy (Whitehead):
- Actual Occasions → Conversational turns
- Eternal Objects → Concepts, patterns, values
- Societies → Persistent entities (people, places, organizations)
- Nexus → Relationships between societies

Integration:
- Called by dae_interactive.py BEFORE Neo4j storage
- Filters stopwords, validates categories, maps to ontology
- Returns enriched entities with ontology_category and salience_base

Author: DAE_HYPHAE_1 + Claude Code
Date: November 17, 2025
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of entity validation."""
    is_valid: bool
    reason: Optional[str] = None
    ontology_category: Optional[str] = None
    process_mapping: Optional[str] = None
    salience_base: float = 0.5


class EntityOntologyValidator:
    """
    Validate entities against Whiteheadian ontology.

    Prevents garbage entity creation by:
    1. Filtering stopwords ("feeling", "do", "your", etc.)
    2. Validating proper capitalization for Person/Place
    3. Requiring relationship context for Person entities
    4. Mapping entities to ontology categories
    5. Initializing category-aware salience

    Philosophy Integration:
    - Person → Personal Society (Whitehead)
    - Place → Physical Society
    - Concept → Eternal Object
    - Organization → Structured Society
    """

    def __init__(self, ontology_path: str = None):
        """
        Initialize entity ontology validator.

        Args:
            ontology_path: Path to whiteheadian_entity_ontology.json
        """
        if ontology_path is None:
            ontology_path = Path(__file__).parent / "whiteheadian_entity_ontology.json"
        else:
            ontology_path = Path(ontology_path)

        # Load ontology
        self.ontology = self._load_ontology(ontology_path)

        # Extract validation components
        self.stopwords = set(self.ontology['validation_rules']['stopwords_blacklist'])
        self.salience_bases = self.ontology['salience_initialization']['category_baselines']

        # Extract category hierarchies
        self._build_category_mappings()

        print(f"✅ EntityOntologyValidator initialized")
        print(f"   Stopwords: {len(self.stopwords)}")
        print(f"   Salience categories: {len(self.salience_bases)}")

    def _load_ontology(self, path: Path) -> Dict:
        """Load Whiteheadian ontology from JSON."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading ontology: {e}")
            return {}

    def _build_category_mappings(self):
        """Build category lookup structures from ontology."""
        common_sense = self.ontology['ontology_structure']['common_sense_surface']

        # Person relationships
        self.person_relationships = {}
        for category_name, category_data in common_sense['person']['categories'].items():
            for rel in category_data['relationships']:
                self.person_relationships[rel] = f"Person::{category_name}"

        # Place types
        self.place_types = {}
        for category_name, category_data in common_sense['place']['categories'].items():
            for place_type in category_data['types']:
                self.place_types[place_type] = f"Place::{category_name}"

        # Concept types
        self.concept_types = {}
        for category_name, category_data in common_sense['concept']['categories'].items():
            for concept_type in category_data['types']:
                self.concept_types[concept_type] = f"Concept::{category_name}"

    def is_stopword(self, entity_value: str) -> bool:
        """Check if entity value is a stopword."""
        return entity_value.lower() in self.stopwords

    def validate_capitalization(self, entity: Dict) -> bool:
        """
        Validate proper capitalization for Person/Place entities.

        Args:
            entity: Entity dict with entity_type and entity_value

        Returns:
            True if capitalization is valid
        """
        entity_type = entity.get('entity_type', '')
        entity_value = entity.get('entity_value', '')

        # Person and Place entities should start with capital letter
        if entity_type in ['Person', 'Place', 'Organization']:
            # Check if first character is uppercase
            if entity_value and entity_value[0].isupper():
                return True
            else:
                return False

        # Other types don't require capitalization
        return True

    def map_to_category(self, entity: Dict) -> ValidationResult:
        """
        Map entity to ontology category.

        Args:
            entity: Entity dict with entity_type, entity_value, and optional relationship

        Returns:
            ValidationResult with ontology_category and salience_base
        """
        entity_type = entity.get('entity_type', '')
        entity_value = entity.get('entity_value', '')
        relationship = entity.get('relationship', entity.get('properties', {}).get('relationship'))

        # Step 1: Check stopwords
        if self.is_stopword(entity_value):
            return ValidationResult(
                is_valid=False,
                reason=f"Stopword: '{entity_value}'"
            )

        # Step 2: Check minimum length
        if len(entity_value) < 2:
            return ValidationResult(
                is_valid=False,
                reason=f"Too short: '{entity_value}' (min 2 chars)"
            )

        # Step 3: Check capitalization for Person/Place
        if not self.validate_capitalization(entity):
            return ValidationResult(
                is_valid=False,
                reason=f"Invalid capitalization: '{entity_value}' (must start with capital)"
            )

        # Step 4: Map to ontology category
        if entity_type == 'Person':
            # Require relationship for Person
            if not relationship:
                return ValidationResult(
                    is_valid=False,
                    reason=f"Person entity missing relationship: '{entity_value}'"
                )

            # Map relationship to category
            ontology_category = self.person_relationships.get(relationship)
            if not ontology_category:
                # Unknown relationship → default to social
                ontology_category = "Person::social"

            # Get salience base
            salience_key = ontology_category.replace('::', '::')
            salience_base = self.salience_bases.get(salience_key, 0.5)

            # Special case: therapist gets higher salience
            if relationship == 'therapist':
                salience_base = self.salience_bases.get("Person::professional::therapist", 0.85)

            return ValidationResult(
                is_valid=True,
                ontology_category=ontology_category,
                process_mapping="Personal Society",
                salience_base=salience_base
            )

        elif entity_type == 'Place':
            # Extract place_type from properties
            place_type = entity.get('place_type', entity.get('properties', {}).get('place_type'))

            if place_type:
                ontology_category = self.place_types.get(place_type)
                if not ontology_category:
                    ontology_category = "Place::public"  # Default
            else:
                ontology_category = "Place::public"  # Default

            salience_base = self.salience_bases.get(ontology_category.replace('::', '::'), 0.4)

            return ValidationResult(
                is_valid=True,
                ontology_category=ontology_category,
                process_mapping="Physical Society",
                salience_base=salience_base
            )

        elif entity_type == 'Concept':
            # Try to match concept to categories
            entity_lower = entity_value.lower()
            ontology_category = None

            for concept_type, category in self.concept_types.items():
                if concept_type in entity_lower or entity_lower in concept_type:
                    ontology_category = category
                    break

            if not ontology_category:
                ontology_category = "Concept::philosophical"  # Default

            salience_base = self.salience_bases.get(ontology_category.replace('::', '::'), 0.6)

            return ValidationResult(
                is_valid=True,
                ontology_category=ontology_category,
                process_mapping="Eternal Object",
                salience_base=salience_base
            )

        elif entity_type == 'Preference':
            # Extract preference type
            pref_type = entity.get('preference_type', 'likes')

            if pref_type in ['likes', 'dislikes', 'interests', 'goals']:
                ontology_category = f"Preference::{pref_type}"
            else:
                ontology_category = "Preference::likes"  # Default

            salience_base = self.salience_bases.get(ontology_category.replace('::', '::'), 0.5)

            return ValidationResult(
                is_valid=True,
                ontology_category=ontology_category,
                process_mapping="Eternal Object",
                salience_base=salience_base
            )

        elif entity_type == 'Organization':
            ontology_category = "Organization"
            salience_base = self.salience_bases.get("Organization", 0.6)

            return ValidationResult(
                is_valid=True,
                ontology_category=ontology_category,
                process_mapping="Structured Society",
                salience_base=salience_base
            )

        else:
            # Unknown entity type
            return ValidationResult(
                is_valid=False,
                reason=f"Unknown entity type: '{entity_type}'"
            )

    def validate_entities(self, entities: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Validate list of entities and enrich with ontology data.

        Args:
            entities: List of entity dicts from extraction

        Returns:
            Tuple of (valid_entities, rejected_entities)
        """
        valid_entities = []
        rejected_entities = []

        for entity in entities:
            result = self.map_to_category(entity)

            if result.is_valid:
                # Enrich entity with ontology data
                entity['ontology_category'] = result.ontology_category
                entity['process_mapping'] = result.process_mapping
                entity['salience_base'] = result.salience_base
                valid_entities.append(entity)
            else:
                # Track rejected entity with reason
                entity['rejection_reason'] = result.reason
                rejected_entities.append(entity)

        return valid_entities, rejected_entities

    def get_salience_base(self, ontology_category: str) -> float:
        """Get salience base for ontology category."""
        return self.salience_bases.get(ontology_category.replace('::', '::'), 0.5)


# Module-level singleton for convenience
_default_validator = None

def get_default_validator() -> EntityOntologyValidator:
    """Get or create default EntityOntologyValidator singleton."""
    global _default_validator
    if _default_validator is None:
        _default_validator = EntityOntologyValidator()
    return _default_validator
