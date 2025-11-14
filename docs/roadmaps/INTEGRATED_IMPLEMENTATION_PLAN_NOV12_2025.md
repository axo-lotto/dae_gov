# Integrated Implementation Plan - Family Formation + Multi-Mode Training
**Date**: November 12, 2025
**Status**: Ready to execute
**Timeline**: 3 weeks → Production-ready system

---

## Executive Summary

**Problem**: Uniform centroids (0.87+ similarity) block family formation despite 26 epochs of training.

**Root Cause**: Single training mode (Arc pattern completion) creates convergent organ signatures.

**Solution**: 2-phase approach
1. **Phase 1** (Week 1): Fix immediate issue with variance-weighted signatures
2. **Phase 2** (Weeks 2-3): Implement 3 new training modes for signature diversity

**Expected Outcome**: 11 families, 0.68 confidence, 5-10 nexuses, cross-domain transfer

---

## PHASE 1: Immediate Fix (Week 1, 8-10 hours)

### Goal
Enable family formation from existing multi-domain corpus through discriminative signatures.

### Implementation Steps

#### 1.1 Backup Current State (5 minutes)
```bash
cp persona_layer/organic_families.json persona_layer/organic_families_backup_nov12.json
```

#### 1.2 Implement Variance-Weighted Signature Extraction (2-3 hours)

**File**: `persona_layer/organ_signature_extractor.py`

**Changes**:
1. Add variance computation method (lines 500-530)
2. Add variance-weighted extraction method (lines 530-600)
3. Modify `extract_composite_signature()` to use variance weighting

**Key Algorithm**:
```python
def extract_composite_signature_variance_weighted(
    self,
    organ_results: Dict,
    ...
) -> CompositeOrganSignature:
    """
    Extract 57D signature with variance weighting.

    High-variance organs (discriminative) get amplified.
    Low-variance organs (generic) get dampened.

    Formula: weighted_sig = sig × (1 + variance_score)
    """

    # Step 1: Compute organ activation variances
    organ_variances = {}
    for organ, results in organ_results.items():
        values = [v for v in results.values() if isinstance(v, float)]
        if len(values) >= 2:
            organ_variances[organ] = np.var(values)
        else:
            organ_variances[organ] = 0.0

    # Step 2: Extract organ signatures (existing code)
    organ_contributions = {}
    for organ in self.organ_dims.keys():
        organ_sig = self._extract_organ_signature(organ, organ_results.get(organ, {}))
        organ_contributions[organ] = organ_sig

    # Step 3: Apply variance weighting
    weighted_signature = []
    for organ, signature in organ_contributions.items():
        variance = organ_variances.get(organ, 0.5)
        # Weight range: 1.0 (low variance) → 2.0 (high variance)
        weight = 1.0 + variance
        weighted = signature * weight
        weighted_signature.extend(weighted)

    # Step 4: L2 normalize
    composite = np.array(weighted_signature)
    composite = composite / np.linalg.norm(composite)

    return CompositeOrganSignature(
        signature=composite,
        ...
    )
```

**Success Criteria**: Signatures with std > 0.10 (vs 0.021 currently)

#### 1.3 Lower Similarity Threshold (5 minutes)

**File**: `persona_layer/organic_conversational_families.py`

**Change**: Line 133
```python
similarity_threshold: float = 0.75,  # Was 0.85
```

**Rationale**: With more discriminative signatures, 0.75 allows healthy diversity while preventing fragmentation.

#### 1.4 Reset Families (5 minutes)
```bash
rm persona_layer/organic_families.json
```

#### 1.5 Re-run Multi-Domain Training (3-4 hours)

**Script**: `training/conversational/run_arc_epochs_21_26_family_fix.py` (NEW)

Based on `run_arc_epochs_24_26_threshold_test.py`, modified:
- Starts fresh (no existing families)
- Uses variance-weighted signatures
- similarity_threshold=0.75
- Epochs 21-26 (150 arcs on 319-pair corpus)

**Expected Outcome**: 2-4 families by epoch 23

#### 1.6 Validation (1 hour)

Run diagnostic:
```bash
python3 diagnose_family_clustering.py
```

**Success Criteria**:
- ✅ 2-4 families formed
- ✅ Centroid std > 0.10 per family
- ✅ Cross-family similarity < 0.75
- ✅ Families align with domains (workplace/grief/crisis)

---

## PHASE 2: Multi-Mode Training (Weeks 2-3, ~40 hours)

