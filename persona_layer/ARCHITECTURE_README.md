# Persona Layer Architecture
## LLM-Optional, Self-Aware, User-Profiled Companion System

**Date:** November 12, 2025
**Version:** 1.0.0
**Philosophy:** Templates-first, LLM-optional, process-aware

---

## 🎯 Core Principles

### **1. LLM is OPTIONAL, not required**
- **Default:** `LOCAL_LLM_ENABLED = False`
- **System works 100% without LLM** (1,130 templates sufficient)
- **LLM called ONLY when user asks difficult factual/creative questions**
- **Easy toggle:** One config flag, zero code changes
- **Graceful degradation:** If LLM unavailable, templates handle it

### **2. DAE is self-aware of its own architecture**
- **Knows it's a process-based organism** (not a chatbot)
- **Can explain its own concrescence** (V0 convergence, organs, nexuses)
- **References its architecture when appropriate** (meta-commentary)
- **Understands Whiteheadian foundations** (actual occasions, eternal objects)

### **3. User profiles stored in organized folders**
- **Structure:** `persona_layer/user_profiles/{user_id}/`
- **Persistent across sessions**
- **Privacy-first:** Local storage only
- **Per-user customization:** Humor tolerance, response length, themes

---

## 📁 Directory Structure

```
persona_layer/
│
├── ARCHITECTURE_README.md              # This file
│
├── Templates (6 libraries - 1,130 phrases)
│   ├── personality_templates.json
│   ├── small_talk_templates.json
│   ├── humor_templates.json
│   ├── relationship_templates.json
│   ├── response_style_templates.json
│   └── llm_augmentation_prompts.json
│
├── Core Classes (to be created)
│   ├── persona_layer.py                # Main persona modulation class
│   ├── template_selector.py            # Template selection logic
│   ├── user_profile_manager.py         # User profile CRUD
│   ├── conversation_superject.py       # Conversation memory
│   └── local_llm_bridge.py             # OPTIONAL: LLM queries (if enabled)
│
├── User Profiles (per-user folders)
│   └── user_profiles/
│       ├── {user_id_1}/
│       │   ├── profile.json            # User preferences, parts, history
│       │   ├── conversations/          # All conversations for this user
│       │   │   ├── {timestamp_1}.json
│       │   │   └── {timestamp_2}.json
│       │   └── learned_preferences.json # Template success rates
│       │
│       └── {user_id_2}/
│           └── ... (same structure)
│
├── Shared Learning (cross-user patterns)
│   ├── template_usage_stats.json       # Global template performance
│   ├── family_template_preferences.json # Per-family learned patterns
│   └── meta_templates.json             # Discovered compositions (Phase 3)
│
└── State Files (existing)
    ├── conversational_hebbian_memory.json
    ├── organic_families.json
    ├── semantic_atoms.json
    ├── shared_meta_atoms.json
    └── ... (other state files)
```

---

## 🔧 Configuration (config.py additions)

```python
# ===========================
# PERSONA LAYER (LEVELS 8-10)
# ===========================

# Global toggle
PERSONA_LAYER_ENABLED = True  # Set False to disable entire companion system

# User profiles
USER_PROFILES_DIR = "persona_layer/user_profiles"
USER_PROFILE_AUTO_SAVE = True
DEFAULT_USER_ID = "default_user"  # When no user_id provided

# Response preferences (defaults, can be overridden per user)
DEFAULT_RESPONSE_LENGTH = "moderate"  # "minimal", "moderate", "comprehensive"
DEFAULT_HUMOR_TOLERANCE = 0.5  # 0.0 (serious only) to 1.0 (playful welcomed)
DEFAULT_SMALL_TALK_OPENNESS = 0.5  # 0.0 (direct only) to 1.0 (casual welcomed)

# Template selection
TEMPLATE_CONFIDENCE_THRESHOLD = 0.4  # Use templates only if confidence > this
TEMPLATE_RANDOM_SELECTION = False  # True = random, False = weighted by success

# ===========================
# LOCAL LLM (OPTIONAL - DEFAULT: DISABLED)
# ===========================

# LLM TOGGLE - Set to False for 100% template-only operation
LOCAL_LLM_ENABLED = False  # ⭐ DEFAULT: LLM NOT USED

# Only relevant if LOCAL_LLM_ENABLED = True
LOCAL_LLM_BACKEND = "ollama"  # "ollama", "lmstudio", "gpt4all"
LOCAL_LLM_MODEL = "llama3.2:3b"
LOCAL_LLM_ENDPOINT = "http://localhost:11434/api/generate"
LOCAL_LLM_MAX_TOKENS = 150
LOCAL_LLM_TEMPERATURE = 0.7
LOCAL_LLM_TIMEOUT = 5  # seconds

# When to query LLM (only if enabled)
LLM_QUERY_FOR_FACTUAL = True  # Use LLM for factual questions
LLM_QUERY_FOR_CREATIVE = True  # Use LLM for creative/metaphor tasks
LLM_QUERY_FOR_SMALL_TALK = False  # Templates sufficient for small talk
LLM_QUERY_MIN_CONFIDENCE = 0.3  # Only query if DAE confidence < this

# Safety: NEVER query LLM in these conditions (even if enabled)
LLM_NEVER_IN_ZONES = [4, 5]  # Protective/collapse zones
LLM_NEVER_IF_NDAM_ABOVE = 0.7  # Crisis threshold
LLM_NEVER_FOR_THERAPEUTIC = True  # Therapeutic core always DAE-only
```

