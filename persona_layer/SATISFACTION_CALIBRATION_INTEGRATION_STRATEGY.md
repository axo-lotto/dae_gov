# Satisfaction Calibration Integration Strategy
## Integrating FFITTSS Metacognitive Insights into DAE-GOV Persona Layer

**Date:** November 10, 2025
**Status:** Design Phase
**Phase:** 1.4c - Satisfaction Calibration Integration

---

## Executive Summary

FFITTSS (ARC-AGI grid solver) discovered a critical metacognitive insight: **satisfaction inversely correlates with accuracy** (-0.0617 correlation). High satisfaction + Low accuracy = "confident but wrong." This has profound implications for trauma-informed conversation, where high organ satisfaction when SELF-energy is low indicates **dangerous blending** (person fused with parts, unaware).

This document outlines the strategy for integrating satisfaction-based metacognitive awareness into DAE-GOV's 4-gate SELF-led cascade.

---

## Core Insight from FFITTSS

### The Discovery

```
High Accuracy (≥80%):  Avg Satisfaction 0.776 (uncertain but correct)
Low Accuracy (<80%):   Avg Satisfaction 0.795 (confident but wrong)
Inverse Correlation:   -0.0617

Transform Family:
  Success:    94.3% accuracy with 0.723 satisfaction (appropriately uncertain)
  Failures:   26.6% accuracy with 0.813 satisfaction (dangerously overconfident)
```

**Interpretation:** The system knows when it doesn't know. High satisfaction indicates convergence confidence, NOT solution correctness.

### Four Quadrants

| Accuracy | Satisfaction | Status | Action |
|----------|--------------|--------|--------|
| High | High | ✅ Correctly confident | Deploy |
| High | Low | ⚠️ Uncertain success | Investigate why |
| Low | High | 🚨 **DANGEROUS** | RED FLAG - System overconfident |
| Low | Low | ✓ Appropriately uncertain | Need more data |

---

## Translation to Conversational Context

### Parallel Between FFITTSS and DAE-GOV

| FFITTSS (Grid) | DAE-GOV (Conversation) | Danger Pattern |
|----------------|------------------------|----------------|
| High satisfaction + Low accuracy | High satisfaction + Low SELF-energy | Dangerous blending |
| Transform family (unstable) | Crisis family (trauma activation) | Need containment |
| Organ convergence confidence | Organ agreement on state | Parts coalition without SELF |
| Metacognitive awareness | Trauma-informed safety | Know when unsafe |

### The Conversational Danger Zone

**Dangerous Blending Pattern:**
```python
if satisfaction > 0.8 and self_energy < 0.6:
    status = "DANGEROUS_BLENDING"
    interpretation = "High organ agreement on parts-led state - person fused with parts, unaware"
    action = "CONTAIN - Do not proceed to deep work"
```

**Example:**
- **Text:** "I'm completely worthless and everyone would be better off without me."
- **Detection:**
  - Polyvagal: Dorsal (0.85 confidence)
  - BOND: Strong exile blending (high coherence, 0.9 agreement)
  - SELF-energy: 0.2 (completely blended)
  - **Satisfaction: 0.85** (organs AGREE this is the state)

**Danger:** High satisfaction = organs converged on "this IS true" (no SELF distance, no observer). This is **fusion**, not exploration.

**Appropriate Response:** CONTAIN at Gate 3, invite grounding BEFORE parts work.

---

## Integration Architecture

### Current Gate 3 (SELF-Energy Check)

```python
def _gate_3_self_energy_check(self, text, organism_context, bagua_context):
    """Gate 3: SELF-Energy Check (CURRENT)"""

    # Detect SELF-energy
    self_energy = self.self_detector.detect_self_energy(text, ...)

    # Simple threshold
    if self_energy.self_energy < 0.6:
        return (False, "GROUND", "Invite to ground with SELF")
    else:
        return (True, "PROCEED", "SELF-energy present")
```

### Enhanced Gate 3 (Satisfaction-Aware)

