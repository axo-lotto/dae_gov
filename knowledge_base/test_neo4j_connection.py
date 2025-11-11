"""
Quick Neo4j Connection Test
Run this after setting up your Neo4j database
"""

def test_neo4j_connection():
    """Test Neo4j connection with your credentials."""

    print("\n" + "="*70)
    print("NEO4J CONNECTION TEST")
    print("="*70 + "\n")

    print("📝 INSTRUCTIONS:")
    print("   1. Set up Neo4j (choose one option):")
    print("      - Option A: Neo4j Aura Free → https://neo4j.com/cloud/aura-free/")
    print("      - Option B: Neo4j Desktop → https://neo4j.com/download/")
    print("")
    print("   2. Update the credentials below with your database info")
    print("   3. Run this script: python3 knowledge_base/test_neo4j_connection.py")
    print("")

    # ==========================================
    # NEO4J AURA CREDENTIALS (from credentials file)
    # ==========================================

    # For Aura Free (cloud):
    URI = "neo4j+s://f63b4064.databases.neo4j.io"

    USER = "neo4j"
    PASSWORD = "zHKglO35XeFD-dhxj6mp5L0WnkAXVD8WVS34pth4AI0"
    DATABASE = "neo4j"

    # ==========================================

    if PASSWORD == "your_password_here":
        print("⚠️  ERROR: Please update the PASSWORD variable in this script first!")
        print("   Edit line 31 in test_neo4j_connection.py")
        return False

    try:
        from neo4j_knowledge_graph import Neo4jKnowledgeGraph

        print("🔌 Connecting to Neo4j...")
        print(f"   URI: {URI}")
        print(f"   Database: {DATABASE}\n")

        # Create knowledge graph
        kg = Neo4jKnowledgeGraph(
            uri=URI,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        print("\n✅ CONNECTION SUCCESSFUL!")
        print("")
        print("📊 Running full test (initializing 16 concepts + 18 relationships)...")
        print("   This will take ~5 seconds...\n")

        # Run the built-in test
        from neo4j_knowledge_graph import test_neo4j_knowledge_graph
        test_neo4j_knowledge_graph()

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the DAE_HYPHAE_1 directory")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("")
        print("💡 TROUBLESHOOTING:")
        print("   1. Check your Neo4j database is running")
        print("   2. Verify URI, username, password are correct")
        print("   3. For Aura: Make sure URI starts with 'neo4j+s://'")
        print("   4. For local: Make sure URI is 'bolt://localhost:7687'")
        return False


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Add parent directory to path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    test_neo4j_connection()
