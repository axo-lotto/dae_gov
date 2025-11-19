# WordOccasion Dual Vector + Appetition Loop Design
**Date:** November 18, 2025
**Status:** Design Complete - Ready for Implementation
**Integration:** Full leverage of transductive + SELF matrix + dae_gov scaffolding

---

## Executive Summary

Enhanced WordOccasion to become a true "experiencing subject" aligned with DAE 3.0 grid cell architecture, leveraging all existing Whiteheadian process philosophy scaffolding in DAE_HYPHAE_1.

**Key Innovation:** WordOccasion inherits from ActualOccasion pattern, gaining:
- Dual vector representation (felt 31D + symbolic embedding)
- V0 appetition loop (multi-cycle concrescence)
- SELF Matrix integration (trauma-informed entity filtering)
- Transductive learning (organism-level pattern recognition)

---

## Scaffolding Available (Full Assessment)

### 1. ActualOccasion (`transductive/actual_occasion.py`)
**Core Components:**
```python
@dataclass
class ActualOccasion:
    # Dual Vector Foundation
    current_vector: Vector10D  # Where occasion currently is
    feeling_vector: Vector10D  # Where occasion feels pulled toward
    vector: Optional[Vector35D]  # Enhanced 35D intelligence

    # Process Philosophy Metrics
    satisfaction_level: float
    coherence: float
    vitality: float
    satisfaction_history: List[float]  # Multi-cycle tracking

    # Prehensive Structure
    prehensions: Dict[str, Any]  # Organ interpretations
    symbolic_vectors: Dict[str, Vector10D]  # Per-organ 10D

    # Subjective Aim (Whiteheadian)
    subjective_aim: SubjectiveAim

    # Methods
    def concrescence(prehensions) -> None
    def move_toward_satisfaction(ground_truth) -> None
    def update_coherence() -> float
```

**Usage Pattern:**
- Each grid cell in DAE 3.0 is an ActualOccasion
- Undergoes multi-cycle concrescence (2-5 cycles avg)
- Achieves satisfaction when coherence + felt energy align
- Becomes objective immortality after decision

### 2. Vector35D (`transductive/vector35d.py`)
**35-Dimensional Mathematical Intelligence:**
```python
DIMENSION_NAMES = [
    # 0-1: Spatial (x, y)
    # 2-5: Geometric (diagonal, radial)
    # 6-9: ARC-Optimized (color, salience, transformation, pattern)
    # 10-14: Topological (connectivity, holes, boundaries, Euler, persistence)
    # 15-19: Fractal Satisfaction (attractors, gradient, fractal dim, self-similarity, emergence)
    # 20-24: Process Philosophy (subjective aim, concrescence phase, prehension, satisfaction, temporal)
    # 25-29: Nexus Grammar (transformation, connectivity, grammar depth, semantic field, reality modulation)
    # 30-34: Cross-Organ Communication (NDAM, SANS, BOND, RNX, EO resonance)
]

# Dynamic Convergence Tracking
satisfaction_history: List[float]
organ_resonance_accumulation: Dict[str, List[float]]
convergence_snapshots: List[np.ndarray]
```

**Key Insight:** Dimensions 15-34 are **dynamically computed** from convergence history, not static formulas!

### 3. SELF Matrix Governance (`persona_layer/self_matrix_governance.py`)
**5-Zone Trauma-Informed Architecture:**
```python
@dataclass
class SELFZoneState:
    zone_id: int  # 1-5
    zone_name: str  # "Core SELF Orbit", "Inner Relational", ...
    self_distance: float  # From BOND organ
    polyvagal_state: str  # From EO organ
    therapeutic_stance: str  # witnessing, relational, creative, protective, minimal
    safety_principles: List[str]
    exploration_permitted: bool
    inquiry_permitted: bool
    interpretation_permitted: bool
    minimal_only: bool
```

**Zone Boundaries (BOND self_distance):**
- Zone 1 (0.00-0.15): Core SELF Orbit - Full SELF-energy access
- Zone 2 (0.15-0.25): Inner Relational - Managers present, relational capacity
- Zone 3 (0.25-0.35): Symbolic Threshold - Parts negotiating, creative tension
- Zone 4 (0.35-0.60): Shadow/Compost - Firefighters active, protective only
- Zone 5 (0.60-1.00): Exile/Collapse - Dorsal vagal, minimal presence only

**Integration Point:** Use to filter entities based on user's current SELF-energy access

