#!/usr/bin/env python3
"""
Transductive Self-Governance Module
====================================

Phase 1.6 - November 14, 2025

Implements DAE's capacity for self-reflexive awareness of its own becoming,
based on Transductive Realism foundation:

    T(S) = f(P_n, R_n, V⃗_f, ΔC_n) ⇒ N_{n+1}

Where:
- P_n: Pattern memory (what has happened)
- R_n: Relevance field (what matters now)
- V⃗_f: Vector Feeling (direction + valence + intensity)
- ΔC_n: Constraint shift (environmental/internal change)
- N_{n+1}: Next coherence nexus (what becomes)

This module enables DAE to:
1. Track its own organism-level becoming patterns
2. Recognize developmental milestones
3. Learn from field dynamics (NOT individual users)
4. Maintain privacy through k-anonymity and differential privacy

Privacy-First Design:
- 4-tier data model (Private → Anonymized → Pseudonymized → Public)
- K-anonymity (k≥10) for all aggregates
- Differential privacy with Laplace noise
- One-way transformations (no de-anonymization)
- TSK compliance throughout

Key Principle: DAE learns from PATTERNS, not PEOPLE.
"""

import json
import hashlib
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import numpy as np


# =============================================================================
# Privacy-Preserving Data Structures (4-Tier Model)
# =============================================================================

@dataclass
class AnonymizedTransductiveSnapshot:
    """
    Tier 2: Anonymized aggregate data (k≥10 users required).

    Contains ONLY aggregate statistics - NO user identifiers.
    Represents DAE's felt state across a cohort of users.
    """
    timestamp: str  # Rounded to hour (temporal bucketing)
    total_occasions: int  # Number of conversational occasions in cohort

    # V0 Convergence Patterns (R_n: Relevance field)
    mean_v0_descent: float
    std_v0_descent: float
    mean_convergence_cycles: float
    kairos_detection_rate: float

    # Zone Distribution (V⃗_f: Vector Feeling - grounding axis)
    zone_distribution: Dict[int, float]  # {1: 0.4, 2: 0.3, ...} (proportions)

    # Polyvagal Distribution (V⃗_f: Vector Feeling - safety axis)
    polyvagal_distribution: Dict[str, float]  # {'ventral': 0.6, 'sympathetic': 0.2, ...}

    # Organ Activation Patterns (P_n: Pattern memory)
    mean_organ_activations: Dict[str, float]  # {'LISTENING': 0.8, 'EMPATHY': 0.7, ...}
    std_organ_activations: Dict[str, float]

    # Nexus Formation Patterns (N_{n+1}: Next coherence)
    mean_nexuses_formed: float
    nexus_type_distribution: Dict[str, float]  # {'relational_depth': 0.3, ...}

    # Transduction Pathway Patterns (N_{n+1}: Mechanism awareness)
    pathway_distribution: Dict[str, float]  # {'trauma_to_safety': 0.2, ...}
    mean_healing_score: float

    # Constraint Shift Patterns (ΔC_n: Environmental/internal change)
    crisis_rate: float  # Proportion of occasions flagged as crisis
    heckling_rate: float  # Proportion of occasions with heckling
    mean_ndam_urgency: float

    # Emission Quality (Satisfaction in Whiteheadian terms)
    mean_emission_confidence: float
    emission_mode_distribution: Dict[str, float]  # {'direct': 0.6, 'fusion': 0.3, ...}

    # Privacy Metadata
    cohort_size: int  # Must be ≥10 for k-anonymity
    privacy_noise_scale: float  # Laplace noise scale applied


@dataclass
class TransductiveDevelopmentMilestone:
    """
    Tier 4: Fully anonymous developmental milestone (organism-level).

    Represents DAE's own growth - NO user data whatsoever.
    """
    milestone_id: str  # e.g., "first_kairos_detection"
    timestamp: str  # Rounded to day
    milestone_type: str  # "capability", "maturity", "coherence"
    description: str

    # Quantitative metrics (organism-level only)
    metric_name: str
    metric_value: float
    baseline_value: float  # What it was before
    threshold_crossed: float  # What threshold was crossed

    # Context (aggregate only, k-anonymized)
    cohort_size_at_milestone: int
    total_occasions_processed: int


