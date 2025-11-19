# RNX Implementation Roadmap for DAE_HYPHAE_1

**Status**: Ready to implement
**Timeline**: 2-3 weeks
**Expected Impact**: +30-50pp conversational quality improvement
**Reference**: `RNX_LEGACY_INTEGRATION_ANALYSIS_NOV18_2025.md`

---

## Quick Summary

**Problem**: DAE_HYPHAE_1 lacks temporal awareness - can't distinguish between converging (CONCRESCENT) and diverging (CRISIS) satisfaction patterns.

**Solution**: RNX adds 3 missing capabilities:
1. **Satisfaction Fingerprinting** - Classify convergence as Crisis/Concrescent/Restorative/Pull
2. **Fourier Spectrum** - Compress temporal sequences from 100 floats → 5 params (20× compression)
3. **Field-Based Memory** - Entities emerge through felt-coherence, not Neo4j lookups

**No Breaking Changes**: All 11 organs remain unchanged. Pure additive enhancement.

---

## PHASE 1: SATISFACTION FINGERPRINTING (Week 1, 2-3 days)

### Goal
Classify satisfaction evolution into 4 archetypes. Use fingerprint to gate emission quality.

### Tasks

**1.1 Create `satisfaction_fingerprinting.py`** (200 lines)

```python
# persona_layer/satisfaction_fingerprinting.py

from enum import Enum
from dataclasses import dataclass
import numpy as np
from typing import List

class SatisfactionFingerprint(Enum):
    CRISIS = "CRISIS"          # Diverging, entropy rising
    CONCRESCENT = "CONCRESCENT"  # Converging, entropy falling
    RESTORATIVE = "RESTORATIVE"  # Crisis → Concrescent (Kairos!)
    PULL = "PULL"              # Oscillating, unstable
    STABLE = "STABLE"          # Equilibrium

@dataclass
class FingerprintResult:
    fingerprint_type: SatisfactionFingerprint
    confidence: float
    delta_S: np.ndarray
    metadata: dict

def classify_satisfaction_fingerprint(S_trace: List[float]) -> FingerprintResult:
    """See reference doc Part 1.3 for full implementation"""
    # Returns FingerprintResult with type + confidence
    pass
```

**Effort**: 1 day
**Testing**: Unit test with 5 satisfaction traces (crisis, concrescent, restorative, pull, stable)

---

**1.2 Wire to V0 Convergence** (50 lines)

```python
# In persona_layer/conversational_occasion.py

# Add after each V0 cycle:
S_trace = [results[i].satisfaction for i in range(cycle + 1)]
fingerprint = classify_satisfaction_fingerprint(S_trace)

if fingerprint.fingerprint_type == SatisfactionFingerprint.CRISIS:
    break  # Stop early, don't waste cycles
elif fingerprint.fingerprint_type == SatisfactionFingerprint.RESTORATIVE:
    kairos_confidence = 0.85
    break  # Opportune moment reached
```

**Effort**: 0.5 day
**Testing**: Run 10 conversational inputs, verify fingerprints in TSK logs

---

**1.3 Wire to Emission Gating** (80 lines)

```python
# In persona_layer/emission_generator.py or conversational_organism_wrapper.py

# Before returning emission:
fingerprint = conversation_tsk['satisfaction_fingerprint']

if fingerprint == "CRISIS":
    # Reject this emission, too risky
    confidence *= 0.7  # Penalize
elif fingerprint == "CONCRESCENT":
    # Boost quality
    confidence *= 1.1  # +10%
elif fingerprint == "RESTORATIVE":
    # Highest confidence
    confidence *= 1.2  # +20%
```

**Effort**: 0.5 day
**Testing**: Verify gating applied in TSK logs

---

**1.4 Add TSK Logging** (50 lines)

```python
# Log fingerprint to conversation_tsk
conversation_tsk['satisfaction_fingerprint'] = fingerprint.fingerprint_type.value
conversation_tsk['fingerprint_confidence'] = fingerprint.confidence
conversation_tsk['satisfaction_history'] = S_trace
```

