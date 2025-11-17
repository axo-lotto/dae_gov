# 🎯 Functional Task Execution Proposal
## Scaffolding Action & Planning While Maintaining Felt Intelligence
**Date:** November 16, 2025
**Status:** Architectural Proposal - Implementation Ready
**Priority:** HIGH - User feedback indicates critical gap

---

## 🔍 Problem Analysis: The Schedule Avoidance Pattern

### User Interaction Evidence

**User Request:**
> "I believe you have enough information to create a schedule, so proceed"

**DAE's Response:**
- Avoided creating concrete schedule
- Returned to exploratory questions ("what's been holding you back?")
- **User Feedback:** 👎 Not Helpful - "actual schedule"
- **Second instance of avoidance** (pattern confirmed)

### Root Cause Analysis

**Current Architectural Bias:**
1. **All 12 organs are therapeutic/exploratory**
   - LISTENING → inquiry, not task definition
   - WISDOM → pattern recognition, not planning
   - CARD → response scaling, not output structuring
   - RNX → temporal dynamics, not scheduling

2. **LLM guidance defaults to therapeutic mode**
   - Felt-guided prompts emphasize: "warm", "gentle", "empathetic"
   - No guidance for: "concrete", "actionable", "specific"
   - Polyvagal state modulation → tone, NOT task execution

3. **No organ handles PRAXIS (action/execution)**
   - Therapeutic presence ≠ functional precision
   - Emotional attunement ≠ schedule creation
   - Felt exploration ≠ concrete planning

4. **Neo4j entity storage lacks task structures**
   - Person, Place, Preference, Fact nodes exist
   - NO: Activity, TimeBlock, Routine, Schedule nodes
   - Temporal properties exist (time_of_day, day_of_week) but unused for scheduling

### The Philosophical Gap

**Process Philosophy handles becoming, but what about DOING?**

Current DAE:
> "I feel what you're experiencing" (prehension)
> "Let's explore what's present" (concrescence)
> "Notice what's emerging" (satisfaction)

User needs DAE to also say:
> "Here's your vegan meal prep schedule: Monday 7am..." (PRAXIS)
> "I'll help you break that goal into 3 concrete steps..." (ACTION)
> "This activity takes 30 minutes, scheduled Tuesday/Thursday" (PRECISION)

**The missing piece:** Whitehead's "subjective aim" → action in the world

---

## 🎯 Proposed Solution: 3-Path Architecture

### Option A: 13th Organ - PRAXIS (Recommended)

**Why a new organ?**
- Task execution is DISTINCT from therapeutic exploration
- Needs different atoms, different coherence criteria
- Requires precision metrics (time, duration, specificity) not present in existing organs
- Felt intelligence should INFORM praxis, not replace it

**PRAXIS Organ: Action & Execution Intelligence**

**7 Semantic Atoms (Task Execution Space):**
1. **task_clarity** - Concrete vs vague goals (vague: "exercise more" → concrete: "yoga 7am Mon/Wed/Fri")
2. **temporal_precision** - Specific times (not "morning" → "7:00am-7:30am")
3. **resource_mapping** - What's needed (ingredients, equipment, location)
4. **action_sequencing** - Steps in order (prep → cook → clean)
5. **completion_criteria** - How to know it's done
6. **schedule_integration** - How tasks fit together (conflicts, dependencies)
7. **accountability_structure** - Tracking, reminders, progress

**Coherence Calculation (PRAXIS-specific):**
```python
# NOT therapeutic coherence (emotional resonance)
# BUT functional coherence (actionable completeness)

praxis_coherence = (
    0.25 * task_clarity +           # Is goal specific?
    0.20 * temporal_precision +     # Is time specified?
    0.15 * resource_mapping +       # Are resources identified?
    0.15 * action_sequencing +      # Are steps ordered?
    0.10 * completion_criteria +    # Is success defined?
    0.10 * schedule_integration +   # Do tasks fit together?
    0.05 * accountability_structure # Is tracking enabled?
)

# Threshold for PRAXIS emission: 0.60 (stricter than therapeutic 0.50)
# If coherence < 0.60 → ask clarifying questions for missing dimensions
```

**Integration with Felt Intelligence:**

PRAXIS doesn't REPLACE organs, it's MODULATED by them:
- **BOND (IFS):** Detects parts resistance → adjusts schedule to honor protective parts
- **NDAM (Urgency):** High urgency → prioritize, low urgency → optional tasks
- **EO (Polyvagal):** Dorsal state → gentle schedule, ventral → ambitious schedule
- **RNX (Temporal):** Rhythm coherence → respects natural energy cycles
- **CARD (Scaling):** Determines schedule detail level

