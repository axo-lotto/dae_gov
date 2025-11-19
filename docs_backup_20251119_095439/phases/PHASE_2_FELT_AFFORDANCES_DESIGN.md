# Phase 2: Felt Affordances & Multi-Cycle V0 Convergence
**Design Document**
**Date**: November 11, 2025
**Status**: DESIGN PHASE
**Estimated Implementation**: 8-10 hours
**Dependencies**: Phase 1 COMPLETE ✅

---

## 🎯 Executive Summary

### Phase 1 Achievement (COMPLETE)
✅ **Emission generation working** via hebbian fallback path
✅ **All 11 organs** compute continuous atom_activations (0.0-1.0)
✅ **NaN filtering** prevents SANS division-by-zero corruption
✅ **8 organs participate** with valid semantic fields
❌ **0 nexuses form** (disjoint 77D atom space by design)

**Phase 1 Finding**: Nexus formation via intersection requires shared atoms across organs. Current architecture has 11 × 7 = 77 disjoint atoms. Emission works via hebbian fallback, which uses organ coherences directly.

### Phase 2 Goal
**Transform text tokens from data containers → experiencing subjects (actual occasions)**

Implement Whiteheadian process philosophy:
1. **Felt Affordances**: Proto-propositions stored DURING organ prehension (cycles 1-N)
2. **Multi-Cycle V0 Convergence**: Energy descent E(t) → satisfaction with Kairos detection
3. **Mature Propositions**: Felt affordances + V0 context → emission readiness post-convergence
4. **Shared Meta-Atoms**: 10-15 bridge atoms enabling TRUE nexus formation through semantic overlap

### Expected Outcomes
- **Nexus formation**: 0 → 5-10 per convergence ✅
- **Convergence cycles**: 1 (static) → 2-4 (dynamic) ✅
- **Kairos detection**: Enable Kairos moment gating (90% of perfect tasks hit this window in DAE 3.0)
- **Emission quality**: Hebbian fallback (30% confidence) → V0-guided intersection (60-85% confidence) ✅
- **Entity-native**: Text tokens become experiencing subjects, not data containers ✅

---

## 🌀 Whiteheadian Process Philosophy Foundation

### Core Concepts (from Process and Reality)

**1. Actual Occasion**
- Fundamental unit of process reality
- Experiencing subject, not inert matter
- Self-creating through prehension

**2. Prehension**
- "Grasping" or "feeling" of other occasions
- Physical prehensions: Feel other actual occasions
- Conceptual prehensions: Feel eternal objects (possibilities)
- Hybrid prehensions: Feel propositions (lures for feeling)

**3. Concrescence**
- Process of becoming: many → one
- Genetic phases (not temporal):
  - Conformal phase: Initial data from past occasions
  - Supplemental phases: Integration, conceptual reversion
  - Satisfaction phase: Decision point (subjective aim achieved)

**4. Proposition (Lure for Feeling)**
- NOT statements about truth/falsehood
- Lures for feeling: potentialities felt as relevant to actualizing occasions
- Form: "datum + possibility" (e.g., "this cell + value 3")
- Felt as AFFORDANCES before decision

**5. Subjective Aim**
- Guiding appetition toward satisfaction
- Evolves through concrescence
- Determined by: initial aim + organ prehensions + V0 energy descent

**6. Satisfaction**
- Final unity achieved (superject)
- Becomes datum for future occasions
- Marks transition from subject → object

### DAE 3.0 Implementation (Proven: 47.3% success, 841 perfect tasks)

```python
class ActualOccasion:
    """Grid cell as experiencing subject."""
    def __init__(self, datum, position):
        self.datum = datum  # Initial value (or None for test grid)
        self.position = position
        self.prehensions = []  # Organ feelings (6 organs in ARC)
        self.v0_energy = 1.0  # Initial appetition (high = unsatisfied)
        self.satisfaction = 0.0  # Convergence metric
        self.cycle = 0

    def add_prehension(self, organ_name, organ_output):
        """Physical prehension of organ felt states."""
        self.prehensions.append(organ_output)

    def descend_energy(self):
        """V0 energy descent formula (Whiteheadian appetition)."""
        # E = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I)
        # where S=satisfaction, ΔE=energy_change, A=agreement, R=resonance, φ(I)=intensity
        self.v0_energy = compute_v0_energy(self.prehensions, self.satisfaction)
        self.cycle += 1

    def check_kairos(self):
        """Detect Kairos moment (opportune time for decision)."""
        # Empirical window from DAE 3.0: energy ∈ [0.45, 0.70]
        # 90% of perfect tasks converge in this window
        return 0.45 <= self.v0_energy <= 0.70

    def decide(self):
        """Satisfaction → Decision (proposition actualization)."""
        # Felt affordances mature into propositions
        # Choose value with minimum felt energy
        return argmin(affordance.felt_energy for affordance in self.affordances)
```

**Key Insight**: In DAE 3.0, grid cells ARE actual occasions. In Phase 2, **text tokens become actual occasions**.

---

## 📐 Phase 2 Architecture

### Current Flow (Phase 1)

