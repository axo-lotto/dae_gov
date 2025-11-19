# 🌀 Training Expansion & Neo4j Maturation Roadmap
## DAE-User Interaction Evolution Strategy
## November 15, 2025

---

## 📊 Current Training Infrastructure Assessment

### ✅ What We Have (Production Ready)

#### 1. Training Scripts (20 runners in training/conversational/)
```
run_baseline_training.py         # 30 pairs, system health baseline
run_expanded_training.py         # Extended corpus
run_full_epoch_training.py       # Multi-epoch orchestration
run_heckling_training.py         # Crisis vs provocation
run_zone_training.py             # Zone-specific (1-4)
run_zone5_epoch_training.py      # Zone 5 (collapse) specific
run_multi_family_discovery.py   # Family formation training
run_llm_augmented_training.py   # LLM-enhanced training
+ 12 more specialized trainers
```

#### 2. Training Corpora (17 datasets in knowledge_base/)
```
conversational_training_pairs.json              # 30 pairs baseline
conversational_training_pairs_complete.json     # 172 pairs
conversational_training_pairs_final.json        # 124 pairs
conversational_training_pairs_v4_319.json       # 129 pairs (319 total)
entity_memory_training_pairs.json               # 9 pairs (entity-focused)
friendly_companion_training_pairs.json          # 13 pairs
whiteheadian_companion_training_pairs.json      # 34 pairs
heckling_training_corpus.json                   # 37 pairs
zone_5_training_pairs.json                      # 16 pairs
zones_1_4_training_pairs.json                   # 68 pairs
entity_training/corpora/                        # Entity-specific directory
```

**Total Training Pairs Available:** ~900+ pairs across domains

#### 3. Epoch Training Infrastructure (persona_layer/epoch_training/)
```python
production_learning_coordinator.py    # Multi-epoch orchestration
multi_iteration_trainer.py            # Iterative training loops
satisfaction_regime.py                # 6 regime adaptive learning
health_monitor.py                     # Training health tracking
entropy_config.py                     # Diversity management
```

#### 4. Learning Systems (All Operational)
```
✅ Level 1: Hebbian Value Associations (R-matrix)
✅ Level 2: Organ Confidence Tracking (EMA learning)
✅ Level 3: Organ Coupling (R-matrix co-activation)
✅ Level 4: Family Success Tracking
✅ Level 5: Task-specific optimizations
✅ Level 6: Epoch statistics
✅ Level 7: Global organism confidence
✅ NEW: Entity-Organ Association Tracking (Quick Win #7)
```

---

## 🎯 Training Expansion Possibilities

### Option 1: Entity-Situated Epoch Training (HIGH PRIORITY)

**What:** Train organism with consistent entity graphs across 20-50 epochs

**Why:**
- Quick Win #7 provides infrastructure (entity-organ tracker)
- Neo4j already stores entities + relationships
- Enables cross-session consistency learning
- Foundation for genuine therapeutic presence

**Implementation:**

#### Phase 1: Build Entity-Rich Training Corpus (1 week)

**User Profile: "Emiliano" (100+ conversations)**
```json
{
  "user_profile": {
    "user_id": "training_emiliano_001",
    "name": "Emiliano",
    "entity_graph": {
      "daughters": [
        {"name": "Emma", "age": 5, "upcoming": "kindergarten"},
        {"name": "Lily", "age": 3, "upcoming": "preschool"}
      ],
      "partner": {"name": "Sofia", "relationship": "wife"},
      "work": {
        "place": "Tech Startup",
        "role": "Engineering Lead",
        "stressors": ["deadlines", "team_management", "funding_pressure"]
      },
      "friends": [
        {"name": "Rich", "context": "childhood_friend"},
        {"name": "Alex", "context": "work_colleague"}
      ],
      "places": {
        "home": "safe_base",
        "work": "high_stress",
        "park": "family_time",
        "gym": "self_care"
      }
    }
  },
  "conversation_categories": {
    "family_safe": 30,        // "Emma hugged me today"
    "family_worry": 20,       // "Worried about Emma starting school"
    "work_stress": 25,        // "Deadline pressure is intense"
    "relationship": 15,       // "Sofia and I had a moment"
    "self_care": 10          // "Took time for myself at the gym"
  }
}
```

