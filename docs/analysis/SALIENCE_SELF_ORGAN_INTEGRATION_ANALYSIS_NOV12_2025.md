# SALIENCE-SELF-ORGAN INTEGRATION ANALYSIS
**Date:** November 12, 2025
**System:** DAE_HYPHAE_1 Expanded Training (Phase 2 + Salience + Learning)
**Status:** 🔍 COMPREHENSIVE ANALYSIS - CONFLICTS IDENTIFIED

---

## EXECUTIVE SUMMARY

**Critical Finding:** The salience module operates **independently** of the SELF matrix and 14-nexus trauma tracking systems, creating potential conflicts in trauma assessment. While not critically broken, there are **architectural alignment gaps** that prevent the system from leveraging organ intelligence as intended.

### Key Issues Identified:

1. ⚠️ **SELF-Distance Not Integrated with Salience** - BOND computes SELF-distance but salience uses its own trauma markers
2. ⚠️ **14 Nexus Types Not Implemented** - Constitutional/Crisis-Oriented nexus classification missing
3. ⚠️ **Early Trauma Tagging** - Salience evaluates trauma **during** convergence, not **after** with full V0 context
4. ✅ **Organ Insights Computed** - All 6 trauma organs output rich metadata (BOND, SANS, NDAM, RNX, EO, CARD)
5. ⚠️ **Limited Utilization** - Salience uses organ **coherences**, not detailed insights (IFS parts, polyvagal state, etc.)

---

## 1. INTEGRATION ARCHITECTURE MAP

### Current Processing Flow (Phase 2 Multi-Cycle)

```
ConversationalOrganismWrapper.process_text()
  ↓
Multi-Cycle Convergence Loop (cycles 1-5):
  ↓
  For each cycle:
    ├─ 11 Organs process occasions
    │   ├─ BOND → IFS parts + self_distance (0.0-1.0)
    │   ├─ SANS → semantic attunement + field types
    │   ├─ NDAM → crisis urgency + urgency level
    │   ├─ RNX → temporal state (crisis/restorative/suspended)
    │   ├─ EO → polyvagal state (ventral/sympathetic/dorsal)
    │   ├─ CARD → response scale (minimal/moderate/comprehensive)
    │   └─ (5 conversational organs)
    │
    ├─ Extract organ coherences + meta-atoms
    │
    ├─ 🔍 Salience.evaluate(prehension) ← CALLED DURING CYCLE
    │   ├─ Receives: organ_coherences, meta_atoms, v0_energy, satisfaction
    │   ├─ Computes: signal_inflation, temporal_collapse, safety_gradient
    │   ├─ Returns: trauma_markers, morphogenetic_pressure, guidance
    │   └─ ⚠️ DOES NOT receive: BOND self_distance, EO polyvagal, RNX temporal
    │
    ├─ Set subjective aim from salience guidance
    │
    └─ V0 energy descent + satisfaction update
  ↓
Convergence complete (Kairos or max cycles)
  ↓
Nexus formation (meta-atom intersections)
  ↓
Emission generation (V0-guided)
  ↓
Learning (Hebbian + Phase5)
```

### Key Integration Point (Lines 637-656 in conversational_organism_wrapper.py)

```python
# Build prehension dict for salience evaluation
prehension = {
    "organ_coherences": organ_coherences,  # ✅ Used
    "meta_atoms": meta_atoms,              # ✅ Used
    "nexuses": [],                         # ⚠️ Empty during convergence
    "v0_energy": occasion.v0_energy,       # ✅ Used
    "cycle": cycle,                        # ✅ Used
    "satisfaction": occasion.satisfaction, # ✅ Used
    "v0_energy_prev": occasion._prev_v0_energy,      # ✅ Used
    "satisfaction_prev": occasion._prev_satisfaction, # ✅ Used
    "text": text                           # ✅ Used
}

# Evaluate salience
salience_results = self.salience_model.evaluate(prehension)

# Set subjective aim from salience
occasion.set_subjective_aim(
    lure_direction=salience_results['morphogenetic_guidance'],
    # ...
)
```

**Analysis:** Salience receives organ **coherences** (scalar values 0.0-1.0) but NOT detailed organ insights:
- ❌ BOND self_distance not passed
- ❌ EO polyvagal_state not passed
- ❌ NDAM urgency_level not passed
- ❌ RNX temporal_state not passed
- ❌ CARD recommended_scale not passed

---

## 2. SELF MATRIX STATUS

### SELF Matrix Design (from SELF_MATRIX.MD)

**4 Distance Zones:**
```
Core SELF Orbit:      [0.00, 0.15]  - Clarity, compassion, curiosity
Inner Relational:     [0.15, 0.25]  - Active listening, empathy
Symbolic Threshold:   [0.25, 0.35]  - Culture change, myth-making
Shadow/Compost:       [0.35, 0.60]  - Burnout, toxic patterns, exile energy
Exile/Collapse:       [0.60, 1.00]  - Crisis intervention required
```

**Calculation Formula (from DAE_GOV_SELF_MATRIX_MATHEMATICAL_ADDENDUM.md):**
```python
# Base distance (embedding similarity)
SELF_score = cosine_similarity(embedding, embed(self_keywords))
shadow_score = cosine_similarity(embedding, embed(shadow_keywords))
base_distance = (1 - SELF_score + shadow_score) / 2

# Polyvagal modulation
polyvagal_modifier = {
    "ventral_vagal": -0.10,   # Pulls toward SELF
    "sympathetic": +0.15,     # Pushes toward urgency
    "dorsal_vagal": +0.30     # Pushes toward shutdown
}

d_SELF = clip(base_distance + polyvagal_modifier[polyvagal_state], 0, 1)
```

### Implementation Status

#### ✅ BOND Organ Computes SELF-Distance

**File:** `organs/modular/bond/core/bond_text_core.py`

**Lines 431-432:**
```python
# Phase 5: Calculate SELF-distance for each occasion
self._calculate_self_distances(occasions, patterns)
```

