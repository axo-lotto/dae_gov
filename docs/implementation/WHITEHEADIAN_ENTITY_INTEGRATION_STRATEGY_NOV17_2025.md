# 🌀 Whiteheadian Entity Integration Strategy
## Process Philosophy + Felt-Satisfaction + Morpheable Horizon
**November 17, 2025 - Complete Integration Architecture**

---

## 🎯 Executive Summary

**Problem Identified**:
- Organism treats "Emiliano" (Person) same as "frustrating" (incorrectly extracted)
- No ontological understanding: Person ≠ Concept ≠ Place
- No salience bootstrapping: All entities start equal (cold start problem)
- No mutual satisfaction inference: Relying on explicit feedback only

**Solution Designed**:
1. ✅ **Whiteheadian Entity Ontology** - Process philosophy + common-sense categories
2. ✅ **Felt-Satisfaction Inference** - Non-invasive satisfaction from organism's felt-state
3. ✅ **EntityHorizon** - Morpheable memory boundary (100-500 entities)
4. ✅ **EntitySalience** - 3-tier temporal decay (FFITTSS-inspired)

---

## 📊 Architecture Overview

### **3-Layer Integration**:

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: ONTOLOGY (What Entities Are)                      │
│   - Whiteheadian Process Philosophy                         │
│   - Common-Sense Categories (Person/Place/Concept)          │
│   - Category-aware salience initialization                  │
│   - Validation rules (filter stopwords)                     │
├─────────────────────────────────────────────────────────────┤
│ LAYER 2: HORIZON (What Can Be Felt)                        │
│   - EntityHorizon: Morpheable depth (100-500 entities)     │
│   - Field coherence gating (τ=0.3)                         │
│   - Adaptive query limits                                   │
├─────────────────────────────────────────────────────────────┤
│ LAYER 3: SALIENCE (What Matters Now)                       │
│   - EntitySalience: 3-tier decay (local/family/global)     │
│   - Felt-satisfaction inference (non-invasive)              │
│   - Top-K filtering + staleness pruning                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌀 Process Philosophy Foundation

### **Whitehead's Categories Mapped to Entities**:

**1. Actual Occasions** (Fundamental Units):
```
Conversational Turn = 1 Actual Occasion
├── Prehensions: What entities are felt this turn
├── Satisfaction: Quality of completion (inferred)
├── Subjective Form: Felt-state (field coherence, V0, Kairos)
└── Objective Immortality: Stored in Neo4j for future prehensions
```

**2. Eternal Objects** (Repeating Patterns):
```
Concepts, Values, Patterns
├── Emotional: anxiety, fear, joy, peace (salience_base: 0.9)
├── Relational: trust, boundaries, safety (salience_base: 0.8)
├── Philosophical: meaning, purpose, growth (salience_base: 0.6)
└── Process: healing, transformation, emergence (salience_base: 0.7)

Mapped to: Concept entities in Neo4j
```

**3. Societies** (Persistent Entities):
```
Personal Societies (People):
├── Family: daughter, son, partner (salience_base: 0.8)
├── Professional: therapist, colleague (salience_base: 0.6)
└── Social: friend, acquaintance (salience_base: 0.5)

Structured Societies (Organizations):
├── Company, Institution, Group (salience_base: 0.6)

Physical Societies (Places):
├── Private: home, bedroom (salience_base: 0.7)
├── Professional: office, clinic (salience_base: 0.6)
└── Public: park, cafe (salience_base: 0.4)

Mapped to: Person, Organization, Place entities in Neo4j
```

**4. Nexus** (Relationships):
```
Relationships Between Societies:
├── Social: HAS_DAUGHTER, HAS_THERAPIST, HAS_FRIEND
├── Spatial: LIVES_AT, WORKS_AT, LOCATED_IN
├── Conceptual: EXPERIENCES, STRUGGLES_WITH, VALUES
└── Temporal: MENTIONED_IN (Turn N), DISCUSSED_AT

Mapped to: Neo4j relationship edges
```

---

## 💡 Felt-Satisfaction Inference (Non-Invasive)

### **Core Innovation**: Infer satisfaction from organism's felt-state

