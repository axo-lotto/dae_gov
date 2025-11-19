# 🧠 Entity Interface Testing Guide
## Interactive Neo4j Entity Management in DAE
**Date:** November 16, 2025
**Status:** Ready for Testing
**Implementation:** Option A - Interface First

---

## ✅ What Was Implemented

### New Commands in `dae_interactive.py`

**View Commands:**
```bash
/entities                 # List all entities for current user
/entities person          # Filter by type (person, place, preference, fact)
/entities Emma            # Show specific entity with relationships
```

**Edit Commands:**
```bash
/entity add person "Name" relationship="daughter" age=8
/entity link "Emma" "Lily" siblings
```

**Graph Commands:**
```bash
/graph Emma              # Show Emma's relationship graph (1-hop)
/graph Emma 2            # Show 2-hop connections
/graph stats             # Neo4j graph statistics
```

### Features

1. **Dual Storage Strategy**
   - Neo4j first (if connected)
   - JSON fallback (always available)
   - Graceful degradation

2. **Entity Types Supported**
   - Person (with relationships: daughter, son, friend, etc.)
   - Place
   - Preference
   - Fact

3. **Relationship Visualization**
   - ASCII tree graph rendering
   - Multi-hop queries (1-3 degrees)
   - Relationship type display

4. **TSK Integration Ready**
   - Properties: polyvagal_state, safety_score, age
   - Mention count tracking
   - Historical context (coming in next update)

---

## 🧪 Testing Workflow

### Test 1: Basic Entity Creation (JSON Fallback)

**Scenario:** No Neo4j connected, test JSON storage

```bash
# Start interactive
python3 dae_interactive.py

# Add yourself
/entity add person "YourName" relationship="self"

# Add family members
/entity add person "Emma" relationship="daughter" age=8
/entity add person "Lily" relationship="daughter" age=5

# List all entities
/entities

# Expected output:
#   📁 Person (3)
#      🔹 YourName     rel:self        (0 mentions)
#      🔹 Emma         rel:daughter | age:8    (0 mentions)
#      🔹 Lily         rel:daughter | age:5    (0 mentions)
```

### Test 2: Entity Filtering

```bash
# Filter by type
/entities person

# View specific entity
/entities Emma

# Expected: Shows Emma's details (JSON fallback)
```

### Test 3: Entity Creation with Neo4j (If Connected)

```bash
# Same as Test 1, but should see:
#   ✅ Added to Neo4j
#   ✅ Added to JSON profile

# Verify dual storage
/entities
# Should show: Source: Neo4j | Count: 3
```

### Test 4: Entity Relationships (Neo4j Required)

```bash
# Link entities
/entity link "Emiliano" "Emma" HAS_DAUGHTER
/entity link "Emiliano" "Lily" HAS_DAUGHTER
/entity link "Emma" "Lily" SIBLINGS

# View graph
/graph Emiliano

# Expected ASCII output:
#   Emiliano
#   ├── [HAS_DAUGHTER] --> Emma
#   └── [HAS_DAUGHTER] --> Lily

/graph Emma 2  # 2-hop connections

# Expected:
#   Emma
#   ├── [HAS_FATHER] --> Emiliano
#   ├── [SIBLINGS] --> Lily
#   └── ... (2nd degree relationships)
```

### Test 5: Graph Statistics

```bash
/graph stats

# Expected output:
#   📊 Overall:
#      Total entity nodes: 3
#      Total relationships: 3
#
#   👤 Your Entities:
#      Entities stored: 3
#      - Person: 3
```

### Test 6: Entity Prehension Integration (Critical!)

```bash
# This tests if entities are retrieved BEFORE organ activation

# First, add an entity
/entity add person "TestPerson" relationship="friend"

# Then ask DAE about it
You: Do you remember TestPerson?

# Watch for in output:
#   🧠 Pre-retrieved 1 entities:
#      - TestPerson (salient_context)
#
#   🔗 Nexuses: 1-2
#      Dominant: Entity Memory (or similar)
#
#   💬 Emission:
#      Yes, I remember TestPerson...

# If this works, entity prehension is operational! 🎉
```

---

## 🔍 Validation Checklist

### Phase 1: JSON Fallback (No Neo4j)
- [ ] `/entities` lists entities from user profile
- [ ] `/entity add` stores in JSON successfully
- [ ] `/entities person` filters correctly
- [ ] `/entities Emma` shows details (from JSON)
- [ ] Entity properties display correctly (relationship, age)

### Phase 2: Neo4j Integration (If Connected)
- [ ] `/entities` retrieves from Neo4j
- [ ] `/entity add` stores in both Neo4j + JSON
- [ ] `/entity link` creates relationships
- [ ] `/graph Emma` displays ASCII tree
- [ ] `/graph stats` shows correct counts
- [ ] `/graph Emma 2` shows 2-hop connections

### Phase 3: Entity Prehension (The Critical Test!)
- [ ] Add test entity manually
- [ ] Ask "Do you remember [entity]?"
- [ ] Verify entity pre-retrieved (watch debug output)
- [ ] Verify Entity Memory Nexus formed
- [ ] Verify emission references entity correctly

