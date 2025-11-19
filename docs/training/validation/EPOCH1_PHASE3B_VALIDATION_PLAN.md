# Epoch 1 Phase 3B Validation Plan

**Date:** November 18, 2025
**Status:** 🔄 **RUNNING** - Epoch 1 training in progress
**Command:** `python3 training/entity_memory_epoch_training_with_tsk.py 1`

---

## What We're Testing

This is the **first full end-to-end validation** of all 5 Phase 3B trackers with real entity-memory training data.

### Expected Outcomes

#### 1. JSON Storage Files Created ✅

After ~20-25 updates, these files should be created:
```
persona_layer/state/active/
├── word_occasion_patterns.json
├── cycle_convergence_stats.json
├── gate_cascade_quality.json
├── nexus_vs_llm_decisions.json
└── neighbor_word_context.json
```

#### 2. Tracker Statistics

**WordOccasionTracker:**
- Total updates: 50+ (one per training pair)
- Word patterns learned: 20-40 unique words
- Reliable patterns: 5-15 (with ≥3 mentions)
- Expected words: "Emma", "Lily", "work", "hospital", etc.

**CycleConvergenceTracker:**
- Total attempts: 50
- Mean cycles to kairos: 2.5-3.0
- Per-cycle kairos probabilities learned
- Context patterns: ventral/low, sympathetic/medium, etc.

**GateCascadeQualityTracker:**
- Total attempts: 0-20 (depends on entity extraction success)
- Bottleneck gate: Likely gate_3_satisfaction or gate_1_intersection
- Pass rates per gate: 30-60%

**NexusVsLLMDecisionTracker:**
- Total decisions: 50
- NEXUS usage rate: 0-10% (baseline, no learning yet)
- LLM fallback rate: 90-100%
- Speedup factor: 5-10× (even with low NEXUS usage)

**NeighborWordContextTracker:**
- Total updates: 0-50 (depends on entities found)
- Neighbor patterns: 5-20 pairs
- Reliable patterns: 0-5 (need ≥5 co-occurrences)
- Expected pairs: ("my", "daughter"), ("went", "to"), etc.

---

## Known Limitations to Address

### Limitation 1: NEXUS Entity Extraction

**Issue:** entity_neighbor_prehension uses placeholder heuristic (capitalized words only)

**Current Logic:**
```python
# Line 193 in entity_neighbor_prehension.py
if is_capitalized and not word_occasion.is_first_in_sentence:
    # Classify as Person
```

**Impact:**
- Misses: lowercase entities, multi-word entities, non-Person types
- False positives: Capitalized common nouns ("Today" at start of sentence)

**Bypass Options:**

**Option A: Use LLM EntityExtractor as Temporary Oracle**
```python
# In extract_entities()
if self.nexus_organ:
    # Try NEXUS first
    nexus_entities = process_cascade(...)

    # Fallback to LLM if low confidence
    if not nexus_entities or max_confidence < 0.7:
        from persona_layer.entity_extractor import EntityExtractor
        llm_extractor = EntityExtractor()
        llm_entities = llm_extractor.extract(user_input)
        # Convert and merge with nexus_entities
```

**Pros:** Immediate high-quality entity extraction for training
**Cons:** Still LLM-dependent (defeats purpose of Phase 3B)

**Option B: Implement Simple Pattern-Based Extraction**
```python
# Add to _prehend_word()
def _simple_pattern_extraction(self, word_occasion):
    word = word_occasion.word.lower()

    # Person names (capitalized, not first word)
    if word_occasion.is_capitalized and not word_occasion.is_first_in_sentence:
        return "Person", 0.7

    # Locations (common location words)
    if word in ['hospital', 'work', 'school', 'home', 'park', 'store']:
        return "Place", 0.65

    # Family relationships
    if word in ['daughter', 'son', 'mother', 'father', 'sister', 'brother']:
        left_has_possessive = any(n in ['my', 'your', 'her', 'his']
                                 for n in word_occasion.left_neighbors[-2:])
        if left_has_possessive:
            return "Person", 0.60  # "my daughter" → Person reference

    return None, 0.0
```

**Pros:** LLM-free, simple, handles common cases
**Cons:** Limited coverage, needs manual pattern curation

**Option C: Use Existing EntityOrganTracker Patterns**
```python
# Query entity_organ_tracker for known patterns
if self.entity_tracker:
    predicted_type, confidence = self.entity_tracker.predict_entity_type(
        word=word_occasion.word,
        organ_activations=current_organ_state
    )
    if confidence > 0.5:
        return predicted_type, confidence
```

