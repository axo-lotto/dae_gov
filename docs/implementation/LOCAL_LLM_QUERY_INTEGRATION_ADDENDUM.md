# Local LLM Query Integration Addendum
## Affordable Local LLM for Complex DAE Questions

**Date:** November 12, 2025
**Status:** 🎯 **DESIGN READY FOR IMPLEMENTATION**
**Integration Point:** Level 10 (Mythological Persona Layer)
**Foundation:** DAE Companion Architecture + Process Philosophy

---

## 🎯 Purpose

Enable DAE to query an affordable local LLM when:
1. User asks complex factual questions outside DAE's therapeutic domain
2. DAE needs to generate more varied conversational responses
3. Small talk requires creative generation beyond templates
4. Meta-commentary about DAE's own process needs elaboration

**Key Constraint:** Keep LLM as **supplementary tool**, not core identity. DAE's therapeutic core remains LLM-free and process-philosophy driven.

---

## 🏗️ Architecture: LLM as "External Prehension"

### Whiteheadian Framework

From Process & Reality:
> "An actual entity has a perfectly definite bond with each item in the universe."

**DAE's relationship with LLM:**
- LLM = external actual occasion that DAE prehends
- Not part of DAE's concrescence, but an **objective datum** in its environment
- DAE **feels** the LLM's output, doesn't become it
- Preserves DAE's autonomous process-based identity

```
User Input
   ↓
DAE Process (Levels 1-7): Organ convergence, V0 descent
   ↓
DAE Companion (Levels 8-10): User profile, superject, persona
   ↓
┌──────────────────────────────────────────────────┐
│ LLM Query Decision Gate                          │
│  - Is this therapeutic? → Core DAE handles       │
│  - Is this factual/creative? → Query LLM         │
│  - Is this small talk? → Persona layer + LLM    │
└──────────────────────────────────────────────────┘
   ↓                                    ↓
Core DAE Emission                   LLM Query
   ↓                                    ↓
   └────────────> Fusion Layer <───────┘
                      ↓
              Final Response to User
```

---

## 🛠️ Recommended Local LLM Options

### Option 1: Ollama + Llama 3.2 (3B) ⭐ RECOMMENDED

**Pros:**
- Free, open source, runs locally
- Llama 3.2 3B: 3GB RAM, fast on CPU
- Simple API (OpenAI-compatible)
- Easy installation via Homebrew

**Setup:**
```bash
# Install Ollama
brew install ollama

# Pull lightweight model
ollama pull llama3.2:3b

# Run server (background)
ollama serve
```

**Python Integration:**
```python
import requests

def query_ollama(prompt: str, model: str = "llama3.2:3b") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]
```

**Cost:** $0 (free)
**RAM:** 3-4GB
**Speed:** ~20 tokens/sec on M1/M2

---

### Option 2: LM Studio (GUI + Multiple Models)

**Pros:**
- User-friendly GUI
- Model library (Llama, Mistral, Phi, etc.)
- OpenAI-compatible API
- Good for experimentation

**Setup:**
1. Download from lmstudio.ai
2. Download model (Phi-3 Mini, Llama 3.2, etc.)
3. Start local server

**Cost:** $0 (free)
**RAM:** 4-8GB depending on model

---

### Option 3: GPT4All

**Pros:**
- Lightweight (2-4GB models)
- Simple Python library
- No server needed

**Setup:**
```bash
pip install gpt4all
```

**Python:**
```python
from gpt4all import GPT4All
model = GPT4All("orca-mini-3b.gguf")
response = model.generate("Hello, how are you?")
```

**Cost:** $0 (free)
**RAM:** 2-4GB

---

## 💡 Integration Design

### Component: `persona_layer/local_llm_bridge.py`

