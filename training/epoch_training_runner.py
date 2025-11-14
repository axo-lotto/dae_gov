"""
Epoch Training Runner - 10-15 Epoch Multi-Iteration Training
=============================================================

Runs complete epoch training with:
- 10-15 epochs
- 4 training regimes (EXPLORING → CONVERGING → STABLE → COMMITTED)
- Multi-iteration training (2-5 iterations per pair)
- DAE 3.0 fractal rewards (R₅/R₆/R₇)
- Intelligence, continuity, and superject dynamic development

Usage:
    # Run complete 15-epoch training
    python3 training/epoch_training_runner.py --epochs 15 --pairs-per-epoch 20

    # Run pilot (1 epoch)
    python3 training/epoch_training_runner.py --epochs 1 --pairs-per-epoch 10

    # Resume from epoch 5
    python3 training/epoch_training_runner.py --start-epoch 6 --epochs 15 --pairs-per-epoch 20

Author: DAE_HYPHAE_1
Date: November 13, 2025
"""

import sys
import json
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_training.epoch_training_orchestrator import EpochTrainingOrchestrator
from config import Config


def load_training_corpus(corpus_path: Path) -> list:
    """Load training corpus from JSON."""
    print(f"📚 Loading training corpus from {corpus_path}")

    if not corpus_path.exists():
        print(f"❌ Training corpus not found: {corpus_path}")
        sys.exit(1)

    with open(corpus_path, 'r') as f:
        data = json.load(f)

    # Extract training pairs
    if isinstance(data, dict) and 'training_pairs' in data:
        pairs = data['training_pairs']
    elif isinstance(data, list):
        pairs = data
    else:
        print(f"❌ Unexpected corpus format: {type(data)}")
        sys.exit(1)

    # Convert to standardized format with pair_id, input_text
    training_pairs = []
    if isinstance(pairs, list):
        # Format: list of dicts with input_text/output_text
        for i, pair in enumerate(pairs):
            pair_id = pair.get('pair_metadata', {}).get('id', f"pair_{i:03d}")
            training_pairs.append({
                'pair_id': pair_id,
                'input_text': pair.get('input_text', pair.get('input', '')),
                'expected_output': pair.get('output_text', pair.get('output', ''))
            })
    elif isinstance(pairs, dict):
        # Format: dict of categories with lists of pairs
        for category_name, category_pairs in pairs.items():
            for pair in category_pairs:
                training_pairs.append({
                    'pair_id': pair.get('id', f"{category_name}_{len(training_pairs)}"),
                    'input_text': pair.get('input', pair.get('input_text', '')),
                    'expected_output': pair.get('expected_output', pair.get('output', ''))
                })
    else:
        print(f"❌ Unexpected pairs format: {type(pairs)}")
        sys.exit(1)

    print(f"✅ Loaded {len(training_pairs)} training pairs")
    print(f"   Categories: {len(pairs)}")

    return training_pairs