**Effort**: 0.5 day
**Testing**: Verify TSK contains fingerprint data

---

### PHASE 1 Validation

Run 30-pair baseline training:
```bash
python3 dae_orchestrator.py train --mode baseline
```

Expected results:
- Fingerprints captured in TSK
- Crisis gating reducing over-emission
- Concrescent boosting improving quality
- Kairos detection 40-60%

---

## PHASE 2: FOURIER SPECTRUM (Week 2, 1-2 days)

### Goal
Compress satisfaction traces to FFT spectrum for bounded-memory archive strategy.

### Tasks

**2.1 Create `temporal_spectrum_analyzer.py`** (150 lines)

```python
# persona_layer/temporal_spectrum_analyzer.py

def compute_satisfaction_spectrum(S_trace: List[float]) -> Dict:
    """
    FFT decomposition of satisfaction evolution.
    Returns: {dc, low_freq, high_freq, dominant_freq, entropy}
    """
    # See reference doc Part 1.2 for full implementation
    pass

def spectrum_to_fingerprint(spectrum: Dict) -> str:
    """Reconstruct fingerprint from spectrum"""
    if spectrum['dc'] > 0.7 and spectrum['high_freq'] < 0.1:
        return "CONCRESCENT"
    elif spectrum['dc'] < 0.5:
        return "CRISIS"
    # ... etc
    pass
```

**Effort**: 1 day
**Testing**: 10 satisfaction traces, verify spectrum matches fingerprint

---

**2.2 Wire to Signature Extraction** (100 lines)

```python
# In persona_layer/organ_signature_extractor.py

# Add to extract_57d_signature():
S_trace = conversation_tsk['satisfaction_history']
spectrum = compute_satisfaction_spectrum(S_trace)

# Include spectrum in metadata
conversation_tsk['temporal_spectrum'] = {
    'dc': spectrum['dc'],
    'low_freq': spectrum['low_freq'],
    'high_freq': spectrum['high_freq'],
    'entropy': spectrum['entropy']
}
```

**Effort**: 0.5 day
**Testing**: Verify spectrum in TSK

---

**2.3 Archive Strategy (Optional)** (200 lines)

```python
# persona_layer/temporal_archive_manager.py

class TemporalArchiveBundle:
    def __init__(self):
        self.hot_atoms = {}      # Last 10 turns, full 7D
        self.warm_spectra = {}   # Turns 10-50, FFT only
        self.cold_aggregates = {} # Archive, mean only
    
    def archive_turn(self, turn_num, entities, coherences):
        """Move turn to appropriate tier"""
        if turn_num <= 10:
            self.hot_atoms[turn_num] = coherences
        elif turn_num <= 50:
            self.warm_spectra[turn_num] = compute_spectrum(coherences)
        else:
            self.cold_aggregates[turn_num] = np.mean(coherences)
```

**Effort**: 1 day (optional, can defer)
**Testing**: Verify archive has constant size (not growing with turns)

---

### PHASE 2 Validation

Run 30-pair training again:
```bash
python3 dae_orchestrator.py train --mode baseline
```

Expected results:
- Spectrum computed for all conversations
- Archive strategy (if implemented) keeping memory constant
- Fingerprint reconstructed from spectrum matches original

---

## PHASE 3: 65D SIGNATURES (Week 2, 1-2 days)

### Goal
Extend family clustering to 65D: 57D base + 8D temporal.

### Tasks

**3.1 Extract 65D Signature** (100 lines)

