# User Identity & Personalization Investigation
**Date:** November 14, 2025  
**Objective:** Assess current user identity system and identify gaps for name-aware, personalized conversations

---

## Executive Summary

**Current State:** DAE_HYPHAE_1 has **robust user identity infrastructure** but **username is not passed to LLM prompts**, resulting in impersonal responses that don't use the user's name.

**Quick Fix Available:** Yes - username can be passed through existing flow with minimal changes.

**Graph Database Needed:** No - current JSON-based system is sufficient for Phase 1. Neo4j exists but is not actively used.

---

## 1. Current User Identity Infrastructure

### ✅ What Exists (Strong Foundation)

#### 1.1 User Registry System (`persona_layer/user_registry.py`)
**Status:** Production-ready, actively used

**Features:**
- User creation with persistent IDs (`user_YYYYMMDD_HHMMSS`)
- Username storage (human-readable name)
- Session history tracking
- Feedback statistics (helpful_rate, excellent_rate)
- Per-user state files (JSON)
- Organic family membership tracking

**Example User:**
```json
{
  "user_id": "user_20251113_143117",
  "username": "Emi",
  "created_at": "2025-11-13T14:31:17.336687",
  "total_sessions": 7,
  "total_turns": 32,
  "preferred_tone": "balanced",
  "session_history": [...],
  "organic_family_membership": []
}
```

**File Locations:**
- Registry: `persona_layer/user_registry.json`
- User states: `persona_layer/users/{user_id}_state.json`

#### 1.2 User Profile Manager (`persona_layer/user_profile_manager.py`)
**Status:** Advanced, feature-rich (Levels 8-10 Companion Integration)

**Capabilities:**
- User preferences (response_length, humor_tolerance, small_talk_openness)
- LLM usage consent tracking
- Template preference learning (Phase 2)
- Family affinity tracking (Phase 3)
- Inside jokes and recurring themes (Level 9)
- Conversation history per session

**User Profile Structure:**
```python
@dataclass
class UserProfile:
    user_id: str
    created_at: str
    last_active: str
    
    # Preferences
    response_length_preference: str  # "minimal", "moderate", "comprehensive"
    humor_tolerance: float  # 0.0 to 1.0
    small_talk_openness: float
    
    # LLM consent
    llm_usage_consent: bool
    
    # Relationship metadata
    total_conversations: int
    total_turns: int
    
    # Learning (Phase 2-3)
    favorite_templates: Dict[str, List[str]]
    template_success_rates: Dict[str, float]
    family_affinities: Dict[str, float]
    
    # Level 9: Inside jokes and callbacks
    inside_jokes: List[Dict[str, Any]]
    recurring_themes: Dict[str, int]
```

**Methods:**
- `get_or_create_profile(user_id)` - Load or create user
- `save_conversation_turn(user_id, session_id, turn)` - Save history
- `get_conversation_history(user_id, max_turns=10)` - Retrieve context
- `update_template_success(user_id, template_id, success)` - Learning
- `add_inside_joke(user_id, joke_text, context)` - Relationship memory

#### 1.3 User Superject Learner (`persona_layer/user_superject_learner.py`)
**Status:** Advanced (Phase 1 complete, Hybrid Week 1 integration)

**Purpose:** Passive and active learning from user's accumulated felt-state trajectory

**Three Learning Modes:**
1. **Passive (instant):** Every conversation turn updates superject
2. **Mini-epoch (every 10 turns):** Learn transformation patterns
3. **Global epoch (every 100 turns):** Aggregate universal patterns

**What It Tracks:**
- 57D organ signatures per turn
- Zone/polyvagal state transitions
- V0 energy descent patterns
- Transformation patterns (what works for THIS user)
- Heckling trajectory (banter unlock)
- Salience patterns (trauma markers, crisis escalation)
- Humor calibration
- Tone preferences per zone

**Example Learned Pattern:**
```python
TransformationPattern(
    pattern_id="zone3_to_zone1_sympathetic_to_ventral",
    from_zone=3, from_polyvagal="sympathetic",
    to_zone=1, to_polyvagal="ventral_vagal",
    successful_organs=["PRESENCE", "EMPATHY", "somatic_wisdom"],
    successful_transduction="parasympathetic_settling",
    humor_safe=True,
    tone="gentle",
    preferred_length="moderate"
)
```

#### 1.4 User Instantiation Manager (`memory/user_instantiation_manager.py`)
**Status:** Multi-tier memory architecture (Tier 1-3)

**Purpose:** Create unique DAE instantiations for each human

**Architecture:**
- **TIER 1:** Session-specific state (ephemeral)
- **TIER 2:** User-specific full memory (persistent)
- **TIER 3:** Global organism memory (shared)

**Per-User Bundle Directory:**
```
Bundle/user_{token}/
├── user_state.json
├── traces/
├── transformation_patterns.json
├── epoch_training_log.json
├── user_hebbian_memory.json
├── identity_trajectory.json
└── neo4j_subgraph_export.json  # Reserved for future
```

