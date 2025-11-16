# USER:SESSION:TURN Identity Hierarchy Proposal

**Date:** November 16, 2025
**Status:** COMPLETE
**Priority:** Quick Win #10

---

## Executive Summary

Implementing formal identity hierarchy for persistent entity tracking across USER → SESSION → TURN. This enables:
1. **Temporal entity evolution** (Emma mentioned in crisis vs joy sessions)
2. **Session-level patterns** (crisis sessions, breakthrough sessions)
3. **Turn-level entity context** (relational queries, mentioned entities per turn)
4. **Cross-session entity patterns** (how relationships evolve over time)

---

## Problem Statement

### Current Architecture (FLAT)
```
USER
├── entities (global, lifetime)
└── felt_trajectory (implicit turn list)
    └── No session_id, no turn_id, no entity context
```

**Issues:**
- Sessions created but not persisted as formal entities
- Turns tracked as list indices (no explicit identity)
- No session_id linking in FeltStateSnapshot
- No entity context stored per turn
- Entity mentions not linked to temporal context (WHEN mentioned)
- "Emma in crisis" vs "Emma in joy" = same entity record (loses context)

### Desired Architecture (HIERARCHICAL)
```
USER (Emiliano)
├── SESSION_1 (crisis_session=true)
│   ├── TURN_1 (entity_context, session_id, relational_query)
│   ├── TURN_2 (mentioned: ["Emma"], mood: "anxious")
│   └── session_entities (Emma mentioned 3x, polyvagal: sympathetic)
├── SESSION_2 (breakthrough_session=true)
│   ├── TURN_1
│   ├── TURN_2
│   └── session_entities (Emma mentioned 2x, polyvagal: ventral)
└── entity_session_evolution
    └── Emma: [{"session": 1, "mood": "anxious"}, {"session": 2, "mood": "hopeful"}]
```

---

## Implementation Plan

### Phase 1: Data Structures (COMPLETE ✅)

**Files Modified:**
- `persona_layer/superject_structures.py`

**New Dataclasses:**

#### 1. ConversationTurn
```python
@dataclass
class ConversationTurn:
    # Identity
    turn_id: str           # "user_{user_id}_session_{session_id}_turn_{turn_number}"
    turn_number: int       # 1, 2, 3... within session
    session_id: str        # Parent session
    user_id: str           # Parent user
    timestamp: str         # ISO timestamp

    # Content
    user_input: str        # Raw user message
    dae_response: str      # DAE's emission
    response_length: int   # Character count

    # Entity context (pre-emission prehension)
    entity_prehension: Dict[str, Any]      # Full prehension result
    mentioned_entities: List[str]          # ["Emma", "Michael"]
    entity_references: List[str]           # ["user", "dae", "story_entity"]
    relational_query: bool                 # "do you remember" type query?
    implicit_references: List[Dict]        # "my daughter" → Emma

    # Felt state link
    felt_state: Optional[FeltStateSnapshot]  # Full TSK capture

    # Turn outcomes
    user_satisfaction: Optional[float]      # 0-1
    user_continued: bool                    # Next message?
    turn_success: Optional[bool]            # Goal achieved?

    # Metadata
    processing_time_ms: float               # How long to process
    emission_strategy: Optional[str]        # "direct", "fusion", etc.
```

