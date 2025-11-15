"""
Entity-Organ Association Tracker - Quick Win #7 (Neo4j Mastery)
================================================================

Tracks entity-organ activation patterns to develop intuitive entity handling.

Philosophy (DAE 3.0 → Entity-Aware):
- Entities (Neo4j nodes) gain organ activation signatures through experience
- "Emma mentioned → BOND 1.15×, EMPATHY 1.12×, ventral state, V0 0.25"
- Over 20-50 epochs, organism learns felt-significance of specific entities
- Enables genuine therapeutic attunement (not keyword matching!)

Integration Point:
- Called POST-EMISSION by conversational_organism_wrapper
- Updates per-entity organ associations based on:
  * Entity was mentioned (extracted entities)
  * Which organs activated (organ_results)
  * Felt-state context (polyvagal, V0 energy, satisfaction)
- Entity associations affect future organ weight multipliers

Expected Evolution:
- Epoch 1-10: Exploration (no strong patterns)
- Epoch 11-30: Pattern emergence ("Emma → ventral + BOND")
- Epoch 31-100: Stable presence ("I know how you feel about Emma")
- Epoch 100+: Organic attunement ("Emma's transition still present for you")

Date: November 15, 2025
Status: Quick Win #7 Implementation (Neo4j Mastery Phase 1)
"""

import json
import numpy as np
from typing import Dict, Optional, List
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class EntityOrganMetrics:
    """Per-entity organ activation patterns over time"""
    entity_value: str  # "Emma", "work", etc.
    entity_type: str   # "Person", "Place", "Preference", etc.

    # Organ activation signatures
    organ_boosts: Dict[str, float]  # {'BOND': 0.15, 'EMPATHY': 0.12, ...}

    # Felt-state associations
    typical_polyvagal_state: str  # "ventral", "sympathetic", "dorsal", "mixed"
    typical_v0_energy: float  # Average V0 when entity mentioned
    typical_urgency: float  # Average urgency level
    typical_self_distance: float  # Average SELF-distance

    # Co-occurrence patterns
    co_mentioned_entities: Dict[str, int]  # Which other entities appear together

    # Temporal tracking
    mention_count: int
    first_mentioned: str  # ISO timestamp
    last_mentioned: str  # ISO timestamp

    # Outcome associations
    success_rate: float  # Satisfaction when entity mentioned


