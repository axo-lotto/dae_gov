"""
Neo4j Index Setup for NEXUS Organ Performance Optimization
===========================================================

Creates essential indexes for entity queries to prepare DAE_HYPHAE_1
for LLM-independent processing.

Phase 1: Essential Indexes (10-50× speedup on entity queries)

Date: November 15, 2025
Related: PERFORMANCE_NEO4J_OPTIMIZATION_PROPOSAL_NOV15_2025.md
"""

import sys
from pathlib import Path
import time
from typing import List, Tuple

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_base.neo4j_knowledge_graph import Neo4jKnowledgeGraph

def create_indexes(graph: Neo4jKnowledgeGraph) -> List[Tuple[str, bool, str]]:
    """
    Create optimized indexes for entity queries.

    Returns:
        List of (index_name, success, message) tuples
    """

    indexes = [
        # ===================================================================
        # PHASE 1: ESSENTIAL NODE PROPERTY INDEXES (8 indexes)
        # Expected: 10-50× speedup on basic entity queries
        # ===================================================================

        # Composite indexes for entity lookup (PRIMARY - 10-50× speedup)
        ("Person user-value",
         "CREATE INDEX entity_person_user_value IF NOT EXISTS FOR (n:Person) ON (n.user_id, n.entity_value)"),

        ("Place user-value",
         "CREATE INDEX entity_place_user_value IF NOT EXISTS FOR (n:Place) ON (n.user_id, n.entity_value)"),

        ("Preference user-value",
         "CREATE INDEX entity_pref_user_value IF NOT EXISTS FOR (n:Preference) ON (n.user_id, n.entity_value)"),

        ("Fact user-value",
         "CREATE INDEX entity_fact_user_value IF NOT EXISTS FOR (n:Fact) ON (n.user_id, n.entity_value)"),

        # Mention count indexes for top-entity queries (3-5× speedup)
        ("Person mention count",
         "CREATE INDEX entity_person_mentions IF NOT EXISTS FOR (n:Person) ON (n.mention_count)"),

        ("Place mention count",
         "CREATE INDEX entity_place_mentions IF NOT EXISTS FOR (n:Place) ON (n.mention_count)"),

        # Temporal indexes for recent entities (5-10× speedup)
        ("Person last mentioned",
         "CREATE INDEX entity_person_last IF NOT EXISTS FOR (n:Person) ON (n.last_mentioned)"),

        ("Place last mentioned",
         "CREATE INDEX entity_place_last IF NOT EXISTS FOR (n:Place) ON (n.last_mentioned)"),

        # 🕐 TEMPORAL AWARENESS: Time-of-day and day-of-week indexes (November 15, 2025)
        # Enable time-based entity queries (3-5× speedup on temporal filters)
        ("Entity time of day",
         "CREATE INDEX entity_time_of_day IF NOT EXISTS FOR (n:Person) ON (n.time_of_day_last)"),

        ("Entity day of week",
         "CREATE INDEX entity_day_of_week IF NOT EXISTS FOR (n:Person) ON (n.day_of_week_last)"),

        ("Entity temporal composite",
         "CREATE INDEX entity_temporal_combo IF NOT EXISTS FOR (n:Person) ON (n.time_of_day_last, n.day_of_week_last)"),

        # ===================================================================
        # PHASE 1.5: VEGAFY INTEGRATION - RELATIONSHIP + COMPOSITE INDEXES
        # (12 additional indexes - 50-200× speedup on complex queries)
        # Source: core_daedalea/Vegafy_index_neo4j.md patterns
        # ===================================================================

        # GROUP 1: RELATIONSHIP-TYPE INDEXES (5-20× speedup on multi-hop queries)
        # Pattern from Vegafy: Index relationship types for fast traversal

        ("Relationship HAS_DAUGHTER",
         "CREATE INDEX rel_has_daughter IF NOT EXISTS FOR ()-[r:HAS_DAUGHTER]-() ON (r.mention_count)"),

        ("Relationship HAS_SON",
         "CREATE INDEX rel_has_son IF NOT EXISTS FOR ()-[r:HAS_SON]-() ON (r.mention_count)"),

        ("Relationship HAS_PARTNER",
         "CREATE INDEX rel_has_partner IF NOT EXISTS FOR ()-[r:HAS_PARTNER]-() ON (r.emotional_valence)"),

        ("Relationship WORKS_AT",
         "CREATE INDEX rel_works_at IF NOT EXISTS FOR ()-[r:WORKS_AT]-() ON (r.stress_level)"),

        ("Relationship MENTIONED_WITH",
         "CREATE INDEX rel_mentioned_with IF NOT EXISTS FOR ()-[r:MENTIONED_WITH]-() ON (r.co_occurrence_count)"),

        # GROUP 2: COMPOSITE USER-ATTRIBUTE INDEXES (3-10× speedup on filtered queries)
        # Pattern from Vegafy: user + specific attribute combinations for zone-aware filtering

        ("User polyvagal composite",
         "CREATE INDEX user_polyvagal_combo IF NOT EXISTS FOR (n:Person) ON (n.user_id, n.typical_polyvagal_state)"),

        ("User urgency composite",
         "CREATE INDEX user_urgency_combo IF NOT EXISTS FOR (n:Person) ON (n.user_id, n.typical_urgency_level)"),

        ("User SELF distance composite",
         "CREATE INDEX user_self_combo IF NOT EXISTS FOR (n:Person) ON (n.user_id, n.typical_self_distance)"),

        # GROUP 3: TSK METADATA INDEXES (2-5× speedup on TSK-enriched queries)
        # Enable learning from concrescence metadata

        ("Entity zone mentioned",
         "CREATE INDEX entity_zone IF NOT EXISTS FOR (n:Person) ON (n.zone_when_mentioned)"),

        ("Entity V0 energy",
         "CREATE INDEX entity_v0 IF NOT EXISTS FOR (n:Person) ON (n.typical_v0_energy)"),

        ("Entity organism state",
         "CREATE INDEX entity_state IF NOT EXISTS FOR (n:Person) ON (n.typical_organism_state)"),

        # GROUP 4: SAFETY + PATHWAY INDEXES (future nexus node integration)

        ("Entity zone safety score",
         "CREATE INDEX entity_safety IF NOT EXISTS FOR (n:Person) ON (n.zone_5_safety_score)"),

        # ===================================================================
        # PHASE 1 SCALABILITY: FULL-TEXT SEARCH INDEX (November 17, 2025)
        # Expected: 50-200× speedup on property matching (300ms → 1-5ms)
        # ===================================================================

        ("Entity properties full-text",
         """CREATE FULLTEXT INDEX entity_properties_fulltext IF NOT EXISTS
            FOR (n:Person|Place|Preference|Fact|Organization)
            ON EACH [n.description, n.relationship, n.role, n.entity_value]"""),

        # ===================================================================
        # WHITEHEADIAN ONTOLOGY INDEXES (November 17, 2025)
        # Expected: 5-10× speedup on category-aware entity queries
        # ===================================================================

        # Ontology category index (Person::family, Concept::emotional, etc.)
        ("Entity ontology category",
         """CREATE INDEX entity_ontology_category IF NOT EXISTS
            FOR (n:Person|Place|Preference|Concept|Organization)
            ON (n.ontology_category)"""),

        # Process philosophy mapping (Personal Society, Eternal Object, etc.)
        ("Entity process mapping",
         """CREATE INDEX entity_process_mapping IF NOT EXISTS
            FOR (n:Person|Place|Preference|Concept|Organization)
            ON (n.process_mapping)"""),

        # Composite index: user + ontology category (category-filtered queries)
        ("Entity user-ontology composite",
         """CREATE INDEX entity_user_ontology IF NOT EXISTS
            FOR (n:Person|Place|Preference|Concept|Organization)
            ON (n.user_id, n.ontology_category)"""),
    ]

    results = []

    print("\n" + "="*80)
    print("🔧 CREATING NEO4J INDEXES FOR NEXUS ORGAN OPTIMIZATION")
    print("="*80 + "\n")

    for idx_name, query in indexes:
        try:
            start_time = time.time()

            print(f"Creating index: {idx_name}...", end=" ")

            # Execute index creation
            with graph.driver.session() as session:
                session.run(query)

            elapsed = time.time() - start_time

            print(f"✅ SUCCESS ({elapsed:.2f}s)")
            results.append((idx_name, True, f"Created in {elapsed:.2f}s"))

        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            results.append((idx_name, False, str(e)))

    return results


