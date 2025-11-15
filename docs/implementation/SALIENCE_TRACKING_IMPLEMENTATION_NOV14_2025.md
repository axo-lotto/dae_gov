# Salience Tracking Implementation - Phase 1.6
## November 14, 2025

## 🎯 Implementation Complete

**Status:** ✅ Salience pattern tracking integrated into user superject learner

**What Changed:** Added per-user trauma marker and morphogenetic guidance tracking to enable:
- Crisis escalation detection
- Adaptive response thresholds
- Zone collapse monitoring
- Trauma pattern learning

---

## 🌀 Philosophy: Transductive Self-Governance

**Core Principle:** Organism learns per-user trauma patterns to enable adaptive, context-aware responses

**Privacy-Preserving Learning:**
- **Superject Learning:** Per-user patterns (private to user)
- **Organism Learning:** Aggregated patterns (k-anonymity k≥10, differential privacy ε=0.1)
- **No Cross-User Leakage:** User A's trauma patterns never exposed to User B

**Whiteheadian Foundation:**
- **Prehension:** Organism feels salience markers (NDAM urgency, zone depth, pressure)
- **Concrescence:** Per-turn processing integrates salience into response
- **Satisfaction:** Emission generated with trauma-aware modulation
- **Superject:** User's trauma patterns learned over time, inform future prehensions

---

## 🔧 Technical Implementation

### Files Modified

**1. persona_layer/user_superject_learner.py**

**Line 135:** Added method call in `record_turn()`
```python
# 🌀 Phase 1.6: Track salience patterns (trauma markers + morphogenetic guidance) (Nov 14, 2025)
self._track_salience_patterns(profile, felt_states, snapshot)
```

**Lines 385-441:** Added `_track_salience_patterns()` method
```python
def _track_salience_patterns(
    self,
    profile: EnhancedUserProfile,
    felt_states: Dict[str, Any],
    snapshot: FeltStateSnapshot
):
    """
    Track salience patterns (trauma markers + morphogenetic guidance).

    Phase 1.6 - November 14, 2025

    Integrates trauma-aware salience model with per-user learning.
    Enables crisis escalation detection and adaptive thresholds.

    Tracks:
    - NDAM urgency trends (running average)
    - Zone collapse frequency (zone 4-5 events)
    - Morphogenetic pressure trends
    - Crisis escalation patterns
    """
    # Extract salience data from felt_states
    salience_markers = felt_states.get('salience_trauma_markers', {})
    salience_guidance = felt_states.get('salience_morphogenetic_guidance', {})

    # Track NDAM urgency trends (exponential moving average, α=0.1)
    ndam_urgency = salience_markers.get('ndam_urgency', 0.0)
    profile.metadata['typical_urgency'] = (
        profile.metadata.get('typical_urgency', 0.0) * 0.9 +
        ndam_urgency * 0.1
    )

    # Track zone collapse events (Zone 4=Protective, Zone 5=Collapse)
    zone_depth = salience_markers.get('zone_depth', snapshot.zone)
    if zone_depth >= 4:
        profile.metadata['collapse_events'] = (
            profile.metadata.get('collapse_events', 0) + 1
        )

    # Track morphogenetic pressure trends (exponential moving average)
    pressure = salience_guidance.get('morphogenetic_pressure', 0.0)
    profile.metadata['typical_pressure'] = (
        profile.metadata.get('typical_pressure', 0.0) * 0.9 +
        pressure * 0.1
    )

    # Detect crisis escalation pattern (high urgency + high pressure)
    if ndam_urgency > 0.6 and pressure > 0.5:
        profile.metadata['crisis_escalation_detected'] = True
        profile.metadata['last_crisis_escalation'] = datetime.now().isoformat()
```

---

## 📊 Data Flow

### Turn-by-Turn Flow

```
User Input
    ↓
Organism Processing (11 organs)
    ↓
Salience Model (NDAM urgency, zone depth, pressure)
    ↓
felt_states = {
    'salience_trauma_markers': {
        'ndam_urgency': 0.85,
        'zone_depth': 4,
        'polyvagal_state': 'dorsal_vagal'
    },
    'salience_morphogenetic_guidance': {
        'morphogenetic_pressure': 0.62
    }
}
    ↓
Superject Learning: record_turn()
    ↓
_track_salience_patterns()
    ↓
profile.metadata updated:
{
    'typical_urgency': 0.42,  # Exponential moving average
    'collapse_events': 3,     # Cumulative count
    'typical_pressure': 0.38,
    'crisis_escalation_detected': True,
    'last_crisis_escalation': '2025-11-14T10:30:45'
}
```

