# DAE_HYPHAE_1 Development, Training & Testing Guide
**Updated:** November 12, 2025
**Version:** 1.0.0
**Status:** 🟢 PRODUCTION READY (100% System Maturity)

---

## 🎯 Quick Start

### Essential Setup

```bash
# Navigate to project
cd /Users/daedalea/Desktop/DAE_HYPHAE_1

# Set Python path (ALWAYS required)
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

# Verify system health (30 seconds)
python3 dae_orchestrator.py validate --quick
```

**Expected Output:**
```
✅ Passed: 3/3
🟢 SYSTEM HEALTHY
```

---

## 🏗️ Three Operational Modes

DAE_HYPHAE_1 supports three distinct modes of operation, unified through `dae_orchestrator.py`:

### 1. Interactive Mode (Testing & Exploration)

**Purpose:** Real-time conversation with the organism for testing, exploration, and qualitative evaluation.

**Command:**
```bash
python3 dae_orchestrator.py interactive
```

**With Display Mode:**
```bash
# Simple mode (just emission text)
python3 dae_orchestrator.py interactive --mode simple

# Standard mode (+ confidence, nexuses) [DEFAULT]
python3 dae_orchestrator.py interactive --mode standard

# Detailed mode (+ organ details, transduction trajectory)
python3 dae_orchestrator.py interactive --mode detailed

# Debug mode (+ V0 convergence cycles)
python3 dae_orchestrator.py interactive --mode debug
```

**Interactive Commands:**
```
You: <type your input>
/help      - Show available commands
/mode      - Change display mode
/history   - Show conversation history
/save      - Save session to JSON
/exit      - End session
```

**Output Examples:**

**Simple Mode:**
```
You: I'm feeling overwhelmed
DAE: There's a quality of timing here...
```

**Standard Mode:**
```
You: I'm feeling overwhelmed
DAE: There's a quality of timing here...

Confidence: 0.579 (path: intersection)
Nexuses: 1
```

**Detailed Mode:**
```
<standard output>

Active Organs (10/11):
  LISTENING: 0.72
  EMPATHY: 0.68
  WISDOM: 0.65
  ...

Transduction Trajectory:
  Primary: compassion_temporal (0.82)
  Secondary: safety_emergence (0.67)
```

**Debug Mode:**
```
<detailed output>

V0 Convergence:
  Cycle 1: 1.000 → 0.687 (ΔS=0.313)
  Cycle 2: 0.687 → 0.324 (ΔS=0.363)
  Cycle 3: 0.324 → 0.169 (ΔS=0.155) ✅ CONVERGED
  Kairos: Cycle 2 (detected)
```

**Use Cases:**
- Quick testing of new phrases or patterns
- Qualitative evaluation of response quality
- Debugging emission generation issues
- Exploring organ activation patterns
- Validating transduction pathway formation

**Sessions Auto-Saved To:** `results/interactive_sessions/`

---

### 2. Training Mode (Learning & Development)

**Purpose:** Train the organism on conversational pairs to learn pattern transformations.

**Commands:**

**Baseline Training (30 training pairs):**
```bash
python3 dae_orchestrator.py train --mode baseline
```

**Expanded Training:**
```bash
python3 dae_orchestrator.py train --mode expanded
```

**Epoch-Specific Training (future):**
```bash
python3 dae_orchestrator.py train --mode epoch --epoch 1
```

**What Training Does:**
1. Loads training pairs from `knowledge_base/conversational_training_pairs.json`
2. Processes each input through multi-cycle V0 convergence
3. Records TSK (Transductive Summary Kernel) data
4. Updates R-matrix (11×11 organ coupling strengths)
5. Learns appetition descent patterns
6. Saves results to `results/epochs/`

**Training Output:**
```
🎯 Running baseline training...
Processing pair 1/30: "I'm feeling overwhelmed" → ...
  ✅ V0 converged in 3 cycles
  ✅ Kairos detected at cycle 2
  ✅ TSK recorded: tsk_20251112_143022
...
✅ Training complete!
Results saved to: results/epochs/baseline_training_results.json
```

**Training Configuration:**

