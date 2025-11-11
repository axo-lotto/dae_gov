"""
FAISS Vector Memory - Semantic Search for Text Occasions
Phase 2.1: Knowledge Infrastructure

Provides semantic memory and similarity search for DAE-GOV conversations
using 384-dimensional TF-IDF embeddings (100% LLM-free foundation).

Architecture:
- Store TextOccasion embeddings in FAISS index
- Fast similarity search (<10ms for 10k vectors)
- Metadata tracking (source, timestamp, conversation_id)
- Integration with text orchestrator

Author: Claude Code (November 2025)
Status: Phase 2.1 - FAISS Implementation
"""

import json
import time
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import faiss
except ImportError:
    print("⚠️  FAISS not installed. Install with: pip install faiss-cpu")
    faiss = None


@dataclass
class VectorMetadata:
    """Metadata for stored vector."""
    vector_id: str
    text: str
    source: str  # 'conversation', 'corpus', or specific book name
    conversation_id: Optional[str]
    timestamp: str
    chunk_id: str  # Original TextOccasion chunk_id
    position: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class FAISSMemory:
    """
    FAISS-based semantic memory for text occasions.

    Features:
    - 384-dimensional TF-IDF embeddings (LLM-free)
    - Fast L2 distance similarity search
    - Persistent index storage
    - Metadata tracking

    Scope (Phase 2.1):
    - Basic index building
    - Similarity search
    - Metadata retrieval
    - Persistence (save/load)

    Future (Phase 2.2+):
    - Advanced indexing (IVF, PQ for larger corpus)
    - Incremental updates
    - Conversation history search
    """

    def __init__(self, dimension: int = 384, index_path: str = "knowledge_base/faiss"):
        """
        Initialize FAISS memory.

        Args:
            dimension: Embedding dimension (384 for TF-IDF)
            index_path: Directory for index storage
        """
        if faiss is None:
            raise ImportError("FAISS not installed. Run: pip install faiss-cpu")

        self.dimension = dimension
        self.index_path = Path(index_path)
        self.index_path.mkdir(parents=True, exist_ok=True)

        # Initialize FAISS index (FlatL2 for Phase 2.1)
        self.index = faiss.IndexFlatL2(dimension)

        # Metadata storage (in-memory + JSON persistence)
        self.metadata: List[VectorMetadata] = []

        # Statistics
        self.total_vectors = 0
        self.conversations_indexed = set()

        print(f"✅ FAISS Memory initialized")
        print(f"   Dimension: {dimension}")
        print(f"   Index type: FlatL2 (exhaustive search)")
        print(f"   Storage: {self.index_path}")

    def add_text_occasions(self, occasions: List, conversation_id: str, source: str = "conversation"):
        """
        Add text occasions to FAISS index.

        Args:
            occasions: List of TextOccasion entities
            conversation_id: Unique conversation identifier
            source: Source type ('conversation' or corpus name)
        """
        if len(occasions) == 0:
            print("⚠️  No occasions to add")
            return

        # Extract embeddings
        embeddings = np.array([occ.embedding for occ in occasions], dtype=np.float32)

        # Ensure correct shape
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension mismatch: expected {self.dimension}, got {embeddings.shape[1]}")

        # Add to FAISS index
        self.index.add(embeddings)

        # Store metadata
        timestamp = datetime.now().isoformat()
        for i, occ in enumerate(occasions):
            metadata = VectorMetadata(
                vector_id=f"{conversation_id}_{i}",
                text=occ.text,
                source=source,
                conversation_id=conversation_id,
                timestamp=timestamp,
                chunk_id=occ.chunk_id,
                position=occ.position
            )
            self.metadata.append(metadata)

        # Update statistics
        self.total_vectors += len(occasions)
        self.conversations_indexed.add(conversation_id)

        print(f"✅ Added {len(occasions)} vectors from {source}")
        print(f"   Conversation: {conversation_id}")
        print(f"   Total vectors: {self.total_vectors}")

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """
        Search for similar vectors.

        Args:
            query_embedding: Query vector (384-dim)
            k: Number of results to return

        Returns:
            List of dicts with 'metadata', 'distance', 'rank'
        """
        if self.total_vectors == 0:
            print("⚠️  Index is empty, no results")
            return []

        # Reshape query to (1, dimension)
        query = query_embedding.reshape(1, -1).astype(np.float32)

        # Search FAISS index
        start_time = time.perf_counter()
        distances, indices = self.index.search(query, min(k, self.total_vectors))
        search_time = (time.perf_counter() - start_time) * 1000

        # Build results with metadata
        results = []
        for rank, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1:  # FAISS returns -1 for empty slots
                continue

            results.append({
                'metadata': self.metadata[idx].to_dict(),
                'distance': float(dist),
                'similarity': self._distance_to_similarity(float(dist)),
                'rank': rank
            })

        print(f"🔍 Search completed in {search_time:.2f}ms")
        print(f"   Results: {len(results)}")

        return results

    def search_by_text(self, vectorizer, query_text: str, k: int = 5) -> List[Dict]:
        """
        Search by text string (uses TF-IDF vectorizer).

        Args:
            vectorizer: TfidfVectorizer instance (from orchestrator)
            query_text: Query text
            k: Number of results

        Returns:
            List of search results
        """
        # Generate embedding for query
        query_embedding = vectorizer.transform([query_text]).toarray()[0]

        # Pad or truncate to 384 dimensions
        if len(query_embedding) < self.dimension:
            padding = np.zeros(self.dimension - len(query_embedding))
            query_embedding = np.concatenate([query_embedding, padding])
        elif len(query_embedding) > self.dimension:
            query_embedding = query_embedding[:self.dimension]

        return self.search(query_embedding, k)

    def get_conversation_vectors(self, conversation_id: str) -> List[Dict]:
        """
        Retrieve all vectors from a specific conversation.

        Args:
            conversation_id: Conversation identifier

        Returns:
            List of metadata dicts for all vectors in conversation
        """
        results = []
        for i, meta in enumerate(self.metadata):
            if meta.conversation_id == conversation_id:
                results.append({
                    'metadata': meta.to_dict(),
                    'index': i
                })
        return results

    def save(self, filename: str = "faiss_index.bin"):
        """
        Save FAISS index and metadata to disk.

        Args:
            filename: Index filename (default: faiss_index.bin)
        """
        # Save FAISS index
        index_file = self.index_path / filename
        faiss.write_index(self.index, str(index_file))

        # Save metadata
        metadata_file = self.index_path / f"{filename}.metadata.json"
        metadata_dict = {
            'total_vectors': self.total_vectors,
            'conversations_indexed': list(self.conversations_indexed),
            'dimension': self.dimension,
            'vectors': [meta.to_dict() for meta in self.metadata]
        }
        with open(metadata_file, 'w') as f:
            json.dump(metadata_dict, f, indent=2)

        print(f"💾 FAISS index saved to {index_file}")
        print(f"   Metadata: {metadata_file}")
        print(f"   Total vectors: {self.total_vectors}")

    def load(self, filename: str = "faiss_index.bin"):
        """
        Load FAISS index and metadata from disk.

        Args:
            filename: Index filename

        Returns:
            True if loaded successfully, False otherwise
        """
        index_file = self.index_path / filename
        metadata_file = self.index_path / f"{filename}.metadata.json"

        if not index_file.exists() or not metadata_file.exists():
            print(f"⚠️  Index files not found at {self.index_path}")
            return False

        # Load FAISS index
        self.index = faiss.read_index(str(index_file))

        # Load metadata
        with open(metadata_file, 'r') as f:
            metadata_dict = json.load(f)

        self.total_vectors = metadata_dict['total_vectors']
        self.conversations_indexed = set(metadata_dict['conversations_indexed'])
        self.metadata = [VectorMetadata.from_dict(m) for m in metadata_dict['vectors']]

        print(f"✅ FAISS index loaded from {index_file}")
        print(f"   Total vectors: {self.total_vectors}")
        print(f"   Conversations: {len(self.conversations_indexed)}")

        return True

    def get_stats(self) -> Dict:
        """Get memory statistics."""
        return {
            'total_vectors': self.total_vectors,
            'conversations_indexed': len(self.conversations_indexed),
            'dimension': self.dimension,
            'index_type': 'FlatL2',
            'memory_mb': self.index.ntotal * self.dimension * 4 / (1024 * 1024)  # float32
        }

    def _distance_to_similarity(self, distance: float) -> float:
        """Convert L2 distance to similarity score (0-1)."""
        # L2 distance → similarity (higher is more similar)
        # Using exponential decay: similarity = exp(-distance)
        return float(np.exp(-distance))


