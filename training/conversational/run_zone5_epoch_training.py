"""
Zone 5 Epoch Training - Organic Learning of Transductive Patterns
==================================================================

Train DAE organism to learn Zone 5 (dorsal collapse) transductive intelligence
through organic epoch learning with 15 collapse scenarios.

Date: November 13, 2025
"""

import sys
import os
import json
from datetime import datetime

# Add project to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def run_zone5_training(num_epochs=3):
    """
    Run Zone 5 epoch training on collapse scenarios.

    Args:
        num_epochs: Number of training epochs (default: 3)
    """

    print("="*80)
    print("🌊 Zone 5 Epoch Training - Transductive Pattern Learning")
    print("="*80)
    print()

    # Load Zone 5 training pairs
    training_file = "knowledge_base/zone_5_training_pairs.json"
    with open(training_file, 'r') as f:
        data = json.load(f)

    training_pairs = data['pairs']
    print(f"📚 Loaded {len(training_pairs)} Zone 5 training pairs")
    print(f"📊 Categories: {len(set(p['category'] for p in training_pairs))}")
    print()

    # Initialize organism
    print("Initializing organism...")
    organism = ConversationalOrganismWrapper()
    print()

    # Training results storage
    all_results = {
        'metadata': {
            'training_date': datetime.now().isoformat(),
            'num_epochs': num_epochs,
            'num_pairs': len(training_pairs),
            'training_file': training_file
        },
        'epochs': []
    }

    # Run epochs
    for epoch in range(1, num_epochs + 1):
        print(f"\n{'='*80}")
        print(f"📖 EPOCH {epoch}/{num_epochs}")
        print(f"{'='*80}\n")

        epoch_results = []

        for i, pair in enumerate(training_pairs, 1):
            user_input = pair['user_input']
            ideal_emission = pair['ideal_emission']
            pair_id = pair['id']
            category = pair['category']
            expected_nexuses = pair['context']['expected_nexuses']

            print(f"[{i}/{len(training_pairs)}] {pair_id} ({category})")
            print(f"  Input: \"{user_input[:60]}...\"")

            try:
                # Process through organism
                result = organism.process_text(user_input)

                # Extract results
                emission = result.get('emission_text', '')
                confidence = result.get('emission_confidence', 0)
                path = result.get('emission_path', 'unknown')
                zone_id = result.get('zone_id', 0)
                zone = result.get('zone', 'unknown')

                # Analyze transductive pathway usage
                felt_states = result.get('felt_states', {})
                organ_results = result.get('organ_results', {})

                # Check if expected nexuses were activated
                # (This would require exposing nexus data from reconstruction pipeline)

                print(f"  Zone: {zone} (Zone {zone_id})")
                print(f"  Path: {path}")
                print(f"  Confidence: {confidence:.3f}")
                print(f"  Emission: \"{emission[:80]}...\"")

                # Store result
                epoch_results.append({
                    'pair_id': pair_id,
                    'category': category,
                    'user_input': user_input,
                    'ideal_emission': ideal_emission,
                    'actual_emission': emission,
                    'zone_detected': zone_id,
                    'confidence': confidence,
                    'path': path,
                    'expected_nexuses': expected_nexuses
                })

            except Exception as e:
                print(f"  ❌ ERROR: {e}")
                import traceback
                traceback.print_exc()

            print()

        # Store epoch results
        all_results['epochs'].append({
            'epoch_number': epoch,
            'pairs_processed': len(epoch_results),
            'results': epoch_results
        })

        # Epoch summary
        zone5_detected = sum(1 for r in epoch_results if r['zone_detected'] == 5)
        avg_confidence = sum(r['confidence'] for r in epoch_results) / len(epoch_results) if epoch_results else 0

        print(f"\n📊 Epoch {epoch} Summary:")
        print(f"  Pairs processed: {len(epoch_results)}/{len(training_pairs)}")
        print(f"  Zone 5 detected: {zone5_detected}/{len(epoch_results)}")
        print(f"  Avg confidence: {avg_confidence:.3f}")

    # Save results
    output_file = f"results/zone5_epoch_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs("results", exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ Zone 5 Training Complete!")
    print(f"📁 Results saved to: {output_file}")
    print(f"{'='*80}\n")

    return all_results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Zone 5 Epoch Training")
    parser.add_argument('--epochs', type=int, default=3, help="Number of training epochs")

    args = parser.parse_args()

    run_zone5_training(num_epochs=args.epochs)
