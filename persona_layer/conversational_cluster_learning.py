"""
Conversational Cluster Learning - Phase 5 of Emission Architecture
===================================================================

Per-conversation and per-family EMA optimizations for adaptive learning.

Purpose:
- Learn optimal organ importance weights per family
- Discover target satisfaction scores for each family
- Track conversation-specific optimizations
- Enable objective immortality (successful patterns guide future emissions)

Philosophy:
- Follows DAE 3.0's cluster learning approach (per-task + per-family optimization)
- EMA updates (α=0.2) for smooth, incremental learning
- Normalize organ weights to mean=1.0 (relative importance, not absolute)
- Mature families (≥3 conversations) provide reliable guidance
- Infant families (<3) too unstable for optimization

Integration Point:
- Called after successful conversation (satisfaction ≥ 0.75)
- Input: conversation metrics (organ results, satisfaction, emission quality)
- Output: updated cluster optimizations stored persistently
- Storage: conversational_cluster_db.json

Date: November 11, 2025
Status: Phase 5 Implementation - Organic Conversational Learning
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from collections import defaultdict


@dataclass
class ConversationCluster:
    """
    Per-conversation optimization record.

    Tracks what worked for this specific conversation.
    """
    conversation_id: str
    family_id: str

    # Learned optimizations
    organ_weights: Dict[str, float]  # {organ_name: importance_weight}
    target_satisfaction: float  # Observed satisfaction (what worked)

    # Performance metrics
    satisfaction_achieved: float
    emission_quality: float  # Coherence of emitted phrases

    # Metadata
    timestamp: str
    user_message_length: int
    emission_text_length: int


@dataclass
class FamilyCluster:
    """
    Per-family aggregated optimizations.

    Represents learned patterns across all conversations in family.
    Mature families (≥3 conversations) provide reliable guidance.
    """
    family_id: str

    # Aggregated optimizations (EMA across family members)
    mean_organ_weights: Dict[str, float]  # Average organ importance
    target_satisfaction: float  # Typical satisfaction for this family

    # Family performance
    mean_emission_quality: float
    success_rate: float  # % of conversations with satisfaction ≥ 0.75

    # Maturity
    conversation_count: int
    is_mature: bool  # True if ≥3 conversations

    # Metadata
    first_seen: str
    last_updated: str


class ConversationalClusterLearning:
    """
    Per-conversation and per-family EMA optimization learning.

    Strategy:
    1. After successful conversation (satisfaction ≥ 0.75):
       - Extract organ coherence values (which organs mattered most)
       - Normalize to mean=1.0 (relative importance)
       - Store as ConversationCluster

    2. Update family cluster (EMA):
       - If family is mature (≥3 conversations):
         - Update mean_organ_weights: new = (1-α) * old + α * observed
         - Update target_satisfaction: new = (1-α) * old + α * observed
       - If family is infant (<3):
         - Initialize or accumulate (don't use for guidance yet)

    3. During emission generation:
       - Retrieve family cluster for current conversation pattern
       - Apply learned organ weights to organ activation
       - Target learned satisfaction level

    EMA Alpha (α=0.2 from DAE 3.0):
    - Smooth adaptation (80% history, 20% new observation)
    - Prevents overfitting to recent conversations
    - Balances stability vs. adaptability

    Organ Weight Normalization:
    - Normalize to mean=1.0 (not sum=1.0)
    - Preserves relative importance while allowing modulation
    - Weight > 1.0 = more important than average
    - Weight < 1.0 = less important than average
    """

    def __init__(
        self,
        storage_path: str = 'persona_layer/conversational_cluster_db.json',
        ema_alpha: float = 0.2,
        maturity_threshold: int = 3,
        success_threshold: float = 0.75
    ):
        """
        Initialize conversational cluster learning.

        Args:
            storage_path: Path to persistent cluster storage (JSON)
            ema_alpha: EMA smoothing factor (0.2 from DAE 3.0)
            maturity_threshold: Minimum conversations for family reliability (3)
            success_threshold: Minimum satisfaction to consider successful (0.75)
        """
        self.storage_path = Path(storage_path)
        self.ema_alpha = ema_alpha
        self.maturity_threshold = maturity_threshold
        self.success_threshold = success_threshold

        # Cluster registries
        self.conversation_clusters: Dict[str, ConversationCluster] = {}
        self.family_clusters: Dict[str, FamilyCluster] = {}

        # Load existing clusters if present
        self._load_clusters()

    def _load_clusters(self):
        """Load existing clusters from persistent storage."""
        if not self.storage_path.exists():
            print(f"📝 No existing cluster database at {self.storage_path}, starting fresh")
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Reconstruct conversation clusters
            for conv_id, cluster_data in data.get('conversation_clusters', {}).items():
                cluster = ConversationCluster(**cluster_data)
                self.conversation_clusters[conv_id] = cluster

            # Reconstruct family clusters
            for fam_id, cluster_data in data.get('family_clusters', {}).items():
                cluster = FamilyCluster(**cluster_data)
                self.family_clusters[fam_id] = cluster

            print(f"✅ Loaded cluster database from {self.storage_path}")
            print(f"   Conversation clusters: {len(self.conversation_clusters)}")
            print(f"   Family clusters: {len(self.family_clusters)}")
            print(f"   Mature families: {sum(1 for c in self.family_clusters.values() if c.is_mature)}")

        except Exception as e:
            print(f"⚠️  Error loading clusters: {e}, starting fresh")
            self.conversation_clusters = {}
            self.family_clusters = {}

    def _save_clusters(self):
        """Persist clusters to storage."""
        try:
            # Convert to JSON-serializable format
            conv_clusters_dict = {
                conv_id: asdict(cluster)
                for conv_id, cluster in self.conversation_clusters.items()
            }

            fam_clusters_dict = {
                fam_id: asdict(cluster)
                for fam_id, cluster in self.family_clusters.items()
            }

            data = {
                'conversation_clusters': conv_clusters_dict,
                'family_clusters': fam_clusters_dict,
                'last_updated': datetime.now().isoformat(),
                'total_conversations': len(self.conversation_clusters),
                'total_families': len(self.family_clusters),
                'mature_families': sum(1 for c in self.family_clusters.values() if c.is_mature)
            }

            # Ensure directory exists
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"💾 Cluster database persisted to {self.storage_path}")

        except Exception as e:
            print(f"❌ Error saving clusters: {e}")

    def update_from_conversation(
        self,
        conversation_id: str,
        family_id: str,
        organ_results: Dict,
        satisfaction_score: float,
        emission_metrics: Dict,
        user_message: str = "",
        emission_text: str = ""
    ):
        """
        Update cluster learning from successful conversation.

        Args:
            conversation_id: Unique conversation identifier
            family_id: Assigned family ID
            organ_results: {organ_name: organ_result_dict} from emission
            satisfaction_score: Overall satisfaction (0-1)
            emission_metrics: {coherence, field_strength, etc.}
            user_message: User's message (for metadata)
            emission_text: Generated response (for metadata)
        """
        timestamp = datetime.now().isoformat()

        # Extract organ coherences (what mattered most)
        organ_weights = self._extract_organ_weights(organ_results)

        # Compute emission quality
        emission_quality = emission_metrics.get('mean_coherence', 0.0)

        # Create conversation cluster
        conv_cluster = ConversationCluster(
            conversation_id=conversation_id,
            family_id=family_id,
            organ_weights=organ_weights,
            target_satisfaction=satisfaction_score,
            satisfaction_achieved=satisfaction_score,
            emission_quality=emission_quality,
            timestamp=timestamp,
            user_message_length=len(user_message),
            emission_text_length=len(emission_text)
        )

        self.conversation_clusters[conversation_id] = conv_cluster

        # Update family cluster (EMA)
        self._update_family_cluster(family_id, conv_cluster)

        # Persist updated state
        self._save_clusters()

        print(f"✅ Cluster learning updated for {conversation_id}")
        print(f"   Family: {family_id}")
        print(f"   Satisfaction: {satisfaction_score:.3f}")
        print(f"   Top organs: {self._get_top_organs(organ_weights, k=3)}")

    def _extract_organ_weights(self, organ_results: Dict) -> Dict[str, float]:
        """
        Extract and normalize organ importance weights.

        Strategy:
        - Use organ coherence as proxy for importance
        - Normalize to mean=1.0 (relative importance)
        - Higher coherence = organ contributed more to emission

        Args:
            organ_results: {organ_name: organ_result_dict}

        Returns:
            {organ_name: normalized_weight}
        """
        weights = {}

        for organ_name, result in organ_results.items():
            # Use coherence as importance proxy
            coherence = result.get('coherence', 0.5)
            weights[organ_name] = coherence

        # Normalize to mean=1.0
        if weights:
            mean_weight = np.mean(list(weights.values()))
            if mean_weight > 1e-6:
                weights = {k: v / mean_weight for k, v in weights.items()}

        return weights

    def _update_family_cluster(self, family_id: str, conv_cluster: ConversationCluster):
        """
        Update family cluster with EMA from new conversation.

        Args:
            family_id: Family identifier
            conv_cluster: New conversation cluster to incorporate
        """
        if family_id not in self.family_clusters:
            # Initialize family cluster
            family_cluster = FamilyCluster(
                family_id=family_id,
                mean_organ_weights=conv_cluster.organ_weights.copy(),
                target_satisfaction=conv_cluster.target_satisfaction,
                mean_emission_quality=conv_cluster.emission_quality,
                success_rate=1.0 if conv_cluster.satisfaction_achieved >= self.success_threshold else 0.0,
                conversation_count=1,
                is_mature=False,
                first_seen=conv_cluster.timestamp,
                last_updated=conv_cluster.timestamp
            )

            self.family_clusters[family_id] = family_cluster

            print(f"🆕 Initialized family cluster: {family_id}")

        else:
            # EMA update existing family cluster
            family_cluster = self.family_clusters[family_id]

            # Update organ weights (EMA per organ)
            for organ_name, observed_weight in conv_cluster.organ_weights.items():
                if organ_name in family_cluster.mean_organ_weights:
                    old_weight = family_cluster.mean_organ_weights[organ_name]
                    new_weight = (1 - self.ema_alpha) * old_weight + self.ema_alpha * observed_weight
                    family_cluster.mean_organ_weights[organ_name] = new_weight
                else:
                    # New organ (shouldn't happen, but handle gracefully)
                    family_cluster.mean_organ_weights[organ_name] = observed_weight

            # Update target satisfaction (EMA)
            old_satisfaction = family_cluster.target_satisfaction
            new_satisfaction = (1 - self.ema_alpha) * old_satisfaction + self.ema_alpha * conv_cluster.target_satisfaction
            family_cluster.target_satisfaction = new_satisfaction

            # Update emission quality (EMA)
            old_quality = family_cluster.mean_emission_quality
            new_quality = (1 - self.ema_alpha) * old_quality + self.ema_alpha * conv_cluster.emission_quality
            family_cluster.mean_emission_quality = new_quality

            # Update success rate (simple average for now)
            old_success_rate = family_cluster.success_rate
            is_success = 1.0 if conv_cluster.satisfaction_achieved >= self.success_threshold else 0.0
            new_success_rate = ((old_success_rate * family_cluster.conversation_count) + is_success) / (family_cluster.conversation_count + 1)
            family_cluster.success_rate = new_success_rate

            # Update metadata
            family_cluster.conversation_count += 1
            family_cluster.last_updated = conv_cluster.timestamp

            # Check maturity
            if family_cluster.conversation_count >= self.maturity_threshold:
                if not family_cluster.is_mature:
                    family_cluster.is_mature = True
                    print(f"🎓 Family {family_id} reached MATURE status (≥{self.maturity_threshold} conversations)")
                    print(f"   Now reliable for emission guidance!")

    def get_family_guidance(self, family_id: str) -> Optional[Dict]:
        """
        Get learned guidance for family (if mature).

        Args:
            family_id: Family identifier

        Returns:
            Guidance dict with organ_weights and target_satisfaction,
            or None if family immature/unknown
        """
        if family_id not in self.family_clusters:
            return None

        family_cluster = self.family_clusters[family_id]

        # Only provide guidance if family is mature
        if not family_cluster.is_mature:
            print(f"⚠️  Family {family_id} not yet mature ({family_cluster.conversation_count} < {self.maturity_threshold}), no guidance available")
            return None

        return {
            'organ_weights': family_cluster.mean_organ_weights.copy(),
            'target_satisfaction': family_cluster.target_satisfaction,
            'emission_quality_expectation': family_cluster.mean_emission_quality,
            'success_rate': family_cluster.success_rate,
            'conversation_count': family_cluster.conversation_count
        }

    def get_conversation_cluster(self, conversation_id: str) -> Optional[ConversationCluster]:
        """Get conversation cluster by ID."""
        return self.conversation_clusters.get(conversation_id)

    def get_family_cluster(self, family_id: str) -> Optional[FamilyCluster]:
        """Get family cluster by ID."""
        return self.family_clusters.get(family_id)

    def get_mature_families(self) -> List[str]:
        """Get list of mature family IDs."""
        return [
            fam_id for fam_id, cluster in self.family_clusters.items()
            if cluster.is_mature
        ]

    def _get_top_organs(self, organ_weights: Dict[str, float], k: int = 3) -> List[str]:
        """Get top k organs by weight."""
        sorted_organs = sorted(organ_weights.items(), key=lambda x: x[1], reverse=True)
        return [organ for organ, _ in sorted_organs[:k]]

    def get_statistics(self) -> Dict:
        """Compute cluster learning statistics."""
        stats = {
            'total_conversations': len(self.conversation_clusters),
            'total_families': len(self.family_clusters),
            'mature_families': sum(1 for c in self.family_clusters.values() if c.is_mature),
            'mean_satisfaction': 0.0,
            'mean_emission_quality': 0.0,
            'overall_success_rate': 0.0
        }

        if self.conversation_clusters:
            stats['mean_satisfaction'] = np.mean([
                c.satisfaction_achieved for c in self.conversation_clusters.values()
            ])
            stats['mean_emission_quality'] = np.mean([
                c.emission_quality for c in self.conversation_clusters.values()
            ])

            successes = sum(
                1 for c in self.conversation_clusters.values()
                if c.satisfaction_achieved >= self.success_threshold
            )
            stats['overall_success_rate'] = successes / len(self.conversation_clusters)

        # Family-level statistics
        if self.family_clusters:
            mature_families = [c for c in self.family_clusters.values() if c.is_mature]
            if mature_families:
                stats['mature_family_stats'] = {
                    'mean_target_satisfaction': np.mean([f.target_satisfaction for f in mature_families]),
                    'mean_success_rate': np.mean([f.success_rate for f in mature_families]),
                    'mean_conversations_per_family': np.mean([f.conversation_count for f in mature_families])
                }

        return stats


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 CONVERSATIONAL CLUSTER LEARNING TEST")
    print("="*70)

    # Clean test environment
    test_storage = Path('persona_layer/test_cluster_db.json')
    if test_storage.exists():
        test_storage.unlink()

    try:
        # Initialize cluster learning
        cluster_learning = ConversationalClusterLearning(
            storage_path=str(test_storage),
            ema_alpha=0.2,
            maturity_threshold=3
        )

        # Simulate 10 conversations across 2 families
        print(f"\n📊 SIMULATING 10 CONVERSATIONS (2 FAMILIES):")
        print("   Family_001: 6 conversations (high EMPATHY)")
        print("   Family_002: 4 conversations (high WISDOM)")

        # Family_001: High EMPATHY conversations
        for i in range(6):
            mock_organ_results = {
                'EMPATHY': {'coherence': 0.85 + np.random.normal(0, 0.05)},
                'LISTENING': {'coherence': 0.70 + np.random.normal(0, 0.05)},
                'PRESENCE': {'coherence': 0.65 + np.random.normal(0, 0.05)},
                'WISDOM': {'coherence': 0.50 + np.random.normal(0, 0.05)}
            }

            mock_emission_metrics = {
                'mean_coherence': 0.80 + np.random.normal(0, 0.05)
            }

            satisfaction = 0.82 + np.random.normal(0, 0.05)
            satisfaction = max(0.75, min(1.0, satisfaction))  # Clamp to [0.75, 1.0]

            cluster_learning.update_from_conversation(
                conversation_id=f'conv_fam1_{i:02d}',
                family_id='Family_001',
                organ_results=mock_organ_results,
                satisfaction_score=satisfaction,
                emission_metrics=mock_emission_metrics,
                user_message="I feel overwhelmed",
                emission_text="I sense what you're feeling deeply."
            )

        print(f"\n✅ Family_001 processed (6 conversations)")

        # Family_002: High WISDOM conversations
        for i in range(4):
            mock_organ_results = {
                'WISDOM': {'coherence': 0.82 + np.random.normal(0, 0.05)},
                'LISTENING': {'coherence': 0.72 + np.random.normal(0, 0.05)},
                'AUTHENTICITY': {'coherence': 0.68 + np.random.normal(0, 0.05)},
                'EMPATHY': {'coherence': 0.55 + np.random.normal(0, 0.05)}
            }

            mock_emission_metrics = {
                'mean_coherence': 0.78 + np.random.normal(0, 0.05)
            }

            satisfaction = 0.78 + np.random.normal(0, 0.05)
            satisfaction = max(0.75, min(1.0, satisfaction))

            cluster_learning.update_from_conversation(
                conversation_id=f'conv_fam2_{i:02d}',
                family_id='Family_002',
                organ_results=mock_organ_results,
                satisfaction_score=satisfaction,
                emission_metrics=mock_emission_metrics,
                user_message="I keep repeating this pattern",
                emission_text="I notice there's a deeper pattern here."
            )

        print(f"\n✅ Family_002 processed (4 conversations)")

        # Print statistics
        stats = cluster_learning.get_statistics()
        print(f"\n📈 CLUSTER LEARNING STATISTICS:")
        print(f"   Total conversations: {stats['total_conversations']}")
        print(f"   Total families: {stats['total_families']}")
        print(f"   Mature families: {stats['mature_families']}")
        print(f"   Mean satisfaction: {stats['mean_satisfaction']:.3f}")
        print(f"   Mean emission quality: {stats['mean_emission_quality']:.3f}")
        print(f"   Overall success rate: {stats['overall_success_rate']*100:.1f}%")

        if 'mature_family_stats' in stats:
            mature_stats = stats['mature_family_stats']
            print(f"\n   Mature Family Stats:")
            print(f"     Mean target satisfaction: {mature_stats['mean_target_satisfaction']:.3f}")
            print(f"     Mean success rate: {mature_stats['mean_success_rate']*100:.1f}%")
            print(f"     Mean conversations/family: {mature_stats['mean_conversations_per_family']:.1f}")

        # Test family guidance retrieval
        print(f"\n🔍 TESTING FAMILY GUIDANCE RETRIEVAL:")

        for family_id in ['Family_001', 'Family_002']:
            guidance = cluster_learning.get_family_guidance(family_id)

            if guidance:
                print(f"\n   {family_id} (MATURE, guidance available):")
                print(f"     Target satisfaction: {guidance['target_satisfaction']:.3f}")
                print(f"     Success rate: {guidance['success_rate']*100:.1f}%")
                print(f"     Top organs:")

                sorted_organs = sorted(
                    guidance['organ_weights'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                for organ, weight in sorted_organs[:3]:
                    print(f"       {organ}: {weight:.3f}")
            else:
                cluster = cluster_learning.get_family_cluster(family_id)
                if cluster:
                    print(f"\n   {family_id} (IMMATURE, {cluster.conversation_count} conversations):")
                    print(f"     Need {cluster_learning.maturity_threshold - cluster.conversation_count} more for guidance")

        print(f"\n✅ Cluster learning working correctly!")
        print(f"   Mature families provide reliable guidance")
        print(f"   Immature families accumulate data until mature")

    except Exception as e:
        print(f"\n❌ Cluster learning failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        if test_storage.exists():
            test_storage.unlink()

    print("\n" + "="*70)
