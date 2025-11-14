# 🔌 Neo4j Setup Instructions - DAE-GOV Knowledge Infrastructure

**Status**: Phase 2.3 - Neo4j Installation & Validation
**Time Required**: 10-15 minutes
**Prerequisite**: Neo4j Python driver installed ✅

---

## 🎯 Quick Start (Recommended Path)

### **Option A: Neo4j Aura Free (Cloud-Based) - RECOMMENDED**

**Why Aura**: Zero installation, works immediately, free forever, perfect for development

#### Step 1: Sign Up & Create Database (5 minutes)

1. **Visit**: https://neo4j.com/cloud/aura-free/
2. **Sign up** with email (free account)
3. **Create new database**:
   - Name: `dae-gov-knowledge`
   - Region: Choose closest to you
   - Click "Create"

#### Step 2: Save Credentials (1 minute)

After database creation, you'll see:
```
Connection URI:   neo4j+s://xxxxx.databases.neo4j.io
Username:         neo4j
Password:         [auto-generated]
```

**⚠️ SAVE THESE!** You'll need them in Step 3.

You can also download a `.env` file with these credentials.

#### Step 3: Update Test Script (1 minute)

Open `knowledge_base/test_neo4j_connection.py` and update lines 24-27:

```python
# For Aura Free (cloud):
URI = "neo4j+s://xxxxx.databases.neo4j.io"  # ← Paste your URI here
USER = "neo4j"
PASSWORD = "your_aura_password"  # ← Paste your password here
DATABASE = "neo4j"
```

#### Step 4: Run Validation Test (2 minutes)

```bash
cd "/Users/daedalea/Desktop/DAE_HYPHAE_1"
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1:$PYTHONPATH"

python3 knowledge_base/test_neo4j_connection.py
```

**Expected Output**:
```
======================================================================
NEO4J CONNECTION TEST
======================================================================

🔌 Connecting to Neo4j...
   URI: neo4j+s://xxxxx.databases.neo4j.io
   Database: neo4j

✅ Neo4j Knowledge Graph connected
   URI: neo4j+s://xxxxx.databases.neo4j.io
   Database: neo4j

✅ CONNECTION SUCCESSFUL!

📊 Running full test (initializing 16 concepts + 18 relationships)...
   This will take ~5 seconds...

✅ Created 16 trauma-informed concepts
✅ Created 18 concept relationships
✅ Transformation path: ['Burnout Spiral', 'Sustainable Rhythm']
✅ ALL TESTS PASSED
```

#### Step 5: Explore Your Graph (Optional - 5 minutes)

1. Go to Aura console: https://console.neo4j.io/
2. Click on your database → "Open with Neo4j Browser"
3. Run this query to see all concepts:
   ```cypher
   MATCH (c:Concept) RETURN c LIMIT 25
   ```
4. Click on nodes to explore relationships

---

## 📊 What Gets Created

### **16 Trauma-Informed Concepts**

| Category | Concepts |
|----------|----------|
| **Polyvagal States** | Ventral Vagal State, Sympathetic State, Dorsal Vagal State |
| **IFS Parts** | Manager Part, Firefighter Part, Exile Part, SELF-Energy |
| **Organizational Shadow** | Burnout Spiral, Toxic Productivity, Scapegoat Dynamics |
| **SELF-Led States** | Sustainable Rhythm, Psychological Safety, Witnessing Presence |
| **Process Philosophy** | Prehension, Concrescence, Satisfaction |

### **18 Concept Relationships**

Examples:
- `Ventral Vagal State` **ENABLES** `Psychological Safety`
- `Sympathetic State` **CORRELATES_WITH** `Toxic Productivity`
- `Manager Part` **PROTECTS** `Exile Part`
- `Burnout Spiral` **TRANSFORMS_TO** `Sustainable Rhythm`
- `SELF-Energy` **ENABLES** `Witnessing Presence`

---

## 🔧 Alternative Option B: Neo4j Desktop (Local Installation)

**When to use**: You want offline access or more control

### Step 1: Download & Install (10 minutes)

1. **Download**: https://neo4j.com/download/
2. **Install** Neo4j Desktop application (~500MB)
3. **Launch** the application

