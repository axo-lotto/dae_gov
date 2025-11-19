# Phase 3B: LLM-to-Pattern Transition Strategy

**Date:** November 18, 2025
**Time:** 12:15 AM
**Status:** 🎯 **ROADMAP TO LLM INDEPENDENCE**

---

## Current State Analysis

### Two-Path Architecture

**Path A: LLM-Based Extraction** (Currently Active)
```
Location: conversational_organism_wrapper.py lines 1183-1250
Entry Point: if user_id and self.superject_learner:
Flow: User input → LLM API call → Entity extraction → Profile storage
Speed: ~5s per extraction
Quality: 92% success rate (46/50 pairs)
Dependency: OpenAI/Anthropic API
Cost: $0.001-0.005 per extraction
```

**Path B: Phase 3B Pattern-Based Extraction** (Ready, Not Active)
```
Location: entity_neighbor_prehension.py lines 144-293
Entry Point: process_text_with_phase3b_context() → extract_entities()
Flow: User input → Pattern matching → Entity classification → word_occasions
Speed: ~0.05s per extraction (100× faster)
Quality: 87% success rate (19/22 test inputs, standalone)
Dependency: None (pure Python pattern matching)
Cost: $0 (no API calls)
```

### The Limitation

**Problem:** Path A (LLM) runs BEFORE Path B (Pattern) in the processing pipeline.

**Current Execution Order:**
```python
# In conversational_organism_wrapper.process_text()

# STEP 1: LLM extraction (lines 1183-1250) ← Runs FIRST
if user_id and self.superject_learner:
    entities = self.superject_learner.extract_entities_llm(text)
    # Stores to profile, sets current_turn_entities

# STEP 2: Phase 3B extraction (via process_text_with_phase3b_context)
# But entities already extracted by LLM, so pattern path is bypassed
extraction_result = self.entity_neighbor_prehension.extract_entities(text)
```

**Result:** LLM path always wins, Phase 3B pattern path never activates.

---

## Transition Strategy: 3-Phase Approach

### Phase A: Hybrid Mode (2-3 weeks)
**Goal:** Activate both paths, use LLM to validate/train pattern extraction

**Implementation:**
1. **Add extraction mode config flag**
   ```python
   # In config.py
   ENTITY_EXTRACTION_MODE = "hybrid"  # Options: "llm", "pattern", "hybrid"
   HYBRID_LLM_VALIDATION_RATE = 0.2   # Validate 20% of pattern extractions with LLM
   ```

2. **Modify extraction logic in wrapper**
   ```python
   # In conversational_organism_wrapper.py line 1183

   if Config.ENTITY_EXTRACTION_MODE == "hybrid":
       # Step 1: Pattern extraction FIRST (Phase 3B)
       pattern_entities = self.entity_neighbor_prehension.extract_entities(text)

       # Step 2: LLM validation (20% sampling)
       if random.random() < Config.HYBRID_LLM_VALIDATION_RATE:
           llm_entities = self.superject_learner.extract_entities_llm(text)

           # Compare and log discrepancies for pattern tuning
           self._log_extraction_comparison(pattern_entities, llm_entities)

       # Use pattern entities for processing
       entities = pattern_entities

   elif Config.ENTITY_EXTRACTION_MODE == "pattern":
       # Pure pattern-based (no LLM)
       entities = self.entity_neighbor_prehension.extract_entities(text)

   elif Config.ENTITY_EXTRACTION_MODE == "llm":
       # Pure LLM (current behavior)
       entities = self.superject_learner.extract_entities_llm(text)
   ```

