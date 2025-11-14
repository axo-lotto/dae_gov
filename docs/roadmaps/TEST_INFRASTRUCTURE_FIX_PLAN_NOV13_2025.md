# Test Infrastructure Fix Plan - Phase A1
**Date:** November 13, 2025
**Status:** 🔧 IN PROGRESS
**Priority:** CRITICAL (blocks all validation)

---

## 🔍 Root Cause Analysis

### **Primary Issue: Attribute Name Mismatch**

**What tests expect:**
```python
organ_result.satisfaction  # ❌ DOESN'T EXIST
```

**What organs actually have:**
```python
organ_result.coherence  # ✅ EXISTS (Whiteheadian process philosophy)
organ_result.lure  # ✅ EXISTS (attractors for concrescence)
```

**Why this happened:**
- Tests were written assuming `.satisfaction` attribute
- Organs implement Whiteheadian process philosophy (coherence + lure)
- "Satisfaction" is the FINAL state after convergence, not per-organ

### **Secondary Issues:**

1. **Emission key mismatch:**
   - Tests look for: `result['emission']`
   - Actual key: `result['emission_text']`

2. **Strategy key mismatch:**
   - Tests look for: `felt_states['emission_strategy']`
   - Actual key: `result['emission_path']`

3. **Nexus location:**
   - Tests look for: `felt_states['nexuses']`
   - Often empty, need to check semantic_fields

4. **Result structure:**
   - `organ_results` is a dict (correct)
   - Organ results are dataclass objects (correct)
   - Just need to access `.coherence` not `.satisfaction`

---

## 🎯 Fix Strategy

### **Universal Pattern to Replace:**

**OLD (broken):**
```python
# In all intelligence/continuity tests
satisfaction = organ_result.get('satisfaction', 0.0)  # ❌ Treats as dict
```

**NEW (working):**
```python
# Correct access pattern
if organ_result and hasattr(organ_result, 'coherence'):
    coherence = organ_result.coherence  # ✅ Access as object attribute
else:
    coherence = 0.0
```

**Even better (using coherence as primary metric):**
```python
# Access coherence directly (philosophically correct)
organ_coherence = {
    organ_name: organ_results.get(organ_name).coherence
    if organ_results.get(organ_name) else 0.0
    for organ_name in ['LISTENING', 'EMPATHY', ...]
}
```

---

## 📋 Files to Fix (Priority Order)

### **Intelligence Tests (5 files)**

#### 1. `test_abstraction_reasoning.py` (CRITICAL)
**Lines to fix:** 214-217 (already fixed), but check vector extraction methods

**Fix:**
```python
# _extract_organ_vector() method
def _extract_organ_vector(self, result: Dict) -> np.ndarray:
    organ_results = result.get('organ_results', {})
    vector = []
    for organ_name in self.ORGAN_ORDER:
        organ_result = organ_results.get(organ_name)
        if organ_result and hasattr(organ_result, 'coherence'):
            vector.append(organ_result.coherence)
        else:
            vector.append(0.0)
    return np.array(vector)
```

#### 2. `test_pattern_transfer.py`
**Same fix:** Update organ vector extraction

#### 3. `test_novelty_handling.py`
**Additional fix:** Strategy detection
```python
# OLD:
strategy = felt_states.get('emission_strategy')  # ❌ Returns None

# NEW:
strategy = result.get('emission_path', 'unknown')  # ✅ Correct key
```

**Additional fix:** Active organ count
```python
# Count organs with coherence > threshold
organs_active = sum(
    1 for organ_name in self.ORGAN_ORDER
    if organ_results.get(organ_name) and
       hasattr(organ_results.get(organ_name), 'coherence') and
       organ_results.get(organ_name).coherence > 0.01
)
```

#### 4. `test_context_integration.py`
**Fix:** Multi-turn state tracking (store organ coherences between turns)

#### 5. `test_meta_learning.py`
**Fix:** Confidence extraction from correct location

---

### **Continuity Tests (4 files)**

#### 6. `test_v0_target_persistence.py`
**Fix:** Family V0 target access (already correct path, just verify)

#### 7. `test_emission_consistency.py`
**Fix:** Strategy extraction
```python
# OLD:
strategy = felt_states.get('emission_strategy')  # ❌

# NEW:
strategy = result.get('emission_path', 'unknown')  # ✅
```

#### 8. `test_semantic_atom_drift.py`
**Fix:** Atom extraction from semantic_fields (verify path)

#### 9. `test_meta_atom_activation.py`
**Fix:** Meta-atom extraction from semantic_fields

---

### **Responsiveness Tests (2 files - mostly OK)**