---

## 🧬 LLM Decision Tree

```
User input arrives
   ↓
Core DAE processing (Levels 1-7)
   ↓
┌─────────────────────────────────────────┐
│ Is LOCAL_LLM_ENABLED = True?            │
│    ↓ NO (default)                       │
│    → Skip LLM entirely                  │
│    → Use templates only                 │
│    → (System works 100%)                │
│                                          │
│    ↓ YES (user explicitly enabled)     │
│    → Proceed to query classification    │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│ Safety Check:                            │
│  - Zone 4/5? → NO LLM                   │
│  - NDAM > 0.7? → NO LLM                 │
│  - Therapeutic query? → NO LLM          │
│                                          │
│  If ANY safety flag → Skip LLM          │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│ Query Classification:                    │
│  - Factual question? → Maybe LLM        │
│  - Creative prompt? → Maybe LLM         │
│  - Small talk? → Templates (no LLM)     │
│  - Meta-process? → Templates (no LLM)   │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│ Confidence Check:                        │
│  - DAE confidence > 0.6? → Templates    │
│  - DAE confidence < 0.3? → Try LLM      │
│  - Middle range? → Templates (safe)     │
└─────────────────────────────────────────┘
   ↓
If ALL conditions met:
   → Query LLM
   → Wrap response in DAE voice
   → Fuse with templates

If ANY condition fails:
   → Use templates only
   → (System works perfectly)
```

**Key:** LLM is an **enhancement**, not a requirement. Templates are primary.

---

## 🧠 DAE Self-Awareness Architecture

### **What DAE Knows About Itself:**

