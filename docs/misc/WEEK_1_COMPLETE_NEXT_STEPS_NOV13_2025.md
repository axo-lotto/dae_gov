# Week 1 Complete - Next Steps for Week 2
**Date:** November 13, 2025, 2:00 AM
**Status:** ✅ WEEK 1 + CONFIG COMPLETE - Ready for Week 2

---

## ✅ What Was Completed (Week 1)

### Core Components (3 files, 1,152 lines)
1. **`persona_layer/memory_retrieval.py`** (563 lines)
2. **`persona_layer/superject_recorder.py`** (422 lines)
3. **`persona_layer/local_llm_bridge.py`** (+167 lines enhancement)

### Documentation (3 files, 1,863 lines)
4. **`HYBRID_MATHEMATICAL_MODEL_REFINED_NOV13_2025.md`** (503 lines)
5. **`HYBRID_ALIGNMENT_WITH_DAE_GOV_NOV13_2025.md`** (680 lines)
6. **`HYBRID_WEEK1_SESSION_COMPLETE_NOV13_2025.md`** (680 lines)

### Configuration (1 file, +97 lines)
7. **`config.py`** - Added hybrid configuration section (19 parameters)

**Total:** 3,112 lines (implementation + documentation + configuration)

---

## 📋 Week 2 Implementation Checklist

### File 1: `persona_layer/conversational_occasion.py` (~50 lines)

**Add hybrid V0 descent method:**

```python
def compute_v0_energy_hybrid(
    self,
    satisfaction: float,
    appetition: float,
    relevance: float,
    complexity: float,
    llm_confidence: float = 0.0,  # NEW parameter
    llm_weight: float = 0.0  # NEW parameter
) -> float:
    """
    Hybrid V0 energy computation including LLM uncertainty term.

    Formula:
    E_v0 = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I) + η·(1-L_conf)

    Args:
        satisfaction: Organ coherence (1 - std(organ_values))
        appetition: Felt pull toward patterns
        relevance: Family-specific organ weights
        complexity: Information content
        llm_confidence: LLM response confidence (0-1)
        llm_weight: Current LLM weaning weight (0-1)

    Returns:
        V0 energy value
    """
    from config import Config

    # Use hybrid coefficients if LLM enabled
    if Config.HYBRID_ENABLED and llm_weight > 0:
        alpha = Config.V0_ALPHA_HYBRID  # 0.35
        beta = Config.V0_BETA_HYBRID    # 0.25
        gamma = Config.V0_GAMMA_HYBRID  # 0.12
        delta = Config.V0_DELTA_HYBRID  # 0.10
        zeta = Config.V0_ZETA_HYBRID    # 0.10
        eta = Config.V0_ETA_HYBRID      # 0.08
    else:
        # Pure DAE coefficients
        alpha = Config.V0_ALPHA  # 0.40
        beta = Config.V0_BETA    # 0.25
        gamma = Config.V0_GAMMA  # 0.15
        delta = Config.V0_DELTA  # 0.10
        zeta = Config.V0_ZETA    # 0.10
        eta = 0.0  # No LLM term

    # Standard V0 components
    E_satisfaction = alpha * (1 - satisfaction)
    E_delta = beta * abs(self.v0_energy - self._last_v0_energy)
    E_appetition = gamma * (1 - appetition)
    E_relevance = delta * (1 - relevance)
    E_complexity = zeta * complexity

    # NEW: LLM uncertainty component (weighted by llm_weight)
    E_llm = eta * (1 - llm_confidence) * llm_weight

    total_energy = (
        E_satisfaction +
        E_delta +
        E_appetition +
        E_relevance +
        E_complexity +
        E_llm  # NEW term
    )

    return total_energy
```

**Location:** Add after existing `compute_v0_energy()` method (around line 200)

---

### File 2: `persona_layer/emission_generator.py` (~80 lines)

**Add Gate 5 (LLM Fusion) method:**

