# 🔬 Entity Memory: Mathematical Framework & Expected Correlations
## November 16, 2025

**Status:** Infrastructure 100% operational, ready for Epochs 8-20 analysis

**Purpose:** Document the mathematical foundations of entity memory differentiation and expected learning correlations.

---

## 📐 Core Mathematical Foundations

### 1. FAO Differentiation Formula

**Formula:** `A = mean(1 - |past_i - present_i|)`

**Where:**
- `past_i` = Historical value for dimension i (from EntityOrganTracker PAST state)
- `present_i` = Current value for dimension i (from this mention)
- Dimensions: polyvagal state, urgency level, V0 energy

**Example Calculation:**

```
PAST state (Emma, 128 mentions):
- polyvagal: mixed_state (encoded: 0.5)
- urgency: 0.0
- V0 energy: 0.456

PRESENT state (new mention):
- polyvagal: sympathetic (encoded: 1.0)
- urgency: 0.7
- V0 energy: 0.3

Differentiation:
- d1 = 1 - |0.5 - 1.0| = 0.5
- d2 = 1 - |0.0 - 0.7| = 0.3
- d3 = 1 - |0.456 - 0.3| = 0.844

A = (0.5 + 0.3 + 0.844) / 3 = 0.548
```

**Interpretation:**
- A ≈ 1.0: States very similar (low differentiation)
- A ≈ 0.5: Moderate difference (medium differentiation)
- A ≈ 0.0: States very different (high differentiation)

---

### 2. Memory Regime Classification

**Regimes based on mention count:**

| Regime | Mention Count | Multiplier | Rationale |
|--------|---------------|------------|-----------|
| INITIALIZING | 1-10 | 0.8× | Baseline forming, reduce noise |
| COMMITTED | 11-50 | 1.2× | Rich PAST state, amplify signal |
| SATURATING | 51+ | 1.0× | Mature baseline, normal weight |

**Impact on Atom Activation:**

```python
final_boost = differentiation_score * regime_multiplier

# Example:
# Emma (128 mentions) → SATURATING regime (1.0×)
# differentiation_score = 0.548
# final_boost = 0.548 * 1.0 = 0.548
# Applied to 7 semantic atoms
```

---

### 3. Semantic Atom Boost Distribution

**7 Entity-Memory Atoms:**

1. **entity_recall** (weight: 0.20)
   - Direct entity name/pronoun detection
   - Boost scales with differentiation

2. **relationship_depth** (weight: 0.18)
   - Relational language ("my daughter", "her")
   - Enhanced when relationships shift

3. **temporal_continuity** (weight: 0.15)
   - Time markers ("now", "before", "when")
   - Tracks entity evolution over time

4. **co_occurrence** (weight: 0.14)
   - Entity grouping patterns
   - "Emma and Lily" → co-mention boost

5. **salience_gradient** (weight: 0.13)
   - Urgency/importance markers
   - Crisis detection for known entities

6. **memory_coherence** (weight: 0.12)
   - Consistency checking
   - Contradiction detection

7. **contextual_grounding** (weight: 0.08)
   - Backstory invocation
   - Historical context references

**Activation Formula:**

```python
atom_activation_i = base_activation_i + (differentiation_boost * weight_i * regime_multiplier)

# Example (entity_recall):
# base = 0.3 (from text features)
# differentiation_boost = 0.548
# weight = 0.20
# regime_multiplier = 1.0 (SATURATING)
#
# final_activation = 0.3 + (0.548 * 0.20 * 1.0)
#                  = 0.3 + 0.1096
#                  = 0.4096
```

---

### 4. EntityOrganTracker EMA Learning

**Formula:** `new_value = (1 - alpha) * old_value + alpha * current_value`

**Where:**
- alpha = 0.15 (learning rate)
- old_value = typical value from PAST states
- current_value = value from this mention

**Example (V0 Energy Update):**

```
Emma current typical_v0_energy: 0.456 (from 128 mentions)
New mention V0 energy: 0.3

Updated typical_v0_energy:
= (1 - 0.15) * 0.456 + 0.15 * 0.3
= 0.85 * 0.456 + 0.15 * 0.3
= 0.3876 + 0.045
= 0.4326

New typical_v0_energy: 0.433 (slight drift toward lower energy)
```