**Active Users in Bundle:**
- `Link` (user_link_20251111_e8936e) - 5 sessions
- `Emi` (user_20251113_143117) - 7 sessions, 32 turns
- `Jason`, `Alice`, `Joe`, etc.

#### 1.5 Interactive Session (`dae_interactive.py`)
**Status:** Production-ready, user login fully implemented

**User Flow:**
1. Launch: `python3 dae_interactive.py`
2. User identification:
   - New user → Enter username
   - Existing user → Select from list or enter user_id
3. Session begins with user context loaded
4. Feedback collection per turn (optional)
5. Session saved on exit

**What Gets Loaded:**
```python
self.user = self.user_registry.get_user(user_id)
self.user_state = self.user_registry.load_user_state(user_id)

# User info displayed:
# ✅ Logged in as: Emi
#    User ID: user_20251113_143117
#    Total sessions: 7
#    Total turns: 32
#    Helpful rate: 85.0% (15 ratings)
```

### ❌ What's Missing (The Gap)

#### 1.6 Username NOT Passed to Emission Generation

**The Problem:** Username is captured and stored, but NOT passed to LLM prompt builder.

**Current Flow:**
```
User Login (username="Emi")
   ↓
User Registry (stores "Emi")
   ↓
Interactive Session (loads user profile)
   ↓
organism.process_text(user_input, context={...})  ❌ NO USERNAME
   ↓
emission_generator.generate_emissions(...)  ❌ NO USERNAME
   ↓
felt_guided_llm.build_felt_prompt(user_input, ...)  ❌ NO USERNAME
   ↓
LLM prompt: "You are responding as a felt-intelligent companion organism."
   (No personalization, no user name!)
```

**Evidence:**

**File:** `persona_layer/llm_felt_guidance.py`, Line 341-442
```python
def build_felt_prompt(
    self,
    user_input: str,
    constraints: LLMConstraints,
    lures: FeltLures,
    memory_context: Optional[List[Dict]] = None,
    organism_narrative: Optional[str] = None
) -> str:
    # Base instruction (minimal - let felt constraints guide)
    prompt = "You are responding as a felt-intelligent companion organism.\n\n"
    
    # Felt state context (EMERGENT, not template)
    prompt += f"Current felt state:\n"
    prompt += f"- Tone: {constraints.tone}\n"
    # ... more felt states ...
    
    # User input
    prompt += f"\n---\nUser: {user_input}\n\n"  # ❌ NOT "Emi: {user_input}"
    
    # Generation instruction
    prompt += f"Respond with {constraints.tone} tone, ..."
    # ❌ NOT "Respond to Emi with..."
```

**File:** `dae_interactive.py`, Line 246-268
```python
def process_input(self, user_input: str) -> dict:
    context = {
        'session_id': self.session_id,
        'timestamp': datetime.now().isoformat(),
        'turn': len(self.conversation_history) + 1
        # ❌ NO 'username': self.user['username']
    }
    
    result = self.organism.process_text(
        user_input,
        context=context,  # ❌ Context has no username
        enable_tsk_recording=self.enable_tsk_recording,
        enable_phase2=self.enable_phase2
    )
```

**File:** `persona_layer/conversational_organism_wrapper.py`, Line 554-563
```python
def process_text(
    self,
    text: str,
    context: Optional[Dict[str, Any]] = None,
    enable_tsk_recording: bool = True,
    enable_phase2: bool = False,
    regime: Optional[SatisfactionRegime] = None,
    user_id: Optional[str] = None,  # ✅ HAS user_id
    user_satisfaction: Optional[float] = None
) -> Dict[str, Any]:
    # ... processes text ...
    # ❌ BUT user_id is ONLY used for superject learning, NOT for emission
```

**File:** `persona_layer/emission_generator.py`, Line 907-917
```python
def generate_emissions(
    self,
    nexuses: List,
    num_emissions: int = 3,
    prefer_variety: bool = True,
    user_input: str = "",  # ✅ HAS user_input
    organ_results: Dict = None,
    v0_energy: float = 1.0,
    satisfaction: float = 0.0,
    memory_context: Optional[List[Dict]] = None
    # ❌ NO username parameter
) -> List[EmittedPhrase]:
```

---

## 2. Existing Graph/Relationship Infrastructure

### 2.1 Neo4j Knowledge Graph (`knowledge_base/neo4j_knowledge_graph.py`)
**Status:** Implemented but NOT actively used

**Purpose:** Trauma-informed concept relationships for organizational consulting

**Features:**
- Concept nodes (trauma_informed, process_philosophy, organizational)
- Relationship edges (ENABLES, REQUIRES, TRANSFORMS_TO, CORRELATES_WITH)
- Multi-hop traversal
- Pattern-based querying

