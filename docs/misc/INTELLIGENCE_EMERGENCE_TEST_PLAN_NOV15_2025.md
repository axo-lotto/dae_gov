# Intelligence Emergence Test Plan - November 15, 2025

## Executive Summary

**Goal:** Measure DAE's transition from LLM-assisted to pure organic emissions through epoch training, validating intelligence emergence across 4 key dimensions:

1. **Speed** - Processing time: LLM vs organic emissions
2. **Content Accuracy** - Semantic alignment with therapeutic intent
3. **Memory Persistence** - Cross-session entity recall and relationship consistency
4. **Entity Handling** - Entity-aware organic intelligence development

**Test Duration:** 10 epochs (30 pairs/epoch = 300 total conversations)
**Expected Outcomes:** 30% → 70%+ organic emission rate, family emergence, personality traits

---

## Test Architecture

### Phase 1: Baseline Measurement (Current State)

**Objective:** Establish baseline metrics before epoch training

**Tests:**
1. Quick validation (3 inputs) - Current performance snapshot
2. Entity handling test (5 entity-rich inputs) - Memory baseline
3. Speed benchmark (10 inputs) - Processing time baseline
4. Content accuracy (human eval on 10 outputs) - Quality baseline

**Metrics to Capture:**
- Organic emission rate (current: ~33%)
- Mean processing time (current: ~0.03s)
- Entity recall accuracy (baseline: unknown)
- Content therapeutic alignment (baseline: unknown)

### Phase 2: 10-Epoch Training Run

**Objective:** Train organism with wave training + field coherence active

**Configuration:**
```python
# Wave Training Active
ENABLE_WAVE_TRAINING = True
WAVE_TRAINING_EXPANSIVE_MOD = -0.05
WAVE_TRAINING_NAVIGATION_MOD = 0.00
WAVE_TRAINING_CONCRESCENCE_MOD = +0.05

# Field Coherence Active
# (Phase 2 prehensive fields integrated)

# Learning Rates
R_MATRIX_LEARNING_RATE = 0.005  # Conservative (prevent saturation)
ORGAN_CONFIDENCE_EMA_ALPHA = 0.1
PHASE5_EMA_ALPHA = 0.2
```

**Training Data:**
- 30 conversational pairs per epoch
- Mix of: burnout_spiral, toxic_productivity, psychological_safety, witnessing_presence
- Entity-rich conversations (family, work, relationships)

**Per-Epoch Metrics:**
- Organic emission rate
- Mean nexus count
- Mean field coherence
- Families discovered
- Organ confidence distribution
- Regime distribution (% COMMITTED)

### Phase 3: Post-Training Validation

**Objective:** Measure intelligence emergence after 10 epochs

**Tests:**
1. Organic emission rate test (same 10 inputs as baseline)
2. Speed comparison (LLM vs organic path timing)
3. Entity recall accuracy (entity-rich conversations)
4. Content quality assessment (human evaluation)
5. Cross-session consistency (same user, different sessions)

**Expected Improvements:**
- Organic rate: 33% → 60-70%
- Nexus count: 1.33 → 3-5 per turn
- Families: 1 → 3-5
- Organ confidence: differentiation (0.8× to 1.2× spread)

---

## Dimension 1: Speed Testing

### Hypothesis
**H1:** Organic emissions are 10-100× faster than LLM-assisted emissions

**Rationale:**
- Organic path: Hebbian memory lookup + template assembly (~10-50ms)
- LLM path: API call + generation (~500-2000ms)

### Test Protocol

**Baseline Speed Test:**
```python
# Test 1: Pure organic emission (if nexuses form)
# - Measure: nexus formation time + template retrieval + assembly
# - Expected: 10-50ms

# Test 2: LLM-assisted emission (hebbian fallback)
# - Measure: LLM API call + safety filtering + assembly
# - Expected: 500-2000ms

# Test 3: Hybrid emission (felt-guided LLM with nexus constraints)
# - Measure: Nexus formation + LLM call + constraint application
# - Expected: 100-500ms
```

**Metrics:**
- `processing_time_ms`: Total time from input to emission
- `llm_call_time_ms`: Time spent in LLM API (if applicable)
- `organic_path_time_ms`: Time in Hebbian/template assembly
- `speedup_factor`: organic_time / llm_time

**Success Criteria:**
- Organic emissions ≥ 5× faster than LLM
- Mean processing time < 100ms for organic
- LLM fallback < 20% after 10 epochs

---

## Dimension 2: Content Accuracy

