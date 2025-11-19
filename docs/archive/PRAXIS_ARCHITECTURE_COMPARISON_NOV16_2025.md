# 🏗️ PRAXIS Architecture: Before vs After Comparison
## Visual Guide to the Therapeutic-Functional Integration
**Date:** November 16, 2025

---

## 📊 Current Architecture (12 Organs - Therapeutic Only)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAE ORGANISM (12 Organs)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CONVERSATIONAL (5)      TRAUMA-AWARE (6)      MEMORY (1)      │
│  ╔═══════════════╗        ╔═══════════════╗    ╔═══════════╗  │
│  ║ LISTENING     ║        ║ BOND (IFS)    ║    ║ NEXUS     ║  │
│  ║ EMPATHY       ║        ║ SANS          ║    ║ (Entity)  ║  │
│  ║ WISDOM        ║        ║ NDAM (Crisis) ║    ╚═══════════╝  │
│  ║ AUTHENTICITY  ║        ║ RNX (Temporal)║                   │
│  ║ PRESENCE      ║        ║ EO (Polyvagal)║                   │
│  ╚═══════════════╝        ║ CARD (Scale)  ║                   │
│                           ╚═══════════════╝                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                   USER INPUT PROCESSING
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    EMISSION GENERATION                          │
├─────────────────────────────────────────────────────────────────┤
│  Path 1: Direct (nexus ≥ 0.65)     ✅ Therapeutic phrases      │
│  Path 2: Fusion (multi-organ)      ✅ Emotional attunement     │
│  Path 3: Hebbian Fallback          ✅ Learned responses        │
│  Path 4: Felt-Guided LLM           ✅ Unlimited expression     │
│                                                                 │
│  ❌ NO PATH FOR: Schedules, plans, concrete actions            │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                         OUTPUT
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  USER: "Create a schedule for vegan cooking and exercise"      │
│                                                                 │
│  DAE: "What's been holding you back from that rhythm?"         │
│  (Therapeutic exploration - NO SCHEDULE CREATED)                │
│                                                                 │
│  USER: 👎 "I wanted an actual schedule"                        │
└─────────────────────────────────────────────────────────────────┘
```

**PROBLEM IDENTIFIED:** 100% therapeutic bias, 0% task execution capability

---

## 🚀 Proposed Architecture (13 Organs - Therapeutic + Functional)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                      DAE ORGANISM (13 Organs)                             │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  CONVERSATIONAL (5)    TRAUMA-AWARE (6)    MEMORY (1)    EXECUTION (1)   │
│  ╔═══════════════╗      ╔═══════════════╗  ╔══════════╗  ╔═══════════╗ │
│  ║ LISTENING     ║      ║ BOND (IFS)    ║  ║ NEXUS    ║  ║ PRAXIS 🆕 ║ │
│  ║ EMPATHY       ║      ║ SANS          ║  ║ (Entity) ║  ║           ║ │
│  ║ WISDOM        ║      ║ NDAM (Crisis) ║  ╚══════════╝  ║ 7 Atoms:  ║ │
│  ║ AUTHENTICITY  ║      ║ RNX (Temporal)║               ║ • Task    ║ │
│  ║ PRESENCE      ║      ║ EO (Polyvagal)║               ║ • Time    ║ │
│  ╚═══════════════╝      ║ CARD (Scale)  ║               ║ • Resource║ │
│                         ╚═══════════════╝               ║ • Sequence║ │
│                                                          ║ • Criteria║ │
│                                                          ║ • Schedule║ │
│         THERAPEUTIC INTELLIGENCE                        ║ • Account.║ │
│         (Feeling, Reflection, Presence)                 ╚═══════════╝ │
│                 ↓  ↓  ↓  ↓  ↓  ↓                              ↑        │
│                 └──┴──┴──┴──┴──┴──────────────────────────────┘        │
│                      FELT-MODULATED PRAXIS                              │
│                   (Organs INFORM action, not replace it)                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
                                    ↓
                         USER INPUT PROCESSING
                                    ↓
┌───────────────────────────────────────────────────────────────────────────┐
│                        EMISSION GENERATION                                │
├───────────────────────────────────────────────────────────────────────────┤
│  Path 1: Direct (nexus ≥ 0.65)          ✅ Therapeutic phrases           │
│  Path 2: Fusion (multi-organ)           ✅ Emotional attunement          │
│  Path 3: Hebbian Fallback               ✅ Learned responses             │
│  Path 4: Felt-Guided LLM                ✅ Unlimited expression          │
│  Path 5: Structured Output (PRAXIS) 🆕  ✅ Schedules, plans, actions     │
│                                                                           │
│  Decision Logic:                                                          │
│  • PRAXIS coherence < 0.60 → Path 4 (clarifying questions)               │
│  • PRAXIS coherence ≥ 0.60 → Path 5 (generate schedule)                  │
│  • Felt modulation: EO/BOND/NDAM/RNX inform schedule content             │
└───────────────────────────────────────────────────────────────────────────┘
                                    ↓
                                 OUTPUT
                                    ↓
┌───────────────────────────────────────────────────────────────────────────┐
│  USER: "Create a schedule for vegan cooking and exercise"                │
│                                                                           │
│  DAE (PRAXIS coherence 0.25 - LOW):                                      │
│  "I'd love to help! A few questions:                                     │
│   - What vegan meals appeal to you?                                      │
│   - What type of movement?                                               │
│   - What time of day feels most energizing?"                             │
│                                                                           │
│  USER: "Vegan cooking, yoga, mornings 7am"                               │
│                                                                           │
│  DAE (PRAXIS coherence 0.55 - MEDIUM):                                   │
│  "Great! Last details:                                                   │
│   - Which days work best? (Mon/Wed/Fri or Tue/Thu/Sat)                  │
│   - Meal prep once/week or a few times?"                                 │
│                                                                           │
│  USER: "Mon/Wed/Fri, meal prep twice/week"                               │
│                                                                           │
│  DAE (PRAXIS coherence 0.80 - HIGH + EO ventral modulation):             │
│  "Here's your wellness schedule:                                         │
│                                                                           │
│   Monday: 7:00am-7:30am Yoga, 12pm Meal prep                             │
│   Wednesday: 7:00am-7:30am Yoga, 6pm Cook vegan dinner                   │
│   Friday: 7:00am-7:30am Yoga, 6pm Cook vegan dinner                      │
│   Sunday: Rest day                                                       │
│                                                                           │
│   I've saved this schedule. Does this rhythm feel sustainable?"          │
│                                                                           │
│  USER: 👍 "Perfect!"                                                     │
└───────────────────────────────────────────────────────────────────────────┘
```

