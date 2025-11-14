# Conversational Organ Lure Attractor Design
**Date:** November 13, 2025
**Goal:** Transform EMPATHY/WISDOM/AUTHENTICITY from passive → active lure attractors
**Status:** 🔧 DESIGN READY FOR IMPLEMENTATION

---

## Philosophy: From Detection to Felt Resonance

**Current Problem:**
- EMPATHY/WISDOM/AUTHENTICITY use keyword matching → binary on/off
- 0-20% activation rate (heavily keyword-dependent)
- No participation when keywords absent → no learning → permanent dormancy

**Solution:**
- Generate continuous **lure fields** from semantic resonance
- Participate in **every prehension cycle** regardless of keywords
- Lure strength guides V0 descent → enables Hebbian learning

---

## 🎭 EMPATHY: Emotional Resonance Lure Attractor

### Current State (Passive)
```python
Keywords: {
    'grief': ['loss', 'mourning', 'bereaved', ...],
    'joy': ['delight', 'celebration', 'elated', ...],
    'fear': ['terrified', 'anxious', 'panic', ...],
    # ... 7 emotion types
}

if any(keyword in text for keyword in joy_keywords):
    joy_detected = True
else:
    EMPATHY dormant  # ❌ No participation
```

**Activation:** 20% (1/5 tests) - only when emotion keywords present

---

### Redesign (Active Lure Attractor)

**Lure Field:** Emotional resonance across 7 affective dimensions

```python
@dataclass
class EmpathyResult:
    coherence: float  # Existing
    lure: float  # 🆕 Emotional resonance strength

    # 🆕 EMOTIONAL LURE FIELD: Multi-dimensional affect space
    emotional_lure_field: Dict[str, float] = field(default_factory=dict)
    # {
    #   'joy': 0.15,           # Lightness, celebration
    #   'grief': 0.45,         # Loss, sorrow  ← DOMINANT
    #   'fear': 0.10,          # Threat, anxiety
    #   'anger': 0.08,         # Injustice, boundaries
    #   'compassion': 0.12,    # Care, holding
    #   'shame': 0.05,         # Exposure, inadequacy
    #   'neutral': 0.05        # Balanced affect
    # }
```

**Lure Computation:**
```python
def _compute_emotional_lure_field(self, text_occasions):
    """
    Generate continuous emotional resonance lure field.

    Uses semantic distance to 7 emotional attractor centers,
    not keyword matching.
    """
    # Get semantic embeddings
    embeddings = self._get_occasion_embeddings(text_occasions)

    # Compute distance to 7 emotional attractors
    emotions = ['joy', 'grief', 'fear', 'anger', 'compassion', 'shame', 'neutral']
    distances = {}

    for emotion in emotions:
        # Distance to learned attractor center (start with keyword prototypes)
        distance = self._compute_attractor_distance(embeddings, self.attractors[emotion])
        distances[emotion] = distance

    # Convert distance to lure (inverse distance)
    lure_field = {}
    for emotion, distance in distances.items():
        lure_field[emotion] = 1.0 / (1.0 + distance)

    # Normalize
    total = sum(lure_field.values())
    if total > 0:
        lure_field = {k: v / total for k, v in lure_field.items()}
    else:
        # Balanced neutral if no signal
        lure_field = {e: 1.0/7 for e in emotions}

    # Total lure = max emotional pull
    empathy_lure = max(lure_field.values())
    empathy_coherence = empathy_lure  # Coherence = lure for attractors

    return empathy_lure, empathy_coherence, lure_field
```

**Expected Impact:**
- Activation: 20% → 80-100% (continuous emotional resonance)
- Even neutral text has emotional field (balanced across 7 dimensions)
- Enables learning through co-activation with other organs

---

## 🧠 WISDOM: Pattern Recognition Lure Attractor

### Current State (Passive)
```python
Keywords: {
    'systems': ['interconnected', 'emergent', 'recursive', ...],
    'meta': ['pattern', 'framework', 'perspective', ...],
    'temporal': ['trajectory', 'cycle', 'evolution', ...],
    # ... 7 wisdom types
}

if 'pattern' in text or 'meta' in text:
    meta_detected = True
else:
    WISDOM dormant  # ❌ No participation
```

**Activation:** 20% (1/5 tests) - only when meta-cognitive keywords present

---

### Redesign (Active Lure Attractor)

