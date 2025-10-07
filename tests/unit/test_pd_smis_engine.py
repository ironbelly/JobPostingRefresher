"""
Unit tests for PDSMISEngine wrapper
Tests engine interface WITHOUT importing from IBJobRefresher
"""

import os
import unittest

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from clui.pd_smis_engine import PDSMISEngine


class TestPDSMISEngine(unittest.TestCase):
    """Test suite for PDSMISEngine wrapper"""

    def setUp(self):
        """Initialize engine wrapper"""
        self.engine = PDSMISEngine()

    def test_initialization(self):
        """Test engine wrapper initialization"""
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.engine.phases)
        self.assertIsNotNone(self.engine.validation_tiers)

    def test_phase_sequence_loading(self):
        """Test that phase sequence is loaded correctly"""
        phases = self.engine.get_phase_sequence()

        # Should have 9 phases in v5.1
        self.assertEqual(len(phases), 9)

        # Check for key phases
        self.assertIn("phase_0_collection", phases)
        self.assertIn("phase_1_extraction", phases)
        self.assertIn("phase_2_hypothesis", phases)
        self.assertIn("phase_3_optimization", phases)
        self.assertIn("phase_4_generation", phases)

    def test_validation_tiers_loading(self):
        """Test that validation tiers are loaded correctly"""
        tiers = self.engine.get_validation_tiers()

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

    def test_input_formatting(self):
        """Test formatting job data for PD-SMIS engine"""
        job_data = {
            "job_id": "test_001",
            "title": "Software Engineer",
            "company": "TestCo",
            "raw_content": "We are looking for a software engineer..."
        }

        formatted = self.engine._format_for_pdsmis(job_data)

        # Check structure
        self.assertIn("input_data", formatted)
        self.assertIn("configuration", formatted)
        self.assertIn("timestamp", formatted)

        # Check input data
        self.assertEqual(formatted["input_data"]["metadata"]["title"], "Software Engineer")
        self.assertEqual(formatted["input_data"]["metadata"]["company"], "TestCo")
        self.assertEqual(formatted["input_data"]["raw_content"], job_data["raw_content"])

        # Check configuration
        self.assertEqual(formatted["configuration"]["phases_enabled"], self.engine.phases)

    def test_output_parsing(self):
        """Test parsing PD-SMIS engine output"""
        pdsmis_output = {
            "status": "completed",
            "generated_output": {
                "optimized_title": "Optimized Title",
                "optimized_content": "Optimized content here..."
            },
            "validation": {
                "tier_1": {"passed": True, "score": 0.92}
            },
            "precision_tier_scores": {
                "tier_1": 0.92,
                "tier_2": 0.88,
                "tier_3": 0.85
            },
            "overall_quality_score": 0.88,
            "iteration_count": 2,
            "warnings": [],
            "errors": []
        }

        parsed = self.engine._parse_output(pdsmis_output)

        # Check structure
        self.assertIn("success", parsed)
        self.assertIn("optimized_content", parsed)
        self.assertIn("metrics", parsed)
        self.assertIn("iterations", parsed)

        # Check values
        self.assertTrue(parsed["success"])
        self.assertEqual(parsed["metrics"]["precision_score"], 0.92)
        self.assertEqual(parsed["metrics"]["adversarial_score"], 0.88)
        self.assertEqual(parsed["metrics"]["verification_score"], 0.85)
        self.assertEqual(parsed["iterations"], 2)

    def test_process_job_basic(self):
        """Test basic job processing"""
        job_data = {
            "job_id": "test_001",
            "title": "Software Engineer",
            "company": "TestCo",
            "raw_content": "We are looking for a software engineer with Python experience."
        }

        result = self.engine.process_job(job_data)

        # Check success
        self.assertTrue(result["success"])

        # Check required fields
        self.assertIn("optimized_content", result)
        self.assertIn("validation_results", result)
        self.assertIn("metrics", result)
        self.assertIn("processing_metadata", result)

        # Check metrics structure
        self.assertIn("precision_score", result["metrics"])
        self.assertIn("adversarial_score", result["metrics"])
        self.assertIn("verification_score", result["metrics"])
        self.assertIn("overall_quality", result["metrics"])

        # Check processing metadata
        self.assertEqual(result["processing_metadata"]["input_job_id"], "test_001")
        self.assertEqual(result["processing_metadata"]["engine_version"], "5.1")
        self.assertEqual(result["processing_metadata"]["wrapper_version"], "6.0")

    def test_process_job_with_minimal_data(self):
        """Test job processing with minimal data"""
        job_data = {
            "raw_content": "Minimal job posting"
        }

        result = self.engine.process_job(job_data)

        # Should still succeed
        self.assertTrue(result["success"])
        self.assertIn("optimized_content", result)

    def test_batch_process_jobs(self):
        """Test batch processing of multiple jobs"""
        jobs = [
            {
                "job_id": "test_001",
                "title": "Engineer 1",
                "company": "Company 1",
                "raw_content": "Content 1"
            },
            {
                "job_id": "test_002",
                "title": "Engineer 2",
                "company": "Company 2",
                "raw_content": "Content 2"
            },
            {
                "job_id": "test_003",
                "title": "Engineer 3",
                "company": "Company 3",
                "raw_content": "Content 3"
            }
        ]

        results = self.engine.batch_process_jobs(jobs)

        # Should process all jobs
        self.assertEqual(len(results), 3)

        # Check all succeeded
        for i, result in enumerate(results):
            self.assertTrue(result["success"])
            self.assertEqual(result["batch_index"], i)

    def test_validate_input_valid(self):
        """Test input validation with valid data"""
        job_data = {
            "job_id": "test_001",
            "title": "Software Engineer",
            "company": "TestCo",
            "raw_content": "We are looking for a software engineer with at least 50 characters of content."
        }

        validation = self.engine.validate_input(job_data)

        self.assertTrue(validation["valid"])
        self.assertEqual(len(validation["errors"]), 0)

    def test_validate_input_missing_content(self):
        """Test input validation with missing content"""
        job_data = {
            "title": "Software Engineer",
            "company": "TestCo"
        }

        validation = self.engine.validate_input(job_data)

        self.assertFalse(validation["valid"])
        self.assertGreater(len(validation["errors"]), 0)
        self.assertIn("raw_content", validation["errors"][0])

    def test_validate_input_short_content(self):
        """Test input validation with short content"""
        job_data = {
            "raw_content": "Short"
        }

        validation = self.engine.validate_input(job_data)

        # Should be valid but have warnings
        self.assertTrue(validation["valid"])
        self.assertGreater(len(validation["warnings"]), 0)

    def test_validate_input_long_content(self):
        """Test input validation with very long content"""
        job_data = {
            "raw_content": "x" * 60000  # 60,000 characters
        }

        validation = self.engine.validate_input(job_data)

        # Should be valid but have warnings
        self.assertTrue(validation["valid"])
        self.assertGreater(len(validation["warnings"]), 0)

    def test_get_engine_info(self):
        """Test engine information retrieval"""
        info = self.engine.get_engine_info()

        # Check required fields
        self.assertIn("engine_version", info)
        self.assertIn("wrapper_version", info)
        self.assertIn("phases_count", info)
        self.assertIn("validation_tiers_count", info)
        self.assertIn("capabilities", info)
        self.assertIn("constraints", info)

        # Check values
        self.assertEqual(info["engine_version"], "5.1")
        self.assertEqual(info["wrapper_version"], "6.0")
        self.assertEqual(info["phases_count"], 9)
        self.assertEqual(info["validation_tiers_count"], 3)

        # Check constraints include key preservation rules
        self.assertTrue(any("NO imports" in c for c in info["constraints"]))
        self.assertTrue(any("unchanged" in c for c in info["constraints"]))

    def test_no_ibjobrefresher_imports(self):
        """Test that engine wrapper does NOT import from IBJobRefresher"""
        import clui.pd_smis_engine as engine_module

        # Get module source
        import inspect
        source = inspect.getsource(engine_module)

        # Check for actual import statements (not in comments/docstrings)
        import_lines = [line.strip() for line in source.split('\n')
                       if line.strip().startswith(('import ', 'from '))
                       and not line.strip().startswith('#')]

        # Filter out docstring content
        actual_imports = [line for line in import_lines
                         if not line.startswith('"""') and not line.startswith("'''")]

        # Should NOT contain any imports from IBJobRefresher
        ibjob_imports = [line for line in actual_imports
                        if 'IBJobRefresher' in line]

        self.assertEqual(len(ibjob_imports), 0,
                        f"Found IBJobRefresher imports: {ibjob_imports}")

    def test_phase_sequence_immutability(self):
        """Test that get_phase_sequence returns a copy"""
        phases1 = self.engine.get_phase_sequence()
        phases2 = self.engine.get_phase_sequence()

        # Should be equal but not the same object
        self.assertEqual(phases1, phases2)
        self.assertIsNot(phases1, phases2)

        # Modifying returned list shouldn't affect engine
        phases1.append("extra_phase")
        self.assertNotEqual(len(self.engine.phases), len(phases1))

    def test_validation_tiers_immutability(self):
        """Test that get_validation_tiers returns a copy"""
        tiers1 = self.engine.get_validation_tiers()
        tiers2 = self.engine.get_validation_tiers()

        # Should be equal but not the same object
        self.assertEqual(tiers1, tiers2)
        self.assertIsNot(tiers1, tiers2)


if __name__ == '__main__':
    unittest.main()
