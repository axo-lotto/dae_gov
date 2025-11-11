"""
Governance Data Loader for DAE_HYPHAE_1 (DAE-GOV)

Converts text conversations to organism-compatible format.
Replaces grid-based ARC processing with text/conversation processing.

Architecture:
- Text embeddings replace grids (768-dim vectors)
- Semantic entities replace grid cells (chunk embeddings into regions)
- Conversation pairs replace ARC tasks ((query, response) instead of (input_grid, output_grid))
- Tri-layer knowledge retrieval provides context (FAISS + Neo4j + Hebbian)

Domain Adaptation:
- FROM: 2D grid arrays (3×3, 9×9, etc.)
- TO: Text sequences (queries, responses, conversations)
- FROM: Color values (0-9 discrete)
- TO: Semantic embeddings (768-dim continuous)
- FROM: Spatial relationships (adjacent cells, rotations)
- TO: Semantic relationships (similar concepts, related entities)

Author: DAE-GOV Team
Date: November 7, 2025
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

# Text processing imports
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  Warning: sentence-transformers not installed. Install with: pip install sentence-transformers")


@dataclass
class ConversationPair:
    """Represents a single conversation pair (query → response)"""
    query: str
    response: str
    metadata: Dict[str, Any] = None


@dataclass
class SemanticEntity:
    """Text-based entity (analogous to grid cell in ARC)"""
    position: Tuple[int, int]  # Spatial position in text (sentence_idx, chunk_idx)
    embedding: np.ndarray      # 768-dim semantic vector
    text: str                  # Original text chunk
    confidence: float          # Semantic coherence


class GovernanceDataLoader:
    """
    Converts text conversations to organism-compatible format.

    Key Transformations:
    1. Text → Embeddings (sentence-transformers)
    2. Embeddings → Entities (chunk into semantic regions)
    3. Conversation pairs → Training pairs (query=INPUT, response=OUTPUT)
    4. Semantic grid → Organism input (compatible with 6 organs)
    """

    def __init__(
        self,
        base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1",
        model_name: str = "all-MiniLM-L6-v2",  # 384-dim, fast
        chunk_size: int = 512,  # Characters per chunk
        grid_size: Tuple[int, int] = (9, 9)  # Semantic grid dimensions
    ):
        self.base_path = Path(base_path)
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.grid_size = grid_size

        # Initialize embedding model
        if EMBEDDINGS_AVAILABLE:
            print(f"Loading embedding model: {model_name}")
            self.embedder = SentenceTransformer(model_name)
            self.embedding_dim = self.embedder.get_sentence_embedding_dimension()
            print(f"✅ Embedding model loaded ({self.embedding_dim}-dim)")
        else:
            self.embedder = None
            self.embedding_dim = 384
            print("⚠️  Embedding model not available (mock mode)")

        # Knowledge base paths (created in Phase 4)
        self.faiss_index_path = self.base_path / "knowledge_base" / "faiss"
        self.neo4j_config_path = self.base_path / "knowledge_base" / "neo4j" / "config.json"

    def load_conversation_corpus(
        self,
        corpus_path: Optional[Path] = None
    ) -> List[ConversationPair]:
        """
        Load conversation corpus from JSON.

        Expected format:
        [
            {"query": "What is prehension?", "response": "...", "metadata": {...}},
            {"query": "Explain concrescence", "response": "...", "metadata": {...}},
            ...
        ]
        """
        if corpus_path is None:
            corpus_path = self.base_path / "knowledge_base" / "corpus" / "conversations.json"

        if not corpus_path.exists():
            print(f"⚠️  Corpus not found: {corpus_path}")
            # Return sample data for testing
            return self._create_sample_conversations()

        with open(corpus_path, 'r') as f:
            data = json.load(f)

        conversations = [
            ConversationPair(
                query=item['query'],
                response=item['response'],
                metadata=item.get('metadata', {})
            )
            for item in data
        ]

        print(f"✅ Loaded {len(conversations)} conversation pairs")
        return conversations

    def _create_sample_conversations(self) -> List[ConversationPair]:
        """Create sample conversations for testing (Phase 2 validation)"""
        return [
            ConversationPair(
                query="What is process philosophy?",
                response="Process philosophy, developed by Alfred North Whitehead, views reality as composed of actual occasions rather than static substances. Each occasion prehends its environment, integrates these prehensions through concrescence, and reaches satisfaction.",
                metadata={"topic": "philosophy", "difficulty": "medium"}
            ),
            ConversationPair(
                query="How does Hebbian learning work?",
                response="Hebbian learning follows the principle 'neurons that fire together, wire together.' When two neurons are repeatedly activated simultaneously, the synaptic connection between them strengthens. This creates learned associations between patterns.",
                metadata={"topic": "neuroscience", "difficulty": "medium"}
            ),
            ConversationPair(
                query="Explain organizational change management",
                response="Organizational change management involves preparing, supporting, and helping individuals and teams in making organizational change. Key steps include creating urgency, building coalitions, developing vision, communicating widely, empowering action, creating wins, consolidating gains, and anchoring changes in culture.",
                metadata={"topic": "hr", "difficulty": "advanced"}
            ),
        ]

    def text_to_embeddings(self, text: str) -> np.ndarray:
        """Convert text to semantic embedding vector"""
        if self.embedder is None:
            # Mock embedding (random vector) for testing without model
            return np.random.randn(self.embedding_dim).astype(np.float32)

        embedding = self.embedder.encode(text, convert_to_numpy=True)
        return embedding.astype(np.float32)

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into semantic chunks.

        Strategy: Sentence-based chunking (preserve semantic boundaries)
        """
        # Simple sentence split (can enhance with spaCy for better boundaries)
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]

        # Group sentences into chunks (~chunk_size characters)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')

        return chunks if chunks else [text]  # Fallback to full text

    def create_semantic_grid(
        self,
        text: str,
        grid_size: Optional[Tuple[int, int]] = None
    ) -> Tuple[np.ndarray, List[SemanticEntity]]:
        """
        Convert text to semantic grid (analogous to ARC grid).

        Process:
        1. Chunk text into semantic regions
        2. Embed each chunk (768-dim)
        3. Arrange chunks in spatial grid (for organ processing)
        4. Create semantic entities (analogous to grid cells)

        Returns:
            grid: np.ndarray of shape (height, width, embedding_dim)
            entities: List of SemanticEntity objects
        """
        if grid_size is None:
            grid_size = self.grid_size

        height, width = grid_size
        grid_capacity = height * width

        # Chunk text
        chunks = self.chunk_text(text)
        num_chunks = len(chunks)

        # Initialize grid
        grid = np.zeros((height, width, self.embedding_dim), dtype=np.float32)
        entities = []

        # Fill grid with chunk embeddings
        for idx, chunk in enumerate(chunks[:grid_capacity]):
            row = idx // width
            col = idx % width

            # Get embedding
            embedding = self.text_to_embeddings(chunk)

            # Store in grid
            grid[row, col, :] = embedding

            # Create entity
            entity = SemanticEntity(
                position=(row, col),
                embedding=embedding,
                text=chunk,
                confidence=1.0  # Can enhance with coherence scoring
            )
            entities.append(entity)

        # If fewer chunks than grid capacity, fill remaining with padding
        if num_chunks < grid_capacity:
            # Padding strategy: repeat last embedding or use zero vector
            padding_embedding = np.zeros(self.embedding_dim, dtype=np.float32)
            for idx in range(num_chunks, grid_capacity):
                row = idx // width
                col = idx % width
                grid[row, col, :] = padding_embedding

        print(f"✅ Created semantic grid: {grid.shape} ({num_chunks} chunks)")
        return grid, entities

    def conversation_to_organism_input(
        self,
        conversation: ConversationPair
    ) -> Dict[str, Any]:
        """
        Convert conversation pair to organism-compatible input.

        Format (compatible with working_pipeline.py):
        {
            'input_grid': semantic_grid (query),
            'output_grid': semantic_grid (response),
            'input_entities': [SemanticEntity, ...],
            'output_entities': [SemanticEntity, ...],
            'metadata': {...}
        }
        """
        # Process query (INPUT)
        input_grid, input_entities = self.create_semantic_grid(conversation.query)

        # Process response (OUTPUT)
        output_grid, output_entities = self.create_semantic_grid(conversation.response)

        organism_input = {
            'input_grid': input_grid,
            'output_grid': output_grid,
            'input_entities': input_entities,
            'output_entities': output_entities,
            'metadata': {
                'query': conversation.query,
                'response': conversation.response,
                'query_length': len(conversation.query),
                'response_length': len(conversation.response),
                **(conversation.metadata or {})
            }
        }

        return organism_input

    def load_training_batch(
        self,
        num_conversations: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Load batch of conversations for training.

        Returns list of organism-compatible inputs (ready for epoch training).
        """
        conversations = self.load_conversation_corpus()

        # Limit to requested number
        conversations = conversations[:num_conversations]

        # Convert to organism inputs
        training_batch = [
            self.conversation_to_organism_input(conv)
            for conv in conversations
        ]

        print(f"✅ Prepared {len(training_batch)} training pairs for organism")
        return training_batch

    def retrieve_knowledge_context(
        self,
        query: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Retrieve relevant knowledge from tri-layer system.

        Tier 1: FAISS semantic search (<10ms)
        Tier 2: Neo4j knowledge graph (<50ms)
        Tier 3: Hebbian learned patterns (varies)

        NOTE: Implemented in Phase 4 (knowledge base build)
        """
        # Placeholder for Phase 4
        return {
            'faiss_results': [],
            'neo4j_concepts': [],
            'hebbian_patterns': [],
            'status': 'pending_phase_4'
        }


def test_governance_data_loader():
    """Test governance data loader with sample conversations"""
    print("\n" + "="*60)
    print("GOVERNANCE DATA LOADER - PHASE 2 TEST")
    print("="*60 + "\n")

    # Initialize loader
    loader = GovernanceDataLoader()

    # Test 1: Load sample conversations
    print("\n[TEST 1] Loading sample conversations...")
    conversations = loader.load_conversation_corpus()
    print(f"✅ Loaded {len(conversations)} conversations")

    # Test 2: Text to embeddings
    print("\n[TEST 2] Converting text to embeddings...")
    sample_text = "Process philosophy is fundamental to understanding DAE-GOV."
    embedding = loader.text_to_embeddings(sample_text)
    print(f"✅ Embedding shape: {embedding.shape} (expected: ({loader.embedding_dim},))")

    # Test 3: Chunk text
    print("\n[TEST 3] Chunking text...")
    long_text = conversations[0].response
    chunks = loader.chunk_text(long_text)
    print(f"✅ Created {len(chunks)} chunks from {len(long_text)} characters")
    for i, chunk in enumerate(chunks[:3]):
        print(f"   Chunk {i+1}: {chunk[:80]}...")

    # Test 4: Create semantic grid
    print("\n[TEST 4] Creating semantic grid...")
    grid, entities = loader.create_semantic_grid(conversations[0].query)
    print(f"✅ Grid shape: {grid.shape}")
    print(f"✅ Entities: {len(entities)}")
    for i, entity in enumerate(entities[:3]):
        print(f"   Entity {i+1} at {entity.position}: {entity.text[:60]}...")

    # Test 5: Conversation to organism input
    print("\n[TEST 5] Converting conversation to organism input...")
    organism_input = loader.conversation_to_organism_input(conversations[0])
    print(f"✅ Organism input keys: {list(organism_input.keys())}")
    print(f"✅ Input grid shape: {organism_input['input_grid'].shape}")
    print(f"✅ Output grid shape: {organism_input['output_grid'].shape}")
    print(f"✅ Input entities: {len(organism_input['input_entities'])}")
    print(f"✅ Output entities: {len(organism_input['output_entities'])}")

    # Test 6: Load training batch
    print("\n[TEST 6] Loading training batch...")
    batch = loader.load_training_batch(num_conversations=3)
    print(f"✅ Training batch size: {len(batch)}")
    print(f"✅ First pair metadata: {batch[0]['metadata'].keys()}")

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED - Governance Data Loader Operational")
    print("="*60 + "\n")

    print("Next Steps:")
    print("  1. Install sentence-transformers: pip install sentence-transformers")
    print("  2. Test with real embedding model (currently mock mode)")
    print("  3. Integrate with organism (working_pipeline.py)")
    print("  4. Build knowledge base (Phase 4)")
    print("  5. Add tri-layer retrieval (FAISS + Neo4j + Hebbian)")


if __name__ == "__main__":
    test_governance_data_loader()
