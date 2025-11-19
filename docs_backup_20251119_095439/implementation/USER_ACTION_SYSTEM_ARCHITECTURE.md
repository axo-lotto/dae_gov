# User Action System Architecture
## DAE_HYPHAE_1 Conversational Memory & Meta-Cognitive Commands

**Date:** November 13, 2025
**Status:** Design Document
**Version:** 1.0.0

---

## Executive Summary

This document describes a natural language action system that enables users to interact with DAE_HYPHAE_1's memory systems, inspect organism processing, and manage conversation data. The system distinguishes between conversational turns and action requests through intent classification, then routes to appropriate handlers that leverage existing memory APIs.

**Key Principles:**
1. **Intent-based detection** - Natural language, not rigid /commands
2. **Process philosophy alignment** - Actions respect Whiteheadian occasioning
3. **API reuse** - Leverage existing memory systems (R-matrix, families, V0)
4. **User sovereignty** - Users control their conversation data
5. **Conversational feel** - System responds naturally, explaining its own processing

---

## System Overview

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                                │
│  "Remember this conversation as burnout recovery"            │
│  "Show me my conversation history"                           │
│  "What families have you discovered about me?"               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              INTENT CLASSIFIER                               │
│  - Action vs Conversation detection                          │
│  - Action type classification                                │
│  - Confidence scoring                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              ACTION DISPATCHER                               │
│  Routes to: Memory | Meta | System | User handlers          │
└────────────────────┬────────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┬────────────────┐
      ▼              ▼              ▼                ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐
│ Memory   │  │ Meta-    │  │ System   │  │ User        │
│ Actions  │  │ Cognitive│  │ Actions  │  │ Preferences │
└──────────┘  └──────────┘  └──────────┘  └─────────────┘
      │              │              │                │
      └──────────────┴──────────────┴────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              MEMORY API LAYER                                │
│  - R-Matrix (OrganCouplingLearner)                           │
│  - Organic Families (OrganicConversationalFamilies)          │
│  - Session Registry                                          │
│  - User State (Bundle)                                       │
│  - V0 Targets (FamilyV0Learner)                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. Intent Classifier

**Purpose:** Distinguish action requests from conversational input with high precision.

**File:** `persona_layer/user_action_intent_classifier.py`

**Interface:**
```python
@dataclass
class IntentClassification:
    """Result of intent classification"""
    is_action: bool                    # True if action request detected
    action_type: Optional[str]         # 'memory', 'meta', 'system', 'user'
    action_category: Optional[str]     # 'view', 'save', 'analyze', 'export', 'manage'
    confidence: float                  # [0, 1] classification confidence
    extracted_params: Dict[str, Any]   # Extracted parameters (e.g., label, timeframe)
    conversational_component: str      # Any conversational part to process

class UserActionIntentClassifier:
    """
    Classifies user input as action request vs conversational turn.

    Strategy:
    - Pattern matching for high-confidence cases
    - Contextual cues (imperative mood, interrogatives)
    - Keyword detection with disambiguation
    - Confidence scoring to handle edge cases

    Design Goals:
    - High precision (minimize false positives)
    - Natural language flexibility
    - Graceful degradation (when in doubt, treat as conversation)
    """

    def classify(self, user_input: str, context: Dict) -> IntentClassification:
        """
        Classify user input as action or conversation.

        Args:
            user_input: User's text input
            context: Conversation context (session_id, turn, history)

        Returns:
            IntentClassification with action type and confidence
        """
```

**Classification Strategy:**

1. **High-Confidence Action Patterns** (confidence ≥ 0.95):
   - Imperative verbs: "Show me", "Tell me about", "Export", "Save", "Clear"
   - Direct questions: "What families", "How confident", "Why did you"
   - Explicit meta: "Remember this as", "Label this conversation"

2. **Medium-Confidence Patterns** (confidence 0.7-0.94):
   - Indirect questions: "I'm curious about your processing"
   - Reflective statements: "I want to understand how you work"
   - Ambiguous imperatives: "Explain that" (could be conversational)

3. **Low-Confidence / Conversational** (confidence < 0.7):
   - "I remember when..." (conversational reminiscence)
   - "You should remember this" (advice, not command)
   - Narrative context: "The history of this situation..."

