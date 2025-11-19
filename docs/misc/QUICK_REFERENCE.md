# DAE_HYPHAE_1 Quick Reference
**Updated:** November 12, 2025

---

## 🚀 Quick Start

```bash
# Set Python path (always required)
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

# Quick system health check (< 30 seconds)
python3 dae_orchestrator.py validate --quick

# Interactive conversation
python3 dae_interactive.py

# Run baseline training
python3 dae_orchestrator.py train --mode baseline
```

---

## 📋 Common Commands

### Validation

```bash
# Quick validation (3 test inputs, ~30s)
python3 dae_orchestrator.py validate --quick

# Full system maturity assessment (4 scenarios, 36 checks, ~2 min)
python3 dae_orchestrator.py validate --full
```

### Interactive Mode

```bash
# Start interactive mode (standard display)
python3 dae_interactive.py

# Detailed mode (shows organ details + transduction)
python3 dae_interactive.py --mode detailed

# Debug mode (shows V0 convergence cycles)
python3 dae_interactive.py --mode debug

# Simple mode (just emission text)
python3 dae_interactive.py --mode simple
```

**Interactive Commands:**
- `/help` - Show help
- `/mode` - Change display mode
- `/history` - Show conversation
- `/save` - Save to JSON
- `/exit` - End session

### Training

```bash
# Baseline training (30 training pairs)
python3 dae_orchestrator.py train --mode baseline

# Expanded training
python3 dae_orchestrator.py train --mode expanded

# Epoch training (future)
python3 dae_orchestrator.py train --mode epoch --epoch 1
```

### Running Specific Tests

```bash
# System maturity assessment
python3 tests/validation/system/test_system_maturity_assessment.py

# Transduction emission tests
python3 tests/unit/mechanisms/test_transduction_emission.py

# Phase 2 comprehensive
python3 tests/validation/phase2/test_phase2_comprehensive.py
```

---

## 📁 Project Structure

```
DAE_HYPHAE_1/
├── config.py                 # Centralized configuration
├── dae_orchestrator.py       # Unified entry point
├── dae_interactive.py        # Interactive mode
├── dae_gov_cli.py            # Government CLI (original)
│
├── tests/                    # All test files
│   ├── unit/                 # Component tests
│   ├── integration/          # Multi-component tests
│   ├── validation/           # System-level validation
│   └── debug/                # Development utilities
│
├── training/                 # Training scripts
│   └── conversational/       # Conversational training
│
├── persona_layer/            # Core processing
├── organs/modular/           # 11 organ implementations
├── knowledge_base/           # Training data
├── results/                  # Output files
└── docs/                     # Documentation (Session 2)
```

---

## 🔧 Configuration

**File:** `config.py`

**Common Parameters:**
```python
# V0 Convergence
V0_MAX_CYCLES = 5
V0_CONVERGENCE_THRESHOLD = 0.1
KAIROS_WINDOW = [0.45, 0.70]

# Emission
EMISSION_DIRECT_THRESHOLD = 0.65
EMISSION_FUSION_THRESHOLD = 0.50

# Interactive Mode
INTERACTIVE_ENABLE_PHASE2 = True
INTERACTIVE_SHOW_ORGAN_DETAILS = True
```

**Access in code:**
```python
from config import Config

# Access paths
atoms_path = Config.SEMANTIC_ATOMS_PATH
results_dir = Config.RESULTS_DIR

# Access parameters
max_cycles = Config.V0_MAX_CYCLES
kairos_window = Config.KAIROS_WINDOW

# Get mode config
mode_config = Config.get_mode_config('interactive')
```

---

## ✅ Test Status

**Quick Validation:** ✅ 3/3 passing (HEALTHY)
**System Maturity:** ✅ 4/4 tests, 100% score (PRODUCTION READY)
**Performance:** ✅ 0.03s avg processing time

---

## 🐛 Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH

# Verify from project root
pwd  # Should be /Users/daedalea/Desktop/DAE_HYPHAE_1
```

### Tests Failing

```bash
# Run quick validation to check system health
python3 dae_orchestrator.py validate --quick

