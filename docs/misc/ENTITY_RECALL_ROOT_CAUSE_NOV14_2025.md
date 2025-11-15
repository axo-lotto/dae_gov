# Entity Recall Root Cause Analysis
## November 14, 2025

---

## 🎯 User Issue

**Report:** "still no entity persistance or recall even of user name!"

**Evidence:**
```
User: "Emi" (user_20251113_143117)
Turn 1: "Hello there! my name is Emiliano"
Turn 2: "do you remember my name?"
DAE Response: "I remember it's something you shared with me earlier. You said it was starting with an 'A'..." ❌
```

**Expected:** DAE should recall "Emiliano" from Turn 1

---

## 🔍 Investigation Results

### Entity Storage: ✅ WORKING

**Verification:**
```python
from persona_layer.user_registry import UserRegistry
registry = UserRegistry()
user_state = registry.load_user_state('user_20251113_143117')

profile = EnhancedUserProfile.from_dict(user_state['user_profile'])
print(profile.entities)
# Result: {'user_name': 'Emiliano'} ✅ STORED CORRECTLY
```

**Conclusion:** Entities ARE being extracted and stored correctly to disk.

---

### Entity Loading: ✅ WORKING

**File:** `dae_interactive.py` lines 315-343

```python
# 🌀 Phase 1.8++: Load entity context on EVERY turn
if 'user_profile' in self.user_state:
    profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])

    # Add entity context string
    context['entity_context_string'] = profile.get_entity_context_string()

    # Add stored entities
    if profile.entities:
        context['stored_entities'] = profile.entities  # ✅ LOADED
```

**Result:**
```python
context = {
    'entity_context_string': "Known information:\n- User's name: Emiliano",
    'stored_entities': {'user_name': 'Emiliano'},
    ...
}
```

**Conclusion:** Entity context IS loaded into `context` dict correctly.

---

### Entity Pass-Through to Organs: ✅ WORKING

**File:** `persona_layer/conversational_organism_wrapper.py`

**Lines 692-697 (Single-cycle path):**
```python
# 🌀 Nov 14, 2025: Build entity context for all organs (Phase 2.1)
entity_context = {
    'stored_entities': context.get('stored_entities', {}),
    'username': context.get('username')
}

# Process through ALL 11 organs
organ_results = {
    'LISTENING': self.listening.process_text_occasions(text_occasions, cycle=cycle, context=entity_context),
    ...
}
```

**Lines 2026-2030 (Multi-cycle path):**
```python
# 🌀 Nov 14, 2025: Build entity context for all organs (Phase 2.1)
entity_context = {
    'stored_entities': context.get('stored_entities', {}) if context else {},
    'username': context.get('username') if context else None
}
```

**Conclusion:** Organs ARE receiving entity context correctly.

---

### Emission Generation: ❌ **BROKEN - ROOT CAUSE FOUND**

**File:** `persona_layer/conversational_organism_wrapper.py` lines 912-921

```python
emitted_phrases = self.emission_generator.generate_emissions(
    nexuses=nexuses,
    num_emissions=num_emissions,
    prefer_variety=True,
    user_input=text,
    organ_results=organ_results,
    v0_energy=final_energy,
    satisfaction=satisfaction_final,
    memory_context=None  # ❌ NOT PASSING ENTITY CONTEXT
    # ❌ MISSING: entity_context_string
    # ❌ MISSING: memory_intent
)
```

**What's available but NOT being passed:**
```python
# Context dict has these available (lines 874-880):
context = {
    'stored_entities': {'user_name': 'Emiliano'},  # ✅ Available
    'username': 'Emi',  # ✅ Available
    'entity_context_string': "Known information:\n- User's name: Emiliano"  # ✅ Available
    'memory_intent': True,  # ✅ Available
    ...
}
```

**Emission Generator CAN Accept These:**

**File:** `persona_layer/emission_generator.py` line 1398-1399

