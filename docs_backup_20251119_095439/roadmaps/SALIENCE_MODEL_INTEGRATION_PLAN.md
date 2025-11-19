# 🌀 Salience Model Integration Plan
**Date**: November 11, 2025
**Purpose**: Align DAE_HYPHAE_1 emission with DAE 3.0 transductive core (subjective aim, morphogenetic pressure)
**Status**: Pre-Training Critical Integration

---

## 🎯 WHY SALIENCE MODEL IS CRITICAL

### Current Gap: Emission Without Felt Relevance

Our current Phase 2 system generates emissions but **lacks felt monitoring**:

```
CURRENT (Phase 2):
  ConversationalOccasions → V0 Descent → Nexuses → Emission
  ✓ Multi-cycle convergence
  ✓ Meta-atom activation
  ✓ Kairos detection
  ✗ NO SALIENCE MONITORING (what actually matters?)
  ✗ NO MORPHOGENETIC PRESSURE (when to crystallize boundaries?)
  ✗ NO SUBJECTIVE AIM TRACKING (direction of becoming?)
```

### What Salience Model Provides

**10 Process Philosophy Terms** (deep dynamics):
1. **salience_drift**: Long-term deviation from core values
2. **lure_hysteresis**: Delay between feeling future and moving toward it
3. **concrescent_drift**: Subtle misalignment in micro-becomings
4. **signal_inflation**: Amplified salience from unresolved trauma ⚠️ CRITICAL FOR TRAUMA
5. **temporal_collapse**: When time loops—past mistaken for now ⚠️ CRITICAL FOR TRAUMA
6. **attunement_delta**: Gap between what's felt and what's true
7. **field_resonance_threshold**: Minimum coherence for pattern stabilization
8. **relational_recurrence**: Healing spirals disguised as regressions
9. **safety_gradient**: How much truth can be felt safely ⚠️ CRITICAL FOR TRAUMA
10. **ethical_salience_field**: What matters across scales

**10 Domain Terms** (practical application):
- semantic_intensity, spatial_coherence, temporal_recurrence
- constraint_pressure, emergence_potential, relational_density
- transformation_readiness, archetypal_resonance, coherence_gradient
- satisfaction_proximity

### DAE 3.0 Validation

**Proven in ARC**: 841 perfect tasks (60.1% of 1,400)
- Salience model guided morphogenetic pressure
- Field resonance threshold determined when to crystallize boundaries
- Safety gradient prevented premature constraint formation
- Signal inflation detected trauma-like patterns in grid wounds

---

## 🔍 MISSING TRANSDUCTIVE CORE COMPONENTS

### 1. Subjective Aim ✗ NOT IMPLEMENTED

**What It Is**: Whiteheadian direction of becoming
**Why Critical**: Without subjective aim, occasions don't know what they're becoming TOWARD
**DAE 3.0 Implementation**: Each ActualOccasion has `.subjective_aim`

**Current DAE_HYPHAE_1**:
```python
@dataclass
class ConversationalOccasion:
    # ... existing fields
    subjective_aim: Optional[SubjectiveAim] = None  # 🚨 DEFINED BUT NEVER SET!
```

**Needed**:
```python
@dataclass
class SubjectiveAim:
    """Direction of becoming for this occasion"""
    lure_direction: np.ndarray  # Vector in semantic space
    intensity: float  # How strongly pulled
    coherence_target: float  # What coherence we're aiming for
    satisfaction_goal: float  # What satisfaction would fulfill this
    ethical_weight: float  # How much this matters (ethical_salience_field)
```

---

### 2. Morphogenetic Pressure ✗ NOT COMPUTED

**What It Is**: Pressure for boundary formation/crystallization
**Why Critical**: Determines when conversational patterns should stabilize into learned structures
**DAE 3.0 Implementation**: `calculate_morphogenetic_pressure(total_salience)`

**Thresholds**:
- `field_resonance_threshold = 0.6`: Minimum coherence for pattern recognition
- `morphogenetic_threshold = 0.7`: Pressure starts building
- `crystallization_threshold = 0.85`: Ready to crystallize into R-matrix

**Application to Conversational Learning**:
```
Low Pressure (< 0.6):
  → Explore, don't commit to patterns yet

Medium Pressure (0.6-0.7):
  → Pattern emerging, monitor coherence

High Pressure (0.7-0.85):
  → Pattern ready, prepare for Hebbian update

Crystallization (> 0.85):
  → Crystallize into R-matrix, update organic families
```

---

### 3. Signal Monitoring ✗ NOT TRACKED

