"""
Complete integration tests for v6.0
Run with: python3 -m unittest tests.test_integration_complete -v
"""
import unittest
import tempfile
import shutil
from pathlib import Path
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clui.job_manager import JobManager
from clui.teamtailor_client import TeamTailorClient
from clui.pd_smis_engine import PDSMISEngine


class TestCompleteIntegration(unittest.TestCase):
    """Test complete system integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.job_manager = JobManager(base_path=str(self.temp_dir))
        self.engine = PDSMISEngine()

    def tearDown(self):
        """Clean up test fixtures"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_full_workflow(self):
        """Test complete workflow: create -> process -> export"""
        # Step 1: Create job
        result = self.job_manager.create_job(
            job_id="test_001",
            title="Integration Test Job",
            company="Test Company",
            raw_data="This is a test job for integration testing of the v6.0 system."
        )

        assert result["success"]
        job_id = result["job_id"]
        print(f"✅ Created job: {job_id}")

        # Step 2: List and retrieve job
        jobs = self.job_manager.list_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["title"], "Integration Test Job")
        print("✅ Job retrieval working")

        # Step 3: Get job data
        job_data = self.job_manager.get_job_data(job_id)
        self.assertTrue(job_data["success"])
        self.assertEqual(job_data["metadata"]["title"], "Integration Test Job")
        print("✅ Get job data working")

        # Step 4: Process through engine
        engine_result = self.engine.process_job({
            "job_id": job_id,
            "title": job_data["metadata"]["title"],
            "company": job_data["metadata"]["company"],
            "raw_content": job_data["raw_content"]
        })

        self.assertTrue(engine_result["success"])
        self.assertIn("optimized_content", engine_result)
        self.assertIn("metrics", engine_result)
        print("✅ Engine processing working")

        # Step 5: Save processed job
        save_result = self.job_manager.save_processed_job(
            job_id=job_id,
            processed_data=engine_result,
            create_version=True
        )

        self.assertTrue(save_result["success"])
        print("✅ Save processed job working")

        # Step 6: Export job
        export_result = self.job_manager.export_job(job_id, format="json")
        self.assertTrue(export_result["success"])
        self.assertIn("path", export_result)
        self.assertTrue(Path(export_result["path"]).exists())
        print("✅ Export working")

        # Step 7: Delete job
        delete_result = self.job_manager.delete_job(job_id, confirm=True)
        self.assertTrue(delete_result["success"])
        jobs = self.job_manager.list_jobs()
        self.assertEqual(len(jobs), 0)
        print("✅ Deletion working")

        print("\n✅ COMPLETE WORKFLOW TEST PASSED")

    def test_data_persistence(self):
        """Test data persists across instances"""
        # Create job with first instance
        job_manager1 = JobManager(base_path=str(self.temp_dir))
        result = job_manager1.create_job(
            job_id="persist_001",
            title="Persistence Test",
            company="TestCo",
            raw_data="Test content"
        )
        self.assertTrue(result["success"])

        # Create new instance with same directory
        job_manager2 = JobManager(base_path=str(self.temp_dir))

        # Should find the job
        jobs = job_manager2.list_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["title"], "Persistence Test")
        print("✅ Data persistence working")

    def test_error_handling(self):
        """Test error handling throughout system"""
        # Test invalid job ID
        result = self.job_manager.get_job_data("nonexistent_job")
        self.assertFalse(result["success"])
        self.assertIn("error", result)

        # Create a job for testing
        create_result = self.job_manager.create_job(
            job_id="error_test",
            title="Error Test",
            company="TestCo",
            raw_data="Test content"
        )
        self.assertTrue(create_result["success"])

        # Test invalid export format
        export_result = self.job_manager.export_job("error_test", format="invalid")
        self.assertFalse(export_result["success"])

        print("✅ Error handling working")

    def test_teamtailor_graceful_degradation(self):
        """Test system works without TeamTailor configuration"""
        client = TeamTailorClient()

        # Should handle missing config gracefully
        status = client.get_status()
        self.assertFalse(status["available"])

        jobs_result = client.list_all_jobs()
        self.assertFalse(jobs_result["success"])

        print("✅ TeamTailor graceful degradation working")

    def test_engine_integration(self):
        """Test engine wrapper integration"""
        # Test with minimal job data
        result = self.engine.process_job({
            "raw_content": "Test job posting content"
        })

        self.assertTrue(result["success"])
        self.assertIn("optimized_content", result)
        self.assertIn("metrics", result)
        self.assertIn("processing_metadata", result)

        # Check metrics structure
        self.assertIn("precision_score", result["metrics"])
        self.assertIn("adversarial_score", result["metrics"])
        self.assertIn("verification_score", result["metrics"])

        print("✅ Engine integration working")


if __name__ == "__main__":
    unittest.main()
