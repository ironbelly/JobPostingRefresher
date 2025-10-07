# Milestone 7: Testing Framework - Preservation and Validation

## Purpose
Implement comprehensive testing framework to ensure v5.1 preservation, validate all functionality, and establish quality gates for the complete system.

**Success Criteria:**
- All preservation tests passing (v5.1 100% intact)
- Component integration tests passing
- End-to-end workflow tests passing
- Performance benchmarks met
- No regression from v5.1 capabilities

## Dependencies
- M1-M6 (all must be complete)

## Start Procedure

### Pre-flight Checks
```bash
# 1. Verify all milestones complete
for i in {1..6}; do
    [ -f "/dev/v6/M${i}.COMPLETE" ] && echo "✅ M${i} Complete" || echo "❌ M${i} not complete"
done

# 2. CRITICAL: Verify v5.1 still intact
./dev/v6/check_preservation.sh || exit 1

# 3. Check test environment
source venv/bin/activate
python -m pytest --version

# 4. Check all components present
[ -f "clui/job_manager.py" ] && echo "✅ JobManager present"
[ -f "clui/teamtailor_client.py" ] && echo "✅ TeamTailor present"
[ -f "clui/pd_smis_engine.py" ] && echo "✅ Engine wrapper present"
[ -f "clui/jbr.py" ] && echo "✅ CLUI present"
```

### Initialize Milestone
```bash
touch /dev/v6/M7.IN_PROGRESS
echo "M7 Started: $(date)" >> /dev/v6/execution_log.md
```

## Tasks

