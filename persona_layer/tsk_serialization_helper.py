"""
TSK Serialization Helper
Created: November 17, 2025

Handles recursive conversion of nested TSK dataclasses to JSON-serializable dicts.
Fixes critical bug where tsk_record contains nested TransductiveSummaryKernel objects.
"""

from typing import Any, Dict, List
import numpy as np


def tsk_to_dict_recursive(obj: Any) -> Any:
    """
    Recursively convert TSK objects and numpy arrays to JSON-serializable types.

    This handles:
    - TransductiveSummaryKernel dataclasses (has to_dict() method)
    - WordOccasion dataclasses (has to_dict() method) ← ADDED NOV 19, 2025
    - Nested dicts containing TSK/WordOccasion objects
    - Lists containing TSK/WordOccasion objects
    - Numpy arrays (convert to lists)
    - Numpy scalar types (convert to Python types)

    Args:
        obj: Object to convert (can be TSK, WordOccasion, dict, list, numpy, or primitive)

    Returns:
        JSON-serializable version of obj
    """
    # Handle None
    if obj is None:
        return None

    # Handle dataclasses with to_dict() method
    # This includes: TransductiveSummaryKernel, WordOccasion
    if hasattr(obj, 'to_dict') and hasattr(obj, '__class__'):
        class_name = str(obj.__class__)
        # Check for known serializable dataclasses
        if any(name in class_name for name in ['TransductiveSummaryKernel', 'WordOccasion']):
            # Convert dataclass to dict, then recursively process
            obj_dict = obj.to_dict()
            return tsk_to_dict_recursive(obj_dict)

    # Handle dict
    if isinstance(obj, dict):
        return {k: tsk_to_dict_recursive(v) for k, v in obj.items()}

    # Handle list/tuple
    if isinstance(obj, (list, tuple)):
        return [tsk_to_dict_recursive(item) for item in obj]

    # Handle numpy arrays
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    # Handle numpy scalar types
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()

    # Handle numpy bool
    if isinstance(obj, np.bool_):
        return bool(obj)

    # Primitives (str, int, float, bool) - return as-is
    return obj


def validate_json_serializable(obj: Any, path: str = 'root') -> List[str]:
    """
    Validate that an object is JSON serializable.
    Returns list of paths where non-serializable objects were found.

    Args:
        obj: Object to validate
        path: Current path (for error reporting)

    Returns:
        List of error paths (empty if fully serializable)
    """
    errors = []

    # Check for common non-serializable types
    if hasattr(obj, '__class__'):
        class_name = obj.__class__.__name__
        # Flag known non-serializable dataclasses (should have been converted by tsk_to_dict_recursive)
        if any(name in class_name for name in ['TransductiveSummaryKernel', 'WordOccasion']):
            errors.append(f"{path}: {class_name} (should be dict)")

    # Recursively check dicts
    if isinstance(obj, dict):
        for k, v in obj.items():
            errors.extend(validate_json_serializable(v, f"{path}.{k}"))

    # Recursively check lists
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            errors.extend(validate_json_serializable(item, f"{path}[{i}]"))

    # Check numpy types
    elif isinstance(obj, np.ndarray):
        errors.append(f"{path}: numpy.ndarray (shape {obj.shape})")
    elif isinstance(obj, (np.integer, np.floating, np.bool_)):
        errors.append(f"{path}: {type(obj).__name__}")

    return errors
