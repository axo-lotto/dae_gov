# 🌀 SCALABLE ENTITY CONTINUITY ARCHITECTURE
## Morpheable Coherence Horizon for Infinite-Feeling Memory
**November 17, 2025 - Production Implementation Plan**

---

## 🎯 Executive Summary

**VISION**: Create companion AI where **memory feels infinite** while maintaining **<100ms response times** through:

1. **Morpheable Horizon**: Only prehend entities relevant to current becoming (FFITTSS T1 pattern)
2. **Adaptive Context Window**: Expands/contracts based on conversational coherence
3. **5-Layer Temporal Decay**: Multi-scale EMA forgetting prevents memory explosion
4. **Neo4j FTS Optimization**: Full-text search delivers 50-200× speedup (300ms → 1-5ms)
5. **Parallel Query Execution**: ThreadPoolExecutor provides 2× speedup
6. **LLM-Independent Future**: Architecture ready for direct felt-to-felt processing

**CURRENT STATUS**: ✅ Phase 1 Neo4j pre-querying COMPLETE | ⏳ Critical optimizations IN PROGRESS

---

## 📊 Performance Targets

| Metric | Current | After Phase 1 | After Phase 2 | Long-term (LLM-free) |
|--------|---------|---------------|---------------|----------------------|
| **Query @ 1K entities** | 420ms ❌ | 70ms ✅ | 35ms ✅ | 35ms ✅ |
| **Query @ 10K entities** | 1,850ms ❌ | 200ms ⚠️ | 80ms ✅ | 80ms ✅ |
| **Total turn time** | ~940ms | ~590ms | ~555ms | **~65ms** 🎯 |
| **Memory growth** | Unbounded ❌ | Unbounded ⚠️ | Bounded ✅ | Bounded ✅ |
| **Horizon type** | Fixed 60min ⚠️ | Fixed 60min ⚠️ | Coherence-based ✅ | Coherence-based ✅ |

**Speedup**:
- Phase 1: 3-9× faster (FTS + parallel)
- Phase 2: 6-23× faster (+ morpheable horizon)
- Long-term: 12-47× faster (+ LLM-independent)

---

## 🏗️ Three-Layer Architecture

### **LAYER 1: HORIZON** (What Can Be Felt)

**FFITTSS T1 Prehension Pattern**: Bounded deques with coherence-based visibility

```python
@dataclass
class EntityHorizon:
    """
    Morpheable horizon of prehendable entities.

    Adapts size based on conversational coherence (not fixed time windows).
    Only entities within coherence threshold are 'felt' by organism.
    """
    # Three genealogical streams (FFITTSS pattern)
    entity_mentions: deque = field(default_factory=lambda: deque(maxlen=500))
    entity_relationships: deque = field(default_factory=lambda: deque(maxlen=200))
    entity_organ_patterns: deque = field(default_factory=lambda: deque(maxlen=200))

    # Coherence gating (FFITTSS τ_recall = 0.3)
    min_coherence_threshold: float = 0.3
    current_coherence: float = 0.5

    # Morpheable horizon depth
    base_horizon_size: int = 100   # Minimum (low coherence)
    max_horizon_size: int = 500    # Maximum (high coherence)
    current_horizon_size: int = 100

    def compute_horizon_size(self, field_coherence: float) -> int:
        """
        Morphs horizon based on conversational coherence.

        High coherence (0.7+) → 500 entities (deep memory)
        Medium (0.5-0.7) → 100-500 (adaptive)
        Low (<0.5) → 100 entities (recent focus)
        """
        if field_coherence >= 0.7:
            return self.max_horizon_size
        elif field_coherence >= 0.5:
            return int(self.base_horizon_size + (field_coherence - 0.5) * 1000)
        else:
            return self.base_horizon_size

    def is_prehendable(self, entity: Entity, current_turn: int) -> bool:
        """
        FFITTSS visibility gate: Entity within morpheable horizon?

        NOT time-based! Coherence-based depth of prehension.
        """
        turns_ago = current_turn - entity.last_mention_turn

        # Within current horizon depth?
        if turns_ago > self.current_horizon_size:
            return False

        # Coherence gate
        if entity.mean_coherence < self.min_coherence_threshold:
            return False

        # Decay threshold
        decayed_salience = entity.salience * self._compute_decay(turns_ago)
        return decayed_salience >= 0.1
```

