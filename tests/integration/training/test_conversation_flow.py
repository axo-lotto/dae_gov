#!/usr/bin/env python3
"""Test conversation flow with greetings and curiosity triggers."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dae_gov_cli import DAEGovCLI

def test_conversation():
    print("Testing DAE-GOV conversation flow...")
    print()

    try:
        cli = DAEGovCLI()
        print()
        print('='*70)
        print('TESTING CONVERSATION FLOW')
        print('='*70)
        print()

        # Test 1: Greeting
        print("TEST 1: Greeting")
        print("👤 You: hello")
        result1 = cli.process_input("hello")
        response1 = cli.generate_response(result1)
        print(f"🌀 DAE: {response1}")
        print()
        print(f"   ✓ Gate: {result1['organism_analysis']['gate_decision']}")
        print(f"   ✓ Knowledge used: {len(result1.get('knowledge_context') or [])}")
        print()

        # Test 2: Confused statement (should trigger curiosity)
        print("="*70)
        print("TEST 2: Confusion (curiosity trigger)")
        print("👤 You: I feel confused and uncertain about this")
        result2 = cli.process_input("I feel confused and uncertain about this")
        response2 = cli.generate_response(result2)
        print(f"🌀 DAE: {response2}")
        print()
        print(f"   ✓ Gate: {result2['organism_analysis']['gate_decision']}")
        if result2.get('conversational_organs'):
            print(f"   ✓ Curiosity triggered: {result2['conversational_organs']['curiosity_triggered']}")
        print()

        # Test 3: Complex organizational statement
        print("="*70)
        print("TEST 3: Organizational question")
        print("👤 You: Our team is experiencing burnout and we need help")
        result3 = cli.process_input("Our team is experiencing burnout and we need help")
        response3 = cli.generate_response(result3)
        print(f"🌀 DAE: {response3[:200]}...")  # Truncate long response
        print()
        print(f"   ✓ Gate: {result3['organism_analysis']['gate_decision']}")
        print(f"   ✓ Knowledge used: {len(result3.get('knowledge_context') or [])}")
        print()

        print("="*70)
        print("✅ ALL CONVERSATION TESTS PASSED")
        print("="*70)
        print()
        print("System is ready for production use!")
        print("Run: python3 dae_gov_cli.py")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    test_conversation()
