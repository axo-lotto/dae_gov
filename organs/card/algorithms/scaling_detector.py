"""
Scaling Detector - CARD Algorithm Module
========================================

Scaling detection and size-change pattern recognition for CARD organ.
Detects traditional uniform scaling and advanced size-change patterns.

Capabilities:
- Uniform scaling detection (2x, 3x, 4x factors)
- Size-change pattern recognition (compression/expansion)
- Content-based scaling analysis
- Scaling confidence assessment

Per DAE 3.0 modular architecture: Focused algorithm module
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np


class ScalingDetector:
    """
    Scaling detection and size-change pattern recognition

    Detects:
    - Traditional uniform scaling patterns
    - Size-change patterns (width/height compression)
    - Content-based reduction patterns
    - Expansion patterns for small grids
    """

    def __init__(self, config):
        """Initialize with CARD configuration"""
        self.config = config
        self.supported_scaling_factors = config.supported_scaling_factors
        self.scaling_confidence_threshold = config.scaling_confidence_threshold
        self.size_change_confidence_threshold = config.size_change_confidence_threshold
        self.compression_ratio_threshold = config.compression_ratio_threshold
        self.expansion_factor_range = config.expansion_factor_range

    def detect_scaling_potential(self, grid: List[List[int]]) -> Dict[str, Any]:
        """
        Comprehensive scaling potential detection

        Analyzes both traditional scaling and size-change patterns
        """
        if not grid or not grid[0]:
            return self._empty_scaling_analysis()

        height, width = len(grid), len(grid[0])

        # Traditional uniform scaling detection
        uniform_scaling = self._detect_uniform_scaling(grid)

        # Size-change pattern detection
        size_change_patterns = self._detect_size_change_patterns(grid)

        # Content-based scaling analysis
        content_analysis = self._analyze_content_scaling(grid)

        # Calculate overall scaling confidence
        overall_confidence = self._calculate_overall_confidence(
            uniform_scaling, size_change_patterns, content_analysis
        )

        # Generate potential output sizes
        potential_outputs = self._generate_potential_outputs(
            grid, uniform_scaling, size_change_patterns
        )

        # Assess scaling feasibility
        scaling_feasibility = self._assess_scaling_feasibility(
            grid, potential_outputs
        )

        return {
            'scaling_possible': (uniform_scaling['possible'] or
                               len(size_change_patterns) > 0),
            'current_dimensions': {'height': height, 'width': width},
            'uniform_scaling': uniform_scaling,
            'size_change_patterns': size_change_patterns,
            'content_analysis': content_analysis,
            'potential_outputs': potential_outputs,
            'scaling_confidence': uniform_scaling['confidence'],
            'size_change_confidence': max([p.get('confidence', 0.0)
                                         for p in size_change_patterns] + [0.0]),
            'overall_confidence': overall_confidence,
            'scaling_feasibility': scaling_feasibility,
            'boundary_confidence': self._calculate_boundary_confidence(grid),
            'pattern_preservation': self._assess_pattern_preservation(grid)
        }

    def _detect_uniform_scaling(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Detect traditional uniform scaling patterns"""
        height, width = len(grid), len(grid[0])

        # Check for scalable dimensions
        scaling_factors = []
        for factor in self.supported_scaling_factors:
            if isinstance(factor, int):  # Only integer factors for uniform scaling
                if height % factor == 0 and width % factor == 0:
                    scaling_factors.append(factor)

        # Calculate pattern complexity for scaling prediction
        complexity = self._assess_scaling_complexity(grid)

        # Calculate scaling confidence
        scaling_confidence = 0.0
        if scaling_factors:
            base_confidence = 0.7
            factor_bonus = min(0.2, len(scaling_factors) * 0.1)
            complexity_penalty = max(0.0, (complexity - 0.8) * 0.3)
            scaling_confidence = max(0.0, base_confidence + factor_bonus - complexity_penalty)

        # Detect block patterns that suggest scaling
        block_patterns = self._detect_block_patterns(grid)

        return {
            'possible': len(scaling_factors) > 0,
            'scaling_factors': scaling_factors,
            'confidence': scaling_confidence,
            'pattern_complexity': complexity,
            'block_patterns': block_patterns,
            'uniform_feasibility': self._assess_uniform_feasibility(grid, scaling_factors)
        }

    def _detect_size_change_patterns(self, grid: List[List[int]]) -> List[Dict[str, Any]]:
        """Detect size reduction/expansion patterns for ARC tasks"""
        height, width = len(grid), len(grid[0])
        patterns = []

        # 1. Width compression patterns (e.g., 3x7 → 3x3)
        if width > height:
            compression_ratio = width / height
            if compression_ratio >= self.compression_ratio_threshold:
                patterns.append({
                    'type': 'width_compression',
                    'source_size': (height, width),
                    'target_size': (height, height),  # Square compression
                    'compression_method': 'column_aggregation',
                    'compression_ratio': compression_ratio,
                    'confidence': min(0.8, 0.4 + (compression_ratio - self.compression_ratio_threshold) * 0.2),
                    'content_preservation': self._assess_compression_content_preservation(grid, 'width')
                })

        # 2. Height compression patterns (e.g., 7x3 → 3x3)
        if height > width:
            compression_ratio = height / width
            if compression_ratio >= self.compression_ratio_threshold:
                patterns.append({
                    'type': 'height_compression',
                    'source_size': (height, width),
                    'target_size': (width, width),  # Square compression
                    'compression_method': 'row_aggregation',
                    'compression_ratio': compression_ratio,
                    'confidence': min(0.8, 0.4 + (compression_ratio - self.compression_ratio_threshold) * 0.2),
                    'content_preservation': self._assess_compression_content_preservation(grid, 'height')
                })

        # 3. Content-based reduction patterns
        content_density = self._analyze_content_density_regions(grid)
        if content_density['sparse_regions'] > 0.5:
            patterns.append({
                'type': 'content_reduction',
                'source_size': (height, width),
                'sparse_ratio': content_density['sparse_regions'],
                'reduction_factor': 2,
                'content_distribution': content_density,
                'confidence': min(0.7, content_density['sparse_regions']),
                'content_preservation': self._assess_content_reduction_preservation(grid, content_density)
            })

        # 4. Expansion patterns (small → large)
        if height <= 3 and width <= 3:
            for expansion_factor in range(self.expansion_factor_range[0],
                                        self.expansion_factor_range[1] + 1):
                patterns.append({
                    'type': 'pattern_expansion',
                    'source_size': (height, width),
                    'target_size': (height * expansion_factor, width * expansion_factor),
                    'expansion_factor': expansion_factor,
                    'expansion_method': 'uniform_scaling',
                    'confidence': 0.6 - (expansion_factor - 2) * 0.1,
                    'content_preservation': self._assess_expansion_content_preservation(grid, expansion_factor)
                })

        # 5. Aspect ratio normalization patterns
        aspect_ratio_patterns = self._detect_aspect_ratio_patterns(grid)
        patterns.extend(aspect_ratio_patterns)

        return patterns

    def _analyze_content_scaling(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze content-based scaling characteristics"""
        height, width = len(grid), len(grid[0])

        # Content distribution analysis
        content_distribution = self._analyze_content_distribution(grid)

        # Scaling sensitivity analysis
        scaling_sensitivity = self._assess_scaling_sensitivity(grid)

        # Information preservation potential
        info_preservation = self._assess_information_preservation(grid)

        return {
            'content_distribution': content_distribution,
            'scaling_sensitivity': scaling_sensitivity,
            'information_preservation': info_preservation,
            'scaling_readiness': self._calculate_scaling_readiness(
                content_distribution, scaling_sensitivity, info_preservation
            )
        }

    def _generate_potential_outputs(self, grid: List[List[int]],
                                  uniform_scaling: Dict[str, Any],
                                  size_change_patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate potential output sizes based on detected patterns"""
        height, width = len(grid), len(grid[0])
        potential_outputs = []

        # Traditional uniform scaling outputs
        if uniform_scaling['possible']:
            for factor in uniform_scaling['scaling_factors']:
                potential_outputs.append({
                    'height': height * factor,
                    'width': width * factor,
                    'factor': factor,
                    'type': 'uniform_scaling',
                    'confidence': uniform_scaling['confidence'],
                    'method': 'traditional_scaling'
                })

        # Size-change pattern outputs
        for pattern in size_change_patterns:
            if 'target_size' in pattern:
                potential_outputs.append({
                    'height': pattern['target_size'][0],
                    'width': pattern['target_size'][1],
                    'factor': pattern.get('compression_ratio') or pattern.get('expansion_factor'),
                    'type': pattern['type'],
                    'confidence': pattern['confidence'],
                    'method': pattern.get('compression_method') or pattern.get('expansion_method', 'size_change')
                })

        # Sort by confidence
        potential_outputs.sort(key=lambda x: x.get('confidence', 0.0), reverse=True)

        return potential_outputs

    def _assess_scaling_complexity(self, grid: List[List[int]]) -> float:
        """Assess pattern complexity for scaling prediction"""
        height, width = len(grid), len(grid[0])

        # Color diversity
        unique_colors = len(set(cell for row in grid for cell in row))
        color_complexity = min(1.0, unique_colors / 8.0)

        # Edge transitions
        transitions = 0
        total_edges = 0

        # Horizontal edges
        for i in range(height):
            for j in range(width - 1):
                if grid[i][j] != grid[i][j + 1]:
                    transitions += 1
                total_edges += 1

        # Vertical edges
        for i in range(height - 1):
            for j in range(width):
                if grid[i][j] != grid[i + 1][j]:
                    transitions += 1
                total_edges += 1

        edge_complexity = transitions / max(1, total_edges)

        # Combined complexity
        complexity = (color_complexity * 0.5) + (edge_complexity * 0.5)
        return min(1.0, complexity)

    def _detect_block_patterns(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Detect block patterns that suggest scaling potential"""
        height, width = len(grid), len(grid[0])

        # Detect uniform blocks of same value
        block_sizes = []

        for block_size in [2, 3, 4]:
            if height >= block_size and width >= block_size:
                blocks_found = 0
                total_possible = (height - block_size + 1) * (width - block_size + 1)

                for i in range(height - block_size + 1):
                    for j in range(width - block_size + 1):
                        if self._is_uniform_block(grid, i, j, block_size):
                            blocks_found += 1

                if total_possible > 0:
                    block_ratio = blocks_found / total_possible
                    if block_ratio > 0.3:  # Significant block presence
                        block_sizes.append({
                            'size': block_size,
                            'ratio': block_ratio,
                            'count': blocks_found
                        })

        return {
            'detected_blocks': block_sizes,
            'max_block_ratio': max([b['ratio'] for b in block_sizes] + [0.0]),
            'scaling_indication': len(block_sizes) > 0
        }

    def _is_uniform_block(self, grid: List[List[int]], start_i: int, start_j: int, block_size: int) -> bool:
        """Check if a block region has uniform values"""
        first_value = grid[start_i][start_j]

        for i in range(start_i, start_i + block_size):
            for j in range(start_j, start_j + block_size):
                if grid[i][j] != first_value:
                    return False

        return True

    def _analyze_content_density_regions(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze content density for size-change detection"""
        height, width = len(grid), len(grid[0])
        total_cells = height * width

        # Count non-zero cells
        non_zero_count = sum(1 for row in grid for cell in row if cell != 0)
        overall_density = non_zero_count / total_cells

        # Analyze in quadrants for sparse region detection
        if height >= 4 and width >= 4:
            mid_h, mid_w = height // 2, width // 2

            quadrants = [
                [row[:mid_w] for row in grid[:mid_h]],  # top-left
                [row[mid_w:] for row in grid[:mid_h]],  # top-right
                [row[:mid_w] for row in grid[mid_h:]],  # bottom-left
                [row[mid_w:] for row in grid[mid_h:]]   # bottom-right
            ]

            sparse_quadrants = 0
            for quadrant in quadrants:
                quad_density = self._calculate_density(quadrant)
                if quad_density < self.config.sparse_region_threshold:
                    sparse_quadrants += 1

            sparse_ratio = sparse_quadrants / 4.0
        else:
            # For small grids, use overall density
            sparse_ratio = 1.0 - overall_density if overall_density < 0.5 else 0.0

        return {
            'sparse_regions': sparse_ratio,
            'dense_regions': 1.0 - sparse_ratio,
            'overall_density': overall_density,
            'total_cells': total_cells,
            'non_zero_cells': non_zero_count
        }

    def _calculate_density(self, grid: List[List[int]]) -> float:
        """Calculate non-zero density of grid"""
        if not grid:
            return 0.0
        total_cells = sum(len(row) for row in grid)
        non_zero_cells = sum(1 for row in grid for cell in row if cell != 0)
        return non_zero_cells / total_cells if total_cells > 0 else 0.0

    def _calculate_overall_confidence(self, uniform_scaling: Dict[str, Any],
                                    size_change_patterns: List[Dict[str, Any]],
                                    content_analysis: Dict[str, Any]) -> float:
        """Calculate overall scaling confidence"""
        confidences = []

        # Uniform scaling confidence
        if uniform_scaling['possible']:
            confidences.append(uniform_scaling['confidence'] * self.config.uniform_scaling_weight)

        # Size-change pattern confidence
        if size_change_patterns:
            max_size_change_confidence = max(p.get('confidence', 0.0) for p in size_change_patterns)
            confidences.append(max_size_change_confidence * self.config.size_change_weight)

        # Content-based confidence
        content_readiness = content_analysis.get('scaling_readiness', 0.0)
        confidences.append(content_readiness * 0.5)

        return max(confidences) if confidences else 0.0

    def _assess_scaling_feasibility(self, grid: List[List[int]],
                                  potential_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess feasibility of different scaling approaches"""
        if not potential_outputs:
            return {'overall_feasibility': 0.0, 'recommended_approach': None}

        # Analyze feasibility of each potential output
        feasibility_scores = []

        for output in potential_outputs:
            feasibility = self._calculate_output_feasibility(grid, output)
            feasibility_scores.append(feasibility)

        overall_feasibility = max(feasibility_scores) if feasibility_scores else 0.0

        # Find best approach
        best_idx = feasibility_scores.index(max(feasibility_scores)) if feasibility_scores else 0
        recommended_approach = potential_outputs[best_idx] if potential_outputs else None

        return {
            'overall_feasibility': overall_feasibility,
            'recommended_approach': recommended_approach,
            'feasibility_scores': feasibility_scores
        }

    def _calculate_output_feasibility(self, grid: List[List[int]], output: Dict[str, Any]) -> float:
        """Calculate feasibility of a specific output configuration"""
        # Base feasibility from confidence
        base_feasibility = output.get('confidence', 0.0)

        # Adjust based on output size reasonableness
        target_height, target_width = output['height'], output['width']
        source_height, source_width = len(grid), len(grid[0])

        # Penalize extreme size changes
        size_change_ratio = (target_height * target_width) / (source_height * source_width)
        if size_change_ratio > 10 or size_change_ratio < 0.1:
            base_feasibility *= 0.5

        # Bonus for common ARC task ratios
        common_ratios = [0.25, 0.5, 2.0, 4.0, 9.0]  # Common ARC scaling ratios
        if any(abs(size_change_ratio - ratio) < 0.1 for ratio in common_ratios):
            base_feasibility += 0.1

        return min(1.0, base_feasibility)

    def _calculate_boundary_confidence(self, grid: List[List[int]]) -> float:
        """Calculate confidence in boundary detection for scaling"""
        height, width = len(grid), len(grid[0])

        # Check boundary clarity (distinct edge values)
        boundary_clarity = 0.0

        # Top/bottom boundary clarity
        top_edge = set(grid[0])
        bottom_edge = set(grid[-1])
        interior_values = set()

        for i in range(1, height - 1):
            for j in range(width):
                interior_values.add(grid[i][j])

        # Calculate how distinct boundaries are from interior
        boundary_values = top_edge | bottom_edge
        boundary_interior_overlap = len(boundary_values & interior_values)
        total_boundary_values = len(boundary_values)

        if total_boundary_values > 0:
            boundary_clarity = 1.0 - (boundary_interior_overlap / total_boundary_values)

        return boundary_clarity

    def _assess_pattern_preservation(self, grid: List[List[int]]) -> float:
        """Assess how well patterns can be preserved during scaling"""
        # Check for repeating patterns that scale well
        pattern_preservation = 0.5  # Default moderate preservation

        # Look for regular patterns
        height, width = len(grid), len(grid[0])

        # Check for row/column repetition
        row_repetition = self._check_row_repetition(grid)
        col_repetition = self._check_column_repetition(grid)

        if row_repetition > 0.7 or col_repetition > 0.7:
            pattern_preservation += 0.3

        # Check for block repetition
        block_repetition = self._check_block_repetition(grid)
        if block_repetition > 0.5:
            pattern_preservation += 0.2

        return min(1.0, pattern_preservation)

    def _check_row_repetition(self, grid: List[List[int]]) -> float:
        """Check for repeating row patterns"""
        height = len(grid)
        if height < 2:
            return 0.0

        matching_rows = 0
        for i in range(height - 1):
            if grid[i] == grid[i + 1]:
                matching_rows += 1

        return matching_rows / max(1, height - 1)

    def _check_column_repetition(self, grid: List[List[int]]) -> float:
        """Check for repeating column patterns"""
        height, width = len(grid), len(grid[0])
        if width < 2:
            return 0.0

        matching_cols = 0
        for j in range(width - 1):
            col1 = [grid[i][j] for i in range(height)]
            col2 = [grid[i][j + 1] for i in range(height)]
            if col1 == col2:
                matching_cols += 1

        return matching_cols / max(1, width - 1)

    def _check_block_repetition(self, grid: List[List[int]]) -> float:
        """Check for repeating block patterns"""
        # This is a simplified version - could be enhanced for more sophisticated block detection
        height, width = len(grid), len(grid[0])

        if height < 2 or width < 2:
            return 0.0

        # Check 2x2 block repetition
        total_blocks = (height - 1) * (width - 1)
        matching_blocks = 0

        for i in range(height - 1):
            for j in range(width - 1):
                # Extract 2x2 block
                block = [grid[i][j], grid[i][j+1], grid[i+1][j], grid[i+1][j+1]]

                # Check if this block pattern repeats nearby
                if self._block_has_nearby_match(grid, i, j, block):
                    matching_blocks += 1

        return matching_blocks / max(1, total_blocks)

    def _block_has_nearby_match(self, grid: List[List[int]], i: int, j: int, target_block: List[int]) -> bool:
        """Check if a block pattern has nearby matches"""
        height, width = len(grid), len(grid[0])

        # Check nearby positions for same block pattern
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue

                ni, nj = i + di, j + dj
                if 0 <= ni < height - 1 and 0 <= nj < width - 1:
                    nearby_block = [grid[ni][nj], grid[ni][nj+1], grid[ni+1][nj], grid[ni+1][nj+1]]
                    if nearby_block == target_block:
                        return True

        return False

    def _empty_scaling_analysis(self) -> Dict[str, Any]:
        """Return empty scaling analysis for invalid input"""
        return {
            'scaling_possible': False,
            'current_dimensions': {'height': 0, 'width': 0},
            'uniform_scaling': {'possible': False, 'scaling_factors': [], 'confidence': 0.0},
            'size_change_patterns': [],
            'content_analysis': {},
            'potential_outputs': [],
            'scaling_confidence': 0.0,
            'size_change_confidence': 0.0,
            'overall_confidence': 0.0,
            'scaling_feasibility': {'overall_feasibility': 0.0},
            'boundary_confidence': 0.0,
            'pattern_preservation': 0.0
        }

    # Additional helper methods for comprehensive analysis
    def _detect_aspect_ratio_patterns(self, grid: List[List[int]]) -> List[Dict[str, Any]]:
        """Detect aspect ratio normalization patterns"""
        height, width = len(grid), len(grid[0])
        patterns = []

        aspect_ratio = width / height if height > 0 else 1.0

        # Detect non-square grids that might benefit from normalization
        if abs(aspect_ratio - 1.0) > 0.5:  # Significantly non-square
            # Suggest square normalization
            target_size = max(height, width)
            patterns.append({
                'type': 'aspect_ratio_normalization',
                'source_size': (height, width),
                'target_size': (target_size, target_size),
                'current_aspect_ratio': aspect_ratio,
                'target_aspect_ratio': 1.0,
                'confidence': min(0.6, abs(aspect_ratio - 1.0) / 2.0)
            })

        return patterns

    def _analyze_content_distribution(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze how content is distributed in the grid"""
        height, width = len(grid), len(grid[0])

        # Center vs edge distribution
        center_density = self._calculate_center_density(grid)
        edge_density = self._calculate_edge_density(grid)

        # Quadrant distribution
        quadrant_densities = self._calculate_quadrant_densities(grid)

        return {
            'center_density': center_density,
            'edge_density': edge_density,
            'quadrant_densities': quadrant_densities,
            'distribution_balance': self._calculate_distribution_balance(quadrant_densities)
        }

    def _calculate_center_density(self, grid: List[List[int]]) -> float:
        """Calculate density in center region"""
        height, width = len(grid), len(grid[0])
        if height < 3 or width < 3:
            return self._calculate_density(grid)

        # Define center region (middle third)
        start_h, end_h = height // 3, 2 * height // 3
        start_w, end_w = width // 3, 2 * width // 3

        center_cells = []
        for i in range(start_h, end_h):
            for j in range(start_w, end_w):
                center_cells.append(grid[i][j])

        non_zero = sum(1 for cell in center_cells if cell != 0)
        return non_zero / len(center_cells) if center_cells else 0.0

    def _calculate_edge_density(self, grid: List[List[int]]) -> float:
        """Calculate density in edge region"""
        height, width = len(grid), len(grid[0])

        edge_cells = []
        # Top and bottom rows
        edge_cells.extend(grid[0])
        edge_cells.extend(grid[-1])

        # Left and right columns (excluding corners)
        for i in range(1, height - 1):
            edge_cells.extend([grid[i][0], grid[i][-1]])

        non_zero = sum(1 for cell in edge_cells if cell != 0)
        return non_zero / len(edge_cells) if edge_cells else 0.0

    def _calculate_quadrant_densities(self, grid: List[List[int]]) -> List[float]:
        """Calculate density in each quadrant"""
        height, width = len(grid), len(grid[0])
        if height < 2 or width < 2:
            return [self._calculate_density(grid)]

        mid_h, mid_w = height // 2, width // 2

        quadrants = [
            [row[:mid_w] for row in grid[:mid_h]],  # top-left
            [row[mid_w:] for row in grid[:mid_h]],  # top-right
            [row[:mid_w] for row in grid[mid_h:]],  # bottom-left
            [row[mid_w:] for row in grid[mid_h:]]   # bottom-right
        ]

        return [self._calculate_density(quad) for quad in quadrants]

    def _calculate_distribution_balance(self, quadrant_densities: List[float]) -> float:
        """Calculate how balanced the distribution is across quadrants"""
        if not quadrant_densities:
            return 0.5

        variance = np.var(quadrant_densities)
        balance = 1.0 / (1.0 + variance * 4)  # Convert variance to balance score
        return balance

    def _assess_scaling_sensitivity(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Assess how sensitive patterns are to scaling operations"""
        return {
            'fine_detail_presence': self._check_fine_detail(grid),
            'pattern_regularity': self._check_pattern_regularity(grid),
            'scaling_robustness': self._estimate_scaling_robustness(grid)
        }

    def _check_fine_detail(self, grid: List[List[int]]) -> float:
        """Check for fine details that might be lost in scaling"""
        height, width = len(grid), len(grid[0])
        if height < 3 or width < 3:
            return 0.0

        # Look for isolated pixels (fine details)
        isolated_pixels = 0
        total_non_zero = 0

        for i in range(1, height - 1):
            for j in range(1, width - 1):
                if grid[i][j] != 0:
                    total_non_zero += 1

                    # Check if surrounded by different values
                    neighbors = [grid[i-1][j], grid[i+1][j], grid[i][j-1], grid[i][j+1]]
                    if all(neighbor != grid[i][j] for neighbor in neighbors):
                        isolated_pixels += 1

        return isolated_pixels / max(1, total_non_zero)

    def _check_pattern_regularity(self, grid: List[List[int]]) -> float:
        """Check how regular/periodic the patterns are"""
        # This is a simplified version - could be enhanced with FFT analysis
        row_regularity = self._check_row_repetition(grid)
        col_regularity = self._check_column_repetition(grid)

        return (row_regularity + col_regularity) / 2

    def _estimate_scaling_robustness(self, grid: List[List[int]]) -> float:
        """Estimate how robust patterns are to scaling operations"""
        fine_detail = self._check_fine_detail(grid)
        regularity = self._check_pattern_regularity(grid)

        # High regularity and low fine detail = high robustness
        robustness = regularity * (1.0 - fine_detail)
        return robustness

    def _assess_information_preservation(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Assess how well information can be preserved during scaling"""
        return {
            'entropy': self._calculate_information_entropy(grid),
            'compressibility': self._estimate_compressibility(grid),
            'redundancy': self._calculate_pattern_redundancy(grid)
        }

    def _calculate_information_entropy(self, grid: List[List[int]]) -> float:
        """Calculate information entropy of the grid"""
        from collections import Counter

        all_values = [cell for row in grid for cell in row]
        if not all_values:
            return 0.0

        value_counts = Counter(all_values)
        total_cells = len(all_values)

        entropy = 0.0
        for count in value_counts.values():
            probability = count / total_cells
            if probability > 0:
                entropy -= probability * np.log2(probability)

        return entropy

    def _estimate_compressibility(self, grid: List[List[int]]) -> float:
        """Estimate how compressible the pattern is"""
        # Simple estimate based on repetition
        height, width = len(grid), len(grid[0])
        total_cells = height * width

        unique_values = len(set(cell for row in grid for cell in row))
        compressibility = 1.0 - (unique_values / total_cells)

        return max(0.0, compressibility)

    def _calculate_pattern_redundancy(self, grid: List[List[int]]) -> float:
        """Calculate how much redundancy exists in patterns"""
        # Combine row and column repetition as a measure of redundancy
        row_redundancy = self._check_row_repetition(grid)
        col_redundancy = self._check_column_repetition(grid)

        return (row_redundancy + col_redundancy) / 2

    def _calculate_scaling_readiness(self, content_distribution: Dict[str, Any],
                                   scaling_sensitivity: Dict[str, Any],
                                   info_preservation: Dict[str, Any]) -> float:
        """Calculate overall scaling readiness score"""
        # Balance between distribution, sensitivity, and preservation
        distribution_score = content_distribution.get('distribution_balance', 0.5)
        robustness_score = scaling_sensitivity.get('scaling_robustness', 0.5)
        preservation_score = info_preservation.get('compressibility', 0.5)

        readiness = (distribution_score + robustness_score + preservation_score) / 3
        return readiness

    def _assess_uniform_feasibility(self, grid: List[List[int]], scaling_factors: List[int]) -> float:
        """Assess feasibility of uniform scaling approaches"""
        if not scaling_factors:
            return 0.0

        # Higher feasibility for more factors and better pattern characteristics
        factor_score = min(1.0, len(scaling_factors) / 3.0)
        complexity_score = 1.0 - self._assess_scaling_complexity(grid)

        return (factor_score + complexity_score) / 2

    def _assess_compression_content_preservation(self, grid: List[List[int]], direction: str) -> float:
        """Assess how well content can be preserved during compression"""
        if direction == 'width':
            # Analyze column similarity for width compression
            height, width = len(grid), len(grid[0])
            column_similarities = []

            for j in range(width - 1):
                col1 = [grid[i][j] for i in range(height)]
                col2 = [grid[i][j + 1] for i in range(height)]
                similarity = sum(1 for a, b in zip(col1, col2) if a == b) / len(col1)
                column_similarities.append(similarity)

            return np.mean(column_similarities) if column_similarities else 0.0

        elif direction == 'height':
            # Analyze row similarity for height compression
            height = len(grid)
            row_similarities = []

            for i in range(height - 1):
                similarity = sum(1 for a, b in zip(grid[i], grid[i + 1]) if a == b) / len(grid[i])
                row_similarities.append(similarity)

            return np.mean(row_similarities) if row_similarities else 0.0

        return 0.5

    def _assess_content_reduction_preservation(self, grid: List[List[int]],
                                             content_density: Dict[str, Any]) -> float:
        """Assess content preservation during content-based reduction"""
        # Higher sparse regions means better preservation potential
        sparse_ratio = content_density.get('sparse_regions', 0.0)
        overall_density = content_density.get('overall_density', 1.0)

        # High sparse ratio and low overall density = good preservation
        preservation = sparse_ratio * (1.0 - overall_density)
        return preservation

    def _assess_expansion_content_preservation(self, grid: List[List[int]], expansion_factor: int) -> float:
        """Assess content preservation during expansion"""
        # Expansion generally preserves content well, but depends on pattern regularity
        regularity = self._check_pattern_regularity(grid)

        # Higher regularity = better expansion preservation
        # Larger expansion factors are slightly penalized
        preservation = regularity * (1.0 - (expansion_factor - 2) * 0.1)
        return max(0.0, preservation)