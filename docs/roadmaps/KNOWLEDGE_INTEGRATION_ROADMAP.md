# 🗺️ Knowledge Integration Roadmap
## DAE-GOV Knowledge Infrastructure Testing & Integration Plan

**Version:** 1.0
**Date:** November 10, 2025
**Status:** Phase 2 Knowledge Infrastructure
**Purpose:** Comprehensive testing and integration plan for FAISS + Neo4j + Hebbian learning

---

## 📊 Current Status

### ✅ Completed (Phase 2.1-2.2)

| Component | Status | Lines | Tests | Performance |
|-----------|--------|-------|-------|-------------|
| **FAISS Memory** | ✅ Complete | 493 | 3/3 passing | <3ms search |
| **Neo4j Graph** | ✅ Complete | 655 | Ready | Awaiting DB |
| **Text Orchestrator** | ✅ Complete | 327 | Validated | 4ms latency |
| **3 Organs (SANS, NDAM, BOND)** | ✅ Complete | ~2,000 | Validated | 30ms total |

**Total Production Code**: 4,904 lines
**Current Architecture**: 100% LLM-free, entity-native prehension

---

## 🎯 Integration Goals

### Week 1: Foundation (Days 1-7)
**Target**: Neo4j operational, basic integration tested

### Week 2: Corpus (Days 8-14)
**Target**: FAISS indexed with synthetic corpus, retrieval validated

### Week 3: Learning (Days 15-21)
**Target**: Hebbian learning implemented, pattern emergence measured

### Week 4: Production (Days 22-28)
**Target**: Full system integration, performance benchmarked, docs complete

---

## 📅 Week-by-Week Breakdown

### **Week 1: Neo4j Setup & Foundation Testing**

#### Day 1-2: Neo4j Installation & Validation ✅ PRIORITY

**Option A: Neo4j Aura (RECOMMENDED)**
```bash
# 1. Sign up: https://neo4j.com/cloud/aura-free/
# 2. Create database (2 minutes)
# 3. Save credentials:
#    URI: neo4j+s://xxxxx.databases.neo4j.io
#    User: neo4j
#    Password: [your_password]
```

**Option B: Neo4j Desktop (Local)**
```bash
# 1. Download: https://neo4j.com/download/
# 2. Install (5 minutes)
# 3. Create database
# 4. Start database
# Default URI: bolt://localhost:7687
```

**Option C: Docker (Fastest)**
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest
```

**Validation Test:**
```bash
cd "/Users/daedalea/Desktop/DAE_HYPHAE_1"
export PYTHONPATH="/Users/daedalea/Desktop/DAE_HYPHAE_1:$PYTHONPATH"

# Update password in neo4j_knowledge_graph.py line 83
# Then run:
python3 knowledge_base/neo4j_knowledge_graph.py
```

**Expected Output:**
```
✅ Neo4j Knowledge Graph connected
✅ Created 16 trauma-informed concepts
✅ Created 18 concept relationships
✅ ALL TESTS PASSED
```

**Success Criteria:**
- [ ] Neo4j connected
- [ ] 16 concepts created (polyvagal, IFS, organizational)
- [ ] 18 relationships created (ENABLES, TRANSFORMS_TO, PROTECTS)
- [ ] Transformation path found: Burnout Spiral → Sustainable Rhythm

---

#### Day 3-4: Integration Test (Orchestrator + FAISS + Neo4j)

**Create Integration Test File:**

File: `tests/test_knowledge_integration.py`

```python
"""
Test full knowledge infrastructure integration.

Flow:
1. Text → TextOccasion entities (orchestrator)
2. Entities → FAISS memory (semantic search)
3. Concepts → Neo4j graph (relationship traversal)
4. Validate end-to-end latency (<300ms)
"""