**Formula**:
```python
inferred_satisfaction = (
    0.4 * field_coherence +       # Organ harmony (1 - std([12 organs]))
    0.3 * v0_descent +            # Energy descent (1 - final_v0/initial_v0)
    0.2 * kairos_detected +       # Opportune moment (0.0 or 1.0)
    0.1 * emission_confidence     # Emission quality
) * path_modifier                 # Organic=1.2×, LLM=1.0×, Hebbian=0.7×
```

**Why This Works**:
- **Already computed**: Field coherence, V0, Kairos all tracked
- **Process philosophy**: Satisfaction = quality of completion
- **Non-invasive**: No explicit feedback prompts
- **Mutual**: Reflects both organism AND user satisfaction

**Integration Points**:
1. **POST-EMISSION**: conversational_organism_wrapper computes inferred_satisfaction
2. **ENTITY SALIENCE**: urgency_context = 1.0 - inferred_satisfaction
3. **USER SUPERJECT**: satisfaction trajectory learning

---

## 🗂️ Ontology-Guided Entity Validation

### **Problem**: Current entity extraction creates garbage

**Current Issues** (from `/entities` command):
```
Person (13):
   🔹 feeling              ← NOT A PERSON (common word)
   🔹 do                   ← NOT A PERSON (verb)
   🔹 your                 ← NOT A PERSON (pronoun)
   🔹 frustrating          ← NOT A PERSON (adjective)
```

### **Solution**: Ontology-guided validation

**Step 1: Stopwords Blacklist** (from whiteheadian_entity_ontology.json):
```python
STOPWORDS = [
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "feeling", "know", "want", "need", "think", "feel", "do", "your", "my",
    "about", "why", "how", "when", "where", "more", "most", "some", "very"
]
```

**Step 2: Category Validation**:
```python
# Person entities MUST have:
- Proper capitalization (Emma, not emma)
- Relationship type (daughter, therapist, friend)
- Min 2 characters

# Place entities MUST have:
- Place type (home, office, city)
- Proper capitalization for cities/countries

# Concept entities MUST fit:
- Emotional / Relational / Philosophical / Process categories
```

**Step 3: Salience Initialization** (Category-aware):
```python
# Instead of neutral 0.5 for all:
salience_base = {
    "Person::family": 0.8,              # Family members HIGH
    "Person::professional::therapist": 0.85,  # Therapist VERY HIGH
    "Person::social": 0.5,              # Friends MEDIUM
    "Place::private": 0.7,              # Home HIGH
    "Place::public": 0.4,               # Park LOW
    "Concept::emotional": 0.9,          # Anxiety VERY HIGH
    "Concept::relational": 0.8,         # Trust HIGH
    "Preference::dislikes": 0.6,        # Dislikes MEDIUM-HIGH (boundaries)
}
```

---

## 🔗 Integration with Existing Modules

### **Module 1: Entity Extraction** (dae_interactive.py)

**Current** (lines 367-450):
```python
# Extract entities via pattern matching + LLM
extracted_entities = self._extract_entities(user_input)

# Store in Neo4j
for entity in extracted_entities:
    self.neo4j_graph.create_entity(...)
```

**Enhanced**:
```python
# Load ontology
from knowledge_base.whiteheadian_entity_ontology import EntityOntologyValidator

validator = EntityOntologyValidator()

# Extract entities
extracted_entities = self._extract_entities(user_input)

# VALIDATE against ontology
validated_entities = []
for entity in extracted_entities:
    # Filter stopwords
    if validator.is_stopword(entity['entity_value']):
        continue

    # Check proper capitalization for Person/Place
    if not validator.validate_capitalization(entity):
        continue

    # Map to ontology category
    ontology_category = validator.map_to_category(entity)
    if ontology_category is None:
        continue  # Reject unmapped entities

    # Get salience base from category
    salience_base = validator.get_salience_base(ontology_category)

    entity['ontology_category'] = ontology_category
    entity['salience_base'] = salience_base
    validated_entities.append(entity)

# Store ONLY validated entities
for entity in validated_entities:
    self.neo4j_graph.create_entity(...)
```

