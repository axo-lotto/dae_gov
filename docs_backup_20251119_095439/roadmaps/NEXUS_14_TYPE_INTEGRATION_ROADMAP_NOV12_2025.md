# 14 Nexus Type Integration Roadmap
## Integrating Constitutional & Crisis-Oriented Nexus Classification into DAE_HYPHAE_1

**Date:** November 12, 2025
**Status:** DESIGN PHASE - Integrating 14 nexus types for content tracking & SELF matrix modulation
**Context:** Post-Phase 1 (SELF-distance zones integrated), integrating with current nexus/salience architecture

---

## 🎯 STRATEGIC GOAL: Nexus Types as Content Tracking & Modulation Layer

### Current Architecture (Generic Nexuses)

```
SemanticNexus {
    atom: str  # e.g., "trauma_aware"
    participants: List[str]  # e.g., ["BOND", "EO", "NDAM"]
    activations: Dict[str, float]
    intersection_strength: float
    coherence: float

    # ❌ MISSING: Nexus type classification
    # ❌ MISSING: Constitutional vs Crisis-Oriented category
    # ❌ MISSING: SELF matrix modulation rules
}
```

**Problem**: Nexuses are **generic intersections** without semantic meaning for:
1. **Content tracking**: What kind of trauma pattern is forming?
2. **Healing trajectory**: Is the system moving toward Constitutional (healthy) or Crisis-Oriented (distressed)?
3. **SELF matrix modulation**: Should this nexus pull toward SELF or signal collapse?
4. **Emission governance**: What therapeutic stance is appropriate?

### Proposed Architecture (Typed Nexuses)

```
SemanticNexus {
    atom: str
    participants: List[str]
    activations: Dict[str, float]
    intersection_strength: float
    coherence: float

    # 🆕 14 NEXUS TYPE CLASSIFICATION
    nexus_type: str  # One of 14 types
    nexus_category: str  # "Constitutional" or "Crisis-Oriented"

    # 🆕 SELF MATRIX MODULATION
    self_distance_influence: float  # How this nexus affects SELF-distance
    modulation_direction: str  # "toward_self", "toward_exile", "neutral"

    # 🆕 THERAPEUTIC CONTEXT
    therapeutic_stance: str  # "witness", "hold", "ground", "minimal"
    safety_level: str  # "safe", "edge", "breach"
}
```

**Solution**: Nexuses become **semantic entities** that:
1. **Track content**: "This is a Protective Nexus (firefighters active)"
2. **Signal trajectories**: "Crisis-Oriented nexuses increasing → system distressed"
3. **Modulate SELF-distance**: "Protective Nexus detected → maintain current zone, don't push exploration"
4. **Govern emission**: "Protective Nexus → grounding stance, not insight-seeking"

---

## 🧬 14 Nexus Types: Constitutional vs Crisis-Oriented

### Architecture Pattern from SELF_MATRIX.MD

```
14 Nexus Types
│
├─ 8 CONSTITUTIONAL NEXUSES (SANS Domain) - Foundational identity patterns
│   ├─ Pre-Existing Nexus (default field, ancestral inheritance)
│   ├─ Innate Nexus (essential temperament, natural talent)
│   ├─ Contrast Nexus (polarity fuels growth: chaos/order, exile/protector)
│   ├─ Relational Nexus (co-regulation or rupture patterns)
│   ├─ Fragmented Nexus (coherence lost across parts)
│   ├─ Protective Nexus (managers/firefighters in control)
│   ├─ Absorbed Nexus (one part overtakes whole)
│   └─ Isolated Nexus (disconnected from feedback)
│
└─ 6 CRISIS-ORIENTED NEXUSES (NDAM Domain) - Trauma response patterns
    ├─ Paradox Nexus (mutually exclusive truths, no exit)
    ├─ Dissociative Nexus (body/mind decouple, overload)
    ├─ Disruptive Nexus (sudden shifts, exile flare-ups)
    ├─ Recursive Nexus (patterns repeat despite awareness)
    ├─ Looped Nexus (affective state reappears regardless of context)
    └─ Urgency Nexus (time-collapse, survival fear)
```