**Connection Details:**
```python
uri = "neo4j+s://f63b4064.databases.neo4j.io"
user = "neo4j"
database = "neo4j"
```

**Current Usage:** NONE in production. Only test files reference it.

**Per-User Neo4j Export:**
- Each user bundle has `neo4j_subgraph_export.json` reserved
- But NOT actively populated

### 2.2 JSON-Based Relationship Tracking (Active)

#### Organic Families (`persona_layer/organic_families.json`)
**Status:** Actively used for family-based learning

**Structure:**
```json
{
  "family_0": {
    "family_id": "family_0",
    "created_at": "...",
    "member_count": 5,
    "centroid_signature": [57D vector],
    "representative_conversations": [...],
    "dominant_nexus_types": ["witnessing_presence", "trauma_holding"],
    "polyvagal_profile": {
      "ventral_vagal": 0.7,
      "sympathetic": 0.2,
      "dorsal_vagal": 0.1
    },
    "zone_distribution": {...},
    "maturity_score": 0.65
  }
}
```

**Purpose:** Cluster similar conversation types, learn family-specific response patterns

**User Relationship:** Users can have `organic_family_membership` in their profile, showing affinity to families.

#### Hebbian Memory (`persona_layer/conversational_hebbian_memory.json`)
**Status:** Actively used for phrase learning

**Structure:**
```json
{
  "r_matrix": {
    "LISTENING_EMPATHY": 0.45,
    "EMPATHY_WISDOM": 0.62,
    ...
  },
  "value_mappings": {
    "listening_inquiry": ["Tell me more", "What feels important here?", ...],
    "empathy_resonance": ["I sense that", "It sounds like", ...]
  }
}
```

**Purpose:** Learn which organ pairings work well together, store successful phrases

**User Relationship:** Global (shared across all users), but user-specific Hebbian memory exists in Bundle dirs.

#### Conversational Training Pairs (`knowledge_base/conversational_training_pairs.json`)
**Status:** 30 training examples across 6 categories

**Categories:**
- burnout_spiral (5 pairs)
- toxic_productivity (5 pairs)
- psychological_safety (5 pairs)
- witnessing_presence (5 pairs)
- sustainable_rhythm (5 pairs)
- scapegoat_dynamics (5 pairs)

**Purpose:** Train organism on therapeutic conversation patterns

**User Relationship:** Not user-specific, but could be extended with per-user examples.

---

## 3. Query Capabilities (Current vs. Needed)

### 3.1 Current Query Capabilities ✅

**User Lookup:**
```python
# Get user by ID
user_registry = UserRegistry()
user = user_registry.get_user("user_20251113_143117")
# Returns: {'user_id': '...', 'username': 'Emi', 'total_sessions': 7, ...}

# Load full user state
user_state = user_registry.load_user_state("user_20251113_143117")
# Returns: Full state with session_history, feedback, preferences

# List all users
users = user_registry.list_users()
# Returns: List of all registered users with stats
```

**User Profile Queries:**
```python
profile_manager = UserProfileManager()

# Get profile
profile = profile_manager.get_or_create_profile("user_20251113_143117")

# Get conversation history
history = profile_manager.get_conversation_history(
    user_id="user_20251113_143117",
    session_id="20251114_133639",
    max_turns=10
)

# Get template preferences
templates = profile_manager.get_template_preferences(
    user_id="user_20251113_143117",
    category="trauma_aware",
    top_k=5
)

# Get preferred organic families
families = profile_manager.get_preferred_families(
    user_id="user_20251113_143117",
    top_k=3
)

# Get inside jokes
jokes = profile_manager.get_inside_jokes(
    user_id="user_20251113_143117",
    max_count=5
)
```

**Superject Queries:**
```python
superject_learner = UserSuperjectLearner()

# Get user superject
profile = superject_learner.get_or_create_profile("user_20251113_143117")

# Access learned patterns
patterns = profile.transformation_patterns
# Dict of pattern_id → TransformationPattern

# Access recurring themes
themes = profile.recurring_themes
# {'burnout': 5, 'creative_blocks': 3, ...}

# Access inside jokes
jokes = profile.inside_jokes
# List of inside joke dicts with context

# Access humor evolution
humor_unlocked = profile.humor_evolution.humor_unlocked
humor_style = profile.humor_evolution.learned_humor_style
```

### 3.2 Missing Query Capabilities ❌

**Cross-User Queries (Not Needed for Phase 1):**
- "Find all users who prefer 'gentle' tone in Zone 3"
- "Find users with similar organic family membership to Emi"
- "Find conversations where 'burnout' theme was successfully addressed"

**Temporal/Trend Queries (Future Phase):**
- "Show Emi's satisfaction trajectory over last 30 days"
- "Has Emi's humor tolerance increased over time?"
- "Which transformation patterns emerged most recently?"

**Relationship Queries (Future Phase):**
- "What inside jokes does Emi have that relate to 'creative blocks'?"
- "Which organic families does Emi prefer, and why?"
- "What templates work best for Emi in Zone 4?"

