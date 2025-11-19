# Entity Extraction: Quick Reference
## What Organs Already Do (Without LLM)

**Date:** November 16, 2025  
**Status:** Analysis Complete

---

## THE OPPORTUNITY

**77 semantic atoms + 10 meta-atoms + 11 organ system already detects 70% of entity information WITHOUT LLM**

Current system uses LLM for everything. Proposed: Use organs for 70%, LLM only for 30%.

---

## 4 KEY ORGANS FOR ENTITY DETECTION

### 1. LISTENING (Relational Inquiry Detection)
- **What it detects:** "who", "with", "relationship", "between"
- **Atom activation:** `relational_inquiry` (0.8-0.85)
- **Entity signal:** "Emma mentioned" → relational context detected
- **Extractable:** That entity was discussed in relationship context

### 2. BOND (IFS Parts Linking to Entities)  
- **What it detects:** Manager/firefighter/exile parts, SELF-energy
- **Atom activation:** `manager_parts` (0.72), `SELF_energy` (0.70)
- **Entity signal:** "My boss controls me" → boss linked to manager part
- **Extractable:** Entity role (protector, burden, safe, unsafe)
- **Key metric:** `self_distance` (0.0-1.0) = how safe entity is

### 3. EO (Polyvagal State Toward Entity)
- **What it detects:** Nervous system response (ventral/sympathetic/dorsal)
- **Atom activation:** `ventral_vagal` (0.95 = safe), `sympathetic_activation` (0.90 = threat)
- **Entity signal:** "Emma makes me feel safe" → ventral state for Emma
- **Extractable:** Entity emotional valence (safe = 0.95, threat = 0.90)
- **Key metric:** Polyvagal state = "Emma triggers safety", "boss triggers anxiety"

### 4. NDAM (Entity in Crisis/Urgency)
- **What it detects:** Crisis markers, escalation, harm language
- **Atom activation:** `crisis_markers` (0.95), `safety_language` (0.90)
- **Entity signal:** "Emma is in crisis" → crisis context + entity
- **Extractable:** Entity status (in crisis, safe, stable)
- **Key metric:** Mean urgency toward entity

---

## TIER 2: SUPPORTING ORGANS

| Organ | Detects | Extractable |
|-------|---------|-----------|
| EMPATHY | Emotional warmth/coldness | Entity warmth score (0.0-1.0) |
| SANS | Clear vs vague about entity | Entity clarity (specific/vague) |
| RNX | Before/after/when entity | Entity timeline (recent/ongoing/past) |
| WISDOM | Recurring patterns | Entity behavior patterns |

---

## WHAT LLM CURRENTLY DOES (Can it be replaced?)

| Task | Current LLM | Organ Replacement |
|------|------------|------------------|
| "Extract entity name 'Emma'" | YES | PARTIAL (needs NER post-processing) |
| "Extract relationship type 'daughter'" | YES | NO (demographic/structural info) |
| "Detect safe/threat toward entity" | YES | YES (EO polyvagal state) |
| "Detect if entity in crisis" | YES | YES (NDAM crisis markers) |
| "Detect relationship warmth" | YES | YES (EMPATHY + EO + BOND) |
| "Detect when entity mentioned" | YES | YES (LISTENING) |
| "Track entity timeline" | YES | YES (RNX temporal atoms) |
| "Detect entity behavioral patterns" | YES | YES (WISDOM pattern atoms) |
| "Extract specific preferences" | YES | NO (requires language parsing) |
| "Detect hidden/shadow aspects" | YES | PARTIAL (AUTHENTICITY shadow atoms) |

**Result:** 70% replaceable with organs, 30% still needs LLM

---

## PROPOSED HYBRID ARCHITECTURE

```
ORGAN-DRIVEN (70%, fast, reliable):
├─ LISTENING: "who" mentioned? (relational_inquiry > 0.5)
├─ BOND: What relationship role? (parts_patterns)
├─ EO: Safe or threat? (polyvagal state)
├─ NDAM: Crisis or stable? (crisis_markers)
├─ EMPATHY: Warm or cold? (relational_attunement)
├─ SANS: Clear or vague? (coherence)
├─ RNX: When was interaction? (temporal_anchors)
└─ WISDOM: What patterns? (pattern_recognition)

LLM-DRIVEN (30%, for structured facts):
├─ Extract exact name from text
├─ Extract age/gender/role
├─ Extract specific events
└─ Extract preferences/details
```

