#!/usr/bin/env python3
"""
Organic Family Loader
=====================

Load and analyze organic family formation for intelligence testing.

Enables:
- Load family data from organic_families.json
- Check family assignments for conversations
- Compute family statistics
- Track family evolution

Date: November 13, 2025
Phase: Intelligence Test Refactoring (Phase 1)
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any, Set


class FamilyLoader:
    """Manages loading and analysis of organic families."""

    def __init__(self, families_path: str = None):
        """
        Initialize family loader.

        Args:
            families_path: Path to organic_families.json
                          (default: persona_layer/organic_families.json)
        """
        if families_path is None:
            families_path = '/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/organic_families.json'

        self.families_path = Path(families_path)

        if not self.families_path.exists():
            raise FileNotFoundError(
                f"Organic families file not found: {families_path}"
            )

        self.families = self._load_families()

    # =========================================================================
    # Load Families
    # =========================================================================

    def _load_families(self) -> Dict[str, Any]:
        """Load families from JSON file."""
        with open(self.families_path, 'r') as f:
            data = json.load(f)

        # Handle both flat and nested structures
        if 'families' in data and isinstance(data['families'], dict):
            families = data['families']
        else:
            families = data

        print(f"✅ Loaded {len(families)} families from {self.families_path.name}")
        return families

    def reload(self):
        """Reload families from file (useful after training)."""
        self.families = self._load_families()

    # =========================================================================
    # Family Assignment
    # =========================================================================

    def get_family_for_conversation(
        self,
        conversation_id: str
    ) -> Optional[str]:
        """
        Get family assignment for a conversation.

        Args:
            conversation_id: Conversation ID to check

        Returns:
            Family ID (e.g., 'family_0') or None if not assigned

        Example:
            >>> loader = FamilyLoader()
            >>> family = loader.get_family_for_conversation('conv_12345')
            >>> print(f"Conversation belongs to: {family}")
            Conversation belongs to: family_0
        """
        for family_id, family_data in self.families.items():
            if not isinstance(family_data, dict):
                continue

            # Support both 'members' and 'member_conversations' keys
            members = family_data.get('members', family_data.get('member_conversations', []))
            if conversation_id in members:
                return family_id

        return None

    def check_same_family(
        self,
        conversation_id_1: str,
        conversation_id_2: str
    ) -> bool:
        """
        Check if two conversations belong to the same family.

        Args:
            conversation_id_1: First conversation ID
            conversation_id_2: Second conversation ID

        Returns:
            True if same family, False otherwise

        Example:
            >>> loader = FamilyLoader()
            >>> same = loader.check_same_family('conv_1', 'conv_2')
            >>> print(f"Same family: {same}")
        """
        family_1 = self.get_family_for_conversation(conversation_id_1)
        family_2 = self.get_family_for_conversation(conversation_id_2)

        if family_1 is None or family_2 is None:
            return False

        return family_1 == family_2

    def get_family_members(
        self,
        family_id: str
    ) -> List[str]:
        """
        Get all member conversation IDs for a family.

        Args:
            family_id: Family ID (e.g., 'family_0')

        Returns:
            List of conversation IDs

        Example:
            >>> loader = FamilyLoader()
            >>> members = loader.get_family_members('family_0')
            >>> print(f"Family has {len(members)} members")
        """
        family_data = self.families.get(family_id, {})
        # Support both 'members' and 'member_conversations' keys
        return family_data.get('members', family_data.get('member_conversations', []))

    # =========================================================================
    # Family Statistics
    # =========================================================================

    def get_family_statistics(self) -> Dict[str, Any]:
        """
        Compute statistics about family formation.

        Returns:
            Dictionary with:
                - 'total_families': int
                - 'mature_families': int (has centroid)
                - 'total_members': int
                - 'family_sizes': List[int]
                - 'mean_family_size': float
                - 'largest_family': str
                - 'largest_family_size': int

        Example:
            >>> loader = FamilyLoader()
            >>> stats = loader.get_family_statistics()
            >>> print(f"Mature families: {stats['mature_families']}")
            >>> print(f"Mean size: {stats['mean_family_size']:.1f}")
        """
        total_families = len(self.families)
        mature_families = 0
        family_sizes = []
        total_members = 0
        largest_family = None
        largest_size = 0

        for family_id, family_data in self.families.items():
            if not isinstance(family_data, dict):
                continue

            # Check if mature (has centroid)
            if 'centroid' in family_data:
                mature_families += 1

            # Get member count (support both keys)
            members = family_data.get('members', family_data.get('member_conversations', []))
            size = len(members)
            family_sizes.append(size)
            total_members += size

            # Track largest
            if size > largest_size:
                largest_size = size
                largest_family = family_id

        mean_size = np.mean(family_sizes) if family_sizes else 0.0

        stats = {
            'total_families': total_families,
            'mature_families': mature_families,
            'total_members': total_members,
            'family_sizes': family_sizes,
            'mean_family_size': float(mean_size),
            'largest_family': largest_family,
            'largest_family_size': largest_size
        }

        return stats

    def print_family_statistics(self):
        """Print formatted family statistics."""
        stats = self.get_family_statistics()

        print("=" * 80)
        print("👨‍👩‍👧‍👦 ORGANIC FAMILY STATISTICS")
        print("=" * 80)
        print(f"Total families: {stats['total_families']}")
        print(f"Mature families: {stats['mature_families']} (have centroids)")
        print(f"Total members: {stats['total_members']}")
        print(f"Mean family size: {stats['mean_family_size']:.1f}")
        print(f"Largest family: {stats['largest_family']} ({stats['largest_family_size']} members)")

        if stats['family_sizes']:
            print(f"\nFamily size distribution:")
            for i, size in enumerate(stats['family_sizes']):
                family_id = f"family_{i}"
                is_mature = "✅" if f"family_{i}" in self.families and 'centroid' in self.families[f"family_{i}"] else "⚪"
                print(f"  {is_mature} {family_id}: {size} members")

        print("=" * 80)

    # =========================================================================
    # Family Centroid Access
    # =========================================================================

    def get_family_centroid(
        self,
        family_id: str
    ) -> Optional[np.ndarray]:
        """
        Get centroid (57D organ signature) for a family.

        Args:
            family_id: Family ID

        Returns:
            57D numpy array or None if family not mature

        Example:
            >>> loader = FamilyLoader()
            >>> centroid = loader.get_family_centroid('family_0')
            >>> if centroid is not None:
            ...     print(f"Centroid shape: {centroid.shape}")
            Centroid shape: (57,)
        """
        family_data = self.families.get(family_id, {})

        if 'centroid' not in family_data:
            return None

        centroid = family_data['centroid']
        return np.array(centroid)

    def compute_distance_to_family(
        self,
        organ_signature: List[float],
        family_id: str
    ) -> Optional[float]:
        """
        Compute Euclidean distance between organ signature and family centroid.

        Args:
            organ_signature: 57D organ signature
            family_id: Family ID

        Returns:
            Distance or None if family not mature

        Example:
            >>> loader = FamilyLoader()
            >>> signature = [0.1] * 57  # Example signature
            >>> distance = loader.compute_distance_to_family(signature, 'family_0')
            >>> print(f"Distance to family: {distance:.3f}")
        """
        centroid = self.get_family_centroid(family_id)

        if centroid is None:
            return None

        signature_array = np.array(organ_signature)
        distance = np.linalg.norm(signature_array - centroid)

        return float(distance)

    # =========================================================================
    # Family Evolution Tracking
    # =========================================================================

    def track_family_evolution(
        self,
        family_id: str,
        historical_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Track how a family has evolved over time.

        Args:
            family_id: Family ID to track
            historical_data: List of historical snapshots, each containing:
                - 'epoch': int
                - 'families': Dict (full families state)

        Returns:
            Dictionary with:
                - 'family_id': str
                - 'birth_epoch': int (when family first appeared)
                - 'size_evolution': List[int] (size at each epoch)
                - 'centroid_evolution': List[np.ndarray] (centroid at each epoch)

        Example:
            >>> loader = FamilyLoader()
            >>> history = [
            ...     {'epoch': 1, 'families': {...}},
            ...     {'epoch': 5, 'families': {...}},
            ... ]
            >>> evolution = loader.track_family_evolution('family_0', history)
            >>> print(f"Born at epoch: {evolution['birth_epoch']}")
        """
        birth_epoch = None
        size_evolution = []
        centroid_evolution = []

        for snapshot in historical_data:
            epoch = snapshot['epoch']
            families = snapshot['families']

            if family_id in families:
                family_data = families[family_id]

                # Record birth
                if birth_epoch is None:
                    birth_epoch = epoch

                # Record size (support both keys)
                members = family_data.get('members', family_data.get('member_conversations', []))
                size_evolution.append(len(members))

                # Record centroid (if available)
                if 'centroid' in family_data:
                    centroid = np.array(family_data['centroid'])
                    centroid_evolution.append(centroid)

        evolution = {
            'family_id': family_id,
            'birth_epoch': birth_epoch,
            'size_evolution': size_evolution,
            'centroid_evolution': centroid_evolution
        }

        return evolution


