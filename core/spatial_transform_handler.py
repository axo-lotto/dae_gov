#!/usr/bin/env python3
"""
Spatial Transform Handler - Robust Shape Transformations
=========================================================

Handles shape mismatches and spatial transformations without broadcast errors.
Learns spatial patterns like tiling, scaling, and replication.

Created: November 3, 2025
"""

import numpy as np
from typing import Tuple, Dict, Optional, List, Any


class SpatialTransformHandler:
    """
    Handle spatial transformations robustly.

    Key capabilities:
    1. Shape mismatch resolution
    2. Tile/repeat pattern detection
    3. Scale factor learning
    4. Spatial relationship preservation
    """

    def __init__(self):
        """Initialize spatial transform handler."""
        self.learned_transforms = {}
        self.spatial_patterns = {}

    def safe_shape_transform(
        self,
        source: np.ndarray,
        target_shape: Tuple[int, int],
        method: str = 'auto'
    ) -> np.ndarray:
        """
        Safely transform array to target shape without broadcast errors.

        Methods:
        - 'tile': Repeat pattern to fill larger shape
        - 'scale': Resize using interpolation
        - 'pad': Add padding to match shape
        - 'crop': Crop to smaller shape
        - 'auto': Detect best method
        """

        source_shape = source.shape

        # No transform needed
        if source_shape == target_shape:
            return source.copy()

        # Auto-detect best method
        if method == 'auto':
            method = self._detect_transform_method(source_shape, target_shape)

        if method == 'tile':
            return self._tile_transform(source, target_shape)
        elif method == 'scale':
            return self._scale_transform(source, target_shape)
        elif method == 'pad':
            return self._pad_transform(source, target_shape)
        elif method == 'crop':
            return self._crop_transform(source, target_shape)
        else:
            # Fallback to safe padding/cropping
            return self._safe_resize(source, target_shape)

    def _detect_transform_method(
        self,
        source_shape: Tuple[int, int],
        target_shape: Tuple[int, int]
    ) -> str:
        """Detect the best transformation method."""

        s_h, s_w = source_shape
        t_h, t_w = target_shape

        # Check if target is exact multiple of source (tiling)
        if t_h % s_h == 0 and t_w % s_w == 0:
            return 'tile'

        # Check if source is exact multiple of target (downscaling)
        if s_h % t_h == 0 and s_w % t_w == 0:
            return 'scale'

        # If target is larger, pad
        if t_h >= s_h and t_w >= s_w:
            return 'pad'

        # If target is smaller, crop
        if t_h <= s_h and t_w <= s_w:
            return 'crop'

        # Mixed case - use scaling
        return 'scale'

    def _tile_transform(
        self,
        source: np.ndarray,
        target_shape: Tuple[int, int]
    ) -> np.ndarray:
        """Tile source pattern to fill target shape."""

        s_h, s_w = source.shape
        t_h, t_w = target_shape

        # Calculate repetitions needed
        reps_h = (t_h + s_h - 1) // s_h
        reps_w = (t_w + s_w - 1) // s_w

        # Tile the pattern
        tiled = np.tile(source, (reps_h, reps_w))

        # Crop to exact target shape
        return tiled[:t_h, :t_w]

    def _scale_transform(
        self,
        source: np.ndarray,
        target_shape: Tuple[int, int]
    ) -> np.ndarray:
        """Scale source to target shape using nearest neighbor."""

        from scipy.ndimage import zoom

        s_h, s_w = source.shape
        t_h, t_w = target_shape

        # Calculate zoom factors
        zoom_h = t_h / s_h
        zoom_w = t_w / s_w

        # Apply zoom with nearest neighbor (order=0)
        scaled = zoom(source, (zoom_h, zoom_w), order=0)

        # Ensure exact shape
        if scaled.shape != target_shape:
            scaled = self._safe_resize(scaled, target_shape)

        return scaled

    def _pad_transform(
        self,
        source: np.ndarray,
        target_shape: Tuple[int, int]
    ) -> np.ndarray:
        """Pad source to target shape."""

        s_h, s_w = source.shape
        t_h, t_w = target_shape

        # Create padded array (fill with 0)
        padded = np.zeros(target_shape, dtype=source.dtype)

        # Center the source in target
        start_h = (t_h - s_h) // 2
        start_w = (t_w - s_w) // 2

        # Place source in padded array
        padded[start_h:start_h+s_h, start_w:start_w+s_w] = source

        return padded

    def _crop_transform(
        self,
        source: np.ndarray,
        target_shape: Tuple[int, int]
    ) -> np.ndarray:
        """Crop source to target shape."""

        s_h, s_w = source.shape
        t_h, t_w = target_shape

        # Center crop
        start_h = (s_h - t_h) // 2
        start_w = (s_w - t_w) // 2

        # Extract crop
        cropped = source[start_h:start_h+t_h, start_w:start_w+t_w]

        return cropped

    def _safe_resize(
        self,
        source: np.ndarray,
        target_shape: Tuple[int, int]
    ) -> np.ndarray:
        """Safe resize that always works without broadcast errors."""

        # Create target array
        result = np.zeros(target_shape, dtype=source.dtype)

        # Calculate overlap region
        min_h = min(source.shape[0], target_shape[0])
        min_w = min(source.shape[1], target_shape[1])

        # Copy overlap
        result[:min_h, :min_w] = source[:min_h, :min_w]

        return result

    def learn_spatial_pattern(
        self,
        input_grid: np.ndarray,
        output_grid: np.ndarray,
        task_id: str
    ) -> Dict[str, Any]:
        """
        Learn spatial transformation pattern from input/output pair.

        Returns detected spatial patterns and transformations.
        """

        patterns = {
            'shape_transform': {
                'from': input_grid.shape,
                'to': output_grid.shape,
                'method': self._detect_transform_method(input_grid.shape, output_grid.shape)
            }
        }

        # Detect tiling pattern
        if self._is_tiling_pattern(input_grid, output_grid):
            tile_info = self._extract_tile_pattern(input_grid, output_grid)
            patterns['tile_pattern'] = tile_info

        # Detect scaling pattern
        scale_factors = (
            output_grid.shape[0] / input_grid.shape[0],
            output_grid.shape[1] / input_grid.shape[1]
        )
        patterns['scale_factors'] = scale_factors

        # Store learned pattern
        self.spatial_patterns[task_id] = patterns

        return patterns

    def _is_tiling_pattern(
        self,
        input_grid: np.ndarray,
        output_grid: np.ndarray
    ) -> bool:
        """Check if output is a tiled version of input."""

        if output_grid.shape[0] < input_grid.shape[0] or \
           output_grid.shape[1] < input_grid.shape[1]:
            return False

        # Check if input pattern repeats in output
        h, w = input_grid.shape

        # Check first tile
        if np.array_equal(output_grid[:h, :w], input_grid):
            return True

        return False

    def _extract_tile_pattern(
        self,
        input_grid: np.ndarray,
        output_grid: np.ndarray
    ) -> Dict[str, Any]:
        """Extract tiling pattern information."""

        h, w = input_grid.shape
        oh, ow = output_grid.shape

        return {
            'tile_size': (h, w),
            'repetitions': (oh // h, ow // w),
            'pattern': input_grid.copy()
        }

    def apply_learned_transform(
        self,
        input_grid: np.ndarray,
        task_id: str,
        target_shape: Optional[Tuple[int, int]] = None
    ) -> np.ndarray:
        """Apply previously learned spatial transformation."""

        if task_id not in self.spatial_patterns:
            # No learned pattern, use safe resize
            if target_shape:
                return self.safe_shape_transform(input_grid, target_shape)
            return input_grid.copy()

        pattern = self.spatial_patterns[task_id]

        # Apply shape transform
        if target_shape is None and 'shape_transform' in pattern:
            target_shape = pattern['shape_transform']['to']

        if target_shape:
            method = pattern['shape_transform'].get('method', 'auto')
            return self.safe_shape_transform(input_grid, target_shape, method)

        return input_grid.copy()