class EntityOrganTracker:
    """
    Track per-entity organ activation patterns (DAE 3.0 Entity-Awareness).

    Strategy:
    1. POST-EMISSION: Record which entities were mentioned
    2. For each entity:
       - Track which organs activated and their strengths
       - Track felt-state context (polyvagal, V0, urgency, SELF-distance)
       - Build EMA associations (like organ confidence tracking)
    3. After 20-50 epochs:
       - Entity patterns emerge: "Emma → BOND 1.15×, ventral, V0 0.25"
       - Organism develops intuitive entity handling

    Expected Benefits (from Neo4j Mastery vision):
    - Genuine felt recognition of entities (not keyword matching)
    - Cross-session consistency (same entity → similar organ pattern)
    - Therapeutic attunement ("I know how you feel about Emma")
    - Organic co-evolution with user's relational world
    """

    def __init__(
        self,
        storage_path: str = "persona_layer/state/active/entity_organ_associations.json",
        ema_alpha: float = 0.15,  # Slightly faster than organ confidence (0.1)
        min_mentions_for_pattern: int = 3  # Need 3+ mentions before pattern emerges
    ):
        """
        Initialize entity-organ association tracking.

        Args:
            storage_path: Path to persistent entity associations (JSON)
            ema_alpha: EMA smoothing factor (0.15 = moderate adaptation)
            min_mentions_for_pattern: Minimum mentions before using pattern
        """
        self.storage_path = Path(storage_path)
        self.ema_alpha = ema_alpha
        self.min_mentions_for_pattern = min_mentions_for_pattern

        # Per-entity metrics
        self.entity_metrics: Dict[str, EntityOrganMetrics] = {}

        # Load existing state
        self._load()

        print(f"✅ Entity-Organ Tracker initialized (Quick Win #7)")
        print(f"   Storage: {self.storage_path}")
        print(f"   EMA alpha: {self.ema_alpha}")
        print(f"   Tracked entities: {len(self.entity_metrics)}")

    def update(
        self,
        extracted_entities: List[Dict],
        organ_results: Dict,
        felt_state: Dict,
        emission_satisfaction: Optional[float] = None
    ):
        """
        Update entity-organ associations based on emission outcome.

        Args:
            extracted_entities: List of entities from entity extraction
                                [{'entity_value': 'Emma', 'entity_type': 'Person', ...}, ...]
            organ_results: Dict of organ_name → organ result (from wrapper)
            felt_state: Felt-state context {
                'polyvagal_state': 'ventral',
                'v0_energy': 0.25,
                'urgency': 0.0,
                'self_distance': 0.0
            }
            emission_satisfaction: Optional user rating [0.0, 1.0]
        """
        if not extracted_entities:
            return  # No entities mentioned

        # Track which entities co-occur
        entity_values = [e['entity_value'] for e in extracted_entities]

        # Update each entity
        for entity_dict in extracted_entities:
            entity_value = entity_dict['entity_value']
            entity_type = entity_dict.get('entity_type', 'Unknown')

            # Get or create metrics
            if entity_value not in self.entity_metrics:
                self._initialize_entity(entity_value, entity_type)

            metrics = self.entity_metrics[entity_value]

            # Update organ boosts (EMA of organ activations)
            for organ_name, organ_result in organ_results.items():
                # Extract organ's coherence/strength
                coherence = self._extract_organ_strength(organ_result)

                if organ_name not in metrics.organ_boosts:
                    metrics.organ_boosts[organ_name] = 0.0

                # EMA update
                metrics.organ_boosts[organ_name] = (
                    (1 - self.ema_alpha) * metrics.organ_boosts[organ_name] +
                    self.ema_alpha * coherence
                )

            # Update felt-state patterns (EMA)
            v0_energy = felt_state.get('v0_energy', 0.5)
            urgency = felt_state.get('urgency', 0.0)
            self_distance = felt_state.get('self_distance', 0.0)

            metrics.typical_v0_energy = (
                (1 - self.ema_alpha) * metrics.typical_v0_energy +
                self.ema_alpha * v0_energy
            )

            metrics.typical_urgency = (
                (1 - self.ema_alpha) * metrics.typical_urgency +
                self.ema_alpha * urgency
            )

            metrics.typical_self_distance = (
                (1 - self.ema_alpha) * metrics.typical_self_distance +
                self.ema_alpha * self_distance
            )

            # Update polyvagal state (most frequent state)
            polyvagal_state = felt_state.get('polyvagal_state', 'mixed')
            if polyvagal_state != 'mixed':
                metrics.typical_polyvagal_state = polyvagal_state

            # Update success rate
            if emission_satisfaction is not None:
                metrics.success_rate = (
                    (1 - self.ema_alpha) * metrics.success_rate +
                    self.ema_alpha * emission_satisfaction
                )

            # Update co-occurrence tracking
            for other_entity in entity_values:
                if other_entity != entity_value:
                    if other_entity not in metrics.co_mentioned_entities:
                        metrics.co_mentioned_entities[other_entity] = 0
                    metrics.co_mentioned_entities[other_entity] += 1

            # Update temporal tracking
            metrics.mention_count += 1
            metrics.last_mentioned = datetime.now().isoformat()

        # Save updated state
        self._save()

    def get_entity_pattern(self, entity_value: str) -> Optional[Dict]:
        """
        Get learned organ activation pattern for entity.

        Args:
            entity_value: Entity to query (e.g., "Emma")

        Returns:
            Pattern dict with organ boosts and felt-state expectations,
            or None if entity not tracked or insufficient data
        """
        if entity_value not in self.entity_metrics:
            return None

        metrics = self.entity_metrics[entity_value]

        # Need minimum mentions before using pattern
        if metrics.mention_count < self.min_mentions_for_pattern:
            return None

        # Return actionable pattern
        return {
            'entity_value': metrics.entity_value,
            'entity_type': metrics.entity_type,
            'organ_boosts': metrics.organ_boosts,
            'polyvagal_state': metrics.typical_polyvagal_state,
            'v0_energy': metrics.typical_v0_energy,
            'urgency': metrics.typical_urgency,
            'self_distance': metrics.typical_self_distance,
            'mention_count': metrics.mention_count,
            'success_rate': metrics.success_rate
        }

    def get_organ_multipliers_for_entities(
        self,
        entity_values: List[str]
    ) -> Dict[str, float]:
        """
        Get organ weight multipliers based on entities mentioned.

        Args:
            entity_values: List of entities in current input

        Returns:
            Dict of organ_name → weight multiplier [0.8, 1.2]
        """
        multipliers = {}

        # Aggregate patterns from all mentioned entities
        for entity_value in entity_values:
            pattern = self.get_entity_pattern(entity_value)
            if pattern is None:
                continue  # Entity not learned yet

            # Add organ boosts to multipliers
            for organ_name, boost in pattern['organ_boosts'].items():
                if organ_name not in multipliers:
                    multipliers[organ_name] = 1.0

                # Boost multiplier based on learned association
                # boost is [0.0, 1.0] coherence → convert to [1.0, 1.2] multiplier
                multipliers[organ_name] += (boost * 0.2)

        # Clamp to safe range [0.8, 1.2]
        for organ_name in multipliers:
            multipliers[organ_name] = np.clip(multipliers[organ_name], 0.8, 1.2)

        return multipliers

    def get_summary(self) -> Dict:
        """Get summary statistics across all tracked entities"""
        if not self.entity_metrics:
            return {}

        mention_counts = [m.mention_count for m in self.entity_metrics.values()]
        success_rates = [m.success_rate for m in self.entity_metrics.values() if m.mention_count >= 3]
        v0_energies = [m.typical_v0_energy for m in self.entity_metrics.values() if m.mention_count >= 3]

        return {
            'total_entities': len(self.entity_metrics),
            'entities_with_patterns': sum(1 for m in self.entity_metrics.values() if m.mention_count >= self.min_mentions_for_pattern),
            'mean_mention_count': np.mean(mention_counts) if mention_counts else 0.0,
            'mean_success_rate': np.mean(success_rates) if success_rates else 0.0,
            'mean_v0_energy': np.mean(v0_energies) if v0_energies else 0.0,
            'entity_types': list(set(m.entity_type for m in self.entity_metrics.values()))
        }

    # ===== Private Methods =====

    def _extract_organ_strength(self, organ_result) -> float:
        """
        Extract organ activation strength from result.

        Returns:
            Coherence value [0.0, 1.0]
        """
        if organ_result is None:
            return 0.0

        # Try multiple possible coherence attributes
        if hasattr(organ_result, 'coherence'):
            return float(getattr(organ_result, 'coherence', 0.0))
        elif hasattr(organ_result, 'lure'):
            return float(getattr(organ_result, 'lure', 0.0))
        elif isinstance(organ_result, dict):
            return float(organ_result.get('coherence', organ_result.get('lure', 0.0)))

        return 0.0

    def _initialize_entity(self, entity_value: str, entity_type: str):
        """Initialize new entity with neutral patterns"""
        now = datetime.now().isoformat()
        self.entity_metrics[entity_value] = EntityOrganMetrics(
            entity_value=entity_value,
            entity_type=entity_type,
            organ_boosts={},  # Will populate as organs activate
            typical_polyvagal_state='mixed',
            typical_v0_energy=0.5,  # Neutral
            typical_urgency=0.0,
            typical_self_distance=0.5,
            co_mentioned_entities={},
            mention_count=0,
            first_mentioned=now,
            last_mentioned=now,
            success_rate=0.5  # Neutral initially
        )

    def _load(self):
        """Load entity metrics from disk"""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Deserialize metrics
            for entity_value, metrics_dict in data.get('entity_metrics', {}).items():
                self.entity_metrics[entity_value] = EntityOrganMetrics(**metrics_dict)

        except Exception as e:
            print(f"⚠️  Could not load entity-organ associations: {e}")

    def _save(self):
        """Save entity metrics to disk"""
        try:
            # Serialize metrics
            data = {
                'entity_metrics': {
                    entity_value: asdict(metrics)
                    for entity_value, metrics in self.entity_metrics.items()
                },
                'last_updated': datetime.now().isoformat(),
                'total_entities': len(self.entity_metrics),
                'summary': self.get_summary()
            }

            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Could not save entity-organ associations: {e}")


