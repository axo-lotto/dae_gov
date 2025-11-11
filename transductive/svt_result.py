"""
SVTResult - Complete SVT cycle results with multi-organ transformation tracking

Implements comprehensive tracking for Symbolic Vector Transduction events:
- Individual transformation events with complete metadata
- Multi-organ coordination results  
- Confidence tracking and genealogical learning
- Backward compatibility with existing PrehensionResult

Based on REFINED_CLASS_STRUCTURE.md and process philosophy principles.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import numpy as np
from datetime import datetime
from .vector10d import Vector10D
from .umwelt_transform import UmweltTransform


@dataclass
class SVTTransformationEvent:
    """Single SVT application with complete metadata"""
    
    # Core transformation data
    organ_type: str
    input_vector: Vector10D
    transformed_vector: Vector10D
    confidence: float
    
    # Transformation details
    umwelt_applied: UmweltTransform
    processing_time: float = 0.0
    
    # Process philosophy metadata
    emergence_markers: List[str] = field(default_factory=list)
    prehension_depth: float = 0.0
    satisfaction_achieved: float = 0.0
    
    # Technical metadata
    timestamp: datetime = field(default_factory=datetime.now)
    transformation_id: str = ""
    parent_cycle_id: Optional[str] = None
    
    def __post_init__(self):
        """Generate unique transformation ID if not provided"""
        if not self.transformation_id:
            timestamp_str = self.timestamp.strftime("%Y%m%d_%H%M%S_%f")
            self.transformation_id = f"{self.organ_type}_{timestamp_str}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "transformation_id": self.transformation_id,
            "organ_type": self.organ_type,
            "input_vector": self.input_vector.to_dict(),
            "transformed_vector": self.transformed_vector.to_dict(),
            "confidence": self.confidence,
            "processing_time": self.processing_time,
            "emergence_markers": self.emergence_markers,
            "prehension_depth": self.prehension_depth,
            "satisfaction_achieved": self.satisfaction_achieved,
            "timestamp": self.timestamp.isoformat(),
            "parent_cycle_id": self.parent_cycle_id
        }
    
    def calculate_transformation_magnitude(self) -> float:
        """Calculate magnitude of transformation applied"""
        input_norm = np.linalg.norm(self.input_vector.dimensions)
        output_norm = np.linalg.norm(self.transformed_vector.dimensions)
        
        if input_norm == 0:
            return output_norm
        
        return abs(output_norm - input_norm) / input_norm
    
    def assess_emergence_quality(self) -> Dict[str, float]:
        """Assess quality of emergence through this transformation"""
        magnitude = self.calculate_transformation_magnitude()
        
        return {
            "novelty": magnitude * self.confidence,
            "coherence": self.satisfaction_achieved,
            "depth": self.prehension_depth,
            "overall_emergence": (magnitude + self.confidence + self.satisfaction_achieved) / 3
        }


@dataclass  
class SVTResult:
    """Result of complete SVT cycle with multi-organ transformations"""
    
    # Backward compatibility with PrehensionResult
    entities_felt: List[Dict[str, Any]] = field(default_factory=list)
    field_coherence: float = 0.0
    umwelt_signature: str = ""
    salience_gradient: Dict[str, float] = field(default_factory=dict)
    environmental_pressure: float = 0.0
    novelty_detected: bool = False
    felt_contrasts: List[str] = field(default_factory=list)
    
    # SVT-specific data
    svt_transformations: List[SVTTransformationEvent] = field(default_factory=list)
    integrated_field: Vector10D = field(default_factory=Vector10D)
    coherence_matrix: np.ndarray = field(default_factory=lambda: np.eye(1))
    multi_organ_agreement: float = 0.0
    transformation_genealogy: Dict[str, Any] = field(default_factory=dict)
    
    # Cycle identification and timing
    cycle_id: str = ""
    total_processing_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Performance metrics
    organs_activated: List[str] = field(default_factory=list)
    average_confidence: float = 0.0
    peak_confidence: float = 0.0
    confidence_variance: float = 0.0
    
    def __post_init__(self):
        """Generate cycle ID and calculate derived metrics"""
        if not self.cycle_id:
            timestamp_str = self.timestamp.strftime("%Y%m%d_%H%M%S_%f")
            self.cycle_id = f"svt_cycle_{timestamp_str}"
        
        self._calculate_performance_metrics()
    
    def _calculate_performance_metrics(self) -> None:
        """Calculate derived performance metrics from transformations"""
        if not self.svt_transformations:
            return
        
        # Extract confidence values
        confidences = [t.confidence for t in self.svt_transformations]
        
        self.average_confidence = np.mean(confidences)
        self.peak_confidence = np.max(confidences)
        self.confidence_variance = np.var(confidences)
        
        # Extract activated organs
        self.organs_activated = list(set(t.organ_type for t in self.svt_transformations))
        
        # Calculate total processing time
        self.total_processing_time = sum(t.processing_time for t in self.svt_transformations)
    
    def add_transformation(self, transformation: SVTTransformationEvent) -> None:
        """Add a transformation event and update metrics"""
        transformation.parent_cycle_id = self.cycle_id
        self.svt_transformations.append(transformation)
        self._calculate_performance_metrics()
    
    def calculate_multi_organ_agreement(self) -> float:
        """Calculate agreement between multiple organ transformations"""
        if len(self.svt_transformations) < 2:
            return 1.0  # Perfect agreement with single/no organs
        
        # Group transformations by input vector (same input, different organs)
        input_groups = {}
        for transform in self.svt_transformations:
            input_key = tuple(transform.input_vector.dimensions)
            if input_key not in input_groups:
                input_groups[input_key] = []
            input_groups[input_key].append(transform)
        
        # Calculate agreement within each input group
        agreements = []
        for group in input_groups.values():
            if len(group) < 2:
                continue
            
            # Calculate pairwise correlations between transformed outputs
            group_agreements = []
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    vec1 = group[i].transformed_vector.dimensions
                    vec2 = group[j].transformed_vector.dimensions
                    
                    # Correlation coefficient as agreement measure
                    correlation = np.corrcoef(vec1, vec2)[0, 1]
                    if not np.isnan(correlation):
                        group_agreements.append(abs(correlation))
            
            if group_agreements:
                agreements.append(np.mean(group_agreements))
        
        self.multi_organ_agreement = np.mean(agreements) if agreements else 1.0
        return self.multi_organ_agreement
    
    def generate_transformation_genealogy(self) -> Dict[str, Any]:
        """Generate genealogical record of transformations"""
        genealogy = {
            "cycle_id": self.cycle_id,
            "timestamp": self.timestamp.isoformat(),
            "organs_involved": self.organs_activated,
            "transformation_sequence": [],
            "emergence_patterns": {},
            "learning_insights": {}
        }
        
        # Document transformation sequence
        for i, transform in enumerate(self.svt_transformations):
            sequence_entry = {
                "step": i,
                "organ": transform.organ_type,
                "confidence": transform.confidence,
                "emergence_quality": transform.assess_emergence_quality(),
                "transformation_magnitude": transform.calculate_transformation_magnitude()
            }
            genealogy["transformation_sequence"].append(sequence_entry)
        
        # Identify emergence patterns
        if len(self.svt_transformations) > 1:
            # Confidence progression pattern
            confidences = [t.confidence for t in self.svt_transformations]
            genealogy["emergence_patterns"]["confidence_trend"] = self._analyze_trend(confidences)
            
            # Organ activation pattern
            organ_sequence = [t.organ_type for t in self.svt_transformations]
            genealogy["emergence_patterns"]["organ_activation_pattern"] = organ_sequence
            
            # Multi-organ coordination effectiveness
            genealogy["emergence_patterns"]["coordination_effectiveness"] = self.multi_organ_agreement
        
        # Learning insights for future cycles
        genealogy["learning_insights"] = {
            "most_effective_organ": max(self.svt_transformations, key=lambda t: t.confidence).organ_type if self.svt_transformations else None,
            "average_satisfaction": np.mean([t.satisfaction_achieved for t in self.svt_transformations]) if self.svt_transformations else 0,
            "recommended_organ_sequence": self._generate_organ_recommendations()
        }
        
        self.transformation_genealogy = genealogy
        return genealogy
    
    def _analyze_trend(self, values: List[float]) -> str:
        """Analyze trend in a sequence of values"""
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple trend analysis
        diff = values[-1] - values[0]
        if abs(diff) < 0.1:
            return "stable"
        elif diff > 0:
            return "increasing"
        else:
            return "decreasing"
    
    def _generate_organ_recommendations(self) -> List[str]:
        """Generate recommendations for future organ activation sequences"""
        if not self.svt_transformations:
            return []
        
        # Sort organs by average confidence when they appeared
        organ_performance = {}
        for transform in self.svt_transformations:
            organ = transform.organ_type
            if organ not in organ_performance:
                organ_performance[organ] = []
            organ_performance[organ].append(transform.confidence)
        
        # Calculate average performance per organ
        organ_averages = {
            organ: np.mean(confidences) 
            for organ, confidences in organ_performance.items()
        }
        
        # Return organs sorted by performance
        return sorted(organ_averages.keys(), key=lambda o: organ_averages[o], reverse=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "cycle_id": self.cycle_id,
            "timestamp": self.timestamp.isoformat(),
            
            # Backward compatibility fields
            "entities_felt": self.entities_felt,
            "field_coherence": self.field_coherence,
            "umwelt_signature": self.umwelt_signature,
            "salience_gradient": self.salience_gradient,
            "environmental_pressure": self.environmental_pressure,
            "novelty_detected": self.novelty_detected,
            "felt_contrasts": self.felt_contrasts,
            
            # SVT-specific fields
            "svt_transformations": [t.to_dict() for t in self.svt_transformations],
            "integrated_field": self.integrated_field.to_dict(),
            "multi_organ_agreement": self.multi_organ_agreement,
            "transformation_genealogy": self.transformation_genealogy,
            
            # Performance metrics
            "organs_activated": self.organs_activated,
            "average_confidence": self.average_confidence,
            "peak_confidence": self.peak_confidence,
            "confidence_variance": self.confidence_variance,
            "total_processing_time": self.total_processing_time
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get concise performance summary"""
        return {
            "cycle_id": self.cycle_id,
            "organs_count": len(self.organs_activated),
            "transformations_count": len(self.svt_transformations),
            "average_confidence": self.average_confidence,
            "multi_organ_agreement": self.multi_organ_agreement,
            "field_coherence": self.field_coherence,
            "total_processing_time": self.total_processing_time,
            "emergence_detected": self.novelty_detected
        }


