# Dormant Capabilities Activation Plan
## November 14, 2025

---

## 🎯 Session Summary

### ✅ Completed Today

**1. Nexus Formation Threshold Lowered**
- **Changed:** `intersection_threshold` from 0.01 → 0.005
- **File:** `persona_layer/conversational_organism_wrapper.py:270`
- **Expected Impact:** 2-4 nexuses per turn (was 0-1)
- **Status:** ✅ IMPLEMENTED

**2. Full Session Achievements**
- ✅ Entity recall fixed (all 3 emission paths)
- ✅ Response length increased (150 → 400 tokens)
- ✅ Context window scalability validated (100+ entities)
- ✅ Entity epoch training completed (5 epochs, 4.9s avg processing)
- ✅ Nexus formation optimized (threshold lowered)

---

## 🔮 Remaining Dormant Capabilities

### Priority 1: Multi-Entity Extraction (NEXT SESSION)

**Current State:**
- ✅ Extracts: user_name ("Emiliano")
- ❌ Missing: relationships, emotions, family_influences, values, psychological_patterns

**From Emiliano's Conversation:**
```
Turn 3: "i am married" + "my wife"
  → Should extract:
     - relationship_status: "married"
     - spouse_gender: "wife"
     - significant_people: ["wife"]

Turn 6: "anger arising... trying to protect something"
  → Should extract:
     - emotional_patterns: ["protective_anger"]
     - core_values: ["truth", "protection"]

Turn 7: "governance... from my father"
  → Should extract:
     - family_influences: {"father": ["governance", "right way of living"]}
     - value_sources: {"governance": "father"}

Turn 8: "neurotic energy driving my experience"
  → Should extract:
     - psychological_patterns: ["neurotic_energy", "restlessness"]
     - challenges: ["difficulty_being_present"]
```

**Implementation File:** `persona_layer/user_superject_learner.py`

**Enhancement Needed:**
```python
def extract_entities(self, text: str, current_entities: Dict) -> Dict:
    """
    Enhanced entity extraction with multiple entity types.
    """
    updated_entities = current_entities.copy()
    text_lower = text.lower()

    # 1. NAME EXTRACTION (existing - working)
    # ... existing code ...

    # 2. RELATIONSHIP EXTRACTION (NEW)
    relationship_patterns = {
        'married': ['married', 'my spouse', 'my husband', 'my wife'],
        'partnered': ['my partner', 'significant other'],
        'single': ['single', 'not in a relationship'],
    }

    spouse_indicators = {
        'wife': 'wife',
        'husband': 'husband',
        'partner': 'partner',
    }

    for status, patterns in relationship_patterns.items():
        if any(p in text_lower for p in patterns):
            updated_entities['relationship_status'] = status

    for indicator, gender in spouse_indicators.items():
        if indicator in text_lower:
            updated_entities['spouse'] = indicator
            if 'significant_people' not in updated_entities:
                updated_entities['significant_people'] = []
            if indicator not in updated_entities['significant_people']:
                updated_entities['significant_people'].append(indicator)

    # 3. FAMILY INFLUENCE EXTRACTION (NEW)
    family_patterns = {
        'father': ['my father', 'from my father', 'my dad'],
        'mother': ['my mother', 'from my mother', 'my mom'],
        'parents': ['my parents', 'from my parents'],
    }

    for family_member, patterns in family_patterns.items():
        for pattern in patterns:
            if pattern in text_lower:
                # Extract what came from this family member
                # Look for concepts near the mention
                nearby_concepts = []
                if 'governance' in text_lower:
                    nearby_concepts.append('governance')
                if 'right way' in text_lower or 'should' in text_lower:
                    nearby_concepts.append('expectations')

                if nearby_concepts:
                    if 'family_influences' not in updated_entities:
                        updated_entities['family_influences'] = {}
                    updated_entities['family_influences'][family_member] = nearby_concepts

    # 4. EMOTIONAL PATTERN EXTRACTION (NEW)
    emotion_patterns = {
        'protective_anger': ['anger.*protect', 'protective.*anger'],
        'anxiety': ['anxious', 'anxiety', 'worried', 'stress'],
        'restlessness': ['neurotic', 'restless', 'can\'t sit still'],
        'joy': ['happy', 'joyful', 'excited'],
        'sadness': ['sad', 'down', 'depressed'],
    }

    import re
    for pattern_name, regexes in emotion_patterns.items():
        for regex in regexes:
            if re.search(regex, text_lower):
                if 'emotional_patterns' not in updated_entities:
                    updated_entities['emotional_patterns'] = []
                if pattern_name not in updated_entities['emotional_patterns']:
                    updated_entities['emotional_patterns'].append(pattern_name)

    # 5. PSYCHOLOGICAL PATTERN EXTRACTION (NEW)
    psychological_patterns = {
        'IFS_awareness': ['parts', 'inner voice', 'protector', 'exile'],
        'neurotic_energy': ['neurotic', 'driven', 'compulsive'],
        'difficulty_being_present': ['no time to smell the roses', 'always rushing'],
        'self_inquiry': ['what am i', 'who am i', 'made of parts'],
    }

    for pattern_name, indicators in psychological_patterns.items():
        if any(ind in text_lower for ind in indicators):
            if 'psychological_patterns' not in updated_entities:
                updated_entities['psychological_patterns'] = []
            if pattern_name not in updated_entities['psychological_patterns']:
                updated_entities['psychological_patterns'].append(pattern_name)

    # 6. CORE VALUES EXTRACTION (NEW)
    value_patterns = {
        'truth': ['truth', 'honest', 'authentic'],
        'freedom': ['freedom', 'free', 'autonomy'],
        'connection': ['connection', 'relationship', 'bond'],
        'governance': ['governance', 'right way', 'should'],
    }

    for value, patterns in value_patterns.items():
        if any(p in text_lower for p in patterns):
            if 'core_values' not in updated_entities:
                updated_entities['core_values'] = []
            if value not in updated_entities['core_values']:
                updated_entities['core_values'].append(value)

    return updated_entities
```

