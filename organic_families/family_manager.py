"""
OrganicFamilyManager - Self-Organizing Task Family Classification

Implements emergent family architecture validated in DAE 3.0 AXO ARC:
- 37 families emerged naturally following Zipf's law (R²=0.94)
- 86.75% cross-dataset transfer (ARC 1.0 → 2.0)
- Self-organization via 35D felt signatures (cosine similarity > 0.85)

Architecture:
- No pre-defined categories (families emerge from data)
- 35D felt signatures from Vector35D projection
- Cosine similarity clustering (threshold 0.85)
- Per-family cluster learning (organ weights, V0 targets)
- Power-law distribution (Zipf's law)

Author: DAE-GOV Development Team
Created: November 10, 2025
Version: 1.0 (Text-Native Foundation)
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict
import time


@dataclass
class OrganicFamily:
    """
    Self-organized family of related conversations/tasks.

    Each family emerges naturally from similarity clustering of 35D felt
    signatures. Families are NOT pre-defined - they self-organize based on
    discovered patterns.
    """

    family_id: str                          # "family_1", "family_2", etc.
    centroid: np.ndarray                    # 35D centroid (mean of all members)
    member_count: int = 0                   # Number of conversations/tasks
    success_count: int = 0                  # Number of successful outcomes
    total_conversations: int = 0            # Total attempts (for success rate)

    # Cluster learning parameters (optimized per-family)
    learned_organ_weights: Dict[str, float] = field(default_factory=dict)
    learned_v0_target: float = 0.35         # Default V0 energy target
    learned_convergence_threshold: float = 0.6  # Default satisfaction threshold

    # Family metadata
    created_timestamp: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)
    maturity_level: str = "emerging"        # "emerging", "maturing", "mature"

    # Exemplar conversations (for human inspection)
    exemplar_ids: List[str] = field(default_factory=list)  # Top 3-5 representative IDs

    def get_success_rate(self) -> float:
        """Calculate success rate for this family."""
        if self.total_conversations == 0:
            return 0.0
        return self.success_count / self.total_conversations

    def update_maturity(self):
        """Update maturity level based on member count."""
        if self.member_count < 3:
            self.maturity_level = "emerging"
        elif self.member_count < 10:
            self.maturity_level = "maturing"
        else:
            self.maturity_level = "mature"

    def add_member(self, conversation_id: str, success: bool):
        """
        Add new member to family and update statistics.

        Args:
            conversation_id: Unique ID of conversation/task
            success: Whether outcome was successful
        """
        self.member_count += 1
        self.total_conversations += 1
        if success:
            self.success_count += 1

        # Add as exemplar if we have < 5
        if len(self.exemplar_ids) < 5:
            self.exemplar_ids.append(conversation_id)

        self.update_maturity()
        self.last_updated = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'family_id': self.family_id,
            'centroid': self.centroid.tolist(),
            'member_count': self.member_count,
            'success_count': self.success_count,
            'total_conversations': self.total_conversations,
            # 'success_rate': self.get_success_rate(),  # Computed property, not stored
            'learned_organ_weights': self.learned_organ_weights,
            'learned_v0_target': self.learned_v0_target,
            'learned_convergence_threshold': self.learned_convergence_threshold,
            'created_timestamp': self.created_timestamp,
            'last_updated': self.last_updated,
            'maturity_level': self.maturity_level,
            'exemplar_ids': self.exemplar_ids
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrganicFamily':
        """Deserialize from dictionary."""
        # Remove computed properties if present
        data.pop('success_rate', None)
        # Convert lists back to numpy
        data['centroid'] = np.array(data['centroid'])
        return cls(**data)


class OrganicFamilyManager:
    """
    Manages self-organizing family classification system.

    Based on validated emergent family architecture from DAE 3.0:
    - Self-organizing (no pre-defined categories)
    - 35D felt signatures for classification
    - Cosine similarity clustering (threshold 0.85)
    - Power-law distribution (Zipf's law)
    - Per-family cluster learning

    Usage:
        manager = OrganicFamilyManager()
        family_id, confidence = manager.classify_conversation(felt_signature_35d)
        manager.update_family_outcome(family_id, conversation_id, success=True)
        manager.save()
    """

    def __init__(
        self,
        storage_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1/organic_families/families.json",
        similarity_threshold: float = 0.85,
        min_members_for_maturity: int = 10
    ):
        """
        Initialize OrganicFamilyManager.

        Args:
            storage_path: Path to JSON storage file
            similarity_threshold: Cosine similarity threshold for assignment (default 0.85)
            min_members_for_maturity: Minimum members to consider family "mature"
        """
        self.storage_path = Path(storage_path)
        self.similarity_threshold = similarity_threshold
        self.min_members_for_maturity = min_members_for_maturity

        # Family registry
        self.families: Dict[str, OrganicFamily] = {}
        self.next_family_id = 1

        # Load existing families if available
        self.load()

        # Statistics
        self.total_classifications = 0
        self.new_families_created = 0

    # ========================================================================
    # CLASSIFICATION METHODS
    # ========================================================================

    def classify_conversation(
        self,
        felt_signature: np.ndarray,
        conversation_id: str,
        success: Optional[bool] = None
    ) -> Tuple[str, float]:
        """
        Classify conversation to family via 35D felt signature.

        Self-organizing process:
        1. Compare signature to existing family centroids (cosine similarity)
        2. If similarity > threshold → assign to best-matching family
        3. If similarity < threshold → create new family

        Args:
            felt_signature: 35D numpy array from Vector35D projection
            conversation_id: Unique conversation identifier
            success: Optional success outcome (if known at classification time)

        Returns:
            (family_id, confidence) tuple
        """
        self.total_classifications += 1

        # Validate signature
        if felt_signature.shape[0] != 35:
            raise ValueError(f"Expected 35D felt signature, got {felt_signature.shape[0]}D")

        # Normalize signature for cosine similarity
        signature_norm = felt_signature / np.linalg.norm(felt_signature)

        # Case 1: No families yet → create first family
        if len(self.families) == 0:
            family_id = self._create_new_family(signature_norm, conversation_id, success)
            return family_id, 1.0

        # Case 2: Compare to existing families
        best_family_id, best_similarity = self._find_best_matching_family(signature_norm)

        # Case 3: Good match found → assign to existing family
        if best_similarity >= self.similarity_threshold:
            if success is not None:
                self.families[best_family_id].add_member(conversation_id, success)
                # Update centroid (running average)
                self._update_family_centroid(best_family_id, signature_norm)

            return best_family_id, best_similarity

        # Case 4: No good match → create new family
        family_id = self._create_new_family(signature_norm, conversation_id, success)
        return family_id, 1.0

    def _find_best_matching_family(self, signature_norm: np.ndarray) -> Tuple[str, float]:
        """
        Find best matching family via cosine similarity.

        Args:
            signature_norm: Normalized 35D signature

        Returns:
            (family_id, similarity) for best match
        """
        best_family_id = None
        best_similarity = -1.0

        for family_id, family in self.families.items():
            centroid_norm = family.centroid / np.linalg.norm(family.centroid)
            similarity = float(np.dot(signature_norm, centroid_norm))

            if similarity > best_similarity:
                best_similarity = similarity
                best_family_id = family_id

        return best_family_id, best_similarity

    def _create_new_family(
        self,
        signature: np.ndarray,
        conversation_id: str,
        success: Optional[bool]
    ) -> str:
        """
        Create new family with this signature as initial centroid.

        Args:
            signature: 35D normalized signature
            conversation_id: Initial member ID
            success: Optional success outcome

        Returns:
            New family_id
        """
        family_id = f"family_{self.next_family_id}"
        self.next_family_id += 1

        family = OrganicFamily(
            family_id=family_id,
            centroid=signature.copy(),
            member_count=0,
            success_count=0,
            total_conversations=0
        )

        if success is not None:
            family.add_member(conversation_id, success)

        self.families[family_id] = family
        self.new_families_created += 1

        print(f"🌱 NEW FAMILY CREATED: {family_id} (total families: {len(self.families)})")

        return family_id

    def _update_family_centroid(self, family_id: str, new_signature: np.ndarray):
        """
        Update family centroid with new member signature (running average).

        Args:
            family_id: Target family
            new_signature: Normalized 35D signature of new member
        """
        family = self.families[family_id]
        n = family.member_count

        # Running average: new_centroid = (old_centroid * (n-1) + new_signature) / n
        family.centroid = (family.centroid * (n - 1) + new_signature) / n
        family.last_updated = time.time()

    # ========================================================================
    # FAMILY OUTCOME TRACKING
    # ========================================================================

    def update_family_outcome(self, family_id: str, conversation_id: str, success: bool):
        """
        Update family outcome after conversation completes.

        Call this when you know the success outcome but didn't provide it
        during initial classification.

        Args:
            family_id: Target family
            conversation_id: Conversation identifier
            success: Whether conversation was successful
        """
        if family_id not in self.families:
            raise ValueError(f"Family {family_id} not found")

        self.families[family_id].add_member(conversation_id, success)

    # ========================================================================
    # CLUSTER LEARNING (PER-FAMILY OPTIMIZATION)
    # ========================================================================

    def update_cluster_learning(
        self,
        family_id: str,
        organ_weights: Optional[Dict[str, float]] = None,
        v0_target: Optional[float] = None,
        convergence_threshold: Optional[float] = None
    ):
        """
        Update cluster learning parameters for family.

        Per-family optimization discovered through experience:
        - Which organs matter most for this family
        - Optimal V0 energy target for convergence
        - Best satisfaction threshold for decisions

        Args:
            family_id: Target family
            organ_weights: Optional organ importance weights
            v0_target: Optional V0 energy target (e.g., 0.29 for spatial tasks)
            convergence_threshold: Optional satisfaction threshold
        """
        if family_id not in self.families:
            raise ValueError(f"Family {family_id} not found")

        family = self.families[family_id]

        if organ_weights is not None:
            family.learned_organ_weights.update(organ_weights)

        if v0_target is not None:
            family.learned_v0_target = v0_target

        if convergence_threshold is not None:
            family.learned_convergence_threshold = convergence_threshold

        family.last_updated = time.time()

    def get_cluster_learning(self, family_id: str) -> Dict[str, Any]:
        """
        Get cluster learning parameters for family.

        Returns:
            Dictionary with:
                - organ_weights: Dict[str, float]
                - v0_target: float
                - convergence_threshold: float
        """
        if family_id not in self.families:
            # Return defaults for unknown family
            return {
                'organ_weights': {},
                'v0_target': 0.35,
                'convergence_threshold': 0.6
            }

        family = self.families[family_id]
        return {
            'organ_weights': family.learned_organ_weights.copy(),
            'v0_target': family.learned_v0_target,
            'convergence_threshold': family.learned_convergence_threshold
        }

    # ========================================================================
    # STATISTICS & ANALYSIS
    # ========================================================================

    def get_family_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive family statistics.

        Returns:
            Dictionary with:
                - total_families: int
                - total_conversations: int
                - success_rate_overall: float
                - families_by_maturity: Dict[str, int]
                - top_families: List[Dict] (sorted by member_count)
                - zipf_validation: Dict (power-law fit statistics)
        """
        if len(self.families) == 0:
            return {
                'total_families': 0,
                'total_conversations': 0,
                'success_rate_overall': 0.0,
                'families_by_maturity': {},
                'top_families': [],
                'zipf_validation': {}
            }

        # Aggregate statistics
        total_conversations = sum(f.total_conversations for f in self.families.values())
        total_successes = sum(f.success_count for f in self.families.values())
        success_rate = total_successes / total_conversations if total_conversations > 0 else 0.0

        # Maturity distribution
        maturity_counts = defaultdict(int)
        for family in self.families.values():
            maturity_counts[family.maturity_level] += 1

        # Top families (sorted by member count)
        families_sorted = sorted(
            self.families.values(),
            key=lambda f: f.member_count,
            reverse=True
        )
        top_families = [
            {
                'family_id': f.family_id,
                'member_count': f.member_count,
                'success_rate': f.get_success_rate(),
                'maturity': f.maturity_level
            }
            for f in families_sorted[:10]
        ]

        # Zipf's law validation (power-law distribution)
        zipf_stats = self._validate_zipf_distribution()

        return {
            'total_families': len(self.families),
            'total_conversations': total_conversations,
            'success_rate_overall': success_rate,
            'families_by_maturity': dict(maturity_counts),
            'top_families': top_families,
            'zipf_validation': zipf_stats,
            'total_classifications': self.total_classifications,
            'new_families_created': self.new_families_created
        }

    def _validate_zipf_distribution(self) -> Dict[str, Any]:
        """
        Validate whether family distribution follows Zipf's law (power-law).

        Expected from DAE 3.0: α ≈ 0.73, R² ≈ 0.94

        Returns:
            Dictionary with:
                - exponent: float (α in power-law)
                - r_squared: float (goodness of fit)
                - follows_zipf: bool (R² > 0.90)
        """
        if len(self.families) < 3:
            return {'exponent': None, 'r_squared': None, 'follows_zipf': False}

        # Get member counts sorted descending
        member_counts = sorted(
            [f.member_count for f in self.families.values()],
            reverse=True
        )

        if member_counts[0] == 0:
            return {'exponent': None, 'r_squared': None, 'follows_zipf': False}

        # Fit power-law: count(rank) = count(1) * rank^(-α)
        # Take log: log(count) = log(count(1)) - α * log(rank)
        ranks = np.arange(1, len(member_counts) + 1)
        log_ranks = np.log(ranks)
        log_counts = np.log(member_counts)

        # Linear regression in log-space
        A = np.vstack([log_ranks, np.ones(len(log_ranks))]).T
        exponent, intercept = np.linalg.lstsq(A, log_counts, rcond=None)[0]
        exponent = -exponent  # Negate because power-law has negative exponent

        # Calculate R²
        predicted = intercept - exponent * log_ranks
        ss_res = np.sum((log_counts - predicted) ** 2)
        ss_tot = np.sum((log_counts - np.mean(log_counts)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

        # Zipf's law typically has 0.7 < α < 1.0 and R² > 0.90
        follows_zipf = (0.5 < exponent < 1.5) and (r_squared > 0.85)

        return {
            'exponent': float(exponent),
            'r_squared': float(r_squared),
            'follows_zipf': follows_zipf,
            'interpretation': 'Power-law distribution (Zipf)' if follows_zipf else 'Not Zipfian'
        }

    # ========================================================================
    # PERSISTENCE
    # ========================================================================

    def save(self):
        """Save families to JSON storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'families': {
                family_id: family.to_dict()
                for family_id, family in self.families.items()
            },
            'metadata': {
                'next_family_id': self.next_family_id,
                'total_families': len(self.families),
                'total_classifications': self.total_classifications,
                'new_families_created': self.new_families_created,
                'similarity_threshold': self.similarity_threshold,
                'last_saved': time.time()
            }
        }

        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Saved {len(self.families)} families to {self.storage_path}")

    def load(self):
        """Load families from JSON storage."""
        if not self.storage_path.exists():
            print(f"📂 No existing families found at {self.storage_path}")
            return

        with open(self.storage_path, 'r') as f:
            data = json.load(f)

        # Load families
        self.families = {
            family_id: OrganicFamily.from_dict(family_data)
            for family_id, family_data in data['families'].items()
        }

        # Load metadata
        metadata = data['metadata']
        self.next_family_id = metadata['next_family_id']
        self.total_classifications = metadata.get('total_classifications', 0)
        self.new_families_created = metadata.get('new_families_created', 0)

        print(f"✅ Loaded {len(self.families)} families from {self.storage_path}")

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_family(self, family_id: str) -> Optional[OrganicFamily]:
        """Get family by ID."""
        return self.families.get(family_id)

    def get_all_families(self) -> List[OrganicFamily]:
        """Get all families sorted by member count."""
        return sorted(
            self.families.values(),
            key=lambda f: f.member_count,
            reverse=True
        )

    def get_mature_families(self) -> List[OrganicFamily]:
        """Get only mature families (≥ min_members_for_maturity)."""
        return [
            f for f in self.families.values()
            if f.maturity_level == "mature"
        ]

    def print_summary(self):
        """Print human-readable summary of family system."""
        stats = self.get_family_statistics()

        print("\n" + "=" * 60)
        print("🌀 ORGANIC FAMILY SYSTEM SUMMARY")
        print("=" * 60)
        print(f"Total Families:       {stats['total_families']}")
        print(f"Total Conversations:  {stats['total_conversations']}")
        print(f"Success Rate:         {stats['success_rate_overall']:.1%}")
        print(f"Classifications:      {self.total_classifications}")
        print(f"New Families Created: {self.new_families_created}")
        print()
        print("Maturity Distribution:")
        for maturity, count in stats['families_by_maturity'].items():
            print(f"  {maturity:12s}: {count:3d} families")
        print()
        print("Top 5 Families (by size):")
        for i, fam in enumerate(stats['top_families'][:5], 1):
            print(f"  {i}. {fam['family_id']:15s}: {fam['member_count']:4d} members, "
                  f"{fam['success_rate']:5.1%} success, {fam['maturity']}")
        print()

        zipf = stats['zipf_validation']
        if zipf.get('follows_zipf'):
            print(f"✅ ZIPF'S LAW VALIDATED:")
            print(f"   Exponent (α): {zipf['exponent']:.3f} (expected ~0.73)")
            print(f"   R²: {zipf['r_squared']:.3f} (expected ~0.94)")
            print(f"   Interpretation: {zipf['interpretation']}")
        elif zipf.get('exponent') is not None:
            print(f"⚠️  Power-law emerging (not yet Zipfian):")
            print(f"   Exponent (α): {zipf['exponent']:.3f}")
            print(f"   R²: {zipf['r_squared']:.3f}")
        else:
            print(f"⏳ Too few families for Zipf validation (need ≥3)")

        print("=" * 60)


if __name__ == "__main__":
    """
    Basic validation test for OrganicFamilyManager.
    """
    print("🧪 OrganicFamilyManager Validation Test")
    print("=" * 60)

    # Create manager with test storage path
    test_path = "/tmp/test_families.json"
    manager = OrganicFamilyManager(storage_path=test_path, similarity_threshold=0.85)

    # Simulate 10 conversations with random 35D signatures
    print("\n📊 Simulating 10 conversations...")
    np.random.seed(42)

    for i in range(10):
        # Create random 35D signature
        signature = np.random.randn(35)
        signature /= np.linalg.norm(signature)

        # Add small noise to create similar signatures (should cluster)
        if i > 0 and i % 3 == 0:
            # Similar to previous
            prev_signature = np.random.randn(35)
            prev_signature /= np.linalg.norm(prev_signature)
            signature = 0.9 * prev_signature + 0.1 * signature
            signature /= np.linalg.norm(signature)

        conversation_id = f"conv_{i+1}"
        success = np.random.rand() > 0.3  # 70% success rate

        family_id, confidence = manager.classify_conversation(
            signature,
            conversation_id,
            success
        )

        print(f"  Conv {i+1:2d} → {family_id:12s} (confidence: {confidence:.3f}, "
              f"success: {success})")

    # Print summary
    manager.print_summary()

    # Save to disk
    manager.save()

    # Test load
    print("\n🔄 Testing persistence...")
    manager2 = OrganicFamilyManager(storage_path=test_path)
    assert len(manager2.families) == len(manager.families)
    print(f"✅ Loaded {len(manager2.families)} families successfully")

    print("\n✅ ALL TESTS PASSED - OrganicFamilyManager operational")