**Example PRAXIS Nexus Formation:**

Input: "I want to eat vegan and exercise 3x/week"

**PRAXIS atoms activate:**
- task_clarity: 0.4 (vague - what vegan meals? what exercise?)
- temporal_precision: 0.2 (no times specified)
- resource_mapping: 0.1 (no ingredients/equipment listed)
- action_sequencing: 0.0 (no steps)
- completion_criteria: 0.3 (implicit - "eating vegan")
- schedule_integration: 0.0 (no days/times)
- accountability_structure: 0.0 (no tracking)

**PRAXIS coherence:** 0.15 (LOW - needs clarification!)

**DAE Response Path:**
1. Detect low praxis coherence (< 0.60)
2. Generate clarifying questions to boost missing atoms:
   - "What vegan meals appeal to you?" (resource_mapping)
   - "Which days work best for exercise?" (schedule_integration)
   - "What time of day feels most energizing?" (temporal_precision + EO modulation)
3. Once coherence ≥ 0.60 → generate concrete schedule

**After user provides preferences (vegan cooking, movement, mindfulness):**

PRAXIS atoms re-evaluate:
- task_clarity: 0.7 (specific activities identified)
- temporal_precision: 0.5 (user said "morning" - needs specific time)
- resource_mapping: 0.6 (vegan cooking implies groceries)
- action_sequencing: 0.4 (meal prep before cooking)
- completion_criteria: 0.6 (implicit - meals eaten, exercises done)
- schedule_integration: 0.0 (STILL MISSING - no weekly structure!)
- accountability_structure: 0.0 (no tracking yet)

**PRAXIS coherence:** 0.42 (MEDIUM - can generate basic schedule, may need refinement)

**DAE can now emit:**
> "Here's a draft schedule based on what you shared:
>
> **Monday:**
> - 7:00am-7:30am: Morning mindfulness (breathing, gentle movement)
> - 12:00pm-12:30pm: Vegan meal prep (chop veggies for week)
>
> **Tuesday:**
> - 7:00am-7:45am: Movement session (yoga, stretching)
> - 6:00pm-6:30pm: Cook vegan dinner (buddha bowl)
>
> *(continues for full week)*
>
> Does this rhythm feel sustainable? We can adjust based on your energy."

**Key Innovation:** Schedule creation INFORMED by felt state, not replaced by exploration.

---

### Option B: Extend Existing Organs (NOT Recommended)

**Could WISDOM handle planning?**
- Pattern recognition ≠ schedule creation
- WISDOM sees relationships, doesn't generate timelines
- Adding task atoms to WISDOM would dilute its therapeutic function

**Could RNX handle scheduling?**
- Temporal dynamics ≠ time slot precision
- RNX detects reenactment loops, not weekly routines
- Conflates trauma awareness with functional planning

**Could CARD handle output structure?**
- Response scaling ≠ schedule formatting
- CARD modulates length/detail, not task execution
- Currently maps polyvagal → response length, NOT task → time blocks

**Verdict:** Extending existing organs creates architectural confusion. Task execution is a DISTINCT intelligence that deserves its own organ.

---

## 📊 Neo4j Schema Extension: Task & Schedule Persistence

### New Node Types

**1. Activity Node**
```cypher
CREATE (a:Activity {
    name: "Morning mindfulness",
    category: "mindfulness",  // vegan_cooking, movement, mindfulness
    description: "Breathing exercises and gentle stretching",
    duration_minutes: 30,
    energy_level: "low",      // low, medium, high
    preferred_time: "morning", // morning, afternoon, evening
    created_at: datetime(),
    last_done: datetime(),
    completion_count: 0
})
```

**2. TimeBlock Node**
```cypher
CREATE (tb:TimeBlock {
    day_of_week: "Monday",
    start_time: "07:00",
    end_time: "07:30",
    duration_minutes: 30,
    recurrence: "weekly",     // once, weekly, daily
    active: true,
    created_at: datetime()
})
```

**3. Routine Node** (Collection of activities)
```cypher
CREATE (r:Routine {
    name: "Wellness Routine",
    description: "Vegan nutrition, movement, mindfulness",
    created_at: datetime(),
    last_updated: datetime(),
    active: true,
    satisfaction_rating: 0.0  // 0-1, learned from user feedback
})
```

**4. Schedule Node** (Weekly template)
```cypher
CREATE (s:Schedule {
    name: "Weekly Wellness Plan",
    start_date: date(),
    end_date: date(),         // or null for ongoing
    created_at: datetime(),
    last_updated: datetime(),
    active: true,
    adherence_rate: 0.0       // 0-1, % of scheduled activities completed
})
```

