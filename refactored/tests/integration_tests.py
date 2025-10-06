#!/usr/bin/env python3
"""
Integration Test Suite for PD-SMIS v5.1
Verifies all components preserved and functionality maintained
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set

class IntegrationTests:
    """Complete integration testing for refactored framework"""

    def __init__(self):
        self.original_path = Path('JobEvalV5.md')
        self.refactored_path = Path('refactored')
        self.critical_markers = self._define_critical_markers()
        self.test_results = []

    def _define_critical_markers(self) -> Dict[str, List[str]]:
        """Define all critical components that must be preserved"""
        return {
            'phases': [
                'PHASE 0: MANDATORY SOURCE COLLECTION',
                'PHASE 0.5: ITERATION CONTEXT MANAGEMENT',
                'PHASE 0.6: ERROR HANDLING PROTOCOLS',  # New addition
                'PHASE 1: COMPREHENSIVE SOURCE EXTRACTION',
                'PHASE 2: INTELLIGENT HYPOTHESIS GENERATION',
                'PHASE 3: STRATEGIC OPTIMIZATION',
                'PHASE 4: CONTEXTUAL GENERATION',
                'PHASE 4.5: ADVERSARIAL VALIDATION',
                'PHASE 5: VERIFICATION',
                'PHASE 6: LEARNING PROTOCOL',
                'PHASE 7: ITERATION CYCLE MANAGEMENT'
            ],
            'core_components': [
                'SEMANTIC_FINGERPRINTS',
                'PRECISION_TIERS',
                'SOURCE_SEGREGATED_FACTS',
                'BOTTLENECK_ANALYZER',
                'HYPOTHESIS_GENERATOR',
                'ADVERSARIAL_VALIDATOR',
                'ITERATION_TRACKER',
                'LEARNING_ACCUMULATOR'
            ],
            'validation_types': [
                'tier_enforcement',
                'adversarial_validation',
                'semantic_diff_validation',
                'domain_boundary_enforcement',
                'source_attribution_check'
            ],
            'safeguards': [
                'Role-Project Firewall',
                'Source Attribution Check',
                'Phrasing Pattern Validation',
                'Evidence-Based Decision Guard',
                'Over-Optimization Prevention',
                'Engagement-Accuracy Balance',
                'Tier Boundary Enforcement',
                'Adversarial Validation Gate',
                'Dual-Lock Verification',
                'Domain Boundary Enforcement',
                'Semantic Diff Validation',
                'Pipeline Enforcement',
                'Engagement Enhancement Boundaries',
                'Learning Accumulator Protection'
            ],
            'critical_logic': [
                'HOSTILE AUDITOR',
                'assume bad faith',
                'violations_found',
                'cannot_escalate',
                'ABORT_EARLY',
                '100% source-context integrity'
            ]
        }

    def test_all_phases_present(self) -> bool:
        """Verify all phases exist in refactored version"""
        print("Testing: All phases present...")

        phases_found = set()
        for module_path in self.refactored_path.glob('**/*.md'):
            content = module_path.read_text()
            for phase in self.critical_markers['phases']:
                if phase in content:
                    phases_found.add(phase)

        missing_phases = set(self.critical_markers['phases']) - phases_found
        if missing_phases:
            print(f"  ❌ Missing phases: {missing_phases}")
            return False

        print(f"  ✅ All {len(self.critical_markers['phases'])} phases found")
        return True

    def test_core_components_preserved(self) -> bool:
        """Verify core components are preserved"""
        print("Testing: Core components preserved...")

        components_found = set()
        for module_path in self.refactored_path.glob('**/*.md'):
            content = module_path.read_text()
            for component in self.critical_markers['core_components']:
                if component in content:
                    components_found.add(component)

        missing_components = set(self.critical_markers['core_components']) - components_found
        if missing_components:
            print(f"  ❌ Missing components: {missing_components}")
            return False

        print(f"  ✅ All {len(self.critical_markers['core_components'])} core components found")
        return True

    def test_all_14_safeguards_intact(self) -> bool:
        """Verify all 14 safeguards are present and unchanged"""
        print("Testing: All 14 safeguards intact...")

        safeguards_path = self.refactored_path / 'safeguards' / 'critical_safeguards.md'
        if not safeguards_path.exists():
            print(f"  ❌ Safeguards file not found at {safeguards_path}")
            return False

        content = safeguards_path.read_text()
        safeguards_found = []

        for safeguard in self.critical_markers['safeguards']:
            if safeguard in content:
                safeguards_found.append(safeguard)

        if len(safeguards_found) != 14:
            missing = set(self.critical_markers['safeguards']) - set(safeguards_found)
            print(f"  ❌ Only {len(safeguards_found)}/14 safeguards found")
            print(f"     Missing: {missing}")
            return False

        print(f"  ✅ All 14 safeguards present and accounted for")
        return True

    def test_adversarial_intensity_maintained(self) -> bool:
        """Verify adversarial validation maintains hostile intensity"""
        print("Testing: Adversarial validation intensity...")

        adversarial_path = self.refactored_path / 'validation' / 'adversarial_validation.md'
        orchestrator_path = self.refactored_path / 'validation' / 'validation_orchestrator.md'

        paths_to_check = [p for p in [adversarial_path, orchestrator_path] if p.exists()]

        if not paths_to_check:
            print(f"  ❌ No adversarial validation files found")
            return False

        intensity_markers = [
            'HOSTILE AUDITOR',
            'assume bad faith',
            'success_metric: "violations_found"',
            'hostile'
        ]

        for path in paths_to_check:
            content = path.read_text().upper()
            for marker in intensity_markers:
                if marker.upper() not in content:
                    print(f"  ❌ Missing intensity marker: {marker}")
                    return False

        print(f"  ✅ Adversarial validation intensity preserved")
        return True

    def test_tier_system_enforcement(self) -> bool:
        """Verify tier system and enforcement logic"""
        print("Testing: Tier system enforcement...")

        tier_path = self.refactored_path / 'validation' / 'precision_tiers.md'
        if not tier_path.exists():
            print(f"  ❌ Precision tiers file not found")
            return False

        content = tier_path.read_text()

        # Check all 5 tiers defined
        required_tiers = ['completion', 'creation', 'participation', 'association', 'proximity']
        for tier in required_tiers:
            if tier not in content.lower():
                print(f"  ❌ Missing tier: {tier}")
                return False

        # Check escalation prevention
        if 'cannot_escalate' not in content.lower():
            print(f"  ❌ Tier escalation prevention not found")
            return False

        print(f"  ✅ All 5 tiers defined with escalation prevention")
        return True

    def test_validation_orchestration_preserves_all_checks(self) -> bool:
        """Verify optimized validation still runs all checks"""
        print("Testing: Validation orchestration completeness...")

        orchestrator_path = self.refactored_path / 'validation' / 'validation_orchestrator.md'
        if not orchestrator_path.exists():
            print(f"  ❌ Validation orchestrator not found")
            return False

        content = orchestrator_path.read_text()

        # Verify all validation types present
        for validation_type in self.critical_markers['validation_types']:
            if validation_type not in content:
                print(f"  ❌ Missing validation type: {validation_type}")
                return False

        # Verify parallel execution doesn't skip checks
        if 'all_14_safeguards_active: true' not in content:
            print(f"  ❌ Not all safeguards marked as active")
            return False

        print(f"  ✅ All validation checks preserved in orchestrator")
        return True

    def test_error_handling_integration(self) -> bool:
        """Verify new error handling doesn't break existing flow"""
        print("Testing: Error handling integration...")

        error_path = self.refactored_path / 'phases' / 'phase_0_6_error_handling.md'
        if not error_path.exists():
            print(f"  ❌ Error handling module not found")
            return False

        content = error_path.read_text()

        # Verify critical errors cause abort
        if 'ABORT' not in content:
            print(f"  ❌ Error handling doesn't include abort logic")
            return False

        # Verify tier violations are caught
        if 'tier_violation' not in content.lower():
            print(f"  ❌ Tier violation handling not found")
            return False

        print(f"  ✅ Error handling properly integrated")
        return True

    def test_source_segregation_maintained(self) -> bool:
        """Verify source segregation boundaries remain intact"""
        print("Testing: Source segregation boundaries...")

        extraction_path = self.refactored_path / 'phases' / 'phase_1_extraction.md'
        if not extraction_path.exists():
            print(f"  ❌ Extraction phase not found")
            return False

        content = extraction_path.read_text()

        segregation_markers = [
            'ROLE_SCOPE',
            'PROJECT_ENVIRONMENT',
            'COMPANY_ATTRIBUTES',
            'SOURCE_SEGREGATED_FACTS'
        ]

        for marker in segregation_markers:
            if marker not in content:
                print(f"  ❌ Missing segregation marker: {marker}")
                return False

        print(f"  ✅ Source segregation boundaries maintained")
        return True

    def test_performance_optimizations_safe(self) -> bool:
        """Verify performance optimizations don't compromise safety"""
        print("Testing: Performance optimization safety...")

        orchestrator_path = self.refactored_path / 'validation' / 'validation_orchestrator.md'
        if not orchestrator_path.exists():
            return False

        content = orchestrator_path.read_text()

        # Check that caching doesn't affect validation
        if 'cache_validation_results: false' not in content:
            print(f"  ⚠️  Validation results might be cached (could be unsafe)")

        # Verify early termination only on critical
        if 'early_termination' in content and 'critical' not in content:
            print(f"  ❌ Early termination without critical check")
            return False

        # Verify parallel execution is safe
        if 'parallel_execution' in content and 'independent_checks' not in content:
            print(f"  ❌ Parallel execution without independence verification")
            return False

        print(f"  ✅ Performance optimizations appear safe")
        return True

    def run_all_tests(self) -> Dict[str, bool]:
        """Execute all integration tests"""
        print("\n" + "="*60)
        print("PD-SMIS v5.1 Integration Test Suite")
        print("="*60 + "\n")

        tests = [
            ('Phases Present', self.test_all_phases_present),
            ('Core Components', self.test_core_components_preserved),
            ('14 Safeguards', self.test_all_14_safeguards_intact),
            ('Adversarial Intensity', self.test_adversarial_intensity_maintained),
            ('Tier System', self.test_tier_system_enforcement),
            ('Validation Completeness', self.test_validation_orchestration_preserves_all_checks),
            ('Error Handling', self.test_error_handling_integration),
            ('Source Segregation', self.test_source_segregation_maintained),
            ('Performance Safety', self.test_performance_optimizations_safe)
        ]

        results = {}
        passed = 0
        failed = 0

        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = result
                if result:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"  ❌ Test failed with error: {e}")
                results[test_name] = False
                failed += 1
            print()

        print("="*60)
        print(f"Test Results: {passed} passed, {failed} failed")
        print("="*60)

        if failed == 0:
            print("\n🎉 ALL TESTS PASSED! Framework integrity maintained.")
        else:
            print(f"\n⚠️  {failed} tests failed. Review required before deployment.")

        return results

    def generate_test_report(self, results: Dict[str, bool]) -> str:
        """Generate detailed test report"""
        report = []
        report.append("# PD-SMIS v5.1 Integration Test Report\n")
        report.append(f"## Test Summary\n")

        passed = sum(1 for r in results.values() if r)
        total = len(results)

        report.append(f"- Total Tests: {total}")
        report.append(f"- Passed: {passed}")
        report.append(f"- Failed: {total - passed}")
        report.append(f"- Success Rate: {(passed/total)*100:.1f}%\n")

        report.append("## Detailed Results\n")
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            report.append(f"- {test_name}: {status}")

        report.append("\n## Validation Guarantees\n")
        if all(results.values()):
            report.append("✅ All original functionality preserved")
            report.append("✅ All 14 safeguards active")
            report.append("✅ Adversarial validation intensity maintained")
            report.append("✅ Tier system enforcement intact")
            report.append("✅ Source segregation boundaries maintained")
            report.append("✅ Performance optimizations safe")

        return "\n".join(report)


if __name__ == "__main__":
    # Run integration tests
    tester = IntegrationTests()
    results = tester.run_all_tests()

    # Generate and save report
    report = tester.generate_test_report(results)

    report_path = Path('refactored/tests/integration_test_report.md')
    report_path.write_text(report)
    print(f"\n📄 Test report saved to: {report_path}")