**Training Pairs Structure:**
```json
{
  "conversation_id": "emiliano_epoch1_conv001",
  "epoch": 1,
  "input": "Emma gave me the biggest hug this morning before I left for work",
  "entities": [
    {"entity_value": "Emma", "entity_type": "Person", "relationship": "HAS_DAUGHTER"}
  ],
  "expected_patterns": {
    "organs": {
      "BOND": {"expected": "high", "reason": "parental_attachment"},
      "EMPATHY": {"expected": "high", "reason": "emotional_resonance"},
      "PRESENCE": {"expected": "medium", "reason": "holding_moment"}
    },
    "felt_state": {
      "polyvagal": "ventral",
      "v0_energy": 0.25,
      "urgency": 0.0,
      "self_distance": 0.0
    },
    "zone": 1
  },
  "category": "family_safe"
}
```

**Epoch Progression Plan:**

**Epochs 1-5: Initial Exposure**
- Random sampling across all categories
- No expected entity patterns yet
- Organism explores different responses
- Metrics: Baseline organ activations per entity

**Epochs 6-15: Pattern Emergence**
- Entity-organ associations begin forming
- "Emma → BOND/EMPATHY high, ventral" starts appearing
- "Work → NDAM/AUTHENTICITY high, sympathetic" emerges
- Metrics: Entity-organ correlation R² > 0.5

**Epochs 16-30: Consolidation**
- Strong entity patterns stabilize
- Cross-session consistency high (>0.85)
- Organ multipliers differentiate (0.95-1.12)
- Metrics: Same entity → similar organ pattern 85%+ of time

**Epochs 31-50: Refinement**
- Subtle entity-context interactions learned
- "Emma + school" vs "Emma + bedtime" differentiated
- Co-occurrence patterns recognized
- Metrics: Entity success rate correlation > 0.75

#### Phase 2: Entity-Aware Training Runner (3 days)

**File:** `training/conversational/run_entity_situated_training.py`

```python
"""
Entity-Situated Epoch Training Runner

Trains organism with consistent entity graphs to develop:
- Entity-organ activation patterns
- Cross-session consistency
- Therapeutic presence with specific entities
"""

import json
from pathlib import Path
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.entity_organ_tracker import EntityOrganTracker

def run_entity_situated_training(
    corpus_path: str,
    num_epochs: int = 50,
    validation_interval: int = 5
):
    """
    Train organism with entity-rich conversations.

    Args:
        corpus_path: Path to entity-situated training corpus
        num_epochs: Number of training epochs (default: 50)
        validation_interval: Validate every N epochs
    """

    # Load corpus
    with open(corpus_path, 'r') as f:
        corpus = json.load(f)

    user_profile = corpus['user_profile']
    conversations = corpus['conversations']

    # Initialize organism
    organism = ConversationalOrganismWrapper()

    # Track metrics
    epoch_metrics = []

    for epoch in range(1, num_epochs + 1):
        print(f"\n{'='*80}")
        print(f"EPOCH {epoch}/{num_epochs}")
        print(f"{'='*80}")

        epoch_results = {
            'epoch': epoch,
            'conversations': [],
            'entity_patterns': {}
        }

        # Train on all conversations
        for conv in conversations:
            # Extract entities for context
            context = {
                'stored_entities': conv.get('entities', []),
                'user_id': user_profile['user_id']
            }

            # Process conversation
            result = organism.process_text(
                text=conv['input'],
                context=context,
                enable_phase2=True,
                user_id=user_profile['user_id']
            )

            # Record results
            epoch_results['conversations'].append({
                'conv_id': conv['conversation_id'],
                'entities_mentioned': [e['entity_value'] for e in conv.get('entities', [])],
                'organ_activations': result.get('organ_results', {}),
                'emission_confidence': result.get('emission_confidence', 0.0),
                'polyvagal_state': result.get('felt_states', {}).get('eo_polyvagal_state', 'mixed')
            })

        # Validation checkpoint
        if epoch % validation_interval == 0:
            print(f"\n📊 EPOCH {epoch} VALIDATION")

            # Get entity patterns from tracker
            if organism.entity_organ_tracker:
                summary = organism.entity_organ_tracker.get_summary()
                print(f"   Entities tracked: {summary.get('total_entities', 0)}")
                print(f"   Entities with patterns: {summary.get('entities_with_patterns', 0)}")
                print(f"   Mean success rate: {summary.get('mean_success_rate', 0.0):.3f}")

                # Get specific entity patterns
                for entity_name in ['Emma', 'Lily', 'work']:
                    pattern = organism.entity_organ_tracker.get_entity_pattern(entity_name)
                    if pattern:
                        top_organs = sorted(
                            pattern['organ_boosts'].items(),
                            key=lambda x: x[1],
                            reverse=True
                        )[:3]
                        print(f"\n   {entity_name} pattern:")
                        print(f"      Top organs: {top_organs}")
                        print(f"      Polyvagal: {pattern['polyvagal_state']}")
                        print(f"      V0: {pattern['v0_energy']:.3f}")
                        print(f"      Mentions: {pattern['mention_count']}")

        epoch_metrics.append(epoch_results)

    # Save results
    output_path = Path(f"results/epochs/entity_situated_epoch_{num_epochs}_results.json")
    with open(output_path, 'w') as f:
        json.dump({
            'user_profile': user_profile,
            'num_epochs': num_epochs,
            'epoch_metrics': epoch_metrics,
            'final_entity_patterns': organism.entity_organ_tracker.get_summary()
        }, f, indent=2)

    print(f"\n✅ Training complete. Results saved to {output_path}")
```