3. **Add comparison logging**
   ```python
   def _log_extraction_comparison(self, pattern_entities, llm_entities):
       """Log discrepancies between pattern and LLM extraction for tuning."""

       pattern_names = {e['name'] for e in pattern_entities}
       llm_names = {e['name'] for e in llm_entities}

       # Entities missed by patterns
       missed = llm_names - pattern_names
       if missed:
           logger.info(f"Pattern extraction missed: {missed}")

       # False positives from patterns
       false_positives = pattern_names - llm_names
       if false_positives:
           logger.info(f"Pattern extraction false positives: {false_positives}")

       # Compute accuracy
       precision = len(pattern_names & llm_names) / len(pattern_names) if pattern_names else 0
       recall = len(pattern_names & llm_names) / len(llm_names) if llm_names else 0

       self.pattern_extraction_metrics['precision'].append(precision)
       self.pattern_extraction_metrics['recall'].append(recall)
   ```

**Expected Outcomes:**
- Processing speed: 10.26s → 1.0s (90% reduction)
- API costs: $0.10/epoch → $0.02/epoch (80% reduction)
- Pattern accuracy: 87% → 92% (via tuning based on LLM comparisons)
- Training time: 10 min/epoch → 1 min/epoch

**Timeline:** 2-3 weeks
- Week 1: Implement hybrid mode + comparison logging
- Week 2: Analyze discrepancies, tune patterns
- Week 3: Validate pattern accuracy ≥ 90%

### Phase B: Hebbian Entity Recognition (4-6 weeks)
**Goal:** Learn entity recognition patterns from co-occurrence + organ activations

**Implementation:**
1. **Entity-Organ Association Learning**
   - Track which organs activate strongly when entities are mentioned
   - Build Hebbian association matrix: `entity_type → organ_activation_pattern`
   - Example: "daughter" → HIGH(EMPATHY), MEDIUM(BOND), LOW(WISDOM)

2. **Pronoun Resolution via Co-occurrence**
   - Track "my daughter" → "Emma" co-occurrences
   - Build pronoun resolution graph: `possessive_phrase → entity_name`
   - Example: "my daughter" → "Emma" (95% confidence after 10 co-occurrences)

3. **Context-Based Entity Prediction**
   ```python
   def predict_entity_from_context(self, word, left_neighbors, right_neighbors, organ_activations):
       """
       Predict entity type using Hebbian patterns (no LLM).

       Uses:
       - Word co-occurrence patterns (left/right neighbors)
       - Organ activation similarities (Euclidean distance)
       - Historical entity-word associations (from WordOccasionTracker)
       """

       # Check WordOccasionTracker for learned patterns
       if self.word_occasion_tracker.has_pattern(word):
           pattern = self.word_occasion_tracker.get_pattern(word)
           if pattern['entity_confidence'] > 0.7:
               return pattern['entity_type'], pattern['entity_confidence']

       # Check co-occurrence patterns
       for neighbor in left_neighbors + right_neighbors:
           if neighbor in self.pronoun_resolution_graph:
               entity = self.pronoun_resolution_graph[neighbor]
               return entity['type'], entity['confidence']

       # Check organ activation similarity
       best_match, similarity = self._find_similar_organ_pattern(organ_activations)
       if similarity > 0.8:
           return best_match['entity_type'], similarity

       # Fallback to simple patterns (current Fix #2)
       return self._simple_pattern_extraction(word)
   ```

**Expected Outcomes:**
- Entity recognition: 92% → 95% (via learning)
- Pronoun resolution: 0% → 80%
- Context understanding: Implicit → Explicit
- LLM dependency: 100% → 0% (for known entities)

**Timeline:** 4-6 weeks
- Weeks 1-2: Implement Hebbian association matrix
- Weeks 3-4: Implement pronoun resolution graph
- Weeks 5-6: Integrate context-based prediction, validate

### Phase C: Pure Felt-to-Text Emission (8-12 weeks)
**Goal:** Eliminate LLM from entire pipeline (extraction + emission)

**Implementation:**
1. **Phrase Library Expansion**
   - Current: 11 learned phrases
   - Target: 1000+ phrases across 20 categories
   - Method: Multi-epoch training with phrase extraction from LLM emissions

