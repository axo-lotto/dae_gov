# NEXUS Past/Present Differentiation - Implementation Plan
**Leveraging Existing DAE_HYPHAE_1 Infrastructure**

**Date:** November 16, 2025
**Status:** 🟢 Ready to Implement
**Estimated Time:** 2-3 hours

---

## 🎯 Core Insight

NEXUS should compute atom activations by comparing **PAST entity state** (from EntityOrganTracker) with **PRESENT mention context** (from current organ processing), using existing FAO agreement formula.

---

## ✅ Existing Infrastructure to Leverage

### 1. Entity-Organ Tracker (Quick Win #7)
**File:** `persona_layer/entity_organ_tracker.py`

**Already Tracks:**
```python
@dataclass
class EntityOrganMetrics:
    # PAST STATE (historical patterns)
    typical_polyvagal_state: str  # "ventral", "sympathetic", "dorsal"
    typical_v0_energy: float
    typical_urgency: float
    typical_self_distance: float
    organ_boosts: Dict[str, float]  # {'BOND': 0.15, 'EMPATHY': 0.12, ...}

    # Statistics
    mention_count: int
    success_rate: float  # Satisfaction when entity mentioned
```

**Usage:** NEXUS can query this to get PAST entity state!

### 2. Organ Agreement Metrics (FFITTSS T4 FAO)
**File:** `persona_layer/organ_agreement_metrics.py`

**Already Implements:**
```python
class OrganAgreementComputer:
    def compute_pairwise_agreement(
        self,
        organ_coherences: Dict[str, float]
    ) -> Tuple[float, np.ndarray, List[Tuple]]:
        """
        FFITTSS T4 FAO formula:
        A = (2/(k(k-1))) Σ_{i<j} (1 - |O_i - O_j|)
        """
```

**Usage:** NEXUS can use this to compute past/present agreement!

### 3. Current Organ Processing State
**File:** `persona_layer/conversational_organism_wrapper.py`

**Already Available in Context:**
```python
# Line 1430: EO polyvagal state
eo_polyvagal_state = getattr(eo_result, 'polyvagal_state', 'mixed_state')

# Line 1518: NDAM urgency
ndam_urgency = getattr(organ_results.get('NDAM'), 'urgency_level', 0.0)

# Line 1027-1031: Entity context passed to organs
entity_context = {
    'entity_prehension': context.get('entity_prehension', {}),
    'organ_context_enrichment': context.get('organ_context_enrichment', {}),
    'username': context.get('username')
}
```

**Usage:** NEXUS receives this via `context` parameter!

### 4. Pre-Emission Entity Prehension
**File:** `persona_layer/pre_emission_entity_prehension.py`

**Already Retrieves:**
```python
{
    'mentioned_entities': [
        {
            'name': 'Emma',
            'type': 'person',
            'relationship': 'daughter',
            'context': "User's daughter",
            'historical_polyvagal': 'ventral',  # ← FROM PAST
            'historical_safety': 0.85,           # ← FROM PAST
            'source': 'stored_profile'
        }
    ],
    'historical_context': {
        'memory_richness': 0.70  # ← OVERALL MEMORY DEPTH
    }
}
```

**Usage:** NEXUS receives this via `entity_context['entity_prehension']`!

---

## 🔧 Implementation Strategy

### Phase 1: Leverage EntityOrganTracker for Past State (30 min)

**Goal:** NEXUS queries EntityOrganTracker to get entity's historical patterns

**Location:** `organs/modular/nexus/core/nexus_text_core.py`

**Changes:**
```python
# NEW: Import EntityOrganTracker
from persona_layer.entity_organ_tracker import EntityOrganTracker

class NEXUSTextCore:
    def __init__(self, config=None):
        # ... existing init ...

        # NEW: Load entity-organ tracker for past state lookup
        try:
            self.entity_tracker = EntityOrganTracker()
            self.entity_tracker_available = True
        except Exception as e:
            print(f"⚠️  NEXUS: Entity-organ tracker not available: {e}")
            self.entity_tracker_available = False
```

