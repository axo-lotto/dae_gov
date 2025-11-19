#!/usr/bin/env python3
"""
Symbiotic LLM Entity Extractor
================================

Extension to LocalLLMBridge for entity extraction in symbiotic training mode.

Leverages existing OLLAMA infrastructure while adding:
1. Entity extraction mode (fast, 0.5s)
2. Three-tier processing (Pure DAE → Augmented → LLM Fallback)
3. Learning loop (LLM → DAE pattern transfer)
4. Comparison logging for pattern tuning

Date: November 18, 2025
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime

try:
    from persona_layer.local_llm_bridge import LocalLLMBridge
except ImportError:
    print("Warning: Could not import LocalLLMBridge")
    LocalLLMBridge = None


class SymbioticLLMEntityExtractor:
    """
    Symbiotic LLM entity extractor using existing LocalLLMBridge.

    Three operational modes:
    1. Entity extraction only (0.5s, minimal LLM usage)
    2. Phrase suggestion (1.0s, moderate LLM usage)
    3. Full response fallback (2.0s, complete LLM usage)

    Learning modes:
    - Bootstrap: 70% LLM consultation (Weeks 1-4)
    - Balanced: 40% LLM consultation (Weeks 5-8)
    - Specialized: 10% LLM consultation (Weeks 9-12)
    """

    def __init__(
        self,
        local_llm_bridge: Optional[LocalLLMBridge] = None,
        learning_mode: str = "bootstrap",
        cache_dir: str = "persona_layer/state/llm_learning_cache"
    ):
        """
        Initialize symbiotic entity extractor.

        Args:
            local_llm_bridge: Existing LocalLLMBridge instance (or create new)
            learning_mode: "bootstrap", "balanced", "specialized"
            cache_dir: Directory for learning cache
        """
        # Use existing bridge or create new one
        if local_llm_bridge is None:
            if LocalLLMBridge is not None:
                self.llm_bridge = LocalLLMBridge()
            else:
                raise ImportError("LocalLLMBridge not available")
        else:
            self.llm_bridge = local_llm_bridge

        self.learning_mode = learning_mode
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Learning cache
        self.successful_extractions = []
        self.comparison_logs = []

        # Tier statistics
        self.tier_stats = {
            "tier1_pure_dae": 0,
            "tier2_augmented": 0,
            "tier3_llm_fallback": 0
        }

        # Consultation rates by learning mode
        self.consultation_rates = {
            "bootstrap": 0.70,     # 70% LLM consultation (Weeks 1-4)
            "balanced": 0.40,      # 40% LLM consultation (Weeks 5-8)
            "specialized": 0.10    # 10% LLM consultation (Weeks 9-12)
        }

        print(f"✅ SymbioticLLMEntityExtractor initialized")
        print(f"   Mode: {learning_mode}")
        print(f"   LLM consultation rate: {self.consultation_rates[learning_mode]*100}%")
        print(f"   Bridge enabled: {self.llm_bridge.enabled}")

    # ================================================================
    # MODE 1: ENTITY EXTRACTION
    # ================================================================

    def extract_entities_llm(
        self,
        text: str,
        current_entities: Dict
    ) -> Dict[str, Any]:
        """
        Extract entities using local LLM (OLLAMA).

        Prompt engineering for therapeutic domain entity extraction.
        Fast mode: ~0.5s per extraction.

        Args:
            text: User input text
            current_entities: Known entities from profile

        Returns:
            Dictionary with extracted entities
        """

        if not self.llm_bridge.enabled:
            return {}

        # Build entity extraction prompt
        prompt = self._build_entity_extraction_prompt(text, current_entities)

        # Query LLM using existing bridge's direct query method
        result = self.llm_bridge.query_direct(
            prompt=prompt,
            temperature=0.3,  # Low temp for consistency
            max_tokens=300
        )

        if result and result.get('success'):
            # Parse JSON response
            try:
                entities = self._parse_entity_response(result['response'])
                self.tier_stats['tier2_augmented'] += 1
                return entities
            except json.JSONDecodeError as e:
                print(f"⚠️  Failed to parse entity JSON: {e}")
                return {}
        else:
            return {}

    def _build_entity_extraction_prompt(
        self,
        text: str,
        current_entities: Dict
    ) -> str:
        """
        Build therapeutic-domain entity extraction prompt.

        Focus on:
        - People (family, friends, therapists, etc.)
        - Places (home, work, hospital, etc.)
        - Emotions (anxiety, joy, depression, etc.)
        - Relationships (daughter, partner, therapist, etc.)
        """

        # Format current entities for context
        known_entities_str = ""
        if current_entities:
            known_entities_str = f"\nKnown entities: {json.dumps(current_entities, indent=2)}"

        prompt = f"""Extract entities from this therapeutic conversation.

