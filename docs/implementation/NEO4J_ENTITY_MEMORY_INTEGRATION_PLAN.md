# 🔧 Neo4j Entity Memory Integration Plan
**Date:** November 14, 2025
**Priority:** CRITICAL
**Goal:** Wire Neo4j knowledge graph for persistent entity memory

---

## Executive Summary

**Current State:**
- Neo4j infrastructure exists (`knowledge_base/neo4j_knowledge_graph.py`)
- Designed for trauma-informed concepts (IFS, polyvagal, organizational patterns)
- **NOT used for entity memory** (persons, relationships, facts)
- dae_interactive.py bypasses it completely

**Target State:**
- Neo4j stores ALL entities and relationships
- JSON fallback for offline/local-only mode
- Graph queries enrich entity context
- Temporal tracking of entity mentions
- Multi-hop relationship inference

---

## Architecture Design

### Dual-Storage Strategy

```
Entity Extraction
    ↓
PARALLEL STORAGE:
    ├─→ JSON (user_state.json)       ← Fast local cache, always works
    └─→ Neo4j (knowledge graph)       ← Rich relationships, when available

PARALLEL RETRIEVAL (on every turn):
    ├─→ JSON → entity_context_string  ← Basic entity list
    └─→ Neo4j → enriched context      ← Related entities, inferred facts
```

**Benefits:**
- **Resilience:** Works offline (JSON fallback)
- **Performance:** Fast JSON reads for basic context
- **Richness:** Neo4j provides deep relationship queries when available
- **Scalability:** Neo4j handles multi-user, cross-session queries

---

## Phase 1: Extend Neo4j for Entities

### 1.1 Add Entity Node Types

**New node labels:**
- `:Person` - Users, family members, friends, colleagues
- `:Place` - Locations, addresses, venues
- `:Preference` - Likes/dislikes, hobbies, interests
- `:Fact` - General knowledge about user
- `:Event` - Important dates, meetings, occurrences

**Example:**
```cypher
CREATE (p:Person {
  name: "Emiliano",
  user_id: "user_20251113_143117",
  entity_type: "user_name",
  first_mentioned: datetime(),
  mention_count: 1,
  confidence: 1.0
})
```

### 1.2 Add Relationship Types

**Entity relationships:**
- `HAS_DAUGHTER` - Parent → child
- `HAS_SON` - Parent → child
- `HAS_FRIEND` - Person → person
- `LIKES` - Person → preference/activity
- `DISLIKES` - Person → preference/activity
- `WORKS_AT` - Person → place/organization
- `LIVES_IN` - Person → place
- `MENTIONED_WITH` - Co-occurrence tracking

**Example:**
```cypher
MATCH (emiliano:Person {name: "Emiliano"})
MATCH (emma:Person {name: "Emma"})
CREATE (emiliano)-[:HAS_DAUGHTER {
  confidence: 0.95,
  first_mentioned: datetime(),
  mention_count: 1
}]->(emma)
```

### 1.3 Temporal Tracking

**Add to all nodes/relationships:**
```python
{
  'first_mentioned': datetime,
  'last_mentioned': datetime,
  'mention_count': int,
  'confidence': float,  # How certain we are (based on felt-state context)
  'polyvagal_state': str,  # State when mentioned (TSK integration)
  'urgency_level': float  # Crisis vs healing context
}
```

---

## Phase 2: Extend Neo4jKnowledgeGraph Class

### 2.1 Add Entity Methods

**File:** `knowledge_base/neo4j_knowledge_graph.py`

