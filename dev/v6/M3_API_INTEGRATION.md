# Milestone 3: API Integration - TeamTailor Connectivity

## Purpose
Implement TeamTailor API client for fetching job data and metrics, enabling automatic synchronization and import capabilities.

**Success Criteria:**
- TeamTailor client can authenticate with API
- Job fetching and metrics retrieval working
- Error handling for API failures
- Configuration management secure
- Can operate without API (graceful degradation)

## Dependencies
- M1_PROJECT_FOUNDATION (must be complete)
- M2_DATA_LAYER (recommended but not required)

## Start Procedure

### Pre-flight Checks
```bash
# 1. Verify M1 is complete
[ -f "/dev/v6/M1.COMPLETE" ] && echo "✅ M1 Complete" || echo "❌ Complete M1 first"

# 2. Check Python environment
source venv/bin/activate
python -c "import requests, json" && echo "✅ Python ready"

# 3. Verify configuration template exists
[ -f "config/teamtailor_config.json.example" ] && echo "✅ Config template exists"

# 4. Check git status
git status
```

### Initialize Milestone
```bash
touch /dev/v6/M3.IN_PROGRESS
echo "M3 Started: $(date)" >> /dev/v6/execution_log.md
```

## Tasks

### Task 3.1: Create TeamTailor Client Foundation
Create `clui/teamtailor_client.py`:
```python
"""
TeamTailor API Integration for JobRefresher v6.0
Handles job and metrics fetching from TeamTailor ATS
"""
import requests
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class TeamTailorClient:
    """Client for TeamTailor API integration"""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize with configuration from user_data"""
        self.config_dir = Path(config_dir) if config_dir else Path("user_data/config")
        self.config = self._load_config()
        self.base_url = "https://api.teamtailor.com/v1"
        self.headers = self._build_headers()
        self.session = requests.Session()
        self.session.headers.update(self.headers)
```

### Task 3.2: Implement Configuration Loading
Add to `clui/teamtailor_client.py`:
```python
    def _load_config(self) -> Dict:
        """
        Load TeamTailor configuration from user_data
        Falls back to example if no config exists
        """
        config_path = self.config_dir / "teamtailor_config.json"

        # Check if user config exists
        if not config_path.exists():
            # Check for example file to copy
            example_path = Path("config/teamtailor_config.json.example")
            if example_path.exists():
                print(f"⚠️  No TeamTailor config found at {config_path}")
                print(f"   Please copy {example_path} to {config_path} and add your credentials")

                # Create directory if needed
                self.config_dir.mkdir(parents=True, exist_ok=True)

                # Copy example to user location
                import shutil
                shutil.copy(example_path, config_path)
                print(f"   Example config copied to {config_path}")

            return {}  # Return empty config

        # Load configuration
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Validate required fields
                if 'api_key' in config and config['api_key'] != 'YOUR_API_KEY_HERE':
                    return config
                else:
                    print("⚠️  TeamTailor API key not configured")
                    return {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Error loading TeamTailor config: {e}")
            return {}

    def _build_headers(self) -> Dict:
        """Build API headers with authentication"""
        if not self.config or 'api_key' not in self.config:
            return {}

        return {
            "Authorization": f"Token token={self.config['api_key']}",
            "X-Api-Version": self.config.get('api_version', '20210218'),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def is_configured(self) -> bool:
        """Check if API is properly configured"""
        return bool(self.config and 'api_key' in self.config)
```

