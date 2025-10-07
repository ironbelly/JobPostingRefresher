# Milestone 2: Data Layer - Job Management System

## Purpose
Implement the complete job management system with versioning, providing the foundation for all job operations without any external dependencies.

**Success Criteria:**
- JobManager class fully functional
- Job CRUD operations working
- Version management implemented
- Search and export capabilities ready
- All operations work with file-based storage

## Dependencies
- M1_PROJECT_FOUNDATION (must be complete)

## Start Procedure

### Pre-flight Checks
```bash
# 1. Verify M1 is complete
[ -f "/dev/v6/M1.COMPLETE" ] && echo "✅ M1 Complete" || echo "❌ Complete M1 first"

# 2. Verify directory structure
[ -d "clui" ] && echo "✅ clui/ exists" || echo "❌ clui/ missing"
[ -d "user_data/jobs" ] && echo "✅ user_data/jobs/ exists" || echo "❌ user_data/jobs/ missing"

# 3. Activate Python environment
source venv/bin/activate
python -c "import json, shutil, pathlib" && echo "✅ Python ready"

# 4. Check git status
git status
```

### Initialize Milestone
```bash
touch /dev/v6/M2.IN_PROGRESS
echo "M2 Started: $(date)" >> /dev/v6/execution_log.md
```

## Tasks

### Task 2.1: Create JobManager Foundation
Create `clui/job_manager.py`:
```python
"""
Job Management System for JobRefresher v6.0
Handles all job CRUD operations, versioning, and data persistence
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import re


class JobManager:
    """Manages job data with file-based storage and versioning"""

    def __init__(self, jobs_dir: Optional[Path] = None):
        """Initialize JobManager with specified or default jobs directory"""
        self.jobs_dir = Path(jobs_dir) if jobs_dir else Path("user_data/jobs")
        self.jobs_dir.mkdir(parents=True, exist_ok=True)

    def _slugify(self, text: str) -> str:
        """Convert text to filesystem-safe slug"""
        # Remove special characters, lowercase, replace spaces with underscores
        text = re.sub(r'[^\w\s-]', '', text.lower())
        text = re.sub(r'[-\s]+', '_', text)
        return text[:50]  # Limit length
```

### Task 2.2: Implement Job Listing
Add to `clui/job_manager.py`:
```python
    def list_jobs(self, status_filter: Optional[str] = None) -> List[Dict]:
        """
        List all jobs with optional status filtering
        Returns list of job information dictionaries
        """
        jobs = []

        for job_dir in self.jobs_dir.iterdir():
            if job_dir.is_dir() and not job_dir.name.startswith('.'):
                job_info = self._read_job_info(job_dir)

                # Apply status filter if specified
                if status_filter and job_info.get('status') != status_filter:
                    continue

                jobs.append(job_info)

        # Sort by creation date (newest first)
        jobs.sort(key=lambda x: x.get('created_date', ''), reverse=True)
        return jobs

    def _read_job_info(self, job_path: Path) -> Dict:
        """Read job metadata and current version info"""
        info = {
            "path": str(job_path),
            "name": job_path.name,
            "job_id": job_path.name.split('_', 1)[0] if '_' in job_path.name else job_path.name
        }

        # Read metadata.json
        metadata_path = job_path / "metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    info.update(metadata)
            except (json.JSONDecodeError, IOError) as e:
                info['metadata_error'] = str(e)

        # Read current version
        current_version_path = job_path / "current_version.txt"
        if current_version_path.exists():
            try:
                with open(current_version_path, 'r', encoding='utf-8') as f:
                    info['current_version'] = f.read().strip()
            except IOError:
                info['current_version'] = 'v1'
        else:
            info['current_version'] = 'v1'

        # Check if has metrics
        version_path = job_path / info['current_version'] / 'metrics.json'
        info['has_metrics'] = version_path.exists()

        return info
```

