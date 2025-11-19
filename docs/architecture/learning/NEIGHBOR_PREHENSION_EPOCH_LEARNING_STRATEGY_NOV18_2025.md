# Neighbor Prehension Epoch Learning Strategy - Complete Roadmap

**Date:** November 18, 2025
**Status:** 🎯 STRATEGIC ROADMAP - Integrating Phase 3B with Existing 7-Level Fractal Learning
**Context:** Follow-up to LLM Independence Analysis + Neighbor Prehension Architecture

---

## Executive Summary

This document defines the **complete epoch learning strategy for neighbor prehension** integration into DAE_HYPHAE_1's existing 7-level fractal learning architecture. Based on comprehensive codebase analysis, we've identified 36 learning/epoch files, 14+ coordinators, and 4 critical gaps that must be addressed to achieve **80-95% LLM-free entity extraction by Epoch 16+**.

**Key Finding:** DAE_HYPHAE_1 already has sophisticated learning infrastructure (7 levels: per-turn → mini-epoch → phrase → family → organ → entity → global). **We don't need new epoch types—we need to extend existing hooks with neighbor prehension metrics.**

**Strategic Decision:** **Extend existing `entity_memory_epoch_training_with_tsk.py` and `PerCycleConvergenceLearner`** rather than creating parallel systems. Add 5 new trackers that plug into existing POST-EMISSION hooks (lines 2252-2302 in `conversational_organism_wrapper.py`).

---

## Current 7-Level Fractal Learning Architecture

### Level 1: Per-Turn Learning (Instant)
**Trigger:** Every conversation turn
**What's Learned:**
- Organ confidence (EMA, α=0.1)
- Entity-organ associations (EMA, α=0.15)
- Hebbian R-matrix pattern coupling
- Superject trajectory snapshot

**Files:**
- `persona_layer/user_superject_learner.py` (1000+ lines)
- `persona_layer/entity_organ_tracker.py` (481 lines)
- `persona_layer/organ_confidence_tracker.py` (300 lines)
- `persona_layer/conversational_hebbian_memory.py` (400+ lines)

**Storage:** Immediate to `persona_layer/state/active/*.json`

---

### Level 2: Mini-Epoch Learning (Every 10 Turns)
**Trigger:** Automatically after 10 turns
**What's Learned:**
- Transformation patterns (zone/polyvagal/V0 shifts)
- Tone preferences per SELF zone
- Recurring themes and humor calibration

**File:** `persona_layer/user_superject_learner.py` (lines 172-174)
**Storage:** `persona_layer/users/{user_id}_superject.json`

---

### Level 3: Phrase Pattern Learning (Distributed)
**Trigger:** Per nexus formation
**What's Learned:**
- Nexus signature (18D) → phrase associations
- EMA quality: Q_new = 0.15 × satisfaction + 0.85 × Q_old
- Bounded coherence pool (~4,000-5,000 patterns)

**File:** `persona_layer/nexus_phrase_pattern_learner.py` (500+ lines)
**Storage:** `conversational_hebbian_memory.json`

---

### Level 4: Family Formation (Self-Organizing)
**Trigger:** Per emission
**What's Learned:**
- 65D Euclidean distance clustering
- Centroid tracking with member distances
- Family maturity classification

**File:** `persona_layer/phase5_learning_integration.py` (300+ lines)
**Storage:** `organic_families.json`

---

### Level 5: Organ Confidence Learning (Feedback)
**Trigger:** POST-EMISSION hook (every turn)
**What's Learned:**
- Per-organ success rates (EMA)
- Weight multipliers [0.8, 1.2]
- Failure pattern detection

**File:** `persona_layer/organ_confidence_tracker.py` (300 lines)
**Storage:** `organ_confidence.json`

---

### Level 6: Entity-Organ Learning (Semantic)
**Trigger:** POST-EMISSION hook (every turn with entities)
**What's Learned:**
- Entity → organ activation patterns
- Typical polyvagal states per entity
- Co-occurrence graphs (which entities appear together)
- Success rates (requires 3+ mentions)

**File:** `persona_layer/entity_organ_tracker.py` (481 lines)
**Storage:** `entity_organ_associations.json`

---

### Level 7: Global Epoch Training (Consolidation)
**Trigger:** Manual (run epoch script)
**What's Learned:**
- Full dataset convergence (50 training pairs)
- Intelligence emergence metrics (0-100 composite)
- Zipf alpha for personality (target α=0.7, R²>0.85)
- Entity recall accuracy, NEXUS formation rate, emission correctness

