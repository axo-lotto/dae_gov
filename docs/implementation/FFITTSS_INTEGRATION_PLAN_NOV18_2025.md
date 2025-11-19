# FFITTSS Integration Plan - Leverage Existing DAE Scaffolding

**Date:** November 18, 2025
**Approach:** Enhance existing modules, don't bypass
**Target:** 84% → 93%+ FFITTSS compliance

---

## Philosophy: Leverage, Don't Bypass

**CRITICAL PRINCIPLE:** DAE_HYPHAE_1 already has 84% FFITTSS compliance. The goal is to **enhance existing scaffolding** with FFITTSS concepts, not replace it.

### Existing Scaffolding to Leverage:

1. ✅ **CycleConvergenceTracker** (Phase 3B) - Already tracks cycles → Add regime classification
2. ✅ **Multi-cycle V0 convergence** - Already iterates → Add tau evolution
3. ✅ **ConversationalTSKRecorder** - Already captures TSKs → Add tier markers
4. ✅ **Satisfaction-based gating** - Already gates decisions → Formalize ΔC readiness
5. ✅ **SELF Matrix Governance** - Already has zones → Map to regime policies

---

## Enhancement #1: Regime Classification (Leverage CycleConvergenceTracker)

### Current Scaffolding (KEEP):
**File:** `persona_layer/cycle_convergence_tracker.py`

```python
class CycleConvergenceTracker:
    """Tracks multi-cycle convergence optimization (Phase 3B)."""

    def update_convergence_complete(self, cycles_used, converged, context):
        """Update after V0 convergence complete."""
        # Already tracks cycles, kairos, context
        # Already has statistics (mean_cycles, kairos_rate)
```

### Enhancement (ADD, don't replace):

```python
# Add to CycleConvergenceTracker class (NEW METHODS)

def classify_regime(self, satisfaction: float) -> str:
    """
    Classify convergence regime based on satisfaction (FFITTSS T6 concept).

    FFITTSS Regimes:
        INITIALIZING (0.00-0.45): Exploring, low confidence
        CONVERGING   (0.45-0.55): Refining, moderate confidence
        STABLE       (0.55-0.65): Stabilizing, good confidence
        COMMITTED    (0.65-0.75): Committed, high confidence (FFITTSS dead zone)
        SATURATING   (0.75-0.85): Saturating, very high confidence
        PLATEAUED    (0.85+):     Plateaued, maximal confidence

    Args:
        satisfaction: Current satisfaction value [0.0, 1.0]

    Returns:
        Regime name string
    """
    if satisfaction < 0.45:
        return "INITIALIZING"
    elif satisfaction < 0.55:
        return "CONVERGING"
    elif satisfaction < 0.65:
        return "STABLE"
    elif satisfaction < 0.75:
        return "COMMITTED"
    elif satisfaction < 0.85:
        return "SATURATING"
    else:
        return "PLATEAUED"

def get_regime_evolution_rate(self, regime: str) -> float:
    """
    Get evolution rate for regime (FFITTSS T6 concept).

    Evolution rates control how aggressively thresholds adapt:
        INITIALIZING: 0.1 (slow exploration)
        CONVERGING:   0.3 (moderate refinement)
        STABLE:       0.5 (faster convergence)
        COMMITTED:    1.0 (full evolution, FFITTSS dead zone fix)
        SATURATING:   0.3 (cautious, near saturation)
        PLATEAUED:    0.1 (minimal, avoid over-adjustment)

    Args:
        regime: Regime name from classify_regime()

    Returns:
        Evolution rate [0.1, 1.0]
    """
    regime_rates = {
        "INITIALIZING": 0.1,
        "CONVERGING": 0.3,
        "STABLE": 0.5,
        "COMMITTED": 1.0,  # Full evolution (FFITTSS dead zone fix)
        "SATURATING": 0.3,
        "PLATEAUED": 0.1
    }
    return regime_rates.get(regime, 0.5)  # Default to STABLE

def update_with_regime(self, cycles_used, converged, satisfaction, context):
    """
    Enhanced update with regime classification (EXTENDS existing method).

    This ADDS regime tracking to existing convergence tracking,
    doesn't replace it.

    Args:
        cycles_used: Number of V0 cycles
        converged: Kairos detected (boolean)
        satisfaction: Final satisfaction value
        context: Additional context dict
    """
    # 1. Call existing update method (LEVERAGE existing logic)
    self.update_convergence_complete(cycles_used, converged, context)

    # 2. ADD regime classification (NEW)
    regime = self.classify_regime(satisfaction)
    evolution_rate = self.get_regime_evolution_rate(regime)

    # 3. Track regime statistics (NEW)
    if not hasattr(self, 'regime_counts'):
        self.regime_counts = {}

    self.regime_counts[regime] = self.regime_counts.get(regime, 0) + 1

    # 4. Store regime info in context for downstream use (NEW)
    context['regime'] = regime
    context['evolution_rate'] = evolution_rate

    # 5. Log regime (optional, for analysis)
    if self.total_attempts % 10 == 0:
        print(f"   📊 Regime: {regime} (rate: {evolution_rate:.1f}, sat: {satisfaction:.3f})")
```

