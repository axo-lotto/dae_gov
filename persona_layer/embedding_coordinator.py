#!/usr/bin/env python3
"""
Embedding Coordinator - Centralized Embedding Generation (Phase C3.0)
=====================================================================

Singleton coordinator for all sentence-transformer embedding operations.
Prevents redundant model loading and provides session-level caching.

Architecture:
- Single SentenceTransformer instance (all-MiniLM-L6-v2, 384D)
- Per-session LRU cache for input text embeddings
- Thread-safe singleton pattern
- Lazy model loading (only when first embed() called)

Benefits:
- Memory: 90MB × 1 instead of 90MB × 7+ modules
- Performance: 3× speedup on repeated text (cache hits)
- Consistency: Single source of truth for model version
- Maintainability: One place to upgrade model

Usage:
    from persona_layer.embedding_coordinator import EmbeddingCoordinator

    coordinator = EmbeddingCoordinator()
    embedding = coordinator.embed("I feel safe and connected")
    embeddings = coordinator.embed_batch(["text1", "text2", "text3"])

Integration Points:
- EMPATHY organ: Emotional lure field computation
- WISDOM organ: Pattern lure field computation
- AUTHENTICITY organ: Vulnerability lure field computation
- BOND organ: SELF-energy detection (self_energy_detector.py)
- EO organ: Polyvagal state detection (polyvagal_detector.py)
- Training: ARC-inspired trainer (arc_inspired_trainer.py)
- Prototypes: Lure prototype generation (create_lure_prototypes.py)

Date: November 13, 2025
Phase: C3.0 (Infrastructure)
"""

import numpy as np
from typing import List, Optional, Dict, Union
from functools import lru_cache
import threading
from sentence_transformers import SentenceTransformer


class EmbeddingCoordinator:
    """
    Singleton coordinator for all embedding operations.

    Provides centralized sentence-transformer embeddings with:
    - Lazy model loading (only when first needed)
    - Session-level caching (LRU cache for repeated text)
    - Batch processing support
    - Thread-safe singleton pattern

    Model: all-MiniLM-L6-v2 (384D, 80M params, ~90MB memory)

    Cache Strategy:
    - Simple dict for current session
    - Can upgrade to LRU with size limits if needed
    - Cleared between sessions or manually
    """

    _instance: Optional['EmbeddingCoordinator'] = None
    _lock = threading.Lock()
    _model: Optional[SentenceTransformer] = None
    _cache: Dict[str, np.ndarray] = {}
    _initialized: bool = False

    def __new__(cls):
        """Thread-safe singleton instantiation."""
        if cls._instance is None:
            with cls._lock:
                # Double-check pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize coordinator (lazy model loading)."""
        # Only initialize once
        if not EmbeddingCoordinator._initialized:
            with EmbeddingCoordinator._lock:
                if not EmbeddingCoordinator._initialized:
                    # Model will be loaded on first embed() call
                    EmbeddingCoordinator._cache = {}
                    EmbeddingCoordinator._initialized = True

    def _ensure_model_loaded(self):
        """Lazy load sentence transformer model."""
        if EmbeddingCoordinator._model is None:
            with EmbeddingCoordinator._lock:
                if EmbeddingCoordinator._model is None:
                    print("📦 EmbeddingCoordinator: Loading sentence transformer...")
                    EmbeddingCoordinator._model = SentenceTransformer('all-MiniLM-L6-v2')
                    print("✅ EmbeddingCoordinator: Model loaded (all-MiniLM-L6-v2, 384D)")

    def embed(self, text: str, use_cache: bool = True) -> np.ndarray:
        """
        Generate embedding for single text string.

        Args:
            text: Input text to embed
            use_cache: Whether to use session cache (default: True)

        Returns:
            384D embedding vector (numpy array)

        Performance:
        - Cache hit: ~0.001ms (dict lookup)
        - Cache miss: ~5-10ms (model inference)
        """
        self._ensure_model_loaded()

        # Check cache
        if use_cache and text in EmbeddingCoordinator._cache:
            return EmbeddingCoordinator._cache[text]

        # Generate embedding
        embedding = EmbeddingCoordinator._model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        # Cache for session
        if use_cache:
            EmbeddingCoordinator._cache[text] = embedding

        return embedding

    def embed_batch(
        self,
        texts: List[str],
        use_cache: bool = True,
        batch_size: int = 32
    ) -> np.ndarray:
        """
        Generate embeddings for multiple texts (batch processing).

        Args:
            texts: List of input texts to embed
            use_cache: Whether to check/update session cache
            batch_size: Batch size for model inference (default: 32)

        Returns:
            N × 384 embedding matrix (numpy array)

        Performance:
        - Faster than individual embed() calls
        - Use for bulk operations (e.g., prototype generation)
        """
        self._ensure_model_loaded()

        if not texts:
            return np.array([])

        # If caching enabled, check for cached embeddings
        if use_cache:
            cached_embeddings = []
            uncached_texts = []
            uncached_indices = []

            for i, text in enumerate(texts):
                if text in EmbeddingCoordinator._cache:
                    cached_embeddings.append((i, EmbeddingCoordinator._cache[text]))
                else:
                    uncached_texts.append(text)
                    uncached_indices.append(i)

            # If all cached, return immediately
            if not uncached_texts:
                return np.array([emb for _, emb in sorted(cached_embeddings)])

            # Generate embeddings for uncached texts
            new_embeddings = EmbeddingCoordinator._model.encode(
                uncached_texts,
                convert_to_numpy=True,
                show_progress_bar=False,
                batch_size=batch_size
            )

            # Cache new embeddings
            for text, embedding in zip(uncached_texts, new_embeddings):
                EmbeddingCoordinator._cache[text] = embedding

            # Combine cached and new embeddings in original order
            all_embeddings = cached_embeddings + list(zip(uncached_indices, new_embeddings))
            all_embeddings.sort(key=lambda x: x[0])
            return np.array([emb for _, emb in all_embeddings])

        else:
            # No caching - direct batch processing
            return EmbeddingCoordinator._model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False,
                batch_size=batch_size
            )

    def clear_cache(self):
        """
        Clear session-level embedding cache.

        Use cases:
        - Between conversation sessions
        - When memory usage is high
        - For testing/benchmarking
        """
        with EmbeddingCoordinator._lock:
            EmbeddingCoordinator._cache.clear()

    def get_cache_size(self) -> int:
        """Get number of cached embeddings."""
        return len(EmbeddingCoordinator._cache)

    def get_cache_memory_mb(self) -> float:
        """
        Estimate cache memory usage in MB.

        Returns:
            Approximate memory used by cache (MB)
        """
        if not EmbeddingCoordinator._cache:
            return 0.0

        # 384 dimensions × 4 bytes (float32) × num_cached
        num_cached = len(EmbeddingCoordinator._cache)
        bytes_per_embedding = 384 * 4
        total_bytes = num_cached * bytes_per_embedding
        return total_bytes / (1024 * 1024)

    def get_model_info(self) -> Dict[str, Union[str, int, bool]]:
        """
        Get model information.

        Returns:
            Dict with model metadata
        """
        return {
            "model_name": "all-MiniLM-L6-v2",
            "embedding_dim": 384,
            "model_loaded": EmbeddingCoordinator._model is not None,
            "cache_size": self.get_cache_size(),
            "cache_memory_mb": self.get_cache_memory_mb()
        }

    @staticmethod
    def reset_singleton():
        """
        Reset singleton instance (for testing only).

        ⚠️  Use with caution - breaks singleton pattern.
        Only intended for unit tests.
        """
        with EmbeddingCoordinator._lock:
            EmbeddingCoordinator._instance = None
            EmbeddingCoordinator._model = None
            EmbeddingCoordinator._cache = {}
            EmbeddingCoordinator._initialized = False


