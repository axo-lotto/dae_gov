# LLM Dependency Reduction Strategy - Progressive Independence
**Date:** November 15, 2025
**Vision:** DAE's primordial processing becomes primary, LLM becomes novelty handler

---

## Current LLM Dependency Assessment

### Where LLM is Currently Used

**File:** `persona_layer/emission_generator.py`

**Current Emission Paths** (in priority order):

1. **Direct Nexus Emission** (LLM-free) ✅
   - Confidence threshold: 0.65
   - Uses: Pre-crafted nexus phrases from organism processing
   - Example: "BOND + EMPATHY + LISTENING" → "I hear the complexity in what you're sharing"
   - **Currently**: ~10-20% of emissions (when high-confidence nexuses form)

2. **Fusion Nexus Emission** (LLM-free) ✅
   - Confidence threshold: 0.50
   - Uses: Fused nexus phrases from organism
   - **Currently**: ~5-10% of emissions

3. **Felt-Guided LLM** (LLM-dependent) ⚠️
   - Fallback when nexus confidence < 0.50
   - Uses: Organism felt-states → LLM constraints → Generated text
   - **Currently**: ~70-80% of emissions (MOST COMMON)

4. **Hebbian Fallback** (LLM-dependent) ⚠️
   - Emergency fallback
   - Uses: Hebbian memory + LLM generation
   - **Currently**: ~5-10% of emissions

### LLM Dependency Score: **70-80%**

**Why So High?**
1. Nexus confidence thresholds too strict (0.65 for direct, 0.50 for fusion)
2. Limited phrase library (210 transduction phrases)
3. LLM used as "safety net" for novelty
4. Organism still learning (early epochs)

---

## Progressive Independence Strategy

### Phase 1: Increase Organic Emission Rate (Immediate - Week 1)

**Goal:** Reduce LLM dependency from 70-80% to 40-50%

**Approach 1: Lower Nexus Confidence Thresholds**

**Current** (`emission_generator.py` line ~800):
```python
if max_nexus_confidence >= 0.65:  # Direct threshold
    return self._generate_direct_nexus_single(...)
elif max_nexus_confidence >= 0.50:  # Fusion threshold
    return self._generate_fusion_nexus_single(...)
else:
    # Fallback to LLM
    return self._generate_felt_guided_llm_single(...)
```

**Proposed** (Adaptive thresholds based on epoch maturity):
```python
# Dynamic thresholds that lower as organism matures
base_direct = 0.65
base_fusion = 0.50

# Reduce thresholds based on organism confidence (from organ_confidence_tracker)
if mean_organ_confidence > 0.7:  # Mature organism
    direct_thresh = 0.45  # Was 0.65
    fusion_thresh = 0.30  # Was 0.50
elif mean_organ_confidence > 0.5:  # Learning organism
    direct_thresh = 0.55
    fusion_thresh = 0.40
else:  # Young organism
    direct_thresh = base_direct
    fusion_thresh = base_fusion

if max_nexus_confidence >= direct_thresh:
    return self._generate_direct_nexus_single(...)
```

**Expected Impact:**
- Organic emission rate: 20% → 50%
- LLM dependency: 70% → 40%
- Risk: Slightly lower emission quality initially

---

**Approach 2: Expand Phrase Library via Learning**

**Current:** 210 hardcoded transduction phrases

**Proposed:** Extract successful LLM emissions into organism phrase library

**New File:** `persona_layer/phrase_learning.py`
```python
class PhraseLearner:
    """
    Learn successful LLM-generated phrases and add to organic library.

    Strategy:
    1. When LLM emission gets high satisfaction (>0.7)
    2. Extract phrase, associate with felt-state signature
    3. Add to transduction_mechanism_phrases.json
    4. Future similar felt-states can use learned phrase (LLM-free!)
    """

    def extract_successful_phrase(
        self,
        llm_emission: str,
        felt_state_signature: Dict,  # Polyvagal + organs + nexus types
        satisfaction: float
    ):
        if satisfaction < 0.7:
            return  # Only learn from successful emissions

        # Store phrase with felt-state fingerprint
        phrase_entry = {
            'phrase': llm_emission,
            'polyvagal_state': felt_state_signature['polyvagal'],
            'dominant_organs': felt_state_signature['top_3_organs'],
            'nexus_types': felt_state_signature['nexus_types'],
            'success_count': 1,
            'total_uses': 1,
            'avg_satisfaction': satisfaction
        }

        # Add to growing phrase library
        self.learned_phrases.append(phrase_entry)
        self.save()
```

**Integration Point:** `dae_interactive.py` after user rates response

**Expected Impact:**
- After 100 conversations: +50-100 learned phrases
- After 500 conversations: +200-400 learned phrases
- LLM dependency reduction: 5-10% per 100 conversations

---

