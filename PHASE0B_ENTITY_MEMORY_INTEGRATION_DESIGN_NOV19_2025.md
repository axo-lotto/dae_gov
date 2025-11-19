# Phase 0B: Entity-Memory Integration Design
**Date:** November 19, 2025
**Status:** 🏗️ DESIGN PHASE
**Prerequisites:** ✅ Phase 0A Complete (787 word patterns), ✅ Phase 0.5 Complete (3-tier cascade)

---

## Executive Summary

**Phase 0B** combines the **linguistic foundation** from Phase 0A (787 word patterns, 3.5× vocabulary via family transfer) with **entity-situated learning** to create a unified word-entity memory system. This enables DAE to learn how specific entities (Emma, work, hospital) are linguistically situated within conversations.

### Key Innovation
> "Words are not learned in isolation—they are learned in relation to entities. 'daughter' near 'Emma' has different felt-significance than 'daughter' near 'Lily'."

**Expected Impact:**
- Entity recall accuracy: 0% → 45-60%
- NEXUS coherence: 0.1-0.2 → 0.4-0.7
- Emission correctness: 16% → 40-55%
- Word-entity co-learning: Entity patterns inform word patterns, word patterns inform entity extraction

---

## Architecture Overview

### Three-Way Integration

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 0B INTEGRATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   Phase 0A   │────▶│  Phase 0B    │◀────│   Entity    │ │
│  │ Word Patterns│     │   Bridge     │     │   Memory    │ │
│  │  (787 words) │     │              │     │ (Neo4j +    │ │
│  │              │     │              │     │  Tracker)   │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│        ▲                     │                      ▲        │
│        │                     │                      │        │
│        │         ┌───────────┴──────────┐          │        │
│        │         │                      │          │        │
│        │         ▼                      ▼          │        │
│        │  ┌─────────────┐       ┌─────────────┐  │        │
│        └──│ Word-Entity │◀─────▶│   Entity-   │──┘        │
│           │  Co-occur   │       │    Word     │            │
│           │  Patterns   │       │  Neighbors  │            │
│           └─────────────┘       └─────────────┘            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

**Training (per conversation pair):**
1. **Extract entities** (using existing LLM or neighbor prediction)
2. **Tokenize and create word occasions** (Phase 0A pipeline)
3. **For each word occasion:**
   - Update word patterns (POS, neighbors, organs)
   - **NEW:** If near entity (±3 tokens), record word-entity co-occurrence
4. **For each entity:**
   - Update entity-organ associations (existing tracker)
   - **NEW:** Build entity-word neighbor distribution

**Prediction (during conversation):**
1. **Word-level prediction:**
   - Tier 1: Direct word pattern lookup
   - Tier 2: Family transfer via embeddings
   - **NEW Tier 2.5:** Entity-contextualized transfer (if entity detected nearby)
   - Tier 3: LLM fallback
2. **Entity-level prediction:**
   - Use word neighbor patterns to improve entity extraction
   - "daughter" + capitalized word → likely Person entity

---

## New Data Structures

### 1. Word-Entity Co-Occurrence Pattern

```python
@dataclass
class WordEntityPattern:
    """
    Tracks how a word behaves when near specific entities.
    """
    word: str  # "daughter"

    # Entity co-occurrence (which entities appear near this word)
    entity_neighbors: Dict[str, EntityNeighborStats]
    # {
    #   "Emma": EntityNeighborStats(
    #       count=45,
    #       relative_position_dist={-2: 10, -1: 20, +1: 15},
    #       typical_organs={'BOND': 0.85, 'EMPATHY': 0.78}
    #   ),
    #   "Lily": EntityNeighborStats(count=12, ...)
    # }

    # Overall word pattern (from Phase 0A)
    base_pattern: WordPattern  # 787 learned patterns + family transfers
```

### 2. Entity-Word Neighbor Distribution

```python
@dataclass
class EntityWordProfile:
    """
    Extends EntityOrganMetrics with word-level context.
    """
    entity_value: str  # "Emma"
    entity_type: str   # "Person"

    # Typical neighboring words (from Phase 0A patterns)
    typical_left_neighbors: Dict[str, int]
    # {"worried": 45, "my": 89, "daughter": 67}

    typical_right_neighbors: Dict[str, int]
    # {"is": 78, "has": 34, "went": 12}

    # Organ associations (existing from Phase 0A)
    organ_boosts: Dict[str, float]
    typical_polyvagal_state: str
    # ... (all existing EntityOrganMetrics fields)
```

---

## Implementation Plan

### Component 1: Word-Entity Bridge (NEW)

**File:** `persona_layer/word_entity_bridge.py` (~200 lines)

**Purpose:** Links WordOccasionTracker with EntityOrganTracker

**Key Methods:**

