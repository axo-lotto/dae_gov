# 🧬 Entity-Organism Integration Roadmap - November 14, 2025

**Status:** 🔧 IN PROGRESS - Architectural Bottleneck Identified & Fix Initiated
**Priority:** 🔴 CRITICAL - Blocks name memorization despite memory persistence fixes
**Approach:** Leverage existing organism scaffolding (11 organs, TSK, meta-atoms)

---

## 🎯 Problem Statement

**User Report:** "Name memorization still not working and we are over-engineering pattern matching when DAE has extensive scaffolding (11-organ organism with prehension)"

**Root Cause:** Entity extraction happens **in isolation** from organism processing:
- Entities extracted PRE-organism but **never reach organs** during prehension
- Organs process raw text without entity context ("alice" is unknown, not stored family member)
- Entity enrichment happens POST-organism (too late for atom activations)

**Symptoms:**
```python
User: "my daughter's name is Alice"
DAE: (stores entity_name="Alice", relation="daughter")

[Later]
User: "remember Alice?"
Organisms: Process "Alice" as generic word (NO stored entity awareness)
DAE: "I'm not sure. Can you remind me?"  # ❌ BROKEN
```

---

## 🔍 Architectural Assessment (Agent-Driven)

### Current Flow (BROKEN)

```
dae_interactive.py:process_input() [Line 299-555]
├─ Line 315-343: Load entity_context_string from user_profile ✅
│  └─ Stored entities available in context dict
│
├─ Line 345-376: Entity Extraction (PRE-organism) ✅
│  ├─ MemoryIntentDetector.detect()
│  └─ EntityExtractor.extract() → {user_name, family_members, ...}
│
├─ Line 378-385: organism.process_text() ❌ ISOLATION POINT
│  ├─ Creates TextOccasions from RAW TEXT (no entity data)
│  ├─ Organs receive occasions ONLY (no context parameter)
│  └─ Returns organ_results (based on keyword matching, not entity awareness)
│
├─ Line 387-484: TSK Entity Enrichment (POST-organism) ⚠️ TOO LATE
│  └─ Enriches with polyvagal, urgency, nexuses
│
└─ Line 438-456: Store in user_profile ✅
```

**The Bottleneck:**
```python
# persona_layer/conversational_organism_wrapper.py:689-725
occasions = self._create_text_occasions(text)  # ← NO entity context

organ_results = {
    'LISTENING': self.listening.process_text_occasions(occasions, cycle=0),
    'EMPATHY': self.empathy.process_text_occasions(occasions, cycle=0),
    # ❌ NO context parameter (except CARD which gets organ-derived context)
}
```

---

## 🧩 Identified Bottlenecks

### 1. **CRITICAL: Organs Don't See Entity Context**
**File:** `persona_layer/conversational_organism_wrapper.py:689-725`
**Problem:** TextOccasions created from raw text with NO entity fields
**Impact:** Organs do keyword matching on "alice" without knowing it's a stored family member

### 2. **Organism Wrapper Doesn't Pass Context to Organs**
**File:** `persona_layer/conversational_organism_wrapper.py:554-675`
**Problem:** `context` dict (with stored_entities, username) available but NEVER passed to organs
**Evidence:** Only CARD organ accepts `context` parameter (for polyvagal gating)

### 3. **TextOccasion Had No Entity Fields** ✅ FIXED
**File:** `transductive/text_occasion.py:96-103` (ADDED Nov 14, 2025)
**Solution:** Added 3 entity-aware fields:
```python
known_entities: Dict[str, Any] = field(default_factory=dict)
entity_references: List[str] = field(default_factory=list)
entity_match_confidence: Dict[str, float] = field(default_factory=dict)
```

### 4. **Entity Context Only Reaches Emission Generator**
**File:** `persona_layer/organ_reconstruction_pipeline.py:485-498`
**Problem:** Entity context passed to LLM-based emission but NOT to organ prehension
**Flow Issue:**
```
Organs (no entity context) → Atom Activations → Emission (has entity context but can't change atoms)
```

---

## 💎 Dormant Potentialities (Existing Scaffolding)

### 1. **Organs Already Have Semantic Atom Infrastructure**
**All 11 `*_text_core.py` files have `_compute_atom_activations()`**
- Every organ loads semantic atoms from `semantic_atoms.json`
- Every organ computes continuous 0-1 activations for 7 atoms
- **Dormant Use:** Atoms could detect entity-aware patterns (e.g., "temporal_inquiry" for "When did Alice say...?")
- **Current:** Generic keyword matching, not entity-aware