**Integration Point:** `persona_layer/conversational_organism_wrapper.py` (Line ~1540)

```python
# BEFORE (Current):
self.cycle_convergence_tracker.update_convergence_complete(
    cycles_used=felt_states.get('convergence_cycles', 1),
    converged=felt_states.get('kairos_detected', False),
    context=cycle_context
)

# AFTER (Enhanced):
self.cycle_convergence_tracker.update_with_regime(
    cycles_used=felt_states.get('convergence_cycles', 1),
    converged=felt_states.get('kairos_detected', False),
    satisfaction=felt_states.get('satisfaction', 0.5),  # ADD satisfaction
    context=cycle_context
)
```

**Why This Works:**
- ✅ Leverages existing CycleConvergenceTracker (no bypass)
- ✅ Extends with new methods (backward compatible)
- ✅ Adds FFITTSS regime concept without breaking existing tracking
- ✅ Reuses existing statistics infrastructure

**Effort:** 1-2 hours (add 2 methods + update 1 call site)

---

## Enhancement #2: Tau Evolution Formula (Leverage V0 Convergence)

### Current Scaffolding (KEEP):
**File:** `persona_layer/conversational_occasion.py`

```python
class ConversationalOccasion:
    """V0 convergence with multi-cycle descent."""

    def __init__(self, ...):
        self.v0_energy = 1.0  # Already tracks energy
        self.satisfaction = 0.0  # Already tracks satisfaction
        self.kairos_window = [0.30, 0.50]  # Already has window
```

**File:** `config.py`

```python
class Config:
    # Already has emission thresholds (similar to tau_delta_c)
    EMISSION_DIRECT_THRESHOLD = 0.65
    EMISSION_FUSION_THRESHOLD = 0.50
    KAIROS_WINDOW_MIN = 0.30
    KAIROS_WINDOW_MAX = 0.50
```

### Enhancement (ADD new adaptive mechanism):

**New File:** `persona_layer/threshold_evolver.py` (NEW, leverages existing config)