```python
def create_entity(
    self,
    entity_type: str,  # 'Person', 'Place', 'Preference', 'Fact'
    name: str,
    user_id: str,
    properties: Dict = None,
    felt_context: Dict = None  # TSK enrichment
) -> bool:
    """
    Create entity node with felt-state context.

    Args:
        entity_type: Node label (Person, Place, etc.)
        name: Entity name/value
        user_id: Owner user ID
        properties: Additional properties
        felt_context: Transductive context (polyvagal, urgency, nexuses)

    Returns:
        True if successful
    """
    if not self.driver:
        return False

    properties = properties or {}
    felt_context = felt_context or {}

    # Merge felt context
    properties.update({
        'first_mentioned': datetime.now().isoformat(),
        'last_mentioned': datetime.now().isoformat(),
        'mention_count': 1,
        'confidence': felt_context.get('confidence', 0.8),
        'polyvagal_state': felt_context.get('polyvagal_state', 'unknown'),
        'urgency_level': felt_context.get('urgency_level', 0.0)
    })

    query = f"""
    MERGE (e:{entity_type} {{name: $name, user_id: $user_id}})
    ON CREATE SET e += $properties
    ON MATCH SET
        e.last_mentioned = $now,
        e.mention_count = e.mention_count + 1
    RETURN e
    """

    try:
        with self.driver.session(database=self.database) as session:
            session.run(
                query,
                name=name,
                user_id=user_id,
                properties=properties,
                now=datetime.now().isoformat()
            )
        return True
    except Exception as e:
        print(f"Error creating entity {name}: {e}")
        return False

def create_entity_relationship(
    self,
    from_entity: str,
    to_entity: str,
    rel_type: str,  # 'HAS_DAUGHTER', 'LIKES', etc.
    user_id: str,
    properties: Dict = None,
    felt_context: Dict = None
) -> bool:
    """Create relationship between entities with temporal tracking."""
    if not self.driver:
        return False

    properties = properties or {}
    felt_context = felt_context or {}

    properties.update({
        'first_mentioned': datetime.now().isoformat(),
        'last_mentioned': datetime.now().isoformat(),
        'mention_count': 1,
        'confidence': felt_context.get('confidence', 0.8)
    })

    query = f"""
    MATCH (from {{name: $from_name, user_id: $user_id}})
    MATCH (to {{name: $to_name, user_id: $user_id}})
    MERGE (from)-[r:{rel_type}]->(to)
    ON CREATE SET r += $properties
    ON MATCH SET
        r.last_mentioned = $now,
        r.mention_count = r.mention_count + 1
    RETURN r
    """

    try:
        with self.driver.session(database=self.database) as session:
            session.run(
                query,
                from_name=from_entity,
                to_name=to_entity,
                user_id=user_id,
                properties=properties,
                now=datetime.now().isoformat()
            )
        return True
    except Exception as e:
        print(f"Error creating entity relationship: {e}")
        return False

def get_user_entities(
    self,
    user_id: str,
    entity_types: List[str] = None
) -> List[Dict]:
    """
    Get all entities for a user.

    Args:
        user_id: User ID
        entity_types: Filter by types (Person, Place, etc.) or None for all

    Returns:
        List of entity dicts with properties
    """
    if not self.driver:
        return []

    if entity_types:
        labels = '|'.join(entity_types)
        query = f"""
        MATCH (e:{labels} {{user_id: $user_id}})
        RETURN e, labels(e) as types
        ORDER BY e.mention_count DESC, e.last_mentioned DESC
        """
    else:
        query = """
        MATCH (e {user_id: $user_id})
        WHERE e:Person OR e:Place OR e:Preference OR e:Fact
        RETURN e, labels(e) as types
        ORDER BY e.mention_count DESC, e.last_mentioned DESC
        """

    try:
        with self.driver.session(database=self.database) as session:
            result = session.run(query, user_id=user_id)
            entities = []
            for record in result:
                entity = dict(record['e'])
                entity['types'] = record['types']
                entities.append(entity)
            return entities
    except Exception as e:
        print(f"Error getting user entities: {e}")
        return []

def get_entity_relationships(
    self,
    entity_name: str,
    user_id: str,
    max_hops: int = 2
) -> List[Dict]:
    """
    Get all relationships for an entity (multi-hop).

    Example: "Emiliano" → HAS_DAUGHTER → "Emma" → LIKES → "Soccer"

    Returns relationship paths with intermediate entities.
    """
    if not self.driver:
        return []

    query = f"""
    MATCH path = (start {{name: $name, user_id: $user_id}})-[r*1..{max_hops}]-(related)
    WHERE related.user_id = $user_id
    RETURN
        related,
        relationships(path) as rels,
        [n in nodes(path) | n.name] as path_names,
        length(path) as distance
    ORDER BY distance, related.mention_count DESC
    LIMIT 50
    """

    try:
        with self.driver.session(database=self.database) as session:
            result = session.run(query, name=entity_name, user_id=user_id)
            paths = []
            for record in result:
                paths.append({
                    'related_entity': dict(record['related']),
                    'path': record['path_names'],
                    'relationships': [dict(rel) for rel in record['rels']],
                    'distance': record['distance']
                })
            return paths
    except Exception as e:
        print(f"Error getting entity relationships: {e}")
        return []

def build_entity_context_string(
    self,
    user_id: str,
    include_relationships: bool = True,
    max_entities: int = 20
) -> str:
    """
    Build rich entity context string from graph.

    Includes:
    - Primary entities (most mentioned)
    - Key relationships
    - Temporal info (recently mentioned)

    Returns formatted string for LLM prompt.
    """
    if not self.driver:
        return ""

    entities = self.get_user_entities(user_id)
    if not entities:
        return ""

    # Build context
    lines = ["Known information about user:"]

    # Add primary person (usually user themselves)
    persons = [e for e in entities if 'Person' in e.get('types', [])]
    if persons:
        user_person = persons[0]  # Most mentioned person
        lines.append(f"- Name: {user_person['name']}")

        if include_relationships and len(persons) > 1:
            # Get family relationships
            family_rels = self.get_entity_relationships(
                user_person['name'],
                user_id,
                max_hops=1
            )

            daughters = [r for r in family_rels if any('HAS_DAUGHTER' in str(rel) for rel in r['relationships'])]
            if daughters:
                daughter_names = [r['related_entity']['name'] for r in daughters]
                lines.append(f"- Daughters: {', '.join(daughter_names)}")

            sons = [r for r in family_rels if any('HAS_SON' in str(rel) for rel in r['relationships'])]
            if sons:
                son_names = [r['related_entity']['name'] for r in sons]
                lines.append(f"- Sons: {', '.join(son_names)}")

            friends = [r for r in family_rels if any('HAS_FRIEND' in str(rel) for rel in r['relationships'])]
            if friends:
                friend_names = [r['related_entity']['name'] for r in friends[:3]]  # Top 3
                lines.append(f"- Friends: {', '.join(friend_names)}")

    # Add preferences
    prefs = [e for e in entities if 'Preference' in e.get('types', [])]
    if prefs:
        likes = [p['name'] for p in prefs[:5]]  # Top 5
        lines.append(f"- Interests: {', '.join(likes)}")

    # Add places
    places = [e for e in entities if 'Place' in e.get('types', [])]
    if places:
        locations = [p['name'] for p in places[:3]]
        lines.append(f"- Places: {', '.join(locations)}")

    return '\n'.join(lines)
```