def run_epoch_training(
    start_epoch: int = 1,
    end_epoch: int = 15,
    pairs_per_epoch: int = 20,
    corpus_path: Path = None,
    results_dir: Path = None,
    verbose: bool = True
):
    """
    Run complete epoch training.

    Args:
        start_epoch: Starting epoch (1-indexed)
        end_epoch: Ending epoch (inclusive)
        pairs_per_epoch: Number of training pairs per epoch
        corpus_path: Path to training corpus JSON
        results_dir: Directory to save results
        verbose: Print training progress
    """
    print("="*70)
    print("🎓 EPOCH TRAINING - DAE_HYPHAE_1")
    print("="*70)
    print(f"\nTraining Configuration:")
    print(f"   Start epoch: {start_epoch}")
    print(f"   End epoch: {end_epoch}")
    print(f"   Total epochs: {end_epoch - start_epoch + 1}")
    print(f"   Pairs per epoch: {pairs_per_epoch}")
    print(f"   Total conversations: {(end_epoch - start_epoch + 1) * pairs_per_epoch}")

    # Set defaults
    if corpus_path is None:
        corpus_path = Config.CONVERSATIONAL_TRAINING_PAIRS_PATH
    if results_dir is None:
        results_dir = Path("results/epoch_training")

    # Load training corpus
    training_corpus = load_training_corpus(corpus_path)

    if len(training_corpus) < pairs_per_epoch:
        print(f"⚠️  Warning: Corpus size ({len(training_corpus)}) < pairs per epoch ({pairs_per_epoch})")
        print(f"   Using all {len(training_corpus)} pairs per epoch")
        pairs_per_epoch = len(training_corpus)

    # Initialize organism
    print(f"\n{'='*70}")
    print("🌀 Initializing Conversational Organism")
    print(f"{'='*70}")

    organism = ConversationalOrganismWrapper()

    # Initialize epoch training orchestrator
    print(f"\n{'='*70}")
    print("🎓 Initializing Epoch Training Orchestrator")
    print(f"{'='*70}")

    orchestrator = EpochTrainingOrchestrator(
        organism_wrapper=organism,
        results_dir=results_dir,
        global_learning_rate=0.1  # EMA alpha for R₇
    )

    # Print regime schedule
    print(f"\n📅 Training Regime Schedule:")
    for regime in orchestrator.regime_configs:
        print(f"   Epochs {regime.epochs[0]}-{regime.epochs[1]}: {regime.name}")
        print(f"      Tau: {regime.tau_threshold:.2f}, "
              f"Exploration: {regime.exploration_factor:.2f}, "
              f"Max iters: {regime.max_iterations}")
        print(f"      {regime.description}")

    # Run training
    print(f"\n{'='*70}")
    print("🚀 Starting Epoch Training")
    print(f"{'='*70}")

    epoch_results = orchestrator.train_multiple_epochs(
        start_epoch=start_epoch,
        end_epoch=end_epoch,
        training_pairs_per_epoch=pairs_per_epoch,
        training_corpus=training_corpus,
        verbose=verbose
    )

    # Print final summary
    print(f"\n{'='*70}")
    print("🎉 EPOCH TRAINING COMPLETE")
    print(f"{'='*70}")

    final_result = epoch_results[-1]
    print(f"\n📊 Final Metrics (Epoch {final_result.epoch_id}):")
    print(f"   Mean satisfaction: {final_result.mean_satisfaction:.3f}")
    print(f"   Convergence rate: {final_result.convergence_rate:.1%}")
    print(f"   Mean iterations: {final_result.mean_iterations:.2f}")
    print(f"   Families discovered: {final_result.families_discovered}")

    print(f"\n🌀 Global Learning:")
    print(f"   Global confidence (R₇): {orchestrator.global_state.global_confidence:.3f}")
    print(f"   CAGR: {orchestrator.global_state.compound_growth_rate:.1f}%")
    print(f"   Total conversations: {orchestrator.global_state.total_conversations}")

    print(f"\n💾 Results saved to: {results_dir}")
    print(f"   - Global state: global_training_state.json")
    print(f"   - Epoch results: epoch_XXX_result.json")

    return epoch_results, orchestrator


def main():
    """Main entry point for epoch training runner."""
    parser = argparse.ArgumentParser(
        description="Run multi-epoch training for DAE_HYPHAE_1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete 15-epoch training
  python3 training/epoch_training_runner.py --epochs 15 --pairs-per-epoch 20

  # Run 1-epoch pilot
  python3 training/epoch_training_runner.py --epochs 1 --pairs-per-epoch 10

  # Resume from epoch 6
  python3 training/epoch_training_runner.py --start-epoch 6 --epochs 15 --pairs-per-epoch 20

  # Use custom corpus
  python3 training/epoch_training_runner.py --epochs 5 --corpus path/to/corpus.json
        """
    )

    parser.add_argument(
        '--start-epoch',
        type=int,
        default=1,
        help='Starting epoch number (default: 1)'
    )

    parser.add_argument(
        '--epochs',
        type=int,
        default=15,
        help='Ending epoch number (default: 15)'
    )

    parser.add_argument(
        '--pairs-per-epoch',
        type=int,
        default=20,
        help='Number of training pairs per epoch (default: 20)'
    )

    parser.add_argument(
        '--corpus',
        type=Path,
        default=None,
        help='Path to training corpus JSON (default: use Config.CONVERSATIONAL_TRAINING_PAIRS_PATH)'
    )

    parser.add_argument(
        '--results-dir',
        type=Path,
        default=None,
        help='Directory to save results (default: results/epoch_training)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.start_epoch < 1:
        print(f"❌ Error: --start-epoch must be >= 1")
        sys.exit(1)

    if args.epochs < args.start_epoch:
        print(f"❌ Error: --epochs must be >= --start-epoch")
        sys.exit(1)

    if args.pairs_per_epoch < 1:
        print(f"❌ Error: --pairs-per-epoch must be >= 1")
        sys.exit(1)

    # Run training
    try:
        run_epoch_training(
            start_epoch=args.start_epoch,
            end_epoch=args.epochs,
            pairs_per_epoch=args.pairs_per_epoch,
            corpus_path=args.corpus,
            results_dir=args.results_dir,
            verbose=not args.quiet
        )

        print("\n✅ Training completed successfully!")
        sys.exit(0)

    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        sys.exit(130)

    except Exception as e:
        print(f"\n\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
