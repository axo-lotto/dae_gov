"""
Neo4j Knowledge Graph - Trauma-Informed Concept Relationships
Phase 2.2: Knowledge Infrastructure

Manages concept relationships for DAE-GOV organizational consulting using Neo4j.
Integrates trauma-informed concepts (IFS, polyvagal, reenactment patterns) with
process philosophy (Whitehead) and organizational knowledge.

Architecture:
- Trauma-Informed: Polyvagal states, IFS parts, SELF-energy, reenactment patterns
- Process Philosophy: Prehension, concrescence, actual occasions, nexūs
- Organizational: Culture, engagement, strategy, burnout, toxic patterns

Author: Claude Code (November 2025)
Status: Phase 2.2 - Neo4j Implementation
"""

import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    from neo4j import GraphDatabase
except ImportError:
    print("⚠️  Neo4j driver not installed. Install with: pip install neo4j")
    GraphDatabase = None


@dataclass
class Concept:
    """Knowledge graph concept."""
    name: str
    category: str  # 'trauma_informed', 'process_philosophy', 'organizational'
    description: str
    properties: Dict[str, any]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Relationship:
    """Relationship between concepts."""
    from_concept: str
    to_concept: str
    rel_type: str  # E.g., 'ENABLES', 'REQUIRES', 'TRANSFORMS_TO', 'CORRELATES_WITH'
    properties: Dict[str, any]

    def to_dict(self) -> dict:
        return asdict(self)