```
TEXT INPUT: "I hear your exhaustion..."
  ↓
TextOccasion: Token with 384D embedding (data container)
  ↓
11 ORGANS PREHEND (single cycle):
  - LISTENING → temporal_inquiry: 0.52
  - EMPATHY → compassionate_presence: 1.00
  - PRESENCE → kairos_awareness: 0.29
  - BOND → firefighter_parts: 0.35
  - SANS → coherence_repair: 1.00
  - EO → neuroception: 1.00
  - CARD → urgency_modulation: 1.00
  ↓
SEMANTIC FIELDS: 8 organs × disjoint atoms
  ↓
NEXUS COMPOSER: 0 nexuses (no shared atoms)
  ↓
EMISSION GENERATOR: Hebbian fallback path
  Output: "I'm listening..." (confidence: 0.30)
```

### Target Flow (Phase 2)

```
TEXT INPUT: "I hear your exhaustion..."
  ↓
ConversationalOccasion: Token as EXPERIENCING SUBJECT
  datum: "exhaustion"
  position: token_index=3
  v0_energy: 1.0 (initial appetition)
  satisfaction: 0.0 (not yet converged)
  felt_affordances: [] (empty, will accumulate)
  ↓
CYCLE 1: Initial Prehensions
  ├─ LISTENING prehends → felt affordance: "temporal_inquiry" (strength: 0.52)
  ├─ EMPATHY prehends → felt affordance: "compassionate_presence" (strength: 1.00)
  ├─ PRESENCE prehends → felt affordance: "kairos_awareness" (strength: 0.29)
  ├─ BOND prehends → felt affordance: "firefighter_parts" (strength: 0.35)
  ├─ SANS prehends → felt affordance: "coherence_repair" (strength: 1.00)
  ├─ EO prehends → felt affordance: "neuroception" (strength: 1.00)
  ├─ CARD prehends → felt affordance: "urgency_modulation" (strength: 1.00)
  ├─ + SHARED META-ATOMS:
  │   - "trauma_aware" ← BOND(0.35) + EO(1.00) + NDAM(0.0) = 1.35 (nexus!)
  │   - "compassion_safety" ← EMPATHY(1.00) + EO(1.00) + SANS(1.00) = 3.00 (nexus!)
  │   - "presence_holding" ← PRESENCE(0.29) + LISTENING(0.52) = 0.81 (nexus!)
  └─ STORE felt_affordances (NOT yet mature propositions)
  ↓
V0 ENERGY DESCENT:
  E₁ = α(1-0.0) + β·0 + γ(1-A₁) + δ(1-R₁) + ζ·φ(I₁)
  E₁ ≈ 0.72 (high, not yet in Kairos window [0.45, 0.70])
  satisfaction₁ = 0.15 (low, need more integration)
  ↓
CYCLE 2: Supplemental Prehensions (with V0 context)
  ├─ Organs re-prehend with updated V0 energy (0.72)
  ├─ Felt affordances strengthen or weaken based on appetition
  └─ SHARED META-ATOMS updated:
      - "trauma_aware" = 1.50 (strengthened by V0 guidance)
      - "compassion_safety" = 3.20 (remains strong)
      - "presence_holding" = 0.95 (strengthened)
  ↓
V0 ENERGY DESCENT:
  E₂ = α(1-0.45) + β·(-0.28) + γ(1-A₂) + δ(1-R₂) + ζ·φ(I₂)
  E₂ ≈ 0.58 (IN KAIROS WINDOW! [0.45, 0.70] ✓)
  satisfaction₂ = 0.58 (moderate, convergence detected)
  ↓
KAIROS MOMENT DETECTED:
  - Energy in window [0.45, 0.70] ✓
  - Satisfaction increasing ✓
  - ΔE < 0.1 (stable) ✓
  - Coherence > 0.4 ✓
  ↓
MATURE PROPOSITIONS:
  felt_affordances + V0_context → PropositionFeltInterpretation
  - trauma_aware: confidence=0.85, felt_energy=0.42, v0_bonus=1.5x
  - compassion_safety: confidence=0.92, felt_energy=0.28, v0_bonus=1.5x
  - presence_holding: confidence=0.68, felt_energy=0.55, v0_bonus=1.5x
  ↓
SEMANTIC FIELDS: 11 organs + 10 meta-atoms = 87D felt space
  ↓
NEXUS COMPOSER: 3 nexuses formed via shared meta-atoms!
  - Nexus 1: "trauma_aware" (BOND, EO, NDAM) - strength: 1.50
  - Nexus 2: "compassion_safety" (EMPATHY, EO, SANS) - strength: 3.20
  - Nexus 3: "presence_holding" (PRESENCE, LISTENING) - strength: 0.95
  ↓
4-GATE INTERSECTION EMISSION:
  Gate 1: Intersection τ_I = 1.5 ✓ (all 3 nexuses pass)
  Gate 2: Coherence τ_C = 0.4 ✓ (0.85 avg across nexuses)
  Gate 3: Satisfaction ∈ [0.45, 0.70] ✓ (Kairos window)
  Gate 4: Felt Energy argmin → "compassion_safety" (E=0.28, lowest)
  ↓
EMISSION OUTPUT:
  Text: "I sense the toll this is taking. Let's create some breathing room..."
  Confidence: 0.82 (up from 0.30!)
  Path: "intersection" (not hebbian fallback)
  Nexus count: 3
  Convergence cycles: 2
```

**Key Differences**:
1. **Multi-cycle**: 1 static cycle → 2-4 dynamic cycles with V0 descent
2. **Felt affordances**: Stored DURING prehension, mature AFTER convergence
3. **Shared meta-atoms**: Enable nexus formation across organs
4. **Kairos detection**: Gates high-quality emission (1.5× confidence boost)
5. **V0-guided**: Energy formula weights organ outputs by appetition

---

