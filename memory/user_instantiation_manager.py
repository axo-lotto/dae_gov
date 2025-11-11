#!/usr/bin/env python3
"""
User Instantiation Manager - Multi-Tier Memory Architecture
=============================================================

Creates and manages unique DAE instantiations for each human.

Architecture:
- TIER 1: Session-specific state (ephemeral)
- TIER 2: User-specific full memory (persistent)
- TIER 3: Global organism memory (shared)

Each user gets:
- Unique token (identity)
- Isolated memory directory
- Personal transformation patterns
- Identity trajectory
- User-specific Hebbian R-matrix

Philosophy:
-----------
Whiteheadian nested actual occasions:
- Individual concrescence path (user instantiation)
- Participating in shared cosmic advance (global organism)

Author: DAE-GOV Development Team
Created: November 11, 2025
Version: 1.0 (Multi-Tier Memory Foundation)
"""

import json
import secrets
import hashlib
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class UserContext:
    """User-specific context (TIER 2 persistent memory)."""
    user_token: str
    human_name: str
    created_at: str
    total_sessions: int
    total_traces: int
    dominant_lure_history: list
    satisfaction_trajectory: list

    # Paths to user-specific files
    user_dir: str
    traces_dir: str
    transformation_patterns_path: str
    epoch_log_path: str
    hebbian_memory_path: str
    identity_trajectory_path: str
    neo4j_subgraph_path: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class UserInstantiationManager:
    """
    Manages DAE instantiations for individual humans.

    Responsibilities:
    - Generate unique user tokens
    - Create user directory structures
    - Initialize user-specific memory files
    - Register users in global registry
    - Load existing user contexts
    """

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize user instantiation manager.

        Args:
            base_path: Base path for DAE_HYPHAE_1, defaults to parent directory
        """
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = Path(base_path)

        # Ensure Bundle directory exists
        self.bundle_path = self.base_path / "Bundle"
        self.bundle_path.mkdir(parents=True, exist_ok=True)

        # Registry path
        self.registry_path = self.bundle_path / "user_registry.json"

        print("✅ User Instantiation Manager initialized")
        print(f"   Base path: {self.base_path}")
        print(f"   Bundle path: {self.bundle_path}")

    def generate_user_token(self, human_name: str) -> str:
        """
        Generate unique user token for DAE instantiation.

        Format: {name_slug}_{timestamp}_{random}
        Example: alice_wonderland_20251111_a3f9c2

        This token becomes the user's persistent identity across all sessions.

        Args:
            human_name: Human-readable name

        Returns:
            Unique user token string
        """
        # Normalize name to slug
        name_slug = human_name.lower()
        name_slug = ''.join(c if c.isalnum() else '_' for c in name_slug)
        name_slug = '_'.join(filter(None, name_slug.split('_')))  # Remove consecutive underscores

        # Timestamp for uniqueness
        timestamp = datetime.now().strftime('%Y%m%d')

        # Random component for security
        random_hex = secrets.token_hex(3)  # 6 characters

        user_token = f"{name_slug}_{timestamp}_{random_hex}"

        return user_token

    def create_user_instantiation(self, human_name: str) -> UserContext:
        """
        Create new user instantiation with full memory structure.

        Creates:
        - User directory (Bundle/user_{token}/)
        - Traces subdirectory
        - User-specific JSON files (patterns, epoch log, etc.)
        - User state file
        - Registry entry

        Args:
            human_name: Human-readable name for the user

        Returns:
            UserContext with paths and initial state
        """
        # Generate unique token
        user_token = self.generate_user_token(human_name)

        # Create user directory
        user_dir = self.bundle_path / f"user_{user_token}"
        traces_dir = user_dir / "traces"

        # Create directories
        traces_dir.mkdir(parents=True, exist_ok=True)

        # Define file paths
        transformation_patterns_path = user_dir / "transformation_patterns.json"
        epoch_log_path = user_dir / "epoch_training_log.json"
        hebbian_memory_path = user_dir / "user_hebbian_memory.json"
        identity_trajectory_path = user_dir / "identity_trajectory.json"
        neo4j_subgraph_path = user_dir / "neo4j_subgraph_export.json"

        # Initialize empty files
        self._init_transformation_patterns(transformation_patterns_path)
        self._init_epoch_log(epoch_log_path)
        self._init_hebbian_memory(hebbian_memory_path)
        self._init_identity_trajectory(identity_trajectory_path)

        # Create user context
        user_context = UserContext(
            user_token=user_token,
            human_name=human_name,
            created_at=datetime.now().isoformat(),
            total_sessions=0,
            total_traces=0,
            dominant_lure_history=[],
            satisfaction_trajectory=[],
            user_dir=str(user_dir),
            traces_dir=str(traces_dir),
            transformation_patterns_path=str(transformation_patterns_path),
            epoch_log_path=str(epoch_log_path),
            hebbian_memory_path=str(hebbian_memory_path),
            identity_trajectory_path=str(identity_trajectory_path),
            neo4j_subgraph_path=str(neo4j_subgraph_path)
        )

        # Save user state
        user_state_path = user_dir / "user_state.json"
        with open(user_state_path, 'w') as f:
            json.dump(user_context.to_dict(), f, indent=2)

        # Register in global registry
        self._register_user(user_context)

        print(f"\n✅ Created DAE instantiation for {human_name}")
        print(f"   User token: {user_token}")
        print(f"   User directory: {user_dir}")
        print(f"   Traces directory: {traces_dir}")
        print(f"\n   💾 Save this token for future sessions!")

        return user_context

    def load_user_context(self, user_token: str) -> UserContext:
        """
        Load existing user context from disk.

        Args:
            user_token: Unique user token

        Returns:
            UserContext loaded from user_state.json

        Raises:
            ValueError: If user not found
        """
        user_dir = self.bundle_path / f"user_{user_token}"
        user_state_path = user_dir / "user_state.json"

        if not user_state_path.exists():
            raise ValueError(
                f"User {user_token} not found.\n"
                f"   Expected path: {user_state_path}\n"
                f"   Create new instantiation first."
            )

        with open(user_state_path, 'r') as f:
            data = json.load(f)

        user_context = UserContext.from_dict(data)

        print(f"\n✅ Loaded user context for {user_context.human_name}")
        print(f"   User token: {user_token}")
        print(f"   Total sessions: {user_context.total_sessions}")
        print(f"   Total traces: {user_context.total_traces}")

        return user_context

    def list_users(self) -> Dict[str, dict]:
        """
        List all registered users.

        Returns:
            Dictionary mapping user_token → user info
        """
        if not self.registry_path.exists():
            return {}

        with open(self.registry_path, 'r') as f:
            registry = json.load(f)

        return registry

    def _register_user(self, user_context: UserContext):
        """
        Register user in global registry.

        Args:
            user_context: UserContext to register
        """
        registry = {}
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                registry = json.load(f)

        registry[user_context.user_token] = {
            "human_name": user_context.human_name,
            "user_dir": user_context.user_dir,
            "created_at": user_context.created_at,
            "total_sessions": user_context.total_sessions,
            "total_traces": user_context.total_traces
        }

        with open(self.registry_path, 'w') as f:
            json.dump(registry, f, indent=2)

        print(f"   ✅ Registered in global user registry")

    def _init_transformation_patterns(self, path: Path):
        """Initialize empty transformation patterns file."""
        initial_data = {
            "patterns": {},
            "last_updated": datetime.now().isoformat(),
            "description": "User-specific transformation patterns learned from felt state changes"
        }
        with open(path, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def _init_epoch_log(self, path: Path):
        """Initialize empty epoch training log."""
        initial_data = {
            "epochs": [],
            "last_epoch": 0,
            "description": "Progressive learning history from mycelium trace transformations"
        }
        with open(path, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def _init_hebbian_memory(self, path: Path):
        """Initialize empty user-specific Hebbian memory."""
        initial_data = {
            "r_matrix": {
                "LISTENING_EMPATHY": 0.0,
                "LISTENING_WISDOM": 0.0,
                "LISTENING_AUTHENTICITY": 0.0,
                "LISTENING_PRESENCE": 0.0,
                "EMPATHY_WISDOM": 0.0,
                "EMPATHY_AUTHENTICITY": 0.0,
                "EMPATHY_PRESENCE": 0.0,
                "WISDOM_AUTHENTICITY": 0.0,
                "WISDOM_PRESENCE": 0.0,
                "AUTHENTICITY_PRESENCE": 0.0
            },
            "value_mappings": {},
            "update_count": 0,
            "last_updated": datetime.now().isoformat(),
            "description": "User-specific Hebbian coupling patterns (which organs co-activate successfully)"
        }
        with open(path, 'w') as f:
            json.dump(initial_data, f, indent=2)

    def _init_identity_trajectory(self, path: Path):
        """Initialize empty identity trajectory."""
        initial_data = {
            "trajectory": [],
            "description": "How user's dominant lure and satisfaction evolve across sessions"
        }
        with open(path, 'w') as f:
            json.dump(initial_data, f, indent=2)


# Standalone test
if __name__ == "__main__":
    print("🌀 User Instantiation Manager - Test\n")

    manager = UserInstantiationManager()

    # Test 1: Create new user
    print("\n" + "="*70)
    print("TEST 1: Create new user instantiation")
    print("="*70)

    user_context = manager.create_user_instantiation("Alice Wonderland")

    print(f"\n   User token: {user_context.user_token}")
    print(f"   Created at: {user_context.created_at}")
    print(f"   User directory: {user_context.user_dir}")

    # Test 2: Load existing user
    print("\n" + "="*70)
    print("TEST 2: Load existing user")
    print("="*70)

    loaded_context = manager.load_user_context(user_context.user_token)

    assert loaded_context.user_token == user_context.user_token
    assert loaded_context.human_name == user_context.human_name

    print(f"\n   ✅ Successfully loaded {loaded_context.human_name}")

    # Test 3: List users
    print("\n" + "="*70)
    print("TEST 3: List all users")
    print("="*70)

    users = manager.list_users()

    print(f"\n   Total users: {len(users)}")
    for token, info in users.items():
        print(f"   - {info['human_name']} ({token[:30]}...)")

    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - User Instantiation Manager Operational")
    print("="*70 + "\n")