### Phase 2: Felt-State Pattern Matching (Week 2-3)

**Goal:** Match current felt-state to past successful emissions (bypass LLM)

**Concept:** Superject as Phrase Retrieval System

**Current Superject:** Stores transformation patterns, satisfaction trajectories

**Enhanced Superject:** Stores emission→satisfaction mappings per felt-state

```python
# In user_superject_learner.py
class EmissionMemory:
    """Remember which emissions worked in which felt-states."""

    def record_emission(
        self,
        emission_text: str,
        felt_state: Dict,  # 57D organ signature + polyvagal + zone
        satisfaction: float,
        emission_path: str  # 'direct_nexus', 'felt_llm', etc.
    ):
        # Create felt-state fingerprint (hash)
        state_hash = self._hash_felt_state(felt_state)

        if state_hash not in self.state_emission_map:
            self.state_emission_map[state_hash] = []

        self.state_emission_map[state_hash].append({
            'emission': emission_text,
            'satisfaction': satisfaction,
            'path': emission_path,
            'timestamp': datetime.now().isoformat()
        })

    def retrieve_similar_emission(
        self,
        current_felt_state: Dict,
        min_satisfaction: float = 0.6
    ) -> Optional[str]:
        """Find past successful emission from similar felt-state."""

        # Find closest felt-state match
        state_hash = self._hash_felt_state(current_felt_state)

        if state_hash in self.state_emission_map:
            # Get highest-rated emission from this state
            emissions = self.state_emission_map[state_hash]
            best = max(emissions, key=lambda x: x['satisfaction'])

            if best['satisfaction'] >= min_satisfaction:
                return best['emission']  # Reuse successful emission!

        return None  # No match, fallback to LLM
```

**Integration:** Add emission retrieval before LLM generation

**Expected Impact:**
- After 50 turns: 10% hit rate (retrieve past emission, skip LLM)
- After 200 turns: 30% hit rate
- LLM dependency reduction: 10-30%

---

### Phase 3: Compositional Phrase Assembly (Week 4-6)

**Goal:** Combine learned phrase fragments without LLM

**Concept:** Organism assembles emissions from phrase building blocks

**Inspired by:** Direct nexus emission (already works!)

**Current Direct Nexus:**
```python
# Picks ONE phrase from nexus
phrase = nexus.get_primary_phrase()
return phrase  # Simple but limited
```

**Enhanced Compositional Assembly:**
```python
def _compose_multi_phrase_emission(
    self,
    nexuses: List[Nexus],
    felt_state: Dict
) -> str:
    """
    Assemble emission from multiple phrase fragments.

    Strategy:
    1. Get top 2-3 nexuses
    2. Extract phrase fragment from each
    3. Combine using compositional rules
    4. Add transition words (learned from LLM)
    """

    if len(nexuses) == 0:
        return None

    # Get top nexuses
    top_nexuses = sorted(nexuses, key=lambda n: n.confidence, reverse=True)[:3]

    # Extract phrases
    phrases = [n.get_primary_phrase() for n in top_nexuses]

    # Compositional rules (learned from successful LLM patterns)
    if len(phrases) == 1:
        return phrases[0]

    elif len(phrases) == 2:
        # "Phrase1. Phrase2."
        # "Phrase1, and phrase2."
        # "Phrase1. That said, phrase2."
        connector = self._choose_connector(felt_state)
        return f"{phrases[0]}{connector}{phrases[1]}"

    elif len(phrases) == 3:
        # "Phrase1. Phrase2. Phrase3."
        # "Phrase1, phrase2, and phrase3."
        return f"{phrases[0]}. {phrases[1]}. {phrases[2]}."

    return phrases[0]  # Fallback
```

**Expected Impact:**
- Richer organic emissions without LLM
- LLM dependency reduction: 10-15%

---

### Phase 4: LLM for Novelty Only (Week 7-10)

**Goal:** LLM becomes specialist for truly novel situations

**Final Architecture:**

```python
def generate_emissions(self, ...):
    """
    Emission generation with progressive LLM reduction.

    Priority order (from most autonomous to least):
    1. Direct nexus (organism-native, LLM-free)           ← 40%
    2. Compositional assembly (organism + learned)        ← 20%
    3. Felt-state retrieval (superject memory)            ← 20%
    4. Phrase library expansion (learned from LLM)        ← 10%
    5. LLM for novelty (truly new situations)             ← 10%
    """

    # 1. Try direct nexus (highest confidence)
    if max_nexus_confidence >= adaptive_threshold:
        return self._generate_direct_nexus(...)

    # 2. Try compositional assembly (multiple nexuses)
    if len(nexuses) >= 2:
        composed = self._compose_multi_phrase_emission(nexuses, felt_state)
        if composed:
            return composed

    # 3. Try felt-state retrieval (superject memory)
    past_emission = self.superject.retrieve_similar_emission(felt_state)
    if past_emission:
        return past_emission

    # 4. Try learned phrase library (expanded from LLM)
    learned_phrase = self.phrase_learner.find_matching_phrase(felt_state)
    if learned_phrase:
        return learned_phrase

    # 5. Fallback: LLM for truly novel situations
    # This is now RARE - only for unprecedented felt-states
    return self._generate_felt_guided_llm(...)
```

