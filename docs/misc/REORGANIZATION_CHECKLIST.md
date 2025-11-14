# DAE_HYPHAE_1 Test Infrastructure Reorganization - Action Checklist

**Status:** Ready to Execute  
**Estimated Total Time:** 10.5 hours  
**Recommended Split:** 3 sessions (4h, 3h, 3.5h)

---

## Session 1: Foundation & Test Organization (4 hours)

### Phase 1: Preparation (2 hours)

- [ ] **Create directory structure** (30 min)
  ```bash
  cd /Users/daedalea/Desktop/DAE_HYPHAE_1
  
  # Test directories
  mkdir -p tests/{unit,integration,validation,debug,infrastructure,fixtures,utilities}
  mkdir -p tests/unit/{phase1,phase2,organs,learning,mechanisms}
  mkdir -p tests/integration/{organs,v0,salience,transduction,memory,training}
  mkdir -p tests/validation/{phase1,phase2}
  
  # Training directories
  mkdir -p training/conversational
  mkdir -p training/configs
  
  # Scripts directories
  mkdir -p scripts/{quick_validate,profiling,debugging,archive}
  mkdir -p scripts/archive/{phase1_migration,phase2_migration}
  
  # Documentation directories
  mkdir -p docs/{architecture,phases,implementation,analysis,roadmaps,archive}
  
  # Results directories
  mkdir -p results/{epochs,validation,visualization}
  ```

- [ ] **Create config.py** (1 hour)
  ```bash
  cat > config.py << 'PYTHON_EOF'
  """
  DAE_HYPHAE_1 Centralized Configuration
  ======================================
  
  Single source of truth for paths, settings, and hyperparameters.
  """
  from pathlib import Path
  import os
  
  # Project root
  PROJECT_ROOT = Path(__file__).parent.resolve()
  
  # Core paths
  BUNDLE_PATH = PROJECT_ROOT / "Bundle"
  TSK_PATH = PROJECT_ROOT / "TSK"
  KNOWLEDGE_BASE = PROJECT_ROOT / "knowledge_base"
  TRAINING_PAIRS = KNOWLEDGE_BASE / "conversational_training_pairs.json"
  RESULTS_PATH = PROJECT_ROOT / "results"
  LOGS_PATH = PROJECT_ROOT / "logs"
  ORGANS_PATH = PROJECT_ROOT / "organs" / "modular"
  
  # Training defaults
  DEFAULT_EPOCHS = 5
  DEFAULT_PAIRS_PER_EPOCH = 30
  ENABLE_PHASE2 = True
  ENABLE_SALIENCE = True
  ENABLE_TSK_RECORDING = True
  
  # System defaults
  DEFAULT_BUNDLE_NAME = os.environ.get('DAE_BUNDLE_NAME', 'default_bundle')
  DEFAULT_LOG_LEVEL = 'INFO'
  
  # Validation thresholds
  MIN_EMISSION_CONFIDENCE = 0.50
  MIN_NEXUS_COUNT = 2
  MIN_ORGAN_COUNT = 11
  PYTHON_EOF
  ```

- [ ] **Create README files** (30 min)
  ```bash
  # Test README
  cat > tests/README_TESTS.md << 'EOF'
  # DAE_HYPHAE_1 Test Suite
  
  ## Organization
  - `unit/` - Fast, isolated unit tests
  - `integration/` - Multi-component integration tests
  - `validation/` - Manual validation scripts
  - `debug/` - Debugging utilities (archived)
  - `infrastructure/` - Infrastructure tests (DB, etc.)
  - `fixtures/` - Shared test data
  - `utilities/` - Test helpers
  
  ## Running Tests
  ```bash
  # All unit tests
  pytest tests/unit/
  
  # All integration tests
  pytest tests/integration/
  
  # Manual validation
  python tests/validation/phase2/validate_phase2_comprehensive.py
  ```
  EOF
  
  # Training README
  cat > training/README_TRAINING.md << 'EOF'
  # DAE_HYPHAE_1 Training Pipeline
  
  ## Directories
  - `arc/` - ARC challenge training (visual reasoning)
  - `conversational/` - Conversational epoch training (therapeutic text)
  - `configs/` - Training configuration files (YAML)
  
  ## Running Training
  ```bash
  # Baseline training (Epochs 1-5)
  python training/conversational/orchestrator.py \
      --config training/configs/baseline_config.yaml \
      --epochs 1-5
  ```
  EOF
  
  # Scripts README
  cat > scripts/README_SCRIPTS.md << 'EOF'
  # DAE_HYPHAE_1 Utility Scripts
  
  ## Quick Validation
  - `./scripts/quick_validate/check_system_health.sh` - System health check (30s)
  
  ## Profiling
  - Performance profiling utilities (future)
  
  ## Archive
  - One-off migration utilities (historical reference)
  EOF
  ```