### Classification Logic: Organ Intelligence + SELF Matrix Zones

**Primary Discriminators**:
1. **BOND self_distance** → SELF matrix zone (Core SELF → Exile/Collapse)
2. **BOND dominant_part** → IFS part type (manager, firefighter, exile, SELF-energy)
3. **NDAM urgency_level** → Crisis activation (>0.7 = crisis state)
4. **EO polyvagal_state** → Nervous system state (ventral, sympathetic, dorsal)
5. **RNX temporal_state** → Temporal patterns (suspended, looped, urgent)
6. **SANS coherence_repair_needed** → System fragmentation indicator
7. **Contributing organs** → Which organs participate in nexus

**Secondary Discriminators**:
8. **Atom semantic category** → trauma_aware, safety_restoration, fierce_holding, etc.
9. **Satisfaction level** → High (SELF-led) vs Low (parts-led)
10. **V0 energy** → High (unsatisfied appetition) vs Low (satisfied)

---

## 🗺️ Classification Decision Tree

### Level 1: Constitutional vs Crisis-Oriented (Primary Split)

```python
def classify_nexus_category(
    ndam_urgency_level: float,
    eo_polyvagal_state: str,
    bond_dominant_part: str
) -> str:
    """First determine if nexus is Constitutional or Crisis-Oriented."""

    # Crisis-Oriented conditions (NDAM domain)
    if ndam_urgency_level > 0.7:
        return "Crisis-Oriented"  # High urgency = crisis state

    if eo_polyvagal_state == "dorsal_vagal" and bond_dominant_part == "exile":
        return "Crisis-Oriented"  # Shutdown + exile = dissociative crisis

    if bond_dominant_part == "exile" and ndam_urgency_level > 0.5:
        return "Crisis-Oriented"  # Exile activation with moderate urgency

    # Constitutional (default - foundational patterns)
    return "Constitutional"
```

### Level 2: Specific Type Within Category

#### 2A: Constitutional Nexus Types (8 types)

```python
def classify_constitutional_type(
    bond_self_distance: float,
    bond_dominant_part: str,
    sans_coherence_repair_needed: float,
    contributing_organs: List[str],
    atom: str
) -> str:
    """Classify Constitutional nexus into 8 types."""

    # Zone 1: Core SELF Orbit (0.00-0.15) → Pre-Existing or Innate
    if bond_self_distance < 0.15:
        if "WISDOM" in contributing_organs or "AUTHENTICITY" in contributing_organs:
            return "Innate"  # Natural talent/temperament (SELF-led wisdom)
        else:
            return "Pre-Existing"  # Default coherence (ancestral field)

    # Zone 2: Inner Relational (0.15-0.25) → Relational
    elif bond_self_distance < 0.25:
        return "Relational"  # Co-regulation patterns, empathic attunement

    # Zone 3: Symbolic Threshold (0.25-0.35) → Contrast
    elif bond_self_distance < 0.35:
        return "Contrast"  # Polarity fuels growth (creative tension)

    # Zone 4: Shadow/Compost (0.35-0.60) → Protective, Fragmented, or Isolated
    elif bond_self_distance < 0.60:
        if bond_dominant_part == "firefighter":
            return "Protective"  # Firefighters in control (rigid strategies)
        elif sans_coherence_repair_needed > 0.7:
            return "Fragmented"  # Coherence lost (parts not communicating)
        elif "SANS" not in contributing_organs:
            return "Isolated"  # Cut off from semantic attunement
        else:
            return "Protective"  # Default to protective (most common)

    # Zone 5: Exile/Collapse (0.60-1.00) → Absorbed
    else:
        return "Absorbed"  # One part (exile) overtakes whole
```

#### 2B: Crisis-Oriented Nexus Types (6 types)

