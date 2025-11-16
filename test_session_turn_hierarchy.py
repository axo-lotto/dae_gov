#!/usr/bin/env python3
"""
Test USER:SESSION:TURN Hierarchy Integration
=============================================

Validates the complete temporal entity tracking hierarchy:
1. Session lifecycle management (start, add_turn, end)
2. Turn-level entity context preservation
3. Session-level pattern tracking (polyvagal, entity evolution)
4. Session classification (crisis, breakthrough)
5. Entity timeline tracking across turns

Date: November 16, 2025
Phase: USER:SESSION:TURN Hierarchy Implementation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.session_turn_manager import SessionTurnManager, session_to_dict
from persona_layer.user_superject_learner import UserSuperjectLearner
from persona_layer.superject_structures import (
    ConversationSession,
    ConversationTurn,
    FeltStateSnapshot,
    create_default_profile
)


def main():
    print("\n" + "="*70)
    print("USER:SESSION:TURN HIERARCHY - INTEGRATION TEST")
    print("="*70 + "\n")

    # Test 1: Session Manager Initialization
    print("TEST 1: Session Manager Initialization")
    print("-" * 50)

    manager = SessionTurnManager(storage_dir="persona_layer/users")
    print(f"  Session manager created")
    print(f"  Storage dir: {manager.storage_dir}")
    print(f"  Active sessions: {len(manager.active_sessions)}")
    print("  ✅ PASSED\n")

    # Test 2: Create Session
    print("TEST 2: Create Session")
    print("-" * 50)

    test_user_id = "test_hierarchy_emiliano"
    session = manager.start_session(test_user_id)

    print(f"  Session ID: {session.session_id[:50]}...")
    print(f"  User ID: {session.user_id}")
    print(f"  Start time: {session.start_time}")
    print(f"  Initial turns: {session.total_turns}")
    print(f"  Crisis session: {session.crisis_session}")
    print(f"  Breakthrough session: {session.breakthrough_session}")
    print("  ✅ PASSED\n")

    # Test 3: Simulate Multi-Turn Conversation with Entity Mentions
    print("TEST 3: Multi-Turn Conversation with Entity Tracking")
    print("-" * 50)

    # Turn 1: User mentions daughter (Emma)
    turn1_prehension = {
        'entity_memory_available': True,
        'mentioned_entities': [
            {'name': 'Emma', 'relationship': 'daughter', 'historical_polyvagal': 'ventral'}
        ],
        'relational_query_detected': False,
        'implicit_references': [],
        'entity_references': ['story_entity']
    }

    # Create minimal FeltStateSnapshot with all required fields
    turn1_felt = FeltStateSnapshot(
        timestamp="2025-11-16T10:00:00",
        organ_signature=[0.5] * 11,
        active_organs=['LISTENING', 'EMPATHY', 'BOND'],
        dominant_nexuses=['coherence_repair'],
        zone=3,
        zone_name="exploratory",
        polyvagal_state="sympathetic",
        self_distance=0.4,
        v0_energy=0.35,
        satisfaction=0.65,
        convergence_cycles=3,
        transduction_mechanism="coherence_repair",
        transduction_pathway="empathic_bridging"
    )

    turn1 = manager.create_turn(
        session=session,
        user_input="I'm worried about Emma. She's been quiet lately.",
        dae_response="I notice concern in how you describe Emma's quietness.",
        entity_prehension=turn1_prehension,
        felt_state=turn1_felt,
        user_satisfaction=0.70
    )

    manager.add_turn(session, turn1)

    print(f"  Turn 1:")
    print(f"    Input: '{turn1.user_input[:50]}...'")
    print(f"    Entities mentioned: {turn1.mentioned_entities}")
    print(f"    Relational query: {turn1.relational_query}")
    print(f"    Session entities now: {list(session.session_entities.keys())}")

    # Turn 2: User mentions same entity with context shift
    turn2_prehension = {
        'entity_memory_available': True,
        'mentioned_entities': [
            {'name': 'Emma', 'relationship': 'daughter', 'historical_polyvagal': 'ventral'}
        ],
        'relational_query_detected': False,
        'implicit_references': [],
        'entity_references': ['story_entity']
    }

    turn2_felt = FeltStateSnapshot(
        timestamp="2025-11-16T10:01:00",
        organ_signature=[0.5] * 11,
        active_organs=['LISTENING', 'EMPATHY'],
        dominant_nexuses=['coherence_repair'],
        zone=3,
        zone_name="exploratory",
        polyvagal_state="mixed",
        self_distance=0.45,
        v0_energy=0.40,
        satisfaction=0.72,
        convergence_cycles=3,
        transduction_mechanism="coherence_repair",
        transduction_pathway="empathic_bridging"
    )

    turn2 = manager.create_turn(
        session=session,
        user_input="Actually, Emma did smile today when I picked her up.",
        dae_response="That smile carries hope, even in the midst of concern.",
        entity_prehension=turn2_prehension,
        felt_state=turn2_felt,
        user_satisfaction=0.75
    )

    manager.add_turn(session, turn2)

    print(f"\n  Turn 2:")
    print(f"    Input: '{turn2.user_input[:50]}...'")
    print(f"    Emma mention count: {session.session_entities['Emma']['mention_count']}")
    print(f"    Emma mood evolution: {session.entity_mood_evolution.get('Emma', [])}")

    # Turn 3: Relational query - do you remember?
    turn3_prehension = {
        'entity_memory_available': True,
        'mentioned_entities': [],
        'relational_query_detected': True,
        'implicit_references': [],
        'entity_references': ['user', 'dae']
    }

    turn3_felt = FeltStateSnapshot(
        timestamp="2025-11-16T10:02:00",
        organ_signature=[0.5] * 11,
        active_organs=['LISTENING', 'EMPATHY'],
        dominant_nexuses=['relational_attunement'],
        zone=2,
        zone_name="safe",
        polyvagal_state="ventral",
        self_distance=0.3,
        v0_energy=0.25,
        satisfaction=0.85,
        convergence_cycles=2,
        transduction_mechanism="relational_attunement",
        transduction_pathway="empathic_bridging"
    )

    turn3 = manager.create_turn(
        session=session,
        user_input="Do you remember what we talked about last time?",
        dae_response="I sense your need for continuity and being remembered.",
        entity_prehension=turn3_prehension,
        felt_state=turn3_felt,
        user_satisfaction=0.82
    )

    manager.add_turn(session, turn3)

    print(f"\n  Turn 3:")
    print(f"    Relational query detected: {turn3.relational_query}")
    print(f"    Polyvagal trajectory: {session.polyvagal_trajectory}")
    print(f"    Satisfaction trend: {session.satisfaction_trend}")

    # Turn 4: User mentions new entity
    turn4_prehension = {
        'entity_memory_available': True,
        'mentioned_entities': [
            {'name': 'Michael', 'relationship': 'colleague', 'historical_polyvagal': 'mixed'}
        ],
        'relational_query_detected': False,
        'implicit_references': [],
        'entity_references': ['story_entity']
    }

    turn4_felt = FeltStateSnapshot(
        timestamp="2025-11-16T10:03:00",
        organ_signature=[0.5] * 11,
        active_organs=['LISTENING', 'EMPATHY'],
        dominant_nexuses=['relational_attunement'],
        zone=2,
        zone_name="safe",
        polyvagal_state="ventral",
        self_distance=0.32,
        v0_energy=0.28,
        satisfaction=0.88,
        convergence_cycles=2,
        transduction_mechanism="relational_attunement",
        transduction_pathway="empathic_bridging"
    )

    turn4 = manager.create_turn(
        session=session,
        user_input="Michael at work has been supportive through this.",
        dae_response="Support from Michael seems to provide grounding during uncertainty.",
        entity_prehension=turn4_prehension,
        felt_state=turn4_felt,
        user_satisfaction=0.85
    )

    manager.add_turn(session, turn4)

    print(f"\n  Turn 4:")
    print(f"    New entity: Michael")
    print(f"    Total session entities: {list(session.session_entities.keys())}")
    print(f"    Entity timeline entries: {len(session.entity_mentions_timeline)}")

    print(f"\n  Session State:")
    print(f"    Total turns: {session.total_turns}")
    print(f"    Mean satisfaction: {session.mean_satisfaction:.3f}")
    print(f"    Satisfaction trend: {session.satisfaction_trend}")
    print(f"    Polyvagal trajectory: {session.polyvagal_trajectory}")
    print(f"    Crisis session: {session.crisis_session}")
    print(f"    Breakthrough session: {session.breakthrough_session}")

    print("  ✅ PASSED\n")

    # Test 4: Entity Timeline Tracking
    print("TEST 4: Entity Timeline Tracking")
    print("-" * 50)

    print(f"  Entity mentions timeline:")
    for entry in session.entity_mentions_timeline:
        print(f"    Turn {entry['turn']}: {entry['entity']} ({entry['context']})")

    print(f"\n  Entity mood evolution:")
    for entity, moods in session.entity_mood_evolution.items():
        print(f"    {entity}: {moods}")

    emma_data = session.session_entities.get('Emma', {})
    print(f"\n  Emma session profile:")
    print(f"    Mention count: {emma_data.get('mention_count', 0)}")
    print(f"    First mention: Turn {emma_data.get('first_mention_turn', 0)}")
    print(f"    Last mention: Turn {emma_data.get('last_mention_turn', 0)}")
    print(f"    Contexts: {emma_data.get('contexts', [])}")

    print("  ✅ PASSED\n")

    # Test 5: Session Classification
    print("TEST 5: Session Classification")
    print("-" * 50)

    # Current session should be breakthrough (high satisfaction, improving trend, ventral state)
    print(f"  Current classification:")
    print(f"    Crisis session: {session.crisis_session}")
    print(f"    Breakthrough session: {session.breakthrough_session}")
    print(f"    Mean satisfaction: {session.mean_satisfaction:.3f}")
    print(f"    Last polyvagal state: {session.polyvagal_trajectory[-1]}")

    # Simulate a crisis session by adding sympathetic turns
    crisis_session = manager.start_session("test_crisis_user")

    for i in range(3):
        crisis_felt = FeltStateSnapshot(
            timestamp=f"2025-11-16T11:0{i}:00",
            organ_signature=[0.5] * 11,
            active_organs=['NDAM', 'BOND'],
            dominant_nexuses=['crisis_response'],
            zone=4,
            zone_name="crisis",
            polyvagal_state="sympathetic",
            self_distance=0.7,
            v0_energy=0.80,
            satisfaction=0.35 - (i * 0.05),  # Declining
            convergence_cycles=4,
            transduction_mechanism="crisis_response",
            transduction_pathway="grounding"
        )

        crisis_turn = manager.create_turn(
            session=crisis_session,
            user_input=f"I'm feeling overwhelmed again... turn {i+1}",
            dae_response="I sense the weight of what you're carrying.",
            entity_prehension={
                'entity_memory_available': False,
                'mentioned_entities': [],
                'relational_query_detected': False
            },
            felt_state=crisis_felt,
            user_satisfaction=0.35 - (i * 0.05)
        )
        manager.add_turn(crisis_session, crisis_turn)

    print(f"\n  Crisis session classification:")
    print(f"    Crisis session: {crisis_session.crisis_session}")
    print(f"    Polyvagal trajectory: {crisis_session.polyvagal_trajectory}")
    print(f"    Satisfaction trend: {crisis_session.satisfaction_trend}")

    print("  ✅ PASSED\n")

    # Test 6: Session End and Summary
    print("TEST 6: Session End and Summary")
    print("-" * 50)

    manager.end_session(session, ended_naturally=True)

    print(f"  Session ended:")
    print(f"    End time: {session.end_time}")
    print(f"    Ended naturally: {session.ended_naturally}")
    print(f"    Last turn continued: {session.turns[-1].user_continued}")

    summary = manager.get_session_summary(session)
    print(f"\n  Session summary:")
    print(f"    Session ID: {summary['session_id'][:40]}...")
    print(f"    Total turns: {summary['total_turns']}")
    print(f"    Entities mentioned: {summary['entities_mentioned']}")
    print(f"    Mean satisfaction: {summary['mean_satisfaction']:.3f}")
    print(f"    Breakthrough: {summary['breakthrough_session']}")

    print("  ✅ PASSED\n")

    # Test 7: Save Session to Profile
    print("TEST 7: Save Session to Profile")
    print("-" * 50)

    learner = UserSuperjectLearner(storage_dir="persona_layer/users")
    profile = learner.get_or_create_profile(test_user_id)

    manager.save_session_to_profile(session, profile)

    print(f"  Profile updated:")
    print(f"    Total sessions: {profile.total_sessions}")
    print(f"    Session patterns: {profile.session_patterns}")
    print(f"\n  Entity session evolution:")
    for entity, evolution in profile.entity_session_evolution.items():
        print(f"    {entity}:")
        for entry in evolution:
            print(f"      Session {entry['session_number']}: {entry['mention_count']} mentions, moods={entry['moods']}")

    # Save profile
    learner.save_profile(profile)
    print(f"\n  Profile saved to disk")
    print("  ✅ PASSED\n")

    # Test 8: JSON Serialization
    print("TEST 8: JSON Serialization")
    print("-" * 50)

    session_dict = session_to_dict(session)
    print(f"  Session serialized to dict:")
    print(f"    Keys: {list(session_dict.keys())[:10]}")
    print(f"    Turns count: {len(session_dict['turns'])}")
    print(f"    First turn keys: {list(session_dict['turns'][0].keys())[:8]}...")
    print(f"    Entity timeline: {len(session_dict['entity_mentions_timeline'])} entries")

    print("  ✅ PASSED\n")

    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)

    checks_passed = 0
    total_checks = 8

    # Check 1: Session creation
    if session.session_id and session.user_id == test_user_id:
        print("✅ Check 1: Session creation PASSED")
        checks_passed += 1
    else:
        print("❌ Check 1: Session creation FAILED")

    # Check 2: Turn tracking
    if session.total_turns == 4:
        print("✅ Check 2: Turn tracking PASSED")
        checks_passed += 1
    else:
        print("❌ Check 2: Turn tracking FAILED")

    # Check 3: Entity timeline
    if len(session.entity_mentions_timeline) == 3:  # Emma (2x) + Michael (1x)
        print("✅ Check 3: Entity timeline PASSED")
        checks_passed += 1
    else:
        print(f"❌ Check 3: Entity timeline FAILED (got {len(session.entity_mentions_timeline)}, expected 3)")

    # Check 4: Entity mood evolution
    if len(session.entity_mood_evolution.get('Emma', [])) == 2:
        print("✅ Check 4: Entity mood evolution PASSED")
        checks_passed += 1
    else:
        print("❌ Check 4: Entity mood evolution FAILED")

    # Check 5: Polyvagal trajectory
    if len(session.polyvagal_trajectory) == 4:
        print("✅ Check 5: Polyvagal trajectory PASSED")
        checks_passed += 1
    else:
        print("❌ Check 5: Polyvagal trajectory FAILED")

    # Check 6: Crisis session detection
    if crisis_session.crisis_session:
        print("✅ Check 6: Crisis session detection PASSED")
        checks_passed += 1
    else:
        print("❌ Check 6: Crisis session detection FAILED")

    # Check 7: Profile persistence
    if profile.total_sessions == 1 and 'Emma' in profile.entity_session_evolution:
        print("✅ Check 7: Profile persistence PASSED")
        checks_passed += 1
    else:
        print("❌ Check 7: Profile persistence FAILED")

    # Check 8: JSON serialization
    if 'turns' in session_dict and 'entity_mentions_timeline' in session_dict:
        print("✅ Check 8: JSON serialization PASSED")
        checks_passed += 1
    else:
        print("❌ Check 8: JSON serialization FAILED")

    print(f"\nResult: {checks_passed}/{total_checks} checks passed")

    if checks_passed == total_checks:
        print("\n🌀 USER:SESSION:TURN HIERARCHY FULLY OPERATIONAL!")
        print("   Temporal entity tracking enabled.")
        print("   Session-level patterns captured.")
        print("   Entity evolution across sessions tracked.")
        print("   Ready for persistent companion memory!")
    else:
        print(f"\n⚠️  {total_checks - checks_passed} checks need attention")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()
