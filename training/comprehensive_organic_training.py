"""
🌀 Comprehensive Organic Intelligence Training
Complete memory scaffolding with TSK logs, family tracking, and metrics

This script extends turn-by-turn training with complete data capture:
1. TSK (Transductive State Knowledge) logs per turn
2. Family emergence tracking per epoch
3. Pattern database snapshots
4. Organ activation distributions
5. Comprehensive intelligence metrics
6. Learning trajectory analysis

Created: November 17, 2025 (Week 4, Day 1 - Enhanced)
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np
import shutil

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from training.organic_intelligence_metrics import OrganicIntelligenceEvaluator


class ComprehensiveTrainingScaffold:
    """
    Complete training scaffolding with full memory capture.

    Captures:
    - TSK logs per turn (57D transformation signatures)
    - Family evolution snapshots per epoch
    - Pattern database growth
    - Organ activation distributions
    - Learning trajectory metrics
    - Satisfaction fingerprint detection
    """

    def __init__(self, output_dir: str):
        """
        Initialize training scaffold.

        Args:
            output_dir: Base directory for all training outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for different data types
        self.tsk_dir = self.output_dir / "tsk_logs"
        self.family_dir = self.output_dir / "family_snapshots"
        self.pattern_dir = self.output_dir / "pattern_snapshots"
        self.metrics_dir = self.output_dir / "metrics"
        self.organ_dir = self.output_dir / "organ_distributions"

        for d in [self.tsk_dir, self.family_dir, self.pattern_dir, self.metrics_dir, self.organ_dir]:
            d.mkdir(exist_ok=True)

        # Initialize metrics evaluator
        self.evaluator = OrganicIntelligenceEvaluator()

        # Training state
        self.current_epoch = 0
        self.training_metadata = {
            'start_time': datetime.now().isoformat(),
            'total_epochs': 0,
            'turns_per_conversation': 3,
            'training_corpus': 'crisis_urgency + shadow_exile',
            'learning_mode': 'INTELLIGENCE_EMERGENCE_MODE'
        }

    def save_tsk_snapshot(self, epoch: int, turn_number: int, result: Dict[str, Any], pair_id: str):
        """
        Save complete TSK (Transductive State Knowledge) for a single turn.

        Captures 57D transformation signature including:
        - Organ activations (12 organs)
        - V0 energy descent
        - Nexus formations
        - Satisfaction evolution
        - Polyvagal state
        - Zone classification
        - RNX/TSK transduction metrics
        """
        tsk_data = {
            'timestamp': datetime.now().isoformat(),
            'epoch': epoch,
            'turn': turn_number,
            'pair_id': pair_id,

            # Core felt-state
            'felt_states': result.get('felt_states', {}),
            'satisfaction': result.get('felt_states', {}).get('satisfaction', 0.0),
            'urgency': result.get('felt_states', {}).get('urgency', 0.5),
            'zone': result.get('felt_states', {}).get('zone', 3),
            'polyvagal_state': result.get('felt_states', {}).get('eo_polyvagal_state', 'unknown'),

            # Organ activations (12 organs)
            'organ_results': {
                organ: {
                    'coherence': data.get('coherence', 0.0),
                    'atoms': data.get('atoms', []),
                    'active_atom_count': len(data.get('atoms', []))
                }
                for organ, data in result.get('organ_results', {}).items()
            },

            # V0 energy & convergence
            'v0_energy': result.get('felt_states', {}).get('v0_energy', {}),
            'convergence_cycles': result.get('felt_states', {}).get('v0_energy', {}).get('cycles', 0) if isinstance(result.get('felt_states', {}).get('v0_energy'), dict) else 0,

            # Nexus formations
            'nexuses': result.get('felt_states', {}).get('nexuses', []),
            'nexus_count': len(result.get('felt_states', {}).get('nexuses', [])),

            # Emission data
            'emission': result.get('emission', ''),
            'emission_strategy': result.get('emission_strategy', 'unknown'),
            'emission_confidence': result.get('emission_confidence', 0.0),

            # Family assignment
            'family_assigned': result.get('family_assigned', 'unknown'),
            'family_similarity': result.get('family_similarity', 0.0),

            # Learning signal
            'learning_update_occurred': result.get('learning_update_occurred', False),
            'modulated_satisfaction': result.get('modulated_satisfaction', None)
        }

        # Save TSK to file
        tsk_file = self.tsk_dir / f"epoch{epoch:02d}_turn{turn_number:04d}_{pair_id}.json"
        with open(tsk_file, 'w') as f:
            json.dump(tsk_data, f, indent=2)

    def save_family_snapshot(self, epoch: int, family_file_path: str):
        """
        Save complete family state at end of epoch.

        Captures:
        - All families with their members
        - Family centroids (65D signatures)
        - Intra-family coherence
        - Inter-family separation
        """
        if not os.path.exists(family_file_path):
            return

        with open(family_file_path) as f:
            families = json.load(f)

        # Add epoch metadata
        snapshot = {
            'epoch': epoch,
            'timestamp': datetime.now().isoformat(),
            'family_count': len(families.get('families', {})),
            'families': families.get('families', {}),

            # Compute family statistics
            'statistics': self._compute_family_statistics(families.get('families', {}))
        }

        snapshot_file = self.family_dir / f"epoch{epoch:02d}_families.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)

    def save_pattern_snapshot(self, epoch: int, pattern_file_path: str):
        """
        Save complete pattern database state at end of epoch.

        Captures:
        - All patterns (nexus signatures)
        - All phrases with qualities
        - Update counts
        - Quality distributions
        """
        if not os.path.exists(pattern_file_path):
            # Create empty snapshot
            snapshot = {
                'epoch': epoch,
                'timestamp': datetime.now().isoformat(),
                'total_patterns': 0,
                'total_phrases': 0,
                'patterns': {}
            }
        else:
            with open(pattern_file_path) as f:
                patterns = json.load(f)

            snapshot = {
                'epoch': epoch,
                'timestamp': datetime.now().isoformat(),
                'total_patterns': len(patterns.get('patterns', {})),
                'total_phrases': sum(
                    len(p.get('phrases', {}))
                    for p in patterns.get('patterns', {}).values()
                ),
                'patterns': patterns.get('patterns', {}),

                # Compute pattern statistics
                'statistics': self._compute_pattern_statistics(patterns.get('patterns', {}))
            }

        snapshot_file = self.pattern_dir / f"epoch{epoch:02d}_patterns.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)

    def save_organ_distribution(self, epoch: int, tsks: List[Dict[str, Any]]):
        """
        Save organ activation distribution for epoch.

        Analyzes which organs activate most frequently and their coalitions.
        """
        organ_activations = {}
        organ_coalitions = []

        for tsk in tsks:
            # Count active organs
            for organ, data in tsk.get('organ_results', {}).items():
                if organ not in organ_activations:
                    organ_activations[organ] = {
                        'activation_count': 0,
                        'mean_coherence': 0.0,
                        'coherence_sum': 0.0
                    }
                organ_activations[organ]['activation_count'] += 1
                organ_activations[organ]['coherence_sum'] += data.get('coherence', 0.0)

            # Track organ coalitions (active organs per turn)
            active_organs = [
                organ for organ, data in tsk.get('organ_results', {}).items()
                if data.get('coherence', 0.0) > 0.1
            ]
            if active_organs:
                organ_coalitions.append(sorted(active_organs))

        # Compute mean coherence
        for organ in organ_activations:
            count = organ_activations[organ]['activation_count']
            if count > 0:
                organ_activations[organ]['mean_coherence'] = (
                    organ_activations[organ]['coherence_sum'] / count
                )

        # Find most common coalitions
        coalition_counts = {}
        for coalition in organ_coalitions:
            key = '+'.join(coalition)
            coalition_counts[key] = coalition_counts.get(key, 0) + 1

        # Sort by frequency
        top_coalitions = sorted(
            coalition_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        distribution = {
            'epoch': epoch,
            'timestamp': datetime.now().isoformat(),
            'organ_activations': organ_activations,
            'total_turns': len(tsks),
            'top_coalitions': [
                {'coalition': c[0], 'count': c[1], 'frequency': c[1]/len(tsks)}
                for c in top_coalitions
            ]
        }

        dist_file = self.organ_dir / f"epoch{epoch:02d}_organ_distribution.json"
        with open(dist_file, 'w') as f:
            json.dump(distribution, f, indent=2)

    def save_epoch_metrics(self, epoch: int, epoch_results: Dict[str, Any],
                          pattern_db: Dict[str, Any], training_corpus: List[Dict[str, Any]]):
        """
        Save comprehensive intelligence metrics for epoch.

        Uses OrganicIntelligenceEvaluator to compute:
        - Pattern learning metrics
        - Human fluency metrics
        - Generalization metrics
        - Learning signal scaffolding
        - Composite intelligence score
        """
        metrics = self.evaluator.evaluate_epoch(
            epoch=epoch,
            pattern_database=pattern_db,
            epoch_results=epoch_results,
            training_corpus=training_corpus,
            novel_test_set=None  # TODO: Add novel test set
        )

        # Save metrics
        metrics_file = self.metrics_dir / f"epoch{epoch:02d}_metrics.json"
        with open(metrics_file, 'w') as f:
            json.dump(metrics.to_dict(), f, indent=2)

        return metrics

    def generate_final_report(self):
        """
        Generate comprehensive final report across all epochs.

        Includes:
        - Training trajectory visualization
        - Key milestones
        - Family emergence timeline
        - Pattern learning velocity
        - Intelligence score progression
        """
        # Generate progress report from evaluator
        self.evaluator.generate_progress_report(
            str(self.output_dir / "comprehensive_intelligence_report.json")
        )

        # Add training metadata
        metadata_file = self.output_dir / "training_metadata.json"
        self.training_metadata['end_time'] = datetime.now().isoformat()
        self.training_metadata['total_epochs_completed'] = self.current_epoch

        with open(metadata_file, 'w') as f:
            json.dump(self.training_metadata, f, indent=2)

        print(f"\n✅ Final comprehensive report saved to: {self.output_dir}")
        print(f"   - TSK logs: {len(list(self.tsk_dir.glob('*.json')))} turns")
        print(f"   - Family snapshots: {len(list(self.family_dir.glob('*.json')))} epochs")
        print(f"   - Pattern snapshots: {len(list(self.pattern_dir.glob('*.json')))} epochs")
        print(f"   - Metrics: {len(list(self.metrics_dir.glob('*.json')))} epochs")
        print(f"   - Organ distributions: {len(list(self.organ_dir.glob('*.json')))} epochs")

    def _compute_family_statistics(self, families: Dict[str, Any]) -> Dict[str, Any]:
        """Compute statistics about family distribution."""
        if not families:
            return {
                'mean_family_size': 0.0,
                'std_family_size': 0.0,
                'largest_family_size': 0,
                'smallest_family_size': 0
            }

        sizes = [f.get('conversation_count', 0) for f in families.values()]

        return {
            'mean_family_size': np.mean(sizes),
            'std_family_size': np.std(sizes),
            'largest_family_size': max(sizes) if sizes else 0,
            'smallest_family_size': min(sizes) if sizes else 0,
            'median_family_size': np.median(sizes) if sizes else 0
        }

    def _compute_pattern_statistics(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Compute statistics about pattern database."""
        if not patterns:
            return {
                'mean_phrases_per_pattern': 0.0,
                'mean_phrase_quality': 0.0,
                'std_phrase_quality': 0.0,
                'high_quality_phrase_count': 0
            }

        # Gather all phrases
        all_phrases = []
        for pattern in patterns.values():
            for phrase_data in pattern.get('phrases', {}).values():
                all_phrases.append(phrase_data)

        if not all_phrases:
            return {
                'mean_phrases_per_pattern': 0.0,
                'mean_phrase_quality': 0.0,
                'std_phrase_quality': 0.0,
                'high_quality_phrase_count': 0
            }

        qualities = [p.get('quality', 0.0) for p in all_phrases]

        return {
            'mean_phrases_per_pattern': len(all_phrases) / len(patterns) if patterns else 0.0,
            'mean_phrase_quality': np.mean(qualities),
            'std_phrase_quality': np.std(qualities),
            'high_quality_phrase_count': sum(1 for q in qualities if q > 0.6),
            'high_quality_rate': sum(1 for q in qualities if q > 0.6) / len(qualities) if qualities else 0.0
        }


def run_comprehensive_training(
    epochs: int,
    turns_per_conversation: int,
    output_dir: str
):
    """
    Run comprehensive organic training with full memory scaffolding.

    Args:
        epochs: Number of training epochs
        turns_per_conversation: Turns per conversation (3-5 recommended)
        output_dir: Output directory for all training data
    """
    print("=" * 80)
    print("🌀 COMPREHENSIVE ORGANIC INTELLIGENCE TRAINING")
    print("   Complete Memory Scaffolding: TSK + Families + Patterns + Metrics")
    print(f"   Epochs: {epochs}")
    print(f"   Turns per conversation: {turns_per_conversation}")
    print(f"   Output directory: {output_dir}")
    print("=" * 80)
    print()

    # Initialize scaffold
    scaffold = ComprehensiveTrainingScaffold(output_dir)
    scaffold.training_metadata['total_epochs'] = epochs
    scaffold.training_metadata['turns_per_conversation'] = turns_per_conversation

    # Load training corpus
    crisis_pairs_file = "knowledge_base/crisis_urgency_training_pairs.json"
    shadow_pairs_file = "knowledge_base/shadow_exile_training_pairs.json"

    with open(crisis_pairs_file) as f:
        crisis_data = json.load(f)
        crisis_pairs = crisis_data.get('training_pairs', [])

    with open(shadow_pairs_file) as f:
        shadow_data = json.load(f)
        shadow_pairs = shadow_data.get('training_pairs', [])

    all_pairs = crisis_pairs + shadow_pairs
    print(f"📚 Loading training corpus...")
    print(f"   ✅ Loaded {len(all_pairs)} training pairs")
    print(f"      • Crisis/Urgency: {len(crisis_pairs)} pairs")
    print(f"      • Shadow/Exile: {len(shadow_pairs)} pairs")
    print()

    # Initialize organism
    print("🌀 Initializing organism...")
    organism = ConversationalOrganismWrapper()
    print()

    # Import turn-by-turn expansion function
    from training.turn_by_turn_pattern_learning import expand_pair_to_multi_turn_conversation

    # Run training epochs
    for epoch in range(1, epochs + 1):
        scaffold.current_epoch = epoch

        print("=" * 80)
        print(f"🌀 EPOCH {epoch}/{epochs} - Comprehensive Training")
        print("=" * 80)
        print()

        # Collect TSKs for this epoch
        epoch_tsks = []

        # Track metrics
        epoch_stats = {
            'epoch': epoch,
            'organic_emissions': 0,
            'llm_emissions': 0,
            'hebbian_emissions': 0,
            'other_emissions': 0,
            'processed_turns': 0,
            'learning_updates': 0,
            'satisfaction_scores': []
        }

        # Process each pair
        for pair_idx, pair in enumerate(all_pairs, 1):
            pair_id = pair.get('pair_id', f'pair_{pair_idx}')

            # Expand to multi-turn
            conversation_turns = expand_pair_to_multi_turn_conversation(
                pair, num_turns=turns_per_conversation
            )

            # Process turn-by-turn
            for turn_data in conversation_turns:
                turn_num = turn_data['turn']
                user_input = turn_data['input']
                expected_satisfaction = turn_data['expected_satisfaction']

                # Process through organism
                result = organism.process_text(
                    text=user_input,
                    context={'turn_number': turn_num, 'pair_id': pair_id},
                    enable_phase2=False,
                    user_satisfaction=expected_satisfaction
                )

                # Save TSK
                scaffold.save_tsk_snapshot(epoch, turn_num, result, pair_id)
                epoch_tsks.append(result)

                # Track metrics
                epoch_stats['processed_turns'] += 1
                epoch_stats['satisfaction_scores'].append(expected_satisfaction)

                emission_strategy = result.get('emission_strategy', 'unknown')
                if emission_strategy == 'nexus_phrase_learned':
                    epoch_stats['organic_emissions'] += 1
                elif emission_strategy == 'felt_guided_llm':
                    epoch_stats['llm_emissions'] += 1
                elif emission_strategy == 'hebbian':
                    epoch_stats['hebbian_emissions'] += 1
                else:
                    epoch_stats['other_emissions'] += 1

                if result.get('learning_update_occurred', False):
                    epoch_stats['learning_updates'] += 1

        # End-of-epoch data capture
        family_file = "persona_layer/organic_families.json"
        pattern_file = "persona_layer/nexus_phrase_patterns.json"

        # Save family snapshot
        scaffold.save_family_snapshot(epoch, family_file)

        # Save pattern snapshot
        scaffold.save_pattern_snapshot(epoch, pattern_file)

        # Save organ distribution
        scaffold.save_organ_distribution(epoch, epoch_tsks)

        # Load pattern database for metrics
        if os.path.exists(pattern_file):
            with open(pattern_file) as f:
                pattern_db = json.load(f)
        else:
            pattern_db = {'patterns': {}}

        # Save comprehensive metrics
        metrics = scaffold.save_epoch_metrics(epoch, epoch_stats, pattern_db, all_pairs)

        # Print epoch summary
        print()
        print("=" * 80)
        print(f"📊 EPOCH {epoch} SUMMARY")
        print("=" * 80)
        print()
        print(f"✅ Processed: {epoch_stats['processed_turns']} turns")
        print()

        total_emissions = (epoch_stats['organic_emissions'] + epoch_stats['llm_emissions'] +
                          epoch_stats['hebbian_emissions'] + epoch_stats['other_emissions'])
        organic_rate = epoch_stats['organic_emissions'] / total_emissions * 100 if total_emissions > 0 else 0.0

        print(f"🌱 Organic Emission Evolution:")
        print(f"   Organic (pattern learner): {epoch_stats['organic_emissions']} ({organic_rate:.1f}%)")
        print(f"   LLM: {epoch_stats['llm_emissions']}")
        print(f"   Hebbian: {epoch_stats['hebbian_emissions']}")
        print(f"   Other: {epoch_stats['other_emissions']}")
        print()

        print(f"📚 Pattern Learning:")
        print(f"   Database size: {metrics.pattern_learning.total_phrases} phrases")
        print(f"   Mean quality: {metrics.pattern_learning.mean_phrase_quality:.3f}")
        print(f"   High quality (>0.6): {metrics.pattern_learning.high_quality_phrase_count} ({metrics.pattern_learning.high_quality_rate:.1%})")
        print(f"   Learning updates: {epoch_stats['learning_updates']}")
        print()

        print(f"🎯 Intelligence Metrics:")
        print(f"   Intelligence Score: {metrics.intelligence_emergence_score:.1f}/100")
        print(f"   Maturity Level: {metrics.maturity_level}")
        print(f"   Satisfaction: {metrics.human_fluency.mean_satisfaction:.3f} ± {np.sqrt(metrics.human_fluency.satisfaction_variance):.3f}")
        print()

        print(f"📁 Data Captured:")
        print(f"   TSK logs: {len(epoch_tsks)} turns")
        print(f"   Families: {metrics.generalization.family_count}")
        print(f"   Patterns: {metrics.pattern_learning.total_patterns}")
        print()

    # Generate final comprehensive report
    print("=" * 80)
    print("🌀 TRAINING COMPLETE - Generating Final Report")
    print("=" * 80)
    print()

    scaffold.generate_final_report()

    print()
    print("✅ Comprehensive organic training complete!")
    print(f"   All data saved to: {output_dir}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comprehensive Organic Intelligence Training")
    parser.add_argument('--epochs', type=int, default=10, help="Number of training epochs")
    parser.add_argument('--turns-per-conversation', type=int, default=3, help="Turns per conversation")
    parser.add_argument('--output-dir', type=str,
                       default=f"results/comprehensive_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                       help="Output directory for training data")

    args = parser.parse_args()

    run_comprehensive_training(
        epochs=args.epochs,
        turns_per_conversation=args.turns_per_conversation,
        output_dir=args.output_dir
    )