### Task 2.3: Implement Job Creation
Add to `clui/job_manager.py`:
```python
    def create_job(self, title: str, company: Optional[str] = None,
                   description: Optional[str] = None,
                   project: Optional[str] = None,
                   kpis: Optional[Dict] = None) -> str:
        """
        Create a new job with initial version v1
        Returns the job_id of created job
        """
        # Generate job ID and directory name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        job_id = f"job_{timestamp}"
        title_slug = self._slugify(title)
        job_dir_name = f"{job_id}_{title_slug}"

        # Create job directory structure
        job_path = self.jobs_dir / job_dir_name
        job_path.mkdir(parents=True, exist_ok=True)

        # Create v1 directory
        v1_path = job_path / "v1"
        v1_path.mkdir(exist_ok=True)

        # Create metadata.json
        metadata = {
            "job_id": job_id,
            "title": title,
            "company": company or "",
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "status": "draft",
            "tags": []
        }

        with open(job_path / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        # Create current_version.txt
        with open(job_path / "current_version.txt", 'w', encoding='utf-8') as f:
            f.write("v1")

        # Create content files in v1
        with open(v1_path / "title.md", 'w', encoding='utf-8') as f:
            f.write(title)

        with open(v1_path / "posting.md", 'w', encoding='utf-8') as f:
            f.write(description or "# Job Posting\n\n[Job description to be added]")

        with open(v1_path / "project.md", 'w', encoding='utf-8') as f:
            f.write(project or "# Project Description\n\n[Project details to be added]")

        # Create metrics.json with initial KPIs
        metrics = {
            "date_measured": datetime.now().isoformat(),
            "source": "manual",
            "kpis": kpis or {
                "visit_application_rate": 0.0,
                "application_screening_rate": 0.0,
                "application_interview_rate": 0.0,
                "interview_offer_rate": 0.0,
                "offer_hire_rate": 0.0
            }
        }

        with open(v1_path / "metrics.json", 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)

        return job_id
```

### Task 2.4: Implement Version Management
Add to `clui/job_manager.py`:
```python
    def create_version(self, job_path: str) -> Path:
        """
        Create a new version of a job by copying current version
        Returns path to new version directory
        """
        job_path = Path(job_path)

        # Get current version
        current_version_file = job_path / "current_version.txt"
        if not current_version_file.exists():
            raise FileNotFoundError(f"No current_version.txt in {job_path}")

        with open(current_version_file, 'r', encoding='utf-8') as f:
            current_version = f.read().strip()

        # Calculate new version number
        current_num = int(current_version.replace('v', ''))
        new_version = f"v{current_num + 1}"

        # Copy current version to new version
        current_path = job_path / current_version
        new_path = job_path / new_version

        if not current_path.exists():
            raise FileNotFoundError(f"Current version directory {current_path} not found")

        shutil.copytree(current_path, new_path)

        # Update current version pointer
        with open(current_version_file, 'w', encoding='utf-8') as f:
            f.write(new_version)

        # Update last_modified in metadata
        metadata_path = job_path / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            metadata['last_modified'] = datetime.now().isoformat()
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)

        print(f"Created new version: {new_version}")
        return new_path

    def get_version_history(self, job_path: str) -> List[str]:
        """Get list of all versions for a job"""
        job_path = Path(job_path)
        versions = []

        for item in job_path.iterdir():
            if item.is_dir() and item.name.startswith('v'):
                versions.append(item.name)

        # Sort versions numerically
        versions.sort(key=lambda x: int(x.replace('v', '')))
        return versions
```