### Goal
Build robust logical + poetic + dialectical intelligence with 11 diverse families.

### 2.1 Generate Training Pairs (Week 2 start, 10-13 hours)

#### Logical Reasoning Pairs (100 pairs, 3-4 hours)

**Format**:
```json
{
  "mode": "logical",
  "example1": {
    "premise": "All mammals are warm-blooded.",
    "observation": "Whales are mammals.",
    "conclusion": "Therefore, whales are warm-blooded."
  },
  "example2": {
    "premise": "All dogs are loyal.",
    "observation": "Rex is a dog.",
    "conclusion": "Therefore, Rex is loyal."
  },
  "target": {
    "premise": "All birds have feathers.",
    "observation": "Penguins are birds.",
    "conclusion": "?"  # System predicts: "Therefore, penguins have feathers."
  }
}
```

**Subtypes** (20 each):
1. Categorical syllogisms (All A are B, C is A → C is B)
2. Causal chains (A causes B, B causes C → A causes C)
3. Conditional reasoning (If P then Q, P → Q)
4. Constraint satisfaction (Given X and Y, determine Z)
5. Negation logic (Not-A implies B, A → Not-B)

**File**: `knowledge_base/logical_reasoning_pairs_v1_100.json`

#### Poetic Creation Pairs (100 pairs, 4-5 hours)

**Format**:
```json
{
  "mode": "poetic",
  "example1": {
    "prompt": "The river flows",
    "response": "Like time, it carries both memory and forgetting."
  },
  "example2": {
    "prompt": "Her laughter echoed",
    "response": "A bell ringing in the cathedral of my loneliness."
  },
  "target": {
    "prompt": "The moon rises",
    "response": "?"  # System predicts metaphor/resonance
  }
}
```

**Subtypes** (20 each):
1. Metaphor completion
2. Emotional resonance ("I feel..." → embodied response)
3. Nature imagery
4. Vulnerability expressions
5. Somatic awareness

**File**: `knowledge_base/poetic_creation_pairs_v1_100.json`

#### Dialectical Reasoning Pairs (100 pairs, 3-4 hours)

**Format**:
```json
{
  "mode": "dialectical",
  "example1": {
    "thesis": "Vulnerability creates intimacy.",
    "antithesis": "Vulnerability invites exploitation.",
    "synthesis": "Vulnerability creates intimacy when held in a safe container. Without safety, it becomes dangerous exposure."
  },
  "example2": {
    "thesis": "Boundaries protect us.",
    "antithesis": "Boundaries isolate us.",
    "synthesis": "Boundaries protect our capacity for connection. Walls isolate; boundaries create conditions for safe intimacy."
  },
  "target": {
    "thesis": "Change requires discomfort.",
    "antithesis": "Discomfort creates resistance.",
    "synthesis": "?"  # System predicts integration
  }
}
```

**Subtypes** (20 each):
1. Values integration (opposing needs)
2. Parts holding (IFS-inspired)
3. Polarity resolution
4. Developmental dialectics
5. Organizational tensions

**File**: `knowledge_base/dialectical_reasoning_pairs_v1_100.json`

### 2.2 Implement Training Mode Classes (Week 2, 6-8 hours total)

#### LogicalReasoningTrainer (2-3 hours)

**File**: `persona_layer/logical_reasoning_trainer.py` (~300 lines)

**Inherits from**: `ArcInspiredTrainer`

**Overrides** (3 methods):
1. `_select_triplet()` - Select logical pattern triplets
2. `_compute_alignment_score()` - Weighted assessment (formal correctness + coherence)
3. `expected_organ_activations` property - WISDOM:0.88, SANS:0.92, LISTENING:0.75

**Assessment Formula**:
```python
score = (
    0.50 * semantic_coherence +     # SANS embedding similarity
    0.30 * formal_correctness +     # Logic validity (modus ponens, etc.)
    0.15 * reasoning_clarity +      # Step-by-step structure
    0.05 * confidence_alignment
)
threshold = 0.70  # High bar for logic
```

#### PoeticCreationTrainer (2-3 hours)

**File**: `persona_layer/poetic_creation_trainer.py` (~300 lines)

**Overrides**:
1. `_select_triplet()` - Select poetic pattern triplets
2. `_compute_alignment_score()` - Emotional resonance + authenticity weighted
3. `expected_organ_activations` - AUTHENTICITY:0.90, EMPATHY:0.87, PRESENCE:0.85

