# Training Script Urgency Detection Fix - November 17, 2025

## The Problem

**Symptom**: All 75 training pairs showed `urgency: 0.000` despite NDAM having 93 keywords including new personal crisis keywords.

**Root Cause Chain**:
1. NDAM organ correctly detects urgency (validated: 0.650-0.780 for crisis inputs)
2. Organism wrapper correctly extracts urgency from NDAM (`result.mean_urgency`)
3. Organism wrapper correctly stores urgency in `felt_states['urgency']`
4. **TRAINING SCRIPT was extracting from wrong path**: `result.get('urgency', 0.0)` instead of `result['felt_states']['urgency']`

## The Fix

### File Modified: `training/phase1_wave_training.py`

**Lines 170-181 (OLD)**:
```python
# Extract metrics from result
satisfaction = result.get('satisfaction', 0.5)
urgency = result.get('urgency', 0.0)  # ❌ WRONG PATH
zone = result.get('zone', 1)
polyvagal_state = result.get('polyvagal_state', 'ventral_vagal')
nexus_count = result.get('nexus_count', 0)
ndam_coherence = result.get('ndam_coherence', 0.0)
bond_coherence = result.get('bond_coherence', 0.0)
eo_coherence = result.get('eo_coherence', 0.0)
convergence_cycles = result.get('convergence_cycles', 0)
```

**Lines 170-183 (NEW)**:
```python
# Extract metrics from result
# 🚨 FIX: Extract from felt_states nested dict (organism wrapper structure)
felt_states = result.get('felt_states', {})
satisfaction = felt_states.get('satisfaction_final', felt_states.get('satisfaction', 0.5))
urgency = felt_states.get('urgency', 0.0)  # ✅ NDAM's mean_urgency
zone = felt_states.get('zone', 1)
polyvagal_state = felt_states.get('polyvagal_state', 'ventral')
nexus_count = felt_states.get('nexus_count', 0)
ndam_coherence = felt_states.get('organ_coherences', {}).get('NDAM', 0.0)
bond_coherence = felt_states.get('organ_coherences', {}).get('BOND', 0.0)
eo_coherence = felt_states.get('organ_coherences', {}).get('EO', 0.0)
convergence_cycles = felt_states.get('convergence_cycles', 0)
field_coherence = felt_states.get('field_coherence', 0.0)  # ✅ Field coherence from felt_states
kairos_detected = felt_states.get('kairos_detected', False)
```

## Validation Steps

### 1. NDAM Isolation Test (PASSING ✅)
```bash
python3 diagnose_ndam_detection.py
```

**Results**:
- crisis_high_1: urgency 0.650, keywords: 2 (terrified, spiraling)
- crisis_high_2: urgency 0.780, keywords: 3 (now, crushing, breathe)
- shadow_1: urgency 0.650, keywords: 1 (ashamed)
- exile_1: urgency 0.650, keywords: 2 (shut down, numb)

**Mean urgency**: 0.683 ✅
**Detection rate**: 100% ✅

### 2. Organism Wrapper Return Structure

**From `conversational_organism_wrapper.py` lines 1650-1663**:
```python
return {
    'mode': 'processing_complete',
    'felt_states': felt_states,  # ✅ Nested dict containing all felt-state data
    'tsk_record': tsk_record,
    'organ_results': organ_results,
    # Emission data at top level
    'emission_text': emission_text,
    'emission_confidence': emission_confidence,
    'emission_path': emission_path,
    'emission_nexus_count': emission_nexus_count,
    'zone': zone_name,
    'zone_id': zone_id
}
```

**Felt-states structure** (from wrapper lines 1450-1466):
```python
final_felt_state = {
    'v0_initial': v0_initial,
    'v0_final': v0_final,
    'convergence_cycles': convergence_cycles,
    'organ_coherences': {
        'LISTENING': ..., 'EMPATHY': ..., 'WISDOM': ..., 'AUTHENTICITY': ...,
        'PRESENCE': ..., 'BOND': ..., 'SANS': ..., 'NDAM': ..., 'RNX': ..., 'EO': ..., 'CARD': ...
    },
    'polyvagal_state': getattr(organ_results.get('EO'), 'polyvagal_state', 'ventral'),
    'zone': computed_zone,
    'satisfaction_final': satisfaction_final,
    'urgency': ndam_urgency,  # ✅ Extracted from NDAM's mean_urgency attribute
    'emission_path': emission_path,
    'kairos_detected': kairos_detected,
    'nexus_count': len(nexuses)
}
```

## Expected Impact

### Before Fix:
- Urgency detection: 0% (always 0.000)
- Urgency variance: 0.000
- NDAM activation tracking: 0/75 (0%)

### After Fix:
- Urgency detection: 60-80% (keywords match crisis inputs)
- Urgency mean: 0.45-0.55 (mix of high/moderate/de-escalation)
- Urgency std: 0.25-0.35 (healthy variance across categories)
- NDAM activation tracking: 40-60/75 (53-80%)

**This variance is CRITICAL for R-matrix coupling learning:**
- NDAM ↔ EO coupling learns crisis → polyvagal state patterns
- NDAM ↔ BOND coupling learns urgency → firefighter activation patterns
- Wave protocols can modulate satisfaction based on urgency levels

## Architectural Insight

**Why this matters for fractal learning**:

The organism wrapper uses **nested structured data** (`felt_states` dict) to preserve all transformation metrics for:
1. **Phase 5 learning** (65D transformation signatures)
2. **Entity-organ tracking** (urgency context per entity mention)
3. **Superject learning** (per-user felt-state trajectories)
4. **TSK recording** (57D transductive state knowledge)

Training scripts MUST extract from this structured format, not assume flat top-level keys.

## Files Modified

1. `training/phase1_wave_training.py` (lines 170-183)
   - Fixed urgency, satisfaction, coherence extraction paths
   - All metrics now extracted from `felt_states` nested dict

## Remaining Issues

1. **Config import bug still present** (emission_generator.py lines 297, 1050)
   - Already fixed in previous session
   - Organism needs restart to take effect
   - Impact: Reconstruction pipeline unavailable (falls back to direct emission)

2. **Polyvagal ERROR: 'ventral'** (investigation needed)
   - Likely string comparison issue in training script
   - Does not block training, just logging

## Next Steps

1. ✅ Validate urgency extraction in 1-epoch test run
2. Run full 20-epoch training with corrected extraction
3. Analyze urgency variance and NDAM activation rates
4. Confirm R-matrix coupling emergence (NDAM ↔ EO, NDAM ↔ BOND)

## Session Context

**Date**: November 17, 2025
**Session**: Post-keyword expansion, pre-training validation
**Goal**: Enable wave training with satisfaction variance via urgency detection
**Status**: FIX APPLIED ✅, TESTING IN PROGRESS ⏳
