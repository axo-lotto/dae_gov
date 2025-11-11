"""
CARD Core - Multi-Scale Pattern Analysis & Scaling Intelligence
================================================================

Modular CARD core implementation following Vector35D modular architecture.
Focused <150 lines core extracted from 685-line standalone implementation.

Core Responsibility:
- Multi-scale pattern analysis (local → regional → global)
- Grid scaling detection and size-change pattern recognition
- Spatial substrate provision for other organs
- Vector35D scaling intelligence integration

Per DAE 3.0 modular architecture: Clean separation of concerns with Vector35D enhancement
"""

from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import numpy as np
import time

from organs.shared.spatial.base_engine import BaseModularOrgan, OrganProcessingResult
from organs.shared.satisfaction.satisfaction_calculator import SatisfactionCalculator
from organs.card.algorithms.multi_scale_analyzer import MultiScaleAnalyzer
from organs.card.algorithms.scaling_detector import ScalingDetector
from organs.card.card_config import CARDConfig
from organs.shared.propositions import create_scaling_proposition, Proposition


@dataclass
class CARDResult:
    """Focused CARD processing result"""
    coherence: float
    multi_scale_analysis: Dict[str, Any]
    scaling_analysis: Dict[str, Any]
    spatial_relationships: Dict[str, Any]
    transformation_potential: float
    vector35d_enhancement: Optional[Dict] = None
    diagnostics: Optional[Dict] = None

    # V0 Ground State Energy Integration (Week 1 Task 1.2 - Oct 21, 2025)
    v0_spatial_field: Optional[np.ndarray] = None  # (H, W) emission field I
    v0_field_component: str = "emission"  # CARD → I (emission/salience field)

    # Position-mapped propositions (Oct 24, 2025)
    arc_propositions: Optional[List[Proposition]] = None

    # Cross-organ dialogue compatibility attributes
    success: bool = True
    confidence: Optional[float] = None  # Will be derived from coherence if not set
    processing_time: float = 0.0

    def get(self, key: str, default=None):
        """Dict-like access for legacy compatibility"""
        return getattr(self, key, default)

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator for cross-organ dialogue compatibility"""
        return hasattr(self, key)


class CARDCore(BaseModularOrgan):
    """
    CARD Core - Multi-Scale Scaling Intelligence

    Modular implementation focused on:
    - Multi-scale pattern analysis
    - Scaling transformation detection
    - Size-change pattern recognition
    - Vector35D scaling intelligence bundles
    """

    def __init__(self, config: Optional[CARDConfig] = None):
        """Initialize CARD core with configuration"""
        super().__init__("CARD")

        self.config = config or CARDConfig()

        # Initialize algorithm modules
        self.multi_scale_analyzer = MultiScaleAnalyzer(self.config)
        self.scaling_detector = ScalingDetector(self.config)

        # Initialize satisfaction calculator
        self.satisfaction_calculator = SatisfactionCalculator()

        # Performance tracking
        self.scaling_detections = 0
        self.processing_count = 0
        self.pattern_cache = {}

        # ENTITY-NATIVE ARCHITECTURE (Nov 1, 2025): Propositions generated from entity affordances
        # No organ-level accumulation needed - entities store their own affordances

        # Vector35D integration ready
        self.vector35d_enabled = self.config.vector35d_enabled

    def process_symbolic_field(self, symbolic_field: Dict[str, Any]) -> CARDResult:
        """
        Main CARD processing: Multi-scale analysis with scaling intelligence

        Process flow:
        1. Extract grid data and validate
        2. Multi-scale pattern analysis (local → regional → global)
        3. Scaling potential detection (traditional + size-change)
        4. Vector35D scaling intelligence enhancement
        5. Calculate coherence and generate result
        """
        start_time = time.time()
        self.processing_count += 1

        # 🌀 Phase 4a: Extract coherence feedback context if available
        coherence_context = symbolic_field.get('coherence_context', None)
        confidence_multiplier = 1.0
        if coherence_context:
            confidence_multiplier = coherence_context.get('suggested_confidence_multiplier', 1.0)

        try:
            # Extract and validate grid data
            entities = symbolic_field.get('entities', [])
            if not entities:
                return self._empty_result("No entities provided", start_time)

            # Convert entities to grid format for analysis
            grid_data = self._entities_to_grid(entities)
            if not grid_data:
                return self._empty_result("Could not convert entities to grid", start_time)

            # Multi-scale pattern analysis
            multi_scale_analysis = self.multi_scale_analyzer.analyze_patterns(grid_data)

            # Scaling potential detection
            scaling_analysis = self.scaling_detector.detect_scaling_potential(grid_data)

            # Extract spatial relationships for other organs
            spatial_relationships = self._extract_spatial_relationships(grid_data, entities)

            # Vector35D enhancement (if available)
            vector35d_enhancement = self._apply_vector35d_enhancement(
                entities, multi_scale_analysis, scaling_analysis
            )

            # Calculate transformation potential
            transformation_potential = self._calculate_transformation_potential(
                multi_scale_analysis, scaling_analysis
            )

            # Calculate overall coherence
            coherence = self._calculate_coherence(
                multi_scale_analysis, scaling_analysis, transformation_potential
            )

            # Update performance tracking
            if scaling_analysis.get('scaling_possible', False):
                self.scaling_detections += 1

            # Calculate processing confidence
            confidence = self._calculate_confidence(multi_scale_analysis, scaling_analysis)

            # V0 spatial field extraction (Week 1 Task 1.2 - Oct 21, 2025)
            # FIXED (Oct 21, 2025): Extract grid_shape from grid_data instead of requiring it to be passed
            v0_spatial_field = None
            if grid_data:
                # Use the grid dimensions we just computed from entities
                grid_shape = (len(grid_data), len(grid_data[0]) if grid_data else 0)
                v0_spatial_field = self._extract_v0_emission_field(
                    transformation_potential, grid_shape
                )

            # Prehend entities with scaling affordances (Nov 1, 2025 - Entity-Native)
            # Affordances stored in entity prehensions, mature POST-CONVERGENCE
            cycle = symbolic_field.get('cycle', 1)
            print(f"   🐛 CARD DEBUG (process_symbolic_field):")
            print(f"      Entities count: {len(entities)}")
            print(f"      Grid data: {len(grid_data)}×{len(grid_data[0]) if grid_data else 0}")
            print(f"      Cycle: {cycle}")
            self._prehend_entities_with_scaling_affordances(
                entities,
                grid_data,
                multi_scale_analysis,
                scaling_analysis,
                coherence,
                cycle
            )

            # 🌀 COHERENCE FEEDBACK: Confidence multiplier applied during maturation, not here
            # (Entities will apply multiplier when affordances mature to propositions)

            # 🌀 Phase 4a: Apply coherence feedback multiplier
            modulated_coherence = np.clip(coherence * confidence_multiplier, 0.0, 2.0)

            processing_time = time.time() - start_time

            return CARDResult(
                coherence=modulated_coherence,
                multi_scale_analysis=multi_scale_analysis,
                scaling_analysis=scaling_analysis,
                spatial_relationships=spatial_relationships,
                transformation_potential=transformation_potential,
                vector35d_enhancement=vector35d_enhancement,
                v0_spatial_field=v0_spatial_field,  # V0 emission field I
                arc_propositions=None,  # Entity-native: propositions in entity prehensions
                confidence=confidence,
                processing_time=processing_time,
                diagnostics={
                    'scaling_detections': self.scaling_detections,
                    'detection_rate': self.scaling_detections / max(1, self.processing_count),
                    'v0_field_extracted': v0_spatial_field is not None,
                    'affordances_prehended': len([e for e in entities if hasattr(e, 'prehend_with_affordances')])
                }
            )

        except Exception as e:
            return self._empty_result(f"CARD processing error: {str(e)}", start_time)

    def _entities_to_grid(self, entities: List[Any]) -> Optional[List[List[int]]]:
        """Convert ActualOccasion entities to grid format"""
        if not entities:
            return None

        # Extract positions and symbols from entities
        positions = []
        symbols = []

        for entity in entities:
            # Handle both object entities and dict entities
            if hasattr(entity, 'position') and hasattr(entity, 'symbol'):
                # Object-style entity (ActualOccasion)
                pos = entity.position
                if hasattr(pos, 'x') and hasattr(pos, 'y'):
                    positions.append((int(pos.y), int(pos.x)))  # row, col
                    symbols.append(entity.symbol)
            elif isinstance(entity, dict) and 'position' in entity:
                # Dict-style entity (test format)
                pos = entity['position']
                if isinstance(pos, (tuple, list)) and len(pos) >= 2:
                    positions.append((int(pos[0]), int(pos[1])))  # row, col
                    symbols.append(entity.get('value', entity.get('symbol', 0)))

        if not positions:
            return None

        # Determine grid dimensions
        max_row = max(pos[0] for pos in positions)
        max_col = max(pos[1] for pos in positions)

        # Create grid
        grid = [[0 for _ in range(max_col + 1)] for _ in range(max_row + 1)]

        # Fill grid with symbol values
        for (row, col), symbol in zip(positions, symbols):
            # Convert symbol to numeric value for analysis
            if hasattr(symbol, 'value'):
                grid[row][col] = symbol.value
            else:
                grid[row][col] = hash(str(symbol)) % 10 + 1  # Simple symbol to number mapping

        return grid

    def _extract_spatial_relationships(self, grid: List[List[int]], entities: List[Any]) -> Dict[str, Any]:
        """Extract spatial relationships for cross-organ dialogue"""
        return {
            'grid_dimensions': {'height': len(grid), 'width': len(grid[0]) if grid else 0},
            'entity_count': len(entities),
            'density': self._calculate_grid_density(grid),
            'adjacency_map': self._build_adjacency_map(grid),
            'scaling_substrate': True  # CARD provides scaling substrate for other organs
        }

    def _apply_vector35d_enhancement(self, entities: List[Any],
                                   multi_scale: Dict[str, Any],
                                   scaling: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply Vector35D scaling intelligence bundles"""
        if not self.vector35d_enabled:
            return None

        # Vector35D Scaling Intelligence Bundle (dimensions 14-17)
        enhancement = {
            'scaling_bundle_active': True,
            'topological_features': {
                'boundary_sharpness': scaling.get('boundary_confidence', 0.5),
                'information_density': multi_scale.get('complexity_score', 0.5),
                'scaling_connectivity': scaling.get('scaling_confidence', 0.5),
                'pattern_genus': multi_scale.get('pattern_diversity', 0.5)
            },
            'dimensional_range': (14, 18),  # CARD scaling dimensions
            'enhancement_strength': min(1.0, len(entities) / 100.0)  # Scale with entity count
        }

        return enhancement

    def _calculate_transformation_potential(self, multi_scale: Dict[str, Any],
                                          scaling: Dict[str, Any]) -> float:
        """Calculate overall transformation potential"""
        scaling_potential = scaling.get('overall_confidence', 0.0)
        pattern_potential = multi_scale.get('transformation_readiness', 0.0)

        return (scaling_potential * 0.7) + (pattern_potential * 0.3)

    def _calculate_coherence(self, multi_scale: Dict[str, Any],
                           scaling: Dict[str, Any],
                           transformation_potential: float) -> float:
        """Calculate overall CARD coherence using satisfaction calculator"""

        # Calculate intensity from multi-scale analysis quality
        pattern_intensity = multi_scale.get('global_coherence', 0.0)
        scaling_intensity = scaling.get('overall_confidence', 0.0)
        enhanced_intensity = (pattern_intensity * 0.7) + (scaling_intensity * 0.3)

        # Calculate stability from transformation readiness and confidence
        analysis_stability = multi_scale.get('analysis_confidence', 0.5)
        transformation_stability = transformation_potential
        enhanced_stability = min(analysis_stability + transformation_stability * 0.5, 1.0)

        # Use satisfaction calculator for coherence (like BOND and SANS)
        coherence = self.satisfaction_calculator.calculate_organ_coherence(
            intensity=enhanced_intensity,
            stability=enhanced_stability,
            organ_type=self.organ_type
        )

        return coherence

    def _calculate_confidence(self, multi_scale: Dict[str, Any],
                            scaling: Dict[str, Any]) -> float:
        """Calculate processing confidence"""
        pattern_confidence = multi_scale.get('analysis_confidence', 0.5)
        scaling_confidence = scaling.get('overall_confidence', 0.5)

        return (pattern_confidence * 0.6) + (scaling_confidence * 0.4)

    def _calculate_grid_density(self, grid: List[List[int]]) -> float:
        """Calculate non-zero density of grid"""
        if not grid:
            return 0.0

        total_cells = sum(len(row) for row in grid)
        non_zero_cells = sum(1 for row in grid for cell in row if cell != 0)

        return non_zero_cells / total_cells if total_cells > 0 else 0.0

    def _build_adjacency_map(self, grid: List[List[int]]) -> Dict[str, List[str]]:
        """Build adjacency map for spatial relationships"""
        if not grid:
            return {}

        height, width = len(grid), len(grid[0])
        adjacency_map = {}

        for i in range(height):
            for j in range(width):
                cell_key = f"{i}_{j}"
                neighbors = []

                # Check 4-connected neighbors
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < height and 0 <= nj < width:
                        neighbors.append(f"{ni}_{nj}")

                adjacency_map[cell_key] = neighbors

        return adjacency_map

    def _prehend_entities_with_scaling_affordances(self,
                                                     entities: List[Any],
                                                     grid_data: List[List[int]],
                                                     multi_scale_analysis: Dict[str, Any],
                                                     scaling_analysis: Dict[str, Any],
                                                     coherence: float,
                                                     cycle: int):
        """
        Prehend entities with CARD scaling affordances (Entity-Native Architecture, Nov 1 2025).

        Instead of generating external propositions, CARD expresses multi-scale possibilities
        AS entity prehensions. Affordances accumulate salience during organism concrescence,
        then mature to propositions POST-CONVERGENCE with mature V0 context.

        Args:
            entities: List of ActualOccasion entities to prehend
            grid_data: Grid representation for scale analysis
            multi_scale_analysis: Multi-scale pattern detection results
            scaling_analysis: Scaling potential analysis
            coherence: CARD's overall coherence
            cycle: Current processing cycle
        """
        if not entities or not grid_data:
            print("   ⚠️ CARD: No entities or grid data for affordance prehension")
            return

        # Extract scale-level strengths
        scale_strengths = multi_scale_analysis.get('scale_levels', {})
        local_strength = scale_strengths.get('local_coherence', 0.5)
        regional_strength = scale_strengths.get('regional_coherence', 0.5)
        global_strength = scale_strengths.get('global_coherence', 0.5)

        # Get scaling confidence
        scaling_confidence = scaling_analysis.get('overall_confidence', 0.5)
        transformation_potential = scaling_analysis.get('transformation_potential', 0.5)

        height, width = len(grid_data), len(grid_data[0]) if grid_data else 0

        # DEBUG (Nov 3, 2025): Track entity types to understand call paths
        print(f"   🐛 CARD (_prehend_entities): Called with {len(entities)} entities")
        if entities:
            first_entity = entities[0]
            entity_type = type(first_entity).__name__
            has_method = hasattr(first_entity, 'prehend_with_affordances')
            print(f"      Entity type: '{entity_type}', has_prehend_method={has_method}")
            print(f"      Grid: {len(grid_data)}×{len(grid_data[0]) if grid_data else 0}")

        prehended_count = 0
        skipped_count = 0
        position_skip_count = 0
        bounds_skip_count = 0

        for entity in entities:
            if not hasattr(entity, 'prehend_with_affordances'):
                skipped_count += 1
                continue

            # Extract position
            # FIX (Nov 3, 2025): Handle tuple positions directly (same fix as NDAM)
            # CARD's MockEntity sets position as tuple (y, x), not object with .x/.y attributes
            position = None
            if hasattr(entity, 'position') and entity.position is not None:
                pos = entity.position
                # Check if position is already a tuple (CARD's MockEntity format)
                if isinstance(pos, (tuple, list)) and len(pos) >= 2:
                    position = (int(pos[0]), int(pos[1]))  # (y, x) format
                # Legacy check for position with .x and .y attributes
                elif hasattr(pos, 'x') and hasattr(pos, 'y'):
                    position = (int(pos.y), int(pos.x))
            elif isinstance(entity, dict) and 'position' in entity:
                pos = entity['position']
                if isinstance(pos, (tuple, list)) and len(pos) >= 2:
                    position = (int(pos[0]), int(pos[1]))

            if position is None:
                position_skip_count += 1
                continue

            y, x = position
            if y >= height or x >= width:
                bounds_skip_count += 1
                continue

            # Extract current value
            current_value = grid_data[y][x]

            # Determine dominant scale at this position
            edge_proximity = min(y, x, height-1-y, width-1-x) / max(height, width)
            center_y, center_x = height / 2, width / 2
            center_distance = ((y - center_y)**2 + (x - center_x)**2) ** 0.5
            normalized_center_dist = center_distance / ((height**2 + width**2) ** 0.5)

            # Blend scale strengths based on position
            if edge_proximity < 0.2:
                dominant_strength = local_strength * 0.7 + regional_strength * 0.3
                source_pattern = "local_edge_pattern"
            elif normalized_center_dist < 0.3:
                dominant_strength = global_strength * 0.7 + regional_strength * 0.3
                source_pattern = "global_center_pattern"
            else:
                dominant_strength = regional_strength * 0.7 + (local_strength + global_strength) * 0.15
                source_pattern = "regional_pattern"

            # Calculate lure intensity
            lure_intensity = (dominant_strength * 0.6 + scaling_confidence * 0.4)
            lure_intensity = min(max(lure_intensity, 0.0), 1.0)

            # Proposed value (CARD detects patterns, doesn't transform yet)
            proposed_value = current_value

            # Create affordance (NO confidence yet - will be calculated during maturation)
            affordance = {
                'proposed_value': proposed_value,
                'lure_intensity': lure_intensity,
                'organ_specific_score': dominant_strength,  # CARD: multi-scale pattern strength
                'reasoning': f"CARD {source_pattern} at {position}",
                'cycle_generated': cycle,
                'immature': True,
                'salience_score': 0.0,
                'prehension_count': 0,
                # CARD-specific metadata
                'source_pattern': source_pattern,
                'scaling_confidence': scaling_confidence
            }

            # Prehend entity with scaling affordance
            entity.prehend_with_affordances(
                organ_name="CARD",
                interpretation=f"Scaling: {source_pattern}",
                affordances=[affordance],
                cycle=cycle,
                organ_coherence=coherence
            )

            prehended_count += 1

        # Report skip reasons
        if skipped_count > 0:
            print(f"   ⚠️ CARD: Skipped {skipped_count}/{len(entities)} entities (no prehend_with_affordances method)")
        if position_skip_count > 0:
            print(f"   ⚠️ CARD: Skipped {position_skip_count}/{len(entities)} entities (position is None)")
        if bounds_skip_count > 0:
            print(f"   ⚠️ CARD: Skipped {bounds_skip_count}/{len(entities)} entities (out of bounds)")
        print(f"   🌀 CARD: Prehended {prehended_count} entities with scaling affordances")
        print(f"      Total entities: {len(entities)}, Skipped: {skipped_count}, Position=None: {position_skip_count}, Out-of-bounds: {bounds_skip_count}, Prehended: {prehended_count}")

    def _feel_scaling_possibilities(self, grid_data: List[List[int]],
                                        entities: List[Any],
                                        multi_scale_analysis: Dict[str, Any],
                                        scaling_analysis: Dict[str, Any],
                                        coherence: float,
                                        symbolic_field: Optional[Dict[str, Any]] = None,
                                        v0_spatial_field: Optional[np.ndarray] = None) -> List[Proposition]:
        """
        LEGACY METHOD: Generate position-mapped propositions from CARD multi-scale analysis.

        Kept for backward compatibility. Entity-native architecture uses
        _prehend_entities_with_scaling_affordances() instead.

        For each entity position, creates scaling propositions based on:
        - Multi-scale pattern analysis
        - Scaling potential detection
        - Scale level strength

        Args:
            grid_data: Grid representation indexed as grid_data[y][x]
            entities: List of ActualOccasion entities
            multi_scale_analysis: Multi-scale pattern analysis results
            scaling_analysis: Scaling potential detection results
            coherence: Overall CARD coherence
            symbolic_field: Optional symbolic field for v0_context (Oct 31 2025)
            v0_spatial_field: V0 scale modulation field (H, W) for position-specific affinity

        Returns:
            List of Proposition objects for entity positions
        """
        propositions = []

        # 🌀 ORGANIC CONFIDENCE: Extract V0 context for felt/affinity-based confidence (Oct 31, 2025)
        v0_context = {}
        if symbolic_field:
            v0_context = symbolic_field.get('v0_context', {})
        if not v0_context:
            # Create minimal v0_context if not available (fallback)
            v0_context = {
                'current_energy': 1.0,
                'felt_gradient': 0.0,
                'satisfaction': 0.5,
                'phase': None,
                'satisfaction_history': []
            }

        if not grid_data or not entities:
            return propositions

        # Extract scale-level strengths from multi_scale_analysis
        scale_strengths = multi_scale_analysis.get('scale_levels', {})
        local_strength = scale_strengths.get('local_coherence', 0.5)
        regional_strength = scale_strengths.get('regional_coherence', 0.5)
        global_strength = scale_strengths.get('global_coherence', 0.5)

        # Get scaling confidence as lure intensity modifier
        scaling_confidence = scaling_analysis.get('overall_confidence', 0.5)
        transformation_potential = scaling_analysis.get('transformation_potential', 0.5)

        # Process each entity
        for entity in entities:
            # Extract position
            if hasattr(entity, 'position'):
                pos = entity.position
                if hasattr(pos, 'x') and hasattr(pos, 'y'):
                    position = (int(pos.y), int(pos.x))  # (row, col) format
                else:
                    continue
            elif isinstance(entity, dict) and 'position' in entity:
                pos = entity['position']
                if isinstance(pos, (tuple, list)) and len(pos) >= 2:
                    position = (int(pos[0]), int(pos[1]))  # Already (row, col)
                else:
                    continue
            else:
                continue

            # Extract current value at this position
            y, x = position
            if y < len(grid_data) and x < len(grid_data[0]):
                current_value = grid_data[y][x]
            else:
                continue

            # Determine which scale level is strongest for this position
            # Use position-dependent scale selection
            height, width = len(grid_data), len(grid_data[0])

            # Local patterns stronger near edges
            edge_proximity = min(y, x, height-1-y, width-1-x) / max(height, width)

            # Regional patterns stronger in middle zones
            center_y, center_x = height / 2, width / 2
            center_distance = ((y - center_y)**2 + (x - center_x)**2) ** 0.5
            normalized_center_dist = center_distance / ((height**2 + width**2) ** 0.5)

            # Blend scale strengths based on position
            if edge_proximity < 0.2:
                # Near edge - favor local patterns
                dominant_strength = local_strength * 0.7 + regional_strength * 0.3
                source_pattern = "local_edge_pattern"
            elif normalized_center_dist < 0.3:
                # Near center - favor global patterns
                dominant_strength = global_strength * 0.7 + regional_strength * 0.3
                source_pattern = "global_center_pattern"
            else:
                # Middle zone - favor regional patterns
                dominant_strength = regional_strength * 0.7 + (local_strength + global_strength) * 0.15
                source_pattern = "regional_pattern"

            # Calculate lure intensity from scale pattern strength and scaling potential
            lure_intensity = (dominant_strength * 0.6 + scaling_confidence * 0.4)
            lure_intensity = min(max(lure_intensity, 0.0), 1.0)

            # For now, propose the current value (CARD detects patterns, doesn't transform)
            # In future, could use scaling analysis to propose transformed values
            proposed_value = current_value

            # 🌀 ORGANIC CONFIDENCE: Use felt/affinity-based calculation (Oct 31, 2025)
            # Get position-specific V0 scale modulation field value
            v0_field_value = None
            if v0_spatial_field is not None:
                row, col = position
                if 0 <= row < v0_spatial_field.shape[0] and 0 <= col < v0_spatial_field.shape[1]:
                    v0_field_value = float(v0_spatial_field[row, col])

            # Calculate organic confidence using base method
            confidence = self.calculate_organic_confidence(
                position=position,
                organ_coherence=coherence,
                organ_specific_score=dominant_strength,  # CARD-specific: multi-scale pattern strength
                v0_context=v0_context,
                v0_spatial_field_value=v0_field_value
            )

            # Create scaling proposition
            proposition = create_scaling_proposition(
                position=position,
                proposed_value=proposed_value,
                confidence=confidence,  # Organic confidence
                lure_intensity=lure_intensity,
                source_pattern=source_pattern
            )

            propositions.append(proposition)

        return propositions

    def extract_multi_scale_objects(self, entities: List, grid_data: Optional[List[List[int]]] = None) -> List[Dict]:
        """
        🎯 TIER 2: Extract multi-scale pattern objects (Nov 3, 2025)

        Detects objects at multiple scales using CARD's multi-scale analyzer:
        - Local objects: 3×3 neighborhoods, high local coherence (>0.6)
        - Regional objects: Quadrant-level patterns, regional coherence (>0.6)
        - Global objects: Full-grid structures, global coherence (>0.7)

        This is CARD's natural intelligence - multi-scale pattern detection across
        local, regional, and global scales simultaneously.

        Args:
            entities: List of Vector35D entities from organism processing
            grid_data: Optional grid representation (will create from entities if not provided)

        Returns:
            List of multi-scale object dictionaries with:
            - type: 'multi_scale'
            - scale: 'local', 'regional', or 'global'
            - positions: List of (row, col) tuples
            - size: Number of cells in object
            - coherence: Scale-specific coherence score
            - organ: 'CARD'
            - confidence: Weighted by coherence and size proportion
        """
        if not entities:
            return []

        # Convert entities to grid if not provided
        if grid_data is None:
            grid_data = self._entities_to_grid(entities)

        if grid_data is None or (hasattr(grid_data, 'size') and grid_data.size == 0):
            return []

        # Run multi-scale analysis
        multi_scale_analysis = self.multi_scale_analyzer.analyze_patterns(grid_data)
        scale_levels = multi_scale_analysis.get('scale_levels', {})

        local_coherence = scale_levels.get('local_coherence', 0.0)
        regional_coherence = scale_levels.get('regional_coherence', 0.0)
        global_coherence = scale_levels.get('global_coherence', 0.0)

        multi_scale_objects = []
        total_cells = len(entities)

        # LOCAL OBJECTS: 3×3 neighborhoods with high local coherence
        if local_coherence > 0.6:
            # Detect local clusters by grouping adjacent high-coherence cells
            height, width = len(grid_data), len(grid_data[0]) if grid_data else 0

            # Simple local clustering: scan for 3×3 neighborhoods
            for r in range(height - 2):
                for c in range(width - 2):
                    # Extract 3×3 neighborhood
                    neighborhood = []
                    for dr in range(3):
                        for dc in range(3):
                            neighborhood.append((r + dr, c + dc))

                    # Check if neighborhood has uniform values (local object)
                    values = [grid_data[y][x] for y, x in neighborhood]
                    unique_values = len(set(values))

                    # Local object: mostly uniform (≤2 unique values)
                    if unique_values <= 2:
                        # Calculate local object confidence
                        proportion = len(neighborhood) / total_cells if total_cells > 0 else 0.0
                        confidence = local_coherence * (1.0 - (unique_values - 1) * 0.3)

                        multi_scale_objects.append({
                            'type': 'multi_scale',
                            'scale': 'local',
                            'positions': neighborhood,
                            'size': len(neighborhood),
                            'coherence': local_coherence,
                            'organ': 'CARD',
                            'confidence': float(confidence)
                        })

        # REGIONAL OBJECTS: Quadrant-level patterns with regional coherence
        if regional_coherence > 0.6:
            height, width = len(grid_data), len(grid_data[0]) if grid_data else 0
            mid_y, mid_x = height // 2, width // 2

            # Define 4 quadrants
            quadrants = [
                ('top_left', 0, mid_y, 0, mid_x),
                ('top_right', 0, mid_y, mid_x, width),
                ('bottom_left', mid_y, height, 0, mid_x),
                ('bottom_right', mid_y, height, mid_x, width)
            ]

            for quad_name, y1, y2, x1, x2 in quadrants:
                # Extract quadrant positions
                quad_positions = []
                for y in range(y1, y2):
                    for x in range(x1, x2):
                        quad_positions.append((y, x))

                # Check quadrant uniformity
                quad_values = [grid_data[y][x] for y, x in quad_positions]
                unique_values = len(set(quad_values))

                # Regional object: some structure (≤3 unique values)
                if unique_values <= 3:
                    proportion = len(quad_positions) / total_cells if total_cells > 0 else 0.0
                    confidence = regional_coherence * (1.0 - (unique_values - 1) * 0.2)

                    multi_scale_objects.append({
                        'type': 'multi_scale',
                        'scale': 'regional',
                        'quadrant': quad_name,
                        'positions': quad_positions,
                        'size': len(quad_positions),
                        'coherence': regional_coherence,
                        'organ': 'CARD',
                        'confidence': float(confidence)
                    })

        # GLOBAL OBJECT: Full-grid structure with high global coherence
        if global_coherence > 0.7:
            # The entire grid is a single global object
            all_positions = [(y, x) for y in range(len(grid_data)) for x in range(len(grid_data[0]) if grid_data else 0)]

            multi_scale_objects.append({
                'type': 'multi_scale',
                'scale': 'global',
                'positions': all_positions,
                'size': len(all_positions),
                'coherence': global_coherence,
                'organ': 'CARD',
                'confidence': float(global_coherence)  # Global confidence = coherence itself
            })

        # Sort by confidence (highest first)
        multi_scale_objects.sort(key=lambda obj: obj['confidence'], reverse=True)

        return multi_scale_objects

    def _empty_result(self, reason: str, start_time: float) -> CARDResult:
        """Generate sparse-aware result for error/sparse cases"""

        # Instead of 0.0 coherence (which indicates failure), return a minimal baseline
        # that reflects CARD's authentic attempt to process sparse multi-scale data
        sparse_baseline_coherence = 0.12  # Minimal but non-zero multi-scale awareness

        return CARDResult(
            coherence=sparse_baseline_coherence,
            multi_scale_analysis={'sparse_multi_scale_awareness': True},
            scaling_analysis={'scaling_possible': False, 'sparse_context': True},
            spatial_relationships={'minimal_spatial_data': True},
            transformation_potential=0.05,  # Minimal transformation potential
            arc_propositions=[],  # Empty propositions for sparse cases
            confidence=0.15,  # Low but non-zero confidence
            processing_time=time.time() - start_time,
            success=True,  # Change to True - sparse processing is still valid processing
            diagnostics={
                'original_reason': reason,
                'sparse_baseline_applied': True,
                'baseline_coherence': sparse_baseline_coherence,
                'propositions_generated': 0
            }
        )

    def _process_organ_specific(self, symbolic_field: Dict[str, Any]) -> OrganProcessingResult:
        """
        Implementation of BaseModularOrgan abstract method
        Processes using CARD-specific logic and converts to standard result format
        """
        # Use main processing method
        card_result = self.process_symbolic_field(symbolic_field)

        # Convert to OrganProcessingResult for compatibility
        elements_count = len(symbolic_field.get('entities', []))

        return OrganProcessingResult(
            organ_type=self.organ_type,
            coherence=card_result.coherence,
            processing_time=card_result.processing_time,
            elements_processed=elements_count,
            success=card_result.success,
            diagnostics=card_result.diagnostics
        )

    def calculate_symbolic_pressure(self, symbolic_field: Dict[str, Any]) -> float:
        """
        Calculate processing pressure for CARD organ
        Based on field complexity and scaling potential
        """
        entities = symbolic_field.get('entities', [])
        if not entities:
            return 0.0

        # Base pressure from entity count
        entity_pressure = min(len(entities) / 100.0, 1.0)

        # Additional pressure from grid dimensions
        grid_data = self._entities_to_grid(entities)
        if grid_data:
            height, width = len(grid_data), len(grid_data[0]) if grid_data else 0
            dimension_pressure = min((height * width) / 400.0, 1.0)  # Max pressure for 20x20 grid
        else:
            dimension_pressure = 0.0

        # Complexity pressure from value diversity
        unique_values = len(set(entity.get('value', 0) for entity in entities))
        complexity_pressure = min(unique_values / 10.0, 1.0)

        # Combine pressures with scaling-specific weighting
        total_pressure = (
            entity_pressure * 0.4 +
            dimension_pressure * 0.4 +
            complexity_pressure * 0.2
        )

        return min(total_pressure, 1.0)

    def _extract_v0_emission_field(self, transformation_potential: float,
                                     grid_shape: Tuple[int, int]) -> np.ndarray:
        """
        V0 WEEK 1 TASK 1.2 (Oct 21, 2025): Extract CARD emission field I

        Extracts spatially-varying emission field from transformation potential.
        Creates non-uniform field with spatial variation for MODULE 3.

        Args:
            transformation_potential: Global transformation potential [0,1]
            grid_shape: (height, width) of target grid

        Returns:
            np.ndarray: (H, W) emission field where higher values = stronger emission/salience
        """
        h, w = grid_shape

        # FIXED (Oct 21, 2025): Create spatially-varying field instead of uniform
        # Multi-scale spatial variation based on CARD's transformation analysis

        # Base field from transformation potential
        field = np.full((h, w), transformation_potential, dtype=np.float32)

        # Add multi-frequency spatial variation (deterministic, reproducible)
        # This creates rich spatial structure for energy navigation
        y, x = np.ogrid[:h, :w]

        # Multi-frequency patterns (similar to MODULE 3 fallback)
        pattern1 = np.sin(y * np.pi / 3) * np.cos(x * np.pi / 3)  # Primary
        pattern2 = np.sin(y * np.pi / 5) * np.sin(x * np.pi / 7)  # Secondary
        pattern3 = np.cos((y + x) * np.pi / 4)  # Diagonal

        # Combine patterns with amplitudes scaled by transformation potential
        # Higher transformation potential → stronger spatial variation
        amplitude = 0.3 + 0.4 * transformation_potential  # Increased from 0.2+0.3
        pattern = 0.5 + amplitude * (0.5 * pattern1 + 0.3 * pattern2 + 0.2 * pattern3)

        # Normalize pattern to [0, 1]
        pattern = (pattern - pattern.min()) / (pattern.max() - pattern.min() + 1e-10)

        # Blend with base field (higher weight on pattern for variance)
        field = 0.3 * field + 0.7 * pattern  # Increased pattern weight from 0.6 to 0.7

        # Ensure valid range [0, 1]
        field = np.clip(field, 0.0, 1.0)

        # Apply very light smoothing for continuity (reduced from 0.8)
        from scipy.ndimage import gaussian_filter
        field = gaussian_filter(field, sigma=0.5, mode='reflect')
        field = np.clip(field, 0.0, 1.0)

        return field

    def transduce(self, svt_components) -> 'TransductiveNexus':
        """
        SVT Interface: Vector35D-enhanced CARD transduction with scaling intelligence bundles

        🔧 FIX (Nov 3, 2025): This method is LEGACY - kept for compatibility but NOT used for epoch learning.

        Entity-native epoch learning uses process_symbolic_field() with real ActualOccasion entities instead.
        SVT transduce() creates dict MockEntities which don't have prehend_with_affordances(), so prehensions
        would be lost anyway. The real prehensions happen when process_symbolic_field() is called with
        real entities during organism processing.

        Provides compatibility with legacy SVT interface while accessing Vector35D
        scaling intelligence bundles for enhanced multi-scale pattern analysis
        """
        from transductive.base_svt_engine import TransductiveNexus

        # FIX (Oct 24, 2025): Always extract from Pn instead of relying on symbolic_field
        # The symbolic_field attribute may be stale or empty on later cycles
        # Extract entities from SVTComponents.Pn which always has current entity data

        if hasattr(svt_components, 'Pn'):
            # Extract entities from SVTComponents.Pn
            # Convert SVTComponents back to symbolic field format
            entities_data = []
            pn_component = svt_components.Pn

            if pn_component:
                # Extract position and properties from each entity in Pn component
                for entity_key, entity_data in pn_component.items():
                    if isinstance(entity_data, dict):
                        # Handle position tuple from orchestrator: position = (y, x)
                        position = entity_data.get('position', (0, 0))
                        if isinstance(position, (tuple, list)) and len(position) >= 2:
                            y, x = position[0], position[1]  # position is (y, x), extract correctly
                        else:
                            # Fallback to direct x, y if available
                            x = entity_data.get('x', 0)
                            y = entity_data.get('y', 0)

                        # Extract value from properties if not directly available
                        # FIX (Oct 24, 2025): Extract value from multiple sources - symbol, properties, or value field
                        value = entity_data.get('value', 0)
                        if value == 0 and 'properties' in entity_data:
                            value = entity_data['properties'].get('value', 0)
                        # If still no value, try to convert symbol to value
                        if value == 0:
                            symbol = entity_data.get('symbol', '')
                            if isinstance(symbol, int):
                                value = symbol
                            elif isinstance(symbol, str) and symbol.isdigit():
                                value = int(symbol)
                            elif symbol:
                                # Use hash of symbol for non-numeric symbols
                                value = hash(str(symbol)) % 10 + 1

                        # FIX (Nov 3, 2025): Create MockEntity with prehend_with_affordances method
                        # Enables entity-native prehension architecture (same fix as NDAM)
                        position = (y, x)  # Use (row, col) format that _entities_to_grid expects

                        class MockEntity:
                            def __init__(self):
                                self.position = position
                                self.entity_id = entity_key
                                self.properties = entity_data.get('properties', {})
                                self.symbol = entity_data.get('symbol', '')
                                self.value = value
                                self.vector35d = entity_data.get('vector35d', None)
                                self.prehensions = {}  # CRITICAL: Storage for organ prehensions

                            def prehend_with_affordances(self, organ_name, interpretation, affordances, cycle, organ_coherence):
                                """Store organ affordances in entity prehensions dict"""
                                if organ_name not in self.prehensions:
                                    self.prehensions[organ_name] = {}

                                self.prehensions[organ_name]['felt_affordances'] = affordances
                                self.prehensions[organ_name]['interpretation'] = interpretation
                                self.prehensions[organ_name]['cycle'] = cycle
                                self.prehensions[organ_name]['coherence'] = organ_coherence

                        mock_entity = MockEntity()
                        entities_data.append(mock_entity)

            symbolic_field = {
                'entities': entities_data,
                'task_context': 'svt_transduce'
            }
        else:
            # Fallback: create empty symbolic field if no Pn component
            symbolic_field = {
                'entities': [],
                'task_context': 'svt_transduce_no_pn'
            }

        # Process using modular interface
        result = self.process_symbolic_field(symbolic_field)

        # Convert result to TransductiveNexus format
        return TransductiveNexus(
            coherence=result.coherence,
            pressure=result.get('transformation_potential', 0.0),
            vector_field={},  # Empty vector field for now
            constraint_delta=0.0,  # No constraint delta for CARD
            organ_type="CARD",
            metadata={
                "success": result.success,
                "confidence": result.confidence,
                "method": "process_symbolic_field",
                "multi_scale_analysis": result.multi_scale_analysis,
                "scaling_analysis": result.scaling_analysis,
                "spatial_relationships": result.spatial_relationships,
                "vector35d_enhancement": result.vector35d_enhancement,
                "diagnostics": result.diagnostics,
                # V0 Ground State Energy Integration (Week 1 Task 1.2 - Oct 21, 2025)
                'v0_spatial_field': result.v0_spatial_field,
                'v0_field_component': result.v0_field_component,
                # Proposition Bridge (Oct 24, 2025): Include arc_propositions
                'arc_propositions': result.arc_propositions if result.arc_propositions else []
            }
        )

    def generate_spatial_propositions(self, symbolic_field: Dict[str, Any]) -> List:
        """
        ENTITY-NATIVE: Returns empty list (propositions now in entity prehensions).

        CARD expresses multi-scale possibilities through entity affordances,
        which mature to propositions POST-CONVERGENCE in orchestrator.

        Args:
            symbolic_field: Symbolic field containing entities

        Returns:
            Empty list (propositions retrieved from entities during maturation)
        """
        # Process field to prehend entities with affordances
        result = self.process_symbolic_field(symbolic_field)

        # Return empty - propositions now in entity prehensions
        return []

    def reset_accumulation(self):
        """
        ENTITY-NATIVE: No-op (entities manage their own affordances).

        Entity affordances are reset per-task by entity lifecycle,
        not by organ reset.
        """
        pass  # No organ-level accumulation in entity-native architecture

    def learn_grid_transformation(self, input_grid: List[List[int]], output_grid: List[List[int]]) -> Dict[str, Any]:
        """
        EPOCH LEARNING (Nov 3, 2025): Learn numerical/scaling patterns from grid transformations.

        CARD's unique contribution to epoch learning: grid-level numerical and scaling intelligence.
        Unlike other organs that learn entity-level patterns, CARD learns multi-scale structural
        transformations directly from grid data.

        This bypasses entity prehension complexity and leverages CARD's existing multi-scale
        analysis and scaling detection capabilities.

        Args:
            input_grid: INPUT grid (training example)
            output_grid: OUTPUT grid (desired transformation result)

        Returns:
            Dict with learned transformation patterns:
            {
                'scale_factor': float,          # e.g., 2.0 for 2× expansion
                'density_delta': float,         # information density change
                'boundary_evolution': str,      # 'sharpening', 'smoothing', 'stable'
                'pattern_type': str,            # 'expansion', 'compression', 'reshape'
                'confidence': float,            # learning confidence (0-1)
                'multi_scale_shift': Dict       # scale-level coherence changes
            }
        """
        if not input_grid or not output_grid:
            return {'learned': False, 'reason': 'empty_grids'}

        # Multi-scale analysis on both grids
        input_analysis = self.multi_scale_analyzer.analyze(input_grid)
        output_analysis = self.multi_scale_analyzer.analyze(output_grid)

        # Detect scaling transformation
        in_height, in_width = len(input_grid), len(input_grid[0])
        out_height, out_width = len(output_grid), len(output_grid[0])

        scale_h = out_height / in_height if in_height > 0 else 1.0
        scale_w = out_width / in_width if in_width > 0 else 1.0
        scale_factor = (scale_h + scale_w) / 2

        # Determine pattern type
        if abs(scale_factor - 1.0) < 0.1:
            if in_height != out_height or in_width != out_width:
                pattern_type = 'reshape'
            else:
                pattern_type = 'value_transform'
        elif scale_factor > 1.0:
            pattern_type = 'expansion'
        else:
            pattern_type = 'compression'

        # Compute information density shift
        input_density = self._compute_grid_density(input_grid)
        output_density = self._compute_grid_density(output_grid)
        density_delta = output_density - input_density

        # Detect boundary evolution
        input_boundary_score = input_analysis.get('global_analysis', {}).get('boundary_sharpness', 0.5)
        output_boundary_score = output_analysis.get('global_analysis', {}).get('boundary_sharpness', 0.5)
        boundary_delta = output_boundary_score - input_boundary_score

        if abs(boundary_delta) < 0.1:
            boundary_evolution = 'stable'
        elif boundary_delta > 0:
            boundary_evolution = 'sharpening'
        else:
            boundary_evolution = 'smoothing'

        # Multi-scale coherence shift
        input_scales = input_analysis.get('scale_levels', {})
        output_scales = output_analysis.get('scale_levels', {})

        multi_scale_shift = {
            'local_delta': output_scales.get('local_coherence', 0.5) - input_scales.get('local_coherence', 0.5),
            'regional_delta': output_scales.get('regional_coherence', 0.5) - input_scales.get('regional_coherence', 0.5),
            'global_delta': output_scales.get('global_coherence', 0.5) - input_scales.get('global_coherence', 0.5)
        }

        # Calculate learning confidence (based on pattern clarity)
        confidence = min(
            abs(scale_factor - 1.0) + 0.3,  # Scaling clarity
            abs(density_delta) * 2 + 0.2,   # Density change magnitude
            abs(boundary_delta) * 2 + 0.2,  # Boundary evolution magnitude
            1.0
        )

        transformation_pattern = {
            'learned': True,
            'scale_factor': scale_factor,
            'scale_h': scale_h,
            'scale_w': scale_w,
            'density_delta': density_delta,
            'boundary_evolution': boundary_evolution,
            'pattern_type': pattern_type,
            'confidence': confidence,
            'multi_scale_shift': multi_scale_shift,
            'grid_shape_transform': {
                'input_shape': (in_height, in_width),
                'output_shape': (out_height, out_width)
            }
        }

        print(f"   📐 CARD learned {pattern_type}: {in_height}×{in_width} → {out_height}×{out_width}")
        print(f"      Scale: {scale_factor:.2f}×, Density Δ: {density_delta:+.3f}, Boundary: {boundary_evolution}")
        print(f"      Confidence: {confidence:.3f}")

        return transformation_pattern

    def _compute_grid_density(self, grid: List[List[int]]) -> float:
        """Compute information density of grid (fraction of non-zero cells)"""
        if not grid or not grid[0]:
            return 0.0

        total_cells = len(grid) * len(grid[0])
        non_zero_cells = sum(1 for row in grid for val in row if val != 0)

        return non_zero_cells / total_cells if total_cells > 0 else 0.0