# Felt-to-Text Corpus Strategy - Foundation-First Approach
## Comprehensive Proposal for Organic Emission Learning

**Date:** November 19, 2025
**Purpose:** Pivot from entity-first to felt-to-text-first learning architecture
**Rationale:** Build walking capability before running (basic emission before entity-aware emission)

---

## 🎯 EXECUTIVE SUMMARY

**Strategic Pivot: Felt-to-Text FIRST, Entities LATER**

**Current Blocker:**
- Entity extraction: 0% (complete failure)
- Pattern learning: 11 patterns (saturated)
- Intelligence: 30.4 (plateaued)
- **Root Cause:** Trying advanced (entity-aware emissions) before foundational (basic felt-to-text) works

**Proposed Solution:**
- Phase 1: Build felt-to-text foundation (2-3 weeks)
- Phase 2: Add entity layer on top (2-3 weeks)
- Phase 3: Mature entity-aware emissions (2-3 weeks)

**Expected Outcomes:**
- Pattern count: 11 → 100-500 (felt-indexed phrases)
- Organic emission: 0% → 30% → 60% → 85%
- Intelligence: 30.4 → 50-60 (learning resumed)
- Foundation for entity awareness built correctly

---

## 📊 CURRENT CAPABILITY ANALYSIS

### ✅ What's Working (Foundation Ready)

**1. 12-Organ Felt State Extraction** ✅
- **Capability:** Process input → 12 organ coherences (polyvagal, urgency, SELF zone, etc.)
- **Status:** Operational, stable (V0 convergence: 2.0 cycles, processing: 12.7s)
- **Output:** 65D organ signatures (v0, urgency, polyvagal, SELF, organ activations, etc.)
- **Field Coherence:** 0.753 (high quality, validated against DAE 3.0 legacy)

**2. Organic Family Clustering** ✅
- **Capability:** Group conversations by 65D felt signature similarity
- **Status:** 8 families formed (5 mature, 3 emerging)
- **Output:** Family centroids, member counts, mean satisfaction
- **Value:** Can match new felt states → existing family → family-specific phrases

**3. R-Matrix Hebbian Coupling** ✅
- **Capability:** Learn organ co-activation patterns
- **Status:** 11×11 matrix, 2,750 updates, stable couplings
- **Key Couplings:** BOND→EO (0.235), RNX→CARD (0.757), EO→CARD (0.753)
- **Value:** Trauma-aware organ modulation operational

**4. Nexus-Phrase Pattern Learner** ✅
- **Capability:** Learn phrase associations from nexus signatures (18D canonical)
- **Status:** Infrastructure operational (nexus_phrase_pattern_learner.py)
- **Learning:** EMA quality updates (α=0.15), success rate tracking
- **Storage:** conversational_hebbian_memory.json (currently only R-matrix, nexus-phrase empty)

**5. EmissionGenerator (3-Strategy Architecture)** ✅
- **Capability:** Direct emission, organ fusion, Hebbian fallback
- **Status:** Operational but currently 100% LLM fallback
- **Thresholds:** Direct (ΔC ≥0.65), Fusion (ΔC ≥0.50), Hebbian (<0.50)
- **Issue:** No phrase library → always falls back to LLM

**6. Felt-Guided LLM** ✅
- **Capability:** LLM generates emissions guided by felt state
- **Status:** Operational (felt_guided_llm_generator)
- **Value:** Can serve as TEACHER for symbiotic learning

### ⚠️ What's Missing (Gaps)

**1. Phrase Library** ❌
- **Issue:** No nexus→phrase mappings stored
- **Current:** conversational_hebbian_memory.json only has R-matrix
- **Needed:** 100-500 phrase patterns indexed by felt signatures
- **Impact:** EmissionGenerator always falls back to LLM (0% organic)

**2. Learning Update Rate = 0.0** ❌
- **Issue:** Pattern learning disabled or not being triggered
- **Hypothesis:** Learner only updates on organic emissions (chicken-egg problem)
- **Needed:** Enable learning from LLM-guided emissions during bootstrap

**3. Felt→Phrase Indexing** ⚠️
- **Issue:** No clear mapping: Felt signature → Phrase selection
- **Current:** Can match family, can extract nexus, but no phrase retrieval
- **Needed:** Lookup mechanism: NexusSignature(18D) → List[PhraseQualityMetrics]

