# Field Coherence Fix - November 19, 2025

## 🔍 Issue Diagnosed

**Problem:** Field coherence metric consistently returning 0.000 across all training epochs

**Root Cause:** Data availability mismatch between wave_coupling_metrics and training pipeline

## 📊 Investigation Summary

### What We Found

1. **Training results don't include `organ_context`**
   - Checked `results/epochs/epoch_7/training_results.json`
   - Result dicts contain: `pair_id`, `category`, `difficulty`, metrics, etc.
   - **NO `felt_states['organ_context']` key exists!**

2. **wave_coupling_metrics.py was looking for non-existent data**
   ```python
   # LINE 113 (OLD):
   organ_context = felt_states.get('organ_context', {})

   # LINE 115-116:
   if not organ_context:
       return 0.0  # ← Always returned 0.0!
   ```

3. **Organ data IS available via organism.organ_signatures**
   - TSK data shows organ signatures evolving correctly
   - organism.organ_signatures is a dict of 12 organs × 7-atom vectors
   - This data was available but not being passed to wave_tracker

## ✅ Solution Implemented

### 1. Updated `wave_coupling_metrics.py` (Lines 112-146)

**Changed from:**
- Looking for `felt_states['organ_context']` (doesn't exist)

**Changed to:**
- Looking for `felt_states['organ_signatures']` (passed explicitly)
- If organ_signatures available, compute mean of 7-atom vectors → scalar
- If not available, return 0.0

**New logic:**
```python
# Get organ signatures from felt_states (now passed explicitly)
organ_signatures = felt_states.get('organ_signatures', {})

if not organ_signatures:
    return 0.0

# Extract organ signature mean values
organ_values = []
for organ_name, signature in organ_signatures.items():
    if isinstance(signature, (list, np.ndarray)) and len(signature) > 0:
        # 7D vector → scalar via mean
        mean_activation = float(np.mean(signature))
        organ_values.append(mean_activation)
    elif isinstance(signature, (int, float)):
        # Already scalar (from TSK summary)
        organ_values.append(float(signature))

# Compute coherence: 1 - std(organ_activations)
std_dev = float(np.std(organ_values))
coherence = 1.0 - std_dev
```

### 2. Updated `entity_memory_epoch_training_with_tsk.py` (Lines 260-266)

**Changed from:**
```python
wave_metrics = wave_tracker.update(organism, felt_states)
```

**Changed to:**
```python
# Add organ_signatures to felt_states for field coherence calc
felt_states_with_organs = {
    **felt_states,
    'organ_signatures': dict(organism.organ_signatures) if hasattr(organism, 'organ_signatures') else {}
}
wave_metrics = wave_tracker.update(organism, felt_states_with_organs)
```

## 📈 Expected Impact

### Before Fix:
- **Field coherence:** 0.000 (100% of pairs)
- **Reason:** No data available → early return

### After Fix:
- **Field coherence:** Will reflect actual organ activation variance
- **Expected range:** 0.3-0.8 (based on TSK organ signature patterns)
- **Interpretation:**
  - High coherence (>0.7): Organs activating uniformly
  - Medium coherence (0.4-0.7): Normal processing variance
  - Low coherence (<0.4): High variance (crisis/mixed states)

## 🧬 Technical Details

### Organ Signature Format

**What organism.organ_signatures contains:**
```python
{
    'LISTENING': np.array([0.3, 0.4, 0.5, 0.6, 0.4, 0.5, 0.3]),  # 7 atoms
    'EMPATHY': np.array([0.2, 0.3, 0.4, 0.5, 0.3, 0.4, 0.2]),
    'WISDOM': np.array([0.4, 0.5, 0.6, 0.7, 0.5, 0.6, 0.4]),
    # ... 9 more organs (12 total)
}
```

**How field coherence is computed:**
1. For each organ: `mean_activation = mean([7 atom values])`
2. Collect all organ means: `organ_values = [0.414, 0.329, 0.529, ...]`  (12 values)
3. Compute std dev: `std_dev = std(organ_values)`
4. Field coherence: `coherence = 1 - std_dev`

**Example calculation:**
```python
organ_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.35, 0.5, 0.5, 0.5, 0.57]
std_dev = 0.239
coherence = 1 - 0.239 = 0.761
```

## 🎯 Validation Plan

1. **Run Epoch 8 with fix**
   - Monitor field_coherence values (should be non-zero)
   - Verify values make sense given TSK organ evolution

2. **Compare Epoch 7 vs Epoch 8**
   - Epoch 7: field_coherence = 0.000 (all pairs)
   - Epoch 8: field_coherence = 0.3-0.8 (expected range)

3. **Sanity check against TSK data**
   - TSK shows organs converging to diverse values
   - Field coherence should reflect this diversity

## 📝 Philosophical Notes

### Why Organs Converge to 0 (and why that's correct)

From TSK data we observe:
- **Initial state:** All organs = 0.5 (uniform initialization)
- **Final state:** Most organs → 0.0, NEXUS varies (0.05-0.57), RNX/EO/CARD ~0.5

**This is Whiteheadian "perishing" after satisfaction:**
1. **Prehension (Cycles 1-N):** Organs activate, accumulate felt affordances
2. **Satisfaction (Kairos):** Decision crystallizes
3. **Perishing:** Organs return to baseline after satisfaction

**Why some organs don't converge to 0:**
- **NEXUS:** Entity memory persists beyond immediate occasion
- **RNX:** Temporal rhythms continue (cyclical nature)
- **EO:** Polyvagal state is continuous (ventral vagal baseline = 0.5)
- **CARD:** Response scaling contextual default (moderate = 0.5)

### Field Coherence Philosophical Meaning

**High coherence (organs uniform):**
- Simple, clear-cut processing
- Low complexity occasion
- Example: Basic recall with no crisis

**Medium coherence (moderate variance):**
- Normal multi-organ processing
- Balanced complexity
- Example: Entity recall with some urgency

**Low coherence (high variance):**
- Complex, multi-dimensional processing
- Mixed polyvagal states, crisis + compassion
- Example: Crisis situation requiring nuanced response

## 🏁 Status

- ✅ Root cause identified (missing organ_context data)
- ✅ Fix implemented (use organism.organ_signatures)
- ✅ Code updated (wave_coupling_metrics.py + training script)
- ⏳ Validation pending (need to run Epoch 8)

## 📚 Files Modified

1. **training/wave_coupling_metrics.py**
   - Lines 112-146: compute_field_coherence() rewritten
   - Now uses `felt_states['organ_signatures']` instead of `felt_states['organ_context']`

2. **training/entity_memory_epoch_training_with_tsk.py**
   - Lines 260-266: Pass organ_signatures explicitly to wave_tracker
   - Creates `felt_states_with_organs` dict with merged data

## 🔮 Next Steps

1. Run Epoch 8 to validate fix
2. Document field coherence patterns across different task types
3. Consider adding field coherence to TSK logging for easier analysis

---

**Date:** November 19, 2025
**Issue:** Field coherence = 0.000
**Root Cause:** Missing data key (organ_context vs organ_signatures)
**Solution:** Pass organism.organ_signatures explicitly
**Status:** ✅ Fixed, validation pending