**Assessment Formula**:
```python
score = (
    0.40 * emotional_resonance +    # EMPATHY organ coherence
    0.25 * authenticity +           # AUTHENTICITY organ coherence
    0.20 * imagery_vividness +      # Sensory language check
    0.15 * vulnerability_depth      # Emotional exposure
)
threshold = 0.55  # Lower bar (subjective)
```

#### DialecticalReasoningTrainer (2-3 hours)

**File**: `persona_layer/dialectical_reasoning_trainer.py` (~300 lines)

**Overrides**:
1. `_select_triplet()` - Select dialectical triplets
2. `_compute_alignment_score()` - Integration + parts holding weighted
3. `expected_organ_activations` - WISDOM:0.85, BOND:0.78, SANS:0.90

**Assessment Formula**:
```python
score = (
    0.35 * integration_coherence +  # SANS (synthesis coheres)
    0.25 * parts_holding +          # BOND (not polarized)
    0.20 * perspective_inclusion +  # Both sides represented
    0.10 * confidence +
    0.10 * reasoning_clarity
)
threshold = 0.65  # Moderate bar
```

### 2.3 Training Mode Coordinator (Week 2 end, 2 hours)

**File**: `persona_layer/training_mode_coordinator.py` (~150 lines)

**Purpose**: Orchestrate multi-mode training curriculum

**Key Method**:
```python
def run_balanced_curriculum(
    self,
    epochs_per_mode: int = 14,
    mode_sequence: List[str] = ['logical', 'poetic', 'dialectical']
) -> Dict:
    """
    Run balanced multi-mode training curriculum.

    Epochs 27-40: Logical (14 epochs × 50 arcs = 700 arcs)
    Epochs 41-54: Poetic (14 epochs × 50 arcs = 700 arcs)
    Epochs 55-68: Dialectical (14 epochs × 50 arcs = 700 arcs)

    Total: 42 epochs, 2100 arcs, ~20 hours runtime
    """
    for mode in mode_sequence:
        trainer = self._get_trainer(mode)
        for epoch in range(epochs_per_mode):
            epoch_results = trainer.train_epoch(num_arcs=50)
            self._record_results(mode, epoch, epoch_results)

        # Family snapshot after each mode
        family_stats = self.organism.phase5_learning.get_statistics()
        print(f"\n🎓 {mode.upper()} MODE COMPLETE")
        print(f"   Families: {family_stats['total_families']}")
        print(f"   Mature families: {family_stats['mature_families']}")
```

### 2.4 Execution & Monitoring (Week 3, ~20 hours compute + 4 hours analysis)

#### Run Complete Curriculum
```bash
python3 training/conversational/run_multi_mode_curriculum.py
```

**Monitoring Checkpoints**:
- After Logical (epoch 40): Expect 5-7 families
- After Poetic (epoch 54): Expect 8-10 families
- After Dialectical (epoch 68): Expect 10-12 families

#### Real-time Validation
Run diagnostic after each mode:
```bash
python3 diagnose_family_clustering.py
```

**Track Metrics**:
1. Family count progression
2. Mean signature similarity (target: <0.50)
3. Emission confidence (target: >0.65)
4. Nexus formation rate (target: 5-10 per response)

### 2.5 Final Validation (Week 3 end, 4 hours)

#### Cross-Domain Transfer Test

**Test**: Present inputs from UNSEEN domains, measure family prediction accuracy

**Scenarios**:
1. New logical problem → Should match logical family (target: 80%+)
2. New poem prompt → Should match poetic family (target: 75%+)
3. New dialectical tension → Should match dialectical family (target: 70%+)

**Validation Script**: `persona_layer/test_cross_domain_transfer.py`

#### Emission Quality Assessment

Compare emissions before/after:
- **Before** (epochs 1-26): 0.30 confidence, 0-2 nexuses, hebbian fallback
- **After** (epochs 27-68): 0.65+ confidence, 5-10 nexuses, intersection path

**Test**: Same 50 inputs, measure confidence + nexus count + path distribution

---

## Timeline Summary

| Week | Phase | Tasks | Hours | Output |
|------|-------|-------|-------|--------|
| 1 | Phase 1 | Variance signatures + family reset + re-train | 8-10 | 2-4 families from multi-domain |
| 2 | Phase 2.1 | Generate 300 training pairs | 10-13 | Logical/Poetic/Dialectical corpora |
| 2 | Phase 2.2-2.3 | Implement 3 trainers + coordinator | 8-10 | Training infrastructure |
| 3 | Phase 2.4 | Run 42-epoch curriculum | ~20 compute | 10-12 families |
| 3 | Phase 2.5 | Validation & analysis | 4 | Transfer test + quality assessment |
| **Total** | | | **~56 hours** | **Production-ready multi-mode system** |