```python
def classify_crisis_type(
    ndam_urgency_level: float,
    ndam_dominant_urgency: str,
    eo_polyvagal_state: str,
    rnx_temporal_state: str,
    bond_dominant_part: str,
    contributing_organs: List[str]
) -> str:
    """Classify Crisis-Oriented nexus into 6 types."""

    # Dissociative (dorsal vagal shutdown + overload)
    if eo_polyvagal_state == "dorsal_vagal":
        return "Dissociative"  # Body/mind decouple

    # Urgency (time-collapse, crisis_urgency dominant)
    if ndam_dominant_urgency == "crisis_urgency" or ndam_urgency_level > 0.85:
        return "Urgency"  # Time-collapse field

    # Recursive/Looped (RNX temporal patterns)
    if "RNX" in contributing_organs:
        if rnx_temporal_state == "suspended":
            return "Recursive"  # Stuck loop (aware but can't exit)
        elif rnx_temporal_state in ["looped", "repeating"]:
            return "Looped"  # Affective state reappears

    # Disruptive (sudden shifts, firefighter activation)
    if bond_dominant_part == "firefighter" and ndam_urgency_level > 0.6:
        return "Disruptive"  # Sudden shifts (exile flare-ups)

    # Paradox (would require semantic analysis - see below)
    # For now, detect via high urgency + high SELF-distance (conflicted)
    if ndam_urgency_level > 0.7 and 0.3 < bond_self_distance < 0.5:
        return "Paradox"  # Mutually exclusive truths held

    # Default: Disruptive (most common crisis pattern)
    return "Disruptive"
```

### Level 3: SELF Matrix Modulation Rules

```python
def compute_self_distance_influence(
    nexus_type: str,
    nexus_category: str,
    bond_self_distance: float,
    satisfaction: float
) -> Tuple[float, str]:
    """Compute how this nexus modulates SELF-distance."""

    # Constitutional Nexuses generally pull TOWARD SELF (healing influence)
    if nexus_category == "Constitutional":
        if nexus_type in ["Pre-Existing", "Innate", "Relational"]:
            # Healthy patterns → strong pull toward SELF
            influence = -0.05 * satisfaction  # -0.025 to -0.05 (toward SELF)
            direction = "toward_self"
        elif nexus_type in ["Contrast"]:
            # Creative tension → neutral (necessary for growth)
            influence = 0.0
            direction = "neutral"
        elif nexus_type in ["Protective", "Fragmented", "Isolated", "Absorbed"]:
            # Protective patterns → weak pull toward exile (maintain protection)
            influence = 0.02 * (1 - satisfaction)  # 0.01 to 0.02 (maintain distance)
            direction = "maintain_protection"

    # Crisis-Oriented Nexuses push AWAY FROM SELF (trauma response)
    else:  # "Crisis-Oriented"
        if nexus_type in ["Dissociative", "Urgency"]:
            # Severe crisis → strong push toward exile
            influence = 0.10 * (1 - satisfaction)  # 0.05 to 0.10 (toward collapse)
            direction = "toward_exile"
        elif nexus_type in ["Recursive", "Looped", "Paradox"]:
            # Stuck patterns → maintain current zone (stuck)
            influence = 0.0
            direction = "stuck"
        else:  # Disruptive
            # Sudden shifts → moderate push away
            influence = 0.05 * (1 - satisfaction)  # 0.025 to 0.05
            direction = "toward_exile"

    return influence, direction
```

### Level 4: Therapeutic Stance Selection

