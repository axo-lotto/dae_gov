# Quick Clone Reference - DAE_HYPHAE_0 Domain Adaptation

## One-Time Setup (for each new domain)

### 1. Clone the Template
```bash
cd /Users/daedalea/Desktop
cp -r DAE_HYPHAE_0 DAE_SUDOKU_0    # For Sudoku
cp -r DAE_HYPHAE_0 DAE_THERAPEUTIC_0  # For Therapy
```

### 2. Update Paths in Clone
```bash
cd /new/clone
# Update all references from DAE_HYPHAE_0 to new path
sed -i '' 's|/Users/daedalea/Desktop/DAE_HYPHAE_0|/Users/daedalea/Desktop/DAE_SUDOKU_0|g' \
  core/*.py training/*.py *.py run_training.sh

# Update data path references (TSK → data already done in migration)
```

### 3. Create Domain-Specific Data Loader
```bash
# Copy template, customize for your domain
cat > training/domain_data_loader.py << 'PYEOF'
import json
import numpy as np
from pathlib import Path

def load_sudoku_task(task_path):
    """Load Sudoku puzzle from domain format."""
    with open(task_path) as f:
        task_data = json.load(f)
    
    # Adapt to your domain structure
    train_pairs = task_data['train']
    test_pairs = task_data['test']
    
    return train_pairs, test_pairs

def load_all_tasks(data_dir):
    """Load all tasks from domain directory."""
    tasks = []
    for task_file in Path(data_dir).glob('*.json'):
        task_id = task_file.stem
        train_pairs, test_pairs = load_sudoku_task(task_file)
        tasks.append({
            'id': task_id,
            'train': train_pairs,
            'test': test_pairs
        })
    return tasks
PYEOF
```

### 4. Create Domain-Specific Training Script
```bash
# Copy and modify training script
cp training/train_arc1.py training/train_sudoku.py

# Edit train_sudoku.py:
# - Replace arc_path with sudoku_data_path
# - Replace arc data loading with domain data loader
# - Update metrics if needed (must match domain evaluation)
```

### 5. Reset Organism State
```bash
# Start fresh for new domain
python3 << 'PYEOF'
import json

# Reset organism state for new domain
state = {
    "global_confidence": 0.5,
    "total_successes": 0,
    "total_attempts": 0,
    "success_rate": 0.0,
    "rewards": {
        "micro": {},
        "meso": {},
        "macro": {}
    },
    "knowledge": {
        "value_mappings": {},
        "family_patterns": {},
        "spatial_transforms": {}
    },
    "sessions": [],
    "last_updated": "2025-11-07T00:00:00"
}

with open('data/organism_state.json', 'w') as f:
    json.dump(state, f, indent=2)

print("✅ Organism state reset for new domain")
PYEOF
```

### 6. Test Migration
```bash
python3 validate_migration.py
# Should run 5 tasks successfully with new domain format
```

## Core Files That MUST Change Per Domain

| File | Change Type | Impact |
|------|-------------|--------|
| `training/train_domain.py` | Full rewrite | Data loading, task iteration |
| `training/data_loader.py` | New file | Domain-specific format handling |
| `core/complete_organic_system.py` | Path update only | Base paths configuration |
| `data/organism_state.json` | Reset | Fresh learning for domain |

## Core Files That DON'T Need Changing

| File | Reason |
|------|--------|
| `core/organic_transformation_learner.py` | Generic learning engine |
| `core/persistent_organism_state.py` | Fractal reward system (domain-independent) |
| `core/tsk_log_memory.py` | Pattern storage (generic) |
| `transductive/*.py` | Entity system (universal) |
| `organs/` | Organ implementations (generic) |

## Configuration Parameters by Domain

### Sudoku-Specific Config
```python
# sudoku_config.py (new file)
SUDOKU_BOARD_SIZE = 9
CELL_ACCURACY_THRESHOLD = 0.99  # Store only near-perfect solutions
MAX_DIFFICULTY = 'expert'
CONVERGENCE_CYCLES = 2  # Sudoku converges faster than ARC
FAMILY_THRESHOLD = 0.85  # Organic family formation threshold
```

### Therapeutic AI-Specific Config
```python
# therapeutic_config.py (new file)
CONVERSATION_MAX_TURNS = 20
EVALUATION_METRIC = 'human_rating'  # Not ground-truth based
HUMAN_EVALUATOR_POOL = 3  # Multiple evaluators for consensus
FRACTAL_REWARD_SCALING = 1.0  # Adjust for conversation context
NO_GROUND_TRUTH = True  # No test output available
```

## Performance Expectations

| Domain | Baseline | Expected After 1 Epoch | Expected After 5 Epochs |
|--------|----------|------------------------|--------------------------|
| Sudoku | TBD | 35-45% | 50-65% |
| Therapeutic | TBD | 20-30% | 30-45% |

## Validation Checklist

- [ ] Clone completed
- [ ] Paths updated (sed command)
- [ ] Data loader created and tested
- [ ] Training script adapted
- [ ] Organism state reset
- [ ] First 5 tasks run successfully
- [ ] Metrics calculated correctly
- [ ] JSON databases populated

## Emergency: Revert to Template

If something breaks:
```bash
cd /Users/daedalea/Desktop
rm -rf DAE_BROKEN_0
cp -r DAE_HYPHAE_0 DAE_BROKEN_0  # Fresh copy
# Then re-apply changes carefully
```

## File Size Expectations After Clone

```
DAE_SUDOKU_0/
├── core/         - 2.4 KB (no change)
├── organs/       - ~350 B (no change)
├── transductive/ - 4.6 KB (no change)
├── training/     - 30 KB (+ domain_loader.py)
├── data/         - 697 KB (reset/fresh)
├── sudoku_data/  - YOUR DOMAIN SIZE
└── Other files   - 100 KB
Total: 7.7 MB + your domain data
```

## Debugging Common Issues

### Issue: "ModuleNotFoundError: No module named 'core'"
**Solution:** Update PYTHONPATH in training script
```python
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_SUDOKU_0')
```

### Issue: "TaskError: task_id not found"
**Solution:** Check data loader returns correct task format
```python
# Should return: (training_pairs, test_pairs)
# Where each pair is: (input_array, output_array)
```

### Issue: "accuracy is NaN"
**Solution:** Domain metrics might need custom evaluation function
```python
# Implement domain-specific accuracy in:
# core/complete_organic_system.py calculate_accuracy()
```

## Next Steps After Clone Works

1. Run 10 tasks to verify learning
2. Analyze organism_state.json for family formation
3. Check hebbian_memory.json for pattern storage
4. Run full training on domain dataset
5. Compare metrics against baseline

## Important Reminders

✓ Keep DAE_HYPHAE_0 as master template (don't modify)
✓ Each domain clone is independent (modify freely)
✓ All 6 JSON databases will be populated during training
✓ Transductive system is universal (no changes needed)
✓ Core algorithms need no modification (just data loading)

---

**Clone time: 2 minutes**  
**Setup time: 30 minutes**  
**First run: 1 hour**  
**Full training: 3-5 hours per domain**

