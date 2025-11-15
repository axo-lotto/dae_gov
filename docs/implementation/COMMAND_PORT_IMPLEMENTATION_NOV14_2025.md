# Command Port Implementation - CLI to Interactive
**Date:** November 14, 2025
**Status:** In Progress
**Goal:** Port 7-9 commands from `dae_gov_cli.py` to `dae_interactive.py`

---

## Summary

This document provides the complete implementation for porting commands from CLI mode to interactive mode, increasing functionality from 5 commands to 15+ commands.

---

## Commands to Port

### **Tier 1: Essential (Highest Priority)**
1. `/identity` - Show mycelial identity
2. `/stats` - Learning statistics
3. `/projects` - Active projects summary

### **Tier 2: Memory & Discovery**
4. `/remember` - Retrieve similar past moments (hybrid mode)
5. `/traces` - Show mycelium traces
6. `/insights` - Filter traces by insights
7. `/notes` - Filter traces by notes

### **Tier 3: New Commands (User Data)**
8. `/patterns` - Show transformation patterns (NEW)
9. `/trajectory` - Show felt-state trajectory (NEW)

---

## Implementation Status

**Session Limitation:** Due to context limits, I've documented the complete implementation strategy. The actual code changes should be implemented in the next session when we have fresh context.

---

## Required Components Check

Before implementing, verify these components are accessible in interactive mode:

```python
# dae_interactive.py needs access to:
1. organism.hebbian_memory (for /stats)
2. organism.conversational_r_matrix (for /stats)
3. identity_tracker (MycelialIdentityTracker) (for /identity, /projects)
4. user_superject_learner (for /patterns, /trajectory)
5. memory_retrieval (for /remember) - Already exists if HYBRID_ENABLED
```

---

## Implementation Plan

### **Step 1: Add Required Imports** (dae_interactive.py)

```python
# Add near top of file (around line 35):
from monitoring.mycelial_identity_tracker import MycelialIdentityTracker
from persona_layer.user_superject_learner import UserSuperjectLearner
```

### **Step 2: Initialize Components in __init__** (dae_interactive.py)

```python
# In InteractiveSession.__init__, after organism initialization (around line 184):

# Initialize identity tracker (for /identity, /projects)
try:
    self.identity_tracker = MycelialIdentityTracker()
    print("   Loading mycelial identity tracker...")
except Exception as e:
    print(f"   ⚠️  Identity tracker initialization failed: {e}")
    self.identity_tracker = None

# Initialize user superject learner (for /patterns, /trajectory)
try:
    self.user_superject_learner = UserSuperjectLearner()
    print("   Loading user superject learner...")
except Exception as e:
    print(f"   ⚠️  User superject learner initialization failed: {e}")
    self.user_superject_learner = None
```

### **Step 3: Add Command Handler Methods**

Add these methods to `InteractiveSession` class (around line 570, after `save_conversation`):

