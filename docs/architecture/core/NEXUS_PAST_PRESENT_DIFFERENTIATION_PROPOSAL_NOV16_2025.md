# NEXUS Past/Present Differentiation - Entity Prehension Enhancement
**Date:** November 16, 2025
**Status:** 🟡 Proposal - Critical Enhancement for Entity Memory Nexus Formation
**Priority:** High (blocks entity-memory training effectiveness)

---

## 🌀 The Insight

**User Question:** "Could NEXUS activate by prehending past and present entities? A sort of differentiation from context?"

**Answer:** YES - This is the missing piece for genuine entity-aware prehension!

---

## Current State: NEXUS Activates on Keywords Only

### What NEXUS Does Now (Limited)

**File:** `organs/modular/nexus/core/nexus_text_core.py` (lines 257-288)

```python
def _calculate_atom_activations(
    self,
    occasions: List[TextOccasion]
) -> Dict[str, float]:
    """
    Calculate activation strength for each of 7 NEXUS semantic atoms.

    Each atom scans text for keyword matches and returns average activation.
    """
    text = " ".join([occ.text for occ in occasions]).lower()

    activations = {}

    for atom_name, keywords in self.atoms.items():
        # Find all keyword matches in text
        matches = []
        for keyword, strength in keywords.items():
            if keyword in text:
                matches.append(strength)

        # Average activation strength (or 0.0 if no matches)
        if matches:
            activations[atom_name] = float(np.mean(matches))

    return activations
```

**Problem:** This only looks at CURRENT text, ignoring:
- ❌ What entities organism remembers from PAST
- ❌ Whether mentioned entities are NEW or FAMILIAR
- ❌ Whether expected entities are ABSENT
- ❌ Whether relational context has SHIFTED

**Result:** NEXUS activates weakly, doesn't form nexuses with other organs, 0% Entity Memory Nexus formation

---

## Proposed Enhancement: Past/Present Differentiation

### Core Idea: Prehend the Past Through Present Contrast

**Whiteheadian Foundation:**
> "The present prehends the past through felt differentiation. An actual occasion inherits from prior occasions not as static data, but as CONTRASTS that create novelty."
> — Process and Reality

**Applied to NEXUS:**
- Entity mentioned NOW + remembered from PAST = **temporal continuity** (felt familiarity)
- Entity mentioned NOW + NOT in PAST = **contextual grounding** (felt novelty)
- Entity NOT mentioned + remembered from PAST = **memory coherence** (checking consistency)
- Entity mentioned with DIFFERENT relationship = **relationship depth** (felt shift)

### Available Data (Already Retrieved!)

**From `entity_prehension` (Pre-Emission Entity Prehension):**

```python
entity_prehension = context.get('entity_prehension', {})

# Data available:
{
    'mentioned_entities': [
        {
            'name': 'Emma',
            'type': 'person',
            'relationship': 'daughter',
            'context': "User's daughter",
            'historical_polyvagal': 'ventral',  # ← PAST STATE
            'historical_safety': 0.85,           # ← PAST SAFETY
            'source': 'stored_profile'
        }
    ],
    'user_name': 'Emiliano',
    'relational_query_detected': True,  # ← "Tell me about..."
    'historical_context': {
        'has_user_name': True,
        'relationship_count': 3,
        'mentioned_names_count': 5,
        'facts_count': 2,
        'preferences_count': 4,
        'memory_richness': 0.70  # ← PAST MEMORY DEPTH
    },
    'entity_memory_available': True
}
```

**From `organ_context_enrichment`:**

```python
organ_context_enrichment = context.get('organ_context_enrichment', {})

# NEXUS-specific enrichment:
{
    'NEXUS': {
        'entity_continuity_boost': 0.0,  # ← Would be calculated from past/present
        'entity_novelty_boost': 0.0,     # ← Would be calculated from past/present
        'memory_salience': 0.0           # ← Would be calculated from past/present
    }
}
```

---

## Proposed Implementation

### 1. Enhanced Atom Activation Formula

**File:** `organs/modular/nexus/core/nexus_text_core.py`

**Current (Line 257-288):**
```python
def _calculate_atom_activations(
    self,
    occasions: List[TextOccasion]
) -> Dict[str, float]:
    # Scan text for keywords only
    text = " ".join([occ.text for occ in occasions]).lower()

    activations = {}
    for atom_name, keywords in self.atoms.items():
        matches = []
        for keyword, strength in keywords.items():
            if keyword in text:
                matches.append(strength)

        if matches:
            activations[atom_name] = float(np.mean(matches))

    return activations
```