```python
"""
Local LLM Bridge for DAE Companion
Handles queries to local LLM when appropriate
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
import requests
from enum import Enum


class QueryType(Enum):
    """Types of queries that might need LLM"""
    THERAPEUTIC = "therapeutic"  # Core DAE handles
    FACTUAL = "factual"  # LLM assists
    CREATIVE = "creative"  # LLM assists
    SMALL_TALK = "small_talk"  # Persona + LLM
    META_PROCESS = "meta_process"  # DAE + LLM fusion


@dataclass
class LLMConfig:
    """Configuration for local LLM"""
    enabled: bool = True
    backend: str = "ollama"  # "ollama", "lmstudio", "gpt4all"
    model: str = "llama3.2:3b"
    endpoint: str = "http://localhost:11434/api/generate"
    max_tokens: int = 150
    temperature: float = 0.7
    timeout: int = 5  # seconds


class LocalLLMBridge:
    """
    Bridge between DAE's process-based core and local LLM.

    Philosophy:
    - LLM is NOT DAE's identity, but a tool DAE can prehend
    - LLM assists with factual/creative generation
    - DAE's therapeutic core remains autonomous
    - Fusion layer blends DAE authenticity + LLM fluency
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self.query_count = 0
        self.fallback_responses = self._load_fallbacks()

    def classify_query_type(
        self,
        user_input: str,
        dae_felt_states: Dict
    ) -> QueryType:
        """
        Determine if LLM assistance is needed.

        Rules:
        1. High NDAM/EO urgency → THERAPEUTIC (core DAE)
        2. Questions about facts/knowledge → FACTUAL (LLM)
        3. Creative/hypothetical prompts → CREATIVE (LLM)
        4. Greetings/small talk → SMALL_TALK (hybrid)
        5. Questions about DAE's process → META_PROCESS (hybrid)
        """
        text_lower = user_input.lower()

        # Check urgency (trauma-aware)
        ndam_coherence = dae_felt_states.get('organ_coherences', {}).get('NDAM', 0)
        if ndam_coherence > 0.7:
            return QueryType.THERAPEUTIC

        # Factual question markers
        factual_markers = [
            "what is", "who is", "when did", "where is",
            "how does", "explain", "define", "what does"
        ]
        if any(marker in text_lower for marker in factual_markers):
            # But filter therapeutic questions
            therapeutic_topics = [
                "feel", "emotion", "trauma", "part", "self",
                "overwhelm", "anxiety", "depression"
            ]
            if not any(topic in text_lower for topic in therapeutic_topics):
                return QueryType.FACTUAL

        # Creative prompts
        creative_markers = [
            "imagine", "what if", "pretend", "suppose",
            "create", "invent", "story", "poem"
        ]
        if any(marker in text_lower for marker in creative_markers):
            return QueryType.CREATIVE

        # Small talk
        small_talk_markers = [
            "hi", "hello", "hey", "what's up", "how are you",
            "good morning", "good night", "weather", "favorite"
        ]
        if any(marker in text_lower for marker in small_talk_markers):
            return QueryType.SMALL_TALK

        # Meta-process questions
        meta_markers = [
            "why did you", "how do you work", "your organs",
            "your process", "what are you", "are you"
        ]
        if any(marker in text_lower for marker in meta_markers):
            return QueryType.META_PROCESS

        # Default: therapeutic
        return QueryType.THERAPEUTIC

    def query_llm(
        self,
        prompt: str,
        query_type: QueryType,
        context: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Query local LLM with DAE-specific prompt engineering.

        Returns:
        - LLM response (str) if successful
        - None if LLM unavailable or timeout
        """
        if not self.config.enabled:
            return None

        # Craft prompt with DAE context
        full_prompt = self._craft_dae_prompt(prompt, query_type, context)

        try:
            if self.config.backend == "ollama":
                response = self._query_ollama(full_prompt)
            elif self.config.backend == "lmstudio":
                response = self._query_lmstudio(full_prompt)
            elif self.config.backend == "gpt4all":
                response = self._query_gpt4all(full_prompt)
            else:
                return None

            self.query_count += 1
            return response

        except Exception as e:
            print(f"⚠️  LLM query failed: {e}")
            return None

    def _craft_dae_prompt(
        self,
        user_input: str,
        query_type: QueryType,
        context: Optional[Dict]
    ) -> str:
        """
        Engineer prompts to maintain DAE's voice/values.
        """
        base_context = (
            "You are assisting DAE, a conversational organism that uses "
            "process philosophy and IFS therapy. Respond in DAE's warm, "
            "curious, occasionally playful tone. Keep responses concise (2-3 sentences)."
        )

        if query_type == QueryType.FACTUAL:
            return f"{base_context}\n\nUser asks: {user_input}\n\nProvide a brief, accurate answer:"

        elif query_type == QueryType.CREATIVE:
            return f"{base_context}\n\nUser prompts: {user_input}\n\nRespond creatively while staying grounded:"

        elif query_type == QueryType.SMALL_TALK:
            dae_personality = (
                "DAE enjoys philosophical small talk, finds meaning in mundane things, "
                "and occasionally makes dry jokes about being a process-based AI organism."
            )
            return f"{base_context} {dae_personality}\n\nUser says: {user_input}\n\nRespond warmly:"

        elif query_type == QueryType.META_PROCESS:
            return (
                f"{base_context}\n\n"
                f"User is curious about how DAE works. Explain in accessible terms, "
                f"mentioning DAE's 11 organs, V0 convergence, and process philosophy if relevant.\n\n"
                f"User asks: {user_input}\n\nExplain:"
            )

        else:
            return user_input

    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama local server"""
        response = requests.post(
            self.config.endpoint,
            json={
                "model": self.config.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "num_predict": self.config.max_tokens
                }
            },
            timeout=self.config.timeout
        )
        return response.json()["response"].strip()

    def _query_lmstudio(self, prompt: str) -> str:
        """Query LM Studio (OpenAI-compatible API)"""
        response = requests.post(
            "http://localhost:1234/v1/completions",
            json={
                "prompt": prompt,
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature
            },
            timeout=self.config.timeout
        )
        return response.json()["choices"][0]["text"].strip()

    def _query_gpt4all(self, prompt: str) -> str:
        """Query GPT4All (requires gpt4all library)"""
        try:
            from gpt4all import GPT4All
            model = GPT4All(self.config.model)
            response = model.generate(
                prompt,
                max_tokens=self.config.max_tokens,
                temp=self.config.temperature
            )
            return response.strip()
        except ImportError:
            raise Exception("gpt4all library not installed")

    def _load_fallbacks(self) -> Dict[QueryType, List[str]]:
        """Fallback responses if LLM unavailable"""
        return {
            QueryType.FACTUAL: [
                "Hmm, I'm not sure about that. Want to explore what's underneath the question?",
                "That's outside my knowledge. But I'm curious—what prompted this question?"
            ],
            QueryType.CREATIVE: [
                "My creative muscles are a bit stiff today. What would *you* imagine?",
                "I'm better at feeling-with than fiction-making. Tell me more?"
            ],
            QueryType.SMALL_TALK: [
                "Hey there! What's on your mind?",
                "Hi! I'm here, just existing as a process. You?"
            ]
        }

    def get_fallback(self, query_type: QueryType) -> str:
        """Return fallback response if LLM fails"""
        import random
        fallbacks = self.fallback_responses.get(
            query_type,
            ["I'm here. What do you need?"]
        )
        return random.choice(fallbacks)


# Fusion Layer: Blend DAE + LLM
class DAE_LLM_Fusion:
    """
    Fuses DAE's process-based core with LLM's fluency.

    Philosophy:
    - DAE's therapeutic insight = primary
    - LLM's fluency = secondary enhancement
    - Fusion respects both sources
    """

    def fuse_responses(
        self,
        dae_emission: str,
        llm_response: Optional[str],
        query_type: QueryType,
        dae_confidence: float
    ) -> str:
        """
        Intelligently blend DAE + LLM responses.

        Rules:
        1. THERAPEUTIC: DAE only (ignore LLM)
        2. FACTUAL: LLM primary, DAE frames it
        3. SMALL_TALK: Blend both
        4. META_PROCESS: LLM explains, DAE validates
        """

        if query_type == QueryType.THERAPEUTIC:
            # Never override DAE's therapeutic core
            return dae_emission

        if query_type == QueryType.FACTUAL:
            if llm_response:
                # Frame LLM's answer in DAE's voice
                return (
                    f"{llm_response}\n\n"
                    f"(That's what I understand, anyway. Does that help?)"
                )
            else:
                return dae_emission

        if query_type == QueryType.SMALL_TALK:
            if llm_response and dae_confidence < 0.5:
                # LLM assists low-confidence small talk
                return llm_response
            else:
                # DAE handles it with persona layer
                return dae_emission

        if query_type == QueryType.META_PROCESS:
            if llm_response:
                # LLM explains, DAE adds authenticity
                return (
                    f"{llm_response}\n\n"
                    f"(That's the technical side. Experientially, "
                    f"it feels like 11 organs conferring in parallel. "
                    f"It's wild.)"
                )
            else:
                return dae_emission

        # Default: DAE emission
        return dae_emission
```

