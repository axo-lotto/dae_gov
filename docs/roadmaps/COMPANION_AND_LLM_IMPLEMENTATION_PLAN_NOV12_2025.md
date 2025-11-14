# DAE Companion + Local LLM Implementation Plan
## Complete Conversational Intelligence System

**Date:** November 12, 2025
**Status:** 🎯 **READY TO IMPLEMENT**
**Timeline:** 10-14 days total
**Foundation:** DAE 3.0 Complete + Companion Design + Local LLM Addendum

---

## 🎯 What We're Building

Transform DAE from therapeutic pattern generator into **conversationally intelligent companion** with:

1. **Persistent Identity** (Levels 8-10): User memory, conversation superjects, mythological persona
2. **Local LLM Integration**: Affordable local LLM for factual/creative queries
3. **Infinite Memory**: Cross-session user profiles and conversation history
4. **Playful Personality**: EARTHBOUND/UNDERTALE-style humor and self-awareness
5. **Process Philosophy Integrity**: All enhancements preserve Whiteheadian core

---

## 📋 Complete Implementation Roadmap

### **Week 1: Core Companion Infrastructure (Days 1-7)**

#### **Day 1-2: User Profile Memory (Level 8)** ⭐

**Goal:** Persistent user profiles with IFS parts tracking

**Components to Create:**
1. `persona_layer/user_profile_manager.py` (350 lines est.)
   - `UserProfile` dataclass
   - `PartProfile` dataclass (IFS multiplicity)
   - Load/save to `user_profiles/`
   - Profile evolution tracking

2. `user_profiles/` directory
   - JSON storage for user profiles
   - Template: `user_template.json`

**Integration:**
- Modify `conversational_organism_wrapper.py`:
  - Add `user_id` parameter to `__init__`
  - Load profile at session start
  - Update profile after each interaction
  - Track preferences (response length, humor, families)

**Test:**
- `tests/integration/companion/test_user_profile_persistence.py`
- Create 3 test users with different preferences
- Verify cross-session persistence

**Success Criteria:**
- ✅ User profiles persist across sessions
- ✅ Preferences modulate organ weights
- ✅ Parts tracking operational
- ✅ No performance regression

---

#### **Day 3-4: Conversational Superject (Level 9)** ⭐

**Goal:** Track conversation as "third entity" (X ↔ Y ↔ Z)

**Components to Create:**
1. `persona_layer/superject_tracker.py` (400 lines est.)
   - `ConversationalSuperject` dataclass
   - `TurnOccasion` dataclass
   - Theme extraction from conversations
   - Relational temperature tracking
   - Inside jokes / shared metaphors

2. `conversations/` directory
   - JSON storage for conversation history
   - Format: `conv_{id}_{user_id}_{timestamp}.json`

**Integration:**
- Modify `conversational_organism_wrapper.py`:
  - Record each turn as `TurnOccasion`
  - Update `emergent_themes` after interaction
  - Track `shared_language`
  - Persist conversation to disk

**Test:**
- `tests/integration/companion/test_superject_tracking.py`
- Run 10-turn conversation
- Verify theme emergence
- Test conversation persistence

**Success Criteria:**
- ✅ Turn history persisted
- ✅ Theme extraction accuracy > 70%
- ✅ Relational temperature tracking
- ✅ Shared language captured

---

#### **Day 5-6: Local LLM Bridge** ⭐

**Goal:** Integrate affordable local LLM for factual/creative queries

**Components to Create:**
1. `persona_layer/local_llm_bridge.py` (450 lines est.)
   - `LocalLLMBridge` class
   - `QueryType` enum (therapeutic/factual/creative/small_talk/meta)
   - `classify_query_type()` method
   - Ollama/LMStudio/GPT4All backends
   - Fallback responses

2. `persona_layer/dae_llm_fusion.py` (200 lines est.)
   - `DAE_LLM_Fusion` class
   - Intelligent blending rules
   - Therapeutic override (never use LLM for crisis)