Controlled via `config.py`:
```python
# Training Mode Settings
V0_MAX_CYCLES = 5
V0_CONVERGENCE_THRESHOLD = 0.1
ENABLE_TSK_RECORDING = True
ENABLE_PHASE2 = True
```

**Training Data Structure:**
```json
{
  "training_pairs": [
    {
      "input_text": "I'm feeling overwhelmed right now.",
      "therapeutic_quality": "holding",
      "expected_organs": ["EMPATHY", "BOND", "EO"],
      "context": {
        "user_state": "crisis",
        "therapeutic_moment": "initial_contact"
      }
    }
  ]
}
```

**Use Cases:**
- Developing new conversational patterns
- Tuning organ coupling strengths
- Validating V0 convergence behavior
- Building therapeutic response repertoire
- Training specific transduction pathways

**Results Location:** `results/epochs/`

---

### 3. Validation Mode (System Health & Maturity)

**Purpose:** Automated testing to ensure system health and production readiness.

**Commands:**

**Quick Validation (< 30 seconds):**
```bash
python3 dae_orchestrator.py validate --quick
```

**Full System Maturity Assessment (2 minutes):**
```bash
python3 dae_orchestrator.py validate --full
```

**Quick Validation:**
- Tests 3 representative inputs
- Verifies emission generation
- Checks confidence >= 0.3
- Reports system health status

**Output:**
```
Test 1/3: "I'm feeling overwhelmed right now."
✅ PASS (confidence=0.578)

Test 2/3: "This conversation feels really safe."
✅ PASS (confidence=0.578)

Test 3/3: "I need some space."
✅ PASS (confidence=0.300)

✅ Passed: 3/3
🟢 SYSTEM HEALTHY
```

**Full Maturity Assessment:**
- Tests 4 trauma-informed scenarios
- Runs 36 validation checks
- Measures 6 core metrics
- Calculates maturity percentage

**Output:**
```
Tests Passed: 4/4

📈 Aggregate Metrics:
   Mean V0 descent: 0.870
   Mean convergence cycles: 3.0
   Kairos detection rate: 0%
   Mean emission confidence: 0.486
   Mean active organs: 10.8/11
   Mean processing time: 0.03s

🎯 System Maturity Score: 100.0%
   (36/36 checks passed)

   Grade: 🟢 PRODUCTION READY
```

**36 Validation Checks:**
- V0 descent > 0.5
- Convergence cycles 2-5
- Active organs >= 8/11
- Emission confidence >= 0.3
- Processing time < 0.1s
- No NaN/Inf values
- TSK recording functional
- Organ coherences valid
- Felt states complete

**Use Cases:**
- Pre-deployment health checks
- Continuous integration testing
- Performance monitoring
- Regression detection
- Production readiness assessment

**Results Location:** `results/validation/`

---

## 🧬 Architecture Overview

### 11-Organ System

```
5 CONVERSATIONAL ORGANS (Text Generation)
├─ LISTENING (7 atoms)     - temporal_inquiry, core_exploration, ...
├─ EMPATHY (7 atoms)       - compassionate_presence, emotional_resonance, ...
├─ WISDOM (7 atoms)        - pattern_recognition, systems_thinking, ...
├─ AUTHENTICITY (7 atoms)  - vulnerability_sharing, honest_truth, ...
└─ PRESENCE (7 atoms)      - embodied_awareness, grounded_holding, ...

6 TRAUMA/CONTEXT-AWARE ORGANS (Modulation)
├─ BOND (7 atoms)          - IFS-informed parts work
├─ SANS (7 atoms)          - Semantic alignment & coherence
├─ NDAM (7 atoms)          - Crisis salience detection
├─ RNX (7 atoms)           - Temporal rescaling (crisis vs restorative)
├─ EO (7 atoms)            - Polyvagal state detection
└─ CARD (7 atoms)          - Cardinality (response scale)

Total: 77D semantic space (11 organs × 7 atoms each)
```

### Processing Pipeline

