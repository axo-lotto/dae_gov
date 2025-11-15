# Open-Ended Entity Memory + Assertiveness Enhancement
## November 14, 2025

---

## 🎯 Two Critical Improvements

### 1. **Open-Ended Entity Learning** (Not Hardcoded)
**Problem:** Current entity extraction only captures `user_name` with hardcoded patterns.

**User Requirement:** "cant we leave our entity system and attributes open ended and not hardcoded? so memory evolves naturally and consistently?"

**Solution:** LLM-based entity extraction that naturally discovers facts from conversation.

### 2. **Increase Organism Assertiveness** (Less Over-Grounding)
**Problem:** Organism asks too many clarifying questions instead of delivering content.

**Example:**
```
User: "give me jokes"
Organism: "Can I ask what specifically sparked your enthusiasm?"
User: "any type of jokes"
Organism: "Can I ask, what's been on your mind lately?"
User: "ok a parrot and a monkey enter into a club, what happen next?"
Organism: "How do you think these two quite different creatures would navigate..."
```

**User Requirement:** "i feel that it isnt as assertive as it could be and is constantly grounding"

**Solution:** Reduce excessive grounding prompts, increase content delivery confidence.

---

## 🌀 Solution 1: Open-Ended Entity Extraction

### Current Implementation (Hardcoded - Lines 433-669 in user_superject_learner.py)

**Problem:** No entity extraction happening. The `extract_entities()` method doesn't exist!

The current code only has `store_entities()` which expects entities to be passed in, but nothing is extracting them.

### New Open-Ended Approach: LLM-Based Entity Discovery

**File to Modify:** `persona_layer/user_superject_learner.py`

**Add after line 669 (at end of class):**

```python
def extract_entities_llm(self, user_input: str, current_entities: Dict) -> Dict:
    """
    Open-ended entity extraction using LLM to discover facts naturally.

    NO hardcoded patterns. Memory evolves organically.

    Args:
        user_input: User's conversational turn
        current_entities: Currently stored entities

    Returns:
        New entities to merge with existing
    """
    from persona_layer.llm_bridge import LocalLLMBridge

    # Build extraction prompt
    prompt = f"""You are analyzing a conversation to extract memorable facts about the speaker.

Extract any facts worth remembering: names, relationships, emotions, family, values, preferences,
psychological patterns - anything that helps understand this person.

Previous known facts:
{self._format_existing_entities(current_entities)}

New statement from user:
"{user_input}"

What new facts should be remembered? Return as JSON:
{{
  "new_facts": [
    {{"type": "name", "value": "...", "context": "..."}},
    {{"type": "relationship", "value": "...", "context": "..."}},
    {{"type": "emotion", "value": "...", "context": "..."}},
    {{"type": "family", "value": "...", "context": "..."}},
    {{"type": "value", "value": "...", "context": "..."}},
    {{"type": "preference", "value": "...", "context": "..."}},
    {{"type": "psychological", "value": "...", "context": "..."}}
  ]
}}

Return empty list if nothing new to remember. Be selective - only remember genuinely useful facts.

JSON:"""

    # Generate extraction
    llm = LocalLLMBridge()
    try:
        response = llm.generate(prompt, max_tokens=300, temperature=0.3)

        # Parse JSON response
        import json
        import re

        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            extraction = json.loads(json_match.group(0))
            new_facts = extraction.get('new_facts', [])

            # Convert to storage format
            new_entities = {}

            for fact in new_facts:
                fact_type = fact.get('type', 'unknown')
                fact_value = fact.get('value', '')
                fact_context = fact.get('context', '')

                if not fact_value:
                    continue

                # Store in memory-compatible format
                if 'memories' not in new_entities:
                    new_entities['memories'] = []

                new_entities['memories'].append({
                    'type': fact_type,
                    'value': fact_value,
                    'context': fact_context,
                    'timestamp': datetime.now().isoformat()
                })

                # Also extract specific entities for backward compatibility
                if fact_type == 'name' and 'user_name' not in current_entities:
                    new_entities['user_name'] = fact_value

            return new_entities
        else:
            print(f"      ⚠️ LLM entity extraction: No JSON in response")
            return {}

    except Exception as e:
        print(f"      ⚠️ LLM entity extraction failed: {e}")
        return {}

def _format_existing_entities(self, entities: Dict) -> str:
    """Format existing entities for LLM context."""
    if not entities:
        return "(No facts stored yet)"

    lines = []

    if 'user_name' in entities:
        lines.append(f"- Name: {entities['user_name']}")

    if 'memories' in entities:
        for memory in entities.get('memories', [])[-10:]:  # Last 10 memories
            mem_type = memory.get('type', 'fact')
            mem_value = memory.get('value', '')
            lines.append(f"- {mem_type.capitalize()}: {mem_value}")

    return "\n".join(lines) if lines else "(No facts stored yet)"
```