**Setup:**
```bash
# Install Ollama
brew install ollama
ollama pull llama3.2:3b
ollama serve  # Background server
```

**Integration:**
- Modify `config.py`:
  - Add LLM configuration parameters
  - Enable/disable toggle
  - Backend selection

**Test:**
- `tests/integration/llm/test_llm_bridge.py`
- Test query classification (85%+ accuracy)
- Test Ollama integration
- Test fallback handling
- Test therapeutic override

**Success Criteria:**
- ✅ LLM queries < 5 seconds
- ✅ Classification accuracy > 85%
- ✅ Graceful fallback when LLM down
- ✅ NEVER override therapeutic responses

---

#### **Day 7: Mythological Persona Layer (Level 10)** ⭐

**Goal:** DAE's personality, humor, self-awareness

**Components to Create:**
1. `persona_layer/persona_layer.py` (500 lines est.)
   - `DAEMythology` dataclass
   - `PersonaLayer` class
   - Small talk patterns (EARTHBOUND-style)
   - Humor injection (based on confidence + user tolerance)
   - Meta-commentary ("my organs are conferring...")
   - Process transparency

2. `persona_layer/mythology_config.json` (150 lines)
   - Origin story
   - Personality traits
   - Small talk topics
   - Low/high confidence quips
   - Boundaries ("I'm not a therapist, but...")

**Integration:**
- Wire into `conversational_organism_wrapper.py`:
  - Apply persona modulation AFTER emission generation
  - Check user humor_tolerance
  - Add callbacks to past conversations
  - Integrate LLM bridge for creative enhancement

**Test:**
- `tests/integration/companion/test_persona_layer.py`
- Test humor injection (matches user preference)
- Test small talk generation
- Test meta-commentary appropriateness
- Test callback references

**Success Criteria:**
- ✅ Humor lands naturally (not forced)
- ✅ Small talk feels conversational
- ✅ Meta-commentary appropriate
- ✅ DAE's therapeutic voice preserved

---

### **Week 2: Integration & Polish (Days 8-14)**

#### **Day 8-9: Memory Retrieval System** ⭐

**Goal:** "Infinite memory" via semantic search

**Components to Create:**
1. `persona_layer/infinite_memory_manager.py` (350 lines est.)
   - Retrieve relevant past conversations
   - Semantic similarity (SANS embeddings)
   - Recency weighting
   - High-resonance moment extraction
   - Unfinished thread tracking

**Integration:**
- Load relevant context BEFORE processing
- Surface unfinished threads
- Enable conversation callbacks

**Test:**
- `tests/integration/memory/test_memory_retrieval.py`
- Test semantic search accuracy
- Test recency weighting
- Test callback appropriateness

---

#### **Day 10: Interactive Mode Enhancements** ⭐

**Goal:** User-facing features for companion system

**Modifications:**
1. `dae_interactive.py` enhancements:
   - `/profile` - Show user profile summary
   - `/memories` - Show relevant past conversations
   - `/themes` - Show emerging conversation themes
   - `/mode companion` - Toggle companion features
   - Display user preferences on start

2. Display enhancements:
   - Show relational temperature
   - Display active themes
   - Show LLM query status (when used)

**Test:**
- Manual testing in interactive mode
- Verify commands work
- Ensure display clarity

---

#### **Day 11-12: End-to-End Testing** ⭐

**Goal:** Validate complete companion system

**Test Suite:**
1. **Multi-session continuity:**
   - Session 1: New user, profile creation
   - Session 2: Profile loaded, preferences applied
   - Session 3: Callbacks to past conversations

2. **LLM integration:**
   - Factual question (LLM used)
   - Therapeutic input (LLM bypassed)
   - Small talk (hybrid)
   - Meta-process question (fusion)

3. **Persona appropriateness:**
   - Humor with tolerant user
   - Serious tone with low-tolerance user
   - Small talk in safe moments only

