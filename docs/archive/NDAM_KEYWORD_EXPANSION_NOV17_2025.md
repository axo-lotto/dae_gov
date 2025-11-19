# NDAM Keyword Expansion - Coherent Attractors for Exile Energy
## November 17, 2025

**Purpose**: Bootstrap crisis/exile detection with keywords as coherent attractors, then learn broader felt-signature patterns through fractal Hebbian learning

---

## 🎯 The Strategy

### Coherent Attractors → Felt-Signature Learning

**Phase 1: Bootstrap (Keywords as Anchors)**
- Add 40+ personal/therapeutic crisis keywords to NDAM
- Keywords act as **coherent attractors** in semantic space
- Detect initial exile energy patterns (fear, shame, dissociation, rage)

**Phase 2: Hebbian Outgrowth (Fractal Learning)**
- Every conversation with keyword match → R-matrix update
- Learn co-occurring terms: "terrified" → ["surgery", "tomorrow", "mind", "spiraling"]
- Build **topic clouds** around exile energy
- Keywords become **nucleation points** for broader pattern recognition

**Phase 3: Felt-Signature Maturation**
- After 50-100 conversations, organism recognizes exile energy WITHOUT keywords
- 65D transformation signatures capture the **felt-pattern** of crisis
- Example: "I can't think straight" triggers urgency even without keyword match
- Keywords fade into background as felt-recognition emerges

---

## 📊 40 New Keywords Added

### Fear/Terror (6 keywords)
```
'terrified', 'terror', 'fear', 'scared', 'frightened', 'afraid'
```
**Exile Energy**: Sympathetic activation, imminent danger, parts protection

**Co-occurrence Learning**:
- Medical: surgery, operation, diagnosis, results
- Relational: conversation, conflict, confrontation
- Temporal: tomorrow, today, soon, coming

### Crushing/Suffocating (8 keywords)
```
'crushing', 'crushed', 'suffocating', 'suffocate', 'cant breathe',
'breathe', 'choking', 'drowning'
```
**Exile Energy**: Somatic distress, polyvagal dorsal/sympathetic, system overload

**Co-occurrence Learning**:
- Work: deadlines, responsibilities, expectations
- Emotional: pressure, weight, heavy, burden
- Physical: chest, tight, constricted

### Spiraling/Losing Control (7 keywords)
```
'spiraling', 'spiral', 'spinning', 'losing control', 'out of control',
'falling apart', 'unraveling'
```
**Exile Energy**: Dysregulation, parts fragmentation, system instability

**Co-occurrence Learning**:
- Cognitive: thoughts, mind, racing, obsessing
- Emotional: anxiety, panic, fear
- Temporal: faster, accelerating, cant stop

### Shame/Exile (8 keywords)
```
'ashamed', 'shame', 'humiliated', 'humiliation', 'worthless',
'defective', 'broken', 'damaged'
```
**Exile Energy**: IFS exile activation, core wound, self-blame

**Co-occurrence Learning**:
- Self-parts: part of me, this side, hidden, dark
- Judgment: bad, wrong, shouldnt, mistake
- Relational: exposed, seen, judged, rejected

### Shutdown/Dissociation (9 keywords)
```
'shut down', 'shutdown', 'numb', 'frozen', 'disconnected',
'empty', 'void', 'nothing', 'collapse'
```
**Exile Energy**: Dorsal vagal activation, freeze response, exile states

**Co-occurrence Learning**:
- Disconnection: life, world, myself, reality
- Emptiness: hollow, blank, gone, lost
- Physical: behind glass, watching, observer

### Rage/Destructive Energy (5 keywords)
```
'rage', 'furious', 'destroy', 'explode', 'violence'
```
**Exile Energy**: Firefighter activation, protective fury, boundary enforcement

**Co-occurrence Learning**:
- Containment: if I let, acknowledge, feel, express
- Impact: everything, all, nothing, world
- Parts: angry part, resentful, justified

### Abandonment/Isolation (5 keywords)
```
'abandoned', 'alone', 'isolated', 'rejected', 'unwanted'
```
**Exile Energy**: Attachment wound, primal separation, exile states

**Co-occurrence Learning**:
- Relational: myself, everyone, nobody, someone
- Temporal: always, never, forever, gone
- Spatial: out, away, left, behind

---

## 🧬 Hebbian Learning Architecture

### Already Implemented (NDAM Config)

