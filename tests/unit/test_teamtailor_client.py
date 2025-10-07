"""
Unit tests for TeamTailorClient
Tests API integration with graceful degradation
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from clui.teamtailor_client import TeamTailorClient, REQUESTS_AVAILABLE
from clui.job_manager import JobManager


class TestTeamTailorClient(unittest.TestCase):
    """Test suite for TeamTailorClient class"""

    def setUp(self):
        """Create temporary directory for test configuration"""
        self.test_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.test_dir, "config", "teamtailor_config.json")

    def tearDown(self):
        """Clean up temporary test directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_init_without_config(self):
        """Test initialization without configuration file"""
        client = TeamTailorClient(config_path=self.config_path)

        self.assertFalse(client.available)
        self.assertTrue(client.degraded_mode)
        self.assertIsNotNone(client.degradation_reason)

    def test_init_with_empty_config(self):
        """Test initialization with empty configuration"""
        # Create empty config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({"api_key": None, "company_id": None}, f)

        client = TeamTailorClient(config_path=self.config_path)

        self.assertFalse(client.available)
        self.assertTrue(client.degraded_mode)

    def test_init_with_valid_config(self):
        """Test initialization with valid configuration"""
        # Create valid config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({
                "api_key": "test_key",
                "company_id": "test_company",
                "api_url": "https://api.teamtailor.com/v1"
            }, f)

        # Mock requests availability
        with patch('clui.teamtailor_client.REQUESTS_AVAILABLE', True):
            client = TeamTailorClient(config_path=self.config_path)

            # Should be available if requests is installed
            # (may be False in test environment without requests)
            self.assertEqual(client.config["api_key"], "test_key")
            self.assertEqual(client.config["company_id"], "test_company")

    def test_degraded_mode_without_requests(self):
        """Test that client enters degraded mode without requests library"""
        # Create valid config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({"api_key": "test_key", "company_id": "test_company"}, f)

        # Mock requests as unavailable
        with patch('clui.teamtailor_client.REQUESTS_AVAILABLE', False):
            client = TeamTailorClient(config_path=self.config_path)

            self.assertTrue(client.degraded_mode)
            self.assertIn("requests library", client.degradation_reason)

    def test_get_status(self):
        """Test status reporting"""
        client = TeamTailorClient(config_path=self.config_path)
        status = client.get_status()

        self.assertIn("available", status)
        self.assertIn("degraded_mode", status)
        self.assertIn("config_loaded", status)
        self.assertIn("api_key_configured", status)
        self.assertIn("company_id_configured", status)

    def test_create_sample_config(self):
        """Test sample configuration creation"""
        client = TeamTailorClient(config_path=self.config_path)
        result = client.create_sample_config()

        self.assertTrue(result["success"])
        self.assertTrue(os.path.exists(self.config_path))

        # Verify config content
        with open(self.config_path, 'r') as f:
            config = json.load(f)
            self.assertIn("api_key", config)
            self.assertIn("company_id", config)
            self.assertIn("api_url", config)

    @unittest.skipUnless(REQUESTS_AVAILABLE, "requests library not available")
    def test_fetch_job_success(self):
        """Test successful job fetch"""
        # Create valid config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({
                "api_key": "test_key",
                "company_id": "test_company",
                "api_url": "https://api.teamtailor.com/v1"
            }, f)

        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "id": "123",
                "attributes": {
                    "title": "Software Engineer",
                    "body": "Job description here",
                    "status": "open",
                    "created-at": "2024-01-01",
                    "updated-at": "2024-01-02"
                }
            }
        }
        # Mock the requests module
        with patch('requests.request', return_value=mock_response):
            client = TeamTailorClient(config_path=self.config_path)
            result = client.fetch_job("123")

            self.assertTrue(result["success"])
            self.assertEqual(result["title"], "Software Engineer")
            self.assertEqual(result["status"], "open")

    @unittest.skipUnless(REQUESTS_AVAILABLE, "requests library not available")
    def test_list_all_jobs_success(self):
        """Test successful job listing"""
        # Create valid config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({
                "api_key": "test_key",
                "company_id": "test_company",
                "api_url": "https://api.teamtailor.com/v1"
            }, f)

        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "123",
                    "attributes": {
                        "title": "Software Engineer",
                        "status": "open",
                        "created-at": "2024-01-01",
                        "updated-at": "2024-01-02"
                    }
                },
                {
                    "id": "456",
                    "attributes": {
                        "title": "Product Manager",
                        "status": "open",
                        "created-at": "2024-01-01",
                        "updated-at": "2024-01-02"
                    }
                }
            ]
        }
        # Mock the requests module
        with patch('requests.request', return_value=mock_response):
            client = TeamTailorClient(config_path=self.config_path)
            result = client.list_all_jobs()

            self.assertTrue(result["success"])
            self.assertEqual(result["count"], 2)
            self.assertEqual(len(result["jobs"]), 2)

    def test_fetch_job_degraded_mode(self):
        """Test job fetch in degraded mode"""
        client = TeamTailorClient(config_path=self.config_path)
        result = client.fetch_job("123")

        self.assertFalse(result["success"])
        self.assertTrue(result.get("degraded", False))
        self.assertIn("unavailable", result["error"])

    def test_list_all_jobs_degraded_mode(self):
        """Test job listing in degraded mode"""
        client = TeamTailorClient(config_path=self.config_path)
        result = client.list_all_jobs()

        self.assertFalse(result["success"])
        self.assertTrue(result.get("degraded", False))

    @unittest.skipUnless(REQUESTS_AVAILABLE, "requests library not available")
    def test_import_to_job_manager_success(self):
        """Test successful job import to JobManager"""
        # Create valid config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({
                "api_key": "test_key",
                "company_id": "test_company",
                "company_name": "TestCo",
                "api_url": "https://api.teamtailor.com/v1"
            }, f)

        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "id": "123",
                "attributes": {
                    "title": "Software Engineer",
                    "body": "Job description",
                    "status": "open",
                    "created-at": "2024-01-01",
                    "updated-at": "2024-01-02"
                }
            }
        }
        # Create JobManager
        jobs_dir = os.path.join(self.test_dir, "jobs")
        job_manager = JobManager(base_path=jobs_dir)

        # Mock the requests module
        with patch('requests.request', return_value=mock_response):
            client = TeamTailorClient(config_path=self.config_path)
            result = client.import_to_job_manager("123", job_manager)

            self.assertTrue(result["success"])
            self.assertEqual(result["teamtailor_job_id"], "123")
            self.assertEqual(result["local_job_id"], "tt_123")
            self.assertEqual(result["title"], "Software Engineer")

            # Verify job was created in JobManager
            job_data = job_manager.get_job_data("tt_123")
            self.assertTrue(job_data["success"])
            self.assertEqual(job_data["metadata"]["source"], "teamtailor")

    def test_import_to_job_manager_degraded_mode(self):
        """Test job import in degraded mode"""
        jobs_dir = os.path.join(self.test_dir, "jobs")
        job_manager = JobManager(base_path=jobs_dir)

        client = TeamTailorClient(config_path=self.config_path)
        result = client.import_to_job_manager("123", job_manager)

        self.assertFalse(result["success"])
        self.assertTrue(result.get("degraded", False))

    @unittest.skipUnless(REQUESTS_AVAILABLE, "requests library not available")
    def test_fetch_metrics_fallback(self):
        """Test metrics fetch with fallback"""
        # Create valid config
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({
                "api_key": "test_key",
                "company_id": "test_company",
                "api_url": "https://api.teamtailor.com/v1"
            }, f)

        # Mock 404 response (metrics not available)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        # Mock the requests module
        with patch('requests.request', return_value=mock_response):
            client = TeamTailorClient(config_path=self.config_path)
            result = client.fetch_metrics("123")

            self.assertFalse(result["success"])
            self.assertTrue(result.get("fallback", False))


if __name__ == '__main__':
    unittest.main()