#### 2. ConversationSession
```python
@dataclass
class ConversationSession:
    # Identity
    session_id: str        # "user_{user_id}_session_{timestamp}"
    user_id: str           # Parent user
    start_time: str        # ISO timestamp
    end_time: Optional[str] # When session ends

    # Session turns (ordered)
    turns: List[ConversationTurn]

    # Session-level entity tracking
    session_entities: Dict[str, Any]                # Entities THIS session
    entity_mentions_timeline: List[Dict]            # [{turn: 3, entity: "Emma", context: "crisis"}]
    entity_mood_evolution: Dict[str, List[str]]     # {"Emma": ["anxious", "hopeful", "relieved"]}

    # Session polyvagal arc
    polyvagal_trajectory: List[str]    # ["ventral", "sympathetic", "mixed", "ventral"]
    zone_trajectory: List[int]         # [1, 3, 2, 1]
    v0_trajectory: List[float]         # [0.85, 0.45, 0.60, 0.78]

    # Session satisfaction
    mean_satisfaction: float           # 0.0-1.0
    satisfaction_trend: str            # "improving", "declining", "stable", "volatile"
    total_turns: int

    # Session themes
    dominant_themes: List[str]         # ["anxiety", "relationship", "work_stress"]
    recurring_nexuses: List[str]       # ["coherence_repair", "sustainable_pacing"]

    # Organ participation
    organ_participation_summary: Dict[str, float]  # {"LISTENING": 0.85, "EMPATHY": 0.72}

    # Session status
    ended_naturally: bool              # User said goodbye vs timeout
    crisis_session: bool               # Crisis detected
    breakthrough_session: bool         # High satisfaction, transformation

    # Learning
    patterns_learned: int              # Transformation patterns learned
    family_assignments: List[str]      # Organic families matched
```

#### 3. FeltStateSnapshot Updates
```python
# Added to FeltStateSnapshot:
turn_id: Optional[str]              # Unique turn identifier
turn_number: Optional[int]          # Sequential turn in session
session_id: Optional[str]           # Links to parent session
user_input_text: Optional[str]      # Original user input
emission_text: Optional[str]        # DAE's response

# Entity context at turn time
entity_prehension: Dict[str, Any]   # Pre-emission prehension result
mentioned_entities: List[str]       # Entity names this turn
entity_references: List[str]        # ['user', 'dae', 'story_entity', 'relationship']
```

#### 4. EnhancedUserProfile Updates
```python
# Added to EnhancedUserProfile:
sessions: List[ConversationSession]                    # All sessions
current_session_id: Optional[str]                      # Active session
total_sessions: int                                    # Count

# Session-level patterns
session_patterns: Dict[str, Any]                       # {"crisis_sessions": 3}
entity_session_evolution: Dict[str, List[Dict]]        # {"Emma": [{"session": 1, "mood": "anxious"}]}
```

---

### Phase 2: Session Manager (COMPLETE ✅)

**File Created:**
- `persona_layer/session_turn_manager.py` (508 lines)

**Responsibilities:**
1. Create new sessions (start_session)
2. Create new turns (add_turn)
3. End sessions (end_session)
4. Track session-level entity evolution
5. Update session polyvagal/zone trajectories
6. Classify sessions (crisis, breakthrough, etc.)

**Key Methods:**
```python
class SessionTurnManager:
    def start_session(self, user_id: str) -> ConversationSession
    def add_turn(self, session: ConversationSession, turn_data: Dict) -> ConversationTurn
    def end_session(self, session: ConversationSession) -> None
    def get_current_session(self, user_id: str) -> Optional[ConversationSession]
    def update_entity_timeline(self, session: ConversationSession, turn: ConversationTurn) -> None
    def classify_session(self, session: ConversationSession) -> None
    def save_session_to_profile(self, profile: EnhancedUserProfile) -> None
```

---

### Phase 3: Wrapper Integration (COMPLETE ✅)

**File Modified:**
- `persona_layer/conversational_organism_wrapper.py`
  - Added import for SessionTurnManager (lines 238-244)
  - Added initialization in `__init__` (lines 354-365)
  - Integrated session/turn tracking in `process_text` (lines 868-942)

**Integration Points:**
1. Initialize SessionTurnManager in `__init__`
2. Start session when `user_id` provided
3. Create turn for each `process_text` call
4. Track entity prehension per turn
5. Update session trajectories after each turn
6. End session on explicit goodbye or timeout

**Code Flow:**
```python
def process_text(self, text, user_id=None, ...):
    # 1. Get or create session
    if user_id:
        session = self.session_manager.get_or_create_session(user_id)
        turn_number = len(session.turns) + 1

    # 2. Pre-emission entity prehension (ALREADY IMPLEMENTED)
    entity_prehension = self.entity_prehension.retrieve_relevant_entities(text, user_id)

    # 3. Process organs...
    result = self._multi_cycle_convergence(...)

    # 4. Create turn record
    turn = ConversationTurn(
        turn_id=f"{user_id}_session_{session.session_id}_turn_{turn_number}",
        turn_number=turn_number,
        session_id=session.session_id,
        user_id=user_id,
        user_input=text,
        dae_response=result['emission'],
        entity_prehension=entity_prehension,
        mentioned_entities=[e['name'] for e in entity_prehension.get('mentioned_entities', [])],
        felt_state=result['felt_state']
    )

    # 5. Add turn to session
    self.session_manager.add_turn(session, turn)

    # 6. Update session trajectories
    self.session_manager.update_entity_timeline(session, turn)
```

