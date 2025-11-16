#!/usr/bin/env python3
"""
Session Turn Manager - USER:SESSION:TURN Identity Hierarchy
=============================================================

Manages the lifecycle of conversation sessions and turns within the DAE system.
Enables temporal entity tracking across USER → SESSION → TURN hierarchy.

Core Responsibilities:
1. Create and manage conversation sessions
2. Track turns within sessions with full entity context
3. Update session-level patterns (polyvagal trajectory, entity evolution)
4. Classify sessions (crisis, breakthrough, therapeutic)
5. Persist session data to user profiles

Philosophy:
- Sessions are containers for temporal context
- Turns capture the moment-to-moment entity prehension
- Entity mentions are linked to temporal context (WHEN mentioned)
- "Emma in crisis session" vs "Emma in joy session" = different contexts

Date: November 16, 2025
Phase: USER:SESSION:TURN Hierarchy Implementation (Phase 2)
"""

from dataclasses import asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from persona_layer.superject_structures import (
    ConversationSession,
    ConversationTurn,
    EnhancedUserProfile,
    FeltStateSnapshot,
)


class SessionTurnManager:
    """
    Manages conversation sessions and turns for temporal entity tracking.

    Key Features:
    - Session lifecycle management (start, add_turn, end)
    - Turn-level entity context preservation
    - Session-level pattern tracking (polyvagal, entity evolution)
    - Session classification (crisis, breakthrough, therapeutic)
    - Integration with EnhancedUserProfile for persistence
    """

    def __init__(self, storage_dir: str = "persona_layer/users"):
        """Initialize session manager."""
        self.storage_dir = storage_dir
        self.active_sessions: Dict[str, ConversationSession] = {}

    def start_session(self, user_id: str) -> ConversationSession:
        """
        Start a new conversation session for a user.

        Args:
            user_id: User identifier

        Returns:
            New ConversationSession instance
        """
        timestamp = datetime.utcnow().isoformat()
        session_id = f"{user_id}_session_{timestamp.replace(':', '-').replace('.', '-')}"

        session = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            start_time=timestamp,
            end_time=None,
            turns=[],
            session_entities={},
            entity_mentions_timeline=[],
            entity_mood_evolution={},
            polyvagal_trajectory=[],
            zone_trajectory=[],
            v0_trajectory=[],
            mean_satisfaction=0.0,
            satisfaction_trend="initializing",
            total_turns=0,
            dominant_themes=[],
            recurring_nexuses=[],
            organ_participation_summary={},
            ended_naturally=False,
            crisis_session=False,
            breakthrough_session=False,
            patterns_learned=0,
            family_assignments=[]
        )

        # Cache active session
        self.active_sessions[user_id] = session

        return session

    def get_current_session(self, user_id: str) -> Optional[ConversationSession]:
        """
        Get the current active session for a user.

        Args:
            user_id: User identifier

        Returns:
            Active ConversationSession or None
        """
        return self.active_sessions.get(user_id)

    def get_or_create_session(self, user_id: str, restore_from_disk: bool = True) -> ConversationSession:
        """
        Get existing session or create new one.

        If restore_from_disk is True, will attempt to restore any active session
        from disk before creating a new one.

        Args:
            user_id: User identifier
            restore_from_disk: Whether to check for active sessions on disk

        Returns:
            ConversationSession (existing or new)
        """
        # Check in-memory cache first
        session = self.get_current_session(user_id)
        if session is not None:
            return session

        # Try to restore from disk if enabled
        if restore_from_disk:
            session = self.restore_active_session(user_id)
            if session is not None:
                return session

        # Create new session
        session = self.start_session(user_id)
        return session

    def create_turn(
        self,
        session: ConversationSession,
        user_input: str,
        dae_response: str,
        entity_prehension: Optional[Dict[str, Any]] = None,
        felt_state: Optional[FeltStateSnapshot] = None,
        processing_time_ms: float = 0.0,
        emission_strategy: Optional[str] = None,
        user_satisfaction: Optional[float] = None
    ) -> ConversationTurn:
        """
        Create a new turn within a session.

        Args:
            session: Parent session
            user_input: User's message
            dae_response: DAE's emission
            entity_prehension: Pre-emission entity retrieval result
            felt_state: Full TSK capture for this turn
            processing_time_ms: Processing time
            emission_strategy: Strategy used ("direct", "fusion", "fallback")
            user_satisfaction: Optional satisfaction score (0-1)

        Returns:
            New ConversationTurn instance
        """
        turn_number = len(session.turns) + 1
        timestamp = datetime.utcnow().isoformat()

        # Extract entity context from prehension
        mentioned_entities = []
        entity_references = []
        relational_query = False
        implicit_references = []

        if entity_prehension:
            mentioned_entities = [
                e.get('name', '') for e in entity_prehension.get('mentioned_entities', [])
            ]
            entity_references = entity_prehension.get('entity_references', [])
            relational_query = entity_prehension.get('relational_query_detected', False)
            implicit_references = entity_prehension.get('implicit_references', [])

        # Create turn
        turn = ConversationTurn(
            turn_id=f"{session.user_id}_session_{session.session_id}_turn_{turn_number}",
            turn_number=turn_number,
            session_id=session.session_id,
            user_id=session.user_id,
            timestamp=timestamp,
            user_input=user_input,
            dae_response=dae_response,
            response_length=len(dae_response),
            entity_prehension=entity_prehension or {},
            mentioned_entities=mentioned_entities,
            entity_references=entity_references,
            relational_query=relational_query,
            implicit_references=implicit_references,
            felt_state=felt_state,
            user_satisfaction=user_satisfaction,
            user_continued=True,  # Will be updated if no follow-up
            turn_success=None,  # Can be set later
            processing_time_ms=processing_time_ms,
            emission_strategy=emission_strategy
        )

        return turn

    def add_turn(
        self,
        session: ConversationSession,
        turn: ConversationTurn,
        auto_save: bool = True
    ) -> None:
        """
        Add a turn to the session and update session-level tracking.

        Args:
            session: Parent session
            turn: Turn to add
            auto_save: Whether to automatically save session to disk after adding turn
        """
        # Add turn to session
        session.turns.append(turn)
        session.total_turns = len(session.turns)

        # Update entity timeline
        self._update_entity_timeline(session, turn)

        # Update polyvagal trajectory
        self._update_polyvagal_trajectory(session, turn)

        # Update zone trajectory
        self._update_zone_trajectory(session, turn)

        # Update V0 trajectory
        self._update_v0_trajectory(session, turn)

        # Update satisfaction tracking
        self._update_satisfaction_tracking(session, turn)

        # Update organ participation summary
        self._update_organ_participation(session, turn)

        # Check for session classification updates
        self._update_session_classification(session)

        # Auto-save to disk for crash recovery
        if auto_save:
            self.auto_save_session(session)

    def _update_entity_timeline(
        self,
        session: ConversationSession,
        turn: ConversationTurn
    ) -> None:
        """
        Update session's entity mention timeline.

        Tracks WHEN entities are mentioned and in what context.
        """
        if not turn.mentioned_entities:
            return

        # Get emotional context from felt state
        emotional_context = "neutral"
        if turn.felt_state:
            # Determine dominant emotional context
            if hasattr(turn.felt_state, 'polyvagal_state'):
                emotional_context = turn.felt_state.polyvagal_state or "neutral"

        # Add to timeline
        for entity_name in turn.mentioned_entities:
            timeline_entry = {
                "turn": turn.turn_number,
                "entity": entity_name,
                "context": emotional_context,
                "timestamp": turn.timestamp,
                "relational_query": turn.relational_query
            }
            session.entity_mentions_timeline.append(timeline_entry)

            # Update entity mood evolution
            if entity_name not in session.entity_mood_evolution:
                session.entity_mood_evolution[entity_name] = []
            session.entity_mood_evolution[entity_name].append(emotional_context)

            # Update session entities count
            if entity_name not in session.session_entities:
                session.session_entities[entity_name] = {
                    "mention_count": 0,
                    "first_mention_turn": turn.turn_number,
                    "last_mention_turn": turn.turn_number,
                    "contexts": []
                }
            session.session_entities[entity_name]["mention_count"] += 1
            session.session_entities[entity_name]["last_mention_turn"] = turn.turn_number
            session.session_entities[entity_name]["contexts"].append(emotional_context)

    def _update_polyvagal_trajectory(
        self,
        session: ConversationSession,
        turn: ConversationTurn
    ) -> None:
        """
        Update session's polyvagal state trajectory.

        Tracks ventral/sympathetic/dorsal patterns over turns.
        """
        polyvagal_state = "unknown"
        if turn.felt_state and hasattr(turn.felt_state, 'polyvagal_state'):
            polyvagal_state = turn.felt_state.polyvagal_state or "unknown"

        session.polyvagal_trajectory.append(polyvagal_state)

    def _update_zone_trajectory(
        self,
        session: ConversationSession,
        turn: ConversationTurn
    ) -> None:
        """
        Update session's zone trajectory.

        Tracks movement through zones 1-5 (or 1-7).
        """
        zone = 3  # Default to middle zone
        if turn.felt_state and hasattr(turn.felt_state, 'zone'):
            zone = turn.felt_state.zone or 3

        session.zone_trajectory.append(zone)

    def _update_v0_trajectory(
        self,
        session: ConversationSession,
        turn: ConversationTurn
    ) -> None:
        """
        Update session's V0 energy trajectory.

        Tracks energy convergence patterns over turns.
        """
        v0_value = 0.5  # Default neutral
        if turn.felt_state and hasattr(turn.felt_state, 'v0_energy'):
            v0_value = turn.felt_state.v0_energy or 0.5

        session.v0_trajectory.append(v0_value)

    def _update_satisfaction_tracking(
        self,
        session: ConversationSession,
        turn: ConversationTurn
    ) -> None:
        """
        Update session's satisfaction metrics.

        Calculates mean satisfaction and trend.
        """
        if turn.user_satisfaction is not None:
            # Calculate new mean
            total_satisfaction = sum(
                t.user_satisfaction for t in session.turns
                if t.user_satisfaction is not None
            )
            count = sum(
                1 for t in session.turns
                if t.user_satisfaction is not None
            )
            session.mean_satisfaction = total_satisfaction / count if count > 0 else 0.0

            # Calculate trend (last 3 turns)
            recent_satisfactions = [
                t.user_satisfaction for t in session.turns[-3:]
                if t.user_satisfaction is not None
            ]

            if len(recent_satisfactions) >= 2:
                diff = recent_satisfactions[-1] - recent_satisfactions[0]
                if diff > 0.1:
                    session.satisfaction_trend = "improving"
                elif diff < -0.1:
                    session.satisfaction_trend = "declining"
                elif max(recent_satisfactions) - min(recent_satisfactions) > 0.3:
                    session.satisfaction_trend = "volatile"
                else:
                    session.satisfaction_trend = "stable"
            else:
                session.satisfaction_trend = "initializing"

    def _update_organ_participation(
        self,
        session: ConversationSession,
        turn: ConversationTurn
    ) -> None:
        """
        Update session's organ participation summary.

        Tracks which organs were active across turns.
        """
        if turn.felt_state and hasattr(turn.felt_state, 'organ_activations'):
            organ_activations = turn.felt_state.organ_activations or {}

            for organ_name, activation in organ_activations.items():
                if organ_name not in session.organ_participation_summary:
                    session.organ_participation_summary[organ_name] = []
                session.organ_participation_summary[organ_name].append(activation)

    def _update_session_classification(
        self,
        session: ConversationSession
    ) -> None:
        """
        Update session classification (crisis, breakthrough, etc).

        Based on patterns in polyvagal trajectory and satisfaction.
        """
        # Crisis session detection
        # - Multiple sympathetic states
        # - High urgency indicators
        # - Declining satisfaction
        sympathetic_count = sum(
            1 for state in session.polyvagal_trajectory
            if "sympathetic" in str(state).lower()
        )
        dorsal_count = sum(
            1 for state in session.polyvagal_trajectory
            if "dorsal" in str(state).lower()
        )

        total_turns = len(session.polyvagal_trajectory)
        if total_turns > 0:
            crisis_ratio = (sympathetic_count + dorsal_count) / total_turns
            if crisis_ratio > 0.5 or session.satisfaction_trend == "declining":
                session.crisis_session = True

        # Breakthrough session detection
        # - High satisfaction (>0.8)
        # - Improving trend
        # - Movement to ventral state
        if session.mean_satisfaction > 0.8 and session.satisfaction_trend == "improving":
            if session.polyvagal_trajectory and "ventral" in str(session.polyvagal_trajectory[-1]).lower():
                session.breakthrough_session = True

    def end_session(
        self,
        session: ConversationSession,
        ended_naturally: bool = True
    ) -> None:
        """
        End a session and finalize metrics.

        Args:
            session: Session to end
            ended_naturally: Whether user said goodbye vs timeout
        """
        session.end_time = datetime.utcnow().isoformat()
        session.ended_naturally = ended_naturally

        # Mark last turn as not continued (session ended)
        if session.turns:
            session.turns[-1].user_continued = False

        # Compute final organ participation averages
        for organ_name, activations in session.organ_participation_summary.items():
            if activations:
                session.organ_participation_summary[organ_name] = sum(activations) / len(activations)

        # Remove from active sessions
        if session.user_id in self.active_sessions:
            del self.active_sessions[session.user_id]

    def save_session_to_profile(
        self,
        session: ConversationSession,
        profile: EnhancedUserProfile
    ) -> None:
        """
        Save completed session to user profile.

        Args:
            session: Session to save
            profile: User's profile
        """
        # Add session to profile
        profile.sessions.append(session)
        profile.total_sessions = len(profile.sessions)
        profile.current_session_id = None  # Session ended

        # Update entity session evolution
        for entity_name, moods in session.entity_mood_evolution.items():
            if entity_name not in profile.entity_session_evolution:
                profile.entity_session_evolution[entity_name] = []

            session_evolution_entry = {
                "session_id": session.session_id,
                "session_number": profile.total_sessions,
                "moods": moods,
                "mention_count": session.session_entities.get(entity_name, {}).get("mention_count", 0),
                "crisis_session": session.crisis_session,
                "breakthrough_session": session.breakthrough_session
            }
            profile.entity_session_evolution[entity_name].append(session_evolution_entry)

        # Update session patterns
        if "total_crisis_sessions" not in profile.session_patterns:
            profile.session_patterns["total_crisis_sessions"] = 0
        if "total_breakthrough_sessions" not in profile.session_patterns:
            profile.session_patterns["total_breakthrough_sessions"] = 0

        if session.crisis_session:
            profile.session_patterns["total_crisis_sessions"] += 1
        if session.breakthrough_session:
            profile.session_patterns["total_breakthrough_sessions"] += 1

        # Track session-level metrics
        profile.session_patterns["last_session_satisfaction"] = session.mean_satisfaction
        profile.session_patterns["last_session_trend"] = session.satisfaction_trend
        profile.session_patterns["last_session_turns"] = session.total_turns

    def get_session_summary(self, session: ConversationSession) -> Dict[str, Any]:
        """
        Get a summary of the session for reporting.

        Args:
            session: Session to summarize

        Returns:
            Summary dictionary
        """
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "total_turns": session.total_turns,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "duration_turns": session.total_turns,
            "entities_mentioned": list(session.session_entities.keys()),
            "entity_count": len(session.session_entities),
            "mean_satisfaction": session.mean_satisfaction,
            "satisfaction_trend": session.satisfaction_trend,
            "polyvagal_trajectory": session.polyvagal_trajectory,
            "zone_trajectory": session.zone_trajectory,
            "crisis_session": session.crisis_session,
            "breakthrough_session": session.breakthrough_session,
            "ended_naturally": session.ended_naturally
        }

    # ========================================
    # JSON PERSISTENCE METHODS (Quick Win #11)
    # ========================================

    def save_session_to_json(self, session: ConversationSession) -> str:
        """
        Save session to JSON file for crash recovery and persistence.

        Args:
            session: Session to save

        Returns:
            Path to saved JSON file
        """
        # Ensure storage directory exists
        sessions_dir = Path(self.storage_dir) / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with user_id and session_id
        filename = f"{session.user_id}_session_{session.start_time.replace(':', '-').replace('.', '-')}.json"
        filepath = sessions_dir / filename

        # Convert session to dict
        session_dict = session_to_dict(session)

        # Add metadata
        session_dict["_metadata"] = {
            "saved_at": datetime.utcnow().isoformat(),
            "version": "1.0",
            "is_active": session.end_time is None
        }

        # Save to JSON
        with open(filepath, 'w') as f:
            json.dump(session_dict, f, indent=2, default=str)

        return str(filepath)

    def load_session_from_json(self, filepath: str) -> Optional[ConversationSession]:
        """
        Load session from JSON file.

        Args:
            filepath: Path to session JSON file

        Returns:
            ConversationSession instance or None if failed
        """
        try:
            with open(filepath, 'r') as f:
                session_dict = json.load(f)

            # Remove metadata before reconstruction
            session_dict.pop("_metadata", None)

            # Reconstruct session
            session = dict_to_session(session_dict)

            return session
        except Exception as e:
            print(f"[SessionTurnManager] Error loading session from {filepath}: {e}")
            return None

    def get_user_sessions_dir(self, user_id: str) -> Path:
        """
        Get the sessions directory for a user.

        Args:
            user_id: User identifier

        Returns:
            Path to user's sessions directory
        """
        sessions_dir = Path(self.storage_dir) / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        return sessions_dir

    def list_user_sessions(self, user_id: str) -> List[str]:
        """
        List all saved session files for a user.

        Args:
            user_id: User identifier

        Returns:
            List of session file paths (sorted by timestamp, newest first)
        """
        sessions_dir = self.get_user_sessions_dir(user_id)

        # Find all sessions for this user
        session_files = list(sessions_dir.glob(f"{user_id}_session_*.json"))

        # Sort by modification time (newest first)
        session_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        return [str(f) for f in session_files]

    def restore_active_session(self, user_id: str) -> Optional[ConversationSession]:
        """
        Restore the most recent active (unended) session for a user.

        If no active session found, returns None (new session will be created).

        Args:
            user_id: User identifier

        Returns:
            Active session or None
        """
        session_files = self.list_user_sessions(user_id)

        for filepath in session_files:
            try:
                with open(filepath, 'r') as f:
                    session_dict = json.load(f)

                metadata = session_dict.get("_metadata", {})

                # Check if session is still active
                if metadata.get("is_active", False) and session_dict.get("end_time") is None:
                    session = self.load_session_from_json(filepath)
                    if session:
                        # Cache as active session
                        self.active_sessions[user_id] = session
                        print(f"[SessionTurnManager] Restored active session with {session.total_turns} turns")
                        return session
            except Exception as e:
                print(f"[SessionTurnManager] Error checking session {filepath}: {e}")
                continue

        return None

    def load_user_session_history(self, user_id: str, max_sessions: int = 10) -> List[ConversationSession]:
        """
        Load historical sessions for a user (for cross-session queries).

        Args:
            user_id: User identifier
            max_sessions: Maximum number of recent sessions to load

        Returns:
            List of ConversationSession instances (newest first)
        """
        session_files = self.list_user_sessions(user_id)[:max_sessions]
        sessions = []

        for filepath in session_files:
            session = self.load_session_from_json(filepath)
            if session:
                sessions.append(session)

        return sessions

    def auto_save_session(self, session: ConversationSession) -> str:
        """
        Auto-save session after each turn (for crash recovery).

        This should be called after each add_turn() to ensure no data is lost.

        Args:
            session: Session to save

        Returns:
            Path to saved file
        """
        return self.save_session_to_json(session)

    def cleanup_old_sessions(self, user_id: str, keep_last_n: int = 50) -> int:
        """
        Clean up old session files to prevent storage bloat.

        Args:
            user_id: User identifier
            keep_last_n: Number of recent sessions to keep

        Returns:
            Number of files deleted
        """
        session_files = self.list_user_sessions(user_id)
        deleted_count = 0

        if len(session_files) > keep_last_n:
            files_to_delete = session_files[keep_last_n:]
            for filepath in files_to_delete:
                try:
                    Path(filepath).unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"[SessionTurnManager] Error deleting {filepath}: {e}")

        return deleted_count