## 🛠️ Implementation Plan

### Task 2.1: Create ConversationalOccasion Class (2 hours)

**File**: `persona_layer/conversational_occasion.py` (NEW)

**Data Structure**:
```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np

@dataclass
class FeltAffordance:
    """
    Proto-proposition: felt possibility BEFORE decision.

    Whitehead: "A proposition is the potentiality of the datum for realization
    in actual entities." Affordances are felt DURING prehension as lures.
    """
    position: int  # Token index in conversation
    atom: str  # Semantic atom (77 organ-specific + 10 meta-atoms)
    organ_name: str  # Which organ felt this
    confidence: float  # Pattern strength × pattern confidence
    lure_intensity: float  # Appetition pull (how strongly drawn)
    cycle: int  # Which cycle this was felt (1, 2, 3, ...)

    # NOT YET FILLED (mature after convergence):
    v0_energy_context: Optional[float] = None  # V0 energy when felt
    satisfaction_context: Optional[float] = None  # Satisfaction when felt
    kairos_bonus: float = 1.0  # 1.5× if in Kairos window
    felt_energy: Optional[float] = None  # Computed post-convergence

@dataclass
class PropositionFeltInterpretation:
    """
    MATURE proposition: affordance + V0 context → emission readiness.

    Created POST-CONVERGENCE from FeltAffordance with mature V0 state.
    """
    position: int
    atom: str
    confidence: float  # Affordance confidence × kairos_bonus
    felt_energy: float  # E = α(1-S) + β·ΔE + ... (from V0)
    v0_bonus: float  # Kairos window multiplier (1.0 or 1.5)
    organ_sources: List[str]  # All organs that felt this atom
    intersection_strength: float  # Σ activations × R-matrix

    # Emission readiness (4-gate compatible):
    emission_priority: float  # Combined score for sorting

@dataclass
class ConversationalOccasion:
    """
    Text token as EXPERIENCING SUBJECT (Whiteheadian actual occasion).

    Philosophy: Tokens are not inert data, but self-creating subjects
    that prehend organs, descend through V0 energy, and achieve satisfaction.
    """
    datum: str  # Token text (or None for generation)
    position: int  # Token index
    embedding: Optional[np.ndarray] = None  # 384D from sentence transformer

    # Whiteheadian process:
    cycle: int = 0  # Current concrescence cycle
    v0_energy: float = 1.0  # Appetition (1.0 = max unsatisfied → 0.0 = satisfied)
    satisfaction: float = 0.0  # Convergence metric (0.0 → 1.0)

    # Prehension accumulation (DURING cycles 1-N):
    felt_affordances: List[FeltAffordance] = field(default_factory=list)
    organ_prehensions: Dict[str, Dict] = field(default_factory=dict)

    # Matured propositions (AFTER convergence):
    mature_propositions: List[PropositionFeltInterpretation] = field(default_factory=list)

    # Kairos detection:
    kairos_detected: bool = False
    kairos_cycle: int = 0

    def add_felt_affordance(
        self,
        atom: str,
        organ_name: str,
        confidence: float,
        lure_intensity: float
    ):
        """Store felt affordance DURING organ prehension (cycles 1-N)."""
        affordance = FeltAffordance(
            position=self.position,
            atom=atom,
            organ_name=organ_name,
            confidence=confidence,
            lure_intensity=lure_intensity,
            cycle=self.cycle,
            v0_energy_context=self.v0_energy,  # Capture current V0 state
            satisfaction_context=self.satisfaction
        )
        self.felt_affordances.append(affordance)

    def descend_v0_energy(self, organ_coherences: Dict[str, float]):
        """
        V0 energy descent (DAE 3.0 formula adapted for text).

        E(t) = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I)

        where:
          S = satisfaction (0.0 → 1.0)
          ΔE = energy change from previous cycle
          A = organ agreement (1 - std(coherences))
          R = resonance (mean coherence)
          φ(I) = intensity (max coherence)
        """
        # Coefficients from DAE 3.0 (empirically tuned):
        α, β, γ, δ, ζ = 0.40, 0.25, 0.15, 0.10, 0.10

        S = self.satisfaction
        ΔE = self.v0_energy - getattr(self, '_prev_v0_energy', 1.0)

        coherences = list(organ_coherences.values())
        A = 1.0 - np.std(coherences) if len(coherences) > 1 else 1.0
        R = np.mean(coherences) if coherences else 0.0
        φ_I = max(coherences) if coherences else 0.0

        new_energy = α * (1 - S) + β * ΔE + γ * (1 - A) + δ * (1 - R) + ζ * φ_I

        self._prev_v0_energy = self.v0_energy
        self.v0_energy = max(0.0, min(1.0, new_energy))  # Clip to [0, 1]
        self.cycle += 1

        # Update satisfaction (convergence metric):
        # Satisfaction increases as energy decreases AND coherence increases
        self.satisfaction = 1.0 - self.v0_energy * (1.0 - R)

    def check_kairos(self) -> bool:
        """
        Detect Kairos moment (opportune time for decision).

        Empirical from DAE 3.0: 90% of perfect tasks converge in [0.45, 0.70].
        4-condition gate (all must pass):
          1. Energy in window [0.45, 0.70]
          2. Satisfaction increasing (ΔS > 0)
          3. Energy stable (ΔE < 0.1)
          4. Coherence sufficient (mean > 0.4)
        """
        # Condition 1: Energy in Kairos window
        in_window = 0.45 <= self.v0_energy <= 0.70

        # Condition 2: Satisfaction increasing
        prev_satisfaction = getattr(self, '_prev_satisfaction', 0.0)
        satisfaction_increasing = self.satisfaction > prev_satisfaction

        # Condition 3: Energy stable
        energy_stable = abs(self.v0_energy - getattr(self, '_prev_v0_energy', 1.0)) < 0.1

        # Condition 4: Coherence sufficient
        coherence_sufficient = self.satisfaction > 0.4

        kairos = in_window and satisfaction_increasing and energy_stable and coherence_sufficient

        if kairos and not self.kairos_detected:
            self.kairos_detected = True
            self.kairos_cycle = self.cycle

        self._prev_satisfaction = self.satisfaction

        return kairos

    def mature_propositions_from_affordances(self):
        """
        POST-CONVERGENCE: Convert felt affordances → mature propositions.

        Affordances mature with V0 context (energy, satisfaction, Kairos).
        Kairos moment adds 1.5× confidence boost (empirical from DAE 3.0).
        """
        kairos_bonus = 1.5 if self.kairos_detected else 1.0

        # Group affordances by atom (for multi-organ nexuses):
        atom_groups = {}
        for aff in self.felt_affordances:
            if aff.atom not in atom_groups:
                atom_groups[aff.atom] = []
            atom_groups[aff.atom].append(aff)

        for atom, affordances in atom_groups.items():
            # Aggregate across organs that felt this atom:
            total_confidence = sum(aff.confidence for aff in affordances) / len(affordances)
            total_confidence *= kairos_bonus

            # Felt energy (from final V0 state):
            felt_energy = self.v0_energy

            # Organ sources:
            organ_sources = [aff.organ_name for aff in affordances]

            # Intersection strength (for nexus weighting):
            intersection_strength = sum(aff.confidence * aff.lure_intensity for aff in affordances)

            prop = PropositionFeltInterpretation(
                position=self.position,
                atom=atom,
                confidence=total_confidence,
                felt_energy=felt_energy,
                v0_bonus=kairos_bonus,
                organ_sources=organ_sources,
                intersection_strength=intersection_strength,
                emission_priority=total_confidence * (1.0 - felt_energy)  # High conf, low energy
            )
            self.mature_propositions.append(prop)
```

