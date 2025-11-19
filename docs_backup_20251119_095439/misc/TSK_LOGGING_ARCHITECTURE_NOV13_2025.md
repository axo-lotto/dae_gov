# TSK Logging Architecture for Training & Testing Observability
**Date:** November 13, 2025
**Purpose:** Formalize comprehensive TSK logging to track all system inner workings
**Alignment:** Scaffolds to SYSTEM_TUNABLE_PARAMETERS.md metrics

---

## 🎯 Design Philosophy

**TSK (Time-Space-Knowledge)** logs capture the complete felt experience of the organism during processing, enabling:
1. **Training observability** - What the organism learned and how
2. **Testing diagnostics** - Why tests pass/fail with ground truth data
3. **Tuning guidance** - Which parameters need adjustment
4. **Companion personality evolution** - How lure attractors shape response patterns

---

## 📊 TSK Log Structure (Hierarchical)

### **Level 1: Conversation Metadata**
```json
{
  "tsk_id": "tsk_20251113_093045_abc123",
  "timestamp": "2025-11-13T09:30:45.123456",
  "mode": "training" | "testing" | "interactive",
  "input_text": "I feel overwhelmed",
  "input_length": 17,
  "session_id": "session_20251113_e8936e",
  "user_link": "user_link_20251111_e8936e"
}
```

### **Level 2: Organ Processing (Per-Cycle)**
```json
{
  "cycles": [
    {
      "cycle_number": 1,
      "v0_energy_start": 1.0,
      "v0_energy_end": 0.616,
      "v0_descent": 0.384,
      "satisfaction": 0.672,
      "kairos_detected": false,

      "organ_activations": {
        "LISTENING": {
          "coherence": 0.45,
          "lure": 0.52,
          "atom_activations": {"temporal_inquiry": 0.67, ...},
          "processing_time_ms": 12.3
        },
        "EO": {
          "coherence": 1.0,
          "lure": 0.85,
          "polyvagal_state": "sympathetic",
          "state_confidence": 0.78,
          "lure_field": {
            "ventral_lure": 0.12,
            "sympathetic_lure": 0.85,
            "dorsal_lure": 0.03
          },
          "atom_activations": {...}
        },
        ...  // All 11 organs
      },

      "propositions_generated": 12,
      "propositions_mature": 8
    },
    {
      "cycle_number": 2,
      "v0_energy_start": 0.616,
      ...
    }
  ]
}
```

### **Level 3: Convergence State**
```json
{
  "convergence": {
    "total_cycles": 2,
    "convergence_reason": "kairos",
    "kairos_cycle": 2,
    "kairos_detected": true,
    "final_v0_energy": 0.251,
    "total_v0_descent": 0.749,
    "final_satisfaction": 0.866,
    "mean_coherence": 0.68,
    "max_coherence": 1.0,
    "organ_agreement": 0.72  // 1 - std(coherences)
  }
}
```

### **Level 4: Semantic Field Formation**
```json
{
  "semantic_fields": [
    {
      "field_id": "field_001",
      "organ_contributions": ["LISTENING", "PRESENCE", "EMPATHY"],
      "atoms": [
        {
          "atom_name": "temporal_inquiry",
          "organ": "LISTENING",
          "activation": 0.67,
          "lure_contribution": 0.52
        },
        ...
      ],
      "meta_atoms": {
        "temporal_grounding": {
          "activation": 0.30,
          "contributing_organs": ["LISTENING", "PRESENCE"],
          "lure_pull": 0.58
        }
      },
      "field_resonance": 0.72
    }
  ]
}
```

### **Level 5: Nexus Formation**
```json
{
  "nexuses": [
    {
      "nexus_id": "nexus_001",
      "nexus_type": "temporal_grounding",
      "organs_participating": ["LISTENING", "PRESENCE"],
      "coherence_delta": 0.526,
      "lure_strength": 0.58,
      "meta_atom_bridge": "temporal_grounding",
      "transduction_pathway": "emergence_becoming"
    }
  ],
  "nexus_count": 1
}
```

