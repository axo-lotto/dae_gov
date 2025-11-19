"""
Entity Lifecycle Management - Dual Memory Phase 1
==================================================

Manages entity updates, deprecation, and salience decay over time.

Philosophy:
- Entities are not static - they evolve through accumulated experience
- Recency matters: Recent mentions carry higher salience
- Confidence grows with repeated coherent mentions
- Contradictory updates require reconciliation
- Entities can become deprecated if not mentioned over time

Architecture:
1. Entity Update Detection (when entity properties change)
2. Contradiction Reconciliation (when new info conflicts with stored)
3. Salience Decay (time-based relevance reduction)
4. Deprecation (entities not mentioned in N days become inactive)
5. Versioning (track entity evolution over time)

Expected Flow:
- Turn 1: "Emma is my daughter" → Entity created (version 1)
- Turn 5: "Emma is 6 years old" → Entity updated (version 2)
- Turn 100: "Emma just turned 7" → Entity updated (version 3), contradiction reconciled
- Turn 500: Emma not mentioned in 90 days → Salience decayed, marked deprecated

Integration Points:
- Called by organism wrapper POST-EMISSION
- Updates Neo4j entity properties
- Tracks entity evolution in superject state

Date: November 18, 2025
Status: Phase 1 - Dual Memory Architecture Implementation
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum


class EntityStatus(Enum):
    """Entity lifecycle status"""
    ACTIVE = "active"           # Recently mentioned, high confidence
    FADING = "fading"          # Not mentioned recently, decaying salience
    DEPRECATED = "deprecated"  # Not mentioned in 90+ days, low salience
    CONFLICTING = "conflicting" # Contains contradictory information


@dataclass
class EntityVersion:
    """Snapshot of entity state at a specific time"""
    version_number: int
    timestamp: str
    properties: Dict[str, Any]
    mention_context: str  # What triggered this update
    confidence: float     # Confidence in this version's accuracy
    source: str          # "user_direct" | "inferred" | "corrected"


@dataclass
class EntityUpdate:
    """Proposed update to an entity"""
    entity_value: str
    entity_type: str
    property_name: str
    old_value: Any
    new_value: Any
    confidence: float
    timestamp: str
    context: str


@dataclass
class EntityLifecycleState:
    """Complete lifecycle state for an entity"""
    entity_value: str
    entity_type: str
    current_properties: Dict[str, Any]

    # Lifecycle tracking
    status: EntityStatus
    salience: float            # [0.0, 1.0] - Current relevance
    confidence: float          # [0.0, 1.0] - Confidence in stored properties
    version_number: int        # Current version

    # Temporal tracking
    first_mentioned: str       # ISO timestamp
    last_mentioned: str        # ISO timestamp
    mention_count: int
    days_since_mention: int

    # Evolution tracking
    version_history: List[EntityVersion]
    pending_updates: List[EntityUpdate]  # Conflicting updates awaiting reconciliation

    # Decay parameters
    salience_decay_rate: float  # How fast salience decays per day
    deprecation_threshold_days: int  # Days until deprecated


class EntityLifecycleManager:
    """
    Manage entity lifecycle: updates, deprecation, salience decay.

    Strategy:
    1. Track entity versions (what changed, when, why)
    2. Detect contradictions (new info conflicts with old)
    3. Apply time-based salience decay
    4. Mark entities deprecated after inactivity
    5. Provide update recommendations to Neo4j

    Expected Benefits:
    - Dynamic entity evolution (not static snapshots)
    - Contradiction awareness (flagged for user clarification)
    - Time-aware relevance (recent entities prioritized)
    - Clean memory (deprecated entities don't clutter queries)
    """

    def __init__(
        self,
        default_salience_decay_rate: float = 0.02,  # 2% decay per day
        deprecation_threshold_days: int = 90,       # 3 months → deprecated
        fading_threshold_days: int = 30,            # 1 month → fading
        storage_path: str = "persona_layer/entity_lifecycle_state.json"
    ):
        """
        Initialize entity lifecycle manager.

        Args:
            default_salience_decay_rate: Daily salience decay (0.02 = 2% per day)
            deprecation_threshold_days: Days until entity marked deprecated
            fading_threshold_days: Days until entity status becomes "fading"
            storage_path: Where to persist lifecycle state
        """
        self.default_salience_decay_rate = default_salience_decay_rate
        self.deprecation_threshold_days = deprecation_threshold_days
        self.fading_threshold_days = fading_threshold_days
        self.storage_path = storage_path

        # Load existing lifecycle state
        self.entity_states: Dict[str, EntityLifecycleState] = {}
        self._load_state()

    def process_entity_mention(
        self,
        entity_value: str,
        entity_type: str,
        extracted_properties: Dict[str, Any],
        mention_context: str,
        confidence: float = 0.8
    ) -> Tuple[EntityLifecycleState, List[EntityUpdate]]:
        """
        Process an entity mention and detect any lifecycle changes.

        Args:
            entity_value: Entity identifier ("Emma", "work", etc.)
            entity_type: Entity category ("Person", "Place", etc.)
            extracted_properties: Properties extracted from this mention
            mention_context: Text that triggered this mention
            confidence: Confidence in extracted properties

        Returns:
            (updated_state, pending_updates)
            - updated_state: New lifecycle state
            - pending_updates: Updates that need reconciliation (if contradictory)
        """
        now = datetime.now().isoformat()

        # Get existing state or create new
        if entity_value in self.entity_states:
            state = self.entity_states[entity_value]

            # Update temporal tracking
            state.last_mentioned = now
            state.mention_count += 1
            state.days_since_mention = 0

            # Restore salience (mentioned again!)
            state.salience = min(1.0, state.salience + 0.2)  # +20% boost
            state.status = EntityStatus.ACTIVE

        else:
            # New entity
            state = EntityLifecycleState(
                entity_value=entity_value,
                entity_type=entity_type,
                current_properties=extracted_properties.copy(),
                status=EntityStatus.ACTIVE,
                salience=1.0,  # Maximum salience when first mentioned
                confidence=confidence,
                version_number=1,
                first_mentioned=now,
                last_mentioned=now,
                mention_count=1,
                days_since_mention=0,
                version_history=[EntityVersion(
                    version_number=1,
                    timestamp=now,
                    properties=extracted_properties.copy(),
                    mention_context=mention_context,
                    confidence=confidence,
                    source="user_direct"
                )],
                pending_updates=[],
                salience_decay_rate=self.default_salience_decay_rate,
                deprecation_threshold_days=self.deprecation_threshold_days
            )
            self.entity_states[entity_value] = state

        # Detect property updates
        pending_updates = []
        for prop_name, new_value in extracted_properties.items():
            old_value = state.current_properties.get(prop_name)

            if old_value is None:
                # New property - add it
                state.current_properties[prop_name] = new_value
                state.version_number += 1
                state.version_history.append(EntityVersion(
                    version_number=state.version_number,
                    timestamp=now,
                    properties=state.current_properties.copy(),
                    mention_context=mention_context,
                    confidence=confidence,
                    source="user_direct"
                ))

            elif old_value != new_value:
                # Property changed - check for contradiction
                update = EntityUpdate(
                    entity_value=entity_value,
                    entity_type=entity_type,
                    property_name=prop_name,
                    old_value=old_value,
                    new_value=new_value,
                    confidence=confidence,
                    timestamp=now,
                    context=mention_context
                )

                # Auto-reconcile if new value has higher confidence
                if confidence > state.confidence:
                    # Accept update
                    state.current_properties[prop_name] = new_value
                    state.confidence = confidence
                    state.version_number += 1
                    state.version_history.append(EntityVersion(
                        version_number=state.version_number,
                        timestamp=now,
                        properties=state.current_properties.copy(),
                        mention_context=mention_context,
                        confidence=confidence,
                        source="corrected"
                    ))
                else:
                    # Flag for reconciliation
                    state.status = EntityStatus.CONFLICTING
                    state.pending_updates.append(update)
                    pending_updates.append(update)

        self._save_state()
        return state, pending_updates

    def apply_time_decay(self, current_time: Optional[datetime] = None) -> Dict[str, EntityLifecycleState]:
        """
        Apply time-based salience decay to all entities.

        Args:
            current_time: Current timestamp (defaults to now)

        Returns:
            Dict of entity states that changed status
        """
        if current_time is None:
            current_time = datetime.now()

        changed_states = {}

        for entity_value, state in self.entity_states.items():
            # Calculate days since last mention
            last_mentioned = datetime.fromisoformat(state.last_mentioned)
            days_elapsed = (current_time - last_mentioned).days
            state.days_since_mention = days_elapsed

            if days_elapsed == 0:
                continue  # No decay on same day

            # Apply exponential decay
            decay_factor = (1.0 - state.salience_decay_rate) ** days_elapsed
            old_salience = state.salience
            state.salience = max(0.0, state.salience * decay_factor)

            # Update status based on time
            old_status = state.status

            if days_elapsed >= state.deprecation_threshold_days:
                state.status = EntityStatus.DEPRECATED
            elif days_elapsed >= self.fading_threshold_days:
                state.status = EntityStatus.FADING

            if state.status != old_status or abs(state.salience - old_salience) > 0.05:
                changed_states[entity_value] = state

        if changed_states:
            self._save_state()

        return changed_states

    def get_active_entities(self, min_salience: float = 0.3) -> List[EntityLifecycleState]:
        """
        Get entities with ACTIVE or FADING status and sufficient salience.

        Args:
            min_salience: Minimum salience threshold

        Returns:
            List of active entity states sorted by salience (highest first)
        """
        active = [
            state for state in self.entity_states.values()
            if state.status in [EntityStatus.ACTIVE, EntityStatus.FADING]
            and state.salience >= min_salience
        ]

        active.sort(key=lambda s: s.salience, reverse=True)
        return active

    def get_deprecated_entities(self) -> List[EntityLifecycleState]:
        """Get all deprecated entities (candidates for archival)"""
        return [
            state for state in self.entity_states.values()
            if state.status == EntityStatus.DEPRECATED
        ]

    def get_conflicting_entities(self) -> List[EntityLifecycleState]:
        """Get entities with pending updates (contradictions to resolve)"""
        return [
            state for state in self.entity_states.values()
            if state.status == EntityStatus.CONFLICTING
            and len(state.pending_updates) > 0
        ]

    def reconcile_update(
        self,
        entity_value: str,
        update_index: int,
        accept: bool,
        reconciliation_note: str = ""
    ) -> EntityLifecycleState:
        """
        Manually reconcile a pending update.

        Args:
            entity_value: Entity to update
            update_index: Index in pending_updates list
            accept: True to accept update, False to reject
            reconciliation_note: Why this decision was made

        Returns:
            Updated entity state
        """
        state = self.entity_states[entity_value]

        if update_index >= len(state.pending_updates):
            raise ValueError(f"Update index {update_index} out of range")

        update = state.pending_updates[update_index]

        if accept:
            # Apply update
            state.current_properties[update.property_name] = update.new_value
            state.version_number += 1
            state.version_history.append(EntityVersion(
                version_number=state.version_number,
                timestamp=datetime.now().isoformat(),
                properties=state.current_properties.copy(),
                mention_context=f"Manual reconciliation: {reconciliation_note}",
                confidence=update.confidence,
                source="corrected"
            ))

        # Remove from pending
        state.pending_updates.pop(update_index)

        # Update status
        if len(state.pending_updates) == 0:
            state.status = EntityStatus.ACTIVE

        self._save_state()
        return state

    def get_entity_state(self, entity_value: str) -> Optional[EntityLifecycleState]:
        """Get lifecycle state for a specific entity"""
        return self.entity_states.get(entity_value)

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for entity lifecycle"""
        total = len(self.entity_states)

        if total == 0:
            return {
                'total_entities': 0,
                'active': 0,
                'fading': 0,
                'deprecated': 0,
                'conflicting': 0,
                'mean_salience': 0.0,
                'mean_days_since_mention': 0.0
            }

        status_counts = {
            EntityStatus.ACTIVE: 0,
            EntityStatus.FADING: 0,
            EntityStatus.DEPRECATED: 0,
            EntityStatus.CONFLICTING: 0
        }

        total_salience = 0.0
        total_days = 0.0

        for state in self.entity_states.values():
            status_counts[state.status] += 1
            total_salience += state.salience
            total_days += state.days_since_mention

        return {
            'total_entities': total,
            'active': status_counts[EntityStatus.ACTIVE],
            'fading': status_counts[EntityStatus.FADING],
            'deprecated': status_counts[EntityStatus.DEPRECATED],
            'conflicting': status_counts[EntityStatus.CONFLICTING],
            'mean_salience': total_salience / total,
            'mean_days_since_mention': total_days / total,
            'entities_by_salience': sorted(
                [(s.entity_value, s.salience) for s in self.entity_states.values()],
                key=lambda x: x[1],
                reverse=True
            )[:10]  # Top 10
        }

    # ===== Private Methods =====

    def _load_state(self):
        """Load entity lifecycle state from JSON"""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            for entity_value, state_dict in data.get('entities', {}).items():
                # Convert enum
                state_dict['status'] = EntityStatus(state_dict['status'])

                # Convert version history
                state_dict['version_history'] = [
                    EntityVersion(**v) for v in state_dict['version_history']
                ]

                # Convert pending updates
                state_dict['pending_updates'] = [
                    EntityUpdate(**u) for u in state_dict['pending_updates']
                ]

                self.entity_states[entity_value] = EntityLifecycleState(**state_dict)

        except FileNotFoundError:
            # First run - no state yet
            pass
        except Exception as e:
            print(f"⚠️  EntityLifecycleManager: Error loading state: {e}")

    def _save_state(self):
        """Save entity lifecycle state to JSON"""
        try:
            data = {
                'entities': {},
                'last_updated': datetime.now().isoformat()
            }

            for entity_value, state in self.entity_states.items():
                state_dict = asdict(state)

                # Convert enum
                state_dict['status'] = state.status.value

                data['entities'][entity_value] = state_dict

            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  EntityLifecycleManager: Error saving state: {e}")


# Quick test
if __name__ == '__main__':
    print("=" * 80)
    print("🧪 ENTITY LIFECYCLE MANAGER TEST")
    print("=" * 80)

    manager = EntityLifecycleManager(
        storage_path="persona_layer/test_entity_lifecycle.json"
    )

    # Scenario 1: New entity mention
    print("\n📋 SCENARIO 1: New entity (Emma, daughter)")
    state1, updates1 = manager.process_entity_mention(
        entity_value="Emma",
        entity_type="Person",
        extracted_properties={"relation": "daughter", "age": 6},
        mention_context="Emma is my 6-year-old daughter",
        confidence=0.9
    )

    print(f"   Entity: {state1.entity_value}")
    print(f"   Status: {state1.status.value}")
    print(f"   Salience: {state1.salience:.3f}")
    print(f"   Version: {state1.version_number}")
    print(f"   Properties: {state1.current_properties}")

    # Scenario 2: Property update (age change)
    print("\n📋 SCENARIO 2: Property update (Emma turned 7)")
    state2, updates2 = manager.process_entity_mention(
        entity_value="Emma",
        entity_type="Person",
        extracted_properties={"relation": "daughter", "age": 7},
        mention_context="Emma just turned 7!",
        confidence=0.95
    )

    print(f"   Updated age: {state2.current_properties['age']}")
    print(f"   Version: {state2.version_number}")
    print(f"   Confidence: {state2.confidence:.3f}")
    print(f"   Mention count: {state2.mention_count}")

    # Scenario 3: Time decay
    print("\n📋 SCENARIO 3: Time decay (30 days later)")
    future_time = datetime.now() + timedelta(days=30)
    changed = manager.apply_time_decay(current_time=future_time)

    emma_state = manager.get_entity_state("Emma")
    print(f"   Days since mention: {emma_state.days_since_mention}")
    print(f"   Salience: {emma_state.salience:.3f} (decayed from 1.0)")
    print(f"   Status: {emma_state.status.value}")

    # Scenario 4: Deprecated entity
    print("\n📋 SCENARIO 4: Deprecated entity (100 days later)")
    future_time_2 = datetime.now() + timedelta(days=100)
    changed_2 = manager.apply_time_decay(current_time=future_time_2)

    emma_state_2 = manager.get_entity_state("Emma")
    print(f"   Days since mention: {emma_state_2.days_since_mention}")
    print(f"   Salience: {emma_state_2.salience:.3f}")
    print(f"   Status: {emma_state_2.status.value}")

    # Summary statistics
    print("\n📊 SUMMARY STATISTICS")
    stats = manager.get_summary_statistics()
    print(f"   Total entities: {stats['total_entities']}")
    print(f"   Active: {stats['active']}")
    print(f"   Fading: {stats['fading']}")
    print(f"   Deprecated: {stats['deprecated']}")
    print(f"   Mean salience: {stats['mean_salience']:.3f}")

    print("\n✅ Entity lifecycle manager operational!")
    print("=" * 80)