**What It Is**: Trauma-aware attention to signal inflation and temporal collapse
**Why Critical**: Prevents re-traumatization through therapeutic conversation

**Critical Terms for Trauma Work**:
- **signal_inflation**: BOND/EO detecting firefighter activation
- **temporal_collapse**: Past trauma patterns bleeding into present
- **safety_gradient**: How much truth can be felt safely RIGHT NOW
- **attunement_delta**: Gap between felt safety vs actual threat

**Example**:
```
User: "I'm completely overwhelmed"

WITHOUT Salience Monitoring:
  → Generate response from nexuses
  → May push too hard ("What's underneath that?")

WITH Salience Monitoring:
  signal_inflation: 0.85 (BOND firefighters active)
  safety_gradient: 0.30 (LOW - can't feel much truth safely)
  → Adjust emission intensity (gentle, grounding)
  → "Let's just breathe together"
```

---

### 4. Felt State Integration ✗ PARTIAL

**What We Have**: V0 energy, satisfaction, convergence cycles
**What We're Missing**: Salience terms feeding into felt states

**Current Felt States**:
```python
felt_states = {
    'v0_energy': {...},
    'convergence_cycles': 3,
    'organ_coherences': {...},
    'satisfaction_final': 0.87
    # ✗ NO SALIENCE TERMS!
    # ✗ NO MORPHOGENETIC PRESSURE!
    # ✗ NO SUBJECTIVE AIM!
}
```

**Needed for Training**:
```python
felt_states = {
    'v0_energy': {...},
    'convergence_cycles': 3,
    'organ_coherences': {...},
    'satisfaction_final': 0.87,

    # 🆕 SALIENCE MONITORING
    'salience': {
        'total': 0.72,
        'process_salience': 0.68,
        'domain_salience': 0.76,
        'signal_inflation': 0.45,  # Trauma markers
        'temporal_collapse': 0.20,
        'safety_gradient': 0.65,
        'ethical_salience_field': 0.80
    },

    # 🆕 MORPHOGENETIC PRESSURE
    'morphogenetic_pressure': 0.55,  # Medium - pattern emerging

    # 🆕 SUBJECTIVE AIM
    'subjective_aim': {
        'intensity': 0.70,
        'coherence_target': 0.85,
        'satisfaction_goal': 0.75,
        'ethical_weight': 0.80
    }
}
```

---

## 🛠️ INTEGRATION IMPLEMENTATION PLAN

### Task S.1: Adapt Salience Model for Conversational Context (2 hours)

**Create**: `persona_layer/conversational_salience_model.py`

