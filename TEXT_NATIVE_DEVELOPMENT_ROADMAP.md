# 🌀 TEXT-NATIVE DEVELOPMENT ROADMAP
## DAE-GOV: Legacy-First Organism Architecture

**Decision**: Option A - Text-Native Parallel Track
**Timeline**: 100-135 hours (2.5-3.5 weeks full-time)
**Philosophy**: Build text-domain organism following proven universal organ pattern from DAE 3.0 AXO ARC
**Goal**: LLM-free operation with <20% fallback for novel patterns

---

## 🎯 STRATEGIC VISION

### **Why Text-Native?**

1. **95% Code Reuse Validated**: DAE_HYPHAE_0 → DAE_HYPHAE_1 clone proved architecture is domain-adaptable
2. **Text Deserves Native Architecture**: Forcing text through grid metaphors (sentence=row, chunk=col) loses discourse structure
3. **LLM-Free from Day 1**: Text-native design enables organism intelligence without LLM dependency
4. **Domain-Appropriate Design**: 85% build ahead anyway - do it right the first time

### **Core Architecture Decision**

**DO NOT** create `ActualOccasion.from_semantic_entity()` bridge.

**INSTEAD**: Create `TextOccasion` (text-native entity) following ActualOccasion pattern but optimized for text domain.

---

## 📊 UNIVERSAL ORGAN PATTERN (Extracted from 6 Modular Organs)

### **Key Insights from Legacy Analysis**

All 6 organs (NDAM, SANS, BOND, RNX, EO, CARD) follow identical architecture:

1. **Core Processing**: `process_symbolic_field(symbolic_field) -> OrganResult`
2. **Entity Prehension**: `_prehend_entities_with_affordances(entities, analysis, coherence, cycle)`
3. **V0 Field Extraction**: `_extract_v0_field(analysis, grid_shape) -> np.ndarray`
4. **Vector35D Enhancement**: `_apply_vector35d_intelligence(entities, patterns) -> Dict`
5. **Coherence Calculation**: `_calculate_organ_coherence(patterns, analysis) -> float`
6. **Pattern Detection**: `_detect_organ_patterns(features) -> List[Pattern]`

**Total Legacy Code**: 9,060 lines across 6 organs (average: 1,510 lines/organ)

**Text-Domain Adaptation**: Same 6 methods, different pattern detection logic

---

## 🏗️ PHASE 1: TEXT-NATIVE FOUNDATION (40-50 hours)

### **Week 1: Core Text Infrastructure**

#### **Milestone 1.1: TextOccasion Entity Class (8 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/transductive/text_occasion.py`

**Purpose**: Text-native equivalent of ActualOccasion (NOT a forced adaptation)

**Implementation**:
```python
@dataclass
class TextOccasion:
    """
    Text-native actual occasion following Whiteheadian process philosophy.

    Unlike ActualOccasion (grid-domain), TextOccasion is optimized for:
    - Sequential text processing (not spatial grid)
    - 384-dim semantic embeddings (not Vector35D)
    - Discourse coherence (not spatial pattern coherence)
    - Rhetorical structure (not geometric structure)
    """

    # ESSENTIAL CORE DATA
    chunk_id: str                      # "doc_5_para_3_sent_2_chunk_1"
    position: int                      # Sequential position in text (0, 1, 2, ...)
    text: str                          # Original text chunk (word/sentence/paragraph)

    # SEMANTIC REPRESENTATION
    embedding: np.ndarray              # 384-dim semantic vector (sentence-transformers)
    embedding_model: str = "all-MiniLM-L6-v2"  # Model used for embedding

    # TEXT-SPECIFIC STRUCTURE
    discourse_role: Optional[str] = None       # "claim", "evidence", "question", "response"
    rhetorical_position: Optional[str] = None  # "introduction", "body", "conclusion"
    paragraph_idx: Optional[int] = None        # Which paragraph this chunk belongs to
    sentence_idx: Optional[int] = None         # Which sentence within paragraph

    # SEMANTIC NEIGHBORS (replaces grid adjacency)
    semantic_neighbors: List[str] = field(default_factory=list)  # Similar chunk IDs (cosine > 0.7)
    discourse_neighbors: List[str] = field(default_factory=list) # Prev/next in sequence

    # UNIVERSAL PROCESS PHILOSOPHY FIELDS (from ActualOccasion)
    prehensions: Dict[str, Any] = field(default_factory=dict)    # Organ interpretations
    confidence: float = 1.0
    coherence: float = 0.0
    satisfaction_level: float = 0.0

    # LEARNING & STATE
    properties: Dict[str, Any] = field(default_factory=dict)

    # Methods (following ActualOccasion pattern)
    def prehend_with_affordances(self, organ_name: str, interpretation: str,
                                 affordances: List[Dict], cycle: int,
                                 organ_coherence: float):
        """Entity-native prehension (same as ActualOccasion)."""
        if organ_name not in self.prehensions:
            self.prehensions[organ_name] = {
                'interpretation': interpretation,
                'affordances': [],
                'cycles': [],
                'coherence_history': []
            }

        self.prehensions[organ_name]['affordances'].extend(affordances)
        self.prehensions[organ_name]['cycles'].append(cycle)
        self.prehensions[organ_name]['coherence_history'].append(organ_coherence)

    def get_semantic_similarity(self, other: 'TextOccasion') -> float:
        """Calculate cosine similarity with another text occasion."""
        from sklearn.metrics.pairwise import cosine_similarity
        sim = cosine_similarity(
            self.embedding.reshape(1, -1),
            other.embedding.reshape(1, -1)
        )[0, 0]
        return float(sim)

    def accumulate_affordance_salience(self, organism_state: Dict):
        """Accumulate salience on affordances during concrescence (same as ActualOccasion)."""
        for organ_name, organ_data in self.prehensions.items():
            for affordance in organ_data.get('affordances', []):
                if affordance.get('immature', True):
                    # Salience from organism state
                    base_salience = organism_state.get('satisfaction', 0.5)
                    energy_bonus = (1.0 - organism_state.get('energy', 0.5)) * 0.3
                    affordance['salience_score'] = base_salience + energy_bonus
                    affordance['prehension_count'] += 1

    def mature_affordances_to_propositions(self, v0_context: Dict) -> List[Dict]:
        """Mature affordances to propositions POST-CONVERGENCE (same as ActualOccasion)."""
        propositions = []

        for organ_name, organ_data in self.prehensions.items():
            for affordance in organ_data.get('affordances', []):
                if affordance.get('immature', True):
                    # Mature with V0 context
                    confidence = self._calculate_mature_confidence(affordance, v0_context)

                    proposition = {
                        'chunk_id': self.chunk_id,
                        'position': self.position,
                        'proposed_value': affordance['proposed_value'],
                        'confidence': confidence,
                        'lure_intensity': affordance['lure_intensity'],
                        'organ_name': organ_name,
                        'reasoning': affordance['reasoning'],
                        'mature': True
                    }
                    propositions.append(proposition)
                    affordance['immature'] = False

        return propositions

    def _calculate_mature_confidence(self, affordance: Dict, v0_context: Dict) -> float:
        """Calculate mature confidence with V0 context."""
        base = affordance.get('organ_specific_score', 0.5)
        salience_bonus = affordance.get('salience_score', 0.0) * 0.2
        energy_bonus = (1.0 - v0_context.get('final_energy', 0.5)) * 0.1
        satisfaction_bonus = v0_context.get('final_satisfaction', 0.5) * 0.2

        confidence = base + salience_bonus + energy_bonus + satisfaction_bonus
        return np.clip(confidence, 0.0, 1.0)
```

