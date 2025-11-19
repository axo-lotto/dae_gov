# persona_layer/ Organization Plan

## Current State
- 59 Python files in root
- 34 JSON files in root
- 9 existing subdirectories

## CRITICAL: Import Safety
**DO NOT MOVE** Python files that are imported by other modules!
We will ONLY organize:
1. JSON configuration/data files
2. Test files (move to /tests/)
3. Backup files (move to backups/)

## Proposed Organization

### 1. JSON Configuration Files → `/persona_layer/config/`

Create subdirectories:
```
persona_layer/config/
├── atoms/          # Semantic atoms & meta-atoms
├── templates/      # LLM templates & prompts
├── transduction/   # Transduction phrases & rules
├── symbols/        # Emoji, glyphs, attractors
└── lures/          # Lure prototypes
```

**Safe moves (NO Python imports depend on exact paths):**
- coherent_attractors.json → config/symbols/
- emoji_felt_library.json → config/symbols/
- humor_templates.json → config/templates/
- llm_augmentation_prompts.json → config/templates/
- personality_templates.json → config/templates/ (if exists)
- relationship_templates.json → config/templates/ (if exists)
- response_style_templates.json → config/templates/ (if exists)
- small_talk_templates.json → config/templates/ (if exists)
- lure_prototypes.json → config/lures/
- meta_atom_activation_rules.json → config/atoms/
- meta_atom_phrase_library.json → config/atoms/
- transduction_mechanism_phrases.json → config/transduction/
- transduction_mechanism_phrases_with_lure_tags.json → config/transduction/

### 2. State/Runtime Files → `/persona_layer/state/`

Create subdirectories:
```
persona_layer/state/
├── active/         # Active runtime state
└── backups/        # Backup files
```

**Safe moves:**
- conversational_hebbian_memory.json → state/active/
- organ_confidence.json → state/active/
- organic_families.json → state/active/
- feedback.json → state/active/
- llm_activation_cache_local.json → state/active/

- conversational_hebbian_memory_backup_*.json → state/backups/
- organic_families_backup_*.json → state/backups/

### 3. Test Files → `/tests/unit/persona_layer/`

**Safe moves (test files don't get imported):**
- All test_*.py files in persona_layer/ → tests/unit/persona_layer/

### 4. Python Files - LEAVE IN PLACE

**DO NOT MOVE** - These are imported by other modules:
- All .py files stay in persona_layer/ root
- Imports like `from persona_layer.conversational_organism_wrapper import...` must continue to work

## Risk Assessment

✅ **ZERO RISK:**
- Moving JSON config files (paths can be updated in config.py)
- Moving backup files
- Moving test files

⚠️ **HIGH RISK - DO NOT DO:**
- Moving any .py files (would break imports across the codebase)

## Implementation Steps

1. Create subdirectory structure
2. Move JSON config files to config/ subdirectories
3. Move state/backup files to state/ subdirectories
4. Move test files to tests/
5. Update config.py to point to new JSON paths
6. Test all imports still work
7. Commit

## Expected Outcome

persona_layer/ root will go from:
- 59 .py files + 34 .json files = 93 files
To:
- 59 .py files only
- All JSON organized in config/ and state/
- Clean, navigable structure
- Zero broken imports
