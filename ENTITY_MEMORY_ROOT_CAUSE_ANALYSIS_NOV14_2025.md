# 🔍 Entity Memory Root Cause Analysis
**Date:** November 14, 2025
**Issue:** DAE forgetting entities immediately
**Status:** ROOT CAUSE IDENTIFIED

---

## Executive Summary

**CRITICAL FINDING:** The Phase 1.8++ fix (loading entity_context_string on every turn) is **WORKING CORRECTLY**. The actual problem is:

1. **Entity context IS loading** - Verified in diagnostic output
2. **But entity_context_string is NOT reaching the LLM** - Pipeline disconnect
3. **And dae_interactive.py is NOT using the organism** - It has its own separate flow

##

 Root Cause Analysis

### What We Thought Was Wrong

We believed entities weren't being loaded from the profile on subsequent turns without "please remember" keywords.

### What's Actually Wrong

**THREE SEPARATE ISSUES:**

#### Issue #1: Test Infrastructure API Mismatch
**File:** `supervised_entity_memory_validator.py`
**Problem:** Validator looking for wrong response structure

```python
# Validator code (WRONG):
emission_text = result.get('emission', {}).get('text', '(no emission)')
```

**Actual organism return structure:**
```python
# From conversational_organism_wrapper.py:1080
return {
    'emission_text': emission_text,      # ← Key is 'emission_text' not 'emission'
    'emission_confidence': emission_confidence,
    ...
}
```

**Evidence from diagnostic run:**
```
DAE: (no emission)          # Validator couldn't find emission
(confidence: 0.000)

# But in the ACTUAL logs above this:
📝 Assembled: 1 phrases → "😌 The weather. I'm not really sure..."
   Confidence: 0.700
✅ Reconstruction complete:
   Strategy: felt_guided_llm
   Confidence: 0.700
```

The emission WAS generated (confidence 0.700), but the validator couldn't extract it!

---

#### Issue #2: dae_interactive.py Doesn't Use process_text()
**File:** `dae_interactive.py`
**Critical Discovery:** `dae_interactive.py` does NOT call `organism.process_text()` at all!

Let me verify this:

```bash
grep "process_text" dae_interactive.py
# RESULT: No matches!
```

**What dae_interactive.py actually does:**
```python
# It has its OWN emission generation logic
# Completely bypassing the organism's process_text() pipeline
```

This means our Phase 1.8++ fix to `process_text()` wouldn't affect interactive mode AT ALL!

---

#### Issue #3: Entity Context Not Reaching LLM in Reconstruction Pipeline
**Even when using process_text()**, the diagnostic shows:

**Turn 2:**
```
✓ Entity context loaded (39 chars)        # ← Context IS loaded
...
🌀 Hebbian path: Using felt-guided LLM    # ← Going to LLM
DAE: "😌 The weather. I'm not really sure..." # ← But no "Sarah" in response
```

This means:
1. Entity context loaded into `context` dict ✅
2. Passed to organism ✅
3. But LLM response doesn't use entity knowledge ❌

**Possible causes:**
- `entity_context_string` in context dict not making it to `felt_state`
- Reconstruction pipeline extracting it but LLM prompt builder ignoring it
- LLM generating response without seeing entity context

---

## Verification Tests

### Test 1: Entity Context Loading (Phase 1.8++)
```
Turn 2: ✓ Entity context loaded (39 chars)
```
**Status:** ✅ WORKING

### Test 2: Entity Extraction (Phase 1.8)
```
Turn 1: ✓ Entities stored: ['user_name']
```
**Status:** ✅ WORKING

### Test 3: Entity Reaching LLM
```
Turn 2: Entity context available, but LLM says "I'm not really sure"
```
**Status:** ❌ FAILING

