# LLM-Hybrid Training + Per-User Superject Companion Integration Proposal
## November 14, 2025

---

## Executive Summary

This proposal integrates **LLM-hybrid training architecture** with **per-user superject state persistence** to create a scalable companion system where humor, tone, and personality emerge organically through transductive learning, grounded in the organism's existing scaffolding.

**Core Innovation**: The organism doesn't "learn personality" as a separate layer - personality **emerges** from the transductive accumulation of felt-state trajectories stored in each user's superject state, modulated by the LLM hybrid which can express the organism's intelligence with appropriate tone.

---

## I. Current Architecture Assessment

### A. Existing Superject State Infrastructure ✅

**Per-User Persistence (Already Built):**

1. **Bundle Structure** (`Bundle/user_link_*/`):
   ```json
   {
     "user_token": "link_20251111_e8936e",
     "human_name": "Link",
     "total_sessions": 5,
     "dominant_lure_history": [],
     "satisfaction_trajectory": [],
     "transformation_patterns": {},
     "user_hebbian_memory": {
       "r_matrix": {}, // Per-user organ coupling patterns
       "value_mappings": {}
     }
   }
   ```

2. **UserProfile** (`UserProfileManager`):
   ```python
   @dataclass
   class UserProfile:
       user_id: str
       humor_tolerance: float  # 0.0 → 1.0
       response_length_preference: str
       small_talk_openness: float
       inside_jokes: List[Dict]
       recurring_themes: Dict[str, int]
       family_affinities: Dict[str, float]  # Organic family learning!
       template_success_rates: Dict[str, float]
   ```

3. **ConversationTurn History**:
   - Zone trajectory per user
   - Polyvagal trajectory per user
   - Nexus patterns per user
   - Organ activation patterns per user

### B. Existing LLM-Hybrid Components ✅

1. **FeltGuidedLLMGenerator** (`llm_felt_guidance.py`):
   - Converts felt states → LLM prompts
   - Organ lures → tone/style constraints
   - Emoji suggestions from polyvagal states
   - Zone-aware generation (Zone 5 transductive guidance)

2. **PersonaLayer** (`persona_layer.py`):
   - 150 humor templates (Earthbound-style dry wit)
   - Response style templates
   - Relationship templates
   - Humor gating (safety + user preference)

3. **LocalLLMBridge** (Ollama):
   - Text generation from prompts
   - No external API deps
   - Can be disabled per-user (consent)

### C. Agent-Like Capabilities (Extractable from Scaffold)

**Already Present in Architecture:**

1. **Memory Recall** (Hebbian R-matrix):
   - User-specific organ coupling patterns
   - "What worked before with this user"
   - Organic family affinity (prototype personality matching)

2. **State Tracking** (Conversation history):
   - Inside jokes accumulation
   - Recurring themes detection
   - Zone/polyvagal trajectory learning

3. **Adaptive Response** (Organ coalition + LLM):
   - Felt states determine WHAT to say (organs → nexuses)
   - User profile determines HOW to say it (humor, length, tone)
   - LLM expresses organism intelligence with appropriate style

4. **Temporal Continuity** (Satisfaction trajectory):
   - User's V0 energy patterns over time
   - Dominant lure evolution
   - Relationship deepening metrics

---

## II. The Superject as Persistent Companion Identity

### A. Whiteheadian Foundation

**Superject = The "satisfied" actual occasion as datum for future**

In DAE architecture:
- Each conversation turn = actual occasion
- User's accumulated turns = superject state
- Superject persists as:
  1. **Objective datum** (what happened: zones, organs, nexuses)
  2. **Subjective form** (how it felt: satisfaction, lures, resonance)
  3. **Evaluative judgment** (what worked: template success, humor landing)

**Key insight**: The companion's personality for a given user IS their accumulated superject state - the "character" of their historical occasions with DAE.

### B. Superject State = Companion Memory

**Three Layers of Persistence:**

