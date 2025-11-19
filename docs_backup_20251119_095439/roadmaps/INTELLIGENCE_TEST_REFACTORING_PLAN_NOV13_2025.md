# Intelligence Test Suite Refactoring Plan
**Date:** November 13, 2025
**Phase:** Post-C3 - Intelligence Validation
**Status:** 🔄 **IN PROGRESS**

---

## Analysis Summary

### Current State of Intelligence Tests

**Location:** `/tests/intelligence/`
**Test Count:** 5 intelligence tests
**Created:** November 13, 2025 (Phase B)
**Status:** ⚠️ **INCOMPATIBLE** with current system architecture

---

## Test Suite Overview

### INTEL-001: Abstraction Reasoning (`test_abstraction_reasoning.py`)
**Goal:** Test pattern detection across abstraction levels (concrete → semi-abstract → abstract)

**Key Metrics:**
- Organ activation correlation: ≥0.70 across levels
- Nexus type overlap: ≥60%
- Emission semantic similarity: ≥0.60
- Confidence stability: ±0.15 range

**Current Compatibility:** 🟡 **PARTIAL**
- ✅ Organ activation tracking works
- ✅ Nexus formation tracking works
- ⚠️  Emission similarity needs semantic comparison (embedding distance)
- ✅ Confidence tracking works

---

### INTEL-002: Pattern Transfer (`test_pattern_transfer.py`)
**Goal:** Transfer learned patterns from domain A → domain B (workplace → family systems)

**Key Metrics:**
- Transfer accuracy: ≥65%
- Organ activation similarity: ≥0.60 between isomorphic patterns
- Confidence on novel domain: ≥0.40
- Nexus type consistency: ≥50%

**Current Compatibility:** 🟡 **PARTIAL**
- ✅ Organ activation comparison works
- ✅ Nexus type tracking works
- ⚠️  Requires training on domain A first (epoch training integration)
- ⚠️  Pattern isomorphism detection (needs structural similarity metric)

---

### INTEL-003: Novelty Handling (`test_novelty_handling.py`)
**Goal:** Graceful degradation on completely novel inputs

**Key Metrics:**
- No crashes on novel input
- ≥5 organs active (general response)
- Emission strategy: hebbian_fallback
- Confidence: [0.20, 0.40] (appropriate uncertainty)

**Current Compatibility:** 🟢 **READY**
- ✅ All metrics directly accessible
- ✅ Emission strategy tracking works
- ✅ Confidence calibration works
- ✅ Organ participation tracking works

**Action:** Minor updates for current organism wrapper API

---

### INTEL-004: Context Integration (`test_context_integration.py`)
**Goal:** Multi-turn context tracking and adaptation

**Key Metrics:**
- Context sensitivity: ≥0.30 correlation change per turn
- Emission evolution: ≥40% unique words per turn
- Satisfaction increase: +0.10 by turn 3
- No degradation: Confidence ≥0.30 across turns

**Current Compatibility:** 🟡 **PARTIAL**
- ✅ Organ activation changes trackable
- ⚠️  Multi-turn context (need session management)
- ⚠️  Emission word uniqueness (need text comparison utility)
- ✅ Satisfaction/confidence tracking works

---

### INTEL-005: Meta-Learning (`test_meta_learning.py`)
**Goal:** Performance improvement across epoch progression

**Key Metrics:**
- Confidence improvement: +0.15 (epoch 1 → 10)
- Family formation: 3-7 families by epoch 10
- Same-input consistency: ≥75% same family assignment
- Convergence acceleration: -0.5 cycles

**Current Compatibility:** 🔴 **INCOMPATIBLE**
- ❌ Requires epoch state snapshots (not currently saved)
- ❌ Requires family formation tracking (organic_families.json integration)
- ⚠️  Convergence tracking works but needs epoch comparison framework
- ⚠️  Requires training infrastructure integration

---

## Key Incompatibilities Identified

### 1. **Epoch State Management** (CRITICAL)
**Problem:** Tests expect to load organism state from specific epochs
**Current:** No epoch checkpoint system
**Solution:** Create checkpoint save/load in training runner

### 2. **Family Formation Tracking** (CRITICAL for INTEL-005)
**Problem:** Test expects family discovery tracking
**Current:** `organic_families.json` exists but not integrated with test harness
**Solution:** Family loader utility

### 3. **Emission Semantic Comparison** (MODERATE)
**Problem:** Tests compare emission semantic similarity
**Current:** No embedding distance utility for emissions
**Solution:** Use embedding coordinator for emission comparison

### 4. **Multi-Turn Session Management** (MODERATE)
**Problem:** INTEL-004 needs conversational context across turns
**Current:** Organism processes single inputs
**Solution:** Session wrapper for multi-turn context

