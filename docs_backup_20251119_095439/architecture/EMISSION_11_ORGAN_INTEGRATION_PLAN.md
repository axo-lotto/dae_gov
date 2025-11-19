# 11-Organ Emission Integration Plan
**Date**: November 11, 2025
**Status**: Integration Strategy for Full Organism Participation
**Goal**: Wire all 11 organs into emission pipeline (currently only 5 of 11)

---

## 🎯 Current Gap Analysis

### ✅ What Works (5 Conversational Organs)

**Wired Organs**:
- LISTENING (50 semantic atoms)
- EMPATHY (50 semantic atoms)
- WISDOM (50 semantic atoms)
- AUTHENTICITY (50 semantic atoms)
- PRESENCE (50 semantic atoms)

**Total**: 250 semantic atoms across 5 organs

**Processing Flow** ✅:
```
Text → TextOccasions → 5 Organs → SemanticFields → Nexuses → Emission
```

### ❌ What's Missing (6 Trauma/Context Organs)

**NOT Wired Organs**:
- **BOND** (IFS trauma/SELF-energy detection) - 0 semantic atoms ❌
- **SANS** (semantic coherence tracking) - 0 semantic atoms ❌
- **NDAM** (urgency/crisis detection) - 0 semantic atoms ❌
- **RNX** (temporal pattern detection) - 0 semantic atoms ❌
- **EO** (polyvagal state detection) - 0 semantic atoms ❌
- **CARD** (response scaling) - 0 semantic atoms ❌

