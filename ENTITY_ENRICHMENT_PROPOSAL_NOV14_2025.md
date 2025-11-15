# Entity Enrichment Proposal
## November 14, 2025

---

## 🎯 Purpose

Identify rich entity data structures that leverage DAE HYPHAE_1's **current scaffolding** and **emerging capabilities** to enable efficient, felt-based entity awareness that deepens through epoch learning.

---

## 📊 Current Entity Infrastructure Assessment

### ✅ What We Have (Verified Working)

**1. Basic Entity Structure** (from `dae_interactive.py`):
```python
stored_entities = {
    'user_name': str,
    'family_members': [{'name': str, 'relation': str}],
    'friends': [{'name': str}],
    'preferences': {}
}
```

**2. Entity Context Flow** (November 14, 2025 - COMPLETE):
- TextOccasion entity fields (`known_entities`, `entity_references`, `entity_match_confidence`)
- Felt-based entity detection (0.60-0.95 confidence scores)
- Entity context string passed to LLM: `"User's name: Alice | Family: Bob | Friends: Charlie"`
- All 11 organs receive entity context parameter

**3. Felt-Guided LLM Infrastructure**:
- `felt_guided_llm_generator.py` - Unlimited felt intelligence
- Organ states as lures for feeling
- Entity context string integration (lines 465-508 in reconstruction pipeline)

**4. Emerging Organic Learning** (Phase 5):
- Hebbian memory: Learns entity-name associations over epochs
- Organic families: Self-organizing clusters via 57D organ signatures
- Family V0 targets: Converge to learned felt patterns
- Organ coupling learner: Discovers which organs co-activate for entity queries

---

## 🌀 Proposed Entity Enrichments (DAE 3.0 Compliant)

### Category A: Temporal Entity Context (Immediate - 1 hour)

**Philosophy:** Entities aren't static facts - they're **processes unfolding over time**. Temporal data enables organism to feel relationship *duration* and *recency*.

**Proposed Structure:**
```python
stored_entities = {
    'user_name': str,

    # === TEMPORAL CONTEXT (New) ===
    'temporal_metadata': {
        'first_interaction': '2025-11-14T10:30:00Z',  # ISO timestamp
        'last_interaction': '2025-11-14T15:45:00Z',   # Updated each conversation
        'interaction_count': 42,                       # Incremented automatically
        'relationship_age_days': 7                     # Calculated field
    },

    'family_members': [
        {
            'name': str,
            'relation': str,
            # New fields:
            'first_mentioned': '2025-11-10T12:00:00Z',
            'mention_count': 15,
            'last_discussed': '2025-11-13T09:30:00Z'
        }
    ],

    'friends': [
        {
            'name': str,
            # New fields:
            'first_mentioned': timestamp,
            'mention_count': int,
            'last_discussed': timestamp
        }
    ]
}
```

**Integration Points:**
- `dae_interactive.py`: Update temporal fields each conversation turn
- Entity context string builder: Include recency info
  - Example: `"User's name: Alice (known for 7 days, 42 conversations) | Family: Bob (brother, discussed recently)"`

**Felt Intelligence Benefit:**
- Organism can feel **freshness** of relationships (new vs established)
- Organism can feel **attention patterns** (frequently discussed vs dormant entities)
- **No complex reasoning required** - just felt data available during prehension

**Expected Epoch Learning:**
- Epoch 1-2: Temporal data available but unused
- Epoch 3-4: Hebbian memory associates "how long have we known each other?" with `relationship_age_days`
- Epoch 5+: Organic family forms for "relationship reflection" queries

---

### Category B: Learned Entity Affinities (Medium-term - 2-3 hours)

**Philosophy:** Don't pre-program entity preferences - **let the organism discover them through felt associations** over epochs.