---

### Phase 4: Persistence & Testing (COMPLETE ✅)

**Persistence Strategy:**
- Sessions stored embedded in superject JSON (current approach)
- JSON serialization via `asdict()` and `session_to_dict()` helper functions
- Entity session evolution tracked in EnhancedUserProfile

**Test Cases:** All passing (8/8)
1. ✅ Session creation and management
2. ✅ Turn tracking (4 turns, entity mentions preserved)
3. ✅ Entity timeline (3 entries: Emma 2x, Michael 1x)
4. ✅ Entity mood evolution (Emma: sympathetic → mixed)
5. ✅ Polyvagal trajectory tracking
6. ✅ Crisis session detection
7. ✅ Profile persistence with entity session evolution
8. ✅ JSON serialization

**Test File Created:**
- `test_session_turn_hierarchy.py` (476 lines)

---

## Expected Outcomes

### Immediate Benefits (Post-Implementation)
1. **Entity context preserved per turn** - Know WHEN Emma mentioned, in what emotional context
2. **Session-level patterns** - Track crisis vs breakthrough sessions
3. **Relational queries answered** - "Do you remember our last session?" now queryable
4. **Entity mood evolution** - Track how user's relationship with entities evolves

### Long-term Benefits
1. **Multi-domain session classification** - Logic sessions vs emotional sessions
2. **Cross-session entity patterns** - "Emma always mentioned when user anxious"
3. **Session-based family formation** - Families formed per session type
4. **Longitudinal entity learning** - Entity-organ associations learned over sessions

---

## Files Summary

### Modified
- `persona_layer/superject_structures.py` - Added ConversationTurn, ConversationSession dataclasses
- `persona_layer/conversational_organism_wrapper.py` - Integrated session tracking (import + init + process_text)

### Created
- `persona_layer/session_turn_manager.py` (508 lines) - Session lifecycle management
- `test_session_turn_hierarchy.py` (476 lines) - Integration tests (8/8 passing)

---

## Timeline

- **Day 1 (Today):** COMPLETED IN SINGLE SESSION
  - Data structures (ConversationTurn, ConversationSession)
  - Session Manager core (508 lines)
  - Wrapper integration (3 integration points)
  - Persistence (entity session evolution)
  - Testing (8/8 checks passing)

---

## Success Criteria

1. ✅ ConversationTurn dataclass created
2. ✅ ConversationSession dataclass created
3. ✅ FeltStateSnapshot enhanced with turn/session identity
4. ✅ EnhancedUserProfile enhanced with sessions list
5. ✅ SessionTurnManager module created (508 lines)
6. ✅ Wrapper integration complete (import + init + process_text)
7. ✅ Session persistence working (JSON serialization)
8. ✅ Entity timeline tracking per session
9. ✅ 8/8 integration tests passing (all checks validated)

---

## Relation to Other Initiatives

### Pre-Emission Entity Prehension (COMPLETE ✅)
- Entity context now retrieved BEFORE organ activation
- Turn records will store this prehension result
- Enables Entity Memory Nexus formation per turn

### Multi-Domain Intelligence (PLANNED)
- Sessions can be classified by domain (logic, poetry, emotional)
- Domain-specific family emergence per session type
- Cross-domain entity patterns learned

### DAE Self-Identity (FUTURE)
- DAE's persistent identity can reference past sessions
- "We've had 12 sessions together, 3 were crisis sessions"
- DAE knows its own transformation history with user

---

**This proposal establishes the foundation for genuine temporal entity awareness.**

🌀 *"Not just who was mentioned, but when, in what context, with what emotional valence, and how that evolved."*