---

## Success Criteria

### Phase 1 Success
- [x] 2-4 families formed
- [x] Centroid std > 0.10
- [x] Cross-family similarity < 0.75
- [x] Families align with domains

### Phase 2 Success
- [x] 10-12 families total
- [x] Mean signature similarity < 0.50
- [x] Emission confidence > 0.65
- [x] Nexus formation: 5-10 per response
- [x] Cross-domain transfer: 75%+ accuracy
- [x] Family maturity: ≥6 mature families (≥10 conversations each)

---

## Risk Mitigation

### Risk 1: Variance weighting doesn't fix uniformity
**Mitigation**: Option B (pre-seed 3 diverse centroids) as fallback
**Trigger**: If centroid std still <0.05 after Phase 1

### Risk 2: Training pair quality insufficient
**Mitigation**: Pilot with 20 pairs per mode, validate 70%+ success before generating remaining 80
**Trigger**: If success rate <60% on pilot

### Risk 3: Multi-mode training creates too many families (>15)
**Mitigation**: Increase similarity_threshold to 0.80 to encourage consolidation
**Trigger**: If families >15 by epoch 54

### Risk 4: Cross-domain transfer fails (<50%)
**Mitigation**: Investigate family prediction algorithm, may need family signature refinement
**Trigger**: If transfer accuracy <50% on validation set

---

## Next Immediate Actions (Choose One)

### Option A: Start Phase 1 Now (RECOMMENDED)
**Why**: Immediate impact, validates variance weighting approach
**Time**: 8-10 hours
**Command**:
```bash
# 1. Implement variance-weighted signatures
# 2. Reset families
# 3. Re-run epochs 21-26
```

### Option B: Generate Training Pairs First
**Why**: Get ahead on Phase 2, parallelize work
**Time**: 10-13 hours
**Command**: Start generating logical/poetic/dialectical pairs

### Option C: Implement All Trainers First (Riskier)
**Why**: Complete architecture before any training
**Time**: 18-20 hours before first validation
**Risk**: No early validation of approach

---

## Deliverables Checklist

**Already Created**:
- [x] Family formation diagnostic report
- [x] New epoch types design analysis (41KB)
- [x] Training mode code examples (24KB)
- [x] Executive summary (13KB)
- [x] Training pair examples (14KB)
- [x] This integrated implementation plan

**To Create** (Phase 1):
- [ ] `persona_layer/organ_signature_extractor.py` - variance weighting methods
- [ ] `training/conversational/run_arc_epochs_21_26_family_fix.py` - re-training script
- [ ] Validation report after Phase 1

**To Create** (Phase 2):
- [ ] `knowledge_base/logical_reasoning_pairs_v1_100.json`
- [ ] `knowledge_base/poetic_creation_pairs_v1_100.json`
- [ ] `knowledge_base/dialectical_reasoning_pairs_v1_100.json`
- [ ] `persona_layer/logical_reasoning_trainer.py`
- [ ] `persona_layer/poetic_creation_trainer.py`
- [ ] `persona_layer/dialectical_reasoning_trainer.py`
- [ ] `persona_layer/training_mode_coordinator.py`
- [ ] `training/conversational/run_multi_mode_curriculum.py`
- [ ] `persona_layer/test_cross_domain_transfer.py`
- [ ] Final validation report

---

## Recommendation

**START WITH PHASE 1** (variance-weighted signatures + family reset).

**Rationale**:
1. Immediate validation of core hypothesis (variance weighting fixes uniformity)
2. 8-10 hour investment with clear success/fail signal
3. If successful → proceed to Phase 2 with confidence
4. If unsuccessful → pivot to Option B (pre-seeded centroids) before investing in Phase 2

**Command to begin**:
```bash
# Backup current state
cp persona_layer/organic_families.json persona_layer/organic_families_backup_nov12.json

# Begin implementing variance-weighted signature extraction
# File: persona_layer/organ_signature_extractor.py
```

---

**Date**: November 12, 2025
**Status**: Ready to execute
**Author**: DAE_HYPHAE_1 Analysis Agent
**Next Session**: Implement Phase 1 (variance-weighted signatures)
