"""
Proposition - Potential patterns of becoming available for prehension

In process philosophy, propositions are not just logical statements but
lures for feeling - potential patterns of actualization that present themselves
to actual occasions during concrescence. They are hybrid entities combining
actual entities (logical subjects) with eternal objects (predicates).

Based on Whitehead's Process and Reality and the tECS architecture.
Propositions are felt possibilities that can be accepted, rejected, or modified.
"""

from typing import Dict, Any, Optional, List, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np
from .vector10d import Vector10D

class PropositionType(Enum):
    """Types of propositions available for prehension"""
    PREDICATIVE = "predicative"           # "X is Y" - simple attribution
    COMPARATIVE = "comparative"           # "X is more/less than Y" - relational
    TEMPORAL = "temporal"                # "X leads to Y" - sequential
    CAUSAL = "causal"                    # "X causes Y" - causal relation
    TRANSFORMATIVE = "transformative"     # "X becomes Y" - change pattern
    EMERGENT = "emergent"                # "X + Y → Z" - novel emergence
    RECURSIVE = "recursive"              # "X contains X" - self-reference
    ARCHETYPAL = "archetypal"            # Eternal object manifestation
    RELATIONAL = "relational"            # Network/connection patterns
    MODAL = "modal"                      # Possibility/necessity patterns

class PropositionTruthValue(Enum):
    """Truth values for propositions in process philosophy"""
    TRUE = "true"                        # Conforming to actuality
    FALSE = "false"                      # Non-conforming to actuality  
    INDETERMINATE = "indeterminate"      # Neither true nor false
    IRRELEVANT = "irrelevant"            # Outside scope of consideration
    EMERGING = "emerging"                # Becoming true through actualization
    POTENTIAL = "potential"              # Could become true under conditions

@dataclass
class LogicalSubject:
    """
    The actual entity or nexus that the proposition is about
    """
    entity_id: str                       # Identifier for the entity
    entity_type: str                     # Type of entity (occasion, nexus, etc.)
    current_state: Dict[str, Any]        # Current state of the entity
    temporal_location: float             # When this entity exists
    vector_representation: np.ndarray    # 10D vector of the entity
    
    def __post_init__(self):
        if len(self.vector_representation) != 10:
            # Pad or truncate to 10 dimensions
            if len(self.vector_representation) < 10:
                self.vector_representation = np.pad(
                    self.vector_representation, 
                    (0, 10 - len(self.vector_representation))
                )
            else:
                self.vector_representation = self.vector_representation[:10]

@dataclass  
class EternalObject:
    """
    The predicate or pattern that could be actualized
    """
    object_id: str                       # Unique identifier
    pattern_type: str                    # Type of pattern (archetype, quality, relation)
    pattern_description: str             # Human-readable description
    vector_form: np.ndarray             # 10D representation of the pattern
    ingression_conditions: Dict[str, Any] # Conditions for manifestation
    stability: float                     # How stable/persistent this pattern is
    novelty_grade: float                # How novel/creative this pattern is
    
    def __post_init__(self):
        if len(self.vector_form) != 10:
            if len(self.vector_form) < 10:
                self.vector_form = np.pad(
                    self.vector_form,
                    (0, 10 - len(self.vector_form))
                )
            else:
                self.vector_form = self.vector_form[:10]