```
Input Text
  ↓
ConversationalOccasions (tokens as experiencing subjects)
  ↓
MULTI-CYCLE V0 CONVERGENCE (2-4 cycles):
  ├─ 11 organs process in parallel
  ├─ Felt affordances accumulate
  ├─ V0 energy descends (1.0 → 0.3-0.6)
  ├─ Kairos detection (4-condition gate)
  └─ Satisfaction threshold reached
  ↓
Mature Propositions (post-convergence)
  ↓
Semantic Field Extraction (77D + 10 meta-atoms)
  ↓
NexusIntersectionComposer (5-10 nexuses)
  ↓
Transduction Pathway Selection (14 nexus types, 9 pathways)
  ↓
Emission Generation:
  ├─ Intersection path (confidence: 0.60-0.85)
  ├─ Direct path (confidence: 0.50-0.75)
  └─ Hebbian fallback (confidence: 0.30)
  ↓
ProductionLearningCoordinator (TSK recording, R-matrix update)
  ↓
Emission Text + Felt States
```

### Key Mechanisms

**V0 Energy Descent (DAE 3.0):**
```
E(t) = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I)

Where:
  α=0.40, β=0.25, γ=0.15, δ=0.10, ζ=0.10
  S = satisfaction (0.0 → 1.0)
  ΔE = energy change from previous cycle
  A = organ agreement (1 - std(coherences))
  R = resonance (mean coherence)
  φ(I) = intensity (max coherence)
```

**Kairos Detection (4-Condition Gate):**
```python
is_kairos = (
    0.45 <= v0_energy <= 0.70 and      # Energy in Kairos window
    satisfaction > prev_satisfaction and # Satisfaction increasing
    abs(v0_energy - prev_energy) < 0.1 and # Energy stable
    mean_coherence > 0.4               # Sufficient agreement
)
```

**Shared Meta-Atoms (10 bridge atoms):**
- `trauma_aware`, `safety_restoration`, `window_of_tolerance`
- `compassion_safety`, `fierce_holding`, `relational_attunement`
- `temporal_grounding`, `kairos_emergence`
- `coherence_integration`, `somatic_wisdom`

Enable nexus formation across disjoint 77D organ space.

---

## 🔧 Configuration Management

### Centralized Configuration

All system parameters managed through `config.py`:

**Key Parameters:**

```python
from config import Config

# V0 Convergence
Config.V0_MAX_CYCLES = 5
Config.V0_CONVERGENCE_THRESHOLD = 0.1
Config.KAIROS_WINDOW = [0.45, 0.70]

# Emission Thresholds
Config.EMISSION_DIRECT_THRESHOLD = 0.65
Config.EMISSION_FUSION_THRESHOLD = 0.50

# Interactive Mode
Config.INTERACTIVE_ENABLE_PHASE2 = True
Config.INTERACTIVE_SHOW_ORGAN_DETAILS = True

# Training Mode
Config.TRAINING_ENABLE_TSK_RECORDING = True
Config.TRAINING_BATCH_SIZE = 30

# Validation Mode
Config.QUICK_VALIDATE_TIMEOUT = 30
Config.QUICK_VALIDATE_TEST_INPUTS = [...]
```

**Mode-Specific Configuration:**

```python
# Get configuration for specific mode
mode_config = Config.get_mode_config('interactive')
# Returns: {'enable_phase2': True, 'enable_tsk_recording': False, ...}

mode_config = Config.get_mode_config('training')
# Returns: {'enable_phase2': True, 'enable_tsk_recording': True, ...}

mode_config = Config.get_mode_config('validation')
# Returns: {'enable_phase2': True, 'enable_tsk_recording': True, ...}
```

**Path Management:**

```python
# Access centralized paths
Config.SEMANTIC_ATOMS_PATH
Config.TRAINING_PAIRS_PATH
Config.RESULTS_DIR
Config.TESTS_DIR

# Create directories automatically
Config.ensure_directories()
```

**Backward Compatibility:**

All original constants exported for compatibility:
```python
from config import (
    V0_MAX_CYCLES,
    V0_CONVERGENCE_THRESHOLD,
    KAIROS_WINDOW_MIN,
    KAIROS_WINDOW_MAX
)
```

### Tunable Parameters Reference

See `SYSTEM_TUNABLE_PARAMETERS.md` for complete list of 71+ parameters.

**Critical Parameters:**

