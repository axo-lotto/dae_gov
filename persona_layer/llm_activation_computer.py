"""
LLM-Augmented Organ Activation Computer
========================================

Uses LLM to compute contextual organ activations for training pairs.
Caches results for fast retrieval during training.

This solves the "keyword ceiling" problem - LLMs can understand subtle
contextual differences between SELF zones that keywords cannot detect.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
import anthropic

class LLMActivationComputer:
    """
    Computes organ activations using Claude to understand context.
    Caches results to avoid repeated API calls.
    """

    def __init__(
        self,
        cache_path: str = "persona_layer/llm_activation_cache.json",
        api_key: Optional[str] = None
    ):
        """
        Initialize LLM activation computer.

        Args:
            cache_path: Path to cache file
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
        """
        self.cache_path = Path(cache_path)
        self.cache = self._load_cache()

        # Initialize Anthropic client
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")
        self.client = anthropic.Anthropic(api_key=api_key)

        self.hits = 0
        self.misses = 0

    def _load_cache(self) -> Dict:
        """Load existing cache or create new one."""
        if self.cache_path.exists():
            with open(self.cache_path) as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Persist cache to disk."""
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def compute_activations(
        self,
        text: str,
        pair_id: Optional[str] = None,
        force_recompute: bool = False
    ) -> Dict[str, float]:
        """
        Compute organ activations for given text using LLM.

        Args:
            text: Input text to analyze
            pair_id: Optional ID for caching
            force_recompute: If True, bypass cache

        Returns:
            Dictionary mapping organ names to activation values (0.0-1.0)
        """
        # Check cache first
        if pair_id and not force_recompute and pair_id in self.cache:
            self.hits += 1
            return self.cache[pair_id]

        self.misses += 1

        # Compute using LLM
        activations = self._llm_compute(text)

        # Cache if pair_id provided
        if pair_id:
            self.cache[pair_id] = activations
            self._save_cache()

        return activations

    def _llm_compute(self, text: str) -> Dict[str, float]:
        """
        Use Claude to analyze text and compute organ activations.
        """
        prompt = f"""Analyze this therapeutic conversation text and rate the following psychological/somatic dimensions on a scale of 0.0 to 1.0:

TEXT TO ANALYZE:
"{text}"

Please rate these 11 dimensions (0.0 = absent/minimal, 1.0 = maximum/intense):

**Conversational Organs (text generation quality):**
1. LISTENING: Quality of inquiry, curiosity, attunement to what's being said
   - 0.0: Dismissive, not listening, missing the point
   - 1.0: Deep attunement, exquisite curiosity, really hearing

2. EMPATHY: Emotional resonance, feeling-with, compassionate presence
   - 0.0: Cold, distant, no emotional connection
   - 1.0: Deep compassion, resonant holding, felt empathy

3. WISDOM: Pattern recognition, systemic understanding, insight
   - 0.0: Simplistic, missing patterns, surface-level
   - 1.0: Profound insight, seeing systems, deep wisdom

4. AUTHENTICITY: Genuine truth-telling, vulnerability, realness
   - 0.0: Performative, fake, hiding behind roles
   - 1.0: Raw honesty, vulnerable sharing, deeply real

5. PRESENCE: Embodied awareness, here-and-now, grounded attention
   - 0.0: Dissociated, abstract, disconnected from body
   - 1.0: Fully embodied, grounded, present in the moment

**Trauma/Context-Aware Organs (modulation/detection):**
6. BOND: IFS parts awareness, SELF vs parts differentiation
   - 0.0: Fully SELF-led, no parts blending, centered
   - 1.0: Parts heavily blended, protectors/exiles activated

7. SANS: Semantic coherence, clarity vs confusion
   - 0.0: Fragmented, incoherent, confusing
   - 1.0: Clear, integrated, coherent meaning

8. NDAM: Urgency level, crisis intensity, need for immediate attention
   - 0.0: Calm, peaceful, no urgency
   - 1.0: Crisis, emergency, high urgency

9. RNX: Temporal rhythm, pacing, rush vs spaciousness
   - 0.0: Rushed, pressured, no breathing room
   - 1.0: Spacious, natural rhythm, unhurried

10. EO: Polyvagal state (autonomic nervous system)
    - 0.0: Dorsal vagal (shutdown, collapse, freeze)
    - 0.5: Sympathetic (fight/flight, activated, mobilized)
    - 1.0: Ventral vagal (safe, social, connected)

11. CARD: Response scaling need (how much support/intervention needed)
    - 0.0: Minimal (just presence, simple reflection)
    - 0.5: Moderate (some guidance, gentle intervention)
    - 1.0: Comprehensive (active support, significant intervention)

Return ONLY a valid JSON object with these exact keys (no explanation):
{{
  "LISTENING": 0.0-1.0,
  "EMPATHY": 0.0-1.0,
  "WISDOM": 0.0-1.0,
  "AUTHENTICITY": 0.0-1.0,
  "PRESENCE": 0.0-1.0,
  "BOND": 0.0-1.0,
  "SANS": 0.0-1.0,
  "NDAM": 0.0-1.0,
  "RNX": 0.0-1.0,
  "EO": 0.0-1.0,
  "CARD": 0.0-1.0
}}"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.3,  # Lower for more consistent ratings
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract JSON from response
            content = response.content[0].text.strip()

            # Handle markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            activations = json.loads(content)

            # Validate all required keys present
            required_organs = [
                "LISTENING", "EMPATHY", "WISDOM", "AUTHENTICITY", "PRESENCE",
                "BOND", "SANS", "NDAM", "RNX", "EO", "CARD"
            ]

            for organ in required_organs:
                if organ not in activations:
                    raise ValueError(f"Missing organ: {organ}")

                # Ensure values are floats in [0, 1]
                activations[organ] = float(activations[organ])
                activations[organ] = max(0.0, min(1.0, activations[organ]))

            return activations

        except Exception as e:
            print(f"⚠️  LLM activation error: {e}")
            # Fallback to neutral activations
            return {
                "LISTENING": 0.5,
                "EMPATHY": 0.5,
                "WISDOM": 0.5,
                "AUTHENTICITY": 0.5,
                "PRESENCE": 0.5,
                "BOND": 0.5,
                "SANS": 0.5,
                "NDAM": 0.5,
                "RNX": 0.5,
                "EO": 0.5,
                "CARD": 0.5
            }

    def batch_compute(
        self,
        pairs: list,
        text_key: str = "input_text",
        id_key: str = "id"
    ) -> Dict[str, Dict[str, float]]:
        """
        Compute activations for multiple pairs in batch.

        Args:
            pairs: List of training pairs
            text_key: Key for text in each pair
            id_key: Key for ID in each pair

        Returns:
            Dictionary mapping pair IDs to activation dicts
        """
        results = {}

        for idx, pair in enumerate(pairs, 1):
            pair_id = pair.get(id_key) or pair.get("pair_metadata", {}).get("id")
            text = pair.get(text_key)

            if not pair_id or not text:
                continue

            print(f"Computing activations {idx}/{len(pairs)}: {pair_id}")

            activations = self.compute_activations(text, pair_id=pair_id)
            results[pair_id] = activations

            # Show sample for first few
            if idx <= 3:
                print(f"  NDAM: {activations['NDAM']:.2f}, EO: {activations['EO']:.2f}, "
                      f"BOND: {activations['BOND']:.2f}, PRESENCE: {activations['PRESENCE']:.2f}")

        print(f"\n✅ Batch complete: {len(results)} pairs computed")
        print(f"   Cache hits: {self.hits}, misses: {self.misses}")

        return results

    def get_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "cache_size": len(self.cache),
            "cache_hits": self.hits,
            "cache_misses": self.misses,
            "hit_rate": self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        }


# Convenience function for quick activation lookup
def get_cached_activations(pair_id: str, cache_path: str = "persona_layer/llm_activation_cache.json") -> Optional[Dict[str, float]]:
    """
    Quick lookup of cached activations without initializing full computer.

    Args:
        pair_id: ID of training pair
        cache_path: Path to cache file

    Returns:
        Activation dict if found, None otherwise
    """
    cache_file = Path(cache_path)
    if not cache_file.exists():
        return None

    with open(cache_file) as f:
        cache = json.load(f)

    return cache.get(pair_id)