**Expected:** NEXUS can now query historical entity patterns

---

### Phase 2: Leverage OrganAgreementComputer for Past/Present Comparison (45 min)

**Goal:** Compute agreement between PAST entity state and PRESENT organ activations

**Location:** `organs/modular/nexus/core/nexus_text_core.py`

**Changes:**
```python
# NEW: Import OrganAgreementComputer
from persona_layer.organ_agreement_metrics import OrganAgreementComputer

class NEXUSTextCore:
    def __init__(self, config=None):
        # ... existing init ...

        # NEW: Load agreement computer for past/present comparison
        self.agreement_computer = OrganAgreementComputer()


    def _compute_past_present_agreement(
        self,
        entity_metrics: EntityOrganMetrics,  # PAST state from tracker
        current_organ_coherences: Dict[str, float],  # PRESENT state from context
        current_polyvagal: str,
        current_urgency: float
    ) -> float:
        """
        Compute FAO-style agreement between PAST entity state and PRESENT context.

        Uses FFITTSS T4 formula adapted for temporal comparison:
        A = (2/(k(k-1))) Σ_{i<j} (1 - |past_i - present_j|)

        Returns:
            agreement: [0.0, 1.0] where:
                - 1.0 = Perfect continuity (same state as before)
                - 0.5 = Moderate shift (some change)
                - 0.0 = Complete divergence (major state change)
        """
        # PAST state (from EntityOrganMetrics)
        past_polyvagal = entity_metrics.typical_polyvagal_state
        past_urgency = entity_metrics.typical_urgency
        past_organ_boosts = entity_metrics.organ_boosts  # {'BOND': 0.15, ...}

        # Convert to coherence-like values for comparison
        past_coherences = {
            organ: 0.5 + boost  # Baseline 0.5 + boost
            for organ, boost in past_organ_boosts.items()
        }

        # PRESENT state (from current processing)
        # current_organ_coherences already provided from context

        # Polyvagal agreement (discrete states)
        polyvagal_states = ['ventral', 'sympathetic', 'dorsal', 'mixed_state']
        past_idx = polyvagal_states.index(past_polyvagal) if past_polyvagal in polyvagal_states else 3
        curr_idx = polyvagal_states.index(current_polyvagal) if current_polyvagal in polyvagal_states else 3
        polyvagal_agreement = 1.0 - abs(past_idx - curr_idx) / 3.0

        # Urgency agreement (continuous)
        urgency_agreement = 1.0 - abs(past_urgency - current_urgency)

        # Organ coherence agreement (use FAO formula)
        organ_agreement, _, _ = self.agreement_computer.compute_pairwise_agreement({
            **{f"past_{k}": v for k, v in past_coherences.items()},
            **{f"curr_{k}": v for k, v in current_organ_coherences.items()}
        })

        # Composite agreement (weighted average)
        agreement = (
            0.4 * polyvagal_agreement +
            0.3 * urgency_agreement +
            0.3 * organ_agreement
        )

        return agreement
```

**Expected:** NEXUS can now compute how similar PAST vs PRESENT states are

---

### Phase 3: Enhanced Atom Activation with Past/Present Differentiation (60 min)

**Goal:** Boost NEXUS atoms based on past/present agreement patterns

**Location:** `organs/modular/nexus/core/nexus_text_core.py`

