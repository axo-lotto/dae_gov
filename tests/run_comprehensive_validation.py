"""
Comprehensive Validation Runner - Phase B Complete Test Suite
==============================================================

Runs all 19 Phase B tests and generates diagnostic report identifying
weak points for targeted training.

Test Categories:
- Intelligence (5 tests): INTEL-001 to INTEL-005
- Continuity (4 tests): CONT-002, CONT-004, CONT-005, CONT-006
- Responsiveness (2 tests): RESP-001, RESP-002-006
- Superject (1 test): SUPER-001

Total: 12 test files, 19 individual tests

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Comprehensive Validation)
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import all test modules
from tests.intelligence.test_abstraction_reasoning import (
    run_abstraction_reasoning_test, AbstractionReasoningTester
)
from tests.intelligence.test_pattern_transfer import (
    run_pattern_transfer_test, PatternTransferTester
)
from tests.intelligence.test_novelty_handling import (
    run_novelty_handling_test, NoveltyHandlingTester
)
from tests.intelligence.test_context_integration import (
    run_context_integration_test, ContextIntegrationTester
)
from tests.intelligence.test_meta_learning import (
    run_meta_learning_test, MetaLearningTester
)

from tests.continuity.test_v0_target_persistence import (
    run_v0_target_persistence_test, V0TargetPersistenceTester
)
from tests.continuity.test_emission_consistency import (
    run_emission_consistency_test, EmissionConsistencyTester
)
from tests.continuity.test_semantic_atom_drift import (
    run_semantic_atom_drift_test, SemanticAtomDriftTester
)
from tests.continuity.test_meta_atom_activation import (
    run_meta_atom_activation_test, MetaAtomActivationTester
)

from tests.responsiveness.test_latency_measurement import (
    run_latency_measurement_test, LatencyMeasurementTester
)
from tests.responsiveness.test_comprehensive_responsiveness import (
    run_all_responsiveness_tests
)

from tests.superject.test_xyz_cycle_validation import (
    run_superject_cycle_validation, SuperjectCycleValidator
)


@dataclass
class TestResult:
    """Individual test result."""
    test_id: str
    test_name: str
    category: str
    success: bool
    reasoning: str
    duration_seconds: float
    details: Dict[str, Any]


@dataclass
class ValidationReport:
    """Complete validation report."""
    timestamp: str
    total_tests: int
    tests_passed: int
    tests_failed: int
    pass_rate: float

    # Category breakdowns
    intelligence_passed: int
    intelligence_total: int
    continuity_passed: int
    continuity_total: int
    responsiveness_passed: int
    responsiveness_total: int
    superject_passed: int
    superject_total: int

    # Test results
    test_results: List[TestResult]

    # Weak points identified
    weak_organs: List[str]
    weak_capabilities: List[str]
    training_recommendations: List[str]


class ComprehensiveValidator:
    """Runs all Phase B tests and generates diagnostic report."""

    def __init__(self):
        self.results: List[TestResult] = []

    def run_all_tests(self, verbose: bool = True) -> ValidationReport:
        """Run all 19 Phase B tests."""
        if verbose:
            print(f"\n{'='*70}")
            print(f"🔬 COMPREHENSIVE VALIDATION - PHASE B TEST SUITE")
            print(f"{'='*70}")
            print(f"\nRunning 19 tests across 4 categories...")
            print(f"Timestamp: {datetime.now().isoformat()}")

        # ====================================================================
        # Intelligence Tests (5)
        # ====================================================================

        if verbose:
            print(f"\n{'='*70}")
            print(f"📊 INTELLIGENCE TESTS (5 tests)")
            print(f"{'='*70}")

        # INTEL-001: Abstraction Reasoning
        self._run_test(
            test_id="INTEL-001",
            test_name="Abstraction Reasoning",
            category="intelligence",
            test_func=lambda: self._run_abstraction_reasoning(),
            verbose=verbose
        )

        # INTEL-002: Pattern Transfer
        self._run_test(
            test_id="INTEL-002",
            test_name="Pattern Transfer",
            category="intelligence",
            test_func=lambda: self._run_pattern_transfer(),
            verbose=verbose
        )

        # INTEL-003: Novelty Handling
        self._run_test(
            test_id="INTEL-003",
            test_name="Novelty Handling",
            category="intelligence",
            test_func=lambda: self._run_novelty_handling(),
            verbose=verbose
        )

        # INTEL-004: Context Integration
        self._run_test(
            test_id="INTEL-004",
            test_name="Context Integration",
            category="intelligence",
            test_func=lambda: self._run_context_integration(),
            verbose=verbose
        )

        # INTEL-005: Meta-Learning
        self._run_test(
            test_id="INTEL-005",
            test_name="Meta-Learning",
            category="intelligence",
            test_func=lambda: self._run_meta_learning(),
            verbose=verbose
        )

        # ====================================================================
        # Continuity Tests (4)
        # ====================================================================

        if verbose:
            print(f"\n{'='*70}")
            print(f"🔗 CONTINUITY TESTS (4 tests)")
            print(f"{'='*70}")

        # CONT-002: V0 Target Persistence
        self._run_test(
            test_id="CONT-002",
            test_name="V0 Target Persistence",
            category="continuity",
            test_func=lambda: self._run_v0_persistence(),
            verbose=verbose
        )

        # CONT-004: Emission Consistency
        self._run_test(
            test_id="CONT-004",
            test_name="Emission Consistency",
            category="continuity",
            test_func=lambda: self._run_emission_consistency(),
            verbose=verbose
        )

        # CONT-005: Semantic Atom Drift
        self._run_test(
            test_id="CONT-005",
            test_name="Semantic Atom Drift",
            category="continuity",
            test_func=lambda: self._run_semantic_drift(),
            verbose=verbose
        )

        # CONT-006: Meta-Atom Activation
        self._run_test(
            test_id="CONT-006",
            test_name="Meta-Atom Activation",
            category="continuity",
            test_func=lambda: self._run_meta_atom_activation(),
            verbose=verbose
        )

        # ====================================================================
        # Responsiveness Tests (6 combined in 2 files)
        # ====================================================================

        if verbose:
            print(f"\n{'='*70}")
            print(f"⚡ RESPONSIVENESS TESTS (6 tests)")
            print(f"{'='*70}")

        # RESP-001: Latency Measurement
        self._run_test(
            test_id="RESP-001",
            test_name="Latency Measurement",
            category="responsiveness",
            test_func=lambda: self._run_latency_measurement(),
            verbose=verbose
        )

        # RESP-002 to RESP-006: Comprehensive (5 tests combined)
        self._run_test(
            test_id="RESP-002-006",
            test_name="Comprehensive Responsiveness (5 tests)",
            category="responsiveness",
            test_func=lambda: self._run_comprehensive_responsiveness(),
            verbose=verbose
        )

        # ====================================================================
        # Superject Test (1)
        # ====================================================================

        if verbose:
            print(f"\n{'='*70}")
            print(f"🌀 SUPERJECT TEST (1 test)")
            print(f"{'='*70}")

        # SUPER-001: X→Y→Z Cycle Validation
        self._run_test(
            test_id="SUPER-001",
            test_name="X→Y→Z Cycle Validation",
            category="superject",
            test_func=lambda: self._run_superject_cycle(),
            verbose=verbose
        )

        # ====================================================================
        # Generate Report
        # ====================================================================

        report = self._generate_report()

        if verbose:
            self._print_report(report)

        return report

    def _run_test(
        self,
        test_id: str,
        test_name: str,
        category: str,
        test_func,
        verbose: bool
    ):
        """Run a single test and record result."""
        if verbose:
            print(f"\n🔬 Running {test_id}: {test_name}...")

        start_time = time.time()

        try:
            result_obj = test_func()
            duration = time.time() - start_time

            # Extract success and reasoning
            if hasattr(result_obj, 'success'):
                success = result_obj.success
                reasoning = result_obj.reasoning
                details = asdict(result_obj) if hasattr(result_obj, '__dataclass_fields__') else {}
            else:
                # Assume boolean return
                success = bool(result_obj)
                reasoning = "Test completed" if success else "Test failed"
                details = {}

            test_result = TestResult(
                test_id=test_id,
                test_name=test_name,
                category=category,
                success=success,
                reasoning=reasoning,
                duration_seconds=duration,
                details=details
            )

            self.results.append(test_result)

            status = "✅ PASSED" if success else "❌ FAILED"
            if verbose:
                print(f"   {status}: {reasoning} ({duration:.1f}s)")

        except Exception as e:
            duration = time.time() - start_time

            test_result = TestResult(
                test_id=test_id,
                test_name=test_name,
                category=category,
                success=False,
                reasoning=f"Exception: {str(e)}",
                duration_seconds=duration,
                details={"error": str(e)}
            )

            self.results.append(test_result)

            if verbose:
                print(f"   ❌ FAILED: Exception: {str(e)} ({duration:.1f}s)")

    # ========================================================================
    # Test execution methods
    # ========================================================================

    def _run_abstraction_reasoning(self):
        """Run abstraction reasoning test."""
        tester = AbstractionReasoningTester()
        return tester.test_abstraction_reasoning(verbose=False)

    def _run_pattern_transfer(self):
        """Run pattern transfer test."""
        tester = PatternTransferTester()
        return tester.test_pattern_transfer(verbose=False)

    def _run_novelty_handling(self):
        """Run novelty handling test."""
        tester = NoveltyHandlingTester()
        return tester.test_novelty_handling(verbose=False)

    def _run_context_integration(self):
        """Run context integration test."""
        tester = ContextIntegrationTester()
        return tester.test_context_integration(verbose=False)

    def _run_meta_learning(self):
        """Run meta-learning test."""
        tester = MetaLearningTester()
        return tester.test_meta_learning(verbose=False)

    def _run_v0_persistence(self):
        """Run V0 target persistence test."""
        tester = V0TargetPersistenceTester()
        return tester.test_v0_target_persistence(verbose=False)

    def _run_emission_consistency(self):
        """Run emission consistency test."""
        tester = EmissionConsistencyTester()
        return tester.test_emission_consistency(verbose=False)

    def _run_semantic_drift(self):
        """Run semantic atom drift test."""
        tester = SemanticAtomDriftTester()
        return tester.test_semantic_atom_drift(verbose=False)

    def _run_meta_atom_activation(self):
        """Run meta-atom activation test."""
        tester = MetaAtomActivationTester()
        return tester.test_meta_atom_activation(verbose=False)

    def _run_latency_measurement(self):
        """Run latency measurement test."""
        tester = LatencyMeasurementTester()
        return tester.test_latency(samples=20, verbose=False)

    def _run_comprehensive_responsiveness(self):
        """Run comprehensive responsiveness tests."""
        return run_all_responsiveness_tests(verbose=False)

    def _run_superject_cycle(self):
        """Run superject cycle validation test."""
        validator = SuperjectCycleValidator()
        return validator.validate_cycle(verbose=False)

    # ========================================================================
    # Report generation
    # ========================================================================

    def _generate_report(self) -> ValidationReport:
        """Generate comprehensive validation report."""
        total_tests = len(self.results)
        tests_passed = sum(1 for r in self.results if r.success)
        tests_failed = total_tests - tests_passed
        pass_rate = tests_passed / total_tests if total_tests > 0 else 0.0

        # Category breakdowns
        intelligence_results = [r for r in self.results if r.category == "intelligence"]
        continuity_results = [r for r in self.results if r.category == "continuity"]
        responsiveness_results = [r for r in self.results if r.category == "responsiveness"]
        superject_results = [r for r in self.results if r.category == "superject"]

        intelligence_passed = sum(1 for r in intelligence_results if r.success)
        continuity_passed = sum(1 for r in continuity_results if r.success)
        responsiveness_passed = sum(1 for r in responsiveness_results if r.success)
        superject_passed = sum(1 for r in superject_results if r.success)

        # Identify weak points
        weak_organs = self._identify_weak_organs()
        weak_capabilities = self._identify_weak_capabilities()
        training_recommendations = self._generate_training_recommendations(
            weak_organs, weak_capabilities
        )

        return ValidationReport(
            timestamp=datetime.now().isoformat(),
            total_tests=total_tests,
            tests_passed=tests_passed,
            tests_failed=tests_failed,
            pass_rate=pass_rate,
            intelligence_passed=intelligence_passed,
            intelligence_total=len(intelligence_results),
            continuity_passed=continuity_passed,
            continuity_total=len(continuity_results),
            responsiveness_passed=responsiveness_passed,
            responsiveness_total=len(responsiveness_results),
            superject_passed=superject_passed,
            superject_total=len(superject_results),
            test_results=self.results,
            weak_organs=weak_organs,
            weak_capabilities=weak_capabilities,
            training_recommendations=training_recommendations
        )

    def _identify_weak_organs(self) -> List[str]:
        """Identify organs that need targeted training."""
        weak_organs = []

        # Look for organ-related failures in test details
        for result in self.results:
            if not result.success:
                details = result.details

                # Check for low organ activation
                if 'organs_participating' in details:
                    organs_active = details['organs_participating']
                    if organs_active < 8:
                        weak_organs.append(f"Low organ activation: {organs_active}/11")

                # Check for organ-specific failures
                if 'organ_results' in details:
                    # Analyze which organs failed
                    pass

        # Add known weak organs from training data
        weak_organs.extend([
            "EO (Polyvagal): 0% activation in training",
            "NDAM (Crisis salience): 0% activation in training",
            "RNX (Temporal dynamics): 0% activation in training",
            "CARD: 26% activation (low)",
            "PRESENCE: 48% activation (moderate)",
            "AUTHENTICITY: 52% activation (moderate)"
        ])

        return list(set(weak_organs))

    def _identify_weak_capabilities(self) -> List[str]:
        """Identify capabilities that need improvement."""
        weak_capabilities = []

        for result in self.results:
            if not result.success:
                weak_capabilities.append(
                    f"{result.test_id} ({result.test_name}): {result.reasoning}"
                )

        return weak_capabilities

    def _generate_training_recommendations(
        self,
        weak_organs: List[str],
        weak_capabilities: List[str]
    ) -> List[str]:
        """Generate targeted training recommendations."""
        recommendations = []

        # Organ-specific recommendations
        if any("EO" in w for w in weak_organs):
            recommendations.append(
                "Create EO polyvagal training corpus (30-50 pairs): "
                "ventral/sympathetic/dorsal state detection"
            )

        if any("NDAM" in w for w in weak_organs):
            recommendations.append(
                "Create NDAM crisis salience corpus (30-50 pairs): "
                "urgency detection, crisis identification"
            )

        if any("RNX" in w for w in weak_organs):
            recommendations.append(
                "Create RNX temporal dynamics corpus (30-50 pairs): "
                "rhythm detection, temporal coherence"
            )

        if any("CARD" in w for w in weak_organs):
            recommendations.append(
                "Enhance CARD response scaling corpus: "
                "minimal/moderate/comprehensive response sizing"
            )

        # Capability-specific recommendations
        if any("INTEL-003" in c for c in weak_capabilities):
            recommendations.append(
                "Add novelty handling training: out-of-distribution inputs, "
                "appropriate uncertainty calibration"
            )

        if any("CONT-006" in c for c in weak_capabilities):
            recommendations.append(
                "Add meta-atom bridge training: trauma-informed atoms, "
                "bridge atoms, contextual activation"
            )

        # General recommendations
        if len(weak_organs) >= 3:
            recommendations.append(
                "Run 15-20 epoch general training to establish baseline "
                "before targeted training"
            )

        return recommendations

    def _print_report(self, report: ValidationReport):
        """Print detailed validation report."""
        print(f"\n{'='*70}")
        print(f"📊 COMPREHENSIVE VALIDATION REPORT")
        print(f"{'='*70}")

        print(f"\n🎯 Overall Results:")
        print(f"   Total tests: {report.total_tests}")
        print(f"   Passed: {report.tests_passed} ✅")
        print(f"   Failed: {report.tests_failed} ❌")
        print(f"   Pass rate: {report.pass_rate:.1%}")

        print(f"\n📊 Category Breakdown:")
        print(f"   Intelligence: {report.intelligence_passed}/{report.intelligence_total} "
              f"({report.intelligence_passed/report.intelligence_total:.1%})")
        print(f"   Continuity: {report.continuity_passed}/{report.continuity_total} "
              f"({report.continuity_passed/report.continuity_total:.1%})")
        print(f"   Responsiveness: {report.responsiveness_passed}/{report.responsiveness_total} "
              f"({report.responsiveness_passed/report.responsiveness_total:.1%})")
        print(f"   Superject: {report.superject_passed}/{report.superject_total} "
              f"({report.superject_passed/report.superject_total:.1%})")

        print(f"\n📋 Test Results:")
        for result in report.test_results:
            status = "✅" if result.success else "❌"
            print(f"   {status} {result.test_id} ({result.category}): {result.reasoning[:60]}...")

        print(f"\n🚨 Weak Organs:")
        for organ in report.weak_organs:
            print(f"   • {organ}")

        print(f"\n🚨 Weak Capabilities:")
        for capability in report.weak_capabilities[:5]:  # Limit to top 5
            print(f"   • {capability[:100]}...")

        print(f"\n💡 Training Recommendations:")
        for i, rec in enumerate(report.training_recommendations, 1):
            print(f"   {i}. {rec}")

        print(f"\n{'='*70}")
        if report.pass_rate >= 0.80:
            print(f"✅ VALIDATION PASSED: {report.pass_rate:.1%} pass rate (≥80% target)")
        elif report.pass_rate >= 0.60:
            print(f"⚠️  VALIDATION MODERATE: {report.pass_rate:.1%} pass rate (60-80%)")
        else:
            print(f"❌ VALIDATION FAILED: {report.pass_rate:.1%} pass rate (<60%)")
        print(f"{'='*70}")

    def save_report(self, report: ValidationReport, output_path: Path):
        """Save validation report to JSON."""
        report_dict = {
            'timestamp': report.timestamp,
            'summary': {
                'total_tests': report.total_tests,
                'tests_passed': report.tests_passed,
                'tests_failed': report.tests_failed,
                'pass_rate': report.pass_rate
            },
            'category_breakdown': {
                'intelligence': {
                    'passed': report.intelligence_passed,
                    'total': report.intelligence_total
                },
                'continuity': {
                    'passed': report.continuity_passed,
                    'total': report.continuity_total
                },
                'responsiveness': {
                    'passed': report.responsiveness_passed,
                    'total': report.responsiveness_total
                },
                'superject': {
                    'passed': report.superject_passed,
                    'total': report.superject_total
                }
            },
            'test_results': [
                {
                    'test_id': r.test_id,
                    'test_name': r.test_name,
                    'category': r.category,
                    'success': r.success,
                    'reasoning': r.reasoning,
                    'duration_seconds': r.duration_seconds
                }
                for r in report.test_results
            ],
            'diagnostics': {
                'weak_organs': report.weak_organs,
                'weak_capabilities': report.weak_capabilities,
                'training_recommendations': report.training_recommendations
            }
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(report_dict, f, indent=2)

        print(f"\n💾 Report saved to: {output_path}")


def run_comprehensive_validation(save_results: bool = True) -> ValidationReport:
    """Run comprehensive validation and optionally save results."""
    validator = ComprehensiveValidator()
    report = validator.run_all_tests(verbose=True)

    if save_results:
        output_path = Path("results/validation/comprehensive_validation_report.json")
        validator.save_report(report, output_path)

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run comprehensive Phase B validation")
    parser.add_argument('--no-save', action='store_true',
                       help='Do not save results to file')

    args = parser.parse_args()

    report = run_comprehensive_validation(save_results=not args.no_save)

    # Exit with code 0 if pass rate ≥ 80%
    sys.exit(0 if report.pass_rate >= 0.80 else 1)