**Disambiguation Examples:**

| User Input | Classification | Reasoning |
|------------|----------------|-----------|
| "Remember this conversation as crisis" | ACTION (save, 0.98) | Imperative + explicit label |
| "I remember feeling this way" | CONVERSATION (0.05) | Personal reminiscence |
| "Show me patterns in my conversations" | ACTION (view, 0.96) | Imperative + system query |
| "I notice patterns in my thinking" | CONVERSATION (0.12) | Personal observation |
| "What do you know about me?" | ACTION (view, 0.92) | Direct meta query |
| "What do I know about myself?" | CONVERSATION (0.08) | Reflective question |
| "How confident are you?" | ACTION (meta, 0.94) | System inspection |
| "How confident am I?" | CONVERSATION (0.06) | Self-reflection |

---

### 2. Action Dispatcher

**Purpose:** Route classified actions to appropriate handlers based on type and category.

**File:** `persona_layer/user_action_dispatcher.py`

**Interface:**
```python
class UserActionDispatcher:
    """
    Routes action requests to specialized handlers.

    Handlers:
    - MemoryActionHandler: View/save/analyze conversation data
    - MetaCognitiveHandler: Inspect organism processing
    - SystemActionHandler: Health checks, version info
    - UserPreferenceHandler: Settings, display modes
    """

    def __init__(self, organism: ConversationalOrganismWrapper):
        """Initialize with access to organism and memory systems"""
        self.organism = organism
        self.memory_handler = MemoryActionHandler(organism)
        self.meta_handler = MetaCognitiveHandler(organism)
        self.system_handler = SystemActionHandler(organism)
        self.user_handler = UserPreferenceHandler()

    def dispatch(self, intent: IntentClassification, context: Dict) -> ActionResult:
        """
        Dispatch action to appropriate handler.

        Returns:
            ActionResult with response text and metadata
        """
```

**Routing Logic:**

```python
action_type_map = {
    'memory': self.memory_handler,
    'meta': self.meta_handler,
    'system': self.system_handler,
    'user': self.user_handler
}

# Confidence threshold for execution
if intent.confidence >= 0.85:
    handler = action_type_map[intent.action_type]
    return handler.execute(intent.action_category, intent.extracted_params, context)
elif intent.confidence >= 0.70:
    # Ask for confirmation
    return self._request_confirmation(intent)
else:
    # Treat as conversation, but suggest action if helpful
    return self._suggest_action(intent)
```

---

### 3. Memory Action Handler

**Purpose:** Core memory operations (view, save, analyze, export, manage).

**File:** `persona_layer/memory_action_handler.py`

**Interface:**
```python
@dataclass
class ActionResult:
    """Result from action execution"""
    success: bool
    response_text: str              # Natural language response to user
    data: Optional[Dict]            # Structured data (for export/analysis)
    metadata: Dict[str, Any]        # Action metadata (timing, records affected)
    suggestions: List[str]          # Follow-up action suggestions

class MemoryActionHandler:
    """
    Handles memory-related actions using existing memory APIs.

    Memory Systems Accessed:
    - R-Matrix: organ_coupling_learner (11×11 Hebbian coupling)
    - Organic Families: phase5_learning.families (57D clustering)
    - V0 Targets: family_v0_learner (learned convergence targets)
    - Session Registry: sessions/session_registry.json
    - User State: Bundle/user_{token}/user_state.json
    - Conversation Logs: results/interactive_sessions/
    """

    def __init__(self, organism: ConversationalOrganismWrapper):
        self.organism = organism

    def execute(self, action_category: str, params: Dict, context: Dict) -> ActionResult:
        """Execute memory action based on category"""
```

**Action Categories:**

#### 3.1 View Actions

**View History:**
```python
def view_history(self, params: Dict, context: Dict) -> ActionResult:
    """
    Show conversation history with filters.

    Params:
        timeframe: 'session', 'today', 'week', 'all'
        family: Optional family_id filter
        min_satisfaction: Optional threshold

    Returns:
        Formatted conversation list with metadata
    """
    # Access session_registry.json
    # Filter by timeframe and family
    # Format with emoji indicators for satisfaction level
```