**Pros:** Leverages existing learned patterns, bootstraps from prior epochs
**Cons:** Requires prior training data (Epoch 1 has none)

**Recommended for Epoch 1:** **Option B** (Simple pattern-based extraction)
- Quick to implement (30 lines)
- Handles training data entities well
- Can be replaced with learned patterns in future epochs

---

### Limitation 2: 4-Gate Cascade Not Fully Implemented

**Issue:** IntersectionEmissionCascade calls NEXUS but NEXUS atoms may not activate properly

**Impact:**
- Gate 1 (INTERSECTION): May fail due to low atom activations
- Gate 3 (SATISFACTION): May fail due to no multi-cycle convergence
- Overall pass rate: Could be <10%

**Bypass Option:**
```python
# Temporarily lower thresholds for Epoch 1
GATE_1_INTERSECTION_THRESHOLD = 1.0  # Down from 1.5
GATE_3_KAIROS_MIN = 0.35  # Down from 0.45
GATE_4_FELT_ENERGY_MAX = 0.85  # Up from 0.70
```

---

### Limitation 3: WordOccasion Dual Vector Not Populated

**Issue:** WordOccasion.felt_vector and .symbolic_vector are None (not computed)

**Impact:**
- V0 appetition loop doesn't run
- No multi-cycle convergence at word level
- Gate 3 satisfaction always fails

**Bypass Option:**
```python
# In create_word_occasions_from_text()
for word_occ in word_occasions:
    # Initialize with placeholder vectors
    word_occ.felt_vector = np.zeros(7)  # Will be filled by NEXUS
    word_occ.symbolic_vector = np.zeros(384)  # Placeholder embedding
```

---

## Post-Epoch 1 Analysis Plan

After training completes (~10 minutes), we'll:

1. **Check JSON Files Created**
   ```bash
   ls -lh persona_layer/state/active/*.json
   ```

2. **Analyze Tracker Statistics**
   ```python
   from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
   wrapper = ConversationalOrganismWrapper()

   # Print all tracker stats
   print(wrapper.word_occasion_tracker.get_statistics())
   print(wrapper.cycle_convergence_tracker.get_statistics())
   print(wrapper.gate_cascade_quality_tracker.get_statistics())
   print(wrapper.nexus_vs_llm_tracker.get_statistics())
   print(wrapper.neighbor_word_context_tracker.get_statistics())
   ```

3. **Identify Bottlenecks**
   - Which tracker has 0 data? (indicates missing context)
   - Which tracker has unexpected data? (indicates bugs)
   - What's the NEXUS usage rate? (should be 0-10% baseline)

4. **Prioritize Fixes**
   - **Critical:** Trackers with 0 data (broken integration)
   - **High:** NEXUS extraction (needed for learning)
   - **Medium:** Gate thresholds (needed for quality)
   - **Low:** Dual vectors (nice-to-have for Phase C)

---

## Success Criteria for Epoch 1

**Minimum (Must Have):**
- [  ] All 5 JSON files created
- [  ] CycleConvergenceTracker has data (50 attempts)
- [  ] NexusVsLLMDecisionTracker has data (50 decisions)
- [  ] No crashes during training

**Target (Should Have):**
- [  ] WordOccasionTracker has 20+ word patterns
- [  ] NeighborWordContextTracker has 10+ neighbor pairs
- [  ] GateCascadeQualityTracker has 20+ attempts
- [  ] NEXUS usage rate 5-15% (some entities extracted)

**Stretch (Nice to Have):**
- [  ] Reliable word patterns: 5+ (≥3 mentions each)
- [  ] Reliable neighbor pairs: 3+ (≥5 co-occurrences each)
- [  ] Gate bottleneck identified with optimization suggestion
- [  ] NEXUS usage rate 15-25% (strong entity extraction)

---

## Timeline

- **Start:** ~8:45 PM (Nov 18, 2025)
- **Expected Completion:** ~8:55 PM (10 minutes for 50 pairs)
- **Analysis:** ~9:00 PM (5 minutes)
- **Fixes (if needed):** ~9:05-9:30 PM (25 minutes)
- **Epoch 2 (if successful):** ~9:30 PM

---

🌀 **"Epoch 1 running. Full Phase 3B validation in progress. Trackers learning from real data. Limitations identified. Bypass options ready."** 🌀