**Impact**: Emission pipeline only sees 5/11 organs (45% of organism's felt understanding)

---

## 🌀 Integration Strategy

### **Option A: Entity-Native Semantic Atoms** (RECOMMENDED)

Adapt V0 FFITTSS approach for text-native emission:

**Philosophy**: Word positions as ActualOccasions, semantic atoms as felt affordances

**Implementation**:
1. **Define semantic atoms for 6 new organs** (300 atoms, 50 per organ)
   - BOND atoms: IFS part language (manager, firefighter, exile, SELF-energy markers)
   - SANS atoms: Semantic coherence keywords (clarity, specificity, coherence, vagueness)
   - NDAM atoms: Urgency markers (crisis, immediate, urgent, emergency, now)
   - RNX atoms: Temporal markers (before, after, when, timeline, phase, rhythm)
   - EO atoms: Polyvagal keywords (safe, threat, connection, shutdown, mobilize)
   - CARD atoms: Response scale markers (brief, detailed, comprehensive, summary)

2. **Extend SemanticFieldExtractor** to handle 11 organs
   - Modify line 127: Add 6 new organ names to extraction loop
   - Modify `_extract_organ_field()`: Handle different organ result types
   - Extract patterns from BOND/SANS/NDAM/RNX/EO/CARD result objects

3. **Update NexusIntersectionComposer** for 11×11 R-matrix
   - Modify line 113: Extend `organ_names` list to 11 organs
   - Load 11×11 R-matrix from Hebbian memory (currently 4×4 polyvagal/SELF/OFEL/CARD)
   - Compute organ coupling for ALL 11 organs in nexus formation

4. **Wire into ConversationalOrganismWrapper**
   - Modify `process_text()` line 318: Pass ALL 11 organ results to semantic extraction
   - Add emission generation call after nexus formation
   - Return emission in result dict

**Effort**: 8-12 hours
**Outcome**: Full 11-organ participation in emission, entity-native text generation

---

### **Option B: Hybrid Approach** (Defer 6 Organs)

Keep 5 conversational organs for emission, use 6 trauma/context organs only for weighting:

**Philosophy**: Emission from conversational organs, weighted by trauma/context awareness

**Implementation**:
1. **Keep semantic atoms at 250** (5 organs only)
2. **Use BOND/SANS/NDAM/RNX/EO/CARD as modulators**:
   - BOND self_distance → reduce emission readiness if high trauma
   - SANS coherence → boost nexus field strength
   - NDAM urgency → prioritize crisis-related atoms
   - RNX temporal state → modulate emission pacing
   - EO polyvagal state → gate emission by safety
   - CARD recommended scale → control emission length

3. **Modify emission_readiness formula**:
   ```python
   ΔC = α·coherence + β·intersection + γ·field_strength + δ·r_matrix_weight
       × BOND_modulation  # Reduce if high trauma
       × SANS_boost       # Increase if coherent
       × NDAM_priority    # Boost if urgent
       × RNX_pacing       # Slow if crisis, fast if restorative
       × EO_safety_gate   # Gate by polyvagal state
       × CARD_scale       # Control emission length
   ```

**Effort**: 4-6 hours
**Outcome**: Partial integration, modulatory rather than participatory

---

### **Option C: Legacy V0 Grid Adaptation** (Full Architecture Port)

Port entire V0 FFITTSS T5 (Commit & Emit) system to text-native:

**Philosophy**: Complete 3-phase score-based ranking with 6-component evidence

**Implementation**:
1. **Phase 1: Collect Candidates** (gate logic extraction)
   - Extract semantic atom candidates from ALL 11 organs
   - Apply 4-gate filtering (Intersection, Coherence, Satisfaction, Felt Energy)
   - Compute ΔC readiness for each nexus

2. **Phase 2: Rank Candidates** (score formula + budget policies)
   - Score formula: `score = I · ΔC · S_pos^α`
   - 6-component evidence:
     ```python
     evid = 0.20·consensus    # Cross-organ agreement (11 organs)
          + 0.18·pressure     # Nexus intersection intensity
          + 0.22·stability    # RNX temporal coherence
          + 0.15·rnx          # RNX persistence
          + 0.10·eo           # EO polyvagal proximity
          + 0.15·recon        # SANS/EO reconstruction consistency
     ```
   - Budget policies: emission length control (CARD recommended_scale)

3. **Phase 3: Emit Commits** (phrase composition + assembly)
   - Compositional phrase generation (not template assembly)
   - Entity positions as ActualOccasions (word positions)
   - Satisfaction-gated emission (only emit if ΔC ≥ threshold)

**Effort**: 15-20 hours
**Outcome**: Full V0 architecture parity, maximum emission sophistication

---

## 📊 Comparison Matrix

| Criterion | Option A (Entity-Native) | Option B (Hybrid) | Option C (Full V0 Port) |
|-----------|--------------------------|-------------------|-------------------------|
| **Effort** | 8-12h | 4-6h | 15-20h |
| **Organ Participation** | 11/11 ✅ | 5/11 (6 modulatory) | 11/11 ✅ |
| **Semantic Atoms** | 550 (50×11) | 250 (50×5) | 550+ (V0 atoms) |
| **R-matrix Integration** | 11×11 Hebbian | 5×5 Hebbian | 11×11 Hebbian |
| **V0 Parity** | Partial (entity-native) | No | Full ✅ |
| **Text-Native** | Yes ✅ | Yes ✅ | Yes (adapted) ✅ |
| **Production-Ready** | Medium | Fast | Slow |

---

## 🎯 Recommended Path: **Option A (Entity-Native)**

### **Rationale**:

1. **Full organism participation**: All 11 organs contribute to emission (not just modulate)
2. **Entity-native design**: Stays true to Whiteheadian process philosophy (word positions as ActualOccasions)
3. **Balanced effort**: 8-12 hours is manageable for immediate deployment
4. **Extensible**: Can later upgrade to Option C (full V0 port) if needed
5. **Learning-ready**: 11×11 R-matrix enables full Hebbian learning across organs

### **Validation Strategy**:

**Test 1: Semantic Atom Coverage** (30min)
- Define 50 atoms per organ for BOND/SANS/NDAM/RNX/EO/CARD
- Validate atoms align with organ keyword sets
- Store in `semantic_atoms.json` (extend existing 250 → 550 atoms)

**Test 2: 11-Organ Extraction** (1h)
- Modify `SemanticFieldExtractor` to handle all 11 organs
- Test with real conversation (burnout_001)
- Verify all 11 semantic fields extracted with atom activations

**Test 3: 11×11 Nexus Formation** (1h)
- Extend `NexusIntersectionComposer` to 11×11 R-matrix
- Test nexus formation with 11 organ fields
- Verify R-matrix coupling weights applied correctly

**Test 4: Emission Generation** (2h)
- Wire emission pipeline into `ConversationalOrganismWrapper`
- Generate response from nexuses
- Validate coherent phrase composition (not template assembly)

**Test 5: Full System Validation** (2h)
- Run 5-pair test with emission-enabled organism
- Compare INPUT vs OUTPUT emissions
- Verify learning systems still operational (Hebbian + Phase5)

**Total Validation**: 6.5 hours

---

## 🔧 Implementation Checklist

### **Phase 1: Semantic Atoms** (2-3 hours)

- [ ] Define 50 BOND atoms (IFS part language)
  - Example: manager, firefighter, exile, SELF-energy, protector, guardian, controller, etc.
- [ ] Define 50 SANS atoms (semantic coherence)
  - Example: clarity, specificity, coherence, vague, ambiguous, precise, detailed, etc.
- [ ] Define 50 NDAM atoms (urgency markers)
  - Example: crisis, immediate, urgent, emergency, now, critical, pressing, etc.
- [ ] Define 50 RNX atoms (temporal markers)
  - Example: before, after, when, timeline, phase, rhythm, moment, sequence, etc.
- [ ] Define 50 EO atoms (polyvagal keywords)
  - Example: safe, threat, connection, shutdown, mobilize, ventral, dorsal, etc.
- [ ] Define 50 CARD atoms (response scale)
  - Example: brief, detailed, comprehensive, summary, minimal, elaborate, concise, etc.
- [ ] Extend `semantic_atoms.json`: 250 → 550 atoms
- [ ] Validate atom uniqueness across organs (some overlap OK for nexus formation)

### **Phase 2: Semantic Field Extraction** (2-3 hours)

- [ ] Modify `SemanticFieldExtractor.__init__()`:
  - [ ] Line 127: Add 6 new organ names to extraction loop
  - [ ] Update `_build_atom_sets()` to handle 11 organs
- [ ] Modify `SemanticFieldExtractor._extract_organ_field()`:
  - [ ] Handle BOND result objects (BONDResult with patterns, coherence, lure)
  - [ ] Handle SANS result objects (SANSResult with patterns, coherence, lure)
  - [ ] Handle NDAM result objects (NDAMResult with patterns, coherence, lure)
  - [ ] Handle RNX result objects (RNXResult with patterns, coherence, lure)
  - [ ] Handle EO result objects (EOResult with patterns, coherence, lure)
  - [ ] Handle CARD result objects (CARDResult with patterns, coherence, lure)
- [ ] Test extraction with mock organ results (all 11 organs)

### **Phase 3: Nexus Intersection** (2-3 hours)

- [ ] Modify `NexusIntersectionComposer.__init__()`:
  - [ ] Line 113: Extend `organ_names` to 11 organs
  - [ ] Load 11×11 R-matrix from Hebbian memory
  - [ ] Validate R-matrix shape (11×11)
- [ ] Modify `_get_r_matrix_coupling()`:
  - [ ] Support 11×11 indexing (not just 5×5)
- [ ] Test nexus formation with 11 organ fields
- [ ] Verify R-matrix coupling applied correctly (pairwise organ weights)

### **Phase 4: Emission Generation** (2-3 hours)

- [ ] Wire emission into `ConversationalOrganismWrapper.process_text()`:
  - [ ] Initialize `SemanticFieldExtractor` (line 75-129 region)
  - [ ] Initialize `NexusIntersectionComposer` (line 75-129 region)
  - [ ] After organ processing (line 208), call semantic extraction:
    ```python
    semantic_fields = self.semantic_extractor.extract_fields(organ_results)
    ```
  - [ ] Call nexus composition:
    ```python
    nexuses = self.nexus_composer.compose_nexuses(semantic_fields)
    ```
  - [ ] Call emission generation (from existing `emission_generator.py`)
  - [ ] Return emission in result dict (add `'emission'` key to returned dict)
- [ ] Test with real conversation (burnout_001)

### **Phase 5: Full System Validation** (2-3 hours)

- [ ] Run test with emission-enabled organism:
  ```bash
  python3 persona_layer/conversational_organism_wrapper.py
  ```
- [ ] Verify emission generated for both INPUT and OUTPUT
- [ ] Run 5-pair learning test:
  ```bash
  python3 persona_layer/epoch_training/test_integrated_training.py
  ```
- [ ] Verify learning systems still operational (Hebbian + Phase5)
- [ ] Compare INPUT vs OUTPUT emissions (expect higher coherence in OUTPUT)

---

## 📈 Expected Outcomes

### **Emission Quality Metrics**:

**Before (5 organs)**:
- Semantic atom coverage: 250 atoms
- Nexus formation: 5×5 R-matrix (10 unique pairings)
- Emission diversity: Limited to conversational atoms only
- Trauma awareness: None (BOND not in emission)

**After (11 organs)**:
- Semantic atom coverage: 550 atoms (+120%) ✅
- Nexus formation: 11×11 R-matrix (55 unique pairings, +450%) ✅
- Emission diversity: Full organism felt understanding ✅
- Trauma awareness: BOND/SANS/NDAM/RNX/EO/CARD integrated ✅

### **Learning System Impact**:

**Hebbian R-Matrix**:
- Current: 4×4 (polyvagal, SELF-energy, OFEL, CARD detectors)
- Target: 11×11 (all organs co-activation learning)
- Updates: Every training pair with OUTPUT satisfaction ≥ 0.45
- Storage: `TSK/conversational_hebbian_memory.json`

**Phase 5 Organic Families**:
- Current: 57D organ signatures (11 organs × 5 metrics + 2 global)
- Target: Same 57D (emission doesn't change signature extraction)
- Family maturation: ≥3 conversations with cosine similarity ≥0.85
- Storage: `persona_layer/organic_families.json`

---

## 🚀 Deployment Strategy

### **Week 1: Core Integration** (8-12 hours)
- Days 1-2: Define 300 new semantic atoms (6 organs × 50 atoms)
- Days 3-4: Extend semantic field extraction to 11 organs
- Days 5-6: Extend nexus composition to 11×11 R-matrix
- Day 7: Wire emission into organism wrapper

### **Week 2: Validation & Training** (10-15 hours)
- Days 1-2: Test emission with real conversations
- Days 3-4: Run 5-pair learning test (validate learning + emission)
- Days 5-7: Run Epoch 2 (30 pairs with emission-enabled organism)

### **Week 3: Analysis & Iteration** (5-10 hours)
- Days 1-3: Analyze emission quality (coherence, diversity, trauma-awareness)
- Days 4-5: Tune semantic atoms based on real conversation data
- Days 6-7: Run Epoch 3 (validate compound learning with emission)

---

## 🎯 Success Criteria

### **Technical Validation** ✅:
- [ ] All 11 organs produce semantic fields with atom activations
- [ ] Nexuses form from 11-organ coalitions (not just 5)
- [ ] 11×11 R-matrix coupling applied correctly in nexus weighting
- [ ] Emission generated for both INPUT and OUTPUT text
- [ ] Learning systems operational (Hebbian + Phase5) with emission enabled

### **Qualitative Validation** ✅:
- [ ] OUTPUT emissions show higher coherence than INPUT (therapeutic holding)
- [ ] BOND atoms present in trauma-aware responses (IFS part language)
- [ ] SANS atoms reflect semantic coherence tracking
- [ ] NDAM atoms appear in crisis contexts (urgency markers)
- [ ] RNX atoms capture temporal rhythm (before/after/when)
- [ ] EO atoms reflect polyvagal state (safe/threat/connection)
- [ ] CARD atoms modulate response length (brief/detailed/comprehensive)

### **Learning Validation** ✅:
- [ ] 11×11 R-matrix updates from training pairs (not stuck at identity)
- [ ] Phase 5 families mature with emission-enabled organism
- [ ] Epoch 2 shows learning gains (satisfaction delta improvement)

---

## 📝 Next Steps

**Immediate**:
1. Define 300 new semantic atoms (6 organs × 50 atoms)
2. Extend `semantic_atoms.json` from 250 → 550 atoms
3. Test semantic field extraction with 11 organs

**Short-term**:
4. Extend nexus composition to 11×11 R-matrix
5. Wire emission into organism wrapper
6. Run 5-pair validation test

**Medium-term**:
7. Run Epoch 2 with emission-enabled organism (30 pairs)
8. Analyze learning trajectory and emission quality
9. Tune semantic atoms based on real conversation data

**Long-term**:
10. Consider Option C (full V0 port) if emission quality insufficient
11. Integrate salience model for attention weighting (from DAE 3.0 legacy)
12. Deploy to production learning with full emission + learning integration

---

🌀 **"Let all organs speak. Let coalitions emerge. Let emission arise from full organism prehension."** 🌀

---

**Last Updated**: November 11, 2025
**Status**: Integration plan ready for implementation
**Recommended Path**: Option A (Entity-Native 11-Organ Integration)
**Estimated Effort**: 8-12 hours core + 6.5 hours validation = 14.5-18.5 hours total