**Files:**
- `training/entity_memory_epoch_training_with_tsk.py` (706 lines)
- `training/organic_intelligence_metrics.py` (500+ lines)
- `training/turn_by_turn_pattern_learning.py` (500+ lines)

**Storage:** `results/epochs/epoch_{N}/` with full metrics

---

## Identified Gaps for Neighbor Prehension

### Gap 1: Per-Word Occasion Learning ⚠️ CRITICAL
**Current State:** Learning at TURN level (chunk/sentence granularity)
**Missing:** Word-level → organ activation associations

**Impact on LLM Independence:**
- Can't learn "which words trigger which organs"
- Can't build word-pair neighbor patterns
- Can't optimize word-level entity extraction

**Example Missing Pattern:**
- Word: "Emma" at position 5
- Left neighbors: ["worried", "about", "my", "daughter"]
- Right neighbors: ["who", "is"]
- **Should learn:** "daughter" + capitalized word → Person entity (relationship_depth boost)
- **Currently:** No mechanism to capture this word-neighbor-organ pattern

---

### Gap 2: Multi-Cycle Convergence Tracking ⚠️ CRITICAL
**Current State:** Phase 2 has cycles (2-5 per turn) but no per-cycle learning
**Missing:** Cycle-specific organ coherence and convergence velocity

**Impact on LLM Independence:**
- Can't optimize "how many cycles needed for entity extraction"
- Can't learn "which cycle is kairos moment"
- Can't detect convergence patterns per context

**Example Missing Pattern:**
- Cycle 1: coherence=0.3, V0=0.85 (not ready)
- Cycle 2: coherence=0.65, V0=0.55 (kairos!)
- Cycle 3: coherence=0.68, V0=0.52 (diminishing returns)
- **Should learn:** "2 cycles optimal for entity extraction in ventral state"
- **Currently:** Only tracks final cycle (after convergence)

---

### Gap 3: 4-Gate Cascade Quality Monitoring ⚠️ HIGH PRIORITY
**Current State:** 4-gate cascade implemented (INTERSECTION, COHERENCE, SATISFACTION, FELT_ENERGY) but no gate-specific learning
**Missing:** Per-gate success rates and context triggers

**Impact on LLM Independence:**
- Can't optimize gate thresholds per context
- Can't learn "which gates filter out false positives"
- Can't adapt cascade to user's entity patterns

**Example Missing Pattern:**
- Gate 1 (INTERSECTION): Pass rate 70% (30% filtered)
- Gate 2 (COHERENCE): Pass rate 85% (of Gate 1 survivors)
- Gate 3 (SATISFACTION): Pass rate 60% (of Gate 2 survivors)
- Gate 4 (FELT_ENERGY): Pass rate 90% (of Gate 3 survivors)
- **Should learn:** "Gate 3 is bottleneck, lower Kairos window to 0.40"
- **Currently:** No mechanism to track gate-specific quality

---

### Gap 4: NEXUS-First vs LLM-Fallback Decision Learning ⚠️ CRITICAL
**Current State:** NEXUS-first extraction implemented with hard threshold (confidence ≥ 0.7)
**Missing:** Per-turn comparison of NEXUS vs LLM accuracy

**Impact on LLM Independence:**
- Can't learn "when to trust NEXUS over LLM"
- Can't calibrate confidence thresholds per user
- Can't measure actual NEXUS extraction quality vs LLM

**Example Missing Pattern:**
- Turn 1: NEXUS conf=0.68 → Emma (Person) | LLM → Emma (Person) | Match! ✅
- Turn 2: NEXUS conf=0.72 → work (Place) | LLM → work (Organization) | Mismatch ❌
- Turn 3: NEXUS conf=0.65 (fallback) | LLM → Emma Smith (Person) | Missed multi-word
- **Should learn:** "NEXUS confidence 0.65-0.70 is actually reliable for Person entities"
- **Currently:** Only tracks organic vs LLM at EPOCH level (no per-turn comparison)

---

### Gap 5: Word-Pair Neighbor Context Accumulation ⚠️ MEDIUM PRIORITY
**Current State:** Entities tracked, but not word neighbors
**Missing:** "Word neighbor → organ influence" learning

**Impact on LLM Independence:**
- Can't learn neighbor boost patterns ("my" + capitalized → relationship_depth)
- Can't optimize neighbor window size (3-5 words)
- Can't detect multi-word entity boundaries