Input: "{text}"{known_entities_str}

Extract these entity types:
1. PEOPLE: Names of people mentioned (family, friends, professionals)
2. RELATIONSHIPS: Family relations (daughter, son, partner, therapist, etc.)
3. PLACES: Locations mentioned (home, work, hospital, school, etc.)
4. EMOTIONS: Emotional states (anxiety, depression, joy, sadness, etc.)

Return ONLY valid JSON in this exact format:
{{
  "relationships": [
    {{"name": "Emma", "relationship": "daughter", "type": "Person"}},
    {{"name": "Dr. Smith", "relationship": "therapist", "type": "Person"}}
  ],
  "places": [
    {{"name": "hospital", "type": "Place"}},
    {{"name": "work", "type": "Place"}}
  ],
  "emotions": [
    {{"name": "anxiety", "intensity": "high"}},
    {{"name": "relief", "intensity": "moderate"}}
  ],
  "mentioned_names": ["Emma", "Dr. Smith"]
}}

JSON response:"""

        return prompt

    def _parse_entity_response(self, llm_response: str) -> Dict[str, Any]:
        """
        Parse LLM entity extraction response.

        Args:
            llm_response: Raw LLM response

        Returns:
            Parsed entities dictionary
        """
        # Try to extract JSON from response
        # LLMs sometimes wrap JSON in markdown code blocks
        llm_response = llm_response.strip()

        # Remove markdown code blocks if present
        if llm_response.startswith("```json"):
            llm_response = llm_response[7:]  # Remove ```json
        if llm_response.startswith("```"):
            llm_response = llm_response[3:]  # Remove ```
        if llm_response.endswith("```"):
            llm_response = llm_response[:-3]  # Remove ```

        llm_response = llm_response.strip()

        # Parse JSON
        entities = json.loads(llm_response)

        return entities

    # ================================================================
    # MODE 2: PHRASE SUGGESTION
    # ================================================================

    def suggest_phrases(
        self,
        felt_state: Dict,
        entity_context: Dict,
        n_suggestions: int = 5
    ) -> List[str]:
        """
        Get phrase suggestions from LLM based on felt-state.

        Speed: ~1.0s
        Use: When DAE has good felt-state but no matching phrases

        Args:
            felt_state: DAE felt-state (polyvagal, organs, etc.)
            entity_context: Entity context
            n_suggestions: Number of suggestions

        Returns:
            List of phrase suggestions
        """

        if not self.llm_bridge.enabled:
            return []

        # Build phrase suggestion prompt
        prompt = self._build_phrase_suggestion_prompt(
            felt_state,
            entity_context,
            n_suggestions
        )

        # Query LLM
        result = self.llm_bridge.query_direct(
            prompt=prompt,
            temperature=0.7,  # Higher temp for variety
            max_tokens=400
        )

        if result and result.get('success'):
            # Parse numbered list
            phrases = self._parse_numbered_list(result['response'])
            self.tier_stats['tier2_augmented'] += 1
            return phrases[:n_suggestions]
        else:
            return []

    def _build_phrase_suggestion_prompt(
        self,
        felt_state: Dict,
        entity_context: Dict,
        n_suggestions: int
    ) -> str:
        """Build phrase suggestion prompt from felt-state."""

        polyvagal = felt_state.get('polyvagal_state', 'unknown')
        self_zone = felt_state.get('self_zone', 'unknown')
        top_organs = felt_state.get('top_organs', [])
        entities = entity_context.get('entities', [])

        prompt = f"""Given this therapeutic state, suggest {n_suggestions} empathetic responses:

Emotional state:
- Polyvagal: {polyvagal}
- SELF zone: {self_zone}
- Dominant organs: {', '.join(top_organs[:3])}
- Entities mentioned: {', '.join([e.get('name', '') for e in entities[:3]])}

Suggest {n_suggestions} brief, trauma-informed responses (1-2 sentences each).
Be empathetic, present, and avoid giving advice.