# =============================================================================
# Self-Test
# =============================================================================

def self_test():
    """Self-test for family loader."""
    print("=" * 80)
    print("👨‍👩‍👧‍👦 TESTING FAMILY LOADER")
    print("=" * 80)

    # Check if organic_families.json exists
    families_path = Path('/Users/daedalea/Desktop/DAE_HYPHAE_1/persona_layer/organic_families.json')

    if not families_path.exists():
        print("⚠️  organic_families.json not found - creating test file")

        # Create minimal test file
        test_families = {
            'family_0': {
                'centroid': [0.1] * 57,
                'members': ['conv_1', 'conv_2', 'conv_3']
            },
            'family_1': {
                'centroid': [0.2] * 57,
                'members': ['conv_4', 'conv_5']
            }
        }

        with open(families_path, 'w') as f:
            json.dump(test_families, f, indent=2)

        print("✅ Test file created")

    # Initialize loader
    loader = FamilyLoader()

    # Test 1: Get family for conversation
    print("\n" + "-" * 80)
    print("Test 1: Get Family Assignment")
    print("-" * 80)

    families = loader.families
    if families:
        # Get first family and first member
        first_family_id = list(families.keys())[0]
        first_family = families[first_family_id]
        if isinstance(first_family, dict):
            # Support both 'members' and 'member_conversations'
            members = first_family.get('members', first_family.get('member_conversations', []))
            if members:
                first_member = members[0]
                assigned_family = loader.get_family_for_conversation(first_member)
                print(f"Conversation: {first_member}")
                print(f"Assigned family: {assigned_family}")
                assert assigned_family == first_family_id, "Family assignment should match"
                print("✅ Family assignment working correctly")
            else:
                print("⚠️  No members found in family")
        else:
            print("⚠️  No valid family structure found")
    else:
        print("⚠️  No families loaded")

    # Test 2: Check same family
    print("\n" + "-" * 80)
    print("Test 2: Check Same Family")
    print("-" * 80)

    if families and len(families) >= 2:
        family_ids = list(families.keys())
        # Support both keys
        family_0 = families[family_ids[0]]
        family_1 = families[family_ids[1]]
        family_0_members = family_0.get('members', family_0.get('member_conversations', []))
        family_1_members = family_1.get('members', family_1.get('member_conversations', []))

        if len(family_0_members) >= 2 and len(family_1_members) >= 1:
            same = loader.check_same_family(family_0_members[0], family_0_members[1])
            different = loader.check_same_family(family_0_members[0], family_1_members[0])

            print(f"Same family check: {same}")
            print(f"Different family check: {different}")

            assert same == True, "Members of same family should return True"
            assert different == False, "Members of different families should return False"
            print("✅ Same family check working correctly")

    # Test 3: Get family members
    print("\n" + "-" * 80)
    print("Test 3: Get Family Members")
    print("-" * 80)

    if families:
        first_family_id = list(families.keys())[0]
        members = loader.get_family_members(first_family_id)
        print(f"Family: {first_family_id}")
        print(f"Members: {members}")
        print(f"Count: {len(members)}")
        assert len(members) > 0, "Should have at least one member"
        print("✅ Get family members working correctly")

    # Test 4: Family statistics
    print("\n" + "-" * 80)
    print("Test 4: Family Statistics")
    print("-" * 80)

    loader.print_family_statistics()
    stats = loader.get_family_statistics()
    assert stats['total_families'] > 0, "Should have at least one family"
    print("✅ Family statistics working correctly")

    # Test 5: Family centroid
    print("\n" + "-" * 80)
    print("Test 5: Family Centroid")
    print("-" * 80)

    if families:
        first_family_id = list(families.keys())[0]
        centroid = loader.get_family_centroid(first_family_id)
        if centroid is not None:
            print(f"Family: {first_family_id}")
            print(f"Centroid shape: {centroid.shape}")
            print(f"Centroid mean: {np.mean(centroid):.3f}")
            assert centroid.shape == (57,), "Centroid should be 57D"
            print("✅ Family centroid working correctly")
        else:
            print("⚠️  Family not mature (no centroid)")

    # Summary
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED - Family Loader Ready")
    print("=" * 80)


if __name__ == '__main__':
    self_test()