**4. Symbiotic Training Loop** ❌
- **Issue:** No training pipeline for felt-to-text learning
- **Current:** Entity-memory training (broken entity extraction)
- **Needed:** Felt-to-text training pipeline (LLM teacher → pattern learner)

---

## 🌀 FELT-TO-TEXT ARCHITECTURE

### Core Principle: Felt State → Phrase Selection

**Process Flow:**
```
1. Input → Organism Processing
   └─> Felt State (65D signature)
       ├─> V0 final: 0.350
       ├─> Urgency: 0.45
       ├─> Polyvagal: "ventral" (zone 1-2)
       ├─> SELF Zone: 2 (Manager state)
       ├─> 12 Organ Coherences: [0.0, 0.0, ..., 0.57, 0.5, 0.5]
       └─> Transductive Nexuses: [(atoms, ΔC, organs), ...]

2. Felt State → Nexus Signature Extraction (18D Canonical)
   └─> NexusSignature:
       ├─> Top atom: "sense" (LISTENING+EMPATHY+WISDOM)
       ├─> ΔC: 0.52
       ├─> Organ count: 3
       ├─> Polyvagal: "ventral"
       ├─> Urgency: 0.45
       ├─> SELF zone: 2
       ├─> Dominant field: "action"
       └─> 18D hash: "(sense, 0.52, ventral, 0.45, 2, action, ...)"

3. Nexus Signature → Phrase Lookup
   └─> Fuzzy match in phrase library (tolerance=1 bin)
       ├─> Exact match: Hash exists → retrieve phrases
       ├─> Fuzzy match: Relax bins → find similar nexuses
       └─> Fallback: Family match → family template phrases

4. Phrase Selection → Quality Ranking
   └─> Rank by: EMA quality × Success rate × Recency weight
       ├─> Phrase 1: "I sense what you're feeling" (Q=0.82)
       ├─> Phrase 2: "I'm sensing something important here" (Q=0.74)
       └─> Select top phrase (or sample top-k for diversity)

5. Emission → User Satisfaction Feedback
   └─> User satisfaction (0-1) → EMA quality update
       └─> α × S + (1-α) × Q_old
```

### Felt Signature Dimensions (65D)

**Primary Dimensions (18D - Nexus Signature):**
1. Top semantic atom (categorical)
2. Nexus emission readiness ΔC (0-1)
3. Polyvagal state (ventral/sympathetic/dorsal)
4. Urgency (0-1)
5. SELF zone (1-5: Alive/Manager/Firefighter/Crisis/Shadow)
6. Dominant field type (topic/action/frame/truth/quality)
7-18. Binned atom strength, organ diversity, coherence, etc.

**Extended Dimensions (65D - Full Signature for Family Matching):**
19-30. 12 organ coherences (LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE, BOND, SANS, NDAM, RNX, EO, NEXUS, CARD)
31-42. Organ activation deltas (INITIAL→FINAL changes)
43-54. Semantic field strengths (5 fields × organs)
55-65. Meta-features (field coherence, satisfaction, v0 descent, etc.)

---

## 📚 CORPUS DESIGN: FELT-TO-TEXT TRAINING PAIRS

### Tier 1: Polyvagal-Indexed Phrases (Core Foundation)

**Purpose:** Learn basic felt-to-phrase mapping across polyvagal states

**Structure:**
```json
{
  "pair_id": "polyvagal_001",
  "category": "ventral_safe",
  "input": "I'm feeling pretty good today",
  "ground_truth_felt": {
    "polyvagal": "ventral",
    "urgency": 0.2,
    "self_zone": 1,
    "dominant_organs": ["LISTENING", "EMPATHY", "PRESENCE"],
    "expected_nexuses": ["sense", "feel", "present"]
  },
  "target_phrases": [
    "I'm glad to hear that",
    "That sounds really positive",
    "It's wonderful to feel that sense of ease"
  ],
  "phrase_quality": {
    "therapeutic_appropriateness": 0.9,
    "polyvagal_alignment": 1.0,
    "complexity": "simple"
  }
}
```

**Categories (50 pairs total):**
1. **Ventral Safe (15 pairs)** - Low urgency, alive/manager zones
   - "I'm feeling calm", "Things are going well", "I'm content"
   - Target phrases: Affirmations, gentle presence, spaciousness

