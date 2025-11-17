"""
Turn-by-Turn Pattern Learning Training
======================================

Grows organism intelligence from the ground up through:
1. Multi-turn conversations with delayed feedback
2. Pattern learner accumulation (nexus signature → phrase → quality)
3. Organic emission evolution (0% → 60%+ over 20 epochs)
4. Stable communicational foundation for diverse domain generalization

CURRICULUM DESIGN (from EMISSION_ARCHITECTURE_INTEGRATION_ANALYSIS_NOV17_2025.md):

Stage 1 (Epochs 1-5): THERAPEUTIC PRIMITIVES
- Crisis response patterns (NDAM + EO + BOND coalitions)
- De-escalation phrases (sympathetic → ventral vagal)
- Grounding techniques (PRESENCE + temporal_grounding)
- Goal: 10-30 stable patterns, quality 0.3-0.5
- Foundation: Basic emotional attunement phrases

Stage 2 (Epochs 5-10): RELATIONAL DEPTH
- Empathic resonance patterns (EMPATHY + LISTENING)
- Boundary-holding phrases (AUTHENTICITY + BOND)
- Wisdom integration (WISDOM + coherence_integration)
- Goal: 30-60 patterns, quality 0.4-0.6
- Foundation: Relationship-building communication

Stage 3 (Epochs 10-20): TRANSFORMATION PATTERNS
- Crisis → recovery trajectories (RESTORATIVE fingerprint)
- Shadow integration sequences (Zone 4 → Zone 3)
- Stable maintenance phrases (STABLE/ATTRACTING regimes)
- Goal: 60-120 patterns, quality 0.5-0.7
- Foundation: Change-oriented therapeutic language

Stage 4 (Epochs 20+): GENERALIZATION
- Cross-context pattern application
- Personality emergence (Zipf's law, R² > 0.85)
- Domain transfer readiness
- Goal: 120-200+ patterns, quality 0.6-0.8
- Foundation: Mature, adaptable communication

EXPECTED ORGANIC EMISSION EVOLUTION:
- Epochs 1-5:   0-10% (learning primitives)
- Epochs 5-10:  10-30% (relational foundation)
- Epochs 10-20: 30-60% (transformation competence)
- Epochs 20+:   60-80% (mature intelligence)

Author: DAE_HYPHAE_1 Curriculum Design
Date: November 17, 2025
"""

import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


def expand_pair_to_multi_turn_conversation(
    pair: Dict[str, Any],
    num_turns: int = 3
) -> List[Dict[str, Any]]:
    """
    Expand a single training pair into a multi-turn conversation.

    Strategy:
    - Turn 1: User input (high urgency/need)
    - Turn 2: Organism response → User shows slight improvement
    - Turn 3: Further response → User shows continued improvement
    - ...

    Satisfaction trajectory examples:
    - RESTORATIVE: 0.25 → 0.40 → 0.60 → 0.75 (crisis → recovery)
    - CONCRESCENT: 0.50 → 0.65 → 0.75 → 0.85 (sustained growth)
    - PLATEAUED: 0.60 → 0.65 → 0.70 → 0.70 (stable maintenance)
    """

    category = pair.get('category', 'unknown')
    expected_felt_state = pair.get('expected_felt_state', {})
    initial_urgency = expected_felt_state.get('urgency', 0.5)
    initial_zone = expected_felt_state.get('zone', 3)

    # Determine satisfaction trajectory based on category
    if category in ['high_urgency', 'crisis']:
        # RESTORATIVE pattern: Crisis → recovery
        trajectory = 'RESTORATIVE'
        base_satisfaction = 0.25
        improvement_per_turn = 0.15
    elif category in ['moderate_stress', 'shadow_integration']:
        # CONCRESCENT pattern: Sustained growth
        trajectory = 'CONCRESCENT'
        base_satisfaction = 0.50
        improvement_per_turn = 0.10
    elif category in ['de_escalation', 'protective_boundary']:
        # PLATEAUED pattern: Stable maintenance
        trajectory = 'PLATEAUED'
        base_satisfaction = 0.60
        improvement_per_turn = 0.05
    else:
        # Default: Moderate improvement
        trajectory = 'MODERATE'
        base_satisfaction = 0.50
        improvement_per_turn = 0.08

    # Generate multi-turn conversation
    turns = []
    for turn_idx in range(num_turns):
        if turn_idx == 0:
            # Turn 1: Original user input
            turn_input = pair['user_input']
            satisfaction = base_satisfaction
        else:
            # Subsequent turns: Continuations showing improvement
            turn_input = generate_followup_input(
                pair['user_input'],
                pair['expected_response'],
                turn_idx,
                trajectory,
                initial_urgency,
                initial_zone
            )
            satisfaction = min(0.95, base_satisfaction + (improvement_per_turn * turn_idx))

        turns.append({
            'turn': turn_idx + 1,
            'input': turn_input,
            'expected_satisfaction': satisfaction,
            'trajectory': trajectory,
            'urgency': max(0.1, initial_urgency * (1.0 - turn_idx * 0.2)),  # Decrease urgency
            'zone': max(1, initial_zone - turn_idx) if initial_zone >= 3 else initial_zone  # Improve zone
        })

    return turns


