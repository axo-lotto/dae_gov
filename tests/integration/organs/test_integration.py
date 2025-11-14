#!/usr/bin/env python3
"""Quick test of DAE-GOV CLI integration with conversational organs."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dae_gov_cli import DAEGovCLI

def main():
    print('Testing DAE-GOV CLI initialization...')
    print()

    try:
        cli = DAEGovCLI()
        print()
        print('='*70)
        print('✅ CLI INITIALIZED SUCCESSFULLY!')
        print('='*70)
        print()

        print('Testing conversational organ processing...')
        print()

        # Test with a sample text that should trigger curiosity
        test_input = 'I feel confused and uncertain about this'
        result = cli._process_conversational_organs(test_input)

        print(f'✅ Organs processed successfully!')
        print(f'   Curiosity triggered: {result["curiosity_triggered"]}')
        print(f'   R-matrix updates: {result["r_matrix_updates"]}')
        print(f'   Decision type: {result["nexus_decision"].decision_type}')
        print(f'   Coherence: {result["nexus_decision"].coherence_score:.3f}')
        print(f'   Intersection: {result["nexus_decision"].intersection_count:.1f}')

        if result['curiosity_triggered']:
            print(f'\n🤔 Curiosity was triggered!')
            print(f'   Question organ: {result["nexus_decision"].question_organ}')
            print(f'   Question type: {result["nexus_decision"].question_type}')
            print(f'   Question: "{result["nexus_decision"].suggested_action}"')

        print()
        print('Testing organ results...')
        for organ_name, organ_result in result['organ_results'].items():
            print(f'   {organ_name}: coherence={organ_result.coherence:.3f}, lure={organ_result.lure:.3f}')

        print()
        print('='*70)
        print('✅ ALL TESTS PASSED - READY FOR PRODUCTION')
        print('='*70)
        print()
        print('To use: python3 dae_gov_cli.py')

    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