### Task 3.3: Implement Job Fetching
Add to `clui/teamtailor_client.py`:
```python
    def fetch_job(self, job_id: str) -> Optional[Dict]:
        """
        Fetch job details from TeamTailor
        Returns job data or None if error
        """
        if not self.is_configured():
            print("❌ TeamTailor not configured")
            return None

        try:
            response = self.session.get(
                f"{self.base_url}/jobs/{job_id}",
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                job = data.get('data', {})

                # Extract relevant fields
                attributes = job.get('attributes', {})
                return {
                    'teamtailor_id': job.get('id'),
                    'title': attributes.get('title', ''),
                    'description': attributes.get('body', ''),
                    'project_description': attributes.get('pitch', ''),
                    'status': attributes.get('status', ''),
                    'created_at': attributes.get('created-at', ''),
                    'updated_at': attributes.get('updated-at', ''),
                    'remote': attributes.get('remote', False),
                    'employment_type': attributes.get('employment-type', ''),
                    'department': self._get_department(job)
                }
            elif response.status_code == 401:
                print("❌ Authentication failed - check API key")
            elif response.status_code == 404:
                print(f"❌ Job {job_id} not found")
            else:
                print(f"❌ API error: {response.status_code}")

        except requests.RequestException as e:
            print(f"❌ Network error: {e}")

        return None

    def _get_department(self, job_data: Dict) -> str:
        """Extract department from job relationships"""
        relationships = job_data.get('relationships', {})
        department = relationships.get('department', {})
        return department.get('data', {}).get('id', '')
```

### Task 3.4: Implement Job Listing
Add to `clui/teamtailor_client.py`:
```python
    def list_all_jobs(self, status: Optional[str] = None,
                      limit: int = 100) -> List[Dict]:
        """
        Fetch all jobs from TeamTailor
        Optional status filter: 'published', 'unpublished', 'archived'
        """
        if not self.is_configured():
            return []

        jobs = []
        page = 1
        has_more = True

        while has_more and len(jobs) < limit:
            params = {
                'page[number]': page,
                'page[size]': min(30, limit - len(jobs))  # API max is usually 30
            }

            if status:
                params['filter[status]'] = status

            try:
                response = self.session.get(
                    f"{self.base_url}/jobs",
                    params=params,
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()
                    page_jobs = data.get('data', [])

                    for job in page_jobs:
                        attributes = job.get('attributes', {})
                        jobs.append({
                            'teamtailor_id': job.get('id'),
                            'title': attributes.get('title', ''),
                            'status': attributes.get('status', ''),
                            'created_at': attributes.get('created-at', ''),
                            'updated_at': attributes.get('updated-at', '')
                        })

                    # Check for more pages
                    links = data.get('links', {})
                    has_more = bool(links.get('next'))
                    page += 1

                    # Rate limiting
                    time.sleep(0.5)
                else:
                    print(f"❌ Failed to fetch jobs: {response.status_code}")
                    break

            except requests.RequestException as e:
                print(f"❌ Network error fetching jobs: {e}")
                break

        return jobs
```

### Task 3.5: Implement Metrics Fetching
Add to `clui/teamtailor_client.py`:
```python
    def fetch_metrics(self, job_id: str) -> Optional[Dict]:
        """
        Fetch job application metrics
        Calculate funnel metrics from candidate stages
        """
        if not self.is_configured():
            return None

        try:
            # Fetch candidates for this job
            params = {
                'filter[job_id]': job_id,
                'page[size]': 100  # Get more candidates for better metrics
            }

            response = self.session.get(
                f"{self.base_url}/candidates",
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                candidates = data.get('data', [])

                # Calculate metrics from candidate stages
                metrics = self._calculate_funnel_metrics(candidates)
                metrics['date_measured'] = datetime.now().isoformat()
                metrics['source'] = 'teamtailor'
                metrics['job_id'] = job_id
                metrics['sample_size'] = len(candidates)

                return metrics
            else:
                print(f"❌ Failed to fetch metrics: {response.status_code}")

        except requests.RequestException as e:
            print(f"❌ Network error fetching metrics: {e}")

        return None

    def _calculate_funnel_metrics(self, candidates: List[Dict]) -> Dict:
        """Calculate funnel metrics from candidate data"""
        total = len(candidates)

        if total == 0:
            return {
                'kpis': {
                    'visit_application_rate': 0.0,
                    'application_screening_rate': 0.0,
                    'application_interview_rate': 0.0,
                    'interview_offer_rate': 0.0,
                    'offer_hire_rate': 0.0
                }
            }

        # Count candidates in each stage
        stages = {
            'applied': 0,
            'screening': 0,
            'interview': 0,
            'offer': 0,
            'hired': 0
        }

        for candidate in candidates:
            attributes = candidate.get('attributes', {})
            stage = attributes.get('stage', '').lower()

            # Map TeamTailor stages to our funnel
            if stage in ['applied', 'application']:
                stages['applied'] += 1
            elif stage in ['screening', 'phone_screen', 'review']:
                stages['screening'] += 1
            elif 'interview' in stage:
                stages['interview'] += 1
            elif stage in ['offer', 'offer_sent']:
                stages['offer'] += 1
            elif stage in ['hired', 'accepted']:
                stages['hired'] += 1

        # Calculate conversion rates
        kpis = {
            'visit_application_rate': 2.1,  # Default - would need analytics
            'application_screening_rate': (
                (stages['screening'] / stages['applied'] * 100)
                if stages['applied'] > 0 else 0.0
            ),
            'application_interview_rate': (
                (stages['interview'] / stages['applied'] * 100)
                if stages['applied'] > 0 else 0.0
            ),
            'interview_offer_rate': (
                (stages['offer'] / stages['interview'] * 100)
                if stages['interview'] > 0 else 0.0
            ),
            'offer_hire_rate': (
                (stages['hired'] / stages['offer'] * 100)
                if stages['offer'] > 0 else 0.0
            )
        }

        return {
            'kpis': {k: round(v, 2) for k, v in kpis.items()},
            'stage_counts': stages
        }
```