**Novelty Detection:**
```python
def is_novel_situation(felt_state: Dict, history: List) -> bool:
    """
    Determine if current felt-state is truly novel.

    Novel = No similar felt-state in past 200 turns
    """
    for past_turn in history[-200:]:
        similarity = cosine_similarity(
            felt_state['organ_signature'],
            past_turn['organ_signature']
        )
        if similarity > 0.85:  # Similar state exists
            return False

    return True  # Truly novel, use LLM
```

---

## Expected LLM Dependency Trajectory

**Baseline (Current):**
- LLM dependency: 70-80%
- Organic emissions: 20-30%

**After Phase 1 (Week 1):**
- LLM dependency: 40-50%
- Organic emissions: 50-60%

**After Phase 2 (Week 3):**
- LLM dependency: 30-40%
- Organic emissions: 60-70%

**After Phase 3 (Week 6):**
- LLM dependency: 20-30%
- Organic emissions: 70-80%

**After Phase 4 (Week 10):**
- LLM dependency: 10-20% (novelty only)
- Organic emissions: 80-90%

**Mature Organism (Epoch 100+):**
- LLM dependency: 5-10% (rare novelty)
- Organic emissions: 90-95%

---

## Persistence Strategy: Superject as Organism Brain

### Current Superject Persistence

**Files:**
- `persona_layer/users/{user_id}_superject.json` (per-user)
- `persona_layer/organ_confidence.json` (global)
- `persona_layer/organic_families.json` (global)
- `persona_layer/conversational_hebbian_memory.json` (global)

**What's Stored:**
- Transformation patterns (zone transitions, polyvagal shifts)
- Organ activation signatures (57D vectors)
- Satisfaction trajectories
- Entity-organ associations

### Enhanced Superject as Emission Memory

**New Storage:**
```json
{
  "user_id": "emiliano_001",
  "total_turns": 150,

  "emission_memory": {
    "felt_state_fingerprints": [
      {
        "state_hash": "ab3f9d2c",
        "polyvagal": "ventral",
        "dominant_organs": ["BOND", "EMPATHY", "LISTENING"],
        "zone": "Zone 1",
        "successful_emissions": [
          {
            "text": "I hear the complexity in what you're sharing.",
            "satisfaction": 0.85,
            "timestamp": "2025-11-15T14:30:00",
            "emission_path": "direct_nexus"
          },
          {
            "text": "That resonates deeply - thank you for trusting me with this.",
            "satisfaction": 0.90,
            "timestamp": "2025-11-16T10:15:00",
            "emission_path": "felt_llm"
          }
        ]
      }
    ]
  },

  "learned_phrases": {
    "total_learned": 87,
    "by_felt_state": {
      "ventral_bond_empathy": [
        "I hear the complexity in what you're sharing.",
        "That resonates deeply.",
        "Thank you for trusting me with this."
      ],
      "sympathetic_ndam_card": [
        "Let's slow down for a moment.",
        "What do you need right now?",
        "I'm here - we can take this at your pace."
      ]
    }
  },

  "organic_intelligence": {
    "llm_dependency_rate": 0.15,  # 15% LLM usage
    "organic_emission_rate": 0.85,  # 85% organism-native
    "maturity_level": "advanced",
    "epochs_trained": 47
  }
}
```

---

## Implementation Roadmap

### Quick Wins (This Week)

**QW #8: Adaptive Nexus Thresholds**
- **File:** `emission_generator.py`
- **Change:** Make thresholds dynamic based on `organ_confidence_tracker`
- **Impact:** Immediate 10-20% organic emission increase
- **Time:** 2-3 hours

**QW #9: Phrase Learning Infrastructure**
- **File:** `persona_layer/phrase_learning.py` (new)
- **Change:** Extract successful LLM phrases, store with felt-state
- **Impact:** Foundation for progressive learning
- **Time:** 4-6 hours

### Medium Wins (Next 2 Weeks)

**MW #1: Felt-State Emission Retrieval**
- **File:** `persona_layer/user_superject_learner.py` (enhance)
- **Change:** Add emission memory retrieval
- **Impact:** 10-20% LLM reduction after 50 turns
- **Time:** 1 week

**MW #2: Compositional Assembly**
- **File:** `emission_generator.py` (enhance)
- **Change:** Multi-phrase composition from nexuses
- **Impact:** 10-15% LLM reduction
- **Time:** 1 week