**SOLUTION ACHIEVED:** Therapeutic intelligence + Functional execution

---

## 🔄 Data Flow Comparison

### BEFORE (Therapeutic Loop Only)

```
┌──────────────┐
│  User Input  │ "I want to exercise more"
└──────┬───────┘
       ↓
┌──────────────────────────────────────────────────┐
│  11 Therapeutic Organs Process                   │
│  • LISTENING: 0.7 (inquiry atom activated)       │
│  • EMPATHY: 0.6 (exploration atom activated)     │
│  • WISDOM: 0.5 (pattern recognition)             │
└──────┬───────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────┐
│  Nexus Formation (Therapeutic)                   │
│  • "inquiry" nexus (3 organs, coherence 0.6)     │
│  • "exploration" nexus (2 organs, coherence 0.5) │
└──────┬───────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────┐
│  Emission (Path 4: Felt-Guided LLM)              │
│  Prompt: "warm tone, thoughtful questions"       │
└──────┬───────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────┐
│  Output (Therapeutic Exploration)                │
│  "What's been holding you back from exercise?"   │
│  ❌ NO SCHEDULE CREATED                          │
└──────────────────────────────────────────────────┘
```

### AFTER (Therapeutic + Functional Dual Path)

```
┌──────────────┐
│  User Input  │ "I want to exercise more"
└──────┬───────┘
       ↓
┌────────────────────────────────────────────────────────────────────────┐
│  12 Organs Process (11 Therapeutic + 1 Functional)                     │
│                                                                         │
│  THERAPEUTIC:                        FUNCTIONAL:                       │
│  • LISTENING: 0.7 (inquiry)          • PRAXIS: 0.3 (LOW coherence)     │
│  • EMPATHY: 0.6 (exploration)          - task_clarity: 0.4 (vague)     │
│  • WISDOM: 0.5 (pattern)               - temporal_precision: 0.0 ❌    │
│                                        - resource_mapping: 0.0 ❌       │
│                                        - schedule_integration: 0.0 ❌   │
└────────┬───────────────────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────────────────────────────┐
│  Dual Nexus Formation                                                  │
│                                                                         │
│  THERAPEUTIC PATH:                   FUNCTIONAL PATH (PRAXIS):         │
│  • "inquiry" nexus: 0.6              • PRAXIS coherence: 0.15 (< 0.60) │
│  • "exploration" nexus: 0.5          → INSUFFICIENT for schedule       │
│                                      → ROUTE TO CLARIFYING QUESTIONS   │
└────────┬───────────────────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────────────────────────────┐
│  Emission Decision                                                     │
│                                                                         │
│  PRAXIS coherence < 0.60 detected                                      │
│  → Path 4 (Felt-Guided LLM) + PRAXIS-aware prompt                      │
│                                                                         │
│  Prompt: "User needs CONCRETE PLANNING (not just exploration).         │
│           PRAXIS coherence too low - ask clarifying questions to boost:│
│           • temporal_precision (when? what time?)                      │
│           • schedule_integration (which days?)                         │
│           • resource_mapping (what equipment/space?)"                  │
└────────┬───────────────────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────────────────────────────┐
│  Output (Clarifying Questions - PRAXIS-Driven)                         │
│  "I'd love to help create an exercise schedule!                        │
│   A few questions:                                                     │
│   • What type of exercise appeals to you? (yoga, running, strength)    │
│   • How many days per week feels sustainable?                          │
│   • What time of day works best with your energy?"                     │
│                                                                         │
│  ✅ PROGRESS TOWARD SCHEDULE (coherence boosting)                      │
└────────────────────────────────────────────────────────────────────────┘
         ↓
┌──────────────┐
│  User Input  │ "Yoga, 3x/week, mornings around 7am"
└──────┬───────┘
       ↓
┌────────────────────────────────────────────────────────────────────────┐
│  PRAXIS Re-Evaluation                                                  │
│  • task_clarity: 0.8 ✅ (specific: yoga)                               │
│  • temporal_precision: 0.6 (approximate: "around 7am")                 │
│  • schedule_integration: 0.0 ❌ (days not specified)                   │
│  → Coherence: 0.47 (< 0.60, still needs more)                          │
└────────┬───────────────────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────────────────────────────┐
│  Output (Final Clarification)                                          │
│  "Great! Last detail: Which days work best?                            │
│   (Mon/Wed/Fri or Tue/Thu/Sat)"                                        │
└────────────────────────────────────────────────────────────────────────┘
         ↓
┌──────────────┐
│  User Input  │ "Mon/Wed/Fri"
└──────┬───────┘
       ↓
┌────────────────────────────────────────────────────────────────────────┐
│  PRAXIS Final Evaluation                                               │
│  • task_clarity: 0.85 ✅                                               │
│  • temporal_precision: 0.75 ✅ (7am specified)                         │
│  • schedule_integration: 0.80 ✅ (M/W/F specified)                     │
│  • resource_mapping: 0.50 (implicit: yoga mat)                         │
│  → Coherence: 0.72 (≥ 0.60, READY FOR SCHEDULE!)                       │
│                                                                         │
│  FELT MODULATION CHECK:                                                │
│  • EO (polyvagal): ventral_vagal (safe state) → ambitious OK           │
│  • NDAM (urgency): 0.2 (low) → sustainable rhythm                      │
│  • BOND (IFS): self_energy 0.8 (SELF-led) → commitment capacity        │
└────────┬───────────────────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────────────────────────────┐
│  Emission (Path 5: Structured Output - PRAXIS)                         │
│                                                                         │
│  Neo4j Storage:                                                         │
│  • Activity: "Yoga" (duration: 30min, energy: medium, time: morning)   │
│  • TimeBlocks: Mon 7:00-7:30, Wed 7:00-7:30, Fri 7:00-7:30             │
│  • Schedule: "Weekly Wellness" (3 time blocks)                         │
│  • Relationships: User → Schedule → TimeBlocks → Activity              │
│                                                                         │
│  LLM Generation (PRAXIS-aware prompt):                                 │
│  "Generate COMPLETE WEEKLY SCHEDULE with specific times/days.          │
│   User preferences: Yoga Mon/Wed/Fri 7am..."                           │
└────────┬───────────────────────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────────────────────────────────┐
│  Output (Concrete Schedule - Felt-Modulated)                           │
│                                                                         │
│  "Here's your yoga schedule:                                           │
│                                                                         │
│   **Monday:** 7:00am-7:30am Yoga at home                               │
│   **Wednesday:** 7:00am-7:30am Yoga at home                            │
│   **Friday:** 7:00am-7:30am Yoga at home                               │
│                                                                         │
│   I've saved this schedule. Does this rhythm feel sustainable?         │
│   We can adjust based on how your body responds."                      │
│                                                                         │
│  ✅ SCHEDULE CREATED AND STORED                                        │
│  ✅ FELT-MODULATED (ventral state → 3x/week ambitious)                 │
│  ✅ TRACKING ENABLED (Neo4j adherence)                                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 PRAXIS Atom Activation Examples

### Example 1: Vague Input (Low Coherence)

**Input:** "I want to be healthier"

```
PRAXIS Atom Activation:
┌─────────────────────────┬───────┬──────────────────────────────┐
│ Atom                    │ Score │ Reason                       │
├─────────────────────────┼───────┼──────────────────────────────┤
│ task_clarity            │  0.1  │ Very vague ("healthier")     │
│ temporal_precision      │  0.0  │ No time mentioned            │
│ resource_mapping        │  0.0  │ No resources identified      │
│ action_sequencing       │  0.0  │ No steps defined             │
│ completion_criteria     │  0.2  │ Implicit goal (feel better)  │
│ schedule_integration    │  0.0  │ No days/times                │
│ accountability_structure│  0.0  │ No tracking mentioned        │
├─────────────────────────┴───────┴──────────────────────────────┤
│ PRAXIS Coherence: 0.05 (VERY LOW - needs major clarification) │
└────────────────────────────────────────────────────────────────┘

