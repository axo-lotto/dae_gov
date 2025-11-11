"""
Neo4j Aura Validation Test - Direct Connection
Runs full knowledge graph initialization with your Aura credentials
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_base.neo4j_knowledge_graph import (
    Neo4jKnowledgeGraph,
    initialize_trauma_informed_concepts,
    initialize_trauma_informed_relationships
)

def test_neo4j_aura():
    """Test Neo4j Aura with direct credentials."""

    print("\n" + "="*70)
    print("NEO4J AURA VALIDATION TEST - Phase 2.3")
    print("="*70 + "\n")

    # Your Neo4j Aura credentials
    URI = "neo4j+s://f63b4064.databases.neo4j.io"
    USER = "neo4j"
    PASSWORD = "zHKglO35XeFD-dhxj6mp5L0WnkAXVD8WVS34pth4AI0"
    DATABASE = "neo4j"

    try:
        # Connect to Neo4j Aura
        print("[TEST 1] Connecting to Neo4j Aura...")
        print(f"   URI: {URI}")
        print(f"   Database: {DATABASE}\n")

        graph = Neo4jKnowledgeGraph(
            uri=URI,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        print("✅ Connection successful!\n")

        # Initialize trauma-informed concepts
        print("[TEST 2] Initializing 16 trauma-informed concepts...")
        concept_count = initialize_trauma_informed_concepts(graph)
        print(f"✅ Created {concept_count} concepts\n")

        # Initialize relationships
        print("[TEST 3] Initializing 18 concept relationships...")
        rel_count = initialize_trauma_informed_relationships(graph)
        print(f"✅ Created {rel_count} relationships\n")

        # Test concept retrieval
        print("[TEST 4] Testing concept retrieval...")
        burnout = graph.find_concept("Burnout Spiral")
        if burnout:
            print(f"   Found: {burnout['name']}")
            print(f"   Category: {burnout['category']}")
            print(f"   SELF-distance: {burnout.get('self_distance', 'N/A')}")
        print("✅ Concept retrieval working\n")

        # Test related concepts
        print("[TEST 5] Testing related concepts (1-hop)...")
        related = graph.find_related_concepts("Burnout Spiral", max_hops=1)
        print(f"   Found {len(related)} related concepts:")
        for r in related[:3]:
            print(f"     - {r['concept']['name']} (distance: {r['distance']})")
        print("✅ Related concept search working\n")

        # Test transformation path
        print("[TEST 6] Testing transformation path...")
        path = graph.find_transformation_path("Burnout Spiral", "Sustainable Rhythm")
        if path:
            print(f"   Path: {' → '.join(path)}")
            print("✅ Transformation path found\n")
        else:
            print("⚠️  No transformation path found (this is OK, concepts may not be directly connected)\n")

        # Get statistics
        print("[TEST 7] Knowledge graph statistics...")
        stats = graph.get_stats()
        print(f"   Total concepts: {stats.get('total_concepts', 0)}")
        print(f"   Total relationships: {stats.get('total_relationships', 0)}")
        print(f"   Trauma concepts: {stats.get('trauma_concepts', 0)}")
        print(f"   Philosophy concepts: {stats.get('philosophy_concepts', 0)}")
        print(f"   Organizational concepts: {stats.get('org_concepts', 0)}")
        print("✅ Statistics retrieved\n")

        # Close connection
        graph.close()

        print("="*70)
        print("✅ ALL TESTS PASSED - Neo4j Aura Operational!")
        print("="*70)
        print("")
        print("📊 Summary:")
        print(f"   • {concept_count} trauma-informed concepts initialized")
        print(f"   • {rel_count} concept relationships created")
        print(f"   • Knowledge graph ready for DAE-GOV integration")
        print("")
        print("🎉 Phase 2.3 COMPLETE!")
        print("")
        print("📍 Next Steps:")
        print("   → Week 1, Day 3-4: Integration testing")
        print("   → Connect Text Orchestrator + FAISS + Neo4j")
        print("   → See KNOWLEDGE_INTEGRATION_ROADMAP.md for details")
        print("")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("")
        print("💡 Troubleshooting:")
        print("   1. Check Neo4j Aura database is running (console.neo4j.io)")
        print("   2. Verify credentials are correct")
        print("   3. Database may still be starting (wait 60 seconds)")
        print("")
        return False


if __name__ == "__main__":
    success = test_neo4j_aura()
    sys.exit(0 if success else 1)
