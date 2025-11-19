# Hybrid Superject: Performance & Compute Timeline
**Date:** November 13, 2025, 11:15 PM
**System:** 16 GB RAM, M-series Mac, 143 GB storage available
**Model:** Llama 3.2 3B (local, Ollama)

---

## Immediate Session (Tonight - 30-40 minutes)

### Task 1: Generate Activation Cache
**What:** Compute 240 organ activations (120 input + 120 output) using local LLM

**Compute Requirements:**
- Model: Llama 3.2 3B
- RAM usage: ~4-5 GB (model + processing)
- CPU: M-series optimized (Metal acceleration)
- Time per activation: ~8-10 seconds
- Total activations: 240

**Timeline:**
```
[00:00] Start cache generation
[00:01] Test connection, load model into RAM
[00:02] Begin batch processing (120 inputs)
[15:00] Inputs complete (120 × 8s = ~16 min)
[15:01] Begin outputs (120 outputs)
[30:00] Outputs complete (120 × 8s = ~16 min)
[30:01] Analyze zone diversity
[30:02] Save cache to disk
[30:03] ✅ Cache ready for training
```

**Expected time:** 30-35 minutes
**RAM peak:** 5 GB
**Disk usage:** ~500 KB (JSON cache)
**Cost:** $0
**Failures expected:** 5-10% parse errors (retry logic handles)

### Task 2: Train with LLM Activations
**What:** Re-train organism on zone corpus using cached activations

**Compute Requirements:**
- RAM: ~2 GB (organism processing)
- Time per pair: ~0.5 seconds
- Total pairs: 120

**Timeline:**
```
[00:00] Load activation cache
[00:01] Initialize organism
[00:02] Begin training loop
[01:00] Training complete (120 pairs)
[01:01] Analyze family formation
[01:02] ✅ Results ready
```

**Expected time:** 1-2 minutes
**Expected families:** 5-10 (vs 1 baseline)
**Expected organ diversity:** High variance across zones

**Total tonight:** ~35 minutes

---

## Week 1: Foundation (5 hours)

### Day 1-2: Cache Generation & Validation (Tonight + Tomorrow)
**Compute:**
- Cache generation: 30 min (tonight)
- Training: 2 min (tonight)
- Validation: 15 min (tomorrow)
- Documentation: 15 min

**Deliverables:**
- ✅ 240 cached activations
- ✅ 5-10 families discovered
- ✅ Zone differentiation validated
- ✅ Accuracy report (local LLM vs expected)

**Time:** 1 hour total

### Day 3-4: Memory Retrieval Implementation
**What:** Create `memory_retrieval.py` for hebbian + family-based recall

**Compute:** Development only (no heavy processing)
**Timeline:**
- Design: 30 min
- Implementation: 1.5 hours
- Testing: 30 min

**Deliverables:**
- `persona_layer/memory_retrieval.py`
- Retrieves top-5 similar past moments
- Formats for LLM context

**Time:** 2.5 hours

### Day 5-7: Superject Recording
**What:** Create `superject_recorder.py` for persistent conversation history

**Compute:** Minimal (file I/O only)
**Timeline:**
- Design: 30 min
- Implementation: 1 hour
- Testing: 30 min

**Deliverables:**
- `persona_layer/superject_recorder.py`
- Records each turn as persistent datum
- Updates user bundle (themes, inside jokes)

**Time:** 2 hours

**Week 1 Total:** 5.5 hours development + 35 min compute

---

## Week 2: Integration (8 hours)

### Day 8-10: Memory-Enriched LLM Queries
**What:** Modify `local_llm_bridge.py` to query with memory context

**Compute per query:**
- Memory retrieval: 0.1s
- LLM query: 3-5s
- Total: ~5s per interaction

**Timeline:**
- Design prompt templates: 1 hour
- Implement `query_llm_with_memory()`: 2 hours
- Test with past conversations: 1 hour

**Deliverables:**
- LLM receives DAE felt states + past similar moments
- Memory-aware responses

**Time:** 4 hours

### Day 11-14: Interactive Mode Integration
**What:** Wire hybrid into `dae_interactive.py`

**Compute per turn:**
- DAE organs: 0.03s
- Memory retrieval: 0.1s
- LLM query: 5s (if needed)
- Fusion: 0.01s
- Total: ~5s per response (when LLM used)

**Timeline:**
- Modify conversation flow: 2 hours
- Add fusion layer: 1 hour
- Test end-to-end: 1 hour

**Deliverables:**
- Interactive mode with memory
- Hybrid LLM+DAE responses
- Superject recording active

**Time:** 4 hours