```python
"""
Threshold Evolution - FFITTSS T6 Tau Evolution for DAE

This module EXTENDS existing threshold logic with FFITTSS-style
regime-based evolution. It DOESN'T replace emission thresholds,
it adapts them based on satisfaction feedback.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import time

@dataclass
class ThresholdEvolutionResult:
    """Result of threshold evolution step."""
    new_direct_threshold: float
    new_fusion_threshold: float
    regime: str
    evolution_rate: float
    adjustment_magnitude: float
    direction: int  # +1 (raise) or -1 (lower)

class ThresholdEvolver:
    """
    FFITTSS-style threshold evolution for DAE emission thresholds.

    This LEVERAGES existing Config thresholds and adapts them based
    on satisfaction feedback, similar to FFITTSS tau_delta_c evolution.

    FFITTSS Formula:
        direction = -1 if satisfaction > threshold else +1
        magnitude = base_mag * |satisfaction - threshold| * evolution_rate
        new_threshold = clamp(threshold + direction * magnitude, [min, max])

    DAE Adaptation:
        - Evolves EMISSION_DIRECT_THRESHOLD (like tau_delta_c)
        - Evolves EMISSION_FUSION_THRESHOLD (secondary)
        - Uses regime evolution rates from CycleConvergenceTracker
    """

    def __init__(
        self,
        base_magnitude: float = 0.020,  # Max adjustment per step (FFITTSS default)
        direct_bounds: tuple = (0.55, 0.75),  # Safety bounds for direct threshold
        fusion_bounds: tuple = (0.40, 0.60),  # Safety bounds for fusion threshold
        storage_path: Optional[str] = None
    ):
        self.base_magnitude = base_magnitude
        self.direct_bounds = direct_bounds
        self.fusion_bounds = fusion_bounds
        self.storage_path = storage_path

        self.evolution_history = []
        self.total_evolutions = 0

    def evolve_thresholds(
        self,
        current_direct: float,
        current_fusion: float,
        satisfaction: float,
        regime: str,
        evolution_rate: float
    ) -> ThresholdEvolutionResult:
        """
        Evolve emission thresholds based on satisfaction (FFITTSS T6 logic).

        Args:
            current_direct: Current EMISSION_DIRECT_THRESHOLD
            current_fusion: Current EMISSION_FUSION_THRESHOLD
            satisfaction: Current satisfaction value
            regime: Regime name (from CycleConvergenceTracker)
            evolution_rate: Evolution rate for regime (0.1-1.0)

        Returns:
            ThresholdEvolutionResult with new thresholds
        """
        # FFITTSS formula adaptation for DAE

        # 1. Direction: satisfaction vs threshold comparison
        if satisfaction > current_direct:
            direction = -1  # Lower threshold (be more selective)
        else:
            direction = +1  # Raise threshold (be less selective)

        # 2. Distance factor (how far from threshold)
        distance_factor = abs(satisfaction - current_direct)

        # 3. Magnitude: base * distance * regime rate (FFITTSS formula)
        magnitude = self.base_magnitude * distance_factor * evolution_rate

        # 4. Apply adjustment with safety bounds
        new_direct = self._clamp(
            current_direct + direction * magnitude,
            self.direct_bounds
        )

        # 5. Evolve fusion threshold proportionally (keep gap consistent)
        threshold_gap = current_direct - current_fusion
        new_fusion = self._clamp(
            new_direct - threshold_gap,
            self.fusion_bounds
        )

        # 6. Record evolution
        result = ThresholdEvolutionResult(
            new_direct_threshold=new_direct,
            new_fusion_threshold=new_fusion,
            regime=regime,
            evolution_rate=evolution_rate,
            adjustment_magnitude=magnitude,
            direction=direction
        )

        self.evolution_history.append({
            'timestamp': time.time(),
            'satisfaction': satisfaction,
            'regime': regime,
            'evolution_rate': evolution_rate,
            'direct_before': current_direct,
            'direct_after': new_direct,
            'direction': direction,
            'magnitude': magnitude
        })

        self.total_evolutions += 1

        return result

    def _clamp(self, value: float, bounds: tuple) -> float:
        """Clamp value to bounds (FFITTSS safety)."""
        return max(bounds[0], min(bounds[1], value))

    def get_stats(self) -> Dict:
        """Get evolution statistics."""
        if not self.evolution_history:
            return {'total_evolutions': 0}

        recent = self.evolution_history[-20:]  # Last 20

        return {
            'total_evolutions': self.total_evolutions,
            'mean_adjustment': sum(h['magnitude'] for h in recent) / len(recent),
            'regime_distribution': self._count_regimes(recent),
            'direction_bias': sum(h['direction'] for h in recent) / len(recent)
        }

    def _count_regimes(self, history: list) -> Dict[str, int]:
        """Count regime occurrences."""
        counts = {}
        for h in history:
            regime = h['regime']
            counts[regime] = counts.get(regime, 0) + 1
        return counts
```