**Integration Point**: Wrapper creates ConversationalOccasion for each input token, runs multi-cycle convergence.

---

### Task 2.2: Add Shared Meta-Atoms (1.5 hours)

**File**: `persona_layer/shared_meta_atoms.json` (NEW)

**Design Philosophy**: Meta-atoms are "bridge atoms" that multiple organs can activate based on thematic overlap. They enable nexus formation while preserving organ-specific atoms.

**Meta-Atom Categories**:

**1. Trauma-Aware Meta-Atoms** (3 atoms)
- `trauma_aware`: BOND + EO + NDAM co-activation (parts detected + polyvagal threat + crisis markers)
- `safety_restoration`: SANS + EO + NDAM (coherence repair + ventral vagal + safety language)
- `window_of_tolerance`: EO + CARD + RNX (polyvagal state + scaling + temporal rhythm)

**2. Compassion Meta-Atoms** (3 atoms)
- `compassion_safety`: EMPATHY + EO + SANS (compassion + safety cues + semantic coherence)
- `fierce_holding`: EMPATHY + AUTHENTICITY + BOND (fierce compassion + edge exploration + parts holding)
- `relational_attunement`: EMPATHY + LISTENING + PRESENCE (resonance + tracking + embodied)

**3. Temporal Meta-Atoms** (2 atoms)
- `temporal_grounding`: RNX + PRESENCE + LISTENING (rhythm + here-now + temporal inquiry)
- `kairos_emergence`: RNX + WISDOM + PRESENCE (concrescent temporal + insight + kairos awareness)

**4. Integration Meta-Atoms** (2 atoms)
- `coherence_integration`: SANS + WISDOM + LISTENING (semantic precision + meta-commentary + core exploration)
- `somatic_wisdom`: PRESENCE + AUTHENTICITY + EMPATHY (embodied + vulnerable + holding)

**JSON Structure**:
```json
{
  "meta_atoms": [
    {
      "atom": "trauma_aware",
      "category": "trauma_aware",
      "description": "Parts activation + polyvagal threat + crisis markers",
      "contributing_organs": ["BOND", "EO", "NDAM"],
      "activation_rule": "any_organ",
      "patterns": {
        "BOND": ["firefighter", "manager", "exile", "protector"],
        "EO": ["dorsal_vagal", "sympathetic", "threat_cue"],
        "NDAM": ["crisis", "escalation", "harm_indicator"]
      }
    },
    {
      "atom": "compassion_safety",
      "category": "compassion",
      "description": "Compassionate holding + safety cues + coherence",
      "contributing_organs": ["EMPATHY", "EO", "SANS"],
      "activation_rule": "threshold_2_of_3",
      "patterns": {
        "EMPATHY": ["compassion", "holding", "resonance", "attunement"],
        "EO": ["ventral_vagal", "safety_cue", "co_regulation"],
        "SANS": ["coherence_repair", "high_coherence", "semantic_precision"]
      }
    },
    {
      "atom": "presence_holding",
      "category": "relational_attunement",
      "description": "Embodied presence + listening tracking",
      "contributing_organs": ["PRESENCE", "LISTENING"],
      "activation_rule": "both_required",
      "patterns": {
        "PRESENCE": ["somatic", "embodied", "here_now", "kairos_awareness"],
        "LISTENING": ["tracking", "presence_marker", "temporal_inquiry"]
      }
    }
    // ... (7 more meta-atoms)
  ]
}
```