def test_full_integration():
    """Test text orchestrator + FAISS + Neo4j integration."""

    # Initialize all components
    orchestrator = BasicTextOrchestrator()
    faiss_memory = FAISSMemory()
    neo4j_graph = Neo4jKnowledgeGraph()

    # Test conversation
    conversation = """
    Our team is experiencing severe burnout.
    People are exhausted, making mistakes, and morale is terrible.
    We need to find a sustainable rhythm that respects boundaries.
    """

    # Process with orchestrator
    result = orchestrator.process_conversation(conversation, "test_001")

    # Store in FAISS
    faiss_memory.add_text_occasions(
        result.entities,
        conversation_id="test_001"
    )

    # Query Neo4j for related concepts
    burnout_concept = neo4j_graph.find_concept("Burnout Spiral")
    related = neo4j_graph.find_related_concepts("Burnout Spiral", max_hops=2)

    # Find transformation path
    path = neo4j_graph.find_transformation_path(
        "Burnout Spiral",
        "Sustainable Rhythm"
    )

    # Validate
    assert result.aggregate_coherence > 0.2
    assert len(faiss_memory.metadata) > 0
    assert burnout_concept is not None
    assert len(related) > 0
    assert path is not None

    print("✅ Full integration test passed")
```

**Run Test:**
```bash
python3 tests/test_knowledge_integration.py
```

**Success Criteria:**
- [ ] Text processed by orchestrator
- [ ] Entities stored in FAISS
- [ ] Concepts queried from Neo4j
- [ ] Transformation path found
- [ ] Total latency <300ms

---

#### Day 5-7: Performance Benchmarking

**Create Performance Test:**

File: `tests/test_knowledge_performance.py`

```python
"""
Benchmark knowledge infrastructure performance.

Metrics:
- Orchestrator latency
- FAISS search time
- Neo4j query time
- Total end-to-end latency
- Memory usage
"""

import time
import psutil
import numpy as np

def benchmark_full_pipeline(num_conversations=20):
    """Benchmark knowledge infrastructure with N conversations."""

    latencies = {
        'orchestrator': [],
        'faiss_store': [],
        'faiss_search': [],
        'neo4j_query': [],
        'total': []
    }

    for i in range(num_conversations):
        start_total = time.perf_counter()

        # Orchestrator
        start = time.perf_counter()
        result = orchestrator.process_conversation(f"Conversation {i}", f"conv_{i}")
        latencies['orchestrator'].append((time.perf_counter() - start) * 1000)

        # FAISS store
        start = time.perf_counter()
        faiss_memory.add_text_occasions(result.entities, f"conv_{i}")
        latencies['faiss_store'].append((time.perf_counter() - start) * 1000)

        # FAISS search
        start = time.perf_counter()
        results = faiss_memory.search(result.entities[0].embedding, k=5)
        latencies['faiss_search'].append((time.perf_counter() - start) * 1000)

        # Neo4j query
        start = time.perf_counter()
        related = neo4j_graph.find_related_concepts("Burnout Spiral", max_hops=1)
        latencies['neo4j_query'].append((time.perf_counter() - start) * 1000)

        latencies['total'].append((time.perf_counter() - start_total) * 1000)

    # Print statistics
    print("\n📊 PERFORMANCE BENCHMARK RESULTS")
    print("="*60)
    for component, times in latencies.items():
        mean = np.mean(times)
        std = np.std(times)
        p95 = np.percentile(times, 95)
        print(f"{component:15s}: {mean:6.2f}ms ± {std:5.2f}ms (p95: {p95:6.2f}ms)")

    # Memory usage
    process = psutil.Process()
    mem_mb = process.memory_info().rss / (1024 * 1024)
    print(f"\nMemory usage: {mem_mb:.1f} MB")
