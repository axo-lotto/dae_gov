# Wave Training Integration Proposal for DAE_HYPHAE_1
**Date:** November 15, 2025
**Objective:** Fix 0 nexuses + flat satisfaction by integrating DAE 3.0 wave training
**Based on:** DAE 3.0 AXO ARC wave training success (Oct 30 - Nov 1, 2025)

---

## 🎯 Problem Statement

### Current Issues in DAE_HYPHAE_1

1. **0 Nexuses Forming** (Critical)
   - User report: "🔗 Nexuses: 0" across multiple turns
   - Without nexuses, no nexus-based emissions possible
   - Forces 70-80% LLM dependency

2. **Flat Satisfaction** (Critical)
   - All cycles converge to same satisfaction value
   - No variance = no kairos detection
   - No temporal learning signal

3. **Weak Organ Differentiation**
   - Mean organ confidence: 0.672
   - Organs not specializing effectively
   - R-matrix previously saturated (fixed, but symptoms remain)

### Root Cause Analysis

**From DAE 3.0 Experience:**
- Flat satisfaction blocked kairos variance gate
- Without variance, temporal learning couldn't engage
- Wave training created variance → unlocked kairos → enabled specialization

**DAE_HYPHAE_1 Symptoms Match DAE 3.0 Pre-Wave-Training:**
```
DAE 3.0 Before:
- Cycle 1: 0.580
- Cycle 2: 0.580
- Cycle 3: 0.580
- Variance: 0.000 ❌

DAE_HYPHAE_1 Current:
- Multiple turns: confidence=0.70, 0 nexuses
- Likely flat satisfaction trajectory
- No kairos moments detected
```

---

## 🌊 Wave Training Overview (from DAE 3.0)

### What Wave Training Does

**Purpose:** Modulate satisfaction during V0 convergence to create temporal variance

**3-Phase Appetitive Cycle:**

1. **EXPANSIVE_PERTURBATION** (Cycles 1-3)
   - Satisfaction × 0.95 (reduce by 5%)
   - Encourages exploration
   - "Let's keep searching"

2. **FELT_GRADIENT_NAVIGATION** (Middle cycles)
   - Satisfaction × 1.00 (neutral)
   - Tracks gradient toward peak
   - "Following the pull"

3. **CONCRESCENCE_COMPLETION** (Final cycles)
   - Satisfaction × 1.05 (boost by 5%)
   - Rewards completion
   - "This feels right"

### Evidence of Success (DAE 3.0)

**Before Wave Training:**
```
Variance: 0.000 (flat)
Kairos detection: 100% (always triggered - meaningless)
Organ specialization: Weak
```

**After Wave Training:**
```
Variance: 0.011 std dev (range 0.462-0.493)
Kairos detection: 80-90% (discriminative)
Organ specialization: Strong (std dev 0.15-0.20)
Accuracy: Stable (62.0%)
```

---

## 📋 Integration Strategy for DAE_HYPHAE_1

### Phase 1: Direct Port (Week 1 - Immediate)

**Goal:** Implement core wave training in conversational_occasion.py

**Files to Modify:**

**1. `persona_layer/conversational_occasion.py`**

Add wave training modulation to V0 descent:

```python
# After line ~150 (where satisfaction is computed)
def _apply_wave_training_modulation(
    self,
    satisfaction: float,
    cycle: int
) -> float:
    """
    Apply temporal variance modulation (DAE 3.0 wave training).

    Creates satisfaction variance across cycles for:
    - Kairos variance gate
    - Temporal learning signal
    - Organic convergence patterns
    """
    if not Config.ENABLE_WAVE_TRAINING:
        return satisfaction

    # Determine appetitive phase
    phase = self._determine_appetitive_phase(
        satisfaction=satisfaction,
        cycle=cycle,
        min_cycles=Config.V0_MIN_CYCLES,
        max_cycles=Config.V0_MAX_CYCLES
    )

    # Apply phase-specific modulation
    if phase == 'EXPANSIVE':
        modulation = -0.05  # Reduce by 5%
    elif phase == 'NAVIGATION':
        modulation = 0.00   # Neutral
    elif phase == 'CONCRESCENCE':
        modulation = +0.05  # Boost by 5%
    else:
        modulation = 0.00

    modulated = satisfaction * (1.0 + modulation)

    # Clamp to valid range
    modulated = max(0.0, min(1.0, modulated))

    if Config.DEBUG_WAVE_TRAINING:
        print(f"   Wave Training: Cycle {cycle}, Phase: {phase}")
        print(f"      Before: {satisfaction:.3f}, Adjustment: {modulation:+.3f}, After: {modulated:.3f}")

    return modulated

def _determine_appetitive_phase(
    self,
    satisfaction: float,
    cycle: int,
    min_cycles: int,
    max_cycles: int
) -> str:
    """
    Determine which appetitive phase the organism is in.

    Phases (Whiteheadian):
    - EXPANSIVE: Early exploration, low satisfaction
    - NAVIGATION: Mid-process, feeling gradient
    - CONCRESCENCE: Completion, high satisfaction
    """
    # EXPANSIVE: Low satisfaction OR early cycles
    if satisfaction < 0.55 and cycle <= min_cycles:
        return 'EXPANSIVE'

    # CONCRESCENCE: High satisfaction OR late cycles
    elif satisfaction >= 0.70 or cycle >= max_cycles - 2:
        return 'CONCRESCENCE'

    # NAVIGATION: Middle range
    else:
        return 'NAVIGATION'
```

**Integration Point:**
```python
# In _process_single_cycle() around line 180
satisfaction = self._calculate_satisfaction(...)

# 🌊 Apply wave training modulation
satisfaction = self._apply_wave_training_modulation(
    satisfaction=satisfaction,
    cycle=current_cycle
)

# Store modulated satisfaction
cycle_result['satisfaction'] = satisfaction
```

**2. `config.py`**

Add wave training parameters:

```python
# Wave Training (DAE 3.0 Legacy Integration - Nov 15, 2025)
ENABLE_WAVE_TRAINING = True
DEBUG_WAVE_TRAINING = False  # Set True for console output
WAVE_TRAINING_EXPANSIVE_MOD = -0.05  # -5% in early cycles
WAVE_TRAINING_NAVIGATION_MOD = 0.00  # Neutral in middle
WAVE_TRAINING_CONCRESCENCE_MOD = +0.05  # +5% in final cycles
```

**Expected Impact (Phase 1):**
- ✅ Satisfaction variance created (0.000 → 0.010+)
- ✅ Kairos detection becomes discriminative
- ✅ Temporal learning signal enabled
- ⚠️ May not immediately fix "0 nexuses" (needs Phase 2)

---

### Phase 2: Multi-Organ Prehensive Fields (Week 2-3)

**Goal:** Improve nexus formation through organ field interaction

**Problem:** Nexuses form from organ co-activation, but may need stronger prehensive fields

**Inspired by DAE 3.0 Architecture:**

From `WAVE_TRAINING_FINAL_SUMMARY`:
> "Creates temporal variance as designed... Unlocks kairos variance gate... Enables temporal learning"

**Key Insight:** Wave training doesn't just modulate satisfaction - it creates **dynamic prehensive fields** that organs can sense and respond to.

**Implementation:**

**File:** `persona_layer/conversational_occasion.py`

Add field coherence tracking:

```python
def _calculate_field_coherence(
    self,
    organ_results: Dict,
    cycle: int
) -> float:
    """
    Calculate cross-organ field coherence.

    Measures how well organs are "listening" to each other's
    prehensive fields (not just activating independently).

    Returns:
        Coherence score [0.0, 1.0]
    """
    if len(organ_results) < 2:
        return 0.0

    # Get organ activations
    activations = {}
    for organ_name, result in organ_results.items():
        if hasattr(result, 'coherence'):
            activations[organ_name] = result.coherence

    if len(activations) < 2:
        return 0.0

    # Calculate pairwise correlations
    # (organs with similar activation patterns = high coherence)
    from itertools import combinations
    correlations = []

    for org1, org2 in combinations(activations.keys(), 2):
        val1 = activations[org1]
        val2 = activations[org2]

        # Simple correlation: 1 - abs(val1 - val2)
        correlation = 1.0 - abs(val1 - val2)
        correlations.append(correlation)

    if not correlations:
        return 0.0

    # Mean correlation = field coherence
    field_coherence = sum(correlations) / len(correlations)

    return field_coherence

# Use in V0 descent:
field_coherence = self._calculate_field_coherence(organ_results, cycle)

# Store in cycle metadata
cycle_result['field_coherence'] = field_coherence

# Use for nexus formation threshold
# Higher field coherence = easier nexus formation
nexus_threshold_adjusted = Config.NEXUS_FORMATION_THRESHOLD * (1.0 - field_coherence * 0.3)
```

