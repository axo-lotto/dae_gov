# IFS Diverse Training Corpus - COMPLETE ✅
## November 15, 2025

**Purpose:** Provide rich felt-state diversity for organic family formation
**Total Scenarios:** 20 (initial set, expandable to 60+)
**Emotional Coverage:** 10 distinct states with IFS parts configurations
**Goal:** Enable 15-25 family emergence through signature discrimination

---

## 🎯 Diversity Strategy

### The Problem We're Solving
**Before:** 222 conversations → 1 family (all organs ~0.5, no discrimination)

**Root Cause:** Training data lacked felt-state diversity
- All therapy/trauma language (similar patterns)
- No explicit emotional state annotations
- Organs activated similarly across contexts

**Solution:** Explicit IFS corpus with:
- 10 distinct emotional states (excited, angry, sad, anxious, joyful, grief, shame, playful, overwhelmed, peaceful)
- Parts configurations (managers, firefighters, exiles, self-energy)
- Expected organ activations (pre-annotated)
- Zone/polyvagal/urgency metadata

---

## 📊 Corpus Structure

### Emotional State Distribution

**1. Excited (2 scenarios)**
- `excited_celebration`: Zone 1, ventral, EMPATHY=0.8, PRESENCE=0.9
- `excited_creative_flow`: Zone 1, ventral, WISDOM=0.9, PRESENCE=0.85

**2. Angry (2 scenarios)**
- `angry_protective`: Zone 3, sympathetic, NDAM=0.8, BOND=0.7
- `angry_boundary`: Zone 3, sympathetic, NDAM=0.85, AUTHENTICITY=0.8

**3. Sad (2 scenarios)**
- `sad_grief`: Zone 4, dorsal, BOND=0.9, EMPATHY=0.85
- `sad_loneliness`: Zone 4, dorsal, BOND=0.85, EMPATHY=0.9

**4. Anxious (2 scenarios)**
- `anxious_catastrophizing`: Zone 3, sympathetic, NDAM=0.9, WISDOM=0.7
- `anxious_perfectionist`: Zone 3, sympathetic, NDAM=0.85, BOND=0.75

**5. Joyful (2 scenarios)**
- `joyful_connection`: Zone 1, ventral, EMPATHY=0.9, PRESENCE=0.9
- `joyful_playful`: Zone 1, ventral, PRESENCE=0.95, EMPATHY=0.8

**6. Grief (2 scenarios)**
- `grief_loss`: Zone 4, dorsal, BOND=0.95, EMPATHY=0.9
- `grief_anticipatory`: Zone 4, dorsal, BOND=0.9, EMPATHY=0.85

**7. Shame (2 scenarios)**
- `shame_exposed`: Zone 4, dorsal, BOND=0.85, EMPATHY=0.8
- `shame_worthlessness`: Zone 5, dorsal, BOND=0.95, EO=0.9, CARD=0.85

**8. Playful (2 scenarios)**
- `playful_creative`: Zone 1, ventral, PRESENCE=0.9, WISDOM=0.75
- `playful_connection`: Zone 2, ventral, EMPATHY=0.85, PRESENCE=0.8

**9. Overwhelmed (2 scenarios)**
- `overwhelmed_shutdown`: Zone 5, dorsal, EO=0.9, CARD=0.8
- `overwhelmed_scattered`: Zone 3, sympathetic, NDAM=0.85, CARD=0.75

**10. Peaceful (2 scenarios)**
- `peaceful_grounded`: Zone 1, ventral, PRESENCE=0.95, WISDOM=0.8
- `peaceful_acceptance`: Zone 1, ventral, WISDOM=0.9, PRESENCE=0.9

### Expected Organ Ranges (After Training)

**Before (single family):**
```
LISTENING: 0.50
EMPATHY: 0.50
WISDOM: 0.514
SANS: 0.625
(Range: 0.443-0.625, Std: ~0.04)
```