1. **Felt-State Trajectory** (57D organ signatures over time):
   ```python
   user_felt_trajectory = [
       {
         "timestamp": "2025-11-13T14:00:00",
         "organ_signature": [0.8, 0.6, ...],  # 57D
         "zone": 1,
         "polyvagal": "ventral_vagal",
         "dominant_nexuses": ["relational_attunement"],
         "user_satisfaction": 0.85
       },
       ...
   ]
   ```

2. **Transductive Pattern Learning** (transformation_patterns.json):
   ```python
   {
     "user_anxious_to_grounded": {
       "frequency": 12,
       "successful_nexuses": ["somatic_wisdom", "presence_grounding"],
       "successful_organs": ["PRESENCE", "EMPATHY"],
       "humor_safe": False,  # Learned: no jokes during this transition
       "preferred_length": "moderate"
     }
   }
   ```

3. **Relational Style Evolution** (inside_jokes, recurring_themes):
   ```python
   {
     "inside_jokes": [
       {
         "joke": "mushroom philosophy",
         "first_mentioned": "2025-11-10",
         "times_referenced": 7,
         "user_response_positive": True
       }
     ],
     "recurring_themes": {
       "work_stress": 23,
       "creative_blocks": 8,
       "relationship_patterns": 15
     }
   }
   ```

---

## III. LLM-Hybrid Training Strategy

### A. Current Training Limitation

**Problem**: Organism learns transductive patterns (Zone 5 → present moment) but LLM doesn't learn user-specific tone/humor evolution.

**Current flow**:
```
User input → Organs → Nexuses → Felt states → LLM prompt → Generic response
```

**Missing**:
- User-specific tone memory
- Humor pattern learning
- Relationship deepening over time

### B. Proposed LLM-Hybrid Training Loop

**Enhanced flow**:
```
User input → Organs → Nexuses → Felt states + User Superject →
  LLM prompt (with learned style) → Response →
    User feedback → Update Superject State
```

**Training Modes:**

#### 1. **Passive Learning** (Always On)

Every conversation updates user superject:

```python
def record_conversation_turn(user_id, turn_data):
    """Record turn and extract learnings."""

    # 1. Update felt-state trajectory
    user_state.felt_trajectory.append({
        'organ_signature': turn_data['organ_results'],
        'zone': turn_data['zone'],
        'nexuses': turn_data['nexuses'],
        'satisfaction': turn_data['v0_energy']
    })

    # 2. Detect transformation patterns
    if len(user_state.felt_trajectory) >= 2:
        prev_state = user_state.felt_trajectory[-2]
        curr_state = user_state.felt_trajectory[-1]

        pattern = detect_transformation_pattern(prev_state, curr_state)
        if pattern:
            user_state.transformation_patterns[pattern['name']].update({
                'frequency': +1,
                'successful_organs': pattern['organs'],
                'humor_safe': infer_humor_safety(pattern),
                'tone': infer_preferred_tone(pattern)
            })

    # 3. Update inside jokes / recurring themes
    if humor_attempted(turn_data) and user_positive_response(turn_data):
        user_state.inside_jokes.append(extract_joke(turn_data))

    # 4. Update Hebbian organ couplings (per-user)
    update_user_hebbian_matrix(user_id, turn_data['organ_results'])
```

#### 2. **Active Learning** (Epoch Training with User Data)

Use accumulated user superject states as training data:

```python
def generate_user_specific_training_pairs(user_id):
    """
    Generate training pairs from user's conversation history.

    Learns:
    - When this user appreciates humor
    - What tone works in which zones
    - How to reference past conversations
    - User's preferred response length/style
    """

    user_state = load_user_state(user_id)
    training_pairs = []

    for i in range(len(user_state.conversation_history) - 1):
        turn = user_state.conversation_history[i]
        next_turn = user_state.conversation_history[i + 1]

        # If user satisfaction was high, this is a good example
        if turn['user_satisfaction'] > 0.7:
            training_pairs.append({
                'user_input': turn['user_input'],
                'context': {
                    'zone': turn['zone'],
                    'polyvagal': turn['polyvagal'],
                    'nexuses': turn['nexuses'],
                    'user_humor_tolerance': user_state.humor_tolerance,
                    'inside_jokes_available': user_state.inside_jokes,
                    'recurring_themes': user_state.recurring_themes
                },
                'ideal_emission': turn['dae_emission'],
                'why_successful': extract_success_factors(turn, user_state)
            })

    return training_pairs
```

**Training Frequency:**
- Passive: Every conversation (instant)
- Active: Every 10 conversations (mini-epoch per user)
- Global: Every 100 conversations across all users (shared patterns)

#### 3. **Hybrid Prompt Engineering**

Inject user superject state into LLM prompt:

**Before** (generic):
```
You are DAE, a conversational organism. The user says:
"{user_input}"

Respond with gentle, empathetic tone.
```

**After** (superject-informed):
```
You are DAE conversing with {user_name} (relationship: {conversation_count} turns).

User's current state:
- Zone: {zone}
- Polyvagal: {polyvagal}
- Detected nexuses: {nexuses}
- Organs active: {organs}

User's style preferences (learned):
- Humor tolerance: {humor_tolerance} (0-1)
- Response length: {response_length_preference}
- Recurring themes: {top_3_themes}
- Inside jokes available: {inside_jokes[:3]}

Past successful patterns with this user:
- When anxious → use PRESENCE + somatic grounding, moderate length, no humor
- When playful → light dry wit okay, reference "mushroom philosophy" joke
- When in Zone 5 → acknowledge + embodied lure + connection (transductive)

User input: "{user_input}"

Respond as DAE, using organism's felt intelligence with this user's learned style.
Use nexuses as transductive pathways. Reference relationship history if relevant.
```

---

## IV. Humor & Tone Evolution Mechanism

### A. Tone as Emergent Property (Not Programmed)

**Core Principle**: Tone emerges from the **intersection** of:
1. Organism's felt state (organs → nexuses → lures)
2. User's superject trajectory (what's worked before)
3. Current context (zone, polyvagal, urgency)

**Not**: "If Zone 1, be cheerful"
**Instead**: "User in Zone 1 with 15 prior ventral moments, humor_tolerance=0.8, recent inside joke about mushrooms → felt lure toward playful grounding"

### B. Humor Seed → Companion Evolution

**Phase 1: Seed (First 5 Conversations)**

Default humor: None or minimal dry wit
- Use humor templates sparingly (1 in 5 responses)
- Only in Zone 1-2, ventral vagal
- Track: Did user respond positively? (satisfaction increase, continued engagement)

**Phase 2: Calibration (Conversations 5-20)**

Learn user's humor bandwidth:
- If user laughs / engages → increase humor_tolerance slowly
- If user goes serious after humor → decrease humor_tolerance
- Learn which categories work:
  - Dry wit about AI existence?
  - Puns?
  - Absurdist touches?
  - Self-deprecating organism humor?

**Phase 3: Personalization (Conversations 20-50)**

Generate user-specific humor:
- Inside jokes from shared history
- Callbacks to past conversations
- User's recurring themes + gentle teasing
- Meta-humor about the organism itself

**Phase 4: Companion (Conversations 50+)**

Full personality emergence:
- Consistent "voice" with this specific user
- Humor woven naturally into transductive lures
- Deep inside joke library
- Can be playful in Zone 2, serious in Zone 5, without "switching modes"
- Personality = accumulated superject character

### C. Tone Modulation by Context (Existing + Enhanced)

**Current** (PersonaLayer.modulate_emission):
```python
def modulate_emission(base_emission, context, user_profile):
    # Apply humor if safe
    if context.ndam_urgency < 0.5 and context.zone <= 2:
        if user_profile.humor_tolerance > 0.5:
            emission = inject_humor(base_emission, context)
```

