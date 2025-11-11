"""
Multi-Scale Analyzer - CARD Algorithm Module
============================================

Multi-scale pattern analysis for CARD organ.
Analyzes patterns at local, regional, and global scales.

Capabilities:
- Local pattern analysis (3x3 neighborhoods)
- Regional analysis (quadrants/sections)
- Global pattern detection (symmetries, density, complexity)
- Pattern transformation readiness assessment

Per DAE 3.0 modular architecture: Focused algorithm module
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np


class MultiScaleAnalyzer:
    """
    Multi-scale pattern analysis for CARD organ

    Analyzes patterns at multiple scales:
    - Local: 3x3 neighborhood patterns
    - Regional: Quadrant/section analysis
    - Global: Overall pattern properties
    """

    def __init__(self, config):
        """Initialize with CARD configuration"""
        self.config = config
        self.max_scale_levels = config.max_scale_levels
        self.local_pattern_size = config.local_pattern_size
        self.regional_min_size = config.regional_min_size

    def analyze_patterns(self, grid: List[List[int]]) -> Dict[str, Any]:
        """
        Perform multi-scale pattern analysis

        Returns comprehensive analysis across all scales
        """
        # Safe emptiness check (avoids NumPy truth value ambiguity)
        if grid is None:
            return self._empty_analysis()
        if hasattr(grid, 'size') and grid.size == 0:
            return self._empty_analysis()
        if isinstance(grid, list) and (not grid or not grid[0]):
            return self._empty_analysis()

        # Convert numpy array to list for consistent processing
        # (avoids NumPy truth value ambiguity errors throughout the code)
        if hasattr(grid, 'tolist'):
            grid = grid.tolist()

        height, width = len(grid), len(grid[0])

        # Global scale analysis
        global_analysis = self._analyze_global_patterns(grid)

        # Regional analysis (if grid is large enough)
        regional_analysis = {}
        if height >= self.regional_min_size and width >= self.regional_min_size:
            regional_analysis = self._analyze_regional_patterns(grid)

        # Local pattern analysis
        local_analysis = self._analyze_local_patterns(grid)

        # Calculate overall metrics
        complexity_score = self._calculate_complexity_score(
            global_analysis, regional_analysis, local_analysis
        )

        transformation_readiness = self._assess_transformation_readiness(
            global_analysis, regional_analysis, local_analysis
        )

        pattern_diversity = self._calculate_pattern_diversity(
            global_analysis, regional_analysis, local_analysis
        )

        # Calculate analysis confidence
        analysis_confidence = self._calculate_analysis_confidence(
            global_analysis, regional_analysis, local_analysis
        )

        return {
            'global': global_analysis,
            'regional': regional_analysis,
            'local': local_analysis,
            'scales_analyzed': self._get_scales_analyzed(regional_analysis),
            'complexity_score': complexity_score,
            'transformation_readiness': transformation_readiness,
            'pattern_diversity': pattern_diversity,
            'analysis_confidence': analysis_confidence,
            'global_coherence': self._calculate_global_coherence(
                global_analysis, complexity_score, pattern_diversity
            )
        }

    def _analyze_global_patterns(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze global-scale patterns"""
        height, width = len(grid), len(grid[0])

        # Basic properties
        dimensions = {'height': height, 'width': width}
        total_cells = height * width
        color_counts = self._count_colors(grid)
        density = self._calculate_density(grid)

        # Symmetry detection
        symmetries = self._detect_symmetries(grid)

        # Edge patterns
        edge_analysis = self._analyze_edge_patterns(grid)

        # Global structure
        structure_analysis = self._analyze_global_structure(grid)

        return {
            'dimensions': dimensions,
            'total_cells': total_cells,
            'color_counts': color_counts,
            'density': density,
            'symmetries': symmetries,
            'edge_analysis': edge_analysis,
            'structure': structure_analysis,
            'aspect_ratio': width / height if height > 0 else 0,
            'unique_colors': len(color_counts)
        }

    def _analyze_regional_patterns(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze regional-scale patterns (quadrants/sections)"""
        height, width = len(grid), len(grid[0])
        mid_h, mid_w = height // 2, width // 2

        # Create regions (quadrants)
        regions = {
            'top_left': [row[:mid_w] for row in grid[:mid_h]],
            'top_right': [row[mid_w:] for row in grid[:mid_h]],
            'bottom_left': [row[:mid_w] for row in grid[mid_h:]],
            'bottom_right': [row[mid_w:] for row in grid[mid_h:]]
        }

        # Analyze each region
        region_analysis = {}
        for region_name, subgrid in regions.items():
            if subgrid and subgrid[0]:  # Check if region is non-empty
                region_analysis[region_name] = {
                    'color_counts': self._count_colors(subgrid),
                    'density': self._calculate_density(subgrid),
                    'dominant_color': self._find_dominant_color(subgrid),
                    'pattern_complexity': self._assess_pattern_complexity(subgrid)
                }

        # Cross-region analysis
        region_similarities = self._analyze_region_similarities(regions)
        region_contrasts = self._analyze_region_contrasts(region_analysis)

        return {
            'regions': region_analysis,
            'region_similarities': region_similarities,
            'region_contrasts': region_contrasts,
            'quadrant_balance': self._calculate_quadrant_balance(region_analysis)
        }

    def _analyze_local_patterns(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze local-scale patterns (3x3 neighborhoods)"""
        height, width = len(grid), len(grid[0])
        pattern_size = self.local_pattern_size

        if height < pattern_size or width < pattern_size:
            return {'patterns': [], 'pattern_count': 0, 'pattern_summary': {}}

        patterns = []
        pattern_frequency = {}

        # Sample local patterns (limit to reasonable number for performance)
        max_patterns = min(20, (height - pattern_size + 1) * (width - pattern_size + 1))
        step = max(1, ((height - pattern_size + 1) * (width - pattern_size + 1)) // max_patterns)

        pattern_count = 0
        for i in range(0, height - pattern_size + 1, step):
            for j in range(0, width - pattern_size + 1, step):
                if pattern_count >= max_patterns:
                    break

                # Extract local pattern
                pattern = []
                for di in range(pattern_size):
                    for dj in range(pattern_size):
                        pattern.append(grid[i + di][j + dj])

                pattern_tuple = tuple(pattern)
                pattern_frequency[pattern_tuple] = pattern_frequency.get(pattern_tuple, 0) + 1

                patterns.append({
                    'position': {'row': i, 'col': j},
                    'pattern': pattern,
                    'center_value': grid[i + pattern_size // 2][j + pattern_size // 2],
                    'pattern_hash': hash(pattern_tuple)
                })

                pattern_count += 1

            if pattern_count >= max_patterns:
                break

        # Pattern summary statistics
        pattern_summary = {
            'unique_patterns': len(pattern_frequency),
            'most_common_pattern': max(pattern_frequency.items(), key=lambda x: x[1])[0] if pattern_frequency else None,
            'pattern_diversity': len(pattern_frequency) / max(1, len(patterns)),
            'repetition_rate': max(pattern_frequency.values()) / max(1, len(patterns)) if pattern_frequency else 0
        }

        return {
            'patterns': patterns,
            'pattern_count': len(patterns),
            'pattern_frequency': dict(list(pattern_frequency.items())[:10]),  # Limit for size
            'pattern_summary': pattern_summary
        }

    def _detect_symmetries(self, grid: List[List[int]]) -> List[str]:
        """Detect various types of symmetries"""
        symmetries = []

        # Horizontal symmetry (mirror across horizontal axis)
        if self._check_horizontal_symmetry(grid):
            symmetries.append('horizontal')

        # Vertical symmetry (mirror across vertical axis)
        if self._check_vertical_symmetry(grid):
            symmetries.append('vertical')

        # Rotational symmetry (180 degrees)
        if self._check_rotational_symmetry(grid):
            symmetries.append('rotational_180')

        # Diagonal symmetries
        if self._check_diagonal_symmetry(grid, 'main'):
            symmetries.append('diagonal_main')

        if self._check_diagonal_symmetry(grid, 'anti'):
            symmetries.append('diagonal_anti')

        return symmetries

    def _check_horizontal_symmetry(self, grid: List[List[int]]) -> bool:
        """Check for horizontal symmetry"""
        return grid == grid[::-1]

    def _check_vertical_symmetry(self, grid: List[List[int]]) -> bool:
        """Check for vertical symmetry"""
        return all(row == row[::-1] for row in grid)

    def _check_rotational_symmetry(self, grid: List[List[int]]) -> bool:
        """Check for 180-degree rotational symmetry"""
        height, width = len(grid), len(grid[0])

        for i in range(height):
            for j in range(width):
                if grid[i][j] != grid[height - 1 - i][width - 1 - j]:
                    return False
        return True

    def _check_diagonal_symmetry(self, grid: List[List[int]], diagonal_type: str) -> bool:
        """Check for diagonal symmetry"""
        height, width = len(grid), len(grid[0])

        if height != width:  # Diagonal symmetry only makes sense for square grids
            return False

        if diagonal_type == 'main':
            # Main diagonal (top-left to bottom-right)
            for i in range(height):
                for j in range(width):
                    if grid[i][j] != grid[j][i]:
                        return False
        elif diagonal_type == 'anti':
            # Anti-diagonal (top-right to bottom-left)
            for i in range(height):
                for j in range(width):
                    if grid[i][j] != grid[width - 1 - j][height - 1 - i]:
                        return False

        return True

    def _analyze_edge_patterns(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze edge and boundary patterns"""
        height, width = len(grid), len(grid[0])

        # Edge values
        top_edge = grid[0]
        bottom_edge = grid[-1]
        left_edge = [row[0] for row in grid]
        right_edge = [row[-1] for row in grid]

        # Corner values
        corners = {
            'top_left': grid[0][0],
            'top_right': grid[0][-1],
            'bottom_left': grid[-1][0],
            'bottom_right': grid[-1][-1]
        }

        # Edge uniformity
        edge_uniformity = {
            'top': len(set(top_edge)) == 1,
            'bottom': len(set(bottom_edge)) == 1,
            'left': len(set(left_edge)) == 1,
            'right': len(set(right_edge)) == 1
        }

        return {
            'corners': corners,
            'edge_uniformity': edge_uniformity,
            'corner_symmetry': len(set(corners.values())) == 1,
            'border_complexity': self._calculate_border_complexity(grid)
        }

    def _calculate_complexity_score(self, global_analysis: Dict[str, Any],
                                   regional_analysis: Dict[str, Any],
                                   local_analysis: Dict[str, Any]) -> float:
        """Calculate overall pattern complexity score"""
        # Global complexity
        global_complexity = min(1.0, global_analysis.get('unique_colors', 1) / 8.0)

        # Regional complexity
        regional_complexity = 0.0
        if regional_analysis:
            regions = regional_analysis.get('regions', {})
            if regions:
                regional_complexity = np.mean([
                    region.get('pattern_complexity', 0.0) for region in regions.values()
                ])

        # Local complexity
        local_complexity = 0.0
        if local_analysis.get('pattern_summary'):
            local_complexity = local_analysis['pattern_summary'].get('pattern_diversity', 0.0)

        # Weighted combination
        weights = [0.4, 0.3, 0.3]  # global, regional, local
        complexities = [global_complexity, regional_complexity, local_complexity]

        return sum(w * c for w, c in zip(weights, complexities))

    def _calculate_analysis_confidence(self, global_analysis: Dict[str, Any],
                                     regional_analysis: Dict[str, Any],
                                     local_analysis: Dict[str, Any]) -> float:
        """Calculate confidence in the analysis"""
        # Base confidence from data availability
        base_confidence = 0.5

        # Boost for available analysis types
        if global_analysis:
            base_confidence += 0.2
        if regional_analysis:
            base_confidence += 0.2
        if local_analysis.get('patterns'):
            base_confidence += 0.1

        # Additional confidence from data quality
        total_cells = global_analysis.get('total_cells', 0)
        if total_cells > 25:
            base_confidence += 0.1
        if total_cells > 100:
            base_confidence += 0.1

        return min(1.0, base_confidence)

    # Helper methods
    def _count_colors(self, grid: List[List[int]]) -> Dict[int, int]:
        """Count color frequencies"""
        counts = {}
        for row in grid:
            for cell in row:
                counts[cell] = counts.get(cell, 0) + 1
        return counts

    def _calculate_density(self, grid: List[List[int]]) -> float:
        """Calculate non-zero density"""
        # Safe emptiness check (avoids NumPy truth value ambiguity)
        if grid is None or (hasattr(grid, 'size') and grid.size == 0) or (isinstance(grid, list) and not grid):
            return 0.0
        total_cells = sum(len(row) for row in grid)
        non_zero_cells = sum(1 for row in grid for cell in row if cell != 0)
        return non_zero_cells / total_cells if total_cells > 0 else 0.0

    def _find_dominant_color(self, grid: List[List[int]]) -> int:
        """Find the most frequent color in grid"""
        color_counts = self._count_colors(grid)
        return max(color_counts.items(), key=lambda x: x[1])[0] if color_counts else 0

    def _assess_pattern_complexity(self, grid: List[List[int]]) -> float:
        """Assess pattern complexity for a grid section"""
        # Safe emptiness check (avoids NumPy truth value ambiguity)
        if grid is None or (hasattr(grid, 'size') and grid.size == 0) or (isinstance(grid, list) and not grid):
            return 0.0

        unique_colors = len(set(cell for row in grid for cell in row))
        total_cells = sum(len(row) for row in grid)

        return min(1.0, unique_colors / max(1, total_cells * 0.3))

    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis for invalid input"""
        return {
            'global': {},
            'regional': {},
            'local': {'patterns': [], 'pattern_count': 0},
            'scales_analyzed': [],
            'complexity_score': 0.0,
            'transformation_readiness': 0.0,
            'pattern_diversity': 0.0,
            'analysis_confidence': 0.0,
            'global_coherence': 0.0
        }

    def _get_scales_analyzed(self, regional_analysis: Dict[str, Any]) -> List[str]:
        """Get list of scales that were analyzed"""
        scales = ['global', 'local']
        if regional_analysis:
            scales.insert(1, 'regional')
        return scales

    def _assess_transformation_readiness(self, global_analysis: Dict[str, Any],
                                       regional_analysis: Dict[str, Any],
                                       local_analysis: Dict[str, Any]) -> float:
        """Assess how ready the pattern is for transformation"""
        readiness_factors = []

        # Global factors
        if global_analysis:
            symmetries = len(global_analysis.get('symmetries', []))
            readiness_factors.append(min(1.0, symmetries / 3.0))  # More symmetries = higher readiness

        # Regional factors
        if regional_analysis:
            balance = regional_analysis.get('quadrant_balance', 0.5)
            readiness_factors.append(balance)

        # Local factors
        if local_analysis.get('pattern_summary'):
            diversity = local_analysis['pattern_summary'].get('pattern_diversity', 0.0)
            readiness_factors.append(1.0 - diversity)  # Less diversity = higher readiness

        return np.mean(readiness_factors) if readiness_factors else 0.5

    def _calculate_pattern_diversity(self, global_analysis: Dict[str, Any],
                                   regional_analysis: Dict[str, Any],
                                   local_analysis: Dict[str, Any]) -> float:
        """Calculate overall pattern diversity"""
        diversity_factors = []

        # Global diversity
        if global_analysis:
            color_diversity = min(1.0, global_analysis.get('unique_colors', 1) / 8.0)
            diversity_factors.append(color_diversity)

        # Local diversity
        if local_analysis.get('pattern_summary'):
            pattern_diversity = local_analysis['pattern_summary'].get('pattern_diversity', 0.0)
            diversity_factors.append(pattern_diversity)

        return np.mean(diversity_factors) if diversity_factors else 0.0

    def _calculate_global_coherence(self, global_analysis: Dict[str, Any],
                                  complexity_score: float,
                                  pattern_diversity: float) -> float:
        """Calculate global coherence score"""
        if not global_analysis:
            return 0.0

        # Base coherence from density and structure
        density = global_analysis.get('density', 0.0)
        symmetries = len(global_analysis.get('symmetries', []))

        structure_coherence = (density * 0.4) + (min(1.0, symmetries / 3.0) * 0.3)

        # Complexity and diversity contributions
        complexity_contribution = complexity_score * 0.2
        diversity_contribution = pattern_diversity * 0.1

        return min(1.0, structure_coherence + complexity_contribution + diversity_contribution)

    def _analyze_global_structure(self, grid: List[List[int]]) -> Dict[str, Any]:
        """Analyze global structural properties"""
        # This is a placeholder for more sophisticated structural analysis
        return {
            'filled_ratio': self._calculate_density(grid),
            'center_prominence': self._check_center_prominence(grid),
            'edge_importance': self._check_edge_importance(grid)
        }

    def _check_center_prominence(self, grid: List[List[int]]) -> float:
        """Check if center region is more prominent"""
        height, width = len(grid), len(grid[0])
        if height < 3 or width < 3:
            return 0.0

        # Extract center region
        center_h_start, center_h_end = height // 3, 2 * height // 3
        center_w_start, center_w_end = width // 3, 2 * width // 3

        center_density = 0
        center_cells = 0

        for i in range(center_h_start, center_h_end):
            for j in range(center_w_start, center_w_end):
                if grid[i][j] != 0:
                    center_density += 1
                center_cells += 1

        return center_density / max(1, center_cells)

    def _check_edge_importance(self, grid: List[List[int]]) -> float:
        """Check if edges are important in the pattern"""
        height, width = len(grid), len(grid[0])
        edge_density = 0
        edge_cells = 0

        # Count edge cells
        for i in range(height):
            for j in range(width):
                if i == 0 or i == height - 1 or j == 0 or j == width - 1:
                    if grid[i][j] != 0:
                        edge_density += 1
                    edge_cells += 1

        return edge_density / max(1, edge_cells)

    def _analyze_region_similarities(self, regions: Dict[str, List[List[int]]]) -> Dict[str, float]:
        """Analyze similarities between regions"""
        similarities = {}
        region_names = list(regions.keys())

        for i in range(len(region_names)):
            for j in range(i + 1, len(region_names)):
                name1, name2 = region_names[i], region_names[j]
                similarity = self._calculate_region_similarity(regions[name1], regions[name2])
                similarities[f"{name1}_{name2}"] = similarity

        return similarities

    def _calculate_region_similarity(self, region1: List[List[int]], region2: List[List[int]]) -> float:
        """Calculate similarity between two regions"""
        if not region1 or not region2:
            return 0.0

        # Simple similarity based on color distribution
        colors1 = set(cell for row in region1 for cell in row)
        colors2 = set(cell for row in region2 for cell in row)

        if not colors1 and not colors2:
            return 1.0
        if not colors1 or not colors2:
            return 0.0

        intersection = len(colors1 & colors2)
        union = len(colors1 | colors2)

        return intersection / union if union > 0 else 0.0

    def _analyze_region_contrasts(self, region_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze contrasts between regions"""
        if not region_analysis:
            return {}

        # Calculate density contrasts
        densities = [region.get('density', 0.0) for region in region_analysis.values()]
        density_variance = np.var(densities) if densities else 0.0

        # Calculate complexity contrasts
        complexities = [region.get('pattern_complexity', 0.0) for region in region_analysis.values()]
        complexity_variance = np.var(complexities) if complexities else 0.0

        return {
            'density_contrast': density_variance,
            'complexity_contrast': complexity_variance,
            'overall_contrast': (density_variance + complexity_variance) / 2
        }

    def _calculate_quadrant_balance(self, region_analysis: Dict[str, Any]) -> float:
        """Calculate balance between quadrants"""
        if not region_analysis:
            return 0.5

        densities = [region.get('density', 0.0) for region in region_analysis.values()]
        if not densities:
            return 0.5

        # Calculate how balanced the densities are (lower variance = higher balance)
        variance = np.var(densities)
        balance = 1.0 / (1.0 + variance * 4)  # Scale variance to 0-1 range

        return balance

    def _calculate_border_complexity(self, grid: List[List[int]]) -> float:
        """Calculate complexity of the border"""
        height, width = len(grid), len(grid[0])
        if height < 2 or width < 2:
            return 0.0

        # Collect border values
        border_values = []

        # Top and bottom rows
        border_values.extend(grid[0])
        border_values.extend(grid[-1])

        # Left and right columns (excluding corners already counted)
        for i in range(1, height - 1):
            border_values.extend([grid[i][0], grid[i][-1]])

        # Calculate complexity as number of unique values normalized
        unique_border_values = len(set(border_values))
        max_possible_unique = min(len(border_values), 10)  # Cap at 10 for normalization

        return unique_border_values / max(1, max_possible_unique)