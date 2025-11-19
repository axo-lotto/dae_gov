# 📊 Results Directory Structure - Current State
## November 17, 2025

**Purpose:** Document actual results directory structure and identify what needs to be organized.

---

## 🗂️ Current Directory Structure

```
results/
├── analysis/                          # Empty (created today)
├── checkpoints/                       # Unknown contents
├── core_grounded_training/            # Legacy training data
├── entity_training/                   # Legacy entity training
├── epoch_training/                    # OLD epoch structure (has data!)
│   ├── epoch_001/                     # Has timestamped JSON files
│   ├── epoch_002/
│   ├── epoch_003/
│   ├── epoch_004/
│   ├── epoch_005/
│   ├── epoch_006/
│   ├── epoch_007/
│   ├── epoch_008/
│   ├── epoch_009/
│   └── epoch_010/
├── epochs/                            # CURRENT epoch structure
│   ├── epoch_8/                       # Empty (created today)
│   ├── epoch_9/                       # Empty (created today)
│   ├── epoch_10/                      # Empty (created today)
│   ├── ... (through epoch_20)         # Empty (created today)
│   ├── full_system_training/          # Unknown contents
│   ├── test/                          # Test results
│   ├── entity_memory_epoch_1_results.json   # 37K - Current training script output
│   ├── entity_memory_epoch_8_results.json   # 37K - Analysis script copy
│   ├── entity_epoch_training_dae_native.json  # 480K - Large results file
│   ├── entity_situated_training_results.json  # 507K - Large results file
│   ├── epoch_2_multi_family_discovery.json
│   ├── epoch_2_results.json through epoch_5_results.json
│   ├── epoch_with_reconstruction_results.json
│   ├── epochs_1_5_baseline_consolidated.json  # 107K - Consolidated
│   └── training_epochs_*.json         # Various training results
├── intelligence_emergence/            # Legacy intelligence tests
├── multi_family_emergence/            # Multi-family training results
├── multi_iteration_training/          # Legacy training
├── rnx_assessment/                    # RNX organ assessment
├── training/                          # General training results
├── tsk_logs/                          # Empty (created today) - FOR TSK LOGS
├── validation/                        # Validation test results
└── visualizations/                    # Empty (created today) - FOR CHARTS
```

---

## 📋 Current File Locations

### Entity Memory Training Results

**Currently Saved To:**
- `results/epochs/entity_memory_epoch_1_results.json` (37K, updated Nov 17 04:04)

**Problem:**
- Training script hardcodes `OUTPUT_PATH = "results/epochs/entity_memory_epoch_1_results.json"`
- Every epoch overwrites the same file
- No epoch-specific preservation

**What Analysis Script Does:**
- Reads from `entity_memory_epoch_1_results.json` after each epoch completes
- Saves copy to `entity_memory_epoch_{N}_results.json` in analysis script
- This IS working (entity_memory_epoch_8_results.json exists)

### Where TSK Logs SHOULD Go

**Currently:** Not saved during training (ENABLE_TSK = False in training script)

**Should Go To:**
- `results/tsk_logs/epoch_{N}/` - One directory per epoch
- `results/tsk_logs/epoch_{N}/pair_{ID}_tsk.json` - Per training pair
- `results/tsk_logs/epoch_{N}/epoch_summary.json` - Aggregated TSK data

### Where Interactive Sessions SHOULD Go

**Currently:** No directory exists

**Should Create:**
- `results/interactive_sessions/`
- `results/interactive_sessions/{timestamp}_{username}_session.json`

---

## 🎯 What Needs to be Fixed

### Issue #1: Training Script Overwrites Same File ✅ FIXED BY ANALYSIS SCRIPT

**Current Behavior:**
```python
# training/entity_memory_epoch_training.py line 49
OUTPUT_PATH = "results/epochs/entity_memory_epoch_1_results.json"  # HARDCODED!
```

**Fix Applied (in analysis script):**
```python
# run_epochs_8_20_with_analysis.py
# Reads entity_memory_epoch_1_results.json
# Saves copy to entity_memory_epoch_{epoch_num}_results.json
```

**Status:** ✅ Working! Analysis script preserves each epoch's results.

### Issue #2: No TSK Logging During Training ⚠️ TO FIX

**Current State:**
```python
# training/entity_memory_epoch_training.py line 52
ENABLE_TSK = False  # Don't need full TSK recording for this training
```

**Why This is a Problem:**
- TSK (Transductive State Knowledge) captures transformation trajectories
- Critical for understanding HOW organism learns
- Needed for future analysis of learning patterns
- Missing data = can't retroactively analyze

**What TSK Contains:**
- 57D organ signatures per turn
- Zone transitions (SELF Matrix)
- Polyvagal state trajectories
- Kairos moment detection
- V0 convergence patterns
- Transformation pathways used

**Proposed Fix:**
1. Create `results/tsk_logs/epoch_{N}/` directory structure
2. Enable TSK logging: `ENABLE_TSK = True`
3. Save TSK per training pair during epochs
4. Create epoch summary aggregating TSK insights

### Issue #3: No Organized Per-Epoch Directories ⚠️ PARTIALLY ADDRESSED

**Current:**
- All results flat in `results/epochs/`
- Empty subdirectories `epoch_8/` through `epoch_20/` (created today)