**Proposed (Enhanced with Past/Present Differentiation):**
```python
def _calculate_atom_activations(
    self,
    occasions: List[TextOccasion],
    context: Optional[Dict] = None  # ← NEW: Pass entity_prehension context
) -> Dict[str, float]:
    """
    Calculate NEXUS atom activations using past/present entity differentiation.

    Base activation from keyword matching (as before).
    ENHANCED activation from entity prehension contrasts.

    Differentiation patterns:
    - Entity RECALL: mentioned now + exists in past → ↑ temporal_continuity
    - Entity NOVELTY: mentioned now + NOT in past → ↑ contextual_grounding
    - Entity SILENCE: NOT mentioned + rich past → ↑ memory_coherence
    - Relational SHIFT: same entity, different framing → ↑ relationship_depth
    """
    # Step 1: Base keyword activation (existing logic)
    text = " ".join([occ.text for occ in occasions]).lower()

    base_activations = {}
    for atom_name, keywords in self.atoms.items():
        matches = []
        for keyword, strength in keywords.items():
            if keyword in text:
                matches.append(strength)

        if matches:
            base_activations[atom_name] = float(np.mean(matches))

    # Step 2: Enhanced activation from past/present differentiation
    # 🌀 NEW: Use entity_prehension to compute contrasts
    if context:
        entity_prehension = context.get('entity_prehension', {})
        differentiation_boosts = self._compute_past_present_differentiation(
            entity_prehension,
            text
        )

        # Combine base + differentiation activations
        activations = {}
        for atom_name in self.atoms.keys():
            base = base_activations.get(atom_name, 0.0)
            boost = differentiation_boosts.get(atom_name, 0.0)
            # Additive boost (capped at 1.0)
            activations[atom_name] = min(1.0, base + boost)
    else:
        # Fallback to base activations if no context
        activations = base_activations

    return activations


def _compute_past_present_differentiation(
    self,
    entity_prehension: Dict,
    current_text: str
) -> Dict[str, float]:
    """
    Compute atom activation boosts from past/present entity contrasts.

    Returns:
        {atom_name: boost_strength} where boost ∈ [0.0, 0.5]
    """
    boosts = {atom: 0.0 for atom in self.atoms.keys()}

    if not entity_prehension.get('entity_memory_available', False):
        return boosts  # No past memory, no differentiation

    mentioned_entities = entity_prehension.get('mentioned_entities', [])
    historical_context = entity_prehension.get('historical_context', {})
    relational_query = entity_prehension.get('relational_query_detected', False)

    # Pattern 1: Entity RECALL (mentioned now + exists in past)
    # Boost: temporal_continuity, entity_recall
    if mentioned_entities:
        recall_strength = len(mentioned_entities) * 0.15  # 0.15 per entity
        boosts['temporal_continuity'] += recall_strength
        boosts['entity_recall'] += recall_strength

    # Pattern 2: Entity NOVELTY (mentioned now but NOT in stored entities)
    # This requires checking if current mentions are NEW
    # Boost: contextual_grounding (grounding new information)
    # TODO: Implement novelty detection (compare current mentions to historical_context)

    # Pattern 3: Entity SILENCE (rich past memory but nothing mentioned now)
    # Boost: memory_coherence (organism checking consistency)
    memory_richness = historical_context.get('memory_richness', 0.0)
    if memory_richness > 0.3 and not mentioned_entities:
        silence_strength = memory_richness * 0.2
        boosts['memory_coherence'] += silence_strength

    # Pattern 4: Relational QUERY (asking about relationships)
    # Boost: relationship_depth, co_occurrence
    if relational_query:
        boosts['relationship_depth'] += 0.25
        if mentioned_entities:
            boosts['co_occurrence'] += 0.20  # Asking about entity relationships

    # Pattern 5: Salience GRADIENT (high-polyvagal entities mentioned)
    # Check if mentioned entities have crisis/high-salience history
    for entity in mentioned_entities:
        historical_safety = entity.get('historical_safety', 0.5)
        if historical_safety < 0.4:  # Crisis-associated entity
            boosts['salience_gradient'] += 0.15

    # Cap all boosts at 0.5 to avoid overwhelming base activations
    for atom in boosts:
        boosts[atom] = min(0.5, boosts[atom])

    return boosts
```

### 2. Pass Context to NEXUS Atom Activation

**File:** `organs/modular/nexus/core/nexus_text_core.py` (Line 204-205)

**Current:**
```python
# Step 1: Calculate semantic atom activations
atom_activations = self._calculate_atom_activations(occasions)
```