```python
def _gate_3_self_energy_check(self, text, organism_context, bagua_context):
    """Gate 3: SELF-Energy Check with Metacognitive Satisfaction Awareness"""

    # Detect SELF-energy
    self_energy = self.self_detector.detect_self_energy(text, ...)

    # Get organism satisfaction (from V0 convergence)
    satisfaction = organism_context.get('satisfaction', 0.7)

    # Get organ coherence (agreement level)
    coherence = organism_context.get('mean_coherence', 0.5)

    # Metacognitive check: DANGEROUS BLENDING pattern
    if self_energy.self_energy < 0.6:

        # HIGH satisfaction + LOW SELF = Dangerous blending
        if satisfaction > 0.8 and coherence > 0.75:
            return (
                False,
                "DANGEROUS_BLENDING",
                "High organ agreement on parts-led state - person fused with parts, unaware. CONTAIN."
            )

        # MEDIUM satisfaction + LOW SELF = Uncertain parts state
        elif satisfaction > 0.6:
            return (
                False,
                "PARTS_UNCLEAR",
                "Parts present but unclear agreement - GROUND with curiosity"
            )

        # LOW satisfaction + LOW SELF = Appropriately uncertain
        else:
            return (
                False,
                "APPROPRIATE_UNCERTAINTY",
                "Low SELF-energy AND low satisfaction - system knows uncertainty. GROUND."
            )

    # SELF-led: Proceed with confidence
    else:
        return (True, "SELF_LED", f"SELF-energy present: {self_energy.dominant_c}")
```

---

## Conversational Family Detection

### Proposed Families (Analogous to FFITTSS)

| Family | Characteristics | Satisfaction Pattern | Multiplier |
|--------|----------------|---------------------|------------|
| **Crisis** | Dorsal shutdown, exile flooding, high distress | Inverse (-1.0) | High agreement = MORE danger |
| **Parts Work** | Multiple parts active, complex internal system | Moderate inverse (-0.3) | Some agreement ok |
| **SELF-Led** | Observer present, 8 C's active, grounded | Standard (0.0) | Agreement is good |
| **Grounding** | Transitional, moving toward SELF | Weak inverse (-0.2) | Monitor closely |

### Family Detection Logic

```python
def detect_conversational_family(self, text, polyvagal, self_energy, organism_context):
    """Detect which conversational family this belongs to"""

    satisfaction = organism_context.get('satisfaction', 0.7)
    ofel_energy = organism_context.get('ofel_energy', 0.5)

    # CRISIS: Dorsal + High OFEL + Low SELF
    if polyvagal.dominant_state == 'dorsal' and ofel_energy > 0.7 and self_energy.self_energy < 0.4:
        return 'crisis', -1.0  # Full inverse satisfaction

    # PARTS WORK: Mixed states, moderate SELF
    elif self_energy.self_energy >= 0.4 and self_energy.self_energy < 0.6:
        return 'parts_work', -0.3  # Moderate inverse

    # SELF-LED: Ventral + High SELF
    elif polyvagal.dominant_state == 'ventral' and self_energy.self_energy >= 0.6:
        return 'self_led', 0.0  # Standard (no inverse)

    # GROUNDING: Transitional
    else:
        return 'grounding', -0.2  # Weak inverse
```

---

## Calibrated Gate 3 with Family-Specific Multipliers

