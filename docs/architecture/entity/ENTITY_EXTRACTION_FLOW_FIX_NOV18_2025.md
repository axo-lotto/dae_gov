# Entity Extraction Flow Fix (November 18, 2025)

## Critical Issue Identified

**Problem**: Entity extraction happens AFTER Phase 2 V0 convergence, but NEXUS organ needs entities DURING the convergence cycles.

**Evidence from Debug Output**:
```
Cycle 1:
🔍 DEBUG Phase2 Cycle 1: entity_memory_available = False
🔍 DEBUG Phase2 Cycle 1: mentioned_entities count = 0
🔍 NEXUS DEBUG: entity_memory_available = False
🔍 NEXUS DEBUG: mentioned_entities = 0
```

**Root Cause**: Current flow in `conversational_organism_wrapper.py`:
```
1. process_text() called
2. Phase 2 V0 convergence (multi-cycle)
   └─> NEXUS activated BUT entities not available yet
3. AFTER convergence: dae_interactive.py extracts entities
4. Entities arrive too late for NEXUS to use
```

---

## Current Flow (Broken)

```
conversational_organism_wrapper.process_text()
│
├─> PRE-EMISSION Entity Prehension (lines 919-954)
│   └─> Calls retrieve_relevant_entities()
│       └─> Queries Neo4j/storage for PAST entities
│       └─> Does NOT extract NEW entities from current input
│
├─> Phase 2: Multi-cycle V0 convergence
│   ├─> Cycle 1: NEXUS sees entity_prehension (EMPTY or stale)
│   ├─> Cycle 2: NEXUS sees entity_prehension (EMPTY or stale)
│   └─> Cycle 3: NEXUS sees entity_prehension (EMPTY or stale)
│
└─> Returns result to dae_interactive.py
    │
    └─> dae_interactive.py (lines 490-575)
        ├─> Lines 490-540: Extract entities (TOO LATE!)
        └─> Lines 558-575: Populate entity_prehension (AFTER Phase 2!)
```

---

## Required Fix

### Option A: Extract Entities BEFORE Phase 2 (RECOMMENDED)

**Move entity extraction to organism wrapper, BEFORE V0 convergence begins**

**Location**: `persona_layer/conversational_organism_wrapper.py`

**Changes**:

```python
def process_text(
    self,
    text: str,
    context: Optional[Dict] = None,
    enable_tsk_recording: bool = False,
    enable_phase2: bool = True,
    user_id: Optional[str] = None,
    user_satisfaction: Optional[float] = None
) -> Dict[str, Any]:
    """
    Process user input through organism.

    🌀 Nov 18, 2025: Entity extraction MOVED BEFORE Phase 2
    to ensure NEXUS has entities during V0 convergence.
    """

    # ═══════════════════════════════════════════════════════════════════
    # STEP 0: EXTRACT ENTITIES **BEFORE** PHASE 2 (NEW - Nov 18, 2025)
    # ═══════════════════════════════════════════════════════════════════

    from persona_layer.memory_intent_detector import MemoryIntentDetector
    from persona_layer.entity_extractor import EntityExtractor

    # Initialize extractors (singleton pattern recommended)
    if not hasattr(self, '_memory_intent_detector'):
        self._memory_intent_detector = MemoryIntentDetector()
    if not hasattr(self, '_entity_extractor'):
        self._entity_extractor = EntityExtractor()

    # Detect memory intent
    intent_result = self._memory_intent_detector.detect(text)

    # Extract entities if memory-related
    current_turn_entities = []
    if intent_result.get('is_memory_related', False):
        current_turn_entities = self._entity_extractor.extract_entities(
            text,
            intent_result
        )

    # Populate entity_prehension (NEXUS-compatible format)
    if current_turn_entities:
        mentioned_entities = [
            {
                'name': entity['entity_value'],
                'type': entity.get('entity_type', 'person'),
                'relationship': entity.get('relationship'),
                'source': entity.get('source', 'explicit')
            }
            for entity in current_turn_entities
        ]

        entity_prehension = {
            'entity_memory_available': True,
            'mentioned_entities': mentioned_entities,
            'user_name': context.get('username', 'User') if context else 'User'
        }
    else:
        entity_prehension = {
            'entity_memory_available': False,
            'mentioned_entities': [],
            'user_name': context.get('username', 'User') if context else 'User'
        }

    # Store in context for Phase 2
    if context is None:
        context = {}
    context['entity_prehension'] = entity_prehension
    context['current_turn_entities'] = current_turn_entities

    # ═══════════════════════════════════════════════════════════════════
    # EXISTING CODE CONTINUES (with entities now available)
    # ═══════════════════════════════════════════════════════════════════

    # Initialize context
    if context is None:
        context = {}

    context['raw_input'] = text
    context['processing_timestamp'] = datetime.now().isoformat()

    # [REST OF EXISTING CODE...]
```