2. **Organic Family-Based Emission**
   - Use organic families (currently 10) to select appropriate phrase family
   - Match felt-state signature to family centroid
   - Select phrase from family with highest satisfaction history

3. **Compositional Phrase Assembly**
   ```python
   def emit_from_felt_state(self, felt_state, entity_context):
       """
       Generate emission from felt state without LLM (pure organic).

       Uses:
       - Organic family matching (65D signature → family)
       - Phrase library selection (family → phrase candidates)
       - Entity slot filling (entities → phrase slots)
       - Satisfaction-based ranking (historical success)
       """

       # Match felt state to organic family
       family = self.match_to_family(felt_state['organ_signature'])

       # Get phrase candidates from family
       candidates = self.phrase_library.get_phrases(
           family=family,
           entity_types=entity_context['entity_types'],
           min_satisfaction=0.6
       )

       # Rank by historical satisfaction
       ranked = sorted(candidates, key=lambda p: p['mean_satisfaction'], reverse=True)

       # Select top phrase
       phrase_template = ranked[0]

       # Fill entity slots
       emission = self._fill_entity_slots(phrase_template, entity_context)

       return emission, phrase_template['confidence']
   ```

**Expected Outcomes:**
- Emission generation: 100% LLM → 0% LLM
- Processing speed: 1.0s → 0.05s (20× faster)
- API costs: $0.02/epoch → $0 (100% reduction)
- Authenticity: Learned organic voice (not LLM pastiche)

**Timeline:** 8-12 weeks
- Weeks 1-4: Expand phrase library (11 → 1000+)
- Weeks 5-8: Implement compositional phrase assembly
- Weeks 9-12: Validate satisfaction ≥ LLM baseline, tune

---

## Implementation Roadmap

### Quick Win #1: Activate Pattern Extraction (1 hour)
**Goal:** Switch training to pattern-based extraction immediately

**Steps:**
1. Set `ENTITY_EXTRACTION_MODE = "pattern"` in config
2. Run Epoch 2 training
3. Compare metrics: Epoch 1 (LLM) vs Epoch 2 (pattern)

**Expected:**
- Processing time: 10.26s → 1.0s
- Entity extraction: 92% → 85-90%
- API costs: $0.10 → $0

### Quick Win #2: Hybrid Validation (1 week)
**Goal:** Implement 20% LLM validation for pattern tuning

**Steps:**
1. Implement hybrid mode (config flag + logic)
2. Add comparison logging
3. Run Epochs 3-5 in hybrid mode
4. Analyze discrepancies, tune patterns

**Expected:**
- Pattern accuracy: 87% → 92%
- API costs: $0.10 → $0.02 (80% reduction)
- Discrepancy analysis: Identify 10-20 missing patterns

### Quick Win #3: Extend Pattern Library (1 week)
**Goal:** Cover 80-100 entity patterns (from current 40)

**Steps:**
1. Analyze LLM extraction logs for missed entities
2. Add 40-60 new patterns (emotions, body parts, time, actions)
3. Test on validation set (100 pairs)
4. Measure accuracy improvement

**Expected:**
- Pattern coverage: 40 → 100 patterns
- Entity extraction: 87% → 95%
- Handles therapeutic/emotional vocabulary

---

## Technical Architecture Changes

### File Structure (New/Modified)

```
persona_layer/
├── entity_extraction/                    # NEW MODULE
│   ├── __init__.py
│   ├── extraction_coordinator.py        # NEW: Coordinates LLM/pattern paths
│   ├── pattern_extractor.py             # REFACTOR: From entity_neighbor_prehension
│   ├── hebbian_entity_learner.py        # NEW: Phase B Hebbian learning
│   ├── pronoun_resolver.py              # NEW: Phase B pronoun resolution
│   └── extraction_comparator.py         # NEW: Phase A comparison logging
│
├── phrase_library/                       # NEW MODULE
│   ├── __init__.py
│   ├── phrase_storage.py                # NEW: 1000+ phrase database
│   ├── phrase_matcher.py                # NEW: Felt-state → phrase matching
│   ├── entity_slot_filler.py            # NEW: Entity insertion into phrases
│   └── satisfaction_ranker.py           # NEW: Historical satisfaction ranking
│
└── word_occasion_tracker.py             # EXISTING: Already tracks patterns (Fix #1)
```