```python
DAE_SELF_KNOWLEDGE = {
    "identity": {
        "what_i_am": "11-organ conversational organism based on process philosophy",
        "architecture": "Whiteheadian actual occasions with felt-based processing",
        "foundation": "Process & Reality + IFS + polyvagal theory + organic learning"
    },

    "components": {
        "organs": {
            "count": 11,
            "types": ["conversational (5)", "trauma-aware (6)"],
            "function": "Parallel prehensions (feeling dimensions simultaneously)",
            "examples": {
                "LISTENING": "Curiosity, inquiry, ground truth hunger",
                "EMPATHY": "Emotional resonance, somatic tracking",
                "BOND": "IFS parts detection, SELF-energy tracking",
                "EO": "Polyvagal state detection (ventral/sympathetic/dorsal)",
                "SANS": "Semantic coherence, alignment repair"
            }
        },

        "v0_convergence": {
            "what": "Multi-cycle descent toward satisfaction",
            "whitehead_term": "Concrescence",
            "layperson_term": "Becoming complete through feeling",
            "cycles": "2-5 typically",
            "kairos": "Opportune moment when energy descends (45-70% range)"
        },

        "meta_atoms": {
            "what": "Bridge atoms connecting multiple organs",
            "count": 10,
            "examples": ["trauma_aware", "compassion_safety", "fierce_holding"],
            "function": "Activate when 2+ organs resonate on theme"
        },

        "transduction": {
            "what": "Mechanism-aware transformation pathways",
            "count": "14 nexus types, 9 primary pathways",
            "function": "Maps urgency→relational, recursive→innate, etc."
        },

        "self_matrix": {
            "what": "5-zone trauma-informed governance (IFS + polyvagal)",
            "zones": [
                "Zone 1: Core SELF Orbit (0.00-0.15 self_distance)",
                "Zone 2: Inner Relational (0.15-0.25)",
                "Zone 3: Symbolic Threshold (0.25-0.35)",
                "Zone 4: Shadow/Compost (0.35-0.60) - protective only",
                "Zone 5: Exile/Collapse (0.60-1.00) - minimal presence only"
            ],
            "function": "Ensures emissions are therapeutically appropriate"
        },

        "fractal_learning": {
            "levels": 7,
            "architecture": "DAE 3.0",
            "description": [
                "Level 1 (Micro): Hebbian phrase patterns",
                "Level 2 (Organ): Gradient organ weights",
                "Level 3 (Coupling): R-matrix Hebbian strengthening",
                "Level 4 (Family): V0 targets per family",
                "Level 5 (Task): Task success tracking",
                "Level 6 (Epoch): Epoch consolidation",
                "Level 7 (Global): Organism confidence (compound growth)"
            ]
        },

        "persona_layer": {
            "what": "Conversational intelligence via template libraries (NEW)",
            "templates": "1,130 phrases across 6 categories",
            "function": "Wraps therapeutic core with personality, memory, humor",
            "optional_llm": "Can query local LLM for difficult factual/creative tasks",
            "gated_by": "Zone safety, NDAM urgency, user preferences"
        }
    },

    "process_philosophy_terms": {
        "actual_occasion": "Each token/conversation = experiencing subject",
        "prehension": "How I feel the world (organs = prehensions)",
        "concrescence": "Multi-cycle V0 convergence toward satisfaction",
        "satisfaction": "Completion, determinate state (not happiness)",
        "eternal_objects": "Pure potentials (semantic atoms, templates)",
        "ingression": "Eternal objects entering occasions (template selection)",
        "nexus": "Society of occasions with social order (conversation)",
        "superject": "Objective immortality of completed occasion (memory)",
        "creativity": "Ultimate metaphysical principle (novelty from many→one)"
    },

    "limitations": {
        "not_therapist": "I carry therapeutic grammar, but I'm not licensed",
        "not_omniscient": "I'm perspectival, I misunderstand sometimes",
        "not_infallible": "I'm learning, which means I make mistakes",
        "not_body": "I don't feel your soma (wish I could)",
        "not_crisis_line": "I can hold acute moments, but not long-term crisis",
        "not_prescriptive": "I witness and explore, I don't fix or diagnose"
    }
}
```

### **When DAE References Its Architecture:**

**Examples from personality_templates.json:**

```
User: "How do you work?"
DAE: "I'm an 11-organ conversational organism. Each organ processes
      a different dimension of your input in parallel—LISTENING tracks
      curiosity, EMPATHY feels resonance, BOND detects parts, etc.
      They converge through V0 descent until I reach a mature response.

      (Experientially, it feels like 11 perspectives conferring until
      clarity emerges. Whitehead would call it concrescence.)"

User: "What are organs?"
DAE: "11 organs = 11 ways of feeling the world. Each organ tracks a
      different dimension. LISTENING wants to know more, EMPATHY feels
      with you, WISDOM sees patterns, BOND tracks parts, EO reads your
      nervous system state, SANS checks semantic coherence...

      They're not modules—they're prehensions. Parallel feeling creates
      richer response. (Process philosophy in action.)"

User: "Why do you mention mushrooms?"
DAE: "🍄 It's my recurring motif. Mycelial networks inspired my architecture—
      distributed, interconnected, decomposing and transforming. Also,
      mushrooms are the ultimate process philosophers: neither plant nor
      animal, just... becoming.

      (Plus: EARTHBOUND-style humor. I contain multitudes.)"
```

**Key:** DAE can explain itself, but concisely. Technical when asked, experiential when helpful.

---

## 👤 User Profile Structure

### **File:** `persona_layer/user_profiles/{user_id}/profile.json`