### Task 2.5: Implement Data Retrieval
Add to `clui/job_manager.py`:
```python
    def get_job_data(self, job_path: str, version: Optional[str] = None) -> Dict:
        """
        Read all job data for a specific version
        If version not specified, uses current version
        """
        job_path = Path(job_path)

        # Get version to read
        if version is None:
            current_version_file = job_path / "current_version.txt"
            if current_version_file.exists():
                with open(current_version_file, 'r', encoding='utf-8') as f:
                    version = f.read().strip()
            else:
                version = "v1"

        version_path = job_path / version
        if not version_path.exists():
            raise FileNotFoundError(f"Version {version} not found in {job_path}")

        # Read all components
        data = {"version": version}

        # Read title
        title_path = version_path / "title.md"
        if title_path.exists():
            with open(title_path, 'r', encoding='utf-8') as f:
                data['title'] = f.read().strip()

        # Read posting
        posting_path = version_path / "posting.md"
        if posting_path.exists():
            with open(posting_path, 'r', encoding='utf-8') as f:
                data['posting'] = f.read()

        # Read project description
        project_path = version_path / "project.md"
        if project_path.exists():
            with open(project_path, 'r', encoding='utf-8') as f:
                data['project_description'] = f.read()

        # Read metrics
        metrics_path = version_path / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path, 'r', encoding='utf-8') as f:
                data['metrics'] = json.load(f)

        # Include metadata
        metadata_path = job_path / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                data['metadata'] = json.load(f)

        return data
```

### Task 2.6: Implement Job Saving
Add to `clui/job_manager.py`:
```python
    def save_processed_job(self, job_path: str, version: str,
                          optimized_data: Dict) -> None:
        """Save processed/optimized job data to specified version"""
        job_path = Path(job_path)
        version_path = job_path / version

        if not version_path.exists():
            raise FileNotFoundError(f"Version directory {version_path} not found")

        # Save optimized title
        if 'title' in optimized_data:
            with open(version_path / "title.md", 'w', encoding='utf-8') as f:
                f.write(optimized_data['title'])

        # Save optimized posting
        if 'posting' in optimized_data:
            with open(version_path / "posting.md", 'w', encoding='utf-8') as f:
                f.write(optimized_data['posting'])

        # Save optimized project description
        if 'project_description' in optimized_data:
            with open(version_path / "project.md", 'w', encoding='utf-8') as f:
                f.write(optimized_data['project_description'])

        # Update metrics with projections
        if 'projected_metrics' in optimized_data:
            metrics_path = version_path / "metrics.json"

            if metrics_path.exists():
                with open(metrics_path, 'r', encoding='utf-8') as f:
                    metrics = json.load(f)
            else:
                metrics = {}

            metrics['projections'] = optimized_data['projected_metrics']
            metrics['optimization_date'] = datetime.now().isoformat()

            with open(metrics_path, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2)

        # Update metadata last_modified
        metadata_path = job_path / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            metadata['last_modified'] = datetime.now().isoformat()
            metadata['last_optimized'] = datetime.now().isoformat()
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)

        print(f"Saved optimized job data to {version_path}")
```

### Task 2.7: Implement Search Functionality
Add to `clui/job_manager.py`:
```python
    def search_jobs(self, query: str, status: Optional[str] = None) -> List[Dict]:
        """
        Search jobs by title or description content
        Optional status filter
        """
        results = []
        query_lower = query.lower()

        for job_dir in self.jobs_dir.iterdir():
            if not job_dir.is_dir() or job_dir.name.startswith('.'):
                continue

            job_info = self._read_job_info(job_dir)

            # Apply status filter
            if status and job_info.get('status') != status:
                continue

            # Search in title
            if query_lower in job_info.get('title', '').lower():
                results.append(job_info)
                continue

            # Search in current version content
            try:
                job_data = self.get_job_data(str(job_dir))
                if query_lower in job_data.get('posting', '').lower():
                    results.append(job_info)
                elif query_lower in job_data.get('project_description', '').lower():
                    results.append(job_info)
            except Exception:
                # Skip jobs with read errors
                pass

        return results
```