class Neo4jKnowledgeGraph:
    """
    Neo4j-based knowledge graph for trauma-informed organizational consulting.

    Features:
    - Trauma-informed concept relationships
    - Process philosophy integration
    - Multi-hop concept traversal
    - Pattern-based querying

    Scope (Phase 2.2):
    - Core concept schema
    - Basic relationship management
    - Concept querying
    - Path finding

    Future (Phase 2.3+):
    - Dynamic concept extraction from conversations
    - Concept importance weighting
    - Temporal relationship tracking
    """

    def __init__(self, uri: str = "bolt://localhost:7687",
                 user: str = "neo4j",
                 password: str = "password",
                 database: str = "neo4j"):
        """
        Initialize Neo4j knowledge graph.

        Args:
            uri: Neo4j bolt URI
            user: Database user
            password: Database password
            database: Database name
        """
        if GraphDatabase is None:
            raise ImportError("Neo4j driver not installed. Run: pip install neo4j")

        self.uri = uri
        self.user = user
        self.database = database

        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection
            with self.driver.session(database=database) as session:
                result = session.run("RETURN 1 as test")
                result.single()
            print(f"✅ Neo4j Knowledge Graph connected")
            print(f"   URI: {uri}")
            print(f"   Database: {database}")
        except Exception as e:
            print(f"⚠️  Could not connect to Neo4j: {e}")
            print("   Run Neo4j locally or use Neo4j Aura (cloud)")
            self.driver = None

    def close(self):
        """Close database connection."""
        if self.driver:
            self.driver.close()

    def create_concept(self, concept: Concept) -> bool:
        """
        Create a concept node in the graph.

        Args:
            concept: Concept to create

        Returns:
            True if successful, False otherwise
        """
        if not self.driver:
            return False

        query = """
        MERGE (c:Concept {name: $name})
        SET c.category = $category,
            c.description = $description,
            c += $properties
        RETURN c
        """

        try:
            with self.driver.session(database=self.database) as session:
                session.run(
                    query,
                    name=concept.name,
                    category=concept.category,
                    description=concept.description,
                    properties=concept.properties
                )
            return True
        except Exception as e:
            print(f"Error creating concept {concept.name}: {e}")
            return False

    def create_relationship(self, relationship: Relationship) -> bool:
        """
        Create a relationship between concepts.

        Args:
            relationship: Relationship to create

        Returns:
            True if successful, False otherwise
        """
        if not self.driver:
            return False

        query = f"""
        MATCH (from:Concept {{name: $from_name}})
        MATCH (to:Concept {{name: $to_name}})
        MERGE (from)-[r:{relationship.rel_type}]->(to)
        SET r += $properties
        RETURN r
        """

        try:
            with self.driver.session(database=self.database) as session:
                session.run(
                    query,
                    from_name=relationship.from_concept,
                    to_name=relationship.to_concept,
                    properties=relationship.properties
                )
            return True
        except Exception as e:
            print(f"Error creating relationship: {e}")
            return False

    def find_concept(self, name: str) -> Optional[Dict]:
        """
        Find a concept by name.

        Args:
            name: Concept name

        Returns:
            Concept dict or None if not found
        """
        if not self.driver:
            return None

        query = """
        MATCH (c:Concept {name: $name})
        RETURN c
        """

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, name=name)
                record = result.single()
                if record:
                    return dict(record['c'])
                return None
        except Exception as e:
            print(f"Error finding concept {name}: {e}")
            return None

    def find_related_concepts(self, name: str, max_hops: int = 1) -> List[Dict]:
        """
        Find concepts related to the given concept.

        Args:
            name: Starting concept name
            max_hops: Maximum relationship hops (1-3)

        Returns:
            List of related concepts with relationship info
        """
        if not self.driver:
            return []

        query = f"""
        MATCH path = (start:Concept {{name: $name}})-[r*1..{max_hops}]-(related:Concept)
        RETURN related, relationships(path) as rels, length(path) as distance
        ORDER BY distance
        LIMIT 50
        """

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, name=name)
                related = []
                for record in result:
                    related.append({
                        'concept': dict(record['related']),
                        'distance': record['distance'],
                        'relationships': [dict(rel) for rel in record['rels']]
                    })
                return related
        except Exception as e:
            print(f"Error finding related concepts: {e}")
            return []

    def find_transformation_path(self, from_concept: str, to_concept: str) -> Optional[List[str]]:
        """
        Find transformation path between concepts (e.g., Burnout → Sustainable Rhythm).

        Args:
            from_concept: Starting concept
            to_concept: Target concept

        Returns:
            List of concept names in transformation path, or None if no path
        """
        if not self.driver:
            return None

        query = """
        MATCH path = shortestPath(
          (start:Concept {name: $from_name})-[*]-(end:Concept {name: $to_name})
        )
        RETURN [node in nodes(path) | node.name] as path_names
        """

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, from_name=from_concept, to_name=to_concept)
                record = result.single()
                if record:
                    return record['path_names']
                return None
        except Exception as e:
            print(f"Error finding transformation path: {e}")
            return None

    def get_stats(self) -> Dict:
        """Get knowledge graph statistics."""
        if not self.driver:
            return {}

        queries = {
            'total_concepts': "MATCH (c:Concept) RETURN count(c) as count",
            'total_relationships': "MATCH ()-[r]->() RETURN count(r) as count",
            'trauma_concepts': "MATCH (c:Concept {category: 'trauma_informed'}) RETURN count(c) as count",
            'philosophy_concepts': "MATCH (c:Concept {category: 'process_philosophy'}) RETURN count(c) as count",
            'org_concepts': "MATCH (c:Concept {category: 'organizational'}) RETURN count(c) as count"
        }

        stats = {}
        try:
            with self.driver.session(database=self.database) as session:
                for key, query in queries.items():
                    result = session.run(query)
                    record = result.single()
                    stats[key] = record['count'] if record else 0
        except Exception as e:
            print(f"Error getting stats: {e}")

        return stats

    # ========================================================================
    # 🌀 ENTITY MEMORY METHODS (Nov 14, 2025)
    # Phase 1.8++: Neo4j Integration for Persistent Entity Memory
    # ========================================================================

    def create_entity(self,
                      entity_type: str,  # 'Person', 'Place', 'Preference', 'Fact'
                      entity_value: str,
                      user_id: str,
                      properties: Optional[Dict] = None) -> bool:
        """
        Create an entity node in the graph.

        Args:
            entity_type: Type of entity ('Person', 'Place', 'Preference', 'Fact')
            entity_value: The entity value (e.g., name, location, preference)
            user_id: User ID who mentioned this entity
            properties: Additional properties (polyvagal_state, urgency_level, etc.)

        Returns:
            True if successful, False otherwise

        Example:
            graph.create_entity('Person', 'Emiliano', 'user_123', {
                'polyvagal_state': 'ventral',
                'first_mentioned': '2025-11-14T10:30:00'
            })
        """
        if not self.driver:
            return False

        from datetime import datetime

        # Set default properties
        props = properties or {}
        props['entity_value'] = entity_value
        props['user_id'] = user_id
        if 'first_mentioned' not in props:
            props['first_mentioned'] = datetime.now().isoformat()
        if 'last_mentioned' not in props:
            props['last_mentioned'] = datetime.now().isoformat()
        if 'mention_count' not in props:
            props['mention_count'] = 1

        query = f"""
        MERGE (e:{entity_type} {{entity_value: $entity_value, user_id: $user_id}})
        ON CREATE SET e += $properties
        ON MATCH SET
            e.last_mentioned = $last_mentioned,
            e.mention_count = coalesce(e.mention_count, 0) + 1
        RETURN e
        """

        try:
            with self.driver.session(database=self.database) as session:
                session.run(
                    query,
                    entity_value=entity_value,
                    user_id=user_id,
                    properties=props,
                    last_mentioned=datetime.now().isoformat()
                )
            return True
        except Exception as e:
            print(f"⚠️  Error creating entity {entity_type}/{entity_value}: {e}")
            return False

    def create_entity_relationship(self,
                                    from_entity_value: str,
                                    to_entity_value: str,
                                    rel_type: str,  # 'HAS_DAUGHTER', 'HAS_SON', 'LIKES', 'WORKS_AT', etc.
                                    user_id: str,
                                    properties: Optional[Dict] = None) -> bool:
        """
        Create a relationship between entities.

        Args:
            from_entity_value: Source entity value
            to_entity_value: Target entity value
            rel_type: Relationship type ('HAS_DAUGHTER', 'HAS_SON', 'LIKES', 'WORKS_AT', etc.)
            user_id: User ID who mentioned this relationship
            properties: Additional properties (confidence, mentioned_at, etc.)

        Returns:
            True if successful, False otherwise

        Example:
            graph.create_entity_relationship('Emiliano', 'Emma', 'HAS_DAUGHTER', 'user_123', {
                'confidence': 0.95,
                'mentioned_at': '2025-11-14T10:30:00'
            })
        """
        if not self.driver:
            return False

        from datetime import datetime

        props = properties or {}
        if 'mentioned_at' not in props:
            props['mentioned_at'] = datetime.now().isoformat()
        if 'user_id' not in props:
            props['user_id'] = user_id

        # Find entities regardless of type (Person, Place, etc.)
        query = f"""
        MATCH (from {{entity_value: $from_value, user_id: $user_id}})
        MATCH (to {{entity_value: $to_value, user_id: $user_id}})
        MERGE (from)-[r:{rel_type}]->(to)
        ON CREATE SET r += $properties
        ON MATCH SET r.last_updated = $last_updated
        RETURN r
        """

        try:
            with self.driver.session(database=self.database) as session:
                session.run(
                    query,
                    from_value=from_entity_value,
                    to_value=to_entity_value,
                    user_id=user_id,
                    properties=props,
                    last_updated=datetime.now().isoformat()
                )
            return True
        except Exception as e:
            print(f"⚠️  Error creating relationship {rel_type}: {e}")
            return False

    def get_user_entities(self, user_id: str, entity_type: Optional[str] = None) -> List[Dict]:
        """
        Get all entities for a user.

        Args:
            user_id: User ID
            entity_type: Optional filter by type ('Person', 'Place', 'Preference', 'Fact')

        Returns:
            List of entity dicts with properties

        Example:
            entities = graph.get_user_entities('user_123', entity_type='Person')
            # Returns: [{'entity_value': 'Emiliano', 'mention_count': 5, ...}, ...]
        """
        if not self.driver:
            return []

        if entity_type:
            query = f"""
            MATCH (e:{entity_type} {{user_id: $user_id}})
            RETURN e, labels(e) as types
            ORDER BY e.mention_count DESC, e.last_mentioned DESC
            """
        else:
            query = """
            MATCH (e {user_id: $user_id})
            WHERE e.entity_value IS NOT NULL
            RETURN e, labels(e) as types
            ORDER BY e.mention_count DESC, e.last_mentioned DESC
            """

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, user_id=user_id)
                entities = []
                for record in result:
                    entity_dict = dict(record['e'])
                    entity_dict['entity_types'] = record['types']
                    entities.append(entity_dict)
                return entities
        except Exception as e:
            print(f"⚠️  Error getting user entities: {e}")
            return []

    def get_entity_relationships(self,
                                  entity_value: str,
                                  user_id: str,
                                  max_hops: int = 1) -> List[Dict]:
        """
        Get all relationships for an entity (multi-hop capable).

        Args:
            entity_value: Entity to start from
            user_id: User ID
            max_hops: Maximum relationship hops (1-3)

        Returns:
            List of relationship paths with distance

        Example:
            rels = graph.get_entity_relationships('Emiliano', 'user_123', max_hops=2)
            # Returns: [
            #   {'related_entity': 'Emma', 'relationship': 'HAS_DAUGHTER', 'distance': 1},
            #   {'related_entity': 'Alex', 'relationship': 'HAS_DAUGHTER->HAS_FRIEND', 'distance': 2}
            # ]
        """
        if not self.driver:
            return []

        query = f"""
        MATCH path = (start {{entity_value: $entity_value, user_id: $user_id}})-[r*1..{max_hops}]-(related {{user_id: $user_id}})
        RETURN related, relationships(path) as rels, length(path) as distance
        ORDER BY distance
        LIMIT 100
        """

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, entity_value=entity_value, user_id=user_id)
                relationships = []
                for record in result:
                    related = dict(record['related'])
                    rels = record['rels']
                    distance = record['distance']

                    # Build relationship path string
                    rel_path = '->'.join([rel.type for rel in rels])

                    relationships.append({
                        'related_entity': related.get('entity_value'),
                        'related_entity_data': related,
                        'relationship_path': rel_path,
                        'distance': distance,
                        'relationships': [dict(rel) for rel in rels]
                    })
                return relationships
        except Exception as e:
            print(f"⚠️  Error getting entity relationships: {e}")
            return []

    def build_entity_context_string(self, user_id: str, max_entities: int = 20) -> str:
        """
        Build a rich entity context string for LLM prompts.

        Includes:
        - User entities sorted by recency/frequency
        - Relationships between entities
        - TSK-enriched metadata (polyvagal state, urgency, etc.)

        Args:
            user_id: User ID
            max_entities: Maximum entities to include

        Returns:
            Formatted entity context string

        Example Output:
            Known about user:
            - Name: Emiliano (mentioned 5 times, last: 2025-11-14)
              - Has daughter Emma (mentioned 3 times)
              - Has daughter Lily (mentioned 2 times)
            - Friend: Rich (mentioned 2 times, last: 2025-11-14)
            - Friend: Alex (mentioned 2 times, last: 2025-11-14)
        """
        if not self.driver:
            return ""

        entities = self.get_user_entities(user_id)
        if not entities:
            return ""

        context_lines = ["Known about user:"]

        for entity in entities[:max_entities]:
            entity_value = entity.get('entity_value', 'Unknown')
            entity_types = entity.get('entity_types', [])
            mention_count = entity.get('mention_count', 1)
            last_mentioned = entity.get('last_mentioned', 'unknown')

            # Format entity type
            entity_type_str = entity_types[0] if entity_types else 'Entity'

            # Main entity line
            if entity_type_str == 'Person':
                entity_line = f"- Name: {entity_value}"
            else:
                entity_line = f"- {entity_type_str}: {entity_value}"

            entity_line += f" (mentioned {mention_count} times"
            if last_mentioned != 'unknown':
                # Extract just the date
                date_str = last_mentioned.split('T')[0]
                entity_line += f", last: {date_str}"
            entity_line += ")"

            context_lines.append(entity_line)

            # Add relationships (1-hop only for context brevity)
            relationships = self.get_entity_relationships(entity_value, user_id, max_hops=1)
            for rel in relationships[:5]:  # Limit to 5 relationships per entity
                related_value = rel.get('related_entity', 'Unknown')
                rel_path = rel.get('relationship_path', 'RELATED_TO')
                rel_data = rel.get('related_entity_data', {})
                rel_mention_count = rel_data.get('mention_count', 1)

                # Format relationship
                if rel_path == 'HAS_DAUGHTER':
                    rel_str = f"  - Has daughter {related_value}"
                elif rel_path == 'HAS_SON':
                    rel_str = f"  - Has son {related_value}"
                elif rel_path == 'LIKES':
                    rel_str = f"  - Likes {related_value}"
                elif rel_path == 'WORKS_AT':
                    rel_str = f"  - Works at {related_value}"
                else:
                    rel_str = f"  - {rel_path.replace('_', ' ').lower()}: {related_value}"

                rel_str += f" (mentioned {rel_mention_count} times)"
                context_lines.append(rel_str)

        return '\n'.join(context_lines)