**View Families:**
```python
def view_families(self, params: Dict, context: Dict) -> ActionResult:
    """
    Show discovered conversation families.

    Returns:
        Family list with:
        - Family ID and maturity level
        - Member count
        - Mean satisfaction
        - Dominant organs
        - Sample conversation examples
    """
    # Access organism.phase5_learning.families
    # Format mature families first
    # Suggest naming for unnamed families
```

**View R-Matrix:**
```python
def view_r_matrix(self, params: Dict, context: Dict) -> ActionResult:
    """
    Show organ coupling matrix evolution.

    Params:
        format: 'summary', 'heatmap_data', 'strongest_pairs'

    Returns:
        R-matrix visualization data or summary
    """
    # Access organism.organ_coupling_learner.R_matrix
    # Format strongest couplings (top 5 pairs)
    # Show diagonal (self-activation) vs off-diagonal (synergies)
```

**View User Profile:**
```python
def view_user_profile(self, params: Dict, context: Dict) -> ActionResult:
    """
    Show what organism knows about user.

    Returns:
        - Total sessions and conversations
        - Dominant conversation families
        - Satisfaction trajectory
        - Learned organ preferences
        - Privacy-aware summary
    """
    # Access Bundle/user_{token}/user_state.json
    # Aggregate family assignments
    # Compute satisfaction trends
```

#### 3.2 Save Actions

**Save/Label Conversation:**
```python
def save_conversation(self, params: Dict, context: Dict) -> ActionResult:
    """
    Label current conversation for future reference.

    Params:
        label: User-provided label (e.g., "burnout recovery")
        scope: 'this_turn', 'last_N', 'session'

    Effects:
        - Add label to session metadata
        - Create bookmark entry
        - Optionally assign to family manually
    """
    # Update session_registry.json with label
    # Store bookmark in user_state.json
    # Confirmation message
```

**Bookmark Moment:**
```python
def bookmark_moment(self, params: Dict, context: Dict) -> ActionResult:
    """
    Bookmark specific turn for later review.

    Stores:
        - Turn number
        - User input
        - Emission response
        - Organism state (V0, organs, nexuses)
    """
```

#### 3.3 Analyze Actions

**Analyze Patterns:**
```python
def analyze_patterns(self, params: Dict, context: Dict) -> ActionResult:
    """
    Analyze patterns across conversations.

    Types:
        - Family evolution (how families form over time)
        - Organ preference (which organs activate most)
        - Satisfaction trends (improving/declining)
        - R-matrix evolution (strengthening couplings)

    Returns:
        Natural language summary with key insights
    """
    # Aggregate data from families, R-matrix, sessions
    # Compute trends
    # Generate insights
```

**Explain Processing:**
```python
def explain_processing(self, params: Dict, context: Dict) -> ActionResult:
    """
    Explain how organism processed specific input.

    Params:
        turn: Which turn to explain (default: last)

    Returns:
        - V0 convergence details (cycles, descent, Kairos)
        - Active organs and their contributions
        - Nexus formation (types, mechanisms)
        - Transduction trajectory (healing/crisis)
        - Emission generation path (direct/fusion/hebbian)
    """
    # Retrieve felt_states from last turn
    # Format detailed breakdown
    # Educational tone
```

#### 3.4 Export Actions

**Export Data:**
```python
def export_data(self, params: Dict, context: Dict) -> ActionResult:
    """
    Export conversation data in various formats.

    Formats:
        - JSON: Raw structured data
        - CSV: Tabular (for spreadsheet analysis)
        - Markdown: Human-readable report
        - TSK: Training record format

    Scope:
        - 'session': Current session only
        - 'user': All user data (privacy-aware)
        - 'families': Family membership data
        - 'r_matrix': Coupling evolution

    Returns:
        File path and format confirmation
    """
    # Serialize requested data
    # Write to results/exports/
    # Provide download path
```

#### 3.5 Manage Actions

**Clear Recent Memory:**
```python
def clear_recent(self, params: Dict, context: Dict) -> ActionResult:
    """
    Clear recent conversation data.

    Scope:
        - 'session': Current session (with confirmation)
        - 'last_N': Last N turns
        - 'bookmarks': Clear bookmarks only

    Safety:
        - Requires explicit confirmation
        - Cannot clear family/R-matrix (permanent learning)
        - Option to archive before clearing
    """
    # Confirmation prompt
    # Archive to results/archives/
    # Remove from active session
```