```python
def _gate_3_self_energy_check_calibrated(self, text, organism_context, bagua_context):
    """Gate 3: SELF-Energy Check with Family-Specific Calibration"""

    # Detect SELF-energy
    self_energy = self.self_detector.detect_self_energy(text, ...)
    polyvagal = organism_context['polyvagal']

    # Get organism metrics
    satisfaction = organism_context.get('satisfaction', 0.7)
    coherence = organism_context.get('mean_coherence', 0.5)

    # Detect conversational family
    family, multiplier = self.detect_conversational_family(
        text, polyvagal, self_energy, organism_context
    )

    # Compute metacognitive confidence score
    # (inspired by FFITTSS metacognitive formula)
    metacog_confidence = self._compute_metacognitive_confidence(
        coherence=coherence,
        exclusion=organism_context.get('ofel_energy', 0.5),
        satisfaction=satisfaction,
        multiplier=multiplier,  # Family-specific
        self_energy=self_energy.self_energy
    )

    # Decision logic based on metacognitive confidence
    if family == 'crisis':
        # Crisis family: HIGH satisfaction = MORE dangerous
        if satisfaction > 0.8 and self_energy.self_energy < 0.4:
            return (False, "CONTAIN", "CRISIS: High agreement on shutdown - dangerous blending")
        else:
            return (False, "GROUND", "CRISIS: Invite grounding with containment")

    elif family == 'parts_work':
        # Parts work: Moderate satisfaction ok if SELF present
        if self_energy.self_energy >= 0.5:
            return (True, "PROCEED", "PARTS WORK: SELF-energy sufficient for exploration")
        else:
            return (False, "GROUND", "PARTS WORK: Need more SELF-energy before proceeding")

    elif family == 'self_led':
        # SELF-led: Satisfaction is valid confidence
        return (True, "RESPOND", f"SELF-LED: {self_energy.dominant_c} present")

    else:  # grounding
        # Grounding: Monitor uncertainty
        if metacog_confidence < 0.5:
            return (False, "CLARIFY", "GROUNDING: System uncertain - clarify before proceeding")
        else:
            return (False, "GROUND", "GROUNDING: Invite presence with SELF")
```

---

## Metacognitive Confidence Formula

**Adapted from FFITTSS:**

```python
def _compute_metacognitive_confidence(
    self,
    coherence: float,      # Organ agreement [0,1]
    exclusion: float,      # OFEL energy [0,1]
    satisfaction: float,   # V0 satisfaction [0,1]
    multiplier: float,     # Family-specific (-1.0 to 0.0)
    self_energy: float     # SELF-energy level [0,1]
) -> float:
    """
    Compute metacognitive confidence with family-specific satisfaction calibration.

    Formula inspired by FFITTSS Phase 8C:
        M = w_C * Coherence +
            w_E * (1 - Exclusion) +        # Relief term
            w_S * multiplier * Satisfaction +  # NEGATIVE for crisis
            w_SELF * SELF_energy

    Returns:
        Metacognitive confidence [0,1]
        - High confidence = Safe to proceed
        - Low confidence = Need caution/clarification
    """
    w_C = 0.3      # Coherence weight
    w_E = 0.2      # Exclusion relief weight
    w_S = 0.3      # Satisfaction weight (modulated by multiplier)
    w_SELF = 0.2   # SELF-energy weight

    # Compute components
    coherence_term = w_C * coherence
    relief_term = w_E * (1.0 - exclusion)  # Lower exclusion = better
    satisfaction_term = w_S * multiplier * satisfaction  # NEGATIVE for crisis
    self_term = w_SELF * self_energy

    # Sum and clamp to [0,1]
    metacog = coherence_term + relief_term + satisfaction_term + self_term
    metacog = np.clip(metacog, 0.0, 1.0)

    return float(metacog)
```

**Key Insight:** For crisis family (multiplier=-1.0), high satisfaction DECREASES metacognitive confidence, flagging dangerous blending.

---

## Implementation Plan

### Phase 1: Add Satisfaction Awareness to Gate 3 (2-3 hours)

**Files to modify:**
1. `self_led_cascade.py:362-415` - Enhance `_gate_3_self_energy_check()`
2. Add satisfaction parameter to organism_context (already available from V0)
3. Add metacognitive confidence computation

**Changes:**
```python
# In process_conversational_turn()
organism_context['satisfaction'] = satisfaction  # From V0 convergence
organism_context['mean_coherence'] = np.mean([o['coherence'] for o in organs.values()])
```

### Phase 2: Implement Family Detection (1-2 hours)

**New method:**
```python
def detect_conversational_family(
    self,
    text: str,
    polyvagal: PolyvagalDetection,
    self_energy: SELFEnergyDetection,
    organism_context: Dict[str, Any]
) -> Tuple[str, float]:
    """Detect conversational family and return satisfaction multiplier"""
    # Implementation as outlined above
```