### Task 2.8: Implement Export Functionality
Add to `clui/job_manager.py`:
```python
    def export_job(self, job_path: str, format: str = "markdown",
                   output_dir: Optional[str] = None) -> str:
        """
        Export job in specified format
        Formats: markdown, json, html, text
        """
        job_path = Path(job_path)
        job_data = self.get_job_data(str(job_path))

        # Determine output directory
        if output_dir:
            output_dir = Path(output_dir)
        else:
            output_dir = Path("exports")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        job_name = job_path.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "markdown":
            filename = f"{job_name}_{timestamp}.md"
            content = self._export_markdown(job_data)
        elif format == "json":
            filename = f"{job_name}_{timestamp}.json"
            content = json.dumps(job_data, indent=2)
        elif format == "html":
            filename = f"{job_name}_{timestamp}.html"
            content = self._export_html(job_data)
        elif format == "text":
            filename = f"{job_name}_{timestamp}.txt"
            content = self._export_text(job_data)
        else:
            raise ValueError(f"Unsupported export format: {format}")

        # Write export file
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def _export_markdown(self, data: Dict) -> str:
        """Export job as formatted Markdown"""
        lines = []
        lines.append(f"# {data.get('title', 'Untitled Job')}")
        lines.append("")

        if 'metadata' in data:
            meta = data['metadata']
            lines.append("## Metadata")
            lines.append(f"- **Company**: {meta.get('company', 'N/A')}")
            lines.append(f"- **Status**: {meta.get('status', 'N/A')}")
            lines.append(f"- **Created**: {meta.get('created_date', 'N/A')}")
            lines.append(f"- **Version**: {data.get('version', 'N/A')}")
            lines.append("")

        lines.append("## Job Posting")
        lines.append(data.get('posting', '[No posting content]'))
        lines.append("")

        if 'project_description' in data:
            lines.append("## Project Description")
            lines.append(data['project_description'])
            lines.append("")

        if 'metrics' in data:
            lines.append("## Metrics")
            kpis = data['metrics'].get('kpis', {})
            for key, value in kpis.items():
                lines.append(f"- **{key}**: {value}%")

        return "\n".join(lines)

    def _export_html(self, data: Dict) -> str:
        """Export job as HTML"""
        # Convert markdown to basic HTML
        md_content = self._export_markdown(data)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{data.get('title', 'Job Export')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; }}
    </style>
</head>
<body>
    <pre>{md_content}</pre>
</body>
</html>"""
        return html

    def _export_text(self, data: Dict) -> str:
        """Export job as plain text"""
        lines = []
        lines.append(data.get('title', 'Untitled Job'))
        lines.append("=" * 50)
        lines.append("")
        lines.append("JOB POSTING")
        lines.append("-" * 30)
        lines.append(data.get('posting', '[No posting content]'))
        lines.append("")

        if 'project_description' in data:
            lines.append("PROJECT DESCRIPTION")
            lines.append("-" * 30)
            lines.append(data['project_description'])

        return "\n".join(lines)
```

### Task 2.9: Add Utility Methods
Add to `clui/job_manager.py`:
```python
    def update_job_status(self, job_path: str, status: str) -> None:
        """Update job status in metadata"""
        job_path = Path(job_path)
        metadata_path = job_path / "metadata.json"

        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {}

        metadata['status'] = status
        metadata['last_modified'] = datetime.now().isoformat()

        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

    def delete_job(self, job_path: str) -> bool:
        """Delete a job and all its versions"""
        job_path = Path(job_path)

        if job_path.exists() and job_path.is_dir():
            shutil.rmtree(job_path)
            return True
        return False

    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        """Find job by its ID"""
        for job_dir in self.jobs_dir.iterdir():
            if job_dir.is_dir() and job_id in job_dir.name:
                return self._read_job_info(job_dir)
        return None

    def compare_versions(self, job_path: str, version1: str, version2: str) -> Dict:
        """Compare two versions of a job"""
        data1 = self.get_job_data(job_path, version1)
        data2 = self.get_job_data(job_path, version2)

        comparison = {
            "version1": version1,
            "version2": version2,
            "differences": {
                "title": data1.get('title') != data2.get('title'),
                "posting": data1.get('posting') != data2.get('posting'),
                "project": data1.get('project_description') != data2.get('project_description'),
                "metrics": data1.get('metrics') != data2.get('metrics')
            }
        }

        return comparison
```

