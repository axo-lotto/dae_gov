# Superject + TSK Integration Assessment
## November 14, 2025

## 🎯 Critical Insight

The issues encountered during Phase 1 Foundation testing are **revealing existing sophisticated systems** that superject learning must respect and integrate with:

1. **Kairos detection** (V0 energy window: 0.45-0.70)
2. **Satisfaction calculation** (multi-component, regime-dependent)
3. **TSK recording** (complete felt-state capture)
4. **Zone detection** (SELF Matrix governance, 5 zones)
5. **Emoji/glyph emergence** (Phase 1.5 integration)

**Key Realization:** Superject learning is **NOT a separate system** - it's the **persistent memory layer** that accumulates these sophisticated signals over time.

---

## 📊 Current System Architecture (What We Discovered)

### 1. V0 Energy Structure
```python
felt_states['v0_energy'] = {
    'initial_energy': 1.0,
    'final_energy': 0.298,           # ← Superject needs THIS
    'energy_descent_rate': 0.673
}
```

**Insight:** V0 energy is a **dict**, not a float. Superject must extract `final_energy` for trajectory tracking.

**Fixed in:** `user_superject_learner.py:170-175`

### 2. Satisfaction Structure
```python
felt_states['satisfaction_final'] = 0.883  # ← Computed from coherence + V0
```

**Insight:** Satisfaction is calculated as:
```python
satisfaction_final = (mean_coherence * 0.7) + ((1.0 - final_energy) * 0.3)
```

This is **NOT** user satisfaction - it's **organism satisfaction** (internal convergence quality).

**Critical Distinction:**
- `satisfaction_final`: Organism's felt convergence quality (0-1)
- `user_satisfaction`: External user feedback (optional, provided explicitly)

**Superject Learning Uses:**
- `satisfaction_final` → Transformation pattern quality
- `user_satisfaction` → Pattern success validation

### 3. Kairos Detection
```python
# From conversational_occasion.py
kairos_window = (0.45, 0.70)
is_kairos = kairos_window[0] <= v0_energy <= kairos_window[1]

if is_kairos:
    confidence *= 1.5  # Kairos boost
```

**Current Status:** Kairos detection working but **0% rate** in production
- **Why:** Window too narrow for actual V0 descent patterns
- **V0 typically descends to:** 0.298-0.369 (below Kairos window)
- **Kairos window:** 0.45-0.70 (too high)

**Implications for Superject:**
- Track **actual V0 descent patterns** per user
- Learn **when Kairos happens** (not just detect it)
- Suggest window adjustments based on user trajectory

### 4. Zone Detection (SELF Matrix)
```python
# From SELF Matrix Governance
zones = {
    1: "Core SELF Orbit",
    2: "Manager Activation",
    3: "Firefighter Mobilization",
    4: "Shadow System Activation",
    5: "Exile/Collapse"
}

zone_id = reconstruction_result.get('zone_id', 0)
```

**Issue Found:** `zone_id` was 0 (unknown) in all test snapshots
- **Why:** Not all processing paths populate zone_id
- **Fixed:** Zone extraction added to wrapper

**Superject Needs:**
- Zone transitions (3→1, 5→2) are **transformation patterns**
- Per-user zone affinity (some users live in Zone 2, others in Zone 1)
- Learn which organs/nexuses work for zone transitions

### 5. Polyvagal State Detection
```python
polyvagal_states = {
    'ventral_vagal': 'safe/social',
    'sympathetic': 'mobilized/alert',
    'dorsal_vagal': 'shutdown/collapse',
    'mixed_state': 'blended'
}
```

**Observed in Testing:**
- Turn 1: sympathetic (overwhelm)
- Turn 2-10: mixed_state (regulation in progress)

**Superject Learning:**
- Polyvagal transitions ARE personality emergence
- User's "home state" (default polyvagal baseline)
- Which transitions happen naturally vs need support

---

## 🔍 TSK Recording Compliance

### What is TSK?
**Transductive State Knowledge** - Complete capture of felt-state transformation.