### 5. **Pattern Transfer Training** (MODERATE)
**Problem:** INTEL-002 needs training on domain A before testing domain B
**Current:** No dynamic training integration in test
**Solution:** Mini-training harness in test setup

---

## Refactoring Strategy

### Phase 1: Infrastructure (Utilities)
**Time:** 1-2 hours
**Priority:** HIGH

1. **`tests/intelligence/utils/test_utils.py`**
   - Emission semantic similarity (embedding distance)
   - Text uniqueness calculator
   - Organ activation correlation
   - Nexus type overlap calculator

2. **`tests/intelligence/utils/checkpoint_manager.py`**
   - Save organism state to checkpoint
   - Load organism state from checkpoint
   - Epoch state comparison utilities

3. **`tests/intelligence/utils/family_loader.py`**
   - Load organic families from JSON
   - Family assignment checker
   - Family statistics

### Phase 2: Test Refactoring (Individual Tests)
**Time:** 2-3 hours
**Priority:** HIGH

**Order of refactoring (easiest → hardest):**

1. **INTEL-003: Novelty Handling** (READY)
   - Minor API updates
   - Run and validate

2. **INTEL-001: Abstraction Reasoning** (PARTIAL)
   - Add emission similarity utility
   - Run and validate

3. **INTEL-004: Context Integration** (PARTIAL)
   - Add multi-turn session wrapper
   - Add text uniqueness utility
   - Run and validate

4. **INTEL-002: Pattern Transfer** (PARTIAL)
   - Add mini-training harness
   - Add pattern isomorphism detector
   - Run and validate

5. **INTEL-005: Meta-Learning** (INCOMPATIBLE)
   - Requires full checkpoint system
   - Requires training runner integration
   - Most complex - do last

### Phase 3: Integration & Validation
**Time:** 1 hour
**Priority:** MEDIUM

1. **Test Runner** (`tests/intelligence/run_all_intelligence_tests.py`)
   - Run all 5 tests sequentially
   - Aggregate results
   - Generate intelligence report

2. **Documentation** (`INTELLIGENCE_TEST_RESULTS_NOV13_2025.md`)
   - Test outcomes
   - Organism intelligence profile
   - Strengths/weaknesses identified

---

## Current System Capabilities (Phase C3 Complete)

### ✅ **Available Metrics:**
- Organ activation patterns (11 organs)
- Nexus formation (14 types)
- Lure fields (3 organs × 7D each = 21D)
- V0 convergence cycles
- Emission confidence
- Emission text
- Processing time
- TSK compliance (full felt_states)

### ✅ **Available Components:**
- `ConversationalOrganismWrapper` (main interface)
- `EmbeddingCoordinator` (for semantic comparison)
- `Config` (centralized parameters)
- Training infrastructure (`dae_orchestrator.py`)
- Validation infrastructure (`quick` and `full`)

### ⚠️  **Missing (Needed for Tests):**
- Checkpoint save/load system
- Multi-turn session manager
- Emission semantic comparison utilities
- Pattern isomorphism detector
- Family assignment checker

---

## Implementation Checklist

### Phase 1: Utilities ✅ (Target: Next)
- [ ] Create `tests/intelligence/utils/__init__.py`
- [ ] Create `test_utils.py` (semantic similarity, text uniqueness, correlations)
- [ ] Create `checkpoint_manager.py` (save/load organism state)
- [ ] Create `family_loader.py` (family assignment utilities)

### Phase 2: Refactor Tests
- [ ] INTEL-003: Novelty Handling (easiest)
- [ ] INTEL-001: Abstraction Reasoning
- [ ] INTEL-004: Context Integration
- [ ] INTEL-002: Pattern Transfer
- [ ] INTEL-005: Meta-Learning (hardest)

### Phase 3: Integration
- [ ] Create test runner
- [ ] Run full intelligence suite
- [ ] Generate results document

---

## Expected Outcomes

### Immediate (Phase 1-2 Complete)
- 4/5 intelligence tests operational
- Organism intelligence baseline established
- Validation of current capabilities

### Short-term (Phase 3 Complete)
- Full 5/5 intelligence test suite operational
- Repeatable intelligence benchmarking
- Confidence in organism reasoning abilities

### Long-term (Ongoing)
- Track intelligence metrics across development
- Identify improvement opportunities
- Validate architectural decisions against intelligence goals

---

## Notes

**Why Intelligence Testing Matters:**
- Validates process philosophy implementation
- Demonstrates learning vs. template matching
- Reveals emergent intelligence patterns
- Guides future development priorities

**Key Insight:**
Current system has ALL the raw capabilities needed (organs, nexuses, lures, transduction).
Tests just need adapters to measure and compare these capabilities systematically.

---

**Status:** 🔄 Utilities creation in progress
**Next:** Create `tests/intelligence/utils/` infrastructure
**Blockers:** None - all dependencies available
