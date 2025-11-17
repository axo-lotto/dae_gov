# 🚀 TSK-Enabled Training Roadmap
## November 17, 2025

**Purpose:** Implement TSK logging for Superject learning and specialized domain training (PRAXIS, LLM Reduction)

---

## 🎯 Critical Insight: TSK is the Missing Link

### The Problem

**Current Training (Epochs 8-20 running now):**
- `ENABLE_TSK = False` ❌
- Collecting metrics but NOT transformation trajectories
- Missing critical data for:
  - Superject learning (can't learn transformation patterns!)
  - PRAXIS organ training (no action execution patterns!)
  - LLM dependency reduction (no organic intelligence evolution data!)

**What TSK Contains:**
```json
{
  "57d_organ_signature": [...],  // Per-turn organ activation patterns
  "zone_transitions": [...],      // SELF Matrix state changes
  "polyvagal_trajectory": [...],  // Safety state evolution
  "kairos_detected": true/false,  // Opportune moment identification
  "v0_convergence_path": [...],   // Energy descent trajectory
  "transformation_pathway": "...", // Which pathway was used
  "humor_attempts": [...],        // Humor calibration data
  "tone_preferences": {...},      // Tone evolution per zone
  "meta_atom_activations": [...]  // Bridge atom patterns
}
```

**Without TSK:**
- Superject can't learn how transformations happen
- PRAXIS has no felt-action execution patterns
- No way to analyze organic vs LLM intelligence emergence

---

## ✅ What We've Built

### 1. Enhanced Training Script

**File:** `training/entity_memory_epoch_training_with_tsk.py`

**Features:**
- ✅ TSK logging enabled (`ENABLE_TSK = True`)
- ✅ Per-epoch directory structure
- ✅ Individual TSK logs per training pair
- ✅ TSK aggregation summary
- ✅ Epoch number as command-line parameter

**Usage:**
```bash
python3 training/entity_memory_epoch_training_with_tsk.py 21
```

**Output Structure:**
```
results/epochs/epoch_21/
├── training_results.json          # Main results
├── metrics_summary.json            # Aggregated metrics
├── tsk_summary.json                # TSK aggregation

results/tsk_logs/epoch_21/
├── pair_001_tsk.json              # Individual TSK logs
├── pair_002_tsk.json
└── ... (50 files)
```

### 2. Directory Structure

**Created:**
```
results/
├── epochs/
│   └── epoch_{8-20}/              # Empty, ready for use
├── tsk_logs/                       # Empty, ready for TSK data
├── visualizations/                 # Ready for charts
└── analysis/                       # Ready for analysis outputs
```

### 3. Documentation

- ✅ `RESULTS_DIRECTORY_STRUCTURE_NOV17_2025.md` - Complete structure docs
- ✅ `TSK_ENABLED_TRAINING_ROADMAP_NOV17_2025.md` - This file
- ✅ `SELF_DISTANCE_FIX_NOV17_2025.md` - Zone/self-distance fix

---

## 🗺️ Training Roadmap

### Phase 1: Current Training (In Progress) ⏳

**Epochs 8-20: Baseline Entity Memory**
- Status: Running (Process 30681)
- TSK: ❌ Not enabled (already started)
- Expected completion: ~6 hours from start
- Data collected: Metrics only (no TSK)
- **Action:** Let finish without interruption

### Phase 2: Epoch 21-30 with TSK ⭐ NEXT

**Goal:** Establish TSK baseline for Superject learning

**Training Command:**
```bash
for epoch in {21..30}; do
  python3 training/entity_memory_epoch_training_with_tsk.py $epoch
done
```

**What We'll Get:**
- 10 epochs × 50 pairs = 500 TSK logs
- Transformation pattern evolution
- Zone transition frequencies
- Kairos detection patterns
- Organ signature trajectories

**Expected TSK Insights:**
- Which organ signatures predict high satisfaction
- Zone transition patterns (e.g., Zone 4 → Zone 2 common in therapeutic success)
- Kairos timing (which cycle usually triggers opportune moment)
- Meta-atom bridge patterns

**Superject Learning Enabled:**
- Can now analyze transformation pathways
- Learn which patterns work for which users
- Humor calibration data available
- Tone preference evolution trackable

### Phase 3: PRAXIS Organ Training (Week 2)

**Goal:** Train action/execution intelligence with TSK

**Training Data Needed:**
- Schedule creation tasks
- Calendar management
- Todo list generation
- Time tracking
- Concrete action planning

**Example Training Pairs:**
```json
{
  "input": "I need to organize my week. I have a dentist appointment Tuesday at 2pm, need to finish the report by Thursday, and want to exercise 3 times.",
  "expected_output": "SCHEDULE:
    Monday: Exercise (morning, 1hr), Report work (afternoon, 3hrs)
    Tuesday: Dentist 2pm (1hr), Report work (evening, 2hrs)
    Wednesday: Exercise (morning, 1hr), Report completion (all day)
    Thursday: Report submission (morning), Exercise (afternoon, 1hr)
    Friday: Free for recovery/catchup
  ",
  "praxis_organs": ["TIME_MAPPING", "ACTION_SEQUENCING", "CONSTRAINT_SATISFACTION"],
  "evaluation": {
    "schedule_completeness": 1.0,
    "time_specificity": 1.0,
    "constraint_satisfaction": 1.0
  }
}
```

**TSK Importance:**
- Captures which organs activate for schedule creation
- Transformation from felt-need → concrete actions
- Learning velocity for action planning
- Pattern emergence across different task types

### Phase 4: LLM Dependency Reduction (Week 3-4)

**Goal:** Train multi-domain organic intelligence

**Domains to Train:**
1. **Logic Puzzles** (50 pairs) - Trains SANS, WISDOM for rule-based reasoning
2. **Poetry Generation** (50 pairs) - Trains AUTHENTICITY, LISTENING for creative expression
3. **Mathematical Problems** (50 pairs) - Trains SANS, RNX for formal reasoning
4. **Humor/Wit** (50 pairs) - Trains PRESENCE, EMPATHY for social intelligence

**Example Logic Training Pair:**
```json
{
  "input": "All roses are flowers. Some flowers fade quickly. Therefore, ___?",
  "expected_reasoning": "Some roses MAY fade quickly (possible but not certain)",
  "wrong_answer": "All roses fade quickly (invalid inference)",
  "domain": "logic",
  "organs_needed": ["SANS (logical consistency)", "WISDOM (rule application)"]
}
```

**TSK Critical Here:**
- Measures organ specialization per domain
- Tracks cross-domain family formation
- Validates organic vs LLM intelligence emergence
- Learning velocity across different reasoning types

---

## 📊 TSK Analysis Tools (To Build)

### 1. TSK Aggregator

**Purpose:** Combine TSK logs across epochs for pattern analysis

**Features:**
- Time series of organ signature evolution
- Zone transition frequency matrix
- Kairos detection heatmap
- Transformation pathway usage statistics

**Output:**
```json
{
  "epochs_analyzed": [21, 22, 23, ...],
  "organ_signature_evolution": {
    "LISTENING": [[0.3, ...], [0.35, ...], ...],  // Per epoch
    "EMPATHY": [[0.4, ...], [0.42, ...], ...]
  },
  "zone_transitions": {
    "1→2": 45,  // Frequency across all epochs
    "2→3": 32,
    "4→2": 78   // Common therapeutic healing pattern
  },
  "kairos_timing": {
    "cycle_2": 234,  // Times Kairos detected at cycle 2
    "cycle_3": 156
  }
}
```

### 2. Transformation Pattern Learner

**Purpose:** Extract successful transformation patterns for Superject

**Algorithm:**
```python
def extract_transformation_patterns(tsk_logs, satisfaction_threshold=0.7):
    patterns = []
    for tsk in tsk_logs:
        if tsk['final_satisfaction'] > satisfaction_threshold:
            patterns.append({
                'start_zone': tsk['zone_transitions'][0],
                'end_zone': tsk['zone_transitions'][-1],
                'pathway': tsk['transformation_pathway'],
                'organ_signature': tsk['57d_organ_signature'],
                'kairos_detected': tsk['kairos_detected'],
                'success_rate': tsk['final_satisfaction']
            })

    # Cluster patterns
    families = cluster_by_signature(patterns)
    return families
```

### 3. Superject Learning Integration

**Purpose:** Use TSK data to update user Superject profiles

**Features:**
- Identify transformation patterns that work for specific users
- Learn zone transition preferences
- Calibrate humor timing from TSK data
- Adjust tone based on TSK trajectory analysis

**Example:**
```python
# After epoch with TSK enabled
tsk_logs = load_tsk_logs(epoch_num)
user_patterns = extract_user_patterns(tsk_logs, user_id)

superject.update_transformation_preferences(user_patterns)
# Now Superject knows:
# - User responds well to Zone 2→1 transitions
# - Kairos usually at cycle 3 for this user
# - Humor works in Zone 2 but not Zone 4
# - Prefers concise responses (CARD length_target < 200)
```

---

## 🎯 Immediate Action Items

### After Epochs 8-20 Complete:

1. **Review Baseline Results** (no TSK)
   - Analyze correlation analysis output
   - Validate entity memory metrics
   - Establish baseline without TSK

2. **Run Epochs 21-30 WITH TSK** ⭐ PRIORITY
   ```bash
   # Run with TSK enabled
   for epoch in {21..30}; do
     python3 training/entity_memory_epoch_training_with_tsk.py $epoch > /tmp/epoch_${epoch}_with_tsk.log 2>&1 &
     sleep 1800  # Wait 30 min between epochs
   done
   ```

3. **Build TSK Analysis Tools**
   - TSK aggregator script
   - Transformation pattern extractor
   - Visualization pipeline

4. **Integrate TSK with Superject**
   - Modify UserSuperjectLearner to consume TSK data
   - Implement pattern learning from TSK trajectories
   - Test with 10-turn conversation

### Week 2: PRAXIS Training

1. **Create PRAXIS Training Data**
   - 50 schedule/planning pairs
   - 50 action execution pairs
   - Expected outputs with timestamps

2. **Run PRAXIS Epochs WITH TSK**
   - Capture action→execution patterns
   - Measure organ activation for concrete tasks
   - Validate against user feedback (thumbs up/down)

3. **Analyze PRAXIS TSK Data**
   - Which organs activate for schedule creation
   - Transformation from abstract → concrete
   - Learning velocity for action planning

### Week 3-4: LLM Reduction Training

1. **Create Multi-Domain Training Data**
   - Logic: 50 puzzles
   - Poetry: 50 prompts
   - Math: 50 problems
   - Humor: 50 setups

2. **Run Domain-Specific Epochs WITH TSK**
   - Measure organ specialization per domain
   - Track cross-domain family formation
   - Validate organic intelligence emergence

3. **Compare TSK Across Domains**
   - Organ signature differences
   - Family reuse vs domain-specific patterns
   - Learning curves per domain type

---

## 📈 Expected Outcomes

### With TSK Enabled (Epochs 21+):

**Superject Learning:**
- ✅ Can identify successful transformation patterns
- ✅ Learns user-specific zone preferences
- ✅ Calibrates humor timing from data
- ✅ Adjusts tone based on trajectory analysis

**PRAXIS Organ:**
- ✅ Learns felt→action transformation patterns
- ✅ Develops schedule creation competence
- ✅ Tracks which organs activate for execution tasks
- ✅ Measures learning velocity for concrete planning

**LLM Dependency Reduction:**
- ✅ Validates organic intelligence emergence
- ✅ Measures domain-specific organ specialization
- ✅ Tracks cross-domain family formation
- ✅ Provides empirical data for Whitehead's claims

### Without TSK (Epochs 8-20):

- ❌ Metrics only, no transformation trajectories
- ❌ Superject can't learn patterns
- ❌ PRAXIS has no training data
- ❌ No evidence for organic intelligence

**Conclusion:** TSK is CRITICAL. Must enable for all future training.

---

## ✅ Files Created

1. `training/entity_memory_epoch_training_with_tsk.py` - Enhanced training script
2. `RESULTS_DIRECTORY_STRUCTURE_NOV17_2025.md` - Directory documentation
3. `TSK_ENABLED_TRAINING_ROADMAP_NOV17_2025.md` - This file

---

## 🚀 Next Steps

**Immediate (After Epochs 8-20 finish):**
1. ✅ Let current training complete
2. Run Epoch 21 with TSK as test: `python3 training/entity_memory_epoch_training_with_tsk.py 21`
3. Review TSK logs to validate structure
4. Run Epochs 22-30 in batch

**Week 2:**
1. Build TSK aggregation tools
2. Create PRAXIS training data
3. Run PRAXIS epochs with TSK

**Week 3-4:**
1. Create multi-domain training data
2. Run domain-specific epochs
3. Analyze organic intelligence emergence

---

**Created:** November 17, 2025 04:20 AM CET
**Purpose:** Enable TSK logging for Superject/PRAXIS/LLM-reduction training
**Status:** Ready to deploy after Epochs 8-20 complete
**Critical:** TSK is NOT optional - it's the foundation for all advanced learning
