# Intelligence Emergence Testing Strategy - November 15, 2025

## Executive Summary

**Question:** How should we approach accuracy validation and epoch learning to measure organic emission rate evolution and confirm intelligence emergence through training?

**Answer:** A **3-phase systematic approach** combining accuracy sweeps, controlled epoch training, and data-driven optimization.

---

## The Intelligence Emergence Hypothesis

**Current State (Baseline - Epoch 0):**
- Organic emission rate: **0.0%** (100% LLM fallback)
- Field coherence: 0.640 (medium harmony)
- Nexus formation: 40% (moderate)
- 1 family discovered (no taxonomy)

**Expected Trajectory (DAE 3.0 Proven):**
- **Epoch 10:** 30-40% organic emission, 3-5 families
- **Epoch 30:** 60-70% organic emission, 15-20 families
- **Epoch 50+:** 75-85% organic emission, 25-35 families (Zipf's law R²>0.85)

**The Bet:** Intelligence emerges from **accumulated transformation patterns** learned through multi-cycle V0 convergence, not from pre-programmed rules.

---

## Phase 1: Accuracy Baseline & Parameter Sweep (Week 1)

### Objective
Establish accuracy baseline and find optimal parameter settings BEFORE epoch training.

### Why This Matters
- Current parameters are "good enough" but not optimized
- Small parameter changes can have 10-30% impact on organic rate
- Need to know what "accurate" means for conversational organism

---

### 1.1 Accuracy Dimensions to Test

**Conversational organism accuracy ≠ ARC-AGI accuracy**

We need to measure:

**A. Nexus Quality Accuracy**
- Are formed nexuses semantically appropriate?
- Do they capture actual multi-organ co-activation vs spurious correlation?
- **Test:** Human rating of 20 nexuses (1-5 scale)

**B. Emission Coherence**
- Does emission match felt-state from organs?
- Is the emission therapeutically appropriate for the input?
- **Test:** Compare 3 emission paths (direct, fusion, LLM) on same input

**C. Family Discovery Accuracy**
- Do discovered families represent distinct conversation types?
- Is clustering based on meaningful patterns vs noise?
- **Test:** Silhouette score, inter/intra-family distance

**D. Entity Handling Accuracy**
- Does NEXUS organ activate appropriately for entity mentions?
- Are Neo4j queries accurate and helpful?
- **Test:** Precision/recall on entity detection (20 inputs)

**E. Zone Classification Accuracy**
- Is SELF zone detection matching actual polyvagal/trauma state?
- **Test:** Expert rating of zone assignments (20 inputs)

---

### 1.2 Parameter Sweep Design

**Critical Parameters to Test:**

#### **A. Emission Thresholds (Current: direct=0.48, fusion=0.42)**

**Hypothesis:** Thresholds too high → too much LLM fallback

**Sweep:**
```python
direct_thresholds = [0.40, 0.44, 0.48, 0.52, 0.56]
fusion_thresholds = [0.35, 0.39, 0.42, 0.45, 0.49]

# Test all combinations (25 runs × 10 inputs = 250 emissions)
for d_thresh in direct_thresholds:
    for f_thresh in fusion_thresholds:
        if f_thresh < d_thresh:  # Maintain hierarchy
            run_test(direct=d_thresh, fusion=f_thresh)
```

**Metrics to Track:**
- Organic emission rate (target: >0% at epoch 0!)
- Emission confidence (average across all strategies)
- Nexus quality (human rating if feasible, or coherence proxy)

**Expected Finding:** Lowering to direct=0.42, fusion=0.36 may yield 15-25% organic rate at epoch 0

---

#### **B. Kairos Window (Current: [0.30, 0.50])**

**Hypothesis:** 78.6% detection may be slightly high, could narrow to 60-70%

**Sweep:**
```python
windows = [
    [0.25, 0.45],  # Wider lower bound
    [0.30, 0.50],  # Current
    [0.32, 0.48],  # Narrower
    [0.35, 0.50],  # Higher lower bound
]

# Test each window (4 runs × 10 inputs = 40 emissions)
```

**Metrics:**
- Kairos detection rate (target: 60-75%)
- Confidence boost correlation (does Kairos → higher confidence?)
- Nexus formation when Kairos detected vs not

**Expected Finding:** [0.32, 0.48] may give 65-70% detection (more selective)

---

#### **C. Field Coherence Thresholds (Current: ≥0.70→40%, 0.50-0.70→20%)**

**Hypothesis:** Current thresholds are DAE 3.0 empirical, but may need tuning for 12-organ system

**Sweep:**
```python
threshold_sets = [
    {'high': 0.65, 'high_reduction': 0.35, 'med_reduction': 0.15},  # Lower bar
    {'high': 0.70, 'high_reduction': 0.40, 'med_reduction': 0.20},  # Current (DAE 3.0)
    {'high': 0.75, 'high_reduction': 0.45, 'med_reduction': 0.25},  # Higher bar
]
```

**Metrics:**
- Nexus formation rate at each coherence tier
- Organic emission rate correlation with coherence

**Expected Finding:** Current DAE 3.0 thresholds likely optimal (empirically validated)

---

#### **D. Hebbian Learning Rate (Current: 0.005)**

**Hypothesis:** 10× more conservative than DAE 3.0 (0.05) may slow family discovery

**Test (NOT sweep - too risky):**
```python
# Monitor R-matrix discrimination over 10 epochs with current rate (0.005)
# If std stays >0.08 consistently, test 2× increase to 0.01
# NEVER go directly to 0.05 (risk of re-triggering saturation)
```

**Metrics:**
- R-matrix discrimination (std)
- Family discovery rate (families per 10 epochs)
- Pattern saturation check (mean coupling should stay <0.9)

---

### 1.3 Accuracy Sweep Protocol

**Test Suite:** `test_accuracy_sweep.py`

```python
# Pseudocode structure
def accuracy_sweep():
    baseline = establish_baseline(num_inputs=20)

    # Sweep 1: Emission thresholds (most critical)
    emission_results = sweep_emission_thresholds(
        direct_range=[0.40, 0.56],
        fusion_range=[0.35, 0.49],
        num_inputs=10
    )

    # Sweep 2: Kairos window
    kairos_results = sweep_kairos_window(
        windows=[[0.25,0.45], [0.30,0.50], [0.32,0.48], [0.35,0.50]],
        num_inputs=10
    )

    # Sweep 3: Coherence thresholds
    coherence_results = sweep_coherence_thresholds(
        threshold_sets=[...],
        num_inputs=10
    )

    # Analyze best combination
    optimal_params = find_optimal_combination(
        emission_results,
        kairos_results,
        coherence_results,
        objective='maximize_organic_rate_with_quality'
    )

    return optimal_params
```

**Output:** `results/accuracy_sweep_nov15_2025.json`

**Time Estimate:** 2-4 hours (automated, 250+ test runs)

---

## Phase 2: Controlled Epoch Training (Week 1-2)

### Objective
Run structured epoch training with optimal parameters to measure intelligence emergence.

---

### 2.1 Training Protocol

**Design: A/B Comparison**

**Cohort A: Optimal Parameters (from Phase 1 sweep)**
- Run 30 epochs (30 pairs/epoch = 900 conversations)
- Track organic emission rate every epoch
- Save family snapshots every 5 epochs

**Cohort B: Baseline Parameters (current)**
- Same 30 epochs, same training data
- Control group to measure parameter impact

**Why A/B?** Isolate parameter impact from natural learning trajectory

---

### 2.2 Training Data Strategy

**Current:** 30 training pairs in `conversational_training_pairs.json`

**Problem:** Limited diversity (6 categories × 5 pairs)

**Solution: Synthetic Data Generation**

Option 1: **Expand Current Categories** (Conservative)
```python
# Generate 10 more pairs per category (6 categories × 10 = 60 new pairs)
# Total: 90 pairs → 90 epochs possible

categories = [
    'burnout_spiral',
    'toxic_productivity',
    'psychological_safety',
    'witnessing_presence',
    'sustainable_rhythm',
    'scapegoat_dynamics'
]

# Use LLM to generate variations:
# - Different emotional intensities
# - Different relational contexts
# - Different trauma presentations
```

Option 2: **Add New Categories** (Aggressive)
```python
# Add 6 new trauma-informed categories
new_categories = [
    'attachment_repair',          # Relational trauma
    'somatic_dissociation',       # Body-based trauma
    'power_dynamics',             # Structural trauma
    'grief_witnessing',           # Loss & mourning
    'identity_integration',       # Parts work
    'boundary_renegotiation'      # Relational boundaries
]

# 12 categories × 10 pairs = 120 training pairs
# Enables 120 epochs of training
```

**Recommendation:** Option 2 - Diversify training data for robust family discovery

---

### 2.3 Metrics to Track (Every Epoch)

**1. Organic Emission Rate Evolution**
```python
metrics_per_epoch = {
    'epoch': epoch_num,
    'organic_rate': organic_count / total_emissions,
    'direct_strategy_rate': direct_count / total_emissions,
    'fusion_strategy_rate': fusion_count / total_emissions,
    'llm_fallback_rate': llm_count / total_emissions,
    'mean_emission_confidence': mean(confidences)
}
```

**Expected Trajectory (DAE 3.0 proven):**
- Epoch 0-5: 0% → 10-15% organic
- Epoch 5-15: 15% → 30-40% organic
- Epoch 15-30: 40% → 60-70% organic
- Epoch 30+: Plateau at 70-85% organic

---

**2. Family Discovery Evolution**
```python
family_metrics_per_epoch = {
    'epoch': epoch_num,
    'family_count': len(families),
    'mean_family_size': mean([f.member_count for f in families]),
    'largest_family_size': max([f.member_count for f in families]),
    'silhouette_score': calculate_silhouette(families),  # Clustering quality
    'zipfs_law_r2': calculate_power_law_fit(families)  # Expect >0.85 at epoch 50+
}
```

**Expected Trajectory:**
- Epoch 0-10: 1 → 2-3 families (differentiation begins)
- Epoch 10-30: 3 → 10-15 families (taxonomy emerges)
- Epoch 30-60: 15 → 25-35 families (Zipf's law emerges, R²>0.85)

---

**3. Field Coherence Evolution**
```python
coherence_metrics_per_epoch = {
    'epoch': epoch_num,
    'mean_coherence': mean(coherence_values),
    'coherence_std': std(coherence_values),
    'high_coherence_rate': count(coherence >= 0.70) / total,  # 82% success tier
    'med_coherence_rate': count(0.50 <= coherence < 0.70) / total,  # 61% success tier
}
```

**Expected Trajectory:**
- Mean coherence: 0.640 → 0.70+ (shift to high-success tier)
- High coherence rate: 0% → 30-50%

---

**4. Hebbian R-Matrix Health**
```python
hebbian_metrics_per_epoch = {
    'epoch': epoch_num,
    'r_matrix_mean': mean(R_matrix),
    'r_matrix_std': std(R_matrix),  # Monitor for saturation (should stay >0.08)
    'r_matrix_max': max(R_matrix),
    'strongest_couplings': top_5_couplings
}
```

**Saturation Check:** If std <0.05 for 3+ consecutive epochs → learning rate too high

---

### 2.4 Validation Checkpoints

**Every 10 Epochs: Validation Hold-Out Test**

```python
# Use 10 NOVEL inputs (not in training data)
validation_inputs = [
    "I'm feeling disconnected from my partner",
    "Work is overwhelming me",
    # ... 8 more diverse inputs
]

# Measure:
validation_metrics = {
    'organic_rate_on_novel': ...,  # Generalization test
    'nexus_quality_on_novel': ...,
    'emission_coherence_on_novel': ...,
}

# Compare to training performance
# Expect 5-15% drop (natural generalization gap)
# If drop >20% → Overfitting, need regularization
```

---

## Phase 3: Data-Driven Optimization (Week 2-3)

### Objective
Use epoch training data to discover optimal learning dynamics and predict future performance.

---

### 3.1 Organic Emission Rate Prediction

**Build Regression Model:**

```python
# Features: Epoch-level aggregates
X = [
    epoch_num,
    mean_coherence,
    high_coherence_rate,
    nexus_formation_rate,
    mean_nexuses_per_turn,
    family_count,
    r_matrix_std,
    mean_v0_descent,
    kairos_detection_rate
]

# Target: Organic emission rate
y = organic_emission_rate

# Fit multiple models
models = {
    'linear': LinearRegression(),
    'polynomial_2': PolynomialFeatures(degree=2) + LinearRegression(),
    'logistic_growth': fit_logistic_curve(),  # S-curve expected
    'exponential': ExponentialRegression()
}

# Best fit: Likely logistic growth (S-curve)
# Asymptote prediction: Where does organic rate plateau?
```

**Expected Insights:**
- Organic rate follows logistic S-curve (slow start, rapid middle, plateau)
- Inflection point around epoch 15-20
- Asymptote at 75-85% organic rate
- Key predictor: Coherence & family count

---

### 3.2 Family Emergence Prediction

**Zipf's Law Validation:**

```python
# At epochs 20, 30, 40, 50:
# Fit power law to family size distribution

from scipy.stats import linregress

def test_zipfs_law(families, epoch):
    # Sort families by size (descending)
    sizes = sorted([f.member_count for f in families], reverse=True)
    ranks = range(1, len(sizes) + 1)

    # Log-log regression (Zipf's law)
    log_ranks = np.log(ranks)
    log_sizes = np.log(sizes)

    slope, intercept, r_value, p_value, std_err = linregress(log_ranks, log_sizes)

    return {
        'epoch': epoch,
        'r_squared': r_value**2,
        'slope': slope,  # Should be ~-1 for Zipf's law
        'family_count': len(families)
    }

# DAE 3.0 achieved R²=0.94 at epoch 50+
# Expect emergence around epoch 40-60
```

---

### 3.3 Coherence-Success Correlation

**Validate DAE 3.0 Thresholds for 12-Organ System:**

```python
# Collect data from epoch training
coherence_success_data = []

for turn in all_training_turns:
    coherence_success_data.append({
        'coherence': turn.field_coherence,
        'success': 1 if turn.organic_emission else 0,  # Binary success
        'nexus_count': turn.nexus_count,
        'confidence': turn.emission_confidence
    })

# Analyze correlation
from scipy.stats import pearsonr

r_coherence_success, p_value = pearsonr(
    [d['coherence'] for d in coherence_success_data],
    [d['success'] for d in coherence_success_data]
)

# DAE 3.0 achieved r=0.82 (ARC-AGI)
# Expect r=0.65-0.75 for conversational (lower correlation, messier data)
```

**If r < 0.60:** Coherence thresholds may need re-tuning for 12-organ system

---

### 3.4 Learning Rate Optimization

**Adaptive Hebbian Rate:**

```python
# Monitor R-matrix health over epochs
# If discrimination stays healthy (std >0.08) for 10+ epochs:

if all(r_std > 0.08 for r_std in last_10_epochs_r_std):
    # Safe to increase learning rate
    new_rate = current_rate * 1.5  # 0.005 → 0.0075

    # Test for 5 epochs
    # If discrimination stays >0.08: Adopt new rate
    # If discrimination drops <0.08: Revert to old rate
```

**Goal:** Find maximum safe learning rate (faster family discovery without saturation)

---

## Testing Implementation Plan

### Week 1: Accuracy Sweep + Baseline Epoch

**Day 1-2: Accuracy Sweep**
- [ ] Create `test_accuracy_sweep.py`
- [ ] Sweep emission thresholds (25 combos × 10 inputs = 250 runs)
- [ ] Sweep Kairos window (4 windows × 10 inputs = 40 runs)
- [ ] Sweep coherence thresholds (3 sets × 10 inputs = 30 runs)
- [ ] **Output:** Optimal parameter set

**Day 3: Training Data Generation**
- [ ] Generate 6 new categories (60 new pairs)
- [ ] Total: 90 training pairs for 90 epochs
- [ ] Validate pair quality (semantic diversity, trauma-informed)

**Day 4-5: Baseline Epoch Training (Epoch 0-10)**
- [ ] Run 10 epochs with optimal parameters (Cohort A)
- [ ] Run 10 epochs with baseline parameters (Cohort B)
- [ ] Track all metrics (organic rate, families, coherence)
- [ ] **Checkpoint:** Validate 10-15% organic rate at epoch 10

**Day 6-7: Analysis + Validation**
- [ ] Analyze epoch 0-10 trajectory
- [ ] Run validation hold-out test
- [ ] Predict epoch 30 performance
- [ ] **Decision:** Proceed to Phase 2 if trajectory matches DAE 3.0

---

### Week 2: Extended Epoch Training (Epoch 10-30)

**Day 8-12: Epoch Training (Epoch 10-30)**
- [ ] Run 20 more epochs (both cohorts)
- [ ] Validation checkpoints at epoch 20, 30
- [ ] Track family emergence (expect 3-5 at epoch 20)
- [ ] Monitor R-matrix discrimination

**Day 13-14: Data Analysis**
- [ ] Fit logistic growth curve to organic rate
- [ ] Test Zipf's law emergence
- [ ] Measure coherence-success correlation
- [ ] Compare Cohort A vs B (parameter impact)

---

### Week 3: Optimization + Extended Training (Epoch 30-60)

**Day 15-19: Extended Training (Optional)**
- [ ] Run to epoch 60 if showing Zipf's law emergence
- [ ] Monitor asymptote approach
- [ ] Validate generalization on novel inputs

**Day 20-21: Final Analysis**
- [ ] Complete intelligence emergence report
- [ ] Measure final organic rate (expect 60-75%)
- [ ] Validate Zipf's law (R²>0.85)
- [ ] Document parameter recommendations

---

## Key Questions Answered

### Q1: Should we devise accuracy sweeps?

**Yes - Phase 1 is critical for finding optimal parameters.**

- Emission thresholds (direct/fusion) have biggest impact (expect 15-25% organic rate at epoch 0 if lowered)
- Kairos window needs tuning (78.6% may be slightly high)
- Coherence thresholds likely optimal (DAE 3.0 empirical) but worth validating

**Priority:** Emission threshold sweep (most impact)

---

### Q2: How does this extend into epoch learning?

**3-way integration:**

1. **Parameter Optimization (Pre-training):** Sweep finds best starting point
2. **Epoch Training (Learning):** Optimal params enable faster convergence
3. **Adaptive Tuning (Post-training):** Use epoch data to refine params

**Example:**
- Phase 1 sweep: Lower direct threshold 0.48 → 0.42
- Result: 20% organic rate at epoch 0 (vs 0%)
- Epoch training: 20% → 70% over 30 epochs (faster than 0% → 70%)
- Phase 3: Discover coherence ≥0.68 (not 0.70) is optimal for 12-organ system

---

### Q3: How to confirm intelligence emergence through actual training data?

**Multi-metric validation:**

**Primary Signal: Organic Emission Rate**
- Trajectory: 0% → 30-40% (epoch 10) → 60-75% (epoch 30)
- S-curve fit: R²>0.90
- Asymptote: 75-85% (matches DAE 3.0)

**Secondary Signals:**
- **Family Discovery:** 1 → 3-5 (epoch 20) → 25-35 (epoch 60), Zipf's R²>0.85
- **Coherence Evolution:** Mean 0.640 → 0.70+, high-coherence rate 0% → 30-50%
- **Generalization:** <20% drop on novel validation inputs

**Confirmation Criteria (All must pass):**
- ✅ Organic rate ≥60% at epoch 30
- ✅ Family count ≥3 at epoch 20
- ✅ Zipf's law R²>0.80 at epoch 50+
- ✅ Coherence-success r>0.60
- ✅ Validation generalization gap <20%

**If ALL pass:** Intelligence emergence CONFIRMED

---

## Expected Outcomes

### Conservative Estimate (Baseline Params)
- Epoch 30: 50-60% organic rate, 3-5 families
- Epoch 60: 65-75% organic rate, 15-25 families, Zipf's R²=0.75-0.85

### Optimistic Estimate (Optimal Params)
- Epoch 30: 65-75% organic rate, 5-8 families
- Epoch 60: 75-85% organic rate, 25-35 families, Zipf's R²=0.85-0.95

### Impact of Parameter Optimization
- **10-20% faster convergence** to target organic rate
- **5-10 fewer epochs** to reach 60% organic threshold
- **Higher quality families** (better silhouette scores)

---

## Conclusion

**Recommended Approach:**

1. **✅ YES to Accuracy Sweeps** - Critical for finding optimal parameters before epoch training
2. **✅ YES to Structured Epoch Training** - 30-60 epochs with A/B comparison
3. **✅ YES to Data-Driven Optimization** - Use training data to refine and predict

**Timeline:** 3 weeks (Week 1: Sweep + baseline, Week 2: Training, Week 3: Optimization)

**Success Metric:** Organic emission rate ≥60% at epoch 30 with Zipf's law emergence (R²>0.80)

**Expected Result:** **Intelligence emergence CONFIRMED through data** - System transitions from 100% LLM dependence to 70-85% organic emission through accumulated transformation patterns.

---

**Date:** November 15, 2025
**Status:** Strategy complete, ready for implementation
**Next Action:** Implement `test_accuracy_sweep.py` and begin Phase 1
