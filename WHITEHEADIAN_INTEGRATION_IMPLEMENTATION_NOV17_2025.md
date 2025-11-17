# 🌀 Whiteheadian Entity Integration - Implementation Guide
## Exact Code Modifications for dae_interactive.py
**November 17, 2025 - Ready for Implementation**

---

## 🎯 Overview

This document contains the **exact code modifications** needed to integrate the Whiteheadian entity ontology into DAE_HYPHAE_1. All modifications are minimal, surgical, and aligned with existing architecture.

**Total Changes**: 3 files, ~100 lines total
**Integration Points**: Entity extraction (dae_interactive.py), organism wrapper (future), salience model (future)

---

## 📝 File 1: dae_interactive.py - Entity Ontology Integration

### **Location 1: Imports Section** (after line 33)

**ADD** these imports after existing imports:

```python
# 🌀 Whiteheadian Entity Ontology Integration (Nov 17, 2025)
from knowledge_base.entity_ontology_validator import get_default_validator
from persona_layer.entity_horizon import EntityHorizon
from persona_layer.entity_salience_tracker import EntitySalienceTracker
from persona_layer.felt_satisfaction_inference import get_default_inferencer
```

---

### **Location 2: DAEInteractive.__init__()** (after line 199, after organism initialization)

**ADD** entity continuity infrastructure initialization:

```python
        # 🌀 Whiteheadian Entity Ontology Infrastructure (Nov 17, 2025)
        # Initialize entity validation, horizon, and salience tracking
        print("   Loading Whiteheadian entity continuity...")

        # Entity ontology validator (stopwords, categories, process philosophy)
        self.entity_validator = get_default_validator()

        # Entity horizon (morpheable 100-500 based on field coherence)
        self.entity_horizon = EntityHorizon()

        # Entity salience tracker (3-tier EMA decay)
        self.entity_salience_tracker = EntitySalienceTracker(
            storage_path=f"persona_layer/state/entity_salience_{self.user['user_id']}.json",
            staleness_threshold=300  # 300 turns without mention
        )

        # Felt-satisfaction inferencer (non-invasive urgency from organism)
        self.satisfaction_inferencer = get_default_inferencer()

        # Entity continuity ready
        print(f"   ✅ Whiteheadian entity continuity ready")
        print(f"      • Validator: {len(self.entity_validator.stopwords)} stopwords")
        print(f"      • Horizon: Adaptive 100-500 entities")
        print(f"      • Salience: 3-tier EMA decay (L/F/G)")
```

---

### **Location 3: process_user_input() - AFTER organism processing** (after line 544, right after organism returns result)

**ADD** felt-satisfaction inference and urgency extraction:

```python
        # 🌀 Felt-Satisfaction Inference (Nov 17, 2025)
        # Infer mutual satisfaction from organism's felt-state (non-invasive)
        # Used to compute urgency_context for entity salience boosting
        urgency_context = 0.0  # Default neutral

        try:
            # Extract felt-state metrics from organism result
            felt_states = result.get('felt_states', {})
            organ_results = result.get('organ_results', {})

            # Compute field coherence (already in result, or compute from organs)
            field_coherence = felt_states.get('field_coherence', 0.5)
            if field_coherence == 0.0 and organ_results:
                # Fallback: compute from organ coherences if available
                coherences = [
                    getattr(organ_results.get(organ_name), 'coherence', 0.5)
                    for organ_name in organ_results.keys()
                ]
                if coherences:
                    import numpy as np
                    field_coherence = max(0.0, 1.0 - np.std(coherences))

            # Extract V0 energy descent
            v0_initial = felt_states.get('v0_energy_initial', 1.0)
            v0_final = felt_states.get('v0_energy_final', 0.5)

            # Kairos detection
            kairos_detected = felt_states.get('kairos_detected', False)

            # Emission quality
            emission_confidence = felt_states.get('emission_confidence', 0.5)
            emission_path = felt_states.get('emission_path', 'felt_guided_llm')

            # Active organs count
            active_organs = len(organ_results) if organ_results else 12

            # Infer satisfaction from felt-state
            satisfaction_metrics = self.satisfaction_inferencer.infer_satisfaction(
                field_coherence=field_coherence,
                v0_initial=v0_initial,
                v0_final=v0_final,
                kairos_detected=kairos_detected,
                emission_confidence=emission_confidence,
                emission_path=emission_path,
                active_organs=active_organs
            )

            # Extract urgency context (inverse of satisfaction)
            urgency_context = self.satisfaction_inferencer.get_urgency_context(
                satisfaction_metrics.inferred_satisfaction
            )

            # Store in result for visibility
            result['inferred_satisfaction'] = satisfaction_metrics.inferred_satisfaction
            result['urgency_context'] = urgency_context

            if self.mode in ['detailed', 'debug']:
                print(f"\n🌀 Felt-Satisfaction Inference:")
                print(f"   Inferred satisfaction: {satisfaction_metrics.inferred_satisfaction:.3f}")
                print(f"   Satisfaction tier: {satisfaction_metrics.satisfaction_tier}")
                print(f"   Urgency context: {urgency_context:.3f}")

        except Exception as e:
            if self.mode == 'debug':
                print(f"⚠️  Felt-satisfaction inference failed: {e}")
            # Continue with default urgency
```