```python
def _generate_felt_guided_llm_single(
    self,
    user_input: str,
    organ_results: Dict,
    nexuses: List,
    v0_energy: float,
    satisfaction: float,
    memory_context: Optional[List[Dict]] = None,
    entity_context_string: Optional[str] = None,  # ✅ PARAMETER EXISTS
    memory_intent: bool = False  # ✅ PARAMETER EXISTS
) -> Optional[EmittedPhrase]:
```

**Conclusion:** The emission generator HAS the capability to use entity context, but it's NOT being passed from the organism wrapper!

---

## 🐛 Root Cause Summary

### The Bug

**Location:** `persona_layer/conversational_organism_wrapper.py` lines 912-921

**Problem:** When calling `emission_generator.generate_emissions()`, the method does NOT pass:
1. `entity_context_string` - The formatted string with user's name and other entities
2. `memory_intent` - Whether memory-related intent was detected

**Impact:** The LLM fallback emission has NO ACCESS to stored entity information, so it cannot recall the user's name.

**Why This Causes the User's Issue:**
- User "Emi" has 0 nexuses formed (hebbian fallback mode)
- Emission generator uses `_generate_felt_guided_llm_fallback()`
- This calls `_generate_felt_guided_llm_single()` which accepts `entity_context_string`
- But `generate_emissions()` never receives this parameter, so it can't pass it down
- LLM generates response WITHOUT knowing the user's name is "Emiliano"

---

## 📊 Entity Flow Trace

```
✅ dae_interactive.py:315-343
   └─> Load entities from profile → context['stored_entities'] = {'user_name': 'Emiliano'}

✅ dae_interactive.py:378
   └─> Pass context to organism.process_text(context=context)

✅ conversational_organism_wrapper.py:692-697 (or 2026-2030)
   └─> Extract entities from context → entity_context = {'stored_entities': {...}}
   └─> Pass to organs via process_text_occasions(context=entity_context)

✅ All 11 organs receive entity_context

❌ conversational_organism_wrapper.py:912-921 **<-- BUG HERE**
   └─> Call emission_generator.generate_emissions()
   └─> MISSING: entity_context_string parameter
   └─> MISSING: memory_intent parameter
   └─> Entities stop flowing here

❌ emission_generator.py:1409-1417
   └─> felt_guided_llm.generate_from_felt_state()
   └─> entity_context_string = None ❌
   └─> LLM has NO KNOWLEDGE of user's name
```

---

## 🔧 The Fix Required

### File: `persona_layer/conversational_organism_wrapper.py`

**Line 912-921:** Modify `emission_generator.generate_emissions()` call

**Current (BROKEN):**
```python
emitted_phrases = self.emission_generator.generate_emissions(
    nexuses=nexuses,
    num_emissions=num_emissions,
    prefer_variety=True,
    user_input=text,
    organ_results=organ_results,
    v0_energy=final_energy,
    satisfaction=satisfaction_final,
    memory_context=None  # TODO comment
)
```

**Fixed:**
```python
# 🌀 Nov 14, 2025: Pass entity context to emission generator
entity_context_string = context.get('entity_context_string', '') if context else ''
memory_intent = context.get('memory_intent', False) if context else False

emitted_phrases = self.emission_generator.generate_emissions(
    nexuses=nexuses,
    num_emissions=num_emissions,
    prefer_variety=True,
    user_input=text,
    organ_results=organ_results,
    v0_energy=final_energy,
    satisfaction=satisfaction_final,
    memory_context=None,  # TODO: Pass from dae_interactive if hybrid enabled
    entity_context_string=entity_context_string,  # 🌀 CRITICAL FIX
    memory_intent=memory_intent  # 🌀 CRITICAL FIX
)
```

### File: `persona_layer/emission_generator.py`

**Line 907-920:** Modify `generate_emissions()` signature to accept new parameters

