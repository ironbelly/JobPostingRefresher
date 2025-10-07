"""
Unit tests for JobManager
Tests CRUD operations, versioning, and export functionality
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from clui.job_manager import JobManager


class TestJobManager(unittest.TestCase):
    """Test suite for JobManager class"""

    def setUp(self):
        """Create temporary directory for test jobs"""
        self.test_dir = tempfile.mkdtemp()
        self.job_manager = JobManager(base_path=self.test_dir)

    def tearDown(self):
        """Clean up temporary test directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_job_success(self):
        """Test successful job creation"""
        result = self.job_manager.create_job(
            job_id="test_job_001",
            title="Senior Python Developer",
            company="TechCorp",
            raw_data="We are looking for a Senior Python Developer...",
            metadata={"tags": ["python", "senior"], "source": "manual"}
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["job_id"], "test_job_001")
        self.assertTrue(os.path.exists(result["path"]))

        # Verify files created
        job_path = Path(result["path"])
        self.assertTrue((job_path / "raw_posting.txt").exists())
        self.assertTrue((job_path / "metadata.json").exists())
        self.assertTrue((job_path / "versions").exists())
        self.assertTrue((job_path / "exports").exists())

    def test_create_job_duplicate(self):
        """Test that duplicate job creation fails"""
        # Create first job
        self.job_manager.create_job(
            job_id="test_job_002",
            title="Developer",
            company="TestCo",
            raw_data="Test content"
        )

        # Try to create duplicate
        result = self.job_manager.create_job(
            job_id="test_job_002",
            title="Another Developer",
            company="AnotherCo",
            raw_data="Another content"
        )

        self.assertFalse(result["success"])
        self.assertIn("already exists", result["error"])

    def test_list_jobs_empty(self):
        """Test listing jobs when none exist"""
        jobs = self.job_manager.list_jobs()
        self.assertEqual(len(jobs), 0)

    def test_list_jobs_multiple(self):
        """Test listing multiple jobs"""
        # Create three jobs
        for i in range(3):
            self.job_manager.create_job(
                job_id=f"test_job_{i:03d}",
                title=f"Job {i}",
                company=f"Company {i}",
                raw_data=f"Content {i}"
            )

        jobs = self.job_manager.list_jobs()
        self.assertEqual(len(jobs), 3)

    def test_list_jobs_with_filter_status(self):
        """Test filtering jobs by status"""
        # Create jobs with different statuses
        self.job_manager.create_job(
            job_id="job_raw",
            title="Raw Job",
            company="RawCo",
            raw_data="Raw content"
        )

        self.job_manager.create_job(
            job_id="job_processed",
            title="Processed Job",
            company="ProcessedCo",
            raw_data="Processed content"
        )

        # Update second job to processed
        self.job_manager.update_metadata("job_processed", {"status": "processed"})

        # Filter by status
        processed_jobs = self.job_manager.list_jobs(filter_by={"status": "processed"})
        self.assertEqual(len(processed_jobs), 1)
        self.assertEqual(processed_jobs[0]["job_id"], "job_processed")

    def test_list_jobs_with_filter_tags(self):
        """Test filtering jobs by tags"""
        self.job_manager.create_job(
            job_id="job_python",
            title="Python Job",
            company="PythonCo",
            raw_data="Python content",
            metadata={"tags": ["python", "backend"]}
        )

        self.job_manager.create_job(
            job_id="job_js",
            title="JavaScript Job",
            company="JSCo",
            raw_data="JS content",
            metadata={"tags": ["javascript", "frontend"]}
        )

        # Filter by tag
        python_jobs = self.job_manager.list_jobs(filter_by={"tags": ["python"]})
        self.assertEqual(len(python_jobs), 1)
        self.assertEqual(python_jobs[0]["job_id"], "job_python")

    def test_get_job_data_success(self):
        """Test retrieving job data"""
        self.job_manager.create_job(
            job_id="test_job_get",
            title="Test Get Job",
            company="GetCo",
            raw_data="Test get content"
        )

        result = self.job_manager.get_job_data("test_job_get")

        self.assertTrue(result["success"])
        self.assertEqual(result["job_id"], "test_job_get")
        self.assertIn("metadata", result)
        self.assertIn("raw_content", result)
        self.assertEqual(result["raw_content"], "Test get content")

    def test_get_job_data_not_found(self):
        """Test retrieving non-existent job"""
        result = self.job_manager.get_job_data("nonexistent_job")

        self.assertFalse(result["success"])
        self.assertIn("not found", result["error"])

    def test_save_processed_job(self):
        """Test saving processed job data"""
        # Create job
        self.job_manager.create_job(
            job_id="test_job_process",
            title="Test Process",
            company="ProcessCo",
            raw_data="Raw data"
        )

        # Save processed data
        processed_data = {
            "optimized_title": "Optimized Title",
            "optimized_content": "Optimized content..."
        }

        result = self.job_manager.save_processed_job(
            "test_job_process",
            processed_data,
            create_version=True
        )

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["version_id"])

        # Verify processed file exists
        job_path = Path(self.test_dir) / "test_job_process"
        self.assertTrue((job_path / "processed.json").exists())

        # Verify metadata updated
        job_data = self.job_manager.get_job_data("test_job_process")
        self.assertEqual(job_data["metadata"]["status"], "processed")

    def test_create_version(self):
        """Test version creation"""
        # Create job
        self.job_manager.create_job(
            job_id="test_job_version",
            title="Version Test",
            company="VersionCo",
            raw_data="Version data"
        )

        # Create first version
        data_v1 = {"content": "Version 1 content"}
        result_v1 = self.job_manager.create_version(
            "test_job_version",
            data_v1,
            notes="First version"
        )

        self.assertTrue(result_v1["success"])
        self.assertEqual(result_v1["version_id"], "v1")

        # Create second version
        data_v2 = {"content": "Version 2 content"}
        result_v2 = self.job_manager.create_version(
            "test_job_version",
            data_v2,
            notes="Second version"
        )

        self.assertTrue(result_v2["success"])
        self.assertEqual(result_v2["version_id"], "v2")

        # Verify version files exist
        job_path = Path(self.test_dir) / "test_job_version" / "versions"
        self.assertTrue((job_path / "v1.json").exists())
        self.assertTrue((job_path / "v2.json").exists())

    def test_export_job_json(self):
        """Test JSON export"""
        # Create and process job
        self.job_manager.create_job(
            job_id="test_export_json",
            title="Export Test",
            company="ExportCo",
            raw_data="Export data"
        )

        processed_data = {"optimized": "data"}
        self.job_manager.save_processed_job("test_export_json", processed_data)

        # Export as JSON
        result = self.job_manager.export_job("test_export_json", format="json")

        self.assertTrue(result["success"])
        self.assertTrue(result["path"].endswith(".json"))
        self.assertTrue(os.path.exists(result["path"]))

    def test_export_job_txt(self):
        """Test TXT export"""
        self.job_manager.create_job(
            job_id="test_export_txt",
            title="Export TXT",
            company="TXTCo",
            raw_data="TXT data"
        )

        result = self.job_manager.export_job("test_export_txt", format="txt")

        self.assertTrue(result["success"])
        self.assertTrue(result["path"].endswith(".txt"))
        self.assertTrue(os.path.exists(result["path"]))

    def test_export_job_html(self):
        """Test HTML export"""
        self.job_manager.create_job(
            job_id="test_export_html",
            title="Export HTML",
            company="HTMLCo",
            raw_data="HTML data"
        )

        result = self.job_manager.export_job("test_export_html", format="html")

        self.assertTrue(result["success"])
        self.assertTrue(result["path"].endswith(".html"))
        self.assertTrue(os.path.exists(result["path"]))

    def test_export_job_markdown(self):
        """Test Markdown export"""
        self.job_manager.create_job(
            job_id="test_export_md",
            title="Export MD",
            company="MDCo",
            raw_data="MD data"
        )

        result = self.job_manager.export_job("test_export_md", format="md")

        self.assertTrue(result["success"])
        self.assertTrue(result["path"].endswith(".md"))
        self.assertTrue(os.path.exists(result["path"]))

    def test_delete_job_without_confirmation(self):
        """Test that deletion requires confirmation"""
        self.job_manager.create_job(
            job_id="test_delete_noconf",
            title="Delete Test",
            company="DeleteCo",
            raw_data="Delete data"
        )

        result = self.job_manager.delete_job("test_delete_noconf", confirm=False)

        self.assertFalse(result["success"])
        self.assertIn("confirmation", result["error"])

    def test_delete_job_with_confirmation(self):
        """Test successful job deletion"""
        self.job_manager.create_job(
            job_id="test_delete_conf",
            title="Delete Test",
            company="DeleteCo",
            raw_data="Delete data"
        )

        result = self.job_manager.delete_job("test_delete_conf", confirm=True)

        self.assertTrue(result["success"])

        # Verify job no longer exists
        job_path = Path(self.test_dir) / "test_delete_conf"
        self.assertFalse(job_path.exists())

    def test_update_metadata(self):
        """Test metadata updates"""
        self.job_manager.create_job(
            job_id="test_update_meta",
            title="Original Title",
            company="OriginalCo",
            raw_data="Original data"
        )

        # Update metadata
        updates = {
            "title": "Updated Title",
            "tags": ["updated", "test"],
            "notes": "Updated notes"
        }

        result = self.job_manager.update_metadata("test_update_meta", updates)

        self.assertTrue(result["success"])
        self.assertEqual(result["metadata"]["title"], "Updated Title")
        self.assertEqual(result["metadata"]["tags"], ["updated", "test"])
        self.assertEqual(result["metadata"]["notes"], "Updated notes")

    def test_metadata_immutable_fields(self):
        """Test that certain metadata fields cannot be updated"""
        self.job_manager.create_job(
            job_id="test_immutable",
            title="Immutable Test",
            company="ImmutableCo",
            raw_data="Immutable data"
        )

        # Try to update job_id (should be ignored)
        updates = {
            "job_id": "new_id",  # Should be ignored
            "created_at": "2020-01-01",  # Should be ignored
            "title": "New Title"  # Should work
        }

        result = self.job_manager.update_metadata("test_immutable", updates)

        self.assertTrue(result["success"])
        # job_id should remain unchanged
        self.assertEqual(result["metadata"]["job_id"], "test_immutable")
        # title should be updated
        self.assertEqual(result["metadata"]["title"], "New Title")


if __name__ == '__main__':
    unittest.main()
