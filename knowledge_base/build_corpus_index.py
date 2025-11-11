"""
FAISS Corpus Index Builder - Week 2, Day 13-14
Phase 2: Build searchable knowledge base from complete corpus

Indexes all knowledge sources:
1. I Ching (James Legge translation + 4 BAGUA excerpts)
2. Whitehead texts (The Concept of Nature + 7 process philosophy excerpts)
3. Synthetic conversations (30 trauma-informed organizational scenarios)

Creates unified FAISS index for semantic search across all sources.

Author: Claude Code (November 2025)
Status: Corpus Indexing - Week 2, Day 13-14
"""

import sys
from pathlib import Path
import json
import re
from typing import List, Dict, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_base.faiss_memory import FAISSMemory
from orchestration.text_orchestrator import BasicTextOrchestrator


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks for better context preservation.

    Args:
        text: Text to chunk
        chunk_size: Target size in characters
        overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence ending within last 100 chars of chunk
            chunk_text = text[start:end]
            last_period = max(
                chunk_text.rfind('. '),
                chunk_text.rfind('! '),
                chunk_text.rfind('? '),
                chunk_text.rfind('\n\n')
            )

            if last_period > chunk_size - 150:  # Found good break point
                end = start + last_period + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def load_corpus_texts(corpus_dir: Path) -> List[Tuple[str, str, str]]:
    """
    Load all text files from corpus directory.

    Args:
        corpus_dir: Path to whitehead_corpus directory

    Returns:
        List of (filename, category, full_text) tuples
    """
    texts = []

    for filepath in sorted(corpus_dir.glob("*.txt")):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Categorize based on filename
            filename = filepath.stem
            if 'i_ching' in filename or 'bagua' in filename or 'trigram' in filename:
                category = 'i_ching_bagua'
            elif 'whitehead' in filename or 'process_and_reality' in filename:
                category = 'whitehead_process'
            elif 'wordsworth' in filename or 'poetry' in filename:
                category = 'poetry'
            elif any(concept in filename for concept in [
                'actual_occasions', 'prehension', 'concrescence',
                'feeling', 'eternal_objects', 'societies', 'negative_prehensions'
            ]):
                category = 'process_philosophy'
            else:
                category = 'whitehead_general'

            texts.append((filename, category, content))
            print(f"   Loaded: {filename} ({len(content):,} chars) → {category}")

        except Exception as e:
            print(f"   ⚠️  Failed to load {filepath.name}: {e}")

    return texts


def load_synthetic_conversations(conversations_file: Path) -> List[Tuple[str, str, str]]:
    """
    Load synthetic trauma-informed conversations.

    Args:
        conversations_file: Path to synthetic_conversations.json

    Returns:
        List of (conv_id, category, conversation_text) tuples
    """
    conversations = []

    try:
        with open(conversations_file, 'r') as f:
            data = json.load(f)

        for conv in data['conversations']:
            conversations.append((
                conv['id'],
                conv['category'],
                conv['conversation'].strip()
            ))

        print(f"   Loaded: {len(conversations)} synthetic conversations")

    except Exception as e:
        print(f"   ⚠️  Failed to load conversations: {e}")

    return conversations