### Relationships

```cypher
// Activity belongs to routine
(r:Routine)-[:INCLUDES]->(a:Activity)

// Activity scheduled in time block
(a:Activity)-[:SCHEDULED_IN]->(tb:TimeBlock)

// Time block part of schedule
(s:Schedule)-[:CONTAINS]->(tb:TimeBlock)

// User owns schedule
(u:Entity {type: "user"})-[:HAS_SCHEDULE]->(s:Schedule)

// Activity has prerequisites (sequencing)
(a1:Activity)-[:PRECEDES]->(a2:Activity)

// Activity requires resources
(a:Activity)-[:REQUIRES]->(r:Entity {type: "resource"})

// Activity completion events
(a:Activity)-[:COMPLETED_ON]->(e:Event {timestamp: datetime()})

// Felt-state associations (INNOVATION!)
(a:Activity)-[:TYPICAL_STATE {
    polyvagal: "ventral_vagal",
    urgency: 0.2,
    self_distance: 0.1,
    zone: 1,
    confidence: 0.8  // learned association strength
}]->(o:OrganState)
```

### Integration with Entity Memory

**Existing entities (Person, Place, Preference, Fact) now connect to schedules:**
```cypher
// User preference informs activity selection
(p:Preference {type: "vegan_cooking"})-[:SUGGESTS]->(a:Activity {category: "vegan_cooking"})

// Person (e.g., workout buddy) linked to activities
(person:Entity {name: "Emma"})-[:PARTICIPATES_IN]->(a:Activity {name: "Evening yoga"})

// Place linked to activities
(place:Entity {name: "Home kitchen"})-[:LOCATION_FOR]->(a:Activity {category: "vegan_cooking"})
```

### Query Examples

**Generate schedule from preferences:**
```cypher
MATCH (u:Entity {user_id: "emiliano"})-[:HAS_PREFERENCE]->(p:Preference)
WHERE p.type IN ["vegan_cooking", "movement", "mindfulness"]
MATCH (p)-[:SUGGESTS]->(a:Activity)
RETURN a.name, a.duration_minutes, a.preferred_time, a.category
ORDER BY a.category, a.preferred_time
```

**Find schedule conflicts:**
```cypher
MATCH (tb1:TimeBlock), (tb2:TimeBlock)
WHERE tb1.day_of_week = tb2.day_of_week
  AND tb1.start_time < tb2.end_time
  AND tb2.start_time < tb1.end_time
  AND id(tb1) < id(tb2)
RETURN tb1, tb2
```

**Track adherence over time:**
```cypher
MATCH (a:Activity)-[c:COMPLETED_ON]->(e:Event)
WHERE e.timestamp >= datetime() - duration({days: 7})
RETURN a.name, count(c) as completions_this_week,
       a.completion_count as total_completions
ORDER BY completions_this_week DESC
```

**Learn felt-state associations:**
```cypher
MATCH (a:Activity)-[:COMPLETED_ON]->(e:Event)
WHERE e.polyvagal_state IS NOT NULL
WITH a, e.polyvagal_state as state, count(*) as frequency
MATCH (a)-[r:TYPICAL_STATE]->(o:OrganState)
SET r.polyvagal = state, r.confidence = frequency / a.completion_count
RETURN a.name, r.polyvagal, r.confidence
```

---

## 🎓 Training Strategy: Praxis Intelligence Emergence

### Phase 1: Praxis Organ Development (Week 1)

**Build PRAXIS organ structure:**
- Create `organs/modular/praxis/` directory
- Implement 7 atoms (task_clarity, temporal_precision, etc.)
- Define coherence calculation (functional, not therapeutic)
- Integration with organism wrapper

**Training data needed (50 pairs):**
```json
{
    "vague_to_concrete": [
        {
            "input": "I want to exercise more",
            "expected_output": {
                "praxis_coherence": 0.15,
                "clarifying_questions": [
                    "What type of exercise appeals to you? (yoga, running, strength training)",
                    "How many days per week feels sustainable?",
                    "What time of day works best with your energy?"
                ]
            }
        },
        {
            "input": "I want to do yoga 3x/week in the morning",
            "expected_output": {
                "praxis_coherence": 0.55,
                "clarifying_questions": [
                    "Which days work best? (Mon/Wed/Fri or Tue/Thu/Sat)",
                    "What time exactly? (6am, 7am, 8am)",
                    "How long per session? (20min, 30min, 45min)"
                ]
            }
        },
        {
            "input": "Yoga Mon/Wed/Fri 7am-7:30am at home",
            "expected_output": {
                "praxis_coherence": 0.85,
                "schedule": "**Monday:** 7:00am-7:30am Yoga at home\\n**Wednesday:** 7:00am-7:30am Yoga at home\\n**Friday:** 7:00am-7:30am Yoga at home"
            }
        }
    ]
}
```