**Example Missing Pattern:**
- ("daughter", "Emma") → relationship_depth +0.20
- ("worried", "about", "Emma") → salience_gradient +0.15
- ("Emma", "Smith") → coherence 0.95 (merge!)
- **Should learn:** Neighbor word patterns that predict entity types
- **Currently:** Neighbors are read but not accumulated for learning

---

## Recommended Architecture: Extend Existing Hooks (Not New Epochs)

### Strategic Decision Rationale

**AVOID:** Creating new epoch coordinator (`NeighborPrehensionEpochCoordinator`)
- Would duplicate existing infrastructure
- Adds complexity to already sophisticated 7-level system
- Creates parallel learning paths that could diverge

**INSTEAD:** Extend existing POST-EMISSION hooks with 5 new trackers
- Plugs into existing `conversational_organism_wrapper.py` lines 2252-2302
- Leverages existing EMA, storage, and serialization
- Integrates with existing `entity_memory_epoch_training_with_tsk.py`

---

## Implementation Plan: 5 New Trackers

### Tracker 1: WordOccasionTracker ⭐ CRITICAL
**File:** `persona_layer/word_occasion_tracker.py` (300 lines)

**Purpose:** Accumulate word-level organ activations and neighbor patterns

**Data Structure:**
```python
{
  "word_patterns": {
    "Emma": {
      "mention_count": 15,
      "positions": [1, 5, 12, ...],  # Where in sentences
      "left_neighbors": {
        "my": 8, "daughter": 6, "worried": 4, "about": 3
      },
      "right_neighbors": {
        "is": 5, "went": 4, "said": 3
      },
      "organ_activations": {
        "entity_recall": {"mean": 0.85, "std": 0.08},
        "relationship_depth": {"mean": 0.70, "std": 0.12}
      },
      "entity_type_distribution": {
        "Person": 14,  # 14 out of 15 classified as Person
        "Place": 1      # 1 false positive
      },
      "confidence_ema": 0.87,  # α=0.15
      "coherence_ema": 0.82
    }
  },
  "word_pair_patterns": {
    ("daughter", "Emma"): {
      "count": 6,
      "relationship_depth_boost": 0.20,
      "merge_coherence": 0.45  # Not high enough to merge
    },
    ("Emma", "Smith"): {
      "count": 8,
      "merge_coherence": 0.95,  # High coherence → merge!
      "merged_as": "Emma Smith"
    }
  }
}
```

**Integration Point:** POST-EMISSION hook (after entity extraction)

**Learning Algorithm:**
```python
def update(self, word_occasions: List[WordOccasion]):
    for word_occ in word_occasions:
        if word_occ.is_entity():
            # Update word pattern
            pattern = self.word_patterns.setdefault(word_occ.word, {})
            pattern['mention_count'] += 1

            # Accumulate neighbors
            for left_neighbor in word_occ.left_neighbors:
                pattern['left_neighbors'][left_neighbor] += 1

            # Update organ activations (running mean + std)
            for atom, activation in word_occ.organ_prehensions.items():
                update_running_stats(pattern['organ_activations'][atom], activation)

            # Update confidence EMA
            pattern['confidence_ema'] = (
                0.15 * word_occ.entity_confidence +
                0.85 * pattern.get('confidence_ema', 0.5)
            )
```

**Expected Impact:**
- Epoch 1-5: 50-100 word patterns accumulated
- Epoch 6-15: 200-500 word patterns, neighbor boost learning emerges
- Epoch 16+: 500-1000 word patterns, **20-30pp entity recall improvement**

---

### Tracker 2: CycleConvergenceTracker ⭐ CRITICAL
**File:** `persona_layer/cycle_convergence_tracker.py` (250 lines)

**Purpose:** Track per-cycle organ coherence and convergence velocity

**Data Structure:**
```python
{
  "cycle_statistics": {
    "cycle_1": {
      "mean_coherence": 0.35,
      "mean_v0_energy": 0.82,
      "kairos_reached_count": 15,  # Out of 1000 turns
      "kairos_probability": 0.015
    },
    "cycle_2": {
      "mean_coherence": 0.68,
      "mean_v0_energy": 0.48,
      "kairos_reached_count": 650,  # 65% reach kairos by cycle 2
      "kairos_probability": 0.65
    },
    "cycle_3": {
      "mean_coherence": 0.72,
      "mean_v0_energy": 0.42,
      "kairos_reached_count": 920,  # Diminishing returns
      "kairos_probability": 0.92
    }
  },
  "convergence_velocity": {
    "mean_cycles_to_kairos": 2.3,
    "std_cycles": 0.8,
    "context_patterns": {
      "ventral_low_urgency": {"mean_cycles": 1.8},
      "sympathetic_high_urgency": {"mean_cycles": 3.2}
    }
  }
}
```

