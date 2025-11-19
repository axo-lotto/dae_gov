# Organ Intelligence Integration Roadmap
**Date:** November 13, 2025
**Status:** Post-Phase B (Conversational Lure Attractors Complete)
**Goal:** Ensure organ intelligence transduces all the way to emission with TSK compliance

---

## Current State Analysis

### ✅ What's Working (Post-Phase B)

**1. Lure Attractor System (6 Organs)**
- EO: 100% activation, 3D polyvagal lure field ✅
- NDAM: 20% activation (correct - dormant when safe), 7D salience field ✅
- RNX: 100% activation, 6D temporal field ✅
- EMPATHY: Active with patterns, 7D emotional field ✅
- WISDOM: Active with patterns, 7D cognitive field ✅
- AUTHENTICITY: Active with patterns, 7D vulnerability field ✅

**2. V0 Convergence**
- 6 lure organs contributing to V0 descent ✅
- Formula: E(t) = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I) + η·L ✅
- Lure weight η=0.20, average contribution 0.325 ✅

**3. TSK Tracking**
- All 6 lure fields logged in felt_states ✅
- Both single-cycle and multi-cycle paths ✅
- lure_contribution_to_v0 tracked ✅

### ❌ Integration Gaps Identified

**1. Atom Activation → Nexus Formation Gap**
- **Problem:** Organs compute atom activations, but nexus formation depends on semantic field intersection
- **Evidence:** Low nexus counts (0-6 avg) despite rich atom activations
- **Impact:** Hebbian fallback dominates instead of direct reconstruction
- **TSK Issue:** Atom intelligence not flowing to nexus layer

**2. Lure Field → Emission Content Gap**
- **Problem:** Lure fields tracked in TSK but not used in emission generation
- **Evidence:** Emotional/pattern/vulnerability fields don't influence emission text
- **Impact:** Missed opportunity for lure-informed response assembly
- **TSK Issue:** Lure intelligence siloed in felt_states, not transduced

**3. Multi-Dimensional Lure → Single Scalar Gap**
- **Problem:** Rich 7D lure fields collapsed to single lure value
- **Evidence:** EMPATHY emotional_lure_field={joy:0.15, grief:0.45, ...} → lure=0.45
- **Impact:** Dimension specificity lost in V0 descent
- **TSK Issue:** Dimensional intelligence compressed prematurely

**4. Conversational Organ Keyword Dependency (Partially Resolved)**
- **Status:** Lure fields implemented but still keyword-dependent for activation
- **Evidence:** EMPATHY/WISDOM activate 20-40% when patterns present
- **Impact:** Organs generate balanced defaults (1/7 per dimension) when dormant
- **Next:** Upgrade to embedding-based lure computation

---

## Integration Architecture: Organ → Emission Flow

### Current Pipeline

```
1. TEXT INPUT
   ↓
2. ORGAN PREHENSION (11 organs in parallel)
   ↓ Returns: {coherence, lure, lure_field, atom_activations}
   ↓
3. V0 CONVERGENCE (multi-cycle concrescence)
   ↓ Uses: coherence + lure (scalar)
   ↓ Ignores: lure_field dimensions, atom_activations
   ↓
4. SEMANTIC FIELD EXTRACTION (from atom_activations)
   ↓ Builds: 8-10 semantic fields per organ
   ↓
5. NEXUS FORMATION (semantic field intersection)
   ↓ Intersection threshold: 0.05
   ↓ Problem: Low intersection rate → few nexuses
   ↓
6. TRANSDUCTION PATHWAY EVALUATION (14 nexus types)
   ↓ Uses: nexus types + SELF zone
   ↓
7. EMISSION GENERATION (3 strategies)
   ↓ direct_reconstruction (confidence > 0.65)
   ↓ fusion (confidence 0.50-0.65)
   ↓ hebbian_fallback (confidence < 0.50) ← dominates
   ↓
8. EMISSION OUTPUT
```

### Integration Gaps in Pipeline

