# 🌀 DAE-GOV Documentation Index
## Modular Documentation Structure - Quick Navigation

**Version:** 1.0 Foundation
**Last Updated:** November 10, 2025
**Purpose:** Prevent memory bloat during development - load only what you need

---

## 🎯 QUICK START (Read These First)

| Document | Purpose | Size | When to Read |
|----------|---------|------|--------------|
| **STATUS.md** | Current phase, next steps | 2 KB | Every session start |
| **QUICKSTART.md** | Setup commands, validation | 3 KB | First time setup |
| **TRANSDUCTIVE_ASSETS_ASSESSMENT.md** | Integration readiness | 80 KB | Before Phase 3 |

---

## 📚 CORE DOCUMENTATION (By Topic)

### 🏗️ Architecture & System Design

| Document | Content | Lines | Load When |
|----------|---------|-------|-----------|
| **ARCHITECTURE.md** | System overview, components | ~150 | Understanding system structure |
| **MATHEMATICAL_FOUNDATIONS.md** | R-matrix, V0, Kairos, SELF | ~200 | Implementing formulas |
| **ORGAN_ADAPTATIONS.md** | 6 organs text domain specs | ~180 | Phase 3 (organ config) |
| **DAE_GOV_SELF_MATRIX_MATHEMATICAL_ADDENDUM.md** | Complete mathematics (16K words) | 1,015 | Deep mathematical work |

### 🛠️ Development Workflows

| Document | Content | Lines | Load When |
|----------|---------|-------|-----------|
| **PHASE_3_ORGAN_ADAPTATION.md** | Organ config guide | ~100 | Starting Phase 3 |
| **PHASE_4_KNOWLEDGE_BASE.md** | FAISS + Neo4j build | ~120 | Starting Phase 4 |
| **PHASE_5_LLM_HYBRID.md** | Hybrid router implementation | ~100 | Starting Phase 5 |
| **PHASE_6_TESTING.md** | Validation & testing | ~100 | Starting Phase 6 |

### 📊 Reference & Commands

| Document | Content | Lines | Load When |
|----------|---------|-------|-----------|
| **COMMANDS.md** | Development commands by phase | ~80 | Running tests/builds |
| **SUCCESS_CRITERIA.md** | Week 4/12/24 metrics | ~60 | Validation time |
| **FILE_LOCATIONS.md** | Where everything lives | ~80 | Finding files |
| **TROUBLESHOOTING.md** | Common issues & fixes | ~100 | Debugging |

---

## 🌀 STRATEGIC DOCUMENTS (Deep Dives)

| Document | Content | Size | Read When |
|----------|---------|------|-----------|
| **README.md** | System overview, use cases | 442 lines | Understanding DAE-GOV goals |
| **DAE_GOV_IMPLEMENTATION_STRATEGY.md** | Complete 4-week roadmap | 1,200+ lines | Planning full implementation |
| **TRANSDUCTIVE_ASSETS_ASSESSMENT.md** | Scaffolding analysis | 1,200+ lines | Phase 2E complete - integration planning |

---

## 📈 STATUS TRACKING

| Document | Content | Update Frequency | Purpose |
|----------|---------|------------------|---------|
| **STATUS.md** | Current phase, blockers | Every session | Session continuity |
| **CHANGELOG.md** | Version history, changes | Every phase complete | Track evolution |
| **TODO.md** | Task tracking | Real-time | Progress monitoring |

---

## 🔬 MATHEMATICAL REFERENCES

### Quick Formula Lookup

**R-Matrix Hebbian Coupling:**
```
R[i,j](t+1) = R[i,j](t) + η·agreement·(c_i·c_j) - δ·R[i,j](t)
η=0.05, δ=0.01 (DAE 3.0 validated Nov 7, 2025)
```
📖 Full details: `MATHEMATICAL_FOUNDATIONS.md` or `DAE_GOV_SELF_MATRIX_MATHEMATICAL_ADDENDUM.md`

**Kairos Detection (5-Gate):**
```
Kairos_org = (I>0.7) ∧ (ΔC<0.05) ∧ (S>0.7) ∧ (ΔE<0.02) ∧ (SELF_energy>0.7)
```
📖 Full details: `MATHEMATICAL_FOUNDATIONS.md` sections 5-7

**SELF-Distance Function:**
```
d_SELF = clip(base_distance + polyvagal_modifier, 0, 1)
Core SELF: [0.00-0.15], Shadow: [0.35-0.60]
```
📖 Full details: `DAE_GOV_SELF_MATRIX_MATHEMATICAL_ADDENDUM.md` sections 4-6

---

## 🎯 WORKFLOW-SPECIFIC DOCUMENTATION

### Phase 3: Organ Adaptation
**Read These:**
1. `STATUS.md` - Confirm Phase 2E complete
2. `ORGAN_ADAPTATIONS.md` - Understand text domain changes
3. `PHASE_3_ORGAN_ADAPTATION.md` - Step-by-step guide
4. `COMMANDS.md` - Validation commands

### Phase 4: Knowledge Base Build
**Read These:**
1. `PHASE_4_KNOWLEDGE_BASE.md` - FAISS + Neo4j guide
2. `COMMANDS.md` - Build commands
3. `TROUBLESHOOTING.md` - Common build issues