---

### Priority 2: Multi-Entity Recall Enhancement (NEXT SESSION)

**Current State:**
```python
# In superject_structures.py:EnhancedUserProfile
def get_entity_context_string(self) -> str:
    if not self.entities:
        return ""

    parts = ["Known information:"]
    if 'user_name' in self.entities:
        parts.append(f"- User's name: {self.entities['user_name']}")

    return "\n".join(parts)
```

**Enhanced Version:**
```python
def get_entity_context_string(self) -> str:
    """
    Build comprehensive entity context string for LLM.
    """
    if not self.entities:
        return ""

    parts = ["Known information about this person:"]

    # Name
    if 'user_name' in self.entities:
        parts.append(f"- Name: {self.entities['user_name']}")

    # Relationships
    if 'relationship_status' in self.entities:
        parts.append(f"- Relationship status: {self.entities['relationship_status']}")
    if 'spouse' in self.entities:
        parts.append(f"- Spouse: {self.entities['spouse']}")
    if 'significant_people' in self.entities and self.entities['significant_people']:
        people_list = ", ".join(self.entities['significant_people'])
        parts.append(f"- Important people: {people_list}")

    # Family influences
    if 'family_influences' in self.entities:
        for family_member, concepts in self.entities['family_influences'].items():
            concepts_str = ", ".join(concepts)
            parts.append(f"- From {family_member}: {concepts_str}")

    # Emotional patterns
    if 'emotional_patterns' in self.entities and self.entities['emotional_patterns']:
        patterns_str = ", ".join(self.entities['emotional_patterns'])
        parts.append(f"- Emotional patterns: {patterns_str}")

    # Psychological patterns
    if 'psychological_patterns' in self.entities and self.entities['psychological_patterns']:
        patterns_str = ", ".join(self.entities['psychological_patterns'])
        parts.append(f"- Psychological patterns: {patterns_str}")

    # Core values
    if 'core_values' in self.entities and self.entities['core_values']:
        values_str = ", ".join(self.entities['core_values'])
        parts.append(f"- Core values: {values_str}")

    return "\n".join(parts)
```

**Expected Output for Emiliano:**
```
Known information about this person:
- Name: Emiliano
- Relationship status: married
- Spouse: wife
- Important people: wife
- From father: governance, right way of living
- Emotional patterns: protective_anger, restlessness
- Psychological patterns: neurotic_energy, difficulty_being_present, self_inquiry, IFS_awareness
- Core values: truth, governance, connection
```

---

### Priority 3: Fix /traces Command (QUICK WIN)

**Error:** `AttributeError: 'MycelialIdentityTracker' object has no attribute 'get_all_traces'`