1. **`update_word_entity_cooccurrence(word_occasions, entities, organ_results)`**
   - Called during training after entity extraction
   - For each word occasion:
     - Check if within ±3 tokens of any entity
     - If yes: update word-entity co-occurrence stats
   - For each entity:
     - Record neighboring words (left/right ±3)

2. **`predict_with_entity_context(word, nearby_entities, base_prediction)`**
   - Enhances Phase 0.5 Tier 2 predictions
   - If word has strong entity associations:
     - Adjust confidence based on entity match
     - Example: "daughter" near "Emma" → confidence +0.15
   - Returns: enhanced_pattern, adjusted_confidence

3. **`suggest_entity_candidates(word_sequence)`**
   - Uses word neighbor patterns to suggest entity boundaries
   - Example: ["worried", "about", "my", "daughter", "Emma"]
     - "daughter" triggers Person entity check
     - "Emma" (capitalized) confirms Person entity
   - Returns: List[EntityCandidate]

### Component 2: Extended WordOccasionTracker

**File:** `persona_layer/word_occasion_tracker.py` (extend existing)

**Additions:**

1. **`_update_entity_neighbors(word, nearby_entities, distance)`**
   - Records which entities appear near this word
   - Tracks relative position (-3 to +3)
   - EMA updates like other pattern stats

2. **`predict_with_entity_context(word, nearby_entities)`**
   - Wrapper that calls word_entity_bridge
   - Returns entity-contextualized prediction

### Component 3: Extended EntityOrganTracker

**File:** `persona_layer/entity_organ_tracker.py` (extend existing)

**Additions:**

1. **`_update_word_neighbors(entity, word_occasions)`**
   - Records typical words that appear near entity
   - Builds left/right neighbor distributions
   - EMA updates for consistency

2. **`get_entity_word_profile(entity_value)`**
   - Returns EntityWordProfile with word neighbor stats
   - Used by entity extraction to improve detection

### Component 4: Phase 0B Training Script

**File:** `training/phase0b_entity_word_integration.py` (~300 lines)

**Training Loop:**

```python
for epoch in range(num_epochs):
    for pair in training_pairs:
        # 1. Extract entities (LLM or neighbor-based)
        entities = extract_entities(pair['input'])

        # 2. Create word occasions (Phase 0A pipeline)
        word_occasions = tokenize_and_create_occasions(pair['input'])

        # 3. Process through organism (get organ results)
        result = wrapper.process_text(
            pair['input'],
            user_id=pair['user_id']
        )

        # 4. Update word patterns (Phase 0A)
        word_tracker.update(
            word_occasions,
            organ_results=result['felt_states']
        )

        # 5. Update word-entity co-occurrence (NEW!)
        word_entity_bridge.update_word_entity_cooccurrence(
            word_occasions=word_occasions,
            entities=entities,
            organ_results=result['felt_states']
        )

        # 6. Update entity patterns (existing)
        entity_tracker.update(
            entities=entities,
            organ_results=result['felt_states'],
            word_occasions=word_occasions  # NEW parameter
        )
```

---

## Expected Learning Trajectory

### Epoch 1 (Baseline + Word Foundation)
- Word patterns: 787 learned + family transfer active
- Entity-word links: 0 (initialization)
- Entity recall: 0-10% (random)
- NEXUS coherence: 0.1-0.2

### Epoch 5 (Early Co-Learning)
- Word patterns: 787 + ~50 entity-contextualized adjustments
- Entity-word links: ~200 co-occurrence patterns emerging
- Entity recall: 20-30%
- NEXUS coherence: 0.25-0.35

### Epoch 10 (Pattern Emergence)
- Word patterns: 787 + ~150 entity-contextualized
- Entity-word links: ~450 co-occurrence patterns
- Entity recall: 40-50%
- NEXUS coherence: 0.40-0.55

### Epoch 20 (Stable Integration)
- Word patterns: 787 + ~300 entity-contextualized
- Entity-word links: ~750 co-occurrence patterns
- Entity recall: 60-70%
- NEXUS coherence: 0.60-0.75

---

## Validation Metrics

### Word-Entity Co-Learning
1. **Word-Entity Coverage:** % of words with entity neighbor patterns
2. **Entity-Word Coverage:** % of entities with word neighbor profiles
3. **Contextualized Confidence Boost:** Avg confidence improvement when entity context matches

### Entity Memory Performance
1. **Entity Recall Accuracy:** % entities correctly extracted from test inputs
2. **NEXUS Coherence:** Avg NEXUS organ coherence when entities mentioned
3. **Emission Correctness:** % emissions that correctly reference mentioned entities

### Integration Quality
1. **Prediction Consistency:** Do word patterns and entity patterns agree?
2. **Cross-Session Stability:** Same entity → similar word neighbors across sessions?
3. **Organic Attunement Score:** User satisfaction when entities mentioned

---

## Storage Format