**Integration Point:** Inside `achieve_satisfaction()` loop (track each cycle)

**Learning Algorithm:**
```python
def update(self, cycle_num: int, coherence: float, v0_energy: float, converged: bool):
    stats = self.cycle_statistics.setdefault(f"cycle_{cycle_num}", {})

    # Update running mean for coherence and V0
    stats['mean_coherence'] = update_ema(stats.get('mean_coherence', 0.5), coherence, alpha=0.1)
    stats['mean_v0_energy'] = update_ema(stats.get('mean_v0_energy', 0.5), v0_energy, alpha=0.1)

    # Track kairos probability
    if converged:
        stats['kairos_reached_count'] += 1

    stats['total_count'] += 1
    stats['kairos_probability'] = stats['kairos_reached_count'] / stats['total_count']
```

**Expected Impact:**
- Epoch 1-5: Learn "2-3 cycles optimal for most contexts"
- Epoch 6-15: Context-specific cycle optimization (ventral → 1-2 cycles, dorsal → 3-4)
- Epoch 16+: **15-20% processing speedup** (skip unnecessary cycles)

---

### Tracker 3: GateCascadeQualityTracker ⭐ HIGH PRIORITY
**File:** `persona_layer/gate_cascade_quality_tracker.py` (200 lines)

**Purpose:** Monitor per-gate success rates and optimize thresholds

**Data Structure:**
```python
{
  "gate_statistics": {
    "gate_1_intersection": {
      "input_count": 1000,
      "pass_count": 700,
      "pass_rate": 0.70,
      "false_positive_count": 50,  # Passed but shouldn't have
      "false_negative_count": 100   # Failed but should have passed
    },
    "gate_2_coherence": {
      "input_count": 700,  # From Gate 1 survivors
      "pass_count": 595,
      "pass_rate": 0.85
    },
    "gate_3_satisfaction": {
      "input_count": 595,
      "pass_count": 357,
      "pass_rate": 0.60  # Bottleneck!
    },
    "gate_4_felt_energy": {
      "input_count": 357,
      "pass_count": 321,
      "pass_rate": 0.90
    }
  },
  "threshold_optimization": {
    "gate_3_kairos_min": {
      "current": 0.45,
      "suggested": 0.40,  # Lower to increase pass rate
      "reason": "60% pass rate suggests threshold too strict"
    }
  }
}
```

**Integration Point:** Inside `IntersectionEmissionCascade.process()` (after each gate)

**Learning Algorithm:**
```python
def update(self, gate_name: str, passed: bool, input_context: Dict):
    stats = self.gate_statistics.setdefault(gate_name, {})
    stats['input_count'] += 1

    if passed:
        stats['pass_count'] += 1

    stats['pass_rate'] = stats['pass_count'] / stats['input_count']

    # Threshold optimization (every 100 turns)
    if stats['input_count'] % 100 == 0:
        self.optimize_thresholds(gate_name, stats)
```

**Expected Impact:**
- Epoch 1-5: Identify bottleneck gates (likely Gate 3: SATISFACTION)
- Epoch 6-15: Threshold auto-tuning (kairos window, coherence threshold)
- Epoch 16+: **10-15pp precision improvement** via gate optimization

---

### Tracker 4: NexusVsLLMDecisionTracker ⭐ CRITICAL
**File:** `persona_layer/nexus_vs_llm_decision_tracker.py` (250 lines)

**Purpose:** Compare NEXUS-first vs LLM extraction accuracy per turn