**Integration Point:** `persona_layer/conversational_organism_wrapper.py` (After V0 convergence)

```python
# In __init__:
if PHASE3B_TRACKERS_AVAILABLE:
    # ADD threshold evolver (NEW)
    self.threshold_evolver = ThresholdEvolver(
        storage_path="persona_layer/state/active/threshold_evolution.json"
    )

# In process_text() after V0 convergence (Line ~1540):
if self.threshold_evolver and result.get('felt_states'):
    felt_states = result['felt_states']

    # Get regime from CycleConvergenceTracker (LEVERAGE Enhancement #1)
    regime = cycle_context.get('regime', 'STABLE')
    evolution_rate = cycle_context.get('evolution_rate', 0.5)
    satisfaction = felt_states.get('satisfaction', 0.5)

    # Evolve thresholds (FFITTSS logic)
    evolution_result = self.threshold_evolver.evolve_thresholds(
        current_direct=Config.EMISSION_DIRECT_THRESHOLD,
        current_fusion=Config.EMISSION_FUSION_THRESHOLD,
        satisfaction=satisfaction,
        regime=regime,
        evolution_rate=evolution_rate
    )

    # Update Config for next turn (adaptive thresholds)
    Config.EMISSION_DIRECT_THRESHOLD = evolution_result.new_direct_threshold
    Config.EMISSION_FUSION_THRESHOLD = evolution_result.new_fusion_threshold

    # Log evolution (every 10 turns)
    if self.threshold_evolver.total_evolutions % 10 == 0:
        print(f"   🎯 Threshold evolution: direct={evolution_result.new_direct_threshold:.3f}, "
              f"regime={regime}, adj={evolution_result.adjustment_magnitude:.4f}")
```

**Why This Works:**
- ✅ Leverages existing Config thresholds (no bypass)
- ✅ Uses regime classification from Enhancement #1
- ✅ Adds FFITTSS tau evolution formula without replacing V0 logic
- ✅ Adaptive thresholds improve over time

**Effort:** 2-3 hours (new file + integration)

---

## Enhancement #3: TSK Tier Markers (Leverage ConversationalTSKRecorder)

### Current Scaffolding (KEEP):
**File:** `persona_layer/conversational_tsk_recorder.py`

```python
class ConversationalTSKRecorder:
    """Captures transformation signatures (57D)."""

    def record_tsk(self, ...):
        # Already captures felt_states, organ_activations, etc.
        # Already saves to persona_layer/state/tsks/
```

### Enhancement (EXTEND TSK structure):