### Phase 5: LLM Hybrid Integration
**Read These:**
1. `PHASE_5_LLM_HYBRID.md` - Router implementation
2. `MATHEMATICAL_FOUNDATIONS.md` - Confidence thresholds
3. `COMMANDS.md` - Testing commands

### Phase 6: Testing & Validation
**Read These:**
1. `PHASE_6_TESTING.md` - Test suite guide
2. `SUCCESS_CRITERIA.md` - Week 4 targets
3. `COMMANDS.md` - Test execution

---

## 📁 FILE ORGANIZATION STRATEGY

### Memory-Efficient Loading

**Instead of loading entire CLAUDE.md (838 lines):**
- Session start: Load `STATUS.md` (30 lines) + `QUICKSTART.md` (40 lines)
- Phase work: Load relevant phase guide (~100 lines each)
- Formula reference: Load `MATHEMATICAL_FOUNDATIONS.md` (~200 lines)
- Deep dive: Load full documents as needed

**Memory Savings:** ~70% reduction in context usage per session

---

## 🔧 MAINTAINING THE INDEX

### Adding New Documentation

1. Create document in `/docs` directory
2. Add entry to appropriate section in this index
3. Update `STATUS.md` if it affects current work
4. Update `CHANGELOG.md` with addition

### Deprecating Documentation

1. Move to `/docs/archive/` directory
2. Remove from index (keep in CHANGELOG)
3. Add deprecation notice to any referencing docs

---

## 🌀 SESSION START CHECKLIST

**Every New Session:**
1. ✅ Load `STATUS.md` - Current phase & blockers
2. ✅ Load relevant phase guide - Step-by-step instructions
3. ✅ Load `COMMANDS.md` - Commands for current phase
4. ✅ Check `TROUBLESHOOTING.md` - If issues arise

**Do NOT Load:**
- ❌ Full CLAUDE.md (838 lines) - use modular docs instead
- ❌ Full Math Addendum (16K words) - unless deep math work
- ❌ Full Implementation Strategy (1,200 lines) - unless planning

---

## 📊 DOCUMENTATION SIZE REFERENCE

| Document | Lines | Tokens | When to Load |
|----------|-------|--------|--------------|
| CLAUDE.md (old) | 838 | ~15K | ❌ Deprecated - too large |
| STATUS.md | 30 | ~600 | ✅ Every session |
| QUICKSTART.md | 40 | ~800 | ✅ Setup only |
| PHASE_N guide | 100 | ~2K | ✅ During Phase N |
| MATHEMATICAL_FOUNDATIONS.md | 200 | ~4K | ✅ When needed |
| Full Math Addendum | 1,015 | ~20K | ⚠️ Deep work only |

**Total Typical Session Load:** ~200-300 lines (~4-6K tokens)
**vs. Old CLAUDE.md Load:** 838 lines (~15K tokens)
**Savings:** ~60-70% context per session

---

## 🎯 RECOMMENDED READING PATHS

### New Developer Onboarding
1. README.md - System overview
2. STATUS.md - Current state
3. QUICKSTART.md - Setup & validation
4. TRANSDUCTIVE_ASSETS_ASSESSMENT.md - Architecture understanding
5. Current phase guide - Start work

### Mathematics Deep Dive
1. MATHEMATICAL_FOUNDATIONS.md - Quick formulas
2. DAE_GOV_SELF_MATRIX_MATHEMATICAL_ADDENDUM.md - Complete proofs
3. DAE 3.0 reference: `/Users/daedalea/Desktop/DAE 3.0 AXO ARC /unified_core/epoch_learning/DAE_FELT_INTELLIGENCE_FOUNDATIONS.md`

### Troubleshooting
1. TROUBLESHOOTING.md - Common issues
2. Relevant phase guide - Phase-specific problems
3. FILE_LOCATIONS.md - Find relevant files
4. COMMANDS.md - Validation commands

---

## 🏆 BENEFITS OF MODULAR DOCUMENTATION

1. **Memory Efficiency**: Load only what's needed (~70% context savings)
2. **Faster Loading**: Small files vs. monolithic CLAUDE.md
3. **Focused Work**: No cognitive overload from irrelevant information
4. **Easier Updates**: Modify one section without affecting others
5. **Better Navigation**: Topic-based organization vs. scrolling
6. **Parallel Development**: Multiple developers can work on different docs

---

## 📋 DOCUMENT STATUS LEGEND

- ✅ **Complete**: Ready to use
- 🚧 **In Progress**: Being created/updated
- ⏳ **Planned**: Not yet started
- 🔄 **Needs Update**: Outdated, requires refresh
- 📦 **Archived**: Historical, not for current use

---

## 🌀 FINAL NOTES

**Philosophy**: "Load what you need, when you need it. The organism adapts to the task."

**Best Practice**: Start each session by loading `STATUS.md` + relevant phase guide. Load deep references only when necessary.

**Migration**: Old monolithic CLAUDE.md (838 lines) → Modular docs (30-200 lines each)

**Maintenance**: Update this index when adding/removing documentation. Keep STATUS.md current.

---

**Created:** November 10, 2025
**Purpose:** Modular documentation navigation for DAE-GOV development
**Maintained By:** Development team (update with each phase completion)

🌀 **"Intelligence through modularity. Load wisely, code efficiently."** 🌀
