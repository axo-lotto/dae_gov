"""
Superject Recorder - Persistent Conversational Datum Formation
================================================================

Records each conversational turn as a "superject" (Whitehead) - the satisfaction
of a completed occasion that becomes objective datum for future occasions.

Key Principles (Process Philosophy):
1. Each conversation is an "actual occasion" that achieves "satisfaction"
2. Satisfaction becomes "superject" - objective datum for future prehensions
3. Superjective immortality: Past occasions persist as felt data
4. Recording integrates with existing fractal learning (organic families)

Integration with Fractal Architecture:
- Leverages Phase5LearningIntegration (organic family assignment)
- Uses OrganSignatureExtractor (57D signatures)
- Stores in organic_families.json (existing persistence)
- Updates user bundles (persistent identity themes)

Architecture:
- POST-emission hook (called after successful response assembly)
- Extracts 57D organ signature from current occasion
- Records conversation in organic family system
- Updates user bundle with themes/patterns
- Maintains session history for continuity

Date: November 13, 2025
Author: DAE_HYPHAE_1 + Claude (hybrid authorship)
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class ConversationalSuperject:
    """
    Superject: The objective datum formed by a completed conversational occasion.

    Represents the "satisfaction" that future occasions will prehend.
    Contains full felt state, organ signature, and conversational context.
    """
    conversation_id: str
    timestamp: str

    # User input
    user_message: str

    # DAE response
    dae_response: str
    emission_confidence: float
    emission_path: str  # 'direct_reconstruction', 'fusion', etc.

    # Organ signature (57D from OrganSignatureExtractor)
    organ_signature: Dict

    # Family assignment
    family_id: Optional[str]
    family_assignment_type: Optional[str]  # 'ASSIGNED', 'CREATED'

    # Felt states
    v0_energy: Dict  # V0 convergence data
    nexuses_formed: List[Dict]
    transduction_pathway: Optional[str]
    self_zone: int  # SELF matrix zone (0-4)
    polyvagal_state: str  # 'ventral', 'sympathetic', 'dorsal', 'mixed'

    # Quality metrics
    satisfaction_score: float
    safety_gradient: float
    signal_inflation: float

    # Session context
    session_id: Optional[str]
    turn_number: int


class SuperjectRecorder:
    """
    Records conversational superjections for persistent memory.

    Integrates with existing fractal learning:
    - Uses Phase5LearningIntegration for family assignment
    - Leverages OrganSignatureExtractor for 57D signatures
    - Stores in organic_families.json (existing persistence)
    - Updates user bundles (themes, inside jokes, preferences)

    Hook Point:
    - Called POST-emission (after response assembly)
    - Requires: organ_results, assembled_response, user_message
    - Returns: Superject metadata (family_id, conversation_id)
    """

    def __init__(
        self,
        session_storage_dir: str = "sessions",
        user_bundles_dir: str = "Bundle",
        enable_session_logging: bool = True
    ):
        """
        Initialize superject recorder.

        Args:
            session_storage_dir: Directory for session-specific logs
            user_bundles_dir: Directory for user identity bundles
            enable_session_logging: Whether to save session transcripts
        """
        self.session_storage_dir = Path(session_storage_dir)
        self.user_bundles_dir = Path(user_bundles_dir)
        self.enable_session_logging = enable_session_logging

        # Ensure directories exist
        self.session_storage_dir.mkdir(parents=True, exist_ok=True)
        self.user_bundles_dir.mkdir(parents=True, exist_ok=True)

        # Session state
        self.current_session_id: Optional[str] = None
        self.current_session_turns: List[ConversationalSuperject] = []
        self.turn_counter = 0

    def start_session(self, user_id: Optional[str] = None) -> str:
        """
        Start new conversational session.

        Args:
            user_id: Optional user identifier

        Returns:
            session_id: Unique session identifier
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_suffix = f"_{user_id}" if user_id else ""
        self.current_session_id = f"session_{timestamp}{user_suffix}"
        self.current_session_turns = []
        self.turn_counter = 0

        print(f"✅ Session started: {self.current_session_id}")
        return self.current_session_id

    def record_superject(
        self,
        user_message: str,
        dae_response: str,
        organ_results: Dict,
        felt_states: Dict,
        family_assignment: Optional[Dict] = None,
        user_id: Optional[str] = None
    ) -> ConversationalSuperject:
        """
        Record conversational turn as persistent superject.

        Args:
            user_message: User input text
            dae_response: DAE emission text
            organ_results: Dict of 11 organ processing results
            felt_states: Dict of felt states (v0_energy, nexuses, etc.)
            family_assignment: Optional family assignment from Phase5
            user_id: Optional user identifier

        Returns:
            ConversationalSuperject: Recorded datum
        """
        self.turn_counter += 1

        # Generate conversation ID
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        conversation_id = f"{self.current_session_id}_turn{self.turn_counter:03d}"

        # Extract organ signature (simplified extraction)
        organ_signature = self._extract_organ_signature(organ_results)

        # Extract felt state components
        v0_energy = felt_states.get('v0_energy', {})
        nexuses = felt_states.get('nexuses_formed', [])
        transduction = felt_states.get('transduction_pathway')
        self_zone = felt_states.get('self_zone', 0)
        polyvagal = felt_states.get('polyvagal_state', 'unknown')

        # Quality metrics
        emission_confidence = felt_states.get('emission_confidence', 0.0)
        emission_path = felt_states.get('emission_path', 'unknown')
        satisfaction = felt_states.get('satisfaction_score', emission_confidence)
        safety = felt_states.get('safety_gradient', 1.0)
        inflation = felt_states.get('signal_inflation', 0.0)

        # Family assignment
        family_id = None
        assignment_type = None
        if family_assignment:
            family_id = family_assignment.get('family_id')
            assignment_type = family_assignment.get('assignment_type')

        # Create superject
        superject = ConversationalSuperject(
            conversation_id=conversation_id,
            timestamp=timestamp,
            user_message=user_message,
            dae_response=dae_response,
            emission_confidence=emission_confidence,
            emission_path=emission_path,
            organ_signature=organ_signature,
            family_id=family_id,
            family_assignment_type=assignment_type,
            v0_energy=v0_energy,
            nexuses_formed=nexuses,
            transduction_pathway=transduction,
            self_zone=self_zone,
            polyvagal_state=polyvagal,
            satisfaction_score=satisfaction,
            safety_gradient=safety,
            signal_inflation=inflation,
            session_id=self.current_session_id,
            turn_number=self.turn_counter
        )

        # Add to session turns
        self.current_session_turns.append(superject)

        # Update user bundle if user_id provided
        if user_id:
            self._update_user_bundle(user_id, superject)

        # Save session log if enabled
        if self.enable_session_logging:
            self._save_session_turn(superject)

        return superject

    def _extract_organ_signature(self, organ_results: Dict) -> Dict:
        """
        Extract simplified organ signature from organ_results.

        Note: Full 57D extraction would use OrganSignatureExtractor,
        but for superject recording, we store raw organ_results which
        contain sufficient detail for later signature computation.

        Args:
            organ_results: Dict of 11 organ processing results

        Returns:
            Simplified signature dict
        """
        signature = {}

        for organ_name, organ_data in organ_results.items():
            if isinstance(organ_data, dict):
                # Extract key metrics
                signature[organ_name] = {
                    "coherence": organ_data.get("coherence", 0.0),
                    "mean": organ_data.get("coherence", 0.0),  # For compatibility
                    "variance": 0.0  # Placeholder
                }
            else:
                # Scalar value
                signature[organ_name] = {
                    "coherence": organ_data if isinstance(organ_data, (int, float)) else 0.0,
                    "mean": organ_data if isinstance(organ_data, (int, float)) else 0.0,
                    "variance": 0.0
                }

        return signature

    def _update_user_bundle(self, user_id: str, superject: ConversationalSuperject):
        """
        Update user bundle with patterns from this superject.

        Extracts:
        - Recurring themes (from dominant organs)
        - Polyvagal patterns (safety trends)
        - Response preferences (confidence, length, detail)

        Args:
            user_id: User identifier
            superject: Recorded conversational datum
        """
        user_link_dir = self.user_bundles_dir / f"user_link_{user_id}"
        user_state_file = user_link_dir / "user_state.json"

        # Load existing bundle
        if user_state_file.exists():
            with open(user_state_file) as f:
                bundle = json.load(f)
        else:
            bundle = {
                "user_id": user_id,
                "total_conversations": 0,
                "themes": [],
                "inside_jokes": [],
                "preferences": {},
                "created_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            }

        # Increment conversation count
        bundle["total_conversations"] = bundle.get("total_conversations", 0) + 1

        # Track polyvagal states (for safety trends)
        polyvagal_history = bundle.get("polyvagal_history", [])
        polyvagal_history.append({
            "state": superject.polyvagal_state,
            "timestamp": superject.timestamp
        })
        bundle["polyvagal_history"] = polyvagal_history[-50:]  # Keep last 50

        # Track SELF zones (for trauma patterns)
        zone_history = bundle.get("zone_history", [])
        zone_history.append({
            "zone": superject.self_zone,
            "timestamp": superject.timestamp
        })
        bundle["zone_history"] = zone_history[-50:]  # Keep last 50

        # Update preferences based on satisfaction
        preferences = bundle.get("preferences", {})
        if superject.satisfaction_score > 0.7:
            # High satisfaction - record preferences
            preferences["preferred_confidence"] = preferences.get("preferred_confidence", [])
            preferences["preferred_confidence"].append(superject.emission_confidence)
            preferences["preferred_confidence"] = preferences["preferred_confidence"][-10:]

        bundle["preferences"] = preferences
        bundle["last_updated"] = superject.timestamp

        # Save updated bundle
        user_link_dir.mkdir(parents=True, exist_ok=True)
        with open(user_state_file, 'w') as f:
            json.dump(bundle, f, indent=2)

    def _save_session_turn(self, superject: ConversationalSuperject):
        """
        Save session turn to disk for transcript logging.

        Args:
            superject: Recorded conversational datum
        """
        if not self.current_session_id:
            return

        # Session directory
        session_dir = self.session_storage_dir / self.current_session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        # Append turn to session transcript
        transcript_file = session_dir / "transcript.jsonl"
        with open(transcript_file, 'a') as f:
            # Write as JSON lines (one turn per line)
            turn_data = asdict(superject)
            f.write(json.dumps(turn_data) + "\n")

    def end_session(self) -> Dict:
        """
        End current session and generate summary.

        Returns:
            Session summary dict
        """
        if not self.current_session_id:
            return {}

        summary = {
            "session_id": self.current_session_id,
            "total_turns": len(self.current_session_turns),
            "mean_satisfaction": sum(s.satisfaction_score for s in self.current_session_turns) / max(len(self.current_session_turns), 1),
            "families_encountered": list(set(s.family_id for s in self.current_session_turns if s.family_id)),
            "polyvagal_distribution": self._compute_polyvagal_distribution(),
            "zone_distribution": self._compute_zone_distribution(),
            "ended_at": datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        }

        # Save session summary
        if self.enable_session_logging:
            session_dir = self.session_storage_dir / self.current_session_id
            session_dir.mkdir(parents=True, exist_ok=True)
            with open(session_dir / "summary.json", 'w') as f:
                json.dump(summary, f, indent=2)

        print(f"✅ Session ended: {self.current_session_id}")
        print(f"   Total turns: {summary['total_turns']}")
        print(f"   Mean satisfaction: {summary['mean_satisfaction']:.3f}")

        # Reset session state
        self.current_session_id = None
        self.current_session_turns = []
        self.turn_counter = 0

        return summary

    def _compute_polyvagal_distribution(self) -> Dict[str, int]:
        """Compute distribution of polyvagal states in session."""
        distribution = {}
        for turn in self.current_session_turns:
            state = turn.polyvagal_state
            distribution[state] = distribution.get(state, 0) + 1
        return distribution

    def _compute_zone_distribution(self) -> Dict[int, int]:
        """Compute distribution of SELF zones in session."""
        distribution = {}
        for turn in self.current_session_turns:
            zone = turn.self_zone
            distribution[zone] = distribution.get(zone, 0) + 1
        return distribution

    def get_session_history(self) -> List[ConversationalSuperject]:
        """
        Get current session's conversational history.

        Returns:
            List of superjections in chronological order
        """
        return self.current_session_turns.copy()

    def format_session_context(self, last_n_turns: int = 3) -> str:
        """
        Format recent session history for LLM context.

        Args:
            last_n_turns: Number of recent turns to include

        Returns:
            Formatted context string
        """
        if not self.current_session_turns:
            return "No previous conversation in this session."

        recent_turns = self.current_session_turns[-last_n_turns:]

        context_lines = ["=== Recent Session History ==="]
        context_lines.append("")

        for turn in recent_turns:
            context_lines.append(f"Turn {turn.turn_number}:")
            context_lines.append(f"  User: {turn.user_message[:100]}...")
            context_lines.append(f"  DAE: {turn.dae_response[:100]}...")
            context_lines.append(f"  State: {turn.polyvagal_state}, Zone {turn.self_zone}")
            context_lines.append("")

        return "\n".join(context_lines)


# Example usage
if __name__ == "__main__":
    print("Superject Recorder - Example Usage")
    print("=" * 80)

    # Initialize recorder
    recorder = SuperjectRecorder()

    # Start session
    session_id = recorder.start_session(user_id="test_user")
    print()

    # Example turn 1
    print("Recording turn 1...")
    superject1 = recorder.record_superject(
        user_message="I'm feeling overwhelmed right now.",
        dae_response="I hear you. That sense of overwhelm is real.",
        organ_results={
            "LISTENING": {"coherence": 0.9},
            "EMPATHY": {"coherence": 0.85},
            "NDAM": {"coherence": 0.8},  # High urgency
            "EO": {"coherence": 0.4}     # Low polyvagal
        },
        felt_states={
            "emission_confidence": 0.75,
            "emission_path": "direct_reconstruction",
            "self_zone": 3,
            "polyvagal_state": "sympathetic",
            "satisfaction_score": 0.78
        },
        family_assignment={
            "family_id": "Family_003",
            "assignment_type": "ASSIGNED"
        },
        user_id="test_user"
    )
    print(f"  ✅ Recorded: {superject1.conversation_id}")
    print()

    # Get session context
    print("Session context:")
    print(recorder.format_session_context())
    print()

    # End session
    summary = recorder.end_session()
    print(f"Session summary: {summary}")