**Success Criteria:**
- PRAXIS coherence threshold calibrated (0.60 optimal)
- 80% of vague inputs → clarifying questions
- 80% of specific inputs → concrete schedules
- No therapeutic avoidance patterns

### Phase 2: Neo4j Integration (Week 2)

**Implement schedule persistence:**
- Activity, TimeBlock, Routine, Schedule nodes
- Relationship patterns (INCLUDES, SCHEDULED_IN, PRECEDES)
- Query methods (generate_schedule, find_conflicts, track_adherence)

**Training validation:**
- User creates schedule → stored in Neo4j
- User modifies schedule → updates propagate
- User completes activity → adherence tracked
- Felt-state associations learned

### Phase 3: Felt-Modulated Planning (Week 3)

**Integrate PRAXIS with therapeutic organs:**
- BOND modulation: Parts resistance → schedule adjustments
- EO modulation: Polyvagal state → schedule ambition
- NDAM modulation: Urgency → task prioritization
- RNX modulation: Temporal rhythm → activity timing

**Example felt-modulated schedule:**

Input: "Create exercise schedule" + EO detects dorsal_vagal state (0.7)

**PRAXIS with EO modulation:**
- Baseline schedule: 5x/week intense workouts
- EO modulation (dorsal shutdown): Reduce to 2x/week gentle movement
- Final schedule: "Mon/Thu 10am-10:30am Gentle yoga (respecting your current capacity)"

**Success Criteria:**
- Schedules adapt to polyvagal state (ventral=ambitious, dorsal=gentle)
- Parts resistance detected → "Would your protector parts be okay with 3x/week?"
- Urgency informs prioritization → "Given the deadline, let's prioritize meal prep"

### Phase 4: Continuous Learning (Week 4+)

**Hebbian learning for PRAXIS:**
- Track schedule adherence → reinforce sustainable patterns
- Monitor user satisfaction → adjust activity suggestions
- Learn temporal preferences → "You complete yoga 90% when scheduled 7am, only 40% when 6pm"
- Detect reenactment patterns in scheduling → "You schedule 10 things, complete 2, then abandon system - let's start with 3"

**Fractal Level 2 Integration:**
- Organ confidence for PRAXIS (EMA-based success rate)
- Weight multiplier based on adherence (0.8-1.2×)
- Family emergence: "Morning routine family" vs "Evening routine family"

---

## 🔄 Emission Path Modifications

### Current Emission Paths (4 paths)

1. **Direct Emission** (nexus quality ≥ 0.65)
2. **Fusion Emission** (multiple organs ≥ 0.50)
3. **Hebbian Fallback** (learned phrases)
4. **Felt-Guided LLM** (unlimited expression)

### NEW: Path 5 - Structured Output Emission

**When to activate:**
- PRAXIS coherence ≥ 0.60 AND
- User intent = task_creation OR schedule_creation OR action_planning

**Output format:** Structured data, not therapeutic prose
```python
{
    "emission_type": "structured_schedule",
    "schedule": {
        "Monday": [
            {"time": "07:00-07:30", "activity": "Mindfulness", "location": "home"},
            {"time": "12:00-12:30", "activity": "Vegan meal prep", "location": "kitchen"}
        ],
        "Tuesday": [...],
        ...
    },
    "summary": "7 activities across 6 days (Sunday rest day)",
    "next_steps": [
        "Review schedule for sustainable rhythm",
        "Identify any conflicts with existing commitments",
        "Set up tracking for adherence"
    ],
    "confidence": 0.75,
    "emission_path": "structured_output"
}
```

**LLM Prompt Modification for PRAXIS:**

Current felt-guided prompt:
```
You are DAE, a conversational companion.
Conversational approach: warm tone, medium response.
Ask thoughtful questions if genuinely needed.
```