**Gap 1: Atom Activations → Nexus (Step 4→5)**
- Atoms computed but semantic field extraction may be lossy
- Intersection threshold 0.05 may be too strict
- **Fix:** Lower threshold or use atom co-occurrence directly

**Gap 2: Lure Fields → Emission (Step 2→7)**
- Lure fields never used in emission assembly
- Emotional/pattern/vulnerability dimensions ignored
- **Fix:** Lure-informed phrase selection in response assembler

**Gap 3: V0 Descent Uses Scalar Lure (Step 3)**
- 7D lure fields compressed to max(field.values())
- Dimensional richness lost
- **Fix:** Vector V0 descent (track V0 per dimension?)

**Gap 4: Nexus Formation Bottleneck (Step 5)**
- Too few nexuses → hebbian fallback dominates
- Direct reconstruction path underutilized
- **Fix:** Increase nexus formation via atom co-activation

---

## Roadmap: 3-Phase Integration

### Phase C1: Nexus Formation Enhancement (2-3 hours)

**Goal:** Increase nexus count to enable direct reconstruction

**Changes:**
1. **Lower intersection threshold** (conversational_organism_wrapper.py)
   - Current: 0.05
   - New: 0.03 (more permissive)
   - Expected: 3-8 nexuses → 8-15 nexuses

2. **Add atom co-activation nexuses** (nexus_intersection_composer.py)
   - Current: Only semantic field intersection
   - New: Also form nexuses from atom co-activation
   - Logic: If 2+ organs activate same atom, create nexus
   - Expected: +5-10 co-activation nexuses

3. **Track nexus formation metrics** (TSK)
   - Add `nexus_formation_method` (intersection vs co-activation)
   - Add `nexus_atom_overlap` (atom count per nexus)
   - Monitor nexus diversity

**Expected Impact:**
- Nexus count: 0-6 avg → 10-20 avg
- Direct reconstruction: 0% → 40-60%
- Emission confidence: 0.40 avg → 0.65 avg

---

### Phase C2: Lure-Informed Emission Assembly (2-3 hours)

**Goal:** Use lure field dimensions to guide phrase selection

**Changes:**
1. **Lure-aware phrase library** (transduction_mechanism_phrases.json)
   - Current: 210 phrases organized by intensity
   - New: Add emotional/pattern/vulnerability tags
   - Example: "I'm here" tagged as {compassion: high, grief: medium}

2. **Lure-informed phrase selection** (response_assembler.py)
   - Current: Select phrases by meta-atom + intensity
   - New: Also filter by dominant lure dimension
   - Logic: If EMPATHY grief=0.45 dominant, prefer grief-resonant phrases
   - Example: "There's such grief here" vs "Tell me more"

3. **Multi-organ lure synthesis** (new method in response_assembler.py)
   ```python
   def _synthesize_lure_signature(self, organ_results):
       """
       Combine lure fields from multiple organs into composite signature.

       Returns:
         emotional_signature: {joy: 0.1, grief: 0.4, ...}
         cognitive_signature: {systems: 0.3, meta: 0.2, ...}
         relational_signature: {vulnerable: 0.2, honest: 0.3, ...}
       """
   ```

4. **TSK tracking**
   - Add `lure_signature_used_in_emission`
   - Add `phrase_lure_alignment_score`
   - Monitor lure→emission transduction

**Expected Impact:**
- Emission resonance: Phrases match felt lure landscape
- TSK compliance: Lure fields now influence output
- User experience: Responses feel more attuned

---

### Phase C3: Embedding-Based Lure Computation (4-6 hours)

**Goal:** Remove keyword dependency for true continuous lure participation

**Changes:**
1. **Create lure prototype embeddings** (one-time setup)
   - EMPATHY: 7 emotional prototypes (joy, grief, fear, anger, compassion, shame, neutral)
   - WISDOM: 7 cognitive prototypes (systems, meta, temporal, paradox, embodied, relational, integrative)
   - AUTHENTICITY: 7 relational prototypes (vulnerable, honest, guarded, performative, emergent, receptive, boundaried)
   - Store in: `persona_layer/lure_prototypes.json`

