#!/usr/bin/env python3
"""
TSK Log Memory System - Persistent Learning Through Logs
========================================================

Store TSK records as logs for reliable pattern accumulation.
Prevents corruption and enables cross-task learning.

Created: November 3, 2025
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np


class TSKLogMemory:
    """
    Store and recall TSK records as logs.

    Each task gets its own log file for reliability.
    Patterns are extracted and indexed for fast recall.
    """

    def __init__(self, log_dir: str = "data/logs", min_recall_threshold: float = 0.9):
        """Initialize TSK log memory system."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Configurable recall threshold (default 90%, can be set to 99%)
        self.min_recall_threshold = min_recall_threshold

        # In-memory index for fast lookup
        self.pattern_index = {}  # pattern_signature -> [(task_id, confidence), ...]
        self.task_index = {}     # task_id -> log_file_path
        self.value_mappings = {}  # "from_X_to_Y" -> [(task_id, occurrences), ...]

        # Load existing logs
        self._load_existing_logs()

        print(f"📝 TSKLogMemory initialized")
        print(f"   Log directory: {self.log_dir}")
        print(f"   Existing tasks: {len(self.task_index)}")
        print(f"   Indexed patterns: {len(self.pattern_index)}")
        print(f"   Min recall threshold: {self.min_recall_threshold:.0%}")

    def store_tsk(self, task_id: str, tsk_record: Dict, mode: str = 'input') -> str:
        """
        Store TSK record as log file.

        Returns: Path to log file
        """
        # Create task directory
        task_dir = self.log_dir / task_id
        task_dir.mkdir(exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = task_dir / f"{mode}_{timestamp}.json"

        # Store TSK record
        with open(log_file, 'w') as f:
            json.dump(tsk_record, f, indent=2, default=str)

        # Update task index
        self.task_index[task_id] = str(task_dir)

        # Extract and index patterns
        self._extract_patterns_from_tsk(task_id, tsk_record)

        print(f"   💾 Stored TSK: {log_file.name}")
        return str(log_file)

    def store_learning_result(
        self,
        task_id: str,
        patterns: Dict[str, Any],
        accuracy: float,
        iterations: int,
        min_accuracy_threshold: float = 0.9
    ):
        """Store learning results for a task - ONLY if accuracy >= 90%."""

        # CRITICAL: Only store patterns from successful transformations
        if accuracy < min_accuracy_threshold:
            print(f"   ⚠️ NOT storing patterns for {task_id} - accuracy {accuracy:.1%} < {min_accuracy_threshold:.0%}%")
            return

        # Create learning log
        task_dir = Path(self.task_index.get(task_id, self.log_dir / task_id))
        task_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        learning_file = task_dir / f"learning_{timestamp}.json"

        learning_data = {
            'task_id': task_id,
            'accuracy': accuracy,
            'iterations': iterations,
            'patterns': patterns,
            'timestamp': timestamp
        }

        with open(learning_file, 'w') as f:
            json.dump(learning_data, f, indent=2)

        # Index patterns for cross-task learning (only for successful patterns)
        for pattern_key, pattern_data in patterns.items():
            if pattern_key.startswith('value_map_'):
                # Extract value mapping
                parts = pattern_key.split('_')
                if len(parts) >= 4:
                    from_val = parts[2]
                    to_val = parts[4] if len(parts) > 4 else parts[3]
                    mapping_key = f"from_{from_val}_to_{to_val}"

                    if mapping_key not in self.value_mappings:
                        self.value_mappings[mapping_key] = []

                    # Store with confidence
                    self.value_mappings[mapping_key].append((task_id, accuracy))

            elif pattern_key.startswith('_'):
                # Skip metadata patterns
                continue
            else:
                # General pattern
                if pattern_key not in self.pattern_index:
                    self.pattern_index[pattern_key] = []
                self.pattern_index[pattern_key].append((task_id, accuracy))

        print(f"   📊 Stored learning: {task_id} - {accuracy:.1%} accuracy")
        print(f"      Patterns: {len(patterns)}")
        print(f"      Value mappings: {len([k for k in patterns if k.startswith('value_map_')])}")

    def recall_patterns(self, task_id: str, task_type: str = None) -> Dict:
        """
        Recall patterns for a task.

        Looks for:
        1. Task-specific patterns
        2. Similar task patterns (same type)
        3. High-confidence cross-task patterns
        """
        recalled_patterns = {}

        # Load task-specific patterns
        task_dir = Path(self.task_index.get(task_id, self.log_dir / task_id))
        if task_dir.exists():
            # Find latest learning file
            learning_files = list(task_dir.glob("learning_*.json"))
            if learning_files:
                latest = max(learning_files, key=lambda f: f.stat().st_mtime)
                with open(latest, 'r') as f:
                    data = json.load(f)
                    recalled_patterns.update(data.get('patterns', {}))
                    print(f"   🔍 Recalled {len(recalled_patterns)} task-specific patterns")

        # Add high-confidence cross-task patterns
        cross_task_patterns = self._find_cross_task_patterns(task_type)
        recalled_patterns.update(cross_task_patterns)

        return recalled_patterns

    def recall_value_mappings(self, confidence_threshold: Optional[float] = None) -> Dict[str, float]:
        """
        Recall high-confidence value mappings across all tasks.

        Uses instance min_recall_threshold if not specified (default 90%, can be 99%).

        Returns: Dict of mapping -> average_confidence
        """
        # Use instance threshold if not specified
        if confidence_threshold is None:
            confidence_threshold = self.min_recall_threshold

        mappings = {}

        for mapping_key, task_list in self.value_mappings.items():
            # Only use mappings from successful tasks (>= threshold accuracy)
            high_accuracy_mappings = [
                (task, conf) for task, conf in task_list
                if conf >= confidence_threshold
            ]

            if high_accuracy_mappings:
                confidences = [conf for _, conf in high_accuracy_mappings]
                avg_confidence = np.mean(confidences) if confidences else 0

                if avg_confidence >= confidence_threshold:
                    mappings[mapping_key] = avg_confidence
                    print(f"      ✅ High-confidence mapping recalled: {mapping_key} (conf={avg_confidence:.2f})")

        return mappings

    def _extract_patterns_from_tsk(self, task_id: str, tsk: Dict):
        """Extract and index patterns from TSK record."""
        # Extract value mappings from TSK
        if 'value_mappings' in tsk:
            for mapping in tsk['value_mappings']:
                if 'from' in mapping and 'to' in mapping:
                    key = f"from_{mapping['from']}_to_{mapping['to']}"
                    if key not in self.value_mappings:
                        self.value_mappings[key] = []
                    confidence = mapping.get('confidence', 0.5)
                    self.value_mappings[key].append((task_id, confidence))

        # Extract organ coherences
        if 'organ_coherences' in tsk:
            for organ, coherence in tsk['organ_coherences'].items():
                pattern_key = f"organ_{organ}_active"
                if pattern_key not in self.pattern_index:
                    self.pattern_index[pattern_key] = []
                # Use coherence as confidence
                conf = coherence if isinstance(coherence, (int, float)) else 0.5
                self.pattern_index[pattern_key].append((task_id, conf))

    def _find_cross_task_patterns(self, task_type: Optional[str]) -> Dict:
        """Find patterns from similar tasks."""
        cross_patterns = {}

        # Find patterns from tasks with high confidence
        for pattern_key, task_list in self.pattern_index.items():
            # Get high-confidence instances
            high_conf = [(t, c) for t, c in task_list if c >= 0.8]

            if len(high_conf) >= 2:  # Pattern appears in multiple successful tasks
                # Add as cross-task pattern
                avg_conf = np.mean([c for _, c in high_conf])
                cross_patterns[f"cross_{pattern_key}"] = {
                    'confidence': avg_conf,
                    'source_tasks': [t for t, _ in high_conf],
                    'type': 'cross_task'
                }

        if cross_patterns:
            print(f"   🔗 Found {len(cross_patterns)} cross-task patterns")

        return cross_patterns

    def _load_existing_logs(self):
        """Load and index existing log files."""
        if not self.log_dir.exists():
            return

        # Scan for task directories
        for task_dir in self.log_dir.iterdir():
            if task_dir.is_dir():
                task_id = task_dir.name
                self.task_index[task_id] = str(task_dir)

                # Load learning files
                for learning_file in task_dir.glob("learning_*.json"):
                    try:
                        with open(learning_file, 'r') as f:
                            data = json.load(f)

                            # Index patterns
                            patterns = data.get('patterns', {})
                            accuracy = data.get('accuracy', 0)

                            for pattern_key in patterns:
                                if pattern_key.startswith('value_map_'):
                                    # Extract value mapping
                                    parts = pattern_key.split('_')
                                    if len(parts) >= 4:
                                        from_val = parts[2]
                                        to_val = parts[4] if len(parts) > 4 else parts[3]
                                        mapping_key = f"from_{from_val}_to_{to_val}"

                                        if mapping_key not in self.value_mappings:
                                            self.value_mappings[mapping_key] = []
                                        self.value_mappings[mapping_key].append((task_id, accuracy))
                    except:
                        pass

    def get_statistics(self) -> Dict:
        """Get memory statistics."""
        return {
            'total_tasks': len(self.task_index),
            'total_patterns': len(self.pattern_index),
            'total_value_mappings': len(self.value_mappings),
            'avg_patterns_per_task': len(self.pattern_index) / max(len(self.task_index), 1),
            'high_conf_mappings': len([m for m, tasks in self.value_mappings.items()
                                      if any(c >= 0.8 for _, c in tasks)])
        }