**Cross-Reference Queries (Not Critical):**
- "Which users are in the same organic family as Emi?"
- "What's the average session count for users with high humor tolerance?"

**Assessment:** Current JSON-based system is **sufficient for Phase 1** (personalized name usage, basic preferences). Graph database would enable **Phase 2+** (advanced relationship discovery, collaborative filtering).

---

## 4. Gap Analysis: What's Needed for Proper Name Usage

### 4.1 Immediate Needs (Phase 1)

**Priority 1: Pass Username to LLM Prompt** ⭐⭐⭐
- **Where:** `build_felt_prompt()` in `llm_felt_guidance.py`
- **Change:** Add `username` parameter, inject into prompt
- **Impact:** LLM can address user by name ("I hear you, Emi...")
- **Effort:** 🟢 Trivial (1 parameter addition + prompt template change)

**Priority 2: Pass Username Through Organism Wrapper** ⭐⭐⭐
- **Where:** `process_text()` in `conversational_organism_wrapper.py`
- **Change:** Extract username from context, pass to emission generator
- **Impact:** Username flows from interactive session → organism → LLM
- **Effort:** 🟢 Trivial (read from context dict)

**Priority 3: Include Username in Context Dict** ⭐⭐⭐
- **Where:** `process_input()` in `dae_interactive.py`
- **Change:** Add `'username': self.user['username']` to context
- **Impact:** Username available throughout processing pipeline
- **Effort:** 🟢 Trivial (1 line change)

### 4.2 Medium-Term Needs (Phase 2)

**Priority 4: User Preference Injection** ⭐⭐
- **Where:** `build_felt_prompt()` constraints
- **Change:** Load user profile, inject preferences into LLM constraints
- **Example:** "Emi prefers moderate-length responses with occasional humor"
- **Effort:** 🟡 Moderate (requires UserProfileManager integration)

**Priority 5: Inside Joke Context** ⭐⭐
- **Where:** `build_felt_prompt()` memory_context
- **Change:** Retrieve inside jokes from profile, add to prompt
- **Example:** "Emi has an inside joke about 'the Tuesday meeting' (context: burnout discussion)"
- **Effort:** 🟡 Moderate (query inside_jokes, format for prompt)

**Priority 6: Recurring Theme Detection** ⭐⭐
- **Where:** Salience model or pre-processing
- **Change:** Check if user input matches recurring themes
- **Example:** If Emi says "burnout again", note theme="burnout" (count=5 previous)
- **Effort:** 🟡 Moderate (theme matching logic)

### 4.3 Long-Term Needs (Phase 3+)

**Priority 7: Collaborative Filtering** ⭐
- **Capability:** "Users like Emi (similar family affinity) found these templates helpful"
- **Requirements:** Graph database OR advanced JSON queries
- **Effort:** 🔴 Complex (requires similarity computation across users)

**Priority 8: Temporal Evolution Tracking** ⭐
- **Capability:** "Emi's tone preference has shifted from 'gentle' to 'playful' over 3 weeks"
- **Requirements:** Timestamped preference history
- **Effort:** 🟡 Moderate (track preference changes over time)

**Priority 9: Cross-User Learning** ⭐
- **Capability:** "Transformation pattern X works for 80% of users in family_0"
- **Requirements:** Aggregation across user superjets
- **Effort:** 🔴 Complex (global epoch learning - already planned)

---

## 5. Graph Database Assessment

### 5.1 Neo4j Current Status

**Infrastructure:** ✅ Implemented (Phase 2.2)
**Active Usage:** ❌ Not used in production
**Connection:** ✅ Cloud instance available
**Schema:** ✅ Trauma-informed concepts + relationships defined

**Why Not Used?**
- Focus shifted to JSON-based organic learning (faster iteration)
- Neo4j adds deployment complexity (requires separate service)
- Current JSON system handles all Phase 1 needs

### 5.2 When Would Neo4j Be Needed?

**Scenario 1: Multi-Hop Relationship Queries**
- Example: "Find transformation patterns that worked for users similar to Emi"
- Complexity: Requires similarity metric → find similar users → aggregate their patterns
- JSON Solution: Feasible but slow (N^2 comparisons)
- Neo4j Solution: Efficient with graph traversal

**Scenario 2: Concept Relationship Discovery**
- Example: "What concepts are related to 'burnout' within 2 hops?"
- Complexity: Graph traversal problem
- JSON Solution: Not feasible (no graph structure)
- Neo4j Solution: Native graph query (Cypher)

**Scenario 3: Collaborative Filtering**
- Example: "Recommend templates to Emi based on users with similar profiles"
- Complexity: User-User similarity + Template success aggregation
- JSON Solution: Possible but inefficient
- Neo4j Solution: Graph-based recommendation engine