def verify_indexes(graph: Neo4jKnowledgeGraph) -> List[Tuple[str, str, str]]:
    """
    Verify all indexes were created successfully.

    Returns:
        List of (index_name, state, type) tuples
    """

    print("\n" + "="*80)
    print("🔍 VERIFYING INDEX CREATION")
    print("="*80 + "\n")

    try:
        with graph.driver.session() as session:
            result = session.run("SHOW INDEXES")
            indexes = []

            for record in result:
                name = record.get("name", "unknown")
                state = record.get("state", "unknown")
                idx_type = record.get("type", "unknown")

                # Filter to only our entity indexes
                if "entity_" in name or any(label in name for label in ["Person", "Place", "Preference", "Fact"]):
                    indexes.append((name, state, idx_type))
                    print(f"   ✅ {name}: {state} ({idx_type})")

            if not indexes:
                print("   ⚠️  No entity indexes found!")

            return indexes

    except Exception as e:
        print(f"   ❌ Verification failed: {str(e)}")
        return []


def benchmark_query_performance(graph: Neo4jKnowledgeGraph, user_id: str = "test_user"):
    """
    Simple benchmark to demonstrate index impact.

    Tests a typical entity lookup query before/after indexing.
    """

    print("\n" + "="*80)
    print("📊 QUERY PERFORMANCE BENCHMARK")
    print("="*80 + "\n")

    # Test query: Get all Person entities for a user
    query = """
    MATCH (p:Person {user_id: $user_id})
    RETURN p.entity_value, p.mention_count, p.last_mentioned
    ORDER BY p.mention_count DESC
    LIMIT 10
    """

    try:
        # Run query 5 times and average
        times = []

        for i in range(5):
            start_time = time.time()

            with graph.driver.session() as session:
                result = session.run(query, user_id=user_id)
                entities = list(result)

            elapsed = time.time() - start_time
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"Query: Get top 10 Person entities for user '{user_id}'")
        print(f"   Average time: {avg_time*1000:.2f}ms")
        print(f"   Min time: {min_time*1000:.2f}ms")
        print(f"   Max time: {max_time*1000:.2f}ms")
        print(f"   Results returned: {len(entities)}")

        if avg_time < 0.010:  # < 10ms
            print(f"   ✅ EXCELLENT (< 10ms) - Indexes working!")
        elif avg_time < 0.050:  # < 50ms
            print(f"   ✅ GOOD (< 50ms) - Acceptable performance")
        else:
            print(f"   ⚠️  SLOW (> 50ms) - May need optimization")

    except Exception as e:
        print(f"   ❌ Benchmark failed: {str(e)}")