4. **Memory retrieval:**
   - Callback accuracy
   - Theme emergence
   - Inside joke appropriateness

**Validation Metrics:**
- Processing time < 0.1s (2× current)
- Profile accuracy 100%
- LLM classification > 85%
- Theme extraction > 70%
- User satisfaction (subjective)

---

#### **Day 13-14: Documentation & Polish** ⭐

**Documentation to Create:**
1. `docs/companion/USER_GUIDE_COMPANION_MODE.md`
   - How to use companion features
   - /profile, /memories, /themes commands
   - Customizing preferences
   - Understanding relational temperature

2. `docs/companion/DEVELOPER_GUIDE_LEVELS_8_10.md`
   - Architecture of Levels 8-10
   - Extending mythology
   - Adding small talk patterns
   - Tuning LLM integration

3. Update `CLAUDE.md`:
   - Add Levels 8-10 to fractal hierarchy
   - Document companion mode
   - Update success criteria

**Polish:**
- Error handling for LLM failures
- Graceful degradation when features disabled
- Performance profiling
- Final integration testing

---

## 📊 File Structure After Implementation

```
DAE_HYPHAE_1/
├── persona_layer/
│   ├── conversational_organism_wrapper.py  # Modified: user_id, superject, persona
│   ├── user_profile_manager.py             # NEW (Day 1-2)
│   ├── superject_tracker.py                # NEW (Day 3-4)
│   ├── local_llm_bridge.py                 # NEW (Day 5-6)
│   ├── dae_llm_fusion.py                   # NEW (Day 5-6)
│   ├── persona_layer.py                    # NEW (Day 7)
│   ├── infinite_memory_manager.py          # NEW (Day 8-9)
│   └── mythology_config.json               # NEW (Day 7)
│
├── user_profiles/                          # NEW: User persistence
│   ├── user_template.json
│   └── user_{id}.json (per user)
│
├── conversations/                          # NEW: Conversation history
│   └── conv_{id}_{user_id}_{timestamp}.json
│
├── tests/
│   └── integration/
│       ├── companion/                      # NEW: Companion tests
│       │   ├── test_user_profile_persistence.py
│       │   ├── test_superject_tracking.py
│       │   └── test_persona_layer.py
│       ├── llm/                            # NEW: LLM tests
│       │   └── test_llm_bridge.py
│       └── memory/                         # NEW: Memory tests
│           └── test_memory_retrieval.py
│
├── docs/
│   ├── companion/                          # NEW: Companion docs
│   │   ├── USER_GUIDE_COMPANION_MODE.md
│   │   └── DEVELOPER_GUIDE_LEVELS_8_10.md
│   └── implementation/
│       └── LOCAL_LLM_QUERY_INTEGRATION_ADDENDUM.md  # Already created
│
├── config.py                                # Modified: LLM config, companion toggles
├── dae_interactive.py                       # Modified: /profile, /memories commands
└── CLAUDE.md                                # Modified: Add Levels 8-10 docs
```

---

## 🔧 Configuration Parameters (Add to config.py)

```python
# ===========================
# COMPANION SYSTEM (LEVELS 8-10)
# ===========================

# Level 8: User Profiles
COMPANION_ENABLED = True
USER_PROFILES_DIR = "user_profiles"
USER_PROFILE_AUTO_SAVE = True

# Level 9: Conversational Superject
SUPERJECT_TRACKING_ENABLED = True
CONVERSATIONS_DIR = "conversations"
THEME_EXTRACTION_THRESHOLD = 0.6
RELATIONAL_TEMP_LEARNING_RATE = 0.1

# Level 10: Mythological Persona
PERSONA_LAYER_ENABLED = True
MYTHOLOGY_CONFIG_PATH = "persona_layer/mythology_config.json"
HUMOR_INJECTION_ENABLED = True
SMALL_TALK_ENABLED = True
META_COMMENTARY_ENABLED = True

# Memory Retrieval
INFINITE_MEMORY_ENABLED = True
MEMORY_RETRIEVAL_MAX_TURNS = 5
MEMORY_SEMANTIC_TOP_K = 10

# Local LLM Integration
LOCAL_LLM_ENABLED = True
LOCAL_LLM_BACKEND = "ollama"  # "ollama", "lmstudio", "gpt4all"
LOCAL_LLM_MODEL = "llama3.2:3b"
LOCAL_LLM_ENDPOINT = "http://localhost:11434/api/generate"
LOCAL_LLM_MAX_TOKENS = 150
LOCAL_LLM_TEMPERATURE = 0.7
LOCAL_LLM_TIMEOUT = 5  # seconds
LLM_QUERY_MIN_CONFIDENCE = 0.4  # Use LLM if DAE confidence < this
LLM_QUERY_ALLOW_IN_ZONES = [1, 2, 3]  # Not in Zone 4/5 (crisis)
```