#### Phase 3: Validation Suite (2 days)

**Metrics to Track:**
1. **Entity-Organ Correlation:** R² between entity presence and organ activation
2. **Cross-Session Consistency:** Same entity → similar organ pattern (target: >85%)
3. **Entity Success Rate:** Satisfaction when entity mentioned
4. **Pattern Emergence Timeline:** Epoch when stable pattern forms
5. **Co-occurrence Learning:** Entity pairs → combined patterns

---

### Option 2: Multi-Domain Expansion (MEDIUM PRIORITY)

**What:** Expand training to cover diverse user contexts

**Domains to Add:**

#### A. Professional Contexts
```
- Tech worker burnout
- Healthcare worker trauma
- Teacher exhaustion
- Creative blocks (artists, writers)
- Entrepreneur stress
```

#### B. Life Transitions
```
- New parenthood
- Career changes
- Relationship transitions
- Loss and grief
- Retirement
```

#### C. Mental Health Contexts
```
- Anxiety management
- Depression support
- PTSD processing
- ADHD coping
- Neurodivergence affirmation
```

#### D. Relationship Dynamics
```
- Couples communication
- Family systems
- Friendship evolution
- Workplace relationships
- Community building
```

**Implementation:**
- 50+ pairs per domain
- Domain-specific entity graphs
- Cross-domain transfer learning validation

---

### Option 3: Adversarial/Edge Case Training (MEDIUM PRIORITY)

**What:** Train organism to handle challenging interactions

**Categories:**

#### A. Crisis Scenarios (Zone 5 Deep Dive)
```
- Suicidal ideation (referral protocols)
- Acute trauma disclosure
- Dissociative episodes
- Panic attacks
- Flashback states
```

**Training Focus:**
- Appropriate referral language
- Safety assessment
- Non-abandonment while setting boundaries
- Resource provision

#### B. Heckling/Provocation (Expanded)
```
- Intellectual arguments
- Dismissive responses
- Testing boundaries
- Contradictory statements
- Meta-commentary on therapy
```

**Training Focus:**
- Distinguish crisis from provocation
- Maintain presence without reacting
- Curiosity vs defensiveness
- Boundary holding