```python
# In persona_layer/organ_signature_extractor.py

def extract_65d_signature(conversation_tsk: Dict) -> np.ndarray:
    """
    65D signature: 57D base + 8D temporal
    
    New dimensions [57-64]:
      [57]: Spectrum DC
      [58]: Spectrum low-freq
      [59]: Spectrum high-freq
      [60]: Fingerprint type (0-4)
      [61]: Convergence length
      [62]: Satisfaction volatility
      [63]: Kairos detected
      [64]: Final satisfaction
    """
    signature = np.zeros(65)
    
    # [0-56]: Existing 57D
    signature[0:57] = extract_base_57d(conversation_tsk)
    
    # [57-64]: NEW temporal
    S_trace = conversation_tsk.get('satisfaction_history', [])
    spectrum = compute_satisfaction_spectrum(S_trace)
    fingerprint = classify_satisfaction_fingerprint(S_trace)
    
    signature[57:60] = [spectrum['dc'], spectrum['low_freq'], spectrum['high_freq']]
    signature[60] = fingerprint.fingerprint_type.value  # 0-4
    signature[61] = len(S_trace)
    signature[62] = np.std(S_trace) if len(S_trace) > 1 else 0.0
    signature[63] = 1.0 if conversation_tsk.get('kairos_detected') else 0.0
    signature[64] = S_trace[-1] if len(S_trace) > 0 else 0.5
    
    # L2 normalize
    norm = np.linalg.norm(signature)
    return signature / (norm + 1e-6) if norm > 0 else signature
```

**Effort**: 0.5 day
**Testing**: 10 conversations, verify signature is 65D and normalized

---

**3.2 Update Family Clustering** (30 lines)

```python
# In persona_layer/conversational_families.py or phase5_learning_integration.py

# Change:
# signature = extract_57d_signature(conversation_tsk)
# To:
signature = extract_65d_signature(conversation_tsk)

# Rest of clustering algorithm unchanged
# (similarity threshold, EMA updates, etc.)
```

**Effort**: 0.5 day
**Testing**: Run family discovery, verify families include temporal coherence

---

### PHASE 3 Validation

Run 100-pair expanded training:
```bash
# First expand training corpus (from CLAUDE.md instructions)
python3 dae_orchestrator.py train --mode expanded

# Monitor family emergence:
# Expected: 3-5 families with semantic meaning
# Expected: Temporal coherence distinguishes families
```

Expected results:
- 65D signatures extracted
- 3-5 semantic families emerge (vs 1 current)
- Families interpretable (temporal + emotional patterns)
- Zipf's law validation possible

---

## PHASE 4: LEARNING RATE MODULATION (Week 3, 1 day)

### Goal
Vary Hebbian learning rate based on fingerprint type (learn more from success, less from failure).

### Tasks

**4.1 Fingerprint-Based Learning Rate** (80 lines)

```python
# In persona_layer/phase5_learning_integration.py

def compute_learning_rate(conversation_tsk: Dict) -> float:
    """Fingerprint determines learning rate"""
    fingerprint = conversation_tsk['satisfaction_fingerprint']
    
    rates = {
        'CRISIS': 0.001,           # Low (learning from failure)
        'STABLE': 0.005,           # Medium
        'CONCRESCENT': 0.010,      # HIGH! (learning from success)
        'RESTORATIVE': 0.015,      # HIGHEST! (Kairos moment)
        'PULL': 0.002              # Low
    }
    
    return rates.get(fingerprint, 0.005)

# In apply_family_learning():
learning_rate = compute_learning_rate(conversation_tsk)
delta = learning_rate * (new_family_centroid - old_centroid)
```

**Effort**: 1 day
**Testing**: Verify R-matrix updates scale with fingerprint type

---

### PHASE 4 Validation

Run full 100-pair training:
```bash
python3 dae_orchestrator.py train --mode expanded
```

Monitor:
- Concrescent conversations get higher learning (delta*0.010 vs 0.005)
- Crisis conversations get lower learning (prevents over-fitting to failures)
- R-matrix evolves faster for RESTORATIVE

---

## SUCCESS CRITERIA

### After Phase 1
- [ ] Fingerprint types captured in 30+ conversations
- [ ] Crisis gating reducing false positives
- [ ] Concrescent boosting improving quality
- [ ] Kairos detection 40-60%

