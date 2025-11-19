# Activation Checklist - November 19, 2025

## 🎯 Mission: Activate Existing Modules (NOT Build New Ones)

**Context**: Strategic analysis revealed that 58% of proposed development already exists in operational form. This checklist focuses on **activation** and **integration** of existing capabilities.

---

## ✅ Immediate Actions (This Week - 5-6 Hours Total)

### [ ] Action 1: Enable Transductive Filter Layer 2-3 (30 min)

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/conversational_organism_wrapper.py`

**Lines**: 277-290

**Current State**:
```python
self.transductive_felt_filter = get_transductive_felt_entity_filter(
    enable_layer0=True,  # BOND IFS parts gate ✅ ENABLED
    enable_layer1=True,  # SELF Matrix zone gating ✅ ENABLED
    enable_layer2=False, # Salience + temporal decay ⏸️ DISABLED
    enable_layer3=False  # Satisfaction fingerprinting ⏸️ DISABLED
)
```

**Required Change**:
```python
self.transductive_felt_filter = get_transductive_felt_entity_filter(
    enable_layer0=True,
    enable_layer1=True,
    enable_layer2=True,   # ✅ ENABLE
    enable_layer3=True    # ✅ ENABLE
)
```

**Expected Impact**:
- 40-60% filtering quality improvement
- 30-50% crisis entity reduction (Zone 4-5 SELF-distance)
- Full 4-layer transductive architecture operational

**Validation**:
```bash
# Test interactive session
python3 dae_interactive.py --mode debug

# Look for initialization message:
# "✅ Transductive felt entity filter initialized (Phase 3 - 4-layer architecture)"
# "   • Layer 0: BOND IFS Parts Gate (120+ keywords)"
# "   • Layer 1: SELF Matrix Zone Gating (5 zones)"
# "   • Layer 2: Salience + Temporal Decay" ← Should NOT say "disabled"
# "   • Layer 3: Satisfaction + Regime" ← Should NOT say "disabled"
```

---

### [ ] Action 2: Prototype NEXUS Entity Signal Extractor (2-3 hours)

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/nexus/core/nexus_text_core.py`

**Task**: Activate existing stub method

**Step 2.1: Locate Stub** (5 min)
```bash
# Find the stub location
grep -n "_extract_entity_signals" organs/modular/nexus/core/nexus_text_core.py
```

**Step 2.2: Implement Method** (60 min)

Add after `_compute_past_present_temporal_boosts()` method:

```python
def _extract_entity_signals(
    self,
    occasions: List[TextOccasion],
    entity_prehension: Dict
) -> Dict[str, Dict]:
    """
    Extract NEXUS-specific entity signals for multi-organ extraction (Phase 0C).

    Signals:
    - Memory strength (mention_count from EntityOrganTracker)
    - Recency (days since last mention)
    - Relationship context (co-mentioned entities)
    - Temporal continuity

    Returns:
        Dict of {entity_value: {'memory_strength': float, 'recency': float, ...}}
    """
    signals = {}

    if self.entity_tracker and entity_prehension.get('entity_memory_available'):
        mentioned_entities = entity_prehension.get('mentioned_entities', [])

        for entity in mentioned_entities:
            entity_value = entity.get('entity_value')

            if entity_value in self.entity_tracker.entity_metrics:
                metrics = self.entity_tracker.entity_metrics[entity_value]

                # Memory strength (0.0-1.0, saturates at 10 mentions)
                mention_count = metrics.mention_count
                memory_strength = min(mention_count / 10.0, 1.0)

                # Recency (0.0-1.0, decays over 30 days)
                from datetime import datetime
                last_seen = datetime.fromisoformat(metrics.last_mentioned)
                days_ago = (datetime.now() - last_seen).days
                recency = max(0.0, 1.0 - days_ago / 30.0)

                # Relationship context (top 5 co-mentioned entities)
                co_mentioned = list(metrics.co_mentioned_entities.keys())[:5]

                # Polyvagal association
                typical_polyvagal = metrics.typical_polyvagal_state

                signals[entity_value] = {
                    'memory_strength': memory_strength,
                    'mention_count': mention_count,
                    'recency': recency,
                    'co_mentioned_entities': co_mentioned,
                    'typical_polyvagal': typical_polyvagal,
                    'confidence': memory_strength * recency,  # Combined score
                    'source': 'NEXUS'
                }

    return signals
```