### Task 3.6: Implement Batch Import
Add to `clui/teamtailor_client.py`:
```python
    def import_job_batch(self, job_ids: List[str]) -> Dict[str, Any]:
        """
        Import multiple jobs in batch
        Returns summary of import results
        """
        if not self.is_configured():
            return {'error': 'TeamTailor not configured'}

        results = {
            'successful': [],
            'failed': [],
            'total': len(job_ids)
        }

        for job_id in job_ids:
            print(f"Importing job {job_id}...")

            # Fetch job data
            job_data = self.fetch_job(job_id)
            if job_data:
                results['successful'].append({
                    'id': job_id,
                    'title': job_data.get('title', '')
                })
            else:
                results['failed'].append(job_id)

            # Rate limiting
            time.sleep(1)

        return results
```

### Task 3.7: Add Connection Testing
Add to `clui/teamtailor_client.py`:
```python
    def test_connection(self) -> bool:
        """
        Test API connection and authentication
        Returns True if successful
        """
        if not self.is_configured():
            print("❌ TeamTailor not configured")
            return False

        try:
            # Try to fetch company info (lightweight endpoint)
            response = self.session.get(
                f"{self.base_url}/company",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                company = data.get('data', {}).get('attributes', {})
                print(f"✅ Connected to TeamTailor")
                print(f"   Company: {company.get('name', 'Unknown')}")
                return True
            elif response.status_code == 401:
                print("❌ Authentication failed - invalid API key")
            else:
                print(f"❌ Connection test failed: {response.status_code}")

        except requests.RequestException as e:
            print(f"❌ Network error: {e}")

        return False
```

### Task 3.8: Add Error Handling and Retry Logic
Add to `clui/teamtailor_client.py`:
```python
    def _make_request(self, method: str, endpoint: str,
                      **kwargs) -> Optional[requests.Response]:
        """
        Make API request with retry logic
        Handles rate limiting and transient errors
        """
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method,
                    f"{self.base_url}{endpoint}",
                    **kwargs
                )

                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', retry_delay))
                    print(f"Rate limited, waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue

                return response

            except requests.Timeout:
                if attempt < max_retries - 1:
                    print(f"Timeout, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print("❌ Request timed out after retries")

            except requests.RequestException as e:
                print(f"❌ Request failed: {e}")
                return None

        return None

    def get_rate_limit_status(self) -> Dict:
        """Get current rate limit status from headers"""
        if hasattr(self, '_last_response'):
            headers = self._last_response.headers
            return {
                'limit': headers.get('X-Rate-Limit-Limit'),
                'remaining': headers.get('X-Rate-Limit-Remaining'),
                'reset': headers.get('X-Rate-Limit-Reset')
            }
        return {}
```

