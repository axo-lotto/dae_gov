# Threshold Adjustment Strategy - Option A
## Lower Assessment Threshold to Enable More Learning

**Date:** November 12, 2025
**Status:** Ready to implement after epochs 15-17

---

## Current Situation

**Epoch 14 Results (threshold=0.65):**
- Success rate: 22% (11/50 arcs)
- Assessment distribution:
  - Good (≥0.65): 11 arcs (22%) → **LEARNED**
  - Partial (≥0.40): 39 arcs (78%) → **NOT LEARNED**
  - Poor (<0.40): 0 arcs (0%)

**Key Insight:** 78% of predictions are "partial" quality - better than poor, but below current threshold. These represent learning opportunities we're currently missing.

---

## Proposal: Lower Threshold to 0.50

### Rationale

1. **Semantic similarity is now accurate** (SANS embeddings)
   - Can trust scores in 0.50-0.65 range
   - These predictions show genuine semantic alignment

2. **Partial predictions have value**
   - Overall scores 0.40-0.65 indicate "partial match"
   - Organism captures some aspects of target response
   - Learning from these helps refine response patterns

3. **Conservative approach**
   - Start with 0.50 (mid-range of partial)
   - Can adjust up/down based on results

### Expected Impact

**With threshold=0.50:**

| Assessment | Score Range | Epoch 14 Count | Will Learn? | Learning Rate |
|------------|-------------|----------------|-------------|---------------|
| Excellent  | ≥0.85      | 0              | ✅ Yes      | 0% (0/50)     |
| Good       | ≥0.65      | 11             | ✅ Yes      | 22% (11/50)   |
| **Partial (high)** | **≥0.50** | **~25** | **✅ Yes (NEW)** | **~50% total** |
| Partial (low) | ≥0.40   | ~14            | ❌ No       | Not learned   |
| Poor       | <0.40      | 0              | ❌ No       | Not learned   |

**Predicted outcome:**
- Learning rate: 22% → **~50%** (2.3× increase)
- Predictions learned per epoch: 11 → **~25**
- Total training exposures: 133 → **175** (+32% increase)

---

## Implementation Plan

### Step 1: Update Threshold (1 minute)

**File:** `training/conversational/run_arc_epochs_18_20.py` (create new script)

```python
ASSESSMENT_THRESHOLD = 0.50  # Was 0.65
```

### Step 2: Run Epochs 18-20 (3 hours)

- 3 epochs × 50 arcs = 150 arcs
- Expected: ~75 predictions learned (vs 33 with 0.65 threshold)
- Monitor: Does quality degrade with lower threshold?

### Step 3: Analyze Results (30 minutes)

Compare epochs 18-20 (threshold=0.50) to epochs 15-17 (threshold=0.65):
- Success rate change
- Mean alignment score
- Response quality (manual inspection of learned predictions)

---

## Risk Assessment

### Potential Risks

1. **Learning from lower-quality predictions**
   - Risk: Organism learns suboptimal patterns
   - Mitigation: 0.50 is still above "poor" threshold (0.40)
   - Monitoring: Track if mean confidence decreases

2. **Diluting high-quality patterns**
   - Risk: More noise in training signal
   - Mitigation: Examples (always learned) provide strong signal
   - Monitoring: Compare epochs 18-20 to 15-17 quality

3. **Plateau without improvement**
   - Risk: More learning doesn't improve performance
   - Mitigation: Can revert to 0.65 if no benefit
   - Monitoring: Track success rate trajectory

### Mitigation Strategies

1. **Gradual approach:** Start with 0.50 (not 0.40)
2. **Limited scope:** Test for 3 epochs (18-20)
3. **Reversible:** Can return to 0.65 if quality degrades
4. **Monitored:** Compare results to baseline

---

## Success Criteria

**After epochs 18-20 (threshold=0.50), we expect:**

✅ **Criterion 1:** Learning rate increases
   - Target: 40-60% of predictions learned (vs 22%)