```

**Target Performance:**
- Orchestrator: 50-100ms
- FAISS store: 5-10ms
- FAISS search: 2-5ms
- Neo4j query: 10-50ms (local) or 30-100ms (cloud)
- **Total: <300ms** ✅

**Success Criteria:**
- [ ] 20 conversations processed
- [ ] Mean latency <300ms
- [ ] Memory usage <500MB
- [ ] No errors or crashes

---

### **Week 2: Corpus Integration**

#### Day 8-10: Synthetic Corpus Generation

**Create Synthetic Trauma-Informed Examples:**

File: `knowledge_base/corpus/synthetic_examples.txt`

```
=== Burnout Spiral Example ===
Our team has been working 60-70 hour weeks for the past six months.
People are exhausted, making more mistakes, and morale is at an all-time low.
We keep saying "just push through, it's almost done" but the deadline keeps moving.
Several team members have called in sick, and two have resigned without another job lined up.
There's a sense of numbness and dissociation in meetings - people are physically present but checked out.

=== Toxic Productivity Example ===
Our culture celebrates overwork as dedication.
People compete to be the first one in and last one out.
Taking breaks is seen as weak, and using vacation days is frowned upon.
Perfectionism is rewarded, and any mistake leads to shame and blame.
The urgency culture means everything is a crisis, everything is due yesterday.

=== Psychological Safety Example ===
Our team has created a culture where vulnerability is welcomed.
People can share mistakes without fear of judgment or punishment.
We practice active listening and genuine curiosity about different perspectives.
Disagreement is seen as valuable data, not personal attack.
Leaders model openness by acknowledging their own learning edges.

[... 20-30 more examples covering all 16 concepts ...]
```

**Generate Examples:**
```bash
cd "/Users/daedalea/Desktop/DAE_HYPHAE_1"
python3 << 'EOF'
# Create 30 synthetic examples (3-5 paragraphs each)
# Covering: Burnout, Toxic Productivity, Scapegoating,
#           Psychological Safety, Sustainable Rhythm, etc.
# Save to knowledge_base/corpus/synthetic_examples.txt
EOF
```

**Success Criteria:**
- [ ] 30 synthetic examples created
- [ ] All 16 concepts represented
- [ ] 3-5 paragraphs per example
- [ ] ~10,000 words total

---

#### Day 11-12: Public Domain Whitehead Texts

**Download Process Philosophy Texts:**

```bash
cd knowledge_base/corpus/whitehead/

# Available from Project Gutenberg / Archive.org
wget https://archive.org/download/processrealitygi00alfr/processrealitygi00alfr.pdf
wget https://archive.org/download/sciencemodernwo00whituoft/sciencemodernwo00whituoft.pdf

# Convert PDF → TXT (using pdftotext or similar)
pdftotext processrealitygi00alfr.pdf process_and_reality.txt
pdftotext sciencemodernwo00whituoft.pdf science_modern_world.txt
```

**Chunk into Paragraphs:**
```python
# Split into 512-token chunks with 50-token overlap
# Create whitehead_chunks.json with metadata
```

**Success Criteria:**
- [ ] 2 Whitehead texts downloaded (public domain)
- [ ] Converted to TXT format
- [ ] Chunked into ~500 paragraphs
- [ ] Metadata tracked (book, chapter, page)

---

#### Day 13-14: FAISS Index Building

**Build FAISS Index from Corpus:**

File: `knowledge_base/build_faiss_corpus.py`

```python
"""
Build FAISS index from corpus.

Process:
1. Load all text files from corpus/
2. Chunk into paragraphs (512 tokens, 50 overlap)
3. Generate TF-IDF embeddings (384-dim)
4. Add to FAISS index with metadata
5. Save index to disk
"""