- [ ] **Git checkpoint** (Commit directory structure)
  ```bash
  git add .
  git commit -m "Create organized directory structure for tests, training, docs, scripts"
  ```

---

### Phase 2: Move Test Files (2 hours)

- [ ] **Move Phase 2 unit tests** (20 min)
  ```bash
  mv test_phase2_multi_cycle.py tests/unit/phase2/
  mv test_phase2_meta_atom_phrases.py tests/unit/phase2/
  mv test_v0_unit.py tests/unit/phase2/
  ```

- [ ] **Move organ unit tests** (20 min)
  ```bash
  mv persona_layer/test_eo_polyvagal.py tests/unit/organs/
  mv persona_layer/test_polyvagal_detector.py tests/unit/organs/
  mv persona_layer/test_self_led_cascade.py tests/unit/organs/
  ```

- [ ] **Move learning/mechanism unit tests** (10 min)
  ```bash
  mv persona_layer/test_conversational_hebbian_learning.py tests/unit/learning/
  mv persona_layer/test_ofel.py tests/unit/mechanisms/
  ```

- [ ] **Move integration tests** (30 min)
  ```bash
  mv test_system_maturity_assessment.py tests/integration/test_system_maturity.py
  mv test_conversation_flow.py tests/integration/
  mv test_monitoring_integration.py tests/integration/
  mv persona_layer/test_11_organ_integration.py tests/integration/organs/
  mv test_v0_integration.py tests/integration/v0/
  mv test_salience_integration.py tests/integration/salience/
  mv test_salience_self_alignment.py tests/integration/salience/
  mv test_transduction_integration.py tests/integration/transduction/
  mv test_transduction_emission.py tests/integration/transduction/
  mv knowledge_base/test_mycelium_felt_integration.py tests/integration/memory/
  mv persona_layer/epoch_training/test_integrated_training.py tests/integration/training/
  ```

- [ ] **Move validation scripts** (10 min)
  ```bash
  mv test_phase1_emission_fix.py tests/validation/phase1/validate_phase1_emission.py
  mv test_phase2_comprehensive.py tests/validation/phase2/validate_phase2_comprehensive.py
  ```

- [ ] **Move debug/infrastructure tests** (10 min)
  ```bash
  mv test_appetition_debug.py tests/debug/debug_appetition.py
  mv test_meta_atom_diagnostic.py tests/debug/debug_meta_atom_diagnostic.py
  mv test_api_fixes.py tests/debug/debug_api_fixes.py
  mv knowledge_base/test_neo4j_connection.py tests/infrastructure/
  mv knowledge_base/test_neo4j_aura.py tests/infrastructure/
  ```

- [ ] **Update imports in moved files** (20 min)
  ```bash
  # Create and run import update script
  python3 << 'PYTHON_UPDATE'
  from pathlib import Path
  import re
  
  def update_imports(file_path):
      """Update sys.path.insert and relative imports."""
      content = file_path.read_text()
      
      # Replace hard-coded sys.path
      content = re.sub(
          r"sys\.path\.insert\(0, '[^']+'\)",
          "sys.path.insert(0, str(Path(__file__).parent.parent.parent))",
          content
      )
      
      # Add config import where needed
      if "TRAINING_PAIRS" in content or "BUNDLE_PATH" in content:
          if "from config import" not in content:
              content = "from config import PROJECT_ROOT, TRAINING_PAIRS, BUNDLE_PATH\n" + content
      
      file_path.write_text(content)
      print(f"Updated: {file_path}")
  
  # Update all moved test files
  for test_file in Path("tests").rglob("*.py"):
      if test_file.name != "__init__.py":
          update_imports(test_file)
  PYTHON_UPDATE
  ```

