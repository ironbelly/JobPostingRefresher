"""
Regression tests to ensure v6 maintains v5.1 capabilities
Run with: python3 -m unittest tests.test_regression -v
"""
import unittest
from pathlib import Path
import sys
import os
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clui.pd_smis_engine import PDSMISEngine
from clui.job_manager import JobManager


class TestRegression(unittest.TestCase):
    """Ensure no regression from v5.1 capabilities"""

    def test_phase_sequence_preserved(self):
        """Test phase execution order matches v5.1"""
        engine = PDSMISEngine()

        phases = engine.get_phase_sequence()

        # Should have 9 phases based on v5.1
        self.assertEqual(len(phases), 9)

        # Check for critical phases
        self.assertIn("phase_0_collection", phases)
        self.assertIn("phase_1_extraction", phases)
        self.assertIn("phase_2_hypothesis", phases)
        self.assertIn("phase_3_optimization", phases)
        self.assertIn("phase_4_generation", phases)
        self.assertIn("phase_6_learning", phases)
        self.assertIn("phase_7_iteration", phases)

        print("✅ Phase sequence preserved")

    def test_validation_tiers_preserved(self):
        """Test validation tier structure matches v5.1"""
        engine = PDSMISEngine()

        tiers = engine.get_validation_tiers()

        # Should have 3 tiers in v5.1
        self.assertEqual(len(tiers), 3)

        # Check for all tiers
        self.assertIn("tier_1_precision", tiers)
        self.assertIn("tier_2_adversarial", tiers)
        self.assertIn("tier_3_verification", tiers)

        # Check tier structure
        for tier_name, tier_config in tiers.items():
            self.assertIn("criteria", tier_config)
            self.assertIn("threshold", tier_config)
            self.assertIsInstance(tier_config["criteria"], list)
            self.assertIsInstance(tier_config["threshold"], float)

        print("✅ Validation tiers preserved")

    def test_engine_output_structure(self):
        """Test engine output maintains v5.1 structure"""
        engine = PDSMISEngine()

        result = engine.process_job({
            "job_id": "regression_test",
            "title": "Test Job",
            "company": "TestCo",
            "raw_content": "Test content for regression testing"
        })

        # Check required output structure
        self.assertTrue(result["success"])
        self.assertIn("optimized_content", result)
        self.assertIn("validation_results", result)
        self.assertIn("metrics", result)
        self.assertIn("processing_metadata", result)

        # Check metrics structure
        metrics = result["metrics"]
        self.assertIn("precision_score", metrics)
        self.assertIn("adversarial_score", metrics)
        self.assertIn("verification_score", metrics)
        self.assertIn("overall_quality", metrics)

        # Check processing metadata
        metadata = result["processing_metadata"]
        self.assertIn("engine_version", metadata)
        self.assertIn("wrapper_version", metadata)
        self.assertEqual(metadata["engine_version"], "5.1")
        self.assertEqual(metadata["wrapper_version"], "6.0")

        print("✅ Engine output structure preserved")

    def test_backwards_compatibility(self):
        """Test v6 can handle v5.1 style operations"""
        temp_dir = tempfile.mkdtemp()

        try:
            jm = JobManager(base_path=temp_dir)

            # Create job with v5.1 style data
            result = jm.create_job(
                job_id='test_001',
                title='Test Job Title',
                company='Test Company',
                raw_data='Test job posting content for backwards compatibility testing'
            )

            # Should work exactly as v5.1 would expect
            self.assertTrue(result["success"])
            self.assertEqual(result["job_id"], 'test_001')

            jobs = jm.list_jobs()
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0]["title"], 'Test Job Title')

            print("✅ Backwards compatibility maintained")

        finally:
            shutil.rmtree(temp_dir)

    def test_no_feature_regression(self):
        """Test all v5.1 features still available"""
        engine = PDSMISEngine()

        # Test input validation
        validation = engine.validate_input({
            "raw_content": "Test content"
        })
        self.assertIn("valid", validation)
        self.assertIn("errors", validation)
        self.assertIn("warnings", validation)

        # Test engine info
        info = engine.get_engine_info()
        self.assertIn("engine_version", info)
        self.assertIn("wrapper_version", info)
        self.assertIn("phases_count", info)
        self.assertIn("validation_tiers_count", info)
        self.assertIn("capabilities", info)
        self.assertIn("constraints", info)

        # Test batch processing
        jobs = [
            {"raw_content": f"Job {i}"} for i in range(3)
        ]
        results = engine.batch_process_jobs(jobs)
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result["success"])

        print("✅ No feature regression detected")


if __name__ == "__main__":
    unittest.main()
