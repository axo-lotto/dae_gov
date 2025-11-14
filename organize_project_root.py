"""
Organize Project Root Directory
November 13, 2025

Moves documentation files to appropriate subdirectories to clean up root.
Currently: 189 files in root
Target: ~10 essential files in root

Organization strategy:
- docs/sessions/ - Session summaries (SESSION_*.md, COMPLETE_*.md)
- docs/enhancements/ - Enhancement completion docs (ENHANCEMENT_*.md)
- docs/training/ - Training reports (BASELINE_*.md, ARC_TRAINING_*.md, EPOCH_*.md)
- docs/analysis/ - Analysis documents (ANALYSIS_*.md, DIAGNOSTIC_*.md, ASSESSMENT_*.md)
- docs/roadmaps/ - Planning documents (*_ROADMAP_*.md, *_PLAN_*.md)
- docs/archive/ - Old/deprecated docs
- Keep in root: CLAUDE.md, DEVELOPMENT_GUIDE.md, QUICK_REFERENCE.md, README.md
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

# Essential files to keep in root
ESSENTIAL_FILES = {
    'CLAUDE.md',
    'DEVELOPMENT_GUIDE.md',
    'QUICK_REFERENCE.md',
    'README.md',
    'config.py',
    'dae_orchestrator.py',
    'dae_interactive.py',
    'dae_gov_cli.py'
}

# Organization mapping (patterns -> destination)
ORGANIZATION_MAP = {
    'docs/sessions/': [
        'SESSION_*',
        'COMPLETE_SESSION_*',
        '*_COMPLETE_NOV*.md'
    ],
    'docs/enhancements/': [
        'ENHANCEMENT_*',
        'REGIME_*',
        'R_MATRIX_*',
        'FAMILY_*'
    ],
    'docs/training/': [
        'BASELINE_*',
        'ARC_TRAINING_*',
        'EPOCH_*',
        'TRAINING_*'
    ],
    'docs/analysis/': [
        'ANALYSIS_*',
        'DIAGNOSTIC_*',
        'ASSESSMENT_*',
        'AUDIT_*',
        'BOTTLENECK_*'
    ],
    'docs/roadmaps/': [
        '*_ROADMAP_*',
        '*_PLAN_*',
        'INTELLIGENCE_EMERGENCE_*',
        'ACTIVATION_*'
    ],
    'docs/architecture/': [
        'ARCHITECTURAL_*',
        'ARCHITECTURE_*',
        'CODEBASE_*'
    ],
    'docs/implementation/': [
        '*_IMPLEMENTATION_*',
        '*_INTEGRATION_*',
        'CONVERSATIONAL_LURE_*'
    ],
    'docs/archive/': [
        'ATOM_EXPANSION.md',
        'CLEAN_RERUN_*',
        'CORPUS_*',
        'CRITICAL_BUG_*'
    ]
}

def should_keep_in_root(filename):
    """Check if file should stay in root."""
    return filename in ESSENTIAL_FILES

def get_destination_dir(filename):
    """Determine destination directory for a file."""
    from fnmatch import fnmatch

    for dest_dir, patterns in ORGANIZATION_MAP.items():
        for pattern in patterns:
            if fnmatch(filename, pattern):
                return dest_dir

    # Default: move to docs/misc/
    return 'docs/misc/'

def organize_root():
    """Organize root directory."""
    print("\n" + "="*70)
    print("🗂️  ORGANIZING PROJECT ROOT")
    print("="*70)

    # Get all .md files in root
    root = Path('.')
    md_files = [f for f in root.glob('*.md') if f.is_file()]

    print(f"\n📊 Found {len(md_files)} .md files in root")

    # Count files to move
    to_move = defaultdict(list)
    to_keep = []

    for md_file in md_files:
        filename = md_file.name

        if should_keep_in_root(filename):
            to_keep.append(filename)
        else:
            dest_dir = get_destination_dir(filename)
            to_move[dest_dir].append(filename)

    print(f"\n📌 Keeping in root: {len(to_keep)} files")
    for f in sorted(to_keep):
        print(f"   ✅ {f}")

    print(f"\n📦 Moving: {len(md_files) - len(to_keep)} files")
    for dest_dir, files in sorted(to_move.items()):
        print(f"\n   {dest_dir} ({len(files)} files)")
        for f in sorted(files)[:5]:  # Show first 5
            print(f"      - {f}")
        if len(files) > 5:
            print(f"      ... and {len(files) - 5} more")

    # Ask for confirmation
    print("\n" + "="*70)
    response = input("Proceed with organization? (yes/no): ").strip().lower()

    if response != 'yes':
        print("❌ Organization cancelled")
        return

    # Create destination directories
    for dest_dir in to_move.keys():
        Path(dest_dir).mkdir(parents=True, exist_ok=True)

    # Move files
    moved_count = 0
    for dest_dir, files in to_move.items():
        for filename in files:
            src = Path(filename)
            dst = Path(dest_dir) / filename

            try:
                shutil.move(str(src), str(dst))
                moved_count += 1
            except Exception as e:
                print(f"   ⚠️  Error moving {filename}: {e}")

    print(f"\n✅ Moved {moved_count} files")
    print(f"📁 Root directory now has {len(to_keep)} essential .md files")

    # Summary
    print("\n" + "="*70)
    print("✅ ORGANIZATION COMPLETE")
    print("="*70)

    print(f"\n📊 Summary:")
    print(f"   Files in root: {len(to_keep)}")
    print(f"   Files organized: {moved_count}")

    print(f"\n📁 Root directory structure:")
    print(f"   CLAUDE.md - Main development guide")
    print(f"   DEVELOPMENT_GUIDE.md - Comprehensive guide")
    print(f"   QUICK_REFERENCE.md - Daily workflow")
    print(f"   README.md - Project overview")
    print(f"   config.py - Configuration")
    print(f"   dae_orchestrator.py - Main entry point")
    print(f"   dae_interactive.py - Interactive mode")

    print(f"\n📂 Documentation organized into:")
    for dest_dir in sorted(to_move.keys()):
        count = len(to_move[dest_dir])
        print(f"   {dest_dir} - {count} files")

if __name__ == "__main__":
    organize_root()