- [ ] **Git checkpoint** (Commit test reorganization)
  ```bash
  git add .
  git commit -m "Reorganize test files into tests/ directory structure"
  ```

---

## Session 2: Cleanup & Documentation (3 hours)

### Phase 3: Archive One-Off Utilities (1 hour)

- [ ] **Move Phase 1 migration utilities** (30 min)
  ```bash
  mv phase1_add_atom_activations.py scripts/archive/phase1_migration/
  mv fix_missing_load_methods.py scripts/archive/phase1_migration/
  mv validate_migration.py scripts/archive/phase1_migration/
  mv apply_fixes.py scripts/archive/phase1_migration/
  mv update_paths.py scripts/archive/phase1_migration/
  ```

- [ ] **Move Phase 2 migration utilities** (20 min)
  ```bash
  mv add_activate_methods.py scripts/archive/phase2_migration/
  mv add_meta_atoms_batch.py scripts/archive/phase2_migration/
  mv batch_add_remaining_meta_atoms.py scripts/archive/phase2_migration/
  ```

- [ ] **Remove duplicate training script** (10 min)
  ```bash
  # Compare first
  diff run_epochs_2_5_baseline.py run_epochs_2_5_baseline_fixed.py
  
  # If minimal differences, merge and delete
  rm run_epochs_2_5_baseline_fixed.py
  ```

- [ ] **Git checkpoint** (Commit utility archival)
  ```bash
  git add .
  git commit -m "Archive completed migration utilities"
  ```

---

### Phase 4: Organize Documentation (1.5 hours)

- [ ] **Identify core docs to keep in root** (10 min)
  ```bash
  # These stay in root:
  # - CLAUDE.md
  # - README.md
  # - STATUS.md
  # - SAFETY_ALIGNMENT_POLICY.md
  # - QUICK_CLONE_REFERENCE.md
  ```

- [ ] **Move phase documentation** (20 min)
  ```bash
  mv PHASE_*.md docs/phases/
  mv OPTION_*.md docs/phases/
  ```

- [ ] **Move architecture documentation** (20 min)
  ```bash
  mv *_ARCHITECTURE_*.md docs/architecture/
  mv *_DESIGN_*.md docs/architecture/
  mv MULTI_TIER_MEMORY_ARCHITECTURE.md docs/architecture/
  mv BACKPROPAGATION_SELF_FEEDING_LOOP_ARCHITECTURE.md docs/architecture/
  ```

- [ ] **Move analysis documentation** (20 min)
  ```bash
  mv *_ANALYSIS_*.md docs/analysis/
  mv *_INVESTIGATION_*.md docs/analysis/
  mv *_ASSESSMENT_*.md docs/analysis/
  mv SYSTEM_MATURITY_ASSESSMENT_REPORT_NOV12_2025.md docs/analysis/
  ```

- [ ] **Move implementation tracking** (10 min)
  ```bash
  mv *_IMPLEMENTATION_*.md docs/implementation/
  mv *_PROGRESS_*.md docs/implementation/
  mv *_STATUS.md docs/implementation/
  ```

- [ ] **Move roadmaps** (10 min)
  ```bash
  mv *_ROADMAP_*.md docs/roadmaps/
  mv *_STRATEGY_*.md docs/roadmaps/
  ```

- [ ] **Move completed/legacy docs to archive** (10 min)
  ```bash
  mv *_COMPLETE_*.md docs/archive/
  mv API_FIXES_COMPLETE_NOV12_2025.md docs/archive/
  mv IMIGRATION_STATUS.md docs/archive/  # Note: typo in filename
  ```

- [ ] **Git checkpoint** (Commit doc reorganization)
  ```bash
  git add .
  git commit -m "Organize documentation into docs/ directory structure"
  ```

---

### Phase 5: Quick Validation Script (30 min)

