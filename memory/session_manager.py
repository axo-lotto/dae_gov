#!/usr/bin/env python3
"""
Session Manager - Multi-Tier Memory Session Lifecycle
======================================================

Manages DAE session initialization and termination with memory propagation.

Flow:
- INIT: Load TIER 2 (user) → Create TIER 1 (session) → Prehend TIER 3 (global)
- TERMINATE: Save TIER 1 artifacts → Propagate to TIER 2 → Contribute to TIER 3

Philosophy:
-----------
Each session is an ephemeral actual occasion that:
1. Prehends the user's persistent memory (TIER 2)
2. Prehends the global organism's wisdom (TIER 3)
3. Creates novel experience (TIER 1)
4. Perishes into objectivity (contributes back to TIER 2 & 3)

Author: DAE-GOV Development Team
Created: November 11, 2025
Version: 1.0 (Session Lifecycle Management)
"""

import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from memory.user_instantiation_manager import UserInstantiationManager, UserContext


@dataclass
class SessionContext:
    """
    Session-specific context (TIER 1 ephemeral state).

    This represents the actual occasion of THIS conversation.
    """
    session_id: str
    user_token: str
    human_name: str
    started_at: str

    # TIER 1: Ephemeral session state
    session_dir: str
    conversation_history: list
    felt_state_trajectory: list
    polyvagal_arc: list
    kairos_moments: list
    traces_created: list

    # TIER 2: User memory (loaded, read-only during session)
    user_context: dict
    user_patterns: dict
    user_hebbian: dict
    identity_trajectory: list
    total_sessions: int
    total_traces: int

    # TIER 3: Global organism (prehended, read-only)
    global_organism: dict

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class SessionManager:
    """
    Manages session lifecycle with multi-tier memory integration.

    Responsibilities:
    - Initialize sessions (load TIER 2, create TIER 1, prehend TIER 3)
    - Terminate sessions (save TIER 1, propagate to TIER 2 & 3)
    - Track active sessions
    - Manage session artifacts
    """

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize session manager.

        Args:
            base_path: Base path for DAE_HYPHAE_1
        """
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = Path(base_path)

        # Initialize user manager
        self.user_manager = UserInstantiationManager(base_path=self.base_path)

        # Paths
        self.sessions_path = self.base_path / "sessions"
        self.sessions_path.mkdir(parents=True, exist_ok=True)

        self.tsk_path = self.base_path / "TSK"
        self.tsk_path.mkdir(parents=True, exist_ok=True)

        self.session_registry_path = self.sessions_path / "session_registry.json"

        print("✅ Session Manager initialized")
        print(f"   Sessions directory: {self.sessions_path}")

    def initialize_session(self, user_token: str) -> SessionContext:
        """
        Initialize new session for existing user.

        Loads TIER 2 (user full memory) into TIER 1 (session state).
        Prehends TIER 3 (global organism) for context.

        Args:
            user_token: Unique user token

        Returns:
            SessionContext with all loaded memories

        Raises:
            ValueError: If user not found
        """
        # Load user context (TIER 2)
        user_context = self.user_manager.load_user_context(user_token)

        # Create session ID and directory (TIER 1)
        session_id = f"session_{user_token}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_dir = self.sessions_path / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        # Load global organism state (TIER 3)
        global_state = self._load_global_organism()

        # Load user transformation patterns (TIER 2)
        patterns_path = Path(user_context.transformation_patterns_path)
        user_patterns = {"patterns": {}}
        if patterns_path.exists():
            with open(patterns_path, 'r') as f:
                user_patterns = json.load(f)

        # Load user Hebbian memory (TIER 2)
        hebbian_path = Path(user_context.hebbian_memory_path)
        user_hebbian = {"r_matrix": {}, "value_mappings": {}, "update_count": 0}
        if hebbian_path.exists():
            with open(hebbian_path, 'r') as f:
                user_hebbian = json.load(f)

        # Load identity trajectory (TIER 2)
        identity_path = Path(user_context.identity_trajectory_path)
        identity_trajectory = {"trajectory": []}
        if identity_path.exists():
            with open(identity_path, 'r') as f:
                identity_trajectory = json.load(f)

        # Increment session count BEFORE creating session context
        incremented_sessions = user_context.total_sessions + 1

        # Synthesize session context
        session_context = SessionContext(
            session_id=session_id,
            user_token=user_token,
            human_name=user_context.human_name,
            started_at=datetime.now().isoformat(),

            # TIER 1: Session state (ephemeral)
            session_dir=str(session_dir),
            conversation_history=[],
            felt_state_trajectory=[],
            polyvagal_arc=[],
            kairos_moments=[],
            traces_created=[],

            # TIER 2: User memory (loaded)
            user_context=user_context.to_dict(),
            user_patterns=user_patterns,
            user_hebbian=user_hebbian,
            identity_trajectory=identity_trajectory.get('trajectory', []),
            total_sessions=incremented_sessions,  # Use incremented value
            total_traces=user_context.total_traces,

            # TIER 3: Global organism (prehended)
            global_organism={
                "confidence": global_state.get('global_confidence', 0.0),
                "total_successes": global_state.get('total_successes', 0),
                "success_rate": global_state.get('success_rate', 0.0),
                "archetypal_lure_distribution": global_state.get('archetypal_lure_distribution', {})
            }
        )

        # Update user session count in file (TIER 2)
        user_state_path = Path(user_context.user_dir) / "user_state.json"
        user_data = user_context.to_dict()
        user_data['total_sessions'] = incremented_sessions
        with open(user_state_path, 'w') as f:
            json.dump(user_data, f, indent=2)

        # Register session
        self._register_session(session_context)

        print(f"\n🌀 Session initialized for {user_context.human_name}")
        print(f"   Session ID: {session_id}")
        print(f"   Total sessions: {incremented_sessions}")
        print(f"   Total traces: {user_context.total_traces}")
        print(f"   Global organism confidence: {session_context.global_organism['confidence']:.3f}")

        return session_context

    def terminate_session(self, session_context: SessionContext) -> Dict:
        """
        Terminate session and propagate learning to TIER 2 and TIER 3.

        Flow:
        1. Save session artifacts (TIER 1 → disk)
        2. Extract transformation patterns (TIER 1 → TIER 2)
        3. Update user Hebbian memory (TIER 1 → TIER 2)
        4. Update identity trajectory (TIER 1 → TIER 2)
        5. Contribute to global organism (TIER 2 → TIER 3)

        Args:
            session_context: Current session context

        Returns:
            Session summary dictionary
        """
        session_dir = Path(session_context.session_dir)

        print(f"\n💾 Terminating session: {session_context.session_id}")

        # 1. Save session artifacts (TIER 1)
        self._save_session_artifacts(session_context)

        # 2-4. Propagate to user memory (TIER 1 → TIER 2)
        patterns_learned = self._propagate_to_user_memory(session_context)

        # 5. Contribute to global organism (TIER 2 → TIER 3)
        self._contribute_to_global_organism(session_context)

        # Generate session summary
        duration = self._calculate_duration(session_context)
        summary = {
            "session_id": session_context.session_id,
            "human_name": session_context.human_name,
            "duration": duration,
            "turns": len(session_context.conversation_history),
            "traces_created": len(session_context.traces_created),
            "kairos_moments": len(session_context.kairos_moments),
            "patterns_learned": patterns_learned,
            "final_satisfaction": session_context.felt_state_trajectory[-1].get('satisfaction', 0.5) if session_context.felt_state_trajectory else 0.5,
            "ended_at": datetime.now().isoformat()
        }

        print(f"\n✅ Session terminated")
        print(f"   Duration: {summary['duration']}")
        print(f"   Turns: {summary['turns']}")
        print(f"   Kairos moments: {summary['kairos_moments']}")
        print(f"   Patterns learned: {summary['patterns_learned']}")

        return summary

    def _load_global_organism(self) -> Dict:
        """Load global organism state (TIER 3)."""
        global_state_path = self.tsk_path / "global_organism_state.json"

        if not global_state_path.exists():
            # Initialize if not exists
            default_state = {
                "global_confidence": 0.0,
                "total_successes": 0,
                "total_sessions": 0,
                "success_rate": 0.0,
                "archetypal_lure_distribution": {},
                "universal_transformation_patterns": {},
                "collective_hebbian_memory": {},
                "created_at": datetime.now().isoformat()
            }
            with open(global_state_path, 'w') as f:
                json.dump(default_state, f, indent=2)
            return default_state

        with open(global_state_path, 'r') as f:
            return json.load(f)

    def _save_session_artifacts(self, session_context: SessionContext):
        """Save TIER 1 artifacts to disk."""
        session_dir = Path(session_context.session_dir)

        artifacts = {
            "conversation_history.json": session_context.conversation_history,
            "felt_state_trajectory.json": session_context.felt_state_trajectory,
            "polyvagal_arc.json": session_context.polyvagal_arc,
            "kairos_moments.json": session_context.kairos_moments,
            "traces_created.json": session_context.traces_created,
            "session_summary.json": {
                "session_id": session_context.session_id,
                "user_token": session_context.user_token,
                "human_name": session_context.human_name,
                "started_at": session_context.started_at,
                "ended_at": datetime.now().isoformat()
            }
        }

        for filename, data in artifacts.items():
            filepath = session_dir / filename
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

        print(f"   ✓ Saved session artifacts to {session_dir}")

    def _propagate_to_user_memory(self, session_context: SessionContext) -> int:
        """Propagate learning from TIER 1 to TIER 2."""
        patterns_learned = 0

        # Update identity trajectory
        if session_context.felt_state_trajectory:
            final_felt = session_context.felt_state_trajectory[-1]
            identity_snapshot = {
                "timestamp": datetime.now().isoformat(),
                "session_id": session_context.session_id,
                "satisfaction": final_felt.get('satisfaction', 0.5),
                "energy": final_felt.get('energy', 0.5),
                "dominant_lure": final_felt.get('dominant_lure', 'unknown'),
                "kairos_count": len(session_context.kairos_moments)
            }

            identity_path = Path(session_context.user_context['identity_trajectory_path'])
            trajectory = {"trajectory": session_context.identity_trajectory}
            trajectory["trajectory"].append(identity_snapshot)

            with open(identity_path, 'w') as f:
                json.dump(trajectory, f, indent=2)

            print(f"   ✓ Updated identity trajectory")

        # Update user state
        user_state_path = Path(session_context.user_context['user_dir']) / "user_state.json"
        with open(user_state_path, 'r') as f:
            user_data = json.load(f)

        user_data['total_traces'] += len(session_context.traces_created)

        with open(user_state_path, 'w') as f:
            json.dump(user_data, f, indent=2)

        return patterns_learned

    def _contribute_to_global_organism(self, session_context: SessionContext):
        """Contribute session learning to global organism (TIER 3)."""
        global_state_path = self.tsk_path / "global_organism_state.json"

        with open(global_state_path, 'r') as f:
            global_state = json.load(f)

        # Update session count
        global_state['total_sessions'] = global_state.get('total_sessions', 0) + 1

        # Update success count if satisfying
        if session_context.felt_state_trajectory:
            final_satisfaction = session_context.felt_state_trajectory[-1].get('satisfaction', 0.0)
            if final_satisfaction > 0.7:
                global_state['total_successes'] = global_state.get('total_successes', 0) + 1

        # Recalculate success rate
        total = global_state['total_sessions']
        if total > 0:
            global_state['success_rate'] = global_state['total_successes'] / total

            # Update global confidence
            if global_state['success_rate'] > 0.45:
                global_state['global_confidence'] = min(1.0, 0.5 + (global_state['success_rate'] - 0.45) * 2)
            else:
                global_state['global_confidence'] = global_state['success_rate'] * 1.1

        with open(global_state_path, 'w') as f:
            json.dump(global_state, f, indent=2)

        print(f"   ✓ Contributed to global organism (confidence: {global_state['global_confidence']:.3f})")

    def _register_session(self, session_context: SessionContext):
        """Register session in registry."""
        registry = {}
        if self.session_registry_path.exists():
            with open(self.session_registry_path, 'r') as f:
                registry = json.load(f)

        registry[session_context.session_id] = {
            "user_token": session_context.user_token,
            "human_name": session_context.human_name,
            "started_at": session_context.started_at,
            "session_dir": session_context.session_dir
        }

        with open(self.session_registry_path, 'w') as f:
            json.dump(registry, f, indent=2)

    def _calculate_duration(self, session_context: SessionContext) -> str:
        """Calculate session duration."""
        start = datetime.fromisoformat(session_context.started_at)
        end = datetime.now()
        duration = end - start

        minutes = int(duration.total_seconds() / 60)
        seconds = int(duration.total_seconds() % 60)

        return f"{minutes}m {seconds}s"


# Standalone test
if __name__ == "__main__":
    print("🌀 Session Manager - Test\n")

    manager = SessionManager()

    # Test 1: Create test user
    print("\n" + "="*70)
    print("TEST 1: Create test user")
    print("="*70)

    user_context = manager.user_manager.create_user_instantiation("Test User")

    # Test 2: Initialize session
    print("\n" + "="*70)
    print("TEST 2: Initialize session")
    print("="*70)

    session_context = manager.initialize_session(user_context.user_token)

    assert session_context.user_token == user_context.user_token
    assert session_context.human_name == user_context.human_name
    assert session_context.total_sessions == 1

    print(f"\n   ✅ Session initialized: {session_context.session_id}")

    # Test 3: Simulate conversation
    print("\n" + "="*70)
    print("TEST 3: Simulate conversation")
    print("="*70)

    session_context.conversation_history.append({
        "turn": 1,
        "user": "Hello DAE!",
        "assistant": "Hello! Welcome to our conversation.",
        "timestamp": datetime.now().isoformat()
    })

    session_context.felt_state_trajectory.append({
        "timestamp": datetime.now().isoformat(),
        "satisfaction": 0.8,
        "energy": 0.6,
        "dominant_lure": "connection"
    })

    print(f"   Added 1 conversation turn")
    print(f"   Final satisfaction: 0.8")

    # Test 4: Terminate session
    print("\n" + "="*70)
    print("TEST 4: Terminate session")
    print("="*70)

    summary = manager.terminate_session(session_context)

    print(f"\n   Session summary:")
    print(f"   - Duration: {summary['duration']}")
    print(f"   - Turns: {summary['turns']}")
    print(f"   - Final satisfaction: {summary['final_satisfaction']}")

    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - Session Manager Operational")
    print("="*70 + "\n")