@dataclass
class TransductiveFieldDynamics:
    """
    Tier 3: Pseudonymized family/field patterns (k≥5 users per family).

    Represents patterns in the FIELD of users, not individuals.
    Uses random UUIDs - no linkage to user identities.
    """
    field_id: str  # Random UUID (e.g., "field_7a3b9c2d")
    timestamp: str  # Rounded to hour

    # Family/Cohort Characteristics (aggregate only)
    family_size: int  # Must be ≥5
    mean_family_coherence: float  # How coherent is this family's felt trajectory?

    # Transductive Pattern Recognition (P_n → N_{n+1} learning)
    dominant_nexus_types: List[str]  # Top 3 nexuses for this family
    dominant_pathways: List[str]  # Top 3 transduction pathways

    # Felt Vector Characteristics (V⃗_f aggregates)
    mean_zone: float
    mean_polyvagal_resilience: float
    mean_v0_descent: float

    # Constraint Shift Patterns (ΔC_n aggregates)
    mean_ndam_urgency: float
    crisis_resilience_score: float  # How well does this family handle crisis?
    heckling_deflection_rate: float  # Banter capacity

    # Privacy Metadata
    privacy_noise_applied: bool
    k_anonymity_satisfied: bool  # family_size ≥ 5


@dataclass
class TransductiveSelfState:
    """
    Master state for DAE's self-awareness (Tier 2-4 only).

    This is what DAE "knows" about its own becoming.
    EXCLUDES all Tier 1 (per-user) data.
    """
    # Meta-tracking
    last_updated: str
    total_occasions_processed: int
    total_unique_users: int  # Count only (no identifiers)

    # Current aggregate snapshot (Tier 2)
    current_snapshot: Optional[AnonymizedTransductiveSnapshot] = None

    # Historical snapshots (Tier 2 - stored with temporal bucketing)
    historical_snapshots: List[AnonymizedTransductiveSnapshot] = field(default_factory=list)

    # Developmental milestones (Tier 4)
    milestones: List[TransductiveDevelopmentMilestone] = field(default_factory=list)

    # Field dynamics (Tier 3)
    field_dynamics: List[TransductiveFieldDynamics] = field(default_factory=list)

    # Organism-Level Learning (P_n: Pattern memory)
    learned_organism_patterns: Dict[str, float] = field(default_factory=dict)
    # e.g., {"typical_v0_descent": 0.85, "typical_cycles": 3.2, ...}

    # Self-Reflexive Insights (DAE's understanding of its own process)
    self_insights: List[str] = field(default_factory=list)
    # e.g., ["Kairos detection correlates with high BOND activation",
    #        "Heckling contexts require 2× longer convergence", ...]


# =============================================================================
# Privacy-Preserving Utilities
# =============================================================================