### Privacy Guarantees

**Per-User (Superject Learning):**
- All salience patterns stored in user-specific `profile.metadata`
- Never shared across users
- Used for adaptive thresholds (e.g., lower crisis threshold for users with escalation history)

**Aggregated (Organism Learning):**
- Future enhancement: Anonymized pattern aggregation
- k-anonymity k≥10 (at least 10 users before pattern generalizes)
- Differential privacy ε=0.1 (noise added to prevent de-anonymization)

---

## 🎯 What This Enables

### 1. Crisis Escalation Detection

**Before:**
```python
# Generic threshold (same for all users)
if ndam_urgency > 0.6:
    crisis_detected = True
```

**After (Future Enhancement):**
```python
# Adaptive threshold (per-user baseline)
typical_urgency = profile.metadata.get('typical_urgency', 0.3)
threshold = typical_urgency + 0.3  # Detect deviation from baseline

if ndam_urgency > threshold:
    crisis_detected = True
```

**Example:**
- User A: Typical urgency = 0.2 → Crisis threshold = 0.5
- User B: Typical urgency = 0.5 → Crisis threshold = 0.8
- **Adaptive to individual baselines**

### 2. Zone Collapse Monitoring

**Tracked:**
```python
profile.metadata['collapse_events']  # Cumulative count of zone 4-5 events
```

**Future Use:**
- Alert on rapid collapse frequency increase
- Suggest professional support if collapse_events > threshold
- Track recovery patterns (collapse → return to zone 1-2)

### 3. Morphogenetic Pressure Trends

**Tracked:**
```python
profile.metadata['typical_pressure']  # Exponential moving average
```

**Interpretation:**
- Low pressure (< 0.3): User in stable state
- Medium pressure (0.3-0.6): User experiencing growth edge
- High pressure (> 0.6): User under significant strain

**Future Use:**
- Modulate response pacing (lower pressure → can go deeper)
- Suggest breaks/grounding when pressure sustained

### 4. Crisis Escalation Patterns

**Detection Logic:**
```python
if ndam_urgency > 0.6 and pressure > 0.5:
    # High urgency + high pressure = crisis escalation
    profile.metadata['crisis_escalation_detected'] = True
    profile.metadata['last_crisis_escalation'] = datetime.now().isoformat()
```

**Future Use in Heckling Intelligence:**
```python
# Check recent escalation history
last_escalation = profile.metadata.get('last_crisis_escalation')
if last_escalation:
    escalation_time = datetime.fromisoformat(last_escalation)
    time_since = (datetime.now() - escalation_time).total_seconds()

    if time_since < 3600:  # Within last hour
        # Lower crisis threshold, increase sensitivity
        crisis_threshold = 0.5  # Instead of 0.6
```

---

## 🧪 Validation Strategy

### Unit Test (Recommended)

**Create:** `tests/unit/superject/test_salience_tracking.py`