def build_corpus_index(
    corpus_dir: Path = None,
    conversations_file: Path = None,
    output_dir: Path = None,
    chunk_size: int = 500,
    overlap: int = 100
) -> Dict[str, any]:
    """
    Build FAISS index from complete corpus.

    Args:
        corpus_dir: Path to whitehead_corpus directory
        conversations_file: Path to synthetic_conversations.json
        output_dir: Directory to save FAISS index
        chunk_size: Size of text chunks in characters
        overlap: Overlap between chunks

    Returns:
        Statistics dictionary
    """
    if corpus_dir is None:
        corpus_dir = Path(__file__).parent / "whitehead_corpus"
    else:
        corpus_dir = Path(corpus_dir)

    if conversations_file is None:
        conversations_file = Path(__file__).parent / "synthetic_conversations.json"
    else:
        conversations_file = Path(conversations_file)

    if output_dir is None:
        output_dir = Path(__file__).parent / "corpus_index"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*70)
    print("FAISS CORPUS INDEX BUILDER - Week 2, Day 13-14")
    print("="*70 + "\n")

    # Initialize components
    print("📚 Initializing FAISS and text orchestrator...")
    faiss_memory = FAISSMemory(dimension=384)
    orchestrator = BasicTextOrchestrator()
    print(f"   ✅ FAISS memory initialized (384-dim)")
    print(f"   ✅ Text orchestrator ready (TF-IDF vectorizer)\n")

    stats = {
        "sources_loaded": 0,
        "total_chunks": 0,
        "chunks_by_category": {},
        "total_chars_indexed": 0,
        "faiss_vectors": 0
    }

    # Load corpus texts
    print("📖 Loading corpus texts...")
    corpus_texts = load_corpus_texts(corpus_dir)
    stats["sources_loaded"] += len(corpus_texts)
    print()

    # Load synthetic conversations
    print("💬 Loading synthetic conversations...")
    conversations = load_synthetic_conversations(conversations_file)
    stats["sources_loaded"] += len(conversations)
    print()

    # Process corpus texts into chunks
    print("🔪 Chunking corpus texts...")
    corpus_chunks = []
    for filename, category, text in corpus_texts:
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        for i, chunk in enumerate(chunks):
            corpus_chunks.append({
                'text': chunk,
                'source': filename,
                'category': category,
                'chunk_id': f"{filename}_chunk_{i}",
                'chunk_index': i,
                'total_chunks': len(chunks)
            })

        # Update stats
        stats["total_chunks"] += len(chunks)
        stats["chunks_by_category"][category] = \
            stats["chunks_by_category"].get(category, 0) + len(chunks)
        stats["total_chars_indexed"] += len(text)

        print(f"   {filename}: {len(chunks)} chunks")

    print(f"   ✅ {len(corpus_chunks)} chunks from corpus texts\n")

    # Process synthetic conversations (no chunking - they're already sized well)
    print("💬 Processing synthetic conversations...")
    conversation_chunks = []
    for conv_id, category, text in conversations:
        conversation_chunks.append({
            'text': text,
            'source': 'synthetic_conversations',
            'category': category,
            'chunk_id': conv_id,
            'conversation_id': conv_id,
            'polyvagal_state': next((c['polyvagal_state'] for c in
                json.load(open(conversations_file))['conversations']
                if c['id'] == conv_id), None),
            'self_distance': next((c['self_distance'] for c in
                json.load(open(conversations_file))['conversations']
                if c['id'] == conv_id), None)
        })

        # Update stats
        stats["total_chunks"] += 1
        stats["chunks_by_category"][category] = \
            stats["chunks_by_category"].get(category, 0) + 1
        stats["total_chars_indexed"] += len(text)

    print(f"   ✅ {len(conversation_chunks)} conversation chunks\n")

    # Combine all chunks
    all_chunks = corpus_chunks + conversation_chunks
    print(f"📊 Total chunks to index: {len(all_chunks)}")
    print(f"   Corpus texts: {len(corpus_chunks)}")
    print(f"   Conversations: {len(conversation_chunks)}\n")

    # Index in FAISS using orchestrator
    print("🔍 Building FAISS index...")
    print("   This may take a few minutes...\n")

    # Extended metadata storage (separate from FAISS)
    extended_metadata = {}

    # Process in batches for progress tracking
    batch_size = 50
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i+batch_size]
        batch_texts = [chunk['text'] for chunk in batch]
        batch_metadata = [
            {k: v for k, v in chunk.items() if k != 'text'}
            for chunk in batch
        ]

        # Create text occasions for this batch
        result = orchestrator.process_conversation(
            "\n\n".join(batch_texts),
            conversation_id=f"corpus_batch_{i // batch_size}"
        )

        # Add to FAISS with standard metadata + store extended metadata separately
        for j, (entity, metadata) in enumerate(zip(result.entities, batch_metadata)):
            chunk_id = metadata.get('chunk_id', f'chunk_{i+j}')

            # Add to FAISS with standard metadata
            faiss_memory.add_text_occasions(
                occasions=[entity],
                conversation_id=chunk_id,
                source=metadata.get('source', 'corpus')
            )

            # Store extended metadata separately, indexed by vector_id
            vector_id = f"{chunk_id}_{0}"  # FAISS uses conversation_id + index
            extended_metadata[vector_id] = metadata

        progress = min(i + batch_size, len(all_chunks))
        print(f"   Progress: {progress}/{len(all_chunks)} chunks indexed ({progress/len(all_chunks)*100:.1f}%)")

    stats["faiss_vectors"] = faiss_memory.total_vectors

    print(f"\n   ✅ FAISS index complete: {faiss_memory.total_vectors:,} vectors\n")

    # Save FAISS index
    index_path = output_dir / "corpus_faiss_index.pkl"
    faiss_memory.save(str(index_path))
    print(f"💾 Saved FAISS index: {index_path}")

    # Save extended metadata (category, chunk indices, etc.)
    extended_metadata_path = output_dir / "corpus_extended_metadata.json"
    with open(extended_metadata_path, 'w') as f:
        json.dump(extended_metadata, f, indent=2)
    print(f"📋 Saved extended metadata: {extended_metadata_path}")
    print(f"   ({len(extended_metadata):,} vectors with extended metadata)")

    # Save index statistics
    metadata_path = output_dir / "corpus_index_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump({
            "created": "2025-11-10",
            "description": "Complete DAE-GOV knowledge corpus index",
            "statistics": stats,
            "chunk_size": chunk_size,
            "overlap": overlap,
            "sources": {
                "i_ching_bagua": "I Ching + BAGUA excerpts (for Vector35D dims 25-32)",
                "whitehead_process": "Process and Reality + The Concept of Nature",
                "process_philosophy": "7 process philosophy excerpts (prehension, concrescence, etc.)",
                "synthetic_conversations": "30 trauma-informed organizational scenarios"
            }
        }, f, indent=2)

    print(f"📋 Saved index statistics: {metadata_path}\n")

    return stats


def print_index_summary(stats: Dict[str, any]):
    """Print summary of index building."""
    print("="*70)
    print("FAISS CORPUS INDEX - COMPLETE")
    print("="*70 + "\n")

    print("📊 Indexing Statistics:")
    print(f"   Sources loaded: {stats['sources_loaded']}")
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   FAISS vectors: {stats['faiss_vectors']:,}")
    print(f"   Total characters: {stats['total_chars_indexed']:,}\n")

    print("📂 Chunks by Category:")
    for category, count in sorted(stats['chunks_by_category'].items(),
                                  key=lambda x: x[1], reverse=True):
        print(f"   {category}: {count} chunks")
    print()

    print("✅ Knowledge base ready for semantic search!")
    print("   Next: Create CLI for organism interaction")
    print()


if __name__ == "__main__":
    # Build index
    stats = build_corpus_index()

    # Print summary
    print_index_summary(stats)

    print("💡 Usage Example:")
    print('   from knowledge_base.faiss_memory import FAISSMemory')
    print('   faiss = FAISSMemory.load("knowledge_base/corpus_index/corpus_faiss_index.pkl")')
    print('   results = faiss.search_by_text(vectorizer, "burnout and trauma", k=5)')
    print()