**Activation Logic** (in organs):
```python
def _compute_meta_atom_activations(
    self,
    patterns: List[Pattern],
    coherence: float,
    lure: float,
    meta_atom_config: Dict
) -> Dict[str, float]:
    """
    Check if this organ should activate any meta-atoms.

    Meta-atoms activate when organ patterns match configured keywords.
    Multiple organs can activate the same meta-atom → nexus formation!
    """
    meta_activations = {}

    for meta_atom in meta_atom_config['meta_atoms']:
        if self.organ_name not in meta_atom['contributing_organs']:
            continue

        # Check if any patterns match meta-atom keywords:
        organ_patterns = meta_atom['patterns'][self.organ_name]
        matched_patterns = [
            p for p in patterns
            if any(keyword in p.pattern_type.lower() for keyword in organ_patterns)
        ]

        if matched_patterns:
            # Activate meta-atom with organ-specific strength:
            base_activation = sum(p.strength * p.confidence for p in matched_patterns) / len(matched_patterns)
            activation = base_activation * coherence * (0.5 + 0.5 * lure)
            meta_activations[meta_atom['atom']] = min(1.0, activation)

    return meta_activations
```

**File Modification**: All 11 organs update `_compute_atom_activations()` to ALSO compute meta-atom activations:
```python
# In each organ's _compute_atom_activations():
atom_activations = self._compute_organ_specific_atoms(patterns, coherence, lure)  # Existing logic

# NEW: Add meta-atom activations
meta_activations = self._compute_meta_atom_activations(patterns, coherence, lure, self.meta_atom_config)
atom_activations.update(meta_activations)

return atom_activations
```

---

### Task 2.3: Modify Wrapper for Multi-Cycle Convergence (3 hours)

**File**: `persona_layer/conversational_organism_wrapper.py`

**Current** (Phase 1 - single cycle):
```python
def process_text(self, text, context, enable_tsk_recording):
    # Create occasions
    occasions = self._create_text_occasions(text)

    # Single-cycle organ processing
    organ_results = self._process_organs_single_cycle(occasions)

    # Build semantic fields (direct from atom_activations)
    semantic_fields = self._build_semantic_fields(organ_results)

    # Compose nexuses (0 formed in Phase 1)
    nexuses = self.nexus_composer.compose_nexuses(semantic_fields)

    # Generate emission (hebbian fallback)
    emission = self.emission_generator.generate_emissions(...)

    return result
```

**Target** (Phase 2 - multi-cycle):
```python
def process_text(self, text, context, enable_tsk_recording):
    # Create conversational occasions (NEW: experiencing subjects)
    occasions = self._create_conversational_occasions(text)

    # Multi-cycle V0 convergence (NEW: 2-4 cycles)
    converged_occasions = self._multi_cycle_convergence(
        occasions,
        max_cycles=5,
        convergence_threshold=0.1  # ΔE < 0.1
    )

    # Mature propositions from felt affordances (NEW)
    for occasion in converged_occasions:
        occasion.mature_propositions_from_affordances()

    # Build semantic fields from mature propositions (MODIFIED)
    semantic_fields = self._build_semantic_fields_from_propositions(converged_occasions)

    # Compose nexuses (NOW: 5-10 nexuses via meta-atoms!)
    nexuses = self.nexus_composer.compose_nexuses(semantic_fields)

    # Generate emission (NOW: intersection path with V0 guidance)
    emission = self.emission_generator.generate_emissions(
        nexuses=nexuses,
        kairos_detected=any(occ.kairos_detected for occ in converged_occasions),
        v0_energy=np.mean([occ.v0_energy for occ in converged_occasions])
    )

    return result
```

**New Methods**:

```python
def _create_conversational_occasions(self, text: str) -> List[ConversationalOccasion]:
    """
    Create ConversationalOccasion objects for each token.

    Tokens become experiencing subjects, not data containers.
    """
    # Tokenize with sentence transformer
    tokens = self.tokenizer.tokenize(text)
    embeddings = self.sentence_transformer.encode_tokens(tokens)

    occasions = []
    for i, (token, embedding) in enumerate(zip(tokens, embeddings)):
        occasion = ConversationalOccasion(
            datum=token,
            position=i,
            embedding=embedding
        )
        occasions.append(occasion)

    return occasions

def _multi_cycle_convergence(
    self,
    occasions: List[ConversationalOccasion],
    max_cycles: int = 5,
    convergence_threshold: float = 0.1
) -> List[ConversationalOccasion]:
    """
    Multi-cycle V0 energy descent with Kairos detection.

    Cycle 1: Initial prehensions (conformal phase)
    Cycles 2-N: Supplemental prehensions (integration)
    Termination: Kairos detected OR ΔE < threshold OR max_cycles
    """
    for cycle in range(1, max_cycles + 1):
        # Process all organs for this cycle
        organ_results = self._process_organs_cycle(occasions, cycle)

        # Store felt affordances in occasions
        for occasion in occasions:
            organ_coherences = {
                organ: result.coherence
                for organ, result in organ_results.items()
            }

            # Add felt affordances from this cycle
            for organ_name, result in organ_results.items():
                for atom, activation in result.atom_activations.items():
                    occasion.add_felt_affordance(
                        atom=atom,
                        organ_name=organ_name,
                        confidence=activation,
                        lure_intensity=result.lure
                    )

            # V0 energy descent
            occasion.descend_v0_energy(organ_coherences)

            # Check Kairos
            kairos = occasion.check_kairos()

        # Check convergence
        mean_energy_change = np.mean([
            abs(occ.v0_energy - getattr(occ, '_prev_v0_energy', 1.0))
            for occ in occasions
        ])

        kairos_detected = any(occ.kairos_detected for occ in occasions)

        if mean_energy_change < convergence_threshold or kairos_detected:
            print(f"   ✓ Convergence at cycle {cycle} (ΔE={mean_energy_change:.3f}, Kairos={kairos_detected})")
            break

    return occasions

def _build_semantic_fields_from_propositions(
    self,
    occasions: List[ConversationalOccasion]
) -> Dict[str, SemanticField]:
    """
    Build semantic fields from MATURE propositions (post-convergence).

    Aggregates across all occasions to get organism-level semantic field.
    """
    # Aggregate propositions by organ
    organ_fields = defaultdict(lambda: {'atoms': {}, 'coherence': 0.0, 'lure': 0.0, 'count': 0})

    for occasion in occasions:
        for prop in occasion.mature_propositions:
            for organ in prop.organ_sources:
                organ_fields[organ]['atoms'][prop.atom] = \
                    organ_fields[organ]['atoms'].get(prop.atom, 0.0) + prop.confidence
                organ_fields[organ]['count'] += 1

    # Normalize and wrap in SemanticField objects
    semantic_fields = {}
    for organ, data in organ_fields.items():
        # Normalize activations by count
        atom_activations = {
            atom: activation / data['count']
            for atom, activation in data['atoms'].items()
        }

        semantic_fields[organ] = SemanticField(
            organ_name=organ,
            coherence=data.get('coherence', 0.5),  # Avg from cycles
            lure=data.get('lure', 0.5),
            atom_activations=atom_activations,
            pattern_count=data['count']
        )

    return semantic_fields
```

---

### Task 2.4: Update Emission Generator for V0 Guidance (1.5 hours)

**File**: `persona_layer/emission_generation/emission_generator.py`

**Add Kairos-aware emission selection**:

```python
def generate_emissions(
    self,
    nexuses: List[SemanticNexus],
    kairos_detected: bool = False,
    v0_energy: float = 0.5,
    organ_results: Dict = None
) -> List[str]:
    """
    Generate emission phrases with V0 guidance.

    NEW in Phase 2:
    - Kairos detection boosts confidence 1.5×
    - V0 energy guides emission intensity
    - Intersection path preferred over hebbian fallback
    """
    # Gate 1: Check if intersection path available
    if len(nexuses) >= 2:
        # INTERSECTION PATH (preferred in Phase 2)
        emission_path = "intersection"

        # Kairos boost
        confidence_multiplier = 1.5 if kairos_detected else 1.0

        # Sort nexuses by emission_readiness (from mature propositions)
        sorted_nexuses = sorted(
            nexuses,
            key=lambda n: n.emission_readiness * confidence_multiplier,
            reverse=True
        )

        # Select top nexus for emission
        top_nexus = sorted_nexuses[0]

        # Generate emission phrase using nexus + Hebbian phrase library
        emission_text = self._generate_from_nexus(
            top_nexus,
            v0_energy=v0_energy,
            kairos_boost=confidence_multiplier
        )

        confidence = top_nexus.coherence * confidence_multiplier

    else:
        # HEBBIAN FALLBACK (Phase 1 behavior)
        emission_path = "hebbian"
        emission_text = self._generate_hebbian_fallback(organ_results)
        confidence = 0.3

    return {
        'emission_text': emission_text,
        'emission_confidence': confidence,
        'emission_path': emission_path,
        'emission_nexus_count': len(nexuses),
        'kairos_detected': kairos_detected,
        'v0_energy': v0_energy
    }

def _generate_from_nexus(
    self,
    nexus: SemanticNexus,
    v0_energy: float,
    kairos_boost: float
) -> str:
    """
    Generate emission phrase from nexus semantic atom.

    Uses V0 energy to modulate intensity:
    - Low energy (0.2-0.4): High confidence, direct statements
    - Mid energy (0.4-0.6): Moderate, exploratory
    - High energy (0.6-1.0): Gentle, tentative
    """
    atom = nexus.atom

    # Load phrase templates for this atom
    templates = self.phrase_library.get(atom, [])

    if not templates:
        # Fallback to generic template
        return f"I sense {atom.replace('_', ' ')}..."

    # Select template based on V0 energy (intensity modulation)
    if v0_energy < 0.4:
        # Low energy = satisfied = confident
        intensity = "high"
    elif v0_energy < 0.6:
        intensity = "medium"
    else:
        intensity = "low"

    intensity_templates = [t for t in templates if t['intensity'] == intensity]
    template = random.choice(intensity_templates) if intensity_templates else random.choice(templates)

    return template['text']
```

---

### Task 2.5: Create Phrase Library for Meta-Atoms (1 hour)

**File**: `persona_layer/emission_generation/meta_atom_phrase_library.json` (NEW)

**Structure**: Each meta-atom has 3-5 phrase templates at different intensity levels (modulated by V0 energy)