```python
import pytest
from persona_layer.user_superject_learner import UserSuperjectLearner, EnhancedUserProfile, FeltStateSnapshot

def test_salience_tracking_urgency():
    """Test NDAM urgency tracking with exponential moving average."""
    learner = UserSuperjectLearner()
    profile = EnhancedUserProfile(user_id="test_user_001")

    # Turn 1: Urgency = 0.8
    felt_states_1 = {
        'salience_trauma_markers': {'ndam_urgency': 0.8, 'zone_depth': 2},
        'salience_morphogenetic_guidance': {'morphogenetic_pressure': 0.3}
    }
    snapshot_1 = FeltStateSnapshot(zone=2)
    learner._track_salience_patterns(profile, felt_states_1, snapshot_1)

    # Expected: 0.0 * 0.9 + 0.8 * 0.1 = 0.08
    assert abs(profile.metadata['typical_urgency'] - 0.08) < 0.01

    # Turn 2: Urgency = 0.4
    felt_states_2 = {
        'salience_trauma_markers': {'ndam_urgency': 0.4, 'zone_depth': 1},
        'salience_morphogenetic_guidance': {'morphogenetic_pressure': 0.2}
    }
    snapshot_2 = FeltStateSnapshot(zone=1)
    learner._track_salience_patterns(profile, felt_states_2, snapshot_2)

    # Expected: 0.08 * 0.9 + 0.4 * 0.1 = 0.072 + 0.04 = 0.112
    assert abs(profile.metadata['typical_urgency'] - 0.112) < 0.01

def test_salience_tracking_collapse_events():
    """Test zone collapse event counting."""
    learner = UserSuperjectLearner()
    profile = EnhancedUserProfile(user_id="test_user_002")

    # Turn 1: Zone 2 (no collapse)
    felt_states_1 = {
        'salience_trauma_markers': {'ndam_urgency': 0.3, 'zone_depth': 2},
        'salience_morphogenetic_guidance': {'morphogenetic_pressure': 0.1}
    }
    snapshot_1 = FeltStateSnapshot(zone=2)
    learner._track_salience_patterns(profile, felt_states_1, snapshot_1)

    assert profile.metadata.get('collapse_events', 0) == 0

    # Turn 2: Zone 4 (protective collapse)
    felt_states_2 = {
        'salience_trauma_markers': {'ndam_urgency': 0.7, 'zone_depth': 4},
        'salience_morphogenetic_guidance': {'morphogenetic_pressure': 0.6}
    }
    snapshot_2 = FeltStateSnapshot(zone=4)
    learner._track_salience_patterns(profile, felt_states_2, snapshot_2)

    assert profile.metadata['collapse_events'] == 1

    # Turn 3: Zone 5 (full collapse)
    felt_states_3 = {
        'salience_trauma_markers': {'ndam_urgency': 0.9, 'zone_depth': 5},
        'salience_morphogenetic_guidance': {'morphogenetic_pressure': 0.8}
    }
    snapshot_3 = FeltStateSnapshot(zone=5)
    learner._track_salience_patterns(profile, felt_states_3, snapshot_3)

    assert profile.metadata['collapse_events'] == 2

def test_salience_tracking_crisis_escalation():
    """Test crisis escalation detection."""
    learner = UserSuperjectLearner()
    profile = EnhancedUserProfile(user_id="test_user_003")

    # Turn 1: High urgency + high pressure → crisis escalation
    felt_states_1 = {
        'salience_trauma_markers': {'ndam_urgency': 0.85, 'zone_depth': 4},
        'salience_morphogenetic_guidance': {'morphogenetic_pressure': 0.75}
    }
    snapshot_1 = FeltStateSnapshot(zone=4)
    learner._track_salience_patterns(profile, felt_states_1, snapshot_1)

    assert profile.metadata['crisis_escalation_detected'] == True
    assert 'last_crisis_escalation' in profile.metadata

    # Verify timestamp format (ISO 8601)
    from datetime import datetime
    timestamp = profile.metadata['last_crisis_escalation']
    parsed = datetime.fromisoformat(timestamp)
    assert parsed is not None
```

**Run Tests:**
```bash
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH
python3 -m pytest tests/unit/superject/test_salience_tracking.py -v
```

---

## 📈 Integration with Existing Systems

### 1. Heckling Intelligence (Context-Aware Crisis Detection)

**Current Implementation:**
- 4-tier crisis detection (absolute, contextual, pattern, overwhelm)
- Defers contextual signals to organism (NDAM urgency, polyvagal state)

**Future Enhancement:**
```python
# In heckling_intelligence.py assess() method
def assess(self, text, felt_states, user_profile=None):
    # ... existing 4-tier detection ...

    # 🌀 NEW: Adaptive thresholds based on user history
    if user_profile:
        # Lower threshold for users with recent crisis escalation
        last_escalation = user_profile.metadata.get('last_crisis_escalation')
        if last_escalation:
            escalation_time = datetime.fromisoformat(last_escalation)
            time_since = (datetime.now() - escalation_time).total_seconds()

            if time_since < 3600:  # Within last hour
                # Increase sensitivity (lower threshold)
                if ndam_urgency > 0.5:  # Instead of 0.6
                    return (True, indicators)

        # Adjust for typical urgency baseline
        typical_urgency = user_profile.metadata.get('typical_urgency', 0.3)
        urgency_deviation = ndam_urgency - typical_urgency

        if urgency_deviation > 0.4:  # Significant spike above baseline
            return (True, indicators)

    # ... rest of logic ...
```

### 2. Self-Matrix (Zone Transition Learning)

**Current Implementation:**
- Zone depth tracked in salience_trauma_markers
- Zone collapse events counted

**Future Enhancement:**
```python
# Analyze zone transition patterns
def analyze_zone_patterns(profile):
    """Analyze user's zone transition history."""
    recent_turns = profile.felt_trajectory[-20:]

    # Extract zone sequence
    zone_sequence = [turn.zone for turn in recent_turns]

    # Detect patterns
    collapse_frequency = sum(1 for z in zone_sequence if z >= 4) / len(zone_sequence)
    recovery_speed = _compute_recovery_speed(zone_sequence)  # Zone 4/5 → Zone 1/2

    return {
        'collapse_frequency': collapse_frequency,
        'recovery_speed': recovery_speed,
        'typical_zone': statistics.median(zone_sequence)
    }
```