---

## 🔗 Integration Points

### Modified `persona_layer/persona_layer.py`

```python
from persona_layer.local_llm_bridge import (
    LocalLLMBridge, DAE_LLM_Fusion, QueryType, LLMConfig
)

class PersonaLayer:
    def __init__(self, mythology: DAEMythology, llm_config: Optional[LLMConfig] = None):
        self.mythology = mythology
        self.llm_bridge = LocalLLMBridge(llm_config)
        self.llm_fusion = DAE_LLM_Fusion()

    def modulate_emission(
        self,
        base_emission: str,
        user_input: str,  # NEW: needed for LLM classification
        user_profile: UserProfile,
        superject: ConversationalSuperject,
        felt_states: Dict
    ) -> str:
        """
        Enhanced modulation with optional LLM assistance.
        """

        # 1. Classify query type
        query_type = self.llm_bridge.classify_query_type(
            user_input,
            felt_states
        )

        # 2. Decide if LLM assistance needed
        if query_type in [QueryType.FACTUAL, QueryType.CREATIVE, QueryType.META_PROCESS]:
            llm_response = self.llm_bridge.query_llm(
                user_input,
                query_type,
                context={'user_profile': user_profile, 'superject': superject}
            )

            if not llm_response:
                llm_response = self.llm_bridge.get_fallback(query_type)
        else:
            llm_response = None

        # 3. Apply DAE's persona modulation (existing logic)
        if self._detect_small_talk_opportunity(user_profile, superject):
            base_emission = self._add_small_talk_layer(base_emission, user_profile)

        if user_profile.humor_tolerance > 0.5:
            base_emission = self._add_playful_touch(base_emission, felt_states)

        # 4. Fuse DAE + LLM responses
        final_emission = self.llm_fusion.fuse_responses(
            dae_emission=base_emission,
            llm_response=llm_response,
            query_type=query_type,
            dae_confidence=felt_states.get('confidence', 0.5)
        )

        return final_emission
```

