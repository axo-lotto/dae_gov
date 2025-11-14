#!/usr/bin/env python3
"""
Feedback Analysis Tool
Analyzes collected user feedback to identify improvement areas

Features:
- Global and per-user statistics
- Not helpful examples for debugging
- Tone/personality calibration insights
- Trend analysis over time

Author: Claude Code (November 2025)
Status: Production Ready
"""

import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.feedback_collector import FeedbackCollector
from persona_layer.user_registry import UserRegistry


def analyze_feedback():
    """Analyze all collected feedback."""

    collector = FeedbackCollector()
    registry = UserRegistry()
    feedback = collector.feedback

    if not feedback:
        print("⚠️  No feedback collected yet")
        print("\nTo collect feedback:")
        print("  1. Run: python3 dae_interactive.py")
        print("  2. Have a conversation")
        print("  3. Rate responses with 1/2/3")
        print("  4. Run this script again")
        return

    print("\n" + "="*80)
    print("📊 FEEDBACK ANALYSIS REPORT")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Global stats
    global_stats = collector.get_global_stats()

    print(f"\n{'='*80}")
    print("GLOBAL STATISTICS")
    print(f"{'='*80}")
    print(f"\n📈 Overall Performance:")
    print(f"   Total Ratings: {global_stats['total_ratings']}")
    print(f"   Unique Users: {global_stats['unique_users']}")
    print(f"   Helpful Rate: {global_stats['helpful_rate']*100:.1f}%")
    print(f"\n   Ratings Breakdown:")
    print(f"     ⭐ Excellent: {global_stats['excellent']} ({global_stats['excellent']/global_stats['total_ratings']*100:.1f}%)")
    print(f"     👍 Helpful: {global_stats['helpful']} ({global_stats['helpful']/global_stats['total_ratings']*100:.1f}%)")
    print(f"     👎 Not Helpful: {global_stats['not_helpful']} ({global_stats['not_helpful']/global_stats['total_ratings']*100:.1f}%)")

    # Per-user stats
    users = set(f['user_id'] for f in feedback.values())

    print(f"\n{'='*80}")
    print(f"PER-USER STATISTICS ({len(users)} users)")
    print(f"{'='*80}")
    for user_id in users:
        user_stats = collector.get_user_feedback_stats(user_id)
        user_data = registry.get_user(user_id)
        username = user_data['username'] if user_data else user_id

        print(f"\n👤 {username}:")
        print(f"   Total ratings: {user_stats['total_ratings']}")
        print(f"   Helpful rate: {user_stats['helpful_rate']*100:.1f}%")
        print(f"   Excellent rate: {user_stats['excellent_rate']*100:.1f}%")
        print(f"   Breakdown: {user_stats['excellent']}⭐ / {user_stats['helpful']}👍 / {user_stats['not_helpful']}👎")

    # Not helpful analysis
    not_helpful = collector.get_not_helpful_examples(limit=10)

    if not_helpful:
        print(f"\n{'='*80}")
        print(f"⚠️  NOT HELPFUL RESPONSES ({len(not_helpful)} total, showing top 10)")
        print(f"{'='*80}")
        for i, f in enumerate(not_helpful[:10], 1):
            print(f"\n📌 Example {i}:")
            print(f"   User Input: \"{f['user_input'][:70]}...\"" if len(f['user_input']) > 70 else f"   User Input: \"{f['user_input']}\"")
            print(f"   Emission: \"{f['emission'][:70]}...\"" if len(f['emission']) > 70 else f"   Emission: \"{f['emission']}\"")
            if f.get('comment'):
                print(f"   💬 Comment: {f['comment']}")
            if f.get('metadata'):
                print(f"   📊 Metadata: conf={f['metadata'].get('confidence', 'N/A'):.3f}, " +
                     f"nexuses={f['metadata'].get('nexuses', 'N/A')}, " +
                     f"strategy={f['metadata'].get('strategy', 'N/A')}")

    # Tone/personality analysis
    print(f"\n{'='*80}")
    print("🎭 TONE & PERSONALITY CALIBRATION")
    print(f"{'='*80}")

    tone_analysis = collector.analyze_tone_patterns()

    if tone_analysis['status'] == 'analyzed':
        print(f"\n📝 Tone Mentions:")
        print(f"   Playful/humorous: {tone_analysis.get('playful_mentions', 0)}")
        print(f"   Too serious/clinical: {tone_analysis.get('serious_mentions', 0)}")
        print(f"   Warm/grounding: {tone_analysis.get('warm_mentions', 0)}")

        insights = tone_analysis.get('insights', [])
        if insights:
            print(f"\n💡 Key Insights:")
            for insight in insights:
                print(f"   {insight}")
    else:
        print("\n⚠️  Not enough tone feedback yet")
        print("   Encourage users to leave comments on excellent ratings!")

    # Strategy analysis
    print(f"\n{'='*80}")
    print("🔧 EMISSION STRATEGY ANALYSIS")
    print(f"{'='*80}")

    strategies = Counter()
    strategy_ratings = {}

    for f in feedback.values():
        strategy = f.get('metadata', {}).get('strategy', 'unknown')
        strategies[strategy] += 1

        if strategy not in strategy_ratings:
            strategy_ratings[strategy] = {'excellent': 0, 'helpful': 0, 'not_helpful': 0}

        strategy_ratings[strategy][f['rating']] += 1

    print(f"\n📊 Strategy Usage:")
    for strategy, count in strategies.most_common():
        ratings = strategy_ratings[strategy]
        total = sum(ratings.values())
        helpful_rate = (ratings['excellent'] + ratings['helpful']) / total if total > 0 else 0

        print(f"\n   {strategy}: {count} uses")
        print(f"      Helpful rate: {helpful_rate*100:.1f}%")
        print(f"      Breakdown: {ratings['excellent']}⭐ / {ratings['helpful']}👍 / {ratings['not_helpful']}👎")

    # Recommendations
    print(f"\n{'='*80}")
    print("💡 RECOMMENDATIONS")
    print(f"{'='*80}")

    if global_stats['helpful_rate'] >= 0.7:
        print("\n✅ System performing well (>70% helpful rate)")
    elif global_stats['helpful_rate'] >= 0.5:
        print("\n⚠️  System performance moderate (50-70% helpful rate)")
        print("   Consider:")
        print("   - Reviewing not_helpful examples")
        print("   - Adjusting emission strategies")
        print("   - Collecting more feedback for patterns")
    else:
        print("\n❌ System needs improvement (<50% helpful rate)")
        print("   Priority actions:")
        print("   - Analyze all not_helpful examples")
        print("   - Identify common failure patterns")
        print("   - Adjust trauma detection thresholds")
        print("   - Review emission generation strategy")

    if global_stats['total_ratings'] < 20:
        print(f"\n📈 Collect more feedback (currently {global_stats['total_ratings']}, target: 50+)")
        print("   More data = better insights!")

    if tone_analysis.get('serious_mentions', 0) > tone_analysis.get('playful_mentions', 0):
        print("\n🎭 Consider adding more warmth/playfulness")
        print("   System may be too clinical/serious")

    print("\n" + "="*80)
    print("End of report")
    print("="*80 + "\n")


if __name__ == '__main__':
    analyze_feedback()