### Step 2: Create Local Database (5 minutes)

1. Click **"New"** → **"Create Project"**
2. Name: `DAE-GOV`
3. Click **"Add"** → **"Local DBMS"**
4. Configure:
   - Name: `dae-gov-knowledge`
   - Password: Choose a password (remember it!)
   - Version: 5.x (latest stable)
5. Click **"Create"**
6. Click **"Start"** to start the database

### Step 3: Update Test Script

```python
# For Desktop (local):
URI = "bolt://localhost:7687"  # Standard local URI
USER = "neo4j"
PASSWORD = "your_chosen_password"  # Password from Step 2
DATABASE = "neo4j"
```

### Step 4: Run Validation

Same as Option A, Step 4 above.

---

## 🧪 Validation Checklist

After running the test script, confirm:

- [ ] ✅ Connection successful
- [ ] ✅ 16 concepts created
- [ ] ✅ 18 relationships created
- [ ] ✅ Transformation path found: Burnout Spiral → Sustainable Rhythm
- [ ] ✅ No errors in output

**If all checked**: Phase 2.3 complete! ✨

---

## 📈 Next Steps (After Validation)

**Week 1, Day 3-4**: Integration Testing
- Connect Text Orchestrator → FAISS → Neo4j
- Test end-to-end conversation processing with knowledge lookup
- File to create: `tests/test_knowledge_integration.py`

**Week 2**: Corpus Integration
- Create 30 synthetic trauma-informed conversation examples
- Build FAISS index from corpus (~1,000 text chunks)
- Test semantic retrieval

**Week 3**: Hebbian Learning
- Implement concept co-activation tracking
- Test pattern emergence with 20 conversations

See `KNOWLEDGE_INTEGRATION_ROADMAP.md` for full 4-week plan.

---

## 🆘 Troubleshooting

### Issue: "Connection refused"

**Aura**: Check database status in console, may take 1-2 min to start
**Desktop**: Make sure you clicked "Start" on the database

### Issue: "Authentication failed"

- Double-check password (case-sensitive!)
- For Aura: Use auto-generated password from credentials download
- For Desktop: Use password you set during creation

### Issue: "ImportError: No module named 'neo4j'"

```bash
python3 -m pip install neo4j
```

### Issue: "Cannot import 'neo4j_knowledge_graph'"

Make sure PYTHONPATH is set:
```bash
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1:$PYTHONPATH"
```

---

## 💰 Cost & Resources

### Neo4j Aura Free Tier

- **Cost**: $0 forever
- **Storage**: Up to 200,000 nodes (more than enough for DAE-GOV)
- **RAM**: Managed by Aura
- **Limits**: Perfect for development, may need upgrade for production scale

### Neo4j Desktop

- **Cost**: Free
- **Storage**: Limited by your disk
- **RAM**: ~2GB recommended
- **Network**: Works offline

### Current DAE-GOV Usage

- **Concepts**: 16 nodes (0.008% of Aura free tier)
- **Relationships**: 18 edges
- **Expected growth**: ~200-500 nodes after corpus integration
- **Projection**: Well within free tier for 1-2 years

---

## 📚 Useful Resources

- **Neo4j Cypher Cheat Sheet**: https://neo4j.com/docs/cypher-cheat-sheet/
- **Aura Documentation**: https://neo4j.com/docs/aura/
- **Graph Data Modeling**: https://neo4j.com/developer/guide-data-modeling/
- **Python Driver Docs**: https://neo4j.com/docs/python-manual/current/

---

## ✅ Success Criteria

**Phase 2.3 Complete When**:
1. Neo4j database running (Aura or Desktop)
2. Test script passes all 4 checks
3. Can query concepts via Neo4j Browser/Workspace
4. Knowledge graph visible and navigable

**Estimated Time**: 10-15 minutes for Aura, 15-20 minutes for Desktop

---

🌀 **Ready to build trauma-informed organizational intelligence.** 🌀

**Created**: November 10, 2025
**Phase**: 2.3 - Knowledge Infrastructure
**Next**: Integration testing (Week 1, Day 3-4)