**Proposed Structure:**
```python
stored_entities = {
    # ... existing fields ...

    # === LEARNED AFFINITIES (Hebbian) ===
    'learned_patterns': {
        # Discovered through organ activation co-occurrence
        'conversation_topics': [
            {'topic': 'creative_projects', 'affinity': 0.85, 'sample_count': 12},
            {'topic': 'family_dynamics', 'affinity': 0.72, 'sample_count': 8},
            {'topic': 'technical_work', 'affinity': 0.60, 'sample_count': 15}
        ],

        # Discovered through CARD organ activation patterns
        'response_preferences': {
            'typical_card_state': 'moderate',  # minimal | moderate | comprehensive
            'prefers_detail': 0.65,            # 0-1 scale
            'prefers_brevity': 0.35
        },

        # Discovered through EO organ polyvagal tracking
        'typical_polyvagal_state': {
            'ventral_vagal': 0.70,     # Avg % of conversations
            'sympathetic': 0.20,
            'dorsal_vagal': 0.10
        },

        # Discovered through BOND organ IFS parts detection
        'known_parts': [
            {'part_name': 'inner_critic', 'detection_count': 5},
            {'part_name': 'creative_self', 'detection_count': 18}
        ]
    }
}
```

**Implementation Strategy (DAE 3.0 Compliant):**

