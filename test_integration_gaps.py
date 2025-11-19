"""
🔍 Integration Gaps Diagnostic Test

Tests the 3 critical integration gaps identified:
1. Polyvagal state showing "unknown"
2. Neo4j entity memory not persisting
3. Organ signatures recording zeros

Date: November 19, 2025
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from knowledge_base.neo4j_knowledge_graph import Neo4jKnowledgeGraph
import json


def test_gap_1_polyvagal_state():
    """Test Gap 1: Polyvagal state capture from EO organ"""
    print("\n" + "=" * 80)
    print("🔍 GAP 1: POLYVAGAL STATE CAPTURE")
    print("=" * 80)

    print("\n📋 Step 1: Initialize organism wrapper")
    wrapper = ConversationalOrganismWrapper()

    print("\n📋 Step 2: Check EO organ initialization")
    if hasattr(wrapper, 'eo') and wrapper.eo:
        print("   ✅ EO organ initialized")
    else:
        print("   ❌ EO organ NOT initialized")
        return False

    print("\n📋 Step 3: Process test message to trigger EO organ")
    test_message = "I'm feeling really stressed and anxious today."

    try:
        result = wrapper.process_text(test_message, user_id="test_user_gap1")
        print(f"   ✅ Message processed: mode={result.get('mode', 'N/A')}")

        # Check if polyvagal state is in result
        felt_states = result.get('felt_states', {})
        polyvagal_in_result = felt_states.get('polyvagal_state', 'NOT_IN_RESULT')
        print(f"   🔍 Polyvagal state in result: '{polyvagal_in_result}'")
    except Exception as e:
        print(f"   ❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n📋 Step 4: Check session transcript for polyvagal state")
    session_files = list(Path("sessions").glob("session_*_test_user_gap1/transcript.jsonl"))

    if not session_files:
        print("   ❌ No session transcript found")
        return False

    latest_session = max(session_files, key=lambda p: p.stat().st_mtime)
    print(f"   📂 Found session: {latest_session.parent.name}")

    with open(latest_session, 'r') as f:
        lines = f.readlines()
        if lines:
            last_turn = json.loads(lines[-1])
            polyvagal_state = last_turn.get('polyvagal_state', 'NOT_FOUND')

            print(f"\n   🔍 Polyvagal state in transcript: '{polyvagal_state}'")

            if polyvagal_state == "unknown":
                print("   ❌ GAP CONFIRMED: Polyvagal state is 'unknown'")
                print("   🔧 This means EO organ is not exporting polyvagal state to felt_states")
                return False
            elif polyvagal_state in ["ventral_vagal", "sympathetic", "dorsal_vagal", "mixed_state"]:
                print(f"   ✅ GAP FIXED: Polyvagal state is valid: '{polyvagal_state}'")
                return True
            else:
                print(f"   ⚠️  Unexpected polyvagal state: '{polyvagal_state}'")
                return False

    print("   ❌ No turns in session transcript")
    return False


def test_gap_2_neo4j_entity_persistence():
    """Test Gap 2: Neo4j entity memory persistence"""
    print("\n" + "=" * 80)
    print("🔍 GAP 2: NEO4J ENTITY PERSISTENCE")
    print("=" * 80)

    print("\n📋 Step 1: Initialize Neo4j connection")
    try:
        graph = Neo4jKnowledgeGraph()
        print("   ✅ Neo4j connection initialized")
    except Exception as e:
        print(f"   ❌ Neo4j connection failed: {e}")
        return False

    print("\n📋 Step 2: Test entity creation")
    test_entity_name = "TestEntity_Gap2_Debug"
    test_user_id = "test_user_gap2"

    try:
        entity_id = graph.create_entity(
            entity_type="Person",
            name=test_entity_name,
            user_id=test_user_id,
            properties={"test": "debug_entity"}
        )
        print(f"   ✅ Entity created: {entity_id}")
    except Exception as e:
        print(f"   ❌ Entity creation failed: {e}")
        return False

    print("\n📋 Step 3: Test entity retrieval by exact name")
    try:
        retrieved = graph.get_entity_by_name(test_entity_name, test_user_id)
        if retrieved:
            print(f"   ✅ Entity retrieved by exact name: {retrieved['name']}")
        else:
            print(f"   ❌ Entity NOT retrieved (returned None)")
            return False
    except Exception as e:
        print(f"   ❌ Entity retrieval failed: {e}")
        return False

    print("\n📋 Step 4: Test fuzzy matching")
    try:
        fuzzy_results = graph.fuzzy_match_entities("TestEntity", test_user_id)
        if fuzzy_results:
            print(f"   ✅ Fuzzy matching works: Found {len(fuzzy_results)} entities")
            for entity in fuzzy_results[:3]:
                print(f"      - {entity['name']} (score: {entity.get('score', 'N/A')})")
        else:
            print(f"   ⚠️  Fuzzy matching returned no results")
    except Exception as e:
        print(f"   ❌ Fuzzy matching failed: {e}")

    print("\n📋 Step 5: Test entity persistence with organism wrapper")
    wrapper = ConversationalOrganismWrapper()

    test_message = f"I talked to {test_entity_name} at the park yesterday."
    print(f"   📝 Test message: \"{test_message}\"")

    try:
        result = wrapper.process_text(test_message, user_id=test_user_id)
        print(f"   ✅ Message processed: mode={result.get('mode', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n📋 Step 6: Check if entity was mentioned and tracked")
    try:
        # Check if entity mention was recorded
        entity_after_mention = graph.get_entity_by_name(test_entity_name, test_user_id)
        if entity_after_mention:
            mention_count = entity_after_mention.get('mention_count', 0)
            print(f"   🔍 Entity mention count: {mention_count}")

            if mention_count >= 1:
                print(f"   ✅ Entity mention tracked in Neo4j")
                return True
            else:
                print(f"   ⚠️  Entity exists but mention count not updated")
                return False
        else:
            print(f"   ❌ Entity disappeared after wrapper processing")
            return False
    except Exception as e:
        print(f"   ❌ Entity check failed: {e}")
        return False


def test_gap_3_organ_signature_recording():
    """Test Gap 3: Organ signatures recording non-zero values"""
    print("\n" + "=" * 80)
    print("🔍 GAP 3: ORGAN SIGNATURE RECORDING")
    print("=" * 80)

    print("\n📋 Step 1: Initialize organism wrapper")
    wrapper = ConversationalOrganismWrapper()

    print("\n📋 Step 2: Process test message with rich content")
    test_message = "I'm really worried about my daughter Emma. She's been feeling anxious about school lately."

    try:
        result = wrapper.process_text(test_message, user_id="test_user_gap3")
        print(f"   ✅ Message processed: mode={result.get('mode', 'N/A')}")

        # Check if organ signatures are in result
        felt_states = result.get('felt_states', {})
        organ_coherences = felt_states.get('organ_coherences', {})
        print(f"   🔍 Organ coherences in result: {len(organ_coherences)} organs")
    except Exception as e:
        print(f"   ❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n📋 Step 3: Check session transcript for organ signatures")
    session_files = list(Path("sessions").glob("session_*_test_user_gap3/transcript.jsonl"))

    if not session_files:
        print("   ❌ No session transcript found")
        return False

    latest_session = max(session_files, key=lambda p: p.stat().st_mtime)
    print(f"   📂 Found session: {latest_session.parent.name}")

    with open(latest_session, 'r') as f:
        lines = f.readlines()
        if lines:
            last_turn = json.loads(lines[-1])
            organ_signatures = last_turn.get('organ_signatures', {})

            print(f"\n   🔍 Organ signatures found: {len(organ_signatures)} organs")

            # Check if any organ has non-zero values
            non_zero_organs = []
            all_zero_organs = []

            for organ_name, signature in organ_signatures.items():
                coherence = signature.get('coherence', 0.0)
                mean = signature.get('mean', 0.0)
                variance = signature.get('variance', 0.0)

                if coherence > 0.0 or mean > 0.0 or variance > 0.0:
                    non_zero_organs.append(organ_name)
                    print(f"   ✅ {organ_name}: coherence={coherence:.3f}, mean={mean:.3f}, variance={variance:.3f}")
                else:
                    all_zero_organs.append(organ_name)

            if non_zero_organs:
                print(f"\n   ✅ {len(non_zero_organs)}/{len(organ_signatures)} organs have non-zero signatures")
                if all_zero_organs:
                    print(f"   ⚠️  {len(all_zero_organs)} organs still at zero: {', '.join(all_zero_organs)}")
                return True
            else:
                print(f"\n   ❌ GAP CONFIRMED: All {len(organ_signatures)} organ signatures are ZERO")
                print("   🔧 This means organ results are not being properly extracted/recorded")
                return False

    print("   ❌ No turns in session transcript")
    return False


def main():
    print("=" * 80)
    print("🔍 DAE INTEGRATION GAPS DIAGNOSTIC TEST")
    print("=" * 80)
    print("\nTesting 3 critical integration gaps:")
    print("1. Polyvagal state showing 'unknown'")
    print("2. Neo4j entity memory not persisting")
    print("3. Organ signatures recording zeros")

    results = {
        "Gap 1 (Polyvagal)": False,
        "Gap 2 (Neo4j)": False,
        "Gap 3 (Organ Signatures)": False
    }

    # Test Gap 1
    try:
        results["Gap 1 (Polyvagal)"] = test_gap_1_polyvagal_state()
    except Exception as e:
        print(f"\n❌ Gap 1 test crashed: {e}")

    # Test Gap 2
    try:
        results["Gap 2 (Neo4j)"] = test_gap_2_neo4j_entity_persistence()
    except Exception as e:
        print(f"\n❌ Gap 2 test crashed: {e}")

    # Test Gap 3
    try:
        results["Gap 3 (Organ Signatures)"] = test_gap_3_organ_signature_recording()
    except Exception as e:
        print(f"\n❌ Gap 3 test crashed: {e}")

    # Summary
    print("\n" + "=" * 80)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 80)

    for gap_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {gap_name}")

    passed_count = sum(results.values())
    total_count = len(results)

    print(f"\n🎯 Overall: {passed_count}/{total_count} gaps resolved")

    if passed_count == total_count:
        print("\n🎉 All integration gaps resolved! System ready for phase learning.")
        return True
    else:
        print(f"\n⚠️  {total_count - passed_count} gap(s) still need fixing.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