---

## Phase 3: Wire into dae_interactive.py

### 3.1 Initialize Neo4j Connection

**File:** `dae_interactive.py` `__init__` method

```python
from knowledge_base.neo4j_knowledge_graph import Neo4jKnowledgeGraph

# Add Neo4j connection (with graceful fallback)
self.knowledge_graph = None
try:
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
    neo4j_database = os.getenv('NEO4J_DATABASE', 'neo4j')

    self.knowledge_graph = Neo4jKnowledgeGraph(
        uri=neo4j_uri,
        user=neo4j_user,
        password=neo4j_password,
        database=neo4j_database
    )
    print("✅ Neo4j entity memory enabled")
except Exception as e:
    print(f"⚠️  Neo4j unavailable, using JSON-only mode: {e}")
    self.knowledge_graph = None
```

### 3.2 Store Entities in Both JSON and Neo4j

**File:** `dae_interactive.py` in entity storage section (lines ~390-410)

```python
# Store enriched entities in user profile
from persona_layer.superject_structures import EnhancedUserProfile

# JSON storage (always)
if 'user_profile' in self.user_state:
    profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])
else:
    profile = EnhancedUserProfile(user_id=self.user['user_id'])

profile.store_entities(enriched_entities)
self.user_state['user_profile'] = profile.to_dict()
self.user_registry.save_user_state(self.user['user_id'], self.user_state)

# Neo4j storage (if available)
if self.knowledge_graph:
    try:
        # Extract felt context for TSK enrichment
        felt_context = {
            'polyvagal_state': felt_state.get('polyvagal_state', 'unknown'),
            'urgency_level': felt_state.get('salience_trauma_markers', {}).get('urgency', 0.0),
            'confidence': felt_state.get('satisfaction', 0.8)
        }

        # Store each entity
        for entity_type, entity_value in enriched_entities.items():
            if entity_type == 'user_name':
                # Create person node
                self.knowledge_graph.create_entity(
                    entity_type='Person',
                    name=entity_value,
                    user_id=self.user['user_id'],
                    properties={'is_primary_user': True},
                    felt_context=felt_context
                )

            elif entity_type == 'family_members' and isinstance(entity_value, list):
                # Create family members and relationships
                user_name = enriched_entities.get('user_name', 'User')
                for member in entity_value:
                    # Create person node for family member
                    self.knowledge_graph.create_entity(
                        entity_type='Person',
                        name=member.get('name'),
                        user_id=self.user['user_id'],
                        felt_context=felt_context
                    )

                    # Create relationship
                    rel_type_map = {
                        'daughter': 'HAS_DAUGHTER',
                        'son': 'HAS_SON',
                        'wife': 'MARRIED_TO',
                        'husband': 'MARRIED_TO',
                        'mother': 'HAS_MOTHER',
                        'father': 'HAS_FATHER',
                        'friend': 'HAS_FRIEND'
                    }
                    rel_type = rel_type_map.get(member.get('relationship', '').lower(), 'RELATED_TO')

                    self.knowledge_graph.create_entity_relationship(
                        from_entity=user_name,
                        to_entity=member.get('name'),
                        rel_type=rel_type,
                        user_id=self.user['user_id'],
                        felt_context=felt_context
                    )

            elif entity_type == 'preferences' and isinstance(entity_value, list):
                # Create preference nodes
                user_name = enriched_entities.get('user_name', 'User')
                for pref in entity_value:
                    self.knowledge_graph.create_entity(
                        entity_type='Preference',
                        name=pref,
                        user_id=self.user['user_id'],
                        felt_context=felt_context
                    )
                    self.knowledge_graph.create_entity_relationship(
                        from_entity=user_name,
                        to_entity=pref,
                        rel_type='LIKES',
                        user_id=self.user['user_id'],
                        felt_context=felt_context
                    )

        if self.display_mode in ['detailed', 'debug']:
            print(f"   ✅ Entities stored in Neo4j knowledge graph")

    except Exception as e:
        if self.display_mode == 'debug':
            print(f"   ⚠️  Neo4j storage failed (JSON fallback): {e}")
```