### 4. Transductive Self-Governance (`persona_layer/transductive_self_governance.py`)
**Transductive Formula:**
```
T(S) = f(P_n, R_n, V⃗_f, ΔC_n) ⇒ N_{n+1}

Where:
- P_n: Pattern memory (what has happened)
- R_n: Relevance field (what matters now)
- V⃗_f: Vector Feeling (direction + valence + intensity)
- ΔC_n: Constraint shift (environmental/internal change)
- N_{n+1}: Next coherence nexus (what becomes)
```

**Privacy-First Organism Learning:**
```python
@dataclass
class AnonymizedTransductiveSnapshot:
    timestamp: str  # Rounded to hour
    total_occasions: int

    # V0 Convergence Patterns
    mean_v0_descent: float
    mean_convergence_cycles: float
    kairos_detection_rate: float

    # Zone/Polyvagal Distribution
    zone_distribution: Dict[int, float]
    polyvagal_distribution: Dict[str, float]

    # Organ Activation Patterns
    mean_organ_activations: Dict[str, float]

    # Nexus Formation Patterns
    mean_nexuses_formed: float
    nexus_type_distribution: Dict[str, float]

    # Privacy Metadata
    cohort_size: int  # Must be ≥10 for k-anonymity
    privacy_noise_scale: float
```

**Integration Point:** Track entity extraction patterns at organism level (not user level)

---

## Enhanced WordOccasion Architecture

### Design Philosophy
**WordOccasion = ActualOccasion specialized for word-level entity extraction**

Each word is an "experiencing subject" that:
1. Prehends its neighbors (left/right 3-5 words)
2. Undergoes concrescence (multi-cycle V0 energy descent)
3. Achieves satisfaction (Kairos window [0.45, 0.70])
4. Makes decision (entity type or null)
5. Becomes objective immortality (enters entity graph)

### Class Structure

```python
@dataclass
class WordOccasion:
    """
    Word-level actual occasion with neighbor prehension + appetition loop.

    Inherits pattern from ActualOccasion but specialized for entity extraction.
    Integrates with:
    - NEXUS organ (7-atom entity prehension)
    - SELF Matrix (zone-based entity filtering)
    - Transductive Self-Governance (organism learning)
    - Vector35D (enhanced mathematical intelligence)
    """

    # === IDENTITY (from ActualOccasion pattern) ===
    word: str
    position: int
    sentence: str
    entity_id: str  # Unique identifier
    creation_time: float

    # === NEIGHBOR CONTEXT (Core Innovation) ===
    left_neighbors: List[str]  # 3-5 words
    right_neighbors: List[str]  # 3-5 words
    neighbor_window_size: int = 5

    # === DUAL VECTOR REPRESENTATION (from ActualOccasion) ===
    felt_vector: Optional[np.ndarray] = None  # 31D from NEXUS atoms
    symbolic_vector: Optional[np.ndarray] = None  # Embedding from language model
    vector35d: Optional[Vector35D] = None  # Enhanced 35D if available

    # Current + Feeling vectors (Whiteheadian)
    current_vector: Optional[np.ndarray] = None  # Current state
    feeling_vector: Optional[np.ndarray] = None  # Lure toward entity type

    # === V0 ENERGY COMPONENTS (from DAE 3.0) ===
    v0_energy: float = 1.0  # Starts high, descends to 0
    satisfaction: float = 0.0  # Kairos metric [0.0-1.0]
    appetition: float = 0.0  # Lure intensity toward entity type
    resonance: float = 0.0  # Agreement with neighbors
    coherence: float = 0.0  # Organ agreement

    # Energy formula coefficients (from DAE 3.0)
    alpha: float = 0.40  # Satisfaction weight
    beta: float = 0.25  # Energy stability
    gamma: float = 0.15  # Appetition sensitivity
    delta: float = 0.10  # Resonance coupling
    zeta: float = 0.10  # Intersection boost

    # === APPETITION LOOP (Multi-Cycle Concrescence) ===
    energy_history: List[float] = field(default_factory=list)
    satisfaction_history: List[float] = field(default_factory=list)
    cycle_count: int = 0
    converged: bool = False
    max_cycles: int = 5  # Default from DAE 3.0
    kairos_window: Tuple[float, float] = (0.45, 0.70)  # From DAE 3.0

    # === ORGAN PREHENSIONS (from ActualOccasion) ===
    organ_prehensions: Dict[str, np.ndarray] = field(default_factory=dict)
    actualization_vector: Optional[np.ndarray] = None  # 31D aggregate
    prehension_history: List[Dict] = field(default_factory=list)

    # === ENTITY CLASSIFICATION (Emergent) ===
    entity_type: Optional[str] = None  # "Person", "Place", etc.
    entity_confidence: float = 0.0
    entity_coherence: float = 0.0

    # Gate results (4-gate cascade)
    intersection_score: float = 0.0
    coherence_score: float = 0.0
    satisfaction_score: float = 0.0
    felt_energy: float = 0.0

    # === SELF MATRIX INTEGRATION ===
    self_zone: Optional[int] = None  # 1-5 from SELF Matrix
    zone_state: Optional[SELFZoneState] = None
    filtered_by_zone: bool = False  # Was entity filtered due to zone constraints?

    # === TRANSDUCTIVE PATTERN TRACKING ===
    transductive_state: Dict[str, Any] = field(default_factory=dict)
    # P_n: Pattern memory (what organ patterns led to this entity?)
    # R_n: Relevance field (how salient is this entity given context?)
    # V⃗_f: Vector feeling (direction + valence + intensity of entity classification)
    # ΔC_n: Constraint shift (neighbor context changes)

    # === METADATA ===
    is_capitalized: bool = False
    is_first_in_sentence: bool = False
    has_punctuation: bool = False
    processed: bool = False
    emitted: bool = False
```