### After Phase 2
- [ ] Spectrum computed for all conversations
- [ ] FFT reconstruction matches original fingerprint
- [ ] Archive strategy (if implemented) constant memory

### After Phase 3
- [ ] 65D signatures extracted
- [ ] 3-5 semantic families emerge
- [ ] Temporal coherence distinguishes families

### After Phase 4
- [ ] Concrescent conversations learn 2× faster
- [ ] Crisis conversations learn slower
- [ ] R-matrix entropy stable

---

## TESTING CHECKLIST

Run before committing each phase:

```bash
# Phase 1 test
python3 tests/unit/satisfaction/test_fingerprinting.py

# Phase 2 test
python3 tests/unit/temporal/test_spectrum.py

# Phase 3 test
python3 tests/unit/signatures/test_65d_extraction.py

# Full pipeline
python3 dae_orchestrator.py validate --full

# Training validation
python3 dae_orchestrator.py train --mode baseline
python3 tests/validation/test_family_discovery.py
```

---

## Files to Create

| File | Lines | Priority | Phase |
|------|-------|----------|-------|
| `persona_layer/satisfaction_fingerprinting.py` | 200 | HIGH | 1 |
| `persona_layer/temporal_spectrum_analyzer.py` | 150 | MEDIUM | 2 |
| `persona_layer/temporal_archive_manager.py` | 200 | LOW (optional) | 2 |
| Tests for above | 200 | HIGH | Each |

---

## Files to Modify

| File | Lines | Change | Phase |
|------|-------|--------|-------|
| `persona_layer/conversational_occasion.py` | +50 | Add fingerprinting to V0 loop | 1 |
| `persona_layer/emission_generator.py` | +80 | Add gating logic | 1 |
| `persona_layer/organ_signature_extractor.py` | +100 | Extract 65D instead of 57D | 3 |
| `persona_layer/phase5_learning_integration.py` | +80 | Learning rate modulation | 4 |

---

## Risk Assessment

**Low Risk**:
- Phase 1: Satisfaction fingerprinting is fully additive, doesn't change organs
- Phase 2: Spectrum compression is read-only, doesn't affect inference
- Phase 3: 65D signatures extend 57D, clustering algorithm unchanged
- Phase 4: Learning rate modulation only affects R-matrix updates

**No Breaking Changes**: All existing functionality preserved.

---

## Expected Timeline

| Phase | Duration | Cumulative |
|-------|----------|-----------|
| 1: Fingerprinting | 2-3 days | ~Day 2 |
| 2: Spectrum | 1-2 days | ~Day 4 |
| 3: 65D Signatures | 1-2 days | ~Day 6 |
| 4: Learning Modulation | 1 day | ~Day 7 |
| Testing + validation | 2-3 days | ~Day 10 |

**Total**: ~10 days of focused development = 2 weeks with breaks

---

## Expected Impact Summary

| Metric | Baseline | Target | Comments |
|--------|----------|--------|----------|
| Kairos detection | 0-15% | 40-60% | Fingerprinting enables opportune moment detection |
| Organ maturity | 100% | 100% | No changes to core organs |
| Family count | 1 | 3-5 | Temporal dimension enables specialization |
| Emission quality | 70% organic | 75-80% | Crisis gating + concrescent boosting |
| Contextual fit | 75% | 85-90% | Learning rate modulation improves convergence |

---

## References

- `RNX_LEGACY_INTEGRATION_ANALYSIS_NOV18_2025.md` - Full technical analysis
- `/Volumes/[DPLM]/FFITTSSV0/docs/analysis/RNX_LEGACY_INTEGRATION_ASSESSMENT.md` - Original FFITTSS analysis
- `CLAUDE.md` - Project overview
- `CURRENT_STATE_NOV13_2025.md` - System status

---

**Status**: Ready to implement
**Next Step**: Start Phase 1 (satisfaction_fingerprinting.py)
**Questions**: See reference docs for code patterns and implementation details