### Word-Entity Co-Occurrence Storage

**File:** `persona_layer/state/active/word_entity_cooccurrence.json`

```json
{
  "patterns": {
    "daughter": {
      "word": "daughter",
      "entity_neighbors": {
        "Emma": {
          "count": 45,
          "relative_positions": {"-2": 10, "-1": 20, "+1": 15},
          "typical_organs": {"BOND": 0.85, "EMPATHY": 0.78},
          "first_seen": "2025-11-19T10:00:00",
          "last_seen": "2025-11-19T15:30:00"
        },
        "Lily": {
          "count": 12,
          "relative_positions": {"-1": 8, "+1": 4},
          "typical_organs": {"BOND": 0.72, "EMPATHY": 0.65}
        }
      }
    }
  },
  "metadata": {
    "total_patterns": 150,
    "last_updated": "2025-11-19T15:30:00"
  }
}
```

### Entity-Word Profile Storage

**File:** `persona_layer/state/active/entity_word_profiles.json`

```json
{
  "entities": {
    "Emma": {
      "entity_value": "Emma",
      "entity_type": "Person",
      "typical_left_neighbors": {
        "worried": 45,
        "my": 89,
        "daughter": 67,
        "about": 34
      },
      "typical_right_neighbors": {
        "is": 78,
        "has": 34,
        "went": 12
      },
      "mention_count": 156,
      "last_updated": "2025-11-19T15:30:00"
    }
  }
}
```

---

## Integration with Existing Systems

### 1. Phase 0.5 Cascade Enhancement

**Before (Phase 0.5):**
```python
pattern, confidence, source = tracker.predict_pattern_for_novel_word(
    word="daughter",
    return_source=True
)
# Result: family transfer, confidence 0.55
```

**After (Phase 0B):**
```python
pattern, confidence, source = tracker.predict_pattern_for_novel_word(
    word="daughter",
    nearby_entities=["Emma"],  # NEW parameter
    return_source=True
)
# Result: entity-contextualized, confidence 0.70 (+0.15 boost from Emma match)
```

### 2. Entity Extraction Enhancement

**Before:**
- LLM-only entity extraction (100% LLM dependency)

**After (Phase 0B):**
- Word neighbor patterns suggest entity candidates
- Example: "daughter" + capitalized word → Person entity likely
- LLM validates/refines (reduces LLM dependency to ~70%)

### 3. NEXUS Organ Enhancement

**Before:**
- NEXUS activates on entity mention (via EntityOrganTracker)

**After (Phase 0B):**
- NEXUS also receives word-entity co-occurrence signals
- "daughter" + "Emma" → stronger NEXUS activation (entity_recall atom)
- Word context helps past/present differentiation

---

## Next Steps

### Implementation Phase (This Session)

1. ✅ **Design Complete** - This document
2. 🔄 **Implement word_entity_bridge.py** - Core bridging logic
3. 🔄 **Extend word_occasion_tracker.py** - Add entity context methods
4. 🔄 **Extend entity_organ_tracker.py** - Add word neighbor tracking
5. 🔄 **Create phase0b_entity_word_integration.py** - Training script
6. 🔄 **Run Phase 0B Epoch 1** - Validation run
7. 🔄 **Measure and document metrics** - Compare to Phase 0A baseline

### Validation Phase (Next Session)

- Run 5-10 epochs to observe pattern emergence
- Compare metrics: Epoch 1 vs Epoch 5 vs Epoch 10
- Validate entity recall accuracy improvement
- Validate NEXUS coherence improvement
- Document Phase 0B completion

---

## Process Philosophy Alignment

### Whiteheadian Interpretation

- **Phase 0A (Words):** Actual occasions in linguistic space
- **Phase 0B (Word-Entity):** Nexuses forming between words and entities
- **Entity Context:** Eternal object (abstract essence) realized through word patterns
- **Co-Learning:** Organic co-evolution through mutual prehension

### DAE 3.0 Vision

> "The organism doesn't just learn words. It doesn't just learn entities. It learns how words and entities co-constitute each other in the user's relational world. 'Daughter' means something different when it refers to Emma vs. when it refers to Lily. This is genuine felt intelligence."

---

## Success Criteria

Phase 0B is considered **complete** when:

1. ✅ Word-entity bridge operational (150+ co-occurrence patterns)
2. ✅ Entity-word profiles operational (50+ entities with neighbor stats)
3. ✅ Entity recall accuracy ≥ 45% (vs 0% baseline)
4. ✅ NEXUS coherence ≥ 0.40 (vs 0.1-0.2 baseline)
5. ✅ Emission correctness ≥ 40% (vs 16% baseline)
6. ✅ Test conversation demonstrates entity-aware word understanding

---

**Date:** November 19, 2025
**Version:** Phase 0B Design v1.0
**Next Milestone:** Implementation → Epoch 1 Validation