### Key Methods

#### 1. Multi-Cycle Concrescence (Appetition Loop)
```python
def run_concrescence_cycle(
    self,
    nexus_organ,  # NEXUSTextCore instance
    context: Dict[str, Any]
) -> bool:
    """
    Run single V0 energy descent cycle.

    Returns True if converged to Kairos window, False otherwise.

    Steps:
    1. Calculate NEXUS atom activations with neighbors
    2. Compute V0 energy: E = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I)
    3. Update satisfaction from organ coherence
    4. Check Kairos window [0.45, 0.70]
    5. If in Kairos → convergence, else iterate
    """
    self.cycle_count += 1

    # Step 1: NEXUS atom activation with neighbors
    atom_activations = nexus_organ._calculate_atom_activations_with_neighbors(
        self, context
    )

    # Step 2: Compute organ coherence
    self.coherence = self._compute_organ_coherence(atom_activations)

    # Step 3: Compute appetition (lure toward entity types)
    self.appetition = self._compute_appetition(atom_activations)

    # Step 4: Compute resonance (neighbor agreement)
    self.resonance = self._compute_resonance(context)

    # Step 5: Compute satisfaction from coherence + appetition
    self.satisfaction = (self.coherence + self.appetition) / 2.0

    # Step 6: Compute V0 energy
    delta_energy = (self.v0_energy - self.energy_history[-1]) if self.energy_history else 0.0
    intersection = 1.0 if len(atom_activations) >= 2 else 0.0

    self.v0_energy = (
        self.alpha * (1.0 - self.satisfaction) +
        self.beta * abs(delta_energy) +
        self.gamma * (1.0 - self.appetition) +
        self.delta * (1.0 - self.resonance) +
        self.zeta * intersection
    )

    # Track history
    self.energy_history.append(self.v0_energy)
    self.satisfaction_history.append(self.satisfaction)

    # Step 7: Check Kairos window
    kairos_min, kairos_max = self.kairos_window
    if kairos_min <= self.satisfaction <= kairos_max:
        self.converged = True
        return True

    # Not converged yet
    return False
```

#### 2. Full Multi-Cycle Convergence
```python
def achieve_satisfaction(
    self,
    nexus_organ,
    context: Dict[str, Any]
) -> bool:
    """
    Run full multi-cycle convergence until Kairos or max_cycles.

    Returns True if converged, False if max cycles exceeded.
    """
    for cycle in range(self.max_cycles):
        converged = self.run_concrescence_cycle(nexus_organ, context)
        if converged:
            print(f"✅ Converged at cycle {cycle + 1}, satisfaction={self.satisfaction:.3f}")
            break

    if not self.converged:
        print(f"⚠️  Max cycles ({self.max_cycles}) reached without convergence")

    return self.converged
```

