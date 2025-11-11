#!/usr/bin/env python3
"""
Test Monitoring Integration for DAE-GOV
========================================

Validates that all monitoring systems work correctly:
1. Session tracking
2. Health dashboard
3. Memory health tracker
4. Bundle directory structure

Run after apply_fixes.py to verify the complete monitoring system.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from monitoring.session_tracker import SessionTracker
from monitoring.health_dashboard import HealthDashboard, SimpleDashboard
from monitoring.memory_health_tracker import MemoryHealthTracker
from datetime import datetime

def test_bundle_structure():
    """Test that Bundle/ directory exists with correct structure."""
    print("\n" + "="*70)
    print("TEST 1: Bundle Structure")
    print("="*70)

    bundle_path = Path("/Users/daedalea/Desktop/DAE_HYPHAE_1/Bundle")

    if not bundle_path.exists():
        print("❌ Bundle directory not found")
        print("   Run: python3 apply_fixes.py")
        return False

    print(f"✅ Bundle exists: {bundle_path}")

    # Check user directories
    user_dirs = list(bundle_path.glob("user*"))
    print(f"✅ Found {len(user_dirs)} user directories")

    # Check structure of user0
    user0 = bundle_path / "user0"
    required_dirs = ['conversations', 'learning', 'r_matrix_snapshots']
    for dir_name in required_dirs:
        if (user0 / dir_name).exists():
            print(f"✅ {user0.name}/{dir_name}/ exists")
        else:
            print(f"❌ {user0.name}/{dir_name}/ missing")
            return False

    # Check user_state.json
    if (user0 / "user_state.json").exists():
        print(f"✅ {user0.name}/user_state.json exists")
    else:
        print(f"❌ {user0.name}/user_state.json missing")
        return False

    return True

def test_session_tracker():
    """Test session tracking functionality."""
    print("\n" + "="*70)
    print("TEST 2: Session Tracker")
    print("="*70)

    try:
        tracker = SessionTracker()

        # Start a test session
        session_id = tracker.start_session("user0")
        print(f"✅ Session started: {session_id}")

        # Record a few test turns
        for i in range(3):
            result = {
                'timestamp': datetime.now().isoformat(),
                'organism_analysis': {
                    'gate_decision': 'RESPOND' if i > 0 else 'GREETING',
                    'polyvagal_state': 'ventral',
                    'self_energy': 0.8
                },
                'knowledge_context': [{'source': 'test'}] if i > 0 else None,
                'conversational_organs': {
                    'curiosity_triggered': i == 2,
                    'r_matrix_updates': 10 + i,
                    'organ_results': {
                        'LISTENING': type('obj', (object,), {'coherence': 0.7})(),
                        'EMPATHY': type('obj', (object,), {'coherence': 0.8})()
                    }
                }
            }
            tracker.record_turn(f"Test input {i}", result, f"Test response {i}")
            print(f"✅ Recorded turn {i+1}")

        # End session
        metrics = tracker.end_session(r_matrix_final=13)
        print(f"✅ Session ended")
        print(f"   Total turns: {metrics.total_turns}")
        print(f"   Curiosity triggers: {metrics.curiosity_triggers}")

        # Get user stats
        stats = tracker.get_user_stats("user0")
        if stats['exists']:
            print(f"✅ User stats retrieved")
            print(f"   Total conversations: {stats['state']['total_conversations']}")
            print(f"   Total turns: {stats['state']['total_turns']}")

        return True

    except Exception as e:
        print(f"❌ Session tracker test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_health_dashboard():
    """Test health dashboard functionality."""
    print("\n" + "="*70)
    print("TEST 3: Health Dashboard")
    print("="*70)

    try:
        dashboard = HealthDashboard()

        # Get current health
        health = dashboard.get_current_health()
        print(f"✅ Health check completed")
        print(f"   R-matrix updates: {health.r_matrix_updates}")
        print(f"   Maturation level: {health.maturation_level}")
        print(f"   Health status: {health.health_status}")

        # Get system status
        system_status = dashboard.get_system_status()
        print(f"✅ System status retrieved")
        print(f"   Total users: {system_status['total_users']}")
        print(f"   Total conversations: {system_status['total_conversations']}")

        # Test simple dashboard
        simple = SimpleDashboard()
        status_line = simple.get_status_line()
        print(f"✅ Status line: {status_line}")

        return True

    except Exception as e:
        print(f"❌ Health dashboard test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_health_tracker():
    """Test memory health tracker functionality."""
    print("\n" + "="*70)
    print("TEST 4: Memory Health Tracker")
    print("="*70)

    try:
        tracker = MemoryHealthTracker()

        # Check memory health
        health = tracker.check_memory_health()
        print(f"✅ Memory health check completed")
        print(f"   Bundle exists: {health.bundle_exists}")
        print(f"   Total users: {health.total_users}")
        print(f"   Healthy users: {health.healthy_users}")
        print(f"   Health score: {health.health_score:.2f}/1.00")

        if health.issues:
            print(f"⚠️  Issues found: {len(health.issues)}")
            for issue in health.issues[:3]:
                print(f"      • {issue}")

        # Get user memory usage
        usage = tracker.get_user_memory_usage("user0")
        if usage['exists']:
            print(f"✅ User memory usage retrieved")
            print(f"   Total size: {usage['total_size_mb']:.2f} MB")
            print(f"   Conversations: {usage['conversations']['count']}")

        return True

    except Exception as e:
        print(f"❌ Memory health tracker test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*70)
    print("DAE-GOV MONITORING INTEGRATION TEST")
    print("="*70)

    results = []

    # Run tests
    results.append(("Bundle Structure", test_bundle_structure()))
    results.append(("Session Tracker", test_session_tracker()))
    results.append(("Health Dashboard", test_health_dashboard()))
    results.append(("Memory Health Tracker", test_memory_health_tracker()))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Results: {passed}/{total} tests passed")
    print()

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print()
        print("Next steps:")
        print("1. Test the full CLI: python3 dae_gov_cli.py")
        print("2. Use 'status' command to see health dashboard")
        print("3. Verify session tracking saves to Bundle/")
        print()
        return 0
    else:
        print("⚠️  SOME TESTS FAILED")
        print()
        print("Troubleshooting:")
        print("1. Ensure apply_fixes.py was run successfully")
        print("2. Check that Bundle/ directory exists")
        print("3. Verify all monitoring files are present")
        print()
        return 1

if __name__ == "__main__":
    exit(main())