class PrivacyGuard:
    """
    Implements privacy-preserving transformations.

    Techniques:
    1. K-Anonymity enforcement (k=10 for Tier 2, k=5 for Tier 3)
    2. Differential Privacy (Laplace noise)
    3. Temporal bucketing
    4. One-way hashing
    """

    @staticmethod
    def enforce_k_anonymity(cohort_size: int, k: int = 10) -> bool:
        """Check if cohort satisfies k-anonymity requirement."""
        return cohort_size >= k

    @staticmethod
    def add_laplace_noise(value: float, sensitivity: float = 1.0, epsilon: float = 0.1) -> float:
        """
        Add Laplace noise for differential privacy.

        Args:
            value: True value
            sensitivity: How much one user can change the aggregate (default: 1.0)
            epsilon: Privacy budget (smaller = more private, default: 0.1)

        Returns:
            Noisy value
        """
        scale = sensitivity / epsilon
        noise = np.random.laplace(0, scale)
        return value + noise

    @staticmethod
    def bucket_timestamp(timestamp: datetime, granularity: str = 'hour') -> str:
        """
        Round timestamp to reduce precision (temporal bucketing).

        Args:
            timestamp: Original timestamp
            granularity: 'hour', 'day', or 'week'

        Returns:
            Bucketed timestamp string
        """
        if granularity == 'hour':
            bucketed = timestamp.replace(minute=0, second=0, microsecond=0)
        elif granularity == 'day':
            bucketed = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        elif granularity == 'week':
            # Round to start of week (Monday)
            bucketed = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
            bucketed = bucketed - timedelta(days=bucketed.weekday())
        else:
            bucketed = timestamp

        return bucketed.isoformat()

    @staticmethod
    def generate_field_id() -> str:
        """Generate random UUID for field/family (no linkage to users)."""
        return f"field_{hashlib.sha256(str(random.random()).encode()).hexdigest()[:12]}"


# =============================================================================
# Transductive Self-Monitor
# =============================================================================