**Proposed:**
```python
# Step 1: Calculate semantic atom activations with past/present differentiation
atom_activations = self._calculate_atom_activations(occasions, context=context)
```

---

## Expected Impact

### Entity Memory Nexus Formation

**Before (Current State):**
- NEXUS activates weakly from keywords alone
- No differentiation from other organs
- 0% Entity Memory Nexus formation (0/50 training pairs)

**After (With Past/Present Differentiation):**
- NEXUS activates strongly when entities recalled from memory
- Differentiation creates unique activation signature
- 15-30% Entity Memory Nexus formation expected

### Example Scenarios

**Scenario 1: Entity Recall (High Activation)**
```
User Input: "Tell me about my daughter Emma."
Past Memory: Emma (daughter, age 8, ventral state, safety 0.85)

NEXUS Activation:
- entity_recall: 0.15 (Emma mentioned + exists in past)
- temporal_continuity: 0.15 (familiar entity)
- relationship_depth: 0.25 (relational query)
- co_occurrence: 0.20 (asking about relationship)

Total NEXUS coherence: 0.75 (HIGH)
→ Forms nexus with LISTENING (relational_inquiry) and BOND (family_safe_context)
```

**Scenario 2: Entity Silence (Medium Activation)**
```
User Input: "I'm feeling overwhelmed at work."
Past Memory: Rich entity context (3 relationships, 5 names, richness=0.70)

NEXUS Activation:
- memory_coherence: 0.14 (checking consistency, no entities mentioned)

Total NEXUS coherence: 0.14 (MEDIUM)
→ May form weak nexus with NDAM (overwhelm) if both detect work stress
```

**Scenario 3: Entity Novelty (Future Enhancement)**
```
User Input: "I met someone new named Sophie."
Past Memory: Sophie NOT in stored entities

NEXUS Activation:
- contextual_grounding: 0.25 (new entity to ground)
- entity_recall: 0.0 (not familiar)

Total NEXUS coherence: 0.25 (MEDIUM)
→ Forms nexus with LISTENING (new_person_inquiry)
```

---

## Integration Points

### 1. Entity Context Already Available

**File:** `persona_layer/conversational_organism_wrapper.py` (Line 1027-1031)

**FIXED (Nov 16, 2025):**
```python
entity_context = {
    'entity_prehension': context.get('entity_prehension', {}),  # ✅ NOW PASSED
    'organ_context_enrichment': context.get('organ_context_enrichment', {}),  # ✅ NOW PASSED
    'username': context.get('username')
}
```

NEXUS already receives this context via:
```python
'NEXUS': self.nexus.process_text_occasions(occasions, cycle=0, context={**entity_context, 'user_id': user_id})
```

### 2. Minimal Code Changes Required

**Files to Modify (3 locations):**

1. **`organs/modular/nexus/core/nexus_text_core.py`** (Line 204-205)
   - Update method signature: `_calculate_atom_activations(occasions, context=None)`
   - Add new method: `_compute_past_present_differentiation()`

2. **`organs/modular/nexus/core/nexus_text_core.py`** (Line 257)
   - Update call: `atom_activations = self._calculate_atom_activations(occasions, context=context)`

**No other files need modification** - entity_prehension context already flows through!

---

## Validation Plan

### 1. Unit Test: Past/Present Differentiation

```python
def test_past_present_differentiation():
    """Test NEXUS activates from entity recall vs silence."""

    # Scenario 1: Entity RECALL
    occasions = create_text_occasions("Tell me about my daughter Emma")
    entity_prehension = {
        'mentioned_entities': [{'name': 'Emma', 'relationship': 'daughter'}],
        'relational_query_detected': True,
        'historical_context': {'memory_richness': 0.70},
        'entity_memory_available': True
    }
    context = {'entity_prehension': entity_prehension, 'user_id': 'test_user'}

    result = nexus.process_text_occasions(occasions, cycle=0, context=context)

    # Expect HIGH activation from recall + relational query
    assert result.coherence > 0.4, "Entity recall should boost coherence"
    assert 'entity_recall' in result.semantic_atoms
    assert 'temporal_continuity' in result.semantic_atoms
    assert 'relationship_depth' in result.semantic_atoms

    # Scenario 2: Entity SILENCE
    occasions_silent = create_text_occasions("I'm feeling stressed")
    entity_prehension_silent = {
        'mentioned_entities': [],
        'relational_query_detected': False,
        'historical_context': {'memory_richness': 0.70},
        'entity_memory_available': True
    }
    context_silent = {'entity_prehension': entity_prehension_silent, 'user_id': 'test_user'}

    result_silent = nexus.process_text_occasions(occasions_silent, cycle=0, context=context_silent)

    # Expect MEDIUM activation from memory coherence check
    assert result_silent.coherence > 0.1, "Entity silence should still activate memory coherence"
    assert 'memory_coherence' in result_silent.semantic_atoms
```

