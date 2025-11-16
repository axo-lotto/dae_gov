#!/usr/bin/env python3
"""
Multi-Family Emergence Trainer - Nexus Intelligence from Organ Agreement
=========================================================================

Uses long, diverse therapeutic prompts to force distinct 57D signatures and
enable multi-family emergence through organ agreement/entropy patterns.

Key Design:
-----------
- 30 long prompts (50-100+ words each)
- Targets specific polyvagal states, BOND zones, urgency levels
- Expected to produce 10-15 distinct families
- Tracks organ agreement patterns for nexus intelligence

Usage:
------
python3 training/multi_family_emergence_trainer.py --epochs 5 --reset

Expected Outcome:
-----------------
- Epoch 1: 5-8 families (initial differentiation)
- Epoch 3: 10-15 families (signature diversity)
- Epoch 5: 12-18 families (Zipf's law emerging)

Created: November 16, 2025
Purpose: Force multi-family emergence for nexus intelligence analysis
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import numpy as np
import shutil
import argparse

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


class MultiFamilyEmergenceTrainer:
    """
    Train with long, diverse prompts to force multi-family emergence
    and analyze nexus intelligence from organ agreement patterns.
    """

    def __init__(
        self,
        corpus_path: str = "knowledge_base/multi_family_emergence_corpus.json",
        reset_state: bool = False,
        verbose: bool = True
    ):
        self.corpus_path = corpus_path
        self.reset_state = reset_state
        self.verbose = verbose

        # Paths
        self.base_dir = Path(__file__).parent.parent
        self.results_dir = self.base_dir / "results" / "multi_family_emergence"
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Load corpus
        with open(corpus_path, 'r') as f:
            corpus_data = json.load(f)

        self.prompts = corpus_data.get('training_pairs', [])
        self.metadata = corpus_data.get('metadata', {})

        print("\n" + "="*80)
        print("MULTI-FAMILY EMERGENCE TRAINER")
        print("Nexus Intelligence from Organ Agreement Patterns")
        print("="*80)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Prompts: {len(self.prompts)}")
        print(f"Expected Families: {self.metadata.get('expected_families', '10-15')}")
        print(f"Reset State: {reset_state}")

        # Reset if requested
        if reset_state:
            self._reset_system_state()

        # Initialize organism
        print("\nInitializing Conversational Organism...")
        self.organism = ConversationalOrganismWrapper()
        print("   Organism ready")

        # Initialize tracking
        self.training_results = {
            'start_time': datetime.now().isoformat(),
            'corpus_info': {
                'total_prompts': len(self.prompts),
                'categories': self._extract_categories()
            },
            'epochs': [],
            'organ_agreement_patterns': [],
            'family_evolution': [],
            'nexus_type_distribution': {}
        }

    def _extract_categories(self) -> List[str]:
        """Extract unique categories from prompts."""
        categories = set()
        for prompt in self.prompts:
            categories.add(prompt.get('category', 'unknown'))
        return sorted(list(categories))

    def _reset_system_state(self):
        """Reset families, R-matrix, and organ confidence."""
        print("\n--- RESETTING SYSTEM STATE ---")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Reset organic families (both locations)
        for families_path in [
            self.base_dir / "persona_layer" / "state" / "active" / "organic_families.json",
            self.base_dir / "persona_layer" / "organic_families.json"
        ]:
            if families_path.exists():
                backup_path = families_path.parent / f"organic_families_backup_{timestamp}.json"
                shutil.copy(families_path, backup_path)
                print(f"   Backed up: {backup_path.name}")

                fresh_state = {
                    "families": {},
                    "conversation_to_family": {},
                    "next_family_id": 1,
                    "total_families": 0,
                    "mature_families": 0,
                    "total_conversations": 0,
                    "last_updated": datetime.now().isoformat()
                }
                with open(families_path, 'w') as f:
                    json.dump(fresh_state, f, indent=2)

        # Reset R-matrix
        rmatrix_path = self.base_dir / "persona_layer" / "state" / "active" / "conversational_hebbian_memory.json"
        if rmatrix_path.exists():
            backup_path = rmatrix_path.parent / f"rmatrix_backup_{timestamp}.json"
            shutil.copy(rmatrix_path, backup_path)

            fresh_rmatrix = {
                "r_matrix": [[0.0] * 11 for _ in range(11)],
                "last_updated": datetime.now().isoformat(),
                "reset_reason": f"Multi-family emergence training - {timestamp}",
                "r_matrix_metadata": {
                    "shape": [11, 11],
                    "learning_rate": 0.005,
                    "initialization": "zeros"
                }
            }
            with open(rmatrix_path, 'w') as f:
                json.dump(fresh_rmatrix, f, indent=2)

        print("   System state reset complete\n")

    def run_training(self, num_epochs: int = 5) -> Dict[str, Any]:
        """
        Run multi-family emergence training.

        Args:
            num_epochs: Number of training epochs

        Returns:
            Complete training results with family emergence data
        """
        print(f"\n{'='*80}")
        print(f"STARTING MULTI-FAMILY EMERGENCE TRAINING - {num_epochs} EPOCHS")
        print(f"{'='*80}")

        for epoch in range(num_epochs):
            epoch_num = epoch + 1
            print(f"\n{'='*80}")
            print(f"EPOCH {epoch_num}/{num_epochs}")
            print(f"{'='*80}")

            epoch_results = self._run_epoch(epoch_num)
            self.training_results['epochs'].append(epoch_results)

            # Track organ agreement patterns
            organ_agreement = self._analyze_organ_agreement(epoch_results)
            self.training_results['organ_agreement_patterns'].append(organ_agreement)

            # Track family evolution
            family_snapshot = self._capture_family_state()
            self.training_results['family_evolution'].append({
                'epoch': epoch_num,
                'timestamp': datetime.now().isoformat(),
                **family_snapshot
            })

            # Print epoch summary
            self._print_epoch_summary(epoch_num, epoch_results, family_snapshot)

        # Final analysis
        print(f"\n{'='*80}")
        print(f"TRAINING COMPLETE - FINAL ANALYSIS")
        print(f"{'='*80}")

        self._analyze_final_results()
        self._save_results()

        return self.training_results

    def _run_epoch(self, epoch_num: int) -> Dict[str, Any]:
        """Run single training epoch."""
        epoch_results = {
            'epoch': epoch_num,
            'timestamp': datetime.now().isoformat(),
            'prompts_processed': 0,
            'results': [],
            'category_breakdown': {},
            'organ_activations': {organ: [] for organ in [
                'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'
            ]},
            'polyvagal_states': {},
            'zones': {},
            'urgency_levels': []
        }

        for i, prompt in enumerate(self.prompts):
            prompt_id = prompt['id']
            user_input = prompt['user_input']
            category = prompt.get('category', 'unknown')
            expected_sig = prompt.get('expected_signature', {})

            if self.verbose and (i + 1) % 10 == 0:
                print(f"   Processing {i+1}/{len(self.prompts)}...")

            try:
                # Process through organism
                result = self.organism.process_text(
                    text=user_input,
                    context={
                        'conversation_id': f"mfe_epoch{epoch_num}_{prompt_id}",
                        'enable_transduction': True
                    },
                    enable_phase2=True
                )

                # Extract felt states
                felt_states = result.get('felt_states', {})
                organ_results = result.get('organ_results', {})

                # Extract key metrics
                actual_polyvagal = felt_states.get('eo_polyvagal_state', 'ventral_vagal')
                actual_zone = felt_states.get('zone', 1)
                actual_urgency = felt_states.get('NDAM_urgency_level', 0.0)
                family_id = felt_states.get('phase5_family_id', 'NONE')
                satisfaction = felt_states.get('satisfaction_final', 0.0)
                v0_descent = felt_states.get('v0_descent_ratio', 0.0)

                # Track organ coherences
                organ_coherences = {}
                for organ_name, organ_result in organ_results.items():
                    if organ_name == 'NEXUS':
                        continue
                    if hasattr(organ_result, 'coherence'):
                        coherence = organ_result.coherence
                        epoch_results['organ_activations'][organ_name].append(coherence)
                        organ_coherences[organ_name] = coherence

                # Track polyvagal distribution
                if actual_polyvagal not in epoch_results['polyvagal_states']:
                    epoch_results['polyvagal_states'][actual_polyvagal] = 0
                epoch_results['polyvagal_states'][actual_polyvagal] += 1

                # Track zone distribution
                zone_key = f"zone_{actual_zone}"
                if zone_key not in epoch_results['zones']:
                    epoch_results['zones'][zone_key] = 0
                epoch_results['zones'][zone_key] += 1

                # Track urgency
                epoch_results['urgency_levels'].append(actual_urgency)

                # Track category
                if category not in epoch_results['category_breakdown']:
                    epoch_results['category_breakdown'][category] = {
                        'count': 0,
                        'families': set(),
                        'avg_satisfaction': []
                    }
                epoch_results['category_breakdown'][category]['count'] += 1
                epoch_results['category_breakdown'][category]['families'].add(family_id)
                epoch_results['category_breakdown'][category]['avg_satisfaction'].append(satisfaction)

                # Store result
                epoch_results['results'].append({
                    'prompt_id': prompt_id,
                    'category': category,
                    'expected': expected_sig,
                    'actual': {
                        'polyvagal': actual_polyvagal,
                        'zone': actual_zone,
                        'urgency': actual_urgency,
                        'family_id': family_id,
                        'satisfaction': satisfaction,
                        'v0_descent': v0_descent
                    },
                    'organ_coherences': organ_coherences
                })

                epoch_results['prompts_processed'] += 1

            except Exception as e:
                if self.verbose:
                    print(f"   Error processing {prompt_id}: {str(e)[:50]}")

        # Convert sets to lists for JSON serialization
        for cat, data in epoch_results['category_breakdown'].items():
            data['families'] = list(data['families'])
            data['avg_satisfaction'] = float(np.mean(data['avg_satisfaction']))

        return epoch_results

    def _analyze_organ_agreement(self, epoch_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze organ agreement patterns for nexus intelligence."""
        organ_activations = epoch_results.get('organ_activations', {})

        # Compute organ co-activation matrix (correlation)
        organ_names = list(organ_activations.keys())
        n_organs = len(organ_names)

        # Build activation matrix
        activation_matrix = []
        for organ in organ_names:
            activations = organ_activations.get(organ, [])
            if activations:
                activation_matrix.append(activations)

        if not activation_matrix or len(activation_matrix[0]) == 0:
            return {'error': 'No activation data'}

        activation_matrix = np.array(activation_matrix)

        # Compute correlation (organ agreement)
        correlation_matrix = np.corrcoef(activation_matrix)

        # Compute entropy per organ (diversity of activations)
        organ_entropy = {}
        for i, organ in enumerate(organ_names):
            activations = organ_activations[organ]
            if activations:
                # Discretize activations into bins
                hist, _ = np.histogram(activations, bins=10, range=(0, 1))
                hist = hist / hist.sum() + 1e-10  # Normalize and avoid log(0)
                entropy = -np.sum(hist * np.log2(hist))
                organ_entropy[organ] = float(entropy)

        # Find strongest organ agreements (off-diagonal correlations)
        agreements = []
        for i in range(n_organs):
            for j in range(i + 1, n_organs):
                corr = correlation_matrix[i, j]
                if not np.isnan(corr):
                    agreements.append({
                        'organ1': organ_names[i],
                        'organ2': organ_names[j],
                        'correlation': float(corr)
                    })

        agreements.sort(key=lambda x: abs(x['correlation']), reverse=True)

        # Compute overall agreement score
        upper_triangle = correlation_matrix[np.triu_indices_from(correlation_matrix, k=1)]
        mean_agreement = float(np.nanmean(upper_triangle))
        agreement_variance = float(np.nanvar(upper_triangle))

        return {
            'epoch': epoch_results['epoch'],
            'mean_agreement': mean_agreement,
            'agreement_variance': agreement_variance,
            'organ_entropy': organ_entropy,
            'top_agreements': agreements[:10],
            'bottom_agreements': agreements[-10:] if len(agreements) >= 10 else agreements
        }

    def _capture_family_state(self) -> Dict[str, Any]:
        """Capture current family clustering state."""
        families_path = self.base_dir / "persona_layer" / "organic_families.json"

        if not families_path.exists():
            return {'total_families': 0, 'families': {}}

        with open(families_path, 'r') as f:
            data = json.load(f)

        family_info = {
            'total_families': data.get('total_families', len(data.get('families', {}))),
            'total_conversations': data.get('total_conversations', 0),
            'family_sizes': [],
            'family_satisfactions': []
        }

        for fam_id, fam_data in data.get('families', {}).items():
            family_info['family_sizes'].append(fam_data.get('member_count', 0))
            family_info['family_satisfactions'].append(fam_data.get('mean_satisfaction', 0.0))

        if family_info['family_sizes']:
            family_info['size_distribution'] = {
                'min': int(np.min(family_info['family_sizes'])),
                'max': int(np.max(family_info['family_sizes'])),
                'mean': float(np.mean(family_info['family_sizes'])),
                'std': float(np.std(family_info['family_sizes']))
            }

        return family_info

    def _print_epoch_summary(
        self,
        epoch_num: int,
        epoch_results: Dict[str, Any],
        family_snapshot: Dict[str, Any]
    ):
        """Print epoch summary."""
        print(f"\n--- EPOCH {epoch_num} SUMMARY ---")

        print(f"   Prompts processed: {epoch_results['prompts_processed']}/{len(self.prompts)}")

        # Polyvagal distribution
        print(f"\n   Polyvagal States:")
        for state, count in sorted(epoch_results['polyvagal_states'].items()):
            pct = count / epoch_results['prompts_processed'] * 100
            print(f"      {state}: {count} ({pct:.1f}%)")

        # Zone distribution
        print(f"\n   SELF Matrix Zones:")
        for zone, count in sorted(epoch_results['zones'].items()):
            pct = count / epoch_results['prompts_processed'] * 100
            print(f"      {zone}: {count} ({pct:.1f}%)")

        # Urgency
        urgency_mean = np.mean(epoch_results['urgency_levels'])
        urgency_std = np.std(epoch_results['urgency_levels'])
        print(f"\n   Urgency: mean={urgency_mean:.3f}, std={urgency_std:.3f}")

        # Family emergence
        print(f"\n   Family Emergence:")
        print(f"      Total families: {family_snapshot['total_families']}")
        print(f"      Total conversations: {family_snapshot['total_conversations']}")
        if 'size_distribution' in family_snapshot:
            dist = family_snapshot['size_distribution']
            print(f"      Size distribution: min={dist['min']}, max={dist['max']}, mean={dist['mean']:.1f}")

        # Category analysis
        print(f"\n   Category → Family Mapping:")
        for category, data in sorted(epoch_results['category_breakdown'].items()):
            n_families = len(data['families'])
            print(f"      {category}: {data['count']} prompts → {n_families} families")

    def _analyze_final_results(self):
        """Analyze final training results."""
        print("\n NEXUS INTELLIGENCE ANALYSIS")
        print("-" * 60)

        # Organ agreement evolution
        if self.training_results['organ_agreement_patterns']:
            first_agreement = self.training_results['organ_agreement_patterns'][0]
            last_agreement = self.training_results['organ_agreement_patterns'][-1]

            print(f"   Organ Agreement Evolution:")
            print(f"      Epoch 1: mean={first_agreement.get('mean_agreement', 0):.4f}")
            print(f"      Final:   mean={last_agreement.get('mean_agreement', 0):.4f}")

            print(f"\n   Top Organ Agreements (Final Epoch):")
            for agreement in last_agreement.get('top_agreements', [])[:5]:
                print(f"      {agreement['organ1']}-{agreement['organ2']}: {agreement['correlation']:.3f}")

        # Family emergence trajectory
        print(f"\n FAMILY EMERGENCE TRAJECTORY")
        print("-" * 60)

        for evolution in self.training_results['family_evolution']:
            epoch = evolution['epoch']
            total_fam = evolution['total_families']
            print(f"   Epoch {epoch}: {total_fam} families")

        # Category → Family mapping quality
        print(f"\n CATEGORY-FAMILY COHERENCE")
        print("-" * 60)

        if self.training_results['epochs']:
            last_epoch = self.training_results['epochs'][-1]
            category_breakdown = last_epoch.get('category_breakdown', {})

            coherent_categories = 0
            for category, data in category_breakdown.items():
                n_families = len(data['families'])
                if n_families <= 2:
                    coherent_categories += 1

            coherence_score = coherent_categories / len(category_breakdown) if category_breakdown else 0
            print(f"   Categories with coherent families (≤2): {coherent_categories}/{len(category_breakdown)}")
            print(f"   Coherence score: {coherence_score:.2%}")

        # Assessment
        print(f"\n OVERALL ASSESSMENT")
        print("-" * 60)

        if self.training_results['family_evolution']:
            final_families = self.training_results['family_evolution'][-1]['total_families']

            if final_families >= 12:
                assessment = "EXCELLENT - Strong multi-family emergence"
            elif final_families >= 8:
                assessment = "GOOD - Moderate family differentiation"
            elif final_families >= 4:
                assessment = "MINIMUM - Basic differentiation achieved"
            else:
                assessment = "POOR - Insufficient family emergence"

            print(f"   Final families: {final_families}")
            print(f"   Assessment: {assessment}")

    def _save_results(self):
        """Save training results to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"multi_family_emergence_{timestamp}.json"
        filepath = self.results_dir / filename

        # Clean for JSON
        results_clean = self._clean_for_json(self.training_results)

        with open(filepath, 'w') as f:
            json.dump(results_clean, f, indent=2)

        print(f"\n   Results saved to: {filepath}")

    def _clean_for_json(self, obj):
        """Convert numpy types for JSON serialization."""
        if isinstance(obj, dict):
            return {k: self._clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._clean_for_json(v) for v in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, set):
            return list(obj)
        else:
            return obj


def main():
    """Run multi-family emergence training."""
    parser = argparse.ArgumentParser(
        description="Multi-Family Emergence Trainer - Nexus Intelligence"
    )
    parser.add_argument(
        '--corpus',
        type=str,
        default='knowledge_base/multi_family_emergence_corpus.json',
        help='Path to training corpus'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=5,
        help='Number of training epochs'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset system state before training'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='Print detailed progress'
    )

    args = parser.parse_args()

    # Initialize trainer
    trainer = MultiFamilyEmergenceTrainer(
        corpus_path=args.corpus,
        reset_state=args.reset,
        verbose=args.verbose
    )

    # Run training
    results = trainer.run_training(num_epochs=args.epochs)

    print(f"\n{'='*80}")
    print("MULTI-FAMILY EMERGENCE TRAINING COMPLETE")
    print(f"{'='*80}")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results in: {trainer.results_dir}")


if __name__ == '__main__':
    main()
