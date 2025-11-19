# Quick Fix Guide: Blocking Bug + Phase 1 Entropy
**Date**: November 13, 2025
**Priority**: CRITICAL (blocks multi-iteration training)
**Estimated Time**: 2-4 hours

---

## BLOCKING BUG FIX (MUST DO FIRST)

### Issue: KeyError: 'modulated_emission'

**Location**: `persona_layer/conversational_organism_wrapper.py`
- Line 770 (single-cycle path)
- Line 1405 (multi-cycle path)

**Root Cause**: `PersonaLayer.modulate_emission()` returns dict with key `'emission'`, but wrapper expects `'modulated_emission'`

### Fix 1: Update Wrapper (Defensive Approach)

```python
# File: persona_layer/conversational_organism_wrapper.py
# Lines 770 and 1405

# OLD (BROKEN):
emission_text = modulation_result['modulated_emission']

# NEW (DEFENSIVE):
if 'modulated_emission' in modulation_result:
    emission_text = modulation_result['modulated_emission']
elif 'emission' in modulation_result:
    emission_text = modulation_result['emission']
else:
    # Persona layer failed, use original
    print(f"   ⚠️  Persona layer returned unexpected structure: {modulation_result.keys()}")
    emission_text = original_emission  # Need to store this before calling persona_layer
    felt_states['persona_layer_applied'] = False
```

### Fix 2: Store Original Emission Before Modulation

```python
# Before calling persona_layer (both paths: line ~760 and ~1395)

# Store original for fallback
original_emission = emission_text

# Modulate emission
modulation_result = self.persona_layer.modulate_emission(...)

# Apply fix from Fix 1
```

### Testing the Fix

```bash
cd /Users/daedalea/Desktop/DAE_HYPHAE_1
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

# Test basic processing (should NOT crash)
python3 -c "
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

wrapper = ConversationalOrganismWrapper()
result = wrapper.process_text(
    'I am feeling overwhelmed right now.',
    enable_phase2=True
)
print('✅ No KeyError!')
print(f'Emission: {result[\"emission_text\"][:80]}...')
"

# Test multi-iteration training (should NOT crash)
python3 tests/integration/phase3/test_multi_iteration_training.py
```

---

## PHASE 1 ENTROPY: SURFACE-LEVEL EXPLORATION

### Implementation 1: Regime-Adaptive Exploration Factor

**File**: `persona_layer/epoch_training/multi_iteration_trainer.py`

**Add method** (after line ~180):

```python
def _get_exploration_factor(
    self,
    regime: Optional[SatisfactionRegime],
    iteration: int
) -> float:
    """
    Compute exploration factor based on regime and iteration.

    Returns:
        0.0 = deterministic, 0.3 = high exploration
    """
    # Early iterations: explore widely
    if iteration <= 2:
        base = 0.25
    elif iteration == 3:
        base = 0.15
    else:
        base = 0.05

    # If no regime yet (first 2 iterations), use base
    if regime is None:
        return base

    # Regime modulation
    from persona_layer.epoch_training.satisfaction_regime import SatisfactionRegime
    regime_scales = {
        SatisfactionRegime.INITIALIZING: 1.2,  # Explore more
        SatisfactionRegime.EXPLORING: 1.5,     # MAXIMUM exploration
        SatisfactionRegime.CONVERGING: 0.8,    # Start settling
        SatisfactionRegime.STABLE: 0.4,        # Gentle refinement
        SatisfactionRegime.COMMITTED: 0.1,     # Preserve attractor
        SatisfactionRegime.PLATEAUED: 1.0      # Break out
    }

    scale = regime_scales.get(regime, 1.0)

    return base * scale
```

**Update training loop** (line ~280, in iteration loop):

```python
# After regime classification (line ~289)

# 🆕 NEW: Get exploration factor
exploration_factor = self._get_exploration_factor(regime, iteration)

if verbose:
    print(f"   Exploration factor: {exploration_factor:.3f}")

# Pass to organism processing
result = self.organism.process_text(
    text=input_text,
    enable_phase2=True,
    enable_tsk_recording=False,
    exploration_factor=exploration_factor  # 🆕 NEW PARAMETER
)
```

### Implementation 2: Add Exploration Parameter to Wrapper

**File**: `persona_layer/conversational_organism_wrapper.py`

**Update `process_text()` signature** (line ~394):