### 2. **TSK Already Enriches Entities with Felt-State**
**`dae_interactive.py:387-484`**
- EntityExtractor accepts `felt_state` (polyvagal, urgency, nexuses)
- Creates `transductive_context` with healing trajectory
- **Dormant Use:** Could happen BEFORE organism for entity-aware atom activations
- **Current:** Happens AFTER organism (too late)

### 3. **Hebbian Memory Already Tracks Pattern Successes**
**`persona_layer/conversational_hebbian_memory.py`**
- Learns which patterns succeed in which contexts
- Stores polyvagal patterns, SELF-energy patterns
- **Dormant Use:** Could learn entity-specific patterns ("daughter mention → high empathy")
- **Current:** No entity data in ConversationalOutcome dataclass

### 4. **CARD Organ Already Accepts Context** 🌟 ARCHITECTURAL PATTERN
**`organs/modular/card/core/card_text_core.py:302`**
```python
def process_text_occasions(self, occasions, cycle=0, context: Dict = None) -> CARDResult:
    polyvagal_state = context.get('polyvagal_state', 'mixed_state')
    # ← PROVES organs CAN accept context!
```
- **Dormant Use:** Pattern exists to pass context to organs
- **Could extend:** All 11 organs with entity-aware context

### 5. **Phase 5 Learning Has 57D Organ Signatures**
**`persona_layer/phase5_learning_integration.py`**
- Extracts 57D organ signature (11 organs × 7 atoms - 20 meta-atoms)
- Clusters conversations into organic families
- **Dormant Use:** Could include entity features in signature (e.g., "mentions_family")
- **Current:** No entity awareness in clustering

---

## 🎯 Recommended Approach: HYBRID (A + D)