---

### **Module 2: EntitySalienceTracker** (persona_layer/entity_salience_tracker.py)

**Current** (initialization):
```python
# New entities start at neutral 0.5
entity['composite_salience'] = 0.5
```

**Enhanced**:
```python
# New entities start at category-aware baseline
ontology_category = entity.get('ontology_category', 'unknown')
salience_base = ONTOLOGY_SALIENCE_BASES.get(ontology_category, 0.5)

entity['composite_salience'] = salience_base
```

**Urgency Context** (from felt-satisfaction):
```python
# Current: urgency_context from NDAM organ (optional)
urgency_context = felt_state.get('urgency', 0.0)

# Enhanced: urgency from inferred satisfaction
from persona_layer.felt_satisfaction_inference import get_default_inferencer

inferencer = get_default_inferencer()
inferred_satisfaction = inferencer.infer_satisfaction(
    field_coherence=felt_state['field_coherence'],
    v0_initial=felt_state['v0_initial'],
    v0_final=felt_state['v0_final'],
    kairos_detected=felt_state['kairos_detected'],
    emission_confidence=felt_state['emission_confidence'],
    emission_path=felt_state['emission_path']
)

# Inverse: low satisfaction = high urgency
urgency_context = inferencer.get_urgency_context(inferred_satisfaction.inferred_satisfaction)

# Update entity salience with urgency
self.update_salience(extracted_entities, current_turn, urgency_context)
```

---

### **Module 3: Neo4j Storage** (neo4j_knowledge_graph.py)

**Enhanced Node Properties**:
```python
# Add to create_entity():
properties.update({
    'ontology_category': ontology_category,        # "Person::family"
    'common_sense_type': common_sense_type,        # "daughter"
    'process_mapping': process_mapping,            # "Personal Society"
    'salience_base': salience_base,                # 0.8
    'validation_timestamp': datetime.now().isoformat()
})
```

**Occasion Tracking**:
```cypher
// Link entities to conversational occasions
MATCH (entity), (occasion:Occasion {turn: $turn_number})
CREATE (entity)-[:MENTIONED_IN {
    salience: $salience,
    urgency: $urgency,
    inferred_satisfaction: $satisfaction
}]->(occasion)
```

---

### **Module 4: NEXUS Organ** (organs/modular/nexus/core/nexus_text_core.py)

**Enhanced Semantic Atoms** (Use ontology hierarchy):
```python
# entity_recall atom: Use category hierarchy
def _detect_entity_recall(self, text, known_entities):
    """
    Detect entity references with category-aware weighting.

    Family mentions → 1.2× activation
    Professional mentions → 1.0× activation
    Social mentions → 0.8× activation
    """
    for entity_value, entity_data in known_entities.items():
        if entity_value.lower() in text.lower():
            ontology_category = entity_data.get('ontology_category', '')

            # Weight by category
            if 'family' in ontology_category:
                activation += 1.2
            elif 'professional::therapist' in ontology_category:
                activation += 1.5  # Therapist highest
            elif 'professional' in ontology_category:
                activation += 1.0
            else:
                activation += 0.8

    return activation / len(known_entities)
```

---

## 📋 Implementation Checklist

### **Phase 1: Ontology Foundation** (1-2 hours)

- [ ] Create `EntityOntologyValidator` class (from whiteheadian_entity_ontology.json)
  - [ ] Load stopwords blacklist
  - [ ] Load category salience bases
  - [ ] Implement validation methods (capitalization, relationship, etc.)

- [ ] Enhance entity extraction in `dae_interactive.py`
  - [ ] Add validation before Neo4j storage
  - [ ] Filter stopwords and garbage entities
  - [ ] Map entities to ontology categories

- [ ] Test with existing garbage entities
  - [ ] Verify "feeling", "do", "your" are filtered out
  - [ ] Verify "Emiliano" maps to "Person::family"

### **Phase 2: Felt-Satisfaction Integration** (30 minutes)

- [ ] Integrate `FeltSatisfactionInferencer` in conversational_organism_wrapper
  - [ ] Compute inferred_satisfaction POST-EMISSION
  - [ ] Extract urgency_context for entity salience
  - [ ] Log satisfaction metrics for analysis