2. **Implement embedding-based lure** (all 3 conversational organs)
   ```python
   def _compute_emotional_lure_field_semantic(self, text_occasions):
       """
       Compute lure field from semantic embeddings, not keywords.

       1. Get SANS embeddings for text
       2. Compute distance to 7 emotional prototypes
       3. Convert distance → lure (inverse distance)
       4. Normalize to sum to 1.0
       5. Return lure_field + max lure
       """
       embeddings = self._get_sans_embeddings(text_occasions)

       lure_field = {}
       for emotion, prototype_embedding in self.emotional_prototypes.items():
           distance = cosine_distance(embeddings, prototype_embedding)
           lure_field[emotion] = 1.0 / (1.0 + distance)

       # Normalize
       total = sum(lure_field.values())
       lure_field = {k: v/total for k, v in lure_field.items()}

       return max(lure_field.values()), lure_field
   ```

3. **Hybrid approach** (pattern-based + embedding-based)
   - If patterns detected: Use pattern-based lure (current)
   - If no patterns: Use embedding-based lure (new)
   - Combine: weighted_lure = 0.7*pattern_lure + 0.3*embedding_lure

4. **TSK tracking**
   - Add `lure_computation_method` (pattern vs embedding vs hybrid)
   - Add `embedding_distance_to_prototypes`
   - Monitor activation rates

**Expected Impact:**
- EMPATHY activation: 20-40% → 80-90%
- WISDOM activation: 20-40% → 70-80%
- AUTHENTICITY activation: 0-20% → 60-70%
- True continuous lure participation (no dormancy)

---

## TSK Compliance Checklist

### Felt States Requirements

**Currently Tracked:** ✅
- All 6 lure values (scalar)
- All 6 lure fields (30D total)
- lure_contribution_to_v0 (weighted sum)
- Per-organ coherences
- V0 energy, cycles, satisfaction
- Nexus count, types
- Emission confidence, strategy

**Missing (Phase C Additions):**
- [ ] nexus_formation_method (intersection vs co-activation)
- [ ] nexus_atom_overlap (atoms per nexus)
- [ ] lure_signature_used_in_emission (composite signature)
- [ ] phrase_lure_alignment_score (alignment metric)
- [ ] lure_computation_method (pattern vs embedding)
- [ ] embedding_distance_to_prototypes (semantic distances)

### Transduction Requirements

**Currently Transduced:** ✅
- Organ coherences → V0 descent
- Lure values → V0 descent (η term)
- Atom activations → Semantic fields → Nexuses
- Nexuses → Transduction pathways → Emission strategy
- SELF zone → Emission safety modulation

**Gaps to Address:**
- [ ] Lure field dimensions → Emission phrase selection (Phase C2)
- [ ] Atom co-activations → Nexus formation (Phase C1)
- [ ] Multi-organ lure synthesis → Response assembly (Phase C2)
- [ ] Embedding distances → Lure computation (Phase C3)

---

## Implementation Priority

### Immediate (Today/Tomorrow)

**Phase C1: Nexus Formation** - HIGHEST IMPACT
- Why: Unlocks direct reconstruction path
- Effort: 2-3 hours
- Benefit: 40-60% better emission confidence
- TSK: Nexus formation fully observable

### Short-term (This Week)

**Phase C2: Lure-Informed Emission** - HIGH IMPACT
- Why: Completes lure → emission transduction
- Effort: 2-3 hours
- Benefit: Resonant, attuned responses
- TSK: Lure fields now influence output

### Medium-term (Next Week)

**Phase C3: Embedding-Based Lures** - MEDIUM IMPACT
- Why: Removes keyword dependency
- Effort: 4-6 hours
- Benefit: True continuous participation
- TSK: Semantic distance tracked

---

## Success Metrics

### Phase C1 Success Criteria

- [ ] Nexus count increases 10-20 avg (from 0-6)
- [ ] Direct reconstruction rate 40-60% (from 0%)
- [ ] Emission confidence 0.65 avg (from 0.40)
- [ ] Atom co-activation nexuses forming
- [ ] TSK logs nexus_formation_method