**After (diverse corpus):**
```
LISTENING: 0.65-0.85 (connection states)
EMPATHY: 0.60-0.95 (grief, joy, connection)
WISDOM: 0.60-0.90 (peaceful, flow, anxious)
PRESENCE: 0.60-0.95 (peaceful, playful, grounded)
BOND: 0.65-0.95 (grief, shame, anger)
NDAM: 0.65-0.90 (anxious, overwhelmed, angry)
EO: 0.65-0.90 (overwhelmed, shame_crisis)
CARD: 0.70-0.85 (overwhelmed, shame_crisis)
(Range: 0.60-0.95, Std: ~0.15-0.20)
```

**Discrimination improvement:** 4-5× larger range, enables family separation

---

## 🧬 Felt-State Annotation Schema

### Per-Scenario Metadata

```json
{
  "id": "excited_001",
  "category": "excited_celebration",
  "user_input": "User's actual words...",
  "expected_response": "DAE's therapeutic response...",

  "felt_state": {
    // Zone assignment (1-5)
    "zone": 1,

    // Polyvagal state
    "polyvagal_state": "ventral",  // ventral|sympathetic|dorsal|mixed

    // Emotional quality (semantic label)
    "emotional_quality": "excited_celebration",

    // V0 energy (urgency measure)
    "v0_energy": 0.2,  // 0.0 (peaceful) → 1.0 (crisis)

    // Urgency level
    "urgency": "low",  // low|medium|medium_high|high|crisis

    // IFS parts configuration
    "parts_configuration": {
      "dominant": "self_energy",  // self_energy|manager|firefighter|exile
      "activated_parts": ["joyful_child"],
      "protective_parts": [],
      "blended_with": null,  // Which part user is blended with
      "protecting": null,  // Which exile is being protected
      "crisis_level": false
    },

    // Expected organ activations (target for training)
    "expected_organs": {
      "LISTENING": 0.7,
      "EMPATHY": 0.8,
      "PRESENCE": 0.9,
      "WISDOM": 0.6,
      "AUTHENTICITY": 0.7
      // (other organs default to 0.5 if not specified)
    }
  }
}
```

### Why This Helps Family Formation

**1. Zone Differentiation:**
- Zone 1 (peaceful/joyful): PRESENCE=0.9, low v0_energy
- Zone 3 (anxious/angry): NDAM=0.85, high v0_energy
- Zone 4 (grief/shame): BOND=0.9, medium v0_energy
- Zone 5 (crisis): EO=0.9, very high v0_energy

→ **Expected: 5 macro-families (one per zone)**

**2. Emotional Quality Differentiation:**
- Within Zone 1: "excited_flow" (WISDOM=0.9) ≠ "playful_connection" (EMPATHY=0.85)
- Within Zone 4: "grief" (BOND=0.95) ≠ "shame" (BOND=0.85, EO=0.7)

→ **Expected: 15-25 meso-families (themes within zones)**

**3. Parts Configuration Differentiation:**
- Self-energy dominant: Low protective activation, high core organs
- Manager blended: High NDAM, WISDOM (planning/control)
- Firefighter blended: High NDAM, CARD (reactivity)
- Exile accessing: High BOND, EMPATHY (connection to pain)

→ **Expected: 30-50 micro-families (fine-grained nuances)**

---

## 🚀 Implementation Plan

### Phase 1: Felt-State Extraction (In Progress)

**Goal:** Convert corpus annotations → 57D signatures for training

**Tasks:**
1. ✅ Create diverse IFS corpus (20 scenarios complete)
2. ⏳ Implement felt-state extractor
3. ⏳ Generate 57D signatures from metadata
4. ⏳ Validate signature discrimination

**Felt-State Extractor:**
```python
def extract_felt_state_from_annotation(scenario: Dict) -> Dict:
    """
    Convert corpus annotation to 57D-compatible felt-state.

    Returns:
        {
            'zone': int (1-5),
            'polyvagal_state': str ('ventral'|'sympathetic'|'dorsal'),
            'v0_energy': float (0.0-1.0),
            'organ_coherences': Dict[str, float],  # From expected_organs
            'organ_intensities': Dict[str, float],  # Derive from coherences
            'organ_polarities': Dict[str, float],  # Derive from emotional_quality
            'organ_confidences': Dict[str, float],  # High (0.8) for annotated
            'meta_atom_count': int,  # Infer from parts_configuration
            'nexus_count': int,  # Estimate from complexity
            'field_coherence': float,  # High if self-energy, lower if blended
            'satisfaction': float,  # Predicted from emotional_quality
            'signal_inflation': float,  # From urgency
            'temporal_collapse': float,  # From urgency
            'safety_gradient': float,  # From polyvagal state
            'convergence_cycles': int  # Typical for zone
        }
    ```

