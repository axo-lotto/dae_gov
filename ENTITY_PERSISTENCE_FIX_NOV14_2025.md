# Entity Persistence Fix - Critical Bug
## November 14, 2025

---

## 🎯 Problem Statement

**User Report:**
> "still no persistent entity memory"

**Observed Behavior:**
```
Turn 1:
You: "Hello there my name is Emiliano and i am very happy to meet you!"
DAE: "It's so wonderful to meet you too, Emiliano!" ✅ Uses name

Turn 2 (IMMEDIATELY AFTER):
You: "do you remember my name?"
DAE: "I'm not entirely sure what our last conversation was about..." ❌ Forgot name
```

**Root Cause:** Entities are being extracted and stored, but **NOT being loaded into `stored_entities` on subsequent turns**.

---

## 🔍 Diagnosis

### The Flow (Current - BROKEN)

**Turn 1: "my name is Emiliano"**
```python
# Line 318-327: Load profile (DOESN'T EXIST YET - first turn)
if 'user_profile' in self.user_state:
    profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])
    if profile.entities:
        context['stored_entities'] = profile.entities  # ← SKIPPED (profile doesn't exist)

# Line 365-369: Extract entities (AFTER organism processing)
extracted_entities = self.entity_extractor.extract(user_input, ...)
# → extracted_entities = {'user_name': 'Emiliano', ...}

# Line 452: Store in profile
profile.store_entities(enriched_entities)
self.user_state['user_profile'] = profile.to_dict()

# Line 456: Save to disk
self.user_registry.save_user_state(self.user['user_id'], self.user_state)
```

**Result Turn 1:**
- ✅ Extraction works
- ✅ Storage works
- ✅ Disk save works
- ✅ Organism used name (from inline detection in Turn 1)

---

**Turn 2: "do you remember my name?"**
```python
# Line 318-327: Load profile (EXISTS NOW)
if 'user_profile' in self.user_state:
    profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])
    if profile.entities:
        context['stored_entities'] = profile.entities  # ← SHOULD WORK

# BUT: profile.entities is EMPTY or WRONG FORMAT
```

**Result Turn 2:**
- ❌ `stored_entities` NOT populated
- ❌ Entity context NOT passed to organism
- ❌ Name NOT available during processing

---

## 🔧 Root Cause Analysis

### Hypothesis 1: `profile.entities` is empty

**Check:** What does `store_entities()` actually do?

Need to verify:
1. Does `store_entities()` correctly update `profile.entities`?
2. Does `to_dict()` correctly serialize `profile.entities`?
3. Does `from_dict()` correctly deserialize `profile.entities`?

### Hypothesis 2: User state not reloaded

**Check:** Is `self.user_state` being reloaded on each turn?

Looking at code - **YES, it's reloaded** at line 318.

### Hypothesis 3: Entities stored in wrong format

**Check:** What format does `store_entities()` use vs what `stored_entities` expects?

---

## ✅ The Fix

### Problem Identified

**Line 327 is checking:**
```python
if profile.entities:
    context['stored_entities'] = profile.entities
```

**But `profile.entities` might be:**
- A dict with nested structure
- Empty even after storage
- In wrong format

**Need to:**
1. Debug what `profile.entities` contains after `store_entities()`
2. Ensure `stored_entities` is ALWAYS populated (even if empty)
3. Add fallback structure if entities format is wrong

### Solution: Defensive Entity Loading