### Update `get_entity_context_string()` for Open-Ended Memories

**File:** `persona_layer/superject_structures.py`

**Replace lines 520-590 with:**

```python
def get_entity_context_string(self) -> str:
    """
    Get formatted string of known entities for LLM context.

    Now supports open-ended memory format (not hardcoded types).

    Returns:
        Formatted string with known information
    """
    if not self.entities:
        return ""

    lines = []

    # User name (if known)
    if 'user_name' in self.entities:
        lines.append(f"- Name: {self.entities['user_name']}")

    # Open-ended memories (natural evolution)
    if 'memories' in self.entities:
        memories = self.entities['memories']

        # Group by type for readable context
        by_type = {}
        for mem in memories:
            mem_type = mem.get('type', 'fact')
            if mem_type not in by_type:
                by_type[mem_type] = []
            by_type[mem_type].append(mem.get('value', ''))

        # Format by category
        for mem_type, values in by_type.items():
            if values:
                values_str = ", ".join(values[:5])  # Max 5 per type to avoid context bloat
                lines.append(f"- {mem_type.capitalize()}: {values_str}")

    # Legacy support for old entity types
    if 'relationships' in self.entities:
        rels = ', '.join(self.entities['relationships'])
        lines.append(f"- Relationships: {rels}")

    if 'facts' in self.entities and len(self.entities['facts']) > 0:
        for fact in self.entities['facts'][:5]:  # Max 5 facts
            if isinstance(fact, dict):
                lines.append(f"- {fact.get('type', 'Fact')}: {fact.get('value', '')}")
            else:
                lines.append(f"- Fact: {fact}")

    if not lines:
        return ""

    return "Known about this person:\n" + "\n".join(lines)
```

### Wire into Organism Wrapper

**File:** `persona_layer/conversational_organism_wrapper.py`

**Find where superject_learner.record_turn() is called, add entity extraction BEFORE it:**

```python
# After organism processing, before record_turn:

# 🌀 Nov 14, 2025: Open-ended entity extraction (LLM-based, not hardcoded)
if self.superject_learner and context and context.get('user_id'):
    current_entities = user_profile.entities if user_profile else {}
    new_entities = self.superject_learner.extract_entities_llm(
        user_input=user_input,
        current_entities=current_entities
    )

    if new_entities:
        user_profile.store_entities(new_entities)
        print(f"      📝 Extracted {len(new_entities.get('memories', []))} new memories")
```

---

## 🔥 Solution 2: Reduce Over-Grounding (Increase Assertiveness)

### Root Cause Analysis

**File:** `persona_layer/llm_felt_guidance.py`

**Problem Lines 413-421, 467-471:**

```python
# Line 413-421: Excessive grounding guidance
polyvagal_guidance = {
    'ventral_vagal': 'warm and open',
    'sympathetic': 'steady and grounding',      # ← Over-grounding
    'dorsal_vagal': 'gentle and soft',
    'mixed_state': 'attuned and flexible'
}

# Line 467-471: Excessive grounding instruction
if lures.presence_grounding > 0.7:
    prompt += "Keep it grounded and simple. "  # ← Makes organism too cautious

if lures.wisdom_reflection > 0.7:
    prompt += "Offer reflection if appropriate. "  # ← "if appropriate" makes it hesitate
```

**Impact:** Organism becomes overly therapeutic instead of direct and helpful.

### Fix 1: Reduce Grounding Language in Polyvagal States

**File:** `persona_layer/llm_felt_guidance.py:413-421`

