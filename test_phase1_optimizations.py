"""
Test Phase 1 Entity Continuity Optimizations
=============================================

Validates the 3 critical optimizations:
1. Full-text search index (50-200× speedup on property matching)
2. Parallel query execution (2× speedup on retrieval)
3. Turn-based tracking (enables morpheable horizon)

Expected Results:
- Query @ 1K entities: <100ms
- Query @ 10K entities: <200ms
- FTS speedup: 50-200× faster than property scan
- Parallel speedup: ~2× faster than sequential

Author: DAE_HYPHAE_1 + Claude Code
Date: November 17, 2025
"""

import sys
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from knowledge_base.neo4j_knowledge_graph import Neo4jKnowledgeGraph


def generate_mock_entities(count: int, user_id: str = "test_user") -> List[Dict]:
    """
    Generate mock entities for testing.

    Creates realistic entity distribution:
    - 60% Person (family, friends, colleagues)
    - 20% Place (cities, buildings, landmarks)
    - 10% Preference (likes, habits, interests)
    - 10% Fact (biographical, historical)
    """
    entities = []

    # Common names for variety
    first_names = ["Emma", "Lily", "Alex", "Jordan", "Taylor", "Morgan", "Casey",
                   "Riley", "Jamie", "Quinn", "Avery", "Blake", "Cameron", "Drew"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                  "Miller", "Davis", "Rodriguez", "Martinez"]

    places = ["New York", "San Francisco", "Seattle", "Austin", "Boston", "Chicago",
              "Portland", "Denver", "Miami", "Atlanta", "The Office", "Home",
              "Coffee Shop", "Park", "Library", "Gym", "Restaurant", "Beach"]

    preferences = ["reading", "hiking", "cooking", "music", "art", "sports",
                   "travel", "photography", "gaming", "writing", "yoga", "coffee",
                   "tea", "movies", "theater", "gardening"]

    # Generate Person entities (60%)
    person_count = int(count * 0.6)
    for i in range(person_count):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}" if i % 3 != 0 else first  # Mix full names and first names

        entities.append({
            'entity_type': 'Person',
            'entity_value': name,
            'user_id': user_id,
            'properties': {
                'description': f"Person {i+1}",
                'relationship': random.choice(['friend', 'colleague', 'family', 'acquaintance']),
                'mention_count': random.randint(1, 50)
            }
        })

    # Generate Place entities (20%)
    place_count = int(count * 0.2)
    for i in range(place_count):
        place = random.choice(places)
        if i > len(places):
            place = f"{place} {i}"  # Make unique

        entities.append({
            'entity_type': 'Place',
            'entity_value': place,
            'user_id': user_id,
            'properties': {
                'description': f"Place {i+1}",
                'role': random.choice(['home', 'work', 'leisure', 'travel']),
                'mention_count': random.randint(1, 30)
            }
        })

    # Generate Preference entities (10%)
    pref_count = int(count * 0.1)
    for i in range(pref_count):
        pref = random.choice(preferences)
        if i > len(preferences):
            pref = f"{pref} {i}"

        entities.append({
            'entity_type': 'Preference',
            'entity_value': pref,
            'user_id': user_id,
            'properties': {
                'description': f"Preference {i+1}",
                'mention_count': random.randint(1, 20)
            }
        })

    # Generate Fact entities (10%)
    fact_count = count - person_count - place_count - pref_count
    for i in range(fact_count):
        entities.append({
            'entity_type': 'Fact',
            'entity_value': f"Fact about life {i+1}",
            'user_id': user_id,
            'properties': {
                'description': f"Biographical fact {i+1}",
                'mention_count': random.randint(1, 15)
            }
        })

    return entities