✅ **Criterion 2:** Quality maintained
   - Mean alignment score: ≥0.55 (within 0.05 of epochs 15-17)
   - No increase in "poor" assessments

✅ **Criterion 3:** Response diversity increases
   - More varied responses (not just "Here", "I'm listening")
   - Predictions match target output styles more closely

❌ **Failure criterion:** If quality degrades significantly
   - Mean alignment drops >0.10
   - Success rate decreases
   - → Revert to 0.65 threshold

---

## Alternative Thresholds

### Conservative (0.55):
- Learning rate: ~35% (vs 22%)
- Lower risk of quality degradation
- More incremental improvement

### Moderate (0.50):
- Learning rate: ~50% (vs 22%)
- **RECOMMENDED** - balanced risk/reward
- Still above "poor" threshold

### Aggressive (0.45):
- Learning rate: ~65% (vs 22%)
- Higher risk - includes some low-partial predictions
- Not recommended initially

---

## Execution Timeline

**After epochs 15-17 complete:**

1. **Hour 1:** Analyze epochs 15-17 results (baseline)
2. **Hour 2:** Create run_arc_epochs_18_20.py with threshold=0.50
3. **Hours 3-6:** Run epochs 18-20 (background)
4. **Hour 7:** Analyze and compare to epochs 15-17
5. **Decision:** Continue with 0.50, adjust, or revert

**Total time:** 7 hours (3 hours training + 4 hours setup/analysis)

---

## Code Changes Required

### New file: `training/conversational/run_arc_epochs_18_20.py`

```python
#!/usr/bin/env python3
"""
Arc Training Epochs 18-20 - Lowered Threshold Experiment
========================================================

Test lowering assessment threshold from 0.65 to 0.50 to enable
learning from "high-partial" predictions.

Expected: 2-3× increase in learning rate (22% → 50%)
"""

# ... (similar to run_arc_epochs_15_17.py)

ASSESSMENT_THRESHOLD = 0.50  # ⬅️ CHANGED from 0.65
START_EPOCH = 18
NUM_EPOCHS = 3

# ... rest of script
```

### No other changes needed!
- Arc trainer already supports threshold parameter
- All assessment logic already in place
- Just change the value and run

---

## Expected Outcomes Summary

| Metric | Epochs 15-17 (0.65) | Epochs 18-20 (0.50) | Change |
|--------|---------------------|---------------------|--------|
| **Learning rate** | 22% | 50% | +2.3× |
| **Predictions learned** | ~11/epoch | ~25/epoch | +14/epoch |
| **Total exposures** | ~133/epoch | ~175/epoch | +32% |
| **Mean alignment** | ~0.57 | ~0.55 | -0.02 (acceptable) |
| **Response diversity** | Low | Higher | Improvement expected |

---

## Rollback Plan

If results are unsatisfactory:

1. **Revert threshold** to 0.65 for epochs 21+
2. **Analyze** what went wrong (quality metrics, response patterns)
3. **Try alternative:**
   - Option B: Expand corpus (500-800 pairs)
   - Option C: Response length modulation
   - Combination approach

---

## Next Steps After Threshold Test

**If successful (recommended continuation):**
1. Keep threshold at 0.50 for epochs 21-25
2. Implement Option C (response length modulation)
3. Monitor for family discovery

**If partially successful:**
1. Adjust threshold to 0.55 (middle ground)
2. Run 3 more epochs to test
3. Decide on permanent threshold

**If unsuccessful:**
1. Revert to 0.65
2. Focus on Option B (corpus expansion) instead
3. Threshold may need higher-quality/more-diverse data

---

**Status:** Ready to implement
**Decision point:** After epochs 15-17 complete
**Timeline:** 7 hours total (3 training + 4 analysis)
**Risk level:** Low (reversible, monitored)
**Expected benefit:** 2-3× increase in learning rate
