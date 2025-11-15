# 🔧 Entity Memory Remediation Strategy
**Date:** November 14, 2025
**Status:** DISCONNECT IDENTIFIED - REMEDIATION PLAN READY

---

## ✅ ROOT CAUSE CONFIRMED

**File:** `persona_layer/conversational_organism_wrapper.py`
**Line:** 844
**Issue:** `context` variable **OVERWRITTEN**, discarding `entity_context_string`

```python
# Line 822-841: felt_state_for_reconstruction built with username from context ✅
felt_state_for_reconstruction = {
    ...
    'username': context.get('username')  # ← Gets username from original context
}

# Line 844-847: context OVERWRITTEN ❌
context = {
    'user_message': text,
    'family_v0_learner': self.family_v0_learner
}
# ← Original context (with entity_context_string) is GONE!

# Line 850-853: reconstruction_pipeline called with NEW context ❌
reconstruction_result = self.reconstruction_pipeline.reconstruct_emission(
    felt_state=felt_state_for_reconstruction,
    context=context  # ← This is the NEW context, not the original!
)
```

**What happens:**
1. `dae_interactive.py` loads `entity_context_string` into `context` ✅
2. Passes `context` to `organism.process_text()` ✅
3. Organism extracts `username` from `context` and adds to `felt_state` ✅
4. **But then organism OVERWRITES `context` variable** ❌
5. Reconstruction pipeline receives NEW context without `entity_context_string` ❌
6. Our Phase 1.8++ code in reconstruction_pipeline tries to extract it from `felt_state` ✅
7. But it's not in `felt_state` either because organism didn't add it! ❌

---

## 🎯 Remediation Strategy

### Option 1: Add entity_context_string to felt_state_for_reconstruction (RECOMMENDED)

**Why:** Cleanest fix, follows existing pattern, minimal changes

**Implementation:**
```python
# File: persona_layer/conversational_organism_wrapper.py
# Line: 822-841

felt_state_for_reconstruction = {
    'organ_coherences': {name: getattr(result, 'coherence', 0.0)
                        for name, result in organ_results.items()},
    'semantic_fields': semantic_fields,
    'v0_energy': final_energy,
    'satisfaction': satisfaction_final,
    'convergence_cycles': convergence_cycles,
    'transduction_state': None,
    'eo_polyvagal_state': eo_polyvagal,
    'ndam_urgency': ndam_urgency,
    'kairos_detected': kairos_cycle_index is not None,
    'user_input': text,
    'organ_results': organ_results,
    'memory_context': None,
    'organism_narrative': context.get('organism_narrative'),
    'username': context.get('username'),
    # 🌀 PHASE 1.8++: Entity memory persistence (Nov 14, 2025)
    'entity_context_string': context.get('entity_context_string'),  # ← ADD THIS
    'memory_intent': context.get('memory_intent', False)            # ← AND THIS
}
```

**Testing:**
- Our Phase 1.8++ code in `organ_reconstruction_pipeline.py` already extracts these
- LLM prompt builder already injects `entity_context_string` (Phase 1.8)
- Should work immediately

---

### Option 2: Preserve original context (ALTERNATIVE)

**Why:** Ensures all context data flows through

**Implementation:**
```python
# File: persona_layer/conversational_organism_wrapper.py
# Line: 844-847

# Build context for reconstruction (includes DAE 3.0 family learner)
reconstruction_context = {
    **context,  # ← Preserve all original context
    'user_message': text,
    'family_v0_learner': self.family_v0_learner
}

# Call reconstruction pipeline
reconstruction_result = self.reconstruction_pipeline.reconstruct_emission(
    felt_state=felt_state_for_reconstruction,
    context=reconstruction_context  # ← Use merged context
)
```

**Risk:** Context dict might have unexpected keys that could interfere

---

### Option 3: Add to both felt_state AND context (BELT & SUSPENDERS)

**Why:** Maximum robustness, works with both extraction paths

**Implementation:**
```python
# In felt_state_for_reconstruction (line 841):
'entity_context_string': context.get('entity_context_string'),
'memory_intent': context.get('memory_intent', False),

# AND in reconstruction context (line 844-847):
reconstruction_context = {
    'user_message': text,
    'family_v0_learner': self.family_v0_learner,
    'entity_context_string': context.get('entity_context_string'),  # ← ADD
    'memory_intent': context.get('memory_intent', False)            # ← ADD
}
```

---

## 📋 Implementation Plan

### Phase 1: Quick Fix (Option 1) - IMMEDIATE

**File to modify:** `persona_layer/conversational_organism_wrapper.py`

**Changes:**
1. Line ~841: Add `'entity_context_string': context.get('entity_context_string'),`
2. Line ~842: Add `'memory_intent': context.get('memory_intent', False)`

**Test:**
```bash
python3 supervised_entity_memory_validator.py
```

**Expected result:**
- Turn 2+ should now show entity knowledge in responses
- "Sarah" should appear when asking about weather
- "Do you remember my name?" should respond "Yes, Sarah"

---

### Phase 2: Validation Testing - NEXT

**Run comprehensive test suite:**

```bash
# Test 1: Supervised scenarios
python3 supervised_entity_memory_validator.py

# Test 2: Interactive session
python3 dae_interactive.py
# Then manually test:
# User: "My name is Alex"
# User: "What's 2+2?"  (should say "Alex" somewhere)
# User: "Do you remember my name?"  (should say "Yes, Alex")

# Test 3: Direct organism test
python3 -c "
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
organism = ConversationalOrganismWrapper()
context = {'entity_context_string': 'Known info: User name is Sarah'}
result = organism.process_text('Hello', context=context, enable_phase2=True)
print(result['emission_text'])
# Should mention Sarah or use personalized greeting
"
```

