# DAE_HYPHAE_1 Training/Learning Infrastructure Audit
**Date:** November 16, 2025  
**Status:** CRITICAL ISSUES FOUND - 8 Dormant/Broken Features  
**Priority:** HIGH - These block multi-family emergence and signal health monitoring  

---

## Executive Summary

The codebase has 65D signature infrastructure and 11 learning components, but **several critical features are broken or dormant**, preventing full realization of the recent breakthroughs:

✅ **Working:**
- 65D Euclidean distance clustering (multi-family emergence operational)
- Phase 5 learning integration (learn_from_conversation_transformation working)
- Organ confidence tracker (Level 2 - initialized and updating)
- Family discovery (3 families emerged from 30 pairs)
- Training corpus (CORE-grounded data created)

❌ **Broken/Dormant:**
1. **FAO Organ Agreement Metrics** - Computed but not being extracted to signatures
2. **Conversational Cluster Learning** - Created but never called/updated
3. **Signal Health Monitor** - Created but not integrated into orchestrator
4. **Family V0 Learning** - Implemented but not called in the main flow
5. **Hebbian R-Matrix Learning** - References exist but updates not happening
6. **Organ Confidence Std** - All organs stuck at 0.0 std (not differentiating)
7. **TSK Recording** - Implementation exists but extraction may be incomplete
8. **Per-Family FAO Tracking** - FAO dims computed but not analyzed per-family

---

## PRIORITY 1: Critical Blockers

### Issue #1: FAO Dimensions Not Being Extracted to Signatures
**File:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/organ_signature_extractor.py`  
**Lines:** 1430-1452  
**Severity:** HIGH  

**Problem:**
```python
if OrganAgreementComputer is not None and final_organs:
    agreement_computer = OrganAgreementComputer()
    agreement_state = agreement_computer.compute_full_agreement_state(final_organs)
    # FAO dimensions [57-64] ARE being set HERE
    signature_65d[57] = agreement_state.pairwise_agreement
    signature_65d[58] = agreement_state.organ_entropy
    # ... etc
else:
    # FALLBACK: Sets FAO dims to 0.5 (neutral) - loses all agreement information!
    signature_65d[57:65] = 0.5
```

**Root Cause:**
- `OrganAgreementComputer` is imported but falls back to neutral (0.5) when not available
- Check if `final_organs` is being populated correctly from the emission pipeline

**Impact:**
- FAO dimensions are supposed to be the DISCRIMINATORS for multi-family emergence
- But they're being set to neutral 0.5 unless OrganAgreementComputer succeeds
- This removes critical separation signal between crisis/safety/ambivalence families

**Fix Required:**
1. Verify `OrganAgreementComputer` is actually computing agreement states
2. Debug why fallback is being triggered (check `final_organs` population)
3. Test that agreement dimensions are non-trivial (not all 0.5)

---

### Issue #2: Organ Confidence Std = 0.0 (No Differentiation)
**File:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/organ_confidence_tracker.py`  
**Lines:** 193-212  
**Severity:** CRITICAL  

**Problem:**
```
Current state (from organ_confidence.json):
  All organs: confidence=1.0, success_rate=1.0
  std_confidence: 0.0 (all organs identical!)
```

**Root Cause:**
- Every organ is getting confidence=1.0 (maximum boost)
- This suggests ALL organs are being marked as "successful"
- Organ participation detection may be too permissive OR emissions are universally successful

**Code Issue in line 126-130:**
```python
def _organ_participated(self, organ_result) -> bool:
    """Check if organ actively participated in emission."""
    # ... checks for atom_activations or pattern
    # DEFAULT: return True  # ⚠️ PROBLEM: Assumes participation if result exists!
    return True
```

Every organ result→marked as participated, every emit→marked successful = all 1.0 confidence!

**Fix Required:**
1. Fix `_organ_participated()` to be more selective (currently too permissive)
2. Check if emissions are failing silently but still counting as "successful" 
3. Verify satisfaction threshold is being applied correctly

**Expected After Fix:**
- Organ std should be 0.15-0.20 (DAE 3.0 target)
- Top organs (EMPATHY, WISDOM) should be 0.65-0.75
- Bottom organs (SANS, RNX) should be 0.25-0.35

---