```python
    def cmd_identity(self):
        """Show mycelial identity (subjective aim + projects)."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return

        print("\n")
        print(self.identity_tracker.get_identity_summary())

    def cmd_stats(self):
        """Show learning statistics."""
        print("\n" + "="*70)
        print("Learning Statistics")
        print("="*70)

        # Check if organism has required attributes
        if not hasattr(self.organism, 'conversational_r_matrix'):
            print("\n⚠️  R-Matrix not available in organism\n")
            return

        # Conversational R-Matrix stats
        r_matrix = self.organism.conversational_r_matrix
        print(f"\n🌀 Conversational Organs R-Matrix:")
        print(f"   Updates: {r_matrix.update_count}")
        print(f"   Organs: {', '.join(r_matrix.organs)}")
        print(f"\n   Strongest Couplings:")
        for organ1, organ2, strength in r_matrix.get_strongest_couplings(top_k=5):
            print(f"      {organ1} + {organ2} = {strength:.3f}")

        # Hebbian memory stats
        if hasattr(self.organism, 'hebbian_memory'):
            hebbian = self.organism.hebbian_memory
            print(f"\n📊 Hebbian Learning:")
            print(f"   Total updates: {hebbian.update_count}")
            print(f"   Successes: {hebbian.success_count}")
            print(f"   Failures: {hebbian.failure_count}")
            print(f"   Success rate: {hebbian.success_rate*100:.1f}%")
            print(f"   Global confidence: {hebbian.get_global_confidence():.3f}")

        print("="*70 + "\n")

    def cmd_projects(self):
        """Show active projects summary."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return

        print("\n")
        print(self.identity_tracker.get_project_summary())

    def cmd_patterns(self):
        """Show transformation patterns for this user (NEW)."""
        if not self.user_superject_learner:
            print("\n❌ User superject learner not available\n")
            return

        # Load user profile
        profile = self.user_superject_learner.load_user_profile(self.user['user_id'])

        if not profile:
            print("\n❌ No profile found for user\n")
            return

        print("\n" + "="*70)
        print(f"Transformation Patterns for {self.user['username']}")
        print("="*70)

        # Get transformation patterns from metadata
        patterns = profile.metadata.get('transformation_patterns', [])

        if not patterns:
            print("\n   No transformation patterns recorded yet.")
            print("   Patterns emerge after 10+ conversations.\n")
            return

        print(f"\n   Total patterns: {len(patterns)}\n")

        for i, pattern in enumerate(patterns[:10], 1):  # Show top 10
            pattern_type = pattern.get('pattern_type', 'unknown')
            frequency = pattern.get('frequency', 0)
            context = pattern.get('context', 'N/A')
            print(f"   {i}. {pattern_type}")
            print(f"      Frequency: {frequency}")
            print(f"      Context: {context}\n")

        print("="*70 + "\n")

    def cmd_trajectory(self):
        """Show felt-state trajectory for this user (NEW)."""
        if not self.user_superject_learner:
            print("\n❌ User superject learner not available\n")
            return

        # Load user superject
        superject = self.user_superject_learner.load_user_superject(self.user['user_id'])

        if not superject:
            print("\n❌ No superject found for user\n")
            return

        print("\n" + "="*70)
        print(f"Felt-State Trajectory for {self.user['username']}")
        print("="*70)

        trajectory = superject.get('felt_trajectory', [])

        if not trajectory:
            print("\n   No trajectory data recorded yet.\n")
            return

        print(f"\n   Total snapshots: {len(trajectory)}")
        print(f"   Recent trajectory (last 10):\n")

        # Show last 10 snapshots
        for snapshot in trajectory[-10:]:
            timestamp = snapshot.get('timestamp', 'unknown')
            zone = snapshot.get('zone', 0)
            polyvagal = snapshot.get('polyvagal_state', 'unknown')
            satisfaction = snapshot.get('satisfaction', 0.0)
            dominant_organs = snapshot.get('dominant_organs', [])

            print(f"   📍 {timestamp}")
            print(f"      Zone: {zone}, Polyvagal: {polyvagal}")
            print(f"      Satisfaction: {satisfaction:.2f}")
            print(f"      Organs: {', '.join(dominant_organs[:3])}\n")

        print("="*70 + "\n")

    def cmd_remember(self):
        """Retrieve similar past moments (hybrid mode)."""
        if not Config.HYBRID_ENABLED or not self.memory_retrieval:
            print("\n❌ Hybrid mode not enabled. Set HYBRID_ENABLED = True in config.py\n")
            return

        print("\n" + "="*70)
        print("Memory Retrieval (Hybrid Superject)")
        print("="*70)

        # This would need current organ signature from last conversation turn
        # For now, show instruction
        print("\n   💡 To retrieve similar moments:")
        print("   1. Have a conversation first")
        print("   2. Use /remember after a response")
        print("   3. DAE will find similar past moments\n")

        print("   Feature: Retrieves similar felt-states from your history")
        print("   Uses: 57D organ signatures for similarity matching\n")

        print("="*70 + "\n")

    def cmd_traces(self):
        """Show mycelium traces (notes, insights, projects)."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return

        print("\n" + "="*70)
        print("Mycelium Traces")
        print("="*70)

        traces = self.identity_tracker.get_all_traces()

        if not traces:
            print("\n   No traces recorded yet.\n")
            return

        print(f"\n   Total traces: {len(traces)}\n")

        for trace in traces[-20:]:  # Show last 20
            trace_type = trace.get('type', 'unknown')
            content = trace.get('content', '')
            timestamp = trace.get('timestamp', 'unknown')

            icon = "📝" if trace_type == "note" else "💡" if trace_type == "insight" else "📂"

            print(f"   {icon} [{trace_type}] {timestamp}")
            print(f"      {content[:100]}...\n" if len(content) > 100 else f"      {content}\n")

        print("="*70 + "\n")

    def cmd_insights(self):
        """Show insights only (filtered traces)."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return

        print("\n" + "="*70)
        print("Insights")
        print("="*70)

        traces = self.identity_tracker.get_traces_by_type('insight')

        if not traces:
            print("\n   No insights recorded yet.\n")
            return

        print(f"\n   Total insights: {len(traces)}\n")

        for trace in traces[-15:]:  # Show last 15
            content = trace.get('content', '')
            timestamp = trace.get('timestamp', 'unknown')

            print(f"   💡 {timestamp}")
            print(f"      {content}\n")

        print("="*70 + "\n")

    def cmd_notes(self):
        """Show notes only (filtered traces)."""
        if not self.identity_tracker:
            print("\n❌ Identity tracker not available\n")
            return

        print("\n" + "="*70)
        print("Notes")
        print("="*70)

        traces = self.identity_tracker.get_traces_by_type('note')

        if not traces:
            print("\n   No notes recorded yet.\n")
            return

        print(f"\n   Total notes: {len(traces)}\n")

        for trace in traces[-15:]:  # Show last 15
            content = trace.get('content', '')
            timestamp = trace.get('timestamp', 'unknown')

            print(f"   📝 {timestamp}")
            print(f"      {content}\n")

        print("="*70 + "\n")
```