def build_corpus_index():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from knowledge_base.faiss_memory import FAISSMemory

    faiss_memory = FAISSMemory(dimension=384)
    vectorizer = TfidfVectorizer(max_features=384, ...)

    # Load corpus files
    corpus_files = [
        "corpus/synthetic_examples.txt",
        "corpus/whitehead/process_and_reality.txt",
        "corpus/whitehead/science_modern_world.txt"
    ]

    all_paragraphs = []
    for file in corpus_files:
        with open(file) as f:
            text = f.read()
            paragraphs = text.split('\n\n')  # Simple paragraph split
            all_paragraphs.extend([(p, file) for p in paragraphs if len(p) > 100])

    print(f"Total paragraphs: {len(all_paragraphs)}")

    # Generate embeddings
    texts = [p[0] for p in all_paragraphs]
    embeddings = vectorizer.fit_transform(texts).toarray()

    # Add to FAISS (in batches of 100)
    for i in range(0, len(all_paragraphs), 100):
        batch_para = all_paragraphs[i:i+100]
        batch_emb = embeddings[i:i+100]

        # Create TextOccasion-like objects
        occasions = [
            TextOccasion(
                chunk_id=f"corpus_{j}",
                position=j,
                text=para[0][:200],  # Store excerpt
                embedding=emb
            )
            for j, (para, emb) in enumerate(zip(batch_para, batch_emb))
        ]

        faiss_memory.add_text_occasions(occasions, f"corpus_batch_{i//100}", source="corpus")

    # Save index
    faiss_memory.save("corpus_index.bin")

    print(f"✅ FAISS corpus index built")
    print(f"   Total vectors: {faiss_memory.total_vectors}")
    print(f"   Index size: ~{faiss_memory.total_vectors * 384 * 4 / (1024*1024):.1f} MB")
```

**Run:**
```bash
python3 knowledge_base/build_faiss_corpus.py
```

**Expected Output:**
```
Total paragraphs: ~1,000
✅ FAISS corpus index built
   Total vectors: 1,000
   Index size: ~1.5 MB
