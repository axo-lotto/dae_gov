"""
CARD Configuration - Multi-Scale Pattern Analysis & Scaling Intelligence
=========================================================================

Configuration management for modular CARD organ.
Extracted from 685-line standalone implementation for clean separation.

Manages:
- Multi-scale pattern analysis parameters
- Scaling detection thresholds and factors
- Size-change pattern recognition settings
- Vector35D scaling intelligence integration
- Performance and caching parameters

Per DAE 3.0 modular architecture: Configuration separation for clean organ architecture
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Tuple


@dataclass
class CARDConfig:
    """
    CARD Configuration - All multi-scale scaling parameters in one place
    """

    # Core multi-scale analysis parameters
    max_scale_levels: int = 3                    # local, regional, global
    local_pattern_size: int = 3                  # 3x3 local neighborhoods
    regional_min_size: int = 4                   # minimum size for regional analysis
    global_complexity_threshold: float = 0.8     # complexity threshold for analysis

    # Scaling detection parameters
    supported_scaling_factors: List[int] = None  # [2, 3, 4] - set in __post_init__
    scaling_confidence_threshold: float = 0.6    # minimum confidence for scaling detection
    size_change_confidence_threshold: float = 0.5  # minimum confidence for size-change patterns
    uniform_scaling_weight: float = 0.7          # traditional scaling importance
    size_change_weight: float = 0.8              # size-change pattern importance

    # Pattern complexity assessment
    color_diversity_weight: float = 0.5          # color variety importance
    edge_transition_weight: float = 0.5          # edge complexity importance
    max_complexity_colors: int = 8               # max colors for complexity calculation
    complexity_normalization: float = 1.0        # complexity scaling factor

    # Size-change pattern detection
    compression_ratio_threshold: float = 1.5     # minimum ratio for compression detection
    expansion_factor_range: Tuple[int, int] = (2, 4)  # expansion factor limits
    sparse_region_threshold: float = 0.3         # threshold for sparse region detection
    content_density_weight: float = 0.6          # content-based size change importance

    # Spatial relationship extraction
    adjacency_type: str = "4_connected"          # 4_connected or 8_connected
    connected_component_analysis: bool = True     # enable connected component analysis
    color_clustering_enabled: bool = True        # enable color-based clustering
    spatial_substrate_enabled: bool = True       # provide substrate for other organs

    # Vector35D integration settings
    vector35d_enabled: bool = True               # enable Vector35D enhancement
    scaling_bundle_priority: bool = True         # prioritize scaling intelligence bundle
    enhanced_dimension_range: Tuple[int, int] = (14, 18)  # scaling dimensions (14-17)
    topological_features_enabled: bool = True    # enable topological feature analysis
    dimensional_enhancement_strength: float = 1.0  # Vector35D enhancement strength

    # Performance and caching
    max_cache_size: int = 50                     # result cache size
    cache_enabled: bool = True                   # enable result caching
    processing_timeout: float = 0.1             # max processing time per field
    max_entities_processed: int = 1000          # limit for large fields

    # Analysis thresholds
    density_threshold: float = 0.1              # minimum density for analysis
    pattern_significance_threshold: float = 0.3  # minimum pattern significance
    transformation_readiness_threshold: float = 0.4  # minimum transformation readiness

    # Memory and learning parameters
    pattern_memory_size: int = 100              # pattern storage capacity
    scaling_learning_rate: float = 0.2          # scaling success update rate
    success_threshold: float = 0.7              # coherence for pattern storage
    adaptive_thresholds: bool = True            # enable adaptive threshold adjustment

    def __post_init__(self):
        """Set defaults after initialization"""
        if self.supported_scaling_factors is None:
            self.supported_scaling_factors = [2, 3, 4]

    @classmethod
    def create_high_performance(cls) -> 'CARDConfig':
        """Create configuration optimized for high performance"""
        config = CARDConfig()

        # Enhanced scaling detection
        config.scaling_confidence_threshold = 0.5
        config.size_change_confidence_threshold = 0.4
        config.uniform_scaling_weight = 0.8
        config.size_change_weight = 0.9

        # Increased analysis depth
        config.max_scale_levels = 4
        config.global_complexity_threshold = 0.6
        config.pattern_significance_threshold = 0.2

        # Enhanced Vector35D integration
        config.dimensional_enhancement_strength = 1.5
        config.topological_features_enabled = True

        # Performance optimizations
        config.max_cache_size = 100
        config.pattern_memory_size = 200
        config.scaling_learning_rate = 0.3

        return config

    @classmethod
    def create_vector35d_optimized(cls) -> 'CARDConfig':
        """Create configuration optimized for Vector35D integration"""
        config = CARDConfig()

        # Maximum Vector35D integration
        config.vector35d_enabled = True
        config.scaling_bundle_priority = True
        config.dimensional_enhancement_strength = 2.0
        config.topological_features_enabled = True

        # Enhanced scaling intelligence
        config.supported_scaling_factors = [2, 3, 4, 5, 6]
        config.scaling_confidence_threshold = 0.4
        config.size_change_confidence_threshold = 0.3

        # Advanced pattern analysis
        config.max_scale_levels = 4
        config.connected_component_analysis = True
        config.color_clustering_enabled = True

        # Learning and adaptation
        config.adaptive_thresholds = True
        config.scaling_learning_rate = 0.4
        config.pattern_memory_size = 300

        return config

    @classmethod
    def create_scaling_focused(cls) -> 'CARDConfig':
        """Create configuration focused on scaling detection"""
        config = CARDConfig()

        # Maximum scaling detection sensitivity
        config.scaling_confidence_threshold = 0.3
        config.size_change_confidence_threshold = 0.2
        config.uniform_scaling_weight = 1.0
        config.size_change_weight = 1.0

        # Enhanced scaling factor support
        config.supported_scaling_factors = [1.5, 2, 2.5, 3, 3.5, 4, 5, 6]
        config.compression_ratio_threshold = 1.2
        config.expansion_factor_range = (1.5, 6)

        # Reduced complexity requirements
        config.global_complexity_threshold = 0.4
        config.pattern_significance_threshold = 0.1
        config.density_threshold = 0.05

        # Enhanced memory for scaling patterns
        config.pattern_memory_size = 500
        config.max_cache_size = 200

        return config

    def validate(self) -> Dict[str, str]:
        """Validate configuration parameters and return any issues"""
        issues = {}

        # Validate scale levels
        if self.max_scale_levels < 1 or self.max_scale_levels > 5:
            issues['max_scale_levels'] = "Should be between 1 and 5"

        # Validate thresholds
        if not 0.0 <= self.scaling_confidence_threshold <= 1.0:
            issues['scaling_confidence_threshold'] = "Should be between 0.0 and 1.0"

        if not 0.0 <= self.size_change_confidence_threshold <= 1.0:
            issues['size_change_confidence_threshold'] = "Should be between 0.0 and 1.0"

        # Validate weights
        if self.uniform_scaling_weight < 0.0:
            issues['uniform_scaling_weight'] = "Should be non-negative"

        if self.size_change_weight < 0.0:
            issues['size_change_weight'] = "Should be non-negative"

        # Validate dimension range
        if (self.enhanced_dimension_range[0] >= self.enhanced_dimension_range[1] or
            self.enhanced_dimension_range[0] < 0 or self.enhanced_dimension_range[1] > 35):
            issues['enhanced_dimension_range'] = "Should be valid range within 0-35"

        # Validate expansion factor range
        if (self.expansion_factor_range[0] >= self.expansion_factor_range[1] or
            self.expansion_factor_range[0] < 1):
            issues['expansion_factor_range'] = "Should be valid range with minimum 1"

        # Validate performance parameters
        if self.max_cache_size < 1:
            issues['max_cache_size'] = "Should be at least 1"

        if self.processing_timeout <= 0:
            issues['processing_timeout'] = "Should be positive"

        return issues

    def get_optimization_hints(self) -> List[str]:
        """Get optimization hints based on current configuration"""
        hints = []

        # Performance hints
        if self.max_cache_size < 50:
            hints.append("Consider increasing max_cache_size for better performance")

        if self.scaling_confidence_threshold > 0.8:
            hints.append("High scaling_confidence_threshold may miss valid scaling patterns")

        if self.size_change_confidence_threshold > 0.7:
            hints.append("High size_change_confidence_threshold may miss size-change patterns")

        # Vector35D hints
        if not self.vector35d_enabled:
            hints.append("Enable vector35d_enabled for enhanced scaling intelligence")

        if not self.topological_features_enabled and self.vector35d_enabled:
            hints.append("Enable topological_features_enabled for full Vector35D benefits")

        # Analysis depth hints
        if self.max_scale_levels < 3:
            hints.append("Consider increasing max_scale_levels for more comprehensive analysis")

        if not self.connected_component_analysis:
            hints.append("Enable connected_component_analysis for better spatial understanding")

        # Learning hints
        if not self.adaptive_thresholds:
            hints.append("Enable adaptive_thresholds for dynamic optimization")

        if self.pattern_memory_size < 100:
            hints.append("Consider increasing pattern_memory_size for better learning")

        return hints

    def get_vector35d_config(self) -> Dict[str, Any]:
        """Get Vector35D-specific configuration for CARD"""
        return {
            'enhanced': self.vector35d_enabled,
            'scaling_dimensions': list(range(*self.enhanced_dimension_range)),
            'scaling_bundle_priority': self.scaling_bundle_priority,
            'topological_features': self.topological_features_enabled,
            'enhancement_strength': self.dimensional_enhancement_strength,
            'multi_scale_focus': True,
            'scaling_intelligence': True
        }