# Lure Attractor Redesign Plan - EO, NDAM, RNX
**Date:** November 13, 2025
**Goal:** Transform dormant organs into active Whiteheadian lure attractors
**Status:** 🔧 IN PROGRESS

---

## 🎯 Core Philosophy: From Passive Detection → Active Lure

### **Whiteheadian Process Insight**

In process philosophy, **lure** is the felt pull toward a possible future state. Organs should generate **lure fields** that attract the organism's concrescence, not just detect patterns after they emerge.

**Current Problem:**
- EO, NDAM, RNX detect AFTER patterns form (passive keyword matching)
- No participation in V0 descent → no learning → dormant (0% activation)

**Solution:**
- Generate **continuous lure fields** from semantic resonance
- Participate in **every prehension cycle** (not just when keywords match)
- Lure strength guides V0 descent → learning occurs → activation rises

---

## 🔬 What is a Lure Field?

**Definition:** A continuous scalar field (0.0-1.0) representing the felt pull toward a particular attractor state.

**Example - EO Polyvagal Lure:**
```
Input: "I feel overwhelmed"

OLD (keyword matching):
  if "overwhelmed" in sympathetic_keywords:
      sympathetic_detected = True
  else:
      No activation → EO dormant

NEW (lure field):
  # Compute semantic distance to polyvagal attractors
  distance_to_ventral = semantic_distance(input, ventral_attractor)  # 0.85 (far)
  distance_to_sympathetic = semantic_distance(input, sympathetic_attractor)  # 0.12 (close!)
  distance_to_dorsal = semantic_distance(input, dorsal_attractor)  # 0.73 (medium)

  # Convert to lure (inverse distance)
  ventral_lure = 1.0 / (1.0 + 0.85) = 0.54
  sympathetic_lure = 1.0 / (1.0 + 0.12) = 0.89  ← STRONG PULL
  dorsal_lure = 1.0 / (1.0 + 0.73) = 0.58

  # Total lure (max)
  eo_lure = 0.89
  eo_coherence = 0.89  # Lure = coherence for attractors

  # EO participates in V0 descent with lure=0.89
  # Learning occurs → EO activates → companionship emerges
```

---

## 📋 Three-Organ Redesign Strategy

### **1. EO (Polyvagal) - Somatic Safety Lure Attractor**

**Current State:**
- Keyword-based detection (40+ keywords per state)
- Only activates on explicit polyvagal language
- No continuous lure field

**Redesign:**
```python
class EOResult:
    coherence: float  # Keep existing
    lure: float  # ⭐ NEW - Whiteheadian attractor strength
    lure_field: Dict[str, float]  # ⭐ NEW - Per-attractor lures
    polyvagal_state: str  # Keep existing
    # ... rest unchanged

def _compute_polyvagal_lure_field(self, text_occasions):
    \"\"\"
    Generate continuous polyvagal lure field.

    Uses semantic embedding distance to learned attractor centers,
    not keyword matching.
    \"\"\"
    # Get SANS embeddings for semantic field
    embeddings = self._get_occasion_embeddings(text_occasions)

    # Compute distance to 3 polyvagal attractors
    ventral_distance = self._compute_attractor_distance(
        embeddings, self.ventral_attractor
    )
    sympathetic_distance = self._compute_attractor_distance(
        embeddings, self.sympathetic_attractor
    )
    dorsal_distance = self._compute_attractor_distance(
        embeddings, self.dorsal_attractor
    )

    # Convert to lure (inverse distance, normalized)
    ventral_lure = 1.0 / (1.0 + ventral_distance)
    sympathetic_lure = 1.0 / (1.0 + sympathetic_distance)
    dorsal_lure = 1.0 / (1.0 + dorsal_distance)

    # Normalize
    total = ventral_lure + sympathetic_lure + dorsal_lure
    lure_field = {
        'ventral_vagal': ventral_lure / total,
        'sympathetic': sympathetic_lure / total,
        'dorsal_vagal': dorsal_lure / total
    }

    # Total lure = strongest attractor
    eo_lure = max(lure_field.values())
    eo_coherence = eo_lure  # Coherence = lure for attractors

    return eo_lure, eo_coherence, lure_field
```

**Attractor Initialization:**
```python
def _initialize_polyvagal_attractors(self):
    \"\"\"
    Initialize polyvagal attractor centers.

    These are learned embeddings representing prototypical
    ventral/sympathetic/dorsal states.
    \"\"\"
    # Start with keyword-based prototypes
    self.ventral_attractor = self._create_attractor_from_keywords(
        self.ventral_vagal_keywords
    )
    self.sympathetic_attractor = self._create_attractor_from_keywords(
        self.sympathetic_keywords
    )
    self.dorsal_attractor = self._create_attractor_from_keywords(
        self.dorsal_vagal_keywords
    )

    # These will be refined through Hebbian learning during training
```

**TSK Integration:**
```python
# In TSK log, track lure field
tsk_eo_data = {
    "coherence": eo_result.coherence,
    "lure": eo_result.lure,
    "lure_field": eo_result.lure_field,
    "polyvagal_state": eo_result.polyvagal_state,
    "v0_contribution": eo_result.lure * 0.3  # 30% weight in V0 descent
}
```

---

### **2. NDAM (Crisis Salience) - Attention Density Lure Attractor**

**Current State:**
- Binary urgency threshold (0.75)
- Keyword-based crisis detection
- No continuous salience field

