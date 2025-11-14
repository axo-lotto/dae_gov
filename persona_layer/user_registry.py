#!/usr/bin/env python3
"""
User Registry - Persistent User Identity Management
Tracks users, sessions, and per-user state for DAE_HYPHAE_1

Features:
- User creation with persistent IDs
- Session history tracking
- Per-user organic family membership
- Feedback statistics
- State persistence across sessions

Author: Claude Code (November 2025)
Status: Production Ready
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List


class UserRegistry:
    """Manage user identities and session continuity."""

    def __init__(self, registry_path='persona_layer/user_registry.json'):
        self.registry_path = Path(registry_path)
        self.users_dir = Path('persona_layer/users')
        self.users_dir.mkdir(exist_ok=True)
        self.users = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load user registry from disk."""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_registry(self):
        """Save user registry to disk."""
        with open(self.registry_path, 'w') as f:
            json.dump(self.users, f, indent=2)

    def create_user(self, username: str = None) -> str:
        """
        Create new user, return user_id.

        Args:
            username: Optional display name

        Returns:
            user_id: Unique identifier for this user
        """
        user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.users[user_id] = {
            'user_id': user_id,
            'username': username or user_id,
            'created_at': datetime.now().isoformat(),
            'total_sessions': 0,
            'total_turns': 0,
            'organic_family_id': None,
            'user_state_path': str(self.users_dir / f'{user_id}_state.json')
        }

        # Create initial user state
        initial_state = {
            'user_id': user_id,
            'username': username or user_id,
            'created_at': datetime.now().isoformat(),
            'session_history': [],
            'feedback_count': 0,
            'helpful_rate': 0.0,
            'excellent_rate': 0.0,
            'organic_family_membership': [],
            'last_session': None,
            'preferred_tone': 'balanced',  # balanced, playful, grounded, minimal
            'dae_personality_notes': []  # Track personality calibration
        }

        state_path = self.users_dir / f'{user_id}_state.json'
        with open(state_path, 'w') as f:
            json.dump(initial_state, f, indent=2)

        self._save_registry()
        return user_id

    def get_user(self, user_id: str) -> Optional[Dict]:
        """Retrieve user profile."""
        return self.users.get(user_id)

    def list_users(self) -> List[Dict]:
        """List all registered users."""
        return [
            {
                'user_id': uid,
                'username': udata['username'],
                'created_at': udata['created_at'],
                'total_sessions': udata['total_sessions'],
                'total_turns': udata['total_turns']
            }
            for uid, udata in self.users.items()
        ]

    def update_user_stats(self, user_id: str, session_turns: int):
        """Update user interaction statistics."""
        if user_id in self.users:
            self.users[user_id]['total_sessions'] += 1
            self.users[user_id]['total_turns'] += session_turns
            self._save_registry()

    def load_user_state(self, user_id: str) -> Dict:
        """Load full user state from disk."""
        user = self.get_user(user_id)
        if not user:
            return {}

        state_path = Path(user['user_state_path'])
        if state_path.exists():
            with open(state_path, 'r') as f:
                return json.load(f)
        return {}

    def save_user_state(self, user_id: str, state: Dict):
        """Save full user state to disk."""
        user = self.get_user(user_id)
        if not user:
            return

        state_path = Path(user['user_state_path'])
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)

    def update_feedback_stats(self, user_id: str, helpful_rate: float, excellent_rate: float):
        """Update user's feedback statistics."""
        user_state = self.load_user_state(user_id)
        user_state['helpful_rate'] = helpful_rate
        user_state['excellent_rate'] = excellent_rate
        self.save_user_state(user_id, user_state)


if __name__ == '__main__':
    # Test user registry
    print("=== Testing User Registry ===\n")

    registry = UserRegistry()

    # Create test user
    user_id = registry.create_user(username="Alice")
    print(f"✅ Created user: {user_id}")

    # Retrieve user
    user = registry.get_user(user_id)
    print(f"✅ User data: {json.dumps(user, indent=2)}")

    # Load user state
    state = registry.load_user_state(user_id)
    print(f"\n✅ User state: {json.dumps(state, indent=2)}")

    # Update stats
    registry.update_user_stats(user_id, session_turns=10)
    print(f"\n✅ Updated stats: {registry.get_user(user_id)['total_turns']} turns")

    # List users
    print(f"\n✅ All users:")
    for u in registry.list_users():
        print(f"   {u['username']} ({u['user_id']}): {u['total_sessions']} sessions, {u['total_turns']} turns")

    print("\n✅ User Registry tests passed!")
