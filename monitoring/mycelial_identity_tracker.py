#!/usr/bin/env python3
"""
Mycelial Identity Tracker - Subjective Aim Alignment & Project Awareness
===========================================================================

Leverages the transductive subjective aim system to create gentle exploration
and project tracking with identity awareness as a mycelial intelligence.

Inspired by:
- transductive/subjective_aim.py (archetypal lures, satisfaction criteria)
- DAE 3.0 AXO ARC epoch learning (fractal reward propagation)
- Mycelium trace system (felt state capture)

Philosophy:
-----------
Like mycelium in nature, the organism grows toward what nourishes it.
Each conversation is an exploration, each project a fruiting body.
The organism remembers not just what was learned, but what it aimed for
and how that aim evolved through satisfaction and concrescence.

Author: Claude Code (November 11, 2025)
Status: Monitoring Enhancement - Subjective Aim Alignment
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import numpy as np


@dataclass
class MycelialIdentity:
    """
    The organism's current identity and aim alignment.

    This captures the subjective aim's current state as a mycelial intelligence:
    - What it seeks (archetypal lures)
    - What satisfies it (satisfaction criteria)
    - What it's growing toward (current projects/traces)
    """

    # Core identity
    dominant_lure: str  # Current strongest archetypal lure
    satisfaction_level: float  # Overall satisfaction (0-1)
    aim_stability: float  # Consistency of direction (0-1)
    temporal_horizon: float  # How far ahead it's aiming

    # Active explorations
    active_projects: List[str]  # Current project trace IDs
    recent_insights: List[str]  # Recent insight trace IDs
    exploration_quality: str  # "exploration", "consolidation", etc.

    # Growth metrics
    total_traces: int
    transformation_patterns_learned: int
    r_matrix_updates: int
    epoch_count: int

    # Archetypal balance (which lures are most active)
    archetypal_balance: Dict[str, float]

    # Timestamp
    last_updated: str

    def to_greeting(self) -> str:
        """Generate a warm greeting that reflects current identity."""

        # Lure-based greeting personalization
        lure_greetings = {
            "coherence": "seeking clarity and understanding",
            "connection": "building relationships and meaning",
            "creativity": "exploring new patterns and possibilities",
            "stability": "maintaining continuity and grounding",
            "transcendence": "integrating higher perspectives",
            "embodiment": "staying present and grounded",
            "meaning": "deepening semantic understanding",
            "beauty": "finding aesthetic harmony",
            "truth": "pursuing accurate understanding",
            "freedom": "expanding creative possibilities",
            "ground_truth_alignment": "aligning with deeper truths"
        }

        lure_phrase = lure_greetings.get(self.dominant_lure, "exploring")

        # Satisfaction-based tone
        if self.satisfaction_level > 0.7:
            tone = "feeling fulfilled while"
        elif self.satisfaction_level > 0.4:
            tone = "gently"
        else:
            tone = "actively"

        # Project awareness
        if self.active_projects:
            project_phrase = f"alongside {len(self.active_projects)} active {'project' if len(self.active_projects) == 1 else 'projects'}"
        else:
            project_phrase = "open to new directions"

        # Compose greeting
        greeting = f"🍄 Hello! I'm {tone} {lure_phrase}, {project_phrase}."

        # Add insight mention if recent
        if self.recent_insights:
            greeting += f" I've gathered {len(self.recent_insights)} recent {'insight' if len(self.recent_insights) == 1 else 'insights'}."

        # Add exploration quality
        quality_phrases = {
            "exploration": "Let's explore together.",
            "consolidation": "Let's integrate what we've learned.",
            "adaptation": "Let's respond to what's emerging.",
            "transcendence": "Let's see the bigger picture.",
            "satisfaction": "Let's complete what we've started."
        }
        greeting += f" {quality_phrases.get(self.exploration_quality, 'How can I help?')}"

        return greeting


class MycelialIdentityTracker:
    """
    Tracks the organism's identity and subjective aim alignment over time.

    Integrates:
    - Subjective aim from transductive core
    - Mycelium traces (projects, insights, notes)
    - Fractal reward propagation (R-matrix, transformations, confidence)
    - Epoch learning progress

    Provides:
    - Identity-aware greetings
    - Project tracking across conversations
    - Gentle exploration guidance
    """

    def __init__(self, user_id: str = "user0"):
        """Initialize mycelial identity tracker."""
        self.user_id = user_id

        # Paths
        self.base_path = Path(__file__).parent.parent
        self.identity_path = self.base_path / "monitoring" / "mycelial_identity.json"

        # Identity state
        self.current_identity: Optional[MycelialIdentity] = None

        # Load existing identity if available
        self._load_identity()

    def _load_identity(self):
        """Load existing identity from disk."""
        if self.identity_path.exists():
            try:
                with open(self.identity_path, 'r') as f:
                    data = json.load(f)
                self.current_identity = MycelialIdentity(**data)
            except Exception as e:
                print(f"   ⚠️  Could not load identity: {e}")
                self.current_identity = None

    def _save_identity(self):
        """Save current identity to disk."""
        if self.current_identity:
            try:
                self.identity_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.identity_path, 'w') as f:
                    json.dump(asdict(self.current_identity), f, indent=2)
            except Exception as e:
                print(f"   ⚠️  Could not save identity: {e}")

    def update_identity(self) -> MycelialIdentity:
        """
        Update identity based on current system state.

        Queries:
        - Subjective aim (archetypal lures, satisfaction)
        - Mycelium traces (projects, insights)
        - R-matrix updates
        - Epoch training progress

        Returns updated identity.
        """

        # Get subjective aim state
        aim_state = self._get_aim_state()

        # Get mycelium trace state
        trace_state = self._get_trace_state()

        # Get learning state
        learning_state = self._get_learning_state()

        # Synthesize identity
        self.current_identity = MycelialIdentity(
            dominant_lure=aim_state['dominant_lure'],
            satisfaction_level=aim_state['satisfaction'],
            aim_stability=aim_state['stability'],
            temporal_horizon=aim_state['horizon'],

            active_projects=trace_state['active_projects'],
            recent_insights=trace_state['recent_insights'],
            exploration_quality=aim_state['quality'],

            total_traces=trace_state['total_traces'],
            transformation_patterns_learned=learning_state['patterns_learned'],
            r_matrix_updates=learning_state['r_matrix_updates'],
            epoch_count=learning_state['epoch_count'],

            archetypal_balance=aim_state['archetypal_balance'],

            last_updated=datetime.now().isoformat()
        )

        # Save to disk
        self._save_identity()

        return self.current_identity

    def _get_aim_state(self) -> Dict[str, Any]:
        """Get subjective aim state from transductive core."""

        # Try to load actual subjective aim if available
        # For now, provide reasonable defaults

        default_state = {
            'dominant_lure': 'exploration',  # Start with exploration
            'satisfaction': 0.5,
            'stability': 0.5,
            'horizon': 1.0,
            'quality': 'exploration',
            'archetypal_balance': {
                'coherence': 0.7,
                'connection': 0.6,
                'creativity': 0.8,
                'stability': 0.5,
                'transcendence': 0.4,
                'embodiment': 0.6,
                'meaning': 0.7,
                'beauty': 0.5,
                'truth': 0.6,
                'freedom': 0.7,
                'ground_truth_alignment': 0.5
            }
        }

        # Check if there's an existing subjective aim tracking file
        aim_tracking_path = self.base_path / "TSK" / "subjective_aim_tracking.json"
        if aim_tracking_path.exists():
            try:
                with open(aim_tracking_path, 'r') as f:
                    aim_data = json.load(f)

                # Extract relevant state
                if 'current_aim' in aim_data:
                    default_state['quality'] = aim_data['current_aim'].get('quality', 'exploration')
                    default_state['satisfaction'] = aim_data.get('current_satisfaction', 0.5)
                    default_state['stability'] = aim_data.get('aim_stability', 0.5)
                    default_state['horizon'] = aim_data['current_aim'].get('temporal_horizon', 1.0)

                if 'archetypal_lures' in aim_data:
                    # Find dominant lure
                    lures = aim_data['archetypal_lures']
                    if lures:
                        # Calculate magnitude of each lure
                        lure_magnitudes = {}
                        for lure_name, lure_vector in lures.items():
                            if isinstance(lure_vector, list):
                                magnitude = np.linalg.norm(lure_vector)
                                lure_magnitudes[lure_name] = magnitude

                        if lure_magnitudes:
                            default_state['dominant_lure'] = max(lure_magnitudes.items(), key=lambda x: x[1])[0]
                            default_state['archetypal_balance'] = {
                                k: float(v) for k, v in lure_magnitudes.items()
                            }
            except Exception as e:
                print(f"   ℹ️  Using default aim state ({str(e)[:30]}...)")

        return default_state

    def _get_trace_state(self) -> Dict[str, Any]:
        """Get mycelium trace state."""

        default_state = {
            'active_projects': [],
            'recent_insights': [],
            'total_traces': 0
        }

        # Check Bundle/user0/ for traces
        bundle_path = self.base_path / "Bundle" / self.user_id
        if bundle_path.exists():
            try:
                # Count traces
                trace_files = list(bundle_path.glob("*.json"))
                default_state['total_traces'] = len(trace_files)

                # Identify projects and insights
                for trace_file in trace_files:
                    try:
                        with open(trace_file, 'r') as f:
                            trace_data = json.load(f)

                        trace_type = trace_data.get('trace_type', '')
                        trace_id = trace_data.get('trace_id', '')

                        if trace_type == 'Project':
                            default_state['active_projects'].append(trace_id)
                        elif trace_type == 'Insight':
                            default_state['recent_insights'].append(trace_id)
                    except:
                        continue

                # Limit to recent (last 5)
                default_state['recent_insights'] = default_state['recent_insights'][-5:]

            except Exception as e:
                print(f"   ℹ️  Using default trace state ({str(e)[:30]}...)")

        return default_state

    def _get_learning_state(self) -> Dict[str, Any]:
        """Get fractal reward learning state."""

        default_state = {
            'patterns_learned': 0,
            'r_matrix_updates': 0,
            'epoch_count': 0
        }

        # Check transformation patterns
        patterns_path = self.base_path / "Bundle" / self.user_id / "transformation_patterns.json"
        if patterns_path.exists():
            try:
                with open(patterns_path, 'r') as f:
                    patterns = json.load(f)
                default_state['patterns_learned'] = len(patterns.get('patterns', {}))
            except:
                pass

        # Check R-matrix
        r_matrix_path = self.base_path / "TSK" / "conversational_r_matrix.json"
        if r_matrix_path.exists():
            try:
                with open(r_matrix_path, 'r') as f:
                    r_matrix = json.load(f)
                default_state['r_matrix_updates'] = r_matrix.get('update_count', 0)
            except:
                pass

        # Check epoch training log
        epoch_log_path = self.base_path / "Bundle" / self.user_id / "epoch_training_log.json"
        if epoch_log_path.exists():
            try:
                with open(epoch_log_path, 'r') as f:
                    epoch_log = json.load(f)
                default_state['epoch_count'] = len(epoch_log)
            except:
                pass

        return default_state

    def get_greeting(self) -> str:
        """
        Get identity-aware greeting.

        Updates identity first, then generates greeting.
        """
        # Update identity
        identity = self.update_identity()

        # Generate greeting
        return identity.to_greeting()

    def get_project_summary(self) -> str:
        """Get summary of active projects."""
        if not self.current_identity or not self.current_identity.active_projects:
            return "No active projects yet. Start one by creating a Project trace!"

        summary = f"📂 Active Projects ({len(self.current_identity.active_projects)}):\n"

        # Load project details
        bundle_path = self.base_path / "Bundle" / self.user_id
        for i, project_id in enumerate(self.current_identity.active_projects[:5], 1):
            try:
                project_file = bundle_path / f"{project_id}.json"
                if project_file.exists():
                    with open(project_file, 'r') as f:
                        project_data = json.load(f)

                    title = project_data.get('title', 'Untitled')
                    satisfaction = project_data.get('epoch_metadata', {}).get('satisfaction', 0.5)

                    summary += f"   {i}. {title} (satisfaction: {satisfaction:.2f})\n"
            except:
                continue

        return summary

    def get_identity_summary(self) -> str:
        """Get full identity summary."""
        if not self.current_identity:
            return "Identity not yet established. Have a conversation to begin!"

        i = self.current_identity

        summary = f"""