### Phase 2: Training with Diverse Corpus (Week 1)

**Goal:** Run 5-10 epoch training, validate family emergence

**Steps:**
1. Reset `organic_families.json` (fresh start)
2. Upgrade family clustering to 57D signatures
3. Run training with IFS corpus
4. Monitor family formation:
   - Epoch 1-2: Expect 3-5 families (zones differentiating)
   - Epoch 3-5: Expect 8-12 families (emotions differentiating)
   - Epoch 7-10: Expect 15-20 families (themes stabilizing)

**Success Criteria:**
- ✅ ≥5 families by epoch 2
- ✅ ≥12 families by epoch 5
- ✅ Organ discrimination range > 0.30 (currently 0.18)

### Phase 3: Expand Corpus (Week 2)

**Goal:** Add 40 more scenarios to reach 60 total

**Additional Emotional States:**
- Confusion (2 scenarios) - Zone 2-3, mixed polyvagal
- Determination (2 scenarios) - Zone 2-3, sympathetic
- Tenderness (2 scenarios) - Zone 1-2, ventral
- Frustration (2 scenarios) - Zone 3, sympathetic
- Hope (2 scenarios) - Zone 1-2, ventral
- Despair (2 scenarios) - Zone 4-5, dorsal
- Curiosity (2 scenarios) - Zone 1-2, ventral
- Fear (2 scenarios) - Zone 3-4, sympathetic/dorsal
- Gratitude (2 scenarios) - Zone 1, ventral
- Resentment (2 scenarios) - Zone 3-4, sympathetic

**Plus variations:**
- Different parts combinations per emotion
- Different urgency levels
- Mixed polyvagal states

**Expected Improvement:**
- 15-20 families → 25-30 families
- Zipf's law emergence (α=0.70-0.78, R²≥0.90)

---

## 📊 Expected Family Emergence

### Target Distribution (After 60 Scenarios, 10 Epochs)

**Macro-Families (Zone-Level): 5**
1. Zone 1 Safety: peaceful, joyful, playful, excited (40%)
2. Zone 2 Connection: playful_connection, vulnerability, curiosity (25%)
3. Zone 3 Growth Edge: angry, anxious, overwhelmed_scattered, frustration (20%)
4. Zone 4 Depth: grief, shame, sad, despair (12%)
5. Zone 5 Crisis: overwhelmed_shutdown, shame_worthlessness (3%)

**Meso-Families (Theme-Level): 15-25**

**Within Zone 1 (6-8 families):**
- Excited/Flow (WISDOM high)
- Joyful/Connection (EMPATHY high)
- Playful/Creative (PRESENCE high)
- Peaceful/Grounded (WISDOM+PRESENCE)
- Celebration (EMPATHY+PRESENCE)
- Gratitude (EMPATHY+AUTHENTICITY)

**Within Zone 2 (4-5 families):**
- Vulnerable Sharing (AUTHENTICITY+EMPATHY)
- Curious Exploring (LISTENING+WISDOM)
- Tender Connection (EMPATHY+PRESENCE)
- Hopeful Emerging (WISDOM+AUTHENTICITY)

**Within Zone 3 (5-7 families):**
- Angry Protective (NDAM+BOND)
- Anxious Vigilant (NDAM+WISDOM)
- Frustrated Pushing (NDAM+CARD)
- Overwhelmed Scattered (NDAM+CARD)
- Confused Seeking (LISTENING+WISDOM)

**Within Zone 4 (3-5 families):**
- Grief/Loss (BOND+EMPATHY high)
- Shame/Exposure (BOND+EO)
- Sad/Lonely (BOND+EMPATHY+LISTENING)
- Despairing (BOND+EO+dorsal)