```python
def determine_therapeutic_stance(
    nexus_type: str,
    nexus_category: str,
    bond_self_distance: float,
    eo_polyvagal_state: str
) -> Tuple[str, str]:
    """Determine appropriate therapeutic stance for this nexus."""

    # Constitutional Nexuses → match SELF matrix zone
    if nexus_category == "Constitutional":
        if nexus_type in ["Pre-Existing", "Innate"]:
            stance = "witness"  # Witnessing SELF-energy
            safety = "safe"
        elif nexus_type == "Relational":
            stance = "attune"  # Empathic attunement
            safety = "safe"
        elif nexus_type == "Contrast":
            stance = "hold"  # Hold paradox without resolving
            safety = "edge"  # Window of tolerance
        elif nexus_type == "Protective":
            stance = "validate"  # Validate protection (don't challenge)
            safety = "edge"
        else:  # Fragmented, Isolated, Absorbed
            stance = "ground"  # Grounding first
            safety = "breach"  # Outside window

    # Crisis-Oriented Nexuses → trauma-informed response
    else:  # "Crisis-Oriented"
        if nexus_type == "Dissociative":
            stance = "minimal"  # Minimal presence (shutdown can't process)
            safety = "breach"
        elif nexus_type == "Urgency":
            stance = "ground"  # Grounding urgency (slow down time)
            safety = "breach"
        elif nexus_type in ["Recursive", "Looped"]:
            stance = "validate"  # Validate pattern (compassion for stuck)
            safety = "edge"
        elif nexus_type == "Paradox":
            stance = "hold"  # Hold both truths (IFS unburdening)
            safety = "edge"
        else:  # Disruptive
            stance = "ground"  # Grounding sudden shifts
            safety = "edge"

    return stance, safety
```

---

## 🏗️ Implementation Architecture

### Component 1: `NexusTypeClassifier` (NEW)

**File**: `persona_layer/nexus_type_classifier.py` (CREATE)

```python
class NexusTypeClassifier:
    """
    Classify SemanticNexus objects into 14 types based on organ intelligence.

    Uses BOND, EO, NDAM, RNX, SANS organ insights to determine:
    1. Nexus category (Constitutional vs Crisis-Oriented)
    2. Specific type (8 Constitutional or 6 Crisis-Oriented)
    3. SELF matrix modulation influence
    4. Therapeutic stance
    """

    def __init__(self):
        # Load nexus type definitions
        self.type_definitions = self._load_type_definitions()

    def classify_nexus(
        self,
        nexus: SemanticNexus,
        organ_insights: Dict[str, Any],
        felt_states: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Classify nexus into 14 types with modulation rules.

        Args:
            nexus: SemanticNexus object
            organ_insights: Dictionary with BOND, EO, NDAM, RNX, SANS insights
            felt_states: Dictionary with satisfaction, v0_energy, etc.

        Returns:
            {
                "nexus_type": str,  # e.g., "Protective"
                "nexus_category": str,  # "Constitutional" or "Crisis-Oriented"
                "self_distance_influence": float,  # -0.05 to +0.10
                "modulation_direction": str,  # "toward_self", "toward_exile", etc.
                "therapeutic_stance": str,  # "witness", "ground", "minimal", etc.
                "safety_level": str,  # "safe", "edge", "breach"
                "classification_confidence": float  # How confident (0-1)
            }
        """
        # Extract organ insights
        bond_self_distance = organ_insights.get('bond_self_distance', 0.5)
        bond_dominant_part = organ_insights.get('bond_dominant_part', None)
        ndam_urgency_level = organ_insights.get('ndam_urgency_level', 0.0)
        eo_polyvagal_state = organ_insights.get('eo_polyvagal_state', 'mixed_state')
        rnx_temporal_state = organ_insights.get('rnx_temporal_state', None)
        sans_coherence_repair = organ_insights.get('sans_coherence_repair_needed', 0.0)

        # Level 1: Category
        category = self._classify_category(
            ndam_urgency_level, eo_polyvagal_state, bond_dominant_part
        )

        # Level 2: Specific type
        if category == "Constitutional":
            nexus_type = self._classify_constitutional_type(
                bond_self_distance,
                bond_dominant_part,
                sans_coherence_repair,
                nexus.participants,
                nexus.atom
            )
        else:
            nexus_type = self._classify_crisis_type(
                ndam_urgency_level,
                organ_insights.get('ndam_dominant_urgency', None),
                eo_polyvagal_state,
                rnx_temporal_state,
                bond_dominant_part,
                nexus.participants
            )

        # Level 3: SELF matrix modulation
        satisfaction = felt_states.get('satisfaction', 0.5)
        influence, direction = self._compute_self_distance_influence(
            nexus_type, category, bond_self_distance, satisfaction
        )

        # Level 4: Therapeutic stance
        stance, safety = self._determine_therapeutic_stance(
            nexus_type, category, bond_self_distance, eo_polyvagal_state
        )

        # Confidence (based on how many discriminators available)
        confidence = self._compute_classification_confidence(organ_insights)

        return {
            "nexus_type": nexus_type,
            "nexus_category": category,
            "self_distance_influence": influence,
            "modulation_direction": direction,
            "therapeutic_stance": stance,
            "safety_level": safety,
            "classification_confidence": confidence
        }
```