#### 10. `test_latency_measurement.py`
**Status:** ✅ PASSED (doesn't use organ satisfaction)

#### 11. `test_comprehensive_responsiveness.py`
**Check:** Resource monitoring might reference organs

---

### **Superject Test (1 file)**

#### 12. `test_xyz_cycle_validation.py`
**Fix:** Multiple issues:
1. Organ participation count (use coherence)
2. R-matrix access (capital R verified)
3. Family access (nested dict verified)

---

## 🔧 Implementation Plan

### **Step 1: Create Universal Utility Functions** (30 min)

Create `tests/test_utils.py`:
```python
\"\"\"
Universal test utilities for correct result extraction.
\"\"\"
import numpy as np
from typing import Dict, List

ORGAN_ORDER = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
               'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']

def extract_organ_coherences(result: Dict) -> Dict[str, float]:
    \"\"\"Extract organ coherences from organism result.\"\"\"
    organ_results = result.get('organ_results', {})
    coherences = {}
    for organ_name in ORGAN_ORDER:
        organ_result = organ_results.get(organ_name)
        if organ_result and hasattr(organ_result, 'coherence'):
            coherences[organ_name] = organ_result.coherence
        else:
            coherences[organ_name] = 0.0
    return coherences

def extract_organ_vector(result: Dict) -> np.ndarray:
    \"\"\"Extract organ coherences as 11D vector.\"\"\"
    coherences = extract_organ_coherences(result)
    return np.array([coherences[organ] for organ in ORGAN_ORDER])

def count_active_organs(result: Dict, threshold: float = 0.01) -> int:
    \"\"\"Count organs with coherence above threshold.\"\"\"
    coherences = extract_organ_coherences(result)
    return sum(1 for c in coherences.values() if c > threshold)

def extract_emission_strategy(result: Dict) -> str:
    \"\"\"Extract emission strategy from result.\"\"\"
    return result.get('emission_path', 'unknown')

def extract_emission_text(result: Dict) -> str:
    \"\"\"Extract emission text from result.\"\"\"
    return result.get('emission_text', '')

def extract_emission_confidence(result: Dict) -> float:
    \"\"\"Extract emission confidence.\"\"\"
    return result.get('emission_confidence', 0.0)
```

### **Step 2: Update Intelligence Tests** (60-90 min)

For each test file:
1. Import test_utils
2. Replace all organ extraction with utility functions
3. Replace `satisfaction` with `coherence`
4. Fix strategy/emission key access
5. Test locally

### **Step 3: Update Continuity Tests** (60-90 min)

Similar pattern, focus on:
- V0 target access (verify correct)
- Emission strategy (fix key)
- Atom/meta-atom extraction (verify paths)

### **Step 4: Update Superject Test** (30 min)

Fix organ participation counting and R-matrix access.

### **Step 5: Re-run Comprehensive Validation** (10 min)

Run full suite, expect ~50-75% pass rate (tests fixed, organs still partially dormant).

---

## ✅ Success Criteria

**After Phase A1 (test fixes):**
- All tests can extract data (no more 0.00 values everywhere)
- Tests fail with REAL metrics (e.g., "coherence 0.45 < 0.70" not "0.00 < 0.70")
- Pass rate: 30-50% (tests work, but organs still have issues)

**After Phase A2-A5 (organ redesign + training):**
- Tests pass with improved metrics
- Pass rate: 70-85% (tests + organs both working)

---

## 📊 Expected Validation Results After Fix

### **Before Fix (Current):**
```
INTEL-001: ❌ Organ inconsistency: 0.00 < 0.70 (CAN'T EXTRACT DATA)
INTEL-002: ❌ Low transfer: 0.00 < 0.60 (CAN'T EXTRACT DATA)
```

### **After Phase A1 Fix:**
```
INTEL-001: ❌ Organ inconsistency: 0.45 < 0.70 (LOW BUT EXTRACTING)
INTEL-002: ❌ Low transfer: 0.52 < 0.60 (CLOSE TO PASSING)
INTEL-003: ⚠️  Overspecialized: 5 organs active (BETTER)
RESP-001: ✅ Latency acceptable (ALREADY PASSING)
```

### **After Phase A2 Fix (Lure Redesign):**
```
INTEL-001: ✅ Abstraction working (0.72 coherence correlation)
INTEL-002: ✅ Pattern transfer working (0.65 similarity)
INTEL-003: ✅ Novelty handling appropriate (8 organs active)
CONT-006: ✅ Meta-atoms activating contextually (75% accuracy)
```

---

## 🚀 Next Steps

1. **Create test_utils.py** (30 min)
2. **Fix intelligence tests** (90 min)
3. **Fix continuity tests** (90 min)
4. **Fix superject test** (30 min)
5. **Re-run validation** (10 min)
6. **Document results** (10 min)

**Total Phase A1 time:** ~4 hours (slightly more than estimated 2-3h due to comprehensive utility creation)

---

**Status:** Ready to implement
**Next:** Create test_utils.py with universal extraction functions
