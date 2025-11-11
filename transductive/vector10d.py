"""
Vector10D - 10-dimensional universal symbolic space
All organs process the same reality through different Umwelts
"""

import numpy as np
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Vector10D:
    """
    10-dimensional symbolic vector representing universal space.
    Each dimension carries specific meaning that organs interpret differently.
    """
    
    # Dimension names for clarity
    DIMENSION_NAMES = [
        "spatial_form",       # 0: Geometric characteristics
        "spatial_relation",   # 1: Topological properties
        "temporal_sequence",  # 2: Sequential patterns
        "change_dynamics",    # 3: Transformation rates
        "transformation_type", # 4: Rotation/reflection/scale
        "pattern_complexity", # 5: Simple/complex/irregular
        "symbolic_role",      # 6: Agent/background/target
        "semantic_intensity", # 7: Importance/salience
        "abstraction_level",  # 8: Concrete/abstract spectrum
        "coherence_pressure"  # 9: Drive toward harmony
    ]
    
    dimensions: np.ndarray = field(default_factory=lambda: np.zeros(10))
    properties: Dict[str, Any] = field(default_factory=dict)  # Additional metadata
    
    def __post_init__(self):
        """Ensure dimensions is numpy array of correct size"""
        if not isinstance(self.dimensions, np.ndarray):
            self.dimensions = np.array(self.dimensions)
        if self.dimensions.shape != (10,):
            self.dimensions = np.zeros(10)
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "Vector10D":
        """Create vector from dictionary of dimension names to values"""
        vector = cls()
        for name, value in data.items():
            if name in cls.DIMENSION_NAMES:
                idx = cls.DIMENSION_NAMES.index(name)
                vector.dimensions[idx] = value
        return vector
    
    @classmethod
    def random(cls, seed: Optional[int] = None) -> "Vector10D":
        """Create random vector for testing"""
        if seed is not None:
            np.random.seed(seed)
        return cls(dimensions=np.random.random(10))
    
    @classmethod
    def zero(cls) -> "Vector10D":
        """Create zero vector"""
        return cls(dimensions=np.zeros(10))
    
    @classmethod
    def one(cls) -> "Vector10D":
        """Create vector of all ones"""
        return cls(dimensions=np.ones(10))
    
    @classmethod
    def sum(cls, vectors: List["Vector10D"]) -> "Vector10D":
        """Sum a list of vectors"""
        if not vectors:
            return cls.zero()
        
        result = np.zeros(10)
        for vector in vectors:
            result += vector.dimensions
        
        return cls(dimensions=result)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary with named dimensions"""
        return {
            name: float(self.dimensions[i]) 
            for i, name in enumerate(self.DIMENSION_NAMES)
        }
    
    def normalize(self) -> "Vector10D":
        """Normalize vector to unit length"""
        norm = np.linalg.norm(self.dimensions)
        if norm > 0:
            self.dimensions = self.dimensions / norm
        return self
    
    def dot(self, other: "Vector10D") -> float:
        """Dot product with another vector"""
        return float(np.dot(self.dimensions, other.dimensions))
    
    def dot_product(self, other: "Vector10D") -> float:
        """Alias for dot method"""
        return self.dot(other)
    
    def magnitude(self) -> float:
        """Calculate magnitude/norm of the vector"""
        return float(np.linalg.norm(self.dimensions))
    
    def cosine_similarity(self, other: "Vector10D") -> float:
        """Calculate cosine similarity with another vector"""
        norm_self = np.linalg.norm(self.dimensions)
        norm_other = np.linalg.norm(other.dimensions)
        
        if norm_self == 0 or norm_other == 0:
            return 0.0
        
        return self.dot(other) / (norm_self * norm_other)
    
    def apply_umwelt(self, weights: np.ndarray) -> "Vector10D":
        """
        Apply organ-specific Umwelt weighting.
        This is how different organs see the same reality differently.
        """
        if weights.shape != (10,):
            raise ValueError("Umwelt weights must be 10-dimensional")
        
        weighted = self.dimensions * weights
        return Vector10D(dimensions=weighted)
    
    def distance(self, other: "Vector10D") -> float:
        """Euclidean distance to another vector"""
        return float(np.linalg.norm(self.dimensions - other.dimensions))
    
    def interpolate(self, other: "Vector10D", t: float) -> "Vector10D":
        """Linear interpolation between vectors"""
        t = max(0, min(1, t))  # Clamp to [0, 1]
        interpolated = self.dimensions * (1 - t) + other.dimensions * t
        return Vector10D(dimensions=interpolated)
    
    def add(self, other: "Vector10D") -> "Vector10D":
        """Vector addition"""
        return Vector10D(dimensions=self.dimensions + other.dimensions)
    
    def subtract(self, other: "Vector10D") -> "Vector10D":
        """Vector subtraction"""
        return Vector10D(dimensions=self.dimensions - other.dimensions)
    
    def scale(self, scalar: float) -> "Vector10D":
        """Scalar multiplication"""
        return Vector10D(dimensions=self.dimensions * scalar)
    
    def get_dimension(self, name: str) -> float:
        """Get value of named dimension"""
        if name in self.DIMENSION_NAMES:
            idx = self.DIMENSION_NAMES.index(name)
            return float(self.dimensions[idx])
        raise ValueError(f"Unknown dimension: {name}")
    
    def set_dimension(self, name: str, value: float) -> None:
        """Set value of named dimension"""
        if name in self.DIMENSION_NAMES:
            idx = self.DIMENSION_NAMES.index(name)
            self.dimensions[idx] = value
        else:
            raise ValueError(f"Unknown dimension: {name}")
    
    def coherence_score(self) -> float:
        """Calculate internal coherence of the vector"""
        # Coherence pressure dimension weighted by overall magnitude
        coherence_dim = self.dimensions[9]
        magnitude = np.linalg.norm(self.dimensions)
        
        if magnitude == 0:
            return 0.0
        
        # Coherence is combination of coherence dimension and overall balance
        balance = 1.0 - np.std(self.dimensions) / (np.mean(np.abs(self.dimensions)) + 1e-10)
        return (coherence_dim * 0.7 + balance * 0.3)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"Vector10D(coherence={self.coherence_score():.2f})"
    
    def __str__(self) -> str:
        """Detailed string representation"""
        lines = ["Vector10D:"]
        for i, name in enumerate(self.DIMENSION_NAMES):
            lines.append(f"  {name:20s}: {self.dimensions[i]:6.3f}")
        lines.append(f"  Coherence Score: {self.coherence_score():.3f}")
        return "\n".join(lines)
    
    # === FELT AFFORDANCE PROPERTIES ===
    # Direct property access for smooth SVT engine integration
    # These provide the "felt affordances" that organs can directly perceive
    
    @property
    def spatial_form(self) -> float:
        """Felt affordance: geometric characteristics of this entity"""
        return float(self.dimensions[0])
    
    @spatial_form.setter
    def spatial_form(self, value: float) -> None:
        self.dimensions[0] = float(value)
    
    @property
    def spatial_relation(self) -> float:
        """Felt affordance: topological relationship to other entities"""
        return float(self.dimensions[1])
    
    @spatial_relation.setter
    def spatial_relation(self, value: float) -> None:
        self.dimensions[1] = float(value)
    
    @property
    def temporal_sequence(self) -> float:
        """Felt affordance: sequential pattern awareness"""
        return float(self.dimensions[2])
    
    @temporal_sequence.setter
    def temporal_sequence(self, value: float) -> None:
        self.dimensions[2] = float(value)
    
    @property
    def change_dynamics(self) -> float:
        """Felt affordance: transformation rate and style"""
        return float(self.dimensions[3])
    
    @change_dynamics.setter
    def change_dynamics(self, value: float) -> None:
        self.dimensions[3] = float(value)
    
    @property
    def transformation_type(self) -> float:
        """Felt affordance: rotation/reflection/scale potential"""
        return float(self.dimensions[4])
    
    @transformation_type.setter
    def transformation_type(self, value: float) -> None:
        self.dimensions[4] = float(value)
    
    @property
    def pattern_complexity(self) -> float:
        """Felt affordance: structural complexity level"""
        return float(self.dimensions[5])
    
    @pattern_complexity.setter
    def pattern_complexity(self, value: float) -> None:
        self.dimensions[5] = float(value)
    
    @property
    def symbolic_role(self) -> float:
        """Felt affordance: purpose/meaning in the system"""
        return float(self.dimensions[6])
    
    @symbolic_role.setter
    def symbolic_role(self, value: float) -> None:
        self.dimensions[6] = float(value)
    
    @property
    def semantic_intensity(self) -> float:
        """Felt affordance: meaning density and importance"""
        return float(self.dimensions[7])
    
    @semantic_intensity.setter
    def semantic_intensity(self, value: float) -> None:
        self.dimensions[7] = float(value)
    
    @property
    def abstraction_level(self) -> float:
        """Felt affordance: concrete to abstract spectrum"""
        return float(self.dimensions[8])
    
    @abstraction_level.setter
    def abstraction_level(self, value: float) -> None:
        self.dimensions[8] = float(value)
    
    @property
    def coherence_pressure(self) -> float:
        """Felt affordance: drive toward internal harmony"""
        return float(self.dimensions[9])
    
    @coherence_pressure.setter
    def coherence_pressure(self, value: float) -> None:
        self.dimensions[9] = float(value)
    
    # === MISSING DIMENSION COMPATIBILITY ===
    # For Spora Explora compatibility (11D) - maps to closest 10D equivalent
    
    @property
    def interaction_potential(self) -> float:
        """Felt affordance: social/interactive capacity (maps to coherence_pressure)"""
        return self.coherence_pressure  # Map to coherence pressure as closest analog
    
    @interaction_potential.setter
    def interaction_potential(self, value: float) -> None:
        self.coherence_pressure = float(value)  # Store in coherence pressure dimension