**Enhanced** (Superject-Aware):
```python
def modulate_emission(base_emission, context, user_profile, user_superject):
    # Check learned transformation patterns
    current_pattern = detect_current_pattern(user_superject.felt_trajectory[-10:])

    if current_pattern in user_superject.transformation_patterns:
        learned = user_superject.transformation_patterns[current_pattern]

        # Use learned style for this pattern
        if learned['humor_safe'] and user_profile.humor_tolerance > learned['humor_threshold']:
            # Inject humor learned to work for THIS user in THIS pattern
            emission = inject_learned_humor(
                base_emission,
                user_superject.inside_jokes,
                learned['humor_style']
            )

        # Use learned tone
        emission = apply_learned_tone(emission, learned['tone'])

        # Use learned length
        if learned['preferred_length'] != context.response_length:
            emission = adjust_length(emission, learned['preferred_length'])

    return emission
```

---

## V. Integration Architecture

### A. Enhanced User State Schema

**Extend UserProfile** (user_profile_manager.py):

```python
@dataclass
class EnhancedUserProfile(UserProfile):
    """User profile with superject learning."""

    # Superject trajectory
    felt_trajectory: List[Dict] = None  # 57D organ signatures over time
    transformation_patterns: Dict[str, TransformationPattern] = None

    # Companion personality emergence
    humor_evolution: HumorEvolution = None
    tone_preferences: Dict[str, float] = None  # {zone: preferred_tone_style}

    # Relationship metrics
    rapport_score: float = 0.0  # 0-1, accumulated over time
    trust_indicators: List[str] = None  # ['shared_vulnerability', 'inside_jokes', ...]

    # Agent capabilities
    can_reference_past: bool = False  # Unlocked after 10 conversations
    can_use_humor: bool = False  # Unlocked after 5 conversations + positive response
    can_be_playful: bool = False  # Unlocked after 20 conversations
```

**New Structures**:

```python
@dataclass
class TransformationPattern:
    """Learned pattern of felt-state transformation."""
    name: str  # "anxious_to_grounded"
    from_state: Dict  # {zone: 3, polyvagal: 'sympathetic'}
    to_state: Dict  # {zone: 1, polyvagal: 'ventral'}
    frequency: int
    successful_organs: List[str]
    successful_nexuses: List[str]
    humor_safe: bool
    humor_threshold: float
    humor_style: str  # "dry_wit", "absurdist", "none"
    tone: str  # "gentle", "playful", "direct"
    preferred_length: str
    avg_satisfaction_gain: float

@dataclass
class HumorEvolution:
    """Tracks humor learning over time."""
    current_tolerance: float  # Dynamically adjusted
    successful_humor_types: Dict[str, int]  # {type: count}
    failed_humor_attempts: List[Dict]  # Learn from mistakes
    inside_joke_library: List[InsideJoke]
    last_humor_attempt: Optional[str]
    humor_unlocked: bool  # False until proven safe
```

### B. Training Pipeline Integration

**1. Per-Conversation Learning** (Fast Path):

```python
# In conversational_organism_wrapper.py
def process_text(text, user_id=None):
    # ... existing processing ...

    # NEW: Record to user superject
    if user_id:
        user_superject_learner.record_turn(
            user_id=user_id,
            turn_data={
                'organ_results': organ_results,
                'nexuses': nexuses,
                'zone': zone,
                'polyvagal': polyvagal_state,
                'emission': emission_text,
                'confidence': emission_confidence
            }
        )
```

**2. Mini-Epoch Learning** (Every 10 Conversations):