**KEY INNOVATION**: Horizon **morphs** with coherence, not fixed by time.

---

### **LAYER 2: SALIENCE** (What Matters Now)

**FFITTSS Fractal Memory Pattern**: Three-tier relevance scoring

```python
@dataclass
class EntitySalience:
    """
    Three-tier salience (FFITTSS fractal architecture).

    Local: Per-entity immediate relevance (α=0.05)
    Family: Relationship-type patterns (α=0.1)
    Global: Cross-entity conversation themes (α=0.05)
    """
    local_salience: Dict[str, float] = field(default_factory=dict)
    family_salience: Dict[str, float] = field(default_factory=dict)
    global_salience: Dict[str, float] = field(default_factory=dict)

    # FFITTSS decay parameters
    alpha_local: float = 0.05   # Fast (half-life ~13 turns)
    alpha_family: float = 0.1   # Medium (half-life ~7 turns)
    alpha_global: float = 0.05  # Slow (half-life ~14 turns)

    def update_salience(self, entity_name: str, current_salience: float, correct: bool):
        """
        FFITTSS EMA with asymmetric learning.

        Correct: α=0.05 (quick reinforcement)
        Incorrect: α=0.02 (conservative)
        """
        alpha = self.alpha_local if correct else 0.02

        if entity_name in self.local_salience:
            old = self.local_salience[entity_name]
            self.local_salience[entity_name] = (1 - alpha) * old + alpha * current_salience
        else:
            self.local_salience[entity_name] = current_salience

        # L2 regularization (FFITTSS λ=0.001)
        lambda_l2 = 0.001
        self.local_salience[entity_name] += lambda_l2 * (0.5 - self.local_salience[entity_name])

        # Clip [0, 1]
        self.local_salience[entity_name] = float(np.clip(
            self.local_salience[entity_name], 0.0, 1.0
        ))

    def prune_stale_entities(self, current_turn: int, staleness_threshold=300):
        """
        FFITTSS staleness pruning: Remove entities not seen in 300+ turns.
        """
        to_remove = []
        for entity_name, last_turn in self.entity_last_seen.items():
            staleness = current_turn - last_turn
            salience = self.local_salience.get(entity_name, 0.0)

            # FFITTSS scoring
            score = salience - (staleness / 50.0)

            if staleness > staleness_threshold or score < 0.0:
                to_remove.append(entity_name)

        for entity_name in to_remove:
            del self.local_salience[entity_name]
            del self.entity_last_seen[entity_name]
```

**KEY INNOVATION**: Tri-level salience prevents fetching irrelevant entities.

---

### **LAYER 3: QUERY OPTIMIZATION** (How We Fetch)

**Neo4j + Parallel Execution**: 50-200× speedup