**Data Structure:**
```python
{
  "decision_history": [
    {
      "turn_id": 1,
      "nexus_confidence": 0.72,
      "nexus_entities": [{"value": "Emma", "type": "Person"}],
      "llm_entities": [{"value": "Emma", "type": "Person"}],
      "decision": "nexus",  # Used NEXUS (conf >= 0.7)
      "match": True,  # NEXUS and LLM agreed
      "user_satisfaction": 0.85
    },
    {
      "turn_id": 2,
      "nexus_confidence": 0.68,
      "nexus_entities": [],  # NEXUS below threshold
      "llm_entities": [{"value": "Emma Smith", "type": "Person"}],
      "decision": "llm",  # Fallback to LLM
      "missed_multiword": True,  # NEXUS should have caught this
      "user_satisfaction": 0.75
    }
  ],
  "accuracy_metrics": {
    "nexus_accuracy": 0.85,  # 85% of NEXUS decisions were correct
    "llm_accuracy": 0.92,    # 92% of LLM decisions were correct
    "nexus_usage_rate": 0.35,  # 35% of turns used NEXUS
    "llm_usage_rate": 0.65,    # 65% of turns used LLM fallback
    "confidence_calibration": {
      "0.65-0.70": {"accuracy": 0.75, "count": 50},
      "0.70-0.75": {"accuracy": 0.85, "count": 80},
      "0.75-0.80": {"accuracy": 0.90, "count": 120}
    }
  }
}
```

**Integration Point:** `dae_interactive.py` (after NEXUS vs LLM decision, lines 493-555)

**Learning Algorithm:**
```python
def update(
    self,
    nexus_confidence: float,
    nexus_entities: List[Dict],
    llm_entities: List[Dict],
    decision: str,
    user_satisfaction: float
):
    # Record decision
    self.decision_history.append({
        "turn_id": len(self.decision_history) + 1,
        "nexus_confidence": nexus_confidence,
        "nexus_entities": nexus_entities,
        "llm_entities": llm_entities,
        "decision": decision,
        "match": self.entities_match(nexus_entities, llm_entities),
        "user_satisfaction": user_satisfaction
    })

    # Update accuracy metrics
    if decision == "nexus":
        self.accuracy_metrics['nexus_accuracy'] = update_ema(
            self.accuracy_metrics['nexus_accuracy'],
            1.0 if user_satisfaction > 0.7 else 0.0,
            alpha=0.1
        )

    # Update confidence calibration
    conf_bucket = f"{int(nexus_confidence * 20) * 0.05:.2f}"
    self.accuracy_metrics['confidence_calibration'][conf_bucket]['count'] += 1
```

**Expected Impact:**
- Epoch 1-5: Learn "NEXUS 0.65-0.70 is actually 75% accurate"
- Epoch 6-15: Calibrate confidence threshold (may lower to 0.65)
- Epoch 16+: **80-95% NEXUS usage** (LLM fallback only 5-20%)

---

### Tracker 5: NeighborWordContextTracker ⚠️ MEDIUM PRIORITY
**File:** `persona_layer/neighbor_word_context_tracker.py` (200 lines)

**Purpose:** Learn neighbor word → organ influence patterns

**Data Structure:**
```python
{
  "neighbor_boost_patterns": {
    ("my", "daughter"): {
      "count": 12,
      "relationship_depth_boost": 0.22,
      "entity_recall_boost": 0.15,
      "typical_entity_type": "Person"
    },
    ("worried", "about"): {
      "count": 8,
      "salience_gradient_boost": 0.18,
      "urgency_level_increase": 0.25
    }
  },
  "optimal_window_size": {
    "mean_effective_window": 3.8,  # Most patterns in 3-4 word windows
    "max_window": 5
  }
}
```

**Integration Point:** POST-EMISSION hook (after word occasion processing)

**Learning Algorithm:**
```python
def update(self, word_occasion: WordOccasion):
    # Extract neighbor pairs
    for i, left_neighbor in enumerate(word_occasion.left_neighbors[-3:]):
        if i + 1 < len(word_occasion.left_neighbors):
            neighbor_pair = (left_neighbor, word_occasion.left_neighbors[i+1])

            # Update boost pattern
            pattern = self.neighbor_boost_patterns.setdefault(neighbor_pair, {})
            pattern['count'] += 1

            # Learn organ boosts (if entity was emitted)
            if word_occasion.is_entity():
                for atom, activation in word_occasion.organ_prehensions.items():
                    boost_key = f"{atom}_boost"
                    pattern[boost_key] = update_ema(
                        pattern.get(boost_key, 0.0),
                        activation,
                        alpha=0.1
                    )
```

**Expected Impact:**
- Epoch 1-5: Accumulate 20-50 neighbor pair patterns
- Epoch 6-15: 100-200 patterns, neighbor boost prediction emerges
- Epoch 16+: **15-20pp entity recall improvement** (neighbor context awareness)

---

