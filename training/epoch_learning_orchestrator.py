#!/usr/bin/env python3
"""
Epoch Learning Orchestrator - Complete Fractal Learning with Signal Health Monitoring
=====================================================================================

Orchestrates multi-epoch training with:
1. 65D Euclidean distance family emergence
2. Signal health monitoring (FFITTSS-inspired)
3. Organ confidence differentiation tracking
4. Zipf's law validation
5. All 7 fractal reward levels active

Date: November 16, 2025
Status: Production Ready - Multi-Family Emergence Working
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
import numpy as np
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.phase5_learning_integration import Phase5LearningIntegration
from persona_layer.organ_confidence_tracker import OrganConfidenceTracker
from training.signal_health_monitor import SignalHealthMonitor


class EpochLearningOrchestrator:
    """
    Orchestrates epoch-based training with complete fractal learning architecture.

    Features:
    - Multi-family emergence via 65D Euclidean distance
    - Signal health monitoring (FAO agreement, multiplicity, etc.)
    - Organ confidence differentiation
    - Zipf's law validation
    - Per-epoch statistics and reporting
    """

    def __init__(
        self,
        num_epochs: int = 10,
        conversations_per_epoch: int = 30,
        reset_families: bool = False,
        reset_organ_confidence: bool = False,
        save_results: bool = True,
        results_dir: str = "results/epoch_training"
    ):
        self.num_epochs = num_epochs
        self.conversations_per_epoch = conversations_per_epoch
        self.reset_families = reset_families
        self.reset_organ_confidence = reset_organ_confidence
        self.save_results = save_results
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self._initialize_system()

        # Track metrics across epochs
        self.epoch_metrics = []
        self.family_emergence_history = []
        self.organ_confidence_history = []
        self.signal_health_history = []

    def _initialize_system(self):
        """Initialize all learning components."""
        print("=" * 80)
        print("🌀 EPOCH LEARNING ORCHESTRATOR")
        print("=" * 80)

        # Reset families if requested
        if self.reset_families:
            print("🔄 Resetting families for clean baseline...")
            families_path = Path("persona_layer/organic_families.json")
            with open(families_path, 'w') as f:
                json.dump({
                    "families": {},
                    "metadata": {
                        "version": "65D_euclidean",
                        "created": datetime.now().isoformat(),
                        "reset_reason": "epoch_training_orchestrator"
                    }
                }, f, indent=2)

        # Reset organ confidence if requested
        if self.reset_organ_confidence:
            print("🔄 Resetting organ confidence to neutral (0.5)...")
            confidence_path = Path("persona_layer/organ_confidence.json")
            neutral_confidence = {
                organ: 0.5 for organ in [
                    'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                    'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'
                ]
            }
            with open(confidence_path, 'w') as f:
                json.dump(neutral_confidence, f, indent=2)

        # Initialize organism
        print("\n📊 Initializing Conversational Organism...")
        self.organism = ConversationalOrganismWrapper()

        # Initialize Phase 5 learning
        print("📊 Initializing Phase 5 Learning (65D Euclidean)...")
        self.phase5_learner = Phase5LearningIntegration(
            storage_path="persona_layer",
            learning_threshold=0.30,
            enable_learning=True
        )

        # Initialize organ confidence tracker
        print("📊 Initializing Organ Confidence Tracker...")
        self.organ_tracker = OrganConfidenceTracker(
            storage_path="persona_layer/organ_confidence.json"
        )

        # Initialize signal health monitor
        print("📊 Initializing Signal Health Monitor...")
        self.signal_monitor = SignalHealthMonitor()

        # Load training data
        print("📊 Loading training corpus...")
        self._load_training_data()

        print(f"\n✅ System initialized:")
        print(f"   Epochs: {self.num_epochs}")
        print(f"   Conversations/epoch: {self.conversations_per_epoch}")
        print(f"   Initial families: {len(self.phase5_learner.families.families)}")
        # Get organ confidences from organ_metrics (correct API)
        initial_confidences = [m.confidence for m in self.organ_tracker.organ_metrics.values()]
        print(f"   Initial organ confidence std: {np.std(initial_confidences) if initial_confidences else 0.0:.4f}")

    def _load_training_data(self):
        """Load diverse training corpus."""
        training_path = Path("knowledge_base/conversational_training_pairs.json")

        if training_path.exists():
            with open(training_path, 'r') as f:
                data = json.load(f)
            self.training_pairs = data.get('training_pairs', [])
            print(f"   Loaded {len(self.training_pairs)} training pairs")
        else:
            # Generate synthetic diverse training data
            print("   Generating synthetic training corpus...")
            self.training_pairs = self._generate_diverse_training_data()

    def _get_organ_confidences(self) -> Dict[str, float]:
        """Extract organ confidence values from tracker (correct API)."""
        if not self.organ_tracker.organ_metrics:
            # Return default if no metrics yet
            return {
                organ: 0.5 for organ in [
                    'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                    'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'
                ]
            }
        return {
            organ: metrics.confidence
            for organ, metrics in self.organ_tracker.organ_metrics.items()
        }

    def _generate_diverse_training_data(self) -> List[Dict]:
        """Generate diverse training data covering different felt-states."""

        # Categories with distinct polyvagal/urgency patterns
        categories = {
            'crisis': [
                "I'm having a panic attack and can't breathe",
                "Everything is falling apart right now",
                "I don't know if I can keep going",
                "The anxiety is overwhelming me",
                "I feel like I'm losing control"
            ],
            'safety': [
                "I feel really calm and grounded today",
                "There's a sense of peace in my body",
                "I feel safe enough to explore this",
                "My nervous system feels settled",
                "I'm noticing spaciousness inside"
            ],
            'ambivalence': [
                "Part of me wants to leave but another part is scared",
                "I feel torn between two choices",
                "There's conflict inside me about this",
                "I'm pulled in different directions",
                "Part of me knows and part of me doubts"
            ],
            'collapse': [
                "I can't feel anything anymore, just numb",
                "Everything feels distant and foggy",
                "I've shut down completely",
                "There's no energy left in me",
                "I'm just going through the motions"
            ],
            'activation': [
                "I'm feeling really angry about what happened",
                "My body is buzzing with energy",
                "I need to do something but don't know what",
                "There's tension building inside me",
                "I feel restless and on edge"
            ],
            'relational': [
                "I feel connected to you right now",
                "It's hard to trust people after what I've been through",
                "I'm noticing how I relate to others",
                "There's something about this relationship that feels different",
                "I want to be seen but I'm afraid"
            ]
        }

        pairs = []
        for category, messages in categories.items():
            for msg in messages:
                pairs.append({
                    'user_input': msg,
                    'category': category,
                    'expected_polyvagal': self._get_expected_polyvagal(category),
                    'expected_urgency': self._get_expected_urgency(category)
                })

        return pairs

    def _get_expected_polyvagal(self, category: str) -> str:
        """Get expected polyvagal state for category."""
        mapping = {
            'crisis': 'sympathetic',
            'safety': 'ventral',
            'ambivalence': 'mixed_state',
            'collapse': 'dorsal',
            'activation': 'sympathetic',
            'relational': 'ventral'
        }
        return mapping.get(category, 'mixed_state')

    def _get_expected_urgency(self, category: str) -> float:
        """Get expected urgency for category."""
        mapping = {
            'crisis': 0.85,
            'safety': 0.1,
            'ambivalence': 0.45,
            'collapse': 0.2,
            'activation': 0.7,
            'relational': 0.3
        }
        return mapping.get(category, 0.5)

    def run_epoch(self, epoch_num: int) -> Dict:
        """Run a single training epoch."""
        print(f"\n{'=' * 80}")
        print(f"🌀 EPOCH {epoch_num}/{self.num_epochs}")
        print(f"{'=' * 80}")

        epoch_start_time = time.time()

        # Select training samples for this epoch
        epoch_samples = self._select_epoch_samples()

        # Track epoch metrics
        epoch_results = {
            'epoch': epoch_num,
            'start_time': datetime.now().isoformat(),
            'conversations': [],
            'family_assignments': [],
            'new_families_created': 0,
            'satisfactions': [],
            'distances': []
        }

        # Initial state
        initial_families = len(self.phase5_learner.families.families)
        initial_organ_confidence = self._get_organ_confidences()

        print(f"\n📊 Processing {len(epoch_samples)} conversations...")

        for i, sample in enumerate(epoch_samples, 1):
            # Process conversation
            result = self._process_conversation(sample, epoch_num, i)
            epoch_results['conversations'].append(result)

            if result.get('learned'):
                epoch_results['family_assignments'].append(result['family_id'])
                epoch_results['satisfactions'].append(result['satisfaction'])
                if result.get('is_new_family'):
                    epoch_results['new_families_created'] += 1
                if result.get('distance'):
                    epoch_results['distances'].append(result['distance'])

            # Progress indicator
            if i % 10 == 0:
                print(f"   Processed {i}/{len(epoch_samples)} conversations...")

        # Compute epoch statistics
        epoch_stats = self._compute_epoch_statistics(
            epoch_num, epoch_results, initial_families, initial_organ_confidence
        )

        # Signal health check
        signal_health = self.signal_monitor.compute_epoch_health(
            self.phase5_learner.families.families,
            self._get_organ_confidences()
        )

        epoch_stats['signal_health'] = signal_health
        epoch_stats['duration_seconds'] = time.time() - epoch_start_time

        # Store history
        self.epoch_metrics.append(epoch_stats)
        self.family_emergence_history.append(len(self.phase5_learner.families.families))
        self.organ_confidence_history.append(self._get_organ_confidences())
        self.signal_health_history.append(signal_health)

        # Report
        self._print_epoch_report(epoch_stats)

        return epoch_stats

    def _select_epoch_samples(self) -> List[Dict]:
        """Select diverse samples for epoch."""
        # Cycle through training pairs to ensure diversity
        samples = []
        idx = 0
        for _ in range(self.conversations_per_epoch):
            samples.append(self.training_pairs[idx % len(self.training_pairs)])
            idx += 1
        return samples

    def _process_conversation(self, sample: Dict, epoch: int, conv_num: int) -> Dict:
        """Process a single conversation through the organism."""
        # Support both formats: user_input and input_text
        user_input = sample.get('user_input') or sample.get('input_text', '')

        # Extract metadata if present
        metadata = sample.get('pair_metadata', {})
        category = metadata.get('category', sample.get('category', 'unknown'))

        try:
            # Process through organism
            response = self.organism.process_text(user_input)

            # Extract felt states from wrapper response structure
            # The wrapper returns: felt_states, tsk_record, emission_text, etc.
            felt_states = response.get('felt_states', {})
            tsk_record = response.get('tsk_record')
            emission = response.get('emission_text', '')

            # Build initial_felt_state from defaults (organism starts neutral)
            initial_state = {
                'v0_initial': 1.0,
                'organ_coherences': {
                    'LISTENING': 0.5, 'EMPATHY': 0.5, 'WISDOM': 0.5,
                    'AUTHENTICITY': 0.5, 'PRESENCE': 0.5, 'BOND': 0.5,
                    'SANS': 0.5, 'NDAM': 0.5, 'RNX': 0.5, 'EO': 0.5, 'CARD': 0.5
                },
                'polyvagal_state': 'ventral',
                'zone': 1,
                'satisfaction': 0.5
            }

            # Build final_felt_state from response data
            final_state = {
                'satisfaction_final': felt_states.get('satisfaction_final', 0.5),
                'organ_coherences': felt_states.get('organ_coherences', {}),
                'v0_final': felt_states.get('v0_energy', {}).get('final_energy', 0.3),
                'polyvagal_state': felt_states.get('polyvagal_state', 'ventral'),
                'zone': response.get('zone_id', 1),
                'convergence_cycles': felt_states.get('convergence_cycles', 1)
            }

            # If TSK record available, extract rich transformation data
            if tsk_record and hasattr(tsk_record, 'initial_polyvagal_state'):
                # Use TSK data for richer initial state reconstruction
                initial_state['polyvagal_state'] = tsk_record.initial_polyvagal_state or 'ventral'
                initial_state['zone'] = tsk_record.initial_zone or 1
                initial_state['organ_coherences'] = tsk_record.initial_organ_coherences or initial_state['organ_coherences']

                # Final state from TSK
                final_state['polyvagal_state'] = tsk_record.final_polyvagal_state or final_state['polyvagal_state']
                final_state['zone'] = tsk_record.final_zone or final_state['zone']
                final_state['organ_coherences'] = tsk_record.final_organ_coherences or final_state['organ_coherences']

                # Add urgency if available
                if hasattr(tsk_record, 'initial_urgency'):
                    initial_state['urgency'] = tsk_record.initial_urgency
                    final_state['urgency'] = tsk_record.final_urgency

            # Learn from transformation
            learning_report = self.phase5_learner.learn_from_conversation_transformation(
                initial_felt_state=initial_state,
                final_felt_state=final_state,
                emission_text=emission,
                user_message=user_input,
                conversation_id=f"epoch{epoch}_conv{conv_num}",
                transduction_trajectory=response.get('transduction_trajectory', []),
                constraint_deltas=response.get('constraint_deltas', {})
            )

            # Update organ confidence (Level 2 fractal rewards)
            if learning_report and felt_states.get('organ_coherences'):
                # Build organ_results format expected by tracker
                organ_results = {
                    organ: {'coherence': coherence}
                    for organ, coherence in final_state.get('organ_coherences', {}).items()
                }
                emission_conf = felt_states.get('satisfaction_final', 0.5)
                self.organ_tracker.update(organ_results, emission_conf)

            return {
                'learned': learning_report is not None,
                'family_id': learning_report.get('family_id') if learning_report else None,
                'is_new_family': learning_report.get('is_new_family', False) if learning_report else False,
                'satisfaction': final_state.get('satisfaction_final', 0.5),
                'distance': learning_report.get('similarity_score', 0) if learning_report else None,
                'category': category,
                'polyvagal': final_state.get('polyvagal_state', 'unknown')
            }

        except Exception as e:
            print(f"   ⚠️ Error processing conversation: {e}")
            import traceback
            traceback.print_exc()
            return {'learned': False, 'error': str(e)}

    def _compute_epoch_statistics(
        self,
        epoch_num: int,
        epoch_results: Dict,
        initial_families: int,
        initial_organ_confidence: Dict
    ) -> Dict:
        """Compute comprehensive epoch statistics."""

        final_families = len(self.phase5_learner.families.families)
        family_sizes = [f.member_count for f in self.phase5_learner.families.families.values()]

        # Organ confidence differentiation
        final_organ_confidence = self._get_organ_confidences()
        organ_confidence_changes = {
            organ: final_organ_confidence.get(organ, 0.5) - initial_organ_confidence.get(organ, 0.5)
            for organ in initial_organ_confidence
        }

        # Zipf's law fit (if enough families)
        zipf_alpha, zipf_r_squared = 0.0, 0.0
        if len(family_sizes) >= 3:
            zipf_alpha, zipf_r_squared = self._fit_zipf_law(sorted(family_sizes, reverse=True))

        return {
            'epoch': epoch_num,
            'conversations_processed': len(epoch_results['conversations']),
            'conversations_learned': sum(1 for c in epoch_results['conversations'] if c.get('learned')),

            # Family metrics
            'initial_families': initial_families,
            'final_families': final_families,
            'new_families_created': epoch_results['new_families_created'],
            'family_sizes': family_sizes,
            'family_size_std': np.std(family_sizes) if family_sizes else 0,

            # Satisfaction metrics
            'mean_satisfaction': np.mean(epoch_results['satisfactions']) if epoch_results['satisfactions'] else 0,
            'satisfaction_std': np.std(epoch_results['satisfactions']) if epoch_results['satisfactions'] else 0,

            # Organ confidence
            'organ_confidence_final': final_organ_confidence,
            'organ_confidence_std': np.std(list(final_organ_confidence.values())),
            'organ_confidence_changes': organ_confidence_changes,
            'max_organ_change': max(organ_confidence_changes.values()) if organ_confidence_changes else 0,
            'min_organ_change': min(organ_confidence_changes.values()) if organ_confidence_changes else 0,

            # Zipf's law
            'zipf_alpha': zipf_alpha,
            'zipf_r_squared': zipf_r_squared,

            # Distance metrics (for family separation quality)
            'mean_distance': np.mean(epoch_results['distances']) if epoch_results['distances'] else 0,
            'distance_std': np.std(epoch_results['distances']) if epoch_results['distances'] else 0
        }

    def _fit_zipf_law(self, family_sizes: List[int]) -> tuple:
        """Fit Zipf's law to family size distribution."""
        if len(family_sizes) < 3:
            return 0.0, 0.0

        ranks = np.arange(1, len(family_sizes) + 1)
        sizes = np.array(family_sizes)

        # Fit power law: size = C / rank^alpha
        # log(size) = log(C) - alpha * log(rank)
        log_ranks = np.log(ranks)
        log_sizes = np.log(sizes + 1e-6)  # Avoid log(0)

        # Linear regression
        slope, intercept = np.polyfit(log_ranks, log_sizes, 1)
        alpha = -slope

        # R-squared
        predicted_log_sizes = intercept + slope * log_ranks
        ss_res = np.sum((log_sizes - predicted_log_sizes) ** 2)
        ss_tot = np.sum((log_sizes - np.mean(log_sizes)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        return alpha, r_squared

    def _print_epoch_report(self, stats: Dict):
        """Print formatted epoch report."""
        print(f"\n📈 EPOCH {stats['epoch']} RESULTS")
        print("-" * 60)

        # Family emergence
        print(f"📁 Families: {stats['initial_families']} → {stats['final_families']} (+{stats['new_families_created']})")
        if stats['family_sizes']:
            print(f"   Distribution: {sorted(stats['family_sizes'], reverse=True)[:10]}...")
        print(f"   Zipf α: {stats['zipf_alpha']:.3f} (target: ~0.7)")
        print(f"   Zipf R²: {stats['zipf_r_squared']:.3f} (target: >0.85)")

        # Satisfaction
        print(f"\n😊 Satisfaction: {stats['mean_satisfaction']:.4f} ± {stats['satisfaction_std']:.4f}")

        # Organ differentiation
        print(f"\n🧬 Organ Confidence:")
        print(f"   Std: {stats['organ_confidence_std']:.4f} (target: >0.15)")
        print(f"   Max change: {stats['max_organ_change']:+.4f}")
        print(f"   Min change: {stats['min_organ_change']:+.4f}")

        # Signal health
        health = stats.get('signal_health', {})
        print(f"\n📊 Signal Health:")
        print(f"   Mean Agreement: {health.get('mean_pairwise_agreement', 0):.4f}")
        print(f"   Mean Multiplicity: {health.get('mean_multiplicity_index', 0):.4f}")
        print(f"   Health Score: {health.get('overall_health_score', 0):.4f}")

        # Duration
        print(f"\n⏱️ Duration: {stats.get('duration_seconds', 0):.2f}s")

    def run_training(self) -> Dict:
        """Run complete multi-epoch training."""
        print("\n" + "=" * 80)
        print("🚀 STARTING MULTI-EPOCH TRAINING")
        print("=" * 80)

        training_start = time.time()

        for epoch in range(1, self.num_epochs + 1):
            self.run_epoch(epoch)

        # Final summary
        total_duration = time.time() - training_start
        final_report = self._generate_final_report(total_duration)

        # Save results
        if self.save_results:
            self._save_results(final_report)

        return final_report

    def _generate_final_report(self, total_duration: float) -> Dict:
        """Generate comprehensive final training report."""
        print("\n" + "=" * 80)
        print("📊 FINAL TRAINING REPORT")
        print("=" * 80)

        final_families = len(self.phase5_learner.families.families)
        final_organ_conf = self._get_organ_confidences()
        final_organ_std = np.std(list(final_organ_conf.values())) if final_organ_conf else 0.0

        report = {
            'training_summary': {
                'num_epochs': self.num_epochs,
                'total_conversations': self.num_epochs * self.conversations_per_epoch,
                'total_duration_seconds': total_duration,
                'final_families': final_families,
                'final_organ_confidence_std': final_organ_std
            },
            'family_emergence': {
                'history': self.family_emergence_history,
                'growth_rate': (final_families - self.family_emergence_history[0]) / self.num_epochs if self.num_epochs > 0 else 0
            },
            'organ_differentiation': {
                'final_confidences': final_organ_conf,
                'std_evolution': [np.std(list(h.values())) for h in self.organ_confidence_history]
            },
            'signal_health': {
                'final': self.signal_health_history[-1] if self.signal_health_history else {},
                'history': self.signal_health_history
            },
            'epoch_metrics': self.epoch_metrics,
            'zipf_validation': {
                'final_alpha': self.epoch_metrics[-1]['zipf_alpha'] if self.epoch_metrics else 0,
                'final_r_squared': self.epoch_metrics[-1]['zipf_r_squared'] if self.epoch_metrics else 0,
                'zipf_law_emerged': self.epoch_metrics[-1]['zipf_r_squared'] > 0.85 if self.epoch_metrics else False
            }
        }

        # Print summary
        print(f"\n🎯 TRAINING COMPLETE")
        print(f"   Epochs: {self.num_epochs}")
        print(f"   Total conversations: {report['training_summary']['total_conversations']}")
        print(f"   Duration: {total_duration:.2f}s")

        print(f"\n📁 Family Emergence:")
        print(f"   Final families: {final_families}")
        print(f"   Growth rate: {report['family_emergence']['growth_rate']:.2f} families/epoch")

        print(f"\n🧬 Organ Differentiation:")
        print(f"   Final std: {final_organ_std:.4f}")
        for organ, conf in sorted(final_organ_conf.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {organ}: {conf:.4f}")

        print(f"\n📈 Zipf's Law:")
        print(f"   α = {report['zipf_validation']['final_alpha']:.3f}")
        print(f"   R² = {report['zipf_validation']['final_r_squared']:.3f}")
        if report['zipf_validation']['zipf_law_emerged']:
            print(f"   ✅ Natural emergence achieved!")
        else:
            print(f"   ⏳ More epochs needed (target: R² > 0.85)")

        return report

    def _save_results(self, report: Dict):
        """Save training results to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"epoch_training_{timestamp}.json"
        filepath = self.results_dir / filename

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Epoch Learning Orchestrator")
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs')
    parser.add_argument('--conversations', type=int, default=30, help='Conversations per epoch')
    parser.add_argument('--reset', action='store_true', help='Reset families and organ confidence')
    parser.add_argument('--no-save', action='store_true', help='Do not save results')

    args = parser.parse_args()

    orchestrator = EpochLearningOrchestrator(
        num_epochs=args.epochs,
        conversations_per_epoch=args.conversations,
        reset_families=args.reset,
        reset_organ_confidence=args.reset,
        save_results=not args.no_save
    )

    orchestrator.run_training()


if __name__ == "__main__":
    main()