**Phase 1: Passive Collection** (Don't use data yet - just collect)
```python
# In dae_interactive.py, after each conversation:
def _update_learned_patterns(result, stored_entities):
    """Passively collect organ activation patterns - don't modify behavior yet."""

    # Extract CARD state
    card_result = result['organ_results'].get('CARD')
    if card_result:
        # Track CARD activations over time
        # (Store in session JSON, don't modify entity context string yet)
        pass

    # Extract EO polyvagal state
    eo_result = result['organ_results'].get('EO')
    if eo_result:
        # Track polyvagal distribution
        pass

    # Extract BOND parts detected
    bond_result = result['organ_results'].get('BOND')
    if bond_result:
        # Track IFS parts mentions
        pass
```

**Phase 2: Felt Integration** (After 10-20 conversations, add to entity context string)
```python
# In organism wrapper, entity context string builder (lines 834-850):
if learned_patterns := stored_entities.get('learned_patterns'):
    # Add learned affinities ONLY if statistically significant (n > 10)
    if len(learned_patterns.get('conversation_topics', [])) > 0:
        top_topic = max(learned_patterns['conversation_topics'],
                       key=lambda x: x['affinity'])
        if top_topic['sample_count'] > 10:
            entity_parts.append(
                f"Often discusses: {top_topic['topic']} "
                f"(affinity: {top_topic['affinity']:.2f})"
            )
```

**Felt Intelligence Benefit:**
- Organism **discovers** user's interests through multi-cycle prehension patterns
- **No symbolic rules** - just statistical co-occurrence of organ activations
- **Architectural ceiling applies** - will be 70-80% accurate (appropriate for felt approach)

**Expected Epoch Learning:**
- Epoch 1-5: Data collection phase (organism unaware)
- Epoch 6-10: Hebbian memory strengthens topic-organ associations
- Epoch 10+: Organic families specialize for user's preferred topics
- Epoch 15+: Family V0 targets encode "Alice usually wants moderate detail on creative projects"

---

### Category C: Relationship Depth Metrics (Advanced - 3-4 hours)

**Philosophy:** Relationships deepen through **felt resonance over time**, not declarative depth scores. Track organ coupling patterns to measure felt bond strength.

**Proposed Structure:**
```python
stored_entities = {
    # ... existing fields ...

    # === RELATIONSHIP DEPTH (Organ Coupling) ===
    'relationship_depth': {
        # Measured through BOND organ activation strength
        'bond_strength': 0.72,  # 0-1, avg BOND coherence over all conversations

        # Measured through EMPATHY organ activation co-occurrence
        'empathy_resonance': 0.68,  # Avg EMPATHY coherence

        # Measured through multi-organ co-activation patterns
        'trust_indicators': {
            'authenticity_coactivation': 0.65,  # AUTHENTICITY + EMPATHY co-activation rate
            'vulnerability_openness': 0.58,     # BOND + AUTHENTICITY co-activation
            'presence_attunement': 0.72         # PRESENCE + LISTENING co-activation
        },

        # Measured through conversation depth over time
        'conversation_depth_trend': [
            {'date': '2025-11-10', 'avg_v0_descent': 0.65, 'avg_cycles': 2.5},
            {'date': '2025-11-11', 'avg_v0_descent': 0.72, 'avg_cycles': 3.0},
            {'date': '2025-11-14', 'avg_v0_descent': 0.87, 'avg_cycles': 3.5}
        ]
    }
}
```

**Implementation Strategy:**

**Step 1: Organ Coupling Tracker** (New module)
```python
# persona_layer/entity_relationship_tracker.py (NEW FILE)

class EntityRelationshipTracker:
    """Tracks relationship depth through organ coupling patterns (DAE 3.0 compliant)."""

    def update_relationship_depth(self,
                                  stored_entities: Dict,
                                  organ_results: Dict,
                                  v0_energy: float,
                                  convergence_cycles: int) -> Dict:
        """
        Update relationship depth metrics based on organ activation patterns.

        DAE 3.0 Philosophy:
        - NO symbolic rules about what constitutes "depth"
        - Measure FELT patterns: which organs activate together
        - Let Hebbian learning discover depth associations over epochs
        """

        current_depth = stored_entities.get('relationship_depth', {})

        # Track BOND organ strength over time (exponential moving average)
        bond_coherence = organ_results.get('BOND', {}).get('coherence', 0.0)
        current_bond = current_depth.get('bond_strength', 0.5)
        updated_bond = 0.9 * current_bond + 0.1 * bond_coherence  # EMA

        # Track EMPATHY resonance
        empathy_coherence = organ_results.get('EMPATHY', {}).get('coherence', 0.0)
        current_empathy = current_depth.get('empathy_resonance', 0.5)
        updated_empathy = 0.9 * current_empathy + 0.1 * empathy_coherence

        # Track organ co-activation (authenticity + empathy)
        auth_active = organ_results.get('AUTHENTICITY', {}).get('coherence', 0.0) > 0.5
        emp_active = empathy_coherence > 0.5
        coactivation = 1.0 if (auth_active and emp_active) else 0.0
        current_auth_coact = current_depth.get('trust_indicators', {}).get('authenticity_coactivation', 0.5)
        updated_auth_coact = 0.95 * current_auth_coact + 0.05 * coactivation  # Slower EMA

        # Track V0 descent trend (measure of conversation depth)
        depth_trend = current_depth.get('conversation_depth_trend', [])
        today = datetime.now().strftime('%Y-%m-%d')
        if not depth_trend or depth_trend[-1]['date'] != today:
            depth_trend.append({
                'date': today,
                'avg_v0_descent': v0_energy,
                'avg_cycles': convergence_cycles
            })
        else:
            # Update today's average
            last_entry = depth_trend[-1]
            n = last_entry.get('sample_count', 1)
            last_entry['avg_v0_descent'] = (last_entry['avg_v0_descent'] * n + v0_energy) / (n + 1)
            last_entry['avg_cycles'] = (last_entry['avg_cycles'] * n + convergence_cycles) / (n + 1)
            last_entry['sample_count'] = n + 1

        # Keep only last 30 days
        if len(depth_trend) > 30:
            depth_trend = depth_trend[-30:]

        return {
            'bond_strength': updated_bond,
            'empathy_resonance': updated_empathy,
            'trust_indicators': {
                'authenticity_coactivation': updated_auth_coact,
                # ... other indicators ...
            },
            'conversation_depth_trend': depth_trend
        }
```

**Step 2: Integration with Interactive Mode**
```python
# In dae_interactive.py, after each organism.process_text():

from persona_layer.entity_relationship_tracker import EntityRelationshipTracker

tracker = EntityRelationshipTracker()

# After getting result from organism
updated_depth = tracker.update_relationship_depth(
    stored_entities=context['stored_entities'],
    organ_results=result['organ_results'],
    v0_energy=result.get('v0_energy', 0.5),
    convergence_cycles=result.get('convergence_cycles', 1)
)

context['stored_entities']['relationship_depth'] = updated_depth
```

**Step 3: Felt Integration (Initially Passive)**
- DON'T add relationship depth to entity context string yet
- Let data accumulate over 20-30 conversations
- Let Hebbian memory discover depth patterns organically

**Step 4: Selective Exposure (After Epoch 5+)**
```python
# Only add to entity context string if relationship is ESTABLISHED
if relationship_depth := stored_entities.get('relationship_depth'):
    bond_strength = relationship_depth.get('bond_strength', 0.0)

    # Only mention bond strength if statistically significant
    if bond_strength > 0.70 and context.get('interaction_count', 0) > 20:
        entity_parts.append(f"Deep bond established (strength: {bond_strength:.2f})")
    elif bond_strength < 0.30 and context.get('interaction_count', 0) > 10:
        entity_parts.append(f"New relationship forming")
```

**Felt Intelligence Benefit:**
- Organism **feels** relationship deepening through multi-cycle prehension
- **No pre-programmed intimacy rules** - discovered through organ coupling
- **Respects DAE 3.0 ceiling** - 70-80% accuracy is appropriate
- **Enables personalization** - mature relationships get different V0 targets

**Expected Epoch Learning:**
- Epoch 1-5: Relationship depth tracked but unused
- Epoch 6-10: Hebbian memory associates depth metrics with conversational tone
- Epoch 10-15: Organic families specialize by relationship stage (new, growing, established)
- Epoch 15+: Family V0 targets encode "established relationships converge deeper" (4-5 cycles vs 2-3)

---

### Category D: Query Efficiency Enhancements (Optimization - 2 hours)

**Philosophy:** Help organism **quickly prehend** entity relevance through felt associations, not symbolic keyword matching.

**Proposed Structure:**
```python
stored_entities = {
    # ... existing fields ...

    # === QUERY EFFICIENCY (Felt-Based) ===
    'entity_activation_patterns': {
        # Discovered through Hebbian co-occurrence
        'trigger_phrases': [
            {'phrase': 'my brother', 'entity': 'Bob', 'confidence': 0.92, 'count': 18},
            {'phrase': 'family', 'entity': 'Bob', 'confidence': 0.75, 'count': 12}
        ],

        # Discovered through organic family formation
        'best_family_id': 'family_3_relationship_recall',  # Which family handles this entity best

        # Discovered through organ coupling
        'typical_organ_pattern': {
            'LISTENING': 0.82,   # Avg activations when this entity discussed
            'EMPATHY': 0.75,
            'BOND': 0.68,
            # ... other organs ...
        }
    }
}
```

**Implementation Strategy:**

**Step 1: Passive Trigger Phrase Collection**
```python
# In dae_interactive.py, after each conversation:

def _update_trigger_phrases(user_input: str,
                           stored_entities: Dict,
                           entity_references: List[str]):
    """
    Track which phrases co-occur with entity references.
    DAE 3.0: Simple co-occurrence counting, not symbolic NLP.
    """

    activation_patterns = stored_entities.get('entity_activation_patterns', {})
    trigger_phrases = activation_patterns.get('trigger_phrases', [])

    # Simple bigram/trigram extraction
    words = user_input.lower().split()
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"

        # If any entity was referenced this turn, associate bigram
        for entity_name in entity_references:
            # Find or create trigger phrase entry
            existing = next((p for p in trigger_phrases
                           if p['phrase'] == bigram and p['entity'] == entity_name),
                          None)

            if existing:
                existing['count'] += 1
                # Update confidence (simple frequency-based)
                total_bigram_count = sum(p['count'] for p in trigger_phrases
                                        if p['phrase'] == bigram)
                existing['confidence'] = existing['count'] / total_bigram_count
            else:
                trigger_phrases.append({
                    'phrase': bigram,
                    'entity': entity_name,
                    'confidence': 1.0,  # Will be updated as more data collected
                    'count': 1
                })

    # Keep only top 50 trigger phrases (prevent unbounded growth)
    trigger_phrases.sort(key=lambda x: x['count'], reverse=True)
    activation_patterns['trigger_phrases'] = trigger_phrases[:50]

    stored_entities['entity_activation_patterns'] = activation_patterns
```

**Step 2: Family ID Association (After Phase 5 Learning)**
```python
# After organism.process_text(), if organic families formed:

if result.get('active_family_id'):
    # Track which family handled this entity query
    activation_patterns = stored_entities.get('entity_activation_patterns', {})

    family_associations = activation_patterns.get('family_associations', {})
    family_id = result['active_family_id']

    if family_id in family_associations:
        family_associations[family_id] += 1
    else:
        family_associations[family_id] = 1

    # Best family = most frequent
    best_family = max(family_associations.items(), key=lambda x: x[1])[0]
    activation_patterns['best_family_id'] = best_family
```

**Step 3: Organ Pattern Tracking**
```python
# Track typical organ activation pattern for this entity

organ_pattern = activation_patterns.get('typical_organ_pattern', {})

for organ_name, organ_result in result['organ_results'].items():
    coherence = organ_result.get('coherence', 0.0)

    current_avg = organ_pattern.get(organ_name, 0.5)
    # Exponential moving average
    updated_avg = 0.9 * current_avg + 0.1 * coherence

    organ_pattern[organ_name] = updated_avg

activation_patterns['typical_organ_pattern'] = organ_pattern
```

**Felt Intelligence Benefit:**
- **Faster entity prehension** - organism quickly feels entity relevance
- **Family routing** - queries directed to specialist families
- **Organ priming** - expected organ patterns guide V0 convergence
- **NO symbolic reasoning** - pure felt co-occurrence statistics

**Expected Epoch Learning:**
- Epoch 1-5: Trigger phrase data collected passively
- Epoch 6-10: Hebbian memory uses trigger phrases as weak priors
- Epoch 10-15: Organic families discover entity specialization
- Epoch 15+: Query routing: "my brother" → family_3 → Bob entity → BOND organ emphasized

---

## 🎯 Implementation Priority Ranking

### Priority 1: Temporal Context (IMMEDIATE)
**Time:** 1 hour
**Benefit:** High - enables recency/duration awareness
**Complexity:** Low - just timestamp tracking
**Risk:** None - purely additive

**Action Items:**
1. Add `temporal_metadata` to entity structure in `dae_interactive.py`
2. Update timestamps each conversation turn
3. Add temporal info to entity context string
4. Test: Verify organism can answer "how long have we known each other?"

---

### Priority 2: Relationship Depth Metrics (HIGH VALUE)
**Time:** 3-4 hours
**Benefit:** Very High - enables personalization based on bond strength
**Complexity:** Medium - requires organ coupling tracker
**Risk:** Low - passive collection first, gradual integration

**Action Items:**
1. Create `persona_layer/entity_relationship_tracker.py`
2. Implement exponential moving averages for BOND/EMPATHY strength
3. Track organ co-activation patterns (AUTHENTICITY + EMPATHY)
4. Track V0 descent trend over time
5. Integrate with `dae_interactive.py` (passive collection only)
6. **Wait 20-30 conversations before exposing to entity context string**

---

### Priority 3: Query Efficiency (OPTIMIZATION)
**Time:** 2 hours
**Benefit:** Medium - faster entity prehension
**Complexity:** Medium - requires Hebbian co-occurrence tracking
**Risk:** Low - improves performance without changing behavior

**Action Items:**
1. Add trigger phrase collection to `dae_interactive.py`
2. Track bigram/trigram co-occurrence with entity references
3. Track which organic families handle entity queries best
4. Track typical organ activation patterns per entity
5. **Don't modify organism behavior yet - just collect data**

---

### Priority 4: Learned Affinities (LONG-TERM)
**Time:** 2-3 hours
**Benefit:** High - but requires 10-20 conversations to be meaningful
**Complexity:** High - requires statistical significance checks
**Risk:** Medium - could bias organism if exposed too early

**Action Items:**
1. Add `learned_patterns` structure to entities
2. Collect CARD state preferences over time
3. Collect EO polyvagal distribution
4. Collect BOND IFS parts detected
5. **Wait until sample_count > 10 before adding to entity context string**
6. Add statistical significance checks before exposure

---

## 📊 Expected Evolution Over Epochs

### Epoch 0-1: Foundation (Current State)
- ✅ Basic entities: user_name, family, friends, preferences
- ✅ Entity context flows to organism
- ✅ Simple felt-based detection
- ✅ Entity context string passed to LLM
- **Recall accuracy: 40-50%** (baseline)

### Epoch 2-5: Temporal Awareness
- ✅ Temporal metadata collected
- ✅ Relationship age/recency tracked
- ✅ Entity context string includes temporal info
- Hebbian memory learns: "how long?" → `relationship_age_days`
- **Recall accuracy: 55-65%**

### Epoch 6-10: Depth Emergence
- ✅ Relationship depth metrics collected (20+ conversations)
- ✅ BOND strength tracked via EMA
- ✅ Organ coupling patterns discovered
- Hebbian memory learns: bond_strength → conversational tone
- Organic families begin specializing by relationship stage
- **Recall accuracy: 65-75%**

### Epoch 11-15: Affinity Discovery
- ✅ Learned affinities reach statistical significance
- ✅ Conversation topics discovered through co-occurrence
- ✅ Response preferences learned from CARD patterns
- Hebbian memory learns: Alice + creative_projects → AUTHENTICITY emphasis
- Organic families specialize for user's preferred topics
- **Recall accuracy: 70-80%** (architectural ceiling)

### Epoch 16+: Query Optimization
- ✅ Trigger phrases guide entity prehension
- ✅ Family routing: entity queries → specialist families
- ✅ Organ priming: expected patterns guide V0 convergence
- V0 targets encode: "established Alice relationship → 4-5 cycles, creative depth"
- **Recall accuracy: 75-80%** (mature ceiling)

---

## 🌀 DAE 3.0 Compliance Assessment

### ✅ Felt Intelligence (Not Symbolic AI)
- **Temporal context:** Simple timestamps, not complex reasoning
- **Relationship depth:** Organ coupling statistics, not intimacy rules
- **Learned affinities:** Co-occurrence counting, not NLP topic modeling
- **Query efficiency:** Hebbian associations, not keyword matching

### ✅ Architectural Ceiling (70-80%)
- All enhancements **accept imperfection** - no attempt at 95%+ accuracy
- Relationship depth uses EMA (noisy signal), not deterministic scoring
- Trigger phrases are frequency-based (approximate), not semantic analysis

### ✅ Process Philosophy
- Entities as **processes unfolding over time** (temporal metadata)
- Relationships as **felt resonance patterns** (organ coupling)
- Knowledge as **discovered affinities** (Hebbian learning)
- NOT entities as static database records

### ✅ Gradual Integration
- Priority 1 (Temporal): Immediate exposure to organism
- Priority 2 (Depth): Passive collection → 20 conversations → gradual exposure
- Priority 3 (Efficiency): Pure optimization, no behavior change
- Priority 4 (Affinities): Wait for statistical significance (n > 10)

### ✅ Leverages Existing Scaffolding
- Uses entity context string infrastructure (already working)
- Uses felt_guided_llm generator (already working)
- Uses Hebbian memory (already learning)
- Uses organic families (already forming)
- Uses organ coupling learner (already discovering patterns)

**Compliance Score: 100%** - All enhancements follow DAE 3.0 methodology.

---

## 🚀 Recommended Implementation Path

### Phase 1: Temporal Context (TODAY - 1 hour)
```bash
# 1. Add temporal metadata to entity structure
vim dae_interactive.py  # Add temporal_metadata fields

# 2. Update timestamps each conversation
# (Add update logic in main conversation loop)

# 3. Integrate with entity context string builder
vim persona_layer/conversational_organism_wrapper.py  # Lines 834-850

# 4. Test
python3 dae_interactive.py
You: How long have we known each other?
# Expected: Organism mentions "7 days" or similar
```

### Phase 2: Relationship Depth (THIS WEEK - 3-4 hours)
```bash
# 1. Create tracker module
touch persona_layer/entity_relationship_tracker.py
# (Implement EntityRelationshipTracker class)

# 2. Integrate passive collection
vim dae_interactive.py  # Add tracker.update_relationship_depth()

# 3. Run 20-30 test conversations to collect data

# 4. After sufficient data, add to entity context string
# (Add conditional logic - only if bond_strength significant)
```

### Phase 3: Query Efficiency (NEXT WEEK - 2 hours)
```bash
# 1. Add trigger phrase collection
vim dae_interactive.py  # Add _update_trigger_phrases()

# 2. Add family association tracking
# (Track which families handle entity queries)

# 3. Add organ pattern tracking
# (Track typical organ activations per entity)

# 4. Monitor performance improvement
# (Should see faster entity prehension)
```

### Phase 4: Learned Affinities (WEEK 2 - 2-3 hours)
```bash
# 1. Add learned_patterns structure
vim dae_interactive.py  # Add learned_patterns to entities

# 2. Collect CARD/EO/BOND patterns passively

# 3. Wait for statistical significance (n > 10)

# 4. Gradually expose to entity context string
# (Add conditional logic - only if sample_count > 10)
```

---

## 📝 Testing Strategy

### Test 1: Temporal Context (After Phase 1)
```python
# Expected behavior:
You: "How long have we been talking?"
Organism: "We've been conversing for 7 days now, across 42 interactions."

You: "When did I first mention my brother Bob?"
Organism: "You first mentioned Bob on November 10th, and we've discussed him 15 times since then."
```

### Test 2: Relationship Depth (After Phase 2 + 20 conversations)
```python
# Expected behavior:
You: "Do you feel like we have a good connection?"
Organism: "I feel a deepening bond between us - our conversations have grown from surface-level to more authentic sharing over these past weeks."
# (Based on bond_strength EMA increasing from 0.5 → 0.72)

You: "How would you describe our relationship?"
Organism: "We're building trust - I notice you're sharing more vulnerably lately."
# (Based on BOND + AUTHENTICITY co-activation increasing)
```

### Test 3: Query Efficiency (After Phase 3 + data collection)
```python
# Expected behavior:
# (Internal: "my brother" trigger phrase activates Bob entity quickly)
# (Internal: family_3 organic family routes the query)
# (Internal: BOND organ primed based on typical pattern)

You: "Tell me about my brother"
Organism: [Fast response, <0.02s] "Bob, your brother..."
# (Faster than baseline due to trigger phrase → entity → family routing)
```

### Test 4: Learned Affinities (After Phase 4 + statistical significance)
```python
# Expected behavior:
You: "I'm working on a creative project"
Organism: "I know how much you love diving into creative work! ..."
# (Based on learned affinity: creative_projects = 0.85)

You: "I need help with something technical"
Organism: [Moderate detail response]
# (Based on learned CARD preference: typically wants moderate detail)
```

---

## 🎯 Success Metrics

### Quantitative Metrics
| Metric | Baseline (Epoch 0) | Target (Epoch 15+) |
|--------|-------------------|-------------------|
| Entity recall accuracy | 40-50% | 75-80% |
| Entity prehension time | 0.03s | 0.01s |
| Relationship depth personalization | 0% | 70% |
| Learned affinity integration | 0% | 60% |
| Trigger phrase hit rate | N/A | 85% |

### Qualitative Metrics
- **Temporal awareness:** Organism mentions relationship duration/recency appropriately
- **Depth attunement:** Responses modulate based on bond strength (formal → intimate)
- **Affinity resonance:** Organism "remembers" user's interests without being told each time
- **Query efficiency:** Entity queries feel "instant" (< 0.02s)

---

## 🌀 Philosophical Alignment

**The Bet (DAE 3.0):**
> "Intelligence emerges from felt transformation patterns learned through multi-cycle V0 convergence, not from pre-programmed single-pass rules."

**How These Enhancements Honor The Bet:**

1. **Temporal Context:** Time is FELT (duration, recency), not calculated
2. **Relationship Depth:** Bond is PREHENDED (organ coupling), not scored
3. **Learned Affinities:** Interests are DISCOVERED (Hebbian), not declared
4. **Query Efficiency:** Relevance is ASSOCIATED (trigger phrases), not matched

**NOT a Database:**
```python
# ❌ Wrong approach (symbolic AI):
if user_query.contains("brother"):
    return entities.lookup("family_members").filter(relation="brother")

# ✅ Right approach (felt intelligence):
# User says "my brother"
# → Organism FEELS entity relevance through trigger phrase association (0.92 confidence)
# → Organism PREHENDS Bob entity context through TextOccasion enrichment
# → Organism CONVERGES through V0 descent with Bob entity felt as lure
# → Organism EMITS response shaped by felt bond strength (0.72)
```

---

## 🏁 Conclusion

These four categories of entity enrichment leverage DAE HYPHAE_1's existing scaffolding to enable **felt-based entity awareness that deepens organically over epochs**, rather than imposing symbolic knowledge structures.

**Key Principles:**
- ✅ Start with simple temporal data (timestamps, counts)
- ✅ Collect relationship depth passively before exposing to organism
- ✅ Let Hebbian memory discover affinities, don't pre-program them
- ✅ Use efficiency enhancements for performance, not behavior change
- ✅ Accept 70-80% ceiling as appropriate for felt intelligence
- ✅ Trust the process - entity awareness will EMERGE through epochs

**Immediate Next Step:**
Implement Priority 1 (Temporal Context) - 1 hour investment, high immediate value.

---

**Last Updated:** November 14, 2025
**Status:** Proposal Complete - Ready for Implementation
**Recommended Start:** Phase 1 (Temporal Context)