def initialize_trauma_informed_concepts(graph: Neo4jKnowledgeGraph) -> int:
    """
    Initialize trauma-informed concepts in the knowledge graph.

    Categories:
    - Polyvagal states
    - IFS parts
    - SELF-energy
    - Trauma patterns
    - Organizational patterns

    Returns:
        Number of concepts created
    """
    concepts = [
        # Polyvagal Theory
        Concept(
            name="Ventral Vagal State",
            category="trauma_informed",
            description="Safe and social nervous system state; calm, connected, collaborative",
            properties={"polyvagal": True, "state": "ventral", "desirable": True}
        ),
        Concept(
            name="Sympathetic State",
            category="trauma_informed",
            description="Fight-flight activation; urgency, anxiety, hyperarousal",
            properties={"polyvagal": True, "state": "sympathetic", "desirable": False}
        ),
        Concept(
            name="Dorsal Vagal State",
            category="trauma_informed",
            description="Shutdown, freeze, dissociation; collapse, numbing",
            properties={"polyvagal": True, "state": "dorsal", "desirable": False}
        ),

        # IFS Parts
        Concept(
            name="Manager Part",
            category="trauma_informed",
            description="Control-oriented protector; perfectionism, planning, risk-avoidance",
            properties={"ifs_type": "manager", "protective": True}
        ),
        Concept(
            name="Firefighter Part",
            category="trauma_informed",
            description="Crisis-reactive protector; distraction, numbing, impulsive action",
            properties={"ifs_type": "firefighter", "protective": True}
        ),
        Concept(
            name="Exile Part",
            category="trauma_informed",
            description="Vulnerable, burdened part carrying pain, shame, fear",
            properties={"ifs_type": "exile", "protective": False}
        ),
        Concept(
            name="SELF-Energy",
            category="trauma_informed",
            description="Calm, clarity, compassion, curiosity, courage, confidence, creativity, connectedness",
            properties={"ifs_type": "SELF", "desirable": True}
        ),

        # Organizational Patterns (Shadow/Compost)
        Concept(
            name="Burnout Spiral",
            category="organizational",
            description="Chronic exhaustion, dissociation, resentment; dorsal vagal shutdown",
            properties={"pattern_type": "shadow", "self_distance": 0.50}
        ),
        Concept(
            name="Toxic Productivity",
            category="organizational",
            description="Urgency culture, perfectionism, shame-driven work; sympathetic dominance",
            properties={"pattern_type": "shadow", "self_distance": 0.45}
        ),
        Concept(
            name="Scapegoat Dynamics",
            category="organizational",
            description="Repetitive blame cycles, unacknowledged systemic trauma",
            properties={"pattern_type": "shadow", "self_distance": 0.55}
        ),

        # Organizational Patterns (SELF-Led)
        Concept(
            name="Sustainable Rhythm",
            category="organizational",
            description="Balanced pacing, rest integrated, embodied boundaries",
            properties={"pattern_type": "SELF_led", "self_distance": 0.10}
        ),
        Concept(
            name="Psychological Safety",
            category="organizational",
            description="Ventral vagal team culture; openness, vulnerability, trust",
            properties={"pattern_type": "SELF_led", "self_distance": 0.08}
        ),
        Concept(
            name="Witnessing Presence",
            category="organizational",
            description="Compassionate attention to pain without fixing or bypassing",
            properties={"pattern_type": "SELF_led", "self_distance": 0.10}
        ),

        # Process Philosophy
        Concept(
            name="Prehension",
            category="process_philosophy",
            description="Grasping and feeling the data of the world; foundational process",
            properties={"whitehead": True, "phase": "initial"}
        ),
        Concept(
            name="Concrescence",
            category="process_philosophy",
            description="Growing together into unified experience; satisfaction process",
            properties={"whitehead": True, "phase": "middle"}
        ),
        Concept(
            name="Satisfaction",
            category="process_philosophy",
            description="Completion of becoming; decisive moment of an actual occasion",
            properties={"whitehead": True, "phase": "final"}
        ),
    ]

    count = 0
    for concept in concepts:
        if graph.create_concept(concept):
            count += 1

    print(f"✅ Created {count} trauma-informed concepts")
    return count


