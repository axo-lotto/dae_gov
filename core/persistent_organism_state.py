#!/usr/bin/env python3
"""
Persistent Organism State - Fractal Reward System
==================================================

Maintains persistent state across tasks with fractal reward propagation
for successful transformations. Enables the organism to start any task
(novel or old) with accumulated knowledge.

Key Features:
1. Persistent state that survives across sessions
2. Fractal reward system (success propagates at multiple scales)
3. Conflict-free recall through confidence weighting
4. Task-agnostic initialization

Created: November 3, 2025
"""

import json
import os
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path


class PersistentOrganismState:
    """
    Persistent state with fractal reward system.

    The organism maintains state across all tasks and sessions,
    rewarding successful transformations at multiple scales.
    """

    def __init__(self, state_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1/data/organism_state.json"):
        """Initialize persistent organism state."""

        self.state_path = state_path
        Path(state_path).parent.mkdir(parents=True, exist_ok=True)

        # Core persistent state
        self.state = {
            # Global organism health
            'global_confidence': 0.5,
            'total_successes': 0,
            'total_attempts': 0,
            'success_rate': 0.0,

            # Fractal reward levels
            'rewards': {
                'micro': {},    # Individual pattern successes
                'meso': {},     # Task-level successes
                'macro': {}     # Family/category successes
            },

            # Accumulated knowledge
            'knowledge': {
                'successful_patterns': {},
                'successful_transforms': {},
                'successful_strategies': {}
            },

            # Conflict resolution
            'confidence_weights': {},

            # Session history
            'sessions': [],
            'last_updated': None
        }

        # Load existing state
        self.load_state()

        # Initialize current session
        self.current_session = {
            'start_time': datetime.now().isoformat(),
            'tasks_attempted': 0,
            'tasks_succeeded': 0,
            'patterns_learned': 0
        }

        print("🧬 Persistent Organism State initialized")
        print(f"   Global confidence: {self.state['global_confidence']:.2f}")
        print(f"   Total successes: {self.state['total_successes']}")
        print(f"   Success rate: {self.state['success_rate']:.1%}")

    def load_state(self):
        """Load persistent state from disk."""

        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, 'r') as f:
                    loaded = json.load(f)
                    self.state.update(loaded)
                    print(f"   ✅ Loaded existing state from {self.state_path}")
            except Exception as e:
                print(f"   ⚠️ Could not load state: {e}")
                print("   Starting with fresh state")

    def save_state(self):
        """Save persistent state to disk."""

        self.state['last_updated'] = datetime.now().isoformat()

        try:
            with open(self.state_path, 'w') as f:
                json.dump(self.state, f, indent=2, default=str)
            print(f"   💾 State saved to {self.state_path}")
        except Exception as e:
            print(f"   ⚠️ Could not save state: {e}")

    def register_success(
        self,
        task_id: str,
        accuracy: float,
        patterns: Dict[str, Any],
        task_type: str = 'unknown'
    ):
        """
        Register a successful transformation with fractal reward propagation.

        Success at 90%+ triggers rewards at multiple scales:
        - Micro: Individual patterns get confidence boost
        - Meso: Task family gets success credit
        - Macro: Global confidence increases
        """

        if accuracy < 0.9:
            print(f"   ⚠️ Not registering {task_id} - accuracy {accuracy:.1%} < 90%")
            return

        print(f"\n   🎊 Registering SUCCESS for {task_id} ({accuracy:.1%})")

        # Update global state
        self.state['total_successes'] += 1
        self.state['total_attempts'] += 1
        self.state['success_rate'] = self.state['total_successes'] / max(self.state['total_attempts'], 1)

        # FRACTAL REWARD PROPAGATION

        # 1. MICRO REWARDS - Individual patterns
        for pattern_key, pattern_data in patterns.items():
            micro_key = f"pattern_{pattern_key}"
            if micro_key not in self.state['rewards']['micro']:
                self.state['rewards']['micro'][micro_key] = {
                    'successes': 0,
                    'confidence': 0.5
                }

            # Boost pattern confidence
            self.state['rewards']['micro'][micro_key]['successes'] += 1
            old_conf = self.state['rewards']['micro'][micro_key]['confidence']
            new_conf = min(1.0, old_conf + 0.1 * accuracy)  # Scale by accuracy
            self.state['rewards']['micro'][micro_key]['confidence'] = new_conf

            print(f"      📈 Micro reward: {pattern_key} confidence {old_conf:.2f} → {new_conf:.2f}")

        # 2. MESO REWARDS - Task family level
        meso_key = f"family_{task_type}"
        if meso_key not in self.state['rewards']['meso']:
            self.state['rewards']['meso'][meso_key] = {
                'successes': 0,
                'total': 0,
                'avg_accuracy': 0.0
            }

        meso = self.state['rewards']['meso'][meso_key]
        meso['successes'] += 1
        meso['total'] += 1
        # Running average of accuracy
        meso['avg_accuracy'] = (meso['avg_accuracy'] * (meso['total'] - 1) + accuracy) / meso['total']

        print(f"      📊 Meso reward: {task_type} family now {meso['successes']}/{meso['total']} successful")

        # 3. MACRO REWARDS - Global organism level
        old_global = self.state['global_confidence']
        # Global confidence increases logarithmically with successes
        success_factor = np.log(self.state['total_successes'] + 1) / 10
        self.state['global_confidence'] = min(1.0, 0.5 + success_factor)

        print(f"      🌍 Macro reward: Global confidence {old_global:.2f} → {self.state['global_confidence']:.2f}")

        # Store successful patterns for recall
        self.state['knowledge']['successful_patterns'][task_id] = {
            'patterns': patterns,
            'accuracy': accuracy,
            'task_type': task_type,
            'timestamp': datetime.now().isoformat()
        }

        # Update session
        self.current_session['tasks_succeeded'] += 1
        self.current_session['patterns_learned'] += len(patterns)

        # Save state after success
        self.save_state()

    def register_attempt(self, task_id: str, accuracy: float):
        """Register a task attempt (success or failure)."""

        self.state['total_attempts'] += 1
        self.current_session['tasks_attempted'] += 1

        if accuracy < 0.9:
            print(f"   ❌ Task {task_id} failed with {accuracy:.1%}")
        else:
            # Will be handled by register_success
            pass

        # Update success rate
        self.state['success_rate'] = self.state['total_successes'] / max(self.state['total_attempts'], 1)

    def get_initial_state_for_task(
        self,
        task_id: str,
        task_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get initial state for starting a new task.

        Returns accumulated knowledge and confidence levels
        relevant to this task, enabling informed initialization.
        """

        initial_state = {
            'global_confidence': self.state['global_confidence'],
            'relevant_patterns': {},
            'family_confidence': 0.5,
            'suggested_strategies': []
        }

        # Get family-specific confidence if available
        if task_type:
            meso_key = f"family_{task_type}"
            if meso_key in self.state['rewards']['meso']:
                family_data = self.state['rewards']['meso'][meso_key]
                initial_state['family_confidence'] = family_data['avg_accuracy']
                print(f"   📊 Family '{task_type}' confidence: {family_data['avg_accuracy']:.2f}")

        # Get high-confidence patterns
        for pattern_key, pattern_data in self.state['rewards']['micro'].items():
            if pattern_data['confidence'] >= 0.7:
                initial_state['relevant_patterns'][pattern_key] = pattern_data

        print(f"   🎯 Initial state for {task_id}:")
        print(f"      Global confidence: {initial_state['global_confidence']:.2f}")
        print(f"      Relevant patterns: {len(initial_state['relevant_patterns'])}")
        print(f"      Family confidence: {initial_state['family_confidence']:.2f}")

        return initial_state

    def conflict_free_recall(
        self,
        query_patterns: List[str],
        confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Recall patterns without conflicts using confidence weighting.

        When multiple patterns match, returns the one with highest
        confidence to avoid conflicts.
        """

        recalled = {}

        for query in query_patterns:
            # Find all matching patterns
            matches = []

            for task_id, task_data in self.state['knowledge']['successful_patterns'].items():
                for pattern_key, pattern in task_data['patterns'].items():
                    if query in pattern_key:
                        matches.append({
                            'pattern': pattern,
                            'confidence': task_data['accuracy'],
                            'task_id': task_id,
                            'key': pattern_key
                        })

            # Select highest confidence match
            if matches:
                best_match = max(matches, key=lambda x: x['confidence'])
                if best_match['confidence'] >= confidence_threshold:
                    recalled[query] = best_match
                    print(f"   🔍 Recalled {query} from {best_match['task_id']} (conf={best_match['confidence']:.2f})")

        return recalled

    def get_learning_trajectory(self) -> Dict[str, Any]:
        """Get organism's learning trajectory over time."""

        trajectory = {
            'total_sessions': len(self.state['sessions']),
            'total_attempts': self.state['total_attempts'],
            'total_successes': self.state['total_successes'],
            'current_success_rate': self.state['success_rate'],
            'global_confidence': self.state['global_confidence'],
            'family_performance': {}
        }

        # Summarize family performance
        for family_key, family_data in self.state['rewards']['meso'].items():
            family_name = family_key.replace('family_', '')
            trajectory['family_performance'][family_name] = {
                'success_rate': family_data['successes'] / max(family_data['total'], 1),
                'avg_accuracy': family_data['avg_accuracy'],
                'total_tasks': family_data['total']
            }

        return trajectory

    def end_session(self):
        """End current session and save state."""

        self.current_session['end_time'] = datetime.now().isoformat()
        self.current_session['success_rate'] = (
            self.current_session['tasks_succeeded'] /
            max(self.current_session['tasks_attempted'], 1)
        )

        # Add to session history
        self.state['sessions'].append(self.current_session)

        # Keep only last 100 sessions
        if len(self.state['sessions']) > 100:
            self.state['sessions'] = self.state['sessions'][-100:]

        print(f"\n📊 Session Summary:")
        print(f"   Tasks attempted: {self.current_session['tasks_attempted']}")
        print(f"   Tasks succeeded: {self.current_session['tasks_succeeded']}")
        print(f"   Session success rate: {self.current_session['success_rate']:.1%}")
        print(f"   Patterns learned: {self.current_session['patterns_learned']}")

        # Save final state
        self.save_state()


class FractalRewardSystem:
    """
    Fractal reward propagation system.

    Rewards successful transformations at multiple scales,
    creating a self-reinforcing learning system.
    """

    def __init__(self):
        """Initialize fractal reward system."""

        self.reward_scales = {
            'micro': 0.1,    # Individual pattern
            'meso': 0.25,    # Task/family level
            'macro': 0.5     # Global organism
        }

    def propagate_reward(
        self,
        success_level: float,
        patterns: Dict[str, Any],
        state: PersistentOrganismState
    ) -> Dict[str, float]:
        """
        Propagate rewards fractally across scales.

        Success at one level influences all scales.
        """

        rewards = {}

        # Micro scale - each pattern
        for pattern_key in patterns:
            micro_reward = success_level * self.reward_scales['micro']
            rewards[f"micro_{pattern_key}"] = micro_reward

        # Meso scale - task family
        meso_reward = success_level * self.reward_scales['meso']
        rewards['meso_family'] = meso_reward

        # Macro scale - global
        macro_reward = success_level * self.reward_scales['macro']
        rewards['macro_global'] = macro_reward

        # Fractal propagation - success at one scale affects others
        if success_level >= 0.95:  # Near perfect
            # Boost all scales
            for key in rewards:
                rewards[key] *= 1.5

        return rewards