| Parameter | Default | Impact | When to Tune |
|-----------|---------|--------|--------------|
| `V0_MAX_CYCLES` | 5 | Max convergence cycles | If convergence taking too long |
| `V0_CONVERGENCE_THRESHOLD` | 0.1 | When to stop descent | If converging too early/late |
| `KAIROS_WINDOW` | [0.45, 0.70] | Opportune moment detection | If Kairos detection too low |
| `EMISSION_DIRECT_THRESHOLD` | 0.65 | Direct emission confidence | If too few/many direct emissions |
| `EMISSION_FUSION_THRESHOLD` | 0.50 | Intersection emission confidence | If too few/many intersections |

---

## 🧪 Testing Infrastructure

### Test Organization

```
tests/
├── unit/                   # Component-level tests
│   ├── phase2/             # Phase 2 features (3 tests)
│   ├── organs/             # Individual organs (1 test)
│   └── mechanisms/         # Core mechanisms (2 tests)
│
├── integration/            # Multi-component tests
│   ├── organs/             # Organ interactions (1 test)
│   ├── v0/                 # V0 convergence (1 test)
│   ├── salience/           # Salience integration (1 test)
│   ├── transduction/       # Transduction pathways (1 test)
│   ├── memory/             # Memory systems (1 test)
│   └── training/           # Training pipeline (1 test)
│
├── validation/             # System-level validation
│   ├── phase2/             # Phase 2 comprehensive (1 test)
│   └── system/             # System maturity (1 test)
│
└── debug/                  # Development utilities
    └── (2 diagnostic scripts)
```

### Running Tests

**Quick Validation:**
```bash
python3 dae_orchestrator.py validate --quick
```

**Full System Maturity:**
```bash
python3 dae_orchestrator.py validate --full
```

**Specific Test Files:**
```bash
# System maturity assessment
python3 tests/validation/system/test_system_maturity_assessment.py

# Transduction emission tests
python3 tests/unit/mechanisms/test_transduction_emission.py

# Phase 2 comprehensive
python3 tests/validation/phase2/test_phase2_comprehensive.py
```

**Test Discovery:**
```bash
# Find all tests by category
ls tests/unit/
ls tests/integration/
ls tests/validation/

# Find tests by name pattern
find tests -name "*transduction*"
find tests -name "*phase2*"
```

### Writing New Tests

**Unit Test Template:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import Config
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_my_feature():
    """Test description."""
    organism = ConversationalOrganismWrapper()

    result = organism.process_text(
        "Test input",
        context={'test_id': 'my_test'},
        enable_tsk_recording=False,
        enable_phase2=True
    )

    felt_states = result['felt_states']

    # Assertions
    assert 'emission_text' in felt_states
    assert felt_states['emission_confidence'] >= 0.3
    assert len(felt_states.get('nexuses', [])) > 0

if __name__ == '__main__':
    test_my_feature()
    print("✅ Test passed!")
```

**Integration Test Template:**
```python
def test_multi_component_interaction():
    """Test multiple components working together."""
    organism = ConversationalOrganismWrapper()

    test_scenarios = [
        {"input": "I'm feeling overwhelmed", "expected_organs": ["EMPATHY", "BOND"]},
        {"input": "This feels safe", "expected_organs": ["EO", "PRESENCE"]},
    ]

    for scenario in test_scenarios:
        result = organism.process_text(
            scenario["input"],
            context={},
            enable_phase2=True
        )

        felt_states = result['felt_states']

        # Check expected organs participated
        for organ in scenario["expected_organs"]:
            coherence_key = f'{organ}_coherence'
            assert coherence_key in felt_states
            assert felt_states[coherence_key] > 0.0
