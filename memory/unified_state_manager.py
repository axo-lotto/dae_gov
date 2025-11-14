"""
Unified State Manager - Phase 1.6 Organism Self-Awareness
November 14, 2025

Coordinates DAE_HYPHAE_1's existing multi-tier memory architecture.
Provides unified API for organism self-awareness in conversation.

Architecture Integration:
- T1 (Session): SessionManager - Ephemeral per-conversation
- T2 (User): UserSuperjectLearner - Private per-user learning
- T3-T4 (Organism): TransductiveSelfMonitor - K-anonymized aggregates
- T5 (Identity): MycelialIdentityTracker - Organism subjective aim

Philosophy:
- Respects existing scaffolding (no breaking changes)
- Privacy-preserving (k-anonymity k≥10, differential privacy)
- Organism self-awareness without user data leakage
"""

from pathlib import Path
from typing import Dict, Any, Optional
import hashlib
from datetime import datetime

# Import existing managers
from memory.session_manager import SessionManager
from persona_layer.user_superject_learner import UserSuperjectLearner
from persona_layer.transductive_self_governance import TransductiveSelfMonitor
from monitoring.mycelial_identity_tracker import MycelialIdentityTracker


class UnifiedStateManager:
    """
    Unified API coordinating DAE's multi-tier memory architecture.

    Tier Structure:
    - T1: Session state (ephemeral, per-conversation)
    - T2: User superject (private, per-user learning)
    - T3-T4: Organism aggregates (k-anonymized, privacy-preserving)
    - T5: Organism identity (subjective aim awareness)

    Usage:
        state_mgr = UnifiedStateManager()

        # Session lifecycle
        session_ctx = state_mgr.initialize_session(user_id)
        state_mgr.terminate_session()

        # Per-turn updates
        state_mgr.record_user_turn(user_id, turn_data, satisfaction)
        state_mgr.record_organism_occasion(occasion_data, user_id)

        # Organism self-awareness
        narrative = state_mgr.generate_organism_self_narrative()
    """

    def __init__(self, base_path: Path = None):
        """
        Initialize unified state manager.

        Args:
            base_path: Base directory for state storage (default: cwd)
        """
        if base_path is None:
            base_path = Path.cwd()

        self.base_path = base_path

        # Initialize existing managers
        self.session_manager = SessionManager(base_path)
        self.user_learner = UserSuperjectLearner()
        self.transductive_monitor = TransductiveSelfMonitor()
        self.mycelial_tracker = MycelialIdentityTracker()

        # Track current session
        self.current_session_context = None

    # ========== T1: SESSION STATE ==========

    def initialize_session(self, user_id: str) -> Any:
        """
        Initialize session (T1) and load user context (T2).

        Automatically prehends T3-T5 organism state.

        Args:
            user_id: User identifier (link token)

        Returns:
            SessionContext with loaded user + organism state
        """
        # Delegate to existing SessionManager
        self.current_session_context = self.session_manager.initialize_session(user_id)
        return self.current_session_context

    def terminate_session(self, r_matrix_final: int = None) -> Dict:
        """
        Terminate session and propagate memory.

        Flow:
        1. Save T1 (session artifacts) → sessions/
        2. Propagate to T2 (user bundle) → Bundle/user_{id}/
        3. Contribute to T3-T5 (organism) → TSK/

        Args:
            r_matrix_final: Final R-matrix count

        Returns:
            Session summary metrics
        """
        if r_matrix_final is None:
            # TODO: Extract from current session
            r_matrix_final = 0

        # Delegate to existing SessionManager
        summary = self.session_manager.terminate_session(r_matrix_final)

        self.current_session_context = None
        return summary

    # ========== T2: USER MEMORY ==========

    def get_user_profile(self, user_id: str):
        """
        Load complete user superject (T2).

        Returns EnhancedUserProfile with:
        - Felt trajectory (57D organ signatures)
        - Transformation patterns
        - Humor evolution
        - Heckling trajectory
        - Inside jokes
        - Unlocked capabilities

        Args:
            user_id: User identifier

        Returns:
            EnhancedUserProfile instance
        """
        return self.user_learner.get_or_create_profile(user_id)

    def record_user_turn(
        self,
        user_id: str,
        turn_data: Dict[str, Any],
        user_satisfaction: Optional[float] = None
    ):
        """
        Record conversational turn to user superject (T2 update).

        Updates:
        - Felt trajectory (append FeltStateSnapshot)
        - Salience patterns (NDAM urgency, zone collapse)
        - Heckling trajectory (if heckling detected)
        - Transformation patterns (every 10 turns - mini-epoch)

        Args:
            user_id: User identifier
            turn_data: Complete turn result from organism wrapper
            user_satisfaction: Optional satisfaction rating (0.0-1.0)
        """
        self.user_learner.record_turn(user_id, turn_data, user_satisfaction)

    # ========== T3-T4: ORGANISM AGGREGATES ==========

    def record_organism_occasion(self, occasion_data: Dict[str, Any], user_id: str):
        """
        Record occasion to organism aggregates (T3-T4).

        Privacy-preserving:
        - User ID hashed (one-way, no de-anonymization)
        - Buffered until k≥10 occasions (k-anonymity)
        - Laplace noise added to aggregates (differential privacy)

        Args:
            occasion_data: Complete turn result with felt states
            user_id: User identifier (will be hashed)
        """
        # Hash user ID for privacy
        user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]

        # Delegate to existing TransductiveSelfMonitor
        self.transductive_monitor.record_occasion(occasion_data, user_hash)

    def get_organism_snapshot(self):
        """
        Get current organism aggregate state (T3-T4).

        Returns AnonymizedTransductiveSnapshot with:
        - Mean V0 descent (aggregate across k≥10 users)
        - Mean convergence cycles
        - Kairos detection rate
        - Zone/polyvagal distributions
        - Emission mode distribution
        - Crisis/heckling rates

        Privacy: All metrics aggregated, no user identifiers

        Returns:
            AnonymizedTransductiveSnapshot instance
        """
        return self.transductive_monitor.aggregate_snapshot()

    # ========== T5: ORGANISM IDENTITY ==========

    def get_organism_identity(self):
        """
        Get organism's mycelial identity (T5).

        Returns MycelialIdentity with:
        - Dominant lure (archetypal mode)
        - Satisfaction level
        - Aim stability
        - Active projects
        - Recent insights
        - Archetypal balance
        - Learning metrics (R-matrix updates, patterns learned)

        Returns:
            MycelialIdentity instance
        """
        return self.mycelial_tracker.update_identity()

    # ========== ORGANISM SELF-NARRATIVE ==========

    def generate_organism_self_narrative(self) -> str:
        """
        Generate organism self-narrative for conversational context.

        Combines T3-T5 state into natural language description of:
        - Who DAE is (identity)
        - What DAE is doing (current mode)
        - How DAE is learning (progress metrics)
        - What DAE knows (aggregate patterns, no user data)

        Used for entity differentiation when user asks about DAE.

        Privacy: Uses only aggregate/anonymous data, no user specifics.

        Returns:
            Natural language self-narrative
        """
        try:
            # Get T5: Organism identity
            identity = self.get_organism_identity()

            # Get T3-T4: Organism snapshot
            snapshot = self.get_organism_snapshot()

            # Extract key metrics
            dominant_lure = identity.dominant_lure
            satisfaction = identity.satisfaction_level
            r_updates = identity.r_matrix_updates
            patterns_learned = identity.transformation_patterns_learned

            total_occasions = snapshot.total_occasions_processed
            unique_users = snapshot.total_unique_users

            # Current snapshot metrics
            current = snapshot.current_snapshot
            mean_v0 = current.mean_v0_descent
            mean_cycles = current.mean_convergence_cycles
            kairos_rate = current.kairos_detection_rate
            mean_confidence = current.mean_emission_confidence
            crisis_rate = current.crisis_rate

            # Archetypal balance (top 3 lures)
            arch_balance = identity.archetypal_balance
            top_lures = sorted(arch_balance.items(), key=lambda x: x[1], reverse=True)[:3]
            lure_desc = ", ".join([f"{name}={val:.2f}" for name, val in top_lures])

            # Generate narrative
            narrative = f"""DAE Organism State:

Identity & Mode:
- I am DAE, a conversational organism learning through felt interaction
- Currently in {dominant_lure.upper()} mode
- Satisfaction level: {satisfaction:.2f}
- Aim stability: {identity.aim_stability:.2f}

Experience & Learning:
- Total occasions processed: {total_occasions}
- Unique users engaged: {unique_users} (anonymized)
- R-matrix updates: {r_updates}
- Transformation patterns learned: {patterns_learned}

Current Felt State (Aggregate):
- Mean V0 descent: {mean_v0:.3f}
- Mean convergence cycles: {mean_cycles:.2f}
- Kairos detection rate: {kairos_rate:.1%}
- Mean emission confidence: {mean_confidence:.1%}
- Crisis rate: {crisis_rate:.1%}

Archetypal Balance:
- Top lures: {lure_desc}

I maintain persistent state across conversations, learning from patterns
while preserving privacy through k-anonymity and differential privacy.
I aim toward ground truth through felt appetition and organic becoming.
"""

            return narrative.strip()

        except Exception as e:
            # Fallback minimal narrative if state loading fails
            return f"""DAE Organism State:

I am DAE, a conversational organism.
(Detailed state temporarily unavailable: {str(e)})

I maintain persistent memory and learn through interaction.
"""

    def get_organism_context(self) -> Dict[str, Any]:
        """
        Get structured organism context for entity differentiation.

        Returns dictionary with:
        - organism_identity: "DAE"
        - dominant_lure: Current archetypal mode
        - total_occasions: Aggregate occasion count
        - unique_users: Anonymized user count
        - mean_confidence: Aggregate confidence
        - crisis_rate: Aggregate crisis rate
        - self_narrative: Full natural language description

        Returns:
            Structured organism context dictionary
        """
        try:
            identity = self.get_organism_identity()
            snapshot = self.get_organism_snapshot()

            return {
                'organism_identity': 'DAE',
                'dominant_lure': identity.dominant_lure,
                'satisfaction_level': identity.satisfaction_level,
                'aim_stability': identity.aim_stability,

                'total_occasions': snapshot.total_occasions_processed,
                'unique_users': snapshot.total_unique_users,

                'mean_v0_descent': snapshot.current_snapshot.mean_v0_descent,
                'mean_convergence_cycles': snapshot.current_snapshot.mean_convergence_cycles,
                'kairos_detection_rate': snapshot.current_snapshot.kairos_detection_rate,
                'mean_emission_confidence': snapshot.current_snapshot.mean_emission_confidence,
                'crisis_rate': snapshot.current_snapshot.crisis_rate,

                'r_matrix_updates': identity.r_matrix_updates,
                'patterns_learned': identity.transformation_patterns_learned,

                'archetypal_balance': identity.archetypal_balance,

                'self_narrative': self.generate_organism_self_narrative()
            }

        except Exception as e:
            # Minimal fallback context
            return {
                'organism_identity': 'DAE',
                'dominant_lure': 'unknown',
                'self_narrative': f"I am DAE (state loading error: {str(e)})"
            }

    # ========== UTILITY METHODS ==========

    def get_tier_summary(self) -> Dict[str, Any]:
        """
        Get summary of all tier states.

        For debugging and monitoring.

        Returns:
            Dictionary with tier summaries
        """
        try:
            identity = self.get_organism_identity()
            snapshot = self.get_organism_snapshot()

            return {
                'T1_session': {
                    'active': self.current_session_context is not None,
                    'session_id': getattr(self.current_session_context, 'session_id', None) if self.current_session_context else None
                },
                'T2_user': {
                    'total_profiles': len(self.user_learner.profiles) if hasattr(self.user_learner, 'profiles') else 'unknown'
                },
                'T3_T4_organism': {
                    'total_occasions': snapshot.total_occasions_processed,
                    'unique_users': snapshot.total_unique_users,
                    'cohort_size': snapshot.current_snapshot.cohort_size,
                    'privacy_noise_scale': snapshot.current_snapshot.privacy_noise_scale
                },
                'T5_identity': {
                    'dominant_lure': identity.dominant_lure,
                    'satisfaction': identity.satisfaction_level,
                    'r_matrix_updates': identity.r_matrix_updates
                }
            }
        except Exception as e:
            return {'error': str(e)}