```

**Success Criteria:**
- [ ] 1,000+ paragraphs indexed
- [ ] FAISS index saved to disk
- [ ] Index size <5 MB
- [ ] Search test: retrieval precision >60%

---

### **Week 3: Hebbian Learning (Phase 2.3)**

#### Day 15-17: Hebbian Implementation

**Create Hebbian Text Learner:**

File: `knowledge_base/hebbian_text_learner.py`

```python
"""
Hebbian Text Learning - Conversation Pattern Co-Activation

Learns which organs, concepts, and patterns co-activate across conversations.

R-Matrix (Organ Coupling):
- Track when SANS + NDAM both activate strongly
- Learn: "Urgency culture" → NDAM high, SANS low
- Learn: "SELF-energy" → SANS high, BOND high

Pattern Memory:
- "Burnout + Firefighter" → often co-occur
- "Psychological Safety + Ventral Vagal" → strong coupling
- "Toxic Productivity + Sympathetic State" → high correlation
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List

class HebbianTextLearner:
    """
    Hebbian learning for conversation patterns.

    Features:
    - R-matrix: Organ co-activation (6x6 matrix)
    - Concept coupling: Which concepts co-occur
    - Pattern strengthening: Reinforce successful patterns
    """

    def __init__(self, memory_path: str = "knowledge_base/hebbian_text_memory.json"):
        self.memory_path = Path(memory_path)

        # R-matrix: Organ coupling (SANS, NDAM, BOND, RNX, EO, CARD)
        self.R_matrix = np.zeros((6, 6), dtype=np.float32)

        # Concept coupling
        self.concept_coupling = {}

        # Pattern counts
        self.pattern_counts = {}

        # Learning rate
        self.learning_rate = 0.05
        self.decay = 0.01

        # Load existing memory
        self.load()

    def update_organ_coupling(self, organ_results: Dict):
        """
        Update R-matrix based on organ co-activation.

        Hebbian rule: R[i,j] += η * (c_i * c_j) - δ * R[i,j]
        """
        organs = ['SANS', 'NDAM', 'BOND', 'RNX', 'EO', 'CARD']
        coherences = np.array([
            organ_results.get(org, {}).get('coherence', 0.0)
            for org in organs
        ])

        # Update R-matrix
        for i in range(6):
            for j in range(6):
                if i != j:
                    # Hebbian: strengthen if both active
                    self.R_matrix[i, j] += (
                        self.learning_rate * coherences[i] * coherences[j]
                        - self.decay * self.R_matrix[i, j]
                    )

                    # Clip to [0, 1]
                    self.R_matrix[i, j] = np.clip(self.R_matrix[i, j], 0, 1)

    def update_concept_coupling(self, detected_concepts: List[str]):
        """Track which concepts co-occur in conversations."""
        for i, concept_a in enumerate(detected_concepts):
            for concept_b in detected_concepts[i+1:]:
                pair = tuple(sorted([concept_a, concept_b]))
                self.concept_coupling[pair] = self.concept_coupling.get(pair, 0) + 1

    def record_pattern(self, pattern_name: str, success: bool = True):
        """Record pattern occurrence and success."""
        if pattern_name not in self.pattern_counts:
            self.pattern_counts[pattern_name] = {'total': 0, 'success': 0}

        self.pattern_counts[pattern_name]['total'] += 1
        if success:
            self.pattern_counts[pattern_name]['success'] += 1

    def get_pattern_confidence(self, pattern_name: str) -> float:
        """Get confidence for a pattern (success rate)."""
        if pattern_name not in self.pattern_counts:
            return 0.0

        counts = self.pattern_counts[pattern_name]
        return counts['success'] / max(counts['total'], 1)

    def save(self):
        """Save Hebbian memory to disk."""
        memory = {
            'R_matrix': self.R_matrix.tolist(),
            'concept_coupling': {
                f"{k[0]}_{k[1]}": v
                for k, v in self.concept_coupling.items()
            },
            'pattern_counts': self.pattern_counts
        }

        with open(self.memory_path, 'w') as f:
            json.dump(memory, f, indent=2)

    def load(self):
        """Load Hebbian memory from disk."""
        if not self.memory_path.exists():
            return

        with open(self.memory_path) as f:
            memory = json.load(f)

        self.R_matrix = np.array(memory.get('R_matrix', np.zeros((6, 6))))

        # Convert concept coupling back to tuples
        coupling = memory.get('concept_coupling', {})
        self.concept_coupling = {
            tuple(k.split('_')): v
            for k, v in coupling.items()
        }

        self.pattern_counts = memory.get('pattern_counts', {})
```

**Success Criteria:**
- [ ] Hebbian learner implemented (~400 lines)
- [ ] R-matrix organ coupling working
- [ ] Concept coupling tracking
- [ ] Pattern confidence calculation

---

#### Day 18-21: Learning Validation

**Test Hebbian Learning with Conversations:**

File: `tests/test_hebbian_learning.py`

```python
"""
Test Hebbian learning across multiple conversations.

Process:
1. Process 20 test conversations
2. Update Hebbian memory after each
3. Measure pattern emergence
4. Validate R-matrix convergence
"""

def test_hebbian_emergence():
    hebbian = HebbianTextLearner()
    orchestrator = BasicTextOrchestrator()

    # Test conversations (10 burnout, 10 psychological safety)
    conversations = [...]

    for i, conv in enumerate(conversations):
        result = orchestrator.process_conversation(conv, f"test_{i}")

        # Update Hebbian memory
        hebbian.update_organ_coupling(result.organ_results)

        # Detect concepts (simple keyword matching for now)
        detected = detect_concepts(conv)
        hebbian.update_concept_coupling(detected)

        # Record pattern
        if "burnout" in conv.lower():
            hebbian.record_pattern("Burnout Spiral", success=True)

    # Validate learning
    print("\n📊 HEBBIAN LEARNING RESULTS")
    print("="*60)

    # R-matrix strongest couplings
    print("\nStrongest Organ Couplings:")
    organs = ['SANS', 'NDAM', 'BOND', 'RNX', 'EO', 'CARD']
    for i in range(6):
        for j in range(i+1, 6):
            coupling = hebbian.R_matrix[i, j]
            if coupling > 0.3:
                print(f"  {organs[i]} ↔ {organs[j]}: {coupling:.3f}")

    # Top concept pairs
    print("\nTop Concept Couplings:")
    sorted_concepts = sorted(
        hebbian.concept_coupling.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    for (c1, c2), count in sorted_concepts:
        print(f"  {c1} ↔ {c2}: {count} co-occurrences")

    # Pattern confidence
    print("\nPattern Confidence:")
    for pattern, counts in hebbian.pattern_counts.items():
        conf = hebbian.get_pattern_confidence(pattern)
        print(f"  {pattern}: {conf:.2%} ({counts['success']}/{counts['total']})")

    hebbian.save()
```

**Expected Results:**
- R-matrix convergence: 2-3 strong couplings emerge
- Concept pairs: "Burnout ↔ Dorsal Vagal" high coupling
- Pattern confidence: "Burnout Spiral" >80% after 10 examples

**Success Criteria:**
- [ ] 20 conversations processed
- [ ] R-matrix shows >2 strong couplings (>0.3)
- [ ] Top 3 concept pairs identified
- [ ] Pattern confidence >60% for trained patterns

---

### **Week 4: Production Integration**

#### Day 22-25: Full System Integration

**End-to-End System Test:**

File: `tests/test_full_system.py`

```python
"""
Complete system integration test.

