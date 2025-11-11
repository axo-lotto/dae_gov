#!/usr/bin/env python3
"""
Health Dashboard for DAE-GOV
============================

Real-time conversation health monitoring with organism state visualization.

Adapted from DAE 3.0 monitoring system for DAE-GOV conversational organism.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ConversationHealth:
    """Health metrics for current conversation state."""
    r_matrix_updates: int
    avg_coherence: float
    polyvagal_state: str
    self_energy: float
    recent_gate_decisions: List[str]
    knowledge_retrievals: int
    curiosity_triggers: int
    maturation_level: str
    health_status: str  # HEALTHY, WARNING, CRITICAL


class HealthDashboard:
    """
    Real-time health monitoring for DAE-GOV conversational organism.

    Features:
    - Organism state visualization
    - R-matrix growth tracking
    - Coherence monitoring
    - Polyvagal state tracking
    - Real-time health indicators
    """

    def __init__(self, base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1"):
        self.base_path = Path(base_path)
        self.bundle_path = self.base_path / "Bundle"

    def get_current_health(self, session_tracker=None) -> ConversationHealth:
        """
        Get current conversation health metrics.

        Args:
            session_tracker: Optional SessionTracker instance for live session data

        Returns:
            ConversationHealth dataclass with current metrics
        """
        # Default values
        r_matrix_updates = 0
        avg_coherence = 0.0
        polyvagal_state = "unknown"
        self_energy = 0.0
        recent_gate_decisions = []
        knowledge_retrievals = 0
        curiosity_triggers = 0

        # If session tracker provided, get live session data
        if session_tracker and session_tracker.current_session:
            session = session_tracker.current_session

            # R-matrix updates from user state
            user_id = session['user_id']
            user_state = self._load_user_state(user_id)
            r_matrix_updates = user_state.get('r_matrix_updates', 0)

            # Metrics from current session
            metrics = session['metrics']
            knowledge_retrievals = metrics['knowledge_retrievals']
            curiosity_triggers = metrics['curiosity_triggers']

            # Calculate average coherence
            coherences = metrics.get('coherences', [])
            avg_coherence = sum(coherences) / len(coherences) if coherences else 0.0

            # Get recent turns data
            recent_turns = session['turns'][-5:]  # Last 5 turns
            if recent_turns:
                # Most recent polyvagal state
                polyvagal_state = recent_turns[-1]['polyvagal_state']

                # Most recent self energy
                self_energy = recent_turns[-1].get('self_energy', 0.0)

                # Recent gate decisions
                recent_gate_decisions = [turn['gate_decision'] for turn in recent_turns]

        # Determine maturation level based on R-matrix
        if r_matrix_updates >= 500:
            maturation_level = "MASTERFUL"
        elif r_matrix_updates >= 200:
            maturation_level = "MATURE"
        elif r_matrix_updates >= 50:
            maturation_level = "GROWING"
        else:
            maturation_level = "NEW"

        # Determine health status
        health_status = self._assess_health_status(
            avg_coherence, polyvagal_state, self_energy
        )

        return ConversationHealth(
            r_matrix_updates=r_matrix_updates,
            avg_coherence=avg_coherence,
            polyvagal_state=polyvagal_state,
            self_energy=self_energy,
            recent_gate_decisions=recent_gate_decisions,
            knowledge_retrievals=knowledge_retrievals,
            curiosity_triggers=curiosity_triggers,
            maturation_level=maturation_level,
            health_status=health_status
        )

    def _assess_health_status(self, coherence: float, polyvagal: str, energy: float) -> str:
        """Assess overall conversation health."""
        # Critical conditions
        if polyvagal == "dorsal" or energy < 0.1:
            return "CRITICAL"

        # Warning conditions
        if coherence < 0.3 or polyvagal == "sympathetic":
            return "WARNING"

        # Healthy conditions
        if coherence >= 0.5 and polyvagal == "ventral" and energy >= 0.3:
            return "HEALTHY"

        return "MODERATE"

    def _load_user_state(self, user_id: str) -> Dict:
        """Load user state from Bundle."""
        user_state_file = self.bundle_path / user_id / "user_state.json"

        if not user_state_file.exists():
            return {
                "user_id": user_id,
                "r_matrix_updates": 0,
                "total_conversations": 0,
                "total_turns": 0
            }

        with open(user_state_file, 'r') as f:
            return json.load(f)

    def display_health_dashboard(self, session_tracker=None):
        """Display formatted health dashboard."""
        health = self.get_current_health(session_tracker)

        # Health status indicator
        status_indicators = {
            "HEALTHY": "✅",
            "MODERATE": "⚡",
            "WARNING": "⚠️",
            "CRITICAL": "❌"
        }
        status_icon = status_indicators.get(health.health_status, "❓")

        # Maturation glyph
        maturation_glyphs = {
            "NEW": "🌱",
            "GROWING": "🌿",
            "MATURE": "🌀",
            "MASTERFUL": "✨"
        }
        maturation_glyph = maturation_glyphs.get(health.maturation_level, "🌱")

        print("\n" + "="*70)
        print(f"{status_icon} DAE-GOV HEALTH DASHBOARD {status_icon}")
        print("="*70)
        print()

        # Organism State
        print(f"{maturation_glyph} ORGANISM STATE: {health.maturation_level}")
        print(f"   R-matrix updates: {health.r_matrix_updates:,}")
        print(f"   Average coherence: {health.avg_coherence:.3f}")
        print(f"   Polyvagal state: {health.polyvagal_state.upper()}")
        print(f"   Self energy: {health.self_energy:.3f}")
        print()

        # Conversation Metrics
        print("📊 CONVERSATION METRICS")
        print(f"   Knowledge retrievals: {health.knowledge_retrievals}")
        print(f"   Curiosity triggers: {health.curiosity_triggers}")
        print()

        # Recent Activity
        if health.recent_gate_decisions:
            print("🔄 RECENT GATE DECISIONS (last 5)")
            for i, gate in enumerate(health.recent_gate_decisions, 1):
                print(f"   {i}. {gate}")
            print()

        # Health Assessment
        print(f"{status_icon} HEALTH STATUS: {health.health_status}")
        if health.health_status == "CRITICAL":
            print("   ⚠️  Organism in distress - dorsal state or very low energy")
        elif health.health_status == "WARNING":
            print("   ⚠️  Low coherence or sympathetic state detected")
        elif health.health_status == "HEALTHY":
            print("   ✅ Organism functioning optimally")
        else:
            print("   ⚡ Moderate health - monitoring recommended")

        print("="*70 + "\n")

    def get_system_status(self) -> Dict:
        """Get overall system health across all users."""
        status = {
            'bundle_exists': self.bundle_path.exists(),
            'total_users': 0,
            'active_users': [],
            'total_conversations': 0,
            'total_r_matrix_updates': 0
        }

        if not self.bundle_path.exists():
            return status

        # Scan all user directories
        for user_dir in self.bundle_path.iterdir():
            if user_dir.is_dir() and user_dir.name.startswith('user'):
                status['total_users'] += 1

                user_state = self._load_user_state(user_dir.name)
                status['total_conversations'] += user_state.get('total_conversations', 0)
                status['total_r_matrix_updates'] += user_state.get('r_matrix_updates', 0)

                if user_state.get('last_active'):
                    status['active_users'].append({
                        'user_id': user_dir.name,
                        'last_active': user_state['last_active'],
                        'conversations': user_state.get('total_conversations', 0)
                    })

        # Sort active users by last active
        status['active_users'].sort(key=lambda x: x['last_active'], reverse=True)

        return status

    def display_system_status(self):
        """Display system-wide health status."""
        status = self.get_system_status()

        print("\n" + "="*70)
        print("🌀 DAE-GOV SYSTEM STATUS")
        print("="*70)
        print()

        if not status['bundle_exists']:
            print("❌ Bundle directory not found")
            print(f"   Expected location: {self.bundle_path}")
            print("="*70 + "\n")
            return

        print(f"📊 SYSTEM METRICS")
        print(f"   Total users: {status['total_users']}")
        print(f"   Total conversations: {status['total_conversations']:,}")
        print(f"   Total R-matrix updates: {status['total_r_matrix_updates']:,}")
        print()

        if status['active_users']:
            print(f"👥 ACTIVE USERS (last {min(5, len(status['active_users']))})")
            for user in status['active_users'][:5]:
                print(f"   • {user['user_id']}: {user['conversations']} conversations")
                print(f"     Last active: {user['last_active']}")
        else:
            print("👥 No active users yet")

        print("="*70 + "\n")


class SimpleDashboard:
    """
    Simplified health display for quick status checks.

    Use this for one-line status indicators during conversations.
    """

    def __init__(self, base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1"):
        self.dashboard = HealthDashboard(base_path)

    def get_status_line(self, session_tracker=None) -> str:
        """Get one-line status indicator."""
        health = self.dashboard.get_current_health(session_tracker)

        # Status indicators
        status_map = {
            "HEALTHY": "✅",
            "MODERATE": "⚡",
            "WARNING": "⚠️",
            "CRITICAL": "❌"
        }
        status = status_map.get(health.health_status, "❓")

        # Maturation glyphs
        maturation_map = {
            "NEW": "🌱",
            "GROWING": "🌿",
            "MATURE": "🌀",
            "MASTERFUL": "✨"
        }
        glyph = maturation_map.get(health.maturation_level, "🌱")

        return (f"{status} {glyph} R:{health.r_matrix_updates} "
                f"C:{health.avg_coherence:.2f} "
                f"PV:{health.polyvagal_state[0].upper()} "
                f"E:{health.self_energy:.2f}")

    def print_status(self, session_tracker=None):
        """Print status line."""
        print(self.get_status_line(session_tracker))


# Convenience functions
def create_health_dashboard(base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1") -> HealthDashboard:
    """Create health dashboard instance."""
    return HealthDashboard(base_path)


def quick_health_check(base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1"):
    """Quick health check and display."""
    dashboard = HealthDashboard(base_path)
    dashboard.display_health_dashboard()
    dashboard.display_system_status()


if __name__ == "__main__":
    # Test health dashboard
    print("Testing DAE-GOV Health Dashboard...")
    print()

    dashboard = HealthDashboard()

    # Display health (no active session)
    dashboard.display_health_dashboard()

    # Display system status
    dashboard.display_system_status()

    # Test simple dashboard
    simple = SimpleDashboard()
    print("Simple status line:")
    simple.print_status()

    print("\n✅ Health dashboard operational")
