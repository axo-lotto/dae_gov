#!/usr/bin/env python3
"""
Rebuild user_registry.json from existing user state files
Recovers lost user data after registry corruption/reset

Usage:
    python3 rebuild_user_registry.py
"""

import json
from pathlib import Path
from datetime import datetime

def rebuild_registry():
    """Scan users/ directory and rebuild registry from state files."""

    users_dir = Path('persona_layer/users')
    registry_path = Path('persona_layer/user_registry.json')

    # Backup existing registry
    if registry_path.exists():
        backup_path = registry_path.with_suffix(f'.json.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        with open(registry_path, 'r') as f:
            old_registry = json.load(f)
        with open(backup_path, 'w') as f:
            json.dump(old_registry, f, indent=2)
        print(f"📦 Backed up old registry to: {backup_path}")
        print(f"   Old registry had {len(old_registry)} users\n")

    # Scan for all user state files
    state_files = list(users_dir.glob('user_*_state.json'))
    # Filter out test users
    state_files = [f for f in state_files if not f.stem.startswith('test_')]

    print(f"🔍 Found {len(state_files)} user state files\n")

    new_registry = {}

    for state_file in sorted(state_files):
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)

            user_id = state.get('user_id')
            if not user_id:
                print(f"⚠️  Skipping {state_file.name}: No user_id found")
                continue

            username = state.get('username', user_id)
            created_at = state.get('created_at', datetime.now().isoformat())
            session_history = state.get('session_history', [])

            # Calculate stats
            total_sessions = len(session_history)
            total_turns = sum(s.get('turns', 0) for s in session_history)

            new_registry[user_id] = {
                'user_id': user_id,
                'username': username,
                'created_at': created_at,
                'total_sessions': total_sessions,
                'total_turns': total_turns,
                'organic_family_id': state.get('organic_family_id'),
                'user_state_path': str(state_file)
            }

            print(f"✅ {username} ({user_id})")
            print(f"   Sessions: {total_sessions}, Turns: {total_turns}")
            if session_history:
                last_session = session_history[-1]
                print(f"   Last session: {last_session.get('timestamp', 'unknown')}")
            print()

        except Exception as e:
            print(f"❌ Error processing {state_file.name}: {e}\n")
            continue

    # Save new registry
    with open(registry_path, 'w') as f:
        json.dump(new_registry, f, indent=2)

    print("="*70)
    print(f"✅ Registry rebuilt successfully!")
    print(f"   Total users: {len(new_registry)}")
    print(f"   Saved to: {registry_path}")
    print("="*70)

    # Show summary sorted by activity
    print("\n📊 Users by activity:")
    users_by_activity = sorted(
        new_registry.values(),
        key=lambda u: (u['total_sessions'], u['total_turns']),
        reverse=True
    )

    for i, user in enumerate(users_by_activity, 1):
        print(f"{i:2}. {user['username']:20} | Sessions: {user['total_sessions']:3} | Turns: {user['total_turns']:4} | Created: {user['created_at'][:10]}")

    print("\n✅ Done! You can now login with existing users in dae_interactive.py")

if __name__ == '__main__':
    rebuild_registry()