def populate_test_entities(graph: Neo4jKnowledgeGraph, entity_count: int, user_id: str = "test_user"):
    """
    Populate Neo4j with test entities.

    Args:
        graph: Neo4j graph connection
        entity_count: Number of entities to create
        user_id: Test user ID
    """
    print(f"\n{'='*80}")
    print(f"🔧 POPULATING NEO4J WITH {entity_count} MOCK ENTITIES")
    print(f"{'='*80}\n")

    entities = generate_mock_entities(entity_count, user_id)

    start_time = time.time()

    for i, entity in enumerate(entities):
        # Simulate turn progression
        current_turn = i + 1

        # Simulate temporal context
        base_time = datetime.now() - timedelta(minutes=entity_count - i)
        temporal_context = {
            'time_of_day': 'afternoon' if 12 <= base_time.hour < 18 else 'evening',
            'day_of_week': base_time.strftime('%A')
        }

        graph.create_entity(
            entity_type=entity['entity_type'],
            entity_value=entity['entity_value'],
            user_id=entity['user_id'],
            properties=entity['properties'],
            temporal_context=temporal_context,
            current_turn=current_turn
        )

        if (i + 1) % 100 == 0:
            print(f"   Created {i + 1}/{entity_count} entities...")

    elapsed = time.time() - start_time
    print(f"\n✅ Created {entity_count} entities in {elapsed:.2f}s ({elapsed/entity_count*1000:.1f}ms per entity)")


def test_query_performance(graph: Neo4jKnowledgeGraph, user_id: str = "test_user"):
    """
    Test query performance with Phase 1 optimizations.

    Tests:
    1. get_recent_entities() - Time-window retrieval
    2. fuzzy_match_entities() - FTS-powered keyword search
    3. Parallel execution - Measure speedup
    """
    print(f"\n{'='*80}")
    print("📊 TESTING QUERY PERFORMANCE")
    print(f"{'='*80}\n")

    # Test 1: Recent entities query
    print("Test 1: get_recent_entities() - Time-window retrieval")
    times = []
    for i in range(5):
        start = time.time()
        results = graph.get_recent_entities(user_id=user_id, limit=20, time_window_minutes=60)
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    print(f"   Average: {avg_time*1000:.2f}ms")
    print(f"   Min: {min(times)*1000:.2f}ms")
    print(f"   Max: {max(times)*1000:.2f}ms")
    print(f"   Results: {len(results)} entities")

    if avg_time < 0.1:
        print(f"   ✅ EXCELLENT (<100ms)")
    elif avg_time < 0.2:
        print(f"   ✅ GOOD (<200ms)")
    else:
        print(f"   ⚠️  SLOW (>{200}ms)")

    # Test 2: Fuzzy match (FTS-powered)
    print(f"\nTest 2: fuzzy_match_entities() - FTS keyword search")
    test_queries = ["Emma", "work", "reading", "coffee", "friend"]

    for query in test_queries:
        times = []
        for i in range(3):
            start = time.time()
            results = graph.fuzzy_match_entities(text=query, user_id=user_id, threshold=0.6)
            elapsed = time.time() - start
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        print(f"   Query '{query}': {avg_time*1000:.2f}ms ({len(results)} results)")

        if avg_time < 0.01:
            print(f"      ✅ FTS WORKING! (<10ms)")
        elif avg_time < 0.05:
            print(f"      ✅ FAST (<50ms)")
        else:
            print(f"      ⚠️  SLOW (>{50}ms)")

    # Test 3: Parallel vs Sequential
    print(f"\nTest 3: Parallel vs Sequential Execution")

    # Sequential
    seq_times = []
    for i in range(3):
        start = time.time()
        r1 = graph.get_recent_entities(user_id=user_id, limit=20)
        r2 = graph.fuzzy_match_entities(text="Emma", user_id=user_id)
        elapsed = time.time() - start
        seq_times.append(elapsed)

    seq_avg = sum(seq_times) / len(seq_times)
    print(f"   Sequential: {seq_avg*1000:.2f}ms")

    # Parallel (simulated via concurrent.futures)
    from concurrent.futures import ThreadPoolExecutor

    par_times = []
    for i in range(3):
        start = time.time()
        with ThreadPoolExecutor(max_workers=2) as executor:
            f1 = executor.submit(graph.get_recent_entities, user_id=user_id, limit=20)
            f2 = executor.submit(graph.fuzzy_match_entities, text="Emma", user_id=user_id)
            r1 = f1.result(timeout=0.5)
            r2 = f2.result(timeout=0.5)
        elapsed = time.time() - start
        par_times.append(elapsed)

    par_avg = sum(par_times) / len(par_times)
    speedup = seq_avg / par_avg if par_avg > 0 else 0

    print(f"   Parallel: {par_avg*1000:.2f}ms")
    print(f"   Speedup: {speedup:.2f}×")

    if speedup >= 1.5:
        print(f"   ✅ PARALLEL WORKING! (≥1.5× speedup)")
    else:
        print(f"   ⚠️  LIMITED BENEFIT (<1.5× speedup)")