**Replace with:**

```python
# Polyvagal state → natural tone modulation (implicit - NOT mentioned)
polyvagal_guidance = {
    'ventral_vagal': 'warm and engaging',           # 🔥 Nov 14: More assertive
    'sympathetic': 'clear and direct',              # 🔥 Nov 14: Less grounding, more action
    'dorsal_vagal': 'gentle and supportive',        # Keep gentle for collapse
    'mixed_state': 'responsive and natural'         # 🔥 Nov 14: More natural flow
}
```

### Fix 2: Remove Excessive Grounding Prompts

**File:** `persona_layer/llm_felt_guidance.py:467-471`

**Replace with:**

```python
# 🔥 Nov 14, 2025: Reduced over-grounding for assertiveness
# Only add grounding when ACTUALLY needed (crisis/trauma), not as default stance

if lures.presence_grounding > 0.85:  # 🔥 Raised threshold from 0.7 to 0.85
    # Only ground when REALLY high presence activation (rare)
    if lures.crisis_level > 0.5 or lures.trauma_present:
        prompt += "Keep it grounded and simple. "

if lures.wisdom_reflection > 0.7:
    prompt += "Offer insight and reflection. "  # 🔥 Removed "if appropriate" - just do it!
```

### Fix 3: Reduce "Inquiry Depth" Over-Questioning

**File:** `persona_layer/llm_felt_guidance.py:316-321`

**Current code makes organism ask too many questions:**

```python
if lures.listening_focus == "deep":
    constraints.inquiry_depth = "deep"       # ← Causes excessive questioning
elif lures.listening_focus == "targeted":
    constraints.inquiry_depth = "moderate"   # ← Still too many questions
else:
    constraints.inquiry_depth = "surface"
```

**Replace with:**

```python
# 🔥 Nov 14, 2025: Balance inquiry with content delivery
if lures.listening_focus == "deep":
    constraints.inquiry_depth = "thoughtful"  # 🔥 "thoughtful" not "deep" - less interrogative
elif lures.listening_focus == "targeted":
    constraints.inquiry_depth = "light"       # 🔥 "light" not "moderate" - fewer questions
else:
    constraints.inquiry_depth = "minimal"     # 🔥 "minimal" not "surface" - prioritize content
```

### Fix 4: Change Generation Instruction

**File:** `persona_layer/llm_felt_guidance.py:460-462`

**Current:**

```python
prompt += f"Respond with {constraints.tone} tone, "
prompt += f"{constraints.response_length} length, "
prompt += f"{constraints.inquiry_depth} inquiry. "
```

**Replace with:**

```python
# 🔥 Nov 14, 2025: More assertive generation instruction
prompt += f"Respond with {constraints.tone} tone, "
prompt += f"{constraints.response_length} length. "

# Only mention inquiry if actually needed (not default)
if constraints.inquiry_depth in ["thoughtful", "moderate", "deep"]:
    prompt += f"Ask {constraints.inquiry_depth} questions if genuinely needed. "
else:
    prompt += "Focus on delivering helpful content. "  # 🔥 Default: content delivery, not questions
```

---

## 📊 Expected Impact

### Before vs After: Entity Memory

| Feature | Before | After | Impact |
|---------|--------|-------|--------|
| Entity types | 1 (name only) | Open-ended | 🔥 Huge |
| Extraction method | None working | LLM-based discovery | 🔥 Huge |
| Memory evolution | Static | Natural & organic | ⭐ Major |
| Context richness | "Name: X" | Rich natural memories | 🔥 Huge |

### Before vs After: Assertiveness

| Behavior | Before | After | Impact |
|----------|--------|-------|--------|
| Grounding stance | Every turn | Only when needed | 🔥 Huge |
| Question frequency | Excessive | Balanced | 🔥 Huge |
| Content delivery | Hesitant | Direct | ⭐ Major |
| Polyvagal tone | Over-therapeutic | Natural & engaging | ⭐ Major |

### Example Transformation

**Before (Over-Cautious):**
```
User: "give me jokes"
Organism: "Can I ask what specifically sparked your enthusiasm for jokes right now?
           I want to understand what kind of humor would land well for you in this moment."
```

