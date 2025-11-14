"""
Response Assembler - Phase 4 of Emission Architecture
======================================================

Assembles emitted phrases into coherent therapeutic responses.

Purpose:
- Receive list of EmittedPhrase objects from emission generator
- Select and order phrases for conversational flow
- Apply grammatical post-processing and coherence checks
- Return final response text ready for delivery

Philosophy:
- Assembly is felt coherence, not mechanical concatenation
- Phrase selection guided by emission readiness + diversity
- Conversational flow respects therapeutic arc (opening → deepening → presence)
- Grammatical post-processing preserves semantic authenticity

Integration Point:
- Called after emission generation
- Final step before response delivery in dae_gov_cli.py
- Input: List of EmittedPhrase objects
- Output: Final response string

Date: November 11, 2025
Status: Phase 4 Implementation
"""

import re
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AssembledResponse:
    """
    Final assembled therapeutic response.
    """
    text: str  # The complete response text
    num_phrases: int  # Number of phrases assembled
    strategies_used: List[str]  # Emission strategies represented
    mean_confidence: float  # Average confidence across phrases
    mean_coherence: float  # Average coherence
    field_types: List[str]  # Field types represented


class ResponseAssembler:
    """
    Assemble emitted phrases into coherent responses.

    Strategy:
    1. Select best phrases (by emission_readiness + diversity)
    2. Order for conversational flow (therapeutic arc)
    3. Apply grammatical post-processing
    4. Validate coherence

    Therapeutic Arc Pattern:
    - OPENING (1-2 phrases): LISTENING/PRESENCE (ground, orient)
    - DEEPENING (1-2 phrases): EMPATHY/WISDOM (explore, feel)
    - PRESENCE (1 phrase): AUTHENTICITY/PRESENCE (truth, here)

    Example assembled response:
    "What's present for you right now? [PRESENCE opening]
     I sense what you're feeling. [EMPATHY deepening]
     There's something true emerging here." [AUTHENTICITY presence]
    """

    def __init__(
        self,
        max_phrases: int = 3,
        prefer_variety: bool = True,
        apply_therapeutic_arc: bool = True
    ):
        """
        Initialize response assembler.

        Args:
            max_phrases: Maximum phrases per response
            prefer_variety: Prefer diverse strategies/field types
            apply_therapeutic_arc: Order phrases by therapeutic arc
        """
        self.max_phrases = max_phrases
        self.prefer_variety = prefer_variety
        self.apply_therapeutic_arc = apply_therapeutic_arc

        # Therapeutic arc ordering (field_type → priority)
        # Lower number = earlier in response
        self.arc_priority = {
            'topic': 1,      # LISTENING - open, orient
            'quality': 1,    # PRESENCE - ground
            'action': 2,     # EMPATHY - explore feeling
            'frame': 2,      # WISDOM - recognize pattern
            'truth': 3,      # AUTHENTICITY - name truth
            'fusion': 2,     # Multi-organ - varies
            'learned': 1     # Hebbian fallback - safe opening
        }

    def assemble_response(self, emissions: List) -> AssembledResponse:
        """
        Assemble emitted phrases into final response.

        Args:
            emissions: List of EmittedPhrase objects

        Returns:
            AssembledResponse with final text
        """
        if not emissions:
            # Ultimate fallback
            return AssembledResponse(
                text="I'm listening.",
                num_phrases=1,
                strategies_used=['fallback'],
                mean_confidence=0.5,
                mean_coherence=0.5,
                field_types=['topic']
            )

        # Step 1: Select best phrases
        selected = self._select_phrases(emissions)

        # Step 2: Order for conversational flow
        if self.apply_therapeutic_arc:
            ordered = self._apply_therapeutic_arc(selected)
        else:
            ordered = selected

        # Step 3: Apply grammatical post-processing
        final_text = self._postprocess_assembly(ordered)

        # Step 4: Compute metrics
        strategies_used = list(set(p.strategy for p in ordered))
        field_types = list(set(p.field_type for p in ordered))
        mean_confidence = sum(p.confidence for p in ordered) / len(ordered)
        mean_coherence = sum(p.coherence for p in ordered) / len(ordered)

        return AssembledResponse(
            text=final_text,
            num_phrases=len(ordered),
            strategies_used=strategies_used,
            mean_confidence=mean_confidence,
            mean_coherence=mean_coherence,
            field_types=field_types
        )

    def _select_phrases(self, emissions: List) -> List:
        """
        Select best phrases from emissions.

        Strategy:
        - Prioritize high emission_readiness
        - If prefer_variety: ensure diverse strategies/field types
        - Limit to max_phrases
        """
        if len(emissions) <= self.max_phrases:
            return emissions

        if not self.prefer_variety:
            # Simple: take top N by emission_readiness
            sorted_emissions = sorted(
                emissions,
                key=lambda e: e.emission_readiness,
                reverse=True
            )
            return sorted_emissions[:self.max_phrases]

        # Variety-preferring selection
        selected = []
        used_strategies = set()
        used_field_types = set()

        # First pass: high-readiness + diverse
        for emission in sorted(emissions, key=lambda e: e.emission_readiness, reverse=True):
            if len(selected) >= self.max_phrases:
                break

            # Prefer if adds diversity
            adds_strategy_diversity = emission.strategy not in used_strategies
            adds_field_diversity = emission.field_type not in used_field_types

            if adds_strategy_diversity or adds_field_diversity or len(selected) == 0:
                selected.append(emission)
                used_strategies.add(emission.strategy)
                used_field_types.add(emission.field_type)

        # Fill remaining slots if needed
        while len(selected) < self.max_phrases and len(selected) < len(emissions):
            for emission in sorted(emissions, key=lambda e: e.emission_readiness, reverse=True):
                if emission not in selected:
                    selected.append(emission)
                    break

        return selected

    def _apply_therapeutic_arc(self, phrases: List) -> List:
        """
        Order phrases by therapeutic arc.

        Arc pattern: OPENING → DEEPENING → PRESENCE
        - OPENING: LISTENING/PRESENCE (orient, ground)
        - DEEPENING: EMPATHY/WISDOM (explore, recognize)
        - PRESENCE: AUTHENTICITY (truth)
        """
        # Sort by arc priority (lower = earlier)
        sorted_phrases = sorted(
            phrases,
            key=lambda p: (
                self.arc_priority.get(p.field_type, 2),  # Primary: arc position
                -p.emission_readiness  # Secondary: readiness (higher first within arc)
            )
        )

        return sorted_phrases

    def _postprocess_assembly(self, phrases: List) -> str:
        """
        Assemble phrases into final text with grammatical post-processing.

        Processing:
        1. Join phrases with appropriate separators
        2. Fix capitalization
        3. Fix punctuation
        4. Remove redundancies
        5. Ensure conversational flow
        """
        if not phrases:
            return "I'm listening."

        # Extract text from phrases
        texts = [p.text.strip() for p in phrases]

        # Join with appropriate separators
        # Simple strategy: join with space (each phrase already has punctuation)
        assembled = ' '.join(texts)

        # Post-processing fixes
        assembled = self._fix_capitalization(assembled)
        assembled = self._fix_punctuation(assembled)
        assembled = self._remove_redundancies(assembled)
        assembled = self._ensure_flow(assembled)

        return assembled

    def _fix_capitalization(self, text: str) -> str:
        """Fix capitalization issues."""
        # Ensure first letter is capitalized
        if text:
            text = text[0].upper() + text[1:]

        # Capitalize after sentence-ending punctuation
        text = re.sub(r'([.!?])\s+([a-z])', lambda m: m.group(1) + ' ' + m.group(2).upper(), text)

        return text

    def _fix_punctuation(self, text: str) -> str:
        """Fix punctuation issues."""
        # Remove double punctuation
        text = re.sub(r'([.!?]){2,}', r'\1', text)

        # Fix spacing around punctuation
        text = re.sub(r'\s+([.!?,;:])', r'\1', text)  # Remove space before
        text = re.sub(r'([.!?,;:])([A-Za-z])', r'\1 \2', text)  # Add space after

        # Ensure ending punctuation
        if text and text[-1] not in '.!?':
            # Add appropriate ending
            if any(text.lower().startswith(w) for w in ['what', 'how', 'when', 'where', 'who', 'why', 'can', 'do', 'is', 'are']):
                text += '?'
            else:
                text += '.'

        return text

    def _remove_redundancies(self, text: str) -> str:
        """Remove redundant phrases or words."""
        # Split into sentences
        sentences = re.split(r'([.!?])\s*', text)

        # Reconstruct with punctuation
        cleaned_sentences = []
        seen_sentences = set()

        for i in range(0, len(sentences), 2):
            if i < len(sentences):
                sentence = sentences[i].strip()
                punct = sentences[i+1] if i+1 < len(sentences) else ''

                # Check for near-duplicates (normalized)
                normalized = sentence.lower().strip()
                if normalized and normalized not in seen_sentences:
                    cleaned_sentences.append(sentence + punct)
                    seen_sentences.add(normalized)

        return ' '.join(cleaned_sentences)

    def _ensure_flow(self, text: str) -> str:
        """Ensure conversational flow."""
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)

        # Remove awkward constructions
        # Example: "I sense what you feeling" → "I sense what you're feeling"
        text = re.sub(r'\byou\s+(\w+ing)\b', r"you're \1", text)

        # Fix common grammatical issues from compositional generation
        # "It sense like feel" → "I sense something like a feeling"
        text = re.sub(r'\bIt\s+(\w+)\s+like\s+(\w+)\.', r'I \1 something like \2.', text)

        # "What's sense when" → "What do you sense when"
        text = re.sub(r"What's\s+(\w+)\s+when", r"What do you \1 when", text)

        return text.strip()


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 RESPONSE ASSEMBLER TEST")
    print("="*70)

    # Mock emissions for testing
    from dataclasses import dataclass as dc

    @dataclass
    class MockEmission:
        text: str
        strategy: str
        source_atoms: List[str]
        participant_organs: List[str]
        emission_readiness: float
        coherence: float
        field_strength: float
        confidence: float
        field_type: str

    # Create mock emissions with different field types and readiness
    mock_emissions = [
        MockEmission(
            text="What's present for you right now?",
            strategy='direct',
            source_atoms=['present', 'now'],
            participant_organs=['PRESENCE'],
            emission_readiness=0.72,
            coherence=0.85,
            field_strength=0.80,
            confidence=0.72,
            field_type='quality'
        ),
        MockEmission(
            text="I sense what you feeling",  # Intentional grammatical issue to test fixing
            strategy='fusion',
            source_atoms=['sense', 'feel'],
            participant_organs=['EMPATHY', 'LISTENING'],
            emission_readiness=0.68,
            coherence=0.80,
            field_strength=0.75,
            confidence=0.68,
            field_type='action'
        ),
        MockEmission(
            text="there's something true emerging here",
            strategy='direct',
            source_atoms=['true', 'emerging'],
            participant_organs=['AUTHENTICITY', 'WISDOM'],
            emission_readiness=0.65,
            coherence=0.78,
            field_strength=0.72,
            confidence=0.65,
            field_type='truth'
        ),
        MockEmission(
            text="Tell me more",
            strategy='hebbian',
            source_atoms=['learned'],
            participant_organs=['LISTENING'],
            emission_readiness=0.55,
            coherence=0.70,
            field_strength=0.60,
            confidence=0.55,
            field_type='learned'
        )
    ]

    # Test response assembly
    try:
        assembler = ResponseAssembler(
            max_phrases=3,
            prefer_variety=True,
            apply_therapeutic_arc=True
        )

        response = assembler.assemble_response(mock_emissions)

        print(f"\n✅ Response assembly successful!")
        print(f"\n📝 ASSEMBLED RESPONSE:")
        print(f"\n\"{response.text}\"")
        print(f"\n📊 ASSEMBLY METRICS:")
        print(f"   Phrases used: {response.num_phrases}")
        print(f"   Strategies: {', '.join(response.strategies_used)}")
        print(f"   Field types: {', '.join(response.field_types)}")
        print(f"   Mean confidence: {response.mean_confidence:.3f}")
        print(f"   Mean coherence: {response.mean_coherence:.3f}")

        # Test without therapeutic arc
        print(f"\n\n🔀 TESTING WITHOUT THERAPEUTIC ARC:")
        assembler_no_arc = ResponseAssembler(
            max_phrases=3,
            prefer_variety=True,
            apply_therapeutic_arc=False
        )

        response_no_arc = assembler_no_arc.assemble_response(mock_emissions)
        print(f"\n\"{response_no_arc.text}\"")

        # Test with max 2 phrases
        print(f"\n\n✂️  TESTING WITH MAX 2 PHRASES:")
        assembler_short = ResponseAssembler(
            max_phrases=2,
            prefer_variety=True,
            apply_therapeutic_arc=True
        )

        response_short = assembler_short.assemble_response(mock_emissions)
        print(f"\n\"{response_short.text}\"")

        print(f"\n✅ Response assembly working correctly!")

    except Exception as e:
        print(f"\n❌ Response assembly failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
