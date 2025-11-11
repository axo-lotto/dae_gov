"""
Subjective Aim - The directional lure of an actual occasion

In process philosophy, the subjective aim is the directional lure that guides 
the concrescence of an actual occasion toward satisfaction. It provides the
"final cause" or teleological direction for the occasion's becoming.

Based on Whitehead's Process and Reality and the tECS architecture.
Part of the transductive formula: T(x) = ƒ(Pₙ, Rₙ, V⃗f, ΔCₙ) → Nₙ₊₁
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
import numpy as np
from .vector10d import Vector10D
from .salience_model import SalienceModel

@dataclass
class AimVector:
    """
    Represents a directional lure with magnitude and quality
    """
    direction: np.ndarray       # Direction in 10D symbolic space
    intensity: float           # Strength of the lure (0.0 to 1.0)
    quality: str              # Type of satisfaction sought
    temporal_horizon: float   # How far into the future this aims
    coherence_threshold: float # Minimum coherence needed for satisfaction
    
    def to_vector10d(self) -> Vector10D:
        """Convert to Vector10D representation"""
        return Vector10D(components=self.direction.tolist()[:10])
    
    def magnitude(self) -> float:
        """Total strength of the aim"""
        return self.intensity * np.linalg.norm(self.direction)
    
    def normalized_direction(self) -> np.ndarray:
        """Unit vector in aim direction"""
        norm = np.linalg.norm(self.direction)
        if norm > 0:
            return self.direction / norm
        return self.direction

@dataclass
class SatisfactionCriteria:
    """
    Defines what constitutes satisfaction for an occasion
    """
    coherence_target: float = 0.8      # Target coherence level
    intensity_threshold: float = 0.6   # Minimum felt intensity
    relational_density: float = 0.5    # Connection richness required
    temporal_stability: float = 0.7    # Persistence over time
    ethical_alignment: float = 0.6     # Alignment with values
    novelty_balance: float = 0.4       # Balance of new vs familiar
    
    def evaluate_satisfaction(self, current_state: Dict[str, float]) -> float:
        """
        Evaluate how well current state meets satisfaction criteria
        Returns satisfaction score from 0.0 to 1.0
        """
        scores = []
        
        if "coherence" in current_state:
            coherence_score = min(1.0, current_state["coherence"] / self.coherence_target)
            scores.append(coherence_score)
        
        if "intensity" in current_state:
            intensity_score = min(1.0, current_state["intensity"] / self.intensity_threshold)
            scores.append(intensity_score)
        
        if "relational_density" in current_state:
            relation_score = min(1.0, current_state["relational_density"] / self.relational_density)
            scores.append(relation_score)
        
        if "temporal_stability" in current_state:
            stability_score = min(1.0, current_state["temporal_stability"] / self.temporal_stability)
            scores.append(stability_score)
        
        if "ethical_alignment" in current_state:
            ethics_score = min(1.0, current_state["ethical_alignment"] / self.ethical_alignment)
            scores.append(ethics_score)
        
        if "novelty_balance" in current_state:
            novelty_score = 1.0 - abs(current_state["novelty_balance"] - self.novelty_balance)
            scores.append(novelty_score)
        
        return np.mean(scores) if scores else 0.0

class SubjectiveAim:
    """
    The subjective aim guides an actual occasion's concrescence toward satisfaction.
    
    It represents the teleological aspect of process philosophy - the "final cause"
    that gives direction and meaning to the occasion's becoming.
    
    The subjective aim emerges from:
    1. Initial conditions (inherited from past occasions)
    2. Environmental affordances (what's possible now)
    3. Eternal objects (archetypal lures/forms)
    4. The occasion's own creative activity
    """
    
    def __init__(self, 
                 initial_aim: Optional[AimVector] = None,
                 satisfaction_criteria: Optional[SatisfactionCriteria] = None,
                 salience_model: Optional[SalienceModel] = None):
        
        # Core directional lure
        self.current_aim = initial_aim or AimVector(
            direction=np.random.random(10) * 0.1,  # Gentle random start
            intensity=0.3,
            quality="exploration",
            temporal_horizon=1.0,
            coherence_threshold=0.5
        )
        
        # What constitutes satisfaction
        self.satisfaction_criteria = satisfaction_criteria or SatisfactionCriteria()
        
        # For salience-weighted aim adjustment
        self.salience_model = salience_model
        
        # Aim evolution history
        self.aim_history: List[AimVector] = []
        self.satisfaction_history: List[float] = []
        self.max_history = 50
        
        # Current state tracking
        self.current_satisfaction = 0.0
        self.satisfaction_momentum = 0.0
        self.aim_stability = 0.5
        
        # Archetypal lures (eternal objects)
        self.archetypal_lures = {
            "coherence": np.array([1,0,0,0,0,0,0,0,0,0]),      # Pure coherence
            "connection": np.array([0,1,0,0,0,0,0,0,0,0]),     # Relational density
            "creativity": np.array([0,0,1,0,0,0,0,0,0,0]),     # Novel emergence
            "stability": np.array([0,0,0,1,0,0,0,0,0,0]),      # Temporal persistence
            "transcendence": np.array([0,0,0,0,1,0,0,0,0,0]),  # Higher integration
            "embodiment": np.array([0,0,0,0,0,1,0,0,0,0]),     # Physical grounding
            "meaning": np.array([0,0,0,0,0,0,1,0,0,0]),        # Semantic depth
            "beauty": np.array([0,0,0,0,0,0,0,1,0,0]),         # Aesthetic harmony
            "truth": np.array([0,0,0,0,0,0,0,0,1,0]),          # Accurate prehension
            "freedom": np.array([0,0,0,0,0,0,0,0,0,1]),        # Creative possibility
            "ground_truth_alignment": np.array([0.5,0,0,0,0,0,0,0,0.5,0])  # Hybrid: coherence + truth (NAVI integration)
        }
        
        # Vector components for organ-specific aims
        self.vector_components: Dict[str, float] = {}
    
    def add_vector_component(self, component_name: str, weight: float) -> None:
        """Add a vector component for organ-specific aiming"""
        self.vector_components[component_name] = weight
    
    def calculate_aim_direction(self, current_vector: Vector10D, feeling_vector: Vector10D) -> Vector10D:
        """Calculate aim direction based on current and feeling vectors"""
        direction = Vector10D()
        
        # Simple aim: move toward feeling vector
        for i in range(len(current_vector.dimensions)):
            direction.dimensions[i] = (feeling_vector.dimensions[i] - current_vector.dimensions[i]) * 0.1
        
        # Apply vector component weights
        for component, weight in self.vector_components.items():
            # Simple weighting (can be enhanced)
            for i in range(len(direction.dimensions)):
                direction.dimensions[i] *= weight
        
        return direction
    
    def update_aim(self, 
                   prehension_data: Dict[str, Any],
                   current_state: Dict[str, float],
                   environmental_lures: Optional[Dict[str, np.ndarray]] = None) -> AimVector:
        """
        Update subjective aim based on current experience
        
        This is the core method that evolves the aim during concrescence,
        integrating past experience, present conditions, and future possibilities.
        """
        
        # Store current aim in history
        self._update_history()
        
        # Evaluate current satisfaction
        self.current_satisfaction = self.satisfaction_criteria.evaluate_satisfaction(current_state)
        
        # Calculate satisfaction momentum (rate of change)
        if len(self.satisfaction_history) > 1:
            self.satisfaction_momentum = self.current_satisfaction - self.satisfaction_history[-1]
        
        # Generate new aim components
        
        # 1. Inheritance from past (weighted by satisfaction)
        inherited_component = self._calculate_inherited_aim()
        
        # 2. Environmental response (what's available now)
        environmental_component = self._calculate_environmental_aim(
            prehension_data, environmental_lures
        )
        
        # 3. Archetypal lures (eternal objects)
        archetypal_component = self._calculate_archetypal_aim(current_state)
        
        # 4. Creative novelty (spontaneous emergence)
        creative_component = self._calculate_creative_aim()
        
        # 5. Satisfaction correction (adjust toward fulfillment)
        correction_component = self._calculate_satisfaction_correction(current_state)
        
        # Combine components with dynamic weights
        weights = self._calculate_component_weights(current_state)
        
        new_direction = (
            weights["inherited"] * inherited_component +
            weights["environmental"] * environmental_component +
            weights["archetypal"] * archetypal_component +
            weights["creative"] * creative_component +
            weights["correction"] * correction_component
        )
        
        # Normalize and create new aim
        new_direction = new_direction / (np.linalg.norm(new_direction) + 1e-10)
        
        # Calculate new intensity based on coherence and momentum
        new_intensity = self._calculate_aim_intensity(current_state)
        
        # Determine temporal horizon based on satisfaction trends
        new_horizon = self._calculate_temporal_horizon()
        
        # Select quality based on dominant aim component
        new_quality = self._determine_aim_quality(weights)
        
        # Create updated aim
        self.current_aim = AimVector(
            direction=new_direction,
            intensity=new_intensity,
            quality=new_quality,
            temporal_horizon=new_horizon,
            coherence_threshold=self.current_aim.coherence_threshold * 0.9 + 
                              current_state.get("coherence", 0.5) * 0.1
        )
        
        return self.current_aim
    
    def _calculate_inherited_aim(self) -> np.ndarray:
        """Calculate aim component inherited from past"""
        if not self.aim_history:
            return self.current_aim.direction
        
        # Weight recent aims by their associated satisfaction
        weights = np.array(self.satisfaction_history[-5:])  # Last 5
        aims = [aim.direction for aim in self.aim_history[-5:]]
        
        if len(weights) > 0 and np.sum(weights) > 0:
            weights = weights / np.sum(weights)
            inherited = np.average(aims, axis=0, weights=weights)
        else:
            inherited = self.current_aim.direction
        
        return inherited
    
    def _calculate_environmental_aim(self, 
                                   prehension_data: Dict[str, Any],
                                   environmental_lures: Optional[Dict[str, np.ndarray]]) -> np.ndarray:
        """Calculate aim component from environmental affordances"""
        environmental = np.zeros(10)
        
        # Use salience model to weight environmental factors
        if self.salience_model and prehension_data:
            # Mock subjective aim for salience evaluation
            mock_aim = {"direction": self.current_aim.direction, 
                       "intensity": self.current_aim.intensity}
            
            salience_terms = self.salience_model.evaluate(
                prehension_data, mock_aim
            )
            
            # Weight environmental lures by salience
            if environmental_lures:
                for lure_name, lure_vector in environmental_lures.items():
                    # Map lure types to salience terms (simplified)
                    salience_weight = getattr(salience_terms, "field_resonance", 0.5)
                    environmental += salience_weight * lure_vector[:10]
        
        # Fallback: respond to prehension intensity
        if "intensity" in prehension_data:
            intensity = prehension_data["intensity"]
            environmental[0] = intensity  # Coherence response
        
        return environmental
    
    def _calculate_archetypal_aim(self, current_state: Dict[str, float]) -> np.ndarray:
        """Calculate aim component from eternal objects/archetypal lures"""
        archetypal = np.zeros(10)
        
        # Determine which archetypes are most relevant
        coherence = current_state.get("coherence", 0.5)
        satisfaction = self.current_satisfaction
        
        # Low coherence -> seek stability and coherence
        if coherence < 0.4:
            archetypal += 0.6 * self.archetypal_lures["coherence"]
            archetypal += 0.4 * self.archetypal_lures["stability"]
        
        # Low satisfaction -> seek connection and meaning
        elif satisfaction < 0.4:
            archetypal += 0.5 * self.archetypal_lures["connection"]
            archetypal += 0.5 * self.archetypal_lures["meaning"]
        
        # High coherence and satisfaction -> seek creativity and transcendence
        elif coherence > 0.7 and satisfaction > 0.7:
            archetypal += 0.6 * self.archetypal_lures["creativity"]
            archetypal += 0.4 * self.archetypal_lures["transcendence"]
        
        # Moderate state -> balanced lure toward beauty and truth
        else:
            archetypal += 0.5 * self.archetypal_lures["beauty"]
            archetypal += 0.5 * self.archetypal_lures["truth"]
        
        return archetypal
    
    def _calculate_creative_aim(self) -> np.ndarray:
        """Calculate spontaneous creative component of aim"""
        # Small random component for genuine novelty
        creative = np.random.normal(0, 0.1, 10)
        
        # Modulate by aim stability (more creative when unstable)
        instability = 1.0 - self.aim_stability
        creative *= instability
        
        return creative
    
    def _calculate_satisfaction_correction(self, current_state: Dict[str, float]) -> np.ndarray:
        """Calculate corrective aim toward satisfaction"""
        correction = np.zeros(10)
        
        # If satisfaction is declining, aim toward what's missing
        if self.satisfaction_momentum < -0.1:
            # Identify which criteria are not being met
            criteria = self.satisfaction_criteria
            
            if current_state.get("coherence", 0) < criteria.coherence_target:
                correction += 0.3 * self.archetypal_lures["coherence"]
            
            if current_state.get("relational_density", 0) < criteria.relational_density:
                correction += 0.3 * self.archetypal_lures["connection"]
            
            if current_state.get("temporal_stability", 0) < criteria.temporal_stability:
                correction += 0.2 * self.archetypal_lures["stability"]
            
            if current_state.get("novelty_balance", 0.5) < criteria.novelty_balance:
                correction += 0.2 * self.archetypal_lures["creativity"]
        
        return correction
    
    def _calculate_component_weights(self, current_state: Dict[str, float]) -> Dict[str, float]:
        """Calculate dynamic weights for aim components"""
        coherence = current_state.get("coherence", 0.5)
        satisfaction = self.current_satisfaction
        
        # Base weights
        weights = {
            "inherited": 0.4,      # Past experience
            "environmental": 0.2,   # Present affordances
            "archetypal": 0.2,     # Eternal lures
            "creative": 0.1,       # Novelty
            "correction": 0.1      # Satisfaction adjustment
        }
        
        # Adjust based on current state
        
        # High coherence -> more creative and environmental
        if coherence > 0.7:
            weights["creative"] += 0.1
            weights["environmental"] += 0.1
            weights["inherited"] -= 0.1
            weights["correction"] -= 0.1
        
        # Low coherence -> more archetypal and inherited
        elif coherence < 0.4:
            weights["archetypal"] += 0.15
            weights["inherited"] += 0.05
            weights["creative"] -= 0.1
            weights["environmental"] -= 0.1
        
        # Low satisfaction -> more correction
        if satisfaction < 0.3:
            weights["correction"] += 0.2
            weights["inherited"] -= 0.1
            weights["creative"] -= 0.1
        
        # Normalize weights
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}
        
        return weights
    
    def _calculate_aim_intensity(self, current_state: Dict[str, float]) -> float:
        """Calculate new aim intensity - ENHANCED with pattern confidence scaling"""
        base_intensity = self.current_aim.intensity
        
        # Increase intensity if satisfaction is low
        satisfaction_factor = 1.0 + (0.5 - self.current_satisfaction) * 0.5
        
        # Decrease intensity if coherence is very high (less need for strong aim)
        coherence = current_state.get("coherence", 0.5)
        coherence_factor = 1.0 - (coherence - 0.7) * 0.3 if coherence > 0.7 else 1.0
        
        # Momentum factor (stronger aim if momentum is negative)
        momentum_factor = 1.0 - self.satisfaction_momentum * 0.2
        
        # ENHANCEMENT: Pattern confidence scaling - THIS ADDRESSES THE 30% INTENSITY ISSUE!
        pattern_confidence_factor = self._calculate_pattern_confidence_factor(current_state)
        
        new_intensity = base_intensity * satisfaction_factor * coherence_factor * momentum_factor * pattern_confidence_factor
        
        return np.clip(new_intensity, 0.1, 2.0)  # Allow up to 2.0 for pattern commitment mode
    
    def _calculate_pattern_confidence_factor(self, current_state: Dict[str, float]) -> float:
        """
        ENHANCEMENT: Calculate pattern confidence scaling factor
        This addresses the core issue from task 0b17323b analysis:
        When patterns are detected with high confidence, increase aim intensity dramatically

        🆕 FELT-INTEGRATED GROUND TRUTH LEARNING (Oct 26, 2025):
        Now applies learned pattern confidence from ground truth feedback before
        calculating the confidence factor. This enables 2.5x intensity boost based
        on actual learning, not just current pattern detection.
        """

        # 🆕 Apply learned pattern confidence FIRST (from ground truth learning)
        pattern_type = current_state.get('pattern_type', 'unknown')
        enhanced_state = self.apply_learned_pattern_confidence(current_state, pattern_type)

        # Base factor (no change)
        base_factor = 1.0

        # Check for pattern recognition signals in enhanced state
        pattern_signals = {
            "sequence_strength": enhanced_state.get("sequence_pattern_strength", 0.0),
            "spatial_coherence": enhanced_state.get("spatial_coherence", 0.0),
            "geometric_strength": enhanced_state.get("geometric_strength", 0.0),
            "organ_consensus": enhanced_state.get("organ_pattern_consensus", 0.0)
        }

        # Calculate overall pattern confidence
        pattern_confidence = max(pattern_signals.values())

        # Strong pattern recognition = much higher intensity (up to 2.5x)
        if pattern_confidence > 0.7:
            # High confidence pattern = commitment mode (was 0.3, now up to 0.75)
            confidence_factor = 1.0 + (pattern_confidence - 0.7) * 5.0  # 5x scaling for strong patterns
        elif pattern_confidence > 0.4:
            # Moderate pattern = enhanced exploration (was 0.3, now up to 0.45)
            confidence_factor = 1.0 + (pattern_confidence - 0.4) * 1.5  # 1.5x for moderate patterns
        else:
            # No clear pattern = stay in exploration mode (0.3 intensity)
            confidence_factor = 1.0

        # Additional boost for multiple pattern types (consensus across organs)
        if len([v for v in pattern_signals.values() if v > 0.4]) > 1:
            confidence_factor *= 1.2  # 20% bonus for multi-signal patterns

        return min(2.5, confidence_factor)  # Cap at 2.5x increase

    def apply_learned_pattern_confidence(self,
                                        current_state: Dict[str, float],
                                        pattern_type: str) -> Dict[str, float]:
        """
        Apply learned pattern confidence to current state

        🆕 FELT-INTEGRATED GROUND TRUTH LEARNING (Oct 26, 2025)

        This is called during _calculate_pattern_confidence_factor to incorporate
        ground truth learning. When the EnhancedGroundTruthFeedbackSystem learns
        from training examples, it stores learned_pattern_confidences on this
        subjective aim. We apply those learned confidences to boost pattern signals.

        This enables the 2.5x intensity boost to be based on actual learning,
        not just current pattern detection.

        Args:
            current_state: Current state dict
            pattern_type: Pattern type detected for current task

        Returns:
            Enhanced current_state with learned confidence boosts
        """
        # Check if we have learned confidence for this pattern type
        if not hasattr(self, 'learned_pattern_confidences'):
            return current_state

        learned_confidence = self.learned_pattern_confidences.get(pattern_type, None)

        if learned_confidence is None:
            return current_state

        # Boost pattern signals based on learned confidence
        # learned_confidence is 0.0-1.0 (from ground truth accuracy)
        boost_factor = learned_confidence  # Direct mapping

        enhanced_state = current_state.copy()

        # Boost relevant pattern signals (multiplicative enhancement)
        if 'organ_pattern_consensus' in enhanced_state:
            enhanced_state['organ_pattern_consensus'] = min(
                1.0,
                enhanced_state['organ_pattern_consensus'] * (1.0 + boost_factor * 0.3)
            )

        if 'sequence_pattern_strength' in enhanced_state:
            enhanced_state['sequence_pattern_strength'] = min(
                1.0,
                enhanced_state['sequence_pattern_strength'] * (1.0 + boost_factor * 0.2)
            )

        if 'spatial_coherence' in enhanced_state:
            enhanced_state['spatial_coherence'] = min(
                1.0,
                enhanced_state['spatial_coherence'] * (1.0 + boost_factor * 0.2)
            )

        if 'geometric_strength' in enhanced_state:
            enhanced_state['geometric_strength'] = min(
                1.0,
                enhanced_state['geometric_strength'] * (1.0 + boost_factor * 0.2)
            )

        return enhanced_state
    
    def _calculate_temporal_horizon(self) -> float:
        """Calculate temporal horizon for aim"""
        base_horizon = self.current_aim.temporal_horizon
        
        # Longer horizon if satisfaction is stable
        if abs(self.satisfaction_momentum) < 0.1:
            return min(base_horizon * 1.2, 3.0)
        
        # Shorter horizon if satisfaction is changing rapidly
        else:
            return max(base_horizon * 0.8, 0.5)
    
    def _determine_aim_quality(self, weights: Dict[str, float]) -> str:
        """Determine qualitative description of aim"""
        dominant_component = max(weights.items(), key=lambda x: x[1])[0]
        
        quality_map = {
            "inherited": "consolidation",
            "environmental": "adaptation", 
            "archetypal": "transcendence",
            "creative": "exploration",
            "correction": "satisfaction"
        }
        
        return quality_map.get(dominant_component, "integration")
    
    def _update_history(self):
        """Update aim and satisfaction history"""
        self.aim_history.append(self.current_aim)
        self.satisfaction_history.append(self.current_satisfaction)
        
        # Maintain maximum history size
        if len(self.aim_history) > self.max_history:
            self.aim_history.pop(0)
            self.satisfaction_history.pop(0)
        
        # Update aim stability (consistency of direction)
        if len(self.aim_history) >= 3:
            recent_directions = [aim.direction for aim in self.aim_history[-3:]]
            
            # Calculate average pairwise similarity
            similarities = []
            for i in range(len(recent_directions)):
                for j in range(i+1, len(recent_directions)):
                    similarity = np.dot(recent_directions[i], recent_directions[j])
                    similarities.append(similarity)
            
            self.aim_stability = np.mean(similarities) if similarities else 0.5
    
    def get_vector_feeling(self) -> Vector10D:
        """
        Get current aim as Vector10D for transductive formula
        This is the V⃗f component in T(x) = ƒ(Pₙ, Rₙ, V⃗f, ΔCₙ) → Nₙ₊₁
        """
        return self.current_aim.to_vector10d()
    
    def is_satisfied(self, threshold: float = 0.8) -> bool:
        """Check if current satisfaction meets threshold"""
        return self.current_satisfaction >= threshold
    
    def get_satisfaction_trend(self) -> str:
        """Get trend in satisfaction over time"""
        if len(self.satisfaction_history) < 3:
            return "stable"
        
        recent_trend = np.polyfit(
            range(len(self.satisfaction_history[-5:])), 
            self.satisfaction_history[-5:], 
            1
        )[0]
        
        if recent_trend > 0.05:
            return "increasing"
        elif recent_trend < -0.05:
            return "decreasing"
        else:
            return "stable"
    
    def reset_to_archetypal_lure(self, archetype_name: str, intensity: float = 0.6):
        """Reset aim to a specific archetypal lure"""
        if archetype_name in self.archetypal_lures:
            self.current_aim = AimVector(
                direction=self.archetypal_lures[archetype_name],
                intensity=intensity,
                quality=archetype_name,
                temporal_horizon=1.0,
                coherence_threshold=0.5
            )
    
    def blend_with_external_aim(self, external_aim: AimVector, weight: float = 0.3):
        """Blend current aim with external influence"""
        blended_direction = (
            (1.0 - weight) * self.current_aim.direction +
            weight * external_aim.direction
        )

        blended_direction = blended_direction / (np.linalg.norm(blended_direction) + 1e-10)

        self.current_aim = AimVector(
            direction=blended_direction,
            intensity=(1.0 - weight) * self.current_aim.intensity + weight * external_aim.intensity,
            quality=f"blended_{self.current_aim.quality}_{external_aim.quality}",
            temporal_horizon=(1.0 - weight) * self.current_aim.temporal_horizon + weight * external_aim.temporal_horizon,
            coherence_threshold=self.current_aim.coherence_threshold
        )

    def align_with_ground_truth(self, accuracy: float, clip_lures: bool = True) -> None:
        """
        Modulate archetypal lures based on ground truth accuracy feedback.

        This is the core NAVI integration that connects subjective aim with ground truth.
        Based on the transductive philosophy analysis (Oct 27, 2025), this implements
        appetition-driven learning where entities hunger for ground truth as a supreme
        archetypal lure.

        🌀 APPETITION-DRIVEN LEARNING (not reward/punishment):
        - High accuracy → Satisfy appetite (reinforce truth-seeking direction)
        - Low accuracy → Amplify appetite (increase exploration/creativity)
        - Ground truth becomes attractive through lure intensification

        This integrates with:
        - EnhancedGroundTruthFeedbackSystem (calls this during feedback distribution)
        - V0 Ground State Energy (energy descent toward ground truth minimum)
        - ExpansiveWaveNavigator (noise-based exploration mechanism)

        Args:
            accuracy: Ground truth accuracy [0,1]
            clip_lures: Whether to clip lure values to reasonable range [0.1, 3.0]

        🆕 Oct 27, 2025 - NAVI Phase 1 Organic Integration
        """
        # High accuracy: Satisfy appetite for ground truth
        if accuracy > 0.85:
            # Strong satisfaction - reinforce this direction
            self.archetypal_lures["ground_truth_alignment"] = self.archetypal_lures["ground_truth_alignment"] * 1.20  # 20% boost
            self.archetypal_lures["truth"] = self.archetypal_lures["truth"] * 1.15  # 15% boost
            self.archetypal_lures["coherence"] = self.archetypal_lures["coherence"] * 1.10  # 10% boost

            # NOTE: NOT modifying current_satisfaction directly!
            # Satisfaction is a CONVERGENCE CONFIDENCE metric (inverse correlation with accuracy)
            # See SATISFACTION_CALIBRATION_V2: High accuracy → Lower satisfaction (uncertain but correct)
            # We modulate LURES to guide future processing, not satisfaction itself

        # Moderate accuracy: Gentle reinforcement
        elif accuracy > 0.60:
            # Moderate satisfaction - maintain direction with slight boost
            self.archetypal_lures["ground_truth_alignment"] = self.archetypal_lures["ground_truth_alignment"] * 1.05  # 5% boost
            self.archetypal_lures["truth"] = self.archetypal_lures["truth"] * 1.03  # 3% boost

        # Low accuracy: Amplify appetite for exploration
        elif accuracy < 0.30:
            # Low satisfaction - need more exploration and creativity
            self.archetypal_lures["creativity"] = self.archetypal_lures["creativity"] * 1.30  # 30% boost to exploration
            self.archetypal_lures["transcendence"] = self.archetypal_lures["transcendence"] * 1.20  # 20% boost to higher integration
            self.archetypal_lures["ground_truth_alignment"] = self.archetypal_lures["ground_truth_alignment"] * 1.10  # Still strengthen GT alignment

            # NOTE: NOT modifying current_satisfaction directly!
            # SAFETY GATE: satisfaction_new >= satisfaction_baseline (MATHEMATICAL_SAFETY_ADDENDUM)
            # Satisfaction measures "convergence confidence" not correctness
            # Let the system's natural convergence process compute satisfaction

        # Very low accuracy: Strong appetite amplification
        else:
            # Moderate dissatisfaction - balance exploration and truth-seeking
            self.archetypal_lures["creativity"] = self.archetypal_lures["creativity"] * 1.15
            self.archetypal_lures["ground_truth_alignment"] = self.archetypal_lures["ground_truth_alignment"] * 1.08

        # 🔥 EXPONENTIAL DECAY (Oct 30, 2025) - Fix lure runaway amplification
        # From LURE_ALIGNMENT_ANALYSIS: Multiplicative growth without decay → exponential amplification
        # Solution: Apply exponential decay λ=0.95 per task to all lures
        # After amplification, before clipping
        LURE_DECAY = 0.95  # 5% decay per task prevents runaway feedback
        for lure_name in self.archetypal_lures:
            self.archetypal_lures[lure_name] = self.archetypal_lures[lure_name] * LURE_DECAY

        # Optional: Clip lures to prevent runaway amplification
        if clip_lures:
            for lure_name in self.archetypal_lures:
                self.archetypal_lures[lure_name] = np.clip(
                    self.archetypal_lures[lure_name],
                    0.1,  # Min (weak lure but not dead)
                    3.0   # Max (strong commitment without instability)
                )

        # Update aim stability based on accuracy consistency
        # (More consistent accuracy = more stable aim)
        if hasattr(self, 'accuracy_history'):
            self.accuracy_history.append(accuracy)
            if len(self.accuracy_history) > 5:
                self.accuracy_history = self.accuracy_history[-5:]
            # Calculate stability from accuracy variance
            accuracy_variance = np.var(self.accuracy_history)
            self.aim_stability = 1.0 - min(0.5, accuracy_variance * 2.0)
        else:
            self.accuracy_history = [accuracy]

    def get_state_summary(self) -> Dict[str, Any]:
        """Get summary of current subjective aim state"""
        return {
            "aim_direction": self.current_aim.direction.tolist(),
            "aim_intensity": self.current_aim.intensity,
            "aim_quality": self.current_aim.quality,
            "temporal_horizon": self.current_aim.temporal_horizon,
            "current_satisfaction": self.current_satisfaction,
            "satisfaction_momentum": self.satisfaction_momentum,
            "satisfaction_trend": self.get_satisfaction_trend(),
            "aim_stability": self.aim_stability,
            "coherence_threshold": self.current_aim.coherence_threshold,
            "is_satisfied": self.is_satisfied()
        }