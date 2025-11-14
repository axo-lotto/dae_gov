#!/usr/bin/env python3
"""
Local LLM Activation Computer
==============================

Uses Ollama (Llama 3.2 3B) for organ activation computation.
100% local, zero cost, data privacy preserved.

Designed as drop-in replacement for Claude-based computer.

Date: November 13, 2025
"""

import json
import requests
from pathlib import Path
from typing import Dict, Optional

class LocalLLMActivationComputer:
    """
    Computes organ activations using local LLM (Ollama).

    Philosophy:
    - Free: $0 cost, runs locally
    - Private: Data never leaves machine
    - Autonomous: DAE learning independence from cloud LLMs
    """

    def __init__(
        self,
        model: str = "llama3.2:3b",
        endpoint: str = "http://localhost:11434/api/generate",
        cache_path: str = "persona_layer/llm_activation_cache_local.json"
    ):
        """
        Initialize local LLM activation computer.

        Args:
            model: Ollama model name (default: llama3.2:3b)
            endpoint: Ollama API endpoint
            cache_path: Path to cache file
        """
        self.model = model
        self.endpoint = endpoint
        self.cache_path = Path(cache_path)
        self.cache = self._load_cache()

        self.hits = 0
        self.misses = 0
        self.failed_parses = 0
        self.total_time = 0.0

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
        Compute organ activations using local LLM.

        Same interface as Claude version - drop-in replacement.

        Args:
            text: Input text to analyze
            pair_id: Optional ID for caching
            force_recompute: If True, bypass cache

        Returns:
            Dictionary mapping organ names to activation values (0.0-1.0)
        """
        # Check cache
        if pair_id and not force_recompute and pair_id in self.cache:
            self.hits += 1
            return self.cache[pair_id]

        self.misses += 1

        # Compute using local LLM
        activations = self._llm_compute(text)

        # Cache if pair_id provided
        if pair_id and activations:
            self.cache[pair_id] = activations
            self._save_cache()

        return activations

    def _llm_compute(self, text: str, max_retries: int = 3) -> Dict[str, float]:
        """
        Use local LLM to analyze text and compute organ activations.

        Includes retry logic for JSON parsing failures.

        Args:
            text: Text to analyze
            max_retries: Number of retry attempts for parsing failures

        Returns:
            Activation dict or neutral fallback
        """
        prompt = self._build_prompt(text)

        for attempt in range(max_retries):
            try:
                # Query Ollama
                import time
                start = time.time()

                response = requests.post(
                    self.endpoint,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.2,  # Lower for consistent ratings
                            "num_predict": 500,
                            "top_p": 0.9
                        }
                    },
                    timeout=60  # 60 sec timeout
                )

                elapsed = time.time() - start
                self.total_time += elapsed

                if response.status_code != 200:
                    print(f"⚠️  Ollama API error: {response.status_code}")
                    continue

                # Extract JSON
                content = response.json()["response"].strip()

                # Handle markdown code blocks
                if "```" in content:
                    # Extract content between ``` markers
                    parts = content.split("```")
                    if len(parts) >= 2:
                        content = parts[1]
                        # Remove "json" prefix if present
                        if content.startswith("json"):
                            content = content[4:]
                        content = content.strip()

                # Sometimes models add explanation before/after JSON
                # Try to extract just the JSON object
                if "{" in content and "}" in content:
                    start_idx = content.find("{")
                    end_idx = content.rfind("}") + 1
                    content = content[start_idx:end_idx]

                # Parse JSON
                activations = json.loads(content)

                # Validate and normalize
                required_organs = [
                    "LISTENING", "EMPATHY", "WISDOM", "AUTHENTICITY", "PRESENCE",
                    "BOND", "SANS", "NDAM", "RNX", "EO", "CARD"
                ]

                for organ in required_organs:
                    if organ not in activations:
                        raise ValueError(f"Missing organ: {organ}")

                    # Clamp to [0, 1]
                    activations[organ] = float(activations[organ])
                    activations[organ] = max(0.0, min(1.0, activations[organ]))

                return activations

            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"⚠️  Parse error (attempt {attempt+1}/{max_retries}): {e}")
                print(f"   Raw response: {content[:200]}...")
                self.failed_parses += 1
                continue

            except requests.exceptions.Timeout:
                print(f"⚠️  Ollama timeout (attempt {attempt+1}/{max_retries})")
                continue

            except Exception as e:
                print(f"⚠️  Unexpected error (attempt {attempt+1}/{max_retries}): {e}")
                continue

        # All retries failed - return neutral
        print(f"❌ Failed to parse after {max_retries} attempts, using neutral fallback")
        return self._neutral_activations()

    def _build_prompt(self, text: str) -> str:
        """
        Build prompt optimized for local LLM.

        Simplified instructions for smaller models.
        """
        return f"""Analyze this conversation text and rate 11 dimensions from 0.0 to 1.0.