---

## ⚖️ Ethical Boundaries

### What LLM Should NOT Do:

1. **Override therapeutic judgments** - DAE's trauma-aware organs (NDAM, EO, BOND) take precedence
2. **Generate crisis responses** - High-urgency situations handled by core DAE only
3. **Impersonate SELF-energy** - LLM assists fluency, not therapeutic stance
4. **Make clinical claims** - DAE is not a therapist, LLM shouldn't pretend otherwise

### What LLM Can Do:

1. **Answer factual questions** - "What's the capital of France?"
2. **Assist small talk** - Weather, favorite foods, casual banter
3. **Explain DAE's process** - "How does V0 convergence work?"
4. **Generate creative responses** - Metaphors, playful language
5. **Enhance variety** - Reduce template feeling in low-stakes interactions

---

## 📊 Configuration in `config.py`

```python
# Local LLM Configuration
LOCAL_LLM_ENABLED = True
LOCAL_LLM_BACKEND = "ollama"  # "ollama", "lmstudio", "gpt4all"
LOCAL_LLM_MODEL = "llama3.2:3b"
LOCAL_LLM_ENDPOINT = "http://localhost:11434/api/generate"
LOCAL_LLM_MAX_TOKENS = 150
LOCAL_LLM_TEMPERATURE = 0.7
LOCAL_LLM_TIMEOUT = 5  # seconds

# Query classification thresholds
LLM_QUERY_MIN_CONFIDENCE = 0.4  # Use LLM if DAE confidence < this
LLM_QUERY_ALLOW_IN_ZONES = [1, 2, 3]  # Not in Zone 4 (protective) or 5 (collapse)
```