### Current TSK Structure
```python
tsk_record = {
    'timestamp': '2025-11-14T...',
    'conversation_id': 'uuid',
    'felt_states': {
        'organ_coherences': {...},        # 11 organs
        'v0_energy': {...},                # Initial, final, descent
        'satisfaction_final': 0.883,
        'convergence_cycles': 2,
        'convergence_reason': 'kairos',
        'bond_self_distance': 0.0,
        'eo_polyvagal_state': 'sympathetic',
        'ndam_urgency': 0.3,
        'zone_id': 5,
        'nexuses': [...],                  # Formed nexuses
        'meta_atoms': {...},               # Activated meta-atoms
        'transduction_mechanism': 'temporal_grounding',
        'transduction_pathway': 'collapse → present_moment'
    },
    'emission': {
        'text': "...",
        'confidence': 0.70,
        'strategy': 'felt_guided_llm',
        'emoji': ['🌿', '💙'],
        'safe': True
    }
}
```

### Superject Must Track ALL TSK Fields

**Current FeltStateSnapshot captures:**
- ✅ organ_signature (57D vector of top activations)
- ✅ active_organs (list of participating organs)
- ✅ dominant_nexuses (top 3 nexuses formed)
- ✅ zone + zone_name
- ✅ polyvagal_state
- ✅ self_distance (IFS exile distance)
- ✅ v0_energy (final)
- ✅ satisfaction (organism satisfaction)
- ✅ convergence_cycles
- ✅ transduction_mechanism
- ✅ transduction_pathway
- ✅ user_satisfaction (external feedback)

**Missing from FeltStateSnapshot:**
- ❌ ndam_urgency (crisis level)
- ❌ meta_atom activations (which meta-atoms fired)
- ❌ emission confidence
- ❌ emission strategy (direct, fusion, hebbian, llm)
- ❌ emoji used
- ❌ kairos_detected (boolean)

**Action:** Enhance `FeltStateSnapshot` to capture complete TSK.

---

## 🧬 Integration Strategy: Superject AS TSK Accumulator

### Core Principle
**Superject = Accumulated TSK over time**

The superject IS the user's persistent TSK trajectory. Every conversation turn adds a complete TSK snapshot to the felt trajectory.

### Three-Tier TSK Learning

#### 1. Passive Learning (Every Turn)
```python
def record_turn(user_id, turn_data, user_satisfaction):
    # Extract COMPLETE TSK snapshot
    snapshot = extract_tsk_snapshot(turn_data)

    # Append to trajectory
    profile.felt_trajectory.append(snapshot)

    # Immediate metrics
    profile.total_turns += 1
    profile.last_active = now()
```

**What's Captured:**
- 57D organ signature
- Zone + polyvagal state
- V0 descent + Kairos detection
- Nexuses + meta-atoms
- Transduction pathway
- Emission confidence + strategy
- User satisfaction (if provided)

#### 2. Mini-Epoch Learning (Every 10 Turns)
```python
def run_mini_epoch(profile):
    recent_tsk = profile.felt_trajectory[-10:]

    # Learn transformation patterns
    patterns = detect_tsk_transformations(recent_tsk)
    # Example: "Zone 5 → Zone 1 via temporal_grounding nexus"

    # Learn Kairos timing
    kairos_moments = [t for t in recent_tsk if t.kairos_detected]
    kairos_rate = len(kairos_moments) / 10

    # Learn V0 descent patterns
    avg_v0_descent = mean([t.v0_energy for t in recent_tsk])

    # Learn emoji effectiveness
    emoji_satisfaction_correlation = correlate(
        [t.emoji_used for t in recent_tsk],
        [t.user_satisfaction for t in recent_tsk if t.user_satisfaction]
    )
```