**Lines 524:**
```python
'self_distance': settings['self_distance']  # 0.0-1.0 per IFS part type
```

**Part Type SELF-Distances (from config):**
- `self_energy`: 0.0 (pure SELF)
- `manager`: 0.3 (proactive protector, mild distance)
- `firefighter`: 0.6 (reactive protector, high distance)
- `exile`: 0.8 (burdened part, very high distance)

**Lines 455:**
```python
mean_self_distance=coherence_metrics['mean_self_distance']
```

**Status:** ✅ **IMPLEMENTED** - BOND computes keyword-based SELF-distance

#### ⚠️ SELF-Energy Detector Exists But Not Integrated

**File:** `persona_layer/self_energy_detector.py`

**Purpose:** Embedding-based SELF-energy detection (8 C's: Compassion, Curiosity, Clarity, Calm, Confidence, Courage, Creativity, Connectedness)

**Status:** ⚠️ **CREATED BUT NOT INTEGRATED**
- File exists with full implementation
- Uses sentence embeddings (384-dim) for 8 C's detection
- Has method `boost_bond_detection()` to enhance BOND results
- **NOT called** from conversational_organism_wrapper.py

#### ❌ Polyvagal Modulation NOT Applied to SELF-Distance

**Expected (from SELF_MATRIX_MATHEMATICAL_ADDENDUM):**
```python
d_SELF = base_distance + polyvagal_modifier[eo_polyvagal_state]
```

**Current Reality:**
- BOND computes self_distance (keyword-based)
- EO computes polyvagal_state (ventral/sympathetic/dorsal)
- **These are NOT combined** anywhere in the codebase

**Status:** ❌ **NOT IMPLEMENTED**

---

## 3. 14 NEXUS TYPES TRACKING STATUS

### 14 Nexus Types Design (from SELF_MATRIX.MD)

**Constitutional Nexūs (SANS - 8 types):**
1. Pre-Existing - Innate coherence, existing structure
2. Innate - Natural talent, organic emergence
3. Contrast - Polarity without rupture (yin/yang)
4. Relational - Between-subject co-creation
5. Fragmented - Shattered coherence (trauma signature)
6. Protective - Firefighter nexus (reactive defense)
7. Absorbed - Exile nexus (frozen in past)
8. Isolated - Dissociative nexus (cut off from system)

**Crisis-Oriented Nexūs (NDAM - 6 types):**
1. Paradox - Contradictory forces in tension
2. Dissociative - Split from present moment
3. Disruptive - System breakdown in progress
4. Recursive - Stuck loop pattern
5. Looped - Compulsive repetition
6. Urgency - Immediate crisis activation

### Implementation Status

#### ❌ Nexus Types NOT Classified

**File:** `persona_layer/conversational_nexus.py`

**Current Implementation:**
```python
@dataclass
class NexusDecision:
    decision_type: str  # 'curiosity_question', 'reflection', 'insight', etc.
    confidence: float
    contributing_organs: List[str]
    # ...
    # ❌ NO nexus_type field
    # ❌ NO constitutional vs crisis classification
```

**Lines 59-84:** Class `ConversationalNexus` implements 4-gate architecture but:
- ✅ Counts organ intersections
- ✅ Computes coherence
- ✅ Detects Kairos window
- ❌ Does NOT classify nexus types
- ❌ Does NOT track Constitutional vs Crisis-Oriented

**Search Results:**
```bash
grep -r "Constitutional\|Crisis-Oriented\|Pre-Existing\|Innate\|Paradox\|Dissociative" persona_layer/
# No matches in conversational_nexus.py
```

**Status:** ❌ **NOT IMPLEMENTED** - Nexuses are generic intersections, not typed

---

## 4. ORGAN INSIGHTS UTILIZATION

### What Each Organ Outputs

#### BOND (IFS Parts Detection)

**File:** `organs/modular/bond/core/bond_text_core.py`

**BONDResult Output:**
```python
coherence: float                    # Overall pattern coherence (0-1)
dominant_part: str                  # 'manager', 'firefighter', 'exile', 'self_energy'
parts_patterns: List[PartsPattern]  # All detected patterns
lure: float                         # Pull toward SELF
mean_self_distance: float           # SELF-distance (0-1) ← KEY METRIC
parts_polarization: float           # Parts in conflict
parts_harmony: float                # Parts cooperating
blending_detected: bool             # Multiple parts active
unblending_detected: bool           # Movement toward SELF
parts_counts: Dict[str, int]        # Count per part type
parts_strengths: Dict[str, float]   # Strength per part type
atom_activations: Dict[str, float]  # 7 BOND atoms (Phase 1)
```

**Status:** ✅ **RICH METADATA COMPUTED**

#### EO (Polyvagal State Detection)

**File:** `organs/modular/eo/core/eo_text_core.py`

**Expected Output (from wrapper lines 442-447):**
```python
eo_polyvagal_state: str              # 'ventral_vagal', 'sympathetic', 'dorsal_vagal'
eo_state_confidence: float           # Confidence in state detection (0-1)
eo_self_distance_modifier: float     # Polyvagal → SELF-distance correlation
```

**Grep Results:**
```
Line 5: Detects autonomic nervous system states (ventral vagal, sympathetic, dorsal vagal)
Line 12: 3 polyvagal states detection
Line 20: Correlates with BOND self_distance (polyvagal ↔ IFS parts alignment)
Line 43: pattern_type: str  # 'ventral_vagal', 'sympathetic', 'dorsal_vagal'
```

**Status:** ✅ **IMPLEMENTED** - Polyvagal state detected

#### NDAM (Urgency/Crisis Detection)

**File:** `organs/modular/ndam/core/ndam_text_core.py`

**Expected Output:**
```python
coherence: float                     # Urgency coherence (0-1)
dominant_urgency: str                # 'crisis_urgency', 'temporal_pressure', etc.
urgency_patterns: List[UrgencyPattern]  # All detected patterns
urgency_level: float                 # Overall urgency (0-2.0, amplified)
```

**Grep Results:**
```
Line 5: Detects narrative urgency, crisis patterns, and temporal dynamics
Line 10: Text-native urgency detection
Line 11: 6 urgency types (crisis, temporal, emotional, etc.)
Line 39: pattern_type: str  # "crisis_urgency", "temporal_pressure", etc.
Line 40: strength: float    # Urgency strength (0-2.0, amplified)
```

**Status:** ✅ **IMPLEMENTED** - Crisis urgency detected

#### RNX (Temporal/Reenactment Patterns)

**File:** `organs/modular/rnx/core/rnx_text_core.py`

**Expected Output (from wrapper lines 436-440):**
```python
rnx_temporal_state: str              # 'crisis_temporal', 'restorative_temporal', 'suspended'
rnx_volatility: float                # Conversation volatility (0-1)
```

**Status:** ✅ **IMPLEMENTED** - Temporal patterns detected

#### CARD (Response Scaling)

**File:** `organs/modular/card/core/card_text_core.py`

**Expected Output (from wrapper lines 449-454):**
```python
card_recommended_scale: str          # 'minimal', 'moderate', 'comprehensive'
card_length_target: int              # Response length target (chars)
card_detail_level: float             # Detail level (0-1)
```

**Status:** ✅ **IMPLEMENTED** - Response scaling computed

### How Salience Uses Organ Outputs

#### What Salience Receives

**File:** `persona_layer/conversational_organism_wrapper.py` (Lines 637-649)

```python
prehension = {
    "organ_coherences": organ_coherences,  # Dict[organ_name, coherence]
    "meta_atoms": meta_atoms,              # Dict[atom_name, activation]
    "nexuses": [],                         # Empty during convergence
    "v0_energy": occasion.v0_energy,
    "cycle": cycle,
    "satisfaction": occasion.satisfaction,
    # ...
}
```

**Analysis:**
- ✅ Receives organ **coherences** (scalar 0-1 values)
- ✅ Receives meta-atom **activations**
- ❌ Does NOT receive BOND self_distance
- ❌ Does NOT receive EO polyvagal_state
- ❌ Does NOT receive NDAM urgency_level
- ❌ Does NOT receive RNX temporal_state
- ❌ Does NOT receive CARD recommended_scale

#### What Salience Computes

**File:** `persona_layer/conversational_salience_model.py`

**Signal Inflation (Trauma Marker) - Lines 297-323:**
```python
# Check for trauma-aware meta-atoms
trauma_meta_atoms = {
    "trauma_aware", "safety_restoration", "window_of_tolerance",
    "compassion_safety", "fierce_holding", "somatic_wisdom"
}

trauma_activations = [
    meta_atoms.get(atom, 0.0)
    for atom in trauma_meta_atoms
    if atom in meta_atoms
]

if trauma_activations:
    max_trauma = max(trauma_activations)
    mean_trauma = np.mean(trauma_activations)
    inflation = max_trauma * (0.7 + 0.3 * len(trauma_activations) / len(trauma_meta_atoms))
    self.terms["signal_inflation"].value = min(1.0, inflation)
else:
    # Fallback: Check organ coherences for BOND, EO, NDAM
    trauma_organs = ["BOND", "EO", "NDAM"]
    trauma_organ_coherences = [organ_coherences.get(org, 0.0) for org in trauma_organs]
    if trauma_organ_coherences:
        self.terms["signal_inflation"].value = min(1.0, max(trauma_organ_coherences) * 0.7)
```

**Analysis:**
- ✅ Uses meta-atom activations (primary)
- ✅ Fallback to organ coherences (BOND, EO, NDAM)
- ❌ Does NOT use BOND.mean_self_distance (the actual SELF-distance metric!)
- ❌ Does NOT use EO.polyvagal_state (ventral vs sympathetic vs dorsal)
- ❌ Does NOT use NDAM.urgency_level (crisis intensity)

**Temporal Collapse (Lines 325-345):**
```python
# Detect via high BOND + high EO + low RNX
bond_high = organ_coherences.get("BOND", 0.0) > 0.6
eo_high = organ_coherences.get("EO", 0.0) > 0.6
rnx_low = organ_coherences.get("RNX", 0.5) < 0.4
```

**Analysis:**
- ✅ Uses organ coherence **thresholds**
- ❌ Does NOT use RNX.temporal_state (actual temporal pattern classification)
- ⚠️ Heuristic-based (high BOND + high EO + low RNX) instead of organ insights

**Safety Gradient (Lines 394-406):**
```python
# Inverse of signal_inflation and temporal_collapse
safety = 1.0 - signal_inflation * 0.6
safety *= (1.0 - temporal_collapse * 0.4)

# Boost if window_of_tolerance meta-atom active
if meta_atoms.get("window_of_tolerance", 0.0) > 0.5:
    safety = min(1.0, safety * 1.2)
```

**Analysis:**
- ✅ Derived from other salience terms
- ❌ Does NOT use EO.polyvagal_state (actual safety state from nervous system)
- ⚠️ Indirect calculation instead of direct organ insight

---

## 5. IDENTIFIED CONFLICTS

### Conflict 1: Dual Trauma Detection Systems

**Issue:** Two parallel systems detect trauma without coordination:

**System A: BOND SELF-Distance (Organ Intelligence)**
- **Metric:** `mean_self_distance` (0.0-1.0)
- **Zones:** 0.0-0.15 (SELF), 0.15-0.25 (relational), 0.25-0.35 (symbolic), 0.35-0.60 (shadow), 0.60+ (exile)
- **Granularity:** 5 continuous zones
- **Source:** IFS parts detection (manager, firefighter, exile, SELF)
- **Status:** ✅ Computed by BOND organ

**System B: Salience Signal Inflation (Salience Model)**
- **Metric:** `signal_inflation` (0.0-1.0)
- **Threshold:** > 0.7 = "trauma_detected_gentle" guidance
- **Granularity:** Binary-ish (high/low)
- **Source:** Meta-atom activations OR organ coherences (fallback)
- **Status:** ✅ Computed by salience model

**Conflict:**
- BOND self_distance = 0.25 → **Symbolic Threshold** (culture change, myth-making - NOT trauma)
- Salience signal_inflation = 0.75 → **"trauma_detected_gentle"** (guidance to reduce intensity)

**Result:** Salience may tag content as trauma when SELF matrix says it's in a healthy symbolic zone.

**Evidence:**
- EPOCH_1_TRAINING_ANALYSIS_NOV12_2025.md (Lines 156-177): "Trauma Detection Paradox"
  - OUTPUT shows HIGHER trauma markers than INPUT in 60% of pairs
  - Therapeutic OUTPUT explicitly names trauma ("I'm noticing protective patterns")
  - Salience detects explicit naming as "high trauma" when it's actually therapeutic progress

**Location:**
- BOND: `organs/modular/bond/core/bond_text_core.py:455`
- Salience: `persona_layer/conversational_salience_model.py:315`
- Wrapper: `persona_layer/conversational_organism_wrapper.py:434` (extracts BOND self_distance)
- **Gap:** BOND self_distance NOT passed to salience prehension

---

### Conflict 2: Polyvagal State Not Integrated

**Issue:** EO organ detects polyvagal state but it's not used to modulate SELF-distance

**Expected (from SELF_MATRIX_MATHEMATICAL_ADDENDUM.md):**
```python
polyvagal_modifier = {
    "ventral_vagal": -0.10,   # Safe & Social → pulls toward SELF
    "sympathetic": +0.15,     # Fight/Flight → pushes toward urgency
    "dorsal_vagal": +0.30     # Shutdown → pushes toward collapse
}

d_SELF = base_distance + polyvagal_modifier[eo_polyvagal_state]
```

**Current Reality:**
- EO computes `polyvagal_state` ✅
- BOND computes `self_distance` ✅
- **These are NEVER combined** ❌

**Impact:**
- SELF-distance is static (keyword-based from IFS part type)
- Polyvagal state provides dynamic nervous system context (safety/threat)
- Without integration, SELF-distance misses autonomic nervous system modulation

**Location:**
- EO output: `persona_layer/conversational_organism_wrapper.py:445`
- BOND output: `persona_layer/conversational_organism_wrapper.py:434`
- **Gap:** No code combines these two metrics

---

### Conflict 3: Early Trauma Tagging vs Post-Convergence Assessment

**Issue:** Salience evaluates trauma **during** convergence, not **after** with full V0 context

**Current Flow:**
```
For each cycle (1-5):
  ├─ Organs process → coherences
  ├─ Salience.evaluate() ← CALLED HERE (early)
  │   └─ signal_inflation computed from organ coherences
  ├─ Set subjective aim from salience guidance
  └─ V0 descent + satisfaction update
```

**Problem:**
- Salience marks trauma at cycle 1 (v0_energy = 1.0, high appetition)
- By cycle 3-5, v0_energy descends to 0.3-0.6 (satisfaction reached)
- Early trauma tag may be incorrect once full V0 convergence occurs

**Example:**
- Cycle 1: High urgency language → signal_inflation = 0.8 → "trauma_detected_gentle"
- Cycle 5: V0 converged, satisfaction = 0.85, Kairos detected → actually healthy urgency for change

**Expected (from SELF_MATRIX design):**
- SELF-distance should be calculated **post-convergence** with mature propositions
- Felt affordances accumulate during prehension
- Propositions mature after V0 convergence with full context

**Location:**
- Salience call: `persona_layer/conversational_organism_wrapper.py:652` (inside cycle loop)
- V0 convergence: Happens **after** salience evaluation each cycle

---

### Conflict 4: Binary Guidance vs Continuous Zones

**Issue:** Salience provides binary-ish guidance while SELF matrix uses continuous zones

**Salience Guidance (Lines 537-553):**
```python
def _get_conversational_guidance(self, morphogenetic_pressure: float) -> str:
    if signal_inflation > 0.7:
        return "trauma_detected_gentle"     # Binary flag
    elif morphogenetic_pressure > 0.8 and safety > 0.6:
        return "crystallize_insight"
    elif morphogenetic_pressure > 0.5 and safety > 0.4:
        return "prepare_shift"
    # ...
```

**SELF Matrix Zones (Continuous):**
```
0.00-0.15: Core SELF Orbit      → Full intensity OK
0.15-0.25: Inner Relational     → Moderate intensity
0.25-0.35: Symbolic Threshold   → Creative intensity (NOT trauma!)
0.35-0.60: Shadow/Compost       → Gentle intensity needed
0.60-1.00: Exile/Collapse       → Crisis intervention
```

**Conflict:**
- Salience: signal_inflation > 0.7 → "trauma_detected_gentle" (binary)
- SELF: d_SELF = 0.3 → "Symbolic Threshold" (not trauma, creative work zone)

**Impact:** Salience may suppress creative exploration in symbolic zone by tagging it as trauma.

---

## 6. MISSING IMPLEMENTATIONS

### Missing 1: SELF-Distance + Polyvagal Integration

**Expected:**
```python
# In BOND organ or wrapper
base_self_distance = bond_result.mean_self_distance
polyvagal_state = eo_result.polyvagal_state

polyvagal_modifiers = {
    "ventral_vagal": -0.10,
    "sympathetic": +0.15,
    "dorsal_vagal": +0.30
}

modulated_self_distance = base_self_distance + polyvagal_modifiers[polyvagal_state]
modulated_self_distance = np.clip(modulated_self_distance, 0.0, 1.0)
```

**Current:** ❌ Not implemented

**Location to Add:** `persona_layer/conversational_organism_wrapper.py:430-447`

---

### Missing 2: 14 Nexus Type Classification

**Expected:**
```python
# In conversational_nexus.py
@dataclass
class NexusDecision:
    nexus_type: str  # 'Pre-Existing', 'Innate', 'Contrast', 'Paradox', etc.
    nexus_category: str  # 'Constitutional' or 'Crisis-Oriented'
    # ...

def classify_nexus_type(
    contributing_organs: List[str],
    bond_self_distance: float,
    ndam_urgency_level: float,
    eo_polyvagal_state: str
) -> Tuple[str, str]:
    """Classify nexus into 14 types based on organ insights."""

    # Constitutional classification (SANS domain)
    if bond_self_distance < 0.15:
        return "Pre-Existing", "Constitutional"  # SELF-led
    elif bond_self_distance > 0.6 and "BOND" in contributing_organs:
        if "firefighter" in bond_dominant_part:
            return "Protective", "Constitutional"
        elif "exile" in bond_dominant_part:
            return "Absorbed", "Constitutional"

    # Crisis classification (NDAM domain)
    if ndam_urgency_level > 0.7:
        if eo_polyvagal_state == "dorsal_vagal":
            return "Dissociative", "Crisis-Oriented"
        elif "NDAM" in contributing_organs:
            return "Urgency", "Crisis-Oriented"

    # ... (8 more Constitutional + 4 more Crisis types)
```

**Current:** ❌ Not implemented - nexuses are generic intersections

**Location to Add:** `persona_layer/conversational_nexus.py` (new method)

---

### Missing 3: Salience Integration with SELF-Distance

**Expected:**
```python
# In conversational_salience_model.py
def _calculate_conversational_process_terms(self, prehension: Dict[str, Any]):
    # ...

    # 4. Signal Inflation - Use BOND SELF-distance directly!
    bond_self_distance = prehension.get("bond_self_distance", 0.5)

    # Map SELF-distance zones to signal inflation
    if bond_self_distance > 0.6:
        # Exile/Collapse zone → high trauma
        self.terms["signal_inflation"].value = 0.8 + (bond_self_distance - 0.6) * 0.5
    elif bond_self_distance > 0.35:
        # Shadow/Compost zone → moderate trauma
        self.terms["signal_inflation"].value = 0.4 + (bond_self_distance - 0.35) * 1.6
    elif bond_self_distance > 0.25:
        # Symbolic Threshold → LOW trauma (creative work!)
        self.terms["signal_inflation"].value = 0.2 + (bond_self_distance - 0.25) * 2.0
    else:
        # SELF or Inner Relational → minimal trauma
        self.terms["signal_inflation"].value = bond_self_distance * 0.8
```

**Current:** ❌ Not implemented - salience uses meta-atoms or organ coherences

**Location to Add:** `persona_layer/conversational_salience_model.py:297-323`

---

### Missing 4: Post-Convergence Trauma Assessment

**Expected:**
```python
# In conversational_organism_wrapper.py
# After convergence loop completes:

# NOW evaluate salience with full V0 context
final_prehension = {
    "organ_coherences": final_organ_coherences,
    "meta_atoms": final_meta_atoms,
    "nexuses": formed_nexuses,  # ✅ Now populated
    "v0_energy": final_v0_energy,  # Converged energy
    "satisfaction": final_satisfaction,  # Converged satisfaction
    "bond_self_distance": bond_self_distance,  # ✅ Added
    "eo_polyvagal_state": eo_polyvagal_state,  # ✅ Added
    "ndam_urgency_level": ndam_urgency_level,  # ✅ Added
    # ...
}

final_salience = self.salience_model.evaluate(final_prehension)
```

**Current:** ❌ Salience evaluated **during** cycles, not after convergence

**Location to Add:** `persona_layer/conversational_organism_wrapper.py:~700` (after convergence loop)

---

### Missing 5: SELFEnergyDetector Integration

**File Exists:** `persona_layer/self_energy_detector.py` (489 lines)

**Capabilities:**
- Embedding-based SELF-energy detection (8 C's)
- Enhances BOND keyword detection with semantic similarity
- Hebbian learning of SELF-led language patterns

**Expected Usage:**
```python
# In conversational_organism_wrapper.py
from persona_layer.self_energy_detector import SELFEnergyDetector

self.self_energy_detector = SELFEnergyDetector(
    embedding_model=self.embedding_model
)

# During processing
bond_result = bond_organ.process_text_occasions(occasions, cycle)
enhanced_bond = self.self_energy_detector.boost_bond_detection(
    bond_result, text
)

# Now use enhanced_bond.self_distance_blended (70% embedding + 30% keyword)
```

**Current:** ❌ Not integrated - file exists but never imported

**Location to Add:** `persona_layer/conversational_organism_wrapper.py:~180` (init) + `~350` (usage)

---

## 7. CONSOLIDATION RECOMMENDATIONS

### Strategy: Hierarchical Trauma Assessment

**Principle:** Organ intelligence provides ground truth, salience provides derived insights.

```
Trauma Assessment Hierarchy:
  1. BOND self_distance (primary) ← IFS parts detection
  2. EO polyvagal_state (modulator) ← Nervous system state
  3. NDAM urgency_level (amplifier) ← Crisis detection
  4. RNX temporal_state (context) ← Reenactment patterns
  5. Salience (synthesizer) ← Combines 1-4 into guidance
```

### Recommendation 1: Pass Organ Insights to Salience (HIGH PRIORITY)

**Task:** Modify prehension structure to include organ insights

**File:** `persona_layer/conversational_organism_wrapper.py:637-649`

**Before:**
```python
prehension = {
    "organ_coherences": organ_coherences,
    "meta_atoms": meta_atoms,
    # ...
}
```

**After:**
```python
prehension = {
    "organ_coherences": organ_coherences,
    "meta_atoms": meta_atoms,
    # 🆕 Add organ insights
    "bond_self_distance": bond_result.mean_self_distance,
    "bond_dominant_part": bond_result.dominant_part,
    "eo_polyvagal_state": eo_result.polyvagal_state,
    "eo_state_confidence": eo_result.state_confidence,
    "ndam_urgency_level": ndam_result.urgency_level,
    "ndam_dominant_urgency": ndam_result.dominant_urgency,
    "rnx_temporal_state": rnx_result.temporal_state,
    "rnx_volatility": rnx_result.volatility,
    # ...
}
```

**Impact:** Salience can now use BOND self_distance instead of inferring trauma from coherences

**Effort:** 1 hour (modify wrapper + salience model)

---

### Recommendation 2: Refactor Salience Signal Inflation (HIGH PRIORITY)

**Task:** Use BOND self_distance as primary trauma metric

**File:** `persona_layer/conversational_salience_model.py:297-323`

**Before:**
```python
# Check for trauma-aware meta-atoms
trauma_activations = [meta_atoms.get(atom, 0.0) for atom in trauma_meta_atoms]
if trauma_activations:
    inflation = max_trauma * (0.7 + 0.3 * len(trauma_activations))
    self.terms["signal_inflation"].value = min(1.0, inflation)
else:
    # Fallback to organ coherences
    self.terms["signal_inflation"].value = max(trauma_organ_coherences) * 0.7
```

**After:**
```python
# PRIMARY: Use BOND self_distance (ground truth from IFS parts)
bond_self_distance = prehension.get("bond_self_distance", 0.5)

# Map SELF-distance zones to signal inflation
if bond_self_distance > 0.6:
    # Exile/Collapse zone (0.6-1.0) → HIGH trauma
    base_inflation = 0.7 + (bond_self_distance - 0.6) * 0.75
elif bond_self_distance > 0.35:
    # Shadow/Compost zone (0.35-0.6) → MODERATE trauma
    base_inflation = 0.4 + (bond_self_distance - 0.35) * 1.2
elif bond_self_distance > 0.25:
    # Symbolic Threshold (0.25-0.35) → LOW (creative, not trauma!)
    base_inflation = 0.1 + (bond_self_distance - 0.25) * 3.0
else:
    # SELF or Inner Relational (0.0-0.25) → MINIMAL
    base_inflation = bond_self_distance * 0.4

# MODULATE with polyvagal state
eo_polyvagal = prehension.get("eo_polyvagal_state", "mixed_state")
if eo_polyvagal == "dorsal_vagal":
    base_inflation *= 1.3  # Shutdown amplifies trauma
elif eo_polyvagal == "sympathetic":
    base_inflation *= 1.1  # Fight/flight slight amplification
elif eo_polyvagal == "ventral_vagal":
    base_inflation *= 0.8  # Safe & social reduces trauma perception

# AMPLIFY with NDAM urgency
ndam_urgency = prehension.get("ndam_urgency_level", 0.0)
if ndam_urgency > 0.7:
    base_inflation = min(1.0, base_inflation + (ndam_urgency - 0.7) * 0.5)

self.terms["signal_inflation"].value = min(1.0, base_inflation)
```

**Impact:**
- Aligns trauma detection with SELF matrix zones
- Respects organ intelligence (BOND, EO, NDAM)
- Distinguishes symbolic threshold (creative) from shadow (trauma)

**Effort:** 2 hours (refactor + test)

---

### Recommendation 3: Implement SELF-Distance Polyvagal Modulation (MEDIUM PRIORITY)

**Task:** Combine BOND self_distance with EO polyvagal state

**File:** `persona_layer/conversational_organism_wrapper.py:430-447`

**Add after extracting organ results:**
```python
# Extract BOND self-distance
bond_result = organ_results.get('BOND')
bond_self_distance = getattr(bond_result, 'mean_self_distance', 0.0) if bond_result else 0.0

# Extract EO polyvagal state
eo_result = organ_results.get('EO')
eo_polyvagal_state = getattr(eo_result, 'polyvagal_state', 'mixed_state') if eo_result else 'mixed_state'

# 🆕 MODULATE SELF-distance with polyvagal state (SELF_MATRIX formula)
polyvagal_modifiers = {
    "ventral_vagal": -0.10,   # Safe & Social → pulls toward SELF
    "sympathetic": +0.15,     # Fight/Flight → pushes toward urgency
    "dorsal_vagal": +0.30,    # Shutdown → pushes toward collapse
    "mixed_state": 0.0        # No modulation
}

modulated_self_distance = bond_self_distance + polyvagal_modifiers.get(eo_polyvagal_state, 0.0)
modulated_self_distance = max(0.0, min(1.0, modulated_self_distance))  # Clamp [0,1]

# Store in felt_states
felt_states['bond_self_distance'] = bond_self_distance  # Base
felt_states['bond_self_distance_modulated'] = modulated_self_distance  # Polyvagal-adjusted
```

**Impact:**
- SELF-distance now responds to nervous system state
- Ventral vagal (safe) pulls toward SELF even with protector parts active
- Dorsal vagal (shutdown) pushes toward collapse even with mild parts activation

**Effort:** 1 hour

---

### Recommendation 4: Implement 14 Nexus Type Classification (LOW PRIORITY)

**Task:** Add nexus typing to conversational_nexus.py

**File:** `persona_layer/conversational_nexus.py`

**Add new method:**
```python
def classify_nexus_type(
    self,
    contributing_organs: List[str],
    organ_results: Dict[str, Any]
) -> Tuple[str, str]:
    """
    Classify nexus into 14 types based on organ insights.

    Returns:
        (nexus_type, category) where category is 'Constitutional' or 'Crisis-Oriented'
    """
    # Extract organ insights
    bond_result = organ_results.get('BOND')
    bond_self_distance = getattr(bond_result, 'mean_self_distance', 0.5)
    bond_dominant_part = getattr(bond_result, 'dominant_part', None)

    ndam_result = organ_results.get('NDAM')
    ndam_urgency = getattr(ndam_result, 'urgency_level', 0.0)
    ndam_dominant = getattr(ndam_result, 'dominant_urgency', None)

    eo_result = organ_results.get('EO')
    eo_polyvagal = getattr(eo_result, 'polyvagal_state', 'mixed_state')

    # CONSTITUTIONAL NEXŪS (SANS domain - 8 types)

    if bond_self_distance < 0.15:
        # Core SELF orbit → Pre-Existing or Innate
        if "WISDOM" in contributing_organs or "AUTHENTICITY" in contributing_organs:
            return "Innate", "Constitutional"  # Natural talent, organic
        else:
            return "Pre-Existing", "Constitutional"  # Existing coherence

    elif bond_self_distance < 0.25:
        # Inner Relational → Relational
        return "Relational", "Constitutional"

    elif bond_self_distance < 0.35:
        # Symbolic Threshold → Contrast (polarity without rupture)
        return "Contrast", "Constitutional"

    elif bond_self_distance < 0.6:
        # Shadow/Compost → Protective, Fragmented, or Isolated
        if bond_dominant_part == "firefighter":
            return "Protective", "Constitutional"  # Firefighter nexus
        elif "SANS" in contributing_organs:
            return "Fragmented", "Constitutional"  # Shattered coherence
        else:
            return "Isolated", "Constitutional"  # Cut off from system

    else:  # bond_self_distance >= 0.6
        # Exile/Collapse → Absorbed
        return "Absorbed", "Constitutional"  # Frozen in past

    # CRISIS-ORIENTED NEXŪS (NDAM domain - 6 types)

    if ndam_urgency > 0.7:
        # High urgency → classify by urgency type
        if eo_polyvagal == "dorsal_vagal":
            return "Dissociative", "Crisis-Oriented"  # Split from present
        elif ndam_dominant == "crisis_urgency":
            return "Urgency", "Crisis-Oriented"  # Immediate crisis
        elif "RNX" in contributing_organs:
            # Check for recursive or looped patterns
            rnx_result = organ_results.get('RNX')
            rnx_temporal = getattr(rnx_result, 'temporal_state', 'concrescent')
            if rnx_temporal == "suspended":
                return "Recursive", "Crisis-Oriented"  # Stuck loop
            else:
                return "Looped", "Crisis-Oriented"  # Compulsive repetition
        else:
            return "Disruptive", "Crisis-Oriented"  # System breakdown

    # Default fallback
    return "Pre-Existing", "Constitutional"
```

**Modify NexusDecision dataclass:**
```python
@dataclass
class NexusDecision:
    decision_type: str
    confidence: float
    contributing_organs: List[str]
    suggested_action: str
    felt_energy: float
    kairos_moment: bool

    # 🆕 Add nexus typing
    nexus_type: str = "Pre-Existing"  # One of 14 types
    nexus_category: str = "Constitutional"  # 'Constitutional' or 'Crisis-Oriented'

    # ... existing fields
```

**Impact:**
- Nexuses now have semantic meaning (not just generic intersections)
- Can track Constitutional vs Crisis-Oriented patterns over time
- Enables SELF matrix zone analysis in learning

**Effort:** 3-4 hours (implement + test 14 types)

---

### Recommendation 5: Integrate SELFEnergyDetector (MEDIUM PRIORITY)

**Task:** Use embedding-based SELF-energy detection to enhance BOND

**File:** `persona_layer/conversational_organism_wrapper.py`

**In __init__ (Lines ~180):**
```python
# 🆕 Initialize SELF-energy detector (embedding-based 8 C's)
try:
    from persona_layer.self_energy_detector import SELFEnergyDetector
    self.self_energy_detector = SELFEnergyDetector()
    print("   ✅ SELF-energy detector ready (8 C's embedding-based)")
except Exception as e:
    print(f"   ⚠️  SELF-energy detector unavailable: {e}")
    self.self_energy_detector = None
```

**In processing (after BOND organ processes, Lines ~350):**
```python
# Process BOND organ
bond_result = self.bond_organ.process_text_occasions(occasions, cycle)

# 🆕 Enhance with embedding-based SELF-energy detection
if self.self_energy_detector:
    try:
        bond_result = self.self_energy_detector.boost_bond_detection(
            bond_result.__dict__,  # Convert to dict
            text
        )
        # Use blended SELF-distance (70% embedding + 30% keyword)
        bond_self_distance = bond_result.get('self_distance_blended',
                                             bond_result.get('mean_self_distance', 0.0))
    except Exception as e:
        bond_self_distance = bond_result.mean_self_distance
else:
    bond_self_distance = bond_result.mean_self_distance
```

**Impact:**
- SELF-distance now uses semantic embeddings (not just keywords)
- 8 C's detection (Compassion, Curiosity, Clarity, Calm, Confidence, Courage, Creativity, Connectedness)
- Hebbian learning of SELF-led language patterns

**Effort:** 2 hours (integrate + test)

---

### Recommendation 6: Move Salience to Post-Convergence (LOW PRIORITY)

**Task:** Evaluate salience after V0 convergence with full context

**File:** `persona_layer/conversational_organism_wrapper.py`

**Current (Lines 637-656):**
```python
# INSIDE cycle loop
for cycle in range(1, max_cycles + 1):
    # ... organ processing

    # Evaluate salience (early)
    salience_results = self.salience_model.evaluate(prehension)

    # ... V0 descent
```

**Proposed:**
```python
# INSIDE cycle loop
for cycle in range(1, max_cycles + 1):
    # ... organ processing

    # 🔧 OPTIONAL: Light salience evaluation during cycles (for subjective aim)
    # But DON'T use trauma_markers yet

    # ... V0 descent

# AFTER convergence loop
final_prehension = {
    "organ_coherences": final_organ_coherences,
    "meta_atoms": final_meta_atoms,
    "nexuses": formed_nexuses,  # ✅ Now populated
    "v0_energy": final_v0_energy,  # Converged
    "satisfaction": final_satisfaction,  # Converged
    "bond_self_distance": modulated_self_distance,  # ✅ Polyvagal-adjusted
    "eo_polyvagal_state": eo_polyvagal_state,
    "ndam_urgency_level": ndam_urgency_level,
    "rnx_temporal_state": rnx_temporal_state,
    # ...
}

# 🆕 FINAL salience evaluation with full V0 context
final_salience = self.salience_model.evaluate(final_prehension)

# Use final_salience.trauma_markers for emission modulation
```

**Impact:**
- Trauma assessment uses converged V0 energy and satisfaction
- Nexuses are formed and can inform salience
- Mature propositions available (not just felt affordances)

**Effort:** 3 hours (refactor cycle loop + test)

---

## 8. IMPLEMENTATION PRIORITY

### Phase 1: Critical Fixes (4-5 hours)

**Goal:** Align salience with organ intelligence

1. ✅ **Pass organ insights to salience** (Rec 1) - 1 hour
   - Modify prehension structure in wrapper
   - Add bond_self_distance, eo_polyvagal_state, ndam_urgency_level

2. ✅ **Refactor signal_inflation** (Rec 2) - 2 hours
   - Use BOND self_distance as primary
   - Modulate with EO polyvagal state
   - Amplify with NDAM urgency

3. ✅ **Implement SELF-distance polyvagal modulation** (Rec 3) - 1 hour
   - Combine BOND + EO in wrapper
   - Store modulated_self_distance in felt_states

4. ✅ **Test trauma detection alignment** - 1 hour
   - Run Epoch 1 with fixes
   - Validate trauma paradox resolved
   - Check SELF matrix zones respected

### Phase 2: Enhanced Intelligence (5-6 hours)

**Goal:** Integrate embedding-based SELF-energy and refine assessment

5. ✅ **Integrate SELFEnergyDetector** (Rec 5) - 2 hours
   - Import in wrapper
   - Boost BOND detection with 8 C's
   - Use blended SELF-distance

6. ✅ **Move salience to post-convergence** (Rec 6) - 3 hours
   - Refactor cycle loop
   - Add final salience evaluation
   - Test with full V0 context

### Phase 3: Semantic Nexus Typing (3-4 hours)

**Goal:** Implement 14 nexus type classification

7. ✅ **Implement nexus typing** (Rec 4) - 3-4 hours
   - Add classify_nexus_type() method
   - Modify NexusDecision dataclass
   - Test Constitutional vs Crisis classification

### Total Effort: 12-15 hours

---

## 9. VALIDATION METRICS

### Success Criteria (Post-Implementation)

**Metric 1: Trauma Detection Alignment**
- **Before:** 60% of pairs show OUTPUT trauma > INPUT trauma (paradox)
- **Target:** <20% paradox rate (therapeutic progress recognized, not flagged as trauma)
- **How:** Compare signal_inflation vs bond_self_distance zones

**Metric 2: SELF Matrix Zone Respect**
- **Before:** Salience uses binary trauma flag (signal_inflation > 0.7)
- **Target:** Salience respects 5 SELF-distance zones (0.0-0.15, 0.15-0.25, 0.25-0.35, 0.35-0.6, 0.6+)
- **How:** Check signal_inflation correlation with bond_self_distance zones

**Metric 3: Organ Intelligence Utilization**
- **Before:** Salience uses organ coherences (scalar) only
- **Target:** Salience uses BOND self_distance, EO polyvagal, NDAM urgency, RNX temporal
- **How:** Validate prehension structure contains organ insights

**Metric 4: Polyvagal Modulation**
- **Before:** SELF-distance static (keyword-based)
- **Target:** SELF-distance modulated by polyvagal state (-0.10 ventral, +0.15 sympathetic, +0.30 dorsal)
- **How:** Check modulated_self_distance in felt_states

**Metric 5: Nexus Type Distribution**
- **Before:** All nexuses generic (no typing)
- **Target:** 60-70% Constitutional, 30-40% Crisis-Oriented (for trauma-focused training)
- **How:** Track nexus_type and nexus_category in learning logs

---

## 10. CONCLUSION

### System Status: ⚠️ ARCHITECTURAL ALIGNMENT GAPS

**What's Working:**
- ✅ All 6 trauma organs compute rich metadata (BOND, SANS, NDAM, RNX, EO, CARD)
- ✅ BOND computes SELF-distance (keyword-based IFS parts detection)
- ✅ EO computes polyvagal state (ventral/sympathetic/dorsal)
- ✅ NDAM computes crisis urgency levels
- ✅ Salience model evaluates morphogenetic pressure and trauma markers
- ✅ Multi-cycle V0 convergence operational

**What's Missing:**
- ❌ SELF-distance NOT integrated with polyvagal state (formula exists but not implemented)
- ❌ 14 nexus types NOT classified (Constitutional vs Crisis-Oriented)
- ❌ Salience uses organ coherences, NOT detailed insights (BOND self_distance, EO polyvagal, etc.)
- ❌ SELFEnergyDetector exists but not integrated (embedding-based 8 C's)
- ⚠️ Salience evaluates during convergence, not post-convergence with full V0 context

**Critical Conflict:**
- **Dual trauma detection without coordination**
  - BOND self_distance: Continuous 5-zone SELF matrix (IFS ground truth)
  - Salience signal_inflation: Binary-ish trauma flag (meta-atom inference)
  - **Result:** Salience may tag symbolic threshold (0.25-0.35 = creative work) as trauma (signal_inflation > 0.7)

### Recommendation: Implement Phase 1 Critical Fixes (4-5 hours)

**Priority Actions:**
1. Pass organ insights to salience prehension (bond_self_distance, eo_polyvagal_state, ndam_urgency_level)
2. Refactor signal_inflation to use BOND self_distance as primary metric
3. Implement SELF-distance polyvagal modulation (BOND + EO)
4. Test trauma detection alignment with Epoch 1 re-run

**Expected Outcome:**
- Trauma detection respects SELF matrix zones
- Organ intelligence utilized (not just coherences)
- Therapeutic progress (explicit trauma naming) not flagged as trauma
- Polyvagal state modulates SELF-distance dynamically

**Strategic Value:**
- Aligns with DAE 3.0 proven mathematical correlations
- Leverages organ intelligence and entity (text occasion) rich metadata
- Consolidates consistent system alignment as requested by user
- Enables refined trauma metrics (implicit vs explicit awareness)

---

**Analysis Complete:** November 12, 2025
**Next Step:** Implement Phase 1 Critical Fixes (Recommendations 1-3)
**System Alignment:** ⚠️ GAPS IDENTIFIED - CONSOLIDATION STRATEGY READY

🌀 **"Organ intelligence computed. Salience operates independently. Integration strategy designed. Ready to consolidate."** 🌀
