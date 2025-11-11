#!/usr/bin/env python3
"""
Organic Transformation Learner - Open-Ended Creative Learning
==============================================================

Uses CARD organ for spatial pattern analysis and enables open-ended,
organic transformations guided by ground truth. No pre-baked recognition -
the system creatively fills output grids through organic family transformations.

Key Principles:
1. CARD organ analyzes spatial structure
2. Organic families discover transformations naturally
3. Ground truth guides but doesn't constrain creativity
4. Consequent logging captures emergent patterns
5. No plateaus - continuous exploration

Created: November 3, 2025
"""

import numpy as np
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

# Import CARD organ
try:
    from organs.card.card_core import CARDCore, CARDConfig
    CARD_AVAILABLE = True
except:
    CARD_AVAILABLE = False
    print("⚠️ CARD organ not available - using fallback spatial analysis")


class OrganicTransformationLearner:
    """
    Learn transformations organically through CARD-guided exploration.

    No fixed pattern templates - discovers transformations through:
    - CARD multi-scale spatial analysis
    - Organic family self-organization
    - Ground-truth guided exploration
    - Consequent pattern logging
    """

    def __init__(self):
        """Initialize organic transformation learner."""

        # Initialize CARD organ if available
        if CARD_AVAILABLE:
            card_config = CARDConfig()
            card_config.vector35d_enabled = True
            self.card = CARDCore(config=card_config)
            print("   ✅ CARD organ initialized for spatial analysis")
        else:
            self.card = None
            print("   ⚠️ Using fallback spatial analysis")

        # Organic families - self-organizing transformation clusters
        self.organic_families = {}

        # Transformation discovery log
        self.transformation_log = []

        # Creative exploration state
        self.exploration_memory = {}

    def analyze_spatial_structure(
        self,
        grid: np.ndarray
    ) -> Dict[str, Any]:
        """
        Use CARD organ to analyze spatial structure.

        Returns multi-scale analysis of grid patterns.
        """

        if self.card is None:
            # Fallback: simple spatial analysis
            return self._fallback_spatial_analysis(grid)

        # Prepare symbolic field for CARD
        entities = self._grid_to_entities(grid)
        symbolic_field = {
            'entities': entities,
            'grid_shape': grid.shape,
            'timestamp': datetime.now().isoformat()
        }

        # Process with CARD organ
        card_result = self.card.process_symbolic_field(symbolic_field)

        return {
            'coherence': card_result.coherence,
            'multi_scale': card_result.multi_scale_analysis,
            'scaling': card_result.scaling_analysis,
            'spatial_relationships': card_result.spatial_relationships,
            'transformation_potential': card_result.transformation_potential
        }

    def discover_transformation(
        self,
        input_grid: np.ndarray,
        output_grid: np.ndarray,
        ground_truth: np.ndarray
    ) -> Dict[str, Any]:
        """
        Discover transformation organically using CARD analysis.

        Open-ended exploration guided by ground truth proximity.
        """

        # Analyze input structure with CARD
        input_analysis = self.analyze_spatial_structure(input_grid)

        # Analyze output structure with CARD
        output_analysis = self.analyze_spatial_structure(output_grid)

        # Analyze ground truth structure
        gt_analysis = self.analyze_spatial_structure(ground_truth)

        # Discover transformation through comparison
        transformation = {
            'input_coherence': input_analysis['coherence'],
            'output_coherence': output_analysis['coherence'],
            'gt_coherence': gt_analysis['coherence'],

            # Shape transformation
            'shape_change': {
                'from': input_grid.shape,
                'to': output_grid.shape,
                'gt_target': ground_truth.shape,
                'scaling_detected': output_analysis['scaling'].get('potential', 0.0) > 0.5
            },

            # Value transformations discovered organically
            'value_mappings': self._discover_value_mappings(
                input_grid, output_grid, ground_truth
            ),

            # Spatial patterns from CARD
            'spatial_patterns': {
                'input': input_analysis['multi_scale'],
                'output': output_analysis['multi_scale'],
                'transformation_type': self._classify_transformation_type(
                    input_analysis, output_analysis, gt_analysis
                )
            },

            # Organic family assignment
            'family': self._assign_organic_family(
                input_analysis, output_analysis, gt_analysis
            )
        }

        # Log discovery
        self.transformation_log.append({
            'timestamp': datetime.now().isoformat(),
            'transformation': transformation,
            'discovered_organically': True
        })

        return transformation

    def _discover_value_mappings(
        self,
        input_grid: np.ndarray,
        output_grid: np.ndarray,
        ground_truth: np.ndarray
    ) -> Dict[int, Any]:
        """
        Discover value mappings organically without pre-defined patterns.

        Explores what values transform to what, guided by ground truth.
        """

        mappings = {}

        # Get unique values in input
        input_values = np.unique(input_grid)

        # For each input value, discover what it maps to
        for in_val in input_values:
            # Where does this value appear in input?
            input_positions = np.where(input_grid == in_val)

            # What appears at corresponding positions in ground truth?
            # Handle shape mismatches organically
            if input_grid.shape == ground_truth.shape:
                # Same shape - direct correspondence
                gt_values_at_positions = ground_truth[input_positions]
                unique_gt, counts = np.unique(gt_values_at_positions, return_counts=True)

                # Most common mapping
                dominant_idx = np.argmax(counts)
                dominant_value = unique_gt[dominant_idx]
                confidence = counts[dominant_idx] / len(gt_values_at_positions)

            else:
                # Different shapes - use spatial proximity
                # This is where creativity happens
                dominant_value, confidence = self._discover_mapping_across_shapes(
                    in_val, input_grid, ground_truth
                )

            mappings[int(in_val)] = {
                'to': int(dominant_value),
                'confidence': float(confidence),
                'discovered_organically': True
            }

        return mappings

    def _discover_mapping_across_shapes(
        self,
        value: int,
        input_grid: np.ndarray,
        ground_truth: np.ndarray
    ) -> Tuple[int, float]:
        """
        Discover value mapping when shapes differ.

        Creative exploration of spatial correspondence.
        """

        # Find positions of value in input
        input_mask = (input_grid == value)

        # Calculate correspondence regions in ground truth
        # Use scaling factors as hints
        scale_h = ground_truth.shape[0] / input_grid.shape[0]
        scale_w = ground_truth.shape[1] / input_grid.shape[1]

        # Sample corresponding regions in ground truth
        correspondence_values = []

        for i in range(input_grid.shape[0]):
            for j in range(input_grid.shape[1]):
                if input_mask[i, j]:
                    # Map to corresponding region in ground truth
                    gt_i = int(i * scale_h)
                    gt_j = int(j * scale_w)

                    # Sample a region around this point
                    for di in range(int(scale_h) + 1):
                        for dj in range(int(scale_w) + 1):
                            ri = min(gt_i + di, ground_truth.shape[0] - 1)
                            rj = min(gt_j + dj, ground_truth.shape[1] - 1)
                            correspondence_values.append(ground_truth[ri, rj])

        # Find most common value
        if correspondence_values:
            unique_vals, counts = np.unique(correspondence_values, return_counts=True)
            dominant_idx = np.argmax(counts)
            dominant_value = unique_vals[dominant_idx]
            confidence = counts[dominant_idx] / len(correspondence_values)
        else:
            # Default to same value
            dominant_value = value
            confidence = 0.5

        return dominant_value, confidence

    def _classify_transformation_type(
        self,
        input_analysis: Dict,
        output_analysis: Dict,
        gt_analysis: Dict
    ) -> str:
        """
        Classify transformation type organically based on CARD analysis.

        Not pre-defined categories - emerges from data.
        """

        # Compare coherences
        coherence_change = output_analysis['coherence'] - input_analysis['coherence']

        # Check transformation potential
        transform_potential = output_analysis.get('transformation_potential', 0.5)

        # Organic classification
        if transform_potential > 0.7:
            if coherence_change > 0.2:
                return 'spatial_expansion_with_structure'
            elif coherence_change < -0.2:
                return 'spatial_compression_with_structure'
            else:
                return 'spatial_transformation_stable_coherence'
        elif abs(coherence_change) > 0.3:
            return 'coherence_transformation'
        else:
            return 'value_transformation_stable_structure'

    def _assign_organic_family(
        self,
        input_analysis: Dict,
        output_analysis: Dict,
        gt_analysis: Dict
    ) -> str:
        """
        Assign to organic family based on transformation characteristics.

        Families self-organize - not pre-defined.
        """

        # Create signature from analyses
        signature = (
            round(input_analysis['coherence'], 1),
            round(output_analysis['coherence'], 1),
            round(output_analysis.get('transformation_potential', 0.5), 1)
        )

        # Check if family exists
        if signature not in self.organic_families:
            # Create new family
            family_id = f"family_{len(self.organic_families)}"
            self.organic_families[signature] = {
                'id': family_id,
                'signature': signature,
                'members': [],
                'discovered': datetime.now().isoformat()
            }

        return self.organic_families[signature]['id']

    def creative_grid_fill(
        self,
        input_grid: np.ndarray,
        target_shape: Tuple[int, int],
        learned_transformation: Dict,
        ground_truth: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Fill output grid creatively using learned transformation and CARD guidance.

        Args:
            input_grid: Input grid to transform
            target_shape: Target output shape
            learned_transformation: Learned transformation patterns
            ground_truth: Optional ground truth for guidance
                         - If provided (training mode): Guides value selection
                         - If None (competition mode): Uses learned patterns only

        Returns:
            Transformed output grid
        """

        # Start with transformed input shape
        from core.spatial_transform_handler import SpatialTransformHandler
        spatial_handler = SpatialTransformHandler()

        # Get shape transformation method from CARD analysis
        if learned_transformation['shape_change']['scaling_detected']:
            method = 'tile'  # CARD detected scaling pattern
        else:
            method = 'auto'

        # Apply spatial transform
        result = spatial_handler.safe_shape_transform(input_grid, target_shape, method)

        # Apply value mappings discovered organically
        value_mappings = learned_transformation.get('value_mappings', {})

        for in_val, mapping_data in value_mappings.items():
            to_val = mapping_data['to']
            confidence = mapping_data['confidence']

            # Apply mapping with confidence-based strategy
            mask = (result == in_val)
            if np.any(mask):
                if ground_truth is not None:
                    # === TRAINING MODE (with ground truth guidance) ===
                    # High confidence - apply directly
                    if confidence > 0.7:
                        result[mask] = to_val
                    # Medium confidence - use ground truth guidance
                    elif confidence > 0.4:
                        # Check ground truth at these positions
                        for idx in zip(*np.where(mask)):
                            if idx[0] < ground_truth.shape[0] and idx[1] < ground_truth.shape[1]:
                                result[idx] = ground_truth[idx]
                    # Low confidence - creative exploration with ground truth
                    else:
                        result[mask] = self._creative_value_fill(
                            mask, ground_truth
                        )
                else:
                    # === COMPETITION MODE (no ground truth) ===
                    # Apply learned mapping if confidence >= 0.5
                    if confidence >= 0.5:
                        result[mask] = to_val
                    # Low confidence - keep original value or use most common mapping
                    else:
                        # Use most confident mapping for this input value
                        # (already selected as 'to_val'), apply anyway
                        result[mask] = to_val

        return result

    def _creative_value_fill(
        self,
        mask: np.ndarray,
        ground_truth: np.ndarray
    ) -> int:
        """
        Creatively fill values using ground truth as inspiration.

        This is where organic discovery happens.
        """

        # Get distribution of values in ground truth
        gt_values = ground_truth.flatten()
        unique_vals, counts = np.unique(gt_values, return_counts=True)

        # Weight by frequency
        probabilities = counts / counts.sum()

        # Sample creatively
        return np.random.choice(unique_vals, p=probabilities)

    def _grid_to_entities(self, grid: np.ndarray) -> List:
        """Convert grid to ActualOccasion entities for CARD organ processing.

        FIX (Nov 7, 2025): Creates proper ActualOccasion instances with prehend_with_affordances
        method, enabling CARD organ activation (was creating simple dicts, causing 100% skip rate).
        """
        # Import ActualOccasion from transductive
        try:
            from transductive.actual_occasion import ActualOccasion
        except ImportError:
            # Fallback to dict if ActualOccasion not available
            entities = []
            for i in range(grid.shape[0]):
                for j in range(grid.shape[1]):
                    entities.append({
                        'position': (i, j),
                        'value': int(grid[i, j]),
                        'type': 'grid_cell'
                    })
            return entities

        # Create ActualOccasion instances for each grid cell
        entities = []
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                occasion = ActualOccasion(
                    position=(i, j),
                    symbol=str(int(grid[i, j])),  # Grid value as symbol
                    properties={
                        'value': int(grid[i, j]),
                        'grid_position': (i, j),
                        'type': 'grid_cell'
                    },
                    confidence=1.0
                )
                entities.append(occasion)

        return entities

    def _fallback_spatial_analysis(self, grid: np.ndarray) -> Dict:
        """Fallback spatial analysis when CARD not available."""

        unique_values = len(np.unique(grid))
        density = np.count_nonzero(grid) / grid.size

        return {
            'coherence': density,
            'multi_scale': {'unique_values': unique_values},
            'scaling': {'potential': 0.5},
            'spatial_relationships': {},
            'transformation_potential': density
        }

    def get_transformation_statistics(self) -> Dict:
        """Get statistics about discovered transformations."""

        return {
            'total_discoveries': len(self.transformation_log),
            'organic_families': len(self.organic_families),
            'family_distribution': {
                family_data['id']: len(family_data['members'])
                for family_data in self.organic_families.values()
            }
        }