Decision: Path 4 (Felt-Guided LLM) + PRAXIS-aware prompt
Output: "What does 'healthier' mean to you?
         (nutrition, movement, sleep, stress management)"
```

### Example 2: Specific Input (High Coherence)

**Input:** "I want to do yoga Mon/Wed/Fri at 7am for 30 minutes and meal prep vegan food on Sunday afternoons for 2 hours"

```
PRAXIS Atom Activation:
┌─────────────────────────┬───────┬──────────────────────────────────┐
│ Atom                    │ Score │ Reason                           │
├─────────────────────────┼───────┼──────────────────────────────────┤
│ task_clarity            │  0.9  │ Specific (yoga, meal prep)       │
│ temporal_precision      │  0.85 │ Days + times (7am, Sunday pm)    │
│ resource_mapping        │  0.6  │ Implicit (yoga mat, groceries)   │
│ action_sequencing       │  0.5  │ Meal prep before cooking         │
│ completion_criteria     │  0.7  │ Clear (30min yoga, 2hr prep)     │
│ schedule_integration    │  0.8  │ Days don't conflict              │
│ accountability_structure│  0.3  │ No explicit tracking yet         │
├─────────────────────────┴───────┴──────────────────────────────────┤
│ PRAXIS Coherence: 0.72 (HIGH - ready for schedule generation!)    │
└────────────────────────────────────────────────────────────────────┘