**Validation**:
- Create 10 TextOccasion entities from sample governance conversation
- Verify semantic similarity calculation
- Test prehension methods (empty affordances, no organs yet)

**Estimated**: 8 hours (includes testing)

---

#### **Milestone 1.2: SANS Organ (Text-Native) (10 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/sans/core/sans_text_core.py`

**Purpose**: Semantic similarity detection via 384-dim embeddings (NO LLM)

**Why SANS First?**:
- Simplest organ (pure cosine similarity)
- No keyword matching needed (uses embeddings directly)
- Proves text-native architecture works
- Foundation for other organs

**Implementation** (following universal organ pattern):

```python
class SANSTextCore(BaseModularOrgan):
    """
    SANS (Semantic Attention & Symbolic Intelligence) - Text Domain Adaptation.

    Grid Domain: Detects color clusters, positive salience for colored cells
    Text Domain: Detects semantic similarity, thematic resonance, conceptual affinity

    Pattern: process_symbolic_field() → detect_patterns() → prehend_entities() → extract_v0_field()
    """

    def __init__(self, config: SANSConfig):
        super().__init__(organ_type="SANS")
        self.config = config
        self.semantic_memory = {}  # Pattern signature → strength (exponential moving avg)

    def process_symbolic_field(self, symbolic_field: Dict[str, Any]) -> OrganResult:
        """
        Universal processing pattern adapted for text.

        Symbolic field for text:
        {
            'entities': [TextOccasion, TextOccasion, ...],
            'text_sequence': str,
            'coherence_context': {...},
            'cycle': int
        }
        """
        start_time = time.time()

        # Phase 1: Extract text entities
        entities = symbolic_field.get('entities', [])
        if not entities:
            return self._empty_result()

        # Phase 2: Detect semantic patterns (text-specific)
        semantic_patterns = self._detect_semantic_patterns(entities)

        # Phase 3: Calculate coherence (thematic consistency)
        coherence = self._calculate_semantic_coherence(semantic_patterns, entities)

        # Phase 4: Extract V0 semantic affinity field (1D text sequence)
        v0_semantic_field = self._extract_v0_semantic_affinity_field(
            semantic_patterns, len(entities)
        )

        # Phase 5: Entity-native prehension
        cycle = symbolic_field.get('cycle', 1)
        self._prehend_text_entities_with_semantic_affordances(
            entities, semantic_patterns, coherence, cycle
        )

        # Phase 6: Update semantic memory (exponential moving average)
        self._update_semantic_memory(semantic_patterns, coherence)

        processing_time = time.time() - start_time

        return OrganResult(
            coherence=coherence,
            patterns=semantic_patterns,
            v0_spatial_field=v0_semantic_field,  # 1D semantic affinity field
            v0_field_component="A_semantic",
            processing_time=processing_time,
            diagnostics={
                'num_entities': len(entities),
                'pattern_count': len(semantic_patterns),
                'memory_size': len(self.semantic_memory)
            }
        )

    def _detect_semantic_patterns(self, entities: List[TextOccasion]) -> List[Dict]:
        """
        Detect semantic patterns using 384-dim embeddings.

        Grid Domain: Color clusters (same color adjacent cells)
        Text Domain: Semantic clusters (high cosine similarity)
        """
        patterns = []

        # Pattern 1: Exact repetition (cosine > 0.95)
        repetitions = self._find_exact_repetitions(entities)
        patterns.extend(repetitions)

        # Pattern 2: Thematic resonance (cosine 0.75-0.95)
        themes = self._find_thematic_resonance(entities)
        patterns.extend(themes)

        # Pattern 3: Semantic echo (cosine 0.70-0.75)
        echoes = self._find_semantic_echoes(entities)
        patterns.extend(echoes)

        return patterns

    def _find_exact_repetitions(self, entities: List[TextOccasion]) -> List[Dict]:
        """Find nearly identical text chunks (cosine > 0.95)."""
        repetitions = []

        for i, entity_a in enumerate(entities):
            for j, entity_b in enumerate(entities[i+1:], start=i+1):
                similarity = entity_a.get_semantic_similarity(entity_b)

                if similarity > 0.95:
                    repetitions.append({
                        'type': 'exact_repetition',
                        'chunk_ids': [entity_a.chunk_id, entity_b.chunk_id],
                        'positions': [entity_a.position, entity_b.position],
                        'similarity': similarity,
                        'confidence': 1.5  # High confidence multiplier
                    })

        return repetitions

    def _find_thematic_resonance(self, entities: List[TextOccasion]) -> List[Dict]:
        """Find thematically related chunks (cosine 0.75-0.95)."""
        themes = []

        for i, entity_a in enumerate(entities):
            for j, entity_b in enumerate(entities[i+1:], start=i+1):
                similarity = entity_a.get_semantic_similarity(entity_b)

                if 0.75 <= similarity <= 0.95:
                    themes.append({
                        'type': 'thematic_resonance',
                        'chunk_ids': [entity_a.chunk_id, entity_b.chunk_id],
                        'positions': [entity_a.position, entity_b.position],
                        'similarity': similarity,
                        'confidence': 1.2
                    })

        return themes

    def _find_semantic_echoes(self, entities: List[TextOccasion]) -> List[Dict]:
        """Find semantically related chunks (cosine 0.70-0.75)."""
        echoes = []

        for i, entity_a in enumerate(entities):
            for j, entity_b in enumerate(entities[i+1:], start=i+1):
                similarity = entity_a.get_semantic_similarity(entity_b)

                if 0.70 <= similarity < 0.75:
                    echoes.append({
                        'type': 'semantic_echo',
                        'chunk_ids': [entity_a.chunk_id, entity_b.chunk_id],
                        'positions': [entity_a.position, entity_b.position],
                        'similarity': similarity,
                        'confidence': 1.1
                    })

        return echoes

    def _calculate_semantic_coherence(self, patterns: List[Dict],
                                      entities: List[TextOccasion]) -> float:
        """
        Calculate overall semantic coherence.

        Grid Domain: Spatial pattern uniformity
        Text Domain: Thematic consistency across chunks
        """
        if not patterns:
            return 0.3  # Baseline

        # Weight by pattern confidence
        weighted_sum = sum(p['confidence'] * p['similarity'] for p in patterns)
        total_weight = sum(p['confidence'] for p in patterns)

        if total_weight == 0:
            return 0.3

        coherence = weighted_sum / total_weight

        # Boost for pattern density (more patterns = more coherent)
        density_bonus = min(len(patterns) / len(entities), 0.3)

        return np.clip(coherence + density_bonus, 0.0, 1.0)

    def _extract_v0_semantic_affinity_field(self, patterns: List[Dict],
                                            seq_length: int) -> np.ndarray:
        """
        Extract 1D semantic affinity field (analogous to 2D spatial field).

        Grid Domain: 2D spatial affinity field (H×W)
        Text Domain: 1D sequential affinity field (seq_length,)
        """
        field = np.zeros(seq_length, dtype=np.float32)

        # Paint affinity values for chunks involved in patterns
        for pattern in patterns:
            positions = pattern.get('positions', [])
            similarity = pattern.get('similarity', 0.0)
            confidence = pattern.get('confidence', 1.0)

            for pos in positions:
                if 0 <= pos < seq_length:
                    field[pos] = max(field[pos], similarity * confidence)

        # Normalize to [0, 1]
        if field.max() > 0:
            field = field / field.max()

        # Ensure minimum variance (required for V0 felt propagation)
        field_std = np.std(field)
        if field_std < 0.05:
            noise = np.random.normal(0, 0.03, seq_length)
            field = field + noise
            field = np.clip(field, 0.0, 1.0)

        return field

    def _prehend_text_entities_with_semantic_affordances(self, entities: List[TextOccasion],
                                                         patterns: List[Dict],
                                                         coherence: float,
                                                         cycle: int):
        """
        Prehend text entities with semantic affordances (entity-native).

        Pattern: Same as spatial organs, but using text-specific logic.
        """
        prehended_count = 0

        for entity in entities:
            # Find patterns involving this entity
            entity_patterns = [p for p in patterns
                              if entity.chunk_id in p.get('chunk_ids', [])]

            if not entity_patterns:
                continue  # No semantic affordances for this entity

            # Calculate lure intensity (average similarity)
            lure_intensity = np.mean([p['similarity'] for p in entity_patterns])

            # Calculate organ-specific score (pattern strength)
            organ_score = np.mean([p['confidence'] for p in entity_patterns])

            # Create affordance
            affordance = {
                'proposed_value': entity.text,  # Text domain: propose text itself
                'lure_intensity': lure_intensity,
                'organ_specific_score': organ_score,
                'reasoning': f"SANS semantic affinity: {len(entity_patterns)} patterns",
                'cycle_generated': cycle,
                'immature': True,
                'salience_score': 0.0,
                'prehension_count': 0,
                'organ_type': 'SANS',
                'pattern_types': [p['type'] for p in entity_patterns]
            }

            # Prehend entity with affordance
            entity.prehend_with_affordances(
                organ_name='SANS',
                interpretation=f"Semantic affinity detected",
                affordances=[affordance],
                cycle=cycle,
                organ_coherence=coherence
            )

            prehended_count += 1

        print(f"   🌀 SANS: Prehended {prehended_count} text entities with semantic affordances")

    def _update_semantic_memory(self, patterns: List[Dict], coherence: float):
        """Update semantic memory with exponential moving average."""
        for pattern in patterns:
            pattern_key = f"{pattern['type']}_{pattern['similarity']:.2f}"

            if pattern_key in self.semantic_memory:
                # Exponential moving average (0.7 old, 0.3 new)
                self.semantic_memory[pattern_key] = (
                    0.7 * self.semantic_memory[pattern_key] + 0.3 * coherence
                )
            else:
                self.semantic_memory[pattern_key] = coherence

    def _empty_result(self) -> OrganResult:
        """Return empty result when no entities."""
        return OrganResult(
            coherence=0.0,
            patterns=[],
            v0_spatial_field=None,
            processing_time=0.0,
            success=False
        )

    # SVT compatibility (legacy interface)
    def transduce(self, svt_components: Dict) -> Dict:
        """Legacy SVT interface (no-op for text domain)."""
        return {}
```

