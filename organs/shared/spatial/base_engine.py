"""
Shared Base Engine for Modular Organs
====================================

Base functionality shared by all modular organs.
Extracted from legacy BaseTransductiveEngine to eliminate duplication.

Provides:
- Common organ interface
- Standardized processing patterns
- Vector35D integration hooks
- Diagnostic capabilities

Per 35D_IMPLEMENTATION_OCCASIONS.md: Shared utilities eliminate duplication
"""

from typing import Dict, Any, Optional, List, Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass
import time


@dataclass
class OrganProcessingResult:
    """Standardized result format for all organs"""
    organ_type: str
    coherence: float
    processing_time: float
    elements_processed: int
    success: bool
    diagnostics: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class ModularOrgan(Protocol):
    """Protocol defining the interface for all modular organs"""

    organ_type: str

    def process_symbolic_field(self, symbolic_field: Dict[str, Any]) -> OrganProcessingResult:
        """Process symbolic field and return standardized result"""
        ...

    def calculate_symbolic_pressure(self, symbolic_field: Dict[str, Any]) -> float:
        """Calculate processing pressure for this organ"""
        ...

    def get_diagnostics(self) -> Dict[str, Any]:
        """Get organ diagnostic information"""
        ...


class BaseModularOrgan(ABC):
    """
    Abstract base class for all modular organs
    Provides common functionality and standardized interface

    V0 Symbiosis Integration (Oct 22, 2025):
    - Parameter adjustment API for felt gradient guidance
    - Dynamic parameter bounds enforcement
    - Adjustment history tracking for learning
    """

    def __init__(self, organ_type: str):
        self.organ_type = organ_type
        self.processing_stats = {
            'total_processes': 0,
            'total_processing_time': 0.0,
            'average_coherence': 0.0,
            'success_rate': 0.0,
            'errors_encountered': 0
        }

        # Common organ capabilities
        self.supports_vector35d = True
        self.supports_pressure_calculation = True
        self.supports_diagnostics = True

        # V0 Symbiosis: Parameter adjustment infrastructure (Oct 22, 2025)
        self._adjustable_params = {}  # name -> {value, min, max, original}
        self._adjustment_history = []  # List of (timestamp, param_name, old_val, new_val, delta)

    def process_symbolic_field(self, symbolic_field: Dict[str, Any]) -> OrganProcessingResult:
        """
        Template method for processing symbolic field
        Provides timing, error handling, and statistics
        """

        start_time = time.time()
        self.processing_stats['total_processes'] += 1

        try:
            # Validate input
            if not self._validate_symbolic_field(symbolic_field):
                return self._create_error_result("Invalid symbolic field", start_time)

            # Count elements for statistics
            elements_count = self._count_elements(symbolic_field)

            # Perform organ-specific processing
            result = self._process_organ_specific(symbolic_field)

            # Create success result
            processing_time = time.time() - start_time
            self._update_processing_stats(result.coherence, processing_time, True)

            return OrganProcessingResult(
                organ_type=self.organ_type,
                coherence=result.coherence,
                processing_time=processing_time,
                elements_processed=elements_count,
                success=True,
                diagnostics=result.diagnostics
            )

        except Exception as e:
            # Create error result
            processing_time = time.time() - start_time
            self._update_processing_stats(0.0, processing_time, False)
            self.processing_stats['errors_encountered'] += 1

            return self._create_error_result(f"Processing error: {str(e)}", start_time)

    @abstractmethod
    def _process_organ_specific(self, symbolic_field: Dict[str, Any]) -> OrganProcessingResult:
        """Organ-specific processing implementation"""
        pass

    @abstractmethod
    def calculate_symbolic_pressure(self, symbolic_field: Dict[str, Any]) -> float:
        """Calculate processing pressure for this organ"""
        pass

    def get_diagnostics(self) -> Dict[str, Any]:
        """Get comprehensive organ diagnostics"""

        return {
            'organ_type': self.organ_type,
            'processing_stats': self.processing_stats,
            'capabilities': {
                'supports_vector35d': self.supports_vector35d,
                'supports_pressure_calculation': self.supports_pressure_calculation,
                'supports_diagnostics': self.supports_diagnostics
            },
            'configuration': self._get_configuration_summary()
        }

    def _validate_symbolic_field(self, symbolic_field: Dict[str, Any]) -> bool:
        """Validate symbolic field structure"""

        if not isinstance(symbolic_field, dict):
            return False

        # Check for required components
        required_keys = ['entities', 'vectors']
        for key in required_keys:
            if key not in symbolic_field:
                return False

        return True

    def _count_elements(self, symbolic_field: Dict[str, Any]) -> int:
        """Count total elements in symbolic field"""

        count = 0

        entities = symbolic_field.get('entities', [])
        count += len(entities) if isinstance(entities, list) else 0

        vectors = symbolic_field.get('vectors', {})
        count += len(vectors) if isinstance(vectors, dict) else 0

        symbols = symbolic_field.get('symbols', [])
        count += len(symbols) if isinstance(symbols, list) else 0

        return count

    def _create_error_result(self, error_message: str, start_time: float) -> OrganProcessingResult:
        """Create standardized error result"""

        processing_time = time.time() - start_time

        return OrganProcessingResult(
            organ_type=self.organ_type,
            coherence=0.0,
            processing_time=processing_time,
            elements_processed=0,
            success=False,
            error_message=error_message
        )

    def _update_processing_stats(self, coherence: float, processing_time: float, success: bool):
        """Update processing statistics"""

        total_processes = self.processing_stats['total_processes']
        total_time = self.processing_stats['total_processing_time'] + processing_time
        current_avg_coherence = self.processing_stats['average_coherence']

        # Update averages
        new_avg_coherence = ((current_avg_coherence * (total_processes - 1)) + coherence) / total_processes

        self.processing_stats.update({
            'total_processing_time': total_time,
            'average_processing_time': total_time / total_processes,
            'average_coherence': new_avg_coherence,
            'success_rate': ((self.processing_stats['success_rate'] * (total_processes - 1)) +
                           (1.0 if success else 0.0)) / total_processes
        })

    def _get_configuration_summary(self) -> Dict[str, Any]:
        """Get organ configuration summary - to be overridden by subclasses"""

        return {
            'organ_type': self.organ_type,
            'base_configuration': 'modular_architecture'
        }

    def reset_statistics(self):
        """Reset processing statistics"""

        self.processing_stats = {
            'total_processes': 0,
            'total_processing_time': 0.0,
            'average_coherence': 0.0,
            'success_rate': 0.0,
            'errors_encountered': 0
        }

    # V0 Symbiosis: Parameter Adjustment API (Oct 22, 2025)
    # ========================================================

    def register_adjustable_parameter(self, name: str, value: float,
                                     min_val: float, max_val: float) -> None:
        """
        Register a parameter as adjustable by V0 felt learning.

        Args:
            name: Parameter name (e.g., 'positive_threshold')
            value: Initial/current value
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Example:
            self.register_adjustable_parameter('positive_threshold', 0.3, 0.15, 0.45)
        """
        self._adjustable_params[name] = {
            'value': value,
            'min': min_val,
            'max': max_val,
            'original': value
        }
        # Also set as instance attribute for direct access
        setattr(self, name, value)

    def adjust_parameter(self, name: str, delta: float) -> Dict[str, Any]:
        """
        Adjust parameter by delta, respecting bounds.

        Args:
            name: Parameter name
            delta: Adjustment amount (can be positive or negative)

        Returns:
            Dictionary with adjustment details:
            - success: Whether adjustment was applied
            - old_value: Value before adjustment
            - new_value: Value after adjustment
            - delta_applied: Actual delta applied (may differ from requested)
            - clipped: Whether value was clipped to bounds

        Example:
            result = organ.adjust_parameter('positive_threshold', -0.05)
            # Decreases threshold by 0.05 if within bounds
        """
        import time

        if name not in self._adjustable_params:
            return {
                'success': False,
                'error': f"Parameter '{name}' not registered as adjustable",
                'registered_params': list(self._adjustable_params.keys())
            }

        param_info = self._adjustable_params[name]
        old_value = param_info['value']
        new_value = old_value + delta

        # Clip to bounds
        clipped = False
        if new_value < param_info['min']:
            new_value = param_info['min']
            clipped = True
        elif new_value > param_info['max']:
            new_value = param_info['max']
            clipped = True

        # Calculate actual delta applied
        delta_applied = new_value - old_value

        # Update parameter
        param_info['value'] = new_value
        setattr(self, name, new_value)

        # Record in history
        self._adjustment_history.append({
            'timestamp': time.time(),
            'param_name': name,
            'old_value': old_value,
            'new_value': new_value,
            'delta_requested': delta,
            'delta_applied': delta_applied,
            'clipped': clipped
        })

        return {
            'success': True,
            'old_value': old_value,
            'new_value': new_value,
            'delta_applied': delta_applied,
            'clipped': clipped,
            'bounds': (param_info['min'], param_info['max'])
        }

    def get_adjustable_parameters(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all adjustable parameters and their current state.

        Returns:
            Dictionary mapping parameter names to their state:
            - value: Current value
            - min: Minimum allowed value
            - max: Maximum allowed value
            - original: Original value at registration
            - drift: How far from original (value - original)
        """
        result = {}
        for name, info in self._adjustable_params.items():
            result[name] = {
                'value': info['value'],
                'min': info['min'],
                'max': info['max'],
                'original': info['original'],
                'drift': info['value'] - info['original']
            }
        return result

    def reset_parameters_to_original(self) -> List[str]:
        """
        Reset all adjustable parameters to their original values.

        Returns:
            List of parameter names that were reset
        """
        reset_params = []
        for name, info in self._adjustable_params.items():
            if info['value'] != info['original']:
                info['value'] = info['original']
                setattr(self, name, info['original'])
                reset_params.append(name)
        return reset_params

    def get_adjustment_history(self, param_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get adjustment history for a parameter (or all parameters).

        Args:
            param_name: Optional parameter name to filter by

        Returns:
            List of adjustment records
        """
        if param_name is None:
            return self._adjustment_history
        else:
            return [h for h in self._adjustment_history if h['param_name'] == param_name]

    def calculate_organic_confidence(
        self,
        position: tuple,
        organ_coherence: float,
        organ_specific_score: float,
        v0_context: Optional[Dict[str, Any]] = None,
        v0_spatial_field_value: Optional[float] = None
    ) -> float:
        """
        🌀 ORGANIC CONFIDENCE CALCULATION (Oct 31, 2025)

        Calculate proposition confidence integrating felt/affinity systems and
        wave training phase awareness. Replaces direct coherence assignment.

        Philosophy:
        - Felt affinity (V0 energy, spatial fields) is PRIMARY
        - Wave training phase modulates confidence (exploration vs convergence)
        - Satisfaction is used INVERSELY (high satisfaction = reduce confidence)
        - Coherence is RELIABILITY modifier, NOT direct confidence
        - Organ-specific signals provide additional boost

        Args:
            position: Grid position (row, col) for this proposition
            organ_coherence: Organ's current coherence (0.0-1.5+)
            organ_specific_score: Organ-specific signal (spatial_score, semantic_intensity, etc.)
            v0_context: Dict containing V0 state:
                - 'current_energy': float (V0 ground state energy)
                - 'felt_gradient': float (V0 felt gradient magnitude)
                - 'satisfaction': float (current cycle satisfaction)
                - 'phase': AppetitivePhase (wave training phase)
                - 'satisfaction_history': List[float] (temporal context)
            v0_spatial_field_value: Position-specific V0 spatial field value

        Returns:
            Organic confidence in [0.0, 1.0] aligned with ground truth affinity

        References:
        - ORGANIC_CONFIDENCE_EVOLUTION_DESIGN_OCT31_2025.md
        - CORRECTED_WAVE_TRAINING_ANALYSIS_OCT31_2025.md
        - SESSION_SUMMARY_ORGANIC_CONFIDENCE_OCT31_2025.md
        """
        import numpy as np

        # Extract V0 context (with safe defaults)
        if v0_context is None:
            v0_context = {}

        v0_energy = v0_context.get('current_energy', 1.0)
        v0_felt_gradient = v0_context.get('felt_gradient', 0.0)
        cycle_satisfaction = v0_context.get('satisfaction', 0.5)
        current_phase = v0_context.get('phase', None)

        # Normalize values for calculation
        def safe_normalize(value, max_val=2.0):
            """Normalize value to [0, 1] range"""
            return min(max(value / max_val, 0.0), 1.0)

        # ================================================================
        # 1. FELT AFFINITY COMPONENT (PRIMARY) - 40-60% weight
        # ================================================================

        # Energy affinity: Low energy = high affinity to ground truth
        energy_affinity = 1.0 - safe_normalize(v0_energy, max_val=2.0)

        # Felt gradient strength: Magnitude of felt pull
        felt_strength = min(abs(v0_felt_gradient), 1.0)

        # Position-specific spatial field affinity
        if v0_spatial_field_value is not None:
            position_affinity = 1.0 - safe_normalize(v0_spatial_field_value, max_val=1.0)
        else:
            position_affinity = 0.5  # Neutral if no field

        # Weighted felt component
        felt_component = (
            position_affinity * 0.4 +
            energy_affinity * 0.4 +
            felt_strength * 0.2
        )

        # ================================================================
        # 2. PHASE-AWARE SATISFACTION MODULATION - Critical for exploration!
        # ================================================================

        if current_phase is not None:
            # Import here to avoid circular dependency
            try:
                from unified_core.wave_training_phases import AppetitivePhase

                if current_phase == AppetitivePhase.EXPANSIVE_PERTURBATION:
                    # Low satisfaction (0.53-0.55) during exploration
                    # REDUCE confidence (exploring possibilities, uncertain)
                    # Satisfaction inverse: high satisfaction = overconfident
                    satisfaction_inverse = 1.0 - cycle_satisfaction
                    sat_modulator = 0.8 + (0.4 * satisfaction_inverse)
                    # Range: [0.8, 1.0] - reduced during exploration

                elif current_phase == AppetitivePhase.FELT_GRADIENT_NAVIGATION:
                    # Mid satisfaction (0.55-0.65) during navigation
                    # NORMAL confidence (converging toward truth)
                    sat_modulator = 0.9 + (0.2 * cycle_satisfaction)
                    # Range: [0.9, 1.1] - normal during navigation

                elif current_phase == AppetitivePhase.CONCRESCENCE_COMPLETION:
                    # High satisfaction (0.59-0.61) during completion
                    # HIGH confidence if LOW energy (found truth)
                    # MODERATE if HIGH energy (false convergence)
                    energy_factor = 1.0 - safe_normalize(v0_energy, max_val=2.0)
                    sat_modulator = 1.0 + (0.3 * energy_factor)
                    # Range: [1.0, 1.3] - high if low energy

                else:
                    sat_modulator = 1.0  # Fallback

            except ImportError:
                # Fallback if wave training not available
                satisfaction_inverse = 1.0 - cycle_satisfaction
                sat_modulator = 0.8 + (0.4 * satisfaction_inverse)

        else:
            # No phase info: use satisfaction inverse
            satisfaction_inverse = 1.0 - cycle_satisfaction
            sat_modulator = 0.8 + (0.4 * satisfaction_inverse)

        # ================================================================
        # 3. COHERENCE AS RELIABILITY (NOT CONFIDENCE!) - 20-30% weight
        # ================================================================

        # Coherence indicates organ reliability, not proposition correctness
        # Use as modulation factor, not direct confidence
        normalized_coherence = safe_normalize(organ_coherence, max_val=1.5)
        reliability = 0.7 + (normalized_coherence * 0.3)
        # Range: [0.7, 1.0] - modulation factor only

        # ================================================================
        # 4. ORGAN-SPECIFIC SIGNAL BOOST - 10-20% additional weight
        # ================================================================

        # Organ-specific signals (spatial_score, semantic_intensity, etc.)
        # provide additional confidence based on organ's specialty
        normalized_organ_score = safe_normalize(organ_specific_score, max_val=1.0)
        organ_boost = normalized_organ_score * 0.2
        # Range: [0.0, 0.2] - additional signal

        # ================================================================
        # 5. FINAL ORGANIC CONFIDENCE CALCULATION
        # ================================================================

        # Combine all components
        base_confidence = felt_component * sat_modulator * reliability
        final_confidence = base_confidence + organ_boost

        # Clip to valid range [0.0, 1.0]
        final_confidence = np.clip(final_confidence, 0.0, 1.0)

        return float(final_confidence)


class OrganCoordinator:
    """
    Coordinates multiple modular organs
    Provides unified interface for orchestrator integration
    """

    def __init__(self):
        self.organs: Dict[str, ModularOrgan] = {}
        self.processing_order = ['constraint', 'semantic', 'spatial', 'temporal', 'archetypal']

    def register_organ(self, organ: ModularOrgan):
        """Register a modular organ"""
        self.organs[organ.organ_type] = organ

    def process_all_organs(self, symbolic_field: Dict[str, Any]) -> Dict[str, OrganProcessingResult]:
        """Process symbolic field with all registered organs"""

        results = {}

        for organ_type in self.processing_order:
            if organ_type in self.organs:
                organ = self.organs[organ_type]
                result = organ.process_symbolic_field(symbolic_field)
                results[organ_type] = result

        return results

    def calculate_all_pressures(self, symbolic_field: Dict[str, Any]) -> Dict[str, float]:
        """Calculate symbolic pressure for all organs"""

        pressures = {}

        for organ_type, organ in self.organs.items():
            try:
                pressure = organ.calculate_symbolic_pressure(symbolic_field)
                pressures[organ_type] = pressure
            except Exception as e:
                pressures[organ_type] = 0.0

        return pressures

    def get_system_diagnostics(self) -> Dict[str, Any]:
        """Get comprehensive system diagnostics"""

        organ_diagnostics = {}
        for organ_type, organ in self.organs.items():
            organ_diagnostics[organ_type] = organ.get_diagnostics()

        return {
            'registered_organs': list(self.organs.keys()),
            'processing_order': self.processing_order,
            'organ_diagnostics': organ_diagnostics,
            'system_status': 'operational' if self.organs else 'no_organs_registered'
        }