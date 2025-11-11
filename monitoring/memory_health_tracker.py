#!/usr/bin/env python3
"""
Memory Health Tracker for DAE-GOV
=================================

Comprehensive memory system health checks for Bundle/ directory.

Adapted from DAE 3.0 monitoring system for DAE-GOV memory persistence.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MemoryHealth:
    """Health status for memory system."""
    bundle_exists: bool
    total_users: int
    healthy_users: int
    corrupted_users: int
    total_conversations: int
    total_size_mb: float
    oldest_session: Optional[str]
    newest_session: Optional[str]
    r_matrix_total_updates: int
    issues: List[str]
    warnings: List[str]
    health_score: float  # 0.0-1.0


class MemoryHealthTracker:
    """
    Track and validate health of DAE-GOV memory Bundle.

    Features:
    - Bundle directory validation
    - User compartment integrity checks
    - Conversation history verification
    - R-matrix snapshot validation
    - Storage usage monitoring
    - Data corruption detection
    """

    def __init__(self, base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1"):
        self.base_path = Path(base_path)
        self.bundle_path = self.base_path / "Bundle"

    def check_memory_health(self) -> MemoryHealth:
        """
        Comprehensive memory health check.

        Returns:
            MemoryHealth dataclass with complete health status
        """
        issues = []
        warnings = []

        # Check Bundle directory exists
        if not self.bundle_path.exists():
            return MemoryHealth(
                bundle_exists=False,
                total_users=0,
                healthy_users=0,
                corrupted_users=0,
                total_conversations=0,
                total_size_mb=0.0,
                oldest_session=None,
                newest_session=None,
                r_matrix_total_updates=0,
                issues=["Bundle directory does not exist"],
                warnings=[],
                health_score=0.0
            )

        # Scan all users
        total_users = 0
        healthy_users = 0
        corrupted_users = 0
        total_conversations = 0
        total_size_bytes = 0
        r_matrix_total_updates = 0
        all_sessions = []

        for user_dir in self.bundle_path.iterdir():
            if not user_dir.is_dir() or not user_dir.name.startswith('user'):
                continue

            total_users += 1
            user_id = user_dir.name

            # Check user structure
            user_issues, user_warnings = self._check_user_structure(user_id)
            issues.extend(user_issues)
            warnings.extend(user_warnings)

            if user_issues:
                corrupted_users += 1
            else:
                healthy_users += 1

            # Count conversations
            conversations_dir = user_dir / "conversations"
            if conversations_dir.exists():
                conversation_files = list(conversations_dir.glob("*.json"))
                total_conversations += len(conversation_files)

                # Track all session timestamps
                for conv_file in conversation_files:
                    try:
                        with open(conv_file, 'r') as f:
                            conv_data = json.load(f)
                            all_sessions.append({
                                'file': conv_file.name,
                                'start_time': conv_data.get('start_time'),
                                'user_id': user_id
                            })
                    except Exception as e:
                        issues.append(f"Failed to read {user_id}/{conv_file.name}: {e}")

            # Calculate storage size
            total_size_bytes += self._get_directory_size(user_dir)

            # Get R-matrix updates from user state
            user_state_file = user_dir / "user_state.json"
            if user_state_file.exists():
                try:
                    with open(user_state_file, 'r') as f:
                        user_state = json.load(f)
                        r_matrix_total_updates += user_state.get('r_matrix_updates', 0)
                except Exception as e:
                    issues.append(f"Failed to read {user_id}/user_state.json: {e}")

        # Find oldest and newest sessions
        oldest_session = None
        newest_session = None
        if all_sessions:
            # Sort by start_time
            valid_sessions = [s for s in all_sessions if s['start_time']]
            if valid_sessions:
                sorted_sessions = sorted(valid_sessions, key=lambda x: x['start_time'])
                oldest_session = f"{sorted_sessions[0]['user_id']}/{sorted_sessions[0]['file']}"
                newest_session = f"{sorted_sessions[-1]['user_id']}/{sorted_sessions[-1]['file']}"

        # Calculate health score (0.0-1.0)
        health_score = self._calculate_health_score(
            total_users, healthy_users, corrupted_users, issues, warnings
        )

        return MemoryHealth(
            bundle_exists=True,
            total_users=total_users,
            healthy_users=healthy_users,
            corrupted_users=corrupted_users,
            total_conversations=total_conversations,
            total_size_mb=total_size_bytes / (1024 * 1024),
            oldest_session=oldest_session,
            newest_session=newest_session,
            r_matrix_total_updates=r_matrix_total_updates,
            issues=issues,
            warnings=warnings,
            health_score=health_score
        )

    def _check_user_structure(self, user_id: str) -> tuple[List[str], List[str]]:
        """
        Check user directory structure integrity.

        Returns:
            (issues, warnings) tuple
        """
        issues = []
        warnings = []

        user_dir = self.bundle_path / user_id

        # Check required subdirectories
        required_dirs = ['conversations', 'learning', 'r_matrix_snapshots']
        for dir_name in required_dirs:
            dir_path = user_dir / dir_name
            if not dir_path.exists():
                issues.append(f"{user_id}: Missing {dir_name}/ directory")

        # Check user_state.json
        user_state_file = user_dir / "user_state.json"
        if not user_state_file.exists():
            issues.append(f"{user_id}: Missing user_state.json")
        else:
            # Validate user_state.json structure
            try:
                with open(user_state_file, 'r') as f:
                    state = json.load(f)

                required_fields = ['user_id', 'created', 'total_conversations',
                                 'total_turns', 'r_matrix_updates', 'last_active']
                for field in required_fields:
                    if field not in state:
                        issues.append(f"{user_id}: Missing field '{field}' in user_state.json")

                # Warn if never active
                if state.get('last_active') is None and state.get('total_conversations', 0) == 0:
                    warnings.append(f"{user_id}: Never been active")

            except json.JSONDecodeError as e:
                issues.append(f"{user_id}: Corrupted user_state.json - {e}")
            except Exception as e:
                issues.append(f"{user_id}: Error reading user_state.json - {e}")

        return issues, warnings

    def _get_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory in bytes."""
        total_size = 0
        try:
            for item in directory.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
        except Exception:
            pass
        return total_size

    def _calculate_health_score(self, total_users: int, healthy_users: int,
                                corrupted_users: int, issues: List[str],
                                warnings: List[str]) -> float:
        """
        Calculate overall health score (0.0-1.0).

        Factors:
        - User integrity ratio
        - Issue count
        - Warning count
        """
        if total_users == 0:
            return 1.0  # No users yet, but system is healthy

        # User integrity component (0.0-0.7)
        user_ratio = healthy_users / total_users
        user_score = user_ratio * 0.7

        # Issue penalty (up to -0.3)
        issue_penalty = min(len(issues) * 0.1, 0.3)

        # Warning penalty (up to -0.1)
        warning_penalty = min(len(warnings) * 0.02, 0.1)

        final_score = user_score - issue_penalty - warning_penalty
        return max(0.0, min(1.0, final_score))

    def display_health_report(self):
        """Display formatted memory health report."""
        health = self.check_memory_health()

        # Health status indicator
        if health.health_score >= 0.8:
            status_icon = "✅"
            status_text = "HEALTHY"
        elif health.health_score >= 0.5:
            status_icon = "⚠️"
            status_text = "WARNING"
        else:
            status_icon = "❌"
            status_text = "CRITICAL"

        print("\n" + "="*70)
        print(f"{status_icon} MEMORY HEALTH REPORT {status_icon}")
        print("="*70)
        print()

        if not health.bundle_exists:
            print("❌ Bundle directory does not exist")
            print(f"   Expected location: {self.bundle_path}")
            print()
            print("Run to create Bundle:")
            print("   python3 apply_fixes.py")
            print("="*70 + "\n")
            return

        # Overall Status
        print(f"📊 OVERALL STATUS: {status_text}")
        print(f"   Health score: {health.health_score:.2f}/1.00")
        print()

        # Memory System Stats
        print("💾 MEMORY SYSTEM")
        print(f"   Total users: {health.total_users}")
        print(f"   Healthy users: {health.healthy_users}")
        if health.corrupted_users > 0:
            print(f"   ⚠️  Corrupted users: {health.corrupted_users}")
        print(f"   Total conversations: {health.total_conversations:,}")
        print(f"   Storage used: {health.total_size_mb:.2f} MB")
        print(f"   R-matrix updates: {health.r_matrix_total_updates:,}")
        print()

        # Session Range
        if health.oldest_session and health.newest_session:
            print("📅 SESSION HISTORY")
            print(f"   Oldest session: {health.oldest_session}")
            print(f"   Newest session: {health.newest_session}")
            print()

        # Issues
        if health.issues:
            print(f"❌ ISSUES ({len(health.issues)})")
            for issue in health.issues[:10]:  # Show first 10
                print(f"   • {issue}")
            if len(health.issues) > 10:
                print(f"   ... and {len(health.issues) - 10} more")
            print()

        # Warnings
        if health.warnings:
            print(f"⚠️  WARNINGS ({len(health.warnings)})")
            for warning in health.warnings[:10]:  # Show first 10
                print(f"   • {warning}")
            if len(health.warnings) > 10:
                print(f"   ... and {len(health.warnings) - 10} more")
            print()

        # Recommendations
        print("💡 RECOMMENDATIONS")
        if health.health_score >= 0.8:
            print("   ✅ Memory system is healthy - no action needed")
        elif health.corrupted_users > 0:
            print("   🔧 Repair corrupted user directories")
            print("      Check issues above for details")
        elif len(health.warnings) > 0:
            print("   📝 Review warnings and clean up inactive users")

        print("="*70 + "\n")

    def repair_user_structure(self, user_id: str):
        """
        Attempt to repair user directory structure.

        Creates missing directories and initializes user_state.json if needed.
        """
        user_dir = self.bundle_path / user_id

        print(f"\n🔧 Repairing user structure: {user_id}")
        print("="*70)

        # Create user directory if missing
        if not user_dir.exists():
            user_dir.mkdir(parents=True)
            print(f"✅ Created {user_id}/ directory")

        # Create required subdirectories
        required_dirs = ['conversations', 'learning', 'r_matrix_snapshots']
        for dir_name in required_dirs:
            dir_path = user_dir / dir_name
            if not dir_path.exists():
                dir_path.mkdir(exist_ok=True)
                print(f"✅ Created {user_id}/{dir_name}/ directory")

        # Create user_state.json if missing
        user_state_file = user_dir / "user_state.json"
        if not user_state_file.exists():
            user_state = {
                "user_id": user_id,
                "created": datetime.now().isoformat(),
                "total_conversations": 0,
                "total_turns": 0,
                "r_matrix_updates": 0,
                "last_active": None
            }
            with open(user_state_file, 'w') as f:
                json.dump(user_state, f, indent=2)
            print(f"✅ Created {user_id}/user_state.json")

        print("="*70)
        print(f"✅ Repair complete for {user_id}\n")

    def get_user_memory_usage(self, user_id: str) -> Dict:
        """Get detailed memory usage for specific user."""
        user_dir = self.bundle_path / user_id

        if not user_dir.exists():
            return {
                'error': f'User {user_id} not found',
                'exists': False
            }

        # Calculate sizes for each subdirectory
        conversations_size = self._get_directory_size(user_dir / "conversations")
        learning_size = self._get_directory_size(user_dir / "learning")
        snapshots_size = self._get_directory_size(user_dir / "r_matrix_snapshots")

        # Count files
        conversations_count = len(list((user_dir / "conversations").glob("*.json")))
        snapshots_count = len(list((user_dir / "r_matrix_snapshots").glob("*.json")))

        return {
            'user_id': user_id,
            'exists': True,
            'total_size_mb': (conversations_size + learning_size + snapshots_size) / (1024 * 1024),
            'conversations': {
                'count': conversations_count,
                'size_mb': conversations_size / (1024 * 1024)
            },
            'learning': {
                'size_mb': learning_size / (1024 * 1024)
            },
            'r_matrix_snapshots': {
                'count': snapshots_count,
                'size_mb': snapshots_size / (1024 * 1024)
            }
        }


# Convenience functions
def create_memory_tracker(base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1") -> MemoryHealthTracker:
    """Create memory health tracker instance."""
    return MemoryHealthTracker(base_path)


def quick_memory_check(base_path: str = "/Users/daedalea/Desktop/DAE_HYPHAE_1"):
    """Quick memory health check and display."""
    tracker = MemoryHealthTracker(base_path)
    tracker.display_health_report()


if __name__ == "__main__":
    # Test memory health tracker
    print("Testing DAE-GOV Memory Health Tracker...")
    print()

    tracker = MemoryHealthTracker()

    # Display health report
    tracker.display_health_report()

    # Check if Bundle exists, if not suggest repair
    health = tracker.check_memory_health()
    if not health.bundle_exists:
        print("💡 Tip: Run apply_fixes.py to create Bundle structure")
    elif health.corrupted_users > 0:
        print(f"💡 Tip: Use tracker.repair_user_structure(user_id) to fix corrupted users")

    print("\n✅ Memory health tracker operational")