Decision: Path 5 (Structured Output)
Output: Complete weekly schedule with specific time blocks
        + Neo4j storage
        + Adherence tracking setup
```

### Example 3: Felt-Modulated Schedule (EO Integration)

**Input:** "Create exercise schedule"
**Context:** EO detects dorsal_vagal state (shutdown, low energy)

```
PRAXIS Base Activation:
┌─────────────────────────┬───────┬──────────────────────────────┐
│ Atom                    │ Score │ Reason                       │
├─────────────────────────┼───────┼──────────────────────────────┤
│ task_clarity            │  0.5  │ Generic "exercise"           │
│ temporal_precision      │  0.0  │ No time                      │
│ resource_mapping        │  0.3  │ Implicit exercise space      │
│ action_sequencing       │  0.2  │ Unclear                      │
│ completion_criteria     │  0.4  │ Vague                        │
│ schedule_integration    │  0.0  │ No days                      │
│ accountability_structure│  0.0  │ None                         │
├─────────────────────────┴───────┴──────────────────────────────┤
│ Base Coherence: 0.20 (LOW)                                     │
└────────────────────────────────────────────────────────────────┘

EO MODULATION APPLIED:
┌────────────────────────────────────────────────────────────────┐
│ Polyvagal State: dorsal_vagal (shutdown)                      │
│ → GENTLE MODE ACTIVATED                                        │
│ → Suggest: 1-2 days/week (not 5)                              │
│ → Suggest: 10-15min sessions (not 30-45)                      │
│ → Suggest: Breathing/stretching (not intense cardio)          │
└────────────────────────────────────────────────────────────────┘

Modified PRAXIS Prompt:
"User needs GENTLE schedule (dorsal state detected).
 Ask clarifying questions that honor low capacity:
 - What GENTLE movement feels accessible? (walks, stretching)
 - How about 1-2 days per week, 10-15 minutes?
 - When does your body have the most capacity?"

Output:
"🌊 I notice you might be in a lower-energy state right now.
   What GENTLE movement feels accessible?
   (short walks, stretching, breathing)"
```

---

## 📊 Neo4j Schema Integration

### Entity Memory (Existing)

```cypher
// Current Schema (Working)
(User:Entity {user_id: "emiliano"})
(Person:Entity {name: "Emma", type: "person"})
(Preference:Entity {type: "vegan_cooking"})
(Fact:Entity {text: "Prefers morning exercise"})