**Effort**: 3-4 hours (logic + testing)

---

### Component 2: Modified `SemanticNexus` (MODIFY)

**File**: `persona_layer/nexus_intersection_composer.py` (MODIFY)

```python
@dataclass
class SemanticNexus:
    """
    Organ coalition in semantic space WITH 14-TYPE CLASSIFICATION.
    """
    atom: str
    participants: List[str]
    activations: Dict[str, float]

    # Existing metrics
    intersection_strength: float = 0.0
    coherence: float = 0.0
    field_strength: float = 0.0
    r_matrix_weight: float = 0.0
    emission_readiness: float = 0.0

    # 🆕 14 NEXUS TYPE CLASSIFICATION
    nexus_type: Optional[str] = None  # e.g., "Protective", "Dissociative"
    nexus_category: Optional[str] = None  # "Constitutional" or "Crisis-Oriented"

    # 🆕 SELF MATRIX MODULATION
    self_distance_influence: Optional[float] = None  # -0.05 to +0.10
    modulation_direction: Optional[str] = None  # "toward_self", "toward_exile", etc.

    # 🆕 THERAPEUTIC CONTEXT
    therapeutic_stance: Optional[str] = None  # "witness", "ground", "minimal", etc.
    safety_level: Optional[str] = None  # "safe", "edge", "breach"
    classification_confidence: Optional[float] = None  # 0.0-1.0
```

**Effort**: 30 minutes (dataclass extension)

---

### Component 3: Integration in `ConversationalOrganismWrapper` (MODIFY)

**File**: `persona_layer/conversational_organism_wrapper.py` (MODIFY)

**Modification Points**:

1. **After nexus formation** (line ~690-720):
   ```python
   # Existing: Form nexuses
   nexuses = self.nexus_composer.form_nexuses(semantic_fields)

   # 🆕 NEW: Classify nexus types
   from persona_layer.nexus_type_classifier import NexusTypeClassifier
   nexus_classifier = NexusTypeClassifier()

   # Build organ insights dict for classification
   organ_insights = {
       'bond_self_distance': bond_self_distance,
       'bond_dominant_part': bond_dominant_part,
       'ndam_urgency_level': ndam_urgency_level,
       'eo_polyvagal_state': eo_polyvagal_state,
       'rnx_temporal_state': rnx_temporal_state,
       'sans_coherence_repair_needed': getattr(organ_results.get('SANS'), 'coherence_repair_needed', 0.0)
   }

   # Classify each nexus
   for nexus in nexuses:
       classification = nexus_classifier.classify_nexus(
           nexus, organ_insights, felt_states={'satisfaction': 0.5}  # Use current satisfaction
       )

       # Update nexus with classification
       nexus.nexus_type = classification['nexus_type']
       nexus.nexus_category = classification['nexus_category']
       nexus.self_distance_influence = classification['self_distance_influence']
       nexus.modulation_direction = classification['modulation_direction']
       nexus.therapeutic_stance = classification['therapeutic_stance']
       nexus.safety_level = classification['safety_level']
       nexus.classification_confidence = classification['classification_confidence']
   ```