### Phase 4: Conversational Learning
- [ ] Have 5-turn conversation mentioning "Emma"
- [ ] Run `/entities Emma` to see mention count increase
- [ ] Check if polyvagal_state is tracked
- [ ] Verify TSK enrichment (safety_score, etc.)

---

## 🚨 Known Limitations (To Be Fixed)

1. **Property Retrieval** - Line 1762: "Property retrieval coming in next update"
   - Can create entities with properties
   - Can't yet query individual entity properties from Neo4j
   - Workaround: Properties stored in JSON, visible in `/entities` list

2. **Entity Mention Count** - Currently hardcoded to 0
   - Need to track mentions during conversation
   - Should increment when entity prehension retrieves entity
   - Fix: Add mention tracking to pre_emission_entity_prehension

3. **No Entity Delete** - Can add entities, can't remove them yet
   - Low priority for testing phase
   - Can manually edit JSON if needed

4. **No Entity Edit** - Can't update properties after creation
   - Workaround: Delete JSON entry and re-add
   - Better UX: `/entity edit Emma age=9` (future)

---

## 🎯 Success Criteria for Option A

### Minimum Viable (Must Have)
1. ✅ `/entities` command works (JSON + Neo4j)
2. ✅ `/entity add` creates entities in both stores
3. ✅ `/graph` visualizes relationships (ASCII)
4. ✅ Dual-storage graceful degradation
5. ⏳ Entity prehension retrieves entities BEFORE organ activation (TEST THIS!)

### Nice to Have
- [ ] Mention count tracking
- [ ] Entity property updates
- [ ] Delete/edit commands
- [ ] Search entities by property value
- [ ] Export/import entity graphs

---

## 📝 Testing Script

```bash
# Quick 5-minute test

# 1. Start DAE interactive
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH
python3 dae_interactive.py

# 2. Add test entities
/entity add person "TestUser" relationship="self"
/entity add person "TestFriend" relationship="friend"

# 3. Check they're stored
/entities

# 4. Test prehension (THE CRITICAL TEST!)
You: Do you remember TestFriend?

# 5. Look for:
#    - Entity pre-retrieved (should see message)
#    - Nexus formed (should be > 0)
#    - Emission mentions TestFriend

# 6. If Neo4j connected, test relationships
/entity link "TestUser" "TestFriend" FRIENDS_WITH
/graph TestUser

# 7. Exit
/exit
```

---

## 🔄 Next Steps After Testing

### If Entity Prehension Works (Most Important!)
✅ **PROCEED TO TRAINING**
- Create 20 basic entity-memory training pairs
- Run first epoch with validation
- Measure: entity recall accuracy, nexus formation rate

### If Entity Prehension Fails
❌ **DEBUG FIRST**
- Check `pre_emission_entity_prehension.py` integration
- Verify entity retrieval happens before organ activation
- Ensure entity context passed to organs correctly
- Test with `test_pre_emission_entity_prehension.py`

### If Neo4j Fails
⚠️ **JSON FALLBACK IS FINE**
- Can still test entity prehension with JSON
- Training will work without Neo4j
- Add Neo4j later for graph queries

---

## 🌀 Philosophy Check

**The Bet:**
> Entities should be PREHENDED (felt as past occasions), not RETRIEVED (looked up as data).

**How to Validate:**
1. Add entity manually: `/entity add person "Emma" relationship="daughter"`
2. Ask DAE: "Do you remember Emma?"
3. **Success:** DAE feels Emma's presence BEFORE generating response
4. **Failure:** DAE treats "Emma" as unknown word, generates generic response

**Expected Behavior:**
```
You: Do you remember Emma?

[Internal - if detailed mode]
🧠 Pre-retrieved 1 entities:
   - Emma (direct_mention)
   Reason: relational_query

LISTENING.relational_inquiry boosted: 0.65 → 0.85
BOND.entity_parts_available: True

🔗 Nexuses: 1
   Dominant: Entity Memory Nexus (coherence: 0.78)

💬 Emission:
   Yes, I remember Emma - your daughter.
```

If this works → **Entity memory is prehension, not retrieval** ✅
If this fails → **Need to debug pre-emission integration** ❌

---

## 📊 Success Metrics

After testing session, record:

- [ ] Total entities added: _____
- [ ] JSON storage working: Yes/No
- [ ] Neo4j storage working: Yes/No (if connected)
- [ ] Relationships created: _____
- [ ] Graph visualization working: Yes/No
- [ ] **Entity prehension working: Yes/No** ⭐ MOST IMPORTANT
- [ ] Nexus formation rate when entities mentioned: _____%

---

**Status:** Ready for Testing
**Priority:** Test entity prehension (Test 6) FIRST - it validates the architecture
**Timeline:** 30 minutes for basic tests, then decide on training corpus or debugging

🌀 *"The entity interface is the window into DAE's memory. If you can see it, edit it, and DAE can prehend it, we have the foundation for persistent relationship learning."*