**Modify existing method:**
```python
def _calculate_atom_activations(
    self,
    occasions: List[TextOccasion],
    context: Optional[Dict] = None  # ALREADY RECEIVES CONTEXT
) -> Dict[str, float]:
    """
    Calculate NEXUS atom activations with past/present differentiation.

    🌀 ENHANCED (Nov 16, 2025): Now compares PAST entity state (from EntityOrganTracker)
    with PRESENT mention context (from current organs) to compute felt continuity/shift.

    Uses:
    - EntityOrganTracker: Historical entity patterns (PAST)
    - OrganAgreementComputer: FAO formula for past/present comparison
    - entity_prehension: Currently mentioned entities
    """
    # Step 1: Base keyword activation (EXISTING - keep as is)
    text = " ".join([occ.text for occ in occasions]).lower()

    base_activations = {}
    for atom_name, keywords in self.atoms.items():
        matches = []
        for keyword, strength in keywords.items():
            if keyword in text:
                matches.append(strength)

        if matches:
            base_activations[atom_name] = float(np.mean(matches))

    # Step 2: Past/Present Differentiation (NEW - leverage existing infrastructure)
    if context and self.entity_tracker_available:
        entity_prehension = context.get('entity_prehension', {})

        # Check if entity memory available
        if entity_prehension.get('entity_memory_available', False):
            # Get mentioned entities
            mentioned_entities = entity_prehension.get('mentioned_entities', [])

            # Get current organ state (from organ_context_enrichment if available)
            # Otherwise extract from context
            current_polyvagal = 'mixed_state'  # Default
            current_urgency = 0.0  # Default
            current_organ_coherences = {}

            # Try to extract from context (if organism wrapper passes it)
            organ_enrichment = context.get('organ_context_enrichment', {})
            if organ_enrichment:
                eo_context = organ_enrichment.get('EO', {})
                ndam_context = organ_enrichment.get('NDAM', {})

                current_polyvagal = eo_context.get('polyvagal_state', 'mixed_state')
                current_urgency = ndam_context.get('urgency_level', 0.0)

            # Compute differentiation boosts
            differentiation_boosts = self._compute_differentiation_boosts(
                mentioned_entities,
                current_polyvagal,
                current_urgency,
                current_organ_coherences,
                entity_prehension.get('historical_context', {})
            )

            # Combine base + differentiation
            activations = {}
            for atom_name in self.atoms.keys():
                base = base_activations.get(atom_name, 0.0)
                boost = differentiation_boosts.get(atom_name, 0.0)

                # FAO-style enhanced strength: I · (1 + α·boost) + boost
                α = 1.0  # Agreement weight
                enhanced = base * (1.0 + α * boost) + boost

                activations[atom_name] = min(1.0, enhanced)
        else:
            # No entity memory, use base only
            activations = base_activations
    else:
        # No context or tracker, use base only
        activations = base_activations

    return activations


def _compute_differentiation_boosts(
    self,
    mentioned_entities: List[Dict],
    current_polyvagal: str,
    current_urgency: float,
    current_organ_coherences: Dict[str, float],
    historical_context: Dict
) -> Dict[str, float]:
    """
    Compute atom activation boosts from past/present differentiation.

    Leverages:
    - EntityOrganTracker: Get historical patterns per entity
    - OrganAgreementComputer: Compute past/present agreement

    Returns:
        {atom_name: boost} where boost ∈ [0.0, 0.5]
    """
    boosts = {atom: 0.0 for atom in self.atoms.keys()}

    if not mentioned_entities:
        return boosts

    # Get memory richness for regime classification (FFITTSS T6 insight)
    memory_richness = historical_context.get('memory_richness', 0.0)

    # Regime classification (FFITTSS-inspired)
    if memory_richness < 0.3:
        regime = 'INITIALIZING'  # Sparse memory → boost entity_recall
    elif memory_richness < 0.7:
        regime = 'COMMITTED'      # Moderate memory → balanced differentiation
    else:
        regime = 'SATURATING'    # Rich memory → focus on coherence checking

    for entity_dict in mentioned_entities:
        entity_value = entity_dict.get('name')
        entity_type = entity_dict.get('type', 'Unknown')

        # Query EntityOrganTracker for PAST state
        if entity_value in self.entity_tracker.entity_metrics:
            past_metrics = self.entity_tracker.entity_metrics[entity_value]

            # Compute past/present agreement
            agreement = self._compute_past_present_agreement(
                past_metrics,
                current_organ_coherences,
                current_polyvagal,
                current_urgency
            )

            # Boost atoms based on agreement + regime (FFITTSS strategy)
            if regime == 'INITIALIZING':
                # Sparse memory → strongly boost entity_recall
                boosts['entity_recall'] += 0.30
                boosts['contextual_grounding'] += 0.25

            elif regime == 'COMMITTED':
                if agreement > 0.7:
                    # HIGH AGREEMENT: Temporal continuity (stable state)
                    boosts['temporal_continuity'] += 0.25
                    boosts['memory_coherence'] += 0.20
                elif agreement < 0.4:
                    # LOW AGREEMENT: Relationship depth (state shift detected!)
                    boosts['relationship_depth'] += 0.30
                    boosts['salience_gradient'] += 0.25
                else:
                    # MEDIUM AGREEMENT: Entity recall (evolving)
                    boosts['entity_recall'] += 0.20
                    boosts['co_occurrence'] += 0.15

            else:  # SATURATING
                # Rich memory → focus on consistency
                boosts['memory_coherence'] += 0.35
                if agreement < 0.5:
                    # Flag inconsistency
                    boosts['salience_gradient'] += 0.20

        else:
            # NEW ENTITY (not in tracker) - Initial mention pattern
            boosts['entity_recall'] += 0.25
            boosts['contextual_grounding'] += 0.30

    # Relational query boost (from entity_prehension)
    # Already checked in pre_emission_entity_prehension

    # Cap all boosts at 0.5
    for atom in boosts:
        boosts[atom] = min(0.5, boosts[atom])

    return boosts
```