### Task 7.1: Create Master Preservation Test
Create `tests/test_v5_preservation_final.py`:
```python
"""
CRITICAL: Final v5.1 preservation verification
This test MUST pass or the entire v6.0 is invalid
Run with: pytest tests/test_v5_preservation_final.py -v
"""
import pytest
import hashlib
from pathlib import Path
import subprocess
import json


class TestV5PreservationFinal:
    """Final comprehensive v5.1 preservation tests"""

    def test_no_modifications_to_ibjobrefresher(self):
        """CRITICAL: Verify zero modifications to IBJobRefresher directory"""
        # Check git status for any changes
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'IBJobRefresher/'],
            capture_output=True,
            text=True
        )

        modified_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        assert len(modified_files) == 0, f"CRITICAL: v5.1 files modified: {modified_files}"

    def test_all_critical_files_present(self):
        """Verify all critical v5.1 files exist"""
        critical_files = [
            "IBJobRefresher/orchestrator.md",
            "IBJobRefresher/phases/phase_0_collection.md",
            "IBJobRefresher/phases/phase_0_5_iteration.md",
            "IBJobRefresher/phases/phase_0_6_error_handling.md",
            "IBJobRefresher/phases/phase_1_extraction.md",
            "IBJobRefresher/phases/phase_2_hypothesis.md",
            "IBJobRefresher/phases/phase_3_optimization.md",
            "IBJobRefresher/phases/phase_4_generation.md",
            "IBJobRefresher/phases/phase_6_learning.md",
            "IBJobRefresher/phases/phase_7_iteration.md",
            "IBJobRefresher/validation/adversarial_validation.md",
            "IBJobRefresher/validation/precision_tiers.md",
            "IBJobRefresher/validation/validation_orchestrator.md",
            "IBJobRefresher/validation/verification_suite.md",
            "IBJobRefresher/safeguards/critical_safeguards.md",
            "IBJobRefresher/components/output_format.md"
        ]

        for file_path in critical_files:
            assert Path(file_path).exists(), f"Critical file missing: {file_path}"

    def test_checksum_verification(self):
        """Verify checksums match baseline"""
        baseline_file = Path("dev/v6/v5_baseline_checksums.txt")

        if not baseline_file.exists():
            pytest.skip("No baseline checksums found (run M1 first)")

        # Read baseline
        baseline = {}
        with open(baseline_file, 'r') as f:
            for line in f:
                if line.strip() and 'IBJobRefresher' in line:
                    parts = line.strip().split('  ')
                    if len(parts) == 2:
                        checksum, filepath = parts
                        baseline[filepath] = checksum

        # Verify each file
        for filepath, expected_checksum in baseline.items():
            if Path(filepath).exists():
                with open(filepath, 'rb') as f:
                    actual_checksum = hashlib.md5(f.read()).hexdigest()
                assert actual_checksum == expected_checksum, \
                    f"Checksum mismatch for {filepath}"

    def test_required_markers_present(self):
        """Verify all required prompt markers exist"""
        collection_file = Path("IBJobRefresher/phases/phase_0_collection.md")

        if collection_file.exists():
            content = collection_file.read_text()

            required_markers = [
                "[PROJECT DESCRIPTION]",
                "[/PROJECT DESCRIPTION]",
                "[ORIGINAL JOB TITLE]",
                "[/ORIGINAL JOB TITLE]",
                "[ORIGINAL JOB POSTING]",
                "[/ORIGINAL JOB POSTING]",
                "[ORIGINAL JOB KPIs]",
                "[/ORIGINAL JOB KPIs]"
            ]

            for marker in required_markers:
                assert marker in content, f"Required marker missing: {marker}"

    def test_wrapper_doesnt_import_from_engine(self):
        """Verify wrapper doesn't import from IBJobRefresher"""
        wrapper_file = Path("clui/pd_smis_engine.py")

        if wrapper_file.exists():
            content = wrapper_file.read_text()
            assert 'from IBJobRefresher' not in content
            assert 'import IBJobRefresher' not in content
            print("✅ Wrapper correctly isolated from engine")

    def test_phase_sequence_preserved(self):
        """Verify phase execution sequence unchanged"""
        from clui.pd_smis_engine import PDSMISEngine

        engine = PDSMISEngine()
        expected = [
            "phase_0_collection",
            "phase_0_5_iteration",
            "phase_1_extraction",
            "phase_2_hypothesis",
            "phase_3_optimization",
            "phase_4_generation",
            "phase_4_5_adversarial",
            "phase_5_verification",
            "phase_6_learning",
            "phase_7_iteration"
        ]

        actual = engine.get_phase_sequence()
        assert actual == expected, "Phase sequence has been altered"

    def test_validation_layers_complete(self):
        """Verify all 14 validation layers present"""
        from clui.pd_smis_engine import PDSMISEngine

        engine = PDSMISEngine()
        report = engine._generate_validation_report()

        expected_layers = [
            "semantic_diff_check",
            "hallucination_detection",
            "fact_preservation",
            "kpi_impact_validation",
            "tier_enforcement",
            "adversarial_validation",
            "role_boundary_check",
            "project_boundary_check",
            "company_boundary_check",
            "statistical_validation",
            "constraint_satisfaction",
            "evidence_chain_validation",
            "iteration_consistency",
            "final_safety_check"
        ]

        for layer in expected_layers:
            assert layer in report['validation_layers'], \
                f"Validation layer missing: {layer}"

        assert len(report['validation_layers']) == 14, \
            "Must have exactly 14 validation layers"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
```