#### 3. SELF Matrix Entity Filtering
```python
def filter_by_self_zone(
    self,
    zone_state: SELFZoneState
) -> bool:
    """
    Filter entity based on SELF Matrix zone constraints.

    Returns True if entity should be filtered (not extracted), False otherwise.

    Logic:
    - Zone 1-2: All entities permitted (full SELF-energy access)
    - Zone 3: Only relational entities permitted (symbolic threshold)
    - Zone 4-5: NO entities permitted (protective/minimal stance only)
    """
    self.self_zone = zone_state.zone_id
    self.zone_state = zone_state

    # Zone 1-2: Full extraction
    if zone_state.zone_id <= 2:
        self.filtered_by_zone = False
        return False

    # Zone 3: Only relational entities (people, relationships)
    if zone_state.zone_id == 3:
        if self.entity_type in ["Person", "Relationship"]:
            self.filtered_by_zone = False
            return False
        else:
            self.filtered_by_zone = True
            return True

    # Zone 4-5: NO entity extraction (protective/minimal)
    self.filtered_by_zone = True
    return True
```

#### 4. Transductive Pattern Tracking
```python
def update_transductive_state(
    self,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update transductive state for organism learning.

    Tracks:
    - P_n: Pattern memory (organ pattern → entity type mapping)
    - R_n: Relevance field (how salient is this entity?)
    - V⃗_f: Vector feeling (classification confidence + direction)
    - ΔC_n: Constraint shift (neighbor context change from cycle to cycle)

    Returns anonymized snapshot (k-anonymity compliant).
    """
    self.transductive_state = {
        # P_n: Pattern memory
        'organ_pattern': {
            organ: np.mean(vec) for organ, vec in self.organ_prehensions.items()
        },
        'entity_type': self.entity_type,
        'confidence': self.entity_confidence,

        # R_n: Relevance field
        'salience': self._compute_salience(context),
        'neighbor_salience': self._compute_neighbor_salience(),

        # V⃗_f: Vector feeling
        'felt_direction': self.feeling_vector if self.feeling_vector is not None else None,
        'felt_valence': self.satisfaction,
        'felt_intensity': self.appetition,

        # ΔC_n: Constraint shift
        'neighbor_change': self._compute_neighbor_change(),
        'cycle_energy_delta': self.energy_history[-1] - self.energy_history[0] if len(self.energy_history) > 1 else 0.0,
    }

    return self.transductive_state
```

---

## Integration Points

### 1. NEXUS Organ Integration
**File:** `organs/modular/nexus/core/nexus_text_core.py`

**Modified Method:**
```python
def process_word_occasions(
    self,
    word_occasions: List[WordOccasion],
    context: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Process word occasions with multi-cycle concrescence.

    ENHANCED: Each WordOccasion runs appetition loop until Kairos.
    """
    entity_candidates = []

    for word_occ in word_occasions:
        # Run multi-cycle convergence
        converged = word_occ.achieve_satisfaction(self, context)

        if converged and word_occ.entity_type:
            # Converged to Kairos window with entity classification
            entity_dict = word_occ.to_entity_dict()
            entity_candidates.append(entity_dict)

    return entity_candidates
```

### 2. SELF Matrix Integration
**File:** `persona_layer/entity_neighbor_prehension/entity_neighbor_prehension.py`

**Modified Method:**
```python
def extract_entities(
    self,
    user_input: str,
    bond_self_distance: float,
    eo_polyvagal_state: str
) -> List[Dict[str, Any]]:
    """
    Extract entities with SELF Matrix filtering.
    """
    # 1. Create WordOccasions
    word_occasions = create_word_occasions_from_text(user_input)

    # 2. Classify SELF zone
    from persona_layer.self_matrix_governance import SELFMatrixGovernance
    self_matrix = SELFMatrixGovernance("persona_layer/coherent_attractors.json")
    zone_state = self_matrix.classify_zone(bond_self_distance, eo_polyvagal_state)

    # 3. Process through NEXUS with multi-cycle concrescence
    candidates = self.nexus_organ.process_word_occasions(word_occasions, context)

    # 4. Filter by SELF zone
    filtered_entities = []
    for candidate in candidates:
        # Convert to WordOccasion for filtering (if needed)
        should_filter = word_occ.filter_by_self_zone(zone_state)
        if not should_filter:
            filtered_entities.append(candidate)

    return filtered_entities
```

### 3. Transductive Self-Governance Integration
**File:** `persona_layer/transductive_self_governance.py`