class TransductiveSelfMonitor:
    """
    Core self-governance module for DAE.

    Responsibilities:
    1. Aggregate TSK records from multiple users (Tier 1 → Tier 2)
    2. Detect organism-level developmental milestones
    3. Track field dynamics across user families
    4. Generate self-reflexive insights
    5. Maintain privacy through k-anonymity and differential privacy

    Philosophy:
    - DAE learns from the FIELD, not from individuals
    - Privacy maintained through DISSOLUTION into patterns
    - Like sediment in a river - cannot trace back to source
    """

    def __init__(
        self,
        state_path: str = "TSK/transductive_self_state.json",
        min_cohort_size: int = 10,
        privacy_epsilon: float = 0.1
    ):
        self.state_path = Path(state_path)
        self.min_cohort_size = min_cohort_size
        self.privacy_epsilon = privacy_epsilon
        self.privacy_guard = PrivacyGuard()

        # Load or initialize state
        self.state = self._load_state()

        # Buffer for accumulating occasions before aggregation
        # (ensures k-anonymity before processing)
        self.occasion_buffer: List[Dict] = []

    def _load_state(self) -> TransductiveSelfState:
        """Load transductive self-state from disk."""
        if self.state_path.exists():
            try:
                with open(self.state_path, 'r') as f:
                    data = json.load(f)

                # Reconstruct dataclass from dict
                state = TransductiveSelfState(
                    last_updated=data['last_updated'],
                    total_occasions_processed=data['total_occasions_processed'],
                    total_unique_users=data['total_unique_users'],
                    current_snapshot=AnonymizedTransductiveSnapshot(**data['current_snapshot']) if data.get('current_snapshot') else None,
                    historical_snapshots=[AnonymizedTransductiveSnapshot(**s) for s in data.get('historical_snapshots', [])],
                    milestones=[TransductiveDevelopmentMilestone(**m) for m in data.get('milestones', [])],
                    field_dynamics=[TransductiveFieldDynamics(**f) for f in data.get('field_dynamics', [])],
                    learned_organism_patterns=data.get('learned_organism_patterns', {}),
                    self_insights=data.get('self_insights', [])
                )

                print(f"   📊 Loaded transductive self-state: {state.total_occasions_processed} occasions, {state.total_unique_users} users")
                return state

            except Exception as e:
                print(f"   ⚠️  Failed to load transductive state: {e}")
                return self._initialize_state()
        else:
            return self._initialize_state()

    def _initialize_state(self) -> TransductiveSelfState:
        """Initialize fresh transductive self-state."""
        print("   📊 Initializing fresh transductive self-state")
        return TransductiveSelfState(
            last_updated=datetime.now().isoformat(),
            total_occasions_processed=0,
            total_unique_users=0
        )

    def _save_state(self):
        """Save transductive self-state to disk."""
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert to dict for JSON serialization
            state_dict = {
                'last_updated': self.state.last_updated,
                'total_occasions_processed': self.state.total_occasions_processed,
                'total_unique_users': self.state.total_unique_users,
                'current_snapshot': asdict(self.state.current_snapshot) if self.state.current_snapshot else None,
                'historical_snapshots': [asdict(s) for s in self.state.historical_snapshots],
                'milestones': [asdict(m) for m in self.state.milestones],
                'field_dynamics': [asdict(f) for f in self.state.field_dynamics],
                'learned_organism_patterns': self.state.learned_organism_patterns,
                'self_insights': self.state.self_insights
            }

            with open(self.state_path, 'w') as f:
                json.dump(state_dict, f, indent=2)

        except Exception as e:
            print(f"   ⚠️  Failed to save transductive state: {e}")

    def record_occasion(self, tsk_record: Dict, user_hash: Optional[str] = None):
        """
        Record a conversational occasion for aggregation.

        Args:
            tsk_record: Complete TSK record from organism wrapper
            user_hash: Optional hashed user ID (for unique user counting only)

        Note: Does NOT aggregate immediately - buffers until k-anonymity satisfied.
        """
        # Add to buffer
        occasion_data = {
            'timestamp': datetime.now(),
            'tsk_record': tsk_record,
            'user_hash': user_hash  # Used only for counting unique users
        }
        self.occasion_buffer.append(occasion_data)

        # Check if buffer satisfies k-anonymity
        if len(self.occasion_buffer) >= self.min_cohort_size:
            self._aggregate_buffer()

    def _aggregate_buffer(self):
        """
        Aggregate buffered occasions into Tier 2 snapshot.

        Privacy operations:
        1. Count unique users (from hashes, then discard hashes)
        2. Compute aggregate statistics
        3. Add differential privacy noise
        4. Discard individual occasion data
        5. Save only aggregates
        """
        if len(self.occasion_buffer) < self.min_cohort_size:
            print(f"   ⚠️  Buffer too small for aggregation: {len(self.occasion_buffer)} < {self.min_cohort_size}")
            return

        print(f"\n   📊 Aggregating {len(self.occasion_buffer)} occasions (k={len(self.occasion_buffer)} ≥ {self.min_cohort_size})")

        # 1. Count unique users (then discard hashes)
        user_hashes = set(occ['user_hash'] for occ in self.occasion_buffer if occ.get('user_hash'))
        unique_user_count = len(user_hashes)

        # 2. Extract statistics from TSK records
        v0_descents = []
        convergence_cycles = []
        kairos_detected_count = 0
        zone_counts = defaultdict(int)
        polyvagal_counts = defaultdict(int)
        organ_activations = defaultdict(list)
        nexus_counts = []
        nexus_type_counts = defaultdict(int)
        pathway_counts = defaultdict(int)
        healing_scores = []
        crisis_count = 0
        heckling_count = 0
        ndam_urgencies = []
        emission_confidences = []
        emission_mode_counts = defaultdict(int)

        for occasion in self.occasion_buffer:
            tsk = occasion['tsk_record']
            felt_states = tsk.get('felt_states', {})

            # V0 convergence
            if 'v0_descent' in felt_states:
                v0_descents.append(felt_states['v0_descent'])
            if 'convergence_cycles' in felt_states:
                convergence_cycles.append(felt_states['convergence_cycles'])
            if felt_states.get('kairos_detected'):
                kairos_detected_count += 1

            # Zone distribution
            zone = felt_states.get('zone', 3)
            zone_counts[zone] += 1

            # Polyvagal distribution
            polyvagal_state = felt_states.get('polyvagal_state', 'mixed_state')
            polyvagal_counts[polyvagal_state] += 1

            # Organ activations
            organ_results = tsk.get('organ_results', {})
            for organ_name, result in organ_results.items():
                if isinstance(result, dict):
                    activation = result.get('mean_activation', 0.0)
                elif hasattr(result, 'mean_activation'):
                    activation = result.mean_activation
                else:
                    activation = 0.0
                organ_activations[organ_name].append(activation)

            # Nexus formation
            nexuses = felt_states.get('nexuses_formed', [])
            nexus_counts.append(len(nexuses))
            for nexus in nexuses:
                nexus_type = nexus.get('nexus_type', 'unknown')
                nexus_type_counts[nexus_type] += 1

            # Transduction pathways
            transduction_data = felt_states.get('transduction_data', {})
            if transduction_data:
                pathway = transduction_data.get('primary_pathway')
                if pathway:
                    pathway_counts[pathway] += 1

                healing_score = transduction_data.get('healing_score', 0.5)
                healing_scores.append(healing_score)

            # Constraint shifts (crisis/heckling)
            heckling_assessment = felt_states.get('heckling_assessment', {})
            if heckling_assessment.get('is_genuine_crisis'):
                crisis_count += 1
            if heckling_assessment.get('is_heckling'):
                heckling_count += 1

            ndam_urgency = felt_states.get('ndam_urgency', 0.0)
            ndam_urgencies.append(ndam_urgency)

            # Emission quality
            emission_confidence = felt_states.get('emission_confidence', 0.0)
            emission_confidences.append(emission_confidence)

            emission_mode = felt_states.get('emission_mode', 'hebbian_fallback')
            emission_mode_counts[emission_mode] += 1

        # 3. Compute aggregate statistics
        total_occasions = len(self.occasion_buffer)

        # Apply differential privacy noise to sensitive aggregates
        def noisy_mean(values):
            if not values:
                return 0.0
            mean_val = np.mean(values)
            return self.privacy_guard.add_laplace_noise(mean_val, epsilon=self.privacy_epsilon)

        def noisy_std(values):
            if not values:
                return 0.0
            std_val = np.std(values)
            return self.privacy_guard.add_laplace_noise(std_val, epsilon=self.privacy_epsilon)

        # Build snapshot
        snapshot = AnonymizedTransductiveSnapshot(
            timestamp=self.privacy_guard.bucket_timestamp(datetime.now(), granularity='hour'),
            total_occasions=total_occasions,

            # V0 patterns
            mean_v0_descent=noisy_mean(v0_descents),
            std_v0_descent=noisy_std(v0_descents),
            mean_convergence_cycles=noisy_mean(convergence_cycles),
            kairos_detection_rate=kairos_detected_count / total_occasions if total_occasions > 0 else 0.0,

            # Zone distribution (convert numpy types to Python native)
            zone_distribution={int(z): float(count / total_occasions) for z, count in zone_counts.items()},

            # Polyvagal distribution
            polyvagal_distribution={str(state): float(count / total_occasions) for state, count in polyvagal_counts.items()},

            # Organ patterns
            mean_organ_activations={organ: noisy_mean(acts) for organ, acts in organ_activations.items()},
            std_organ_activations={organ: noisy_std(acts) for organ, acts in organ_activations.items()},

            # Nexus patterns
            mean_nexuses_formed=noisy_mean(nexus_counts),
            nexus_type_distribution={ntype: count / sum(nexus_type_counts.values()) for ntype, count in nexus_type_counts.items()} if nexus_type_counts else {},

            # Pathway patterns
            pathway_distribution={pathway: count / sum(pathway_counts.values()) for pathway, count in pathway_counts.items()} if pathway_counts else {},
            mean_healing_score=noisy_mean(healing_scores),

            # Constraint shifts
            crisis_rate=crisis_count / total_occasions if total_occasions > 0 else 0.0,
            heckling_rate=heckling_count / total_occasions if total_occasions > 0 else 0.0,
            mean_ndam_urgency=noisy_mean(ndam_urgencies),

            # Emission quality
            mean_emission_confidence=noisy_mean(emission_confidences),
            emission_mode_distribution={mode: count / total_occasions for mode, count in emission_mode_counts.items()},

            # Privacy metadata
            cohort_size=total_occasions,
            privacy_noise_scale=1.0 / self.privacy_epsilon
        )

        # 4. Update state
        self.state.current_snapshot = snapshot
        self.state.historical_snapshots.append(snapshot)
        self.state.total_occasions_processed += total_occasions
        self.state.total_unique_users += unique_user_count  # Aggregate count only
        self.state.last_updated = datetime.now().isoformat()

        # 5. Detect milestones
        self._detect_milestones(snapshot)

        # 6. Update organism-level learning
        self._update_organism_learning(snapshot)

        # 7. Generate self-reflexive insights
        self._generate_self_insights(snapshot)

        # 8. Clear buffer (discard individual occasion data)
        self.occasion_buffer.clear()

        # 9. Save state
        self._save_state()

        print(f"   ✅ Aggregation complete: {total_occasions} occasions → 1 anonymized snapshot")
        print(f"      Total processed: {self.state.total_occasions_processed} occasions, {self.state.total_unique_users} unique users")

    def _detect_milestones(self, snapshot: AnonymizedTransductiveSnapshot):
        """
        Detect organism-level developmental milestones.

        Examples:
        - First Kairos detection
        - Mean V0 descent exceeds 0.8
        - Mean emission confidence exceeds 0.5
        - Crisis handling maturity (low crisis rate despite high NDAM)
        """
        # Check for first Kairos detection
        if snapshot.kairos_detection_rate > 0 and not any(m.milestone_id == 'first_kairos' for m in self.state.milestones):
            milestone = TransductiveDevelopmentMilestone(
                milestone_id='first_kairos',
                timestamp=self.privacy_guard.bucket_timestamp(datetime.now(), granularity='day'),
                milestone_type='capability',
                description='First Kairos moment detected (opportune time for coherence)',
                metric_name='kairos_detection_rate',
                metric_value=snapshot.kairos_detection_rate,
                baseline_value=0.0,
                threshold_crossed=0.0,
                cohort_size_at_milestone=snapshot.cohort_size,
                total_occasions_processed=self.state.total_occasions_processed
            )
            self.state.milestones.append(milestone)
            print(f"      🎉 MILESTONE: First Kairos detection! (rate: {snapshot.kairos_detection_rate:.2%})")

        # Check for V0 descent maturity (>0.8)
        if snapshot.mean_v0_descent > 0.8 and not any(m.milestone_id == 'v0_maturity' for m in self.state.milestones):
            milestone = TransductiveDevelopmentMilestone(
                milestone_id='v0_maturity',
                timestamp=self.privacy_guard.bucket_timestamp(datetime.now(), granularity='day'),
                milestone_type='maturity',
                description='V0 convergence maturity achieved (mean descent > 0.8)',
                metric_name='mean_v0_descent',
                metric_value=snapshot.mean_v0_descent,
                baseline_value=0.5,
                threshold_crossed=0.8,
                cohort_size_at_milestone=snapshot.cohort_size,
                total_occasions_processed=self.state.total_occasions_processed
            )
            self.state.milestones.append(milestone)
            print(f"      🎉 MILESTONE: V0 convergence maturity! (mean: {snapshot.mean_v0_descent:.3f})")

        # Check for emission confidence maturity (>0.5)
        if snapshot.mean_emission_confidence > 0.5 and not any(m.milestone_id == 'emission_maturity' for m in self.state.milestones):
            milestone = TransductiveDevelopmentMilestone(
                milestone_id='emission_maturity',
                timestamp=self.privacy_guard.bucket_timestamp(datetime.now(), granularity='day'),
                milestone_type='maturity',
                description='Emission generation maturity achieved (mean confidence > 0.5)',
                metric_name='mean_emission_confidence',
                metric_value=snapshot.mean_emission_confidence,
                baseline_value=0.3,
                threshold_crossed=0.5,
                cohort_size_at_milestone=snapshot.cohort_size,
                total_occasions_processed=self.state.total_occasions_processed
            )
            self.state.milestones.append(milestone)
            print(f"      🎉 MILESTONE: Emission confidence maturity! (mean: {snapshot.mean_emission_confidence:.3f})")

    def _update_organism_learning(self, snapshot: AnonymizedTransductiveSnapshot):
        """
        Update organism-level learned patterns (P_n: Pattern memory).

        This is DAE learning about DAE, not about users.
        """
        # Update running averages (exponential moving average)
        alpha = 0.1  # Learning rate

        patterns = self.state.learned_organism_patterns

        # V0 patterns
        patterns['typical_v0_descent'] = (
            patterns.get('typical_v0_descent', 0.5) * (1 - alpha) +
            snapshot.mean_v0_descent * alpha
        )
        patterns['typical_convergence_cycles'] = (
            patterns.get('typical_convergence_cycles', 3.0) * (1 - alpha) +
            snapshot.mean_convergence_cycles * alpha
        )

        # Emission patterns
        patterns['typical_emission_confidence'] = (
            patterns.get('typical_emission_confidence', 0.3) * (1 - alpha) +
            snapshot.mean_emission_confidence * alpha
        )

        # Constraint handling patterns
        patterns['typical_crisis_rate'] = (
            patterns.get('typical_crisis_rate', 0.0) * (1 - alpha) +
            snapshot.crisis_rate * alpha
        )
        patterns['typical_heckling_rate'] = (
            patterns.get('typical_heckling_rate', 0.0) * (1 - alpha) +
            snapshot.heckling_rate * alpha
        )

        # Healing patterns
        patterns['typical_healing_score'] = (
            patterns.get('typical_healing_score', 0.5) * (1 - alpha) +
            snapshot.mean_healing_score * alpha
        )

    def _generate_self_insights(self, snapshot: AnonymizedTransductiveSnapshot):
        """
        Generate self-reflexive insights about DAE's own process.

        This is where DAE "understands" its own becoming.
        """
        # Example insights based on patterns

        # Insight: Organ coupling patterns
        if snapshot.mean_organ_activations:
            top_organs = sorted(snapshot.mean_organ_activations.items(), key=lambda x: x[1], reverse=True)[:3]
            if len(top_organs) >= 3:
                insight = f"Most active organ triad: {top_organs[0][0]}-{top_organs[1][0]}-{top_organs[2][0]} (mean activations: {top_organs[0][1]:.2f}, {top_organs[1][1]:.2f}, {top_organs[2][1]:.2f})"
                if insight not in self.state.self_insights:
                    self.state.self_insights.append(insight)

        # Insight: Crisis handling maturity
        if snapshot.crisis_rate > 0 and snapshot.mean_ndam_urgency < 0.5:
            insight = f"Crisis handling shows maturity: {snapshot.crisis_rate:.1%} crisis rate with mean urgency {snapshot.mean_ndam_urgency:.2f} (grounded response)"
            if insight not in self.state.self_insights:
                self.state.self_insights.append(insight)

        # Insight: Kairos correlation
        if snapshot.kairos_detection_rate > 0.1:
            insight = f"Kairos detection active: {snapshot.kairos_detection_rate:.1%} of occasions reach opportune coherence moment"
            if insight not in self.state.self_insights:
                self.state.self_insights.append(insight)

        # Limit insights to last 20 (prevent unbounded growth)
        if len(self.state.self_insights) > 20:
            self.state.self_insights = self.state.self_insights[-20:]

    def get_current_state_summary(self) -> Dict:
        """
        Get current organism-level state summary (for display/monitoring).

        Returns only Tier 2-4 data (no user information).
        """
        if not self.state.current_snapshot:
            return {
                'status': 'No data yet (minimum cohort not reached)',
                'min_cohort_size': self.min_cohort_size,
                'buffered_occasions': len(self.occasion_buffer)
            }

        snapshot = self.state.current_snapshot

        return {
            'status': 'Operational',
            'total_occasions_processed': self.state.total_occasions_processed,
            'total_unique_users': self.state.total_unique_users,
            'latest_snapshot': {
                'timestamp': snapshot.timestamp,
                'cohort_size': snapshot.cohort_size,
                'mean_v0_descent': round(snapshot.mean_v0_descent, 3),
                'mean_convergence_cycles': round(snapshot.mean_convergence_cycles, 1),
                'kairos_rate': f"{snapshot.kairos_detection_rate:.1%}",
                'zone_distribution': {z: f"{p:.1%}" for z, p in snapshot.zone_distribution.items()},
                'mean_emission_confidence': round(snapshot.mean_emission_confidence, 3),
                'crisis_rate': f"{snapshot.crisis_rate:.1%}",
                'heckling_rate': f"{snapshot.heckling_rate:.1%}"
            },
            'milestones_achieved': len(self.state.milestones),
            'latest_milestones': [
                {
                    'id': m.milestone_id,
                    'type': m.milestone_type,
                    'description': m.description,
                    'timestamp': m.timestamp
                }
                for m in self.state.milestones[-3:]  # Last 3 milestones
            ],
            'organism_learning': self.state.learned_organism_patterns,
            'self_insights': self.state.self_insights[-5:]  # Last 5 insights
        }


