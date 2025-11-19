# Phase 3B Immediate Fixes - Action Plan

**Date:** November 18, 2025
**Priority:** HIGH - 3 critical fixes to achieve 100% Phase 3B functionality

---

## Fix #1: WordOccasionTracker Pattern Learning ⚠️ **CRITICAL**

### Root Cause Identified

**File:** `persona_layer/word_occasion_tracker.py` (Line 129)
**Issue:** Chicken-and-egg problem

```python
# Current code (Line 129)
def update(self, word_occasions: List[WordOccasion]):
    for word_occ in word_occasions:
        # Only track entities (words that passed 4-gate cascade)
        if not word_occ.is_entity():  # ← PROBLEM: Skips ALL words when no entities found
            continue
```

**Impact:**
- 50 updates captured ✅
- 0 words tracked ❌ (all words filtered out)
- WordOccasionTracker can't learn patterns to help predict future entities

**Chicken-and-Egg:**
1. WordOccasionTracker should learn patterns to PREDICT entities
2. But it only tracks words ALREADY classified as entities
3. Since entity extraction finds 0 entities → learns nothing
4. Can't improve entity extraction because has no patterns

---

### Solution: Track ALL Words, Mark Entities

**Change:** Remove entity filter, track all words with entity flag

```python
# Fix (Line 129)
def update(self, word_occasions: List[WordOccasion]):
    for word_occ in word_occasions:
        # Track ALL words, not just entities
        # This allows pattern learning even when entity extraction fails
        self._update_word_pattern(word_occ)

        # Update word pair patterns (for multi-word detection)
        self._update_word_pair_patterns(word_occ, word_occasions)

    self.total_updates += 1

    # Save every 10 updates
    if self.total_updates % 10 == 0:
        self._save_patterns()
```

**And in `_update_word_pattern` (add entity flag tracking):**

```python
def _update_word_pattern(self, word_occ: WordOccasion):
    """
    Update pattern for a single word (tracks ALL words).

    Args:
        word_occ: WordOccasion from current turn
    """
    word = word_occ.word.lower()

    # Create or get word pattern
    if word not in self.word_patterns:
        self.word_patterns[word] = WordPattern(word=word)

    pattern = self.word_patterns[word]

    # Update mention count
    pattern.mention_count += 1
    pattern.positions.append(word_occ.position)

    # Track neighbors
    for left_neighbor in word_occ.left_neighbors:
        pattern.left_neighbors[left_neighbor.lower()] = \
            pattern.left_neighbors.get(left_neighbor.lower(), 0) + 1

    for right_neighbor in word_occ.right_neighbors:
        pattern.right_neighbors[right_neighbor.lower()] = \
            pattern.right_neighbors.get(right_neighbor.lower(), 0) + 1

    # Track organ activations (if available)
    if hasattr(word_occ, 'organ_activations') and word_occ.organ_activations:
        for organ_name, activation in word_occ.organ_activations.items():
            if organ_name not in pattern.organ_activations:
                pattern.organ_activations[organ_name] = {
                    'sum': 0.0,
                    'count': 0,
                    'ema': 0.5
                }

            # Update running stats
            pattern.organ_activations[organ_name]['sum'] += activation
            pattern.organ_activations[organ_name]['count'] += 1

            # Update EMA
            pattern.organ_activations[organ_name]['ema'] = \
                (1 - self.ema_alpha) * pattern.organ_activations[organ_name]['ema'] + \
                self.ema_alpha * activation

    # Track entity classification (if this word was classified as entity)
    if word_occ.is_entity():  # ← NEW: Track entity flag
        entity_type = word_occ.entity_type or "Unknown"
        pattern.entity_type_distribution[entity_type] = \
            pattern.entity_type_distribution.get(entity_type, 0) + 1

        # Update confidence/coherence EMA (only for entities)
        if word_occ.entity_confidence is not None:
            pattern.confidence_ema = \
                (1 - self.ema_alpha) * pattern.confidence_ema + \
                self.ema_alpha * word_occ.entity_confidence

        if word_occ.entity_coherence is not None:
            pattern.coherence_ema = \
                (1 - self.ema_alpha) * pattern.coherence_ema + \
                self.ema_alpha * word_occ.entity_coherence

    # Update timestamps
    pattern.last_seen = time.time()
```

**Expected Impact:**
- ✅ Tracks all 50+ words per turn
- ✅ Learns neighbor patterns (left/right context)
- ✅ Learns organ activation patterns (even for non-entities)
- ✅ Can predict entity types based on accumulated patterns
- ✅ Bootstraps entity extraction through learned patterns

**Effort:** 30 minutes (modify 1 function, test with 5 inputs)

---

## Fix #2: Simple Pattern-Based Entity Extraction ❌ **CRITICAL**

### Root Cause

**File:** `entity_neighbor_prehension.py` (Line 193)
**Issue:** Placeholder heuristic too restrictive