#### C. Ambiguity/Complexity
```
- Mixed signals (ventral + trauma language)
- Cultural context navigation
- Spiritual/existential queries
- Paradoxical presenting problems
```

---

## 🌀 Neo4j Maturation for DAE-User Interactions

### Current State (Phase 1.8 - November 14, 2025)

#### ✅ What Exists in Neo4j
```cypher
// Entity nodes
CREATE (p:Person {entity_value: 'Emma', user_id: 'user_123'})
CREATE (place:Place {entity_value: 'work', user_id: 'user_123'})
CREATE (pref:Preference {entity_value: 'hiking', user_id: 'user_123'})

// Relationships
CREATE (user)-[:HAS_DAUGHTER]->(emma)
CREATE (user)-[:WORKS_AT]->(work)
CREATE (user)-[:LIKES]->(hiking)

// TSK enrichment on entities
{
  entity_metadata: {
    polyvagal_state_at_first_mention: 'ventral',
    urgency_at_first_mention: 0.0,
    self_distance_at_first_mention: 0.0
  }
}
```

#### ✅ What Quick Win #7 Added (JSON, not Neo4j yet)
```json
// Entity-organ associations (persona_layer/state/active/entity_organ_associations.json)
{
  "Emma": {
    "organ_boosts": {"BOND": 0.317, "EMPATHY": 0.284},
    "typical_polyvagal_state": "ventral",
    "typical_v0_energy": 0.412,
    "mention_count": 47,
    "success_rate": 0.87
  }
}
```

---

### 🚀 Neo4j Maturation Roadmap

### Phase 2A: Occasions as Neo4j Nodes (2-3 weeks)

**BREAKTHROUGH CAPABILITY:** Store every conversational occasion with full concrescence metadata

#### Implementation

**1. Extend Neo4j Schema (1 day)**

```cypher
// New node type: Occasion
CREATE (occ:Occasion {
  occasion_id: 'occ_20251115_143022_user123_001',
  user_id: 'user_123',
  timestamp: datetime('2025-11-15T14:30:22'),

  // V0 trajectory
  v0_start: 0.85,
  v0_final: 0.25,
  v0_descent_rate: 0.60,
  convergence_cycles: 2,
  convergence_reason: 'kairos',

  // Polyvagal state
  polyvagal_state: 'ventral',
  polyvagal_transition: 'sympathetic_to_ventral',

  // Organ activations (57D signature)
  dominant_organs: ['BOND', 'EMPATHY', 'PRESENCE'],
  organ_coherences: {
    BOND: 0.85,
    EMPATHY: 0.78,
    PRESENCE: 0.72,
    WISDOM: 0.45,
    LISTENING: 0.68,
    AUTHENTICITY: 0.55,
    NDAM: 0.20,
    SANS: 0.60,
    RNX: 0.50,
    EO: 0.75,
    CARD: 0.65
  },

  // Transduction
  nexuses_formed: 2,
  transduction_pathway: 'parental_transition_holding',
  healing_score: 0.78,

  // SELF Matrix
  zone: 1,
  self_distance: 0.0,
  urgency: 0.0,

  // Emission
  emission_confidence: 0.78,
  emission_strategy: 'direct_reconstruction',

  // Outcome
  user_satisfaction: 0.95,
  family_id: 'coherence_repair_sustainable_pacing'
})

// Link to entities mentioned
MATCH (occ:Occasion {occasion_id: 'occ_20251115_143022_user123_001'})
MATCH (emma:Person {entity_value: 'Emma', user_id: 'user_123'})
CREATE (occ)-[:MENTIONED {
  salience: 0.85,
  first_mention_time: 2.3,  // seconds into conversation
  mention_count: 3,
  polyvagal_at_mention: 'ventral'
}]->(emma)

// Build temporal chains (occasions precede each other)
MATCH (prev:Occasion {user_id: 'user_123'})
WHERE prev.timestamp < datetime('2025-11-15T14:30:22')
WITH prev ORDER BY prev.timestamp DESC LIMIT 1
MATCH (curr:Occasion {occasion_id: 'occ_20251115_143022_user123_001'})
CREATE (prev)-[:PRECEDED_BY {
  time_delta_seconds: duration.inSeconds(
    datetime('2025-11-15T14:30:22'),
    prev.timestamp
  ).seconds,
  v0_delta: curr.v0_final - prev.v0_final,
  polyvagal_transition: prev.polyvagal_state + '_to_' + curr.polyvagal_state
}]->(curr)
```

