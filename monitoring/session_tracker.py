#!/usr/bin/env python3
"""
Session Tracker for DAE-GOV
============================

Tracks conversation sessions with user compartmentalization,
R-matrix evolution, and learning progression.

Adapted from DAE 3.0 monitoring system.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict


@dataclass
class SessionMetrics:
    """Metrics for a single conversation session."""
    session_id: str
    user_id: str
    start_time: str
    end_time: Optional[str]
    total_turns: int
    greetings: int
    curiosity_triggers: int
    knowledge_retrievals: int
    r_matrix_start: int
    r_matrix_end: int
    r_matrix_delta: int
    avg_coherence: float
    polyvagal_states: Dict[str, int]  # ventral, sympathetic, dorsal counts


class SessionTracker:
    """
    Track and persist conversation sessions with user compartmentalization.

    Features:
    - Per-user session isolation
    - R-matrix evolution tracking
    - Learning progression metrics
    - Conversation health monitoring
    """

    def __init__(self, base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1"):
        self.base_path = Path(base_path)
        self.bundle_path = self.base_path / "Bundle"
        self.current_session: Optional[Dict] = None
        self.current_user: Optional[str] = None

    def start_session(self, user_id: str = "user0") -> str:
        """
        Start a new conversation session.

        Args:
            user_id: User identifier (user0, user1, etc.)

        Returns:
            session_id: Unique session identifier
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.current_user = user_id
        self.current_session = {
            'session_id': session_id,
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'turns': [],
            'metrics': {
                'total_turns': 0,
                'greetings': 0,
                'curiosity_triggers': 0,
                'knowledge_retrievals': 0,
                'polyvagal_states': {'ventral': 0, 'sympathetic': 0, 'dorsal': 0},
                'coherences': []
            }
        }

        # Update user state
        self._update_user_state(user_id, session_start=True)

        print(f"✅ Session started: {session_id} for {user_id}")
        return session_id

    def record_turn(self,
                   user_input: str,
                   result: Dict,
                   response: str):
        """Record a single conversation turn."""

        if not self.current_session:
            raise RuntimeError("No active session. Call start_session() first.")

        turn_data = {
            'turn_number': self.current_session['metrics']['total_turns'] + 1,
            'timestamp': result.get('timestamp', datetime.now().isoformat()),
            'user_input': user_input,
            'response': response,
            'gate_decision': result['organism_analysis']['gate_decision'],
            'polyvagal_state': result['organism_analysis']['polyvagal_state'],
            'self_energy': result['organism_analysis'].get('self_energy', 0.0),
            'knowledge_used': len(result.get('knowledge_context') or []),
            'conversational_organs': None
        }

        # Track conversational organs if present
        if result.get('conversational_organs'):
            organs = result['conversational_organs']
            turn_data['conversational_organs'] = {
                'curiosity_triggered': organs.get('curiosity_triggered', False),
                'r_matrix_updates': organs.get('r_matrix_updates', 0)
            }

            # Calculate average coherence from organs
            if organs.get('organ_results'):
                coherences = [o.coherence for o in organs['organ_results'].values()]
                avg_coherence = sum(coherences) / len(coherences)
                turn_data['avg_coherence'] = avg_coherence
                self.current_session['metrics']['coherences'].append(avg_coherence)

        # Update metrics
        self.current_session['turns'].append(turn_data)
        self.current_session['metrics']['total_turns'] += 1

        # Track gate decisions
        gate = result['organism_analysis']['gate_decision']
        if gate == 'GREETING':
            self.current_session['metrics']['greetings'] += 1
        elif gate == 'CURIOSITY_QUESTION':
            self.current_session['metrics']['curiosity_triggers'] += 1

        # Track polyvagal state
        pv_state = result['organism_analysis']['polyvagal_state']
        self.current_session['metrics']['polyvagal_states'][pv_state] += 1

        # Track knowledge retrieval
        if result.get('knowledge_context'):
            self.current_session['metrics']['knowledge_retrievals'] += 1

        # Update user state
        self._update_user_state(self.current_user, turn_recorded=True)

    def end_session(self, r_matrix_final: int) -> SessionMetrics:
        """
        End the current session and save to Bundle.

        Args:
            r_matrix_final: Final R-matrix update count

        Returns:
            SessionMetrics with session summary
        """
        if not self.current_session:
            raise RuntimeError("No active session to end.")

        # Finalize session
        self.current_session['end_time'] = datetime.now().isoformat()

        # Calculate R-matrix delta
        r_matrix_start = self.current_session.get('r_matrix_start', r_matrix_final)
        r_matrix_delta = r_matrix_final - r_matrix_start
        self.current_session['r_matrix_end'] = r_matrix_final
        self.current_session['r_matrix_delta'] = r_matrix_delta

        # Calculate average coherence
        coherences = self.current_session['metrics']['coherences']
        avg_coherence = sum(coherences) / len(coherences) if coherences else 0.0

        # Create metrics summary
        metrics = SessionMetrics(
            session_id=self.current_session['session_id'],
            user_id=self.current_session['user_id'],
            start_time=self.current_session['start_time'],
            end_time=self.current_session['end_time'],
            total_turns=self.current_session['metrics']['total_turns'],
            greetings=self.current_session['metrics']['greetings'],
            curiosity_triggers=self.current_session['metrics']['curiosity_triggers'],
            knowledge_retrievals=self.current_session['metrics']['knowledge_retrievals'],
            r_matrix_start=r_matrix_start,
            r_matrix_end=r_matrix_final,
            r_matrix_delta=r_matrix_delta,
            avg_coherence=avg_coherence,
            polyvagal_states=self.current_session['metrics']['polyvagal_states']
        )

        # Save session to Bundle
        self._save_session()

        # Update user state
        self._update_user_state(self.current_user, session_end=True)

        print(f"✅ Session ended: {self.current_session['session_id']}")
        print(f"   Total turns: {metrics.total_turns}")
        print(f"   Curiosity triggers: {metrics.curiosity_triggers}")
        print(f"   R-matrix growth: +{r_matrix_delta} updates")
        print(f"   Avg coherence: {avg_coherence:.3f}")

        # Clear current session
        session_id = self.current_session['session_id']
        self.current_session = None
        self.current_user = None

        return metrics

    def _save_session(self):
        """Save session to user's Bundle directory."""
        if not self.current_session:
            return

        user_id = self.current_session['user_id']
        session_id = self.current_session['session_id']

        # Create user directory if it doesn't exist
        user_dir = self.bundle_path / user_id / "conversations"
        user_dir.mkdir(parents=True, exist_ok=True)

        # Save session JSON
        session_file = user_dir / f"{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(self.current_session, f, indent=2)

    def _update_user_state(self, user_id: str,
                          session_start: bool = False,
                          session_end: bool = False,
                          turn_recorded: bool = False):
        """Update user state file in Bundle."""
        user_state_file = self.bundle_path / user_id / "user_state.json"

        # Load existing state
        if user_state_file.exists():
            with open(user_state_file, 'r') as f:
                state = json.load(f)
        else:
            state = {
                "user_id": user_id,
                "created": datetime.now().isoformat(),
                "total_conversations": 0,
                "total_turns": 0,
                "r_matrix_updates": 0,
                "last_active": None
            }

        # Update state
        if session_start:
            state['total_conversations'] += 1

        if turn_recorded:
            state['total_turns'] += 1

        state['last_active'] = datetime.now().isoformat()

        # Save state
        with open(user_state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def get_user_stats(self, user_id: str) -> Dict:
        """Get statistics for a specific user."""
        user_state_file = self.bundle_path / user_id / "user_state.json"

        if not user_state_file.exists():
            return {
                'error': f'User {user_id} not found',
                'user_id': user_id,
                'exists': False
            }

        with open(user_state_file, 'r') as f:
            state = json.load(f)

        # Get session history
        conversations_dir = self.bundle_path / user_id / "conversations"
        sessions = []
        if conversations_dir.exists():
            for session_file in sorted(conversations_dir.glob("*.json")):
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    sessions.append({
                        'session_id': session_data['session_id'],
                        'start_time': session_data['start_time'],
                        'turns': session_data['metrics']['total_turns'],
                        'curiosity_triggers': session_data['metrics']['curiosity_triggers']
                    })

        return {
            'user_id': user_id,
            'exists': True,
            'state': state,
            'total_sessions': len(sessions),
            'recent_sessions': sessions[-5:]  # Last 5 sessions
        }

    def print_session_summary(self, user_id: str):
        """Print formatted session summary for user."""
        stats = self.get_user_stats(user_id)

        if not stats['exists']:
            print(f"❌ User {user_id} not found")
            return

        print("\n" + "="*70)
        print(f"📊 SESSION SUMMARY: {user_id}")
        print("="*70)
        print(f"Created: {stats['state']['created']}")
        print(f"Last active: {stats['state']['last_active']}")
        print(f"Total conversations: {stats['state']['total_conversations']}")
        print(f"Total turns: {stats['state']['total_turns']}")
        print()

        if stats['recent_sessions']:
            print("Recent sessions:")
            for session in stats['recent_sessions']:
                print(f"  • {session['session_id']}: {session['turns']} turns, "
                      f"{session['curiosity_triggers']} curiosity triggers")

        print("="*70 + "\n")


# Convenience functions
def create_session_tracker(base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1") -> SessionTracker:
    """Create session tracker instance."""
    return SessionTracker(base_path)


if __name__ == "__main__":
    # Test session tracker
    tracker = create_session_tracker()

    # Start session
    session_id = tracker.start_session("user0")

    # Simulate some turns
    for i in range(3):
        result = {
            'timestamp': datetime.now().isoformat(),
            'organism_analysis': {
                'gate_decision': 'RESPOND' if i > 0 else 'GREETING',
                'polyvagal_state': 'ventral',
                'self_energy': 0.8
            },
            'knowledge_context': [{'source': 'test'}] if i > 0 else None,
            'conversational_organs': {
                'curiosity_triggered': i == 2,
                'r_matrix_updates': 10 + i,
                'organ_results': {
                    'LISTENING': type('obj', (object,), {'coherence': 0.7})(),
                    'EMPATHY': type('obj', (object,), {'coherence': 0.8})()
                }
            }
        }
        tracker.record_turn(f"Test input {i}", result, f"Test response {i}")

    # End session
    metrics = tracker.end_session(r_matrix_final=13)

    # Print stats
    tracker.print_session_summary("user0")

    print("✅ Session tracker operational")