### Task 7.2: Create Integration Test Suite
Create `tests/test_integration_complete.py`:
```python
"""
Complete integration tests for v6.0
Run with: pytest tests/test_integration_complete.py -v
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from clui.job_manager import JobManager
from clui.teamtailor_client import TeamTailorClient
from clui.pd_smis_engine import PDSMISEngine


class TestCompleteIntegration:
    """Test complete system integration"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)

    @pytest.fixture
    def job_manager(self, temp_dir):
        """Create JobManager with temp directory"""
        return JobManager(temp_dir / "jobs")

    @pytest.fixture
    def engine(self):
        """Create engine wrapper"""
        return PDSMISEngine()

    def test_full_workflow(self, job_manager, engine):
        """Test complete workflow: create -> optimize -> export"""
        # Step 1: Create job
        job_id = job_manager.create_job(
            title="Integration Test Job",
            company="Test Company",
            description="This is a test job for integration testing",
            project="Test project description",
            kpis={
                'visit_application_rate': 2.0,
                'application_interview_rate': 10.0
            }
        )

        assert job_id is not None
        print(f"✅ Created job: {job_id}")

        # Step 2: List and retrieve job
        jobs = job_manager.list_jobs()
        assert len(jobs) == 1
        assert jobs[0]['title'] == "Integration Test Job"

        job_path = jobs[0]['path']
        job_data = job_manager.get_job_data(job_path)
        assert job_data['title'] == "Integration Test Job"
        print("✅ Job retrieval working")

        # Step 3: Create new version
        new_version = job_manager.create_version(job_path)
        assert new_version.name == 'v2'
        print("✅ Version management working")

        # Step 4: Process through engine
        result = engine.process_job(job_data)
        assert result['status'] == 'success'
        assert 'validation_report' in result
        assert result['validation_report']['passed'] == True
        print("✅ Engine processing working")

        # Step 5: Save optimized data
        job_manager.save_processed_job(job_path, 'v2', result)

        # Step 6: Verify saved data
        optimized_data = job_manager.get_job_data(job_path, 'v2')
        assert '[Optimized]' in optimized_data['title']
        print("✅ Save and retrieval working")

        # Step 7: Export job
        export_path = job_manager.export_job(job_path, format="json")
        assert Path(export_path).exists()
        print("✅ Export working")

        # Step 8: Search functionality
        search_results = job_manager.search_jobs("Integration")
        assert len(search_results) == 1
        print("✅ Search working")

        # Step 9: Clean up
        job_manager.delete_job(job_path)
        jobs = job_manager.list_jobs()
        assert len(jobs) == 0
        print("✅ Deletion working")

        print("\n✅ COMPLETE WORKFLOW TEST PASSED")

    def test_data_persistence(self, job_manager):
        """Test data persists across instances"""
        # Create job with first instance
        job_id = job_manager.create_job("Persistence Test")

        # Create new instance with same directory
        job_manager2 = JobManager(job_manager.jobs_dir)

        # Should find the job
        jobs = job_manager2.list_jobs()
        assert len(jobs) == 1
        assert jobs[0]['title'] == "Persistence Test"
        print("✅ Data persistence working")

    def test_error_handling(self, job_manager, engine):
        """Test error handling throughout system"""
        # Test invalid job path
        with pytest.raises(FileNotFoundError):
            job_manager.get_job_data("nonexistent/path")

        # Test invalid version
        job_id = job_manager.create_job("Error Test")
        jobs = job_manager.list_jobs()

        with pytest.raises(FileNotFoundError):
            job_manager.get_job_data(jobs[0]['path'], 'v99')

        # Test invalid export format
        with pytest.raises(ValueError):
            job_manager.export_job(jobs[0]['path'], format="invalid")

        print("✅ Error handling working")

    def test_teamtailor_graceful_degradation(self):
        """Test system works without TeamTailor configuration"""
        client = TeamTailorClient()

        # Should handle missing config gracefully
        result = client.fetch_job("test")
        assert result is None

        jobs = client.list_all_jobs()
        assert jobs == []

        connected = client.test_connection()
        assert connected == False

        print("✅ TeamTailor graceful degradation working")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Task 7.3: Create End-to-End Test
Create `tests/test_e2e_workflow.py`:
```python
"""
End-to-end workflow tests
Run with: pytest tests/test_e2e_workflow.py -v
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "clui"))

from jbr import JobRefresherCLUI


class TestE2EWorkflow:
    """Test end-to-end workflows through CLUI"""

    @pytest.fixture
    def app(self):
        """Create CLUI app with mocked console"""
        with patch('jbr.Console'):
            app = JobRefresherCLUI()
            app.console = Mock()
            return app

    def test_job_creation_workflow(self, app):
        """Test complete job creation workflow"""
        # Mock user inputs
        with patch('jbr.Prompt.ask') as mock_prompt:
            mock_prompt.side_effect = [
                'Test Job Title',  # Title
                'Test Company',    # Company
                'N',              # No TeamTailor import
                '',               # Default for other prompts
            ]

            with patch('jbr.Confirm.ask', return_value=True):
                with patch.object(app, 'get_multiline_input') as mock_multi:
                    mock_multi.side_effect = [
                        'Test job description',
                        'Test project description'
                    ]

                    # Run creation
                    app.create_new_job()

                    # Verify job was created
                    jobs = app.job_manager.list_jobs()
                    assert len(jobs) > 0
                    print("✅ Job creation workflow works")

    def test_optimization_workflow(self, app):
        """Test job optimization workflow"""
        # Create a test job first
        job_id = app.job_manager.create_job(
            title="Optimization Test",
            description="Test job for optimization"
        )

        jobs = app.job_manager.list_jobs()
        job_path = jobs[0]['path']

        # Mock console for optimization
        with patch('jbr.time.sleep'):  # Skip delays
            app.optimize_job(job_path)

        # Verify new version created
        versions = app.job_manager.get_version_history(job_path)
        assert len(versions) > 1
        print("✅ Optimization workflow works")

    def test_navigation_flow(self, app):
        """Test menu navigation"""
        # Test navigation path tracking
        assert app.current_path == ["Home"]

        # Simulate navigation
        app.current_path.append("Job Management")
        assert len(app.current_path) == 2

        app.current_path.pop()
        assert app.current_path == ["Home"]
        print("✅ Navigation flow works")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Task 7.4: Create Performance Benchmark Tests
Create `tests/test_performance.py`:
```python
"""
Performance benchmark tests
Run with: pytest tests/test_performance.py -v
"""
import pytest
import time
import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from clui.job_manager import JobManager


class TestPerformance:
    """Performance benchmark tests"""

    @pytest.fixture
    def job_manager(self):
        """Create JobManager with temp directory"""
        temp_dir = tempfile.mkdtemp()
        yield JobManager(Path(temp_dir) / "jobs")
        import shutil
        shutil.rmtree(temp_dir)

    def test_job_creation_performance(self, job_manager):
        """Test job creation performance"""
        start_time = time.time()

        for i in range(10):
            job_manager.create_job(
                title=f"Performance Test Job {i}",
                description=f"Description for job {i}"
            )

        elapsed = time.time() - start_time

        # Should create 10 jobs in under 5 seconds
        assert elapsed < 5.0, f"Job creation too slow: {elapsed:.2f}s"
        print(f"✅ Created 10 jobs in {elapsed:.2f}s")

    def test_job_listing_performance(self, job_manager):
        """Test job listing performance with many jobs"""
        # Create 50 jobs
        for i in range(50):
            job_manager.create_job(f"Job {i}")

        start_time = time.time()
        jobs = job_manager.list_jobs()
        elapsed = time.time() - start_time

        assert len(jobs) == 50
        assert elapsed < 1.0, f"Job listing too slow: {elapsed:.2f}s"
        print(f"✅ Listed 50 jobs in {elapsed:.2f}s")

    def test_search_performance(self, job_manager):
        """Test search performance"""
        # Create jobs with varied content
        for i in range(30):
            job_manager.create_job(
                title=f"Job {i}",
                description=f"Python developer position {i}" if i % 2 == 0 else f"Java position {i}"
            )

        start_time = time.time()
        results = job_manager.search_jobs("Python")
        elapsed = time.time() - start_time

        assert len(results) == 15  # Half have "Python"
        assert elapsed < 2.0, f"Search too slow: {elapsed:.2f}s"
        print(f"✅ Searched 30 jobs in {elapsed:.2f}s")

    def test_version_creation_performance(self, job_manager):
        """Test version creation performance"""
        job_id = job_manager.create_job("Version Test")
        jobs = job_manager.list_jobs()
        job_path = jobs[0]['path']

        start_time = time.time()

        for i in range(5):
            job_manager.create_version(job_path)

        elapsed = time.time() - start_time

        versions = job_manager.get_version_history(job_path)
        assert len(versions) == 6  # v1 + 5 new versions
        assert elapsed < 3.0, f"Version creation too slow: {elapsed:.2f}s"
        print(f"✅ Created 5 versions in {elapsed:.2f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Task 7.5: Create Validation Report Generator
Create `tests/generate_validation_report.py`:
```python
"""
Generate comprehensive validation report for v6.0
Run with: python tests/generate_validation_report.py
"""
import subprocess
import json
from pathlib import Path
from datetime import datetime


def run_test(test_file):
    """Run a test file and return results"""
    result = subprocess.run(
        ['python', '-m', 'pytest', test_file, '-v', '--tb=short'],
        capture_output=True,
        text=True
    )
    return {
        'passed': result.returncode == 0,
        'output': result.stdout,
        'errors': result.stderr
    }


def generate_report():
    """Generate comprehensive validation report"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'version': 'v6.0',
        'tests': {},
        'summary': {
            'total': 0,
            'passed': 0,
            'failed': 0
        }
    }

    # Test files to run
    test_files = [
        'tests/test_v5_preservation_final.py',
        'tests/test_job_manager.py',
        'tests/test_teamtailor_client.py',
        'tests/test_engine_preservation.py',
        'tests/test_output_comparison.py',
        'tests/test_clui_basic.py',
        'tests/test_clui_features.py',
        'tests/test_integration_complete.py',
        'tests/test_e2e_workflow.py',
        'tests/test_performance.py'
    ]

    print("JobRefresher v6.0 Validation Report")
    print("=" * 50)

    for test_file in test_files:
        if Path(test_file).exists():
            print(f"Running {test_file}...")
            result = run_test(test_file)

            report['tests'][test_file] = result
            report['summary']['total'] += 1

            if result['passed']:
                report['summary']['passed'] += 1
                print(f"  ✅ PASSED")
            else:
                report['summary']['failed'] += 1
                print(f"  ❌ FAILED")
                print(f"  Error: {result['errors'][:200]}")

    # Critical v5.1 preservation check
    print("\n" + "=" * 50)
    print("CRITICAL: v5.1 Preservation Check")

    checksum_result = subprocess.run(
        ['./dev/v6/check_preservation.sh'],
        capture_output=True,
        text=True
    )

    if checksum_result.returncode == 0:
        print("✅ v5.1 ENGINE COMPLETELY PRESERVED")
        report['v5_preservation'] = 'PASSED'
    else:
        print("❌ v5.1 ENGINE MODIFIED - CRITICAL FAILURE")
        report['v5_preservation'] = 'FAILED'

    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Total Tests: {report['summary']['total']}")
    print(f"  Passed: {report['summary']['passed']}")
    print(f"  Failed: {report['summary']['failed']}")
    print(f"  v5.1 Preservation: {report['v5_preservation']}")

    # Save report
    with open('validation_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print("\nReport saved to validation_report.json")

    # Final verdict
    if report['summary']['failed'] == 0 and report['v5_preservation'] == 'PASSED':
        print("\n🎉 ALL VALIDATION TESTS PASSED - v6.0 READY FOR RELEASE")
        return 0
    else:
        print("\n❌ VALIDATION FAILED - DO NOT RELEASE")
        return 1


if __name__ == "__main__":
    exit(generate_report())
```

### Task 7.6: Create Regression Test Suite
Create `tests/test_regression.py`:
```python
"""
Regression tests to ensure v6 maintains v5.1 capabilities
Run with: pytest tests/test_regression.py -v
"""
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from clui.pd_smis_engine import PDSMISEngine
from clui.job_manager import JobManager


class TestRegression:
    """Ensure no regression from v5.1 capabilities"""

    def test_input_format_compatibility(self):
        """Test v5.1 input format still works"""
        engine = PDSMISEngine()

        # v5.1 format data
        v5_data = {
            'title': 'Senior Developer',
            'posting': 'We are looking for a senior developer...',
            'project_description': 'Building cloud platform',
            'metrics': {
                'kpis': {
                    'visit_application_rate': 2.0,
                    'application_screening_rate': 45.0,
                    'application_interview_rate': 15.0,
                    'interview_offer_rate': 25.0,
                    'offer_hire_rate': 60.0
                }
            }
        }

        formatted = engine._format_for_pdsmis(v5_data)

        # All v5.1 markers present
        assert '[PROJECT DESCRIPTION]' in formatted
        assert '[ORIGINAL JOB TITLE]' in formatted
        assert '[ORIGINAL JOB POSTING]' in formatted
        assert '[ORIGINAL JOB KPIs]' in formatted

        # Content preserved
        assert 'Senior Developer' in formatted
        assert 'cloud platform' in formatted
        assert '2.0%' in formatted or '2%' in formatted

    def test_validation_layers_unchanged(self):
        """Test all 14 validation layers still present"""
        engine = PDSMISEngine()
        report = engine._generate_validation_report()

        # Exact v5.1 validation layer names
        v5_layers = [
            "semantic_diff_check",
            "hallucination_detection",
            "fact_preservation",
            "kpi_impact_validation",
            "tier_enforcement",
            "adversarial_validation",
            "role_boundary_check",
            "project_boundary_check",
            "company_boundary_check",
            "statistical_validation",
            "constraint_satisfaction",
            "evidence_chain_validation",
            "iteration_consistency",
            "final_safety_check"
        ]

        for layer in v5_layers:
            assert layer in report['validation_layers']

    def test_phase_sequence_unchanged(self):
        """Test phase execution order unchanged"""
        engine = PDSMISEngine()

        v5_sequence = [
            "phase_0_collection",
            "phase_0_5_iteration",
            "phase_1_extraction",
            "phase_2_hypothesis",
            "phase_3_optimization",
            "phase_4_generation",
            "phase_4_5_adversarial",
            "phase_5_verification",
            "phase_6_learning",
            "phase_7_iteration"
        ]

        assert engine.get_phase_sequence() == v5_sequence

    def test_backwards_compatibility(self):
        """Test v6 can handle v5.1 style operations"""
        import tempfile
        temp_dir = tempfile.mkdtemp()
        jm = JobManager(Path(temp_dir) / "jobs")

        # Create job with v5.1 style data
        job_id = jm.create_job(
            title='Test Job Title',
            description='Test job posting content',
            project='Test project description',
            kpis={
                'visit_application_rate': 2.5,
                'application_screening_rate': 45.0,
                'application_interview_rate': 15.0,
                'interview_offer_rate': 25.0,
                'offer_hire_rate': 60.0
            }
        )

        # Should work exactly as v5.1 would expect
        assert job_id is not None
        jobs = jm.list_jobs()
        assert len(jobs) == 1

        # Clean up
        import shutil
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Task 7.7: Create CI/CD Test Script
Create `tests/run_ci_tests.sh`:
```bash
#!/bin/bash
# CI/CD test runner for v6.0
# Run this before any commit or deployment

set -e  # Exit on error

echo "======================================"
echo "JobRefresher v6.0 CI/CD Test Runner"
echo "======================================"

# 1. Check Python environment
echo "Checking Python environment..."
python --version
pip list | grep -E "rich|prompt-toolkit|requests|pytest"

# 2. CRITICAL: v5.1 Preservation Check
echo ""
echo "CRITICAL: Checking v5.1 preservation..."
./dev/v6/check_preservation.sh
if [ $? -ne 0 ]; then
    echo "❌ CRITICAL FAILURE: v5.1 has been modified!"
    exit 1
fi
echo "✅ v5.1 preserved"

# 3. Run unit tests
echo ""
echo "Running unit tests..."
pytest tests/test_job_manager.py -v --tb=short
pytest tests/test_teamtailor_client.py -v --tb=short
pytest tests/test_engine_preservation.py -v --tb=short

# 4. Run integration tests
echo ""
echo "Running integration tests..."
pytest tests/test_integration_complete.py -v --tb=short

# 5. Run preservation tests
echo ""
echo "Running final preservation tests..."
pytest tests/test_v5_preservation_final.py -v --tb=short

# 6. Run regression tests
echo ""
echo "Running regression tests..."
pytest tests/test_regression.py -v --tb=short

# 7. Quick performance check
echo ""
echo "Running performance tests..."
pytest tests/test_performance.py -v --tb=short

# 8. Generate report
echo ""
echo "Generating validation report..."
python tests/generate_validation_report.py

echo ""
echo "======================================"
echo "CI/CD Tests Complete"
echo "======================================"
```

```bash
chmod +x tests/run_ci_tests.sh
```

### Task 7.8: Create Test Coverage Report
Create `tests/check_coverage.sh`:
```bash
#!/bin/bash
# Test coverage checker

echo "Generating test coverage report..."

# Install coverage if needed
pip install coverage > /dev/null 2>&1

# Run coverage
coverage run -m pytest tests/ -v
coverage report -m --include="clui/*"
coverage html --include="clui/*"

echo "Coverage report generated in htmlcov/index.html"
echo "Open htmlcov/index.html to view detailed coverage"

# Show summary
coverage report --include="clui/*" | tail -n 1
```

```bash
chmod +x tests/check_coverage.sh
```

## Validation Tests

### V7.1: Preservation Test
```bash
# Run critical preservation test
pytest tests/test_v5_preservation_final.py -v

# Must show all tests passing
```

### V7.2: Integration Test
```bash
# Run complete integration test
pytest tests/test_integration_complete.py -v

# Should show workflow test passing
```

### V7.3: Performance Test
```bash
# Run performance benchmarks
pytest tests/test_performance.py -v

# All performance targets should be met
```

### V7.4: CI/CD Test Suite
```bash
# Run complete CI/CD test suite
./tests/run_ci_tests.sh

# All tests must pass
```

### V7.5: Coverage Check
```bash
# Check test coverage
./tests/check_coverage.sh

# Should show >80% coverage for clui modules
```

## Completion Procedure

### Final Validation
```bash
# 1. Run complete CI/CD suite
./tests/run_ci_tests.sh

# 2. Verify validation report shows all passing
cat validation_report.json | grep '"passed"'

# 3. Final v5.1 check
./dev/v6/check_preservation.sh

# 4. Check coverage
./tests/check_coverage.sh

# 5. Manual smoke test
python clui/jbr.py
# Create job, optimize, export
```

### Mark Complete
```bash
# Commit all test files
git add tests/*.py tests/*.sh
git commit -m "M7 Complete: Comprehensive testing framework"

# Mark milestone complete
mv /dev/v6/M7.IN_PROGRESS /dev/v6/M7.COMPLETE
echo "M7 Completed: $(date)" >> /dev/v6/execution_log.md
echo "✅ Milestone 7: Testing Framework COMPLETE"
echo "✅ v5.1 preservation verified"
echo "✅ All tests passing"
```

### Handoff Notes
- Complete test coverage implemented
- v5.1 preservation verified
- Integration tests passing
- Performance benchmarks met
- CI/CD pipeline ready
- Ready for M8 (Final Integration)

## Rollback Plan

If this milestone fails:

```bash
# 1. Remove test files
rm -f tests/test_v5_preservation_final.py
rm -f tests/test_integration_complete.py
rm -f tests/test_e2e_workflow.py
rm -f tests/test_performance.py
rm -f tests/test_regression.py
rm -f tests/generate_validation_report.py
rm -f tests/run_ci_tests.sh
rm -f tests/check_coverage.sh

# 2. Reset git
git reset --hard HEAD~1

# 3. Remove milestone marker
rm -f /dev/v6/M7.COMPLETE /dev/v6/M7.IN_PROGRESS

# 4. Note in execution log
echo "ROLLED BACK M7: $(date)" >> /dev/v6/execution_log.md
```