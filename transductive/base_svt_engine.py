"""
Base SVT Transductive Engine - Core T(x) Formula Implementation

Implements the universal SVT formula that all organs specialize:
T(x) = ƒ(Pₙ, Rₙ, V⃗f, ΔCₙ) → Nₙ₊₁

Each organ inherits this and modifies parameters for specialized processing.
Based on organ_svt_engines.md architecture specification.
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from .actual_occasion import ActualOccasion
from .vector10d import Vector10D


@dataclass
class TransductiveNexus:
    """Result of SVT transduction process"""
    coherence: float
    pressure: float  # How strongly the organ feels about this result
    vector_field: Dict[str, Vector10D]
    constraint_delta: float
    organ_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    svt_components: Optional['SVTComponents'] = None  # Original components for reference


@dataclass
class SVTComponents:
    """Core components of SVT formula T(x) = ƒ(Pₙ, Rₙ, V⃗f, ΔCₙ)"""
    Pn: Dict[str, Any]  # Past/Prehension component
    Rn: Dict[str, float]  # Relevance component
    Vf: Dict[str, Vector10D]  # Vector field component
    delta_Cn: float  # Constraint delta component
    symbolic_field: Optional[Dict[str, Any]] = None  # V0: Symbolic field with input_grid_shape for field extraction


class BaseTransductiveEngine(ABC):
    """
    Base class for organ-specific SVT transductive engines.
    
    Each organ implements the same core formula but with different:
    - Relevance calculations (Rₙ)
    - Constraint handling (ΔCₙ)
    - Vector field processing (V⃗f)
    - Prehension strategies (Pₙ)
    """
    
    def __init__(self, organ_name: str):
        self.organ_name = organ_name
        self.coherence_threshold = 0.75
        self.max_transduction_depth = 5
        self.pressure_sensitivity = 1.0
        
        # Organ-specific configuration (overridden by subclasses)
        self.relevance_bias = "neutral"  # "positive", "negative", "spatial", "temporal"
        self.delta_preference = "moderate"  # "minimal", "moderate", "maximal"
        self.vector_focus = "balanced"  # Which dimensions the organ emphasizes
        
    @abstractmethod
    def transduce(self, svt_components: SVTComponents) -> TransductiveNexus:
        """
        Core SVT transduction: T(x) = ƒ(Pₙ, Rₙ, V⃗f, ΔCₙ) → Nₙ₊₁
        Each organ implements its specialized version
        """
        pass
    
    @abstractmethod
    def calculate_symbolic_pressure(self, symbolic_field: Dict[str, Any]) -> float:
        """
        Calculate how strongly this organ 'feels' about the symbolic field.
        Higher pressure = organ is more activated by this field.
        """
        pass
    
    @abstractmethod
    def extract_relevance(self, symbolic_field: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract organ-specific relevance (Rₙ) from symbolic field.
        Each organ sees different aspects as relevant.
        """
        pass
    
    def extract_svt_components(self, symbolic_field: Dict[str, Any], 
                             context: Dict[str, Any]) -> SVTComponents:
        """
        Extract the four core SVT components from symbolic field and context.
        This is shared logic, but each organ can override for specialization.
        """
        
        # Extract entities from symbolic field
        entities = symbolic_field.get("entities", [])
        
        # Pₙ: Past/Prehension component (what the organ remembers/feels)
        Pn = self._extract_prehension_component(entities, context)
        
        # Rₙ: Relevance component (organ-specific relevance calculation)
        Rn = self.extract_relevance(symbolic_field)
        
        # V⃗f: Vector field component (spatial arrangement of vectors)
        Vf = self._extract_vector_field(entities)
        
        # ΔCₙ: Constraint delta component (readiness for transformation)
        delta_Cn = self._calculate_constraint_delta(symbolic_field, context)
        
        return SVTComponents(Pn=Pn, Rn=Rn, Vf=Vf, delta_Cn=delta_Cn)
    
    def _extract_prehension_component(self, entities: List[ActualOccasion], 
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract past/prehension data for SVT processing"""
        
        prehension_data = {
            "entity_count": len(entities),
            "positions": [],
            "symbols": [],
            "coherence_history": context.get("coherence_history", []),
            "organ_memory": getattr(self, f"{self.organ_name}_memory", {})
        }
        
        for entity in entities:
            if hasattr(entity, 'position'):
                prehension_data["positions"].append(entity.position)
            if hasattr(entity, 'symbol'):
                prehension_data["symbols"].append(entity.symbol)
        
        return prehension_data
    
    def _extract_vector_field(self, entities: List[ActualOccasion]) -> Dict[str, Vector10D]:
        """Extract vector field from entities for V⃗f component"""
        
        vector_field = {}
        
        for i, entity in enumerate(entities):
            # Get entity's vector or create one from its properties
            if hasattr(entity, 'current_vector') and entity.current_vector:
                vector = entity.current_vector
            else:
                # Create vector from entity properties
                vector = Vector10D()
                if hasattr(entity, 'symbol'):
                    # Basic symbol-to-vector mapping
                    symbol_intensity = min(1.0, len(entity.symbol) / 10.0) if entity.symbol else 0.0
                    vector.semantic_intensity = symbol_intensity
                    vector.symbolic_role = 0.8 if entity.symbol else 0.0
                
                if hasattr(entity, 'position'):
                    pos = entity.position
                    if isinstance(pos, (tuple, list)) and len(pos) >= 2:
                        # Normalize position to [0,1] range
                        vector.spatial_form = min(1.0, pos[0] / 10.0)
                        vector.spatial_relation = min(1.0, pos[1] / 10.0)
            
            # Use position as key, or index if no position
            if hasattr(entity, 'position'):
                key = f"{entity.position[0]}_{entity.position[1]}"
            else:
                key = f"entity_{i}"
            
            vector_field[key] = vector
        
        return vector_field
    
    def _calculate_constraint_delta(self, symbolic_field: Dict[str, Any], 
                                  context: Dict[str, Any]) -> float:
        """Calculate constraint transformation readiness (ΔCₙ)"""
        
        # Base delta calculation (organs can override for specialized behavior)
        base_delta = 0.5  # Neutral readiness
        
        # Factors that influence transformation readiness
        field_complexity = len(symbolic_field.get("entities", [])) / 30.0  # Normalize
        field_complexity = min(1.0, field_complexity)
        
        # Past success influences readiness
        success_rate = context.get("success_rate", 0.5)
        
        # Calculate delta based on organ preference
        if self.delta_preference == "minimal":
            # Organs that prefer stability (like SANS)
            delta = base_delta * 0.5 + success_rate * 0.3
        elif self.delta_preference == "maximal":
            # Organs that embrace change (like NDAM)
            delta = base_delta * 1.5 + field_complexity * 0.5
        else:  # moderate
            delta = base_delta + (field_complexity + success_rate) * 0.25
        
        return min(2.0, max(0.0, delta))
    
    def apply_core_svt_formula(self, svt_components: SVTComponents) -> TransductiveNexus:
        """
        Apply the core SVT formula: T(x) = ƒ(Pₙ, Rₙ, V⃗f, ΔCₙ) → Nₙ₊₁
        This is the shared mathematical foundation that organs specialize.
        """
        
        Pn, Rn, Vf, delta_Cn = svt_components.Pn, svt_components.Rn, svt_components.Vf, svt_components.delta_Cn
        
        # Step 1: Calculate coherence based on relevance and past experience
        relevance_sum = sum(Rn.values()) if Rn else 0.0
        avg_relevance = relevance_sum / max(1, len(Rn)) if Rn else 0.0
        
        prehension_coherence = len(Pn.get("coherence_history", [])) / 10.0  # Normalize
        prehension_coherence = min(1.0, prehension_coherence)
        
        # Enhanced coherence calculation with meaningful baseline
        # If no relevance detected, use entity presence and vector field strength as baseline
        if avg_relevance == 0.0 and len(Vf) > 0:
            # Calculate vector field strength as baseline coherence
            vector_strengths = []
            for vector in Vf.values():
                strength = (vector.semantic_intensity + vector.spatial_form + 
                           vector.pattern_complexity + vector.symbolic_role) / 4.0
                vector_strengths.append(strength)
            avg_relevance = np.mean(vector_strengths) if vector_strengths else 0.3
        
        # Ensure minimum coherence when entities are present
        entity_presence_bonus = min(0.4, len(Pn.get("positions", [])) * 0.1)
        
        base_coherence = (avg_relevance * 0.6) + (prehension_coherence * 0.2) + (entity_presence_bonus * 0.2)
        
        # Step 2: Apply constraint delta transformation
        transformed_coherence = base_coherence * (1.0 + delta_Cn * 0.3)
        final_coherence = min(1.0, max(0.1, transformed_coherence))  # Minimum 0.1 when processing
        
        # Step 3: Calculate symbolic pressure
        pressure = self.calculate_symbolic_pressure({
            "entities": Pn,
            "relevance": Rn,
            "vectors": Vf
        })
        
        # Step 4: Process vector field (organs can override this)
        processed_vectors = self._process_vector_field(Vf, Rn, delta_Cn)
        
        return TransductiveNexus(
            coherence=final_coherence,
            pressure=pressure,
            vector_field=processed_vectors,
            constraint_delta=delta_Cn,
            organ_type=self.organ_name,
            metadata={
                "relevance_avg": avg_relevance,
                "prehension_depth": len(Pn.get("positions", [])),
                "vector_count": len(Vf)
            },
            svt_components=svt_components
        )
    
    def _process_vector_field(self, vector_field: Dict[str, Vector10D], 
                            relevance: Dict[str, float], 
                            delta_Cn: float) -> Dict[str, Vector10D]:
        """
        Process vector field based on relevance and constraint delta.
        Base implementation - organs override for specialized processing.
        """
        
        processed_vectors = {}
        
        for key, vector in vector_field.items():
            # Apply relevance weighting if available
            relevance_weight = relevance.get(key, 1.0)
            
            # Create processed vector
            processed = Vector10D()
            processed.spatial_form = vector.spatial_form * relevance_weight
            processed.spatial_relation = vector.spatial_relation * relevance_weight
            processed.pattern_complexity = vector.pattern_complexity * relevance_weight
            processed.semantic_intensity = vector.semantic_intensity * relevance_weight
            processed.symbolic_role = vector.symbolic_role * relevance_weight
            processed.abstraction_level = vector.abstraction_level * relevance_weight
            processed.transformation_type = vector.transformation_type * delta_Cn
            processed.interaction_potential = vector.interaction_potential * relevance_weight
            processed.temporal_sequence = vector.temporal_sequence
            processed.change_dynamics = vector.change_dynamics * delta_Cn
            
            processed_vectors[key] = processed
        
        return processed_vectors
    
    def get_organ_statistics(self) -> Dict[str, Any]:
        """Return organ-specific performance statistics"""
        return {
            "organ_name": self.organ_name,
            "coherence_threshold": self.coherence_threshold,
            "relevance_bias": self.relevance_bias,
            "delta_preference": self.delta_preference,
            "vector_focus": self.vector_focus,
            "pressure_sensitivity": self.pressure_sensitivity
        }