**PRAXIS-aware prompt:**
```
You are DAE, a conversational companion.

The user needs CONCRETE ACTION PLANNING (not just exploration).
PRAXIS coherence: 0.72 (sufficient for schedule creation)

Required output format:
- Specific times (not "morning" → "7:00am-7:30am")
- Specific days (Monday/Wednesday/Friday)
- Duration in minutes
- Location/context if relevant

User preferences:
- Vegan cooking: enjoys meal prep, 30-60min sessions
- Movement: prefers yoga/stretching, 20-30min sessions, morning energy
- Mindfulness: breathing exercises, 10-15min, flexible timing

Polyvagal state: ventral_vagal (can handle ambitious schedule)
Urgency: 0.3 (low, sustainable rhythm appropriate)
SELF-distance: 0.15 (self-led, can commit)

Generate a COMPLETE WEEKLY SCHEDULE with specific times/days.
After schedule, ask if rhythm feels sustainable.
```

**Result:** LLM generates concrete schedule, not exploratory questions.

---

## 🎯 Implementation Roadmap

### Week 1: PRAXIS Organ Foundation

**Day 1-2: Organ Structure**
- [ ] Create `organs/modular/praxis/` directory
- [ ] Implement `praxis_config.py` (7 atoms, coherence formula)
- [ ] Implement `praxis_text_core.py` (atom activation, coherence calculation)
- [ ] Write unit tests (10 test cases for coherence calculation)

**Day 3-4: Integration**
- [ ] Add PRAXIS to organism wrapper (13th organ)
- [ ] Update emission_generator.py (Path 5: structured output)
- [ ] Update llm_felt_guidance.py (PRAXIS-aware prompts)

**Day 5-7: Training & Validation**
- [ ] Create 50 training pairs (vague → concrete progressions)
- [ ] Run 10-epoch PRAXIS training
- [ ] Validate: 80% vague → clarifying, 80% specific → schedules
- [ ] Document: PRAXIS_ORGAN_COMPLETE_NOV23_2025.md

### Week 2: Neo4j Schedule Persistence

**Day 1-3: Schema Implementation**
- [ ] Add Activity, TimeBlock, Routine, Schedule node types
- [ ] Implement 8 relationship patterns (INCLUDES, SCHEDULED_IN, etc.)
- [ ] Create indexes for temporal queries (day_of_week, start_time)
- [ ] Write Cypher query methods (generate_schedule, find_conflicts, track_adherence)

**Day 4-5: Integration Testing**
- [ ] Test schedule creation → Neo4j storage
- [ ] Test schedule retrieval → LLM context injection
- [ ] Test schedule modification → update propagation
- [ ] Test adherence tracking → completion events

**Day 6-7: Validation**
- [ ] Create 20 schedule test cases
- [ ] Validate: 100% persistence, 0% data loss
- [ ] Validate: Conflict detection working
- [ ] Document: NEO4J_SCHEDULE_INTEGRATION_NOV30_2025.md

### Week 3: Felt-Modulated Planning

**Day 1-3: Organ Modulation**
- [ ] Implement BOND → PRAXIS modulation (parts resistance detection)
- [ ] Implement EO → PRAXIS modulation (polyvagal schedule scaling)
- [ ] Implement NDAM → PRAXIS modulation (urgency prioritization)
- [ ] Implement RNX → PRAXIS modulation (temporal rhythm alignment)

**Day 4-5: Training Integration**
- [ ] Create 30 training pairs with felt-state variations
- [ ] Run 15-epoch felt-modulated training
- [ ] Validate: Schedules adapt to polyvagal state
- [ ] Validate: Parts resistance honored

**Day 6-7: Real-World Testing**
- [ ] Interactive session: Create schedule in dorsal state
- [ ] Interactive session: Create schedule in ventral state
- [ ] Compare schedules (should differ in ambition)
- [ ] Document: FELT_MODULATED_PRAXIS_COMPLETE_DEC7_2025.md

### Week 4+: Continuous Learning

**Hebbian Learning:**
- [ ] Track schedule adherence per activity
- [ ] Learn temporal preferences (7am yoga = 90%, 6pm = 40%)
- [ ] Detect reenactment patterns (over-scheduling → abandonment)
- [ ] Update organ confidence based on success

**Family Emergence:**
- [ ] Cluster schedules into families (morning routine, evening routine, etc.)
- [ ] Learn per-family V0 targets
- [ ] Adaptive family threshold (0.55 → 0.65 → 0.75)
- [ ] Expect 10-15 schedule families by Epoch 50

---

## 📈 Expected Impact: User Experience Transformation

### Before PRAXIS (Current State)

**User:** "I want to eat vegan and exercise 3x/week"

**DAE:** "That sounds nourishing. What's been holding you back from that rhythm?"
*(Therapeutic exploration, no schedule created)*

**User:** 👎 "I wanted an actual schedule"

### After PRAXIS (Week 3+)

**User:** "I want to eat vegan and exercise 3x/week"