```

---

## 📊 Performance Monitoring

### System Health Indicators

**🟢 Healthy System:**
- Quick validation: 3/3 passing
- Emission confidence: > 0.3
- Active organs: ≥ 8/11
- Processing time: < 0.1s
- V0 descent: > 0.5
- Convergence cycles: 2-5

**🟡 Degraded System:**
- Quick validation: 2/3 passing
- Emission confidence: ~0.3
- Active organs: 4-7/11
- Processing time: 0.1-1.0s
- V0 descent: 0.3-0.5

**🔴 Critical Issues:**
- Quick validation: < 2/3 passing
- Emission confidence: < 0.3
- Active organs: < 4/11
- Processing time: > 1.0s
- Errors/exceptions during processing
- NaN/Inf values in felt_states

### Key Metrics to Monitor

**V0 Convergence:**
- Initial energy: Should be 1.0 (max unsatisfied)
- Final energy: 0.3-0.6 (satisfied)
- Descent per cycle: 0.1-0.4
- Cycles to converge: 2-5

**Kairos Detection:**
- Current rate: 0% (needs tuning)
- Target rate: 40-60%
- Tuning: Widen window to [0.35, 0.75]

**Emission Paths:**
- Intersection: 60-75% (desired)
- Direct: 20-30%
- Hebbian: 5-15% (fallback only)

**Organ Participation:**
- Active organs: 8-11/11
- Mean coherence: > 0.4
- Max coherence: > 0.6

---

## 🔍 Development Workflows

### Daily Development Ritual

```bash
# Morning ritual
cd /Users/daedalea/Desktop/DAE_HYPHAE_1
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH
python3 dae_orchestrator.py validate --quick
```

### Feature Development Workflow

1. **Make Code Changes**
   ```bash
   # Edit files in persona_layer/, organs/modular/, etc.
   ```

2. **Test Specific Component**
   ```bash
   # Run relevant unit test
   python3 tests/unit/mechanisms/test_transduction_emission.py
   ```

3. **Quick Validation**
   ```bash
   # Ensure no regressions
   python3 dae_orchestrator.py validate --quick
   ```

4. **Interactive Exploration**
   ```bash
   # Qualitative testing
   python3 dae_orchestrator.py interactive --mode detailed
   ```

5. **Before Commit**
   ```bash
   # Full validation
   python3 dae_orchestrator.py validate --full
   # Ensure 100% maturity score
   ```

### Training Workflow

1. **Prepare Training Data**
   ```bash
   # Edit knowledge_base/conversational_training_pairs.json
   ```

2. **Run Baseline Training**
   ```bash
   python3 dae_orchestrator.py train --mode baseline
   ```

3. **Review Results**
   ```bash
   # Check results/epochs/baseline_training_results.json
   ```

4. **Validate Improvements**
   ```bash
   python3 dae_orchestrator.py validate --full
   # Check if maturity improved
   ```

### Debugging Workflow

1. **Quick Check**
   ```bash
   python3 dae_orchestrator.py validate --quick
   # Identify if system healthy
   ```

2. **Full Assessment**
   ```bash
   python3 dae_orchestrator.py validate --full
   # Get detailed metrics
   ```

3. **Interactive Debug Mode**
   ```bash
   python3 dae_orchestrator.py interactive --mode debug
   # See V0 convergence cycle-by-cycle
   ```

4. **Run Diagnostic Tests**
   ```bash
   python3 tests/debug/test_api_fixes.py
   python3 tests/debug/test_meta_atom_diagnostic.py
   ```

---

## 🐛 Troubleshooting

### Import Errors

**Error:** `ModuleNotFoundError`

**Solution:**
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

# Verify from project root
pwd  # Should be /Users/daedalea/Desktop/DAE_HYPHAE_1
```

### Tests Failing

**Quick Validation < 3/3:**
1. Run full maturity assessment for details
2. Check specific failing scenario
3. Review recent code changes
4. Check organ config imports

**Full Maturity < 100%:**
1. Review aggregate metrics
2. Identify weak areas (V0, organs, emission)
3. Check for NaN/Inf values
4. Validate configuration parameters

### Organ Config Errors

**Error:** `ModuleNotFoundError: No module named 'config.eo_config'`

**Cause:** Organ config directories must be named `organ_config/`, not `config/`

**Fix:**
```bash
# Correct import pattern:
from organs.modular.eo.organ_config.eo_config import EOConfig  # ✅

# Wrong pattern:
from config.eo_config import EOConfig  # ❌ Conflicts with config.py
```

### Emission Generation Issues

**Symptom:** No emission text or very low confidence