### Task 2.10: Create Test Suite
Create `tests/test_job_manager.py`:
```python
"""
Test suite for JobManager functionality
Run with: pytest tests/test_job_manager.py -v
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from clui.job_manager import JobManager


class TestJobManager:
    """Test JobManager functionality"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path)

    @pytest.fixture
    def job_manager(self, temp_dir):
        """Create JobManager with temporary directory"""
        return JobManager(temp_dir / "jobs")

    def test_create_job(self, job_manager):
        """Test job creation"""
        job_id = job_manager.create_job(
            title="Test Job",
            company="Test Company",
            description="Test description",
            project="Test project"
        )

        assert job_id.startswith("job_")

        # Verify job was created
        jobs = job_manager.list_jobs()
        assert len(jobs) == 1
        assert jobs[0]['title'] == "Test Job"

    def test_list_jobs(self, job_manager):
        """Test job listing"""
        # Create multiple jobs
        job_manager.create_job("Job 1")
        job_manager.create_job("Job 2")
        job_manager.create_job("Job 3")

        jobs = job_manager.list_jobs()
        assert len(jobs) == 3

    def test_version_management(self, job_manager):
        """Test version creation and management"""
        job_id = job_manager.create_job("Version Test Job")
        jobs = job_manager.list_jobs()
        job_path = jobs[0]['path']

        # Current version should be v1
        assert jobs[0]['current_version'] == 'v1'

        # Create new version
        new_version_path = job_manager.create_version(job_path)
        assert new_version_path.name == 'v2'

        # Check version history
        versions = job_manager.get_version_history(job_path)
        assert versions == ['v1', 'v2']

    def test_get_job_data(self, job_manager):
        """Test reading job data"""
        job_id = job_manager.create_job(
            title="Data Test Job",
            description="Test posting content",
            project="Test project content"
        )

        jobs = job_manager.list_jobs()
        job_data = job_manager.get_job_data(jobs[0]['path'])

        assert job_data['title'] == "Data Test Job"
        assert "Test posting content" in job_data['posting']
        assert "Test project content" in job_data['project_description']
        assert 'metrics' in job_data

    def test_save_processed_job(self, job_manager):
        """Test saving optimized job data"""
        job_id = job_manager.create_job("Save Test Job")
        jobs = job_manager.list_jobs()
        job_path = jobs[0]['path']

        # Save optimized data
        optimized_data = {
            'title': 'Optimized Title',
            'posting': 'Optimized posting content',
            'projected_metrics': {
                'visit_application_rate': 5.0
            }
        }

        job_manager.save_processed_job(job_path, 'v1', optimized_data)

        # Verify saved data
        updated_data = job_manager.get_job_data(job_path)
        assert updated_data['title'] == 'Optimized Title'
        assert updated_data['posting'] == 'Optimized posting content'
        assert 'projections' in updated_data['metrics']

    def test_search_jobs(self, job_manager):
        """Test job search functionality"""
        job_manager.create_job("Frontend Developer", description="React experience required")
        job_manager.create_job("Backend Engineer", description="Python expertise needed")
        job_manager.create_job("Full Stack Developer", description="React and Python")

        # Search by title
        results = job_manager.search_jobs("Frontend")
        assert len(results) == 1
        assert "Frontend" in results[0]['title']

        # Search by content
        results = job_manager.search_jobs("React")
        assert len(results) == 2

    def test_export_job(self, job_manager, temp_dir):
        """Test job export functionality"""
        job_id = job_manager.create_job(
            title="Export Test Job",
            description="Test content for export"
        )

        jobs = job_manager.list_jobs()
        job_path = jobs[0]['path']

        # Test markdown export
        export_path = job_manager.export_job(
            job_path,
            format="markdown",
            output_dir=str(temp_dir / "exports")
        )

        assert Path(export_path).exists()
        with open(export_path, 'r') as f:
            content = f.read()
            assert "Export Test Job" in content
            assert "Test content for export" in content

        # Test JSON export
        json_path = job_manager.export_job(
            job_path,
            format="json",
            output_dir=str(temp_dir / "exports")
        )
        assert Path(json_path).exists()

    def test_delete_job(self, job_manager):
        """Test job deletion"""
        job_id = job_manager.create_job("Delete Test Job")
        jobs = job_manager.list_jobs()
        assert len(jobs) == 1

        # Delete job
        deleted = job_manager.delete_job(jobs[0]['path'])
        assert deleted == True

        # Verify deletion
        jobs = job_manager.list_jobs()
        assert len(jobs) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## Validation Tests

### V2.1: Import and Basic Functionality Test
```python
# Run in Python
from clui.job_manager import JobManager