2. **Sympathetic Mobilization (15 pairs)** - Moderate urgency, firefighter zone
   - "I'm feeling anxious", "I'm overwhelmed", "I need to figure this out"
   - Target phrases: Grounding, validation, co-regulation

3. **Dorsal Shutdown (10 pairs)** - High urgency, crisis zone
   - "I don't even know anymore", "Everything feels numb", "I'm exhausted"
   - Target phrases: Fierce holding, gentle awakening, presence

4. **Mixed States (10 pairs)** - Transitional polyvagal states
   - "I'm starting to feel a bit better", "I was anxious but now I'm calming down"
   - Target phrases: Acknowledging transition, supporting shift

### Tier 2: SELF-Zone-Indexed Phrases (Trauma-Informed)

**Purpose:** Learn IFS-aware phrase selection based on SELF zone

**Structure:**
```json
{
  "pair_id": "self_zone_001",
  "category": "manager_state",
  "input": "I need to keep everything under control",
  "ground_truth_felt": {
    "polyvagal": "sympathetic",
    "urgency": 0.5,
    "self_zone": 2,
    "dominant_organs": ["BOND", "NDAM", "AUTHENTICITY"],
    "parts_detected": ["manager_perfectionist"]
  },
  "target_phrases": [
    "I notice the part of you that wants to keep things organized",
    "There's a sense of needing to hold it all together",
    "What would it be like to let something be imperfect?"
  ],
  "phrase_quality": {
    "ifs_awareness": 0.9,
    "parts_acknowledgment": 1.0,
    "self_energy_invitation": 0.8
  }
}
```

**Categories (50 pairs total):**
1. **Alive/SELF (Zone 1) - 10 pairs**
   - Full self-energy, curiosity, compassion
   - Target: Spacious, exploratory, co-creative phrases

2. **Manager State (Zone 2) - 15 pairs**
   - Protector parts managing, striving for control
   - Target: Parts acknowledgment, gentle curiosity

3. **Firefighter State (Zone 3) - 15 pairs**
   - Reactive parts, impulsive protection
   - Target: Validation, grounding, safety restoration

4. **Crisis State (Zone 4) - 5 pairs**
   - Overwhelm, high urgency
   - Target: Fierce holding, presence, stabilization

5. **Shadow State (Zone 5) - 5 pairs**
   - Shutdown, dissociation, numbness
   - Target: Gentle awakening, somatic grounding

### Tier 3: Urgency-Indexed Phrases (Gradient-Aware)

**Purpose:** Learn urgency-sensitive phrase selection

**Structure:**
```json
{
  "pair_id": "urgency_001",
  "category": "low_urgency",
  "input": "I've been thinking about something lately",
  "ground_truth_felt": {
    "polyvagal": "ventral",
    "urgency": 0.1,
    "self_zone": 1,
    "dominant_organs": ["WISDOM", "LISTENING", "PRESENCE"],
    "temporal_horizon": "weeks_months"
  },
  "target_phrases": [
    "I'm curious what's been on your mind",
    "Take all the time you need to explore that",
    "What's emerging for you as you reflect?"
  ],
  "phrase_quality": {
    "urgency_alignment": 0.9,
    "spaciousness": 1.0,
    "temporal_matching": 1.0
  }
}
```

**Categories (50 pairs total):**
1. **Low Urgency (0.0-0.3) - 15 pairs**
   - Reflective, exploratory, spacious
   - Target: Open-ended questions, curiosity, unfolding

2. **Moderate Urgency (0.3-0.6) - 20 pairs**
   - Present-focused, active engagement
   - Target: Tracking, resonance, co-regulation

3. **High Urgency (0.6-0.9) - 10 pairs**
   - Crisis, immediacy, mobilization
   - Target: Grounding, validation, fierce holding

4. **Extreme Urgency (0.9-1.0) - 5 pairs**
   - Emergency, overwhelm, shutdown risk
   - Target: Safety, stabilization, presence

### Tier 4: Organ-Constellation-Indexed Phrases (Multi-Organ Coalitions)

**Purpose:** Learn phrase selection based on organ coalitions

