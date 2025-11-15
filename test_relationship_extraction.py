#!/usr/bin/env python3
"""
Relationship Extraction Test Suite - November 14, 2025
======================================================

Validates relationship extraction accuracy using training corpus.
Tests both pattern matching and integration with entity system.

Run after each epoch training round to measure improvement.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.entity_extraction.extractors.relationship_extractor import RelationshipExtractor


class RelationshipExtractionTest:
    """Test suite for relationship extraction."""

    def __init__(self, corpus_path: str = None):
        """
        Initialize test suite.

        Args:
            corpus_path: Path to training corpus JSON
        """
        if corpus_path is None:
            corpus_path = "knowledge_base/entity_training/corpora/relationship_training_corpus.json"

        with open(corpus_path, 'r') as f:
            self.corpus = json.load(f)

        self.extractor = RelationshipExtractor()
        self.test_results = []

    def run_all_tests(self):
        """Run all test pairs from corpus."""
        print("\n" + "="*70)
        print("🧪 RELATIONSHIP EXTRACTION TEST SUITE")
        print("="*70)
        print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total test pairs: {self.corpus['metadata']['total_pairs']}")
        print()

        total_tests = 0
        passed_tests = 0
        failed_tests = []

        # Test each pair
        for pair in self.corpus['training_pairs']:
            test_id = pair['id']
            input_text = pair['input']
            expected = pair['expected']
            difficulty = pair.get('difficulty', 'unknown')

            # Extract
            actual = self.extractor.extract(input_text, confidence_threshold=0.7)

            # Score
            score, details = self._score_extraction(expected, actual)

            total_tests += 1
            if score >= 0.8:  # 80% threshold for passing
                passed_tests += 1
                status = "✅"
            else:
                failed_tests.append({
                    'id': test_id,
                    'input': input_text,
                    'expected': expected,
                    'actual': actual,
                    'score': score,
                    'details': details
                })
                status = "❌"

            # Store result
            self.test_results.append({
                'id': test_id,
                'input': input_text,
                'expected': expected,
                'actual': actual,
                'score': score,
                'details': details,
                'difficulty': difficulty,
                'passed': score >= 0.8
            })

            # Print result
            print(f"{status} {test_id} (diff={difficulty}, score={score:.2f})")
            if score < 0.8:
                print(f"   Input: \"{input_text}\"")
                print(f"   Expected: {expected}")
                print(f"   Actual: {actual}")
                print(f"   Details: {details}")
                print()

        # Summary
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)

        accuracy = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        print(f"\nTotal tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {len(failed_tests)}")
        print(f"Accuracy: {accuracy:.1f}%")

        # Breakdown by difficulty
        print("\nAccuracy by difficulty:")
        for diff in ['easy', 'medium', 'hard', 'very_hard']:
            diff_tests = [t for t in self.test_results if t['difficulty'] == diff]
            if diff_tests:
                diff_passed = sum(1 for t in diff_tests if t['passed'])
                diff_accuracy = (diff_passed / len(diff_tests)) * 100
                print(f"  {diff}: {diff_accuracy:.1f}% ({diff_passed}/{len(diff_tests)})")

        # Overall result
        print("\n" + "="*70)
        threshold = self.corpus['evaluation_criteria']['passing_threshold'] * 100
        if accuracy >= threshold:
            print(f"✅ PASS - Accuracy {accuracy:.1f}% >= {threshold:.1f}% threshold")
        else:
            print(f"⚠️  NEEDS IMPROVEMENT - Accuracy {accuracy:.1f}% < {threshold:.1f}% threshold")
        print("="*70 + "\n")

        return accuracy >= threshold

    def _score_extraction(self, expected: dict, actual: dict) -> tuple:
        """
        Score extraction quality.

        Args:
            expected: Expected entities dict
            actual: Extracted entities dict

        Returns:
            (score, details_dict) - Score 0-1, details of comparison
        """
        total_score = 0
        max_score = 0
        details = {
            'exact_matches': [],
            'name_correct_relation_wrong': [],
            'name_wrong_relation_correct': [],
            'missed': [],
            'extra': []
        }

        # Check each category
        for category in ['family_members', 'friends', 'colleagues', 'other_relations']:
            expected_rels = expected.get(category, [])
            actual_rels = actual.get(category, [])

            for exp_rel in expected_rels:
                max_score += 1.0
                exp_name = exp_rel['name']
                exp_relation = exp_rel['relation']

                # Find match in actual
                found_exact = False
                found_name = False
                found_relation = False

                for act_rel in actual_rels:
                    act_name = act_rel['name']
                    act_relation = act_rel['relation']

                    if act_name == exp_name and act_relation == exp_relation:
                        # Exact match
                        total_score += 1.0
                        details['exact_matches'].append(f"{exp_name} ({exp_relation})")
                        found_exact = True
                        break
                    elif act_name == exp_name:
                        # Name correct, relation wrong
                        total_score += 0.5
                        details['name_correct_relation_wrong'].append(
                            f"{exp_name}: expected {exp_relation}, got {act_relation}"
                        )
                        found_name = True
                    elif act_relation == exp_relation:
                        # Relation correct, name wrong
                        total_score += 0.3
                        details['name_wrong_relation_correct'].append(
                            f"{exp_relation}: expected {exp_name}, got {act_name}"
                        )
                        found_relation = True

                if not found_exact and not found_name and not found_relation:
                    # Completely missed
                    details['missed'].append(f"{exp_name} ({exp_relation})")

            # Check for extra extractions (false positives)
            for act_rel in actual_rels:
                act_name = act_rel['name']
                act_relation = act_rel['relation']

                found = False
                for exp_rel in expected_rels:
                    if exp_rel['name'] == act_name and exp_rel['relation'] == act_relation:
                        found = True
                        break

                if not found:
                    details['extra'].append(f"{act_name} ({act_relation})")

        # Calculate final score
        final_score = total_score / max_score if max_score > 0 else 0

        return final_score, details

    def save_results(self, output_path: str = None):
        """Save test results to JSON."""
        if output_path is None:
            output_path = f"results/entity_training/relationship_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        output = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.test_results),
            'passed': sum(1 for t in self.test_results if t['passed']),
            'failed': sum(1 for t in self.test_results if not t['passed']),
            'accuracy': (sum(1 for t in self.test_results if t['passed']) / len(self.test_results)) * 100,
            'results': self.test_results
        }

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"📁 Results saved to: {output_path}")


def main():
    """Main test runner."""
    try:
        tester = RelationshipExtractionTest()
        passed = tester.run_all_tests()
        tester.save_results()
        sys.exit(0 if passed else 1)
    except Exception as e:
        print(f"\n❌ TEST SUITE CRASHED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
