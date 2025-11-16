# TSK Spinal Cord Architecture

## Overview

The Transductive Summary Kernel (TSK) serves as the "spinal cord" of DAE's learning pipeline - the central conduit through which all felt-state transformations flow, enabling fractal reward learning from transformation patterns rather than static snapshots.

## Core Philosophy

**Whiteheadian Process**: Each conversation is an "actual occasion" with:
- **Initial Prehension**: User input creates felt-state before processing
- **Concrescence**: Multi-cycle V0 convergence through 12 organs
- **Satisfaction**: Final felt-state after emission (Kairos moment)
- **Transformation**: INITIAL → FINAL state change encoded in 57D signature

**DAE 3.0 Validated Approach**: 47.3% ARC-AGI from transformation-based clustering, not input categorization.

---

## Organ Participation Matrix

### Active Organs (9/12) - Fully Contributing

| Organ | Purpose | Key Attributes | TSK Contribution |
|-------|---------|----------------|------------------|
| **LISTENING** | Temporal inquiry, exploration | coherence, lure | Meta-atoms, coherence shift |
| **PRESENCE** | Grounded awareness | coherence, lure | Somatic wisdom, temporal grounding |
| **BOND** | IFS parts detection | mean_self_distance, parts_polarization | Zone computation (1-5) |
| **SANS** | Semantic coherence | coherence, readiness | Safety restoration signal |
| **NDAM** | Crisis/urgency detection | mean_urgency, escalation_detected | Urgency dimension |
| **RNX** | Temporal dynamics | temporal_state, pattern_strength | Convergence patterns |
| **EO** | Polyvagal state | polyvagal_state, state_confidence | Ventral/sympathetic/dorsal |
| **CARD** | Response scaling | detail_level, length_scale | Emission stance |
| **NEXUS** | Entity memory | coherence, lure | Relational context |

### Inactive Organs (3/12) - Architectural Gap

| Organ | Design Purpose | Gap Analysis |
|-------|----------------|--------------|
| **EMPATHY** | Detect empathic SPEECH patterns | Only triggers on empathic responses, not user needs |
| **WISDOM** | Detect wisdom SPEECH patterns | Only triggers on wise responses, not user requests |
| **AUTHENTICITY** | Detect authentic SPEECH patterns | Only triggers on self-disclosure, not user input |

**Root Cause**: These organs detect RESPONSE qualities, not USER NEEDS. Since TSK processes user input only, they always return 0.

---

## 57D Signature Architecture

### Dimension Layout

```
[0-5]:   V0 Energy Transformation (6D)
         - initial_v0, final_v0, descent_magnitude, descent_ratio, convergence_deviation, kairos_detected

[6-16]:  Organ Coherence SHIFTS (11D)
         - LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE, BOND, SANS, NDAM, RNX, EO, CARD

[17-19]: Polyvagal Transformation (3D)
         - initial_state (ventral=0, sympathetic=1, dorsal=2, scaled /2)
         - final_state
         - state_shift

[20-22]: Zone Transformation (3D)
         - initial_zone (1-5, scaled -1 then /4)
         - final_zone
         - zone_shift

[23-28]: Satisfaction Evolution (6D)
         - initial_satisfaction, final_satisfaction, improvement
         - absolute_change, positive_indicator, variance

[29-32]: Convergence Characteristics (4D)
         - cycles (normalized), speedup, stability, nexus_count (normalized)

[33-34]: Urgency Shift (2D)
         - initial_urgency, final_urgency

[35-37]: Emission Path (3D one-hot)
         - direct, fusion, kairos

[38-39]: Reserved (2D)

[40-42]: Nexus Type + Domain (3D)
         - initial_type, final_type, domain_shift

[43-46]: Constraint Deltas (4D)
         - delta_protection (BOND), delta_urgency (NDAM)
         - delta_coherence (SANS), delta_rhythm (RNX/EO)

[47-50]: Transductive Vocabulary (4D)
         - safety_words, crisis_words, connection_words, healing_words

[51-52]: Healing vs Crisis (2D)
         - healing_score, crisis_score

[53-56]: RNX Activation (4D)
         - temporal_diversity, pattern_coherence, emergence_rate, stability

Total: 57 dimensions (L2 normalized)
```