class SVTResultAnalyzer:
    """Analyzer for SVT results and performance optimization"""
    
    def __init__(self):
        self.historical_results: List[SVTResult] = []
    
    def add_result(self, result: SVTResult) -> None:
        """Add result to historical analysis"""
        self.historical_results.append(result)
    
    def analyze_organ_performance(self) -> Dict[str, Dict[str, float]]:
        """Analyze performance patterns across organs"""
        organ_stats = {}
        
        for result in self.historical_results:
            for transform in result.svt_transformations:
                organ = transform.organ_type
                if organ not in organ_stats:
                    organ_stats[organ] = {
                        "total_activations": 0,
                        "total_confidence": 0.0,
                        "total_processing_time": 0.0,
                        "emergence_events": 0
                    }
                
                stats = organ_stats[organ]
                stats["total_activations"] += 1
                stats["total_confidence"] += transform.confidence
                stats["total_processing_time"] += transform.processing_time
                
                if transform.emergence_markers:
                    stats["emergence_events"] += 1
        
        # Calculate averages
        for organ, stats in organ_stats.items():
            if stats["total_activations"] > 0:
                stats["average_confidence"] = stats["total_confidence"] / stats["total_activations"]
                stats["average_processing_time"] = stats["total_processing_time"] / stats["total_activations"]
                stats["emergence_rate"] = stats["emergence_events"] / stats["total_activations"]
        
        return organ_stats
    
    def recommend_optimization(self) -> Dict[str, Any]:
        """Generate optimization recommendations based on historical data"""
        if not self.historical_results:
            return {"status": "insufficient_data"}
        
        organ_performance = self.analyze_organ_performance()
        
        # Find best performing organs
        best_organs = sorted(
            organ_performance.keys(),
            key=lambda o: organ_performance[o].get("average_confidence", 0),
            reverse=True
        )
        
        # Find performance bottlenecks
        slow_organs = sorted(
            organ_performance.keys(),
            key=lambda o: organ_performance[o].get("average_processing_time", 0),
            reverse=True
        )
        
        return {
            "best_performing_organs": best_organs[:3],
            "performance_bottlenecks": slow_organs[:2],
            "overall_stats": {
                "total_cycles": len(self.historical_results),
                "average_multi_organ_agreement": np.mean([r.multi_organ_agreement for r in self.historical_results]),
                "average_field_coherence": np.mean([r.field_coherence for r in self.historical_results])
            },
            "recommendations": self._generate_specific_recommendations(organ_performance)
        }
    
    def _generate_specific_recommendations(self, organ_performance: Dict) -> List[str]:
        """Generate specific optimization recommendations"""
        recommendations = []
        
        # Performance-based recommendations
        for organ, stats in organ_performance.items():
            avg_conf = stats.get("average_confidence", 0)
            avg_time = stats.get("average_processing_time", 0)
            
            if avg_conf < 0.3:
                recommendations.append(f"Consider retuning {organ} organ weights - low confidence pattern detected")
            
            if avg_time > 10.0:  # ms
                recommendations.append(f"Optimize {organ} organ processing - performance bottleneck detected")
            
            if stats.get("emergence_rate", 0) > 0.8:
                recommendations.append(f"{organ} organ shows high emergence potential - consider primary activation")
        
        return recommendations