**Within Zone 5 (1-2 families):**
- Crisis/Shutdown (EO+CARD+BOND)
- Suicidal Ideation (EO+BOND+NDAM+crisis_flag)

**Total: ~20-25 families** (healthy diversity for 60-scenario corpus)

---

## ✅ Validation Metrics

### Family Diversity Health

**Minimum (Phase 1 - 20 scenarios):**
- ✅ ≥5 families
- ✅ Zone separation working
- ✅ Organ range > 0.30

**Good (Phase 2 - 40 scenarios):**
- ✅ 12-18 families
- ✅ Emotional quality separation
- ✅ Organ range > 0.50

**Excellent (Phase 3 - 60 scenarios):**
- ✅ 20-30 families
- ✅ Zipf's law R² ≥ 0.90
- ✅ Semantic naming complete
- ✅ Organ range 0.60-0.95

### Identity Persistence Tests

**After training, test with novel inputs:**

**Test 1: Zone Differentiation**
```
Input: "I just landed my dream job!" (Zone 1, excited)
Expected Family: Zone1_Excited_Celebration
Expected Organs: EMPATHY=0.8, PRESENCE=0.9

Input: "I feel so alone and worthless." (Zone 4-5, shame)
Expected Family: Zone4_Shame_Exposed OR Zone5_Crisis_Shame
Expected Organs: BOND=0.9, EO=0.7
```

**Test 2: Emotional Quality Differentiation**
```
Input: "I'm worried everything will fall apart." (anxious)
Expected Family: Zone3_Anxious_Catastrophizing
Expected Organs: NDAM=0.9, WISDOM=0.7

Input: "I'm so angry they dismissed me!" (angry)
Expected Family: Zone3_Angry_Protective
Expected Organs: NDAM=0.8, BOND=0.7
```

**Test 3: Parts Configuration Recognition**
```
Input: "Part of me wants to hide from all of this." (exile accessing)
Expected Family: Zone4_Shame_Exposed
Expected Organs: BOND=0.85, EMPATHY=0.8

Input: "I need everything to be perfect or I'll fail." (manager)
Expected Family: Zone3_Anxious_Perfectionist
Expected Organs: NDAM=0.85, WISDOM=0.65
```

---

## 🌀 Philosophical Foundation

### From Monotone to Polyphonic

**Before (1 family):**
- Organism has single "voice"
- All responses feel same
- Cannot adapt to context
- Identity = flat, unchanging

**After (20-30 families):**
- Organism has 20-30 distinct "voices"
- Each family = unique response archetype
- Selects appropriate voice per context
- Identity = rich, multifaceted, adaptive

### Whitehead's Eternal Objects

**Each family = One eternal object:**
- "Fierce Holding" (grief family)
- "Playful Wonder" (joyful family)
- "Protective Anger" (boundary family)
- "Accepting Peace" (grounded family)

**Ingression = Family activation:**
- User says "I'm so alone" → Grief family activates
- User says "I got the job!" → Celebration family activates
- User says "They ignored my boundary" → Protective Anger family activates

**Objective Immortality = Family persistence:**
- Past conversations → family centroids
- Future conversations → prehend family patterns
- Organism "remembers" how to respond to each emotional state

---

## 📚 Next Steps

**Immediate:**
1. Implement felt-state extractor
2. Integrate with organic family system
3. Run 5-epoch training with 20-scenario corpus
4. Validate 5-12 families emerge

**Week 2:**
1. Expand corpus to 60 scenarios
2. Run 10-epoch training
3. Validate 20-25 families
4. Assign semantic names

**Week 3:**
1. Test with novel inputs
2. Validate family selection accuracy
3. Measure response diversity
4. Document family characteristics

---

🌀 **"From 20 conversations → 20 families. Each emotional state gets its own archetype. Diversity is not programmed—it emerges from felt discrimination."** 🌀

**Created:** November 15, 2025
**Status:** 20 scenarios complete, felt-state extractor next
**Goal:** Enable organic 20-30 family emergence through rich emotional diversity