### 3.3 Load Entity Context from Both Sources

**File:** `dae_interactive.py` in `process_input` method (lines ~290-301)

```python
# 🌀 Phase 1.8++: Load entity context on EVERY turn
# 🌀 Phase NEO4J: Enrich with graph relationships
if 'user_profile' in self.user_state:
    from persona_layer.superject_structures import EnhancedUserProfile
    profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])

    # Base context from JSON
    if profile.has_entity_memory():
        context['entity_context_string'] = profile.get_entity_context_string()
        if 'user_name' in profile.entities:
            context['username'] = profile.entities['user_name']
        elif 'username' in self.user:
            context['username'] = self.user['username']

    # Enrich with Neo4j graph context (if available)
    if self.knowledge_graph:
        try:
            graph_context = self.knowledge_graph.build_entity_context_string(
                user_id=self.user['user_id'],
                include_relationships=True,
                max_entities=20
            )
            if graph_context:
                # Merge graph context with JSON context
                if context.get('entity_context_string'):
                    context['entity_context_string'] += '\n\n' + graph_context
                else:
                    context['entity_context_string'] = graph_context

                if self.display_mode in ['detailed', 'debug']:
                    print(f"🔗 Neo4j: Enriched context with {len(graph_context)} chars of graph data")
        except Exception as e:
            if self.display_mode == 'debug':
                print(f"⚠️  Neo4j enrichment failed (using JSON only): {e}")
```

---

## Phase 4: Configuration

### 4.1 Add to config.py

```python
# Neo4j Entity Memory Configuration
NEO4J_ENABLED = os.getenv('NEO4J_ENABLED', 'false').lower() == 'true'
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'neo4j')

# Entity storage strategy
ENTITY_STORAGE_JSON = True  # Always on (fallback)
ENTITY_STORAGE_NEO4J = NEO4J_ENABLED  # Only if enabled
```

### 4.2 Add to .env.example

```bash
# Neo4j Entity Memory (optional - uses JSON fallback if not configured)
NEO4J_ENABLED=false
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=neo4j

# For Neo4j Aura (cloud):
# NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your_aura_password
```

---

## Phase 5: Testing Strategy

### 5.1 Unit Tests

**Test JSON-only mode** (Neo4j disabled):
```python
# Test entity extraction and storage without Neo4j
def test_entity_storage_json_only():
    interactive = DAEInteractive(enable_neo4j=False)
    result = interactive.process_input("My name is Emiliano")

    # Check JSON storage
    assert 'user_profile' in interactive.user_state
    profile = EnhancedUserProfile.from_dict(interactive.user_state['user_profile'])
    assert profile.entities.get('user_name') == 'Emiliano'
```