```python
def generate_hybrid_emission(
    self,
    organ_emission: str,
    llm_emission: str,
    organ_confidence: float,
    llm_confidence: float,
    llm_weight: float,
    kairos_boost: float = 1.0
) -> Dict:
    """
    5-gate hybrid emission with LLM fusion.

    Gate 5 decision paths:
    - Path A: Direct organ (w_llm < 0.3, organ_conf > 0.7)
    - Path B: LLM scaffolded (w_llm > 0.6, organ_conf < 0.4)
    - Path C: Hybrid fusion (balanced)

    Args:
        organ_emission: Best emission from organ nexuses
        llm_emission: Memory-enriched LLM response
        organ_confidence: Organ emission confidence
        llm_confidence: LLM response confidence
        llm_weight: Current weaning weight (0-1)
        kairos_boost: Kairos multiplier (1.0 or 1.5)

    Returns:
        {
            'emission': final_text,
            'confidence': final_confidence,
            'emission_path': 'direct_organ'|'llm_scaffolded'|'hybrid_fusion',
            'organ_contribution': percentage,
            'llm_contribution': percentage
        }
    """
    from config import Config

    # Apply Kairos boost to both
    organ_conf_boosted = organ_confidence * kairos_boost
    llm_conf_boosted = llm_confidence * kairos_boost

    # PATH A: Direct organ reconstruction
    if llm_weight < 0.3 and organ_conf_boosted > 0.7:
        return {
            'emission': organ_emission,
            'confidence': organ_conf_boosted,
            'emission_path': 'direct_organ',
            'organ_contribution': 1.0,
            'llm_contribution': 0.0
        }

    # PATH B: LLM scaffolded
    elif llm_weight > 0.6 or organ_conf_boosted < 0.4:
        return {
            'emission': llm_emission,
            'confidence': llm_conf_boosted * 0.9,  # Slight penalty for scaffolding
            'emission_path': 'llm_scaffolded',
            'organ_contribution': 0.0,
            'llm_contribution': 1.0
        }

    # PATH C: Hybrid fusion
    else:
        fused_text = self._fuse_organ_llm_text(
            organ_emission,
            llm_emission,
            organ_weight=(1 - llm_weight),
            llm_weight=llm_weight
        )

        fused_confidence = (
            (1 - llm_weight) * organ_conf_boosted +
            llm_weight * llm_conf_boosted
        )

        return {
            'emission': fused_text,
            'confidence': fused_confidence,
            'emission_path': 'hybrid_fusion',
            'organ_contribution': (1 - llm_weight),
            'llm_contribution': llm_weight
        }

def _fuse_organ_llm_text(
    self,
    organ_text: str,
    llm_text: str,
    organ_weight: float,
    llm_weight: float
) -> str:
    """
    Fuse organ and LLM emissions into coherent response.

    Strategy:
    - High organ weight: Use LLM structure, organ content
    - High LLM weight: Use LLM content, organ tone
    - Balanced: Interleave or blend
    """
    if organ_weight > 0.7:
        # Organ-dominant: Extract felt qualities, apply to LLM structure
        return organ_text  # For now, simple version
    elif llm_weight > 0.7:
        # LLM-dominant: Use LLM text directly
        return llm_text
    else:
        # Balanced: Simple concatenation for MVP
        # TODO: Implement sophisticated blending
        return f"{organ_text}\n\n{llm_text}"
```

**Location:** Add after existing `generate_emission()` method

---

### File 3: `dae_interactive.py` (~150 lines)

**Wire hybrid components:**