### Issue #3: Conversational Cluster Learning Never Updated
**File:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/phase5_learning_integration.py`  
**Lines:** 242-243  
**Severity:** HIGH  

**Problem:**
```python
def learn_from_conversation_transformation(...):
    # ... extract signature and assign to family
    
    # STEP 3: Update Cluster Learning (DORMANT!)
    # For transformation approach, we track transformation characteristics
    transformation_metrics = {
        'v0_descent': ...,
        'satisfaction_improvement': ...,
        # ... etc
    }
    
    # NOTE: cluster_learning expects organ_results dict, but for transformation
    # approach we'll need to adapt this. For now, skip cluster learning update
    # and focus on family assignment (the critical part for DAE 3.0 replication)
```

**Root Cause:**
- Line 241-243 explicitly SKIPS cluster learning
- `self.cluster_learning.update_from_conversation()` is never called for transformation signatures
- This means organ weights per family are NOT being learned

**Fix Required:**
1. Implement `update_from_conversation()` call for transformation signatures
2. Track organ_weights per family from 65D signatures
3. Feed transformation_metrics to cluster learning

---

## PRIORITY 2: Broken Integrations

### Issue #4: Signal Health Monitor Created But Never Called
**File:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/training/signal_health_monitor.py`  
**Integration Point:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/training/epoch_learning_orchestrator.py`  
**Lines:** 32, 126 (initialized), but never used in training loop  
**Severity:** MEDIUM  

**Problem:**
```python
# epoch_learning_orchestrator.py line 126:
self.signal_monitor = SignalHealthMonitor()

# BUT: Never called in _run_epoch() or anywhere!
# Training loop ignores signal health entirely
```

**Expected Usage:**
```python
# Should be called after each epoch
health = self.signal_monitor.compute_epoch_health(
    families=self.phase5_learner.families.families,
    organ_confidences=self._get_organ_confidences()
)
self.signal_health_history.append(health)

# Should warn if organ_confidence_std < 0.05 (low differentiation)
if health['organ_confidence_std'] < 0.05:
    print(f"⚠️  WARNING: Organs not differentiating!")
```

**Fix Required:**
1. Add signal health computation to `_run_epoch()`
2. Track health metrics in `signal_health_history`
3. Add warnings when FAO agreement or multiplicity are out of range

---

### Issue #5: Family V0 Learner Not Integrated
**File:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/family_v0_learner.py`  
**Where It Should Be Called:** `epoch_learning_orchestrator.py` line 393-410  
**Severity:** MEDIUM  

**Problem:**
```python
# family_v0_learner.py exists and is complete BUT:
# Never imported or initialized in epoch_learning_orchestrator
# Never called with update_family_v0() after each conversation
```

**What It Does (If Integrated):**
```python
# Should learn per-family V0 targets
learner.update_family_v0(
    family_id=learning_report['family_id'],
    v0_final=result['felt_states']['v0_energy']['final_energy'],
    satisfaction=user_satisfaction,
    convergence_cycles=result['felt_states']['v0_energy']['cycles'],
    organ_coherences=result['organ_results'],  # For organ weight learning
    r_matrix_coupling=0.05  # From conversational_hebbian_memory
)
```

**Fix Required:**
1. Import FamilyV0Learner in epoch_learning_orchestrator
2. Initialize in `_initialize_system()`
3. Call `update_family_v0()` after each learning report in training loop
4. Save family V0 states at end of epoch

---

### Issue #6: Hebbian R-Matrix Learning Not Being Called
**File:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/conversational_hebbian_memory.py`  
**Where Missing:** `epoch_learning_orchestrator.py`, `conversational_organism_wrapper.py`  
**Severity:** MEDIUM  

**Problem:**
```python
# conversational_hebbian_memory.py is complete with:
# - Outcome-gated learning (η=0.01)
# - 4×4 detector coupling matrix
# - Pattern memory storage
# BUT: Never initialized or called in training loop!

# Only reference is in conversational_organism_wrapper.py:
#   r_matrix_path="persona_layer/state/active/conversational_hebbian_memory.json"
# But actual updates to this file don't happen in epoch learning
```

**Root Cause:**
- Hebbian memory is used for READING (in nexus composer)
- But never updated with ConversationalHebbianMemory.update() calls

**Fix Required:**
1. Initialize ConversationalHebbianMemory in epoch_learning_orchestrator
2. After each conversation, call hebbian_memory.update_from_outcome()
3. Save hebbian memory state at end of epoch

---

## PRIORITY 3: Incomplete Implementations

### Issue #7: TSK Recording May Be Incomplete
**File:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/training/epoch_learning_orchestrator.py`  
**Lines:** 347-410 (felt-state extraction)  
**Severity:** MEDIUM  