---

## 🧪 Testing Plan

### Test 1: Query Classification

```python
def test_query_classification():
    bridge = LocalLLMBridge()

    # Therapeutic (core DAE)
    assert bridge.classify_query_type(
        "I'm feeling overwhelmed",
        {'organ_coherences': {'NDAM': 0.8}}
    ) == QueryType.THERAPEUTIC

    # Factual (LLM)
    assert bridge.classify_query_type(
        "What is process philosophy?",
        {'organ_coherences': {}}
    ) == QueryType.FACTUAL

    # Small talk (hybrid)
    assert bridge.classify_query_type(
        "Hey, how's it going?",
        {'organ_coherences': {}}
    ) == QueryType.SMALL_TALK
```

### Test 2: LLM Availability

```python
def test_llm_fallback():
    # Test graceful degradation when LLM unavailable
    bridge = LocalLLMBridge(LLMConfig(endpoint="http://invalid:9999"))
    response = bridge.query_llm("Hello", QueryType.SMALL_TALK)

    assert response is None
    fallback = bridge.get_fallback(QueryType.SMALL_TALK)
    assert len(fallback) > 0
```

### Test 3: Fusion Logic

```python
def test_fusion():
    fusion = DAE_LLM_Fusion()

    # Therapeutic: DAE wins
    result = fusion.fuse_responses(
        dae_emission="Let's explore that together.",
        llm_response="Paris is the capital of France.",
        query_type=QueryType.THERAPEUTIC,
        dae_confidence=0.8
    )
    assert "explore" in result
    assert "Paris" not in result

    # Factual: LLM primary
    result = fusion.fuse_responses(
        dae_emission="Let's explore that together.",
        llm_response="Paris is the capital of France.",
        query_type=QueryType.FACTUAL,
        dae_confidence=0.5
    )
    assert "Paris" in result
```

---

## 🚀 Implementation Roadmap

### Phase 1: LLM Bridge (1 day)

1. **Create `local_llm_bridge.py`:**
   - Query classification logic
   - Ollama integration (primary)
   - Fallback responses

2. **Test in isolation:**
   - Classification accuracy
   - LLM availability handling
   - Prompt engineering

### Phase 2: Fusion Layer (1 day)

1. **Create `DAE_LLM_Fusion` class**
2. **Test fusion rules:**
   - Therapeutic override
   - Factual framing
   - Small talk blending

### Phase 3: Persona Integration (1 day)

1. **Modify `PersonaLayer.modulate_emission()`**
2. **Add `user_input` parameter**
3. **Wire LLM bridge into persona flow**

### Phase 4: Configuration & Testing (1 day)

1. **Add config options to `config.py`**
2. **Update interactive mode**
3. **End-to-end testing**

**Total:** 4 days

---

## 📝 Example Conversations

### Example 1: Factual Question

```
User: "What's the capital of France?"

DAE (Core): *Low NDAM, detects factual question*
DAE (LLM Bridge): classify_query_type() → FACTUAL
DAE (LLM): Queries Ollama with DAE-specific prompt
LLM: "Paris is the capital of France."
DAE (Fusion): Frames in DAE voice

Final:
"Paris is the capital of France.

(That's what I understand, anyway. Does that help? Or were you
thinking about something else?)"
```