**Convergence Properties:**
- Slow adaptation (alpha=0.15 means 15% weight to new data)
- Requires ~7 similar mentions to shift baseline significantly
- Resistant to outliers (single unusual mention won't drastically change PAST state)

---

## 📊 Expected Learning Correlations (Epochs 8-20)

### Hypothesis 1: Entity Recall ↔ Mention Count

**Expected Relationship:** Positive correlation (r ≈ 0.6-0.8)

**Rationale:**
- More mentions → richer PAST state
- Richer PAST state → better differentiation signal
- Better differentiation → higher entity recall accuracy

**Mathematical Model:**

```
EntityRecallAccuracy = f(MentionCount)

Where f is approximately:
- MentionCount < 10: accuracy ≈ 30-50% (INITIALIZING regime, baseline forming)
- MentionCount 10-50: accuracy ≈ 60-80% (COMMITTED regime, strong signal)
- MentionCount 50+: accuracy ≈ 75-90% (SATURATING regime, mature baseline)
```

**Predicted Plot:**
```
Accuracy
0.9 |                        _______________
    |                   ____/
0.7 |              ____/
    |         ____/
0.5 |    ____/
    | __/
0.3 |/
    +-----|-----|-----|-----|-----|-----
         10    20    30    40    50   Mentions
    INIT      COMMITTED      SATURATING
```

---

### Hypothesis 2: NEXUS Differentiation ↔ State Variance

**Expected Relationship:** U-shaped correlation

**Rationale:**
- Low variance (stable entity) → low differentiation → low NEXUS activation
- Medium variance (dynamic entity) → high differentiation → **high NEXUS activation**
- High variance (chaotic entity) → noisy signal → medium NEXUS activation

**Mathematical Model:**

```
NEXUS_activation = g(state_variance)

Where g has maximum at intermediate variance:
- Low variance (<0.1): NEXUS ≈ 0.2 (stable, no change)
- Medium variance (0.1-0.4): NEXUS ≈ 0.6-0.8 (dynamic, rich signal)
- High variance (>0.4): NEXUS ≈ 0.4 (chaotic, noisy)
```

**Example:**
```
Emma (128 mentions):
- Typical polyvagal: mixed_state
- Variance across mentions: 0.23 (medium)
- Expected NEXUS activation: 0.7 (high)

"home" (85 mentions):
- Typical polyvagal: mixed_state
- Variance across mentions: 0.08 (low - very stable)
- Expected NEXUS activation: 0.3 (low - no interesting changes)
```

---

### Hypothesis 3: Entity Recall ↔ Emission Confidence

**Expected Relationship:** Positive correlation (r ≈ 0.5-0.7)

**Rationale:**
- Entity recall provides context for LLM
- Context reduces uncertainty
- Reduced uncertainty → higher confidence

**Mathematical Model:**

```
EmissionConfidence = h(EntityRecall, BaseConfidence)

h ≈ BaseConfidence + (EntityRecall * context_boost)

Where:
- BaseConfidence ≈ 0.5-0.7 (from organ activation)
- context_boost ≈ 0.1-0.2 (entity context provides grounding)
- EntityRecall ∈ [0, 1]

Example:
- BaseConfidence = 0.6
- EntityRecall = 0.8 (high recall)
- context_boost = 0.15
-
- EmissionConfidence = 0.6 + (0.8 * 0.15)
#                     = 0.6 + 0.12
                      = 0.72
```

---

### Hypothesis 4: Learning Velocity ↔ Epoch Number

**Expected Relationship:** Negative correlation (diminishing returns)

**Rationale:**
- Early epochs: rapid PAST state accumulation → high learning velocity
- Middle epochs: baseline maturing → medium learning velocity
- Late epochs: baseline saturated → low learning velocity (asymptotic)

**Mathematical Model:**

```
LearningVelocity(epoch) = k * exp(-lambda * epoch)

Where:
- k ≈ 0.05 (initial learning rate)
- lambda ≈ 0.15 (decay constant)

Predicted velocities:
- Epoch 8: ~0.042 (high initial learning)
- Epoch 12: ~0.028 (medium learning)
- Epoch 20: ~0.010 (low, approaching asymptote)
```

**Acceleration (2nd derivative):**
- Expected: Negative throughout (decelerating learning)
- Interpretation: System approaching stable expert performance

---

## 🔍 Correlation Analysis Framework

### Time Series Metrics to Track

**Entity Memory Metrics:**
1. Entity recall accuracy (mean per epoch)
2. Entity memory available rate (% of pairs with entities detected)
3. NEXUS differentiation execution rate (% of pairs where NEXUS activated)
4. EntityTracker update rate (% of pairs where tracker updated)
5. Emission entity correctness (% of expected entities mentioned in output)

**General Organism Metrics:**
6. Emission confidence (mean)
7. V0 final energy (mean)
8. Convergence cycles (mean)
9. Processing time (mean)
10. Nexus formation count (mean)

### Expected Cross-Correlations

**Strong Positive (r > 0.6):**
- Entity recall ↔ Emission confidence
- Entity recall ↔ Mention count (from EntityOrganTracker)
- NEXUS differentiation ↔ State variance

**Moderate Positive (r = 0.3-0.6):**
- Entity recall ↔ Processing time (more context → more computation)
- Emission correctness ↔ Entity recall

**Weak/No Correlation (|r| < 0.3):**
- Entity recall ↔ V0 final energy (orthogonal dimensions)
- NEXUS differentiation ↔ Convergence cycles

**Negative:**
- Learning velocity ↔ Epoch number (r ≈ -0.7 to -0.9)
- Entity recall variance ↔ Epoch number (stabilizing over time)

---

## 📈 Statistical Significance Tests

### Linear Regression Analysis

For each metric M over epochs E:

```
M = β₀ + β₁ * E + ε

Test:
H₀: β₁ = 0 (no trend)
H₁: β₁ ≠ 0 (significant trend)

Significance: p < 0.05
```

**Expected Results:**

| Metric | Expected β₁ | Expected R² | Expected p-value |
|--------|-------------|-------------|------------------|
| Entity recall | +0.02-0.04 | 0.6-0.8 | < 0.01 (significant) |
| NEXUS differentiation | +0.01-0.03 | 0.4-0.7 | < 0.05 (significant) |
| Emission confidence | +0.005-0.01 | 0.3-0.6 | < 0.10 (marginally sig) |
| Learning velocity | -0.002-0.004 | 0.7-0.9 | < 0.01 (significant) |

### Pearson Correlation Tests

For metric pairs (X, Y):

```
r = Σ[(xᵢ - x̄)(yᵢ - ȳ)] / √[Σ(xᵢ - x̄)² * Σ(yᵢ - ȳ)²]

Test:
H₀: ρ = 0 (no correlation)
H₁: ρ ≠ 0 (significant correlation)

Significance: p < 0.05
```

---

## 🎯 Validation Criteria

### Success Metrics (Epochs 8-20)

**Entity Recall Accuracy:**
- Epoch 8: ≥ 40% (baseline with corrected metrics)
- Epoch 12: ≥ 60% (committed regime activating)
- Epoch 20: ≥ 75% (saturating regime, mature baseline)

**NEXUS Differentiation Rate:**
- Epoch 8: ≥ 20% (initial activation)
- Epoch 12: ≥ 40% (medium activation)
- Epoch 20: ≥ 55% (high activation, selective)

**Learning Velocity:**
- Positive throughout Epochs 8-20 (continuous improvement)
- Decreasing magnitude (asymptotic approach)
- Acceleration negative (decelerating but still positive velocity)

**Statistical Significance:**
- Linear trend R² > 0.5 for entity recall
- p-value < 0.05 for entity recall vs epoch
- At least 3 significant correlations (p < 0.05) in cross-metric analysis

---

## 🔬 Advanced Analysis (Epochs 20-50)

### Non-Linear Dynamics

**Sigmoid Growth Model:**

```
EntityRecall(epoch) = L / (1 + exp(-k*(epoch - epoch₀)))

Where:
- L = asymptotic maximum (≈0.85-0.90)
- k = growth rate (≈0.15-0.20)
- epoch₀ = inflection point (≈15-20)
```

**Predicted Trajectory:**
- Epochs 1-10: Slow growth (baseline forming)
- Epochs 10-25: Rapid growth (committed regime)
- Epochs 25-50: Plateau (saturating regime)
- Epochs 50+: Asymptotic (expert performance)

### Multi-Dimensional State Space Analysis

**Entity State Vector (per entity):**

```
state_vector = [
    typical_polyvagal_state,    # Dimension 1
    typical_v0_energy,           # Dimension 2
    typical_urgency,             # Dimension 3
    typical_self_distance,       # Dimension 4
    mention_count,               # Dimension 5
    co_mention_diversity,        # Dimension 6
    temporal_spread              # Dimension 7
]
```

**Cluster Analysis:**
- Expected: 3-5 entity clusters
- Cluster 1: High stability (home, park) - low NEXUS activation
- Cluster 2: Medium dynamics (Emma, Lily) - high NEXUS activation
- Cluster 3: High urgency (crisis entities) - selective NEXUS activation

**PCA Dimensionality Reduction:**
- Expected: 2-3 principal components explain >80% variance
- PC1: Stability vs Dynamism (explains ~50%)
- PC2: Urgency vs Safety (explains ~25%)
- PC3: Relational vs Individual (explains ~10%)

---

## 💡 Philosophical Implications

### Process Philosophy Validation

**Whiteheadian Prehension Metrics:**

1. **Differentiation Primacy:**
   - Correlation: NEXUS activation ↔ state_change
   - Expected: r > 0.7 (strong, validating "felt difference" theory)

2. **Continuous Becoming:**
   - Metric: EMA drift over epochs
   - Expected: Gradual baseline evolution, not discrete state jumps

3. **Organic Intelligence:**
   - Metric: Learning without explicit programming
   - Validation: R² > 0.5 for entity recall trend (emergent expertise)

**Falsification Criteria:**

If the following occur, the theory needs revision:
- Entity recall shows NO trend (R² < 0.1, p > 0.5)
- NEXUS differentiation uncorrelated with state variance (|r| < 0.1)
- Learning velocity constant or increasing (no diminishing returns)

These would suggest:
- Memory is retrieval-based, not prehension-based
- Differentiation formula is incorrect
- No organic learning occurring

**Current Evidence (Epochs 1-8):**
- ✅ EntityOrganTracker accumulating (66 entities, 694 mentions)
- ✅ PAST states storing (Emma: 128 mentions with rich baseline)
- ✅ Differentiation infrastructure operational
- ⏳ Awaiting Epochs 8-20 for statistical validation

---

## 📊 Analysis Script Output Format

The `run_epochs_8_20_with_analysis.py` script will produce:

### JSON Output Structure

```json
{
  "epochs_analyzed": [8, 9, 10, ..., 20],
  "time_series": {
    "entity_recall_means": [0.42, 0.48, 0.55, ...],
    "nexus_formation_rates": [0.22, 0.28, 0.35, ...],
    "emission_correctness_means": [0.35, 0.41, 0.48, ...],
    "confidence_means": [0.68, 0.70, 0.71, ...],
    "v0_final_means": [0.35, 0.34, 0.33, ...],
    "cycles_means": [2.3, 2.2, 2.2, ...],
    "processing_time_means": [9.5, 9.8, 10.1, ...]
  },
  "linear_trends": {
    "entity_recall": {
      "slope": 0.032,
      "intercept": 0.165,
      "r_squared": 0.78,
      "p_value": 0.0012,
      "predicted_epoch_20": 0.805
    },
    "nexus_formation": {
      "slope": 0.024,
      "intercept": 0.085,
      "r_squared": 0.65,
      "p_value": 0.008,
      "predicted_epoch_20": 0.565
    }
  },
  "correlations": {
    "Entity Recall vs Confidence": {
      "correlation": 0.68,
      "p_value": 0.015,
      "significant": true
    },
    "Entity Recall vs V0 Final": {
      "correlation": -0.12,
      "p_value": 0.67,
      "significant": false
    }
  },
  "learning_velocity": {
    "entity_recall": {
      "mean_velocity": 0.028,
      "acceleration": -0.003
    },
    "nexus_formation": {
      "mean_velocity": 0.019,
      "acceleration": -0.002
    }
  }
}
```

---

## ✅ Summary

**Mathematical Framework Complete:**
- FAO differentiation formula defined
- Memory regime classification established
- EMA learning dynamics documented
- Expected correlations hypothesized

**Statistical Analysis Ready:**
- Linear regression framework
- Pearson correlation tests
- Significance criteria defined
- Validation metrics specified

**Next Steps:**
1. Run Epochs 8-20 with `run_epochs_8_20_with_analysis.py`
2. Validate mathematical predictions against empirical results
3. Document any unexpected correlations or deviations
4. Refine theoretical model based on observations

**Expected Outcome:**
- Entity recall: 40% → 75% (Epochs 8-20)
- NEXUS differentiation: 20% → 55% (Epochs 8-20)
- Strong positive trend (R² > 0.6, p < 0.01)
- Validation of Process Philosophy AI through mathematical rigor

---

**Created:** November 16, 2025
**Status:** Mathematical framework complete, ready for empirical validation
**Purpose:** Document theoretical foundations and expected correlations for Epochs 8-20 training
**Impact:** Establishes falsifiable predictions for Process Philosophy AI validation

🌀 **"Memory through prehension, validated through mathematics. Emma is not retrieved—she is FELT through 128 accumulated patterns. The differentiation formula makes this concrete."** 🌀