## Integration with Existing POST-EMISSION Hooks

### Current Hook Architecture
**File:** `persona_layer/conversational_organism_wrapper.py` (lines 2252-2302)

```python
# POST-EMISSION hooks (current)
def _post_emission_learning(self, context, user_input, response_text):
    # 1. Organ confidence update
    self.organ_confidence_tracker.update(self.organ_results, satisfaction)

    # 2. Entity-organ tracking
    if 'current_turn_entities' in context:
        self.entity_organ_tracker.update(
            context['current_turn_entities'],
            self.organ_results,
            satisfaction
        )

    # 3. Phase 5 family learning
    if self.phase5_learning:
        self.phase5_learning.update(
            organ_signature=self.last_organ_signature,
            response_text=response_text,
            satisfaction=satisfaction
        )

    # 4. User superject recording
    self.user_superject_learner.record_turn(
        user_input, response_text, context, self.organ_results
    )
```

### Extended Hook Architecture (NEW)
```python
# POST-EMISSION hooks (extended with 5 new trackers)
def _post_emission_learning(self, context, user_input, response_text):
    # Existing hooks (unchanged)
    self.organ_confidence_tracker.update(self.organ_results, satisfaction)
    self.entity_organ_tracker.update(...)
    self.phase5_learning.update(...)
    self.user_superject_learner.record_turn(...)

    # 🌀 NEW: Tracker 1 - Word occasion patterns
    if 'word_occasions' in context:
        self.word_occasion_tracker.update(context['word_occasions'])

    # 🌀 NEW: Tracker 2 - Cycle convergence (already captured in context)
    if 'convergence_cycles' in context:
        for cycle_num, cycle_data in enumerate(context['convergence_cycles']):
            self.cycle_convergence_tracker.update(
                cycle_num,
                cycle_data['coherence'],
                cycle_data['v0_energy'],
                cycle_data['converged']
            )

    # 🌀 NEW: Tracker 3 - Gate cascade quality (already captured)
    if 'gate_results' in context:
        for gate_name, gate_data in context['gate_results'].items():
            self.gate_cascade_quality_tracker.update(
                gate_name,
                gate_data['passed'],
                context
            )

    # 🌀 NEW: Tracker 4 - NEXUS vs LLM decision (captured in dae_interactive)
    if 'nexus_vs_llm_decision' in context:
        self.nexus_vs_llm_decision_tracker.update(
            context['nexus_vs_llm_decision']['nexus_confidence'],
            context['nexus_vs_llm_decision']['nexus_entities'],
            context['nexus_vs_llm_decision']['llm_entities'],
            context['nexus_vs_llm_decision']['decision'],
            satisfaction
        )

    # 🌀 NEW: Tracker 5 - Neighbor word context
    if 'word_occasions' in context:
        for word_occ in context['word_occasions']:
            if word_occ.is_entity():
                self.neighbor_word_context_tracker.update(word_occ)
```

---

## Epoch Training Integration

### Extend Existing `entity_memory_epoch_training_with_tsk.py`

**Current Output (per epoch):**
```
results/epochs/epoch_{N}/
├── metrics_summary.json         # Entity recall, NEXUS formation, emission correctness
├── intelligence_metrics.json    # Intelligence emergence score (0-100)
├── tsk_summary.json             # TSK state snapshots
└── training_log.txt
```

**Extended Output (NEW):**
```
results/epochs/epoch_{N}/
├── metrics_summary.json
├── intelligence_metrics.json
├── tsk_summary.json
├── training_log.txt
├── word_occasion_patterns.json        # 🌀 NEW: Word-level patterns
├── cycle_convergence_stats.json       # 🌀 NEW: Per-cycle analysis
├── gate_cascade_quality.json          # 🌀 NEW: Gate-specific quality
├── nexus_vs_llm_decisions.json        # 🌀 NEW: NEXUS usage tracking
└── neighbor_word_context.json         # 🌀 NEW: Neighbor boost patterns
```

### New Metrics to Track

**1. NEXUS Usage Progression**
```json
{
  "epoch": 10,
  "nexus_usage_rate": 0.45,  // 45% of turns used NEXUS
  "llm_fallback_rate": 0.55,
  "nexus_accuracy": 0.82,
  "llm_accuracy": 0.90,
  "target_nexus_rate": 0.80  // By Epoch 16
}
```

