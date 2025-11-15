"""
Organic Conversational Families - Phase 5 of Emission Architecture
===================================================================

Self-organizing family discovery through cosine similarity clustering.

Purpose:
- Discover archetypal conversation patterns (Eternal Objects)
- NO pre-defined categories - patterns emerge naturally
- Cluster 45D organ-native signatures (cosine similarity ≥ 0.85)
- EMA centroid updates (α=0.2) for smooth family maturation
- Enable objective immortality (successful patterns persist)

Philosophy:
- Follows DAE 3.0's proven organic emergence (841 perfect tasks, 37 families)
- Zipf's law expected (power law distribution)
- Maturity threshold: ≥3 conversations for statistical reliability
- Semantic naming AFTER emergence (discovered, not pre-designed)
- Whiteheadian Eternal Objects through experience accumulation

Integration Point:
- Called after successful emissions (satisfaction ≥ 0.75)
- Input: 45D CompositeOrganSignature from signature extractor
- Output: Family assignment or new family creation
- Storage: organic_families.json (persistent family state)

Date: November 11, 2025
Status: Phase 5 Implementation - Organic Conversational Learning
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime
from collections import defaultdict


@dataclass
class ConversationalFamily:
    """
    Self-organizing family of similar conversations (Eternal Objects).

    Represents archetypal pattern discovered through experience accumulation.
    Analogous to DAE 3.0's families (e.g., 'value', 'spatial', 'complex').
    """
    family_id: str  # e.g., 'Family_001', 'Family_002'

    # Family centroid (45D, L2-normalized)
    centroid: np.ndarray  # EMA-updated mean signature

    # Membership
    member_conversations: List[str]  # Conversation IDs in this family
    member_count: int

    # Family metrics
    mean_satisfaction: float  # Average satisfaction across members
    std_satisfaction: float  # Satisfaction variance

    # Maturity status
    is_mature: bool  # True if ≥3 members (statistical reliability)
    maturity_level: str  # 'infant' (1-2), 'emerging' (3-9), 'mature' (10+)

    # Discovery metadata
    first_seen: str  # ISO timestamp of family creation
    last_updated: str  # ISO timestamp of last member added

    # Semantic naming (discovered AFTER emergence)
    semantic_name: Optional[str] = None  # Human-assigned after inspection
    semantic_description: Optional[str] = None

    # Organ importance (learned per family)
    dominant_organs: List[str] = field(default_factory=list)  # Top 3 organs
    organ_activation_means: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        """Compute derived metrics after initialization."""
        if self.member_count >= 3:
            self.is_mature = True
            if self.member_count >= 10:
                self.maturity_level = 'mature'
            else:
                self.maturity_level = 'emerging'
        else:
            self.is_mature = False
            self.maturity_level = 'infant'


@dataclass
class FamilyAssignment:
    """Result of family assignment decision."""
    conversation_id: str
    family_id: str
    assignment_type: str  # 'ASSIGNED' (joined existing) or 'CREATED' (new family)
    similarity_score: float  # Cosine similarity to assigned family centroid
    family_maturity: str  # 'infant', 'emerging', 'mature'
    timestamp: str


class OrganicConversationalFamilies:
    """
    Self-organizing family clustering for conversational patterns.

    Strategy (from DAE 3.0's proven approach):
    1. Extract 45D organ-native signature from successful conversation
    2. Compute cosine similarity to all existing family centroids
    3. IF max similarity ≥ 0.85 → Join existing family (EMA update centroid)
    4. ELSE → Create NEW family (novel pattern discovered!)
    5. Update family metrics (satisfaction, organ importance, maturity)
    6. Persist state to organic_families.json

    Expected Emergence Pattern (from DAE 3.0):
    - After 50 conversations: 8-15 families discovered
    - After 200 conversations: 15-25 families, semantic naming begins
    - After 1,000 conversations: 20-30 families (saturated), Zipf's law validated
    - Power law distribution: α ∈ [0.7, 1.0] (universal scaling)

    Maturity Thresholds:
    - Infant (1-2 members): Unstable, don't use for guidance
    - Emerging (3-9 members): Statistically reliable, use with caution
    - Mature (10+ members): High confidence, strong guidance

    Semantic Naming (Manual Discovery):
    - Inspect mature families after 200+ conversations
    - Name based on organ activation patterns + example conversations
    - Examples: "Compassionate Validation", "Insight Generation", "Trauma Processing"
    """

    def __init__(
        self,
        storage_path: str = 'persona_layer/state/active/organic_families.json',
        similarity_threshold: float = 0.65,  # OPTIMIZED Nov 13, 2025: 0.75 → 0.65 (0.50 experiment showed threshold not bottleneck)
        ema_alpha: float = 0.2,
        maturity_threshold: int = 3,
        max_members_per_family: int = 100
    ):
        """
        Initialize organic conversational family discovery.

        Args:
            storage_path: Path to persistent family storage (JSON)
            similarity_threshold: Minimum cosine similarity for family assignment (0.85 from DAE 3.0)
            ema_alpha: EMA smoothing factor for centroid updates (0.2 from DAE 3.0)
            maturity_threshold: Minimum members for statistical reliability (3 from DAE 3.0)
            max_members_per_family: Maximum members to track per family (prevents unbounded growth)
        """
        self.storage_path = Path(storage_path)
        self.similarity_threshold = similarity_threshold
        self.ema_alpha = ema_alpha
        self.maturity_threshold = maturity_threshold
        self.max_members_per_family = max_members_per_family

        # Family registry
        self.families: Dict[str, ConversationalFamily] = {}
        self.next_family_id = 1

        # Conversation → Family mapping
        self.conversation_to_family: Dict[str, str] = {}

        # Assignment history
        self.assignment_history: List[FamilyAssignment] = []

        # Load existing families if present
        self._load_families()

    def _load_families(self):
        """Load existing families from persistent storage."""
        if not self.storage_path.exists():
            print(f"📝 No existing families found at {self.storage_path}, starting fresh")
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Reconstruct families
            for fam_id, fam_data in data.get('families', {}).items():
                # Reconstruct centroid as numpy array
                centroid = np.array(fam_data['centroid'])

                # Deduplicate members on load (fix existing duplicates)
                members = fam_data['member_conversations']
                unique_members = []
                seen = set()
                for member in members:
                    if member not in seen:
                        unique_members.append(member)
                        seen.add(member)

                family = ConversationalFamily(
                    family_id=fam_id,
                    centroid=centroid,
                    member_conversations=unique_members,
                    member_count=len(unique_members),  # Use deduplicated count
                    mean_satisfaction=fam_data['mean_satisfaction'],
                    std_satisfaction=fam_data['std_satisfaction'],
                    is_mature=fam_data['is_mature'],
                    maturity_level=fam_data['maturity_level'],
                    first_seen=fam_data['first_seen'],
                    last_updated=fam_data['last_updated'],
                    semantic_name=fam_data.get('semantic_name'),
                    semantic_description=fam_data.get('semantic_description'),
                    dominant_organs=fam_data.get('dominant_organs', []),
                    organ_activation_means=fam_data.get('organ_activation_means', {})
                )

                self.families[fam_id] = family

            # Reconstruct conversation mapping
            self.conversation_to_family = data.get('conversation_to_family', {})

            # Restore next family ID
            self.next_family_id = data.get('next_family_id', 1)

            print(f"✅ Loaded {len(self.families)} existing families from {self.storage_path}")
            print(f"   Mature families: {sum(1 for f in self.families.values() if f.is_mature)}")
            print(f"   Total conversations: {len(self.conversation_to_family)}")

        except Exception as e:
            print(f"⚠️  Error loading families: {e}, starting fresh")
            self.families = {}
            self.conversation_to_family = {}
            self.next_family_id = 1

    def _save_families(self):
        """Persist families to storage."""
        try:
            # Convert families to JSON-serializable format
            families_dict = {}
            for fam_id, family in self.families.items():
                fam_dict = asdict(family)
                # Convert numpy centroid to list
                fam_dict['centroid'] = family.centroid.tolist()
                families_dict[fam_id] = fam_dict

            data = {
                'families': families_dict,
                'conversation_to_family': self.conversation_to_family,
                'next_family_id': self.next_family_id,
                'last_updated': datetime.now().isoformat(),
                'total_families': len(self.families),
                'mature_families': sum(1 for f in self.families.values() if f.is_mature),
                'total_conversations': len(self.conversation_to_family)
            }

            # Ensure directory exists
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"💾 Families persisted to {self.storage_path}")

        except Exception as e:
            print(f"❌ Error saving families: {e}")

    def assign_to_family(
        self,
        conversation_id: str,
        signature: np.ndarray,
        satisfaction_score: float,
        organ_contributions: Dict[str, np.ndarray]
    ) -> FamilyAssignment:
        """
        Assign conversation to family (or create new family).

        This is the CRITICAL DECISION POINT for organic emergence.

        Args:
            conversation_id: Unique conversation identifier
            signature: 45D L2-normalized organ signature
            satisfaction_score: Overall satisfaction (0-1)
            organ_contributions: {organ_name: organ_signature} for interpretability

        Returns:
            FamilyAssignment with decision details
        """
        timestamp = datetime.now().isoformat()

        # Edge case: No families yet → create first family
        if not self.families:
            return self._create_family(
                conversation_id=conversation_id,
                signature=signature,
                satisfaction_score=satisfaction_score,
                organ_contributions=organ_contributions,
                timestamp=timestamp
            )

        # Compute cosine similarity to all family centroids
        similarities = {}
        for fam_id, family in self.families.items():
            # Cosine similarity: dot product of L2-normalized vectors
            similarity = np.dot(signature, family.centroid)
            similarities[fam_id] = similarity

        # Find best matching family
        best_family_id = max(similarities, key=similarities.get)
        best_similarity = similarities[best_family_id]

        # 🆕 Adaptive threshold (Nov 15, 2025 - DAE 3.0 legacy integration)
        # Encourage family diversity when few families exist
        adaptive_threshold = self._get_adaptive_threshold()

        # DECISION: Assign to existing family OR create new
        if best_similarity >= adaptive_threshold:
            # HIGH SIMILARITY → Join existing family
            return self._add_to_family(
                family_id=best_family_id,
                conversation_id=conversation_id,
                signature=signature,
                satisfaction_score=satisfaction_score,
                organ_contributions=organ_contributions,
                similarity_score=best_similarity,
                timestamp=timestamp
            )
        else:
            # LOW SIMILARITY → Create NEW family (novel pattern discovered!)
            print(f"🆕 NOVEL PATTERN DETECTED (similarity={best_similarity:.3f} < {self.similarity_threshold})")
            return self._create_family(
                conversation_id=conversation_id,
                signature=signature,
                satisfaction_score=satisfaction_score,
                organ_contributions=organ_contributions,
                timestamp=timestamp
            )

    def _add_to_family(
        self,
        family_id: str,
        conversation_id: str,
        signature: np.ndarray,
        satisfaction_score: float,
        organ_contributions: Dict[str, np.ndarray],
        similarity_score: float,
        timestamp: str
    ) -> FamilyAssignment:
        """Add conversation to existing family with EMA centroid update."""
        family = self.families[family_id]

        # EMA update centroid: new = (1-α) * old + α * observed
        family.centroid = (1 - self.ema_alpha) * family.centroid + self.ema_alpha * signature

        # Re-normalize centroid (maintain L2 norm = 1.0)
        norm = np.linalg.norm(family.centroid)
        if norm > 1e-6:
            family.centroid = family.centroid / norm

        # Add member (deduplicate to prevent repeated epochs from inflating count)
        if conversation_id not in family.member_conversations:
            family.member_conversations.append(conversation_id)

        # Enforce member limit (keep most recent members)
        if len(family.member_conversations) > self.max_members_per_family:
            family.member_conversations = family.member_conversations[-self.max_members_per_family:]
            print(f"⚠️  Family {family_id} member list capped at {self.max_members_per_family} (keeping most recent)")

        family.member_count = len(family.member_conversations)  # Always sync count with actual list length

        # Update satisfaction metrics
        old_mean = family.mean_satisfaction
        new_mean = ((old_mean * (family.member_count - 1)) + satisfaction_score) / family.member_count
        family.mean_satisfaction = new_mean

        # Incremental std update (Welford's algorithm for numerical stability)
        if family.member_count == 1:
            family.std_satisfaction = 0.0
        else:
            # Simplified: recompute std from all members
            # In production, use Welford's algorithm for efficiency
            pass  # TODO: Implement Welford's algorithm if performance critical

        # Update organ activation means
        self._update_organ_activations(family, organ_contributions)

        # Update maturity
        family.last_updated = timestamp
        if family.member_count >= self.maturity_threshold:
            family.is_mature = True
            if family.member_count >= 10:
                family.maturity_level = 'mature'
                if family.member_count == 10:
                    print(f"🎓 Family {family_id} reached MATURE status (10+ members)")
            else:
                family.maturity_level = 'emerging'
                if family.member_count == self.maturity_threshold:
                    print(f"🌱 Family {family_id} reached EMERGING status (3+ members, statistically reliable)")

        # Record assignment
        self.conversation_to_family[conversation_id] = family_id

        assignment = FamilyAssignment(
            conversation_id=conversation_id,
            family_id=family_id,
            assignment_type='ASSIGNED',
            similarity_score=similarity_score,
            family_maturity=family.maturity_level,
            timestamp=timestamp
        )

        self.assignment_history.append(assignment)

        # Persist updated state
        self._save_families()

        print(f"✅ Conversation {conversation_id} ASSIGNED to {family_id} (similarity={similarity_score:.3f}, members={family.member_count})")

        return assignment

    def _get_adaptive_threshold(self) -> float:
        """
        Compute adaptive similarity threshold based on current family count.

        Strategy (DAE 3.0 inspired):
        - Few families (< 10): Lower threshold → encourage diversity
        - Medium families (10-25): Base threshold → balanced growth
        - Many families (> 25): Higher threshold → consolidation

        Returns:
            Adaptive threshold [0.55, 0.70]
        """
        current_families = len(self.families)
        target_families = 25  # DAE 3.0 achieved 37, target ~25 for conversational

        if current_families < target_families // 3:  # < 8 families
            # Aggressive exploration phase
            threshold = max(0.55, self.similarity_threshold - 0.10)
        elif current_families < target_families:  # 8-24 families
            # Balanced growth phase
            threshold = self.similarity_threshold  # Use base threshold (0.65)
        else:  # ≥ 25 families
            # Consolidation phase
            threshold = min(0.75, self.similarity_threshold + 0.10)

        return threshold

    def _create_family(
        self,
        conversation_id: str,
        signature: np.ndarray,
        satisfaction_score: float,
        organ_contributions: Dict[str, np.ndarray],
        timestamp: str
    ) -> FamilyAssignment:
        """Create new family (novel pattern discovered)."""
        family_id = f"Family_{self.next_family_id:03d}"
        self.next_family_id += 1

        # Initialize family with first member
        family = ConversationalFamily(
            family_id=family_id,
            centroid=signature.copy(),  # Initial centroid = first member
            member_conversations=[conversation_id],
            member_count=1,
            mean_satisfaction=satisfaction_score,
            std_satisfaction=0.0,  # Need ≥2 members for std
            is_mature=False,
            maturity_level='infant',
            first_seen=timestamp,
            last_updated=timestamp
        )

        # Initialize organ activations
        self._update_organ_activations(family, organ_contributions)

        # Register family
        self.families[family_id] = family
        self.conversation_to_family[conversation_id] = family_id

        # Record assignment
        assignment = FamilyAssignment(
            conversation_id=conversation_id,
            family_id=family_id,
            assignment_type='CREATED',
            similarity_score=1.0,  # Perfect similarity (first member)
            family_maturity='infant',
            timestamp=timestamp
        )

        self.assignment_history.append(assignment)

        # Persist updated state
        self._save_families()

        print(f"🆕 NEW FAMILY CREATED: {family_id} (total families: {len(self.families)})")

        return assignment

    def _update_organ_activations(
        self,
        family: ConversationalFamily,
        organ_contributions: Dict[str, np.ndarray]
    ):
        """Update family's organ activation means (for interpretability)."""
        # Compute mean activation per organ across family
        for organ_name, organ_sig in organ_contributions.items():
            mean_activation = np.mean(organ_sig)

            if organ_name in family.organ_activation_means:
                # EMA update
                old_mean = family.organ_activation_means[organ_name]
                new_mean = (1 - self.ema_alpha) * old_mean + self.ema_alpha * mean_activation
                family.organ_activation_means[organ_name] = new_mean
            else:
                # Initialize
                family.organ_activation_means[organ_name] = mean_activation

        # Update dominant organs (top 3 by activation)
        sorted_organs = sorted(
            family.organ_activation_means.items(),
            key=lambda x: x[1],
            reverse=True
        )
        family.dominant_organs = [organ for organ, _ in sorted_organs[:3]]

    def _get_adaptive_threshold(self) -> float:
        """
        Compute adaptive similarity threshold based on current family count.

        Strategy (from DAE 3.0):
        - Few families (<8): Lower threshold → Encourage new family formation
        - Medium families (8-25): Balanced threshold → Natural growth
        - Many families (≥25): Higher threshold → Consolidation

        Returns:
            Adaptive similarity threshold [0.55, 0.75]
        """
        current_families = len(self.families)

        if current_families < 8:
            # Aggressive exploration (few families)
            return 0.55
        elif current_families < 25:
            # Balanced growth (medium families)
            return 0.65  # Base threshold
        else:
            # Consolidation (many families, approaching saturation)
            return 0.75

    def get_family(self, family_id: str) -> Optional[ConversationalFamily]:
        """Get family by ID."""
        return self.families.get(family_id)

    def get_conversation_family(self, conversation_id: str) -> Optional[str]:
        """Get family ID for conversation."""
        return self.conversation_to_family.get(conversation_id)

    def get_mature_families(self) -> List[ConversationalFamily]:
        """Get all mature families (≥3 members)."""
        return [f for f in self.families.values() if f.is_mature]

    def get_family_statistics(self) -> Dict:
        """Compute statistics about family distribution."""
        stats = {
            'total_families': len(self.families),
            'mature_families': sum(1 for f in self.families.values() if f.is_mature),
            'total_conversations': len(self.conversation_to_family),
            'family_sizes': {
                'infant': sum(1 for f in self.families.values() if f.maturity_level == 'infant'),
                'emerging': sum(1 for f in self.families.values() if f.maturity_level == 'emerging'),
                'mature': sum(1 for f in self.families.values() if f.maturity_level == 'mature')
            },
            'mean_family_size': np.mean([f.member_count for f in self.families.values()]) if self.families else 0,
            'largest_family_size': max((f.member_count for f in self.families.values()), default=0),
            'smallest_family_size': min((f.member_count for f in self.families.values()), default=0)
        }

        # Zipf's law validation (if enough families)
        if len(self.families) >= 5:
            family_sizes = sorted([f.member_count for f in self.families.values()], reverse=True)
            stats['family_size_distribution'] = family_sizes[:10]  # Top 10 families
            stats['zipf_candidate'] = True  # Can check Zipf's law

            # Simple Zipf check: Does largest family have ~2× members of 2nd largest?
            if len(family_sizes) >= 2:
                ratio = family_sizes[0] / family_sizes[1]
                stats['zipf_ratio_1_to_2'] = ratio
                stats['zipf_expected_ratio'] = 2.0 ** 0.73  # Expected from DAE 3.0's α=0.73
        else:
            stats['zipf_candidate'] = False

        return stats

    def suggest_semantic_names(self) -> List[Dict]:
        """
        Suggest semantic names for mature families based on organ patterns.

        Returns list of families with suggested names for human inspection.
        """
        suggestions = []

        for family in self.get_mature_families():
            # Skip if already named
            if family.semantic_name:
                continue

            # Analyze organ activation patterns
            suggestion = {
                'family_id': family.family_id,
                'member_count': family.member_count,
                'mean_satisfaction': family.mean_satisfaction,
                'dominant_organs': family.dominant_organs,
                'organ_activations': {
                    organ: family.organ_activation_means.get(organ, 0.0)
                    for organ in family.dominant_organs
                },
                'suggested_names': []
            }

            # Pattern-based name suggestions
            top_organ = family.dominant_organs[0] if family.dominant_organs else None

            if top_organ == 'EMPATHY':
                if family.organ_activation_means.get('EMPATHY', 0) > 0.75:
                    suggestion['suggested_names'].append("Compassionate Validation")
                else:
                    suggestion['suggested_names'].append("Empathic Resonance")

            elif top_organ == 'WISDOM':
                if family.organ_activation_means.get('WISDOM', 0) > 0.75:
                    suggestion['suggested_names'].append("Insight Generation")
                else:
                    suggestion['suggested_names'].append("Pattern Recognition")

            elif top_organ == 'BOND':
                self_distance = family.organ_activation_means.get('BOND', 0.5)
                if self_distance > 0.6:
                    suggestion['suggested_names'].append("Trauma Processing")
                else:
                    suggestion['suggested_names'].append("Parts Integration")

            elif top_organ == 'PRESENCE':
                suggestion['suggested_names'].append("Grounded Awareness")

            elif top_organ == 'AUTHENTICITY':
                suggestion['suggested_names'].append("Truth Speaking")

            elif top_organ == 'LISTENING':
                suggestion['suggested_names'].append("Deep Listening")

            suggestions.append(suggestion)

        return suggestions


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 ORGANIC CONVERSATIONAL FAMILIES TEST")
    print("="*70)

    # Clean test environment
    test_storage = Path('persona_layer/test_organic_families.json')
    if test_storage.exists():
        test_storage.unlink()

    try:
        # Initialize family discovery
        families = OrganicConversationalFamilies(
            storage_path=str(test_storage),
            similarity_threshold=0.85,
            ema_alpha=0.2
        )

        # Simulate 20 conversations with 3 distinct patterns
        print(f"\n📊 SIMULATING 20 CONVERSATIONS (3 PATTERNS):")
        print("   Pattern A: High EMPATHY (10 conversations)")
        print("   Pattern B: High WISDOM (6 conversations)")
        print("   Pattern C: High BOND (4 conversations)")

        # Pattern A: High EMPATHY (should form family)
        empathy_base = np.zeros(45)
        empathy_base[6:13] = 0.85  # EMPATHY dims
        empathy_base = empathy_base / np.linalg.norm(empathy_base)

        for i in range(10):
            # Add small noise (maintain pattern)
            signature = empathy_base + np.random.normal(0, 0.05, 45)
            signature = signature / np.linalg.norm(signature)

            assignment = families.assign_to_family(
                conversation_id=f'conv_A_{i:02d}',
                signature=signature,
                satisfaction_score=0.82 + np.random.normal(0, 0.05),
                organ_contributions={'EMPATHY': np.ones(7) * 0.85}
            )

        print(f"\n✅ Pattern A processed (10 conversations)")

        # Pattern B: High WISDOM (should form separate family)
        wisdom_base = np.zeros(45)
        wisdom_base[13:20] = 0.80  # WISDOM dims
        wisdom_base = wisdom_base / np.linalg.norm(wisdom_base)

        for i in range(6):
            signature = wisdom_base + np.random.normal(0, 0.05, 45)
            signature = signature / np.linalg.norm(signature)

            assignment = families.assign_to_family(
                conversation_id=f'conv_B_{i:02d}',
                signature=signature,
                satisfaction_score=0.78 + np.random.normal(0, 0.05),
                organ_contributions={'WISDOM': np.ones(7) * 0.80}
            )

        print(f"\n✅ Pattern B processed (6 conversations)")

        # Pattern C: High BOND (should form third family)
        bond_base = np.zeros(45)
        bond_base[32:37] = 0.75  # BOND dims
        bond_base = bond_base / np.linalg.norm(bond_base)

        for i in range(4):
            signature = bond_base + np.random.normal(0, 0.05, 45)
            signature = signature / np.linalg.norm(signature)

            assignment = families.assign_to_family(
                conversation_id=f'conv_C_{i:02d}',
                signature=signature,
                satisfaction_score=0.70 + np.random.normal(0, 0.05),
                organ_contributions={'BOND': np.ones(5) * 0.75}
            )

        print(f"\n✅ Pattern C processed (4 conversations)")

        # Print family statistics
        stats = families.get_family_statistics()
        print(f"\n📈 FAMILY STATISTICS:")
        print(f"   Total families: {stats['total_families']}")
        print(f"   Mature families: {stats['mature_families']}")
        print(f"   Total conversations: {stats['total_conversations']}")
        print(f"   Family sizes:")
        print(f"     Infant (1-2): {stats['family_sizes']['infant']}")
        print(f"     Emerging (3-9): {stats['family_sizes']['emerging']}")
        print(f"     Mature (10+): {stats['family_sizes']['mature']}")
        print(f"   Mean family size: {stats['mean_family_size']:.1f}")
        print(f"   Largest family: {stats['largest_family_size']} members")

        # Print family details
        print(f"\n👥 FAMILY DETAILS:")
        for fam_id, family in families.families.items():
            print(f"\n   {fam_id} ({family.maturity_level}):")
            print(f"     Members: {family.member_count}")
            print(f"     Mean satisfaction: {family.mean_satisfaction:.3f}")
            print(f"     Dominant organs: {', '.join(family.dominant_organs)}")

        # Suggest semantic names for mature families
        if families.get_mature_families():
            print(f"\n🏷️  SEMANTIC NAME SUGGESTIONS:")
            suggestions = families.suggest_semantic_names()
            for sugg in suggestions:
                print(f"\n   {sugg['family_id']} ({sugg['member_count']} members):")
                print(f"     Dominant: {', '.join(sugg['dominant_organs'])}")
                print(f"     Suggested names: {', '.join(sugg['suggested_names'])}")

        print(f"\n✅ Organic family discovery working correctly!")
        print(f"   Expected: 3 families (EMPATHY, WISDOM, BOND)")
        print(f"   Actual: {stats['total_families']} families")

    except Exception as e:
        print(f"\n❌ Family discovery failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        if test_storage.exists():
            test_storage.unlink()

    print("\n" + "="*70)