```python
#!/usr/bin/env python3
"""
DAE Interactive Mode with Hybrid Superject Support
"""

from config import Config
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.phase5_learning_integration import Phase5LearningIntegration

# Hybrid components (conditional import)
if Config.HYBRID_ENABLED:
    from persona_layer.memory_retrieval import MemoryRetrieval
    from persona_layer.superject_recorder import SuperjectRecorder
    from persona_layer.local_llm_bridge import MemoryEnrichedLLMBridge

class DAEInteractive:
    """Interactive conversation with optional hybrid scaffolding."""

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id

        # Core organism
        self.organism = ConversationalOrganismWrapper()
        self.phase5 = Phase5LearningIntegration()

        # Hybrid components (if enabled)
        if Config.HYBRID_ENABLED:
            print("🆕 Hybrid mode ENABLED (experimental)")
            self.memory_retrieval = MemoryRetrieval(
                hebbian_memory_path=str(Config.HEBBIAN_MEMORY_PATH),
                organic_families_path=str(Config.ORGANIC_FAMILIES_PATH),
                top_k=Config.HYBRID_MEMORY_TOP_K
            )
            self.superject_recorder = SuperjectRecorder(
                session_storage_dir=str(Config.HYBRID_SUPERJECT_SESSION_DIR),
                user_bundles_dir=str(Config.HYBRID_SUPERJECT_USER_BUNDLES_DIR)
            )
            self.llm_bridge = MemoryEnrichedLLMBridge(
                model_name=Config.HYBRID_LLM_MODEL,
                ollama_url=Config.HYBRID_LLM_OLLAMA_URL
            )
            self.llm_weight = Config.HYBRID_LLM_INITIAL_WEIGHT

            # Start session
            self.session_id = self.superject_recorder.start_session(user_id=user_id)
        else:
            print("Pure DAE mode (hybrid disabled)")
            self.memory_retrieval = None
            self.superject_recorder = None
            self.llm_bridge = None

    def process_input(self, user_input: str) -> str:
        """Process user input through organism (with optional hybrid)."""

        # 1. Process through 11 organs
        organ_results = self.organism.process_text(user_input)

        # 2. Extract signature & assign family
        organ_signature = self.organism.extract_organ_signature(organ_results)
        family_id = self.phase5.assign_family(organ_signature)

        # 3. Memory retrieval (if hybrid)
        llm_response = None
        similar_moments = None
        if Config.HYBRID_ENABLED and self.llm_bridge:
            similar_moments = self.memory_retrieval.retrieve_similar_moments(
                current_organ_signature=organ_signature,
                current_family_id=family_id,
                user_id=self.user_id
            )
            user_bundle = self.memory_retrieval.load_user_bundle(self.user_id)

            # Query LLM with memory context
            llm_response = self.llm_bridge.query_with_memory(
                user_input=user_input,
                dae_felt_states={
                    'polyvagal': organ_results.get('EO', {}).get('polyvagal_state', 'unknown'),
                    'self_zone': organ_results.get('BOND', {}).get('self_zone', 0),
                    'top_organs': self.organism.get_top_organs(organ_results, k=3),
                },
                similar_moments=similar_moments,
                user_bundle=user_bundle
            )

        # 4. V0 convergence (hybrid if LLM available)
        v0_result = self.organism.converge_v0(
            organ_results=organ_results,
            llm_confidence=llm_response['confidence'] if llm_response else 0.0,
            llm_weight=self.llm_weight if Config.HYBRID_ENABLED else 0.0
        )

        # 5. Generate emission (hybrid if LLM available)
        if Config.HYBRID_ENABLED and llm_response:
            emission_result = self.organism.generate_hybrid_emission(
                organ_results=organ_results,
                llm_response=llm_response['response'],
                v0_result=v0_result,
                llm_weight=self.llm_weight
            )
        else:
            emission_result = self.organism.generate_emission(v0_result)

        # 6. Learn from conversation
        family_assignment = self.phase5.learn_from_conversation(
            organ_results=organ_results,
            emission=emission_result['emission']
        )

        # 7. Record superject (if hybrid)
        if Config.HYBRID_ENABLED and self.superject_recorder:
            self.superject_recorder.record_superject(
                user_message=user_input,
                dae_response=emission_result['emission'],
                organ_results=organ_results,
                felt_states={
                    'v0_energy': v0_result.get('v0_energy_final', 0.0),
                    'satisfaction_score': v0_result.get('satisfaction', 0.0),
                    'emission_confidence': emission_result['confidence'],
                    'emission_path': emission_result.get('emission_path', 'unknown'),
                },
                family_assignment=family_assignment,
                user_id=self.user_id
            )

        return emission_result['emission']

if __name__ == "__main__":
    interactive = DAEInteractive()
    print("\nDAE Interactive (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        response = interactive.process_input(user_input)
        print(f"DAE: {response}\n")
```