**Validation**:
- Process 10 governance text chunks
- Verify semantic pattern detection (repetitions, themes, echoes)
- Confirm entity prehension (affordances stored)
- Check V0 field has std >= 0.05

**Estimated**: 10 hours (includes testing)

---

#### **Milestone 1.3: NDAM Organ (Text-Native) (8 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/ndam/core/ndam_text_core.py`

**Purpose**: Urgency detection via keyword matching (NO LLM)

**Pattern Detection**:
- Urgency keywords from config (40+ keywords)
- Keyword density calculation
- Constraint boundary detection (urgency vs. calm zones)

**Implementation** (following SANS pattern, but keyword-based):

```python
class NDAMTextCore(BaseModularOrgan):
    """
    NDAM (Negative Prehension & Constraint Modulation) - Text Domain.

    Grid Domain: Spatial constraint detection (color boundaries, exclusion patterns)
    Text Domain: Urgency detection (urgent vs. calm language boundaries)
    """

    def _detect_urgency_patterns(self, entities: List[TextOccasion]) -> List[Dict]:
        """Detect urgency patterns via keyword matching."""
        patterns = []

        # Load urgency keywords from config
        urgency_keywords = set(self.config.urgency_keywords)

        for entity in entities:
            text_lower = entity.text.lower()
            words = text_lower.split()

            # Count urgency keyword matches
            urgency_count = sum(1 for word in words if word in urgency_keywords)
            urgency_density = urgency_count / max(len(words), 1)

            if urgency_density > self.config.urgency_threshold:
                patterns.append({
                    'type': 'high_urgency',
                    'chunk_id': entity.chunk_id,
                    'position': entity.position,
                    'urgency_density': urgency_density,
                    'matched_keywords': [w for w in words if w in urgency_keywords],
                    'confidence': min(urgency_density * 2.0, 1.0)
                })

        # Detect urgency boundaries (transitions calm → urgent)
        for i in range(len(entities) - 1):
            current_urgency = self._calculate_chunk_urgency(entities[i])
            next_urgency = self._calculate_chunk_urgency(entities[i+1])

            if next_urgency - current_urgency > 0.4:  # Sharp increase
                patterns.append({
                    'type': 'urgency_boundary',
                    'chunk_ids': [entities[i].chunk_id, entities[i+1].chunk_id],
                    'positions': [entities[i].position, entities[i+1].position],
                    'urgency_delta': next_urgency - current_urgency,
                    'confidence': 1.3
                })

        return patterns
```