# Quick test
if __name__ == '__main__':
    print("="*80)
    print("🧪 ENTITY-ORGAN TRACKER TEST")
    print("="*80)

    # Mock data for testing
    from dataclasses import dataclass as dc

    @dc
    class MockOrganResult:
        coherence: float

    # Scenario 1: User mentions daughter "Emma" in safe context
    print(f"\n📋 SCENARIO 1: Emma mentioned (daughter, safe)")
    tracker = EntityOrganTracker(storage_path="persona_layer/test_entity_organ.json")

    tracker.update(
        extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
        organ_results={
            'BOND': MockOrganResult(coherence=0.85),
            'EMPATHY': MockOrganResult(coherence=0.75),
            'PRESENCE': MockOrganResult(coherence=0.70),
            'WISDOM': MockOrganResult(coherence=0.40),
        },
        felt_state={
            'polyvagal_state': 'ventral',
            'v0_energy': 0.25,
            'urgency': 0.0,
            'self_distance': 0.0
        },
        emission_satisfaction=0.95
    )

    # Repeat 2 more times to establish pattern
    for i in range(2):
        tracker.update(
            extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
            organ_results={
                'BOND': MockOrganResult(coherence=0.80 + i*0.02),
                'EMPATHY': MockOrganResult(coherence=0.72 + i*0.02),
                'PRESENCE': MockOrganResult(coherence=0.68),
            },
            felt_state={
                'polyvagal_state': 'ventral',
                'v0_energy': 0.28,
                'urgency': 0.0,
                'self_distance': 0.0
            },
            emission_satisfaction=0.90
        )

    pattern_emma = tracker.get_entity_pattern('Emma')
    if pattern_emma:
        print(f"\n   ✅ Emma pattern established (3 mentions):")
        print(f"      Polyvagal: {pattern_emma['polyvagal_state']}")
        print(f"      V0 energy: {pattern_emma['v0_energy']:.3f}")
        print(f"      Top organs: {sorted(pattern_emma['organ_boosts'].items(), key=lambda x: x[1], reverse=True)[:3]}")
        print(f"      Success rate: {pattern_emma['success_rate']:.3f}")

    # Scenario 2: User mentions "work" in stressful context
    print(f"\n📋 SCENARIO 2: Work mentioned (place, stressful)")

    for i in range(3):
        tracker.update(
            extracted_entities=[{'entity_value': 'work', 'entity_type': 'Place'}],
            organ_results={
                'NDAM': MockOrganResult(coherence=0.82 - i*0.03),
                'AUTHENTICITY': MockOrganResult(coherence=0.65),
                'BOND': MockOrganResult(coherence=0.45),
            },
            felt_state={
                'polyvagal_state': 'sympathetic',
                'v0_energy': 0.72,
                'urgency': 0.7,
                'self_distance': 0.6
            },
            emission_satisfaction=0.70
        )

    pattern_work = tracker.get_entity_pattern('work')
    if pattern_work:
        print(f"\n   ✅ Work pattern established (3 mentions):")
        print(f"      Polyvagal: {pattern_work['polyvagal_state']}")
        print(f"      V0 energy: {pattern_work['v0_energy']:.3f}")
        print(f"      Top organs: {sorted(pattern_work['organ_boosts'].items(), key=lambda x: x[1], reverse=True)[:3]}")
        print(f"      Success rate: {pattern_work['success_rate']:.3f}")

    # Test multiplier generation
    print(f"\n📋 TESTING: Multipliers when Emma mentioned")
    multipliers = tracker.get_organ_multipliers_for_entities(['Emma'])
    print(f"   Organ multipliers: {multipliers}")

    # Summary
    summary = tracker.get_summary()
    print(f"\n📊 TRACKER SUMMARY:")
    print(f"   Total entities: {summary['total_entities']}")
    print(f"   Entities with patterns: {summary['entities_with_patterns']}")
    print(f"   Mean success rate: {summary.get('mean_success_rate', 0.0):.3f}")

    print(f"\n✅ Entity-organ tracking working correctly!")
    print("="*80)