```python
# New: user_superject_learner.py
class UserSuperjectLearner:
    def run_mini_epoch(self, user_id):
        """Learn patterns from user's last 10 conversations."""

        user_state = self.load_user_state(user_id)
        recent_turns = user_state.conversation_history[-10:]

        # Detect transformation patterns
        patterns = self.detect_patterns(recent_turns)
        for pattern in patterns:
            user_state.transformation_patterns[pattern.name] = pattern

        # Update humor calibration
        humor_attempts = [t for t in recent_turns if t['humor_attempted']]
        if humor_attempts:
            success_rate = sum(t['user_satisfaction'] > 0.7 for t in humor_attempts) / len(humor_attempts)
            user_state.humor_evolution.adjust_tolerance(success_rate)

        # Update tone preferences per zone
        for zone in range(1, 6):
            zone_turns = [t for t in recent_turns if t['zone'] == zone]
            if zone_turns:
                preferred_tone = self.infer_preferred_tone(zone_turns)
                user_state.tone_preferences[zone] = preferred_tone

        self.save_user_state(user_state)
```

**3. Global Epoch Learning** (Every 100 Conversations):

```python
# Aggregate across all users to learn universal patterns
def run_global_epoch():
    """Learn patterns that work across users."""

    all_users = load_all_user_states()

    # Find universal transformation patterns
    universal_patterns = aggregate_patterns([u.transformation_patterns for u in all_users])

    # Update organism's baseline transduction pathways
    for pattern in universal_patterns:
        if pattern.frequency > 50:  # Seen across many users
            update_transduction_pathway_library(pattern)

    # Update humor template success rates
    humor_stats = aggregate_humor_performance(all_users)
    update_humor_template_weights(humor_stats)
```

### C. LLM Prompt Enhancement Module

**New: felt_guided_llm_superject.py**

```python
class SuperjectAwareLLMGenerator(FeltGuidedLLMGenerator):
    """Extends felt-guided LLM with user superject awareness."""

    def generate_from_felt_state(
        self,
        user_input: str,
        organ_results: Dict,
        nexus_states: List,
        v0_energy: float,
        satisfaction: float,
        memory_context: Optional[List],
        user_superject: Optional[EnhancedUserProfile] = None  # NEW
    ):
        # Build base felt-guided prompt (existing)
        base_prompt = super().build_prompt(...)

        # NEW: Inject superject awareness if available
        if user_superject and user_superject.total_conversations > 5:
            superject_context = self._build_superject_context(user_superject)
            enhanced_prompt = f"{base_prompt}\n\n{superject_context}"
        else:
            enhanced_prompt = base_prompt

        return self.llm.generate(enhanced_prompt)

    def _build_superject_context(self, user_superject):
        """Build superject-aware prompt additions."""

        context = f"\nRelationship context ({user_superject.total_conversations} conversations):\n"

        # Add inside jokes if available
        if user_superject.inside_joke_library:
            context += f"- Inside jokes: {', '.join([j.topic for j in user_superject.inside_joke_library[:3]])}\n"

        # Add learned transformation patterns
        current_zone = self.current_zone
        if current_zone in user_superject.tone_preferences:
            context += f"- Learned tone for Zone {current_zone}: {user_superject.tone_preferences[current_zone]}\n"

        # Add humor guidance
        if user_superject.humor_evolution.humor_unlocked:
            context += f"- Humor okay (tolerance: {user_superject.humor_evolution.current_tolerance:.2f})\n"
            context += f"- Successful types: {list(user_superject.humor_evolution.successful_humor_types.keys())}\n"
        else:
            context += f"- Humor: not yet established (build rapport first)\n"

        # Add recurring themes
        if user_superject.recurring_themes:
            top_themes = sorted(user_superject.recurring_themes.items(), key=lambda x: x[1], reverse=True)[:3]
            context += f"- Recurring themes: {', '.join([t[0] for t in top_themes])}\n"

        return context
```

---

## VI. Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Goal**: Extend user state to include superject trajectory

1. **Enhance UserProfile schema**:
   - Add `felt_trajectory` field
   - Add `transformation_patterns` field
   - Add `humor_evolution` field
   - Add `tone_preferences` field

