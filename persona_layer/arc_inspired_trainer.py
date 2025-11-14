#!/usr/bin/env python3
"""
Arc-Inspired Training - Pattern Completion Learning
===================================================

Training paradigm inspired by ARC (Abstraction and Reasoning Corpus):
- Show organism 2 input→output examples
- Ask organism to predict 3rd output
- Compare prediction to ground truth
- Learn from alignment/misalignment

Philosophy (Whiteheadian):
- Contrast: Learning through difference (predicted vs actual)
- Pattern: Eternal objects emerge through repetition
- Satisfaction: Self-assessment of prediction quality
- Concrescence: Organism "feels" the arc between examples

Architecture:
1. Pattern Exposure Phase: Process 2 examples (no learning)
2. Prediction Phase: Generate response for 3rd input
3. Assessment Phase: Compare prediction to ground truth
4. Learning Phase: Update based on misalignment

Expected Benefits:
- Faster family discovery (patterns become explicit)
- Better confidence calibration (organism assesses own predictions)
- Meta-learning (organism learns how to learn from examples)
- Voice consistency (organism maintains coherence across arc)

Date: November 12, 2025
Status: Arc-Inspired Training v1.0
"""

import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from datetime import datetime
import numpy as np

# Embedding model for semantic similarity
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  Warning: sentence-transformers not installed. Falling back to length-based similarity.")