---

### Option B: Keep Extraction in dae_interactive.py but Pass Entities

**Less recommended** - requires passing entities as parameter

```python
# In dae_interactive.py (lines 490-540)
# Extract entities BEFORE calling organism

# Detect memory intent
intent_result = self.memory_intent_detector.detect(user_input)

# Extract entities
current_turn_entities = []
if intent_result.get('is_memory_related', False):
    current_turn_entities = self.entity_extractor.extract_entities(
        user_input,
        intent_result
    )

# Create entity prehension
entity_prehension = {
    'entity_memory_available': len(current_turn_entities) > 0,
    'mentioned_entities': [...],
    'user_name': self.user.get('username', 'User')
}

# Pass to organism via context
context['entity_prehension'] = entity_prehension
context['current_turn_entities'] = current_turn_entities

# THEN call organism
result = self.organism.process_text(
    user_input,
    context=context,  # Now has entities!
    enable_tsk_recording=self.enable_tsk_recording,
    enable_phase2=self.enable_phase2,
    user_id=self.user['user_id'],
    user_satisfaction=user_satisfaction
)
```

---

## Recommended Implementation: Option A

**Rationale**:
1. Entity extraction is CORE organism functionality, not UI concern
2. Needed for ALL modes (interactive, training, validation)
3. Ensures entities available during Phase 2 (critical for NEXUS)
4. Cleaner separation of concerns

**Files to Modify**:

1. **`persona_layer/conversational_organism_wrapper.py`**
   - Add entity extraction at top of `process_text()` (lines ~825-870)
   - Initialize `MemoryIntentDetector` and `EntityExtractor` as singletons
   - Populate `context['entity_prehension']` BEFORE Phase 2

2. **`dae_interactive.py`**
   - REMOVE entity extraction code (lines 490-575)
   - Entity prehension now handled by organism
   - Keep entity display for user feedback

3. **`training/entity_memory_epoch_training_with_tsk.py`**
   - NO CHANGES NEEDED (organism handles it automatically)

---

## Expected Impact

### Before Fix:
```
All 50 training pairs:
   Entity memory available: ❌ No (0/50)
   Entity recall accuracy: 0.00
   NEXUS differentiation: ❌ Not executed
```

### After Fix:
```
All 50 training pairs:
   Entity memory available: ✅ Yes (38/50, 76%)
   Entity recall accuracy: 0.65-0.85 (depending on Neo4j data)
   NEXUS differentiation: ✅ Executed (38 pairs)
```

---

## Testing Plan

1. **Unit Test** (entity extraction in organism):
```python
def test_entity_extraction_before_phase2():
    organism = ConversationalOrganismWrapper()

    result = organism.process_text(
        "Do you remember my daughter Emma?",
        enable_phase2=True
    )

    # Verify entities extracted
    assert 'entity_prehension' in result
    assert result['entity_prehension']['entity_memory_available'] == True
    assert len(result['entity_prehension']['mentioned_entities']) >= 1

    # Verify NEXUS saw entities
    assert 'nexus_entity_activation' in result  # If NEXUS logged it
```

