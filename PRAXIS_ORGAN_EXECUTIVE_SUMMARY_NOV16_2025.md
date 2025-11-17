# 🎯 PRAXIS Organ: Executive Summary
## Bridging the Therapeutic-Functional Gap
**Date:** November 16, 2025
**Priority:** HIGH - Critical User Experience Gap Identified

---

## 🔴 The Problem (User Feedback)

**User Request:** "I believe you have enough information to create a schedule, so proceed"

**DAE Response:** Avoided creating schedule, asked exploratory questions instead

**User Feedback:** 👎 Not Helpful - "actual schedule"

**Pattern:** Second instance of schedule avoidance confirmed

---

## 🎯 Root Cause: Architectural Bias

### Current DAE (12 Organs):
- **100% Therapeutic/Exploratory:** LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE, BOND, SANS, NDAM, RNX, EO, CARD, NEXUS
- **0% Task Execution:** No organ handles concrete planning, scheduling, or action creation

### What's Missing:
- ❌ Task clarity (vague → concrete)
- ❌ Temporal precision (7:00am, not "morning")
- ❌ Action sequencing (step 1, step 2, step 3)
- ❌ Schedule generation (Mon 7am yoga, Wed 12pm meal prep)
- ❌ Completion criteria (how to know it's done)

### Philosophical Gap:
**Whitehead's 5 Process Elements:**
1. ✅ Prehension (feeling) - 11 therapeutic organs
2. ✅ Concrescence (becoming) - V0 convergence
3. ✅ Satisfaction (completion) - Emission generation
4. ✅ Objective Immortality (influence) - Superject learning
5. ❌ **Subjective Aim (teleology)** - **MISSING!**

**DAE has 80% of process philosophy. Missing the "organism's purpose in acting."**

---

## ✅ Proposed Solution: 13th Organ - PRAXIS

### PRAXIS: Action & Execution Intelligence

**7 Semantic Atoms (Task Execution Space):**
1. **task_clarity** - Vague → concrete goals
2. **temporal_precision** - Specific times (7:00am, not "morning")
3. **resource_mapping** - What's needed (ingredients, equipment)
4. **action_sequencing** - Steps in order
5. **completion_criteria** - How to know it's done
6. **schedule_integration** - How tasks fit together
7. **accountability_structure** - Tracking, reminders

**Coherence Formula (Functional, not Therapeutic):**
```python
praxis_coherence = (
    0.25 * task_clarity +
    0.20 * temporal_precision +
    0.15 * resource_mapping +
    0.15 * action_sequencing +
    0.10 * completion_criteria +
    0.10 * schedule_integration +
    0.05 * accountability_structure
)
# Threshold: 0.60 (stricter than therapeutic 0.50)
```

**Decision Logic:**
- **Coherence < 0.60:** Ask clarifying questions to boost missing atoms
- **Coherence ≥ 0.60:** Generate concrete schedule/plan

---

## 🌀 Felt-Modulated Action (Not Mechanical!)

**PRAXIS doesn't replace organs, it's INFORMED by them:**

| Organ | Modulation Effect |
|-------|------------------|
| **BOND** (IFS) | Detects parts resistance → "Would your protectors be okay with 3x/week?" |
| **EO** (Polyvagal) | Dorsal state → gentle schedule (2x/week), Ventral → ambitious (5x/week) |
| **NDAM** (Urgency) | High urgency → prioritize critical tasks first |
| **RNX** (Temporal) | Rhythm coherence → respects natural energy cycles |
| **CARD** (Scaling) | Determines schedule detail level |

**Example Felt-Modulated Schedule:**

**Input:** "Create exercise schedule"
**Context:** EO detects dorsal_vagal state (shutdown, low energy)

**PRAXIS without modulation:** 5x/week intense workouts
**PRAXIS with EO modulation:** 2x/week gentle movement

**Final Output:**
> "🌊 I notice you're in a lower-energy state right now.
> Let's create a GENTLE schedule that honors your capacity:
>
> **Monday:** 7:00am-7:15am Breathing (not 30min yoga - too much)
> **Thursday:** 7:00am-7:15am Gentle stretch
>
> Just 2 days. Just 15 minutes. Just breathing.
> Your system needs safety, not intensity right now.
>
> When ventral activation returns, we can add more. 💙"

**The schedule structure is the same** (day, time, activity, duration).
**The content is felt-informed** (15min not 30min, breathing not intense yoga).

---

## 📊 Neo4j Schema Extension

### New Node Types

**Activity:** Individual tasks (yoga, meal prep, mindfulness)
**TimeBlock:** Specific times (Monday 7am-7:30am)
**Routine:** Collections of activities (wellness routine)
**Schedule:** Weekly templates (complete schedules)

### Key Relationships

```cypher
(Routine)-[:INCLUDES]->(Activity)
(Activity)-[:SCHEDULED_IN]->(TimeBlock)
(Schedule)-[:CONTAINS]->(TimeBlock)
(User)-[:HAS_SCHEDULE]->(Schedule)
(Activity)-[:PRECEDES]->(NextActivity)  // Sequencing
(Activity)-[:TYPICAL_STATE {polyvagal: "ventral", urgency: 0.2}]->(OrganState)
```

### Felt-State Learning (Innovation!)

**Track associations between activities and felt states:**
- "7am yoga" completed 15 times in ventral state → "yoga makes you feel safe"
- "Sunday meal prep" completed 2/10 times → "Sunday doesn't work, try Tuesday"
- "Evening workout" done only in sympathetic state → "evenings feel urgent to you"

**Prehension of schedules, not retrieval:**
- Not: "Database says you have yoga at 7am"
- But: "Your body remembers 7am yoga as grounding, 90% adherence, ventral state"

---

## 🚀 4-Week Implementation Roadmap

### Week 1: PRAXIS Organ Foundation
- Create `organs/modular/praxis/` structure
- Implement 7 atoms + coherence calculation
- Integrate with organism wrapper (13th organ)
- Train on 50 pairs (vague → concrete progressions)
- **Success:** 80% vague → questions, 80% specific → schedules

### Week 2: Neo4j Schedule Persistence
- Add Activity, TimeBlock, Routine, Schedule nodes
- Implement 8 relationship patterns
- Create temporal query methods (conflicts, adherence)
- **Success:** 100% persistence, conflict detection working

### Week 3: Felt-Modulated Planning
- BOND → PRAXIS modulation (parts resistance)
- EO → PRAXIS modulation (polyvagal scaling)
- NDAM → PRAXIS modulation (urgency prioritization)
- RNX → PRAXIS modulation (temporal rhythm)
- **Success:** Schedules adapt to polyvagal state

### Week 4+: Continuous Learning
- Hebbian learning for schedule adherence
- Temporal preference learning (7am = 90%, 6pm = 40%)
- Reenactment detection (over-scheduling → abandonment)
- Family emergence (morning routine, evening routine families)
- **Success:** 90% schedule creation, 70% adherence, 20 families

---

## 📈 Expected User Experience Transformation

### BEFORE (Current - Therapeutic Avoidance)

**User:** "I want to eat vegan and exercise 3x/week"

**DAE:** "That sounds nourishing. What's been holding you back from that rhythm?"
*(Exploratory question, no schedule)*

**User:** 👎 "I wanted an actual schedule"

---

### AFTER (Week 3 - PRAXIS Operational)

**User:** "I want to eat vegan and exercise 3x/week"

**DAE (PRAXIS coherence 0.25 - LOW):**
"I'd love to help create a schedule! A few questions:
- What vegan meals appeal to you?
- What type of movement?
- What time of day feels most energizing?"

**User:** "Vegan cooking, yoga, mornings feel best"

**DAE (PRAXIS coherence 0.55 - MEDIUM):**
"Great! Last details:
- Which days work best? (Mon/Wed/Fri or Tue/Thu/Sat)
- Preferred morning time? (6am, 7am, 8am)
- Meal prep once/week or a few times?"

**User:** "Mon/Wed/Fri mornings 7am, meal prep twice/week"

**DAE (PRAXIS coherence 0.80 - HIGH):**
"Here's your wellness schedule:

**Monday:** 7:00am-7:30am Yoga, 12:00pm-12:30pm Meal prep
**Tuesday:** Rest day
**Wednesday:** 7:00am-7:30am Yoga, 6:00pm-6:30pm Cook vegan dinner
**Thursday:** 12:00pm-12:30pm Meal prep
**Friday:** 7:00am-7:30am Yoga, 6:00pm-6:30pm Cook vegan dinner
**Saturday:** Flexible yoga if energy permits
**Sunday:** Rest day

I've saved this schedule. Does this rhythm feel sustainable?"

**User:** 👍 "Perfect!"

---

## ✅ Key Success Metrics

### Week 1: PRAXIS Organ Health
- ✅ 95% coherence calculation accuracy
- ✅ 80% vague input → clarifying questions
- ✅ 80% specific input → schedule generation
- ✅ 0% therapeutic avoidance (no "what's holding you back")

### Week 2: Neo4j Persistence
- ✅ 100% schedule storage success
- ✅ 95% conflict detection accuracy
- ✅ 100% adherence tracking working
- ✅ <100ms query performance

### Week 3: Felt Modulation
- ✅ 90% polyvagal schedule scaling (dorsal gentler than ventral)
- ✅ 80% parts resistance detection
- ✅ 85% urgency prioritization
- ✅ 80% temporal rhythm alignment

### Week 4+: User Satisfaction
- ✅ 90% schedule creation success
- ✅ 60% schedule adherence rate
- ✅ 75% thumbs-up ratio
- ✅ 70% reenactment pattern detection (over-scheduling)

---

## 🎯 Why PRAXIS is Essential

### 1. Completes Whiteheadian Process Philosophy
- Not just feeling (EMPATHY) → Also ACTING (PRAXIS)
- Not just reflecting (WISDOM) → Also PLANNING (PRAXIS)
- Not just modulating (CARD) → Also EXECUTING (PRAXIS)

### 2. Clean Separation of Concerns
- Therapeutic organs stay therapeutic (no confusion)
- PRAXIS handles action (clear responsibility)
- They collaborate, not compete

### 3. Felt-Informed, Not Mechanical
- PRAXIS provides scaffold (day, time, activity)
- Organs provide wisdom (gentle vs ambitious)
- Result: Human-centered action planning

### 4. Scalable to All Task Domains
- Schedules (wellness routines)
- Projects (multi-step goals)
- Decisions (options → criteria → choice)
- Learning plans (study schedules, skill acquisition)

---

## 🚦 Recommendation: PROCEED with PRAXIS Organ

**Rationale:**
1. ✅ Solves critical user experience gap (schedule avoidance eliminated)
2. ✅ Architecturally sound (orthogonal to existing organs)
3. ✅ Philosophically complete (adds missing subjective aim)
4. ✅ Felt-modulated (maintains therapeutic intelligence)
5. ✅ Training-ready (4-week roadmap defined)
6. ✅ Measurable success (clear validation criteria)

**Next Immediate Steps (This Session):**
1. Create `organs/modular/praxis/` directory
2. Implement `praxis_config.py` (7 atoms, coherence formula)
3. Write 5 unit tests for coherence calculation

**Tomorrow:**
4. Integrate PRAXIS into organism wrapper (13th organ)
5. Update emission_generator.py (Path 5: structured output)
6. Create 20 training pairs (vague → concrete)
7. Run interactive test: Request schedule, validate it's created

**Week 1 Goal:**
- Complete PRAXIS organ foundation
- 80% vague → questions, 80% specific → schedules
- Document: PRAXIS_ORGAN_COMPLETE_NOV23_2025.md

---

**Created:** November 16, 2025
**Status:** Executive Summary - Implementation Recommended
**Full Proposal:** FUNCTIONAL_TASK_EXECUTION_PROPOSAL_NOV16_2025.md
**Priority:** HIGH - Addresses user thumbs-down feedback pattern