**Estimated**: 8 hours

---

#### **Milestone 1.4: BOND Organ (Text-Native) (10 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/bond/core/bond_text_core.py`

**Purpose**: IFS parts detection via keyword matching (NO LLM)

**Pattern Detection**:
- Manager keywords (40+): "should", "must", "plan", "control", etc.
- Firefighter keywords (30+): "crisis", "panic", "overwhelmed", etc.
- Exile keywords (30+): "worthless", "abandoned", "shame", etc.
- SELF keywords (30+): "calm", "clarity", "curiosity", "compassion", etc.

**SELF-Distance Calculation** (core BOND intelligence):
```python
def _calculate_self_distance(self, entity: TextOccasion) -> float:
    """
    Calculate distance from SELF-energy (0.0 = pure SELF, 1.0 = deep trauma).

    Ranges (from bond_config.py):
    - SELF-energy: 0.00-0.15
    - Manager: 0.15-0.35
    - Firefighter: 0.40-0.60
    - Exile: 0.50-0.75
    - Trauma: 0.75-1.00
    """
    text_lower = entity.text.lower()
    words = set(text_lower.split())

    # Count keyword matches
    self_count = len(words & set(self.config.self_energy_keywords))
    manager_count = len(words & set(self.config.manager_keywords))
    firefighter_count = len(words & set(self.config.firefighter_keywords))
    exile_count = len(words & set(self.config.exile_keywords))

    # Weighted distance calculation
    if self_count > 0:
        return 0.05  # Close to SELF
    elif manager_count > 0:
        return 0.25
    elif firefighter_count > 0:
        return 0.50
    elif exile_count > 0:
        return 0.65
    else:
        return 0.40  # Default (mixed state)
```

**Estimated**: 10 hours

---

#### **Milestone 1.5: Text Orchestrator (Basic - 3 Organs) (8 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/orchestration/text_orchestrator.py`

**Purpose**: Coordinate SANS + NDAM + BOND for text processing

**Flow**:
1. Text → TextOccasion entities
2. Process with 3 organs (SANS, NDAM, BOND)
3. Aggregate coherence
4. No reconstruction yet (just organ processing)

**Implementation**:
```python
class TextOrchestrator:
    """Orchestrate text processing with 3 organs (Phase 1)."""

    def __init__(self):
        self.sans = SANSTextCore(SANS_TEXT_CONFIG)
        self.ndam = NDAMTextCore(NDAM_TEXT_CONFIG)
        self.bond = BONDTextCore(BOND_TEXT_CONFIG)

    def process_conversation(self, conversation_text: str) -> Dict:
        """Process governance conversation with 3 organs."""

        # Step 1: Create TextOccasion entities
        entities = self._create_text_entities(conversation_text)

        # Step 2: Prepare symbolic field
        symbolic_field = {
            'entities': entities,
            'text_sequence': conversation_text,
            'cycle': 1
        }

        # Step 3: Process with 3 organs
        sans_result = self.sans.process_symbolic_field(symbolic_field)
        ndam_result = self.ndam.process_symbolic_field(symbolic_field)
        bond_result = self.bond.process_symbolic_field(symbolic_field)

        # Step 4: Aggregate coherence
        avg_coherence = np.mean([
            sans_result.coherence,
            ndam_result.coherence,
            bond_result.coherence
        ])

        return {
            'entities': entities,
            'organ_results': {
                'SANS': sans_result,
                'NDAM': ndam_result,
                'BOND': bond_result
            },
            'coherence': avg_coherence
        }

    def _create_text_entities(self, text: str) -> List[TextOccasion]:
        """Create TextOccasion entities from text (sentence chunking)."""
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim

        # Split into sentences
        sentences = text.split('. ')

        entities = []
        for i, sentence in enumerate(sentences):
            if not sentence.strip():
                continue

            # Generate embedding
            embedding = model.encode(sentence, convert_to_numpy=True)

            entity = TextOccasion(
                chunk_id=f"sent_{i}",
                position=i,
                text=sentence,
                embedding=embedding
            )
            entities.append(entity)

        return entities
```

**Validation**:
- Process 5 governance conversations
- Verify all 3 organs execute
- Check entity prehensions (all entities should have SANS, NDAM, BOND affordances)
- Measure coherence (should be 0.3-0.8 range)

**Estimated**: 8 hours

---

### **Phase 1 Deliverable** (Week 1 End)

✅ **Organism processes text with 3 organs, ZERO LLM calls**

**Capabilities**:
- Semantic similarity detection (SANS)
- Urgency detection (NDAM)
- IFS parts detection (BOND)
- Entity-native prehension
- V0 field extraction (1D text sequence)

**Validation Metrics**:
- 10 conversations processed
- All entities prehended by 3 organs
- No LLM API calls (100% local)
- Processing time < 5 seconds/conversation

---

## 🗄️ PHASE 2: KNOWLEDGE INFRASTRUCTURE (30-40 hours)

### **Week 2-3: Build Retrieval Systems**

#### **Milestone 2.1: FAISS Vector Store (12 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/faiss_store.py`

**Purpose**: Semantic search via 384-dim embeddings (NO LLM)

**Implementation**:
```python
import faiss
import numpy as np
import json
from pathlib import Path

class FAISSStore:
    """FAISS vector store for semantic search."""

    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.dimension = 384  # all-MiniLM-L6-v2
        self.index = None
        self.metadata = []

        self._initialize_index()

    def _initialize_index(self):
        """Initialize FAISS index (IndexFlatIP for cosine similarity)."""
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            metadata_path = self.index_path.parent / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    self.metadata = json.load(f)
        else:
            # Inner product index (for cosine similarity with L2-normalized vectors)
            self.index = faiss.IndexFlatIP(self.dimension)

    def add_vectors(self, embeddings: np.ndarray, metadata: List[Dict]):
        """Add vectors to index with L2 normalization."""
        # L2 normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def search(self, query_embedding: np.ndarray, k: int = 5,
               min_similarity: float = 0.70) -> List[Dict]:
        """Search for top-k similar vectors."""
        # L2 normalize query
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)

        # Search
        distances, indices = self.index.search(query_embedding, k)

        # Filter by minimum similarity
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if dist >= min_similarity and idx < len(self.metadata):
                results.append({
                    'similarity': float(dist),
                    'metadata': self.metadata[idx]
                })

        return results

    def save(self):
        """Persist index to disk."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))

        metadata_path = self.index_path.parent / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
```