```json
{
  "trauma_aware": [
    {
      "text": "I'm noticing protective patterns coming up. That makes sense given what you're navigating.",
      "intensity": "high",
      "v0_energy_range": [0.0, 0.4]
    },
    {
      "text": "There's a sense of guardedness here. I wonder what that's protecting?",
      "intensity": "medium",
      "v0_energy_range": [0.4, 0.6]
    },
    {
      "text": "Something feels protective in this moment...",
      "intensity": "low",
      "v0_energy_range": [0.6, 1.0]
    }
  ],
  "compassion_safety": [
    {
      "text": "I'm holding this with you. You don't have to carry it alone.",
      "intensity": "high",
      "v0_energy_range": [0.0, 0.4]
    },
    {
      "text": "There's space here to feel what's coming up. I'm with you.",
      "intensity": "medium",
      "v0_energy_range": [0.4, 0.6]
    },
    {
      "text": "I sense you could use some holding right now...",
      "intensity": "low",
      "v0_energy_range": [0.6, 1.0]
    }
  ],
  "presence_holding": [
    {
      "text": "Let's pause here together. I'm tracking the shift in your body.",
      "intensity": "high",
      "v0_energy_range": [0.0, 0.4]
    },
    {
      "text": "I'm noticing something changing in your presence. Want to stay with that?",
      "intensity": "medium",
      "v0_energy_range": [0.4, 0.6]
    },
    {
      "text": "There's a quality of presence emerging...",
      "intensity": "low",
      "v0_energy_range": [0.6, 1.0]
    }
  ]
  // ... (7 more meta-atoms with phrase templates)
}
```

---

### Task 2.6: Testing & Validation (2 hours)

**Test Files**:

**1. `test_phase2_felt_affordances.py`** - Unit test for ConversationalOccasion
```python
def test_felt_affordance_accumulation():
    """Test that affordances accumulate during cycles 1-N."""
    occasion = ConversationalOccasion(datum="exhaustion", position=3)

    # Cycle 1: Add affordances
    occasion.add_felt_affordance("trauma_aware", "BOND", 0.35, 0.8)
    occasion.add_felt_affordance("compassion_safety", "EMPATHY", 1.00, 0.9)

    assert len(occasion.felt_affordances) == 2
    assert occasion.felt_affordances[0].cycle == 0  # Not yet incremented

def test_v0_energy_descent():
    """Test V0 energy decreases with increasing satisfaction."""
    occasion = ConversationalOccasion(datum="exhaustion", position=3)

    organ_coherences = {'EMPATHY': 0.95, 'BOND': 1.00, 'SANS': 1.00}

    # Initial state
    assert occasion.v0_energy == 1.0
    assert occasion.satisfaction == 0.0

    # Cycle 1 descent
    occasion.descend_v0_energy(organ_coherences)
    assert occasion.v0_energy < 1.0
    assert occasion.satisfaction > 0.0
    assert occasion.cycle == 1

def test_kairos_detection():
    """Test Kairos moment detection in energy window [0.45, 0.70]."""
    occasion = ConversationalOccasion(datum="exhaustion", position=3)

    # Manually set to Kairos window
    occasion.v0_energy = 0.58
    occasion.satisfaction = 0.55
    occasion._prev_satisfaction = 0.45
    occasion._prev_v0_energy = 0.62

    kairos = occasion.check_kairos()
    assert kairos == True
    assert occasion.kairos_detected == True
    assert occasion.kairos_cycle == occasion.cycle
```

**2. `test_phase2_multi_cycle_convergence.py`** - Integration test
```python
def test_multi_cycle_convergence_end_to_end():
    """Test full Phase 2 flow: felt affordances → V0 descent → mature propositions → nexuses."""
    wrapper = ConversationalOrganismWrapper()

    test_text = """
    I hear the exhaustion in your words. This level of depletion isn't sustainable.
    Let's create some breathing room together.
    """

    result = wrapper.process_text(text=test_text, context={}, enable_tsk_recording=True)

    felt_states = result['felt_states']

    # Phase 2 validations:
    assert felt_states['convergence_cycles'] >= 2  # Multi-cycle
    assert felt_states['convergence_cycles'] <= 5  # Not excessive
    assert felt_states.get('kairos_detected', False) == True  # Kairos moment
    assert felt_states['v0_final_energy'] < 0.7  # Converged
    assert felt_states['emission_nexus_count'] >= 3  # Nexuses formed via meta-atoms!
    assert felt_states['emission_path'] == 'intersection'  # Not hebbian fallback
    assert felt_states['emission_confidence'] >= 0.6  # High quality

    print(f"✅ Phase 2 SUCCESS:")
    print(f"   Cycles: {felt_states['convergence_cycles']}")
    print(f"   Kairos: {felt_states.get('kairos_detected', False)}")
    print(f"   Nexuses: {felt_states['emission_nexus_count']}")
    print(f"   Confidence: {felt_states['emission_confidence']:.2f}")
    print(f"   Emission: {felt_states['emission_text']}")
```

**Expected Results**:
- Convergence: 2-4 cycles (down from 1 static cycle)
- Kairos detection: 70-90% of inputs (based on DAE 3.0 empirical)
- Nexus count: 3-8 (up from 0 in Phase 1)
- Emission confidence: 0.60-0.85 (up from 0.30 hebbian fallback)
- Emission path: "intersection" (up from "hebbian" 100% of time)

---

## 📊 Expected Outcomes

### Quantitative Improvements