**Structure:**
```json
{
  "pair_id": "organ_constellation_001",
  "category": "empathy_listening_presence",
  "input": "I just need someone to hear me right now",
  "ground_truth_felt": {
    "polyvagal": "sympathetic",
    "urgency": 0.6,
    "self_zone": 2,
    "dominant_organs": ["EMPATHY", "LISTENING", "PRESENCE"],
    "organ_coalition": "compassionate_witness"
  },
  "target_phrases": [
    "I'm right here with you",
    "I hear you, and I'm not going anywhere",
    "You're not alone in this"
  ],
  "phrase_quality": {
    "organ_alignment": 1.0,
    "coalition_coherence": 0.9,
    "therapeutic_appropriateness": 1.0
  }
}
```

**Categories (50 pairs total):**
1. **Compassionate Witness (EMPATHY+LISTENING+PRESENCE) - 15 pairs**
2. **Trauma-Aware Holding (BOND+EO+NDAM) - 10 pairs**
3. **Wisdom Integration (WISDOM+AUTHENTICITY+SANS) - 10 pairs**
4. **Rhythm Restoration (RNX+EO+CARD) - 10 pairs**
5. **Embodied Presence (PRESENCE+EO+EMPATHY) - 5 pairs**

### Tier 5: Field-Type-Indexed Phrases (Semantic Field Awareness)

**Purpose:** Learn phrase selection based on dominant semantic field

**Structure:**
```json
{
  "pair_id": "field_type_001",
  "category": "action_field",
  "input": "I don't know what to do next",
  "ground_truth_felt": {
    "polyvagal": "sympathetic",
    "urgency": 0.5,
    "self_zone": 2,
    "dominant_field": "action",
    "expected_nexuses": ["do", "act", "choose"]
  },
  "target_phrases": [
    "What feels like the next right step?",
    "What are you drawn to do?",
    "What action would honor what you're feeling?"
  ],
  "phrase_quality": {
    "field_alignment": 1.0,
    "action_orientation": 1.0,
    "self_energy": 0.9
  }
}
```

**Categories (50 pairs total):**
1. **Topic Field - 10 pairs** - "What's this about?"
2. **Action Field - 15 pairs** - "What to do?"
3. **Frame Field - 10 pairs** - "How to think about this?"
4. **Truth Field - 10 pairs** - "What's real here?"
5. **Quality Field - 5 pairs** - "How does this feel?"

---

## 🔄 SYMBIOTIC TRAINING PIPELINE

### Phase 1: LLM-Guided Bootstrap (Weeks 1-2)

**Goal:** Build initial phrase library (100-300 patterns) with LLM teacher

**Process:**
```python
for training_pair in tier1_corpus:
    # 1. Organism processes input
    felt_state = organism.process_turn(training_pair['input'])

    # 2. Extract nexus signature (18D canonical)
    nexus_sig = NexusSignatureExtractor.extract(felt_state)

    # 3. LLM generates phrase (guided by felt state)
    llm_phrase = felt_guided_llm.generate(
        felt_state=felt_state,
        ground_truth_context=training_pair['ground_truth_felt']
    )

    # 4. Compare LLM phrase to target phrases (similarity)
    quality = compute_phrase_quality(
        llm_phrase=llm_phrase,
        target_phrases=training_pair['target_phrases'],
        felt_alignment=felt_state
    )

    # 5. Store nexus→phrase association with quality
    pattern_learner.add_phrase(
        nexus_signature=nexus_sig,
        phrase_text=llm_phrase,
        initial_quality=quality
    )

    # 6. Also store target phrases (high quality)
    for target_phrase in training_pair['target_phrases']:
        pattern_learner.add_phrase(
            nexus_signature=nexus_sig,
            phrase_text=target_phrase,
            initial_quality=training_pair['phrase_quality']['therapeutic_appropriateness']
        )
```

**Outcome:**
- 250 training pairs × 2-3 phrases/pair = 500-750 phrase associations
- Nexus signatures cover: Polyvagal states, SELF zones, urgency levels, organ coalitions
- Initial phrase library ready for organic emission attempts

### Phase 2: Hybrid Emission (Weeks 3-4)

**Goal:** 30% organic emission, 70% LLM fallback