### Task 3.9: Create Integration Helper
Add to `clui/teamtailor_client.py`:
```python
    def import_to_job_manager(self, job_id: str, job_manager) -> Optional[str]:
        """
        Import a TeamTailor job directly to JobManager
        Returns created job_id or None
        """
        # Fetch from TeamTailor
        job_data = self.fetch_job(job_id)
        if not job_data:
            return None

        # Fetch metrics
        metrics = self.fetch_metrics(job_id)

        # Create in JobManager
        local_job_id = job_manager.create_job(
            title=job_data.get('title', 'Untitled'),
            company=job_data.get('department', ''),
            description=job_data.get('description', ''),
            project=job_data.get('project_description', ''),
            kpis=metrics.get('kpis') if metrics else None
        )

        # Store TeamTailor ID in metadata
        jobs = job_manager.list_jobs()
        for job in jobs:
            if job['job_id'] == local_job_id:
                metadata_path = Path(job['path']) / "metadata.json"
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                metadata['teamtailor_id'] = job_id
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                break

        print(f"✅ Imported job {job_data.get('title')} as {local_job_id}")
        return local_job_id
```

### Task 3.10: Create Test Suite
Create `tests/test_teamtailor_client.py`:
```python
"""
Test suite for TeamTailor API client
Run with: pytest tests/test_teamtailor_client.py -v
"""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from clui.teamtailor_client import TeamTailorClient


class TestTeamTailorClient:
    """Test TeamTailor API client functionality"""

    @pytest.fixture
    def mock_config_dir(self, tmp_path):
        """Create temporary config directory"""
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        # Create test config
        config = {
            "api_key": "test_api_key_123",
            "company_id": "test_company",
            "api_version": "20210218"
        }

        with open(config_dir / "teamtailor_config.json", 'w') as f:
            json.dump(config, f)

        return config_dir

    @pytest.fixture
    def client_with_config(self, mock_config_dir):
        """Create client with test configuration"""
        return TeamTailorClient(config_dir=mock_config_dir)

    @pytest.fixture
    def client_without_config(self, tmp_path):
        """Create client without configuration"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        return TeamTailorClient(config_dir=empty_dir)

    def test_configuration_loading(self, client_with_config):
        """Test configuration is loaded correctly"""
        assert client_with_config.is_configured() == True
        assert client_with_config.config['api_key'] == 'test_api_key_123'

    def test_missing_configuration(self, client_without_config):
        """Test handling of missing configuration"""
        assert client_without_config.is_configured() == False
        assert client_without_config.config == {}

    def test_headers_generation(self, client_with_config):
        """Test API headers are generated correctly"""
        headers = client_with_config.headers
        assert 'Authorization' in headers
        assert headers['Authorization'] == 'Token token=test_api_key_123'
        assert headers['X-Api-Version'] == '20210218'

    @patch('requests.Session.get')
    def test_fetch_job(self, mock_get, client_with_config):
        """Test job fetching from API"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'id': '12345',
                'attributes': {
                    'title': 'Test Job',
                    'body': 'Job description',
                    'pitch': 'Project description',
                    'status': 'published'
                }
            }
        }
        mock_get.return_value = mock_response

        # Fetch job
        job_data = client_with_config.fetch_job('12345')

        assert job_data is not None
        assert job_data['title'] == 'Test Job'
        assert job_data['teamtailor_id'] == '12345'

    @patch('requests.Session.get')
    def test_fetch_metrics(self, mock_get, client_with_config):
        """Test metrics calculation from candidates"""
        # Mock API response with candidates
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {'attributes': {'stage': 'applied'}},
                {'attributes': {'stage': 'applied'}},
                {'attributes': {'stage': 'screening'}},
                {'attributes': {'stage': 'interview'}},
                {'attributes': {'stage': 'offer'}}
            ]
        }
        mock_get.return_value = mock_response

        # Fetch metrics
        metrics = client_with_config.fetch_metrics('12345')

        assert metrics is not None
        assert 'kpis' in metrics
        assert metrics['sample_size'] == 5

    @patch('requests.Session.get')
    def test_connection_test(self, mock_get, client_with_config):
        """Test API connection testing"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'attributes': {
                    'name': 'Test Company'
                }
            }
        }
        mock_get.return_value = mock_response

        # Test connection
        result = client_with_config.test_connection()
        assert result == True

    @patch('requests.Session.get')
    def test_error_handling(self, mock_get, client_with_config):
        """Test error handling for API failures"""
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        # Try to fetch job
        job_data = client_with_config.fetch_job('12345')
        assert job_data is None

    def test_not_configured_operations(self, client_without_config):
        """Test operations fail gracefully without configuration"""
        assert client_without_config.fetch_job('12345') is None
        assert client_without_config.fetch_metrics('12345') is None
        assert client_without_config.list_all_jobs() == []
        assert client_without_config.test_connection() == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## Validation Tests

### V3.1: Import and Configuration Test
```python
from clui.teamtailor_client import TeamTailorClient