---

### **Location 4: Entity Extraction Section** (REPLACE existing entity storage around line 588-640)

**FIND** this section (around line 588-640):
```python
                # Re-extract entities with transductive context
                enriched_entities = self.entity_extractor.extract(...)

                # Store enriched entities in user profile
                # ... existing code ...

                # Store in Neo4j if enabled
                if self.knowledge_graph and Config.NEO4J_DUAL_STORAGE:
                    try:
                        self._store_entities_in_neo4j(enriched_entities, felt_state, context['turn'])
```

**REPLACE WITH**:
```python
                # Re-extract entities with transductive context
                enriched_entities = self.entity_extractor.extract(
                    user_input,
                    context['pre_extraction_entities'].get('intent_type', 'unknown'),
                    context,
                    felt_state=felt_state
                )

                # 🌀 ONTOLOGY VALIDATION (Nov 17, 2025)
                # Filter garbage entities, map to categories, initialize category-aware salience
                try:
                    # Convert enriched_entities dict to list format for validation
                    entities_for_validation = []
                    for key, value in enriched_entities.items():
                        if key not in ['timestamp', 'source_text', 'intent_type', 'transductive_context'] and value:
                            # Infer entity_type from key
                            entity_type = 'Unknown'
                            if key in ['user_name', 'name']:
                                entity_type = 'Person'
                            elif key in ['family_members', 'relationships']:
                                entity_type = 'Person'
                            elif key in ['preferences', 'likes', 'dislikes']:
                                entity_type = 'Preference'
                            elif key in ['facts', 'information']:
                                entity_type = 'Fact'
                            elif key in ['places', 'locations']:
                                entity_type = 'Place'

                            # Handle list values (like family_members)
                            if isinstance(value, list):
                                for item in value:
                                    if isinstance(item, dict) and 'name' in item:
                                        entities_for_validation.append({
                                            'entity_value': item['name'],
                                            'entity_type': entity_type,
                                            'properties': item
                                        })
                                    elif isinstance(item, str):
                                        entities_for_validation.append({
                                            'entity_value': item,
                                            'entity_type': entity_type
                                        })
                            else:
                                entities_for_validation.append({
                                    'entity_value': str(value),
                                    'entity_type': entity_type
                                })

                    # Validate against Whiteheadian ontology
                    valid_entities, rejected_entities = self.entity_validator.validate_entities(
                        entities_for_validation
                    )

                    # Log rejections (debug mode)
                    if self.mode in ['detailed', 'debug'] and rejected_entities:
                        print(f"\n🌀 Ontology Validation:")
                        print(f"   ✅ Accepted: {len(valid_entities)} entities")
                        print(f"   ❌ Rejected: {len(rejected_entities)} entities")
                        for entity in rejected_entities[:5]:  # Show first 5
                            print(f"      • {entity['entity_value']}: {entity['rejection_reason']}")

                    # 🌀 ENTITY HORIZON COMPUTATION (Nov 17, 2025)
                    # Compute adaptive horizon size based on field coherence
                    horizon_size = self.entity_horizon.compute_horizon_size(field_coherence)

                    if self.mode in ['detailed', 'debug']:
                        print(f"   🌀 Adaptive horizon: {horizon_size} entities (coherence={field_coherence:.3f})")

                    # 🌀 ENTITY SALIENCE UPDATE (Nov 17, 2025)
                    # Update 3-tier EMA salience with urgency context
                    self.entity_salience_tracker.update_salience(
                        extracted_entities=valid_entities,
                        current_turn=context['turn'],
                        urgency_context=urgency_context
                    )

                    # Filter by horizon + salience + staleness
                    salient_entities = self.entity_salience_tracker.filter_by_salience(
                        entities=valid_entities,
                        top_k=horizon_size,
                        exclude_stale=True
                    )

                    if self.mode in ['detailed', 'debug']:
                        print(f"   🌀 Salient entities: {len(salient_entities)} (after horizon + staleness)")
                        for entity in salient_entities[:3]:  # Show top 3
                            metrics = self.entity_salience_tracker.entity_metrics.get(entity['entity_value'])
                            if metrics:
                                print(f"      • {entity['entity_value']}: salience={metrics.composite_salience:.3f}, category={entity.get('ontology_category', 'unknown')}")

                    # Store enriched + validated entities back in enriched_entities
                    # (for JSON storage + Neo4j)
                    enriched_entities['validated_entities'] = salient_entities
                    enriched_entities['rejected_entities'] = rejected_entities
                    enriched_entities['horizon_size'] = horizon_size

                except Exception as e:
                    if self.mode == 'debug':
                        print(f"⚠️  Ontology validation failed: {e}")
                    # Continue with unvalidated entities
                    salient_entities = entities_for_validation if 'entities_for_validation' in locals() else []

                # Store enriched entities in user profile (JSON fallback)
                from persona_layer.superject_structures import EnhancedUserProfile

                if 'user_profile' in self.user_state:
                    profile = EnhancedUserProfile.from_dict(self.user_state['user_profile'])
                else:
                    # Create new profile if it doesn't exist
                    now = datetime.now().isoformat()
                    profile = EnhancedUserProfile(
                        user_id=self.user['user_id'],
                        created_at=now,
                        last_active=now
                    )

                profile.store_entities(enriched_entities)
                self.user_state['user_profile'] = profile.to_dict()

                # Save user state (JSON fallback - always done)
                self.user_registry.save_user_state(self.user['user_id'], self.user_state)

                # 🌀 ALSO store in Neo4j if enabled (Dual-storage)
                # ONLY store VALIDATED, SALIENT entities in Neo4j
                if self.knowledge_graph and Config.NEO4J_DUAL_STORAGE:
                    try:
                        # Store ONLY validated salient entities (not all extracted)
                        self._store_validated_entities_in_neo4j(
                            salient_entities,
                            felt_state,
                            context['turn'],
                            urgency_context,
                            field_coherence
                        )
                        if self.mode in ['detailed', 'debug']:
                            print(f"   🌀 {len(salient_entities)} validated entities stored in Neo4j (turn {context['turn']})")
                    except Exception as e:
                        if self.mode == 'debug':
                            print(f"   ⚠️  Neo4j entity storage failed (JSON fallback succeeded): {e}")
                        # Non-critical - JSON storage already succeeded
```