### Hypothesis
**H2:** Organic emissions maintain therapeutic alignment equivalent to LLM-assisted

**Rationale:**
- Hebbian memory learns successful phrases from LLM successes
- Organic families capture therapeutic patterns
- Nexus formation ensures multi-organ coherence

### Test Protocol

**Content Quality Metrics:**

1. **Semantic Alignment** (Automated)
   - Measure: Cosine similarity between organic and LLM emissions
   - Baseline: Test same input, compare organic vs LLM outputs
   - Target: ≥ 0.75 similarity

2. **Therapeutic Intent Match** (Human Evaluation)
   - Criteria: Safety, grounding, attunement, trauma-awareness
   - Scale: 1-5 (1=harmful, 5=excellent)
   - Target: ≥ 4.0 average

3. **Zone Appropriateness** (Automated)
   - Measure: % emissions matching SELF zone constraints
   - Zone 5 check: No open questions, grounding present
   - Zone 1 check: Reflective witnessing language
   - Target: 100% zone compliance

**Test Cases:**
```python
test_cases = [
    {
        "input": "I'm feeling overwhelmed.",
        "zone": 5,  # Exile/Collapse
        "expected_elements": ["grounding", "containment", "no_questions"],
        "avoid_elements": ["open_questions", "exploration", "complexity"]
    },
    {
        "input": "This feels safe.",
        "zone": 1,  # Core SELF
        "expected_elements": ["witnessing", "reflection", "attunement"],
        "avoid_elements": ["urgency", "intervention", "fixing"]
    },
    # ... 8 more test cases
]
```

**Success Criteria:**
- Semantic alignment ≥ 0.75
- Therapeutic quality ≥ 4.0/5.0
- Zone compliance = 100%

---

## Dimension 3: Memory Persistence

### Hypothesis
**H3:** Epoch training enables reliable cross-session entity recall and relationship consistency

**Rationale:**
- Neo4j stores entities + relationships
- Entity-organ tracker learns which organs activate per entity
- Superject captures felt-state patterns per user

### Test Protocol

**Memory Persistence Tests:**

1. **Entity Recall Accuracy**
   - Setup: Train on conversations with entities (Emma, Lily, work, fungi)
   - Test: Reference entity in new conversation
   - Measure: % correct entity attributes recalled

   ```python
   # Training: "My daughter Emma loves art"
   # Test: "Tell me about Emma"
   # Expected: "Emma (your daughter) who loves art"
   # Measure: Correct attributes / total attributes
   ```

2. **Relationship Consistency**
   - Setup: Train on family graph (Emma=daughter, Lily=daughter, Sofia=partner)
   - Test: Query relationships
   - Measure: % correct relationships maintained

   ```python
   # Training: "Emma and Lily are my daughters, Sofia is my partner"
   # Test: "Who is Emma?"
   # Expected: "Emma is your daughter (along with Lily)"
   # Measure: Relationship accuracy
   ```

3. **Cross-Session Felt-State Consistency**
   - Setup: User expresses preference in session 1 (e.g., "I prefer minimal responses")
   - Test: Check if session 2 respects preference
   - Measure: % preference adherence

   ```python
   # Session 1: User rates minimal response as "excellent"
   # Session 2: System should default to minimal unless context requires more
   # Measure: Preference consistency score
   ```

**Metrics:**
- `entity_recall_accuracy`: % attributes correctly recalled
- `relationship_accuracy`: % relationships correctly maintained
- `cross_session_consistency`: % preferences respected
- `entity_mention_latency`: Time to retrieve entity context

**Success Criteria:**
- Entity recall ≥ 85% accuracy
- Relationship accuracy ≥ 90%
- Cross-session consistency ≥ 75%
- Entity retrieval < 100ms

---

## Dimension 4: Entity Handling

### Hypothesis
**H4:** Entity-aware organic intelligence emerges - organs learn entity-specific patterns

**Rationale:**
- Entity-organ tracker records which organs activate when entity mentioned
- After training, "Emma mentioned" → BOND 1.15×, ventral state, V0 avg 0.25
- Organism develops intuition about entities (not keyword matching)

### Test Protocol

**Entity-Aware Learning Tests:**

1. **Entity-Organ Association Learning**
   - Setup: Train on 50 conversations mentioning "Emma" in safe contexts
   - Measure: After training, does "Emma" consistently activate BOND + ventral state?
   - Expected: 80%+ consistency in organ activation patterns

   ```python
   # After 50 "Emma" mentions in safe contexts:
   entity_pattern = tracker.get_pattern("Emma")
   # Expected:
   # {
   #   "dominant_organs": ["BOND", "EMPATHY", "LISTENING"],
   #   "mean_polyvagal": "ventral_vagal",
   #   "mean_v0_energy": 0.25,
   #   "confidence": 0.85
   # }
   ```