**Ingestion Pipeline**:
```python
def ingest_conversations_to_faiss(conversations: List[str],
                                  faiss_store: FAISSStore):
    """Ingest processed conversations into FAISS."""
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings = []
    metadata = []

    for conv_id, conv_text in enumerate(conversations):
        sentences = conv_text.split('. ')

        for sent_id, sentence in enumerate(sentences):
            if not sentence.strip():
                continue

            # Generate embedding
            emb = model.encode(sentence, convert_to_numpy=True)

            embeddings.append(emb)
            metadata.append({
                'conversation_id': conv_id,
                'sentence_id': sent_id,
                'text': sentence
            })

    # Batch add
    embeddings_array = np.array(embeddings).astype('float32')
    faiss_store.add_vectors(embeddings_array, metadata)
    faiss_store.save()
```

**Estimated**: 12 hours

---

#### **Milestone 2.2: Neo4j Knowledge Graph (15 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/neo4j_graph.py`

**Purpose**: Relationship tracking (concepts, topics, reenactment patterns)

**Schema**:
```cypher
// Nodes
(:Concept {name: str, embedding: list[float]})
(:Topic {name: str, description: str})
(:Reenactment {pattern_type: str, confidence: float})
(:IFSPart {part_type: str})  // manager, firefighter, exile, SELF
(:PolyvagalState {state: str})  // ventral, sympathetic, dorsal

// Relationships
(:Concept)-[:RELATES_TO {strength: float}]->(:Concept)
(:Topic)-[:HAS_PATTERN]->(:Reenactment)
(:IFSPart)-[:ACTIVATES {urgency: float}]->(:PolyvagalState)
(:Concept)-[:BELONGS_TO]->(:Topic)
```

**Implementation**:
```python
from neo4j import GraphDatabase

class Neo4jGraph:
    """Neo4j knowledge graph for concept relationships."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def add_concept(self, name: str, embedding: List[float]):
        """Add concept node."""
        with self.driver.session() as session:
            session.run(
                "MERGE (c:Concept {name: $name}) "
                "SET c.embedding = $embedding",
                name=name, embedding=embedding
            )

    def add_relationship(self, concept_a: str, concept_b: str, strength: float):
        """Add RELATES_TO relationship."""
        with self.driver.session() as session:
            session.run(
                "MATCH (a:Concept {name: $concept_a}) "
                "MATCH (b:Concept {name: $concept_b}) "
                "MERGE (a)-[r:RELATES_TO]->(b) "
                "SET r.strength = $strength",
                concept_a=concept_a, concept_b=concept_b, strength=strength
            )

    def find_related_concepts(self, concept: str, min_strength: float = 0.65) -> List[Dict]:
        """Find related concepts via graph traversal."""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Concept {name: $concept})-[r:RELATES_TO]->(related:Concept) "
                "WHERE r.strength >= $min_strength "
                "RETURN related.name AS name, r.strength AS strength "
                "ORDER BY r.strength DESC",
                concept=concept, min_strength=min_strength
            )
            return [dict(record) for record in result]
```

**Estimated**: 15 hours (includes Docker setup, schema design, testing)

---

#### **Milestone 2.3: Hebbian Learning for Text (8 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/orchestration/v0/hebbian/text_hebbian_memory.py`

**Purpose**: Learn concept→concept co-activation (R-matrix coupling)

**Adaptation from Grid Domain**:
- Grid: value mappings (0→3, 1→4)
- Text: concept→concept mappings ("urgency"→"firefighter", "calm"→"SELF")

**Implementation**:
```python
class TextHebbianMemory:
    """Hebbian learning for text domain (concept co-activation)."""

    def __init__(self, memory_path: Path):
        self.memory_path = memory_path
        self.concept_coactivations = {}  # (concept_a, concept_b) → strength
        self.reinforcement_rate = 0.05  # η
        self.decay_rate = 0.01  # δ

        self._load_memory()

    def update_coactivation(self, concept_a: str, concept_b: str,
                           confidence: float):
        """Update concept co-activation strength (Hebbian learning)."""
        key = tuple(sorted([concept_a, concept_b]))

        if key in self.concept_coactivations:
            # Reinforce: old_strength + η * confidence
            self.concept_coactivations[key] += self.reinforcement_rate * confidence
        else:
            # Initialize
            self.concept_coactivations[key] = confidence * 0.5

        # Clip to [0, 1]
        self.concept_coactivations[key] = np.clip(
            self.concept_coactivations[key], 0.0, 1.0
        )

    def decay_all(self):
        """Apply decay to all patterns (prevent overfitting)."""
        for key in self.concept_coactivations:
            self.concept_coactivations[key] *= (1.0 - self.decay_rate)

    def get_coactivation(self, concept_a: str, concept_b: str) -> float:
        """Retrieve co-activation strength."""
        key = tuple(sorted([concept_a, concept_b]))
        return self.concept_coactivations.get(key, 0.0)

    def save(self):
        """Persist to disk."""
        with open(self.memory_path, 'w') as f:
            json.dump({
                'coactivations': {
                    f"{k[0]}|{k[1]}": v
                    for k, v in self.concept_coactivations.items()
                }
            }, f, indent=2)
```

**Estimated**: 8 hours

---

### **Phase 2 Deliverable** (Week 2-3 End)

✅ **Organism learns from conversations WITHOUT LLM**

**Capabilities**:
- FAISS semantic search (top-K retrieval)
- Neo4j concept relationships (graph traversal)
- Hebbian concept co-activation learning

**Validation Metrics**:
- 100 conversations ingested to FAISS
- 50+ concept relationships in Neo4j
- Hebbian memory: 200+ concept pairs

---

## 🧠 PHASE 3: ADVANCED ORGANS (20-30 hours)

### **Week 3-4: Complete Organism**

#### **Milestone 3.1: RNX Organ (4-Layer Reenactment Detection) (12 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/rnx/core/rnx_text_core.py`

**Purpose**: Trauma reenactment detection with LLM reduction strategy

**4-Layer Detection** (from rnx_config.py):
1. **Layer 1 (Hebbian)**: Learned reenactment patterns (confidence > 0.80)
2. **Layer 2 (Template)**: Predefined 25+ patterns (confidence > 0.70)
3. **Layer 3 (Neo4j)**: Graph relationship detection (confidence > 0.65)
4. **Layer 4 (FAISS)**: Historical corpus similarity (confidence > 0.60)
5. **LLM Fallback**: Only for novel patterns (target: <20%)

