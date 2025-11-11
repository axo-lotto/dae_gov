# DEPRECATED: Keyword-Based Organ Configs

**Date Deprecated:** November 10, 2025
**Reason:** Architectural course correction toward embedding-based organic learning

## Files Deprecated

- `eo_text_config.py` - Polyvagal keyword configuration
- `bond_text_config.py` - IFS parts keyword configuration

## Why Deprecated?

These files implemented **rigid keyword-based** detection that violated core DAE-GOV architectural principles:

### ❌ What Was Wrong:

1. **Hard-coded keyword lists** - Exhaustive lists like:
   ```python
   'ventral': {
       'keywords': ['connected', 'safe', 'curious', ...]  # 67 hard-coded keywords
   }
   ```

2. **No organic learning** - Keywords couldn't expand through Hebbian memory

3. **Violated open-ended intelligence** - Registries were closed, not extensible

4. **Ignored existing organs** - Tried to replace instead of extend

5. **No BAGUA modulation** - Rigid classification without creative exploration

### ✅ What Replaced Them:

**`polyvagal_detector.py`** - Embedding-based polyvagal detection

**Architecture:**
- **SEED** from I Ching corpus + initial keywords (not exhaustive)
- **LEARN** through 384-dim embedding similarity
- **EXPAND** via Hebbian memory over epochs
- **BAGUA-modulate** for lateral blending (Lake Joy 0.718)
- **Entity-native** propositions (felt affordances → mature patterns)

**Key Principle:**
> Keywords are SEEDS, not EXHAUSTIVE LISTS. Let embedding space learn organically.

## Migration Path

If you were using the deprecated configs:

### Old (WRONG):
```python
from persona_layer.eo_text_config import EOPolyvagalDetector

detector = EOPolyvagalDetector()
output = detector.prehend_text("I feel safe.")
# Hard-coded keyword matching, no learning
```

### New (RIGHT):
```python
from persona_layer.polyvagal_detector import PolyvagalDetector

detector = PolyvagalDetector()
detection = detector.detect_polyvagal_state("I feel safe.")
# Embedding similarity, learns over epochs
```

## Timeline

- **Nov 10, 18:15-18:17** - Keyword configs created (initial implementation)
- **Nov 10, 18:20** - User feedback: "Wait! are you leveraging from existing organs?"
- **Nov 10, 18:31** - Polyvagal detector created (embedding-based)
- **Nov 10, 18:35** - Keyword configs deprecated

## Lesson Learned

**Always consult architecture before implementing.** The course correction saved us from:
- Weeks of maintaining rigid templates
- Inability to learn from conversational epochs
- Violation of core organic intelligence principles
- Redundant code with existing embedding-based organs

**Process philosophy as computational substrate requires fluid, learning-based approaches, not rigid templates.**

---

**Status:** DO NOT USE THESE FILES
**Replacement:** `polyvagal_detector.py` (embedding-based)
**Future:** These files may be deleted after Phase 1.3 validation
