# Quick Fix Checklist - Training Infrastructure Repairs
**Date:** November 16, 2025  
**Urgency:** CRITICAL - Blocks multi-family emergence  
**Estimated Time:** 2-4 hours for Priority 1 fixes  

---

## PRIORITY 1: FIX NOW (Blocks Everything)

### [ ] Fix #1: Organ Participation Detection (organ_confidence_tracker.py:216-238)

**Current Code (BROKEN):**
```python
def _organ_participated(self, organ_result) -> bool:
    # ... some checks ...
    # DEFAULT: return True  # ALWAYS returns True!
    return True
```

**What to Do:**
1. Add real participation checks (check for non-zero activations)
2. Must return False if organ didn't actually compute anything
3. Test: After fix, organ_confidence.json should show mixed 0.3-0.8 not all 1.0

**Expected Outcome:**
```
BEFORE: All organs confidence=1.0, std=0.0
AFTER:  EMPATHY=0.72, WISDOM=0.68, SANS=0.35, RNX=0.28, std=0.17 ✅
```

**Quick Test:**
```bash
python3 -c "
from persona_layer.organ_confidence_tracker import OrganConfidenceTracker
tracker = OrganConfidenceTracker()
summary = tracker.get_summary()
print(f'Organ confidence std: {summary[\"std_confidence\"]:.3f}')
print(f'Should be > 0.05, got {summary[\"std_confidence\"]:.3f}')
"
```

---

### [ ] Fix #2: Activate Conversational Cluster Learning (phase5_learning_integration.py:240-245)

**Current Code (BROKEN - Line 241-243):**
```python
# Note: cluster_learning expects organ_results dict, but for transformation
# approach we'll need to adapt this. For now, skip cluster learning update
# and focus on family assignment (the critical part for DAE 3.0 replication)
```

**What to Do:**
1. UNCOMMENT or implement the cluster_learning.update call
2. Build organ_contributions from 65D signature dimensions
3. Extract organ weights from transformation signature

**Code to Add:**
```python
# After family_assignment block (around line 226):
self.cluster_learning.update_from_conversation(
    conversation_id=conversation_id,
    family_id=family_assignment.family_id,
    organ_results=organ_contributions,  # From 65D signature
    satisfaction_score=final_sat,
    emission_metrics=transformation_metrics,
    user_message=user_message,
    emission_text=emission_text
)
```

**Expected Outcome:**
- Family V0 targets and organ weights start being learned
- `conversational_clusters.json` gets populated

---

### [ ] Fix #3: Debug FAO Dimension Extraction (organ_signature_extractor.py:1430-1452)

**Current Code (May Be Broken):**
```python
if OrganAgreementComputer is not None and final_organs:
    # FAO dims 57-64 set here
else:
    signature_65d[57:65] = 0.5  # FALLBACK: All neutral!
```

**What to Do:**
1. Add logging to see which path is taken
2. Verify `OrganAgreementComputer` is imported successfully
3. Check if `final_organs` is populated correctly

**Debug Script:**
```python
import sys; sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')
from persona_layer.organ_signature_extractor import OrganSignatureExtractor
from persona_layer.organ_agreement_metrics import OrganAgreementComputer

extractor = OrganSignatureExtractor()
print(f"OrganAgreementComputer available: {OrganAgreementComputer is not None}")

# Test with real felt states
initial = {'organ_coherences': {'LISTENING': 0.7, 'EMPATHY': 0.8}}
final = {'organ_coherences': {'LISTENING': 0.75, 'EMPATHY': 0.82}}
sig = extractor.extract_transformation_signature_65d(initial, final)
print(f"FAO dims [57-64]: {sig[57:65]}")
# Should NOT all be 0.5!
```

**Expected Outcome:**
- FAO dimensions [57-64] contain actual agreement metrics
- Not all 0.5 (neutral)

---

## PRIORITY 2: FIX NEXT (Session After This)

### [ ] Fix #4: Integrate Signal Health Monitoring

**File:** `training/epoch_learning_orchestrator.py`

**Add to `_run_epoch()` method (after each epoch, around line 450):**
```python
# Compute signal health
health = self.signal_monitor.compute_epoch_health(
    families=self.phase5_learner.families.families,
    organ_confidences=self._get_organ_confidences()
)
self.signal_health_history.append(health)

# Warn if problems detected
if health['organ_confidence_std'] < 0.05:
    print(f"⚠️  WARNING: Organs not differentiating (std={health['organ_confidence_std']:.4f})")
```

**Expected Outcome:**
- See warnings about system health each epoch
- Track FAO agreement, multiplicity, etc.

---

### [ ] Fix #5: Connect FamilyV0Learner

**File:** `training/epoch_learning_orchestrator.py`

**In `_initialize_system()`, add:**
```python
from persona_layer.family_v0_learner import FamilyV0Learner
self.v0_learner = FamilyV0Learner(
    families_path=Path("persona_layer/state/active/organic_families.json"),
    learning_rate=0.1
)
```

