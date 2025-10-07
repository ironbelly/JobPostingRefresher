"""
TeamTailor API Client
Handles API integration with graceful degradation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  Warning: 'requests' library not available. TeamTailor API integration will be limited.")


class TeamTailorClient:
    """
    TeamTailor API client with graceful degradation.

    Features:
    - Fetch individual jobs
    - List all jobs
    - Retrieve performance metrics
    - Import jobs to JobManager
    - Graceful handling of missing configuration
    """

    def __init__(self, config_path: str = "user_data/config/teamtailor_config.json"):
        """
        Initialize TeamTailor client.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.available = self._check_availability()

        if not self.available:
            self.degraded_mode = True
            self.degradation_reason = self._get_degradation_reason()
        else:
            self.degraded_mode = False
            self.degradation_reason = None

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.

        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            return {
                "api_key": None,
                "api_url": "https://api.teamtailor.com/v1",
                "company_id": None
            }

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {
                "api_key": None,
                "api_url": "https://api.teamtailor.com/v1",
                "company_id": None
            }

    def _check_availability(self) -> bool:
        """
        Check if API integration is available.

        Returns:
            True if API can be used, False otherwise
        """
        if not REQUESTS_AVAILABLE:
            return False

        if not self.config.get("api_key"):
            return False

        if not self.config.get("company_id"):
            return False

        return True

    def _get_degradation_reason(self) -> str:
        """
        Determine reason for degraded mode.

        Returns:
            Human-readable degradation reason
        """
        if not REQUESTS_AVAILABLE:
            return "requests library not installed (pip install requests)"

        if not self.config_path.exists():
            return f"Configuration file not found: {self.config_path}"

        if not self.config.get("api_key"):
            return "API key not configured"

        if not self.config.get("company_id"):
            return "Company ID not configured"

        return "Unknown reason"

    def _make_request(self, endpoint: str, method: str = "GET",
                     params: Optional[Dict[str, Any]] = None,
                     data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Args:
            endpoint: API endpoint
            method: HTTP method
            params: Query parameters
            data: Request body data

        Returns:
            Dict containing success status and response data or error
        """
        if self.degraded_mode:
            return {
                "success": False,
                "error": f"API unavailable: {self.degradation_reason}",
                "degraded": True
            }

        url = f"{self.config['api_url']}/{endpoint}"
        headers = {
            "Authorization": f"Token token={self.config['api_key']}",
            "X-Api-Version": "20210218",
            "Content-Type": "application/vnd.api+json"
        }

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "status_code": response.status_code,
                    "response": response.text
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout (30s)"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Connection error - check network"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }

    def fetch_job(self, job_id: str) -> Dict[str, Any]:
        """
        Fetch a single job from TeamTailor.

        Args:
            job_id: TeamTailor job ID

        Returns:
            Dict containing job data or error
        """
        result = self._make_request(f"jobs/{job_id}")

        if not result["success"]:
            return result

        # Extract job data from JSON:API format
        job_data = result["data"].get("data", {})
        attributes = job_data.get("attributes", {})

        return {
            "success": True,
            "job_id": job_id,
            "title": attributes.get("title", ""),
            "body": attributes.get("body", ""),
            "status": attributes.get("status", ""),
            "created_at": attributes.get("created-at", ""),
            "updated_at": attributes.get("updated-at", ""),
            "raw_data": job_data
        }

    def list_all_jobs(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List all jobs from TeamTailor.

        Args:
            filters: Optional filters (status, department, etc.)

        Returns:
            Dict containing list of jobs or error
        """
        params = {
            "page[size]": filters.get("page_size", 100) if filters else 100
        }

        if filters:
            if "status" in filters:
                params["filter[status]"] = filters["status"]
            if "department" in filters:
                params["filter[department-id]"] = filters["department"]

        result = self._make_request("jobs", params=params)

        if not result["success"]:
            return result

        # Extract jobs from JSON:API format
        jobs_data = result["data"].get("data", [])
        jobs = []

        for job in jobs_data:
            attributes = job.get("attributes", {})
            jobs.append({
                "id": job.get("id"),
                "title": attributes.get("title", ""),
                "status": attributes.get("status", ""),
                "created_at": attributes.get("created-at", ""),
                "updated_at": attributes.get("updated-at", "")
            })

        return {
            "success": True,
            "count": len(jobs),
            "jobs": jobs
        }

    def fetch_metrics(self, job_id: str) -> Dict[str, Any]:
        """
        Fetch performance metrics for a job.

        Args:
            job_id: TeamTailor job ID

        Returns:
            Dict containing metrics or error
        """
        # Note: Actual metrics endpoint may vary by TeamTailor API version
        # This is a placeholder implementation
        result = self._make_request(f"jobs/{job_id}/metrics")

        if not result["success"]:
            # If metrics endpoint doesn't exist, return graceful fallback
            if result.get("status_code") == 404:
                return {
                    "success": False,
                    "error": "Metrics not available for this job",
                    "fallback": True
                }
            return result

        metrics_data = result["data"].get("data", {})
        attributes = metrics_data.get("attributes", {})

        return {
            "success": True,
            "job_id": job_id,
            "views": attributes.get("views", 0),
            "applications": attributes.get("applications", 0),
            "clicks": attributes.get("clicks", 0),
            "raw_metrics": metrics_data
        }

    def import_to_job_manager(self, job_id: str, job_manager) -> Dict[str, Any]:
        """
        Import a TeamTailor job into JobManager.

        Args:
            job_id: TeamTailor job ID
            job_manager: JobManager instance

        Returns:
            Dict containing import status
        """
        # Fetch job from TeamTailor
        fetch_result = self.fetch_job(job_id)

        if not fetch_result["success"]:
            return {
                "success": False,
                "error": f"Failed to fetch job: {fetch_result.get('error')}",
                "degraded": fetch_result.get("degraded", False)
            }

        # Extract job data
        title = fetch_result["title"]
        company = self.config.get("company_name", "Unknown Company")
        body = fetch_result["body"]

        # Create unique job ID for local storage
        local_job_id = f"tt_{job_id}"

        # Create job in JobManager
        create_result = job_manager.create_job(
            job_id=local_job_id,
            title=title,
            company=company,
            raw_data=body,
            metadata={
                "source": "teamtailor",
                "teamtailor_id": job_id,
                "imported_at": datetime.now().isoformat(),
                "original_status": fetch_result.get("status", ""),
                "tags": ["teamtailor", "imported"]
            }
        )

        if not create_result["success"]:
            return create_result

        return {
            "success": True,
            "teamtailor_job_id": job_id,
            "local_job_id": local_job_id,
            "title": title,
            "path": create_result["path"]
        }

    def batch_import_jobs(self, job_manager, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Import multiple jobs from TeamTailor.

        Args:
            job_manager: JobManager instance
            filters: Optional filters for job selection

        Returns:
            Dict containing batch import results
        """
        # List all jobs
        list_result = self.list_all_jobs(filters)

        if not list_result["success"]:
            return {
                "success": False,
                "error": f"Failed to list jobs: {list_result.get('error')}",
                "degraded": list_result.get("degraded", False)
            }

        jobs = list_result["jobs"]
        results = {
            "success": True,
            "total": len(jobs),
            "imported": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }

        for job in jobs:
            job_id = job["id"]
            import_result = self.import_to_job_manager(job_id, job_manager)

            if import_result["success"]:
                results["imported"] += 1
                results["details"].append({
                    "job_id": job_id,
                    "status": "imported",
                    "local_id": import_result["local_job_id"]
                })
            elif "already exists" in import_result.get("error", ""):
                results["skipped"] += 1
                results["details"].append({
                    "job_id": job_id,
                    "status": "skipped",
                    "reason": "already exists"
                })
            else:
                results["failed"] += 1
                results["details"].append({
                    "job_id": job_id,
                    "status": "failed",
                    "error": import_result.get("error")
                })

        return results

    def get_status(self) -> Dict[str, Any]:
        """
        Get current API client status.

        Returns:
            Dict containing status information
        """
        return {
            "available": self.available,
            "degraded_mode": self.degraded_mode,
            "degradation_reason": self.degradation_reason if self.degraded_mode else None,
            "config_loaded": self.config_path.exists(),
            "api_key_configured": bool(self.config.get("api_key")),
            "company_id_configured": bool(self.config.get("company_id")),
            "requests_library": REQUESTS_AVAILABLE
        }

    def create_sample_config(self) -> Dict[str, Any]:
        """
        Create a sample configuration file.

        Returns:
            Dict containing creation status
        """
        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        sample_config = {
            "api_key": "YOUR_TEAMTAILOR_API_KEY",
            "api_url": "https://api.teamtailor.com/v1",
            "company_id": "YOUR_COMPANY_ID",
            "company_name": "Your Company Name"
        }

        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(sample_config, f, indent=2)

            return {
                "success": True,
                "path": str(self.config_path),
                "message": "Sample configuration created. Please edit with your API credentials."
            }
        except IOError as e:
            return {
                "success": False,
                "error": f"Failed to create config: {str(e)}"
            }