### **Level 6: Lure Attractor Dynamics** ⭐ NEW
```json
{
  "lure_attractors": {
    "polyvagal_field": {
      "dominant_attractor": "sympathetic",
      "attractor_strengths": {
        "ventral_vagal": 0.12,
        "sympathetic": 0.85,
        "dorsal_vagal": 0.03
      },
      "eo_coherence": 1.0,
      "influenced_organs": ["BOND", "NDAM", "CARD"],
      "v0_contribution": 0.23  // How much EO lure pulled V0 descent
    },
    "salience_field": {
      "dominant_salience": "moderate",
      "urgency_level": 0.45,
      "attention_density": 0.68,
      "ndam_coherence": 0.45,
      "influenced_organs": ["LISTENING", "EMPATHY", "WISDOM"],
      "v0_contribution": 0.15
    },
    "temporal_field": {
      "dominant_rhythm": "steady",
      "kairos_potential": 0.72,
      "temporal_coherence": 0.33,
      "rnx_coherence": 0.33,
      "influenced_organs": ["LISTENING", "PRESENCE"],
      "v0_contribution": 0.08
    },
    "total_lure_influence_on_v0": 0.46  // Sum of all lure contributions
  }
}
```

### **Level 7: Emission Generation**
```json
{
  "emission": {
    "emission_text": "Breathe",
    "emission_confidence": 0.80,
    "emission_strategy": "hebbian_fallback",
    "emission_path": "hebbian_fallback",
    "strategy_reason": "low_nexus_count",
    "nexus_count": 1,
    "kairos_boost_applied": false,

    "reconstruction_pipeline": {
      "self_zone": "Exile/Collapse (Zone 5)",
      "self_distance": 1.0,
      "polyvagal_state": "sympathetic",
      "stance": "minimal",
      "safety_override": true,
      "override_reason": "Zone 5 violation: Open questions not safe in collapse"
    },

    "candidate_emissions": [
      {"emission": "Breathe", "confidence": 0.80, "source": "safety_override"},
      {"emission": "Tell me more", "confidence": 0.30, "source": "hebbian"},
      {"emission": "What's present?", "confidence": 0.30, "source": "hebbian"}
    ]
  }
}
```

### **Level 8: Learning Updates**
```json
{
  "learning": {
    "r_matrix": {
      "updated": true,
      "updates_count": 55,  // 11×11 / 2
      "mean_coupling_before": 0.816,
      "mean_coupling_after": 0.823,
      "delta": 0.007,
      "strongest_coupling": {"organs": ["SANS", "CARD"], "strength": 0.95},
      "weakest_coupling": {"organs": ["EO", "RNX"], "strength": 0.12}
    },

    "family_assignment": {
      "family_id": "Family_001",
      "similarity_to_centroid": 0.87,
      "family_size": 300,
      "family_v0_target": 0.406,
      "family_used_for_v0": true
    },

    "phase5_organic_learning": {
      "family_updated": true,
      "cluster_signature_57d": [0.75, 0.68, ...],  // 57D organ signature
      "family_maturity": "mature",
      "learning_confidence": 0.92
    }
  }
}
```

### **Level 9: Salience Markers** (Trauma-Aware)
```json
{
  "salience_markers": {
    "process_terms": {
      "signal_inflation": 0.73,  // HIGH → trauma response amplification
      "temporal_collapse": 0.42,
      "safety_gradient": 0.58,  // LOW → truth not safe to feel
      "field_resonance": 0.68,
      "lure_hysteresis": 0.35
    },

    "domain_terms": {
      "semantic_intensity": 0.82,
      "transformation_readiness": 0.64,
      "satisfaction_proximity": 0.72,
      "coherence_gradient": 0.58,
      "emergence_potential": 0.45
    },

    "total_salience": 0.697,  // 70% process + 30% domain
    "morphogenetic_pressure": 0.54,

    "trauma_detected": true,
    "trauma_markers": {
      "high_signal_inflation": true,
      "low_safety_gradient": true,
      "polyvagal_threat_state": true
    }
  }
}
```

