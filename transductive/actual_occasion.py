"""
Actual Occasion - Universal process class for all entities in tECS

Based on DAE1.0 and Spora Explora v2 patterns.
Every entity is an occasion of experience that prehends, concresces, and satisfies.
Follows the proven pattern from the legacy implementations.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import time
import numpy as np
from .vector10d import Vector10D
from .subjective_aim import SubjectiveAim

# Import Vector35D for enhanced intelligence
try:
    from .physical_feeling_duality_vector35d import PhysicalFeelingDualityVector35D
    VECTOR35D_AVAILABLE = True
except ImportError:
    VECTOR35D_AVAILABLE = False


@dataclass  
class ActualOccasion:
    """
    Universal building block of symbolic field - follows DAE1.0 pattern
    
    An ActualOccasion represents a discrete symbolic event or entity
    that can be prehended (interpreted) by multiple organs from different
    perspectives, following Whitehead's process philosophy.
    
    This is the concrete implementation, not abstract.
    """
    
    # ESSENTIAL CORE DATA (from DAE1.0 pattern)
    position: Tuple = field(default_factory=tuple)  # Where in space/time/context
    symbol: str = ""                                # Primary symbolic content
    
    # UNIVERSAL PROPERTIES  
    properties: Dict[str, Any] = field(default_factory=dict)  # Domain-specific data
    confidence: float = 1.0                                   # Certainty about data
    
    # PREHENSIVE STRUCTURE (key to multi-organ intelligence)
    prehensions: Dict[str, Any] = field(default_factory=dict)           # Organ interpretations
    symbolic_vectors: Dict[str, Vector10D] = field(default_factory=dict) # 10D representations
    
    # RELATIONAL CONTEXT (from DAE1.0)
    relations: List[Tuple] = field(default_factory=list)  # Connections to other AOs
    temporal_order: Optional[int] = None                  # Position in sequence
    
    # PROCESS PHILOSOPHY STATE (from Spora v2 pattern)
    entity_id: str = ""
    creation_time: float = field(default_factory=time.time)
    satisfaction_level: float = 0.0
    coherence: float = 0.75  # 🔥 BUG FIX #1 (Oct 30): Default to "ready" state for Kairos detection (was 0.0, causing 100% readiness failures)
    vitality: float = 1.0

    # OPTION C: Multi-Cycle Satisfaction Tracking (Phase 3.3B, Oct 28, 2025)
    satisfaction_history: List[float] = field(default_factory=list)  # Per-cycle satisfaction values
    satisfaction_variance: float = 0.0  # Temporal variance computed after convergence

    # T(x) CYCLE COMPONENTS
    current_vector: Optional[Vector10D] = None    # Where occasion currently is
    feeling_vector: Optional[Vector10D] = None    # Where occasion feels pulled toward
    subjective_aim: Optional[SubjectiveAim] = None

    # OCCASION 3: Vector35D Enhanced Intelligence Support
    vector: Optional[Any] = None  # PhysicalFeelingDualityVector35D when available
    
    # GENEALOGY AND HISTORY
    prehension_history: List[Dict] = field(default_factory=list)
    genealogy: List[str] = field(default_factory=list)

    # NEIGHBOR AWARENESS FOR ENTITY CLUSTERING (NAVI Phase 2)
    neighbor_affinities: Dict[str, float] = field(default_factory=dict)  # entity_id -> affinity
    nearby_entities: List[Tuple[str, float]] = field(default_factory=list)  # sorted by affinity
    nexus_membership: Optional[str] = None  # Which nexus this entity belongs to
    affinity_threshold: float = 0.5  # Minimum affinity to be "neighbor"

    # GROUND TRUTH FEEDBACK FOR LEARNING (NAVI Phase 2)
    ground_truth_feedback: Dict[str, Any] = field(default_factory=dict)  # accuracy, metadata
    is_correct: bool = False
    learned_from_feedback: bool = False
    feedback_history: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize the occasion's becoming - follows Spora v2 pattern"""
        if not self.entity_id:
            self.entity_id = f"AO_{id(self)}_{self.creation_time}"
        
        # Initialize vectors if not provided
        if not self.current_vector:
            self.current_vector = Vector10D()
        if not self.feeling_vector:
            self.feeling_vector = Vector10D()
        
        # Initialize subjective aim
        if not self.subjective_aim:
            self.subjective_aim = SubjectiveAim()
        
        self.emit_signal("occasion_created", {"id": self.entity_id})

        # Initialize Vector35D if available - OCCASION 3 ENHANCEMENT
        self._initialize_vector35d_if_available()
    
    def prehend(self, organ_name: str, interpretation: Any) -> None:
        """
        Allow an organ to add its interpretation of this occasion
        Follows DAE1.0 pattern for multi-organ prehension
        
        Args:
            organ_name: Which organ is interpreting (SANS, BOND, etc.)
            interpretation: The organ's interpretation (any data structure)
        """
        self.prehensions[organ_name] = interpretation
        
        # Record in prehension history
        prehension_record = {
            "time": time.time(),
            "organ": organ_name,
            "interpretation": interpretation,
            "coherence": self.coherence
        }
        self.prehension_history.append(prehension_record)
    
    def add_symbolic_vector(self, organ_name: str, vector: Vector10D) -> None:
        """
        Store the 10D symbolic vector representation from an organ
        Follows DAE1.0 pattern
        
        Args:
            organ_name: Which organ created this vector
            vector: The 10D symbolic vector
        """
        self.symbolic_vectors[organ_name] = vector
        # Link vector to this occasion's position
        vector.properties = vector.properties or {}
        vector.properties["source_organ"] = organ_name
        vector.properties["position"] = self.position
    
    def concrescence(self, prehensions: Optional[Dict[str, Any]] = None) -> None:
        """
        Integrate prehensions into coherent becoming.
        This is the T(x) process of achieving satisfaction.
        Follows Spora v2 pattern but simplified for ARC tasks.
        """
        if prehensions:
            # Update prehensions
            for organ_name, interpretation in prehensions.items():
                self.prehend(organ_name, interpretation)
        
        # Simple concrescence process
        self.update_coherence()
        self.move_toward_satisfaction()
        
        # Emit signal for completion
        self.emit_signal("concrescence_completed", {
            "satisfaction": self.satisfaction_level,
            "coherence": self.coherence
        })
    
    def update_coherence(self) -> float:
        """
        Calculate coherence across all organ interpretations
        Uses symbolic vectors to measure how much organs agree
        Follows DAE1.0 coherence pattern
        """
        if len(self.symbolic_vectors) < 2:
            self.coherence = 1.0  # Single or no interpretation = perfect coherence
            return self.coherence
            
        vectors = list(self.symbolic_vectors.values())
        total_coherence = 0.0
        comparisons = 0
        
        # Calculate pairwise coherence between all organ vectors
        for i, vec1 in enumerate(vectors):
            for vec2 in vectors[i+1:]:
                coherence_score = vec1.calculate_coherence_with(vec2)
                total_coherence += coherence_score
                comparisons += 1
                
        self.coherence = total_coherence / comparisons if comparisons > 0 else 1.0
        return self.coherence
    
    def move_toward_satisfaction(self, ground_truth_value=None, feedback_system=None) -> None:
        """
        Move toward satisfaction - ENHANCED with pattern commitment feeling

        Week 1 Phase 2 (Oct 26, 2025): Felt-integrated ground truth learning
        - Entities learn through full felt scaffolding
        - SubjectiveAim pattern confidence (not raw intensity)
        - AppetitionState TRUTH_SEEKING updates
        - Vector35D satisfaction_history accumulation
        - V0 resonance learning preparation

        Args:
            ground_truth_value: Optional ground truth symbol for training feedback
            feedback_system: Optional EnhancedGroundTruthFeedbackSystem for felt learning
        """
        if not self.current_vector or not self.feeling_vector:
            return

        # ENHANCEMENT: Activate feeling vector processing based on pattern recognition
        self._activate_pattern_feeling()

        # Calculate direction toward satisfaction
        if self.subjective_aim:
            satisfaction_direction = self.subjective_aim.calculate_aim_direction(
                self.current_vector, self.feeling_vector
            )

            # ENHANCED: Scale attraction strength based on feeling activation
            feeling_strength = self._calculate_feeling_strength()
            base_attraction = 0.1
            enhanced_attraction = base_attraction * (1.0 + feeling_strength * 2.0)  # Up to 3x stronger

            for i in range(len(self.current_vector.dimensions)):
                self.current_vector.dimensions[i] += (
                    satisfaction_direction.dimensions[i] * enhanced_attraction
                )

        # ENHANCED: Update satisfaction level with feeling component
        feeling_bonus = self._calculate_feeling_satisfaction_bonus()
        base_satisfaction = self.coherence * self.vitality
        self.satisfaction_level = min(1.0, base_satisfaction + feeling_bonus)

        # 🆕 FELT-INTEGRATED GROUND TRUTH LEARNING (Oct 26, 2025)
        # Replaces simple intensity multiplication (Week 1 Phase 2) with
        # full felt scaffolding integration (SubjectiveAim pattern confidence,
        # AppetitionState TRUTH_SEEKING, Vector35D satisfaction_history)
        if ground_truth_value is not None and feedback_system is not None:
            # Calculate accuracy for this entity
            is_correct = (self.symbol == ground_truth_value)
            accuracy = 1.0 if is_correct else 0.0

            # Use felt-integrated feedback system (replaces simple approach)
            # This updates:
            # 1. TRUTH_SEEKING appetition (accuracy → satisfaction/hunger)
            # 2. SubjectiveAim pattern confidence (not raw intensity)
            # 3. Vector35D satisfaction_history (dims 15-19)
            # 4. Marks entity for V0 resonance learning
            task_result = {
                'entity_symbol': self.symbol,
                'ground_truth': ground_truth_value,
                'pattern_type': self.properties.get('pattern_type', 'unknown')
            }

            feedback_system._update_felt_scaffolding(self, accuracy, task_result)

            # Legacy property storage for compatibility
            self.set_property('ground_truth_correct', is_correct)
            self.set_property('ground_truth_accuracy', accuracy)
    
    def get_prehension(self, organ_name: str) -> Optional[Any]:
        """Get a specific organ's interpretation of this occasion"""
        return self.prehensions.get(organ_name)
    
    def get_symbolic_vector(self, organ_name: str) -> Optional[Vector10D]:
        """Get a specific organ's 10D vector representation"""
        return self.symbolic_vectors.get(organ_name)
    
    def coherence_score(self) -> float:
        """Get current coherence score - DAE1.0 compatibility"""
        return self.coherence
    
    def add_relation(self, relation_type: str, target_position: Tuple, strength: float = 1.0) -> None:
        """
        Add a relationship to another ActualOccasion
        Follows DAE1.0 relation pattern
        
        Args:
            relation_type: Type of relationship (adjacent, contains, transforms_to, etc.)
            target_position: Position of the related occasion
            strength: Strength of the relationship [0.0, 1.0]
        """
        self.relations.append((relation_type, target_position, strength))
    
    def get_relations(self, relation_type: Optional[str] = None) -> List[Tuple]:
        """Get all relations, optionally filtered by type"""
        if relation_type is None:
            return self.relations
        return [rel for rel in self.relations if rel[0] == relation_type]
    
    def has_prehension_from(self, organ_name: str) -> bool:
        """Check if a specific organ has interpreted this occasion"""
        return organ_name in self.prehensions
    
    def active_organs(self) -> List[str]:
        """Get list of organs that have prehended this occasion"""
        return list(self.prehensions.keys())
    
    def set_property(self, key: str, value: Any) -> None:
        """Set a domain-specific property"""
        self.properties[key] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a domain-specific property"""
        return self.properties.get(key, default)

    # =====================================================================
    # NEIGHBOR AWARENESS METHODS (NAVI Phase 2)
    # =====================================================================

    def add_neighbor(self, neighbor_id: str, affinity_score: float) -> None:
        """Register neighbor with affinity score"""
        self.neighbor_affinities[neighbor_id] = affinity_score
        self._update_nearby_entities_list()

    def _update_nearby_entities_list(self) -> None:
        """Keep nearby_entities sorted by affinity"""
        self.nearby_entities = sorted(
            self.neighbor_affinities.items(),
            key=lambda x: x[1],
            reverse=True
        )

    def get_neighborhood(self, threshold: Optional[float] = None) -> List[str]:
        """Get neighbors above affinity threshold"""
        if threshold is None:
            threshold = self.affinity_threshold
        return [eid for eid, affinity in self.neighbor_affinities.items()
                if affinity >= threshold]

    def calculate_neighborhood_coherence(self) -> float:
        """Average coherence of neighborhood"""
        if not self.nearby_entities:
            return 0.0
        # This will be populated by orchestrator with neighbor coherences
        avg_neighborhood_coherence = sum(
            self.neighbor_affinities.values()
        ) / len(self.neighbor_affinities)
        return avg_neighborhood_coherence

    def get_neighbors_sorted_by_coherence(self) -> List[Tuple[str, float]]:
        """Get neighbors ordered by affinity (proxy for coherence)"""
        return self.nearby_entities

    def receive_ground_truth_feedback(self, accuracy: float,
                                      metadata: Dict[str, Any]) -> None:
        """Learn from task outcome"""
        self.ground_truth_feedback['accuracy'] = accuracy
        self.ground_truth_feedback['is_correct'] = accuracy > 0.85
        self.ground_truth_feedback['timestamp'] = time.time()
        self.ground_truth_feedback['metadata'] = metadata

        self.is_correct = accuracy > 0.85
        self.learned_from_feedback = True

        # Track history
        self.feedback_history.append({
            'accuracy': accuracy,
            'is_correct': self.is_correct,
            'timestamp': self.ground_truth_feedback['timestamp']
        })

        # Adjust satisfaction based on correctness
        if accuracy > 0.85:
            # Reinforce successful pattern
            self.satisfaction_level = min(1.0, self.satisfaction_level * 1.1)
            if self.subjective_aim:
                self.subjective_aim.satisfaction_history.append(0.9)
        elif accuracy < 0.5:
            # Course correct when failing
            self.satisfaction_level = max(0.0, self.satisfaction_level * 0.9)
            if self.subjective_aim:
                self.subjective_aim.satisfaction_history.append(0.3)

        # Add feedback marker to genealogy
        self.genealogy.append(f"feedback:{self.ground_truth_feedback['timestamp']}")

    # =====================================================================
    # END NEIGHBOR AWARENESS METHODS
    # =====================================================================

    # =====================================================================
    # ENTITY-NATIVE PROPOSITION/AFFORDANCE METHODS (Nov 1, 2025)
    # Propositions as intrinsic prehensions, not external organ outputs
    # =====================================================================

    def prehend_with_affordances(
        self,
        organ_name: str,
        interpretation: Any,
        affordances: List[Dict[str, Any]],
        cycle: int,
        organ_coherence: float
    ) -> None:
        """
        Store organ interpretation + felt affordances in entity prehension.

        This implements propositions as native entity prehensions - organs don't
        generate propositions externally, but express felt possibilities WITHIN
        the entity's becoming.

        Args:
            organ_name: Which organ is prehending (NDAM, SANS, etc.)
            interpretation: Organ's analysis/interpretation
            affordances: List of felt possibilities (proto-propositions)
                Each affordance: {
                    'proposed_value': int,
                    'lure_intensity': float,
                    'organ_specific_score': float,
                    'reasoning': Optional[str],
                    'cycle_generated': int,
                    'immature': True,  # Needs maturation
                    'salience_score': 0.0,  # Will accumulate
                    'prehension_count': 0  # How many times prehended
                }
            cycle: Current processing cycle
            organ_coherence: Organ's coherence at prehension time
        """
        # Store interpretation + affordances together
        self.prehensions[organ_name] = {
            'interpretation': interpretation,
            'felt_affordances': affordances,
            'coherence': organ_coherence,
            'cycle': cycle,
            'timestamp': time.time()
        }

        # Record in prehension history
        prehension_record = {
            "time": time.time(),
            "organ": organ_name,
            "interpretation": interpretation,
            "affordance_count": len(affordances),
            "coherence": organ_coherence,
            "cycle": cycle
        }
        self.prehension_history.append(prehension_record)

        # Mark affordances with entity genealogy
        for affordance in affordances:
            affordance['entity_id'] = self.entity_id
            affordance['entity_position'] = self.position

    def accumulate_affordance_salience(
        self,
        organism_state: Dict[str, Any],
        salience_weights: Optional[Dict[str, float]] = None
    ) -> None:
        """
        Affordances prehend organism state during entity concrescence.

        This is the key integration point - as the entity undergoes concrescence
        across cycles, its affordances accumulate salience from the evolving
        organism state (V0 energy, EO archetypes, coherence field, etc.).

        Args:
            organism_state: Current state with:
                - v0_energy: V0 ground state energy
                - v0_gradient: V0 energy gradient
                - eo_archetypes: EO archetypal activations
                - coherence_field: Hybrid coherence field state
                - subjective_aim: Collective aim (if active)
                - kairos_gates: Kairos gate states
                - satisfaction: Current satisfaction
                - cycle: Current cycle number
            salience_weights: Optional weights for salience terms
        """
        # Compute salience signals from organism state
        salience_signals = self._compute_salience_signals(
            organism_state, salience_weights
        )

        # Each organ's affordances prehend the organism state
        for organ_name, prehension_data in self.prehensions.items():
            if not isinstance(prehension_data, dict):
                continue

            affordances = prehension_data.get('felt_affordances', [])

            for affordance in affordances:
                if affordance.get('immature', True):
                    # Affordance integrates salience signals
                    weighted_salience = self._integrate_salience_for_affordance(
                        affordance, salience_signals, salience_weights
                    )

                    # Accumulate
                    affordance['salience_score'] = affordance.get('salience_score', 0.0) + weighted_salience
                    affordance['prehension_count'] = affordance.get('prehension_count', 0) + 1

    def mature_affordances_to_propositions(
        self,
        mature_organism_state: Dict[str, Any],
        calculate_organic_confidence_fn: callable
    ) -> List[Any]:
        """
        Convert immature affordances to mature propositions with organism intelligence.

        This happens POST-CONVERGENCE when V0 has reached mature state:
        - V0 energy near minimum (e.g., 0.293 vs 1.0 at Cycle 1)
        - V0 phase = CONCRESCENCE
        - Satisfaction calibrated

        Each affordance calculates confidence NOW with MATURE context.

        Args:
            mature_organism_state: Post-convergence state with:
                - v0_context: Mature V0 context (energy, gradient, phase)
                - v0_spatial_field: V0 spatial field values
                - organ_coherences: Final organ coherences
            calculate_organic_confidence_fn: Function to calculate confidence

        Returns:
            List of mature Proposition objects ready for application
        """
        from organs.shared.propositions import Proposition, PropositionType

        matured_propositions = []
        mature_v0_context = mature_organism_state.get('v0_context', {})
        v0_spatial_field = mature_organism_state.get('v0_spatial_field')

        for organ_name, prehension_data in self.prehensions.items():
            if not isinstance(prehension_data, dict):
                continue

            affordances = prehension_data.get('felt_affordances', [])
            organ_coherence = prehension_data.get('coherence', 0.5)

            for affordance in affordances:
                if not affordance.get('immature', True):
                    continue  # Already matured

                # Get V0 spatial field value for this position
                v0_field_value = 0.0
                if v0_spatial_field is not None:
                    try:
                        row, col = self.position
                        if row < v0_spatial_field.shape[0] and col < v0_spatial_field.shape[1]:
                            v0_field_value = float(v0_spatial_field[row, col])
                    except:
                        pass

                # Calculate organic confidence with MATURE V0 context
                confidence = calculate_organic_confidence_fn(
                    position=self.position,
                    organ_coherence=organ_coherence,
                    organ_specific_score=affordance.get('organ_specific_score', 0.5),
                    v0_context=mature_v0_context,
                    v0_spatial_field_value=v0_field_value
                )

                # Modulate by accumulated salience
                prehension_count = affordance.get('prehension_count', 1)
                avg_salience = affordance.get('salience_score', 0.0) / max(1, prehension_count)
                salience_modulation = np.clip(avg_salience, 0.5, 1.5)
                confidence *= salience_modulation
                confidence = np.clip(confidence, 0.0, 1.0)

                # Map organ name to proposition type
                proposition_type_map = {
                    'NDAM': PropositionType.CONSTRAINT_SATISFACTION,
                    'SANS': PropositionType.SEMANTIC_ENHANCEMENT,
                    'BOND': PropositionType.SPATIAL_TRANSFORMATION,
                    'RNX': PropositionType.TEMPORAL_PREDICTION,
                    'EO': PropositionType.COLOR_TRANSFORMATION,
                    'CARD': PropositionType.SCALING_PATTERN
                }
                prop_type = proposition_type_map.get(organ_name, PropositionType.SPATIAL_TRANSFORMATION)

                # Create mature Proposition with entity lineage
                prop = Proposition(
                    position=self.position,
                    organ_name=organ_name,
                    proposition_type=prop_type,
                    proposed_value=affordance.get('proposed_value', 0),
                    confidence=confidence,
                    lure_intensity=affordance.get('lure_intensity', 0.5),
                    source_pattern=affordance.get('reasoning', 'entity_prehension'),
                    metadata={
                        # Entity lineage
                        'entity_id': self.entity_id,
                        'entity_coherence': self.coherence,
                        'entity_satisfaction': self.satisfaction_level,
                        'entity_genealogy': self.genealogy.copy(),

                        # Affordance lifecycle
                        'cycle_generated': affordance.get('cycle_generated', 1),
                        'prehension_count': prehension_count,
                        'avg_salience': avg_salience,
                        'salience_modulation': salience_modulation,

                        # V0 context at maturation
                        'v0_energy_at_maturation': mature_v0_context.get('energy', 1.0),
                        'v0_phase_at_maturation': mature_v0_context.get('phase', 'unknown'),

                        # Organ-specific score preserved
                        'organ_specific_score': affordance.get('organ_specific_score', 0.5)
                    }
                )

                # Set organ-specific score attribute
                organ_score_attr = f"{organ_name.lower()}_score"
                if hasattr(prop, organ_score_attr):
                    setattr(prop, organ_score_attr, affordance.get('organ_specific_score', 0.5))

                # Mark as matured
                affordance['immature'] = False
                affordance['confidence'] = confidence

                matured_propositions.append(prop)

        return matured_propositions

    def _compute_salience_signals(
        self,
        organism_state: Dict[str, Any],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, float]:
        """
        Compute salience signals from organism state.

        15 integrated salience terms from unified architecture:
        - V0 Navigation (3): energy_proximity, gradient_strength, trajectory_confidence
        - EO Archetypal (3): lure_intensity, family_coherence, transformation_match
        - Hybrid Coherence (3): field_resonance, organ_harmony, coupled_synergy
        - Subjective Aim (3): collective_alignment, lure_congruence, phase_fit
        - Kairos (3): window_proximity, variance_adequacy, gate_readiness
        """
        signals = {}

        # V0 NAVIGATION
        v0_energy = organism_state.get('v0_energy', 1.0)
        v0_gradient = organism_state.get('v0_gradient', 0.0)

        signals['v0_energy_proximity'] = 1.0 - v0_energy  # Closer to ground truth
        signals['v0_gradient_strength'] = abs(v0_gradient)
        signals['v0_trajectory_confidence'] = 0.5  # Placeholder (would track descent)

        # EO ARCHETYPAL RESONANCE
        eo_archetypes = organism_state.get('eo_archetypes', {})
        if eo_archetypes:
            activations = [float(v) for v in eo_archetypes.values() if isinstance(v, (int, float))]
            signals['archetypal_lure_intensity'] = max(activations) if activations else 0.5
            if len(activations) > 1:
                variance = np.var(activations)
                signals['archetype_family_coherence'] = 1.0 - min(variance, 1.0)
            else:
                signals['archetype_family_coherence'] = 0.5
            signals['transformation_archetype_match'] = 0.5  # Placeholder
        else:
            signals['archetypal_lure_intensity'] = 0.5
            signals['archetype_family_coherence'] = 0.5
            signals['transformation_archetype_match'] = 0.5

        # HYBRID COHERENCE
        coherence_field = organism_state.get('coherence_field', {})
        coh_cross = coherence_field.get('coh_cross', 0.5)
        coh_safe = coherence_field.get('coh_safe', 0.5)
        signals['field_resonance'] = coh_cross * coh_safe
        signals['organ_harmony'] = 0.3 if coherence_field.get('multi_organ_crisis') else 0.8
        signals['coupled_organ_synergy'] = coherence_field.get('coupled_strength', 0.5)

        # SUBJECTIVE AIM
        subjective_aim = organism_state.get('subjective_aim')
        if subjective_aim:
            signals['collective_aim_alignment'] = subjective_aim.get('alignment', 0.5)
            signals['aim_lure_congruence'] = subjective_aim.get('lure_congruence', 0.5)
            signals['appetitive_phase_fit'] = subjective_aim.get('phase_fit', 0.5)
        else:
            signals['collective_aim_alignment'] = 0.5
            signals['aim_lure_congruence'] = 0.5
            signals['appetitive_phase_fit'] = 0.5

        # KAIROS
        kairos_gates = organism_state.get('kairos_gates', {})
        satisfaction = organism_state.get('satisfaction', 0.5)

        # Satisfaction window [0.45, 0.70]
        if 0.45 <= satisfaction <= 0.70:
            signals['satisfaction_window_proximity'] = 1.0
        else:
            if satisfaction < 0.45:
                signals['satisfaction_window_proximity'] = satisfaction / 0.45
            else:
                signals['satisfaction_window_proximity'] = 1.0 - min((satisfaction - 0.70) / 0.30, 1.0)

        signals['variance_adequacy'] = 0.8 if kairos_gates.get('variance_sufficient') else 0.3
        gates_passing = sum(1 for v in kairos_gates.values() if v)
        total_gates = len(kairos_gates) if kairos_gates else 5
        signals['gate_readiness'] = gates_passing / total_gates if total_gates > 0 else 0.5

        return signals

    def _integrate_salience_for_affordance(
        self,
        affordance: Dict[str, Any],
        salience_signals: Dict[str, float],
        weights: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Integrate salience signals for an affordance with weighted sum.

        Default weights (can be overridden):
        - V0 Navigation: 1.5, 1.2, 1.0 (high - ground truth pull)
        - EO Archetypal: 1.3, 1.0, 1.1 (high - pattern attractors)
        - Hybrid Coherence: 0.9, 0.8, 0.7 (medium)
        - Subjective Aim: 1.0, 0.9, 0.8 (medium)
        - Kairos: 0.5, 0.4, 0.6 (lower - timing not generation)
        """
        default_weights = {
            'v0_energy_proximity': 1.5,
            'v0_gradient_strength': 1.2,
            'v0_trajectory_confidence': 1.0,
            'archetypal_lure_intensity': 1.3,
            'archetype_family_coherence': 1.0,
            'transformation_archetype_match': 1.1,
            'field_resonance': 0.9,
            'organ_harmony': 0.8,
            'coupled_organ_synergy': 0.7,
            'collective_aim_alignment': 1.0,
            'aim_lure_congruence': 0.9,
            'appetitive_phase_fit': 0.8,
            'satisfaction_window_proximity': 0.5,
            'variance_adequacy': 0.4,
            'gate_readiness': 0.6,
        }

        if weights is None:
            weights = default_weights

        weighted_sum = 0.0
        total_weight = 0.0

        for signal_name, signal_value in salience_signals.items():
            weight = weights.get(signal_name, 1.0)
            weighted_sum += signal_value * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.5

    # =====================================================================
    # END ENTITY-NATIVE AFFORDANCE METHODS
    # =====================================================================

    def feel_into(self, data: Any) -> Any:
        """
        Transform raw data through felt experience.
        Not computation but genuine feeling - Spora v2 pattern.
        """
        # Record in prehension history
        prehension = {
            "time": time.time(),
            "data": data,
            "coherence": self.coherence,
            "vitality": self.vitality
        }
        self.prehension_history.append(prehension)
        
        # Feel the data (basic implementation)
        return data
    
    def seek_satisfaction(self) -> bool:
        """Determine if the occasion has achieved satisfaction"""
        return self.satisfaction_level >= 0.8
    
    def _activate_pattern_feeling(self) -> None:
        """
        ENHANCEMENT: Activate feeling vector based on pattern recognition context
        This addresses the zero feeling vector issue found in TSK analysis
        """
        if not self.feeling_vector:
            return
        
        # Check if this occasion is part of pattern recognition
        pattern_context = self._detect_pattern_context()
        
        if pattern_context["has_pattern"]:
            # Activate feeling toward pattern completion
            pattern_strength = pattern_context["strength"]
            
            # Set feeling vector dimensions based on pattern type
            if pattern_context["type"] == "sequence":
                # Feel toward sequence continuation
                self.feeling_vector.pattern_complexity = pattern_strength * 0.8
                self.feeling_vector.transformation_type = pattern_strength * 0.7
                self.feeling_vector.change_dynamics = pattern_strength * 0.6
                
            elif pattern_context["type"] == "spatial":
                # Feel toward spatial completion
                self.feeling_vector.spatial_form = pattern_strength * 0.8
                self.feeling_vector.spatial_relation = pattern_strength * 0.7
                self.feeling_vector.interaction_potential = pattern_strength * 0.6
                
            # General pattern feeling activation
            self.feeling_vector.symbolic_role = pattern_strength * 0.5
            self.feeling_vector.semantic_intensity = pattern_strength * 0.4
    
    def _detect_pattern_context(self) -> Dict[str, Any]:
        """Detect if this occasion is part of a recognizable pattern"""
        pattern_info = {
            "has_pattern": False,
            "type": "none",
            "strength": 0.0
        }
        
        # Check for sequence patterns (look in properties for BOND sequence info)
        if "sequence_pattern" in self.properties:
            sequence_data = self.properties["sequence_pattern"]
            if sequence_data.get("strength", 0.0) > 0.4:
                pattern_info = {
                    "has_pattern": True,
                    "type": "sequence", 
                    "strength": sequence_data["strength"]
                }
        
        # Check for spatial patterns
        if "spatial_coherence" in self.properties:
            spatial_coherence = self.properties["spatial_coherence"]
            if spatial_coherence > 0.6:
                pattern_info = {
                    "has_pattern": True,
                    "type": "spatial",
                    "strength": spatial_coherence
                }
        
        # Check for organ consensus (multiple organs detecting same pattern)
        organ_agreement = self._calculate_organ_pattern_agreement()
        if organ_agreement > 0.7:
            if not pattern_info["has_pattern"]:
                pattern_info = {
                    "has_pattern": True,
                    "type": "consensus",
                    "strength": organ_agreement
                }
        
        return pattern_info
    
    def _calculate_organ_pattern_agreement(self) -> float:
        """Calculate how much organs agree on pattern recognition"""
        if len(self.symbolic_vectors) < 2:
            return 0.0
        
        # Look for pattern-related high values across organs
        pattern_dimensions = [2, 3, 8]  # pattern_complexity, spatial_form, transformation_type
        agreements = []
        
        vectors = list(self.symbolic_vectors.values())
        for dim in pattern_dimensions:
            dim_values = [v.dimensions[dim] for v in vectors if len(v.dimensions) > dim]
            if len(dim_values) > 1:
                # High values that are similar = agreement
                avg_val = sum(dim_values) / len(dim_values)
                if avg_val > 0.5:
                    variance = sum((v - avg_val)**2 for v in dim_values) / len(dim_values)
                    agreement = avg_val * (1.0 - min(1.0, variance))
                    agreements.append(agreement)
        
        return sum(agreements) / len(agreements) if agreements else 0.0
    
    def _calculate_feeling_strength(self) -> float:
        """Calculate overall feeling vector activation strength"""
        if not self.feeling_vector:
            return 0.0
        
        # Sum of all non-zero feeling dimensions
        total_feeling = sum(abs(d) for d in self.feeling_vector.dimensions)
        normalized_feeling = min(1.0, total_feeling / 5.0)  # Normalize to 0-1
        
        return normalized_feeling
    
    def _calculate_feeling_satisfaction_bonus(self) -> float:
        """Calculate satisfaction bonus from active feeling processing"""
        feeling_strength = self._calculate_feeling_strength()
        
        # Strong feelings contribute to satisfaction when they align with coherence
        if feeling_strength > 0.3 and self.coherence > 0.6:
            # Feeling + coherence = higher satisfaction (pattern commitment)
            return feeling_strength * 0.2  # Up to 20% bonus
        
        return 0.0
    
    def emit_signal(self, signal_type: str, data: Dict[str, Any]) -> None:
        """
        Emit signals for tier communication.
        No direct references, only signals - follows 3-tier compliance.
        """
        # In actual implementation, this would connect to event bus
        signal_data = {
            "type": signal_type,
            "source": self.entity_id,
            "data": data,
            "time": time.time()
        }
        # EventBus.emit(signal_data)  # Placeholder
        
    def add_to_genealogy(self, ancestor_id: str) -> None:
        """Track genealogical relationships between occasions"""
        self.genealogy.append(ancestor_id)
    
    def get_entity_type(self) -> str:
        """Return entity type - override in subclasses"""
        return "actual_occasion"
    
    def stimulate_vitality(self, amount: float) -> None:
        """Increase vitality by amount - Spora v2 pattern"""
        self.vitality = min(self.vitality + amount, 2.0)
        self.coherence = min(self.coherence + amount * 0.1, 1.0)
    
    def __str__(self) -> str:
        """Human-readable representation - DAE1.0 pattern"""
        organs = ", ".join(self.active_organs())
        return f"AO(pos={self.position}, symbol='{self.symbol}', organs=[{organs}], coherence={self.coherence:.2f})"
    
    def __repr__(self) -> str:
        return self.__str__()

    def _initialize_vector35d_if_available(self) -> None:
        """Initialize Vector35D for enhanced intelligence bundle access - OCCASION 3"""
        if not VECTOR35D_AVAILABLE:
            return

        # Only create Vector35D if we have position and symbol information
        if not self.position or len(self.position) < 2:
            return

        try:
            # Extract position and color information
            row, col = self.position[:2]

            # Convert symbol to color value (ARC uses 0-9)
            color_value = 0
            if self.symbol.isdigit():
                color_value = int(self.symbol)
            elif hasattr(self, 'properties') and 'color' in self.properties:
                color_prop = self.properties['color']
                if isinstance(color_prop, (int, float)):
                    color_value = int(color_prop)

            # Determine grid shape from context or use reasonable default
            grid_shape = (15, 15)  # Default for ARC-like tasks
            if hasattr(self, 'properties') and 'grid_shape' in self.properties:
                grid_shape = self.properties['grid_shape']

            # Create Vector35D with enhanced intelligence bundles
            self.vector = PhysicalFeelingDualityVector35D(
                position=(row, col),
                color_value=color_value,
                grid_shape=grid_shape
            )

            # 🔥 STAGE 1: Cluster-Aware Organ Resonance (Dims 30-34)
            # After Vector35D initialization, modulate organ resonance by cluster-learned weights
            # This provides task-family-appropriate organ biases for Stage 2 reconstruction
            self._apply_cluster_learned_weights()

        except Exception as e:
            # Graceful fallback - Vector35D creation should never break existing functionality
            pass

    def _apply_cluster_learned_weights(self) -> None:
        """
        Apply cluster-learned organ weights to Vector35D dims 30-34 (STAGE 1).

        Modulates organ resonance values by task-family-specific learned weights.
        For example, spatial tasks may boost BOND (dim 32) and reduce SANS (dim 31).

        This enables Stage 2 cluster reconstruction to use task-appropriate organ emphasis.
        """
        # Check if Vector35D is available
        if not self.vector or not hasattr(self.vector, 'dimensions'):
            return

        # Check if entity has cluster membership (nexus_id)
        cluster_id = getattr(self, 'nexus_id', None)

        if not cluster_id:
            # No cluster membership - use default weights (no modulation)
            return

        try:
            # Load cluster-learned weights from coordinator
            from unified_core.cluster_learning_coordinator import ClusterLearningCoordinator

            coordinator = ClusterLearningCoordinator()
            weights = coordinator.get_cluster_weights(
                cluster_id,
                default={'NDAM': 1.0, 'SANS': 1.0, 'BOND': 1.0, 'RNX': 1.0, 'EO': 1.0, 'CARD': 1.0}
            )

            # Apply weights to Vector35D organ resonance dims (30-34)
            # Multiply existing computed resonance by learned weight multipliers
            self.vector.dimensions[30] *= weights['NDAM']  # organ_resonance_ndam
            self.vector.dimensions[31] *= weights['SANS']  # organ_resonance_sans
            self.vector.dimensions[32] *= weights['BOND']  # organ_resonance_bond
            self.vector.dimensions[33] *= weights['RNX']   # organ_resonance_rnx
            self.vector.dimensions[34] *= weights['EO']    # organ_resonance_eo
            # Note: CARD weight available but not used (only 5 dims for organs)

        except Exception as e:
            # Graceful degradation - cluster weight loading should never break entity creation
            pass

    def ensure_vector35d_availability(self) -> bool:
        """Ensure Vector35D is available for bundle access - OCCASION 3 HELPER"""
        if self.vector and hasattr(self.vector, 'spatial_intelligence_bundle'):
            return True

        # Try to initialize if not already done
        self._initialize_vector35d_if_available()

        return self.vector is not None and hasattr(self.vector, 'spatial_intelligence_bundle')

    def calculate_neighbor_affinity(self, neighbors):
        """
        Calculate affinity to neighbors using Vector35D (NAVI Phase 2).

        Args:
            neighbors: List of ActualOccasion instances

        Returns:
            List of (neighbor, affinity_score, fractal_affinity, resonance_affinity) tuples
        """
        from transductive.entity_clustering import EntityClusteringAwareness

        clustering = EntityClusteringAwareness()
        return clustering.calculate_neighbor_affinity(self, neighbors)

    def get_cluster_membership(self):
        """Get cluster/nexus this entity belongs to (NAVI Phase 2)."""
        return getattr(self, 'nexus_id', None)

    def set_cluster_membership(self, nexus_id, nexus_members=None):
        """
        Assign entity to a cluster/nexus (NAVI Phase 2).

        Args:
            nexus_id: Cluster identifier
            nexus_members: Optional list of member entity IDs
        """
        self.nexus_id = nexus_id
        if nexus_members:
            self.nexus_members = nexus_members

    def get_cluster_centroid(self):
        """Get centroid position of this entity's cluster (NAVI Phase 2)."""
        return getattr(self, 'nexus_centroid', None)

    def set_cluster_centroid(self, centroid):
        """Set centroid position of this entity's cluster (NAVI Phase 2)."""
        self.nexus_centroid = centroid


# Factory functions for common use cases - DAE1.0 pattern
def create_grid_occasion(row: int, col: int, color: str, **properties) -> ActualOccasion:
    """Create an ActualOccasion for grid-based tasks (like ARC)"""
    return ActualOccasion(
        position=(row, col),
        symbol=color,
        properties=properties
    )

def create_temporal_occasion(time_step: int, symbol: str, **properties) -> ActualOccasion:
    """Create an ActualOccasion for temporal sequences"""
    return ActualOccasion(
        position=(time_step,),
        symbol=symbol,
        temporal_order=time_step,
        properties=properties
    )

def create_conceptual_occasion(concept: str, context: str = "default", **properties) -> ActualOccasion:
    """Create an ActualOccasion for abstract concepts"""
    return ActualOccasion(
        position=(context,),
        symbol=concept,
        properties=properties
    )