def generate_followup_input(
    original_input: str,
    expected_response: str,
    turn_idx: int,
    trajectory: str,
    initial_urgency: float,
    initial_zone: int
) -> str:
    """
    Generate follow-up user inputs that show progression.

    Uses template-based generation for consistency and learning signal clarity.
    """

    if trajectory == 'RESTORATIVE':
        # Crisis → recovery progression
        followups = [
            f"That helps a little... I can feel myself breathing more deeply",
            f"I'm starting to feel more grounded. This sense of panic is easing",
            f"Thank you. I feel like I can face this now. The terror has softened"
        ]
    elif trajectory == 'CONCRESCENT':
        # Sustained growth progression
        followups = [
            f"This resonates deeply. I want to explore this further",
            f"I'm noticing more clarity emerging. This feels important",
            f"This understanding feels transformative. I'm integrating this"
        ]
    elif trajectory == 'PLATEAUED':
        # Stable maintenance progression
        followups = [
            f"Yes, that's helpful. I feel steady",
            f"This feels right. I'm in a good place with this",
            f"Thank you. I feel complete with this for now"
        ]
    else:
        # Default progression
        followups = [
            f"I appreciate that. This is helping",
            f"That makes sense. I feel better about this",
            f"Thank you. This conversation has been valuable"
        ]

    # Return appropriate followup for turn index
    return followups[min(turn_idx - 1, len(followups) - 1)]