**Expected Impact (Phase 2):**
- ✅ Stronger organ co-activation patterns
- ✅ More nexuses forming
- ✅ Better organ specialization
- ✅ Reduced LLM dependency (more organic emissions)

---

### Phase 3: TSK Metadata Capture (Week 4)

**Goal:** Ensure wave training metadata persists for learning

**From `WAVE_TRAINING_TSK_METADATA_FIX_NOV01_2025.md`:**
> "Wave training metadata was computed but never stored to TSK"

**Implementation:**

**File:** `persona_layer/conversational_organism_wrapper.py`

Enhance TSK recording:

```python
# In process_text() around line 750 (after V0 convergence)
if enable_tsk_recording:
    tsk_metadata = {
        'wave_training': {
            'enabled': Config.ENABLE_WAVE_TRAINING,
            'phases': [],  # Populated below
            'field_coherence': [],
            'modulations': []
        }
    }

    # Extract from V0 cycles
    for cycle_idx, cycle in enumerate(result.get('v0_cycles', [])):
        phase_data = {
            'cycle': cycle_idx,
            'phase': cycle.get('appetitive_phase', 'unknown'),
            'satisfaction_pre': cycle.get('satisfaction_pre_modulation', 0.0),
            'satisfaction_post': cycle.get('satisfaction', 0.0),
            'field_coherence': cycle.get('field_coherence', 0.0)
        }
        tsk_metadata['wave_training']['phases'].append(phase_data)

    # Store to superject
    self.superject_learner.record_wave_training_metadata(
        user_id=user_id,
        tsk_metadata=tsk_metadata
    )
```

**Expected Impact (Phase 3):**
- ✅ Wave training metadata persists
- ✅ Epoch learning can analyze phase transitions
- ✅ Per-user phase preference learning possible
- ✅ Cross-session intelligence growth

---

## 📊 Expected Improvements

### Quantitative Targets

| Metric | Current | After Phase 1 | After Phase 2 | After Phase 3 |
|--------|---------|---------------|---------------|---------------|
| **Satisfaction Variance** | ~0.000 | 0.010+ | 0.015+ | 0.020+ |
| **Nexus Formation Rate** | 0% | 10-20% | 40-60% | 60-80% |
| **Kairos Detection** | 0% | 80-90% | 85-95% | 90-95% |
| **Organic Emissions** | 20-30% | 30-40% | 50-70% | 70-80% |
| **Organ Specialization** | 0.00 std | 0.05 std | 0.10 std | 0.15-0.20 std |
| **LLM Dependency** | 70-80% | 60-70% | 30-50% | 20-30% |

### Qualitative Improvements

**User Experience:**
- ✅ More varied responses (not flat personality)
- ✅ Adaptive to conversation rhythm (expansive → navigation → completion)
- ✅ Genuine kairos moments ("this feels right")
- ✅ Stronger personality emergence

**Organism Intelligence:**
- ✅ Organs learn when to activate (temporal patterns)
- ✅ Cross-organ coordination (field coherence)
- ✅ Dynamic convergence (not always 3 cycles)
- ✅ Whiteheadian prehension (feeling past satisfactions)

---

## 🗓️ Implementation Timeline

### Week 1: Core Wave Training (Priority: CRITICAL)

**Days 1-2:**
- [ ] Implement `_apply_wave_training_modulation()` in conversational_occasion.py
- [ ] Implement `_determine_appetitive_phase()`
- [ ] Add config parameters
- [ ] Test with 10 conversations