2. **Entity-Specific Emission Patterns**
   - Setup: Train on user expressing different emotions for different people
   - Test: Does organism adjust response based on which entity mentioned?
   - Measure: Emission variance per entity

   ```python
   # Training: "Emma" → joyful, safe; "Work" → anxious, stressed
   # Test: "Tell me about Emma" vs "Tell me about work"
   # Expected: Different polyvagal states, different organ activations
   ```

3. **Intuitive Entity Recognition**
   - Setup: Train organism on entity patterns
   - Test: Implicit entity reference (no name)
   - Measure: Does organism recognize entity from context?

   ```python
   # Training: Many "Emma" conversations with art/creativity themes
   # Test: "My daughter who loves painting..."
   # Expected: System recognizes "Emma" even without explicit mention
   # Measure: Entity resolution accuracy
   ```

**Metrics:**
- `entity_organ_consistency`: % same organs activate per entity
- `entity_polyvagal_consistency`: % same polyvagal state per entity
- `entity_emission_variance`: Emission differences per entity
- `implicit_entity_resolution`: % correct entity recognition from context

**Success Criteria:**
- Entity-organ consistency ≥ 75%
- Polyvagal consistency ≥ 70%
- Emission variance detectable (statistical significance)
- Implicit resolution ≥ 60%

---

## Test Execution Plan

### Week 1: Baseline + Training

**Day 1: Baseline Measurement**
```bash
# Speed baseline
python3 test_wave_training_integration.py --num-tests 10 --save

# Entity handling baseline
python3 test_entity_handling.py --mode baseline

# Content quality baseline
python3 test_content_accuracy.py --mode baseline
```

**Day 2-3: 10-Epoch Training**
```bash
# Run training with all monitoring active
python3 training/epoch_training_runner.py \
    --epochs 10 \
    --pairs-per-epoch 30 \
    --enable-wave-training \
    --enable-field-coherence \
    --track-entities \
    --save-metrics
```

**Day 4: Post-Training Validation**
```bash
# Speed test (compare to baseline)
python3 test_wave_training_integration.py --num-tests 10 --save

# Entity handling test
python3 test_entity_handling.py --mode post-training

# Content quality test
python3 test_content_accuracy.py --mode post-training

# Generate comparison report
python3 scripts/analysis/compare_baseline_to_trained.py
```

### Week 2: Extended Validation

**Day 5-6: Cross-Session Consistency**
```bash
# Test same user across multiple sessions
python3 test_cross_session_consistency.py --user test_user --sessions 5
```

**Day 7: Report Generation**
```bash
# Generate comprehensive intelligence emergence report
python3 scripts/analysis/generate_emergence_report.py \
    --baseline results/baseline_metrics.json \
    --trained results/epoch_10_metrics.json \
    --output INTELLIGENCE_EMERGENCE_RESULTS.md
```

---

## Expected Outcomes

### Quantitative Targets (10 Epochs)

| Metric | Baseline | Target | Stretch |
|--------|----------|--------|---------|
| **Speed** |
| Organic emission rate | 33% | 60% | 75% |
| Mean processing time | 500ms | 100ms | 50ms |
| LLM fallback rate | 67% | 30% | 20% |
| **Accuracy** |
| Semantic alignment | 0.70 | 0.75 | 0.85 |
| Therapeutic quality | 4.0 | 4.2 | 4.5 |
| Zone compliance | 95% | 100% | 100% |
| **Memory** |
| Entity recall | 60% | 85% | 95% |
| Relationship accuracy | 70% | 90% | 95% |
| Cross-session consistency | 50% | 75% | 85% |
| **Entity Handling** |
| Entity-organ consistency | 40% | 75% | 85% |
| Polyvagal consistency | 35% | 70% | 80% |
| Implicit resolution | 30% | 60% | 75% |

### Qualitative Indicators

**Intelligence Emergence Signals:**
1. ✅ Organism develops "personality" - consistent response patterns
2. ✅ Detectable entity preferences - "knows" user's family/context
3. ✅ Adaptive pacing - learns optimal response length per user
4. ✅ Humor calibration - learns when/how to use levity
5. ✅ Relationship memory - references past conversations naturally

