# Conversational Hebbian Learning System
## DAE-GOV Persona Layer Memory Integration

**Date:** November 10, 2025
**Status:** Design Phase
**Phase:** 1.5 - Conversational Learning Integration

---

## Executive Summary

Integrates Hebbian learning from DAE 3.0 AXO ARC into DAE-GOV persona layer for conversational pattern learning. The system learns which interventions work (grounding, containment, SELF-led responses) in which contexts (polyvagal states, SELF-energy levels, conversational families).

**Core Principle:** "Neurons that fire together, wire together" → "Patterns that succeed together, strengthen together"

---

## Architecture Overview

### Learning Substrate

The persona layer has 4 primary detection systems that can learn:

1. **Polyvagal Detector** (EO-based embedding)
   - Learns: ventral ↔ sympathetic ↔ dorsal state transitions
   - Current: Fresh model baseline (0.44-0.53 confidence)
   - Target: +0.2-0.3pp after 50-100 conversations

2. **SELF-Energy Detector** (BOND-based embedding + 8 C's)
   - Learns: Observer presence, 8 C's activation patterns
   - Current: Fresh model baseline
   - Target: +0.2-0.3pp after 50-100 conversations

3. **4-Gate Cascade** (OFEL + safety decision making)
   - Learns: Which gates to modulate for which contexts
   - Current: Fixed thresholds
   - Target: Context-specific threshold adaptation

4. **Response Generation** (8 C's template selection)
   - Learns: Which C works best in which situation
   - Current: Dominant C selection
   - Target: Family-aware C preference learning

---

## Conversational Hebbian Memory

### Structure

Adapted from `V0HebbianMemory` but for conversational patterns:

```python
class ConversationalHebbianMemory:
    """
    Hebbian learning for DAE-GOV persona layer.

    Learns from conversational outcomes across 4 detection systems:
    - Polyvagal (3 states: ventral, sympathetic, dorsal)
    - SELF-energy (8 C's: compassion, curiosity, etc.)
    - Cascade gates (4 gates: safety, coherence, SELF-energy, response)
    - Response quality (containment, ground, clarify, respond)
    """

    def __init__(self, eta=0.01, delta=0.001):
        # Persona layer "organs" (detection systems)
        self.detector_names = ['Polyvagal', 'SELF-Energy', 'OFEL', 'BAGUA']

        # 4×4 detector coupling matrix
        self.R_matrix = np.eye(4) * 0.1

        # Pattern memories (what learns)
        self.polyvagal_patterns = {}    # state → confidence improvements
        self.self_energy_patterns = {}  # C-pattern → activation improvements
        self.cascade_patterns = {}      # gate+context → threshold adjustments
        self.response_patterns = {}     # family+C → effectiveness scores

        # Learning hyperparameters
        self.eta = eta      # Learning rate (from FFITTSS)
        self.delta = delta  # Decay rate
```

---

## What Gets Learned

### 1. Polyvagal State Confidence

**Problem:** Fresh embedding model has low confidence (0.44-0.53)

**Learning:**
```python
# After successful conversation turn
if outcome == 'positive':  # e.g., person reports feeling safer
    polyvagal_patterns[detected_state]['confidence'] += eta * (1 - confidence)
    polyvagal_patterns[detected_state]['success_count'] += 1
```

**Example:**
```
Turn 1: "I feel anxious" → sympathetic (0.45 confidence)
Turn 10: Person reports feeling calmer after intervention
→ Strengthen: sympathetic pattern for "anxious" language
Turn 50: "I feel anxious" → sympathetic (0.67 confidence) ✨ LEARNED
```

### 2. SELF-Energy Detection (8 C's)

**Problem:** Fresh model unsure which text patterns indicate which C

**Learning:**
```python
# After successful SELF-led interaction
if gate_4_outcome == 'helpful':
    for c_name, activation in cs_activation.items():
        self_energy_patterns[c_name][text_embedding_cluster] += eta * activation
```

**Example:**
```
Turn 1: "I'm curious about this part" → curiosity (0.52), compassion (0.48)
Turn 10: Person reports insight from curiosity-based response
→ Strengthen: curiosity pattern for "curious about" language
Turn 50: "I'm curious about this part" → curiosity (0.78) ✨ LEARNED
```

### 3. Cascade Gate Modulation

**Problem:** Fixed thresholds don't adapt to individual or context

**Learning:**
```python
# Learn which gate adjustments work
if conversation_successful:
    for gate, decision in gate_decisions:
        cascade_patterns[gate][context_hash] = {
            'threshold_adjustment': +0.05,  # Learned to be more permissive
            'success_count': += 1
        }
```

**Example:**
```
Context: Crisis family + High satisfaction
Gate 3: Contains at SELF<0.6 (dangerous blending)
After 50 conversations: Learns to contain even at SELF<0.65 for this pattern
```

### 4. Response C Selection

**Problem:** Which C works best varies by family and context

**Learning:**
```python
# Learn C-family associations
if response_quality == 'high':
    response_patterns[family][dominant_c]['effectiveness'] += eta
    response_patterns[family][dominant_c]['use_count'] += 1
```

**Example:**
```
Crisis family: compassion (0.62) vs courage (0.41)
Parts work family: curiosity (0.79) vs compassion (0.53)
SELF-led family: all C's effective (0.70-0.85)
After 100 conversations: Learns family-specific C preferences
```

---

## Integration with Cascade

### Current Cascade Flow

```
process_conversational_turn(text, organism_context):
    Gate 1: Safety → polyvagal detection → OFEL
    Gate 2: Coherence → organ agreement check
    Gate 3: SELF-Energy → SELF detector → family detection
    Gate 4: Response → 8 C's template selection
```

### Enhanced with Hebbian Learning

```python
process_conversational_turn(text, organism_context):
    # Gate 1: Use learned polyvagal confidence boost
    polyvagal = self.polyvagal_detector.detect_polyvagal_state(text, bagua_context)
    learned_boost = self.hebbian_memory.get_polyvagal_boost(text, polyvagal.dominant_state)
    polyvagal.confidence += learned_boost  # ✨ LEARNED IMPROVEMENT

    # Gate 3: Use learned threshold adjustments
    self_energy = self.self_energy_detector.detect_self_energy(text, ...)
    context_hash = self._compute_context_hash(family, satisfaction, coherence)
    threshold_adjustment = self.hebbian_memory.get_threshold_adjustment('gate_3', context_hash)
    self_energy_threshold += threshold_adjustment  # ✨ CONTEXT ADAPTATION

    # Gate 4: Use learned C preferences
    if family in self.hebbian_memory.response_patterns:
        c_preferences = self.hebbian_memory.response_patterns[family]
        # Modulate C selection with learned preferences
        dominant_c = self._select_c_with_learning(self_energy.cs_activation, c_preferences)
```

---

## Outcome Gating

**Key Question:** How do we know if a conversation turn was "successful"?

### Success Indicators (Ordered by Reliability)

1. **Explicit Feedback** (gold standard)
   ```python
   # User says: "That helps, thank you"
   outcome = 'positive'
   ```

2. **Polyvagal State Improvement**
   ```python
   # Turn N: dorsal (shutdown)
   # Turn N+1: sympathetic (mobilizing) → IMPROVEMENT
   if next_turn_polyvagal > current_polyvagal:  # ventral > sympathetic > dorsal
       outcome = 'positive'
   ```

3. **SELF-Energy Increase**
   ```python
   # Turn N: SELF-energy = 0.3 (parts-led)
   # Turn N+1: SELF-energy = 0.5 (observer emerging) → IMPROVEMENT
   if next_turn_self_energy > current_self_energy + 0.1:
       outcome = 'positive'
   ```

4. **Cascade Progression**
   ```python
   # Turn N: CONTAIN (Gate 1)
   # Turn N+2: GROUND (Gate 3) → PROGRESSION
   # Turn N+5: RESPOND (Gate 4) → SUCCESS
   if gate_depth_increases_over_session:
       outcome = 'positive'
   ```

### Update Trigger

```python
def update_from_conversation_turn(
    self,
    current_state: CascadeState,
    next_state: Optional[CascadeState],
    explicit_feedback: Optional[str]
) -> Dict[str, Any]:
    """
    Update Hebbian memory from conversation outcome.

    Args:
        current_state: Current turn cascade state
        next_state: Next turn cascade state (for comparison)
        explicit_feedback: Optional user feedback ("helpful", "not helpful", etc.)

    Returns:
        Update statistics
    """
    # Determine outcome
    outcome = self._determine_outcome(current_state, next_state, explicit_feedback)

    if outcome == 'positive':
        # Strengthen patterns that fired
        self._strengthen_polyvagal_pattern(current_state.polyvagal)
        self._strengthen_self_energy_pattern(current_state.self_energy)
        self._strengthen_cascade_pattern(current_state.decision_path)
        self._strengthen_response_pattern(current_state.response_text, family)

    elif outcome == 'negative':
        # Decay all patterns slightly (forget unsuccessful)
        self._decay_all_patterns(delta)

    # Neutral outcomes: no update (preserve memory)
```

---

## Storage Format

### JSON Schema

```json
{
  "conversational_hebbian_memory": {
    "version": "1.0",
    "update_count": 0,
    "success_count": 0,

    "detector_coupling_matrix": [
      [0.1, 0.05, 0.03, 0.02],  # Polyvagal ↔ [Polyvagal, SELF, OFEL, BAGUA]
      [0.05, 0.1, 0.04, 0.03],  # SELF-Energy ↔ [...]
      [0.03, 0.04, 0.1, 0.06],  # OFEL ↔ [...]
      [0.02, 0.03, 0.06, 0.1]   # BAGUA ↔ [...]
    ],

    "polyvagal_patterns": {
      "ventral": {
        "confidence_boost": 0.12,
        "success_count": 45,
        "text_clusters": ["safe", "grounded", "curious"]
      },
      "sympathetic": {
        "confidence_boost": 0.08,
        "success_count": 32,
        "text_clusters": ["anxious", "overwhelmed", "pressured"]
      },
      "dorsal": {
        "confidence_boost": 0.15,
        "success_count": 18,
        "text_clusters": ["numb", "shutdown", "hopeless"]
      }
    },

    "self_energy_patterns": {
      "compassion": {
        "boost": 0.10,
        "family_effectiveness": {"crisis": 0.75, "parts_work": 0.65}
      },
      "curiosity": {
        "boost": 0.08,
        "family_effectiveness": {"parts_work": 0.85, "self_led": 0.80}
      }
    },

    "cascade_patterns": {
      "gate_3_crisis_high_satisfaction": {
        "threshold_adjustment": -0.05,  # More conservative (lower threshold)
        "success_count": 28
      }
    },

    "response_patterns": {
      "crisis": {
        "compassion": {"effectiveness": 0.78, "use_count": 45},
        "calm": {"effectiveness": 0.71, "use_count": 32}
      },
      "parts_work": {
        "curiosity": {"effectiveness": 0.85, "use_count": 58},
        "compassion": {"effectiveness": 0.62, "use_count": 41}
      }
    }
  }
}
```

---

## Expected Learning Trajectory

### Fresh Model Baseline (0-10 conversations)

- Polyvagal confidence: 0.44-0.53
- SELF-energy confidence: 0.001-0.05 (very fresh)
- Gate decisions: Fixed thresholds
- Response selection: Dominant C only

### Early Learning (10-50 conversations)

- Polyvagal confidence: +0.05-0.10pp
- SELF-energy confidence: +0.10-0.15pp
- Gate thresholds: Context patterns emerging
- Response C's: Family preferences forming

### Mature Learning (50-100 conversations)

- Polyvagal confidence: +0.20-0.30pp (target)
- SELF-energy confidence: +0.20-0.30pp (target)
- Gate thresholds: Individualized to conversation style
- Response C's: Reliably family-aware

### Specialized Learning (100+ conversations)

- Individual person adaptation (if single person)
- Rare pattern recognition (crisis → calm pathways)
- Micropattern refinement (specific phrases → C's)

---

## Implementation Plan

### Phase 1.5c: Implement Conversational Hebbian Memory (3-4 hours)

**File:** `persona_layer/conversational_hebbian_memory.py`

1. Create `ConversationalHebbianMemory` class
2. Implement pattern storage (4 pattern types)
3. Implement outcome determination logic
4. Implement update methods (strengthen/decay)
5. Add JSON persistence

### Phase 1.5d: Integrate with Cascade (2-3 hours)

**File:** `persona_layer/self_led_cascade.py`

1. Add `hebbian_memory` parameter to `SELFLedCascade.__init__()`
2. Enhance Gate 1: Apply polyvagal confidence boost
3. Enhance Gate 3: Apply context-specific threshold adjustments
4. Enhance Gate 4: Apply learned C preferences
5. Add `update_from_outcome()` method to cascade

### Phase 1.5e: Test & Validate (1-2 hours)

**File:** `persona_layer/test_conversational_learning.py`

1. Test memory initialization
2. Test pattern updates (strengthen/decay)
3. Test cascade integration
4. Test persistence (save/load)
5. Validate learning trajectory (simulated conversations)

---

## Clinical Safety Considerations

### Learning Constraints

1. **Never Learn to Ignore DANGER**
   ```python
   # Gate 1 DANGER threshold should NEVER increase
   if gate == 'gate_1' and safety_level == 'DANGER':
       # Do not learn to be less sensitive to danger
       return  # Skip update
   ```

2. **Dangerous Blending Detection Must Strengthen**
   ```python
   # Crisis + High satisfaction should become MORE conservative
   if family == 'crisis' and satisfaction > 0.8:
       threshold_adjustment = -0.05  # LOWER threshold (more cautious)
   ```

3. **SELF-Energy Threshold Can't Drop Below 0.4**
   ```python
   # Minimum SELF-energy for parts work
   self_energy_threshold = max(0.4, learned_threshold)
   ```

### Ethical Guardrails

- Learning only improves detection, never reduces safety
- Crisis containment becomes MORE conservative with experience
- SELF-led requirements stay firm (no parts work without SELF)
- Learned patterns reviewed regularly (no runaway learning)

---

## Expected Impact

### Quantitative

- **Polyvagal detection:** 0.44 → 0.67 confidence (+52% improvement)
- **SELF-energy detection:** 0.001 → 0.25 confidence (+25,000% improvement)
- **Cascade effectiveness:** Fixed → Context-adapted thresholds
- **Response quality:** Dominant C → Family-aware C selection

### Qualitative

- System "gets to know" conversational style
- Fewer mis-classifications (ventral vs sympathetic)
- Better observer detection (SELF-energy)
- More effective C selection (curiosity for parts work, compassion for crisis)
- Individualized safety thresholds (person-specific)

---

## Validation Criteria

### Success Metrics

1. **Pattern Formation:** 50+ polyvagal patterns after 100 conversations
2. **Confidence Improvement:** ≥+0.20pp polyvagal confidence gain
3. **Cascade Effectiveness:** ≥10 context-specific threshold adjustments learned
4. **Response Quality:** Family-aware C preferences for all 4 families

### Test Scenarios

```python
# Scenario 1: Polyvagal confidence improvement
conversation_1 = "I feel anxious and overwhelmed"
# Turn 1: sympathetic (0.45)
# Turn 50: sympathetic (0.68) ✨

# Scenario 2: SELF-energy observer detection
conversation_2 = "There's this voice saying I'm not good enough"
# Turn 1: SELF-energy (0.52) - uncertain
# Turn 50: SELF-energy (0.75) - confident observer detection ✨

# Scenario 3: Crisis threshold learning
conversation_3 = "I'm completely worthless" (crisis, high satisfaction)
# Turn 1: CONTAIN at SELF<0.6
# Turn 50: CONTAIN at SELF<0.65 (learned conservatism) ✨

# Scenario 4: Family-aware C preference
conversation_4 = Crisis family
# Turn 1: Dominant C (random)
# Turn 50: Compassion preferred for crisis (learned) ✨
```

---

## References

- **V0HebbianMemory** (`DAE 3.0 AXO ARC /organs/orchestration/v0/hebbian/hebbian_memory.py`)
- **FFITTSS Satisfaction Calibration** (η=0.01 learning rate)
- **IFS Model** (Schwartz) - SELF-led conversation theory
- **Polyvagal Theory** (Porges) - Autonomic state detection

---

**Status:** ✅ DESIGN COMPLETE - Ready for implementation