**Scenario 4: Temporal Relationship Evolution**
- Example: "How has Emi's relationship to 'creative blocks' theme evolved?"
- Complexity: Time-series queries on relationships
- JSON Solution: Possible with timestamped arrays
- Neo4j Solution: Temporal graph queries (advanced)

### 5.3 Python Graph Libraries (Lightweight Alternative)

**Option 1: NetworkX** (No external service needed)
```python
import networkx as nx

# Build user relationship graph in-memory
G = nx.Graph()
G.add_node("user_emi", username="Emi", humor_tolerance=0.6)
G.add_node("user_alice", username="Alice", humor_tolerance=0.5)
G.add_edge("user_emi", "family_0", weight=0.8)
G.add_edge("user_alice", "family_0", weight=0.7)

# Find similar users (connected to same families)
similar_users = list(nx.common_neighbors(G, "user_emi", "family_0"))
```

**Pros:**
- No external service (pure Python)
- Fast for small-medium graphs (< 10k nodes)
- Rich algorithms (shortest path, centrality, clustering)

**Cons:**
- In-memory only (not persistent)
- No query language (manual graph traversal)
- Slower than Neo4j for large graphs (> 100k nodes)

**Verdict:** ✅ **Good fit for Phase 2** (user similarity, family recommendations)

**Option 2: Python-based Graph Database (TinyDB + NetworkX hybrid)**
```python
# Store user profiles in TinyDB (JSON on disk)
# Build graph in NetworkX for queries
# Sync graph from TinyDB on load

from tinydb import TinyDB
import networkx as nx

db = TinyDB('user_graph.json')
G = nx.Graph()

# Load users from TinyDB into graph
for user in db.all():
    G.add_node(user['user_id'], **user)

# Query graph
similar_users = nx.neighbors(G, "user_emi")
```

**Pros:**
- Persistent storage (TinyDB on disk)
- Graph queries (NetworkX)
- No external service

**Cons:**
- Manual sync between TinyDB and NetworkX
- Not as robust as Neo4j for concurrent writes

**Verdict:** ✅ **Good fit for Phase 2-3** (hybrid approach)

### 5.4 Recommendation: Defer Neo4j to Phase 3+

**Phase 1 (Current):** JSON-based system is **sufficient**
- User profiles in `persona_layer/users/*.json`
- Organic families in `organic_families.json`
- Hebbian memory in `conversational_hebbian_memory.json`

**Phase 2 (Next 1-3 months):** Add **NetworkX** for user similarity
- Build in-memory graph from user profiles
- Compute user-user similarity (cosine similarity on preferences)
- Recommend organic families, templates, transformation patterns

**Phase 3 (3-6 months):** Evaluate **Neo4j** migration
- If user base grows (> 1000 users)
- If complex multi-hop queries needed
- If collaborative filtering becomes critical

**Phase 4 (6+ months):** Production **Neo4j** deployment
- Only if query complexity justifies overhead
- Cloud-hosted Neo4j instance
- Migrate user relationships to graph

---

## 6. Recommended Strategy

### 6.1 Immediate Fixes (Next Session - < 1 hour)

**Fix 1: Add Username to Context**
```python
# File: dae_interactive.py, line 256
def process_input(self, user_input: str) -> dict:
    context = {
        'session_id': self.session_id,
        'timestamp': datetime.now().isoformat(),
        'turn': len(self.conversation_history) + 1,
        'username': self.user['username'],  # ✅ ADD THIS
        'user_id': self.user['user_id']     # ✅ ADD THIS
    }
```

**Fix 2: Pass Username Through Organism Wrapper**
```python
# File: conversational_organism_wrapper.py, around line 999+
# Already has user_id extraction - add username
if context:
    user_id = context.get('user_id', None)
    username = context.get('username', None)  # ✅ ADD THIS
    
    # Later, pass to emission generator
    emission_result = self.emission_generator.generate_emissions(
        nexuses=final_nexuses,
        user_input=text,
        username=username,  # ✅ ADD THIS
        organ_results=organ_results,
        v0_energy=v0_final,
        satisfaction=satisfaction_final,
        memory_context=memory_context
    )
```

**Fix 3: Update Emission Generator Signature**
```python
# File: emission_generator.py, line 907
def generate_emissions(
    self,
    nexuses: List,
    num_emissions: int = 3,
    prefer_variety: bool = True,
    user_input: str = "",
    username: Optional[str] = None,  # ✅ ADD THIS
    organ_results: Dict = None,
    v0_energy: float = 1.0,
    satisfaction: float = 0.0,
    memory_context: Optional[List[Dict]] = None
) -> List[EmittedPhrase]:
```

**Fix 4: Pass Username to Felt-Guided LLM**
```python
# File: emission_generator.py, around line 970 (in generate_emissions)
if self.felt_guided_llm:
    emission_text, confidence, metadata = self.felt_guided_llm.generate_from_felt_state(
        user_input=user_input,
        username=username,  # ✅ ADD THIS
        organ_results=organ_results,
        nexus_states=nexuses,
        v0_energy=v0_energy,
        satisfaction=satisfaction,
        memory_context=memory_context
    )
```