**In `_run_epoch()`, after learning_report, add:**
```python
if learning_report and learning_report.get('learned'):
    self.v0_learner.update_family_v0(
        family_id=learning_report['family_id'],
        v0_final=result['felt_states']['v0_energy']['final_energy'],
        satisfaction=user_satisfaction,
        convergence_cycles=result['felt_states']['v0_energy']['cycles'],
        organ_coherences=result.get('organ_results', {})
    )
```

**At end of epoch:**
```python
self.v0_learner.save()
```

**Expected Outcome:**
- Each family learns its optimal V0 target
- Faster convergence in future conversations

---

### [ ] Fix #6: Activate Hebbian Memory Updates

**File:** `training/epoch_learning_orchestrator.py`

**In `_initialize_system()`, add:**
```python
from persona_layer.conversational_hebbian_memory import ConversationalHebbianMemory
self.hebbian_memory = ConversationalHebbianMemory(
    storage_path="persona_layer/state/active/conversational_hebbian_memory.json"
)
```

**In training loop, after each emission:**
```python
if self.hebbian_memory:
    outcome = ConversationalOutcome(
        polyvagal_state=result['felt_states']['eo_polyvagal_state'],
        polyvagal_confidence=0.8,  # From emission
        self_energy=result['felt_states'].get('self_energy', 0.0),
        self_energy_confidence=0.7,
        # ... populate other fields ...
    )
    self.hebbian_memory.update_from_outcome(outcome)
```

**Expected Outcome:**
- R-matrix learns polyvagal→response patterns
- Pattern memory gets populated

---

## PRIORITY 3: VERIFY & MONITOR

### [ ] Verify Tests Pass
```bash
cd /Users/daedalea/Desktop/DAE_HYPHAE_1
python3 -m pytest tests/integration/ -v
```

### [ ] Run Quick Epoch (3 epochs, 10 pairs)
```bash
python3 training/epoch_learning_orchestrator.py --num-epochs 3 --conversations-per-epoch 10
```

**Expected Output:**
```
Epoch 1:
  ✅ Families: 1-3 (starting from fresh)
  ✅ Organ conf std: 0.12-0.18 (IMPROVING!)
  ✅ Signal health: 0.75+ (system healthy)
  ✅ FAO agreement: 0.78-0.92 (organs coordinating)
  
Epoch 2:
  ✅ Families: 3-5 (more diversity)
  ✅ Organ conf std: 0.16-0.20 (even better)
  ✅ V0 targets: Started learning per-family
  
Epoch 3:
  ✅ Families: 5-8 (Zipf's law emerging)
  ✅ Organ conf std: 0.18+ (stable differentiation)
  ✅ Hebbian patterns: 10+ learned
```

---

## Testing Commands

```bash
# Test 1: Organ confidence differentiation
python3 << 'PYEOF'
import json
data = json.load(open('persona_layer/state/active/organ_confidence.json'))
confs = [m['confidence'] for m in data['organ_metrics'].values()]
import numpy as np
print(f"✅ Organ confidence std: {np.std(confs):.4f} (target: 0.15+)")
print(f"✅ Range: {min(confs):.3f} - {max(confs):.3f}")
PYEOF

# Test 2: Family emergence
python3 << 'PYEOF'
import json
data = json.load(open('persona_layer/state/active/organic_families.json'))
families = data.get('families', {})
print(f"✅ Families discovered: {len(families)}")
for fid, fam in list(families.items())[:3]:
    print(f"   {fid}: {fam['member_count']} members, maturity={fam['maturity_level']}")
PYEOF

# Test 3: FAO dimensions in signatures
python3 << 'PYEOF'
import sys; sys.path.insert(0, '.')
from persona_layer.organ_signature_extractor import OrganSignatureExtractor
import numpy as np
extractor = OrganSignatureExtractor()
sig = extractor.extract_transformation_signature_65d(
    {'organ_coherences': {'LISTENING': 0.7}},
    {'organ_coherences': {'LISTENING': 0.75}}
)
fao_dims = sig[57:65]
print(f"✅ FAO dimensions: {fao_dims}")
print(f"   All 0.5? {np.allclose(fao_dims, 0.5)}")
PYEOF
```

---

## Done Checklist

- [ ] Fix organ_participated() → organs differentiate (std > 0.1)
- [ ] Activate cluster_learning.update() → clusters learning organ weights
- [ ] Debug FAO extraction → FAO dims not all 0.5
- [ ] Run epoch with all 3 fixes → see multi-family emergence
- [ ] Record baseline metrics before fixes (make backup)
- [ ] Record metrics after fixes (see improvement)
- [ ] Commit fixes with message: "Fix: Activate dormant learning features (65D/FAO/cluster-learning)"

**Time Estimate:**
- Priority 1 fixes: 1-2 hours
- Testing: 30 minutes
- Priority 2 integration: 1-2 hours (can do later)