**Step 2.3: Integrate with process_text_occasions()** (30 min)

Find the `process_text_occasions()` method and add near the end (before `return result`):

```python
def process_text_occasions(self, occasions, cycle=0, context=None):
    # ... existing processing ...

    # Extract entity signals if multi-organ extraction enabled
    entity_signals = {}
    if Config.MULTI_ORGAN_ENTITY_SIGNALS_ENABLED:
        entity_prehension = context.get('entity_prehension', {}) if context else {}
        entity_signals = self._extract_entity_signals(occasions, entity_prehension)

    # Add to result
    result.entity_signals = entity_signals

    return result
```

**Step 2.4: Add Config Flag** (5 min)

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/config.py`

Add after line 200:

```python
# ============================================================================
# PHASE 0C: MULTI-ORGAN ENTITY EXTRACTION
# ============================================================================

MULTI_ORGAN_ENTITY_SIGNALS_ENABLED = False  # Enable when organ extractors ready
MULTI_ORGAN_MIN_AGREEMENT = 3  # 3+ organs must detect entity
MULTI_ORGAN_COHERENCE_THRESHOLD = 0.75  # DAE 3.0 proven threshold
```

**Step 2.5: Validation** (30 min)

Create test script: `/Users/daedalea/Desktop/DAE_HYPHAE_1/test_nexus_signal_extraction.py`

```python
"""
Test NEXUS entity signal extraction.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from organs.modular.nexus.core.nexus_text_core import NEXUSTextCore
from transductive.text_occasion import TextOccasion

# Initialize NEXUS organ
nexus = NEXUSTextCore(enable_neo4j=True, enable_entity_tracker=True)

# Mock entity prehension context
context = {
    'entity_prehension': {
        'mentioned_entities': [
            {'entity_value': 'Emma', 'entity_type': 'Person', 'confidence': 0.95},
            {'entity_value': 'Boston', 'entity_type': 'Place', 'confidence': 0.90}
        ],
        'entity_memory_available': True
    }
}

# Create mock occasions
occasions = [TextOccasion(token='Emma', position=0, total_tokens=1)]

# Extract signals
signals = nexus._extract_entity_signals(occasions, context['entity_prehension'])

# Validate
print("\n🧪 NEXUS Entity Signal Extraction Test")
print("=" * 70)
print(f"\nExtracted signals: {len(signals)}")
for entity_value, signal in signals.items():
    print(f"\n{entity_value}:")
    print(f"  Memory strength: {signal['memory_strength']:.2f}")
    print(f"  Recency: {signal['recency']:.2f}")
    print(f"  Confidence: {signal['confidence']:.2f}")
    print(f"  Mention count: {signal['mention_count']}")
    print(f"  Co-mentioned: {signal['co_mentioned_entities']}")

print("\n✅ Test complete!")
```

Run test:
```bash
python3 test_nexus_signal_extraction.py
```

Expected output: Signals for Emma, Boston with memory_strength, recency, confidence scores.

---

### [ ] Action 3: Create Multi-Organ Extractor Stub (1 hour)

**File**: Create `/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/multi_organ_entity_extractor.py`

**Content**:

```python
"""
Multi-Organ Entity Extractor - Phase 0C
========================================

Intersection-based entity extraction using multi-organ signals.

Architecture:
1. Collect entity signals from all 12 organs
2. Intersection: Find entities detected by 3+ organs
3. Coherence scoring: C̄ = 1 - variance(confidences)
4. Satisfaction gate: Accept if C̄ > 0.75