**Archive Conversations:**
```python
def archive_conversations(self, params: Dict, context: Dict) -> ActionResult:
    """
    Archive old conversations for long-term storage.

    Criteria:
        - Older than N days
        - Low satisfaction (< threshold)
        - Manual selection

    Effects:
        - Move from active to archive directory
        - Preserve family membership (don't unlearn)
        - Update user_state counters
    """
```

---

### 4. Meta-Cognitive Handler

**Purpose:** Inspect organism's internal processing and self-awareness.

**File:** `persona_layer/meta_cognitive_handler.py`

**Interface:**
```python
class MetaCognitiveHandler:
    """
    Handles meta-cognitive queries about organism processing.

    Philosophy:
    - Educational tone (help user understand system)
    - Honest uncertainty (when confidence is low)
    - Process-oriented (explain occasioning, not rules)
    """

    def execute(self, action_category: str, params: Dict, context: Dict) -> ActionResult:
        """Execute meta-cognitive action"""
```

**Action Types:**

#### 4.1 Confidence Inspection

**How Confident:**
```python
def explain_confidence(self, params: Dict, context: Dict) -> ActionResult:
    """
    Explain confidence score for last response.

    Returns:
        - Emission confidence value
        - Emission path (direct/fusion/hebbian)
        - Contributing factors:
            * Nexus count and quality
            * Kairos detection (boost applied?)
            * Organ coherence levels
            * Family guidance (if mature family)
        - What would increase confidence
    """
    # Access last felt_states
    # Break down confidence calculation
    # Suggest improvements
```

#### 4.2 Organ Inspection

**Which Organs Active:**
```python
def show_organ_activity(self, params: Dict, context: Dict) -> ActionResult:
    """
    Show which organs participated and why.

    Returns:
        - Active organs (coherence > threshold)
        - Dominant organs (top 3)
        - Organ-specific metrics:
            * BOND: self-distance
            * NDAM: urgency level
            * EO: polyvagal state
            * CARD: response scale
        - Organ synergies (R-matrix couplings)
    """
```

#### 4.3 Processing Explanation

**Why That Response:**
```python
def explain_response_choice(self, params: Dict, context: Dict) -> ActionResult:
    """
    Explain why organism generated specific response.

    Returns:
        - V0 convergence journey (cycle-by-cycle)
        - Nexus types formed (relational/healing/protective)
        - Transduction trajectory (mechanism transitions)
        - Emission generation:
            * Direct: High-confidence single organ
            * Fusion: Nexus intersection
            * Hebbian: Fallback from learned patterns
        - Family influence (if assigned)
    """
    # Access full processing record
    # Narrative explanation
    # Connect to process philosophy concepts
```

#### 4.4 Learning Inspection

**What Have You Learned:**
```python
def explain_learning(self, params: Dict, context: Dict) -> ActionResult:
    """
    Explain what organism has learned from conversations.

    Returns:
        - Family formation progress
        - Strongest organ couplings (R-matrix)
        - V0 target adjustments per family
        - Conversation count and success rate
        - Learning trajectory (improving?)
    """
    # Aggregate learning metrics
    # Show evolution over time
    # Maturity indicators
```

---

### 5. System Action Handler

**Purpose:** System health, status, and diagnostics.

**File:** `persona_layer/system_action_handler.py`

**Interface:**
```python
class SystemActionHandler:
    """
    Handles system-level queries and diagnostics.

    Actions:
    - Health checks
    - Version info
    - Capability queries
    - Performance metrics
    """
```

**Action Types:**

#### 5.1 Health Check

```python
def check_health(self, params: Dict, context: Dict) -> ActionResult:
    """
    Quick system health check.

    Returns:
        - Organ status (11/11 operational?)
        - Memory systems (R-matrix, families loaded?)
        - Phase 2 status (V0 convergence enabled?)
        - Recent errors/warnings
    """
```

#### 5.2 Capability Query

```python
def show_capabilities(self, params: Dict, context: Dict) -> ActionResult:
    """
    Show what organism can do.

    Returns:
        - 11 organs and their functions
        - Phase completion status (1, 2, T1-T4, 5)
        - Available actions (memory, meta, etc.)
        - Current configuration (from config.py)
    """
```