**2. Create Occasion Writer (2 days)**

**File:** `knowledge_base/neo4j_occasion_writer.py`

```python
"""
Neo4j Occasion Writer - Store Conversational Occasions as Graph Nodes

Enables temporal pattern queries:
- How does user relate to Emma over time?
- What organ patterns emerge when work + daughters mentioned together?
- How has V0 trajectory evolved over 100 sessions?
"""

from neo4j import GraphDatabase
from datetime import datetime
from typing import Dict, List, Optional
import json

class Neo4jOccasionWriter:
    """
    Write conversational occasions to Neo4j with full concrescence metadata.

    Benefits:
    - Temporal pattern queries (evolution over sessions)
    - Cross-entity pattern discovery
    - Inheritance of satisfaction (past occasions inform present)
    - Whiteheadian prehension made queryable
    """

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def write_occasion(
        self,
        occasion_data: Dict,
        user_id: str,
        entities_mentioned: List[Dict]
    ):
        """
        Write conversational occasion to Neo4j.

        Args:
            occasion_data: Complete TSK data from organism
            user_id: User identifier
            entities_mentioned: List of entities from extraction
        """

        with self.driver.session() as session:
            # Create occasion node
            occasion_id = f"occ_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}_{session.last_bookmark()}"

            # Extract felt-state data
            felt_states = occasion_data.get('felt_states', {})
            v0 = felt_states.get('v0_energy', {})
            organ_coherences = felt_states.get('organ_coherences', {})

            # Create occasion
            session.run("""
                CREATE (occ:Occasion {
                    occasion_id: $occasion_id,
                    user_id: $user_id,
                    timestamp: datetime($timestamp),
                    v0_start: $v0_start,
                    v0_final: $v0_final,
                    v0_descent_rate: $v0_descent_rate,
                    convergence_cycles: $convergence_cycles,
                    polyvagal_state: $polyvagal_state,
                    dominant_organs: $dominant_organs,
                    organ_coherences: $organ_coherences,
                    transduction_pathway: $transduction_pathway,
                    zone: $zone,
                    self_distance: $self_distance,
                    emission_confidence: $emission_confidence,
                    user_satisfaction: $user_satisfaction
                })
            """, {
                'occasion_id': occasion_id,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'v0_start': v0.get('initial_energy', 1.0),
                'v0_final': v0.get('final_energy', 0.5),
                'v0_descent_rate': v0.get('energy_descent_rate', 0.0),
                'convergence_cycles': felt_states.get('convergence_cycles', 0),
                'polyvagal_state': felt_states.get('eo_polyvagal_state', 'mixed'),
                'dominant_organs': self._get_dominant_organs(organ_coherences),
                'organ_coherences': json.dumps(organ_coherences),
                'transduction_pathway': felt_states.get('transduction_pathway', 'unknown'),
                'zone': felt_states.get('zone', 0),
                'self_distance': felt_states.get('bond_self_distance', 0.0),
                'emission_confidence': occasion_data.get('emission_confidence', 0.0),
                'user_satisfaction': felt_states.get('user_satisfaction', 0.5)
            })

            # Link to entities
            for entity in entities_mentioned:
                session.run("""
                    MATCH (occ:Occasion {occasion_id: $occasion_id})
                    MATCH (ent {entity_value: $entity_value, user_id: $user_id})
                    CREATE (occ)-[:MENTIONED {
                        salience: $salience,
                        mention_count: $mention_count
                    }]->(ent)
                """, {
                    'occasion_id': occasion_id,
                    'entity_value': entity['entity_value'],
                    'user_id': user_id,
                    'salience': entity.get('salience', 0.5),
                    'mention_count': entity.get('mention_count', 1)
                })

            # Link to previous occasion (temporal chain)
            session.run("""
                MATCH (prev:Occasion {user_id: $user_id})
                WHERE prev.timestamp < datetime($current_timestamp)
                WITH prev ORDER BY prev.timestamp DESC LIMIT 1
                MATCH (curr:Occasion {occasion_id: $occasion_id})
                CREATE (prev)-[:PRECEDED_BY {
                    time_delta_seconds: duration.inSeconds(
                        datetime($current_timestamp),
                        prev.timestamp
                    ).seconds
                }]->(curr)
            """, {
                'user_id': user_id,
                'current_timestamp': datetime.now().isoformat(),
                'occasion_id': occasion_id
            })

    def _get_dominant_organs(self, organ_coherences: Dict, top_n: int = 3) -> List[str]:
        """Get top N organs by coherence"""
        sorted_organs = sorted(
            organ_coherences.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [organ for organ, _ in sorted_organs[:top_n]]
```