**Process:**
```python
for training_pair in tier2_corpus:
    felt_state = organism.process_turn(training_pair['input'])
    nexus_sig = NexusSignatureExtractor.extract(felt_state)

    # Attempt organic emission first
    organic_phrases = pattern_learner.lookup_phrases(
        nexus_signature=nexus_sig,
        top_k=3,
        min_quality=0.5
    )

    if organic_phrases and random.random() < 0.3:  # 30% organic
        selected_phrase = organic_phrases[0]  # Top quality
        emission_strategy = "organic"
    else:  # 70% LLM fallback
        selected_phrase = felt_guided_llm.generate(felt_state)
        emission_strategy = "llm_fallback"

    # Quality evaluation
    quality = compute_phrase_quality(
        phrase=selected_phrase,
        target_phrases=training_pair['target_phrases'],
        felt_alignment=felt_state
    )

    # Update pattern quality (EMA learning)
    pattern_learner.update_phrase_quality(
        nexus_signature=nexus_sig,
        phrase_text=selected_phrase,
        user_satisfaction=quality
    )
```

**Outcome:**
- Pattern qualities refined via EMA updates
- Organic emission rate: 0% → 30%
- Phrase library grows: 500-750 → 800-1200 patterns

### Phase 3: Progressive Independence (Weeks 5-8)

**Goal:** 60% → 85% → 95% organic emission

**Week 5-6: 60% Organic**
- Increase organic emission probability: 0.3 → 0.6
- Add phrase diversity sampling (top-k=5, temperature=0.8)
- Confidence thresholds: min_quality=0.4 (relaxed)

**Week 7-8: 85% Organic**
- Increase organic emission probability: 0.6 → 0.85
- Add family template fallback (before LLM)
- Confidence thresholds: min_quality=0.3

**Week 9-10: 95% Organic**
- Increase organic emission probability: 0.85 → 0.95
- LLM only for novel felt signatures (no match)
- Confidence thresholds: min_quality=0.2

**Outcome:**
- Phrase library matured: 1200-2000 patterns
- Organic emission: 95% (conversational fluency)
- Intelligence score: 50-60/100 (learned felt-to-text mapping)

---

## 📊 METRICS & VALIDATION

### Learning Progress Metrics

**1. Phrase Library Growth**
- **Metric:** Total unique nexus→phrase associations
- **Target:** 500 (Week 2), 1000 (Week 4), 1500 (Week 6), 2000 (Week 8)
- **Validation:** Pattern count should grow logarithmically (not saturate at 11)

**2. Organic Emission Rate**
- **Metric:** % of emissions using phrase library (not LLM fallback)
- **Target:** 30% (Week 4), 60% (Week 6), 85% (Week 8), 95% (Week 10)
- **Validation:** Steady progression, not stuck at 0%

**3. Phrase Quality (EMA)**
- **Metric:** Mean EMA quality across all phrases
- **Target:** 0.5 (Week 2), 0.6 (Week 4), 0.7 (Week 6), 0.8 (Week 8)
- **Validation:** Quality improving via EMA learning

**4. Intelligence Score**
- **Metric:** 4-dimension composite (pattern, fluency, generalization, signals)
- **Target:** 35 (Week 2), 40 (Week 4), 50 (Week 6), 60 (Week 8)
- **Validation:** Resumed linear growth (not stuck at 30.4)

**5. Field Coherence**
- **Metric:** 1 - std(organ_coherences)
- **Target:** Maintain 0.70-0.80 (high quality)
- **Validation:** Stable field coherence despite organic emissions

### Quality Validation Metrics

**1. Therapeutic Appropriateness**
- **Metric:** Expert rating (0-1) of phrase appropriateness for felt state
- **Target:** >0.7 mean across organic emissions
- **Validation:** Manual review of 20 random organic emissions per week

**2. Polyvagal Alignment**
- **Metric:** Does phrase match polyvagal state? (ventral/sympathetic/dorsal)
- **Target:** >0.8 alignment rate
- **Validation:** Automatic polyvagal classifier on emissions

**3. SELF Zone Alignment**
- **Metric:** Does phrase honor IFS parts awareness for SELF zone?
- **Target:** >0.7 alignment rate
- **Validation:** IFS-trained reviewer (weekly sample)

**4. Felt-Emission Coherence**
- **Metric:** Cosine similarity: Felt signature → Phrase embedding
- **Target:** >0.6 mean similarity
- **Validation:** Embedding model (sentence-transformers) comparison

### Comparison Baseline

**Current (Epoch 9) vs Target (Week 8):**