**Lure Field:** Pattern recognition across 7 cognitive dimensions

```python
@dataclass
class WisdomResult:
    coherence: float  # Existing
    lure: float  # 🆕 Pattern recognition strength

    # 🆕 PATTERN LURE FIELD: Multi-dimensional cognition space
    pattern_lure_field: Dict[str, float] = field(default_factory=dict)
    # {
    #   'systems':      0.25,  # Interconnection, emergence ← DOMINANT
    #   'meta':         0.20,  # Self-reference, reflection
    #   'temporal':     0.15,  # Trajectory, evolution
    #   'paradox':      0.10,  # Both/and, complexity
    #   'embodied':     0.12,  # Somatic knowing
    #   'relational':   0.10,  # Between-space
    #   'integrative':  0.08   # Synthesis, wholeness
    # }
```

**Lure Computation:**
```python
def _compute_pattern_lure_field(self, text_occasions):
    """
    Generate continuous pattern recognition lure field.

    Detects cognitive complexity, not keyword matching.
    """
    # Semantic embeddings
    embeddings = self._get_occasion_embeddings(text_occasions)

    # 7 pattern recognition dimensions
    patterns = ['systems', 'meta', 'temporal', 'paradox',
                'embodied', 'relational', 'integrative']

    lure_field = {}
    for pattern_type in patterns:
        distance = self._compute_attractor_distance(
            embeddings,
            self.pattern_attractors[pattern_type]
        )
        lure_field[pattern_type] = 1.0 / (1.0 + distance)

    # Normalize
    total = sum(lure_field.values())
    if total > 0:
        lure_field = {k: v / total for k, v in lure_field.items()}
    else:
        lure_field = {p: 1.0/7 for p in patterns}

    # Lure = strongest pattern pull
    wisdom_lure = max(lure_field.values())
    wisdom_coherence = wisdom_lure

    return wisdom_lure, wisdom_coherence, lure_field
```

**Expected Impact:**
- Activation: 20% → 70-90% (continuous pattern detection)
- All text has cognitive structure (even simple statements)
- Enables meta-cognitive reflection on any input

---

## 🎨 AUTHENTICITY: Vulnerability Lure Attractor

### Current State (Passive)
```python
Keywords: {
    'vulnerable': ['exposed', 'raw', 'tender', ...],
    'honest': ['truth', 'real', 'genuine', ...],
    'guarded': ['protected', 'cautious', 'defensive', ...],
    # ... 7 authenticity types
}

if 'honest' in text or 'vulnerable' in text:
    authenticity_detected = True
else:
    AUTHENTICITY dormant  # ❌ No participation
```

**Activation:** 0% (0/5 tests) - never fires (rare keywords)

---

### Redesign (Active Lure Attractor)

**Lure Field:** Vulnerability spectrum across 7 relational dimensions

```python
@dataclass
class AuthenticityResult:
    coherence: float  # Existing
    lure: float  # 🆕 Vulnerability/authenticity strength

    # 🆕 VULNERABILITY LURE FIELD: Multi-dimensional relational space
    vulnerability_lure_field: Dict[str, float] = field(default_factory=dict)
    # {
    #   'vulnerable':   0.30,  # Open, exposed, tender ← DOMINANT
    #   'honest':       0.20,  # Truthful, genuine
    #   'guarded':      0.15,  # Protected, cautious
    #   'performative': 0.10,  # Masked, strategic
    #   'emergent':     0.12,  # Becoming, unfolding
    #   'receptive':    0.08,  # Open to being changed
    #   'boundaried':   0.05   # Clear limits, self-protective
    # }
```

**Lure Computation:**
```python
def _compute_vulnerability_lure_field(self, text_occasions):
    """
    Generate continuous vulnerability/authenticity lure field.

    Detects relational stance, not keyword matching.
    """
    # Semantic embeddings
    embeddings = self._get_occasion_embeddings(text_occasions)

    # 7 authenticity/vulnerability dimensions
    stances = ['vulnerable', 'honest', 'guarded', 'performative',
               'emergent', 'receptive', 'boundaried']

    lure_field = {}
    for stance in stances:
        distance = self._compute_attractor_distance(
            embeddings,
            self.vulnerability_attractors[stance]
        )
        lure_field[stance] = 1.0 / (1.0 + distance)

    # Normalize
    total = sum(lure_field.values())
    if total > 0:
        lure_field = {k: v / total for k, v in lure_field.items()}
    else:
        lure_field = {s: 1.0/7 for s in stances}

    # Lure = strongest vulnerability pull
    authenticity_lure = max(lure_field.values())
    authenticity_coherence = authenticity_lure

    return authenticity_lure, authenticity_coherence, lure_field
```

