#!/usr/bin/env python3
"""
Entity Memory Epoch Training with Context Window Scalability Testing
November 14, 2025

Tests:
1. Entity extraction and persistence across epochs
2. Entity recall accuracy (name, relationships, preferences, goals)
3. Context window scalability (entity_context_string growth)
4. Multi-turn memory consistency
5. TSK learning (R-matrix adaptation to entity patterns)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from datetime import datetime
from typing import Dict, List, Tuple
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.user_registry import UserRegistry
from persona_layer.superject_structures import EnhancedUserProfile
import time

class EntityEpochTrainer:
    """
    Entity-focused epoch training with context window scalability metrics.
    """

    def __init__(
        self,
        corpus_path: str = 'knowledge_base/entity_memory_training_pairs.json',
        results_dir: str = 'results/entity_training'
    ):
        self.corpus_path = corpus_path
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Load training corpus
        with open(corpus_path, 'r') as f:
            self.corpus = json.load(f)

        # Initialize organism
        print("\n🌀 Initializing organism for entity training...")
        self.organism = ConversationalOrganismWrapper()

        # User registry for managing test users
        self.user_registry = UserRegistry()

        # Metrics tracking
        self.metrics = {
            'epochs': [],
            'context_window_growth': [],
            'entity_recall_accuracy': [],
            'processing_time': [],
            'r_matrix_evolution': []
        }

    def measure_context_window(self, entity_context_string: str) -> Dict:
        """
        Measure context window metrics for scalability testing.
        """
        return {
            'character_count': len(entity_context_string),
            'line_count': entity_context_string.count('\n'),
            'entity_count': entity_context_string.count('- '),  # Entities start with "- "
            'estimated_tokens': len(entity_context_string.split()),  # Rough estimate
        }

    def run_scenario(
        self,
        scenario: Dict,
        user_id: str,
        epoch_num: int
    ) -> Dict:
        """
        Run a single scenario (multi-turn conversation) and measure entity handling.
        """
        scenario_results = {
            'scenario_id': scenario['scenario_id'],
            'scenario_name': scenario['name'],
            'turns': [],
            'entity_recall_successes': 0,
            'entity_recall_failures': 0,
            'context_window_per_turn': []
        }

        print(f"\n   📖 Scenario: {scenario['name']}")
        print(f"      Turns: {len(scenario['turns'])}")

        # Load user state (or create fresh)
        user_state = self.user_registry.load_user_state(user_id)
        if 'user_profile' not in user_state:
            from datetime import datetime
            user_state['user_profile'] = EnhancedUserProfile(
                user_id=user_id,
                created_at=datetime.now().isoformat(),
                last_active=datetime.now().isoformat()
            ).to_dict()

        profile = EnhancedUserProfile.from_dict(user_state['user_profile'])

        for turn_data in scenario['turns']:
            turn_num = turn_data['turn']
            user_input = turn_data['user_input']

            print(f"\n      Turn {turn_num}: \"{user_input[:50]}...\"")

            # Build context (exactly as dae_interactive.py does)
            entity_context_string = profile.get_entity_context_string()
            context = {
                'user_id': user_id,
                'username': profile.entities.get('user_name', 'Unknown'),
                'stored_entities': profile.entities.copy(),
                'entity_context_string': entity_context_string,
                'memory_intent': turn_data.get('memory_intent', False),
                'epoch_num': epoch_num,
                'scenario_id': scenario['scenario_id'],
                'turn': turn_num
            }

            # Measure context window BEFORE processing
            context_metrics = self.measure_context_window(entity_context_string)
            print(f"         Context window: {context_metrics['estimated_tokens']} tokens, "
                  f"{context_metrics['entity_count']} entities")

            # Process with organism
            start_time = time.time()
            result = self.organism.process_text(user_input, context=context)
            processing_time = time.time() - start_time

            # Extract emission text
            if isinstance(result, dict):
                emission_text = result.get('emission_text', str(result))
            else:
                emission_text = str(result)

            print(f"         Response: \"{emission_text[:60]}...\"")
            print(f"         Processing: {processing_time:.3f}s")

            # Update profile from organism (entity extraction)
            # The organism's superject_learner automatically updates profile
            # Reload user state to get updated entities
            user_state = self.user_registry.load_user_state(user_id)
            if 'user_profile' in user_state:
                profile = EnhancedUserProfile.from_dict(user_state['user_profile'])
            else:
                # Profile not yet created by organism, keep existing one
                pass

            # Check entity recall accuracy
            expected_contains = turn_data.get('expected_response_contains', [])
            recall_success = all(
                term.lower() in emission_text.lower()
                for term in expected_contains
            )

            if expected_contains:
                if recall_success:
                    print(f"         ✅ Entity recall: All expected terms present")
                    scenario_results['entity_recall_successes'] += 1
                else:
                    print(f"         ❌ Entity recall: Missing expected terms: {expected_contains}")
                    scenario_results['entity_recall_failures'] += 1

            # Record turn results
            turn_results = {
                'turn': turn_num,
                'user_input': user_input,
                'emission_text': emission_text,
                'processing_time': processing_time,
                'context_window': context_metrics,
                'entities_after_turn': profile.entities.copy(),
                'entity_recall_success': recall_success if expected_contains else None,
                'expected_contains': expected_contains,
                'memory_intent': turn_data.get('memory_intent', False)
            }

            scenario_results['turns'].append(turn_results)
            scenario_results['context_window_per_turn'].append(context_metrics)

        # Compute scenario metrics
        total_recall_tests = scenario_results['entity_recall_successes'] + scenario_results['entity_recall_failures']
        scenario_results['entity_recall_accuracy'] = (
            scenario_results['entity_recall_successes'] / total_recall_tests
            if total_recall_tests > 0 else 0.0
        )

        print(f"\n      ✅ Scenario complete:")
        print(f"         Entity recall accuracy: {scenario_results['entity_recall_accuracy']:.1%}")
        print(f"         Successes: {scenario_results['entity_recall_successes']}")
        print(f"         Failures: {scenario_results['entity_recall_failures']}")

        return scenario_results

    def run_epoch(self, epoch_num: int, scenarios_to_run: List[int] = None) -> Dict:
        """
        Run one training epoch on entity memory scenarios.

        Args:
            epoch_num: Epoch number (1-indexed)
            scenarios_to_run: List of scenario indices to run (None = all)
        """
        print(f"\n{'='*80}")
        print(f"🎓 ENTITY EPOCH {epoch_num}")
        print(f"{'='*80}")

        epoch_results = {
            'epoch_num': epoch_num,
            'timestamp': datetime.now().isoformat(),
            'scenarios': [],
            'aggregate_metrics': {}
        }

        # Determine which scenarios to run
        scenarios = self.corpus['scenarios']
        if scenarios_to_run:
            scenarios = [scenarios[i] for i in scenarios_to_run if i < len(scenarios)]

        print(f"\n📚 Running {len(scenarios)} scenarios...")

        # Create a test user for this epoch
        test_user_id = f"entity_training_epoch{epoch_num}_{int(time.time())}"

        for scenario in scenarios:
            scenario_results = self.run_scenario(scenario, test_user_id, epoch_num)
            epoch_results['scenarios'].append(scenario_results)

        # Aggregate metrics across all scenarios
        total_successes = sum(s['entity_recall_successes'] for s in epoch_results['scenarios'])
        total_failures = sum(s['entity_recall_failures'] for s in epoch_results['scenarios'])
        total_tests = total_successes + total_failures

        epoch_results['aggregate_metrics'] = {
            'total_scenarios': len(scenarios),
            'total_turns': sum(len(s['turns']) for s in epoch_results['scenarios']),
            'entity_recall_accuracy': total_successes / total_tests if total_tests > 0 else 0.0,
            'entity_recall_successes': total_successes,
            'entity_recall_failures': total_failures,
            'mean_processing_time': sum(
                turn['processing_time']
                for s in epoch_results['scenarios']
                for turn in s['turns']
            ) / sum(len(s['turns']) for s in epoch_results['scenarios']),
            'max_context_tokens': max(
                turn['context_window']['estimated_tokens']
                for s in epoch_results['scenarios']
                for turn in s['turns']
            ),
            'mean_context_tokens': sum(
                turn['context_window']['estimated_tokens']
                for s in epoch_results['scenarios']
                for turn in s['turns']
            ) / sum(len(s['turns']) for s in epoch_results['scenarios']),
            'max_entity_count': max(
                turn['context_window']['entity_count']
                for s in epoch_results['scenarios']
                for turn in s['turns']
            )
        }

        # Print epoch summary
        print(f"\n{'='*80}")
        print(f"📊 EPOCH {epoch_num} SUMMARY")
        print(f"{'='*80}")
        print(f"   Scenarios: {epoch_results['aggregate_metrics']['total_scenarios']}")
        print(f"   Total turns: {epoch_results['aggregate_metrics']['total_turns']}")
        print(f"   Entity recall accuracy: {epoch_results['aggregate_metrics']['entity_recall_accuracy']:.1%}")
        print(f"   Mean processing time: {epoch_results['aggregate_metrics']['mean_processing_time']:.3f}s")
        print(f"   Mean context tokens: {epoch_results['aggregate_metrics']['mean_context_tokens']:.0f}")
        print(f"   Max context tokens: {epoch_results['aggregate_metrics']['max_context_tokens']:.0f}")
        print(f"   Max entities: {epoch_results['aggregate_metrics']['max_entity_count']}")

        return epoch_results

    def run_multi_epoch_training(
        self,
        num_epochs: int = 5,
        scenarios_per_epoch: int = None
    ) -> Dict:
        """
        Run multi-epoch training and track context window scalability.
        """
        print(f"\n{'='*80}")
        print(f"🚀 ENTITY MULTI-EPOCH TRAINING")
        print(f"{'='*80}")
        print(f"   Epochs: {num_epochs}")
        print(f"   Scenarios per epoch: {scenarios_per_epoch or 'All'}")
        print(f"   Corpus: {self.corpus_path}")
        print(f"   Total scenarios available: {len(self.corpus['scenarios'])}")

        training_results = {
            'metadata': {
                'start_time': datetime.now().isoformat(),
                'num_epochs': num_epochs,
                'corpus_path': self.corpus_path,
                'total_scenarios': len(self.corpus['scenarios'])
            },
            'epochs': [],
            'context_window_evolution': [],
            'entity_recall_evolution': []
        }

        for epoch_num in range(1, num_epochs + 1):
            # Run epoch
            epoch_results = self.run_epoch(epoch_num, scenarios_to_run=None)
            training_results['epochs'].append(epoch_results)

            # Track evolution
            training_results['context_window_evolution'].append({
                'epoch': epoch_num,
                'mean_tokens': epoch_results['aggregate_metrics']['mean_context_tokens'],
                'max_tokens': epoch_results['aggregate_metrics']['max_context_tokens'],
                'max_entities': epoch_results['aggregate_metrics']['max_entity_count']
            })

            training_results['entity_recall_evolution'].append({
                'epoch': epoch_num,
                'accuracy': epoch_results['aggregate_metrics']['entity_recall_accuracy']
            })

        # Final summary
        training_results['metadata']['end_time'] = datetime.now().isoformat()
        training_results['summary'] = {
            'final_accuracy': training_results['entity_recall_evolution'][-1]['accuracy'],
            'mean_accuracy': sum(e['accuracy'] for e in training_results['entity_recall_evolution']) / num_epochs,
            'accuracy_improvement': (
                training_results['entity_recall_evolution'][-1]['accuracy'] -
                training_results['entity_recall_evolution'][0]['accuracy']
            ),
            'final_max_context_tokens': training_results['context_window_evolution'][-1]['max_tokens'],
            'context_window_growth': (
                training_results['context_window_evolution'][-1]['max_tokens'] -
                training_results['context_window_evolution'][0]['max_tokens']
            )
        }

        print(f"\n{'='*80}")
        print(f"🎉 TRAINING COMPLETE")
        print(f"{'='*80}")
        print(f"   Final entity recall accuracy: {training_results['summary']['final_accuracy']:.1%}")
        print(f"   Mean accuracy: {training_results['summary']['mean_accuracy']:.1%}")
        print(f"   Accuracy improvement: {training_results['summary']['accuracy_improvement']:+.1%}")
        print(f"   Final max context tokens: {training_results['summary']['final_max_context_tokens']:.0f}")
        print(f"   Context window growth: {training_results['summary']['context_window_growth']:+.0f} tokens")

        # Save results
        output_path = self.results_dir / f"entity_epoch_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_path, 'w') as f:
            json.dump(training_results, f, indent=2)

        print(f"\n💾 Results saved: {output_path}")

        return training_results


def main():
    """Run entity epoch training with context window testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Entity Memory Epoch Training')
    parser.add_argument('--epochs', type=int, default=5, help='Number of epochs (default: 5)')
    parser.add_argument('--corpus', type=str,
                       default='knowledge_base/entity_memory_training_pairs.json',
                       help='Path to entity training corpus')
    parser.add_argument('--results-dir', type=str,
                       default='results/entity_training',
                       help='Directory for results')

    args = parser.parse_args()

    # Initialize trainer
    trainer = EntityEpochTrainer(
        corpus_path=args.corpus,
        results_dir=args.results_dir
    )

    # Run training
    results = trainer.run_multi_epoch_training(num_epochs=args.epochs)

    # Print final summary
    print(f"\n{'='*80}")
    print(f"📈 CONTEXT WINDOW SCALABILITY ANALYSIS")
    print(f"{'='*80}")

    for i, cw in enumerate(results['context_window_evolution'], 1):
        print(f"   Epoch {i}: mean={cw['mean_tokens']:.0f} tokens, "
              f"max={cw['max_tokens']:.0f} tokens, "
              f"entities={cw['max_entities']}")

    print(f"\n{'='*80}")
    print(f"📈 ENTITY RECALL ACCURACY EVOLUTION")
    print(f"{'='*80}")

    for i, er in enumerate(results['entity_recall_evolution'], 1):
        print(f"   Epoch {i}: {er['accuracy']:.1%}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