def run_turn_by_turn_epoch(
    organism: ConversationalOrganismWrapper,
    training_pairs: List[Dict[str, Any]],
    epoch: int,
    total_epochs: int,
    turns_per_conversation: int = 3
) -> Dict[str, Any]:
    """
    Run one epoch with turn-by-turn conversations and delayed feedback.

    Key Innovation:
    - Turn N: Emit phrase, store for feedback
    - Turn N+1: User satisfaction updates Turn N phrase quality via EMA

    Returns:
        Epoch statistics including pattern database metrics
    """

    print(f"{'=' * 80}")
    print(f"🌀 EPOCH {epoch}/{total_epochs} - Turn-by-Turn Pattern Learning")
    print(f"{'=' * 80}")
    print()

    epoch_stats = {
        'epoch': epoch,
        'total_pairs': len(training_pairs),
        'total_turns': 0,
        'processed_turns': 0,
        'satisfaction_scores': [],
        'urgency_scores': [],
        'organic_emissions': 0,
        'llm_emissions': 0,
        'hebbian_emissions': 0,
        'other_emissions': 0,
        'pattern_database_size_start': 0,
        'pattern_database_size_end': 0,
        'mean_pattern_quality_start': 0.0,
        'mean_pattern_quality_end': 0.0,
        'learning_updates': 0,
        'errors': []
    }

    # Get initial pattern database size
    if hasattr(organism.emission_generator, 'pattern_learner'):
        stats = organism.emission_generator.pattern_learner.get_stats()
        epoch_stats['pattern_database_size_start'] = stats['total_phrases']
        epoch_stats['mean_pattern_quality_start'] = stats['mean_phrase_quality']
        print(f"📊 Pattern Database at Epoch Start:")
        print(f"   Total phrases: {stats['total_phrases']}")
        print(f"   Total patterns: {stats['total_patterns']}")
        print(f"   Mean quality: {stats['mean_phrase_quality']:.3f}")
        print()

    # Process each training pair as a multi-turn conversation
    for pair_idx, pair in enumerate(training_pairs, 1):
        pair_id = pair.get('pair_id', f'pair_{pair_idx}')
        category = pair.get('category', 'unknown')

        print(f"{'=' * 60}")
        print(f"[{pair_idx}/{len(training_pairs)}] {pair_id} ({category})")
        print(f"{'=' * 60}")

        # Expand to multi-turn conversation
        conversation_turns = expand_pair_to_multi_turn_conversation(
            pair,
            num_turns=turns_per_conversation
        )

        epoch_stats['total_turns'] += len(conversation_turns)

        # Process conversation turn-by-turn
        for turn_data in conversation_turns:
            turn_num = turn_data['turn']
            user_input = turn_data['input']
            expected_satisfaction = turn_data['expected_satisfaction']

            print(f"\n🔄 Turn {turn_num}/{turns_per_conversation}")
            print(f"   Input: {user_input[:70]}...")
            print(f"   Expected satisfaction: {expected_satisfaction:.3f}")

            try:
                # Process through organism
                result = organism.process_text(
                    text=user_input,
                    context={'turn_number': turn_num, 'pair_id': pair_id},
                    enable_phase2=False,  # Use Phase 1 for faster training
                    user_satisfaction=expected_satisfaction  # ← DELAYED FEEDBACK!
                )

                epoch_stats['processed_turns'] += 1

                # Track emission strategy
                emission_strategy = result.get('emission_strategy', 'unknown')
                if emission_strategy == 'nexus_phrase_learned':
                    epoch_stats['organic_emissions'] += 1
                    print(f"   🌱 ORGANIC EMISSION (pattern learner)")
                elif emission_strategy == 'felt_guided_llm':
                    epoch_stats['llm_emissions'] += 1
                    print(f"   🤖 LLM EMISSION")
                elif emission_strategy == 'hebbian':
                    epoch_stats['hebbian_emissions'] += 1
                    print(f"   📚 HEBBIAN EMISSION")
                else:
                    epoch_stats['other_emissions'] += 1
                    print(f"   ⚙️  {emission_strategy.upper()} EMISSION")

                # Track metrics
                felt_states = result.get('felt_states', {})
                satisfaction = felt_states.get('satisfaction', expected_satisfaction)
                urgency = felt_states.get('urgency', turn_data.get('urgency', 0.5))

                epoch_stats['satisfaction_scores'].append(satisfaction)
                epoch_stats['urgency_scores'].append(urgency)

                # Check if learning update occurred (delayed feedback from previous turn)
                if result.get('learning_update_occurred', False):
                    epoch_stats['learning_updates'] += 1

            except Exception as e:
                print(f"   ❌ Error: {e}")
                epoch_stats['errors'].append({
                    'pair_id': pair_id,
                    'turn': turn_num,
                    'error': str(e)
                })

    # Get final pattern database size
    if hasattr(organism.emission_generator, 'pattern_learner'):
        stats = organism.emission_generator.pattern_learner.get_stats()
        epoch_stats['pattern_database_size_end'] = stats['total_phrases']
        epoch_stats['mean_pattern_quality_end'] = stats['mean_phrase_quality']

        print(f"\n📊 Pattern Database at Epoch End:")
        print(f"   Total phrases: {stats['total_phrases']} (+{stats['total_phrases'] - epoch_stats['pattern_database_size_start']})")
        print(f"   Mean quality: {stats['mean_phrase_quality']:.3f} (Δ: {stats['mean_phrase_quality'] - epoch_stats['mean_pattern_quality_start']:+.3f})")
        print()

    # Calculate organic emission rate
    total_emissions = (epoch_stats['organic_emissions'] + epoch_stats['llm_emissions'] +
                       epoch_stats['hebbian_emissions'] + epoch_stats['other_emissions'])
    organic_rate = (epoch_stats['organic_emissions'] / total_emissions * 100) if total_emissions > 0 else 0.0

    print(f"\n{'=' * 80}")
    print(f"📊 EPOCH {epoch} SUMMARY")
    print(f"{'=' * 80}")
    print()
    print(f"✅ Processed: {epoch_stats['processed_turns']}/{epoch_stats['total_turns']} turns")
    print()
    print(f"🌱 Organic Emission Evolution:")
    print(f"   Organic (pattern learner): {epoch_stats['organic_emissions']} ({organic_rate:.1f}%)")
    print(f"   LLM: {epoch_stats['llm_emissions']}")
    print(f"   Hebbian: {epoch_stats['hebbian_emissions']}")
    print(f"   Other: {epoch_stats['other_emissions']}")
    print()
    print(f"📚 Pattern Learning:")
    print(f"   Database growth: {epoch_stats['pattern_database_size_start']} → {epoch_stats['pattern_database_size_end']} (+{epoch_stats['pattern_database_size_end'] - epoch_stats['pattern_database_size_start']} phrases)")
    print(f"   Quality evolution: {epoch_stats['mean_pattern_quality_start']:.3f} → {epoch_stats['mean_pattern_quality_end']:.3f} (Δ: {epoch_stats['mean_pattern_quality_end'] - epoch_stats['mean_pattern_quality_start']:+.3f})")
    print(f"   Learning updates: {epoch_stats['learning_updates']}")
    print()
    print(f"📈 Satisfaction:")
    mean_sat = np.mean(epoch_stats['satisfaction_scores']) if epoch_stats['satisfaction_scores'] else 0.0
    std_sat = np.std(epoch_stats['satisfaction_scores']) if epoch_stats['satisfaction_scores'] else 0.0
    print(f"   Mean: {mean_sat:.3f} ± {std_sat:.3f}")
    print()

    if epoch_stats['errors']:
        print(f"⚠️  Errors: {len(epoch_stats['errors'])}")
        print()

    epoch_stats['organic_rate'] = organic_rate
    epoch_stats['mean_satisfaction'] = mean_sat

    return epoch_stats