```python
# Add to ConversationalTSKRecorder.record_tsk() method

def record_tsk(self, turn_data: Dict, felt_states: Dict, result: Dict):
    """
    Record TSK with FFITTSS tier markers (EXTENDS existing method).

    This ADDS tier metadata to existing TSK capture, doesn't replace it.
    """
    # 1. Existing TSK capture (KEEP)
    tsk_entry = {
        'turn_id': turn_data.get('turn_id'),
        'user_id': turn_data.get('user_id'),
        'session_id': turn_data.get('session_id'),
        'transformation_signature': self._compute_signature(felt_states),
        'felt_states': felt_states,
        # ... existing fields ...
    }

    # 2. ADD FFITTSS tier markers (NEW)
    tsk_entry['ffittss_tiers'] = {
        'T0_canonicalization': {
            'equivalent': 'Word occasions + entity extraction',
            'modules': ['word_occasion.py', 'entity_neighbor_prehension.py'],
            'word_count': len(turn_data.get('word_occasions', [])),
            'entities_extracted': len(turn_data.get('nexus_entities', []))
        },
        'T1_prehension': {
            'equivalent': 'User superject + entity memory',
            'modules': ['user_superject_learner.py', 'entity_organ_tracker.py'],
            'user_memory_depth': felt_states.get('memory_depth', 0),
            'prior_turns': felt_states.get('prior_turns', 0)
        },
        'T2_relevance': {
            'equivalent': 'NDAM urgency + SANS coherence',
            'modules': ['ndam/ndam_text_core.py', 'sans/sans_text_core.py'],
            'urgency': felt_states.get('ndam_urgency_level', 0.0),
            'semantic_coherence': felt_states.get('sans_coherence', 0.0)
        },
        'T3_organs': {
            'equivalent': '12-organ activation (65D vector)',
            'modules': ['organs/modular/*/organ_text_core.py'],
            'active_organs': felt_states.get('active_organs', 0),
            'mean_activation': felt_states.get('mean_activation', 0.0),
            'vector_dim': 65
        },
        'T4_intersections': {
            'equivalent': 'Nexus formation (14 types)',
            'modules': ['transductive_nexus_evaluator.py', 'meta_atom_activator.py'],
            'nexuses_formed': felt_states.get('nexuses_formed', 0),
            'meta_atoms': felt_states.get('meta_atoms_activated', 0)
        },
        'T5_commit': {
            'equivalent': 'V0 convergence + satisfaction gating',
            'modules': ['conversational_occasion.py', 'emission_generator.py'],
            'v0_cycles': felt_states.get('convergence_cycles', 1),
            'kairos_detected': felt_states.get('kairos_detected', False),
            'satisfaction': felt_states.get('satisfaction', 0.0),
            'v0_energy_final': felt_states.get('v0_energy', 1.0)
        },
        'T6_feedback': {
            'equivalent': 'Cycle tracking + regime classification',
            'modules': ['cycle_convergence_tracker.py', 'threshold_evolver.py'],
            'regime': turn_data.get('regime', 'STABLE'),
            'evolution_rate': turn_data.get('evolution_rate', 0.5),
            'threshold_adjusted': turn_data.get('threshold_adjusted', False)
        },
        'T7_governance': {
            'equivalent': 'SELF matrix + organic families',
            'modules': ['self_matrix_governance.py', 'organic_families.json'],
            'self_zone': felt_states.get('self_zone', 'Zone 1'),
            'family_assigned': result.get('family_assigned', 'Unknown')
        },
        'T8_memory': {
            'equivalent': 'TSK capture + session logging',
            'modules': ['conversational_tsk_recorder.py', 'turn_history_manager.py'],
            'tsk_events': len(self.current_session_tsks),
            'session_turns': felt_states.get('session_turns', 0)
        }
    }

    # 3. Existing save logic (KEEP)
    self._save_tsk(tsk_entry)
```

**Why This Works:**
- ✅ Leverages existing TSK recorder (no bypass)
- ✅ Adds tier metadata without changing TSK structure
- ✅ Maps DAE modules to FFITTSS tiers
- ✅ Provides clear tier-to-module mapping for analysis

**Effort:** 1 hour (extend 1 method)

---

## Implementation Priority & Timeline

### Phase 1: Regime Classification (2 hours)
1. Add `classify_regime()` and `get_regime_evolution_rate()` to `CycleConvergenceTracker`
2. Add `update_with_regime()` method
3. Update wrapper call site to use `update_with_regime()`
4. Test with 5 inputs to validate regime classification

**Expected:** +10% T6 compliance (80% → 90%)

### Phase 2: Threshold Evolution (3 hours)
1. Create `threshold_evolver.py` with `ThresholdEvolver` class
2. Add evolver to wrapper initialization
3. Integrate threshold evolution after V0 convergence
4. Test with 10 inputs to validate evolution

**Expected:** +15% T6 compliance (90% → 95%+)