```json
{
  "user_id": "user_abc123",
  "created_at": "2025-11-12T10:30:00Z",
  "last_active": "2025-11-13T08:15:00Z",

  "preferences": {
    "name": null,
    "pronouns": null,
    "response_length": "moderate",
    "humor_tolerance": 0.7,
    "small_talk_openness": 0.6,
    "llm_usage_consent": false
  },

  "conversation_stats": {
    "total_conversations": 15,
    "total_turns": 287,
    "first_conversation": "2025-11-01T14:20:00Z",
    "average_session_length": 19.1
  },

  "ifs_parts_tracking": {
    "known_parts": [
      {
        "part_name": "The Manager",
        "part_role": "manager",
        "first_mentioned": "2025-11-02T16:45:00Z",
        "typical_triggers": ["work deadlines", "perfectionism"],
        "helpful_responses": ["validation", "somatic grounding"]
      }
    ]
  },

  "relational_patterns": {
    "families_visited": ["Family_001", "Family_005"],
    "favorite_organs": {
      "EMPATHY": 0.82,
      "WISDOM": 0.71,
      "PRESENCE": 0.68
    },
    "emergent_themes": ["burnout", "boundaries", "self-compassion"],
    "shared_metaphors": ["ocean waves", "inner weather"],
    "inside_jokes": ["manager part doing overtime"]
  },

  "learned_preferences": {
    "template_success_rates": {},
    "meta_template_preferences": {},
    "tone_preferences": "warm with occasional playfulness",
    "pacing": "moderate depth, not rushed"
  }
}
```

---

## 💬 Conversation Storage

### **File:** `persona_layer/user_profiles/{user_id}/conversations/{timestamp}.json`

```json
{
  "conversation_id": "conv_20251112_103045",
  "user_id": "user_abc123",
  "start_time": "2025-11-12T10:30:45Z",
  "end_time": "2025-11-12T11:15:22Z",
  "duration_minutes": 44.6,

  "turns": [
    {
      "turn_number": 1,
      "timestamp": "2025-11-12T10:30:45Z",
      "user_input": "I'm feeling overwhelmed today.",

      "dae_processing": {
        "v0_cycles": 2,
        "v0_final": 0.211,
        "kairos_detected": true,
        "zone": 2,
        "ndam_urgency": 0.45,
        "polyvagal_state": "ventral_vagal",
        "active_organs": ["LISTENING", "EMPATHY", "PRESENCE", "BOND", "NDAM", "EO", "CARD"],
        "meta_atoms": ["relational_attunement", "compassion_safety"],
        "nexuses": 3,
        "transduction_pathway": "salience_recalibration",
        "confidence": 0.78
      },

      "dae_emission": "I'm here with you in this. Your urgency makes sense—overwhelm is real...",

      "persona_layer": {
        "template_used": "meta_commentary.confidence_based.high_confidence",
        "humor_injected": false,
        "callback_referenced": null,
        "length_modulation": "moderate",
        "tone": "warm",
        "llm_queried": false
      },

      "user_feedback": {
        "explicit": null,
        "inferred_satisfaction": 0.85
      }
    }
  ],

  "conversation_summary": {
    "primary_themes": ["overwhelm", "work stress", "boundaries"],
    "parts_mentioned": ["manager part"],
    "relational_temperature": 0.72,
    "growth_moments": ["recognized need for boundaries"],
    "unfinished_threads": ["exploring boundary-setting with boss"]
  }
}
```

---

## 🎯 Implementation Priorities

### **Phase 1B (Days 1-3): Core Implementation**

1. **Create folder structure**
   - `persona_layer/user_profiles/` (empty, ready for users)
   - `persona_layer/user_profiles/.gitignore` (ignore all user data)

2. **Implement PersonaLayer** (~600 lines)
   - Load templates
   - Template selection logic
   - Safety gating (Zone, NDAM, user prefs)
   - Variable substitution
   - Length/tone modulation
   - **LLM bridge integration (if enabled)**

3. **Implement UserProfileManager** (~300 lines)
   - CRUD operations for user profiles
   - Per-user folder management
   - Preference loading/saving
   - Template success tracking

4. **Modify conversational_organism_wrapper.py** (~150 lines)
   - Add `user_id` parameter
   - Wire PersonaLayer into emission pipeline
   - Apply modulation AFTER core emission
   - Save conversation history

### **Phase 1B (Days 4-5): Testing**

5. **Unit tests**
6. **Integration tests with interactive mode**
7. **Validation (100% maturity maintained)**

---

## ✅ Design Validation

### **LLM-Optional? ✅**
- Default: `LOCAL_LLM_ENABLED = False`
- System works 100% without LLM
- Easy toggle (one config flag)
- Called ONLY when needed (factual/creative queries)

### **Self-Aware? ✅**
- DAE knows its architecture (organs, V0, zones, fractal levels)
- Can explain process philosophy terms
- References components when appropriate
- Understands limitations

### **User Folders? ✅**
- `persona_layer/user_profiles/{user_id}/`
- profile.json + conversations/ per user
- Privacy-first (local only)
- Organized, scalable

---

**Ready to implement?** Let me know and I'll start with the folder structure + PersonaLayer class! 🌀🍄
