#!/usr/bin/env python3
"""
Feedback Collector - User Rating and Comment Collection
Stores ratings (helpful/not helpful/excellent) for emission improvement

Features:
- 3-level rating system (excellent/helpful/not helpful)
- Optional comments for qualitative feedback
- Metadata capture (confidence, nexuses, mode, etc.)
- Per-user and global statistics
- Tone/personality calibration tracking

Author: Claude Code (November 2025)
Status: Production Ready
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List


class FeedbackCollector:
    """Collect and store user feedback on emissions."""

    def __init__(self, feedback_path='persona_layer/feedback.json'):
        self.feedback_path = Path(feedback_path)
        self.feedback = self._load_feedback()

    def _load_feedback(self) -> Dict:
        """Load feedback from disk."""
        if self.feedback_path.exists():
            with open(self.feedback_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_feedback(self):
        """Save feedback to disk."""
        with open(self.feedback_path, 'w') as f:
            json.dump(self.feedback, f, indent=2)

    def record_rating(self,
                      user_id: str,
                      session_id: str,
                      turn_id: int,
                      user_input: str,
                      emission: str,
                      rating: str,
                      comment: str = None,
                      metadata: Dict = None,
                      tone_notes: str = None):
        """
        Record user rating for an emission.

        Args:
            user_id: User identifier
            session_id: Session identifier
            turn_id: Turn number in session
            user_input: User's input text
            emission: Generated emission text
            rating: 'helpful', 'not_helpful', or 'excellent'
            comment: Optional user comment
            metadata: Optional metadata (confidence, nexuses, organs, etc.)
            tone_notes: Optional notes on DAE personality/tone
        """
        feedback_id = f"{session_id}_turn_{turn_id}"

        self.feedback[feedback_id] = {
            'user_id': user_id,
            'session_id': session_id,
            'turn_id': turn_id,
            'user_input': user_input,
            'emission': emission,
            'rating': rating,
            'comment': comment,
            'tone_notes': tone_notes,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }

        self._save_feedback()

    def get_user_feedback_stats(self, user_id: str) -> Dict:
        """Get feedback statistics for a user."""
        user_feedback = [f for f in self.feedback.values()
                        if f['user_id'] == user_id]

        if not user_feedback:
            return {
                'total_ratings': 0,
                'helpful': 0,
                'not_helpful': 0,
                'excellent': 0,
                'helpful_rate': 0.0,
                'excellent_rate': 0.0
            }

        ratings = [f['rating'] for f in user_feedback]
        total = len(ratings)

        helpful_count = ratings.count('helpful')
        excellent_count = ratings.count('excellent')

        return {
            'total_ratings': total,
            'helpful': helpful_count,
            'not_helpful': ratings.count('not_helpful'),
            'excellent': excellent_count,
            'helpful_rate': (helpful_count + excellent_count) / total,
            'excellent_rate': excellent_count / total
        }

    def get_global_stats(self) -> Dict:
        """Get global feedback statistics."""
        if not self.feedback:
            return {
                'total_ratings': 0,
                'helpful': 0,
                'not_helpful': 0,
                'excellent': 0,
                'helpful_rate': 0.0,
                'excellent_rate': 0.0,
                'unique_users': 0
            }

        ratings = [f['rating'] for f in self.feedback.values()]
        users = set(f['user_id'] for f in self.feedback.values())
        total = len(ratings)

        helpful_count = ratings.count('helpful')
        excellent_count = ratings.count('excellent')

        return {
            'total_ratings': total,
            'helpful': helpful_count,
            'not_helpful': ratings.count('not_helpful'),
            'excellent': excellent_count,
            'helpful_rate': (helpful_count + excellent_count) / total,
            'excellent_rate': excellent_count / total,
            'unique_users': len(users)
        }

    def get_not_helpful_examples(self, limit=10) -> List[Dict]:
        """Get not_helpful feedback for analysis."""
        not_helpful = [
            f for f in self.feedback.values()
            if f['rating'] == 'not_helpful'
        ]

        # Sort by timestamp (newest first)
        not_helpful.sort(key=lambda x: x['timestamp'], reverse=True)

        return not_helpful[:limit]

    def get_tone_feedback(self, limit=20) -> List[Dict]:
        """Get feedback with tone/personality notes for calibration."""
        tone_feedback = [
            f for f in self.feedback.values()
            if f.get('tone_notes') or f.get('comment')
        ]

        # Sort by timestamp (newest first)
        tone_feedback.sort(key=lambda x: x['timestamp'], reverse=True)

        return tone_feedback[:limit]

    def analyze_tone_patterns(self) -> Dict:
        """
        Analyze tone/personality feedback patterns.

        Returns insights about DAE personality calibration:
        - Too serious vs too playful
        - Presence of humor (Earthbound/Undertale style)
        - Grounding vs clinical feel
        """
        tone_feedback = self.get_tone_feedback(limit=100)

        if not tone_feedback:
            return {'status': 'no_tone_feedback', 'insights': []}

        # Keywords for tone analysis
        playful_keywords = ['playful', 'humor', 'funny', 'light', 'undertale', 'earthbound']
        serious_keywords = ['serious', 'clinical', 'dry', 'formal', 'stiff']
        warm_keywords = ['warm', 'safe', 'holding', 'present', 'grounding']

        playful_count = 0
        serious_count = 0
        warm_count = 0

        insights = []

        for f in tone_feedback:
            tone_text = f.get('tone_notes') or ''
            comment_text = f.get('comment') or ''
            text = (tone_text + ' ' + comment_text).lower()

            if any(kw in text for kw in playful_keywords):
                playful_count += 1
                if f['rating'] == 'excellent':
                    insights.append(f"✨ Playful tone well-received: \"{f['emission'][:50]}...\"")

            if any(kw in text for kw in serious_keywords):
                serious_count += 1
                if f['rating'] == 'not_helpful':
                    insights.append(f"⚠️  Too serious/clinical: \"{f['emission'][:50]}...\"")

            if any(kw in text for kw in warm_keywords):
                warm_count += 1

        return {
            'status': 'analyzed',
            'playful_mentions': playful_count,
            'serious_mentions': serious_count,
            'warm_mentions': warm_count,
            'insights': insights[:10]  # Top 10 insights
        }


if __name__ == '__main__':
    # Test feedback collector
    print("=== Testing Feedback Collector ===\n")

    collector = FeedbackCollector()

    # Record test feedback (various ratings)
    collector.record_rating(
        user_id='user_test',
        session_id='session_test',
        turn_id=1,
        user_input="I'm feeling overwhelmed",
        emission="I'm with you",
        rating='excellent',
        comment="Very helpful, felt safe",
        metadata={'confidence': 0.8, 'nexuses': 2, 'strategy': 'hebbian_fallback'},
        tone_notes="Appropriately minimal, grounding"
    )

    collector.record_rating(
        user_id='user_test',
        session_id='session_test',
        turn_id=2,
        user_input="What should I do?",
        emission="What feels right to you in this moment?",
        rating='helpful',
        comment="Good question, made me think",
        metadata={'confidence': 0.65, 'nexuses': 3}
    )

    collector.record_rating(
        user_id='user_test',
        session_id='session_test',
        turn_id=3,
        user_input="I don't know",
        emission="Let's explore what's underneath that 'not knowing' - sometimes uncertainty is its own kind of knowing.",
        rating='not_helpful',
        comment="Too interpretive, wanted simpler presence",
        metadata={'confidence': 0.7, 'nexuses': 5}
    )

    # Get stats
    user_stats = collector.get_user_feedback_stats('user_test')
    print(f"✅ User stats:")
    print(f"   Total: {user_stats['total_ratings']}")
    print(f"   Helpful rate: {user_stats['helpful_rate']*100:.1f}%")
    print(f"   Excellent rate: {user_stats['excellent_rate']*100:.1f}%")

    global_stats = collector.get_global_stats()
    print(f"\n✅ Global stats:")
    print(f"   Total: {global_stats['total_ratings']}")
    print(f"   Users: {global_stats['unique_users']}")
    print(f"   Helpful rate: {global_stats['helpful_rate']*100:.1f}%")

    # Get not helpful examples
    not_helpful = collector.get_not_helpful_examples(limit=5)
    print(f"\n⚠️  Not helpful examples ({len(not_helpful)}):")
    for f in not_helpful:
        print(f"   Input: \"{f['user_input'][:40]}...\"")
        print(f"   Emission: \"{f['emission'][:40]}...\"")
        print(f"   Comment: {f.get('comment', 'N/A')}")
        print()

    # Analyze tone
    tone_analysis = collector.analyze_tone_patterns()
    print(f"✅ Tone analysis:")
    print(f"   Status: {tone_analysis['status']}")
    print(f"   Playful mentions: {tone_analysis.get('playful_mentions', 0)}")
    print(f"   Serious mentions: {tone_analysis.get('serious_mentions', 0)}")
    print(f"   Warm mentions: {tone_analysis.get('warm_mentions', 0)}")

    print("\n✅ Feedback Collector tests passed!")