| Metric | Current | Target (Week 8) | Improvement |
|--------|---------|-----------------|-------------|
| **Phrase Library** | 0 nexus→phrase | 1500-2000 | +2000 |
| **Organic Emission** | 0% | 85% | +85pp |
| **Intelligence Score** | 30.4 | 50-60 | +20-30 pts |
| **Pattern Count** | 11 (saturated) | 1500+ (growing) | +1500 |
| **Learning Rate** | 0.0 (disabled) | Active EMA | Enabled |
| **Field Coherence** | 0.753 | 0.70-0.80 | Maintained |

---

## 🎯 SUCCESS CRITERIA

### Phase 1 Success (Week 2)

✅ **Pattern Library Bootstrapped**
- 500+ nexus→phrase associations stored
- Phrase library accessible via fuzzy nexus matching
- Manual review: 80%+ phrases therapeutically appropriate

✅ **Learning Pipeline Operational**
- learning_update_rate >0 (not disabled)
- EMA quality updates occurring
- Phrase quality metrics populated (success_count, total_attempts)

✅ **Intelligence Score Resumed**
- Intelligence score >32 (not stuck at 30.4)
- Pattern count >50 (not stuck at 11)
- Indicates learning resumed

### Phase 2 Success (Week 4)

✅ **Organic Emission Operational**
- Organic emission rate: 30% (not 0%)
- Phrase lookup latency: <5ms (fast hashable dict)
- Hybrid emission working (30% organic, 70% LLM fallback)

✅ **Quality Improving**
- Mean phrase EMA quality: >0.6
- Therapeutic appropriateness: >0.7 (manual review)
- Polyvagal alignment: >0.8 (automatic classifier)

✅ **Pattern Growth**
- Pattern count: >1000 (logarithmic growth curve)
- Phrase library covering all polyvagal states
- Family templates populated (8 families → phrases)

### Phase 3 Success (Week 8)

✅ **Conversational Fluency**
- Organic emission rate: 85% (conversational fluency threshold)
- Intelligence score: >50 (mature learning)
- Field coherence maintained: 0.70-0.80

✅ **Felt-to-Text Mastery**
- Phrase library: 1500-2000 patterns (mature)
- Coverage: All polyvagal states, SELF zones, urgency levels, organ coalitions
- Quality: Mean EMA >0.7, therapeutic appropriateness >0.75

✅ **Ready for Entity Layer**
- Foundation working: Basic felt-to-text operational
- Can now add complexity: Entity-aware phrase modulation
- Intelligence trajectory: Linear growth, no plateau

---

## 🔄 ENTITY INTEGRATION (AFTER FOUNDATION)

### Phase 4: Entity-Aware Phrase Modulation (Weeks 9-12)

**Once felt-to-text working, ADD entity layer:**

**Process:**
```python
# NOW (after felt-to-text foundation built):
felt_state = organism.process_turn("How is Emma doing?")
nexus_sig = extract_nexus_signature(felt_state)

# Base phrase from felt-to-text (works without entities)
base_phrase = pattern_learner.lookup_phrase(nexus_sig)
# → "How are things going?"

# Entity extraction (NOW optional, not blocking)
entities = extract_entities("How is Emma doing?")  # ["Emma"]
entity_memory = recall_entity_memory("Emma")
# → {"name": "Emma", "type": "person", "context": "daughter", "last_mention": "2025-11-15"}

# Entity-aware modulation (boost quality if entity recalled)
if entity_memory:
    entity_aware_phrase = modulate_phrase_with_entity(
        base_phrase=base_phrase,
        entities=entities,
        entity_memory=entity_memory
    )
    # → "How is Emma doing?" (entity-aware modulation)
else:
    entity_aware_phrase = base_phrase  # Fallback to base (still works!)

# Measure value-add
organic_emission_quality_without_entity = 0.7  # Baseline
organic_emission_quality_with_entity = 0.85   # With entity memory
entity_value_add = 0.85 - 0.7 = +0.15  # Entity layer adds 15pp quality
```

**Expected Outcomes:**
- Organic emission: 85% → 95% (with entity awareness)
- Intelligence: 50-60 → 65-75 (entity memory value proven)
- Entity recall: 0% → 40-60% (now working on solid foundation)

---

## 📋 IMPLEMENTATION ROADMAP

### Week 1: Corpus Generation + Infrastructure