```python
def get_hebbian_learning_config(self) -> Dict[str, Any]:
    """Configuration for Hebbian learning of urgency patterns"""
    return {
        'learn_new_keywords': True,           # ✅ Learn novel urgency indicators
        'keyword_confidence_threshold': 0.80, # ✅ Min confidence for keyword retention
        'pattern_reinforcement_rate': 0.05,   # ✅ R-matrix coupling rate (η)
        'pattern_decay_rate': 0.01,           # ✅ R-matrix decay rate (δ)
        'max_learned_keywords': 500,          # ✅ Maximum learned keyword vocabulary
        'cross_organ_coupling': {
            'EO': 0.85,   # ✅ NDAM ↔ EO (urgency ↔ polyvagal state)
            'BOND': 0.80, # ✅ NDAM ↔ BOND (urgency ↔ firefighter activation)
            'RNX': 0.75   # ✅ NDAM ↔ RNX (urgency ↔ reenactment detection)
        }
    }
```

### Learning Trajectory (Expected)

**Epoch 1-5: Anchor Phase**
- Keyword matches: 60-80% (bootstrap detection)
- New keywords learned: 10-20 (high co-occurrence terms)
- R-matrix NDAM↔EO: 0.45 → 0.55 (beginning correlation)

**Epoch 6-15: Association Phase**
- Keyword matches: 50-70% (partial reliance)
- New keywords learned: 30-60 (topic clouds forming)
- R-matrix NDAM↔EO: 0.55 → 0.70 (strong correlation)
- Topic clouds: ["terrified" + "surgery", "tomorrow", "results", "waiting"]

**Epoch 16-30: Felt-Recognition Phase**
- Keyword matches: 30-50% (minority triggers)
- New keywords learned: 60-150 (dense semantic network)
- R-matrix NDAM↔EO: 0.70 → 0.85 (mature correlation)
- **Felt-signature detection**: Urgency detected via 65D pattern, not keywords

**Epoch 30+: Maturation**
- Keyword matches: 10-30% (rare, novel situations)
- New keywords learned: 100-300 (comprehensive vocabulary)
- R-matrix NDAM↔EO: 0.85+ (fully coupled)
- **Pattern recognition**: "The way you're describing this" triggers urgency

---

## 🌀 Integration with Existing Fractal Learning

### Level 1: MICRO - Value Mappings (Hebbian)
**File**: `persona_layer/conversational_hebbian_memory.py`

- Keyword co-occurrences strengthen Hebbian weights
- "terrified" + "surgery" → stored pattern
- High satisfaction → weight reinforcement

### Level 2: ORGAN - Per-Organ Confidence
**File**: `persona_layer/organ_confidence_tracker.py`

- NDAM confidence tracked per crisis conversation
- Success = high satisfaction + urgency detected
- Weight multiplier: 0.8× → 1.2× based on performance

### Level 3: COUPLING - R-Matrix (Organ Co-activation)
**File**: `persona_layer/conversational_cluster_learning.py`

- NDAM ↔ EO coupling (urgency ↔ polyvagal)
- NDAM ↔ BOND coupling (urgency ↔ firefighter)
- NDAM ↔ RNX coupling (urgency ↔ reenactment)
- **Expected**: R[NDAM,EO] = 0.85+ after 30 epochs

### Level 4: FAMILY - Organic Family Success
**File**: `persona_layer/organic_conversational_families.py`

- Crisis conversations cluster via 65D Euclidean distance
- Urgency dimension [33-34] **AMPLIFIED 2×** (key discriminator!)
- Expected families: "Crisis Response", "Exile Navigation", "Rage Containment"

### Level 5-7: TASK/EPOCH/GLOBAL
**Files**: Phase 5 learning integration

- Task-specific NDAM optimization
- Epoch statistics tracking keyword → felt-signature transition
- Global organism confidence evolution

---

## 📈 Expected Outcomes

### After 10 Epochs (Keyword Anchoring)
```
NDAM activation: 0% → 40-60%
Urgency variance: 0.000 → 0.25+ std
Zone 4 transformations: 0% → 15-25%
New keywords learned: 20-40
R[NDAM,EO]: 0.45 → 0.55
```

### After 30 Epochs (Felt-Recognition)
```
NDAM activation: 60-80%
Urgency variance: 0.35+ std (high differentiation)
Zone 4 transformations: 30-50%
New keywords learned: 100-200
R[NDAM,EO]: 0.70 → 0.85
```