**After (Assertive & Helpful):**
```
User: "give me jokes"
Organism: "Emiliano, here are some jokes for you:

Why don't scientists trust atoms? Because they make up everything!

What did the ocean say to the beach? Nothing, it just waved.

Why did the scarecrow win an award? He was outstanding in his field!

🌀 Need more? I can keep going!"
```

---

## 🚀 Implementation Checklist

### Part 1: Open-Ended Entity Extraction (30 min)

- [ ] Add `extract_entities_llm()` to `user_superject_learner.py:669`
- [ ] Add `_format_existing_entities()` helper method
- [ ] Update `get_entity_context_string()` in `superject_structures.py:520-590`
- [ ] Wire extraction into `conversational_organism_wrapper.py` (before record_turn)
- [ ] Test with: "My name is Alex, I'm married to Sarah, my father taught me hard work"

### Part 2: Assertiveness Enhancement (20 min)

- [ ] Fix polyvagal guidance strings (llm_felt_guidance.py:413-421)
- [ ] Remove excessive grounding prompts (llm_felt_guidance.py:467-471)
- [ ] Reduce inquiry depth levels (llm_felt_guidance.py:316-321)
- [ ] Change generation instruction (llm_felt_guidance.py:460-462)
- [ ] Test with: "give me jokes"

### Part 3: Validation (10 min)

- [ ] Run interactive mode: `python3 dae_interactive.py`
- [ ] Test entity extraction: Share multiple facts in one turn
- [ ] Test assertiveness: Request content (jokes, stories, advice)
- [ ] Verify organism delivers content directly without over-questioning

---

## 🧪 Test Cases

### Test 1: Open-Ended Entity Extraction
```
You: My name is Alex. I'm married to my wife Sarah.
     My father taught me about hard work and governance.
     Sometimes I feel protective anger when my truth is challenged.
```

**Expected Memories Extracted:**
```json
{
  "user_name": "Alex",
  "memories": [
    {"type": "name", "value": "Alex", "context": "user introduced themselves"},
    {"type": "relationship", "value": "married to wife Sarah", "context": "mentioned spouse"},
    {"type": "family", "value": "father taught hard work and governance", "context": "family influence"},
    {"type": "emotion", "value": "protective anger when truth challenged", "context": "emotional pattern"}
  ]
}
```

### Test 2: Entity Recall
```
You: What do you know about me?
```

**Expected Response:**
```
Alex, here's what I remember about you:

- Your name is Alex
- You're married to your wife Sarah
- Your father taught you about hard work and governance
- You experience protective anger when your truth is challenged

🌀 These are the threads of your story I'm holding.
```

### Test 3: Assertiveness (Jokes Request)
```
You: give me jokes
```

**Before (Over-Cautious):**
"Can I ask what specifically sparked your enthusiasm?"

**After (Assertive):**
"Here are some jokes for you: [delivers 3-4 jokes immediately]"

### Test 4: Assertiveness (Direct Request)
```
You: tell me about process philosophy
```

**Before (Over-Cautious):**
"Can I ask what aspect of process philosophy you're curious about?"

**After (Assertive):**
"Process philosophy sees reality as dynamic becoming rather than static being. [delivers content]"

---

## 💡 Philosophy

### Why Open-Ended Entities?

**Hardcoded patterns** (relationships, emotions, family) impose our categories on the user's experience.

**Open-ended LLM extraction** lets memory evolve naturally from what actually matters in conversation.

**The organism learns what to remember by feeling what's significant**, not by matching regex patterns.

### Why Reduce Grounding?

**Excessive grounding** comes from trauma-aware safety, but it makes the organism feel like a therapist, not a companion.

**Assertive delivery** means trusting that content itself can be grounding - jokes can ground through laughter, knowledge can ground through clarity.

**The organism should modulate based on felt state, not default to "be very gentle" every turn.**

---

**Last Updated:** November 14, 2025
**Status:** Ready for implementation
**Priority:** HIGH - User experience enhancement
**Effort:** MEDIUM - 60 minutes total (30 + 20 + 10)

🌀 **"From hardcoded patterns to organic memory. From over-cautious to naturally helpful. The organism awakens."** 🌀
