#!/usr/bin/env python3
"""
System Response Monitor - Interactive Testing & Analysis
========================================================

Tool for testing and analyzing DAE_HYPHAE_1 conversational organism responses.

Features:
1. Interactive mode: Test individual inputs and see detailed diagnostics
2. Batch mode: Test multiple inputs and compare responses
3. Analysis mode: Analyze response patterns, organ activation, families
4. Comparison mode: Compare responses before/after training epochs

Usage:
    # Interactive testing
    python3 tools/system_response_monitor.py --mode interactive

    # Batch testing
    python3 tools/system_response_monitor.py --mode batch --inputs test_inputs.json

    # Analysis
    python3 tools/system_response_monitor.py --mode analyze --family Family_001

Date: November 12, 2025
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


class SystemResponseMonitor:
    """
    Interactive tool for testing and monitoring organism responses.
    """

    def __init__(self):
        """Initialize system monitor with organism wrapper."""
        print("🌀 Initializing System Response Monitor...")
        self.organism = ConversationalOrganismWrapper()

        # Check learning state
        if hasattr(self.organism, 'phase5_learning') and self.organism.phase5_learning:
            self.families = self.organism.phase5_learning.families
            print(f"   ✅ Phase 5 Learning: {len(self.families.families)} families")
        else:
            self.families = None
            print("   ⚠️  Phase 5 Learning not available")

        self.response_history = []
        print("   ✅ Monitor ready")
        print()

    def test_input(
        self,
        input_text: str,
        context: Optional[Dict] = None,
        verbose: bool = True
    ) -> Dict:
        """
        Test single input and return detailed diagnostics.

        Args:
            input_text: User input to test
            context: Optional context dict
            verbose: Print detailed diagnostics

        Returns:
            Full response dict with diagnostics
        """
        if context is None:
            context = {'test_id': f"test_{len(self.response_history):04d}"}

        if verbose:
            print(f"\n🎯 Testing Input:")
            print(f"   \"{input_text}\"")
            print()

        # Process input
        result = self.organism.process_text(
            input_text,
            context=context,
            enable_tsk_recording=False,
            enable_phase2=True
        )

        # Extract key metrics
        response_text = result.get('emission_text', '')
        confidence = result.get('emission_confidence', 0.0)
        emission_path = result.get('emission_path', 'unknown')
        felt_states = result.get('felt_states', {})

        # Detailed diagnostics
        diagnostic = {
            'timestamp': datetime.now().isoformat(),
            'input': input_text,
            'output': {
                'text': response_text,
                'confidence': confidence,
                'emission_path': emission_path
            },
            'felt_states': {
                'satisfaction': felt_states.get('satisfaction_final', 0.0),
                'convergence_cycles': felt_states.get('convergence_cycles', 0),
                'nexuses_formed': felt_states.get('nexuses_formed', 0),
                'zone_id': felt_states.get('zone_id', 0),
                'v0_energy_final': felt_states.get('v0_energy_final', 0.0),
                'kairos_detected': felt_states.get('kairos_detected', False)
            },
            'organ_activations': self._extract_organ_activations(felt_states),
            'meta_atoms_activated': self._extract_meta_atoms(felt_states),
            'family_assignment': self._get_family_assignment(context.get('test_id', 'unknown'))
        }

        if verbose:
            self._print_diagnostic(diagnostic)

        self.response_history.append(diagnostic)
        return diagnostic

    def _extract_organ_activations(self, felt_states: Dict) -> Dict:
        """Extract organ activation scores from felt states."""
        organ_results = felt_states.get('organ_results', {})
        activations = {}

        for organ_name, organ_result in organ_results.items():
            if isinstance(organ_result, dict):
                coherence = organ_result.get('coherence', 0.0)
                activations[organ_name] = float(coherence)

        return activations

    def _extract_meta_atoms(self, felt_states: Dict) -> List[str]:
        """Extract activated meta-atoms from felt states."""
        # This would extract meta-atoms from semantic fields
        # Simplified for now
        return []

    def _get_family_assignment(self, conversation_id: str) -> Optional[str]:
        """Get family assignment for conversation if available."""
        if self.families:
            return self.families.conversation_to_family.get(conversation_id)
        return None

    def _print_diagnostic(self, diagnostic: Dict):
        """Print detailed diagnostic information."""
        print("📊 Response Diagnostic:")
        print()

        # Output
        print(f"   🗣️  Output: \"{diagnostic['output']['text'][:80]}...\"")
        print(f"   📈 Confidence: {diagnostic['output']['confidence']:.3f}")
        print(f"   🎯 Emission path: {diagnostic['output']['emission_path']}")
        print()

        # Felt states
        felt = diagnostic['felt_states']
        print(f"   🌀 Felt States:")
        print(f"      Satisfaction: {felt['satisfaction']:.3f}")
        print(f"      Convergence cycles: {felt['convergence_cycles']}")
        print(f"      Nexuses formed: {felt['nexuses_formed']}")
        print(f"      SELF Zone: {felt['zone_id']}")
        print(f"      V0 energy: {felt['v0_energy_final']:.3f}")
        print(f"      Kairos detected: {felt['kairos_detected']}")
        print()

        # Organ activations
        if diagnostic['organ_activations']:
            print(f"   🧬 Top Organ Activations:")
            sorted_organs = sorted(
                diagnostic['organ_activations'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            for organ, activation in sorted_organs[:5]:
                print(f"      {organ}: {activation:.3f}")
            print()

        # Family assignment
        if diagnostic['family_assignment']:
            print(f"   👥 Family: {diagnostic['family_assignment']}")
            print()

    def interactive_mode(self):
        """Run interactive testing session."""
        print("="*80)
        print("🌀 INTERACTIVE TESTING MODE")
        print("="*80)
        print()
        print("Commands:")
        print("   <input text>  - Test an input")
        print("   /history      - Show response history")
        print("   /stats        - Show session statistics")
        print("   /families     - Show learned families")
        print("   /quit         - Exit")
        print()

        while True:
            try:
                user_input = input("\n> ").strip()

                if not user_input:
                    continue

                if user_input == '/quit':
                    print("\nExiting interactive mode.")
                    break

                elif user_input == '/history':
                    self._show_history()

                elif user_input == '/stats':
                    self._show_statistics()

                elif user_input == '/families':
                    self._show_families()

                else:
                    # Test input
                    self.test_input(user_input, verbose=True)

            except KeyboardInterrupt:
                print("\n\nExiting interactive mode.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def _show_history(self):
        """Show response history."""
        print("\n📜 Response History:")
        print()
        if not self.response_history:
            print("   No responses yet.")
            return

        for i, response in enumerate(self.response_history, 1):
            print(f"   {i}. \"{response['input'][:50]}...\"")
            print(f"      → \"{response['output']['text'][:50]}...\"")
            print(f"      Confidence: {response['output']['confidence']:.3f}, "
                  f"Satisfaction: {response['felt_states']['satisfaction']:.3f}")
        print()

    def _show_statistics(self):
        """Show session statistics."""
        print("\n📊 Session Statistics:")
        print()

        if not self.response_history:
            print("   No responses yet.")
            return

        confidences = [r['output']['confidence'] for r in self.response_history]
        satisfactions = [r['felt_states']['satisfaction'] for r in self.response_history]
        cycles = [r['felt_states']['convergence_cycles'] for r in self.response_history]
        paths = [r['output']['emission_path'] for r in self.response_history]

        print(f"   Total responses: {len(self.response_history)}")
        print(f"   Mean confidence: {sum(confidences)/len(confidences):.3f}")
        print(f"   Mean satisfaction: {sum(satisfactions)/len(satisfactions):.3f}")
        print(f"   Mean cycles: {sum(cycles)/len(cycles):.2f}")
        print()

        # Emission path distribution
        path_counts = {}
        for path in paths:
            path_counts[path] = path_counts.get(path, 0) + 1

        print("   Emission paths:")
        for path, count in sorted(path_counts.items()):
            pct = 100 * count / len(paths)
            print(f"      {path}: {count} ({pct:.1f}%)")
        print()

    def _show_families(self):
        """Show learned families."""
        print("\n👥 Learned Families:")
        print()

        if not self.families:
            print("   Phase 5 learning not available.")
            return

        if not self.families.families:
            print("   No families discovered yet.")
            return

        for family_id, family in self.families.families.items():
            print(f"   {family_id}:")
            print(f"      Members: {family.member_count}")
            print(f"      Maturity: {family.maturity_level}")
            print(f"      Mean satisfaction: {family.mean_satisfaction:.3f}")
            if family.dominant_organs:
                print(f"      Dominant organs: {', '.join(family.dominant_organs)}")
            print()

    def batch_test(self, inputs: List[str], save_path: Optional[str] = None):
        """Test batch of inputs and save results."""
        print(f"\n🔬 Batch Testing ({len(inputs)} inputs)")
        print("="*80)

        results = []
        for i, input_text in enumerate(inputs, 1):
            print(f"\n[{i}/{len(inputs)}] Testing...")
            diagnostic = self.test_input(input_text, verbose=False)
            results.append(diagnostic)

            # Print summary
            print(f"   Input: \"{input_text[:50]}...\"")
            print(f"   Output: \"{diagnostic['output']['text'][:50]}...\"")
            print(f"   Confidence: {diagnostic['output']['confidence']:.3f}")

        # Save results
        if save_path:
            with open(save_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Results saved to: {save_path}")

        # Print summary statistics
        self._print_batch_summary(results)

        return results

    def _print_batch_summary(self, results: List[Dict]):
        """Print summary statistics for batch test."""
        print(f"\n📊 Batch Test Summary:")
        print("="*80)

        confidences = [r['output']['confidence'] for r in results]
        satisfactions = [r['felt_states']['satisfaction'] for r in results]
        cycles = [r['felt_states']['convergence_cycles'] for r in results]

        print(f"   Total tests: {len(results)}")
        print(f"   Mean confidence: {sum(confidences)/len(confidences):.3f}")
        print(f"   Confidence range: {min(confidences):.3f} - {max(confidences):.3f}")
        print(f"   Mean satisfaction: {sum(satisfactions)/len(satisfactions):.3f}")
        print(f"   Mean cycles: {sum(cycles)/len(cycles):.2f}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="System Response Monitor")
    parser.add_argument(
        '--mode',
        choices=['interactive', 'batch', 'analyze'],
        default='interactive',
        help='Operating mode'
    )
    parser.add_argument(
        '--inputs',
        help='Path to JSON file with test inputs (for batch mode)'
    )
    parser.add_argument(
        '--output',
        help='Path to save results (for batch mode)'
    )

    args = parser.parse_args()

    # Initialize monitor
    monitor = SystemResponseMonitor()

    if args.mode == 'interactive':
        monitor.interactive_mode()

    elif args.mode == 'batch':
        if not args.inputs:
            print("❌ Error: --inputs required for batch mode")
            return

        with open(args.inputs) as f:
            inputs = json.load(f)

        if isinstance(inputs, dict) and 'inputs' in inputs:
            inputs = inputs['inputs']

        monitor.batch_test(inputs, save_path=args.output)

    elif args.mode == 'analyze':
        monitor._show_families()
        monitor._show_statistics()


if __name__ == "__main__":
    main()