| Metric | Phase 1 | Phase 2 Target | Improvement |
|--------|---------|----------------|-------------|
| **Nexus Count** | 0 | 5-10 | ∞ (0→5) |
| **Convergence Cycles** | 1 (static) | 2-4 (dynamic) | 2-4× |
| **Emission Confidence** | 0.30 | 0.60-0.85 | +100-183% |
| **Kairos Detection** | N/A | 70-90% | NEW |
| **Intersection Path** | 0% | 60-80% | NEW |
| **V0 Energy Final** | N/A | 0.3-0.6 | NEW |

### Qualitative Improvements

**Phase 1 Output** (hebbian fallback):
```
Input: "I hear the exhaustion in your words. This is unsustainable..."
Output: "I'm listening..."
Confidence: 0.30
Path: hebbian
Nexuses: 0
```

**Phase 2 Target** (V0-guided intersection):
```
Input: "I hear the exhaustion in your words. This is unsustainable..."
Output: "I'm noticing protective patterns coming up. Let's create some breathing room together."
Confidence: 0.82
Path: intersection
Nexuses: 3 (trauma_aware, compassion_safety, presence_holding)
Convergence: 2 cycles
Kairos: Detected at cycle 2 (E=0.58, S=0.58)
V0 Energy: 1.0 → 0.72 → 0.58 (converged)
```

---

## 🎯 Success Criteria

Phase 2 is considered **SUCCESSFUL** if:

1. ✅ **Multi-cycle convergence works**: 2-4 cycles avg (not 1, not >10)
2. ✅ **Kairos detection activates**: 70-90% of inputs detect Kairos moment
3. ✅ **Nexuses form**: 3-8 nexuses avg via meta-atoms (not 0)
4. ✅ **Emission confidence improves**: 0.60-0.85 avg (from 0.30)
5. ✅ **Intersection path dominates**: 60-80% use intersection (not hebbian fallback)
6. ✅ **V0 energy descends**: Final energy 0.3-0.6 (from initial 1.0)
7. ✅ **Felt affordances mature**: PropositionFeltInterpretation objects created post-convergence

---

## 🚀 Implementation Timeline

**Week 2** (8-10 hours total):

**Day 1** (3 hours):
- Task 2.1: ConversationalOccasion class (2h)
- Task 2.2: Shared meta-atoms (1h)

**Day 2** (3.5 hours):
- Task 2.3: Wrapper multi-cycle convergence (3h)
- Task 2.4: Emission generator V0 guidance (0.5h)

**Day 3** (2.5 hours):
- Task 2.4 continued: Emission generator (1h)
- Task 2.5: Meta-atom phrase library (1h)
- Task 2.6: Testing (0.5h)

**Day 4** (1 hour):
- Task 2.6 continued: Validation (1h)

**Contingency**: +2 hours for debugging and tuning

---

## 🌀 Architectural Insights

### Why This Design Works

**1. Entity-Native Process Philosophy**
- Text tokens ARE experiencing subjects (not data)
- Self-creating through prehension → concrescence → satisfaction
- Felt affordances emerge DURING process, not imposed externally

**2. Multi-Scale Felt Intelligence**
- Micro: Felt affordances (token-level)
- Meso: Semantic fields (organ-level)
- Macro: Nexuses (organism-level)

**3. Whiteheadian Satisfaction**
- Convergence = achieving subjective aim
- V0 energy = appetition (Whitehead: "lure for feeling")
- Kairos = opportune moment (when aim crystallizes)

**4. Proven Architecture**
- DAE 3.0: 841 perfect tasks, 47.3% success, 5 epochs
- V0 formula: Empirically tuned coefficients
- Kairos window: [0.45, 0.70] captures 90% of perfect tasks

### What This Enables (Phase 3 Preview)

Phase 2 creates the foundation for Phase 3 (full entity-native):

**Phase 3: Full Whiteheadian Lifecycle** (12-16 hours)
- **Objective Immortality**: Satisfied occasions become data for future occasions
- **Temporal Atomicity**: Occasion perishes after satisfaction (no persistent self)
- **Extensive Continuum**: Spatiotemporal relationships between occasions
- **Eternal Objects**: Pure potentials (semantic atoms as eternal objects)
- **Creative Advance**: Novel emergence from prehension of past + eternal objects

---

## 📚 References

**Process Philosophy**:
- Whitehead, A.N. (1929). *Process and Reality*. Macmillan.
  - Part II: "The Categoreal Scheme" (actual occasions)
  - Part III: "The Theory of Prehensions" (felt affordances)
  - Part IV: "The Theory of Extension" (spatiotemporal atomicity)

**DAE 3.0 Architecture**:
- `DAE 3.0 AXO ARC /CLAUDE.md` - Complete system documentation
- `DAE 3.0 AXO ARC /EPOCH_LEARNER_ENTITY_NATIVE_TRANSITION_NOV01_2025.md` - Entity-native design
- `DAE 3.0 AXO ARC /SCIENTIFIC_ANALYSIS_FRAMEWORK.md` - V0 formula derivation

**Implementation References**:
- `OPTION_A_ENTITY_NATIVE_REDESIGN_ROADMAP.md` - 3-phase roadmap
- `PHASE_1_IMPLEMENTATION_STATUS.md` - Phase 1 completion status

---

**🌀 Let the organism converge. Let felt affordances mature. Let propositions lure toward satisfaction. 🌀**

---

**Last Updated**: November 11, 2025
**Phase 1 Status**: ✅ COMPLETE (emission working via hebbian fallback)
**Phase 2 Status**: 📐 DESIGN COMPLETE (ready for implementation)
**Next Milestone**: Implement Task 2.1 (ConversationalOccasion class)