```python
# Current heuristic (Line 193)
if is_capitalized and not word_occasion.is_first_in_sentence:
    # Classify as Person
```

**Impact:**
- Finds 0 entities in entity-memory training corpus
- GateCascadeQualityTracker: 0 attempts (blocked)
- NeighborWordContextTracker: 0 updates (blocked)
- NEXUS usage: 0% (no entities to track)

---

### Solution: Simple Pattern-Based Extraction

**File:** `entity_neighbor_prehension.py`
**Add new method after line 192:**

```python
def _simple_pattern_extraction(self, word_occasion: WordOccasion) -> Tuple[Optional[str], float]:
    """
    Simple pattern-based entity extraction (LLM-free, 30 lines).

    Uses common patterns to classify entities with reasonable confidence.
    This is a bootstrap mechanism until word_occasion_tracker has enough
    learned patterns.

    Args:
        word_occasion: WordOccasion to classify

    Returns:
        Tuple of (entity_type, confidence) or (None, 0.0)
    """
    word = word_occasion.word.lower()
    is_capitalized = word_occasion.word[0].isupper()

    # Pattern 1: Person names (capitalized, not first word)
    if is_capitalized and not word_occasion.is_first_in_sentence:
        return "Person", 0.70

    # Pattern 2: Locations (common location words)
    location_words = {
        'hospital': 0.65,
        'work': 0.65,
        'school': 0.65,
        'home': 0.60,
        'park': 0.60,
        'store': 0.60,
        'office': 0.65,
        'restaurant': 0.60,
        'library': 0.60,
        'gym': 0.60
    }
    if word in location_words:
        return "Place", location_words[word]

    # Pattern 3: Family relationships with possessives
    family_words = {
        'daughter': 0.60,
        'son': 0.60,
        'mother': 0.60,
        'father': 0.60,
        'sister': 0.60,
        'brother': 0.60,
        'wife': 0.60,
        'husband': 0.60,
        'parent': 0.60,
        'child': 0.60,
        'grandmother': 0.60,
        'grandfather': 0.60,
        'aunt': 0.60,
        'uncle': 0.60,
        'cousin': 0.60
    }
    if word in family_words:
        # Check for possessive in left neighbors
        left_has_possessive = any(
            n.lower() in ['my', 'your', 'her', 'his', 'their', 'our']
            for n in word_occasion.left_neighbors[-3:]  # Check last 3 left neighbors
        )
        if left_has_possessive:
            return "Person", family_words[word]  # "my daughter" → Person reference

    # Pattern 4: Professions/roles (often entities)
    profession_words = {
        'doctor': 0.55,
        'nurse': 0.55,
        'teacher': 0.55,
        'therapist': 0.60,
        'counselor': 0.60,
        'manager': 0.55,
        'boss': 0.55,
        'friend': 0.60,
        'partner': 0.60,
        'colleague': 0.55
    }
    if word in profession_words:
        # Higher confidence if preceded by possessive
        left_has_possessive = any(
            n.lower() in ['my', 'your', 'her', 'his', 'their', 'our']
            for n in word_occasion.left_neighbors[-3:]
        )
        if left_has_possessive:
            return "Person", profession_words[word] + 0.05  # Boost confidence
        else:
            return "Person", profession_words[word]

    # No pattern matched
    return None, 0.0
```

**And update `_prehend_word` to use it (around line 193):**

```python
def _prehend_word(self, word_occasion: WordOccasion, ...) -> Optional[Dict[str, Any]]:
    """Extract entity from word occasion using neighbor prehension."""

    # Try simple pattern-based extraction first (LLM-free)
    entity_type, confidence = self._simple_pattern_extraction(word_occasion)

    if entity_type and confidence >= 0.55:  # Threshold for simple patterns
        # Build entity dict
        entity = {
            'entity_value': word_occasion.word,
            'entity_type': entity_type,
            'confidence_score': confidence,
            'coherence': confidence * 0.9,  # Approximate coherence from confidence
            'position': word_occasion.position,
            'source': 'pattern_based_extraction'
        }

        # Add to candidates if not duplicate
        # ... (existing deduplication logic)

        return entity

    # Fallback to capitalized word heuristic (existing logic)
    # ...
```

**Expected Impact:**
- ✅ Extracts 15-30 entities per epoch (up from 0)
- ✅ Unblocks GateCascadeQualityTracker (20-40 attempts expected)
- ✅ Unblocks NeighborWordContextTracker (10-30 updates expected)
- ✅ NEXUS usage: 5-15% (entities extracted and tracked)
- ✅ Bootstrap mechanism until WordOccasionTracker learns patterns

**Coverage:**
- Person names: Capitalized words (existing)
- Locations: 10 common places (new)
- Family relations: 15 family words + possessives (new)
- Professions/roles: 10 common roles + possessives (new)

**Total patterns: ~40 entity patterns** (covers most entity-memory training corpus)

**Effort:** 2-3 hours (add 1 method, update 1 method, test with 10 inputs)