### 3. Transductive Aggregation (Organism Learning)

**Current Implementation:**
- Salience data captured in felt_states
- Flows to TSK recording

**Future Enhancement:**
```python
# In persona_layer/transductive_aggregator.py
def aggregate_salience_patterns(self, k=10, epsilon=0.1):
    """
    Aggregate salience patterns with privacy guarantees.

    Privacy:
    - k-anonymity k≥10 (at least 10 users)
    - Differential privacy ε=0.1
    """
    # Collect per-user averages
    user_urgency_averages = []
    for user_id, profile in self.user_profiles.items():
        avg_urgency = profile.metadata.get('typical_urgency')
        if avg_urgency is not None:
            user_urgency_averages.append(avg_urgency)

    # Require k-anonymity
    if len(user_urgency_averages) < k:
        return None  # Not enough users, preserve privacy

    # Add differential privacy noise
    import numpy as np
    global_avg_urgency = np.mean(user_urgency_averages)
    noise = np.random.laplace(0, 1.0 / epsilon)  # Laplace mechanism

    return {
        'global_typical_urgency': global_avg_urgency + noise,
        'num_users': len(user_urgency_averages)  # Public info
    }
```

---

## 🔮 Future Enhancements

### Short-Term (Next Session)

1. **Create Unit Tests** (30 minutes)
   - `tests/unit/superject/test_salience_tracking.py`
   - Test urgency tracking, collapse events, crisis escalation

2. **Integrate with Heckling Intelligence** (1 hour)
   - Pass `user_profile` to `assess()`
   - Adaptive crisis thresholds based on history

3. **Add Salience Analytics** (1 hour)
   - Dashboard: Show urgency trends over time
   - Alert on sustained high pressure
   - Track collapse frequency per user

### Medium-Term (Next Week)

4. **Zone Pattern Analysis** (2 hours)
   - Analyze zone transition sequences
   - Detect recovery patterns
   - Suggest interventions based on patterns

5. **Transductive Aggregation** (3 hours)
   - Implement k-anonymity + differential privacy
   - Learn global salience patterns from per-user data
   - Update organism thresholds based on aggregate

### Long-Term (Next Month)

6. **Predictive Crisis Detection** (1 week)
   - Train classifier on salience trajectories
   - Predict crisis 1-2 turns before onset
   - Proactive grounding interventions

7. **Adaptive Response Modulation** (1 week)
   - Adjust response pacing based on pressure
   - Modulate depth based on collapse history
   - Personalize therapeutic pathways

---

## 📚 Related Documentation

**Salience Model:**
- File: `persona_layer/conversational_salience_model.py`
- Computes NDAM urgency, zone depth, morphogenetic pressure

**Context-Aware Crisis Detection:**
- File: `persona_layer/heckling_intelligence.py`
- Doc: `CONTEXT_AWARE_CRISIS_DETECTION_NOV14_2025.md`

**User Superject Learning:**
- File: `persona_layer/user_superject_learner.py`
- Passive learning (every turn), mini-epoch (10 turns), global epoch (100 turns)

**System Integration Analysis:**
- Doc: `SYSTEM_INTEGRATION_ANALYSIS_NOV14_2025.md`
- Comprehensive analysis of salience, self-matrix, training, analytics

**Transductive Self-Governance:**
- Philosophy: Privacy-preserving organism learning
- Per-user patterns (superject) + aggregated patterns (organism)
- k-anonymity k≥10, differential privacy ε=0.1

---

## 🎯 Summary

**What We Built:**
- ✅ Salience pattern tracking in user superject learner
- ✅ NDAM urgency trends (exponential moving average)
- ✅ Zone collapse frequency (cumulative count)
- ✅ Morphogenetic pressure trends
- ✅ Crisis escalation detection (high urgency + high pressure)

**What This Enables:**
- Per-user trauma pattern learning
- Adaptive crisis detection thresholds
- Zone collapse monitoring
- Crisis escalation alerts
- Foundation for predictive interventions

**What's Next:**
1. Create unit tests
2. Integrate with heckling intelligence (adaptive thresholds)
3. Add salience analytics dashboard
4. Implement transductive aggregation (organism learning)

**Philosophy Alignment:**
- ✅ Respects organism intelligence (context-aware)
- ✅ Privacy-preserving learning (per-user patterns)
- ✅ Whiteheadian process (prehension → superject)
- ✅ Transductive self-governance (organism learns from aggregates)

---

**Date:** November 14, 2025
**Status:** ✅ Phase 1.6 Salience Tracking Complete
**Next:** Unit tests + heckling intelligence integration