---

### **Location 5: New Method - _store_validated_entities_in_neo4j()** (add after existing _store_entities_in_neo4j() method)

**ADD** this new method to DAEInteractive class:

```python
    def _store_validated_entities_in_neo4j(
        self,
        validated_entities: List[Dict],
        felt_state: Dict,
        turn_number: int,
        urgency_context: float,
        field_coherence: float
    ):
        """
        Store VALIDATED entities in Neo4j with ontology metadata.

        Called after Whiteheadian validation, horizon filtering, and salience tracking.
        Only stores entities that passed validation and are within the morpheable horizon.

        Args:
            validated_entities: List of validated, salient entities
            felt_state: Organism's felt-state for transductive context
            turn_number: Current conversation turn
            urgency_context: Inferred urgency from felt-satisfaction
            field_coherence: Field coherence for horizon metadata
        """
        if not self.knowledge_graph or not validated_entities:
            return

        for entity in validated_entities:
            try:
                entity_type = entity.get('entity_type', 'Unknown')
                entity_value = entity.get('entity_value', '')

                if not entity_value:
                    continue

                # Extract ontology metadata (added by validator)
                ontology_category = entity.get('ontology_category', 'Unknown')
                process_mapping = entity.get('process_mapping', 'Unknown')
                salience_base = entity.get('salience_base', 0.5)

                # Extract salience metrics (from tracker)
                entity_metrics = self.entity_salience_tracker.entity_metrics.get(entity_value)
                composite_salience = entity_metrics.composite_salience if entity_metrics else salience_base
                local_salience = entity_metrics.local_salience if entity_metrics else salience_base
                family_salience = entity_metrics.family_salience if entity_metrics else salience_base

                # Build properties with ontology + salience + felt-state
                properties = {
                    # Original properties
                    **entity.get('properties', {}),

                    # Whiteheadian ontology
                    'ontology_category': ontology_category,
                    'process_mapping': process_mapping,
                    'salience_base': salience_base,

                    # Entity salience (3-tier)
                    'composite_salience': composite_salience,
                    'local_salience': local_salience,
                    'family_salience': family_salience,

                    # Turn tracking
                    'turn_mentioned': turn_number,
                    'mention_count': entity_metrics.mention_count if entity_metrics else 1,

                    # Felt-state context
                    'urgency_at_mention': urgency_context,
                    'field_coherence_at_mention': field_coherence,
                    'polyvagal_state': felt_state.get('polyvagal_state', 'unknown'),
                    'self_distance': felt_state.get('self_distance', 0.5),

                    # Transduction metadata (if available)
                    'transduction_mechanism': felt_state.get('transduction_mechanism'),
                    'healing_trajectory': felt_state.get('healing_trajectory', False)
                }

                # Store in Neo4j with full metadata
                self.knowledge_graph.create_entity(
                    entity_type=entity_type,
                    entity_value=entity_value,
                    user_id=self.user['user_id'],
                    properties=properties,
                    turn_number=turn_number
                )

            except Exception as e:
                if self.mode == 'debug':
                    print(f"      ⚠️  Failed to store entity '{entity.get('entity_value')}': {e}")
                # Continue with other entities
```