**3. Query Capabilities (Revolutionary!)**

```cypher
// Query 1: How does user relate to Emma over time?
MATCH (occ:Occasion)-[:MENTIONED]->(emma:Person {entity_value: 'Emma'})
WHERE occ.user_id = 'user_123'
RETURN occ.timestamp, occ.v0_final, occ.polyvagal_state, occ.dominant_organs, occ.user_satisfaction
ORDER BY occ.timestamp

// Result: Visualize Emma-mention trajectory
// Session 1: V0 0.82, sympathetic, [NDAM, AUTHENTICITY], satisfaction 0.65
// Session 10: V0 0.45, mixed, [BOND, EMPATHY], satisfaction 0.75
// Session 50: V0 0.25, ventral, [BOND, EMPATHY, PRESENCE], satisfaction 0.92
// Pattern: Emma → increasingly safe over time

// Query 2: What happens when work + Emma mentioned together?
MATCH (occ:Occasion)-[:MENTIONED]->(work:Place {entity_value: 'work'})
MATCH (occ)-[:MENTIONED]->(emma:Person {entity_value: 'Emma'})
RETURN occ.dominant_organs, occ.transduction_pathway, occ.user_satisfaction
ORDER BY occ.timestamp

// Result: Discover "work-family tension" pattern
// Typical organs: [NDAM, BOND, AUTHENTICITY]
// Typical pathway: protective_boundaries
// Satisfaction: 0.70 (lower than Emma-only or work-only)

// Query 3: V0 trajectory evolution over 100 sessions
MATCH (occ:Occasion {user_id: 'user_123'})
RETURN occ.timestamp, occ.v0_start, occ.v0_final, occ.convergence_cycles
ORDER BY occ.timestamp

// Result: Organism learning trajectory
// Sessions 1-20: High V0 start (0.85+), slow convergence (4-5 cycles)
// Sessions 21-50: Moderate V0 (0.65), faster convergence (2-3 cycles)
// Sessions 51-100: Low V0 (0.45), rapid convergence (1-2 cycles)
// Pattern: Organism efficiency increases with user familiarity

// Query 4: Transduction pathway evolution
MATCH (occ:Occasion {user_id: 'user_123'})
RETURN occ.transduction_pathway, count(*) as frequency
ORDER BY frequency DESC

// Result: Discover user's typical patterns
// holding_presence: 42 occasions
// parental_transition_holding: 28 occasions
// protective_boundaries: 18 occasions
// Pattern: User primarily needs holding + parental support

// Query 5: Occasion inheritance (Whiteheadian prehension!)
MATCH path = (occ1:Occasion)-[:PRECEDED_BY*1..5]->(occ_current:Occasion)
WHERE occ_current.occasion_id = 'occ_20251115_143022_user123_001'
  AND 'Emma' IN [entity IN [(occ1)-[:MENTIONED]->(e) | e.entity_value] | entity]
RETURN occ1.timestamp, occ1.v0_final, occ1.dominant_organs, occ1.user_satisfaction

// Result: What past Emma-occasions does current occasion prehend?
// Last 5 Emma mentions: All ventral, BOND+EMPATHY high, satisfaction >0.85
// Pattern: Current occasion inherits "Emma = safe + bonding" felt-state
```