2. **Integration Test** (interactive mode):
```bash
python3 dae_interactive.py

You: "I have a daughter named Emma"
# Should see: entity_memory_available = True, mentioned_entities = 1

You: "Tell me about Emma"
# Should see: NEXUS activates with Emma context from Neo4j
```

3. **Training Validation** (epoch 30):
```bash
python3 training/entity_memory_epoch_training_with_tsk.py 30

# Expected output:
#   Entity memory available: ✅ Yes (38/50)
#   Entity recall accuracy: 0.75+
#   NEXUS differentiation: ✅ Executed
```

---

## Implementation Steps

### Step 1: Add Entity Extractors to Organism (15 min)

**File**: `persona_layer/conversational_organism_wrapper.py`

**Lines ~150-160** (in `__init__`):
```python
# Entity extraction components (Nov 18, 2025)
from persona_layer.memory_intent_detector import MemoryIntentDetector
from persona_layer.entity_extractor import EntityExtractor

self._memory_intent_detector = MemoryIntentDetector()
self._entity_extractor = EntityExtractor()
```

### Step 2: Extract Entities BEFORE Phase 2 (30 min)

**File**: `persona_layer/conversational_organism_wrapper.py`

**Lines ~830-900** (at top of `process_text()`):
```python
# ═══════════════════════════════════════════════════════════════════
# 🌀 Nov 18, 2025: EXTRACT ENTITIES **BEFORE** PHASE 2
# Critical: NEXUS needs entities DURING V0 convergence cycles
# ═══════════════════════════════════════════════════════════════════

# Detect memory intent
intent_result = self._memory_intent_detector.detect(text)

# Extract entities if memory-related
current_turn_entities = []
if intent_result.get('is_memory_related', False):
    current_turn_entities = self._entity_extractor.extract_entities(
        text,
        intent_result
    )

# Populate entity_prehension (NEXUS-compatible format)
if current_turn_entities:
    mentioned_entities = [
        {
            'name': entity['entity_value'],
            'type': entity.get('entity_type', 'person'),
            'relationship': entity.get('relationship'),
            'source': entity.get('source', 'explicit')
        }
        for entity in current_turn_entities
    ]

    entity_prehension = {
        'entity_memory_available': True,
        'mentioned_entities': mentioned_entities,
        'user_name': context.get('username', 'User') if context else 'User'
    }
else:
    entity_prehension = {
        'entity_memory_available': False,
        'mentioned_entities': [],
        'user_name': context.get('username', 'User') if context else 'User'
    }

# Initialize context if None
if context is None:
    context = {}

# Store for Phase 2
context['entity_prehension'] = entity_prehension
context['current_turn_entities'] = current_turn_entities

# [EXISTING CODE CONTINUES...]
```

### Step 3: Remove Redundant Code from dae_interactive.py (10 min)

**File**: `dae_interactive.py`

**Lines 490-575**: Comment out or remove (organism handles it now)

### Step 4: Test & Validate (30 min)

Run tests listed above, verify entity detection working during Phase 2.

---

## Timeline

- **Step 1-3**: 1 hour (implementation)
- **Step 4**: 30 min (testing)
- **Total**: 1.5 hours

---

## Success Criteria

✅ Entity extraction happens BEFORE Phase 2 V0 convergence
✅ NEXUS sees `entity_memory_available = True` during cycles
✅ Interactive mode: "I am Xeno" → NEXUS activates with entities
✅ Training mode: 76%+ entity detection rate (38/50 pairs)
✅ Entity-organ tracker receives entities after emission
✅ No regression in existing functionality

---

**Date**: November 18, 2025
**Status**: Implementation Plan Ready
**Priority**: CRITICAL (blocks NEXUS organ effectiveness)
**Estimated Impact**: +40pp entity recall accuracy, NEXUS fully operational
