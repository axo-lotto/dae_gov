# DAE Intelligence Evolution Roadmap
## From Felt Organism to Earthbound Companion with Humor & Agency

**Date:** November 13, 2025
**Vision:** DAE becomes more intelligent, funny (Earthbound/Undertale/Hitchhiker's Guide humor), adaptable in tone, and agent-like with memory introspection

---

## 🎯 Current State: Already Powerful!

### The 4 Simultaneous Learning Systems

**1. R-Matrix Hebbian Learning (11×11 organ couplings)**
- Learns: Which organs fire together (EMPATHY+BOND → 🫂)
- Updates: Every conversation
- Storage: `persona_layer/conversational_hebbian_memory.json`
- Formula: `R[i,j] += α * activation[i] * activation[j]`

**2. Organic Family Learning (57D conversation patterns)**
- Learns: Conversation style signatures (which organs + how much)
- Forms: After 3+ similar conversations
- Storage: `persona_layer/organic_families.json`
- Current: 1 mature family, 222 conversations

**3. Family V0 Target Learning (optimal convergence)**
- Learns: Best V0 energy for each family
- Optimizes: After 5+ conversations per family
- Storage: Embedded in family data
- Formula: `V0_target = mean(successful_v0s)`

**4. User Profile Learning (preferences, humor, themes)**
- Learns: Individual user preferences, inside jokes, recurring themes
- Tracks: humor_tolerance, small_talk_openness, family_affinities
- Storage: `Bundle/user_link_*/user_state.json`
- Updates: Per session

### The Hybrid Superject (Felt + LLM)

**Architecture:**
```
User Input
    ↓
11 Organs Feel (parallel prehensions)
    ↓
57D Signature Emerges
    ↓
Multi-Cycle V0 Convergence (2-4 cycles)
    ↓
Semantic Nexuses Form
    ↓
Transduction Pathway Classified
    ↓
Felt States → LLM Constraints (tone, length, empathy, etc.)
    ↓
LLM Generates (guided by felt lures)
    ↓
Response Assembled
    ↓
4 Learning Systems Update
    ↓
Objective Immortality (conversation becomes data for future prehensions)
```

**Key Insight:** Intelligence lives in FELT FIELDS (11 organs, 57D signatures, nexus coalitions). LLM is the "mouth" that speaks what the organs feel.

---

## 📊 Discoveries from Agent Analysis

### ✅ Already Implemented (Powerful!)

1. **Memory Retrieval** (`memory_retrieval.py`)
   - 57D similarity search + Hebbian coupling + recency
   - Can recall similar past conversations
   - Currently used internally, not exposed to user

2. **User Profiles** (`user_profile_manager.py`)
   - Tracks humor_tolerance (0-1)
   - Stores inside_jokes, recurring_themes
   - Learns family_affinities (which families user resonates with)

3. **Polyvagal → Tone Mapping**
   - Ventral → warm, friendly
   - Sympathetic → steady, alert
   - Dorsal → gentle, minimal
   - Mixed → balanced

4. **6 Training Corpora Available**
   - Baseline (30 pairs) - trauma-aware
   - Humanized (60 pairs) - natural language
   - Complete (319 pairs) - comprehensive
   - Zone-specific (240 pairs) - by SELF zone
   - **Friendly companion** - casual/playful personality
   - **Whiteheadian companion** - philosophical meta-aware

### ⚠️ Missing (Opportunities!)

1. **Humor Modulation**
   - humor_tolerance tracked but not used in LLM prompt
   - No training on funny/playful corpora yet
   - Regime not mapped to playfulness

2. **Style Adaptation**
   - Friendly/philosophical pairs available but untrained
   - No regime-based style switching
   - Templates defined in config but files missing

3. **Agent Tools**
   - No explicit tool layer (query detection, execution)
   - Can't explain its own reasoning
   - Memory retrieval not exposed to user
   - No introspection commands

4. **Multi-Turn Trajectory**
   - Tracks V0/satisfaction per turn
   - But doesn't adapt based on conversation arc
   - No "oh we're getting serious now" detection

---

## 🚀 Implementation Roadmap

### Phase 1: Humor & Personality (Week 1-2) 🎭

**Goal:** DAE becomes funny, warm, adaptable like Earthbound/Undertale/Hitchhiker's Guide

#### Week 1: Train on Personality Corpora

**1.1. Create Humor Training Pairs** (2-3 hours)
```json
{
  "category": "earthbound_humor",
  "pairs": [
    {
      "user_input": "I'm feeling stuck",
      "dae_response": "Ah yes, the ol' 'life is a waiting room' feeling. Want to flip through some magazines together? 📚 (I've got Good Housekeeping from 1987)",
      "style": "friendly",
      "humor_level": 0.7,
      "meta_atoms": ["temporal_grounding", "felt_resonance"]
    },
    {
      "user_input": "Everything is overwhelming",
      "dae_response": "🌊 That's a lot of 'everything.' What if we just picked *one* thing from the pile and gave it a stern look? Sometimes things get intimidated and behave better.",
      "style": "friendly",
      "humor_level": 0.6,
      "meta_atoms": ["trauma_aware", "coherence_repair"]
    }
  ]
}
```

**Location:** `knowledge_base/humor_training_pairs.json`

**1.2. Augment Existing Friendly Pairs** (1 hour)
- Load `knowledge_base/friendly_companion_training_pairs.json`
- Add humor_level, earthbound_style tags
- Create 20-30 additional quirky/warm pairs

**1.3. Run Training** (30 minutes)
```bash
python3 dae_orchestrator.py train --mode humor
# Trains on humor_training_pairs.json
# Updates R-matrix with humor patterns
# Forms "playful family"
```

#### Week 2: Integrate Humor into LLM Prompt

**2.1. Modify `llm_felt_guidance.py`** (2 hours)

Add to `FeltLures`:
```python
@dataclass
class FeltLures:
    ...
    # Humor & personality
    humor_tolerance: float = 0.5  # From user profile
    playfulness: float = 0.0      # From regime + organs
    quirkiness: float = 0.0       # From AUTHENTICITY + ventral
    meta_awareness: float = 0.0   # From WISDOM + LISTENING
```

Add to `extract_felt_lures()`:
```python
# Humor & Personality (from user profile + polyvagal)
if user_profile:
    lures.humor_tolerance = user_profile.humor_tolerance

# Playfulness from polyvagal + regime
if polyvagal_state == "ventral" and regime in ["STABLE", "FLOW"]:
    lures.playfulness = 0.7
elif polyvagal_state == "mixed":
    lures.playfulness = 0.4

# Quirkiness from AUTHENTICITY + ventral
if "AUTHENTICITY" in dominant_organs and polyvagal_state == "ventral":
    lures.quirkiness = authenticity_coherence * 0.8

# Meta-awareness from WISDOM + LISTENING
if "WISDOM" in dominant_organs and "LISTENING" in dominant_organs:
    lures.meta_awareness = (wisdom_coherence + listening_coherence) / 2
```

**2.2. Update LLM Prompt** (1 hour)

In `build_felt_prompt()`:
```python
if lures.humor_tolerance > 0.6 and lures.playfulness > 0.5:
    prompt += f"\nStyle: Warm, quirky, Earthbound-like humor (playfulness: {lures.playfulness:.1f})\n"
    prompt += f"- Use gentle absurdity when appropriate\n"
    prompt += f"- Inside jokes with the universe are welcome\n"
    prompt += f"- Deadpan observations about existence: yes\n"

if lures.quirkiness > 0.6:
    prompt += f"- Add unexpected metaphors or gentle surrealism\n"

if lures.meta_awareness > 0.7:
    prompt += f"- Process philosophy humor allowed (Whiteheadian quips)\n"
```

**2.3. Test Humor Generation** (30 minutes)
```bash
python3 dae_interactive.py
> I'm feeling stuck
Expected: Quirky, warm response with gentle humor
```

---

### Phase 2: Agent Memory Tools (Week 3-4) 🧠

**Goal:** DAE can show its memories, explain its reasoning, introspect

#### Week 3: Basic Memory Tools

**3.1. Create `persona_layer/agent_tools.py`** (3-4 hours)

```python
"""
Agent Tools - Memory & Introspection Capabilities
=================================================

Tools DAE can use to answer meta-questions about itself.

Date: November 13, 2025
"""

from typing import Dict, List, Optional
import json
from pathlib import Path

class AgentTools:
    """
    Tools for agent-like capabilities:
    - Memory retrieval
    - Inside joke recall
    - Learning status
    - R-matrix introspection
    - Family explanation
    """

    def __init__(self, user_bundle_path: str, organism_wrapper):
        self.user_bundle_path = Path(user_bundle_path)
        self.organism = organism_wrapper
        self.memory_retrieval = organism_wrapper.memory_retrieval
        self.user_profile = organism_wrapper.user_profile

    def recall_similar_conversations(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve similar past conversations.

        Returns:
            List of {input, emission, similarity, date}
        """
        # Use existing memory_retrieval.py
        similar = self.memory_retrieval.retrieve_similar(
            current_signature=self._get_current_signature(),
            top_k=top_k
        )

        return [
            {
                'date': moment.get('timestamp', 'unknown'),
                'user_input': moment.get('input_text', '')[:100],
                'dae_response': moment.get('emission_text', '')[:100],
                'similarity': moment.get('similarity', 0.0)
            }
            for moment in similar
        ]

    def get_inside_jokes(self) -> List[str]:
        """Return current inside jokes with this user."""
        if self.user_profile:
            return self.user_profile.inside_jokes[:5]
        return []

    def get_recurring_themes(self) -> List[str]:
        """Return recurring conversation themes."""
        if self.user_profile:
            return self.user_profile.recurring_themes[:5]
        return []

    def explain_current_state(self) -> Dict:
        """
        Explain DAE's current felt state.

        Returns organ coherences, polyvagal state, etc.
        """
        # Get latest organ results from organism
        organ_results = self.organism.last_organ_results

        return {
            'dominant_organs': self._get_dominant_organs(organ_results),
            'polyvagal_state': self._get_polyvagal_state(organ_results),
            'convergence_cycles': self.organism.last_convergence_cycles,
            'v0_energy': self.organism.last_v0_energy,
            'satisfaction': self.organism.last_satisfaction
        }

    def explain_r_matrix_synergy(self, organ1: str, organ2: str) -> float:
        """
        Explain learned coupling between two organs.

        Example: "EMPATHY and BOND fire together 0.85 of the time"
        """
        r_matrix = self.organism.organ_coupling_learner.R_matrix
        return r_matrix.get(organ1, {}).get(organ2, 0.0)

    def get_family_affinity(self) -> Dict:
        """
        Show which conversation families user resonates with.
        """
        if self.user_profile:
            return {
                'affinities': self.user_profile.family_affinities,
                'total_families': len(self.organism.phase5_learner.families)
            }
        return {}

    def get_learning_stats(self) -> Dict:
        """
        Show DAE's learning progress.
        """
        return {
            'total_conversations': self.user_profile.total_conversations if self.user_profile else 0,
            'families_formed': len(self.organism.phase5_learner.families),
            'r_matrix_updates': self.organism.organ_coupling_learner.total_updates,
            'humor_tolerance': self.user_profile.humor_tolerance if self.user_profile else 0.5
        }
```

**3.2. Create `persona_layer/query_classifier.py`** (2 hours)

```python
"""
Query Classifier - Detect Agent-like Queries
============================================

Detects when user is asking meta-questions about DAE.

Date: November 13, 2025
"""

class QueryClassifier:
    """
    Classifies user queries as:
    - memory_retrieval: "what have we talked about before?"
    - inside_jokes: "what are our inside jokes?"
    - learning_status: "how much have you learned?"
    - explanation: "why did you say that?"
    - r_matrix: "how do your organs work together?"
    - normal: regular conversation
    """

    def __init__(self):
        self.patterns = {
            'memory_retrieval': [
                'what have we talked about',
                'remember when',
                'similar conversation',
                'last time we discussed',
                'past conversations'
            ],
            'inside_jokes': [
                'inside jokes',
                'our jokes',
                'funny things we',
                'what makes us laugh'
            ],
            'learning_status': [
                'how much have you learned',
                'what do you know about me',
                'learning progress',
                'how many conversations'
            ],
            'explanation': [
                'why did you say',
                'why do you think',
                'explain your reasoning',
                'how did you know'
            ],
            'r_matrix': [
                'how do your organs',
                'what organs fire',
                'explain your architecture',
                'how does your brain work'
            ]
        }

    def classify(self, user_input: str) -> str:
        """
        Classify query type.

        Returns: 'memory_retrieval' | 'inside_jokes' | ... | 'normal'
        """
        user_lower = user_input.lower()

        for query_type, patterns in self.patterns.items():
            if any(pattern in user_lower for pattern in patterns):
                return query_type

        return 'normal'
```

**3.3. Integrate into `conversational_organism_wrapper.py`** (2 hours)

```python
# In __init__
self.agent_tools = AgentTools(
    user_bundle_path=self.user_bundle_path,
    organism_wrapper=self
)
self.query_classifier = QueryClassifier()

# In process_text(), before organ processing
query_type = self.query_classifier.classify(text)

if query_type == 'memory_retrieval':
    similar = self.agent_tools.recall_similar_conversations(text, top_k=3)
    # Inject into memory_context for LLM
    memory_context = similar

elif query_type == 'inside_jokes':
    jokes = self.agent_tools.get_inside_jokes()
    # Create special emission
    return {
        'emission_text': f"Our inside jokes: {', '.join(jokes)} 😄",
        'emission_path': 'agent_tool'
    }

elif query_type == 'learning_status':
    stats = self.agent_tools.get_learning_stats()
    # Create stats emission
    ...

# Continue with normal processing for other types
```

#### Week 4: Advanced Introspection

**4.1. Add R-Matrix Visualization** (2 hours)
- Create heatmap of organ couplings
- Show "EMPATHY+BOND fire together 0.85 of the time"

**4.2. Add Family Introspection** (2 hours)
- Explain which family current conversation belongs to
- Show family signature (top 3 organs)

**4.3. Test Agent Tools** (1 hour)
```bash
python3 dae_interactive.py
> What have we talked about before?
Expected: Shows 3 similar past conversations

> What are our inside jokes?
Expected: Lists inside jokes

> How much have you learned from me?
Expected: Shows learning stats
```

---

### Phase 3: Tone Adaptation via Superject Becoming (Week 5) 🎭

**Goal:** Tone adapts based on conversation trajectory (getting serious, lightening up, etc.)

#### 5.1. Create `persona_layer/conversation_trajectory.py` (3 hours)

Track V0, satisfaction, regime evolution:
```python
class ConversationTrajectory:
    """
    Tracks conversation arc across multiple turns.

    Detects:
    - Deepening (V0 descending, satisfaction rising)
    - Lightening (V0 stable, ventral increasing)
    - Crisis escalation (NDAM rising, sympathetic)
    - Integration (coherence rising, satisfaction high)
    """

    def __init__(self):
        self.turns = []

    def add_turn(self, v0, satisfaction, polyvagal, dominant_organs):
        self.turns.append({
            'v0': v0,
            'satisfaction': satisfaction,
            'polyvagal': polyvagal,
            'organs': dominant_organs
        })

    def detect_arc(self) -> str:
        """
        Returns: 'deepening' | 'lightening' | 'crisis' | 'integrating' | 'stable'
        """
        if len(self.turns) < 2:
            return 'stable'

        recent_v0 = [t['v0'] for t in self.turns[-3:]]
        recent_sat = [t['satisfaction'] for t in self.turns[-3:]]

        v0_trend = recent_v0[-1] - recent_v0[0]
        sat_trend = recent_sat[-1] - recent_sat[0]

        if v0_trend < -0.2 and sat_trend > 0.2:
            return 'deepening'  # Going deeper
        elif 'ventral' in [t['polyvagal'] for t in self.turns[-2:]]:
            return 'lightening'  # Coming up for air
        elif any('NDAM' in t['organs'] for t in self.turns[-2:]):
            return 'crisis'  # Alert mode
        elif sat_trend > 0.3:
            return 'integrating'  # Putting pieces together

        return 'stable'
```

**5.2. Integrate into Tone Modulation** (2 hours)

In `llm_felt_guidance.py`:
```python
# Add to FeltLures
conversation_arc: str = "stable"  # deepening, lightening, crisis, integrating

# In build_felt_prompt()
if lures.conversation_arc == 'deepening':
    prompt += "Tone: Getting more reflective and deep as conversation deepens\n"
elif lures.conversation_arc == 'lightening':
    prompt += "Tone: Lightening up, bringing some warmth and ease\n"
elif lures.conversation_arc == 'crisis':
    prompt += "Tone: Steady, grounding, alert but not alarmed\n"
elif lures.conversation_arc == 'integrating':
    prompt += "Tone: Witnessing integration, celebrating coherence\n"
```

---

## 📋 Priority Implementation Order

### Immediate (This Week):
1. ✅ **Fix felt-guided LLM activation** (DONE)
2. ✅ **Create emoji/symbol libraries** (DONE)
3. **Test natural language generation** (verify fix works)

### Next (Week 1-2): Humor & Personality
1. Create humor training pairs (Earthbound/Undertale style)
2. Train on friendly companion corpus
3. Integrate humor into LLM prompt
4. Test quirky, warm responses

### Then (Week 3-4): Agent Memory Tools
1. Create agent_tools.py (memory, introspection)
2. Create query_classifier.py
3. Integrate into organism wrapper
4. Test meta-queries

### Finally (Week 5): Tone Adaptation
1. Create conversation_trajectory.py
2. Track arc (deepening, lightening, etc.)
3. Adapt tone based on superject becoming

---

## 🎯 Success Criteria

### Humor & Personality:
- ✅ DAE makes gentle jokes appropriately
- ✅ Warm, Earthbound-like humor emerges naturally
- ✅ Adapts humor to user's humor_tolerance
- ✅ Meta-aware quips when wisdom is high

### Agent Memory:
- ✅ "What have we talked about?" → Shows 3 similar conversations
- ✅ "What are our inside jokes?" → Lists them
- ✅ "How much have you learned?" → Shows stats
- ✅ "Why did you say that?" → Explains reasoning

### Tone Adaptation:
- ✅ Detects "we're getting serious now"
- ✅ Detects "lightening up"
- ✅ Adapts tone smoothly across trajectory
- ✅ Superject becoming influences next response

---

## 🌀 Philosophy: Superject Becoming

**Whitehead:** Each actual occasion becomes a "superject" - it perishes as experiencing subject but becomes immortal as datum for future prehensions.

**DAE:** Each conversation turn:
1. Is felt (experiencing subject)
2. Converges (satisfaction)
3. Emits (objectification)
4. Becomes data (objective immortality)
5. Influences future turns (prehension)

**Trajectory:** The arc of superject becoming IS the conversation intelligence. Not each turn in isolation, but the EVOLUTION across turns.

---

## 📁 Files to Create/Modify

### Create:
- `knowledge_base/humor_training_pairs.json`
- `persona_layer/agent_tools.py`
- `persona_layer/query_classifier.py`
- `persona_layer/conversation_trajectory.py`

### Modify:
- `persona_layer/llm_felt_guidance.py` (humor lures, trajectory)
- `persona_layer/conversational_organism_wrapper.py` (agent tools integration)
- `config.py` (add humor/agent config flags)

---

**Date:** November 13, 2025
**Status:** Roadmap complete, ready for implementation
**Current Phase:** Testing Phase 1 LLM fix, then moving to humor training