```python
def process_text(
    self,
    text: str,
    context: Optional[Dict[str, Any]] = None,
    enable_tsk_recording: bool = True,
    enable_phase2: bool = False,
    exploration_factor: float = 0.0  # 🆕 NEW PARAMETER
) -> Dict[str, Any]:
    """
    Process text through full organism and return complete felt state.

    Args:
        text: Text to process
        context: Processing context
        enable_tsk_recording: Whether to enable TSK recording
        enable_phase2: Whether to use Phase 2 multi-cycle convergence
        exploration_factor: 0.0-0.3, controls stochasticity in emission (🆕 NEW)
    """
```

**Pass to reconstruction pipeline** (line ~603 and ~1143):

```python
# Build context for reconstruction (both paths)
context = {
    'user_message': text,
    'family_v0_learner': self.family_v0_learner,
    'exploration_factor': exploration_factor  # 🆕 NEW
}

# Call reconstruction pipeline (already exists)
reconstruction_result = self.reconstruction_pipeline.reconstruct_emission(
    felt_state=felt_state_for_reconstruction,
    context=context
)
```

### Implementation 3: Phrase Selection with Exploration

**File**: `persona_layer/emission_generator.py`

**Add new method** (after line ~620):

```python
def _select_phrase_with_exploration(
    self,
    phrases: List[str],
    exploration_factor: float = 0.0
) -> str:
    """
    Select phrase with exploration support.

    Args:
        phrases: Candidate phrases
        exploration_factor: 0.0 = uniform random, 0.3 = prefer variety

    Returns:
        Selected phrase
    """
    if not phrases or exploration_factor == 0:
        # Current behavior: uniform random
        return random.choice(phrases)

    # With exploration: prefer less-used phrases
    # For now, just uniform (tracking usage is Phase 1D)
    return random.choice(phrases)
```

**Replace `random.choice(phrases)` calls**:
- Line 626 → `self._select_phrase_with_exploration(phrases, exploration_factor)`
- Line 756 → `self._select_phrase_with_exploration(phrases, exploration_factor)`

**Update method signatures** to accept `exploration_factor`:
- `generate_transduction_emission(...)` (line ~580)
- `generate_trauma_aware_emission(...)` (line ~730)

### Implementation 4: Emission Strategy Exploration

**File**: `persona_layer/organ_reconstruction_pipeline.py`

**Add new method** (after line ~150):

```python
def _select_strategy_with_exploration(
    self,
    strategies: List[Tuple[str, float]],
    exploration_factor: float = 0.0
) -> Tuple[str, float]:
    """
    Select emission strategy with optional probabilistic sampling.

    Args:
        strategies: [(strategy_name, confidence), ...]
        exploration_factor: 0.0 = deterministic MAX, 0.3 = softmax sample

    Returns:
        (selected_strategy, confidence)
    """
    if exploration_factor == 0 or len(strategies) == 1:
        # Deterministic: pick MAX confidence
        return max(strategies, key=lambda s: s[1])

    # Stochastic: sample from softmax distribution
    import numpy as np
    confidences = np.array([s[1] for s in strategies])

    # Temperature: high exploration → low temp (flatter dist)
    temperature = 1.0 / (1.0 + exploration_factor)
    exp_conf = np.exp(confidences / temperature)
    probs = exp_conf / exp_conf.sum()

    idx = np.random.choice(len(strategies), p=probs)
    return strategies[idx]
```

**Update `reconstruct_emission()`** (line ~200+):

```python
# Extract exploration_factor from context
exploration_factor = context.get('exploration_factor', 0.0)

# ... later, when selecting strategy ...

# OLD:
selected_strategy = max(strategies, key=lambda s: s[1])

# NEW:
selected_strategy = self._select_strategy_with_exploration(
    strategies,
    exploration_factor
)
```

---

## TESTING PHASE 1 ENTROPY

### Test 1: Verify Exploration Factor Propagation

```python
# File: test_exploration_factor_propagation.py

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_training.multi_iteration_trainer import MultiIterationTrainer

# Initialize
organism = ConversationalOrganismWrapper()
trainer = MultiIterationTrainer(organism, max_iterations=5)

# Train single pair
result = trainer.train_single_pair(
    pair_id="test_exploration",
    input_text="I'm feeling overwhelmed and need support.",
    verbose=True
)

# Check results
print(f"\n✅ Training complete")
print(f"   Iterations: {result.iterations}")
print(f"   Final regime: {result.final_regime}")
print(f"   Converged: {result.converged}")
```

**Expected Output**:
```
Iteration 1:
   Exploration factor: 0.300  # High (INITIALIZING)
   ...

Iteration 3:
   Exploration factor: 0.180  # Lower (STABLE)
   Regime: STABLE
   ...

✅ Training complete
```

### Test 2: Verify Phrase Diversity