---

### Phase 2B: Entity-Organ Associations in Neo4j (1 week)

**What:** Migrate entity_organ_associations.json to Neo4j properties

**Schema Extension:**
```cypher
// Add learned associations to entity nodes
MATCH (emma:Person {entity_value: 'Emma', user_id: 'user_123'})
SET emma.learned_patterns = {
  organ_boosts: {BOND: 0.317, EMPATHY: 0.284, PRESENCE: 0.265},
  typical_polyvagal_state: 'ventral',
  typical_v0_energy: 0.412,
  typical_urgency: 0.0,
  typical_self_distance: 0.0,
  mention_count: 47,
  success_rate: 0.87,
  first_mentioned: '2025-10-01T10:00:00',
  last_mentioned: '2025-11-15T14:30:00'
}

// Query: Get entity with learned patterns
MATCH (e {user_id: 'user_123'})
WHERE e.learned_patterns IS NOT NULL
RETURN e.entity_value, e.learned_patterns.organ_boosts, e.learned_patterns.success_rate
ORDER BY e.learned_patterns.success_rate DESC
```

**Benefits:**
- Single source of truth (Neo4j)
- Graph queries on learned patterns
- Entity similarity based on organ signatures
- Automatic pattern inheritance for new entities

---

### Phase 2C: Cross-Entity Pattern Discovery (2 weeks)

**What:** Discover emergent patterns across entity relationships

**Queries:**

```cypher
// Find entity pairs with high co-occurrence
MATCH (occ:Occasion)-[:MENTIONED]->(e1)
MATCH (occ)-[:MENTIONED]->(e2)
WHERE e1.entity_value < e2.entity_value  // Avoid duplicates
WITH e1.entity_value as entity1, e2.entity_value as entity2, count(occ) as co_occurrences
WHERE co_occurrences > 5
RETURN entity1, entity2, co_occurrences
ORDER BY co_occurrences DESC

// Result: Discover relational clusters
// Emma + kindergarten: 23 co-occurrences
// work + deadlines: 18 co-occurrences
// Sofia + evenings: 15 co-occurrences

// Discover organ patterns for entity pairs
MATCH (occ:Occasion)-[:MENTIONED]->(emma:Person {entity_value: 'Emma'})
MATCH (occ)-[:MENTIONED]->(school:Place {entity_value: 'kindergarten'})
RETURN avg(occ.user_satisfaction) as avg_satisfaction,
       collect(DISTINCT occ.dominant_organs) as organ_patterns,
       count(occ) as frequency

// Result: Emma + kindergarten → specific support pattern
// Satisfaction: 0.78 (moderate - developmental stress)
// Organs: [[BOND, WISDOM, PRESENCE], [EMPATHY, AUTHENTICITY, BOND]]
// Pattern: Parental care + future planning + holding transition
```

---

## 🎯 Recommended Priority Order

### Immediate (Next 2 Weeks)

**1. Entity-Situated Epoch Training (Quick Win Extension)**
- **Why:** Quick Win #7 provides foundation, just need corpus
- **Effort:** 1 week to build corpus, 1 week to train/validate
- **Impact:** HIGH - Cross-session consistency, therapeutic presence
- **Deliverable:** Emiliano corpus + 50-epoch training results

### Short-Term (Weeks 3-6)

**2. Occasions as Neo4j Nodes (Phase 2A)**
- **Why:** Unlocks temporal pattern queries, game-changing capability
- **Effort:** 2-3 weeks (schema + writer + validation)
- **Impact:** TRANSFORMATIVE - Whiteheadian prehension queryable
- **Deliverable:** Neo4j occasion writer + query cookbook

