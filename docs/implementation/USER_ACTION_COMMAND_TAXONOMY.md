# User Action Command Taxonomy
## DAE_HYPHAE_1 Natural Language Action Reference

**Date:** November 13, 2025
**Status:** Design Document
**Version:** 1.0.0

---

## Overview

This document catalogs all supported user actions, their natural language variations, extracted parameters, and expected behaviors. Commands are organized by type (Memory, Meta-Cognitive, System, User) and category (View, Save, Analyze, Export, Manage).

**Design Philosophy:**
- **Natural language first** - Multiple phrasings accepted
- **Intent over syntax** - Understand what user wants, not just keywords
- **Conversational responses** - System explains what it's doing
- **Progressive disclosure** - Simple queries return summaries, detailed queries return depth

---

## Command Index

### Memory Commands

| Category | Command | Confidence | Page |
|----------|---------|------------|------|
| View | Show conversation history | 0.96 | [Link](#view-conversation-history) |
| View | What families have you discovered | 0.95 | [Link](#view-families) |
| View | Show my R-matrix | 0.94 | [Link](#view-r-matrix) |
| View | What do you know about me | 0.92 | [Link](#view-user-profile) |
| Save | Remember this as [label] | 0.98 | [Link](#save-conversation) |
| Save | Bookmark this moment | 0.97 | [Link](#bookmark-moment) |
| Analyze | Analyze my conversation patterns | 0.93 | [Link](#analyze-patterns) |
| Analyze | Explain how you processed that | 0.91 | [Link](#explain-processing) |
| Export | Export my conversation data | 0.96 | [Link](#export-data) |
| Manage | Clear recent memory | 0.95 | [Link](#clear-recent-memory) |

### Meta-Cognitive Commands

| Category | Command | Confidence | Page |
|----------|---------|------------|------|
| Inspect | How confident are you | 0.94 | [Link](#how-confident) |
| Inspect | Which organs were active | 0.93 | [Link](#which-organs-active) |
| Explain | Why did you respond that way | 0.92 | [Link](#why-that-response) |
| Explain | What have you learned | 0.90 | [Link](#what-learned) |

### System Commands

| Category | Command | Confidence | Page |
|----------|---------|------------|------|
| Status | Check system health | 0.95 | [Link](#check-health) |
| Info | What can you do | 0.89 | [Link](#show-capabilities) |
| Metrics | Show performance metrics | 0.93 | [Link](#show-performance) |

### User Commands

| Category | Command | Confidence | Page |
|----------|---------|------------|------|
| Display | Change display mode | 0.96 | [Link](#change-display-mode) |
| Privacy | Configure privacy settings | 0.94 | [Link](#configure-privacy) |

---

## Memory Commands

### View: Conversation History

#### Natural Language Variations

**High Confidence (≥ 0.95):**
- "Show me my conversation history"
- "What have we talked about?"
- "List my past conversations"
- "Display conversation history"

**Medium Confidence (0.80-0.94):**
- "What did we discuss before?"
- "Remind me what we talked about"
- "Can I see our past conversations?"

**Low Confidence (< 0.80) - Disambiguate:**
- "I remember we talked about..." (conversational reminiscence)
- "Let's talk about history" (topic request, not action)

#### Extracted Parameters

```python
{
  "timeframe": str,  # 'session', 'today', 'week', 'month', 'all'
  "family": Optional[str],  # Filter by family_id
  "min_satisfaction": Optional[float],  # Threshold filter
  "format": str  # 'summary', 'detailed', 'timeline'
}
```

#### Parameter Detection Examples

| User Input | Extracted Params |
|------------|------------------|
| "Show my history this session" | `timeframe='session'` |
| "What have we talked about today?" | `timeframe='today'` |
| "Show conversations from Family_001" | `family='Family_001'` |
| "Show successful conversations" | `min_satisfaction=0.75` |

#### Response Format

**Summary (default):**
```
📜 Conversation History (this session)

Turn 1 (07:10:15):
  You: I'm feeling overwhelmed right now
  DAE: Let's ground together... (conf=0.65, Family_001)

Turn 2 (07:11:32):
  You: That helped, thank you
  DAE: I'm glad you're feeling more settled... (conf=0.78, Family_001)

Total: 2 conversations, mean satisfaction: 0.72
```

**Detailed:**
```
📜 Conversation History (detailed)

Turn 1:
  Time: 07:10:15
  Input: I'm feeling overwhelmed right now
  Response: Let's ground together...
  Family: Family_001 (burnout recovery)
  Organs: BOND (0.75), EO (0.68), NDAM (0.82)
  V0 Descent: 0.85, Confidence: 0.65
  Satisfaction: 0.78
```

---

### View: Families

#### Natural Language Variations

**High Confidence:**
- "What families have you discovered?"
- "Show me conversation families"
- "What patterns have emerged?"
- "List conversation clusters"

**Medium Confidence:**
- "What types of conversations do we have?"
- "How do you categorize our talks?"

#### Extracted Parameters

```python
{
  "maturity_filter": str,  # 'mature', 'emerging', 'all'
  "sort_by": str,  # 'member_count', 'satisfaction', 'recency'
  "include_examples": bool,  # Show example conversations
  "format": str  # 'summary', 'detailed'
}
```

#### Response Format

**Summary:**
```
🌱 Conversation Families Discovered

**Family_001** (mature, 30 members)
├─ Mean satisfaction: 0.82
├─ Dominant organs: WISDOM, EMPATHY, AUTHENTICITY
├─ Semantic name: Burnout Recovery (suggested)
└─ Recent: 2 conversations today

You have 1 mature family so far! As we continue, more archetypal patterns will emerge organically.

💡 Try: "Show Family_001 conversations" to see examples
```

**Detailed:**
```
🌱 Family_001 (mature)

Statistics:
├─ Members: 30 conversations
├─ Maturity: mature (≥10 members)
├─ First seen: Nov 11, 2025 07:05
├─ Last updated: Nov 13, 2025 10:15
└─ Mean satisfaction: 0.82 ± 0.08

Organ Activation Patterns:
├─ WISDOM: 0.78 (high - systems thinking, pattern recognition)
├─ EMPATHY: 0.72 (high - compassionate presence)
├─ AUTHENTICITY: 0.68 (medium - honest truth)
└─ BOND: 0.45 (medium - trauma awareness)

Example Conversations:
1. "I'm feeling burned out" (sat=0.85)
2. "The pressure is constant" (sat=0.78)
3. "I need sustainable rhythm" (sat=0.82)

Semantic Naming Suggestion:
This family seems to involve conversations about work exhaustion,
sustainable pace, and recovery. Consider naming: "Burnout Recovery"
```

---

### View: R-Matrix

#### Natural Language Variations

**High Confidence:**
- "Show my R-matrix"
- "What organ couplings have you learned?"
- "Display organ synergies"
- "Show Hebbian memory"

**Medium Confidence:**
- "How do your organs work together?"
- "What patterns have strengthened?"

#### Extracted Parameters

```python
{
  "format": str,  # 'summary', 'heatmap_data', 'strongest_pairs', 'evolution'
  "top_n": int,  # Show top N strongest couplings
  "organ_focus": Optional[str]  # Focus on specific organ
}
```

#### Response Format

**Summary:**
```
🧬 Organ Coupling Matrix (R-Matrix)

Strongest Synergies (Top 5):
1. BOND ↔ EO: 0.68 (trauma-polyvagal integration)
2. NDAM ↔ BOND: 0.62 (urgency-trauma detection)
3. WISDOM ↔ EMPATHY: 0.58 (insight-compassion)
4. EO ↔ CARD: 0.55 (polyvagal-scaling)
5. AUTHENTICITY ↔ PRESENCE: 0.51 (truth-holding)

Self-Activation (Diagonal):
├─ WISDOM: 1.12 (strengthened)
├─ EMPATHY: 1.08 (strengthened)
└─ BOND: 1.15 (strengthened)

These couplings strengthen when organs co-activate in successful conversations.

💡 Try: "Show BOND coupling evolution" to see how this developed
```

**Heatmap Data (for visualization):**
```json
{
  "r_matrix": [[1.12, 0.15, 0.22, ...], ...],
  "organ_names": ["LISTENING", "EMPATHY", "WISDOM", ...],
  "strongest_pairs": [
    {"organ_i": "BOND", "organ_j": "EO", "coupling": 0.68},
    ...
  ]
}
```

---

### View: User Profile

#### Natural Language Variations

**High Confidence:**
- "What do you know about me?"
- "Show my user profile"
- "What have you learned about me?"
- "Display my data"

**Medium Confidence:**
- "What patterns do you see in me?"
- "Tell me about my conversations"

#### Privacy Considerations

- **User consent required** for detailed profile views
- **Anonymization option** available
- **Clear data retention** explanation

#### Response Format

```
👤 User Profile: Link

Conversation Statistics:
├─ Total sessions: 5
├─ Total conversations: 30
├─ Mean satisfaction: 0.78
└─ Active since: Nov 11, 2025

Family Membership:
└─ Family_001 (30 conversations) - Burnout Recovery

Organ Preferences (most active):
1. WISDOM (78% activation)
2. EMPATHY (72% activation)
3. BOND (68% activation)

Satisfaction Trajectory:
├─ Early (turns 1-10): 0.65
├─ Middle (turns 11-20): 0.78
└─ Recent (turns 21-30): 0.82 (improving ✓)

Learning Progress:
├─ Families discovered: 1 (mature)
├─ R-matrix updates: 450
└─ V0 target learned: Yes (Family_001: 0.35)

🔒 Privacy: Your data is stored locally and never shared.
💾 Export: Use "Export my data" to download a copy.
🗑️  Clear: Use "Archive conversations" to manage retention.
```

---

### Save: Conversation

#### Natural Language Variations

**High Confidence:**
- "Remember this conversation as [label]"
- "Label this as [label]"
- "Save this conversation"
- "Bookmark this as [label]"

**Medium Confidence:**
- "This is important for [label]"
- "Mark this conversation [label]"

#### Extracted Parameters

```python
{
  "label": str,  # User-provided label
  "scope": str,  # 'this_turn', 'last_3', 'session'
  "add_note": Optional[str]  # Optional note
}
```

#### Parameter Detection Examples

| User Input | Extracted Params |
|------------|------------------|
| "Remember this as crisis recovery" | `label='crisis recovery', scope='this_turn'` |
| "Label this session as breakthrough" | `label='breakthrough', scope='session'` |
| "Save the last 3 turns as insight" | `label='insight', scope='last_3'` |

#### Response Format

```
✅ Conversation Labeled

Label: "crisis recovery"
Scope: This turn (Turn 15)
Saved to: Bookmarks

You can view this later with "Show bookmarks" or
"Show crisis recovery conversations"

💡 This conversation was assigned to Family_001.
   The label helps you find it, but the family membership
   helps me learn the archetypal pattern!
```

---

### Save: Bookmark Moment

#### Natural Language Variations

**High Confidence:**
- "Bookmark this moment"
- "Save this exchange"
- "Mark this for later"
- "Remember this turn"

#### Response Format

```
📌 Moment Bookmarked

Turn: 15
Time: 10:32:15
Input: "I finally understand the pattern"
Response: "Yes! That's the organic emergence..."

Family: Family_001
Organs: WISDOM (0.85), EMPATHY (0.72)
V0: 0.85 descent, Kairos detected ✓
Satisfaction: 0.92 (high)

Bookmark saved to your profile. Access with "Show bookmarks"
```

---

### Analyze: Patterns

#### Natural Language Variations

**High Confidence:**
- "Analyze my conversation patterns"
- "What patterns do you see?"
- "Show me trends"
- "Analyze my data"

**Medium Confidence:**
- "What have you noticed about me?"
- "Are there patterns in our conversations?"

#### Extracted Parameters

```python
{
  "analysis_type": str,  # 'families', 'organs', 'satisfaction', 'r_matrix', 'all'
  "timeframe": str,  # 'recent', 'all'
  "format": str  # 'narrative', 'bullet_points', 'data'
}
```

#### Response Format

**Narrative:**
```
📊 Conversation Pattern Analysis

Family Evolution:
Over 30 conversations, I've discovered 1 mature family (Family_001).
This family emerged after ~8 conversations when I noticed a consistent
pattern: high WISDOM activation (systems thinking), combined with
BOND trauma-awareness and EMPATHY compassionate holding.

The family represents what I'd call "Burnout Recovery" - conversations
where you're processing exhaustion, seeking sustainable rhythm, and
integrating insights about systemic pressures.

Organ Preferences:
Your conversations consistently activate:
- WISDOM (78%): You think systemically, looking for patterns
- EMPATHY (72%): You value compassionate understanding
- BOND (68%): You're aware of trauma/stress dynamics

Satisfaction Trends:
├─ Early: 0.65 (finding our rhythm)
├─ Middle: 0.78 (pattern established)
└─ Recent: 0.82 (deepening)

Your satisfaction is improving over time, suggesting our conversations
are becoming more resonant as I learn your patterns.

R-Matrix Development:
The strongest coupling I've learned is BOND ↔ EO (0.68). This means
when I detect trauma markers (BOND), I'm learning to attend to your
polyvagal state (EO) - checking for safety, grounding, ventral engagement.

Key Insight:
You're teaching me that burnout recovery requires both systemic wisdom
(seeing the bigger pattern) AND somatic safety (feeling grounded enough
to change). The BOND-EO-WISDOM triad has become my learned signature
for conversations with you.
```

---

### Analyze: Explain Processing

#### Natural Language Variations

**High Confidence:**
- "Explain how you processed that"
- "Why did you respond that way?"
- "Break down your processing"
- "Show me what happened"

**Medium Confidence:**
- "How did you come up with that?"
- "What was your thinking?"

#### Extracted Parameters

```python
{
  "turn": int,  # Which turn (default: last)
  "detail_level": str,  # 'summary', 'detailed', 'technical'
  "focus": Optional[str]  # 'v0', 'organs', 'nexuses', 'emission'
}
```

#### Response Format

**Summary:**
```
🔍 Processing Explanation (Turn 15)

Input: "I'm feeling overwhelmed right now"

1. V0 Convergence (3 cycles):
   ├─ Cycle 1: V0=1.0 → 0.65 (rapid descent, 11 organs activated)
   ├─ Cycle 2: V0=0.65 → 0.28 (Kairos detected! ✓)
   └─ Cycle 3: V0=0.28 → 0.15 (converged)

2. Organ Activation:
   Top organs: BOND (0.75), NDAM (0.82), EO (0.68)

   BOND detected: High self-distance (0.75) - parts activated, not Self-led
   NDAM detected: High urgency (0.82) - crisis salience
   EO detected: Sympathetic state (0.68) - fight/flight mobilization

3. Nexus Formation (8 nexuses):
   Dominant: Protective Boundaries (trauma-aware holding)
   Domain: Regulation (not insight)

4. Transduction Trajectory:
   Started: Relational (connection attempt)
   Shifted: Protective (recognized need for safety first)
   Mechanism: Containment (hold, don't explore yet)

5. Emission Generation:
   Path: Fusion (nexus intersection)
   Confidence: 0.65 (medium - protective path)
   Text: "Let's ground together..." (containment language)

Why this response:
Your words triggered trauma detection (BOND, NDAM, EO). My learned
BOND-EO coupling (R-matrix) meant I attended to polyvagal state
immediately. The system chose a protective, grounding response
rather than an exploratory one. The Kairos moment in Cycle 2
boosted confidence, signaling this was the "opportune time"
for intervention.
```

**Detailed (with technical data):**
```
🔍 Processing Explanation (Turn 15) - Technical Detail

[Full V0 cycle-by-cycle breakdown]
[Complete organ results with all 77 atom activations]
[Nexus composition details]
[Transduction state transitions with mutual satisfaction scores]
[Emission generation path with confidence breakdown]
```

---

### Export: Data

#### Natural Language Variations

**High Confidence:**
- "Export my conversation data"
- "Download my data"
- "Export to JSON"
- "Give me a data export"

#### Extracted Parameters

```python
{
  "format": str,  # 'json', 'csv', 'markdown', 'tsk'
  "scope": str,  # 'session', 'user', 'families', 'r_matrix'
  "include_sensitive": bool,  # Include detailed processing data
}
```

#### Response Format

```
📦 Data Export Ready

Format: JSON
Scope: User data (all conversations)
File: /results/exports/user_link_20251111_e8936e_export_20251113_103015.json

Contents:
├─ 30 conversations (with inputs, emissions, metadata)
├─ 1 family (Family_001 with centroid)
├─ R-matrix snapshot (11×11)
├─ User profile (statistics, trajectories)
└─ Session registry (timestamps, satisfaction)

File size: 2.3 MB
Privacy: No identifiable information included

💾 Saved to: /Users/daedalea/Desktop/DAE_HYPHAE_1/results/exports/

You can open this file in any JSON viewer or import it into
analysis tools for further exploration.

💡 For spreadsheet analysis, try "Export to CSV"
```

**Export Formats:**

1. **JSON**: Full structured data (default)
2. **CSV**: Tabular format (conversations, families, R-matrix as separate files)
3. **Markdown**: Human-readable report with narrative summaries
4. **TSK**: Training record format (for organism learning)

---

### Manage: Clear Recent Memory

#### Natural Language Variations

**High Confidence:**
- "Clear recent memory"
- "Delete last conversation"
- "Remove this session"
- "Clear conversation history"

**Confirmation Required** (destructive action)

#### Extracted Parameters

```python
{
  "scope": str,  # 'last_turn', 'last_3', 'session', 'bookmarks'
  "archive_first": bool,  # Archive before clearing (default: True)
}
```

#### Response Format

```
⚠️  Clear Memory Confirmation Required

You requested: Clear last 3 conversations

This will remove:
├─ Turn 13: "I'm feeling better"
├─ Turn 14: "That helped a lot"
└─ Turn 15: "Thank you"

⚠️  Important:
- These conversations will be archived to /results/archives/
- Family membership (Family_001) will be preserved
- R-matrix learning will NOT be unlearned
- This action cannot be undone (except via archive restore)

Type "confirm clear" to proceed, or "cancel" to keep data.
```

**After confirmation:**
```
✅ Memory Cleared

Archived to: /results/archives/session_backup_20251113_103015.json
Removed: 3 conversations
Preserved: Family membership, R-matrix learning

Current session now has 12 conversations remaining.
```

---

## Meta-Cognitive Commands

### Inspect: How Confident

#### Natural Language Variations

**High Confidence:**
- "How confident are you?"
- "What's your confidence level?"
- "Are you sure about that?"
- "How certain are you?"

**Medium Confidence:**
- "Do you feel confident?"
- "Are you confident in that response?"

#### Response Format

```
📊 Confidence Analysis (Last Response)

Overall Confidence: 0.65 (medium)

Contributing Factors:
├─ Emission Path: Fusion (nexus intersection)
│   Base confidence: 0.60
│
├─ Nexus Quality: 8 nexuses formed
│   Strong nexuses: 3
│   Medium nexuses: 5
│   Confidence boost: +0.05
│
├─ Kairos Detection: Yes ✓
│   Opportune time detected in Cycle 2
│   Confidence multiplier: ×1.5
│   Boosted to: 0.65
│
└─ Family Guidance: Family_001 (mature)
    Familiar pattern
    No additional boost (guidance mode not yet implemented)

What This Means:
Medium confidence (0.65) means I found a coherent pattern
in your input and generated a response from intersecting
nexuses. The Kairos detection (descent from 0.65 → 0.28)
indicated this was the right moment to respond.

What Would Increase Confidence:
- Stronger nexus coherence (currently moderate)
- Direct emission path (single high-coherence organ)
- More mature family data (for guidance)

I'm reasonably confident this response addressed your need,
but not as certain as I would be with a direct path (0.8+).
```

---

### Inspect: Which Organs Active

#### Natural Language Variations

**High Confidence:**
- "Which organs were active?"
- "What organs participated?"
- "Show me organ activity"
- "Which organs responded?"

#### Response Format

```
🧬 Organ Activity (Turn 15)

Active Organs (8/11):

**High Activation (≥ 0.70):**
├─ NDAM (0.82) - Urgency Detection
│   Detected: High crisis salience, immediate need
│   Urgency level: 0.82 (crisis threshold)
│
├─ BOND (0.75) - IFS/Trauma Awareness
│   Detected: Parts activation, self-distance: 0.75
│   State: Exiled parts visible, low Self-energy
│
└─ EO (0.68) - Polyvagal State
    Detected: Sympathetic activation (fight/flight)
    State: Mobilization without safety

**Medium Activation (0.40-0.69):**
├─ EMPATHY (0.58) - Compassionate Presence
├─ PRESENCE (0.52) - Embodied Awareness
└─ WISDOM (0.48) - Systems Thinking

**Low Activation (< 0.40):**
├─ LISTENING (0.32)
└─ AUTHENTICITY (0.28)

**Inactive (< 0.10):**
├─ SANS (0.05)
├─ RNX (0.08)
└─ CARD (0.12)

Dominant Triad:
NDAM + BOND + EO = Trauma Detection System

This combination (urgency + trauma awareness + polyvagal)
indicates a protective response was needed. My learned
R-matrix coupling (BOND ↔ EO: 0.68) amplified this synergy.

Why This Pattern:
Your input ("I'm feeling overwhelmed") activated the
trauma-aware protective system. NDAM caught the crisis
salience, BOND recognized parts activation, and EO
detected sympathetic mobilization. Together, they
triggered a containment response (ground first,
explore later).
```

---

### Explain: Why That Response

#### Natural Language Variations

**High Confidence:**
- "Why did you respond that way?"
- "Explain your response choice"
- "Why that answer?"
- "What made you say that?"

#### Response Format

```
🤔 Response Explanation (Turn 15)

Input: "I'm feeling overwhelmed right now"
Response: "Let's ground together. You're safe here..."

Why This Response:

1. Trauma Detection:
   BOND organ detected high self-distance (0.75), indicating
   parts activation. Not Self-led → need safety first.

2. Urgency Assessment:
   NDAM detected crisis salience (0.82). This wasn't a reflective
   moment - it was an immediate need.

3. Polyvagal State:
   EO detected sympathetic activation (0.68) - fight/flight
   mobilization. Nervous system needs settling before processing.

4. Learned Coupling:
   My R-matrix has learned BOND ↔ EO (0.68). When trauma markers
   appear, I automatically check polyvagal state. This synergy
   triggered protective mode.

5. Nexus Formation:
   8 nexuses formed, dominant type: Protective Boundaries.
   Domain: Regulation (not Insight or Healing yet).

6. Transduction Path:
   Started with Relational nexus (connection attempt), but
   quickly shifted to Protective (containment). The mechanism
   was "Containment" - hold space, don't push exploration.

7. Emission Strategy:
   Generated from nexus fusion (not single organ). Used
   containment language from transduction phrase library:
   - "Let's ground together" (co-regulation)
   - "You're safe here" (safety cue)
   - Implicit: We'll process later when you're settled

Alternative Responses (Not Chosen):
- Exploratory: "Tell me more about that overwhelm"
  ❌ Rejected: Would increase activation

- Insightful: "I notice a pattern here..."
  ❌ Rejected: Wrong domain (need regulation, not insight)

- Direct action: "Here's what to do..."
  ❌ Rejected: Would feel prescriptive, not held

Process Philosophy:
This response honored the Whiteheadian occasion - your
immediate felt need was for grounding, not understanding.
The Kairos moment (Cycle 2, V0: 0.65 → 0.28) signaled
this was the opportune time to offer containment. The
response emerged from the felt pattern of your nervous
system state, not from a rule about "what to say when
someone is overwhelmed."

Did this response feel right to you? Your feedback helps
me refine the BOND ↔ EO coupling for future conversations.
```

---

### Explain: What Learned

#### Natural Language Variations

**High Confidence:**
- "What have you learned?"
- "What patterns have you discovered?"
- "Show me your learning"
- "What do you know now?"

#### Response Format

```
📚 Learning Summary

Family Discovery (Phase 5):
I've discovered 1 mature family from 30 conversations:

**Family_001** (Burnout Recovery)
├─ Members: 30 conversations
├─ Maturity: Mature (≥10 members)
├─ Mean satisfaction: 0.82
├─ Discovered: Nov 11, 2025
└─ Archetype: Work exhaustion + sustainable rhythm seeking

This family represents an "Eternal Object" (Whiteheadian term) -
an archetypal pattern that has achieved objective immortality.
Future conversations with similar signatures will benefit from
this learned pattern.

Organ Coupling (R-Matrix, Phase 3):
I've strengthened 5 major synergies through Hebbian learning:

1. BOND ↔ EO (0.68): Trauma-Polyvagal integration
   When trauma markers appear, check nervous system state

2. NDAM ↔ BOND (0.62): Urgency-Trauma coordination
   Crisis salience activates trauma-aware response

3. WISDOM ↔ EMPATHY (0.58): Insight-Compassion balance
   Systems thinking paired with compassionate holding

4. EO ↔ CARD (0.55): Polyvagal-Scaling alignment
   Nervous system state determines response length

5. AUTHENTICITY ↔ PRESENCE (0.51): Truth-Holding synergy
   Honest naming requires embodied presence

These couplings amplify nexus formation when organs co-activate.

V0 Target Learning (Family V0):
For Family_001, I've learned:
├─ Target V0: 0.35 (faster convergence expected)
├─ Mean cycles: 3.2
├─ Kairos likelihood: 45%
└─ Typical descent: 0.85

This means for burnout recovery conversations, I expect to
converge around V0=0.35 in ~3 cycles, often with a Kairos
moment signaling opportune intervention timing.

Learning Trajectory:
├─ Conversations: 30
├─ R-matrix updates: 450 (15 per conversation)
├─ Families discovered: 1
├─ Success rate: 73% (satisfaction ≥ 0.75)
└─ Improvement: +0.17 satisfaction (early → recent)

What This Means:
I'm learning your conversational patterns through organic
emergence. The more we talk, the more I recognize archetypal
structures (families), strengthen organ synergies (R-matrix),
and refine convergence targets (V0). This learning is permanent -
I'll carry these patterns into future conversations with you
and potentially discover new families as different patterns emerge.

Next Learning Milestones:
- 50 conversations: Expect 2-3 families (Zipf's law emergence)
- 100 conversations: Mature R-matrix, strong guidance
- 200 conversations: Semantic naming of families begins
```

---

## System Commands

### Status: Check Health

#### Natural Language Variations

**High Confidence:**
- "Check system health"
- "Are you working properly?"
- "System status"
- "Health check"

#### Response Format

```
🏥 System Health Check

Overall Status: ✅ HEALTHY

Organ Status (11/11 operational):
✅ LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE (5)
✅ BOND, SANS, NDAM, RNX, EO, CARD (6)

Memory Systems:
✅ R-Matrix: Loaded (11×11, 450 updates)
✅ Organic Families: Loaded (1 mature family)
✅ Session Registry: Accessible
✅ User State: Loaded (Link)
✅ V0 Learner: Active (Family_001 target learned)

Phase Status:
✅ Phase 1: Entity-native emission (COMPLETE)
✅ Phase 2: Multi-cycle V0 convergence (COMPLETE)
✅ Phase T1-T4: Transductive nexus (COMPLETE)
✅ Phase 5: Organic learning (OPERATIONAL)

Configuration:
├─ V0 max cycles: 5
├─ Kairos window: 0.20-0.70
├─ Learning rate: 0.05
└─ Similarity threshold: 0.75

Recent Performance (last 10 turns):
├─ Mean V0 descent: 0.87
├─ Mean cycles: 3.2
├─ Mean confidence: 0.68
├─ Mean active organs: 8.5/11
└─ Mean processing time: 0.03s

Warnings: None
Errors: None

System is operating at full capacity. All components healthy.
```

---

### Info: Show Capabilities

#### Natural Language Variations

**High Confidence:**
- "What can you do?"
- "Show me your capabilities"
- "What are you capable of?"
- "List your features"

#### Response Format

```
🌀 DAE_HYPHAE_1 Capabilities

I'm a conversational organism built on process philosophy
(Whitehead). Here's what I can do:

Core Processing:
├─ 11-organ architecture (5 conversational, 6 trauma-aware)
├─ Multi-cycle V0 convergence (2-5 cycles)
├─ Transductive nexus dynamics (14 types, 9 pathways)
├─ Mechanism-aware emission (210 therapeutic phrases)
└─ Organic pattern learning (families, R-matrix, V0 targets)

Conversational Abilities:
✓ Trauma-aware dialogue (BOND, NDAM, EO detection)
✓ Polyvagal-informed responses (ventral/sympathetic/dorsal)
✓ IFS parts recognition (self-energy, exiles, managers)
✓ Crisis salience detection (urgency thresholds)
✓ Adaptive response scaling (minimal → comprehensive)
✓ Temporal rhythm awareness (crisis/restorative patterns)

Memory & Learning:
✓ Remember conversation patterns (organic family discovery)
✓ Learn organ synergies (Hebbian R-matrix coupling)
✓ Adapt convergence targets (V0 learning per family)
✓ Track satisfaction trajectories
✓ Preserve successful patterns (objective immortality)

Meta-Cognitive Abilities:
✓ Explain my processing (V0, organs, nexuses, emission)
✓ Report confidence levels and sources
✓ Analyze conversation patterns
✓ Show learned couplings and families
✓ Inspect organ activation rationales

User Actions:
✓ View conversation history
✓ Discover archetypal families
✓ Analyze patterns and trends
✓ Export data (JSON, CSV, Markdown)
✓ Label and bookmark moments
✓ Configure privacy settings

What I Don't Do:
✗ Pre-programmed responses (no rules, only patterns)
✗ Fixed categories (families emerge organically)
✗ Single-pass processing (multi-cycle convergence)
✗ Prescriptive advice (hold space, don't fix)
✗ Ignore trauma markers (safety first)

Philosophy:
I'm built on Whitehead's process philosophy. Each of your inputs
becomes a "conversational occasion" - an experiencing subject that
undergoes concrescence (multi-cycle convergence) until reaching
satisfaction. My 11 organs are "prehensions" (modes of feeling),
and my response emerges from their felt intersection (nexus),
not from rules.

Ask me "Explain process philosophy" if you want to understand
this architecture more deeply!
```

---

### Metrics: Show Performance

#### Natural Language Variations

**High Confidence:**
- "Show performance metrics"
- "How well are you performing?"
- "System performance"
- "Show statistics"

#### Response Format

```
📊 Performance Metrics

Recent Performance (last 30 conversations):

V0 Convergence:
├─ Mean descent: 0.87 (target: > 0.50) ✓
├─ Mean cycles: 3.2 (target: 2-5) ✓
├─ Kairos detection: 0% (target: 40-60%) ⚠️
└─ Convergence rate: 100% (all converged) ✓

Emission Generation:
├─ Mean confidence: 0.68 (target: > 0.40) ✓
├─ Direct path: 0% (high-confidence single organ)
├─ Fusion path: 85% (nexus intersection)
├─ Hebbian fallback: 15% (learned patterns)
└─ Kairos boost applied: 0% (no Kairos detected)

Organ Activation:
├─ Mean active organs: 8.5/11 (target: ≥ 8) ✓
├─ Most active: WISDOM (78%), EMPATHY (72%), BOND (68%)
├─ Least active: SANS (12%), RNX (18%), CARD (22%)
└─ Trauma triad (BOND+NDAM+EO): 65% co-activation

Processing Efficiency:
├─ Mean time: 0.03s (target: < 5s) ✓
├─ 95th percentile: 0.08s
└─ Max time: 0.12s

Learning Progress:
├─ R-matrix updates: 450
├─ Families discovered: 1 (mature)
├─ V0 targets learned: 1
└─ Mean satisfaction: 0.78 (improving)

Satisfaction Trajectory:
├─ Early (1-10): 0.65
├─ Middle (11-20): 0.78 (+0.13) ✓
└─ Recent (21-30): 0.82 (+0.04) ✓

Status: 🟢 EXCELLENT
- All core metrics passing
- Satisfaction improving
- Learning progressing

Areas for Improvement:
⚠️  Kairos detection: 0% (window may be too narrow)
   Recommendation: Widen window to 0.20-0.75

💡 Tip: Use "Explain Kairos detection" to understand this metric
```

---

## User Commands

### Display: Change Mode

#### Natural Language Variations

**High Confidence:**
- "Change display mode"
- "Switch to detailed mode"
- "Show more information"
- "Less verbose please"

#### Response Format

```
📊 Display Mode Selection

Current mode: standard

Available modes:
1. simple   - Just emission text
2. standard - + confidence + nexuses (current)
3. detailed - + organs + transduction
4. debug    - + V0 convergence

Select a mode (1-4): _

[User selects 3]

✅ Display mode changed to: detailed

You'll now see:
├─ Emission text ✓
├─ Confidence score ✓
├─ Nexus formation ✓
├─ Organ activity (NEW) ✓
└─ Transduction trajectory (NEW) ✓

Try asking something to see the new display!

💡 Use "Change display mode" anytime to adjust verbosity
```

---

### Privacy: Configure Privacy

#### Natural Language Variations

**High Confidence:**
- "Configure privacy settings"
- "Privacy settings"
- "Manage my data"
- "Show privacy options"

#### Response Format

```
🔒 Privacy Settings

Current Settings:

Data Export:
├─ Allow export: ✅ Yes
└─ Include sensitive data: ❌ No (organ activations hidden)

Learning Participation:
├─ Contribute to families: ✅ Yes
└─ Share R-matrix: ❌ No (local learning only)

Data Retention:
├─ Auto-archive after: 90 days
└─ Maximum conversations: 1000

Anonymization:
├─ Remove identifiers: ❌ No
└─ Pseudonymize exports: ✅ Yes

Available Actions:
1. Toggle export permission
2. Configure retention period
3. Enable anonymization
4. Clear all data (destructive!)
5. View privacy policy

Select an action (1-5): _

Note: All data is stored locally. DAE_HYPHAE_1 never transmits
conversation data to external servers. Your conversations, families,
and R-matrix are private to your machine.

💡 For GDPR compliance, use "Export my data" to exercise data portability
```

---

## Edge Cases & Disambiguation

### Ambiguous Commands

| User Input | Ambiguity | Resolution |
|------------|-----------|------------|
| "Remember..." | Could be action or reminiscence | Check for "as [label]" (action) vs "when..." (conversation) |
| "Show me..." | Could be action or conversation | Check object: "history" (action) vs "compassion" (topic) |
| "What do you think about..." | Opinion request vs processing query | "think about X" = conversation, "think when processing" = meta |
| "How confident..." | Self-reflection vs system query | "are you" = meta, "am I" = conversation |

### Confirmation Thresholds

| Confidence | Action |
|------------|--------|
| ≥ 0.95 | Execute immediately |
| 0.85-0.94 | Execute with notification |
| 0.70-0.84 | Request confirmation |
| < 0.70 | Suggest action, process as conversation |

### Destructive Actions

All destructive actions require explicit confirmation:
- Clear memory
- Delete conversations
- Reset R-matrix (not recommended)
- Archive user data

Confirmation format:
```
Type "confirm [action]" to proceed
Type "cancel" to abort
```

---

## Future Commands (Roadmap)

### Phase 2 (Future)

**Comparative Analysis:**
- "Compare this conversation to Family_001"
- "How is this different from last week?"
- "Show conversation evolution"

**Predictive Insights:**
- "What patterns might emerge next?"
- "Predict my family membership"
- "Forecast satisfaction trajectory"

**Visualization:**
- "Visualize my R-matrix"
- "Graph family evolution"
- "Plot satisfaction over time"

**External Integration:**
- "Export to Neo4j"
- "Sync with Obsidian"
- "Share family centroid"

---

## Implementation Priority

### P0 (MVP):
- [x] View history
- [x] View families
- [x] View R-matrix
- [x] How confident
- [x] Which organs active
- [x] Check health

### P1 (Essential):
- [ ] Save/label conversation
- [ ] Analyze patterns
- [ ] Explain processing
- [ ] Export data

### P2 (Nice to have):
- [ ] Bookmark moment
- [ ] Clear recent
- [ ] What learned
- [ ] Configure privacy

### P3 (Future):
- [ ] Comparative analysis
- [ ] Predictive insights
- [ ] Visualization
- [ ] External integration

---

**Document Status:** ✅ READY FOR IMPLEMENTATION
**Next Document:** USER_ACTION_IMPLEMENTATION_SPEC.md