#### 5.3 Performance Metrics

```python
def show_performance(self, params: Dict, context: Dict) -> ActionResult:
    """
    Show performance metrics from recent processing.

    Returns:
        - Mean processing time
        - Mean V0 descent
        - Mean convergence cycles
        - Mean emission confidence
        - Mean active organs
    """
```

---

### 6. User Preference Handler

**Purpose:** User settings and display preferences.

**File:** `persona_layer/user_preference_handler.py`

**Interface:**
```python
class UserPreferenceHandler:
    """
    Manages user preferences and display settings.

    Settings:
    - Display mode (simple/standard/detailed/debug)
    - Verbosity level
    - Privacy preferences
    - Notification preferences
    """
```

**Action Types:**

#### 6.1 Display Settings

```python
def change_display_mode(self, params: Dict, context: Dict) -> ActionResult:
    """
    Change interactive display mode.

    Modes:
        - simple: Just emission
        - standard: + confidence + nexuses
        - detailed: + organs + transduction
        - debug: + V0 convergence
    """
```

#### 6.2 Privacy Settings

```python
def configure_privacy(self, params: Dict, context: Dict) -> ActionResult:
    """
    Configure privacy preferences.

    Settings:
        - Export: Allow/disallow data export
        - Learning: Participate in family learning
        - Retention: Auto-archive after N days
        - Anonymization: Remove identifying info
    """
```

---

## Integration with Interactive Mode

**Modified:** `dae_interactive.py`

```python
class InteractiveSession:
    """Enhanced with action system"""

    def __init__(self, mode='standard'):
        # ... existing initialization ...

        # Initialize action system
        self.intent_classifier = UserActionIntentClassifier()
        self.action_dispatcher = UserActionDispatcher(self.organism)

    def process_input(self, user_input: str) -> dict:
        """Enhanced to handle actions"""

        # 1. Classify intent
        intent = self.intent_classifier.classify(
            user_input,
            context={'session_id': self.session_id,
                    'turn': len(self.conversation_history)}
        )

        # 2. If high-confidence action, dispatch
        if intent.is_action and intent.confidence >= 0.85:
            action_result = self.action_dispatcher.dispatch(intent, context)
            return self._format_action_response(action_result)

        # 3. If medium-confidence action, confirm
        elif intent.is_action and intent.confidence >= 0.70:
            return self._request_action_confirmation(intent)

        # 4. Otherwise, process as conversation
        else:
            # Existing organism processing
            result = self.organism.process_text(
                user_input,
                context=context,
                enable_tsk_recording=self.enable_tsk_recording,
                enable_phase2=self.enable_phase2
            )
            return result
```

---

## Data Formats

### Intent Classification Schema

```json
{
  "is_action": true,
  "action_type": "memory",
  "action_category": "view",
  "confidence": 0.96,
  "extracted_params": {
    "timeframe": "session",
    "format": "summary"
  },
  "conversational_component": ""
}
```

### Action Result Schema

```json
{
  "success": true,
  "response_text": "Here are your conversation families:\n\n**Family_001** (mature, 30 members)\n- Mean satisfaction: 0.82\n- Dominant organs: WISDOM, EMPATHY, AUTHENTICITY\n- Example: 'burnout recovery conversations'\n\nYou have 1 mature family so far. As we continue, more patterns will emerge!",
  "data": {
    "families": [
      {
        "family_id": "Family_001",
        "member_count": 30,
        "maturity_level": "mature",
        "mean_satisfaction": 0.82,
        "dominant_organs": ["WISDOM", "EMPATHY", "AUTHENTICITY"]
      }
    ]
  },
  "metadata": {
    "action_type": "memory",
    "action_category": "view_families",
    "execution_time": 0.015,
    "records_retrieved": 1
  },
  "suggestions": [
    "Try 'Show me Family_001 conversations' to see examples",
    "Use 'Analyze family evolution' to see how families formed"
  ]
}
```

### Export Format (JSON)