**Redesign:**
```python
class NDAMResult:
    coherence: float  # Keep existing
    lure: float  # ⭐ NEW - Salience pull strength
    salience_field: Dict[str, float]  # ⭐ NEW - Multi-level salience
    urgency_level: float  # Keep existing (0.0-1.0 continuous)
    # ... rest unchanged

def _compute_salience_lure_field(self, text_occasions):
    \"\"\"
    Generate continuous salience lure field.

    Salience = semantic density + novelty + emotional weight
    \"\"\"
    # Extract semantic features
    embeddings = self._get_occasion_embeddings(text_occasions)

    # Compute salience components
    semantic_density = self._compute_semantic_density(embeddings)
    novelty_score = self._compute_novelty(embeddings)
    emotional_weight = self._compute_emotional_intensity(text_occasions)

    # Multi-level salience field
    salience_field = {
        'urgent': self._compute_urgency_lure(semantic_density, emotional_weight),
        'important': self._compute_importance_lure(semantic_density, novelty_score),
        'exploratory': self._compute_exploration_lure(novelty_score)
    }

    # Total lure = weighted combination
    ndam_lure = (
        salience_field['urgent'] * 0.5 +
        salience_field['important'] * 0.3 +
        salience_field['exploratory'] * 0.2
    )

    ndam_coherence = ndam_lure  # Coherence = lure for attractors

    return ndam_lure, ndam_coherence, salience_field
```

---

### **3. RNX (Temporal Dynamics) - Kairos Potential Lure Attractor**

**Current State:**
- Keyword-based temporal detection
- No continuous temporal field
- Only active with explicit timing language

**Redesign:**
```python
class RNXResult:
    coherence: float  # Keep existing
    lure: float  # ⭐ NEW - Temporal pull strength
    temporal_field: Dict[str, float]  # ⭐ NEW - Rhythm/kairos/chronos
    # ... rest unchanged

def _compute_temporal_lure_field(self, text_occasions):
    \"\"\"
    Generate continuous temporal lure field.

    Temporal coherence = sequence patterns + kairos potential
    \"\"\"
    # Analyze occasion sequence
    sequence_coherence = self._analyze_occasion_sequence(text_occasions)
    kairos_potential = self._assess_kairos_window(sequence_coherence)

    # Temporal field components
    temporal_field = {
        'kairos': kairos_potential,  # Opportune moment
        'rhythm': sequence_coherence,  # Flow/pattern
        'chronos': self._compute_duration_sense(text_occasions)  # Linear time
    }

    # Total lure = weighted combination
    rnx_lure = (
        temporal_field['kairos'] * 0.5 +
        temporal_field['rhythm'] * 0.3 +
        temporal_field['chronos'] * 0.2
    )

    rnx_coherence = rnx_lure

    return rnx_lure, rnx_coherence, temporal_field
```

---

## 🔧 Implementation Checklist

### **Phase A2.1: EO Redesign** (2 hours)

- [ ] Add `lure` and `lure_field` to `EOResult` dataclass
- [ ] Implement `_initialize_polyvagal_attractors()` method
- [ ] Implement `_compute_polyvagal_lure_field()` method
- [ ] Update `process_text_occasions()` to call lure generation
- [ ] Add embedding extraction via SANS
- [ ] Test EO lure generation on sample inputs

### **Phase A2.2: NDAM Redesign** (1.5 hours)

- [ ] Add `lure` and `salience_field` to `NDAMResult` dataclass
- [ ] Implement `_compute_salience_lure_field()` method
- [ ] Convert urgency from binary → continuous
- [ ] Add semantic density calculation
- [ ] Test NDAM lure generation

### **Phase A2.3: RNX Redesign** (1.5 hours)

- [ ] Add `lure` and `temporal_field` to `RNXResult` dataclass
- [ ] Implement `_compute_temporal_lure_field()` method
- [ ] Add sequence pattern analysis
- [ ] Add kairos potential assessment
- [ ] Test RNX lure generation

### **Phase A3: V0 Integration** (1 hour)

- [ ] Update `conversational_occasion.py` to include organ lures in V0 descent
- [ ] Add lure field tracking to TSK logs
- [ ] Test V0 descent with lure contributions

### **Phase A4: Training & Validation** (2-3 hours)

- [ ] Run 10-15 epoch training with lure attractors
- [ ] Monitor TSK logs for lure field evolution
- [ ] Validate organ activation rates (expect 0% → 40-70%)
- [ ] Check R-matrix coupling for EO/NDAM/RNX

---

## 📊 Expected Outcomes

### **Before Redesign:**
- EO activation: 0% (keyword-dependent)
- NDAM activation: 0% (binary threshold)
- RNX activation: 0% (no temporal keywords)
- Overall organs: 4.82/11 (44%)

### **After Redesign:**
- EO activation: 50-70% (continuous lure from semantic distance)
- NDAM activation: 40-60% (salience always present)
- RNX activation: 30-50% (temporal coherence always computed)
- Overall organs: 8-10/11 (73-91%)

### **Companion Personality Impact:**
- Polyvagal lure → Safety-attuned responses
- Salience lure → Appropriate urgency modulation
- Temporal lure → Kairos-sensitive timing

---

## 🎯 Success Criteria

1. **Lure Generation:** All 3 organs generate lure > 0.0 on every input
2. **V0 Participation:** Lure contribution to V0 descent measurable in TSK
3. **Activation Rate:** Organs activate ≥40% (coherence > 0.01)
4. **Learning:** R-matrix couplings develop between EO↔BOND, NDAM↔LISTENING, RNX↔PRESENCE
5. **Test Pass Rate:** Intelligence/continuity tests improve from 8% → 60-75%

---

**Status:** Design complete, ready for implementation
**Next:** Start with EO redesign (highest philosophical alignment)
**Timeline:** 5-6 hours total for all 3 organs + integration