**Days 3-4:**
- [ ] Validate satisfaction variance created
- [ ] Measure kairos detection improvement
- [ ] Fix any edge cases
- [ ] Document results

**Day 5:**
- [ ] Deploy to interactive mode
- [ ] User testing
- [ ] Verify nexus formation improvement

**Deliverable:** Satisfaction variance 0.000 → 0.010+, Kairos detection functional

---

### Week 2-3: Multi-Organ Prehensive Fields (Priority: HIGH)

**Week 2:**
- [ ] Implement `_calculate_field_coherence()`
- [ ] Integrate with nexus formation threshold
- [ ] Test with 20 conversations
- [ ] Measure nexus formation rate

**Week 3:**
- [ ] Tune coherence weighting (0.3 factor adjustable)
- [ ] Add debug visualization
- [ ] Validate organ specialization
- [ ] Deploy to production

**Deliverable:** Nexus formation 0% → 40-60%, Organic emissions 30% → 50-70%

---

### Week 4: TSK Metadata & Learning (Priority: MEDIUM)

**Days 1-3:**
- [ ] Add wave training metadata to TSK recording
- [ ] Implement phase transition tracking
- [ ] Store to superject

**Days 4-5:**
- [ ] Build epoch learning analysis
- [ ] Visualize phase preferences per user
- [ ] Document learning patterns

**Deliverable:** Wave training intelligence persists across sessions

---

## 🔧 Technical Specifications

### Phase Detection Algorithm (from DAE 3.0)

```python
def determine_phase(satisfaction: float, cycle: int, min_cycles: int, max_cycles: int):
    """
    Phase decision tree (validated in DAE 3.0):

    EXPANSIVE (exploration):
    - IF satisfaction < 0.55 AND cycle <= min_cycles
    - Modulation: -5%
    - Purpose: Encourage searching, prevent premature convergence

    CONCRESCENCE (completion):
    - IF satisfaction >= 0.70 OR cycle >= max_cycles - 2
    - Modulation: +5%
    - Purpose: Reward completion, boost confidence

    NAVIGATION (gradient following):
    - ELSE (satisfaction in [0.55, 0.70) AND mid-cycles)
    - Modulation: 0%
    - Purpose: Track felt gradient, neutral observation
    """
    if satisfaction < 0.55 and cycle <= min_cycles:
        return 'EXPANSIVE'
    elif satisfaction >= 0.70 or cycle >= max_cycles - 2:
        return 'CONCRESCENCE'
    else:
        return 'NAVIGATION'
```

### Modulation Application

```python
# CRITICAL: Apply modulation BEFORE storing to cycle result
satisfaction_raw = calculate_satisfaction(...)
satisfaction_modulated = satisfaction_raw * (1.0 + modulation)
satisfaction_final = clamp(satisfaction_modulated, 0.0, 1.0)

# Store final (modulated) value
cycle_result['satisfaction'] = satisfaction_final

# Also store pre-modulation for analysis (optional)
cycle_result['satisfaction_pre_modulation'] = satisfaction_raw
cycle_result['appetitive_phase'] = phase
cycle_result['modulation_applied'] = modulation
```

---

## 🚨 Risks & Mitigations

### Risk 1: Regression in Emission Quality

**Risk:** Wave training might reduce emission confidence

**Likelihood:** LOW (DAE 3.0 showed no regression)

**Mitigation:**
- Monitor confidence scores before/after
- A/B test: 50 conversations with wave training vs 50 without
- Rollback flag: `ENABLE_WAVE_TRAINING = False` if issues

### Risk 2: Over-Modulation

**Risk:** ±5% modulation too aggressive for conversational domain

**Likelihood:** MEDIUM (ARC-AGI ≠ conversation)

**Mitigation:**
- Start with ±3% modulation (configurable)
- Tune based on variance measurements
- Adjust phase thresholds (0.55/0.70) if needed

### Risk 3: Complexity Increase

**Risk:** Wave training adds cognitive load for debugging

**Likelihood:** MEDIUM

**Mitigation:**
- Comprehensive debug logging (`DEBUG_WAVE_TRAINING = True`)
- Visualization tools for phase transitions
- Clear documentation
- Disable flag for simplified debugging

---

## ✅ Success Criteria