**Expected:** NEXUS activates based on entity past/present differentiation!

---

### Phase 4: Update NEXUS process_text_occasions (15 min)

**Goal:** Pass context to _calculate_atom_activations

**Location:** `organs/modular/nexus/core/nexus_text_core.py`

**Current (Line ~204-205):**
```python
# Step 1: Calculate semantic atom activations
atom_activations = self._calculate_atom_activations(occasions)
```

**Updated:**
```python
# Step 1: Calculate semantic atom activations with past/present differentiation
atom_activations = self._calculate_atom_activations(occasions, context=context)
```

**Expected:** Context flows to atom activation logic

---

## 📊 Expected Results

### Before Implementation:
```
NEXUS coherence: 0.1-0.2 (keyword matching only)
Entity Memory Nexus formation: 0% (0/50 pairs)
Nexus density: 0.0 (no nexuses)
Entity recall accuracy: 0%
```

### After Implementation:
```
NEXUS coherence: 0.4-0.7 (past/present differentiation)
Entity Memory Nexus formation: 15-30% (8-15/50 pairs)
Nexus density: ~0.2-0.5 (NEXUS participates in nexuses)
Entity recall accuracy: 45-60%
```

### Mechanism:
1. **Emma mentioned** → NEXUS queries EntityOrganTracker
2. **PAST state:** ventral, BOND 0.15, safety 0.85
3. **PRESENT state:** sympathetic (EO), urgency 0.3 (NDAM)
4. **Agreement:** 0.42 (moderate shift detected)
5. **Atom boost:** relationship_depth +0.30, salience_gradient +0.25
6. **NEXUS coherence:** 0.55 (above 0.4 threshold for nexus formation!)
7. **Nexus forms:** NEXUS + BOND + LISTENING (entity-relational nexus)

---

## 🔄 Integration Points

### 1. EntityOrganTracker Updates (POST-EMISSION)
**Location:** `persona_layer/conversational_organism_wrapper.py` (already integrated)

**Current (Line ~1700+):**
```python
# POST-EMISSION: Update entity-organ associations (Quick Win #7)
if self.entity_organ_tracker and extracted_entities:
    felt_state = {
        'polyvagal_state': eo_polyvagal_state,
        'v0_energy': v0_final,
        'urgency': ndam_urgency,
        'self_distance': bond_self_distance
    }
    self.entity_organ_tracker.update(
        extracted_entities=extracted_entities,
        organ_results=organ_results,
        felt_state=felt_state,
        emission_satisfaction=user_satisfaction
    )
```