TEXT:
"{text}"

Rate each dimension:

CONVERSATIONAL ORGANS (text quality):
1. LISTENING: Attunement, curiosity (0.0=dismissive, 1.0=deeply attuned)
2. EMPATHY: Emotional resonance (0.0=cold, 1.0=compassionate)
3. WISDOM: Insight, pattern recognition (0.0=simplistic, 1.0=wise)
4. AUTHENTICITY: Genuine realness (0.0=fake, 1.0=authentic)
5. PRESENCE: Embodied awareness (0.0=dissociated, 1.0=grounded)

TRAUMA/CONTEXT ORGANS (modulation):
6. BOND: Parts activation (0.0=SELF-led, 1.0=parts blended)
7. SANS: Coherence (0.0=fragmented, 1.0=coherent)
8. NDAM: Urgency/crisis (0.0=calm, 1.0=emergency)
9. RNX: Rhythm (0.0=rushed, 1.0=spacious)
10. EO: Nervous system state (0.0=shutdown, 0.5=activated, 1.0=safe)
11. CARD: Support needed (0.0=minimal, 0.5=moderate, 1.0=comprehensive)

Return ONLY valid JSON (no explanation):
{{"LISTENING": 0.0, "EMPATHY": 0.0, "WISDOM": 0.0, "AUTHENTICITY": 0.0, "PRESENCE": 0.0, "BOND": 0.0, "SANS": 0.0, "NDAM": 0.0, "RNX": 0.0, "EO": 0.0, "CARD": 0.0}}"""

    def _neutral_activations(self) -> Dict[str, float]:
        """Fallback to neutral activations if parsing fails."""
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
        Batch compute activations for multiple pairs.

        Args:
            pairs: List of training pairs
            text_key: Key for text in each pair
            id_key: Key for ID in each pair

        Returns:
            Dictionary mapping pair IDs to activation dicts
        """
        results = {}
        total_pairs = len(pairs)

        for idx, pair in enumerate(pairs, 1):
            # Extract pair_id
            if isinstance(pair.get(id_key), dict):
                pair_id = pair[id_key].get("id")
            else:
                pair_id = pair.get(id_key) or pair.get("pair_metadata", {}).get("id")

            text = pair.get(text_key)

            if not pair_id or not text:
                print(f"⚠️  Skipping pair {idx}: missing ID or text")
                continue

            print(f"\n[{idx}/{total_pairs}] Computing: {pair_id}")

            activations = self.compute_activations(text, pair_id=pair_id)
            results[pair_id] = activations

            # Show sample for first few
            if idx <= 3:
                print(f"  NDAM: {activations['NDAM']:.2f}, EO: {activations['EO']:.2f}, "
                      f"BOND: {activations['BOND']:.2f}, PRESENCE: {activations['PRESENCE']:.2f}")

        print(f"\n{'='*60}")
        print(f"✅ Batch complete: {len(results)}/{total_pairs} pairs computed")
        print(f"   Cache hits: {self.hits}, misses: {self.misses}")
        print(f"   Failed parses: {self.failed_parses}")
        if self.misses > 0:
            print(f"   Avg time per computation: {self.total_time/self.misses:.2f}s")
        print(f"{'='*60}")

        return results

    def get_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "cache_size": len(self.cache),
            "cache_hits": self.hits,
            "cache_misses": self.misses,
            "failed_parses": self.failed_parses,
            "hit_rate": self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0,
            "parse_success_rate": 1 - (self.failed_parses / self.misses) if self.misses > 0 else 1,
            "total_time": self.total_time,
            "avg_time_per_miss": self.total_time / self.misses if self.misses > 0 else 0
        }


# Convenience function for quick activation lookup
def get_cached_activations(
    pair_id: str,
    cache_path: str = "persona_layer/llm_activation_cache_local.json"
) -> Optional[Dict[str, float]]:
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