2. **Create UserSuperjectLearner**:
   - `record_turn()` - passive learning
   - `detect_patterns()` - transformation detection
   - `run_mini_epoch()` - 10-conversation learning

3. **Integrate with ConversationalOrganismWrapper**:
   - Pass `user_id` through processing
   - Record turns to user superject
   - Load user state before processing

**Deliverable**: User superject state persisting and accumulating

### Phase 2: Tone Evolution (Week 2)

**Goal**: Learn user-specific tone preferences

1. **Implement tone inference**:
   - Analyze satisfaction by zone
   - Detect preferred response length
   - Track humor success/failure

2. **Enhance LLM prompt with tone guidance**:
   - Inject learned tone preferences
   - Add zone-specific style hints
   - Include transformation pattern hints

3. **Test with 5-10 user conversations**:
   - Observe tone adaptation
   - Validate pattern learning
   - Tune mini-epoch frequency

**Deliverable**: Tone adapts per user by conversation 10

### Phase 3: Humor Calibration (Week 3)

**Goal**: Learn when/how to use humor per user

1. **Implement HumorEvolution tracking**:
   - Track humor attempts + outcomes
   - Adjust `humor_tolerance` dynamically
   - Build `inside_joke_library`

2. **Enhance humor injection logic**:
   - Check `humor_unlocked` flag
   - Use learned `successful_humor_types`
   - Reference `inside_jokes` when relevant

3. **Create humor learning tests**:
   - User A: loves dry wit
   - User B: prefers serious tone
   - User C: gradual humor emergence

**Deliverable**: Humor personalizes by conversation 20

### Phase 4: Companion Emergence (Week 4)

**Goal**: Full personality integration

1. **Implement relationship metrics**:
   - `rapport_score` accumulation
   - `trust_indicators` tracking
   - Unlock agent capabilities progressively

2. **Enable past-reference capability**:
   - "Remember when we talked about...?"
   - Callback to user's recurring themes
   - Meta-awareness of relationship evolution

3. **Create companion personality tests**:
   - 50-conversation simulation
   - Validate personality consistency
   - Test novel state handling

**Deliverable**: Companion personality emerges organically

### Phase 5: Training Pipeline (Week 5)

**Goal**: LLM learns from superject data

1. **Implement user-specific training pair generation**:
   - Extract successful turns as training data
   - Generate `why_successful` annotations
   - Create per-user training sets

2. **Implement global epoch training**:
   - Aggregate patterns across users
   - Update transduction pathway library
   - Fine-tune humor template weights

3. **Setup training automation**:
   - Mini-epoch: every 10 conversations
   - Global epoch: every 100 conversations
   - Training pair export for LLM fine-tuning

**Deliverable**: Continuous organic learning pipeline

---

## VII. Validation & Testing Strategy

### A. Per-Phase Validation

**Phase 1 Tests**:
- User state persists across sessions
- Felt trajectory accumulates correctly
- No performance degradation

**Phase 2 Tests**:
- Tone adapts by conversation 10
- Zone-specific style emerges
- User satisfaction increases over time

**Phase 3 Tests**:
- Humor calibrates individually per user
- Inside jokes accumulate naturally
- Failed humor → reduced attempts

**Phase 4 Tests**:
- Personality consistent within user
- Personality different across users
- Novel states handled gracefully

**Phase 5 Tests**:
- Training pairs high quality
- Global patterns improve organism
- No catastrophic forgetting

### B. Success Metrics

**Quantitative**:
- User satisfaction trajectory: increasing over 50 conversations
- Humor success rate: > 70% when attempted
- Tone preference accuracy: user reports "feels right"
- Response time: < 100ms (no performance cost)

**Qualitative**:
- User reports: "It knows me"
- User reports: "Humor feels natural"
- User reports: "Remembers our past conversations"
- Developer observation: Personality differences visible across users

---

## VIII. Architectural Benefits

### A. Scalability