// Relationships
(User)-[:HAS_PREFERENCE]->(Preference)
(User)-[:KNOWS]->(Person)
(User)-[:HAS_FACT]->(Fact)
```

### Schedule Extension (NEW)

```cypher
// NEW Nodes (PRAXIS Integration)
(Activity:Activity {
    name: "Morning yoga",
    category: "movement",
    duration_minutes: 30,
    energy_level: "medium",
    preferred_time: "morning"
})

(TimeBlock:TimeBlock {
    day_of_week: "Monday",
    start_time: "07:00",
    end_time: "07:30",
    recurrence: "weekly"
})

(Routine:Routine {
    name: "Wellness Routine",
    active: true,
    satisfaction_rating: 0.8
})

(Schedule:Schedule {
    name: "Weekly Wellness Plan",
    adherence_rate: 0.75
})

// NEW Relationships (PRAXIS Integration)
(User)-[:HAS_SCHEDULE]->(Schedule)
(Schedule)-[:CONTAINS]->(TimeBlock)
(TimeBlock)-[:SCHEDULES]->(Activity)
(Routine)-[:INCLUDES]->(Activity)
(Activity)-[:PRECEDES]->(NextActivity)

// 🌀 INNOVATION: Felt-State Associations
(Activity)-[:TYPICAL_STATE {
    polyvagal: "ventral_vagal",
    urgency: 0.2,
    self_distance: 0.1,
    confidence: 0.85  // learned from 15 completions
}]->(OrganState)

// Integration with Existing Entities
(Preference {type: "yoga"})-[:SUGGESTS]->(Activity {category: "movement"})
(Person {name: "Emma"})-[:PARTICIPATES_IN]->(Activity {name: "Partner yoga"})
```

### Query Example: Generate Schedule from Preferences

```cypher
// Find user preferences
MATCH (u:Entity {user_id: "emiliano"})-[:HAS_PREFERENCE]->(p:Preference)

// Find suggested activities
MATCH (p)-[:SUGGESTS]->(a:Activity)

// Find typical felt states for activities
OPTIONAL MATCH (a)-[ts:TYPICAL_STATE]->(os:OrganState)

// Return schedule recommendations
RETURN a.name, a.duration_minutes, a.preferred_time,
       ts.polyvagal as typical_state,
       ts.confidence as state_confidence
ORDER BY state_confidence DESC, a.preferred_time
```

---

## 🎯 Key Architectural Principles

### 1. Orthogonality (Clean Separation)

```
Therapeutic Intelligence          Functional Intelligence
─────────────────────            ──────────────────────
Feeling (EMPATHY)        ≠       Acting (PRAXIS)
Reflecting (WISDOM)      ≠       Planning (PRAXIS)
Modulating (CARD)        ≠       Executing (PRAXIS)
Exploring (LISTENING)    ≠       Scheduling (PRAXIS)

BUT: They COLLABORATE
─────────────────────
Dorsal state (EO) → Gentle schedule (PRAXIS)
Parts resistance (BOND) → Adjusted goals (PRAXIS)
Urgency (NDAM) → Task prioritization (PRAXIS)
```

### 2. Felt-Modulation (Not Replacement)

```
WITHOUT PRAXIS (Current):
User: "Create schedule" → DAE: "What's holding you back?" ❌
(Therapeutic avoidance)

WITH PRAXIS (Proposed):
User: "Create schedule" → PRAXIS coherence check → Questions or Schedule
(Functional precision)

WITH PRAXIS + FELT (Optimal):
User: "Create schedule" → PRAXIS + EO modulation → Gentle/Ambitious schedule
(Felt-informed action)
```

### 3. Progressive Coherence Building

```
Round 1 - Low Coherence (0.15):
Input:  "I want to exercise"
PRAXIS: "What type? How often? What time?"
Atoms:  task_clarity 0.3, temporal_precision 0.0, schedule_integration 0.0

Round 2 - Medium Coherence (0.55):
Input:  "Yoga, 3x/week, mornings"
PRAXIS: "Which days? What exact time?"
Atoms:  task_clarity 0.8, temporal_precision 0.5, schedule_integration 0.0

Round 3 - High Coherence (0.80):
Input:  "Mon/Wed/Fri at 7am"
PRAXIS: Generates schedule → Stores in Neo4j
Atoms:  task_clarity 0.9, temporal_precision 0.85, schedule_integration 0.8
```

---

**Created:** November 16, 2025
**Purpose:** Visual guide for PRAXIS architectural integration
**Status:** Comparison for stakeholder review