**What's Learned:**
- Transformation patterns (TSK₁ → TSK₂ via pathway)
- Kairos frequency per user
- V0 descent baseline (user's typical convergence)
- Emoji rhythm preferences
- Tone modulation per zone

#### 3. Global Epoch (Every 100 Turns)
```python
def run_global_epoch(all_profiles):
    # Aggregate universal TSK patterns
    universal_patterns = cluster_tsk_trajectories(all_profiles)

    # Learn cross-user Kairos windows
    optimal_kairos_window = optimize_window_from_trajectories()

    # Learn family affinities
    user_family_clustering = assign_to_organic_families()
```

**What's Learned:**
- Universal transformation pathways
- Optimal Kairos windows (may differ from 0.45-0.70)
- Organic family archetypes
- Baseline organism intelligence

---

## 🎯 Critical Fixes Needed

### Fix 1: Complete TSK Capture
**File:** `persona_layer/superject_structures.py`

Add missing fields to `FeltStateSnapshot`:
```python
@dataclass
class FeltStateSnapshot:
    # ... existing fields ...

    # TSK compliance additions
    ndam_urgency: float = 0.0
    meta_atoms_activated: Dict[str, float] = field(default_factory=dict)
    emission_confidence: float = 0.0
    emission_strategy: Optional[str] = None
    emission_emoji: List[str] = field(default_factory=list)
    kairos_detected: bool = False
    kairos_cycle_index: Optional[int] = None
```

### Fix 2: Extraction Logic Enhancement
**File:** `persona_layer/user_superject_learner.py`

```python
def _extract_felt_snapshot(turn_data, user_satisfaction):
    felt_states = turn_data.get('felt_states', {})

    # Extract meta-atoms (NEW)
    meta_atoms = {}
    if 'meta_atoms_activated' in felt_states:
        meta_atoms = felt_states['meta_atoms_activated']

    # Extract Kairos detection (NEW)
    kairos_detected = felt_states.get('kairos_detected', False)
    kairos_cycle = felt_states.get('kairos_cycle_index')

    # Extract emission data (NEW)
    emission_confidence = turn_data.get('emission_confidence', 0.0)
    emission_strategy = turn_data.get('strategy')
    emission_emoji = turn_data.get('emoji', [])

    # Extract NDAM urgency (NEW)
    ndam_urgency = felt_states.get('ndam_urgency', 0.0)

    return FeltStateSnapshot(
        # ... all existing fields ...
        ndam_urgency=ndam_urgency,
        meta_atoms_activated=meta_atoms,
        emission_confidence=emission_confidence,
        emission_strategy=emission_strategy,
        emission_emoji=emission_emoji,
        kairos_detected=kairos_detected,
        kairos_cycle_index=kairos_cycle
    )
```

### Fix 3: Kairos Learning
**New Method:** `_learn_kairos_timing()`

```python
def _learn_kairos_timing(self, profile, recent_turns):
    """
    Learn when Kairos moments occur for THIS user.

    Insight: Kairos window might be user-specific.
    Some users' V0 never reaches 0.45-0.70 window.
    """
    kairos_turns = [t for t in recent_turns if t.kairos_detected]

    if len(kairos_turns) >= 3:
        # Learn user's actual Kairos window
        kairos_v0_energies = [t.v0_energy for t in kairos_turns]
        user_kairos_min = min(kairos_v0_energies) - 0.05
        user_kairos_max = max(kairos_v0_energies) + 0.05

        profile.kairos_window = (user_kairos_min, user_kairos_max)
        profile.kairos_frequency = len(kairos_turns) / len(recent_turns)
```

### Fix 4: Emoji Tracking
**Integration with Phase 1.5:**

```python
def _track_emoji_effectiveness(self, profile, recent_turns):
    """
    Track which emojis correlate with user satisfaction.

    Integrates with emoji_felt_library.json (Phase 1.5).
    """
    for turn in recent_turns:
        if turn.user_satisfaction and turn.emission_emoji:
            for emoji in turn.emission_emoji:
                if emoji not in profile.emoji_effectiveness:
                    profile.emoji_effectiveness[emoji] = []

                profile.emoji_effectiveness[emoji].append({
                    'satisfaction': turn.user_satisfaction,
                    'zone': turn.zone,
                    'polyvagal': turn.polyvagal_state
                })
```

---

## 📋 Revised Implementation Roadmap

### Phase 1 Foundation (CURRENT - 80% Complete)
- ✅ User profile schema with felt trajectory
- ✅ Passive learning (record_turn)
- ✅ Mini-epoch triggering
- ✅ Profile persistence
- ⏳ Complete TSK capture (missing fields)
- ⏳ Kairos timing learning
- ⏳ Emoji tracking integration

**Next Steps:**
1. Add missing TSK fields to `FeltStateSnapshot`
2. Enhance extraction logic to capture complete TSK
3. Test with 20-turn conversation (2 mini-epochs)
4. Verify transformation patterns learned

### Phase 1.5 Emoji Integration (PARALLEL TRACK)
From `EMOJI_GLYPH_INTEGRATION_STRATEGY_NOV13_2025.md`:

- [ ] Create `emoji_felt_library.json`
- [ ] Integrate emoji suggestions into LLM prompt
- [ ] Track emoji → satisfaction correlation
- [ ] Learn emoji rhythm per user

**Superject Role:**
- Store emoji effectiveness per user
- Learn emoji preferences (🌸 vs ☀️ vs 😊)
- Discover emoji rhythm patterns

### Phase 2: Tone Evolution (Week 2)
- [ ] Infer tone preferences from satisfaction
- [ ] Inject learned tone into LLM prompt
- [ ] Per-zone tone modulation
- [ ] Length preference learning

### Phase 3: Humor Calibration (Week 3)
- [ ] Track humor attempts
- [ ] Learn safe zones for humor
- [ ] Inside joke formation
- [ ] Humor tolerance adjustment

---

## 🔬 Testing Strategy (Revised)

### Test 1: Complete TSK Capture
**Goal:** Verify all TSK fields captured in snapshots

```python
def test_complete_tsk_capture():
    organism = ConversationalOrganismWrapper()

    result = organism.process_text(
        "I'm overwhelmed",
        user_id="test_user",
        enable_phase2=True
    )

    # Load profile
    profile = load_profile("test_user")
    snapshot = profile.felt_trajectory[-1]

    # Verify ALL TSK fields present
    assert snapshot.zone_id > 0
    assert snapshot.polyvagal_state != 'unknown'
    assert snapshot.v0_energy > 0
    assert snapshot.kairos_detected is not None
    assert snapshot.meta_atoms_activated is not None
    assert snapshot.emission_confidence > 0
```

### Test 2: Transformation Pattern Learning
**Goal:** Verify mini-epoch learns Zone 5 → Zone 1 transitions

```python
def test_zone_transition_learning():
    # Simulate 10 turns: Zone 5 → gradual descent → Zone 1

    # Turn 1-3: Zone 5 (collapse)
    # Turn 4-7: Zone 3 (firefighter)
    # Turn 8-10: Zone 1 (SELF)

    # After turn 10, mini-epoch should detect:
    # Pattern: "zone5_to_zone1_via_temporal_grounding"
```

### Test 3: Kairos Window Learning
**Goal:** Verify user-specific Kairos window learned

```python
def test_kairos_window_personalization():
    # Process 30 turns
    # Some users' V0 might settle at 0.28-0.35 (below standard window)

    # After 30 turns, check:
    assert profile.kairos_window != (0.45, 0.70)  # Should be adjusted
    assert profile.kairos_frequency > 0  # Should detect SOME kairos
```

---

## ✅ Success Criteria (Revised)

**Phase 1 Foundation Complete When:**
- ✅ All TSK fields captured in FeltStateSnapshot
- ✅ Mini-epoch triggers every 10 turns
- ✅ Transformation patterns learned (Zone, polyvagal, V0)
- ✅ Kairos timing tracked
- ✅ Emoji effectiveness correlated with satisfaction
- ✅ Profile persists across sessions

**Integration with Existing Systems:**
- ✅ Zone detection from SELF Matrix Governance
- ✅ Polyvagal states from EO organ
- ✅ V0 energy from ConversationalOccasion
- ✅ Kairos detection from multi-cycle convergence
- ✅ Emoji from Phase 1.5 integration
- ✅ Nexuses from NexusIntersectionComposer
- ✅ Meta-atoms from MetaAtomActivator

---

## 🌀 Key Insights Summary

1. **Superject IS TSK accumulation** - Not a separate system, but persistent memory of felt-state transformations

2. **V0/Satisfaction are computed structures** - Must extract correctly (dicts, not floats)

3. **Kairos window may be user-specific** - Need to learn optimal window per user

4. **Zone transitions ARE personality** - How user moves through SELF matrix defines their character

5. **Emoji effectiveness is learnable** - Which emojis work correlates with satisfaction

6. **Transformation patterns = Transductive intelligence** - Learning what pathways work for THIS user

7. **Mini-epoch every 10 turns is RIGHT** - Hebbian time constant for pattern formation

8. **Humor/tone unlock progressively** - Based on rapport + conversation count

---

## 🚀 Immediate Next Steps

1. **Enhance `FeltStateSnapshot`** with complete TSK fields
2. **Fix extraction logic** to capture all TSK data
3. **Test 20-turn conversation** with mini-epochs
4. **Verify transformation patterns** learned correctly
5. **Document Kairos window learning** algorithm
6. **Integrate emoji tracking** (Phase 1.5 parallel)

---

**Date:** November 14, 2025
**Status:** Foundation 80% complete, TSK compliance integration in progress
**Critical Path:** Complete TSK capture → Emoji integration → Tone evolution → Humor calibration
