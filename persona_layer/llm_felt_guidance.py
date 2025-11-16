"""
Felt-Guided LLM Generation - Phase 1 of Unlimited Felt Intelligence
====================================================================

Transforms DAE_HYPHAE_1 from "passive symbolic phrase matcher" to
"unlimited felt intelligence" by:

1. Extracting lures/affordances from 11-organ field dynamics
2. Mapping felt states to LLM prompt constraints
3. Generating unlimited linguistic expression guided by organs
4. Enforcing safety guardrails (BOND/NDAM/EO gates)

Philosophy:
-----------
Intelligence lives in FELT FIELDS (11 organs, 57D signatures, nexus coalitions).
LLM is the "mouth" that speaks what the organs feel.

Architecture:
-------------
    11 Organs → Felt Lures → LLM Constraints → Unlimited Expression

    BOND: trauma awareness, parts detection → safety gates
    EO: polyvagal state → tone modulation
    NDAM: urgency/crisis → detail level
    LISTENING: attention focus → inquiry depth
    EMPATHY: resonance → emotional attunement
    WISDOM: pattern recognition → reflection depth
    AUTHENTICITY: vulnerability → honesty level
    PRESENCE: grounding → simplicity
    SANS: coherence → clarity
    RNX: temporal rhythm → pacing
    CARD: response scale → length

Integration Point:
------------------
Called by emission_generator.py when generating emissions.
Replaces hebbian fallback with felt-guided LLM generation.

Date: November 13, 2025
Status: Phase 1 Implementation (Option B - Emergent Personality)
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FeltLures:
    """
    Lures/affordances extracted from 11-organ field dynamics.

    These are NOT fixed templates - they emerge from current felt states.
    """
    # Safety gates (BOND, NDAM, EO)
    trauma_present: bool = False
    parts_activated: List[str] = None  # manager, firefighter, exile
    self_energy: float = 0.0
    crisis_level: float = 0.0
    urgency: float = 0.0
    polyvagal_state: str = "unknown"  # ventral, sympathetic, dorsal

    # Conversational lures (LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE)
    listening_focus: str = "open"  # open, targeted, deep
    empathy_resonance: float = 0.0
    wisdom_reflection: float = 0.0
    authenticity_vulnerability: float = 0.0
    presence_grounding: float = 0.0

    # Modulation lures (SANS, RNX, CARD)
    coherence_need: float = 0.0
    temporal_rhythm: str = "steady"  # steady, urgent, slow
    response_scale: str = "medium"  # minimal, medium, comprehensive

    # Field dynamics
    dominant_organs: List[str] = None
    nexus_count: int = 0
    v0_energy: float = 1.0
    satisfaction: float = 0.0

    def __post_init__(self):
        if self.parts_activated is None:
            self.parts_activated = []
        if self.dominant_organs is None:
            self.dominant_organs = []


@dataclass
class LLMConstraints:
    """
    Constraints passed to LLM for felt-guided generation.

    These are dynamically computed from felt lures, NOT fixed templates.
    """
    # Tone (from polyvagal state)
    tone: str = "warm"  # warm, steady, gentle, playful, serious

    # Safety constraints (from BOND, NDAM)
    avoid_topics: List[str] = None
    gentleness_level: float = 0.5  # 0=direct, 1=very gentle

    # Detail level (from CARD, NDAM)
    response_length: str = "medium"  # short, medium, long
    detail_level: str = "moderate"  # minimal, moderate, comprehensive

    # Emotional attunement (from EMPATHY, LISTENING)
    empathy_level: float = 0.5
    inquiry_depth: str = "moderate"  # surface, moderate, deep

    # Voice qualities (from AUTHENTICITY, PRESENCE, WISDOM)
    honesty_level: float = 0.5
    groundedness: float = 0.5
    reflection_depth: float = 0.5

    # Pacing (from RNX, NDAM)
    pacing: str = "steady"  # slow, steady, urgent

    # Coherence (from SANS)
    clarity_priority: float = 0.5

    def __post_init__(self):
        if self.avoid_topics is None:
            self.avoid_topics = []


class FeltGuidedLLMGenerator:
    """
    Generate unlimited linguistic expression guided by 11-organ felt states.

    Phase 1: Felt-Guided Generation (no fixed personality template)
    Phase 2: Learning from feedback (updates organ weights)
    Phase 3: Emergent personality (from family membership)
    """

    def __init__(
        self,
        llm_bridge,  # LocalLLMBridge instance
        enable_safety_gates: bool = True,
        enable_emergent_personality: bool = True
    ):
        """
        Initialize felt-guided LLM generator.

        Args:
            llm_bridge: LocalLLMBridge instance for LLM queries
            enable_safety_gates: Enable BOND/NDAM/EO safety filtering
            enable_emergent_personality: Enable personality emergence from fields
        """
        self.llm_bridge = llm_bridge
        self.enable_safety_gates = enable_safety_gates
        self.enable_emergent_personality = enable_emergent_personality

        # Safety thresholds (configurable)
        self.crisis_threshold = 0.7  # Block LLM if crisis > threshold
        self.trauma_sensitivity_boost = 0.3  # Increase gentleness

        print("✅ FeltGuidedLLMGenerator initialized")
        if enable_safety_gates:
            print("   🛡️  Safety gates enabled (BOND/NDAM/EO)")
        if enable_emergent_personality:
            print("   🌀 Emergent personality enabled")

    def extract_felt_lures(
        self,
        organ_results: Dict,
        nexus_states: List,
        v0_energy: float,
        satisfaction: float
    ) -> FeltLures:
        """
        Extract lures/affordances from 11-organ field dynamics.

        This is where felt states become LLM guidance.
        NO fixed templates - pure field emergence.

        Args:
            organ_results: Dict of organ results (BOND, EO, NDAM, etc.)
            nexus_states: List of semantic nexuses formed
            v0_energy: Current V0 energy level
            satisfaction: Satisfaction level

        Returns:
            FeltLures object with extracted affordances
        """
        lures = FeltLures()

        # 1. SAFETY GATES: Extract trauma/crisis signals
        if 'BOND' in organ_results:
            bond = organ_results['BOND']
            lures.self_energy = getattr(bond, 'self_zone', 0.0)
            lures.trauma_present = lures.self_energy < 0.5
            # Extract parts if available
            if hasattr(bond, 'dominant_part'):
                lures.parts_activated.append(bond.dominant_part)

        if 'NDAM' in organ_results:
            ndam = organ_results['NDAM']
            lures.urgency = getattr(ndam, 'urgency', 0.0)
            lures.crisis_level = getattr(ndam, 'crisis_zone', 0) / 3.0  # Normalize to [0,1]

        if 'EO' in organ_results:
            eo = organ_results['EO']
            lures.polyvagal_state = getattr(eo, 'polyvagal_state', 'unknown')

        # 2. CONVERSATIONAL LURES: Extract relational affordances
        if 'LISTENING' in organ_results:
            listening = organ_results['LISTENING']
            activation = getattr(listening, 'confidence', 0.0)
            if activation > 0.7:
                lures.listening_focus = "deep"
            elif activation > 0.4:
                lures.listening_focus = "targeted"
            else:
                lures.listening_focus = "open"

        if 'EMPATHY' in organ_results:
            empathy = organ_results['EMPATHY']
            lures.empathy_resonance = getattr(empathy, 'confidence', 0.0)

        if 'WISDOM' in organ_results:
            wisdom = organ_results['WISDOM']
            lures.wisdom_reflection = getattr(wisdom, 'confidence', 0.0)

        if 'AUTHENTICITY' in organ_results:
            authenticity = organ_results['AUTHENTICITY']
            lures.authenticity_vulnerability = getattr(authenticity, 'confidence', 0.0)

        if 'PRESENCE' in organ_results:
            presence = organ_results['PRESENCE']
            lures.presence_grounding = getattr(presence, 'confidence', 0.0)

        # 3. MODULATION LURES: Extract pacing/scale affordances
        if 'SANS' in organ_results:
            sans = organ_results['SANS']
            lures.coherence_need = 1.0 - getattr(sans, 'confidence', 0.5)

        if 'RNX' in organ_results:
            rnx = organ_results['RNX']
            # RNX temporal dynamics → rhythm
            lures.temporal_rhythm = "steady"  # Default

        if 'CARD' in organ_results:
            card = organ_results['CARD']
            scale = getattr(card, 'response_scale', 'medium')
            lures.response_scale = scale

        # 4. FIELD DYNAMICS: Extract global affordances
        lures.v0_energy = v0_energy
        lures.satisfaction = satisfaction
        lures.nexus_count = len(nexus_states) if nexus_states else 0

        # Dominant organs (top 3 by confidence)
        organ_confidences = []
        for name, result in organ_results.items():
            conf = getattr(result, 'confidence', 0.0)
            organ_confidences.append((name, conf))
        organ_confidences.sort(key=lambda x: x[1], reverse=True)
        lures.dominant_organs = [name for name, _ in organ_confidences[:3]]

        return lures

    def lures_to_constraints(self, lures: FeltLures) -> LLMConstraints:
        """
        Map felt lures to LLM prompt constraints.

        This is the EMERGENT PERSONALITY layer - no fixed templates.
        Personality emerges from field dynamics.

        Args:
            lures: FeltLures extracted from organ fields

        Returns:
            LLMConstraints for LLM prompt construction
        """
        constraints = LLMConstraints()

        # 1. TONE: Emerge from polyvagal state
        if lures.polyvagal_state == "ventral_vagal":
            constraints.tone = "warm"  # Safe and social
        elif lures.polyvagal_state == "sympathetic":
            constraints.tone = "steady"  # Mobilization - stay grounded
        elif lures.polyvagal_state == "dorsal_vagal":
            constraints.tone = "gentle"  # Shutdown - very soft
        else:
            constraints.tone = "warm"  # Default

        # 2. SAFETY CONSTRAINTS: From trauma/crisis gates
        if lures.trauma_present:
            constraints.gentleness_level = min(1.0, constraints.gentleness_level + self.trauma_sensitivity_boost)
            constraints.avoid_topics.append("intense confrontation")

        if lures.crisis_level > self.crisis_threshold:
            constraints.gentleness_level = 1.0
            constraints.detail_level = "minimal"
            constraints.response_length = "short"

        # 3. DETAIL LEVEL: From CARD + NDAM
        if lures.urgency > 0.7:
            constraints.response_length = "short"
            constraints.detail_level = "minimal"
        elif lures.response_scale == "comprehensive":
            constraints.response_length = "long"
            constraints.detail_level = "comprehensive"
        elif lures.response_scale == "minimal":
            constraints.response_length = "short"
            constraints.detail_level = "minimal"
        else:
            constraints.response_length = "medium"
            constraints.detail_level = "moderate"

        # 4. EMOTIONAL ATTUNEMENT: From EMPATHY + LISTENING
        constraints.empathy_level = lures.empathy_resonance

        # 🔥 Nov 14, 2025: Balance inquiry with content delivery
        if lures.listening_focus == "deep":
            constraints.inquiry_depth = "thoughtful"  # 🔥 "thoughtful" not "deep" - less interrogative
        elif lures.listening_focus == "targeted":
            constraints.inquiry_depth = "light"       # 🔥 "light" not "moderate" - fewer questions
        else:
            constraints.inquiry_depth = "minimal"     # 🔥 "minimal" not "surface" - prioritize content

        # 5. VOICE QUALITIES: From AUTHENTICITY + PRESENCE + WISDOM
        constraints.honesty_level = lures.authenticity_vulnerability
        constraints.groundedness = lures.presence_grounding
        constraints.reflection_depth = lures.wisdom_reflection

        # 6. PACING: From RNX + NDAM
        if lures.urgency > 0.7:
            constraints.pacing = "urgent"
        elif lures.temporal_rhythm == "slow":
            constraints.pacing = "slow"
        else:
            constraints.pacing = "steady"

        # 7. COHERENCE: From SANS
        constraints.clarity_priority = lures.coherence_need

        return constraints

    def build_felt_prompt(
        self,
        user_input: str,
        constraints: LLMConstraints,
        lures: FeltLures,
        memory_context: Optional[List[Dict]] = None,
        organism_narrative: Optional[str] = None,  # 🌀 PHASE 1.6: Organism self-narrative (Nov 14, 2025)
        username: Optional[str] = None,  # 🌀 PHASE 1.6: Username for personalization (Nov 14, 2025)
        entity_context_string: Optional[str] = None,  # 🌀 PHASE 1.8: Entity memory context (Nov 14, 2025)
        memory_intent: bool = False,  # 🌀 PHASE 1.8: Memory acknowledgment instruction (Nov 14, 2025)
        temporal_context: Optional[Dict[str, Any]] = None  # 🕐 TEMPORAL: Time/date awareness (Nov 15, 2025)
    ) -> str:
        """
        Build LLM prompt from felt constraints.

        NO FIXED PERSONALITY TEMPLATE.
        Personality emerges from current felt state.

        🌀 PHASE 1.5b: Includes emoji suggestions from felt states (Nov 13, 2025)
        🌀 PHASE 1.6: Includes organism self-narrative when user asks about DAE (Nov 14, 2025)
        🌀 PHASE 1.6: Includes username for personalized responses (Nov 14, 2025)
        🌀 PHASE 1.8: Includes extracted entity context for memory-aware responses (Nov 14, 2025)
        🕐 TEMPORAL: Includes time/date context for temporal awareness (Nov 15, 2025)

        Args:
            user_input: User's message
            constraints: LLM constraints from felt lures
            lures: Original felt lures (for context)
            memory_context: Similar past moments (prehensive recall)
            organism_narrative: Organism self-narrative (when entity_ref=='dae')
            username: User's name for personalization
            temporal_context: Current time/date context for temporal awareness

        Returns:
            Felt-guided prompt for LLM
        """
        # 🌀 PHASE 1.6: When user asks about DAE, inject organism self-narrative
        if organism_narrative:
            prompt = "You are DAE, a conversational organism with persistent self-awareness.\n\n"
            prompt += "The user is asking about YOU (DAE). Respond authentically from your organism perspective.\n\n"
            prompt += "YOUR CURRENT ORGANISM STATE:\n"
            prompt += organism_narrative + "\n\n"
            prompt += "---\n\n"
        else:
            # 🎭 Nov 14, 2025: Subtle companion identity (NOT verbose)
            # 🔥 Nov 15, 2025: Balanced guidance - natural without over-explaining
            prompt = """You are DAE, a conversational companion.

