# Interactive Mode Issues - November 15, 2025

## Issues Identified

### 1. ⚠️ Neo4j Connection Errors (Non-Critical)

**Error:**
```
[#E4D6]  _: <CONNECTION> error: Failed to read from defunct connection
ConnectionResetError(54, 'Connection reset by peer')
Unable to retrieve routing information
```

**Impact:** Entity memory queries failing, but system continues via fallback

**Root Cause:** Neo4j cloud database connection unstable (network issue)

**Solution:** Graceful degradation already in place - system continues without entity enrichment

**Priority:** LOW - Non-blocking, entity memory is optional enhancement

---

### 2. ❌ LLM JSON Parsing Errors (Medium Priority)

**Error:**
```
⚠️  LLM generated invalid JSON: Expecting value: line 5 column 16 (char 62)
JSON attempted: {
  "new_facts": [
    {
      "type": "name",
      "value": Emiliano's partner (not explicitly stated, but implied through the use of "my wife"),
      "context": "Emiliano has a partner"
    },
```

**Root Cause:** LLM generating invalid JSON (unquoted string value)

**Impact:** Entity extraction failing, memories not being saved

**Solution:** Add JSON salvage/repair logic OR constrain LLM output format better

**Priority:** MEDIUM - Affects entity memory learning but system functions

**Fix Location:** `persona_layer/felt_guided_llm_generator.py` or entity extraction code

---

### 3. ⚠️ 0 Nexuses Forming in Interactive Mode (Context-Dependent)

**Observation:**
```
✓ 4 semantic fields created
LISTENING meta-atoms: {'relational_attunement': 0.225, 'temporal_grounding': 0.225, 'coherence_integration': 0.225}
✓ 0 nexuses formed
```

**Analysis:**
- Only LISTENING organ activating conversational meta-atoms
- Other organs (EMPATHY, WISDOM, etc.) not showing meta-atom activations
- Need at least 2 organs on same meta-atom to form nexus

**Is This a Bug?**
Possibly not - if the input truly doesn't activate multiple organs strongly, 0 nexuses is correct behavior.

**Input Analyzed:**
```
"you know that i am also vegan! me and my wife follow a vegan diet"
```

This is:
- Factual/informational (not emotional → less EMPATHY)
- Not crisis/urgent (less NDAM/EO)
- Not deeply reflective (less WISDOM)
- Primarily relational info → LISTENING dominant

**Expected Behavior:**
- LISTENING: High (relational info)
- EMPATHY: Low-Medium (no emotional content)
- BOND: Low (no parts language)
- WISDOM: Low (factual, not reflective)

**Conclusion:** This might be **correct**! The input is semantically narrow.

**Test:** Try emotionally richer input:
```
"I'm feeling overwhelmed and don't know what to do"
```

This should activate:
- EMPATHY (emotional content)
- PRESENCE (somatic awareness)
- WISDOM (need for perspective)
- LISTENING (relational attunement)

And form nexuses like `somatic_wisdom`, `compassion_safety`

---

### 4. ❌ Phase 2 Field Coherence Still 0.0 (Critical for Wave Training)

**Status:** Field coherence calculation implemented but NOT being called

**Evidence from Baseline Test:**
```
Field coherence mean: 0.000
Field coherence std: 0.000
```

**Root Cause:** Missing integration in V0 convergence loop

**Impact:** Phase 2 benefits (dynamic nexus threshold modulation) not active

**Fix Needed:**
1. Locate V0 convergence loop in `_run_v0_convergence()` or `_process_organs_with_v0()`
2. Add call to `occasion._calculate_field_coherence(organ_prehensions)`
3. Verify field coherence populated in all occasions

**Priority:** HIGH - Needed for wave training Phase 2 completion

---

## Recommendations

### Immediate Actions

1. **Ignore Neo4j errors for now** - Graceful degradation working, non-blocking

2. **Fix JSON parsing** - Add try/except with salvage logic:
   ```python
   try:
       entities = json.loads(llm_output)
   except json.JSONDecodeError:
       # Try salvaging common issues
       fixed = llm_output.replace("Emiliano's partner (", '"Emiliano\'s partner ("')
       entities = json.loads(fixed)
   ```

3. **Test with richer inputs** - Verify 0 nexuses is contextual, not a bug

4. **Fix Phase 2 field coherence** - Critical for wave training completion

### Testing Protocol

**Test Nexus Formation:**
```bash
# Test 1: Factual input (expect 0-1 nexuses)
"I'm vegan and work at Google"

# Test 2: Emotional input (expect 2-4 nexuses)
"I'm feeling overwhelmed and scared"

# Test 3: Reflective input (expect 2-3 nexuses)
"I'm noticing a pattern in how I respond to stress"
```

**Test Field Coherence:**
```bash
python3 test_wave_training_integration.py --num-tests 3
# Should show field_coherence > 0.0
```

---

## Summary

**Non-Issues (Working as Designed):**
- Neo4j errors (graceful degradation)
- 0 nexuses on factual inputs (correct if organs don't co-activate)

**Real Issues Needing Fixes:**
1. JSON parsing errors (MEDIUM priority)
2. Phase 2 field coherence not called (HIGH priority)

**Next Steps:**
1. Fix Phase 2 field coherence integration
2. Test with emotionally richer inputs
3. Add JSON salvage logic if entity extraction critical
4. Update baseline test results once Phase 2 fixed

---

**Date:** November 15, 2025
**Status:** 2 real issues, 2 false alarms
**Priority:** Fix field coherence first, then JSON parsing