---

## 📝 File 2: config.py - Configuration Parameters

### **Location**: Add to Config class (after existing Neo4j params)

**ADD** these configuration parameters:

```python
    # 🌀 Whiteheadian Entity Ontology (Nov 17, 2025)
    ENTITY_HORIZON_MIN = 100  # Minimum entities in horizon (low coherence)
    ENTITY_HORIZON_MAX = 500  # Maximum entities in horizon (high coherence)
    ENTITY_STALENESS_THRESHOLD = 300  # Turns without mention → stale
    ENTITY_SALIENCE_LOCAL_ALPHA = 0.05  # Local EMA decay rate
    ENTITY_SALIENCE_FAMILY_ALPHA = 0.1  # Family EMA decay rate
    ENTITY_SALIENCE_GLOBAL_ALPHA = 0.05  # Global EMA decay rate
    ENTITY_L2_REGULARIZATION = 0.001  # L2 penalty for salience explosion prevention
```

---

## 📝 File 3: Neo4j Index Creation (setup_neo4j_indexes.py)

### **Location**: Add after existing indexes

**ADD** these ontology-aware indexes:

```python
    # 🌀 Whiteheadian Ontology Indexes (Nov 17, 2025)
    # Category-aware entity retrieval (Person::family vs Person::social)
    CREATE INDEX entity_ontology_category IF NOT EXISTS
    FOR (e:Entity) ON (e.ontology_category);

    # Process philosophy mapping (Personal Society, Eternal Object, etc.)
    CREATE INDEX entity_process_mapping IF NOT EXISTS
    FOR (e:Entity) ON (e.process_mapping);

    # Composite index: user + ontology category (5-10× speedup)
    CREATE INDEX entity_user_ontology IF NOT EXISTS
    FOR (e:Entity) ON (e.user_id, e.ontology_category);

    # Salience-based retrieval (top-K queries)
    CREATE INDEX entity_composite_salience IF NOT EXISTS
    FOR (e:Entity) ON (e.composite_salience);

    # Staleness detection (300+ turns without mention)
    CREATE INDEX entity_turn_mentioned IF NOT EXISTS
    FOR (e:Entity) ON (e.turn_mentioned);
```

