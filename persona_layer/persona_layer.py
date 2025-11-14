"""
PersonaLayer - Conversational Intelligence via Template Libraries
================================================================

Wraps DAE's therapeutic core with personality, memory, and conversational intelligence.

Philosophy:
- Templates as Whiteheadian eternal objects ingressing into occasions
- Therapeutic core is sacrosanct (NEVER override in crisis/protective modes)
- LLM is OPTIONAL (default: disabled, templates-only operation)
- User preferences honored (humor tolerance, response length, etc.)

Architecture:
- Load 6 template libraries (1,130 phrases)
- Select templates based on felt states (Zone, NDAM, meta-atoms, confidence)
- Apply safety gating (Zone 4/5, NDAM > 0.7 → NO personality injection)
- Perform variable substitution (dynamic content insertion)
- Modulate length/tone based on user preferences
- Optionally query LLM (only if enabled + conditions met)
- Track template usage for learning (Phase 2)

Date: November 12, 2025
Status: Phase 1B Implementation
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from config import Config


class QueryType(Enum):
    """Types of queries for LLM classification"""
    THERAPEUTIC = "therapeutic"  # Core DAE only (no LLM ever)
    FACTUAL = "factual"  # LLM can assist
    CREATIVE = "creative"  # LLM can assist
    SMALL_TALK = "small_talk"  # Templates sufficient
    META_PROCESS = "meta_process"  # DAE self-awareness templates


@dataclass
class TemplateContext:
    """Context for template selection and modulation"""
    # Felt states (from organism processing)
    zone: int  # 1-5 (SELF matrix zone)
    ndam_urgency: float  # 0.0-1.0
    polyvagal_state: str  # "ventral_vagal", "sympathetic", "dorsal_vagal", "mixed_state"
    confidence: float  # 0.0-1.0 (emission confidence)
    v0_energy: float  # 0.0-1.0
    kairos_detected: bool

    # Organ states
    organ_coherences: Dict[str, float]
    active_meta_atoms: List[str]
    transduction_pathway: Optional[str]

    # User input
    user_input: str

    # User preferences (from profile)
    response_length: str  # "minimal", "moderate", "comprehensive"
    humor_tolerance: float  # 0.0-1.0
    small_talk_openness: float  # 0.0-1.0
    llm_usage_consent: bool


class PersonaLayer:
    """
    Conversational intelligence layer using template libraries.

    Wraps therapeutic emissions with personality, memory, humor while
    preserving process philosophy integrity and therapeutic safety.
    """

    def __init__(self):
        """Initialize PersonaLayer with all template libraries."""

        # Load template libraries
        self.templates = self._load_templates()

        # LLM bridge (only if enabled)
        self.llm_enabled = Config.LOCAL_LLM_ENABLED
        self.llm_bridge = None
        if self.llm_enabled:
            try:
                from persona_layer.local_llm_bridge import LocalLLMBridge
                self.llm_bridge = LocalLLMBridge()
                print(f"✅ LocalLLMBridge initialized ({Config.LOCAL_LLM_BACKEND})")
            except ImportError:
                print(f"⚠️  LLM enabled but local_llm_bridge not found. Using templates only.")
                self.llm_enabled = False

        # Template usage tracking (for Phase 2 learning)
        self.usage_stats = {}

        print(f"✅ PersonaLayer initialized")
        print(f"   Templates loaded: {sum(len(v) if isinstance(v, list) else self._count_nested(v) for v in self.templates.values())}")
        print(f"   LLM enabled: {self.llm_enabled}")

    def _load_templates(self) -> Dict[str, Any]:
        """Load all 6 template libraries from JSON files."""
        templates = {}

        template_files = {
            'personality': Config.PERSONALITY_TEMPLATES_PATH,
            'small_talk': Config.SMALL_TALK_TEMPLATES_PATH,
            'humor': Config.HUMOR_TEMPLATES_PATH,
            'relationship': Config.RELATIONSHIP_TEMPLATES_PATH,
            'response_style': Config.RESPONSE_STYLE_TEMPLATES_PATH,
            'llm_prompts': Config.LLM_AUGMENTATION_PROMPTS_PATH
        }

        for name, path in template_files.items():
            if path.exists():
                with open(path, 'r') as f:
                    templates[name] = json.load(f)
            else:
                print(f"⚠️  Template file not found: {path}")
                templates[name] = {}

        return templates

    def _count_nested(self, obj) -> int:
        """Count phrases in nested dictionary structure."""
        count = 0
        if isinstance(obj, dict):
            for v in obj.values():
                if isinstance(v, list):
                    count += len(v)
                elif isinstance(v, dict):
                    count += self._count_nested(v)
        return count

    def modulate_emission(
        self,
        base_emission: str,
        context: TemplateContext,
        user_profile: Optional[Dict] = None,
        conversation_history: Optional[List] = None
    ) -> Dict[str, Any]:
        """
        Main modulation logic: wrap therapeutic core with personality.

        Args:
            base_emission: Core therapeutic emission from organism
            context: Felt states and user preferences
            user_profile: Optional user profile data
            conversation_history: Optional past turns

        Returns:
            {
                'emission': str,  # Final modulated emission
                'template_used': Optional[str],  # Which template was applied
                'llm_queried': bool,  # Whether LLM was called
                'safety_override': bool,  # Whether personality was bypassed
                'query_type': str  # Classification of input
            }
        """

        # 1. SAFETY CHECK: Bypass persona layer if therapeutic override needed
        if self._should_bypass_persona(context):
            return {
                'emission': base_emission,
                'template_used': None,
                'llm_queried': False,
                'safety_override': True,
                'query_type': 'THERAPEUTIC',
                'reason': f'Zone {context.zone} or NDAM {context.ndam_urgency:.2f} requires therapeutic core only'
            }

        # 2. Classify query type
        query_type = self._classify_query_type(context)

        # 3. Select and apply templates based on query type
        modulated = base_emission
        template_used = None
        llm_queried = False

        if query_type == QueryType.SMALL_TALK and context.small_talk_openness > 0.5:
            # Add small talk layer
            modulated, template_used = self._add_small_talk_layer(modulated, context)

        elif query_type == QueryType.META_PROCESS:
            # Add self-awareness/process explanation
            modulated, template_used = self._add_process_explanation(modulated, context)

        # 4. Add personality touches (if appropriate)
        if self._humor_appropriate(context):
            modulated, humor_template = self._inject_humor(modulated, context)
            if humor_template:
                template_used = f"{template_used}+{humor_template}" if template_used else humor_template

        # 5. Add meta-commentary (organ references, confidence-based)
        if self._meta_commentary_appropriate(context):
            modulated, meta_template = self._add_meta_commentary(modulated, context)
            if meta_template:
                template_used = f"{template_used}+{meta_template}" if template_used else meta_template

        # 6. Add callbacks (if conversation history exists)
        if conversation_history and len(conversation_history) > 0:
            modulated, callback_template = self._add_callback(modulated, context, conversation_history)
            if callback_template:
                template_used = f"{template_used}+{callback_template}" if template_used else callback_template

        # 7. Modulate length/tone based on user preferences
        modulated = self._modulate_length(modulated, context)
        modulated = self._modulate_tone(modulated, context)

        # 8. OPTIONAL: Query LLM (only if enabled + conditions met)
        if self.llm_enabled and self._should_query_llm(query_type, context):
            llm_response = self._query_llm(context.user_input, query_type, context)
            if llm_response:
                modulated = self._fuse_with_llm(modulated, llm_response, query_type)
                llm_queried = True

        # 9. Track template usage (for Phase 2 learning)
        if template_used:
            self._track_usage(template_used, context)

        return {
            'emission': modulated,
            'template_used': template_used,
            'llm_queried': llm_queried,
            'safety_override': False,
            'query_type': query_type.value
        }

    def _should_bypass_persona(self, context: TemplateContext) -> bool:
        """
        Check if persona layer should be bypassed (safety override).

        Bypass conditions:
        - Zone 4/5 (protective/collapse)
        - NDAM > 0.7 (crisis)
        - Dorsal vagal state (shutdown)
        - Persona layer globally disabled
        """
        if not Config.PERSONA_LAYER_ENABLED:
            return True

        if context.zone in [4, 5]:
            return True

        if context.ndam_urgency > 0.7:
            return True

        if context.polyvagal_state == "dorsal_vagal":
            return True

        return False

    def _classify_query_type(self, context: TemplateContext) -> QueryType:
        """
        Classify user input into query types for appropriate handling.

        Priority order:
        1. THERAPEUTIC (if crisis/high urgency)
        2. META_PROCESS (if asking about DAE)
        3. FACTUAL (if asking factual questions)
        4. CREATIVE (if asking for metaphors/imagination)
        5. SMALL_TALK (if casual/greeting)
        """
        text_lower = context.user_input.lower()

        # High urgency → therapeutic
        if context.ndam_urgency > 0.7:
            return QueryType.THERAPEUTIC

        # Meta-process questions (about DAE itself)
        meta_markers = [
            "how do you work", "what are you", "what are your organs",
            "how does v0", "what is v0", "explain your", "how do your",
            "what's an organ", "how do organs", "why do you", "are you"
        ]
        if any(marker in text_lower for marker in meta_markers):
            return QueryType.META_PROCESS

        # Factual question markers
        factual_markers = [
            "what is", "who is", "when did", "where is",
            "how does", "explain", "define", "what does"
        ]
        if any(marker in text_lower for marker in factual_markers):
            # Filter out therapeutic questions
            therapeutic_topics = [
                "feel", "emotion", "trauma", "part", "self",
                "overwhelm", "anxiety", "depression", "sad", "angry"
            ]
            if not any(topic in text_lower for topic in therapeutic_topics):
                return QueryType.FACTUAL

        # Creative prompts
        creative_markers = [
            "imagine", "what if", "pretend", "suppose",
            "create", "metaphor", "like", "similar to"
        ]
        if any(marker in text_lower for marker in creative_markers):
            return QueryType.CREATIVE

        # Small talk
        small_talk_markers = [
            "hi", "hello", "hey", "what's up", "how are you",
            "good morning", "good night", "weather", "how's it going"
        ]
        if any(marker in text_lower for marker in small_talk_markers):
            return QueryType.SMALL_TALK

        # Default: therapeutic
        return QueryType.THERAPEUTIC

    def _add_small_talk_layer(
        self,
        base_emission: str,
        context: TemplateContext
    ) -> Tuple[str, Optional[str]]:
        """Add small talk template to emission."""
        small_talk_templates = self.templates.get('small_talk', {})

        # Check if greeting
        if any(word in context.user_input.lower() for word in ['hi', 'hello', 'hey']):
            greetings = small_talk_templates.get('greetings', {})
            casual_hellos = greetings.get('casual_hellos', [])
            if casual_hellos:
                greeting = random.choice(casual_hellos)
                return f"{greeting}\n\n{base_emission}", "small_talk.greeting"

        # Default: just return base
        return base_emission, None

    def _add_process_explanation(
        self,
        base_emission: str,
        context: TemplateContext
    ) -> Tuple[str, Optional[str]]:
        """Add process philosophy self-awareness explanation."""
        personality_templates = self.templates.get('personality', {})
        meta_commentary = personality_templates.get('meta_commentary', {})
        process_explanations = meta_commentary.get('process_explanations', {})

        # Check what they're asking about
        text_lower = context.user_input.lower()

        if "organ" in text_lower:
            why_organs = process_explanations.get('why_organs', [])
            if why_organs:
                explanation = random.choice(why_organs)
                return f"{base_emission}\n\n{explanation}", "meta.why_organs"

        if "v0" in text_lower or "converge" in text_lower:
            v0_conv = process_explanations.get('v0_convergence', [])
            if v0_conv:
                explanation = random.choice(v0_conv)
                return f"{base_emission}\n\n{explanation}", "meta.v0_convergence"

        # Default: explain general process
        why_organs = process_explanations.get('why_organs', [])
        if why_organs:
            explanation = random.choice(why_organs)
            return f"{base_emission}\n\n{explanation}", "meta.general"

        return base_emission, None

    def _humor_appropriate(self, context: TemplateContext) -> bool:
        """Check if humor injection is appropriate."""
        # Strict gating
        if context.zone not in [1, 2, 3]:
            return False
        if context.ndam_urgency > 0.5:
            return False
        if context.humor_tolerance < 0.5:
            return False
        if context.confidence < 0.6:
            return False
        if context.polyvagal_state == "dorsal_vagal":
            return False

        # Random chance (don't overdo it)
        return random.random() < 0.3  # 30% chance when all conditions met

    def _inject_humor(
        self,
        base_emission: str,
        context: TemplateContext
    ) -> Tuple[str, Optional[str]]:
        """Inject playful humor if appropriate."""
        humor_templates = self.templates.get('humor', {})

        # Randomly select humor type
        humor_type = random.choice(['absurdist', 'organ_reference', 'mushroom'])

        if humor_type == 'absurdist':
            absurdist = humor_templates.get('absurdist_touches', {})
            non_sequiturs = absurdist.get('non_sequiturs', [])
            if non_sequiturs:
                joke = random.choice(non_sequiturs)
                return f"{base_emission}\n\n{joke}", "humor.absurdist"

        elif humor_type == 'organ_reference':
            dry_wit = humor_templates.get('dry_wit', {})
            about_organs = dry_wit.get('about_organs', [])
            if about_organs and context.confidence > 0.7:  # Only if high confidence
                joke = random.choice(about_organs)
                return f"{base_emission}\n\n{joke}", "humor.organs"

        elif humor_type == 'mushroom':
            # Simple mushroom emoji
            return f"{base_emission} 🍄", "humor.mushroom"

        return base_emission, None

    def _meta_commentary_appropriate(self, context: TemplateContext) -> bool:
        """Check if meta-commentary about organs/process is appropriate."""
        # Safe zones only
        if context.zone not in [1, 2, 3]:
            return False

        # Not during high urgency
        if context.ndam_urgency > 0.5:
            return False

        # Random chance (moderate frequency)
        return random.random() < 0.4  # 40% chance

    def _add_meta_commentary(
        self,
        base_emission: str,
        context: TemplateContext
    ) -> Tuple[str, Optional[str]]:
        """Add meta-commentary about DAE's process/organs."""
        personality_templates = self.templates.get('personality', {})
        meta_commentary = personality_templates.get('meta_commentary', {})

        # Confidence-based commentary
        confidence_based = meta_commentary.get('confidence_based', {})

        if context.confidence > 0.7:
            high_conf_data = confidence_based.get('high_confidence', {})
            high_conf = high_conf_data.get('phrases', []) if isinstance(high_conf_data, dict) else high_conf_data
            if high_conf and context.zone in high_conf_data.get('zone_appropriate', [1, 2, 3, 4, 5]):
                comment = random.choice(high_conf)
                return f"{base_emission}\n\n{comment}", "meta.high_confidence"
        elif context.confidence < 0.4:
            low_conf_data = confidence_based.get('low_confidence', {})
            low_conf = low_conf_data.get('phrases', []) if isinstance(low_conf_data, dict) else low_conf_data
            if low_conf and context.zone in low_conf_data.get('zone_appropriate', [1, 2, 3, 4, 5]):
                comment = random.choice(low_conf)
                return f"{base_emission}\n\n{comment}", "meta.low_confidence"

        # Organ references (if specific organ is highly active)
        organ_refs = meta_commentary.get('organ_references', {})
        for organ, coherence in context.organ_coherences.items():
            if coherence > 0.8 and organ in organ_refs:
                refs = organ_refs[organ]
                if refs:
                    comment = random.choice(refs)
                    return f"{base_emission}\n\n{comment}", f"meta.organ.{organ}"

        return base_emission, None

    def _add_callback(
        self,
        base_emission: str,
        context: TemplateContext,
        conversation_history: List
    ) -> Tuple[str, Optional[str]]:
        """Add callback reference to past conversations (placeholder for Phase 2)."""
        # TODO: Implement proper callback logic when Level 9 (Superject) is ready
        # For now, just return unchanged
        return base_emission, None

    def _modulate_length(self, emission: str, context: TemplateContext) -> str:
        """Modulate response length based on user preference."""
        target_length = context.response_length

        # For now, just return as-is
        # TODO: Implement intelligent truncation/expansion in Phase 2
        return emission

    def _modulate_tone(self, emission: str, context: TemplateContext) -> str:
        """Modulate tone based on context."""
        # Tone is already implicit in template selection
        # This is placeholder for future enhancement
        return emission

    def _should_query_llm(self, query_type: QueryType, context: TemplateContext) -> bool:
        """Determine if LLM should be queried."""
        if not self.llm_enabled:
            return False

        if not context.llm_usage_consent:
            return False

        # Safety checks (NEVER query in these conditions)
        if context.zone in Config.LLM_NEVER_IN_ZONES:
            return False

        if context.ndam_urgency > Config.LLM_NEVER_IF_NDAM_ABOVE:
            return False

        if query_type == QueryType.THERAPEUTIC:
            return False

        # Query for factual/creative only if DAE confidence is low
        if query_type == QueryType.FACTUAL and Config.LLM_QUERY_FOR_FACTUAL:
            return context.confidence < Config.LLM_QUERY_MIN_CONFIDENCE

        if query_type == QueryType.CREATIVE and Config.LLM_QUERY_FOR_CREATIVE:
            return context.confidence < Config.LLM_QUERY_MIN_CONFIDENCE

        return False

    def _query_llm(
        self,
        user_input: str,
        query_type: QueryType,
        context: TemplateContext
    ) -> Optional[str]:
        """Query local LLM (if enabled and available)."""
        if not self.llm_bridge:
            return None

        try:
            response = self.llm_bridge.query(user_input, query_type, context)
            return response
        except Exception as e:
            print(f"⚠️  LLM query failed: {e}")
            return None

    def _fuse_with_llm(
        self,
        dae_emission: str,
        llm_response: str,
        query_type: QueryType
    ) -> str:
        """Fuse DAE emission with LLM response."""
        if query_type == QueryType.FACTUAL:
            # Frame LLM factual answer in DAE's voice
            return f"{llm_response}\n\n(That's what I understand, anyway. Does that help?)"

        elif query_type == QueryType.CREATIVE:
            # LLM provides creative element, DAE grounds it
            return f"{llm_response}\n\nDoes that resonate? What's the felt sense?"

        # Default: just return LLM response wrapped
        return f"{llm_response}\n\n{dae_emission}"

    def _track_usage(self, template_used: str, context: TemplateContext):
        """Track template usage for Phase 2 learning."""
        # Simple tracking for now
        if template_used not in self.usage_stats:
            self.usage_stats[template_used] = {
                'count': 0,
                'total_satisfaction': 0.0,
                'contexts': []
            }

        self.usage_stats[template_used]['count'] += 1
        # Satisfaction will be updated when we have user feedback

        # Store context summary
        self.usage_stats[template_used]['contexts'].append({
            'zone': context.zone,
            'ndam': context.ndam_urgency,
            'confidence': context.confidence
        })

        # Limit context storage
        if len(self.usage_stats[template_used]['contexts']) > 10:
            self.usage_stats[template_used]['contexts'].pop(0)