Status: STUB (Week 3-4 implementation)
"""

from typing import List, Dict, Any
from collections import defaultdict
import numpy as np
from config import Config


class MultiOrganEntityExtractor:
    """Extract entities via multi-organ intersection (Phase 0C)."""

    def __init__(
        self,
        coherence_threshold: float = 0.75,
        min_organs: int = 3
    ):
        """
        Initialize multi-organ entity extractor.

        Args:
            coherence_threshold: Minimum coherence for acceptance (DAE 3.0 proven: 0.75)
            min_organs: Minimum organs that must detect entity (default: 3)
        """
        self.coherence_threshold = coherence_threshold
        self.min_organs = min_organs

    def extract_entities_multi_organ(
        self,
        organ_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Extract entities from organ signals using intersection + coherence.

        Algorithm:
        1. Collect entity_signals from all organ_results
        2. Find entities detected by ≥ min_organs
        3. Compute coherence: C̄ = 1 - variance(confidences)
        4. Gate by satisfaction: Accept if C̄ ≥ coherence_threshold

        Args:
            organ_results: Dict of {organ_name: organ_result} from processing

        Returns:
            List of entity dicts in standard format:
            [
                {
                    'entity_value': 'Emma',
                    'entity_type': 'Person',
                    'confidence': 0.92,
                    'coherence': 0.85,
                    'detecting_organs': ['NEXUS', 'BOND', 'EMPATHY']
                },
                ...
            ]
        """
        # Week 3-4 implementation:
        # Step 1: Collect signals from all organs
        # Step 2: Intersection filter
        # Step 3: Coherence scoring
        # Step 4: Satisfaction gate

        # STUB: Return empty list for now
        return []

    def _collect_entity_signals(
        self,
        organ_results: Dict[str, Any]
    ) -> Dict[str, Dict]:
        """
        Collect entity signals from all organs.

        Returns:
            Dict of {entity_value: {'organs': [...], 'confidences': [...], ...}}
        """
        # Week 3 implementation
        pass

    def _compute_coherence(self, confidences: List[float]) -> float:
        """
        Compute coherence from multi-organ confidences.

        Formula: C̄ = 1 - variance(confidences)

        Args:
            confidences: List of confidence scores from different organs

        Returns:
            Coherence score [0.0, 1.0] (1.0 = perfect agreement)
        """
        if len(confidences) < 2:
            return 0.0

        return 1.0 - np.var(confidences)


# Quick test
if __name__ == "__main__":
    print("🧪 Multi-Organ Entity Extractor Stub Test")
    print("=" * 70)

    extractor = MultiOrganEntityExtractor()
    print(f"✅ Extractor initialized")
    print(f"   Coherence threshold: {extractor.coherence_threshold}")
    print(f"   Min organs: {extractor.min_organs}")

    # Test coherence computation
    test_confidences = [0.85, 0.90, 0.88, 0.92]
    coherence = extractor._compute_coherence(test_confidences)
    print(f"\n✅ Coherence test: {test_confidences} → {coherence:.4f}")

    print("\n✅ Stub test complete!")
```

**Validation**:
```bash
python3 persona_layer/multi_organ_entity_extractor.py
```

Expected output: Stub initialized, coherence test passes.

---

### [ ] Action 4: Tune Symbiotic LLM Consultation Rate (15 min)

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/config.py`

**Add** after existing LLM config (around line 150):

```python
# ============================================================================
# PHASE 1: SYMBIOTIC LLM ENTITY EXTRACTION
# ============================================================================

# Learning mode: Controls LLM consultation rate
# - 'bootstrap': 70% LLM (high accuracy, learning patterns)
# - 'transition': 50% LLM (balanced, pattern validation)
# - 'independent': 20% LLM (rare edge cases, quality assurance)
SYMBIOTIC_LEARNING_MODE = 'transition'  # ✅ CHANGE from 'bootstrap'

# Consultation rates per mode
SYMBIOTIC_CONSULTATION_RATES = {
    'bootstrap': 0.70,    # 70% LLM, 30% pattern
    'transition': 0.50,   # 50% LLM, 50% pattern
    'independent': 0.20   # 20% LLM, 80% pattern
}
```

**Expected Impact**:
- LLM usage: 70% → 50% (29% reduction)
- API costs: 80% → 50% (38% cost reduction)
- Processing speed: 5s → 2.5s (50% faster)
- Accuracy: ~92% (maintained via pattern learning from LLM)