**Fix 5: Update FeltGuidedLLMGenerator**
```python
# File: llm_felt_guidance.py, line 444
def generate_from_felt_state(
    self,
    user_input: str,
    username: Optional[str] = None,  # ✅ ADD THIS
    organ_results: Dict,
    nexus_states: List,
    v0_energy: float,
    satisfaction: float,
    memory_context: Optional[List[Dict]] = None,
    organism_narrative: Optional[str] = None
) -> Tuple[str, float, Dict]:
    
    # ... later, pass to build_felt_prompt ...
    
    prompt = self.build_felt_prompt(
        user_input=user_input,
        username=username,  # ✅ ADD THIS
        constraints=constraints,
        lures=lures,
        memory_context=memory_context,
        organism_narrative=organism_narrative
    )
```

**Fix 6: Update Prompt Builder**
```python
# File: llm_felt_guidance.py, line 341
def build_felt_prompt(
    self,
    user_input: str,
    username: Optional[str] = None,  # ✅ ADD THIS
    constraints: LLMConstraints,
    lures: FeltLures,
    memory_context: Optional[List[Dict]] = None,
    organism_narrative: Optional[str] = None
) -> str:
    if organism_narrative:
        prompt = "You are DAE, a conversational organism with persistent self-awareness.\n\n"
        
        # ✅ ADD PERSONALIZATION
        if username:
            prompt += f"You are speaking with {username}, someone you've conversed with before.\n\n"
        
        prompt += "The user is asking about YOU (DAE). Respond authentically from your organism perspective.\n\n"
        prompt += "YOUR CURRENT ORGANISM STATE:\n"
        prompt += organism_narrative + "\n\n"
        prompt += "---\n\n"
    else:
        prompt = "You are responding as a felt-intelligent companion organism.\n\n"
        
        # ✅ ADD PERSONALIZATION
        if username:
            prompt += f"You are speaking with {username}.\n\n"
    
    # ... later in prompt ...
    
    # User input
    # ✅ PERSONALIZE USER PREFIX
    user_prefix = f"{username}: " if username else "User: "
    prompt += f"\n---\n{user_prefix}{user_input}\n\n"
```

**Testing:**
```bash
# Launch interactive mode
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1":$PYTHONPATH
python3 dae_interactive.py

# Login as Emi (or create new user)
# Send message: "I'm feeling overwhelmed"

# Expected LLM prompt (internal):
You are responding as a felt-intelligent companion organism.

You are speaking with Emi.

Current felt state:
- Tone: gentle
- Polyvagal: sympathetic
...

---
Emi: I'm feeling overwhelmed

Respond with gentle tone, ...

# Expected emission:
"I hear you, Emi. That sounds really hard right now. 🌊"
```

**Impact:** ✅ Immediate personalization with user names

### 6.2 Medium-Term Enhancements (Next 1-2 weeks)

**Enhancement 1: User Preference Loading**
```python
# Load user preferences and inject into LLM constraints
# File: llm_felt_guidance.py, in extract_felt_lures() or map_lures_to_constraints()

# Load user profile
if username:
    profile_manager = UserProfileManager()
    profile = profile_manager.get_or_create_profile(user_id)
    
    # Override default constraints with learned preferences
    constraints.response_length = profile.response_length_preference
    constraints.empathy_level = profile.humor_tolerance
    # ... etc ...
```

**Enhancement 2: Inside Joke Retrieval**
```python
# Retrieve inside jokes and add to prompt
# File: llm_felt_guidance.py, in build_felt_prompt()

if username and user_id:
    profile_manager = UserProfileManager()
    jokes = profile_manager.get_inside_jokes(user_id, max_count=3)
    
    if jokes:
        prompt += f"\nYour relationship with {username}:\n"
        for joke in jokes:
            prompt += f"- Inside joke: \"{joke['joke']}\" (from: {joke['context']})\n"
        prompt += f"\nUse these callbacks if contextually appropriate.\n\n"
```

**Enhancement 3: Recurring Theme Context**
```python
# Detect recurring themes and add to prompt
# File: llm_felt_guidance.py or conversational_organism_wrapper.py

if username and user_id:
    superject_learner = UserSuperjectLearner()
    profile = superject_learner.get_or_create_profile(user_id)
    
    # Check if current input matches recurring themes
    recurring = profile.recurring_themes
    theme_mentions = [theme for theme in recurring if theme.lower() in user_input.lower()]
    
    if theme_mentions:
        prompt += f"\n{username} has discussed these themes before:\n"
        for theme in theme_mentions:
            count = recurring[theme]
            prompt += f"- {theme} (mentioned {count} times previously)\n"
        prompt += f"\nAcknowledge the pattern if appropriate.\n\n"
```

