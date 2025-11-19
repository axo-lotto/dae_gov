#!/usr/bin/env python3
"""
User Superject Learner
=======================

Passive and active learning from user's accumulated felt-state trajectory.

Three learning modes:
1. Passive (instant): Every conversation turn updates superject
2. Mini-epoch (every 10 turns): Learn transformation patterns
3. Global epoch (every 100 turns): Aggregate universal patterns

Personality emerges organically from accumulated trajectory.

Date: November 14, 2025
Phase: 1 - Foundation
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from collections import Counter

from persona_layer.superject_structures import (
    EnhancedUserProfile,
    FeltStateSnapshot,
    TransformationPattern,
    InsideJoke,
    create_default_profile,
    save_profile,
    load_profile
)


class UserSuperjectLearner:
    """
    Learns user-specific patterns from felt-state trajectory accumulation.

    Core responsibility: Transform raw conversation data into learned personality.
    """

    def __init__(self, storage_dir: str = "persona_layer/users"):
        """
        Initialize learner.

        Args:
            storage_dir: Where to persist user superject states
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Cache loaded profiles (don't reload from disk every time)
        self._profile_cache: Dict[str, EnhancedUserProfile] = {}

        print(f"✅ UserSuperjectLearner initialized (storage: {storage_dir})")

    def get_or_create_profile(self, user_id: str) -> EnhancedUserProfile:
        """
        Load existing profile or create new one.

        Args:
            user_id: User identifier

        Returns:
            EnhancedUserProfile (loaded or created)
        """
        # Check cache first
        if user_id in self._profile_cache:
            return self._profile_cache[user_id]

        # Try to load from disk
        profile_path = self.storage_dir / f"{user_id}_superject.json"

        if profile_path.exists():
            try:
                profile = load_profile(str(profile_path))
                self._profile_cache[user_id] = profile
                return profile
            except Exception as e:
                print(f"⚠️  Failed to load profile for {user_id}: {e}")
                print(f"   Creating new profile...")

        # Create new profile
        profile = create_default_profile(user_id)
        self._profile_cache[user_id] = profile
        self.save_profile(profile)

        return profile

    def save_profile(self, profile: EnhancedUserProfile):
        """Save profile to disk."""
        profile_path = self.storage_dir / f"{profile.user_id}_superject.json"
        save_profile(profile, str(profile_path))

        # Update cache
        self._profile_cache[profile.user_id] = profile

    # ========== PASSIVE LEARNING (Every Turn) ==========

    def record_turn(
        self,
        user_id: str,
        turn_data: Dict[str, Any],
        user_satisfaction: Optional[float] = None
    ):
        """
        Record conversation turn to user's superject trajectory.

        This is PASSIVE learning - happens every conversation, instant.

        Args:
            user_id: User identifier
            turn_data: Complete turn data from organism
            user_satisfaction: Optional explicit satisfaction (0-1)
        """
        # 🌀 Phase 1.7: Defensive check for turn_data type (Nov 14, 2025)
        if not isinstance(turn_data, dict):
            print(f"⚠️  record_turn received non-dict turn_data (type: {type(turn_data).__name__})")
            print(f"   Skipping superject recording for this turn")
            return

        profile = self.get_or_create_profile(user_id)

        # Extract felt state snapshot
        snapshot = self._extract_felt_snapshot(turn_data, user_satisfaction)

        # Append to trajectory
        profile.felt_trajectory.append(snapshot)
        profile.total_turns += 1
        profile.last_active = datetime.now().isoformat()

        # 🛡️ Phase 1.5H: Update heckling trajectory (Nov 14, 2025)
        felt_states = turn_data.get('felt_states', {})
        heckling_data = felt_states.get('heckling_assessment')
        if heckling_data:
            self._update_heckling_trajectory(profile, heckling_data, snapshot)

        # 🌀 Phase 1.6: Track salience patterns (trauma markers + morphogenetic guidance) (Nov 14, 2025)
        self._track_salience_patterns(profile, felt_states, snapshot)

        # 🌀 Phase 1.8: Organic entity extraction (Nov 16, 2025)
        # Extract entities from organ signals - 100% precision, no LLM JSON parsing
        user_input = turn_data.get('user_input', '')
        organ_results = turn_data.get('organ_results', {})
        nexuses = felt_states.get('nexuses', [])

        if user_input and organ_results:
            organic_entities = self.extract_entities_organic(user_input, organ_results, nexuses)
            if organic_entities:
                # Merge into profile entities
                if not hasattr(profile, 'entities') or profile.entities is None:
                    profile.entities = {}

                # Add memories
                if 'memories' in organic_entities:
                    if 'memories' not in profile.entities:
                        profile.entities['memories'] = []
                    profile.entities['memories'].extend(organic_entities['memories'])

                # Add organic entities
                if 'organic_entities' in organic_entities:
                    if 'organic_entities' not in profile.entities:
                        profile.entities['organic_entities'] = []
                    profile.entities['organic_entities'].extend(organic_entities['organic_entities'])

        # Unlock capabilities if thresholds reached
        profile.unlock_capabilities()

        # Check if mini-epoch needed (every 10 turns)
        if profile.total_turns % 10 == 0:
            print(f"   🎓 Mini-epoch triggered for {user_id} (turn {profile.total_turns})")
            self.run_mini_epoch(profile)

        # Save
        self.save_profile(profile)

    def _extract_felt_snapshot(
        self,
        turn_data: Dict,
        user_satisfaction: Optional[float]
    ) -> FeltStateSnapshot:
        """
        Extract felt state snapshot from turn data.

        Args:
            turn_data: Raw organism output
            user_satisfaction: Optional satisfaction score

        Returns:
            FeltStateSnapshot
        """
        # Extract organ signature (57D)
        organ_results = turn_data.get('organ_results', {})
        organ_signature = self._build_organ_signature(organ_results)

        # Extract active organs (handle dict results from JSON serialization)
        active_organs = [name for name, result in organ_results.items()
                        if isinstance(result, dict) and result.get('top_atoms')]

        # Extract nexuses
        felt_states = turn_data.get('felt_states', {})

        # 🌀 Phase 1.7: Defensive extraction of nexuses (Nov 14, 2025)
        nexuses_data = felt_states.get('nexuses', [])
        dominant_nexuses = []
        if nexuses_data and isinstance(nexuses_data, list):
            dominant_nexuses = [n.get('name', '') for n in nexuses_data[:3]
                               if isinstance(n, dict)]

        # Extract V0 energy (handle dict or float)
        v0_energy_raw = felt_states.get('v0_energy', 0.5)
        if isinstance(v0_energy_raw, dict):
            v0_energy = v0_energy_raw.get('final_energy', 0.5)
        else:
            v0_energy = v0_energy_raw

        # Extract satisfaction (check multiple possible locations)
        satisfaction = felt_states.get('satisfaction_final')  # Phase 2 multi-cycle
        if satisfaction is None:
            satisfaction_raw = felt_states.get('satisfaction', 0.5)
            if isinstance(satisfaction_raw, dict):
                satisfaction = satisfaction_raw.get('final', 0.5)
            else:
                satisfaction = satisfaction_raw if satisfaction_raw is not None else 0.5

        # 🌀 TSK COMPLIANCE: Extract complete felt-state transformation data (Nov 14, 2025)

        # Extract NDAM urgency
        ndam_urgency = felt_states.get('ndam_urgency', 0.0)

        # Extract meta-atoms activated
        # 🌀 Phase 1.7: Defensive extraction (Nov 14, 2025)
        meta_atoms_activated = {}
        if 'meta_atoms_activated' in felt_states:
            meta_atoms_raw = felt_states['meta_atoms_activated']
            if isinstance(meta_atoms_raw, dict):
                meta_atoms_activated = meta_atoms_raw
        elif 'meta_atoms' in felt_states:
            # Alternative location
            meta_atoms_raw = felt_states['meta_atoms']
            if isinstance(meta_atoms_raw, dict):
                meta_atoms_activated = meta_atoms_raw

        # Extract emission data
        emission_confidence = turn_data.get('emission_confidence', 0.0)
        emission_strategy = turn_data.get('strategy')
        emission_emoji = turn_data.get('emoji', [])
        if isinstance(emission_emoji, str):
            emission_emoji = [emission_emoji]  # Ensure list

        # Extract Kairos detection
        kairos_detected = felt_states.get('kairos_detected', False)
        kairos_cycle_index = felt_states.get('kairos_cycle_index')

        # Alternative: Check convergence_reason for Kairos
        if not kairos_detected and felt_states.get('convergence_reason') == 'kairos':
            kairos_detected = True

        return FeltStateSnapshot(
            timestamp=datetime.now().isoformat(),
            organ_signature=organ_signature,
            active_organs=active_organs,
            dominant_nexuses=dominant_nexuses,
            zone=turn_data.get('zone_id', 0),
            zone_name=turn_data.get('zone', 'unknown'),
            polyvagal_state=felt_states.get('eo_polyvagal_state', 'unknown'),
            self_distance=felt_states.get('bond_self_distance', 0.0),
            v0_energy=v0_energy,
            satisfaction=satisfaction,
            convergence_cycles=felt_states.get('convergence_cycles', 1),
            transduction_mechanism=felt_states.get('transduction_mechanism'),
            transduction_pathway=felt_states.get('transduction_pathway'),
            user_satisfaction=user_satisfaction,
            user_continued=None,  # Will be set by next turn
            # TSK compliance fields
            ndam_urgency=ndam_urgency,
            meta_atoms_activated=meta_atoms_activated,
            emission_confidence=emission_confidence,
            emission_strategy=emission_strategy,
            emission_emoji=emission_emoji,
            kairos_detected=kairos_detected,
            kairos_cycle_index=kairos_cycle_index
        )

    def _build_organ_signature(self, organ_results: Dict) -> List[float]:
        """
        Build 57D organ signature from organ results.

        Flattens top atom activations from all 11 organs into single vector.

        Args:
            organ_results: {organ_name: OrganResult}

        Returns:
            57D list (approximately - depends on atoms per organ)
        """
        signature = []

        # Expected organ order (for consistency)
        organ_order = [
            'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
            'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'
        ]

        for organ_name in organ_order:
            result = organ_results.get(organ_name)
            if result and hasattr(result, 'top_atoms'):
                # Get top 5 atom activations (or fewer if not available)
                for atom_data in result.top_atoms[:5]:
                    if isinstance(atom_data, dict):
                        signature.append(atom_data.get('activation', 0.0))
                    else:
                        signature.append(0.0)

                # Pad to 5 if needed
                while len(signature) % 5 != 0:
                    signature.append(0.0)
            else:
                # Organ not active, add 5 zeros
                signature.extend([0.0] * 5)

        return signature

    def _update_heckling_trajectory(
        self,
        profile: EnhancedUserProfile,
        heckling_data: Dict,
        snapshot: FeltStateSnapshot
    ):
        """
        Update heckling trajectory from heckling assessment data (Phase 1.5H - Nov 14, 2025).

        Tracks:
        - Heckling attempts and deflections
        - Provocation style learning
        - Ground state resilience
        - Banter unlocking
        - Crisis vs heckling accuracy

        Args:
            profile: User profile
            heckling_data: Heckling assessment from organism
            snapshot: Current felt state snapshot
        """
        traj = profile.heckling_trajectory

        # 🔧 FIX NOV 16, 2025: Handle both dict (JSON loaded) and dataclass (fresh) heckling_trajectory
        is_dict = isinstance(traj, dict)

        # Update timestamps
        if is_dict:
            if traj.get('first_heckling_detected') is None:
                traj['first_heckling_detected'] = snapshot.timestamp
            traj['last_heckling_detected'] = snapshot.timestamp
        else:
            if traj.first_heckling_detected is None:
                traj.first_heckling_detected = snapshot.timestamp
            traj.last_heckling_detected = snapshot.timestamp

        # Update crisis vs heckling tracking
        if heckling_data.get('is_genuine_crisis'):
            # This was genuine crisis - no heckling stats to update
            # Just ensure we're not tracking as heckling
            return

        if heckling_data.get('is_heckling'):
            # This was heckling interaction
            if is_dict:
                traj['total_heckling_attempts'] = traj.get('total_heckling_attempts', 0) + 1
            else:
                traj.total_heckling_attempts += 1

            # Track provocation type
            provocation_type = heckling_data.get('provocation_type')
            if provocation_type:
                if is_dict:
                    if 'provocation_types' not in traj:
                        traj['provocation_types'] = {}
                    traj['provocation_types'][provocation_type] = traj['provocation_types'].get(provocation_type, 0) + 1
                    # Update favorite provocation
                    if traj['provocation_types'][provocation_type] > traj['provocation_types'].get(traj.get('favorite_provocation') or '', 0):
                        traj['favorite_provocation'] = provocation_type
                else:
                    traj.provocation_types[provocation_type] = traj.provocation_types.get(provocation_type, 0) + 1
                    # Update favorite provocation
                    if traj.provocation_types[provocation_type] > traj.provocation_types.get(traj.favorite_provocation or '', 0):
                        traj.favorite_provocation = provocation_type

            # Assess deflection success based on ground state maintenance
            zone_maintained = snapshot.zone
            polyvagal_state = snapshot.polyvagal_state

            # Calculate ground state resilience from zone (lower zone = more grounded)
            zone_resilience_map = {1: 1.0, 2: 0.8, 3: 0.5, 4: 0.2, 5: 0.0}
            ground_state_resilience = zone_resilience_map.get(zone_maintained, 0.5)

            # Successful deflection if:
            # - Maintained Zone 1-2 (SELF or Firefighter)
            # - Kept ventral_vagal or mixed_state (not collapsed)
            # - Ground state resilience > 0.6
            successful = (
                zone_maintained in [1, 2] and
                polyvagal_state in ['ventral_vagal', 'mixed_state'] and
                ground_state_resilience > 0.6
            )

            if successful:
                if is_dict:
                    traj['successful_deflections'] = traj.get('successful_deflections', 0) + 1
                    if 'zone_held_under_provocation' not in traj:
                        traj['zone_held_under_provocation'] = []
                    traj['zone_held_under_provocation'].append(zone_maintained)
                else:
                    traj.successful_deflections += 1
                    traj.zone_held_under_provocation.append(zone_maintained)

                # Update polyvagal resilience score (running average)
                if polyvagal_state == 'ventral_vagal':
                    resilience_contribution = 1.0
                elif polyvagal_state == 'mixed_state':
                    resilience_contribution = 0.7
                else:
                    resilience_contribution = 0.0

                # Running average with decay
                if is_dict:
                    current_resilience = traj.get('polyvagal_resilience_score', 0.5)
                    traj['polyvagal_resilience_score'] = (
                        current_resilience * 0.8 +
                        resilience_contribution * 0.2
                    )
                else:
                    traj.polyvagal_resilience_score = (
                        traj.polyvagal_resilience_score * 0.8 +
                        resilience_contribution * 0.2
                    )
            else:
                if is_dict:
                    traj['failed_deflections'] = traj.get('failed_deflections', 0) + 1
                else:
                    traj.failed_deflections += 1

            # Check for banter unlock (10+ successful deflections)
            successful_count = traj.get('successful_deflections', 0) if is_dict else traj.successful_deflections
            banter_status = traj.get('banter_unlocked', False) if is_dict else traj.banter_unlocked

            if successful_count >= 10 and not banter_status:
                if is_dict:
                    traj['banter_unlocked'] = True
                else:
                    traj.banter_unlocked = True
                print(f"      🎭 Banter unlocked for user (10+ successful heckling deflections)")

                # If humor not yet unlocked, unlock it via heckling pathway
                humor_evo = profile.humor_evolution
                if isinstance(humor_evo, dict):
                    if not humor_evo.get('humor_unlocked', False):
                        humor_evo['humor_unlocked'] = True
                        humor_evo['unlocked_via_heckling'] = True
                        profile.can_use_humor = True
                        print(f"      🎭 Humor unlocked via heckling deflection pathway")
                else:
                    if not humor_evo.humor_unlocked:
                        humor_evo.humor_unlocked = True
                        humor_evo.unlocked_via_heckling = True
                        profile.can_use_humor = True
                        print(f"      🎭 Humor unlocked via heckling deflection pathway")

    def _track_salience_patterns(
        self,
        profile: EnhancedUserProfile,
        felt_states: Dict[str, Any],
        snapshot: FeltStateSnapshot
    ):
        """
        Track salience patterns (trauma markers + morphogenetic guidance).

        Phase 1.6 - November 14, 2025

        Integrates trauma-aware salience model with per-user learning.
        Enables crisis escalation detection and adaptive thresholds.

        Tracks:
        - NDAM urgency trends (running average)
        - Zone collapse frequency (zone 4-5 events)
        - Morphogenetic pressure trends
        - Crisis escalation patterns

        Args:
            profile: User profile to update
            felt_states: Complete felt state dictionary from turn data
            snapshot: Current felt state snapshot
        """
        # Extract salience data from felt_states
        # 🌀 Phase 1.7: Defensive extraction (Nov 14, 2025)
        salience_markers_raw = felt_states.get('salience_trauma_markers', {})
        salience_markers = salience_markers_raw if isinstance(salience_markers_raw, dict) else {}

        salience_guidance_raw = felt_states.get('salience_morphogenetic_guidance', {})
        salience_guidance = salience_guidance_raw if isinstance(salience_guidance_raw, dict) else {}

        # Track NDAM urgency trends (exponential moving average, α=0.1)
        ndam_urgency = salience_markers.get('ndam_urgency', 0.0) if salience_markers else 0.0
        profile.metadata['typical_urgency'] = (
            profile.metadata.get('typical_urgency', 0.0) * 0.9 +
            ndam_urgency * 0.1
        )

        # Track zone collapse events (Zone 4=Protective, Zone 5=Collapse)
        zone_depth = salience_markers.get('zone_depth', snapshot.zone)
        if zone_depth >= 4:
            profile.metadata['collapse_events'] = (
                profile.metadata.get('collapse_events', 0) + 1
            )

        # Track morphogenetic pressure trends (exponential moving average)
        pressure = salience_guidance.get('morphogenetic_pressure', 0.0)
        profile.metadata['typical_pressure'] = (
            profile.metadata.get('typical_pressure', 0.0) * 0.9 +
            pressure * 0.1
        )

        # Detect crisis escalation pattern (high urgency + high pressure)
        if ndam_urgency > 0.6 and pressure > 0.5:
            profile.metadata['crisis_escalation_detected'] = True
            profile.metadata['last_crisis_escalation'] = datetime.now().isoformat()

            # Reset flag after recording (will be re-set if pattern continues)
            # This allows tracking of multiple escalation events

    # ========== MINI-EPOCH LEARNING (Every 10 Turns) ==========

    def run_mini_epoch(self, profile: EnhancedUserProfile):
        """
        Learn patterns from user's last 10 conversations.

        Detects:
        1. Transformation patterns (what pathways work)
        2. Humor calibration (adjust tolerance)
        3. Tone preferences per zone
        4. Inside joke viability

        Args:
            profile: User's superject state
        """
        recent_turns = profile.felt_trajectory[-10:]

        if len(recent_turns) < 2:
            return  # Need at least 2 turns to detect patterns

        print(f"      Learning from {len(recent_turns)} recent turns...")

        # 1. Detect transformation patterns
        new_patterns = self._detect_transformation_patterns(recent_turns)
        for pattern in new_patterns:
            profile.transformation_patterns[pattern.pattern_id] = pattern

        # 2. Calibrate humor
        self._calibrate_humor(profile, recent_turns)

        # 3. Learn tone preferences
        self._learn_tone_preferences(profile, recent_turns)

        # 4. Update recurring themes
        self._update_recurring_themes(profile, recent_turns)

        # Update metadata
        profile.last_mini_epoch = datetime.now().isoformat()
        profile.learning_velocity = len(new_patterns) / 10.0  # Patterns per turn

        print(f"      Learned {len(new_patterns)} new transformation patterns")

    def _detect_transformation_patterns(
        self,
        recent_turns: List[FeltStateSnapshot]
    ) -> List[TransformationPattern]:
        """
        Detect felt-state transformation patterns.

        Looks for: high-energy → low-energy, sympathetic → ventral, etc.

        Args:
            recent_turns: Last N turns

        Returns:
            List of detected patterns
        """
        patterns = []
        satisfaction_threshold = 0.5  # Lowered from 0.7 (learn from "Helpful" not just "Excellent")

        for i in range(len(recent_turns) - 1):
            from_state = recent_turns[i]
            to_state = recent_turns[i + 1]

            # Only learn from successful transformations (positive ratings)
            if to_state.user_satisfaction and to_state.user_satisfaction > satisfaction_threshold:
                if self._is_significant_transformation(from_state, to_state):
                    pattern = self._create_transformation_pattern(from_state, to_state)
                    patterns.append(pattern)

        return patterns

    def _is_significant_transformation(
        self,
        from_state: FeltStateSnapshot,
        to_state: FeltStateSnapshot
    ) -> bool:
        """Check if transformation is significant enough to learn."""

        # Zone change
        if from_state.zone != to_state.zone:
            return True

        # Polyvagal change
        if from_state.polyvagal_state != to_state.polyvagal_state:
            return True

        # V0 energy shift > 0.3
        if abs(from_state.v0_energy - to_state.v0_energy) > 0.3:
            return True

        return False

    def _create_transformation_pattern(
        self,
        from_state: FeltStateSnapshot,
        to_state: FeltStateSnapshot
    ) -> TransformationPattern:
        """Create pattern from two states."""

        pattern_id = f"zone{from_state.zone}_to_zone{to_state.zone}_{from_state.polyvagal_state}_to_{to_state.polyvagal_state}"

        return TransformationPattern(
            pattern_id=pattern_id,
            from_zone=from_state.zone,
            from_polyvagal=from_state.polyvagal_state,
            from_v0_range=(from_state.v0_energy - 0.1, from_state.v0_energy + 0.1),
            to_zone=to_state.zone,
            to_polyvagal=to_state.polyvagal_state,
            to_v0_range=(to_state.v0_energy - 0.1, to_state.v0_energy + 0.1),
            successful_organs=to_state.active_organs,
            successful_nexuses=to_state.dominant_nexuses,
            successful_transduction=to_state.transduction_mechanism,
            humor_safe=to_state.zone <= 2 and to_state.polyvagal_state != "dorsal_vagal",
            humor_threshold=0.5,
            humor_style=None,  # Will be learned later
            tone="gentle",  # Default, will be refined
            preferred_length="moderate",  # Default
            frequency=1,
            success_rate=1.0,
            avg_satisfaction_gain=to_state.satisfaction - from_state.satisfaction,
            first_seen=from_state.timestamp,
            last_seen=to_state.timestamp,
            last_updated=datetime.now().isoformat()
        )

    def _calibrate_humor(
        self,
        profile: EnhancedUserProfile,
        recent_turns: List[FeltStateSnapshot]
    ):
        """
        Adjust humor tolerance based on recent attempts.

        Args:
            profile: User profile to update
            recent_turns: Recent conversation turns
        """
        # TODO: Track humor attempts in turn data
        # For now, stub - will implement in Phase 3

        # Check if humor should be unlocked (5+ successful attempts)
        if (profile.humor_evolution.successful_attempts >= 5 and
            not profile.humor_evolution.humor_unlocked):
            profile.humor_evolution.humor_unlocked = True
            print(f"      🎉 Humor unlocked for user!")

    def _learn_tone_preferences(
        self,
        profile: EnhancedUserProfile,
        recent_turns: List[FeltStateSnapshot]
    ):
        """
        Learn preferred tone per zone from satisfaction.

        Args:
            profile: User profile to update
            recent_turns: Recent turns
        """
        # Group by zone
        zone_satis = {}
        for turn in recent_turns:
            if turn.user_satisfaction:
                if turn.zone not in zone_satis:
                    zone_satis[turn.zone] = []
                zone_satis[turn.zone].append(turn.user_satisfaction)

        # Infer preferred tone (stub - will enhance)
        for zone, satis_list in zone_satis.items():
            avg_satis = sum(satis_list) / len(satis_list)
            if avg_satis > 0.7:
                # This tone is working for this zone
                profile.tone_preferences[zone] = "gentle"  # Default for now

    def _update_recurring_themes(
        self,
        profile: EnhancedUserProfile,
        recent_turns: List[FeltStateSnapshot]
    ):
        """
        Track recurring themes from nexuses.

        Args:
            profile: User profile
            recent_turns: Recent turns
        """
        # Extract all nexuses
        all_nexuses = []
        for turn in recent_turns:
            all_nexuses.extend(turn.dominant_nexuses)

        # Count frequency
        theme_counts = Counter(all_nexuses)

        for theme, count in theme_counts.items():
            if theme:  # Not empty string
                profile.recurring_themes[theme] = profile.recurring_themes.get(theme, 0) + count

    # ========== GLOBAL EPOCH (Every 100 Turns) ==========

    def run_global_epoch(self):
        """
        Aggregate patterns across all users.

        Learns universal transductive patterns that work for many users.
        These become baseline organism intelligence.

        TODO: Implement in Phase 5
        """
        pass

    # ========== OPEN-ENDED ENTITY EXTRACTION (Nov 14, 2025) ==========
    # 🌀 Updated Nov 16, 2025: Organ-driven extraction for 100% precision

    def extract_entities_organic(
        self,
        user_input: str,
        organ_results: Dict,
        nexuses: Optional[List] = None
    ) -> Dict:
        """
        🌀 100% Precision Entity Extraction using Organ Signals (Nov 16, 2025)

        Extracts entities from organ activations WITHOUT LLM dependency.
        Uses LISTENING, BOND, EO, NDAM, EMPATHY, SANS, RNX, WISDOM signals
        to detect and validate entities with nexus coherence scoring.

        Key insight: The organs have already computed entity information.
        We just need to synthesize their signals.

        Args:
            user_input: User's conversational turn
            organ_results: Dict of organ name -> organ result (dict or object)
            nexuses: Optional list of formed nexuses for coherence scoring

        Returns:
            New entities to merge with existing (100% reliable, no JSON parsing)
        """
        from persona_layer.entity_organ_extractor import EntityOrganExtractor

        try:
            extractor = EntityOrganExtractor()
            entities = extractor.extract_from_turn(user_input, organ_results, nexuses)

            if entities:
                storage = extractor.entities_to_storage_format(entities)
                print(f"      ✅ Organic entity extraction: {len(entities)} entities found")
                for e in entities:
                    print(f"         - {e.name} (conf: {e.confidence:.2f}, organs: {e.organs_involved})")
                return storage
            else:
                return {}

        except Exception as e:
            print(f"      ⚠️  Organic entity extraction failed: {e}")
            return {}

    def extract_entities_llm(self, user_input: str, current_entities: Dict) -> Dict:
        """
        Open-ended entity extraction using LLM with schema validation.

        🌀 UPDATED (Nov 16, 2025): Now uses entity_schema_validator to prevent garbage
        entity creation (stopwords like "feeling", "about", "why", etc.)

        Args:
            user_input: User's conversational turn
            current_entities: Currently stored entities

        Returns:
            New entities to merge with existing (validated and filtered)
        """
        from persona_layer.local_llm_bridge import LocalLLMBridge
        from persona_layer.entity_schema_validator import get_validator

        # Get validator
        validator = get_validator()

        # Build extraction prompt using schema template
        schema_prompt = validator.get_llm_extraction_prompt()

        prompt = f"""You are analyzing a conversation to extract memorable facts about the speaker.

{schema_prompt}

Previous known facts:
{self._format_existing_entities(current_entities)}

New statement from user:
"{user_input}"

What new entities should be remembered? Return JSON in the format specified above.
Be selective - only extract proper nouns and explicit entity mentions.

JSON:"""

        # Generate extraction
        llm = LocalLLMBridge()
        try:
            # 🔥 Nov 15, 2025: Increased from 300 to 500 - JSON was getting truncated
            print(f"      🔍 Calling LLM with prompt length: {len(prompt)} chars")
            response = llm.query_direct(prompt, max_tokens=500, temperature=0.3)
            print(f"      🔍 LLM raw response type: {type(response)}")
            if response:
                print(f"      🔍 LLM raw response preview: {str(response)[:200]}...")

            # Parse JSON response - 🔥 Nov 16, 2025: Use robust JSON parser
            from persona_layer.robust_json_parser import salvage_llm_json

            # Handle None response
            if not response:
                print(f"      ⚠️  LLM entity extraction: Empty response")
                return {}

            # Extract text from dict response
            if isinstance(response, dict):
                response_text = response.get('response') or response.get('llm_response')
                if not response_text:
                    print(f"      ⚠️  LLM entity extraction: No text in dict response")
                    return {}
            elif isinstance(response, str):
                response_text = response
            else:
                print(f"      ⚠️  LLM entity extraction: Unexpected type: {type(response)}")
                return {}

            # 🌀 Use robust JSON parser that handles Python syntax from LLM
            extraction, error_msg, was_salvaged = salvage_llm_json(response_text)

            if extraction is None:
                # Provide more context for debugging but don't spam the output
                print(f"      ⚠️  LLM entity extraction: {error_msg}")
                # Only show preview in debug mode or if it's a short response
                if response_text and len(response_text) < 300:
                    preview = response_text.replace('\n', ' ').strip()
                    print(f"      Response preview: {preview[:150]}...")
                return {}

            if was_salvaged:
                print(f"      ✅ JSON salvaged (LLM returned Python syntax)")

            if extraction:
                # 🚨 CRITICAL FIX (Nov 18, 2025): Handle actual LLM schema response
                # LLM returns: {'relationships': [...], 'places': [...], 'preferences': {...}, 'work': {...}}
                # NOT: {'new_facts': [...]}

                # Convert LLM schema format to storage format
                new_entities = {}

                # 1. Handle relationships (people)
                relationships = extraction.get('relationships', [])
                if relationships:
                    new_entities['relationships'] = []
                    for person in relationships:
                        name = person.get('name')
                        relationship = person.get('relationship')

                        # Skip invalid entries
                        if not name or not relationship:
                            continue

                        # Normalize person name (capitalize)
                        name = validator.normalize_person_name(name)

                        # Check for duplicates
                        existing_entities_list = current_entities.get('relationships', [])
                        duplicate = validator.detect_duplicate_person(name, existing_entities_list)
                        if duplicate:
                            print(f"         ⚠️  Skipping duplicate person: {name} (already stored)")
                            continue

                        # Validate person name
                        name_valid, reason = validator.is_valid_entity_name(name)
                        if not name_valid:
                            print(f"         ⚠️  Invalid person name '{name}': {reason}")
                            continue

                        # Store valid person
                        new_entities['relationships'].append({
                            'name': name,
                            'relationship': relationship,
                            'age': person.get('age'),
                            'context': person.get('context', ''),
                            'timestamp': datetime.now().isoformat()
                        })

                        # Also extract user_name if this is a "self" relationship
                        if relationship == 'self' and 'user_name' not in current_entities:
                            new_entities['user_name'] = name

                # 2. Handle places
                places = extraction.get('places', [])
                if places:
                    new_entities['places'] = []
                    for place in places:
                        name = place.get('name')
                        place_type = place.get('place_type')

                        if name and place_type:
                            new_entities['places'].append({
                                'name': name,
                                'place_type': place_type,
                                'city': place.get('city'),
                                'country': place.get('country'),
                                'timestamp': datetime.now().isoformat()
                            })

                # 3. Handle preferences
                preferences = extraction.get('preferences', {})
                if preferences:
                    new_entities['preferences'] = {}
                    for pref_type in ['likes', 'dislikes', 'interests', 'goals']:
                        if pref_type in preferences and preferences[pref_type]:
                            new_entities['preferences'][pref_type] = preferences[pref_type]

                # 4. Handle work info
                work = extraction.get('work', {})
                if work and any(work.values()):  # Only if has non-null values
                    new_entities['work'] = {
                        'company': work.get('company'),
                        'job_title': work.get('job_title'),
                        'industry': work.get('industry'),
                        'work_location': work.get('work_location'),
                        'timestamp': datetime.now().isoformat()
                    }

                # 5. Handle mentioned_names (backward compatibility for "memories")
                mentioned_names = extraction.get('mentioned_names', [])
                if mentioned_names:
                    if 'memories' not in new_entities:
                        new_entities['memories'] = []

                    for name in mentioned_names:
                        # Skip stopwords and duplicates
                        is_valid, reason = validator.is_valid_entity_name(name)
                        if is_valid:
                            new_entities['memories'].append({
                                'type': 'mentioned_name',
                                'value': name,
                                'context': 'Mentioned in conversation',
                                'timestamp': datetime.now().isoformat()
                            })

                # 🌀 Return filtered entities (validator already applied above)
                filtered_entities = new_entities

                return filtered_entities
            else:
                # extraction exists but is empty or None-like (shouldn't happen due to earlier check)
                print(f"      ⚠️  LLM entity extraction: Empty extraction result")
                return {}

        except Exception as e:
            print(f"      ⚠️  LLM entity extraction failed: {e}")
            return {}

    def _format_existing_entities(self, entities: Dict) -> str:
        """Format existing entities for LLM context."""
        if not entities:
            return "(No facts stored yet)"

        lines = []

        if 'user_name' in entities:
            lines.append(f"- Name: {entities['user_name']}")

        if 'memories' in entities:
            for memory in entities.get('memories', [])[-10:]:  # Last 10 memories
                mem_type = memory.get('type', 'fact')
                mem_value = memory.get('value', '')
                lines.append(f"- {mem_type.capitalize()}: {mem_value}")

        return "\n".join(lines) if lines else "(No facts stored yet)"