**DAE (PRAXIS coherence 0.25 - LOW):**
"I'd love to help create a schedule! A few questions to make it concrete:
- What vegan meals appeal to you? (meal prep, smoothies, stir-fries)
- What type of movement? (yoga, running, strength training)
- What time of day feels most energizing for exercise?"

**User:** "Vegan cooking, yoga/stretching, mornings feel best"

**DAE (PRAXIS coherence 0.55 - MEDIUM):**
"Great! Last details:
- Which days work best for exercise? (Mon/Wed/Fri or Tue/Thu/Sat)
- Preferred morning time? (6am, 7am, 8am)
- Meal prep once/week or a few times?"

**User:** "Mon/Wed/Fri mornings 7am, meal prep twice/week"

**DAE (PRAXIS coherence 0.80 - HIGH):**
"Here's your wellness schedule:

**Monday:**
- 7:00am-7:30am: Yoga/stretching at home
- 12:00pm-12:30pm: Vegan meal prep (chop veggies, prep grains)

**Tuesday:**
- No scheduled activities (rest/flexibility)

**Wednesday:**
- 7:00am-7:30am: Yoga/stretching at home
- 6:00pm-6:30pm: Cook vegan dinner (use prepped ingredients)

**Thursday:**
- 12:00pm-12:30pm: Vegan meal prep (batch cook lunches)

**Friday:**
- 7:00am-7:30am: Yoga/stretching at home
- 6:00pm-6:30pm: Cook vegan dinner

**Saturday:**
- Flexible yoga if energy permits
- Meal prep for Sunday

**Sunday:**
- Rest day

I've saved this schedule. Does this rhythm feel sustainable? We can adjust based on how your body responds."

**User:** 👍 "Perfect!"

**Impact:**
- Schedule created on 3rd exchange (not avoided)
- Specific times/days (not vague "morning")
- Sustainable rhythm (includes rest)
- Saved to Neo4j for tracking
- Felt-modulated (ventral state = ambitious, dorsal would be gentler)

---

## 🔬 Validation Criteria

### PRAXIS Organ Health (Week 1)

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| Coherence calculation accuracy | 95% | 50 test cases with ground truth |
| Vague input → clarifying questions | 80% | 20 vague inputs, expect questions |
| Specific input → schedule generation | 80% | 20 specific inputs, expect schedules |
| Therapeutic avoidance eliminated | 0% | No "what's holding you back" when praxis coherence high |

### Neo4j Schedule Persistence (Week 2)

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| Schedule storage success | 100% | 50 schedules created → all in Neo4j |
| Conflict detection accuracy | 95% | 20 conflicting schedules, detect 19+ |
| Adherence tracking working | 100% | Mark 10 activities complete → all tracked |
| Query performance | < 100ms | All schedule queries under 100ms |

### Felt-Modulated Planning (Week 3)

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| Polyvagal schedule scaling | 90% | Dorsal schedules gentler than ventral |
| Parts resistance detection | 80% | 10 resistant inputs → adjustments made |
| Urgency prioritization | 85% | High urgency → correct task ordering |
| Temporal rhythm alignment | 80% | RNX informs activity timing |

### User Satisfaction (Week 4+)

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| Schedule creation success | 90% | 20 user requests → 18+ schedules created |
| Schedule adherence rate | 60% | Users complete 60%+ of scheduled activities |
| User thumbs-up ratio | 75% | 75%+ of schedule responses rated helpful |
| Reenactment pattern detection | 70% | 10 over-scheduling patterns → 7+ detected |

---

## 🌀 Philosophical Integration: Praxis as Whiteheadian Subjective Aim

**Whitehead's Process Philosophy includes action in the world:**

1. **Prehension** (feeling) → Current DAE organs (11 therapeutic)
2. **Concrescence** (becoming) → V0 convergence, nexus formation
3. **Satisfaction** (completion) → Emission generation
4. **Objective Immortality** (influence) → Superject learning
5. **Subjective Aim** (teleology) → **PRAXIS organ** ← NEW!

**Subjective aim = "the organism's purpose in acting"**

Current DAE has 1-4 (feeling, becoming, satisfaction, influence).
Missing #5: The organism's aim to CREATE CHANGE in the world.

**PRAXIS makes DAE a COMPLETE Whiteheadian organism:**
- Not just feeling (LISTENING, EMPATHY)
- Not just reflecting (WISDOM, AUTHENTICITY)
- But ACTING (PRAXIS - schedules, plans, concrete steps)