**Implementation**:
```python
class RNXTextCore(BaseModularOrgan):
    """RNX (Trauma Reenactment Detection) - Text Domain with 4-Layer Strategy."""

    def __init__(self, config: RNXConfig, faiss_store: FAISSStore,
                 neo4j_graph: Neo4jGraph, hebbian_memory: TextHebbianMemory):
        super().__init__(organ_type="RNX")
        self.config = config
        self.faiss_store = faiss_store
        self.neo4j_graph = neo4j_graph
        self.hebbian_memory = hebbian_memory

        # LLM reduction tracking
        self.total_detections = 0
        self.llm_fallback_count = 0

    def _detect_reenactment_patterns(self, entities: List[TextOccasion]) -> List[Dict]:
        """4-layer reenactment detection strategy."""
        patterns = []

        for entity in entities:
            # Try each layer in order (highest confidence first)

            # Layer 1: Hebbian memory (learned patterns)
            if self.config.layer1_hebbian_enabled:
                hebbian_match = self._check_hebbian_patterns(entity)
                if hebbian_match and hebbian_match['confidence'] > 0.80:
                    patterns.append(hebbian_match)
                    self.total_detections += 1
                    continue  # Found with high confidence, skip other layers

            # Layer 2: Template matching (predefined patterns)
            if self.config.layer2_template_enabled:
                template_match = self._check_template_patterns(entity)
                if template_match and template_match['confidence'] > 0.70:
                    patterns.append(template_match)
                    self.total_detections += 1
                    continue

            # Layer 3: Neo4j graph (relationship-based)
            if self.config.layer3_graph_enabled:
                graph_match = self._check_neo4j_patterns(entity)
                if graph_match and graph_match['confidence'] > 0.65:
                    patterns.append(graph_match)
                    self.total_detections += 1
                    continue

            # Layer 4: FAISS similarity (historical corpus)
            if self.config.layer4_faiss_enabled:
                faiss_match = self._check_faiss_patterns(entity)
                if faiss_match and faiss_match['confidence'] > 0.60:
                    patterns.append(faiss_match)
                    self.total_detections += 1
                    continue

            # LLM Fallback: Novel pattern (NOT IMPLEMENTED YET - Phase 5)
            # For now, mark as "novel" and skip
            self.llm_fallback_count += 1

        return patterns

    def _check_hebbian_patterns(self, entity: TextOccasion) -> Optional[Dict]:
        """Layer 1: Check learned Hebbian patterns."""
        # Check if any learned concept pairs appear in text
        text_lower = entity.text.lower()
        words = set(text_lower.split())

        for (concept_a, concept_b), strength in self.hebbian_memory.concept_coactivations.items():
            if concept_a in words and concept_b in words:
                return {
                    'type': 'reenactment_hebbian',
                    'pattern': f"{concept_a}_{concept_b}",
                    'confidence': strength,
                    'layer': 'hebbian',
                    'chunk_id': entity.chunk_id
                }

        return None

    def _check_template_patterns(self, entity: TextOccasion) -> Optional[Dict]:
        """Layer 2: Check predefined reenactment templates."""
        text_lower = entity.text.lower()

        # Check each template pattern from config
        for template in self.config.reenactment_templates:
            # Simple keyword matching (can be enhanced with regex)
            if template.replace('_', ' ') in text_lower:
                return {
                    'type': 'reenactment_template',
                    'pattern': template,
                    'confidence': 0.75,  # Fixed confidence for templates
                    'layer': 'template',
                    'chunk_id': entity.chunk_id
                }

        return None

    def _check_neo4j_patterns(self, entity: TextOccasion) -> Optional[Dict]:
        """Layer 3: Check Neo4j graph relationships."""
        # Extract key concepts from entity
        concepts = self._extract_concepts(entity.text)

        for concept in concepts:
            # Query Neo4j for reenactment relationships
            related = self.neo4j_graph.find_related_concepts(concept, min_strength=0.65)

            for rel in related:
                if 'reenactment' in rel['name'].lower():
                    return {
                        'type': 'reenactment_graph',
                        'pattern': f"{concept}_{rel['name']}",
                        'confidence': rel['strength'],
                        'layer': 'neo4j',
                        'chunk_id': entity.chunk_id
                    }

        return None

    def _check_faiss_patterns(self, entity: TextOccasion) -> Optional[Dict]:
        """Layer 4: Check FAISS historical similarity."""
        # Search FAISS for similar historical conversations
        results = self.faiss_store.search(entity.embedding, k=3, min_similarity=0.70)

        for result in results:
            # Check if similar conversation had reenactment pattern
            if result['metadata'].get('reenactment_detected'):
                return {
                    'type': 'reenactment_faiss',
                    'pattern': result['metadata'].get('reenactment_type', 'unknown'),
                    'confidence': result['similarity'],
                    'layer': 'faiss',
                    'chunk_id': entity.chunk_id
                }

        return None

    def get_llm_fallback_rate(self) -> float:
        """Calculate current LLM fallback rate."""
        if self.total_detections == 0:
            return 0.0
        return self.llm_fallback_count / self.total_detections
```

**Estimated**: 12 hours

---

#### **Milestone 3.2: EO Organ (Polyvagal State Detection) (8 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/eo/core/eo_text_core.py`

**Purpose**: Polyvagal state detection via keyword matching

**Pattern Detection**:
- Ventral vagal keywords (40+): "safe", "calm", "grounded", "connected"
- Sympathetic keywords (40+): "urgent", "crisis", "panic", "fight"
- Dorsal vagal keywords (40+): "numb", "frozen", "shutdown", "collapse"

**SELF-Distance Modifier** (from eo_config.py):
```python
def _apply_polyvagal_modifier(self, base_self_distance: float,
                              polyvagal_state: str) -> float:
    """Apply polyvagal modifier to SELF-distance."""
    modifiers = {
        'ventral_vagal': 0.0,    # No distance (ventral IS SELF)
        'sympathetic': +0.3,     # Moderate distance
        'dorsal_vagal': +0.5     # High distance (shutdown)
    }

    modifier = modifiers.get(polyvagal_state, 0.0)
    return np.clip(base_self_distance + modifier, 0.0, 1.0)
```

**Estimated**: 8 hours

---

#### **Milestone 3.3: CARD Organ (Response Scaling) (8 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/card/core/card_text_core.py`

**Purpose**: Calibrate response depth based on polyvagal state + SELF-distance

**Response Calibration** (from card_config.py):
```python
def _determine_response_scale(self, polyvagal_state: str,
                              self_distance: float,
                              urgency_level: str) -> str:
    """Determine appropriate response scale."""

    # Polyvagal state dominates (weight: 0.40)
    if polyvagal_state == 'ventral_vagal':
        return 'detailed'  # 600 words
    elif polyvagal_state == 'sympathetic':
        return 'brief'  # 150 words
    elif polyvagal_state == 'dorsal_vagal':
        return 'minimal'  # 50 words

    # SELF-distance modulates (weight: 0.30)
    if self_distance < 0.15:
        return 'comprehensive'  # 1000 words (SELF-led)
    elif self_distance > 0.70:
        return 'minimal'  # Trauma (gentle, spacious)

    # Urgency constrains (weight: 0.20)
    if urgency_level == 'extreme':
        return 'minimal'
    elif urgency_level == 'high':
        return 'brief'

    # Default
    return 'moderate'  # 300 words
```

**Estimated**: 8 hours

---

