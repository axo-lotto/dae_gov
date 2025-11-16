"""
FeltDifferenceLearner - Learning from Transformation Patterns
==============================================================

Core component for learning which transformation pathways lead to high
satisfaction outcomes. Inspired by DAE 3.0's FeltDifferenceLearner that
enabled 841 perfect tasks with 47.3% ARC-AGI success.

Philosophy:
- Learn from HOW things change (not WHAT they are)
- Track transformation signatures that lead to satisfaction
- Hebbian co-occurrence: "what transforms together, succeeds together"
- Build intuition about which pathways work for different input types

Key Concepts:
- Felt Difference = How much felt-state transformed during processing
- Success Pathway = Transformation pattern that led to high satisfaction
- Failure Pathway = Transformation pattern that led to low satisfaction
- Pathway Confidence = EMA of success rate for specific transformation

Architecture:
- Input: TSK with transformation_signature and satisfaction
- Process: Update pathway confidence based on outcome
- Output: Learned transformation preferences

Expected Outcomes:
- Learn which V0 descent patterns lead to success
- Identify optimal convergence cycle counts
- Discover effective organ shift patterns
- Build confidence in specific nexus type transitions

Created: November 16, 2025
Status: Core learning component for epoch training
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, asdict, field
from collections import defaultdict

# Import TSK structures
from persona_layer.conversational_tsk_recorder import TransductiveSummaryKernel


@dataclass
class TransformationPathway:
    """
    Learned pathway representing a class of transformations.

    This captures what patterns of transformation lead to good/bad outcomes.
    Not specific instances, but learned clusters of transformation behavior.
    """
    pathway_id: str
    centroid_signature: List[float]  # 57D centroid of this pathway

    # Learning metrics
    success_count: int = 0
    failure_count: int = 0
    total_count: int = 0
    confidence: float = 0.5  # EMA-based confidence (0-1)

    # Outcome statistics
    mean_satisfaction: float = 0.5
    std_satisfaction: float = 0.0
    max_satisfaction: float = 0.5
    min_satisfaction: float = 0.5

    # Transformation characteristics
    mean_v0_descent: float = 0.5
    mean_convergence_cycles: float = 3.0
    kairos_rate: float = 0.0

    # Dominant features
    dominant_nexus_type: str = "Relational"
    dominant_organ_shifts: List[str] = field(default_factory=list)

    # Temporal
    first_seen: str = ""
    last_updated: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> 'TransformationPathway':
        return TransformationPathway(**data)


class FeltDifferenceLearner:
    """
    Learns which transformation patterns lead to successful outcomes.

    This is the core learning engine that:
    1. Clusters TSKs by transformation signature similarity
    2. Tracks success/failure rates for each pathway
    3. Updates pathway confidence using EMA
    4. Provides recommendations for future transformations

    Usage:
    ------
    >>> learner = FeltDifferenceLearner()
    >>> learner.learn_from_tsk(tsk)  # Update based on new TSK
    >>> pathway = learner.get_best_pathway(input_signature)  # Get recommendation
    >>> insights = learner.get_learning_insights()  # Analyze patterns
    """

    def __init__(
        self,
        storage_path: str = 'persona_layer/state/active/transformation_pathways.json',
        learning_rate: float = 0.1,
        success_threshold: float = 0.7,
        pathway_similarity_threshold: float = 0.75,
        min_samples_for_confidence: int = 5
    ):
        """
        Initialize FeltDifferenceLearner.

        Args:
            storage_path: Path to persist learned pathways
            learning_rate: EMA learning rate for confidence updates
            success_threshold: Satisfaction threshold for "success" classification
            pathway_similarity_threshold: Cosine similarity for pathway matching
            min_samples_for_confidence: Minimum samples before trusting confidence
        """
        self.storage_path = Path(storage_path)
        self.learning_rate = learning_rate
        self.success_threshold = success_threshold
        self.pathway_similarity_threshold = pathway_similarity_threshold
        self.min_samples_for_confidence = min_samples_for_confidence

        # Core data structures
        self.pathways: Dict[str, TransformationPathway] = {}
        self.tsk_to_pathway: Dict[str, str] = {}  # conversation_id -> pathway_id

        # Hebbian co-occurrence matrix (pathway × pathway)
        self.pathway_cooccurrence = defaultdict(lambda: defaultdict(float))

        # Learning statistics
        self.total_tsks_learned = 0
        self.success_rate_history: List[float] = []

        # Ensure storage directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing pathways
        self._load_pathways()

        print(f"✅ FeltDifferenceLearner initialized")
        print(f"   Storage: {self.storage_path}")
        print(f"   Learning rate: {self.learning_rate}")
        print(f"   Success threshold: {self.success_threshold}")
        print(f"   Existing pathways: {len(self.pathways)}")
        print(f"   Total TSKs learned: {self.total_tsks_learned}")

    def learn_from_tsk(self, tsk: TransductiveSummaryKernel) -> Dict[str, Any]:
        """
        Learn from a single TSK by updating pathway confidence.

        This is the core learning step:
        1. Find or create pathway for this transformation
        2. Classify as success/failure based on satisfaction
        3. Update pathway confidence using EMA
        4. Update pathway statistics

        Args:
            tsk: Transductive Summary Kernel to learn from

        Returns:
            Learning result dict
        """
        signature = np.array(tsk.transformation_signature)

        # Step 1: Find matching pathway or create new one
        pathway_id, similarity, is_new = self._assign_to_pathway(signature)
        pathway = self.pathways[pathway_id]

        # Step 2: Classify outcome
        is_success = tsk.final_satisfaction >= self.success_threshold
        outcome = "SUCCESS" if is_success else "FAILURE"

        # Step 3: Update pathway using EMA
        if is_success:
            pathway.success_count += 1
            target_confidence = 1.0
        else:
            pathway.failure_count += 1
            target_confidence = 0.0

        pathway.total_count += 1

        # EMA update: confidence = (1 - α) * old_confidence + α * new_observation
        pathway.confidence = (
            (1 - self.learning_rate) * pathway.confidence +
            self.learning_rate * target_confidence
        )

        # Step 4: Update pathway statistics
        self._update_pathway_statistics(pathway, tsk)

        # Step 5: Track mapping and persist
        self.tsk_to_pathway[tsk.conversation_id] = pathway_id
        self.total_tsks_learned += 1

        # Update success rate history
        current_success_rate = pathway.success_count / pathway.total_count
        self.success_rate_history.append(current_success_rate)

        # Auto-save periodically
        if self.total_tsks_learned % 10 == 0:
            self._save_pathways()

        return {
            'pathway_id': pathway_id,
            'is_new_pathway': is_new,
            'similarity': similarity,
            'outcome': outcome,
            'satisfaction': tsk.final_satisfaction,
            'pathway_confidence': pathway.confidence,
            'pathway_total_count': pathway.total_count,
            'total_tsks_learned': self.total_tsks_learned
        }

    def learn_from_tsk_batch(
        self,
        tsks: List[TransductiveSummaryKernel],
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Learn from a batch of TSKs (e.g., one epoch's worth).

        Args:
            tsks: List of TSKs to learn from
            verbose: Print progress

        Returns:
            Batch learning statistics
        """
        if verbose:
            print(f"\n🧠 Learning from {len(tsks)} TSKs...")

        results = []
        successes = 0
        new_pathways = 0

        for tsk in tsks:
            result = self.learn_from_tsk(tsk)
            results.append(result)

            if result['outcome'] == 'SUCCESS':
                successes += 1
            if result['is_new_pathway']:
                new_pathways += 1

        # Compute batch statistics
        success_rate = successes / len(tsks) if tsks else 0.0
        avg_confidence = np.mean([r['pathway_confidence'] for r in results])

        if verbose:
            print(f"   Batch success rate: {success_rate:.2%}")
            print(f"   New pathways created: {new_pathways}")
            print(f"   Average pathway confidence: {avg_confidence:.3f}")
            print(f"   Total pathways: {len(self.pathways)}")

        # Save after batch
        self._save_pathways()

        return {
            'batch_size': len(tsks),
            'success_rate': success_rate,
            'new_pathways': new_pathways,
            'avg_confidence': avg_confidence,
            'total_pathways': len(self.pathways),
            'results': results
        }

    def _assign_to_pathway(
        self,
        signature: np.ndarray
    ) -> Tuple[str, float, bool]:
        """
        Assign transformation signature to existing pathway or create new one.

        Args:
            signature: 57D transformation signature

        Returns:
            Tuple of (pathway_id, similarity, is_new_pathway)
        """
        # If no pathways yet, create first one
        if not self.pathways:
            pathway_id = "Pathway_001"
            new_pathway = TransformationPathway(
                pathway_id=pathway_id,
                centroid_signature=signature.tolist(),
                first_seen=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat()
            )
            self.pathways[pathway_id] = new_pathway
            return pathway_id, 1.0, True

        # Find most similar pathway
        best_pathway = None
        best_similarity = -1

        for pathway_id, pathway in self.pathways.items():
            centroid = np.array(pathway.centroid_signature)
            # Cosine similarity (signatures are L2 normalized)
            similarity = float(np.dot(signature, centroid))
            if similarity > best_similarity:
                best_similarity = similarity
                best_pathway = pathway_id

        # Match if above threshold
        if best_similarity >= self.pathway_similarity_threshold:
            # Update centroid incrementally
            pathway = self.pathways[best_pathway]
            old_centroid = np.array(pathway.centroid_signature)
            # Running average: new_centroid = (n * old + new) / (n + 1)
            n = pathway.total_count
            new_centroid = (n * old_centroid + signature) / (n + 1)
            # Re-normalize to unit sphere
            new_centroid = new_centroid / np.linalg.norm(new_centroid)
            pathway.centroid_signature = new_centroid.tolist()
            pathway.last_updated = datetime.now().isoformat()
            return best_pathway, best_similarity, False
        else:
            # Create new pathway
            pathway_num = len(self.pathways) + 1
            pathway_id = f"Pathway_{pathway_num:03d}"
            new_pathway = TransformationPathway(
                pathway_id=pathway_id,
                centroid_signature=signature.tolist(),
                first_seen=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat()
            )
            self.pathways[pathway_id] = new_pathway
            return pathway_id, best_similarity, True

    def _update_pathway_statistics(
        self,
        pathway: TransformationPathway,
        tsk: TransductiveSummaryKernel
    ):
        """
        Update pathway statistics based on new TSK.

        Args:
            pathway: Pathway to update
            tsk: New TSK observation
        """
        # Update satisfaction statistics (running mean)
        n = pathway.total_count
        old_mean = pathway.mean_satisfaction
        new_value = tsk.final_satisfaction

        # Welford's online algorithm for mean and variance
        new_mean = old_mean + (new_value - old_mean) / n
        pathway.mean_satisfaction = new_mean

        # Update min/max
        pathway.max_satisfaction = max(pathway.max_satisfaction, new_value)
        pathway.min_satisfaction = min(pathway.min_satisfaction, new_value)

        # Update transformation characteristics
        pathway.mean_v0_descent = (
            (pathway.mean_v0_descent * (n - 1) + tsk.v0_energy_descent) / n
        )
        pathway.mean_convergence_cycles = (
            (pathway.mean_convergence_cycles * (n - 1) + tsk.convergence_cycles) / n
        )

        # Update Kairos rate
        if tsk.kairos_detected:
            pathway.kairos_rate = (
                (pathway.kairos_rate * (n - 1) + 1.0) / n
            )
        else:
            pathway.kairos_rate = (
                (pathway.kairos_rate * (n - 1) + 0.0) / n
            )

        # Update dominant nexus type (mode)
        pathway.dominant_nexus_type = tsk.nexus_type_final

        # Update timestamp
        pathway.last_updated = datetime.now().isoformat()

    def get_best_pathway_for_input(
        self,
        input_signature: List[float]
    ) -> Optional[TransformationPathway]:
        """
        Get the best learned pathway for a given input signature.

        This is used during inference to recommend transformation strategy.

        Args:
            input_signature: 57D transformation signature of current state

        Returns:
            Best matching pathway with highest confidence, or None
        """
        if not self.pathways:
            return None

        signature = np.array(input_signature)
        best_pathway = None
        best_score = -1  # Combines similarity and confidence

        for pathway_id, pathway in self.pathways.items():
            centroid = np.array(pathway.centroid_signature)
            similarity = float(np.dot(signature, centroid))

            # Only consider if pathway is mature enough
            if pathway.total_count >= self.min_samples_for_confidence:
                # Score = similarity * confidence
                score = similarity * pathway.confidence
                if score > best_score:
                    best_score = score
                    best_pathway = pathway

        return best_pathway

    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Analyze learned transformation patterns.

        Returns:
            Dict with learning insights and statistics
        """
        if not self.pathways:
            return {'error': 'No pathways learned yet'}

        # Pathway statistics
        confidences = [p.confidence for p in self.pathways.values()]
        success_rates = [
            p.success_count / p.total_count if p.total_count > 0 else 0
            for p in self.pathways.values()
        ]
        satisfactions = [p.mean_satisfaction for p in self.pathways.values()]

        # Find best and worst pathways
        sorted_by_confidence = sorted(
            self.pathways.values(),
            key=lambda p: p.confidence,
            reverse=True
        )

        best_pathways = sorted_by_confidence[:3]
        worst_pathways = sorted_by_confidence[-3:]

        # Mature pathways (enough samples)
        mature_pathways = [
            p for p in self.pathways.values()
            if p.total_count >= self.min_samples_for_confidence
        ]

        return {
            'total_pathways': len(self.pathways),
            'total_tsks_learned': self.total_tsks_learned,
            'mean_confidence': float(np.mean(confidences)),
            'std_confidence': float(np.std(confidences)),
            'mean_success_rate': float(np.mean(success_rates)),
            'mean_satisfaction': float(np.mean(satisfactions)),
            'mature_pathways': len(mature_pathways),
            'best_pathways': [
                {
                    'id': p.pathway_id,
                    'confidence': p.confidence,
                    'success_rate': p.success_count / p.total_count,
                    'mean_satisfaction': p.mean_satisfaction,
                    'total_count': p.total_count
                }
                for p in best_pathways
            ],
            'worst_pathways': [
                {
                    'id': p.pathway_id,
                    'confidence': p.confidence,
                    'success_rate': p.success_count / p.total_count,
                    'mean_satisfaction': p.mean_satisfaction,
                    'total_count': p.total_count
                }
                for p in worst_pathways
            ]
        }

    def get_pathway_recommendations(
        self,
        current_state: Dict
    ) -> List[Dict[str, Any]]:
        """
        Get recommendations for transformation based on learned pathways.

        Args:
            current_state: Current felt state dict

        Returns:
            List of recommended pathways with expected outcomes
        """
        if not self.pathways:
            return []

        # Rank pathways by confidence * success_rate
        ranked = sorted(
            [
                p for p in self.pathways.values()
                if p.total_count >= self.min_samples_for_confidence
            ],
            key=lambda p: p.confidence * (p.success_count / p.total_count),
            reverse=True
        )

        recommendations = []
        for pathway in ranked[:5]:
            recommendations.append({
                'pathway_id': pathway.pathway_id,
                'confidence': pathway.confidence,
                'success_rate': pathway.success_count / pathway.total_count,
                'expected_satisfaction': pathway.mean_satisfaction,
                'expected_v0_descent': pathway.mean_v0_descent,
                'expected_cycles': pathway.mean_convergence_cycles,
                'kairos_likelihood': pathway.kairos_rate,
                'dominant_nexus': pathway.dominant_nexus_type,
                'sample_count': pathway.total_count
            })

        return recommendations

    def _save_pathways(self):
        """Save learned pathways to disk."""
        data = {
            'pathways': {
                pid: pathway.to_dict()
                for pid, pathway in self.pathways.items()
            },
            'total_tsks_learned': self.total_tsks_learned,
            'learning_rate': self.learning_rate,
            'success_threshold': self.success_threshold,
            'pathway_similarity_threshold': self.pathway_similarity_threshold,
            'last_updated': datetime.now().isoformat()
        }

        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_pathways(self):
        """Load pathways from disk."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path) as f:
                data = json.load(f)

            # Restore pathways
            for pid, pathway_data in data.get('pathways', {}).items():
                self.pathways[pid] = TransformationPathway.from_dict(pathway_data)

            self.total_tsks_learned = data.get('total_tsks_learned', 0)

            print(f"   Loaded {len(self.pathways)} pathways from disk")

        except Exception as e:
            print(f"⚠️  Failed to load pathways: {e}")

    def reset(self):
        """Reset all learned pathways (fresh start)."""
        self.pathways.clear()
        self.tsk_to_pathway.clear()
        self.total_tsks_learned = 0
        self.success_rate_history.clear()

        # Remove storage file if exists
        if self.storage_path.exists():
            self.storage_path.unlink()

        print(f"🔄 FeltDifferenceLearner reset to fresh state")

    def export_learning_report(self, output_path: str):
        """
        Export comprehensive learning report.

        Args:
            output_path: Path to save report JSON
        """
        report = {
            'learner_type': 'FeltDifferenceLearner',
            'timestamp': datetime.now().isoformat(),
            'total_pathways': len(self.pathways),
            'total_tsks_learned': self.total_tsks_learned,
            'learning_insights': self.get_learning_insights(),
            'pathway_details': {
                pid: pathway.to_dict()
                for pid, pathway in self.pathways.items()
            },
            'configuration': {
                'learning_rate': self.learning_rate,
                'success_threshold': self.success_threshold,
                'pathway_similarity_threshold': self.pathway_similarity_threshold,
                'min_samples_for_confidence': self.min_samples_for_confidence
            }
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📊 Learning report exported to: {output_path}")


# Example usage & testing
if __name__ == "__main__":
    print("🧠 FeltDifferenceLearner - Standalone Test\n")

    # Create learner
    learner = FeltDifferenceLearner()

    # Create mock TSKs
    print("\n" + "="*70)
    print("Creating mock TSKs for testing...")
    print("="*70)

    from persona_layer.conversational_tsk_recorder import TransductiveSummaryKernel

    # High satisfaction TSK (should become success pathway)
    high_sat_tsk = TransductiveSummaryKernel(
        conversation_id="test_high_sat",
        timestamp=datetime.now().isoformat(),
        user_input="I feel safe here",
        response_text="Honoring your safety",
        initial_v0_energy=1.0,
        final_v0_energy=0.3,
        v0_energy_descent=0.7,
        convergence_cycles=3,
        final_satisfaction=0.85,
        emission_confidence=0.7,
        transformation_signature=[0.1] * 57  # Simple uniform signature
    )

    # Low satisfaction TSK (should become failure pathway)
    low_sat_tsk = TransductiveSummaryKernel(
        conversation_id="test_low_sat",
        timestamp=datetime.now().isoformat(),
        user_input="I feel anxious",
        response_text="Generic response",
        initial_v0_energy=1.0,
        final_v0_energy=0.8,  # Poor descent
        v0_energy_descent=0.2,
        convergence_cycles=5,
        final_satisfaction=0.4,  # Below threshold
        emission_confidence=0.3,
        transformation_signature=[-0.1] * 57  # Different signature
    )

    print("\nLearning from high satisfaction TSK...")
    result1 = learner.learn_from_tsk(high_sat_tsk)
    print(f"   Result: {result1['outcome']}")
    print(f"   Pathway: {result1['pathway_id']}")
    print(f"   Confidence: {result1['pathway_confidence']:.3f}")

    print("\nLearning from low satisfaction TSK...")
    result2 = learner.learn_from_tsk(low_sat_tsk)
    print(f"   Result: {result2['outcome']}")
    print(f"   Pathway: {result2['pathway_id']}")
    print(f"   Confidence: {result2['pathway_confidence']:.3f}")

    print("\n" + "="*70)
    print("Learning Insights:")
    print("="*70)
    insights = learner.get_learning_insights()
    print(f"   Total pathways: {insights['total_pathways']}")
    print(f"   Total TSKs learned: {insights['total_tsks_learned']}")
    print(f"   Mean confidence: {insights['mean_confidence']:.3f}")

    print("\n✅ FeltDifferenceLearner test complete!")