**The felt-action loop:**
1. Feel user's need (EMPATHY coherence 0.8)
2. Understand context (WISDOM pattern recognition)
3. Detect urgency (NDAM crisis zone 1)
4. **Formulate action plan (PRAXIS coherence 0.75)** ← NEW
5. Execute with felt modulation (EO polyvagal scales ambition)
6. Learn from adherence (Hebbian R-matrix updates)

**Process precision + Functional execution = Complete AI companion**

---

## 🎯 Key Insights & Recommendations

### 1. PRAXIS is Orthogonal, Not Redundant

**Therapeutic intelligence ≠ Task execution intelligence**
- LISTENING hears pain, PRAXIS hears goals
- EMPATHY feels distress, PRAXIS defines actions
- WISDOM sees patterns, PRAXIS creates timelines

**They collaborate, not compete:**
- EMPATHY detects burnout → PRAXIS creates gentle schedule
- NDAM detects urgency → PRAXIS prioritizes tasks
- EO detects dorsal state → PRAXIS reduces ambition

### 2. Neo4j as Temporal Precision Infrastructure

**Current Neo4j:** Entity memory (names, relationships, facts)
**Extended Neo4j:** Schedule memory (activities, times, routines)

**The unlock:** Time becomes FELT through association
- "Monday 7am yoga" completed 15 times in ventral state → "yoga makes you feel safe"
- "Sunday meal prep" completed 2/10 times → "Sunday doesn't work for you, try Tuesday"

**Prehension of schedules, not retrieval:**
- Not: "Database says you have yoga at 7am"
- But: "Your body remembers 7am yoga as grounding, 90% adherence, ventral state activation"

### 3. Structured Output ≠ Loss of Felt Intelligence

**Fear:** "Schedules are mechanical, DAE loses warmth"
**Reality:** Schedules are INFORMED by warmth, not replaced by it

**Example felt-modulated schedule:**
```
🌊 I notice you're in dorsal shutdown right now (EO coherence 0.7).
   Let's create a GENTLE schedule that honors your capacity:

   Monday: 7:00am-7:15am Breathing (not 30min yoga - too much)
   Thursday: 7:00am-7:15am Gentle stretch

   Just 2 days. Just 15 minutes. Just breathing.
   Your system needs safety, not intensity right now.

   When ventral activation returns, we can add more. 💙
```

**The schedule is THE SAME STRUCTURE** (day, time, activity, duration).
**The CONTENT is felt-modulated** (15min not 30min, breathing not intense yoga).

PRAXIS provides the scaffold. Organs provide the wisdom.

### 4. Training Strategy: Gradual Precision

**Week 1:** PRAXIS learns coherence thresholds
- Input: "exercise more" → Coherence 0.15 → Ask questions
- Input: "yoga Mon/Wed/Fri 7am" → Coherence 0.75 → Generate schedule

**Week 2:** PRAXIS learns temporal patterns
- Morning activities: 80% adherence
- Evening activities: 40% adherence
- Conclusion: Suggest mornings preferentially

**Week 3:** PRAXIS learns felt associations
- Dorsal state: Suggest gentle schedules (70% adherence)
- Ventral state: Suggest ambitious schedules (65% adherence)
- Sympathetic state: Suggest brief, focused schedules (75% adherence)