# Test import
client = TeamTailorClient()
print(f"✅ TeamTailorClient imports successfully")

# Test configuration check
if client.is_configured():
    print("✅ TeamTailor configured")
else:
    print("⚠️  TeamTailor not configured (this is OK)")
```

### V3.2: Connection Test (if configured)
```python
from clui.teamtailor_client import TeamTailorClient

client = TeamTailorClient()
if client.is_configured():
    success = client.test_connection()
    if success:
        print("✅ TeamTailor API connection successful")
    else:
        print("❌ TeamTailor API connection failed")
else:
    print("⚠️  Skipping connection test (not configured)")
```

### V3.3: Mock API Test
```bash
# Run test suite with mocked API
pytest tests/test_teamtailor_client.py -v

# Should see all tests passing even without real API
```

### V3.4: Graceful Degradation Test
```python
from clui.teamtailor_client import TeamTailorClient

# Test without configuration
import tempfile
temp_dir = tempfile.mkdtemp()
client = TeamTailorClient(config_dir=temp_dir)

# Should handle gracefully
job = client.fetch_job("test")
assert job is None
print("✅ Handles missing config gracefully")
```

### V3.5: Integration with JobManager Test
```python
from clui.teamtailor_client import TeamTailorClient
from clui.job_manager import JobManager

client = TeamTailorClient()
jm = JobManager()

if client.is_configured():
    # Test would import a real job
    print("Would test real import here")
else:
    print("✅ Integration test ready (needs API config)")
```

## Completion Procedure

### Final Validation
```bash
# 1. Run test suite
pytest tests/test_teamtailor_client.py -v

# 2. Verify no modifications to v5.1
./dev/v6/check_preservation.sh

# 3. Test configuration handling
python -c "
from clui.teamtailor_client import TeamTailorClient
client = TeamTailorClient()
print(f'Configured: {client.is_configured()}')
print('✅ Configuration handling works')
"

# 4. Check error handling
python -c "
from clui.teamtailor_client import TeamTailorClient
client = TeamTailorClient()
job = client.fetch_job('nonexistent')
print('✅ Error handling works') if job is None else print('❌ Error handling failed')
"
```

### Mark Complete
```bash
# Commit changes
git add clui/teamtailor_client.py tests/test_teamtailor_client.py
git commit -m "M3 Complete: TeamTailor API integration"

# Mark milestone complete
mv /dev/v6/M3.IN_PROGRESS /dev/v6/M3.COMPLETE
echo "M3 Completed: $(date)" >> /dev/v6/execution_log.md
echo "✅ Milestone 3: API Integration COMPLETE"
```

### Handoff Notes
- TeamTailor client functional with graceful degradation
- Handles missing configuration appropriately
- Error handling and retry logic implemented
- Rate limiting handled
- Ready for M4 (Engine Wrapper) or M5 (CLUI Core)

## Rollback Plan

If this milestone fails:

```bash
# 1. Remove created files
rm -f clui/teamtailor_client.py
rm -f tests/test_teamtailor_client.py

# 2. Reset git
git reset --hard HEAD~1

# 3. Remove milestone marker
rm -f /dev/v6/M3.COMPLETE /dev/v6/M3.IN_PROGRESS

# 4. Note in execution log
echo "ROLLED BACK M3: $(date)" >> /dev/v6/execution_log.md
```