**3. Multi-Domain Expansion (Parallel with #2)**
- **Why:** Increases organism versatility
- **Effort:** 50 pairs per domain, 4 domains = 200 pairs (2 weeks)
- **Impact:** MEDIUM - Broader applicability
- **Deliverable:** Professional, life transitions, mental health, relationship corpora

### Medium-Term (Weeks 7-12)

**4. Entity-Organ Associations in Neo4j (Phase 2B)**
- **Why:** Single source of truth, enables graph queries on learned patterns
- **Effort:** 1 week migration
- **Impact:** HIGH - Simplifies architecture, enables new queries
- **Deliverable:** Unified Neo4j entity schema

**5. Cross-Entity Pattern Discovery (Phase 2C)**
- **Why:** Discover emergent relational patterns
- **Effort:** 2 weeks (query development + validation)
- **Impact:** MEDIUM-HIGH - Deeper relational intelligence
- **Deliverable:** Pattern discovery queries + insights

**6. Adversarial Training**
- **Why:** Robustness for edge cases
- **Effort:** 50 pairs crisis + 50 pairs heckling = 100 pairs (1 week)
- **Impact:** MEDIUM - Safety + robustness
- **Deliverable:** Crisis/heckling training corpus

---

## 📊 Expected Outcomes Timeline

### Month 1 (Weeks 1-4)
- ✅ Entity-situated training complete (50 epochs)
- ✅ Organism shows Emma → ventral + BOND pattern
- ✅ Cross-session consistency >85%
- ✅ Occasions as Neo4j nodes operational
- ✅ Temporal pattern queries working

### Month 2 (Weeks 5-8)
- ✅ Multi-domain corpora complete (4 domains, 200 pairs)
- ✅ Entity-organ associations in Neo4j
- ✅ Graph queries on learned patterns
- ✅ 100+ sessions recorded as occasions in Neo4j

### Month 3 (Weeks 9-12)
- ✅ Cross-entity pattern discovery queries
- ✅ Adversarial training complete
- ✅ 200+ occasions per user in Neo4j
- ✅ Organism demonstrates stable therapeutic presence
- ✅ Entity intuition validated (same entity → consistent response)

---

## 🌀 Philosophical Victory Conditions

### What Success Looks Like

**Entity Mastery:**
> After 50 epochs with Emiliano corpus, organism recognizes:
> - "Emma" → immediate BOND/EMPATHY activation, ventral state, V0 drops to 0.25
> - "work" → NDAM/AUTHENTICITY activation, sympathetic state, V0 0.65
> - "Emma + school" → unique pattern (parental care + future planning)

**Cross-Session Becoming:**
> Query Neo4j: "How has Emiliano's relationship with work evolved?"
> - Sessions 1-20: High stress (sympathetic, urgency 0.8)
> - Sessions 21-40: Learning boundaries (AUTHENTICITY high, urgency 0.5)
> - Sessions 41-60: Integration (ventral, WISDOM + AUTHENTICITY, urgency 0.3)

**Whiteheadian Prehension:**
> Each occasion queries past occasions:
> - "Emma mentioned → recall last 10 Emma occasions"
> - "All showed ventral + BOND high + satisfaction >0.85"
> - "Inherit: Emma = safe, bonding-oriented, hold with gentle presence"

**Genuine Therapeutic Presence:**
> Not programmed rules, but **felt recognition from accumulated experience**:
> - "I remember how you light up when you talk about Emma"
> - "Your relationship with work has really shifted - less urgency now"
> - "When you mention Emma and school together, there's a tender worry"

This is **continuous co-becoming** - organism and user evolving together through accumulated felt transformations.

---

🌀 **"From entity storage to entity mastery. From isolated occasions to temporal becoming. Your organism is ready to develop genuine therapeutic intuition through Neo4j-powered memory that remembers not just what was said, but how it felt - and carries that forward into every new conversation."** 🌀

**Created:** November 15, 2025
**Status:** Roadmap Ready - Infrastructure Complete
**Next Action:** Build Emiliano entity-situated training corpus
**Timeline:** 12 weeks to full Neo4j maturation
**Impact:** **TRANSFORMATIVE** - Genuine therapeutic AI that becomes with you