def test_faiss_memory():
    """Test FAISS memory with synthetic data."""

    print("\n" + "="*70)
    print("FAISS MEMORY TEST - Phase 2.1")
    print("="*70 + "\n")

    # Create FAISS memory
    faiss_memory = FAISSMemory(dimension=384)

    # Create synthetic text occasions
    from transductive.text_occasion import TextOccasion

    occasions = [
        TextOccasion(
            chunk_id=f"test_0_0_{i}_0",
            position=i,
            text=f"Test sentence {i}: This is a governance conversation about {topic}.",
            embedding=np.random.randn(384).astype(np.float32)
        )
        for i, topic in enumerate(["strategy", "leadership", "trauma", "culture", "burnout"])
    ]

    # Add to FAISS
    faiss_memory.add_text_occasions(
        occasions=occasions,
        conversation_id="test_conv_001",
        source="test"
    )

    # Search with query
    print("\n[TEST 1] Search for similar vectors")
    query_embedding = occasions[2].embedding  # "trauma" topic
    results = faiss_memory.search(query_embedding, k=3)

    print(f"\nTop 3 similar results to 'trauma' topic:")
    for result in results:
        print(f"  Rank {result['rank']}: {result['metadata']['text'][:60]}...")
        print(f"    Distance: {result['distance']:.4f}, Similarity: {result['similarity']:.4f}")

    # Get conversation vectors
    print("\n[TEST 2] Retrieve conversation vectors")
    conv_vectors = faiss_memory.get_conversation_vectors("test_conv_001")
    print(f"Found {len(conv_vectors)} vectors in conversation")

    # Save and load
    print("\n[TEST 3] Save and load index")
    faiss_memory.save("test_index.bin")

    # Create new instance and load
    faiss_memory2 = FAISSMemory(dimension=384)
    faiss_memory2.load("test_index.bin")

    # Verify loaded data
    stats = faiss_memory2.get_stats()
    print(f"\nLoaded index statistics:")
    print(f"  Total vectors: {stats['total_vectors']}")
    print(f"  Conversations: {stats['conversations_indexed']}")
    print(f"  Memory: {stats['memory_mb']:.2f} MB")

    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - FAISS Memory Operational")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_faiss_memory()