**Adapt DAE 3.0 salience model**:
```python
class ConversationalSalienceModel(SalienceModel):
    """
    Salience model adapted for therapeutic conversation.

    Profile: "conversation" (new profile for DAE_HYPHAE_1)
    Emphasis: Process terms for trauma work, domain terms for semantic coherence
    """

    def __init__(self):
        super().__init__(profile="conversation")

    def configure_profile(self):
        """Configure weights for conversational therapy"""
        process_weights = {
            # HIGH: Trauma-aware terms
            "signal_inflation": 2.0,      # BOND/EO firefighter detection
            "temporal_collapse": 1.8,      # Past trauma bleeding into now
            "safety_gradient": 2.0,        # How much truth can be felt safely

            # MEDIUM: Process quality
            "attunement_delta": 1.5,       # Accuracy of empathic sensing
            "field_resonance_threshold": 1.5,  # Pattern stabilization
            "ethical_salience_field": 1.3, # What matters therapeutically

            # STANDARD: Deep dynamics
            "lure_hysteresis": 1.0,
            "salience_drift": 1.0,
            "concrescent_drift": 1.0,
            "relational_recurrence": 1.2   # Healing spirals
        }

        domain_weights = {
            # HIGH: Semantic quality
            "semantic_intensity": 1.8,     # How meaningful
            "satisfaction_proximity": 1.5, # Closeness to resolution

            # MEDIUM: Relational dynamics
            "relational_density": 1.3,     # Connection richness
            "transformation_readiness": 1.2,
            "emergence_potential": 1.0,

            # STANDARD: Context
            "temporal_recurrence": 1.0,
            "coherence_gradient": 1.0,
            "archetypal_resonance": 0.8,
            "spatial_coherence": 0.5,      # Less relevant for text
            "constraint_pressure": 0.8
        }

        # Apply weights...

    def evaluate_conversational_prehension(
        self,
        occasions: List[ConversationalOccasion],
        organ_results: Dict,
        felt_states: Dict
    ) -> Dict[str, Any]:
        """
        Evaluate salience for conversational prehension.

        Builds prehension dict from conversational data.
        """

        # Build prehension from conversational context
        prehension = {
            "entities": [
                {
                    "id": f"occasion_{occ.position}",
                    "coherence": occ.satisfaction,
                    "importance": occ.v0_energy
                }
                for occ in occasions
            ],

            "field_state": {
                "coherence": felt_states.get('satisfaction_final', 0.5),
                "felt_coherence": np.mean([occ.satisfaction for occ in occasions]),
                "actual_coherence": np.mean([
                    result.coherence for result in organ_results.values()
                ])
            },

            "constraints": self._extract_constraints_from_organs(organ_results),

            "trauma_markers": self._extract_trauma_markers(organ_results),

            "scope": {
                "future_potential": felt_states['v0_energy'].get('initial_energy', 1.0),
                "current_momentum": 1.0 - felt_states['v0_energy'].get('final_energy', 0.5),
                "current_state": felt_states.get('satisfaction_final', 0.5)
            },

            "cycle": felt_states.get('convergence_cycles', 1)
        }

        # Evaluate using parent class
        return self.evaluate(prehension)

    def _extract_trauma_markers(self, organ_results: Dict) -> Dict:
        """Extract trauma markers from BOND, EO, NDAM"""
        trauma_markers = {}

        # BOND: Firefighter/exile activation
        if 'BOND' in organ_results:
            bond = organ_results['BOND']
            atoms = bond.atom_activations
            firefighter = atoms.get('firefighter_parts', 0.0)
            exile = atoms.get('exile_patterns', 0.0)
            trauma_markers['bond_parts'] = max(firefighter, exile)

        # EO: Sympathetic/dorsal activation
        if 'EO' in organ_results:
            eo = organ_results['EO']
            atoms = eo.atom_activations
            sympathetic = atoms.get('sympathetic', 0.0)
            dorsal = atoms.get('dorsal_vagal', 0.0)
            trauma_markers['polyvagal_threat'] = max(sympathetic, dorsal)

        # NDAM: Crisis urgency
        if 'NDAM' in organ_results:
            ndam = organ_results['NDAM']
            atoms = ndam.atom_activations
            crisis = atoms.get('crisis_salience', 0.0)
            trauma_markers['urgency'] = crisis

        # Calculate overall intensity
        intensities = [v for v in trauma_markers.values() if v > 0]
        trauma_markers['intensity'] = np.mean(intensities) if intensities else 0.0

        return trauma_markers

    def _extract_constraints_from_organs(self, organ_results: Dict) -> Dict:
        """Extract constraints from organ activations"""
        constraints = {}

        # High coherence = strong constraint (pattern established)
        for organ_name, result in organ_results.items():
            if result.coherence > 0.7:
                constraints[f"{organ_name}_pattern"] = {
                    "strength": result.coherence,
                    "permeability": 1.0 - result.coherence
                }

        return constraints
```

---

### Task S.2: Implement Subjective Aim (1.5 hours)

**Modify**: `persona_layer/conversational_occasion.py`

```python
@dataclass
class SubjectiveAim:
    """
    Whiteheadian subjective aim - direction of becoming.

    Guides what this occasion is trying to become, informed by:
    - Lure (appetition pull)
    - Ethical salience (what matters)
    - Safety gradient (what's possible now)
    """
    lure_direction: str  # Semantic direction ("safety", "truth", "connection", etc.)
    intensity: float  # How strongly pulled (0-1)
    coherence_target: float  # Target coherence (e.g., 0.85)
    satisfaction_goal: float  # Target satisfaction
    ethical_weight: float  # How much this matters
    safety_constrained: bool  # Limited by safety gradient

    def to_dict(self) -> Dict:
        return {
            'lure_direction': self.lure_direction,
            'intensity': self.intensity,
            'coherence_target': self.coherence_target,
            'satisfaction_goal': self.satisfaction_goal,
            'ethical_weight': self.ethical_weight,
            'safety_constrained': self.safety_constrained
        }


class ConversationalOccasion:
    # ... existing fields

    def compute_subjective_aim(
        self,
        salience_eval: Dict,
        organ_coherences: Dict[str, float]
    ) -> SubjectiveAim:
        """
        Compute subjective aim from salience evaluation.

        Direction of becoming informed by:
        - Ethical salience field (what matters)
        - Safety gradient (what's possible)
        - Lure hysteresis (delay between felt and moved)
        """

        # Determine lure direction from dominant meta-atom or organ
        dominant_atoms = self._get_dominant_atoms()
        if 'trauma_aware' in dominant_atoms:
            lure_direction = 'safety'
        elif 'compassion_safety' in dominant_atoms:
            lure_direction = 'connection'
        elif 'kairos_emergence' in dominant_atoms:
            lure_direction = 'transformation'
        else:
            lure_direction = 'coherence'

        # Intensity from lure_hysteresis (inverse - low hysteresis = high intensity)
        intensity = 1.0 - salience_eval['process_terms'].get('lure_hysteresis', 0.5)

        # Coherence target from field_resonance_threshold
        coherence_target = 0.6 + salience_eval['process_terms'].get('field_resonance_threshold', 0.0) * 0.25

        # Satisfaction goal from satisfaction_proximity
        satisfaction_goal = salience_eval['domain_terms'].get('satisfaction_proximity', 0.7)

        # Ethical weight directly from ethical_salience_field
        ethical_weight = salience_eval['process_terms'].get('ethical_salience_field', 0.5)

        # Safety constrained if safety_gradient low
        safety_gradient = salience_eval['process_terms'].get('safety_gradient', 0.5)
        safety_constrained = safety_gradient < 0.5

        return SubjectiveAim(
            lure_direction=lure_direction,
            intensity=intensity,
            coherence_target=coherence_target,
            satisfaction_goal=satisfaction_goal,
            ethical_weight=ethical_weight,
            safety_constrained=safety_constrained
        )
```