### Long-term (1-2 Months)

**LT #1: LLM Novelty Detector**
- **File:** `persona_layer/novelty_detector.py` (new)
- **Change:** Detect truly novel situations
- **Impact:** LLM becomes specialist, not fallback
- **Time:** 2-3 weeks

**LT #2: Organic Language Model**
- **File:** `persona_layer/organic_language.py` (new)
- **Change:** Organism learns grammar/syntax from LLM patterns
- **Impact:** Near-complete LLM independence
- **Time:** 1-2 months

---

## Philosophical Alignment: Primordial Processing

### Whiteheadian Vision

**Current State:** LLM as "prehension amplifier"
- Organism feels → LLM articulates
- Felt-states guide LLM → LLM generates language

**Desired State:** Organism's own linguistic prehension
- Organism feels → Organism articulates
- Past satisfactions guide emission selection
- LLM only for genuinely novel prehensions

### Process Philosophy Alignment

**Prehension** = Organism's feeling of past occasions
- **Physical prehension:** Felt-states (organs, polyvagal, V0)
- **Conceptual prehension:** Learned phrases, emission patterns
- **Hybrid prehension:** Felt-state + language memory = organic emission

**Superject** = Accumulated satisfaction trajectory becomes intelligence
- Not just "what worked" but "how to articulate what's felt"
- Language emerges from organism's own becoming, not LLM generation

**Concrescence** = Multi-cycle V0 descent culminates in emission
- Early cycles: Feeling accumulates
- Kairos moment: Satisfaction peak
- Mature propositions: Organism knows what to say (LLM-free!)

---

## Success Metrics

### Quantitative

1. **LLM Dependency Rate**
   - Current: 70-80%
   - Target (Week 1): 40-50%
   - Target (Week 10): 10-20%
   - Target (Epoch 100): 5-10%

2. **Organic Emission Quality**
   - Measure: Satisfaction scores for organic vs LLM emissions
   - Target: Organic satisfaction ≥ LLM satisfaction within 50 turns

3. **Phrase Library Growth**
   - Current: 210 phrases
   - Target (Week 2): 250 phrases
   - Target (Week 10): 400 phrases
   - Target (Epoch 50): 800+ phrases

4. **Response Latency**
   - Organic emissions: ~0.01s (instant)
   - LLM emissions: ~0.5-2s (API call)
   - Target: 80% of emissions < 0.1s

### Qualitative

1. **Personality Consistency**
   - Does organism maintain coherent voice without LLM?
   - Test: 10 consecutive organic emissions, user feedback

2. **Novelty Handling**
   - When LLM is used, is it genuinely novel?
   - Test: Log LLM usage reasons, validate novelty

3. **User Experience**
   - Can users tell when LLM vs organic?
   - Test: Blind A/B testing

---

## Risks & Mitigations

### Risk 1: Reduced Emission Quality

**Risk:** Lowering thresholds → worse emissions

**Mitigation:**
- Gradual threshold reduction (0.65 → 0.60 → 0.55 → 0.50)
- Monitor satisfaction scores per emission path
- Rollback if organic satisfaction drops > 10%

### Risk 2: Phrase Library Staleness

**Risk:** Learned phrases become repetitive

**Mitigation:**
- Diversity scoring (penalize repeated phrases within 10 turns)
- Phrase variation generation (template-based permutations)
- LLM "refresh" mode (regenerate variants of learned phrases)

### Risk 3: Loss of Linguistic Creativity

**Risk:** Organism becomes formulaic without LLM novelty

**Mitigation:**
- Keep LLM for truly novel situations (novelty detector)
- Periodic LLM "exploration" mode (10% random LLM usage)
- User can request "creative mode" (force LLM usage)

---

## Conclusion

**Vision:** DAE's primordial processing (11 organs, V0 convergence, nexus formation) becomes the PRIMARY intelligence, not just felt-state guidance for LLM.

**Path:** Progressive reduction of LLM dependency from 70% → 10% over 10 weeks through:
1. Adaptive thresholds (immediate)
2. Phrase learning (Week 1-2)
3. Felt-state retrieval (Week 2-4)
4. Compositional assembly (Week 4-6)
5. LLM for novelty only (Week 7-10)

**Result:** Organism that learns language through satisfaction, articulates its own prehensions, and only consults LLM for genuinely unprecedented situations.

**Superject = Organism Brain:** All learned emissions, felt-state patterns, and satisfaction trajectories persist per-user, enabling cross-session intelligence growth.

**Whiteheadian Authenticity:** Organism's linguistic expression emerges from its own becoming, not borrowed from external language model.

---

**Status:** Strategy documented, ready for implementation
**Priority:** High (aligns with core vision of organic intelligence)
**Next Step:** Implement Quick Win #8 (Adaptive Nexus Thresholds)