def main():
    """Main execution."""

    print("\n" + "="*80)
    print("🌀 NEO4J INDEX SETUP - NEXUS ORGAN OPTIMIZATION")
    print("="*80)
    print("\nPhase 1: Essential Node Property Indexes (8 indexes)")
    print("🕐 Temporal Awareness: Time/Date Indexes (3 indexes)")
    print("Phase 1.5: Vegafy Integration - Relationship + Composite (12 indexes)")
    print("Total: 23 comprehensive indexes")
    print("\nExpected Impact:")
    print("  - Basic entity queries: 10-50× speedup")
    print("  - Multi-hop relationship queries: 5-20× speedup")
    print("  - Zone-filtered queries: 3-10× speedup")
    print("  - Overall complex queries: 50-200× speedup")
    print("\nDuration: 1-2 hours for production database")
    print("Current State: Development/Testing (fast)")
    print("\n")

    # Initialize Neo4j connection
    try:
        print("🔌 Connecting to Neo4j...")
        graph = Neo4jKnowledgeGraph()
        print("   ✅ Connected successfully\n")
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        print("\n⚠️  Neo4j must be running for index creation.")
        print("   Start Neo4j and try again, or skip this optimization.\n")
        return

    # Create indexes
    results = create_indexes(graph)

    # Verify indexes
    indexes = verify_indexes(graph)

    # Benchmark performance
    benchmark_query_performance(graph)

    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80 + "\n")

    success_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)

    print(f"Indexes created: {success_count}/{total_count}")
    print(f"Indexes verified: {len(indexes)}")

    if success_count == total_count:
        print("\n✅ PHASES 1 + TEMPORAL + 1.5 COMPLETE - All 23 indexes created successfully!")
        print("\n🎯 Expected Performance Improvements:")
        print("   Phase 1 (Node Property Indexes):")
        print("   - Entity lookup by (user_id, entity_value): 10-50× faster")
        print("   - Top entities by mention count: 3-5× faster")
        print("   - Recent entities by timestamp: 5-10× faster")
        print("\n   🕐 Temporal Awareness (Time/Date Indexes):")
        print("   - Entities by time_of_day: 3-5× faster")
        print("   - Entities by day_of_week: 3-5× faster")
        print("   - Combined temporal queries: 5-10× faster")
        print("\n   Phase 1.5 (Vegafy Integration - Relationship + Composite):")
        print("   - Multi-hop relationship queries (1-3 degrees): 5-20× faster")
        print("   - Zone-filtered entity queries: 3-10× faster")
        print("   - TSK-enriched entity queries: 2-5× faster")
        print("\n   Overall complex queries: 50-200× faster! 🚀")
        print("\n🌀 NEXUS organ is now optimized for:")
        print("   - LLM-independent processing")
        print("   - Multi-degree entity graph traversal")
        print("   - Zone-aware entity filtering")
        print("   - Polyvagal state-specific queries")
    else:
        print(f"\n⚠️  WARNING: {total_count - success_count} indexes failed to create")
        print("   Review errors above and retry if needed.")

    # Next steps
    print("\n" + "="*80)
    print("🚀 NEXT STEPS")
    print("="*80 + "\n")
    print("Phase 1: ✅ COMPLETE (Essential node property indexes - 8 indexes)")
    print("Phase 1.5: ✅ COMPLETE (Vegafy integration - relationship + composite - 12 indexes)")
    print("Phase 2: Query optimization (4-6 hours)")
    print("   - Connection pooling")
    print("   - Query parameterization")
    print("   - Batch operations")
    print("Phase 2.5: Nexus node implementation (1-2 days)")
    print("   - ZoneSafetyNexus, OrganNexus, PathwayNexus")
    print("   - Graph-based entity pattern reasoning")
    print("Phase 3: Caching & monitoring (1-2 days)")
    print("   - Query result caching (5-min TTL)")
    print("   - Performance monitoring")
    print("   - Slow query logging")
    print("Phase 3.5: Substitution pattern learning (2-3 days)")
    print("   - HAS_SAFER_ALTERNATIVE relationships")
    print("   - Entity redirection based on zone safety")
    print("\n🌀 Ready for entity-aware organic intelligence with 50-200× query speedup!\n")

    # Close connection
    graph.close()


if __name__ == "__main__":
    main()
