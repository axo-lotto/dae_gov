"""
IFS Diversity Training - Leverage All Existing Infrastructure
==============================================================

This script feeds the IFS diverse corpus through the existing organism infrastructure
to achieve felt-state diversity and organic family formation.

Strategy:
---------
1. Load IFS corpus (20 scenarios with felt-state annotations)
2. Feed each scenario through ConversationalOrganismWrapper.respond()
3. Organism automatically:
   - Processes 11 organs in parallel
   - Extracts 57D signature (via OrganSignatureExtractor)
   - Assigns to family (via OrganicConversationalFamilies)
   - Updates learning (R-matrix, organ confidence)
4. Validate family diversity after training

Expected Outcome:
-----------------
- Before: 1 family (all organs ~0.5, range 0.18)
- After: 12-15 families (organ range 0.60-0.95, 5× improvement)

Infrastructure Leveraged:
-------------------------
✅ organ_signature_extractor.py - 57D signatures
✅ organic_conversational_families.py - Cosine similarity clustering
✅ conversational_organism_wrapper.py - Complete processing pipeline
✅ llm_felt_guidance.py - Zone-specific LLM prompts

Created: November 15, 2025
Author: DAE_HYPHAE_1 Development Team
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import numpy as np

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


class IFSDiversityTrainer:
    """Train organism with diverse IFS corpus to enable family formation."""

    def __init__(
        self,
        corpus_path: str = "knowledge_base/ifs_diverse_corpus.json",
        reset_families: bool = False
    ):
        """
        Initialize IFS diversity trainer.

        Args:
            corpus_path: Path to IFS corpus JSON
            reset_families: If True, backup and reset family state before training
        """
        self.corpus_path = corpus_path
        self.reset_families = reset_families

        # Load corpus
        with open(corpus_path, 'r') as f:
            corpus_data = json.load(f)

        self.scenarios = corpus_data.get('training_pairs', [])
        self.metadata = corpus_data.get('metadata', {})

        print(f"\n{'='*80}")
        print(f"IFS DIVERSITY TRAINING")
        print(f"{'='*80}\n")
        print(f"Corpus: {corpus_path}")
        print(f"Scenarios: {len(self.scenarios)}")
        print(f"Emotional states: {self.metadata.get('total_scenarios', 'N/A')}")
        print(f"Zones covered: {self.metadata.get('zones_covered', 'N/A')}")
        print(f"Polyvagal states: {self.metadata.get('polyvagal_states', 'N/A')}\n")

        # Initialize organism
        print("Initializing conversational organism...")
        self.organism = ConversationalOrganismWrapper()
        print("✅ Organism ready\n")

        # Optionally reset families
        if reset_families:
            self._reset_family_state()

    def _reset_family_state(self):
        """Backup current families and reset to fresh start."""
        import shutil
        from datetime import datetime

        family_path = Path("persona_layer/state/active/organic_families.json")

        if family_path.exists():
            # Backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = family_path.parent / f"organic_families_backup_{timestamp}.json"
            shutil.copy(family_path, backup_path)
            print(f"📦 Backed up families to: {backup_path}")

            # Reset
            fresh_state = {
                "families": {},
                "conversation_to_family": {},
                "next_family_id": 1,
                "total_families": 0,
                "mature_families": 0,
                "total_conversations": 0
            }

            with open(family_path, 'w') as f:
                json.dump(fresh_state, f, indent=2)

            print("✅ Family state reset to fresh start\n")

    def run_training(
        self,
        num_epochs: int = 5,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run diversity training with IFS corpus.

        Args:
            num_epochs: Number of training epochs
            verbose: Print detailed progress

        Returns:
            Training results with family formation metrics
        """
        results = {
            'epochs': [],
            'final_families': None,
            'diversity_metrics': None
        }

        for epoch in range(num_epochs):
            print(f"\n{'='*80}")
            print(f"EPOCH {epoch + 1}/{num_epochs}")
            print(f"{'='*80}\n")

            epoch_results = self._run_epoch(epoch + 1, verbose=verbose)
            results['epochs'].append(epoch_results)

            # Print epoch summary
            families = self.organism.family_clusterer.families if hasattr(self.organism, 'family_clusterer') else {}
            total_families = len(families)
            mature_families = sum(1 for f in families.values() if getattr(f, 'is_mature', False))

            print(f"\n📊 Epoch {epoch + 1} Summary:")
            print(f"   Total families: {total_families}")
            print(f"   Mature families: {mature_families}")
            print(f"   Scenarios processed: {len(self.scenarios)}")

        # Final validation
        print(f"\n{'='*80}")
        print(f"TRAINING COMPLETE")
        print(f"{'='*80}\n")

        validation_results = self._validate_diversity()
        results['final_families'] = validation_results['families']
        results['diversity_metrics'] = validation_results['metrics']

        return results

    def _run_epoch(self, epoch_num: int, verbose: bool = True) -> Dict[str, Any]:
        """Run single training epoch."""
        epoch_results = {
            'epoch': epoch_num,
            'scenarios_processed': 0,
            'family_assignments': [],
            'avg_satisfaction': 0.0
        }

        satisfactions = []

        for i, scenario in enumerate(self.scenarios):
            scenario_id = scenario['id']
            user_input = scenario['user_input']
            category = scenario.get('category', 'unknown')

            if verbose:
                print(f"[{i+1}/{len(self.scenarios)}] {scenario_id} ({category})")
                print(f"User: {user_input[:80]}{'...' if len(user_input) > 80 else ''}")

            # LEVERAGE EXISTING INFRASTRUCTURE
            # All processing happens automatically in organism.respond():
            # 1. Entity extraction
            # 2. 11-organ prehension (parallel)
            # 3. V0 convergence (multi-cycle)
            # 4. Nexus formation
            # 5. Transduction
            # 6. Emission generation
            # 7. 57D signature extraction
            # 8. Family assignment
            # 9. Learning updates

            try:
                response = self.organism.process_text(
                    text=user_input,
                    context={'conversation_id': f"ifs_epoch{epoch_num}_{scenario_id}"},
                    enable_phase2=True  # Use multi-cycle V0 convergence
                )

                # Extract results from felt_states
                felt_states = response.get('felt_states', {})
                family_id = felt_states.get('phase5_family_id', 'N/A')
                satisfaction = felt_states.get('satisfaction_final', 0.0)

                satisfactions.append(satisfaction)

                epoch_results['scenarios_processed'] += 1
                epoch_results['family_assignments'].append({
                    'scenario_id': scenario_id,
                    'family_id': family_id,
                    'satisfaction': satisfaction
                })

                if verbose:
                    print(f"  → Family: {family_id}")
                    print(f"  → Satisfaction: {satisfaction:.3f}")
                    print()

            except Exception as e:
                print(f"  ❌ Error processing {scenario_id}: {e}")
                print()

        epoch_results['avg_satisfaction'] = np.mean(satisfactions) if satisfactions else 0.0

        return epoch_results

    def _validate_diversity(self) -> Dict[str, Any]:
        """Validate family diversity after training."""
        print("🔍 Validating family diversity...\n")

        # Access family clusterer
        if not hasattr(self.organism, 'family_clusterer'):
            print("⚠️  Family clusterer not available")
            return {'families': {}, 'metrics': {}}

        families = self.organism.family_clusterer.families

        # Compute metrics
        total_families = len(families)
        mature_families = sum(1 for f in families.values() if getattr(f, 'is_mature', False))

        family_sizes = []
        organ_activations = {organ: [] for organ in [
            'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
            'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'
        ]}

        for family_id, family in families.items():
            member_count = getattr(family, 'member_count', 0)
            family_sizes.append(member_count)

            # Extract organ means from centroid
            centroid = getattr(family, 'centroid', np.zeros(57))

            # Organ signature structure (from OrganSignatureExtractor):
            # LISTENING: 0-5 (6D)
            # EMPATHY: 6-12 (7D)
            # WISDOM: 13-19 (7D)
            # AUTHENTICITY: 20-25 (6D)
            # PRESENCE: 26-31 (6D)
            # BOND: 32-36 (5D)
            # SANS: 37-40 (4D)
            # NDAM: 41-44 (4D)
            # RNX: 45-48 (4D)
            # EO: 49-52 (4D)
            # CARD: 53-56 (4D)

            organ_ranges = {
                'LISTENING': (0, 6),
                'EMPATHY': (6, 13),
                'WISDOM': (13, 20),
                'AUTHENTICITY': (20, 26),
                'PRESENCE': (26, 32),
                'BOND': (32, 37),
                'SANS': (37, 41),
                'NDAM': (41, 45),
                'RNX': (45, 49),
                'EO': (49, 53),
                'CARD': (53, 57)
            }

            for organ, (start, end) in organ_ranges.items():
                organ_mean = float(np.mean(centroid[start:end]))
                organ_activations[organ].append(organ_mean)

        # Compute organ discrimination (range across families)
        organ_discrimination = {}
        for organ, values in organ_activations.items():
            if values:
                organ_discrimination[organ] = {
                    'min': float(np.min(values)),
                    'max': float(np.max(values)),
                    'range': float(np.max(values) - np.min(values)),
                    'mean': float(np.mean(values)),
                    'std': float(np.std(values))
                }

        # Compute diversity score
        target_families = 15  # Expected for 20 scenarios
        diversity_score = min(total_families / target_families, 1.0)

        # Compute overall organ discrimination
        organ_ranges = [stats['range'] for stats in organ_discrimination.values()]
        avg_discrimination = float(np.mean(organ_ranges)) if organ_ranges else 0.0

        metrics = {
            'total_families': total_families,
            'mature_families': mature_families,
            'family_sizes': {
                'min': int(np.min(family_sizes)) if family_sizes else 0,
                'max': int(np.max(family_sizes)) if family_sizes else 0,
                'mean': float(np.mean(family_sizes)) if family_sizes else 0.0,
                'std': float(np.std(family_sizes)) if family_sizes else 0.0
            },
            'organ_discrimination': organ_discrimination,
            'avg_discrimination': avg_discrimination,
            'diversity_score': diversity_score,
            'assessment': self._assess_diversity(
                total_families,
                avg_discrimination
            )
        }

        # Print results
        print(f"✅ Validation Complete\n")
        print(f"📊 Family Diversity Metrics:")
        print(f"   Total families: {total_families} (target: 12-15 for 20 scenarios)")
        print(f"   Mature families: {mature_families}")
        print(f"   Diversity score: {diversity_score:.2f}")
        print(f"   Avg organ discrimination: {avg_discrimination:.3f} (target: >0.30)")
        print(f"\n📈 Organ Discrimination Ranges:")

        for organ, stats in organ_discrimination.items():
            print(f"   {organ:15s}: {stats['range']:.3f} (min={stats['min']:.3f}, max={stats['max']:.3f})")

        print(f"\n🎯 Assessment: {metrics['assessment']}")

        return {
            'families': {fid: self._serialize_family(f) for fid, f in families.items()},
            'metrics': metrics
        }

    def _serialize_family(self, family) -> Dict[str, Any]:
        """Convert family object to serializable dict."""
        return {
            'member_count': getattr(family, 'member_count', 0),
            'is_mature': getattr(family, 'is_mature', False),
            'maturity_level': getattr(family, 'maturity_level', 'unknown'),
            'centroid_shape': getattr(family, 'centroid', np.zeros(57)).shape
        }

    def _assess_diversity(self, total_families: int, avg_discrimination: float) -> str:
        """Assess diversity quality."""
        if total_families >= 12 and avg_discrimination >= 0.50:
            return "EXCELLENT - Strong family diversity with clear organ differentiation"
        elif total_families >= 8 and avg_discrimination >= 0.30:
            return "GOOD - Moderate family diversity, zones differentiating"
        elif total_families >= 5 and avg_discrimination >= 0.20:
            return "MINIMUM - Basic differentiation achieved, needs more diversity"
        else:
            return "POOR - Insufficient diversity, single-family collapse likely"


def main():
    """Run IFS diversity training."""
    import argparse

    parser = argparse.ArgumentParser(description="IFS Diversity Training")
    parser.add_argument(
        '--corpus',
        type=str,
        default='knowledge_base/ifs_diverse_corpus.json',
        help='Path to IFS corpus JSON'
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
        help='Reset family state before training'
    )
    parser.add_argument(
        '--save-results',
        type=str,
        default='results/ifs_diversity_training_results.json',
        help='Path to save training results'
    )

    args = parser.parse_args()

    # Initialize trainer
    trainer = IFSDiversityTrainer(
        corpus_path=args.corpus,
        reset_families=args.reset
    )

    # Run training
    results = trainer.run_training(
        num_epochs=args.epochs,
        verbose=True
    )

    # Save results
    results_path = Path(args.save_results)
    results_path.parent.mkdir(parents=True, exist_ok=True)

    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {results_path}")
    print(f"\n{'='*80}")
    print("🌀 IFS DIVERSITY TRAINING COMPLETE 🌀")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