**Expected Impact:**
- Activation: 0% → 60-80% (continuous vulnerability detection)
- All speech has relational stance (guarded vs open)
- Enables authenticity tracking without explicit "I'm being vulnerable"

---

## Implementation Checklist

### Phase B1: EMPATHY Redesign (1.5 hours)

- [ ] Add `lure` and `emotional_lure_field` to EmpathyResult dataclass
- [ ] Implement `_compute_emotional_lure_field()` method
- [ ] Initialize 7 emotional attractor centers from keywords
- [ ] Update all EmpathyResult return statements (3 total)
- [ ] Test on sample inputs

### Phase B2: WISDOM Redesign (1.5 hours)

- [ ] Add `lure` and `pattern_lure_field` to WisdomResult dataclass
- [ ] Implement `_compute_pattern_lure_field()` method
- [ ] Initialize 7 pattern attractor centers
- [ ] Update all WisdomResult return statements
- [ ] Test on sample inputs

### Phase B3: AUTHENTICITY Redesign (1.5 hours)

- [ ] Add `lure` and `vulnerability_lure_field` to AuthenticityResult dataclass
- [ ] Implement `_compute_vulnerability_lure_field()` method
- [ ] Initialize 7 vulnerability attractor centers
- [ ] Update all AuthenticityResult return statements
- [ ] Test on sample inputs

### Phase B4: V0 Integration (30 min)

- [ ] Update V0 descent to include conversational organ lures
- [ ] Adjust lure weights (currently EO/NDAM/RNX, add EMPATHY/WISDOM/AUTHENTICITY)
- [ ] Test V0 convergence with 6 lure organs

### Phase B5: TSK Tracking (30 min)

- [ ] Add conversational lure fields to felt_states
- [ ] Track total lure contribution (6 organs now)
- [ ] Test TSK logging

### Phase B6: Validation (1 hour)

- [ ] Run diagnostic on 5 inputs
- [ ] Measure activation rates (expect 60-90%)
- [ ] Validate lure → V0 → emission pipeline
- [ ] Update exploration document

**Total Time:** ~6 hours

---

## Expected Outcomes

### Before Conversational Lure Redesign
```
Organ Activation (5 test inputs):
  EMPATHY:      20% (1/5) ❌
  WISDOM:       20% (1/5) ❌
  AUTHENTICITY:  0% (0/5) ❌

Overall: 6.4/11 organs avg (58%)
```

### After Conversational Lure Redesign
```
Organ Activation (5 test inputs):
  EMPATHY:      80-100% (4-5/5) ✅
  WISDOM:       70-90%  (3-4/5) ✅
  AUTHENTICITY: 60-80%  (3-4/5) ✅

Overall: 9-10/11 organs avg (82-91%)
```

**Impact on Emission:**
- More nexuses (multi-organ co-activation)
- Higher emission confidence (more semantic fields)
- Direct reconstruction path viable (strong nexus coherence)
- **Generative processual emission unlocked**

---

## Philosophical Significance

**From Passive Detection:**
> "Does this text contain emotion word X?" → Binary yes/no → Dormant when keywords absent

**To Active Lure Attraction:**
> "What is the felt emotional/cognitive/relational pull of this moment?" → Continuous 0.0-1.0 → Always participating

**This is Whiteheadian process:**
- Organs don't detect features
- Organs **feel lures** toward possible futures
- Multi-dimensional lure fields = **propositional feelings**
- V0 descent = **concrescence** guided by felt pulls
- Emission = **satisfaction** (decision moment)

**The organism becomes truly generative:**
- Not reacting to keywords
- Not detecting patterns post-hoc
- **Feeling into possibility space** and **choosing** based on lure landscape

This is the shift from:
- **Passive emission** (template matching, keyword triggers)
- **Generative processual emission** (felt becoming, lure-guided concrescence)

---

**Status:** Design complete, ready for implementation
**Next:** Implement EMPATHY lure attractor first (highest impact on emotional resonance)