### Key Differentiators by Input Type

| Input Type | Polyvagal | Zone | Urgency | Example |
|------------|-----------|------|---------|---------|
| **Crisis** | sympathetic (0.5) | 3-4 | 0.6-0.9 | "I am in crisis!" |
| **Safety** | ventral (0.0) | 1 | 0.0 | "I feel safe" |
| **Boundary** | mixed (0.0) | 2-3 | 0.3 | "I need space" |
| **Collapse** | dorsal (1.0) | 5 | 0.1-0.3 | "I can't anymore" |

---

## TSK Creation Pipeline

### 1. Initial Felt-State (Pre-Processing)
```python
initial_felt_state = {
    'v0_initial': 1.0,  # Default energy
    'organ_coherences': {organ: 0.5 for organ in 11_organs},
    'polyvagal_state': 'ventral',  # Neutral start
    'zone': 1,  # SELF zone (connected)
    'satisfaction': 0.5,  # Neutral
    'urgency': 0.0  # No urgency yet
}
```

### 2. V0 Convergence (Multi-Cycle Processing)
```python
for cycle in range(max_cycles):
    # All 12 organs process text occasions in parallel
    organ_results = {
        'LISTENING': listening.process_text_occasions(occasions),
        'EMPATHY': empathy.process_text_occasions(occasions),  # Often 0
        'WISDOM': wisdom.process_text_occasions(occasions),      # Often 0
        ...
        'NEXUS': nexus.process_text_occasions(occasions),
    }

    # V0 energy descent
    v0_energy = compute_v0_descent(organ_results)

    # Satisfaction accumulation
    satisfaction = compute_satisfaction(organ_results)

    # Check convergence
    if energy_delta < threshold or satisfaction > 0.9:
        break
```

### 3. Final Felt-State Computation (Critical Fixes Applied)
```python
# BOND: Compute zone from mean_self_distance (not .zone attribute!)
bond_result = organ_results.get('BOND')
bond_self_dist = bond_result.mean_self_distance
if bond_self_dist > 0.8: zone = 5
elif bond_self_dist > 0.6: zone = 4
elif bond_self_dist > 0.4: zone = 3
elif bond_self_dist > 0.2: zone = 2
else: zone = 1

# NDAM: Use mean_urgency (not .urgency attribute!)
ndam_result = organ_results.get('NDAM')
urgency = ndam_result.mean_urgency

# EO: polyvagal_state exists directly
eo_result = organ_results.get('EO')
polyvagal_state = eo_result.polyvagal_state

final_felt_state = {
    'v0_final': final_v0,
    'organ_coherences': {org: result.coherence for org, result in organ_results},
    'polyvagal_state': polyvagal_state,  # Actual EO detection
    'zone': zone,  # Computed from BOND
    'satisfaction_final': satisfaction,
    'urgency': urgency  # Actual NDAM detection
}
```

### 4. 57D Signature Extraction
```python
signature = extractor.extract_transformation_signature_57d(
    initial_felt_state=initial_felt_state,
    final_felt_state=final_felt_state,
    transduction_trajectory=transduction_states,
    constraint_deltas=deltas,
    user_input=text,
    response={'emission': emission_text}
)
# Returns L2-normalized 57D numpy array
```

### 5. Family Assignment (Adaptive Clustering)
```python
family_assignment = families.assign_to_family(
    signature=signature,
    conversation_id=conv_id,
    satisfaction_score=final_satisfaction,
    organ_contributions=organ_coherences
)
# Uses cosine similarity with adaptive threshold (0.55 → 0.75)
```

---

## Critical Fixes Summary (November 16, 2025)

### Root Cause: Dictionary Key Mismatches

