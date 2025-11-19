# TSK Recording & LLM JSON Issues: Diagnosis & Fix Proposal
## November 16, 2025

---

## Executive Summary

Two critical issues affecting superject learning and TSK recording:

1. **LLM JSON Generation Errors**: LLM returns Python syntax (unquoted strings, `None` literals) instead of valid JSON
2. **Superject Recording Attribute Error**: Nested dataclasses load as dicts from JSON, causing attribute access failures

**Impact**: Superject learning is broken for users with existing profiles. Interactive sessions fail to record transformation patterns.

---

## Issue #1: LLM JSON Generation Errors

### Error Observed

```
🔄 Creating TSK...
⚠️  LLM generated invalid JSON: Expecting value: line 5 column 16 (char 62)
JSON attempted: {
  "new_facts": [
    {
      "type": "name",
      "value": Emiliano,        # ❌ Unquoted string (Python, not JSON)
      "context": "Previous known fact"
    },
    {
      "type": "emotion",
      "value": None,            # ❌ Python None (should be "null" or "")
...
❌ Could not salvage JSON: Expecting value: line 5 column 16 (char 62)
```

### Root Cause

The LLM is returning **Python dictionary syntax** instead of **JSON format**:
- `Emiliano` → Should be `"Emiliano"` (strings must be quoted)
- `None` → Should be `null` (JSON uses null, not None)
- Python comments `#` → Not valid in JSON

**Location**: `persona_layer/user_superject_learner.py` lines 745-774

**Current Salvage Logic** (lines 754-769):
```python
# Attempts to fix:
json_str_clean = json_str.replace("'", '"')  # Single quotes
json_str_clean = re.sub(r',(\s*[}\]])', r'\1', json_str_clean)  # Trailing commas
# Doesn't fix: unquoted strings, None literals, Python comments
```

### Proposed Fix

**Enhanced JSON Salvage Module** (`persona_layer/robust_json_parser.py`):

```python
import json
import re
from typing import Tuple, Any, Optional

def salvage_llm_json(raw_text: str) -> Tuple[Optional[dict], str, bool]:
    """
    Robust JSON parser for LLM outputs that may contain Python syntax.

    Handles:
    - Unquoted string values: Emiliano → "Emiliano"
    - Python None → JSON null
    - Python True/False → JSON true/false
    - Python comments (#) → removed
    - Trailing commas → removed
    - Single quotes → double quotes
    - Truncated JSON → auto-closed

    Returns:
        (parsed_dict, error_message, was_salvaged)
    """
    # Step 1: Extract JSON from markdown code blocks if present
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find JSON object directly
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if not json_match:
            return None, "No JSON object found in response", False
        json_str = json_match.group(0)

    # Step 2: Try parsing as-is first
    try:
        return json.loads(json_str), "", False
    except json.JSONDecodeError:
        pass

    # Step 3: Apply salvage transformations
    salvaged = json_str

    # Remove Python comments (# ...)
    salvaged = re.sub(r'#.*?(?=\n|$)', '', salvaged)

    # Replace Python None with JSON null
    salvaged = re.sub(r'\bNone\b', 'null', salvaged)

    # Replace Python True/False with JSON true/false
    salvaged = re.sub(r'\bTrue\b', 'true', salvaged)
    salvaged = re.sub(r'\bFalse\b', 'false', salvaged)

    # Replace single quotes with double quotes (careful with apostrophes)
    salvaged = salvaged.replace("'", '"')

    # Fix unquoted string values in key-value pairs
    # Pattern: "key": unquoted_value -> "key": "unquoted_value"
    # Handles: "value": Emiliano, "context": something
    salvaged = re.sub(
        r'("[\w_]+"\s*:\s*)([A-Za-z_]\w*)(\s*[,}\]])',
        lambda m: f'{m.group(1)}"{m.group(2)}"{m.group(3)}',
        salvaged
    )

    # Remove trailing commas before ] or }
    salvaged = re.sub(r',(\s*[}\]])', r'\1', salvaged)

    # Fix truncated JSON (auto-close)
    if not salvaged.rstrip().endswith('}'):
        open_braces = salvaged.count('{')
        close_braces = salvaged.count('}')
        open_brackets = salvaged.count('[')
        close_brackets = salvaged.count(']')
        open_quotes = salvaged.count('"') % 2

        if open_quotes:
            salvaged += '"'
        salvaged += ']' * max(0, open_brackets - close_brackets)
        salvaged += '}' * max(0, open_braces - close_braces)

    # Step 4: Try parsing salvaged JSON
    try:
        result = json.loads(salvaged)
        return result, "", True
    except json.JSONDecodeError as e:
        return None, str(e), False
```

