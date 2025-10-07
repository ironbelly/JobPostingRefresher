"""
Performance benchmark tests
Run with: python3 -m unittest tests.test_performance -v
"""
import unittest
import time
import tempfile
from pathlib import Path
import sys
import os
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clui.job_manager import JobManager


class TestPerformance(unittest.TestCase):
    """Performance benchmark tests"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.job_manager = JobManager(base_path=self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)

    def test_job_creation_performance(self):
        """Test job creation performance"""
        start_time = time.time()

        for i in range(10):
            self.job_manager.create_job(
                job_id=f"perf_test_{i:03d}",
                title=f"Performance Test Job {i}",
                company="TestCo",
                raw_data=f"Test job description for performance test {i}"
            )

        elapsed = time.time() - start_time

        # Should create 10 jobs in under 5 seconds
        self.assertLess(elapsed, 5.0, f"Job creation too slow: {elapsed:.2f}s")
        print(f"✅ Created 10 jobs in {elapsed:.2f}s")

    def test_job_listing_performance(self):
        """Test job listing performance with many jobs"""
        # Create 50 jobs
        for i in range(50):
            self.job_manager.create_job(
                job_id=f"list_test_{i:03d}",
                title=f"Job {i}",
                company="TestCo",
                raw_data=f"Content {i}"
            )

        start_time = time.time()
        jobs = self.job_manager.list_jobs()
        elapsed = time.time() - start_time

        self.assertEqual(len(jobs), 50)
        self.assertLess(elapsed, 1.0, f"Job listing too slow: {elapsed:.2f}s")
        print(f"✅ Listed 50 jobs in {elapsed:.2f}s")

    def test_job_retrieval_performance(self):
        """Test job retrieval performance"""
        # Create test job
        result = self.job_manager.create_job(
            job_id="retrieval_test",
            title="Retrieval Test",
            company="TestCo",
            raw_data="Test content for retrieval"
        )
        job_id = result["job_id"]

        start_time = time.time()

        for i in range(20):
            job_data = self.job_manager.get_job_data(job_id)
            self.assertTrue(job_data["success"])

        elapsed = time.time() - start_time

        self.assertLess(elapsed, 2.0, f"Job retrieval too slow: {elapsed:.2f}s")
        print(f"✅ Retrieved job 20 times in {elapsed:.2f}s")

    def test_version_creation_performance(self):
        """Test version creation performance"""
        result = self.job_manager.create_job(
            job_id="version_test",
            title="Version Test",
            company="TestCo",
            raw_data="Test content"
        )
        job_id = result["job_id"]

        start_time = time.time()

        for i in range(5):
            version_result = self.job_manager.create_version(
                job_id=job_id,
                data={"iteration": i},
                notes=f"Version {i+2}"
            )
            self.assertTrue(version_result["success"])

        elapsed = time.time() - start_time

        # Check that versions were created
        job_data = self.job_manager.get_job_data(job_id)
        self.assertTrue(job_data["success"])

        self.assertLess(elapsed, 3.0, f"Version creation too slow: {elapsed:.2f}s")
        print(f"✅ Created 5 versions in {elapsed:.2f}s")

    def test_export_performance(self):
        """Test export performance"""
        # Create test job
        result = self.job_manager.create_job(
            job_id="export_test",
            title="Export Test",
            company="TestCo",
            raw_data="Test content for export"
        )
        job_id = result["job_id"]

        start_time = time.time()

        # Export in multiple formats
        for format in ["json", "txt", "md"]:
            export_result = self.job_manager.export_job(job_id, format=format)
            self.assertTrue(export_result["success"])

        elapsed = time.time() - start_time

        self.assertLess(elapsed, 2.0, f"Export too slow: {elapsed:.2f}s")
        print(f"✅ Exported job in 3 formats in {elapsed:.2f}s")


if __name__ == "__main__":
    unittest.main()