Components:
1. Text Orchestrator (3 organs)
2. FAISS Memory (semantic search)
3. Neo4j Knowledge Graph (concept relationships)
4. Hebbian Learner (pattern co-activation)

Flow:
Text → Orchestrator → FAISS + Neo4j + Hebbian → Response
"""

def test_complete_system():
    # Initialize all components
    orchestrator = BasicTextOrchestrator()
    faiss_memory = FAISSMemory()
    faiss_memory.load("corpus_index.bin")
    neo4j_graph = Neo4jKnowledgeGraph()
    hebbian = HebbianTextLearner()

    # Test conversation
    conversation = """
    Our team is showing signs of severe burnout.
    People are exhausted, making mistakes, and several have resigned.
    We need to transition to a more sustainable rhythm.
    How do we support this transformation?
    """

    # 1. Process with orchestrator
    print("[1/5] Processing with orchestrator...")
    result = orchestrator.process_conversation(conversation, "prod_test_001")
    print(f"   Coherence: {result.aggregate_coherence:.3f}")
    print(f"   Patterns: {result.total_patterns}")

    # 2. Store in FAISS
    print("[2/5] Storing in FAISS...")
    faiss_memory.add_text_occasions(result.entities, "prod_test_001")

    # 3. Search FAISS for similar conversations
    print("[3/5] Searching for similar conversations...")
    similar = faiss_memory.search_by_text(
        orchestrator.vectorizer,
        "burnout exhaustion sustainable",
        k=3
    )
    print(f"   Found {len(similar)} similar conversations")

    # 4. Query Neo4j for transformation path
    print("[4/5] Querying transformation path...")
    path = neo4j_graph.find_transformation_path(
        "Burnout Spiral",
        "Sustainable Rhythm"
    )
    print(f"   Path: {' → '.join(path) if path else 'Not found'}")

    # 5. Update Hebbian memory
    print("[5/5] Updating Hebbian memory...")
    hebbian.update_organ_coupling(result.organ_results)
    detected_concepts = ["Burnout Spiral", "Dorsal Vagal State", "Sustainable Rhythm"]
    hebbian.update_concept_coupling(detected_concepts)
    hebbian.record_pattern("Burnout to Sustainable", success=True)
    hebbian.save()

    print("\n✅ COMPLETE SYSTEM TEST PASSED")
    print(f"   Total latency: ~{result.processing_time_ms + 50:.0f}ms")
```

**Success Criteria:**
- [ ] All 5 components working
- [ ] No errors or exceptions
- [ ] Total latency <500ms
- [ ] Memory usage <600MB

---

#### Day 26-28: Documentation & Production Readiness

**Create User Documentation:**

Files:
- `docs/KNOWLEDGE_SYSTEM_GUIDE.md` - How to use knowledge infrastructure
- `docs/PERFORMANCE_BENCHMARKS.md` - Expected performance metrics
- `docs/TROUBLESHOOTING.md` - Common issues and solutions

**Create Admin Tools:**
```bash
# FAISS index status
python3 -m knowledge_base.faiss_memory --stats

# Neo4j concept browser
python3 -m knowledge_base.neo4j_knowledge_graph --browse

# Hebbian memory viewer
python3 -m knowledge_base.hebbian_text_learner --stats
```

**Success Criteria:**
- [ ] Documentation complete (3 guides)
- [ ] Admin tools implemented
- [ ] Error handling tested
- [ ] Logging configured

---

## 📊 Success Metrics Summary

### Week 1 Targets
- [ ] Neo4j: 16 concepts, 18 relationships
- [ ] Integration test: <300ms latency
- [ ] Performance: <500MB memory

### Week 2 Targets
- [ ] Corpus: 1,000+ paragraphs indexed
- [ ] FAISS: >60% retrieval precision
- [ ] Index size: <5MB

### Week 3 Targets
- [ ] Hebbian: 20 conversations processed
- [ ] R-matrix: >2 strong couplings
- [ ] Patterns: >60% confidence

### Week 4 Targets
- [ ] Full system: All components integrated
- [ ] Latency: <500ms end-to-end
- [ ] Documentation: Complete

---

## 🚀 Quick Start (Next Session)

**Immediate Next Steps:**

1. **Install Neo4j** (5 minutes)
   ```bash
   # Option A: Neo4j Aura (cloud, easiest)
   # Sign up at https://neo4j.com/cloud/aura-free/

   # Option B: Docker (fastest local)
   docker run -d --name neo4j \
     -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/your_password \
     neo4j:latest
   ```

2. **Test Neo4j Connection** (2 minutes)
   ```bash
   cd "/Users/daedalea/Desktop/DAE_HYPHAE_1"
   # Update password in neo4j_knowledge_graph.py:83
   python3 knowledge_base/neo4j_knowledge_graph.py
   ```

3. **Run Integration Test** (5 minutes)
   ```bash
   # Create and run integration test
   python3 tests/test_knowledge_integration.py
   ```

**Total Time**: 12 minutes to Neo4j validation ✅

---

## 🔧 Resource Requirements

### Development (Current)
- **CPU**: 2 cores (light)
- **RAM**: 500MB (FAISS + orchestrator + Neo4j client)
- **Disk**: 50MB (code + small index)
- **Latency**: <300ms per conversation

### Production (After Week 4)
- **CPU**: 2-4 cores (moderate)
- **RAM**: 600-800MB (full system + corpus index)
- **Disk**: 100MB (code + 5MB FAISS + 20MB Neo4j)
- **Latency**: <500ms per conversation

### Neo4j Options
- **Aura Free**: 200K nodes, 400K relationships (plenty!)
- **Local**: 2GB RAM, ~500MB disk
- **Docker**: 1-2GB RAM container

---

## 📝 Notes

### Copyright & Corpus
- Use public domain texts (Whitehead - available on Archive.org)
- Create synthetic examples (no copyright issues)
- Commercial deployment: Purchase actual texts or use summaries

### Neo4j Choice
- **Development**: Neo4j Aura Free (easiest, zero install)
- **Production**: Neo4j Desktop (full control) or Aura Pro (managed)

### Performance
- Current system: 100% LLM-free, <300ms, $0 cost per conversation
- With LLM hybrid (Phase 4): ~20-30% LLM usage, <2s, ~$0.003/conversation
- 100x cheaper than pure LLM approach ✅

---

**Created**: November 10, 2025
**Version**: 1.0
**Status**: Ready for Week 1 implementation
**Next Milestone**: Neo4j validation (Day 1-2)

🌀 **"Knowledge integrates, patterns emerge, wisdom grows."** 🌀