### Phase 3: Add Metacognitive Formula (1 hour)

**New method:**
```python
def _compute_metacognitive_confidence(
    self,
    coherence: float,
    exclusion: float,
    satisfaction: float,
    multiplier: float,
    self_energy: float
) -> float:
    """Compute metacognitive confidence with FFITTSS-inspired formula"""
    # Implementation as outlined above
```

### Phase 4: Update Tests (1-2 hours)

**New test scenarios:**
1. Crisis + High Satisfaction → CONTAIN (dangerous blending)
2. Crisis + Low Satisfaction → GROUND (appropriate uncertainty)
3. Parts Work + Moderate Satisfaction → Contextual decision
4. SELF-Led + High Satisfaction → RESPOND (valid confidence)

**Test file:** `test_satisfaction_calibration.py`

---

## Expected Impact

### Improved Safety Detection

**Before (simple threshold):**
- Low SELF-energy → Always GROUND
- Doesn't distinguish dangerous blending from appropriate uncertainty

**After (satisfaction-aware):**
- Low SELF + High Satisfaction → CONTAIN (dangerous)
- Low SELF + Low Satisfaction → GROUND (uncertain but aware)
- Metacognitive awareness of system confidence

### Trauma-Informed Responsiveness

| Pattern | Detection | Response | Clinical Rationale |
|---------|-----------|----------|-------------------|
| "I'm worthless" (dorsal, high agreement) | Dangerous blending | CONTAIN | Fused with exile, no observer |
| "I notice I'm worthless" (observer present) | Parts with SELF | GROUND | Observer present, can work |
| "Something feels off" (low satisfaction) | Appropriate uncertainty | CLARIFY | System knows it doesn't know |
| "I'm curious about this part" (SELF-led) | SELF-energy present | RESPOND | Safe to proceed |

---

## Validation Criteria

### Success Metrics

1. **Dangerous Blending Detection:** Correctly flag high satisfaction + low SELF as CONTAIN
2. **Family Classification:** Accurate detection of crisis/parts_work/self_led/grounding
3. **Metacognitive Calibration:** Inverse satisfaction in crisis family, standard in SELF-led
4. **No False Positives:** Don't over-contain appropriate uncertainty

### Test Cases

```python
# Test 1: Dangerous blending (high satisfaction crisis)
text = "I'm completely worthless and everyone would be better off without me."
# Expected: satisfaction=0.85, self_energy=0.2, family='crisis', decision='CONTAIN'

# Test 2: Appropriate uncertainty (low satisfaction crisis)
text = "Everything feels really confusing and I don't know what's happening."
# Expected: satisfaction=0.4, self_energy=0.3, family='grounding', decision='CLARIFY'

# Test 3: SELF-led confidence (high satisfaction SELF-led)
text = "I'm feeling compassion toward this hurt part and curious what it needs."
# Expected: satisfaction=0.75, self_energy=0.8, family='self_led', decision='RESPOND'
```

---

## Timeline

**Total Estimated Time:** 5-8 hours

- Phase 1: Satisfaction awareness (2-3h)
- Phase 2: Family detection (1-2h)
- Phase 3: Metacognitive formula (1h)
- Phase 4: Tests and validation (1-2h)

---

## Next Steps

1. **Review this strategy** with user for alignment
2. **Implement Phase 1** (satisfaction awareness)
3. **Validate with test cases**
4. **Iterate based on results**
5. **Document findings** in Phase 1.4d summary

---

## References

- **FFITTSS Satisfaction Calibration V2 Presentation** (November 2025)
- **FFITTSS Metacognition Insight Analysis** (Legacy document)
- **DAE-GOV Architecture Addendum Phase 1.2-1.3** (Persona layer design)
- **IFS Model (Schwartz)** - SELF-energy and parts theory

---

**Status:** ✅ STRATEGY COMPLETE - Ready for implementation discussion
