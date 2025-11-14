#!/usr/bin/env python3
"""
User Profile Manager
====================

Manages user-specific profiles, preferences, and conversation history for the DAE Companion system.
Each user gets their own folder with persistent preferences and conversation memory.

Architecture:
    user_profiles/
    └── {user_id}/
        ├── profile.json          # User preferences and metadata
        └── conversations/        # Conversation history
            ├── session_{id}.json
            └── ...

Date: November 12, 2025
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from config import Config


@dataclass
class UserProfile:
    """User profile with preferences and learning data."""

    user_id: str
    created_at: str
    last_active: str

    # User preferences (Level 9: Conversational Superject)
    response_length_preference: str = "moderate"  # "minimal", "moderate", "comprehensive"
    humor_tolerance: float = 0.5  # 0.0 (serious) to 1.0 (playful)
    small_talk_openness: float = 0.5  # 0.0 (direct) to 1.0 (casual)

    # LLM usage preferences
    llm_usage_consent: bool = False  # Explicit opt-in for LLM queries

    # Relationship metadata
    total_conversations: int = 0
    total_turns: int = 0

    # Template preferences (learned over time - Phase 2)
    favorite_templates: Dict[str, List[str]] = None  # {category: [template_ids]}
    template_success_rates: Dict[str, float] = None  # {template_id: success_rate}

    # Family affinity (learned from organic families - Phase 3)
    family_affinities: Dict[str, float] = None  # {family_id: affinity_score}

    # Inside jokes and callbacks (Level 9)
    inside_jokes: List[Dict[str, Any]] = None
    recurring_themes: Dict[str, int] = None  # {theme: occurrence_count}

    def __post_init__(self):
        """Initialize empty collections if None."""
        if self.favorite_templates is None:
            self.favorite_templates = {}
        if self.template_success_rates is None:
            self.template_success_rates = {}
        if self.family_affinities is None:
            self.family_affinities = {}
        if self.inside_jokes is None:
            self.inside_jokes = []
        if self.recurring_themes is None:
            self.recurring_themes = {}


@dataclass
class ConversationTurn:
    """Single turn in a conversation."""

    timestamp: str
    user_input: str
    dae_emission: str

    # Context snapshot
    zone: int
    ndam_urgency: float
    polyvagal_state: str
    active_organs: List[str]
    dominant_nexuses: List[str]

    # Persona layer metadata
    templates_used: List[str]
    query_type: str
    llm_queried: bool
    confidence: float

    # User feedback (for learning)
    user_satisfaction: Optional[float] = None  # 0.0 to 1.0, set later


class UserProfileManager:
    """
    Manages user profiles, preferences, and conversation history.

    Each user gets a persistent folder with:
    - profile.json (preferences, learning data)
    - conversations/ (session history)

    Responsibilities:
    - Load/save user profiles
    - Track conversation history
    - Update template success rates (Phase 2)
    - Learn user preferences over time
    - Manage relationship memory (callbacks, inside jokes)
    """

    def __init__(self):
        """Initialize UserProfileManager."""
        self.user_profiles_dir = Config.USER_PROFILES_DIR
        self.default_user_id = Config.DEFAULT_USER_ID

        # Ensure base directory exists
        self.user_profiles_dir.mkdir(parents=True, exist_ok=True)

        # Cache for loaded profiles (avoid repeated file I/O)
        self._profile_cache: Dict[str, UserProfile] = {}

    # ================================================================
    # USER PROFILE MANAGEMENT
    # ================================================================

    def get_or_create_profile(self, user_id: str = None) -> UserProfile:
        """
        Get existing user profile or create new one.

        Args:
            user_id: User identifier (default: Config.DEFAULT_USER_ID)

        Returns:
            UserProfile object
        """
        if user_id is None:
            user_id = self.default_user_id

        # Check cache first
        if user_id in self._profile_cache:
            return self._profile_cache[user_id]

        profile_path = self._get_profile_path(user_id)

        if profile_path.exists():
            # Load existing profile
            with open(profile_path, 'r') as f:
                data = json.load(f)

            profile = UserProfile(**data)

            # Update last active
            profile.last_active = datetime.now().isoformat()

        else:
            # Create new profile
            profile = UserProfile(
                user_id=user_id,
                created_at=datetime.now().isoformat(),
                last_active=datetime.now().isoformat(),
                response_length_preference=Config.DEFAULT_RESPONSE_LENGTH,
                humor_tolerance=Config.DEFAULT_HUMOR_TOLERANCE,
                small_talk_openness=Config.DEFAULT_SMALL_TALK_OPENNESS,
                llm_usage_consent=False  # Explicit opt-in required
            )

            # Create user directory
            user_dir = self._get_user_dir(user_id)
            user_dir.mkdir(parents=True, exist_ok=True)

            # Create conversations subdirectory
            (user_dir / "conversations").mkdir(exist_ok=True)

        # Cache and save
        self._profile_cache[user_id] = profile
        self._save_profile(profile)

        return profile

    def update_profile(self, profile: UserProfile):
        """
        Update user profile (both cache and disk).

        Args:
            profile: Updated UserProfile object
        """
        profile.last_active = datetime.now().isoformat()
        self._profile_cache[profile.user_id] = profile
        self._save_profile(profile)

    def _save_profile(self, profile: UserProfile):
        """Save profile to disk."""
        profile_path = self._get_profile_path(profile.user_id)

        with open(profile_path, 'w') as f:
            json.dump(asdict(profile), f, indent=2)

    def _get_user_dir(self, user_id: str) -> Path:
        """Get path to user's directory."""
        return self.user_profiles_dir / user_id

    def _get_profile_path(self, user_id: str) -> Path:
        """Get path to user's profile.json."""
        return self._get_user_dir(user_id) / "profile.json"

    # ================================================================
    # CONVERSATION HISTORY
    # ================================================================

    def save_conversation_turn(
        self,
        user_id: str,
        session_id: str,
        turn: ConversationTurn
    ):
        """
        Save a conversation turn to session history.

        Args:
            user_id: User identifier
            session_id: Session identifier
            turn: ConversationTurn object
        """
        session_path = self._get_session_path(user_id, session_id)

        # Load existing session or create new
        if session_path.exists():
            with open(session_path, 'r') as f:
                session_data = json.load(f)
        else:
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "started_at": datetime.now().isoformat(),
                "turns": []
            }

        # Append turn
        session_data["turns"].append(asdict(turn))
        session_data["last_updated"] = datetime.now().isoformat()

        # Save
        with open(session_path, 'w') as f:
            json.dump(session_data, f, indent=2)

        # Update profile turn count
        profile = self.get_or_create_profile(user_id)
        profile.total_turns += 1
        self.update_profile(profile)

    def get_conversation_history(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        max_turns: int = 10
    ) -> List[ConversationTurn]:
        """
        Get recent conversation history for context.

        Args:
            user_id: User identifier
            session_id: Session identifier (if None, get from most recent session)
            max_turns: Maximum number of turns to retrieve

        Returns:
            List of ConversationTurn objects (most recent first)
        """
        if session_id is None:
            # Get most recent session
            sessions = self._list_user_sessions(user_id)
            if not sessions:
                return []
            session_id = sessions[-1]  # Most recent

        session_path = self._get_session_path(user_id, session_id)

        if not session_path.exists():
            return []

        with open(session_path, 'r') as f:
            session_data = json.load(f)

        # Get recent turns
        turns_data = session_data.get("turns", [])[-max_turns:]

        # Convert to ConversationTurn objects
        turns = [ConversationTurn(**turn_data) for turn_data in turns_data]

        return turns

    def _get_session_path(self, user_id: str, session_id: str) -> Path:
        """Get path to session JSON file."""
        conversations_dir = self._get_user_dir(user_id) / "conversations"
        return conversations_dir / f"session_{session_id}.json"

    def _list_user_sessions(self, user_id: str) -> List[str]:
        """List all session IDs for a user (sorted chronologically)."""
        conversations_dir = self._get_user_dir(user_id) / "conversations"

        if not conversations_dir.exists():
            return []

        session_files = sorted(conversations_dir.glob("session_*.json"))

        # Extract session IDs
        session_ids = [
            f.stem.replace("session_", "")
            for f in session_files
        ]

        return session_ids

    # ================================================================
    # PHASE 2: TEMPLATE LEARNING
    # ================================================================

    def update_template_success(
        self,
        user_id: str,
        template_id: str,
        success: bool
    ):
        """
        Update template success rate for user (Phase 2 learning).

        Args:
            user_id: User identifier
            template_id: Template identifier
            success: Whether template was successful (user satisfaction > 0.7)
        """
        profile = self.get_or_create_profile(user_id)

        # Initialize if not exists
        if template_id not in profile.template_success_rates:
            profile.template_success_rates[template_id] = 0.5  # Neutral prior

        # Update with exponential moving average
        current_rate = profile.template_success_rates[template_id]
        alpha = 0.2  # Learning rate

        new_rate = (1 - alpha) * current_rate + alpha * (1.0 if success else 0.0)
        profile.template_success_rates[template_id] = new_rate

        self.update_profile(profile)

    def get_template_preferences(
        self,
        user_id: str,
        category: str,
        top_k: int = 5
    ) -> List[str]:
        """
        Get user's preferred templates for a category (Phase 2).

        Args:
            user_id: User identifier
            category: Template category
            top_k: Number of templates to return

        Returns:
            List of template IDs sorted by success rate
        """
        profile = self.get_or_create_profile(user_id)

        if not profile.template_success_rates:
            return []

        # Filter by category (template_id format: "category:template_name")
        category_templates = {
            tid: rate
            for tid, rate in profile.template_success_rates.items()
            if tid.startswith(f"{category}:")
        }

        # Sort by success rate
        sorted_templates = sorted(
            category_templates.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [tid for tid, _ in sorted_templates[:top_k]]

    # ================================================================
    # PHASE 3: FAMILY AFFINITY LEARNING
    # ================================================================

    def update_family_affinity(
        self,
        user_id: str,
        family_id: str,
        affinity_delta: float
    ):
        """
        Update user's affinity for an organic family (Phase 3).

        Args:
            user_id: User identifier
            family_id: Organic family identifier
            affinity_delta: Change in affinity (-1.0 to 1.0)
        """
        profile = self.get_or_create_profile(user_id)

        # Initialize if not exists
        if family_id not in profile.family_affinities:
            profile.family_affinities[family_id] = 0.5  # Neutral prior

        # Update (clamped to [0, 1])
        current_affinity = profile.family_affinities[family_id]
        new_affinity = max(0.0, min(1.0, current_affinity + affinity_delta * 0.1))

        profile.family_affinities[family_id] = new_affinity

        self.update_profile(profile)

    def get_preferred_families(
        self,
        user_id: str,
        top_k: int = 3
    ) -> List[str]:
        """
        Get user's preferred organic families (Phase 3).

        Args:
            user_id: User identifier
            top_k: Number of families to return

        Returns:
            List of family IDs sorted by affinity
        """
        profile = self.get_or_create_profile(user_id)

        if not profile.family_affinities:
            return []

        sorted_families = sorted(
            profile.family_affinities.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [fid for fid, _ in sorted_families[:top_k]]

    # ================================================================
    # LEVEL 9: RELATIONSHIP MEMORY (CALLBACKS, INSIDE JOKES)
    # ================================================================

    def add_recurring_theme(self, user_id: str, theme: str):
        """
        Track recurring theme in user's conversations.

        Args:
            user_id: User identifier
            theme: Theme identifier (e.g., "work_burnout", "creative_blocks")
        """
        profile = self.get_or_create_profile(user_id)

        if theme not in profile.recurring_themes:
            profile.recurring_themes[theme] = 0

        profile.recurring_themes[theme] += 1

        self.update_profile(profile)

    def add_inside_joke(
        self,
        user_id: str,
        joke_text: str,
        context: str,
        session_id: str
    ):
        """
        Add an inside joke to user's relationship memory.

        Args:
            user_id: User identifier
            joke_text: The joke or callback text
            context: Contextual explanation
            session_id: Session where joke originated
        """
        profile = self.get_or_create_profile(user_id)

        inside_joke = {
            "joke": joke_text,
            "context": context,
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "times_referenced": 0
        }

        profile.inside_jokes.append(inside_joke)

        self.update_profile(profile)

    def get_inside_jokes(self, user_id: str, max_count: int = 5) -> List[Dict]:
        """
        Get user's inside jokes (most frequently referenced first).

        Args:
            user_id: User identifier
            max_count: Maximum number to return

        Returns:
            List of inside joke dictionaries
        """
        profile = self.get_or_create_profile(user_id)

        # Sort by times_referenced
        sorted_jokes = sorted(
            profile.inside_jokes,
            key=lambda j: j.get("times_referenced", 0),
            reverse=True
        )

        return sorted_jokes[:max_count]

    # ================================================================
    # STATISTICS & REPORTING
    # ================================================================

    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics about user's interaction with DAE.

        Args:
            user_id: User identifier

        Returns:
            Dictionary with user statistics
        """
        profile = self.get_or_create_profile(user_id)

        return {
            "user_id": profile.user_id,
            "created_at": profile.created_at,
            "last_active": profile.last_active,
            "total_conversations": profile.total_conversations,
            "total_turns": profile.total_turns,
            "response_length_preference": profile.response_length_preference,
            "humor_tolerance": profile.humor_tolerance,
            "small_talk_openness": profile.small_talk_openness,
            "llm_usage_consent": profile.llm_usage_consent,
            "learned_template_preferences": len(profile.template_success_rates),
            "family_affinities": len(profile.family_affinities),
            "inside_jokes": len(profile.inside_jokes),
            "recurring_themes": len(profile.recurring_themes)
        }


# ================================================================
# CONVENIENCE FUNCTIONS
# ================================================================

def get_default_profile() -> UserProfile:
    """Get or create profile for default user."""
    manager = UserProfileManager()
    return manager.get_or_create_profile()


def save_turn(session_id: str, turn: ConversationTurn, user_id: str = None):
    """Save conversation turn for default or specified user."""
    manager = UserProfileManager()
    if user_id is None:
        user_id = Config.DEFAULT_USER_ID
    manager.save_conversation_turn(user_id, session_id, turn)


def get_recent_history(max_turns: int = 10, user_id: str = None) -> List[ConversationTurn]:
    """Get recent conversation history for default or specified user."""
    manager = UserProfileManager()
    if user_id is None:
        user_id = Config.DEFAULT_USER_ID
    return manager.get_conversation_history(user_id, max_turns=max_turns)