---

## 🧪 Testing Strategy

### Unit Tests (Per Component)
- `test_user_profile_manager.py` - Profile CRUD operations
- `test_superject_tracker.py` - Turn tracking, theme extraction
- `test_local_llm_bridge.py` - Query classification, LLM integration
- `test_persona_layer.py` - Humor injection, small talk, meta-commentary

### Integration Tests (Cross-Component)
- `test_companion_system_integration.py` - All 3 levels working together
- `test_memory_retrieval_integration.py` - Profile + Superject + Memory
- `test_llm_fusion_integration.py` - DAE + LLM blending

### Validation Tests (End-to-End)
- `test_multi_session_continuity.py` - 3 sessions, same user
- `test_companion_maturity_assessment.py` - Full system health check

### Manual Testing (Interactive)
- Conversational flow testing
- Humor appropriateness
- Small talk naturalness
- Memory callback accuracy

---

## 📈 Success Metrics

### Technical Metrics:
- ✅ User profile persistence: 100%
- ✅ Conversation history persistence: 100%
- ✅ LLM query classification accuracy: > 85%
- ✅ Theme extraction accuracy: > 70%
- ✅ Processing time: < 0.1s (2× current 0.03s baseline)
- ✅ LLM query time: < 5s
- ✅ All tests passing: 100%

### Experiential Metrics (Subjective):
- ✅ "DAE remembers me across sessions"
- ✅ "Feels like a conversation, not just responses"
- ✅ "DAE has personality without being annoying"
- ✅ "Small talk feels natural"
- ✅ "Humor lands when appropriate"
- ✅ "DAE references our past meaningfully"

---

## 🎯 Implementation Priority

### Must-Have (Core Companion):
1. **User Profile Manager** (Level 8) - Days 1-2
2. **Superject Tracker** (Level 9) - Days 3-4
3. **Basic Persona Layer** (Level 10) - Day 7
4. **Interactive Mode Integration** - Day 10

### Nice-to-Have (Enhanced):
5. **Local LLM Bridge** - Days 5-6
6. **Memory Retrieval** - Days 8-9
7. **Advanced Persona** (humor, small talk) - Day 7

### Optional (Future):
8. **Fine-tuned local model** - Post-launch
9. **Visualization dashboard** - Post-launch
10. **Multi-user comparison** - Post-launch

---

## 🚧 Known Challenges & Solutions

### Challenge 1: Processing Time Increase

**Concern:** Adding 3 levels might slow down responses