def main():
    """Run turn-by-turn pattern learning training."""

    import argparse
    parser = argparse.ArgumentParser(description='Turn-by-Turn Pattern Learning Training')
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs to run')
    parser.add_argument('--turns-per-conversation', type=int, default=3, help='Number of turns per conversation')
    parser.add_argument('--save-results', type=str, default='results/turn_by_turn_learning', help='Results directory')
    args = parser.parse_args()

    print(f"\n{'=' * 80}")
    print(f"🌀 TURN-BY-TURN PATTERN LEARNING TRAINING")
    print(f"   Curriculum: Stable Communicational Foundation → Diverse Domain Generalization")
    print(f"   Epochs: {args.epochs}")
    print(f"   Turns per conversation: {args.turns_per_conversation}")
    print(f"{'=' * 80}\n")

    # Verify INTELLIGENCE_EMERGENCE_MODE enabled
    if not Config.INTELLIGENCE_EMERGENCE_MODE:
        print("⚠️  WARNING: INTELLIGENCE_EMERGENCE_MODE is disabled")
        print("   Pattern learner will compete with felt-guided LLM")
        print("   Set INTELLIGENCE_EMERGENCE_MODE = True in config.py for pure organic learning")
        print()

    # Load training data
    print("📚 Loading training corpus...")
    crisis_path = Path(__file__).parent.parent / "knowledge_base" / "crisis_urgency_training_pairs.json"
    shadow_path = Path(__file__).parent.parent / "knowledge_base" / "shadow_exile_training_pairs.json"

    with open(crisis_path, 'r') as f:
        crisis_data = json.load(f)
    with open(shadow_path, 'r') as f:
        shadow_data = json.load(f)

    training_pairs = crisis_data['training_pairs'] + shadow_data['training_pairs']
    print(f"   ✅ Loaded {len(training_pairs)} training pairs")
    print(f"      • Crisis/Urgency: {len(crisis_data['training_pairs'])} pairs")
    print(f"      • Shadow/Exile: {len(shadow_data['training_pairs'])} pairs")
    print()

    # Initialize organism
    print("🌀 Initializing organism...")
    organism = ConversationalOrganismWrapper()
    print()

    # Run training epochs
    all_epoch_stats = []
    for epoch in range(1, args.epochs + 1):
        epoch_stats = run_turn_by_turn_epoch(
            organism=organism,
            training_pairs=training_pairs,
            epoch=epoch,
            total_epochs=args.epochs,
            turns_per_conversation=args.turns_per_conversation
        )
        all_epoch_stats.append(epoch_stats)

    # Final summary
    print(f"\n{'=' * 80}")
    print(f"🎉 TRAINING COMPLETE")
    print(f"{'=' * 80}\n")

    print(f"📈 Organic Emission Evolution:")
    for i, stats in enumerate(all_epoch_stats, 1):
        print(f"   Epoch {i:2d}: {stats['organic_rate']:5.1f}% organic ({stats['pattern_database_size_end']:3d} phrases, quality: {stats['mean_pattern_quality_end']:.3f})")

    # Save results
    results_dir = Path(args.save_results)
    results_dir.mkdir(parents=True, exist_ok=True)

    results_path = results_dir / f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_path, 'w') as f:
        json.dump({
            'config': {
                'epochs': args.epochs,
                'turns_per_conversation': args.turns_per_conversation,
                'intelligence_emergence_mode': Config.INTELLIGENCE_EMERGENCE_MODE,
                'training_pairs': len(training_pairs)
            },
            'epoch_stats': all_epoch_stats
        }, f, indent=2)

    print(f"\n💾 Results saved to: {results_path}")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