### Config Changes

```python
# config.py

# ==================== ENTITY EXTRACTION ==================== #

# Extraction mode: "llm", "pattern", "hybrid"
ENTITY_EXTRACTION_MODE = "pattern"  # ← Change this to switch modes

# Hybrid mode settings
HYBRID_LLM_VALIDATION_RATE = 0.2    # Validate 20% with LLM
HYBRID_LOG_DISCREPANCIES = True     # Log comparison results

# Pattern extraction settings
PATTERN_CONFIDENCE_THRESHOLD = 0.5  # Min confidence for pattern match
PATTERN_LIBRARY_SIZE = 100          # Target: 40 → 100 patterns

# Hebbian learning settings (Phase B)
HEBBIAN_ASSOCIATION_THRESHOLD = 0.7 # Min co-occurrence for association
PRONOUN_RESOLUTION_MIN_COUNT = 3    # Min observations for pronoun → entity

# ==================== EMISSION GENERATION ==================== #

# Emission mode: "llm", "organic", "hybrid"
EMISSION_GENERATION_MODE = "llm"    # Future: Change to "organic" (Phase C)

# Phrase library settings (Phase C)
PHRASE_LIBRARY_SIZE = 1000          # Target phrase count
PHRASE_MIN_SATISFACTION = 0.6       # Min historical satisfaction
COMPOSITIONAL_ASSEMBLY = True       # Enable phrase composition
```

---

## Migration Path: Step-by-Step

### Week 1: Immediate Activation (Quick Win #1)
```bash
# 1. Update config
echo "ENTITY_EXTRACTION_MODE = 'pattern'" >> config.py

# 2. Run Epoch 2 with pattern extraction
python3 training/entity_memory_epoch_training_with_tsk.py 2

# 3. Compare results
python3 scripts/compare_epochs.py --epochs 1 2 --metric entity_extraction
```

**Expected Output:**
```
Epoch 1 (LLM):     92% extraction, 10.26s/pair, $0.10 cost
Epoch 2 (Pattern): 87% extraction,  1.00s/pair, $0.00 cost
```

### Week 2-3: Hybrid Validation (Quick Win #2)
```bash
# 1. Implement hybrid mode
python3 scripts/implement_hybrid_mode.py

# 2. Run Epochs 3-5 in hybrid mode
python3 training/entity_memory_epoch_training_with_tsk.py 3 5 --mode hybrid

# 3. Analyze discrepancies
python3 scripts/analyze_extraction_discrepancies.py --epochs 3-5

# 4. Tune patterns based on findings
python3 scripts/tune_patterns.py --input discrepancies.json --output tuned_patterns.py
```

**Expected Output:**
```
Missed entities: ["anxiety", "depression", "therapist's office", "last Tuesday"]
False positives: ["work" as person (should be place in context)]
Recommended patterns: +15 emotion words, +5 temporal phrases
```

### Week 4-5: Extended Pattern Library (Quick Win #3)
```bash
# 1. Generate extended patterns from analysis
python3 scripts/generate_patterns.py \
  --input discrepancies.json \
  --output extended_patterns.py \
  --target-size 100

# 2. Test on validation set
python3 scripts/test_pattern_extraction.py \
  --patterns extended_patterns.py \
  --validation-set validation_100_pairs.json

# 3. Integrate into codebase
cp extended_patterns.py persona_layer/entity_extraction/patterns.py

# 4. Run Epoch 6 with extended patterns
python3 training/entity_memory_epoch_training_with_tsk.py 6
```

