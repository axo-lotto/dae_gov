#!/usr/bin/env python3
"""
Apply critical fixes to DAE-GOV CLI:
1. Fix timestamp KeyError
2. Add dynamic state glyphs to DAE handle
3. Create memory bundle directories

Run after to complete the full memory system setup.
"""

import re
from datetime import datetime
from pathlib import Path

def apply_timestamp_fixes():
    """Add timestamp to all return statements in process_input."""

    file_path = Path("/Users/daedalea/Desktop/DAE_HYPHAE_1/dae_gov_cli.py")
    content = file_path.read_text()

    # Get current timestamp format
    timestamp = datetime.now().isoformat()

    # Fix 1: Add timestamp to greeting return (around line 302)
    content = re.sub(
        r"(return \{\s+'cascade_state'.*?'conversational_organs': None  # Skip organ processing for greetings\s+\})",
        lambda m: m.group(1).replace(
            "'conversational_organs': None  # Skip organ processing for greetings\n            }",
            "'conversational_organs': None,  # Skip organ processing for greetings\n                'timestamp': datetime.now().isoformat()\n            }"
        ),
        content,
        count=1,
        flags=re.DOTALL
    )

    # Fix 2: Add timestamp to curiosity return (around line 335)
    content = re.sub(
        r"(return \{\s+'cascade_state'.*?'conversational_organs': conversational_analysis\s+\})",
        lambda m: m.group(1).replace(
            "'conversational_organs': conversational_analysis\n            }",
            "'conversational_organs': conversational_analysis,\n                'timestamp': datetime.now().isoformat()\n            }"
        ),
        content,
        count=1,
        flags=re.DOTALL
    )

    # Fix 3: Add datetime import at top
    if 'from datetime import datetime' not in content:
        # Find the import section and add datetime import
        content = re.sub(
            r'(import sys\nfrom pathlib import Path)',
            r'\1\nfrom datetime import datetime',
            content
        )

    file_path.write_text(content)
    print("✅ Applied timestamp fixes to dae_gov_cli.py")

def add_dynamic_glyph_system():
    """Add dynamic glyph system based on organism state."""

    file_path = Path("/Users/daedalea/Desktop/DAE_HYPHAE_1/dae_gov_cli.py")
    content = file_path.read_text()

    # Add get_state_glyph method after __init__
    glyph_method = '''
    def get_state_glyph(self) -> str:
        """
        Get dynamic glyph based on organism state.

        Glyphs reflect R-matrix maturation and conversational energy:
        - 🌱 New/learning (updates < 50)
        - 🌿 Growing (updates 50-200)
        - 🌀 Mature/flowing (updates 200-500)
        - ✨ Masterful (updates 500+)
        - 🔥 High energy state (recent high coherence)
        - 💫 Transcendent (all organs highly aligned)
        """

        # Get R-matrix state
        r_updates = self.conversational_r_matrix.update_count

        # Check for recent high coherence (if we have organ history)
        try:
            if hasattr(self, '_recent_coherence_avg'):
                if self._recent_coherence_avg > 0.8:
                    return '💫'  # Transcendent
                elif self._recent_coherence_avg > 0.7:
                    return '🔥'  # High energy
        except:
            pass

        # Based on maturation level
        if r_updates >= 500:
            return '✨'  # Masterful
        elif r_updates >= 200:
            return '🌀'  # Mature
        elif r_updates >= 50:
            return '🌿'  # Growing
        else:
            return '🌱'  # New
    '''

    # Find the right place to insert (after __init__ method)
    init_end = content.find('self.conversation_history = []')
    if init_end != -1:
        # Find the next method definition
        next_method = content.find('\n    def ', init_end)
        if next_method != -1:
            content = content[:next_method] + glyph_method + content[next_method:]

    # Update the response display line (around line 620)
    content = re.sub(
        r'print\(f"\\n🌀 DAE: \{response\}\\n"\)',
        r'print(f"\\n{self.get_state_glyph()} DAE: {response}\\n")',
        content
    )

    file_path.write_text(content)
    print("✅ Added dynamic glyph system")

def create_memory_bundle_structure():
    """Create Bundle/ directory structure for memory persistence."""

    base_path = Path("/Users/daedalea/Desktop/DAE_HYPHAE_1")

    # Create main Bundle directory
    bundle_dir = base_path / "Bundle"
    bundle_dir.mkdir(exist_ok=True)

    # Create user directories
    for i in range(5):  # Create user0-user4 initially
        user_dir = bundle_dir / f"user{i}"
        user_dir.mkdir(exist_ok=True)

        # Create subdirectories for each user
        (user_dir / "conversations").mkdir(exist_ok=True)
        (user_dir / "learning").mkdir(exist_ok=True)
        (user_dir / "r_matrix_snapshots").mkdir(exist_ok=True)

        # Create initial user state file
        user_state_file = user_dir / "user_state.json"
        if not user_state_file.exists():
            import json
            user_state = {
                "user_id": f"user{i}",
                "created": datetime.now().isoformat(),
                "total_conversations": 0,
                "total_turns": 0,
                "r_matrix_updates": 0,
                "last_active": None
            }
            user_state_file.write_text(json.dumps(user_state, indent=2))

    # Create monitoring directory
    monitoring_dir = base_path / "monitoring"
    monitoring_dir.mkdir(exist_ok=True)

    # Create README for Bundle
    readme = bundle_dir / "README.md"
    readme.write_text("""# DAE-GOV Memory Bundle

## Structure

- `user0/`, `user1/`, etc. - Per-user memory compartments
  - `conversations/` - Conversation logs
  - `learning/` - Learning progression data
  - `r_matrix_snapshots/` - R-matrix state over time

- `../monitoring/` - System health monitoring

## Usage

Each user gets isolated memory. The system automatically:
1. Tracks R-matrix updates per user
2. Saves conversation history
3. Monitors learning progression
4. Creates periodic snapshots

## Monitoring

Run health checks:
```bash
python3 monitoring/health_check.py
```
""")

    print(f"✅ Created Bundle structure at {bundle_dir}")
    print(f"   Created 5 user directories (user0-user4)")
    print(f"   Created monitoring infrastructure")

def main():
    print("="*70)
    print("DAE-GOV CRITICAL FIXES APPLICATION")
    print("="*70)
    print()

    try:
        print("1. Applying timestamp fixes...")
        apply_timestamp_fixes()
        print()

        print("2. Adding dynamic glyph system...")
        add_dynamic_glyph_system()
        print()

        print("3. Creating memory bundle structure...")
        create_memory_bundle_structure()
        print()

        print("="*70)
        print("✅ ALL FIXES APPLIED SUCCESSFULLY")
        print("="*70)
        print()
        print("Next steps:")
        print("1. Test the system: python3 dae_gov_cli.py")
        print("2. Verify dynamic glyphs change with R-matrix updates")
        print("3. Check Bundle/ directory for user compartments")
        print()

    except Exception as e:
        print(f"❌ Error applying fixes: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