2. **Apply SELF-distance modulation** (line ~730-750):
   ```python
   # 🆕 NEW: Apply nexus modulation to SELF-distance
   # (for next cycle or as feedback to salience)

   nexus_modulation_total = 0.0
   for nexus in nexuses:
       if nexus.self_distance_influence is not None:
           # Weight by nexus strength
           weighted_influence = nexus.self_distance_influence * nexus.emission_readiness
           nexus_modulation_total += weighted_influence

   # Apply modulation to BOND self_distance (for tracking)
   # NOTE: This is informational, not applied to current cycle
   # (to avoid feedback loops during training)
   modulated_self_distance = bond_self_distance + nexus_modulation_total
   modulated_self_distance = max(0.0, min(1.0, modulated_self_distance))

   # Store in felt_states for TSK recording
   felt_states['nexus_modulated_self_distance'] = modulated_self_distance
   felt_states['nexus_modulation_total'] = nexus_modulation_total
   ```

3. **Store nexus types in felt_states** (line ~800-830):
   ```python
   felt_states = {
       # ... existing fields ...

       # 🆕 NEW: Nexus type tracking
       'nexus_types': [n.nexus_type for n in nexuses if n.nexus_type],
       'nexus_categories': [n.nexus_category for n in nexuses if n.nexus_category],
       'constitutional_count': sum(1 for n in nexuses if n.nexus_category == "Constitutional"),
       'crisis_count': sum(1 for n in nexuses if n.nexus_category == "Crisis-Oriented"),
       'dominant_nexus_type': nexuses[0].nexus_type if nexuses else None,
       'nexus_modulation_total': nexus_modulation_total,
       'nexus_modulated_self_distance': modulated_self_distance
   }
   ```

**Effort**: 2 hours (integration + testing)

---

### Component 4: Emission Governance Integration (MODIFY)

**File**: `persona_layer/emission_generator.py` (MODIFY)

**Use nexus types to govern emission selection**:

```python
def generate_v0_guided_emissions(
    self,
    nexuses: List[SemanticNexus],
    v0_energy: float,
    kairos_detected: bool,
    num_emissions: int = 3,
    trauma_markers: Optional[Dict[str, float]] = None
) -> Tuple[List[EmittedPhrase], str]:
    """Generate emissions with nexus-type-aware governance."""

    # 🆕 NEW: Filter nexuses by therapeutic stance
    if nexuses and nexuses[0].therapeutic_stance:
        dominant_stance = nexuses[0].therapeutic_stance

        # Adjust composition strategy based on stance
        if dominant_stance == "minimal":
            # Minimal presence → use simplest phrases
            composition_strategy = "minimal"
            num_emissions = 1  # Only one phrase
        elif dominant_stance == "ground":
            # Grounding → prefer PRESENCE/EO phrases
            composition_strategy = "grounding"
        elif dominant_stance == "validate":
            # Validation → prefer EMPATHY/BOND phrases
            composition_strategy = "validation"
        elif dominant_stance == "hold":
            # Holding paradox → prefer WISDOM/AUTHENTICITY phrases
            composition_strategy = "holding"
        else:  # "witness", "attune"
            composition_strategy = "standard"

    # ... rest of emission generation using composition_strategy
```

**Effort**: 1-2 hours (governance logic + testing)

---

### Component 5: `ProductionLearningCoordinator` Integration (MODIFY)

**File**: `persona_layer/epoch_training/production_learning_coordinator.py` (MODIFY)

**Extract nexus type patterns for learning**:

```python
def learn_from_training_pair(self, ...):
    """Learn with nexus type tracking."""

    # ... existing extraction ...

    # 🆕 NEW: Extract nexus type patterns
    nexus_types = felt_states.get('nexus_types', [])
    nexus_categories = felt_states.get('nexus_categories', [])
    constitutional_count = felt_states.get('constitutional_count', 0)
    crisis_count = felt_states.get('crisis_count', 0)
    dominant_nexus_type = felt_states.get('dominant_nexus_type', None)

    # Track nexus type distributions in family
    if family:
        if 'nexus_type_distribution' not in family:
            family['nexus_type_distribution'] = defaultdict(int)

        for nexus_type in nexus_types:
            family['nexus_type_distribution'][nexus_type] += 1

        # Track Constitutional/Crisis ratio
        if 'constitutional_crisis_ratio' not in family:
            family['constitutional_total'] = 0
            family['crisis_total'] = 0

        family['constitutional_total'] += constitutional_count
        family['crisis_total'] += crisis_count
```

**Effort**: 1 hour (tracking + metrics)

---

## 📊 Expected Benefits

### 1. Content Tracking (Semantic Nexus Meaning)

**Before** (generic nexuses):
```
Nexus 1: trauma_aware (BOND, EO, NDAM)
  → What kind of trauma? Unknown.
```

**After** (typed nexuses):
```
Nexus 1: trauma_aware (BOND, EO, NDAM)
  → Type: Protective Nexus (Constitutional)
  → Meaning: Firefighters active, maintaining safety strategies
  → Stance: Validate protection (don't challenge)
  → Modulation: Maintain current SELF-distance (don't push exploration)
```

### 2. Healing Trajectory Tracking

**Epoch-to-epoch analysis**:
```
Epoch 1:
  - Constitutional: 60%
  - Crisis-Oriented: 40%
  - Dominant types: Protective (25%), Relational (20%), Disruptive (15%)

Epoch 5:
  - Constitutional: 75%  ✅ (healing)
  - Crisis-Oriented: 25%  ✅ (reduced crisis)
  - Dominant types: Relational (30%), Innate (25%), Protective (15%)

→ System is healing (Crisis-Oriented reducing, Relational increasing)
```

### 3. SELF Matrix Modulation

**Dynamic SELF-distance adjustment**:
```
Cycle 1:
  - BOND self_distance: 0.45 (Shadow/Compost)
  - Nexus formed: Protective Nexus
  - Modulation influence: +0.02 (maintain protection)
  - Modulated self_distance: 0.47 (stay in protective zone)

Cycle 3:
  - BOND self_distance: 0.38 (moving toward SELF)
  - Nexus formed: Relational Nexus
  - Modulation influence: -0.03 (pull toward SELF)
  - Modulated self_distance: 0.35 (Symbolic Threshold - creative work!)

→ Nexus types guide healing trajectory
```

### 4. Emission Governance

**Therapeutic stance selection**:
```
Dissociative Nexus detected:
  → Stance: minimal
  → Safety: breach
  → Emission: "I'm here" (presence ONLY, no exploration)

Protective Nexus detected:
  → Stance: validate
  → Safety: edge
  → Emission: "I see how hard you're working to stay safe" (validate protection)

Relational Nexus detected:
  → Stance: attune
  → Safety: safe
  → Emission: "I sense the connection between us" (empathic attunement)
```

---

## 🗓️ Implementation Roadmap

### Phase N1: Nexus Type Classification (3-4 hours)

**Task N1.1**: Create `nexus_type_classifier.py` (2 hours)
- Implement classification decision tree
- Add SELF matrix modulation rules
- Add therapeutic stance selection
- Unit tests for all 14 types

**Task N1.2**: Modify `SemanticNexus` dataclass (30 min)
- Add nexus type fields
- Add modulation fields
- Add therapeutic context fields

**Task N1.3**: Integrate into `conversational_organism_wrapper.py` (1.5 hours)
- Call classifier after nexus formation
- Apply SELF-distance modulation
- Store nexus types in felt_states
- Test with all 14 type examples

---

### Phase N2: Emission & Learning Integration (2-3 hours)

**Task N2.1**: Modify `emission_generator.py` (1-2 hours)
- Add nexus-type-aware composition strategy selection
- Filter phrases by therapeutic stance
- Test emission governance