### **Step 4: Add Command Routing in run() Method**

In the `run()` method, add command handlers after the existing `/help`, `/mode`, etc. (around line 530):

```python
                    elif user_input == '/identity':
                        self.cmd_identity()
                        continue
                    elif user_input == '/stats':
                        self.cmd_stats()
                        continue
                    elif user_input == '/projects':
                        self.cmd_projects()
                        continue
                    elif user_input == '/patterns':
                        self.cmd_patterns()
                        continue
                    elif user_input == '/trajectory':
                        self.cmd_trajectory()
                        continue
                    elif user_input == '/remember':
                        self.cmd_remember()
                        continue
                    elif user_input == '/traces':
                        self.cmd_traces()
                        continue
                    elif user_input == '/insights':
                        self.cmd_insights()
                        continue
                    elif user_input == '/notes':
                        self.cmd_notes()
                        continue
```

### **Step 5: Update Help Command**

Update `show_help()` method to include new commands (around line 580):

```python
    def show_help(self):
        """Show help message."""
        print("\n" + "="*80)
        print("📖 HELP")
        print("="*80)
        print("\nCommands:")
        print("  /help     - Show this help message")
        print("  /mode     - Change display mode (simple/standard/detailed/debug)")
        print("  /history  - Show conversation history")
        print("  /save     - Save conversation to JSON file")
        print("  /exit     - Exit interactive mode")
        print("\n🌀 Organism Commands:")
        print("  /identity - Show mycelial identity (subjective aim + projects)")
        print("  /stats    - Learning statistics (R-matrix, hebbian, families)")
        print("  /projects - Active projects summary")
        print("\n💭 Memory Commands:")
        print("  /remember - Retrieve similar past moments (hybrid mode)")
        print("  /traces   - Show mycelium traces (notes, insights, projects)")
        print("  /insights - Show insights only")
        print("  /notes    - Show notes only")
        print("\n👤 User Commands:")
        print("  /patterns   - Show transformation patterns (your learning)")
        print("  /trajectory - Show felt-state trajectory (your journey)")
        print("\nDisplay Modes:")
        print("  simple   - Just emission text")
        print("  standard - Emission + confidence + nexuses (default)")
        print("  detailed - + organ details + transduction trajectory")
        print("  debug    - + V0 convergence details")
        print("="*80 + "\n")
```

---

## Testing Checklist

After implementation, test each command:

```bash
# Start interactive mode
python3 dae_interactive.py

# Test each command:
You: /help
You: /identity
You: /stats
You: /projects
You: /patterns
You: /trajectory
You: /remember
You: /traces
You: /insights
You: /notes

# Verify:
# ✓ No errors
# ✓ Output displays correctly
# ✓ All commands listed in /help
```

---

## Expected Behavior

### **/identity**
```
🌀 MYCELIAL IDENTITY
==================
Subjective Aim: [current dominant lure]
Satisfaction: 0.XX
Total Occasions: XXX
Projects: [list of active projects]
```

### **/stats**
```
Learning Statistics
==================
🌀 Conversational Organs R-Matrix:
   Updates: XXX
   Organs: LISTENING, EMPATHY, WISDOM...

   Strongest Couplings:
      LISTENING + EMPATHY = 0.XXX
      ...
```

### **/patterns**
```
Transformation Patterns for Alice
==================
   Total patterns: X

   1. pattern_type
      Frequency: X
      Context: ...
```

---

## Dependencies & Requirements

**Required for /identity, /projects:**
- `monitoring.mycelial_identity_tracker.MycelialIdentityTracker`
- `monitoring/mycelial_identity.json` (file)

**Required for /stats:**
- `organism.conversational_r_matrix` (ConversationalOrganRMatrix)
- `organism.hebbian_memory` (ConversationalHebbianMemory)

**Required for /patterns, /trajectory:**
- `persona_layer.user_superject_learner.UserSuperjectLearner`
- `persona_layer/users/user_{id}_superject.json` (files)

**Required for /remember:**
- `Config.HYBRID_ENABLED = True`
- `persona_layer.memory_retrieval.MemoryRetrieval`

**Required for /traces, /insights, /notes:**
- `monitoring.mycelial_identity_tracker.MycelialIdentityTracker`
- `Bundle/user_link_{id}/traces/` (directory)

---

## Next Steps

1. **Implement changes** in next session (fresh context)
2. **Test each command** individually
3. **Verify no breaking changes** (existing commands still work)
4. **Update CLAUDE.md** with new command count (5 → 15)
5. **Document any issues** encountered

---

## Success Metrics

- ✅ All 9 new commands implemented
- ✅ No errors on command execution
- ✅ Help text updated
- ✅ Backwards compatible (existing 5 commands still work)
- ✅ Interactive mode matches CLI parity (12+ commands)

---

**Implementation Document Complete**
**Ready for execution in next session with fresh context**