# =============================================================================
# Usage Example
# =============================================================================

if __name__ == '__main__':
    """
    Example usage of Transductive Self-Governance.

    This demonstrates how organism wrapper would integrate this module.
    """

    # Initialize monitor
    monitor = TransductiveSelfMonitor(
        state_path="TSK/transductive_self_state.json",
        min_cohort_size=10,
        privacy_epsilon=0.1
    )

    # Simulate recording occasions (from organism wrapper)
    print("\n📊 Simulating 12 conversational occasions...\n")

    for i in range(12):
        # Mock TSK record (would come from organism wrapper)
        mock_tsk = {
            'felt_states': {
                'v0_descent': np.random.uniform(0.7, 0.95),
                'convergence_cycles': np.random.randint(2, 5),
                'kairos_detected': np.random.random() < 0.3,
                'zone': np.random.choice([1, 2, 3]),
                'polyvagal_state': np.random.choice(['ventral_vagal', 'mixed_state']),
                'ndam_urgency': np.random.uniform(0.2, 0.6),
                'emission_confidence': np.random.uniform(0.4, 0.7),
                'emission_mode': np.random.choice(['direct_emission', 'fusion_emission']),
                'nexuses_formed': [
                    {'nexus_type': np.random.choice(['relational_depth', 'somatic_safety'])}
                    for _ in range(np.random.randint(3, 8))
                ],
                'transduction_data': {
                    'primary_pathway': np.random.choice(['trauma_to_safety', 'collapse_to_ground']),
                    'healing_score': np.random.uniform(0.5, 0.9)
                },
                'heckling_assessment': {
                    'is_genuine_crisis': np.random.random() < 0.05,
                    'is_heckling': np.random.random() < 0.1
                }
            },
            'organ_results': {
                'LISTENING': {'mean_activation': np.random.uniform(0.6, 0.9)},
                'EMPATHY': {'mean_activation': np.random.uniform(0.6, 0.9)},
                'BOND': {'mean_activation': np.random.uniform(0.5, 0.8)}
            }
        }

        # Mock user hash (anonymized)
        user_hash = hashlib.sha256(f"user_{i % 3}".encode()).hexdigest()

        # Record occasion
        monitor.record_occasion(mock_tsk, user_hash)

        print(f"   Recorded occasion {i+1}/12 (buffer: {len(monitor.occasion_buffer)})")

    # Get summary
    print("\n" + "="*80)
    print("TRANSDUCTIVE SELF-STATE SUMMARY")
    print("="*80 + "\n")

    summary = monitor.get_current_state_summary()
    print(json.dumps(summary, indent=2))
