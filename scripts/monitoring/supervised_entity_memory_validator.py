#!/usr/bin/env python3
"""
🌀 Supervised Entity Memory Validator (Nov 14, 2025)

Runs multi-turn entity memory scenarios to diagnose exactly where
the entity memory system is failing in practice.

This validates the COMPLETE pipeline:
1. Entity extraction (Phase 1.8)
2. Entity storage in profile
3. Entity loading on every turn (Phase 1.8++)
4. Entity context reaching LLM
5. LLM using entity knowledge in responses

Outputs detailed diagnostics for each failure point.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Set PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from persona_layer.memory_intent_detector import MemoryIntentDetector
from persona_layer.entity_extractor import EntityExtractor
from persona_layer.superject_structures import EnhancedUserProfile
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

class EntityMemoryValidator:
    """Validates entity memory persistence across multi-turn conversations."""

    def __init__(self):
        self.detector = MemoryIntentDetector()
        self.extractor = EntityExtractor()
        self.organism = ConversationalOrganismWrapper()
        self.results = []

    def print_section(self, title: str, char: str = '='):
        """Print formatted section header."""
        print(f"\n{char*70}")
        print(f"  {title}")
        print(f"{char*70}\n")

    def validate_scenario(self, scenario: Dict) -> Dict[str, Any]:
        """
        Run a multi-turn scenario and validate entity memory.

        Returns detailed diagnostics for each turn.
        """
        self.print_section(f"Scenario: {scenario['name']}")
        print(f"Description: {scenario['description']}")

        # Initialize profile for this scenario
        profile = EnhancedUserProfile(
            user_id=f"test_{scenario['scenario_id']}",
            created_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat()
        )

        scenario_results = {
            'scenario_id': scenario['scenario_id'],
            'name': scenario['name'],
            'turns': [],
            'overall_success': True,
            'failures': []
        }

        # Process each turn
        for turn_data in scenario['turns']:
            turn_result = self.validate_turn(turn_data, profile, scenario_results)
            scenario_results['turns'].append(turn_result)

            if not turn_result['success']:
                scenario_results['overall_success'] = False

        return scenario_results

    def validate_turn(
        self,
        turn_data: Dict,
        profile: EnhancedUserProfile,
        scenario_results: Dict
    ) -> Dict[str, Any]:
        """Validate a single turn in the conversation."""

        turn_num = turn_data['turn']
        user_input = turn_data['user_input']

        print(f"\n--- Turn {turn_num} ---")
        print(f"User: {user_input}")

        turn_result = {
            'turn': turn_num,
            'user_input': user_input,
            'success': True,
            'checks': {},
            'diagnostics': {}
        }

        # Create context dict (simulating dae_interactive.py)
        context = {
            'user_input': user_input,
            'timestamp': datetime.now().isoformat()
        }

        # 🔍 CHECK 1: Entity context loading on THIS turn
        turn_result['checks']['entity_context_loaded'] = False
        turn_result['diagnostics']['entity_context_string'] = None

        if profile.has_entity_memory():
            entity_context_string = profile.get_entity_context_string()
            context['entity_context_string'] = entity_context_string
            turn_result['checks']['entity_context_loaded'] = True
            turn_result['diagnostics']['entity_context_string'] = entity_context_string
            print(f"✓ Entity context loaded ({len(entity_context_string)} chars)")
        else:
            print(f"  (No entity memory yet)")

        # Detect memory intent
        memory_intent_detected, intent_type, confidence, intent_context = \
            self.detector.detect(user_input)

        if memory_intent_detected:
            context['memory_intent'] = True
            context['memory_intent_type'] = intent_type
            print(f"✓ Memory intent detected: {intent_type}")

            # Extract entities
            # Mock felt-state (in reality this comes from organism)
            mock_felt_state = {
                'polyvagal_state': 'ventral_vagal',
                'self_distance': 0.7,
                'urgency_level': 0.3,
                'nexuses': [{'name': 'Relational', 'confidence': 0.8}],
                'v0_energy': 0.4,
                'satisfaction': 0.7
            }

            entities = self.extractor.extract(
                user_input,
                intent_type,
                intent_context,
                felt_state=mock_felt_state
            )

            # Store in profile
            profile.store_entities(entities)
            turn_result['checks']['entities_extracted'] = True
            turn_result['diagnostics']['entities_stored'] = list(profile.entities.keys())
            print(f"✓ Entities stored: {list(profile.entities.keys())}")
        else:
            turn_result['checks']['entities_extracted'] = False

        # 🔍 CHECK 2: Process through organism
        print(f"\n🌀 Processing through organism...")

        try:
            result = self.organism.process_text(
                text=user_input,
                context=context,
                enable_phase2=True
            )

            turn_result['checks']['organism_processed'] = True

            # Extract emission
            emission_text = result.get('emission', {}).get('text', '(no emission)')
            emission_confidence = result.get('emission', {}).get('confidence', 0.0)

            turn_result['diagnostics']['emission'] = emission_text
            turn_result['diagnostics']['emission_confidence'] = emission_confidence

            print(f"\nDAE: {emission_text}")
            print(f"(confidence: {emission_confidence:.3f})")

            # 🔍 CHECK 3: Expected entities in response
            if 'expected_response_contains' in turn_data:
                expected_terms = turn_data['expected_response_contains']
                missing_terms = []

                for term in expected_terms:
                    if term.lower() not in emission_text.lower():
                        missing_terms.append(term)

                if missing_terms:
                    turn_result['checks']['contains_expected_entities'] = False
                    turn_result['diagnostics']['missing_terms'] = missing_terms
                    turn_result['success'] = False

                    failure_msg = f"Turn {turn_num}: Expected terms not in response: {missing_terms}"
                    scenario_results['failures'].append(failure_msg)
                    print(f"❌ FAILED: Missing expected terms: {missing_terms}")
                else:
                    turn_result['checks']['contains_expected_entities'] = True
                    print(f"✓ Contains all expected terms")

            # 🔍 CHECK 4: Should NOT contain certain terms
            if 'expected_response_not_contains' in turn_data:
                forbidden_terms = turn_data['expected_response_not_contains']
                found_forbidden = []

                for term in forbidden_terms:
                    if term.lower() in emission_text.lower():
                        found_forbidden.append(term)

                if found_forbidden:
                    turn_result['checks']['avoids_forbidden_terms'] = False
                    turn_result['diagnostics']['forbidden_terms_found'] = found_forbidden
                    turn_result['success'] = False

                    failure_msg = f"Turn {turn_num}: Response contains forbidden terms: {found_forbidden}"
                    scenario_results['failures'].append(failure_msg)
                    print(f"❌ FAILED: Contains forbidden terms: {found_forbidden}")
                else:
                    turn_result['checks']['avoids_forbidden_terms'] = True

            # 🔍 CHECK 5: Critical test annotation
            if 'critical_test' in turn_data:
                critical_test = turn_data['critical_test']
                print(f"\n🎯 Critical Test: {critical_test}")

                if not turn_result['success']:
                    print(f"   ❌ CRITICAL TEST FAILED")

        except Exception as e:
            turn_result['checks']['organism_processed'] = False
            turn_result['success'] = False
            turn_result['diagnostics']['error'] = str(e)

            failure_msg = f"Turn {turn_num}: Organism processing failed: {e}"
            scenario_results['failures'].append(failure_msg)
            print(f"❌ ERROR: {e}")

        return turn_result

    def run_validation(self, scenarios_path: str) -> Dict[str, Any]:
        """Run full validation across all scenarios."""

        self.print_section("🌀 SUPERVISED ENTITY MEMORY VALIDATION")

        # Load scenarios
        with open(scenarios_path, 'r') as f:
            data = json.load(f)

        scenarios = data['scenarios']
        print(f"Loaded {len(scenarios)} scenarios")
        print(f"Total turns: {data['metadata']['total_turns']}")

        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'total_scenarios': len(scenarios),
            'scenarios_passed': 0,
            'scenarios_failed': 0,
            'scenario_results': []
        }

        # Run each scenario
        for scenario in scenarios:
            scenario_result = self.validate_scenario(scenario)
            validation_results['scenario_results'].append(scenario_result)

            if scenario_result['overall_success']:
                validation_results['scenarios_passed'] += 1
            else:
                validation_results['scenarios_failed'] += 1

        # Print summary
        self.print_summary(validation_results)

        return validation_results

    def print_summary(self, results: Dict[str, Any]):
        """Print validation summary."""

        self.print_section("VALIDATION SUMMARY", '=')

        total = results['total_scenarios']
        passed = results['scenarios_passed']
        failed = results['scenarios_failed']

        print(f"Total Scenarios: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")

        # Detailed failures
        if failed > 0:
            self.print_section("FAILED SCENARIOS", '-')

            for scenario_result in results['scenario_results']:
                if not scenario_result['overall_success']:
                    print(f"\n❌ {scenario_result['name']}")
                    for failure in scenario_result['failures']:
                        print(f"   {failure}")

        # Diagnostic insights
        self.print_section("DIAGNOSTIC INSIGHTS", '-')

        # Check if entity_context_string is being loaded
        entity_loading_failures = 0
        entity_recall_failures = 0

        for scenario_result in results['scenario_results']:
            for turn_result in scenario_result['turns']:
                # Turn 2+ should have entity context loaded
                if turn_result['turn'] >= 2:
                    if not turn_result['checks'].get('entity_context_loaded', False):
                        entity_loading_failures += 1

                # Check if expected entities missing from response
                if not turn_result['checks'].get('contains_expected_entities', True):
                    entity_recall_failures += 1

        if entity_loading_failures > 0:
            print(f"⚠️  Entity context NOT loaded on {entity_loading_failures} Turn 2+ instances")
            print(f"   → This suggests Phase 1.8++ fix not working")
            print(f"   → Check: dae_interactive.py entity loading logic")

        if entity_recall_failures > 0:
            print(f"⚠️  Entity recall failed in {entity_recall_failures} responses")
            print(f"   → Entity context might be loaded but not reaching LLM")
            print(f"   → Check: llm_felt_guidance.py and organ_reconstruction_pipeline.py")

        if entity_loading_failures == 0 and entity_recall_failures == 0:
            print(f"✅ Entity loading and recall working as expected!")

def main():
    """Main entry point."""

    scenarios_path = "/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/entity_memory_training_pairs.json"

    validator = EntityMemoryValidator()
    results = validator.run_validation(scenarios_path)

    # Save results
    results_path = "/Users/daedalea/Desktop/DAE_HYPHAE_1/results/entity_memory_validation_results.json"
    os.makedirs(os.path.dirname(results_path), exist_ok=True)

    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📊 Results saved: {results_path}")

    # Exit code based on success
    sys.exit(0 if results['scenarios_failed'] == 0 else 1)

if __name__ == '__main__':
    main()
