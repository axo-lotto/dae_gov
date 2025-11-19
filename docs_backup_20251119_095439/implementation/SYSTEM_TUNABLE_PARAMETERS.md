# DAE_HYPHAE_1 - Comprehensive System Tunable Parameters
**Date**: November 12, 2025 (Updated with Phase 2 + Salience)
**System**: 11-Organ Trauma-Informed Conversational AI with Multi-Cycle V0 + Salience
**Status**: Training-Ready Configuration + Tuning Guide

---

## 📋 Table of Contents

1. [🆕 Phase 2: Multi-Cycle V0 Convergence Parameters](#phase-2-multi-cycle-v0-convergence-parameters)
2. [🆕 Salience Model Parameters](#salience-model-parameters)
3. [🆕 Meta-Atom Parameters](#meta-atom-parameters)
4. [Emission Generation Parameters](#emission-generation-parameters)
5. [Semantic Field Extraction Parameters](#semantic-field-extraction-parameters)
6. [Nexus Intersection Composition Parameters](#nexus-intersection-composition-parameters)
7. [Conversational Organ Parameters](#conversational-organ-parameters)
8. [Trauma/Context Organ Parameters](#traumacontext-organ-parameters)
9. [Hebbian Learning Parameters](#hebbian-learning-parameters)
10. [Phase 5 Organic Learning Parameters](#phase-5-organic-learning-parameters)
11. [Global Organism Parameters](#global-organism-parameters)
12. [Tuning Recommendations](#tuning-recommendations)

---

## 🆕 Phase 2: Multi-Cycle V0 Convergence Parameters

**File**: `persona_layer/conversational_organism_wrapper.py` (method: `_multi_cycle_convergence()`)

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **max_cycles** | 5 | [3, 10] | int | Maximum convergence cycles before forced termination | Higher → allows more convergence iterations, slower |
| **convergence_threshold** | 0.1 | [0.05, 0.2] | float | ΔE threshold for satisfaction-driven convergence | Lower → converges faster, may under-converge |
| **kairos_window_min** | 0.45 | [0.3, 0.6] | float | Lower bound of Kairos satisfaction window (Gate 3) | - |
| **kairos_window_max** | 0.70 | [0.6, 0.9] | float | Upper bound of Kairos satisfaction window (Gate 3) | - |

**V0 Energy Descent Formula** (DAE 3.0 validated):
```python
# Located in conversational_occasion.py → descend_v0_energy()
# Coefficients from DAE 3.0 (empirically tuned on 2400 ARC tasks)
α = 0.40  # Satisfaction weight (primary driver)
β = 0.25  # Energy change momentum
γ = 0.15  # Agreement weight (1 - std(coherences))
δ = 0.10  # Resonance weight (mean coherence)
ζ = 0.10  # Intensity weight (max coherence)

E(t) = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I)

# Satisfaction calculation
S = 1.0 - E(t) * (1.0 - R)
```

**Kairos Detection (4-Condition Gate)**:
```python
# Located in conversational_occasion.py → detect_kairos()
kairos = (
    0.45 <= v0_energy <= 0.70 and           # Condition 1: Energy in window
    satisfaction > prev_satisfaction and     # Condition 2: Satisfaction increasing
    abs(v0_energy - prev_energy) < 0.1 and  # Condition 3: Energy stable
    mean_coherence > 0.4                    # Condition 4: Coherence sufficient
)

# Kairos boost
if kairos_detected:
    emission_confidence *= 1.5  # 50% confidence boost
```

**Convergence Decision Tree**:
```
Cycle 1: V0=1.0 → organs process → V0 descends → check Kairos
Cycle 2: V0=0.6 → organs process → V0 descends → check Kairos
Cycle 3: V0=0.3 → organs process → V0 descends → check Kairos
  ↓
if ΔE < 0.1:
    → CONVERGED (satisfaction-driven)
elif kairos_detected:
    → CONVERGED (Kairos moment)
elif cycle >= max_cycles:
    → FORCED CONVERGENCE
else:
    → Continue to next cycle
```

---

## 🆕 Salience Model Parameters

**File**: `persona_layer/conversational_salience_model.py`

### Core Thresholds

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **field_resonance_threshold** | 0.6 | [0.5, 0.7] | float | Minimum coherence for pattern stabilization | Higher → stricter pattern formation |
| **morphogenetic_threshold** | 0.7 | [0.6, 0.8] | float | Threshold for morphogenetic pressure onset | Higher → slower boundary formation |
| **crystallization_threshold** | 0.85 | [0.8, 0.95] | float | Threshold for maximum morphogenetic pressure | Higher → stricter crystallization |

### Process Term Weights (Trauma-Aware Focus)

| Term | Weight | Range | Description |
|------|--------|-------|-------------|
| **signal_inflation** | 2.5 | [1.5, 3.0] | CRITICAL: Trauma response amplification (BOND/EO/NDAM) |
| **temporal_collapse** | 2.0 | [1.0, 2.5] | Past trauma bleeding into present |
| **safety_gradient** | 2.5 | [1.5, 3.0] | CRITICAL: How much truth can be felt safely |
| **field_resonance_threshold** | 1.5 | [1.0, 2.0] | Pattern stabilization (nexus formation) |
| **ethical_salience_field** | 1.5 | [1.0, 2.0] | What matters across conversation |
| **relational_recurrence** | 1.3 | [0.8, 1.8] | Healing spirals in conversation |
| **attunement_delta** | 1.0 | [0.5, 1.5] | Accuracy of organ sensing |
| **lure_hysteresis** | 0.8 | [0.5, 1.2] | Delay between feeling and moving |
| **salience_drift** | 0.7 | [0.3, 1.0] | Long-term deviation (less relevant single conv) |
| **concrescent_drift** | 0.6 | [0.3, 1.0] | Micro-misalignments (tracked by V0) |

### Domain Term Weights

| Term | Weight | Range | Description |
|------|--------|-------|-------------|
| **semantic_intensity** | 1.8 | [1.0, 2.5] | How meaningful/important (meta-atom activation) |
| **transformation_readiness** | 1.8 | [1.0, 2.5] | Capacity for change (V0 descent) |
| **satisfaction_proximity** | 1.5 | [1.0, 2.0] | Convergence closeness (Kairos) |
| **coherence_gradient** | 1.3 | [0.8, 1.8] | Direction toward coherence (organ agreement) |
| **relational_density** | 1.0 | [0.5, 1.5] | Connection richness (nexus count) |
| **emergence_potential** | 1.0 | [0.5, 1.5] | Novelty (new meta-atom combinations) |
| **spatial_coherence** | 0.5 | [0.3, 0.8] | Pattern consistency (less applicable to text) |
| **temporal_recurrence** | 0.8 | [0.5, 1.2] | Pattern repetition |
| **constraint_pressure** | 0.7 | [0.4, 1.0] | Boundary formation |
| **archetypal_resonance** | 0.6 | [0.3, 1.0] | Eternal forms (tracked by meta-atoms) |

**Profile Blend**:
```python
# Located in __init__() method
process_weight = 0.7  # 70% process philosophy terms
domain_weight = 0.3   # 30% domain terms

total_salience = process_salience * 0.7 + domain_salience * 0.3
```

**Trauma-Aware Emission Modulation**:
```python
# Located in emission_generator.py → generate_v0_guided_emissions()
if trauma_markers:
    signal_inflation = trauma_markers.get('signal_inflation', 0.0)
    temporal_collapse = trauma_markers.get('temporal_collapse', 0.0)
    safety_gradient = trauma_markers.get('safety_gradient', 1.0)

    # CRITICAL: High trauma → gentle intensity (override V0)
    if signal_inflation > 0.7 or temporal_collapse > 0.7 or safety_gradient < 0.4:
        intensity = 'low'  # Gentle, grounding phrases
        print("🛡️  TRAUMA DETECTED: Using gentle intensity")
```

**Morphogenetic Pressure Calculation**:
```python
# Located in calculate_morphogenetic_pressure() method
if total_salience < 0.6:
    return 0.0  # No pressure
elif total_salience < 0.7:
    return linear_interpolation(0.6, 0.7)  # 0.0 → 0.5
elif total_salience < 0.85:
    return linear_interpolation(0.7, 0.85)  # 0.5 → 1.0
else:
    return 1.0  # Maximum pressure (ready for crystallization)
```

---

## 🆕 Meta-Atom Parameters

**File**: `persona_layer/shared_meta_atoms.json` + organ cores

### Meta-Atom Definitions (10 Bridge Atoms)

| Meta-Atom | Organs | Category | Description |
|-----------|--------|----------|-------------|
| **trauma_aware** | BOND, EO, NDAM | Trauma-aware | Protective patterns, trauma responses |
| **safety_restoration** | EO, SANS, PRESENCE | Trauma-aware | Calming, grounding, co-regulation |
| **window_of_tolerance** | BOND, EO, RNX | Trauma-aware | Regulated state, optimal arousal |
| **compassion_safety** | EMPATHY, EO, SANS | Compassion | Validation + safety |
| **fierce_holding** | EMPATHY, AUTHENTICITY, BOND | Compassion | Boundaries with compassion |
| **relational_attunement** | LISTENING, EMPATHY, EO | Compassion | Connection, resonance |
| **temporal_grounding** | RNX, PRESENCE, CARD | Temporal | Present-moment awareness |
| **kairos_emergence** | RNX, WISDOM, AUTHENTICITY | Temporal | Opportune moment, threshold |
| **coherence_integration** | SANS, WISDOM, CARD | Integration | Making sense, complexity |
| **somatic_wisdom** | PRESENCE, BOND, EO | Integration | Embodied knowing |

### Activation Thresholds

**File**: `persona_layer/nexus_intersection_composer.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **intersection_threshold** | 0.05 | [0.03, 0.10] | float | 🆕 LOWERED for meta-atoms! Minimum activation for nexus participation | Lower → more nexuses form, may be noisy |
| **meta_atom_direct_threshold** | 0.30 | [0.20, 0.50] | float | 🆕 Direct emission threshold for meta-atoms (vs 0.65 for regular atoms) | Lower → easier meta-atom emission |
| **meta_atom_fusion_threshold** | 0.20 | [0.15, 0.35] | float | 🆕 Fusion threshold for meta-atoms (vs 0.50 for regular) | Lower → easier meta-atom fusion |
| **meta_atom_confidence_boost** | 1.2 | [1.0, 1.5] | float | Confidence multiplier for meta-atom emissions | Higher → favors meta-atom phrases |

**Activation Logic**:
```python
# Located in organ cores → _activate_meta_atoms() method
# Example: BOND activates trauma_aware
if meta_atom == 'trauma_aware':
    if firefighter_patterns > 0.6 or exile_patterns > 0.6:
        activation = max(firefighter_patterns, exile_patterns)
        activation *= coherence  # Organ confidence
        activation *= (0.5 + 0.5 * lure)  # Appetition modulation
        meta_activations['trauma_aware'] = min(1.0, activation)
```

**Meta-Atom Phrase Library**:
```python
# File: persona_layer/meta_atom_phrase_library.json
# 130 trauma-informed phrases across 10 meta-atoms × 3 intensities
{
  "trauma_aware": {
    "high": ["I'm noticing protective patterns activating strongly", ...],
    "medium": ["I'm noticing some protective patterns", ...],
    "low": ["I notice a protective quality", ...]
  },
  # ... 9 more meta-atoms
}
```

---

## 🎨 Emission Generation Parameters

**File**: `persona_layer/emission_generator.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **direct_threshold** | 0.65 | [0.5, 0.9] | float | Minimum emission readiness for DIRECT EMISSION path (≥3 organs, strong agreement) | Higher → fewer but more confident direct emissions |
| **fusion_threshold** | 0.50 | [0.3, 0.7] | float | Minimum emission readiness for ORGAN FUSION path (≥2 organs, moderate agreement) | Higher → more selective fusion emissions |
| **hebbian_fallback_threshold** | 0.0 | [0.0, 0.5] | float | Hebbian memory is used when emission readiness < fusion_threshold | Higher → stricter before using learned phrases |
| **max_emission_length** | 150 | [50, 300] | int | Maximum character length for single emission phrase | Higher → longer, more detailed emissions |
| **min_nexus_count** | 1 | [1, 5] | int | Minimum number of nexuses required for emission generation | Higher → more selective emission (needs more organ agreement) |
| **variety_bonus** | 0.1 | [0.0, 0.3] | float | Confidence boost for diverse emission strategies (when `prefer_variety=True`) | Higher → favors diverse emission paths |

**Compositional Strategy Weighting**:
```python
# Located in _select_emission_strategy() method
strategy_weights = {
    'direct': 1.0,      # DIRECT EMISSION (strong organ agreement)
    'fusion': 0.85,     # ORGAN FUSION (moderate agreement)
    'hebbian': 0.70     # HEBBIAN FALLBACK (learned phrases)
}
```

**Path Selection Decision Tree**:
```
if emission_readiness ≥ direct_threshold AND participants ≥ 3:
    → DIRECT EMISSION (highest confidence 0.7-1.0)
elif emission_readiness ≥ fusion_threshold AND participants ≥ 2:
    → ORGAN FUSION (medium confidence 0.5-0.7)
else:
    → HEBBIAN FALLBACK (use learned phrases, confidence 0.4-0.6)
```

---

## 🧬 Semantic Field Extraction Parameters

**File**: `persona_layer/semantic_field_extractor.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **semantic_atoms_path** | `persona_layer/semantic_atoms.json` | - | str | Path to 550-atom semantic database (50×11 organs) | - |
| **lure_weight_min** | 0.5 | [0.0, 0.8] | float | Minimum lure weighting (when lure=0.0) | Higher → stronger baseline activation |
| **lure_weight_max** | 1.0 | [0.8, 1.5] | float | Maximum lure weighting (when lure=1.0) | Higher → stronger appetite-driven activation |
| **coherence_weight** | 1.0 | [0.5, 1.5] | float | Organ coherence multiplier for atom activation | Higher → more selective (favors confident organs) |
| **pattern_strength_weight** | 1.0 | [0.5, 1.5] | float | Pattern strength multiplier for atom activation | Higher → emphasizes pattern detection quality |

**Keyword Matching Strategy**:
```python
# Located in _match_keywords_to_atoms() method
EXACT_MATCH_SIMILARITY = 1.0       # keyword == atom
SUBSTRING_MATCH_SIMILARITY = 0.8   # keyword in atom or atom in keyword
PARTIAL_MATCH_SIMILARITY = 0.5     # shared 3+ characters
MIN_SHARED_CHARS = 3               # Minimum overlap for partial match
```

**Lure Weighting Formula**:
```python
# Located in _extract_organ_field() method (line 272)
lure_weight = 0.5 + 0.5 * lure  # Range: [0.5, 1.0]
activation = base_activation * lure_weight
```

---

## 🌀 Nexus Intersection Composition Parameters

**File**: `persona_layer/nexus_intersection_composer.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **r_matrix_path** | `persona_layer/conversational_hebbian_memory.json` | - | str | Path to 11×11 Hebbian R-matrix (organ coupling) | - |
| **intersection_threshold** | 0.3 | [0.2, 0.5] | float | Minimum atom activation for organ participation in nexus | Higher → stricter nexus formation (fewer nexuses, stronger agreement) |
| **coherence_threshold** | 0.4 | [0.3, 0.6] | float | Gate 2: Minimum coherence (agreement) among organs | Higher → requires tighter organ consensus |
| **satisfaction_window_min** | 0.45 | [0.3, 0.6] | float | Gate 3: Lower bound of Kairos satisfaction window | - |
| **satisfaction_window_max** | 0.70 | [0.6, 0.9] | float | Gate 3: Upper bound of Kairos satisfaction window | - |
| **min_emission_readiness** | 0.5 | [0.3, 0.7] | float | Gate 4: Minimum emission readiness (ΔC) to pass all gates | Higher → more selective emission candidates |

**Emission Readiness Formula (ΔC)**:
```python
# Located in compose_nexuses() method (lines 248-253)
# From FFITTSS 4-gate architecture (DAE 3.0 validated)
alpha = 0.47  # Coherence weight
beta = 0.35   # Intersection strength weight
gamma = 0.11  # Field strength weight
delta = 0.07  # R-matrix coupling weight

emission_readiness = (
    alpha * coherence +
    beta * intersection_strength +
    gamma * field_strength +
    delta * r_matrix_weight
)
```

**4-Gate Filtering Architecture**:
```python
# Gate 1: Intersection (≥2 organs activate same atom, τ_I = 1.5)
if len(participants) < 2:
    continue  # Reject

# Gate 2: Coherence (agreement threshold, τ_C = 0.4)
if coherence < 0.4:
    continue  # Reject

# Gate 3: Satisfaction (Kairos window, S ∈ [0.45, 0.70])
if not (0.45 <= field_strength <= 0.70):
    continue  # Reject

# Gate 4: Felt Energy (emission readiness, ΔC ≥ 0.5)
if emission_readiness < 0.5:
    continue  # Reject

# PASS: Nexus is ready for emission
```

**R-Matrix Coupling Computation**:
```python
# Located in compose_nexuses() method (lines 220-245)
# Pairwise organ coupling × activations
for organ1, organ2 in participant_pairs:
    coupling = R_matrix[organ1, organ2]  # Hebbian learned coupling
    activation_product = activations[organ1] * activations[organ2]
    r_matrix_sum += coupling * activation_product

r_matrix_weight = r_matrix_sum / pair_count  # Normalize
```

---

## 🎧 Conversational Organ Parameters

**File**: `organs/modular/{organ}/core/{organ}_core.py` (5 organs)

### **LISTENING**
| Parameter | Default | Range | Type | Description |
|-----------|---------|-------|------|-------------|
| **pattern_count** | 50 | [30, 100] | int | Number of listening patterns (acknowledgment, exploration, etc.) |
| **coherence_threshold** | 0.6 | [0.4, 0.8] | float | Minimum coherence for pattern detection |
| **lure_decay** | 0.1 | [0.05, 0.2] | float | Appetition decay rate when patterns not detected |

### **EMPATHY**
| Parameter | Default | Range | Type | Description |
|-----------|---------|-------|------|-------------|
| **pattern_count** | 50 | [30, 100] | int | Number of empathy patterns (feeling, somatic, etc.) |
| **coherence_threshold** | 0.6 | [0.4, 0.8] | float | Minimum coherence for pattern detection |
| **body_emphasis** | 1.2 | [1.0, 1.5] | float | Weighting for somatic/body-related patterns |

### **WISDOM**
| Parameter | Default | Range | Type | Description |
|-----------|---------|-------|------|-------------|
| **pattern_count** | 50 | [30, 100] | int | Number of wisdom patterns (pattern recognition, context) |
| **coherence_threshold** | 0.6 | [0.4, 0.8] | float | Minimum coherence for pattern detection |
| **meta_level_boost** | 1.3 | [1.0, 1.6] | float | Weighting for meta-cognitive patterns |

### **AUTHENTICITY**
| Parameter | Default | Range | Type | Description |
|-----------|---------|-------|------|-------------|
| **pattern_count** | 50 | [30, 100] | int | Number of authenticity patterns (congruence, truth) |
| **coherence_threshold** | 0.6 | [0.4, 0.8] | float | Minimum coherence for pattern detection |
| **vulnerability_bonus** | 1.4 | [1.0, 1.7] | float | Weighting for vulnerability expressions |

### **PRESENCE**
| Parameter | Default | Range | Type | Description |
|-----------|---------|-------|------|-------------|
| **pattern_count** | 50 | [30, 100] | int | Number of presence patterns (grounding, nowness) |
| **coherence_threshold** | 0.6 | [0.4, 0.8] | float | Minimum coherence for pattern detection |
| **temporal_proximity_weight** | 1.3 | [1.0, 1.6] | float | Weighting for "right now" language |

---

## 🩹 Trauma/Context Organ Parameters

### **BOND (IFS Trauma/SELF-Energy Detection)**
**File**: `organs/modular/bond/core/bond_text_core.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **manager_keywords** | 33 | - | int | Keywords for manager parts (control, plan, organize) | - |
| **firefighter_keywords** | 32 | - | int | Keywords for firefighter parts (escape, numb, distract) | - |
| **exile_keywords** | 31 | - | int | Keywords for exile parts (worthless, abandoned, rejected) | - |
| **self_keywords** | 35 | - | int | Keywords for SELF-energy (calm, curious, compassionate) | - |
| **self_distance_threshold** | 0.5 | [0.3, 0.7] | float | Threshold for trauma detection (higher = more trauma) | Higher → more sensitive trauma detection |
| **parts_blend_threshold** | 0.6 | [0.4, 0.8] | float | Threshold for part blending detection | Higher → stricter blending detection |

**SELF-Distance Formula**:
```python
# Located in process() method
parts_score = (managers + firefighters + exiles) / total_keywords
self_energy_score = self_energy / total_keywords
self_distance = parts_score / (self_energy_score + 1e-6)
```

### **SANS (Semantic Coherence Tracking)**
**File**: `organs/modular/sans/core/sans_text_core.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **similarity_threshold** | 0.7 | [0.5, 0.9] | float | Minimum semantic similarity for coherence detection | Higher → stricter coherence (detects only very similar sentences) |
| **embedding_dim** | 384 | [256, 768] | int | Sentence embedding dimensionality (all-MiniLM-L6-v2) | - |
| **coherence_window** | 3 | [2, 5] | int | Number of sentences for rolling coherence check | Higher → slower response to coherence shifts |

**Coherence Calculation**:
```python
# Located in _compute_semantic_similarity() method
embeddings = model.encode(sentences)  # all-MiniLM-L6-v2
embeddings_norm = embeddings / ||embeddings||  # L2 normalization
similarity = embeddings_norm @ embeddings_norm.T  # Cosine similarity matrix
coherence = mean(similarity > threshold)
```

### **NDAM (Urgency/Crisis Detection)**
**File**: `organs/modular/ndam/core/ndam_text_core.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **urgency_threshold** | 0.75 | [0.5, 0.9] | float | Minimum urgency score for crisis detection | Higher → only detects severe crisis |
| **urgency_keywords** | 45 | - | int | Keywords for urgency detection (crisis, urgent, emergency, now) | - |
| **escalation_window** | 5 | [3, 10] | int | Number of sentences for urgency escalation detection | Higher → slower escalation response |
| **crisis_amplification** | 1.5 | [1.2, 2.0] | float | Multiplier for crisis-related keywords | Higher → more sensitive to crisis language |

**Urgency Score Formula**:
```python
# Located in process() method
urgency_keywords_detected = count(keywords in text)
urgency_score = (urgency_keywords_detected / total_keywords) * crisis_amplification
```

### **RNX (Temporal Pattern Detection)**
**File**: `organs/modular/rnx/core/rnx_text_core.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **temporal_keywords** | 50 | - | int | Keywords for temporal markers (before, after, when, timeline) | - |
| **rhythm_detection_window** | 3 | [2, 5] | int | Sentences for rhythm pattern detection | Higher → requires longer temporal pattern |
| **sequence_bonus** | 1.3 | [1.0, 1.6] | float | Weighting for sequence detection (first, then, next) | Higher → emphasizes sequential patterns |

### **EO (Polyvagal State Detection)**
**File**: `organs/modular/eo/core/eo_text_core.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **safe_keywords** | 50 | - | int | Keywords for ventral vagal (safe, connection, calm) | - |
| **threat_keywords** | 50 | - | int | Keywords for sympathetic (threat, anxiety, panic) | - |
| **shutdown_keywords** | 50 | - | int | Keywords for dorsal vagal (shutdown, numb, freeze) | - |
| **state_transition_threshold** | 0.3 | [0.2, 0.5] | float | Threshold for polyvagal state shift detection | Higher → requires stronger state shift |

**Polyvagal State Formula**:
```python
# Located in process() method
safe_score = count(safe_keywords) / total_keywords
threat_score = count(threat_keywords) / total_keywords
shutdown_score = count(shutdown_keywords) / total_keywords

dominant_state = argmax([safe_score, threat_score, shutdown_score])
```

### **CARD (Response Scaling)**
**File**: `organs/modular/card/core/card_text_core.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **brief_threshold** | 0.3 | [0.2, 0.4] | float | Threshold for recommending brief response | - |
| **detailed_threshold** | 0.7 | [0.6, 0.8] | float | Threshold for recommending detailed response | - |
| **context_window** | 100 | [50, 200] | int | Characters considered for complexity assessment | Higher → considers more context for scaling |

**Recommended Scale Formula**:
```python
# Located in process() method
if complexity < brief_threshold:
    recommended_scale = 'brief'  # 1-2 sentences
elif complexity < detailed_threshold:
    recommended_scale = 'moderate'  # 2-4 sentences
else:
    recommended_scale = 'detailed'  # 4+ sentences
```

---

## 🧠 Hebbian Learning Parameters

**File**: `persona_layer/conversational_hebbian_memory.py` (manages learning)

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **learning_rate** | 0.1 | [0.05, 0.3] | float | Hebbian weight update rate (Δw = η * x₁ * x₂) | Higher → faster learning, less stable |
| **decay_rate** | 0.01 | [0.0, 0.05] | float | Coupling decay rate (prevents runaway strengthening) | Higher → faster forgetting |
| **min_confidence** | 0.5 | [0.3, 0.7] | float | Minimum confidence for pattern storage | Higher → only stores high-confidence patterns |
| **max_patterns** | 10000 | [1000, 50000] | int | Maximum patterns in memory (LRU eviction) | Higher → more memory, slower lookup |
| **r_matrix_size** | 11×11 | - | int | Organ coupling matrix (11 organs) | Fixed (architecture constraint) |

**Hebbian Update Rule**:
```python
# Located in update_r_matrix() method
# Hebbian plasticity: "Neurons that fire together, wire together"
for organ1 in range(11):
    for organ2 in range(11):
        if organ1 != organ2:
            activation1 = organ_activations[organ1]
            activation2 = organ_activations[organ2]

            # Hebbian update
            delta_w = learning_rate * activation1 * activation2

            # Apply update with decay
            R_matrix[organ1, organ2] += delta_w
            R_matrix[organ1, organ2] *= (1 - decay_rate)

            # Symmetry (R-matrix is symmetric)
            R_matrix[organ2, organ1] = R_matrix[organ1, organ2]
```

**Storage Format** (`conversational_hebbian_memory.json`):
```json
{
  "r_matrix": [[11×11 float matrix]],
  "patterns": [
    {
      "input_text": "...",
      "output_text": "...",
      "confidence": 0.85,
      "timestamp": "2025-11-11T...",
      "organ_activations": [11-element array]
    }
  ],
  "total_updates": 1234,
  "last_updated": "2025-11-11T..."
}
```

---

## 🌱 Phase 5 Organic Learning Parameters

**File**: `persona_layer/phase5_organic_learning.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **storage_dir** | `persona_layer/` | - | str | Directory for learning databases | - |
| **similarity_threshold** | 0.75 | [0.6, 0.9] | float | Cosine similarity threshold for family membership | Higher → stricter family grouping (more specific families) |
| **family_maturity_count** | 3 | [2, 5] | int | Minimum conversations for family maturation | Higher → slower maturation, more stable families |
| **organ_signature_dim** | 57 | - | int | Signature dimensionality (11 organs × 5 metrics + 2 global) | Fixed (architecture constraint) |
| **cluster_update_rate** | 1.0 | [0.5, 1.5] | float | Cluster centroid update rate | Higher → faster adaptation to new data |

**Organ Signature Components** (57D vector):
```python
# Located in _extract_organ_signature() method
signature = [
    # Per-organ metrics (11 organs × 5 = 55 dimensions)
    listening_coherence,    # LISTENING
    listening_lure,
    listening_pattern_count,
    listening_satisfaction,
    listening_field_strength,

    empathy_coherence,      # EMPATHY
    empathy_lure,
    ... (repeat for all 11 organs) ...

    card_field_strength,    # CARD

    # Global metrics (2 dimensions)
    mean_coherence,         # Overall organism coherence
    polyvagal_state_encoded # EO polyvagal state (0=safe, 1=threat, 2=shutdown)
]
```

**Family Formation**:
```python
# Located in record_conversation() method
for existing_family in families:
    centroid = existing_family['centroid']  # 57D average signature
    similarity = cosine_similarity(organ_signature, centroid)

    if similarity >= similarity_threshold:
        # Join existing family
        existing_family['conversations'].append(conversation_id)
        existing_family['centroid'] = update_centroid(centroid, organ_signature, cluster_update_rate)

        if len(existing_family['conversations']) >= family_maturity_count:
            existing_family['mature'] = True

        return

# No match found → create new family
new_family = {
    'family_id': generate_id(),
    'centroid': organ_signature,
    'conversations': [conversation_id],
    'mature': False,
    'created_at': timestamp
}
families.append(new_family)
```

**Storage Format** (`organic_families.json`):
```json
{
  "families": [
    {
      "family_id": "family_001",
      "centroid": [57-element float array],
      "conversations": ["conv_001", "conv_002", "conv_003"],
      "mature": true,
      "created_at": "2025-11-10T...",
      "characteristic_features": {
        "dominant_organs": ["EMPATHY", "LISTENING", "BOND"],
        "polyvagal_tendency": "safe",
        "mean_coherence": 0.78
      }
    }
  ],
  "total_families": 12,
  "mature_families": 7,
  "last_updated": "2025-11-11T..."
}
```

---

## 🌐 Global Organism Parameters

**File**: `persona_layer/conversational_organism_wrapper.py`

| Parameter | Default | Range | Type | Description | Impact |
|-----------|---------|-------|------|-------------|--------|
| **emission_enabled** | True | - | bool | Enable/disable emission generation | - |
| **learning_enabled** | True | - | bool | Enable/disable Hebbian + Phase5 learning | - |
| **min_text_length** | 10 | [5, 50] | int | Minimum characters for processing | Lower → process shorter inputs |
| **max_text_length** | 10000 | [1000, 50000] | int | Maximum characters for processing (truncate beyond) | Higher → process longer texts |
| **organ_timeout** | 10.0 | [5.0, 30.0] | float | Timeout (seconds) for individual organ processing | Higher → allow slower organs, risk timeout |

**Processing Flow Control**:
```python
# Located in process_text() method

# Stage 1: Text preprocessing
if len(text) < min_text_length:
    return empty_result
if len(text) > max_text_length:
    text = text[:max_text_length]

# Stage 2: Organ processing (11 organs)
organ_results = {}
for organ_name, organ in organs.items():
    try:
        result = organ.process(text, timeout=organ_timeout)
        organ_results[organ_name] = result
    except TimeoutError:
        organ_results[organ_name] = default_result

# Stage 3: Emission generation (if enabled)
if emission_enabled:
    semantic_fields = extract_fields(organ_results)
    nexuses = compose_nexuses(semantic_fields)
    emission = generate_emission(nexuses)

# Stage 4: Learning (if enabled)
if learning_enabled:
    update_hebbian_memory(organ_results, emission)
    record_organic_family(organ_signature)

return {
    'organ_results': organ_results,
    'emission_text': emission,
    'emission_confidence': emission_confidence,
    'felt_states': felt_states
}
```

---

## 🎛️ Tuning Recommendations

### **Scenario 1: High-Confidence, Low-Diversity Emissions**

**Symptoms**:
- Only DIRECT EMISSION path used
- Few nexuses forming (< 3 per input)
- Emission text repetitive

**Adjustments**:
```python
# Increase emission variety
direct_threshold = 0.75  # (default: 0.65) → stricter direct path
variety_bonus = 0.15     # (default: 0.10) → reward diverse strategies

# Lower nexus formation barriers
intersection_threshold = 0.25  # (default: 0.30) → easier nexus formation
coherence_threshold = 0.35     # (default: 0.40) → tolerate more organ disagreement
```

**Expected Outcome**: More diverse emission paths (fusion + hebbian), 5-8 nexuses per input

---

### **Scenario 2: Low-Confidence, High-Diversity Emissions**

**Symptoms**:
- Mostly HEBBIAN FALLBACK path used
- Many nexuses forming (> 10 per input)
- Emission confidence < 0.5

**Adjustments**:
```python
# Increase emission selectivity
direct_threshold = 0.60  # (default: 0.65) → easier direct path access
fusion_threshold = 0.45  # (default: 0.50) → easier fusion path access

# Raise nexus quality standards
intersection_threshold = 0.35  # (default: 0.30) → stricter nexus formation
coherence_threshold = 0.45     # (default: 0.40) → require tighter organ agreement
min_emission_readiness = 0.55  # (default: 0.50) → higher ΔC threshold
```

**Expected Outcome**: Fewer but higher-confidence nexuses (3-5 per input), direct/fusion paths preferred

---

### **Scenario 3: Trauma-Insensitive Responses**

**Symptoms**:
- BOND not activating atoms despite trauma language
- Emission doesn't reflect SELF-distance
- System responds to exiled parts without caution

**Adjustments**:
```python
# Increase BOND sensitivity
self_distance_threshold = 0.4  # (default: 0.5) → detect trauma earlier

# Weight BOND more heavily in nexus composition
# Modify R-matrix manually or via training:
R_matrix[BOND, EMPATHY] = 0.9   # Strengthen BOND-EMPATHY coupling
R_matrix[BOND, LISTENING] = 0.85  # Strengthen BOND-LISTENING coupling

# Reduce emission when BOND detects high trauma
# (Requires custom logic in emission_generator.py)
if self_distance > 0.7:
    emission_readiness *= 0.7  # Reduce emission confidence by 30%
```

**Expected Outcome**: More cautious emissions when trauma detected, BOND atoms prominent in nexuses

---

### **Scenario 4: Slow Organism Response Time**

**Symptoms**:
- Processing takes > 5 seconds per input
- Organ timeouts occurring
- Emission generation delayed

**Adjustments**:
```python
# Speed optimizations
organ_timeout = 5.0           # (default: 10.0) → faster organ timeout
max_text_length = 5000        # (default: 10000) → process shorter texts
coherence_window = 2          # (default: 3) → SANS faster coherence check
embedding_dim = 256           # (default: 384) → SANS faster embedding (if using smaller model)

# Reduce emission complexity
max_emission_length = 100     # (default: 150) → shorter emissions
min_nexus_count = 2           # (default: 1) → skip emission if < 2 nexuses
```

**Expected Outcome**: < 3 second processing time per input, faster emission generation

---

### **Scenario 5: Over-Sensitive Crisis Detection**

**Symptoms**:
- NDAM always detecting high urgency (> 0.8)
- System overreacts to mild stress language
- False positives on crisis detection

**Adjustments**:
```python
# Reduce NDAM sensitivity
urgency_threshold = 0.85       # (default: 0.75) → stricter crisis detection
crisis_amplification = 1.2     # (default: 1.5) → reduce keyword amplification
escalation_window = 7          # (default: 5) → slower escalation response

# Adjust semantic atoms
# Remove or reduce weight of mild urgency atoms:
# Edit persona_layer/semantic_atoms.json → NDAM section
# Reduce activation for: 'stressed', 'worried', 'concerned'
# Keep high activation for: 'crisis', 'emergency', 'urgent'
```

**Expected Outcome**: NDAM urgency scores 0.3-0.6 for typical stress, > 0.8 only for true crisis

---

### **Scenario 6: Hebbian Memory Not Learning**

**Symptoms**:
- R-matrix stays at identity (all 1.0 on diagonal, 0.0 off-diagonal)
- No pattern accumulation in Hebbian memory
- Emission doesn't improve with training

**Adjustments**:
```python
# Increase Hebbian learning rate
learning_rate = 0.15           # (default: 0.10) → faster weight updates
decay_rate = 0.005             # (default: 0.01) → slower forgetting
min_confidence = 0.4           # (default: 0.5) → store more patterns

# Ensure learning is triggered
# Check that OUTPUT satisfaction ≥ 0.45 in training pairs
# Verify conversational_hebbian_memory.json is writable
```

**Expected Outcome**: R-matrix develops structure (off-diagonal elements > 0.2), pattern database grows

---

### **Scenario 7: Phase 5 Families Not Maturing**

**Symptoms**:
- Many families created (> 20) but none mature
- Families have 1-2 conversations each
- Centroid cosine similarity always < threshold

**Adjustments**:
```python
# Lower similarity threshold
similarity_threshold = 0.65    # (default: 0.75) → easier family joining
family_maturity_count = 2      # (default: 3) → faster maturation
cluster_update_rate = 1.2      # (default: 1.0) → centroids adapt faster

# Check organ signature variance
# If all signatures very similar (low variance):
#   → Add noise to signatures during development
# If all signatures very different (high variance):
#   → Normalize organ metrics before signature extraction
```

**Expected Outcome**: 5-10 families after 20 conversations, 3-5 mature families

---

## 📊 Parameter Validation Checklist

Before deploying tuned parameters to production:

### **Emission Quality Checks**
- [ ] Emission confidence mean > 0.5 (across 100 test inputs)
- [ ] Emission path distribution: 40% direct, 40% fusion, 20% hebbian
- [ ] Nexus count: 3-7 per input (median)
- [ ] Emission text length: 80-150 characters (median)
- [ ] No empty emissions (emission_text != None) on valid inputs

### **Organ Health Checks**
- [ ] All 11 organs activate (coherence > 0.0) on rich conversational input
- [ ] BOND self-distance: 0.3-0.6 on typical conversations, > 0.7 on trauma narratives
- [ ] SANS coherence: > 0.7 on coherent text, < 0.5 on fragmented text
- [ ] NDAM urgency: < 0.5 on calm text, > 0.8 on crisis language
- [ ] EO polyvagal state: correct detection (safe/threat/shutdown)

### **Learning System Checks**
- [ ] R-matrix updates: off-diagonal elements grow from 0.0 → 0.2-0.5 after 50 training pairs
- [ ] Hebbian patterns: > 100 stored patterns after 50 training pairs
- [ ] Phase 5 families: 5-10 families after 20 conversations, 3+ mature
- [ ] Cluster centroids: stable (cosine similarity > 0.9 between epochs)

### **Performance Checks**
- [ ] Processing time: < 3 seconds per input (median)
- [ ] Memory usage: < 500MB organism process (stable)
- [ ] No organ timeouts (< 1% timeout rate)
- [ ] Emission generation: < 500ms (after organ processing)

---

## 🔧 Advanced Tuning: Custom Logic Examples

### **Example 1: Trauma-Modulated Emission Confidence**

**Goal**: Reduce emission confidence when BOND detects high trauma (self-distance > 0.7)

**File to Edit**: `persona_layer/emission_generator.py` → `generate_emissions()` method

```python
# After line 289: emitted_phrases = ...

# Apply trauma modulation
if self.trauma_modulation_enabled:
    for phrase in emitted_phrases:
        # Get BOND self-distance from nexus participants
        bond_self_distance = get_bond_self_distance_from_nexus(phrase.nexus)

        if bond_self_distance > 0.7:
            # High trauma detected → reduce confidence
            trauma_penalty = 0.7  # 30% confidence reduction
            phrase.confidence *= trauma_penalty
            phrase.metadata['trauma_modulated'] = True
            phrase.metadata['original_confidence'] = phrase.confidence / trauma_penalty
```

**Result**: Emissions with high trauma context have lower confidence (0.4-0.6 instead of 0.7-0.9)

---

### **Example 2: Polyvagal-Gated Emission**

**Goal**: Skip emission entirely when EO detects shutdown state (dorsal vagal)

**File to Edit**: `persona_layer/conversational_organism_wrapper.py` → `process_text()` method

```python
# After line 246: if self.semantic_extractor and ...

# Check polyvagal state before emission
eo_result = organ_results.get('EO')
if eo_result and hasattr(eo_result, 'polyvagal_state'):
    polyvagal_state = eo_result.polyvagal_state

    if polyvagal_state == 'shutdown':
        # Dorsal vagal shutdown detected → skip emission (respect the freeze)
        print("   ⚠️  Polyvagal shutdown detected, skipping emission (respecting freeze response)")
        emission_text = None
        emission_confidence = 0.0
        emission_path = 'polyvagal_gated'
        emission_nexus_count = 0
    else:
        # Safe to emit
        semantic_fields = self.semantic_extractor.extract_fields(organ_results)
        nexuses = self.nexus_composer.compose_nexuses(semantic_fields)
        # ... (rest of emission logic) ...
```

**Result**: System respects polyvagal shutdown (no emission when user is in freeze/collapse)

---

### **Example 3: Urgency-Prioritized Nexus Selection**

**Goal**: When NDAM detects high urgency (> 0.8), prioritize nexuses with urgency atoms

**File to Edit**: `persona_layer/nexus_intersection_composer.py` → `get_top_nexuses()` method

```python
# After line 325: if apply_gates: ...

# Check if NDAM detected urgency
ndam_urgency = get_ndam_urgency_from_fields(semantic_fields)

if ndam_urgency > 0.8:
    # High urgency → prioritize urgency-related nexuses
    urgency_atoms = load_urgency_atoms()  # From semantic_atoms.json → NDAM section

    for nexus in nexuses:
        if nexus.atom in urgency_atoms:
            # Boost emission readiness for urgency nexuses
            nexus.emission_readiness *= 1.5
            nexus.metadata['urgency_boosted'] = True

    # Re-sort by boosted emission readiness
    nexuses.sort(key=lambda n: n.emission_readiness, reverse=True)
```

**Result**: Crisis-related nexuses appear first, emission addresses urgency

---

## 📈 Performance Profiling Commands

### **Measure Processing Time**
```bash
cd "/Users/daedalea/Desktop/DAE_HYPHAE_1"
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

python3 -m cProfile -o profile.stats -s cumtime persona_layer/conversational_organism_wrapper.py

# Analyze results
python3 -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumtime').print_stats(20)"
```

### **Monitor Emission Quality Over Time**
```bash
# Collect emission metrics from 100 test inputs
python3 persona_layer/epoch_training/analyze_emission_quality.py --num_samples 100

# Expected output:
# Emission confidence: 0.63 ± 0.15 (mean ± std)
# Nexus count: 5.2 ± 2.1
# Emission path distribution: direct=42%, fusion=38%, hebbian=20%
# Processing time: 2.3s ± 0.8s
```

### **Validate Hebbian Learning**
```bash
# Snapshot R-matrix before training
cp persona_layer/conversational_hebbian_memory.json snapshot_before.json

# Run training (50 pairs)
python3 persona_layer/epoch_training/test_integrated_training.py --num_pairs 50

# Snapshot R-matrix after training
cp persona_layer/conversational_hebbian_memory.json snapshot_after.json

# Compare matrices
python3 -c "
import json
import numpy as np

with open('snapshot_before.json') as f:
    before = np.array(json.load(f)['r_matrix'])

with open('snapshot_after.json') as f:
    after = np.array(json.load(f)['r_matrix'])

delta = after - before
print(f'R-matrix change (Frobenius norm): {np.linalg.norm(delta):.4f}')
print(f'Max weight increase: {delta.max():.4f}')
print(f'Mean off-diagonal weight: {after[np.triu_indices(11, k=1)].mean():.4f}')
"
```

---

## 🎯 Quick Start: Recommended Production Settings

**Balanced Configuration** (good for most use cases):

```python
# Emission Generation
direct_threshold = 0.65
fusion_threshold = 0.50
hebbian_fallback_threshold = 0.0

# Semantic Field Extraction
lure_weight_min = 0.5
lure_weight_max = 1.0
coherence_weight = 1.0

# Nexus Intersection Composition
intersection_threshold = 0.3
coherence_threshold = 0.4
satisfaction_window = (0.45, 0.70)
min_emission_readiness = 0.5

# Hebbian Learning
learning_rate = 0.1
decay_rate = 0.01
min_confidence = 0.5

# Phase 5 Organic Learning
similarity_threshold = 0.75
family_maturity_count = 3
cluster_update_rate = 1.0

# Trauma Sensitivity
self_distance_threshold = 0.5  # BOND
urgency_threshold = 0.75       # NDAM
```

**Test this configuration** with your specific use case and adjust as needed using the tuning recommendations above.

---

## 📝 Summary

This comprehensive parameter table documents **all tunable parameters** across the DAE_HYPHAE_1 system:

- **Emission Generation**: 6 parameters (confidence thresholds, strategy selection)
- **Semantic Field Extraction**: 5 parameters (keyword matching, lure weighting)
- **Nexus Intersection Composition**: 6 parameters (4-gate thresholds, ΔC formula)
- **Conversational Organs**: 5 organs × 3 parameters each = 15 parameters
- **Trauma/Context Organs**: 6 organs × 4 parameters each = 24 parameters
- **Hebbian Learning**: 5 parameters (learning rate, decay, storage)
- **Phase 5 Organic Learning**: 5 parameters (similarity, maturation, clustering)
- **Global Organism**: 5 parameters (timeouts, text limits, feature flags)

**Total: 71 tunable parameters** + advanced custom logic examples

Use this document as a reference for:
1. Understanding system behavior
2. Tuning for specific use cases (trauma sensitivity, performance, emission quality)
3. Validating production configurations
4. Debugging unexpected behavior

---

🌀 **"Tune with care. Each parameter shapes how the organism feels, learns, and responds."** 🌀

---

**Last Updated**: November 11, 2025
**System Version**: DAE_HYPHAE_1 Phase 2 (11-Organ + Emission + Learning)
**Status**: Production-Ready Configuration Documented