**Testing:**
```bash
# After user Emi has had 5 sessions discussing "burnout"
Emi: "I'm feeling burnt out again"

# LLM prompt includes:
---
Emi has discussed these themes before:
- burnout (mentioned 5 times previously)

Acknowledge the pattern if appropriate.
---

# Expected emission:
"Emi, I notice burnout has been coming up a lot for you lately. 
What's different this time, or is it the same pattern? 💙"
```

**Impact:** ✅ Relationship memory, continuity across sessions

### 6.3 Long-Term Enhancements (Next 1-3 months)

**Enhancement 4: User Similarity Graph (NetworkX)**
```python
# Build user similarity graph for collaborative filtering
# New file: persona_layer/user_similarity_graph.py

import networkx as nx
from persona_layer.user_registry import UserRegistry
from persona_layer.user_profile_manager import UserProfileManager

class UserSimilarityGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.user_registry = UserRegistry()
        self.profile_manager = UserProfileManager()
    
    def build_graph(self):
        """Build graph from all user profiles."""
        users = self.user_registry.list_users()
        
        for user in users:
            user_id = user['user_id']
            profile = self.profile_manager.get_or_create_profile(user_id)
            
            # Add user node with attributes
            self.G.add_node(user_id, 
                username=profile.user_id,
                humor_tolerance=profile.humor_tolerance,
                response_preference=profile.response_length_preference,
                total_turns=profile.total_turns
            )
            
            # Add edges to organic families
            for family_id, affinity in profile.family_affinities.items():
                self.G.add_edge(user_id, family_id, weight=affinity, type='family_member')
    
    def find_similar_users(self, user_id: str, top_k: int = 5) -> List[str]:
        """Find users similar to given user."""
        # Method 1: Common neighbors (same organic families)
        neighbors = list(nx.common_neighbors(self.G, user_id, "family_0"))
        
        # Method 2: Attribute similarity (cosine similarity on preferences)
        # ... compute similarity scores ...
        
        return neighbors[:top_k]
    
    def recommend_templates(self, user_id: str, category: str, top_k: int = 5) -> List[str]:
        """Recommend templates based on similar users' success."""
        similar_users = self.find_similar_users(user_id, top_k=10)
        
        # Aggregate template success rates from similar users
        template_scores = defaultdict(list)
        for similar_user_id in similar_users:
            similar_profile = self.profile_manager.get_or_create_profile(similar_user_id)
            for template_id, success_rate in similar_profile.template_success_rates.items():
                if template_id.startswith(f"{category}:"):
                    template_scores[template_id].append(success_rate)
        
        # Average scores
        avg_scores = {tid: np.mean(scores) for tid, scores in template_scores.items()}
        
        # Sort and return top K
        sorted_templates = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
        return [tid for tid, score in sorted_templates[:top_k]]
```

**Usage:**
```python
# In felt-guided LLM generation
graph = UserSimilarityGraph()
graph.build_graph()

# Find similar users
similar = graph.find_similar_users("user_emi")
# Returns: ["user_alice", "user_jason", ...]

# Recommend templates
recommended = graph.recommend_templates("user_emi", category="trauma_aware", top_k=3)
# Returns: ["trauma_aware:gentle_inquiry", "trauma_aware:somatic_grounding", ...]

# Inject into prompt
if recommended:
    prompt += f"\nUsers similar to {username} found these approaches helpful:\n"
    for template in recommended:
        prompt += f"- {template}\n"
```

**Impact:** ✅ Collaborative filtering, improved recommendations

**Enhancement 5: Temporal Preference Evolution**
```python
# Track preference changes over time
# Modify: user_profile_manager.py

@dataclass
class UserProfile:
    # ... existing fields ...
    
    # NEW: Preference history
    preference_history: List[Dict[str, Any]] = field(default_factory=list)
    # Example: [
    #   {"timestamp": "2025-11-01", "humor_tolerance": 0.3, "response_length": "brief"},
    #   {"timestamp": "2025-11-15", "humor_tolerance": 0.6, "response_length": "moderate"},
    # ]

# NEW method:
def update_preference(self, user_id: str, preference_name: str, value: Any):
    """Update preference and log to history."""
    profile = self.get_or_create_profile(user_id)
    
    # Log current value to history before updating
    profile.preference_history.append({
        "timestamp": datetime.now().isoformat(),
        preference_name: getattr(profile, preference_name)
    })
    
    # Update preference
    setattr(profile, preference_name, value)
    
    self.update_profile(profile)

# NEW method:
def get_preference_trend(self, user_id: str, preference_name: str) -> str:
    """Detect if preference is increasing, decreasing, or stable."""
    profile = self.get_or_create_profile(user_id)
    history = profile.preference_history
    
    if len(history) < 3:
        return "stable"  # Not enough data
    
    # Get last 3 values
    recent = [h.get(preference_name) for h in history[-3:] if preference_name in h]
    
    if len(recent) < 3:
        return "stable"
    
    # Detect trend
    if recent[0] < recent[1] < recent[2]:
        return "increasing"
    elif recent[0] > recent[1] > recent[2]:
        return "decreasing"
    else:
        return "stable"
```