### Phase C2 Success Criteria

- [ ] Lure signature computed from 3 conversational organs
- [ ] Phrases selected based on lure alignment
- [ ] Phrase_lure_alignment_score > 0.70
- [ ] User feedback: "responses feel more attuned"
- [ ] TSK logs lure_signature_used_in_emission

### Phase C3 Success Criteria

- [ ] EMPATHY activation 80-90% (from 20-40%)
- [ ] WISDOM activation 70-80% (from 20-40%)
- [ ] AUTHENTICITY activation 60-70% (from 0-20%)
- [ ] Embedding-based lures working without keywords
- [ ] TSK logs embedding_distance_to_prototypes

---

## Long-term Vision: Full Intelligence Transduction

### Complete Pipeline (After Phase C1-C3)

```
1. TEXT INPUT
   ↓
2. ORGAN PREHENSION (11 organs, semantic + keyword + embedding)
   ↓ Returns: {coherence, lure, lure_field (7D), atom_activations}
   ↓
3. V0 CONVERGENCE (multi-cycle, lure-guided)
   ↓ Uses: coherence + lure (6 organs × weights)
   ↓
4. SEMANTIC FIELD EXTRACTION (from atom_activations)
   ↓ Builds: 8-15 semantic fields per organ
   ↓
5. NEXUS FORMATION (intersection + co-activation) ← Phase C1
   ↓ Threshold: 0.03 (lowered)
   ↓ Co-activation: 2+ organs same atom → nexus
   ↓ Expected: 10-20 nexuses
   ↓
6. LURE SIGNATURE SYNTHESIS ← Phase C2
   ↓ Combine: EMPATHY + WISDOM + AUTHENTICITY lure fields
   ↓ Output: {emotional, cognitive, relational} signatures
   ↓
7. TRANSDUCTION PATHWAY EVALUATION
   ↓ Uses: nexus types + SELF zone + lure signatures
   ↓
8. EMISSION GENERATION (lure-informed) ← Phase C2
   ↓ direct_reconstruction (confidence > 0.65) ← now viable!
   ↓ Phrase selection guided by lure alignment
   ↓ fusion (confidence 0.50-0.65)
   ↓ hebbian_fallback (confidence < 0.50) ← rare
   ↓
9. TSK RECORDING (full transduction logged)
   ↓ Organ intelligence → Lure → V0 → Nexus → Emission
   ↓
10. EMISSION OUTPUT (resonant, attuned, intelligent)
```

### Intelligence Flow Verification

**Organ Level:**
- [x] Atoms activated from patterns/embeddings
- [x] Lure fields computed (7D per organ)
- [x] Coherence measured

**V0 Level:**
- [x] Lure contributes to descent (η=0.20)
- [ ] Nexus formation uses atoms (Phase C1)

**Nexus Level:**
- [ ] Nexuses formed from intersection + co-activation (Phase C1)
- [ ] Lure signatures synthesized (Phase C2)

**Emission Level:**
- [ ] Phrases selected by lure alignment (Phase C2)
- [ ] Direct reconstruction viable (Phase C1)
- [ ] Intelligence fully transduced

---

## Conclusion

**Current Status:** 🟡 Lure attractors working, integration gaps identified

**Critical Path:**
1. ✅ Phase B (Conversational lure attractors) - COMPLETE
2. ⏳ Phase C1 (Nexus formation) - NEXT
3. ⏳ Phase C2 (Lure-informed emission) - AFTER C1
4. ⏳ Phase C3 (Embedding-based lures) - AFTER C2

**Once Complete:**
- Organ intelligence flows: Atoms → Lures → V0 → Nexuses → Emission
- TSK tracking: Full observability of transduction
- User experience: Resonant, attuned, intelligent responses
- Architecture: True Whiteheadian process philosophy

**Next Action:** Implement Phase C1 (Nexus Formation Enhancement)

---

**Roadmap Created:** November 13, 2025
**Target Completion:** Phase C1-C2 this week, C3 next week
**Status:** 🔧 READY FOR IMPLEMENTATION