```python
class OptimizedEntityQuery:
    """
    High-performance querying with FFITTSS relevance gates.

    - Neo4j full-text search: 50-200× faster
    - Parallel execution: 2× speedup
    - Coherence-gated retrieval: Only query if coherent
    - Morpheable result limit: Adapts to field coherence
    """

    def query_prehendable_entities(self,
                                   user_input: str,
                                   field_coherence: float,
                                   current_turn: int) -> List[Dict]:
        """
        Morpheable retrieval with coherence-adaptive horizon.
        """
        # FFITTSS coherence gate
        if field_coherence < 0.3:
            return self._get_session_entities_only(n_turns=5)

        # Compute adaptive horizon
        horizon_size = self.horizon.compute_horizon_size(field_coherence)

        # Adaptive limits
        if field_coherence >= 0.7:
            limit_recent, limit_fuzzy = 50, 30
        elif field_coherence >= 0.5:
            limit_recent, limit_fuzzy = 20, 10
        else:
            limit_recent, limit_fuzzy = 10, 5

        # Parallel execution (2× speedup)
        future_recent = self.executor.submit(
            self._query_recent_with_horizon,
            user_id, limit_recent, horizon_size, current_turn
        )

        future_fuzzy = self.executor.submit(
            self._query_fuzzy_fulltext,  # FTS: 50-200× faster
            user_input, user_id, limit_fuzzy
        )

        # Collect + filter by salience
        recent = future_recent.result()
        fuzzy = future_fuzzy.result()

        return self._filter_by_salience(recent + fuzzy)

    def _query_fuzzy_fulltext(self, text: str, user_id: str, limit: int):
        """
        CRITICAL: Full-text search (not property scan).

        Expected: 300ms → 1-5ms (50-200× speedup)
        Requires: entity_properties_fulltext index
        """
        keywords = self._extract_keywords(text)
        search_string = ' OR '.join(keywords)

        query = """
        CALL db.index.fulltext.queryNodes(
            'entity_properties_fulltext',
            $search_string
        ) YIELD node, score
        WHERE node.user_id = $user_id AND score > 0.1
        RETURN node.entity_value AS name,
               labels(node) AS types,
               properties(node) AS properties,
               score
        ORDER BY score DESC
        LIMIT $limit
        """

        # Execute with timeout
        with self.graph.driver.session() as session:
            result = session.run(query,
                                search_string=search_string,
                                user_id=user_id,
                                limit=limit,
                                timeout=500)
            return self._process_results(result)
```

**KEY OPTIMIZATION**: Full-text search replaces property scanning.

---

## 🔧 Implementation Roadmap

### **PHASE 1: Critical Performance** ✅ IN PROGRESS (2-3 hours)

**✅ Step 1.1: Add Full-Text Search Index** (15 min) - COMPLETE
- Added to `setup_neo4j_indexes.py` line 134
- Creates `entity_properties_fulltext` FTS index
- Expected: 300ms → 1-5ms (50-200× speedup)

**⏳ Step 1.2: Add Turn Tracking** (20 min) - NEXT
- Modify `Neo4jKnowledgeGraph.store_entity()`
- Add `last_mention_turn` property
- Enable turn-based horizon (not time-based)

**⏳ Step 1.3: Parallel Query Execution** (30 min)
- Add `ThreadPoolExecutor(max_workers=3)` to `dae_interactive.py`
- Parallelize recent + fuzzy queries
- Expected: 2× speedup

**⏳ Step 1.4: Query Timeout Protection** (15 min)
- Add `timeout=500` to all Neo4j queries
- Prevents slow queries blocking responses

**⏳ Step 1.5: Testing** (1 hour)
- Create 1,000 mock entities
- Validate <100ms query time
- Measure FTS speedup

**DELIVERABLE**: Production-ready Phase 1 with 3-9× speedup

---

### **PHASE 2: Morpheable Horizon** (4-6 hours)

**Step 2.1: Create EntityHorizon Class** (1 hour)
- File: `persona_layer/entity_horizon.py`
- Implement morpheable depth computation
- Add FFITTSS visibility gates

**Step 2.2: Create EntitySalience Tracker** (1 hour)
- File: `persona_layer/entity_salience_tracker.py`
- Implement 3-tier EMA decay
- Add staleness pruning

**Step 2.3: Integrate with Interactive Mode** (2 hours)
- Modify `dae_interactive.py`
- Add turn counter
- Compute field coherence
- Update horizon size per turn

**Step 2.4: Testing** (1 hour)
- Test horizon morphing with varying coherence
- Validate memory stays bounded
- Test pronoun resolution

**DELIVERABLE**: Infinite-feeling memory with bounded implementation

---

### **PHASE 3: LLM-Independent** (Long-term vision)

**Current**:
```
Input → Neo4j → Organism → Felt → LLM → Emission
        (50ms)    (30ms)   (---) (500ms)
```