**Usage:**
```python
# In LLM prompt builder
if user_id:
    trend = profile_manager.get_preference_trend(user_id, "humor_tolerance")
    if trend == "increasing":
        prompt += f"\nNote: {username}'s humor tolerance has been increasing recently. 
        You can be slightly more playful than usual.\n"
```

**Impact:** ✅ Adaptive to user evolution over time

---

## 7. Final Recommendations

### 7.1 Immediate Action (This Session)

**Priority:** ⭐⭐⭐ CRITICAL

**Tasks:**
1. ✅ Add `username` to context dict in `dae_interactive.py`
2. ✅ Pass `username` through organism wrapper to emission generator
3. ✅ Update `build_felt_prompt()` to accept and use `username`
4. ✅ Test with interactive session

**Estimated Time:** 30-60 minutes

**Expected Outcome:** LLM addresses user by name in responses

### 7.2 Near-Term Action (Next 1-2 weeks)

**Priority:** ⭐⭐ HIGH

**Tasks:**
1. Load user preferences from `UserProfile` and inject into LLM constraints
2. Retrieve inside jokes and add to prompt context
3. Detect recurring themes and acknowledge in responses
4. Add conversation history summary to prompt (last 3-5 turns)

**Estimated Time:** 4-6 hours

**Expected Outcome:** Personalized responses based on learned user preferences and relationship memory

### 7.3 Medium-Term Action (Next 1-3 months)

**Priority:** ⭐ MEDIUM

**Tasks:**
1. Implement `UserSimilarityGraph` with NetworkX
2. Build collaborative filtering for template recommendations
3. Track temporal preference evolution
4. Create user similarity dashboard (optional)

**Estimated Time:** 2-3 days

**Expected Outcome:** Improved recommendations via collaborative learning across users

### 7.4 Long-Term Action (3-6 months)

**Priority:** ⭐ LOW (Evaluate Later)

**Tasks:**
1. Evaluate Neo4j migration if user base grows significantly (> 1000 users)
2. Implement advanced graph queries for multi-hop relationship discovery
3. Build temporal graph for relationship evolution over time

**Estimated Time:** 1-2 weeks

**Expected Outcome:** Scalable graph infrastructure for complex relationship queries

---

## 8. Conclusion

### 8.1 Key Findings

**✅ Strong Foundation:**
- DAE_HYPHAE_1 has **robust user identity infrastructure**
- 3 complementary systems: UserRegistry, UserProfileManager, UserSuperjectLearner
- Per-user state persistence with rich metadata
- Comprehensive learning (transformation patterns, inside jokes, preferences)

**❌ Critical Gap:**
- **Username is NOT passed to LLM prompts**
- Easy fix: Add username parameter through processing pipeline

**✅ Graph Assessment:**
- **Neo4j exists but is NOT needed for Phase 1**
- JSON-based system is sufficient for current needs
- NetworkX is better fit for Phase 2 (user similarity, collaborative filtering)
- Neo4j only needed for Phase 3+ (if query complexity justifies deployment overhead)

### 8.2 Recommended Path Forward

**Phase 1 (Current Session):**
- ✅ Implement username passing (6 code changes, < 1 hour)
- ✅ Test with interactive session
- ✅ Verify LLM uses user name in responses

**Phase 2 (Next 2 weeks):**
- ✅ Add user preference loading
- ✅ Add inside joke retrieval
- ✅ Add recurring theme detection
- ✅ Test relationship memory across sessions

**Phase 3 (Next 1-3 months):**
- ✅ Build NetworkX user similarity graph
- ✅ Implement collaborative filtering
- ✅ Track temporal preference evolution
- ⚠️ Defer Neo4j (not needed yet)

**Phase 4 (3-6 months):**
- ⚠️ Re-evaluate Neo4j if:
  - User base > 1000 active users
  - Complex multi-hop queries needed
  - Graph-based recommendations critical

### 8.3 Success Metrics

**Phase 1 Success:**
- ✅ LLM addresses user by name: "I hear you, Emi..."
- ✅ No impersonal "User" or generic responses
- ✅ All tests passing, no regressions

**Phase 2 Success:**
- ✅ Responses reflect learned preferences (tone, length, humor)
- ✅ Inside jokes referenced when appropriate
- ✅ Recurring themes acknowledged
- ✅ User feels "DAE knows me"

**Phase 3 Success:**
- ✅ Template recommendations improve with similar user data
- ✅ User similarity graph builds successfully
- ✅ Collaborative filtering shows measurable improvement (A/B test)

---

**END OF INVESTIGATION**

**Next Step:** Implement Phase 1 fixes (username passing) in current session.