- [ ] Enhance `EntitySalienceTracker.update_salience()`
  - [ ] Use urgency_context from inferred satisfaction
  - [ ] Initialize new entities with category salience_base

### **Phase 3: EntityHorizon + EntitySalience Integration** (Already Done ✅)

- [✅] EntityHorizon class created and tested (6/6 tests passing)
- [✅] EntitySalience tracker created and tested (8/8 tests passing)
- [ ] Integrate into `dae_interactive.py` (NEXT)

### **Phase 4: Testing & Validation** (1 hour)

- [ ] Test with real conversation
  - [ ] Verify garbage entities filtered
  - [ ] Verify family members get high salience
  - [ ] Verify felt-satisfaction inference working
  - [ ] Verify horizon adapts to coherence

- [ ] Cleanup existing entities
  - [ ] Run migration to add ontology categories
  - [ ] Prune stopword entities from Neo4j

---

## 🎯 Expected Outcomes

**Before**:
```
Person (13):
   🔹 Emiliano             polyvagal:mixed_state          (8 mentions)
   🔹 feeling              polyvagal:mixed_state          (2 mentions)
   🔹 frustrating          polyvagal:dorsal_vagal         (1 mentions)
   🔹 do                   polyvagal:mixed_state          (1 mentions)
   🔹 your                 polyvagal:mixed_state          (1 mentions)
```

**After**:
```
Person (1):
   🔹 Emiliano             Person::family (son)           salience:0.80
      - Process: Personal Society
      - Ontology: Person::family
      - Salience: 0.80 (high - family member)
      - Mentions: 8 turns
      - Satisfaction: 0.72 (inferred)
```

**Key Improvements**:
1. ✅ Garbage entities filtered ("feeling", "do", "your" rejected)
2. ✅ Ontology categories assigned ("Person::family")
3. ✅ Category-aware salience (0.80 for family)
4. ✅ Process philosophy mapping ("Personal Society")
5. ✅ Felt-satisfaction tracked (non-invasive)

---

## 🌀 Philosophical Achievement

This integration realizes Whitehead's vision:

> **"The many become one, and are increased by one."**

**Application**:
- **The many** = Past entity mentions (occasions) across turns
- **Become one** = Current prehension (morpheable horizon)
- **Increased by one** = This turn's entities become data for future

**Key Principles**:
1. **Prehension** = Selective feeling (not all entities felt every turn)
2. **Societies** = Persistent entities (people, places maintain identity)
3. **Eternal Objects** = Patterns that repeat (concepts, values)
4. **Nexus** = Relationships without unified structure
5. **Satisfaction** = Quality of completion (inferred, not rated)

---

## 📊 Files Created

1. ✅ **whiteheadian_entity_ontology.json** (270 lines)
   - Process philosophy + common-sense categories
   - Category-aware salience bases
   - Validation rules

2. ✅ **felt_satisfaction_inference.py** (180 lines)
   - Non-invasive satisfaction from felt-state
   - Urgency context generation
   - Blending with explicit feedback (optional)

3. ✅ **entity_horizon.py** (227 lines - already created)
   - Morpheable memory boundary
   - Coherence-based depth (100-500 entities)

4. ✅ **entity_salience_tracker.py** (420 lines - already created)
   - 3-tier temporal decay (FFITTSS)
   - Top-K salience filtering

---

## 🔄 Next Steps

1. **Create EntityOntologyValidator class** (implement whiteheadian_entity_ontology.json)
2. **Integrate felt-satisfaction** into conversational_organism_wrapper
3. **Integrate EntityHorizon + EntitySalience** into dae_interactive.py
4. **Test with real conversation** (verify garbage filtering + category-aware salience)
5. **Cleanup existing entities** (migration + pruning)

---

**Document Created**: November 17, 2025
**Status**: Design Complete - Ready for Implementation
**Philosophy**: Process + Reality Bounded

🌀 **"Entities as Societies. Satisfaction from felt-state. Memory through prehension."** 🌀