---

### File 4: `tests/integration/test_hybrid_integration.py` (~200 lines)

**Create integration tests:**

```python
#!/usr/bin/env python3
"""
Integration tests for hybrid superject architecture.
"""

import pytest
from config import Config
from persona_layer.memory_retrieval import MemoryRetrieval
from persona_layer.superject_recorder import SuperjectRecorder
from persona_layer.local_llm_bridge import MemoryEnrichedLLMBridge

def test_hybrid_disabled_equals_pure_dae():
    """Verify hybrid mode with LLM disabled produces identical results."""
    Config.HYBRID_ENABLED = False
    # TODO: Implement test
    pass

def test_memory_retrieval_integration():
    """Verify memory retrieval returns similar moments."""
    memory = MemoryRetrieval()
    # TODO: Implement test
    pass

def test_superject_recording():
    """Verify superjections are recorded correctly."""
    recorder = SuperjectRecorder()
    # TODO: Implement test
    pass

def test_llm_fallback():
    """Verify graceful fallback when LLM unavailable."""
    # TODO: Implement test
    pass

def test_multiturn_conversation():
    """Verify memory continuity across turns."""
    # TODO: Implement test
    pass
```

---

## 🎯 Implementation Order

**Total estimated time: 3-4 hours**

1. **conversational_occasion.py** (30 min)
   - Add `compute_v0_energy_hybrid()` method
   - Test with Config.HYBRID_ENABLED = False (should match pure DAE)

2. **emission_generator.py** (45 min)
   - Add `generate_hybrid_emission()` method
   - Add `_fuse_organ_llm_text()` helper
   - Test three emission paths

3. **dae_interactive.py** (90 min)
   - Wire hybrid components (conditional on Config.HYBRID_ENABLED)
   - Test with hybrid disabled (pure DAE)
   - Test with hybrid enabled + Ollama running

4. **Integration tests** (60 min)
   - Implement 5 test cases
   - Run full test suite
   - Verify 100% maturity maintained

---

## ✅ Completion Criteria

**Week 2 will be complete when:**
- [ ] Hybrid V0 descent method implemented
- [ ] Gate 5 LLM fusion implemented
- [ ] dae_interactive.py wiring complete
- [ ] Integration tests passing
- [ ] End-to-end validation (multi-turn conversation)
- [ ] Documentation updated (CLAUDE.md)

---

## 📝 Testing Strategy

**1. Unit Tests:**
- `test_hybrid_v0_energy()` - Verify formula correctness
- `test_gate5_fusion_paths()` - Verify 3 emission paths
- `test_memory_retrieval()` - Verify prehensive recall
- `test_superject_persistence()` - Verify session logs

**2. Integration Tests:**
- `test_hybrid_disabled()` - Pure DAE equivalence
- `test_hybrid_enabled()` - LLM scaffolding
- `test_multiturn_memory()` - Conversational continuity
- `test_llm_fallback()` - Graceful degradation

**3. End-to-End Validation:**
```bash
# Enable hybrid mode
Config.HYBRID_ENABLED = True

# Start Ollama
ollama serve

# Run interactive
python3 dae_interactive.py

# Test conversation
You: I'm feeling overwhelmed right now.
DAE: [memory-enriched LLM scaffolded response]

You: That helps. Tell me more.
DAE: [should prehend Turn 1, show continuity]

You: What did I just say?
DAE: [should recall "overwhelmed" from memory]
```

---

## 🚀 Ready for Implementation

**All components specified. Ready to code when you are!**

**Estimated delivery:** 3-4 hours for complete Week 2 integration

---

🌀 **"Week 1 foundation complete. Mathematical model refined. Configuration added. Ready for Week 2 wiring."** 🌀

**Date:** November 13, 2025, 2:00 AM
**Status:** ✅ WEEK 1 COMPLETE + CONFIG - WEEK 2 SPEC READY