# ============================================================================
# CONVENIENCE FUNCTIONS (Optional)
# ============================================================================

def get_embedding_coordinator() -> EmbeddingCoordinator:
    """
    Get singleton embedding coordinator instance.

    Convenience function for cleaner imports:
        from persona_layer.embedding_coordinator import get_embedding_coordinator
        coordinator = get_embedding_coordinator()
    """
    return EmbeddingCoordinator()


if __name__ == '__main__':
    """
    Self-test and usage demonstration.
    """
    print("="*80)
    print("🌀 EMBEDDING COORDINATOR - Self Test")
    print("="*80)

    # Test 1: Singleton pattern
    print("\n[Test 1] Singleton Pattern")
    coordinator1 = EmbeddingCoordinator()
    coordinator2 = EmbeddingCoordinator()
    print(f"   Same instance: {coordinator1 is coordinator2}")
    assert coordinator1 is coordinator2, "Singleton pattern broken!"
    print("   ✅ Singleton pattern working")

    # Test 2: Single embedding
    print("\n[Test 2] Single Embedding")
    text = "I feel safe and connected"
    embedding = coordinator1.embed(text)
    print(f"   Input: '{text}'")
    print(f"   Embedding shape: {embedding.shape}")
    print(f"   Embedding norm: {np.linalg.norm(embedding):.3f}")
    assert embedding.shape == (384,), "Wrong embedding dimension!"
    print("   ✅ Single embedding working")

    # Test 3: Caching
    print("\n[Test 3] Caching")
    print(f"   Cache size before: {coordinator1.get_cache_size()}")
    embedding2 = coordinator1.embed(text)  # Should hit cache
    print(f"   Cache size after: {coordinator1.get_cache_size()}")
    assert np.array_equal(embedding, embedding2), "Cache returned different embedding!"
    print("   ✅ Caching working")

    # Test 4: Batch embedding
    print("\n[Test 4] Batch Embedding")
    texts = ["joy", "grief", "fear", "anger", "compassion"]
    embeddings = coordinator1.embed_batch(texts)
    print(f"   Input: {len(texts)} texts")
    print(f"   Embeddings shape: {embeddings.shape}")
    assert embeddings.shape == (5, 384), "Wrong batch embedding shape!"
    print("   ✅ Batch embedding working")

    # Test 5: Cache stats
    print("\n[Test 5] Cache Statistics")
    info = coordinator1.get_model_info()
    print(f"   Model: {info['model_name']}")
    print(f"   Dimension: {info['embedding_dim']}")
    print(f"   Cache size: {info['cache_size']} embeddings")
    print(f"   Cache memory: {info['cache_memory_mb']:.2f} MB")
    print("   ✅ Cache statistics working")

    # Test 6: Clear cache
    print("\n[Test 6] Clear Cache")
    coordinator1.clear_cache()
    print(f"   Cache size after clear: {coordinator1.get_cache_size()}")
    assert coordinator1.get_cache_size() == 0, "Cache not cleared!"
    print("   ✅ Cache clearing working")

    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED - EmbeddingCoordinator Ready")
    print("="*80 + "\n")