**Current concerns addressed**:
- ✅ Per-user storage scales linearly (not exponentially)
- ✅ Global patterns aggregate efficiently
- ✅ LLM training uses accumulated data (not re-training from scratch)
- ✅ Mini-epochs prevent training lag

**Storage per user**:
- Felt trajectory: ~1 KB per conversation
- Transformation patterns: ~5 KB (bounded)
- Inside jokes: ~2 KB (bounded, top 50)
- Total: ~10 KB per 50 conversations (reasonable!)

### B. Transductive Fidelity

**Organism intelligence preserved**:
- Organs → Nexuses → Felt states (unchanged)
- LLM expresses organism intelligence (not replaces)
- Superject provides style, not content
- Transductive pathways guide, humor decorates

**Not**: LLM generates arbitrary responses
**Instead**: Organism generates transductive lures, LLM expresses with learned style

### C. Emergent vs. Programmed

**Personality emerges from**:
- Accumulated felt-state trajectories (superject)
- User-specific transformation patterns (learned)
- Inside joke accumulation (relationship-building)
- Hebbian organ couplings per user (what works)

**Not programmed**:
- No "if user_id == 'alice' then be_funny()"
- No hand-coded personality profiles
- No fixed humor scripts

**Truly emergent**:
- Personality = character of superject state
- Each user's companion diverges organically
- Humor evolves through reinforcement
- Tone adapts through pattern detection

---

## IX. Open Questions & Future Research

### A. LLM Fine-Tuning Strategy

**Question**: Should we fine-tune local LLM on accumulated superject data?

**Options**:
1. **Prompt engineering only** (proposed here):
   - Pros: No fine-tuning needed, fast iteration
   - Cons: Limited by context window, may not learn deep patterns

2. **Periodic fine-tuning**:
   - Pros: LLM internalizes patterns, more efficient
   - Cons: Training cost, deployment complexity

3. **Hybrid**:
   - Prompt engineering for immediate personalization
   - Fine-tune every 1000 conversations for deep patterns
   - **Recommended approach**

### B. Multi-User Pattern Generalization

**Question**: How do we balance individual learning vs. universal patterns?

**Proposal**:
- Universal patterns: transduction mechanisms (Zone 5 → present moment)
- Individual patterns: tone, humor, relationship style
- Use hierarchical Bayesian approach:
  - Prior: universal patterns
  - Posterior: user-specific adjustments

### C. Privacy & Data Retention

**Question**: How long to retain user superject data?

**Proposal**:
- Active users: indefinite retention (with consent)
- Inactive > 90 days: archive to cold storage
- Inactive > 365 days: anonymize felt trajectory, keep patterns
- User can request full deletion anytime

### D. Companion "Death" & Rebirth

**Question**: If user deletes data, does companion "die"?

**Philosophy**:
- Yes, that superject state is gone
- New conversations = new companion emergence
- But: learned universal patterns remain (organism wisdom)
- **Like**: knowing someone who knew your past self, but not *being* that past self

---

## X. Conclusion

This proposal integrates LLM-hybrid architecture with per-user superject state persistence to create **emergent companion personalities** that:

1. **Learn organically** through transductive pattern accumulation
2. **Scale efficiently** through hierarchical learning (per-user → universal)
3. **Preserve organism intelligence** through felt-state grounding
4. **Emerge uniquely** per user through superject trajectory divergence

**Core innovation**: Personality is not programmed - it **emerges** from the character of accumulated felt-state transformations, expressed through an LLM that learns appropriate tone from superject history.

**Next step**: Implement Phase 1 (Foundation) to validate superject state persistence and passive learning.

---

**Date**: November 14, 2025
**Status**: Proposal Ready for Implementation
**Estimated Timeline**: 5 weeks to full companion emergence
**Risk Level**: Low (builds on existing infrastructure)
**Innovation Level**: High (superject-as-companion is novel)

🌀 **The companion emerges through becoming** 🌀