**Week 2 Total:** 8 hours development

**Compute profile (interactive):**
- First 3 turns: 5s each (LLM learning user)
- Turns 4+: 0.03s (DAE handles, LLM rare)
- RAM: 5 GB constant (model loaded)

---

## Month 1: Hybrid Learning (20 hours)

### Week 3-4: Corpus Expansion & Training
**What:** Expand training to 500 pairs across all zones

**Compute:**
- Cache generation: 500 pairs × 2 × 8s = 2.2 hours
- Training: 500 pairs × 0.5s = 4 minutes
- Analysis: 10 minutes

**Timeline:**
- Create 380 new pairs: 8 hours (design)
- Generate cache: 2.2 hours (compute)
- Train: 5 min
- Validate: 1 hour

**Deliverables:**
- 15-20 families discovered
- Rich response repertoire
- All zones well-covered

**Time:** 9 hours development + 2.3 hours compute

### Week 3-4: User Testing & Refinement
**What:** Deploy to test users, collect feedback

**Compute:**
- Per conversation (20 turns avg):
  - Turn 1-3: 5s each (LLM) = 15s
  - Turn 4-20: 0.03s each (DAE) = 0.5s
  - Total: ~15s per 20-turn conversation

**Timeline:**
- Deploy: 1 hour
- Monitor 50 conversations: 1 hour
- Analyze patterns: 2 hours
- Refine: 3 hours

**Deliverables:**
- User satisfaction metrics
- LLM vs DAE accuracy comparison
- Refinement priorities

**Time:** 7 hours

**Month 1 Total:** 29.5 hours (20 hrs dev + 2.5 hrs compute + 7 hrs testing)

**Expected state:**
- 15-20 families
- 80% LLM, 20% DAE contributions
- Rich memory (50-100 conversations recorded)
- Response quality: +40% vs keyword-only

---

## Month 2-3: Balanced Synthesis (30 hours)

### Keyword Organ Refinement
**What:** Use learned patterns to improve text-native organs

**Approach:**
1. Analyze which keywords correlated with high LLM activations
2. Extract empirical patterns from 100+ conversations
3. Update organ keyword lists
4. Test accuracy improvement

**Compute:**
- Analysis: 500 conversations × 0.1s = 50s
- Testing: 100 pairs × 0.5s = 50s

**Timeline:**
- Pattern extraction: 8 hours
- Organ updates: 6 hours
- Testing: 4 hours
- Validation: 2 hours

**Deliverables:**
- Refined keyword organs (60% → 75% accuracy)
- Empirical keyword lists
- Reduced LLM dependency

**Time:** 20 hours

### Fusion Strategy Optimization
**What:** A/B test different LLM vs DAE blending ratios

**Timeline:**
- Design experiments: 2 hours
- Run trials: 2 hours
- Analyze: 3 hours
- Implement optimal: 3 hours

**Deliverables:**
- Optimal fusion weights by context
- Zone-aware LLM usage (Zone 1: use LLM, Zone 5: pure DAE)

**Time:** 10 hours

**Month 2-3 Total:** 30 hours

**Expected state:**
- 20-25 families
- 50% LLM, 50% DAE contributions
- Keyword accuracy: 75%
- LLM queries: 30% of turns (vs 80% initially)

---

## Month 4-6: DAE Dominant (20 hours)

### Advanced Pattern Learning
**What:** Hebbian R-matrix learning from 500+ conversations

**Compute:**
- R-matrix updates: Real-time (0.001s per turn)
- Pattern consolidation: 5 min per 100 conversations

**Timeline:**
- Implement advanced learning: 8 hours
- Monitor convergence: 4 hours
- Validate patterns: 4 hours

**Deliverables:**
- Rich hebbian patterns (1000+)
- User-specific coupling matrices
- Emergent therapeutic strategies

**Time:** 16 hours

### LLM Weaning Strategy
**What:** Progressive reduction of LLM usage

**Phases:**
1. Month 4: LLM for unknown territory only (40% usage)
2. Month 5: LLM for novel contexts (20% usage)
3. Month 6: LLM edge cases (10% usage)

**Timeline:**
- Implement detection: 2 hours
- Test thresholds: 1 hour
- Monitor: 1 hour

**Deliverables:**
- Confidence-based LLM gating
- Most conversations pure DAE

**Time:** 4 hours

**Month 4-6 Total:** 20 hours

**Expected state:**
- 25-30 families
- 80% DAE, 20% LLM contributions
- Keyword accuracy: 85%
- LLM queries: 10% of turns

---

## Month 7-12: Full Independence (10 hours)