### Phase 3: TSK Tier Markers (1 hour)
1. Extend `record_tsk()` to add `ffittss_tiers` dict
2. Test TSK output structure
3. Validate all 8 tiers captured

**Expected:** +5% T8 compliance (95% → 100%)

**Total Effort:** 6 hours
**Total Compliance Gain:** 84.4% → 93%+ (Grade: B+ → A)

---

## Validation Plan

### After Each Enhancement:

**Test Script:** `test_ffittss_enhancements.py`
```python
# Test regime classification
organism = ConversationalOrganismWrapper()
result = organism.process_text_with_phase3b_context("Test input")
assert 'regime' in result['context']
assert result['context']['regime'] in ['INITIALIZING', 'CONVERGING', ...]

# Test threshold evolution
assert hasattr(organism, 'threshold_evolver')
stats = organism.threshold_evolver.get_stats()
assert stats['total_evolutions'] > 0

# Test TSK tier markers
tsk_file = latest_tsk_file()
tsk_data = load_json(tsk_file)
assert 'ffittss_tiers' in tsk_data
assert len(tsk_data['ffittss_tiers']) == 8
```

### Full Integration Test:

Run 50-input epoch training to validate:
- Regime distribution (expect 60-80% COMMITTED, like FFITTSS)
- Threshold convergence (expect adaptive adjustment)
- TSK tier markers (expect all 8 tiers captured)

---

## Key Principles Maintained

### ✅ 1. No Bypass - Only Enhancement
- All existing modules remain functional
- New functionality **extends** existing classes
- Backward compatible (old code still works)

### ✅ 2. Leverage Existing Infrastructure
- CycleConvergenceTracker → Add regime methods
- Config thresholds → Evolve adaptively
- TSK recorder → Add tier markers
- V0 convergence → Use for threshold feedback

### ✅ 3. FFITTSS Concepts Mapped to DAE
- FFITTSS tau_delta_c → DAE emission thresholds
- FFITTSS regimes → DAE satisfaction windows
- FFITTSS spatial fields → DAE temporal sequences
- FFITTSS 35D vector → DAE 65D organ signatures

### ✅ 4. Domain-Specific Adaptation
- Spatial (x,y) → Temporal (position in sequence)
- Grid processing → Text processing
- Task completion → Conversation turn
- 6 organs → 12 organs (enhanced, not reduced)

---

## Expected Outcomes

### Compliance Improvements:

| Enhancement | T6 Before | T6 After | Gain |
|-------------|-----------|----------|------|
| Regime Classification | 80% | 90% | +10% |
| Threshold Evolution | 90% | 95%+ | +5%+ |
| TSK Tier Markers (T8) | 95% | 100% | +5% |

**Overall:** 84.4% → **93%+ compliance** (Grade: B+ → A)

### Functional Improvements:

1. **Better Convergence** - Regime-aware evolution prevents dead zones
2. **Adaptive Thresholds** - Thresholds learn from satisfaction feedback
3. **Better Telemetry** - TSK tier markers enable FFITTSS-style analysis
4. **Cross-System Insights** - Can compare DAE vs FFITTSS patterns

---

## Conclusion

This implementation plan **leverages existing DAE scaffolding** rather than bypassing it:

1. ✅ **Extends** CycleConvergenceTracker with regime classification
2. ✅ **Adds** ThresholdEvolver that uses existing Config thresholds
3. ✅ **Enhances** TSK recording with tier metadata
4. ✅ **Maintains** all existing functionality (backward compatible)

The result: **93%+ FFITTSS compliance** while **preserving DAE's unique strengths** (12 organs, conversational domain, felt-to-text processing).

---

🌀 **"From 84% to 93%+ FFITTSS compliance through enhancement, not replacement. Leverage existing scaffolding. Extend with FFITTSS concepts. Preserve DAE's conversational felt-to-text architecture."** 🌀

**Last Updated:** November 18, 2025
**Approach:** Leverage existing modules
**Timeline:** 6 hours total
**Expected Compliance:** 93%+ (Grade: A)
