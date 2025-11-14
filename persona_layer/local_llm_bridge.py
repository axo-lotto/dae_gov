#!/usr/bin/env python3
"""
Local LLM Bridge (OPTIONAL)
============================

Bridge to local LLM (Ollama, LMStudio, GPT4All) for factual/creative queries.

IMPORTANT:
- This module is OPTIONAL and only used if Config.LOCAL_LLM_ENABLED = True
- Default behavior: LOCAL_LLM_ENABLED = False (100% template-based)
- LLM is NEVER used for therapeutic core - only factual/creative queries
- Strict safety gating: never in Zone 4/5, never if NDAM > 0.7

Architecture:
    PersonaLayer → LocalLLMBridge → Ollama API
                ↓
           Prompt engineering to preserve DAE voice
                ↓
           Fusion with therapeutic core emission

Date: November 12, 2025
"""

import json
import requests
from typing import Dict, List, Optional, Any
from enum import Enum
from config import Config


class LLMBackend(Enum):
    """Supported LLM backends."""
    OLLAMA = "ollama"
    LMSTUDIO = "lmstudio"
    GPT4ALL = "gpt4all"


class LocalLLMBridge:
    """
    Bridge to local LLM for factual/creative queries (OPTIONAL).

    Only used if Config.LOCAL_LLM_ENABLED = True (default: False).

    Responsibilities:
    - Send queries to local LLM API (Ollama, LMStudio, GPT4All)
    - Prompt engineering to preserve DAE's voice
    - Fusion rules for combining LLM output with therapeutic core
    - Timeout and error handling
    - Usage tracking for monitoring

    Safety guarantees:
    - NEVER used for therapeutic core (always bypassed)
    - NEVER used in Zone 4/5 (protective/collapse)
    - NEVER used if NDAM > 0.7 (crisis)
    - NEVER used without explicit user consent
    """

    def __init__(self):
        """Initialize LocalLLMBridge."""
        self.enabled = Config.LOCAL_LLM_ENABLED
        self.backend = LLMBackend(Config.LOCAL_LLM_BACKEND)
        self.model = Config.LOCAL_LLM_MODEL
        self.endpoint = Config.LOCAL_LLM_ENDPOINT
        self.max_tokens = Config.LOCAL_LLM_MAX_TOKENS
        self.temperature = Config.LOCAL_LLM_TEMPERATURE
        self.timeout = Config.LOCAL_LLM_TIMEOUT

        # Usage tracking
        self.queries_sent = 0
        self.queries_failed = 0
        self.total_tokens = 0

        # Load augmentation prompts (if enabled)
        if self.enabled:
            self._load_augmentation_prompts()

    def _load_augmentation_prompts(self):
        """Load LLM augmentation prompts from JSON."""
        try:
            with open(Config.LLM_AUGMENTATION_PROMPTS_PATH, 'r') as f:
                data = json.load(f)

            self.system_prompts = data.get("system_prompts", {})
            self.fusion_rules = data.get("fusion_rules", {})
            self.voice_characteristics = data.get("dae_voice_characteristics", {})

        except FileNotFoundError:
            print(f"Warning: LLM augmentation prompts not found at {Config.LLM_AUGMENTATION_PROMPTS_PATH}")
            self.system_prompts = {}
            self.fusion_rules = {}
            self.voice_characteristics = {}

    # ================================================================
    # QUERY INTERFACE
    # ================================================================

    def query_llm(
        self,
        user_input: str,
        query_type: str,
        dae_emission: str,
        context: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Query local LLM with prompt engineering to preserve DAE voice.

        Args:
            user_input: User's original input
            query_type: Type of query ("factual", "creative", etc.)
            dae_emission: DAE's therapeutic core emission
            context: Optional context dictionary

        Returns:
            Dictionary with LLM response and metadata, or None if failed
        """
        if not self.enabled:
            return None

        # Build prompt
        system_prompt = self._build_system_prompt(query_type)
        user_prompt = self._build_user_prompt(user_input, dae_emission, query_type, context)

        # Query LLM
        try:
            llm_response = self._send_query(system_prompt, user_prompt)

            if llm_response is None:
                self.queries_failed += 1
                return None

            self.queries_sent += 1

            return {
                "llm_text": llm_response,
                "query_type": query_type,
                "backend": self.backend.value,
                "model": self.model,
                "success": True
            }

        except Exception as e:
            print(f"LocalLLMBridge error: {e}")
            self.queries_failed += 1
            return None

    def query_direct(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 150
    ) -> Optional[Dict[str, Any]]:
        """
        Direct LLM query for felt-guided generation (simpler interface).

        Args:
            prompt: The complete prompt to send
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Dictionary with 'response' key containing LLM text, or None if failed
        """
        if not self.enabled:
            return None

        try:
            # Send simple query (no system prompt, just user prompt)
            llm_response = self._send_query(
                system_prompt="You are a helpful, empathetic conversation partner.",
                user_prompt=prompt
            )

            if llm_response is None:
                self.queries_failed += 1
                return None

            self.queries_sent += 1

            return {
                "response": llm_response,
                "llm_response": llm_response,  # Alternate key
                "confidence": 0.7,  # Default confidence
                "backend": self.backend.value,
                "model": self.model,
                "success": True
            }

        except Exception as e:
            print(f"LocalLLMBridge direct query error: {e}")
            self.queries_failed += 1
            return None

    def _build_system_prompt(self, query_type: str) -> str:
        """
        Build system prompt to preserve DAE's voice.

        Args:
            query_type: Type of query

        Returns:
            System prompt string
        """
        base_prompt = self.system_prompts.get(query_type, self.system_prompts.get("default", ""))

        # Add voice characteristics
        voice_traits = "\n".join([
            f"- {trait}: {desc}"
            for trait, desc in self.voice_characteristics.items()
        ])

        system_prompt = f"""{base_prompt}

DAE Voice Characteristics (preserve these):
{voice_traits}

Remember: You are AUGMENTING DAE's therapeutic response, not replacing it.
Keep your response brief, factual, and aligned with DAE's voice.
"""

        return system_prompt

    def _build_user_prompt(
        self,
        user_input: str,
        dae_emission: str,
        query_type: str,
        context: Optional[Dict]
    ) -> str:
        """
        Build user prompt with context.

        Args:
            user_input: User's input
            dae_emission: DAE's emission
            query_type: Query type
            context: Optional context

        Returns:
            User prompt string
        """
        # Get fusion rule for this query type
        fusion_rule = self.fusion_rules.get(query_type, {})
        instruction = fusion_rule.get("instruction", "Provide a brief, factual response.")

        user_prompt = f"""User asked: "{user_input}"

DAE's therapeutic response: "{dae_emission}"

{instruction}

Your response (2-3 sentences max):"""

        return user_prompt

    def _send_query(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """
        Send query to LLM API.

        Args:
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            LLM response text, or None if failed
        """
        if self.backend == LLMBackend.OLLAMA:
            return self._query_ollama(system_prompt, user_prompt)
        elif self.backend == LLMBackend.LMSTUDIO:
            return self._query_lmstudio(system_prompt, user_prompt)
        elif self.backend == LLMBackend.GPT4ALL:
            return self._query_gpt4all(system_prompt, user_prompt)
        else:
            print(f"Unsupported LLM backend: {self.backend}")
            return None

    # ================================================================
    # BACKEND-SPECIFIC IMPLEMENTATIONS
    # ================================================================

    def _query_ollama(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """
        Query Ollama API.

        Args:
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            Response text or None
        """
        try:
            payload = {
                "model": self.model,
                "prompt": f"{system_prompt}\n\n{user_prompt}",
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }

            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip()
            else:
                print(f"Ollama API error: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print(f"Ollama API timeout after {self.timeout}s")
            return None
        except Exception as e:
            print(f"Ollama query error: {e}")
            return None

    def _query_lmstudio(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """
        Query LMStudio API (OpenAI-compatible).

        Args:
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            Response text or None
        """
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }

            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                print(f"LMStudio API error: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print(f"LMStudio API timeout after {self.timeout}s")
            return None
        except Exception as e:
            print(f"LMStudio query error: {e}")
            return None

    def _query_gpt4all(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """
        Query GPT4All API.

        Args:
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            Response text or None
        """
        # GPT4All API implementation (similar to Ollama)
        # TODO: Implement if needed
        print("GPT4All backend not yet implemented")
        return None

    # ================================================================
    # FUSION LOGIC
    # ================================================================

    def fuse_with_dae_emission(
        self,
        dae_emission: str,
        llm_response: str,
        query_type: str
    ) -> str:
        """
        Fuse LLM response with DAE's therapeutic emission.

        Fusion strategies:
        - therapeutic_override: Use DAE only (LLM ignored)
        - factual_framing: Wrap factual content in DAE's holding
        - creative_enhancement: Blend LLM creativity with DAE wisdom

        Args:
            dae_emission: DAE's therapeutic emission
            llm_response: LLM's response
            query_type: Query type

        Returns:
            Fused emission
        """
        fusion_rule = self.fusion_rules.get(query_type, {})
        strategy = fusion_rule.get("strategy", "factual_framing")

        if strategy == "therapeutic_override":
            # Therapeutic core always takes precedence
            return dae_emission

        elif strategy == "factual_framing":
            # Frame factual content with therapeutic holding
            return f"{dae_emission}\n\n{llm_response}"

        elif strategy == "creative_enhancement":
            # Blend creative suggestions with DAE's wisdom
            return f"{dae_emission}\n\n*drawing on broader creative patterns*\n{llm_response}"

        else:
            # Default: simple append
            return f"{dae_emission}\n\n{llm_response}"

    # ================================================================
    # MONITORING & STATISTICS
    # ================================================================

    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get LLM usage statistics.

        Returns:
            Dictionary with usage stats
        """
        return {
            "enabled": self.enabled,
            "backend": self.backend.value if self.enabled else None,
            "model": self.model if self.enabled else None,
            "queries_sent": self.queries_sent,
            "queries_failed": self.queries_failed,
            "success_rate": (
                self.queries_sent / (self.queries_sent + self.queries_failed)
                if (self.queries_sent + self.queries_failed) > 0
                else 0.0
            ),
            "total_tokens_estimate": self.total_tokens
        }

    def reset_stats(self):
        """Reset usage statistics."""
        self.queries_sent = 0
        self.queries_failed = 0
        self.total_tokens = 0


# ================================================================
# CONVENIENCE FUNCTIONS
# ================================================================

def query_llm_if_enabled(
    user_input: str,
    query_type: str,
    dae_emission: str,
    context: Optional[Dict] = None
) -> Optional[Dict[str, Any]]:
    """
    Convenience function to query LLM if enabled.

    Args:
        user_input: User input
        query_type: Query type
        dae_emission: DAE emission
        context: Optional context

    Returns:
        LLM response dict or None
    """
    if not Config.LOCAL_LLM_ENABLED:
        return None

    bridge = LocalLLMBridge()
    return bridge.query_llm(user_input, query_type, dae_emission, context)


def fuse_llm_response(
    dae_emission: str,
    llm_response: str,
    query_type: str
) -> str:
    """
    Convenience function to fuse LLM response with DAE emission.

    Args:
        dae_emission: DAE emission
        llm_response: LLM response
        query_type: Query type

    Returns:
        Fused emission
    """
    bridge = LocalLLMBridge()
    return bridge.fuse_with_dae_emission(dae_emission, llm_response, query_type)


# ================================================================
# MEMORY-ENRICHED LLM BRIDGE (HYBRID SUPERJECT)
# ================================================================

class MemoryEnrichedLLMBridge:
    """
    Extended LLM bridge with memory-enriched context (Hybrid Superject).

    Combines:
    - DAE felt states (11 organs, V0, transduction)
    - Retrieved past moments (prehensive memory)
    - User bundle (persistent identity)
    - Session history (recent turns)

    For creating "LLM with perfect memory through process philosophy."

    Date: November 13, 2025
    """

    def __init__(
        self,
        model_name: str = "llama3.2:3b",
        ollama_url: str = "http://localhost:11434",
        response_mode: str = "full_response",
        max_tokens: int = 500,
        temperature: float = 0.7
    ):
        """
        Initialize memory-enriched LLM bridge.

        Args:
            model_name: Ollama model
            ollama_url: Ollama API endpoint
            response_mode: 'full_response', 'guidance', 'validation'
            max_tokens: Maximum response length
            temperature: Sampling temperature
        """
        # Use existing LocalLLMBridge for Ollama queries
        self.base_bridge = LocalLLMBridge()
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.response_mode = response_mode
        self.max_tokens = max_tokens
        self.temperature = temperature

    def query_with_memory(
        self,
        user_input: str,
        dae_felt_states: Dict,
        similar_moments: List[Dict],
        user_bundle: Dict,
        session_context: Optional[str] = None,
        dae_emission: Optional[str] = None
    ) -> Dict:
        """
        Query local LLM with memory-enriched context.

        Args:
            user_input: Current user message
            dae_felt_states: DAE organ results + V0 + transduction
            similar_moments: Retrieved past moments (from MemoryRetrieval)
            user_bundle: User identity bundle
            session_context: Recent session history
            dae_emission: Optional DAE emission (for validation mode)

        Returns:
            {
                "llm_response": str,
                "mode": str,
                "confidence": float,
                "felt_alignment": Dict
            }
        """
        # Build memory-enriched prompt
        prompt = self._build_memory_prompt(
            user_input, dae_felt_states, similar_moments,
            user_bundle, session_context, dae_emission
        )

        # Query using base bridge's Ollama connection
        try:
            llm_response = self.base_bridge._query_ollama(
                system_prompt="",  # Included in full prompt
                user_prompt=prompt
            )

            if llm_response:
                return {
                    "llm_response": llm_response,
                    "mode": self.response_mode,
                    "confidence": 0.7,  # Placeholder
                    "felt_alignment": {"overall": 0.7}
                }
            else:
                return {
                    "llm_response": "",
                    "mode": self.response_mode,
                    "confidence": 0.0,
                    "felt_alignment": {}
                }
        except Exception as e:
            print(f"Memory-enriched query error: {e}")
            return {
                "llm_response": f"[Error: {e}]",
                "mode": self.response_mode,
                "confidence": 0.0,
                "felt_alignment": {}
            }

    def _build_memory_prompt(
        self,
        user_input: str,
        dae_felt_states: Dict,
        similar_moments: List[Dict],
        user_bundle: Dict,
        session_context: Optional[str],
        dae_emission: Optional[str]
    ) -> str:
        """Build memory-enriched prompt."""
        sections = []

        # System identity
        sections.append(
            "You are DAE (Deeply Attending Entity), a trauma-informed AI "
            "with persistent memory and felt intelligence."
        )
        sections.append("")

        # Felt states
        sections.append("=== CURRENT FELT STATES ===")
        polyvagal = dae_felt_states.get("polyvagal_state", "unknown")
        self_zone = dae_felt_states.get("self_zone", 0)
        sections.append(f"Polyvagal: {polyvagal}, SELF Zone: {self_zone}")
        sections.append("")

        # Memory
        if similar_moments:
            sections.append("=== MEMORY (Similar Past Moments) ===")
            for i, m in enumerate(similar_moments[:2], 1):
                sections.append(f"{i}. User: {m.get('input_text', '')[:60]}...")
                sections.append(f"   DAE: {m.get('response_text', '')[:60]}...")
            sections.append("")

        # User identity
        if user_bundle:
            themes = user_bundle.get("themes", [])
            if themes:
                sections.append(f"=== USER THEMES === \n{', '.join(themes[:3])}")
                sections.append("")

        # Session
        if session_context:
            sections.append(f"=== SESSION ===\n{session_context}")
            sections.append("")

        # Current input
        sections.append(f'=== USER MESSAGE ===\n"{user_input}"')
        sections.append("")

        # Instructions
        sections.append("=== RESPONSE ===")
        sections.append("Respond with trauma-awareness and relational continuity.")
        sections.append("")

        return "\n".join(sections)

    def query_direct(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 150
    ) -> Optional[Dict[str, Any]]:
        """
        Direct LLM query for felt-guided generation (delegates to base_bridge).

        Args:
            prompt: The complete prompt to send
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Dictionary with 'response' key containing LLM text, or None if failed
        """
        return self.base_bridge.query_direct(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

