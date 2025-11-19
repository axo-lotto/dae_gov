"""
Transductive Felt Entity Filter - Process-Philosophy Aligned
============================================================

Replaces static heuristics with 4-layer learnable filtering:
- Layer 0: BOND IFS Parts Gate (IFS parts-aware pre-filtering)
- Layer 1: SELF Matrix Gate (therapeutic appropriateness)
- Layer 2: Salience Model + Entity Salience Tracker (process terms + temporal decay)
- Layer 3: Satisfaction Fingerprinting + Regime Modulation (trajectory awareness)

Philosophy: Entity storage is not keyword-based (LLM extraction) but
felt-based (BOND parts + organ activation + salience + trajectory + therapeutic appropriateness).

Date: November 18, 2025
Author: DAE_HYPHAE_1 + Claude Code
"""

from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import re

from persona_layer.self_matrix_governance import SELFMatrixGovernance, SELFZoneState
from persona_layer.conversational_salience_model import ConversationalSalienceModel
from persona_layer.entity_salience_tracker import EntitySalienceTracker
from persona_layer.satisfaction_fingerprinting import SatisfactionFingerprintClassifier
from persona_layer.epoch_training.satisfaction_regime import SatisfactionRegime


class TransductiveFeltEntityFilter:
    """
    4-Layer transductive entity filtering with learnable, trauma-aware mechanisms.

    Philosophy: Entity storage is not keyword-based (LLM extraction) but
    felt-based (organ activation + salience + trajectory + therapeutic appropriateness).

    Layers:
    0. BOND IFS Parts Gate: IFS parts-aware pre-filtering (120+ keywords)
    1. SELF Matrix Gate: Zone-based therapeutic appropriateness (IFS + Polyvagal)
    2. Salience Model + Entity Salience Tracker: 20 process terms + 3-tier temporal decay
    3. Satisfaction Fingerprinting + Regime Modulation: Trajectory-aware + adaptive thresholds
    """

    def __init__(
        self,
        self_matrix_governance: SELFMatrixGovernance,
        salience_model: ConversationalSalienceModel,
        entity_salience_tracker: EntitySalienceTracker,
        satisfaction_classifier: SatisfactionFingerprintClassifier,
        bond_config = None,
        enable_layer0: bool = True,
        enable_layer1: bool = True,
        enable_layer2: bool = True,
        enable_layer3: bool = True
    ):
        """
        Initialize transductive entity filter.

        Args:
            self_matrix_governance: SELF Matrix for zone-based gating
            salience_model: 20-term salience model for process-aware scoring
            entity_salience_tracker: 3-tier EMA temporal decay tracker
            satisfaction_classifier: Satisfaction fingerprint classifier
            bond_config: BOND organ config for IFS keyword access (optional)
            enable_layer0: Enable BOND IFS Parts Gate
            enable_layer1: Enable SELF Matrix gate
            enable_layer2: Enable Salience Model + Entity Salience Tracker
            enable_layer3: Enable Satisfaction Fingerprinting + Regime Modulation
        """
        self.self_matrix = self_matrix_governance
        self.salience_model = salience_model
        self.entity_salience_tracker = entity_salience_tracker
        self.satisfaction_classifier = satisfaction_classifier
        self.bond_config = bond_config

        self.enable_layer0 = enable_layer0
        self.enable_layer1 = enable_layer1
        self.enable_layer2 = enable_layer2
        self.enable_layer3 = enable_layer3

        # Tracking
        self.turn_number = 0
        self.filter_history = []

        # Load BOND IFS keywords if available
        if bond_config:
            self._load_bond_keywords()
        else:
            self.bond_keywords = {}

    def _load_bond_keywords(self):
        """Load BOND's 120+ IFS keywords for parts detection."""
        try:
            from organs.modular.bond.organ_config.bond_config import BONDConfig

            config = BONDConfig()
            self.bond_keywords = {
                'manager': config.manager_keywords if hasattr(config, 'manager_keywords') else [],
                'firefighter': config.firefighter_keywords if hasattr(config, 'firefighter_keywords') else [],
                'exile': config.exile_keywords if hasattr(config, 'exile_keywords') else [],
                'self_energy': config.self_energy_keywords if hasattr(config, 'self_energy_keywords') else []
            }
        except Exception as e:
            print(f"⚠️  Could not load BOND keywords: {e}")
            self.bond_keywords = {}

    def filter_entities_transductively(
        self,
        candidate_entities: List[Dict[str, Any]],
        bond_result: Any = None,
        zone: SELFZoneState = None,
        prehension: Dict[str, Any] = None,
        satisfaction_trace: List[float] = None,
        regime: Optional[SatisfactionRegime] = None,
        existing_entities: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Filter entities through 4-layer transductive architecture.

        Args:
            candidate_entities: Entities extracted by LLM
            bond_result: BOND organ result (for Layer 0 IFS parts gate)
            zone: Current SELF zone state (from BOND organ, for Layer 1)
            prehension: Full organism prehension (organ results, meta-atoms, etc.)
            satisfaction_trace: Recent satisfaction history (last 10 turns)
            regime: Current satisfaction regime (optional, for Layer 3B)
            existing_entities: User's existing entity ecosystem (for Layer 2B)

        Returns:
            filtered_entities: Entities that passed all enabled layers
            filter_metadata: Detailed filtering metrics
        """
        metadata = {
            'initial_count': len(candidate_entities),
            'layer0_filtered': 0,
            'layer1_filtered': 0,
            'layer2_filtered': 0,
            'layer3_filtered': 0,
            'final_count': 0,
            'layers_enabled': {
                'layer0': self.enable_layer0,
                'layer1': self.enable_layer1,
                'layer2': self.enable_layer2,
                'layer3': self.enable_layer3
            }
        }

        entities = candidate_entities.copy()

        # LAYER 0: BOND IFS Parts Gate (IFS parts-aware pre-filtering)
        if self.enable_layer0 and bond_result:
            entities, layer0_meta = self.layer0_bond_ifs_parts_gate(entities, bond_result)
            metadata['layer0_filtered'] = layer0_meta['entities_filtered']
            metadata['layer0_ifs_detected'] = layer0_meta['ifs_entities_detected']

        # LAYER 1: SELF Matrix Gate (Therapeutic Appropriateness)
        if self.enable_layer1 and zone:
            entities, layer1_meta = self.layer1_zone_gate(entities, zone)
            metadata['layer1_filtered'] = layer1_meta['entities_filtered']
            metadata['layer1_zone'] = layer1_meta['zone_name']

        # LAYER 2: Salience Model + Entity Salience Tracker
        if self.enable_layer2 and len(entities) > 0 and prehension:
            # 2A: Process term scoring
            salience_results = self.salience_model.evaluate(prehension)
            entities = self.layer2a_process_term_scoring(
                entities, salience_results, prehension, bond_result
            )

            # 2B: Temporal decay filtering
            pre_layer2b = len(entities)
            entities = self.layer2b_temporal_decay_filtering(entities, zone)
            metadata['layer2_filtered'] = pre_layer2b - len(entities)

        # LAYER 3: Satisfaction Fingerprinting + Regime Modulation
        if self.enable_layer3 and len(entities) > 0 and satisfaction_trace and len(satisfaction_trace) >= 3:
            # 3A: Archetype adjustment
            entities = self.layer3a_archetype_adjustment(entities, satisfaction_trace)

            # 3B: Regime threshold
            if regime:
                pre_layer3b = len(entities)
                entities = self.layer3b_regime_threshold(entities, regime)
                metadata['layer3_filtered'] = pre_layer3b - len(entities)

        metadata['final_count'] = len(entities)
        metadata['total_filtered'] = metadata['initial_count'] - metadata['final_count']
        metadata['filter_rate'] = (
            metadata['total_filtered'] / metadata['initial_count']
            if metadata['initial_count'] > 0 else 0.0
        )

        # Track history
        self.turn_number += 1
        self.filter_history.append(metadata)

        return entities, metadata

    # ============================================================================
    # LAYER 0: BOND IFS Parts Gate (IFS Parts-Aware Pre-Filtering)
    # ============================================================================

    def layer0_bond_ifs_parts_gate(
        self,
        candidate_entities: List[Dict],
        bond_result: Any
    ) -> Tuple[List[Dict], Dict]:
        """
        Gate entity storage based on BOND IFS parts detection.

        Strategy:
        1. Classify entities as IFS parts entities ("my inner critic", "my anxiety")
        2. Enrich with parts metadata (part_type, self_distance context)
        3. Gate based on parts appropriateness:
           - Exile entities: Only store in safe zones (Zone 1-3)
           - Firefighter entities: Avoid storing in Zone 5 (crisis)
           - SELF resource entities: Always store (healing resource)
        """
        # Step 1: Classify IFS parts entities
        entities_with_parts = self._classify_ifs_entities(
            candidate_entities,
            bond_result
        )

        # Step 2: Gate based on parts type + self-distance
        filtered = []
        mean_self_distance = getattr(bond_result, 'mean_self_distance', 0.5)

        for entity in entities_with_parts:
            entity_type = entity.get('entity_type', 'Unknown')

            # Zone 5 (Exile/Collapse, self_distance 0.60-1.0)
            if mean_self_distance >= 0.60:
                # ONLY SELF resources (grounding anchors)
                if entity_type == 'IFS_SELF_Resource':
                    filtered.append(entity)

            # Zone 4 (Shadow/Compost, self_distance 0.35-0.60)
            elif mean_self_distance >= 0.35:
                # NO exile entities (avoid retriggering trauma)
                if entity_type != 'IFS_Exile_Part':
                    filtered.append(entity)

            # Zone 1-3 (Safe zones, self_distance 0.0-0.35)
            else:
                # Store ALL entities
                filtered.append(entity)

        metadata = {
            'bond_self_distance': mean_self_distance,
            'bond_dominant_part': getattr(bond_result, 'dominant_part', None),
            'ifs_entities_detected': sum(1 for e in entities_with_parts
                                         if e.get('entity_type', '').startswith('IFS_')),
            'entities_filtered': len(candidate_entities) - len(filtered)
        }

        return filtered, metadata

    def _classify_ifs_entities(
        self,
        entities: List[Dict],
        bond_result: Any
    ) -> List[Dict]:
        """
        Classify entities as IFS parts entities using BOND's keyword matching.

        Strategy:
        1. Check for explicit parts patterns ("part of me", "my inner X")
        2. Match against BOND's 120+ IFS keywords
        3. Assign part type based on keyword domain
        4. Enrich with parts metadata from BOND
        """
        # Explicit parts language patterns
        ifs_patterns = {
            'explicit_part': r'part of me|a part that|this part|my (\w+) part',
            'inner_voice': r'my inner (\w+)|the voice that|something in me',
            'parts_blending': r'part of me wants .+ but .+ part',
            'unblending': r'I notice|I\'m aware of|there\'s a part'
        }

        enriched = []

        for entity in entities:
            entity_text = entity.get('value', '') or entity.get('name', '')
            if not entity_text:
                enriched.append(entity)
                continue

            entity_lower = entity_text.lower()

            # Check for explicit parts patterns
            is_parts_entity = False
            for pattern_name, pattern in ifs_patterns.items():
                if re.search(pattern, entity_lower):
                    is_parts_entity = True
                    break

            # Classify part type using BOND keywords
            detected_part_type = None
            if is_parts_entity and self.bond_keywords:
                for part_type, keywords in self.bond_keywords.items():
                    if any(keyword in entity_lower for keyword in keywords):
                        detected_part_type = part_type
                        break

            # Enrich entity with IFS metadata
            entity['ifs_metadata'] = {
                'is_parts_entity': is_parts_entity,
                'part_type': detected_part_type,
                'context_self_distance': getattr(bond_result, 'mean_self_distance', 0.5),
                'context_dominant_part': getattr(bond_result, 'dominant_part', None),
                'bond_atom_activations': getattr(bond_result, 'atom_activations', {})
            }

            # Update entity_type if IFS parts entity
            if is_parts_entity and detected_part_type:
                entity['entity_type'] = f'IFS_{detected_part_type.title()}_Part'

                # Store BOND-derived self-distance
                part_self_distances = {
                    'manager': 0.25,
                    'firefighter': 0.50,
                    'exile': 0.60,
                    'self_energy': 0.00
                }
                entity['entity_self_distance'] = part_self_distances.get(detected_part_type, 0.5)

            enriched.append(entity)

        return enriched

    # ============================================================================
    # LAYER 1: SELF Matrix Gate (Therapeutic Appropriateness)
    # ============================================================================

    def layer1_zone_gate(
        self,
        candidate_entities: List[Dict],
        zone: SELFZoneState
    ) -> Tuple[List[Dict], Dict]:
        """
        Gate entity storage based on SELF zone.

        Zone-based entity gating:
        - Zone 1-2 (0.0-0.25): Store ALL entities
        - Zone 3 (0.25-0.35): Store with caution flags
        - Zone 4 (0.35-0.60): Only protective/grounding entities
        - Zone 5 (0.60-1.0): MINIMAL (emergency contacts, grounding anchors only)
        """
        if zone.zone_id >= 5:
            # Zone 5: Only crisis-relevant entities
            filtered = [e for e in candidate_entities
                       if e.get('entity_type') in ['Emergency_Contact', 'Grounding_Anchor', 'IFS_SELF_Resource']]

        elif zone.zone_id >= 4:
            # Zone 4: No relational depth, no exile parts (firefighters active)
            filtered = [e for e in candidate_entities
                       if e.get('entity_type') not in ['Relationship', 'Past_Trauma', 'Deep_Exploration', 'IFS_Exile_Part']]

        elif zone.zone_id >= 3:
            # Zone 3: Store with caution flags
            filtered = candidate_entities.copy()
            for e in filtered:
                e['zone_caution'] = True

        else:
            # Zone 1-2: Store all
            filtered = candidate_entities

        metadata = {
            'zone_id': zone.zone_id,
            'zone_name': zone.zone_name,
            'filter_reason': zone.therapeutic_stance,
            'entities_filtered': len(candidate_entities) - len(filtered)
        }

        return filtered, metadata

    # ============================================================================
    # LAYER 2A: Process Term Scoring (BOND-Aware Salience)
    # ============================================================================

    def layer2a_process_term_scoring(
        self,
        entities: List[Dict],
        salience_results: Dict,
        prehension: Dict,
        bond_result: Any = None
    ) -> List[Dict]:
        """
        Score entities using BOND parts context + salience model.

        OLD (static heuristic):
            if entity_lower in ['bullied', 'sad', 'anxious']:
                salience += 0.6  # HARDCODED

        NEW (BOND-aware):
            salience = f(bond_atom_activation, part_type, self_distance, process_terms)
        """
        trauma_markers = salience_results.get('trauma_markers', {})
        guidance = salience_results.get('morphogenetic_guidance', 'hold_diffuse')
        process_terms = salience_results.get('process_terms', {})

        atom_activations = getattr(bond_result, 'atom_activations', {}) if bond_result else {}

        for entity in entities:
            entity_type = entity.get('entity_type', 'Unknown')
            ifs_metadata = entity.get('ifs_metadata', {})

            # Base salience by entity type
            base_salience = {
                'Person': 0.7,
                'Place': 0.5,
                'Preference': 0.4,
                'Fact': 0.3,
                'IFS_SELF_Resource': 0.95,      # Always high (healing resource)
                'IFS_Manager_Part': 0.65,
                'IFS_Firefighter_Part': 0.85,   # High crisis relevance
                'IFS_Exile_Part': 0.75,
                'Emotion': 0.70
            }.get(entity_type, 0.5)

            # BOND atom activation modulation
            part_type = ifs_metadata.get('part_type')

            # Boost entities that match active BOND parts
            if bond_result and atom_activations:
                if part_type == 'manager' and atom_activations.get('manager_parts', 0) > 0.5:
                    base_salience *= 1.3
                elif part_type == 'firefighter' and atom_activations.get('firefighter_parts', 0) > 0.7:
                    base_salience *= 1.5  # High crisis urgency
                elif part_type == 'exile' and atom_activations.get('exile_parts', 0) > 0.6:
                    base_salience *= 1.2
                elif part_type == 'self_energy' and atom_activations.get('SELF_energy', 0) > 0.6:
                    base_salience *= 1.4  # Healing resource

            # Salience model trauma markers modulation
            signal_inflation = trauma_markers.get('signal_inflation', 0.0)
            if signal_inflation > 0.7:
                # HIGH TRAUMA: Boost grounding, dampen exploration
                if entity_type in ['IFS_SELF_Resource', 'IFS_Manager_Part', 'Grounding_Anchor']:
                    base_salience *= 1.2
                elif entity_type in ['IFS_Exile_Part', 'Past_Trauma']:
                    base_salience *= 0.6  # Avoid retriggering

            # Safety gradient modulation
            safety_gradient = trauma_markers.get('safety_gradient', 0.5)
            if safety_gradient < 0.4:
                # NARROW WINDOW: Filter exploratory entities
                if entity_type in ['Deep_Exploration', 'Relationship']:
                    base_salience *= 0.6

            # Morphogenetic guidance modulation
            if guidance == 'crystallize_insight':
                # READY FOR INSIGHT: Boost all entities
                base_salience *= 1.2
            elif guidance == 'hold_diffuse':
                # NOT READY: More conservative
                base_salience *= 0.8

            # Temporal collapse modulation
            temporal_collapse = process_terms.get('temporal_collapse', 0.0)
            if temporal_collapse > 0.6 and entity.get('temporal_context') == 'past':
                # Don't store historical entities during temporal collapse
                base_salience *= 0.4

            # Relational recurrence modulation
            relational_recurrence = process_terms.get('relational_recurrence', 0.0)
            if relational_recurrence > 0.6 and entity_type == 'Relationship':
                # Boost relational entities during healing spirals
                base_salience *= 1.4

            # Self-distance proximity boost
            self_distance = ifs_metadata.get('context_self_distance', 0.5)
            proximity_to_self = 1.0 - self_distance

            final_salience = base_salience * (0.7 + 0.3 * proximity_to_self)
            entity['process_score'] = min(1.0, final_salience)

        return entities

    # ============================================================================
    # LAYER 2B: Temporal Decay Filtering (3-Tier EMA)
    # ============================================================================

    def layer2b_temporal_decay_filtering(
        self,
        entities: List[Dict],
        zone: SELFZoneState = None
    ) -> List[Dict]:
        """
        Apply 3-tier temporal decay + zone-aware top-K.

        Uses EntitySalienceTracker's 3-tier EMA:
        - Local salience (α=0.05, entity-specific, fast)
        - Family salience (α=0.1, relationship type, medium)
        - Global salience (α=0.05, cross-entity theme, slow)
        """
        # Update salience for current turn
        self.entity_salience_tracker.update_salience(
            extracted_entities=entities,
            current_turn=self.turn_number,
            urgency_context=getattr(zone, 'zone_id', 3) if zone else 3
        )

        # Zone-aware top-K filtering
        if zone:
            zone_top_k = {
                1: 20,  # Core SELF: Rich entity storage
                2: 15,  # Inner Relational: Moderate storage
                3: 10,  # Symbolic Threshold: Selective storage
                4: 5,   # Shadow/Compost: Minimal storage
                5: 3    # Exile/Collapse: Emergency only
            }
            top_k = zone_top_k.get(zone.zone_id, 10)
        else:
            top_k = 10

        # Filter by composite salience (3-tier EMA)
        filtered = self.entity_salience_tracker.filter_by_salience(
            entities=entities,
            top_k=top_k,
            remove_stale=True  # Remove entities not mentioned in 300+ turns
        )

        return filtered

    # ============================================================================
    # LAYER 3A: Satisfaction Fingerprinting (Archetype-Based Quality Adjustment)
    # ============================================================================

    def layer3a_archetype_adjustment(
        self,
        entities: List[Dict],
        satisfaction_trace: List[float]
    ) -> List[Dict]:
        """
        Adjust entity confidence based on satisfaction trajectory archetype.

        Archetypes (FFITTSS proven: +8-12pp quality):
        - CRISIS: -0.20 (reject bad entity storage)
        - RESTORATIVE: +0.15 (Kairos bonus)
        - CONCRESCENT: +0.10 (convergence boost)
        - PULL: -0.05 (volatility penalty)
        - STABLE: 0.0 (neutral)
        """
        fingerprint = self.satisfaction_classifier.classify(satisfaction_trace)

        # Apply archetype-based adjustment
        for entity in entities:
            base_confidence = entity.get('process_score', 0.5)

            if fingerprint.archetype == 'CRISIS':
                # REJECT entity storage during crisis divergence
                entity['trajectory_adjusted_score'] = base_confidence - 0.20
                entity['kairos_context'] = 'crisis'

            elif fingerprint.archetype == 'RESTORATIVE':
                # BOOST entity storage during Kairos moment (crisis → healing)
                entity['trajectory_adjusted_score'] = base_confidence + 0.15
                entity['kairos_context'] = 'restorative_kairos'
                entity['kairos_bonus'] = True

            elif fingerprint.archetype == 'CONCRESCENT':
                # BOOST entity storage during convergence
                entity['trajectory_adjusted_score'] = base_confidence + 0.10
                entity['kairos_context'] = 'concrescent'

            elif fingerprint.archetype == 'PULL':
                # PENALTY for volatility
                entity['trajectory_adjusted_score'] = base_confidence - 0.05
                entity['kairos_context'] = 'volatile'

            else:  # STABLE
                # NEUTRAL
                entity['trajectory_adjusted_score'] = base_confidence
                entity['kairos_context'] = 'stable'

            # Clip to valid range
            entity['trajectory_adjusted_score'] = np.clip(
                entity['trajectory_adjusted_score'], 0.0, 1.0
            )

        return entities

    # ============================================================================
    # LAYER 3B: Regime-Based Adaptive Thresholds
    # ============================================================================

    def layer3b_regime_threshold(
        self,
        entities: List[Dict],
        regime: SatisfactionRegime
    ) -> List[Dict]:
        """
        Apply regime-based adaptive threshold.

        Adaptive thresholds based on learning state:
        - INITIALIZING: 0.8 (very cautious)
        - EXPLORING: 0.6 (moderate)
        - CONVERGING: 0.5 (permissive)
        - STABLE: 0.7 (quality focus)
        - COMMITTED: 0.5 (confident)
        - PLATEAUED: 0.3 (aggressive exploration)
        """
        regime_thresholds = {
            SatisfactionRegime.INITIALIZING: 0.8,
            SatisfactionRegime.EXPLORING: 0.6,
            SatisfactionRegime.CONVERGING: 0.5,
            SatisfactionRegime.STABLE: 0.7,
            SatisfactionRegime.COMMITTED: 0.5,
            SatisfactionRegime.PLATEAUED: 0.3
        }

        threshold = regime_thresholds.get(regime, 0.6)

        # Filter entities based on adaptive threshold
        filtered = [
            e for e in entities
            if e.get('trajectory_adjusted_score', 0.0) >= threshold
        ]

        return filtered


def get_transductive_felt_entity_filter(
    self_matrix_governance: SELFMatrixGovernance = None,
    salience_model: ConversationalSalienceModel = None,
    entity_salience_tracker: EntitySalienceTracker = None,
    satisfaction_classifier: SatisfactionFingerprintClassifier = None,
    enable_layer0: bool = True,
    enable_layer1: bool = True,
    enable_layer2: bool = True,
    enable_layer3: bool = True
) -> TransductiveFeltEntityFilter:
    """
    Get transductive felt entity filter with default initialization.

    Args:
        self_matrix_governance: SELF Matrix (if None, creates new instance)
        salience_model: Salience model (if None, creates new instance)
        entity_salience_tracker: Entity salience tracker (if None, creates new instance)
        satisfaction_classifier: Satisfaction classifier (if None, creates new instance)
        enable_layer0: Enable BOND IFS Parts Gate
        enable_layer1: Enable SELF Matrix gate
        enable_layer2: Enable Salience Model + Entity Salience Tracker
        enable_layer3: Enable Satisfaction Fingerprinting + Regime Modulation

    Returns:
        TransductiveFeltEntityFilter instance
    """
    # Create default instances if not provided
    if self_matrix_governance is None:
        # Use placeholder path for coherent attractors (can be empty/missing for testing)
        coherent_attractors_path = "persona_layer/state/active/coherent_attractors.json"
        self_matrix_governance = SELFMatrixGovernance(coherent_attractors_path=coherent_attractors_path)

    if salience_model is None:
        salience_model = ConversationalSalienceModel()

    if entity_salience_tracker is None:
        entity_salience_tracker = EntitySalienceTracker(
            storage_path="persona_layer/state/active/entity_salience.json"
        )

    if satisfaction_classifier is None:
        from persona_layer.satisfaction_fingerprinting import SatisfactionFingerprintClassifier
        satisfaction_classifier = SatisfactionFingerprintClassifier()

    return TransductiveFeltEntityFilter(
        self_matrix_governance=self_matrix_governance,
        salience_model=salience_model,
        entity_salience_tracker=entity_salience_tracker,
        satisfaction_classifier=satisfaction_classifier,
        enable_layer0=enable_layer0,
        enable_layer1=enable_layer1,
        enable_layer2=enable_layer2,
        enable_layer3=enable_layer3
    )