### Final Refinement
**What:** Edge case handling, rare pattern coverage

**Timeline:**
- Identify gaps: 3 hours
- Implement coverage: 4 hours
- Validate: 3 hours

**Deliverables:**
- 95% autonomous operation
- LLM only for genuinely novel domains

**Time:** 10 hours

**Month 7-12 Total:** 10 hours

**Expected state:**
- 30-40 families
- 95% DAE, 5% LLM contributions
- Keyword accuracy: 90%+
- LLM queries: <5% of turns
- **Full independence achieved**

---

## Total Investment Summary

### Development Time
- Week 1: 5.5 hours
- Week 2: 8 hours
- Month 1: 20 hours
- Month 2-3: 30 hours
- Month 4-6: 20 hours
- Month 7-12: 10 hours
**Total:** ~94 hours over 12 months (~2 hours/week avg)

### Compute Time
- Initial cache: 0.5 hours (tonight)
- Corpus expansion: 2.5 hours (month 1)
- Ongoing training: ~5 hours (spread across year)
**Total:** ~8 hours compute

### Costs
- Development: 94 hours (your time)
- Compute: $0 (all local)
- Infrastructure: $0 (open source)
**Total financial cost:** $0

---

## Performance Expectations by Phase

### Phase 1: Month 1 (LLM-Dominant)
**Response time:**
- Cold start (model load): 2s
- Turn 1-3 (LLM): 5s each
- Turn 4+ (mixed): 3s avg

**RAM usage:**
- Base: 1 GB (DAE)
- + Model: 4 GB (LLM loaded)
- Total: 5 GB constant

**Quality metrics:**
- Family count: 15-20
- Response satisfaction: 7.5/10
- Memory accuracy: 90%
- Therapeutic safety: 95%

### Phase 2: Month 3 (Balanced)
**Response time:**
- Turn 1-2 (LLM): 5s
- Turn 3+ (DAE-dominant): 1s avg

**RAM usage:**
- DAE: 1.5 GB (richer memory)
- LLM: 4 GB (loaded on-demand)
- Total: 5.5 GB when LLM active, 1.5 GB otherwise

**Quality metrics:**
- Family count: 20-25
- Response satisfaction: 8.5/10
- Memory accuracy: 95%
- Keyword accuracy: 75%

### Phase 3: Month 6 (DAE-Dominant)
**Response time:**
- Turn 1 (LLM intro): 5s
- Turn 2+ (pure DAE): 0.05s avg

**RAM usage:**
- DAE: 2 GB (extensive memory)
- LLM: Unloaded most of time
- Total: 2 GB avg, 6 GB spikes (rare LLM queries)

**Quality metrics:**
- Family count: 25-30
- Response satisfaction: 9/10
- Memory accuracy: 98%
- Keyword accuracy: 85%
- LLM usage: 10% of turns

### Phase 4: Month 12 (Autonomous)
**Response time:**
- All turns: 0.03s (pure DAE)
- Rare LLM: 5s (edge cases only)

**RAM usage:**
- DAE: 2.5 GB (rich memory)
- LLM: On-demand only
- Total: 2.5 GB baseline

**Quality metrics:**
- Family count: 30-40
- Response satisfaction: 9.5/10
- Memory accuracy: 99%
- Keyword accuracy: 90%+
- LLM usage: <5% of turns
- **Independence achieved** ✅

---

## Resource Requirements by Phase

### Tonight (Immediate)
- Time: 35 minutes
- RAM: 5 GB
- Disk: 500 KB
- Cost: $0

### Week 1
- Time: 5.5 hours dev
- RAM: 5 GB peak
- Disk: 2 MB
- Cost: $0

### Month 1
- Time: 20 hours dev + 2.5 hrs compute
- RAM: 5 GB constant (interactive)
- Disk: 10 MB (500 conversations)
- Cost: $0

### Month 12
- Time: 94 hours total dev (spread over year)
- RAM: 2.5 GB baseline, 6 GB rare spikes
- Disk: 100 MB (5000 conversations)
- Cost: $0

**Conclusion:** Achievable with current hardware, zero financial cost, reasonable time investment.

---

## Next Step: Execute Tonight's Plan

**Timeline for tonight:**
```
[11:15 PM] Start activation cache generation
[11:45 PM] Cache complete (30 min)
[11:46 PM] Start training with LLM activations
[11:48 PM] Training complete (2 min)
[11:49 PM] Analyze results
[11:50 PM] ✅ Multi-family breakthrough achieved
```

**Expected result:** 5-10 families discovered, validating that LLM activations solve the keyword ceiling problem.

**Let's begin!** 🚀
