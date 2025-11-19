"""
Atomic JSON Writer - Prevents corruption during file writes
=============================================================

Implements atomic write operations for JSON files to prevent corruption
from interrupted writes (crashes, KeyboardInterrupt, etc.).

Date: November 18, 2025
Author: Claude Code + DAE Team
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict


def atomic_write_json(file_path: str, data: Dict[str, Any], indent: int = 2):
    """
    Atomically write JSON data to a file.

    Uses a temp file + atomic rename to ensure the file is never left in a
    corrupted state. If the write fails, the original file remains untouched.

    Args:
        file_path: Path to the target JSON file
        data: Dictionary to serialize as JSON
        indent: JSON indentation (default: 2)

    Raises:
        OSError: If write or rename fails
        TypeError: If data is not JSON-serializable
    """
    file_path = Path(file_path)

    # Ensure parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create temp file in same directory (ensures same filesystem for atomic rename)
    temp_fd, temp_path = tempfile.mkstemp(
        dir=file_path.parent,
        prefix=f".{file_path.name}.",
        suffix=".tmp"
    )

    try:
        # Write JSON to temp file
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.flush()  # Ensure data is written to disk
            os.fsync(f.fileno())  # Force filesystem sync

        # Atomic rename (POSIX guarantees atomicity)
        # On Windows, this may fail if target exists - delete first
        if os.name == 'nt' and file_path.exists():
            os.remove(file_path)

        os.rename(temp_path, file_path)

    except Exception:
        # Clean up temp file if something went wrong
        try:
            os.remove(temp_path)
        except OSError:
            pass
        raise


def atomic_update_json(file_path: str, update_func, default_data: Dict = None, indent: int = 2):
    """
    Atomically update a JSON file using a function.

    Reads existing data, applies update function, writes atomically.
    If file doesn't exist, uses default_data.

    Args:
        file_path: Path to the JSON file
        update_func: Function that takes current data dict and returns updated dict
        default_data: Default data if file doesn't exist (default: empty dict)
        indent: JSON indentation (default: 2)

    Returns:
        Updated data dictionary

    Example:
        def add_session(data):
            data['sessions'].append({'id': 'new_session'})
            return data

        atomic_update_json('user_state.json', add_session, default_data={'sessions': []})
    """
    file_path = Path(file_path)

    # Read current data
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except (json.JSONDecodeError, OSError):
            # If corrupted, use default
            current_data = default_data if default_data is not None else {}
    else:
        current_data = default_data if default_data is not None else {}

    # Apply update function
    updated_data = update_func(current_data)

    # Write atomically
    atomic_write_json(file_path, updated_data, indent=indent)

    return updated_data


# Example usage
if __name__ == "__main__":
    # Test atomic write
    test_data = {
        "user_id": "test_user",
        "sessions": [{"id": "session_1", "turns": 5}],
        "metadata": {"created": "2025-11-18"}
    }

    atomic_write_json("/tmp/test_atomic.json", test_data)
    print("✅ Atomic write successful")

    # Test atomic update
    def add_session(data):
        data['sessions'].append({"id": "session_2", "turns": 3})
        return data

    updated = atomic_update_json("/tmp/test_atomic.json", add_session)
    print(f"✅ Atomic update successful: {len(updated['sessions'])} sessions")