```json
{
  "export_type": "user_data",
  "user_token": "link_20251111_e8936e",
  "export_timestamp": "2025-11-13T10:30:00",
  "conversations": [
    {
      "session_id": "session_link_20251111_e8936e_20251111_070949",
      "turn": 1,
      "timestamp": "2025-11-11T07:10:15",
      "user_input": "I'm feeling overwhelmed right now",
      "emission": "...",
      "confidence": 0.65,
      "family_assigned": "Family_001",
      "organs_active": ["BOND", "EO", "NDAM", "EMPATHY"],
      "v0_descent": 0.85,
      "satisfaction": 0.78
    }
  ],
  "families": {
    "Family_001": {
      "member_count": 30,
      "mean_satisfaction": 0.82
    }
  },
  "r_matrix_snapshot": [[1.0, 0.15, ...], ...],
  "statistics": {
    "total_conversations": 30,
    "mean_satisfaction": 0.78,
    "most_active_organs": ["WISDOM", "EMPATHY", "BOND"]
  }
}
```

---

## Error Handling

### Graceful Failures

```python
class ActionError(Exception):
    """Base exception for action errors"""
    pass

class InsufficientDataError(ActionError):
    """Not enough data to complete action"""
    pass

class PrivacyViolationError(ActionError):
    """Action would violate privacy settings"""
    pass

class ConfirmationRequiredError(ActionError):
    """Destructive action requires explicit confirmation"""
    pass

# Error responses are conversational
def handle_insufficient_data():
    return ActionResult(
        success=False,
        response_text="I don't have enough conversation data yet to show patterns. "
                     "After a few more conversations, I'll be able to identify families!",
        suggestions=["Continue conversing to build up data"]
    )

def handle_privacy_violation():
    return ActionResult(
        success=False,
        response_text="Your privacy settings don't allow that action. "
                     "You can change settings with 'Configure privacy'.",
        suggestions=["Try 'Show privacy settings'"]
    )
```

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1)
- [ ] Intent classifier with pattern matching
- [ ] Action dispatcher with routing
- [ ] Memory API layer (unified access)
- [ ] ActionResult formatting

### Phase 2: Memory Actions (Week 2)
- [ ] View actions (history, families, R-matrix)
- [ ] Save actions (labels, bookmarks)
- [ ] Export actions (JSON, CSV, Markdown)

### Phase 3: Meta-Cognitive Actions (Week 3)
- [ ] Confidence inspection
- [ ] Organ activity display
- [ ] Processing explanation
- [ ] Learning summary

### Phase 4: Integration & Polish (Week 4)
- [ ] Interactive mode integration
- [ ] Comprehensive testing
- [ ] Error handling
- [ ] Documentation

### Phase 5: Advanced Features (Future)
- [ ] Visualization generation
- [ ] Comparative analysis
- [ ] Predictive insights
- [ ] Export to external tools

---

## Testing Strategy

### Unit Tests

```python
def test_intent_classification():
    classifier = UserActionIntentClassifier()

    # High-confidence action
    intent = classifier.classify("Show me my conversation history", {})
    assert intent.is_action == True
    assert intent.action_type == "memory"
    assert intent.action_category == "view"
    assert intent.confidence >= 0.95

    # Conversational (not action)
    intent = classifier.classify("I remember feeling overwhelmed", {})
    assert intent.is_action == False
    assert intent.confidence < 0.20

def test_memory_actions():
    handler = MemoryActionHandler(organism)

    result = handler.view_families({}, context)
    assert result.success == True
    assert "Family_001" in result.response_text
    assert len(result.data['families']) > 0
```

### Integration Tests

```python
def test_action_end_to_end():
    session = InteractiveSession()

    # User asks for families
    result = session.process_input("What families have you discovered?")

    assert "Family_001" in result['response_text']
    assert result['action_executed'] == True

    # User continues conversation
    result = session.process_input("I'm feeling better today")

    assert result['action_executed'] == False
    assert 'emission_text' in result['felt_states']
```

---

## Next Steps

1. Review this architecture with stakeholders
2. Create command taxonomy document (see USER_ACTION_COMMAND_TAXONOMY.md)
3. Create implementation specification (see USER_ACTION_IMPLEMENTATION_SPEC.md)
4. Begin Phase 1 development

---

**Document Status:** ✅ READY FOR REVIEW
**Next Document:** USER_ACTION_COMMAND_TAXONOMY.md