- [ ] **Create system health check script**
  ```bash
  cat > scripts/quick_validate/check_system_health.sh << 'BASH_EOF'
  #!/bin/bash
  # Quick system health check for DAE_HYPHAE_1
  
  echo "🔬 DAE_HYPHAE_1 System Health Check"
  echo "===================================="
  echo ""
  
  echo "📦 Checking Python environment..."
  python3 --version || { echo "❌ Python 3 not found"; exit 1; }
  echo ""
  
  echo "📁 Checking core directories..."
  [ -d "Bundle" ] && echo "✅ Bundle/" || echo "❌ Bundle/ missing"
  [ -d "TSK" ] && echo "✅ TSK/" || echo "❌ TSK/ missing"
  [ -d "organs" ] && echo "✅ organs/" || echo "❌ organs/ missing"
  [ -d "persona_layer" ] && echo "✅ persona_layer/" || echo "❌ persona_layer/ missing"
  [ -d "tests" ] && echo "✅ tests/" || echo "❌ tests/ missing"
  echo ""
  
  echo "🧬 Checking 11 organs load..."
  python3 << 'PYTHON_EOF'
  import sys
  sys.path.insert(0, '.')
  try:
      from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
      wrapper = ConversationalOrganismWrapper()
      organ_count = len([k for k in wrapper.organs.keys() if k != 'meta_atoms'])
      if organ_count >= 11:
          print(f"✅ Loaded {organ_count} organs")
      else:
          print(f"⚠️  Only {organ_count} organs loaded (expected 11)")
  except Exception as e:
      print(f"❌ Organ loading failed: {e}")
  PYTHON_EOF
  echo ""
  
  echo "✅ System health check complete!"
  BASH_EOF
  
  chmod +x scripts/quick_validate/check_system_health.sh
  ```

- [ ] **Test health check script**
  ```bash
  ./scripts/quick_validate/check_system_health.sh
  ```

---

## Session 3: Training & Validation (3.5 hours)

### Phase 6: Configuration System (1 hour)

- [ ] **Update key scripts to use config.py** (30 min)
  ```bash
  # Update run_baseline_training.py
  # Update test_phase2_comprehensive.py (now in tests/validation/phase2/)
  # Update test_system_maturity.py (now in tests/integration/)
  
  # Example update:
  # BEFORE:
  # sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')
  # TRAINING_PAIRS_PATH = "knowledge_base/conversational_training_pairs.json"
  #
  # AFTER:
  # from config import PROJECT_ROOT, TRAINING_PAIRS, ENABLE_PHASE2
  ```

- [ ] **Test updated scripts** (30 min)
  ```bash
  # Test a few key scripts with new config
  python tests/validation/phase2/validate_phase2_comprehensive.py
  python tests/integration/test_system_maturity.py
  ```

---

### Phase 7: Training Orchestrator (1.5 hours)

- [ ] **Create baseline configuration** (30 min)
  ```bash
  cat > training/configs/baseline_config.yaml << 'YAML_EOF'
  metadata:
    name: "Baseline Epochs 1-5"
    description: "Establish pre-governance baseline performance"
    
  training:
    epochs: 5
    pairs_per_epoch: 30
    training_pairs_path: "knowledge_base/conversational_training_pairs.json"
    
  system:
    enable_phase2: true
    enable_salience: true
    enable_tsk_recording: true
    
  checkpointing:
    checkpoint_dir: "results/epochs"
    save_interval: 1
    
  monitoring:
    health_checks: true
    real_time_monitoring: true
    log_level: "INFO"
    
  output:
    results_dir: "results/epochs"
    visualization_dir: "results/visualization"
  YAML_EOF
  ```