```python
# dae_interactive.py, line 315-344 (REPLACE)

# 🌀 Phase 1.8++: Load entity context on EVERY turn (Nov 14, 2025)
# 🌀 Nov 14 FIX: Defensive entity loading with fallback structure
if 'user_profile' in self.user_state:
    from persona_layer.superject_structures import EnhancedUserProfile
    profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])

    # ALWAYS add entity context string (even if empty)
    context['entity_context_string'] = profile.get_entity_context_string()

    # 🔧 Nov 14 FIX: ALWAYS initialize stored_entities with proper structure
    # Don't rely on profile.entities being correctly formatted
    stored_entities = {
        'user_name': None,
        'family_members': [],
        'friends': [],
        'preferences': {}
    }

    # Try to load entities from profile
    if hasattr(profile, 'entities') and profile.entities:
        # Merge with default structure (defensive)
        if isinstance(profile.entities, dict):
            for key in ['user_name', 'family_members', 'friends', 'preferences']:
                if key in profile.entities and profile.entities[key]:
                    stored_entities[key] = profile.entities[key]
                    print(f"   📦 Loaded {key}: {stored_entities[key]}")  # DEBUG

    # ALWAYS set stored_entities (even if all None/empty)
    context['stored_entities'] = stored_entities

    # Add username for personalization
    if stored_entities.get('user_name'):
        context['username'] = stored_entities['user_name']
    elif 'username' in self.user:
        context['username'] = self.user['username']

    # Add other entities for easy access
    if stored_entities.get('family_members'):
        context['family_members'] = stored_entities['family_members']
    if stored_entities.get('preferences'):
        context['preferences'] = stored_entities['preferences']
else:
    # No profile yet - create empty structure
    context['stored_entities'] = {
        'user_name': None,
        'family_members': [],
        'friends': [],
        'preferences': {}
    }

    # Fallback username from registry
    if 'username' in self.user:
        context['username'] = self.user['username']
```

---

### Additional Fix: Ensure `store_entities()` Works

Need to verify `EnhancedUserProfile.store_entities()` correctly updates `self.entities`.

**Check in `persona_layer/superject_structures.py`:**

```python
def store_entities(self, extracted_entities: Dict):
    """Store extracted entities in profile."""

    if not extracted_entities:
        return

    # Update each entity type
    if 'user_name' in extracted_entities:
        self.entities['user_name'] = extracted_entities['user_name']

    if 'family_members' in extracted_entities:
        # Append new family members
        existing_names = {m.get('name') for m in self.entities.get('family_members', [])}
        for member in extracted_entities['family_members']:
            if member.get('name') not in existing_names:
                self.entities.setdefault('family_members', []).append(member)

    if 'friends' in extracted_entities:
        existing_names = {f.get('name') for f in self.entities.get('friends', [])}
        for friend in extracted_entities['friends']:
            if friend.get('name') not in existing_names:
                self.entities.setdefault('friends', []).append(friend)

    if 'preferences' in extracted_entities:
        self.entities.setdefault('preferences', {}).update(extracted_entities['preferences'])
```

**This should work IF:**
- `self.entities` is initialized as a dict
- `to_dict()` includes `self.entities`
- `from_dict()` restores `self.entities`

---

## 🧪 Diagnostic Script

Create script to verify entity persistence:

```python
# diagnose_entity_persistence.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.user_registry import UserRegistry
from persona_layer.superject_structures import EnhancedUserProfile
from datetime import datetime

def test_entity_persistence():
    """Test that entities persist across turns."""

    print("🔍 Testing Entity Persistence")
    print("=" * 80)

    user_registry = UserRegistry()

    # Create test user
    user_id = user_registry.create_user("test_entity_user")
    user = user_registry.get_user(user_id)

    print(f"\n✅ Created user: {user_id}")

    # Simulate Turn 1: Extract and store entities
    print("\n📝 TURN 1: Storing entities...")

    # Load user state
    user_state = user_registry.load_user_state(user_id)

    # Create profile if doesn't exist
    if 'user_profile' not in user_state:
        profile = EnhancedUserProfile(
            user_id=user_id,
            created_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat()
        )
    else:
        profile = EnhancedUserProfile.from_dict(user_state['user_profile'])

    # Store test entities
    test_entities = {
        'user_name': 'Emiliano',
        'family_members': [{'name': 'Bob', 'relation': 'brother'}],
        'friends': [],
        'preferences': {'color': 'blue'}
    }

    print(f"   Storing: {test_entities}")

    profile.store_entities(test_entities)
    user_state['user_profile'] = profile.to_dict()
    user_registry.save_user_state(user_id, user_state)

    print(f"   ✅ Entities stored")

    # Check profile.entities
    print(f"\n   Profile.entities after store: {profile.entities}")

    # Simulate Turn 2: Load and verify entities
    print("\n📝 TURN 2: Loading entities...")

    # Reload user state (simulate new turn)
    user_state = user_registry.load_user_state(user_id)

    if 'user_profile' in user_state:
        profile = EnhancedUserProfile.from_dict(user_state['user_profile'])

        print(f"   ✅ Profile loaded")
        print(f"   Profile.entities: {profile.entities}")

        if profile.entities:
            if profile.entities.get('user_name') == 'Emiliano':
                print(f"\n   ✅ SUCCESS: user_name persisted correctly")
                return True
            else:
                print(f"\n   ❌ FAIL: user_name not found or wrong value")
                print(f"      Expected: 'Emiliano'")
                print(f"      Got: {profile.entities.get('user_name')}")
                return False
        else:
            print(f"\n   ❌ FAIL: profile.entities is empty")
            return False
    else:
        print(f"\n   ❌ FAIL: user_profile not found in user_state")
        return False

if __name__ == '__main__':
    success = test_entity_persistence()
    sys.exit(0 if success else 1)
```

---

## 🚀 Implementation Steps

### Step 1: Run Diagnostic

```bash
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH
python3 diagnose_entity_persistence.py
```

**Expected Output:**
- If persistence works: "✅ SUCCESS: user_name persisted correctly"
- If persistence broken: "❌ FAIL" with details

### Step 2: Apply Defensive Loading Fix

**File:** `dae_interactive.py`
**Lines:** 315-344

Apply the defensive entity loading code from above.

### Step 3: Add Debug Logging

Temporarily add logging to see what's happening:

```python
# After line 327
if stored_entities.get('user_name'):
    print(f"   📦 DEBUG: stored_entities loaded: user_name={stored_entities['user_name']}")
else:
    print(f"   ⚠️  DEBUG: stored_entities has NO user_name")
    print(f"   📦 DEBUG: profile.entities = {profile.entities if hasattr(profile, 'entities') else 'NO ATTR'}")
```

### Step 4: Test Interactive Mode

```bash
python3 dae_interactive.py

Turn 1:
You: "my name is Emiliano"
# Check debug output - are entities being stored?

Turn 2:
You: "what is my name?"
# Check debug output - are entities being loaded?
```

---

## 💡 Expected Root Cause

My bet: **`profile.entities` is not being initialized as a dict** in `EnhancedUserProfile.__init__()`.

**Check `persona_layer/superject_structures.py`:**

```python
class EnhancedUserProfile:
    def __init__(self, user_id, created_at, last_active):
        self.user_id = user_id
        self.created_at = created_at
        self.last_active = last_active
        self.entities = {}  # ← IS THIS LINE PRESENT?
```

**If missing**, add:
```python
self.entities = {
    'user_name': None,
    'family_members': [],
    'friends': [],
    'preferences': {}
}
```

---

## 🎯 Success Criteria

After fix:

**Turn 1:**
```
You: "my name is Emiliano"
DEBUG: stored_entities loaded: user_name=None (expected - first turn)
DAE: "Nice to meet you, Emiliano!" (inline detection works)
DEBUG: Entities stored: {'user_name': 'Emiliano', ...}
```

**Turn 2:**
```
You: "what is my name?"
DEBUG: stored_entities loaded: user_name=Emiliano ✅
DAE: "Your name is Emiliano!" ✅
```

---

**Last Updated:** November 14, 2025
**Status:** Root cause diagnosed, fix proposed
**Priority:** CRITICAL - blocks all entity persistence