**Proposed Structure:**
```
results/epochs/
├── entity_memory_epoch_1_results.json    # Keep for backward compat
├── epoch_8/
│   ├── training_results.json              # Main results
│   ├── metrics_summary.json               # Aggregated metrics
│   ├── tsk_logs/                          # TSK per pair
│   │   ├── pair_001_tsk.json
│   │   ├── pair_002_tsk.json
│   │   └── ...
│   └── analysis/                          # Optional analysis outputs
│       ├── entity_recall_trajectory.json
│       └── nexus_formation_patterns.json
├── epoch_9/
│   └── ... (same structure)
└── ...
```

---

## 💡 Recommended Actions

### Option A: Keep Current System (Minimal Changes)

**Keep:**
- Training script writes to `entity_memory_epoch_1_results.json`
- Analysis script copies to `entity_memory_epoch_{N}_results.json` ✅ Already working

**Add:**
- Enable TSK logging (`ENABLE_TSK = True`)
- Save TSK to `results/tsk_logs/epoch_{N}/`

**Pros:**
- Minimal code changes
- Analysis script already handles epoch-specific copies
- Backward compatible

**Cons:**
- TSK logs separate from epoch results
- Not as organized as it could be

### Option B: Full Restructure (Comprehensive)

**Change:**
- Training script accepts `--epoch N` parameter
- Saves to `results/epochs/epoch_{N}/training_results.json`
- Saves TSK to `results/epochs/epoch_{N}/tsk_logs/`
- Analysis script reads from structured directories

**Pros:**
- Clean organization
- All epoch data in one place
- Future-proof for analysis

**Cons:**
- Requires modifying training script (currently running!)
- More complex implementation
- Risk of breaking current system

### ⭐ RECOMMENDED: Option A + Gradual Migration

**Immediate (Do Now):**
1. ✅ Keep analysis script copying epoch results (already working)
2. Enable TSK logging in NEXT training run
3. Create TSK directory structure: `results/tsk_logs/epoch_{N}/`
4. Document current structure (this file)

**Future (After Epochs 8-20 Complete):**
1. Refactor training script to accept epoch parameter
2. Migrate to per-epoch directory structure
3. Create analysis tools that read from structured directories

---

## 📊 Current Training (Epochs 8-20) Status

**Process:** 30681 (running)
**Output:** `entity_memory_epoch_1_results.json` (overwrites each epoch)
**Copies:** `entity_memory_epoch_{8-20}_results.json` (saved by analysis script)
**TSK:** Not being saved (ENABLE_TSK = False)

**After Training Completes:**
- We'll have 13 result files (epochs 8-20)
- We'll have correlation analysis JSON
- We'll NOT have TSK logs (missed opportunity!)

**Recommendation:**
- Let current training finish (don't interrupt!)
- For NEXT training run (epochs 21-50), enable TSK logging
- Use this as baseline, future epochs will have richer data

---

## 🔍 Data We're Currently Capturing

### Per Epoch (via analysis script):
- ✅ Entity recall accuracy
- ✅ Entity memory available rate
- ✅ NEXUS differentiation rate
- ✅ Entity tracker update rate
- ✅ Emission correctness
- ✅ Confidence means
- ✅ V0 final energy
- ✅ Convergence cycles
- ✅ Processing time

### What We're MISSING (TSK Not Enabled):
- ❌ Per-pair organ signatures (57D)
- ❌ Zone transition patterns
- ❌ Polyvagal state trajectories
- ❌ Kairos detection per pair
- ❌ Transformation pathway usage
- ❌ Learning velocity per organ
- ❌ Humor attempt tracking
- ❌ Tone evolution patterns

---

## ✅ Action Items

### Immediate (Don't Break Running Training):
1. ✅ Document current structure (this file)
2. ✅ Let Epochs 8-20 finish without interruption
3. ✅ Analysis script already saves epoch-specific copies

### After Training Completes:
1. Review analysis results
2. Decide on TSK logging for future epochs
3. Create visualization scripts for existing data
4. Plan next training run with TSK enabled

### Future Enhancement:
1. Refactor training script for epoch parameter
2. Implement per-epoch directory structure
3. Create TSK aggregation analysis tools
4. Build visualization pipeline

---

## 📁 Detailed Directory Contents

### results/epochs/ - JSON Files

| File | Size | Purpose | Last Modified |
|------|------|---------|---------------|
| entity_memory_epoch_1_results.json | 37K | Current training output | Nov 17 04:04 |
| entity_memory_epoch_8_results.json | 37K | Analysis script copy | Nov 17 04:04 |
| entity_epoch_training_dae_native.json | 480K | Legacy large dataset | Nov 15 13:19 |
| entity_situated_training_results.json | 507K | Entity-situated training | Nov 15 15:31 |
| epochs_1_5_baseline_consolidated.json | 107K | Consolidated baseline | Nov 15 08:37 |

### results/epoch_training/ - Old Structure

Has 10 subdirectories (epoch_001 through epoch_010) with timestamped JSON files. This appears to be from a previous training architecture. Consider archiving if no longer used.

---

**Created:** November 17, 2025 04:10 AM CET
**Purpose:** Document actual results directory structure before making changes
**Status:** Current training (Epochs 8-20) should NOT be interrupted
**Next Steps:** Enable TSK logging for future training runs