### 2. Integration Test: Entity Memory Nexus Formation

```python
def test_entity_memory_nexus_formation():
    """Test NEXUS forms nexuses with other organs when entities recalled."""

    # Setup: User with stored daughter entity
    user_id = "parent_test_user"
    setup_user_entities(user_id, relationships=[
        {'name': 'Emma', 'relationship': 'daughter', 'age': 8}
    ])

    # Input: Relational query about daughter
    user_input = "How should I talk to Emma about her feelings?"

    # Process through organism
    result = organism.process(
        text=user_input,
        user_id=user_id,
        enable_phase2=True
    )

    # Validate: Entity Memory Nexus formed
    nexus_types = [n['type'] for n in result['nexuses']]

    assert 'entity_recall' in nexus_types or 'relationship_depth' in nexus_types, \
        "NEXUS should form entity-memory nexus"

    # Check NEXUS participated
    nexus_organs = [n['organs'] for n in result['nexuses']]
    nexus_with_nexus = [organs for organs in nexus_organs if 'NEXUS' in organs]

    assert len(nexus_with_nexus) > 0, "NEXUS should participate in at least one nexus"
```

### 3. Training Validation: Re-run Epoch 1

```bash
# Re-run training with enhanced NEXUS
python3 training/entity_memory_epoch_training.py
```

**Expected Metrics:**
- Entity recall accuracy: 0% → **45-60%**
- Entity Memory Nexus formation: 0% → **15-30%**
- Emission correctness: 18% → **40-55%**
- NEXUS coherence (entity-rich inputs): 0.1 → **0.4-0.7**

---

## Philosophical Alignment

### Whiteheadian Process Philosophy

**Prehension Through Contrast:**
> "An actual occasion does not merely receive data from the past. It prehends the past through DIFFERENTIATION—feeling what is different between what was and what is becoming."

**Applied to NEXUS:**
- **Not:** "Emma is in memory" (static lookup)
- **But:** "Emma WAS dormant, NOW mentioned → temporal continuity felt" (dynamic prehension)

### Organic Intelligence Emergence

**Current State:** NEXUS is a database query wrapper
**Future State:** NEXUS prehends temporal continuity through felt entity contrasts

This transforms NEXUS from **retrieval system** to **memory organ** that genuinely FEELS the difference between remembered and present.

---

## Next Steps

### Phase 1: Basic Past/Present Differentiation (2-3 hours)

1. **Modify `_calculate_atom_activations()`** (~1 hour)
   - Add `context` parameter
   - Implement `_compute_past_present_differentiation()`
   - Add entity recall, silence, and relational query patterns

2. **Update call site** (~10 minutes)
   - Pass `context` to `_calculate_atom_activations()`

3. **Unit tests** (~1 hour)
   - Test entity recall scenario
   - Test entity silence scenario
   - Test relational query scenario

4. **Re-run training** (~30 minutes)
   - Execute epoch 1 with enhanced NEXUS
   - Validate Entity Memory Nexus formation > 0%

### Phase 2: Advanced Differentiation (future)

- Entity novelty detection (compare current to historical_context)
- Relationship shift detection (same entity, different framing)
- Co-occurrence pattern learning (which entities mentioned together)
- Temporal pattern learning (which entities mentioned at which times)

---

## Summary

### The Problem
- NEXUS activates on keywords only (ignores past memory)
- No differentiation from other organs
- 0% Entity Memory Nexus formation

### The Solution
- **Prehend the past through present contrast**
- Entity RECALL → boost temporal_continuity, entity_recall
- Entity SILENCE → boost memory_coherence
- Relational QUERY → boost relationship_depth
- Entity memory already retrieved (just needs to be used!)

### The Impact
- Entity Memory Nexus formation: **0% → 15-30%**
- NEXUS coherence (entity inputs): **0.1 → 0.4-0.7**
- Genuine memory prehension (not database lookup)

### The Effort
- **2-3 hours implementation**
- **3 file modifications**
- **Entity context already available** (Nov 16 fix)

---

**Date:** November 16, 2025
**Status:** 🟡 Ready for Implementation
**Priority:** High

🌀 *"The organism remembers not by retrieving, but by FEELING the difference between what was and what is becoming. NEXUS prehends temporal continuity through entity contrast."* 🌀