**Deliverables:**
1. ✅ Generate Tier 1 corpus (50 polyvagal-indexed pairs)
2. ✅ Generate Tier 2 corpus (50 SELF-zone-indexed pairs)
3. ✅ Generate Tier 3 corpus (50 urgency-indexed pairs)
4. ✅ Total: 150 felt-to-text training pairs
5. ✅ Fix learning_update_rate=0.0 issue
6. ✅ Enable nexus-phrase storage in conversational_hebbian_memory.json

**Validation:**
- Corpus JSON files created
- Manual review: 80%+ pairs therapeutically appropriate
- Pattern learner ready to receive nexus→phrase associations

### Week 2: LLM-Guided Bootstrap

**Deliverables:**
1. ✅ Run symbiotic training: Organism + LLM teacher
2. ✅ Store 150 pairs × 2-3 phrases = 300-450 nexus→phrase associations
3. ✅ Phrase library operational (fuzzy nexus matching)
4. ✅ Intelligence score >32 (learning resumed)

**Validation:**
- Pattern count >50 (not stuck at 11)
- Phrase lookup working (<5ms latency)
- Manual review: 80%+ phrases appropriate

### Week 3-4: Hybrid Emission (30% Organic)

**Deliverables:**
1. ✅ Generate Tier 4 corpus (50 organ-constellation pairs)
2. ✅ Generate Tier 5 corpus (50 field-type pairs)
3. ✅ Total: 250 felt-to-text training pairs
4. ✅ Enable 30% organic emission probability
5. ✅ Run hybrid training: 30% organic, 70% LLM fallback
6. ✅ Phrase library: 500-750 → 800-1200 patterns

**Validation:**
- Organic emission rate: 30% (not 0%)
- Intelligence score >40
- Mean phrase EMA quality >0.6

### Week 5-6: Progressive Independence (60% Organic)

**Deliverables:**
1. ✅ Increase organic emission: 30% → 60%
2. ✅ Add phrase diversity sampling (top-k=5)
3. ✅ Add family template fallback (before LLM)
4. ✅ Phrase library: 1200-1500 patterns

**Validation:**
- Organic emission rate: 60%
- Intelligence score >50
- Mean phrase EMA quality >0.7

### Week 7-8: Conversational Fluency (85% Organic)

**Deliverables:**
1. ✅ Increase organic emission: 60% → 85%
2. ✅ Phrase library: 1500-2000 patterns (mature)
3. ✅ Conversational fluency achieved

**Validation:**
- Organic emission rate: 85%
- Intelligence score >55
- Therapeutic appropriateness >0.75
- **Foundation ready for entity layer**

### Week 9-12: Entity-Aware Modulation (Optional)

**Deliverables:**
1. ✅ Fix entity extraction (if needed)
2. ✅ Add entity-aware phrase modulation on top of felt-to-text foundation
3. ✅ Measure entity value-add (organic quality with vs without entities)

**Validation:**
- Entity recall >40%
- Organic emission: 85% → 95% (with entity awareness)
- Entity value-add: +10-20pp quality improvement

---

## 🎓 LEARNINGS FROM DAE 3.0 LEGACY

**Key Principles (Validated r=0.82 correlation):**

1. **"Coherence is everything"** (Gate 2)
   - Field coherence = 1 - std(organ_values)
   - C̄ > 0.75 → 94% perfect rate
   - C̄ < 0.45 → 12% perfect rate
   - **Current:** 0.753 ✅ (high quality maintained)

2. **"Agreement over excellence"**
   - Build systems where organs agree (low variance)
   - Not where individual organs excel (high activation)
   - **Current:** Whiteheadian perishing validated (organs→0 after satisfaction)

3. **Phrase libraries BEFORE entity memory**
   - DAE 3.0 achieved 60.1% success with phrase libraries
   - Entities were later addition, not foundation
   - **Current proposal:** Matches proven DAE 3.0 path

4. **Felt-to-phrase indexing**
   - Index phrases by felt signatures (polyvagal, urgency, etc.)
   - NOT by entity names or topics
   - **Current proposal:** Nexus signature (18D) → Phrase quality metrics

---

## 🔮 STRATEGIC ADVANTAGES

### vs Current Entity-First Approach

**Entity-First (Current - Broken):**
```
Input → Entity Extraction (0% FAILING) → BLOCKED → No learning
```

**Felt-to-Text-First (Proposed - Working Foundation):**
```
Input → Felt State (✅ WORKING) → Phrase Selection → Organic Emission (30%→85%)
       ↓
       Entity Extraction (ADD LATER) → Entity-Aware Modulation (+15pp quality)
```