---

## Fix #3: Kairos Detection Rate Investigation ⚠️ **IMPORTANT**

### Issue

**Observed:**
- Mean cycles to kairos: 2.24 ✅ (good convergence)
- Kairos success rate: 0.0% ❌ (expected 70-80%)

**Expected:**
- Kairos window: [0.30, 0.50] (config.py)
- Detection rate: 78.6% (proven in wave training)

---

### Investigation Steps

**Step 1: Check if kairos is being detected during V0 convergence**

```python
# Add debug logging in conversational_occasion.py (V0 descent loop)

# Around line where kairos is checked
if self.kairos_window[0] <= satisfaction <= self.kairos_window[1]:
    print(f"   ✅ KAIROS DETECTED: satisfaction={satisfaction:.3f}, window=[{self.kairos_window[0]}, {self.kairos_window[1]}]")
    kairos_detected = True
else:
    print(f"   ⚠️  No kairos: satisfaction={satisfaction:.3f}, window=[{self.kairos_window[0]}, {self.kairos_window[1]}]")
    kairos_detected = False
```

**Step 2: Check if kairos flag is being passed to tracker**

```python
# In conversational_organism_wrapper.py (Line 1540)

# Debug log before passing to tracker
print(f"   🔍 Passing to tracker: cycles={cycles_used}, kairos={converged}")

self.cycle_convergence_tracker.update_convergence_complete(
    cycles_used=felt_states.get('convergence_cycles', 1),
    converged=felt_states.get('kairos_detected', False),  # ← Check this value
    context=cycle_context
)
```

**Step 3: Check tracker's internal logic**

```python
# In cycle_convergence_tracker.py

def update_convergence_complete(self, cycles_used, converged, context):
    print(f"   📊 Tracker received: cycles={cycles_used}, converged={converged}, context={context}")

    # ... rest of logic
```

**Expected Diagnosis:**
One of three issues:
1. Kairos not being detected (satisfaction never in [0.30, 0.50])
2. Kairos flag not in felt_states dict
3. Tracker not receiving kairos flag correctly

**Effort:** 1 hour (add debug logs, run 5 test inputs, identify issue, fix)

---

## Implementation Plan

### Priority Order:

**1. Fix #2: Pattern-Based Entity Extraction** (2-3 hours) ⚠️ **DO FIRST**
   - Unblocks 2/5 trackers immediately
   - Enables entity-memory learning
   - Highest impact per hour

**2. Fix #1: WordOccasionTracker** (30 minutes)
   - Quick win
   - Enables pattern learning for all words
   - Synergizes with Fix #2

**3. Fix #3: Kairos Detection** (1 hour)
   - Important but not blocking other trackers
   - Improves learning quality
   - Can be done after #1 and #2

**Total Time: 3.5-4.5 hours**

---

### Testing Strategy

**After Each Fix:**

```bash
# Quick test (5 inputs)
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH
python3 test_phase3b_fix.py

# Analyze tracker stats
python3 analyze_epoch1_trackers.py
```

**After All 3 Fixes:**

```bash
# Full Epoch 1 re-run (50 inputs)
python3 training/entity_memory_epoch_training_with_tsk.py 1

# Expected results:
# - WordOccasionTracker: 50 updates, 20-40 unique words, 5-15 reliable patterns
# - CycleConvergenceTracker: 50 attempts, ~2.3 mean cycles, 70-80% kairos rate
# - GateCascadeQualityTracker: 20-40 attempts, bottleneck identified
# - NexusVsLLMDecisionTracker: 50 decisions, 5-15% NEXUS usage
# - NeighborWordContextTracker: 10-30 updates, 0-5 reliable patterns
```

**Expected Outcome:**
- ✅ 5/5 trackers operational
- ✅ 5/5 JSON files created
- ✅ 100% Phase 3B functionality achieved

---

## Success Criteria

### Before Fixes:
- Operational trackers: 3/5 (60%)
- JSON files: 3/5
- Entity extraction: 0 entities
- Word patterns: 0 learned

### After Fixes:
- Operational trackers: 5/5 (100%) ✅
- JSON files: 5/5 ✅
- Entity extraction: 15-30 entities per epoch ✅
- Word patterns: 20-40 words, 5-15 reliable ✅
- Gate attempts: 20-40 per epoch ✅
- Neighbor updates: 10-30 per epoch ✅
- Kairos rate: 70-80% ✅

---

🌀 **"Three critical fixes to achieve 100% Phase 3B functionality. Pattern-based entity extraction unblocks 2/5 trackers. WordOccasionTracker learns from all words, not just entities. Kairos detection restored to 70-80% rate. Total effort: 3.5-4.5 hours. Expected outcome: Full time-crystal learning operational across all 5 trackers."** 🌀

**Last Updated:** November 18, 2025, 10:45 PM
**Status:** READY FOR IMPLEMENTATION
**Priority:** HIGH (blocks full Phase 3B learning)