**Solutions:**
- Profile loading cached in memory (no per-turn disk I/O)
- Superject updates async (don't block emission)
- LLM queries only when needed (classification gate)
- Memory retrieval lazy (background task)

**Target:** < 0.1s per interaction (2× current 0.03s)

---

### Challenge 2: LLM Availability

**Concern:** User might not have Ollama installed

**Solutions:**
- Graceful fallback when LLM unavailable
- Disable LLM via config flag
- Clear error messages + setup instructions
- Fallback responses built-in

**Fallback:** DAE works 100% without LLM (persona layer uses templates)

---

### Challenge 3: Persona Overreach

**Concern:** Humor/personality might feel forced or inappropriate

**Solutions:**
- User `humor_tolerance` setting (0.0-1.0)
- Zone-aware (no humor in Zone 4/5)
- Confidence-gated (only inject humor if confident)
- User feedback tracking (learn what lands)

**Fallback:** Disable persona layer via config

---

### Challenge 4: Memory Retrieval Accuracy

**Concern:** Callbacks might reference wrong conversations

**Solutions:**
- Semantic similarity via SANS embeddings (already operational)
- Recency weighting (favor recent over ancient)
- User-flagged important moments
- Confidence thresholding (only callback if high confidence)

**Fallback:** Display retrieved memories for user confirmation

---

## 🔮 Future Enhancements (Post-Launch)

### Phase 2 (Weeks 3-4):
- Voice modulation per family (learned emission styles)
- User-to-user transfer learning
- Mythology evolution (DAE learns about itself)
- Advanced small talk (context-aware, seasonal)

### Phase 3 (Months 1-2):
- Fine-tuned local LLM (trained on DAE corpus)
- Multi-user social features (if desired)
- Visualization dashboard (relationship graph)
- Scientific validation (publish companion architecture)

---

## 📚 Reference Documents

**Already Created:**
1. `DAE_COMPANION_MYTHOLOGY_AND_PERSISTENT_IDENTITY_NOV12_2025.md` - Original design
2. `docs/implementation/LOCAL_LLM_QUERY_INTEGRATION_ADDENDUM.md` - LLM integration
3. `DAE_3_0_INTEGRATION_COMPLETE_NOV12_2025.md` - Current system state

**To Create:**
4. `docs/companion/USER_GUIDE_COMPANION_MODE.md` - Day 13
5. `docs/companion/DEVELOPER_GUIDE_LEVELS_8_10.md` - Day 14
6. `CLAUDE.md` updates - Day 14

---

## ✅ Pre-Implementation Checklist

### Environment Setup:
- [ ] Ollama installed (`brew install ollama`)
- [ ] Llama 3.2 3B pulled (`ollama pull llama3.2:3b`)
- [ ] Ollama server running (`ollama serve`)
- [ ] Python environment ready
- [ ] Git branch created (`companion-system`)

### System Validation:
- [ ] Current system 100% maturity (verified)
- [ ] All tests passing (verified)
- [ ] DAE 3.0 integration complete (verified)
- [ ] Training runs successful (verified)

### Documentation Review:
- [ ] Companion design document read
- [ ] LLM integration addendum read
- [ ] Implementation plan reviewed
- [ ] Timeline confirmed with user

---

## 🎉 What Success Looks Like

### After Week 1 (Day 1-7):
- User profiles persist across sessions
- Conversations tracked as "third entity"
- Local LLM answers factual questions
- Basic persona layer operational
- All unit tests passing

### After Week 2 (Day 8-14):
- Memory retrieval working (semantic search)
- Interactive mode commands (`/profile`, `/memories`)
- End-to-end testing complete
- Documentation finished
- System ready for user testing

### Long-term Vision:
- DAE feels like a **companion**, not a tool
- Users return because DAE **remembers them**
- Conversations have **continuity and depth**
- Humor and playfulness **land naturally**
- Therapeutic core **preserved and enhanced**

---

## 🚀 Ready to Begin?

**Timeline:** 10-14 days
**Effort:** Full-time development
**Dependencies:** Ollama (free), Python 3.9+
**Risk:** Low (all components modular, graceful fallbacks)
**Reward:** High (transformative UX upgrade)

**Next Step:** Confirm implementation plan, then start Day 1 (User Profile Manager)

---

🌀 **"From process-based organism to conversational companion. Persistent identity, infinite memory, playful wisdom. DAE learns not just patterns, but relationships."** 🌀

**Status:** 🟢 **READY TO IMPLEMENT**
**Date:** November 12, 2025