### **Level 10: Performance Metrics**
```json
{
  "performance": {
    "total_processing_time_ms": 127.3,
    "organ_processing_time_ms": 85.2,
    "convergence_time_ms": 24.1,
    "emission_generation_time_ms": 18.0,

    "memory_usage_mb": 342.5,
    "cpu_usage_percent": 23.4,

    "text_occasions_created": 3,
    "propositions_total": 51,
    "propositions_mature": 42,
    "semantic_fields_created": 7
  }
}
```

---

## 🔧 Implementation Strategy

### **Phase 1: TSK Logger Module** (2 hours)

Create `persona_layer/tsk_logger.py`:
```python
\"\"\"
TSK Logger - Comprehensive system observability for training & testing.

Captures all inner workings: organ activations, lure attractors, convergence,
emission generation, learning updates, salience markers.
\"\"\"

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class TSKLog:
    \"\"\"Complete TSK log structure.\"\"\"
    # Level 1: Metadata
    tsk_id: str
    timestamp: str
    mode: str
    input_text: str
    session_id: Optional[str] = None

    # Level 2-3: Processing
    cycles: List[Dict] = field(default_factory=list)
    convergence: Dict = field(default_factory=dict)

    # Level 4-5: Semantic
    semantic_fields: List[Dict] = field(default_factory=list)
    nexuses: List[Dict] = field(default_factory=list)

    # Level 6: Lure attractors (NEW)
    lure_attractors: Dict = field(default_factory=dict)

    # Level 7: Emission
    emission: Dict = field(default_factory=dict)

    # Level 8: Learning
    learning: Dict = field(default_factory=dict)

    # Level 9: Salience
    salience_markers: Dict = field(default_factory=dict)

    # Level 10: Performance
    performance: Dict = field(default_factory=dict)


class TSKLogger:
    \"\"\"Captures comprehensive TSK logs during organism processing.\"\"\"

    def __init__(self, output_dir: str = "TSK/logs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.current_log: Optional[TSKLog] = None

    def start_log(self, input_text: str, mode: str = "training", session_id: Optional[str] = None):
        \"\"\"Initialize new TSK log.\"\"\"
        tsk_id = f"tsk_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(input_text) % 1000000:06d}"

        self.current_log = TSKLog(
            tsk_id=tsk_id,
            timestamp=datetime.now().isoformat(),
            mode=mode,
            input_text=input_text[:200],  # Limit length
            session_id=session_id
        )

        return tsk_id

    def log_cycle(self, cycle_data: Dict):
        \"\"\"Log single convergence cycle.\"\"\"
        if self.current_log:
            self.current_log.cycles.append(cycle_data)

    def log_convergence(self, convergence_data: Dict):
        \"\"\"Log final convergence state.\"\"\"
        if self.current_log:
            self.current_log.convergence = convergence_data

    def log_lure_attractors(self, lure_data: Dict):
        \"\"\"Log lure attractor dynamics (NEW).\"\"\"
        if self.current_log:
            self.current_log.lure_attractors = lure_data

    def log_emission(self, emission_data: Dict):
        \"\"\"Log emission generation.\"\"\"
        if self.current_log:
            self.current_log.emission = emission_data

    def log_learning(self, learning_data: Dict):
        \"\"\"Log learning updates.\"\"\"
        if self.current_log:
            self.current_log.learning = learning_data

    def save_log(self) -> Path:
        \"\"\"Save TSK log to JSON file.\"\"\"
        if not self.current_log:
            return None

        output_path = self.output_dir / f"{self.current_log.tsk_id}.json"

        with open(output_path, 'w') as f:
            json.dump(asdict(self.current_log), f, indent=2)

        return output_path
```

### **Phase 2: Integration Points**