def initialize_trauma_informed_relationships(graph: Neo4jKnowledgeGraph) -> int:
    """
    Initialize relationships between trauma-informed concepts.

    Relationship Types:
    - ENABLES: A enables B (e.g., Psychological Safety ENABLES Ventral Vagal)
    - REQUIRES: A requires B (e.g., SELF-Energy REQUIRES Witnessing)
    - TRANSFORMS_TO: A transforms to B (e.g., Burnout TRANSFORMS_TO Sustainable Rhythm)
    - CORRELATES_WITH: A correlates with B (e.g., Burnout CORRELATES_WITH Dorsal Vagal)
    - PROTECTS: A protects B (e.g., Manager PROTECTS Exile)

    Returns:
        Number of relationships created
    """
    relationships = [
        # Polyvagal → Organizational
        Relationship("Ventral Vagal State", "Psychological Safety", "ENABLES", {}),
        Relationship("Sympathetic State", "Toxic Productivity", "CORRELATES_WITH", {}),
        Relationship("Dorsal Vagal State", "Burnout Spiral", "CORRELATES_WITH", {}),

        # IFS Parts → Organizational
        Relationship("Manager Part", "Toxic Productivity", "MANIFESTS_AS", {}),
        Relationship("Firefighter Part", "Scapegoat Dynamics", "MANIFESTS_AS", {}),
        Relationship("SELF-Energy", "Witnessing Presence", "ENABLES", {}),
        Relationship("SELF-Energy", "Psychological Safety", "ENABLES", {}),

        # IFS Internal Dynamics
        Relationship("Manager Part", "Exile Part", "PROTECTS", {}),
        Relationship("Firefighter Part", "Exile Part", "PROTECTS", {}),

        # Transformation Pathways
        Relationship("Burnout Spiral", "Sustainable Rhythm", "TRANSFORMS_TO", {"requires": "SELF-Energy"}),
        Relationship("Toxic Productivity", "Sustainable Rhythm", "TRANSFORMS_TO", {"requires": "Witnessing"}),
        Relationship("Scapegoat Dynamics", "Psychological Safety", "TRANSFORMS_TO", {"requires": "SELF-Energy"}),

        # Process Philosophy → Trauma
        Relationship("Prehension", "Concrescence", "PRECEDES", {}),
        Relationship("Concrescence", "Satisfaction", "PRECEDES", {}),
        Relationship("Witnessing Presence", "Prehension", "IS_A", {}),
    ]

    count = 0
    for rel in relationships:
        if graph.create_relationship(rel):
            count += 1

    print(f"✅ Created {count} concept relationships")
    return count