Suggestions:
1."""

        return prompt

    def _parse_numbered_list(self, text: str) -> List[str]:
        """Parse numbered list from LLM response."""
        import re

        # Find all numbered items (1., 2., etc.)
        pattern = r'^\d+\.\s*(.+?)(?=\n\d+\.|$)'
        matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)

        # Clean up each match
        phrases = [match.strip() for match in matches if match.strip()]

        return phrases

    # ================================================================
    # MODE 3: FULL RESPONSE FALLBACK
    # ================================================================

    def generate_full_response(
        self,
        user_input: str,
        felt_state_context: Optional[Dict] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Full response from LLM (Tier 3 fallback).

        Speed: ~2.0s
        Use: Novel situations, low confidence, learning opportunities

        Args:
            user_input: User input
            felt_state_context: Optional felt-state hints
            conversation_history: Optional conversation history

        Returns:
            LLM response text
        """

        if not self.llm_bridge.enabled:
            return ""

        # Build full response prompt
        prompt = self._build_full_response_prompt(
            user_input,
            felt_state_context,
            conversation_history
        )

        # Query LLM
        result = self.llm_bridge.query_direct(
            prompt=prompt,
            temperature=0.8,  # Creative temperature
            max_tokens=400
        )

        if result and result.get('success'):
            self.tier_stats['tier3_llm_fallback'] += 1
            return result['response']
        else:
            return ""

    def _build_full_response_prompt(
        self,
        user_input: str,
        felt_state_context: Optional[Dict],
        conversation_history: Optional[List[Dict]]
    ) -> str:
        """Build full response prompt with context."""

        sections = []

        # Conversation history
        if conversation_history:
            sections.append("Conversation context:")
            for turn in conversation_history[-3:]:  # Last 3 turns
                sections.append(f"  User: {turn.get('user', '')}")
                sections.append(f"  DAE: {turn.get('assistant', '')}")
            sections.append("")

        # Felt-state hints
        if felt_state_context:
            sections.append("Emotional indicators:")
            sections.append(f"  - Polyvagal state: {felt_state_context.get('polyvagal', 'unknown')}")
            sections.append(f"  - Urgency: {felt_state_context.get('urgency', 'moderate')}")
            sections.append(f"  - Stance: {felt_state_context.get('stance', 'empathetic')}")
            sections.append("")

        # Current input
        sections.append(f'Current input: "{user_input}"')
        sections.append("")

        # Instructions
        sections.append("Respond with trauma-awareness and empathy (2-3 sentences):")

        return "\n".join(sections)

    # ================================================================
    # LEARNING LOOP: LLM → DAE TRANSFER
    # ================================================================

    def log_successful_extraction(
        self,
        user_input: str,
        llm_entities: Dict,
        pattern_entities: Dict,
        user_satisfaction: float
    ):
        """
        Log successful extraction for learning.

        Args:
            user_input: Input text
            llm_entities: Entities extracted by LLM
            pattern_entities: Entities extracted by patterns
            user_satisfaction: User satisfaction score
        """

        if user_satisfaction > 0.7:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "input": user_input,
                "llm_entities": llm_entities,
                "pattern_entities": pattern_entities,
                "satisfaction": user_satisfaction
            }

            self.successful_extractions.append(log_entry)

            # Save to cache periodically
            if len(self.successful_extractions) % 10 == 0:
                self._save_learning_cache()

    def compare_extraction_methods(
        self,
        pattern_entities: Dict,
        llm_entities: Dict
    ) -> Dict[str, Any]:
        """
        Compare pattern vs LLM extraction for tuning.

        Args:
            pattern_entities: Entities from pattern matching
            llm_entities: Entities from LLM

        Returns:
            Comparison metrics
        """

        # Extract entity names from both sources
        pattern_names = self._extract_entity_names(pattern_entities)
        llm_names = self._extract_entity_names(llm_entities)

        # Compute metrics
        true_positives = pattern_names & llm_names
        false_positives = pattern_names - llm_names
        false_negatives = llm_names - pattern_names

        precision = (
            len(true_positives) / len(pattern_names)
            if pattern_names else 0.0
        )
        recall = (
            len(true_positives) / len(llm_names)
            if llm_names else 0.0
        )
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0 else 0.0
        )

        comparison = {
            "pattern_count": len(pattern_names),
            "llm_count": len(llm_names),
            "true_positives": list(true_positives),
            "false_positives": list(false_positives),
            "false_negatives": list(false_negatives),
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }

        # Log for analysis
        self.comparison_logs.append(comparison)

        return comparison

    def _extract_entity_names(self, entities: Dict) -> set:
        """Extract all entity names from entity dict."""
        names = set()

        # Extract from relationships
        for rel in entities.get('relationships', []):
            if 'name' in rel:
                names.add(rel['name'].lower())

        # Extract from places
        for place in entities.get('places', []):
            if 'name' in place:
                names.add(place['name'].lower())

        # Extract from mentioned_names
        for name in entities.get('mentioned_names', []):
            names.add(name.lower())

        return names

    def _save_learning_cache(self):
        """Save learning cache to disk."""
        cache_file = self.cache_dir / f"learning_cache_{self.learning_mode}.json"

        cache_data = {
            "learning_mode": self.learning_mode,
            "successful_extractions": self.successful_extractions[-100:],  # Keep last 100
            "comparison_logs": self.comparison_logs[-100:],
            "tier_stats": self.tier_stats,
            "timestamp": datetime.now().isoformat()
        }

        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)

        print(f"💾 Saved learning cache: {len(self.successful_extractions)} extractions")

    # ================================================================
    # TIER ROUTING
    # ================================================================

    def should_use_llm(
        self,
        dae_confidence: float,
        entity_confidence: float
    ) -> Tuple[str, bool]:
        """
        Decide whether to use LLM based on confidence and learning mode.

        Args:
            dae_confidence: DAE emission confidence
            entity_confidence: Entity extraction confidence

        Returns:
            Tuple of (tier_name, should_use_llm)
        """

        consultation_rate = self.consultation_rates[self.learning_mode]

        # Tier 1: Pure DAE (high confidence)
        if dae_confidence > 0.85 and entity_confidence > 0.85:
            self.tier_stats['tier1_pure_dae'] += 1
            return ("tier1_pure_dae", False)

        # Tier 2: Augmented (medium confidence, within consultation rate)
        elif dae_confidence > 0.65:
            import random
            if random.random() < consultation_rate:
                return ("tier2_augmented", True)
            else:
                self.tier_stats['tier1_pure_dae'] += 1
                return ("tier1_pure_dae", False)

        # Tier 3: LLM Fallback (low confidence)
        else:
            return ("tier3_llm_fallback", True)

    # ================================================================
    # STATISTICS
    # ================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get extraction and tier statistics."""
        total_interactions = sum(self.tier_stats.values())

        stats = {
            "learning_mode": self.learning_mode,
            "consultation_rate": self.consultation_rates[self.learning_mode],
            "total_interactions": total_interactions,
            "tier_distribution": {
                "tier1_pure_dae": self.tier_stats['tier1_pure_dae'],
                "tier2_augmented": self.tier_stats['tier2_augmented'],
                "tier3_llm_fallback": self.tier_stats['tier3_llm_fallback']
            },
            "tier_percentages": {
                "tier1_pct": (
                    self.tier_stats['tier1_pure_dae'] / total_interactions * 100
                    if total_interactions > 0 else 0.0
                ),
                "tier2_pct": (
                    self.tier_stats['tier2_augmented'] / total_interactions * 100
                    if total_interactions > 0 else 0.0
                ),
                "tier3_pct": (
                    self.tier_stats['tier3_llm_fallback'] / total_interactions * 100
                    if total_interactions > 0 else 0.0
                )
            },
            "successful_extractions": len(self.successful_extractions),
            "comparison_logs": len(self.comparison_logs),
            "llm_bridge_stats": self.llm_bridge.get_usage_stats()
        }

        return stats

    def print_stats(self):
        """Print formatted statistics."""
        stats = self.get_stats()

        print("\n" + "="*60)
        print("📊 SYMBIOTIC LLM EXTRACTOR STATISTICS")
        print("="*60)
        print(f"Learning mode: {stats['learning_mode']}")
        print(f"LLM consultation rate: {stats['consultation_rate']*100}%")
        print(f"Total interactions: {stats['total_interactions']}")
        print()
        print("Tier Distribution:")
        print(f"  Tier 1 (Pure DAE):     {stats['tier_distribution']['tier1_pure_dae']:3d} ({stats['tier_percentages']['tier1_pct']:.1f}%)")
        print(f"  Tier 2 (Augmented):    {stats['tier_distribution']['tier2_augmented']:3d} ({stats['tier_percentages']['tier2_pct']:.1f}%)")
        print(f"  Tier 3 (LLM Fallback): {stats['tier_distribution']['tier3_llm_fallback']:3d} ({stats['tier_percentages']['tier3_pct']:.1f}%)")
        print()
        print(f"Successful extractions cached: {stats['successful_extractions']}")
        print(f"Comparison logs: {stats['comparison_logs']}")
        print("="*60)


# ================================================================
# CONVENIENCE FUNCTIONS
# ================================================================

def create_symbiotic_extractor(
    learning_mode: str = "bootstrap"
) -> SymbioticLLMEntityExtractor:
    """
    Create symbiotic extractor with existing LocalLLMBridge.

    Args:
        learning_mode: "bootstrap", "balanced", "specialized"

    Returns:
        SymbioticLLMEntityExtractor instance
    """
    if LocalLLMBridge is None:
        raise ImportError("LocalLLMBridge not available")

    # Create or reuse existing bridge
    bridge = LocalLLMBridge()

    # Create symbiotic extractor
    extractor = SymbioticLLMEntityExtractor(
        local_llm_bridge=bridge,
        learning_mode=learning_mode
    )

    return extractor