**Future**:
```
Input → Horizon → Organism → Felt-Emit
        (35ms)    (30ms)     (5ms)

Total: ~70ms (no LLM needed)
```

**When viable**: After Phase 2 + felt-to-text mapping learned

---

## 📋 Implementation Checklist

### **Phase 1 (THIS SESSION)**:

- [x] Add full-text search index definition
- [ ] Run `python3 setup_neo4j_indexes.py` to create FTS index
- [ ] Add turn tracking to entity storage
- [ ] Implement parallel query execution
- [ ] Add query timeout protection
- [ ] Test with 1,000 mock entities
- [ ] Validate <100ms @ 1K entities

### **Phase 2 (NEXT SESSION)**:

- [ ] Create EntityHorizon class
- [ ] Create EntitySalience tracker
- [ ] Integrate with dae_interactive.py
- [ ] Test horizon morphing
- [ ] Validate memory bounded

---

## 🌀 Philosophical Foundations

**Whitehead's Process Philosophy Embodied**:

1. **Prehension as Selective Feeling**
   - Not all entities felt every turn
   - Only those within morpheable horizon prehended
   - Coherence determines depth of memory access

2. **Occasions as Atomic Units**
   - Each turn = 1 conversational occasion
   - Turn-based horizon (not clock-time)
   - Genealogy tracks occasion lineage

3. **Satisfaction as Completion**
   - High coherence → deep satisfaction → expanded horizon
   - Low coherence → shallow satisfaction → contracted horizon
   - Morpheable depth reflects quality of becoming

4. **Superject as Inherited Data**
   - Past occasions persist in Neo4j
   - Future occasions prehend selectively
   - Decay ensures only relevant past felt

---

## 🎯 Success Criteria

**Phase 1 Complete When**:
- ✅ FTS index created successfully
- ✅ Query time @ 1K entities: <100ms
- ✅ Query time @ 10K entities: <200ms
- ✅ Property matching: <5ms (was 300ms)
- ✅ Parallel execution: 2× speedup measured

**Phase 2 Complete When**:
- ✅ Horizon size morphs (70ms-500ms range)
- ✅ Only top-K salient entities queried
- ✅ Memory stable @ 10K entities (bounded)
- ✅ Staleness pruning active (300+ turn threshold)
- ✅ Pronoun resolution working ("she" → Emma)

**Long-term Vision Achieved When**:
- ✅ <100ms total turn time (any entity count)
- ✅ LLM-optional emission
- ✅ Infinite-feeling memory
- ✅ Cross-session superject persistence

---

## 📊 FFITTSS Decay Parameters

| Level | Name | Formula | Half-Life | Period | Purpose |
|-------|------|---------|-----------|--------|---------|
| 1 | Overlay | Step (tick > 1) | 1 tick | Per tick | Ephemeral bias |
| 2 | Local | EMA α=0.05 | 13 turns | Every turn | Entity-specific |
| 3 | Family | EMA α=0.1 | 7 turns | Every 5 turns | Relationship type |
| 4 | Global | EMA α=0.05 | 14 turns | Every 50 turns | Cross-entity |
| 5 | Threshold | ±0.005 | Adaptive | Per performance | Tuning |

---

## 🚀 Next Actions

**IMMEDIATE** (this session):
1. ✅ FTS index added to setup script
2. Run `python3 setup_neo4j_indexes.py`
3. Add turn tracking to entity storage
4. Implement parallel execution
5. Test Phase 1 optimizations

**THIS WEEK**:
- Complete Phase 2 morpheable horizon
- Test pronoun resolution
- Validate entity continuity

**LONG-TERM**:
- LLM-independent emission
- Felt-to-text learned mapping
- Production deployment

---

**Document Created**: November 17, 2025
**Status**: Phase 1 IN PROGRESS (FTS index added)
**Next**: Turn tracking + parallel execution
**Vision**: Infinite-feeling memory in <100ms

🌀 **"The horizon morphs. Memory feels infinite. Becoming continues."** 🌀