**Current:**
```python
def generate_emissions(
    self,
    nexuses: List,
    num_emissions: int = 3,
    prefer_variety: bool = True,
    user_input: str = "",
    organ_results: Dict = None,
    v0_energy: float = 1.0,
    satisfaction: float = 0.0,
    memory_context: Optional[List[Dict]] = None
) -> List[EmittedPhrase]:
```

**Fixed:**
```python
def generate_emissions(
    self,
    nexuses: List,
    num_emissions: int = 3,
    prefer_variety: bool = True,
    user_input: str = "",
    organ_results: Dict = None,
    v0_energy: float = 1.0,
    satisfaction: float = 0.0,
    memory_context: Optional[List[Dict]] = None,
    entity_context_string: Optional[str] = None,  # 🌀 NEW (Nov 14, 2025)
    memory_intent: bool = False  # 🌀 NEW (Nov 14, 2025)
) -> List[EmittedPhrase]:
```

**Lines 980-989:** Pass parameters to `_generate_felt_guided_llm_single()`

```python
emission = self._generate_felt_guided_llm_single(
    user_input=user_input,
    organ_results=organ_results,
    nexuses=nexuses,
    v0_energy=v0_energy,
    satisfaction=satisfaction,
    memory_context=memory_context,
    entity_context_string=entity_context_string,  # 🌀 PASS THROUGH
    memory_intent=memory_intent  # 🌀 PASS THROUGH
)
```

**Line 1459:** Same for fallback path

```python
emission = self._generate_felt_guided_llm_single(
    user_input=user_input,
    organ_results=organ_results,
    nexuses=nexuses,
    v0_energy=v0_energy,
    satisfaction=satisfaction,
    memory_context=memory_context,
    entity_context_string=entity_context_string,  # 🌀 PASS THROUGH
    memory_intent=memory_intent  # 🌀 PASS THROUGH
)
```

---

## ✅ Expected Outcome After Fix

**User Session:**
```
Turn 1: "Hello there! my name is Emiliano"
→ Entity extracted: {'user_name': 'Emiliano'}
→ Stored to profile ✅
→ Emission: "Nice to meet you, Emiliano!"

Turn 2: "do you remember my name?"
→ Entity loaded: {'user_name': 'Emiliano'}
→ Passed to organs ✅
→ Passed to emission_generator ✅ (AFTER FIX)
→ LLM receives: entity_context_string="Known information:\n- User's name: Emiliano"
→ Emission: "Yes! Your name is Emiliano." ✅
```

---

## 📝 Additional Observations

### Reconstruction Pipeline Path Works

**Lines 874-886:** The reconstruction pipeline DOES receive entity context correctly:

```python
reconstruction_context = {
    'user_message': text,
    'family_v0_learner': self.family_v0_learner,
    'stored_entities': context.get('stored_entities', {}),  # ✅ PASSED
    'username': context.get('username')  # ✅ PASSED
}

reconstruction_result = self.reconstruction_pipeline.reconstruct_emission(
    felt_state=felt_state_for_reconstruction,
    context=reconstruction_context
)
```

**This suggests:**
- If reconstruction pipeline is enabled, entity recall MIGHT work
- But fallback emission generator path (lines 912-921) is broken
- User "Emi" is using fallback path (0 nexuses), so they hit the bug

---

## 🎯 Summary

**Problem:** Entity context stops flowing at emission generation step

**Root Cause:** `emission_generator.generate_emissions()` not receiving entity parameters

**Files to Modify:**
1. `persona_layer/conversational_organism_wrapper.py` (lines 912-921)
2. `persona_layer/emission_generator.py` (lines 907-920, 980-989, 1459)

**Complexity:** Low - just parameter pass-through

**Risk:** Very low - parameters are optional, backward compatible

**Expected Fix Time:** < 5 minutes

---

**Last Updated:** November 14, 2025
**Status:** Root cause identified, fix ready to implement
**Priority:** CRITICAL - user-facing issue
**Impact:** Affects ALL entity recall when using felt-guided LLM fallback path