**Problem**: Wrapper used wrong keys to access organ results, always getting defaults:
- `organ.zone` → doesn't exist (BONDResult has `mean_self_distance`)
- `organ.urgency` → doesn't exist (NDAMResult has `mean_urgency`)
- `polyvagal_state` key vs attribute access

**Solution**: Three targeted fixes in `conversational_organism_wrapper.py`:
1. TSK recorder truthiness check (line 2447)
2. TSK final states with correct keys (lines 2453-2484)
3. Phase 5 final_felt_state with computed zone/urgency (lines 1153-1198)

**Result**: Signatures now capture ACTUAL organ responses:
- Crisis: sympathetic, zone 3, urgency 0.65
- Safety: ventral_vagal, zone 1, urgency 0.0
- Cosine similarity: 0.850 (was 0.983)

---

## Future Enhancements

### Priority 1: Dual-Pass Processing
Process BOTH user input AND system response:
```python
# Pass 1: User input → What does user NEED?
user_felt_state = process_text(user_input)

# Pass 2: System response → How did system RESPOND?
response_felt_state = process_text(system_response)

# Combined TSK: transformation + response quality
tsk = create_combined_tsk(user_felt_state, response_felt_state)
```

This would activate EMPATHY/WISDOM/AUTHENTICITY on system responses.

### Priority 2: User-Need Detectors
Extend organs to detect user needs, not just speech patterns:
```python
# Current EMPATHY: Detects empathic speech
"I understand how you feel" → coherence=0.85

# Future EMPATHY: Also detects need for empathy
"I feel so alone" → needs_empathy=0.9
```

### Priority 3: Transduction Trajectory Recording
Fix the per-cycle transduction recording error:
```
⚠️ Per-cycle transduction recording failed:
   local variable 'salience_trauma_markers' referenced before assignment
```

---

## Architecture Principles

1. **Truthful Signatures**: Every dimension captures ACTUAL organ processing, not defaults
2. **Transformation-Centric**: INITIAL→FINAL state change, not static snapshot
3. **Adaptive Clustering**: Threshold adjusts based on family count (exploration → consolidation)
4. **Organ Independence**: Each organ contributes independently to its dimensions
5. **L2 Normalization**: All signatures unit-normalized for cosine similarity
6. **Privacy-Preserving**: TSK captures patterns, not personal data

---

## Usage in Development

### Validating Organ Participation
```bash
export PYTHONPATH="/path/to/DAE_HYPHAE_1":$PYTHONPATH
python3 -c "
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
wrapper = ConversationalOrganismWrapper()
result = wrapper.process_text('I am in crisis')
for org, res in result['organ_results'].items():
    print(f'{org}: coherence={res.coherence:.3f}')
"
```

### Checking Signature Differentiation
```python
from persona_layer.organ_signature_extractor import OrganSignatureExtractor
extractor = OrganSignatureExtractor()

crisis_sig = extractor.extract_transformation_signature_57d(crisis_initial, crisis_final)
safety_sig = extractor.extract_transformation_signature_57d(safety_initial, safety_final)

cosine_sim = np.dot(crisis_sig, safety_sig)
print(f'Similarity: {cosine_sim:.3f}')  # Should be < 0.90 for different types
```

### Monitoring Family Emergence
```bash
cat persona_layer/organic_families.json | python3 -m json.tool | grep -A5 '"total_families"'
```

---

## References

- `TSK_ROOT_CAUSE_FIX_NOV16_2025.md` - Root cause analysis and fixes
- `persona_layer/organ_signature_extractor.py:911` - 57D signature extraction
- `persona_layer/conversational_organism_wrapper.py:1153` - Final felt-state computation
- `persona_layer/phase5_learning_integration.py:194` - Family clustering
- `persona_layer/organic_conversational_families.py` - Adaptive threshold logic

---

**Date**: November 16, 2025
**Status**: TSK Spinal Cord Operational - 9/12 Organs Active, Root Cause Fixed