**Test Neo4j mode** (with graph):
```python
def test_entity_storage_neo4j():
    graph = Neo4jKnowledgeGraph(uri='bolt://localhost:7687')
    interactive = DAEInteractive(knowledge_graph=graph)

    result = interactive.process_input("My name is Emiliano, I have two daughters Emma and Lily")

    # Check Neo4j storage
    entities = graph.get_user_entities(user_id=interactive.user['user_id'])
    assert any(e['name'] == 'Emiliano' for e in entities)
    assert any(e['name'] == 'Emma' for e in entities)

    # Check relationships
    rels = graph.get_entity_relationships('Emiliano', interactive.user['user_id'])
    assert any('HAS_DAUGHTER' in str(r) for r in rels)
```

### 5.2 Integration Tests

**Test entity recall**:
```python
def test_entity_recall_persistence():
    interactive = DAEInteractive()

    # Turn 1: Introduce
    interactive.process_input("My name is Emiliano")

    # Turn 2: Test recall
    result = interactive.process_input("What's my name?")
    assert 'emiliano' in result['emission_text'].lower()

    # Turn 3: Test relationship recall
    interactive.process_input("I have two daughters Emma and Lily")
    result = interactive.process_input("Tell me about my family")
    assert 'emma' in result['emission_text'].lower() or 'lily' in result['emission_text'].lower()
```

### 5.3 Graph Query Tests

**Test multi-hop queries**:
```python
def test_graph_relationship_inference():
    graph = Neo4jKnowledgeGraph()

    # Create: Emiliano -> HAS_DAUGHTER -> Emma -> LIKES -> Soccer
    graph.create_entity('Person', 'Emiliano', user_id='test_user')
    graph.create_entity('Person', 'Emma', user_id='test_user')
    graph.create_entity('Preference', 'Soccer', user_id='test_user')

    graph.create_entity_relationship('Emiliano', 'Emma', 'HAS_DAUGHTER', user_id='test_user')
    graph.create_entity_relationship('Emma', 'Soccer', 'LIKES', user_id='test_user')

    # Query: What does Emiliano's daughter like?
    paths = graph.get_entity_relationships('Emiliano', user_id='test_user', max_hops=2)

    # Should find: Emiliano -> Emma -> Soccer
    soccer_path = [p for p in paths if p['related_entity']['name'] == 'Soccer']
    assert len(soccer_path) > 0
    assert soccer_path[0]['distance'] == 2
```

---

## Phase 6: Migration & Deployment

### 6.1 Gradual Rollout

**Phase 6.1:** JSON-only (current fixes)
- ✅ Always-on entity extraction
- ✅ Auto-create user profile
- ✅ Hebbian fallback entity passing
- **Status:** Implemented, ready to test

**Phase 6.2:** Dual storage (JSON + Neo4j)
- Add Neo4j initialization (optional)
- Store entities in both
- Load from JSON, enrich from Neo4j
- **Status:** Design complete, implementation needed

**Phase 6.3:** Neo4j-primary
- Neo4j as primary source
- JSON as backup/cache
- Full graph queries for context

### 6.2 Backward Compatibility

**Existing users without Neo4j:**
- System continues to work (JSON fallback)
- No breaking changes
- Graceful degradation

**Existing users with Neo4j:**
- Automatic entity migration from JSON → Neo4j
- Graph enriches existing context
- No data loss

---

## Success Metrics

### Functional
- ✅ Entities stored in JSON (100% of cases)
- ✅ Entities stored in Neo4j (when enabled)
- ✅ Entity recall works across sessions
- ✅ Relationships tracked and queryable
- ✅ Multi-hop queries return valid paths

### Performance
- JSON load time: < 10ms
- Neo4j query time: < 100ms
- Combined context build: < 150ms
- No noticeable latency increase

### Quality
- Entity extraction accuracy: > 90%
- Relationship inference accuracy: > 80%
- Temporal tracking: 100%
- TSK enrichment: 100% (when felt-state available)

---

## Summary

**Integration Approach:**
1. Extend Neo4jKnowledgeGraph with entity methods
2. Wire into dae_interactive.py (dual storage)
3. Graceful fallback to JSON-only
4. Gradual rollout with testing

**Key Benefits:**
- **Offline-capable:** JSON fallback
- **Scalable:** Neo4j for multi-user
- **Rich:** Graph relationships and queries
- **TSK-aware:** Felt-state enrichment

**Next Actions:**
1. Implement entity methods in Neo4jKnowledgeGraph
2. Wire dual storage in dae_interactive.py
3. Test with JSON-only mode first
4. Enable Neo4j for testing
5. Validate entity recall and relationships

---

**Status:** DESIGN COMPLETE, READY FOR IMPLEMENTATION
**Priority:** CRITICAL - Core capability restoration
**Estimated Time:** 4-6 hours implementation, 2-3 hours testing