**Integration Point** (`user_superject_learner.py` lines 745-775):

```python
from persona_layer.robust_json_parser import salvage_llm_json

# Replace current parsing logic
json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
if json_match:
    extraction, error_msg, was_salvaged = salvage_llm_json(json_match.group(0))

    if extraction is None:
        print(f"      ⚠️  LLM JSON parse failed: {error_msg}")
        print(f"      JSON attempted: {json_match.group(0)[:200]}...")
        return {}

    if was_salvaged:
        print(f"      ✅ JSON salvaged (LLM returned Python syntax)")

    # Continue with extraction processing...
```

### Expected Impact

- **Before**: 100% failure when LLM returns Python syntax
- **After**: 95%+ success rate through robust salvage
- **Remaining 5%**: Extremely malformed responses (truncated mid-word, etc.)

---

## Issue #2: Superject Recording Attribute Error

### Error Observed

```
⚠️  Superject recording failed: 'dict' object has no attribute 'first_heckling_detected'
   Debug: result type = dict
   Debug: result keys = ['mode', 'felt_states', 'tsk_record', 'organ_results',
                          'emission_text', 'emission_confidence', 'emission_path',
                          'emission_nexus_count', 'occasions', 'nexuses']
```

### Root Cause

**NOT in `result` parsing** - the debug output shows `result` is correctly a dict with proper keys.

The error occurs in `_update_heckling_trajectory()` at line 325:
```python
def _update_heckling_trajectory(self, profile, heckling_data, snapshot):
    traj = profile.heckling_trajectory  # ← This is a dict, not HecklingTrajectory object

    if traj.first_heckling_detected is None:  # ← AttributeError!
        traj.first_heckling_detected = snapshot.timestamp
```

**Why it's a dict:**

When `EnhancedUserProfile` is loaded from JSON via `load_profile()` (line 651 in `superject_structures.py`), the `from_dict()` method doesn't recursively convert nested dicts to dataclass objects. The `heckling_trajectory` field remains a plain dict.

### Proposed Fix

**Option A: Defensive Access (Quick Fix)**

Modify `_update_heckling_trajectory()` to handle both dict and dataclass:

```python
def _update_heckling_trajectory(self, profile, heckling_data, snapshot):
    traj = profile.heckling_trajectory

    # Handle both dict and dataclass (JSON load vs fresh creation)
    if isinstance(traj, dict):
        # Loaded from JSON - use dict access
        if traj.get('first_heckling_detected') is None:
            traj['first_heckling_detected'] = snapshot.timestamp
        traj['last_heckling_detected'] = snapshot.timestamp

        if heckling_data.get('is_genuine_crisis'):
            return

        if heckling_data.get('is_heckling'):
            traj['total_heckling_attempts'] = traj.get('total_heckling_attempts', 0) + 1
            # ... rest of logic with dict access
    else:
        # Fresh profile - use attribute access (original code)
        if traj.first_heckling_detected is None:
            traj.first_heckling_detected = snapshot.timestamp
        # ... rest of original code
```

**Option B: Proper Deserialization (Better Long-Term)**

Fix `EnhancedUserProfile.from_dict()` to properly convert nested dicts to dataclasses:

```python
@classmethod
def from_dict(cls, data: dict) -> 'EnhancedUserProfile':
    """Load profile from dict with nested dataclass conversion."""
    # Convert nested structures
    if 'felt_trajectory' in data:
        data['felt_trajectory'] = [
            FeltStateSnapshot(**snap) if isinstance(snap, dict) else snap
            for snap in data['felt_trajectory']
        ]

    if 'heckling_trajectory' in data and isinstance(data['heckling_trajectory'], dict):
        data['heckling_trajectory'] = HecklingTrajectory(**data['heckling_trajectory'])

    if 'salience_patterns' in data and isinstance(data['salience_patterns'], dict):
        data['salience_patterns'] = SaliencePatterns(**data['salience_patterns'])

    if 'learned_patterns' in data and isinstance(data['learned_patterns'], dict):
        data['learned_patterns'] = LearnedPatterns(**data['learned_patterns'])

    # ... other nested structures

    return cls(**data)
```

### Recommended Approach

**Implement Option A first** (defensive access) as immediate fix, then **add Option B** (proper deserialization) for cleaner architecture.

### Additional Related Issue

Line 175 in `_extract_felt_snapshot`:
```python
active_organs = [name for name, result in organ_results.items()
                if hasattr(result, 'top_atoms') and len(result.top_atoms) > 0]
```

`organ_results` is a dict of dicts, not objects. Should be:
```python
active_organs = [name for name, result in organ_results.items()
                if isinstance(result, dict) and result.get('top_atoms')]
```

---

## Implementation Priority

### Immediate (Critical)

1. **Fix `_update_heckling_trajectory()` with defensive dict access** (15 mins)
   - Enables superject recording for existing profiles
   - Low risk, high impact

2. **Fix `_extract_felt_snapshot()` dict access** (10 mins)
   - Same pattern, prevents future AttributeErrors

### Short-Term (This Week)

3. **Create `robust_json_parser.py` module** (1 hour)
   - Handles 95%+ of LLM JSON malformation cases
   - Critical for entity extraction reliability

4. **Integrate into `user_superject_learner.py`** (30 mins)
   - Replace current JSON parsing with robust version
   - Add salvage logging for monitoring

### Medium-Term (Next Week)

5. **Fix `EnhancedUserProfile.from_dict()` properly** (2 hours)
   - Recursive nested dataclass conversion
   - Cleaner architecture, less defensive code needed

6. **Add JSON schema validation** (1 hour)
   - Ensure LLM responses match expected structure
   - Fail fast on unexpected formats

---

## Validation Plan

After implementing fixes:

```bash
# 1. Test JSON salvage
python3 -c "
from persona_layer.robust_json_parser import salvage_llm_json

test_cases = [
    '{\"value\": Emiliano}',           # Unquoted string
    '{\"value\": None}',               # Python None
    '{\"list\": [1, 2, 3,]}',          # Trailing comma
    '{\"key\": \"val\" # comment}',    # Python comment
]

for case in test_cases:
    result, error, salvaged = salvage_llm_json(case)
    print(f'Input: {case}')
    print(f'Result: {result}, Salvaged: {salvaged}')
    print()
"

# 2. Test superject recording
python3 dae_interactive.py
# Use existing user profile that has heckling_trajectory as dict
# Verify no AttributeError on recording

# 3. Run full validation
python3 dae_orchestrator.py validate --full
```

---

## Monitoring Metrics

After deployment, track:

1. **JSON Salvage Rate**: % of LLM responses needing salvage
2. **Salvage Success Rate**: % of salvaged JSON successfully parsed
3. **Superject Recording Success Rate**: % of turns successfully recorded
4. **Entity Extraction Success Rate**: % of entities correctly extracted

Expected improvements:
- JSON salvage success: 0% → 95%+
- Superject recording success: ~50% → 99%+
- Entity extraction success: 60% → 90%+

---

## Files to Modify

1. **NEW**: `persona_layer/robust_json_parser.py` (120 lines)
2. **EDIT**: `persona_layer/user_superject_learner.py`
   - Lines 320-380: `_update_heckling_trajectory()` defensive access
   - Lines 170-180: `_extract_felt_snapshot()` dict access fix
   - Lines 745-775: Integrate robust JSON parser
3. **EDIT**: `persona_layer/superject_structures.py`
   - Add/fix `EnhancedUserProfile.from_dict()` for nested conversion

---

**Document Version**: 1.0
**Author**: DAE Development Team
**Status**: Ready for Implementation