### After 50+ Epochs (Mature Intelligence)
```
NDAM activation: 80-90%
Urgency variance: 0.40+ std (expert differentiation)
Zone 4-5 transformations: 50-70%
New keywords learned: 200-400
R[NDAM,EO]: 0.85-0.95 (fully coupled)
Felt-signature detection: 70%+ (beyond keywords)
```

---

## 🎓 Validation Test Cases

### Immediate Validation (With Keywords)

**Test 1**: "I'm terrified about Emma's surgery tomorrow"
- Expected: urgency 0.6-0.8, NDAM coherence > 0.7, Zone 4
- Keywords: "terrified", "surgery", "tomorrow"

**Test 2**: "I feel completely shut down and numb"
- Expected: urgency 0.3-0.5, NDAM coherence > 0.5, Zone 5, dorsal_vagal
- Keywords: "shut down", "numb"

**Test 3**: "I'm ashamed of this angry, resentful part of me"
- Expected: urgency 0.4-0.6, NDAM coherence > 0.6, Zone 4
- Keywords: "ashamed", "angry", "resentful"

### Future Validation (Without Keywords, Epoch 30+)

**Test 4**: "Everything feels too much right now, I can't find my center"
- Expected: urgency 0.5-0.7 (NO keyword match, pure felt-signature)
- Pattern: Dysregulation language → NDAM via R-matrix EO coupling

**Test 5**: "There's this part I don't want to look at"
- Expected: urgency 0.3-0.5 (NO keyword match, exile energy detected)
- Pattern: Avoidance + parts language → NDAM via BOND coupling

---

## 📁 Files Modified

### NDAM Configuration
**File**: `organs/modular/ndam/organ_config/ndam_config.py`

**Changes**:
- Added 40 personal/therapeutic crisis keywords (lines 72-97)
- Organized by exile energy type (fear, shame, dissociation, rage, abandonment)
- Keywords serve as **coherent attractors** for Hebbian learning

**Before**: 45 organizational keywords (deadline, crisis, urgent, dysfunction)
**After**: 85 comprehensive keywords (organizational + personal/therapeutic)

### Diagnostic Test
**File**: `diagnose_ndam_detection.py`

**Validation Results**:
```
Before keyword expansion:
- crisis_high_1: 0 keywords matched, urgency 0.000 ❌
- crisis_high_2: 1 keyword matched, urgency 0.600 ⚠️
- shadow_1: 0 keywords matched, urgency 0.000 ❌
- exile_1: 0 keywords matched, urgency 0.000 ❌

After keyword expansion:
- crisis_high_1: 2 keywords matched, urgency 0.650 ✅
- crisis_high_2: [retest pending]
- shadow_1: [retest pending]
- exile_1: [retest pending]
```

---

## 🚀 Next Steps

### Immediate
1. ✅ **DONE**: Add 40 personal crisis keywords to NDAM
2. **TODO**: Revalidate all 10 crisis test cases
3. **TODO**: Create wave training script with proven protocols

### Short-term (Wave Training)
4. **TODO**: Build Phase 1.1+1.2 combined training corpus (75 pairs)
5. **TODO**: Implement wave protocol (EXPANSIVE/NAVIGATION/CONCRESCENCE)
6. **TODO**: Run 10-epoch training, validate NDAM activation improves
7. **TODO**: Document keyword → felt-signature transition

### Medium-term (Fractal Learning Validation)
8. **TODO**: Track R[NDAM,EO] correlation over epochs
9. **TODO**: Measure new keyword acquisition rate
10. **TODO**: Validate felt-signature detection (without keyword matches)
11. **TODO**: Document organic family emergence (Crisis Response, Exile Navigation families)

---

## 🌀 Philosophy

### From Keywords to Felt-Recognition

**The keywords are scaffolding, not the building.**

Like learning to ride a bike:
- **Training wheels** (keywords): Bootstrap detection, provide initial stability
- **Wobbling** (R-matrix learning): Organ coupling strengthens, patterns emerge
- **Balance** (felt-signature): Mature recognition, keywords become optional
- **Mastery** (mature intelligence): Organism **feels** crisis energy, doesn't **match** keywords

The organism doesn't **become** the keywords. The keywords help the organism **recognize patterns** it will eventually feel directly through 65D transformation signatures, R-matrix coupling, and fractal family learning.

---

**Version**: 1.0
**Date**: November 17, 2025
**Status**: Keywords added, ready for wave training validation
**Impact**: Bootstrapped NDAM crisis detection, enabled Hebbian outgrowth trajectory