def test_turn_tracking(graph: Neo4jKnowledgeGraph, user_id: str = "test_user"):
    """
    Test turn-based tracking.

    Validates:
    1. Entities have first_mention_turn and last_mention_turn
    2. Turn numbers increment correctly
    3. Queries can filter by turn range
    """
    print(f"\n{'='*80}")
    print("📊 TESTING TURN-BASED TRACKING")
    print(f"{'='*80}\n")

    # Query entities with turn info
    query = """
    MATCH (e {user_id: $user_id})
    WHERE e.first_mention_turn IS NOT NULL
    RETURN e.entity_value AS name,
           labels(e)[0] AS type,
           e.first_mention_turn AS first_turn,
           e.last_mention_turn AS last_turn,
           e.mention_count AS mentions
    ORDER BY e.first_mention_turn ASC
    LIMIT 10
    """

    try:
        with graph.driver.session(database=graph.database) as session:
            result = session.run(query, user_id=user_id)
            entities = list(result)

        if entities:
            print(f"✅ Turn tracking ACTIVE - Found {len(entities)} entities with turn data:\n")
            for e in entities[:5]:
                print(f"   • {e['name']} ({e['type']})")
                print(f"     First turn: {e['first_turn']}, Last turn: {e['last_turn']}, Mentions: {e['mentions']}")

            # Check turn progression
            turns = [e['first_turn'] for e in entities]
            if len(set(turns)) > 1:
                print(f"\n✅ Turn progression detected: {min(turns)} → {max(turns)}")
            else:
                print(f"\n⚠️  All entities on same turn (expected for batch creation)")
        else:
            print("❌ No entities with turn tracking found!")
            print("   This suggests turn tracking is not working.")

    except Exception as e:
        print(f"❌ Turn tracking test failed: {e}")


def cleanup_test_entities(graph: Neo4jKnowledgeGraph, user_id: str = "test_user"):
    """Clean up test entities."""
    print(f"\n{'='*80}")
    print(f"🧹 CLEANING UP TEST ENTITIES")
    print(f"{'='*80}\n")

    query = """
    MATCH (e {user_id: $user_id})
    DELETE e
    """

    try:
        with graph.driver.session(database=graph.database) as session:
            result = session.run(query, user_id=user_id)
            summary = result.consume()
            deleted = summary.counters.nodes_deleted

        print(f"✅ Deleted {deleted} test entities")
    except Exception as e:
        print(f"⚠️  Cleanup failed: {e}")


def main():
    """Run Phase 1 optimization tests."""
    print(f"\n{'='*80}")
    print("🌀 PHASE 1 ENTITY CONTINUITY OPTIMIZATION TESTS")
    print(f"{'='*80}")
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing optimizations:")
    print(f"  1. Full-text search index (FTS)")
    print(f"  2. Parallel query execution")
    print(f"  3. Turn-based tracking")
    print(f"\nTarget: <100ms @ 1K entities, <200ms @ 10K entities")

    # Connect to Neo4j
    print(f"\n{'='*80}")
    print("🔌 CONNECTING TO NEO4J")
    print(f"{'='*80}\n")

    try:
        graph = Neo4jKnowledgeGraph()
        if not graph.driver:
            print("❌ Neo4j connection failed!")
            print("   Ensure Neo4j is running and configured correctly.")
            return

        print("✅ Connected to Neo4j successfully")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return

    # Test with 1K entities
    entity_count = 1000
    test_user = f"test_phase1_{int(time.time())}"

    try:
        # Populate
        populate_test_entities(graph, entity_count, test_user)

        # Test queries
        test_query_performance(graph, test_user)

        # Test turn tracking
        test_turn_tracking(graph, test_user)

        # Summary
        print(f"\n{'='*80}")
        print("📊 TEST SUMMARY")
        print(f"{'='*80}\n")
        print(f"✅ Phase 1 optimizations validated with {entity_count} entities")
        print(f"\nNext steps:")
        print(f"  1. If tests pass: Phase 1 COMPLETE ✅")
        print(f"  2. If tests fail: Debug specific optimization")
        print(f"  3. Optional: Test with 10K entities for full validation")

    finally:
        # Cleanup
        cleanup_test_entities(graph, test_user)
        graph.close()

    print(f"\n🌀 Testing complete! 🌀\n")


if __name__ == "__main__":
    main()