@dataclass
class Proposition:
    """
    A proposition is a lure for feeling - a potential pattern of becoming
    that presents itself to an actual occasion during concrescence.
    
    Structure: Logical Subject + Eternal Object + Propositional Relations
    """
    proposition_id: str
    proposition_type: PropositionType
    logical_subject: LogicalSubject       # What the proposition is about
    eternal_object: EternalObject         # What could be actualized
    propositional_relation: str           # How they relate ("is", "becomes", etc.)
    
    # Felt qualities of the proposition
    lure_intensity: float                 # How attractive/compelling
    relevance_grade: float               # How relevant to current situation  
    feasibility: float                   # How possible to actualize
    coherence_impact: float              # Expected impact on coherence
    novelty_potential: float             # How much novelty would result
    risk_factor: float                   # Potential negative consequences
    
    # Temporal characteristics
    temporal_span: Tuple[float, float]   # (start_time, end_time) for actualization
    urgency: float                       # How time-sensitive
    persistence: float                   # How long the opportunity lasts
    
    # Contextual information
    environmental_conditions: Dict[str, Any]  # Required conditions
    prerequisite_propositions: List[str]      # Other propositions that must be true
    incompatible_propositions: List[str]      # Propositions that conflict
    
    # Truth evaluation
    truth_value: PropositionTruthValue    # Current truth status
    confidence: float                     # Confidence in truth evaluation
    evidence_support: float               # How much evidence supports this
    
    def __post_init__(self):
        # Ensure all probability-like values are in [0,1]
        self.lure_intensity = np.clip(self.lure_intensity, 0.0, 1.0)
        self.relevance_grade = np.clip(self.relevance_grade, 0.0, 1.0)
        self.feasibility = np.clip(self.feasibility, 0.0, 1.0)
        self.confidence = np.clip(self.confidence, 0.0, 1.0)
        self.evidence_support = np.clip(self.evidence_support, 0.0, 1.0)
    
    def get_proposition_vector(self) -> np.ndarray:
        """Get 10D vector representation of this proposition"""
        # Combine logical subject and eternal object vectors
        subject_vector = self.logical_subject.vector_representation
        object_vector = self.eternal_object.vector_form
        
        # Weighted combination based on proposition characteristics
        subject_weight = 0.6  # Subject is primary
        object_weight = 0.4   # Object modifies subject
        
        combined = subject_weight * subject_vector + object_weight * object_vector
        
        # Normalize
        return combined / (np.linalg.norm(combined) + 1e-10)
    
    def calculate_total_appeal(self) -> float:
        """Calculate overall appeal/attractiveness of this proposition"""
        appeal = (
            self.lure_intensity * 0.3 +
            self.relevance_grade * 0.25 +
            self.feasibility * 0.2 +
            self.novelty_potential * 0.15 +
            (1.0 - self.risk_factor) * 0.1  # Lower risk = higher appeal
        )
        
        # Modulate by urgency and confidence
        appeal *= (1.0 + self.urgency * 0.2) * self.confidence
        
        return np.clip(appeal, 0.0, 1.0)
    
    def is_compatible_with(self, other_proposition: 'Proposition') -> bool:
        """Check if this proposition is compatible with another"""
        # Check explicit incompatibilities
        if (other_proposition.proposition_id in self.incompatible_propositions or
            self.proposition_id in other_proposition.incompatible_propositions):
            return False
        
        # Check vector similarity (too similar might be redundant)
        vector_similarity = np.dot(
            self.get_proposition_vector(),
            other_proposition.get_proposition_vector()
        )
        
        # If very similar (>0.95), consider incompatible (redundant)
        if vector_similarity > 0.95:
            return False
        
        # If moderately conflicting (<-0.3), consider incompatible
        if vector_similarity < -0.3:
            return False
        
        return True
    
    def evaluate_truth_relative_to_state(self, current_state: Dict[str, Any]) -> PropositionTruthValue:
        """Evaluate proposition truth value relative to a given state"""
        
        # Get expected post-actualization state
        expected_state = self.predict_actualization_outcome(current_state)
        
        # Compare with current reality
        if self.proposition_type == PropositionType.PREDICATIVE:
            # Check if subject already has the predicate property
            predicate_key = self.eternal_object.object_id
            if predicate_key in current_state:
                current_value = current_state[predicate_key]
                expected_value = expected_state.get(predicate_key, 0.0)
                
                if abs(current_value - expected_value) < 0.1:
                    return PropositionTruthValue.TRUE
                else:
                    return PropositionTruthValue.FALSE
            else:
                return PropositionTruthValue.INDETERMINATE
        
        elif self.proposition_type == PropositionType.TRANSFORMATIVE:
            # Check if transformation conditions are met
            feasibility_met = self.feasibility > 0.6
            conditions_met = all(
                condition in current_state 
                for condition in self.environmental_conditions.keys()
            )
            
            if feasibility_met and conditions_met:
                return PropositionTruthValue.POTENTIAL
            else:
                return PropositionTruthValue.FALSE
        
        elif self.proposition_type == PropositionType.EMERGENT:
            # Emergence depends on precursor conditions
            emergence_readiness = current_state.get("emergence_readiness", 0.0)
            if emergence_readiness > 0.7:
                return PropositionTruthValue.EMERGING
            elif emergence_readiness > 0.4:
                return PropositionTruthValue.POTENTIAL
            else:
                return PropositionTruthValue.FALSE
        
        # Default fallback
        return PropositionTruthValue.INDETERMINATE
    
    def predict_actualization_outcome(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Predict the state that would result from actualizing this proposition"""
        predicted_state = current_state.copy()
        
        # Apply eternal object pattern to logical subject
        if self.proposition_type == PropositionType.PREDICATIVE:
            # Subject gains the eternal object property
            predicate_key = self.eternal_object.object_id
            predicted_state[predicate_key] = self.eternal_object.stability
        
        elif self.proposition_type == PropositionType.TRANSFORMATIVE:
            # Subject undergoes transformation toward eternal object
            transformation_vector = self.eternal_object.vector_form
            current_vector = self.logical_subject.vector_representation
            
            # Blend vectors based on transformation strength
            blend_factor = self.feasibility * self.lure_intensity
            new_vector = (1.0 - blend_factor) * current_vector + blend_factor * transformation_vector
            
            # Update state to reflect transformed vector
            predicted_state["vector_representation"] = new_vector.tolist()
            predicted_state["coherence"] = current_state.get("coherence", 0.5) + self.coherence_impact
        
        elif self.proposition_type == PropositionType.EMERGENT:
            # New properties emerge
            predicted_state["emergent_property"] = self.eternal_object.object_id
            predicted_state["novelty_level"] = current_state.get("novelty_level", 0.0) + self.novelty_potential
            predicted_state["complexity"] = current_state.get("complexity", 0.5) + 0.1
        
        # Apply general coherence impact
        if "coherence" in predicted_state:
            predicted_state["coherence"] = np.clip(
                predicted_state["coherence"] + self.coherence_impact,
                0.0, 1.0
            )
        
        return predicted_state
    
    def get_actualization_requirements(self) -> Dict[str, Any]:
        """Get requirements that must be met for actualization"""
        requirements = {
            "minimum_feasibility": 0.3,
            "minimum_relevance": 0.2,
            "maximum_risk": 0.8,
            "environmental_conditions": self.environmental_conditions,
            "prerequisite_propositions": self.prerequisite_propositions,
            "minimum_confidence": 0.4,
            "temporal_window": self.temporal_span
        }
        
        return requirements

class PropositionGenerator:
    """
    Generates propositions for actual occasions to consider during concrescence
    
    This is a key component of the transductive engine - it creates the menu
    of possibilities that an occasion can choose from during its becoming.
    """
    
    def __init__(self):
        # Eternal object registry - archetypal patterns available for ingression
        self.eternal_objects: Dict[str, EternalObject] = {}
        self._initialize_basic_eternal_objects()
        
        # Proposition templates for different types
        self.proposition_templates: Dict[PropositionType, Dict[str, Any]] = {}
        self._initialize_proposition_templates()
        
        # Generation parameters
        self.max_propositions_per_cycle = 10
        self.relevance_threshold = 0.1
        self.feasibility_threshold = 0.05
        
        # Learning and adaptation
        self.proposition_success_history: Dict[str, List[float]] = {}
        self.pattern_effectiveness: Dict[str, float] = {}
        
        # Context tracking
        self.current_environmental_context: Dict[str, Any] = {}
        self.active_proposition_ids: List[str] = []
    
    def _initialize_basic_eternal_objects(self):
        """Initialize basic eternal objects (archetypal patterns)"""
        
        basic_objects = [
            # Fundamental qualities
            ("coherence", "coherence_attractor", "Pattern of internal harmony", 
             np.array([1,0,0,0,0,0,0,0,0,0]), {"stability": 0.8}, 0.9, 0.1),
            
            ("connection", "relational_bond", "Pattern of connection/relationship",
             np.array([0,1,0,0,0,0,0,0,0,0]), {"proximity": 0.5}, 0.7, 0.3),
            
            ("creativity", "creative_emergence", "Pattern of novel emergence",
             np.array([0,0,1,0,0,0,0,0,0,0]), {"novelty_potential": 0.6}, 0.4, 0.8),
            
            ("stability", "temporal_persistence", "Pattern of persistence over time",
             np.array([0,0,0,1,0,0,0,0,0,0]), {"temporal_coherence": 0.7}, 0.9, 0.2),
            
            ("transcendence", "higher_integration", "Pattern of transcendent unity",
             np.array([0,0,0,0,1,0,0,0,0,0]), {"integration_capacity": 0.8}, 0.6, 0.7),
            
            # Derived qualities
            ("beauty", "aesthetic_harmony", "Pattern of aesthetic satisfaction",
             np.array([0.5,0,0.3,0.2,0,0,0,0,0,0]), {"harmony_resonance": 0.6}, 0.5, 0.6),
            
            ("truth", "epistemic_accuracy", "Pattern of accurate representation", 
             np.array([0.3,0,0,0.4,0,0,0,0.3,0,0]), {"verification": 0.7}, 0.8, 0.3),
            
            ("freedom", "creative_possibility", "Pattern of open possibility",
             np.array([0,0,0.6,0,0.4,0,0,0,0,0]), {"constraint_absence": 0.5}, 0.3, 0.9)
        ]
        
        for obj_id, pattern_type, description, vector, conditions, stability, novelty in basic_objects:
            self.eternal_objects[obj_id] = EternalObject(
                object_id=obj_id,
                pattern_type=pattern_type,
                pattern_description=description,
                vector_form=vector,
                ingression_conditions=conditions,
                stability=stability,
                novelty_grade=novelty
            )
    
    def _initialize_proposition_templates(self):
        """Initialize templates for different proposition types"""
        
        self.proposition_templates = {
            PropositionType.PREDICATIVE: {
                "relation": "is",
                "base_feasibility": 0.7,
                "base_urgency": 0.5,
                "typical_span": 1.0
            },
            
            PropositionType.TRANSFORMATIVE: {
                "relation": "becomes",
                "base_feasibility": 0.5,
                "base_urgency": 0.6,
                "typical_span": 2.0
            },
            
            PropositionType.EMERGENT: {
                "relation": "emerges_as",
                "base_feasibility": 0.3,
                "base_urgency": 0.4,
                "typical_span": 3.0
            },
            
            PropositionType.COMPARATIVE: {
                "relation": "is_more_than",
                "base_feasibility": 0.6,
                "base_urgency": 0.4,
                "typical_span": 1.5
            },
            
            PropositionType.CAUSAL: {
                "relation": "causes",
                "base_feasibility": 0.4,
                "base_urgency": 0.7,
                "typical_span": 2.5
            }
        }
    
    def generate_propositions_for_occasion(self,
                                         logical_subject: LogicalSubject,
                                         current_state: Dict[str, Any],
                                         environmental_context: Dict[str, Any],
                                         subjective_aim_vector: Optional[np.ndarray] = None,
                                         salience_weights: Optional[Dict[str, float]] = None) -> List[Proposition]:
        """
        Generate propositions for an actual occasion to consider
        
        This is the core method that creates the menu of possibilities
        available during concrescence.
        """
        
        self.current_environmental_context = environmental_context
        propositions = []
        
        # Generate different types of propositions
        
        # 1. Predicative propositions (subject IS eternal object)
        predicative_props = self._generate_predicative_propositions(
            logical_subject, current_state, subjective_aim_vector
        )
        propositions.extend(predicative_props)
        
        # 2. Transformative propositions (subject BECOMES eternal object)
        transformative_props = self._generate_transformative_propositions(
            logical_subject, current_state, subjective_aim_vector
        )
        propositions.extend(transformative_props)
        
        # 3. Emergent propositions (something new emerges)
        emergent_props = self._generate_emergent_propositions(
            logical_subject, current_state, environmental_context
        )
        propositions.extend(emergent_props)
        
        # 4. Relational propositions (connections with other entities)
        if "nearby_entities" in environmental_context:
            relational_props = self._generate_relational_propositions(
                logical_subject, environmental_context["nearby_entities"]
            )
            propositions.extend(relational_props)
        
        # Filter by relevance and feasibility
        filtered_propositions = self._filter_propositions(
            propositions, current_state, salience_weights
        )
        
        # Rank by appeal and select top N
        ranked_propositions = sorted(
            filtered_propositions, 
            key=lambda p: p.calculate_total_appeal(),
            reverse=True
        )
        
        # Limit number of propositions
        final_propositions = ranked_propositions[:self.max_propositions_per_cycle]
        
        # Store active proposition IDs
        self.active_proposition_ids = [p.proposition_id for p in final_propositions]
        
        return final_propositions
    
    def _generate_predicative_propositions(self,
                                        logical_subject: LogicalSubject,
                                        current_state: Dict[str, Any],
                                        subjective_aim_vector: Optional[np.ndarray]) -> List[Proposition]:
        """Generate 'X is Y' propositions"""
        propositions = []
        
        for eo_id, eternal_object in self.eternal_objects.items():
            # Skip if subject already strongly has this property
            if eo_id in current_state and current_state[eo_id] > 0.8:
                continue
            
            # Calculate relevance based on subjective aim alignment
            relevance = self._calculate_aim_relevance(eternal_object, subjective_aim_vector)
            
            # Calculate feasibility based on current state and eternal object requirements
            feasibility = self._calculate_feasibility(
                eternal_object, current_state, self.current_environmental_context
            )
            
            if relevance >= self.relevance_threshold and feasibility >= self.feasibility_threshold:
                proposition = Proposition(
                    proposition_id=f"pred_{logical_subject.entity_id}_{eo_id}",
                    proposition_type=PropositionType.PREDICATIVE,
                    logical_subject=logical_subject,
                    eternal_object=eternal_object,
                    propositional_relation="is",
                    lure_intensity=relevance * 0.8,
                    relevance_grade=relevance,
                    feasibility=feasibility,
                    coherence_impact=self._estimate_coherence_impact(eternal_object, current_state),
                    novelty_potential=eternal_object.novelty_grade * 0.5,
                    risk_factor=self._estimate_risk(eternal_object, current_state),
                    temporal_span=(0.0, 1.0),
                    urgency=0.5,
                    persistence=eternal_object.stability,
                    environmental_conditions=eternal_object.ingression_conditions,
                    prerequisite_propositions=[],
                    incompatible_propositions=[],
                    truth_value=PropositionTruthValue.POTENTIAL,
                    confidence=feasibility * relevance,
                    evidence_support=0.5
                )
                
                propositions.append(proposition)
        
        return propositions
    
    def _generate_transformative_propositions(self,
                                           logical_subject: LogicalSubject,
                                           current_state: Dict[str, Any],
                                           subjective_aim_vector: Optional[np.ndarray]) -> List[Proposition]:
        """Generate 'X becomes Y' propositions"""
        propositions = []
        
        for eo_id, eternal_object in self.eternal_objects.items():
            # Check if this represents a meaningful transformation
            current_alignment = self._calculate_current_alignment(
                logical_subject, eternal_object
            )
            
            # Only generate transformation if current alignment is moderate (room for change)
            if 0.2 < current_alignment < 0.8:
                relevance = self._calculate_aim_relevance(eternal_object, subjective_aim_vector)
                
                # Transformative feasibility is generally lower
                base_feasibility = self._calculate_feasibility(
                    eternal_object, current_state, self.current_environmental_context
                )
                transformation_feasibility = base_feasibility * 0.7  # Harder than simple attribution
                
                if relevance >= self.relevance_threshold and transformation_feasibility >= self.feasibility_threshold:
                    proposition = Proposition(
                        proposition_id=f"trans_{logical_subject.entity_id}_{eo_id}",
                        proposition_type=PropositionType.TRANSFORMATIVE,
                        logical_subject=logical_subject,
                        eternal_object=eternal_object,
                        propositional_relation="becomes",
                        lure_intensity=relevance * transformation_feasibility,
                        relevance_grade=relevance,
                        feasibility=transformation_feasibility,
                        coherence_impact=self._estimate_coherence_impact(eternal_object, current_state) * 0.8,
                        novelty_potential=eternal_object.novelty_grade * 0.8,
                        risk_factor=self._estimate_risk(eternal_object, current_state) * 1.2,
                        temporal_span=(0.0, 2.0),
                        urgency=0.6,
                        persistence=eternal_object.stability * 0.9,
                        environmental_conditions=eternal_object.ingression_conditions,
                        prerequisite_propositions=[],
                        incompatible_propositions=[],
                        truth_value=PropositionTruthValue.POTENTIAL,
                        confidence=transformation_feasibility * relevance * 0.8,
                        evidence_support=0.4
                    )
                    
                    propositions.append(proposition)
        
        return propositions
    
    def _generate_emergent_propositions(self,
                                      logical_subject: LogicalSubject,
                                      current_state: Dict[str, Any],
                                      environmental_context: Dict[str, Any]) -> List[Proposition]:
        """Generate emergent 'X + context → Z' propositions"""
        propositions = []
        
        # Check for emergence readiness
        emergence_readiness = current_state.get("emergence_potential", 0.0)
        environmental_complexity = environmental_context.get("complexity", 0.0)
        
        if emergence_readiness > 0.4 and environmental_complexity > 0.3:
            # Create novel eternal objects for emergent possibilities
            emergent_objects = self._generate_emergent_eternal_objects(
                logical_subject, current_state, environmental_context
            )
            
            for emergent_object in emergent_objects:
                # Add to eternal object registry temporarily
                temp_id = f"emergent_{emergent_object.object_id}"
                
                proposition = Proposition(
                    proposition_id=f"emerg_{logical_subject.entity_id}_{temp_id}",
                    proposition_type=PropositionType.EMERGENT,
                    logical_subject=logical_subject,
                    eternal_object=emergent_object,
                    propositional_relation="emerges_as",
                    lure_intensity=0.6 * emergence_readiness,
                    relevance_grade=0.7,  # Emergence is generally relevant
                    feasibility=emergence_readiness * 0.5,  # Emergence is difficult
                    coherence_impact=0.3,  # Emergence can be disruptive initially
                    novelty_potential=0.9,  # Very novel by definition
                    risk_factor=0.6,  # Higher risk due to novelty
                    temporal_span=(1.0, 4.0),  # Takes time to emerge
                    urgency=0.4,
                    persistence=0.6,  # Emergent properties may be fragile initially
                    environmental_conditions={"emergence_potential": 0.5},
                    prerequisite_propositions=[],
                    incompatible_propositions=[],
                    truth_value=PropositionTruthValue.EMERGING,
                    confidence=0.6,
                    evidence_support=emergence_readiness
                )
                
                propositions.append(proposition)
        
        return propositions
    
    def _generate_relational_propositions(self,
                                        logical_subject: LogicalSubject,
                                        nearby_entities: List[Dict[str, Any]]) -> List[Proposition]:
        """Generate propositions about relationships with other entities"""
        propositions = []
        
        # Relational eternal objects
        relational_objects = {
            "connection": self.eternal_objects.get("connection"),
            "cooperation": EternalObject(
                object_id="cooperation",
                pattern_type="relational_pattern",
                pattern_description="Cooperative interaction pattern",
                vector_form=np.array([0.3,0.7,0,0,0,0,0,0,0,0]),
                ingression_conditions={"proximity": 0.3, "compatibility": 0.5},
                stability=0.7,
                novelty_grade=0.4
            )
        }
        
        for entity in nearby_entities[:3]:  # Limit to 3 nearest
            entity_vector = np.array(entity.get("vector", [0]*10))
            compatibility = np.dot(logical_subject.vector_representation, entity_vector)
            
            if compatibility > 0.3:  # Only if reasonably compatible
                for rel_name, rel_object in relational_objects.items():
                    if rel_object:
                        proposition = Proposition(
                            proposition_id=f"rel_{logical_subject.entity_id}_{entity['id']}_{rel_name}",
                            proposition_type=PropositionType.RELATIONAL,
                            logical_subject=logical_subject,
                            eternal_object=rel_object,
                            propositional_relation=f"relates_to_{entity['id']}_via",
                            lure_intensity=compatibility * 0.6,
                            relevance_grade=compatibility,
                            feasibility=0.7,  # Relations generally feasible
                            coherence_impact=0.4,
                            novelty_potential=0.3,
                            risk_factor=0.2,  # Relations generally low risk
                            temporal_span=(0.0, 2.0),
                            urgency=0.3,
                            persistence=0.8,  # Relations can be stable
                            environmental_conditions={"proximity": 0.5},
                            prerequisite_propositions=[],
                            incompatible_propositions=[],
                            truth_value=PropositionTruthValue.POTENTIAL,
                            confidence=0.7,
                            evidence_support=compatibility
                        )
                        
                        propositions.append(proposition)
        
        return propositions
    
    def _calculate_aim_relevance(self, eternal_object: EternalObject, 
                               subjective_aim_vector: Optional[np.ndarray]) -> float:
        """Calculate how relevant an eternal object is to the subjective aim"""
        if subjective_aim_vector is None:
            return 0.5  # Neutral relevance
        
        # Calculate alignment between eternal object and subjective aim
        alignment = np.dot(eternal_object.vector_form, subjective_aim_vector)
        
        # Convert to relevance score (0 to 1)
        relevance = (alignment + 1.0) / 2.0  # Map [-1,1] to [0,1]
        
        return np.clip(relevance, 0.0, 1.0)
    
    def _calculate_feasibility(self, eternal_object: EternalObject,
                             current_state: Dict[str, Any],
                             environmental_context: Dict[str, Any]) -> float:
        """Calculate how feasible it is to actualize an eternal object"""
        feasibility = 1.0
        
        # Check ingression conditions
        for condition, required_value in eternal_object.ingression_conditions.items():
            if condition in current_state:
                current_value = current_state[condition]
                if current_value < required_value:
                    deficit = required_value - current_value
                    feasibility *= (1.0 - deficit * 0.5)  # Reduce feasibility by deficit
            
            elif condition in environmental_context:
                current_value = environmental_context[condition]
                if current_value < required_value:
                    deficit = required_value - current_value
                    feasibility *= (1.0 - deficit * 0.3)  # Environmental deficits less critical
            
            else:
                # Condition not present - significant feasibility reduction
                feasibility *= 0.5
        
        # Factor in eternal object stability (more stable = more feasible)
        feasibility *= eternal_object.stability
        
        return np.clip(feasibility, 0.0, 1.0)
    
    def _estimate_coherence_impact(self, eternal_object: EternalObject,
                                 current_state: Dict[str, Any]) -> float:
        """Estimate impact on coherence from actualizing this eternal object"""
        
        # Base impact from eternal object stability
        base_impact = eternal_object.stability * 0.3 - 0.15  # [-0.15, 0.15]
        
        # Adjust based on current coherence level
        current_coherence = current_state.get("coherence", 0.5)
        
        if current_coherence < 0.4:  # Low coherence
            # Stable eternal objects help more
            if eternal_object.stability > 0.7:
                base_impact += 0.2
        elif current_coherence > 0.8:  # High coherence  
            # Novel eternal objects may disrupt
            if eternal_object.novelty_grade > 0.7:
                base_impact -= 0.1
        
        return np.clip(base_impact, -0.5, 0.5)
    
    def _estimate_risk(self, eternal_object: EternalObject,
                      current_state: Dict[str, Any]) -> float:
        """Estimate risk from actualizing this eternal object"""
        
        # Base risk from novelty (more novel = more risky)
        base_risk = eternal_object.novelty_grade * 0.3
        
        # Increase risk if low current stability
        current_stability = current_state.get("stability", 0.5)
        if current_stability < 0.4:
            base_risk += 0.2
        
        # Reduce risk if eternal object is very stable
        if eternal_object.stability > 0.8:
            base_risk *= 0.7
        
        return np.clip(base_risk, 0.0, 1.0)
    
    def _calculate_current_alignment(self, logical_subject: LogicalSubject,
                                   eternal_object: EternalObject) -> float:
        """Calculate how aligned the subject already is with the eternal object"""
        
        alignment = np.dot(
            logical_subject.vector_representation,
            eternal_object.vector_form
        )
        
        # Convert to [0,1] range
        return (alignment + 1.0) / 2.0
    
    def _generate_emergent_eternal_objects(self,
                                         logical_subject: LogicalSubject,
                                         current_state: Dict[str, Any],
                                         environmental_context: Dict[str, Any]) -> List[EternalObject]:
        """Generate novel eternal objects for emergent propositions"""
        emergent_objects = []
        
        # Combine subject vector with environmental complexity to create new patterns
        subject_vector = logical_subject.vector_representation
        complexity = environmental_context.get("complexity", 0.5)
        
        # Generate a novel vector by combining subject with random variation
        novel_vector = subject_vector + np.random.normal(0, 0.2, 10) * complexity
        novel_vector = novel_vector / (np.linalg.norm(novel_vector) + 1e-10)
        
        emergent_object = EternalObject(
            object_id=f"emergent_{logical_subject.entity_id}_{int(self.current_time)}",
            pattern_type="emergent_pattern",
            pattern_description=f"Novel pattern emerging from {logical_subject.entity_type}",
            vector_form=novel_vector,
            ingression_conditions={"emergence_potential": 0.6},
            stability=0.4,  # Emergent patterns start less stable
            novelty_grade=0.9  # Very novel by definition
        )
        
        emergent_objects.append(emergent_object)
        
        return emergent_objects
    
    def _filter_propositions(self, propositions: List[Proposition],
                           current_state: Dict[str, Any],
                           salience_weights: Optional[Dict[str, float]]) -> List[Proposition]:
        """Filter propositions based on relevance, feasibility, and salience"""
        
        filtered = []
        
        for proposition in propositions:
            # Basic thresholds
            if (proposition.relevance_grade < self.relevance_threshold or
                proposition.feasibility < self.feasibility_threshold):
                continue
            
            # Apply salience weighting if available
            if salience_weights:
                # Adjust proposition appeal based on salience
                salience_factor = 1.0
                
                if "novelty" in salience_weights and proposition.novelty_potential > 0.5:
                    salience_factor *= (1.0 + salience_weights["novelty"] * 0.5)
                
                if "coherence" in salience_weights and proposition.coherence_impact > 0:
                    salience_factor *= (1.0 + salience_weights["coherence"] * 0.3)
                
                # Update proposition lure intensity
                proposition.lure_intensity *= salience_factor
                proposition.relevance_grade *= salience_factor
            
            # Check for compatibility with current active propositions
            compatible = True
            for active_id in self.active_proposition_ids:
                # This would require storing active propositions - simplified for now
                pass
            
            if compatible:
                filtered.append(proposition)
        
        return filtered
    
    def add_eternal_object(self, eternal_object: EternalObject):
        """Add a new eternal object to the registry"""
        self.eternal_objects[eternal_object.object_id] = eternal_object
    
    def record_proposition_outcome(self, proposition_id: str, success_score: float):
        """Record the outcome of a proposition for learning"""
        if proposition_id not in self.proposition_success_history:
            self.proposition_success_history[proposition_id] = []
        
        self.proposition_success_history[proposition_id].append(success_score)
        
        # Update pattern effectiveness
        # Extract pattern from proposition_id (simplified)
        pattern_key = proposition_id.split('_')[0]  # e.g., "pred", "trans", "emerg"
        
        if pattern_key not in self.pattern_effectiveness:
            self.pattern_effectiveness[pattern_key] = 0.5
        
        # Update with exponential moving average
        self.pattern_effectiveness[pattern_key] = (
            0.9 * self.pattern_effectiveness[pattern_key] + 0.1 * success_score
        )
    
    def get_proposition_statistics(self) -> Dict[str, Any]:
        """Get statistics about proposition generation"""
        return {
            "eternal_objects_count": len(self.eternal_objects),
            "pattern_effectiveness": self.pattern_effectiveness,
            "active_propositions": len(self.active_proposition_ids),
            "success_history_entries": len(self.proposition_success_history)
        }