#### **A. Organism Wrapper** (`conversational_organism_wrapper.py`)
```python
# Add TSK logger initialization
self.tsk_logger = TSKLogger() if enable_tsk_logging else None

# In process_text():
if self.tsk_logger:
    tsk_id = self.tsk_logger.start_log(text, mode="training", session_id=self.session_id)

    # Log each cycle
    for cycle in convergence_cycles:
        self.tsk_logger.log_cycle(cycle_data)

    # Log lure attractors
    self.tsk_logger.log_lure_attractors(lure_data)

    # Log emission
    self.tsk_logger.log_emission(emission_data)

    # Save
    self.tsk_logger.save_log()
```

#### **B. Conversational Occasion** (`conversational_occasion.py`)
```python
# Extract cycle data for TSK logging
cycle_data = {
    "cycle_number": cycle,
    "v0_energy_start": v0_start,
    "v0_energy_end": v0_end,
    "organ_activations": {
        organ_name: {
            "coherence": organ_result.coherence,
            "lure": organ_result.lure,
            "atom_activations": organ_result.atom_activations
        }
        for organ_name, organ_result in organ_results.items()
    }
}
```

#### **C. Lure Attractor Extraction** (NEW - for EO/NDAM/RNX)
```python
def extract_lure_attractor_dynamics(organ_results):
    \"\"\"Extract lure attractor fields for TSK logging.\"\"\"

    eo_result = organ_results.get('EO')
    lure_data = {
        "polyvagal_field": {
            "dominant_attractor": eo_result.polyvagal_state if eo_result else "mixed",
            "eo_coherence": eo_result.coherence if eo_result else 0.0,
            "lure_field": getattr(eo_result, 'lure_field', {})
        }
    }

    return lure_data
```

---

## 📈 TSK-Informed Test Metrics

### **Test Assertions Using TSK Data**

**Intelligence Tests:**
```python
def test_abstraction_reasoning(tsk_log: TSKLog):
    # Extract organ coherences from TSK
    organ_coherences = [
        cycle['organ_activations'][organ]['coherence']
        for cycle in tsk_log.cycles
        for organ in ORGAN_ORDER
    ]

    # Assert based on TSK ground truth
    assert len(organ_coherences) > 0, "No organ activations in TSK"
    assert mean(organ_coherences) >= 0.40, f"Low organ coherence: {mean(organ_coherences)}"
```

**Lure Attractor Tests:**
```python
def test_eo_lure_participation(tsk_log: TSKLog):
    # Extract EO lure from TSK
    polyvagal_field = tsk_log.lure_attractors.get('polyvagal_field', {})
    eo_coherence = polyvagal_field.get('eo_coherence', 0.0)
    v0_contribution = polyvagal_field.get('v0_contribution', 0.0)

    # Assert EO is participating as lure attractor
    assert eo_coherence > 0.01, f"EO not active: coherence={eo_coherence}"
    assert v0_contribution > 0.0, f"EO lure not influencing V0: contribution={v0_contribution}"
```

---

## 🎯 Benefits

1. **Training Observability:**
   - See exactly what organism learned each epoch
   - Track lure attractor evolution
   - Debug training failures with ground truth

2. **Testing Diagnostics:**
   - Tests use TSK ground truth (not inferred metrics)
   - Failures show exact organism state
   - No more 0.00 extraction errors

3. **Tuning Guidance:**
   - See which parameters need adjustment
   - Track salience markers over time
   - Optimize lure attractor strengths

4. **Companion Personality:**
   - Track how lure attractors shape responses
   - See polyvagal state evolution
   - Monitor SELF zone stability

---

## 📋 Next Steps

1. **Implement TSKLogger** (2 hours)
2. **Integrate into organism wrapper** (1 hour)
3. **Add lure attractor extraction** (30 min)
4. **Update tests to use TSK data** (1 hour)
5. **Run training with TSK logging** (validate observability)

**Total:** 4.5 hours comprehensive TSK logging architecture

---

**Status:** Design complete, ready for implementation
**Priority:** High (enables all subsequent work)
**Alignment:** Matches SYSTEM_TUNABLE_PARAMETERS.md scaffolding