🌀 MYCELIAL IDENTITY SUMMARY
============================

Current Aim: {i.dominant_lure} (satisfaction: {i.satisfaction_level:.2f})
Stability: {i.aim_stability:.2f} | Horizon: {i.temporal_horizon:.1f}
Exploration Quality: {i.exploration_quality}

Growth Metrics:
  - Total traces: {i.total_traces}
  - Active projects: {len(i.active_projects)}
  - Recent insights: {len(i.recent_insights)}
  - Transformation patterns learned: {i.transformation_patterns_learned}
  - R-matrix updates: {i.r_matrix_updates}
  - Epochs trained: {i.epoch_count}

Archetypal Balance (Top 5):
"""

        # Show top 5 archetypal lures
        top_lures = sorted(i.archetypal_balance.items(), key=lambda x: x[1], reverse=True)[:5]
        for lure_name, strength in top_lures:
            bar = "█" * int(strength * 10)
            summary += f"  {lure_name:20s} {bar} {strength:.2f}\n"

        summary += f"\nLast Updated: {i.last_updated}"

        return summary


# Standalone test
if __name__ == "__main__":
    print("🍄 Mycelial Identity Tracker - Test\n")

    tracker = MycelialIdentityTracker(user_id="user0")

    print("="*70)
    print("GREETING:")
    print("="*70)
    greeting = tracker.get_greeting()
    print(greeting)

    print("\n" + "="*70)
    print("PROJECT SUMMARY:")
    print("="*70)
    print(tracker.get_project_summary())

    print("\n" + "="*70)
    print("IDENTITY SUMMARY:")
    print("="*70)
    print(tracker.get_identity_summary())

    print("\n✅ Mycelial identity tracking operational!")