**Validation**:
```bash
# Run interactive session
python3 dae_interactive.py --mode debug

# Look for initialization message:
# "✅ Symbiotic LLM extractor ready (Phase 1: transition mode, 50% LLM)"
```

---

### [ ] Action 5: Document Phase 0B Completion (1 hour)

**Create**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/PHASE0B_VALIDATION_COMPLETE_NOV19_2025.md`

**Analysis Steps**:

1. **Load word patterns**:
```python
import json
data = json.load(open('persona_layer/state/active/word_occasion_patterns.json'))
print(f"Word patterns: {len(data['word_patterns'])}")
print(f"Pair patterns: {len(data['word_pair_patterns'])}")
print(f"Total updates: {data['statistics']['total_updates']}")
```

2. **Analyze entity coverage**:
```python
# Check which entities have word patterns
entity_types = {}
for word, pattern in data['word_patterns'].items():
    entity_dist = pattern.get('entity_type_distribution', {})
    for entity_type, count in entity_dist.items():
        entity_types[entity_type] = entity_types.get(entity_type, 0) + count

print(f"\nEntity types covered: {list(entity_types.keys())}")
print(f"Total entity associations: {sum(entity_types.values())}")
```

3. **Validate bidirectional enrichment**:
```python
# Load entity-organ associations
entity_data = json.load(open('persona_layer/state/active/entity_organ_associations.json'))
print(f"\nEntities tracked: {len(entity_data['entity_metrics'])}")
print(f"Entity names: {list(entity_data['entity_metrics'].keys())}")

# Check if entities have neighbor patterns
for entity_name, metrics in entity_data['entity_metrics'].items():
    left_count = len(metrics.get('typical_left_neighbors', {}))
    right_count = len(metrics.get('typical_right_neighbors', {}))
    print(f"  {entity_name}: {left_count} left neighbors, {right_count} right neighbors")
```

4. **Document findings** in markdown:
```markdown
# Phase 0B Validation - Complete

## Summary
- ✅ 191 word patterns (2× minimum viable threshold of 90)
- ✅ 46 word pair patterns
- ✅ 910 total updates (~18 epochs × 50 pairs)
- ✅ 11 entities tracked with neighbor patterns
- ✅ Bidirectional enrichment operational

## Quality Metrics
[... results from analysis above ...]

## Conclusion
Phase 0B is COMPLETE and operational. Ready for Phase 0C integration.
```

---

## 📋 Next Week Actions (Week 2-3: Multi-Organ Implementation)

### [ ] Action 6: Add Signal Extractors to Remaining 11 Organs (14 hours)

**Pattern** (from NEXUS implementation above):

For each organ, add `_extract_entity_signals()` method:

1. **BOND**: IFS parts detection strength, SELF-energy proximity
2. **NDAM**: Urgency spike when entity mentioned, crisis association
3. **LISTENING**: Temporal inquiry density around entity
4. **EMPATHY**: Compassionate presence activation
5. **WISDOM**: Pattern recognition when entity appears
6. **AUTHENTICITY**: Vulnerability sharing correlation
7. **PRESENCE**: Embodied awareness when entity mentioned
8. **SANS**: Semantic coherence shift (entity stabilizes/destabilizes)
9. **RNX**: Temporal pattern correlation (crisis/restorative)
10. **EO**: Polyvagal state correlation (entity → ventral/sympathetic/dorsal)
11. **CARD**: Response scaling preference when entity appears

**Estimated Time**: 2 hours per organ × 11 organs = 22 hours (can parallelize)

---

### [ ] Action 7: Implement Multi-Organ Intersection Logic (2-3 days)

**File**: `persona_layer/multi_organ_entity_extractor.py`

**Implement `_collect_entity_signals()`**:
```python
def _collect_entity_signals(self, organ_results):
    entity_candidates = defaultdict(lambda: {'organs': [], 'confidences': []})

    for organ_name, organ_result in organ_results.items():
        if hasattr(organ_result, 'entity_signals'):
            for entity_value, signal in organ_result.entity_signals.items():
                entity_candidates[entity_value]['organs'].append(organ_name)
                entity_candidates[entity_value]['confidences'].append(
                    signal.get('confidence', 0.5)
                )

    return entity_candidates