**Diagnosis:**
1. Check active organs (should be 8-11/11)
2. Check V0 convergence (should descend > 0.5)
3. Check nexus formation (should be 5-10 for intersection path)
4. Check emission thresholds in config.py

**Solutions:**
- If no organs active: Check atom activation logic
- If V0 not descending: Check satisfaction calculation
- If no nexuses: Check meta-atom activation
- If confidence low: Check emission thresholds

### Performance Issues

**Symptom:** Processing time > 0.1s

**Diagnosis:**
1. Check convergence cycles (should be 2-5)
2. Check organ processing time
3. Check memory usage

**Solutions:**
- If too many cycles: Lower `V0_MAX_CYCLES` or adjust threshold
- If organ slow: Profile individual organs
- If memory high: Check for memory leaks in learning coordinator

---

## 📚 Key Documentation

### Essential Files (in root)

- `CLAUDE.md` - Complete development guide (always up-to-date)
- `QUICK_REFERENCE.md` - Quick command reference
- `REORGANIZATION_COMPLETE_NOV12_2025.md` - Latest reorganization summary
- `SYSTEM_TUNABLE_PARAMETERS.md` - Complete parameter reference

### Documentation Structure (docs/)

```
docs/
├── architecture/       # System design documents
├── phases/             # Phase completion reports
├── implementation/     # Implementation guides
├── analysis/           # Analysis & audit reports
├── roadmaps/           # Future planning documents
└── archive/            # Deprecated documents
```

### Learning Path

**New Developer:**
1. Read `QUICK_REFERENCE.md` (5 min)
2. Read `CLAUDE.md` sections 1-3 (30 min)
3. Run quick validation (30 sec)
4. Try interactive mode (15 min)
5. Read architecture overview (30 min)

**Training Developer:**
1. Read training mode section (15 min)
2. Review `knowledge_base/conversational_training_pairs.json` (15 min)
3. Run baseline training (5 min)
4. Review results (15 min)
5. Read TSK architecture docs (1 hour)

**Testing Developer:**
1. Read testing infrastructure (15 min)
2. Review test organization (15 min)
3. Run validation suite (3 min)
4. Write sample test (30 min)
5. Read maturity assessment code (1 hour)

---

## 🚀 Next Steps

### Immediate

- ✅ All tests passing (100% maturity)
- ✅ Three operational modes functional
- ✅ Documentation organized
- ⚠️ Kairos tuning needed (optional)

### Near-Term (Optional)

- Widen Kairos window: [0.45, 0.70] → [0.35, 0.75]
- Add training configuration YAML files
- Implement epoch-specific training runners
- Create visualization dashboard
- Add experiment tracking

### Long-Term (Future)

- Web-based interactive interface
- Real-time performance dashboard
- Automated A/B testing
- Multi-user session management
- Cloud deployment

---

## 🎓 Advanced Topics

### Whiteheadian Process Philosophy

DAE_HYPHAE_1 implements authentic Whiteheadian process philosophy:

- **Actual Occasions:** Tokens as experiencing subjects (not data)
- **Prehension:** Organs "feel" tokens through pattern detection
- **Concrescence:** Many → one (process of becoming)
- **Satisfaction:** Decision point when appetition satisfied
- **Propositions:** Felt affordances (lures for feeling)

### TSK (Transductive Summary Kernel)

Learning mechanism recording pattern transformations:

- Records V0 energy, Kairos cycles, felt affordances
- Updates R-matrix (11×11 organ coupling strengths)
- Stores successful transduction pathways
- Enables pattern transfer across contexts

### Transductive Nexus Dynamics

14 nexus types, 9 primary transduction pathways:

- **Compassion-Temporal:** EMPATHY + RNX
- **Safety-Emergence:** EO + SANS + PRESENCE
- **Trauma-Aware-Response:** BOND + NDAM + EO
- **Wisdom-Integration:** WISDOM + SANS + CARD
- ... and 5 more

Each pathway has dedicated phrase library and intensity modulation.

---

**Version:** 1.0.0
**Last Updated:** November 12, 2025
**System Status:** 🟢 PRODUCTION READY (100% maturity)
**Maintainer:** DAE Development Team