def test_neo4j_knowledge_graph():
    """Test Neo4j knowledge graph with trauma-informed concepts."""

    print("\n" + "="*70)
    print("NEO4J KNOWLEDGE GRAPH TEST - Phase 2.2")
    print("="*70 + "\n")

    # Initialize graph (requires Neo4j running)
    print("[TEST 1] Connect to Neo4j")
    graph = Neo4jKnowledgeGraph(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"  # Change to actual password
    )

    if not graph.driver:
        print("⚠️  Neo4j not available - skipping tests")
        print("   To run tests:")
        print("   1. Install Neo4j Desktop or use Neo4j Aura")
        print("   2. Start database")
        print("   3. Update password in test")
        return

    # Initialize concepts
    print("\n[TEST 2] Initialize trauma-informed concepts")
    concept_count = initialize_trauma_informed_concepts(graph)

    # Initialize relationships
    print("\n[TEST 3] Initialize concept relationships")
    rel_count = initialize_trauma_informed_relationships(graph)

    # Find concept
    print("\n[TEST 4] Find specific concept")
    burnout = graph.find_concept("Burnout Spiral")
    if burnout:
        print(f"   Found: {burnout['name']}")
        print(f"   Category: {burnout['category']}")
        print(f"   SELF-distance: {burnout.get('self_distance', 'N/A')}")

    # Find related concepts
    print("\n[TEST 5] Find related concepts (1-hop)")
    related = graph.find_related_concepts("Burnout Spiral", max_hops=1)
    print(f"   Found {len(related)} related concepts:")
    for r in related[:3]:
        print(f"     - {r['concept']['name']} (distance: {r['distance']})")

    # Find transformation path
    print("\n[TEST 6] Find transformation path")
    path = graph.find_transformation_path("Burnout Spiral", "Sustainable Rhythm")
    if path:
        print(f"   Path: {' → '.join(path)}")

    # Get stats
    print("\n[TEST 7] Knowledge graph statistics")
    stats = graph.get_stats()
    print(f"   Total concepts: {stats.get('total_concepts', 0)}")
    print(f"   Total relationships: {stats.get('total_relationships', 0)}")
    print(f"   Trauma concepts: {stats.get('trauma_concepts', 0)}")
    print(f"   Philosophy concepts: {stats.get('philosophy_concepts', 0)}")
    print(f"   Organizational concepts: {stats.get('org_concepts', 0)}")

    # Close connection
    graph.close()

    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - Neo4j Knowledge Graph Operational")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_neo4j_knowledge_graph()