**Problem:**
```python
# Building initial_felt_state from defaults:
initial_felt_state = {
    'v0_initial': 1.0,  # HARDCODED!
    'satisfaction': 0.5,  # HARDCODED!
    'zone': 1,  # DEFAULT
    'organ_coherences': {},  # EMPTY!
}

# These should be extracted from:
# 1. Previous turn's result (if exists)
# 2. Or organism's current polyvagal/SELF-energy state
```

**Fix Required:**
1. Extract initial_felt_state from organism.get_state() if available
2. Populate organ_coherences from last turn's results
3. Use actual satisfaction from user rating, not default 0.5
4. Track actual V0 initial value from organism state

---

### Issue #8: Per-Family FAO Tracking Dormant
**File:** `/Users/daedalea/Desktop/DAE_HYPHAE_1/training/signal_health_monitor.py`  
**Lines:** 159-192  
**Severity:** LOW  

**Problem:**
```python
def _extract_agreement_metrics(self, families: Dict) -> Dict:
    """Extract organ agreement metrics from family centroids."""
    # Correctly extracts FAO dimensions from 65D centroids
    # BUT: This data is computed but never used for diagnosis
    
    for family in families.values():
        centroid = family.centroid
        if len(centroid) >= 65:
            pairwise_agreements.append(centroid[57])  # ✅ Extracted
            # ... etc
    
    # Returns mean agreement, entropy, etc.
    # But epoch_learning_orchestrator never calls this!
```

**Fix Required:**
1. Use this method in signal_health_monitor.compute_epoch_health()
2. Track per-family FAO trends across epochs
3. Alert if any family has low agreement (organs not coordinating)

---

## Summary of Fixes Required

| Priority | Issue | File | Line | Type | Impact |
|----------|-------|------|------|------|--------|
| 1 | FAO dims not extracted | organ_signature_extractor.py | 1430 | Missing fallback logic | Loss of agreement discrimination |
| 1 | Organ conf std = 0.0 | organ_confidence_tracker.py | 126 | Overly permissive participation check | No organ differentiation |
| 1 | Cluster learning dormant | phase5_learning_integration.py | 241 | Skipped in code | No per-family organ weights |
| 2 | Signal health not called | epoch_learning_orchestrator.py | 126 | Init but no usage | No system health monitoring |
| 2 | FamilyV0Learner dormant | family_v0_learner.py | whole | Not integrated | No per-family V0 targets |
| 2 | Hebbian R-matrix dormant | conversational_hebbian_memory.py | whole | Not called in training | No learned pattern memory |
| 3 | TSK extraction incomplete | epoch_learning_orchestrator.py | 347 | Hardcoded defaults | Poor learning signal |
| 3 | Per-family FAO tracking | signal_health_monitor.py | 159 | Computed but unused | No per-family diagnostics |

---

## Recommendations

### Immediate (Session This)
1. Fix organ confidence std issue (#2) - should see organs differentiate after 10 turns
2. Enable FAO dimension extraction (#1) - verify OrganAgreementComputer is called
3. Activate cluster learning updates (#3) - call update_from_conversation() in Phase 5

### Short Term (Next Session)
4. Integrate signal health monitoring (#4) - add to epoch reporting
5. Connect FamilyV0Learner (#5) - minimal integration (5 lines)
6. Activate Hebbian memory updates (#6) - already built, just needs calling

### Medium Term
7. Fix TSK extraction (#7) - better initial state capture
8. Add per-family FAO diagnostics (#8) - leverage existing computation

### Expected Outcomes After All Fixes
- Organ confidence std: 0.0 → 0.15-0.20 (organs differentiate!)
- Family separation: Better FAO-guided clustering
- Signal health: Track coherence, agreement, entropy across epochs
- V0 learning: Each family learns optimal convergence point
- Hebbian patterns: Learn which polyvagal→response sequences work best
- Overall: Multi-family emergence with clear therapeutic patterns per family