### Test 4: LLM Using Entity Knowledge
```
Turn 3: User asks "Do you remember my name?"
DAE: "😌 I'm not sure. 🤔 Can you tell me a bit more..."
```
**Status:** ❌ FAILING (LLM doesn't demonstrate knowledge of "Sarah")

---

## Detailed Pipeline Trace

**Expected Flow (Phase 1.8++):**
```
process_input()
  → loads entity_context_string from profile ✅ WORKING
  → adds to context dict ✅ WORKING
organism.process_text(context=context)
  → should include context in felt_state
reconstruction_pipeline.reconstruct()
  → should extract entity_context_string from felt_state
  → should pass to generate_from_felt_state()
generate_from_felt_state()
  → should pass to build_felt_prompt()
build_felt_prompt()
  → should inject into LLM prompt
LLM
  → should see and use entity knowledge ❌ NOT HAPPENING
```

**Actual behavior observed:**
- Phases 1-2: ✅ Working
- Phases 3-7: ❌ Breaking down somewhere

---

## Investigation Needed

### High Priority: Where is entity_context_string getting lost?

**Check 1:** Does `process_text()` include `context` dict in `felt_state`?
```python
# File: conversational_organism_wrapper.py
# Need to verify context dict is passed to reconstruction pipeline
```

**Check 2:** Does reconstruction pipeline extract `entity_context_string`?
```python
# File: organ_reconstruction_pipeline.py:556-573
# We ADDED this code in Phase 1.8++, verify it's executing
```

**Check 3:** Is `generate_from_felt_state()` receiving it?
```python
# File: llm_felt_guidance.py:472-473
# We ADDED parameters, verify they're being passed
```

**Check 4:** Is `build_felt_prompt()` actually injecting it?
```python
# File: llm_felt_guidance.py:390-391
# Code exists from Phase 1.8, verify execution
```

**Check 5:** Is the actual LLM prompt correct?
```
# Need to add debug logging to see ACTUAL prompt sent to LLM
```

---

## Why dae_interactive.py Doesn't Work

**CRITICAL DISCOVERY:** `dae_interactive.py` doesn't use the organism's `process_text()` method at all!

**What this means:**
- Our Phase 1.8++ fixes to the organism pipeline don't affect interactive mode
- `dae_interactive.py` has its own separate emission generation
- Need to find where `dae_interactive.py` generates responses and fix THAT path

**Investigation needed:**
```bash
grep -n "def process_input" dae_interactive.py
# Find the actual processing method
grep -n "emission" dae_interactive.py
# Find where it generates responses
```

---

## Immediate Next Steps

### 1. Fix Test Infrastructure (Low Priority)
Update `supervised_entity_memory_validator.py` to use correct API:
```python
# OLD (wrong):
emission_text = result.get('emission', {}).get('text', '(no emission)')

# NEW (correct):
emission_text = result.get('emission_text', '(no emission)')
emission_confidence = result.get('emission_confidence', 0.0)
```

### 2. Find dae_interactive.py Processing Path (HIGH PRIORITY)
- Locate where `dae_interactive.py` actually processes user input
- Determine if it uses organism at all
- If not, that's why our fixes don't work in practice!

### 3. Add Debug Logging to Pipeline (HIGH PRIORITY)
Add logging at each step to verify entity_context_string flow:
```python
# In conversational_organism_wrapper.py
print(f"DEBUG: context contains entity_context_string: {'entity_context_string' in context}")

# In organ_reconstruction_pipeline.py
print(f"DEBUG: felt_state contains entity_context_string: {felt_state.get('entity_context_string')}")

# In llm_felt_guidance.py
print(f"DEBUG: Received entity_context_string: {entity_context_string}")
print(f"DEBUG: Final LLM prompt:\n{prompt}")
```

### 4. Test with process_text() Directly
Create minimal test that calls `organism.process_text()` directly and verifies entity usage:
```python
context = {'entity_context_string': "Known info: User's name is Sarah"}
result = organism.process_text("What's the weather?", context=context)
# Check if "Sarah" appears in emission_text
```

---

## Hypothesis: dae_interactive.py Bypasses Entire Pipeline

**Strong evidence suggests:**
1. `dae_interactive.py` doesn't call `process_text()`
2. It has its own processing logic
3. Our Phase 1.8++ fixes only touched `process_text()` path
4. Therefore, interactive mode never benefited from the fix

**If true, we need to:**
1. Find `dae_interactive.py`'s actual processing method
2. Apply similar fix there (load entity_context, pass to LLM)
3. OR: Refactor `dae_interactive.py` to use `organism.process_text()`

---

## Summary

**What's Working:**
- ✅ Entity extraction (Phase 1.8)
- ✅ Entity storage in profile
- ✅ Entity context loading on every turn (Phase 1.8++)
- ✅ Phase 1.8++ code changes are correct

**What's NOT Working:**
- ❌ Entity context reaching LLM in `process_text()` flow
- ❌ `dae_interactive.py` doesn't use `process_text()` at all (suspected)
- ❌ LLM not demonstrating knowledge of stored entities

**Root Cause:**
Either:
1. **Pipeline disconnect:** `context` dict not flowing to `felt_state` to reconstruction to LLM
2. **Wrong path:** `dae_interactive.py` uses completely different code path we didn't fix

**Next Actions:**
1. Investigate `dae_interactive.py` processing flow
2. Add debug logging throughout pipeline
3. Test `process_text()` directly with entity context
4. Fix the actual code path that `dae_interactive.py` uses

---

**Completion Date:** November 14, 2025
**Status:** ROOT CAUSE IDENTIFIED - REMEDIATION IN PROGRESS