- [ ] **Create training orchestrator stub** (1 hour)
  ```bash
  cat > training/conversational/orchestrator.py << 'PYTHON_EOF'
  """
  Unified Training Orchestrator for DAE_HYPHAE_1 Conversational System
  ====================================================================
  
  Single entry point for all conversational epoch training.
  """
  import sys
  from pathlib import Path
  import yaml
  import argparse
  
  sys.path.insert(0, str(Path(__file__).parent.parent.parent))
  from config import PROJECT_ROOT, TRAINING_PAIRS
  
  def load_config(config_path):
      """Load training configuration from YAML."""
      with open(config_path, 'r') as f:
          return yaml.safe_load(f)
  
  def run_orchestrator(config_path, epochs_str):
      """
      Main orchestrator entry point.
      
      Args:
          config_path: Path to YAML configuration
          epochs_str: Epoch range (e.g., "1-5" or "3")
      """
      print(f"🌀 DAE_HYPHAE_1 Training Orchestrator")
      print("="*60)
      print()
      
      # Load config
      config = load_config(config_path)
      print(f"📋 Config: {config['metadata']['name']}")
      print()
      
      # Parse epoch range
      if '-' in epochs_str:
          start, end = map(int, epochs_str.split('-'))
      else:
          start = end = int(epochs_str)
      
      print(f"🎯 Running Epochs {start} through {end}")
      print()
      
      # TODO: Implement full orchestration
      # For now, delegate to existing run_baseline_training.py
      print("⚠️  Full orchestrator not yet implemented.")
      print("   Using existing run_baseline_training.py for now.")
      print()
      
      import subprocess
      subprocess.run([
          sys.executable,
          str(PROJECT_ROOT / "run_baseline_training.py")
      ])
  
  if __name__ == "__main__":
      parser = argparse.ArgumentParser(description="DAE_HYPHAE_1 Training Orchestrator")
      parser.add_argument("--config", required=True, help="Path to config YAML")
      parser.add_argument("--epochs", required=True, help="Epoch range (e.g., '1-5')")
      
      args = parser.parse_args()
      run_orchestrator(args.config, args.epochs)
  PYTHON_EOF
  ```

- [ ] **Git checkpoint** (Commit orchestrator)
  ```bash
  git add .
  git commit -m "Add training orchestrator and configuration system"
  ```

---

### Phase 8: Final Validation (1 hour)

- [ ] **Run system health check** (5 min)
  ```bash
  ./scripts/quick_validate/check_system_health.sh
  ```

- [ ] **Run key unit tests** (15 min)
  ```bash
  pytest tests/unit/phase2/ -v
  pytest tests/unit/organs/ -v
  ```

- [ ] **Run key integration tests** (20 min)
  ```bash
  pytest tests/integration/v0/ -v
  pytest tests/integration/salience/ -v
  ```

- [ ] **Run manual validation** (10 min)
  ```bash
  python tests/validation/phase2/validate_phase2_comprehensive.py
  ```

- [ ] **Test training orchestrator** (10 min)
  ```bash
  python training/conversational/orchestrator.py \
      --config training/configs/baseline_config.yaml \
      --epochs 1
  ```

- [ ] **Final git checkpoint** (Commit completion)
  ```bash
  git add .
  git commit -m "Complete test infrastructure reorganization - validation passing"
  ```

---

## Post-Reorganization Checklist

After completing all phases, verify:

- [ ] Root directory has ≤ 10 Python files
- [ ] Root directory has ≤ 10 .md files
- [ ] `/tests/` contains 25+ organized test files
- [ ] `/docs/` contains 100+ organized documentation files
- [ ] `/scripts/archive/` contains all one-off utilities
- [ ] `config.py` exists and is imported by key scripts
- [ ] System health check runs in < 30 seconds
- [ ] All moved tests still pass
- [ ] Git history is clean with descriptive commits

---

## Success Metrics

**Target Reductions:**
- Root Python files: 30 → 7 (77% reduction)
- Root .md files: 109 → 5 (95% reduction)
- Test organization: 1 → 28+ files in `/tests/`

**Target Improvements:**
- ✅ Centralized configuration
- ✅ Quick system validation (< 30s)
- ✅ Clear test hierarchy
- ✅ Training orchestrator foundation
- ✅ Documentation organization

---

## Troubleshooting

**If tests fail after moving:**
1. Check import paths in moved files
2. Ensure `sys.path.insert(0, str(Path(__file__).parent.parent.parent))`
3. Verify `config.py` is imported correctly
4. Run with `-v` flag for detailed errors

**If orchestrator fails:**
1. Check YAML config syntax
2. Ensure `pyyaml` is installed: `pip install pyyaml`
3. Verify config paths are correct

**If health check fails:**
1. Ensure you're in project root: `cd /Users/daedalea/Desktop/DAE_HYPHAE_1`
2. Check organ files exist in `organs/modular/`
3. Verify Bundle/ and TSK/ directories exist

---

## Notes

- Take breaks between phases
- Git commit after each major phase
- Test incrementally (don't move everything at once)
- Keep backup before starting: `git stash` or `git branch backup-before-reorg`

---

**Ready to begin!** Start with Session 1 when ready.