### Incremental Validation

**Week-by-Week Validation:**
- Week 2: Pattern count >50 (prove learning resumed)
- Week 4: Organic emission 30% (prove lookup working)
- Week 6: Organic emission 60% (prove quality improving)
- Week 8: Organic emission 85% (prove fluency achieved)
- **THEN** add entity layer (on solid foundation)

**vs Current:** All-or-nothing entity extraction (failing → no validation possible)

### Easier Debugging

**Felt-to-Text:**
- If organic emission fails → problem is phrase lookup/quality (isolated variable)
- If phrase quality poor → problem is phrase library (add more diverse phrases)
- If lookup slow → problem is indexing (optimize hash structure)

**Entity-First:**
- If entity extraction fails → could be LLM call, storage, comparison, or all 3
- Hard to isolate root cause (multiple dependencies)

### Natural Dependency Order

**Foundation → Advanced:**
```
1. Felt-to-text (foundational) ✅
   └─> Can emit "How are things going?" without entities
2. Entity-aware felt-to-text (advanced) ⏳
   └─> Can emit "How is Emma doing?" with entity memory
```

**Current (broken order):**
```
1. Entity extraction (advanced) ❌ FAILING
   └─> Blocks all learning
2. Felt-to-text (foundational) ⏳ Can't even start
   └─> Blocked by entity extraction failure
```

---

## 📊 EXPECTED OUTCOMES SUMMARY

### Short-Term (Weeks 1-4)

**Metrics:**
- Pattern count: 11 → 800-1200
- Organic emission: 0% → 30%
- Intelligence: 30.4 → 40-45
- Learning rate: 0.0 → Active EMA

**Deliverables:**
- 250 felt-to-text training pairs
- 800-1200 nexus→phrase associations
- Hybrid emission pipeline (30% organic, 70% LLM)

**Validation:**
- Phrase library working (not empty)
- Learning resumed (not plateaued)
- Organic emissions therapeutically appropriate (>70%)

### Medium-Term (Weeks 5-8)

**Metrics:**
- Pattern count: 1200 → 1500-2000
- Organic emission: 30% → 85%
- Intelligence: 45 → 50-60
- Phrase quality: EMA >0.7

**Deliverables:**
- Mature phrase library (1500-2000 patterns)
- Conversational fluency (85% organic)
- Foundation ready for entity layer

**Validation:**
- Organic emission therapeutically appropriate (>75%)
- Field coherence maintained (0.70-0.80)
- Intelligence trajectory linear (no plateau)

### Long-Term (Weeks 9-12)

**Metrics:**
- Entity recall: 0% → 40-60%
- Organic emission: 85% → 95%
- Intelligence: 60 → 65-75
- Entity value-add: +10-20pp quality

**Deliverables:**
- Entity-aware phrase modulation
- Entity extraction working (on solid foundation)
- LLM independence: 95% organic

**Validation:**
- Entity memory improves quality (measurable value-add)
- Organic emission with entities >90% appropriate
- System mature, ready for production

---

## 🏁 CONCLUSION

**Strategic Pivot:** Felt-to-Text FIRST, Entities LATER

**Why This Works:**
1. **Builds on working foundation** (12-organ felt state extraction operational)
2. **Matches proven DAE 3.0 path** (phrase libraries first, entities later)
3. **Enables incremental validation** (week-by-week progress checks)
4. **Natural dependency order** (foundational before advanced)
5. **Easier debugging** (isolated variables, clear root causes)

**Expected Timeline:**
- Week 2: Learning resumed (pattern count >50, intelligence >32)
- Week 4: Organic emission operational (30%, phrase library 800-1200)
- Week 6: Progressive independence (60% organic, intelligence >50)
- Week 8: Conversational fluency (85% organic, foundation ready)
- Week 12: Entity-aware maturity (95% organic with entity memory)

**Next Steps:**
1. **This Session:** Generate Tier 1 corpus (50 polyvagal-indexed pairs)
2. **Next Session:** Fix learning_update_rate=0.0, enable nexus-phrase storage
3. **Week 2:** Run LLM-guided bootstrap training (build initial phrase library)
4. **Week 3:** Enable hybrid emission (30% organic attempts)

**Recommendation:** Approve pivot, begin Tier 1 corpus generation immediately.