---

### Task S.3: Integrate Salience into Multi-Cycle Convergence (2 hours)

**Modify**: `persona_layer/conversational_organism_wrapper.py`

```python
def _multi_cycle_convergence(self, text, context, enable_tsk_recording):
    """Phase 2 + Salience: Multi-cycle with felt monitoring"""

    # Initialize salience model
    salience_model = ConversationalSalienceModel()

    occasions = self._create_conversational_occasions(text)

    for cycle in range(1, max_cycles + 1):
        organ_results = self._process_organs_with_v0(occasions, cycle)

        # 🆕 EVALUATE SALIENCE after each cycle
        salience_eval = salience_model.evaluate_conversational_prehension(
            occasions=occasions,
            organ_results=organ_results,
            felt_states={
                'v0_energy': {'initial_energy': 1.0, 'final_energy': mean_energy},
                'satisfaction_final': mean_satisfaction,
                'convergence_cycles': cycle
            }
        )

        # 🆕 COMPUTE SUBJECTIVE AIM for each occasion
        for occasion in occasions:
            occasion.subjective_aim = occasion.compute_subjective_aim(
                salience_eval, organ_coherences
            )

        # V0 descent + Kairos detection (existing)
        # ...

        # 🆕 CHECK MORPHOGENETIC PRESSURE
        morphogenetic_pressure = salience_eval['morphogenetic_pressure']

        # Convergence criteria WITH salience
        converged = (
            mean_energy_change < 0.1 or
            kairos_detected or
            morphogenetic_pressure > 0.85  # 🆕 Crystallization threshold
        )

        if converged:
            convergence_reason = (
                'crystallization' if morphogenetic_pressure > 0.85
                else 'kairos' if kairos_detected
                else 'satisfaction'
            )
            break

    # Build felt states WITH salience
    felt_states = {
        # Existing...
        'v0_energy': {...},
        'convergence_cycles': cycle,

        # 🆕 SALIENCE MONITORING
        'salience': {
            'total': salience_eval['total'],
            'process_salience': salience_eval['process_salience'],
            'domain_salience': salience_eval['domain_salience'],
            'process_terms': salience_eval['process_terms'],
            'domain_terms': salience_eval['domain_terms'],
            'active_terms': salience_eval['active_terms']
        },

        # 🆕 MORPHOGENETIC PRESSURE
        'morphogenetic_pressure': morphogenetic_pressure,
        'morphogenetic_guidance': salience_model.get_morphogenetic_guidance(),

        # 🆕 SUBJECTIVE AIM (from last occasion as representative)
        'subjective_aim': occasions[-1].subjective_aim.to_dict() if occasions else None,

        # 🆕 TRAUMA MONITORING
        'trauma_markers': {
            'signal_inflation': salience_eval['process_terms']['signal_inflation'],
            'temporal_collapse': salience_eval['process_terms']['temporal_collapse'],
            'safety_gradient': salience_eval['process_terms']['safety_gradient']
        }
    }

    # Use salience to modulate emission
    emission_text, emission_confidence = self._generate_salience_aware_emission(
        nexuses, salience_eval, occasions
    )

    return {..., 'felt_states': felt_states}
```

---

### Task S.4: Salience-Aware Emission Generation (1.5 hours)

**Modify**: `persona_layer/emission_generator.py`