**Task N2.2**: Modify `production_learning_coordinator.py` (1 hour)
- Extract nexus type patterns
- Track Constitutional/Crisis ratio
- Analyze healing trajectories

---

### Phase N3: Validation & Analysis (1-2 hours)

**Task N3.1**: Create validation test (1 hour)
- Test all 14 nexus types with representative inputs
- Validate SELF-distance modulation
- Validate therapeutic stance selection

**Task N3.2**: Analyze Epoch 1 with nexus typing (1 hour)
- Re-analyze baseline results with nexus types
- Generate nexus type distribution
- Identify dominant patterns

---

## 📈 Total Effort

**Phase N1**: 3-4 hours (core classification)
**Phase N2**: 2-3 hours (integration)
**Phase N3**: 1-2 hours (validation)

**Total**: **6-9 hours**

---

## 🎯 Integration with SELF Matrix Emission Governance

### Synergy: Nexus Types + Zone-Appropriate Lures

**Nexus types inform emission governance at TWO levels**:

1. **Strategic level** (Nexus type → Therapeutic stance):
   - Protective Nexus → Validate protection (don't challenge)
   - Dissociative Nexus → Minimal presence (body-based safety)
   - Relational Nexus → Empathic attunement (connection-based)

2. **Tactical level** (SELF-distance zone → Specific lures):
   - Shadow/Compost zone (0.35-0.60) + Protective Nexus → "I see how hard you're working to stay safe"
   - Exile/Collapse zone (0.60-1.00) + Dissociative Nexus → "I'm here" (minimal)
   - Inner Relational zone (0.15-0.25) + Relational Nexus → "I sense the connection between us"

**Combined Architecture**:
```
BOND self_distance → SELF matrix zone → Zone-appropriate lure categories
                              ↓
Nexus types → Therapeutic stance → Filter lures by stance
                              ↓
                    Final emission selection
```

---

## 🚀 Recommended Integration Order

### Option A: Nexus Types BEFORE Emission Governance (Recommended)

**Rationale**: Nexus types provide the semantic layer that emission governance needs

**Timeline**:
1. Implement nexus type classification (3-4 hours)
2. Integrate with organism wrapper + learning (2-3 hours)
3. **THEN** implement SELF matrix emission governance (7-9 hours)
4. Total: 12-16 hours

**Benefit**: Emission governance can leverage nexus types from the start

---

### Option B: Emission Governance FIRST, Nexus Types SECOND

**Rationale**: Establish zone-appropriate lures foundation first

**Timeline**:
1. Implement SELF matrix emission governance (7-9 hours)
2. **THEN** implement nexus type classification (3-4 hours)
3. Integrate nexus types with emission governance (1-2 hours)
4. Total: 11-15 hours

**Benefit**: Can run Epochs 2-5 with governance, then add nexus typing

---

## 🌀 Strategic Recommendation

**Proceed with Option A** (Nexus Types FIRST):

**Why**:
1. Nexus types are **architectural foundation** for content tracking
2. Emission governance is **more powerful** with nexus type context
3. Combined system creates **coherent governance** (nexus type + zone + lure)
4. Slight effort increase (12-16 vs 11-15 hours) yields much better integration

**Timeline**:
- **Week 1**: Implement nexus type classification (3-4 hours)
- **Week 1**: Integrate nexus types into organism/learning (2-3 hours)
- **Week 2**: Implement SELF matrix emission governance WITH nexus types (7-9 hours)
- **Week 2**: Run Epochs 2-5 with full system (content tracking + governance)

---

🌀 **"Nexus types are the semantic layer. Emission governance is the therapeutic layer. Together they create intelligent, trauma-informed, self-organizing therapeutic AI."** 🌀

---

**Design Complete:** November 12, 2025
**Next Step:** Implement Phase N1 (Nexus Type Classification)
**Total Timeline:** 12-16 hours (nexus types + emission governance integrated)