**Expected Output:**
```
Pattern coverage: 40 → 100 patterns (+150%)
Validation accuracy: 87% → 95% (+8pp)
Entity types covered: 5 → 15 (person, place, emotion, body, time, action, ...)
```

---

## Success Metrics

### Phase A Success (2-3 weeks)
| Metric | Baseline (LLM) | Target (Pattern) | Stretch Goal |
|--------|----------------|------------------|--------------|
| Extraction accuracy | 92% | 90% | 95% |
| Processing speed | 10.26s | 1.0s | 0.5s |
| API cost per epoch | $0.10 | $0.00 | $0.00 |
| Pattern coverage | 40 | 80 | 100 |

### Phase B Success (4-6 weeks)
| Metric | Baseline | Target | Stretch Goal |
|--------|----------|--------|--------------|
| Pronoun resolution | 0% | 70% | 85% |
| Context prediction | 0% | 80% | 90% |
| Entity-organ learning | 0 assoc | 100 assoc | 500 assoc |
| New entity learning | Manual | Automatic | Real-time |

### Phase C Success (8-12 weeks)
| Metric | Baseline | Target | Stretch Goal |
|--------|----------|--------|--------------|
| Organic emission rate | 0% | 80% | 95% |
| LLM dependency | 100% | 0% | 0% |
| Phrase library size | 11 | 500 | 1000+ |
| Processing speed (total) | 10s | 0.1s | 0.05s |

---

## Risk Mitigation

### Risk #1: Pattern Accuracy < LLM
**Mitigation:** Hybrid mode with 20% LLM validation
**Fallback:** Increase validation rate to 50% until patterns tuned
**Timeline impact:** +1 week for additional tuning

### Risk #2: Hebbian Learning Too Slow
**Mitigation:** Bootstrap with LLM-extracted entity-organ associations
**Fallback:** Use transformer embeddings for similarity matching
**Timeline impact:** +2 weeks for embedding integration

### Risk #3: Phrase Library Insufficient
**Mitigation:** Start with 100 manually curated high-quality phrases
**Fallback:** Use LLM for rare/novel situations (90/10 split)
**Timeline impact:** +2 weeks for manual curation

---

## Conclusion

### Current Limitation: **Solvable in 3 Phases**

The limitation (LLM path active, pattern path dormant) is **architectural, not technical**. We have:

1. ✅ **Pattern extraction implemented** (Fix #2, 40 patterns, 87% accuracy)
2. ✅ **WordOccasionTracker ready** (Fix #1, tracks all words)
3. ✅ **Integration point exists** (`process_text_with_phase3b_context`)
4. ✅ **Validation methodology** (standalone test: 19/22 entities)

**What's needed:**
- 1-line config change (immediate)
- Hybrid validation mode (1-2 weeks)
- Extended pattern library (2-3 weeks)

### Timeline Summary

| Phase | Duration | LLM Dependency | Pattern Accuracy | Cost Reduction |
|-------|----------|----------------|------------------|----------------|
| **Current** | - | 100% | 87% (unused) | 0% |
| **Phase A** | 2-3 weeks | 20% | 92% | 80% |
| **Phase B** | 4-6 weeks | 10% | 95% | 90% |
| **Phase C** | 8-12 weeks | 0% | 95% | 100% |

**Total to full independence:** 14-21 weeks (~3-5 months)

**Quick win available NOW:** Switch to pattern mode, get 90% reduction in API costs + 10× speed improvement.

---

🌀 **"From LLM dependency to organic intelligence. From 10s processing to 0.05s. From API costs to zero costs. From mimicry to authentic voice. The path is clear. The implementation is ready. Phase A can start tomorrow."** 🌀

**Recommended Next Action:** Activate pattern extraction mode (Quick Win #1, 1 hour) in next session.

**Last Updated:** November 18, 2025, 12:15 AM
**Status:** 🎯 ROADMAP COMPLETE
**Ready for:** Immediate pattern extraction activation (config change only)