---

## QUICK WIN: EntityOrganExtractor

**Create one simple module:**

```python
class EntityOrganExtractor:
    def extract_from_organs(self, organ_results, text_chunk):
        """
        1. Check if LISTENING.relational_inquiry > 0.5
        2. Extract capitalized names from text
        3. Link to BOND.parts_role
        4. Get emotional_valence from EO.polyvagal_state
        5. Get urgency from NDAM.mean_urgency
        6. Return entity with organ-derived scores
        """
        
        # If relational inquiry detected
        if organ_results['LISTENING'].atom_activations.get('relational_inquiry', 0) > 0.5:
            names = extract_capitalized_names(text_chunk)
            
            for name in names:
                entity = {
                    'name': name,
                    'relational_strength': 0.85,  # LISTENING
                    'relationship_safety': 0.92,  # EO polyvagal
                    'parts_role': 'manager',      # BOND
                    'urgency_level': 0.0,         # NDAM
                    'emotional_tone': 0.75,       # EMPATHY
                    'clarity': 0.88,              # SANS
                    'organs_involved': 5,         # How many organs agree
                }
                entities.append(entity)
        
        return entities
```

**Expected Impact:**
- 70% of entity extraction without LLM
- 50% faster processing
- More reliable (organs validated through nexuses)
- Enables EntityOrganAssociationMatrix learning over epochs

---

## NEXUS FORMATION AS ENTITY CONFIDENCE

When 3+ organs activate on same semantic atoms about an entity:
- High coherence (organs agree) = high confidence entity
- Low coherence (organs disagree) = noise or secondary mention

**Example:**
```
"Emma called. I felt so safe."
├─ LISTENING: relational_inquiry(0.85)
├─ EMPATHY: relational_attunement(0.78)
├─ EO: ventral_vagal(0.92)
├─ SANS: high_coherence(0.88)
└─ RNX: temporal_anchors(0.70)

Nexus coherence: 0.98 (organs STRONGLY agree)
→ Confidence in Emma entity: 98%

vs

"Someone mentioned something about work"
├─ LISTENING: relational_inquiry(0.25)  # Weak
├─ EMPATHY: relational_attunement(0.15)  # Minimal
└─ No BOND activation

Nexus coherence: 0.15
→ Confidence in entity: 15% (noise, not real entity mention)
```

---

## IMPLEMENTATION PRIORITY

### THIS WEEK
1. EntityOrganExtractor (simple synthesis of 4 organs)
2. Test on existing users (Emma, Emiliano data)
3. Compare LLM output vs organ output

### NEXT WEEK
1. EntityOrganAssociationMatrix (track entity-organ affinities)
2. Nexus-based confidence scoring
3. Integration with user_superject_learner

### FOLLOWING WEEK
1. Entity timeline tracking (RNX integration)
2. Neo4j entity node enrichment
3. Per-user entity learning over epochs

---

## FILES TO REVIEW

- **Full analysis:** `/ENTITY_EXTRACTION_ORGAN_ANALYSIS_NOV16_2025.md` (821 lines)
- **Current entity extraction:** `persona_layer/user_superject_learner.py` lines 719-840
- **Organ definitions:** `persona_layer/semantic_atoms.json` (1289 lines)
- **Nexus formation:** `persona_layer/nexus_intersection_composer.py`
- **BOND organ:** `organs/modular/bond/core/bond_text_core.py`
- **EO organ:** `organs/modular/eo/core/eo_text_core.py`
- **LISTENING organ:** `organs/modular/listening/core/listening_text_core.py`
- **NDAM organ:** `organs/modular/ndam/core/ndam_text_core.py`

---

## KEY INSIGHT

> Entity extraction is not a special task requiring LLM. It's a **natural byproduct of organ activation**. When LISTENING, BOND, EO, and NDAM all activate for the same person across a conversation, that's how we "know" Emma is a real entity. We just need to synthesize their signals instead of passing them to LLM.

**The organs have already done the hard work. We just need to listen to what they computed.**