### **Phase 3 Deliverable** (Week 3-4 End)

✅ **Full 6-organ organism, LLM-free operation with <20% fallback**

**Capabilities**:
- Semantic similarity (SANS)
- Urgency detection (NDAM)
- IFS parts detection (BOND)
- Trauma reenactment detection (RNX) - 4-layer strategy
- Polyvagal state detection (EO)
- Response scaling (CARD)

**Validation Metrics**:
- 50 conversations processed
- RNX LLM fallback rate < 25% (target: <20% Week 12)
- All entities prehended by 6 organs
- Response scaling matches polyvagal state

---

## 🔀 PHASE 4: LLM HYBRID ROUTER (10-15 hours)

### **Week 4: Graceful LLM Integration**

#### **Milestone 4.1: Confidence-Based Routing (6 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/llm_hybrid/hybrid_router.py`

**Purpose**: Route to organism vs. LLM based on confidence

**Implementation**:
```python
class HybridRouter:
    """Route to organism (LLM-free) vs. LLM based on confidence."""

    def __init__(self, text_orchestrator: TextOrchestrator,
                 llm_client: Optional[Any] = None):
        self.orchestrator = text_orchestrator
        self.llm_client = llm_client

        # Routing thresholds
        self.high_confidence_threshold = 0.85  # Pure organism
        self.low_confidence_threshold = 0.60   # Pure LLM

    def route_query(self, query: str) -> Dict:
        """Route query to organism vs. LLM."""

        # Step 1: Process with organism
        organism_result = self.orchestrator.process_conversation(query)
        organism_confidence = organism_result['coherence']

        # Step 2: Route based on confidence
        if organism_confidence >= self.high_confidence_threshold:
            # High confidence → pure organism response
            return {
                'source': 'organism',
                'confidence': organism_confidence,
                'response': self._generate_organism_response(organism_result),
                'llm_used': False
            }

        elif organism_confidence >= self.low_confidence_threshold:
            # Medium confidence → hybrid (organism retrieval + LLM synthesis)
            return {
                'source': 'hybrid',
                'confidence': organism_confidence,
                'response': self._generate_hybrid_response(organism_result, query),
                'llm_used': True
            }

        else:
            # Low confidence → LLM primary with organism context
            return {
                'source': 'llm',
                'confidence': organism_confidence,
                'response': self._generate_llm_response(organism_result, query),
                'llm_used': True
            }

    def _generate_organism_response(self, organism_result: Dict) -> str:
        """Generate response using ONLY organism intelligence."""

        # Extract key insights from organs
        sans_patterns = organism_result['organ_results']['SANS'].patterns
        ndam_patterns = organism_result['organ_results']['NDAM'].patterns
        bond_patterns = organism_result['organ_results']['BOND'].patterns
        rnx_patterns = organism_result['organ_results']['RNX'].patterns
        eo_patterns = organism_result['organ_results']['EO'].patterns
        card_result = organism_result['organ_results']['CARD']

        # Determine response scale (from CARD)
        response_scale = card_result.patterns[0]['response_scale']  # 'minimal', 'brief', 'moderate', 'detailed', 'comprehensive'

        # Construct response from organism intelligence
        response = f"[Organism Response - {response_scale}]\n\n"

        # Add polyvagal state context (from EO)
        polyvagal_state = eo_patterns[0]['state'] if eo_patterns else 'unknown'
        response += f"Polyvagal State Detected: {polyvagal_state}\n\n"

        # Add IFS parts context (from BOND)
        if bond_patterns:
            parts = [p['part_type'] for p in bond_patterns]
            response += f"IFS Parts Present: {', '.join(parts)}\n\n"

        # Add reenactment detection (from RNX)
        if rnx_patterns:
            reenactment = rnx_patterns[0]['pattern']
            response += f"⚠️ Reenactment Pattern Detected: {reenactment}\n\n"

        # Template-based response (organism intelligence, no LLM)
        response += self._apply_response_template(
            polyvagal_state, parts, response_scale
        )

        return response

    def _generate_hybrid_response(self, organism_result: Dict, query: str) -> str:
        """Hybrid: organism retrieval + LLM synthesis."""

        if not self.llm_client:
            return self._generate_organism_response(organism_result)

        # Construct prompt with organism context
        context = self._format_organism_context(organism_result)

        prompt = f"""You are a trauma-informed organizational consultant.

ORGANISM INTELLIGENCE (grounding context):
{context}

USER QUERY:
{query}

Respond in a trauma-informed way, integrating the organism's intelligence."""

        # LLM synthesis
        llm_response = self.llm_client.generate(prompt)

        return llm_response

    def _generate_llm_response(self, organism_result: Dict, query: str) -> str:
        """LLM primary with organism grounding."""

        if not self.llm_client:
            return self._generate_organism_response(organism_result)

        context = self._format_organism_context(organism_result)

        prompt = f"""You are a trauma-informed organizational consultant.

ORGANISM CONTEXT (low confidence, use as supplemental):
{context}

USER QUERY:
{query}

Respond in a trauma-informed way."""

        return self.llm_client.generate(prompt)
```

**Estimated**: 6 hours

---

#### **Milestone 4.2: Response Synthesis Layer (6 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/llm_hybrid/response_synthesis.py`

**Purpose**: Format organism intelligence for LLM consumption

**Estimated**: 6 hours

---

#### **Milestone 4.3: Logging & Monitoring (3 hours)**

**File**: `/Users/daedalea/Desktop/DAE_HYPHAE_1/llm_hybrid/usage_monitor.py`

**Purpose**: Track LLM usage rate over time

**Metrics**:
- LLM usage rate (target: <25% Week 1 → <15% Week 12)
- Organism confidence distribution
- Routing decision counts

**Estimated**: 3 hours

---

### **Phase 4 Deliverable** (Week 4 End)

✅ **Hybrid system: defaults to organism, uses LLM gracefully**

**Capabilities**:
- Confidence-based routing (organism vs. LLM)
- Pure organism responses (confidence > 0.85)
- Hybrid responses (confidence 0.60-0.85)
- LLM fallback (confidence < 0.60)

**Validation Metrics**:
- 100 test queries routed
- LLM usage rate: ~50% (Week 4 baseline)
- Target trajectory: 50% → 35% → 25% (Weeks 4 → 8 → 12)

---

## 📊 COMPLETE TIMELINE & RESOURCE ALLOCATION

### **Summary by Phase**

| Phase | Focus | Hours | Weeks | Key Deliverables |
|-------|-------|-------|-------|------------------|
| **Phase 1** | Text-Native Foundation | 40-50 | 1-2 | TextOccasion + 3 organs (SANS, NDAM, BOND) |
| **Phase 2** | Knowledge Infrastructure | 30-40 | 2-3 | FAISS + Neo4j + Hebbian learning |
| **Phase 3** | Advanced Organs | 20-30 | 3-4 | RNX (4-layer) + EO + CARD |
| **Phase 4** | LLM Hybrid Router | 10-15 | 4 | Confidence-based routing + monitoring |
| **TOTAL** | **Full System** | **100-135** | **2.5-3.5** | **LLM-free organism with <20% fallback** |