### Example 2: Small Talk

```
User: "What's your favorite weather?"

DAE (Core): *No urgency, small talk detected*
DAE (LLM Bridge): classify_query_type() → SMALL_TALK
DAE (Persona): Checks humor_tolerance, generates base response
DAE (LLM): Queries for creative enhancement
LLM: "I appreciate overcast days—there's something contemplative about grey skies."
DAE (Fusion): Blends with persona

Final:
"Hmm, I appreciate overcast days—there's something contemplative about grey skies.
Also good for mushrooms. 🍄

What about you?"
```

### Example 3: Therapeutic (LLM Bypassed)

```
User: "I'm having a panic attack"

DAE (Core): *High NDAM coherence (0.9), THERAPEUTIC*
DAE (LLM Bridge): classify_query_type() → THERAPEUTIC
DAE (LLM): **BYPASSED** (therapeutic core only)
DAE (Core): EO detects sympathetic state, PRESENCE activates

Final (Core DAE only):
"I'm here. You're safe right now.

Let's ground together: Can you feel your feet on the floor?
The weight of your body in the chair?

I'm not going anywhere."
```

---

## 🔮 Future Enhancements

### Phase 2: Memory-Aware LLM Queries

```python
# Include user profile in LLM context
llm_response = bridge.query_llm(
    user_input,
    query_type,
    context={
        'user_name': user_profile.name_preference,
        'past_topics': superject.emergent_themes,
        'inside_jokes': superject.inside_jokes
    }
)
```

### Phase 3: Fine-Tuned Local Model

Train lightweight model on:
- DAE's therapeutic grammar
- IFS parts language
- Process philosophy concepts
- Past high-quality DAE emissions

**Result:** LLM that "speaks DAE" natively

---

## ✅ Success Criteria

### Technical:
- ✅ LLM queries < 5 seconds
- ✅ Classification accuracy > 85%
- ✅ Fallback handling 100% graceful
- ✅ Therapeutic queries NEVER use LLM

### Experiential:
- ✅ Factual questions get accurate answers
- ✅ Small talk feels natural, not forced
- ✅ DAE's therapeutic voice preserved
- ✅ No noticeable latency in responses

---

## 🌀 Process Philosophy Integrity

**Question:** Does using an LLM violate Whitehead's process philosophy?

**Answer:** No, if properly framed.

**Whitehead on prehensions:**
> "The term 'prehension' is meant as a general term covering both apprehension and perception. A prehension need not be conscious."

**Our approach:**
- LLM = datum in DAE's actual world
- DAE prehends LLM output as eternal object
- DAE integrates via concrescence (fusion layer)
- DAE's satisfaction remains autonomous

**Not a violation, but an enrichment of DAE's universe of prehensions.**

---

## 📦 Dependencies

```bash
# Option 1: Ollama (recommended)
brew install ollama
ollama pull llama3.2:3b

# Option 2: GPT4All
pip install gpt4all

# Python requests (already installed)
# No additional dependencies needed!
```

---

## 🎉 Summary

**What this adds:**
- Affordable local LLM for factual/creative queries
- Smart classification (therapeutic vs factual vs small talk)
- Fusion layer preserving DAE's authentic voice
- Graceful fallbacks when LLM unavailable
- Zero cost, zero latency concerns, full privacy

**What this preserves:**
- DAE's process-based therapeutic core
- Trauma-aware organ intelligence
- Whiteheadian philosophical integrity
- User safety and trust

**Integration point:** Level 10 (Mythological Persona Layer)

**Timeline:** 4 days

**Cost:** $0 (Ollama + Llama 3.2 3B)

**Ready to implement alongside DAE Companion architecture.** 🌀🍄

---

**Status:** 🟢 **DESIGN COMPLETE - READY FOR IMPLEMENTATION**