---

### Phase 3: Debug Logging - VERIFY

**Add temporary debug output to confirm fix:**

```python
# In conversational_organism_wrapper.py, after line 841:
if context.get('entity_context_string'):
    print(f"🔍 DEBUG: Entity context in felt_state: {context.get('entity_context_string')[:50]}...")

# In organ_reconstruction_pipeline.py, line ~558:
if entity_context_string:
    print(f"🔍 DEBUG: Entity context extracted: {entity_context_string[:50]}...")

# In llm_felt_guidance.py, after receiving entity_context_string:
if entity_context_string:
    print(f"🔍 DEBUG: Entity context in LLM prompt builder: {entity_context_string[:50]}...")
```

---

### Phase 4: Epoch Training Validation - SUPERVISED LEARNING

**Once fix confirmed working, run supervised training:**

```bash
# Create entity memory training orchestrator
python3 entity_memory_epoch_trainer.py \
    --scenarios knowledge_base/entity_memory_training_pairs.json \
    --epochs 3 \
    --output results/entity_memory_training_results.json
```

**Metrics to track:**
1. Entity recall accuracy (Turn N mentions Turn 1 entity) - Target: > 90%
2. Entity context presence in felt_state - Target: 100%
3. LLM response contains expected entities - Target: > 80%
4. Memory persistence across 3+ turns - Target: 100%

---

## 🔬 Verification Checklist

**After implementing Option 1:**

- [ ] Code change made to conversational_organism_wrapper.py
- [ ] Grep confirms `entity_context_string` in `felt_state_for_reconstruction`
- [ ] Grep confirms `memory_intent` in `felt_state_for_reconstruction`
- [ ] Static validation passes: `python3 validate_entity_fix.py`
- [ ] Supervised validation passes: `python3 supervised_entity_memory_validator.py`
- [ ] Interactive test: Manual conversation with name introduction + recall
- [ ] Debug logging shows entity_context flowing through all stages
- [ ] No regressions: Existing tests still pass

---

## 📊 Success Criteria

**Minimum Viable Fix:**
- ✅ Entity context string reaches reconstruction pipeline
- ✅ Entity context string reaches LLM prompt builder
- ✅ LLM demonstrates knowledge of stored entities in responses
- ✅ Multi-turn entity persistence (3+ turns)

**Full Success:**
- ✅ All 5 supervised scenarios pass
- ✅ Entity recall accuracy > 90%
- ✅ TSK differentiation working (crisis vs healing contexts)
- ✅ Entity updates handled correctly
- ✅ No false negatives ("I don't know" when entity was mentioned)

---

## 🚨 Rollback Plan

**If fix causes issues:**

1. Revert changes to `conversational_organism_wrapper.py`
2. Git diff to confirm clean revert
3. Run system maturity assessment to verify stability
4. Document issue encountered
5. Consider Option 2 or Option 3 as alternative

---

## 🔄 Alternative Approaches (If Option 1 Fails)

### Approach A: Pass entity_context via separate parameter

```python
# In organism.process_text() signature:
def process_text(
    self,
    text: str,
    context: Optional[Dict] = None,
    entity_context: Optional[str] = None,  # NEW
    ...
)
```

**Pros:** Explicit, hard to miss
**Cons:** API change, more invasive

### Approach B: Use global entity context store

```python
# Create singleton EntityContextManager
# Organism queries it when needed
```

**Pros:** No parameter passing needed
**Cons:** Global state, harder to test

### Approach C: Inject via organism initialization

```python
# Pass user profile to organism on init
# Organism loads entity context itself
```

**Pros:** Self-contained
**Cons:** Organism becomes stateful, complicates multi-user

---

## 📝 Code Change Summary

### Single File Modification

**File:** `persona_layer/conversational_organism_wrapper.py`

**Location:** Lines 822-841 (felt_state_for_reconstruction dict)

**Addition:**
```python
# Add these two lines before the closing brace:
'entity_context_string': context.get('entity_context_string'),
'memory_intent': context.get('memory_intent', False)
```

**That's it!** Two lines to fix the entire entity memory system.

---

## 🎯 Next Steps (Priority Order)

1. **IMMEDIATE:** Implement Option 1 (add to felt_state)
2. **VERIFY:** Run supervised_entity_memory_validator.py
3. **TEST:** Manual interactive session with entity memory
4. **VALIDATE:** Confirm entity_context flows through pipeline (debug logs)
5. **DOCUMENT:** Update Phase 1.8++ completion doc with fix
6. **TRAIN:** Run epoch training on entity memory scenarios (optional)
7. **DEPLOY:** Merge to main, update CLAUDE.md

---

## 🌀 Philosophical Note

This bug is a perfect example of **why entity-native, felt-based intelligence is powerful but requires careful plumbing**.

The organism correctly:
- Extracts username from context ✅
- Adds it to felt_state ✅
- Flows it to LLM ✅

But it didn't yet know about `entity_context_string` because that's a Phase 1.8++ addition!

**The fix:** Teach the organism to include entity context in its felt-state, just like it does with username.

Once that single connection is made, the entire entity memory system works end-to-end.

---

**Status:** READY TO IMPLEMENT
**Estimated Time:** 5 minutes to code, 10 minutes to test
**Risk:** Very low (single dict addition)
**Impact:** HIGH (fixes entire entity memory system)

🔧 **Let's fix this!**