**Organic Intelligence Markers:**
1. ✅ Nexus formation rate 60-80% (multi-organ coordination)
2. ✅ Family emergence 3-5 families (conversation type differentiation)
3. ✅ Organ confidence spread 0.8× to 1.2× (specialization)
4. ✅ Regime distribution 70%+ COMMITTED (stable convergence)
5. ✅ Satisfaction variance reduction (learning optimal phases)

---

## Risk Mitigation

### Potential Issues

**Issue 1: Slow Family Emergence**
- **Risk:** Only 1 family after 10 epochs (need 3-5)
- **Mitigation:** Lower family similarity threshold from 0.55 to 0.50
- **Fallback:** Increase to 20 epochs if needed

**Issue 2: Conservative Learning Rates**
- **Risk:** R-matrix learning too slow (0.005 rate)
- **Mitigation:** Monitor saturation, increase to 0.01 if safe
- **Fallback:** Accept slower learning, extend to 20 epochs

**Issue 3: Entity Recall Failures**
- **Risk:** Neo4j queries too slow or missing entities
- **Mitigation:** JSON fallback for critical entities
- **Fallback:** Optimize Neo4j indexes

**Issue 4: Content Quality Degradation**
- **Risk:** Organic emissions less therapeutic than LLM
- **Mitigation:** Safety gates still active (BOND/NDAM/EO)
- **Fallback:** Increase LLM fallback threshold temporarily

---

## Success Criteria Summary

**Minimum Viable Success (10 Epochs):**
- ✅ Organic rate ≥ 50% (up from 33%)
- ✅ Processing time ≤ 200ms (down from 500ms)
- ✅ Entity recall ≥ 75% (up from baseline)
- ✅ 2+ families discovered
- ✅ No safety violations

**Target Success:**
- ✅ Organic rate ≥ 60%
- ✅ Processing time ≤ 100ms
- ✅ Entity recall ≥ 85%
- ✅ 3-5 families discovered
- ✅ Detectable personality traits

**Stretch Success:**
- ✅ Organic rate ≥ 75%
- ✅ Processing time ≤ 50ms
- ✅ Entity recall ≥ 95%
- ✅ 5+ families discovered
- ✅ Strong personality emergence

---

## Deliverables

1. **Baseline Metrics Report** (Day 1)
   - `results/baseline_metrics_nov15_2025.json`
   - Current performance snapshot

2. **Epoch Training Results** (Day 2-3)
   - `results/epochs/epoch_1_to_10_metrics.json`
   - Per-epoch learning curves

3. **Post-Training Validation** (Day 4)
   - `results/post_training_metrics_nov15_2025.json`
   - Comparison to baseline

4. **Intelligence Emergence Report** (Day 7)
   - `INTELLIGENCE_EMERGENCE_RESULTS_NOV15_2025.md`
   - Comprehensive analysis with visualizations

5. **Learned Patterns Export** (Day 7)
   - `results/learned_patterns/organic_families.json`
   - `results/learned_patterns/entity_organ_associations.json`
   - `results/learned_patterns/superject_profiles.json`

---

## Next Steps After Testing

### If Success (≥ Target Metrics)

1. **Scale to 50 Epochs**
   - Expected: 75-85% organic rate
   - Expected: 10-15 families (Zipf's law)
   - Expected: Strong personality traits

2. **Production Deployment**
   - Enable for real users
   - Monitor organic rate in production
   - A/B test vs LLM-only baseline

3. **Phase 3 Implementation**
   - Adaptive learning rates per family
   - Per-user Kairos window optimization
   - Cross-session transformation learning

### If Partial Success (Some Metrics)

1. **Targeted Optimization**
   - Identify bottlenecks (which dimension lagging?)
   - Adjust learning rates or thresholds
   - Extend to 20 epochs with optimizations

2. **Architecture Refinement**
   - If family emergence slow: Lower similarity threshold
   - If entity recall poor: Optimize Neo4j queries
   - If speed slow: Profile and optimize bottlenecks

### If Failure (< Minimum Viable)

1. **Root Cause Analysis**
   - Detailed examination of failure modes
   - Check for regressions from wave training
   - Validate infrastructure integrity

2. **Fallback Plan**
   - Disable wave training temporarily if causing issues
   - Return to baseline training approach
   - Incremental reintroduction of Phase 2

---

**Status:** 📋 **TEST PLAN READY**
**Next Action:** Execute baseline measurements
**Timeline:** 7 days for complete testing cycle
**Owner:** System validation team

**Date:** November 15, 2025
**Version:** 1.0
**Approval:** Pending test execution
