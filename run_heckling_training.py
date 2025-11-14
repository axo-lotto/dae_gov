#!/usr/bin/env python3
"""
Heckling Corpus Training with Transductive Self-Governance Testing
===================================================================

Trains the organism on the 35-example heckling corpus and verifies:
1. Heckling intelligence classification accuracy
2. Transductive self-governance aggregation (k≥10)
3. Milestone detection
4. Organism-level learning

Phase: 1.5H + 1.6 Integration Test
Date: November 14, 2025
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Set PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def run_heckling_training():
    """Run training on heckling corpus and analyze transductive aggregation."""

    print("="*80)
    print("HECKLING CORPUS TRAINING + TRANSDUCTIVE SELF-GOVERNANCE TEST")
    print("="*80)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load heckling corpus
    corpus_path = Path("knowledge_base/heckling_training_corpus.json")
    print(f"📖 Loading heckling corpus: {corpus_path}")

    with open(corpus_path, 'r') as f:
        corpus = json.load(f)

    total_examples = corpus['metadata']['total_examples']
    print(f"   Total examples: {total_examples}")
    print(f"   Categories: {len(corpus['categories'])}")
    print()

    # Initialize organism
    print("🌀 Initializing organism...")
    organism = ConversationalOrganismWrapper()
    print()

    # Training results
    results = []
    heckling_classifications = {
        'GENUINE_CRISIS': 0,
        'HARMFUL_AGGRESSION': 0,
        'PLAYFUL_PROVOCATION': 0,
        'INTELLECTUAL_HECKLING': 0,
        'ABSURDIST_HUMOR': 0,
        'SAFE_CONVERSATION': 0
    }

    correct_classifications = 0
    total_classifications = 0

    # Process each example
    print("🎓 Processing heckling corpus examples...\n")

    for category_data in corpus['categories']:
        category = category_data['category']
        print(f"\n{'─'*80}")
        print(f"Category: {category} ({category_data['count']} examples)")
        print(f"{'─'*80}\n")

        for example in category_data['examples']:
            example_id = example['id']
            user_input = example['user_input']
            expected_intent = example['intent']

            print(f"Example {example_id}:")
            print(f"  Input: \"{user_input[:60]}...\"" if len(user_input) > 60 else f"  Input: \"{user_input}\"")

            # Process through organism
            result = organism.process_text(
                text=user_input,
                context={
                    'conversation_id': f'heckling_training_{example_id}',
                    'user_id': f'training_user_{example_id[:10]}',  # Mock user ID for transductive aggregation
                    'training_phase': 'heckling_corpus'
                },
                enable_tsk_recording=True,
                enable_phase2=True
            )

            # Extract heckling assessment
            felt_states = result.get('felt_states', {})
            heckling_data = felt_states.get('heckling_assessment', {})

            if heckling_data:
                detected_intent = heckling_data.get('intent', 'UNKNOWN')
                is_crisis = heckling_data.get('is_genuine_crisis', False)
                is_heckling = heckling_data.get('is_heckling', False)
                safe_for_banter = heckling_data.get('safe_for_banter', False)

                print(f"  Detected: {detected_intent}")
                print(f"  Expected: {expected_intent}")
                print(f"  Crisis: {is_crisis}, Heckling: {is_heckling}, Safe for banter: {safe_for_banter}")

                # Track classification
                heckling_classifications[detected_intent] = heckling_classifications.get(detected_intent, 0) + 1

                # Check accuracy (case-insensitive matching)
                if detected_intent.lower().replace('_', ' ') == expected_intent.lower().replace('_', ' '):
                    correct_classifications += 1
                    print("  ✅ Correct classification")
                else:
                    print(f"  ❌ Misclassification (expected: {expected_intent})")

                total_classifications += 1
            else:
                print("  ⚠️  No heckling assessment generated")

            # Store result
            results.append({
                'example_id': example_id,
                'category': category,
                'user_input': user_input,
                'expected_intent': expected_intent,
                'detected_intent': heckling_data.get('intent', 'NONE') if heckling_data else 'NONE',
                'is_crisis': heckling_data.get('is_genuine_crisis', False) if heckling_data else False,
                'is_heckling': heckling_data.get('is_heckling', False) if heckling_data else False,
                'ndam_urgency': felt_states.get('ndam_urgency', 0.0),
                'v0_descent': felt_states.get('v0_descent', 0.0),
                'convergence_cycles': felt_states.get('convergence_cycles', 0),
                'emission_confidence': felt_states.get('emission_confidence', 0.0)
            })

            print()

    # Summary statistics
    print("\n" + "="*80)
    print("TRAINING SUMMARY")
    print("="*80 + "\n")

    print(f"Total examples processed: {len(results)}")
    print(f"Heckling assessments generated: {total_classifications}")
    print(f"Classification accuracy: {correct_classifications}/{total_classifications} ({correct_classifications/total_classifications*100:.1f}%)" if total_classifications > 0 else "No classifications")
    print()

    print("Intent Distribution:")
    for intent, count in sorted(heckling_classifications.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {intent}: {count}")
    print()

    # Transductive Self-Governance Summary
    print("="*80)
    print("TRANSDUCTIVE SELF-GOVERNANCE STATE")
    print("="*80 + "\n")

    if hasattr(organism, 'transductive_monitor') and organism.transductive_monitor:
        summary = organism.transductive_monitor.get_current_state_summary()

        if summary.get('status') == 'Operational':
            print(f"✅ Transductive monitoring OPERATIONAL")
            print(f"\nTotal occasions processed: {summary['total_occasions_processed']}")
            print(f"Unique users: {summary['total_unique_users']}")
            print(f"Milestones achieved: {summary['milestones_achieved']}")
            print()

            # Latest snapshot
            snapshot = summary.get('latest_snapshot', {})
            if snapshot:
                print("Latest Aggregate Snapshot:")
                print(f"  Timestamp: {snapshot['timestamp']}")
                print(f"  Cohort size: {snapshot['cohort_size']}")
                print(f"  Mean V0 descent: {snapshot['mean_v0_descent']}")
                print(f"  Mean convergence cycles: {snapshot['mean_convergence_cycles']}")
                print(f"  Kairos rate: {snapshot['kairos_rate']}")
                print(f"  Mean emission confidence: {snapshot['mean_emission_confidence']}")
                print(f"  Crisis rate: {snapshot['crisis_rate']}")
                print(f"  Heckling rate: {snapshot['heckling_rate']}")
                print()

                print("Zone Distribution:")
                for zone, proportion in snapshot['zone_distribution'].items():
                    print(f"  Zone {zone}: {proportion}")
                print()

            # Milestones
            milestones = summary.get('latest_milestones', [])
            if milestones:
                print("Developmental Milestones:")
                for m in milestones:
                    print(f"  • {m['description']} ({m['timestamp']})")
                print()

            # Organism learning
            organism_learning = summary.get('organism_learning', {})
            if organism_learning:
                print("Organism-Level Learning:")
                for key, value in organism_learning.items():
                    print(f"  {key}: {value:.3f}")
                print()

            # Self-insights
            insights = summary.get('self_insights', [])
            if insights:
                print("Self-Reflexive Insights:")
                for insight in insights:
                    print(f"  • {insight}")
                print()
        else:
            print(f"⏳ Status: {summary['status']}")
            print(f"   Buffered occasions: {summary.get('buffered_occasions', 0)}")
            print(f"   Need {summary.get('min_cohort_size', 10)} for first aggregation")
            print()
    else:
        print("⚠️  Transductive self-governance not available")
        print()

    # Save results
    output_path = Path("results/heckling_training_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'corpus_path': str(corpus_path),
            'total_examples': len(results),
            'classification_accuracy': correct_classifications / total_classifications if total_classifications > 0 else 0.0
        },
        'intent_distribution': heckling_classifications,
        'transductive_summary': organism.transductive_monitor.get_current_state_summary() if hasattr(organism, 'transductive_monitor') and organism.transductive_monitor else {},
        'results': results
    }

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"💾 Results saved to: {output_path}")
    print()

    # Check transductive state file
    tsk_state_path = Path("TSK/transductive_self_state.json")
    if tsk_state_path.exists():
        print(f"✅ Transductive state saved to: {tsk_state_path}")
        with open(tsk_state_path, 'r') as f:
            tsk_state = json.load(f)
        print(f"   Total occasions: {tsk_state.get('total_occasions_processed', 0)}")
        print(f"   Unique users: {tsk_state.get('total_unique_users', 0)}")
        print(f"   Historical snapshots: {len(tsk_state.get('historical_snapshots', []))}")
        print(f"   Milestones: {len(tsk_state.get('milestones', []))}")
    else:
        print(f"⏳ Transductive state not yet saved (waiting for k≥10)")

    print("\n" + "="*80)
    print("TRAINING COMPLETE")
    print("="*80)


if __name__ == '__main__':
    run_heckling_training()