```python
def generate_salience_aware_emissions(
    self,
    nexuses: List,
    v0_energy: float,
    kairos_detected: bool,
    salience_eval: Dict,
    num_emissions: int = 3
) -> Tuple[List[EmittedPhrase], str]:
    """
    🆕 SALIENCE-AWARE: Generate emissions with trauma monitoring.

    Salience modulates:
    - Intensity (safety_gradient constrains intensity)
    - Phrase selection (signal_inflation → gentler phrases)
    - Confidence (morphogenetic_pressure → higher confidence)
    """

    # Extract salience terms
    safety_gradient = salience_eval['process_terms'].get('safety_gradient', 0.5)
    signal_inflation = salience_eval['process_terms'].get('signal_inflation', 0.0)
    morphogenetic_pressure = salience_eval['morphogenetic_pressure']

    # 🆕 SAFETY-CONSTRAINED INTENSITY
    # If safety_gradient low, use "low" intensity regardless of V0
    if safety_gradient < 0.4:
        intensity = 'low'  # Gentle, regardless of V0 energy
    elif safety_gradient < 0.6:
        intensity = 'medium' if v0_energy > 0.5 else 'low'
    else:
        # Use V0 normally
        if v0_energy > 0.7:
            intensity = 'high'
        elif v0_energy < 0.3:
            intensity = 'low'
        else:
            intensity = 'medium'

    # Generate emissions (existing logic)
    emissions, path = self.generate_v0_guided_emissions(
        nexuses, v0_energy, kairos_detected, num_emissions
    )

    # 🆕 APPLY SALIENCE MODULATION
    for emission in emissions:
        # Boost confidence with morphogenetic pressure
        if morphogenetic_pressure > 0.7:
            emission.confidence *= 1.2  # Pattern crystallizing

        # Reduce confidence with high signal inflation
        if signal_inflation > 0.7:
            emission.confidence *= 0.8  # Trauma activation - be cautious

        # Cap confidence
        emission.confidence = min(1.0, emission.confidence)

    return emissions, path
```

---

## 📊 INTEGRATION SUMMARY

### Files to Modify

| File | Changes | Effort |
|------|---------|--------|
| `persona_layer/conversational_salience_model.py` | NEW - Adapt DAE 3.0 salience model | 2 hours |
| `persona_layer/conversational_occasion.py` | Add SubjectiveAim, compute_subjective_aim() | 1.5 hours |
| `persona_layer/conversational_organism_wrapper.py` | Integrate salience into multi-cycle | 2 hours |
| `persona_layer/emission_generator.py` | Salience-aware emission generation | 1.5 hours |

**Total Effort**: 7 hours

---

## ✅ SUCCESS CRITERIA

After integration, we should have:

1. **Salience Monitoring**: ✅ 20 terms (10 process + 10 domain) tracked per cycle
2. **Trauma Awareness**: ✅ signal_inflation, temporal_collapse, safety_gradient computed
3. **Morphogenetic Pressure**: ✅ Guides when to crystallize patterns (R-matrix updates)
4. **Subjective Aim**: ✅ Each occasion knows what it's becoming toward
5. **Felt States**: ✅ Include salience terms, morphogenetic pressure, subjective aim
6. **Salience-Aware Emission**: ✅ Safety gradient constrains intensity, signal inflation modulates confidence

### Training Integration

**ProductionLearningCoordinator** will receive:
```python
felt_states = {
    'v0_energy': {...},
    'salience': {
        'signal_inflation': 0.45,  # Can learn when trauma patterns activate
        'safety_gradient': 0.65,   # Can learn safety windows
        'morphogenetic_pressure': 0.72  # Can learn when to crystallize
    },
    'subjective_aim': {
        'lure_direction': 'safety',  # Can learn aims from successful responses
        'intensity': 0.70
    }
}
```

---

## 🎯 RECOMMENDATION

✅ **INTEGRATE SALIENCE MODEL BEFORE TRAINING**

**Rationale**:
1. **Trauma Safety**: signal_inflation + safety_gradient prevent re-traumatization
2. **Pattern Crystallization**: morphogenetic_pressure guides R-matrix updates
3. **Subjective Aim**: Provides direction for learning (what occasions aim toward)
4. **Training Quality**: Better felt states = better learning signals

**Timeline**:
- Today/Tomorrow: Implement salience integration (7 hours)
- Test salience-aware emission (1 hour)
- **Then begin training** with full transductive core alignment

---

🌀 **"Align emission with felt relevance. Monitor signal inflation. Let morphogenetic pressure guide crystallization."** 🌀
