#!/usr/bin/env python3
"""
CORE-Grounded Training - Train organism with IFS + Polyvagal + Trauma-Informed foundation
=========================================================================================

Uses the CORE-grounded training corpus (from BOOKS_FOUNDATION_PROTOCOLS.md) to train
the organism for natural family emergence with proper 65D signature discrimination.

Key Features:
1. Polyvagal-state diverse training (ventral, sympathetic, dorsal)
2. IFS parts detection (managers, firefighters, exiles)
3. Tone modulation per arousal state
4. Natural family clustering via 65D Euclidean distance

Date: November 16, 2025
Status: Production Ready - CORE Foundation Active
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path
import numpy as np
from typing import Dict, List
from scipy import stats  # For Zipf's law computation
from scipy.spatial.distance import euclidean  # For inter-family distances

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.phase5_learning_integration import Phase5LearningIntegration
from persona_layer.organ_confidence_tracker import OrganConfidenceTracker
from persona_layer.family_v0_learner import FamilyV0Learner
from persona_layer.conversational_hebbian_memory import ConversationalHebbianMemory, ConversationalOutcome
from training.signal_health_monitor import SignalHealthMonitor


class COREGroundedTrainer:
    """
    Trains the organism with CORE protocols (IFS + Polyvagal + Trauma-Informed).

    Philosophy: Natural family emergence without discrimination, grounded in
    trauma-informed IFS principles from BOOKS_FOUNDATION_PROTOCOLS.md.
    """

    def __init__(
        self,
        num_epochs: int = 10,
        reset_families: bool = True,
        reset_organ_confidence: bool = True,
        save_results: bool = True,
        results_dir: str = "results/core_grounded_training"
    ):
        self.num_epochs = num_epochs
        self.reset_families = reset_families
        self.reset_organ_confidence = reset_organ_confidence
        self.save_results = save_results
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Track metrics
        self.epoch_metrics = []
        self.family_evolution = []
        self.organ_evolution = []

        # Initialize system
        self._initialize_system()

    def _initialize_system(self):
        """Initialize all training components."""
        print("=" * 80)
        print("🌀 CORE-GROUNDED TRAINING")
        print("   Foundation: BOOKS_FOUNDATION_PROTOCOLS.md")
        print("   Principles: IFS + Polyvagal + Trauma-Informed + Whiteheadian")
        print("=" * 80)

        # Reset families for clean baseline
        if self.reset_families:
            print("\n🔄 Resetting families for CORE baseline...")
            families_path = Path("persona_layer/organic_families.json")
            families_path.parent.mkdir(parents=True, exist_ok=True)
            with open(families_path, 'w') as f:
                json.dump({
                    "families": {},
                    "conversation_to_family": {},
                    "next_family_id": 1,
                    "last_updated": datetime.now().isoformat(),
                    "total_families": 0,
                    "mature_families": 0,
                    "total_conversations": 0
                }, f, indent=2)

        # Reset organ confidence
        if self.reset_organ_confidence:
            print("🔄 Resetting organ confidence to neutral (0.5)...")
            # Use state/active path to match wrapper's internal tracker
            confidence_path = Path("persona_layer/state/active/organ_confidence.json")
            confidence_path.parent.mkdir(parents=True, exist_ok=True)
            neutral = {
                organ: 0.5 for organ in [
                    'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                    'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD', 'NEXUS'  # Include NEXUS
                ]
            }
            with open(confidence_path, 'w') as f:
                json.dump(neutral, f, indent=2)
            # Also update the old path for backwards compatibility
            old_confidence_path = Path("persona_layer/organ_confidence.json")
            old_confidence_path.parent.mkdir(parents=True, exist_ok=True)
            with open(old_confidence_path, 'w') as f:
                json.dump(neutral, f, indent=2)

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

        # Initialize organ confidence tracker (use state/active path to match wrapper)
        print("📊 Initializing Organ Confidence Tracker...")
        self.organ_tracker = OrganConfidenceTracker(
            storage_path="persona_layer/state/active/organ_confidence.json"
        )

        # Initialize signal health monitor
        print("📊 Initializing Signal Health Monitor...")
        self.signal_monitor = SignalHealthMonitor()
        self.signal_health_history = []

        # Initialize Family V0 Learner (DAE 3.0 Level 4)
        print("📊 Initializing Family V0 Learner...")
        self.family_v0_learner = FamilyV0Learner(
            families_path=Path("persona_layer/organic_families.json")
        )

        # Initialize Hebbian R-Matrix Learning (DAE 3.0 Level 3)
        print("📊 Initializing Hebbian R-Matrix Memory...")
        self.hebbian_memory = ConversationalHebbianMemory(
            storage_path="persona_layer/conversational_hebbian_memory.json"
        )

        # Load CORE corpus
        print("📊 Loading CORE-grounded training corpus...")
        self._load_core_corpus()

        print(f"\n✅ CORE Training System Initialized:")
        print(f"   Epochs: {self.num_epochs}")
        print(f"   Training pairs: {len(self.training_pairs)}")
        print(f"   Categories: {len(set(p['category'] for p in self.training_pairs))}")
        print(f"   Polyvagal states: {set(p.get('polyvagal_state', 'ventral') for p in self.training_pairs)}")

    def _load_core_corpus(self):
        """Load the CORE-grounded training corpus."""
        corpus_path = Path("knowledge_base/core_grounded_training_corpus.json")

        if corpus_path.exists():
            with open(corpus_path, 'r') as f:
                data = json.load(f)
            self.training_pairs = data.get('training_pairs', [])
            self.corpus_metadata = data.get('metadata', {})
            print(f"   ✅ Loaded {len(self.training_pairs)} CORE training pairs")
        else:
            raise FileNotFoundError(f"CORE corpus not found at {corpus_path}")

    def _get_organ_confidences(self) -> Dict[str, float]:
        """Extract current organ confidences."""
        if not self.organ_tracker.organ_metrics:
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

    def train(self):
        """Run CORE-grounded training across all epochs."""
        print(f"\n🚀 Starting CORE-Grounded Training: {self.num_epochs} epochs")
        print("=" * 80)

        start_time = time.time()

        for epoch in range(1, self.num_epochs + 1):
            epoch_result = self._run_epoch(epoch)
            self.epoch_metrics.append(epoch_result)

            # Save checkpoint
            if self.save_results:
                self._save_checkpoint(epoch)

        total_time = time.time() - start_time

        # Final summary
        self._print_final_summary(total_time)

        if self.save_results:
            self._save_final_results()

    def _run_epoch(self, epoch_num: int) -> Dict:
        """Run a single training epoch with CORE corpus."""
        print(f"\n{'='*80}")
        print(f"📊 EPOCH {epoch_num}/{self.num_epochs}")
        print(f"{'='*80}")

        epoch_start = time.time()
        initial_families = len(self.phase5_learner.families.families)
        initial_organ_confidence = self._get_organ_confidences()

        # Track per-category results
        category_results = {}
        all_satisfactions = []
        all_distances = []
        new_families = 0
        families_touched = set()

        # Process each training pair
        for idx, pair in enumerate(self.training_pairs):
            category = pair.get('category', 'unknown')
            subcategory = pair.get('subcategory', 'unknown')
            input_text = pair.get('input_text', '')
            expected_polyvagal = pair.get('polyvagal_state', 'ventral')
            expected_zone = pair.get('zone', 1)
            expected_urgency = pair.get('urgency', 0.0)
            key_organs = pair.get('key_organs', [])

            # Process through organism
            result = self._process_single_conversation(
                input_text, epoch_num, idx + 1, category
            )

            if result.get('learned'):
                # Track family
                family_id = result.get('family_id')
                if family_id:
                    families_touched.add(family_id)
                    if result.get('is_new_family'):
                        new_families += 1

                # Track satisfaction and distance
                all_satisfactions.append(result.get('satisfaction', 0.5))
                if result.get('distance') is not None:
                    all_distances.append(result.get('distance'))

                # Track per-category
                if category not in category_results:
                    category_results[category] = {
                        'count': 0, 'satisfactions': [], 'families': set()
                    }
                category_results[category]['count'] += 1
                category_results[category]['satisfactions'].append(result.get('satisfaction', 0.5))
                if family_id:
                    category_results[category]['families'].add(family_id)

            # Progress indicator
            if (idx + 1) % 10 == 0:
                print(f"   Processed {idx + 1}/{len(self.training_pairs)} pairs...")

        epoch_time = time.time() - epoch_start

        # Compute epoch statistics
        final_families = len(self.phase5_learner.families.families)
        final_organ_confidence = self._get_organ_confidences()

        # Organ confidence changes
        organ_changes = {
            organ: final_organ_confidence.get(organ, 0.5) - initial_organ_confidence.get(organ, 0.5)
            for organ in initial_organ_confidence
        }

        # Family size distribution
        family_sizes = [f.member_count for f in self.phase5_learner.families.families.values()]

        epoch_result = {
            'epoch': epoch_num,
            'conversations_processed': len(self.training_pairs),
            'new_families_created': new_families,
            'total_families': final_families,
            'families_touched': len(families_touched),
            'family_sizes': family_sizes,
            'mean_satisfaction': np.mean(all_satisfactions) if all_satisfactions else 0.0,
            'satisfaction_std': np.std(all_satisfactions) if all_satisfactions else 0.0,
            'mean_distance': np.mean(all_distances) if all_distances else 0.0,
            'distance_std': np.std(all_distances) if all_distances else 0.0,
            'organ_confidence_final': final_organ_confidence,
            'organ_confidence_std': np.std(list(final_organ_confidence.values())),
            'organ_changes': organ_changes,
            'category_results': {
                cat: {
                    'count': data['count'],
                    'mean_satisfaction': np.mean(data['satisfactions']) if data['satisfactions'] else 0.0,
                    'num_families': len(data['families'])
                }
                for cat, data in category_results.items()
            },
            'epoch_time_seconds': epoch_time
        }

        # Compute signal health (FFITTSS-inspired monitoring)
        try:
            signal_health = self.signal_monitor.compute_epoch_health(
                self.phase5_learner.families.families,
                final_organ_confidence
            )
            epoch_result['signal_health'] = signal_health
            self.signal_health_history.append(signal_health)

            # Warn if organ confidence not differentiating
            if signal_health.get('organ_confidence_std', 0.0) < 0.05:
                print(f"   ⚠️  WARNING: Organ confidence std = {signal_health.get('organ_confidence_std', 0.0):.4f} (target > 0.15)")
        except Exception as e:
            print(f"   ⚠️  Signal health computation failed: {e}")

        # Print epoch summary
        self._print_epoch_summary(epoch_result)

        return epoch_result

    def _process_single_conversation(
        self, input_text: str, epoch: int, conv_num: int, category: str
    ) -> Dict:
        """Process a single CORE training conversation."""
        try:
            # Process through organism
            response = self.organism.process_text(input_text)

            # Extract felt states
            felt_states = response.get('felt_states', {})
            tsk_record = response.get('tsk_record')
            emission = response.get('emission_text', '')

            # Build initial state (neutral baseline)
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

            # Build final state from response
            final_state = {
                'satisfaction_final': felt_states.get('satisfaction_final', 0.5),
                'organ_coherences': felt_states.get('organ_coherences', {}),
                'v0_final': felt_states.get('v0_energy', {}).get('final_energy', 0.3),
                'polyvagal_state': felt_states.get('polyvagal_state', 'ventral'),
                'zone': response.get('zone_id', 1),
                'convergence_cycles': felt_states.get('convergence_cycles', 1)
            }

            # Enrich from TSK if available
            if tsk_record and hasattr(tsk_record, 'initial_polyvagal_state'):
                if tsk_record.initial_polyvagal_state:
                    initial_state['polyvagal_state'] = tsk_record.initial_polyvagal_state
                if tsk_record.initial_zone:
                    initial_state['zone'] = tsk_record.initial_zone
                if tsk_record.initial_organ_coherences:
                    initial_state['organ_coherences'] = tsk_record.initial_organ_coherences

                if tsk_record.final_polyvagal_state:
                    final_state['polyvagal_state'] = tsk_record.final_polyvagal_state
                if tsk_record.final_zone:
                    final_state['zone'] = tsk_record.final_zone
                if tsk_record.final_organ_coherences:
                    final_state['organ_coherences'] = tsk_record.final_organ_coherences

                if hasattr(tsk_record, 'initial_urgency'):
                    initial_state['urgency'] = tsk_record.initial_urgency or 0.0
                    final_state['urgency'] = tsk_record.final_urgency or 0.0

            # Learn from transformation
            learning_report = self.phase5_learner.learn_from_conversation_transformation(
                initial_felt_state=initial_state,
                final_felt_state=final_state,
                emission_text=emission,
                user_message=input_text,
                conversation_id=f"core_epoch{epoch}_conv{conv_num}",
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

            # Update Family V0 learning (Level 4 fractal rewards)
            if learning_report and learning_report.get('family_id'):
                try:
                    self.family_v0_learner.update_family_v0(
                        family_id=learning_report['family_id'],
                        v0_final=final_state.get('v0_final', 0.3),
                        satisfaction=final_state.get('satisfaction_final', 0.5),
                        convergence_cycles=final_state.get('convergence_cycles', 3),
                        organ_coherences=final_state.get('organ_coherences', {}),
                        r_matrix_coupling=0.05  # Default coupling
                    )
                except Exception as e:
                    pass  # Silent fail - V0 learning is optional enhancement

            # Update Hebbian R-Matrix (Level 3 fractal rewards)
            try:
                outcome = ConversationalOutcome(
                    polyvagal_state=final_state.get('polyvagal_state', 'ventral'),
                    polyvagal_confidence=0.7,
                    self_energy=0.5,
                    self_energy_confidence=0.7,
                    dominant_c='calm',
                    cs_activation={'calm': 0.8, 'clarity': 0.7, 'compassion': 0.6, 'curiosity': 0.5,
                                   'confidence': 0.5, 'courage': 0.4, 'creativity': 0.4, 'connectedness': 0.5},
                    conversational_family=learning_report.get('family_id', 'default') if learning_report else 'default',
                    satisfaction=final_state.get('satisfaction_final', 0.5),
                    coherence=np.mean(list(final_state.get('organ_coherences', {}).values())) if final_state.get('organ_coherences') else 0.5,
                    ofel_energy=0.3,
                    card_scale='moderate',
                    gate_decision='RESPOND',
                    response_text=emission,
                    response_quality='adequate'
                )
                self.hebbian_memory.update_from_outcome(outcome)
            except Exception as e:
                pass  # Silent fail - Hebbian learning is optional

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
            print(f"   ⚠️ Error processing: {e}")
            import traceback
            traceback.print_exc()
            return {'learned': False, 'error': str(e)}

    def _compute_zipf_metrics(self, family_sizes: List[int]) -> Dict:
        """
        Compute Zipf's law metrics from family size distribution.

        From DAE 3.0 architecture docs:
        - Expected α ≈ 0.7-0.8 for natural emergence
        - R² > 0.85 indicates Zipf's law is holding
        - Lower α = more even distribution
        - Higher α = more skewed (few large families dominate)
        """
        if len(family_sizes) < 2:
            return {'alpha': 0.0, 'r_squared': 0.0, 'valid': False}

        # Sort in descending order (largest family = rank 1)
        sorted_sizes = sorted(family_sizes, reverse=True)

        # Compute ranks (1, 2, 3, ...)
        ranks = np.arange(1, len(sorted_sizes) + 1)

        # Log-log transform for Zipf's law: log(size) = -α * log(rank) + C
        log_ranks = np.log(ranks)
        log_sizes = np.log(np.array(sorted_sizes) + 1e-6)  # Avoid log(0)

        # Linear regression in log-log space
        slope, intercept, r_value, p_value, std_err = stats.linregress(log_ranks, log_sizes)

        # α is the negative of the slope (Zipf: frequency ~ rank^-α)
        alpha = -slope
        r_squared = r_value ** 2

        return {
            'alpha': alpha,
            'r_squared': r_squared,
            'valid': len(family_sizes) >= 3,
            'interpretation': self._interpret_zipf(alpha, r_squared, len(family_sizes))
        }

    def _interpret_zipf(self, alpha: float, r_squared: float, num_families: int) -> str:
        """Interpret Zipf's law metrics for learning progress."""
        if num_families < 5:
            return "exploration_phase"  # Not enough families to assess

        if r_squared < 0.7:
            return "non_zipfian"  # Distribution doesn't follow Zipf's law

        if alpha < 0.5:
            return "too_flat"  # Families too evenly distributed
        elif alpha > 1.2:
            return "too_concentrated"  # Too few families dominating
        else:
            return "healthy_emergence"  # Natural emergence (α ≈ 0.7-0.8)

    def _compute_inter_family_distances(self) -> Dict:
        """
        Compute pairwise Euclidean distances between family centroids.

        From Euclidean distance docs:
        - Target: Inter-family distance > 1.5 (good separation)
        - Warning: < 1.0 (families too similar)
        - Critical: < 0.5 (families collapsing)
        """
        families = self.phase5_learner.families.families

        if len(families) < 2:
            return {'mean_distance': 0.0, 'min_distance': 0.0, 'max_distance': 0.0, 'pairs': []}

        family_ids = list(families.keys())
        centroids = {fid: np.array(fam.centroid) for fid, fam in families.items()}

        distances = []
        pairs = []

        # Compute all pairwise distances
        for i in range(len(family_ids)):
            for j in range(i + 1, len(family_ids)):
                fid_i, fid_j = family_ids[i], family_ids[j]
                dist = euclidean(centroids[fid_i], centroids[fid_j])
                distances.append(dist)
                pairs.append({
                    'family_i': fid_i,
                    'family_j': fid_j,
                    'distance': dist
                })

        if not distances:
            return {'mean_distance': 0.0, 'min_distance': 0.0, 'max_distance': 0.0, 'pairs': []}

        return {
            'mean_distance': np.mean(distances),
            'min_distance': np.min(distances),
            'max_distance': np.max(distances),
            'std_distance': np.std(distances),
            'pairs': sorted(pairs, key=lambda x: x['distance'])  # Sorted by distance
        }

    def _print_signal_health_warnings(self, organ_conf_std: float, family_distances: Dict, zipf_metrics: Dict):
        """
        Print warnings based on signal health thresholds from FFITTSS architecture.

        Thresholds from docs:
        - Organ confidence std: target > 0.15, warning < 0.05
        - Inter-family distance: target > 1.5, warning < 1.0
        - Zipf's law: target R² > 0.85, α ≈ 0.7-0.8
        """
        warnings = []

        # Organ differentiation check
        if organ_conf_std < 0.05:
            warnings.append(f"🚨 CRITICAL: Organ confidence std={organ_conf_std:.4f} < 0.05 (organs not differentiating!)")
        elif organ_conf_std < 0.15:
            warnings.append(f"⚠️  WARNING: Organ confidence std={organ_conf_std:.4f} < 0.15 (insufficient differentiation)")

        # Family separation check
        if family_distances.get('min_distance', 0) > 0:
            min_dist = family_distances['min_distance']
            if min_dist < 0.5:
                warnings.append(f"🚨 CRITICAL: Min inter-family distance={min_dist:.4f} < 0.5 (families collapsing!)")
            elif min_dist < 1.0:
                warnings.append(f"⚠️  WARNING: Min inter-family distance={min_dist:.4f} < 1.0 (families too similar)")

        # Zipf's law check (only if enough families)
        if zipf_metrics.get('valid', False):
            interpretation = zipf_metrics.get('interpretation', '')
            if interpretation == 'too_flat':
                warnings.append(f"⚠️  WARNING: Zipf α={zipf_metrics['alpha']:.3f} < 0.5 (families too evenly distributed)")
            elif interpretation == 'too_concentrated':
                warnings.append(f"⚠️  WARNING: Zipf α={zipf_metrics['alpha']:.3f} > 1.2 (too few families dominating)")
            elif interpretation == 'non_zipfian':
                warnings.append(f"⚠️  WARNING: Zipf R²={zipf_metrics['r_squared']:.3f} < 0.7 (distribution not following natural emergence)")

        # Print all warnings
        if warnings:
            print(f"\n   📊 SIGNAL HEALTH WARNINGS:")
            for warning in warnings:
                print(f"      {warning}")
        else:
            print(f"\n   ✅ SIGNAL HEALTH: All metrics within healthy ranges")

    def _get_expected_trajectory(self, epoch: int) -> Dict:
        """
        Return expected learning trajectory targets based on epoch.

        From Complete Fractal Learning Architecture docs:
        - Epoch 0-20: Exploration phase (organ std: 0→0.08, families: 1→5)
        - Epoch 20-50: Differentiation phase (organ std: 0.08→0.15, families: 5→15)
        - Epoch 50-100: Consolidation phase (organ std: 0.15→0.20, families: 15→25)
        """
        if epoch <= 20:
            return {
                'phase': 'exploration',
                'expected_organ_std': 0.04 * (epoch / 20),  # 0 → 0.08
                'expected_families': 1 + int(4 * (epoch / 20)),  # 1 → 5
                'expected_zipf_r2': 'N/A (insufficient families)',
                'description': 'Organ patterns forming, initial family discovery'
            }
        elif epoch <= 50:
            progress = (epoch - 20) / 30
            return {
                'phase': 'differentiation',
                'expected_organ_std': 0.08 + 0.07 * progress,  # 0.08 → 0.15
                'expected_families': 5 + int(10 * progress),  # 5 → 15
                'expected_zipf_r2': 0.7 + 0.15 * progress,  # 0.7 → 0.85
                'description': 'Organs differentiating, families specializing'
            }
        else:
            progress = min((epoch - 50) / 50, 1.0)
            return {
                'phase': 'consolidation',
                'expected_organ_std': 0.15 + 0.05 * progress,  # 0.15 → 0.20
                'expected_families': 15 + int(10 * progress),  # 15 → 25
                'expected_zipf_r2': 0.85 + 0.05 * progress,  # 0.85 → 0.90
                'description': 'Mature taxonomy, Zipf law emergence'
            }

    def _print_epoch_summary(self, result: Dict):
        """Print summary of epoch results."""
        print(f"\n📊 EPOCH {result['epoch']} SUMMARY:")
        print(f"   Conversations: {result['conversations_processed']}")
        print(f"   Total Families: {result['total_families']} (+{result['new_families_created']} new)")
        print(f"   Family Sizes: {result['family_sizes']}")
        print(f"   Mean Satisfaction: {result['mean_satisfaction']:.4f} (±{result['satisfaction_std']:.4f})")
        print(f"   Mean Distance: {result['mean_distance']:.4f} (±{result['distance_std']:.4f})")
        print(f"   Organ Confidence Std: {result['organ_confidence_std']:.4f}")

        # Top organ changes
        changes = result['organ_changes']
        if changes:
            top_increase = max(changes.items(), key=lambda x: x[1])
            top_decrease = min(changes.items(), key=lambda x: x[1])
            print(f"   Top Organ Increase: {top_increase[0]} (+{top_increase[1]:.4f})")
            print(f"   Top Organ Decrease: {top_decrease[0]} ({top_decrease[1]:.4f})")

        # NEW: Compute advanced metrics from architecture docs
        family_sizes = result['family_sizes']
        zipf_metrics = self._compute_zipf_metrics(family_sizes)
        family_distances = self._compute_inter_family_distances()

        # Print Zipf's law metrics
        if zipf_metrics.get('valid', False):
            print(f"\n   📈 ZIPF'S LAW METRICS:")
            print(f"      α (power law exponent): {zipf_metrics['alpha']:.3f}")
            print(f"      R² (goodness of fit): {zipf_metrics['r_squared']:.3f}")
            print(f"      Interpretation: {zipf_metrics['interpretation']}")

        # Print inter-family distances
        if family_distances.get('mean_distance', 0) > 0:
            print(f"\n   🔍 INTER-FAMILY DISTANCES (65D Euclidean):")
            print(f"      Mean: {family_distances['mean_distance']:.4f}")
            print(f"      Min: {family_distances['min_distance']:.4f}")
            print(f"      Max: {family_distances['max_distance']:.4f}")

        # Print signal health warnings
        self._print_signal_health_warnings(
            result['organ_confidence_std'],
            family_distances,
            zipf_metrics
        )

        # Print expected trajectory comparison
        trajectory = self._get_expected_trajectory(result['epoch'])
        print(f"\n   📊 LEARNING TRAJECTORY:")
        print(f"      Phase: {trajectory['phase'].upper()}")
        print(f"      Expected organ std: {trajectory['expected_organ_std']:.4f}")
        print(f"      Actual organ std: {result['organ_confidence_std']:.4f}")
        print(f"      Expected families: {trajectory['expected_families']}")
        print(f"      Actual families: {result['total_families']}")
        if isinstance(trajectory['expected_zipf_r2'], float):
            print(f"      Expected Zipf R²: {trajectory['expected_zipf_r2']:.3f}")
        print(f"      Description: {trajectory['description']}")

        # Category breakdown
        print(f"\n   Per-Category Results:")
        for cat, data in sorted(result['category_results'].items()):
            print(f"      {cat}: {data['count']} pairs, "
                  f"satisfaction={data['mean_satisfaction']:.3f}, "
                  f"families={data['num_families']}")

        print(f"\n   ⏱️ Epoch Time: {result['epoch_time_seconds']:.2f}s")

    def _print_final_summary(self, total_time: float):
        """Print final training summary."""
        print(f"\n{'='*80}")
        print("🏆 CORE-GROUNDED TRAINING COMPLETE")
        print(f"{'='*80}")

        final_families = len(self.phase5_learner.families.families)
        final_organ_conf = self._get_organ_confidences()

        print(f"\n📊 FINAL METRICS:")
        print(f"   Total Epochs: {self.num_epochs}")
        print(f"   Total Families Emerged: {final_families}")
        print(f"   Training Time: {total_time:.2f}s")

        # Family evolution
        if self.epoch_metrics:
            family_counts = [m['total_families'] for m in self.epoch_metrics]
            print(f"\n📈 FAMILY EVOLUTION:")
            print(f"   Epoch 1: {family_counts[0]} families")
            print(f"   Epoch {len(family_counts)}: {family_counts[-1]} families")
            print(f"   Growth: +{family_counts[-1] - family_counts[0]} families")

        # Organ confidence differentiation
        conf_values = list(final_organ_conf.values())
        print(f"\n🧬 ORGAN CONFIDENCE DIFFERENTIATION:")
        print(f"   Mean: {np.mean(conf_values):.4f}")
        print(f"   Std: {np.std(conf_values):.4f}")
        print(f"   Range: [{min(conf_values):.4f}, {max(conf_values):.4f}]")

        # Top/bottom organs
        sorted_organs = sorted(final_organ_conf.items(), key=lambda x: x[1], reverse=True)
        print(f"   Top 3 Organs:")
        for organ, conf in sorted_organs[:3]:
            print(f"      {organ}: {conf:.4f}")
        print(f"   Bottom 3 Organs:")
        for organ, conf in sorted_organs[-3:]:
            print(f"      {organ}: {conf:.4f}")

        # Family diversity check
        if final_families > 1:
            print(f"\n✅ MULTI-FAMILY EMERGENCE ACHIEVED!")
            family_sizes = [f.member_count for f in self.phase5_learner.families.families.values()]
            print(f"   Family Distribution: {family_sizes}")

            # Final Zipf's law analysis
            zipf_metrics = self._compute_zipf_metrics(family_sizes)
            if zipf_metrics.get('valid', False):
                print(f"\n📈 FINAL ZIPF'S LAW ANALYSIS:")
                print(f"   α (power law exponent): {zipf_metrics['alpha']:.3f}")
                print(f"   R² (goodness of fit): {zipf_metrics['r_squared']:.3f}")
                print(f"   Interpretation: {zipf_metrics['interpretation']}")

                # Compare to targets from docs
                if zipf_metrics['r_squared'] > 0.85:
                    print(f"   ✅ R² > 0.85 - Natural emergence confirmed!")
                if 0.6 < zipf_metrics['alpha'] < 1.0:
                    print(f"   ✅ α ≈ 0.7-0.8 range - Healthy power law distribution!")

            # Final inter-family distances
            family_distances = self._compute_inter_family_distances()
            if family_distances.get('mean_distance', 0) > 0:
                print(f"\n🔍 FINAL INTER-FAMILY DISTANCES:")
                print(f"   Mean: {family_distances['mean_distance']:.4f}")
                print(f"   Min: {family_distances['min_distance']:.4f}")
                print(f"   Max: {family_distances['max_distance']:.4f}")
                print(f"   Std: {family_distances['std_distance']:.4f}")

                # Assess separation quality
                if family_distances['min_distance'] > 1.5:
                    print(f"   ✅ Min distance > 1.5 - Excellent family separation!")
                elif family_distances['min_distance'] > 1.0:
                    print(f"   ✅ Min distance > 1.0 - Good family separation")
                else:
                    print(f"   ⚠️ Min distance < 1.0 - Families may be too similar")

        else:
            print(f"\n⚠️ Single family formed - may need more diverse inputs or tuning")

        # Final learning trajectory assessment
        trajectory = self._get_expected_trajectory(self.num_epochs)
        print(f"\n📊 LEARNING TRAJECTORY ASSESSMENT:")
        print(f"   Final phase: {trajectory['phase'].upper()}")
        print(f"   Expected organ std: {trajectory['expected_organ_std']:.4f}")
        print(f"   Actual organ std: {np.std(conf_values):.4f}")
        print(f"   Expected families: {trajectory['expected_families']}")
        print(f"   Actual families: {final_families}")

        # Overall health assessment
        print(f"\n🎯 OVERALL TRAINING HEALTH:")
        health_score = 0
        total_checks = 4

        # Check 1: Organ differentiation
        if np.std(conf_values) > 0.15:
            print(f"   ✅ Organ differentiation: EXCELLENT (std > 0.15)")
            health_score += 1
        elif np.std(conf_values) > 0.05:
            print(f"   ⚠️ Organ differentiation: MODERATE (std > 0.05)")
            health_score += 0.5
        else:
            print(f"   ❌ Organ differentiation: POOR (std < 0.05)")

        # Check 2: Multi-family emergence
        if final_families >= 3:
            print(f"   ✅ Multi-family emergence: ACHIEVED ({final_families} families)")
            health_score += 1
        elif final_families >= 2:
            print(f"   ⚠️ Multi-family emergence: PARTIAL ({final_families} families)")
            health_score += 0.5
        else:
            print(f"   ❌ Multi-family emergence: NOT ACHIEVED")

        # Check 3: Family separation (if applicable)
        if final_families > 1:
            distances = self._compute_inter_family_distances()
            if distances.get('min_distance', 0) > 1.0:
                print(f"   ✅ Family separation: GOOD (min dist > 1.0)")
                health_score += 1
            elif distances.get('min_distance', 0) > 0.5:
                print(f"   ⚠️ Family separation: MODERATE (min dist > 0.5)")
                health_score += 0.5
            else:
                print(f"   ❌ Family separation: POOR (min dist < 0.5)")
        else:
            total_checks -= 1  # Skip if single family

        # Check 4: Satisfaction convergence
        if self.epoch_metrics:
            final_satisfaction = self.epoch_metrics[-1].get('mean_satisfaction', 0)
            if final_satisfaction > 0.8:
                print(f"   ✅ Satisfaction: HIGH ({final_satisfaction:.3f})")
                health_score += 1
            elif final_satisfaction > 0.6:
                print(f"   ⚠️ Satisfaction: MODERATE ({final_satisfaction:.3f})")
                health_score += 0.5
            else:
                print(f"   ❌ Satisfaction: LOW ({final_satisfaction:.3f})")
        else:
            total_checks -= 1

        health_percentage = (health_score / total_checks) * 100 if total_checks > 0 else 0
        print(f"\n   OVERALL HEALTH SCORE: {health_percentage:.1f}% ({health_score}/{total_checks} checks)")

    def _save_checkpoint(self, epoch: int):
        """Save checkpoint after each epoch."""
        checkpoint = {
            'epoch': epoch,
            'timestamp': datetime.now().isoformat(),
            'metrics': self.epoch_metrics[-1] if self.epoch_metrics else {},
            'families': len(self.phase5_learner.families.families),
            'organ_confidence': self._get_organ_confidences()
        }

        checkpoint_path = self.results_dir / f"checkpoint_epoch_{epoch}.json"
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2, default=str)

    def _save_final_results(self):
        """Save complete training results."""
        results = {
            'metadata': {
                'foundation': 'BOOKS_FOUNDATION_PROTOCOLS.md',
                'principles': ['IFS', 'Polyvagal', 'Trauma-Informed', 'Whiteheadian'],
                'num_epochs': self.num_epochs,
                'training_pairs': len(self.training_pairs),
                'completed': datetime.now().isoformat()
            },
            'epoch_metrics': self.epoch_metrics,
            'final_state': {
                'total_families': len(self.phase5_learner.families.families),
                'organ_confidence': self._get_organ_confidences(),
                'family_sizes': [f.member_count for f in self.phase5_learner.families.families.values()]
            }
        }

        results_path = self.results_dir / "core_grounded_training_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {results_path}")


def main():
    """Run CORE-grounded training."""
    import argparse

    parser = argparse.ArgumentParser(description="CORE-Grounded Training for DAE Organism")
    parser.add_argument('--epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('--no-reset', action='store_true', help='Do not reset families/confidence')
    parser.add_argument('--no-save', action='store_true', help='Do not save results')
    args = parser.parse_args()

    trainer = COREGroundedTrainer(
        num_epochs=args.epochs,
        reset_families=not args.no_reset,
        reset_organ_confidence=not args.no_reset,
        save_results=not args.no_save
    )

    trainer.train()


if __name__ == "__main__":
    main()