---

### **Weekly Milestones**

**Week 1** (40-50 hours):
- ✅ Day 1-2: TextOccasion entity class (8h)
- ✅ Day 2-3: SANS organ (10h)
- ✅ Day 3-4: NDAM organ (8h)
- ✅ Day 4-5: BOND organ (10h)
- ✅ Day 5: Text orchestrator (8h)
- **Deliverable**: 3-organ text processor, 100% LLM-free

**Week 2** (30-40 hours):
- ✅ Day 1-3: FAISS vector store (12h)
- ✅ Day 3-5: Neo4j knowledge graph (15h)
- ✅ Day 5: Hebbian text learning (8h)
- **Deliverable**: Knowledge infrastructure, learning from conversations

**Week 3** (20-30 hours):
- ✅ Day 1-3: RNX organ (4-layer detection) (12h)
- ✅ Day 3-4: EO organ (polyvagal) (8h)
- ✅ Day 4-5: CARD organ (response scaling) (8h)
- **Deliverable**: 6-organ organism, <25% LLM fallback

**Week 4** (10-15 hours):
- ✅ Day 1-2: Hybrid router (6h)
- ✅ Day 2-3: Response synthesis (6h)
- ✅ Day 3: Monitoring (3h)
- **Deliverable**: Production-ready hybrid system

---

## 🎯 SUCCESS CRITERIA

### **Technical Validation**

| Metric | Week 1 | Week 2 | Week 3 | Week 4 | Target |
|--------|--------|--------|--------|--------|--------|
| **Organ Count** | 3 | 3 | 6 | 6 | 6 organs |
| **LLM-Free Processing** | ✅ | ✅ | ✅ | ✅ | 100% |
| **FAISS Vectors** | 0 | 100+ | 500+ | 1000+ | 1000+ |
| **Neo4j Concepts** | 0 | 50+ | 150+ | 300+ | 300+ |
| **Hebbian Patterns** | 0 | 200+ | 500+ | 1000+ | 1000+ |
| **RNX LLM Fallback** | N/A | N/A | 50% | 40% | <25% Week 4 |
| **Organism Confidence** | 0.40 | 0.55 | 0.65 | 0.75 | 0.70+ |

---

### **Architectural Validation**

**Week 1**: Text-native architecture proves viable
- ✅ TextOccasion entities created without ActualOccasion bridge
- ✅ 3 organs process text without spatial metaphors
- ✅ Entity-native prehension works for text domain

**Week 2**: Knowledge infrastructure enables learning
- ✅ FAISS retrieves semantically similar conversations
- ✅ Neo4j tracks concept relationships
- ✅ Hebbian memory learns concept co-activations

**Week 3**: Organism intelligence matures
- ✅ RNX 4-layer strategy reduces LLM dependency
- ✅ EO + BOND + NDAM detect patterns without LLM
- ✅ CARD calibrates responses based on organism state

**Week 4**: Hybrid system production-ready
- ✅ Confidence-based routing works
- ✅ LLM enhances organism (not replaces)
- ✅ Monitoring tracks LLM usage reduction

---

## 🚀 NEXT SESSION STARTING POINT

### **Immediate Action (Hour 0-1)**

```bash
cd "/Users/daedalea/Desktop/DAE_HYPHAE_1"

# Create Phase 1 file structure
mkdir -p transductive
mkdir -p organs/modular/{sans,ndam,bond}/core

# Start with TextOccasion entity class
# File: transductive/text_occasion.py
```

**First Implementation**: `TextOccasion` class (8 hours)

**Validation Target**: Create 10 TextOccasion entities from sample governance text, verify semantic similarity calculation

---

## 📚 REFERENCE MATERIALS

### **Universal Organ Pattern** (from Legacy Analysis)

All text organs follow this architecture:

1. `process_symbolic_field(symbolic_field) -> OrganResult`
2. `_detect_organ_patterns(entities) -> List[Dict]`
3. `_calculate_organ_coherence(patterns, entities) -> float`
4. `_extract_v0_field(patterns, seq_length) -> np.ndarray`
5. `_prehend_text_entities_with_affordances(entities, patterns, coherence, cycle)`
6. `_update_organ_memory(patterns, coherence)`

### **Key Files to Reference**

From DAE 3.0 AXO ARC:
- `/organs/modular/sans/core/sans_core.py` - SANS spatial implementation (1,134 lines)
- `/organs/modular/ndam/core/ndam_core.py` - NDAM constraint detection (1,662 lines)
- `/organs/modular/bond/core/bond_core.py` - BOND spatial patterns (1,650 lines)
- `/organs/modular/rnx/core/rnx_core.py` - RNX temporal intelligence (1,895 lines)
- `/organs/modular/eo/core/eo_core.py` - EO archetypal patterns (1,524 lines)
- `/organs/modular/card/core/card_core.py` - CARD multi-scale analysis (1,195 lines)

From DAE_HYPHAE_1 (configs already created):
- `/organs/modular/sans/config/sans_config.py` - Text-domain config ready
- `/organs/modular/ndam/config/ndam_config.py` - 40+ urgency keywords
- `/organs/modular/bond/config/bond_config.py` - IFS parts keywords
- `/organs/modular/rnx/config/rnx_config.py` - 4-layer detection config
- `/organs/modular/eo/config/eo_config.py` - Polyvagal keywords
- `/organs/modular/card/config/card_config.py` - Response scaling ranges

---

## 🌀 FINAL REMARKS

### **Why This Will Work**

1. **Proven Architecture**: 95% code reuse from DAE 3.0 AXO ARC (9,060 lines, 6 organs, validated)
2. **Domain-Appropriate Design**: Text-native entities, not forced grid metaphors
3. **LLM-Free Foundation**: Organism intelligence from day 1, LLM as graceful enhancement
4. **Progressive Learning**: FAISS + Neo4j + Hebbian = knowledge accumulation without LLM
5. **Clear Reduction Strategy**: RNX 4-layer detection targets <20% LLM usage Week 24

### **The Bet**

**Hypothesis**: Text-domain organism with native architecture, 6 organs, and progressive learning will achieve LLM-free operation with <20% fallback for novel patterns.

**Timeline**: 100-135 hours (2.5-3.5 weeks full-time)

**Success Metric**: 80%+ of governance queries answered by organism alone, LLM used only for novel patterns and synthesis

---

**🌀 Let's build text intelligence that emerges from organism learning, not LLM dependency. 🌀**

**Ready to start with TextOccasion entity class?**