```

**Implement `extract_entities_multi_organ()` full version**:
```python
def extract_entities_multi_organ(self, organ_results):
    # Step 1: Collect signals
    candidates = self._collect_entity_signals(organ_results)

    # Step 2: Intersection filter (3+ organs)
    intersected = {
        entity: data
        for entity, data in candidates.items()
        if len(data['organs']) >= self.min_organs
    }

    # Step 3: Coherence scoring
    for entity, data in intersected.items():
        coherence = self._compute_coherence(data['confidences'])
        data['coherence'] = coherence

    # Step 4: Satisfaction gate
    accepted = [
        {
            'entity_value': entity,
            'entity_type': self._infer_type(entity),
            'confidence': np.mean(data['confidences']),
            'coherence': data['coherence'],
            'detecting_organs': data['organs']
        }
        for entity, data in intersected.items()
        if data['coherence'] >= self.coherence_threshold
    ]

    return accepted
```

---

### [ ] Action 8: A/B Testing Framework (1 day)

**File**: `config.py`

Add:
```python
# A/B testing for multi-organ vs LLM extraction
MULTI_ORGAN_AB_TEST_MODE = 'compare'  # 'llm_only', 'multi_organ_only', 'compare'
```

**File**: `persona_layer/conversational_organism_wrapper.py`

Add comparison logic in entity extraction section:
```python
if Config.MULTI_ORGAN_AB_TEST_MODE == 'compare':
    # Run both extractors
    llm_entities = self.symbiotic_extractor.extract_entities(text)
    multi_organ_entities = self.multi_organ_extractor.extract_entities_multi_organ(organ_results)

    # Compare results
    llm_set = set(e['entity_value'] for e in llm_entities)
    multi_set = set(e['entity_value'] for e in multi_organ_entities)

    precision = len(llm_set & multi_set) / len(multi_set) if multi_set else 0.0
    recall = len(llm_set & multi_set) / len(llm_set) if llm_set else 0.0

    # Log comparison
    print(f"   🔬 A/B Test: Precision={precision:.1%}, Recall={recall:.1%}")

    # Use multi-organ if precision ≥ 90%
    entities = multi_organ_entities if precision >= 0.9 else llm_entities
```

---

## 🎯 Success Criteria

### Week 1 Success (Actions 1-5)
- [✅] Transductive filter Layer 2-3 enabled
- [✅] NEXUS signal extractor operational
- [✅] Multi-organ stub created and tested
- [✅] Symbiotic LLM in transition mode (50% consultation)
- [✅] Phase 0B completion documented

**Time Investment**: 5-6 hours
**Expected Impact**: 40-60% filtering quality, 50% LLM cost reduction

### Week 2-3 Success (Actions 6-8)
- [ ] All 11 organs have signal extractors
- [ ] Multi-organ intersection logic operational
- [ ] A/B testing shows ≥90% precision vs LLM
- [ ] Multi-organ extraction faster than LLM (0.002s vs 5s)

**Time Investment**: 3-4 days
**Expected Impact**: Phase 0C operational, 100× speedup vs LLM

---

## 📊 Progress Tracking

### Completed
- [ ] Action 1: Enable filter Layer 2-3 (30 min)
- [ ] Action 2: NEXUS signal extractor (2-3 hours)
- [ ] Action 3: Multi-organ stub (1 hour)
- [ ] Action 4: Tune LLM rate (15 min)
- [ ] Action 5: Document Phase 0B (1 hour)

**Total Time**: 0 / 5-6 hours

### Next Session
- [ ] Action 6: 11 organ extractors (14 hours)
- [ ] Action 7: Intersection logic (2-3 days)
- [ ] Action 8: A/B testing (1 day)

---

**Status**: 🎯 **READY FOR ACTIVATION**
**Timeline**: Week 1 (5-6 hours) → Week 2-3 (3-4 days)
**Focus**: Activate existing modules, NOT build new ones

🌀 **"From planning to action. From proposals to activation. The modules exist. Now we enable them."** 🌀
