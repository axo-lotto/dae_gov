"""
Memory Persistence & Scalability Audit
=======================================

Audits:
1. Superject persistent state per user
2. Memory management (hebbian, families, sessions)
3. Scalability (file sizes, growth rates, cleanup)

Date: November 13, 2025
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

def get_file_info(filepath):
    """Get file size and modification time."""
    if os.path.exists(filepath):
        stat = os.stat(filepath)
        return {
            'exists': True,
            'size_bytes': stat.st_size,
            'size_kb': round(stat.st_size / 1024, 2),
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
    return {'exists': False}

def audit_memory_files():
    """Audit all memory/state persistence files."""

    print("="*80)
    print("🧠 Memory Persistence & Scalability Audit")
    print("="*80)
    print()

    audit_results = {
        'audit_date': datetime.now().isoformat(),
        'files': {},
        'warnings': [],
        'recommendations': []
    }

    # Files to audit
    memory_files = {
        'hebbian_memory': 'persona_layer/conversational_hebbian_memory.json',
        'hebbian_memory_backup': 'TSK/conversational_hebbian_memory.json',
        'organic_families': 'persona_layer/organic_families.json',
        'organic_families_backup': 'persona_layer/organic_families_backup_nov12.json',
        'coherent_attractors': 'persona_layer/coherent_attractors.json',
        'semantic_atoms': 'persona_layer/semantic_atoms.json',
        'shared_meta_atoms': 'persona_layer/shared_meta_atoms.json',
        'meta_atom_rules': 'persona_layer/meta_atom_activation_rules.json',
        'session_registry': 'sessions/session_registry.json',
        'global_organism_state': 'TSK/global_organism_state.json',
        'mycelial_identity': 'monitoring/mycelial_identity.json'
    }

    print("📁 File Status:")
    print("-" * 80)

    for name, filepath in memory_files.items():
        info = get_file_info(filepath)
        audit_results['files'][name] = {
            'path': filepath,
            **info
        }

        if info['exists']:
            size_str = f"{info['size_kb']} KB" if info['size_kb'] < 1024 else f"{info['size_mb']} MB"
            print(f"✅ {name:30} {size_str:>15}  {filepath}")

            # Warnings for large files
            if info['size_mb'] > 10:
                warning = f"{name} is large ({info['size_mb']} MB) - consider cleanup/archival"
                audit_results['warnings'].append(warning)
        else:
            print(f"❌ {name:30} {'NOT FOUND':>15}  {filepath}")

    print()

    # Audit user-specific states
    print("👤 User State Management:")
    print("-" * 80)

    bundle_dir = Path('Bundle')
    if bundle_dir.exists():
        user_dirs = list(bundle_dir.glob('user_link_*'))
        print(f"User bundles found: {len(user_dirs)}")

        for user_dir in user_dirs:
            user_id = user_dir.name
            user_state_file = user_dir / 'user_state.json'

            if user_state_file.exists():
                info = get_file_info(str(user_state_file))
                print(f"  {user_id}: {info['size_kb']} KB")

                audit_results['files'][f'user_state_{user_id}'] = {
                    'path': str(user_state_file),
                    **info
                }
    else:
        print("  No Bundle directory found")

    print()

    # Audit sessions
    print("💬 Session Management:")
    print("-" * 80)

    sessions_dir = Path('sessions')
    if sessions_dir.exists():
        session_dirs = list(sessions_dir.glob('session_link_*'))
        print(f"Session directories: {len(session_dirs)}")

        total_session_size = 0
        for session_dir in session_dirs[:5]:  # Show first 5
            session_files = list(session_dir.glob('*.json'))
            session_size = sum(f.stat().st_size for f in session_files)
            total_session_size += session_size
            print(f"  {session_dir.name}: {len(session_files)} files, {round(session_size/1024, 2)} KB")

        if len(session_dirs) > 5:
            print(f"  ... and {len(session_dirs) - 5} more sessions")

        print(f"\nTotal session storage: {round(total_session_size/1024, 2)} KB")

        if total_session_size > 10 * 1024 * 1024:  # > 10 MB
            audit_results['warnings'].append(
                f"Session storage is large ({round(total_session_size/(1024*1024), 2)} MB) - consider archival strategy"
            )
    else:
        print("  No sessions directory found")

    print()

    # Analyze memory content
    print("🔍 Memory Content Analysis:")
    print("-" * 80)

    # Hebbian memory
    hebbian_path = 'persona_layer/conversational_hebbian_memory.json'
    if os.path.exists(hebbian_path):
        with open(hebbian_path, 'r') as f:
            hebbian = json.load(f)

        r_matrix = hebbian.get('R_matrix', {})
        conversations = hebbian.get('conversations_processed', 0)

        print(f"Hebbian R-matrix:")
        print(f"  Organ couplings tracked: {len(r_matrix)} organs")
        print(f"  Conversations processed: {conversations}")

        audit_results['hebbian_analysis'] = {
            'organs_tracked': len(r_matrix),
            'conversations': conversations
        }

    # Organic families
    families_path = 'persona_layer/organic_families.json'
    if os.path.exists(families_path):
        with open(families_path, 'r') as f:
            families = json.load(f)

        families_dict = families.get('families', {})
        if isinstance(families_dict, dict):
            family_list = list(families_dict.values())
        else:
            family_list = families_dict

        mature = sum(1 for f in family_list if f.get('status') == 'mature')
        total_convs = sum(len(f.get('member_conversations', [])) for f in family_list)

        print(f"\nOrganic families:")
        print(f"  Total families: {len(family_list)}")
        print(f"  Mature families: {mature}")
        print(f"  Total conversations: {total_convs}")

        audit_results['families_analysis'] = {
            'total_families': len(family_list),
            'mature_families': mature,
            'conversations': total_convs
        }

    print()

    # Recommendations
    print("💡 Recommendations:")
    print("-" * 80)

    recommendations = []

    # Check for cleanup needs
    if os.path.exists(hebbian_path):
        info = get_file_info(hebbian_path)
        if info['size_mb'] > 5:
            recommendations.append("Consider implementing Hebbian memory pruning for old/low-weight couplings")

    if os.path.exists(families_path):
        with open(families_path, 'r') as f:
            families = json.load(f)
        families_dict = families.get('families', {})
        num_families = len(families_dict) if isinstance(families_dict, dict) else len(families_dict)
        if num_families > 10:
            recommendations.append("Consider archiving inactive families (no recent conversations)")

    # Session cleanup
    if sessions_dir.exists() and len(list(sessions_dir.glob('session_link_*'))) > 20:
        recommendations.append("Implement session archival/cleanup for sessions older than 30 days")

    # User state scalability
    if bundle_dir.exists() and len(list(bundle_dir.glob('user_link_*'))) > 100:
        recommendations.append("Consider database migration for user states at scale (>100 users)")

    if not recommendations:
        recommendations.append("✅ Memory management looks healthy - no immediate actions needed")

    for rec in recommendations:
        print(f"  • {rec}")
        audit_results['recommendations'].append(rec)

    print()

    # Warnings
    if audit_results['warnings']:
        print("⚠️  Warnings:")
        print("-" * 80)
        for warning in audit_results['warnings']:
            print(f"  ⚠️  {warning}")
        print()

    # Save audit results
    os.makedirs('results', exist_ok=True)
    output_file = f"results/memory_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(audit_results, f, indent=2)

    print("="*80)
    print(f"✅ Audit Complete!")
    print(f"📁 Results saved to: {output_file}")
    print("="*80)

    return audit_results


if __name__ == "__main__":
    audit_memory_files()