def session_to_dict(session: ConversationSession) -> Dict[str, Any]:
    """
    Convert session to dictionary for JSON serialization.

    Handles nested dataclasses and complex types.
    """
    result = asdict(session)

    # Handle turns with nested FeltStateSnapshot
    result["turns"] = []
    for turn in session.turns:
        turn_dict = asdict(turn)
        # FeltStateSnapshot is already handled by asdict
        result["turns"].append(turn_dict)

    return result


def turn_to_dict(turn: ConversationTurn) -> Dict[str, Any]:
    """
    Convert turn to dictionary for JSON serialization.
    """
    return asdict(turn)


def dict_to_session(session_dict: Dict[str, Any]) -> ConversationSession:
    """
    Reconstruct ConversationSession from dictionary (JSON deserialization).

    Handles nested ConversationTurn and FeltStateSnapshot objects.
    """
    # Reconstruct turns
    turns = []
    for turn_dict in session_dict.get("turns", []):
        # Reconstruct FeltStateSnapshot if present
        felt_state = None
        if turn_dict.get("felt_state"):
            felt_state_dict = turn_dict["felt_state"]
            felt_state = FeltStateSnapshot(**felt_state_dict)

        # Create ConversationTurn
        turn = ConversationTurn(
            turn_id=turn_dict["turn_id"],
            turn_number=turn_dict["turn_number"],
            session_id=turn_dict["session_id"],
            user_id=turn_dict["user_id"],
            timestamp=turn_dict["timestamp"],
            user_input=turn_dict["user_input"],
            dae_response=turn_dict["dae_response"],
            response_length=turn_dict["response_length"],
            entity_prehension=turn_dict.get("entity_prehension", {}),
            mentioned_entities=turn_dict.get("mentioned_entities", []),
            entity_references=turn_dict.get("entity_references", []),
            relational_query=turn_dict.get("relational_query", False),
            implicit_references=turn_dict.get("implicit_references", []),
            felt_state=felt_state,
            user_satisfaction=turn_dict.get("user_satisfaction"),
            user_continued=turn_dict.get("user_continued", True),
            turn_success=turn_dict.get("turn_success"),
            processing_time_ms=turn_dict.get("processing_time_ms", 0.0),
            emission_strategy=turn_dict.get("emission_strategy")
        )
        turns.append(turn)

    # Reconstruct ConversationSession
    session = ConversationSession(
        session_id=session_dict["session_id"],
        user_id=session_dict["user_id"],
        start_time=session_dict["start_time"],
        end_time=session_dict.get("end_time"),
        turns=turns,
        session_entities=session_dict.get("session_entities", {}),
        entity_mentions_timeline=session_dict.get("entity_mentions_timeline", []),
        entity_mood_evolution=session_dict.get("entity_mood_evolution", {}),
        polyvagal_trajectory=session_dict.get("polyvagal_trajectory", []),
        zone_trajectory=session_dict.get("zone_trajectory", []),
        v0_trajectory=session_dict.get("v0_trajectory", []),
        mean_satisfaction=session_dict.get("mean_satisfaction", 0.0),
        satisfaction_trend=session_dict.get("satisfaction_trend", "initializing"),
        total_turns=session_dict.get("total_turns", len(turns)),
        dominant_themes=session_dict.get("dominant_themes", []),
        recurring_nexuses=session_dict.get("recurring_nexuses", []),
        organ_participation_summary=session_dict.get("organ_participation_summary", {}),
        ended_naturally=session_dict.get("ended_naturally", False),
        crisis_session=session_dict.get("crisis_session", False),
        breakthrough_session=session_dict.get("breakthrough_session", False),
        patterns_learned=session_dict.get("patterns_learned", 0),
        family_assignments=session_dict.get("family_assignments", [])
    )

    return session