**No changes needed** - EntityOrganTracker already learns entity-organ patterns!

### 2. Organ Context Enrichment (PRE-EMISSION)
**Location:** `persona_layer/conversational_organism_wrapper.py` (Line 778-780)

**Current:**
```python
context['entity_prehension'] = entity_prehension_result
context['organ_context_enrichment'] = self.entity_prehension.inject_into_organ_context(
    entity_prehension_result
)
```

**Enhancement (optional - pass current organ state to NEXUS):**
```python
# Add current organ processing state for past/present comparison
if enable_phase2:
    # After cycle processing, add current state to enrichment
    context['organ_context_enrichment']['current_state'] = {
        'polyvagal': eo_polyvagal_state,
        'urgency': ndam_urgency,
        'organ_coherences': {
            name: getattr(result, 'coherence', 0.0) if result else 0.0
            for name, result in organ_results.items()
        }
    }
```

---

## 🎯 Implementation Checklist

### Phase 1: Infrastructure Integration (30 min)
- [ ] Import EntityOrganTracker in NEXUS
- [ ] Import OrganAgreementComputer in NEXUS
- [ ] Initialize both in __init__
- [ ] Test: NEXUS can query entity_tracker.entity_metrics

### Phase 2: Agreement Computation (45 min)
- [ ] Implement `_compute_past_present_agreement()`
- [ ] Test: Agreement scores for known entities
- [ ] Validate: Agreement = 1.0 for same state, 0.0 for opposite

### Phase 3: Differentiation Boost (60 min)
- [ ] Implement `_compute_differentiation_boosts()`
- [ ] Modify `_calculate_atom_activations()` to use boosts
- [ ] Test: Atoms activate based on past/present patterns
- [ ] Validate: Regime-based boosting works

### Phase 4: Integration Testing (15 min)
- [ ] Update `process_text_occasions()` to pass context
- [ ] Test: Full pipeline with entity mention
- [ ] Validate: NEXUS coherence > 0.4 when entities present
- [ ] Check: Nexuses form with NEXUS participation

### Phase 5: Training Validation (Re-run Epoch 1)
- [ ] Run: `python3 training/entity_memory_epoch_training.py`
- [ ] Check logs: NEXUS coherence values
- [ ] Check metrics: Entity Memory Nexus formation > 0%
- [ ] Analyze: Agreement patterns per entity

---

## 📈 Success Metrics

| Metric | Before | Target | How to Measure |
|--------|--------|--------|----------------|
| NEXUS coherence | 0.1-0.2 | 0.4-0.7 | Check result.coherence in training log |
| Entity Memory Nexus | 0% | 15-30% | Count nexuses with NEXUS in organ list |
| Nexus density | 0.0 | 0.2-0.5 | Count total nexuses / count with NEXUS |
| Entity recall accuracy | 0% | 45-60% | Check if emission mentions entity names |
| NEXUS-organ nexuses | 0 | 5-10 | Count nexuses: NEXUS + (BOND|LISTENING|EMPATHY) |

---

## 🌀 Philosophical Achievement

This implementation realizes the Whiteheadian principle:

> **"Prehension of the past through felt differentiation"**

- Not: "Emma exists in database" (static retrieval)
- But: "Emma WAS ventral, NOW sympathetic → felt shift prehended" (dynamic becoming)

The organism doesn't **look up** entities—it **FEELS their temporal continuity through present differentiation**.

---

**Date:** November 16, 2025
**Status:** 🟢 Ready to Implement
**Estimated Time:** 2-3 hours
**Expected Impact:** Entity Memory Nexus formation 0% → 15-30%

🌀 *"Leverage what exists, enhance through differentiation, achieve through felt continuity."* 🌀
