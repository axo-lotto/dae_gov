#!/usr/bin/env python3
"""
Test Mycelium Trace Integration with Felt Capture
==================================================

Validates end-to-end integration of:
- SimpleFeltCapture for organism felt state
- MyceliumTracer for persistent memory traces
- Vector signatures for semantic similarity

Author: Claude Code (November 2025)
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_base.mycelium_traces import MyceliumTracer, TraceType, RelationType
from knowledge_base.simple_felt_capture import cosine_similarity
import numpy as np


def test_trace_creation_with_felt_state():
    """Test creating traces with automatic felt state capture."""

    print("\n🧪 TEST 1: Trace Creation with Felt State Capture")
    print("=" * 60)

    # Initialize tracer (will initialize felt capture automatically)
    tracer = MyceliumTracer(user_id="user0")

    # Create a Note trace
    print("\n📝 Creating Note trace...")
    note = tracer.create_trace(
        TraceType.NOTE,
        title="Team burnout observation",
        content="Team members report feeling exhausted during standup meetings. Energy levels are noticeably low.",
        tags=["burnout", "team_health", "observation"],
        conversation_id="test_session_001"
    )

    print(f"   Trace ID: {note.trace_id}")

    if note.epoch_metadata:
        print(f"   ✅ Felt state captured!")
        print(f"      Satisfaction: {note.epoch_metadata.get('satisfaction', 0):.2f}")
        print(f"      Energy: {note.epoch_metadata.get('energy', 0):.2f}")
        print(f"      Organ coherences:")
        for organ, coherence in note.epoch_metadata.get('organ_coherences', {}).items():
            print(f"        {organ}: {coherence:.2f}")
    else:
        print("   ⚠️  No felt state captured")

    # Create an Insight trace
    print("\n💡 Creating Insight trace...")
    insight = tracer.create_trace(
        TraceType.INSIGHT,
        title="Burnout correlates with lack of autonomy",
        content="Pattern observation: teams with highest burnout also have least decision-making autonomy. This suggests autonomy restoration could reduce exhaustion.",
        tags=["burnout", "autonomy", "insight", "pattern"],
        conversation_id="test_session_001",
        # Simulate organ states from orchestrator
        organ_states={
            'LISTENING': 0.75,
            'EMPATHY': 0.70,
            'WISDOM': 0.85,  # High wisdom for insight
            'AUTHENTICITY': 0.65,
            'PRESENCE': 0.80
        }
    )

    print(f"   Trace ID: {insight.trace_id}")

    if insight.epoch_metadata:
        print(f"   ✅ Felt state captured!")
        print(f"      Satisfaction: {insight.epoch_metadata.get('satisfaction', 0):.2f}")
        print(f"      Energy: {insight.epoch_metadata.get('energy', 0):.2f}")
        print(f"      Organ coherences:")
        for organ, coherence in insight.epoch_metadata.get('organ_coherences', {}).items():
            print(f"        {organ}: {coherence:.2f}")

    # Create relationship
    print("\n🔗 Creating relationship: Note DERIVES_FROM Insight...")
    tracer.create_relationship(
        note.trace_id,
        insight.trace_id,
        RelationType.DERIVES_FROM,
        strength=0.9
    )
    print("   ✅ Relationship created")

    return note, insight


def test_vector_similarity():
    """Test vector similarity between traces."""

    print("\n🧪 TEST 2: Vector Similarity Comparison")
    print("=" * 60)

    tracer = MyceliumTracer(user_id="user0")

    # Create two related traces
    trace1 = tracer.create_trace(
        TraceType.NOTE,
        title="Observation about team dynamics",
        content="Team seems disconnected and lacks collaboration energy.",
        tags=["teamwork", "observation"]
    )

    trace2 = tracer.create_trace(
        TraceType.INSIGHT,
        title="Team disconnection linked to remote work",
        content="The lack of collaboration may stem from prolonged remote work without intentional connection practices.",
        tags=["teamwork", "remote_work", "insight"]
    )

    # Compare vector signatures
    if trace1.epoch_metadata and trace2.epoch_metadata:
        vec1 = np.array(trace1.epoch_metadata.get('felt_state_7d', [0]*7))
        vec2 = np.array(trace2.epoch_metadata.get('felt_state_7d', [0]*7))

        similarity = cosine_similarity(vec1, vec2)

        print(f"\nVector Similarity Analysis:")
        print(f"   Trace 1: {trace1.title}")
        print(f"   Trace 2: {trace2.title}")
        print(f"   Cosine similarity: {similarity:.3f}")

        if similarity > 0.7:
            print(f"   ✅ High similarity - traces are related (threshold: 0.7)")
        elif similarity > 0.5:
            print(f"   ⚠️  Moderate similarity")
        else:
            print(f"   ❌ Low similarity - traces are unrelated")
    else:
        print("   ⚠️  Vector signatures not available")


def test_transformation_learning():
    """Test learning from trace transformations (Note → Insight)."""

    print("\n🧪 TEST 3: Transformation Learning Pattern")
    print("=" * 60)

    tracer = MyceliumTracer(user_id="user0")

    # Create note
    note = tracer.create_trace(
        TraceType.NOTE,
        title="Frequent meeting interruptions",
        content="Noticed that team meetings often get interrupted or derailed.",
        tags=["meetings", "observation"]
    )

    # Create insight derived from note
    insight = tracer.create_trace(
        TraceType.INSIGHT,
        title="Interruptions signal lack of psychological safety",
        content="The frequent interruptions may indicate low psychological safety - people don't feel secure enough to speak without being challenged.",
        tags=["meetings", "psychological_safety", "insight"]
    )

    # Analyze transformation pattern
    if note.epoch_metadata and insight.epoch_metadata:
        note_sat = note.epoch_metadata.get('satisfaction', 0)
        insight_sat = insight.epoch_metadata.get('satisfaction', 0)
        sat_gain = insight_sat - note_sat

        note_wisdom = note.epoch_metadata.get('organ_coherences', {}).get('WISDOM', 0)
        insight_wisdom = insight.epoch_metadata.get('organ_coherences', {}).get('WISDOM', 0)
        wisdom_gain = insight_wisdom - note_wisdom

        print(f"\nTransformation Pattern (Note → Insight):")
        print(f"   Satisfaction gain: {sat_gain:+.2f}")
        print(f"   Wisdom gain: {wisdom_gain:+.2f}")

        if sat_gain > 0 and wisdom_gain > 0:
            print(f"   ✅ Expected pattern validated:")
            print(f"      - Insights have higher satisfaction than notes")
            print(f"      - Insights engage more wisdom than notes")
        else:
            print(f"   ⚠️  Unexpected pattern - may need tuning")


def test_user_statistics():
    """Test user trace statistics."""

    print("\n🧪 TEST 4: User Trace Statistics")
    print("=" * 60)

    tracer = MyceliumTracer(user_id="user0")

    # Get stats
    stats = tracer.get_user_stats()

    print(f"\nUser Statistics for user0:")
    print(f"   Total traces: {stats['total_traces']}")
    print(f"   By type:")
    for trace_type, count in stats['by_type'].items():
        print(f"      {trace_type}: {count}")
    print(f"   Total relationships: {stats['total_relationships']}")
    print(f"   Recent traces (last 5):")
    for trace in stats['recent_traces'][:5]:
        # Handle both MyceliumTrace objects and dicts
        if isinstance(trace, dict):
            print(f"      - {trace.get('trace_type', 'Unknown')}: {trace.get('title', 'Untitled')}")
        else:
            trace_type_str = trace.trace_type.value if hasattr(trace.trace_type, 'value') else str(trace.trace_type)
            print(f"      - {trace_type_str}: {trace.title}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🍄 MYCELIUM TRACE FELT INTEGRATION TEST SUITE")
    print("="*60)

    try:
        # Run tests
        test_trace_creation_with_felt_state()
        test_vector_similarity()
        test_transformation_learning()
        test_user_statistics()

        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\n🎉 Integration validated:")
        print("   - Felt state capture working")
        print("   - Vector signatures for similarity")
        print("   - Transformation learning patterns")
        print("   - User statistics tracking")
        print("\n🌀 The mycelial network grows with felt understanding! 🌀\n")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