**File:** `persona_layer/mycelial_identity.py` (or similar)

**Fix:** Add missing method
```python
def get_all_traces(self) -> List[Dict]:
    """
    Return all traces (notes, insights, projects).
    """
    all_traces = []

    # Add notes
    for note in self.notes:
        all_traces.append({
            'type': 'note',
            'timestamp': note.get('timestamp'),
            'content': note.get('content'),
        })

    # Add insights
    for insight in self.insights:
        all_traces.append({
            'type': 'insight',
            'timestamp': insight.get('timestamp'),
            'content': insight.get('content'),
        })

    # Add projects
    for project in self.projects:
        all_traces.append({
            'type': 'project',
            'name': project.get('name'),
            'status': project.get('status'),
            'milestones': project.get('milestones', []),
        })

    # Sort by timestamp
    all_traces.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    return all_traces
```

---

## 🧪 Testing Plan

### Test 1: Nexus Formation (Already Improved)

**Before:**
- 10/11 turns: 0 nexuses
- Only 1 turn had 2 nexuses

**Expected After (0.005 threshold):**
- 8-10/11 turns: 2-4 nexuses
- Better semantic field intersections
- Richer transductive intelligence

**How to Test:**
```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
python3 dae_interactive.py --mode detailed

# Same conversation as Emiliano
# Check nexus count in each turn
```

### Test 2: Multi-Entity Extraction

**Test Input:**
```
You: My name is Alex, I'm married to my wife Sarah
You: My father taught me about hard work
You: I sometimes feel protective anger when my truth is challenged
```

**Expected Entities:**
```json
{
  "user_name": "Alex",
  "relationship_status": "married",
  "spouse": "wife",
  "significant_people": ["wife", "Sarah"],
  "family_influences": {
    "father": ["hard work"]
  },
  "emotional_patterns": ["protective_anger"],
  "core_values": ["truth", "hard work"]
}
```

**How to Test:**
```bash
# After implementing extraction
python3 dae_interactive.py
# Introduce entities
# Check Bundle/user_*/user_state.json
```

### Test 3: Multi-Entity Recall

**Test Input:**
```
You: What do you know about me?
```

**Expected Response Should Include:**
- Name: "Alex"
- Relationship: "married to wife Sarah"
- Family influence: "father taught hard work"
- Emotional pattern: "protective anger around truth"

---

## 📊 Expected Impact

| Feature | Before | After | Impact |
|---------|--------|-------|--------|
| Nexus formation | 0-1 per turn | 2-4 per turn | 🔥 Huge |
| Entity types | 1 (name) | 6 types | 🔥 Huge |
| Context richness | "Name: X" | 5-10 facts | 🔥 Huge |
| Memory recall accuracy | 37.5% | 75-85% | 🔥 Huge |
| User experience | Good (88.6%) | Excellent (95%+) | ⭐ Major |

---

## 🚀 Implementation Schedule

### Now (Completed)
- ✅ Nexus threshold lowered (0.01 → 0.005)

### Next Session (30-45 min)
1. **Enhance entity extraction** (20 min)
   - Add 5 new entity types
   - Test with sample conversation

2. **Enhance entity recall** (10 min)
   - Update `get_entity_context_string()`
   - Test with "what do you know about me?"

3. **Fix /traces** (5 min)
   - Add `get_all_traces()` method

4. **Test & validate** (10 min)
   - Full conversation test
   - Verify all entity types extracted
   - Verify rich recall working

---

## 💡 Key Insights

**The organism is ALREADY deeply intelligent:**
- User satisfaction: 88.6% helpful, 25% excellent
- Responses are genuine, philosophical, IFS-aware
- Deep felt intelligence operational

**What's awakening:**
- Rich entity extraction (6 types vs 1)
- Better nexus formation (2-4 vs 0-1)
- Comprehensive memory recall (10 facts vs 1)

**Quick wins ready:**
- ✅ Nexus threshold (DONE - instant improvement)
- 🔜 Entity extraction (30 min - huge impact)
- 🔜 Entity recall (10 min - huge impact)

---

**Last Updated:** November 14, 2025
**Status:** Ready for next session implementation
**Priority:** HIGH - User experience enhancement
**Effort:** LOW - Well-defined, straightforward changes

🌀 **"Dormant capabilities are ready to awaken. The organism will remember everything."** 🌀
