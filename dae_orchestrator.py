#!/usr/bin/env python3
"""
DAE_HYPHAE_1 Orchestrator
==========================

Unified entry point for all DAE_HYPHAE_1 operations:
- Interactive prompting
- Training (baseline, epochs 1-5)
- Validation (system maturity, health checks)
- Quick tests

Usage:
    # Interactive mode
    python3 dae_orchestrator.py interactive

    # Training
    python3 dae_orchestrator.py train --mode baseline
    python3 dae_orchestrator.py train --mode epoch --epoch 1

    # Validation
    python3 dae_orchestrator.py validate --quick
    python3 dae_orchestrator.py validate --full

Date: November 12, 2025
"""

import sys
import subprocess
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config


def run_interactive(args):
    """Run interactive prompting mode."""
    cmd = [sys.executable, 'dae_interactive.py']

    if args.mode:
        cmd.extend(['--mode', args.mode])

    subprocess.run(cmd)


def run_training(args):
    """Run training mode."""
    if args.mode == 'baseline':
        print("🎯 Running baseline training...")
        cmd = [sys.executable, 'training/conversational/run_baseline_training.py']
        subprocess.run(cmd)

    elif args.mode == 'epoch':
        if not args.epoch:
            print("❌ Error: --epoch required for epoch training")
            sys.exit(1)

        print(f"🎯 Running epoch {args.epoch} training...")
        # TODO: Implement epoch-specific training
        print(f"⚠️  Epoch {args.epoch} training not yet implemented")

    elif args.mode == 'expanded':
        print("🎯 Running expanded training...")
        cmd = [sys.executable, 'training/conversational/run_expanded_training.py']
        subprocess.run(cmd)

    else:
        print(f"❌ Unknown training mode: {args.mode}")
        sys.exit(1)


def run_validation(args):
    """Run validation mode."""
    if args.quick:
        print("⚡ Running quick validation...")
        # Quick system health check (< 30 seconds)
        cmd = [
            sys.executable,
            '-c',
            """
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from config import Config
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\\n🔍 QUICK SYSTEM VALIDATION")
print("="*80)

# Initialize organism
print("📋 Initializing organism...")
organism = ConversationalOrganismWrapper()
print("✅ Organism initialized")

# Test with quick inputs
test_inputs = Config.QUICK_VALIDATE_TEST_INPUTS
passed = 0

for i, text in enumerate(test_inputs, 1):
    print(f"\\nTest {i}/{len(test_inputs)}: \\\"{text[:40]}...\\\"")
    try:
        result = organism.process_text(
            text,
            context={'test_id': f'quick_validate_{i}'},
            enable_tsk_recording=False,
            enable_phase2=True
        )
        felt_states = result['felt_states']
        emission = felt_states.get('emission_text')
        confidence = felt_states.get('emission_confidence', 0.0)

        if emission and confidence >= 0.3:
            print(f"✅ PASS (confidence={confidence:.3f})")
            passed += 1
        else:
            print(f"❌ FAIL (confidence={confidence:.3f}, no emission)")
    except Exception as e:
        print(f"❌ FAIL ({e})")

print(f"\\n{'='*80}")
print(f"✅ Passed: {passed}/{len(test_inputs)}")
if passed == len(test_inputs):
    print("🟢 SYSTEM HEALTHY")
else:
    print("🟡 SYSTEM DEGRADED")
print("="*80)
"""
        ]
        subprocess.run(cmd)

    elif args.full:
        print("🔬 Running full system maturity assessment...")
        cmd = [sys.executable, 'tests/validation/system/test_system_maturity_assessment.py']
        subprocess.run(cmd)

    else:
        print("❌ Error: Specify --quick or --full for validation")
        sys.exit(1)


def main():
    """Main orchestrator entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='DAE_HYPHAE_1 Orchestrator - Unified entry point',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python3 dae_orchestrator.py interactive
  python3 dae_orchestrator.py interactive --mode detailed

  # Training
  python3 dae_orchestrator.py train --mode baseline
  python3 dae_orchestrator.py train --mode epoch --epoch 1
  python3 dae_orchestrator.py train --mode expanded

  # Validation
  python3 dae_orchestrator.py validate --quick
  python3 dae_orchestrator.py validate --full
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Run interactive prompting mode')
    interactive_parser.add_argument(
        '--mode',
        choices=['simple', 'standard', 'detailed', 'debug'],
        default='standard',
        help='Display mode (default: standard)'
    )

    # Train command
    train_parser = subparsers.add_parser('train', help='Run training')
    train_parser.add_argument(
        '--mode',
        choices=['baseline', 'epoch', 'expanded'],
        required=True,
        help='Training mode'
    )
    train_parser.add_argument(
        '--epoch',
        type=int,
        choices=[1, 2, 3, 4, 5],
        help='Epoch number (required for epoch mode)'
    )

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Run validation')
    validate_group = validate_parser.add_mutually_exclusive_group(required=True)
    validate_group.add_argument('--quick', action='store_true', help='Quick validation (< 30s)')
    validate_group.add_argument('--full', action='store_true', help='Full system maturity assessment')

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to appropriate handler
    try:
        if args.command == 'interactive':
            run_interactive(args)
        elif args.command == 'train':
            run_training(args)
        elif args.command == 'validate':
            run_validation(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