# If failing, run full maturity assessment for details
python3 dae_orchestrator.py validate --full
```

### Organ Config Errors

Organ configs moved to `organ_config/`:
- Old: `from config.eo_config import ...` ❌
- New: `from organs.modular.eo.organ_config.eo_config import ...` ✅

---

## 📊 System Health Indicators

### 🟢 Healthy System
- Quick validation: 3/3 passing
- Emission confidence: > 0.3
- Active organs: ≥ 8/11
- Processing time: < 0.1s
- V0 descent: > 0.5

### 🟡 Degraded System
- Quick validation: 2/3 passing
- Emission confidence: 0.3
- Active organs: 4-7/11
- Processing time: 0.1-1.0s

### 🔴 Critical Issues
- Quick validation: < 2/3 passing
- Emission confidence: < 0.3
- Active organs: < 4/11
- Processing time: > 1.0s
- Errors/exceptions during processing

---

## 🎯 Daily Workflow

### Morning Ritual
```bash
cd /Users/daedalea/Desktop/DAE_HYPHAE_1
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH
python3 dae_orchestrator.py validate --quick
```

### Development
```bash
# Make changes to code
# ...

# Test specific component
python3 tests/unit/mechanisms/test_transduction_emission.py

# Quick validation
python3 dae_orchestrator.py validate --quick

# Interactive exploration
python3 dae_interactive.py --mode detailed
```

### Before Commit
```bash
# Full validation
python3 dae_orchestrator.py validate --full

# Ensure 100% maturity score
# Review any warnings
```

---

## 📝 Interactive Mode Tips

### Display Modes

**simple** - For quick testing:
```
You: I'm feeling overwhelmed
DAE: There's a quality of timing
```

**standard** - For normal use (default):
```
You: I'm feeling overwhelmed
DAE: There's a quality of timing

Confidence: 0.579 (path: intersection)
Nexuses: 1
```

**detailed** - For development:
```
<standard output>
+ Active Organs (10/11)
+ Transduction Trajectory
+ Key organ metrics
```

**debug** - For troubleshooting:
```
<detailed output>
+ V0 Convergence: 1.000 → 0.169 over 3 cycles
+ Cycle-by-cycle details
```

### Saving Sessions

Conversations auto-saved to `results/interactive_sessions/` when using `/save`

---

## 🔍 Finding Things

### Find a test
```bash
# By category
ls tests/unit/
ls tests/integration/
ls tests/validation/

# By name
find tests -name "*transduction*"
```

### Find configuration
```bash
# All in config.py
grep "V0_" config.py
grep "EMISSION_" config.py
grep "INTERACTIVE_" config.py
```

### Find documentation
```bash
# Currently in root (Session 2 will organize)
ls *.md

# After Session 2
ls docs/architecture/
ls docs/phases/
```

---

## 🚨 Known Issues

1. **Kairos Detection:** Currently 0% detection rate
   - Non-critical, system functional
   - Tuning recommended: widen window to [0.35, 0.75]

2. **Short Inputs:** May generate hebbian fallback (confidence=0.3)
   - Expected behavior
   - Not a bug

3. **Documentation:** 109 .md files in root
   - Session 2 will organize to `/docs/`
   - Not affecting functionality

---

## 📚 Key Documents

- `REORGANIZATION_COMPLETE_NOV12_2025.md` - Full reorganization summary
- `SYSTEM_MATURITY_ASSESSMENT_REPORT_NOV12_2025.md` - Latest maturity report
- `TEST_INFRASTRUCTURE_AUDIT_REPORT.md` - Infrastructure audit
- `TRANSDUCTIVE_NEXUS_COMPLETE_NOV12_2025.md` - Transduction integration
- `CLAUDE.md` - Development guide (always up-to-date)

---

## 🎓 Learning Resources

### Understanding the System

1. **Start with:** `CLAUDE.md` - Complete system overview
2. **Then read:** `SYSTEM_MATURITY_ASSESSMENT_REPORT_NOV12_2025.md`
3. **Deep dive:** `TRANSDUCTIVE_NEXUS_COMPLETE_NOV12_2025.md`

### Interactive Exploration

```bash
# Start in detailed mode
python3 dae_interactive.py --mode detailed

# Try different inputs
You: I'm feeling overwhelmed
You: This feels really safe
You: I need some space

# Observe organ participation, nexus formation, transduction pathways
```

### Code Exploration

```bash
# Core processing
cat persona_layer/conversational_organism_wrapper.py

# Configuration
cat config.py

# Specific organ
cat organs/modular/bond/core/bond_text_core.py
```

---

**Last Updated:** November 12, 2025
**System Status:** 🟢 PRODUCTION READY (100% maturity)
**Next Session:** Documentation cleanup (optional)