### Must-Have (Phase 1)

1. ✅ **Satisfaction variance created**
   - Measurement: Std dev > 0.010 across cycles
   - Validation: Run 20 conversations, calculate variance

2. ✅ **Kairos detection functional**
   - Measurement: Kairos detected in 80-90% of multi-cycle conversations
   - Validation: Count kairos moments in 50 conversations

3. ✅ **No accuracy regression**
   - Measurement: User satisfaction ≥ baseline
   - Validation: Compare satisfaction ratings before/after

### Should-Have (Phase 2)

4. ✅ **Nexus formation improvement**
   - Measurement: Nexus formation rate > 40%
   - Validation: Count nexuses in 50 conversations

5. ✅ **Organ specialization**
   - Measurement: Organ confidence std dev > 0.10
   - Validation: Analyze organ_confidence.json after 100 conversations

### Nice-to-Have (Phase 3)

6. ✅ **Temporal learning enabled**
   - Measurement: Phase preferences learned per user
   - Validation: Analyze TSK metadata after 200 conversations

---

## 🔄 Integration with Current Todos

### Current Todo List (from session context)

1. [completed] Fix entity-organ tracker type mismatch
2. [completed] Check entity context string generation for placeholders
3. [completed] Test fixes with quick validation
4. [completed] Document all fixes in comprehensive report

### New Todos (Wave Training Integration)

5. [ ] **Implement core wave training** (Week 1, Priority: CRITICAL)
   - Add wave training modulation to conversational_occasion.py
   - Add config parameters
   - Test satisfaction variance

6. [ ] **Implement multi-organ prehensive fields** (Week 2-3, Priority: HIGH)
   - Add field coherence calculation
   - Integrate with nexus formation
   - Measure nexus improvement

7. [ ] **Implement TSK metadata capture** (Week 4, Priority: MEDIUM)
   - Add wave training metadata to TSK
   - Enable epoch learning
   - Validate persistence

8. [ ] **Implement Hebbian phrase extraction** (Parallel track, Priority: HIGH)
   - Extract successful LLM phrases
   - Store with felt-state signatures
   - Reduce LLM dependency 70% → 50%

---

## 📚 References

**DAE 3.0 Legacy:**
- `WAVE_TRAINING_FINAL_SUMMARY_OCT30_2025.md` - Core implementation
- `WAVE_TRAINING_TSK_METADATA_FIX_NOV01_2025.md` - TSK capture fixes

**DAE_HYPHAE_1 Current State:**
- `LEVEL2_FRACTAL_REWARDS_COMPLETE_NOV15_2025.md` - Organ confidence tracking
- `LLM_DEPENDENCY_REDUCTION_STRATEGY_NOV15_2025.md` - Phrase learning strategy
- `NEO4J_ROBUSTNESS_AND_FIXES_NOV15_2025.md` - Entity extraction fixes

**Process Philosophy:**
- Whitehead's Process and Reality (appetitive phases)
- DAE architecture philosophy (prehension, concrescence, satisfaction)

---

## 🎯 Conclusion

**Wave training integration is the HIGHEST PRIORITY fix** for DAE_HYPHAE_1's core intelligence issues.

**Why:**
1. ✅ Proven in DAE 3.0 (variance 0.000 → 0.011, kairos functional)
2. ✅ Addresses root cause of 0 nexuses (flat satisfaction → no variance → no discrimination)
3. ✅ Unlocks temporal learning (currently blocked)
4. ✅ Minimal risk (can be disabled via flag)
5. ✅ Fast implementation (Week 1 for core, Weeks 2-4 for enhancements)

**Recommendation:**
- **START IMMEDIATELY with Phase 1** (core wave training)
- **Parallel track: Hebbian phrase extraction** (Week 1-2)
- **Validate at each phase** before proceeding

**Expected Outcome:**
- Nexus formation: 0% → 60-80%
- Organic emissions: 30% → 70-80%
- LLM dependency: 70-80% → 20-30%
- Organism intelligence: Emergent, adaptive, Whiteheadian

**Status:** Ready for implementation
**Priority:** CRITICAL
**Next Step:** Implement Phase 1 core wave training (this week)