class ArcInspiredTrainer:
    """
    Arc-Inspired Training: 2 examples → predict 3rd → assess → learn.

    Training loop:
    1. Select 3 related pairs from corpus (same category/family)
    2. Expose organism to first 2 pairs (pattern recognition)
    3. Generate prediction for 3rd input (without seeing target)
    4. Compare prediction to ground truth (self-assessment)
    5. Learn from misalignment (both Phase 5 + Hebbian)

    Metrics tracked:
    - Prediction confidence (organism's self-assessment)
    - Alignment score (prediction vs ground truth similarity)
    - Pattern recognition quality (organ activation consistency)
    - Voice consistency (emission path stability across arc)
    """

    def __init__(
        self,
        organism_wrapper,
        training_pairs: List[Dict],
        enable_learning: bool = True,
        assessment_threshold: float = 0.65  # Min similarity for "good" prediction
    ):
        """
        Initialize Arc-Inspired Trainer.

        Args:
            organism_wrapper: ConversationalOrganismWrapper instance
            training_pairs: Full corpus of training pairs
            enable_learning: Enable Phase 5 learning from assessments
            assessment_threshold: Minimum similarity for positive assessment
        """
        self.organism = organism_wrapper
        self.training_pairs = training_pairs
        self.enable_learning = enable_learning
        self.assessment_threshold = assessment_threshold

        # CRITICAL FIX: Enable learning on organism's phase5 integration
        # The organism defaults to enable_learning=False, but arc trainer
        # needs to explicitly enable it for organic family discovery
        if self.enable_learning and hasattr(self.organism, 'phase5_learning'):
            if self.organism.phase5_learning:
                self.organism.phase5_learning.enable_learning = True
                print("   ✅ Phase 5 learning ENABLED on organism")
            else:
                print("   ⚠️  Phase 5 learning not available")
                self.enable_learning = False
        elif not self.enable_learning:
            print("   ℹ️  Phase 5 learning DISABLED by trainer config")

        # Initialize embedding model for semantic similarity
        if EMBEDDINGS_AVAILABLE:
            print("   Loading embedding model for semantic similarity...")
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim, fast
            self.use_embeddings = True
            print("   ✅ Embedding model loaded (384-dim)")
        else:
            self.embedder = None
            self.use_embeddings = False
            print("   ⚠️  Using length-based similarity (fallback)")

        # Group pairs by category for arc selection
        self.pairs_by_category = self._group_by_category()

        # Training metrics
        self.arc_results = []
        self.total_arcs_processed = 0
        self.successful_predictions = 0

        print("🌀 Arc-Inspired Trainer initialized")
        print(f"   Training pairs: {len(training_pairs)}")
        print(f"   Categories: {len(self.pairs_by_category)}")
        print(f"   Learning: {'✅ ACTIVE' if enable_learning else '❌ INACTIVE'}")
        print(f"   Assessment threshold: {assessment_threshold}")
        print(f"   Semantic similarity: {'SANS embeddings' if self.use_embeddings else 'Length-based (fallback)'}")

    def _group_by_category(self) -> Dict[str, List[Dict]]:
        """Group training pairs by category for arc selection."""
        groups = {}
        for pair in self.training_pairs:
            # Handle both old format (pair_metadata) and new format (direct category field)
            if 'pair_metadata' in pair:
                category = pair['pair_metadata'].get('category', 'unknown')
            else:
                category = pair.get('category', 'unknown')

            if category not in groups:
                groups[category] = []
            groups[category].append(pair)
        return groups

    def _get_input(self, pair: Dict) -> str:
        """Extract input from pair, handling both old and new formats."""
        return pair.get('input_text', pair.get('input', ''))

    def _get_output(self, pair: Dict) -> str:
        """Extract output from pair, handling both old and new formats."""
        return pair.get('output_text', pair.get('output', ''))

    def _get_category(self, pair: Dict) -> str:
        """Extract category from pair, handling both old and new formats."""
        if 'pair_metadata' in pair:
            return pair['pair_metadata'].get('category', 'unknown')
        return pair.get('category', 'unknown')

    def _get_id(self, pair: Dict) -> str:
        """Extract ID from pair, handling both old and new formats."""
        if 'pair_metadata' in pair:
            return pair['pair_metadata'].get('id', 'unknown')
        # New format doesn't have IDs, generate from category
        category = self._get_category(pair)
        return f"{category}_{id(pair)}"

    def _select_arc_triplet(self, category: Optional[str] = None) -> Optional[Tuple[Dict, Dict, Dict]]:
        """
        Select 3 related pairs for arc training.

        Args:
            category: Specific category to sample from (or None for random)

        Returns:
            (example1, example2, target) or None if not enough pairs
        """
        if category and category in self.pairs_by_category:
            pool = self.pairs_by_category[category]
        else:
            # Pick random category with ≥3 pairs
            valid_categories = [cat for cat, pairs in self.pairs_by_category.items()
                                if len(pairs) >= 3]
            if not valid_categories:
                return None
            category = np.random.choice(valid_categories)
            pool = self.pairs_by_category[category]

        if len(pool) < 3:
            return None

        # Sample 3 pairs without replacement
        indices = np.random.choice(len(pool), 3, replace=False)
        return pool[indices[0]], pool[indices[1]], pool[indices[2]]

    def _compute_alignment_score(
        self,
        predicted_response: str,
        predicted_confidence: float,
        predicted_path: str,
        predicted_felt_states: Dict,
        target_output: str,
        target_pair: Dict
    ) -> Dict:
        """
        Assess alignment between prediction and ground truth.

        Metrics:
        - Semantic similarity (SANS organ embedding distance)
        - Confidence alignment (is organism's confidence warranted?)
        - Path alignment (does emission strategy match target's implied path?)
        - Satisfaction alignment (did organism feel satisfied?)

        Returns:
            {
                'semantic_similarity': float (0-1),
                'confidence_aligned': bool,
                'path_appropriate': bool,
                'overall_score': float (0-1),
                'assessment': str ('excellent' | 'good' | 'partial' | 'poor')
            }
        """
        # 1. Semantic similarity (using SANS embeddings)
        try:
            if self.use_embeddings and self.embedder is not None:
                # Use SANS embeddings for true semantic similarity
                pred_embedding = self.embedder.encode(predicted_response, convert_to_numpy=True)
                target_embedding = self.embedder.encode(target_output, convert_to_numpy=True)

                # Normalize embeddings
                pred_norm = pred_embedding / np.linalg.norm(pred_embedding)
                target_norm = target_embedding / np.linalg.norm(target_embedding)

                # Cosine similarity (dot product of normalized vectors)
                semantic_similarity = float(np.dot(pred_norm, target_norm))

                # Ensure in [0, 1] range (cosine can be [-1, 1])
                semantic_similarity = (semantic_similarity + 1.0) / 2.0
            else:
                # Fallback to length-based similarity
                pred_len = len(predicted_response.split())
                target_len = len(target_output.split())
                length_similarity = 1.0 - min(abs(pred_len - target_len) / max(pred_len, target_len, 1), 1.0)
                semantic_similarity = length_similarity
        except Exception as e:
            print(f"   ⚠️  Error computing semantic similarity: {e}")
            semantic_similarity = 0.5

        # 2. Confidence alignment (is confidence appropriate for quality?)
        confidence_aligned = (
            (semantic_similarity >= 0.7 and predicted_confidence >= 0.5) or
            (semantic_similarity < 0.7 and predicted_confidence < 0.5)
        )

        # 3. Path appropriateness (did organism use sensible strategy?)
        path_appropriate = predicted_path in ['hebbian_fallback', 'direct_reconstruction', 'family_template']

        # 4. Satisfaction alignment
        satisfaction = predicted_felt_states.get('satisfaction_final', 0.0)
        satisfaction_aligned = satisfaction >= 0.75

        # 5. Overall score (weighted average)
        overall_score = (
            0.60 * semantic_similarity +
            0.20 * (1.0 if confidence_aligned else 0.0) +
            0.10 * (1.0 if path_appropriate else 0.0) +
            0.10 * satisfaction
        )

        # 6. Assessment label
        if overall_score >= 0.85:
            assessment = 'excellent'
        elif overall_score >= self.assessment_threshold:
            assessment = 'good'
        elif overall_score >= 0.40:
            assessment = 'partial'
        else:
            assessment = 'poor'

        return {
            'semantic_similarity': float(semantic_similarity),
            'confidence_aligned': bool(confidence_aligned),
            'path_appropriate': bool(path_appropriate),
            'satisfaction': float(satisfaction),
            'overall_score': float(overall_score),
            'assessment': assessment,
            'prediction_confidence': float(predicted_confidence),
            'prediction_path': predicted_path
        }

    def train_arc(self, category: Optional[str] = None, verbose: bool = True) -> Optional[Dict]:
        """
        Run single arc training iteration.

        Process:
        1. Select 3 related pairs (same category)
        2. Expose organism to examples 1 & 2 (pattern recognition)
        3. Generate prediction for input 3
        4. Compare prediction to target output 3
        5. Learn from misalignment (if enabled)

        Args:
            category: Specific category to train on (or None for random)
            verbose: Print detailed progress

        Returns:
            Arc results dict or None if no valid triplet found
        """
        # Step 1: Select arc triplet
        triplet = self._select_arc_triplet(category)
        if triplet is None:
            if verbose:
                print(f"⚠️  No valid arc triplet available (category={category})")
            return None

        example1, example2, target = triplet
        arc_id = f"arc_{self.total_arcs_processed:04d}_{self._get_category(target)}"

        if verbose:
            print(f"\n🌀 Arc Training: {arc_id}")
            print(f"   Category: {self._get_category(target)}")
            print(f"   Example 1: {self._get_id(example1)}")
            print(f"   Example 2: {self._get_id(example2)}")
            print(f"   Target: {self._get_id(target)}")

        # Step 2: Expose pattern (examples 1 & 2) - NO LEARNING
        if verbose:
            print(f"\n   📖 Pattern Exposure Phase (2 examples)...")

        example1_result = self.organism.process_text(
            self._get_input(example1),
            context={'arc_id': arc_id, 'role': 'example1'},
            enable_tsk_recording=False,
            enable_phase2=True
        )

        example2_result = self.organism.process_text(
            self._get_input(example2),
            context={'arc_id': arc_id, 'role': 'example2'},
            enable_tsk_recording=False,
            enable_phase2=True
        )

        # Step 3: Generate prediction for target input
        if verbose:
            print(f"\n   🎯 Prediction Phase (generate for target input)...")

        prediction_result = self.organism.process_text(
            self._get_input(target),
            context={'arc_id': arc_id, 'role': 'prediction'},
            enable_tsk_recording=False,
            enable_phase2=True
        )

        predicted_response = prediction_result.get('emission_text', '')
        predicted_confidence = prediction_result.get('emission_confidence', 0.0)
        predicted_path = prediction_result.get('emission_path', 'unknown')
        predicted_felt_states = prediction_result.get('felt_states', {})

        if verbose:
            print(f"      Predicted: \"{predicted_response[:60]}...\"")
            print(f"      Confidence: {predicted_confidence:.3f}")
            print(f"      Path: {predicted_path}")

        # Step 4: Assess prediction vs ground truth
        if verbose:
            print(f"\n   📊 Assessment Phase (compare to ground truth)...")

        target_output = self._get_output(target)
        alignment = self._compute_alignment_score(
            predicted_response,
            predicted_confidence,
            predicted_path,
            predicted_felt_states,
            target_output,
            target
        )

        if verbose:
            print(f"      Ground truth: \"{target_output[:60]}...\"")
            print(f"      Semantic similarity: {alignment['semantic_similarity']:.3f}")
            print(f"      Overall score: {alignment['overall_score']:.3f}")
            print(f"      Assessment: {alignment['assessment'].upper()}")

        # Step 5: Learn from assessment (if enabled)
        learning_applied = False
        if self.enable_learning:
            if verbose:
                print(f"\n   🧠 Learning Phase...")

            # Learn from ALL 3 occasions (pattern + prediction)
            # This is the key insight: organism learns from the arc itself

            # Learn from example 1 (high satisfaction assumed)
            if hasattr(self.organism, 'phase5_learning') and self.organism.phase5_learning:
                try:
                    assembled_response_1 = type('obj', (object,), {
                        'text': example1_result.get('emission_text', ''),
                        'confidence': example1_result.get('emission_confidence', 0.0),
                        'emission_path': example1_result.get('emission_path', ''),
                        'satisfaction': example1_result.get('felt_states', {}).get('satisfaction_final', 0.8)
                    })()

                    self.organism.phase5_learning.learn_from_conversation(
                        organ_results=example1_result.get('organ_results', {}),
                        assembled_response=assembled_response_1,
                        user_message=self._get_input(example1),
                        conversation_id=f"{arc_id}_ex1"
                    )

                    # Learn from example 2
                    assembled_response_2 = type('obj', (object,), {
                        'text': example2_result.get('emission_text', ''),
                        'confidence': example2_result.get('emission_confidence', 0.0),
                        'emission_path': example2_result.get('emission_path', ''),
                        'satisfaction': example2_result.get('felt_states', {}).get('satisfaction_final', 0.8)
                    })()

                    self.organism.phase5_learning.learn_from_conversation(
                        organ_results=example2_result.get('organ_results', {}),
                        assembled_response=assembled_response_2,
                        user_message=self._get_input(example2),
                        conversation_id=f"{arc_id}_ex2"
                    )

                    # Learn from prediction ONLY if assessment is good+
                    if alignment['overall_score'] >= self.assessment_threshold:
                        assembled_response_pred = type('obj', (object,), {
                            'text': predicted_response,
                            'confidence': predicted_confidence,
                            'emission_path': predicted_path,
                            'satisfaction': alignment['overall_score']  # Use assessment as satisfaction
                        })()

                        self.organism.phase5_learning.learn_from_conversation(
                            organ_results=predicted_felt_states.get('organ_results', {}),
                            assembled_response=assembled_response_pred,
                            user_message=self._get_input(target),
                            conversation_id=f"{arc_id}_pred"
                        )

                        learning_applied = True
                        if verbose:
                            print(f"      ✅ Learning applied to all 3 occasions (prediction quality: {alignment['assessment']})")
                    else:
                        if verbose:
                            print(f"      ⚠️  Learning applied to examples only (prediction quality too low: {alignment['assessment']})")
                        learning_applied = True  # Still learned from examples

                except Exception as e:
                    if verbose:
                        print(f"      ❌ Learning error: {e}")
                    learning_applied = False

        # Track results
        arc_result = {
            'arc_id': arc_id,
            'category': self._get_category(target),
            'timestamp': datetime.now().isoformat(),
            'examples': {
                'example1_id': self._get_id(example1),
                'example2_id': self._get_id(example2),
                'target_id': self._get_id(target)
            },
            'prediction': {
                'text': predicted_response,
                'confidence': predicted_confidence,
                'path': predicted_path,
                'felt_states': {
                    'satisfaction': predicted_felt_states.get('satisfaction_final', 0.0),
                    'convergence_cycles': predicted_felt_states.get('convergence_cycles', 0),
                    'nexuses_formed': predicted_felt_states.get('nexuses_formed', 0),
                    'zone_id': predicted_felt_states.get('zone_id', 0)
                }
            },
            'ground_truth': {
                'text': target_output
            },
            'assessment': alignment,
            'learning_applied': learning_applied
        }

        self.arc_results.append(arc_result)
        self.total_arcs_processed += 1
        if alignment['overall_score'] >= self.assessment_threshold:
            self.successful_predictions += 1

        return arc_result

    def train_epoch(
        self,
        num_arcs: int = 50,
        category_distribution: Optional[Dict[str, float]] = None,
        verbose: bool = False
    ) -> Dict:
        """
        Train full epoch of arc iterations.

        Args:
            num_arcs: Number of arc triplets to process
            category_distribution: Optional dict of category→probability
            verbose: Print detailed progress for each arc

        Returns:
            Epoch summary statistics
        """
        print(f"\n🌀 Arc Training Epoch Beginning ({num_arcs} arcs)")
        print("="*60)

        epoch_start = self.total_arcs_processed
        epoch_successes = 0
        category_counts = {}
        assessment_counts = {'excellent': 0, 'good': 0, 'partial': 0, 'poor': 0}

        for i in range(num_arcs):
            # Select category (weighted if distribution provided)
            if category_distribution:
                category = np.random.choice(
                    list(category_distribution.keys()),
                    p=list(category_distribution.values())
                )
            else:
                category = None

            # Run arc training
            arc_result = self.train_arc(category=category, verbose=verbose)

            if arc_result:
                cat = arc_result['category']
                category_counts[cat] = category_counts.get(cat, 0) + 1

                assessment = arc_result['assessment']['assessment']
                assessment_counts[assessment] += 1

                if arc_result['assessment']['overall_score'] >= self.assessment_threshold:
                    epoch_successes += 1

                # Progress indicator
                if (i + 1) % 10 == 0 or (i + 1) == num_arcs:
                    success_rate = epoch_successes / (i + 1) if (i + 1) > 0 else 0.0
                    print(f"   [{i+1}/{num_arcs}] Success rate: {success_rate:.1%}")

        # Epoch summary
        epoch_end = self.total_arcs_processed
        arcs_processed = epoch_end - epoch_start

        print(f"\n📊 Arc Training Epoch Complete")
        print("="*60)
        print(f"   Arcs processed: {arcs_processed}")
        print(f"   Success rate: {epoch_successes}/{arcs_processed} ({100*epoch_successes/arcs_processed:.1f}%)")
        print(f"\n   Assessment distribution:")
        for assessment, count in assessment_counts.items():
            pct = 100 * count / arcs_processed if arcs_processed > 0 else 0.0
            print(f"      {assessment}: {count} ({pct:.1f}%)")

        print(f"\n   Category distribution:")
        for cat, count in sorted(category_counts.items()):
            pct = 100 * count / arcs_processed if arcs_processed > 0 else 0.0
            print(f"      {cat}: {count} ({pct:.1f}%)")

        return {
            'arcs_processed': arcs_processed,
            'success_rate': epoch_successes / arcs_processed if arcs_processed > 0 else 0.0,
            'assessment_distribution': assessment_counts,
            'category_distribution': category_counts
        }

    def save_results(self, output_path: str):
        """Save all arc training results to JSON."""
        output = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_arcs_processed': self.total_arcs_processed,
                'successful_predictions': self.successful_predictions,
                'overall_success_rate': self.successful_predictions / self.total_arcs_processed if self.total_arcs_processed > 0 else 0.0,
                'assessment_threshold': self.assessment_threshold,
                'learning_enabled': self.enable_learning
            },
            'results': self.arc_results
        }

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"💾 Arc training results saved to: {output_path}")

    def get_statistics(self) -> Dict:
        """Get training statistics summary."""
        if not self.arc_results:
            return {'error': 'No arc results yet'}

        scores = [r['assessment']['overall_score'] for r in self.arc_results]
        confidences = [r['prediction']['confidence'] for r in self.arc_results]
        assessments = [r['assessment']['assessment'] for r in self.arc_results]

        return {
            'total_arcs': self.total_arcs_processed,
            'successful_predictions': self.successful_predictions,
            'success_rate': self.successful_predictions / self.total_arcs_processed if self.total_arcs_processed > 0 else 0.0,
            'mean_alignment_score': float(np.mean(scores)),
            'mean_prediction_confidence': float(np.mean(confidences)),
            'assessment_distribution': {
                'excellent': sum(1 for a in assessments if a == 'excellent'),
                'good': sum(1 for a in assessments if a == 'good'),
                'partial': sum(1 for a in assessments if a == 'partial'),
                'poor': sum(1 for a in assessments if a == 'poor')
            }
        }


if __name__ == "__main__":
    print("Arc-Inspired Trainer v1.0")
    print("Run via: python3 training/conversational/run_arc_training.py")