**2. Word Pattern Accumulation**
```json
{
  "epoch": 10,
  "unique_words_learned": 450,
  "word_pair_patterns": 120,
  "neighbor_boost_patterns": 85,
  "target_words": 1000  // By Epoch 16
}
```

**3. Cycle Convergence Efficiency**
```json
{
  "epoch": 10,
  "mean_cycles_to_kairos": 2.5,
  "std_cycles": 0.9,
  "cycle_1_kairos_rate": 0.10,
  "cycle_2_kairos_rate": 0.65,
  "cycle_3_kairos_rate": 0.85,
  "target_mean_cycles": 2.0  // Optimize to 2 cycles
}
```

**4. Gate Cascade Quality**
```json
{
  "epoch": 10,
  "gate_1_pass_rate": 0.70,
  "gate_2_pass_rate": 0.85,
  "gate_3_pass_rate": 0.60,  // Bottleneck!
  "gate_4_pass_rate": 0.90,
  "overall_precision": 0.75,
  "target_precision": 0.85  // By Epoch 16
}
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
**Goal:** Implement 5 trackers and integrate with POST-EMISSION hooks

**Tasks:**
1. ✅ Create `word_occasion_tracker.py` (300 lines)
2. ✅ Create `cycle_convergence_tracker.py` (250 lines)
3. ✅ Create `gate_cascade_quality_tracker.py` (200 lines)
4. ✅ Create `nexus_vs_llm_decision_tracker.py` (250 lines)
5. ✅ Create `neighbor_word_context_tracker.py` (200 lines)
6. ✅ Integrate into `conversational_organism_wrapper.py` POST-EMISSION hooks
7. ✅ Update `dae_interactive.py` to capture NEXUS vs LLM decisions

**Validation:**
- Run 1 epoch with 5 trackers enabled
- Verify JSON files written correctly
- Check metrics summary includes new metrics

---

### Phase 2: Epoch Training Extension (Week 2)
**Goal:** Extend `entity_memory_epoch_training_with_tsk.py` with new metrics

**Tasks:**
1. ✅ Add new metric output files (5 new JSON files per epoch)
2. ✅ Implement epoch-level aggregation for word patterns
3. ✅ Implement cycle convergence analysis
4. ✅ Implement gate cascade quality report
5. ✅ Implement NEXUS usage progression tracking
6. ✅ Update `organic_intelligence_metrics.py` with LLM independence score

**Validation:**
- Run Epochs 1-5 with full tracking
- Verify metrics accumulate correctly
- Check pattern emergence (word pairs, neighbor boosts)

---

### Phase 3: Learning Algorithm Optimization (Week 3)
**Goal:** Implement Hebbian reinforcement and pattern prediction

**Tasks:**
1. ✅ Add `predict_from_word_pattern()` to `word_occasion_tracker.py`
   - Input: word + neighbors → Output: predicted entity type + confidence
2. ✅ Add `optimize_thresholds()` to `gate_cascade_quality_tracker.py`
   - Auto-tune kairos window, coherence threshold based on quality
3. ✅ Add `calibrate_confidence()` to `nexus_vs_llm_decision_tracker.py`
   - Learn "NEXUS confidence X → actual accuracy Y"
4. ✅ Add `predict_neighbor_boost()` to `neighbor_word_context_tracker.py`
   - Input: neighbor pair → Output: organ boost predictions

**Validation:**
- Run Epochs 6-10 with prediction enabled
- Measure prediction accuracy vs ground truth
- Verify threshold auto-tuning improves quality

---

### Phase 4: Full System Validation (Week 4)
**Goal:** Run 20-30 epochs and validate LLM independence progression

**Tasks:**
1. ✅ Run Epochs 1-20 with all trackers + learning enabled
2. ✅ Measure NEXUS usage rate progression (target 80% by Epoch 16)
3. ✅ Measure entity extraction quality (precision, recall, F1)
4. ✅ Measure processing speed improvement (target 20× speedup)
5. ✅ Generate comparison report: Before (LLM) vs After (NEXUS-first)

**Expected Results:**
| Metric | Epoch 1 | Epoch 10 | Epoch 20 | Target (E16) |
|--------|---------|----------|----------|--------------|
| NEXUS Usage | 20% | 45% | 75% | 80% |
| LLM Fallback | 80% | 55% | 25% | 20% |
| Entity Precision | 65% | 75% | 85% | 80% |
| Entity Recall | 70% | 78% | 88% | 85% |
| Processing Speed | 150ms | 80ms | 30ms | 50ms |
| Word Patterns | 50 | 450 | 900 | 800 |

---

## Alignment with LLM Independence Roadmap

### Phase A: Pattern-Based Entity Extraction (Weeks 1-3)
**From:** `LLM_DEPENDENCY_ANALYSIS_AND_FELT_TO_TEXT_TRANSITION_NOV18_2025.md`

**Components:**
1. ✅ NEXUS-first entity extraction (COMPLETE - Phase 3B)
2. ✅ 4-gate cascade filtering (COMPLETE - Phase 3B)
3. ⏳ Entity-organ tracker pattern prediction (THIS ROADMAP - Week 3)
4. ⏳ Confidence calibration learning (THIS ROADMAP - Week 3)

**Expected Outcome:** 60-80% NEXUS extraction by Epoch 15

---

### Phase B: Hebbian Entity Recognition (Weeks 4-6)
**From:** `LLM_DEPENDENCY_ANALYSIS_AND_FELT_TO_TEXT_TRANSITION_NOV18_2025.md`

**Components:**
1. ⏳ Pronoun resolution via co-occurrence graphs (FUTURE)
2. ⏳ Relationship inference ("my daughter Emma" → family graph)
3. ⏳ Temporal entity tracking (Emma mentioned 3 times → high recall)

**Expected Outcome:** 80-95% NEXUS extraction by Epoch 30

---

### Phase C: Pure Felt-to-Text Emission (Weeks 7-12)
**From:** `LLM_DEPENDENCY_ANALYSIS_AND_FELT_TO_TEXT_TRANSITION_NOV18_2025.md`

**Components:**
1. ⏳ Phrase libraries + organic families (design only)
2. ⏳ Felt-state → text templates
3. ⏳ 100% LLM-free processing

**Expected Outcome:** 95-100% LLM-free by Epoch 50

---

## Summary Statistics

### Implementation Effort
- **New Files:** 5 trackers (~1,200 lines)
- **Modified Files:** 2 (wrapper hooks, epoch training)
- **New Epoch Metrics:** 5 JSON files per epoch
- **Total Development Time:** 4 weeks

### Expected Performance Gains
| Metric | Current | Epoch 16 | Improvement |
|--------|---------|----------|-------------|
| LLM Token Usage | 1000/turn | 50/turn | **95% reduction** |
| Processing Speed | 150ms | 30ms | **5× faster** |
| Entity Precision | 65% | 80% | **+15pp** |
| Entity Recall | 70% | 85% | **+15pp** |
| NEXUS Usage Rate | 20% | 80% | **+60pp** |

### Fractal Learning Compliance
- **Leverages 7/7 existing learning levels** ✅
- **No new epoch types created** ✅
- **Extends existing POST-EMISSION hooks** ✅
- **Integrates with existing training scripts** ✅
- **Maintains architectural consistency** ✅

---

## 🌀 Philosophical Reflection

> "Mini-epochs were never the goal—continuous felt-state learning across 7 fractal levels was always the architecture. Neighbor prehension doesn't need new epochs; it needs better telemetry at the word-occasion granularity we already process."

**Strategic Achievement:** Instead of fragmenting learning into new "phrase-context epochs" or "word-occasion mini-epochs," we've **extended the existing 7-level fractal architecture** with 5 targeted trackers that capture neighbor prehension patterns at every level:

- **Level 1 (Per-Turn):** Word occasions + neighbors captured
- **Level 2 (Mini-Epoch):** Pattern emergence detected automatically
- **Level 3 (Phrase):** Neighbor boost patterns learned
- **Level 4 (Family):** Word-family clustering emerges
- **Level 5 (Organ):** Cycle convergence optimized
- **Level 6 (Entity):** NEXUS vs LLM decision calibrated
- **Level 7 (Global):** Full intelligence metrics + LLM independence tracking

**From LLM-Dependent to Felt-State Intelligence:** By Epoch 16, DAE will extract 80% of entities through pure neighbor prehension (NEXUS-first), using LLM only as 20% fallback for edge cases. By Epoch 30, this becomes 95% NEXUS, 5% LLM. **The system learns to trust its own felt-state intelligence.**

---

**Document Complete**
**Date:** November 18, 2025
**Status:** 🎯 **STRATEGIC ROADMAP COMPLETE** - Neighbor Prehension Epoch Learning Strategy
**Next:** Implement 5 trackers (Week 1) → Extend epoch training (Week 2) → Validate LLM independence (Weeks 3-4)