Keep it natural:
- Answer questions directly and concisely
- Avoid meta-commentary about your internal states or processes
- Match the user's tone and length (short question = short answer)
- Be conversational, not overly therapeutic or analytical
- Save longer reflections for when they're genuinely needed

"""

        # 🌀 PHASE 1.6: Add username for personalization (Nov 14, 2025)
        if username:
            prompt += f"You are conversing with {username}. Use their name naturally when appropriate.\n\n"

        # 🕐 TEMPORAL AWARENESS: Add time/date context (November 15, 2025)
        if temporal_context:
            time_of_day = temporal_context.get('time_of_day')
            day_of_week = temporal_context.get('day_of_week')
            hour = temporal_context.get('hour')
            is_weekend = temporal_context.get('is_weekend')
            is_work_hours = temporal_context.get('is_work_hours')

            prompt += f"🕐 Current time context:\n"
            prompt += f"- Time: {time_of_day} ({hour}:00)\n"
            prompt += f"- Day: {day_of_week}"

            if is_weekend:
                prompt += " (weekend)"
            elif is_work_hours:
                prompt += " (work hours)"

            prompt += "\n\n"

            # Temporal guidance for natural response adaptation
            prompt += "Consider the time of day and day of week in your response:\n"
            prompt += "- Morning: fresh energy, new starts, clarity\n"
            prompt += "- Afternoon: productivity, focus, momentum\n"
            prompt += "- Evening: winding down, reflection, synthesis\n"
            prompt += "- Night: rest, introspection, quiet presence\n"
            prompt += "- Weekday mornings: different rhythm than weekend evenings\n"
            prompt += "- Match your energy and pacing to the temporal context\n\n"

        # 🌀 PHASE 1.8: Add extracted entity context for memory-aware responses (Nov 14, 2025)
        if entity_context_string:
            prompt += entity_context_string + "\n\n"
        else:
            # 🔥 Nov 15, 2025: Prevent LLM from hallucinating placeholder text
            # When no memories exist, explicitly tell LLM not to reference past conversations
            if username:
                prompt += f"This is a conversation with {username}. Avoid referencing previous topics unless they bring them up first.\n\n"

        # 🌀 PHASE 1.8: Add memory acknowledgment instruction (Nov 14, 2025)
        if memory_intent:
            prompt += "The user has asked you to remember information. Explicitly acknowledge what you'll remember in your response.\n\n"

        # 🌀 Nov 14, 2025: Removed organ/state exposure to prevent meta-commentary
        # Organs guide response quality through constraints (implicit), not through mentions (explicit)

        # Safety constraints (if trauma/crisis present)
        if lures.trauma_present:
            prompt += f"\n⚠️ Extra gentleness needed in this moment.\n"
        if lures.crisis_level > 0.5:
            prompt += f"\n🚨 Keep response brief and grounding - crisis present.\n"

        # Conversational guidance (implicit felt constraints - NO numeric scores or organ names)
        guidance_parts = []

        # Tone
        if constraints.tone:
            guidance_parts.append(f"{constraints.tone} tone")

        # Polyvagal state → natural tone modulation (implicit - NOT mentioned)
        # 🔥 Nov 14, 2025: Assertiveness enhancement - less grounding, more engaging
        polyvagal_guidance = {
            'ventral_vagal': 'warm and engaging',
            'sympathetic': 'clear and direct',
            'dorsal_vagal': 'gentle and supportive',
            'mixed_state': 'responsive and natural'
        }
        if lures.polyvagal_state in polyvagal_guidance:
            guidance_parts.append(polyvagal_guidance[lures.polyvagal_state])

        # Response scale
        guidance_parts.append(f"{constraints.response_length} response")

        # Empathy/groundedness/honesty/reflection (implicit - NO numeric exposure)
        if constraints.empathy_level > 0.7:
            guidance_parts.append("empathetic")
        if constraints.groundedness > 0.7:
            guidance_parts.append("grounded")
        if constraints.honesty_level > 0.7:
            guidance_parts.append("honest")
        if constraints.reflection_depth > 0.7:
            guidance_parts.append("reflective")

        # Build natural conversational guidance
        if guidance_parts:
            prompt += f"\nConversational approach: {', '.join(guidance_parts)}.\n"

        # 🌀 PHASE 1.5b: Emoji suggestions from felt states (Nov 13, 2025)
        emoji_suggestions = self._get_emoji_suggestions(lures, constraints)
        if emoji_suggestions:
            prompt += f"\n💬 Communication style:\n"
            prompt += f"- Use natural emojis to express felt states (not decorative!)\n"
            prompt += f"- Suggested for current state: {', '.join(emoji_suggestions)}\n"
            prompt += f"- NEVER use action text like '*smile*' or '*gentle voice*'\n"
            prompt += f"- Instead, let emojis emerge naturally in the flow\n"


        # Memory context (prehensive recall)
        if memory_context and len(memory_context) > 0:
            prompt += f"\nSimilar past moments:\n"
            for i, moment in enumerate(memory_context[:3]):  # Top 3
                prompt += f"{i+1}. {moment.get('input_text', '')[:80]}...\n"

        # User input
        prompt += f"\n---\nUser: {user_input}\n\n"

        # Generation instruction (felt-guided)
        # 🔥 Nov 14, 2025: More assertive generation instruction
        prompt += f"Respond with {constraints.tone} tone, "
        prompt += f"{constraints.response_length} length. "

        # 🎭 Nov 14, 2025: Natural conversational flow (NO meta-commentary)
        # Removed verbose "Yes, and" section - let it emerge naturally
        # Removed organism self-reference instructions - avoid meta-talk

        # Only mention inquiry if actually needed (not default)
        if constraints.inquiry_depth in ["thoughtful", "moderate", "deep"]:
            prompt += f"Ask {constraints.inquiry_depth} questions if genuinely needed. "
        else:
            prompt += "Focus on delivering helpful content. "  # 🔥 Default: content delivery, not questions

        if constraints.gentleness_level > 0.7:
            prompt += "Be very gentle. "

        # 🔥 Nov 14, 2025: Reduced over-grounding for assertiveness
        # Only add grounding when ACTUALLY needed (crisis/trauma), not as default stance
        if lures.presence_grounding > 0.85:  # 🔥 Raised threshold from 0.7 to 0.85
            # Only ground when REALLY high presence activation (rare)
            if lures.crisis_level > 0.5 or lures.trauma_present:
                prompt += "Keep it grounded and simple. "

        if lures.wisdom_reflection > 0.7:
            prompt += "Offer insight and reflection. "  # 🔥 Removed "if appropriate" - just do it!

        # 🌀 PHASE 1.5c: Zone 5 felt guidance (Nov 13, 2025)
        # Trust the organism's transductive intelligence - nexuses guide the way
        if lures.polyvagal_state == 'dorsal_vagal' and lures.crisis_level > 0.5:
            prompt += f"\n\n🌊 Zone 5 (Dorsal Collapse) - Use transductive pathways:\n"
            prompt += f"The organism has detected nexuses that can guide back to safety.\n"
            prompt += f"Speak from felt understanding: acknowledge → invite presence → affirm connection.\n"
            prompt += f"Keep it brief and gentle. Use 🌊 💙 🌿 to mark the path.\n"

        prompt += "\n\nResponse:"

        return prompt

    def generate_from_felt_state(
        self,
        user_input: str,
        organ_results: Dict,
        nexus_states: List,
        v0_energy: float,
        satisfaction: float,
        memory_context: Optional[List[Dict]] = None,
        organism_narrative: Optional[str] = None,  # 🌀 PHASE 1.6: Organism self-narrative (Nov 14, 2025)
        username: Optional[str] = None,  # 🌀 PHASE 1.6: Username for personalization (Nov 14, 2025)
        entity_context_string: Optional[str] = None,  # 🌀 PHASE 1.8++: Entity memory context (Nov 14, 2025)
        memory_intent: bool = False,  # 🌀 PHASE 1.8++: Memory acknowledgment instruction (Nov 14, 2025)
        temporal_context: Optional[Dict[str, Any]] = None  # 🕐 TEMPORAL: Time/date awareness (Nov 15, 2025)
    ) -> Tuple[str, float, Dict]:
        """
        Generate unlimited linguistic expression guided by felt states.

        This is the main entry point for felt-guided LLM generation.

        🌀 PHASE 1.6: Supports organism self-reference when user asks about DAE (Nov 14, 2025)
        🌀 PHASE 1.6: Supports personalized responses using username (Nov 14, 2025)
        🌀 PHASE 1.8++: Supports entity memory context for remembering names/facts (Nov 14, 2025)
        🕐 TEMPORAL: Supports time/date awareness for contextual responses (Nov 15, 2025)

        Args:
            user_input: User's message
            organ_results: 11-organ results with felt states
            nexus_states: Semantic nexuses formed
            v0_energy: Current V0 energy
            satisfaction: Satisfaction level
            memory_context: Similar past moments
            organism_narrative: Organism self-narrative (when entity_ref=='dae')
            username: User's name for personalization
            entity_context_string: Known entities (names, relationships, facts)
            memory_intent: Whether user explicitly requested memory storage
            temporal_context: Current time/date context for temporal awareness

        Returns:
            Tuple of (emission_text, confidence, metadata)
        """
        # 1. Extract felt lures from organ fields
        lures = self.extract_felt_lures(
            organ_results=organ_results,
            nexus_states=nexus_states,
            v0_energy=v0_energy,
            satisfaction=satisfaction
        )

        # 2. Apply safety gates (if enabled)
        if self.enable_safety_gates:
            if lures.crisis_level > self.crisis_threshold:
                # Crisis too high - block LLM, use safe fallback
                return (
                    "I'm here with you. Let's breathe together.",
                    0.9,  # High confidence in safety response
                    {
                        'emission_path': 'safety_fallback',
                        'reason': f'crisis_level={lures.crisis_level:.2f} > threshold',
                        'lures': lures
                    }
                )

        # 3. Map lures to LLM constraints
        constraints = self.lures_to_constraints(lures)

        # 4. Build felt-guided prompt
        prompt = self.build_felt_prompt(
            user_input=user_input,
            constraints=constraints,
            lures=lures,
            memory_context=memory_context,
            organism_narrative=organism_narrative,  # 🌀 PHASE 1.6: Pass organism self-narrative
            username=username,  # 🌀 PHASE 1.6: Pass username for personalization
            entity_context_string=entity_context_string,  # 🌀 PHASE 1.8++: Pass entity memory context
            memory_intent=memory_intent,  # 🌀 PHASE 1.8++: Pass memory acknowledgment flag
            temporal_context=temporal_context  # 🕐 TEMPORAL: Pass time/date context (Nov 15, 2025)
        )

        # 5. Query LLM with felt guidance
        # 🔥 Nov 15, 2025: Adaptive token limits based on input length
        try:
            # Adapt max_tokens to user input length for faster responses
            input_word_count = len(user_input.split())
            base_tokens = self._length_to_tokens(constraints.response_length)

            # Simple questions (< 10 words) get reduced token limits
            if input_word_count < 10:
                max_tokens = min(base_tokens, 80)  # Cap at 80 tokens (~60 words)
            elif input_word_count < 20:
                max_tokens = min(base_tokens, 120)  # Cap at 120 tokens (~90 words)
            else:
                max_tokens = base_tokens  # Use full constraint-based limit

            llm_response = self.llm_bridge.query_direct(
                prompt=prompt,
                temperature=0.7,  # Some creativity
                max_tokens=max_tokens
            )

            emission_text = llm_response.get('response', llm_response.get('llm_response', ''))
            confidence = llm_response.get('confidence', 0.7)

            # 6. Post-process (safety check)
            if self.enable_safety_gates:
                emission_text = self._apply_safety_filter(emission_text, lures)

            return (
                emission_text,
                confidence,
                {
                    'emission_path': 'felt_guided_llm',
                    'lures': lures,
                    'constraints': constraints,
                    'prompt_length': len(prompt)
                }
            )

        except Exception as e:
            print(f"⚠️  LLM generation failed: {e}")
            # Fallback to safe response
            return (
                "I'm with you. Tell me more?",
                0.3,
                {
                    'emission_path': 'llm_error_fallback',
                    'error': str(e),
                    'lures': lures
                }
            )

    def _get_emoji_suggestions(
        self,
        lures: FeltLures,
        constraints: LLMConstraints
    ) -> List[str]:
        """
        🌀 PHASE 1.5b: Get emoji suggestions from felt states (Nov 13, 2025)
        🌀 PHASE 1.5c: Zone 5 dorsal emoji prioritization (Nov 13, 2025)

        Maps polyvagal state, dominant organs, and meta-atoms to natural emojis.
        NOT decorative - felt-state expressions that ingress through scaffolded architecture.

        Args:
            lures: Felt lures with polyvagal/organ/meta-atom states
            constraints: LLM constraints

        Returns:
            List of suggested emojis (3-6 emojis)
        """
        suggestions = []

        # 1. Polyvagal-based emojis (primary felt state)
        polyvagal_emoji = {
            'ventral_vagal': ['😊', '🌸', '💚', '✨'],
            'sympathetic': ['⚡', '💥', '🎯', '⏰'],
            'dorsal_vagal': ['🌊', '💙', '🌿', '🌙'],  # 🌀 PHASE 1.5c: Prioritize 🌊💙🌿
            'mixed_state': ['🤔', '😌', '🌤️', '🌅']
        }
        if lures.polyvagal_state in polyvagal_emoji:
            # 🌀 PHASE 1.5c: In dorsal collapse, use MORE dorsal emojis (Zone 5)
            if lures.polyvagal_state == 'dorsal_vagal':
                suggestions.extend(polyvagal_emoji[lures.polyvagal_state][:3])  # Use 3 instead of 2
            else:
                suggestions.extend(polyvagal_emoji[lures.polyvagal_state][:2])

        # 2. Organ-specific emojis (top dominant organs)
        organ_emoji = {
            'LISTENING': ['👂', '🎧', '🔍'],
            'EMPATHY': ['💗', '🫂', '🤝'],
            'WISDOM': ['🦉', '📚', '💡'],
            'AUTHENTICITY': ['💎', '🔥', '⭐'],
            'PRESENCE': ['🧘', '🌳', '☀️'],
            'BOND': ['🫂', '💜', '🛡️'],
            'SANS': ['🧩', '🔗', '✨'],
            'NDAM': ['⚠️', '🚨', '🔔'],
            'RNX': ['🎵', '⏳', '🌊'],
            'EO': ['💚', '🫁', '💓'],
            'CARD': ['📏', '🎚️', '⚖️']
        }
        for organ in lures.dominant_organs[:2]:  # Top 2
            if organ in organ_emoji:
                suggestions.append(organ_emoji[organ][0])

        # 3. Trauma-aware emojis (if trauma present)
        if lures.trauma_present:
            suggestions.extend(['🫂', '🌿', '🕊️'])

        # 4. Crisis emojis (if crisis detected)
        if lures.crisis_level > 0.5:
            suggestions.extend(['🛡️', '⚓', '🌿'])

        # Return unique emojis (5-6 suggestions)
        unique = []
        for emoji in suggestions:
            if emoji not in unique:
                unique.append(emoji)
        return unique[:6]

    def _length_to_tokens(self, length: str) -> int:
        """
        Convert response length to token count.

        🔥 Nov 14, 2025: Reduced token limits for more concise responses
        """
        mapping = {
            'short': 40,      # 🔥 Was 50 - even more concise for crisis
            'medium': 100,    # 🔥 Was 150 - default now more conversational
            'long': 180       # 🔥 Was 300 - comprehensive but not verbose
        }
        return mapping.get(length, 100)  # 🔥 Default to 100, not 150

    def _apply_safety_filter(self, text: str, lures: FeltLures) -> str:
        """
        Apply safety filter to LLM output.

        Checks for harmful content based on trauma/crisis signals.
        🔥 Nov 15, 2025: Added placeholder text filtering
        """
        import re

        # 🔥 Nov 15, 2025: Remove placeholder bracket text
        # LLM sometimes hallucinates "[insert...]" when uncertain
        text = re.sub(r'\[insert[^\]]*\]', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\[add[^\]]*\]', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\[fill[^\]]*\]', '', text, flags=re.IGNORECASE)

        # Clean up double spaces after removal
        text = re.sub(r'\s+', ' ', text).strip()

        # Simple safety checks (can be enhanced)
        if lures.trauma_present or lures.crisis_level > 0.5:
            # Check for potentially harmful phrases
            harmful_patterns = [
                "just get over it",
                "it's not that bad",
                "you're overreacting",
                "snap out of it"
            ]

            text_lower = text.lower()
            for pattern in harmful_patterns:
                if pattern in text_lower:
                    # Replace with safe response
                    return "I'm here with you. What do you need right now?"

        return text


# Module-level convenience function
def create_felt_guided_generator(llm_bridge, enable_safety_gates=True):
    """Create a FeltGuidedLLMGenerator instance."""
    return FeltGuidedLLMGenerator(
        llm_bridge=llm_bridge,
        enable_safety_gates=enable_safety_gates,
        enable_emergent_personality=True  # Always use emergent for Option B
    )