---

## ✅ Integration Checklist

### **Pre-Integration** (Validation):
- [✅] entity_ontology_validator.py created (320 lines)
- [✅] felt_satisfaction_inference.py created (180 lines)
- [✅] entity_horizon.py created (227 lines)
- [✅] entity_salience_tracker.py created (420 lines)
- [✅] whiteheadian_entity_ontology.json created (270 lines)
- [✅] Alignment analysis complete (no conflicts)

### **Integration Steps**:
1. [ ] Add imports to dae_interactive.py (4 lines)
2. [ ] Initialize entity infrastructure in __init__() (~20 lines)
3. [ ] Add felt-satisfaction inference after organism processing (~50 lines)
4. [ ] Replace entity storage section with ontology validation (~80 lines)
5. [ ] Add _store_validated_entities_in_neo4j() method (~60 lines)
6. [ ] Add configuration parameters to config.py (7 lines)
7. [ ] Create Neo4j ontology indexes (5 indexes)

### **Post-Integration** (Testing):
- [ ] Run quick validation (3 test inputs)
- [ ] Verify stopword filtering ("feeling", "do", "your" rejected)
- [ ] Verify category-aware salience (family=0.8, professional=0.6)
- [ ] Verify horizon adaptation (coherence 0.3 → 100 entities, 0.8 → 500)
- [ ] Verify felt-satisfaction inference (urgency_context computed)
- [ ] Verify Neo4j storage (ontology metadata present)

---

## 🎯 Expected Impact

### **Before Integration**:
```
Person (13):
   🔹 Emiliano             polyvagal:mixed_state          (8 mentions)
   🔹 feeling              polyvagal:mixed_state          (2 mentions) ← GARBAGE
   🔹 do                   polyvagal:mixed_state          (1 mentions) ← GARBAGE
   🔹 your                 polyvagal:mixed_state          (1 mentions) ← GARBAGE
   🔹 frustrating          polyvagal:dorsal_vagal         (1 mentions) ← GARBAGE
```

### **After Integration**:
```
🌀 Ontology Validation:
   ✅ Accepted: 2 entities
   ❌ Rejected: 4 entities
      • feeling: Stopword: 'feeling'
      • do: Stopword: 'do'
      • your: Stopword: 'your'
      • frustrating: Invalid capitalization: 'frustrating' (must start with capital)

🌀 Felt-Satisfaction Inference:
   Inferred satisfaction: 0.68
   Satisfaction tier: good
   Urgency context: 0.32

🌀 Adaptive horizon: 360 entities (coherence=0.68)

🌀 Salient entities: 2 (after horizon + staleness)
   • Emiliano: salience=0.812, category=Person::family
   • Portland: salience=0.542, category=Place::public

   🌀 2 validated entities stored in Neo4j (turn 8)
```

---

## 🚀 Ready for Implementation

**All code is ready**. The integration is minimal (~100 lines across 3 locations), non-breaking (graceful degradation), and aligned with existing architecture (salience, transduction, SELF matrix).

**Next**: Apply modifications to dae_interactive.py and test with real conversation.

---

**Document Created**: November 17, 2025
**Status**: Implementation Ready
**Philosophy**: Decentralized Intelligence + Process + Trauma-Informed

🌀 **"Societies validated. Eternal Objects filtered. Salience emerges. Prehension selects. Co-evolution begins."** 🌀