# Test import works
jm = JobManager()
print("✅ JobManager imports successfully")

# Test job creation
job_id = jm.create_job("Test Job", company="Test Co")
print(f"✅ Created job: {job_id}")

# Test listing
jobs = jm.list_jobs()
print(f"✅ Listed {len(jobs)} job(s)")
```

### V2.2: Version Management Test
```python
from clui.job_manager import JobManager

jm = JobManager()
jobs = jm.list_jobs()
if jobs:
    job_path = jobs[0]['path']

    # Test version creation
    new_version = jm.create_version(job_path)
    print(f"✅ Created new version: {new_version}")

    # Test version history
    versions = jm.get_version_history(job_path)
    print(f"✅ Version history: {versions}")
```

### V2.3: Search and Export Test
```python
from clui.job_manager import JobManager

jm = JobManager()

# Create test jobs
jm.create_job("Python Developer", description="Django experience")
jm.create_job("JavaScript Developer", description="React expertise")

# Test search
results = jm.search_jobs("Python")
print(f"✅ Search found {len(results)} result(s)")

# Test export
if results:
    export_path = jm.export_job(results[0]['path'], format="markdown")
    print(f"✅ Exported to: {export_path}")
```

### V2.4: Full Test Suite
```bash
# Run pytest test suite
pytest tests/test_job_manager.py -v

# Should see all tests passing
```

### V2.5: Data Persistence Test
```bash
# Create a job, restart Python, verify job persists
python -c "from clui.job_manager import JobManager; jm = JobManager(); jm.create_job('Persistence Test')"

# New Python session
python -c "from clui.job_manager import JobManager; jm = JobManager(); jobs = jm.list_jobs(); print(f'✅ Found {len(jobs)} persisted job(s)')"
```

## Completion Procedure

### Final Validation
```bash
# 1. Run all tests
pytest tests/test_job_manager.py -v

# 2. Verify no modifications to v5.1
./dev/v6/check_preservation.sh

# 3. Test with real-world scenario
python -c "
from clui.job_manager import JobManager
jm = JobManager()

# Full workflow test
job_id = jm.create_job('Senior Developer', company='Tech Corp', description='Full stack role')
jobs = jm.list_jobs()
job_path = jobs[0]['path']

# Create new version
new_version = jm.create_version(job_path)
print(f'Created version: {new_version}')

# Save optimized data
jm.save_processed_job(job_path, 'v2', {'title': 'Senior Full Stack Developer'})

# Export
export_path = jm.export_job(job_path, 'markdown')
print(f'Exported to: {export_path}')

print('✅ Full workflow successful')
"
```

### Mark Complete
```bash
# Commit changes
git add clui/job_manager.py tests/test_job_manager.py
git commit -m "M2 Complete: Data layer - JobManager implementation"

# Mark milestone complete
mv /dev/v6/M2.IN_PROGRESS /dev/v6/M2.COMPLETE
echo "M2 Completed: $(date)" >> /dev/v6/execution_log.md
echo "✅ Milestone 2: Data Layer COMPLETE"
```

### Handoff Notes
- JobManager fully functional with all CRUD operations
- Version management working
- Search and export capabilities ready
- Test suite passing
- Ready for M3 (API Integration) or M5 (CLUI Core) - can be done in parallel

## Rollback Plan

If this milestone fails:

```bash
# 1. Remove created files
rm -f clui/job_manager.py
rm -f tests/test_job_manager.py

# 2. Clean up any test data
rm -rf user_data/jobs/job_*
rm -rf exports/

# 3. Reset git
git reset --hard HEAD~1

# 4. Remove milestone marker
rm -f /dev/v6/M2.COMPLETE /dev/v6/M2.IN_PROGRESS

# 5. Note in execution log
echo "ROLLED BACK M2: $(date)" >> /dev/v6/execution_log.md
```