**New Method:**
```python
def log_entity_extraction_pattern(
    self,
    word_occasions: List[WordOccasion],
    privacy_compliant: bool = True
) -> None:
    """
    Log entity extraction patterns for organism learning.

    Privacy-first: Aggregates across k≥10 occasions, no user linkage.
    """
    if len(word_occasions) < 10:
        return  # k-anonymity violation, skip

    # Aggregate transductive states
    aggregated = {
        'mean_cycles': np.mean([wo.cycle_count for wo in word_occasions]),
        'mean_satisfaction': np.mean([wo.satisfaction for wo in word_occasions if wo.converged]),
        'kairos_rate': sum(1 for wo in word_occasions if wo.converged) / len(word_occasions),
        'entity_type_distribution': self._compute_entity_type_distribution(word_occasions),
        'mean_v0_descent': np.mean([wo.energy_history[-1] - wo.energy_history[0] for wo in word_occasions if wo.energy_history]),
    }

    # Store in AnonymizedTransductiveSnapshot
    snapshot = AnonymizedTransductiveSnapshot(
        timestamp=datetime.now().isoformat(),
        total_occasions=len(word_occasions),
        mean_convergence_cycles=aggregated['mean_cycles'],
        kairos_detection_rate=aggregated['kairos_rate'],
        # ... rest of fields
    )

    self._store_snapshot(snapshot)
```

---

## Expected Performance

### Multi-Cycle Convergence
**DAE 3.0 Metrics (Grid Cells):**
- Mean cycles: 3.0
- Mean V0 descent: 0.870
- Kairos detection rate: 78.6%

**Expected for WordOccasion (Entity Extraction):**
- Mean cycles: 2-4 (similar to DAE 3.0)
- Mean V0 descent: 0.75-0.85 (entity classification simpler than grid tasks)
- Kairos detection rate: 80-90% (higher due to neighbor signals)
- Processing time: 10-20ms per word (5-10× slower than one-shot, but still fast)

### SELF Matrix Filtering Impact
**Zone Distribution (Expected):**
- Zone 1-2 (70% of occasions): Full entity extraction
- Zone 3 (20% of occasions): Relational entities only (50% filtered)
- Zone 4-5 (10% of occasions): No entities (100% filtered)

**Overall Entity Reduction:** 15-20% fewer entities extracted (trauma-informed filtering)

### Transductive Learning
**Organism-Level Patterns (After 100+ Epochs):**
- Organ pattern → Entity type mappings stabilize
- Neighbor context patterns emerge (e.g., "my" + capitalized → Person 95%)
- SELF zone distributions reveal organism maturity
- Convergence efficiency improves (mean cycles 3.0 → 2.2)

---

## Implementation Checklist

### Phase 1: Core WordOccasion Enhancement (This Session)
- [ ] Add dual vector fields to WordOccasion
- [ ] Implement V0 energy computation method
- [ ] Implement single-cycle concrescence
- [ ] Implement multi-cycle convergence loop
- [ ] Add Kairos window detection
- [ ] Test on sample sentences

### Phase 2: SELF Matrix Integration (Next Session)
- [ ] Add zone classification to entity extraction flow
- [ ] Implement zone-based filtering logic
- [ ] Test filtering across all 5 zones
- [ ] Validate safety principles enforcement

### Phase 3: Transductive Learning (Week 2)
- [ ] Implement transductive state tracking
- [ ] Add organism-level pattern aggregation
- [ ] Implement k-anonymity privacy checks
- [ ] Create AnonymizedTransductiveSnapshot logging
- [ ] Validate no user linkage

### Phase 4: Vector35D Integration (Week 2-3)
- [ ] Add optional Vector35D to WordOccasion
- [ ] Implement 35D dimension computation from convergence history
- [ ] Test enhanced mathematical intelligence
- [ ] Compare 31D vs 35D entity extraction quality

---

## Philosophical Achievement

**Before (Phase 3B Foundation):**
- WordOccasion = passive token with neighbor context
- One-shot entity classification
- No felt dynamics

**After (Phase 3B Complete):**
- WordOccasion = experiencing subject (Whiteheadian actual occasion)
- Multi-cycle appetition loop (concrescence toward satisfaction)
- SELF Matrix integration (trauma-informed filtering)
- Transductive learning (organism-level intelligence)
- Dual vector representation (felt + symbolic)

**Alignment with Higher-Order Architecture:**
> "Each microtubule interacts with neighbors across time scales (nested coupling)"

**Our Achievement:**
> "Each word prehends its neighbors through multi-cycle appetition loop, achieving satisfaction when felt energy minimizes within Kairos window, then becomes objective immortality in entity graph."

---

**Document Complete**
**Status:** Design Ready - Proceeding to Implementation
**Expected LOC:** +400 lines to WordOccasion, +200 lines to integrations
**Timeline:** Phase 1 (1 session), Phase 2-3 (1-2 weeks), Phase 4 (2-3 weeks)