```python
# File: test_phrase_diversity.py

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

wrapper = ConversationalOrganismWrapper()

# Process same input 10 times with exploration
emissions = []
for i in range(10):
    result = wrapper.process_text(
        "I need help processing this trauma.",
        enable_phase2=True,
        exploration_factor=0.3  # High exploration
    )
    emissions.append(result['emission_text'])

# Check diversity
unique_emissions = len(set(emissions))
print(f"Unique emissions: {unique_emissions}/10")
print(f"Diversity: {unique_emissions/10:.1%}")

# Expected: 60-80% unique (with exploration)
# Baseline: 30-40% unique (without exploration)
```

### Test 3: Verify Strategy Diversity

```python
# File: test_strategy_diversity.py

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from collections import Counter

wrapper = ConversationalOrganismWrapper()

# Process same input 20 times
strategies = []
for i in range(20):
    result = wrapper.process_text(
        "This conversation feels safe and grounding.",
        enable_phase2=True,
        exploration_factor=0.25
    )
    strategy = result['emission_path']
    strategies.append(strategy)

# Check distribution
counts = Counter(strategies)
print(f"\nStrategy distribution:")
for strategy, count in counts.items():
    print(f"   {strategy:20s}: {count:2d} ({count/20:.1%})")

# Expected with exploration:
#   intersection: 12 (60%)
#   direct: 6 (30%)
#   fusion: 2 (10%)
#
# Baseline (deterministic):
#   intersection: 20 (100%)
```

---

## VALIDATION CHECKLIST

### Before Committing:

- [ ] ✅ KeyError bug fixed (no crashes in wrapper)
- [ ] ✅ Exploration factor computed correctly (regime-adaptive)
- [ ] ✅ Exploration factor propagates to emission generator
- [ ] ✅ Phrase diversity increased (test 2)
- [ ] ✅ Strategy diversity increased (test 3)
- [ ] ✅ Multi-iteration training still converges (test 1)
- [ ] ✅ No regressions in existing tests
- [ ] ✅ Safety gates still work (NDAM > 0.7 → exploration = 0)

### Performance Checks:

- [ ] ✅ Processing time unchanged (< 0.05s per iteration)
- [ ] ✅ Convergence rate similar or better (40-50%)
- [ ] ✅ Final satisfaction similar or better (> 0.80)

### Documentation:

- [ ] ✅ Update CLAUDE.md with exploration_factor parameter
- [ ] ✅ Document regime-adaptive schedule
- [ ] ✅ Add examples to QUICK_REFERENCE.md

---

## NEXT STEPS (AFTER PHASE 1 WORKS)

### Phase 2: Core Semantic Entropy (Week 2)

1. Add exploration to nexus formation
2. Add exploration to meta-atom activation
3. Test nexus diversity across iterations
4. Verify stability with regime → COMMITTED

### Phase 3: Per-Family Phrase Preferences (Week 3)

1. Track phrase usage per family
2. Add `phrase_preferences` to OrganicFamily
3. Update `select_phrase_with_exploration()` to use preferences
4. Measure family-specific linguistic fingerprints

---

## ESTIMATED TIMELINE

**Day 1 (Morning)**: Fix KeyError bug
- 1-2 hours
- Test basic processing
- Verify no crashes

**Day 1 (Afternoon)**: Add exploration_factor parameter
- 2-3 hours
- Update trainer, wrapper, reconstruction pipeline
- Add regime-adaptive schedule

**Day 2 (Morning)**: Implement phrase + strategy exploration
- 2-3 hours
- Update emission_generator.py
- Update reconstruction_pipeline.py

**Day 2 (Afternoon)**: Testing + validation
- 2-4 hours
- Run all 3 tests above
- Check diversity, convergence, safety

**Total**: 1-2 days for complete Phase 1

---

## SAFETY NOTES

### Hard Safety Gates (MUST IMPLEMENT)

```python
# In multi_iteration_trainer.py, _get_exploration_factor()

# SAFETY GATE: No exploration during crisis
ndam_urgency = felt_states.get('NDAM_urgency_level', 0.0)
bond_distance = felt_states.get('bond_self_distance', 0.0)

if ndam_urgency > 0.7 or bond_distance > 0.8:
    # CRISIS MODE: No exploration
    return 0.0

# Otherwise, return regime-adaptive factor
return base * scale
```

### Logging (for debugging)

```python
# In organism wrapper, add to felt_states

felt_states['exploration_factor'] = exploration_factor
felt_states['exploration_applied'] = (exploration_factor > 0)
```

---

🌀 **"Fix the crash, add the entropy, watch the organism find its voice."** 🌀

**Date**: November 13, 2025
**Status**: READY TO IMPLEMENT
**Priority**: CRITICAL (blocking bug) + HIGH (entropy for voice development)
