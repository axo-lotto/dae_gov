"""
Turn History Manager - LLM Bridge Phase 2
=========================================

Manages recent conversation turns for multi-turn context.

Purpose:
- Store last 3-5 turns per session (in-memory, lightweight)
- Provide context for felt-guided LLM prompts
- Enable "you mentioned X earlier" continuity

Integration Point:
- Called by conversational_organism_wrapper
- Provides turn history to llm_felt_guidance.py
- No persistent storage needed (session-scoped)

Design:
- Simple ring buffer (fixed capacity)
- Per-session isolation
- Minimal memory footprint

Date: November 18, 2025
Status: Phase 2 - LLM Bridge Strategy Implementation
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque


@dataclass
class ConversationTurn:
    """
    Single conversation turn (user + organism exchange).
    """

    turn_number: int
    user_input: str
    organism_emission: str

    # Metadata
    timestamp: str
    emission_confidence: float
    emission_path: str  # 'felt_guided_llm', 'pattern_learner', etc.

    # Optional felt-state summary (for context)
    polyvagal_state: Optional[str] = None
    urgency: Optional[float] = None
    zone: Optional[int] = None
    satisfaction: Optional[float] = None


class TurnHistoryManager:
    """
    Manages conversation turn history for multi-turn context.

    Features:
    - Per-session turn buffers (isolated)
    - Fixed capacity ring buffers (3-5 turns)
    - Lightweight in-memory storage
    - Session cleanup on timeout

    Design Principles:
    - Simple and fast (no database)
    - Session-scoped (no cross-session leakage)
    - Conservative memory (<1KB per session)
    """

    def __init__(
        self,
        max_turns_per_session: int = 5,
        session_timeout_minutes: int = 30
    ):
        """
        Initialize turn history manager.

        Args:
            max_turns_per_session: Max turns to keep per session (ring buffer)
            session_timeout_minutes: Auto-cleanup idle sessions after this time
        """
        self.max_turns = max_turns_per_session
        self.session_timeout_minutes = session_timeout_minutes

        # Per-session turn buffers
        # {session_id: deque([ConversationTurn, ...], maxlen=max_turns)}
        self.session_buffers: Dict[str, deque] = {}

        # Per-session metadata
        # {session_id: {'last_activity': timestamp, 'turn_count': int}}
        self.session_metadata: Dict[str, Dict[str, Any]] = {}

    def add_turn(
        self,
        session_id: str,
        user_input: str,
        organism_emission: str,
        emission_metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Add a new conversation turn to session history.

        Args:
            session_id: Unique session identifier
            user_input: User's message
            organism_emission: Organism's response
            emission_metadata: Optional metadata (confidence, path, felt-state)

        Returns:
            Turn number (0-indexed within session)
        """
        # Initialize session if new
        if session_id not in self.session_buffers:
            self.session_buffers[session_id] = deque(maxlen=self.max_turns)
            self.session_metadata[session_id] = {
                'last_activity': datetime.now(),
                'turn_count': 0
            }

        # Extract metadata
        metadata = emission_metadata or {}
        turn_number = self.session_metadata[session_id]['turn_count']

        # Create turn object
        turn = ConversationTurn(
            turn_number=turn_number,
            user_input=user_input,
            organism_emission=organism_emission,
            timestamp=datetime.now().isoformat(),
            emission_confidence=metadata.get('emission_confidence', 0.0),
            emission_path=metadata.get('emission_path', 'unknown'),
            polyvagal_state=metadata.get('polyvagal_state'),
            urgency=metadata.get('urgency'),
            zone=metadata.get('zone'),
            satisfaction=metadata.get('satisfaction')
        )

        # Add to ring buffer (automatically evicts oldest if full)
        self.session_buffers[session_id].append(turn)

        # Update metadata
        self.session_metadata[session_id]['last_activity'] = datetime.now()
        self.session_metadata[session_id]['turn_count'] += 1

        return turn_number

    def get_recent_turns(
        self,
        session_id: str,
        num_turns: Optional[int] = None
    ) -> List[ConversationTurn]:
        """
        Get recent turns for a session.

        Args:
            session_id: Session identifier
            num_turns: Number of recent turns (default: all available)

        Returns:
            List of ConversationTurn objects (oldest first)
        """
        if session_id not in self.session_buffers:
            return []

        buffer = self.session_buffers[session_id]

        if num_turns is None:
            return list(buffer)
        else:
            # Get last N turns
            return list(buffer)[-num_turns:]

    def get_context_string(
        self,
        session_id: str,
        num_turns: Optional[int] = 3,
        include_metadata: bool = False
    ) -> str:
        """
        Get formatted context string for LLM prompt.

        Args:
            session_id: Session identifier
            num_turns: Number of recent turns to include
            include_metadata: Include felt-state metadata in context

        Returns:
            Formatted conversation history string
        """
        turns = self.get_recent_turns(session_id, num_turns)

        if not turns:
            return ""

        context_lines = ["Recent conversation:"]

        for turn in turns:
            context_lines.append(f"User: {turn.user_input}")
            context_lines.append(f"You: {turn.organism_emission}")

            # Optional: Add felt-state summary
            if include_metadata and turn.polyvagal_state:
                meta_parts = []
                if turn.polyvagal_state:
                    meta_parts.append(f"state: {turn.polyvagal_state}")
                if turn.zone is not None:
                    meta_parts.append(f"zone: {turn.zone}")
                if turn.urgency is not None:
                    meta_parts.append(f"urgency: {turn.urgency:.2f}")

                if meta_parts:
                    context_lines.append(f"  [{', '.join(meta_parts)}]")

        return "\n".join(context_lines)

    def clear_session(self, session_id: str) -> bool:
        """
        Clear all turns for a session.

        Args:
            session_id: Session identifier

        Returns:
            True if session existed and was cleared
        """
        if session_id in self.session_buffers:
            del self.session_buffers[session_id]
            del self.session_metadata[session_id]
            return True
        return False

    def cleanup_idle_sessions(self) -> int:
        """
        Remove sessions that have been idle beyond timeout.

        Returns:
            Number of sessions cleaned up
        """
        now = datetime.now()
        sessions_to_remove = []

        for session_id, metadata in self.session_metadata.items():
            last_activity = metadata['last_activity']
            idle_minutes = (now - last_activity).total_seconds() / 60

            if idle_minutes > self.session_timeout_minutes:
                sessions_to_remove.append(session_id)

        for session_id in sessions_to_remove:
            self.clear_session(session_id)

        return len(sessions_to_remove)

    def get_session_stats(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a session.

        Args:
            session_id: Session identifier

        Returns:
            Stats dict or None if session doesn't exist
        """
        if session_id not in self.session_metadata:
            return None

        metadata = self.session_metadata[session_id]
        buffer = self.session_buffers[session_id]

        now = datetime.now()
        last_activity = metadata['last_activity']
        idle_minutes = (now - last_activity).total_seconds() / 60

        return {
            'session_id': session_id,
            'total_turns': metadata['turn_count'],
            'buffered_turns': len(buffer),
            'last_activity': last_activity.isoformat(),
            'idle_minutes': idle_minutes,
            'buffer_capacity': self.max_turns
        }

    def get_all_session_stats(self) -> List[Dict[str, Any]]:
        """
        Get statistics for all sessions.

        Returns:
            List of stats dicts
        """
        return [
            self.get_session_stats(session_id)
            for session_id in self.session_buffers.keys()
        ]

    def get_total_memory_usage(self) -> Dict[str, int]:
        """
        Estimate memory usage (approximate).

        Returns:
            Dict with memory estimates in bytes
        """
        # Rough estimate: 200 bytes per turn average
        bytes_per_turn = 200

        total_turns = sum(len(buffer) for buffer in self.session_buffers.values())
        total_sessions = len(self.session_buffers)

        return {
            'total_sessions': total_sessions,
            'total_turns': total_turns,
            'estimated_bytes': total_turns * bytes_per_turn,
            'estimated_kb': (total_turns * bytes_per_turn) / 1024
        }