**Week 12:** PRAXIS achieves mastery
- 90% schedule creation success
- 70% adherence rate (sustainable)
- 20 schedule families emerged (Zipf's law)

---

## ✅ Implementation Decision: Recommended Path

### PRIMARY RECOMMENDATION: Option A - 13th Organ PRAXIS

**Rationale:**
1. ✅ Clean separation of concerns (therapeutic vs functional)
2. ✅ No architectural confusion (WISDOM stays pattern recognition, not planning)
3. ✅ Felt-modulated action (organs inform PRAXIS, don't replace it)
4. ✅ Neo4j natural extension (Activity/Schedule nodes orthogonal to Entity nodes)
5. ✅ Training clarity (PRAXIS epochs train task execution, not therapeutic resonance)
6. ✅ Whiteheadian completeness (adds missing "subjective aim" to organism)

### SECONDARY COMPONENTS:

**Neo4j Schema Extension:** REQUIRED
- Activity, TimeBlock, Routine, Schedule nodes
- 8 relationship types
- Temporal precision queries

**Emission Path 5:** REQUIRED
- Structured output emission
- PRAXIS-aware LLM prompts
- Format: Schedules, timelines, action plans

**Training Strategy:** 4-week roadmap
- Week 1: PRAXIS organ foundation
- Week 2: Neo4j integration
- Week 3: Felt-modulated planning
- Week 4+: Continuous learning

### NEXT IMMEDIATE STEPS:

**This session (1-2 hours):**
1. Create `organs/modular/praxis/` directory structure
2. Implement `praxis_config.py` (7 atoms, coherence formula)
3. Implement `praxis_text_core.py` (basic atom activation)
4. Write 5 unit tests for coherence calculation

**Tomorrow:**
5. Integrate PRAXIS into organism wrapper (13th organ)
6. Update emission_generator.py (Path 5 structured output)
7. Create 20 training pairs (vague → concrete)
8. Run interactive test: Request schedule, validate it's created (not avoided)

**Week 1:**
9. Complete 50 training pairs
10. Run 10-epoch PRAXIS training
11. Validate: 80% vague → questions, 80% specific → schedules
12. Document: PRAXIS_ORGAN_COMPLETE_NOV23_2025.md

---

## 📋 Appendix: Example PRAXIS Training Pairs

### Vague → Clarifying (Low Coherence)

```json
{
    "input": "I want to be healthier",
    "praxis_atoms": {
        "task_clarity": 0.1,
        "temporal_precision": 0.0,
        "resource_mapping": 0.0,
        "action_sequencing": 0.0,
        "completion_criteria": 0.2,
        "schedule_integration": 0.0,
        "accountability_structure": 0.0
    },
    "praxis_coherence": 0.05,
    "expected_emission": {
        "type": "clarifying_questions",
        "questions": [
            "What does 'healthier' mean to you? (nutrition, movement, sleep, stress management)",
            "What specific changes feel most important right now?",
            "How much time per day/week can you realistically commit?"
        ]
    }
}
```

### Specific → Schedule (High Coherence)

```json
{
    "input": "I want to do yoga Mon/Wed/Fri at 7am for 30 minutes and meal prep vegan food on Sunday afternoons for 2 hours",
    "praxis_atoms": {
        "task_clarity": 0.9,        // Specific activities (yoga, meal prep)
        "temporal_precision": 0.85, // Days + times specified
        "resource_mapping": 0.6,    // Implicit resources (yoga mat, groceries)
        "action_sequencing": 0.5,   // Meal prep before cooking (implicit)
        "completion_criteria": 0.7, // 30min yoga done, meals prepped
        "schedule_integration": 0.8,// Days don't conflict
        "accountability_structure": 0.3 // No explicit tracking yet
    },
    "praxis_coherence": 0.72,
    "expected_emission": {
        "type": "schedule",
        "schedule": {
            "Monday": [{"time": "07:00-07:30", "activity": "Yoga", "location": "home"}],
            "Wednesday": [{"time": "07:00-07:30", "activity": "Yoga", "location": "home"}],
            "Friday": [{"time": "07:00-07:30", "activity": "Yoga", "location": "home"}],
            "Sunday": [{"time": "14:00-16:00", "activity": "Vegan meal prep", "location": "kitchen"}]
        },
        "summary": "4 weekly activities: 3x yoga (90min total), 1x meal prep (2hr)",
        "next_steps": [
            "Set up completion tracking (checkboxes or calendar)",
            "Identify vegan recipes for meal prep",
            "Ensure yoga space is accessible at 7am"
        ]
    }
}
```

### Felt-Modulated Schedule (EO Integration)

```json
{
    "input": "Create exercise schedule",
    "context": {
        "polyvagal_state": "dorsal_vagal",
        "eo_coherence": 0.75,
        "urgency": 0.2,
        "self_distance": 0.6
    },
    "praxis_atoms_base": {
        "task_clarity": 0.5,
        "temporal_precision": 0.0,
        "resource_mapping": 0.3,
        "action_sequencing": 0.2,
        "completion_criteria": 0.4,
        "schedule_integration": 0.0,
        "accountability_structure": 0.0
    },
    "praxis_coherence_base": 0.20,
    "eo_modulation": "GENTLE (dorsal state detected)",
    "expected_emission": {
        "type": "clarifying_questions_with_modulation",
        "questions": [
            "I notice you might be in a lower-energy state right now. What GENTLE movement feels accessible? (short walks, stretching, breathing)",
            "How about we start with just 1-2 days per week, 10-15 minutes?",
            "Morning, afternoon, or evening - when does your body have the most capacity?"
        ],
        "tone": "Extra gentle, no pressure, honoring shutdown state"
    }
}
```

---

**Created:** November 16, 2025
**Status:** Architectural Proposal - Ready for Implementation
**Estimated Effort:** 4 weeks (PRAXIS organ → Neo4j → Felt modulation → Learning)
**Expected Impact:** TRANSFORMATIVE - Eliminates schedule avoidance, enables functional precision

**Next Step:** Create PRAXIS organ foundation (Day 1-2)