**Philosophy:** Integrate entity context INTO organism processing (following CARD organ's proven pattern) + Create entity-specific meta-atoms (leveraging existing bridge infrastructure)

### **Why Hybrid?**
1. **Option A (Context Integration):** Immediate entity awareness to organs via context parameter
2. **Option D (Meta-Atoms):** Leverages existing meta-atom infrastructure for entity-specific bridging
3. **Minimal Disruption:** Extends existing patterns (CARD already uses context, 10 meta-atoms already exist)

---

## 🛠️ Implementation Roadmap

### **Phase 1: Foundation (< 2 hours)** ✅ STARTED

#### ✅ Step 1.1: Add Entity Fields to TextOccasion (COMPLETED)
**File:** `transductive/text_occasion.py:96-103`
```python
# === ENTITY-AWARE FIELDS ===
known_entities: Dict[str, Any] = field(default_factory=dict)
entity_references: List[str] = field(default_factory=list)
entity_match_confidence: Dict[str, float] = field(default_factory=dict)
```
**Status:** ✅ COMPLETE (Nov 14, 2025)

#### 🔧 Step 1.2: Enrich TextOccasions with Entity Context (IN PROGRESS)
**File:** `persona_layer/conversational_organism_wrapper.py`
**Line:** 689 (`_create_text_occasions()`)
**Change:**
```python
def _create_text_occasions(self, text: str, context: Optional[Dict] = None):
    occasions = [...]  # Create occasions from text chunks

    # 🌀 Nov 14, 2025: Entity-aware enrichment
    if context and 'stored_entities' in context:
        stored_entities = context['stored_entities']

        for occasion in occasions:
            # Add stored entities to occasion
            occasion.known_entities = stored_entities

            # Detect entity references in this chunk
            occasion.entity_references = self._detect_entity_references(
                occasion.text, stored_entities
            )

    return occasions
```

#### 🔧 Step 1.3: Create Entity Reference Detector
**File:** `persona_layer/conversational_organism_wrapper.py`
**New Method:**
```python
def _detect_entity_references(self, text: str, stored_entities: Dict) -> List[str]:
    """
    Detect which stored entities are referenced in text.

    Returns: List of entity names/relations mentioned (e.g., ["Alice", "daughter"])
    """
    references = []
    text_lower = text.lower()

    # Check user_name
    if 'user_name' in stored_entities:
        name = stored_entities['user_name'].lower()
        if name in text_lower:
            references.append(stored_entities['user_name'])

    # Check family_members
    if 'family_members' in stored_entities:
        for member in stored_entities['family_members']:
            name = member.get('name', '').lower()
            relation = member.get('relation', '').lower()
            if name in text_lower:
                references.append(member['name'])
            if relation in text_lower:
                references.append(member['relation'])

    return references
```

### **Phase 2: Organism Integration (< 4 hours)**

#### Step 2.1: Pass Entity Context to All 11 Organs
**File:** `persona_layer/conversational_organism_wrapper.py:689-725`
**Change:**
```python
# Build entity-aware context dict
entity_context = {
    'stored_entities': context.get('stored_entities', {}),
    'username': context.get('username'),
    'entity_context_string': context.get('entity_context_string')
}

# Pass to all organs (following CARD pattern)
organ_results = {
    'LISTENING': self.listening.process_text_occasions(
        occasions, cycle=0, context=entity_context
    ),
    'EMPATHY': self.empathy.process_text_occasions(
        occasions, cycle=0, context=entity_context
    ),
    # ... all 11 organs with context parameter ...
}
```

#### Step 2.2: Update All 11 Organ Signatures
**Files:** All `organs/modular/*/core/*_text_core.py`
**Change Signature:**
```python
def process_text_occasions(
    self,
    occasions: List,
    cycle: int,
    context: Optional[Dict[str, Any]] = None  # ← Add parameter
) -> OrganResult:
    # Extract stored entities from context
    stored_entities = context.get('stored_entities', {}) if context else {}
    username = context.get('username') if context else None

    # Access entity references from occasions
    for occasion in occasions:
        entity_refs = occasion.entity_references  # ["Alice", "daughter"]
        known_entities = occasion.known_entities  # {user_name: "...", family_members: [...]}

        # Entity-aware atom activation
        # Check if text matches stored entity patterns
```

### **Phase 3: Meta-Atom Integration (< 2 hours)**

#### Step 3.1: Create Entity-Specific Meta-Atoms
**File:** `persona_layer/shared_meta_atoms.json`
**Add:**
```json
{
  "meta_atoms": {
    "entity_recall_precision": {
      "description": "Precise recall of stored entity details (names, relationships, preferences)",
      "participating_organs": ["LISTENING", "WISDOM", "PRESENCE"],
      "activation_logic": "Detect when user asks about stored entities + organism provides accurate recall"
    },
    "relationship_acknowledgment": {
      "description": "Acknowledging known relationships (family, friends) with personalized presence",
      "participating_organs": ["EMPATHY", "BOND", "PRESENCE"],
      "activation_logic": "Detect family/friend mentions + empathy coherence when referencing stored relationships"
    },
    "preference_attunement": {
      "description": "Responding with awareness of stored user preferences",
      "participating_organs": ["LISTENING", "EMPATHY", "WISDOM"],
      "activation_logic": "Detect preference-related input + wisdom suggests options aligned with stored preferences"
    }
  }
}
```

#### Step 3.2: Update MetaAtomActivator
**File:** `persona_layer/meta_atom_activator.py`
**Add Methods:**
```python
def _activate_entity_recall_precision(self, organ_results, context):
    """Activate when organism accurately recalls stored entities."""
    stored_entities = context.get('stored_entities', {})
    entity_refs = context.get('entity_references', [])

    # Check if LISTENING detected entity reference
    listening_result = organ_results.get('LISTENING')
    # Check if reference matches stored entity
    # Compute activation strength based on match accuracy

def _activate_relationship_acknowledgment(self, organ_results, context):
    """Activate when organism acknowledges stored relationships."""
    family_members = context.get('stored_entities', {}).get('family_members', [])

    # Check if EMPATHY + BOND activated for family mention
    # Higher activation for personalized acknowledgment
```

### **Phase 4: Testing & Validation (< 2 hours)**

#### Step 4.1: Create Entity Awareness Test Suite
**File:** `test_organism_entity_awareness.py`
**Test Cases:**
```python
def test_name_recall():
    """Test organism remembers user's name during prehension."""
    # Setup: Store user_name="Alice" in user_profile
    # Input: "do you remember my name?"
    # Expected: Organs see known_entities={'user_name': 'Alice'}
    # Expected: entity_recall_precision meta-atom activates
    # Expected: Emission includes "Alice"

def test_family_member_recognition():
    """Test organism recognizes stored family members."""
    # Setup: Store family_members=[{"name": "Jake", "relation": "son"}]
    # Input: "how is Jake doing?"
    # Expected: entity_references=["Jake"]
    # Expected: relationship_acknowledgment meta-atom activates

def test_preference_attunement():
    """Test organism responds with stored preference awareness."""
    # Setup: Store preferences={"likes": ["hiking"], "dislikes": ["spicy food"]}
    # Input: "suggest a dinner option"
    # Expected: Wisdom organ sees known_entities['preferences']
    # Expected: preference_attunement meta-atom activates
```

---

## 📊 Success Metrics

**Immediate (Phase 1-2):**
- ✅ TextOccasions enriched with entity data
- ✅ All 11 organs receive entity context during prehension
- ✅ Organs can access `occasion.known_entities` and `occasion.entity_references`

**Short-term (Phase 3):**
- ✅ 3 entity-specific meta-atoms operational
- ✅ MetaAtomActivator detects entity-aware patterns
- ✅ Phase 5 learning includes entity features in 57D signatures

**Long-term (Phase 4):**
- ✅ Name memorization working ("remember my name?" → "Your name is Alice!")
- ✅ Family member recognition ("how is Jake?" → organism knows Jake is user's son)
- ✅ Preference attunement (suggestions aligned with stored preferences)
- ✅ Hebbian memory learns entity-specific success patterns

---

## 🔮 Future Enhancements (Post-Integration)

**Entity-Aware Semantic Atoms:**
- Update `semantic_atoms.json` with entity-specific patterns
- Example: `"personalized_inquiry": {"keywords": ["[NAME]", "how is [RELATIONSHIP]"]}`

**Entity-Specific Organic Families:**
- Cluster conversations by entity mention patterns
- Example: "family_introduction" family, "crisis_with_child" family

**TSK Entity Disambiguation:**
- Use polyvagal state to disambiguate entity mentions
- Example: "Alice mentioned during ventral state" vs "Alice mentioned during crisis"

**Hebbian Entity Learning:**
- Learn which entity mentions predict positive outcomes
- Strengthen organ patterns that led to accurate entity recall

---

## 🚨 Critical Insights

### **Why This Matters**

**Before (BROKEN):**
```
Entity Extraction (isolated) → Organism (blind to entities) → Emission (too late)
```

**After (INTEGRATED):**
```
Entity Extraction → TextOccasion Enrichment → Organism (entity-aware prehension) → Emission (coherent recall)
```

### **Key Architectural Lesson**

**Don't treat entities as "application concern" (like UI feedback).**
**Entities are CORE ORGANISM CAPABILITY (like trauma detection, polyvagal state).**

Entity awareness belongs in **persona_layer/** (core architecture), not just `dae_interactive.py` (application layer).

### **Leverage Existing Patterns**

1. **CARD already accepts context** → Extend to all 11 organs
2. **10 meta-atoms already bridge organs** → Add 3 entity-specific meta-atoms
3. **TSK already enriches entities** → Move enrichment PRE-prehension
4. **Hebbian memory already learns patterns** → Add entity features to outcomes

---

## 📝 Implementation Status

| Phase | Task | Status | ETA |
|-------|------|--------|-----|
| **Phase 1** | **Foundation** | 🔧 **IN PROGRESS** | **< 2 hours** |
| 1.1 | Add entity fields to TextOccasion | ✅ COMPLETE | - |
| 1.2 | Enrich TextOccasions with entity context | 🔧 IN PROGRESS | 30 min |
| 1.3 | Create entity reference detector | 🔧 IN PROGRESS | 30 min |
| **Phase 2** | **Organism Integration** | ⏳ PENDING | < 4 hours |
| 2.1 | Pass entity context to all 11 organs | ⏳ PENDING | 1 hour |
| 2.2 | Update all 11 organ signatures | ⏳ PENDING | 3 hours |
| **Phase 3** | **Meta-Atom Integration** | ⏳ PENDING | < 2 hours |
| 3.1 | Create entity-specific meta-atoms | ⏳ PENDING | 1 hour |
| 3.2 | Update MetaAtomActivator | ⏳ PENDING | 1 hour |
| **Phase 4** | **Testing** | ⏳ PENDING | < 2 hours |
| 4.1 | Create entity awareness test suite | ⏳ PENDING | 2 hours |

**Total Estimated Effort:** 8-10 hours
**Current Progress:** Phase 1.1 complete (10% done)

---

## 🔗 Related Documents

- `MEMORY_PERSISTENCE_FIX_NOV14_2025.md` - Memory persistence bug fixes (prerequisite)
- `persona_layer/entity_extraction/` - Entity extraction infrastructure
- `persona_layer/shared_meta_atoms.json` - Existing meta-atom architecture
- `organs/modular/card/core/card_text_core.py` - Proven context parameter pattern
- `persona_layer/phase5_learning_integration.py` - Organic learning infrastructure

---

**Created:** November 14, 2025
**Status:** 🔧 IN PROGRESS - Foundation phase started
**Next:** Complete TextOccasion enrichment + entity reference detection

🌀 **"From isolated entity extraction to organism-integrated entity awareness. Unblocking dormant prehension capabilities."** 🌀
