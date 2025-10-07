"""
JobManager - Multi-Job Management System
Handles CRUD operations, versioning, and export functionality
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class JobManager:
    """
    Manages multiple job postings with file-based storage.

    Features:
    - CRUD operations for job data
    - Version control for processed jobs
    - Multi-format export (JSON, TXT, HTML, Markdown)
    - Metadata tracking
    """

    def __init__(self, base_path: str = "user_data/jobs"):
        """
        Initialize JobManager with base storage path.

        Args:
            base_path: Root directory for job storage
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def create_job(self, job_id: str, title: str, company: str,
                   raw_data: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new job entry with metadata.

        Args:
            job_id: Unique identifier for the job
            title: Job title
            company: Company name
            raw_data: Original job posting content
            metadata: Additional metadata (tags, notes, source, etc.)

        Returns:
            Dict containing job creation status and path
        """
        job_path = self.base_path / job_id

        # Check if job already exists
        if job_path.exists():
            return {
                "success": False,
                "error": f"Job {job_id} already exists",
                "path": str(job_path)
            }

        # Create job directory structure
        job_path.mkdir(parents=True, exist_ok=True)
        (job_path / "versions").mkdir(exist_ok=True)
        (job_path / "exports").mkdir(exist_ok=True)

        # Prepare job metadata
        job_metadata = {
            "job_id": job_id,
            "title": title,
            "company": company,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "versions": [],
            "tags": metadata.get("tags", []) if metadata else [],
            "notes": metadata.get("notes", "") if metadata else "",
            "source": metadata.get("source", "manual") if metadata else "manual",
            "status": "raw"
        }

        # Save raw job data
        raw_file = job_path / "raw_posting.txt"
        raw_file.write_text(raw_data, encoding='utf-8')

        # Save metadata
        metadata_file = job_path / "metadata.json"
        metadata_file.write_text(json.dumps(job_metadata, indent=2), encoding='utf-8')

        return {
            "success": True,
            "job_id": job_id,
            "path": str(job_path),
            "metadata": job_metadata
        }

    def list_jobs(self, filter_by: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        List all jobs with optional filtering.

        Args:
            filter_by: Optional filters (status, tags, company, etc.)

        Returns:
            List of job metadata dictionaries
        """
        jobs = []

        if not self.base_path.exists():
            return jobs

        for job_dir in self.base_path.iterdir():
            if not job_dir.is_dir():
                continue

            metadata_file = job_dir / "metadata.json"
            if not metadata_file.exists():
                continue

            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                # Apply filters if provided
                if filter_by:
                    if "status" in filter_by and metadata.get("status") != filter_by["status"]:
                        continue
                    if "company" in filter_by and metadata.get("company") != filter_by["company"]:
                        continue
                    if "tags" in filter_by:
                        job_tags = set(metadata.get("tags", []))
                        filter_tags = set(filter_by["tags"])
                        if not filter_tags.issubset(job_tags):
                            continue

                jobs.append(metadata)

            except (json.JSONDecodeError, IOError) as e:
                # Skip corrupted metadata files
                continue

        # Sort by creation date (newest first)
        jobs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return jobs

    def get_job_data(self, job_id: str) -> Dict[str, Any]:
        """
        Retrieve complete job data including metadata and content.

        Args:
            job_id: Job identifier

        Returns:
            Dict containing metadata, raw content, and latest version
        """
        job_path = self.base_path / job_id

        if not job_path.exists():
            return {
                "success": False,
                "error": f"Job {job_id} not found"
            }

        # Load metadata
        metadata_file = job_path / "metadata.json"
        if not metadata_file.exists():
            return {
                "success": False,
                "error": f"Metadata file missing for job {job_id}"
            }

        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Load raw content
        raw_file = job_path / "raw_posting.txt"
        raw_content = ""
        if raw_file.exists():
            raw_content = raw_file.read_text(encoding='utf-8')

        # Load latest processed version if exists
        latest_version = None
        versions = metadata.get("versions", [])
        if versions:
            latest_version_id = versions[-1]
            version_file = job_path / "versions" / f"{latest_version_id}.json"
            if version_file.exists():
                with open(version_file, 'r', encoding='utf-8') as f:
                    latest_version = json.load(f)

        return {
            "success": True,
            "job_id": job_id,
            "metadata": metadata,
            "raw_content": raw_content,
            "latest_version": latest_version,
            "path": str(job_path)
        }

    def save_processed_job(self, job_id: str, processed_data: Dict[str, Any],
                          create_version: bool = True) -> Dict[str, Any]:
        """
        Save processed/optimized job data.

        Args:
            job_id: Job identifier
            processed_data: Optimized job content from PD-SMIS
            create_version: Whether to create a new version

        Returns:
            Dict containing save status and version info
        """
        job_path = self.base_path / job_id

        if not job_path.exists():
            return {
                "success": False,
                "error": f"Job {job_id} not found"
            }

        # Load metadata
        metadata_file = job_path / "metadata.json"
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Save processed data
        processed_file = job_path / "processed.json"
        processed_file.write_text(json.dumps(processed_data, indent=2), encoding='utf-8')

        # Update metadata
        metadata["updated_at"] = datetime.now().isoformat()
        metadata["status"] = "processed"

        version_id = None
        if create_version:
            # Create version
            version_result = self.create_version(job_id, processed_data)
            if version_result["success"]:
                version_id = version_result["version_id"]
                if version_id not in metadata.get("versions", []):
                    metadata.setdefault("versions", []).append(version_id)

        # Save updated metadata
        metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

        return {
            "success": True,
            "job_id": job_id,
            "version_id": version_id,
            "path": str(processed_file)
        }

    def create_version(self, job_id: str, data: Dict[str, Any],
                      notes: str = "") -> Dict[str, Any]:
        """
        Create a versioned snapshot of job data.

        Args:
            job_id: Job identifier
            data: Data to version
            notes: Version notes

        Returns:
            Dict containing version creation status
        """
        job_path = self.base_path / job_id

        if not job_path.exists():
            return {
                "success": False,
                "error": f"Job {job_id} not found"
            }

        versions_path = job_path / "versions"
        versions_path.mkdir(exist_ok=True)

        # Load metadata to get version count
        metadata_file = job_path / "metadata.json"
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Generate version ID
        version_count = len(metadata.get("versions", []))
        version_id = f"v{version_count + 1}"

        # Prepare version data
        version_data = {
            "version_id": version_id,
            "created_at": datetime.now().isoformat(),
            "notes": notes,
            "data": data
        }

        # Save version
        version_file = versions_path / f"{version_id}.json"
        version_file.write_text(json.dumps(version_data, indent=2), encoding='utf-8')

        # Update metadata with new version
        if version_id not in metadata.get("versions", []):
            metadata.setdefault("versions", []).append(version_id)
            metadata["updated_at"] = datetime.now().isoformat()
            metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

        return {
            "success": True,
            "job_id": job_id,
            "version_id": version_id,
            "path": str(version_file)
        }

    def export_job(self, job_id: str, format: str = "json",
                   version: Optional[str] = None) -> Dict[str, Any]:
        """
        Export job in specified format.

        Args:
            job_id: Job identifier
            format: Export format (json, txt, html, md)
            version: Specific version to export (defaults to latest)

        Returns:
            Dict containing export status and file path
        """
        job_data = self.get_job_data(job_id)

        if not job_data["success"]:
            return job_data

        job_path = self.base_path / job_id
        exports_path = job_path / "exports"
        exports_path.mkdir(exist_ok=True)

        # Determine data to export
        if version:
            version_file = job_path / "versions" / f"{version}.json"
            if not version_file.exists():
                return {
                    "success": False,
                    "error": f"Version {version} not found"
                }
            with open(version_file, 'r', encoding='utf-8') as f:
                export_data = json.load(f)["data"]
        else:
            # Handle case where latest_version might be None
            latest_version = job_data.get("latest_version")
            if latest_version and isinstance(latest_version, dict):
                export_data = latest_version.get("data", job_data["metadata"])
            else:
                export_data = job_data["metadata"]

        # Generate export filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_suffix = f"_{version}" if version else ""

        if format == "json":
            export_file = exports_path / f"{job_id}{version_suffix}_{timestamp}.json"
            export_file.write_text(json.dumps(export_data, indent=2), encoding='utf-8')

        elif format == "txt":
            export_file = exports_path / f"{job_id}{version_suffix}_{timestamp}.txt"
            # Convert dict to readable text
            text_content = f"Job ID: {job_id}\n"
            text_content += f"Exported: {timestamp}\n\n"
            text_content += json.dumps(export_data, indent=2)
            export_file.write_text(text_content, encoding='utf-8')

        elif format == "html":
            export_file = exports_path / f"{job_id}{version_suffix}_{timestamp}.html"
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{job_data['metadata']['title']} - {job_data['metadata']['company']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .metadata {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        pre {{ background: #f9f9f9; padding: 15px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>{job_data['metadata']['title']}</h1>
    <div class="metadata">
        <p><strong>Company:</strong> {job_data['metadata']['company']}</p>
        <p><strong>Job ID:</strong> {job_id}</p>
        <p><strong>Exported:</strong> {timestamp}</p>
    </div>
    <h2>Job Data</h2>
    <pre>{json.dumps(export_data, indent=2)}</pre>
</body>
</html>"""
            export_file.write_text(html_content, encoding='utf-8')

        elif format == "md":
            export_file = exports_path / f"{job_id}{version_suffix}_{timestamp}.md"
            md_content = f"""# {job_data['metadata']['title']}

**Company:** {job_data['metadata']['company']}
**Job ID:** {job_id}
**Exported:** {timestamp}

## Job Data

```json
{json.dumps(export_data, indent=2)}
```
"""
            export_file.write_text(md_content, encoding='utf-8')

        else:
            return {
                "success": False,
                "error": f"Unsupported format: {format}"
            }

        return {
            "success": True,
            "job_id": job_id,
            "format": format,
            "path": str(export_file)
        }

    def delete_job(self, job_id: str, confirm: bool = False) -> Dict[str, Any]:
        """
        Delete a job and all associated data.

        Args:
            job_id: Job identifier
            confirm: Safety confirmation flag

        Returns:
            Dict containing deletion status
        """
        if not confirm:
            return {
                "success": False,
                "error": "Deletion requires confirmation flag"
            }

        job_path = self.base_path / job_id

        if not job_path.exists():
            return {
                "success": False,
                "error": f"Job {job_id} not found"
            }

        # Remove entire job directory
        shutil.rmtree(job_path)

        return {
            "success": True,
            "job_id": job_id,
            "message": "Job deleted successfully"
        }

    def update_metadata(self, job_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update job metadata fields.

        Args:
            job_id: Job identifier
            updates: Dictionary of fields to update

        Returns:
            Dict containing update status
        """
        job_path = self.base_path / job_id

        if not job_path.exists():
            return {
                "success": False,
                "error": f"Job {job_id} not found"
            }

        metadata_file = job_path / "metadata.json"
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Update allowed fields
        allowed_fields = ["title", "company", "tags", "notes", "status"]
        for field in allowed_fields:
            if field in updates:
                metadata[field] = updates[field]

        metadata["updated_at"] = datetime.now().isoformat()

        # Save updated metadata
        metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

        return {
            "success": True,
            "job_id": job_id,
            "metadata": metadata
        }
